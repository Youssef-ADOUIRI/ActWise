"""The risk classifier as a LangGraph workflow that walks the rules in order (step 10).

    uv run --extra local --extra frameworks python evals/run_classifier.py --agent langgraph

`retrieve_for_rule` reads the articles of one rule by id, `decide` asks the model whether
that rule applies (yes, no or unclear), and `submit` builds the agent's `Classification`
and runs the agent's guards (`agent.classifier.accept`). Art. 5 comes first, then Art. 6
with Annexes I and III, then Art. 50. The first rule that applies decides the tier, an
unclear one asks for the missing facts, and when none applies the system is minimal risk.
The nodes call our own LLM chain, so the model, the cache and the retries are the agent's.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.runtime import Runtime
from pydantic import BaseModel, Field, ValidationError

from actwise.agent.classifier import (
    MAX_STEPS,
    Articles,
    ClassificationError,
    ClassifyOutcome,
    accept,
    uncited,
)
from actwise.agent.schemas import TIER_ARTICLES, Classification, tool_schema
from actwise.generation.prompts import load_prompt
from actwise.generation.rag import Search, format_sources
from actwise.llm.base import LLM, Message

CLASSIFY_PROMPT = "classify_rule.v1"  # the agent's name for it, so one harness loads both
RULES = list(TIER_ARTICLES.items())  # (tier, the articles that decide it), in checking order
NUDGE = "Call decide_rule now."
SYSTEM = load_prompt(CLASSIFY_PROMPT)


class RuleDecision(BaseModel):
    """Whether one rule of the AI Act applies to the described AI system."""

    applies: Literal["yes", "no", "unclear"]
    reasons: list[str] = Field(min_length=1, description="Short reasons")
    citations: list[str] = Field(min_length=1, description="Ids from the rule text you were given")
    confidence: float = Field(ge=0, le=1)
    follow_up_questions: list[str] = Field(
        default_factory=list, description="The facts to ask for when the answer is unclear"
    )


DECIDE_TOOL = {
    "name": "decide_rule",
    "description": "Decide whether the rule applies to the AI system.",
    "parameters": tool_schema(RuleDecision),
}


@dataclass(frozen=True)
class Deps:
    """What the nodes use besides the state: the agent's model and articles, and the limits."""

    llm: LLM
    articles: Articles
    max_steps: int
    deadline: float | None


class State(TypedDict, total=False):
    description: str
    rule: int  # index into RULES
    messages: list[Message]  # the conversation about the current rule
    retrieved: set[str]  # every paragraph id read so far: what may be cited
    decisions: list[RuleDecision]  # one per rule checked; the last may still be refused
    steps: int  # model calls
    result: Classification


def tool_replies(asked: Message, content: str) -> list[Message]:
    """The same answer to every tool call of the model's message, as the providers require."""
    calls = asked["tool_calls"]
    return [{"role": "tool", "tool_call_id": c["id"], "content": content} for c in calls]


def retrieve_for_rule(state: State, runtime: Runtime[Deps]) -> State:
    """Move to the next rule: read its articles and start a conversation about it."""
    rule = state.get("rule", -1) + 1
    found = [p for article in RULES[rule][1] for p in runtime.context.articles.get(article, [])]
    prompt = (
        f"AI system description:\n{state['description']}\n\n"
        f"Check rule {rule + 1}.\n\n{format_sources(found)}"
    )
    return {
        "rule": rule,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        "retrieved": state.get("retrieved", set()) | {p["id"] for p in found},
    }


def check(arguments: dict[str, object], retrieved: set[str]) -> RuleDecision | str:
    """The decision if it is valid and cites only what was read, else what to tell the model."""
    try:
        decision = RuleDecision.model_validate(arguments)
    except ValidationError as exc:
        return f"Invalid decision: {exc.errors(include_url=False)}"
    return uncited(decision.citations, retrieved) or decision


