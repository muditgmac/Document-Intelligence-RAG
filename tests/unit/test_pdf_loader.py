"""Unit tests for PDF loading error handling (no real PDF binary needed here)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pdf_rag.core.exceptions import DocumentProcessingError
from pdf_rag.ingestion.pdf_loader import load_pdf_pages


def test_load_pdf_pages_missing_file_raises():
    with pytest.raises(DocumentProcessingError):
        load_pdf_pages("/tmp/does-not-exist-12345.pdf")
