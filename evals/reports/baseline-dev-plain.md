# Retrieval report: baseline-dev-plain

Baseline: fixed 150-word windows (25 shared) ignoring structure, dense BGE-M3, cosine similarity, no rerank. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.375 |
| **Recall@5** | **0.650** [0.45, 0.85] |
| Recall@10 | 0.750 |
| Recall@20 | 0.825 |
| MRR@10 | 0.504 [0.32, 0.69] |
| nDCG@10 | 0.547 |
| ms / query | 141 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 0.654 | 0.494 |
| fr | 7 | 0.643 | 0.524 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.250 | 0.100 |
| definition | 1 | 0.000 | 0.000 |
| lookup | 12 | 0.625 | 0.560 |
| obligation | 5 | 1.000 | 0.633 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Rec130 |
| q011 (fr) | GDPR-Art14 | 3 | GDPR-Art13, GDPR-Art12, GDPR-Art14 |
| q013 (fr) | GDPR-Art36 | 3 | GDPR-Art35, GDPR-Rec94, GDPR-Art36 |
| q007 (en) | AIA-Art56 | 4 | AIA-Rec179, AIA-Rec116, AIA-Rec173 |
| q012 (en) | GDPR-Art22 | 4 | GDPR-Rec71, GDPR-Rec70, GDPR-Art21 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 5 | AIA-Rec131, AIA-Art71, AIA-AnnexVIII |
| q010 (en) | GDPR-Art3 | 9 | GDPR-Rec23, GDPR-Rec24, AIA-Art74 |
| q014 (en) | GDPR-Art49 | 9 | GDPR-Art44, GDPR-Rec101, GDPR-Art46 |
| q001 (en) | AIA-AnnexII | 15 | AIA-Art5, AIA-Rec42, AIA-Rec32 |
| q009 (en) | AIA-Art83 | 29 | AIA-Art23, AIA-Art48, AIA-Rec128 |
| q002 (fr) | AIA-AnnexV | none | AIA-Art46, AIA-Art47, AIA-Art42 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | none | AIA-Art76, AIA-Rec59, AIA-Rec70 |

## Answers: `plain`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 22 |
| in_scope | 20 |
| out_of_scope | 2 |
| refusal_rate | 0.0 |
| false_refusal_rate | 0.0 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | None |
| citation_precision_lenient | None |
| faithfulness | 0.9886 |
| faithfulness_ci95 | (0.9659, 1.0) |
| judged | 22 |
| judge_failed | 0 |
| uncited_sentences | 2.95 |
| input_tokens | 21837 |
| output_tokens | 2483 |

### q001 (en, lookup)

**Question:** Is trafficking in human beings one of the crimes for which the police may be allowed to use real-time facial recognition in public spaces to locate a suspect?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, yes. The use of 'real-time' remote biometric identification systems in publicly accessible spaces for law enforcement is permitted if it is strictly necessary for "the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons."

Judge: 4/5. The answer correctly notes trafficking is listed as an objective, but the source does not state it is for locating a suspect.

### q002 (fr, lookup)

**Question:** Quelles mentions doit contenir la déclaration UE de conformité d'un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte fourni, la déclaration UE de conformité doit contenir :
>
> * Les informations qui figurent à l'annexe V.
> * Toutes les informations nécessaires à l'identification de la législation d'harmonisation de l'Union à laquelle la déclaration se rapporte (lorsque le système est soumis à plusieurs actes législatifs d'harmonisation).
>
> Elle doit également identifier le système d'IA à haut risque pour lequel elle a été établie et attester que ce système satisfait aux exigences énoncées à la section 2.

Judge: 5/5. All statements in the answer are directly supported by the provided source excerpts.

### q003 (en, obligation)

**Question:** How must a high-risk AI system that keeps learning after deployment be built so that its own biased outputs do not feed back into future decisions?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, high-risk AI systems that continue to learn after being placed on the market or put into service must be developed in such a way as to:
>
> 1. **Eliminate or reduce as far as possible** the risk of possibly biased outputs influencing inputs for future operations (feedback loops).
> 2. **Ensure that any such feedback loops are duly addressed** with appropriate mitigation measures.

Judge: 5/5. All statements in the answer are directly supported by the cited provisions of the AI Act.

### q004 (en, lookup)

