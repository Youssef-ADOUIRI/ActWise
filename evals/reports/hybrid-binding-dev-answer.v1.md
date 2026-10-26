# Retrieval report: hybrid-binding-dev-answer.v1

E: as C, with articles and annexes ranked before recitals. Split `dev`, 20 scored questions (2 out-of-scope questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.

| Metric | Value |
|---|---|
| Recall@1 | 0.600 |
| **Recall@5** | **0.925** [0.80, 1.00] |
| Recall@10 | 1.000 |
| Recall@20 | 1.000 |
| MRR@10 | 0.806 [0.69, 0.93] |
| nDCG@10 | 0.842 |
| ms / query | 158 |

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

## Answers: `answer.v1`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 22 |
| in_scope | 20 |
| out_of_scope | 2 |
| refusal_rate | 1.0 |
| false_refusal_rate | 0.2 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.8696 |
| citation_precision_lenient | 1.0 |
| faithfulness | 1.0 |
| faithfulness_ci95 | (1.0, 1.0) |
| judged | 16 |
| judge_failed | 0 |
| uncited_sentences | 0.0 |
| input_tokens | 20123 |
| output_tokens | 1979 |

### q001 (en, lookup)

**Question:** Is trafficking in human beings one of the crimes for which the police may be allowed to use real-time facial recognition in public spaces to locate a suspect?

**Answer** (gemini-3.5-flash-lite):

> Yes, trafficking in human beings is listed as one of the criminal offences referred to in Article 5(1), first subparagraph, point (h)(iii), for which the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement may be strictly necessary and allowed [AIA-Art5-1, AIA-AnnexII].

Judge: 5/5. All claims are directly supported by the cited sources.

### q002 (fr, lookup)

**Question:** Quelles mentions doit contenir la déclaration UE de conformité d'un système d'IA à haut risque ?

**Answer** (gemini-3.5-flash-lite):

> La déclaration UE de conformité d'un système d'IA à haut risque doit attester qu'il satisfait aux exigences énoncées à la section 2 [AIA-Art47-2]. Elle doit également contenir les informations qui figurent à l'annexe V [AIA-Art47-2]. De plus, si le système d'IA à haut risque est soumis à d'autres actes législatifs d'harmonisation de l'Union exigeant également une déclaration UE de conformité, elle doit contenir toutes les informations nécessaires à l'identification de la législation d'harmonisation de l'Union à laquelle elle se rapporte [AIA-Art47-3].

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

> La Commission enquête, s’il y a lieu, sur tous les cas où il existe des raisons de douter de la compétence d’un organisme notifié ou du respect continu, par un organisme notifié, des exigences établies à l’article 31 et de ses responsabilités applicables [AIA-Art37-1]. De plus, lorsqu'une autorité notifiante a des raisons suffisantes de considérer qu’un organisme notifié ne répond plus aux exigences définies à l’article 31 ou qu’il ne s’acquitte pas de ses obligations, elle procède sans retard à une enquête avec la plus grande diligence [AIA-Art36-4].

Judge: 5/5. All statements are directly supported by the cited articles.

### q006 (en, obligation)

**Question:** Does a public authority that starts using a high-risk AI system to decide who receives social benefits have to register that use in an EU database?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q007 (en, lookup)

**Question:** Who facilitates the drawing up of codes of practice for general-purpose AI models, and by when were they supposed to be ready?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q008 (fr, lookup)

**Question:** Quelles conditions doivent remplir les experts du groupe scientifique qui conseille le Bureau de l'IA ?

**Answer** (gemini-3.5-flash-lite):

> Les experts du groupe scientifique doivent être sélectionnés par la Commission en fonction de leur expertise à la pointe des connaissances scientifiques ou techniques dans le domaine de l'IA, nécessaire pour s'acquitter des tâches prévues [AIA-Art68-2]. Ils doivent en outre être en mesure de démontrer qu'ils remplissent toutes les conditions suivantes :
> a) disposer d'une expertise et d'une compétence particulières ainsi que d'une expertise scientifique ou technique dans le domaine de l'IA [AIA-Art68-2];
> b) être indépendants vis-à-vis de tout fournisseur de systèmes d'IA ou de modèles d'IA à usage général [AIA-Art68-2];
> c) être capables de mener des activités avec diligence, précision et objectivité [AIA-Art68-2].
>
> De plus, ils s'acquittent de leurs tâches avec impartialité et objectivité, et garantissent la confidentialité des informations et des données obtenues dans l'exercice de leurs tâches et activités [AIA-Art68-4]. Ils ne doivent pas solliciter ni accepter d'instructions de quiconque dans l'exercice de leurs tâches, et chacun d'eux doit établir une déclaration d'intérêts qui est rendue publique [AIA-Art68-4].

