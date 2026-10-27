# Retrieval report: baseline-dev-plain

Baseline: fixed 150-word windows (25 shared) ignoring structure, dense BGE-M3, cosine similarity, no rerank. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.289 |
| **Recall@5** | **0.775** [0.68, 0.87] |
| Recall@10 | 0.873 |
| Recall@20 | 0.908 |
| MRR@10 | 0.484 [0.40, 0.56] |
| nDCG@10 | 0.574 |
| ms / query | 171 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 0.779 | 0.497 |
| fr | 28 | 0.768 | 0.464 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.250 | 0.100 |
| definition | 1 | 0.000 | 0.000 |
| lookup | 39 | 0.756 | 0.528 |
| obligation | 29 | 0.862 | 0.468 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.650 | 0.504 |
| synthetic | 51 | 0.824 | 0.476 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q006 (en) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Rec130 |
| q054 (fr) | GDPR-Art30 | 2 | GDPR-Rec13, GDPR-Art30, GDPR-Rec97 |
| q060 (en) | GDPR-Art78 | 2 | GDPR-Art77, GDPR-Art78, GDPR-Rec141 |
| q065 (fr) | AIA-Art34 | 2 | AIA-Art29, AIA-Art34, AIA-Art27 |
| q070 (fr) | AIA-Art49 | 2 | AIA-Rec131, AIA-Art49, AIA-Art78 |
| q074 (en) | GDPR-Art30 | 2 | GDPR-Art29, GDPR-Art30, GDPR-Rec97 |
| q077 (en) | AIA-Art77 | 2 | AIA-Art76, AIA-Art77, AIA-Rec59 |
| q086 (fr) | AIA-Art34 | 2 | AIA-Art31, AIA-Art34, AIA-Art43 |
| q093 (en) | AIA-Art15 | 2 | AIA-Rec74, AIA-Art15, AIA-Rec142 |
| q096 (en) | GDPR-Art30 | 2 | GDPR-Rec81, GDPR-Art30, GDPR-Art29 |
| q098 (en) | GDPR-Art49 | 2 | GDPR-Art46, GDPR-Art49, GDPR-Rec107 |
| q011 (fr) | GDPR-Art14 | 3 | GDPR-Art13, GDPR-Art12, GDPR-Art14 |
| q013 (fr) | GDPR-Art36 | 3 | GDPR-Art35, GDPR-Rec94, GDPR-Art36 |
| q053 (en) | GDPR-Art14 | 3 | GDPR-Art13, GDPR-Rec61, GDPR-Art14 |
| q055 (fr) | AIA-Art83 | 3 | AIA-Art82, AIA-Art79, AIA-Art83 |
| q058 (en) | GDPR-Art49 | 3 | GDPR-Art47, GDPR-Art44, GDPR-Art49 |
| q059 (fr) | GDPR-Art80 | 3 | GDPR-Art57, GDPR-Art76, GDPR-Art80 |
| q071 (fr) | GDPR-Art66 | 3 | GDPR-Art65, GDPR-Rec136, GDPR-Art66 |
| q083 (en) | AIA-Art37 | 3 | AIA-Art36, AIA-Art31, AIA-Art37 |
| q087 (en) | GDPR-Art82 | 3 | GDPR-Rec146, GDPR-Art81, GDPR-Art82 |
| q088 (en) | AIA-Art38 | 3 | AIA-Art37, AIA-Art31, AIA-Art38 |
| q094 (en) | GDPR-Art22 | 3 | GDPR-Rec70, GDPR-Art21, GDPR-Art22 |
| q097 (en) | AIA-Art77 | 3 | AIA-Art76, AIA-Art78, AIA-Art77 |
| q099 (fr) | GDPR-Art78 | 3 | GDPR-Art77, GDPR-Rec143, GDPR-Art78 |
| q007 (en) | AIA-Art56 | 4 | AIA-Rec179, AIA-Rec116, AIA-Rec173 |
| q012 (en) | GDPR-Art22 | 4 | GDPR-Rec71, GDPR-Rec70, GDPR-Art21 |
| q067 (en) | GDPR-Art82 | 4 | GDPR-Rec145, GDPR-Rec146, GDPR-Art81 |
| q069 (en) | GDPR-Art23 | 4 | GDPR-Rec72, GDPR-Art22, GDPR-Rec19 |
| q073 (fr) | GDPR-Art22 | 4 | GDPR-Art21, AIA-Art2, AIA-Rec10 |
| q075 (fr) | AIA-Art83 | 4 | AIA-Art82, AIA-Art79, AIA-Rec155 |
| q078 (en) | GDPR-Art49 | 4 | GDPR-Rec107, GDPR-Art45, GDPR-Rec113 |
| q095 (en) | GDPR-Art14 | 4 | GDPR-Art13, GDPR-Rec59, GDPR-Rec61 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 5 | AIA-Rec131, AIA-Art71, AIA-AnnexVIII |
| q084 (fr) | AIA-Art36 | 5 | AIA-Art35, AIA-Art34, AIA-Art29 |
| q092 (fr) | GDPR-Art36 | 5 | GDPR-Art35, GDPR-Rec94, GDPR-Rec131 |
| q056 (en) | AIA-Art56 | 6 | AIA-Rec116, AIA-Art53, AIA-Art54 |
| q064 (en) | GDPR-Art86 | 6 | GDPR-Rec154, GDPR-Rec153, GDPR-Rec31 |
| q090 (en) | AIA-Art49 | 6 | AIA-Rec131, AIA-Art48, AIA-Rec53 |
| q010 (en) | GDPR-Art3 | 9 | GDPR-Rec23, GDPR-Rec24, AIA-Art74 |
| q014 (en) | GDPR-Art49 | 9 | GDPR-Art44, GDPR-Rec101, GDPR-Art46 |
| q081 (en) | GDPR-Art78 | 9 | GDPR-Rec135, GDPR-Art60, GDPR-Art66 |
| q061 (fr) | AIA-Art37 | 10 | AIA-Art34, AIA-Art30, AIA-Art29 |
| q066 (fr) | GDPR-Art67 | 12 | GDPR-Art66, GDPR-Art61, GDPR-Rec168 |
| q001 (en) | AIA-AnnexII | 15 | AIA-Art5, AIA-Rec42, AIA-Rec32 |
| q009 (en) | AIA-Art83 | 29 | AIA-Art23, AIA-Art48, AIA-Rec128 |
| q063 (fr) | GDPR-Art3 | 29 | GDPR-Rec115, GDPR-Rec23, GDPR-Rec79 |
| q002 (fr) | AIA-AnnexV | none | AIA-Art46, AIA-Art47, AIA-Art42 |
| q020 (fr) | GDPR-Art80, AIA-Art77 | none | AIA-Art76, AIA-Rec59, AIA-Rec70 |
| q068 (en) | AIA-Art38 | none | AIA-Art37, AIA-Art43, AIA-Art34 |
| q085 (fr) | GDPR-Art3 | none | GDPR-Rec22, GDPR-Rec20, GDPR-Rec17 |

