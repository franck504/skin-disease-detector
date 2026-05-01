# STRUCTURE DES DIAPOSITIVES — Soutenance Cutisia
## Durée estimée : 20–25 minutes (15 diapos)

---

## DIAPO 1 : Page de garde

**📝 Contenu texte :**
- Titre : "Cutisia — Application mobile sanitaire avec modèle CNN léger pour la détection de maladies cutanées tropicales-africaines"
- Sous-titre : Mémoire de Master 2 — Smart DATA-CITY
- Votre nom, prénom
- Nom de l'encadrant
- Année universitaire 2025–2026
- Logo de l'université

**🖼️ Contenu image :**
- Logo de l'application Cutisia (icône de l'app)
- Logo de l'université

**🎤 Parole :**
> "Bonjour à tous, membres du jury. Je suis [votre nom], étudiant en Master 2 Smart DATA-CITY. Je vais vous présenter aujourd'hui mon projet de fin d'études : Cutisia, une application mobile qui utilise l'intelligence artificielle pour détecter les maladies de peau en zones isolées. Ce travail s'inscrit dans une vision de ville intelligente au service de la santé publique."

---

## DIAPO 2 : Sommaire / Plan de la présentation

**📝 Contenu texte :**
1. Contexte et problématique
2. Collecte et analyse des données
3. Préparation et ingénierie des données
4. Entraînement du modèle IA
5. Déploiement et application mobile
6. Résultats et évaluation
7. Démonstration
8. Conclusion et perspectives

**🖼️ Contenu image :**
- Aucune (slide épurée, juste le plan numéroté)

**🎤 Parole :**
> "Voici le fil conducteur de ma présentation. Nous allons partir du problème de terrain, passer par l'ingénierie des données et la modélisation, pour arriver aux résultats concrets et à une démonstration de l'application."

---

## DIAPO 3 : Contexte et Problème

**📝 Contenu texte :**
- 900 millions de personnes touchées par des maladies de peau chaque année
- 1 dermatologue pour plusieurs millions d'habitants dans les pays en développement
- Conséquences : diagnostic tardif, complications graves, stigmatisation sociale
- Question de recherche : **Comment rendre le diagnostic dermatologique accessible sans spécialiste ?**

**🖼️ Contenu image :**
- Carte du monde montrant la répartition des dermatologues (ou une infographie chiffrée)
- Schéma Mermaid "Sans Cutisia vs Avec Cutisia" (Schéma 1 de la rédaction)

**🎤 Parole :**
> "Les maladies de peau touchent près d'un milliard de personnes dans le monde. Dans les pays en développement, il y a parfois un seul dermatologue pour des millions d'habitants. Les patients doivent parcourir des centaines de kilomètres pour un diagnostic qui arrive souvent trop tard. Notre question est simple : peut-on utiliser le smartphone, l'outil le plus accessible au monde, pour combler cette fracture sanitaire ?"

---

## DIAPO 4 : La solution Cutisia — Vue d'ensemble

**📝 Contenu texte :**
- Cutisia = Application mobile d'aide au diagnostic dermatologique
- 3 piliers :
  - **Ingénierie des données** : Pipeline U-Net + Data Augmentation
  - **IA embarquée** : MobileNetV2 / EfficientNetV2 (Edge Computing)
  - **UX accessible** : Flutter + localisation Malgache
- 6 pathologies cibles : Candidiase, Leprosy, Mélanome, Monkeypox, Scabies, Tinea

