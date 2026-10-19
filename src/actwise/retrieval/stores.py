"""Vector stores. NumPy brute force for now; Qdrant joins in step 4 behind the same search()."""

from __future__ import annotations

import numpy as np


class NumpyStore:
    """Exact cosine search over L2-normalised vectors: a few thousand passages take ~1 ms."""

    def __init__(self, keys: list[str], vectors: np.ndarray):
        if len(keys) != len(vectors):
            raise ValueError(f"{len(keys)} keys for {len(vectors)} vectors")
        self.keys, self.vectors = keys, vectors.astype(np.float32)

    def search(self, vector: np.ndarray, k: int = 30) -> list[tuple[str, float]]:
        scores = self.vectors @ vector.astype(np.float32)
        top = np.argsort(-scores, kind="stable")[:k]  # stable: ties keep corpus order
        return [(self.keys[i], float(scores[i])) for i in top]