## Answers: `plain`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 83 |
| in_scope | 71 |
| out_of_scope | 12 |
| refusal_rate | 0.0 |
| false_refusal_rate | 0.0 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | None |
| citation_precision_lenient | None |
| faithfulness | 0.991 |
| fully_supported | 0.9639 |
| faithfulness_ci95 | (0.9789, 1.0) |
| judged | 83 |
| judge_failed | 0 |
| uncited_sentences | 2.52 |
| input_tokens | 83696 |
| output_tokens | 8576 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness | Fully supported |
|---|---|---|---|---|---|
| hand | 22 | 0.0 | 0.0 | 0.9886 | 0.9545 |
| synthetic | 61 | 0.0 | 0.0 | 0.9918 | 0.9672 |

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

### q051 (en, lookup)

**Question:** What specific types of attacks must the technical solutions for high-risk AI systems address, where appropriate, to counter AI-specific vulnerabilities?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the technical solutions to address AI-specific vulnerabilities shall include, where appropriate, measures to prevent, detect, respond to, resolve, and control for the following types of attacks:
>
> * Attacks trying to manipulate the training data set (**data poisoning**)
> * Attacks trying to manipulate pre-trained components used in training (**model poisoning**)
> * Inputs designed to cause the AI model to make errors (referred to in the French text as *exemples contradictoires* / adversarial attacks)
> * Attacks leveraging trained models such as **membership inference**

Judge: 5/5. All listed attack types are explicitly mentioned in the provided sources.

### q052 (fr, obligation)

**Question:** Quelles mesures minimales le responsable du traitement doit-il mettre en œuvre pour protéger les intérêts d'une personne concernée par une décision individuelle automatisée fondée sur un contrat ou un consentement ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, lorsque la décision automatisée est fondée sur la conclusion ou l'exécution d'un contrat (point a) ou sur le consentement explicite de la personne concernée (point c), le responsable du traitement doit mettre en œuvre au moins **le droit de la personne concernée d'obtenir une intervention humaine de la part du responsable du traitement, d'exprimer son point de vue et de contester la décision**.

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 22 provisions.

### q053 (en, lookup)

**Question:** What specific information must a controller provide to a data subject when the personal data have not been obtained directly from them?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, when personal data have not been obtained from the data subject, the controller must provide the following information:
>
> (a) The identity and the contact details of the controller and, where applicable, of the controller's representative;
> (b) The contact details of the data protection officer, where applicable;
> (c) The purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
> (d) The categories of personal data concerned;
> (e) The recipients or categories of recipients of the personal data, if any;
> (f) Where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation and the existence or absence of an adequacy decision by the Commission.

Judge: 4/5. Answer lists most required items but omits the required information on automated decision‑making, which is in the source

### q054 (fr, obligation)

**Question:** Dans quels cas précis une entreprise de moins de 250 employés est-elle tout de même tenue de tenir un registre des activités de traitement ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, les obligations relatives à la tenue de registres s'appliquent à une entreprise ou une organisation comptant moins de 250 employés dans les cas précis où le traitement qu'elle effectue :
>
> 1. Est susceptible de comporter un risque pour les droits et les libertés des personnes concernées ;
> 2. N'est pas occasionnel ;
> 3. Porte notamment sur des catégories particulières de données (visées à l'article 9, paragraphe 1) ou sur des données à caractère personnel relatives à des condamnations pénales et à des infractions (visées à l'article 10).

Judge: 5/5. All three conditions listed are directly stated in the GDPR Article 30 provisions cited.

### q055 (fr, lookup)

**Question:** Dans quelles situations précises une autorité de surveillance du marché doit-elle inviter un fournisseur à mettre un terme à une non-conformité formelle?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni (Article 83), une autorité de surveillance du marché d'un État membre doit inviter le fournisseur concerné à mettre un terme à la non-conformité lorsqu'elle fait l'une des constatations suivantes (cas de non-conformité formelle) :
>
> a) Le marquage CE a été apposé en violation de l'article 48 ;
> b) Le marquage CE n'a pas été apposé ;
> c) La déclaration UE de conformité visée à l'article 47 n'a pas été établie ;
> d) La déclaration UE de conformité visée à l'article 47 n'a pas été établie correctement ;
> e) L'enregistrement dans la base de données de l'UE visée à l'article 71 n'a pas été effectué ;
> f) Le cas échéant, il n'a pas été désigné de mandataire ;
> g) La documentation technique n'est pas disponible.

