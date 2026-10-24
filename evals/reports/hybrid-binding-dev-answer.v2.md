# Retrieval report: hybrid-binding-dev-answer.v2

E: as C, with articles and annexes ranked before recitals. Split `dev`, 71 scored questions (12 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.817 |
| **Recall@5** | **0.979** [0.94, 1.00] |
| Recall@10 | 1.000 |
| Recall@20 | 1.000 |
| MRR@10 | 0.904 [0.85, 0.95] |
| nDCG@10 | 0.925 |
| ms / query | 159 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 43 | 1.000 | 0.907 |
| fr | 28 | 0.946 | 0.900 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.750 | 0.750 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 39 | 0.974 | 0.877 |
| obligation | 29 | 1.000 | 0.966 |

## By source (hand-written or synthetic)

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| hand | 20 | 0.925 | 0.806 |
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
| q070 (fr) | AIA-Art49 | 3 | AIA-AnnexIII, AIA-AnnexVIII, AIA-Art49 |
| q073 (fr) | GDPR-Art22 | 4 | AIA-Art86, AIA-Art2, AIA-Art5 |
| q002 (fr) | AIA-AnnexV | 9 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |

## Answers: `answer.v2`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 83 |
| in_scope | 71 |
| out_of_scope | 12 |
| refusal_rate | 1.0 |
| false_refusal_rate | 0.0282 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.8989 |
| citation_precision_lenient | 0.9438 |
| faithfulness | 0.971 |
| faithfulness_ci95 | (0.9348, 0.9964) |
| judged | 69 |
| judge_failed | 0 |
| uncited_sentences | 0.51 |
| input_tokens | 77592 |
| output_tokens | 8766 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness |
|---|---|---|---|---|
| hand | 22 | 1.0 | 0.0 | 0.9875 |
| synthetic | 61 | 1.0 | 0.0392 | 0.9643 |

### q001 (en, lookup)

**Question:** Is trafficking in human beings one of the crimes for which the police may be allowed to use real-time facial recognition in public spaces to locate a suspect?

**Answer** (gemini-3.5-flash-lite):

> Yes, trafficking in human beings is listed as one of the criminal offences referred to in Article 5(1), first subparagraph, point (h)(iii), for which the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for law enforcement may be permitted, provided that such use is strictly necessary for that objective and complies with all required conditions and safeguards [AIA-Art5-1, AIA-AnnexII, AIA-Art5-2]. The provided sources do not cover whether trafficking in human beings is specifically included under point (h)(i) (targeted search for victims of trafficking), as they only mention it in the context of criminal offences under point (h)(iii).

Judge: 4/5. Main claim is supported, but the statement that sources do not cover point (h)(i) is inaccurate.

### q002 (fr, lookup)

**Question:** Quelles mentions doit contenir la déclaration UE de conformité d'un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> La déclaration UE de conformité doit contenir toutes les informations nécessaires à l'identification de la législation d'harmonisation de l'Union à laquelle elle se rapporte [AIA-Art47-3]. Elle doit également contenir les informations qui figurent à l'annexe V [AIA-Art47-2].
>
> Les sources ne précisent pas la liste détaillée de ces informations figurant à l'annexe V.

Judge: 5/5. All statements in the answer are directly supported by the cited sources.

### q003 (en, obligation)

**Question:** How must a high-risk AI system that keeps learning after deployment be built so that its own biased outputs do not feed back into future decisions?

**Answer** (gemini-3.5-flash-lite):

> High-risk AI systems that continue to learn after being placed on the market or put into service must be developed in such a way as to eliminate or reduce as far as possible the risk of possibly biased outputs influencing input for future operations (feedback loops), and to ensure that any such feedback loops are duly addressed with appropriate mitigation measures [AIA-Art15-4].

Judge: 5/5. All statements are directly supported by the cited source.

### q004 (en, lookup)

**Question:** If a notified body stops its conformity assessment activities, how long can the certificates it issued remain valid?

**Answer** (gemini-3.5-flash-lite):

> If a notified body decides to cease its conformity assessment activities, its certificates may remain valid for a period of nine months after the cessation of its activities, provided that another notified body has confirmed in writing that it will assume responsibilities for the high-risk AI systems covered by those certificates [AIA-Art36-3].

Judge: 5/5. All statements in the answer are directly supported by the cited source.

### q005 (fr, lookup)

**Question:** Qui peut enquêter lorsqu'on doute qu'un organisme notifié soit encore compétent ?

**Answer** (gemini-3.5-flash-lite):

> La Commission enquête, s’il y a lieu, sur tous les cas où il existe des raisons de douter de la compétence d’un organisme notifié ou du respect continu, par un organisme notifié, des exigences établies à l’article 31 et de ses responsabilités applicables [AIA-Art37-1]. Les sources ne couvrent pas l'éventualité où d'autres entités que la Commission mèneraient ce type d'enquête spécifique.

Judge: 5/5. All statements are directly supported by the cited source and the interpretation about lack of coverage is consistent with the sources.

### q006 (en, obligation)

**Question:** Does a public authority that starts using a high-risk AI system to decide who receives social benefits have to register that use in an EU database?

**Answer** (gemini-3.5-flash-lite):

> Before putting into service or using a high-risk AI system listed in Annex III—with the exception of those listed in point 2 of Annex III—deployers that are public authorities must register themselves, select the system, and register its use in the EU database referred to in Article 71 [AIA-Art26-8, AIA-Art49-3]. However, the provided sources do not cover whether decision-making regarding the recipients of social benefits falls under point 2 of Annex III or another specific provision that might alter this registration obligation.

Judge: 5/5. All statements are directly supported by the cited articles, and the note about lack of coverage is accurate.

### q007 (en, lookup)

**Question:** Who facilitates the drawing up of codes of practice for general-purpose AI models, and by when were they supposed to be ready?

**Answer** (gemini-3.5-flash-lite):

> The AI Office may invite all providers of general-purpose AI models, as well as relevant national competent authorities, to participate in the drawing-up of codes of practice [AIA-Art56-3].
> The provided sources do not cover by when the codes of practice were supposed to be ready.

Judge: 5/5. All statements are supported by the cited source and no deadline is mentioned in the sources.

### q008 (fr, lookup)

**Question:** Quelles conditions doivent remplir les experts du groupe scientifique qui conseille le Bureau de l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Les experts du groupe scientifique doivent être sélectionnés par la Commission en fonction de leur expertise à la pointe des connaissances scientifiques ou techniques dans le domaine de l'IA, nécessaire pour s'acquitter des tâches prévues [AIA-Art68-2]. De plus, ils doivent être en mesure de démontrer qu'ils remplissent les conditions suivantes :
> a) disposer d'une expertise et d'une compétence particulières ainsi que d'une expertise scientifique ou technique dans le domaine de l'IA [AIA-Art68-2];
> b) être indépendants vis-à-vis de tout fournisseur de systèmes d'IA ou de modèles d'IA à usage général [AIA-Art68-2];
> c) être capables de mener des activités avec diligence, précision et objectivité [AIA-Art68-2].
>
> Les sources ne couvrent pas la rémunération ou d'autres conditions administratives non mentionnées dans les articles fournis.

