# ActWise Roadmap

> A citation-grounded assistant for the **EU AI Act** and **GDPR**. It answers in EN/FR with article-level citations, classifies AI systems into AI Act risk tiers, plugs into Slack, MCP and Google Sheets, and runs on Google Cloud Run at **EUR 0**.

- **Duration:** 10 weeks × ~12 h, about 120 h in total
- **Day-to-day checklist:** [`TODO.md`](../TODO.md)
- **Design decisions:** `docs/decisions/`, one five-line note for each choice (the options, what was measured, what was chosen)

---

## Product features

| #   | Feature                  | What the user gets                                                                                                                                           | Milestone |
| --- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| F1  | **Cited Q&A**            | Ask about the AI Act or GDPR in EN or FR. The answer cites each rule as `AI Act, Art. 6(2)`, and a citation is never invented                                | M3        |
| F2  | **Honest refusal**       | `NOT_COVERED` turns into a polite refusal in the user's language. It gives no legal verdicts                                                                 | M3        |
| F3  | **Risk-tier classifier** | Describe an AI system and get back `prohibited / high_risk / transparency_only / minimal_risk / needs_more_info`, with cited reasons and follow-up questions | M4        |
| F4  | **Document upload**      | Upload a PDF, DOCX or TXT system description, and it is classified                                                                                           | M4        |
| F5  | **REST API + UI**        | `/health`, `/search`, `/ask`, `/classify`, `/upload` and a Streamlit chat UI                                                                                 | M4        |
| F6  | **Slack command**        | `/actwise ask …` and `/actwise classify …`                                                                                                                   | M6        |
| F7  | **MCP server**           | `ask_ai_act` and `classify_ai_system` tools for any MCP client                                                                                               | M6        |
| F8  | **AI system register**   | Each classification adds a row to Google Sheets. Only a hash is stored, never the raw text                                                                   | M6        |

## Platform capabilities (the LLMOps side)

| #   | Capability                                                                                      | Milestone |
| --- | ----------------------------------------------------------------------------------------------- | --------- |
| P1  | Structure-aware ingestion with stable, language-free chunk IDs                                  | M0        |
| P2  | Evaluation harness: article-level splits, golden set, Recall@k, MRR, nDCG                       | M1        |
| P3  | Hybrid retrieval (dense + BM25 + RRF), optional cross-encoder rerank, ablation table            | M2        |
| P4  | LLM gateway: OpenAI SDK + Anthropic SDK adapters, disk cache, retries, fallback chain           | M3        |
| P5  | Versioned prompts, A/B on dev, LLM judge calibrated with Cohen's kappa                          | M3        |
| P6  | Embedder fine-tune (MiniLM) followed by int8 ONNX, served without PyTorch                       | M5        |
| P7  | Framework comparison: LlamaIndex and LangGraph against hand-written code                        | M5        |
| P8  | Observability: Langfuse traces, JSON logs, cost per query                                       | M6        |
| P9  | Cloud Run + Secret Manager + keyless GitHub Actions deploy with a candidate-revision smoke test | M7        |
| P10 | Hardening: OWASP-mapped safety suite, load test, failure drills, model card                     | M8        |

---

## Milestones

