# Retrieval report: v3a-train

E: as C, with articles and annexes ranked before recitals. Split `train`, 19 scored questions (0 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.342 |
| **Recall@5** | **0.868** [0.71, 1.00] |
| Recall@10 | 0.921 |
| Recall@20 | 0.974 |
| MRR@10 | 0.580 [0.43, 0.74] |
| nDCG@10 | 0.661 |
| ms / query | 136 |

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
| citation_precision_strict | 0.7857 |
| gold_in_context | 1.0 |
| gold_cited | 0.9474 |
| citation_precision_lenient | 0.8214 |
| faithfulness | 0.875 |
| fully_supported | 0.6667 |
| faithfulness_ci95 | (0.7778, 0.9583) |
| judged | 18 |
| judge_failed | 0 |
| uncited_sentences | 0.44 |
| input_tokens | 30189 |
| output_tokens | 2262 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 6 | None | 0.0 | 0.875 | 0.5 |
| hard | 13 | None | 0.0769 | 0.875 | 0.75 |

### q045 (en, definition)

**Question:** Who counts as a deployer of an AI system?

**Answer** (gemini-3.5-flash-lite):

> A 'deployer' means a natural or legal person, public authority, agency or other body using an AI system under its authority, except where the AI system is used in the course of a personal non-professional activity [AIA-Art3-4].

Judge: 5/5. The answer accurately reflects the definition of 'deployer' as given in the cited source.

### q046 (fr, lookup)

**Question:** Un logiciel d'IA qui trie automatiquement les CV des candidats est-il un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> Oui, un système d'IA destiné à être utilisé pour le recrutement ou la sélection de personnes physiques, en particulier pour analyser et filtrer les candidatures, est considéré comme un système d'IA à haut risque [AIA-AnnexIII-4, AIA-Art6-2]. Néanmoins, les sources ne précisent pas si cette classification s'applique sans exception dans tous les cas individuels, ni si la dérogation prévue à l'article 6, paragraphe 3, peut s'y appliquer (à l'exception de la règle interdisant la dérogation en cas de profilage).

Judge: 4/5. The answer correctly cites that recruitment AI is high‑risk, but incorrectly claims the sources do not address possible exceptions, which they do.

### q047 (en, obligation)

**Question:** Do people have to be told when they are chatting with an AI system rather than a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. This obligation does not apply if it is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use [AIA-Art50-1]. Furthermore, this obligation does not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence [AIA-Art50-1]. The provided sources do not cover whether this transparency obligation applies specifically to voice-based assistants or telephone interactions. [AIA-Art50-1]

Judge: 4/5. All main legal claims are directly supported by Article 50(1), but the citation for the statement about sources not covering voice assistants is not directly supported.

### q048 (en, lookup)

**Question:** When can I ask a company to delete the personal data it holds about me?

**Answer** (gemini-3.5-flash-lite):

> You have the right to obtain the erasure of your personal data without undue delay from the controller when one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) you withdraw consent on which the processing is based and there is no other legal ground for the processing; (c) you object to the processing under certain provisions and there are no overriding legitimate grounds for the processing; (d) the personal data have been unlawfully processed; (e) the personal data must be erased to comply with a legal obligation in Union or Member State law to which the controller is subject; or (f) the personal data have been collected in relation to the offer of information society services [GDPR-Art17-1]. The provided sources do not cover what specific steps or format you must use to submit this request to the company [GDPR-Art17-1].

Judge: 5/5. All statements are directly supported by the cited GDPR article, and the note about missing procedural details is accurate.

### q049 (fr, definition)

**Question:** Qu'est-ce que la pseudonymisation au sens du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Au sens du RGPD, la « pseudonymisation » désigne le traitement de données à caractère personnel de telle façon que celles-ci ne puissent plus être attribuées à une personne concernée précise sans avoir recours à des informations supplémentaires, pour autant que ces informations supplémentaires soient conservées séparément et soumises à des mesures techniques et organisationnelles afin de garantir que les données à caractère personnel ne sont pas attribuées à une personne physique identifiée ou identifiable [GDPR-Art4-5].

Judge: 5/5. The answer's definition matches the source and is correctly cited.

### q050 (en, lookup)

**Question:** From what date do the AI Act's bans on prohibited AI practices apply?

**Answer** (gemini-3.5-flash-lite):

> The sources do not state the specific application date for all of the AI Act's bans on prohibited AI practices, but they state that Chapters I and II (which include the rules on prohibited AI practices) shall apply from 2 February 2025 [AIA-Art113].

Judge: 4/5. The answer correctly cites the date from the source for Chapters I and II, but the comment about sources not stating the specific date is not directly supported.

### h001 (en, obligation)

**Question:** Can a non-EU startup with no office or presence in Europe face fines under the EU AI Act?

**Answer** (gemini-3.5-flash-lite):

> The AI Act applies to providers and deployers of AI systems that have their place of establishment or are located in a third country, where the output produced by the AI system is used in the Union, as well as to providers placing AI systems or general-purpose AI models on the market in the Union irrespective of their location [AIA-Art2-1]. The provided sources do not cover whether non-EU startups can actually be subjected to administrative fines [AIA-Art99-4, AIA-Art100-2, AIA-Art100-3, AIA-Art100-1].

Judge: 3/5. Answer correctly cites the scope but incorrectly claims the sources do not address fines for non‑EU startups, which the penalty provisions do cover.

### h002 (en, obligation)

**Question:** Do I have to comply with the AI Act if I use an AI image generator at home for fun?

**Answer** (gemini-3.5-flash-lite):

> The regulation does not apply to obligations of deployers who are natural persons using AI systems in the course of a purely personal non-professional activity [AIA-Art2-10]. The provided sources do not cover whether using an image generator at home for fun specifically qualifies as a purely personal non-professional activity. [AIA-Art2-10]

Judge: 5/5. All claims are directly supported by the cited source and the statement about source coverage is accurate.

### h003 (fr, obligation)

**Question:** Une armée qui développe un système d'IA uniquement pour la défense doit-elle respecter le règlement sur l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Non, le règlement sur l'IA ne s'applique pas aux systèmes d'IA si et dans la mesure où ils sont mis sur le marché, mis en service ou utilisés avec ou sans modifications exclusivement à des fins militaires, de défense ou de sécurité nationale, quel que soit le type d'entité exerçant ces activités [AIA-Art2-3].

Judge: 5/5. The answer's claim is directly stated in the cited source.

### h004 (en, obligation)

**Question:** A US company with no office in Europe wants to sell a high-risk AI system there. Who does it need to name in the EU before it can?

**Answer** (gemini-3.5-flash-lite):

> Prior to making its high-risk AI system available on the Union market, a provider established in a third country shall, by written mandate, appoint an authorised representative which is established in the Union [AIA-Art22-1]. The provided sources do not cover any other roles or entities that need to be named beyond this authorised representative. [AIA-Art22-1, AIA-Art22-2, AIA-Art22-3, AIA-Art23-1, AIA-Art23-2]

Judge: 5/5. All statements are directly supported by the cited articles, and no citation contradicts the answer.

### h005 (en, obligation)

**Question:** Our website chatbot answers customers. Do we have to tell them they are not chatting with a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. This obligation does not apply if it is obvious from the point of view of a reasonably well-informed, observant, and circumspect natural person, taking into account the circumstances and the context of use [AIA-Art50-1]. Furthermore, this obligation does not apply to AI systems authorized by law to detect, prevent, investigate, or prosecute criminal offenses—subject to appropriate safeguards for the rights and freedoms of third parties—unless those systems are available for the public to report a criminal offense [AIA-Art50-1]. The provided sources do not cover whether a specific website chatbot meets these criteria or is exempt in your specific case [AIA-Art50-1].

Judge: 5/5. All statements are directly supported by the cited source AIA-Art50-1.

### h006 (fr, obligation)

**Question:** Si notre média publie une fausse vidéo d'un homme politique créée avec une IA, devons-nous le signaler ?

**Answer** (gemini-3.5-flash-lite):

> Les déployeurs d’un système d’IA qui génère ou manipule des images ou des contenus audio ou vidéo constituant un hypertrucage (une image ou un contenu audio ou vidéo généré ou manipulé par l’IA, présentant une ressemblance avec des personnes, des objets, des lieux, des entités ou événements existants et pouvant être perçu à tort par une personne comme authentiques ou véridiques) indiquent que les contenus ont été générés ou manipulés par une IA [AIA-Art50-4, AIA-Art3-60]. Lorsque le contenu fait partie d’une œuvre ou d’un programme manifestement artistique, créatif, satirique, fictif ou analogue, ces obligations de transparence se limitent à la divulgation de l’existence de tels contenus générés ou manipulés d’une manière appropriée qui n’entrave pas l’affichage ou la jouissance de l’œuvre [AIA-Art50-4]. Les sources ne précisent pas si cette obligation s'applique dans le cas où la vidéo n'est pas qualifiée d'hypertrucage au sens de la définition ou si elle relève d'autres contextes spécifiques non mentionnés [AIA-Art50-4, AIA-Art3-60].

Judge: 5/5. All claims in the answer are directly supported by the cited sources.

### h007 (en, obligation)

**Question:** Is an AI tool that only fixes spelling mistakes in job ads high-risk just because it is used in hiring?

**Answer** (gemini-3.5-flash-lite):

> An AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making, provided that certain conditions are fulfilled such as being intended to perform a narrow procedural task or to improve the result of a previously completed human activity [AIA-Art6-3]. The provided sources do not cover whether a spelling-correction tool specifically meets these exemption criteria.

Judge: 5/5. All claims are directly supported by the cited source and the statement about lack of coverage is accurate.

### h008 (en, obligation)

**Question:** Is software that scores how likely someone is to repay a loan subject to extra rules under the AI Act?

**Answer** (gemini-3.5-flash-lite):

> AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score (with the exception of those used for detecting financial fraud) are classified as high-risk AI systems under the AI Act [AIA-AnnexIII-5]. The provided sources do not cover whether such systems are subject to any additional "extra" rules beyond their classification as high-risk [AIA-AnnexIII-5].

Judge: 5/5. All statements are directly supported by the cited source and no unsupported citations are present.

### h009 (fr, lookup)

**Question:** Quelle amende risque une entreprise qui donne des informations fausses aux autorités sur son système d'IA ?

**Answer** (gemini-3.5-flash-lite):

> La fourniture d’informations inexactes, incomplètes ou trompeuses aux organismes notifiés ou aux autorités nationales compétentes en réponse à une demande fait l’objet d’une amende administrative pouvant aller jusqu’à 7 500 000 EUR ou, si l’auteur de l’infraction est une entreprise, jusqu’à 1 % de son chiffre d’affaires annuel mondial total réalisé au cours de l’exercice précédent, le montant le plus élevé étant retenu [AIA-Art99-5]. Les sources ne couvrent pas les amendes applicables en cas de fourniture d'informations fausses spécifiques aux modèles d'IA à usage général dans ce contexte précis.

Judge: 3/5. The fine amount is correctly supported by AIA-Art99-5, but the statement that sources do not cover fines for false information by general AI model providers is inaccurate.

### h010 (en, lookup)

**Question:** Are AI Act fines lower for a small startup than for a big company?

**Answer** (gemini-3.5-flash-lite):

> In the case of SMEs, including start-ups, each fine referred to in Article 99 shall be up to the percentages or amounts referred to in paragraphs 3, 4, and 5 of that Article, whichever thereof is lower [AIA-Art99-6]. The provided sources do not cover whether fines are lower for a small startup than for a big company under other articles of the AI Act.

Judge: 3/5. The answer correctly cites Article 99(6) for SMEs, but incorrectly claims the sources do not address whether fines are lower for startups versus large companies, which the sources actually do indicate.

### h011 (en, obligation)

**Question:** We only resell an AI system that another company built. Do we have anything to check before selling it?

**Answer** (gemini-3.5-flash-lite):

> Before making a high-risk AI system available on the market, distributors shall verify that it bears the required CE marking, that it is accompanied by a copy of the EU declaration of conformity referred to in Article 47 and instructions for use, and that the provider and the importer of that system, as applicable, have complied with their respective obligations as laid down in Article 16, points (b) and (c) and Article 23(3) [AIA-Art24-1]. The provided sources do not cover whether you have any checks to perform if the AI system you resell is not classified as high-risk.

Judge: 5/5. All statements are directly supported by the cited source and the comment about lack of coverage is accurate.

### h012 (fr, obligation)

**Question:** Une entreprise peut-elle refuser d'effacer mes données parce que la loi l'oblige à les conserver ?

**Answer** (gemini-3.5-flash-lite):

> Oui, le responsable du traitement a l'obligation d'effacer les données à caractère personnel dans les meilleurs délais lorsque les données doivent être effacées pour respecter une obligation légale prévue par le droit de l'Union ou par le droit de l'État membre auquel le responsable du traitement est soumis [GDPR-Art17-1]. Les sources fournies ne précisent pas explicitement si une entreprise peut refuser l'effacement dans ce cas précis, mais elles indiquent que l'existence d'une telle obligation légale constitue l'un des motifs pour lesquels l'effacement est requis [GDPR-Art17-1].

Judge: 5/5. All claims in the answer are directly supported by GDPR Article 17(1) and no citation is unsupported.

### h013 (en, obligation)

**Question:** Can a gym scan members' fingerprints at the entrance without asking them?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.
