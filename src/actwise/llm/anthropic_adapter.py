"""Anthropic SDK adapter, with the same `chat()` as `OpenAICompatLLM`."""

from __future__ import annotations

from typing import Any

from actwise.llm.base import MAX_TOKENS, LLMResponse, Message, Tool, ToolCall, time_left


def to_anthropic_messages(messages: list[Message]) -> list[dict[str, Any]]:
    """Provider-neutral messages, system ones excluded, in the Messages API format.

    Tool calls become `tool_use` blocks, and consecutive tool results are merged into
    ONE user message of `tool_result` blocks, as the API expects.
    """
    out: list[dict[str, Any]] = []
    for m in messages:
        if m["role"] == "assistant":
            blocks: list[dict[str, Any]] = []
            if m.get("content"):
                blocks.append({"type": "text", "text": m["content"]})
            for tc in m.get("tool_calls", []):
                blocks.append(
                    {
                        "type": "tool_use",
                        "id": tc["id"],
                        "name": tc["name"],
                        "input": tc["arguments"],
                    }
                )
            out.append({"role": "assistant", "content": blocks or m["content"]})
        elif m["role"] == "tool":
            block = {
                "type": "tool_result",
                "tool_use_id": m["tool_call_id"],
                "content": m["content"],
            }
            # only tool results make a user turn whose content is a list
            if out and out[-1]["role"] == "user" and isinstance(out[-1]["content"], list):
                out[-1]["content"].append(block)
            else:
                out.append({"role": "user", "content": [block]})
        else:
            out.append({"role": "user", "content": m["content"]})
    return out


class AnthropicLLM:
    """The Messages API through the Anthropic SDK."""

    def __init__(self, model: str, api_key: str, timeout: float, client: Any = None):
        """Use `client` if given (tests pass a fake), else an SDK client that never retries."""
        if client is None:
            import anthropic  # imported here so tests can run with a fake

            client = anthropic.Anthropic(api_key=api_key, max_retries=0)  # R13
        self.client, self.model, self.timeout = client, model, timeout
        self.config = {"provider": "anthropic", "model": model}

    def chat(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        temperature: float | None = None,
        max_tokens: int = MAX_TOKENS,
        deadline: float | None = None,
    ) -> LLMResponse:
        """Send one request. `temperature` is ignored: the Messages API has none any more (R11)."""
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": to_anthropic_messages([m for m in messages if m["role"] != "system"]),
            "timeout": time_left(deadline, self.timeout),
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "input_schema": t["parameters"],
                }
                for t in tools
            ]
        response = self.client.messages.create(**kwargs)
        text = "".join(block.text for block in response.content if block.type == "text")
        calls = [
            ToolCall(block.id, block.name, dict(block.input))
            for block in response.content
            if block.type == "tool_use"
        ]
        return LLMResponse(
            text=text,
            tool_calls=calls,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            model=self.model,
        )
