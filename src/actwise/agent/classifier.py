"""A tool-calling agent that classifies an AI system into an AI Act risk tier.

The agent reads the articles that decide a tier (by id) and searches the AI Act for
the rest, then submits a classification. A run ends only on a valid, grounded result:
the schema holds, every citation was read or retrieved, and the tier cites its own
rule (Art. 5, Art. 6 / Annex I / Annex III, or Art. 50).
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from pydantic import ValidationError

from actwise.agent.schemas import TIER_ARTICLES, Classification, tool_schema
from actwise.generation.prompts import load_prompt
from actwise.generation.rag import Search, format_sources
from actwise.ids import article_id, paragraph_id
from actwise.llm.base import LLM, Message
from actwise.retrieval.passages import Passage

CLASSIFY_PROMPT = "classify.v1"
MAX_STEPS = 8  # model calls per run
BUDGET_STEPS = 3  # left when the agent is told to conclude: room to fix a refused submission
NUDGE = "Call submit_classification now."
BUDGET_NUDGE = f"{BUDGET_STEPS} steps left: submit your classification now, with the ids you have."
NOTHING_FOUND = "Nothing found."
SHOWN = "(shown above)"
DEFAULT_TOP_K, MAX_TOP_K = 5, 8
RULE_ARTICLES = sorted({a for articles in TIER_ARTICLES.values() for a in articles})
READ_TOOL = {
    "name": "read_ai_act_article",
    "description": "Read every paragraph of one AI Act article or annex that decides a tier.",
    "parameters": {
        "type": "object",
        "properties": {"article": {"type": "string", "enum": RULE_ARTICLES}},
        "required": ["article"],
    },
}
SEARCH_TOOL = {
    "name": "search_ai_act",
    "description": "Search the EU AI Act. Returns passages with the ids to cite.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "top_k": {
                "type": "integer",
                "description": f"1 to {MAX_TOP_K}, default {DEFAULT_TOP_K}",
            },
        },
        "required": ["query"],
    },
}
SUBMIT_TOOL = {
    "name": "submit_classification",
    "description": "Submit the final classification, once the deciding rules have been read.",
    "parameters": tool_schema(Classification),
}
TOOLS = [READ_TOOL, SEARCH_TOOL, SUBMIT_TOOL]

Articles = Mapping[str, list[dict[str, str]]]  # article id -> its paragraphs as {id, text}


class ClassificationError(RuntimeError):
    """No valid classification within the step budget."""


@dataclass(frozen=True)
class ClassifyOutcome:
    """The accepted classification, and what it took to get there."""

    result: Classification
    steps: int  # model calls
    lookups: int  # articles read and searches made


def ai_act_articles(passages: Sequence[Passage]) -> dict[str, list[dict[str, str]]]:
    """English AI Act paragraphs grouped by article: what `read_ai_act_article` returns."""
    articles: dict[str, list[dict[str, str]]] = defaultdict(list)
    for p in passages:
        if p.lang == "en" and p.id.startswith("AIA-"):
            articles[article_id(p.id)].append({"id": paragraph_id(p.id), "text": p.text})
    return dict(articles)


def search_ai_act(search: Search, query: str, top_k: object) -> list[dict[str, str]]:
    """AI Act passages only, one per paragraph: classifying a system is an AI Act question."""
    try:
        k = max(1, min(int(str(top_k)), MAX_TOP_K))
    except ValueError:
        k = DEFAULT_TOP_K
    found: dict[str, str] = {}
    for hit in search(query, 2 * k):
        if hit.id.startswith("AIA-"):
            found.setdefault(paragraph_id(hit.id), hit.text)
    return [{"id": pid, "text": text} for pid, text in list(found.items())[:k]]


def accept(arguments: dict[str, Any], retrieved: set[str]) -> Classification | str:
    """The classification if it is valid and grounded, else what to tell the model."""
    try:
        result = Classification.model_validate(arguments)
    except ValidationError as exc:
        return f"Invalid classification: {exc.errors(include_url=False)}"
    if unknown := [c for c in result.citations if paragraph_id(c) not in retrieved]:
        return f"Cite only ids that you read or searched. Unknown: {unknown}"
    needed = TIER_ARTICLES.get(result.tier)
    if needed and not any(article_id(c) in needed for c in result.citations):
        return f"A {result.tier} classification must cite {' or '.join(needed)}."
    if result.tier == "needs_more_info" and not result.follow_up_questions:
        return "needs_more_info must list the follow-up questions to ask."
    return result


def classify(
    llm: LLM, search: Search, articles: Articles, description: str, max_steps: int = MAX_STEPS
) -> ClassifyOutcome:
    """Run the agent until it submits an acceptable classification; errors go back to it."""
    lookup = {
        READ_TOOL["name"]: lambda args: articles.get(str(args.get("article", "")).strip(), []),
        SEARCH_TOOL["name"]: lambda args: search_ai_act(
            search, str(args.get("query", "")), args.get("top_k")
        ),
    }
    messages: list[Message] = [
        {"role": "system", "content": load_prompt(CLASSIFY_PROMPT)},
        {"role": "user", "content": f"AI system description:\n{description}"},
    ]
    retrieved: set[str] = set()
    lookups = 0
    for step in range(1, max_steps + 1):
        reply = llm.chat(messages, tools=TOOLS, temperature=0)
        if not reply.tool_calls:
            messages += [
                {"role": "assistant", "content": reply.text},
                {"role": "user", "content": NUDGE},
            ]
            continue
        calls = [asdict(call) for call in reply.tool_calls]
        messages.append({"role": "assistant", "content": reply.text, "tool_calls": calls})
        for call in reply.tool_calls:
            if call.name in lookup:
                found = lookup[call.name](call.arguments)
                lookups += 1
                shown = [p | {"text": SHOWN} if p["id"] in retrieved else p for p in found]
                retrieved.update(p["id"] for p in found)
                content = format_sources(shown) if found else NOTHING_FOUND
            elif call.name == SUBMIT_TOOL["name"]:
                verdict = accept(call.arguments, retrieved)
                if isinstance(verdict, Classification):
                    return ClassifyOutcome(verdict, step, lookups)
                content = verdict
            else:
                content = f"Unknown tool {call.name!r}."
            messages.append({"role": "tool", "tool_call_id": call.id, "content": content})
        if max_steps - step == BUDGET_STEPS:  # an agent that keeps researching has to conclude
            messages.append({"role": "user", "content": BUDGET_NUDGE})
    raise ClassificationError(f"no valid classification within {max_steps} steps")
