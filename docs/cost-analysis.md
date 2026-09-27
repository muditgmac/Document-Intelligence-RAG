# Cost Analysis

No production usage exists yet, so this document explains the **calculation
method**, not measured historical spend.

## Embedding cost (one-time per document)
`OpenAI text-embedding-3-small` is billed per input token. Approximate token
count = (PDF character count) / 4. Multiply by the model's published
per-token price (check current OpenAI pricing) to estimate ingestion cost for
a given document.

## Generation cost (per question)
Each `/chat/ask` call sends: system prompt + retrieved chunks (up to
`RETRIEVAL_TOP_K` × `CHUNK_SIZE` characters) + the question, and receives up
to `max_tokens=800` tokens back. Cost scales roughly linearly with
`RETRIEVAL_TOP_K` and `CHUNK_SIZE` — reducing either lowers per-query cost at
some risk to answer quality/completeness.

## Infrastructure cost
- PostgreSQL + pgvector avoids a separate vector-DB subscription; cost is
  whatever the hosting PostgreSQL instance costs (self-hosted Docker, a small
  managed Postgres instance, or RDS).
- No autoscaling/serverless compute is configured in v0.1 (see deployment.md
  for the AWS reference architecture).

## Cost levers available to the operator
- `CHUNK_SIZE` / `CHUNK_OVERLAP` — smaller chunks reduce prompt size but may
  require a higher `RETRIEVAL_TOP_K` to preserve answer quality.
- `RETRIEVAL_TOP_K` — directly controls how much context (and therefore
  tokens) is sent per question.
- `RETRIEVAL_SCORE_THRESHOLD` — filtering weak matches avoids paying to send
  irrelevant context to the LLM.
