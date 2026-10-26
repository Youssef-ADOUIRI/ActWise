# Retrieval report: hybrid-binding-dev-answer.v2

E: as C, with articles and annexes ranked before recitals. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.600 |
| **Recall@5** | **0.925** [0.80, 1.00] |
| Recall@10 | 1.000 |
| Recall@20 | 1.000 |
| MRR@10 | 0.806 [0.69, 0.93] |
| nDCG@10 | 0.842 |
| ms / query | 152 |

## By language

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| en | 13 | 1.000 | 0.769 |
| fr | 7 | 0.786 | 0.873 |

## By question type

| | n | Recall@5 | MRR@10 |
|---|---|---|---|
| cross_law | 2 | 0.750 | 0.750 |
| definition | 1 | 1.000 | 0.500 |
| lookup | 12 | 0.917 | 0.759 |
| obligation | 5 | 1.000 | 1.000 |

## Questions whose gold article is not ranked first

| Question | Gold | First hit | Top 3 retrieved |
|---|---|---|---|
| q001 (en) | AIA-AnnexII | 2 | AIA-Art5, AIA-AnnexII, AIA-Art61 |
| q009 (en) | AIA-Art83 | 2 | AIA-Art48, AIA-Art83, AIA-Art24 |
| q010 (en) | GDPR-Art3 | 2 | GDPR-Art2, GDPR-Art3, GDPR-Art47 |
| q014 (en) | GDPR-Art49 | 2 | GDPR-Art45, GDPR-Art49, GDPR-Art48 |
| q016 (en) | GDPR-Art78 | 2 | GDPR-Art12, GDPR-Art78, GDPR-Art77 |
| q019 (en) | GDPR-Art30, AIA-Art49 | 2 | AIA-Art71, AIA-Art49, AIA-AnnexV |
| q002 (fr) | AIA-AnnexV | 9 | AIA-Art47, AIA-Art16, AIA-AnnexVIII |

## Answers: `answer.v2`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 22 |
| in_scope | 20 |
| out_of_scope | 2 |
| refusal_rate | 1.0 |
| false_refusal_rate | 0.0 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.8276 |
| citation_precision_lenient | 0.8966 |
| faithfulness | 0.9875 |
| faithfulness_ci95 | (0.9625, 1.0) |
| judged | 20 |
| judge_failed | 0 |
| uncited_sentences | 0.65 |
| input_tokens | 20739 |
| output_tokens | 2475 |

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
