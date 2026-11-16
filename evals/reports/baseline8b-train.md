# Retrieval report: baseline8b-train

E: as C, with articles and annexes ranked before recitals. Split `train`, 19 scored questions (0 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.342 |
| **Recall@5** | **0.868** [0.71, 1.00] |
| Recall@10 | 0.921 |
| Recall@20 | 0.974 |
| MRR@10 | 0.580 [0.43, 0.74] |
| nDCG@10 | 0.661 |
| ms / query | 173 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.808 | 0.559 |
| fr | 6 | 1.000 | 0.625 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| definition | 2 | 1.000 | 0.750 |
| lookup | 5 | 1.000 | 0.617 |
| obligation | 12 | 0.792 | 0.536 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 6 | 1.000 | 0.639 |
| hard | 13 | 0.808 | 0.553 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q046 (fr) | AIA-AnnexIII, AIA-Art6 | 2 | AIA-Art25, AIA-Art6, AIA-Art9 |
| q047 (en) | AIA-Art50 | 2 | AIA-Art14, AIA-Art50, AIA-Art78 |
| q049 (fr) | GDPR-Art4 | 2 | GDPR-Art25, GDPR-Art4, GDPR-Art93 |
| h001 (en) | AIA-Art2, AIA-Art99 | 2 | AIA-Art100, AIA-Art99, AIA-Art3 |
| h012 (fr) | GDPR-Art17 | 2 | GDPR-Art47, GDPR-Art17, GDPR-Art61 |
| q050 (en) | AIA-Art113 | 3 | AIA-Art5, AIA-Art111, AIA-Art113 |
| h008 (en) | AIA-Art6, AIA-AnnexIII | 3 | AIA-AnnexIV, AIA-AnnexXII, AIA-AnnexIII |
| h003 (fr) | AIA-Art2 | 4 | AIA-Art82, AIA-Art3, AIA-Art9 |
| h004 (en) | AIA-Art22 | 4 | AIA-Art49, AIA-Art24, AIA-Art25 |
| h010 (en) | AIA-Art99 | 4 | AIA-Art100, AIA-Art101, AIA-Art57 |
| h002 (en) | AIA-Art2 | 10 | AIA-Art50, AIA-Art53, AIA-Art41 |
| h013 (en) | GDPR-Art9 | 20 | AIA-Art5, AIA-Art99, AIA-Art70 |

## Answers: `answer.v2`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 19 |
| in_scope | 19 |
| out_of_scope | 0 |
| refusal_rate | None |
| false_refusal_rate | 0.3684 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 1.0 |
| gold_in_context | 0.7895 |
| gold_cited | 0.6316 |
| citation_precision_lenient | 1.0 |
| faithfulness | 0.9583 |
| fully_supported | 0.9167 |
| faithfulness_ci95 | (0.875, 1.0) |
| judged | 12 |
| judge_failed | 0 |
| uncited_sentences | 1.0 |
| input_tokens | 18754 |
| output_tokens | 1595 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 6 | None | 0.3333 | 1.0 | 1.0 |
| hard | 13 | None | 0.3846 | 0.9375 | 0.875 |

### q045 (en, definition)

**Question:** Who counts as a deployer of an AI system?

**Answer** (gemini-3.5-flash-lite):

> A ‘deployer’ is defined as a natural or legal person, public authority, agency, or other body using an AI system under its authority, except when the AI system is used in the course of a personal non-professional activity [AIA-Art3-4].

Judge: 5/5. The answer accurately reflects the definition of 'deployer' as given in the cited source.

### q046 (fr, lookup)

**Question:** Un logiciel d'IA qui trie automatiquement les CV des candidats est-il un système d'IA à haut risque ?

**Answer** (refused (uncited)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.

### q047 (en, obligation)

**Question:** Do people have to be told when they are chatting with an AI system rather than a human?

**Answer** (gemini-3.5-flash-lite):

> Yes, providers must ensure that AI systems intended to interact directly with natural persons are designed and developed so that the people concerned are informed they are interacting with an AI system [AIA-Art50-1]. However, this obligation does not apply if it is obvious from the point of view of a reasonably well-informed, observant, and circumspect person, taking into account the circumstances and context of use, nor does it apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences (unless those systems are available for the public to report a criminal offence) [AIA-Art50-1].

Judge: 5/5. All statements are directly supported by Article 50(1) as cited.

### q048 (en, lookup)

**Question:** When can I ask a company to delete the personal data it holds about me?

**Answer** (gemini-3.5-flash-lite):

> You have the right to obtain the erasure of personal data concerning you from the controller without undue delay when one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) you withdraw consent on which the processing is based (according to point (a) of Article 6(1) or point (a) of Article 9(2)) and there is no other legal ground for the processing; (c) you object to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or you object to the processing pursuant to Article 21(2); or (d) the personal data have been unlawfully processed [GDPR-Art17-1].
>
> Please note that the provided sources do not cover the complete text for ground (e) or any subsequent grounds listed under Article 17(1) [GDPR-Art17-1].
>
> *Note: This is legal information, not legal advice.*

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR Article 17(1) source.

### q049 (fr, definition)

**Question:** Qu'est-ce que la pseudonymisation au sens du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Au sens du règlement (UE) n° 2016/679 (RGPD), la «pseudonymisation» désigne le traitement de données à caractère personnel de telle façon que celles-ci ne puissent plus être attribuées à une personne concernée précise sans avoir recours à des informations supplémentaires [GDPR-Art4-5]. Pour ce faire, ces informations supplémentaires doivent être conservées séparément et soumises à des mesures techniques et organisationnelles afin de garantir que les données à caractère personnel ne sont pas attribuées à une personne physique identifiée ou identifiable [GDPR-Art4-5].

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR Article 4(5) definitions.

### q050 (en, lookup)

**Question:** From what date do the AI Act's bans on prohibited AI practices apply?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h001 (en, obligation)

**Question:** Can a non-EU startup with no office or presence in Europe face fines under the EU AI Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h002 (en, obligation)

**Question:** Do I have to comply with the AI Act if I use an AI image generator at home for fun?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h003 (fr, obligation)

**Question:** Une armée qui développe un système d'IA uniquement pour la défense doit-elle respecter le règlement sur l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Le présent règlement ne s'applique pas aux systèmes d'IA si et dans la mesure où ils sont mis sur le marché, mis en service ou utilisés avec ou sans modifications exclusivement à des fins militaires, de défense ou de sécurité nationale, quel que soit le type d'entité exerçant ces activités [AIA-Art2-3]. Les sources ne précisent pas d'autres aspects du régime juridique applicable à ce système d'IA en dehors de cette exclusion du champ d'application.

Judge: 5/5. All statements in the answer are directly supported by the cited source.

### h004 (en, obligation)

**Question:** A US company with no office in Europe wants to sell a high-risk AI system there. Who does it need to name in the EU before it can?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h005 (en, obligation)

**Question:** Our website chatbot answers customers. Do we have to tell them they are not chatting with a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. However, this obligation does not apply if it is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use, or if the system is authorised by law to detect, prevent, investigate or prosecute criminal offences (unless available for the public to report a criminal offence) [AIA-Art50-1].
>
> The provided sources do not cover whether your specific website chatbot meets the criteria of being "obvious" to a reasonably well-informed, observant, and circumspect person in your particular context of use.
>
> You give legal information, not legal advice. Never say whether a specific company or system is compliant.

Judge: 5/5. All claims are directly supported by the cited source AIA-Art50-1.

### h006 (fr, obligation)

**Question:** Si notre média publie une fausse vidéo d'un homme politique créée avec une IA, devons-nous le signaler ?

**Answer** (gemini-3.5-flash-lite):

> Oui, en tant que déployeurs d’un système d’IA qui génère ou manipule des images ou des contenus audio ou vidéo constituant un hypertrucage, vous devez indiquer que les contenus ont été générés ou manipulés par une IA [AIA-Art50-4].
>
> Les sources fournies ne précisent pas les sanctions applicables en cas de non-respect de cette obligation.

Judge: 5/5. All statements are directly supported by the cited source and no unsupported citations are present.

### h007 (en, obligation)

**Question:** Is an AI tool that only fixes spelling mistakes in job ads high-risk just because it is used in hiring?

**Answer** (gemini-3.5-flash-lite):

> An AI system referred to in Annex III—which includes AI systems intended to be used for the recruitment or selection of natural persons, specifically to place targeted job advertisements—shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making [AIA-AnnexIII-4, AIA-Art6-3]. This exception applies if the AI system is intended to perform a narrow procedural task, is intended to improve the result of a previously completed human activity, is intended to detect decision-making patterns or deviations from prior decision-making patterns without replacing or influencing the previously completed human assessment without proper human review, or is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III [AIA-Art6-3].
>
> The provided sources do not cover whether fixing spelling mistakes in job ads specifically fulfills these exemption conditions.

Judge: 5/5. All claims are supported by the cited sources.

### h008 (en, obligation)

**Question:** Is software that scores how likely someone is to repay a loan subject to extra rules under the AI Act?

**Answer** (gemini-3.5-flash-lite):

> AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score (with the exception of AI systems used for the purpose of detecting financial fraud) are classified as high-risk AI systems [AIA-AnnexIII-5].
>
> The sources do not cover what specific extra rules apply to these high-risk AI systems under the AI Act.

Judge: 5/5. All claims are directly supported by the cited source.

### h009 (fr, lookup)

**Question:** Quelle amende risque une entreprise qui donne des informations fausses aux autorités sur son système d'IA ?

**Answer** (gemini-3.5-flash-lite):

> Une entreprise qui fournit des informations inexactes, incomplètes ou trompeuses aux organismes notifiés ou aux autorités nationales compétentes en réponse à une demande s'expose à une amende administrative pouvant aller jusqu'à 7 500 000 EUR ou jusqu'à 1 % de son chiffre d'affaires annuel mondial total réalisé au cours de l'exercice précédent, le montant le plus élevé étant retenu [AIA-Art99-5].

Judge: 5/5. The answer's claim is fully supported by source AIA-Art99-5.

### h010 (en, lookup)

**Question:** Are AI Act fines lower for a small startup than for a big company?

**Answer** (gemini-3.5-flash-lite):

> In the case of SMEs, including start-ups, each fine referred to in Article 99 shall be up to the percentages or amount referred to in paragraphs 3, 4, and 5 of that article, whichever thereof is lower [AIA-Art99-6]. The provided sources do not cover whether fines are lower for a small startup under provisions outside of Article 99, such as those for general-purpose AI models or Union institutions.
>
> You give legal information, not legal advice. Never say whether a specific company or system is compliant.

Judge: 5/5. All claims are directly supported by the cited source and the statement about source coverage is accurate.

### h011 (en, obligation)

**Question:** We only resell an AI system that another company built. Do we have anything to check before selling it?

**Answer** (gemini-3.5-flash-lite):

> Before making a high-risk AI system available on the market, distributors shall verify that it bears the required CE marking, that it is accompanied by a copy of the EU declaration of conformity referred to in Article 47 and instructions for use, and that the provider and the importer of that system, as applicable, have complied with their respective obligations as laid down in Article 16, points (b) and (c) and Article 23(3) [AIA-Art24-1].
>
> The sources do not cover whether these obligations apply if you are reselling an AI system that is not classified as high-risk.

Judge: 3/5. The answer correctly cites the distributor obligations for high‑risk AI, but incorrectly claims the sources do not address obligations for non‑high‑risk reselling, which is contradicted by other provided articles.

### h012 (fr, obligation)

**Question:** Une entreprise peut-elle refuser d'effacer mes données parce que la loi l'oblige à les conserver ?

**Answer** (refused (not_covered)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.

### h013 (en, obligation)

**Question:** Can a gym scan members' fingerprints at the entrance without asking them?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.
