"""Small BM25 (Okapi) index: no dependency, easy to explain.

Terms are lower-case words with accents folded, so "Données" and "donnees" match,
and elisions split ("l’accès" -> "l", "acces"). EN and FR passages share one index,
each keyed by its storage key like the vector stores (R1).
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, defaultdict

from actwise.retrieval.passages import Hit, Passage, to_hit

TOKEN = re.compile(r"\w+")


def tokenize(text: str) -> list[str]:
    """Lower-case words, accents folded: "L’accès aux données" -> l, acces, aux, donnees."""
    folded = unicodedata.normalize("NFKD", text.lower())
    return TOKEN.findall("".join(ch for ch in folded if not unicodedata.combining(ch)))


class BM25:
    """Okapi BM25 over passages; a search only visits passages that share a query term."""

    def __init__(self, passages: list[Passage], k1: float = 1.5, b: float = 0.75):
        """Count the terms of every passage once."""
        self.passages, self.k1, self.b = passages, k1, b
        self.lengths: list[int] = []
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)  # term -> (row, tf)
        for row, passage in enumerate(passages):
            counts = Counter(tokenize(passage.text))
            self.lengths.append(sum(counts.values()))
            for term, tf in counts.items():
                self.postings[term].append((row, tf))
        n = len(passages)
        self.avg_len = sum(self.lengths) / max(n, 1)
        self.idf = {
            term: math.log(1 + (n - len(rows) + 0.5) / (len(rows) + 0.5))
            for term, rows in self.postings.items()
        }
        self.config = {"bm25": {"k1": k1, "b": b}, "passages": n}

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        """The `top_k` best passages for the query terms, best first; none if no term is known."""
        scores: dict[int, float] = defaultdict(float)
        for term in tokenize(query):
            for row, tf in self.postings.get(term, []):
                norm = tf + self.k1 * (1 - self.b + self.b * self.lengths[row] / self.avg_len)
                scores[row] += self.idf[term] * tf * (self.k1 + 1) / norm
        best = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_k]
        return [to_hit(self.passages[row], score) for row, score in best]
