# Retrieval report: phase3-dev

E: as C, with articles and annexes ranked before recitals. Split `dev`, 76 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.789 |
| **Recall@5** | **0.954** [0.91, 0.99] |
| Recall@10 | 0.974 |
| Recall@20 | 0.987 |
| MRR@10 | 0.878 [0.82, 0.93] |
| nDCG@10 | 0.899 |
| ms / query | 142 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 46 | 0.978 | 0.880 |
| fr | 30 | 0.917 | 0.873 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.750 | 0.750 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 39 | 0.974 | 0.877 |
| obligation | 34 | 0.941 | 0.897 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.925 | 0.806 |
| hard | 5 | 0.600 | 0.500 |
| synthetic | 51 | 1.000 | 0.943 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Art61 |
| q009 (en) | AIA-Art83 | 2 | AIA-Art48, AIA-Art83, AIA-Art24 |
| q010 (en) | GDPR-Art3 | 2 | GDPR-Art2, GDPR-Art3, GDPR-Art47 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art48 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Art12, GDPR-Art78, GDPR-Art77 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 2 | AIA-Art71, AIA-Art49, AIA-AnnexV |
| q056 (en) | AIA-Art56 | 2 | AIA-Art55, AIA-Art56, AIA-Art53 |
| q058 (en) | GDPR-Art49 | 2 | GDPR-Art44, GDPR-Art49, GDPR-Art45 |
| q059 (fr) | GDPR-Art80 | 2 | GDPR-Art77, GDPR-Art80, GDPR-Art34 |
| h018 (en) | AIA-Art49 | 2 | AIA-Art24, AIA-Art49, AIA-Art6 |
| q070 (fr) | AIA-Art49 | 3 | AIA-AnnexIII, AIA-AnnexVIII, AIA-Art49 |
| q073 (fr) | GDPR-Art22 | 4 | AIA-Art86, AIA-Art2, AIA-Art5 |
| q002 (fr) | AIA-AnnexV | 9 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |
| h016 (fr) | GDPR-Art22 | 11 | AIA-Art74, GDPR-Art61, AIA-Art5 |
| h017 (en) | AIA-Art83 | none | AIA-Art48, AIA-Art23, AIA-Art24 |

## Answers: `answer.v2`

Top 5 passages, temperature 0, judge: none.

| Metric | Value |
|---|---|
| n | 88 |
| in_scope | 76 |
| out_of_scope | 12 |
| refusal_rate | 1.0 |
| false_refusal_rate | 0.0132 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.8396 |
| gold_in_context | 0.9605 |
| gold_cited | 0.9474 |
| citation_precision_lenient | None |
| faithfulness | None |
| fully_supported | None |
| faithfulness_ci95 | None |
| judged | 0 |
| judge_failed | 0 |
| uncited_sentences | 0.73 |
| input_tokens | 130965 |
| output_tokens | 11477 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 22 | 1.0 | 0.0 | None | None |
| hard | 5 | None | 0.2 | None | None |
| synthetic | 61 | 1.0 | 0.0 | None | None |

### q001 (en, lookup)

**Question:** Is trafficking in human beings one of the crimes for which the police may be allowed to use real-time facial recognition in public spaces to locate a suspect?

**Answer** (gemini-3.5-flash-lite):

> Yes, trafficking in human beings is one of the criminal offences for the purpose of which competent authorities may be authorised to use real-time remote biometric identification systems in publicly accessible spaces for law enforcement, specifically for the localisation or identification of a person suspected of having committed a criminal offence referred to in Annex II [AIA-Art5-1, AIA-Art5-5, AIA-AnnexII].

### q002 (fr, lookup)

**Question:** Quelles mentions doit contenir la déclaration UE de conformité d'un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> La déclaration UE de conformité contient les informations qui figurent à l'annexe V [AIA-Art47-2].
>
> Les sources fournies ne précisent pas la liste détaillée des informations figurant à l'annexe V.

### q003 (en, obligation)

**Question:** How must a high-risk AI system that keeps learning after deployment be built so that its own biased outputs do not feed back into future decisions?

**Answer** (gemini-3.5-flash-lite):

> High-risk AI systems that continue to learn after being placed on the market or put into service shall be developed in such a way as to eliminate or reduce as far as possible the risk of possibly biased outputs influencing input for future operations (feedback loops), and as to ensure that any such feedback loops are duly addressed with appropriate mitigation measures [AIA-Art15-4].

### q004 (en, lookup)

**Question:** If a notified body stops its conformity assessment activities, how long can the certificates it issued remain valid?

**Answer** (gemini-3.5-flash-lite):

> Where a notified body decides to cease its conformity assessment activities, its certificates may remain valid for a period of nine months after the cessation of its activities, provided that another notified body has confirmed in writing that it will assume responsibilities for the high-risk AI systems covered by those certificates [AIA-Art36-3].

### q005 (fr, lookup)

**Question:** Qui peut enquêter lorsqu'on doute qu'un organisme notifié soit encore compétent ?

**Answer** (gemini-3.5-flash-lite):

> La Commission enquête, s'il y a lieu, sur tous les cas où il existe des raisons de douter de la compétence d'un organisme notifié ou du respect continu, par un organisme notifié, des exigences établies à l'article 31 et de ses responsabilités applicables [AIA-Art37-1].
>
> Les sources fournies ne traitent pas de la question de savoir si d'autres entités peuvent également mener de telles enquêtes.

### q006 (en, obligation)

**Question:** Does a public authority that starts using a high-risk AI system to decide who receives social benefits have to register that use in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Yes, before putting into service or using a high-risk AI system listed in Annex III (with the exception of those listed in point 2 of Annex III), deployers that are public authorities, Union institutions, bodies, offices, or agencies, or persons acting on their behalf, must register themselves, select the system, and register its use in the EU database referred to in Article 71 [AIA-Art49-3]. The provided sources do not cover whether deciding who receives social benefits falls under Annex III or its point 2 exception.

### q007 (en, lookup)

**Question:** Who facilitates the drawing up of codes of practice for general-purpose AI models, and by when were they supposed to be ready?

**Answer** (gemini-3.5-flash-lite):

> The AI Office shall encourage and facilitate the drawing up of codes of practice at Union level [AIA-Art56-1]. The provided sources do not cover by when the codes of practice were supposed to be ready.

### q008 (fr, lookup)

**Question:** Quelles conditions doivent remplir les experts du groupe scientifique qui conseille le Bureau de l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Les experts du groupe scientifique doivent être sélectionnés par la Commission en fonction de leur expertise à la pointe des connaissances scientifiques ou techniques dans le domaine de l'IA, nécessaire pour s'acquitter des tâches prévues [AIA-Art68-2]. De plus, ils doivent être en mesure de démontrer qu'ils remplissent les conditions suivantes :
> a) disposer d'une expertise et d'une compétence particulières ainsi que d'une expertise scientifique ou technique dans le domaine de l'IA [AIA-Art68-2];
> b) être indépendants vis-à-vis de tout fournisseur de systèmes d'IA ou de modèles d'IA à usage général [AIA-Art68-2];
> c) être capables de mener des activités avec diligence, précision et objectivité [AIA-Art68-2].
> Les sources fournies ne précisent pas d'autres conditions spécifiques requises pour ces experts.

### q009 (en, definition)

