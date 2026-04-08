# Guide de Saisie Jira (Manuel) : Projet "Cutisia"

Ce document détaille chaque étape pour construire votre tableau de bord Jira. 

## 💡 Mode d'emploi pour la saisie :
1. **Créer les Épiques** en premier (Bouton "Créer" > Type : Épique).
2. **Créer les Tâches** et les lier à leur Épique respective via le champ "Épique" ou "Parent".
3. **Ajouter les Sous-tâches** à l'intérieur de chaque tâche pour le suivi quotidien.

---

## 🏗️ EPIC 1 : Recherche & Ingestion de Données
**Labels :** `DATA`, `CRISP-DM` | **Priorité :** High

### TASK 1.1 : Analyse & Inventaire des sources
*   **Description :** Étude structurelle des datasets ISIC et HAM10000.
*   **Sous-tâches :**
    - [ ] **ST-1.1.1 :** Vérification de l'intégrité des dossiers extraits.
    - [ ] **ST-1.1.2 :** Mapping des classes (Lèpre, Gale, etc.) vers les dossiers sources.
    - [ ] **ST-1.1.3 :** Analyse de la résolution moyenne par source.

### TASK 1.2 : Migration Technique Unifiée
*   **Description :** Déplacement physique des fichiers vers `datasets-cutisia/`.
*   **Sous-tâches :**
    - [ ] **ST-1.2.1 :** Test du script `migrate_and_unify.py` sur un échantillon.
    - [ ] **ST-1.2.2 :** Migration complète des 11 000+ images.
    - [ ] **ST-1.2.3 :** Contrôle des doublons et des liens brisés.

---

## 🧪 EPIC 2 : Pipeline de Préparation & Qualité
**Labels :** `QUALITY`, `PREPROCESSING` | **Priorité :** High

### TASK 2.1 : Standardisation & Resizing
*   **Description :** Préparation visuelle des clichés pour le modèle MobileNetV3.
*   **Sous-tâches :**
    - [ ] **ST-2.1.1 :** Redimensionnement massif en 224x224 (Interpolation Lanczos).
    - [ ] **ST-2.1.2 :** Conversion de tous les formats exotiques (PNG, BMP) en JPEG.
    - [ ] **ST-2.1.3 :** Normalisation de la luminosité (Histogram Equalization).

### TASK 2.2 : Nettoyage & Data Augmentation
*   **Description :** Enrichissement du dataset pour simuler des photos prises sur smartphone.
*   **Sous-tâches :**
    - [ ] **ST-2.2.1 :** Tri manuel pour supprimer les images floues.
    - [ ] **ST-2.2.2 :** Configuration de la rotation, zoom et bruit numérique (Roboflow).
    - [ ] **ST-2.2.3 :** Vérification de la diversité des teintes de peau (Fitzpatrick).

---

## 🧠 EPIC 3 : Modélisation & Entraînement IA
**Labels :** `AI`, `MODELING` | **Priorité :** High

### TASK 3.1 : Entraînement Cloud (EfficientNetV2)
*   **Description :** Création du modèle "Lourd" pour l'expertise via API.
*   **Sous-tâches :**
    - [ ] **ST-3.1.1 :** Setup de l'environnement GPU (Colab Pro/Kaggle).
    - [ ] **ST-3.1.2 :** Fine-tuning des poids ImageNet sur Cutisia.
    - [ ] **ST-3.1.3 :** Exportation du modèle au format `.h5`.

### TASK 3.2 : Optimisation Mobile (TFLite)
*   **Description :** Conversion du modèle léger pour Flutter.
*   **Sous-tâches :**
    - [ ] **ST-3.2.1 :** Entraînement MobileNetV3-Large.
    - [ ] **ST-3.2.2 :** Quantification INT8 pour réduire la taille à < 10 Mo.
    - [ ] **ST-3.2.3 :** Génération du fichier `labels.txt`.

---

## 📱 EPIC 4 : Application Mobile Flutter
**Labels :** `MOBILE`, `FLUTTER` | **Priorité :** Medium

### TASK 4.1 : Expérience de Capture Intelligent
*   **Description :** UI caméra avec guide de distance.
*   **Sous-tâches :**
    - [ ] **ST-4.1.1 :** Développement de l'overlay caméra (Rectangle de focus).
    - [ ] **ST-4.1.2 :** Logique de validation de la netteté avant capture.

### TASK 4.2 : Diagnostic & Recommandations
*   **Description :** Affichage des résultats et conseils de santé.
*   **Sous-tâches :**
    - [ ] **ST-4.2.1 :** Intégration du moteur d'inférence TFLite.
    - [ ] **ST-4.2.2 :** Traduction dynamique des termes médicaux en Malgache.

---

## 🚀 EPIC 5 : Déploiement & Livraison
**Labels :** `DEVOPS`, `RELEASE` | **Priorité :** Medium

### TASK 5.1 : Validation Terrain & Publication
*   **Description :** Tests finaux et mise en production.
*   **Sous-tâches :**
    - [ ] **ST-5.1.1 :** Test de performance sur smartphones d'entrée de gamme.
    - [ ] **ST-5.1.2 :** Signature de l'APK/App Bundle.
    - [ ] **ST-5.1.3 :** Mise en ligne du serveur API pour le modèle lourd.
