"""MCP server: any MCP client (VS Code, IDEs, agents) calls ActWise as two tools.

    uv run --extra integrations python -m actwise.integrations.mcp_server   (make mcp)

The client starts it over stdio (.vscode/mcp.json), so stdout carries the protocol and
nothing else may print there. Its tools call the API at ACTWISE_API_URL: `make serve` first.
"""

from __future__ import annotations

import os
from typing import Any, Literal

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from actwise.integrations.client import ApiClient, ApiError
from actwise.integrations.formatting import format_ask, format_classification

INSTRUCTIONS = (
    "Cited answers on the EU AI Act and the GDPR, and AI Act risk classification. "
    "Information only, not legal advice."
)


def build_server(api: Any) -> MCPServer:
    """The server and its two tools, which post to `api`."""
    server = MCPServer("actwise", instructions=INSTRUCTIONS)

    def post(path: str, payload: dict[str, str]) -> dict[str, Any]:
        """The API's JSON; an API error becomes a tool error the client shows."""
        try:
            return api.post(path, json=payload)
        except ApiError as exc:
            raise ToolError(str(exc)) from exc

    @server.tool()
    def ask_ai_act(question: str, lang: Literal["en", "fr"] = "en") -> str:
        """Answer a question on the EU AI Act or the GDPR from the law's text, with citations."""
        return format_ask(post("/ask", {"question": question, "lang": lang}))

    @server.tool()
    def classify_ai_system(description: str) -> str:
        """Classify an AI system into an EU AI Act risk tier, with cited reasons.

        The tiers are prohibited, high risk, transparency only and minimal risk; when facts
        are missing, the answer is "needs more info" with the questions to ask.
        """
        return format_classification(post("/classify", {"description": description}))

    return server


if __name__ == "__main__":
    load_dotenv()  # .env fills in what the environment doesn't set
    build_server(ApiClient.from_env(os.environ)).run()  # stdio
