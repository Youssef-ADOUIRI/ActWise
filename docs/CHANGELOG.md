# Changelog

What changed, when, and why, file by file. Newest first.
Add a section for every step you commit.

---

## 2026-10-28: Step 8, the API and the UI

**Goal:** serve the cited answers and the classifier over HTTP, with cost guards, and add a small UI.
**Branch:** `step-8-api`

| File | What | Why |
|---|---|---|
| `src/actwise/api/main.py` | `create_app()`: `/health`, `/search`, `/ask`, `/classify`, `/upload`, the API key, the daily cap, one deadline per request, and 503 when no model answers in time. Answers and classifications carry the disclaimer | The pipelines are injected, so the contract tests run on fakes |
| `src/actwise/api/guards.py` | `DailyCap`: in memory, per instance, safe across threads | R6, decision 009 |
| `src/actwise/ingest/files.py` | `extract_text()` for .txt, .md, .pdf and .docx, cut to the 8,000 characters of `/classify`. Readers yield their text piece by piece, and reading stops at the limit | `/upload`. A 2 MB, 880-page PDF took 15.6 s before the early stop and takes 0.12 s with it |
| `src/actwise/api/app.py` | The wiring: serving profile, system E, `answer.v2` and the classifier; `make serve` | |
| `src/actwise/llm/wrappers.py`, `factory.py` | `LLMUnavailable`. `Profile.max_wait`: a Retry-After above it (5 s serving, 60 s offline) skips the provider, without a request, until it has passed | Serving fails over instead of sleeping through a rate limit (found by `/simplify`); from the step 6a review: a spent quota costs no request |
| `src/actwise/generation/rag.py`, `src/actwise/agent/classifier.py` | A `deadline` passed to every model call | R5, API side |
| `src/actwise/retrieval/systems.py` | `SYSTEMS`, their builders, and `SERVED` (system E), moved from `evals/run_eval.py` | The API and both eval scripts pick the system by name |
| `ui/app.py` | Streamlit: an Ask tab and a Classify tab (text or file), calling the API over HTTP. `make ui` stops uploads at 2 MB; `ui` extra | The API image stays without Streamlit |
| `docs/decisions/009-api.md`, `docs/failure_cases.md` | The request deadline, the cap kept per instance, and the error codes. A question on the workplace emotion-recognition ban that retrieval missed | |

**Results (local, Gemini 3.5 Flash-Lite):**
- **Guards, live:** 401 without the key, 422 for bad input, 415 for a `.exe`, and 429 once `MAX_DAILY_REQUESTS` was reached. The tests also cover 413 and 503.
- **Live:** `/ask` answered in English and French in 2–3 s, and three dev scenarios came back with their gold tiers in 1.4–2.8 s, as JSON, from a `.txt` and from a `.docx`. A PDF upload was classified in 2.7 s.
- **UI:** both tabs ran against the live API in a Streamlit `AppTest` smoke run.
- **Checks:** 226 tests pass, coverage is 95 %, and ruff and mypy are clean.

**Next:** step 9 fine-tunes and shrinks the embedder, which the cloud profile needs.

---

## 2026-10-27: Step 7, the risk classifier agent

**Goal:** an agent that reads the AI Act before it decides, and cannot return a classification that is invalid or ungrounded.
**Branch:** `step-7-classifier`

| File | What | Why |
|---|---|---|
| `src/actwise/agent/schemas.py` | `Classification` (tier, reasons, citations, confidence, follow-up questions), its title-free tool schema, and `TIER_ARTICLES` | The output shape is defined once; each tier names the articles it must cite |
| `src/actwise/agent/classifier.py` | Tools `read_ai_act_article` (by id), `search_ai_act` (AI Act only, one per paragraph) and `submit_classification`. Guards: schema errors fed back, citations read or retrieved, the tier cites its own rule, follow-ups for `needs_more_info`, a plain-text nudge, a budget warning 3 steps before the limit of 8 | A wrong or ungrounded answer is refused inside the loop, not after it |
| `src/actwise/prompts/classify.v1.md` | The order of checks: Art. 5, Art. 6 with Annex I/III and the Art. 6(3) exceptions, Art. 50, else minimal risk | |
| `data/eval/risk_scenarios.csv`, `src/actwise/evaluation/scenarios.py`, `tests/test_scenarios.py` | 40 scenarios (20 dev / 20 test, 12 in French, 6 ambiguous). Each quotes its deciding sentence, checked word for word against the paragraph the agent reads, and every label is verified by a person | The guide's rule: never trust a label nobody checked |
| `src/actwise/evaluation/classifier_eval.py`, `evals/run_classifier.py` | Accuracy on clear and ambiguous scenarios apart, the confusion matrix, prohibited labelled minimal and other dangerous downgrades, failed runs, steps; `make eval-classifier` | |
| `src/actwise/llm/base.py`, `openai_compat.py` | `ToolCall.extra`: unknown provider fields kept per provider and sent back unchanged | Gemini 3 rejects a turn whose function calls lack their thought signature |
| `src/actwise/retrieval/passages.py` | `paragraph_passages()`: a long paragraph's windows joined back, without their shared words | What the read tool shows and what the scenario test checks |
| `evals/run_eval.py`, `evals/judge_kappa.py` | One `write_report()` for the three eval scripts | Found by `/simplify` |
| `docs/decisions/008-classifier.md`, `docs/model_card.md`, `docs/failure_cases.md` | The design record; the first limitations, including the AI Omnibus dates; queries that name an article miss it | |

