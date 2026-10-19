.PHONY: install lint test ingest index eval serve deploy deck

install:
	uv sync --extra local
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src

test:
	uv run pytest --cov=src --cov-fail-under=80

ingest:
	uv run python -m actwise.ingest.build_chunks

index:
	@echo "TODO step 4: embed chunks and upload to Qdrant"

eval:
	@echo "TODO step 3: run evals/run_eval.py"

serve:
	@echo "TODO step 8: uv run uvicorn actwise.api.app:app --reload"

deploy:
	@echo "TODO step 13: deploy to Cloud Run"

# Project decks: collect facts from the repo, then build the review and pipeline .pptx (needs Node 18+)
deck:
	uv run python docs/deck/collect.py --with-tests
	cd docs/deck && npm install --silent --no-audit --no-fund && npm run build --silent
