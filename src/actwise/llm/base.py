"""One small interface for every LLM provider.

Provider-neutral messages are plain dicts:

    {"role": "system" | "user", "content": str}
    {"role": "assistant", "content": str, "tool_calls": [{"id", "name", "arguments", "extra"}]}
    {"role": "tool", "tool_call_id": str, "content": str}

Tools are {"name": str, "description": str, "parameters": <JSON schema>}. A tool call's
`extra` holds provider data that must go back unchanged on the next turn, keyed by
provider, such as the thought signature Gemini 3 attaches to every function call.

`deadline` is a `time.monotonic()` value by which a call must return: retries,
fallbacks and HTTP timeouts all fit inside it, so one call can't outlive its time
budget (review item R5). A failed call raises the SDK's error; an error with an
HTTP `status_code` (both SDKs set one on API errors) may be worth retrying.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Protocol

Message = dict[str, Any]
Tool = dict[str, Any]
MAX_TOKENS = 1024  # the default answer length, the same at every layer of the chain


@dataclass(frozen=True)
class ToolCall:
    """A tool the model asks to call, with its arguments already parsed."""

    id: str
    name: str
    arguments: dict[str, Any]
    extra: dict[str, Any] = field(default_factory=dict)  # provider data, sent back as received


@dataclass(frozen=True)
class LLMResponse:
    """What a model returned: text, tool calls or both, and the tokens it cost."""

    text: str
    tool_calls: list[ToolCall]
    input_tokens: int
    output_tokens: int
    model: str  # the model that answered: behind a fallback chain, not always the first


class LLM(Protocol):
    config: dict[str, Any]  # what decides the answers (provider, model), never an API key

    def chat(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        temperature: float | None = None,
        max_tokens: int = MAX_TOKENS,
        deadline: float | None = None,
    ) -> LLMResponse:
        """One reply to `messages`, returned before `deadline` if one is set."""
        ...


def time_left(deadline: float | None, timeout: float) -> float:
    """Seconds one HTTP call may take: `timeout`, or less when the deadline is nearer."""
    if deadline is None:
        return timeout
    return max(min(timeout, deadline - time.monotonic()), 0.1)  # never 0 or negative
