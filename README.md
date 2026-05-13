# Cutisia - Système d'Assistance au Diagnostic Dermatologique

Cutisia est une plateforme complète utilisant l'intelligence artificielle pour assister le personnel de santé dans le diagnostic de maladies cutanées tropicales. Le système combine une application mobile pour le diagnostic de terrain et une infrastructure cloud pour des analyses de haute précision.

## Structure du Projet

Le projet est organisé en trois composantes principales :

- **backend/** : Logique serveur, API REST et scripts d'entraînement IA.
- **cutisia/** : Application mobile développée avec Flutter.
- **livre_memoire/** : Documentation académique et rapports techniques.

## Fonctionnalités Principales

- **Segmentation de lésions** : Isolation automatique de la zone affectée via un modèle U-Net (backbone ResNet34).
- **Classification multi-classes** : Diagnostic parmi 6 pathologies (Lèpre, Monkeypox, Mélanomes, etc.) via EfficientNetV2-L.
- **Mode Hybride** : Inférence locale (TFLite) pour la rapidité et mode Cloud pour la précision maximale.
- **Collecte de données** : Point d'accès sécurisé pour l'archivage de nouveaux cas cliniques.

## Installation et Configuration

### Prérequis

- Python 3.10 ou supérieur
- Flutter SDK (pour l'application mobile)
- Un compte Ngrok (optionnel, pour l'exposition de l'API)

### Installation du Backend

1. Clonez le dépôt et accédez au répertoire racine.
2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/macOS
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Configurez les variables d'environnement :
   ```bash
   cp .env.example .env
   # Modifiez le fichier .env avec vos propres paramètres
   ```

## Utilisation de l'API

Le serveur API est le cœur du système Cloud.

### Démarrage

```bash
python -m backend.api.main
```

### Points d'accès (Endpoints)

- **GET /** : Vérifie l'état de santé du serveur.
- **POST /predict** : Soumission d'une image pour diagnostic.
  - Paramètre : `file` (image)
  - Réponse : Classe prédite, score de confiance et détails.
- **POST /collect** : Envoi de données terrain.
  - Paramètres : `file` (image), `metadata` (JSON string).

## Entraînement et Évaluation

Des scripts utilitaires sont disponibles dans `backend/scripts/` :

- `audit_dataset.py` : Analyse statistique des données disponibles.
- `generate_masks.py` : Génération des masques de segmentation.
- `train_dual_models.py` : Lancement du cycle d'entraînement complet.
- `evaluate_and_visualize.py` : Génération des métriques de performance.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
