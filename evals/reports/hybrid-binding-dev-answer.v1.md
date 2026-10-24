# Retrieval report: hybrid-binding-dev-answer.v1

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

## Answers: `answer.v1`

Top 5 passages, temperature 0, judge: {'fallback': [{'provider': 'groq', 'model': 'openai/gpt-oss-120b'}], 'prompt': 'judge.v1'}.

| Metric | Value |
|---|---|
| n | 83 |
| in_scope | 71 |
| out_of_scope | 12 |
| refusal_rate | 1.0 |
| false_refusal_rate | 0.0704 |
| invented_citations | 0 |
| invented_shown | 0 |
| citation_precision_strict | 0.925 |
| citation_precision_lenient | 1.0 |
| faithfulness | 0.9924 |
| faithfulness_ci95 | (0.9773, 1.0) |
| judged | 66 |
| judge_failed | 0 |
| uncited_sentences | 0.02 |
| input_tokens | 75268 |
| output_tokens | 7368 |

| Source | n | Refused (out of scope) | False refusals | Faithfulness |
|---|---|---|---|---|
| hand | 22 | 1.0 | 0.2 | 1.0 |
| synthetic | 61 | 1.0 | 0.0196 | 0.99 |

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

### q051 (en, lookup)

**Question:** What specific types of attacks must the technical solutions for high-risk AI systems address, where appropriate, to counter AI-specific vulnerabilities?

**Answer** (gemini-3.5-flash-lite):

> To address AI-specific vulnerabilities, the technical solutions for high-risk AI systems shall include, where appropriate, measures to prevent, detect, respond to, resolve, and control for the following types of attacks:
> - Attacks trying to manipulate the training data set (data poisoning) or pre-trained components used in training (model poisoning) [AIA-Art15-5].
> - Inputs designed to cause the AI model to make a mistake (adversarial examples or model evasion) [AIA-Art15-5].
> - Confidentiality attacks [AIA-Art15-5].
> - Model flaws [AIA-Art15-5].

Judge: 5/5. All listed attack types are explicitly mentioned in the cited source.

### q052 (fr, obligation)

**Question:** Quelles mesures minimales le responsable du traitement doit-il mettre en œuvre pour protéger les intérêts d'une personne concernée par une décision individuelle automatisée fondée sur un contrat ou un consentement ?

**Answer** (gemini-3.5-flash-lite):

> Dans les cas où la décision est nécessaire à la conclusion ou à l'exécution d'un contrat ou est fondée sur le consentement explicite de la personne concernée, le responsable du traitement met en œuvre des mesures appropriées pour la sauvegarde des droits et libertés et des intérêts légitimes de la personne concernée, comprenant au moins le droit d'obtenir une intervention humaine de sa part, d'exprimer son point de vue et de contester la décision [GDPR-Art22-3, GDPR-Art22-2].

Judge: 5/5. All claims are directly supported by the cited GDPR articles.

### q053 (en, lookup)

**Question:** What specific information must a controller provide to a data subject when the personal data have not been obtained directly from them?

**Answer** (gemini-3.5-flash-lite):

> When personal data have not been obtained from the data subject, the controller shall provide the data subject with the following information:
> - The identity and the contact details of the controller and, where applicable, of the controller's representative [GDPR-Art14-1].
> - The contact details of the data protection officer, where applicable [GDPR-Art14-1].
> - The purposes of the processing for which the personal data are intended as well as the legal basis for the processing [GDPR-Art14-1].
> - The categories of personal data concerned [GDPR-Art14-1].
> - The recipients or categories of recipients of the personal data, if any [GDPR-Art14-1].
> - Where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation, along with the existence or absence of an adequacy decision by the Commission, or reference to the appropriate safeguards in the case of transfers referred to in Article 46, 47, or the second subparagraph of Article 49(1) [GDPR-Art14-1].
> - The period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period [GDPR-Art14-2].
> - Where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party [GDPR-Art14-2].
> - The existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject and to object to processing as well as the right to data portability [GDPR-Art14-2].
> - Where processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent [GDPR-Art14-2].
> - Any other relevant further information necessary to ensure fair and transparent processing in respect of the data subject as referred to in paragraph 2 [GDPR-Art14-2, GDPR-Art14-4].