Judge: 5/5. All claims are directly supported by the cited article AIA-Art68-2.

### q009 (en, definition)

**Question:** Which situations count as formal non-compliance of a high-risk AI system, such as a missing CE marking?

**Answer** (gemini-3.5-flash-lite):

> According to the provided sources, the following findings by the market surveillance authority of a Member State count as formal non-compliance:
> - the CE marking has been affixed in violation of Article 48 [AIA-Art83-1];
> - the CE marking has not been affixed [AIA-Art83-1];
> - the EU declaration of conformity referred to in Article 47 has not been drawn up [AIA-Art83-1];
> - the EU declaration of conformity referred to in Article 47 has not been drawn up correctly [AIA-Art83-1];
> - the registration in the EU database referred to in Article 71 has not been carried out [AIA-Art83-1];
> - where applicable, no authorised representative has been appointed [AIA-Art83-1];
> - technical documentation is not available [AIA-Art83-1].

Judge: 5/5. All listed situations are directly stated in Article 83(1) of the AI Act.

### q010 (en, lookup)

**Question:** Does the GDPR apply to a company based outside the EU that tracks the online behaviour of people in the EU?

**Answer** (gemini-3.5-flash-lite):

> Yes, the GDPR applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to the monitoring of their behaviour as far as their behaviour takes place within the Union [GDPR-Art3-2].

Judge: 5/5. The answer's claim is fully supported by GDPR Article 3(2).

### q011 (fr, obligation)

**Question:** Lorsque des données personnelles n'ont pas été collectées auprès de la personne concernée, dans quel délai le responsable du traitement doit-il l'informer ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement fournit les informations dans un délai raisonnable après avoir obtenu les données à caractère personnel, mais ne dépassant pas un mois, eu égard aux circonstances particulières dans lesquelles les données sont traitées [GDPR-Art14-3].
>
> Cependant, des délais spécifiques s'appliquent si les données doivent être utilisées aux fins de la communication avec la personne concernée (au plus tard au moment de la première communication) ou s'il est envisagé de communiquer les informations à un autre destinataire (au plus tard lorsque les données sont communiquées pour la première fois) [GDPR-Art14-3]. Les sources ne couvrent pas les autres exceptions ou conditions particulières dans lesquelles ces délais ne s'appliquent pas, hormis les exceptions générales de non-application de l'article 14 [GDPR-Art14-5].
>
> Vous donnez des informations juridiques et non des conseils juridiques.

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR articles.

### q012 (en, lookup)

**Question:** Can a bank reject my loan application based only on an automated decision, with no human involved?

**Answer** (gemini-3.5-flash-lite):

> The data subject has the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning them or similarly significantly affects them [GDPR-Art22-1]. However, this right does not apply if the decision is necessary for entering into, or performance of, a contract between the data subject and a data controller, is authorised by Union or Member State law with suitable safeguard measures, or is based on the data subject's explicit consent [GDPR-Art22-2].
>
> The provided sources do not cover whether the specific scenario of a bank rejecting a loan application falls under these exceptions or how financial institutions apply these rules.

Judge: 5/5. All statements are directly supported by the cited GDPR articles, and the comment about sources not covering the specific scenario is accurate.

### q013 (fr, obligation)

**Question:** Dans quel cas le responsable du traitement doit-il consulter l'autorité de contrôle avant de commencer un traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement consulte l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données effectuée au titre de l'article 35 indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque [GDPR-Art36-1]. De plus, nonobstant ce cas, le droit des États membres peut exiger que les responsables du traitement consultent l'autorité de contrôle et obtiennent son autorisation préalable en ce qui concerne le traitement effectué par un responsable du traitement dans le cadre d'une mission d'intérêt public exercée par celui-ci, y compris le traitement dans le cadre de la protection sociale et de la santé publique [GDPR-Art36-5].

Judge: 5/5. All statements are directly supported by the cited GDPR articles.

### q014 (en, lookup)

**Question:** Can personal data be sent to a country without an adequacy decision if the person explicitly agrees to the transfer?

**Answer** (gemini-3.5-flash-lite):

> Yes, a transfer of personal data to a third country or international organisation in the absence of an adequacy decision or appropriate safeguards may take place if the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards [GDPR-Art49-1].

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 49(1).

### q015 (en, lookup)

**Question:** In an emergency, can a national data protection authority act on its own without going through the cooperation procedure with other authorities, and for how long?

**Answer** (gemini-3.5-flash-lite):

> In exceptional circumstances where a supervisory authority concerned considers that there is an urgent need to act to protect the rights and freedoms of data subjects, it may immediately adopt provisional measures intended to produce legal effects on its own territory by way of derogation from the consistency mechanism or the cooperation procedure [GDPR-Art66-1]. The specified period of validity for these measures shall not exceed three months [GDPR-Art66-1].

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 66(1).

### q016 (en, lookup)

**Question:** What can I do if the data protection authority does not deal with my complaint?

**Answer** (gemini-3.5-flash-lite):

> Without prejudice to any other administrative or non-judicial remedy, you have the right to an effective judicial remedy if the competent supervisory authority does not handle your complaint or does not inform you within three months on the progress or outcome of the complaint lodged pursuant to Article 77 [GDPR-Art78-2].
>
> The sources provided do not cover what other specific steps or actions you can take outside of seeking this effective judicial remedy.

Judge: 5/5. All statements are directly supported by the cited GDPR article and the summary about source coverage is accurate.

### q017 (fr, lookup)