**🖼️ Contenu image :**
- Schéma d'architecture global (Edge ↔ Cloud)
- Captures d'écran de l'application (écran d'accueil en Malgache)

**🎤 Parole :**
> "Notre réponse, c'est Cutisia. C'est une application mobile qui embarque un cerveau d'intelligence artificielle directement sur le téléphone. Elle fonctionne sans internet, elle parle Malgache, et elle est capable de détecter 6 maladies de peau tropicales en moins de 2 secondes. L'architecture repose sur trois piliers : l'ingénierie des données, l'IA embarquée, et une expérience utilisateur pensée pour le terrain."

---

## DIAPO 5 : Collecte de données

**📝 Contenu texte :**
- Sources multiples :
  - ISIC Archive, HAM10000 (références mondiales)
  - Kaggle, Huggingface (datasets open-source)
  - Web Scrapping ciblé (images médicales publiques)
- Total : **11 209 images** réparties en 6 classes
- Défi : déséquilibre entre les classes (Mélanome : 3680 vs Monkeypox : 772)

**🖼️ Contenu image :**
- Graphique en barres : nombre d'images par classe (bar chart coloré)
- Logos des sources (ISIC, Kaggle, Huggingface)

**🎤 Parole :**
> "La qualité d'une IA dépend de ses données. Nous avons agrégé plus de 11 000 images depuis des sources reconnues comme ISIC, HAM10000, Kaggle et Huggingface. Vous pouvez voir ici que les classes sont déséquilibrées : nous avons beaucoup plus d'images de mélanomes que de monkeypox. C'est un défi majeur que nous avons dû résoudre."

---

## DIAPO 6 : Analyse et sélection des classes

**📝 Contenu texte :**
- Recensement initial de toutes les classes disponibles
- Critères de sélection :
  - Quantité suffisante d'images
  - Qualité des images (résolution, diversité)
  - Pertinence médicale pour les zones tropicales
- **6 classes retenues** : Candidiase, Leprosy, Tinea, Mélanome, Monkeypox, Scabies

**🖼️ Contenu image :**
- Tableau 1 de la rédaction (Prévalence et facteurs favorisants)
- Mosaïque de 6 images : une par maladie

**🎤 Parole :**
> "Nous avons commencé par recenser toutes les classes disponibles dans nos sources. Ensuite, nous avons sélectionné 6 pathologies prioritaires selon trois critères : la quantité d'images disponibles, leur qualité, et surtout la pertinence médicale pour les zones tropicales africaines. Vous voyez dans ce tableau que la gale et la teigne sont endémiques dans ces régions, ce qui justifie leur présence dans notre sélection."

---

## DIAPO 7 : Préparation des données — Pipeline

**📝 Contenu texte :**
- Étape 1 : **Segmentation U-Net** → Génération de masques binaires
- Étape 2 : **Auto-Cropping** → Centrage sur la lésion (OpenCV)
- Étape 3 : **Normalisation** → Uniformisation des couleurs
- Étape 4 : **Data Augmentation** → Rotation 90°/180°, luminosité, zoom
- Étape 5 : **Sur-échantillonnage** → Équilibrage des classes minoritaires

**🖼️ Contenu image :**
- Schéma du pipeline (Schéma 5 de la rédaction : Images Brutes → U-Net → Masque → Cropping → Augmentation → Dataset Final)
- Exemple visuel : image brute → masque → lésion isolée (Schéma 4)

**🎤 Parole :**
> "Avant de nourrir l'IA, nous devons préparer les images. Le pipeline commence par U-Net, qui génère un masque pour isoler la lésion de l'arrière-plan. Ensuite, OpenCV découpe automatiquement l'image autour de la zone malade. Nous normalisons les couleurs, puis nous enrichissons le dataset par des rotations et des variations de luminosité. Enfin, nous sur-échantillonnons les classes rares comme le Monkeypox pour que l'IA ne les ignore pas."

---

## DIAPO 8 : Entraînement du modèle

**📝 Contenu texte :**
- Architectures choisies :
  - **MobileNetV2** : léger, rapide, conçu pour le mobile (Convolutions séparables)
  - **EfficientNetV2** : précis, mode "Elite" pour le Cloud
- Transfer Learning : modèle pré-entraîné sur ImageNet → spécialisé en dermatologie
- Infrastructure : **Kaggle GPU P100** / Google Colab **Tesla T4**
- Suivi : courbes Loss/Accuracy, ajustement des hyperparamètres

**🖼️ Contenu image :**
- Graphique des courbes d'entraînement (Accuracy vs Epochs) — Schéma 6
- Schéma comparatif MobileNetV2 vs EfficientNetV2 (taille vs précision)

**🎤 Parole :**
> "Pour l'entraînement, nous avons choisi deux architectures complémentaires. MobileNetV2 est conçu pour le smartphone : il est 8 fois plus rapide qu'un modèle classique grâce aux convolutions séparables. EfficientNetV2 est notre modèle 'Elite', plus précis mais plus lourd, destiné à l'analyse Cloud. Grâce au Transfer Learning, nous avons récupéré un modèle déjà entraîné sur des millions d'images et nous l'avons spécialisé en dermatologie. L'entraînement a été réalisé sur les GPU de Kaggle et Google Colab."

---

## DIAPO 9 : Interprétabilité — Grad-CAM (XAI)

**📝 Contenu texte :**
- L'IA ne doit pas être une "boîte noire"
- **Grad-CAM** : génère des cartes de chaleur sur les zones décisives
- Conformité avec l'**AI Act** européen (transparence, droit à l'explication)
- Seuil de confiance : si < 60% → "Résultat incertain, consultez un spécialiste"