Judge: 5/5. All listed information items are directly stated in the cited GDPR articles.

### q054 (fr, obligation)

**Question:** Dans quels cas précis une entreprise de moins de 250 employés est-elle tout de même tenue de tenir un registre des activités de traitement ?

**Answer** (gemini-3.5-flash-lite):

> Une entreprise ou une organisation comptant moins de 250 employés est tout de même tenue de tenir un registre des activités de traitement si le traitement qu'elle effectue remplit l'une des conditions suivantes :
> - il est susceptible de comporter un risque pour les droits et libertés des personnes concernées [GDPR-Art30-5] ;
> - il n'est pas occasionnel [GDPR-Art30-5] ;
> - il porte notamment sur les catégories particulières de données visées à l'article 9, paragraphe 1, ou sur des données à caractère personnel relatives à des condamnations pénales et à des infractions visées à l'article 10 [GDPR-Art30-5].

Judge: 5/5. All claims are directly supported by GDPR Article 30(5) source.

### q055 (fr, lookup)

**Question:** Dans quelles situations précises une autorité de surveillance du marché doit-elle inviter un fournisseur à mettre un terme à une non-conformité formelle?

**Answer** (gemini-3.5-flash-lite):

> Une autorité de surveillance du marché d'un État membre invite un fournisseur concerné à mettre un terme à une non-conformité formelle lorsqu'elle fait l'une des constatations suivantes:
> - le marquage CE a été apposé en violation de l'article 48 [AIA-Art83-1];
> - le marquage CE n'a pas été apposé [AIA-Art83-1];
> - la déclaration UE de conformité visée à l'article 47 n'a pas été établie [AIA-Art83-1];
> - la déclaration UE de conformité visée à l'article 47 n'a pas été établie correctement [AIA-Art83-1];
> - l'enregistrement dans la base de données de l'UE visée à l'article 71 n'a pas été effectué [AIA-Art83-1];
> - le cas échéant, il n'a pas été désigné de mandataire [AIA-Art83-1];
> - la documentation technique n'est pas disponible [AIA-Art83-1].

Judge: 5/5. All listed situations are directly stated in source AIA-Art83-1 and correctly cited.

### q056 (en, lookup)

**Question:** To what obligations may adherence to the codes of practice be limited for providers of general-purpose AI models that do not present systemic risks?

**Answer** (gemini-3.5-flash-lite):

> For providers of general-purpose AI models not presenting systemic risks, adherence to the codes of practice may be limited to the obligations provided for in Article 53, unless they declare explicitly their interest to join the full code [AIA-Art56-7].

Judge: 5/5. The answer's claim is directly supported by the cited source.

### q057 (en, lookup)

**Question:** By what date must Member States identify and publish the list of public authorities or bodies that protect fundamental rights in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> By 2 November 2024, each Member State shall identify the public authorities or bodies referred to in paragraph 1 and make a list of them publicly available [AIA-Art77-2].

Judge: 5/5. The answer directly reflects the statement in source AIA-Art77-2.

### q058 (en, obligation)

**Question:** Under what specific conditions may a data transfer to a third country take place when no other provisions or derogations apply?

**Answer** (gemini-3.5-flash-lite):

> Where a transfer could not be based on a provision in Article 45 or 46 (including binding corporate rules) and none of the derogations for a specific situation referred to in the first subparagraph of GDPR Article 49(1) are applicable, a transfer to a third country or an international organisation may take place only if all of the following conditions are met:
> - The transfer is not repetitive [GDPR-Art49-1].
> - The transfer concerns only a limited number of data subjects [GDPR-Art49-1].
> - The transfer is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject [GDPR-Art49-1].
> - The controller has assessed all the circumstances surrounding the data transfer and has, on the basis of that assessment, provided suitable safeguards with regard to the data [GDPR-Art49-1].

Judge: 5/5. All claims in the answer are directly supported by GDPR Article 49(1) source.

### q059 (fr, obligation)

**Question:** Est-ce qu'une organisation de protection des données peut introduire une réclamation auprès d'une autorité de contrôle sans avoir reçu de mandat de la personne concernée ?