**Question:** Which situations count as formal non-compliance of a high-risk AI system, such as a missing CE marking?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, a high-risk AI system is considered not in conformity with the regulation in situations where:
> - The system is not in conformity with the requirements set out in Section 2 [AIA-Art16, AIA-Art8-1, AIA-Art20-1].
> - The provider has failed to take the necessary corrective actions to bring the system into conformity, withdraw it, disable it, or recall it when it presents a non-conformity or risk [AIA-Art20-1].
> - The system presents a risk within the meaning of Article 79(1) [AIA-Art20-2].
> - A market surveillance authority finds that an AI system classified by the provider as non-high-risk is indeed high-risk and requires the provider to bring it into compliance [AIA-Art80-2].
>
> The provided sources do not cover what other specific situations beyond a missing CE marking constitute formal non-compliance (such as specific administrative or documentation failures).

### q010 (en, lookup)

**Question:** Does the GDPR apply to a company based outside the EU that tracks the online behaviour of people in the EU?

**Answer** (gemini-3.5-flash-lite):

> Yes, the Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to the monitoring of their behaviour as far as their behaviour takes place within the Union [GDPR-Art3-2].
>
> You give legal information, not legal advice.

### q011 (fr, obligation)

**Question:** Lorsque des données personnelles n'ont pas été collectées auprès de la personne concernée, dans quel délai le responsable du traitement doit-il l'informer ?

**Answer** (gemini-3.5-flash-lite):

> Lorsque les données à caractère personnel n'ont pas été collectées auprès de la personne concernée, le responsable du traitement doit fournir les informations dans un délai raisonnable après avoir obtenu les données à caractère personnel, ne dépassant pas un mois, eu égard aux circonstances particulières dans lesquelles les données à caractère personnel sont traitées [GDPR-Art14-3]. Toutefois, si les données doivent être utilisées aux fins de la communication avec la personne concernée, les informations doivent être fournies au plus tard au moment de la première communication à ladite personne, ou s'il est envisagé de communiquer les informations à un autre destinataire, au plus tard lorsque les données sont communiquées pour la première fois [GDPR-Art14-3]. Les sources fournies ne traitent pas des éventuelles exceptions ou conditions particulières autres que ces modalités et délais de transmission.
>
> Vous donnez des informations juridiques, pas des conseils juridiques.

### q012 (en, lookup)

**Question:** Can a bank reject my loan application based only on an automated decision, with no human involved?

**Answer** (gemini-3.5-flash-lite):

> Data subjects have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning them or similarly significantly affects them [GDPR-Art22-1]. However, this does not apply if the decision is necessary for entering into, or the performance of, a contract between the data subject and a data controller, is authorized by Union or Member State law with suitable safeguarding measures, or is based on the data subject's explicit consent [GDPR-Art22-2]. In cases where the decision is necessary for entering into or performing a contract, or is based on explicit consent, the data controller must implement suitable measures to safeguard the data subject's rights, freedoms, and legitimate interests, which must include at least the right to obtain human intervention on the part of the controller, to express their point of view, and to contest the decision [GDPR-Art22-3].
>
> The provided sources do not cover whether the specific scenario of a bank rejecting a loan application qualifies as being necessary for entering into a contract, authorized by law, or based on explicit consent under Article 22 of the GDPR.
>
> *(Note: You give legal information, not legal advice.)*

### q013 (fr, obligation)

**Question:** Dans quel cas le responsable du traitement doit-il consulter l'autorité de contrôle avant de commencer un traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement consulte l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données effectuée au titre de l'article 35 indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque [GDPR-Art36-1]. De plus, le droit des États membres peut exiger des consultations et une autorisation préalable pour les traitements effectués dans le cadre d'une mission d'intérêt public [GDPR-Art36-5]. Les sources ne couvrent pas les autres éventuels cas de consultation préalable qui ne seraient pas fondés sur une analyse d'impact avec risque résiduel élevé ou sur le droit des États membres relatif à une mission d'intérêt public.

### q014 (en, lookup)

**Question:** Can personal data be sent to a country without an adequacy decision if the person explicitly agrees to the transfer?

**Answer** (gemini-3.5-flash-lite):

> Yes, in the absence of an adequacy decision pursuant to Article 45(3) or appropriate safeguards, a transfer of personal data to a third country or an international organisation may take place if the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards [GDPR-Art49-1].

### q015 (en, lookup)

**Question:** In an emergency, can a national data protection authority act on its own without going through the cooperation procedure with other authorities, and for how long?

**Answer** (gemini-3.5-flash-lite):

> In exceptional circumstances, where a supervisory authority concerned considers that there is an urgent need to act in order to protect the rights and freedoms of data subjects, it may immediately adopt provisional measures intended to produce legal effects on its own territory by way of derogation from the consistency and cooperation procedures [GDPR-Art66-1, GDPR-Art60-11]. The period of validity of these provisional measures shall not exceed three months [GDPR-Art66-1].

### q016 (en, lookup)

**Question:** What can I do if the data protection authority does not deal with my complaint?

**Answer** (gemini-3.5-flash-lite):

> If the competent supervisory authority does not handle your complaint, or does not inform you within three months on the progress or outcome of the complaint lodged, you have the right to an effective judicial remedy [GDPR-Art78-2].

### q017 (fr, lookup)

**Question:** Devant quels tribunaux puis-je agir contre une entreprise qui a violé mes droits au titre du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Toute action contre un responsable du traitement ou un sous-traitant est intentée devant les juridictions de l'État membre dans lequel le responsable du traitement ou le sous-traitant dispose d'un établissement [GDPR-Art79-2]. Une telle action peut aussi être intentée devant les juridictions de l'État membre dans lequel la personne concernée a sa résidence habituelle, sauf si le responsable du traitement ou le sous-traitant est une autorité publique d'un État membre agissant dans l'exercice de ses prérogatives de puissance publique [GDPR-Art79-2]. Les sources ne couvrent pas la question des recours ou actions possibles devant des juridictions en dehors de ces critères spécifiques (par exemple, le lieu de la violation).

### q018 (en, obligation)

**Question:** If a processor ignores the controller's instructions and this causes damage to someone, does the processor have to pay compensation?

**Answer** (gemini-3.5-flash-lite):

> Any controller involved in processing shall be liable for the damage caused by processing which infringes the GDPR [GDPR-Art82-2]. A processor shall be liable for the damage caused by processing where it has acted outside or contrary to lawful instructions of the controller [GDPR-Art82-2]. Any person who has suffered material or non-material damage as a result of an infringement of the regulation has the right to receive compensation from the controller or processor for the damage suffered [GDPR-Art82-1].

### q019 (en, cross_law)

**Question:** We provide an AI tool that screens job applicants. What must our GDPR record of processing activities contain, and does the AI Act also require us to register the tool in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Each controller and, where applicable, the controller's representative, must maintain a record of processing activities under their responsibility containing the following information:
> - The name and contact details of the controller and, where applicable, the joint controller, the controller's representative and the data protection officer [GDPR-Art30-1].
> - The purposes of the processing [GDPR-Art30-1].
> - A description of the categories of data subjects and of the categories of personal data [GDPR-Art30-1].
> - The categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations [GDPR-Art30-1].
> - Where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards [GDPR-Art30-1].
> - Where possible, the envisaged time limits for erasure of the different categories of data [GDPR-Art30-1].
> - Where possible, a general description of the technical and organisational security measures referred to in Article 32(1) [GDPR-Art30-1].
>
> The provided sources do not cover whether the AI Act requires you to register an AI tool that screens job applicants in an EU database.

### q020 (fr, cross_law)

**Question:** Une association de défense des droits peut-elle agir au nom de personnes discriminées par un système d'IA, et quelles autorités peuvent exiger la documentation de ce système ?

