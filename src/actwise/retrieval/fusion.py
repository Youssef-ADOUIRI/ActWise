"""Reciprocal rank fusion: merge ranked lists without tuning weights."""

from __future__ import annotations

from collections import defaultdict

from actwise.retrieval.passages import Hit, to_hit


def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Fused (key, score) pairs, best first: score = sum over lists of 1 / (k + rank).

    Ranks start at 1, so a key that several retrievers find adds up their votes.
    Ties keep the order in which keys first appear.
    """
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, key in enumerate(ranking, start=1):
            scores[key] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: -item[1])


def fuse_hits(rankings: list[list[Hit]], k: int = 60) -> list[Hit]:
    """The hits of several rankings (one per query), fused with `rrf` on their storage keys."""
    by_key = {hit.key: hit for ranking in rankings for hit in ranking}
    fused = rrf([[hit.key for hit in ranking] for ranking in rankings], k)
    return [to_hit(by_key[key], score) for key, score in fused]