**Question:** Devant quels tribunaux puis-je agir contre une entreprise qui a violé mes droits au titre du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Toute action contre un responsable du traitement ou un sous-traitant est intentée devant les juridictions de l'État membre dans lequel le responsable du traitement ou le sous-traitant dispose d'un établissement [GDPR-Art79-2]. Une telle action peut aussi être intentée devant les juridictions de l'État membre dans lequel la personne concernée a sa résidence habituelle, sauf si le responsable du traitement ou le sous-traitant est une autorité publique d'un État membre agissant dans l'exercice de ses prérogatives de puissance publique [GDPR-Art79-2].
>
> Les sources fournies ne traitent pas des actions intentées contre des entreprises qui ne seraient ni un responsable du traitement ni un sous-traitant.

Judge: 5/5. All statements are directly supported by GDPR Article 79(2) and the meta‑statement about the sources is accurate.

### q018 (en, obligation)

**Question:** If a processor ignores the controller's instructions and this causes damage to someone, does the processor have to pay compensation?

**Answer** (gemini-3.5-flash-lite):

> Any controller involved in processing shall be liable for the damage caused by processing which infringes the GDPR [GDPR-Art82-2]. A processor shall be liable for the damage caused by processing where it has acted outside or contrary to lawful instructions of the controller [GDPR-Art82-2]. Any person who has suffered material or non-material damage as a result of an infringement of the regulation has the right to receive compensation from the controller or processor for the damage suffered [GDPR-Art82-1].

Judge: 5/5. All statements are directly supported by the cited GDPR articles.

### q019 (en, cross_law)

**Question:** We provide an AI tool that screens job applicants. What must our GDPR record of processing activities contain, and does the AI Act also require us to register the tool in an EU database?

**Answer** (gemini-3.5-flash-lite):

> The sources do not contain any information regarding what a GDPR record of processing activities must contain.
>
> Regarding your obligation to register the tool in an EU database under the AI Act, the sources state the following:
> Before placing on the market or putting into service a high-risk AI system listed in Annex III (with the exception of high-risk AI systems listed in point 2 of Annex III), the provider or, where applicable, the authorised representative must register themselves and their system in the EU database referred to in Article 71 [AIA-Art49-1]. Alternatively, if the provider has concluded that the AI system is not high-risk according to Article 6(3), that provider or authorised representative must register themselves and that system in the EU database before placing it on the market or putting it into service [AIA-Art49-2].
>
> (Note: You are given legal information, not legal advice.)

Judge: 5/5. All statements are directly supported by the cited sources.

### q020 (fr, cross_law)

**Question:** Une association de défense des droits peut-elle agir au nom de personnes discriminées par un système d'IA, et quelles autorités peuvent exiger la documentation de ce système ?

**Answer** (gemini-3.5-flash-lite):

> Les autorités ou organismes publics nationaux qui supervisent ou font respecter les obligations au titre du droit de l'Union visant à protéger les droits fondamentaux (y compris le droit à la non-discrimination) en ce qui concerne l'utilisation des systèmes d'IA à haut risque visés à l'annexe III sont habilités à demander toute documentation créée ou conservée en vertu du règlement et à y avoir accès, lorsque cela est nécessaire à l'accomplissement effectif de leur mandat [AIA-Art77-1]. Les sources fournies ne traitent pas de la question de savoir si une association de défense des droits peut agir au nom de personnes discriminées par un système d'IA.

Judge: 5/5. All statements are directly supported by the cited source and correctly note the lack of coverage on associations.

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
>
> * Attacks trying to manipulate the training data set (data poisoning) or pre-trained components used in training (model poisoning) [AIA-Art15-5].
> * Inputs designed to cause the AI model to make a mistake (adversarial examples or model evasion) [AIA-Art15-5].
> * Confidentiality attacks [AIA-Art15-5].
> * Model flaws [AIA-Art15-5].
>
> *(Note: You give legal information, not legal advice. Never say whether a specific company or system is compliant.)*

Judge: 5/5. All listed attack types are explicitly mentioned in AI Act Article 15(5) and correctly cited.

### q052 (fr, obligation)

**Question:** Quelles mesures minimales le responsable du traitement doit-il mettre en œuvre pour protéger les intérêts d'une personne concernée par une décision individuelle automatisée fondée sur un contrat ou un consentement ?

**Answer** (gemini-3.5-flash-lite):

> Dans les cas où une décision individuelle automatisée est nécessaire à la conclusion ou à l'exécution d'un contrat, ou qu'elle est fondée sur le consentement explicite de la personne concernée, le responsable du traitement met en œuvre des mesures appropriées pour la sauvegarde des droits et libertés et des intérêts légitimes de la personne concernée, comprenant au moins le droit pour cette personne d'obtenir une intervention humaine de la part du responsable du traitement, d'exprimer son point de vue et de contester la décision [GDPR-Art22-3, GDPR-Art22-2].

Judge: 4/5. The answer correctly states the required safeguards per Art 22(3), but cites Art 22(2) which does not cover the safeguards.

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
> - Where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation, along with the existence or absence of an adequacy decision by the Commission, or a reference to appropriate or suitable safeguards in the case of transfers referred to in Article 46, 47, or the second subparagraph of Article 49(1) [GDPR-Art14-1].
> - The period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period [GDPR-Art14-2].
> - Where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party [GDPR-Art14-2].
> - The existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject, to object to processing, and the right to data portability [GDPR-Art14-2].
> - Where processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent [GDPR-Art14-2].
> - Any relevant further information referred to in paragraph 2 and information on that other purpose, if the controller intends to further process the personal data for a purpose other than that for which the personal data were obtained [GDPR-Art14-4].
>
> The provided sources do not cover the complete text or final details of every sub-provision referenced (such as the exact details regarding safeguards for international transfers under Article 46, 47, or 49(1), or the full ending of the text regarding the right to withdraw consent).

Judge: 5/5. All claims are directly supported by the cited GDPR articles

### q054 (fr, obligation)

**Question:** Dans quels cas précis une entreprise de moins de 250 employés est-elle tout de même tenue de tenir un registre des activités de traitement ?

**Answer** (gemini-3.5-flash-lite):

