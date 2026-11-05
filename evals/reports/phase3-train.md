# Retrieval report: phase3-train

E: as C, with articles and annexes ranked before recitals. Split `train`, 19 scored questions (0 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.342 |
| **Recall@5** | **0.868** [0.71, 1.00] |
| Recall@10 | 0.921 |
| Recall@20 | 0.974 |
| MRR@10 | 0.580 [0.43, 0.74] |
| nDCG@10 | 0.661 |
| ms / query | 148 |

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

Top 5 passages, temperature 0, judge: none.

| Metric | Value |
|---|---|
| n | 19 |
| in_scope | 19 |
| out_of_scope | 0 |
| refusal_rate | None |
| false_refusal_rate | 0.1053 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.9545 |
| gold_in_context | 1.0 |
| gold_cited | 0.8947 |
| citation_precision_lenient | None |
| faithfulness | None |
| fully_supported | None |
| faithfulness_ci95 | None |
| judged | 0 |
| judge_failed | 0 |
| uncited_sentences | 1.12 |
| input_tokens | 30541 |
| output_tokens | 2283 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 6 | None | 0.0 | None | None |
| hard | 13 | None | 0.1538 | None | None |

### q045 (en, definition)

**Question:** Who counts as a deployer of an AI system?

**Answer** (gemini-3.5-flash-lite):

> A 'deployer' means a natural or legal person, public authority, agency or other body using an AI system under its authority, except where the AI system is used in the course of a personal non-professional activity [AIA-Art3-4].

### q046 (fr, lookup)

**Question:** Un logiciel d'IA qui trie automatiquement les CV des candidats est-il un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> Un système d'IA destiné à être utilisé pour analyser et filtrer les candidatures est considéré comme un système d'IA à haut risque relevant de l'emploi, de la gestion de la main-d'œuvre et de l'accès à l'emploi indépendant [AIA-AnnexIII-4].
>
> Cependant, les sources ne précisent pas si cette classification s'applique automatiquement ou si des dérogations spécifiques (telles que l'absence de risque important de préjudice lorsque le système accomplit une tâche procédurale étroite) pourraient s'appliquer dans un cas particulier [AIA-Art6-3].
>
> *Note: Je donne des informations juridiques et non des conseils juridiques.*

### q047 (en, obligation)

**Question:** Do people have to be told when they are chatting with an AI system rather than a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. This requirement does not apply if it is obvious from the point of view of a reasonably well-informed, observant, and circumspect natural person, taking into account the circumstances and the context of use [AIA-Art50-1]. Furthermore, this obligation does not apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences, provided appropriate safeguards for the rights and freedoms of third parties are in place, unless those systems are available for the public to report a criminal offence [AIA-Art50-1]. The provided sources do not cover whether other specific exceptions or rules apply to this transparency obligation.

### q048 (en, lookup)

**Question:** When can I ask a company to delete the personal data it holds about me?

**Answer** (gemini-3.5-flash-lite):

> You have the right to obtain the erasure of personal data concerning you without undue delay from the controller when one of the following grounds applies:
> - The personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed [GDPR-Art17-1].
> - You withdraw consent on which the processing is based (according to point (a) of Article 6(1) or point (a) of Article 9(2)), and there is no other legal ground for the processing [GDPR-Art17-1].
> - You object to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or you object to the processing pursuant to Article 21(2) [GDPR-Art17-1].
> - The personal data have been unlawfully processed [GDPR-Art17-1].
> - The personal data have to be erased to comply with a legal obligation in Union or Member State law to which the controller is subject [GDPR-Art17-1].
> - The personal data have been collected in relation to the offer of information society services referred to in Article 8(1) [GDPR-Art17-1].
>
> The provided sources do not cover any potential conditions or limitations outside of these specific grounds.

### q049 (fr, definition)