| Milestone                                                                       | Weeks | Guide steps | Status         |
| ------------------------------------------------------------------------------- | ----- | ----------- | -------------- |
| [M0 Foundation and corpus](#m0-foundation-and-corpus)                           | 1     | 0, 1, 2     | ⬜ Not started |
| [M1 Measured baseline](#m1-measured-baseline)                                   | 2     | 3           | ⬜             |
| [M2 Retrieval quality](#m2-retrieval-quality)                                   | 3–4   | 4           | ⬜             |
| [M3 Grounded generation](#m3-grounded-generation)                               | 3–4   | 5, 6        | ⬜             |
| [M4 Classifier agent and API](#m4-classifier-agent-and-api)                     | 5     | 7, 8        | ⬜             |
| [M5 Own model and framework comparison](#m5-own-model-and-framework-comparison) | 6     | 9, 10       | ⬜             |
| [M6 Integrations and observability](#m6-integrations-and-observability)         | 7     | 11, 12      | ⬜             |
| [M7 Production on Cloud Run](#m7-production-on-cloud-run)                       | 8     | 13          | ⬜             |
| [M8 Hardening](#m8-hardening)                                                   | 9     | 14          | ⬜             |
| [M9 Showcase](#m9-showcase)                                                     | 10    | 15          | ⬜             |

Status key: ⬜ not started · 🟨 in progress · ✅ done (exit criteria met and committed)

### M0 Foundation and corpus

**Delivers:** a repo with green CI, four saved EUR-Lex pages, and `data/processed/chunks.jsonl`.
**Exit criteria**

- `make test` passes locally and the CI badge is green
- Parsed counts match the official ones: AI Act 113 articles, 13 annexes, 180 recitals; GDPR 99 articles, 173 recitals
- Every EN chunk ID has a FR twin; roughly 3–4k chunks in total

### M1 Measured baseline

**Delivers:** `splits.json` split by article, 50 hand-written golden questions (15 or more in FR), a naive dense baseline, and `evals/reports/baseline.json`.
**Exit criteria:** `make eval-retrieval` prints Recall@5, MRR@10 and nDCG@10, and the baseline report is committed.

### M2 Retrieval quality

**Delivers:** Qdrant + BM25 + RRF + an optional reranker, `docs/ablations.md` (baseline → A–D, with ms/query), and `docs/failure_cases.md`.
**Exit criteria:** **Recall@5 ≥ 0.85** on dev, or the gap is explained in `failure_cases.md`.

### M3 Grounded generation

**Delivers:** one `chat()` interface over Gemini, Groq, Ollama and Anthropic; cache, retry and fallback; a cited RAG pipeline; guardrails; prompts v1/v2; a calibrated judge; the golden set grown to 150.
**Exit criteria (dev):**

| Metric                            | Target |
| --------------------------------- | ------ |
| Invented citations shown to users | **0**  |
| Faithfulness (judge)              | ≥ 0.85 |
| Citation precision                | ≥ 0.90 |
| Out-of-scope refusals             | ≥ 95 % |
| Judge vs. human Cohen's kappa     | ≥ 0.6  |

### M4 Classifier agent and API

**Delivers:** a tool-calling classifier (with validated, grounded output), 40 risk scenarios, a FastAPI service with an API key and a daily cap, file upload, and a Streamlit UI.
**Exit criteria:** **≥ 85 %** accuracy on the non-ambiguous scenarios, **0 prohibited systems labelled minimal risk**, `make serve` works, and the API contract tests pass.

### M5 Own model and framework comparison

**Delivers:** a fine-tuned multilingual MiniLM published to the Hugging Face Hub as int8 ONNX, a base → FT → int8 table, and `frameworks/COMPARISON.md`.
**Exit criteria:** the before/after table is measured on the **test** split, the int8 model loses ≤ 1 point of Recall@5, the leakage test passes, and both framework versions are smoke-tested.

### M6 Integrations and observability

**Delivers:** the Slack slash command, the MCP server, the Sheets register, the upload demo, Langfuse traces, JSON logs and cost per query.
**Exit criteria:** a screen capture of each integration, plus a trace screenshot in `docs/`.

### M7 Production on Cloud Run

**Delivers:** an image under 450 MB, Secret Manager, keyless WIF deploy with a smoke-tested candidate revision, and a EUR 1 budget alert.
**Exit criteria:** the public URL serves `/ask`, `/classify` and `/search`; cold start ≤ 15 s; billing shows **EUR 0.00** after a week.

### M8 Hardening

**Delivers:** a 40-prompt adversarial suite mapped to the OWASP LLM Top 10, a Locust report (p50/p95, RPS), three failure drills (cap, provider loss, Qdrant loss), and `docs/model_card.md`.
**Exit criteria:** the safety suite passes at **≥ 95 %**, load numbers are recorded, and the drills pass.

### M9 Showcase

**Delivers:** a README with a GIF, live link, results table and architecture diagram; a 2-minute demo video; the blog post _"What broke when I built RAG on the EU AI Act"_; the CV entry.

**If behind schedule, cut in this order:** step 10 (frameworks), then the Sheets register, then the UI. **Never cut** evaluation, the classifier or deployment.

---

## Engineering review of the reference code

I reviewed the guide's snippets as a senior engineer. The issues below are real defects or risks. Each one has a matching task in `TODO.md`, tagged **[fix]**.

| #   | Where                                            | Problem                                                                                                                                                                                                                                                 | Fix                                                                                                                                                                                        |
| --- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R1  | `HybridRetriever.chunks`, `QdrantStore.point_id` | Chunk IDs are **language-free on purpose**, so EN and FR chunks share an ID. Keying `chunks` by `id` makes FR overwrite EN, and `uuid5(chunk_id)` makes the FR Qdrant upsert overwrite the EN point. Half the corpus would disappear without any error. | Use a storage key `f"{id}@{lang}"` for the dict, the NumPy index, Qdrant points and BM25 docs. Keep the language-free `id` for citations and metrics. Optionally filter by query language. |
| R2  | `RagPipeline.ask`                                | `text.replace(bad, "")` also removes substrings of valid IDs: an invented `AIA-Art6` damages a valid `[AIA-Art6-2]`.                                                                                                                                    | Remove only the exact bracketed token, with a regex on `\[...\]` groups.                                                                                                                   |
| R3  | `RagPipeline.ask`                                | `text == "NOT_COVERED"` misses `NOT_COVERED.`, `**NOT_COVERED**` and similar variants.                                                                                                                                                                  | Normalise first (strip punctuation and markdown), then check the start of the text.                                                                                                        |
| R4  | `CachedLLM._key`                                 | The cache key leaves out the **model names** and `max_tokens`. If `GEMINI_MODEL` changes, the cache returns stale answers and the evals look valid when they aren't.                                                                                    | Add the model IDs of the whole chain and `max_tokens` to the key.                                                                                                                          |
| R5  | `RetryingLLM` inside `FallbackLLM`               | With `min_interval=4` and backoff 2+4+8 s, a provider can spend 15–20 s or more before the fallback takes over, while Cloud Run's timeout is 60 s and `/classify` makes several calls.                                                                  | Fail over quickly on 429 in serving (`max_tries=2`) and keep long retries for offline evals only. Set an overall deadline for each request.                                                |
| R6  | `DailyCap`                                       | The counter lives in memory **per instance**: with `--max-instances 2` the real cap is 2×, and it resets on every cold start.                                                                                                                           | Accept and document this, or keep the counter in Firestore or Redis (Firestore's free tier is enough).                                                                                     |
| R7  | Retrieval metrics                                | `recall_at_k` raises an error when `gold` is empty, which is the case for the "not covered" golden questions.                                                                                                                                           | The runner leaves those questions out of retrieval metrics and scores them as refusals instead.                                                                                            |
| R8  | CI                                               | `--cov-fail-under=80` from day 0 will fail once untested glue code arrives (Slack bot, MCP server, Sheets client, `api/app.py`).                                                                                                                        | Add `[tool.coverage.run] omit` for the I/O glue, or raise the threshold gradually.                                                                                                         |
| R9  | Branches                                         | The local branch is `master`, but `main` is the main branch and `deploy.yml` triggers on `main`.                                                                                                                                                        | Rename to `main` before the first push.                                                                                                                                                    |
| R10 | `RetryingLLM` test                               | The test expects delays of 1 s then 2 s, but `base_delay` defaults to 2.0.                                                                                                                                                                              | Pass `base_delay=1` and a fake `sleep` in the test.                                                                                                                                        |
