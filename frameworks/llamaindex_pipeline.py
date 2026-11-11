"""System H rebuilt with LlamaIndex: the fine-tuned MiniLM over the same passages (step 10).

    uv run --extra local --extra frameworks python evals/run_eval.py --system llamaindex-ft

LlamaIndex embeds the corpus with its stock `HuggingFaceEmbedding`, keeps the vectors in
its `SimpleVectorStore` and persists the index under .cache/llamaindex, so only the first
run embeds. Each node keeps its chunk id and language as metadata, left out of the
embedded text: by default LlamaIndex prepends the metadata to what it embeds.
"""

from __future__ import annotations

import json
from importlib.metadata import version
from pathlib import Path
from typing import Any

from actwise.retrieval.dense import text_hash
from actwise.retrieval.embedders import MINILM_MAX_LEN
from actwise.retrieval.passages import Hit, Passage, chunk_passages
from actwise.retrieval.systems import MINILM_FT, minilm

CACHE_DIR = Path(".cache/llamaindex")
METADATA = ["id", "lang"]  # what a hit needs back; never embedded


class LlamaIndexRetriever:
    """A LlamaIndex vector index behind our `Retriever` protocol: chunk ids, best first."""

    def __init__(self, index: Any, config: dict[str, Any]):
        """Search `index`; `config` names the framework, the embedder and the corpus."""
        self.index, self.config = index, config

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        """The `top_k` nodes closest to the query, as our hits."""
        found = self.index.as_retriever(similarity_top_k=top_k).retrieve(query)
        return [
            Hit(n.node.metadata["id"], n.node.metadata["lang"], n.node.get_content(), n.score or 0)
            for n in found
        ]


def build(
    passages: list[Passage] | None = None, embed_model: Any = None, cache_dir: Path = CACHE_DIR
) -> LlamaIndexRetriever:
    """Load the persisted index for this embedder and corpus, or embed and persist it first."""
    from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
    from llama_index.core.schema import TextNode

    passages = chunk_passages() if passages is None else passages
    if embed_model is None:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        embedder = minilm(MINILM_FT).config  # names the weights by their hash, like H
        embed_model = HuggingFaceEmbedding(
            MINILM_FT, max_length=MINILM_MAX_LEN, embed_batch_size=32
        )
    else:
        embedder = {"model": embed_model.model_name}
    corpus = text_hash("\n".join(f"{p.key}\t{p.text}" for p in passages))[:16]
    config = {
        "framework": f"llama-index-core {version('llama-index-core')}",
        "embedder": embedder,
        "passages": corpus,
    }
    folder = cache_dir / text_hash(json.dumps(config, sort_keys=True))[:16]
    if folder.is_dir():
        storage = StorageContext.from_defaults(persist_dir=str(folder))
        index = load_index_from_storage(storage, embed_model=embed_model)
    else:
        nodes = [
            TextNode(
                id_=p.key,
                text=p.text,
                metadata={"id": p.id, "lang": p.lang},
                excluded_embed_metadata_keys=METADATA,
                excluded_llm_metadata_keys=METADATA,
            )
            for p in passages
        ]
        index = VectorStoreIndex(nodes, embed_model=embed_model)
        partial = folder.with_name(folder.name + ".partial")  # an interrupted save is never loaded
        index.storage_context.persist(persist_dir=str(partial))
        partial.rename(folder)
    return LlamaIndexRetriever(index, config)
