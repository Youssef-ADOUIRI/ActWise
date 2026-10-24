.PHONY: install lint test ingest splits index eval eval-retrieval eval-answers ablations llm-smoke \
	candidates label-sheet serve deploy

SYSTEM ?= baseline
SPLIT ?= dev
PROMPT ?= answer.v1

install:
	uv sync --extra local
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src evals

test:
	uv run pytest --cov=src --cov-fail-under=80

ingest:
	uv run python -m actwise.ingest.build_chunks

splits:
	uv run python -m actwise.evaluation.splits

# Needs Qdrant: docker compose up -d qdrant. Vectors come from the embedding cache.
index:
	uv run --extra local python -m actwise.retrieval.index

# Retrieval metrics on the golden set. First run downloads the embedder;
# vectors are cached in .cache/embeddings, so an interrupted run resumes.
eval-retrieval:
	uv run --extra local python evals/run_eval.py --system $(SYSTEM) --split $(SPLIT)

# Every row of docs/ablations.md; the reranked run takes minutes on a laptop CPU.
ablations:
	for system in baseline dense bm25 hybrid hybrid-rerank hybrid-binding hybrid-rerank-binding; do \
		uv run --extra local python evals/run_eval.py --system $$system --split $(SPLIT) || exit 1; \
	done

# Retrieval metrics plus an answer per question (PROMPT=plain|answer.v1|answer.v2), scored by
# the judge. Every LLM call is cached in .cache/llm, so a re-run makes no API call.
eval-answers:
	uv run --extra local python evals/run_eval.py --system $(SYSTEM) --split $(SPLIT) --prompt $(PROMPT) --judge

# Step 6 review files: golden-set candidates, and 60 answers to score by hand.
candidates:
	uv run python evals/make_synthetic.py

label-sheet:
	uv run python evals/make_calibration.py

eval: eval-retrieval

# One prompt through each LLM provider configured in .env, then through the cached chain.
llm-smoke:
	uv run python -m actwise.llm.smoke

serve:
	@echo "TODO step 8: uv run uvicorn actwise.api.app:app --reload"

deploy:
	@echo "TODO step 13: deploy to Cloud Run"
