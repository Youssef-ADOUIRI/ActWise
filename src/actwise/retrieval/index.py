"""Upload the structure-aware chunks to Qdrant: `docker compose up -d qdrant`, then `make index`.

Vectors come from the embedding cache, so a warm cache never loads the model.
Point ids derive from the storage key, so running it again only overwrites.
"""

from __future__ import annotations

import os

from actwise.retrieval.dense import CACHE_DIR, build_store
from actwise.retrieval.embedders import BGE_M3, SentenceTransformerEmbedder
from actwise.retrieval.passages import chunk_passages
from actwise.retrieval.stores import QdrantStore

COLLECTION = "actwise_bge_m3"  # one collection per embedder


def main() -> None:
    """Embed whatever is missing, then upsert every chunk into `COLLECTION`."""
    from qdrant_client import QdrantClient

    passages = chunk_passages()
    store = build_store(passages, SentenceTransformerEmbedder(*BGE_M3), CACHE_DIR)
    client = QdrantClient(
        url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        api_key=os.environ.get("QDRANT_API_KEY") or None,
    )
    QdrantStore(client, COLLECTION).index(store.payloads, store.vectors)
    print(f"indexed {len(passages)} passages into {COLLECTION}")


if __name__ == "__main__":
    main()
