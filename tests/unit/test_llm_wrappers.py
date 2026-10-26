import logging

import anthropic
import httpx
import openai
import pytest

from actwise.llm.base import LLMResponse, ToolCall
from actwise.llm.wrappers import CachedLLM, FallbackLLM, RetryingLLM
from tests.unit.toys import ScriptedLLM

MESSAGES = [{"role": "user", "content": "Which AI practices are banned?"}]
ANSWER = LLMResponse("Article 5.", [ToolCall("c1", "lookup", {"id": "AIA-Art5"})], 12, 3, "m")
REQUEST = httpx.Request("POST", "https://llm.invalid/v1/chat/completions")


def sdk_error(error_class, status, retry_after=None):
    """A real SDK error carrying an HTTP status (and a Retry-After), as a provider raises it."""
    headers = {"retry-after": retry_after} if retry_after else {}
    response = httpx.Response(status, headers=headers, request=REQUEST)
    return error_class("provider error", response=response, body=None)


class FakeClock:
    """Monotonic time that only moves when the code sleeps or a test moves it."""

    def __init__(self):
        """Start at t = 0, with no sleep recorded."""
        self.now = 0.0
        self.sleeps = []

    def __call__(self):
        """The current time."""
        return self.now

    def sleep(self, seconds):
        """Record the sleep and move time forward."""
        self.sleeps.append(seconds)
        self.now += seconds


class SlowFailure:
    """A provider that uses up `seconds` of the fake clock, then times out."""

    config = {"provider": "fake", "model": "slow"}

    def __init__(self, clock, seconds):
        """Fail after `seconds` on `clock`."""
        self.clock, self.seconds = clock, seconds

    def chat(self, messages, tools=None, temperature=None, max_tokens=1024, deadline=None):
        """Take the time, then fail like an HTTP timeout."""
        self.clock.now += self.seconds
        raise TimeoutError("too slow")


def test_cache_hits_skip_provider(tmp_path):
    """A repeated request, even from a new process, is answered from disk without a call."""
    inner = ScriptedLLM(ANSWER)
    llm = CachedLLM(inner, tmp_path)

    first, second = llm.chat(MESSAGES, max_tokens=100), llm.chat(MESSAGES, max_tokens=100)
    fresh = ScriptedLLM(ANSWER)
    third = CachedLLM(fresh, tmp_path).chat(MESSAGES, max_tokens=100)

    assert first == second == third == ANSWER
    assert len(inner.calls) == 1 and fresh.calls == []
    assert (llm.hits, llm.misses) == (1, 1)


def test_cache_key_includes_models_and_max_tokens(tmp_path):
    """Another model or another max_tokens never gets a stored answer (R4)."""
    CachedLLM(ScriptedLLM(ANSWER, model="a"), tmp_path).chat(MESSAGES, max_tokens=100)
    other_model = ScriptedLLM(ANSWER, model="b")
    other_max_tokens = ScriptedLLM(ANSWER, model="a")

    CachedLLM(other_model, tmp_path).chat(MESSAGES, max_tokens=100)
    CachedLLM(other_max_tokens, tmp_path).chat(MESSAGES, max_tokens=200)

    assert len(other_model.calls) == 1
    assert len(other_max_tokens.calls) == 1


def test_failures_are_not_cached(tmp_path):
    """A failed call stores nothing, so the next identical request asks the provider again."""
    inner = ScriptedLLM(sdk_error(openai.RateLimitError, 429), ANSWER)
    llm = CachedLLM(inner, tmp_path)

    with pytest.raises(openai.RateLimitError):
        llm.chat(MESSAGES)

    assert llm.chat(MESSAGES) == ANSWER
    assert len(inner.calls) == 2


def test_retry_backoff():
    """A 429 then a 529 are retried after 1 s, then 2 s (R10: base_delay=1, fake sleep)."""
    clock = FakeClock()
    inner = ScriptedLLM(
        sdk_error(openai.RateLimitError, 429), sdk_error(anthropic.OverloadedError, 529), ANSWER
    )
    llm = RetryingLLM(inner, max_tries=4, base_delay=1, sleep=clock.sleep, clock=clock)

    assert llm.chat(MESSAGES) == ANSWER
    assert clock.sleeps == [1, 2]


@pytest.mark.parametrize(
    "error", [ValueError("a bug"), openai.APITimeoutError(request=REQUEST)], ids=["bug", "timeout"]
)
def test_retry_skips_errors_that_waiting_cannot_fix(error):
    """A bug is raised at once, and a timeout goes straight to the next provider: no retry."""
    clock = FakeClock()
    inner = ScriptedLLM(error, ANSWER)

    with pytest.raises(type(error)):
        RetryingLLM(inner, max_tries=4, base_delay=1, sleep=clock.sleep, clock=clock).chat(MESSAGES)

    assert len(inner.calls) == 1 and clock.sleeps == []


