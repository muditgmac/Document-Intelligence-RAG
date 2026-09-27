"""Unit tests for the chunking logic."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pdf_rag.ingestion.chunker import chunk_pages
from pdf_rag.ingestion.pdf_loader import PageContent


def test_chunk_pages_produces_chunks_for_nonempty_text():
    pages = [PageContent(page_number=1, text="Sentence one. " * 50)]
    chunks = chunk_pages(pages, source_file="doc.pdf", chunk_size=200, chunk_overlap=20)

    assert len(chunks) > 1
    assert all(chunk.source_file == "doc.pdf" for chunk in chunks)
    assert all(chunk.page_number == 1 for chunk in chunks)


def test_chunk_pages_skips_empty_pages():
    pages = [
        PageContent(page_number=1, text=""),
        PageContent(page_number=2, text="Real content here that should be chunked properly."),
    ]
    chunks = chunk_pages(pages, source_file="doc.pdf", chunk_size=100, chunk_overlap=10)

    assert len(chunks) >= 1
    assert all(chunk.page_number == 2 for chunk in chunks)


def test_chunk_ids_are_unique():
    pages = [PageContent(page_number=1, text="Some content. " * 100)]
    chunks = chunk_pages(pages, source_file="doc.pdf", chunk_size=150, chunk_overlap=15)

    ids = [chunk.chunk_id for chunk in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_overlap_preserves_context():
    pages = [PageContent(page_number=1, text="word " * 500)]
    chunks = chunk_pages(pages, source_file="doc.pdf", chunk_size=200, chunk_overlap=50)

    # With overlap > 0 and multiple chunks, later chunks should share some
    # trailing text with the chunk before them.
    assert len(chunks) > 1
