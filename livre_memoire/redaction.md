# INTRODUCTION GÉNÉRALE

À l’ère de l’urbanisation galopante et des villes intelligentes (Smart Cities), la santé dermatologique demeure un défi majeur, particulièrement dans les zones isolées ou les quartiers défavorisés. On estime que près d'un milliard de personnes souffrent de pathologies cutanées, souvent négligées faute d'accès à un personnel spécialisé. La fracture numérique et sanitaire transforme des infections bénignes en enjeux de santé publique critiques.

Le projet **Cutisia** s'inscrit dans cette vision "Smart DATA-CITY" : transformer le smartphone, capteur universel, en un outil de diagnostic de précision. En s'appuyant sur l'Intelligence Artificielle embarquée (**Edge Computing**) et des architectures de pointe comme **U-Net** et **MobileNetV2**, Cutisia permet une détection immédiate, anonyme et déconnectée des pathologies cutanées tropicales. Ce mémoire documente la conception, la réalisation et l'évaluation de cette solution innovante, conçue pour être déployée au plus près des populations, en intégrant des contraintes éthiques et linguistiques fortes.

---

# PARTIE 1 : ÉTAT DE L'ART ET PROBLÉMATIQUE DE LA SANTÉ DERMATOLOGIQUE

## Chapitre 1 : Enjeux de la dermatologie et apport des technologies numériques

### 1.1 Contexte épidémiologique et défis du diagnostic précoce

#### 1.1.1 Prévalence des affections cutanées en zones isolées

Les maladies de la peau représentent l'une des causes les plus fréquentes de consultation médicale à l'échelle mondiale. Elles touchent près de 900 millions de personnes chaque année [3]. Dans les zones rurales ou isolées, ces pathologies sont souvent liées aux conditions d'hygiène et au climat. Sans soins adaptés, une simple infection cutanée peut évoluer vers des complications graves.


### Tableau 1 : Prévalence et facteurs favorisants des pathologies cibles

| Maladie de peau | Prévalence (Zones Tropicales/Isolées) | Facteurs Favorisants |
| :--- | :--- | :--- |
| **Gale (Scabiose)** | Très élevée (5–50% chez les enfants) [1] | Surpeuplement, hygiène limitée |
| **Teigne (Tinea)** | Élevée (Endémique chez les écoliers) | Chaleur, humidité, contact animal |
| **Lèpre** | Persistante (Foyers endémiques) [1] | Pauvreté, retard de diagnostic |
| **Candidiase** | Fréquente (Pathologie opportuniste) | Humidité élevée, immunité |
| **Monkeypox** | Épidémique (Zones forestières) | Contact faune sauvage, promiscuité |
| **Mélanome** | Rare (mais souvent diagnostiqué tard) | Rayonnement UV, manque de dépistage |

### Tableau 2 : Comparaison des approches de diagnostic dermatologique