**Question:** If a notified body stops its conformity assessment activities, how long can the certificates it issued remain valid?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the certificates of the notified body may remain valid for a period of **nine months** after the cessation of the notified body’s activities (provided that another notified body has confirmed in writing that it will assume responsibilities for the high-risk AI systems covered by those certificates).

Judge: 5/5. All claims in the answer are directly stated in the source.

### q005 (fr, lookup)

**Question:** Qui peut enquêter lorsqu'on doute qu'un organisme notifié soit encore compétent ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte (Article 37), **la Commission** enquête, s'il y a lieu, sur tous les cas où il existe des raisons de douter de la compétence d'un organisme notifié ou du respect continu de ses exigences et responsabilités.
>
> De plus, **l'autorité notifiante** procède également sans retard à une enquête avec la plus grande diligence lorsqu'elle a des raisons suffisantes de considérer qu'un organisme notifié ne répond plus aux exigences ou ne s'acquitte pas de ses obligations.

Judge: 5/5. All statements in the answer are directly supported by the provided source excerpts.

### q006 (en, obligation)

**Question:** Does a public authority that starts using a high-risk AI system to decide who receives social benefits have to register that use in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, yes. Deployers of high-risk AI systems that are public authorities, agencies, bodies, or Union institutions, offices, and agencies must register themselves, select the system, and register its use in the EU database before using/putting into service a high-risk AI system listed in the relevant annex (with specific exceptions, such as certain high-risk systems listed in point 2 of Annex III or specific systems in law enforcement, migration, asylum, and border control management which have different registration requirements).

Judge: 5/5. All statements in the answer are directly supported by the cited EU AI Regulation sources.

### q007 (en, lookup)

**Question:** Who facilitates the drawing up of codes of practice for general-purpose AI models, and by when were they supposed to be ready?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context:
>
> * **Who facilitates/draws up the codes of practice:** The **AI Office** may invite providers of general-purpose AI models, as well as relevant national competent authorities, to participate in the drawing-up of codes of practice. They should also collaborate with relevant national competent authorities, and could consult with civil society organisations, other relevant stakeholders, and experts (including the Scientific Panel). Additionally, civil society organisations, industry, academia, and other relevant stakeholders (such as downstream providers and independent experts) may support the process.
> * **By when they were supposed to be ready:** Codes of practice should be ready by **2 May 2025**.

Judge: 5/5. All statements about who facilitates the drawing up of codes of practice and the deadline are directly supported by the provided sources.

### q008 (fr, lookup)

**Question:** Quelles conditions doivent remplir les experts du groupe scientifique qui conseille le Bureau de l'IA ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte (notamment l'article 68 et les passages associés), les experts du groupe scientifique doivent remplir les conditions suivantes :
>
> 1. **Expertise et compétences** : Disposer d'une expertise à la pointe des connaissances scientifiques ou techniques, ainsi que d'une expertise et d'une compétence particulières dans le domaine de l’IA.
> 2. **Indépendance** : Être indépendants vis-à-vis de tout fournisseur de systèmes d’IA ou de modèles d’IA à usage général.
> 3. **Capacités professionnelles** : Être capables de mener des activités, de s'acquitter de leurs tâches avec diligence, impartialité, précision et objectivité.
> 4. **Confidentialité** : Veiller à la confidentialité des informations et des données obtenues dans l’exercice de leurs tâches et activités.

Judge: 5/5. All conditions listed in the answer are directly stated in the provided sources.

### q009 (en, definition)

**Question:** Which situations count as formal non-compliance of a high-risk AI system, such as a missing CE marking?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the situations that indicate a high-risk AI system is not in conformity (non-compliance) include:
>
> * When it does not bear the required CE marking.
> * When it is not accompanied by a copy of the EU declaration of conformity and instructions for use.
> * When the provider, importer, or distributor has not complied with their respective obligations (such as the provider drawing up technical documentation, carrying out the relevant conformity assessment procedure, or appointing an authorised representative).
> * When the system itself is falsified or accompanied by falsified documentation.

Judge: 5/5. All listed situations are directly stated in the cited articles of the AI Act.

### q010 (en, lookup)

