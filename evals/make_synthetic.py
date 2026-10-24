"""Draft golden-set candidates for review: data/eval/candidates.csv and candidates.md.

    uv run python evals/make_synthetic.py

In scope: 60 dev and 60 test questions, each written by the LLM from one article or
annex paragraph (about 30 % French), 20 % more than step 6b needs. Out of scope: 12 dev
and 12 test questions on other EU law. Rules mark the obvious failures "drop"; a reviewer
fills `decision` (keep, drop or fix) and may edit `question` and `reference` in the CSV.
"""

from __future__ import annotations

import csv
import os
import random
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from actwise.evaluation.answers import quote
from actwise.evaluation.golden import load_golden
from actwise.evaluation.splits import load_splits, split_of
from actwise.evaluation.synthetic import (
    FR_SHARE,
    OUT_OF_SCOPE_TOPICS,
    draft_in_scope,
    draft_out_of_scope,
    normalise,
    pick_chunks,
    screen,
)
from actwise.ids import human_label
from actwise.ingest.build_chunks import load_chunks
from actwise.llm.factory import OFFLINE, build_llm

IN_SCOPE_PER_SPLIT = 60
CSV_FILE, MD_FILE = Path("data/eval/candidates.csv"), Path("data/eval/candidates.md")
COLUMNS = ["cid", "split", "lang", "type", "gold", "source", "question", "reference"]
COLUMNS += ["screen", "decision", "note"]


def review_markdown(candidates: list[dict[str, Any]], passages: dict[tuple[str, str], str]) -> str:
    """Each candidate with the passage it came from, to read next to the CSV."""
    lines = ["# Golden-set candidates", "", "Decide in `candidates.csv`; this file is for reading."]
    for c in candidates:
        gold = ", ".join(human_label(g, c["lang"]) for g in c["gold"]) or "out of scope"
        lines += ["", f"## {c['cid']} · {c['split']} · {c['lang']} · {c['type']} · {gold}", ""]
        lines += [f"**Question:** {c['question']}", "", f"**Reference:** {c['reference']}"]
        if passage := passages.get((c["source"], c["lang"])):
            lines += ["", "**Passage:**", ""] + quote(passage)
        else:
            lines += ["", f"**Topic:** {c['source']}"]
        lines += ["", f"**Screen:** {c['screen'] or 'ok'} · **Decision:** {c['decision'] or '?'}"]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Draft, screen and write every candidate."""
    load_dotenv()
    llm = build_llm(os.environ, OFFLINE)
    chunks = load_chunks()
    article_split = split_of(load_splits())
    drafts = []
    for split in ("dev", "test"):
        for chunk in pick_chunks(chunks, article_split, split, IN_SCOPE_PER_SPLIT):
            drafts.append(draft_in_scope(llm, chunk, split))
    rng = random.Random(42)
    topics = rng.sample(OUT_OF_SCOPE_TOPICS, len(OUT_OF_SCOPE_TOPICS))
    for i, topic in enumerate(topics):
        lang = "fr" if rng.random() < FR_SHARE else "en"
        drafts.append(draft_out_of_scope(llm, topic, lang, ("dev", "test")[i % 2]))

    seen = {normalise(q.question) for q in load_golden()}
    candidates = []
    for n, draft in enumerate(drafts, start=1):
        reasons = screen(draft, seen)
        seen.add(normalise(draft["question"]))
        candidates.append(
            {"cid": f"c{n:03d}", **draft, "screen": "; ".join(reasons)}
            | {"decision": "drop" if reasons else "", "note": ""}
        )

    with CSV_FILE.open("w", encoding="utf-8-sig", newline="") as f:  # the BOM lets Excel read é
        writer = csv.DictWriter(f, COLUMNS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows([c | {"gold": " ".join(c["gold"])} for c in candidates])
    passages = {(c.id, c.lang): c.embed_text for c in chunks}
    MD_FILE.write_text(review_markdown(candidates, passages), encoding="utf-8", newline="\n")
    dropped = sum(1 for c in candidates if c["screen"])
    print(
        f"wrote {len(candidates)} candidates ({dropped} dropped by rule) to {CSV_FILE}, {MD_FILE}"
    )


if __name__ == "__main__":
    main()