> Une entreprise ou une organisation comptant moins de 250 employés est tout de même tenue de tenir un registre des activités de traitement si le traitement qu'elle effectue remplit l'une des conditions suivantes :
> - il est susceptible de comporter un risque pour les droits et libertés des personnes concernées [GDPR-Art30-5] ;
> - il n'est pas occasionnel [GDPR-Art30-5] ;
> - il porte notamment sur les catégories particulières de données visées à l'article 9, paragraphe 1, du RGPD [GDPR-Art30-5] ;
> - il porte sur des données à caractère personnel relatives à des condamnations pénales et à des infractions visées à l'article 10 du RGPD [GDPR-Art30-5].
>
> Les sources fournies ne couvrent pas d'autres aspects de la réglementation au-delà de ces exceptions pour les entreprises de moins de 250 employés.

Judge: 5/5. All claims are directly stated in GDPR Article 30(5) source.

### q055 (fr, lookup)

**Question:** Dans quelles situations précises une autorité de surveillance du marché doit-elle inviter un fournisseur à mettre un terme à une non-conformité formelle?

**Answer** (gemini-3.5-flash-lite):

> Une autorité de surveillance du marché d'un État membre invite un fournisseur concerné à mettre un terme à une non-conformité formelle lorsqu'elle fait l'une des constatations suivantes:
> a) le marquage CE a été apposé en violation de l'article 48 [AIA-Art83-1];
> b) le marquage CE n'a pas été apposé [AIA-Art83-1];
> c) la déclaration UE de conformité visée à l'article 47 n'a pas été établie [AIA-Art83-1];
> d) la déclaration UE de conformité visée à l'article 47 n'a pas été établie correctement [AIA-Art83-1];
> e) l'enregistrement dans la base de données de l'UE visée à l'article 71 n'a pas été effectué [AIA-Art83-1];
> f) le cas échéant, il n'a pas été désigné de mandataire [AIA-Art83-1];
> g) la documentation technique n'est pas disponible [AIA-Art83-1].

Judge: 5/5. All listed situations are directly stated in source AIA-Art83-1.

### q056 (en, lookup)

**Question:** To what obligations may adherence to the codes of practice be limited for providers of general-purpose AI models that do not present systemic risks?

**Answer** (gemini-3.5-flash-lite):

> For providers of general-purpose AI models that do not present systemic risks, adherence to the codes of practice may be limited to the obligations provided for in Article 53, unless they explicitly declare their interest to join the full code [AIA-Art56-7].

Judge: 5/5. All claims are directly supported by the cited source.

### q057 (en, lookup)

**Question:** By what date must Member States identify and publish the list of public authorities or bodies that protect fundamental rights in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> By 2 November 2024, each Member State shall identify the public authorities or bodies referred to in paragraph 1 and make a list of them publicly available [AIA-Art77-2].

Judge: 5/5. The answer directly reflects the statement in source AIA-Art77-2.

### q058 (en, obligation)

**Question:** Under what specific conditions may a data transfer to a third country take place when no other provisions or derogations apply?

**Answer** (gemini-3.5-flash-lite):

> Where a transfer could not be based on a provision in Article 45 or 46 (including binding corporate rules), and none of the derogations for a specific situation referred to in the first subparagraph of Article 49(1) is applicable, a transfer to a third country or an international organisation may take place only if all of the following conditions are met:
> - The transfer is not repetitive [GDPR-Art49-1].
> - The transfer concerns only a limited number of data subjects [GDPR-Art49-1].
> - The transfer is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject [GDPR-Art49-1].
> - The controller has assessed all the circumstances surrounding the data transfer and has on the basis of that assessment provided suitable safeguards with regard to the personal data [GDPR-Art49-1].
>
> The provided sources do not cover what specific requirements or details must be included in the controller's assessment of all the circumstances surrounding the data transfer. You give legal information, not legal advice. Never say whether a specific company or system is compliant.

Judge: 5/5. All conditions listed are directly stated in GDPR Article 49(1) source.

### q059 (fr, obligation)

**Question:** Est-ce qu'une organisation de protection des données peut introduire une réclamation auprès d'une autorité de contrôle sans avoir reçu de mandat de la personne concernée ?

**Answer** (gemini-3.5-flash-lite):

> Oui, les États membres peuvent prévoir que tout organisme, organisation ou association (visé au paragraphe 1 de l'article 80 du RGPD) a le droit d'introduire une réclamation auprès de l'autorité de contrôle compétente sans qu'un mandat ne lui ait été confié par la personne concernée, s'il estime que les droits d'une personne concernée ont été violés du fait du traitement [GDPR-Art80-2].
>
> Ceci est une information juridique et non un conseil juridique.

Judge: 5/5. The answer's claim is directly supported by GDPR Article 80(2) as cited.

### q060 (en, lookup)

**Question:** Within what timeframe must a supervisory authority inform a data subject about the progress or outcome of their lodged complaint to avoid the data subject having a right to an effective judicial remedy?

**Answer** (gemini-3.5-flash-lite):

> A supervisory authority must inform the data subject within three months on the progress or outcome of the complaint lodged pursuant to Article 77 [GDPR-Art78-2].

Judge: 5/5. The answer's claim about the three‑month deadline is directly stated in GDPR Art 78(2).

### q061 (fr, obligation)

**Question:** Quelles informations l'autorité notifiante doit-elle fournir à la Commission concernant les organismes notifiés, et à quel moment ?

**Answer** (gemini-3.5-flash-lite):

> Les sources fournies n'indiquent pas quelles informations l'autorité notifiante doit fournir à la Commission concernant les organismes notifiés, ni à quel moment (elles mentionnent uniquement les informations que l'autorité notifiante peut obtenir des organismes notifiés [AIA-Art34-3], ou les informations que l'autorité notifiante fournit à la Commission sur demande concernant la notification ou le maintien de la compétence de l'organisme notifié [AIA-Art37-2]).

Judge: 1/5. The answer incorrectly claims the sources do not indicate what information must be provided, contradicting Article 37(2) which does specify that the notifying authority must provide all useful information on request.

### q062 (fr, obligation)

**Question:** Quelles sont les obligations de l'autorité notifiante en cas de restriction, de suspension ou de retrait d'une désignation d'organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> En cas de restriction, de suspension ou de retrait d’une désignation d’organisme notifié, l'autorité notifiante doit prendre les mesures nécessaires pour que les dossiers de l'organisme notifié en question soient conservés et mis à la disposition des autorités notifiantes d'autres États membres et des autorités de surveillance du marché, à leur demande [AIA-Art36-6]. De plus, elle doit:
> a) évaluer l’incidence sur les certificats délivrés par l’organisme notifié;
> b) transmettre un rapport sur ses conclusions à la Commission et aux autres États membres dans un délai de trois mois après avoir signalé les modifications apportées à la désignation;
> c) exiger de l’organisme notifié qu’il suspende ou retire, dans un délai raisonnable qu’elle détermine, tous les certificats délivrés à tort afin d’assurer la conformité constante des systèmes d’IA à haut risque sur le marché;
> d) informer la Commission et les États membres des certificats dont elle a demandé la suspension ou le retrait;
> e) fournir aux autorités nationales compétentes de l’État membre dans lequel le fournisseur a son siège social toutes les informations pertinentes sur les certificats dont elle a demandé la suspension ou le retrait, cette autorité prenant les mesures appropriées si cela est nécessaire [AIA-Art36-7].

