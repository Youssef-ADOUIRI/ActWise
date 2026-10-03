# Changelog

What changed, when, and why, file by file. Newest first.
Add a section for every step you commit.

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
