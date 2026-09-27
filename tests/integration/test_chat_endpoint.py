"""
Integration tests for the /chat/ask endpoint.

These tests mock the retrieval and generation layers so they run without a
live PostgreSQL/pgvector instance or real LLM API keys, keeping CI fast and
free. True end-to-end tests against a real database live in tests/e2e and
are run separately (see docs/testing.md).
"""

import sys
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pdf_rag.main import app
from pdf_rag.retrieval.retriever import RetrievedChunk

client = TestClient(app)


def test_ask_with_no_relevant_chunks_returns_graceful_message():
    with patch("pdf_rag.api.routes.chat.retrieve_relevant_chunks", return_value=[]):
        response = client.post("/chat/ask", json={"question": "What is in the document?"})

    assert response.status_code == 200
    body = response.json()
    assert body["citations"] == []
    assert "couldn't find relevant information" in body["answer"]


def test_ask_with_chunks_returns_answer_and_citations():
    fake_chunks = [RetrievedChunk(text="Q3 revenue was $2M.", source_file="q3.pdf", page_number=4, score=0.87)]

    with (
        patch("pdf_rag.api.routes.chat.retrieve_relevant_chunks", return_value=fake_chunks),
        patch("pdf_rag.api.routes.chat.generate_answer", return_value="Q3 revenue was $2M [q3.pdf, p.4]."),
    ):
        response = client.post("/chat/ask", json={"question": "What was Q3 revenue?"})

    assert response.status_code == 200
    body = response.json()
    assert body["citations"][0]["source_file"] == "q3.pdf"
    assert body["citations"][0]["page_number"] == 4
    assert "$2M" in body["answer"]


def test_ask_rejects_empty_question():
    response = client.post("/chat/ask", json={"question": ""})
    assert response.status_code == 422
