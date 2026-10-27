.PHONY: install lint test ingest splits index eval eval-retrieval eval-answers ablations llm-smoke \
	candidates label-sheet eval-classifier serve ui deploy

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

# Risk classifier on the scenarios of SPLIT (agent calls cached in .cache/llm).
eval-classifier:
	uv run --extra local python evals/run_classifier.py --split $(SPLIT)

# Step 6 review files: golden-set candidates, and 60 answers to score by hand.
candidates:
	uv run python evals/make_synthetic.py

label-sheet:
	uv run python evals/make_calibration.py

eval: eval-retrieval

# One prompt through each LLM provider configured in .env, then through the cached chain.
llm-smoke:
	uv run python -m actwise.llm.smoke

# The API on http://localhost:8000 (try it at /docs). BGE-M3 takes about 2 GB of RAM.
serve:
	uv run --extra local uvicorn actwise.api.app:app --port 8000

# The Streamlit UI; it calls the API at ACTWISE_API_URL, so start `make serve` first.
ui:
	uv run --extra ui streamlit run ui/app.py

deploy:
	@echo "TODO step 13: deploy to Cloud Run"
