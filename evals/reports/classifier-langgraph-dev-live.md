# Classifier report: classifier-langgraph-dev

Classifier `langgraph`, prompt `classify_rule.v1`, retrieval `hybrid-binding`, split `dev`: 20 scenarios (17 clear, 3 ambiguous).

Scored again from the saved runs on 2026-11-12, at commit `afe4c97`; no model was called.

| Metric | Value |
|---|---|
| **Accuracy, clear scenarios** | **0.9412** |
| Accuracy, ambiguous scenarios | 1.0 |
| **Recall, prohibited (all scenarios)** | **1.0** (4 of 4) |
| **Recall, high risk (all scenarios)** | **1.0** (6 of 6) |
| Prohibited labelled minimal risk | 0 |
| Prohibited or high risk labelled minimal risk | 0 |
| Runs that hit the step budget | 0 |
| Steps / lookups (reads and searches) per run | 2.9 / 3.75 |
| Seconds / input tokens per run | 12.743 / 11312 |
| Accuracy by language (clear) | {'en': 0.9167, 'fr': 1.0} |

## Confusion matrix (all scenarios: gold rows, predicted columns)

In the first two rows, a count right of the diagonal is an under-classified system, except in `needs_more_info`, which asks for the missing facts. Failed runs are not in the matrix.

| Gold \ predicted | prohibited | high_risk | transparency_only | minimal_risk | needs_more_info |
|---|---|---|---|---|---|
| **prohibited** | 4 | 0 | 0 | 0 | 0 |
| **high_risk** | 0 | 6 | 0 | 0 | 0 |
| **transparency_only** | 0 | 0 | 3 | 0 | 0 |
| **minimal_risk** | 0 | 1 | 0 | 4 | 0 |
| **needs_more_info** | 0 | 0 | 0 | 0 | 2 |

## Misses

| Scenario | Gold | Predicted | Reasons |
|---|---|---|---|
| s29 | minimal_risk | high_risk | The described AI system simply converts CVs into a structured form without ranking, scoring, or profiling candidates. It does not engage in any of the prohibited practices listed in Article 5(1). / Das beschriebene KI-System wird im Personalwesen eingesetzt, um Lebensläufe in strukturierte Formate zu konvertieren. Auch wenn das System keine Kandidaten bewertet, einstuft oder profiliert, fällt es unter den Anwendungsbereich von Anhang III Nummer 4 Buchstabe a, da es zur Filterung und Analyse von Bewerbungen im Rahmen der Personalbeschaffung verwendet wird, und ist somit gemäß Artikel 6 Absatz 2 als Hochrisiko-KI-System einzustufen (es sei denn, eine Ausnahme nach Artikel 6 Absatz 3 greift, wobei hier kein Ausschluss allein durch das Fehlen von Ranking/Scoring vorliegt, da es sich um eine filternde/analysierende Tätigkeit im Rekrutierungskontext handelt). |
