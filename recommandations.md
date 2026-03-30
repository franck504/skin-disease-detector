# Recommandations Stratégiques - Projet Cutisia (IA Médicale)

Ce document récapitule les observations critiques effectuées lors de la phase de préparation des données et les recommandations pour la phase d'entraînement (Deep Learning).

## 1. Équilibre du Dataset (Data Balancing)

> [!IMPORTANT]
> **Observation :** Le dataset est fortement déséquilibré. Les **Mélanomes (4068 images)** et la **Tinea (2650 images)** dominent largement, tandis que d'autres classes comme Monkeypox (772) sont plus faibles.
> 
> **Action entreprise :** Nous avons **éliminé** les classes *Cellulite* (49) et *Impétigo* (72) car leur volume était trop faible pour garantir une précision médicale acceptable.
> 
> **Recommandation :** Utiliser des **Class Weights** (poids de classes) lors de l'entraînement pour donner plus d'importance aux erreurs sur les classes minoritaires (Monkeypox, Scabies).

## 2. Qualité et Résolution des Images

> [!NOTE]
> **Observation :** La résolution moyenne est excellente (> 500px), mais hétérogène (de 170px à 2400px).
> 
> **Recommandation 1 (Resizing) :** Normaliser toutes les images en **224x224 pixels** avant l'entrée dans le modèle (standard MobileNetV3).
> **Recommandation 2 (Augmentation) :** Appliquer une **Data Augmentation massive** (rotations, symétries, variations de zoom et de contraste) pour compenser les petites résolutions et augmenter artificiellement la diversité des cas.

## 3. Infrastructure & Stockage

> [!CAUTION]
> **Observation :** Le stockage local est limité (saturation à 100% lors de la migration). Les liens symboliques (Symlinks) ne sont pas compatibles avec Google Drive/Colab.
> 
> **Décision technique :** Nous avons opté pour une **Migration Physique** (déplacement des fichiers) dans un dossier unique `datasets-cutisia/`.
> 
> **Recommandation :** Toujours zipper ce dossier avant l'upload pour éviter les erreurs de transfert de fichiers individuels (plus de 11 000 images).

## 4. Prochaines Étapes Techniques

1. **Phase de Validation** : Effectuer une passe manuelle rapide sur les dossiers pour supprimer d'éventuels fichiers non-médicaux (logos, textes).
2. **Setup Colab** : Utiliser un environnement GPU (T4 ou A100) pour l'entraînement.
3. **Format Mobile** : Prévoir la conversion finale du modèle en `.tflite` pour l'intégration Flutter.

---
**Document établi le : 26 Mars 2026**
