"""Reciprocal rank fusion: merge ranked lists without tuning weights."""

from __future__ import annotations

from collections import defaultdict


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
