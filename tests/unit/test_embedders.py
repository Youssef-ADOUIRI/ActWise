from types import SimpleNamespace

import numpy as np

from actwise.retrieval.embedders import (
    OnnxEmbedder,
    SentenceTransformerEmbedder,
    l2_normalize,
    mean_pool,
)


def test_pooling_ignores_padding():
    """Masked tokens don't count; the mean matches a hand calculation, then unit norm."""
    hidden = np.array([[[1.0, 2.0], [3.0, 4.0], [100.0, 100.0]]], dtype=np.float32)
    mask = np.array([[1, 1, 0]])

    pooled = mean_pool(hidden, mask)

    assert np.allclose(pooled, [[2.0, 3.0]])
    assert np.allclose(np.linalg.norm(l2_normalize(pooled), axis=1), 1.0)


def test_a_local_model_is_fingerprinted_by_its_weights(tmp_path):
    """Retraining changes the config, so cached vectors of the old weights are never reused."""
    (tmp_path / "model.safetensors").write_bytes(b"first weights")
    before = SentenceTransformerEmbedder(str(tmp_path)).config["revision"]
    (tmp_path / "model.safetensors").write_bytes(b"second weights")

    assert before != SentenceTransformerEmbedder(str(tmp_path)).config["revision"]
    assert SentenceTransformerEmbedder("org/name", "abc123").config["revision"] == "abc123"


class FakeTokenizer:
    """Pads each batch to its longest text: one token per word, mask 0 on the padding."""

    def encode_batch(self, texts):
        """Token ids 1..n per word, then zeros."""
        width = max(len(t.split()) for t in texts)
        return [
            SimpleNamespace(
                ids=[i + 1 for i in range(len(t.split()))] + [0] * (width - len(t.split())),
                attention_mask=[1] * len(t.split()) + [0] * (width - len(t.split())),
            )
            for t in texts
        ]


class FakeSession:
    """Each token's hidden state is (token id, 1); records the batches it ran."""

    def __init__(self):
        """No batch run yet."""
        self.batches = []

    def get_inputs(self):
        """The input names of a BERT-style export."""
        return [SimpleNamespace(name=n) for n in ("input_ids", "attention_mask", "token_type_ids")]

    def run(self, outputs, feeds):
        """Hidden states shaped (batch, tokens, 2)."""
        self.batches.append(feeds)
        ids = feeds["input_ids"].astype(np.float32)
        return [np.stack([ids, np.ones_like(ids)], axis=-1)]


def test_onnx_embedder_pools_each_batch(tmp_path):
    """Texts go through in batches, padding never counts, and each row has unit norm."""
    (tmp_path / "model.onnx").write_bytes(b"onnx weights")
    embedder = OnnxEmbedder(tmp_path, batch_size=2, query_prefix="q ")
    session = FakeSession()
    embedder._session, embedder._tokenizer = session, FakeTokenizer()
    embedder._inputs = {i.name for i in session.get_inputs()}

    vectors = embedder.encode(["a", "a b c", "a b"], kind="query")

    assert [len(b["input_ids"]) for b in session.batches] == [2, 1]
    assert np.all(session.batches[0]["token_type_ids"] == 0)
    # "q a" has tokens 1, 2: mean (1.5, 1); "q a b c": mean (2.5, 1); "q a b": mean (2, 1)
    expected = l2_normalize(np.array([[1.5, 1.0], [2.5, 1.0], [2.0, 1.0]], dtype=np.float32))
    assert np.allclose(vectors, expected)
    assert vectors.dtype == np.float32


def test_onnx_config_names_the_weights(tmp_path):
    """Two exports (fp32 and int8) never share cached vectors; nothing loads until used."""
    (tmp_path / "model.onnx").write_bytes(b"int8")
    embedder = OnnxEmbedder(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    (other / "model.onnx").write_bytes(b"fp32")

    assert embedder.config["weights"] != OnnxEmbedder(other).config["weights"]
    assert embedder._session is None
