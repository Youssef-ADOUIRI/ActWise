"""Upload the structure-aware chunks to Qdrant, one collection per embedder.

    make index         BGE-M3 into actwise_bge_m3 (local Qdrant: docker compose up -d qdrant)
    make index-cloud   the int8 MiniLM into actwise_ft_int8, plus data/processed/index.npz

QDRANT_URL and QDRANT_API_KEY come from the environment or `.env`. Vectors come from
the embedding cache, so a warm cache never loads the model. Point ids derive from the
storage key, so running it again only overwrites.
"""

from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from pathlib import Path

from dotenv import load_dotenv

from actwise.retrieval.dense import CACHE_DIR, build_store
from actwise.retrieval.embedders import BGE_M3, Embedder, SentenceTransformerEmbedder
from actwise.retrieval.passages import chunk_passages
from actwise.retrieval.stores import QdrantStore
from actwise.retrieval.systems import minilm_int8

NPZ_FILE = Path("data/processed/index.npz")  # the step 13 image searches it when Qdrant fails
INDEXES: dict[str, tuple[str, Callable[[], Embedder]]] = {
    "bge-m3": ("actwise_bge_m3", lambda: SentenceTransformerEmbedder(*BGE_M3)),
    "ft-int8": ("actwise_ft_int8", minilm_int8),
}


def main() -> None:
    """Embed whatever is missing, then upsert every chunk into the embedder's collection."""
    from qdrant_client import QdrantClient

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--embedder", choices=INDEXES, default="bge-m3")
    parser.add_argument("--npz", action="store_true", help=f"also write {NPZ_FILE}")
    args = parser.parse_args()
    load_dotenv()  # .env fills in what the environment doesn't set
    collection, embedder = INDEXES[args.embedder]
    passages = chunk_passages()
    store = build_store(passages, embedder(), CACHE_DIR)
    if args.npz:
        store.save(NPZ_FILE)
        print(f"wrote {NPZ_FILE}")
    client = QdrantClient(
        url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        api_key=os.environ.get("QDRANT_API_KEY") or None,
    )
    QdrantStore(client, collection).index(store.payloads, store.vectors)
    print(f"indexed {len(passages)} passages into {collection}")


if __name__ == "__main__":
    main()