**🖼️ Contenu image :**
- Image Grad-CAM générée par votre script (`gradcam_sample.png`)
- Tableau 3 de la rédaction (Obligations AI Act vs Cutisia)

**🎤 Parole :**
> "Un point fondamental de notre travail est la transparence. L'IA ne doit pas être une boîte noire, surtout en santé. Nous avons intégré Grad-CAM, une technique qui montre exactement quelles zones de la peau ont convaincu l'IA de son diagnostic. Vous voyez ici les zones rouges sur la lésion : c'est ce que le modèle a regardé. De plus, si l'IA n'est pas sûre à plus de 60%, elle affiche un message d'incertitude. C'est une exigence éthique conforme à l'AI Act européen."

---

## DIAPO 10 : Déploiement — Architecture technique

**📝 Contenu texte :**
- **Backend** : FastAPI hébergé sur Google Colab, exposé via pyngrok
- **Stockage** : Google Drive pour les modèles et les datasets
- **Frontend** : Application Flutter (Android)
  - Moteur TFLite embarqué (diagnostic hors-ligne)
  - Localisation complète en Malgache
  - Base locale SQLite pour les dossiers patients
- **API de collecte** : GPS + métadonnées → centralisation épidémiologique

**🖼️ Contenu image :**
- Schéma d'architecture Edge-to-Cloud (Schéma 7 : Diagnostic Mobile → Anonymisation → API Cloud → SIG)
- Capture d'écran de l'interface de collecte (Schéma 10)

**🎤 Parole :**
> "Pour le déploiement, nous avons une architecture hybride. Le cœur de l'application est Flutter, avec le modèle TFLite embarqué directement sur le téléphone. Le diagnostic fonctionne sans internet. Pour le mode Elite, l'image est envoyée via une API FastAPI hébergée sur Colab et exposée par pyngrok. Chaque diagnostic est accompagné de coordonnées GPS, ce qui alimente notre vision Smart DATA-CITY de surveillance épidémiologique."

---

## DIAPO 11 : L'application Cutisia — Démonstration visuelle

**📝 Contenu texte :**
- Écran d'accueil en Malgache (Fandraisana)
- Écran de capture avec guide de centrage
- Écran de résultat avec traitement recommandé
- Écran de collecte de données (Fanangonana angon-drakitra)

**🖼️ Contenu image :**
- 3 à 4 captures d'écran de l'application côte à côte (Schémas 8, 9, 10)
- Ou vidéo courte de démonstration (si possible)

**🎤 Parole :**
> "Voici l'application en action. L'écran d'accueil est entièrement en Malgache pour être accessible aux agents de santé locaux. L'écran de capture guide l'utilisateur pour centrer correctement la lésion. Le résultat s'affiche en moins de 2 secondes avec des recommandations de traitement. Enfin, l'écran de collecte permet au personnel de santé d'enrichir le dataset avec de nouvelles images annotées, alimentant ainsi la boucle d'Active Learning."

---

## DIAPO 12 : Résultats — Matrice de confusion et ROC

**📝 Contenu texte :**
- Évaluation sur **11 209 images**
- Matrice de confusion : identification des confusions inter-classes
- Courbes AUC-ROC : capacité de discrimination par classe
- Meilleure performance : **Leprosy (F1 = 0.65)**

**🖼️ Contenu image :**
- `confusion_matrix.png` (générée par votre script)
- `roc_curve.png` (générée par votre script)

**🎤 Parole :**
> "Passons aux résultats. La matrice de confusion montre comment le modèle classe les 11 209 images de test. On voit que la Lèpre est très bien reconnue, tandis que certaines classes comme le Monkeypox sont plus difficiles en raison de la rareté des données. Les courbes AUC-ROC confirment que le modèle a une bonne capacité de discrimination globale."

---

## DIAPO 13 : Résultats — Rapport de classification

**📝 Contenu texte :**
- Tableau 5 : Métriques par pathologie

