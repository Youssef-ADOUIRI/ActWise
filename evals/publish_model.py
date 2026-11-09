"""Publish the int8 embedder and its card on the Hugging Face Hub (step 9, decision 011).

    uv run --extra local --extra train python evals/publish_model.py      (make publish-model)

HF_TOKEN, from the environment or `.env`, needs write access. The files of
models/minilm-ft-int8/ and docs/embedder_card.md (as README.md) go to the public repo
<user>/actwise-minilm-l12-ft-int8 in one commit. Pin the printed commit in MINILM_HUB.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from actwise.retrieval.systems import MINILM_FT_INT8

REPO_NAME = "actwise-minilm-l12-ft-int8"
CARD = Path("docs/embedder_card.md")


def main() -> None:
    """Create the repo if needed, then upload the model files and the card in one commit."""
    from huggingface_hub import CommitOperationAdd, HfApi

    load_dotenv()  # .env fills in what the environment doesn't set
    api = HfApi(token=os.environ["HF_TOKEN"])
    repo_id = f"{api.whoami()['name']}/{REPO_NAME}"
    api.create_repo(repo_id, exist_ok=True)
    files = sorted(p for p in Path(MINILM_FT_INT8).iterdir() if p.is_file())
    operations = [CommitOperationAdd(p.name, p) for p in files]
    operations.append(CommitOperationAdd("README.md", CARD))
    commit = api.create_commit(repo_id, operations, commit_message="ActWise int8 embedder")
    print(f"published {', '.join(p.name for p in files)} and README.md")
    print(f"https://huggingface.co/{repo_id} at commit {commit.oid}")


if __name__ == "__main__":
    main()
