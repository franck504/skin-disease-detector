Voici la structure complète de votre présentation, diapositive par diapositive :

---

## 🎯 Structure de présentation — 12 diapositives

---

### **Diapo 1 — Titre / Couverture**

**Contenu texte :**
- Titre : *Détection de maladies cutanées tropicales-africaines*
- Sous-titre : *Application mobile sanitaire à base d'un modèle CNN léger*
- Auteur(s), institution, date

**Contenu image :**
- Illustration stylisée d'un smartphone affichant une analyse de peau sur fond médical (carte d'Afrique en arrière-plan, tons vert médical + bleu profond)

**Parole à dire :**
> *"Bonjour à tous. Aujourd'hui, je vais vous présenter un projet qui se situe à l'intersection de l'intelligence artificielle, de la santé publique et du mobile. L'idée centrale : détecter les maladies cutanées tropicales grâce à une application accessible depuis un simple smartphone."*

---

### **Diapo 2 — Contexte et problème**

**Contenu texte :**
- Faible accès aux dermatologues en Afrique subsaharienne
- Maladies cutanées fréquentes mais souvent mal diagnostiquées
- Besoin d'un outil de pré-diagnostic rapide, léger, hors-ligne
- Question : *Comment rendre le diagnostic cutané accessible à tous ?*

**Contenu image :**
- Deux colonnes : à gauche une icône "médecin manquant" (ratio médecin/population), à droite une carte de chaleur Afrique montrant la densité de dermatologues (faible)

**Parole à dire :**
> *"En Afrique, l'accès à un dermatologue est un luxe. Des maladies comme la lèpre, la gale ou le monkeypox sont diagnostiquées trop tard. Notre question : peut-on entraîner un modèle léger, embarqué sur mobile, pour aider au pré-diagnostic ?"*

---

### **Diapo 3 — Collecte des données**

**Contenu texte :**
- Sources utilisées :
  - ISIC Archive
  - HAM10000
  - Kaggle
  - Hugging Face
  - Web Scraping ciblé
- Volume total collecté (à préciser selon vos chiffres)

**Contenu image :**
- Logos des 5 sources arrangés en cercle ou grille avec une flèche convergente vers "Dataset brut"
- Badge indiquant le nombre total d'images

**Parole à dire :**
> *"Pour construire notre dataset, nous avons combiné plusieurs sources reconnues : ISIC, HAM10000, Kaggle, Hugging Face, et du web scraping pour les maladies africaines sous-représentées. La diversité des sources était essentielle pour couvrir nos 6 classes cibles."*

---

### **Diapo 4 — Analyse des données**

**Contenu texte :**
- Recensement de toutes les classes identifiées
- Harmonisation des noms de classes (dédoublonnage)
- Statistiques : nombre d'images par classe
- Problème d'équilibre des classes identifié

**Contenu image :**
- Graphique à barres (bar chart) horizontal montrant le nombre d'images par classe, avec mise en évidence des classes déséquilibrées en rouge/orange

**Parole à dire :**
> *"Une fois les données collectées, nous avons fait un inventaire complet. Plusieurs noms désignaient la même maladie selon les sources. Après unification, nous avons visualisé la distribution — et constaté un fort déséquilibre entre classes, ce qui a guidé nos choix."*

---

### **Diapo 5 — Sélection des 6 classes**

**Contenu texte :**
- Critères de sélection : quantité suffisante + qualité d'images + pertinence clinique tropicale
- Les 6 classes retenues :
  1. 🦠 Monkeypox
  2. 🤝 Lèpre (Leprosy)
  3. 🍄 Teigne (Tinea)
  4. 🔵 Candidose
  5. ⚠️ Mélanome
  6. 🪲 Gale (Scabies)

**Contenu image :**
- Grille 2×3 avec une photo d'exemple (propre, médicale) de chaque maladie + son nom en étiquette

**Parole à dire :**
> *"Parmi toutes les classes disponibles, nous en avons retenu 6 selon deux critères : la qualité et la quantité des données disponibles, et leur pertinence dans le contexte sanitaire africain. Ces 6 maladies représentent des affections fréquentes, graves, et souvent confondues visuellement."*

---

### **Diapo 6 — Préparation & Prétraitement**

**Contenu texte :**
- Normalisation / standardisation :
  - Architecture U-Net pour la segmentation
  - OpenCV : rognage, génération de masques, zoom
- Augmentation des données :
  - Rotations 90° / 180°
  - Variation de luminosité
  - Recadrage aléatoire

**Contenu image :**
- Pipeline visuel horizontal : Image brute → Masque U-Net → Image traitée → Images augmentées (×4 variantes)

**Parole à dire :**
> *"La préparation des données est une étape critique. Nous avons utilisé U-Net pour isoler les lésions du fond de l'image, et OpenCV pour standardiser les tailles. L'augmentation artificielle — rotations, variations de lumière, rognage — nous a permis d'équilibrer et d'enrichir le dataset."*

