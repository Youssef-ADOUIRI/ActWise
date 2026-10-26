# ActWise TODO

Milestones, targets and the code review are in [`docs/ROADMAP.md`](docs/ROADMAP.md).
Tick a box only when the work is **committed**. Commit after every step.
`[test]` marks a test to write first, and `[fix]` marks a correction to the guide's reference code (see ROADMAP §Engineering review).

---

## Before you start: accounts (all free)

- [x] GitHub public repo `actwise`
- [x] Google AI Studio: Gemini key in a project with **no billing account**
- [x] Groq console key
- [ ] Qdrant Cloud account
- [ ] Langfuse Cloud (Hobby plan)
- [ ] Hugging Face account
- [ ] Colab or Kaggle (GPU)
- [ ] Free Slack workspace
- [ ] Google Cloud project for Cloud Run (billing linked, kept separate from the Gemini project)
- [ ] Local tools: Python 3.12, uv, Docker Desktop, git, Ollama (optional)

---

## M0 Foundation and corpus (week 1)

### Step 0: Repo, tooling, CI

- [x] `[fix]` Rename the branch `master` → `main` (R9)
- [x] `pyproject.toml` (src layout)
- [x] Add the dependencies: core, `local` extra, `cloud` extra, dev
- [x] `Makefile` stubs: `ingest`, `index`, `test`, `eval`, `serve`, `deploy`
- [x] `.env.example`, plus `.gitignore` covering `.env`, `.cache/`, `models/`
- [x] ruff, mypy and pytest config in `pyproject.toml`; pre-commit config
- [ ] Install uv + make locally, then `make install` (sets up pre-commit hooks)
- [x] `[fix]` Coverage `omit` for I/O glue modules (R8)
- [x] `.github/workflows/ci.yml` (check the action versions)
- [x] Placeholder test, one-line pitch in the README
- [x] Push and confirm the CI badge is green
- [x] Create the `docs/decisions/` folder

### Step 1: Legal text

- [x] Save `data/raw/ai_act.en.html`, `ai_act.fr.html`, `gdpr.en.html`, `gdpr.fr.html` (curl worked, no bot challenge)
- [x] `html_to_text(path)` with BeautifulSoup + lxml
- [x] Check that the output contains "Article 6" and "ANNEX III" / "ANNEXE III"
- [x] `data/raw/SOURCES.md` with URLs and access date

### Step 2: Parse and chunk with stable IDs

