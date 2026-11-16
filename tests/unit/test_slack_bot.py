from actwise.agent.schemas import DISCLAIMER
from actwise.integrations.client import ApiError
from actwise.integrations.formatting import HELP
from actwise.integrations.slack_bot import WAIT, handle

ANSWER = {"answer": "Banned [AIA-Art5-1].", "citations": ["AIA-Art5-1"], "disclaimer": DISCLAIMER}


class FakeApi:
    """Answers every POST with `reply`, or raises `error`; records each request."""

    def __init__(self, reply=None, error=None):
        """Reply with `reply`, or raise `error`."""
        self.reply, self.error, self.calls = reply, error, []

    def post(self, path, **request):
        """The canned reply."""
        self.calls.append((path, request))
        if self.error:
            raise self.error
        return self.reply


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
    reply = {
        "tier": "prohibited",
        "reasons": ["Social scoring."],
        "citations": ["AIA-Art5-1"],
        "confidence": 0.9,
        "follow_up_questions": [],
        "disclaimer": DISCLAIMER,
    }
    api = FakeApi(reply)

    events = run("classify A city scores its residents.", api)

    assert "Prohibited" in events[1][1]["text"]
    assert api.calls == [("/classify", {"json": {"description": "A city scores its residents."}})]


def test_slack_handler_reports_api_errors():
    """An API error becomes a readable reply, not a crash."""
    events = run("ask Anything?", FakeApi(error=ApiError("Error 503: no model answered")))

    assert "Error 503: no model answered" in events[1][1]["text"]


def test_slack_handler_help_needs_no_api():
    """An unknown command is acknowledged with the usage, and the API is not called."""
    api = FakeApi()

    assert run("summarise this", api) == [("ack", HELP)]
    assert api.calls == []