def test_retry_waits_for_a_short_retry_after():
    """A 429 asking for 7 s is retried after 7 s, not after the 1 s backoff."""
    clock = FakeClock()
    inner = ScriptedLLM(sdk_error(openai.RateLimitError, 429, retry_after="7"), ANSWER)

    llm = RetryingLLM(inner, max_tries=4, base_delay=1, sleep=clock.sleep, clock=clock)

    assert llm.chat(MESSAGES) == ANSWER
    assert clock.sleeps == [7.0]


def test_a_long_retry_after_means_a_spent_quota():
    """A 429 asking for an hour raises at once: no more tries, no sleep."""
    clock = FakeClock()
    inner = ScriptedLLM(sdk_error(openai.RateLimitError, 429, retry_after="3600"), ANSWER)

    with pytest.raises(openai.RateLimitError):
        RetryingLLM(inner, max_tries=4, base_delay=1, sleep=clock.sleep, clock=clock).chat(MESSAGES)

    assert len(inner.calls) == 1 and clock.sleeps == []


def test_gemini_retry_delay_in_the_body_counts_as_retry_after():
    """Gemini says how long to wait in the error body; a spent daily quota raises at once."""
    clock = FakeClock()
    body = "Error code: 429 - [{'error': {'details': [{'retryDelay': '17389s'}]}}]"
    response = httpx.Response(429, request=REQUEST)
    inner = ScriptedLLM(openai.RateLimitError(body, response=response, body=None), ANSWER)

    with pytest.raises(openai.RateLimitError):
        RetryingLLM(inner, max_tries=4, base_delay=1, sleep=clock.sleep, clock=clock).chat(MESSAGES)

    assert len(inner.calls) == 1 and clock.sleeps == []


def test_retry_gives_up_after_max_tries():
    """When every try gets a 429, the last error is raised after `max_tries` calls."""
    clock = FakeClock()
    inner = ScriptedLLM(sdk_error(openai.RateLimitError, 429))

    with pytest.raises(openai.RateLimitError):
        RetryingLLM(inner, max_tries=2, base_delay=1, sleep=clock.sleep, clock=clock).chat(MESSAGES)

    assert len(inner.calls) == 2 and clock.sleeps == [1]


def test_retry_never_sleeps_past_the_deadline():
    """A retry that could only start after the deadline is not attempted (R5)."""
    clock = FakeClock()
    inner = ScriptedLLM(sdk_error(openai.RateLimitError, 429), ANSWER)
    llm = RetryingLLM(inner, max_tries=4, base_delay=2, sleep=clock.sleep, clock=clock)

    with pytest.raises(openai.RateLimitError):
        llm.chat(MESSAGES, deadline=1.5)

    assert len(inner.calls) == 1 and clock.sleeps == []
    assert inner.calls[0]["deadline"] == 1.5


def test_min_interval_spaces_calls():
    """With a 4 s interval, the first call goes at once and a call 1 s later waits 3 s."""
    clock = FakeClock()
    llm = RetryingLLM(ScriptedLLM(ANSWER), 1, 1.0, min_interval=4.0, sleep=clock.sleep, clock=clock)

    llm.chat(MESSAGES)
    clock.now += 1.0
    llm.chat(MESSAGES)

    assert clock.sleeps == [3.0]


def test_fallback_chain(caplog):
    """The first provider fails, the second answers, and the failover is logged (R15)."""
    first = ScriptedLLM(sdk_error(openai.RateLimitError, 429), model="first-model")
    second = ScriptedLLM(ANSWER, model="second-model")

    with caplog.at_level(logging.WARNING):
        answer = FallbackLLM([first, second]).chat(MESSAGES)

    assert answer == ANSWER
    assert "first-model" in caplog.text


def test_fallback_raises_one_clear_error_when_all_fail():
    """When every provider fails, one error says so and keeps the last cause."""
    providers = [ScriptedLLM(ValueError("down 1")), ScriptedLLM(ValueError("down 2"))]

    with pytest.raises(RuntimeError, match="no LLM provider answered") as info:
        FallbackLLM(providers).chat(MESSAGES)

    assert str(info.value.__cause__) == "down 2"


def test_fallback_starts_no_provider_after_the_deadline():
    """When the first provider uses up the 25 s budget, the second is not tried (R5)."""
    clock = FakeClock()
    second = ScriptedLLM(ANSWER)
    llm = FallbackLLM([SlowFailure(clock, 30), second], budget=25, clock=clock)

    with pytest.raises(RuntimeError, match="deadline"):
        llm.chat(MESSAGES)

    assert second.calls == []


def test_fallback_passes_the_deadline_down():
    """The budget sets the deadline of each provider call; a caller's own deadline wins."""
    clock = FakeClock()
    clock.now = 100.0
    inner = ScriptedLLM(ANSWER)
    llm = FallbackLLM([inner], budget=25, clock=clock)

    llm.chat(MESSAGES)
    llm.chat(MESSAGES, deadline=110.0)

    assert [call["deadline"] for call in inner.calls] == [125.0, 110.0]