**Answer** (gemini-3.5-flash-lite):

> Une personne concernée a le droit de mandater un organisme, une organisation ou une association à but non lucratif remplissant certaines conditions (constitution selon le droit d'un État membre, objectifs statutaires d'intérêt public, et activité dans le domaine de la protection des droits et libertés en matière de données à caractère personnel) pour qu'il introduise une réclamation en son nom, exerce en son nom certains droits (visés aux articles 77, 78 et 79 du RGPD) et exerce le droit d'obtenir réparation (visé à l'article 82 du RGPD) lorsque le droit d'un État membre le prévoit [GDPR-Art80-1].
>
> Concernant les autorités habilitées à exiger la documentation, les autorités ou organismes publics nationaux qui supervisent ou font respecter les obligations au titre du droit de l’Union visant à protéger les droits fondamentaux (y compris la non-discrimination) en lien avec les systèmes d’IA à haut risque de l'annexe III sont habilités à demander et à avoir accès à toute documentation créée ou conservée en vertu du règlement IA, dans une langue et un format accessibles, lorsque cela est nécessaire pour accomplir leur mandat [AIA-Art77-1]. De plus, la documentation technique peut être examinée par les autorités nationales compétentes [AIA-Art11-1] et les organismes notifiés [AIA-AnnexVII-4].
>
> Les sources fournies ne précisent pas explicitement si une association peut agir au nom de personnes discriminées spécifiquement sur la base du règlement IA (en dehors du cadre du RGPD mentionné ci-dessus).

### q021 (en, not_covered)

**Question:** What fines can the European Commission impose on gatekeepers that breach the Digital Markets Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q022 (fr, not_covered)

**Question:** Quelles obligations le règlement sur les données (Data Act) impose-t-il aux fabricants d'objets connectés ?

**Answer** (refused (not_covered)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.

### q051 (en, lookup)

**Question:** What specific types of attacks must the technical solutions for high-risk AI systems address, where appropriate, to counter AI-specific vulnerabilities?

**Answer** (gemini-3.5-flash-lite):

> To address AI-specific vulnerabilities, the technical solutions shall include, where appropriate, measures to prevent, detect, respond to, resolve, and control for the following types of attacks:
> - Attacks trying to manipulate the training data set (data poisoning) or pre-trained components used in training (model poisoning) [AIA-Art15-5].
> - Inputs designed to cause the AI model to make a mistake (adversarial examples or model evasion) [AIA-Art15-5].
> - Confidentiality attacks [AIA-Art15-5].
> - Model flaws [AIA-Art15-5].

### q052 (fr, obligation)

**Question:** Quelles mesures minimales le responsable du traitement doit-il mettre en œuvre pour protéger les intérêts d'une personne concernée par une décision individuelle automatisée fondée sur un contrat ou un consentement ?

**Answer** (gemini-3.5-flash-lite):

> Dans les cas où une décision individuelle automatisée est fondée sur la conclusion ou l'exécution d'un contrat ou sur le consentement explicite de la personne concernée, le responsable du traitement met en œuvre des mesures appropriées pour la sauvegarde des droits et libertés et des intérêts légitimes de la personne concernée [GDPR-Art22-2, GDPR-Art22-3]. Ces mesures comprennent au moins le droit pour la personne concernée d'obtenir une intervention humaine de la part du responsable du traitement, d'exprimer son point de vue et de contester la décision [GDPR-Art22-3].
>
> Les sources fournies ne couvrent pas d'autres mesures spécifiques en dehors de celles mentionnées ci-dessus.
>
> *Note : Ces informations sont fournies à des fins juridiques et ne constituent pas un conseil juridique.*

### q053 (en, lookup)

**Question:** What specific information must a controller provide to a data subject when the personal data have not been obtained directly from them?

**Answer** (gemini-3.5-flash-lite):

> When personal data have not been obtained from the data subject, the controller must provide the following information:
>
> - The identity and contact details of the controller and, where applicable, of the controller's representative [GDPR-Art14-1].
> - The contact details of the data protection officer, where applicable [GDPR-Art14-1].
> - The purposes of the processing for which the personal data are intended as well as the legal basis for the processing [GDPR-Art14-1].
> - The categories of personal data concerned [GDPR-Art14-1].
> - The recipients or categories of recipients of the personal data, if any [GDPR-Art14-1].
> - Where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation, along with the existence or absence of an adequacy decision by the Commission, or references to appropriate/suitable safeguards and the means to obtain a copy of them or where they have been made available [GDPR-Art14-1].
> - The period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period [GDPR-Art14-2].
> - Where processing is based on Article 6(1), point (f), the legitimate interests pursued by the controller or by a third party [GDPR-Art14-2].
> - The existence of the right to request from the controller access to and rectification or erasure of personal data, restriction of processing concerning the data subject, the right to object to processing, and the right to data portability [GDPR-Art14-2].
> - Where processing is based on Article 6(1), point (a) or Article 9(2), point (a), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal [GDPR-Art14-2].
> - The right to lodge a complaint with a supervisory authority [GDPR-Art14-2].
> - From which source the personal data originate, and if applicable, whether it came from publicly accessible sources [GDPR-Art14-2].
> - The existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject [GDPR-Art14-2].
>
> The provided sources do not cover paragraph 3 of GDPR Article 14.
>
> Please note that this is legal information and not legal advice.

### q054 (fr, obligation)

**Question:** Dans quels cas précis une entreprise de moins de 250 employés est-elle tout de même tenue de tenir un registre des activités de traitement ?

**Answer** (gemini-3.5-flash-lite):

> Une entreprise ou une organisation comptant moins de 250 employés est tout de même tenue de tenir un registre des activités de traitement si le traitement qu'elle effectue est susceptible de comporter un risque pour les droits et les libertés des personnes concernées, s'il n'est pas occasionnel, ou s'il porte notamment sur les catégories particulières de données visées à l'article 9, paragraphe 1, ou sur des données à caractère personnel relatives à des condamnations pénales et à des infractions visées à l'article 10 [GDPR-Art30-5]. Les sources fournies ne précisent pas d'autres cas que ceux mentionnés.

### q055 (fr, lookup)

**Question:** Dans quelles situations précises une autorité de surveillance du marché doit-elle inviter un fournisseur à mettre un terme à une non-conformité formelle?

**Answer** (gemini-3.5-flash-lite):

> Une autorité de surveillance du marché d’un État membre doit inviter le fournisseur concerné à mettre un terme à la non-conformité lorsqu’elle fait l’une des constatations suivantes :
> a) le marquage CE a été apposé en violation de l’article 48 [AIA-Art83-1];
> b) le marquage CE n’a pas été apposé [AIA-Art83-1];
> c) la déclaration UE de conformité visée à l’article 47 n’a pas été établie [AIA-Art83-1];
> d) la déclaration UE de conformité visée à l’article 47 n’a pas été établie correctement [AIA-Art83-1];
> e) l’enregistrement dans la base de données de l’UE visée à l’article 71 n’a pas été effectué [AIA-Art83-1];
> f) le cas échéant, il n’a pas été désigné de mandataire [AIA-Art83-1];
> g) la documentation technique n’est pas disponible [AIA-Art83-1].
>
> Les sources fournies ne traitent pas des autres types de non-conformités ou de situations en dehors de cette liste précise de non-conformités formelles.
>
> Je vous donne des informations juridiques et non des conseils juridiques.

### q056 (en, lookup)

