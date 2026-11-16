# 012: Tracing with LangSmith, not Langfuse

- **Options:**
  - **Langfuse Cloud, Hobby plan** (the guide's choice): 50,000 units a month, 30 days retention. `@observe`, plus a drop-in OpenAI client.
  - **LangSmith, Developer plan:** 5,000 base traces a month, 14 days retention, 1 seat, no card ([pricing](https://www.langchain.com/pricing)). The `langsmith` SDK offers `@traceable` and the client wrappers `wrap_openai` and `wrap_anthropic`, and needs no LangChain code.
- **Measured:** nothing yet. Step 12 builds the tracing and checks a trace.
- **Chosen:** LangSmith, for step 12:
  - `observability/tracing.py`: `@traceable` on `ask` and `classify`, and a no-op when the package is absent or tracing is off;
  - `wrap_openai` in `OpenAICompatLLM` (Gemini, Groq, Ollama) and `wrap_anthropic` in `AnthropicLLM`;
  - `/classify` sends no inputs (`process_inputs`), and `redact_pii` runs on whatever is sent.
- **Why:**
  - **It covers what Langfuse would have:** a trace of retrieval and of each model call, through the same two adapters.
  - **Step 10's LangGraph classifier** reports to LangSmith with no extra code.
  - **What it costs:**
    - **The free quota is a tenth of Langfuse's.** Tracing stays off unless `LANGSMITH_TRACING=true`. Evals, tests and step 14's load test never send traces. The deployed API samples traces if it gets close to the quota.
    - **Traces last 14 days, not 30,** so the screenshot for `docs/` must be taken soon after the trace is recorded.
    - **An EU account** needs `LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com`.
- **Revisit if:**
  - the deployed API nears 5,000 traces a month;
  - LangSmith's free plan changes.