Judge: 5/5. All listed situations match the lists provided in the sources.

### q056 (en, lookup)

**Question:** To what obligations may adherence to the codes of practice be limited for providers of general-purpose AI models that do not present systemic risks?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the text does not state that adherence to codes of practice is *limited* to specific obligations for providers of models that do not present systemic risks.
>
> Instead, the context mentions a different limitation regarding modifications or fine-tuning: "In the case of a modification or fine-tuning of a model, the obligations for providers of general-purpose AI models should be limited to that modification or fine-tuning..."
>
> Regarding codes of practice, the context states that providers may rely on them to demonstrate compliance with the general obligations set out under the Regulation (such as those in Article 53, and for models released under a free and open-source licence, provided they do not present systemic risks).

Judge: 5/5. All statements in the answer are directly supported by the provided sources.

### q057 (en, lookup)

**Question:** By what date must Member States identify and publish the list of public authorities or bodies that protect fundamental rights in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, Member States must identify and make the list of those public authorities or bodies publicly available by **2 November 2024**.

Judge: 5/5. The answer correctly states the deadline as 2 November 2024, which is directly supported by the sources.

### q058 (en, obligation)

**Question:** Under what specific conditions may a data transfer to a third country take place when no other provisions or derogations apply?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, when a transfer cannot be based on Article 45, Article 46 (including binding corporate rules), and none of the derogations for a specific situation are applicable, a transfer to a third country or an international organisation may take place only if **all** of the following conditions are met:
>
> 1. The transfer is not repetitive.
> 2. It concerns only a limited number of data subjects.
> 3. It is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject.
> 4. The controller has assessed all the circumstances surrounding the data transfer and, on the basis of that assessment, has provided suitable safeguards with regard to the protection of personal data.

Judge: 5/5. All conditions listed in the answer are directly supported by Article 49 of the GDPR source.

### q059 (fr, obligation)

**Question:** Est-ce qu'une organisation de protection des données peut introduire une réclamation auprès d'une autorité de contrôle sans avoir reçu de mandat de la personne concernée ?

**Answer** (gemini-3.5-flash-lite):

> Oui, selon le contexte, les États membres peuvent prévoir qu'un organisme, une organisation ou une association (constitué conformément à la législation d'un État membre et dont les objectifs statutaires relèvent de l'intérêt public dans le domaine de la protection des droits et libertés des personnes concernées) a le droit d'introduire, **indépendamment du mandat d'une personne concernée**, une réclamation auprès de l'autorité de contrôle compétente dans cet État membre.

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 80.

### q060 (en, lookup)

**Question:** Within what timeframe must a supervisory authority inform a data subject about the progress or outcome of their lodged complaint to avoid the data subject having a right to an effective judicial remedy?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the supervisory authority must inform the data subject on the progress or outcome of the complaint **within three months**. If it fails to do so (or does not handle the complaint), the data subject has the right to an effective judicial remedy.

Judge: 5/5. The answer's claim that the authority must inform within three months is directly stated in the cited GDPR articles.

### q061 (fr, obligation)

