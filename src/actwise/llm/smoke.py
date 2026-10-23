"""Send one prompt through each LLM provider, then through the cached chain: `make llm-smoke`.

Prints each provider's model, latency, tokens and answer, so a missing key, a retired
model or a spent quota shows up here rather than halfway through an eval run.
"""

from __future__ import annotations

import io
import os
import sys
import time

from dotenv import load_dotenv

from actwise.llm.factory import PROVIDERS, SERVING, build_llm, build_provider

PROMPT = "In one sentence: which article of the EU AI Act lists the prohibited AI practices?"
MESSAGES = [{"role": "user", "content": PROMPT}]


def main() -> None:
    """Ask every provider in turn (a failure is printed, not raised), then the whole chain."""
    if isinstance(sys.stdout, io.TextIOWrapper):  # a Windows console can't print every character
        sys.stdout.reconfigure(errors="replace")
    load_dotenv()  # .env fills in what the environment doesn't set
    print(f"prompt: {PROMPT}")
    for name in PROVIDERS:
        llm = build_provider(name, os.environ, SERVING)
        if llm is None:
            print(f"\n{name}: skipped, no key or model in .env")
            continue
        start = time.perf_counter()
        try:
            answer = llm.chat(MESSAGES, temperature=0, max_tokens=256)
        except Exception as exc:  # show the error and go on with the next provider
            print(f"\n{name}: failed after {(time.perf_counter() - start) * 1000:.0f} ms: {exc!r}")
            continue
        print(
            f"\n{name} ({answer.model}): {(time.perf_counter() - start) * 1000:.0f} ms, "
            f"{answer.input_tokens} tokens in, {answer.output_tokens} out\n  {answer.text.strip()}"
        )

    chain = build_llm(os.environ, SERVING)
    answer = chain.chat(MESSAGES, temperature=0, max_tokens=256)
    order = " -> ".join(provider["model"] for provider in chain.config["fallback"])
    source = "the disk cache" if chain.hits else "a provider call"
    print(f"\nchain {order}: answered by {answer.model}, from {source}")


if __name__ == "__main__":
    main()
