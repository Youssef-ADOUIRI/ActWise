"""Agreement between the judge and the human labels: evals/reports/judge-calibration.json, .md.

    uv run python evals/judge_kappa.py

Both scores are binarised at 4 (faithful = 4 or 5), as the guide asks: Cohen's kappa on
that split is the M3 target (>= 0.6). Two diagnostics come with it: kappa when only 5
counts as faithful (any unsupported claim fails), and quadratic-weighted kappa on the
1-5 scale. The judge scores each item afresh; the real answers come from the cache.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from sklearn.metrics import cohen_kappa_score

from actwise.evaluation.judge import JUDGE_PROMPT, judge_answer
from actwise.llm.factory import build_judge

LABELS = Path("data/eval/human_labels.csv")
KEY = Path("data/eval/human_labels_key.json")
OUT = Path("evals/reports/judge-calibration")
TARGET = 0.6


def kappa(rows: list[dict[str, Any]], threshold: int) -> float:
    """Cohen's kappa of human and judge after binarising both at `threshold`."""
    human = [r["human"] >= threshold for r in rows]
    judge = [r["judge"] >= threshold for r in rows]
    return round(float(cohen_kappa_score(human, judge)), 4)


def to_markdown(report: dict[str, Any]) -> str:
    """The headline numbers, then every item where human and judge disagree at 4."""
    lines = [
        "# Judge calibration",
        "",
        f"Judge `{report['judge']['fallback'][0]['model']}` with `{report['judge']['prompt']}`, "
        f"against {report['n']} human labels ({report['perturbed']} answers with a planted "
        "unsupported claim). Faithful = score 4 or 5.",
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| **Cohen's kappa, faithful = 4–5 (target ≥ {TARGET})** | **{report['kappa_at_4']}** |",
        f"| Agreement, faithful = 4–5 | {report['agreement_at_4']} |",
        f"| Cohen's kappa, faithful = 5 only | {report['kappa_at_5']} |",
        f"| Quadratic-weighted kappa, 1–5 | {report['kappa_weighted']} |",
        f"| Planted claims marked below 5: human / judge | "
        f"{report['planted_caught']['human']} / {report['planted_caught']['judge']} |",
        f"| Unreadable judge replies | {report['judge_failed']} |",
        "",
        "## Disagreements at 4",
        "",
        "| Item | Kind | Question | Human | Judge | Judge's reason |",
        "|---|---|---|---|---|---|",
    ]
    lines += [
        f"| {r['item']} | {r['kind']} | {r['id']} | {r['human']} | {r['judge']} | {r['reason']} |"
        for r in report["items"]
        if r["judge"] is not None and (r["human"] >= 4) != (r["judge"] >= 4)
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Judge every labelled item, compare with the human scores, and write the report."""
    load_dotenv()
    judge = build_judge(os.environ)
    key = json.loads(KEY.read_text(encoding="utf-8"))
    with LABELS.open(encoding="utf-8-sig") as f:
        labels = {row["item"]: row for row in csv.DictReader(f)}

    items = []
    for name, item in key.items():
        verdict = judge_answer(judge, item["question"], item["sources"], item["answer"])
        items.append(
            {
                "item": name,
                "kind": item["kind"],
                "report": item["report"],
                "id": item["id"],
                "human": int(labels[name]["human_score"]),
                "judge": verdict.score,
                "reason": verdict.reason,
                "notes": labels[name]["notes"],
            }
        )
    scored = [r for r in items if r["judge"] is not None]
    planted = [r for r in scored if r["kind"] == "perturbed"]
    report = {
        "judge": judge.config | {"prompt": JUDGE_PROMPT},
        "n": len(items),
        "perturbed": sum(r["kind"] == "perturbed" for r in items),
        "judge_failed": len(items) - len(scored),
        "kappa_at_4": kappa(scored, 4),
        "agreement_at_4": round(
            sum((r["human"] >= 4) == (r["judge"] >= 4) for r in scored) / len(scored), 4
        ),
        "kappa_at_5": kappa(scored, 5),
        "kappa_weighted": round(
            float(
                cohen_kappa_score(
                    [r["human"] for r in scored], [r["judge"] for r in scored], weights="quadratic"
                )
            ),
            4,
        ),
        "planted_caught": {
            "human": f"{sum(r['human'] < 5 for r in planted)}/{len(planted)}",
            "judge": f"{sum(r['judge'] < 5 for r in planted)}/{len(planted)}",
        },
        "cache_hits_misses": [judge.hits, judge.misses],
        "items": items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    Path(f"{OUT}.json").write_text(json_text, encoding="utf-8", newline="\n")
    Path(f"{OUT}.md").write_text(to_markdown(report), encoding="utf-8", newline="\n")
    print(
        f"kappa at 4: {report['kappa_at_4']} (target {TARGET}), at 5: {report['kappa_at_5']}, "
        f"weighted: {report['kappa_weighted']}; planted caught {report['planted_caught']}; "
        f"cache {report['cache_hits_misses']}"
    )


if __name__ == "__main__":
    main()
