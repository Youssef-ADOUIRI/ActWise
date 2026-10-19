import math

import pytest

from actwise.evaluation.metrics import (
    bootstrap_ci,
    mean,
    ndcg_at_k,
    ranked_articles,
    recall_at_k,
    reciprocal_rank,
)


def test_chunks_of_one_article_count_once():
    retrieved = ["AIA-Art6-1", "AIA-Art6-2", "AIA-Art5-1"]

    assert ranked_articles(retrieved) == ["AIA-Art6", "AIA-Art5"]
    assert recall_at_k(retrieved, {"AIA-Art6", "AIA-Art9"}, 2) == 0.5


def test_recall_counts_every_gold_article():
    retrieved = ["GDPR-Art17-1", "AIA-Art5-1", "GDPR-Art21-2"]

    assert recall_at_k(retrieved, {"GDPR-Art17", "GDPR-Art21"}, 3) == 1.0
    assert recall_at_k(retrieved, {"GDPR-Art17", "GDPR-Art21"}, 1) == 0.5


def test_recall_needs_gold():
    with pytest.raises(ValueError):
        recall_at_k(["AIA-Art5-1"], set(), 5)


def test_reciprocal_rank():
    retrieved = ["AIA-Art1-1", "AIA-Art2-1", "AIA-Art5-1"]

    assert reciprocal_rank(retrieved, {"AIA-Art5"}) == pytest.approx(1 / 3)
    assert reciprocal_rank(retrieved, {"AIA-Art5"}, k=2) == 0.0
    assert reciprocal_rank(retrieved, {"GDPR-Art9"}) == 0.0


def test_ndcg_matches_hand_calculation():
    # Gold A and B retrieved at ranks 1 and 3: DCG = 1/log2(2) + 1/log2(4) = 1.5
    # Ideal order puts them at ranks 1 and 2: IDCG = 1/log2(2) + 1/log2(3)
    retrieved = ["AIA-Art5-1", "AIA-Art7-1", "AIA-Art6-2"]
    expected = 1.5 / (1 + 1 / math.log2(3))

    assert ndcg_at_k(retrieved, {"AIA-Art5", "AIA-Art6"}) == pytest.approx(expected)
    assert ndcg_at_k(["AIA-Art5-1"], {"AIA-Art5"}) == 1.0


def test_mean_of_nothing_is_zero():
    assert mean([]) == 0.0
    assert mean([1.0, 0.0]) == 0.5


def test_bootstrap_ci_brackets_the_mean_and_is_reproducible():
    values = [1.0, 0.0, 1.0, 1.0, 0.5, 0.0, 1.0, 0.0, 1.0, 1.0]

    low, high = bootstrap_ci(values, seed=1)

    assert low <= mean(values) <= high
    assert (low, high) == bootstrap_ci(values, seed=1)
    assert bootstrap_ci([0.7, 0.7, 0.7]) == (0.7, 0.7)
    assert bootstrap_ci([]) == (0.0, 0.0)
