# Setup Guide

## 1. Prerequisites

- Python 3.12+
- Docker + Docker Compose
- An OpenAI API key (embeddings are always OpenAI in v0.1)
- Optionally, an Anthropic API key if you want Claude for generation

## 2. Clone and install

```bash
git clone https://github.com/sohaggain/pdf-rag-knowledge-assistant.git
cd pdf-rag-knowledge-assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:
- Set `OPENAI_API_KEY` (required).
- Optionally set `ANTHROPIC_API_KEY` and `PRIMARY_LLM_PROVIDER=anthropic`.
- Leave `DATABASE_URL` as-is if using the provided `docker-compose.yml`.

## 4. Start PostgreSQL with pgvector

```bash
docker compose up -d postgres
```

This uses the `pgvector/pgvector:pg16` image, which ships the `vector`
extension pre-installed. `langchain-postgres` creates the required tables
automatically on first use — no manual migration step is needed.

## 5. Run the API

```bash
PYTHONPATH=src uvicorn pdf_rag.main:app --reload --app-dir src
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

## 6. Ingest a PDF

Via the API:
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/path/to/your/document.pdf"
```

Via the CLI:
```bash
python scripts/ingest_cli.py /path/to/your/document.pdf
```

## 7. Ask a question

```bash
curl -X POST http://localhost:8000/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does this document say about refunds?"}'
```
