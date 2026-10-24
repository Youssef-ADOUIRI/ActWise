"""Versioned prompts shipped in the package (actwise/prompts/<name>.md), and their JSON replies."""

from __future__ import annotations

import json
import re
from importlib.resources import files
from typing import Any

PROMPTS = files("actwise") / "prompts"  # inside the package, so it works from any directory


def load_prompt(name: str) -> str:
    """The text of `prompts/<name>.md`, such as answer.v1 or judge.v1."""
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8").strip()


def answer_prompts() -> list[str]:
    """The answer prompt versions, such as ["answer.v1", "answer.v2"]."""
    names = (p.name.removesuffix(".md") for p in PROMPTS.iterdir() if p.name.endswith(".md"))
    return sorted(name for name in names if name.startswith("answer.v"))


def json_object(reply: str) -> dict[str, Any] | None:
    """The JSON object in a model's reply, even inside prose or a code fence; else None."""
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    try:
        data = json.loads(match.group(0)) if match else None
    except ValueError:
        return None
    return data if isinstance(data, dict) else None
