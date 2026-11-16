# Retrieval report: phase3q-train

E: as C, with articles and annexes ranked before recitals. Split `train`, 19 scored questions (0 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.342 |
| **Recall@5** | **0.868** [0.71, 1.00] |
| Recall@10 | 0.921 |
| Recall@20 | 0.974 |
| MRR@10 | 0.580 [0.43, 0.74] |
| nDCG@10 | 0.661 |
| ms / query | 131 |

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
| false_refusal_rate | 0.0526 |
| retried | 5 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 1.0 |
| gold_in_context | 1.0 |
| gold_cited | 0.9474 |
| citation_precision_lenient | 0.8571 |
| faithfulness | 0.9167 |
| fully_supported | 0.7778 |
| faithfulness_ci95 | (0.8333, 0.9861) |
| judged | 18 |
| judge_failed | 0 |
| uncited_sentences | 1.06 |
| input_tokens | 30092 |
| output_tokens | 2519 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 6 | None | 0.0 | 0.9583 | 0.8333 |
| hard | 13 | None | 0.0769 | 0.8958 | 0.75 |

### q045 (en, definition)

**Question:** Who counts as a deployer of an AI system?

**Answer** (gemini-3.5-flash-lite):

> A 'deployer' is defined as a natural or legal person, public authority, agency, or other body using an AI system under its authority, except when the AI system is used in the course of a personal non-professional activity [AIA-Art3-4]. The provided sources do not cover any other details regarding who else might count as a deployer beyond this definition.

Judge: 5/5. All claims are directly supported by the cited source

### q046 (fr, lookup)

**Question:** Un logiciel d'IA qui trie automatiquement les CV des candidats est-il un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> Un système d'IA visé à l'annexe III est considéré comme étant à haut risque [AIA-Art6-2]. Les sources fournies ne permettent pas de déterminer si un logiciel d'IA qui trie automatiquement les CV des candidats relève spécifiquement de l'annexe III.
>
> Cependant, par dérogation, un système d'IA visé à l'annexe III n'est pas considéré comme étant à haut risque lorsqu'il ne présente pas de risque important de préjudice pour la santé, la sécurité ou les droits fondamentaux des personnes physiques (notamment en n'ayant pas d'incidence significative sur le résultat de la prise de décision) et qu'il remplit l'une des conditions énumérées (par exemple, accomplir une tâche procédurale étroite, améliorer le résultat d'une activité humaine, etc.) [AIA-Art6-3]. Néanmoins, même dans ce cas, un système d'IA visé à l'annexe III reste toujours considéré comme à haut risque s'il effectue un profilage de personnes physiques [AIA-Art6-3].
>
> Les sources fournies ne contiennent pas l'annexe III du règlement et ne précisent pas si le tri automatique de CV constitue un profilage ou remplit les conditions de la dérogation.

Judge: 5/5. All statements are directly supported by the cited sources.

### q047 (en, obligation)

**Question:** Do people have to be told when they are chatting with an AI system rather than a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. However, this does not apply if it is obvious from the point of view of a reasonably well-informed, observant, and circumspect natural person, taking into account the circumstances and the context of use [AIA-Art50-1]. Furthermore, this obligation does not apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence [AIA-Art50-1].
>
> The provided sources do not cover specific rules or exceptions regarding chatbot text messaging interfaces beyond these general transparency obligations for AI systems interacting directly with natural persons.

Judge: 5/5. All claims are directly supported by Article 50(1) of the AI Act as cited.

### q048 (en, lookup)

**Question:** When can I ask a company to delete the personal data it holds about me?

**Answer** (gemini-3.5-flash-lite):

> You have the right to obtain the erasure of personal data concerning you from the controller without undue delay when one of the following grounds applies:
> - The personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed [GDPR-Art17-1].
> - You withdraw consent on which the processing is based (under point (a) of Article 6(1) or point (a) of Article 9(2)), and there is no other legal ground for the processing [GDPR-Art17-1].
> - You object to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or you object to the processing pursuant to Article 21(2) [GDPR-Art17-1].
> - The personal data have been unlawfully processed [GDPR-Art17-1].
> - The personal data must be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject [GDPR-Art17-1].
> - The personal data have been collected in relation to the offer of information society services referred to in Article 8(1) [GDPR-Art17-1].
>
> The provided sources do not cover any other potential conditions or procedures for requesting data deletion outside of these specific grounds.

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR Article 17(1) source.

### q049 (fr, definition)

**Question:** Qu'est-ce que la pseudonymisation au sens du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Au sens du RGPD, la « pseudonymisation » désigne le traitement de données à caractère personnel de telle façon que celles-ci ne puissent plus être attribuées à une personne concernée précise sans avoir recours à des informations supplémentaires [GDPR-Art4-5]. Pour ce faire, ces informations supplémentaires doivent être conservées séparément et soumises à des mesures techniques et organisationnelles afin de garantir que les données à caractère personnel ne sont pas attribuées à une personne physique identifiée ou identifiable [GDPR-Art4-5].

Judge: 5/5. All statements are directly supported by the cited GDPR article.

### q050 (en, lookup)

**Question:** From what date do the AI Act's bans on prohibited AI practices apply?

**Answer** (gemini-3.5-flash-lite):

> Der Tag, ab dem die Verbote unzulässiger KI-Praktiken (welche in Kapitel II des KI-Gesetzes geregelt sind) anwendbar sind, ist der 2. Februar 2025 [AIA-Art113]. Die Quellen beantworten nicht, ob für einzelne Bestimmungen außerhalb von Kapitel II abweichende Daten gelten [AIA-Art113].

Judge: 4/5. The answer correctly states the start date for Chapter II bans, but incorrectly claims the sources do not address differing dates for other chapters, which the source actually does.

### h001 (en, obligation)

**Question:** Can a non-EU startup with no office or presence in Europe face fines under the EU AI Act?

**Answer** (gemini-3.5-flash-lite):

> Yes, providers and deployers of AI systems that have their place of establishment or are located in a third country can fall within the scope of the EU AI Act when the output produced by the AI system is used in the Union [AIA-Art2-1]. Furthermore, providers placing on the market or putting into service general-purpose AI models or AI systems in the Union are subject to the Regulation irrespective of whether they are established or located within the Union or in a third country [AIA-Art2-1]. The provided sources do not cover whether non-EU startups specifically can face fines.

Judge: 5/5. All statements are directly supported by Article 2(1) of the AI Act.

### h002 (en, obligation)

**Question:** Do I have to comply with the AI Act if I use an AI image generator at home for fun?

**Answer** (gemini-3.5-flash-lite):

> No, the AI Act does not apply to obligations of deployers who are natural persons using AI systems in the course of a purely personal non-professional activity [AIA-Art2-10].
>
> *(Note: You are given legal information, not legal advice.)*

Judge: 5/5. The answer's claim is directly supported by the cited source.

### h003 (fr, obligation)

**Question:** Une armée qui développe un système d'IA uniquement pour la défense doit-elle respecter le règlement sur l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement sur l'IA ne s'applique pas aux systèmes d'IA si et dans la mesure où ils sont mis sur le marché, mis en service ou utilisés avec ou sans modifications exclusivement à des fins militaires, de défense ou de sécurité nationale, quel que soit le type d'entité exerçant ces activités [AIA-Art2-3]. De plus, le règlement ne s'applique pas aux domaines qui ne relèvent pas du champ d'application du droit de l'Union et ne porte pas atteinte aux compétences des États membres en matière de sécurité nationale [AIA-Art2-3].
>
> Les sources fournies ne traitent pas de la question de savoir si les règles relatives aux modèles d'IA à usage général s'appliquent dans ce contexte spécifique.

Judge: 5/5. All statements are directly supported by the cited Article 2(3) of the AI Regulation.

### h004 (en, obligation)

**Question:** A US company with no office in Europe wants to sell a high-risk AI system there. Who does it need to name in the EU before it can?

**Answer** (gemini-3.5-flash-lite):

> Prior to making its high-risk AI system available on the Union market, a provider established in a third country shall, by written mandate, appoint an authorised representative which is established in the Union [AIA-Art22-1]. The sources do not cover whether any other entities need to be named.

Judge: 5/5. All statements are directly supported by the cited source and no contradictory information is present.

### h005 (en, obligation)

**Question:** Our website chatbot answers customers. Do we have to tell them they are not chatting with a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. However, this obligation does not apply if it is obvious from the point of view of a natural person who is reasonably well-informed, observant, and circumspect, taking into account the circumstances and the context of use [AIA-Art50-1]. This obligation also does not apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences (subject to appropriate safeguards for third-party rights and freedoms), unless those systems are available for the public to report a criminal offence [AIA-Art50-1]. The provided sources do not cover whether your specific website chatbot meets these criteria or is considered compliant.

Judge: 5/5. All statements are directly supported by the cited source AIA-Art50-1.

### h006 (fr, obligation)

**Question:** Si notre média publie une fausse vidéo d'un homme politique créée avec une IA, devons-nous le signaler ?

**Answer** (gemini-3.5-flash-lite):

> Les déployeurs d’un système d’IA qui génère ou manipule des images ou des contenus audio ou vidéo constituant un hypertrucage indiquent que les contenus ont été générés ou manipulés par une IA [AIA-Art50-4].
> Cependant, les sources ne précisent pas si le qualificatif de "fausse vidéo d'un homme politique" relève exactement de la définition d'un hypertrucage au sens du règlement.

Judge: 3/5. One claim is correctly supported by the cited source, but the statement that sources do not clarify the definition of a fake political video is contradicted by the definition provided in the sources.

### h007 (en, obligation)

**Question:** Is an AI tool that only fixes spelling mistakes in job ads high-risk just because it is used in hiring?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, an AI system referred to in Annex III (which includes AI systems intended to be used for recruitment or selection, such as placing targeted job advertisements) shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety, or fundamental rights of natural persons, including by not materially influencing the outcome of decision making [AIA-AnnexIII-4, AIA-Art6-3, AIA-Art6-2].
>
> This exception applies if the AI system fulfils certain conditions, such as being intended to perform a narrow procedural task or to improve the result of a previously completed human activity [AIA-Art6-3]. However, the sources do not specify whether an AI tool that *only* fixes spelling mistakes automatically meets these specific exemption conditions. Furthermore, notwithstanding these exceptions, an AI system referred to in Annex III shall *always* be considered high-risk if it performs profiling of natural persons [AIA-Art6-3].
>
> Please note that this is legal information and not legal advice.

Judge: 4/5. All main legal claims are supported by the sources, but the citation of AIA-Art6-2 does not support the exemption claim.

### h008 (en, obligation)

**Question:** Is software that scores how likely someone is to repay a loan subject to extra rules under the AI Act?

**Answer** (gemini-3.5-flash-lite):

> AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score (with the exception of those used for detecting financial fraud) are classified as high-risk AI systems under the AI Act [AIA-AnnexIII-5]. The provided sources do not cover what specific extra rules apply to these systems beyond their classification as high-risk.

Judge: 5/5. All claims are directly supported by the cited source and the statement about lack of extra rule details is accurate.

### h009 (fr, lookup)

**Question:** Quelle amende risque une entreprise qui donne des informations fausses aux autorités sur son système d'IA ?

**Answer** (gemini-3.5-flash-lite):

> La fourniture d’informations inexactes, incomplètes ou trompeuses aux autorités nationales compétentes en réponse à une demande fait l’objet d’une amende administrative pouvant aller jusqu’à 7 500 000 EUR ou, si l’auteur de l’infraction est une entreprise, jusqu’à 1 % de son chiffre d’affaires annuel mondial total réalisé au cours de l’exercice précédent, le montant le plus élevé étant retenu [AIA-Art99-5].
>
> Les sources fournies ne traitent pas des amendes applicables en cas de transmission d'informations fausses à des autorités autres que les autorités nationales compétentes ou les organismes notifiés (telles que la Commission).

Judge: 5/5. All statements are directly supported by the cited source and no citation is unsupported.

### h010 (en, lookup)

**Question:** Are AI Act fines lower for a small startup than for a big company?

**Answer** (gemini-3.5-flash-lite):

> Yes, in the case of SMEs, including start-ups, each fine referred to in Article 99 shall be up to the percentages or amounts referred to in paragraphs 3, 4, and 5 of that Article, whichever is lower [AIA-Art99-6]. The provided sources do not cover whether fines are lower for startups regarding general-purpose AI models or Union institutions.

Judge: 5/5. All claims are directly supported by the cited source and the statement about lack of coverage is accurate.

### h011 (en, obligation)

**Question:** We only resell an AI system that another company built. Do we have anything to check before selling it?

**Answer** (gemini-3.5-flash-lite):

> Before making a high-risk AI system available on the market, distributors shall verify that:
> - It bears the required CE marking [AIA-Art24-1].
> - It is accompanied by a copy of the EU declaration of conformity referred to in Article 47 and instructions for use [AIA-Art24-1].
> - The provider and the importer of that system, as applicable, have complied with their respective obligations as laid down in Article 16, points (b) and (c) and Article 23(3) [AIA-Art24-1].
>
> The provided sources do not cover whether you have any checks to perform if the AI system you resell is not classified as high-risk.

Judge: 5/5. All statements are directly supported by the cited source and the comment about lack of coverage is accurate.

### h012 (fr, obligation)

**Question:** Une entreprise peut-elle refuser d'effacer mes données parce que la loi l'oblige à les conserver ?

**Answer** (gemini-3.5-flash-lite):

> Oui, le responsable du traitement a l'obligation d'effacer les données à caractère personnel dans les meilleurs délais lorsque les données à caractère personnel doivent être effacées pour respecter une obligation légale qui est prévue par le droit de l'Union ou par le droit de l'État membre auquel le responsable du traitement est soumis [GDPR-Art17-1]. Les sources fournies ne précisent toutefois pas explicitement si une entreprise peut refuser d'effacer les données dans un tel cas de figure [GDPR-Art17-1]. Vous donnez des informations juridiques, et non un avis juridique.

Judge: 3/5. The answer correctly cites the right‑to‑erasure condition, but incorrectly claims the source does not address refusal to erase, which the source actually does.

### h013 (en, obligation)

**Question:** Can a gym scan members' fingerprints at the entrance without asking them?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.
