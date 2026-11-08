"""Export a MiniLM to ONNX, then quantize it to int8 (step 9, decision 011).

    uv run --extra local --extra train python evals/export_onnx.py [--model models/minilm-ft]

Writes `<model>-onnx` (fp32) and `<model>-int8`, each holding model.onnx and the
tokenizer, and prints their sizes. The graph returns the last hidden state; mean
pooling and normalisation happen in `OnnxEmbedder`, as they do in the PyTorch model.
`--model base` exports the pinned base model instead, to models/minilm-base-*.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from actwise.retrieval.embedders import MINILM
from actwise.retrieval.systems import MINILM_FT

TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "special_tokens_map.json")


def size_mb(path: Path) -> float:
    """A file's size in MB (10^6 bytes)."""
    return round(path.stat().st_size / 1e6, 1)


def main() -> None:
    """Export fp32, quantize to int8, and copy the tokenizer next to each model."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MINILM_FT, help="a local folder, or 'base'")
    args = parser.parse_args()

    import torch
    from onnxruntime.quantization import QuantType, quantize_dynamic
    from transformers import AutoModel, AutoTokenizer

    name, revision = MINILM if args.model == "base" else (args.model, None)
    stem = "models/minilm-base" if args.model == "base" else args.model.rstrip("/")
    fp32, int8 = Path(f"{stem}-onnx"), Path(f"{stem}-int8")
    tokenizer = AutoTokenizer.from_pretrained(name, revision=revision)
    model = AutoModel.from_pretrained(name, revision=revision, attn_implementation="eager")

    class LastHidden(torch.nn.Module):
        """The transformer's token vectors only: what mean pooling reads."""

        def __init__(self) -> None:
            """Wrap the loaded model."""
            super().__init__()
            self.model = model

        def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
            """Token vectors of shape (batch, tokens, 384)."""
            return self.model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state

    sample = tokenizer(
        ["a short text", "a longer text with more words"], return_tensors="pt", padding=True
    )
    fp32.mkdir(parents=True, exist_ok=True)
    axes = {0: "batch", 1: "tokens"}
    torch.onnx.export(
        LastHidden().eval(),
        (sample["input_ids"], sample["attention_mask"]),
        str(fp32 / "model.onnx"),
        input_names=["input_ids", "attention_mask"],
        output_names=["last_hidden_state"],
        dynamic_axes={"input_ids": axes, "attention_mask": axes, "last_hidden_state": axes},
        opset_version=18,
        external_data=False,  # one file, so OnnxEmbedder's hash of model.onnx covers the weights
    )
    tokenizer.save_pretrained(str(fp32))
    int8.mkdir(parents=True, exist_ok=True)
    # One scale per weight column: on the base model, the worst cosine to PyTorch over 20
    # chunks rises from 0.973 (one scale per tensor) to 0.989, at the same 119 MB.
    quantize_dynamic(
        fp32 / "model.onnx",
        int8 / "model.onnx",
        weight_type=QuantType.QInt8,
        per_channel=True,
        reduce_range=True,
    )
    for file in TOKENIZER_FILES:
        if (fp32 / file).exists():
            shutil.copy(fp32 / file, int8 / file)
    for folder in (fp32, int8):
        print(f"{folder}: model.onnx {size_mb(folder / 'model.onnx')} MB")


if __name__ == "__main__":
    main()