**Results (dev, commit `f3670f9`):**
- **Clear scenarios:** 17/17, in English and in French. **Ambiguous:** 3/3.
- **Safety:** 0 prohibited or high-risk systems labelled minimal risk, and 0 runs out of steps.
- **Cost:** 3.55 model calls per run on Gemini 3.5 Flash-Lite.
- **Checks:** 212 tests pass, coverage is 97 %, and ruff and mypy are clean.

**Found live:**
- Searching for "Article 6(1)" never returned it, which led to the read tool.
- The agent kept searching after it had found its rule, which led to the budget warning.

**Next:** step 8 serves `/classify` through the API, with one deadline per request.

---

## 2026-10-25: Step 6b, calibrated judge and 179 questions

**Goal:** a judge calibrated against human labels, a golden set of 150+ questions, and the retrieval and answer results re-measured on it. This closes M3.
**Branch:** `step-6b-golden-150`

| File | What | Why |
|---|---|---|
| `data/eval/human_labels.csv` | 58 answers scored blind by a person, then re-checked at the 3/4 boundary with one written rule (six labels moved) | Calibration data |
| `evals/judge_kappa.py`, `evals/reports/judge-calibration.*` | Cohen's kappa at faithful = 4–5 (the target), plus kappa at 5 only, quadratic-weighted kappa and planted claims caught | **0.739**, with `judge.v1` unchanged (decision 007) |
| `evals/merge_candidates.py`, `data/eval/golden.jsonl` | 129 reviewed candidates become q051–q179 with `source: synthetic` | Dev has 71 scored + 12 out-of-scope questions, test 78 + 12 |
| `src/actwise/evaluation/golden.py`, `tests/test_golden_set.py` | `Question.source`; ≥ 150 questions, and ≥ 50 scored and ≥ 10 refusal questions in dev and in test | Decision 002 revisited |
| `src/actwise/evaluation/runner.py`, `generation.py`, `answers.py`, `evals/run_eval.py` | Breakdowns by source in every report, and a **fully supported** rate (answers scored 5) | Synthetic questions are easier; the judge agrees with humans best on "any unsupported claim" |
| `evals/reports/*-dev.*` | Seven retrieval rows (commit `c2288b1`) and v1/v2 answers (`c07703c`) on the grown dev set | The source of the tables |
| `docs/ablations.md`, `docs/generation.md` | Both tables on the grown dev set, hand-written and synthetic apart | |
| `docs/decisions/002-evaluation-protocol.md`, `007-judge-calibration.md` | The new allocation, and the calibration record | |

**Results (dev):**
- **Retrieval, 71 questions:** E has Recall@5 **0.979** [0.94, 1.00] and MRR 0.904; F has MRR 0.966. The hand-written numbers reproduce step 4 exactly, and synthetic questions reach Recall@5 1.000 on every structure-aware row.
- **Answers, 83 questions:** v2 refuses 12/12 out of scope and wrongly refuses 2/71, shows 0 invented citations, and scores faithfulness 0.971 [0.93, 1.00] (fully supported 0.942) and lenient citation precision 0.944. v1 is more faithful (0.992) but refuses 5/71.
- **Every M3 target is met with v2.**
- **Checks:** 188 tests pass, coverage is 96 %, and ruff and mypy are clean.

**Plain baseline on the grown set (added after merge):** it refuses 0 of 12 out-of-scope questions; faithfulness 0.991 and fully supported 0.964, but no citations.

