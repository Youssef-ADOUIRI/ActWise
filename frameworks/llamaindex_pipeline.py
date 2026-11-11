"""System H rebuilt with LlamaIndex: the fine-tuned MiniLM over the same passages (step 10).

    uv run --extra local --extra frameworks python evals/run_eval.py --system llamaindex-ft

LlamaIndex embeds the corpus with its stock `HuggingFaceEmbedding`, keeps the vectors in
its `SimpleVectorStore` and persists the index under .cache/llamaindex, so only the first
run embeds. A node holds only the passage text, under the passage's storage key: by
default LlamaIndex prepends a node's metadata to what it embeds.
"""

from __future__ import annotations

import json
from importlib.metadata import version
from pathlib import Path
from typing import Any

from actwise.retrieval.dense import text_hash
from actwise.retrieval.passages import Hit, Passage, chunk_passages, to_hit
from actwise.retrieval.systems import MINILM_FT, minilm

CACHE_DIR = Path(".cache/llamaindex")


class LlamaIndexRetriever:
    """A LlamaIndex vector index behind our `Retriever` protocol: chunk ids, best first."""

    def __init__(self, index: Any, passages: list[Passage], config: dict[str, Any]):
        """Search `index`; `config` names the framework, the embedder and the corpus."""
        self.index, self.config = index, config
        self.passages = {p.key: p for p in passages}  # node id -> passage, as in DenseRetriever

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        """The `top_k` nodes closest to the query, as our hits."""
        found = self.index.as_retriever(similarity_top_k=top_k).retrieve(query)
        return [to_hit(self.passages[n.node.node_id], n.score or 0) for n in found]


def build(
    passages: list[Passage] | None = None, embed_model: Any = None, cache_dir: Path = CACHE_DIR
) -> LlamaIndexRetriever:
    """Load the persisted index for this embedder and corpus, or embed and persist it first."""
    from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
    from llama_index.core.schema import TextNode

    passages = chunk_passages() if passages is None else passages
    if embed_model is None:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        ours = minilm(MINILM_FT)  # H's model and settings
        embedder = ours.config  # names the weights by their hash, like H
        embed_model = HuggingFaceEmbedding(
            ours.name, max_length=ours.max_len, embed_batch_size=ours.batch_size
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
        nodes = [TextNode(id_=p.key, text=p.text) for p in passages]
        index = VectorStoreIndex(nodes, embed_model=embed_model)
        partial = folder.with_name(folder.name + ".partial")  # an interrupted save is never loaded
        index.storage_context.persist(persist_dir=str(partial))
        partial.rename(folder)
    return LlamaIndexRetriever(index, passages, config)
