import pytest

from actwise.retrieval.fusion import fuse_hits, rrf
from actwise.retrieval.passages import Passage, to_hit


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


def test_fuse_hits_merges_rankings_by_storage_key():
    """A passage found by two queries comes first; the EN and FR copies stay apart."""
    art2 = to_hit(Passage("AIA-Art2-1", "en", "scope"), 0.1)
    art2_fr = to_hit(Passage("AIA-Art2-1", "fr", "champ"), 0.1)
    art99 = to_hit(Passage("AIA-Art99-3", "en", "fines"), 0.9)

    fused = fuse_hits([[art99, art2], [art2, art2_fr]])

    assert [hit.key for hit in fused] == ["AIA-Art2-1@en", "AIA-Art99-3@en", "AIA-Art2-1@fr"]
    assert fused[0].score == pytest.approx(1 / 62 + 1 / 61)
