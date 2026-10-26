import json

import pytest

from actwise.llm.factory import OFFLINE, SERVING, build_judge, build_llm

ENV = {
    "GEMINI_API_KEY": "gemini-secret",
    "GEMINI_MODEL": "gemini-2.5-flash-lite",
    "GROQ_API_KEY": "groq-secret",
    "GROQ_MODEL": "openai/gpt-oss-20b",
    "OLLAMA_MODEL": "qwen3:4b",
}


def models(llm):
    """The model of each provider in the chain, in fallback order."""
    return [provider["model"] for provider in llm.config["fallback"]]


def test_factory_builds_the_default_order():
    """Without LLM_PROVIDER_ORDER, the chain is Gemini, then Groq, then Ollama."""
    assert models(build_llm(ENV, SERVING)) == [
        "gemini-2.5-flash-lite",
        "openai/gpt-oss-20b",
        "qwen3:4b",
    ]


def test_factory_skips_unconfigured():
    """A missing or empty key or model skips its provider (R14); with none left, it raises."""
    env = {name: value for name, value in ENV.items() if name != "GROQ_MODEL"}
    env["GEMINI_API_KEY"] = ""  # what a copied .env.example holds

    assert models(build_llm(env, OFFLINE)) == ["qwen3:4b"]
    with pytest.raises(RuntimeError, match="no LLM provider configured"):
        build_llm(env | {"OLLAMA_MODEL": ""}, OFFLINE)


def test_unknown_provider_fails_loudly():
    """A typo in LLM_PROVIDER_ORDER is an error, not a silently skipped provider (R14)."""
    with pytest.raises(ValueError, match="gemnii"):
        build_llm(ENV | {"LLM_PROVIDER_ORDER": "gemnii,groq"}, OFFLINE)


def test_serving_profile_fails_over_fast():
    """Serving: 2 tries, no throttle, a budget, fallback; offline: throttled, one provider (R5)."""
    serving, offline = build_llm(ENV, SERVING).inner, build_llm(ENV, OFFLINE).inner

    assert serving.budget == SERVING.budget
    assert [(p.max_tries, p.min_interval) for p in serving.providers] == [(2, 0.0)] * 3
    assert offline.budget is None
    assert [p.min_interval for p in offline.providers] == [4.0]  # an eval run is one model


def test_config_never_holds_a_key():
    """Configs go into cache keys and reports, so they name models but never an API key."""
    env = ENV | {
        "LLM_PROVIDER_ORDER": "anthropic,gemini,groq",
        "ANTHROPIC_API_KEY": "anthropic-secret",
        "ANTHROPIC_MODEL": "claude-x",
    }

    config = json.dumps(build_llm(env, SERVING).config)

    assert "secret" not in config
    assert models(build_llm(env, SERVING)) == [
        "claude-x",
        "gemini-2.5-flash-lite",
        "openai/gpt-oss-20b",
    ]


def test_build_judge():
    """The judge runs JUDGE_MODEL with its provider's key; without a model it raises."""
    judge = build_judge(ENV | {"JUDGE_PROVIDER": "gemini", "JUDGE_MODEL": "gemini-3.6-flash"})

    assert models(judge) == ["gemini-3.6-flash"]
    with pytest.raises(RuntimeError, match="JUDGE_MODEL"):
        build_judge(ENV)
    with pytest.raises(ValueError, match="JUDGE_PROVIDER"):
        build_judge(ENV | {"JUDGE_PROVIDER": "openai", "JUDGE_MODEL": "x"})
