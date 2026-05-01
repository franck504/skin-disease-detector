# FICHE TECHNIQUE — Projet Cutisia (Portfolio)

---

## 1. C'est du Machine Learning ou du Deep Learning ?

**→ Deep Learning (Apprentissage Profond)**

Le Machine Learning classique utilise des algorithmes qui travaillent sur des caractéristiques extraites manuellement (ex: SVM, Random Forest).
Le Deep Learning utilise des **réseaux de neurones profonds** qui apprennent automatiquement à extraire les caractéristiques pertinentes directement depuis les pixels de l'image.

Dans Cutisia, nous utilisons :
- Des **CNN** (Convolutional Neural Networks) pour la classification des maladies
- Un **U-Net** (réseau encodeur-décodeur) pour la segmentation des lésions

Ce sont des architectures profondes avec des dizaines de millions de paramètres → c'est du **Deep Learning**, pas du ML classique.

---

## 2. Famille du modèle et architecture

### Modèle principal : **EfficientNetV2-L** (Large)
- **Famille** : Réseaux de neurones convolutifs (CNN)
- **Sous-famille** : Architecture à mise à l'échelle composée (Compound Scaling)
- **Créateur** : Google Brain (Mingxing Tan & Quoc V. Le, 2021)
- **Particularité** : Équilibre optimal entre profondeur, largeur et résolution
- **Taille d'entrée** : 384×384 pixels (configuré dans le code)
- **Nombre de paramètres** : ~118 millions
- **Couche de tête personnalisée** :
  ```
  EfficientNetV2-L (base gelée) → GlobalAveragePooling2D → Dense(512, ReLU) → Dropout(0.4) → Dense(6, Softmax)
  ```

### Modèle de segmentation : **U-Net** (avec backbone ResNet34)
- **Famille** : Réseau encodeur-décodeur pour segmentation sémantique
- **Rôle** : Générer des masques binaires pour isoler les lésions cutanées
- **Bibliothèque** : `segmentation-models` (sm.Unet)

### Modèle mobile : **TFLite** (conversion du modèle principal)
- Le modèle EfficientNetV2-L est converti en format `.tflite` pour l'inférence sur smartphone

---

## 3. Entraînement from zero ou ré-entraînement ?

**→ Ré-entraînement (Transfer Learning + Fine-Tuning)**

Nous n'avons **PAS** entraîné le modèle à partir de zéro. Voici ce qui a été fait :

