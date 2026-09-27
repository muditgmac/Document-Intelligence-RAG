# Resume Project Entry

### PDF RAG Knowledge Assistant
Retrieval-Augmented Generation API for citation-grounded question-answering over PDF documents.

- Designed and built a full RAG pipeline (PDF extraction, semantic chunking,
  embedding, PostgreSQL + pgvector storage, similarity retrieval, and
  citation-grounded generation) using Python, FastAPI, and LangChain.
- Implemented a provider-agnostic LLM layer supporting both OpenAI and
  Anthropic Claude, selectable via configuration without code changes.
- Engineered defensive error handling and guardrails against hallucination —
  including a relevance-threshold gate that prevents the LLM from being
  called when no supporting context exists.
- Wrote a 12-test unit/integration suite (pytest, mocked LLM/DB calls) and a
  GitHub Actions CI pipeline running lint, tests, and a Docker build on every push.
- Containerized the full stack (API + PostgreSQL/pgvector) with Docker Compose
  for one-command local deployment.