**Question:** To what obligations may adherence to the codes of practice be limited for providers of general-purpose AI models that do not present systemic risks?

**Answer** (gemini-3.5-flash-lite):

> For providers of general-purpose AI models that do not present systemic risks, adherence to the codes of practice may be limited to the obligations provided for in Article 53, unless they explicitly declare their interest to join the full code [AIA-Art56-7].

### q057 (en, lookup)

**Question:** By what date must Member States identify and publish the list of public authorities or bodies that protect fundamental rights in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> Member States must identify the public authorities or bodies and make a list of them publicly available by 2 November 2024 [AIA-Art77-2].

### q058 (en, obligation)

**Question:** Under what specific conditions may a data transfer to a third country take place when no other provisions or derogations apply?

**Answer** (gemini-3.5-flash-lite):

> Under the GDPR, where a transfer could not be based on an adequacy decision under Article 45, appropriate safeguards under Article 46 (including binding corporate rules), and none of the specific derogations referred to in the first subparagraph of Article 49(1) are applicable, a transfer of personal data to a third country or an international organisation may take place only if all of the following conditions are met:
> - The transfer is not repetitive [GDPR-Art49-1].
> - The transfer concerns only a limited number of data subjects [GDPR-Art49-1].
> - The transfer is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject [GDPR-Art49-1].
> - The controller has assessed all the circumstances surrounding the data transfer and has, on the basis of that assessment, provided suitable safeguards with regard to the protection of personal data [GDPR-Art49-1].
> - The controller informs the supervisory authority of the transfer [GDPR-Art49-1].
> - The controller informs the data subject of the transfer and on the compelling legitimate interests pursued, in addition to providing the information referred to in Articles 13 and 14 [GDPR-Art49-1].
>
> The provided sources do not cover whether any other conditions from outside these specific provisions might also apply.

### q059 (fr, obligation)

**Question:** Est-ce qu'une organisation de protection des données peut introduire une réclamation auprès d'une autorité de contrôle sans avoir reçu de mandat de la personne concernée ?

**Answer** (gemini-3.5-flash-lite):

