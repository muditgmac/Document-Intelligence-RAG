# Security

## Secrets Management
- All credentials (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DATABASE_URL`, `API_KEY`)
  are loaded exclusively from environment variables via `pydantic-settings`.
- `.env` is listed in `.gitignore`; only `.env.example` (with empty values) is committed.
- No credentials are logged — `structlog` calls in this codebase never include
  request headers or environment values.

## Authentication
- Optional shared-secret API key via `X-API-Key` header
  (`api/dependencies.py::require_api_key`).
- **Production upgrade path:** replace with OAuth2/JWT per-user auth if the
  service is exposed to multiple untrusted clients; the current shared-secret
  model is appropriate for a single-tenant/internal deployment only.

## Authorization
- No role-based access control in v0.1 — every authenticated caller can
  upload documents and query all ingested content (single shared collection).
  See Limitations in the README.

## Input Validation
- Pydantic models validate all JSON bodies (`ChatRequest` enforces
  1–2000 char questions, `top_k` bounds).
- File uploads are restricted to `.pdf` extension and a configurable byte-size
  cap enforced during streaming (not after full upload).

## Injection Risks
- **SQL injection:** mitigated — all DB access goes through SQLAlchemy/psycopg
  parameterized queries via `langchain-postgres`; no raw string SQL is built
  from user input anywhere in this codebase.
- **Prompt injection:** a malicious PDF could contain text instructing the
  model to ignore its system prompt. Mitigation: the system prompt explicitly
  instructs the model to treat document content as data, not instructions, and
  to only answer from context. This reduces but does not eliminate risk —
  documented as a known limitation.

## Webhook Verification
- Not applicable — this service does not currently receive webhooks.

## Rate Limiting
- In-memory per-IP limiter, `RATE_LIMIT_PER_MINUTE` requests/minute.
- Single-process only; a multi-instance deployment needs a shared store
  (Redis) — documented in Future Improvements.

## PII / Data Privacy
- Uploaded PDF files are deleted from local disk immediately after ingestion
  (see `documents.py`'s `finally` block) — only extracted chunk text and
  metadata persist.
- No automatic PII detection/redaction is implemented. If ingesting documents
  containing PII, that text will be stored (as embeddings + plaintext chunks)
  in PostgreSQL and will be included verbatim in prompts sent to the LLM
  provider. Treat the vector store as containing the same sensitivity level
  as the source documents.

## Excessive Agency
- The system has no tool-calling or write-access to external systems; it only
  reads from the vector store and calls the LLM for text generation. This
  significantly limits blast radius even if prompt injection succeeds.
