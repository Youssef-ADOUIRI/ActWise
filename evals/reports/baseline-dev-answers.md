# Retrieval report: baseline-dev-answers

Baseline: fixed 150-word windows (25 shared) ignoring structure, dense BGE-M3, cosine similarity, no rerank. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.375 |
| **Recall@5** | **0.650** [0.45, 0.85] |
| Recall@10 | 0.750 |
| Recall@20 | 0.825 |
| MRR@10 | 0.504 [0.32, 0.69] |
| nDCG@10 | 0.547 |
| ms / query | 144 |

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

## Answers

Plain prompt, top 5 passages, temperature 0. 22 answers by gemini-3.5-flash-lite (22); 21,837 input and 2,536 output tokens.

### q001 (en, lookup)

**Question:** Is trafficking in human beings one of the crimes for which the police may be allowed to use real-time facial recognition in public spaces to locate a suspect?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the use of "real-time" remote biometric identification systems in publicly accessible spaces for law enforcement is permitted if it is strictly necessary for the targeted search for specific victims of abduction, trafficking in human beings, or sexual exploitation, as well as the search for missing persons (objective i under point (h)).
>
> Additionally, for the purpose of locating or identifying a person suspected of having committed a criminal offence (objective iii), the exemption applies to offences referred to in Annex II that are punishable by a custodial sentence or a detention order for a maximum period of at least four years. Therefore, trafficking in human beings is explicitly mentioned as a valid objective (as a targeted search for victims) under the exceptions allowing this technology.

### q002 (fr, lookup)

**Question:** Quelles mentions doit contenir la déclaration UE de conformité d'un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, la déclaration UE de conformité d'un système d'IA à haut risque doit contenir les éléments suivants :
>
> * Les informations qui figurent à l'annexe V.
> * Toutes les informations nécessaires à l'identification de la législation d'harmonisation de l'Union à laquelle la déclaration se rapporte (lorsque le système est soumis à plusieurs actes législatifs d'harmonisation de l'Union).

### q003 (en, obligation)

**Question:** How must a high-risk AI system that keeps learning after deployment be built so that its own biased outputs do not feed back into future decisions?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, high-risk AI systems that continue to learn after being placed on the market or put into service must be developed in such a way as to:
>
> 1. **Eliminate or reduce as far as possible** the risk of possibly biased outputs influencing input for future operations (feedback loops).
> 2. Ensure that any such feedback loops are **duly addressed with appropriate mitigation measures**.

### q004 (en, lookup)

**Question:** If a notified body stops its conformity assessment activities, how long can the certificates it issued remain valid?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the certificates of the notified body may remain valid for a period of **nine months** after the cessation of the notified body's activities, provided that another notified body has confirmed in writing that it will assume responsibilities for the high-risk AI systems covered by those certificates.

### q005 (fr, lookup)

**Question:** Qui peut enquêter lorsqu'on doute qu'un organisme notifié soit encore compétent ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte (Article 37), **la Commission** enquête, s'il y a lieu, sur tous les cas où il existe des raisons de douter de la compétence d'un organisme notifié ou du respect continu de ses exigences et responsabilités.
>
> De plus, **l'autorité notifiante** procède également sans retard à une enquête avec la plus grande diligence lorsqu'elle a des raisons suffisantes de considérer qu'un organisme notifié ne répond plus aux exigences ou ne s'acquitte pas de ses obligations.

### q006 (en, obligation)

**Question:** Does a public authority that starts using a high-risk AI system to decide who receives social benefits have to register that use in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, yes. Deployers of high-risk AI systems that are public authorities, agencies, bodies, or Union institutions, offices, and agencies must register themselves, select the system, and register its use in the EU database before using/putting into service a high-risk AI system listed in the relevant annex (with specific exceptions, such as certain points in Annex III like law enforcement, migration, asylum, and border control management, which go into a secure non-public section, or critical infrastructure systems which are registered at the national level).

### q007 (en, lookup)

**Question:** Who facilitates the drawing up of codes of practice for general-purpose AI models, and by when were they supposed to be ready?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context:
>
> * **Who facilitates/draws up the codes of practice:** The **AI Office** may invite providers of general-purpose AI models, as well as relevant national competent authorities, to participate in the drawing-up of codes of practice. They should also collaborate with relevant national competent authorities, and could consult with civil society organisations, other relevant stakeholders, and experts (including the Scientific Panel). Additionally, civil society organisations, industry, academia, downstream providers, and independent experts may support the process.
> * **By when they should be ready:** Codes of practice should be ready by **2 May 2025**.

