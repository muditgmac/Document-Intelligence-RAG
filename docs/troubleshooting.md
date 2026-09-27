# Troubleshooting

## "OPENAI_API_KEY is required for embeddings but was not set"
Set `OPENAI_API_KEY` in your `.env` file. Embeddings always use OpenAI in v0.1
regardless of `PRIMARY_LLM_PROVIDER`.

## "Failed to initialize pgvector store"
- Confirm PostgreSQL is running: `docker compose ps`
- Confirm `DATABASE_URL` in `.env` matches the running container's
  host/port/credentials.
- If using your own PostgreSQL instance (not the provided
  `pgvector/pgvector` image), ensure the `vector` extension is installed:
  `CREATE EXTENSION IF NOT EXISTS vector;`

## `/chat/ask` returns 502
This means either retrieval or generation failed. Check:
1. Has any document been ingested yet? An empty vector store returns a
   graceful "no relevant information" message, not a 502 — a 502 usually
   means the database connection itself failed, or the LLM API call failed
   (check API key validity and provider status).
2. Check application logs (structured JSON) for the specific exception message.

## Upload returns 400 "No extractable text found"
The PDF is likely a scanned image without an OCR text layer. OCR is not
implemented in v0.1 — see Future Improvements in the README.

## `ModuleNotFoundError: No module named 'pdf_rag'`
Run uvicorn with the src directory on the path:
```bash
PYTHONPATH=src uvicorn pdf_rag.main:app --reload --app-dir src
```
or run from inside `src/`.

## Tests fail with missing API key errors
Unit and integration tests do not require real API keys — set dummy values
(`OPENAI_API_KEY=test ANTHROPIC_API_KEY=test`) since the settings model
requires the keys to be present for construction, but integration tests mock
all real API calls.