def decide(state: State, runtime: Runtime[Deps]) -> State:
    """One model call about the current rule; a bad reply goes back to the model."""
    deps = runtime.context
    steps = state.get("steps", 0)
    if steps >= deps.max_steps:
        raise ClassificationError(f"no valid classification within {deps.max_steps} steps")
    reply = deps.llm.chat(
        state["messages"], tools=[DECIDE_TOOL], temperature=0, deadline=deps.deadline
    )
    if not reply.tool_calls:
        told: list[Message] = [
            {"role": "assistant", "content": reply.text},
            {"role": "user", "content": NUDGE},
        ]
        return {"steps": steps + 1, "messages": state["messages"] + told}
    calls = [asdict(call) for call in reply.tool_calls]
    asked: Message = {"role": "assistant", "content": reply.text, "tool_calls": calls}
    messages = state["messages"] + [asked]
    verdict = check(reply.tool_calls[0].arguments, state["retrieved"])
    if isinstance(verdict, str):
        return {"steps": steps + 1, "messages": messages + tool_replies(asked, verdict)}
    decisions = state.get("decisions", []) + [verdict]
    return {"steps": steps + 1, "messages": messages, "decisions": decisions}


def after_decide(state: State) -> str:
    """Ask again, check the next rule, or submit: the first rule that applies decides."""
    decisions = state.get("decisions", [])
    if len(decisions) <= state["rule"]:  # no decision on the current rule yet
        return "decide"
    if decisions[-1].applies == "no" and state["rule"] + 1 < len(RULES):
        return "retrieve_for_rule"
    return "submit"


def submit(state: State) -> State:
    """Build the classification from every rule checked, and run the agent's guards."""
    decisions = state["decisions"]
    decision = decisions[-1]
    tier = {"yes": RULES[state["rule"]][0], "unclear": "needs_more_info", "no": "minimal_risk"}
    arguments = {
        "tier": tier[decision.applies],
        "reasons": [reason for d in decisions for reason in d.reasons],
        "citations": list(dict.fromkeys(c for d in decisions for c in d.citations)),
        "confidence": decision.confidence,
        "follow_up_questions": decision.follow_up_questions,
    }
    verdict = accept(arguments, state["retrieved"])
    if isinstance(verdict, Classification):
        return {"result": verdict}
    messages = state["messages"]
    return {"decisions": decisions[:-1], "messages": messages + tool_replies(messages[-1], verdict)}


def compile_graph() -> CompiledStateGraph[State, Deps, State, State]:
    """START → retrieve_for_rule → decide → (decide | retrieve_for_rule | submit) → END."""
    graph = StateGraph(State, context_schema=Deps)
    graph.add_node("retrieve_for_rule", retrieve_for_rule)
    graph.add_node("decide", decide)
    graph.add_node("submit", submit)
    graph.add_edge(START, "retrieve_for_rule")
    graph.add_edge("retrieve_for_rule", "decide")
    graph.add_conditional_edges("decide", after_decide, ["decide", "retrieve_for_rule", "submit"])
    graph.add_conditional_edges("submit", lambda s: END if "result" in s else "decide")
    return graph.compile()


GRAPH = compile_graph()


def classify(
    llm: LLM,
    search: Search,
    articles: Articles,
    description: str,
    max_steps: int = MAX_STEPS,
    deadline: float | None = None,
) -> ClassifyOutcome:
    """Walk the rules until one applies; the agent's signature, so one harness runs both.

    `search` goes unused: each rule is read whole, by id, as the agent's reader does.
    """
    state = GRAPH.invoke(
        {"description": description},
        context=Deps(llm, articles, max_steps, deadline),
        config={"recursion_limit": 4 * max_steps},
    )
    lookups = sum(len(articles) for _, articles in RULES[: state["rule"] + 1])  # articles read
    return ClassifyOutcome(state["result"], state["steps"], lookups)