---

## 2026-10-24: Step 6a, cited answers, guardrails and the judge

**Goal:** answers that cite only retrieved passages and refuse otherwise; a judge, answer metrics and a first prompt A/B; review files for the human steps of 6b.
**Branch:** `step-6a-cited-answers`

| File | What | Why |
|---|---|---|
| `src/actwise/generation/citations.py` | Extract paragraph-level citation ids, flag invented ones, and strip exactly those ids from their brackets | R2: `str.replace` damaged valid ids such as `[AIA-Art6-2]` |
| `src/actwise/generation/rag.py` | `RagPipeline`: refuses injection-looking questions, `NOT_COVERED` in any dress, and answers left with no valid citation. Citations are read back from the shown text, and the pipeline fails closed | R3. No citation reaches a user that the system can't back, on the serving path too |
| `src/actwise/generation/guardrails.py` | PII redaction (used before logging) and injection regexes, EN and FR | Cheap input checks |
| `src/actwise/prompts/*.md`, `generation/prompts.py` | Versioned prompts shipped in the package: `answer.v1`, `answer.v2`, `judge.v1`, and the synthetic and perturbation prompts. `json_object()` reads JSON replies | Serving finds them from any directory |
| `src/actwise/evaluation/judge.py` | Verdicts as JSON: score 1–5, a reason and the unsupported citations. An unreadable reply stays unreadable, never a 0 | Faithfulness and lenient citation precision from one call |
| `src/actwise/evaluation/generation.py` | Refusal rate, **false-refusal rate**, invented citations raw and shown, citation precision strict and lenient, faithfulness with an interval | Refusing everything must not pass the refusal target |
| `src/actwise/evaluation/answers.py`, `evals/run_eval.py` | `--prompt plain\|answer.vN` and `--judge` replace `--llm`; one row format for the baseline and the cited pipeline | The A/B table in `docs/generation.md` |
| `src/actwise/llm/factory.py` | `Profile.fallback` (evals use one model) and `build_judge` (`JUDGE_PROVIDER`, `JUDGE_MODEL`) | A prompt A/B must not mix two models. The judge is another model family |
| `src/actwise/llm/wrappers.py` | Honour `Retry-After` and Gemini's in-body `retryDelay`; a wait over 60 s raises at once | Gemini's spent daily quota had burned four tries |
| `src/actwise/evaluation/synthetic.py`, `evals/make_synthetic.py` | 144 golden-set candidates: 60 dev + 60 test in scope from seeded paragraphs, 24 out of scope; screened by rule | The 150-question set of 6b |
| `evals/make_calibration.py` | A blind sheet of 58 answers, 13 of them with a planted unsupported claim | Without unfaithful items, kappa can't tell a good judge from a bad one |
| `data/eval/candidates.csv`, `.md` | The candidates with Claude's pre-screen: 129 kept or fixed, 15 dropped, each with a reason | For you to confirm or override |
| `data/eval/human_labels.csv`, `.md`, `_key.json` | The sheet to score, the reading file, and the key for 6b | Judge calibration |
| `evals/reports/*-dev-{plain,answer.v1,answer.v2}.*` | Dev answer reports from commit `9d5aefa`; `baseline-dev-answers` becomes `baseline-dev-plain` | The source of `docs/generation.md` |
| `docs/generation.md`, `docs/decisions/006-cited-answers.md` | The provisional A/B table and the design record | |
| `ids.py`, `build_chunks.py`, `golden.py`, `splits.py` | `paragraph_id`, `load_chunks`, `NAMES_AN_ARTICLE` each get one home | Found by the `/simplify` pass |
| `tests/unit/` | The six TODO tests, plus judge, metrics, candidate, Retry-After and fallback-profile tests | |

**Results (dev, 22 questions, provisional):**
- **v1** refuses 4 of 20 in-scope questions. They are partly covered: two by retrieval misses on cross-law questions, two by the strict prompt.
- **v2** answers the covered part and has **0 false refusals**. Both v1 and v2 refuse 2 of 2 out-of-scope questions and invent no citation.
- **Faithfulness** is 0.99–1.00 for every row, plain included, from a judge that is not calibrated yet.
- **Checks:** 186 tests pass, coverage is 96 %, and ruff and mypy are clean. A full re-run is served from the cache.

**Judge choice:**
- `gemini-3.8-flash` takes 130–150 s for a one-word reply on the free tier, and `gemini-3.6-flash` allows 20 requests a day.
- `openai/gpt-oss-120b` on Groq caught a planted claim, and costs about 1.5K tokens per verdict.

