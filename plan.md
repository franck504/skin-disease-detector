# TITRE : Conception et Implémentation d'un Système d'Aide au Diagnostic des Maladies de la Peau par Vision par Ordinateur
## Sous-titre : Intelligence Artificielle embarquée, Deep Learning et télédermatologie sur mobile

---

# INTRODUCTION

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

## Chapitre 3 : Ingénierie des données et Cycle d'apprentissage de l'IA
### 3.1 Constitution du Dataset et sources de données
#### 3.1.1 Collecte par Web Scrapping et exploration des archives (ISIC, Kaggle)
#### 3.1.2 Sélection et justification des classes (Mélanomes, Monkeypox, Leprosy, etc.)
### 3.2 Préparation et Analyse Exploratoire des Données (EDA)
#### 3.2.1 Nettoyage, normalisation et gestion du déséquilibre des classes
#### 3.2.2 Techniques d'augmentation de données (Data Augmentation) pour la robustesse
### 3.3 Processus d'entraînement et infrastructure Cloud
#### 3.3.1 Environnements de calcul haute performance (Kaggle Kernels, Google Colab)
#### 3.3.2 Choix des hyperparamètres et optimisation des fonctions de perte

# PARTIE 2 : CONCEPTION ARCHITECTURALE ET MÉTHODOLOGIE DU SYSTÈME CUTISIA

## Chapitre 4 : Architecture système et pipeline de traitement
### 4.1 Conception globale de la solution "Edge-to-Cloud"
#### 4.1.1 Architecture hybride : Inférence locale vs Analyse Cloud
#### 4.1.2 Flux de données : De la capture d'image à la proposition de traitement
### 4.2 Modélisation et optimisation du moteur d'IA
#### 4.2.1 Prétraitement des images et segmentation des lésions
#### 4.2.2 Conversion et optimisation du modèle pour l'embarqué (TFLite)

## Chapitre 5 : Développement de l'écosystème logiciel
### 5.1 Interface utilisateur et expérience patient (Mobile)
#### 5.1.1 Architecture logicielle et design system (Flutter)
#### 5.1.2 Gestion du cycle de vie de la caméra et capture optimisée
### 5.2 Gestion des données et synchronisation Cloud
#### 5.2.1 Persistance locale des dossiers patients (SQLite/sqflite)
#### 5.2.2 API de collecte et centralisation des données épidémiologiques

# PARTIE 3 : RÉALISATION, TESTS ET ANALYSE DES RÉSULTATS

## Chapitre 6 : Mise en œuvre technique et intégration logicielle
### 6.1 Développement du prototype mobile "Cutisia Elite AI"
#### 6.1.1 Intégration du moteur d'inférence en temps réel
#### 6.1.2 Implémentation des modules de localisation et de traitement
### 6.2 Optimisation pour les contraintes du terrain
#### 6.2.1 Gestion des performances sur terminaux à ressources limitées (API 24)
#### 6.2.2 Interface multilingue et accessibilité (Localisation Malgache)

## Chapitre 7 : Évaluation des performances et discussion
### 7.1 Validation expérimentale du modèle de détection
#### 7.1.1 Analyse de la matrice de confusion et taux de réussite par pathologie
#### 7.1.2 Comparaison des performances Local vs Cloud
### 7.2 Analyse critique et perspectives d'évolution
#### 7.2.1 Limites du système : Variabilité lumineuse et types de peau
#### 7.2.2 Évolutivité : Intégration de la détection par segmentation et suivi temporel

# CONCLUSION

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
