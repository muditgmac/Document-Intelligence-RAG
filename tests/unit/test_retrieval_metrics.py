import pytest

from evaluation.retrieval_metrics import (
    hit_rate_at_k,
    mean_reciprocal_rank,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k_all_relevant_found():
    retrieved = ["a", "b", "c", "d"]
    relevant = {"a", "c"}

    assert recall_at_k(retrieved, relevant, k=3) == 1.0


def test_recall_at_k_partial_retrieval():
    retrieved = ["a", "x", "y", "b"]
    relevant = {"a", "b"}

    assert recall_at_k(retrieved, relevant, k=2) == 0.5


def test_recall_at_k_no_hits():
    retrieved = ["x", "y", "z"]
    relevant = {"a", "b"}

    assert recall_at_k(retrieved, relevant, k=3) == 0.0


def test_hit_rate_at_k_hit():
    retrieved = ["x", "relevant", "z"]
    relevant = {"relevant"}

    assert hit_rate_at_k(retrieved, relevant, k=2) == 1.0


def test_hit_rate_at_k_miss():
    retrieved = ["x", "y", "relevant"]
    relevant = {"relevant"}

    assert hit_rate_at_k(retrieved, relevant, k=2) == 0.0


def test_reciprocal_rank_first_position():
    retrieved = ["relevant", "x", "y"]

    assert reciprocal_rank(retrieved, {"relevant"}) == 1.0


def test_reciprocal_rank_third_position():
    retrieved = ["x", "y", "relevant"]

    assert reciprocal_rank(retrieved, {"relevant"}) == pytest.approx(1 / 3)


def test_reciprocal_rank_respects_k():
    retrieved = ["x", "y", "relevant"]

    assert reciprocal_rank(retrieved, {"relevant"}, k=2) == 0.0


def test_mean_reciprocal_rank():
    retrieved = [
        ["a", "x", "y"],
        ["x", "b", "y"],
        ["x", "y", "c"],
    ]

    relevant = [
        {"a"},
        {"b"},
        {"c"},
    ]

    expected = (1.0 + 0.5 + (1 / 3)) / 3

    assert mean_reciprocal_rank(retrieved, relevant) == pytest.approx(expected)


def test_empty_relevant_set_returns_zero():
    assert recall_at_k(["a"], set(), k=1) == 0.0
    assert hit_rate_at_k(["a"], set(), k=1) == 0.0
    assert reciprocal_rank(["a"], set()) == 0.0


@pytest.mark.parametrize("k", [0, -1])
def test_invalid_k_raises(k):
    with pytest.raises(ValueError):
        recall_at_k(["a"], {"a"}, k=k)
