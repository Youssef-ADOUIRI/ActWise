"""Training pairs for the embedder (step 9): a question and the passage that answers it.

Questions are written from train paragraphs only, so nothing scored in dev or test
reaches training (decision 002). One call drafts a question in each language. Each
question pairs with the passage in its own language. The windows of a long paragraph
fall at different words in English and French, so a window gives an English pair only.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from actwise.evaluation.splits import SEED
from actwise.evaluation.synthetic import normalise, pick_chunks, screen_question
from actwise.generation.prompts import json_object, load_prompt
from actwise.ids import storage_key
from actwise.ingest.chunk import Chunk
from actwise.llm.base import LLM

PAIRS_PROMPT = "pairs.v1"
PAIRS_FILE = Path("data/train/pairs.jsonl")
LANGS = ("en", "fr")


def draft_pair(llm: LLM, chunk: Chunk) -> dict[str, str]:
    """A question per language that `chunk` answers; a field the reply lacks comes back empty."""
    messages = [
        {"role": "system", "content": load_prompt(PAIRS_PROMPT)},
        {"role": "user", "content": f"Passage:\n{chunk.embed_text}"},
    ]
    data = json_object(llm.chat(messages, temperature=0).text) or {}
    return {lang: str(data.get(lang, "")).strip() for lang in LANGS}


def make_pairs(
    llm: LLM, chunks: list[Chunk], article_split: dict[str, str], n: int
) -> list[dict[str, str]]:
    """Pairs from `n` train paragraphs (English chunks), each screened with its reasons."""
    by_key = {c.key: c for c in chunks}
    seen: set[str] = set()
    pairs = []
    for chunk in pick_chunks(chunks, article_split, "train", n, fr_share=0):
        for lang, question in draft_pair(llm, chunk).items():
            passage = by_key.get(storage_key(chunk.id, lang))
            if passage is None or (lang != chunk.lang and "#" in chunk.id):
                continue  # no passage with the same text in that language
            reasons = screen_question(question, seen)
            seen.add(normalise(question))
            pairs.append(
                {
                    "source": passage.key,
                    "lang": lang,
                    "anchor": question,
                    "positive": passage.embed_text,
                    "screen": "; ".join(reasons),
                }
            )
    return pairs


def review_sample(pairs: list[dict[str, str]], n: int) -> list[dict[str, str]]:
    """`n` pairs drawn with the project seed, for a person to read."""
    return random.Random(SEED).sample(pairs, min(n, len(pairs)))


def load_pairs(path: Path = PAIRS_FILE) -> list[dict[str, str]]:
    """The committed training pairs: source, lang, anchor and positive."""
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]