**Question:** Quelles informations l'autorité notifiante doit-elle fournir à la Commission concernant les organismes notifiés, et à quel moment ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, voici les informations que l'autorité notifiante doit fournir à la Commission et les moments correspondants :
>
> 1. **Informations sur chaque organisme d'évaluation de la conformité (procédure de notification) :**
>    * L'autorité notifiante informe la Commission à l'aide de l'outil de notification électronique.
>    * La notification comprend des informations complètes sur :
>      * Les activités d'évaluation de la conformité.
>      * Le ou les modules d'évaluation de la conformité.
>      * Les types de systèmes d'IA concernés.
>      * Le certificat d'accréditation (visé à l'article 29, paragraphe 2) ou les preuves documentaires (visées à l'article 29, paragraphe 3).
>    * **Moment :** La Commission statue (ou des délais s'appliquent) :
>      * Dans les **deux semaines** suivant la notification si celle-ci comprend le certificat d'accréditation.
>      * Dans les **deux mois** suivant la notification si celle-ci comprend les preuves documentaires.
>
> 2. **Informations en cas de modification de la désignation :**
>    * **Moment :** Immédiatement, l'autorité notifiante (ou l'organisme concerné par la modification) en informe la Commission et les autres États membres.
>
> 3. **Informations en cas d'enquête sur la compétence d'un organisme notifié :**
>    * L'autorité notifiante fournit à la Commission **sur demande** toutes les informations utiles relatives à la notification ou au maintien de la compétence de l'organisme notifié concerné.
>
> 4. **Informations en cas de restriction, suspension ou retrait d'une désignation :**
>    * Si l'autorité notifiante conclut que l'organisme ne répond plus aux exigences ou ne s'acquitte pas de ses obligations et qu'elle soumet la désignation à des restrictions, la suspend ou la retire :
>    * **Moment :** Elle en informe **immédiatement** la Commission et les autres États membres.

Judge: 5/5. All statements in the answer are directly supported by the cited provisions of the regulation.

### q062 (fr, obligation)

**Question:** Quelles sont les obligations de l'autorité notifiante en cas de restriction, de suspension ou de retrait d'une désignation d'organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, en cas de restriction, de suspension ou de retrait d'une désignation d'organisme notifié, l'autorité notifiante doit accomplir les actions suivantes :
>
> 1. **Informer immédiatement** la Commission et les autres États membres de la restriction, de la suspension ou du retrait de la désignation.
> 2. **Prendre les mesures nécessaires** pour que les dossiers de l'organisme notifié concerné soient conservés et mis à la disposition des autorités notifiantes d'autres États membres et des autorités de surveillance du marché, à leur demande.
> 3. **Évaluer l'incidence** sur les certificats délivrés par l'organisme notifié.
> 4. **Transmettre un rapport** sur ses conclusions à la Commission et aux autres États membres dans un délai de **trois mois** après avoir signalé les modifications apportées à la désignation.
> 5. **Exiger de l'organisme notifié** qu'il suspende ou retire, dans un délai raisonnable déterminé par elle, tous les certificats délivrés à tort afin d'assurer la conformité constante des systèmes d'IA à haut risque sur le marché.
> 6. *(Le cas échéant)* **Retirer la désignation** si l'organisme notifié décide de cesser ses activités et qu'elle a suffisamment de raisons de le faire.

Judge: 5/5. All listed obligations are directly stated in the provided AIA-Art36 (and related) source texts.

### q063 (fr, lookup)

**Question:** Dans quelle situation le règlement s'applique-t-il au traitement de données par un responsable du traitement non établi dans l'Union, mais dans un lieu régi par le droit d'un État membre en vertu du droit international public ?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention or explanation regarding the specific situation where the regulation applies to a controller "dans un lieu régi par le droit d'un État membre en vertu du droit international public".
>
> The context only specifies that the regulation applies when a controller or processor not established in the Union processes personal data of data subjects who are in the Union, and such activities are related to:
> 1. The offering of goods or services to such data subjects in the Union (whether a payment is required or not); or
> 2. The monitoring of their behavior, to the extent that their behavior takes place within the Union.

Judge: 5/5. All statements in the answer are consistent with the provided sources, and no unsupported citations are present.

### q064 (en, obligation)

**Question:** How can public authorities reconcile public access to official documents with the right to the protection of personal data?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, public authorities can reconcile public access to official documents with the right to the protection of personal data through provisions in Union or Member State law. Specifically:
>
> * The disclosure of personal data contained in documents held by a public authority or body should be provided for by Union or Member State law to which that authority or body is subject.
> * Such laws should reconcile public access to official documents and the reuse of public sector information with the right to the protection of personal data, and may therefore provide for the necessary reconciliation pursuant to the regulation.

Judge: 5/5. All statements in the answer are directly supported by the GDPR Recital 154 source.

### q065 (fr, obligation)

**Question:** Quels documents les organismes notifiés doivent-ils fournir à l'autorité notifiante pour faciliter ses activités de surveillance et d'évaluation ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, les organismes notifiés doivent mettre à la disposition de l'autorité notifiante et lui soumettre sur demande :
>
> * **Toute la documentation pertinente, y compris celle des fournisseurs**, afin de permettre à cette autorité de réaliser ses activités d'évaluation, de désignation, de notification et de surveillance et pour faciliter les évaluations.

Judge: 5/5. All claims are directly supported by source AIA-Art34.

### q066 (fr, lookup)

**Question:** Quel organe européen peut adopter des actes d'exécution pour définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle et le comité?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, il s'agit de **la Commission** (qui peut adopter des actes d'exécution afin de définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle, et entre ces autorités et le comité).

Judge: 5/5. The answer correctly identifies the Commission, which is explicitly stated in the sources as the body that can adopt implementing acts for electronic information exchange.

### q067 (en, obligation)

**Question:** Who is liable to pay compensation to a person who has suffered material or non-material damage due to an infringement of the regulation?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the **controller or processor** is liable to pay compensation to a person who has suffered material or non-material damage as a result of an infringement of the regulation.
>
> Specifically:
> * **Any person** who has suffered damage has the right to receive compensation from the controller or processor.
> * **Any controller** involved in processing is liable for the damage caused by processing which infringes the regulation.
> * **A processor** is liable for the damage caused by processing only where it has not complied with obligations of the regulation specifically directed to processors or where it has acted outside or contrary to lawful instructions of the controller.

Judge: 5/5. All statements in the answer are directly supported by the provided GDPR articles and recitals.

### q068 (en, lookup)

**Question:** How does the Commission ensure appropriate coordination and cooperation between notified bodies involved in conformity assessment procedures for high-risk AI systems?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the Commission ensures appropriate coordination and cooperation between notified bodies active in conformity assessment procedures for high-risk AI systems by putting them in place and properly operating them **in the form of a sectoral group of notified bodies**. Additionally, each notifying authority must ensure that the bodies it notifies participate in the work of this group, either directly or through designated representatives.

Judge: 5/5. All statements in the answer are directly supported by the source text.

### q069 (en, obligation)

**Question:** Under what conditions can Union or Member State law restrict data protection rights and obligations?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, Union or Member State law may restrict data protection rights and obligations under the following conditions:
>
> 1. **By way of a legislative measure** (to which the data controller or processor is subject).
> 2. The limitation must be **necessary and proportionated in a democratic society**.
> 3. It must respect **the essence of the fundamental rights and freedoms**.
> 4. It must be done to safeguard specific important objectives, such as:
>    * Public security (including the protection of human life, especially in response to natural or manmade disasters, and safeguarding against/preventing threats to public security).
>    * National security.
>    * National defense.
>    * The prevention, investigation, and prosecution of criminal offences, or the execution of criminal penalties.
>    * Breaches of ethics for regulated professions.
>    * Other important objectives of general public interest of the Union or of a Member State (in particular, an important economic or financial interest).

Judge: 5/5. All claims in the answer are directly supported by the provided GDPR recitals and articles.

### q070 (fr, lookup)

**Question:** Où sont enregistrés les systèmes d'IA à haut risque utilisés dans les domaines de la migration et de l'asile, et qui a accès à ces informations ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, les systèmes d'IA à haut risque dans le domaine de la migration et de l'asile doivent être enregistrés dans **une section non publique sécurisée de la base de données de l'UE**.
>
> **Qui a accès à ces informations :**
> * L'accès à cette section est **strictement réservé à la Commission**.
> * Il est également réservé **aux autorités de surveillance du marché** pour ce qui est de la section nationale de cette base de données les concernant.

Judge: 5/5. All statements in the answer are directly supported by the provided sources.

### q071 (fr, lookup)

**Question:** Quelle est la durée de validité maximale des mesures provisoires qu'une autorité de contrôle peut adopter d'urgence pour protéger les droits des personnes ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, la durée de validité maximale des mesures provisoires qu'une autorité de contrôle peut adopter d'urgence n'excède pas **trois mois** (ou a une durée déterminée qui ne devrait pas excéder trois mois).

Judge: 5/5. The answer's claim that the maximum validity is three months is directly stated in the provided GDPR sources.

### q072 (en, obligation)

**Question:** At what point and with whom must Member States consult regarding legislative or regulatory measures related to data processing?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, Member States must consult the supervisory authority during the preparation of:
> 1. A proposal for a legislative measure to be adopted by a national parliament, which relates to processing.
> 2. A regulatory measure based on such a legislative measure, which relates to processing.

Judge: 5/5. The answer accurately reflects the source stating that Member States must consult the supervisory authority during preparation of legislative or regulatory measures related to processing.

### q073 (fr, lookup)

**Question:** Dans quelles circonstances l'interdiction générale de prendre des décisions individuelles automatisées ne s'applique-t-elle pas selon le règlement ?

**Answer** (gemini-3.5-flash-lite):

> Selon le contexte fourni, l'interdiction générale (le paragraphe 1) relative aux décisions individuelles automatisées ne s'applique pas lorsque la décision :
>
> a) **Est nécessaire à la conclusion ou à l'exécution d'un contrat** entre la personne concernée et un responsable du traitement ;
> b) **Est autorisée par le droit de l'Union ou le droit de l'État membre** auquel le responsable du traitement est soumis, et qui prévoit également des mesures appropriées pour sauvegarder les droits, libertés et intérêts légitimes de la personne concernée ; ou
> c) **Est fondée sur le consentement explicite** de la personne concernée.