Judge: 5/5. All statements in the answer are directly supported by the cited articles.

### q009 (en, definition)

**Question:** Which situations count as formal non-compliance of a high-risk AI system, such as a missing CE marking?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the following situations count as formal non-compliance for a high-risk AI system:
> * The CE marking has been affixed in violation of Article 48 [AIA-Art83-1].
> * The CE marking has not been affixed [AIA-Art83-1].
> * The EU declaration of conformity referred to in Article 47 has not been drawn up [AIA-Art83-1].
> * The EU declaration of conformity referred to in Article 47 has not been drawn up correctly [AIA-Art83-1].
> * The registration in the EU database referred to in Article 71 has not been carried out [AIA-Art83-1].
> * Where applicable, no authorised representative has been appointed [AIA-Art83-1].
> * Technical documentation is not available [AIA-Art83-1].

Judge: 5/5. All listed situations are directly stated in Article 83(1) of the AI Act.

### q010 (en, lookup)

**Question:** Does the GDPR apply to a company based outside the EU that tracks the online behaviour of people in the EU?

**Answer** (gemini-3.5-flash-lite):

> Yes, the GDPR applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to the monitoring of their behaviour as far as their behaviour takes place within the Union [GDPR-Art3-2].

Judge: 5/5. The answer's claim is fully supported by GDPR Article 3(2).

### q011 (fr, obligation)

**Question:** Lorsque des données personnelles n'ont pas été collectées auprès de la personne concernée, dans quel délai le responsable du traitement doit-il l'informer ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement fournit les informations dans un délai raisonnable après avoir obtenu les données à caractère personnel, mais ne dépassant pas un mois, eu égard aux circonstances particulières dans lesquelles les données à caractère personnel sont traitées [GDPR-Art14-3].
>
> Cependant, si les données à caractère personnel doivent être utilisées aux fins de la communication avec la personne concernée, le responsable du traitement fournit les informations au plus tard au moment de la première communication à ladite personne [GDPR-Art14-3].
>
> De plus, s'il est envisagé de communiquer les informations à un autre destinataire, les informations doivent être fournies au plus tard lorsque les données à caractère personnel sont communiquées pour la première fois [GDPR-Art14-3].

Judge: 5/5. All statements are directly supported by GDPR Article 14(3) as cited.

### q012 (en, lookup)

**Question:** Can a bank reject my loan application based only on an automated decision, with no human involved?

**Answer** (gemini-3.5-flash-lite):

> The data subject has the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning them or similarly significantly affects them [GDPR-Art22-1]. However, this right does not apply if the decision is necessary for entering into, or performance of, a contract between the data subject and a data controller, is authorised by Union or Member State law that lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, or is based on the data subject's explicit consent [GDPR-Art22-2].

Judge: 5/5. All statements are directly supported by the cited GDPR articles.

### q013 (fr, obligation)

**Question:** Dans quel cas le responsable du traitement doit-il consulter l'autorité de contrôle avant de commencer un traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement consulte l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données effectuée au titre de l'article 35 indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque [GDPR-Art36-1]. De plus, nonobstant ce cas, le droit des États membres peut exiger que les responsables du traitement consultent l'autorité de contrôle et obtiennent son autorisation préalable en ce qui concerne le traitement effectué par un responsable du traitement dans le cadre d'une mission d'intérêt public exercée par celui-ci, y compris le traitement dans le cadre de la protection sociale et de la santé publique [GDPR-Art36-5].

