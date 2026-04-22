# TITRE : Conception et Implémentation d'un Système d'Aide au Diagnostic des Maladies de la Peau par Vision par Ordinateur
## Sous-titre : Intelligence Artificielle embarquée, Deep Learning et télédermatologie sur mobile

---

# INTRODUCTION

Dans un monde de plus en plus connecté, l'accès aux soins de santé spécialisés demeure l'un des défis majeurs pour les populations vivant dans des zones isolées ou à ressources limitées. Les maladies de la peau, bien que souvent négligées, touchent près d'un tiers de la population mondiale et constituent un fardeau socio-économique considérable. La rareté des dermatologues, couplée à la difficulté d'accès aux infrastructures hospitalières, entraîne des diagnostics tardifs qui aggravent les complications médicales.

Le projet **Cutisia** s'inscrit dans cette dynamique de transformation numérique de la santé. Il propose de mettre la puissance de l'Intelligence Artificielle et de la vision par ordinateur au service du dépistage précoce. En exploitant la ubiquité des smartphones, notre solution permet de capturer, de segmenter et de classifier des lésions cutanées en temps réel, offrant ainsi une première orientation diagnostique fiable. Intégré dans une vision de "Smart DATA-CITY", Cutisia n'est pas seulement un outil individuel, mais un maillon essentiel d'un système d'information géographique sanitaire capable de monitorer l'évolution épidémiologique à l'échelle urbaine.

Ce mémoire présente le parcours de conception et de réalisation de ce système, depuis l'ingénierie complexe d'un dataset multi-sources jusqu'au déploiement d'un moteur d'inférence optimisé pour les terminaux mobiles à ressources limitées. La démarche adoptée est encadrée dès le départ par des principes éthiques et de gouvernance des données de santé, garants de la fiabilité et de l'acceptabilité de la solution.

---

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

## Chapitre 3 : Éthique, Gouvernance et Contraintes Réglementaires
### 3.1 Spécificités des données de santé et obligations légales
#### 3.1.1 Anonymisation des métadonnées et sécurité des échanges (Protocole HTTPS/TLS)
#### 3.1.2 Conformité aux principes de protection des données personnelles (RGPD/Santé)

### 3.2 Responsabilité de l'IA en contexte médical
#### 3.2.1 Limites légales de l'aide au diagnostic et rôle du professionnel de santé
#### 3.2.2 Cadre réglementaire de la transparence algorithmique (AI Act, droit à l'explication)

---

# PARTIE 2 : CONCEPTION ARCHITECTURALE ET INGÉNIERIE DES DONNÉES

## Chapitre 4 : Ingénierie des données et Prétraitement Avancé
### 4.1 Constitution du Dataset et Pipeline de Collecte
#### 4.1.1 Agrégation multi-sources : HAM10000, ISIC Archive, CO2Wounds et Web Scrapping
#### 4.1.2 Sélection des classes pathologiques et analyse de la représentativité

### 4.2 Segmentation et Localisation des Lésions (ROI)
#### 4.2.1 Architecture U-Net pour la génération automatique de masques binaires
#### 4.2.2 Algorithmes de détourage (Auto-Cropping) et centrage sur la pathologie

### 4.3 Préparation finale et Optimisation des entrées
#### 4.3.1 Normalisation chromatique et techniques d'augmentation (Data Augmentation)
#### 4.3.2 Gestion du déséquilibre par sur-échantillonnage et pondération des pertes

## Chapitre 5 : Cycle d'Apprentissage et Modélisation de l'IA
### 5.1 Stratégie d'entraînement et infrastructure Cloud
#### 5.1.1 Environnements de calcul haute performance (Kaggle Kernels, Google Colab)
#### 5.1.2 Choix des architectures (MobileNetV2, EfficientNet) et Transfer Learning

### 5.2 Optimisation et Exportation vers l'embarqué
#### 5.2.1 Analyse des hyperparamètres et suivi de la convergence (Loss/Accuracy)
#### 5.2.2 Quantification (Int8/Float16) et conversion vers le format TFLite

### 5.3 Mise en œuvre technique de l'interprétabilité (XAI)
#### 5.3.1 Implémentation de Grad-CAM : Visualisation des zones d'activation sur les lésions
#### 5.3.2 Seuils de confiance et gestion des cas d'incertitude du modèle

## Chapitre 6 : Architecture Système et Conception de la Solution "Edge-to-Cloud"
### 6.1 Conception globale de la solution
#### 6.1.1 Architecture hybride : Inférence locale vs Analyse Cloud
#### 6.1.2 Arbitrage Performance/Consommation en Edge Computing

### 6.2 Modélisation du pipeline de traitement bout-en-bout
#### 6.2.1 Du dataset U-Net à l'intégration dans le moteur embarqué : fil conducteur technique
#### 6.2.2 API de collecte et centralisation des données épidémiologiques

### 6.3 Vision "Smart DATA-CITY" et Système d'Information Géographique Sanitaire
#### 6.3.1 Cutisia comme maillon d'un réseau de surveillance épidémiologique urbaine
#### 6.3.2 Modélisation des flux de données et monitoring à l'échelle de la ville

---

# PARTIE 3 : RÉALISATION, TESTS ET ANALYSE DES RÉSULTATS

## Chapitre 7 : Développement et Intégration logicielle
### 7.1 Interface utilisateur et expérience patient (Mobile)
#### 7.1.1 Architecture logicielle et design system (Flutter)
#### 7.1.2 Gestion du cycle de vie de la caméra et capture optimisée

### 7.2 Développement du prototype mobile "Cutisia Elite AI"
#### 7.2.1 Intégration du moteur d'inférence en temps réel
#### 7.2.2 Implémentation des modules de localisation et de traitement

### 7.3 Gestion des données et synchronisation Cloud
#### 7.3.1 Persistance locale des dossiers patients (SQLite/sqflite)
#### 7.3.2 Optimisation pour les contraintes du terrain (API 24, terminaux limités)

### 7.4 Accessibilité et adaptation au contexte local
#### 7.4.1 Interface multilingue et accessibilité (Localisation Malgache)
#### 7.4.2 Gestion de la variabilité lumineuse et des phototypes locaux

## Chapitre 8 : Évaluation des performances et Validation
### 8.1 Validation expérimentale du modèle de détection
#### 8.1.1 Analyse de la matrice de confusion et courbes AUC-ROC
#### 8.1.2 Comparaison des performances Local vs Cloud

### 8.2 Validation terrain et retour utilisateurs
#### 8.2.1 Protocole de test avec agents de santé et personnel médical
#### 8.2.2 Analyse de l'acceptabilité et des cas d'usage réels

### 8.3 Analyse critique des limites du système
#### 8.3.1 Identification des biais du dataset et des conditions d'échec du modèle
#### 8.3.2 Limites de l'architecture Edge et contraintes de déploiement à grande échelle

## Chapitre 9 : Perspectives d'évolution et Scalabilité
### 9.1 Évolutivité technique du moteur d'IA
#### 9.1.1 Intégration de la détection par segmentation sémantique et suivi temporel
#### 9.1.2 Renforcement des boucles de rétroaction médecin–modèle (Active Learning)

### 9.2 Scalabilité urbaine et déploiement à grande échelle
#### 9.2.1 Gestion des flux massifs de données épidémiologiques (Big Data Santé)
#### 9.2.2 Interopérabilité avec les systèmes de santé nationaux et régionaux

---

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