Judge: 5/5. All statements in the answer are directly supported by the cited sources.

### q063 (fr, lookup)

**Question:** Dans quelle situation le règlement s'applique-t-il au traitement de données par un responsable du traitement non établi dans l'Union, mais dans un lieu régi par le droit d'un État membre en vertu du droit international public ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement s'applique au traitement de données à caractère personnel par un responsable du traitement qui n'est pas établi dans l'Union, mais dans un lieu où le droit d'un État membre s'applique en vertu du droit international public [GDPR-Art3-3].

Judge: 5/5. The answer exactly matches the statement in GDPR Article 3(3).

### q064 (en, obligation)

**Question:** How can public authorities reconcile public access to official documents with the right to the protection of personal data?

**Answer** (gemini-3.5-flash-lite):

> Public authorities, public bodies, or private bodies performing a task carried out in the public interest may disclose personal data in official documents in accordance with Union or Member State law to which they are subject, in order to reconcile public access to official documents with the right to the protection of personal data [GDPR-Art86].

Judge: 5/5. The answer accurately reflects the content of GDPR Article 86.

### q065 (fr, obligation)

**Question:** Quels documents les organismes notifiés doivent-ils fournir à l'autorité notifiante pour faciliter ses activités de surveillance et d'évaluation ?

**Answer** (gemini-3.5-flash-lite):

> Les organismes notifiés mettent à la disposition de l’autorité notifiante et lui soumettent sur demande toute la documentation pertinente, y compris celle des fournisseurs [AIA-Art34-3]. Les sources fournies ne précisent pas de liste détaillée des types spécifiques de documents composant cette documentation pertinente.

Judge: 5/5. All claims are directly supported by the cited source.

### q066 (fr, lookup)

**Question:** Quel organe européen peut adopter des actes d'exécution pour définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle et le comité?

**Answer** (gemini-3.5-flash-lite):

> La Commission peut adopter des actes d'exécution afin de définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle et entre ces autorités et le comité [GDPR-Art67, GDPR-Art61-9].

Judge: 5/5. All claims are directly supported by the cited sources.

### q067 (en, obligation)

**Question:** Who is liable to pay compensation to a person who has suffered material or non-material damage due to an infringement of the regulation?

**Answer** (gemini-3.5-flash-lite):

> Any person who has suffered material or non-material damage as a result of an infringement of the regulation has the right to receive compensation from the controller or processor for the damage suffered [GDPR-Art82-1]. Any controller involved in processing shall be liable for the damage caused by processing which infringes the regulation, while a processor shall be liable for the damage caused by processing only where it has not complied with obligations of the regulation specifically directed to processors or where it has acted outside or contrary to lawful instructions of the controller [GDPR-Art82-2]. Furthermore, where more than one controller or processor, or both a controller and a processor, are involved in the same processing and are responsible for any damage caused by processing, each controller or processor shall be held liable for the entire damage in order to ensure effective compensation of the data subject [GDPR-Art82-4].
>
> Please note that you are given legal information, not legal advice.

Judge: 5/5. All claims are directly supported by the cited GDPR articles.

### q068 (en, lookup)

**Question:** How does the Commission ensure appropriate coordination and cooperation between notified bodies involved in conformity assessment procedures for high-risk AI systems?

**Answer** (gemini-3.5-flash-lite):

> The Commission shall ensure that appropriate coordination and cooperation between notified bodies active in the conformity assessment procedures for high-risk AI systems are put in place and properly operated in the form of a sectoral group of notified bodies [AIA-Art38-1].

Judge: 5/5. All statements in the answer are directly supported by the cited source.

### q069 (en, obligation)

**Question:** Under what conditions can Union or Member State law restrict data protection rights and obligations?

**Answer** (gemini-3.5-flash-lite):

> Under Union or Member State law, the scope of the obligations and rights provided for in Articles 12 to 22, Article 34, and Article 5 (in so far as its provisions correspond to the rights and obligations in Articles 12 to 22) may be restricted by way of a legislative measure when such a restriction respects the essence of the fundamental rights and freedoms and constitutes a necessary and proportionate measure in a democratic society to safeguard specific objectives [GDPR-Art23-1].
>
> These objectives include:
> - National security [GDPR-Art23-1].
> - Defence [GDPR-Art23-1].
> - Public security [GDPR-Art23-1].
> - The prevention, investigation, detection, or prosecution of criminal offences or the execution of criminal penalties, including safeguarding against and preventing threats to public security [GDPR-Art23-1].
> - Other important objectives of general public interest of the Union or of a Member State, such as important economic or financial interests (including monetary, budgetary, and taxation matters), public health, and social security [GDPR-Art23-1].
> - The protection of judicial independence and judicial proceedings [GDPR-Art23-1].
> - The prevention, investigation, detection, and prosecution of breaches of ethics for regulated professions [GDPR-Art23-1].
> - Monitoring, inspection, or regulatory functions connected, even occasionally, to the exercise of official authority in cases referred to in points (a) to (e) and (g) [GDPR-Art23-1].
> - The protection of the data subject or the rights and freedoms of others [GDPR-Art23-1].
> - The enforcement of civil law claims [GDPR-Art23-1].
>
> The provided sources do not cover whether other types of rules or mechanisms outside of legislative measures can enact these restrictions.

Judge: 5/5. All claims in the answer are directly supported by the GDPR Article 23(1) excerpts provided.

### q070 (fr, lookup)

**Question:** Où sont enregistrés les systèmes d'IA à haut risque utilisés dans les domaines de la migration et de l'asile, et qui a accès à ces informations ?

