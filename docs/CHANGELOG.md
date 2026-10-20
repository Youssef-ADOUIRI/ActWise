# Changelog

What changed, when, and why, file by file. Newest first.
Add a section for every step you commit.

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
