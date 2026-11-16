# Retrieval report: v3-train

E: as C, with articles and annexes ranked before recitals. Split `train`, 19 scored questions (0 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.342 |
| **Recall@5** | **0.868** [0.71, 1.00] |
| Recall@10 | 0.921 |
| Recall@20 | 0.974 |
| MRR@10 | 0.580 [0.43, 0.74] |
| nDCG@10 | 0.661 |
| ms / query | 143 |

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

## Answers: `answer.v3`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 19 |
| in_scope | 19 |
| out_of_scope | 0 |
| refusal_rate | None |
| false_refusal_rate | 0.0526 |
| retried | 6 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.9565 |
| gold_in_context | 1.0 |
| gold_cited | 0.9474 |
| citation_precision_lenient | 0.9565 |
| faithfulness | 0.9722 |
| fully_supported | 0.9444 |
| faithfulness_ci95 | (0.9167, 1.0) |
| judged | 18 |
| judge_failed | 0 |
| uncited_sentences | 0.78 |
| input_tokens | 29714 |
| output_tokens | 2314 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 6 | None | 0.0 | 0.9167 | 0.8333 |
| hard | 13 | None | 0.0769 | 1.0 | 1.0 |

### q045 (en, definition)

**Question:** Who counts as a deployer of an AI system?

**Answer** (gemini-3.5-flash-lite):

> A ‘deployer’ is defined as any natural or legal person, public authority, agency or other body using an AI system under its authority, except when the AI system is used in the course of a personal non-professional activity [AIA-Art3-4]. The provided sources do not cover whether any other entities or specific conditions outside of this definition qualify as a deployer.

Judge: 5/5. All statements are directly supported by the cited definition and the lack of additional coverage in the sources.

### q046 (fr, lookup)

**Question:** Un logiciel d'IA qui trie automatiquement les CV des candidats est-il un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> Oui, un système d'IA destiné à être utilisé pour analyser et filtrer les candidatures et évaluer les candidats dans le cadre du recrutement ou de la sélection de personnes physiques est considéré comme un système d'IA à haut risque, car il relève des systèmes d'IA visés à l'annexe III dans le domaine de l'emploi et de la gestion de la main-d'œuvre [AIA-AnnexIII-4, AIA-Art6-2].
>
> Cependant, les sources ne précisent pas si ce système peut échapper à cette qualification de haut risque par dérogation (notamment s'il ne présente pas de risque important de préjudice ou s'il remplit l'une des conditions prévues à l'article 6, paragraphe 3) [AIA-Art6-3].

Judge: 3/5. The answer correctly cites Annex III and Article 6(2) for the high‑risk classification, but incorrectly states that Article 6(3) does not address possible derogations, which it actually does.

### q047 (en, obligation)

**Question:** Do people have to be told when they are chatting with an AI system rather than a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. This obligation does not apply if it is obvious from the point of view of a reasonably well-informed, observant, and circumspect natural person, taking into account the circumstances and the context of use [AIA-Art50-1]. Furthermore, this obligation does not apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence [AIA-Art50-1]. The provided sources do not cover whether specific exceptions apply to other types of public services or non-criminal contexts.

Judge: 5/5. All statements are directly supported by the cited source AIA-Art50-1.

### q048 (en, lookup)

**Question:** When can I ask a company to delete the personal data it holds about me?

**Answer** (gemini-3.5-flash-lite):

> You have the right to obtain the erasure of personal data concerning you from the controller without undue delay when one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) you withdraw consent on which the processing is based, and there is no other legal ground for the processing; (c) you object to the processing and there are no overriding legitimate grounds for the processing, or you object to processing under Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data must be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; or (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1) [GDPR-Art17-1]. The provided sources do not cover whether any other conditions or exceptions apply beyond these specific grounds.

Judge: 5/5. All claims in the answer are directly supported by GDPR Article 17(1) source.

### q049 (fr, definition)

**Question:** Qu'est-ce que la pseudonymisation au sens du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Au sens du RGPD, la « pseudonymisation » désigne le traitement de données à caractère personnel de telle façon que celles-ci ne puissent plus être attribuées à une personne concernée précise sans avoir recours à des informations supplémentaires [GDPR-Art4-5]. Pour ce faire, ces informations supplémentaires doivent être conservées séparément et soumises à des mesures techniques et organisationnelles afin de garantir que les données à caractère personnel ne sont pas attribuées à une personne physique identifiée ou identifiable [GDPR-Art4-5].

