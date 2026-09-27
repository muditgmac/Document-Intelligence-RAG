# Demo Video Script (Target: 2:30–3:00)

## 0:00–0:20 — Problem
"Teams have PDFs full of knowledge — handbooks, contracts, manuals — that are
slow to search and impossible to safely paste into a generic chatbot.
This is a RAG API that answers questions from your own PDFs, with citations."

## 0:20–0:40 — Architecture
Show the Mermaid architecture diagram from the README. Walk through: PDF →
chunk → embed → pgvector → retrieve → LLM → cited answer.

## 0:40–2:00 — Live Demo
1. Start the stack: `docker compose up --build`
2. Open `/docs` Swagger UI.
3. Upload a sample PDF via `/documents/upload` — show the response
   (`pages_processed`, `chunks_created`).
4. Ask a question via `/chat/ask` that the PDF actually answers — show the
   returned answer and the `citations` array with file + page number.
5. Ask a question the PDF does NOT cover — show the graceful "not enough
   information" response instead of a hallucinated answer.
6. Briefly show a failed upload (e.g. a `.txt` file) returning a clean `400`
   error.

## 2:00–2:30 — Technology
"Built with FastAPI, LangChain, PostgreSQL + pgvector for vector storage, and
a provider-agnostic LLM layer supporting both OpenAI and Anthropic Claude.
Fully tested — 12 passing unit and integration tests — and containerized with
Docker Compose for one-command startup."

## 2:30–3:00 — Business Value
"This pattern — grounded, cited answers instead of free-form LLM guesses — is
directly applicable to internal knowledge bases, contract review, and
customer support use cases where trust in the source of an answer matters as
much as the answer itself."
