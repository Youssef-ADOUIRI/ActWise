"""Toys shared by the tests: passages, a bag-of-words embedder and a scripted LLM."""

import numpy as np

from actwise.retrieval.embedders import l2_normalize
from actwise.retrieval.passages import Passage

VOCAB = ["erasure", "ban", "risk", "fine"]


class ScriptedLLM:
    """Fake LLM: returns or raises its script in order (the last item repeats); records calls."""

    def __init__(self, *script, model="scripted"):
        """`script` holds `LLMResponse`s and exceptions."""
        self.script = list(script)
        self.config = {"provider": "fake", "model": model}
        self.calls = []

    def chat(self, messages, tools=None, temperature=None, max_tokens=1024, deadline=None):
        """Record the request, then answer with the next item of the script."""
        self.calls.append(
            {
                "messages": list(messages),  # a copy: an agent keeps appending to its list
                "tools": tools,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "deadline": deadline,
            }
        )
        item = self.script[min(len(self.calls), len(self.script)) - 1]
        if isinstance(item, Exception):
            raise item
        return item


class CountingEmbedder:
    """Bag-of-words over a tiny vocabulary; counts how many texts it embedded."""

    config = {"model": "counting", "vocab": VOCAB}

    def __init__(self):
        """Start with no text embedded."""
        self.calls = 0

    def encode(self, texts, kind="passage"):
        """Count each vocabulary word in each text (+0.01, so no row is all zeros)."""
        self.calls += len(texts)
        counts = [[t.lower().count(word) + 0.01 for word in VOCAB] for t in texts]
        return l2_normalize(np.array(counts, dtype=np.float32))


PASSAGES = [
    Passage("GDPR-Art17-1", "en", "Right to erasure: erasure of personal data"),
    Passage("AIA-Art5-1", "en", "The ban on prohibited practices"),
    Passage("AIA-Art9-1", "en", "Risk management system for high risk systems"),
    Passage("GDPR-Art83-5", "en", "Administrative fine up to 4 %"),
    Passage("AIA-Art5-1", "fr", "Interdiction : ban des pratiques"),
]
