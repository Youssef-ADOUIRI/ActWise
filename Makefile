.PHONY: install lint test ingest splits index eval eval-retrieval ablations serve deploy

SYSTEM ?= baseline
SPLIT ?= dev

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

eval: eval-retrieval

serve:
	@echo "TODO step 8: uv run uvicorn actwise.api.app:app --reload"

deploy:
	@echo "TODO step 13: deploy to Cloud Run"
