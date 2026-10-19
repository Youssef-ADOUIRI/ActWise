# ActWise TODO

Milestones, targets and the code review are in [`docs/ROADMAP.md`](docs/ROADMAP.md).
Tick a box only when the work is **committed**. Commit after every step.
`[test]` marks a test to write first, and `[fix]` marks a correction to the guide's reference code (see ROADMAP §Engineering review).

---

## Before you start: accounts (all free)

- [ ] GitHub public repo `actwise`
- [ ] Google AI Studio: Gemini key in a project with **no billing account**
- [ ] Groq console key
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
- [ ] Push and confirm the CI badge is green
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

- [ ] `data/eval/splits.json`: 70/15/15 **by article**, seed 42
- [ ] 50 hand-written golden questions (≥ 15 FR; types lookup / definition / obligation / cross-law / not-covered)
- [ ] Naive baseline: 150-word windows, BGE-M3, cosine only
- [ ] `[test]` Metric tests (article dedup, MRR = 1/3, nDCG by hand)
- [ ] `src/actwise/evaluation/metrics.py`
- [ ] `[fix]` The runner leaves empty-gold questions out of retrieval metrics (R7)
- [ ] `evals/run_eval.py --split --profile --llm --slice`, writing a JSON report and a markdown summary
- [ ] `make eval-retrieval`
- [ ] Commit `evals/reports/baseline.json`

---

## M2 Retrieval quality (weeks 3–4)

### Step 4: Hybrid retrieval, reranking, ablations

- [ ] `docker-compose.yml` with Qdrant
- [ ] `[fix]` Index by storage key `id@lang`; point ID = `uuid5(key)`; payload holds `id`, `law`, `lang` (R1)
- [ ] `[test]` `test_rrf`
- [ ] `[test]` `test_bm25`
- [ ] `[test]` `test_hybrid_end_to_end`
- [ ] `[test]` `test_reranker_reorders`
- [ ] `[test]` `test_store_failover`
- [ ] `[test]` `test_gdpr_filter` (integration, Qdrant in Docker)
- [ ] `retrieval/bm25.py`, `retrieval/fusion.py`
- [ ] `retrieval/stores.py` (Numpy, Qdrant, Fallback)
- [ ] `retrieval/hybrid.py`
- [ ] Optional: filter or boost by query language
- [ ] Cross-encoder `bge-reranker-v2-m3` ablation
- [ ] `docs/ablations.md`: baseline, A, B, C, D, with ms/query
- [ ] Error analysis of the 20 worst dev questions → fix the biggest cause → `docs/failure_cases.md`
- [ ] Reach **Recall@5 ≥ 0.85** on dev
- [ ] Decision notes: fusion, rerank

---

## M3 Grounded generation (weeks 3–4)

### Step 5: Provider layer

- [ ] Gemini and Groq keys in `.env`; Ollama `qwen3:4b` (optional)
- [ ] `[test]` `test_openai_adapter_round_trip`
- [ ] `[test]` `test_anthropic_adapter`
- [ ] `[test]` `test_cache_hits_skip_provider`
- [ ] `[test]` `test_retry_backoff` (`[fix]` inject `base_delay=1` and a fake sleep, R10)
- [ ] `[test]` `test_fallback_chain`
- [ ] `[test]` `test_factory_skips_unconfigured`
- [ ] `llm/base.py`, `llm/openai_compat.py`, `llm/anthropic_adapter.py`
- [ ] `llm/wrappers.py` (cache, retry, fallback)
- [ ] `[fix]` Cache key includes model IDs and `max_tokens` (R4)
- [ ] `[fix]` Serving profile fails over quickly (`max_tries=2`, per-request deadline) (R5)
- [ ] `llm/factory.py`
- [ ] Script: the same prompt through Gemini, Groq (and Anthropic if you have credits), printing answer, tokens and latency

### Step 6: Cited answers, guardrails, prompts, judge

- [ ] `configs/prompts/answer.v1.md`
- [ ] `[test]` `test_extract_citations`
- [ ] `[test]` `test_verify_flags_invented`
- [ ] `[test]` `test_rag_strips_invented_citations` (+ a case where an invented `AIA-Art6` sits next to a valid `AIA-Art6-2`)
- [ ] `[test]` `test_rag_refuses_in_user_language` (+ variants like `NOT_COVERED.`)
- [ ] `[test]` `test_redact_pii`
- [ ] `[test]` `test_injection_detection`
- [ ] `generation/citations.py`, `generation/rag.py`, `generation/guardrails.py`
- [ ] `[fix]` Strip only the exact bracketed invented IDs (R2)
- [ ] `[fix]` Robust `NOT_COVERED` detection (R3)
- [ ] `answer.v2.md` + A/B on dev → record the winner
- [ ] LLM judge prompt (score 1–5 + reason, JSON)
- [ ] 60 human labels in `data/eval/human_labels.csv` → **kappa ≥ 0.6**
- [ ] Citation precision, strict and lenient
- [ ] `evals/make_synthetic.py`: 100 synthetic questions (~30 % FR), all reviewed by hand → 150 total
- [ ] Re-run the Step 4 ablations on 150 questions; report hand-written and synthetic separately
- [ ] Hit the dev targets: 0 invented · faithfulness ≥ 0.85 · citation precision ≥ 0.90 · refusals ≥ 95 %

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
- [ ] `make index-cloud` → `index.npz` + Qdrant `actwise_ft_int8`

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
