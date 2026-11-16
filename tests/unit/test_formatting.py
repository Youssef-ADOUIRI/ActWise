from actwise.agent.schemas import DISCLAIMER
from actwise.integrations.formatting import (
    HELP,
    format_ask,
    format_classification,
    parse_command,
)

CLASSIFICATION = {
    "tier": "needs_more_info",
    "reasons": ["It may rank job applicants."],
    "citations": ["AIA-AnnexIII-4", "AIA-Art6-3"],
    "confidence": 0.55,
    "follow_up_questions": ["Does it rank or filter candidates?"],
    "model": "gemini-test",
    "disclaimer": DISCLAIMER,
}


def test_parse_command():
    """`ask ...` and `classify ...` are parsed, any case; anything else asks for help."""
    assert parse_command("  ask  What is high risk? ") == ("ask", "What is high risk?")
    assert parse_command("CLASSIFY A CV ranker") == ("classify", "A CV ranker")
    assert [parse_command(text) for text in ["", "ask", "help me", "summarise x"]] == [
        ("help", "")
    ] * 4
    assert "/actwise ask" in HELP and "/actwise classify" in HELP


def test_format_classification():
    """Tier, confidence as a percentage, reasons, labelled citations, follow-ups, notice."""
    text = format_classification(CLASSIFICATION)

    assert "Needs more info" in text and "55%" in text
    assert "It may rank job applicants." in text
    assert "AI Act, Annex III, point 4" in text and "AIA-Art6-3" in text
    assert "Does it rank or filter candidates?" in text
    assert text.rstrip().endswith(f"_{DISCLAIMER}_")


def test_format_classification_without_follow_ups():
    """No follow-up heading when the classifier has nothing to ask."""
    text = format_classification(CLASSIFICATION | {"tier": "high_risk", "follow_up_questions": []})

    assert "High risk" in text and "needs to know" not in text


def test_format_ask():
    """The answer, the sources it cites under their labels, and the notice; a refusal cites none."""
    answer = {
        "answer": "Social scoring is banned [AIA-Art5-1].",
        "refused": False,
        "citations": ["AIA-Art5-1"],
        "disclaimer": DISCLAIMER,
    }
    refusal = answer | {"answer": "The sources don't cover this.", "refused": True, "citations": []}

    assert "AI Act, Art. 5(1)" in format_ask(answer)
    assert "Sources" not in format_ask(refusal)
    assert format_ask(refusal).startswith("The sources don't cover this.")
