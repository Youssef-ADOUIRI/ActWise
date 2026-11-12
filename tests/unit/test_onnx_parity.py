from pathlib import Path

import pytest

from actwise.provenance import file_hash
from actwise.retrieval.embedders import MINILM_HUB, OnnxEmbedder, hub_snapshot
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


@pytest.mark.slow
def test_the_published_model_is_the_export():
    """MINILM_HUB pins the same int8 weights that evals/export_onnx.py wrote."""
    if not Path(MINILM_FT_INT8).is_dir():
        pytest.skip("needs models/minilm-ft-int8 (evals/export_onnx.py)")
    pytest.importorskip("huggingface_hub")

    published = hub_snapshot(*MINILM_HUB) / "model.onnx"

    assert file_hash(published) == file_hash(Path(MINILM_FT_INT8) / "model.onnx")