Judge: 5/5. All three listed exceptions match the text of GDPR Article 22 paragraph 2 provided in the sources.

### q074 (en, lookup)

**Question:** What specific information must be included in the record of processing activities maintained by a controller?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the record of processing activities maintained by a controller must contain all of the following information:
>
> (a) The name and contact details of the controller and, where applicable, the joint controller, the controller's representative, and the data protection officer;
> (b) The purposes of the processing;
> (c) A description of the categories of data subjects and of the categories of personal data;
> (d) The categories of recipients to whom the personal data have been or will be disclosed, including recipients in third countries.

Judge: 5/5. All listed items match the requirements in GDPR Article 30 as provided in the source.

### q075 (fr, obligation)

**Question:** Que doit faire l'autorité de surveillance du marché si une non-conformité formelle persiste malgré les mesures initiales ?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the text mentions that the market surveillance authority requires the relevant provider to put an end to the non-compliance within a prescribed period. If an operator of an AI system does not take adequate corrective measures within the specified time period, the market surveillance authority shall take all appropriate provisional measures to prohibit or restrict the making available of the AI system on its national market, to withdraw the product or the stand-alone AI system from that market, or to recall it.

Judge: 5/5. All statements in the answer are directly supported by the cited provisions in the sources.

### q076 (fr, lookup)

**Question:** Quel organisme facilite la révision des codes de bonne pratique et évalue les normes disponibles ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte fourni, c'est le **Bureau de l'IA** qui encourage et facilite le réexamen (la révision) des codes de bonne pratique et qui participe à l'évaluation des normes disponibles.

Judge: 5/5. The answer correctly identifies the Bureau de l'IA, which the sources state encourages and facilitates the revision of good practice codes and participates in evaluating available standards.

### q077 (en, obligation)

**Question:** What can a public authority protecting fundamental rights do if the available documentation is not enough to determine if a high-risk AI system infringes Union law?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, if the documentation is insufficient to ascertain whether an infringement of obligations under Union law protecting fundamental rights has occurred, the public authority or body may make a reasoned request to the market surveillance authority to organise testing of the high-risk AI system through technical means.

Judge: 5/5. The answer accurately reflects the provision in Article 77 about making a reasoned request for testing when documentation is insufficient.

### q078 (en, obligation)

**Question:** What action must Member States take regarding national provisions that set limits on personal data transfers to third countries for important reasons of public interest in the absence of an adequacy decision?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, Member States shall notify the Commission of such provisions.

Judge: 5/5. The answer correctly states that Member States must notify the Commission, as supported by GDPR-Art49.

### q079 (en, lookup)

**Question:** In which courts can a data subject bring judicial proceedings against a controller or processor?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, proceedings against a controller or processor shall be brought before the courts of the Member State where the controller or processor has an establishment.
>
> Alternatively, such proceedings may be brought before the courts of the Member State where the data subject has his or her habitual residence (or where the data subject resides), unless the controller or processor is a public authority of a Member State acting in the exercise of its public powers.

Judge: 5/5. All statements in the answer are directly supported by GDPR Art. 79 (and Recital 144).

### q080 (en, lookup)