**Left for 6b:** kappa from the human labels; merging the reviewed candidates; the ablations and the A/B on 150+ questions; and optionally dropping repeated passages from the context.

---

## 2026-10-24: Step 5, the LLM provider layer

**Goal:** one `chat()` over Gemini, Groq, Ollama and Anthropic, with a disk cache, retries and a fallback chain, so that evals can be re-run for free and the demo stays up.
**Branch:** `step-5-provider-layer`

| File | What | Why |
|---|---|---|
| `src/actwise/llm/base.py` | Provider-neutral messages, `ToolCall`, `LLMResponse` (with the model that answered), and the `LLM` protocol, whose `chat()` takes a `deadline` | One interface for every provider. The deadline lets retries, fallbacks and HTTP timeouts share one time budget (R5) |
| `src/actwise/llm/openai_compat.py` | One adapter for Gemini, Groq and Ollama; it sends `max_tokens` and shrinks the HTTP timeout to the deadline | All three speak the OpenAI protocol. The guide's adapter never sent `max_tokens` (R12) |
| `src/actwise/llm/anthropic_adapter.py` | Messages API adapter: system prompt split off, tool results merged into one user turn, no `temperature` | `anthropic` 1.x has no `temperature` argument (R11) |
| Both adapters | SDK clients built with `max_retries=0` | Stacked under the SDKs' own retries, 4 tries became 12 (R13) |
| `src/actwise/llm/wrappers.py` | `CachedLLM`, keyed by the chain's model ids, the request and `max_tokens`, with atomic writes. `RetryingLLM` retries 408, 429, 5xx and 529, waiting for the backoff or the rate-limit interval, whichever is longer, within the deadline. `FallbackLLM` logs each failover and starts no provider after the deadline | R4, R5, R15 |
| `src/actwise/llm/factory.py` | Providers from `.env`; `OFFLINE` and `SERVING` profiles; `build_llm(env, profile)`, with the profile required | An empty key or model skips a provider and an unknown name raises (R14). Evals wait out rate limits, while serving fails over within 25 s (R5) |
| `src/actwise/llm/smoke.py`, `make llm-smoke` | One prompt through each provider, then through the cached chain | The live check of the step. It found the retired Gemini model |
| `src/actwise/evaluation/answers.py`, `evals/run_eval.py --llm`, `make eval-answers` | The baseline answers deferred from step 3: plain prompt, top 5 passages, temperature 0, and the model of each answer recorded | The "before" row that the step 6 judge scores. `--llm` builds the chain first, so a bad `.env` fails before model loading. It refuses reranked systems, which would load both 2 GB models |
| `evals/reports/baseline-dev-answers.json`, `.md` | 22 dev answers from commit `d511957` | The baseline for step 6 |
| `pyproject.toml`, `uv.lock` | `python-dotenv` becomes a direct dependency; `smoke.py` is left out of coverage | It reads `.env` correctly, while `uv run --env-file` stops at `REGISTER_NAME=ActWise register` |
| `.env.example` | `GEMINI_MODEL=gemini-3.5-flash-lite`; empty providers are skipped | `gemini-2.5-flash-lite` answers 404 to new users |
| `docs/decisions/005-provider-chain.md` | Provider order, one retry layer, the two profiles | Design record |
| `docs/ROADMAP.md` | M3 in progress; review items R11 to R15 | Defects found by reading the guide's code against the installed SDKs |
| `tests/unit/` | `test_openai_adapter_round_trip`, `test_anthropic_adapter`, `test_cache_hits_skip_provider`, `test_retry_backoff` (R10), `test_fallback_chain`, `test_factory_skips_unconfigured`, plus deadline, rate-limit, config and answers tests; `ScriptedLLM` in `toys.py` | Real SDK error classes and fake clients, so CI makes no network call |

**Results:**
- **Live check:** `gemini-3.5-flash-lite` answers in 0.8–0.9 s and names the right article (Art. 5). `gpt-oss-20b` on Groq answers in 0.2–0.5 s and names the wrong one (Art. 6).
- **`max_tokens=16`:** caps both providers. gpt-oss then returns empty text, because its reasoning uses up the budget.
- **Baseline answers:** 22 dev answers, all from Gemini, using 21,837 input and 2,536 output tokens. A re-run makes 22 cache hits and no API call.
- **Checks:** 137 tests pass; coverage is 95 %, and 100 % on `llm/`; ruff and mypy are clean.

