"""Unit tests for retrieval metadata and threshold behavior."""

from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from pdf_rag.config import Settings
from pdf_rag.retrieval.retriever import retrieve_relevant_chunks


def test_retriever_preserves_chunk_metadata_and_filters_low_scores():
    settings = Settings(retrieval_score_threshold=0.5)

    vector_store = MagicMock()
    vector_store.similarity_search_with_relevance_scores.return_value = [
        (
            Document(
                page_content="Revenue was $2 million.",
                metadata={
                    "chunk_id": "report.pdf::p4::c7",
                    "source_file": "report.pdf",
                    "page_number": 4,
                    "chunk_index": 7,
                },
            ),
            0.91,
        ),
        (
            Document(
                page_content="Unrelated material.",
                metadata={
                    "chunk_id": "report.pdf::p8::c15",
                    "source_file": "report.pdf",
                    "page_number": 8,
                    "chunk_index": 15,
                },
            ),
            0.20,
        ),
    ]

    with (
        patch(
            "pdf_rag.retrieval.retriever.get_embeddings_client",
            return_value=MagicMock(),
        ),
        patch(
            "pdf_rag.retrieval.retriever.get_vector_store",
            return_value=vector_store,
        ),
    ):
        chunks = retrieve_relevant_chunks(
            "What was the revenue?",
            settings,
            top_k=5,
        )

    assert len(chunks) == 1

    chunk = chunks[0]
    assert chunk.text == "Revenue was $2 million."
    assert chunk.source_file == "report.pdf"
    assert chunk.page_number == 4
    assert chunk.score == 0.91
    assert chunk.chunk_id == "report.pdf::p4::c7"
    assert chunk.chunk_index == 7

    vector_store.similarity_search_with_relevance_scores.assert_called_once_with(
        "What was the revenue?",
        k=5,
    )
