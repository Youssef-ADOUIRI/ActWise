from pathlib import Path

import pytest

from actwise.retrieval.embedders import OnnxEmbedder
from actwise.retrieval.passages import chunk_passages
from actwise.retrieval.systems import MINILM_FT, MINILM_FT_INT8, minilm


@pytest.mark.slow
def test_onnx_parity():
    """The int8 ONNX model embeds 20 chunks, EN and FR, within cosine 0.98 of PyTorch."""
    if not (Path(MINILM_FT).is_dir() and Path(MINILM_FT_INT8).is_dir()):
        pytest.skip("needs models/ (evals/train_embedder.py, then evals/export_onnx.py)")
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("onnxruntime")
    texts = [p.text for p in chunk_passages()[::190]][:20]

    reference = minilm(MINILM_FT).encode(texts)
    vectors = OnnxEmbedder(MINILM_FT_INT8).encode(texts)

    assert (reference * vectors).sum(axis=1).min() >= 0.98