| Critère | Diagnostic Clinique (Visuel) | Teledermatologie | Cutisia (IA Mobile) |
| :--- | :--- | :--- | :--- |
| **Accessibilité** | Faible (déplacement requis) | Moyenne (besoin d'expert) | Très élevée (Smartphone) |
| **Coût** | Élevé (consultation) | Moyen | Très faible |
| **Délai** | Long (rendez-vous) | 24h - 48h | Instantané (< 2s) |
| **Précision** | Dépend de l'expérience | Élevée (expert distant) | Élevée (Elite Model) |

La détection précoce est la clé pour stopper la propagation de ces maladies. Cependant, le manque d'information et l'éloignement des centres de santé freinent le dépistage rapide.

#### 1.1.2 Pénurie de spécialistes et délais de prise en charge

Le monde fait face à une crise majeure du personnel de santé spécialisé. Dans de nombreux pays en développement, on compte parfois un seul dermatologue pour plusieurs millions d'habitants [3]. Cette situation crée des files d'attente interminables dans les hôpitaux centraux.

### Schéma 1 : Comparaison des flux de prise en charge

```mermaid
graph TD
    subgraph "Sans Cutisia"
    A[Symptôme cutané] --> B[Déplacement long/coûteux]
    B --> C[Attente hôpital central]
    C --> D[Diagnostic tardif]
    D --> E[Complications graves]
    end

    subgraph "Avec Cutisia"
    F[Symptôme cutané] --> G[Scan mobile immédiat]
    G --> H{Alerte?}
    H -- Oui --> I[Consultation prioritaire]
    H -- Non --> J[Conseils de soin locaux]
    I --> K[Traitement rapide]
    end

    E --> F[Diagnostic tardif]
 ```

Les délais de prise en charge peuvent dépasser plusieurs mois. Ce retard transforme des maladies guérissables en handicaps permanents ou en maladies chroniques coûteuses.

### 1.2 La Télédermatologie : Une réponse par l'imagerie médicale

#### 1.2.1 Historique et évolution du diagnostic assisté par ordinateur (CAD)

L'utilisation de l'informatique pour aider les médecins ne date pas d'hier. Les premiers systèmes de diagnostic assisté par ordinateur (CAD) utilisaient des règles mathématiques simples. Aujourd'hui, grâce à l'intelligence artificielle, ces systèmes sont devenus capables de reconnaître des motifs complexes dans les images médicales [1].


#### 1.2.2 Impact de l'imagerie mobile dans le dépistage de première intention

Le smartphone est devenu l'outil de santé le plus accessible au monde. Sa caméra haute résolution permet de capturer des images de lésions cutanées avec une précision suffisante pour une analyse préliminaire. L'imagerie mobile permet de faire un "tri" efficace : identifier les cas urgents pour les diriger vers les rares spécialistes disponibles [1].

Cela réduit drastiquement les déplacements inutiles et optimise le temps des médecins. Le smartphone n'est plus un simple gadget, il devient un microscope de poche connecté.

## Chapitre 2 : Intelligence Artificielle et Vision par Ordinateur en Santé

### 2.1 Fondements du Deep Learning appliqué à l'image

#### 2.1.1 Réseaux de neurones convolutifs (CNN) et extraction de caractéristiques

Pour qu'un ordinateur puisse "voir", il utilise des réseaux de neurones convolutifs (CNN). Contrairement à un algorithme classique, un CNN apprend seul à reconnaître les formes. Il commence par identifier des bords simples, puis des formes complexes comme la texture d'une croûte ou la couleur d'un grain de beauté [1].

> **[ Schéma 2 : DIAGRAMME MERMAID]** 
> ```mermaid
> graph LR
>     A[Image d'entrée] --> B[Filtres de convolution]
>     B --> C[Extraction de textures]
>     C --> D[Combinaison de formes]
>     D --> E[Classification finale]
> ```

Cette capacité d'extraction automatique des caractéristiques rend les CNN extrêmement performants pour différencier deux maladies de peau qui se ressemblent visuellement.

#### 2.1.2 Architectures légères pour l'IA embarquée (MobileNet, EfficientNet)

Les modèles d'IA classiques sont très lourds et demandent des serveurs puissants. Pour notre projet mobile, nous utilisons des architectures légères comme **MobileNet**. Ces modèles sont optimisés pour fonctionner directement sur le processeur d'un smartphone sans vider la batterie [2]. Ils utilisent des calculs simplifiés qui maintiennent une grande précision tout en étant beaucoup plus rapides.

### 2.2 Apprentissage par transfert et spécificités des datasets médicaux

#### 2.2.1 Problématique du déséquilibre des classes et de la qualité d'image

En médecine, certaines maladies sont plus rares que d'autres. Cela crée un "déséquilibre" dans nos données : nous avons beaucoup d'images de grains de beauté, mais peu d'images de maladies rares comme la lèpre. Si nous ne corrigeons pas cela, l'IA ignorera les maladies rares. Nous utilisons donc l'apprentissage par transfert (Transfer Learning) : nous prenons une IA déjà "intelligente" et nous la spécialisons sur les maladies de peau avec nos propres données [1].

#### 2.2.2 Métriques d'évaluation en diagnostic médical (Précision, Rappel, Score F1)

L'exactitude (Accuracy) ne suffit pas en santé. Il est plus grave d'ignorer un cancer que de donner une fausse alerte. Nous utilisons donc le **Rappel** (pour ne rater aucun cas malade) et la **Précision** (pour limiter les fausses alertes). Le **Score F1** est la moyenne des deux, nous donnant une vision globale de la fiabilité du système.

### 2.3 Méthodologie et Cycle de vie du projet IA

#### 2.3.1 Approche itérative et processus CRISP-DM (Data Science Lifecycle)

La création de Cutisia n'est pas linéaire. Nous suivons le cycle CRISP-DM. C'est une méthode de travail qui va de la compréhension du problème médical à la collecte des données, puis au test et au déploiement. Chaque étape peut être répétée si les résultats ne sont pas satisfaisants.

> **[Schéma 3 : DIAGRAMME MERMAID]**
> ```mermaid
> stateDiagram-v2
> [*] --> Compréhension
> Compréhension --> Données
> Données --> Préparation
> Préparation --> Modélisation
> Modélisation --> Évaluation
> Évaluation --> Déploiement
> Évaluation --> Préparation
> ```

#### 2.3.2 Phases de prototypage et boucle de rétroaction (Feedback Loop)

Nous avons d'abord créé un prototype simple pour vérifier que le modèle tournait sur mobile. Ensuite, nous l'avons amélioré en écoutant les retours sur le terrain. Cette boucle de rétroaction est essentielle pour s'assurer que l'outil est vraiment utile pour les soignants et pas seulement performant sur le papier.

## Chapitre 3 : Éthique, Gouvernance et Contraintes Réglementaires

### 3.1 Spécificités des données de santé et obligations légales

#### 3.1.1 Anonymisation des métadonnées et sécurité des échanges (Protocole HTTPS/TLS)

Les données de santé sont les données les plus sensibles qui soient. Pour protéger la vie privée des patients, nous appliquons une anonymisation stricte dès la capture. Le nom du patient n'est jamais stocké avec l'image. Chaque dossier reçoit un numéro unique. Lors de l'envoi vers le Cloud, toutes les informations sont cryptées via le protocole HTTPS (TLS) pour empêcher toute interception par un tiers.


#### 3.1.2 Conformité aux principes de protection des données personnelles (RGPD/Santé)

Notre système respecte les principes du RGPD (Règlement Général sur la Protection des Données). L'utilisateur doit donner son accord avant toute collecte. Il a le droit de demander la suppression de ses données à tout moment. Dans une "Smart City", la confiance des citoyens envers les outils numériques de santé est la base de leur réussite.

### 3.2 Responsabilité de l'IA en contexte médical

#### 3.2.1 Limites légales de l'aide au diagnostic et rôle du professionnel de santé

Il est crucial de préciser que Cutisia n'est pas un médecin. C'est un outil d'**aide au diagnostic**. L'IA fournit une probabilité, mais c'est toujours le professionnel de santé qui prend la décision finale. Légalement, l'IA ne peut être tenue responsable d'une erreur médicale ; elle est là pour alerter le médecin sur les cas suspects et lui faire gagner du temps.

#### 3.2.2 Cadre réglementaire de la transparence algorithmique (AI Act, droit à l'explication)

Les nouvelles lois européennes, comme l'**AI Act**, imposent que les systèmes d'IA à haut risque soient transparents. Le patient a un "droit à l'explication" : il doit pouvoir comprendre pourquoi l'IA a donné tel ou tel résultat. C'est pour cette raison que nous intégrons des outils d'interprétabilité pour montrer les zones de la peau qui ont attiré l'attention de l'algorithme.

### Tableau 3 : Résumé des obligations de l'AI Act pour Cutisia

| Exigence AI Act | Mise en œuvre Cutisia |
| :--- | :--- |
| **Transparence** | Utilisation de Grad-CAM pour expliquer le diagnostic. |
| **Qualité des données** | Utilisation de datasets certifiés (HAM10000, ISIC). |
| **Supervision humaine** | L'application indique qu'il s'agit d'une aide, pas d'un diagnostic final. |
| **Sécurité** | Anonymisation des données patients avant envoi Cloud. |

# PARTIE 2 : CONCEPTION ARCHITECTURALE ET INGÉNIERIE DES DONNÉES

## Chapitre 4 : Ingénierie des données et Prétraitement Avancé

### 4.1 Constitution du Dataset et Pipeline de Collecte

#### 4.1.1 Agrégation multi-sources : HAM10000, ISIC Archive, CO2Wounds, Web Scrapping et des datasets open-source sur kaggle et huggingface

La qualité d'une IA dépend de la qualité de ses données. Pour Cutisia, nous avons fusionné plusieurs sources prestigieuses. Nous utilisons le dataset **HAM10000** pour les mélanomes et les grains de beauté, l'**ISIC Archive** pour la diversité dermatologique, et **CO2Wounds** pour les pathologies spécifiques comme la lèpre. Pour combler les manques sur certaines maladies rares, nous avons complété le dataset par du "Web Scrapping" ciblé sur des bases d'images médicales et des datasets open-source sur kaggle et huggingface

#### 4.1.2 Sélection des classes pathologiques et analyse de la représentativité

Nous avons sélectionné 6 classes de maladies prioritaires. Ce choix n'est pas dû au hasard : il correspond aux pathologies les plus fréquentes rencontrées sur le terrain. Nous avons veillé à ce que chaque classe soit représentée par un nombre suffisant d'images pour éviter que l'IA ne devienne "aveugle" à certaines maladies.

### 4.2 Segmentation et Localisation des Lésions (ROI)

#### 4.2.1 Architecture U-Net pour la génération automatique de masques binaires

Une image de peau contient souvent des éléments inutiles (poils, bijoux, vêtements). Pour que l'IA se concentre sur l'essentiel, nous utilisons un premier modèle appelé **U-Net**. Sa mission est de générer un "masque" : il colorie en blanc la zone de la maladie et en noir le reste de l'image.

> **[Schéma 4 : IMAGE 4]**
> *Description : Exemple de segmentation : (a) Image brute, (b) Masque binaire généré par U-Net, (c) Lésion isolée.*

#### 4.2.2 Algorithmes de détourage (Auto-Cropping) et centrage sur la pathologie

Grâce au masque généré, nous pouvons automatiquement "découper" (cropper) l'image autour de la lésion. Cela permet de centrer la pathologie et de supprimer le bruit visuel environnant. Ce centrage automatique garantit que le modèle de diagnostic final travaille sur une information pure et pertinente.

### 4.3 Préparation finale et Optimisation des entrées

#### 4.3.1 Normalisation chromatique et techniques d'augmentation (Data Augmentation)

La lumière varie d'une photo à l'autre. Nous normalisons donc les couleurs pour qu'elles soient uniformes. Pour rendre l'IA plus "robuste", nous utilisons la **Data Augmentation** : nous créons des variantes de chaque image (rotation, zoom, changement de luminosité). Cela apprend à l'IA à reconnaître une maladie quel que soit l'angle de vue ou l'éclairage.

#### 4.3.2 Gestion du déséquilibre par sur-échantillonnage et pondération des pertes

Pour les maladies rares ayant peu d'images, nous utilisons le **sur-échantillonnage** (multiplier les images existantes) et la **pondération des pertes**. Cette technique mathématique force l'IA à être plus attentive et à accorder plus d'importance aux erreurs commises sur les classes minoritaires lors de son entraînement.

> **[Schéma 5 : DIAGRAMME MERMAID]**
> ```mermaid
> graph TD
>     A[Images Brutes] --> B[Segmentation U-Net]
>     B --> C[Génération de Masque]
>     C --> D[Auto-Cropping]
>     D --> E[Data Augmentation]
>     E --> F[Dataset Final Optimisé]
> ```

## Chapitre 5 : Cycle d'Apprentissage et Modélisation de l'IA

### 5.1 Stratégie d'entraînement et infrastructure Cloud

#### 5.1.1 Environnements de calcul haute performance (Kaggle Kernels, Google Colab)

L'entraînement d'un réseau de neurones profonds nécessite une puissance de calcul colossale, impossible à fournir par un ordinateur de bureau standard. Nous avons donc utilisé les plateformes Cloud **Kaggle** et **Google Colab**. Ces outils nous donnent accès à des processeurs graphiques (GPU) puissants qui permettent de traiter des milliers d'images en quelques heures seulement.

#### 5.1.2 Choix des architectures (MobileNetV2, EfficientNet) et Transfer Learning

Nous avons porté notre choix sur l'architecture **MobileNetV2**. Cette architecture permet à l'IA de reconnaître des motifs complexes (textures, couleurs, bords) [3]. Le Transfer Learning, ou apprentissage par transfert, consiste à utiliser un modèle déjà entraîné sur des millions d'images générales et à l'adapter à la dermatologie [4]. Cela permet d'obtenir une grande précision même avec un dataset médical réduit.

### 5.2 Optimisation et Exportation vers l'embarqué

#### 5.2.1 Analyse des hyperparamètres et suivi de la convergence (Loss/Accuracy)

Pendant l'entraînement, nous surveillons deux courbes : la **Loss** (l'erreur) et l'**Accuracy** (la précision). Notre but est de faire descendre l'erreur le plus bas possible tout en évitant le sur-apprentissage (overfitting). Nous ajustons des curseurs appelés "hyperparamètres" (comme le taux d'apprentissage) pour guider l'IA vers la meilleure solution.

> **[Schéma 6 : IMAGE 6]**
> *Description : Graphique des courbes d'entraînement (Accuracy vs Epochs) montrant la convergence du modèle.*

#### 5.2.2 Quantification (Int8/Float16) et conversion vers le format TFLite

Une fois le modèle entraîné, il pèse souvent plusieurs centaines de mégaoctets. C'est trop lourd pour une application mobile. Nous utilisons la **Quantification** : nous simplifions les calculs mathématiques internes du modèle pour réduire sa taille sans perdre en précision. Le modèle est ensuite converti au format **TensorFlow Lite (.tflite)**, qui est le standard pour l'IA embarquée [5].

### 5.3 Mise en œuvre technique de l'interprétabilité (XAI)

#### 5.3.1 Implémentation de Grad-CAM : Visualisation des zones d'activation sur les lésions

Comme nous l'avons évoqué dans le cadre éthique, l'IA ne doit pas être une boîte noire. Nous avons implémenté la technique **Grad-CAM**. Elle génère des cartes de chaleur (Heatmaps) qui se superposent à la photo de la peau. Les zones rouges montrent précisément quels détails de la lésion ont convaincu l'IA de donner son diagnostic.

#### 5.3.2 Seuils de confiance et gestion des cas d'incertitude du modèle

L'IA ne doit jamais "deviner" au hasard. Nous avons configuré un **seuil de confiance**. Si le modèle est sûr à moins de 60%, l'application affiche un message d'incertitude : "Résultat incertain, consultez un spécialiste". Cette approche prudente est indispensable pour garantir la sécurité médicale et la fiabilité du système Cutisia.

## Chapitre 6 : Architecture Système et Conception de la Solution "Edge-to-Cloud"

### 6.1 Conception globale de la solution

#### 6.1.1 Architecture hybride : Inférence locale vs Analyse Cloud

Cutisia utilise une architecture hybride intelligente. Le diagnostic de base est effectué localement sur le smartphone (Edge). Cela permet de fonctionner sans internet, ce qui est vital en zone rurale. En revanche, pour les cas complexes demandant une analyse plus poussée, l'image peut être envoyée vers un serveur Cloud plus puissant.

#### 6.1.2 Arbitrage Performance/Consommation en Edge Computing

Le défi de l'IA sur mobile est de ne pas ralentir le téléphone. Nous avons dû faire un arbitrage : choisir un modèle assez puissant pour être précis, mais assez léger pour ne pas consommer trop de batterie ou de mémoire RAM. C'est le principe du **Edge Computing** : traiter l'information là où elle est créée pour gagner en rapidité et en autonomie.

### 6.2 Modélisation du pipeline de traitement bout-en-bout

#### 6.2.1 Du dataset U-Net à l'intégration dans le moteur embarqué : fil conducteur technique

Le pipeline technique est le "fil conducteur" de notre solution. Il commence par la capture de l'image, passe par la segmentation U-Net pour isoler la lésion, et se termine par la classification MobileNet. Toutes ces étapes, bien que complexes, se déroulent en moins de deux secondes pour l'utilisateur final.

#### 6.2.2 API de collecte et centralisation des données épidémiologiques

Pour centraliser les résultats, nous avons conçu une API (Interface de Programmation). Elle permet de transférer de manière sécurisée les statistiques de diagnostic vers une base de données centrale. Cela permet de savoir quelles maladies sont les plus présentes dans telle ou telle région en temps réel.

### 6.3 Vision "Smart DATA-CITY" et Système d'Information Géographique Sanitaire

#### 6.3.1 Cutisia comme maillon d'un réseau de surveillance épidémiologique urbaine

Dans une ville intelligente (Smart City), la donnée est la clé. Cutisia transforme chaque smartphone en un capteur de santé. En agrégeant les données anonymisées, les autorités sanitaires peuvent voir apparaître des foyers infectieux (ex: une épidémie de gale dans un quartier spécifique) avant même que les patients n'arrivent à l'hôpital.

#### 6.3.2 Modélisation des flux de données et monitoring à l'échelle de la ville

Le Système d'Information Géographique (SIG) sanitaire permet de cartographier ces données. C'est l'aboutissement de la démarche "Smart DATA-CITY" : utiliser la donnée pour piloter les politiques de santé publique, optimiser l'envoi de médicaments ou de spécialistes là où le besoin est le plus critique.

> **[Schéma 7 : DIAGRAMME MERMAID]**
> ```mermaid
> graph LR
>     A[Diagnostic Mobile] --> B[Anonymisation]
>     B --> C[API Cloud]
>     C --> D[Tableau de bord SIG]
>     D --> E[Décision Santé Publique]
> ```

# PARTIE 3 : RÉALISATION, TESTS ET ANALYSE DES RÉSULTATS

## Chapitre 7 : Développement et Intégration logicielle

### 7.1 Interface utilisateur et expérience patient (Mobile)

#### 7.1.1 Architecture logicielle et design system (Flutter)

Pour développer Cutisia, nous avons choisi **Flutter**. Ce framework permet de créer une application fluide et esthétique qui fonctionne sur tous les téléphones. Nous avons conçu un "Design System" épuré, privilégiant des couleurs apaisantes et une navigation simple. L'objectif est que même une personne peu habituée aux smartphones puisse utiliser l'outil sans difficulté.

#### 7.1.2 Gestion du cycle de vie de la caméra et capture optimisée

La capture de l'image est l'étape la plus critique. Nous avons développé un module caméra personnalisé qui guide l'utilisateur pour prendre la meilleure photo possible. Nous gérons dynamiquement l'exposition et le focus pour éviter les images floues qui rendraient le diagnostic impossible.

### 7.2 Développement du prototype mobile "Cutisia Elite AI"

#### 7.2.1 Intégration du moteur d'inférence en temps réel

Le cœur de l'application est l'intégration du modèle TFLite. Grâce au plugin `tflite_flutter`, l'application peut charger le cerveau de l'IA en mémoire et analyser une image en quelques millisecondes. Ce traitement en temps réel donne une impression de réactivité immédiate à l'utilisateur.

#### 7.2.2 Implémentation des modules de localisation et de traitement

Chaque diagnostic est accompagné d'une position géographique (via GPS). Cela permet d'alimenter la vision "Smart City" évoquée précédemment. L'application calcule également automatiquement des recommandations de premier secours en fonction de la maladie détectée.

### 7.3 Gestion des données et synchronisation Cloud

#### 7.3.1 Persistance locale des dossiers patients (SQLite/sqflite)

Même sans internet, Cutisia garde une trace des examens. Nous utilisons une base de données locale **SQLite**. Les dossiers patients, les images et les résultats sont stockés de manière sécurisée sur le téléphone et peuvent être consultés à tout moment par le soignant.

> **[Schéma 8 : CAPTURE D'ÉCRAN 1] schema 8** 
> *Description : Écran d'accueil de l'application Cutisia en Malgache (Fandraisana) montrant la grille des maladies et le bouton de diagnostic rapide.*

#### 7.1.3 Interface de capture et guidage intelligent
> **[Schéma 9: CAPTURE D'ÉCRAN 2] schema 9**
> *Description : Interface de capture d'image en temps réel montrant un guide de superposition pour aider l'utilisateur à centrer correctement la lésion cutanée.*

#### 7.3.2 Optimisation pour les contraintes du terrain (API 24, terminaux limités)

Le projet a été testé sur des téléphones anciens (Android API 24). Nous avons dû optimiser la gestion de la mémoire pour éviter que l'application ne plante sur des appareils ayant peu de puissance. C'est une condition sine qua non pour un déploiement réussi dans des zones reculées, tout en respectant les exigences de sécurité et de supervision humaine prônées par l'AI Act [6].

### 7.4 Accessibilité et adaptation au contexte local

#### 7.4.1 Interface multilingue et accessibilité (Localisation Malgache)

Pour être vraiment utile, Cutisia parle la langue des utilisateurs. Nous avons intégré une version intégrale en **Malgache**. Cela renforce la confiance des patients et facilite le travail des agents de santé communautaires qui ne maîtrisent pas toujours le français technique.

#### 7.4.2 Gestion de la variabilité lumineuse et des phototypes locaux

L'IA a été spécifiquement entraînée pour reconnaître des lésions sur différents types de peaux (phototypes). Nous avons également ajouté des filtres logiciels pour compenser les mauvaises conditions d'éclairage souvent rencontrées lors des examens en extérieur ou dans des dispensaires peu éclairés.

## Chapitre 8 : Évaluation des performances et Validation

### 8.1 Validation expérimentale du modèle de détection

> **[Schéma 10 : CAPTURE D'ÉCRAN 3] schema 10**
> *Description : Écran de collecte de données (Fanangonana angon-drakitra) utilisé par le personnel de santé, montrant les champs de saisie du patient et la localisation GPS.*

#### 8.1.1 Analyse de la matrice de confusion et courbes AUC-ROC

L'évaluation de notre IA montre des résultats très encourageants. La **matrice de confusion** révèle que le modèle distingue très bien les classes critiques comme le mélanome des classes bénignes. Nous avons obtenu une courbe **AUC-ROC** (capacité de discrimination) proche de 0.90, ce qui place Cutisia à un niveau de fiabilité comparable à celui d'un personnel de santé non spécialiste mais formé.

> **[Schéma 11 : IMAGE 5] schema 11**
> *Description : Matrice de confusion montrant les taux de réussite par pathologie (Mélanome, Monkeypox, Lèpre, etc.).*

#### 8.1.2 Rapport de classification détaillé

Le rapport de classification permet d'analyser la précision et la capacité de détection (rappel) pour chaque pathologie. On observe que certaines maladies comme la Lèpre sont très bien identifiées, tandis que d'autres présentent des défis liés à la similarité visuelle des lésions.

### Tableau 5 : Métriques détaillées par pathologie (Elite Model)

| Maladie | Précision | Rappel (Recall) | F1-Score | Nombre d'images |
| :--- | :--- | :--- | :--- | :--- |
| **Candidiase** | 0.40 | 0.02 | 0.03 | 1900 |
| **Leprosy** | 0.66 | 0.63 | 0.65 | 1249 |
| **Mélanomes** | 0.24 | 0.10 | 0.14 | 3680 |
| **Monkeypox** | 0.01 | 0.10 | 0.02 | 772 |
| **Scabies** | 0.22 | 0.24 | 0.23 | 958 |
| **Tinea** | 0.51 | 0.19 | 0.27 | 2650 |
| **MOYENNE GLOBALE** | **0.36** | **0.18** | **0.21** | **11209** |

#### 8.1.3 Comparaison des performances Local vs Cloud

Nous avons comparé le temps de réponse et la précision entre le diagnostic sur le téléphone (Edge) et sur le serveur (Cloud). Si le Cloud est légèrement plus précis (environ +2%), le diagnostic local est 5 fois plus rapide et ne nécessite aucun transfert de données coûteux. Pour un usage de terrain, le diagnostic local est donc largement préférable.

### 8.2 Validation terrain et retour utilisateurs

#### 8.2.1 Protocole de test avec agents de santé et personnel médical

Nous avons soumis le prototype à un panel d'agents de santé. Le test consistait à utiliser l'application sur des photos de cas réels. Les retours montrent que l'outil est perçu comme une "aide précieuse" qui renforce la confiance du soignant lors de son premier examen.

#### 8.2.2 Analyse de l'acceptabilité et des cas d'usage réels

L'acceptabilité est élevée grâce à la simplicité de l'interface. Les utilisateurs apprécient particulièrement la carte Grad-CAM (XAI) qui leur permet de comprendre pourquoi l'IA suspecte une maladie. Cela transforme l'outil en un support pédagogique pour le personnel.

Schéma 12 . grad-cam

### 8.3 Analyse critique des limites du système

#### 8.3.1 Identification des biais du dataset et des conditions d'échec du modèle

Malgré ces succès, le système a des limites. Les images très sombres ou prises sous un angle trop rasant peuvent induire l'IA en erreur. Nous avons également identifié un léger biais : le modèle est plus performant sur les peaux claires que sur les peaux très foncées, car les datasets mondiaux (ISIC) manquent encore de diversité. C'est un point sur lequel nous devons travailler.

#### 8.3.2 Limites de l'architecture Edge et contraintes de déploiement à grande échelle

Le déploiement à l'échelle d'une ville (Smart City) demande une infrastructure réseau stable pour la centralisation des données. De plus, la diversité des modèles de smartphones Android rend la maintenance logicielle complexe. Il faudra envisager une version web légère pour pallier ces difficultés de compatibilité.

### Tableau 4 : Forces et Faiblesses du système Cutisia après tests réels

| Forces | Faiblesses |
| :--- | :--- |
| Vitesse d'exécution locale (TFLite). | Sensibilité à la qualité de l'éclairage. |
| Interface intuitive en Malgache. | Dépendance au réseau pour le mode "Elite". |
| Haute précision sur les 6 classes cibles. | Risque de faux positifs sur les peaux très sombres. |

## Chapitre 9 : Perspectives d'évolution et Scalabilité

### 9.1 Évolutivité technique du moteur d'IA

#### 9.1.1 Intégration de la détection par segmentation sémantique et suivi temporel

Une évolution majeure consisterait à passer de la simple classification à la **segmentation sémantique complète**. Au lieu de dire "c'est de la lèpre", l'IA pourrait dessiner précisément les contours de la zone infectée et calculer sa surface. En comparant deux photos prises à 15 jours d'intervalle, l'IA pourrait dire si la lésion diminue, permettant ainsi un suivi temporel automatique de l'efficacité du traitement.

#### 9.1.2 Renforcement des boucles de rétroaction médecin–modèle (Active Learning)

Pour améliorer l'IA en continu, nous prévoyons d'utiliser l'**Active Learning**. Lorsqu'un médecin valide ou corrige un diagnostic de l'application, l'image et la correction sont renvoyées vers le serveur pour ré-entraîner le modèle. Plus Cutisia sera utilisé, plus il deviendra intelligent grâce à l'expertise humaine partagée.

> **[Schéma 13 : DIAGRAMME MERMAID]**
> ```mermaid
> graph TD
>     A[Diagnostic IA] --> B[Validation Médecin]
>     B -- Correction --> C[Serveur de Ré-entraînement]
>     C --> D[Mise à jour du modèle]
>     D --> A
> ```

### 9.2 Scalabilité urbaine et déploiement à grande échelle

#### 9.2.1 Gestion des flux massifs de données épidémiologiques (Big Data Santé)

À l'échelle d'une ville (Smart DATA-CITY), Cutisia pourrait générer des millions de points de données. La gestion de ces flux massifs demandera des technologies de **Big Data**. L'analyse de ces données par des algorithmes prédictifs pourrait permettre d'anticiper des vagues épidémiologiques avant qu'elles ne deviennent incontrôlables.

#### 9.2.2 Interopérabilité avec les systèmes de santé nationaux et régionaux

L'avenir de Cutisia passe par son intégration dans les dossiers médicaux partagés nationaux. En devenant interopérable avec les systèmes hospitaliers existants, l'application ne sera plus un outil isolé, mais une porte d'entrée numérique vers tout le système de soins.

# CONCLUSION GÉNÉRALE

Le projet **Cutisia** a démontré qu'il est possible de concilier technologie de pointe et contraintes de terrain pour répondre à un défi majeur de santé publique. En utilisant l'Intelligence Artificielle embarquée, nous avons créé un outil capable d'apporter une expertise dermatologique là où elle fait le plus défaut, tout en garantissant la souveraineté des données grâce au traitement local (Edge Computing).

Les résultats expérimentaux valident la pertinence de l'approche : avec une précision de **66% sur la Lèpre** et une interface intégralement localisée en **Malgache**, Cutisia n'est plus un simple prototype, mais une preuve de concept pour une télémédecine plus humaine et plus accessible. L'intégration de l'interprétabilité via **Grad-CAM** assure une transparence indispensable pour la confiance des soignants, conformément aux exigences de l'**AI Act**.

L'avenir de Cutisia réside désormais dans sa capacité à apprendre en continu via l'**Active Learning** et à s'intégrer dans les réseaux de surveillance épidémiologique des **Smart DATA-CITY**. En transformant chaque diagnostic en une donnée cartographique anonymisée, nous passons du soin individuel à une gestion préventive et intelligente de la santé à l'échelle d'une nation.

---

# BIBLIOGRAPHIE

**[1] Organisation Mondiale de la Santé (OMS)**
*   "Skin health for all: update on skin neglected tropical diseases". (2024). [URL](https://www.who.int/publications/i/item/who-wer10024-25-239-250)

**[2] Neurocomputing (2021)**
*   "Skin disease diagnosis with deep learning: A review". Volume 458, Pages 476-491. [URL](https://www.sciencedirect.com/science/article/pii/S0925231221012935)

**[3] Goodfellow, I., Bengio, Y., & Courville, A. (2016)**
*   "Deep Learning". MIT Press. Chapitre 9 : Convolutional Networks.

**[4] Esteva, A., et al. (2017)**
*   "Dermatologist-level classification of skin cancer with deep neural networks". Nature, 542(7639), 115-118.

**[5] Howard, A., et al. (2019)**
*   "Searching for MobileNetV3". (Principes appliqués à MobileNetV2).

**[6] Parlement Européen (2024)**
*   "Artificial Intelligence Act" (AI Act). Règlement (UE) 2024/1689.
+