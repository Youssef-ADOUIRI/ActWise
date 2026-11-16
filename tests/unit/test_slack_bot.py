from actwise.agent.schemas import DISCLAIMER
from actwise.integrations.client import ApiError
from actwise.integrations.slack_bot import HELP, WAIT, handle, parse_command
from tests.unit.toys import CLASSIFICATION, FakeApi

ANSWER = {
    "answer": "Banned [AIA-Art5-1].",
    "citations": ["AIA-Art5-1"],
    "sources": [{"id": "AIA-Art5-1", "label": "AI Act, Art. 5(1)"}],
    "disclaimer": DISCLAIMER,
}


def run(text, api):
    """Handle `/actwise <text>`; the events in the order Slack would see them."""
    events = []
    handle(
        lambda message: events.append(("ack", message)),
        lambda **reply: events.append(("respond", reply)),
        {"text": text},
        api,
    )
    return events


def test_parse_command():
    """`ask ...` and `classify ...` are parsed, any case; anything else asks for help."""
    assert parse_command("  ask  What is high risk? ") == ("ask", "What is high risk?")
    assert parse_command("CLASSIFY A CV ranker") == ("classify", "A CV ranker")
    assert [parse_command(text) for text in ["", "ask", "help me", "summarise x"]] == [
        ("help", "")
    ] * 4
    assert "/actwise ask" in HELP and "/actwise classify" in HELP


def test_slack_handler():
    """`ack` comes first; then the formatted answer, only for the user who asked."""
    api = FakeApi(ANSWER)

    events = run("ask Is social scoring banned?", api)

    assert events[0] == ("ack", WAIT)
    assert events[1][0] == "respond"
    assert "AI Act, Art. 5(1)" in events[1][1]["text"]
    assert events[1][1]["response_type"] == "ephemeral"
    assert api.calls == [("/ask", {"json": {"question": "Is social scoring banned?"}})]


def test_slack_handler_classifies():
    """`classify` posts the description to /classify."""
    api = FakeApi(CLASSIFICATION)

    events = run("classify A tool that ranks CVs.", api)

    assert "High risk" in events[1][1]["text"]
    assert api.calls == [("/classify", {"json": {"description": "A tool that ranks CVs."}})]


def test_slack_handler_reports_api_errors():
    """An API error becomes a readable reply, not a crash."""
    events = run("ask Anything?", FakeApi(error=ApiError("Error 503: no model answered")))

    assert "Error 503: no model answered" in events[1][1]["text"]


def test_slack_handler_help_needs_no_api():
    """An unknown command is acknowledged with the usage, and the API is not called."""
    api = FakeApi()

    assert run("summarise this", api) == [("ack", HELP)]
    assert api.calls == []
