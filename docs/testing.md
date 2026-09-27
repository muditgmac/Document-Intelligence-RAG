# Testing Strategy

## Levels

| Level | Location | What it covers | External deps |
|---|---|---|---|
| Unit | `tests/unit/` | Chunking logic, prompt construction, PDF-loader error paths | None |
| Integration | `tests/integration/` | FastAPI endpoints, with retrieval/generation mocked | None (mocked) |
| End-to-End | `tests/e2e/` | Full ingest → retrieve → answer roundtrip | Live PostgreSQL + real API keys |

## Running tests

```bash
# Fast suite (CI-safe, no external services, no API costs)
pytest tests/unit tests/integration -v

# With coverage report
pytest tests/unit tests/integration --cov=src/pdf_rag --cov-report=term-missing

# Full end-to-end (opt-in, costs real API tokens)
RUN_E2E=1 pytest tests/e2e -v
```

## What is currently covered

- `test_chunker.py` — chunk count, chunk-id uniqueness, empty-page skipping,
  overlap behavior.
- `test_prompt_builder.py` — citation formatting, empty-context handling,
  question inclusion in the final prompt.
- `test_pdf_loader.py` — missing-file error handling.
- `test_api_health.py` — `/health` returns `200` with the correct shape.
- `test_chat_endpoint.py` — graceful "no relevant info" response, successful
  answer + citation shape, and `422` on an empty question.

## AI-specific testing notes

Because LLM output is non-deterministic, integration tests assert on
**structure** (citation fields present, correct source/page echoed back) and
**behavior** (empty retrieval → no LLM call) rather than exact generated text.
A dedicated AI-quality evaluation harness (retrieval precision/recall, answer
faithfulness scoring) is listed under Future Improvements and is intentionally
out of scope for the current test suite.

## CI

`.github/workflows/ci.yml` runs `ruff`, `black --check`, the unit+integration
suite with coverage, and a Docker build on every push/PR to `main`.