Judge: 5/5. All statements are directly supported by the cited GDPR article.

### q050 (en, lookup)

**Question:** From what date do the AI Act's bans on prohibited AI practices apply?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, Chapters I and II of the Regulation—which include the provisions on prohibited AI practices (Articles 1 through 5)—shall apply from 2 February 2025 [AIA-Art113]. The provided sources do not cover the application dates for any specific bans outside of what is established for Chapter II as a whole.

Judge: 5/5. All statements in the answer are directly supported by the cited source.

### h001 (en, obligation)

**Question:** Can a non-EU startup with no office or presence in Europe face fines under the EU AI Act?

**Answer** (gemini-3.5-flash-lite):

> Yes, providers and deployers of AI systems that have their place of establishment or are located in a third country can fall within the scope of the EU AI Act where the output produced by the AI system is used in the Union, and providers placing general-purpose AI models or AI systems on the market or putting them into service in the Union are covered irrespective of whether they are established within the Union or in a third country [AIA-Art2-1]. Furthermore, non-compliance with certain provisions by operators is subject to administrative fines of up to EUR 15 000 000 or, for undertakings, up to 3 % of total worldwide annual turnover for the preceding financial year, and Member States must lay down rules on penalties for infringements by operators that take into account the interests of SMEs, including start-ups, and their economic viability [AIA-Art99-4, AIA-Art99-1]. The provided sources do not cover whether the specific startup in question would actually be fined in a given scenario.

Judge: 5/5. All claims are directly supported by the cited sources.

### h002 (en, obligation)

**Question:** Do I have to comply with the AI Act if I use an AI image generator at home for fun?

**Answer** (gemini-3.5-flash-lite):

> The AI Act does not apply to obligations of deployers who are natural persons using AI systems in the course of a purely personal non-professional activity [AIA-Art2-10].

Judge: 5/5. The answer's claim is directly supported by the cited source.

### h003 (fr, obligation)

**Question:** Une armée qui développe un système d'IA uniquement pour la défense doit-elle respecter le règlement sur l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Non, le règlement sur l'IA ne s'applique pas aux systèmes d'IA si et dans la mesure où ils sont mis sur le marché, mis en service ou utilisés avec ou sans modifications exclusivement à des fins militaires, de défense ou de sécurité nationale, quel que soit le type d'entité exerçant ces activités [AIA-Art2-3].

Judge: 5/5. The answer's claim is directly stated in the cited source.

### h004 (en, obligation)

**Question:** A US company with no office in Europe wants to sell a high-risk AI system there. Who does it need to name in the EU before it can?

**Answer** (gemini-3.5-flash-lite):

> Prior to making its high-risk AI system available on the Union market, a provider established in a third country shall, by written mandate, appoint an authorised representative which is established in the Union [AIA-Art22-1]. The provided sources do not cover whether any other entities need to be named.

Judge: 5/5. All statements are directly supported by the cited source and no citation is unsupported.

### h005 (en, obligation)

**Question:** Our website chatbot answers customers. Do we have to tell them they are not chatting with a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. However, this obligation does not apply if it is obvious from the point of view of a natural person who is reasonably well-informed, observant, and circumspect, taking into account the circumstances and the context of use, nor does it apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences (subject to appropriate safeguards for third-party rights and freedoms and unless the systems are available for the public to report a criminal offence) [AIA-Art50-1].
>
> The provided sources do not cover whether your specific website chatbot meets these exceptions or how the transparency obligation applies to your particular setup.

Judge: 5/5. All statements are directly supported by the cited AI Act Article 50(1) source.

### h006 (fr, obligation)

**Question:** Si notre média publie une fausse vidéo d'un homme politique créée avec une IA, devons-nous le signaler ?

**Answer** (gemini-3.5-flash-lite):

> Les déployeurs d’un système d’IA qui génère ou manipule des images ou des contenus audio ou vidéo constituant un hypertrucage (une image ou un contenu audio ou vidéo généré ou manipulé par l’IA, présentant une ressemblance avec des personnes, des objets, des lieux, des entités ou événements existants et pouvant être perçu à tort par une personne comme authentiques ou véridiques) indiquent que les contenus ont été générés ou manipulés par une IA [AIA-Art50-4, AIA-Art3-60]. Lorsque le contenu fait partie d’une œuvre ou d’un programme manifestement artistique, créatif, satirique, fictif ou analogue, les obligations de transparence se limitent à la divulgation de l’existence de tels contenus d’une manière appropriée qui n’entrave pas l’affichage ou la jouissance de l’œuvre [AIA-Art50-4].
>
> Les sources fournies ne précisent pas si ces règles s'appliquent spécifiquement à un cas où le média relaie une telle vidéo sans en être le déployeur.

