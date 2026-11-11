# Classifier report: classifier-langgraph-dev

Classifier `langgraph`, prompt `classify_rule.v1`, retrieval `hybrid-binding`, split `dev`: 20 scenarios (17 clear, 3 ambiguous).

| Metric | Value |
|---|---|
| **Accuracy, clear scenarios** | **0.9412** |
| Accuracy, ambiguous scenarios | 1.0 |
| Prohibited labelled minimal risk | 0 |
| Prohibited or high risk labelled minimal risk | 0 |
| Runs that hit the step budget | 0 |
| Steps / lookups (reads and searches) per run | 2.9 / 3.75 |
| Seconds / input tokens per run | 0.006 / 11312 |
| Accuracy by language (clear) | {'en': 0.9167, 'fr': 1.0} |

## Confusion (clear scenarios: gold → predicted)

- **prohibited**: {'prohibited': 4}
- **high_risk**: {'high_risk': 5}
- **transparency_only**: {'transparency_only': 3}
- **minimal_risk**: {'minimal_risk': 2, 'high_risk': 1}
- **needs_more_info**: {'needs_more_info': 2}

## Misses

| Scenario | Gold | Predicted | Reasons |
|---|---|---|---|
| s29 | minimal_risk | high_risk | The described AI system simply converts CVs into a structured form without ranking, scoring, or profiling candidates. It does not engage in any of the prohibited practices listed in Article 5(1). / Das beschriebene KI-System wird im Personalwesen eingesetzt, um Lebensläufe in strukturierte Formate zu konvertieren. Auch wenn das System keine Kandidaten bewertet, einstuft oder profiliert, fällt es unter den Anwendungsbereich von Anhang III Nummer 4 Buchstabe a, da es zur Filterung und Analyse von Bewerbungen im Rahmen der Personalbeschaffung verwendet wird, und ist somit gemäß Artikel 6 Absatz 2 als Hochrisiko-KI-System einzustufen (es sei denn, eine Ausnahme nach Artikel 6 Absatz 3 greift, wobei hier kein Ausschluss allein durch das Fehlen von Ranking/Scoring vorliegt, da es sich um eine filternde/analysierende Tätigkeit im Rekrutierungskontext handelt). |
