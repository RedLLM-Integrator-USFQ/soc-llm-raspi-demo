import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

app = FastAPI(title="API + Ollama", version="1.0.0")


class GenerateRequest(BaseModel):
    model: str = Field(..., description="Nombre del modelo de Ollama")
    prompt: str = Field(..., min_length=1, description="Prompt a enviar al modelo")
    stream: bool = Field(default=False, description="Streaming de respuesta")


class PullModelRequest(BaseModel):
    model: str = Field(..., description="Nombre del modelo a descargar")


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
