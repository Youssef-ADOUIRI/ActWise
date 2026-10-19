"""Small EN and FR extracts that mimic the real EUR-Lex text layout."""

EN_SAMPLE = """\
Whereas:
(1)
The purpose of this Regulation is to improve the functioning of the internal market.
(2)
AI systems can be easily deployed
in a large variety of sectors.
HAVE ADOPTED THIS REGULATION:
CHAPTER I
GENERAL PROVISIONS
Article 1
Subject matter
1.   The purpose of this Regulation is to promote human-centric AI.
2.   This Regulation lays down:
(a) harmonised rules for AI systems;
(b) prohibitions of certain practices.
Article 3
Definitions
For the purposes of this Regulation, the following definitions apply:
(1) 'AI system' means a machine-based system that infers outputs;
(2) 'risk' means the combination of the probability of harm and its severity;
CHAPTER II
PROHIBITED AI PRACTICES
Article 5
Prohibited AI practices
1. The following AI practices shall be prohibited:
(a) the placing on the market of an AI system that deploys subliminal techniques;
(b) social scoring of natural persons.
ANNEX III
High-risk AI systems referred to in Article 6(2)
1. Biometrics, in so far as their use is permitted:
(a) remote biometric identification systems.
4. Employment, workers' management:
(a) AI systems intended to be used for the recruitment or selection of natural persons.
"""

# Real French layout: "ONT ADOPTÉ", "Article premier", "1)" definitions, "a)" points.
FR_SAMPLE = """\
considérant ce qui suit:
(1)
L'objectif du présent règlement est d'améliorer le fonctionnement du marché intérieur.
(2)
Les systèmes d'IA peuvent être facilement déployés
dans une grande variété de secteurs.
ONT ADOPTÉ LE PRÉSENT RÈGLEMENT:
CHAPITRE I
DISPOSITIONS GÉNÉRALES
Article premier
Objet
1.   L'objectif du présent règlement est de promouvoir une IA axée sur l'humain.
2.   Le présent règlement établit:
a)
des règles harmonisées pour les systèmes d'IA;
b)
l'interdiction de certaines pratiques.
Article 3
Définitions
Aux fins du présent règlement, on entend par:
1)
«système d'IA», un système automatisé qui déduit des sorties;
2)
«risque», la combinaison de la probabilité d'un préjudice et de sa gravité;
CHAPITRE II
PRATIQUES INTERDITES EN MATIÈRE D'IA
Article 5
Pratiques interdites en matière d'IA
1. Les pratiques en matière d'IA suivantes sont interdites:
a) la mise sur le marché d'un système d'IA qui a recours à des techniques subliminales;
b) la notation sociale des personnes physiques.
ANNEXE III
Systèmes d'IA à haut risque visés à l'article 6, paragraphe 2
1. Biométrie, dans la mesure où leur utilisation est autorisée:
a) systèmes d'identification biométrique à distance.
4. Emploi, gestion de la main-d'œuvre:
a) systèmes d'IA destinés à être utilisés pour le recrutement de personnes physiques.
"""

EXPECTED_IDS = [
    "AIA-Rec1",
    "AIA-Rec2",
    "AIA-Art1-1",
    "AIA-Art1-2",
    "AIA-Art3-0",
    "AIA-Art3-1",
    "AIA-Art3-2",
    "AIA-Art5-1",
    "AIA-AnnexIII-1",
    "AIA-AnnexIII-4",
]