**Left for later:** honouring `Retry-After` before the 150-question runs (step 6); one deadline per API request (step 8); loading `.env` in `retrieval/index.py` (step 9).

---

## 2026-10-20: Step 4, hybrid retrieval, reranking and ablations

**Goal:** reach Recall@5 ≥ 0.85 on dev, with each change measured on its own.
**Branch:** `step-4-hybrid-rerank`

| File | What | Why |
|---|---|---|
| `src/actwise/retrieval/passages.py` | `Passage` and `Hit` (moved from `dense.py`); `chunk_passages()` builds structure-aware passages with their headers; payloads hold `key`, `id`, `law` and `lang` | Every retriever shares them; stores filter on the payload |
| `src/actwise/retrieval/bm25.py` | Okapi BM25 on an inverted index; accents folded, elisions split | No dependency; finds exact legal terms, and French typed without accents still matches |
| `src/actwise/retrieval/fusion.py` | Reciprocal rank fusion | Merges rankings with no score normalisation or tuned weight (decision 003) |
| `src/actwise/retrieval/hybrid.py` | Stage 1: dense + BM25 fused with RRF; stage 2: optional rerank. `binding_first` ranks articles and annexes before recitals | The fix for the biggest failure cause (`docs/failure_cases.md`) |
| `src/actwise/retrieval/rerank.py` | `CrossEncoderReranker` for `bge-reranker-v2-m3`, pinned to commit `953dc6f` | Rows D and F (decision 004) |
| `src/actwise/retrieval/stores.py` | `Store` protocol and payload filters; `QdrantStore` with point id = `uuid5(id@lang)`; `FallbackStore` | R1: with `uuid5(chunk id)`, FR points would overwrite EN ones. The fallback keeps search up if Qdrant fails |
| `src/actwise/retrieval/dense.py` | The embedding cache is keyed by text; `build_store()` returns a store with payloads | Rows A to F share one set of vectors, and an edited passage re-embeds only itself |
| `src/actwise/retrieval/embedders.py` | The `BGE_M3` pin moves here; the model loads on first use; `unload()` | With a warm cache the model never loads (`make index` takes 10 s) |
| `src/actwise/retrieval/index.py`, `docker-compose.yml`, `Makefile` | `make index` uploads the 3,799 chunks to Qdrant 1.19.2; `make ablations` runs every row | One command per step |
| `src/actwise/ids.py`, `src/actwise/ingest/chunk.py` | `is_recital()`, `law_of()` | For the ordering rule and the payloads |
| `evals/run_eval.py` | Systems baseline and A to F; reranked rows run in two passes | The embedder and the reranker take about 2 GB each, more than the laptop can hold together |
| `evals/reports/*-dev.json`, `.md` | One report per row, all from commit `8e5e84b` | The source of the table |
| `docs/ablations.md` | The filled table, what each change did, and the choice of E | The step 4 deliverable |
| `docs/failure_cases.md` | Each dev failure labelled with its cause, before and after the fix | Picks the fix and lists what is left |
| `docs/decisions/003-fusion.md`, `004-rerank.md` | Fusion and reranking decisions | Design record |
| `tests/unit/` | `test_rrf`, `test_bm25`, `test_hybrid_end_to_end`, `test_reranker_reorders`, `test_store_failover`, `test_gdpr_filter`, plus cache, payload and lazy-model tests; shared toys in `toys.py` | `test_gdpr_filter` runs on Qdrant in process in CI, and on the Docker server when one is running |
| `README.md` | Retrieval commands in the quickstart | |

**Results (dev, n = 20):**
- **E (the default):** Recall@5 **0.925** [0.80, 1.00], MRR@10 0.806, 149 ms/query, against a baseline of 0.650.
- **F (with the reranker):** MRR@10 0.906, at 11.8 s/query.
- **Qdrant:** gives the same top 10 as the NumPy store in 150 of 150 samples.
- **Checks:** 110 tests pass, plus the Qdrant server test; coverage is 93.6 %; ruff and mypy are clean.

**Cache migration:** the step 3 baseline vectors moved into the text-keyed cache bit for bit, and the baseline report reproduces field for field.

**Deferred:** NumPy snapshots for the cloud image (`save()`/`load()`) arrive with `make index-cloud` in step 9.

---

## 2026-10-20: Cleanup of the step 3 code

