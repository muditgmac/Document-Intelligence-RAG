# Interview Preparation — PDF RAG Knowledge Assistant

## Project-Specific Questions

1. **Walk me through what happens end-to-end when a user uploads a PDF.**
   File is streamed to disk with a size cap → `pypdf` extracts text per page
   (encrypted/unreadable PDFs rejected early) → text is chunked with
   `RecursiveCharacterTextSplitter` (1000 chars, 150 overlap) → chunks are
   embedded via OpenAI → embeddings + metadata (source file, page number)
   are written to PostgreSQL/pgvector → the raw uploaded file is deleted.

2. **Why did you choose pgvector over Pinecone or Qdrant?**
   At this project's scale, pgvector avoids standing up and paying for a
   second managed data store, and keeps vectors + metadata in the same
   database as everything else. The tradeoff is it doesn't offer the same
   managed horizontal scaling as a dedicated vector DB — acceptable now,
   revisit if document volume grows substantially.

3. **How do you prevent the model from hallucinating an answer?**
   Two layers: (1) if retrieval returns no chunks above the relevance
   threshold, the LLM is never called — a fixed message is returned instead;
   (2) the system prompt explicitly instructs the model to answer only from
   provided context and say "not enough information" rather than guess.

4. **How are citations generated — does the model produce them?**
   No — citations returned to the API caller come directly from retrieval
   metadata (source file, page, score), not parsed from the LLM's free text.
   This means citation accuracy doesn't depend on the model reliably
   formatting structured output.

5. **What happens if a PDF is a scanned image with no text layer?**
   `load_pdf_pages` raises a `DocumentProcessingError` if zero pages produce
   extractable text, with a clear message. OCR is explicitly out of scope for
   v0.1 and listed as a Future Improvement.

6. **Why chunk with overlap instead of clean, non-overlapping chunks?**
   An answer's relevant text can span a chunk boundary. Overlap (150 of 1000
   chars) means that text is very likely to appear fully within at least one
   chunk, at a small storage/embedding cost.

7. **How do you support both OpenAI and Anthropic?**
   `generation/llm_client.py` exposes a single `generate_answer()` function
   that branches on `PRIMARY_LLM_PROVIDER`, calling `_call_openai` or
   `_call_anthropic` — both wrapped in the same retry decorator. Callers never
   need to know which provider is active.

8. **What's your retry strategy for LLM calls?**
   `tenacity`-based exponential backoff, 3 attempts, retrying only on
   `TimeoutError`/`ConnectionError` — not on e.g. authentication errors, which
   would fail identically on every retry and should surface immediately.

9. **How is the uploaded file's lifecycle managed?**
   Written to `data/uploads/` with a UUID-prefixed name during processing,
   then deleted in a `finally` block regardless of success or failure — it
   never persists beyond the request.

10. **What would you change first if this had to scale to 10,000 documents?**
    Add an HNSW/IVFFlat index on the pgvector embedding column (currently
    relying on default exact search), and move the in-memory rate limiter and
    vector-store singleton to shared state (Redis) for multi-instance deployment.

## Architecture Questions

1. Why separate `retrieval` and `generation` into distinct modules instead of one RAG function?
2. How would you swap the embedding provider without touching the API layer?
3. What's the blast radius if the vector store connection fails mid-request?
4. Why is `main.py` the only place exceptions are mapped to HTTP status codes?
5. How does the ingestion pipeline stay identical between the API and the CLI script?
6. What's the tradeoff of a process-local vector-store singleton?
7. How would you add multi-tenant document isolation?
8. Why use Pydantic settings instead of raw `os.getenv()` calls?
9. How is the system prompt kept independently reviewable from request-time logic?
10. What's the deployment story if you needed to run this on Kubernetes instead of Compose?

## AI/Automation Questions

1. How do you evaluate whether a chunking strategy is "good" for a given document type?
2. What's the difference in outcome between `RETRIEVAL_TOP_K=3` vs `RETRIEVAL_TOP_K=10`?
3. How would you add a reranking step, and what would it cost in latency?
4. How do you decide `CHUNK_SIZE`/`CHUNK_OVERLAP` defaults?
5. What's your plan for automated RAG evaluation (precision/recall, faithfulness)?
6. How would multi-turn conversational memory change the retrieval strategy?
7. What guardrails exist against prompt injection embedded in an uploaded PDF?
8. Why is temperature set low (0.1) for generation?
9. How would you add streaming responses to `/chat/ask`?
10. What's the cost impact of increasing `max_tokens` on generation calls?

## Security Questions

1. How are secrets kept out of the codebase and version control?
2. What's the current authentication model, and what's the upgrade path to OAuth2/JWT?
3. How is SQL injection prevented given the app writes to PostgreSQL?
4. What's the biggest unaddressed security limitation of the current design?
5. How is uploaded file content prevented from persisting beyond the ingestion request?

## Failure & Scalability Questions

1. What happens if the OpenAI API is down when a user uploads a PDF?
2. What happens if PostgreSQL is unreachable when a question is asked?
3. How would duplicate/retry uploads of the same PDF be handled today, and what's missing?
4. How does the in-memory rate limiter behave across multiple running instances?
5. What's the first bottleneck you'd expect under high concurrent load, and how would you address it?