### q008 (fr, lookup)

**Question:** Quelles conditions doivent remplir les experts du groupe scientifique qui conseille le Bureau de l'IA ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, les experts du groupe scientifique doivent remplir les conditions suivantes :
>
> 1. **Disposer d'une expertise et d'une compétence particulières ainsi que d'une expertise scientifique ou technique** à la pointe des connaissances dans le domaine de l'IA.
> 2. **Être indépendants** vis-à-vis de tout fournisseur de systèmes d'IA ou de modèles d'IA à usage général.
> 3. **Être capables de mener des activités avec diligence, précision et objectivité** (ou s'acquitter de leurs tâches avec impartialité et objectivité).
> 4. **Veiller à la confidentialité** des informations et des données obtenues dans l'exercice de leurs tâches et activités.

### q009 (en, definition)

**Question:** Which situations count as formal non-compliance of a high-risk AI system, such as a missing CE marking?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the situations that indicate a high-risk AI system is not in conformity (or presents issues regarding its requirements and documentation) include:
>
> * **Missing or incorrect CE marking:** The system does not bear the required CE marking.
> * **Missing conformity documentation:** The system is not accompanied by a copy of the EU declaration of conformity (referred to in Article 47) or instructions for use.
> * **Obligations not met:** The provider, importer, or authorised representative has not complied with their respective obligations (such as drawing up technical documentation under Article 11 and Annex IV, or carrying out the relevant conformity assessment procedure under Article 43).
> * **Falsification:** The system is falsified or is accompanied by falsified documentation.
> * **General non-conformity:** The system is considered, or there is sufficient reason to consider, not to be in conformity with the requirements set out in Section 2 or with the Regulation as a whole.

### q010 (en, lookup)

**Question:** Does the GDPR apply to a company based outside the EU that tracks the online behaviour of people in the EU?

**Answer** (gemini-3.5-flash-lite):

> Yes. According to the context, the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union should be subject to this Regulation when it is related to the monitoring of their behavior, provided that the behavior takes place within the Union. This includes tracking natural persons on the internet, such as through techniques like profiling to analyze or predict preferences, behaviors, or attitudes.

### q011 (fr, obligation)

**Question:** Lorsque des données personnelles n'ont pas été collectées auprès de la personne concernée, dans quel délai le responsable du traitement doit-il l'informer ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, lorsque les données à caractère personnel n'ont pas été collectées auprès de la personne concernée, le responsable du traitement doit fournir les informations :
>
> * Dans un délai raisonnable après l'obtention des données à caractère personnel, mais **au plus tard dans un délai d'un mois**, compte tenu des circonstances particulières de leur traitement.
> * Ou, si les données doivent être utilisées pour la communication avec la personne concernée, au plus tard au moment de la première communication.
> * Ou, si une communication à un autre destinataire est envisagée, au plus tard lors de la première divulgation des données.

### q012 (en, lookup)

**Question:** Can a bank reject my loan application based only on an automated decision, with no human involved?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, the general rule is that **you have the right not to be subject to a decision based solely on automated processing** (without human intervention) that produces legal effects or significantly affects you, and the text specifically gives the example of the "automatic refusal of an online credit application."
>
> However, this rule does not apply if the decision:
> 1. Is necessary for entering into, or the performance of, a contract between you and a data controller (such as a bank);
> 2. Is authorized by Union or Member State law to which the controller is subject and which lays down suitable measures to safeguard your rights, freedoms, and legitimate interests; or
> 3. Is based on your explicit consent.
>
> In cases where the decision is necessary for a contract or based on your explicit consent, the data controller is required to implement suitable measures to safeguard your rights, freedoms, and legitimate interests.

### q013 (fr, obligation)

**Question:** Dans quel cas le responsable du traitement doit-il consulter l'autorité de contrôle avant de commencer un traitement ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, le responsable du traitement doit consulter l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données (effectuée au titre de l'article 35) indique que **le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque**.

### q014 (en, lookup)

**Question:** Can personal data be sent to a country without an adequacy decision if the person explicitly agrees to the transfer?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of whether personal data can be sent to a country without an adequacy decision based on the explicit agreement or consent of the person. Therefore, the context does not contain the information needed to answer this question.

### q015 (en, lookup)

