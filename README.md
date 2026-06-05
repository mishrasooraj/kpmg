# KPMG AI Data Platform

FastAPI application scaffold for enterprise AI and data engineering workloads:

- Async Python/FastAPI REST APIs
- LangChain chat integration with OpenAI and Claude
- LangGraph multi-agent workflow orchestration
- PostgreSQL with Alembic migrations and pgvector embeddings
- Azure data workflow boundary for ADF, Storage, Functions, and Logic Apps
- Dockerized API and PostgreSQL stack

## Run Locally

```bash
cp .env.example .env
docker compose up --build
```

API docs are available at `http://localhost:8000/docs`.

## Migrations

```bash
docker compose run --rm api alembic upgrade head
```

## Example Requests

```bash
curl http://localhost:8000/api/v1/health
```

```bash
curl -X POST http://localhost:8000/api/v1/ai/agents/run \
  -H "Content-Type: application/json" \
  -d '{"objective":"Design a compliant RAG platform","context":{"client":"enterprise"}}'
```

```bash
curl -X POST http://localhost:8000/api/v1/data/pipelines/run \
  -H "Content-Type: application/json" \
  -d '{"pipeline_name":"customer_ingestion","source_uri":"sftp://source","target_uri":"az://landing","parameters":{"mode":"incremental"}}'
```
