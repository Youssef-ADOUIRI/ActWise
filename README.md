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

Retrieval results: [docs/ablations.md](docs/ablations.md) · Answer quality: [docs/generation.md](docs/generation.md).

Plan: [docs/ROADMAP.md](docs/ROADMAP.md) · Tasks: [TODO.md](TODO.md) · Changes: [docs/CHANGELOG.md](docs/CHANGELOG.md)

Legal text source: [EUR-Lex](https://eur-lex.europa.eu).
