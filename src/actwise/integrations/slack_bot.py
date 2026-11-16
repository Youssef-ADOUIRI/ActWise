"""The Slack command /actwise, over Socket Mode: no public URL, a free workspace is enough.

    uv run --extra integrations python -m actwise.integrations.slack_bot   (make slack)

Needs SLACK_BOT_TOKEN and SLACK_APP_TOKEN (docs/integrations.md) and the API at
ACTWISE_API_URL. Replies are ephemeral: only the user who typed the command sees them,
so a pasted system description stays private.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

from dotenv import load_dotenv

from actwise.integrations.client import ApiClient, ApiError
from actwise.integrations.formatting import (
    HELP,
    format_ask,
    format_classification,
    parse_command,
)

WAIT = "Reading the law…"
ROUTES: dict[str, tuple[str, str, Callable[[dict[str, Any]], str]]] = {
    "ask": ("/ask", "question", format_ask),  # action: (path, field, formatter)
    "classify": ("/classify", "description", format_classification),
}


def handle(
    ack: Callable[..., Any], respond: Callable[..., Any], command: dict[str, Any], api: Any
) -> None:
    """Acknowledge within Slack's 3 seconds, then reply from the API."""
    action, text = parse_command(command.get("text", ""))
    if action == "help":
        ack(HELP)
        return
    ack(WAIT)
    path, field, formatter = ROUTES[action]
    try:
        reply = formatter(api.post(path, json={field: text}))
    except ApiError as exc:
        reply = f"ActWise could not answer. {exc}"
    respond(text=reply, response_type="ephemeral")


def main() -> None:
    """Connect to Slack and serve /actwise until stopped."""
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    load_dotenv()  # .env fills in what the environment doesn't set
    api = ApiClient.from_env(os.environ)
    app = App(token=os.environ["SLACK_BOT_TOKEN"])

    @app.command("/actwise")
    def actwise(ack: Any, respond: Any, command: Any) -> None:
        """Bolt passes the arguments by name."""
        handle(ack, respond, command, api)

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()