**Question:** What kind of bodies or organisations can a data subject mandate to lodge a complaint or exercise data protection rights on their behalf?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, a data subject can mandate a not-for-profit body, organisation, or association that:
> * Has been properly constituted in accordance with the law of a Member State,
> * Has statutory objectives which are in the public interest, and
> * Is active in the field of the protection of data subjects' rights and freedoms with regard to the protection of their personal data (or active in the field of the protection of personal data).

Judge: 5/5. All three criteria listed are directly stated in the provided GDPR articles and recitals.

### q081 (en, obligation)

**Question:** What must a supervisory authority do when proceedings are brought against its decision that was preceded by an opinion or decision of the Board in the consistency mechanism?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of what a supervisory authority must do when proceedings are brought against its decision that was preceded by an opinion or decision of the Board in the consistency mechanism.

Judge: 5/5. The answer correctly states that the sources do not address the required action, which is accurate.

### q082 (en, lookup)

**Question:** What are the specific tasks of the scientific panel of independent experts regarding cross-border market surveillance activities and the Union safeguard procedure?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the specific tasks of the scientific panel of independent experts are:
>
> * To carry out **cross-border market surveillance activities** referred to in Article 74, paragraph 11 (without prejudice to the powers of market surveillance authorities); and
> * To **support the AI Office** in carrying out its duties within the context of the Union safeguard procedure pursuant to Article 81.

Judge: 5/5. All claims in the answer are directly supported by the cited source.

### q083 (en, lookup)

**Question:** Which institution is responsible for investigating cases where there are doubts regarding the competence of a notified body?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the **Commission** is responsible for investigating cases where there are reasons to doubt the competence of a notified body.

Judge: 5/5. The sources explicitly state that the Commission investigates doubts about notified bodies' competence.

### q084 (fr, lookup)

**Question:** Par quel moyen l'autorité notifiante doit-elle informer la Commission et les autres États membres des modifications apportées à la notification d'un organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte (Article 36), l'autorité notifiante doit informer la Commission et les autres États membres des modifications apportées à la notification d'un organisme notifié **au moyen de l'outil de notification électronique visé à l'article 30, paragraphe 2**.

Judge: 5/5. The answer accurately reflects the source text stating the notifying authority must use the electronic notification tool of Article 30(2).

### q085 (fr, lookup)

**Question:** Dans quelles conditions le règlement s'applique-t-il au traitement des données effectué par un établissement d'un responsable du traitement, indépendamment du lieu où se déroule le traitement ?

**Answer** (gemini-3.5-flash-lite):

> En se basant sur le contexte fourni, le règlement s'applique au traitement des données à caractère personnel lorsqu'il est effectué **dans le cadre des activités d'un établissement d'un responsable du traitement ou d'un sous-traitant sur le territoire de l'Union**, que le traitement lui-même ait lieu ou non dans l'Union.
>
> Pour que cet établissement existe, il est supposé correspondre à "l'exercice effectif et réel d'une activité au moyen d'un dispositif stable" (la forme juridique retenue, qu'il s'agisse d'une succursale ou d'une filiale, n'étant pas déterminante).

Judge: 5/5. All statements in the answer are directly supported by the provided GDPR source excerpts.

### q086 (fr, obligation)

**Question:** De quelle manière les organismes notifiés doivent-ils tenir compte de la taille des fournisseurs et de la complexité des systèmes d'IA dans leurs activités ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, les organismes notifiés doivent tenir compte de la taille des fournisseurs et de la complexité des systèmes d'IA de la manière suivante :
>
> * **Dans l'exercice de leurs activités :** Ils tiennent dûment compte de la taille du fournisseur, du secteur dans lequel il exerce ses activités, de sa structure et du degré de complexité du système d’IA à haut risque concerné, en particulier **en vue de réduire au minimum les charges administratives et les coûts de mise en conformité pour les microentreprises et les petites entreprises** au sens de la recommandation 2003/361/CE, tout en évitant les charges inutiles pour les fournisseurs.
> * **Dans leurs procédures :** Ils disposent de procédures pour accomplir leurs activités qui **tiennent dûment compte** de la taille des fournisseurs, du secteur dans lequel ils exercent, de leur structure et du degré de complexité du système d’IA concerné.

Judge: 5/5. All statements in the answer are directly supported by the provided source texts.

### q087 (en, lookup)

**Question:** What right does a controller or processor have after paying full compensation for damage caused by processing?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, a controller or processor which has paid full compensation for the damage suffered has the right to subsequently institute recourse proceedings (or claim back) from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage.

Judge: 5/5. All claims in the answer are directly supported by the cited GDPR provisions.

### q088 (en, obligation)

**Question:** How must notified bodies be involved in the sectoral group that the Commission sets up for them?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, each notifying authority must ensure that the bodies it has notified participate in the work of the sectoral group, either directly or through designated representatives.

Judge: 5/5. All claims are directly supported by the cited provisions

### q089 (fr, lookup)

**Question:** Quels éléments spécifiques les mesures législatives limitant la portée des obligations et des droits du RGPD doivent-elles contenir au minimum ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, toute mesure législative limitant la portée des obligations et des droits doit contenir au minimum des dispositions spécifiques concernant, le cas échéant :
>
> * a) Les finalités du traitement ou les catégories de traitement ;
> * b) Les catégories de données à caractère personnel ;
> * c) La portée des restrictions introduites ;
> * d) Les garanties.

Judge: 5/5. All listed required elements match the specific provisions stated in the GDPR source.

### q090 (en, obligation)

**Question:** Who is required to register a non-high-risk AI system in the EU database before it is placed on the market or put into service?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, before placing on the market or putting into service an AI system for which the provider has concluded that it is not high-risk (according to Article 6(3)), **the provider or, where applicable, the authorised representative** is required to register themselves and that system in the EU database.