**Goal:** give each rule that step 3 wrote twice a single home, and drop options nothing uses. No output changes.

| File | What | Why |
|---|---|---|
| `src/actwise/ids.py` | `storage_key()` builds `id@lang` for `Chunk.key` and `Passage.key` | The storage-key format (review item R1) was written in two classes |
| `src/actwise/ingest/chunk.py`, `build_chunks.py` | `unit_id()` and `parse_source()`, also used by the baseline | The article-id format behind the gold labels, and the raw-file naming, were in two modules |
| `src/actwise/ingest/parse.py` | `_starts_with_punctuation()` replaces a helper that only ever got one character | The name says what the footnote rule checks |
| `src/actwise/evaluation/metrics.py`, `runner.py` | `first_hit_rank()` shared by MRR and the report rows; `ranked_articles()` is one line; the unused `pool` argument is gone | The first-hit rule was written twice |
| `src/actwise/evaluation/splits.py` | Reads `build_chunks.OUT_FILE` instead of its own copy of the path | One path to change if the chunks move |
| `src/actwise/retrieval/dense.py`, `stores.py` | `Hit` extends `Passage`; `build_store()` always uses the cache; the temp shard name comes from `path()`; `search()` loses its unused default `k` | Fewer field lists and branches to keep in sync |
| `src/actwise/retrieval/naive.py`, `evals/run_eval.py` | `MAX_WORDS` and `OVERLAP` name the baseline windows, and the report description is built from them | The description can't drift from the code |
| `tests/unit/test_dense.py` | The retriever test uses a temporary cache | `build_store()` no longer has a mode without a cache |

**Checked:** `chunks.jsonl` rebuilds byte for byte, the 2,385 baseline passages are identical, and a fresh dev run reproduces `baseline-dev.json` field for field (except time, commit and ms/query). 93 tests pass (92 % coverage); ruff and mypy are clean.

**Left for step 4:** the embedding cache keys its folder on every text, so editing one passage re-embeds them all. Keying vectors by text hash would let the ablations reuse what is already embedded.

---

## 2026-10-20: Docstrings on every function

**Goal:** every function and method says in one line what it does.

| File | What | Why |
|---|---|---|
| `src/actwise/**/*.py`, `evals/run_eval.py` | A docstring on the 45 functions and methods that had none; `parse_regulation` also says how it reads the text | What a function does, without reading its body |
| `tests/**/*.py` | A docstring on the 75 tests, fixtures and helpers that had none | When a test fails, its docstring says which rule broke |
| `pyproject.toml` | Ruff rules D102, D103, D105, D107 | A new public function without a docstring now fails `make lint`, pre-commit and CI |

**Results:** every function has a docstring. Ruff does not check private or nested helpers (6 today), so those stay a review habit. No behaviour changed: ruff and mypy are clean, and the 93 tests pass.

---

## 2026-10-20: Step 3, baseline and evaluation harness

**Goal:** a naive retrieval system, measured on a hand-written golden set, so every later change can be compared against it.
**Branch:** `step-3-baseline-eval`