**Question:** Does the GDPR apply to a company based outside the EU that tracks the online behaviour of people in the EU?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, **yes**, the processing of personal data by a controller or processor not established in the Union is subject to this Regulation (the GDPR) when it is related to the monitoring of the behaviour of data subjects who are in the Union, in so far as their behaviour takes place within the Union.
>
> To determine if an activity is considered monitoring behaviour, it must be ascertained whether natural persons are tracked on the internet, which includes the potential subsequent use of personal data processing techniques such as profiling a natural person, particularly to make decisions concerning them or to analyze or predict their preferences, behaviors, and attitudes.

Judge: 5/5. All statements in the answer are directly supported by the provided GDPR excerpts.

### q011 (fr, obligation)

**Question:** Lorsque des données personnelles n'ont pas été collectées auprès de la personne concernée, dans quel délai le responsable du traitement doit-il l'informer ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, lorsque les données à caractère personnel n'ont pas été collectées auprès de la personne concernée, le responsable du traitement doit fournir les informations :
>
> * Dans un délai raisonnable après avoir obtenu les données à caractère personnel, mais **au plus tard dans un délai d'un mois**, compte tenu des circonstances particulières dans lesquelles les données sont traitées.
> * Ou, si les données doivent être utilisées pour la communication avec la personne concernée, **au plus tard au moment de la première communication** avec cette personne.
> * Ou, si une communication à un autre destinataire est envisagée, **au plus tard lorsque les données sont divulguées pour la première fois**.

Judge: 5/5. All statements in the answer are directly supported by GDPR Art 14 source.

### q012 (en, lookup)

**Question:** Can a bank reject my loan application based only on an automated decision, with no human involved?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, **no**, you generally have the right not to be subject to a decision based solely on automated processing (with no human intervention) that produces legal effects or similarly significantly affects you. The text specifically cites the "automatic refusal of an online credit application [...] without any human intervention" as an example of this.
>
> However, paragraph 1 (which grants this right) does not apply if the decision:
> 1. Is necessary for entering into, or the performance of, a contract between you and a data controller;
> 2. Is authorized by Union or Member State law to which the controller is subject (which also lays down suitable measures to safeguard your rights, freedoms, and legitimate interests); or
> 3. Is based on your explicit consent.
>
> In cases where the decision is based on a contract or explicit consent, the data controller is required to implement suitable measures to safeguard your rights, freedoms, and legitimate interests.

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR articles and recitals.

### q013 (fr, obligation)

**Question:** Dans quel cas le responsable du traitement doit-il consulter l'autorité de contrôle avant de commencer un traitement ?

**Answer** (gemini-3.5-flash-lite):

> En vous basant sur le contexte, le responsable du traitement doit consulter l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données indique que le traitement **présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque**.

Judge: 5/5. The answer exactly matches the condition described in GDPR Art. 36 as cited in the source.

### q014 (en, lookup)

**Question:** Can personal data be sent to a country without an adequacy decision if the person explicitly agrees to the transfer?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of whether personal data can be sent to a country without an adequacy decision based on the explicit agreement or consent of the person. Therefore, the context does not provide enough information to answer this question.

Judge: 5/5. The answer correctly states that the provided sources do not address consent as a basis for transfers without an adequacy decision.

### q015 (en, lookup)

**Question:** In an emergency, can a national data protection authority act on its own without going through the cooperation procedure with other authorities, and for how long?

**Answer** (gemini-3.5-flash-lite):

> Yes, to protect the rights and freedoms of data subjects, a supervisory authority may—by way of derogation from the consistency mechanism or the cooperation procedure—immediately adopt provisional measures intended to produce legal effects on its own territory.
>
> The specified period of validity for these measures **shall not exceed three months**.

Judge: 5/5. The answer's statements are directly supported by GDPR-Art66 and GDPR-Rec136.

### q016 (en, lookup)

**Question:** What can I do if the data protection authority does not deal with my complaint?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, if a supervisory authority (data protection authority) does not handle your complaint, or does not inform you within three months on the progress or outcome of the complaint, you have the right to an **effective judicial remedy** against the supervisory authority (pursuant to Article 78).
>
> Proceedings against the supervisory authority must be brought before the courts of the Member State where the supervisory authority is established.

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR provisions.

### q017 (fr, lookup)

