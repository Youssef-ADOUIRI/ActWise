# ActWise

![ci](https://github.com/Youssef-ADOUIRI/actwise/actions/workflows/ci.yml/badge.svg)

Ask the EU AI Act and GDPR in English or French and get answers with article-level citations, or classify an AI system into its AI Act risk tier.

## Quickstart

```bash
cp .env.example .env
make install
make test
make eval-retrieval SYSTEM=hybrid-binding  # dev metrics; the first run embeds the chunks (~30 min on a CPU)
docker compose up -d qdrant && make index  # optional: the same vectors in Qdrant
make llm-smoke                             # one prompt through each LLM provider set in .env
make eval-answers SYSTEM=hybrid-binding PROMPT=answer.v2  # cited answers, scored by the judge
```

## API and UI

```bash
make serve   # the API on http://localhost:8000; try it at /docs. Loads BGE-M3 (~2 GB of RAM)
make ui      # the Streamlit UI, in another terminal
```

```bash
curl localhost:8000/health
curl "localhost:8000/search?q=social+scoring&top_k=3"
curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "Which AI practices are prohibited?", "lang": "en"}'
curl -X POST localhost:8000/classify -H "Content-Type: application/json" \
  -d '{"description": "A bank scores the creditworthiness of people who apply for a loan."}'
curl -X POST localhost:8000/upload -F "file=@description.docx"  # .txt, .md, .pdf or .docx
```

With `ACTWISE_API_KEY` set, every route except `/health` needs the header `X-API-Key`. `MAX_DAILY_REQUESTS` caps the requests that reach a model; after the cap, the API answers 429 until the next day ([decision 009](docs/decisions/009-api.md)).

Retrieval results: [docs/ablations.md](docs/ablations.md) · Answer quality: [docs/generation.md](docs/generation.md).

Plan: [docs/ROADMAP.md](docs/ROADMAP.md) · Tasks: [TODO.md](TODO.md) · Changes: [docs/CHANGELOG.md](docs/CHANGELOG.md)

Legal text source: [EUR-Lex](https://eur-lex.europa.eu).
