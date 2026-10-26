"""A tool-calling agent that classifies an AI system into an AI Act risk tier.

The agent reads the articles that decide a tier (by id) and searches the AI Act for
the rest, then submits a classification. A run ends only on a valid, grounded result:
the schema holds, every citation was read or retrieved, and the tier cites its own
rule (Art. 5, Art. 6 / Annex I / Annex III, or Art. 50).
"""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass

from pydantic import ValidationError

from actwise.agent.schemas import TIER_ARTICLES, Classification, tool_schema
from actwise.generation.prompts import load_prompt
from actwise.generation.rag import Search
from actwise.ids import article_id, paragraph_id
from actwise.llm.base import LLM, Message
from actwise.retrieval.passages import Passage

CLASSIFY_PROMPT = "classify.v1"
NUDGE = "Call submit_classification now."
BUDGET_NUDGE = "Two steps left: submit your classification now, with the ids you have."
DEFAULT_TOP_K, MAX_TOP_K = 5, 8
READ_TOOL = {
    "name": "read_ai_act_article",
    "description": "Read every paragraph of one AI Act article or annex, with the ids to cite.",
    "parameters": {
        "type": "object",
        "properties": {
            "article": {
                "type": "string",
                "description": "An id: AIA-Art5, AIA-Art6, AIA-Art50, AIA-AnnexI, AIA-AnnexIII",
            }
        },
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
            "top_k": {"type": "integer", "description": f"1 to {MAX_TOP_K}, default 5"},
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

Read = Callable[[str], list[dict[str, str]]]  # article id -> its paragraphs as {id, text}


class ClassificationError(RuntimeError):
    """No valid classification within the step budget."""


@dataclass(frozen=True)
class ClassifyOutcome:
    """The accepted classification, and what it took to get there."""

    result: Classification
    steps: int  # model calls
    lookups: int  # articles read and searches made
    retrieved: frozenset[str]  # every paragraph id the agent was shown


def article_reader(passages: Sequence[Passage]) -> Read:
    """`read_ai_act_article` over these passages: English AI Act text, paragraph parts joined."""
    by_article: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for p in passages:
        if p.lang == "en" and p.id.startswith("AIA-"):
            by_article[article_id(p.id)][paragraph_id(p.id)].append(p.text)

    def read(article: str) -> list[dict[str, str]]:
        """Every paragraph of the article, or nothing for an unknown id."""
        paragraphs = by_article.get(article.strip(), {})
        return [{"id": pid, "text": "\n".join(parts)} for pid, parts in paragraphs.items()]

    return read


def search_ai_act(search: Search, query: str, top_k: object) -> list[dict[str, str]]:
    """AI Act passages only, as {id, text}: classifying a system is an AI Act question."""
    try:
        k = max(1, min(int(str(top_k)), MAX_TOP_K))
    except ValueError:
        k = DEFAULT_TOP_K
    hits = [h for h in search(query, 2 * k) if h.id.startswith("AIA-")][:k]
    return [{"id": paragraph_id(h.id), "text": h.text} for h in hits]


def check(result: Classification, retrieved: set[str]) -> str | None:
    """Why a valid classification can't be accepted yet, or None if it can."""
    if unknown := [c for c in result.citations if paragraph_id(c) not in retrieved]:
        return f"Cite only ids that you read or searched. Unknown: {unknown}"
    needed = TIER_ARTICLES.get(result.tier)
    if needed and not any(article_id(paragraph_id(c)) in needed for c in result.citations):
        return f"A {result.tier} classification must cite {' or '.join(needed)}."
    if result.tier == "needs_more_info" and not result.follow_up_questions:
        return "needs_more_info must list the follow-up questions to ask."
    return None


def classify(
    llm: LLM, search: Search, read: Read, description: str, max_steps: int = 8
) -> ClassifyOutcome:
    """Run the agent until it submits an acceptable classification; errors go back to it."""
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
            args = call.arguments
            if call.name in (READ_TOOL["name"], SEARCH_TOOL["name"]):
                if call.name == READ_TOOL["name"]:
                    found = read(str(args.get("article", "")))
                else:
                    found = search_ai_act(search, str(args.get("query", "")), args.get("top_k"))
                retrieved.update(passage["id"] for passage in found)
                lookups += 1
                content = (
                    json.dumps(found, ensure_ascii=False)
                    if found
                    else ("Nothing found. Article ids look like AIA-Art6 or AIA-AnnexIII.")
                )
            elif call.name == SUBMIT_TOOL["name"]:
                try:
                    result = Classification.model_validate(args)
                except ValidationError as exc:
                    content = f"Invalid classification: {exc.errors(include_url=False)}"
                else:
                    problem = check(result, retrieved)
                    if problem is None:
                        return ClassifyOutcome(result, step, lookups, frozenset(retrieved))
                    content = problem
            else:
                content = f"Unknown tool {call.name!r}."
            messages.append({"role": "tool", "tool_call_id": call.id, "content": content})
        if max_steps - step == 2:  # an agent that keeps researching has to conclude
            messages.append({"role": "user", "content": BUDGET_NUDGE})
    raise ClassificationError(f"no valid classification within {max_steps} steps")