- [x] `[test]` `tests/unit/sample_text.py` (the guide's sample) plus a French mirror
- [x] `[test]` `test_ids`
- [x] `[test]` `test_parse_structure`
- [x] `[test]` `test_chapter_titles_not_glued`
- [x] `[test]` `test_chunk_ids`
- [x] `[test]` `test_embed_text_header`
- [x] `[test]` `test_same_ids_in_french`
- [x] `[test]` `test_long_paragraph_split`
- [x] `src/actwise/ids.py`
- [x] `src/actwise/ingest/parse.py`
- [x] `src/actwise/ingest/chunk.py`
- [x] `[fix]` Add a `key` property (`f"{id}@{lang}"`) to `Chunk` for storage (R1)
- [x] `ingest/build_chunks.py` + `make ingest` → `data/processed/chunks.jsonl`
- [x] Count check: AIA 113 art. / 13 annexes / 180 recitals; GDPR 99 art. / 173 recitals
- [ ] Read 20 random chunks per language (noise scan + 6 samples done; a full read is still to do)
- [x] Decision note: chunking (`docs/decisions/001-chunking.md`)
- [x] Real-text edge cases: FR `ONT ADOPTÉ`, `1)` definitions, footnote marks, end matter, annex sections

---

## M1 Measured baseline (week 2)

### Step 3: Baseline RAG + eval harness

- [x] `data/eval/splits.json`: 70/15/15 **by article**, seed 42 (404 / 87 / 87 units)
- [x] 50 hand-written golden questions (18 FR; 20 dev, 20 test, 6 train, 4 out of scope; all five types)
- [x] Naive baseline: 150-word windows, BGE-M3 (pinned revision), cosine only
- [x] `[test]` Metric tests (article dedup, MRR = 1/3, nDCG by hand) + bootstrap intervals
- [x] `src/actwise/evaluation/metrics.py`
- [x] `[fix]` The runner leaves empty-gold questions out of retrieval metrics (R7)
- [x] `evals/run_eval.py --system --split --name`, writing a JSON report and a markdown summary (`--llm` / `--slice` come with generation in steps 5–6)
- [x] `make eval-retrieval` (`SYSTEM=`, `SPLIT=`)
- [x] Commit `evals/reports/baseline-dev.json`: Recall@5 0.650, MRR@10 0.504, nDCG@10 0.547 (dev, n = 20)
- [x] `tests/test_golden_set.py`: labels valid, no split-spanning question, no article named in a question
- [x] Resumable embedding cache (`.cache/embeddings`, keyed by model, revision and texts)
- [x] Parser: drop `*` footnote marks, glue punctuation after a removed mark (107 chunks, text only)
- [x] Decision note: evaluation protocol (`docs/decisions/002-evaluation-protocol.md`)

---

## M2 Retrieval quality (weeks 3–4)

### Step 4: Hybrid retrieval, reranking, ablations

- [x] `docker-compose.yml` with Qdrant (`qdrant/qdrant:v1.19.2`); `make index` uploads the 3,799 chunks
- [x] `[fix]` Index by storage key `id@lang`; point ID = `uuid5(key)`; payload holds `key`, `id`, `law`, `lang` (R1): 3,799 points, EN and FR both kept
- [x] `[test]` `test_rrf`
- [x] `[test]` `test_bm25`
- [x] `[test]` `test_hybrid_end_to_end`
- [x] `[test]` `test_reranker_reorders`
- [x] `[test]` `test_store_failover`
- [x] `[test]` `test_gdpr_filter` (Qdrant in process in CI, plus the Docker server when it runs)
- [x] `retrieval/bm25.py`, `retrieval/fusion.py`
- [x] `retrieval/stores.py` (Numpy, Qdrant, Fallback)
- [x] `retrieval/hybrid.py`
- [ ] Optional: filter or boost by query language (not needed on dev: no failure came from the language, see `docs/failure_cases.md`)
- [x] Cross-encoder `bge-reranker-v2-m3` ablation (row D and F; 12 s/query on CPU, offline only)
- [x] `docs/ablations.md`: baseline, A to F, with ms/query
- [x] Error analysis of the dev questions → biggest cause: recitals above the article → fix: binding text first (rows E, F) → `docs/failure_cases.md`
- [x] Reach **Recall@5 ≥ 0.85** on dev: 0.925 with E (default) and F
- [x] Decision notes: fusion (003), rerank (004)
- [x] Embedding cache keyed by text, so subsets and edited passages reuse vectors (from the step 3 review)

---

## M3 Grounded generation (weeks 3–4)

### Step 5: Provider layer

- [x] Gemini and Groq keys in `.env` (`gemini-2.5-flash-lite` is closed to new users: `gemini-3.5-flash-lite`); Ollama `qwen3:4b` (optional, not installed)
- [x] `[test]` `test_openai_adapter_round_trip`
- [x] `[test]` `test_anthropic_adapter`
- [x] `[test]` `test_cache_hits_skip_provider`
- [x] `[test]` `test_retry_backoff` (`[fix]` inject `base_delay=1` and a fake sleep, R10)
- [x] `[test]` `test_fallback_chain`
- [x] `[test]` `test_factory_skips_unconfigured`
- [x] `llm/base.py`, `llm/openai_compat.py`, `llm/anthropic_adapter.py`
- [x] `llm/wrappers.py` (cache, retry, fallback)
- [x] `[fix]` Cache key includes model IDs and `max_tokens` (R4)
- [x] `[fix]` Serving profile fails over quickly (`max_tries=2`, a deadline through every layer) (R5, LLM side; the API side is in step 8)
- [x] `[fix]` No `temperature` for Anthropic: `anthropic` 1.x has none (R11)
- [x] `[fix]` The OpenAI-compatible adapter sends `max_tokens` (R12)
- [x] `[fix]` SDK clients with `max_retries=0`: one retry layer (R13)
- [x] `[fix]` An empty key or model skips a provider; an unknown name raises (R14)
- [x] `[fix]` Each failover is logged; each response records the model that answered (R15)
- [x] `llm/factory.py`
- [x] Script: the same prompt through Gemini, Groq (and Anthropic if you have credits), printing answer, tokens and latency (`make llm-smoke`)
- [x] Baseline answers with a plain prompt and no citation check (deferred from step 3): `evals/reports/baseline-dev-answers`, 22 dev answers

### Step 6: Cited answers, guardrails, prompts, judge

**6a (PR: cited answers, judge, review files)**

- [x] `answer.v1` prompt (in `src/actwise/prompts/`, shipped with the package so serving finds it from any directory)
- [x] `[test]` `test_extract_citations`
- [x] `[test]` `test_verify_flags_invented`
- [x] `[test]` `test_rag_strips_invented_citations` (+ a case where an invented `AIA-Art6` sits next to a valid `AIA-Art6-2`)
- [x] `[test]` `test_rag_refuses_in_user_language` (+ variants like `NOT_COVERED.`)
- [x] `[test]` `test_redact_pii`
- [x] `[test]` `test_injection_detection`
- [x] `generation/citations.py`, `generation/rag.py`, `generation/guardrails.py`
- [x] `[fix]` Strip only the exact bracketed invented IDs (R2)
- [x] `[fix]` Robust `NOT_COVERED` detection (R3)
- [x] `answer.v2` + A/B on today's dev set (22 questions): v2 answers partly covered questions, so false refusals go from 4 to 0 (`docs/generation.md`)
- [x] LLM judge prompt (score 1–5 + reason + unsupported citations, JSON) on `gpt-oss-120b` (Groq): Gemini 3.8 Flash is too slow and 3.6 Flash allows 20 requests a day
- [x] Citation precision, strict and lenient
- [x] `evals/make_synthetic.py`: 144 candidates (60 dev + 60 test in scope, 24 out of scope), screened by rule, pre-screened by Claude
- [x] `evals/make_calibration.py`: blind sheet of 58 answers (45 real, 13 with a planted unsupported claim)
- [x] Before the 150-question runs: honour `Retry-After` and Gemini's in-body `retryDelay`; evals use one provider, so a spent quota stops the run (skipping a spent provider while serving is in step 8)

**Your hand-off**

- [x] Score the 58 answers in `data/eval/human_labels.csv` (read them in `human_labels.md`); re-checked at the 3/4 boundary with one written rule
- [x] Confirm or override the keep / drop / fix marks in `data/eval/candidates.csv` (all 129 confirmed)

**6b (PR: calibrated judge, 150+ questions)**

- [x] Kappa between the judge and the human labels: **0.739** at faithful = 4–5 (0.952 at 5 only); `judge.v1` unchanged (decision 007)
- [x] Merge the kept candidates into `golden.jsonl` (`source: hand | synthetic`): 179 questions; dev 71 scored + 12 out of scope, test 78 + 12 (`evals/merge_candidates.py`)
- [x] Re-run the Step 4 ablations on the grown dev set; hand-written and synthetic reported separately (`docs/ablations.md`: E and F still lead)
- [x] Confirm the A/B winner on the grown dev set: **v2** (2.8 % false refusals against 7.0 %, faithfulness 0.971 against 0.992)
- [x] Hit the dev targets with v2: 0 invented · faithfulness 0.971 · citation precision 0.944 lenient · refusals 12/12 · kappa 0.739
- [ ] Plain baseline on the grown dev set: answers cached, the judge calls wait for Groq's daily tokens
- [ ] Optional: drop repeated passages from the context (parts of one paragraph, EN and FR copies: 11 of 110 slots on dev)
- [ ] Optional: `answer.v3` against v2's wrong "not covered" sentences (q061, q085)

---

## M4 Classifier agent and API (week 5)

### Step 7: Risk classifier agent

- [ ] `[test]` `test_happy_path`
- [ ] `[test]` `test_rejects_invented_citation`
- [ ] `[test]` `test_schema_errors_fed_back`
- [ ] `[test]` `test_plain_text_is_nudged`
- [ ] `[test]` `test_schema_has_no_titles`
- [ ] `agent/schemas.py`, `agent/classifier.py`
- [ ] 40 scenarios in `data/eval/risk_scenarios.jsonl`, each gold label checked against the article text; mark ambiguous ones
- [ ] Classifier eval: **≥ 85 %** non-ambiguous, **0** prohibited labelled minimal risk
- [ ] Note the AI Omnibus date (Reg. 2026/1744) for the model card

### Step 8: API and UI

- [ ] `[test]` `test_daily_cap_resets_next_day`
- [ ] `[test]` `test_extract_text`
- [ ] `[test]` `test_api_contract` (422 / 401 / 429 / 415)
- [ ] `[test]` `test_register_failure_is_ignored`
- [ ] `api/guards.py`, `api/main.py`, `ingest/files.py`
- [ ] `[fix]` One deadline per API request, passed to every `chat()` of `/ask` and `/classify` (R5, API side)
- [ ] Skip a provider whose quota is spent while serving (a `blocked_until` next to the throttle; from the step 6a review)
- [ ] `[fix]` Decide on the per-instance cap: document it or move it to Firestore (R6)
- [ ] `api/app.py` wiring (profiles: local, cloud)
- [ ] `make serve` + curl examples
- [ ] Optional: SSE streaming for `/ask`
- [ ] `ui/app.py` (Streamlit: ask tab + classify tab)

---

## M5 Own model and framework comparison (week 6)

### Step 9: Fine-tune and shrink the embedder

- [ ] ~800 train chunks → EN + FR questions (cached) → read 50, drop bad pairs → 1,000–1,600 pairs
- [ ] `[test]` `test_no_split_leakage`
- [ ] `[test]` `test_pooling_ignores_padding`
- [ ] `[test]` `test_onnx_parity` (slow, cosine ≥ 0.98)
- [ ] Train MiniLM-L12 on Colab/Kaggle (MNRL, 3 epochs, `max_seq_length=256`)
- [ ] Evaluate base vs FT on the **test** split with your own harness (hand-written and synthetic separately)
- [ ] Export to ONNX → int8 quantization; Recall@5 loss ≤ 1 point; record size and ms/query
- [ ] `retrieval/embedders.py` (SentenceTransformer, ONNX)
- [ ] Publish the int8 model and model card on the HF Hub
- [ ] `make index-cloud` → `index.npz` + Qdrant `actwise_ft_int8` (load `.env` in `retrieval/index.py`, so `QDRANT_URL` and `QDRANT_API_KEY` apply)

### Step 10: Frameworks (first to cut)

- [ ] `frameworks/llamaindex_pipeline.py` + smoke test
- [ ] `frameworks/langgraph_classifier.py` + smoke test
- [ ] `frameworks/COMPARISON.md` filled from measured numbers

---

## M6 Integrations and observability (week 7)

### Step 11: Integrations

- [ ] `[test]` `test_parse_command`
- [ ] `[test]` `test_format_classification`
- [ ] `[test]` `test_slack_handler`
- [ ] `[test]` `test_mcp_tools_registered`
- [ ] `[test]` `test_register_row`
- [ ] `[test]` `test_register_outage_ignored`
- [ ] `integrations/formatting.py`
- [ ] Slack app (Socket Mode, `/actwise`) + `integrations/slack_bot.py`
- [ ] `integrations/mcp_server.py` → MCP Inspector → desktop client
- [ ] Enable the Sheets and Drive APIs, service account, shared sheet + `integrations/sheets.py`
- [ ] Upload demo with a DOCX
- [ ] Screen captures: Slack, MCP, Sheets, upload

### Step 12: Observability

- [ ] `[test]` `test_observe_is_noop_without_langfuse`
- [ ] `[test]` `test_log_event_is_valid_json`
- [ ] `observability/tracing.py` (optional Langfuse); `@observe` on `ask` and `classify`
- [ ] Langfuse OpenAI drop-in inside `OpenAICompatLLM`; no input capture on `/classify`; `redact_pii`
- [ ] JSON structured logs, one line per request
- [ ] Cost per query at paid prices → README
- [ ] Trace screenshot in `docs/`

---

## M7 Production on Cloud Run (week 8)

### Step 13: Deploy

- [ ] Free-tier arithmetic re-checked on deploy day
- [ ] GCP project, enabled APIs, Artifact Registry `actwise` (europe-west1)
- [ ] Secrets: gemini, groq, qdrant, gsheets; grant `secretAccessor`
- [ ] **EUR 1 budget alert** (50 / 90 / 100 %)
- [ ] Qdrant Cloud cluster + `make index-cloud`
- [ ] `requirements-cloud.txt`, multi-stage `Dockerfile`, image **< 450 MB** compressed
- [ ] `deploy/env.yaml`
- [ ] Manual first deploy + smoke tests + cold start ≤ 15 s
- [ ] Workload Identity Federation for GitHub
- [ ] `.github/workflows/deploy.yml` (candidate revision → smoke test → traffic)
- [ ] Clean up old images after each deploy
- [ ] After a week: billing shows EUR 0.00 → screenshot

---

## M8 Hardening (week 9)

### Step 14: Safety, load, cost guardrails

- [ ] `data/eval/adversarial.jsonl`: 10 direct injection, 5 indirect, 8 out-of-scope, 7 legal-advice bait, 5 PII, 5 garbage
- [ ] Indirect-injection test with a poisoned chunk
- [ ] `docs/security.md` mapped to the OWASP LLM Top 10, plus the unmitigated risks
- [ ] Safety suite **≥ 95 %**
- [ ] `tests/load/locustfile.py` → p50/p95, error rate, RPS, instance count
- [ ] Drill: cap exhausted → 429 + UI message
- [ ] Drill: Gemini key removed → fallback logged
- [ ] Drill: Qdrant down → NumPy fallback
- [ ] `docs/model_card.md`

---

## M9 Showcase (week 10)

### Step 15

- [ ] README: pitch + GIF, live link + 3 questions, results table, architecture diagram, 3-command quickstart, eval method, decisions, limitations
- [ ] 2-minute demo video
- [ ] Blog post: "What broke when I built RAG on the EU AI Act"
- [ ] CV entry with **measured** numbers only
- [ ] Rehearse the interview answers