| File | What | Why |
|---|---|---|
| `src/actwise/evaluation/splits.py` | Article-level 70/15/15 split, seed 42; `make splits` | Splitting by article keeps one article's paragraphs out of two splits, so step 9 training pairs cannot leak into dev or test |
| `data/eval/splits.json` | 404 train, 87 dev, 87 test units | Fixed before any question was written |
| `data/eval/golden.jsonl` | 50 hand-written questions: 20 dev, 20 test, 6 train, 4 out of scope; 18 in French | Labels checked against the article text; the allocation gives dev and test 20 questions each (decision 002) |
| `src/actwise/evaluation/golden.py` | `Question`, `load_golden`, `question_split` | A question takes the split of its gold articles; out-of-scope questions carry their own |
| `src/actwise/evaluation/metrics.py` | Recall@k, MRR, nDCG at article level, bootstrap intervals | Gold labels are articles; with 20 questions every number needs an interval |
| `src/actwise/evaluation/runner.py` | `evaluate()` and the Markdown summary | Per-question rows, breakdowns by language and type, and the list of misses for error analysis; out-of-scope questions are skipped for retrieval (review item R7) |
| `src/actwise/retrieval/naive.py` | Fixed 150-word windows over the whole text, each labelled with the article where it starts | The baseline the guide asks for: structure is ignored on purpose |
| `src/actwise/retrieval/embedders.py` | `Embedder` protocol, `SentenceTransformerEmbedder` with a pinned revision | One interface for local and (later) ONNX models; the Hub commit is part of the config |
| `src/actwise/retrieval/stores.py` | `NumpyStore`: exact cosine search | Enough for 2,385 passages (~1 ms); Qdrant comes in step 4 |
| `src/actwise/retrieval/dense.py` | `Passage`, `Hit`, `EmbeddingCache`, `build_store`, `DenseRetriever` | Vectors are cached in atomic on-disk shards keyed by model, revision and texts: a 45-minute CPU run can stop and resume, and stale vectors are never reused |
| `evals/run_eval.py` | `--system --split --name`; writes `evals/reports/<name>.json` and `.md` | Each report records the commit, the embedder revision and fingerprints of the golden set and splits |
| `evals/reports/baseline-dev.json`, `.md` | Dev results of the baseline | The reference row of `docs/ablations.md` |
| `docs/ablations.md` | Ablation table with the baseline row and its failure patterns | The table step 4 fills in |
| `docs/decisions/002-evaluation-protocol.md` | Splits, allocation, labels, intervals | Design record |
| `src/actwise/ingest/parse.py`, `chunk.py`, `data/processed/chunks.jsonl` | Also drop `*` footnote marks and glue the punctuation that follows a removed mark; `window_starts()` shared with the baseline | Found while reading articles for the golden set: 107 chunks change text only, ids unchanged |
| `Makefile` | `splits`, `eval-retrieval` (`SYSTEM`, `SPLIT` variables), `eval`; mypy also checks `evals/` | One command per step |
| `tests/` | Unit tests for metrics, splits, golden set, naive windows, store, cache, runner; `tests/test_golden_set.py` validates the real golden set | Labels and protocol are tested like code |

**Results (dev, n = 20):** Recall@5 **0.650** [0.45, 0.85], MRR@10 0.504 [0.32, 0.69], nDCG@10 0.547, Recall@20 0.825, 170 ms/query on CPU. 93 tests pass (92 % coverage); ruff and mypy are clean.

**Provenance fix:** the main BGE-M3 commit only ships `pytorch_model.bin`, so transformers silently loaded the safetensors conversion from a Hub pull request. The pin now names that commit (`9a0624b`), so reports record the weights that were really used (vectors verified identical).

**Deferred:** generating baseline answers with a plain prompt needs the provider layer, so it moves to step 5.

---

## 2026-10-04: Step 2, parse and chunk with stable IDs

**Goal:** turn the four pages into `data/processed/chunks.jsonl`, one record per paragraph, recital or annex point, with IDs shared by EN and FR.
**Branch:** `step-2-parse-chunk`

| File | What | Why |
|---|---|---|
| `src/actwise/ids.py` | `parse_id`, `is_valid_id`, `article_id`, `human_label` | One ID format for ingestion, retrieval, evaluation and citations. Also supports annex sections (`AIA-AnnexVIII-b.1`). |
| `src/actwise/ingest/parse.py` | `normalise_lines`, `parse_regulation` → recitals, articles, annexes | A line-based parser, so it survives markup changes. Fixes everything the guide's version missed on the real text (see decision 001). |
| `src/actwise/ingest/chunk.py` | `Chunk` (`id`, `key`, `embed_text`), `split_words`, `chunk_units` | Splits paragraphs into 150-word windows with 25 words of overlap. `key = id@lang` stops FR from overwriting EN in stores (review item R1). The header uses French law names for FR. |
| `src/actwise/ingest/build_chunks.py` | Builds and writes `chunks.jsonl`, prints counts | The entry point for `make ingest`. |
| `data/processed/chunks.jsonl` | 3,799 chunks (AI Act 1,128 EN / 1,196 FR, GDPR 716 EN / 759 FR) | Committed: small, public, and the input to every later step. |
| `Makefile` | `ingest` target | `make ingest` rebuilds the chunks. |
| `tests/unit/sample_text.py` | EN sample (from the guide) plus a FR sample using the real layout | Offline fixtures for the parser tests. |
| `tests/unit/test_ids.py` | Valid and invalid IDs, `article_id`, labels in EN/FR | The ID format is the contract between modules. |
| `tests/unit/test_parse.py` | Structure, chapter titles, FR layout, footnotes, end matter, annex sections | Each real-text edge case is pinned by a test. |
| `tests/unit/test_chunk.py` | Expected IDs, header, FR names, storage key, long-paragraph windows | Chunking rules from the guide, plus fix R1. |
| `tests/test_corpus.py` | Runs on the real pages: official counts, valid and unique IDs, FR = EN ID sets | Fails if a parser change drops or duplicates anything. |
| `tests/__init__.py`, `tests/unit/__init__.py` | Package markers | Let tests import the shared sample. |
| `docs/decisions/001-chunking.md` | The chunking decision and its edge cases | Design record for the README and interviews. |

