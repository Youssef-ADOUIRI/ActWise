# 002: Evaluation protocol: article splits, golden set, article-level metrics

- **Options:** split chunks or articles at random; allocate questions in proportion to split size or on purpose; label gold paragraphs or gold articles; report bare means or means with intervals.
- **Measured:** 578 units (recitals, articles, annexes) split 404 / 87 / 87 with seed 42. A proportional 70/15/15 allocation of 50 questions would leave about 8 in dev, so a single miss would move Recall@5 by 0.12. Bootstrap intervals on 20 questions are still about ±0.20 wide.
- **Chosen:** split by article before writing any question. Write 20 scored questions for dev, 20 for test and 6 for train, plus 4 out-of-scope questions with an explicit dev/test split. Gold labels are articles, and metrics deduplicate retrieved chunks to articles over a pool of 50 passages. Every headline number carries a 95 % bootstrap interval.
- **Why:** splitting by article keeps one article's paragraphs out of two splits, so fine-tuning pairs (step 9) cannot leak into dev or test. Article-level gold is what a reviewer can check by hand. The intervals stop a 0.05 difference between configs from being read as a real gain.
- **Revisit if:** the synthetic questions of step 6 bring dev and test to 50+ questions each. The intervals then narrow, and the proportional allocation becomes acceptable.

Rules enforced by `tests/test_golden_set.py`:

| Rule | Why |
|---|---|
| Gold ids are article-level and exist in the corpus | A typo in a label silently zeroes a question |
| A question's gold articles all sit in one split | Otherwise it belongs to no split |
| Only `not_covered` questions have empty gold, and they carry a `split` | They have nothing to retrieve; they are scored on refusals in step 6 |
| Cross-law questions cite both laws | That is what makes them cross-law |
| No question names its article ("Article 6", "Annex III") | It would make retrieval trivially easy |
| ≥ 50 questions, ≥ 15 in French, ≥ 20 scored in dev and in test | The minimum the guide asks for, plus usable split sizes |

Side effect of the seeded draw: the best-known provisions (AI Act Articles 3, 6, 50, 113 and Annex III; GDPR Articles 4, 6, 9, 17, 35) all landed in train. So dev and test questions target less famous articles, which makes the evaluation harder but not biased: the split was fixed before any question was written.

## Revisited in step 6b: the set grows to 179 questions

- **Options:** spread 100 synthetic questions over train, dev and test (about 70/15/15, as the guide says), or put them all in dev and test.
- **Measured:**
  - The guide's spread would leave dev with about 35 scored questions and 2 out-of-scope ones. Train questions are never scored.
  - 144 candidates were drafted from seeded dev and test paragraphs and from 24 out-of-scope topics. They were screened by rule, pre-screened by Claude and confirmed by a person; 129 were kept.
- **Chosen:**
  - In scope: 51 dev and 58 test synthetic questions, each from one article or annex paragraph of its split.
  - Out of scope: 10 dev and 10 test questions, so the 95 % refusal target can be measured.
  - Every line now has a `source` field (`hand` or `synthetic`), and every report breaks its numbers down by source.
- **Result:** dev has 71 scored and 12 out-of-scope questions, test has 78 and 12, and 67 of the 179 questions are in French.
- **Caveat:** each synthetic question is written from a single passage. That makes it easier for retrieval than a hand-written one, so hand-written and synthetic results are reported apart.
