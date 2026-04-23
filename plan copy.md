# TITRE : Conception et Implémentation d'un Système d'Aide au Diagnostic des Maladies de la Peau par Vision par Ordinateur
## Sous-titre : Intelligence Artificielle embarquée, Deep Learning et télédermatologie sur mobile

---

# INTRODUCTION

Dans un monde de plus en plus connecté, l'accès aux soins de santé spécialisés demeure l'un des défis majeurs pour les populations vivant dans des zones isolées ou à ressources limitées. Les maladies de la peau, bien que souvent négligées, touchent près d'un tiers de la population mondiale et constituent un fardeau socio-économique considérable. La rareté des dermatologues, couplée à la difficulté d'accès aux infrastructures hospitalières, entraîne des diagnostics tardifs qui aggravent les complications médicales.

Le projet **Cutisia** s'inscrit dans cette dynamique de transformation numérique de la santé. Il propose de mettre la puissance de l'Intelligence Artificielle et de la vision par ordinateur au service du dépistage précoce. En exploitant la ubiquité des smartphones, notre solution permet de capturer, de segmenter et de classifier des lésions cutanées en temps réel, offrant ainsi une première orientation diagnostique fiable. Intégré dans une vision de "Smart DATA-CITY", Cutisia n'est pas seulement un outil individuel, mais un maillon essentiel d'un système d'information géographique sanitaire capable de monitorer l'évolution épidémiologique à l'échelle urbaine.

Ce mémoire présente le parcours de conception et de réalisation de ce système, depuis l'ingénierie complexe d'un dataset multi-sources jusqu'au déploiement d'un moteur d'inférence optimisé pour les terminaux mobiles à ressources limitées.

# PARTIE 1 : ÉTAT DE L'ART ET PROBLÉMATIQUE DE LA SANTÉ DERMATOLOGIQUE

## Chapitre 1 : Enjeux de la dermatologie et apport des technologies numériques
### 1.1 Contexte épidémiologique et défis du diagnostic précoce
#### 1.1.1 Prévalence des affections cutanées en zones isolées
#### 1.1.2 Pénurie de spécialistes et délais de prise en charge
### 1.2 La Télédermatologie : Une réponse par l'imagerie médicale
#### 1.2.1 Historique et évolution du diagnostic assisté par ordinateur (CAD)
#### 1.2.2 Impact de l'imagerie mobile dans le dépistage de première intention

## Chapitre 2 : Intelligence Artificielle et Vision par Ordinateur en Santé
### 2.1 Fondements du Deep Learning appliqué à l'image
#### 2.1.1 Réseaux de neurones convolutifs (CNN) et extraction de caractéristiques
#### 2.1.2 Architectures légères pour l'IA embarquée (MobileNet, EfficientNet)
### 2.2 Apprentissage par transfert et spécificités des datasets médicaux
#### 2.2.1 Problématique du déséquilibre des classes et de la qualité d'image
#### 2.2.2 Métriques d'évaluation en diagnostic médical (Précision, Rappel, Score F1)
### 2.3 Méthodologie et Cycle de vie du projet IA
#### 2.3.1 Approche itérative et processus CRISP-DM (Data Science Lifecycle)
#### 2.3.2 Phases de prototypage et boucle de rétroaction (Feedback Loop)

## Chapitre 3 : Ingénierie des données et Prétraitement Avancé
### 3.1 Constitution du Dataset et Pipeline de Collecte
#### 3.1.1 Agrégation multi-sources : HAM10000, ISIC Archive, CO2Wounds et Web Scrapping
#### 3.1.2 Sélection des classes pathologiques et analyse de la représentativité
### 3.2 Segmentation et Localisation des Lésions (ROI)
#### 3.2.1 Architecture U-Net pour la génération automatique de masques binaires
#### 3.2.2 Algorithmes de détourage (Auto-Cropping) et centrage sur la pathologie
### 3.3 Préparation finale et Optimisation des entrées
#### 3.3.1 Normalisation chromatique et techniques d'augmentation (Data Augmentation)
#### 3.3.2 Gestion du déséquilibre par sur-échantillonnage et pondération des pertes

## Chapitre 4 : Cycle d'Apprentissage et Modélisation de l'IA
### 4.1 Stratégie d'entraînement et infrastructure Cloud
#### 4.1.1 Environnements de calcul haute performance (Kaggle Kernels, Google Colab)
#### 4.1.2 Choix des architectures (MobileNetV2, EfficientNet) et Transfer Learning
### 4.2 Optimisation et Exportation vers l'embarqué
#### 4.2.1 Analyse des hyperparamètres et suivi de la convergence (Loss/Accuracy)
#### 4.2.2 Quantification (Int8/Float16) et conversion vers le format TFLite
### 4.3 Interprétabilité et Fiabilité du modèle (Explainable AI - XAI)
#### 4.3.1 Visualisation des zones d'activation via Grad-CAM (Heatmaps)
#### 4.3.2 Analyse des faux positifs et gestion de l'incertitude médicale

