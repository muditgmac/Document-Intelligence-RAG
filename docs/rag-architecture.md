# RAG Architecture

## Pipeline

```text
PDF → Loader (pypdf) → Chunker (RecursiveCharacterTextSplitter)
    → Embedder (OpenAI text-embedding-3-small) → Vector Store (pgvector)
    → [query] → Retriever (similarity search) → Prompt Builder → LLM → Answer
```

## Ingestion

- `ingestion/pdf_loader.py` extracts text page-by-page. Encrypted PDFs are
  rejected explicitly (not silently mishandled). Pages that fail extraction
  are logged and skipped; if **all** pages fail, ingestion raises a clear
  `DocumentProcessingError` (e.g. for scanned/image-only PDFs).

## Chunking

- `ingestion/chunker.py` uses `RecursiveCharacterTextSplitter` with a
  separator priority of `["\n\n", "\n", ". ", " ", ""]` — it tries to split on
  paragraph breaks first, falling back to sentences, then words, so chunks
  stay semantically coherent rather than cutting mid-sentence whenever possible.
- Default `CHUNK_SIZE=1000` characters, `CHUNK_OVERLAP=150` characters. Overlap
  ensures an answer whose relevant text spans a chunk boundary is still
  retrievable from at least one chunk.
- Each chunk retains its page number in metadata, enabling page-level
  citations in the final answer.

## Embeddings

- OpenAI `text-embedding-3-small` — chosen for a strong cost/quality tradeoff
  for a portfolio-scale project (see `docs/cost-analysis.md`).

## Vector Database

- **PostgreSQL + pgvector**, via `langchain-postgres`'s `PGVector` class.
- Chosen over Pinecone/Qdrant to avoid a second managed data store and
  per-vector hosting fees for a project at this scale; the tradeoff is that
  it doesn't natively provide managed horizontal scaling the way a dedicated
  vector DB service does — acceptable at current scale, revisit if document
  volume grows substantially (see Limitations).

## Retrieval

- `retrieval/retriever.py` runs `similarity_search_with_relevance_scores`,
  returning the top `RETRIEVAL_TOP_K` chunks, filtered by
  `RETRIEVAL_SCORE_THRESHOLD` to exclude weak/irrelevant matches.

## Reranking

- Not implemented in v0.1. A cross-encoder reranking step after initial
  retrieval (e.g. re-scoring the top 20 candidates down to the best 5) is
  listed under Future Improvements — it typically improves precision at the
  cost of added latency and a second model call.

## Generation & Citations

- See `docs/ai-architecture.md` for prompt/generation details. Citations
  returned to the API caller come directly from retrieval metadata, not
  parsed from the LLM's free-text output, so citation accuracy does not
  depend on the model correctly reformatting file/page info.
