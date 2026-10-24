"""Answer a question from retrieved passages; citations are checked before anyone sees them."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from actwise.generation.citations import extract_citations, invented_citations, strip_citations
from actwise.generation.guardrails import looks_like_injection, redact_pii
from actwise.ids import human_label, paragraph_id
from actwise.llm.base import LLM, LLMResponse, Message
from actwise.retrieval.passages import Hit

log = logging.getLogger(__name__)

CONTEXT_PASSAGES = 5  # the generator reads the top 5 passages (decision 004)
REFUSAL = {
    "en": "I can't answer this from the text of the AI Act or the GDPR that I have. "
    "Please rephrase the question, or ask a lawyer.",
    "fr": "Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont "
    "je dispose. Reformulez la question, ou consultez un juriste.",
}

Search = Callable[[str, int], list[Hit]]  # (question, top_k) -> passages, best first


@dataclass(frozen=True)
class AskResult:
    """What the user gets, plus what the evaluation needs to score it."""

    answer: str  # the checked answer, or the refusal message
    reason: str  # why it was refused ("injection", "not_covered", "uncited"); "" if answered
    citations: list[str]  # the ids cited in `answer`, all of them retrieved
    invented: list[str]  # ids the model cited without retrieving them, removed from `answer`
    sources: list[dict[str, str]]  # each retrieved passage: key, id (as cited), label, text
    reply: LLMResponse | None  # the model's raw reply; None if the model was not asked

    @property
    def refused(self) -> bool:
        """True when the user gets the refusal message instead of an answer."""
        return bool(self.reason)


def sources_of(hits: Sequence[Hit], lang: str) -> list[dict[str, str]]:
    """Each passage as the model, the judge and the user see it."""
    return [
        {"key": h.key, "id": paragraph_id(h.id), "label": human_label(h.id, lang), "text": h.text}
        for h in hits
    ]


def format_sources(sources: list[dict[str, str]]) -> str:
    """Each source under its id: exactly what the answering model and the judge read."""
    return "\n\n".join(f"[{s['id']}]\n{s['text']}" for s in sources)


def build_messages(prompt: str, question: str, sources: list[dict[str, str]]) -> list[Message]:
    """The system prompt, then the sources and the question."""
    return [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": f"Sources:\n\n{format_sources(sources)}\n\nQuestion: {question}",
        },
    ]


def is_refusal(reply: str) -> bool:
    """True for NOT_COVERED however it is dressed: `NOT_COVERED.`, `**NOT_COVERED**` (R3)."""
    return re.sub(r"[^A-Z]+", " ", reply.upper()).split()[:2] == ["NOT", "COVERED"]


def refusal(lang: str) -> str:
    """The refusal message in the user's language (English if there is none)."""
    return REFUSAL.get(lang, REFUSAL["en"])


class RagPipeline:
    """Retrieve, answer with a versioned prompt, and keep only the citations that were retrieved."""

    def __init__(self, llm: LLM, search: Search, prompt: str):
        """`prompt` is the system prompt text, such as `load_prompt("answer.v1")`."""
        self.llm, self.search, self.prompt = llm, search, prompt

    def ask(self, question: str, lang: str) -> AskResult:
        """Answer in `lang`, or refuse; an answer left with no valid citation is refused too."""
        if looks_like_injection(question):
            return AskResult(refusal(lang), "injection", [], [], [], None)
        sources = sources_of(self.search(question, CONTEXT_PASSAGES), lang)
        reply = self.llm.chat(build_messages(self.prompt, question, sources), temperature=0)
        if is_refusal(reply.text):
            return AskResult(refusal(lang), "not_covered", [], [], sources, reply)
        retrieved = {s["id"] for s in sources}
        invented = invented_citations(reply.text, retrieved)
        if invented:
            log.warning("removed invented citations %s (%r)", invented, redact_pii(question))
        answer = strip_citations(reply.text, set(invented)).strip()
        citations = extract_citations(answer)  # read back from the text the user will see
        if not citations or not retrieved.issuperset(citations):  # fail closed
            return AskResult(refusal(lang), "uncited", [], invented, sources, reply)
        return AskResult(answer, "", citations, invented, sources, reply)