**Answer** (gemini-3.5-flash-lite):

> Oui, les États membres peuvent prévoir que tout organisme, organisation ou association (visé au paragraphe 1 de l'article 80 du RGPD) a le droit d'introduire une réclamation auprès de l'autorité de contrôle compétente sans qu'un tel mandat ne lui ait été confié par la personne concernée, s'il considère que les droits de cette dernière ont été violés du fait du traitement [GDPR-Art80-2].

Judge: 5/5. The answer's claim is fully supported by GDPR Article 80(2).

### q060 (en, lookup)

**Question:** Within what timeframe must a supervisory authority inform a data subject about the progress or outcome of their lodged complaint to avoid the data subject having a right to an effective judicial remedy?

**Answer** (gemini-3.5-flash-lite):

> A supervisory authority must inform the data subject about the progress or outcome of the complaint within three months [GDPR-Art78-2].

Judge: 5/5. The answer correctly states the three‑month deadline as required by GDPR Art 78(2).

### q061 (fr, obligation)

**Question:** Quelles informations l'autorité notifiante doit-elle fournir à la Commission concernant les organismes notifiés, et à quel moment ?

**Answer** (gemini-3.5-flash-lite):

> L'autorité notifiante fournit à la Commission, sur demande, toutes les informations utiles relatives à la notification ou au maintien de la compétence de l’organisme notifié concerné [AIA-Art37-2].

Judge: 5/5. The answer exactly matches the statement in the cited source.

### q062 (fr, obligation)

**Question:** Quelles sont les obligations de l'autorité notifiante en cas de restriction, de suspension ou de retrait d'une désignation d'organisme notifié ?

**Answer** (gemini-3.5-flash-lite):

> En cas de restriction, de suspension ou de retrait d’une désignation d’organisme notifié, l'autorité notifiante doit prendre les mesures nécessaires pour que les dossiers de l'organisme notifié en question soient conservés et mis à la disposition des autorités notifiantes d’autres États membres et des autorités de surveillance du marché, à leur demande [AIA-Art36-6].
>
> De plus, elle est tenue de [AIA-Art36-7]:
> - Évaluer l’incidence sur les certificats délivrés par l’organisme notifié [AIA-Art36-7].
> - Transmettre un rapport sur ses conclusions à la Commission et aux autres États membres dans un délai de trois mois après avoir signalé les modifications apportées à la désignation [AIA-Art36-7].
> - Exiger de l’organisme notifié qu’il suspende ou retire, dans un délai raisonnable qu’elle détermine, tous les certificats délivrés à tort afin d’assurer la conformité constante des systèmes d’IA à haut risque sur le marché [AIA-Art36-7].
> - Informer la Commission et les États membres des certificats dont elle a demandé la suspension ou le retrait [AIA-Art36-7].
> - Fournir aux autorités nationales compétentes de l’État membre dans lequel le fournisseur a son siège social toutes les informations pertinentes sur les certificats dont elle a demandé la suspension ou le retrait, cette autorité prenant les mesures appropriées si cela est nécessaire [AIA-Art36-7].

Judge: 5/5. All statements in the answer are directly supported by the cited sources.

### q063 (fr, lookup)

**Question:** Dans quelle situation le règlement s'applique-t-il au traitement de données par un responsable du traitement non établi dans l'Union, mais dans un lieu régi par le droit d'un État membre en vertu du droit international public ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement s'applique au traitement de données à caractère personnel par un responsable du traitement qui n'est pas établi dans l'Union mais dans un lieu où le droit d'un État membre s'applique en vertu du droit international public [GDPR-Art3-3].

Judge: 5/5. All claims are directly supported by the cited source.

### q064 (en, obligation)

**Question:** How can public authorities reconcile public access to official documents with the right to the protection of personal data?

**Answer** (gemini-3.5-flash-lite):

> Personal data in official documents held by a public authority, a public body, or a private body for the performance of a task carried out in the public interest may be disclosed in accordance with Union or Member State law to which the authority or body is subject, in order to reconcile public access to official documents with the right to the protection of personal data [GDPR-Art86].

Judge: 5/5. The answer's claim is directly stated in GDPR Article 86.

### q065 (fr, obligation)

**Question:** Quels documents les organismes notifiés doivent-ils fournir à l'autorité notifiante pour faciliter ses activités de surveillance et d'évaluation ?

**Answer** (gemini-3.5-flash-lite):

> Les organismes notifiés mettent à la disposition de l’autorité notifiante et lui soumettent sur demande toute la documentation pertinente, y compris celle des fournisseurs, afin de lui permettre de réaliser ses activités d’évaluation, de désignation, de notification et de surveillance et pour faciliter les évaluations décrites à la présente section [AIA-Art34-3].

Judge: 5/5. The answer directly reflects the content of source AIA-Art34-3.

### q066 (fr, lookup)

**Question:** Quel organe européen peut adopter des actes d'exécution pour définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle et le comité?

**Answer** (gemini-3.5-flash-lite):

> La Commission peut adopter des actes d'exécution afin de définir les modalités de l'échange d'informations par voie électronique entre les autorités de contrôle, et entre ces autorités et le comité [GDPR-Art67, GDPR-Art61-9].

Judge: 5/5. All claims are directly supported by the cited sources.

### q067 (en, obligation)

**Question:** Who is liable to pay compensation to a person who has suffered material or non-material damage due to an infringement of the regulation?

**Answer** (gemini-3.5-flash-lite):

> Any person who has suffered material or non-material damage as a result of an infringement of the regulation has the right to receive compensation from the controller or processor for the damage suffered [GDPR-Art82-1].

Judge: 5/5. All claims are directly supported by the cited source

### q068 (en, lookup)

**Question:** How does the Commission ensure appropriate coordination and cooperation between notified bodies involved in conformity assessment procedures for high-risk AI systems?

**Answer** (gemini-3.5-flash-lite):

> The Commission shall ensure that appropriate coordination and cooperation between notified bodies active in conformity assessment procedures for high-risk AI systems are put in place and properly operated in the form of a sectoral group of notified bodies [AIA-Art38-1].

Judge: 5/5. The answer's claim is directly stated in the cited source.

### q069 (en, obligation)

**Question:** Under what conditions can Union or Member State law restrict data protection rights and obligations?

**Answer** (gemini-3.5-flash-lite):

> Union or Member State law may restrict the scope of data protection rights and obligations (specifically those provided for in Articles 12 to 22, Article 34, and Article 5 where its provisions correspond to Articles 12 to 22) through a legislative measure, provided that the restriction respects the essence of the fundamental rights and freedoms and constitutes a necessary and proportionate measure in a democratic society to safeguard specific objectives [GDPR-Art23-1].
>
> These objectives include:
> - national security [GDPR-Art23-1];
> - defence [GDPR-Art23-1];
> - public security [GDPR-Art23-1];
> - the prevention, investigation, detection, or prosecution of criminal offences or the execution of criminal penalties, including safeguarding against and preventing threats to public security [GDPR-Art23-1];
> - other important objectives of general public interest of the Union or of a Member State, such as important economic or financial interests (including monetary, budgetary, and taxation matters), public health, and social security [GDPR-Art23-1];
> - the protection of judicial independence and judicial proceedings [GDPR-Art23-1];
> - the prevention, investigation, detection, and prosecution of breaches of ethics for regulated professions [GDPR-Art23-1];
> - monitoring, inspection, or regulatory functions connected, even occasionally, to the exercise of official authority in cases referred to in points (a) to (e) and (g) [GDPR-Art23-1];
> - the protection of the data subject or the rights and freedoms of others [GDPR-Art23-1];
> - the enforcement of civil law claims [GDPR-Art23-1].

Judge: 5/5. All statements in the answer are directly supported by the cited GDPR Article 23(1) sources.

### q070 (fr, lookup)

**Question:** Où sont enregistrés les systèmes d'IA à haut risque utilisés dans les domaines de la migration et de l'asile, et qui a accès à ces informations ?

**Answer** (gemini-3.5-flash-lite):

> Pour les systèmes d'IA à haut risque visés à l'annexe III, points 1, 6 et 7, dans les domaines des activités répressives, de la migration, de l'asile et de la gestion des contrôles aux frontières, l'enregistrement figure dans une section sécurisée non publique de la base de données de l'UE visée à l'article 71 [AIA-Art49-4].
>
> Seules la Commission et les autorités nationales visées à l'article 74, paragraphe 8, ont accès aux différentes sections restreintes de cette base de données [AIA-Art49-4].

Judge: 5/5. All statements in the answer are directly supported by the cited source AIA-Art49-4.

### q071 (fr, lookup)

**Question:** Quelle est la durée de validité maximale des mesures provisoires qu'une autorité de contrôle peut adopter d'urgence pour protéger les droits des personnes ?

**Answer** (gemini-3.5-flash-lite):

> La durée de validité des mesures provisoires adoptées d'urgence par une autorité de contrôle ne peut excéder trois mois [GDPR-Art66-1].

Judge: 5/5. The answer's claim about the maximum three‑month validity is directly stated in GDPR Art 66(1).

### q072 (en, obligation)

**Question:** At what point and with whom must Member States consult regarding legislative or regulatory measures related to data processing?

**Answer** (gemini-3.5-flash-lite):

> Member States shall consult the supervisory authority during the preparation of a proposal for a legislative measure to be adopted by a national parliament, or of a regulatory measure based on such a legislative measure, which relates to processing [GDPR-Art36-4].

Judge: 5/5. The answer exactly matches the statement in GDPR Article 36(4).

### q073 (fr, lookup)

**Question:** Dans quelles circonstances l'interdiction générale de prendre des décisions individuelles automatisées ne s'applique-t-elle pas selon le règlement ?

**Answer** (refused (not_covered)):

> Je ne peux pas répondre à partir du texte du règlement sur l'IA ou du RGPD dont je dispose. Reformulez la question, ou consultez un juriste.

### q074 (en, lookup)

**Question:** What specific information must be included in the record of processing activities maintained by a controller?

**Answer** (gemini-3.5-flash-lite):

> The record of processing activities maintained by a controller must contain all of the following information:
> (a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representative and the data protection officer [GDPR-Art30-1].
> (b) the purposes of the processing [GDPR-Art30-1].
> (c) a description of the categories of data subjects and of the categories of personal data [GDPR-Art30-1].
> (d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations [GDPR-Art30-1].
> (e) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards [GDPR-Art30-1].
> (f) where possible, the envisaged time limits for erasure [GDPR-Art30-1].

Judge: 5/5. All listed items are directly stated in GDPR Article 30(1) as cited.

### q075 (fr, obligation)

**Question:** Que doit faire l'autorité de surveillance du marché si une non-conformité formelle persiste malgré les mesures initiales ?

**Answer** (gemini-3.5-flash-lite):

> Si le cas de non-conformité formelle persiste, l’autorité de surveillance du marché de l’État membre concerné prend toutes les mesures appropriées et proportionnées pour restreindre ou interdire la mise à disposition du système d’IA à haut risque sur le marché ou pour assurer son rappel ou son retrait sans tarder du marché [AIA-Art83-2].
>
> *Ceci constitue une information juridique et non un avis juridique.*

Judge: 5/5. The answer's claim is fully supported by the cited source AIA-Art83-2.

### q076 (fr, lookup)

**Question:** Quel organisme facilite la révision des codes de bonne pratique et évalue les normes disponibles ?

**Answer** (gemini-3.5-flash-lite):

> Le Bureau de l’IA encourage et facilite le réexamen et l’adaptation des codes de bonne pratique, et il participe à l’évaluation des normes disponibles [AIA-Art56-8].

Judge: 5/5. All claims are directly stated in the cited source.

### q077 (en, obligation)

**Question:** What can a public authority protecting fundamental rights do if the available documentation is not enough to determine if a high-risk AI system infringes Union law?

**Answer** (gemini-3.5-flash-lite):

> Where the available documentation is insufficient to ascertain whether an infringement of obligations under Union law protecting fundamental rights has occurred, the public authority or body may make a reasoned request to the market surveillance authority to organise testing of the high-risk AI system through technical means [AIA-Art77-3]. Upon such a request, the market surveillance authority shall organise the testing with the close involvement of the requesting public authority or body within a reasonable time [AIA-Art77-3].

Judge: 5/5. All statements are directly supported by Article 77(3) of the AI Act.

### q078 (en, obligation)

**Question:** What action must Member States take regarding national provisions that set limits on personal data transfers to third countries for important reasons of public interest in the absence of an adequacy decision?

**Answer** (gemini-3.5-flash-lite):

> Member States shall notify such provisions to the Commission [GDPR-Art49-5].

Judge: 5/5. The answer directly reflects the statement in GDPR-Art49-5.

### q079 (en, lookup)

**Question:** In which courts can a data subject bring judicial proceedings against a controller or processor?

**Answer** (gemini-3.5-flash-lite):

> Proceedings against a controller or a processor shall be brought before the courts of the Member State where the controller or processor has an establishment [GDPR-Art79-2]. Alternatively, such proceedings may be brought before the courts of the Member State where the data subject has his or her habitual residence, unless the controller or processor is a public authority of a Member State acting in the exercise of its public powers [GDPR-Art79-2].

Judge: 5/5. All statements are directly supported by GDPR Article 79(2).

### q080 (en, lookup)

**Question:** What kind of bodies or organisations can a data subject mandate to lodge a complaint or exercise data protection rights on their behalf?

**Answer** (gemini-3.5-flash-lite):

> A data subject can mandate a not-for-profit body, organisation, or association which has been properly constituted in accordance with the law of a Member State, has statutory objectives in the public interest, and is active in the field of the protection of data subjects' rights and freedoms with regard to the protection of their personal data [GDPR-Art80-1].

Judge: 5/5. All statements in the answer are directly supported by GDPR Article 80(1).

### q081 (en, obligation)

**Question:** What must a supervisory authority do when proceedings are brought against its decision that was preceded by an opinion or decision of the Board in the consistency mechanism?

**Answer** (gemini-3.5-flash-lite):

> Where proceedings are brought against a decision of a supervisory authority which was preceded by an opinion or a decision of the Board in the consistency mechanism, the supervisory authority shall forward that opinion or decision to the court [GDPR-Art78-4].

Judge: 5/5. The answer directly matches the wording of the cited source.

### q082 (en, lookup)

**Question:** What are the specific tasks of the scientific panel of independent experts regarding cross-border market surveillance activities and the Union safeguard procedure?

**Answer** (gemini-3.5-flash-lite):

> Based on the provided sources, the specific tasks of the scientific panel of independent experts regarding cross-border market surveillance activities and the Union safeguard procedure are:
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

> L'autorité notifiante notifie à la Commission et aux autres États membres toute modification pertinente apportée à la notification d'un organisme notifié au moyen de l'outil de notification électronique visé à l'article 30, paragraphe 2 [AIA-Art36-1].

Judge: 5/5. The answer is fully supported by the cited source.

### q085 (fr, lookup)

**Question:** Dans quelles conditions le règlement s'applique-t-il au traitement des données effectué par un établissement d'un responsable du traitement, indépendamment du lieu où se déroule le traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le règlement s'applique au traitement des données à caractère personnel effectué dans le cadre des activités d'un établissement d'un responsable du traitement sur le territoire de l'Union, que le traitement ait lieu ou non dans l'Union [GDPR-Art3-1].

Judge: 5/5. All claims are directly supported by the cited source.

### q086 (fr, obligation)

**Question:** De quelle manière les organismes notifiés doivent-ils tenir compte de la taille des fournisseurs et de la complexité des systèmes d'IA dans leurs activités ?

**Answer** (gemini-3.5-flash-lite):

> Les organismes notifiés doivent tenir compte de la taille du fournisseur, du secteur dans lequel il exerce, de sa structure et du degré de complexité du système d'IA à haut risque concerné afin d'éviter les charges inutiles, en particulier pour réduire au minimum les charges administratives et les coûts de mise en conformité pour les microentreprises et les petites entreprises [AIA-Art34-2]. De plus, ils doivent respecter le degré de rigueur et le niveau de protection requis pour garantir la conformité du système d'IA à haut risque avec les exigences du règlement [AIA-Art34-2]. Pour ce faire, ils disposent de procédures spécifiques pour accomplir leurs activités qui tiennent dûment compte de ces éléments (taille des fournisseurs, secteur, structure et degré de complexité) [AIA-Art31-8].

Judge: 5/5. All statements in the answer are directly supported by the cited sources.

### q087 (en, lookup)

**Question:** What right does a controller or processor have after paying full compensation for damage caused by processing?

**Answer** (gemini-3.5-flash-lite):

> Where a controller or processor has paid full compensation for the damage suffered, that controller or processor is entitled to claim back from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage, in accordance with the conditions set out in paragraph 2 [GDPR-Art82-5].

Judge: 5/5. The answer exactly reflects the content of GDPR Article 82(5) and is fully supported.

### q088 (en, obligation)

**Question:** How must notified bodies be involved in the sectoral group that the Commission sets up for them?

**Answer** (gemini-3.5-flash-lite):

> Notified bodies must participate in the sectoral group (coordination activities referred to in Article 38), either directly or through designated representatives [AIA-Art38-2, AIA-Art31-12].

Judge: 5/5. All statements are directly supported by the cited articles.

### q089 (fr, lookup)

**Question:** Quels éléments spécifiques les mesures législatives limitant la portée des obligations et des droits du RGPD doivent-elles contenir au minimum ?

**Answer** (gemini-3.5-flash-lite):

> En particulier, toute mesure législative limitant la portée des obligations et des droits du RGPD doit contenir des dispositions spécifiques relatives au moins, le cas échéant, aux éléments suivants :
> a) aux finalités du traitement ou des catégories de traitement [GDPR-Art23-2];
> b) aux catégories de données à caractère personnel [GDPR-Art23-2];
> c) à l'étendue des limitations introduites [GDPR-Art23-2];
> d) aux garanties destinées à prévenir les abus ou l'accès ou le transfert illicites [GDPR-Art23-2];
> e) à la détermination du responsable du traitement ou des catégories de responsables du traitement [GDPR-Art23-2];
> f) aux durées de conservation et aux garanties applicables, en tenant compte de la nature, de la portée et des finalités du traitement ou des catégories de traitement [GDPR-Art23-2];
> g) aux risques pour les droits et libertés des personnes concernées [GDPR-Art23-2];
> h) au droit des personnes concernées d'être informées de la limitation, à moins que cela risque de nuire à la finalité de la limitation [GDPR-Art23-2].

