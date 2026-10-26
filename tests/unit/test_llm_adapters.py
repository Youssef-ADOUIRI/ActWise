import json
import time
from dataclasses import asdict
from types import SimpleNamespace

from actwise.llm.anthropic_adapter import AnthropicLLM, to_anthropic_messages
from actwise.llm.base import ToolCall
from actwise.llm.openai_compat import OpenAICompatLLM, to_openai_messages

TOOL = {
    "name": "lookup",
    "description": "Fetch an article by id.",
    "parameters": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]},
}
CONVERSATION = [
    {"role": "system", "content": "You answer questions about the AI Act."},
    {"role": "user", "content": "What does Article 5 ban?"},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {"id": "c1", "name": "lookup", "arguments": {"id": "AIA-Art5"}},
            {"id": "c2", "name": "lookup", "arguments": {"id": "AIA-Art6"}},
        ],
    },
    {"role": "tool", "tool_call_id": "c1", "content": "Article 5: prohibited practices."},
    {"role": "tool", "tool_call_id": "c2", "content": "Article 6: high-risk systems."},
]

OPENAI_RESPONSE = SimpleNamespace(
    choices=[
        SimpleNamespace(
            message=SimpleNamespace(
                content=None,
                tool_calls=[
                    SimpleNamespace(
                        id="c9",
                        function=SimpleNamespace(name="lookup", arguments='{"id": "AIA-Art5"}'),
                    )
                ],
            )
        )
    ],
    usage=SimpleNamespace(prompt_tokens=42, completion_tokens=7),
)
ANTHROPIC_RESPONSE = SimpleNamespace(
    content=[
        SimpleNamespace(type="thinking", thinking="The user asks about Article 5."),
        SimpleNamespace(type="text", text="Let me check."),
        SimpleNamespace(type="tool_use", id="t1", name="lookup", input={"id": "AIA-Art5"}),
    ],
    usage=SimpleNamespace(input_tokens=50, output_tokens=9),
)


class FakeCreate:
    """Stands in for an SDK's `create()`: records the request, returns a canned response."""

    def __init__(self, response):
        """Answer every request with `response`."""
        self.response, self.kwargs = response, {}

    def __call__(self, **kwargs):
        """Record the request."""
        self.kwargs = kwargs
        return self.response


def openai_llm(create):
    """An OpenAI-compatible adapter whose client calls `create`."""
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    return OpenAICompatLLM("gemini-x", "key", "https://llm.invalid/v1", "gemini", 60.0, client)


def anthropic_llm(create):
    """An Anthropic adapter whose client calls `create`."""
    return AnthropicLLM(
        "claude-x", "key", 60.0, SimpleNamespace(messages=SimpleNamespace(create=create))
    )


def test_openai_adapter_round_trip():
    """Tools go out as functions with max_tokens (R12); tool calls come back parsed from JSON."""
    create = FakeCreate(OPENAI_RESPONSE)

    response = openai_llm(create).chat(CONVERSATION, tools=[TOOL], temperature=0, max_tokens=300)

    assert create.kwargs["tools"] == [{"type": "function", "function": TOOL}]
    assert create.kwargs["tool_choice"] == "auto"
    assert (create.kwargs["temperature"], create.kwargs["max_tokens"]) == (0, 300)
    assert response.tool_calls == [ToolCall("c9", "lookup", {"id": "AIA-Art5"})]
    assert (response.text, response.input_tokens, response.output_tokens) == ("", 42, 7)
    assert response.model == "gemini-x"


def test_openai_messages_carry_tool_calls_as_json():
    """Assistant tool calls become function calls with JSON-string arguments."""
    messages = to_openai_messages(CONVERSATION)

    assert messages[2]["content"] is None
    assert messages[2]["tool_calls"][0] == {
        "id": "c1",
        "type": "function",
        "function": {"name": "lookup", "arguments": json.dumps({"id": "AIA-Art5"})},
    }
    assert messages[3] == {
        "role": "tool",
        "tool_call_id": "c1",
        "content": CONVERSATION[3]["content"],
    }


def test_anthropic_adapter():
    """System split off, input_schema used, tool results merged, tool_use parsed, no temperature."""
    create = FakeCreate(ANTHROPIC_RESPONSE)

    response = anthropic_llm(create).chat(CONVERSATION, tools=[TOOL], temperature=0, max_tokens=300)

    sent = create.kwargs
    assert sent["system"] == "You answer questions about the AI Act."
    assert sent["tools"] == [
        {"name": "lookup", "description": TOOL["description"], "input_schema": TOOL["parameters"]}
    ]
    assert "temperature" not in sent  # R11: the Messages API no longer takes one
    assert sent["max_tokens"] == 300
    assert [m["role"] for m in sent["messages"]] == ["user", "assistant", "user"]
    assert [block["tool_use_id"] for block in sent["messages"][2]["content"]] == ["c1", "c2"]
    assert response.text == "Let me check."
    assert response.tool_calls == [ToolCall("t1", "lookup", {"id": "AIA-Art5"})]
    assert (response.input_tokens, response.output_tokens, response.model) == (50, 9, "claude-x")


def test_anthropic_messages_turn_tool_calls_into_blocks():
    """An assistant turn with text and a tool call becomes a text block then a tool_use block."""
    messages = to_anthropic_messages(
        [
            {"role": "user", "content": "Ban?"},
            {
                "role": "assistant",
                "content": "Checking.",
                "tool_calls": CONVERSATION[2]["tool_calls"],
            },
        ]
    )

    assert [block["type"] for block in messages[1]["content"]] == ["text", "tool_use", "tool_use"]
    assert messages[1]["content"][1]["input"] == {"id": "AIA-Art5"}


def test_http_timeout_shrinks_to_the_deadline():
    """A call has its usual timeout, or only the time left before the deadline (R5)."""
    openai_create, anthropic_create = FakeCreate(OPENAI_RESPONSE), FakeCreate(ANTHROPIC_RESPONSE)
    question = CONVERSATION[1:2]

    openai_llm(openai_create).chat(question)
    assert openai_create.kwargs["timeout"] == 60.0

    for create, llm in ((openai_create, openai_llm), (anthropic_create, anthropic_llm)):
        llm(create).chat(question, deadline=time.monotonic() + 5)
        assert 4 < create.kwargs["timeout"] <= 5


def test_sdk_clients_do_not_retry_on_their_own():
    """The SDKs' own retries are off, so RetryingLLM is the only retry layer (R13)."""
    openai_client = OpenAICompatLLM("m", "key", "http://localhost:11434/v1", "ollama", 60.0).client
    anthropic_client = AnthropicLLM("m", "key", 60.0).client

    assert openai_client.max_retries == 0
    assert anthropic_client.max_retries == 0


def test_provider_extras_on_tool_calls_go_back_unchanged():
    """Gemini's thought signature, an unknown field on a tool call, is kept and sent back."""
    signature = {"extra_content": {"google": {"thought_signature": "c2ln"}}}
    call = SimpleNamespace(
        id="c1",
        function=SimpleNamespace(name="lookup", arguments="{}"),
        model_extra=signature,
    )
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=None, tool_calls=[call]))],
        usage=None,
    )

    [parsed] = openai_llm(FakeCreate(response)).chat(CONVERSATION[1:2]).tool_calls
    turn = {"role": "assistant", "content": "", "tool_calls": [asdict(parsed)]}

    assert parsed.extra == signature
    assert (
        to_openai_messages([turn])[0]["tool_calls"][0]["extra_content"]
        == signature["extra_content"]
    )
