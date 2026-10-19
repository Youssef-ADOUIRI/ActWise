"""Collect the facts the review deck shows, straight from the repo.

Writes docs/deck/facts.json. Everything here is measured, never typed by hand:
corpus statistics from data/processed/chunks.jsonl, milestone progress from the
checkboxes in TODO.md, design decisions from docs/decisions/, eval reports found
in evals/reports/, and the latest commit. Narrative (findings, risks, scorecard
values) lives in docs/deck/content.json.

Usage (from the repo root):
    python docs/deck/collect.py               # fast, no test run
    python docs/deck/collect.py --with-tests  # also runs pytest and reads coverage
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "facts.json"

LENGTH_BINS = [(1, 25), (26, 50), (51, 75), (76, 100), (101, 125), (126, 150)]


def git_facts() -> dict:
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()

    try:
        commit, date, subject = run("log", "-1", "--format=%h|%ad|%s", "--date=short").split("|", 2)
        return {
            "commit": commit,
            "date": date,
            "subject": subject,
            "count": int(run("rev-list", "--count", "HEAD")),
        }
    except (OSError, subprocess.CalledProcessError, ValueError):
        return {}


def todo_progress() -> list[dict]:
    """One entry per '## ' section of TODO.md, counting [x] and [ ] boxes."""
    path = ROOT / "TODO.md"
    if not path.exists():
        return []
    sections: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            m = re.match(r"^(M\d+)\s+(.*?)\s*(?:\((weeks?[^)]*)\))?$", title)
            if m:
                sections.append(
                    {
                        "id": m.group(1),
                        "name": m.group(2),
                        "weeks": m.group(3) or "",
                        "done": 0,
                        "total": 0,
                    }
                )
            else:
                sections.append(
                    {"id": "Setup", "name": title.split(":")[0], "weeks": "", "done": 0, "total": 0}
                )
        elif sections and re.match(r"^\s*- \[[ xX]\]", line):
            sections[-1]["total"] += 1
            if re.match(r"^\s*- \[[xX]\]", line):
                sections[-1]["done"] += 1
    return sections


def corpus_facts() -> dict:
    path = ROOT / "data" / "processed" / "chunks.jsonl"
    if not path.exists():
        return {}
    rows = [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    words = [len(r["text"].split()) for r in rows]

    by_group = Counter(f"{r['law']}|{r['lang']}|{r['kind']}" for r in rows)
    units = Counter()
    for law, lang, kind, _number in {(r["law"], r["lang"], r["kind"], r["number"]) for r in rows}:
        units[f"{law}|{lang}|{kind}"] += 1

    hist = {f"{lo}-{hi}": sum(1 for w in words if lo <= w <= hi) for lo, hi in LENGTH_BINS}
    windowed = [r for r in rows if "#" in r["id"]]
    per_lang = {}
    for lang in sorted({r["lang"] for r in rows}):
        w = [len(r["text"].split()) for r in rows if r["lang"] == lang]
        per_lang[lang] = {
            "chunks": len(w),
            "median_words": statistics.median(w),
            "mean_words": round(statistics.mean(w), 1),
        }

    return {
        "total_chunks": len(rows),
        "by_group": dict(sorted(by_group.items())),
        "units": dict(sorted(units.items())),
        "words": {
            "median": statistics.median(words),
            "mean": round(statistics.mean(words), 1),
            "min": min(words),
            "max": max(words),
        },
        "length_histogram": hist,
        "windowed_chunks": len(windowed),
        "split_paragraphs": len({(r["id"].split("#")[0], r["lang"]) for r in windowed}),
        "per_lang": per_lang,
    }


def decisions() -> list[dict]:
    out = []
    for path in sorted((ROOT / "docs" / "decisions").glob("[0-9]*.md")):
        text = path.read_text(encoding="utf-8")
        title = re.search(r"^#\s*(.+)$", text, re.M)
        chosen = re.search(r"\*\*Chosen:\*\*\s*(.+)", text)
        out.append(
            {
                "file": path.name,
                "title": title.group(1).strip() if title else path.stem,
                "chosen": chosen.group(1).strip() if chosen else "",
            }
        )
    return out


def eval_reports() -> list[str]:
    folder = ROOT / "evals" / "reports"
    return sorted(p.name for p in folder.glob("*.json")) if folder.exists() else []


def test_facts() -> dict:
    """Run the suite once and read the pass count and total coverage."""
    proc = subprocess.run(
        ["uv", "run", "pytest", "-q", "--cov=src", "--cov-report=term"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    passed = re.search(r"(\d+) passed", proc.stdout)
    failed = re.search(r"(\d+) failed", proc.stdout)
    cov = re.search(r"^TOTAL\s+.*?(\d+)%\s*$", proc.stdout, re.M)
    return {
        "passed": int(passed.group(1)) if passed else 0,
        "failed": int(failed.group(1)) if failed else 0,
        "coverage_pct": int(cov.group(1)) if cov else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--with-tests", action="store_true", help="run pytest and record pass count and coverage"
    )
    args = parser.parse_args()

    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    facts = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git": git_facts() or previous.get("git", {}),
        "progress": todo_progress(),
        "corpus": corpus_facts(),
        "decisions": decisions(),
        "eval_reports": eval_reports(),
        "tests": previous.get("tests", {}),
    }
    if args.with_tests:
        measured = test_facts()
        # Keep the last good numbers if the run could not be parsed (uv missing, collection error).
        if measured["passed"] or measured["failed"]:
            facts["tests"] = {**measured, "measured_at": facts["generated_at"]}
        else:
            print("warning: could not read pytest results, keeping the previous test numbers")
    OUT.write_text(json.dumps(facts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    c = facts["corpus"]
    done = sum(s["done"] for s in facts["progress"])
    total = sum(s["total"] for s in facts["progress"])
    print(f"facts.json: {c.get('total_chunks', 0)} chunks, {done}/{total} TODO items done")


if __name__ == "__main__":
    main()
