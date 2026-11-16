import asyncio

import pytest

from actwise.agent.schemas import DISCLAIMER
from actwise.integrations.client import ApiError
from tests.unit.test_slack_bot import FakeApi

pytest.importorskip("mcp")  # the integrations extra
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402

from actwise.integrations.mcp_server import build_server  # noqa: E402

CLASSIFICATION = {
    "tier": "high_risk",
    "reasons": ["It ranks job applicants."],
    "citations": ["AIA-AnnexIII-4"],
    "confidence": 0.8,
    "follow_up_questions": [],
    "disclaimer": DISCLAIMER,
}


def test_mcp_tools_registered():
    """The server lists exactly the two ActWise tools, each with a description."""
    tools = asyncio.run(build_server(FakeApi()).list_tools())

    assert sorted(tool.name for tool in tools) == ["ask_ai_act", "classify_ai_system"]
    assert all(tool.description for tool in tools)


def test_mcp_tool_returns_the_formatted_reply():
    """A tool call posts to the API and returns the text a person would read."""
    api = FakeApi(CLASSIFICATION)
    server = build_server(api)

    result = asyncio.run(server.call_tool("classify_ai_system", {"description": "A CV ranker."}))

    assert not result.is_error
    assert "High risk" in result.content[0].text
    assert api.calls == [("/classify", {"json": {"description": "A CV ranker."}})]


def test_mcp_tool_reports_api_errors():
    """An API error is a tool error with the API's message, which the client shows."""
    server = build_server(FakeApi(error=ApiError("Error 429: the demo's daily quota is used up")))

    with pytest.raises(ToolError, match="daily quota"):
        asyncio.run(server.call_tool("ask_ai_act", {"question": "Is it banned?"}))