---

### **Diapo 7 — Architecture du modèle**

**Contenu texte :**
- Deux candidats évalués :
  - **MobileNetV2** — ultra-léger, adapté mobile
  - **EfficientNetV2** — meilleur équilibre précision/taille
- Entraînement sur Kaggle (GPU P100)
- Transfer Learning depuis ImageNet
- Métriques : Accuracy, F1-score, Matrice de confusion

**Contenu image :**
- Comparaison visuelle côte-à-côte : taille du modèle (Mo), accuracy, vitesse d'inférence (ms) — sous forme de tableau ou radar chart

**Parole à dire :**
> *"Pour le cœur de notre système, nous avons comparé MobileNetV2 et EfficientNetV2. Ces deux architectures sont conçues pour être légères et efficaces sur mobile. Nous avons entraîné les modèles sur Kaggle avec un GPU P100, en exploitant le transfer learning pour gagner du temps et de la performance."*

---

### **Diapo 8 — Résultats du modèle**

**Contenu texte :**
- Accuracy globale obtenue : XX%
- F1-score par classe (tableau ou graphique)
- Matrice de confusion
- Modèle retenu : [MobileNetV2 / EfficientNetV2]

**Contenu image :**
- Matrice de confusion colorée (heatmap) + graphique F1 par classe en barres

**Parole à dire :**
> *"Voici nos résultats. Le modèle [X] a atteint une accuracy de XX% sur le jeu de test. La matrice de confusion révèle que les confusions les plus fréquentes se font entre [X] et [Y], ce qui est cohérent cliniquement. Ces performances sont satisfaisantes pour un modèle embarqué sur mobile."*

---

### **Diapo 9 — Architecture de déploiement**

**Contenu texte :**
- Backend : **FastAPI** (Python)
- Environnement serveur : Google Colab
- Exposition de l'API : **pyngrok**
- Stockage des images/modèles : **Google Drive**
- Frontend : **Flutter** (application mobile cross-platform)

**Contenu image :**
- Schéma d'architecture système : Mobile Flutter → API FastAPI (Colab) → Modèle CNN → Résultat retourné, avec icônes et flèches

**Parole à dire :**
> *"Pour le déploiement, nous avons opté pour une stack légère et accessible. FastAPI expose notre modèle en tant qu'API REST, hébergée sur Google Colab et accessible via pyngrok. Le frontend Flutter communique avec cette API et affiche le diagnostic à l'utilisateur en quelques secondes."*

---

### **Diapo 10 — Démonstration**

**Contenu texte :**
- Capture d'écran ou GIF de l'application Flutter
- Étapes : Prise de photo → Envoi → Résultat affiché
- Temps de réponse moyen

**Contenu image :**
- Mockup de smartphone montrant l'interface Flutter avec un exemple de résultat (ex : "Monkeypox détecté — confiance : 87%")

**Parole à dire :**
> *"Voici l'application en action. L'utilisateur prend une photo de la lésion, l'envoie via l'app. En quelques secondes, le modèle retourne sa prédiction avec un niveau de confiance. L'interface est volontairement simple pour être utilisable même par des agents de santé communautaires."*

---

### **Diapo 11 — Amélioration continue du dataset**

**Contenu texte :**
- Fonctionnalité de collecte participative :
  - Photo de la lésion
  - Pays, âge, sexe
  - Nom de la maladie (label)
  - Coordonnées GPS
- Objectif : créer un dataset africain natif et évolutif

**Contenu image :**
- Schéma "data flywheel" : Utilisateur → Collecte → Dataset enrichi → Modèle amélioré → Meilleur diagnostic → retour vers Utilisateur

**Parole à dire :**
> *"Un point fort de ce projet : l'application intègre une fonctionnalité de collecte de données. Chaque utilisation peut enrichir notre dataset avec des informations contextuelles — pays, GPS, profil du patient — ce qui nous permettra d'entraîner des versions futures sur des données africaines réelles, de plus en plus représentatives."*

---

### **Diapo 12 — Conclusion & Perspectives**

**Contenu texte :**
- ✅ Modèle CNN léger fonctionnel sur mobile
- ✅ 6 maladies tropicales détectables
- ✅ Pipeline de collecte continue intégré
- 🔜 Perspectives : validation clinique, partenariats ONG/ministères, extension à d'autres maladies

**Contenu image :**
- Visuel fort : smartphone + stéthoscope + carte d'Afrique, avec la phrase *"L'IA au service de la santé pour tous"*

**Parole à dire :**
> *"En conclusion, ce projet démontre qu'il est possible de déployer un outil d'IA médicale léger, accessible et évolutif pour des contextes à ressources limitées. Les prochaines étapes sont la validation clinique et l'extension du dataset. Notre ambition : faire de cette application un outil de santé publique concret, au service des populations africaines."*

---

Souhaitez-vous que je génère directement le fichier `.pptx` correspondant à cette structure ?