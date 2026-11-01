import json

import pytest

from actwise.agent.classifier import (
    BUDGET_NUDGE,
    NUDGE,
    READ_TOOL,
    SHOWN,
    SUBMIT_TOOL,
    ClassificationError,
    ai_act_articles,
    classify,
    search_ai_act,
)
from actwise.llm.base import LLMResponse, ToolCall
from actwise.retrieval.passages import Passage, to_hit
from tests.unit.toys import ScriptedLLM

HITS = [
    to_hit(
        Passage("AIA-Art5-1#2", "en", "AI Act Article 5(1)\nThe following AI practices..."), 1.0
    ),
    to_hit(Passage("GDPR-Art22-1", "en", "GDPR Article 22(1)\nThe data subject shall..."), 0.9),
    to_hit(Passage("AIA-Art50-1", "en", "AI Act Article 50(1)\nProviders shall ensure..."), 0.8),
]
SEARCH = ("search_ai_act", {"query": "social scoring"})


def search(query, top_k):
    """Fake retriever: the same three passages, best first."""
    return HITS[:top_k]


articles = ai_act_articles(HITS)


def reply(*calls, text=""):
    """A model reply that makes these (name, arguments) tool calls."""
    tool_calls = [ToolCall(f"call{i}", name, args) for i, (name, args) in enumerate(calls)]
    return LLMResponse(text, tool_calls, 10, 5, "m")


def submit(**fields):
    """A submit_classification call; `fields` override a valid prohibited result."""
    valid = {
        "tier": "prohibited",
        "reasons": ["Social scoring is banned."],
        "citations": ["AIA-Art5-1"],
        "confidence": 0.9,
    }
    return ("submit_classification", valid | fields)


def tool_messages(llm, call):
    """The tool results the model had seen when it made call number `call` (0-based)."""
    return [m["content"] for m in llm.calls[call]["messages"] if m["role"] == "tool"]


def test_happy_path():
    """Search then submit: the result is returned, and the search reached the model."""
    llm = ScriptedLLM(reply(SEARCH), reply(submit()))
    description = "A city scores residents' trustworthiness."

    outcome = classify(llm, search, articles, description, deadline=42.0)

    assert outcome.result.tier == "prohibited"
    assert (outcome.steps, outcome.lookups) == (2, 1)
    assert [call["deadline"] for call in llm.calls] == [42.0, 42.0]  # one per request (R5)
    [found] = tool_messages(llm, 1)
    assert found.startswith("[AIA-Art5-1]\n") and "[AIA-Art50-1]" in found
    assert "GDPR" not in found


def test_rejects_invented_citation():
    """Citing an id never retrieved is refused with a message; the corrected call is accepted."""
    llm = ScriptedLLM(reply(SEARCH), reply(submit(citations=["AIA-Art5-3"])), reply(submit()))

    outcome = classify(llm, search, articles, "A city scores residents' trustworthiness.")

    assert outcome.result.citations == ["AIA-Art5-1"]
    assert "Unknown: ['AIA-Art5-3']" in tool_messages(llm, 2)[-1]


def test_schema_errors_fed_back():
    """A bad tier, empty reasons and confidence 3 go back to the model; the budget then raises."""
    llm = ScriptedLLM(reply(SEARCH), reply(submit(tier="banned", reasons=[], confidence=3)))

    with pytest.raises(ClassificationError):
        classify(llm, search, articles, "Something.", max_steps=3)

    error = tool_messages(llm, 2)[-1]
    assert error.startswith("Invalid classification")
    assert all(field in error for field in ("tier", "reasons", "confidence"))


def test_plain_text_is_nudged():
    """A reply without a tool call is answered with the nudge to submit."""
    llm = ScriptedLLM(
        LLMResponse("It is prohibited.", [], 10, 5, "m"), reply(SEARCH), reply(submit())
    )

    classify(llm, search, articles, "A city scores residents' trustworthiness.")

    assert llm.calls[1]["messages"][-1] == {"role": "user", "content": NUDGE}


def test_schema_has_no_titles():
    """The submit tool's schema has no `title` key, which some providers reject."""
    schema = json.dumps(SUBMIT_TOOL["parameters"])

    assert '"title"' not in schema
    assert '"enum": ["prohibited", "high_risk"' in schema


