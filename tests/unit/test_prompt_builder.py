"""Unit tests for prompt construction."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pdf_rag.generation.prompt_builder import build_context_block, build_user_prompt
from pdf_rag.retrieval.retriever import RetrievedChunk


def test_build_context_block_empty_chunks():
    result = build_context_block([])
    assert "No relevant context" in result


def test_build_context_block_includes_citations():
    chunks = [RetrievedChunk(text="Revenue grew 20%.", source_file="report.pdf", page_number=3, score=0.9)]
    result = build_context_block(chunks)

    assert "report.pdf" in result
    assert "p.3" in result
    assert "Revenue grew 20%." in result


def test_build_user_prompt_includes_question_and_context():
    chunks = [RetrievedChunk(text="Key fact.", source_file="doc.pdf", page_number=1, score=0.8)]
    prompt = build_user_prompt("What is the key fact?", chunks)

    assert "What is the key fact?" in prompt
    assert "Key fact." in prompt
    assert "doc.pdf" in prompt