Judge: 5/5. All statements are directly supported by the cited GDPR articles.

### q014 (en, lookup)

**Question:** Can personal data be sent to a country without an adequacy decision if the person explicitly agrees to the transfer?

**Answer** (gemini-3.5-flash-lite):

> Yes, in the absence of an adequacy decision or appropriate safeguards, a transfer or set of transfers of personal data to a third country or an international organisation may take place if the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards [GDPR-Art49-1].

Judge: 5/5. The answer's claim is directly stated in GDPR Article 49(1).

### q015 (en, lookup)

**Question:** In an emergency, can a national data protection authority act on its own without going through the cooperation procedure with other authorities, and for how long?

**Answer** (gemini-3.5-flash-lite):

> Oui, dans des circonstances exceptionnelles, lorsqu'une autorité de contrôle concernée considère qu'il est urgent d'intervenir pour protéger les droits et libertés des personnes concernées, elle peut, par dérogation au mécanisme de cohérence ou à la procédure de coopération, adopter immédiatement des mesures provisoires destinées à produire des effets juridiques sur son propre territoire [GDPR-Art66-1]. La durée de validité de ces mesures ne doit pas excéder trois mois [GDPR-Art66-1].

Judge: 5/5. All claims are directly supported by GDPR Article 66(1).

### q016 (en, lookup)

**Question:** What can I do if the data protection authority does not deal with my complaint?

**Answer** (gemini-3.5-flash-lite):

> Without prejudice to any other administrative or non-judicial remedy, you have the right to an effective judicial remedy if the competent supervisory authority does not handle a complaint or does not inform you within three months on the progress or outcome of the complaint lodged pursuant to Article 77 [GDPR-Art78-2].

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR article.

### q017 (fr, lookup)

**Question:** Devant quels tribunaux puis-je agir contre une entreprise qui a violé mes droits au titre du RGPD ?

**Answer** (gemini-3.5-flash-lite):

> Toute action contre un responsable du traitement ou un sous-traitant est intentée devant les juridictions de l'État membre dans lequel le responsable du traitement ou le sous-traitant dispose d'un établissement [GDPR-Art79-2]. Une telle action peut aussi être intentée devant les juridictions de l'État membre dans lequel la personne concernée a sa résidence habituelle, sauf si le responsable du traitement ou le sous-traitant est une autorité publique d'un État membre agissant dans l'exercice de ses prérogatives de puissance publique [GDPR-Art79-2].

Judge: 5/5. All statements are directly supported by GDPR Article 79(2) as cited.

### q018 (en, obligation)

**Question:** If a processor ignores the controller's instructions and this causes damage to someone, does the processor have to pay compensation?

**Answer** (gemini-3.5-flash-lite):

> Yes, a processor shall be liable for the damage caused by processing where it has acted outside or contrary to lawful instructions of the controller [GDPR-Art82-2]. Furthermore, any person who has suffered material or non-material damage as a result of an infringement of the Regulation has the right to receive compensation from the controller or processor for the damage suffered [GDPR-Art82-1].

Judge: 5/5. All statements are directly supported by the cited GDPR articles.

### q019 (en, cross_law)

**Question:** We provide an AI tool that screens job applicants. What must our GDPR record of processing activities contain, and does the AI Act also require us to register the tool in an EU database?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q020 (fr, cross_law)

**Question:** Une association de défense des droits peut-elle agir au nom de personnes discriminées par un système d'IA, et quelles autorités peuvent exiger la documentation de ce système ?

**Answer** (refused (not_covered)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.

### q021 (en, not_covered)

**Question:** What fines can the European Commission impose on gatekeepers that breach the Digital Markets Act?

**Answer** (refused (not_covered)):

> I can't answer this from the text of the AI Act or the GDPR that I have. Please rephrase the question, or ask a lawyer.

### q022 (fr, not_covered)

**Question:** Quelles obligations le règlement sur les données (Data Act) impose-t-il aux fabricants d'objets connectés ?

**Answer** (refused (not_covered)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.
