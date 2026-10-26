"""Evaluate the risk classifier on the scenarios; write evals/reports/classifier-<split>.json, .md.

    uv run --extra local python evals/run_classifier.py --split dev

The agent searches with system E (hybrid-binding) and answers with the LLM chain in .env
(offline profile: one model, every call cached). Tune on dev; report test once, at the end.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from run_eval import REPORTS, SYSTEMS, fingerprint, git_commit

from actwise.agent.classifier import CLASSIFY_PROMPT
from actwise.evaluation.classifier_eval import classify_scenarios, summarise_classifications
from actwise.evaluation.scenarios import SCENARIOS_FILE, load_scenarios
from actwise.llm.factory import OFFLINE, build_llm

SYSTEM = "hybrid-binding"


def to_markdown(report: dict[str, Any]) -> str:
    """The headline numbers, the confusion matrix, and every scenario the agent got wrong."""
    s = report["summary"]
    lines = [
        f"# Classifier report: {report['name']}",
        "",
        f"Prompt `{report['prompt']}`, retrieval `{SYSTEM}`, split `{report['split']}`: "
        f"{s['n']} scenarios ({s['clear']} clear, {s['n'] - s['clear']} ambiguous).",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| **Accuracy, clear scenarios** | **{s['accuracy']}** |",
        f"| Accuracy, ambiguous scenarios | {s['accuracy_ambiguous']} |",
        f"| Prohibited labelled minimal risk | {s['prohibited_as_minimal']} |",
        f"| Prohibited or high risk labelled minimal risk | {s['dangerous_downgrades']} |",
        f"| Runs that hit the step budget | {s['failed']} |",
        f"| Results citing only retrieved ids | {s['citations_retrieved']} |",
        f"| Steps / searches per run | {s['steps']} / {s['searches']} |",
        "",
        "## Confusion (clear scenarios: gold → predicted)",
        "",
    ]
    lines += [f"- **{gold}**: {predicted}" for gold, predicted in s["confusion"].items()]
    lines += ["", "## Misses", "", "| Scenario | Gold | Predicted | Reasons |", "|---|---|---|---|"]
    lines += [
        f"| {r['id']}{' (ambiguous)' if r['ambiguous'] else ''} | {r['gold']} | {r['predicted']} "
        f"| {' / '.join(r.get('reasons', [])) or r.get('error', '')} |"
        for r in report["per_scenario"]
        if r["predicted"] != r["gold"]
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Classify every scenario of the split, then write the JSON and Markdown reports."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logging.getLogger("actwise").setLevel(logging.INFO)
    load_dotenv()  # .env fills in what the environment doesn't set
    llm = build_llm(os.environ, OFFLINE)

    scenarios = [s for s in load_scenarios() if s.split == args.split]
    retriever = SYSTEMS[SYSTEM].build()
    rows = classify_scenarios(llm, retriever.search, scenarios)
    report = {
        "name": f"classifier-{args.split}",
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "split": args.split,
        "prompt": CLASSIFY_PROMPT,
        "system": retriever.config,
        "llm": llm.config,
        "inputs": {"scenarios": fingerprint(SCENARIOS_FILE)},
        "summary": summarise_classifications(rows) | {"cache_hits_misses": [llm.hits, llm.misses]},
        "per_scenario": rows,
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / report["name"]
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    Path(f"{out}.json").write_text(json_text, encoding="utf-8", newline="\n")
    Path(f"{out}.md").write_text(to_markdown(report), encoding="utf-8", newline="\n")
    s = report["summary"]
    print(
        f"{report['name']}: accuracy {s['accuracy']} (clear), {s['accuracy_ambiguous']} "
        f"(ambiguous); prohibited as minimal {s['prohibited_as_minimal']}; failed {s['failed']}; "
        f"cache {s['cache_hits_misses']}"
    )
    print(f"wrote {out}.json and {out}.md")


if __name__ == "__main__":
    main()