**Question:** Devant quels tribunaux puis-je agir contre une entreprise qui a violé mes droits au titre du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, vous pouvez intenter une action contre un responsable du traitement ou un sous-traitant devant les juridictions de l'un des États membres suivants :
>
> 1. L'État membre dans lequel le responsable du traitement ou le sous-traitant **dispose d'un établissement**.
> 2. **Alternativement**, l'État membre dans lequel la personne concernée (le data subject) a **sa résidence habituelle** *(sauf si le responsable du traitement ou le sous-traitant est une autorité publique d'un État membre agissant dans l'exercice de ses prérogatives de puissance publique)*.

Judge: 5/5. All claims in the answer are directly stated in the GDPR Article 79 source.

### q018 (en, obligation)

**Question:** If a processor ignores the controller's instructions and this causes damage to someone, does the processor have to pay compensation?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, yes. A processor is liable for the damage caused by processing where it has "acted outside or contrary to lawful instructions of the controller." Additionally, the context states that a processor shall be liable for damage caused by processing which infringes the Regulation, and that data subjects should receive full and effective compensation for the damage they have suffered.

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR articles and recitals.

### q019 (en, cross_law)

**Question:** We provide an AI tool that screens job applicants. What must our GDPR record of processing activities contain, and does the AI Act also require us to register the tool in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of what a "GDPR record of processing activities" must contain.
>
> However, regarding the registration of the AI tool in an EU database under the AI Act:
> * If you are a **public authority, agency, or body**, you are required to register yourself in the EU database and select the system you envisage to use before using a high-risk AI system listed in the annex to the Regulation.
> * If you are **another type of deployer** (not a public authority, agency, or body), you are entitled to register voluntarily.
> * Additionally, any **substantial modification** of high-risk AI systems must also be registered in the EU database.
> * Note: High-risk AI systems in the area of **critical infrastructure** should *only* be registered at the national level, and registration for high-risk AI systems in **law enforcement, migration, asylum, and border control management** must be fulfilled in a secure non-public section of the EU database.

Judge: 5/5. All statements in the answer are directly supported by the provided AI Act source excerpts.

### q020 (fr, cross_law)

**Question:** Une association de défense des droits peut-elle agir au nom de personnes discriminées par un système d'IA, et quelles autorités peuvent exiger la documentation de ce système ?

**Answer** (gemini-3.5-flash-lite):

> En vous basant sur le contexte fourni :
>
> * **Concernant l'action d'une association de défense des droits au nom de personnes discriminées :** Le texte ne contient aucune information permettant de dire si une association de défense des droits peut ou non agir au nom de ces personnes.
> * **Concernant les autorités pouvant exiger la documentation :** Les autorités ou organismes publics nationaux qui supervisent ou font respecter les obligations au titre du droit de l’Union visant à protéger les droits fondamentaux (y compris le droit à la non-discrimination, les organismes chargés des questions d’égalité et les autorités de protection des données) sont habilités à demander toute documentation créée ou conservée en vertu du règlement et à y avoir accès, lorsque c'est nécessaire à l'accomplissement effectif de leur mandat.

Judge: 5/5. All statements in the answer are consistent with the provided sources.

### q021 (en, not_covered)

**Question:** What fines can the European Commission impose on gatekeepers that breach the Digital Markets Act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of "gatekeepers" or the "Digital Markets Act."
>
> The context does, however, mention that the European Commission may impose fines on **providers of general-purpose AI models** not exceeding 3% of their annual total worldwide turnover in the preceding financial year or EUR 15 000 000 (whichever is higher), when they intentionally or negligently infringe relevant provisions or fail to comply with requests/provide accurate information.

Judge: 5/5. All statements in the answer are consistent with the provided sources, which discuss AI model fines and do not mention DMA gatekeepers.

### q022 (fr, not_covered)

**Question:** Quelles obligations le règlement sur les données (Data Act) impose-t-il aux fabricants d'objets connectés ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte fourni, il n'y a aucune information concernant des obligations imposées par le règlement sur les données (*Data Act*) aux fabricants d'objets connectés. Le texte aborde l'intelligence artificielle, les modèles d'IA à usage général, la protection des données personnelles (RGPD), le Contrôleur européen de la protection des données et les sanctions, mais il ne mentionne pas les objets connectés ni leurs fabricants.

Judge: 5/5. The answer correctly states that the provided sources contain no information on Data Act obligations for manufacturers of connected objects.
