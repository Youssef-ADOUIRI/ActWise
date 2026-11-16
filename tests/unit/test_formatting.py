from actwise.agent.schemas import DISCLAIMER
from actwise.integrations.formatting import format_ask, format_classification, tier_label
from tests.unit.toys import CLASSIFICATION

UNCLEAR = CLASSIFICATION | {
    "tier": "needs_more_info",
    "confidence": 0.55,
    "follow_up_questions": ["Does it rank or filter candidates?"],
}


def test_format_classification():
    """Tier, confidence as a percentage, reasons, labelled citations, follow-ups, notice."""
    text = format_classification(UNCLEAR)

    assert "Needs more info" in text and "55%" in text
    assert "It ranks job applicants." in text
    assert "AI Act, Annex III, point 4" in text and "AIA-Art6-2" in text
    assert "Does it rank or filter candidates?" in text
    assert text.rstrip().endswith(f"_{DISCLAIMER}_")


def test_format_classification_without_follow_ups():
    """No follow-up heading when the classifier has nothing to ask."""
    text = format_classification(CLASSIFICATION)

    assert "High risk" in text and "needs to know" not in text


def test_format_ask_labels_citations_from_the_sources():
    """The answer, its cited sources under the API's labels (in the answer's language), the
    notice; a refusal cites none."""
    answer = {
        "answer": "La notation sociale est interdite [AIA-Art5-1].",
        "citations": ["AIA-Art5-1"],
        "sources": [{"id": "AIA-Art5-1", "label": "AI Act, art. 5, paragraphe 1"}],
        "disclaimer": DISCLAIMER,
    }
    refusal = answer | {"answer": "The sources don't cover this.", "citations": []}

    assert "AI Act, art. 5, paragraphe 1 `AIA-Art5-1`" in format_ask(answer)
    assert "Sources" not in format_ask(refusal)
    assert format_ask(refusal).startswith("The sources don't cover this.")


def test_tier_label():
    """Underscores become spaces, the first letter a capital."""
    assert tier_label("transparency_only") == "Transparency only"
