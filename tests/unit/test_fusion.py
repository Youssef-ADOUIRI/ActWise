import pytest

from actwise.retrieval.fusion import rrf


def test_rrf():
    """Scores are 1 / (k + rank) summed over the lists; a key found in both lists wins."""
    fused = rrf([["a", "b", "c"], ["c", "d"]], k=60)

    assert fused[0][0] == "c"
    assert dict(fused)["c"] == pytest.approx(1 / 63 + 1 / 61)
    assert dict(fused)["a"] == pytest.approx(1 / 61)
    assert [key for key, _ in fused] == ["c", "a", "b", "d"]


def test_rrf_ties_keep_the_first_list_first():
    """Equal scores keep the order in which the keys first appear."""
    assert [key for key, _ in rrf([["dense"], ["bm25"]])] == ["dense", "bm25"]
