"""Information-retrieval metrics for evaluating RAG retrieval quality."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence


def _validate_k(k: int) -> None:
    if not isinstance(k, int):
        raise TypeError("k must be an integer")
    if k <= 0:
        raise ValueError("k must be greater than 0")


def recall_at_k(
    retrieved_ids: Sequence[Hashable],
    relevant_ids: Iterable[Hashable],
    k: int,
) -> float:
    """Return the fraction of relevant items retrieved in the top-k results.

    Recall@K =
        (# relevant documents retrieved in top K)
        /
        (# relevant documents)
    """
    _validate_k(k)

    relevant = set(relevant_ids)
    if not relevant:
        return 0.0

    retrieved_top_k = set(retrieved_ids[:k])
    hits = retrieved_top_k.intersection(relevant)

    return len(hits) / len(relevant)


def hit_rate_at_k(
    retrieved_ids: Sequence[Hashable],
    relevant_ids: Iterable[Hashable],
    k: int,
) -> float:
    """Return 1.0 when top-k contains at least one relevant item, else 0.0."""
    _validate_k(k)

    relevant = set(relevant_ids)
    if not relevant:
        return 0.0

    return float(any(item_id in relevant for item_id in retrieved_ids[:k]))


def reciprocal_rank(
    retrieved_ids: Sequence[Hashable],
    relevant_ids: Iterable[Hashable],
    k: int | None = None,
) -> float:
    """Return reciprocal rank of the first relevant retrieved item.

    Example:
        First relevant item appears at rank 3 -> RR = 1 / 3.
    """
    relevant = set(relevant_ids)
    if not relevant:
        return 0.0

    if k is not None:
        _validate_k(k)
        candidates = retrieved_ids[:k]
    else:
        candidates = retrieved_ids

    for rank, item_id in enumerate(candidates, start=1):
        if item_id in relevant:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    retrieved_batches: Sequence[Sequence[Hashable]],
    relevant_batches: Sequence[Iterable[Hashable]],
    k: int | None = None,
) -> float:
    """Return MRR across multiple queries."""
    if len(retrieved_batches) != len(relevant_batches):
        raise ValueError(
            "retrieved_batches and relevant_batches must contain "
            "the same number of queries"
        )

    if not retrieved_batches:
        return 0.0

    reciprocal_ranks = [
        reciprocal_rank(retrieved, relevant, k=k)
        for retrieved, relevant in zip(
            retrieved_batches,
            relevant_batches,
            strict=True,
        )
    ]

    return sum(reciprocal_ranks) / len(reciprocal_ranks)
