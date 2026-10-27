"""Build the provider chain from environment variables; LLM_PROVIDER_ORDER is the fallback order."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from actwise.llm.anthropic_adapter import AnthropicLLM
from actwise.llm.base import LLM
from actwise.llm.openai_compat import OpenAICompatLLM
from actwise.llm.wrappers import MAX_RETRY_AFTER, CachedLLM, FallbackLLM, RetryingLLM

log = logging.getLogger(__name__)

CACHE_DIR = Path(".cache/llm")
DEFAULT_ORDER = "gemini,groq,ollama"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROQ_URL = "https://api.groq.com/openai/v1"
OLLAMA_URL = "http://localhost:11434/v1"


@dataclass(frozen=True)
class Provider:
    """Where a provider's settings live in the environment, and how to reach it."""

    key_var: str | None  # API key; None for a local server that needs none
    model_var: str
    base_url: str | None  # OpenAI-compatible endpoint; None means the Anthropic SDK
    min_interval: float  # seconds between calls offline, to stay under the free tier's rate


PROVIDERS = {
    "gemini": Provider("GEMINI_API_KEY", "GEMINI_MODEL", GEMINI_URL, 4.0),  # 15 requests/minute
    "groq": Provider("GROQ_API_KEY", "GROQ_MODEL", GROQ_URL, 2.0),  # 30 requests/minute
    "ollama": Provider(None, "OLLAMA_MODEL", OLLAMA_URL, 0.0),
    "anthropic": Provider("ANTHROPIC_API_KEY", "ANTHROPIC_MODEL", None, 0.0),
}


@dataclass(frozen=True)
class Profile:
    """How patient the chain is (R5): evals wait out rate limits, serving fails over fast."""

    max_tries: int  # calls per provider on 408, 429, 5xx and 529
    base_delay: float  # seconds before the first retry, doubled after each one
    throttle: bool  # space each provider's calls by its `min_interval`
    timeout: float  # seconds for one HTTP call
    budget: float | None  # seconds for one chat(), retries and fallbacks included
    fallback: bool  # move on to the next provider; evals don't, so one run is one model
    max_wait: float  # the longest Retry-After worth sleeping through; above it, skip the provider


OFFLINE = Profile(
    4, 2.0, throttle=True, timeout=60.0, budget=None, fallback=False, max_wait=MAX_RETRY_AFTER
)
SERVING = Profile(2, 1.0, throttle=False, timeout=15.0, budget=25.0, fallback=True, max_wait=5.0)


def build_provider(name: str, env: Mapping[str, str], profile: Profile) -> RetryingLLM | None:
    """One provider behind retries, or None when its key or model is missing or empty (R14)."""
    spec = PROVIDERS[name]
    model = env.get(spec.model_var, "")
    key = env.get(spec.key_var, "") if spec.key_var else "ollama"  # Ollama ignores the key
    if not (model and key):
        log.info("LLM provider %s skipped: no key or model", name)
        return None
    adapter: LLM
    if spec.base_url is None:
        adapter = AnthropicLLM(model, key, profile.timeout)
    else:
        adapter = OpenAICompatLLM(model, key, spec.base_url, name, profile.timeout)
    interval = spec.min_interval if profile.throttle else 0.0
    return RetryingLLM(adapter, profile.max_tries, profile.base_delay, interval, profile.max_wait)


def build_llm(env: Mapping[str, str], profile: Profile) -> CachedLLM:
    """The configured providers of LLM_PROVIDER_ORDER, in that order, behind one disk cache.

    `profile` has no default: each caller says whether it serves users or runs evals.
    """
    order = env.get("LLM_PROVIDER_ORDER") or DEFAULT_ORDER  # empty means unset, as for keys
    names = [name.strip() for name in order.split(",") if name.strip()]
    if unknown := [name for name in names if name not in PROVIDERS]:
        raise ValueError(f"unknown LLM provider in LLM_PROVIDER_ORDER: {', '.join(unknown)}")
    providers = [p for name in names if (p := build_provider(name, env, profile)) is not None]
    if not providers:
        raise RuntimeError("no LLM provider configured: set a key and a model in .env")
    if not profile.fallback:  # a spent quota stops the run; a re-run resumes from the cache
        providers = providers[:1]
    return CachedLLM(FallbackLLM(providers, profile.budget), CACHE_DIR)


def build_judge(env: Mapping[str, str]) -> CachedLLM:
    """The judge: JUDGE_MODEL on JUDGE_PROVIDER (with that provider's key), offline profile."""
    name, model = env.get("JUDGE_PROVIDER") or "gemini", env.get("JUDGE_MODEL", "")
    if name not in PROVIDERS:
        raise ValueError(f"unknown JUDGE_PROVIDER: {name}")
    judge = build_provider(name, {**env, PROVIDERS[name].model_var: model}, OFFLINE)
    if judge is None:
        raise RuntimeError(f"no judge: set JUDGE_MODEL and the {name} key in .env")
    return CachedLLM(FallbackLLM([judge]), CACHE_DIR)