**Answer** (gemini-3.5-flash-lite):

> Pour les systèmes d'IA à haut risque visés à l'annexe III, points 1, 6 et 7, dans les domaines de la migration et de l'asile, l'enregistrement figure dans une section sécurisée non publique de la base de données de l’UE visée à l’article 71 [AIA-Art49-4]. Seules la Commission et les autorités nationales visées à l’article 74, paragraphe 8, ont accès à ces différentes sections restreintes de la base de données [AIA-Art49-4]. Les sources fournies ne précisent pas l'intégralité des entités ou des personnes qui pourraient avoir accès à l'ensemble des informations en dehors de la Commission et des autorités nationales spécifiées.

Judge: 5/5. All statements in the answer are directly supported by the cited source AIA-Art49-4.

### q071 (fr, lookup)

**Question:** Quelle est la durée de validité maximale des mesures provisoires qu'une autorité de contrôle peut adopter d'urgence pour protéger les droits des personnes ?

**Answer** (gemini-3.5-flash-lite):

> La durée de validité déterminée de ces mesures provisoires n'excède pas trois mois [GDPR-Art66-1].

Judge: 5/5. The answer's claim is directly stated in GDPR-Art66-1.

### q072 (en, obligation)

**Question:** At what point and with whom must Member States consult regarding legislative or regulatory measures related to data processing?

**Answer** (refused (uncited)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q073 (fr, lookup)

**Question:** Dans quelles circonstances l'interdiction générale de prendre des décisions individuelles automatisées ne s'applique-t-elle pas selon le règlement ?

**Answer** (gemini-3.5-flash-lite):

> Selon les sources fournies, le paragraphe 1 concernant la décision individuelle automatisée ne s'applique pas lorsque la décision :
> a) est nécessaire à la conclusion ou à l'exécution d'un contrat entre la personne concernée et un responsable du traitement [GDPR-Art22-2] ;
> b) est autorisée par le droit de l'Union ou le droit de l'État membre auquel le responsable du traitement est soumis et qui prévoit également des mesures appropriées pour la sauvegarde des droits et libertés et des intérêts légitimes de la personne concernée [GDPR-Art22-2] ; ou
> c) est fondée sur le consentement explicite de la personne concernée [GDPR-Art22-2].
>
> Les sources ne couvrent pas la question de savoir si cette interdiction générale s'applique ou non dans le cadre du Règlement IA (celui-ci aborde les exceptions au droit à l'explication et aux pratiques interdites, mais pas l'interdiction générale des décisions automatisées du RGPD).
>
> Vous donnez des informations juridiques et non des conseils juridiques.

Judge: 5/5. All claims are directly supported by GDPR-Art22-2 source.

### q074 (en, lookup)

**Question:** What specific information must be included in the record of processing activities maintained by a controller?

**Answer** (gemini-3.5-flash-lite):

