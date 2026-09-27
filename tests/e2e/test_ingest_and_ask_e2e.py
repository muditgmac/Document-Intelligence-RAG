"""
End-to-end test: ingest a real PDF into a live pgvector instance and ask a
question against it.

Skipped by default in CI (requires DATABASE_URL, OPENAI_API_KEY pointing to
real services). Run manually with:
    RUN_E2E=1 pytest tests/e2e -v
"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_E2E") != "1",
    reason="E2E tests require RUN_E2E=1 and live DATABASE_URL/OPENAI_API_KEY.",
)


def test_ingest_and_ask_roundtrip():
    from pdf_rag.config import get_settings
    from pdf_rag.ingestion.pipeline import ingest_pdf
    from pdf_rag.retrieval.retriever import retrieve_relevant_chunks

    settings = get_settings()
    sample_pdf = Path(__file__).parent / "fixtures" / "sample.pdf"

    result = ingest_pdf(sample_pdf, settings)
    assert result["chunks_created"] > 0

    chunks = retrieve_relevant_chunks("What is this document about?", settings)
    assert len(chunks) > 0
