"""Disk cache, retries with backoff, and provider fallback, around any `LLM`.

Together they make free tiers usable: the cache turns a re-run eval into zero
API calls, retries ride out 429s, and the fallback chain keeps the demo up.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from collections.abc import Callable, Sequence
from dataclasses import asdict
from pathlib import Path

from actwise.llm.base import LLM, MAX_TOKENS, LLMResponse, Message, Tool, ToolCall

log = logging.getLogger(__name__)

# 408 request timeout, 429 rate limit, 5xx server errors, 529 Anthropic overloaded
RETRYABLE = {408, 429, 500, 502, 503, 504, 529}


class CachedLLM:
    """Answers kept on disk, keyed by everything that decides them (R4)."""

    def __init__(self, inner: LLM, cache_dir: Path):
        """Store `inner`'s answers as JSON files in `cache_dir`, created on the first write."""
        self.inner, self.dir, self.config = inner, cache_dir, inner.config
        self.hits = self.misses = 0

    def chat(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        temperature: float | None = None,
        max_tokens: int = MAX_TOKENS,
        deadline: float | None = None,
    ) -> LLMResponse:
        """The stored answer if there is one; otherwise ask `inner` and store its answer.

        The key holds the model ids of the whole chain, so another model never gets
        this one's answers.
        """
        request = [self.config, messages, tools, temperature, max_tokens]
        key = hashlib.sha256(json.dumps(request, sort_keys=True).encode("utf-8")).hexdigest()
        path = self.dir / f"{key}.json"
        if path.exists():
            self.hits += 1
            stored = json.loads(path.read_text(encoding="utf-8"))
            calls = [ToolCall(**call) for call in stored["tool_calls"]]
            return LLMResponse(**{**stored, "tool_calls": calls})
        self.misses += 1
        response = self.inner.chat(messages, tools, temperature, max_tokens, deadline=deadline)
        self.dir.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f"{key}.{uuid.uuid4().hex}.tmp")  # unique per writer
        tmp.write_text(json.dumps(asdict(response), ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)  # atomic: a killed run never leaves half an entry
        return response


class RetryingLLM:
    """Retry rate limits and server errors with exponential backoff, and space calls out."""

    def __init__(
        self,
        inner: LLM,
        max_tries: int,
        base_delay: float,
        min_interval: float = 0.0,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ):
        """`min_interval` keeps calls under a rate limit; `sleep` and `clock` are for tests."""
        self.inner, self.config = inner, inner.config
        self.max_tries, self.base_delay, self.min_interval = max_tries, base_delay, min_interval
        self.sleep, self.clock = sleep, clock
        self._last = float("-inf")  # start of the previous call: the first call never waits

    def chat(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        temperature: float | None = None,
        max_tokens: int = MAX_TOKENS,
        deadline: float | None = None,
    ) -> LLMResponse:
        """Ask `inner`; retry a RETRYABLE status while tries remain and the wait fits the deadline.

        Before each try, wait for the backoff or the rate-limit interval, whichever is longer.
        """
        error: Exception | None = None
        for attempt in range(self.max_tries):
            backoff = self.base_delay * 2 ** (attempt - 1) if attempt else 0.0
            wait = max(backoff, self.min_interval - (self.clock() - self._last))
            if deadline is not None and self.clock() + wait >= deadline:
                break
            if wait > 0:
                self.sleep(wait)
            self._last = self.clock()
            try:
                return self.inner.chat(messages, tools, temperature, max_tokens, deadline=deadline)
            except Exception as exc:  # SDK error classes differ, but both carry `status_code`
                if getattr(exc, "status_code", None) not in RETRYABLE:
                    raise
                error = exc
        raise error or TimeoutError("the deadline passed before the first try")


class FallbackLLM:
    """Ask each provider in turn until one answers, within an optional time budget (R5)."""

    def __init__(
        self,
        providers: Sequence[LLM],
        budget: float | None = None,
        clock: Callable[[], float] = time.monotonic,
    ):
        """`budget` (seconds) sets the deadline of each call whose caller gave none."""
        self.providers, self.budget, self.clock = providers, budget, clock
        self.config = {"fallback": [provider.config for provider in providers]}

    def chat(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        temperature: float | None = None,
        max_tokens: int = MAX_TOKENS,
        deadline: float | None = None,
    ) -> LLMResponse:
        """The first answer. Each failure is logged (R15); no provider starts after the deadline."""
        if deadline is None and self.budget is not None:
            deadline = self.clock() + self.budget
        last: Exception | None = None
        for provider in self.providers:
            if deadline is not None and self.clock() >= deadline:
                raise RuntimeError("no LLM provider answered before the deadline") from last
            try:
                return provider.chat(messages, tools, temperature, max_tokens, deadline=deadline)
            except Exception as exc:  # any failure moves on to the next provider
                name = f"{provider.config['provider']}/{provider.config['model']}"
                log.warning("LLM %s failed, trying the next provider: %r", name, exc)
                last = exc
        raise RuntimeError("no LLM provider answered") from last
