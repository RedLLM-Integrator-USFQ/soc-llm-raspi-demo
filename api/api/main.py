import os
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from qdrant_client import AsyncQdrantClient
from llama_index.core import Settings, VectorStoreIndex, PromptTemplate
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:4")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "security_context")
DEFAULT_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))

SECURITY_QA_PROMPT = PromptTemplate(
    """
Eres un analista SOC. Responde usando exclusivamente el contexto de seguridad proporcionado.
No inventes informacion ni agregues conocimiento externo.
Si el contexto no contiene la respuesta, responde exactamente: "No hay contexto suficiente para responder."

Contexto:
{context_str}

Pregunta:
{query_str}

Respuesta:
""".strip()
)

_qdrant_client: AsyncQdrantClient | None = None
_index: VectorStoreIndex | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _qdrant_client, _index

    Settings.llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_URL, request_timeout=120.0)
    Settings.embed_model = OllamaEmbedding(model_name=OLLAMA_EMBED_MODEL, base_url=OLLAMA_URL)

    _qdrant_client = AsyncQdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(client=_qdrant_client, collection_name=QDRANT_COLLECTION)
    _index = VectorStoreIndex.from_vector_store(vector_store)

    try:
        yield
    finally:
        if _qdrant_client is not None:
            await _qdrant_client.close()

app = FastAPI(title="API + Ollama", version="1.0.0", lifespan=lifespan)


class GenerateRequest(BaseModel):
    model: str = Field(..., description="Nombre del modelo de Ollama")
    prompt: str = Field(..., min_length=1, description="Prompt a enviar al modelo")
    stream: bool = Field(default=False, description="Streaming de respuesta")


class PullModelRequest(BaseModel):
    model: str = Field(..., description="Nombre del modelo a descargar")


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Pregunta del usuario")
    top_k: int | None = Field(default=None, ge=1, le=20, description="Cantidad de contextos a recuperar")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/models")
async def list_models() -> Any:
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"No se pudo conectar con Ollama: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail=f"Error de Ollama: {exc.response.text}") from exc

    return response.json()


@app.post("/models/pull")
async def pull_model(payload: PullModelRequest) -> Any:
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            response = await client.post(
                f"{OLLAMA_URL}/api/pull",
                json={"name": payload.model, "stream": False},
            )
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"No se pudo conectar con Ollama: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail=f"Error de Ollama: {exc.response.text}") from exc

    return response.json()


@app.post("/generate")
async def generate(payload: GenerateRequest) -> Any:
    body = {
        "model": payload.model,
        "prompt": payload.prompt,
        "stream": payload.stream,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(f"{OLLAMA_URL}/api/generate", json=body)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"No se pudo conectar con Ollama: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail=f"Error de Ollama: {exc.response.text}") from exc

    return response.json()


def _build_query_engine(top_k: int):
    if _index is None:
        return None

    return _index.as_query_engine(
        similarity_top_k=top_k,
        text_qa_template=SECURITY_QA_PROMPT,
        use_async=True,
    )


@app.post("/query")
async def query(payload: QueryRequest) -> Any:
    top_k = payload.top_k or DEFAULT_TOP_K
    query_engine = _build_query_engine(top_k)
    if query_engine is None:
        raise HTTPException(status_code=503, detail="LlamaIndex no esta inicializado")

    try:
        response = await query_engine.aquery(payload.query)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Error en LlamaIndex: {exc}") from exc

    sources = []
    for node in response.source_nodes or []:
        text = node.node.get_text() if node.node else None
        metadata = node.node.metadata if node.node else None
        sources.append({"score": node.score, "text": text, "metadata": metadata})

    return {"answer": str(response), "sources": sources}