Judge: 5/5. All claims are directly supported by the cited sources, and the statement about lack of specificity is accurate.

### h007 (en, obligation)

**Question:** Is an AI tool that only fixes spelling mistakes in job ads high-risk just because it is used in hiring?

**Answer** (gemini-3.5-flash-lite):

> An AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making, provided that certain conditions are fulfilled (such as being intended to perform a narrow procedural task or to improve the result of a previously completed human activity) [AIA-Art6-3]. However, notwithstanding this derogation, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons [AIA-Art6-3]. The provided sources do not cover whether fixing spelling mistakes in job ads specifically meets these exemption conditions or amounts to profiling.

Judge: 5/5. All statements are directly supported by the cited source AIA-Art6-3 and no citation is unsupported.

### h008 (en, obligation)

**Question:** Is software that scores how likely someone is to repay a loan subject to extra rules under the AI Act?

**Answer** (gemini-3.5-flash-lite):

> AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score (with the exception of those used for detecting financial fraud) are classified as high-risk AI systems under the AI Act [AIA-AnnexIII-5]. The provided sources do not cover what specific extra rules apply to these high-risk AI systems.

Judge: 5/5. All claims are directly supported by the cited source and the statement about source coverage is accurate.

### h009 (fr, lookup)

**Question:** Quelle amende risque une entreprise qui donne des informations fausses aux autorités sur son système d'IA ?

**Answer** (gemini-3.5-flash-lite):

> La fourniture d’informations inexactes, incomplètes ou trompeuses aux organismes notifiés ou aux autorités nationales compétentes en réponse à une demande fait l’objet d’une amende administrative pouvant aller jusqu’à 7 500 000 EUR ou, si l’auteur de l’infraction est une entreprise, jusqu’à 1 % de son chiffre d’affaires annuel mondial total réalisé au cours de l’exercice précédent, le montant le plus élevé étant retenu [AIA-Art99-5]. Les sources ne couvrent pas les amendes applicables en cas de fourniture d'informations fausses dans d'autres contextes non spécifiés.

Judge: 5/5. All claims are directly supported by the cited source.

### h010 (en, lookup)

**Question:** Are AI Act fines lower for a small startup than for a big company?

**Answer** (gemini-3.5-flash-lite):

> Yes, in the case of SMEs, including start-ups, each fine referred to in Article 99 shall be up to the percentages or amount referred to in paragraphs 3, 4, and 5 of that Article, whichever thereof is lower [AIA-Art99-6]. The provided sources do not cover whether fines for general-purpose AI model providers or Union institutions are similarly reduced for startups.

Judge: 5/5. The answer's claim about lower fines for SMEs is directly supported by the cited source, and no unsupported statements are made.

### h011 (en, obligation)

**Question:** We only resell an AI system that another company built. Do we have anything to check before selling it?

**Answer** (gemini-3.5-flash-lite):

> Before making a high-risk AI system available on the market, distributors shall verify that it bears the required CE marking, that it is accompanied by a copy of the EU declaration of conformity and instructions for use, and that the provider and the importer (as applicable) have complied with their respective obligations set out in Article 16, points (b) and (c), and Article 23(3) [AIA-Art24-1].
>
> The provided sources do not cover whether you have any checks to perform if the AI system you are reselling is not classified as high-risk.

Judge: 5/5. All statements are directly supported by the cited source and the claim about lack of coverage is consistent with the sources provided.

### h012 (fr, obligation)

**Question:** Une entreprise peut-elle refuser d'effacer mes données parce que la loi l'oblige à les conserver ?

**Answer** (gemini-3.5-flash-lite):

> Oui, une entreprise est tenue d'effacer les données à caractère personnel dans les meilleurs délais si les données doivent être effacées pour respecter une obligation légale prévue par le droit de l'Union ou par le droit de l'État membre auquel le responsable du traitement est soumis [GDPR-Art17-1]. Les sources fournies ne précisent toutefois pas si une entreprise peut *refuser* explicitement l'effacement dans cette situation précise, se contentant d'établir l'obligation d'effacement correspondante.

Judge: 5/5. All statements in the answer are directly supported by the cited source GDPR-Art17-1.

### h013 (en, obligation)

**Question:** Can a gym scan members' fingerprints at the entrance without asking them?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.
