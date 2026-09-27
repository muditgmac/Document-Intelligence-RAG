"""Shared pytest fixtures."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pdf_rag.config import Settings  # noqa: E402


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        openai_api_key="test-key",
        anthropic_api_key="test-key",
        database_url="postgresql+psycopg://postgres:postgres@localhost:5432/pdf_rag_test",
        api_key=None,
    )
