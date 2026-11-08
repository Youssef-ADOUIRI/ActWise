"""Fine-tune the multilingual MiniLM on the training pairs (step 9, decision 011).

    PYTHONPATH=src python evals/train_embedder.py

Runs on a GPU (Colab or Kaggle: notebooks/train_embedder.ipynb) or, slowly, on a CPU.
It needs `sentence-transformers[train]` and nothing else from the project, so the
notebook installs no other package.

MultipleNegativesRankingLoss treats the other passages of a batch as negatives. Each
batch holds one language, so an English question never meets the French twin of its
passage as a negative, which would teach the model to pull the two languages apart.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path

from actwise.retrieval.embedders import MINILM, MINILM_MAX_LEN

SEED = 42  # the project seed (evaluation/splits.py)
EPOCHS, BATCH_SIZE, LEARNING_RATE, WARMUP_RATIO = 3, 32, 2e-5, 0.1


def git_commit() -> str:
    """The commit being trained, or "unknown" outside a git checkout."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> None:
    """Train, save the model to `--out`, and record how it was made in training.json."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=Path, default=Path("data/train/pairs.jsonl"))
    parser.add_argument("--out", type=Path, default=Path("models/minilm-ft"))
    args = parser.parse_args()

    import datasets
    import sentence_transformers
    import torch
    import transformers
    from sentence_transformers import (
        SentenceTransformer,
        SentenceTransformerTrainer,
        SentenceTransformerTrainingArguments,
    )
    from sentence_transformers.losses import MultipleNegativesRankingLoss
    from sentence_transformers.training_args import BatchSamplers

    raw = args.pairs.read_bytes()
    pairs = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    train = datasets.DatasetDict(
        {
            lang: datasets.Dataset.from_dict(
                {
                    "anchor": [p["anchor"] for p in pairs if p["lang"] == lang],
                    "positive": [p["positive"] for p in pairs if p["lang"] == lang],
                }
            )
            for lang in ("en", "fr")
        }
    )
    model = SentenceTransformer(MINILM[0], revision=MINILM[1])
    model.max_seq_length = MINILM_MAX_LEN
    training_args = SentenceTransformerTrainingArguments(
        output_dir=str(args.out / "checkpoints"),
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        warmup_steps=WARMUP_RATIO,  # a float below 1 is a ratio in Transformers 5
        fp16=torch.cuda.is_available(),
        batch_sampler=BatchSamplers.NO_DUPLICATES,  # within each language's dataset
        seed=SEED,
        save_strategy="no",
        logging_steps=10,
        report_to="none",
    )
    trainer = SentenceTransformerTrainer(
        model=model,
        args=training_args,
        train_dataset=train,  # a dict of datasets: each batch comes from one of them
        loss=MultipleNegativesRankingLoss(model),
    )
    start = time.perf_counter()
    result = trainer.train()
    model.save_pretrained(str(args.out))
    shutil.rmtree(args.out / "checkpoints", ignore_errors=True)  # save_strategy="no": empty

    record = {
        "base": {"model": MINILM[0], "revision": MINILM[1]},
        "pairs": {
            "file": args.pairs.as_posix(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "by_lang": {lang: len(ds) for lang, ds in train.items()},
        },
        "recipe": {
            "loss": "MultipleNegativesRankingLoss",
            "epochs": EPOCHS,
            "batch_size": BATCH_SIZE,
            "learning_rate": LEARNING_RATE,
            "warmup_ratio": WARMUP_RATIO,
            "max_seq_length": MINILM_MAX_LEN,
            "seed": SEED,
            "fp16": training_args.fp16,
        },
        "result": {"train_loss": result.training_loss, "steps": result.global_step},
        "seconds": round(time.perf_counter() - start),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "git_commit": git_commit(),
        "versions": {
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "sentence_transformers": sentence_transformers.__version__,
            "datasets": datasets.__version__,
        },
    }
    (args.out / "training.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record["result"]), f"saved to {args.out}")


if __name__ == "__main__":
    main()