def test_tier_must_cite_its_own_rule():
    """High risk citing only Art. 5 is refused; transparency citing Art. 50 is accepted."""
    llm = ScriptedLLM(
        reply(SEARCH),
        reply(submit(tier="high_risk")),
        reply(submit(tier="transparency_only", citations=["AIA-Art50-1"])),
    )

    outcome = classify(llm, search, articles, "A chatbot on a shop website.")

    assert outcome.result.tier == "transparency_only"
    assert "must cite AIA-Art6 or AIA-AnnexI or AIA-AnnexIII" in tool_messages(llm, 2)[-1]


def test_needs_more_info_must_ask_questions():
    """needs_more_info without follow-up questions is refused; with them it is accepted."""
    vague = submit(tier="needs_more_info", reasons=["The purpose is unknown."])
    llm = ScriptedLLM(
        reply(SEARCH), reply(vague), reply(submit(**vague[1], follow_up_questions=["What for?"]))
    )

    outcome = classify(llm, search, articles, "An AI model for a client.")

    assert outcome.result.follow_up_questions == ["What for?"]
    assert "follow-up questions" in tool_messages(llm, 2)[-1]


def test_unknown_tool_gets_an_error():
    """A call to a tool that doesn't exist is answered with an error, and the run goes on."""
    llm = ScriptedLLM(reply(("delete_everything", {})), reply(SEARCH), reply(submit()))

    classify(llm, search, articles, "A city scores residents' trustworthiness.")

    assert tool_messages(llm, 1) == ["Unknown tool 'delete_everything'."]


def test_search_tool_keeps_the_ai_act_and_clamps_top_k():
    """Only AI Act passages come back, one per paragraph; top_k is held to 1–8."""
    asked = []

    def recording_search(query, top_k):
        """Record the requested top_k, then return the passages and a second part of Art. 5(1)."""
        asked.append(top_k)
        return [*HITS, to_hit(Passage("AIA-Art5-1#3", "en", "...part three"), 0.5)]

    found = search_ai_act(recording_search, "q", 50)
    search_ai_act(recording_search, "q", "not a number")

    assert [p["id"] for p in found] == ["AIA-Art5-1", "AIA-Art50-1"]
    assert asked == [16, 10]  # twice top_k (8 at most, 5 by default) before filtering


def test_read_tool_shows_paragraphs_that_count_as_retrieved():
    """Reading AIA-Art5 shows its paragraph by id; citing it then needs no search."""
    llm = ScriptedLLM(reply(("read_ai_act_article", {"article": "AIA-Art5"})), reply(submit()))

    outcome = classify(llm, search, articles, "A city scores residents' trustworthiness.")

    [shown] = tool_messages(llm, 1)
    assert shown.startswith("[AIA-Art5-1]\nAI Act Article 5(1)")
    assert outcome.lookups == 1


def test_a_passage_already_shown_is_not_sent_again():
    """The same search twice: the second result points back instead of repeating the text."""
    llm = ScriptedLLM(reply(SEARCH), reply(SEARCH), reply(submit()))

    classify(llm, search, articles, "A city scores residents' trustworthiness.")

    first, second = tool_messages(llm, 2)
    assert "The following AI practices" in first
    assert second == f"[AIA-Art5-1]\n{SHOWN}\n\n[AIA-Art50-1]\n{SHOWN}"


def test_the_read_tool_offers_the_tier_articles():
    """The read tool's article argument is an enum of the articles a tier must cite."""
    enum = READ_TOOL["parameters"]["properties"]["article"]["enum"]

    assert enum == ["AIA-AnnexI", "AIA-AnnexIII", "AIA-Art5", "AIA-Art50", "AIA-Art6"]


def test_reading_an_unknown_article_says_so():
    """An id that matches no article gets a hint, not an empty list."""
    llm = ScriptedLLM(
        reply(("read_ai_act_article", {"article": "Article 5"})), reply(SEARCH), reply(submit())
    )

    classify(llm, search, articles, "A city scores residents' trustworthiness.")

    assert tool_messages(llm, 1)[0].startswith("Nothing found")


def test_an_agent_that_keeps_searching_is_told_to_conclude():
    """Three steps before the budget runs out, the agent is told to submit with what it has."""
    llm = ScriptedLLM(reply(SEARCH))  # searches forever

    with pytest.raises(ClassificationError):
        classify(llm, search, articles, "Something.", max_steps=5)

    assert llm.calls[2]["messages"][-1] == {"role": "user", "content": BUDGET_NUDGE}
    assert all(BUDGET_NUDGE not in str(m) for m in llm.calls[1]["messages"])
