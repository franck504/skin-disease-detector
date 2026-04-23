# ANNEXE : TABLEAUX ET RÉFÉRENCES DU MÉMOIRE CUTISIA

Ce document contient le contenu textuel des tableaux identifiés dans le plan de rédaction, ainsi que les références bibliographiques vérifiées.

---

## I. TABLEAUX DU MÉMOIRE

### TABLEAU 1 : Comparaison des approches de diagnostic dermatologique
*Emplacement : Chapitre 1*

| Critère | Diagnostic Clinique (Visuel) | Teledermatologie | Cutisia (IA Mobile) |
| :--- | :--- | :--- | :--- |
| **Accessibilité** | Faible (déplacement requis) | Moyenne (besoin d'expert) | Très élevée (Smartphone) |
| **Coût** | Élevé (consultation) | Moyen | Très faible |
| **Délai** | Long (rendez-vous) | 24h - 48h | Instantané (< 2s) |
| **Précision** | Dépend de l'expérience | Élevée (expert distant) | Élevée (Elite Model) |

### TABLEAU 2 : Résumé des obligations de l'AI Act pour Cutisia
*Emplacement : Chapitre 3*

| Exigence AI Act | Mise en œuvre Cutisia |
| :--- | :--- |
| **Transparence** | Utilisation de Grad-CAM pour expliquer le diagnostic. |
| **Qualité des données** | Utilisation de datasets certifiés (HAM10000, ISIC). |
| **Supervision humaine** | L'application indique qu'il s'agit d'une aide, pas d'un diagnostic final. |
| **Sécurité** | Anonymisation des données patients avant envoi Cloud. |

### TABLEAU 3 : Forces et Faiblesses du système Cutisia
*Emplacement : Chapitre 8*

| Forces | Faiblesses |
| :--- | :--- |
| Vitesse d'exécution locale (TFLite). | Sensibilité à la qualité de l'éclairage. |
| Interface intuitive en Malgache. | Dépendance au réseau pour le mode "Elite". |
| Haute précision sur les 6 classes cibles. | Risque de faux positifs sur les peaux très sombres. |

---

## II. RÉFÉRENCES BIBLIOGRAPHIQUES VÉRIFIÉES

**[1] Organisation Mondiale de la Santé (OMS)**
*   *Titre :* "Skin health for all: update on skin neglected tropical diseases".
*   *Lien :* [https://www.who.int/publications/i/item/who-wer10024-25-239-250](https://www.who.int/publications/i/item/who-wer10024-25-239-250)
*   *Note :* Justifie l’importance des maladies de peau comme problème majeur de santé publique.

**[2] Neurocomputing (2021)**
*   *Article :* "Skin disease diagnosis with deep learning: A review".
*   *Lien :* [https://www.sciencedirect.com/science/article/pii/S0925231221012935](https://www.sciencedirect.com/science/article/pii/S0925231221012935)
*   *Note :* Présente les méthodes de deep learning pour le diagnostic dermatologique.

**[3] Goodfellow, I., Bengio, Y., & Courville, A. (2016)**
*   *Livre :* "Deep Learning". MIT Press.
*   *Chapitre 9 :* Convolutional Networks (Pages 326-366).
*   *Lien :* [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/) 

**[4] Esteva, A., et al. (2017)**
*   *Article :* "Dermatologist-level classification of skin cancer with deep neural networks". Nature.
*   *URL :* [https://www.nature.com/articles/nature21056](https://www.nature.com/articles/nature21056)
*   *Note :* La référence de base pour l'utilisation des CNN en dermatologie.

**[5] Howard, A., et al. (2019)**
*   *Article :* "Searching for MobileNetV3" (Applicable à votre MobileNetV2).
*   *Lien :* [https://arxiv.org/abs/1905.02244](https://arxiv.org/abs/1905.02244)

**[6] Règlement (UE) 2024/1689 (AI Act)**
*   *Lien :* [https://eur-lex.europa.eu/eli/reg/2024/1689/oj](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
*   *Note :* Pour le Chapitre 3 sur l'éthique.