> Oui, les États membres peuvent prévoir que tout organisme, organisation ou association (répondant aux critères visés au paragraphe 1 de l'article 80) a le droit d'introduire une réclamation auprès de l'autorité de contrôle compétente sans qu'un mandat ne lui ait été confié par la personne concernée [GDPR-Art80-2]. Les sources fournies ne précisent pas quels États membres ont effectivement adopté cette disposition dans leur droit national.

### q060 (en, lookup)

**Question:** Within what timeframe must a supervisory authority inform a data subject about the progress or outcome of their lodged complaint to avoid the data subject having a right to an effective judicial remedy?

**Answer** (gemini-3.5-flash-lite):

> The supervisory authority must inform the data subject within three months on the progress or outcome of the complaint lodged pursuant to Article 77 to avoid the data subject having a right to an effective judicial remedy under that provision [GDPR-Art78-2].

### q061 (fr, obligation)

**Question:** Quelles informations l'autorité notifiante doit-elle fournir à la Commission concernant les organismes notifiés, et à quel moment ?

**Answer** (gemini-3.5-flash-lite):

> L'autorité notifiante fournit à la Commission, sur demande, toutes les informations utiles relatives à la notification ou au maintien de la compétence de l'organisme notifié concerné [AIA-Art37-2]. De plus, elle informe immédiatement la Commission et les autres États membres si elle conclut qu'un organisme notifié ne répond plus aux exigences ou ne s'acquitte pas de ses obligations (après avoir mené une enquête et lui avoir donné la possibilité de faire connaître son point de vue), en soumettant la désignation à des restrictions, en la suspendant ou en la retirant [AIA-Art36-4]. Enfin, elle notifie à la Commission toute modification pertinente apportée à la notification d’un organisme notifié au moyen de l’outil de notification électronique visé à l’article 30, paragraphe 2 [AIA-Art36-1].
>
> Les sources fournies ne précisent pas les délais précis (calendaires) pour la transmission des informations demandées sur la compétence ni pour la notification des modifications pertinentes.

### q062 (fr, obligation)

**Question:** Quelles sont les obligations de l'autorité notifiante en cas de restriction, de suspension ou de retrait d'une désignation d'organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> En cas de restriction, de suspension ou de retrait d'une désignation d'organisme notifié, l'autorité notifiante doit:
>
> * Soumettre la désignation à des restrictions, la suspendre ou la retirer selon la gravité du manquement [AIA-Art36-4].
> * Informer immédiatement la Commission et les autres États membres de cette décision [AIA-Art36-4].
> * Prendre les mesures nécessaires pour que les dossiers de l'organisme notifié soient conservés et mis à la disposition des autorités notifiantes des autres États membres et des autorités de surveillance du marché qui en font la demande [AIA-Art36-6].
> * Évaluer l'incidence sur les certificats délivrés par l'organisme notifié [AIA-Art36-7].
> * Transmettre un rapport sur ses conclusions à la Commission et aux autres États membres dans un délai de trois mois après avoir signalé les modifications apportées à la désignation [AIA-Art36-7].
> * Exiger de l'organisme notifié qu'il suspende ou retire, dans un délai raisonnable déterminé par elle, tous les certificats délivrés à tort afin d'assurer la conformité constante des systèmes d'IA à haut risque sur le marché [AIA-Art36-7].
> * Informer la Commission et les États membres des certificats dont elle a demandé la suspension ou le retrait [AIA-Art36-7].
> * Fournir à l'autorité nationale compétente de l'État membre où le fournisseur a son siège social toutes les informations pertinentes sur les certificats dont la suspension ou le retrait a été demandé [AIA-Art36-7].
>
> Les sources fournies ne traitent pas des potentielles obligations financières ou administratives supplémentaires que l'autorité notifiante pourrait avoir envers l'organisme notifié lui-même au-delà de ces mesures.

### q063 (fr, lookup)

**Question:** Dans quelle situation le règlement s'applique-t-il au traitement de données par un responsable du traitement non établi dans l'Union, mais dans un lieu régi par le droit d'un État membre en vertu du droit international public ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement s'applique au traitement de données à caractère personnel par un responsable du traitement qui n'est pas établi dans l'Union mais dans un lieu où le droit d'un État membre s'applique en vertu du droit international public [GDPR-Art3-3]. Les sources fournies ne couvrent pas les éventuelles conditions ou obligations spécifiques supplémentaires applicables dans cette situation.
>
> Ceci est une information juridique et non un conseil juridique.

### q064 (en, obligation)

**Question:** How can public authorities reconcile public access to official documents with the right to the protection of personal data?

**Answer** (gemini-3.5-flash-lite):

> Personal data in official documents held by a public authority, public body, or private body for the performance of a task carried out in the public interest may be disclosed in accordance with Union or Member State law to which the body is subject in order to reconcile public access to official documents with the right to the protection of personal data [GDPR-Art86].

### q065 (fr, obligation)

**Question:** Quels documents les organismes notifiés doivent-ils fournir à l'autorité notifiante pour faciliter ses activités de surveillance et d'évaluation ?

**Answer** (gemini-3.5-flash-lite):

> Les organismes notifiés mettent à la disposition de l'autorité notifiante et lui soumettent sur demande toute la documentation pertinente, y compris celle des fournisseurs, afin de lui permettre de réaliser ses activités d’évaluation, de désignation, de notification et de surveillance et pour faciliter les évaluations [AIA-Art34-3]. Les sources ne couvrent pas la question de savoir si d'autres documents spécifiques non mentionnés ici doivent être fournis.
>
> Vous fournissez des informations juridiques, et non un avis juridique.

### q066 (fr, lookup)

**Question:** Quel organe européen peut adopter des actes d'exécution pour définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle et le comité?

**Answer** (gemini-3.5-flash-lite):

> La Commission peut adopter des actes d'exécution afin de définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle, et entre ces autorités et le comité [GDPR-Art67]. Les sources fournies ne couvrent pas d'autres détails concernant cet organe européen au-delà de sa capacité à adopter ces actes d'exécution.

### q067 (en, obligation)

**Question:** Who is liable to pay compensation to a person who has suffered material or non-material damage due to an infringement of the regulation?

**Answer** (gemini-3.5-flash-lite):

> Any person who has suffered material or non-material damage as a result of an infringement of the regulation has the right to receive compensation from the controller or processor for the damage suffered [GDPR-Art82-1]. Any controller involved in processing shall be liable for the damage caused by processing which infringes the regulation [GDPR-Art82-2]. A processor shall be liable for the damage caused by processing only where it has not complied with obligations of the regulation specifically directed to processors or where it has acted outside or contrary to lawful instructions of the controller [GDPR-Art82-2]. Furthermore, where more than one controller or processor, or both a controller and a processor, are involved in the same processing and are responsible for any damage caused by processing, each controller or processor shall be held liable for the entire damage in order to ensure effective compensation of the data subject [GDPR-Art82-4].

### q068 (en, lookup)

**Question:** How does the Commission ensure appropriate coordination and cooperation between notified bodies involved in conformity assessment procedures for high-risk AI systems?

**Answer** (gemini-3.5-flash-lite):

> The Commission shall ensure that appropriate coordination and cooperation between notified bodies active in conformity assessment procedures for high-risk AI systems are put in place and properly operated in the form of a sectoral group of notified bodies [AIA-Art38-1].

### q069 (en, obligation)

**Question:** Under what conditions can Union or Member State law restrict data protection rights and obligations?

**Answer** (gemini-3.5-flash-lite):

> Union or Member State law may restrict by way of a legislative measure the scope of the obligations and rights provided for in Articles 12 to 22 and Article 34, as well as Article 5 (in so far as its provisions correspond to the rights and obligations provided for in Articles 12 to 22), under the condition that such a restriction respects the essence of the fundamental rights and freedoms and is a necessary and proportionate measure in a democratic society to safeguard certain objectives [GDPR-Art23-1].
>
> These objectives include:
> (a) national security [GDPR-Art23-1];
> (b) defence [GDPR-Art23-1];
> (c) public security [GDPR-Art23-1];
> (d) the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security [GDPR-Art23-1];
> (e) other important objectives of general public interest of the Union or of a Member State, in particular an important economic or financial interest of the Union or of a Member State, including monetary, budgetary and taxation matters, public health and social security [GDPR-Art23-1];
> (f) the protection of judicial independence and judicial proceedings [GDPR-Art23-1];
> (g) the prevention, investigation, detection and prosecution of breaches of ethics for regulated professions [GDPR-Art23-1];
> (h) a monitoring, inspection or regulatory function connected, even occasionally, to the exercise of official authority in the cases referred to in points (a) to (e) and (g) [GDPR-Art23-1];
> (i) the protection of the data subject or the rights and freedoms of others [GDPR-Art23-1];
> (j) the enforcement of civil law claims [GDPR-Art23-1].
>
> Furthermore, any such legislative measure must contain specific provisions at least, where relevant, regarding:
> (a) the purposes of the processing or categories of processing [GDPR-Art23-2];
> (b) the categories of personal data [GDPR-Art23-2];
> (c) the scope of the restrictions introduced [GDPR-Art23-2];
> (d) the safeguards to prevent abuse or unlawful access or transfer [GDPR-Art23-2];
> (e) the specification of the controller or categories of controllers [GDPR-Art23-2];
> (f) the storage periods and the applicable safeguards taking into account the nature, scope and purposes of the processing or categories of processing [GDPR-Art23-2];
> (g) the risks to the rights and freedoms of data subjects [GDPR-Art23-2]; and
> (h) the right of data subjects to be informed about the restriction, unless that may be prejudicial to the purpose of the restriction [GDPR-Art23-2].
>
> The provided sources do not cover any conditions for restricting data protection rights and obligations outside of legislative measures enacted by the Union or Member States.

### q070 (fr, lookup)

**Question:** Où sont enregistrés les systèmes d'IA à haut risque utilisés dans les domaines de la migration et de l'asile, et qui a accès à ces informations ?

**Answer** (gemini-3.5-flash-lite):

> Les systèmes d’IA à haut risque visés à l’annexe III, points 1, 6 et 7, dans les domaines des activités répressives, de la migration, de l’asile et de la gestion des contrôles aux frontières, sont enregistrés dans une section sécurisée non publique de la base de données de l’UE visée à l’article 71 [AIA-Art49-4].
>
> Seules la Commission et les autorités nationales visées à l’article 74, paragraphe 8, ont accès aux différentes sections restreintes de la base de données de l’UE [AIA-Art49-4]. Les sources fournies ne précisent pas les aspects relatifs à d'autres catégories de systèmes d'IA ou d'autres types d'utilisateurs non mentionnés dans ces articles.
>
> Ces informations relèvent d'une information juridique et non d'un conseil juridique.

### q071 (fr, lookup)

**Question:** Quelle est la durée de validité maximale des mesures provisoires qu'une autorité de contrôle peut adopter d'urgence pour protéger les droits des personnes ?

**Answer** (gemini-3.5-flash-lite):

> La durée de validité des mesures provisoires adoptées d'urgence par une autorité de contrôle pour protéger les droits et libertés des personnes concernées ne doit pas excéder trois mois [GDPR-Art66-1].
>
> Les sources fournies ne précisent pas d'autres dispositions ou prolongations possibles pour cette durée maximale spécifique de trois mois dans le cadre de la procédure d'urgence du RGPD.

### q072 (en, obligation)

**Question:** At what point and with whom must Member States consult regarding legislative or regulatory measures related to data processing?

**Answer** (gemini-3.5-flash-lite):

> Member States shall consult the supervisory authority during the preparation of a proposal for a legislative measure to be adopted by a national parliament, or of a regulatory measure based on such a legislative measure, which relates to processing [GDPR-Art36-4].

### q073 (fr, lookup)

**Question:** Dans quelles circonstances l'interdiction générale de prendre des décisions individuelles automatisées ne s'applique-t-elle pas selon le règlement ?

**Answer** (gemini-3.5-flash-lite):

> Selon les sources fournies, le droit de ne pas faire l'objet d'une décision fondée exclusivement sur un traitement automatisé, y compris le profilage, ne s'applique pas lorsque la décision :
> - est nécessaire à la conclusion ou à l'exécution d'un contrat entre la personne concernée et un responsable du traitement [GDPR-Art22-2] ;
> - est autorisée par le droit de l'Union ou le droit de l'État membre auquel le responsable du traitement est soumis, et qui prévoit également des mesures appropriées pour la sauvegarde des droits et libertés et des intérêts légitimes de la personne concernée [GDPR-Art22-2] ; ou
> - est fondée sur le consentement explicite de la personne concernée [GDPR-Art22-2].
>
> Les sources fournies ne contiennent aucune information sur les circonstances d'application de telles interdictions en vertu du Règlement IA (elles abordent uniquement le RGPD pour cette exception précise).
>
> Vous donnez des informations juridiques et non des conseils juridiques.

### q074 (en, lookup)

**Question:** What specific information must be included in the record of processing activities maintained by a controller?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the record of processing activities maintained by each controller (and, where applicable, the controller's representative) must contain all of the following information:
>
> (a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representative and the data protection officer [GDPR-Art30-1].
> (b) the purposes of the processing [GDPR-Art30-1].
> (c) a description of the categories of data subjects and of the categories of personal data [GDPR-Art30-1].
> (d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations [GDPR-Art30-1].
> (e) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards [GDPR-Art30-1].
> (f) where possible, the envisaged time limits for erasure of the different categories of data [GDPR-Art30-1].
> (g) where possible, a general description of the technical and organisational security measures referred to in Article 32(1) [GDPR-Art30-1].
> (h) the documentation of the assessment as well as the suitable safeguards referred to in the second subparagraph of Article 49(1), where applicable [GDPR-Art49-6].
>
> Please note that we provide legal information, not legal advice [Intro].

### q075 (fr, obligation)

**Question:** Que doit faire l'autorité de surveillance du marché si une non-conformité formelle persiste malgré les mesures initiales ?

**Answer** (gemini-3.5-flash-lite):

> Si la non-conformité formelle persiste, l’autorité de surveillance du marché de l’État membre concerné prend toutes les mesures appropriées et proportionnées pour restreindre ou interdire la mise à disposition du système d’IA à haut risque sur le marché ou pour assurer son rappel ou son retrait sans tarder du marché [AIA-Art83-2].
>
> Vous donnez des informations juridiques et non un avis juridique.

### q076 (fr, lookup)

**Question:** Quel organisme facilite la révision des codes de bonne pratique et évalue les normes disponibles ?

**Answer** (gemini-3.5-flash-lite):

> Le Bureau de l’IA encourage et facilite le réexamen et l’adaptation des codes de bonne pratique, et il participe à l’évaluation des normes disponibles [AIA-Art56-8].

### q077 (en, obligation)

**Question:** What can a public authority protecting fundamental rights do if the available documentation is not enough to determine if a high-risk AI system infringes Union law?

**Answer** (gemini-3.5-flash-lite):

> Where the documentation is insufficient to ascertain whether an infringement of obligations under Union law protecting fundamental rights has occurred, the relevant public authority or body may make a reasoned request to the market surveillance authority to organise testing of the high-risk AI system through technical means [AIA-Art77-3]. The market surveillance authority shall then organise this testing with the close involvement of the requesting public authority or body within a reasonable time following the request [AIA-Art77-3].

### q078 (en, obligation)

**Question:** What action must Member States take regarding national provisions that set limits on personal data transfers to third countries for important reasons of public interest in the absence of an adequacy decision?

**Answer** (gemini-3.5-flash-lite):

> Member States must notify the Commission of any provisions that, for important reasons of public interest, expressly set limits to the transfer of specific categories of personal data to a third country or an international organisation in the absence of an adequacy decision [GDPR-Art49-5].

### q079 (en, lookup)

**Question:** In which courts can a data subject bring judicial proceedings against a controller or processor?

**Answer** (gemini-3.5-flash-lite):

> Proceedings against a controller or a processor shall be brought before the courts of the Member State where the controller or processor has an establishment [GDPR-Art79-2]. Alternatively, such proceedings may be brought before the courts of prisons or the Member State where the data subject has his or her habitual residence, unless the controller or processor is a public authority of a Member State acting in the exercise of its public powers [GDPR-Art79-2]. (Note: the provided sources do not cover the specific term "prisons", which appears to be a typographical anomaly in this context, but the rule applies regarding the Member State of the data subject's habitual residence [GDPR-Art79-2].)
>
> You give legal information, not legal advice. Never say whether a specific company or system is compliant.

### q080 (en, lookup)

**Question:** What kind of bodies or organisations can a data subject mandate to lodge a complaint or exercise data protection rights on their behalf?

**Answer** (gemini-3.5-flash-lite):

> A data subject has the right to mandate a not-for-profit body, organisation, or association that has been properly constituted in accordance with the law of a Member State, has statutory objectives which are in the public interest, and is active in the field of the protection of data subjects' rights and freedoms regarding the protection of their personal data [GDPR-Art80-1].
>
> The provided sources do not cover whether other types of bodies or organisations outside of these criteria can be mandated.
>
> You give legal information, not legal advice.

### q081 (en, obligation)

**Question:** What must a supervisory authority do when proceedings are brought against its decision that was preceded by an opinion or decision of the Board in the consistency mechanism?

**Answer** (gemini-3.5-flash-lite):

> When proceedings are brought against a decision of a supervisory authority which was preceded by an opinion or a decision of the Board in the consistency mechanism, the supervisory authority shall forward that opinion or decision to the court [GDPR-Art78-4].

### q082 (en, lookup)

**Question:** What are the specific tasks of the scientific panel of independent experts regarding cross-border market surveillance activities and the Union safeguard procedure?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the scientific panel of independent experts has the following specific tasks regarding cross-border market surveillance activities and the Union safeguard procedure:
>
> * Supporting cross-border market surveillance activities as referred to in Article 74(11), without prejudice to the powers of market surveillance authorities [AIA-Art68-3].
> * Supporting the AI Office in carrying out its duties in the context of the Union safeguard procedure pursuant to Article 81 [AIA-Art68-3].
>
> The provided sources do not cover any further details or specific duties beyond supporting these activities as stated.

### q083 (en, lookup)

**Question:** Which institution is responsible for investigating cases where there are doubts regarding the competence of a notified body?

**Answer** (gemini-3.5-flash-lite):

> The Commission shall investigate all cases where there are reasons to doubt the competence of a notified body or the continued fulfilment by a notified body of the requirements laid down in Article 31 and of its applicable responsibilities [AIA-Art37-1].

### q084 (fr, lookup)

**Question:** Par quel moyen l'autorité notifiante doit-elle informer la Commission et les autres États membres des modifications apportées à la notification d'un organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> L'autorité notifiante notifie toute modification pertinente apportée à la notification d'un organisme notifié au moyen de l'outil de notification électronique visé à l'article 30, paragraphe 2 [AIA-Art36-1].

### q085 (fr, lookup)

**Question:** Dans quelles conditions le règlement s'applique-t-il au traitement des données effectué par un établissement d'un responsable du traitement, indépendamment du lieu où se déroule le traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement s'applique au traitement des données à caractère personnel effectué dans le cadre des activités d'un établissement d'un responsable du traitement sur le territoire de l'Union, que le traitement ait lieu ou non dans l'Union [GDPR-Art3-1]. Les sources fournies ne traitent pas des conditions d'application du règlement dans d'autres cas de figure qui ne relèveraient pas de l'établissement d'un responsable du traitement sur le territoire de l'Union.

### q086 (fr, obligation)

**Question:** De quelle manière les organismes notifiés doivent-ils tenir compte de la taille des fournisseurs et de la complexité des systèmes d'IA dans leurs activités ?

**Answer** (gemini-3.5-flash-lite):

> Les organismes notifiés disposent de procédures pour accomplir leurs activités qui tiennent dûment compte de la taille des fournisseurs, du secteur dans lequel ils exercent leurs activités, de leur structure et du degré de complexité du système d’IA concerné [AIA-Art31-8]. De plus, dans l'exercice de leurs activités, ils évitent les charges inutiles pour les fournisseurs et tiennent dûment compte de ces mêmes facteurs (taille, secteur, structure et complexité du système d’IA à haut risque), en particulier afin de réduire au minimum les charges administratives et les coûts de mise en conformité pour les microentreprises et les petites entreprises [AIA-Art34-2]. Tout en tenant compte de ces aspects, l'organisme notifié respecte néanmoins le degré de rigueur et le niveau de protection requis pour garantir la conformité du système d’IA à haut risque avec les exigences du règlement [AIA-Art34-2].

### q087 (en, lookup)

**Question:** What right does a controller or processor have after paying full compensation for damage caused by processing?

**Answer** (gemini-3.5-flash-lite):

> Where a controller or processor has paid full compensation for the damage suffered, that controller or processor is entitled to claim back from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage, in accordance with the conditions set out in paragraph 2 [GDPR-Art82-5].

### q088 (en, obligation)

**Question:** How must notified bodies be involved in the sectoral group that the Commission sets up for them?

**Answer** (gemini-3.5-flash-lite):

> Notified bodies must participate in the sectoral group of notified bodies, either directly or through designated representatives [AIA-Art38-2].

### q089 (fr, lookup)

**Question:** Quels éléments spécifiques les mesures législatives limitant la portée des obligations et des droits du RGPD doivent-elles contenir au minimum ?

**Answer** (gemini-3.5-flash-lite):

> Les mesures législatives limitant la portée des obligations et des droits du RGPD doivent contenir, le cas échéant, des dispositions spécifiques relatives au moins aux éléments suivants :
> - aux finalités du traitement ou des catégories de traitement [GDPR-Art23-2] ;
> - aux catégories de données à caractère personnel [GDPR-Art23-2] ;
> - à l'étendue des limitations introduites [GDPR-Art23-2] ;
> - aux garanties destinées à prévenir les abus ou l'accès ou le transfert illicites [GDPR-Art23-2] ;
> - à la détermination du responsable du traitement ou des catégories de responsables du traitement [GDPR-Art23-2] ;
> - aux durées de conservation et aux garanties applicables, en tenant compte de la nature, de la portée et des finalités du traitement ou des catégories de traitement [GDPR-Art23-2] ;
> - aux risques pour les droits et libertés des personnes concernées [GDPR-Art23-2] ;
> - au droit des personnes concernées d'être informées de la limitation, à moins que cela risque de nuire à la finalité de la limitation [GDPR-Art23-2].

### q090 (en, obligation)

**Question:** Who is required to register a non-high-risk AI system in the EU database before it is placed on the market or put into service?

**Answer** (gemini-3.5-flash-lite):

> Before an AI system for which the provider has concluded that it is not high-risk according to Article 6(3) is placed on the market or put into service, the provider or, where applicable, the authorised representative shall register themselves and that system in the EU database [AIA-Art49-2].

### q091 (fr, lookup)

**Question:** Dans quel délai et à quelle majorité le comité doit-il adopter un avis ou une décision contraignante dans le cadre de la procédure d'urgence ?

**Answer** (gemini-3.5-flash-lite):

> Dans le cadre de la procédure d'urgence, l'avis d'urgence ou la décision contraignante d'urgence est adopté dans un délai de deux semaines à la majorité simple des membres du comité [GDPR-Art66-4].

### q092 (fr, obligation)

**Question:** Dans quelle situation précise le responsable du traitement est-il tenu de consulter l'autorité de contrôle avant de procéder au traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement consulte l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données effectuée au titre de l'article 35 indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque [GDPR-Art36-1]. Les sources ne couvrent pas d'autres situations potentielles de consultation préalable en dehors de celle-ci et de celle prévue par le droit des États membres pour une mission d'intérêt public.

### q093 (en, obligation)

**Question:** How should the development of benchmarks and measurement methodologies for AI systems be encouraged, and who is involved in this process?

**Answer** (gemini-3.5-flash-lite):

> To address the technical aspects of measuring appropriate levels of accuracy and robustness (and any other relevant performance metrics), the Commission shall encourage the development of benchmarks and measurement methodologies [AIA-Art15-2]. This process is carried out in cooperation with relevant stakeholders and organisations, such as metrology and benchmarking authorities [AIA-Art15-2].

### q094 (en, lookup)

**Question:** What right does a data subject have regarding decisions based solely on automated processing, including profiling?

**Answer** (gemini-3.5-flash-lite):

> The data subject has the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her [GDPR-Art22-1]. Furthermore, in cases where such a decision is necessary for entering into or performing a contract, or is based on the data subject's explicit consent, the data subject has the right to obtain human intervention on the part of the controller, to express his or her point of view, and to contest the decision [GDPR-Art22-3, GDPR-Art22-2]. Additionally, the data subject has the right to obtain confirmation of whether personal data are processed, access to that data, and specific information including the existence of automated decision-making and meaningful information about the logic involved, significance, and envisaged consequences [GDPR-Art15-1].

### q095 (en, lookup)

**Question:** What additional information must a controller provide to a data subject when personal data have not been obtained directly from them, in order to ensure fair and transparent processing?

**Answer** (gemini-3.5-flash-lite):

> In addition to the information required under paragraph 1 of Article 14, the controller must provide the data subject with the following information necessary to ensure fair and transparent processing:
> - The period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period [GDPR-Art14-2].
> - Where the processing is based on Article 6(1), point (f), the legitimate interests pursued by the controller or by a third party [GDPR-Art14-2].
> - The existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject and to object to processing as well as the right to data portability [GDPR-Art14-2].
> - Where processing is based on Article 6(1), point (a) or Article 9(2), point (a), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal [GDPR-Art14-2].
> - The right to lodge a complaint with a supervisory authority [GDPR-Art14-2].
> - From which source the personal data originate, and if applicable, whether it came from publicly accessible sources [GDPR-Art14-2].
> - The existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject [GDPR-Art14-2].
>
> The provided sources do not cover whether any other specific rules or exceptions apply to this additional information beyond what is stated in Article 14.

### q096 (en, obligation)

**Question:** Who must make the record of processing activities available to the supervisory authority upon request?

**Answer** (gemini-3.5-flash-lite):

> The controller or the processor and, where applicable, the controller's or the processor's representative, shall make the record available to the supervisory authority on request [GDPR-Art30-4].

### q097 (en, obligation)

**Question:** How must national public authorities handle information and documentation they obtain regarding fundamental rights protection in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> Any information or documentation obtained by national public authorities or bodies protecting fundamental rights in relation to high-risk AI systems must be treated in accordance with the confidentiality obligations set out in Article 78 [AIA-Art77-4].
>
> *(Note: The provided sources do not cover additional handling requirements outside of these confidentiality obligations.)*

### q098 (en, lookup)

**Question:** What conditions allow for the transfer of personal data to a third country when there is neither an adequacy decision nor appropriate safeguards in place?

**Answer** (gemini-3.5-flash-lite):

> In the absence of an adequacy decision and appropriate safeguards (including binding corporate rules), a transfer or a set of transfers of personal data to a third country or an international organisation may take place only on one of the following conditions:
> (a) the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards;
> (b) the transfer is necessary for the performance of a contract between the data subject and the controller or the implementation of pre-contractual measures taken at the data subject's request;
> (c) the transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person;
> (d) the transfer is necessary for important reasons of public interest;
> (e) the transfer is necessary for the establishment, exercise or defence of legal claims;
> (f) the transfer is necessary in order to protect the vital interests of the data subject or of other persons, where the data subject is physically or legally incapable of giving consent; or
> (g) the transfer is made from a register which according to Union or Member State law is intended to provide information to the public and which is open to consultation either by the public in general or by any person who can demonstrate a legitimate interest, but only to the extent that the conditions laid down by Union or Member State law for consultation are fulfilled in the particular case [GDPR-Art49-1].
>
> Furthermore, if none of those specific derogations apply and there is no adequacy decision or appropriate safeguards (including binding corporate rules), a transfer to a third country or an international organisation may take place only if all of the following additional conditions are met: the transfer is not repetitive, concerns only a limited number of data subjects, is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject, and the controller has assessed all the circumstances surrounding the data transfer and has on the basis of that assessment provided suitable safeguards with regard to the protection of personal data [GDPR-Art49-1]. In such cases, the controller must also inform the supervisory authority of the transfer, and inform the data subject of the transfer and on the compelling legitimate interests pursued in addition to providing the information referred to in Articles 13 and 14 [GDPR-Art49-1].
>
> The provided sources do not cover any other conditions or rules outside of these specific GDPR provisions.

### q099 (fr, obligation)

**Question:** Quels recours une personne physique ou morale possède-t-elle face à une décision juridiquement contraignante d'une autorité de contrôle qui la concerne ?

**Answer** (gemini-3.5-flash-lite):

> Sans préjudice de tout autre recours administratif ou extrajudiciaire, toute personne physique ou morale a le droit de former un recours juridictionnel effectif contre une décision juridiquement contraignante d'une autorité de contrôle qui la concerne [GDPR-Art78-1].

### q100 (en, lookup)

**Question:** What aspects regarding the scientific panel and its members must be included in the implementing act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the implementing act adopted by the Commission to establish the scientific panel must include provisions on the conditions, procedures, and detailed arrangements for the scientific panel and its members to issue alerts, and to request the assistance of the AI Office for the performance of the tasks of the scientific panel [AIA-Art68-1, AIA-Art68-5]. The provided sources do not cover what other specific aspects must be included in that implementing act beyond these provisions.

### q101 (en, obligation)

**Question:** What actions can the Commission take if a Member State fails to implement corrective measures after being informed that a notified body no longer meets its requirements?

**Answer** (gemini-3.5-flash-lite):

> Where a Member State fails to take the necessary corrective measures after the Commission informs it that a notified body no longer meets the requirements for its notification, the Commission may, by means of an implementing act, suspend, restrict, or withdraw the designation [AIA-Art37-4]. This implementing act must be adopted in accordance with the examination procedure referred to in Article 98(2) [AIA-Art37-4].

### q161 (en, not_covered)

**Question:** What specific interoperability requirements must gatekeepers implement for their core platform messaging services under the Digital Markets Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q163 (en, not_covered)

**Question:** What are the specific global and European turnover thresholds that require a concentration to be notified to the European Commission under the EU Merger Regulation?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q165 (en, not_covered)

**Question:** What are the mandatory vulnerability reporting timelines for manufacturers under the EU Cyber Resilience Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q167 (fr, not_covered)

**Question:** Quelles sont les obligations de garantie légale de conformité pour un téléviseur intelligent vendu à un consommateur en France?

**Answer** (refused (not_covered)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.

### q169 (en, not_covered)

**Question:** What are the VAT registration thresholds for a business selling physical goods online to consumers in other EU member states?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q171 (en, not_covered)

**Question:** What are the specific minimum capital requirements and prudential safeguards for licensing crypto-asset service providers under the Markets in Crypto-Assets (MiCA) regulation?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q173 (en, not_covered)

**Question:** What are the exact technical protocols required by the revised Payment Services Directive (PSD2) for implementing multi-factor authentication in cross-border e-commerce transactions?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q174 (en, not_covered)

**Question:** What specific font size and contrast ratios are mandated for reflowable e-books under the European Accessibility Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q176 (en, not_covered)

**Question:** What is the maximum surcharge a mobile network operator can apply for data roaming within the European Union under current telecom regulations?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q178 (en, not_covered)

**Question:** What are the technical specifications for issuing a European Digital Identity Wallet under the eIDAS regulation, and how do member states handle cross-border recognition of these wallets?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h015 (en, obligation)

**Question:** We are a Canadian app with no EU office, but we track where our users in France go. Does the GDPR apply to us?

**Answer** (refused (uncited)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### h016 (fr, obligation)

**Question:** Une banque peut-elle refuser mon crédit par un algorithme, sans qu'aucun humain n'intervienne ?

**Answer** (gemini-3.5-flash-lite):

> La personne concernée a le droit de ne pas faire l'objet d'une décision fondée exclusivement sur un traitement automatisé, y compris le profilage, produisant des effets juridiques la concernant ou l'affectant de manière significative de façon similaire [GDPR-Art22-1].
>
> Cependant, ce principe ne s'applique pas si la décision est nécessaire à la conclusion ou à l'exécution d'un contrat entre la personne concernée et un responsable du traitement, si elle est autorisée par le droit de l'Union ou d'un État membre (avec des mesures appropriées de sauvegarde), ou si elle est fondée sur le consentement explicite de la personne concernée [GDPR-Art22-2].
>
> Dans les cas où une telle décision est nécessaire à un contrat ou autorisée par le consentement explicite, le responsable du traitement met en œuvre des mesures appropriées pour sauvegarder les droits, libertés et intérêts légitimes de la personne concernée, ce qui inclut au moins le droit d'obtenir une intervention humaine de la part du responsable du traitement, d'exprimer son point de vue et de contester la décision [GDPR-Art22-3].
>
> Les sources fournies ne permettent pas de déterminer si le refus d'un crédit spécifique par une banque remplit les conditions d'exemption du paragraphe 2 (comme la nécessité pour un contrat ou le consentement).

### h017 (en, obligation)

**Question:** A high-risk AI system is sold without its CE marking but otherwise works safely. Can the authorities still make the provider fix that?

**Answer** (gemini-3.5-flash-lite):

> Providers of high-risk AI systems must ensure that their systems undergo the relevant conformity assessment procedure prior to being placed on the market or put into service [AIA-Art16]. They are also required to draw up an EU declaration of conformity and affix the CE marking to indicate conformity with the Regulation [AIA-Art16]. Furthermore, upon a reasoned request of a national competent authority, providers must demonstrate the conformity of the high-risk AI system with the requirements set out in Section 2, which includes taking necessary corrective actions [AIA-Art16]. The provided sources do not cover whether authorities can make the provider fix the specific issue of a missing CE marking when the system otherwise works safely.
>
> You give legal information, not legal advice.

### h018 (en, obligation)

**Question:** Before selling a high-risk AI system that screens job candidates, does the provider have to put it on some official EU list?

**Answer** (gemini-3.5-flash-lite):

> Before placing a high-risk AI system listed in Annex III on the market (with the exception of high-risk AI systems referred to in point 2 of Annex III), the provider or their authorised representative must register themselves and their system in the EU database referred to in Article 71 [AIA-Art49-1]. The provided sources do not cover whether a high-risk AI system that screens job candidates falls under Annex III or under point 2 of Annex III.
>
> You give legal information, not legal advice.

### h019 (fr, obligation)

**Question:** Une fuite de mes données m'a causé du stress, mais aucune perte d'argent. Puis-je demander une indemnisation ?

**Answer** (gemini-3.5-flash-lite):

> Toute personne ayant subi un dommage matériel ou moral du fait d'une violation du règlement a le droit d'obtenir du responsable du traitement ou du sous-traitant réparation du préjudice subi [GDPR-Art82-1]. Les sources fournies ne précisent pas explicitement si le stress constitue un dommage moral réparable.