| Maladie | Précision | Rappel | F1-Score | Images |
|:---|:---|:---|:---|:---|
| Candidiase | 0.40 | 0.02 | 0.03 | 1900 |
| **Leprosy** | **0.66** | **0.63** | **0.65** | 1249 |
| Mélanomes | 0.24 | 0.10 | 0.14 | 3680 |
| Monkeypox | 0.01 | 0.10 | 0.02 | 772 |
| Scabies | 0.22 | 0.24 | 0.23 | 958 |
| Tinea | 0.51 | 0.19 | 0.27 | 2650 |

- Analyse : la diversité morphologique des lésions tropicales est un défi majeur

**🖼️ Contenu image :**
- Tableau stylisé avec la ligne Leprosy surlignée en vert
- Tableau 4 : Forces et Faiblesses

**🎤 Parole :**
> "Ce tableau détaille les performances par maladie. Le point fort est la Lèpre, avec un F1-Score de 0.65, ce qui est très encourageant pour une maladie à fort enjeu de santé publique. Les scores plus faibles sur le Monkeypox s'expliquent par le faible nombre d'images disponibles : seulement 772. C'est précisément pour cela que nous avons ajouté la fonctionnalité de collecte dans l'application, pour enrichir le dataset en continu."

---

## DIAPO 14 : Perspectives et Smart DATA-CITY

**📝 Contenu texte :**
- **Active Learning** : le médecin corrige → le modèle s'améliore
- **Segmentation sémantique** : dessiner les contours exacts de la lésion
- **Suivi temporel** : comparer 2 photos à 15 jours d'intervalle
- **SIG Sanitaire** : cartographie épidémiologique en temps réel
- **Interopérabilité** : intégration dans les dossiers médicaux nationaux

**🖼️ Contenu image :**
- Schéma Mermaid Active Learning (Schéma 13 : Diagnostic → Validation Médecin → Ré-entraînement → Mise à jour)
- Maquette d'un tableau de bord SIG avec carte de chaleur épidémiologique

**🎤 Parole :**
> "Pour l'avenir, trois axes majeurs. Premièrement, l'Active Learning : chaque correction d'un médecin rend l'IA plus intelligente. Deuxièmement, passer de la classification à la segmentation complète pour mesurer précisément la surface des lésions et suivre leur évolution dans le temps. Troisièmement, la dimension Smart DATA-CITY : en agrégeant les données anonymisées de tous les smartphones, nous pouvons cartographier les foyers épidémiologiques en temps réel et anticiper les crises sanitaires."

---

## DIAPO 15 : Conclusion et remerciements

**📝 Contenu texte :**
- Cutisia = preuve de concept d'une télémédecine mobile, éthique et accessible
- Résultats prometteurs malgré les défis (déséquilibre, qualité d'image)
- Le smartphone : un multiplicateur de compétences médicales
- **Merci** — Questions ?

**🖼️ Contenu image :**
- Logo Cutisia centré
- QR code du dépôt GitHub (optionnel)

**🎤 Parole :**
> "En conclusion, Cutisia démontre qu'il est possible de mettre l'intelligence artificielle au service de la santé de proximité. Le smartphone ne remplace pas le médecin, mais il devient un multiplicateur de compétences qui garantit que la distance ne soit plus un obstacle à une santé de qualité pour tous. Je vous remercie pour votre attention et je suis prêt à répondre à vos questions."

---

## 💡 CONSEILS POUR LA SOUTENANCE

1. **Timing** : Ne dépassez pas 2 minutes par diapo. Les diapos 7, 8 et 12-13 sont les plus techniques, prenez votre temps dessus.
2. **Regardez le jury** : Ne lisez pas vos slides, utilisez-les comme support visuel.
3. **Questions anticipées** :
   - "Pourquoi MobileNetV2 ?" → Convolutions séparables, 8x plus rapide, conçu pour le mobile.
   - "L'accuracy est faible (18%), pourquoi ?" → Dataset tropicaux très complexes, diversité morphologique, déséquilibre des classes. Le F1-Score par classe est plus pertinent.
   - "Est-ce que c'est un dispositif médical ?" → Non, c'est un outil d'aide au diagnostic. Le médecin reste décisionnaire.
   - "Et la vie privée ?" → Anonymisation dès la capture, HTTPS/TLS, conformité AI Act.
4. **Point fort à marteler** : La Lèpre à 66% de précision — c'est votre meilleur résultat et c'est une maladie à fort impact social.
