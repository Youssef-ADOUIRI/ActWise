"""Draw up to 60 answers for human scoring: data/eval/human_labels.csv, .md and _key.json.

    uv run python evals/make_calibration.py

Up to 15 real answers come from each dev answer report (plain, answer.v1, answer.v2).
Up to 15 more are real answers that the LLM rewrote with one unsupported claim: without
some unfaithful items, nearly every label is "faithful" and kappa can't tell a good judge
from a bad one. The sheet hides the source of each item and the judge's score, so the
labels stay blind; the key file keeps everything step 6b needs to compute kappa.
"""

from __future__ import annotations

import csv
import json
import os
import random
from pathlib import Path

from dotenv import load_dotenv

from actwise.evaluation.answers import quote
from actwise.generation.prompts import load_prompt
from actwise.generation.rag import format_sources
from actwise.llm.factory import OFFLINE, build_llm

REPORTS = [
    Path("evals/reports/baseline-dev-plain.json"),
    Path("evals/reports/hybrid-binding-dev-answer.v1.json"),
    Path("evals/reports/hybrid-binding-dev-answer.v2.json"),
]
REAL, PERTURBED = 15, 15  # real answers per report; perturbed ones in all
PERTURB_PROMPT = "perturb.v1"
OUT = Path("data/eval")


def main() -> None:
    """Sample and perturb the answers, then write the sheet, the reading file and the key."""
    load_dotenv()
    llm = build_llm(os.environ, OFFLINE)
    rng = random.Random(42)
    items, rest = [], []
    for path in REPORTS:
        rows = json.loads(path.read_text(encoding="utf-8"))["answers"]["per_question"]
        answered = [r for r in rows if not r["refused"]]
        rng.shuffle(answered)
        items += [{"report": path.stem, "kind": "real", **row} for row in answered[:REAL]]
        rest += [{"report": path.stem, "kind": "perturbed", **row} for row in answered[REAL:]]
    rng.shuffle(rest)
    for item in rest[:PERTURBED]:  # each question appears once, real or perturbed
        sources = format_sources(item["sources"])
        messages = [
            {"role": "system", "content": load_prompt(PERTURB_PROMPT)},
            {"role": "user", "content": f"Sources:\n\n{sources}\n\nAnswer:\n{item['answer']}"},
        ]
        items.append(item | {"answer": llm.chat(messages, temperature=0).text.strip()})
    rng.shuffle(items)

    key, lines = {}, ["# Human labels", ""]
    lines += [
        "Score each answer from 1 to 5 in `human_labels.csv`, on one question only: is",
        "every claim supported by the sources shown? (5 = all supported; 4 = a minor detail",
        "is not; 3 = some claims are not; 2 = most are not; 1 = contradicts or unrelated.)",
    ]
    for n, item in enumerate(items, start=1):
        name = f"h{n:02d}"
        key[name] = {k: item[k] for k in ("report", "kind", "id", "question", "sources", "answer")}
        lines += ["", f"## {name}", "", f"**Question:** {item['question']}", "", "**Sources:**"]
        for s in item["sources"]:
            lines += ["", f"[{s['id']}] {s['label']}", ""]
            lines += quote(s["text"])
        lines += ["", "**Answer:**", ""] + quote(item["answer"])

    with (OUT / "human_labels.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["item", "human_score", "notes"])
        writer.writerows([[name, "", ""] for name in key])
    (OUT / "human_labels.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    key_text = json.dumps(key, indent=1, ensure_ascii=False) + "\n"
    (OUT / "human_labels_key.json").write_text(key_text, encoding="utf-8", newline="\n")
    perturbed = sum(item["kind"] == "perturbed" for item in items)
    print(f"wrote {len(key)} items ({perturbed} perturbed) to {OUT}/human_labels.csv and .md")


if __name__ == "__main__":
    main()