Judge: 5/5. All listed elements are directly stated in GDPR Article 23(2) source.

### q090 (en, obligation)

**Question:** Who is required to register a non-high-risk AI system in the EU database before it is placed on the market or put into service?

**Answer** (gemini-3.5-flash-lite):

> Before an AI system for which the provider has concluded that it is not high-risk is placed on the market or put into service, the provider or, where applicable, the authorised representative shall register themselves and that system in the EU database [AIA-Art49-2].

Judge: 5/5. The answer directly reflects the statement in source AIA-Art49-2.

### q091 (fr, lookup)

**Question:** Dans quel délai et à quelle majorité le comité doit-il adopter un avis ou une décision contraignante dans le cadre de la procédure d'urgence ?

**Answer** (gemini-3.5-flash-lite):

> Dans le cadre de la procédure d'urgence, l'avis d'urgence ou la décision contraignante d'urgence est adopté dans un délai de deux semaines à la majorité simple des membres du comité [GDPR-Art66-4].

Judge: 5/5. The answer's claim matches the source exactly.

### q092 (fr, obligation)

**Question:** Dans quelle situation précise le responsable du traitement est-il tenu de consulter l'autorité de contrôle avant de procéder au traitement ?

**Answer** (gemini-3.5-flash-lite):

> Le responsable du traitement consulte l'autorité de contrôle préalablement au traitement lorsqu'une analyse d'impact relative à la protection des données effectuée au titre de l'article 35 indique que le traitement présenterait un risque élevé si le responsable du traitement ne prenait pas de mesures pour atténuer le risque [GDPR-Art36-1].