Judge: 5/5. The answer's claim is directly supported by source [AIA-Art48].

### q091 (fr, lookup)

**Question:** Dans quel délai et à quelle majorité le comité doit-il adopter un avis ou une décision contraignante dans le cadre de la procédure d'urgence ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, dans le cadre de la procédure d'urgence (article 66), l'avis d'urgence ou la décision contraignante d'urgence est adopté dans un **délai de deux semaines** à la **majorité simple** des membres du comité.

Judge: 5/5. The answer's claim about a two‑week deadline and simple majority is directly stated in GDPR Art. 66.

### q092 (fr, obligation)

**Question:** Dans quelle situation précise le responsable du traitement est-il tenu de consulter l'autorité de contrôle avant de procéder au traitement ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte (Article 36 - Consultation préalable), le responsable du traitement est tenu de consulter l'autorité de contrôle préalablement au traitement lorsque **l'analyse d'impact relative à la protection des données (effectuée au titre de l'article 35) indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque.**

Judge: 5/5. The answer exactly matches the statement in GDPR-Art35 and is fully supported.

### q093 (en, obligation)

**Question:** How should the development of benchmarks and measurement methodologies for AI systems be encouraged, and who is involved in this process?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the development of benchmarks and measurement methodologies for AI systems should be encouraged by the Commission, as appropriate, in cooperation with relevant stakeholders and organizations, such as metrology and benchmarking authorities. In doing so, the Commission should also take note of and collaborate with international partners working on metrology and relevant measurement indicators relating to AI.

Judge: 5/5. All statements in the answer are directly supported by the cited source texts.

### q094 (en, lookup)

**Question:** What right does a data subject have regarding decisions based solely on automated processing, including profiling?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the data subject has the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.

Judge: 5/5. The answer accurately reflects the right described in the GDPR articles and recitals.

### q095 (en, lookup)

**Question:** What additional information must a controller provide to a data subject when personal data have not been obtained directly from them, in order to ensure fair and transparent processing?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, when personal data have not been obtained directly from the data subject (under Article 14), the controller must provide the following information:
>
> (a) The identity and the contact details of the controller and, where applicable, of the controller's representative;
> (b) The contact details of the data protection officer, where applicable;
> (c) The purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
> (d) The categories of personal data concerned;
> (e) The recipients or categories of recipients of the personal data, if any; and
> (f) Where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation, along with the existence or absence of an adequacy decision by the Commission.
>
> *(Note: The controller is also required to provide this information within specific timeframes, such as a reasonable period after obtaining the data—at the latest within one month—or, if the data are to be used for communication with the data subject, at the latest at the time of the first communication, or if disclosure to another recipient is envisaged, at the latest when the personal data are first disclosed.)*

Judge: 4/5. The answer correctly lists the required information (a‑f) as per Article 14, but the additional time‑frame details are not supported by the provided sources.

### q096 (en, obligation)

**Question:** Who must make the record of processing activities available to the supervisory authority upon request?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, **the controller or the processor** (and, where applicable, the controller's or the processor's representative) must make the record available to the supervisory authority on request.

Judge: 5/5. All claims in the answer are directly stated in the cited source GDPR-Art30.

### q097 (en, obligation)

**Question:** How must national public authorities handle information and documentation they obtain regarding fundamental rights protection in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, national public authorities and bodies handling information and documentation regarding fundamental rights protection must adhere to the following rules:
>
> * **Format and Language:** They have the power to request and access any documentation created or maintained under the Regulation in an *accessible language and format* when necessary to fulfill their mandates.
> * **Notification:** The relevant public authority or body must inform the market surveillance authority of the Member State concerned of any such request for documentation.
> * **Cybersecurity Measures:** They must put in place *adequate and effective cybersecurity measures* to protect the security and confidentiality of the information and data obtained.
> * **Data Retention and Deletion:** They must *delete the data collected as soon as it is no longer needed* for the purpose for which it was obtained, in accordance with applicable Union or national law.

Judge: 5/5. All claims in the answer are directly supported by the provided sources.

### q098 (en, lookup)

**Question:** What conditions allow for the transfer of personal data to a third country when there is neither an adequacy decision nor appropriate safeguards in place?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, in the absence of an adequacy decision and appropriate safeguards, a transfer (or a set of transfers) of personal data to a third country or an international organisation may take place only on one of the following conditions:
>
> (a) The data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards;
> (b) The transfer is necessary for the performance of a contract between the data subject and the controller or the implementation of pre-contractual measures taken at the data subject's request;
> (c) The transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person;
> (d) The transfer is necessary for important reasons of public interest.

Judge: 5/5. All listed conditions are directly taken from GDPR Article 49, which the sources provide.

### q099 (fr, obligation)

**Question:** Quels recours une personne physique ou morale possède-t-elle face à une décision juridiquement contraignante d'une autorité de contrôle qui la concerne ?

**Answer** (gemini-3.5-flash-lite):

> En se basant sur le contexte fourni, toute personne physique ou morale a le droit de **former un recours juridictionnel effectif** contre une décision juridiquement contraignante d'une autorité de contrôle qui la concerne.
>
> Ce recours s'exerce :
> * Devant la juridiction nationale compétente (ou devant les juridictions de l'État membre sur le territoire duquel l'autorité de contrôle est établie).
> * Sans préjudice de tout autre recours administratif ou extrajudiciaire.

Judge: 5/5. All claims in the answer are directly stated in the provided GDPR articles.

### q100 (en, lookup)

**Question:** What aspects regarding the scientific panel and its members must be included in the implementing act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the implementing act must include provisions on:
>
> * The conditions, procedures, and detailed arrangements for the scientific panel and its members to issue alerts and to request the assistance of the AI Office for the performance of their tasks.
> * The structure and level of fees, as well as the scale and structure of recoverable costs, for the advice and support provided by the experts to Member States.

Judge: 5/5. All statements in the answer are directly supported by the provided source excerpts.

### q101 (en, obligation)

**Question:** What actions can the Commission take if a Member State fails to implement corrective measures after being informed that a notified body no longer meets its requirements?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, if a Member State fails to take the necessary corrective measures after the Commission informs it that a notified body does not meet or no longer meets the requirements for its notification, the Commission may, by means of an implementing act, **suspend, restrict or withdraw the designation**.

Judge: 5/5. The answer's claim is directly supported by the cited provisions in the sources.

### q161 (en, not_covered)

**Question:** What specific interoperability requirements must gatekeepers implement for their core platform messaging services under the Digital Markets Act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of gatekeepers, core platform messaging services, or the Digital Markets Act. Therefore, the question cannot be answered using the provided text.

Judge: 5/5. The answer correctly states that the provided sources do not contain any information about gatekeepers, core platform messaging services, or the Digital Markets Act.

### q163 (en, not_covered)

**Question:** What are the specific global and European turnover thresholds that require a concentration to be notified to the European Commission under the EU Merger Regulation?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of the EU Merger Regulation, concentrations, or the specific global and European turnover thresholds required for notifying a concentration to the European Commission. The text discusses administrative fines (such as up to 20,000,000 EUR or up to 7% of total worldwide annual turnover, and up to 15,000,000 EUR or up to 3% of total worldwide annual turnover), but these relate to non-compliance with specific articles and provisions (such as data processing principles, supervisory orders, and obligations of operators or notified bodies), not merger notifications.

Judge: 5/5. The answer correctly states that the provided sources do not cover EU Merger Regulation thresholds and accurately reflects the content about administrative fines.

### q165 (en, not_covered)

**Question:** What are the mandatory vulnerability reporting timelines for manufacturers under the EU Cyber Resilience Act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of the mandatory vulnerability reporting timelines for manufacturers under the EU Cyber Resilience Act. The context mentions requirements regarding cybersecurity and the Cyber Resilience Act, but it does not contain information about specific reporting timelines.

Judge: 5/5. The answer correctly states that the provided sources do not contain mandatory vulnerability reporting timelines.

### q167 (fr, not_covered)

**Question:** Quelles sont les obligations de garantie légale de conformité pour un téléviseur intelligent vendu à un consommateur en France?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, il n'y a aucune information concernant les obligations de garantie légale de conformité pour un téléviseur intelligent vendu à un consommateur en France. Le contexte traite uniquement des systèmes d'intelligence artificielle (notamment les obligations des fournisseurs, importateurs et distributeurs, ainsi que la déclaration UE de conformité et le marquage CE).

Judge: 5/5. The answer correctly states that the provided sources contain no information on legal guarantee obligations for a smart TV, which is accurate.

### q169 (en, not_covered)

**Question:** What are the VAT registration thresholds for a business selling physical goods online to consumers in other EU member states?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of VAT registration thresholds for a business selling physical goods online to consumers in other EU member states. Therefore, the question cannot be answered using this context.

Judge: 5/5. The answer correctly states that the provided sources do not contain VAT registration thresholds, which is accurate.

### q171 (en, not_covered)

**Question:** What are the specific minimum capital requirements and prudential safeguards for licensing crypto-asset service providers under the Markets in Crypto-Assets (MiCA) regulation?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of the Markets in Crypto-Assets (MiCA) regulation, crypto-asset service providers, specific minimum capital requirements, or prudential safeguards. Therefore, the question cannot be answered using the provided text.

Judge: 5/5. The answer correctly states that the provided sources contain no information on MiCA, capital requirements, or prudential safeguards.

### q173 (en, not_covered)

**Question:** What are the exact technical protocols required by the revised Payment Services Directive (PSD2) for implementing multi-factor authentication in cross-border e-commerce transactions?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of the revised Payment Services Directive (PSD2), multi-factor authentication, or cross-border e-commerce transactions. Therefore, the context does not contain the answer to your question.

Judge: 5/5. The answer correctly states that the provided sources do not mention PSD2, multi-factor authentication, or cross‑border e‑commerce, which is fully supported by the sources.

### q174 (en, not_covered)

**Question:** What specific font size and contrast ratios are mandated for reflowable e-books under the European Accessibility Act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of specific font sizes or contrast ratios mandated for reflowable e-books under the European Accessibility Act.

Judge: 5/5. The answer correctly states that the provided sources do not specify font size or contrast ratios for reflowable e‑books.

### q176 (en, not_covered)

**Question:** What is the maximum surcharge a mobile network operator can apply for data roaming within the European Union under current telecom regulations?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of mobile network operators, data roaming, or roaming surcharges within the European Union. Therefore, the context does not contain the information needed to answer the question.

Judge: 5/5. The answer correctly states that the provided sources contain no information on mobile network operators or roaming surcharges.

### q178 (en, not_covered)

**Question:** What are the technical specifications for issuing a European Digital Identity Wallet under the eIDAS regulation, and how do member states handle cross-border recognition of these wallets?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no information regarding the technical specifications for issuing a European Digital Identity Wallet under the eIDAS regulation, nor how member states handle cross-border recognition of these wallets. Therefore, the context does not provide an answer to your question.

Judge: 5/5. The answer correctly notes that none of the provided sources contain information on the technical specifications or cross‑border recognition of a European Digital Identity Wallet.