# PARTIE 2 : CONCEPTION ARCHITECTURALE ET MÉTHODOLOGIE DU SYSTÈME CUTISIA

## Chapitre 5 : Architecture système et pipeline de traitement
### 5.1 Conception globale de la solution "Edge-to-Cloud"
#### 5.1.1 Architecture hybride : Inférence locale vs Analyse Cloud
#### 5.1.2 Arbitrage Performance/Consommation en Edge Computing
### 5.2 Modélisation et optimisation du moteur d'IA
#### 5.2.1 Prétraitement des images et segmentation des lésions
#### 5.2.2 Conversion et optimisation du modèle pour l'embarqué (TFLite)
### 5.3 Gouvernance et Éthique des données de santé
#### 5.3.1 Anonymisation des métadonnées et sécurité des échanges (Protocole HTTPS/TLS)
#### 5.3.2 Conformité aux principes de protection des données personnelles (RGPD/Santé)

## Chapitre 6 : Développement de l'écosystème logiciel
### 6.1 Interface utilisateur et expérience patient (Mobile)
#### 6.1.1 Architecture logicielle et design system (Flutter)
#### 6.1.2 Gestion du cycle de vie de la caméra et capture optimisée
### 6.2 Gestion des données et synchronisation Cloud
#### 6.2.1 Persistance locale des dossiers patients (SQLite/sqflite)
#### 6.2.2 API de collecte et centralisation des données épidémiologiques

# PARTIE 3 : RÉALISATION, TESTS ET ANALYSE DES RÉSULTATS

## Chapitre 7 : Mise en œuvre technique et intégration logicielle
### 7.1 Développement du prototype mobile "Cutisia Elite AI"
#### 7.1.1 Intégration du moteur d'inférence en temps réel
#### 7.1.2 Implémentation des modules de localisation et de traitement
### 7.2 Optimisation pour les contraintes du terrain
#### 7.2.1 Gestion des performances sur terminaux à ressources limitées (API 24)
#### 7.2.2 Interface multilingue et accessibilité (Localisation Malgache)

## Chapitre 8 : Évaluation des performances et discussion
### 8.1 Validation expérimentale du modèle de détection
#### 8.1.1 Analyse de la matrice de confusion et courbes AUC-ROC
#### 8.1.2 Comparaison des performances Local vs Cloud
### 8.2 Analyse critique et perspectives d'évolution
#### 8.2.1 Scalabilité urbaine : Gestion des flux massifs de données épidémiologiques
#### 8.2.2 Évolutivité : Intégration de la détection par segmentation et suivi temporel

# CONCLUSION

Au terme de ce projet, nous avons réussi à concevoir et à déployer une solution complète d'aide au diagnostic dermatologique alliant rigueur scientifique et contraintes de terrain. L'implémentation d'un pipeline hybride, utilisant l'architecture **U-Net** pour une segmentation précise de la lésion et des modèles de classification optimisés pour le **Edge Computing**, a permis de garantir des performances élevées tout en maintenant une réactivité optimale sur mobile.

Les tests effectués sur une diversité de pathologies — allant du mélanome aux maladies tropicales négligées comme la lèpre — démontrent le potentiel de l'IA pour combler le fossé médical dans les zones sous-dotées. Au-delà de l'aspect technique, le projet **Cutisia** valide l'idée qu'une gestion intelligente des données de santé peut transformer une ville en une "Smart City" proactive en matière de santé publique.

Bien que des défis subsistent, notamment en termes de variabilité lumineuse et de diversité des phototypes, les perspectives d'évolution sont nombreuses. L'intégration future de techniques d'IA explicable (XAI) plus poussées et le renforcement des boucles de rétroaction entre personnels de santé et modèles d'apprentissage permettront de faire de Cutisia un standard de la télédermatologie mobile, accessible à tous, partout.

---

# RÉFÉRENCES

### Bibliographie (Biblio)
*   **[1]** : Esteva, A., et al. (2017). "*Dermatologist-level classification of skin cancer with deep neural networks*". Nature. (Référence majeure de l'IA en dermatologie).
*   **[2]** : Howard, A. G., et al. (2017). "*MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*". (Base technique de l'inférence mobile).
*   **[3]** : WHO. "*Global report on neglected tropical diseases 2023*". (Cadre sanitaire pour les maladies de peau en Afrique).

### Webographie (Web)
*   **[4]** : TensorFlow Lite. "*Deploy machine learning models on mobile and edge devices*". [https://www.tensorflow.org/lite](https://www.tensorflow.org/lite)
*   **[5]** : Flutter Documentation. "*Multi-platform app development*". [https://docs.flutter.dev/](https://docs.flutter.dev/)
*   **[6]** : ISIC Archive. "*International Skin Imaging Collaboration*". [https://www.isic-archive.com/](https://www.isic-archive.com/)