Judge: 5/5. The answer exactly matches the statement in GDPR-Art36-1 and is fully supported.

### q093 (en, obligation)

**Question:** How should the development of benchmarks and measurement methodologies for AI systems be encouraged, and who is involved in this process?

**Answer** (gemini-3.5-flash-lite):

> To address the technical aspects of how to measure appropriate levels of accuracy, robustness, and any other relevant performance metrics for AI systems, the Commission shall encourage the development of benchmarks and measurement methodologies [AIA-Art15-2]. This process is done in cooperation with relevant stakeholders and organizations, such as metrology and benchmarking authorities [AIA-Art15-2].

Judge: 5/5. All claims are directly supported by the cited source.

### q094 (en, lookup)

**Question:** What right does a data subject have regarding decisions based solely on automated processing, including profiling?

**Answer** (gemini-3.5-flash-lite):

> The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her [GDPR-Art22-1].

Judge: 5/5. The answer exactly matches the statement in GDPR Article 22(1) and is fully supported.

### q095 (en, lookup)

**Question:** What additional information must a controller provide to a data subject when personal data have not been obtained directly from them, in order to ensure fair and transparent processing?

**Answer** (gemini-3.5-flash-lite):

> When personal data have not been obtained from the data subject, the controller shall provide the data subject with the following additional information necessary to ensure fair and transparent processing: (a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period; (b) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party; (c) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject and to object to processing as well as the right to data portability; and (d) where processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any [GDPR-Art14-2].

Judge: 5/5. All claims in the answer are directly supported by GDPR Article 14(2) as provided in the source.

### q096 (en, obligation)

**Question:** Who must make the record of processing activities available to the supervisory authority upon request?

**Answer** (gemini-3.5-flash-lite):

> The controller or the processor and, where applicable, the controller's or the processor's representative, shall make the record available to the supervisory authority on request [GDPR-Art30-4].

Judge: 5/5. The answer exactly matches the statement in GDPR Article 30(4).

### q097 (en, obligation)

**Question:** How must national public authorities handle information and documentation they obtain regarding fundamental rights protection in relation to AI systems?

**Answer** (gemini-3.5-flash-lite):

> Any information or documentation obtained by national public authorities or bodies protecting fundamental rights pursuant to Article 77 shall be treated in accordance with the confidentiality obligations set out in Article 78 [AIA-Art77-4].

Judge: 5/5. The answer's claim is directly stated in the cited source.

### q098 (en, lookup)

**Question:** What conditions allow for the transfer of personal data to a third country when there is neither an adequacy decision nor appropriate safeguards in place?

**Answer** (gemini-3.5-flash-lite):

> When there is neither an adequacy decision nor appropriate safeguards in place, a transfer or a set of transfers of personal data to a third country or an international organisation may take place only on one of the following conditions:
> (a) the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards;
> (b) the transfer is necessary for the performance of a contract between the data subject and the controller or the implementation of pre-contractual measures taken at the data subject's request;
> (c) the transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person [GDPR-Art49-1].

Judge: 3/5. Answer omits other conditions (e.g., condition d) listed in the source, making it incomplete

### q099 (fr, obligation)

**Question:** Quels recours une personne physique ou morale possède-t-elle face à une décision juridiquement contraignante d'une autorité de contrôle qui la concerne ?

**Answer** (gemini-3.5-flash-lite):

> Sans préjudice de tout autre recours administratif ou extrajudiciaire, toute personne physique ou morale a le droit de former un recours juridictionnel effectif contre une décision juridiquement contraignante d'une autorité de contrôle qui la concerne [GDPR-Art78-1].

Judge: 5/5. The answer's claim is directly stated in the cited source GDPR-Art78-1.

### q100 (en, lookup)

**Question:** What aspects regarding the scientific panel and its members must be included in the implementing act?

**Answer** (gemini-3.5-flash-lite):

> The implementing act shall include provisions on the conditions, procedures, and detailed arrangements for the scientific panel and its members to issue alerts, and to request the assistance of the AI Office for the performance of the tasks of the scientific panel [AIA-Art68-5].

Judge: 5/5. The answer directly reflects the content of source AIA-Art68-5 with no unsupported claims.

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
