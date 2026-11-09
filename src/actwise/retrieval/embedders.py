"""Embedders behind one interface: encode(texts, kind) -> L2-normalised float32 matrix.

`kind` is "query" or "passage" because some models (e5, BGE v1.5) want a
prefix on one side; BGE-M3 and MiniLM need none. `config` names the vector space,
so a cache built with another model or setting is never reused by mistake.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Protocol

import numpy as np

# Hub name and pinned commit. 9a0624b is the bot-made safetensors variant of main (5617a9f):
# same weights, but it loads without pickle and without transformers' silent PR redirect.
BGE_M3 = ("BAAI/bge-m3", "9a0624b896d81da7492a910ffa53731274b6cf3d")
# The step 9 base model: multilingual, small, and not trained for retrieval (decision 011).
MINILM = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
)
MINILM_MAX_LEN = 256  # its default of 128 tokens would cut most passages
# Our fine-tuned MiniLM in int8, as evals/publish_model.py published it; the image uses it too.
MINILM_HUB = (
    "Youssef-ADOUIRI/actwise-minilm-l12-ft-int8",
    "8f2058b361a58d21ab169ba90848410f28d91609",
)


def hub_snapshot(repo: str, revision: str) -> Path:
    """The folder of a pinned Hub commit, downloaded once into the Hugging Face cache."""
    from huggingface_hub import snapshot_download  # cloud extra: imported only when used

    return Path(snapshot_download(repo, revision=revision))


def file_hash(path: Path) -> str:
    """The first 16 hex digits of a file's SHA-256: it names weights that have no Hub commit."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()[:16]


class Embedder(Protocol):
    config: dict[str, Any]

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        """One L2-normalised float32 row per text; `kind` is "query" or "passage"."""
        ...

    def unload(self) -> None:
        """Free the model's memory; the next `encode()` loads it again."""
        ...


def l2_normalize(x: np.ndarray) -> np.ndarray:
    """Scale each row to unit length, so a dot product is a cosine similarity."""
    return x / np.clip(np.linalg.norm(x, axis=1, keepdims=True), 1e-12, None)


def mean_pool(last_hidden: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
    """Average each text's token vectors, leaving out the padding."""
    mask = attention_mask[..., None].astype(last_hidden.dtype)
    return (last_hidden * mask).sum(axis=1) / np.clip(mask.sum(axis=1), 1e-9, None)


class SentenceTransformerEmbedder:
    """Local profile: BGE-M3, multilingual-e5 or a fine-tuned model (needs torch)."""

    def __init__(
        self,
        name: str,
        revision: str | None = None,
        max_len: int = 512,
        batch_size: int = 8,
        query_prefix: str = "",
        passage_prefix: str = "",
    ):
        """Record the settings in `config`; the model loads on the first `encode()`."""
        # Pin `revision` (a Hub commit hash) so reported numbers stay reproducible.
        self.name, self.revision = name, revision
        self.max_len, self.batch_size = max_len, batch_size
        self.prefix = {"query": query_prefix, "passage": passage_prefix}
        weights = Path(name) / "model.safetensors"  # a local model has no commit: hash it
        self.config = {
            "model": name,
            "revision": revision or (file_hash(weights) if weights.is_file() else None),
            "max_len": max_len,
            "prefix": self.prefix,
        }
        self._model: Any = None

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        """Add the prefix for `kind`, embed in batches and L2-normalise the result."""
        if self._model is None:  # a run served entirely from the cache never loads it
            from sentence_transformers import SentenceTransformer  # heavy: imported only when used

            self._model = SentenceTransformer(self.name, revision=self.revision)
            self._model.max_seq_length = self.max_len
        vectors = self._model.encode(
            [self.prefix[kind] + text for text in texts],
            batch_size=self.batch_size,
            show_progress_bar=False,
        )
        return l2_normalize(np.asarray(vectors, dtype=np.float32))

    def unload(self) -> None:
        """Free the model's memory; the next `encode()` loads it again."""
        self._model = None


class OnnxEmbedder:
    """Cloud profile: an ONNX export run with `onnxruntime` and `tokenizers` only, no torch."""

    def __init__(
        self,
        model_dir: str | Path,
        max_len: int = MINILM_MAX_LEN,
        batch_size: int = 32,
        query_prefix: str = "",
        passage_prefix: str = "",
    ):
        """Record the settings in `config`; the session loads on the first `encode()`."""
        self.dir = Path(model_dir)
        self.max_len, self.batch_size = max_len, batch_size
        self.prefix = {"query": query_prefix, "passage": passage_prefix}
        self.config = {
            "model": "onnx",
            "weights": file_hash(self.dir / "model.onnx"),  # fp32 and int8 never share a cache
            "max_len": max_len,
            "prefix": self.prefix,
        }
        self._session: Any = None
        self._tokenizer: Any = None
        self._inputs: set[str] = set()

    def _load(self) -> None:
        """Open the ONNX session and the tokenizer, truncating and padding like the model."""
        import onnxruntime as ort  # cloud extra: imported only when used
        from tokenizers import Tokenizer

        tokenizer = Tokenizer.from_file(str(self.dir / "tokenizer.json"))
        tokenizer.enable_truncation(max_length=self.max_len)
        pad = tokenizer.token_to_id("<pad>")  # XLM-R pads with id 1, not the default 0
        tokenizer.enable_padding(pad_id=0 if pad is None else pad, pad_token="<pad>")
        self._session = ort.InferenceSession(
            str(self.dir / "model.onnx"), providers=["CPUExecutionProvider"]
        )
        self._tokenizer = tokenizer
        self._inputs = {i.name for i in self._session.get_inputs()}

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        """Add the prefix for `kind`, run in batches, mean-pool and L2-normalise."""
        if self._session is None:
            self._load()
        rows = []
        for start in range(0, len(texts), self.batch_size):
            batch = [self.prefix[kind] + text for text in texts[start : start + self.batch_size]]
            encodings = self._tokenizer.encode_batch(batch)
            ids = np.array([e.ids for e in encodings], dtype=np.int64)
            mask = np.array([e.attention_mask for e in encodings], dtype=np.int64)
            feeds = {"input_ids": ids, "attention_mask": mask}
            if "token_type_ids" in self._inputs:
                feeds["token_type_ids"] = np.zeros_like(ids)
            rows.append(mean_pool(self._session.run(None, feeds)[0], mask))
        return l2_normalize(np.concatenate(rows).astype(np.float32))

    def unload(self) -> None:
        """Free the session's memory; the next `encode()` loads it again."""
        self._session = None
