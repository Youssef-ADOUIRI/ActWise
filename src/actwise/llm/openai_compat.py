"""OpenAI SDK adapter for the OpenAI-compatible endpoints of Gemini, Groq and Ollama."""

from __future__ import annotations

import json
from typing import Any

from actwise.llm.base import MAX_TOKENS, LLMResponse, Message, Tool, ToolCall, time_left


def to_openai_messages(messages: list[Message], provider: str) -> list[dict[str, Any]]:
    """Provider-neutral messages in the Chat Completions format, as `provider` expects them.

    Tool arguments become JSON strings; a tool call carries back only the extra fields that
    this provider attached to it (a fallback chain must not send Gemini's signature to Groq).
    """
    out: list[dict[str, Any]] = []
    for m in messages:
        if m["role"] == "assistant" and m.get("tool_calls"):
            calls = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": json.dumps(tc["arguments"])},
                    **tc.get("extra", {}).get(provider, {}),  # Gemini: the thought signature
                }
                for tc in m["tool_calls"]
            ]
            out.append(
                {"role": "assistant", "content": m.get("content") or None, "tool_calls": calls}
            )
        elif m["role"] == "tool":
            out.append({"role": "tool", "tool_call_id": m["tool_call_id"], "content": m["content"]})
        else:
            out.append({"role": m["role"], "content": m["content"]})
    return out


class OpenAICompatLLM:
    """Chat Completions through the OpenAI SDK, sent to `base_url`."""

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str,
        provider: str,
        timeout: float,
        client: Any = None,
    ):
        """Use `client` if given (tests pass a fake), else an SDK client that never retries."""
        if client is None:
            from openai import OpenAI  # imported here so tests can run with a fake

            # max_retries=0: RetryingLLM is the only retry layer (R13)
            client = OpenAI(api_key=api_key, base_url=base_url, max_retries=0)
        self.client, self.model, self.timeout = client, model, timeout
        self.config = {"provider": provider, "model": model}

    def chat(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        temperature: float | None = None,
        max_tokens: int = MAX_TOKENS,
        deadline: float | None = None,
    ) -> LLMResponse:
        """Send one request; tool-call arguments come back parsed from their JSON strings."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": to_openai_messages(messages, self.config["provider"]),
            "max_tokens": max_tokens,  # R12: the guide's adapter never sent it
            "timeout": time_left(deadline, self.timeout),
        }
        if temperature is not None:
            kwargs["temperature"] = temperature
        if tools:
            kwargs["tools"] = [{"type": "function", "function": t} for t in tools]
            kwargs["tool_choice"] = "auto"
        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        calls = [
            ToolCall(
                tc.id,
                tc.function.name,
                json.loads(tc.function.arguments or "{}"),
                {self.config["provider"]: extra}
                if (extra := getattr(tc, "model_extra", None))
                else {},
            )
            for tc in message.tool_calls or []
        ]
        usage = getattr(response, "usage", None)
        return LLMResponse(
            text=message.content or "",
            tool_calls=calls,
            input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
            output_tokens=getattr(usage, "completion_tokens", 0) or 0,
            model=self.model,
        )
