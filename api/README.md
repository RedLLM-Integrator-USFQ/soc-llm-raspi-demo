# API + Ollama con Docker

Proyecto con 2 servicios:
- `ollama`: servidor de modelos LLM
- `api`: API en FastAPI que consume Ollama

## Requisitos
- Docker
- Docker Compose

## Levantar servicios

```bash
docker compose up --build -d
```

Ver logs:

```bash
docker compose logs -f
```

## Endpoints de la API

Base URL: `http://localhost:8000`

### 1) Health check

```bash
curl http://localhost:8000/health
```

### 2) Listar modelos disponibles en Ollama

```bash
curl http://localhost:8000/models
```

### 3) Descargar un modelo en Ollama

Esto te permite elegir después qué modelo usar en `generate`.

```bash
curl -X POST http://localhost:8000/models/pull \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2"}'
```

### 4) Generar texto con el modelo elegido

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model":"llama3.2",
    "prompt":"Explica en 3 lineas que es Docker",
    "stream": false
  }'
```

## Alternativa para descargar modelos directo en el contenedor de Ollama

```bash
docker compose exec ollama ollama pull llama3.2
```

## Apagar servicios

```bash
docker compose down
```
