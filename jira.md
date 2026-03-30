# Planification de Projet Jira : IA Médicale "Cutisia"

Ce document simule votre **Backlog Jira** pour piloter le projet. Il suit l'approche hybride **CRISP-DM** (IA) et **Agile** (Mobile).

---

## 🏗️ EPIC 1 : Recherche & Ingestion de Données (2-3 semaines)

### TASK 1.1 : Identification & Analyse des sources (CRISP-DM Phase 1 & 2)
*   **Sub-task 1.1.1 :** Analyse structurale des archives extraites (3j) - **[TERMINE]**
*   **Sub-task 1.1.2 :** Inventaire des classes & choix manuel des 9 maladies cibles (2j) - **[TERMINE]**
*   **Sub-task 1.1.3 :** Étude de la distance de capture camera/zoom par source (3j)

### TASK 1.2 : Migration & Organisation (CRISP-DM Phase 3)
*   **Sub-task 1.2.1 :** Création du dossier unifié `datasets-cutisia` (0.5j) - **[TERMINE]**
*   **Sub-task 1.2.2 :** Script de migration automatique vers l'organisation cible (2j)
*   **Sub-task 1.2.3 :** Création de dossier par "distance de capture" (sous-classes) (2j)

---

## 🧪 EPIC 2 : Pipeline de Préparation & Qualité (3-4 semaines)

### TASK 2.1 : Uniformisation Technique (CRISP-DM Phase 3)
*   **Sub-task 2.1.1 :** Standardisation des résolutions & formats d'images (3j)
*   **Sub-task 2.1.2 :** Normalisation des noms de fichiers (1j)
*   **Sub-task 2.1.3 :** Tri manuel pour validation du zoom (Validation Humaine) (7j)

### TASK 2.2 : Annotation & Augmentation
*   **Sub-task 2.2.1 :** Importation dans l'outil d'annotation (ex: Roboflow) (2j)
*   **Sub-task 2.2.2 :** Configuration de la Data Augmentation (simuler photos mobiles) (3j)
*   **Sub-task 2.2.3 :** Vérification des biais (couleurs de peau) (4j)

---

## 🧠 EPIC 3 : Modélisation & Entraînement IA (4-6 semaines)

### TASK 3.1 : Entraînement & Expérimentation (CRISP-DM Phase 4)
*   **Sub-task 3.1.1 :** Configuration de l'environnement (Kaggle/Colab) (2j)
*   **Sub-task 3.1.2 :** Entraînement modèles (EfficientNet, MobileNetV3) (10j)
*   **Sub-task 3.1.3 :** Fine-tuning sur les maladies tropicales spécifiques (7j)

### TASK 3.2 : Évaluation & Compression (CRISP-DM Phase 5)
*   **Sub-task 3.2.1 :** Analyse de la matrice de confusion (Précision/Rappel) (3j)
*   **Sub-task 3.2.2 :** Conversion & Optimisation au format TensorFlow Lite (.tflite) (4j)
*   **Sub-task 3.2.3 :** Validation des performances sur matériel cible (Android/iOS) (5j)

---

## 📱 EPIC 4 : Application Mobile Flutter (4-6 semaines)

### TASK 4.1 : Interface Utilisateur (Agile Sprint 1 & 2)
*   **Sub-task 4.1.1 :** UI Prise de photo avec guide de distance (Overlay caméra) (5j)
*   **Sub-task 4.1.2 :** Écran de résultats & recommandations médicales (5j)

### TASK 4.2 : Intégration IA & Cloud (Agile Sprint 3)
*   **Sub-task 4.2.1 :** Intégration moteur d'inférence TFLite (Offline) (7j)
*   **Sub-task 4.2.2 :** API Cloud pour traduction en Malgache (si réseau) (5j)

---

## 🚀 EPIC 5 : Déploiement & Feedback Terrain (2-3 semaines)

### TASK 5.1 : Tests finaux & Livraison (CRISP-DM Phase 6)
*   **Sub-task 5.1.1 :** Phase BETA avec médecins testeurs (10j)
*   **Sub-task 5.1.2 :** Correction des bugs critiques (5j)
*   **Sub-task 5.1.3 :** Publication sur les stores ou déploiement APK (2j)

---

### 📊 Estimation Totale du Projet : **15 à 22 Semaines** (Environ 4-5 mois)
*   **Ressources :** 1 ML Engineer, 1 Flutter Dev, 1 Expert Médical (Ponctuel).
