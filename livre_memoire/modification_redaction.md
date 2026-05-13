# Modifications à apporter à `redaction.md`

> Ce document décrit les 10 modifications à appliquer manuellement dans `redaction.md`.
> Chaque modification indique : la ligne concernée, le texte actuel, le texte de remplacement, et les éventuels effets sur le reste du document.

---

## Modification 1 — Préciser EfficientNetV2-L (Section 5.1.2, ligne 232-234)

**Texte actuel (ligne 232-234) :**
> #### 5.1.2 Choix des architectures (MobileNetV2, EfficientNet) et Transfer Learning
>
> Nous avons porté notre choix sur l'architecture **MobileNetV2**. Cette architecture permet à l'IA de reconnaître des motifs complexes (textures, couleurs, bords) [3]. Le Transfer Learning, ou apprentissage par transfert, consiste à utiliser un modèle déjà entraîné sur des millions d'images générales et à l'adapter à la dermatologie [4]. Cela permet d'obtenir une grande précision même avec un dataset médical réduit.

**Remplacer par :**
> #### 5.1.2 Choix des architectures (MobileNetV2, EfficientNetV2-L) et Transfer Learning
>
Pour le diagnostic sur mobile, nous utilisons MobileNetV2, une architecture légère qui exploite les **Convolutions Séparables en Profondeur** (Depthwise Separable Convolutions), réduisant le nombre de calculs par un facteur 8 tout en maintenant une haute précision [3]. Pour le mode Cloud (Elite), nous avons choisi **EfficientNetV2-L** (Large), une architecture plus puissante (~118 millions de paramètres) qui équilibre intelligemment la profondeur, la largeur et la résolution du réseau grâce au principe de **Compound Scaling** [4]. Les deux modèles sont chargés avec des poids pré-entraînés sur **ImageNet** (1,4 million d'images), puis spécialisés sur notre dataset dermatologique par Transfer Learning.

**⚠️ Effet sur le reste :**
- Le titre de la sous-section change : "EfficientNet" → "EfficientNetV2-L". Vérifier que les autres mentions de "EfficientNet" dans le document (lignes 109, 275) restent cohérentes. La ligne 109 dit "EfficientNet" de manière générale dans l'état de l'art, c'est OK de le garder tel quel. La ligne 275 dit "classification MobileNet", c'est OK aussi car elle parle du mode local.

---

## Modification 2 — Ajouter le processus en 2 phases (Section 5.2.1, après ligne 240)

**Texte actuel (ligne 238-240) :**
> Pendant l'entraînement, nous surveillons deux courbes : la **Loss** (l'erreur) et l'**Accuracy** (la précision). Notre but est de faire descendre l'erreur le plus bas possible tout en évitant le sur-apprentissage (overfitting). Nous ajustons des curseurs appelés "hyperparamètres" (comme le taux d'apprentissage) pour guider l'IA vers la meilleure solution.

**Remplacer par :**
Pendant l'entraînement, nous surveillons deux courbes : la Loss (l'erreur, mesurée par la fonction `categorical_crossentropy`) et l'Accuracy (la précision). Le suivi est effectué en temps réel via la plateforme Weights & Biases (wandb), permettant un monitoring à distance. L'optimiseur utilisé est Adam (adaptatif), et les labels sont encodés en One-Hot Encoding (ex : Leprosy = [0,1,0,0,0,0]).