### Phase 1 : Transfer Learning (Warm-up) — 5 epochs
- Le modèle **EfficientNetV2-L** a été chargé avec des poids **pré-entraînés sur ImageNet** (1,4 million d'images de la vie courante)
- La base convolutive a été **entièrement gelée** (`base_model.trainable = False`)
- Seules les **couches de tête** (Dense + Softmax) ont été entraînées
- Learning rate : `1e-4`

### Phase 2 : Fine-Tuning — Jusqu'à 50 epochs
- Les **50 dernières couches** de la base ont été **dégelées**
- L'ensemble du modèle a été ré-entraîné avec un learning rate réduit (`1e-5`)
- Utilisation de callbacks : EarlyStopping (patience=8), ReduceLROnPlateau

### Pourquoi pas from zero ?
- Entraîner EfficientNetV2-L from zero nécessiterait **des millions d'images** et **des semaines de calcul GPU**
- Avec seulement 11 209 images médicales, le Transfer Learning est **indispensable** pour éviter le sur-apprentissage (overfitting)

---

## 4. Modules Python et outils utilisés

### A. Deep Learning & IA
| Module | Rôle |
|:---|:---|
| **TensorFlow / Keras** | Framework principal : définition, entraînement et inférence des modèles CNN |
| **TensorFlow Lite** | Conversion et optimisation du modèle pour l'embarqué mobile |
| **segmentation-models (sm)** | Bibliothèque U-Net pour la segmentation des lésions (backbone ResNet34) |

### B. Traitement d'images
| Module | Rôle |
|:---|:---|
| **OpenCV (cv2)** | CLAHE (égalisation adaptative), crop de lésion, resize, Grad-CAM heatmap |
| **Pillow (PIL)** | Lecture et conversion d'images côté API serveur |
| **NumPy** | Manipulation matricielle des images (tableaux de pixels) |

### C. Évaluation & Visualisation
| Module | Rôle |
|:---|:---|
| **Scikit-learn (sklearn)** | Métriques : confusion_matrix, roc_curve, auc, classification_report |
| **Matplotlib** | Génération des graphiques (courbes ROC, matrice de confusion) |
| **Seaborn** | Heatmap stylisée pour la matrice de confusion |

### D. Gestion des données
| Module | Rôle |
|:---|:---|
| **os / glob / pathlib** | Navigation dans le système de fichiers, recherche récursive |
| **shutil** | Déplacement physique des fichiers lors de la migration du dataset |
| **re (regex)** | Tri intelligent des dossiers hybrides (ex: Cellulite vs Impétigo) |
| **imghdr** | Vérification du format réel des fichiers images |
| **tqdm** | Barre de progression pour le traitement des images |

### E. Déploiement & API
| Module | Rôle |
|:---|:---|
| **FastAPI** | Framework API REST pour le endpoint `/predict` et `/collect` |
| **Uvicorn** | Serveur ASGI pour exécuter FastAPI |
| **pyngrok (ngrok)** | Tunnel HTTPS pour exposer l'API Colab sur internet |
| **nest_asyncio** | Compatibilité asyncio dans les notebooks Jupyter/Colab |
| **json** | Sérialisation des métadonnées de collecte |

### F. Suivi d'entraînement
| Module | Rôle |
|:---|:---|
| **Weights & Biases (wandb)** | Monitoring en temps réel des courbes d'entraînement (Loss, Accuracy) |

### G. Application Mobile
| Outil | Rôle |
|:---|:---|
| **Flutter / Dart** | Framework frontend mobile (Android) |
| **tflite_flutter** | Plugin Flutter pour charger et exécuter le modèle TFLite sur le téléphone |
| **sqflite (SQLite)** | Base de données locale pour les dossiers patients |

---

## 5. Type et méthode d'apprentissage

### Type : **Apprentissage Supervisé (Supervised Learning)**

Le modèle apprend à partir d'images **étiquetées** : chaque image est associée à un label (Candidiase, Leprosy, Mélanome, etc.). L'IA compare sa prédiction avec le label réel et ajuste ses poids pour minimiser l'erreur.

### Méthodes utilisées :

| Méthode | Description |
|:---|:---|
| **Transfer Learning** | Réutilisation des poids pré-entraînés d'ImageNet comme point de départ |
| **Fine-Tuning** | Dégel progressif des couches profondes pour spécialiser le modèle |
| **Data Augmentation** | Rotation, zoom, variation de luminosité pour enrichir le dataset |
| **CLAHE** | Égalisation adaptative du contraste pour normaliser les conditions d'éclairage |
| **Classification multi-classe** | Softmax en sortie → probabilité pour chacune des 6 classes |
| **One-Hot Encoding** | Les labels sont encodés en vecteurs binaires ([0,1,0,0,0,0] = Leprosy) |

### Fonction de perte : `categorical_crossentropy`
### Optimiseur : `Adam` (adaptatif)
### Callbacks :
- **EarlyStopping** : Arrêt si pas d'amélioration pendant 8 epochs
- **ReduceLROnPlateau** : Réduction du learning rate si stagnation
- **ModelCheckpoint** : Sauvegarde automatique du meilleur modèle

---

## 6. Résumé pour le Portfolio (Version courte)

> **Cutisia** — Application mobile de détection de maladies cutanées tropicales par Deep Learning.
>
> - **Type** : Deep Learning / Vision par Ordinateur (Computer Vision)
> - **Architecture** : EfficientNetV2-L (CNN) + U-Net (Segmentation)
> - **Méthode** : Apprentissage supervisé avec Transfer Learning et Fine-Tuning
> - **Dataset** : 11 209 images, 6 classes pathologiques
> - **Stack** : TensorFlow, OpenCV, FastAPI, Flutter, SQLite
> - **Déploiement** : Edge Computing (TFLite sur mobile) + Cloud (API FastAPI/ngrok)
> - **Interprétabilité** : Grad-CAM (XAI)
> - **Résultats** : F1-Score de 0.65 sur la Lèpre (meilleure classe)











Excellente idée pour le portfolio ! Je vais d'abord revoir vos fichiers de code pour vous donner des réponses **100% exactes**, puis je vous prépare une fiche technique complète.

Viewed evaluate_and_visualize.py:1-252
Viewed audit_dataset.py:1-37
Listed directory projet3
Viewed train_dual_models.py:1-195
Viewed generate_masks.py:1-106
Viewed api_server.py:1-148
Viewed migrate_and_unify.py:1-138

Parfait, j'ai relu tout votre code de A à Z. Voici la fiche technique complète pour votre portfolio.

Edited fiche_technique_portfolio.md

J'ai créé le fichier **`livre_memoire/fiche_technique_portfolio.md`** après avoir relu l'intégralité de votre code. Voici le résumé des réponses à vos 5 questions :

---

### 🎯 Réponses rapides :

| Question | Réponse |
|:---|:---|
| **ML ou DL ?** | **Deep Learning** (CNN à +118M de paramètres) |
| **Famille / Architecture ?** | **CNN** → **EfficientNetV2-L** (classification) + **U-Net/ResNet34** (segmentation) |
| **From zero ou ré-entraînement ?** | **Transfer Learning + Fine-Tuning** sur poids ImageNet (pas from zero) |
| **Modules Python ?** | TensorFlow, OpenCV, Scikit-learn, FastAPI, pyngrok, wandb, segmentation-models, Matplotlib, Seaborn, NumPy, PIL, tqdm |
| **Méthode d'apprentissage ?** | **Supervisé** (images étiquetées) avec Data Augmentation, CLAHE, et One-Hot Encoding |

### 📁 Scripts du projet (rappel) :

| Script | Rôle |
|:---|:---|
| `migrate_and_unify.py` | Agrégation et nettoyage du dataset multi-sources |
| `generate_masks.py` | Segmentation U-Net → masques binaires |
| `train_dual_models.py` | Entraînement EfficientNetV2-L + conversion TFLite |
| `evaluate_and_visualize.py` | Évaluation + Grad-CAM + Matrice + ROC |
| `api_server.py` | API FastAPI + ngrok pour le mode Cloud |
| `audit_dataset.py` | Audit du nombre d'images par classe |

La fiche complète avec tous les détails est dans votre fichier `fiche_technique_portfolio.md`.