"""Risk scenarios: AI system descriptions with a gold AI Act tier (data/eval/risk_scenarios.csv).

Each row names the rule that decides its tier and quotes the deciding sentence from the
corpus; a person verified every label. Ambiguous scenarios are scored apart. The file
is a CSV so that labels can be checked and fixed in a spreadsheet.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

SCENARIOS_FILE = Path("data/eval/risk_scenarios.csv")


@dataclass(frozen=True)
class Scenario:
    id: str
    split: str  # "dev" | "test"
    lang: str  # "en" | "fr"
    ambiguous: bool
    gold: str  # one of agent.schemas.TIERS
    rule: str  # paragraph id of the deciding rule; empty when no rule applies
    evidence: str  # the deciding sentence, quoted from the rule's paragraph
    description: str
    verified: str  # "yes" once a person has checked the label


def load_scenarios(path: Path = SCENARIOS_FILE) -> list[Scenario]:
    """Read every scenario of the CSV (UTF-8 with or without a BOM)."""
    with path.open(encoding="utf-8-sig") as f:
        return [
            Scenario(
                row["id"],
                row["split"],
                row["lang"],
                row["ambiguous"] == "yes",
                row["gold"],
                row["rule"],
                row["evidence"],
                row["description"],
                row["verified"],
            )
            for row in csv.DictReader(f)
        ]