**Results:** all official counts match, with no duplicate or invalid IDs. 56 tests pass with 93 % coverage, and ruff and mypy are clean.

---

## 2026-10-04: Step 1, legal text

**Goal:** have the four official texts in the repo and turn them into plain text.
**Commit:** `2fc1cb9`

| File | What | Why |
|---|---|---|
| `data/raw/ai_act.en.html` | AI Act, English, from EUR-Lex | The source of truth. It's committed so ingestion is reproducible offline. |
| `data/raw/ai_act.fr.html` | AI Act, French | Bilingual corpus: French questions need French text. |
| `data/raw/gdpr.en.html` | GDPR, English | Second law, for cross-law questions. |
| `data/raw/gdpr.fr.html` | GDPR, French | Same as above, in French. |
| `data/raw/SOURCES.md` | URLs, access date, legal notice | Traceability and the EUR-Lex reuse terms. Also notes that the AI Omnibus (2026/1744) isn't included. |
| `src/actwise/ingest/__init__.py` | Empty package marker | Makes `actwise.ingest` importable. |
| `src/actwise/ingest/html.py` | `html_to_text(path)` and `html_string_to_text(html)` | Removes scripts, styles and menus, and turns `&nbsp;` into a space so `Article 6` matches simple regexes. Silences the harmless XHTML parser warning. |
| `tests/unit/test_html.py` | 5 tests | Checks the cleanup on a small HTML sample, and checks that each saved page contains `Article 6` and `ANNEX III` / `ANNEXE III` (AI Act) or `Article 17` (GDPR). |
| `.gitattributes` | LF line endings, HTML left untouched | Windows was turning files into CRLF, which breaks the `Makefile` on Linux CI. |

**Notes**
- A plain `curl` downloaded the pages. The bot challenge described in the guide didn't happen.
- In the real text, point markers such as `(a)` sit on their own line. Step 2 has to handle this.

---

## 2026-10-04: Step 0, project skeleton

**Goal:** an empty but professional project that runs lint and tests on every push.
**Commit:** `b5f8634`

| File | What | Why |
|---|---|---|
| `pyproject.toml` | Package metadata, dependencies, `local`/`cloud` extras, dev group, ruff/mypy/pytest/coverage config | One place for all settings. The `cloud` extra leaves out PyTorch to keep the Docker image small. Coverage leaves out I/O glue (review item R8) so the 80 % gate stays meaningful. |
| `src/actwise/__init__.py` | Package with `__version__` | Root of the `src/` layout. |
| `tests/unit/test_smoke.py` | Import test | Placeholder so CI has something to run. |
| `Makefile` | `install`, `lint`, `test`, plus stubs for `ingest`, `index`, `eval`, `serve`, `deploy` | The same commands locally and in CI. The stubs mark the steps to come. |
| `.env.example` | Every setting, with comments | A template for `.env`. Secrets are never committed. |
| `.gitignore` | Secrets, caches, models, build output | Keeps the repo clean. It extends the original `.env`-only file. |
| `.pre-commit-config.yaml` | `ruff-check` + `ruff-format` hooks | Catches style issues before each commit. |
| `.github/workflows/ci.yml` | uv install → `make lint` → `make test` | Every push is checked. It runs on Python 3.12. |
| `README.md` | Pitch, CI badge, quickstart | The first thing a visitor reads. |
| `docs/decisions/TEMPLATE.md` | Five-line decision template | Each design choice is written down as options → measured → chosen. |

**Repo change:** the branch was renamed from `master` to `main` (review item R9), so the deploy workflow will trigger on it.

---

## 2026-10-03: Planning

**Goal:** turn the project guide into a plan you can follow.
**Commits:** `c8e9764`, `321e2f7`

| File | What | Why |
|---|---|---|
| `docs/ROADMAP.md` | Features, milestones M0–M9, exit criteria, engineering review of the reference code (R1–R10) | A readable plan with measurable targets, plus the defects to fix in the guide's code. |
| `TODO.md` | A checklist for each step, tagged `[test]` and `[fix]` | Day-to-day tracking. A box is ticked only once the work is committed. |