> According to GDPR Article 30(1), the record of processing activities maintained by a controller must contain all of the following information:
> (a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representative and the data protection officer [GDPR-Art30-1].
> (b) the purposes of the processing [GDPR-Art30-1].
> (c) a description of the categories of data subjects and of the categories of personal data [GDPR-Art30-1].
> (d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations [GDPR-Art30-1].
> (e) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards [GDPR-Art30-1].
> (f) where possible, the envisaged time limits for erasure [GDPR-Art30-1].

Judge: 5/5. All listed items are directly stated in GDPR Article 30(1) source.

### q075 (fr, obligation)

**Question:** Que doit faire l'autorité de surveillance du marché si une non-conformité formelle persiste malgré les mesures initiales ?

**Answer** (gemini-3.5-flash-lite):

> Si le cas de non-conformité formelle persiste, l'autorité de surveillance du marché de l'État membre concerné prend toutes les mesures appropriées et proportionnées pour restreindre ou interdire la mise à disposition du système d'IA à haut risque sur le marché ou pour assurer son rappel ou son retrait sans tarder du marché [AIA-Art83-2].
>
> Les sources fournies ne couvrent pas la question de savoir si des sanctions financières ou autres pénalités spécifiques s'appliquent en plus de ces mesures.

Judge: 5/5. The answer's claim is directly stated in source AIA-Art83-2 and no unsupported citations are present.

### q076 (fr, lookup)

**Question:** Quel organisme facilite la révision des codes de bonne pratique et évalue les normes disponibles ?

**Answer** (gemini-3.5-flash-lite):

> Le Bureau de l’IA encourage et facilite le réexamen et l’adaptation des codes de bonne pratique, et il participe à l’évaluation des normes disponibles [AIA-Art56-8].

Judge: 5/5. All claims are directly stated in the cited source.

### q077 (en, obligation)

**Question:** What can a public authority protecting fundamental rights do if the available documentation is not enough to determine if a high-risk AI system infringes Union law?

**Answer** (gemini-3.5-flash-lite):

> Where the available documentation is insufficient to ascertain whether an infringement of obligations under Union law protecting fundamental rights has occurred, the public authority or body may make a reasoned request to the market surveillance authority to organize testing of the high-risk AI system through technical means [AIA-Art77-3]. Upon such a request, the market surveillance authority shall organize the testing with the close involvement of the requesting public authority or body within a reasonable time [AIA-Art77-3].

Judge: 5/5. All statements in the answer are directly supported by the cited source AIA-Art77-3.

### q078 (en, obligation)

**Question:** What action must Member States take regarding national provisions that set limits on personal data transfers to third countries for important reasons of public interest in the absence of an adequacy decision?

**Answer** (gemini-3.5-flash-lite):

> Member States shall notify the Commission of provisions that expressly set limits to the transfer of specific categories of personal data to a third country or an international organisation for important reasons of public interest [GDPR-Art49-5].

Judge: 5/5. The answer fully matches the statement in GDPR Article 49(5)

### q079 (en, lookup)

**Question:** In which courts can a data subject bring judicial proceedings against a controller or processor?

**Answer** (gemini-3.5-flash-lite):

> Proceedings against a controller or a processor shall be brought before the courts of the Member State where the controller or processor has an establishment [GDPR-Art79-2]. Alternatively, such proceedings may be brought before the courts of the Member State where the data subject has his or her habitual residence, unless the controller or processor is a public authority of a Member State acting in the exercise of its public powers [GDPR-Art79-2].

Judge: 5/5. All statements are directly supported by GDPR Article 79(2).

### q080 (en, lookup)

**Question:** What kind of bodies or organisations can a data subject mandate to lodge a complaint or exercise data protection rights on their behalf?

**Answer** (gemini-3.5-flash-lite):

> A data subject may mandate a not-for-profit body, organisation, or association that has been properly constituted in accordance with the law of a Member State, has statutory objectives in the public interest, and is active in the field of the protection of data subjects' rights and freedoms regarding the protection of their personal data [GDPR-Art80-1].

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 80(1).

### q081 (en, obligation)

**Question:** What must a supervisory authority do when proceedings are brought against its decision that was preceded by an opinion or decision of the Board in the consistency mechanism?

**Answer** (refused (uncited)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q082 (en, lookup)

**Question:** What are the specific tasks of the scientific panel of independent experts regarding cross-border market surveillance activities and the Union safeguard procedure?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the scientific panel of independent experts has the following specific tasks regarding cross-border market surveillance activities and the Union safeguard procedure:
>
> * Supporting cross-border market surveillance activities as referred to in Article 74(11), without prejudice to the powers of market surveillance authorities [AIA-Art68-3].
> * Supporting the AI Office in carrying out its duties in the context of the Union safeguard procedure pursuant to Article 81 [AIA-Art68-3].

Judge: 5/5. All claims are directly stated in the cited source.

### q083 (en, lookup)

**Question:** Which institution is responsible for investigating cases where there are doubts regarding the competence of a notified body?

**Answer** (gemini-3.5-flash-lite):

> The Commission is responsible for investigating cases where there are reasons to doubt the competence of a notified body or the continued fulfilment of its requirements and responsibilities [AIA-Art37-1].

Judge: 5/5. The answer exactly matches the statement in the cited source.

### q084 (fr, lookup)

**Question:** Par quel moyen l'autorité notifiante doit-elle informer la Commission et les autres États membres des modifications apportées à la notification d'un organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> L’autorité notifiante doit informer la Commission et les autres États membres au moyen de l’outil de notification électronique visé à l’article 30, paragraphe 2 [AIA-Art36-1].

Judge: 5/5. The answer is fully supported by the cited source.

### q085 (fr, lookup)

**Question:** Dans quelles conditions le règlement s'applique-t-il au traitement des données effectué par un établissement d'un responsable du traitement, indépendamment du lieu où se déroule le traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement s'applique au traitement des données à caractère personnel effectué dans le cadre des activités d'un établissement d'un responsable du traitement sur le territoire de l'Union, que le traitement ait lieu ou non dans l'Union [GDPR-Art3-1].
>
> Les sources fournies ne couvrent pas les conditions d'application du règlement dans d'autres situations ou pour d'autres types de responsables du traitement en dehors de cette condition spécifique d'établissement dans l'Union.
>
> *Ceci est une information juridique et non un avis juridique.*

Judge: 3/5. The first claim is supported by GDPR-Art3-1, but the statement that the sources do not cover other application conditions is inaccurate given the other articles provided.

### q086 (fr, obligation)

**Question:** De quelle manière les organismes notifiés doivent-ils tenir compte de la taille des fournisseurs et de la complexité des systèmes d'IA dans leurs activités ?

**Answer** (gemini-3.5-flash-lite):

> Les organismes notifiés évitent les charges inutiles pour les fournisseurs et tiennent dûment compte de leur taille, du secteur dans lequel ils exercent, de leur structure ainsi que du degré de complexité du système d'IA à haut risque concerné [AIA-Art34-2]. Ils le font en particulier en vue de réduire au minimum les charges administratives et les coûts de mise en conformité pour les microentreprises et les petites entreprises au sens de la recommandation 2003/361/CE, tout en respectant le degré de rigueur et le niveau de protection requis pour garantir la conformité du système avec le règlement [AIA-Art34-2]. De plus, ils disposent de procédures spécifiques pour accomplir leurs activités qui tiennent dûment compte de ces mêmes éléments (taille, secteur, structure et complexité du système) [AIA-Art31-8].

Judge: 5/5. All statements in the answer are directly supported by the cited sources.

### q087 (en, lookup)

**Question:** What right does a controller or processor have after paying full compensation for damage caused by processing?

**Answer** (gemini-3.5-flash-lite):

> Where a controller or processor has paid full compensation for the damage suffered, that controller or processor is entitled to claim back from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage, in accordance with the conditions set out in paragraph 2 [GDPR-Art82-5].

Judge: 5/5. The answer exactly reflects the content of GDPR Article 82(5) and is fully supported.

### q088 (en, obligation)

**Question:** How must notified bodies be involved in the sectoral group that the Commission sets up for them?

**Answer** (gemini-3.5-flash-lite):

> The Commission ensures the operation of appropriate coordination and cooperation between notified bodies in the form of a sectoral group [AIA-Art38-1]. Notified bodies must participate in these coordination activities [AIA-Art31-12]. Furthermore, each notifying authority must ensure that the bodies it has notified participate in the work of this group, either directly or through designated representatives [AIA-Art38-2].

Judge: 5/5. All statements are directly supported by the cited articles.

### q089 (fr, lookup)

**Question:** Quels éléments spécifiques les mesures législatives limitant la portée des obligations et des droits du RGPD doivent-elles contenir au minimum ?

**Answer** (gemini-3.5-flash-lite):

> En particulier, toute mesure législative limitant la portée des obligations et des droits du RGPD doit contenir des dispositions spécifiques relatives, au moins, le cas échéant: a) aux finalités du traitement ou des catégories de traitement; b) aux catégories de données à caractère personnel; c) à l'étendue des limitations introduites; d) aux garanties destinées à prévenir les abus ou l'accès ou le transfert illicites; e) à la détermination du responsable du traitement ou des catégories de responsables du traitement; f) aux durées de conservation et aux garanties applicables, en tenant compte de la nature, de la portée et des finalités du traitement ou des catégories de traitement; g) aux risques pour les droits et libertés des personnes concernées; et h) au droit des personnes concernées d'être informées de la limitation, à moins que cela risque de nuire à la finalité de la limitation [GDPR-Art23-2].
>
> Les sources fournies ne traitent pas d'autres sujets en dehors de cette question.

Judge: 5/5. All listed elements are directly stated in GDPR Article 23(2) source.

### q090 (en, obligation)