**Question:** Qu'est-ce que la pseudonymisation au sens du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Au sens du RGPD, la « pseudonymisation » désigne le traitement de données à caractère personnel de telle façon que celles-ci ne puissent plus être attribuées à une personne concernée précise sans avoir recours à des informations supplémentaires [GDPR-Art4-5]. Pour ce faire, ces informations supplémentaires doivent être conservées séparément et soumises à des mesures techniques et organisationnelles afin de garantir que les données à caractère personnel ne sont pas attribuées à une personne physique identifiée ou identifiable [GDPR-Art4-5]. Les sources fournies ne couvrent pas d'autres aspects ou définitions de la pseudonymisation.

### q050 (en, lookup)

**Question:** From what date do the AI Act's bans on prohibited AI practices apply?

**Answer** (gemini-3.5-flash-lite):

> The bans on prohibited AI practices, which are contained in Chapter II of the AI Act, apply from 2 February 2025 [AIA-Art113].

### h001 (en, obligation)

**Question:** Can a non-EU startup with no office or presence in Europe face fines under the EU AI Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h002 (en, obligation)

**Question:** Do I have to comply with the AI Act if I use an AI image generator at home for fun?

**Answer** (refused (uncited)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h003 (fr, obligation)

**Question:** Une armée qui développe un système d'IA uniquement pour la défense doit-elle respecter le règlement sur l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement sur l'intelligence artificielle ne s'applique pas aux systèmes d'IA si et dans la mesure où ils sont mis sur le marché, mis en service ou utilisés exclusivement à des fins militaires, de défense ou de sécurité nationale, quel que soit le type d'entité exerçant ces activités [AIA-Art2-3].
>
> Les sources fournies ne permettent pas de déterminer si d'autres conditions spécifiques ou obligations indirectes pourraient s'appliquer en dehors de cette exclusion d'usage exclusif.

### h004 (en, obligation)

**Question:** A US company with no office in Europe wants to sell a high-risk AI system there. Who does it need to name in the EU before it can?

**Answer** (gemini-3.5-flash-lite):

> Prior to making their high-risk AI systems available on the Union market, providers established in third countries shall, by written mandate, appoint an authorised representative which is established in the Union [AIA-Art22-1].
>
> The sources do not cover whether the US company must name anyone else besides an authorised representative.
>
> *Disclaimer: You are receiving legal information, not legal advice.*

### h005 (en, obligation)

**Question:** Our website chatbot answers customers. Do we have to tell them they are not chatting with a human?

**Answer** (gemini-3.5-flash-lite):

> Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system [AIA-Art50-1]. This obligation does not apply if it is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use, or to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences (unless those systems are available for the public to report a criminal offence) [AIA-Art50-1]. This information must be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure, and must conform to applicable accessibility requirements [AIA-Art50-5].
>
> The sources do not cover whether your specific website chatbot meets the criteria of being "obvious" to a reasonably well-informed, observant, and circumspect person in its particular context of use.
>
> Please note that this is legal information and not legal advice.

### h006 (fr, obligation)

**Question:** Si notre média publie une fausse vidéo d'un homme politique créée avec une IA, devons-nous le signaler ?

**Answer** (gemini-3.5-flash-lite):

> Les déployeurs d’un système d’IA qui génère ou manipule des images ou des contenus audio ou vidéo constituant un hypertrucage (dééfini comme une image ou un contenu audio ou vidéo généré ou manipulé par l’IA, présentant une ressemblance avec des personnes, des objets, des lieux, des entités ou événements existants et pouvant être perçu à tort par une personne comme authentiques ou véridiques) doivent indiquer que les contenus ont été générés ou manipulés par une IA [AIA-Art50-4, AIA-Art3-60].
>
> Cependant, les sources ne précisent pas les règles spécifiques applicables aux médias en dehors de cette obligation générale concernant les hypertrucages [AIA-Art50-4].
>
> *Note : Ces informations constituent des données juridiques et non un conseil juridique.*

### h007 (en, obligation)

**Question:** Is an AI tool that only fixes spelling mistakes in job ads high-risk just because it is used in hiring?

**Answer** (gemini-3.5-flash-lite):

> An AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making, provided that certain conditions are fulfilled (such as being intended to perform a narrow procedural task or to improve the result of a previously completed human activity) [AIA-Art6-3]. However, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons, notwithstanding those derogation conditions [AIA-Art6-3]. The provided sources do not cover whether a tool *only fixing spelling mistakes* specifically meets these derogation conditions or the profiling exception.

### h008 (en, obligation)

**Question:** Is software that scores how likely someone is to repay a loan subject to extra rules under the AI Act?

**Answer** (gemini-3.5-flash-lite):

> AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score are considered high-risk AI systems pursuant to Article 6(2), with the exception of those used for detecting financial fraud [AIA-AnnexIII-5, AIA-Art6-2]. The provided sources do not cover what specific extra rules apply to these high-risk AI systems.

### h009 (fr, lookup)

**Question:** Quelle amende risque une entreprise qui donne des informations fausses aux autorités sur son système d'IA ?

**Answer** (gemini-3.5-flash-lite):

> La fourniture d’informations inexactes, incomplètes ou trompeuses aux organismes notifiés ou aux autorités nationales compétentes en réponse à une demande fait l’objet d’une amende administrative pouvant aller jusqu’à 7 500 000 EUR ou, si l’auteur de l’infraction est une entreprise, jusqu’à 1 % de son chiffre d’affaires annuel mondial total réalisé au cours de l’exercice précédent, le montant le plus élevé étant retenu [AIA-Art99-5].
>
> Les sources fournies ne traitent pas des sanctions applicables si ces informations fausses sont données à des entités autres que les organismes notifiés ou les autorités nationales compétentes.

### h010 (en, lookup)

**Question:** Are AI Act fines lower for a small startup than for a big company?

**Answer** (gemini-3.5-flash-lite):

> Yes, in the case of SMEs, including start-ups, each fine referred to in the relevant Article shall be up to the percentages or amount referred to in the provisions, whichever thereof is lower [AIA-Art99-6]. Additionally, the rules on penalties laid down by Member States shall take into account the interests of SMEs, including start-ups, and their economic viability [AIA-Art99-1].
>
> *Disclaimer: You are given legal information, not legal advice. Never say whether a specific company or system is compliant.*

### h011 (en, obligation)

**Question:** We only resell an AI system that another company built. Do we have anything to check before selling it?

**Answer** (gemini-3.5-flash-lite):

> Before making a high-risk AI system available on the market, distributors shall verify that it bears the required CE marking, that it is accompanied by a copy of the EU declaration of conformity and instructions for use, and that the provider and the importer (as applicable) have complied with their respective obligations laid down in Article 16, points (b) and (c) and Article 23(3) [AIA-Art24-1].
>
> Please note that you are providing legal information, not legal advice. The provided sources do not cover whether you are considered a distributor or if the AI system in question is classified as high-risk.

### h012 (fr, obligation)

**Question:** Une entreprise peut-elle refuser d'effacer mes données parce que la loi l'oblige à les conserver ?

**Answer** (gemini-3.5-flash-lite):

> Oui, une entreprise peut refuser d'effacer vos données si le traitement est nécessaire pour respecter une obligation légale qui requiert le traitement, prévue par le droit de l'Union ou par le droit de l'État membre auquel le responsable du traitement est soumis [GDPR-Art17-3]. Les sources fournies ne couvrent pas d'éventuelles exceptions supplémentaires ou conditions procédurales liées à ce refus.

### h013 (en, obligation)

**Question:** Can a gym scan members' fingerprints at the entrance without asking them?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the processing of biometric data for the purpose of uniquely identifying a natural person is generally prohibited [GDPR-Art9-1]. The sources do not cover whether a gym is specifically permitted to scan members' fingerprints at the entrance without asking them.
