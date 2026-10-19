# Project decks

Two living decks, rebuilt from the repo so they always match it.

| Deck | What it is | Built by |
|---|---|---|
| `ActWise_Project_Review.pptx` | Status, metrics, findings, risks and next steps; updated after every step or major finding | `build_deck.js` |
| `ActWise_Pipeline.pptx` | The end-to-end pipeline, stage by stage, with diagrams and explanations | `build_pipeline.js` |

| File | Role | Edited by hand? |
|---|---|---|
| `content.json` | Narrative for the review deck, plus `pipeline.stages` (built / in_progress / planned) for the pipeline deck | Yes |
| `facts.json` | Measured facts: corpus stats, TODO progress, decision records, eval reports, tests, latest commit | No, written by `collect.py` |
| `collect.py` | Reads the repo and writes `facts.json` (standard library only) | No |
| `common.js` | Shared palette, fonts, layouts and drawing helpers | Only to restyle |
| `build_deck.js`, `build_pipeline.js` | Turn the JSON files into the two `.pptx` files (pptxgenjs) | Only to change a layout |
| `assets/icons/` | Lucide icons (ISC licence) rendered to PNG | No |

## Update the decks

1. Edit `content.json`:
   - review deck: bump `meta.iteration`, `meta.date`, `meta.trigger`, `meta.stage`; fill `baseline` / `current` and `status` in the scorecards; move hypotheses to `supported` or `rejected` with a `result`; add findings, risks, next steps and a line in `iteration_log.entries`;
   - pipeline deck: set each stage in `pipeline.stages` to `built`, `in_progress` or `planned`. Boxes on every diagram change colour to match.
2. Run `make deck` from the repo root. It runs `collect.py --with-tests`, then builds both decks.
3. Commit `content.json`, `facts.json` and both `.pptx` files with the step.

Without make: `uv run python docs/deck/collect.py --with-tests`, then `cd docs/deck && npm install && npm run build`. Needs Node 18 or newer.

## Conventions

- Tokens such as `{chunks}`, `{coverage}`, `{units_pct}`, `{windowed_pct}`, `{m0_done}` are filled from `facts.json`, so numbers in the text never drift from the data.
- Status words: `done`, `built`, `in_progress`, `planned`, `met`, `not_met`, `not_measured`, `partial`, `fixed`, `open`, `untested`, `supported`, `rejected`, `mitigated`, `watch`.
- A status changes only with a measured number behind it.
- Speaker notes live in each section's `notes` field (review deck) or next to each slide in `build_pipeline.js`.
- Walkthrough slides in the pipeline deck are labelled illustrative until the pipeline runs; replace them with measured runs when it does.
