"""Pure helpers for the Slack bot and the MCP server: parse a command, format the API's JSON.

No Slack or MCP import here, so the tests need neither. The text uses Slack's mrkdwn
(*bold*, _italic_), which an MCP client's model reads as plain text.
"""

from __future__ import annotations

from typing import Any

from actwise.ids import human_label

COMMANDS = ("ask", "classify")
HELP = "Usage: `/actwise ask <question>` or `/actwise classify <describe your AI system>`"


def parse_command(text: str) -> tuple[str, str]:
    """'ask What is high risk?' -> ('ask', 'What is high risk?'); anything else -> ('help', '')."""
    parts = text.strip().split(maxsplit=1)
    if len(parts) < 2 or parts[0].lower() not in COMMANDS:
        return "help", ""
    return parts[0].lower(), parts[1]


def cited(ids: list[str]) -> str:
    """Each id under its label: 'AI Act, Art. 5(1) `AIA-Art5-1`, ...'."""
    return ", ".join(f"{human_label(i)} `{i}`" for i in ids)


def format_ask(data: dict[str, Any]) -> str:
    """The answer (or the refusal), the sources it cites, and the notice."""
    lines = [data["answer"]]
    if data["citations"]:
        lines.append(f"*Sources:* {cited(data['citations'])}")
    lines.append(f"_{data['disclaimer']}_")
    return "\n\n".join(lines)


def format_classification(data: dict[str, Any]) -> str:
    """The tier and confidence, the reasons, the citations, any follow-up questions, the notice."""
    tier = data["tier"].replace("_", " ").capitalize()
    lines = [f"*Risk tier: {tier}* (confidence {data['confidence']:.0%})"]
    lines += [f"- {reason}" for reason in data["reasons"]]
    lines.append(f"*Cited:* {cited(data['citations'])}")
    if data["follow_up_questions"]:
        lines.append("*To decide, the classifier needs to know:*")
        lines += [f"- {question}" for question in data["follow_up_questions"]]
    lines.append(f"_{data['disclaimer']}_")
    return "\n".join(lines)