L'entraînement se déroule en deux phases distinctes :
- Phase 1 - Warm-up (5 epochs) : Les couches pré-entraînées d'EfficientNetV2-L sont entièrement gelées. Seules les couches de tête ajoutées (GlobalAveragePooling2D → Dense(512) → Dropout(0.4) → Softmax(6)) sont entraînées, avec un learning rate de 1e-4.
- Phase 2 — Fine-Tuning (jusqu'à 50 epochs) : Les 50 dernières couches de la base sont dégelées progressivement. Le learning rate est réduit à 1e-5 pour éviter de dégrader les poids pré-entraînés.
Trois callbacks automatiques protègent ce processus : EarlyStopping (arrêt si pas d'amélioration pendant 8 epochs), ReduceLROnPlateau (réduction automatique du learning rate en cas de stagnation), et ModelCheckpoint (sauvegarde du meilleur modèle sur Google Drive). Les images sont redimensionnées à 384×384 pixels et traitées par lots de 8 images (batch size réduit pour éviter les erreurs de mémoire GPU).

**⚠️ Effet sur le reste :**
- Ce paragraphe devient plus long (environ +10 lignes). Cela peut décaler les numéros de lignes de toutes les sections qui suivent.
- La section 5.2.2 (Quantification/TFLite) qui suit immédiatement reste parfaitement cohérente, aucun ajustement nécessaire.

---

## Modification 3 — Ajouter CLAHE (Section 4.3.1, ligne 206-208)

**Texte actuel (ligne 206-208) :**
> La lumière varie d'une photo à l'autre. Nous normalisons donc les couleurs pour qu'elles soient uniformes. Pour rendre l'IA plus "robuste", nous utilisons la **Data Augmentation** : nous créons des variantes de chaque image (rotation, zoom, changement de luminosité). Cela apprend à l'IA à reconnaître une maladie quel que soit l'angle de vue ou l'éclairage.

**Remplacer par :**
La lumière varie d'une photo à l'autre. Nous appliquons la technique CLAHE (Contrast Limited Adaptive Histogram Equalization) pour normaliser le contraste des images de manière adaptative, zone par zone, via la bibliothèque OpenCV. Cette technique est particulièrement efficace pour les photos de peau prises dans des conditions d'éclairage variables. Pour rendre l'IA plus "robuste", nous utilisons ensuite la Data Augmentation : nous créons des variantes de chaque image (rotation 90°/180°, zoom, changement de luminosité). Cela apprend à l'IA à reconnaître une maladie quel que soit l'angle de vue ou l'éclairage.

**⚠️ Effet sur le reste :**
- Aucun impact sur les sections suivantes. Le paragraphe garde la même structure, il est juste enrichi techniquement.

---

## Modification 4 — Préciser U-Net + ResNet34 (Section 4.2.1, ligne 193-195)

**Texte actuel (ligne 193-195) :**
> Une image de peau contient souvent des éléments inutiles (poils, bijoux, vêtements). Pour que l'IA se concentre sur l'essentiel, nous utilisons un premier modèle appelé **U-Net**. Sa mission est de générer un "masque" : il colorie en blanc la zone de la maladie et en noir le reste de l'image.

**Remplacer par :**
Une image de peau contient souvent des éléments inutiles (poils, bijoux, vêtements). Pour que l'IA se concentre sur l'essentiel, nous utilisons un premier modèle de segmentation : U-Net avec un backbone ResNet34 pré-entraîné sur ImageNet, implémenté via la bibliothèque Python segmentation-models. Sa mission est de générer un "masque binaire" : il colorie en blanc la zone de la maladie et en noir le reste de l'image. L'image est redimensionnée à 256×256 pixels pour la segmentation, puis le masque est reprojeté à la taille originale de la photo.

**⚠️ Effet sur le reste :**
- La section 4.2.2 (Auto-Cropping) qui suit parle justement du masque généré → la cohérence est renforcée.

---

## Modification 5 — Préciser FastAPI + pyngrok (Section 6.2.2, ligne 277-279)

**Texte actuel (ligne 277-279) :**
> Pour centraliser les résultats, nous avons conçu une API (Interface de Programmation). Elle permet de transférer de manière sécurisée les statistiques de diagnostic vers une base de données centrale. Cela permet de savoir quelles maladies sont les plus présentes dans telle ou telle région en temps réel.

**Remplacer par :**
Pour centraliser les résultats, nous avons conçu une API REST développée avec FastAPI (framework Python haute performance), hébergée sur Google Colab et exposée sur Internet via un tunnel HTTPS pyngrok. L'API propose deux endpoints : `/predict` pour le diagnostic Cloud (mode Elite) et `/collect` pour la collecte de nouvelles images annotées. Elle permet de transférer de manière sécurisée les statistiques de diagnostic vers une base de données centrale, rendant possible le suivi épidémiologique en temps réel.

**⚠️ Effet sur le reste :**
- La section 6.3 (Smart DATA-CITY / SIG) qui suit parle de "cartographier ces données" → la mention de `/collect` renforce la cohérence.

---

## Modification 6 — Ajouter U-Net au pipeline Cloud (Section 8.1.3, ligne 381-383)

**Texte actuel (ligne 381-383) :**
> Nous avons comparé le temps de réponse et la précision entre le diagnostic sur le téléphone (Edge) et sur le serveur (Cloud). Si le Cloud est légèrement plus précis (environ +2%), le diagnostic local est 5 fois plus rapide et ne nécessite aucun transfert de données coûteux. Pour un usage de terrain, le diagnostic local est donc largement préférable.

**Remplacer par :**
Nous avons comparé le temps de réponse et la précision entre le diagnostic sur le téléphone (Edge) et sur le serveur (Cloud). En mode Cloud (Elite), l'image passe par un pipeline complet reproduisant les conditions d'entraînement : segmentation U-Net (isolation de la lésion), crop automatique, CLAHE (égalisation du contraste), puis classification par EfficientNetV2-L, tirant parti du GPU Tesla T4 disponible sur le serveur. Ce pipeline amélioré rend le mode Cloud plus précis que le mode local. Cependant, le diagnostic local reste 5 fois plus rapide et ne nécessite aucun transfert de données coûteux. Pour un usage de terrain sans connexion, le diagnostic local est donc préférable.

**⚠️ Effet sur le reste :**
- Cela contredit légèrement l'ancienne formulation "environ +2%". La nouvelle version est plus honnête et ne donne pas de chiffre inventé puisque nous n'avons pas re-mesuré la différence avec U-Net dans le pipeline Cloud.

---

## Modification 7 — Préciser les GPU utilisés (Section 5.1.1, ligne 228-230)

**Texte actuel (ligne 228-230) :**
> L'entraînement d'un réseau de neurones profonds nécessite une puissance de calcul colossale, impossible à fournir par un ordinateur de bureau standard. Nous avons donc utilisé les plateformes Cloud **Kaggle** et **Google Colab**. Ces outils nous donnent accès à des processeurs graphiques (GPU) puissants qui permettent de traiter des milliers d'images en quelques heures seulement.

**Remplacer par :**
L'entraînement d'un réseau de neurones profonds nécessite une puissance de calcul colossale, impossible à fournir par un ordinateur de bureau standard. Nous avons donc utilisé les plateformes Cloud Kaggle (GPU NVIDIA P100) et Google Colab (GPU NVIDIA Tesla T4). Ces processeurs graphiques disposent de 16 Go de mémoire dédiée et permettent de traiter nos 11 209 images en quelques heures seulement.

**⚠️ Effet sur le reste :**
- Aucun. Information purement additive.

---

## Modification 8 — Mentionner la bibliothèque Scikit-learn (Section 8.1.1 ou 8.1.2)

**Où :** Après le Tableau 5 (ligne 379), avant la section 8.1.3 (ligne 381).

**Ajouter ce paragraphe :**
Les métriques du tableau ci-dessus ont été calculées automatiquement à l'aide de la bibliothèque Scikit-learn (classification_report, confusion_matrix, roc_curve). Les visualisations (matrice de confusion et courbes ROC) ont été générées avec Matplotlib et Seaborn.

**⚠️ Effet sur le reste :**
- Décale les lignes suivantes de +2. Aucun impact sur la cohérence.

---

## Résumé des modifications

| # | Section | Type | Complexité |
|:---|:---|:---|:---|
| 1 | 5.1.2 | Remplacement | Moyenne |
| 2 | 5.2.1 | Remplacement + Ajout | **Haute** (le plus gros ajout) |
| 3 | 4.3.1 | Remplacement | Faible |
| 4 | 4.2.1 | Remplacement | Faible |
| 5 | 6.2.2 | Remplacement | Faible |
| 6 | 8.1.3 | Remplacement | Moyenne |
| 7 | 5.1.1 | Remplacement | Faible |
| 8 | Après Tableau 5 | Ajout | Faible |

> [!IMPORTANT]
> **Ordre recommandé :** Appliquer les modifications **de bas en haut** (8 → 1) pour éviter que les décalages de lignes n'affectent les repères des modifications suivantes.

> [!WARNING]
> La **Modification 2** (processus en 2 phases) est la plus volumineuse. Elle ajoute environ 10 lignes dans la section 5.2.1. Toutes les références de type "ligne XXX" dans ce document sont basées sur la version actuelle du fichier. Après cette modification, les lignes 242+ seront décalées d'environ +10.


CNN : Convolutional Neural Network
ROI : Region of Interest
XAI : Explainable Artificial Intelligence
CRISP-DM : Cross Industry Standard Process for Data Mining
HTTPS : HyperText Transfer Protocol Secure
TLS : Transport Layer Security
RGPD : Règlement Général sur la Protection des Données
AI Act : Artificial Intelligence Act
HAM10000 : Human Against Machine with 10000 training images
ISIC : International Skin Imaging Collaboration
U-Net : U-shaped Convolutional Network
GPU : Graphics Processing Unit
TFLite : TensorFlow Lite
API : Application Programming Interface
SIG : Système d’Information Géographique
UX : User Experience
GPS : Global Positioning System
SQLite : Structured Query Language Lite
AUC-ROC : Area Under the Curve - Receiver Operating Characteristic
CAD : Computer-Aided Diagnosis
Edge Computing : Informatique en périphérie
Transfer Learning : Apprentissage par transfert
Data Augmentation : Augmentation des données
Grad-CAM : Gradient-weighted Class Activation Mapping
Smart City : Ville intelligente
Big Data : Données massives
IoT : Internet of Things

