"""How the clients show the API's JSON: the tier, cited ids under their labels, the notice.

No Slack, MCP or Streamlit import here, so the tests need none. The text uses Slack's
mrkdwn (*bold*, _italic_), which an MCP client's model reads as plain text.
"""

from __future__ import annotations

from typing import Any

from actwise.ids import human_label

FOLLOW_UPS = "To decide, the classifier needs to know:"


def tier_label(tier: str) -> str:
    """'needs_more_info' -> 'Needs more info'."""
    return tier.replace("_", " ").capitalize()


def cited(ids: list[str], labels: dict[str, str] | None = None) -> str:
    """Each id under its label: 'AI Act, Art. 5(1) `AIA-Art5-1`, ...'.

    `labels` are the API's own, in the answer's language; other ids get English ones.
    """
    labels = labels or {}
    return ", ".join(f"{labels.get(i) or human_label(i)} `{i}`" for i in ids)


def format_ask(data: dict[str, Any]) -> str:
    """The answer (or the refusal), the sources it cites, and the notice."""
    lines = [data["answer"]]
    if data["citations"]:
        labels = {source["id"]: source["label"] for source in data["sources"]}
        lines.append(f"*Sources:* {cited(data['citations'], labels)}")
    lines.append(f"_{data['disclaimer']}_")
    return "\n\n".join(lines)


def format_classification(data: dict[str, Any]) -> str:
    """The tier and confidence, the reasons, the citations, any follow-up questions, the notice."""
    lines = [f"*Risk tier: {tier_label(data['tier'])}* (confidence {data['confidence']:.0%})"]
    lines += [f"- {reason}" for reason in data["reasons"]]
    lines.append(f"*Cited:* {cited(data['citations'])}")
    if data["follow_up_questions"]:
        lines.append(f"*{FOLLOW_UPS}*")
        lines += [f"- {question}" for question in data["follow_up_questions"]]
    lines.append(f"_{data['disclaimer']}_")
    return "\n".join(lines)