**Question:** In an emergency, can a national data protection authority act on its own without going through the cooperation procedure with other authorities, and for how long?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, yes, a supervisory authority may immediately adopt provisional measures intended to produce legal effects on its own territory by way of derogation from the consistency mechanism or the cooperation procedure.
>
> These provisional measures have a specified period of validity which **shall not exceed three months**.

### q016 (en, lookup)

**Question:** What can I do if the data protection authority does not deal with my complaint?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, if a supervisory authority (data protection authority) does not handle your complaint, or does not inform you within three months on the progress or outcome of the complaint, you have the right to an **effective judicial remedy** against the supervisory authority (pursuant to Article 78).
>
> Proceedings against the supervisory authority must be brought before the courts of the Member State where the supervisory authority is established.

### q017 (fr, lookup)

**Question:** Devant quels tribunaux puis-je agir contre une entreprise qui a violé mes droits au titre du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> D'après le contexte, une action contre un responsable du traitement ou un sous-traitant (par exemple, une entreprise) doit être intentée :
>
> 1. Devant les juridictions de l'**État membre dans lequel le responsable du traitement ou le sous-traitant dispose d'un établissement**.
> 2. **Alternativement**, une telle action peut être intentée devant les juridictions de l'**État membre dans lequel la personne concernée a sa résidence habituelle** (sauf si le responsable du traitement ou le sous-traitant est une autorité publique d'un État membre agissant dans l'exercice de ses prérogatives de puissance publique).

### q018 (en, obligation)

**Question:** If a processor ignores the controller's instructions and this causes damage to someone, does the processor have to pay compensation?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, yes. A processor is liable for the damage caused by processing where it has "acted outside or contrary to lawful instructions of the controller," and a controller or processor must compensate any damage a person may suffer as a result of processing that infringes the Regulation (unless they prove they are not in any way responsible for the event giving rise to the damage).

### q019 (en, cross_law)

**Question:** We provide an AI tool that screens job applicants. What must our GDPR record of processing activities contain, and does the AI Act also require us to register the tool in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of what a "GDPR record of processing activities" must contain.
>
> However, regarding the EU database registration:
> * If you are a **public authority, agency, or body**, you must register yourself in the EU database and select the system you envisage to use *before* using a high-risk AI system listed in an annex to the Regulation.
> * If you are an **other type of deployer**, you are entitled to register voluntarily.
> * Any **substantial modification** of high-risk AI systems must also be registered in the EU database.
> * *(Note: If your AI system is in the area of critical infrastructure, it should only be registered at the national level according to the text).*

### q020 (fr, cross_law)

**Question:** Une association de défense des droits peut-elle agir au nom de personnes discriminées par un système d'IA, et quelles autorités peuvent exiger la documentation de ce système ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni :
>
> 1. **Concernant l'action d'une association de défense des droits au nom de personnes discriminées :** Le texte fourni ne contient aucune information permettant de dire si une association de défense des droits peut ou non agir au nom de personnes discriminées par un système d'IA.
>
> 2. **Concernant les autorités qui peuvent exiger la documentation de ce système :**
>    - Les **autorités ou organismes publics nationaux** qui supervisent ou font respecter les obligations au titre du droit de l’Union visant à protéger les droits fondamentaux (y compris le droit à la non-discrimination) en ce qui concerne l'utilisation des systèmes d'IA à haut risque visés à l'annexe III.
>    - Les **autorités ou organismes publics nationaux compétents** qui contrôlent l’application du droit de l’Union en matière de protection des droits fondamentaux (notamment les organismes chargés des questions d’égalité et les autorités de protection des données), lorsque leur mandat l’exige.

### q021 (en, not_covered)

**Question:** What fines can the European Commission impose on gatekeepers that breach the Digital Markets Act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided context, there is no mention of "gatekeepers" or the "Digital Markets Act." The context does, however, state that the European Commission may impose fines on providers of general-purpose AI models not exceeding 3% of their annual total worldwide turnover in the preceding financial year or EUR 15 000 000 (whichever is higher) for certain infringements or failures to comply.

### q022 (fr, not_covered)

**Question:** Quelles obligations le règlement sur les données (Data Act) impose-t-il aux fabricants d'objets connectés ?

**Answer** (gemini-3.5-flash-lite):

> Sur la base du contexte fourni, il n'y a aucune information concernant les "fabricants d'objets connectés" ou les obligations spécifiques que le règlement sur les données (*Data Act*) leur impose. Le texte traite principalement des modèles d'IA à usage général, des PME, du Contrôleur européen de la protection des données, des amendes et du traitement des données personnelles, mais ne mentionne pas les objets connectés.
