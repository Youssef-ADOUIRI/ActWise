"""Evaluate the risk classifier on the scenarios; write evals/reports/classifier-<split>.json, .md.

    uv run --extra local python evals/run_classifier.py --split dev
    uv run --extra local --extra frameworks python evals/run_classifier.py --agent langgraph

The agent searches with system E (hybrid-binding) and answers with the LLM chain in .env
(offline profile: one model, every call cached). Tune on dev; report test once, at the end.
`--agent langgraph` runs the step 10 LangGraph version instead of the agent.
`--rescore evals/reports/classifier-dev.json` scores saved runs again with the current metrics.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from collections import Counter
from datetime import UTC, datetime
from importlib import import_module
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from run_eval import fingerprint, git_commit, write_report

from actwise.agent.classifier import ai_act_articles
from actwise.agent.schemas import TIERS
from actwise.evaluation.classifier_eval import (
    COSTLY,
    classify_scenarios,
    summarise_classifications,
)
from actwise.evaluation.scenarios import SCENARIOS_FILE, load_scenarios
from actwise.llm.factory import OFFLINE, build_llm
from actwise.retrieval.passages import paragraph_passages
from actwise.retrieval.systems import SERVED, SYSTEMS

# Each module has `classify` and `CLASSIFY_PROMPT`; the LangGraph one needs the frameworks
# extra, so it is imported only when chosen.
CLASSIFIERS = {"agent": "actwise.agent.classifier", "langgraph": "frameworks.langgraph_classifier"}


def to_markdown(report: dict[str, Any]) -> str:
    """The headline numbers, the confusion matrix, and every scenario the agent got wrong."""
    s = report["summary"]
    golds = Counter(r["gold"] for r in report["per_scenario"])
    rescored = report.get("rescored")
    lines = [
        f"# Classifier report: {report['name']}",
        "",
        f"Classifier `{report['agent']}`, prompt `{report['prompt']}`, retrieval `{SERVED}`, "
        f"split `{report['split']}`: "
        f"{s['n']} scenarios ({s['clear']} clear, {s['n'] - s['clear']} ambiguous).",
        "",
    ]
    if rescored:
        lines += [
            f"Scored again from the saved runs on {rescored['date']}, at commit "
            f"`{rescored['git_commit']}`; no model was called.",
            "",
        ]
    lines += [
        "| Metric | Value |",
        "|---|---|",
        f"| **Accuracy, clear scenarios** | **{s['accuracy']}** |",
        f"| Accuracy, ambiguous scenarios | {s['accuracy_ambiguous']} |",
    ]
    lines += [
        f"| **Recall, {tier.replace('_', ' ')} (all scenarios)** | **{s[f'recall_{tier}']}** "
        f"({s['confusion'][tier][tier]} of {golds[tier]}) |"
        for tier in COSTLY
    ]
    lines += [
        f"| Prohibited labelled minimal risk | {s['prohibited_as_minimal']} |",
        f"| Prohibited or high risk labelled minimal risk | {s['dangerous_downgrades']} |",
        f"| Runs that hit the step budget | {s['failed']} |",
        f"| Steps / lookups (reads and searches) per run | {s['steps']} / {s['lookups']} |",
        f"| Seconds / input tokens per run | {s['seconds']} / {s['input_tokens']} |",
        f"| Accuracy by language (clear) | {s['by_lang']} |",
        "",
        "## Confusion matrix (all scenarios: gold rows, predicted columns)",
        "",
        "In the first two rows, a count right of the diagonal is an under-classified system, "
        "except in `needs_more_info`, which asks for the missing facts. "
        "Failed runs are not in the matrix.",
        "",
        f"| Gold \\ predicted | {' | '.join(TIERS)} |",
        "|---" * (len(TIERS) + 1) + "|",
    ]
    lines += [
        f"| **{gold}** | {' | '.join(str(n) for n in predicted.values())} |"
        for gold, predicted in s["confusion"].items()
    ]
    lines += ["", "## Misses", "", "| Scenario | Gold | Predicted | Reasons |", "|---|---|---|---|"]
    lines += [
        f"| {r['id']}{' (ambiguous)' if r['ambiguous'] else ''} | {r['gold']} | {r['predicted']} "
        f"| {' / '.join(r.get('reasons', [])) or r.get('error', '')} |"
        for r in report["per_scenario"]
        if r["predicted"] != r["gold"]
    ]
    return "\n".join(lines) + "\n"


def rescore(path: Path) -> None:
    """Score a saved report's runs again with the current metrics; no model is called."""
    report = json.loads(path.read_text(encoding="utf-8"))
    hits_misses = report["summary"]["cache_hits_misses"]  # of the run itself
    report["summary"] = summarise_classifications(report["per_scenario"]) | {
        "cache_hits_misses": hits_misses
    }
    report["rescored"] = {"date": datetime.now(UTC).date().isoformat(), "git_commit": git_commit()}
    write_report(report, to_markdown(report), path.with_suffix(""))
    print(f"rescored {path}")


def main() -> None:
    """Classify every scenario of the split, then write the JSON and Markdown reports."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--agent", choices=CLASSIFIERS, default="agent")
    parser.add_argument(
        "--rescore", nargs="+", type=Path, metavar="REPORT", help="saved .json reports to rescore"
    )
    args = parser.parse_args()
    if args.rescore:
        for path in args.rescore:
            rescore(path)
        return
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logging.getLogger("actwise").setLevel(logging.INFO)
    load_dotenv()  # .env fills in what the environment doesn't set
    llm = build_llm(os.environ, OFFLINE)

    scenarios = [s for s in load_scenarios() if s.split == args.split]
    retriever = SYSTEMS[SERVED].build()
    articles = ai_act_articles(paragraph_passages())
    chosen = import_module(CLASSIFIERS[args.agent])
    rows = classify_scenarios(llm, retriever.search, articles, scenarios, chosen.classify)
    report = {
        "name": f"classifier-{args.split}"
        if args.agent == "agent"
        else f"classifier-{args.agent}-{args.split}",
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "split": args.split,
        "prompt": chosen.CLASSIFY_PROMPT,
        "agent": args.agent,
        "system": retriever.config,
        "llm": llm.config,
        "inputs": {"scenarios": fingerprint(SCENARIOS_FILE)},
        "summary": summarise_classifications(rows) | {"cache_hits_misses": [llm.hits, llm.misses]},
        "per_scenario": rows,
    }
    out = write_report(report, to_markdown(report))
    s = report["summary"]
    print(
        f"{report['name']}: accuracy {s['accuracy']} (clear), {s['accuracy_ambiguous']} "
        f"(ambiguous); recall prohibited {s['recall_prohibited']}, high risk "
        f"{s['recall_high_risk']}; prohibited as minimal {s['prohibited_as_minimal']}; "
        f"failed {s['failed']}; cache {s['cache_hits_misses']}"
    )
    print(f"wrote {out}.json and {out}.md")


if __name__ == "__main__":
    main()
