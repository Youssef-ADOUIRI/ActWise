# ActWise model card

The full model card comes in step 14. This page starts with the limitations that every user of the answers and the classifier must know.

## Limitations

- **The corpus is the 2024 text of the AI Act (Regulation (EU) 2024/1689) and the GDPR, as published on EUR-Lex** (`data/raw/SOURCES.md`). Later amendments are not included.
- **The AI Omnibus is not in the corpus.** Regulation (EU) 2026/1744 was published in the Official Journal on 24 July 2026 and entered into force on 27 July 2026. It moves the application dates of the high-risk obligations:
  - from 2 August 2026 to **2 December 2027** for the stand-alone systems of Annex III;
  - to **2 August 2028** for systems in products covered by Annex I.
  - Article 50's transparency duties and the general-purpose AI rules applied as scheduled, from 2 August 2026.
  - The rules that decide a system's risk tier did not change, so the classifier's tiers still hold. Its sources cannot say *when* each obligation applies. These dates come from secondary sources ([White & Case](https://www.whitecase.com/insight-alert/eu-ai-omnibus-enters-force-amending-ai-act), [FPF timeline](https://fpf.org/wp-content/uploads/2026/07/FPF-EU-AI-Act-Timeline-2026-R2.pdf)); EUR-Lex refused scripted access when this page was written.
- **Legal information, not legal advice.** The answers and classifications cite the text but do not judge a specific company's compliance. The API returns every answer and classification with the notice "Information only, not legal advice."
- **The classifier was tuned on 20 dev scenarios** (17 clear, 3 ambiguous) and gets all of them right ([classifier-dev](../evals/reports/classifier-dev.md)). That is a small sample: the 20 test scenarios are scored once, at the end of the project. It only knows the tier rules of the 2024 text, and a description without the deciding facts gets `needs_more_info` with questions, not a guess.
- **Measured quality (dev split):** see [generation.md](generation.md) for answers, [ablations.md](ablations.md) for retrieval and [decision 008](decisions/008-classifier.md) for the classifier. Test-split numbers are reported once, at the end of the project.