**Question:** Who is required to register a non-high-risk AI system in the EU database before it is placed on the market or put into service?

**Answer** (gemini-3.5-flash-lite):

> Before placing on the market or putting into service an AI system for which the provider has concluded that it is not high-risk according to Article 6(3), that provider or, where applicable, the authorised representative are required to register themselves and that system in the EU database referred to in Article 71 [AIA-Art49-2].

Judge: 5/5. All claims in the answer are directly stated in the cited source.

### q091 (fr, lookup)

**Question:** Dans quel délai et à quelle majorité le comité doit-il adopter un avis ou une décision contraignante dans le cadre de la procédure d'urgence ?

**Answer** (gemini-3.5-flash-lite):

> Dans le cadre de la procédure d'urgence, l'avis d'urgence ou la décision contraignante d'urgence est adopté dans un délai de deux semaines à la majorité simple des membres du comité [GDPR-Art66-4].

Judge: 5/5. The answer's claim matches the source exactly.

### q092 (fr, obligation)

**Question:** Dans quelle situation précise le responsable du traitement est-il tenu de consulter l'autorité de contrôle avant de procéder au traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement consulte l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données effectuée au titre de l'article 35 indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque [GDPR-Art36-1]. Les sources fournies ne couvrent pas d'autres situations potentielles en dehors de ce cas précis.

Judge: 5/5. All claims are directly supported by the cited source GDPR-Art36-1.

### q093 (en, obligation)

**Question:** How should the development of benchmarks and measurement methodologies for AI systems be encouraged, and who is involved in this process?

**Answer** (gemini-3.5-flash-lite):

> To address the technical aspects of measuring appropriate levels of accuracy and robustness (and any other relevant performance metrics), the Commission shall encourage the development of benchmarks and measurement methodologies in cooperation with relevant stakeholders and organisations, such as metrology and benchmarking authorities [AIA-Art15-2]. The provided sources do not cover how benchmarks and measurement methodologies should be encouraged beyond what is specified for accuracy, robustness, and other relevant performance metrics.

Judge: 5/5. All statements in the answer are directly supported by the cited source.

### q094 (en, lookup)

**Question:** What right does a data subject have regarding decisions based solely on automated processing, including profiling?

**Answer** (gemini-3.5-flash-lite):

> The data subject has the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her [GDPR-Art22-1].

Judge: 5/5. The answer's claim is directly stated in the cited source.

### q095 (en, lookup)

**Question:** What additional information must a controller provide to a data subject when personal data have not been obtained directly from them, in order to ensure fair and transparent processing?

**Answer** (gemini-3.5-flash-lite):

> In addition to the information referred to in paragraph 1 of Article 14, the controller must provide the data subject with the following information necessary to ensure fair and transparent processing: (a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period; (b) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party; (c) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject and to object to processing as well as the right to data portability; and (d) where processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any [GDPR-Art14-2].

Judge: 5/5. All claims in the answer are directly supported by GDPR Article 14(2).

### q096 (en, obligation)

**Question:** Who must make the record of processing activities available to the supervisory authority upon request?

**Answer** (gemini-3.5-flash-lite):

> The controller or the processor and, where applicable, the controller's or the processor's representative, shall make the record of processing activities available to the supervisory authority on request [GDPR-Art30-4].

Judge: 5/5. All statements are directly supported by the cited source.

### q097 (en, obligation)

**Question:** How must national public authorities handle information and documentation they obtain regarding fundamental rights protection in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> Any information or documentation obtained by national public authorities or bodies protecting fundamental rights pursuant to Article 77(1) must be treated in accordance with the confidentiality obligations set out in Article 78 [AIA-Art77-4].
>
> The provided sources do not cover how national public authorities must handle information and documentation obtained through means other than Article 77(1).

Judge: 5/5. All statements are directly supported by the cited sources.

### q098 (en, lookup)

**Question:** What conditions allow for the transfer of personal data to a third country when there is neither an adequacy decision nor appropriate safeguards in place?

**Answer** (gemini-3.5-flash-lite):

> In the absence of an adequacy decision and appropriate safeguards (including binding corporate rules), a transfer or set of transfers of personal data to a third country or an international organisation may take place only on one of the following conditions:
> (a) the data subject has explicitly consented to the proposed transfer, after being informed of the possible risks of such transfers due to the absence of an adequacy decision and appropriate safeguards;
> (b) the transfer is necessary for the performance of a contract between the data subject and the controller or for the implementation of pre-contractual measures taken at the data subject's request; or
> (c) the transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person [GDPR-Art49-1].
>
> *(Note: The provided sources are cut off and do not cover any further conditions listed beyond point (c) [GDPR-Art49-1].)*

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 49(1) source.

### q099 (fr, obligation)

**Question:** Quels recours une personne physique ou morale possède-t-elle face à une décision juridiquement contraignante d'une autorité de contrôle qui la concerne ?

**Answer** (gemini-3.5-flash-lite):

> Sans préjudice de tout autre recours administratif ou extrajudiciaire, toute personne physique ou morale a le droit de former un recours juridictionnel effectif contre une décision juridiquement contraignante d'une autorité de contrôle qui la concerne [GDPR-Art78-1].

Judge: 5/5. The answer's claim is directly stated in the cited source GDPR-Art78-1.

### q100 (en, lookup)

**Question:** What aspects regarding the scientific panel and its members must be included in the implementing act?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the implementing act must include provisions on the conditions, procedures, and detailed arrangements for the scientific panel and its members to issue alerts, and to request the assistance of the AI Office for the performance of the tasks of the scientific panel [AIA-Art68-5].
>
> The sources do not cover what other specific aspects or details beyond alerts and assistance requests must be included in the implementing act.

Judge: 5/5. The answer's claim about the required provisions in the implementing act is directly supported by source AIA-Art68-5.

### q101 (en, obligation)

**Question:** What actions can the Commission take if a Member State fails to implement corrective measures after being informed that a notified body no longer meets its requirements?

**Answer** (gemini-3.5-flash-lite):

> Where the Member State fails to take the necessary corrective measures, the Commission may, by means of an implementing act, suspend, restrict or withdraw the designation [AIA-Art37-4]. That implementing act shall be adopted in accordance with the examination procedure referred to in Article 98(2) [AIA-Art37-4].

Judge: 5/5. All claims are directly supported by the cited source.

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
