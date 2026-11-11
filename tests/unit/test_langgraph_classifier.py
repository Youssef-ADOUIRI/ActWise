import pytest

pytest.importorskip("langgraph")

from actwise.agent.classifier import ClassificationError, ai_act_articles  # noqa: E402
from actwise.llm.base import LLMResponse, ToolCall  # noqa: E402
from actwise.retrieval.passages import Passage  # noqa: E402
from frameworks.langgraph_classifier import DECIDE_TOOL, NUDGE, classify  # noqa: E402
from tests.unit.toys import ScriptedLLM  # noqa: E402

ARTICLES = ai_act_articles(
    [
        Passage("AIA-Art5-1", "en", "AI Act Article 5(1)\nThe following AI practices..."),
        Passage("AIA-Art6-2", "en", "AI Act Article 6(2)\nAI systems referred to in Annex III..."),
        Passage("AIA-AnnexIII-4", "en", "AI Act Annex III(4)\nEmployment, workers' management..."),
        Passage("AIA-Art50-1", "en", "AI Act Article 50(1)\nProviders shall ensure..."),
    ]
)
CV_TOOL = "A tool that ranks job applicants' CVs."


def search(query, top_k):
    """The graph reads each rule by id and never searches."""
    raise AssertionError("unexpected search")


def decide(applies, citations, **fields):
    """A model reply that calls decide_rule once."""
    arguments = {"applies": applies, "reasons": [f"{applies}."], "citations": citations}
    arguments |= {"confidence": 0.8} | fields
    return LLMResponse("", [ToolCall("call0", DECIDE_TOOL["name"], arguments)], 10, 5, "m")


def prompt(llm, call):
    """The user message of model call number `call` (0-based): the description and one rule."""
    return next(m["content"] for m in llm.calls[call]["messages"] if m["role"] == "user")


def test_the_rules_are_walked_in_order():
    """Art. 5 doesn't apply, Art. 6 does: high risk after two calls, each seeing its rule only."""
    llm = ScriptedLLM(decide("no", ["AIA-Art5-1"]), decide("yes", ["AIA-Art6-2", "AIA-AnnexIII-4"]))

    outcome = classify(llm, search, ARTICLES, CV_TOOL, deadline=42.0)

    assert outcome.result.tier == "high_risk"
    assert outcome.result.citations == ["AIA-Art5-1", "AIA-Art6-2", "AIA-AnnexIII-4"]
    assert outcome.result.reasons == ["no.", "yes."]  # one per rule checked
    assert (outcome.steps, outcome.lookups) == (2, 4)  # Art. 5, then Art. 6, Annex I, Annex III
    assert "AIA-Art5-1" in prompt(llm, 0) and "AIA-Art6-2" not in prompt(llm, 0)
    assert "AIA-AnnexIII-4" in prompt(llm, 1) and "AIA-Art5-1" not in prompt(llm, 1)
    assert [call["deadline"] for call in llm.calls] == [42.0, 42.0]


def test_a_missing_fact_asks_for_it():
    """An unclear rule stops the walk with needs_more_info and its follow-up questions."""
    question = "Does it score people's social behaviour?"
    llm = ScriptedLLM(decide("unclear", ["AIA-Art5-1"], follow_up_questions=[question]))

    outcome = classify(llm, search, ARTICLES, "A city app that rates residents.")

    assert outcome.result.tier == "needs_more_info"
    assert outcome.result.follow_up_questions == [question]
    assert outcome.steps == 1


def test_no_rule_applies():
    """Three rules that don't apply give minimal risk, citing the rules checked."""
    llm = ScriptedLLM(
        decide("no", ["AIA-Art5-1"]), decide("no", ["AIA-Art6-2"]), decide("no", ["AIA-Art50-1"])
    )

    outcome = classify(llm, search, ARTICLES, "A spam filter.")

    assert outcome.result.tier == "minimal_risk"
    assert outcome.result.citations == ["AIA-Art5-1", "AIA-Art6-2", "AIA-Art50-1"]
    assert outcome.steps == 3


def told(llm, call):
    """What the model had been told when it made call number `call`: prompts and tool results."""
    return [m["content"] for m in llm.calls[call]["messages"] if m["role"] in ("user", "tool")]


def test_errors_go_back_to_the_model():
    """Plain text gets a nudge; an id it never read and a tier without its rule are refused."""
    llm = ScriptedLLM(
        LLMResponse("I think it is high risk.", [], 10, 5, "m"),
        decide("no", ["AIA-Art99-1"]),
        decide("no", ["AIA-Art5-1"]),
        decide("yes", ["AIA-Art5-1"]),  # Art. 6 applies, but only Art. 5 is cited
        decide("yes", ["AIA-Art6-2"]),
    )

    outcome = classify(llm, search, ARTICLES, CV_TOOL)

    assert outcome.result.tier == "high_risk"
    assert outcome.steps == 5
    assert NUDGE in told(llm, 1)
    assert any("AIA-Art99-1" in text for text in told(llm, 2))
    assert any("must cite AIA-Art6" in text for text in told(llm, 4))


def test_the_step_budget_ends_the_run():
    """A model that never decides fails after `max_steps` calls, like the agent."""
    llm = ScriptedLLM(LLMResponse("Let me think.", [], 10, 5, "m"))

    with pytest.raises(ClassificationError):
        classify(llm, search, ARTICLES, "Anything.", max_steps=3)

    assert len(llm.calls) == 3
