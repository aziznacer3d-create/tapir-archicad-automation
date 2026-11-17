# Suivi : options de l'API C++ d'Archicad ajoutées à Tapir

À lire en premier pour reprendre le travail, sur cet ordinateur ou sur un autre.
Le journal détaillé, dans l'ordre où le travail a été fait, est dans [BILAN.md](BILAN.md).

Cette branche `suivi-options-manquantes` contient :

- le code des deux pull requests réunies (la version qui a été testée dans Archicad 29 et 30) ;
- ce dossier `suivi/` : bilan, scripts de test et de mesure, rapports, et les deux fichiers `.apx` de test.

Ce n'est **pas** une branche à proposer en pull request : elle sert seulement à reprendre le travail.

## Où en est le travail (17/11/2026)

| Pull request | Branche (sur la copie `aziznacer3d-create`) | État |
|---|---|---|
| [#2899](https://github.com/ENZYME-APD/tapir-archicad-automation/pull/2899) garde-corps : `segments[].pattern`, `nodes[].post` (#2572) | `railings-pattern-post-models` | relue par le robot : rien de bloquant ; compilations en attente de l'accord d'un mainteneur |
| [#2900](https://github.com/ENZYME-APD/tapir-archicad-automation/pull/2900) commandes de champs et réglages par défaut (#2883) | `element-fields-commands` | relue par le robot : rien de bloquant ; compilations en attente de l'accord d'un mainteneur |

Il n'y a rien à faire sur ces deux PR tant qu'un mainteneur n'a pas autorisé les compilations ou posé une question.

## Ce qui est fait

1. **Garde-corps** (PR #2899) : `ModifyRailings` change le motif d'un segment (`segments[].pattern` : poteaux intermédiaires, panneaux, jeux de balustres, répartition) et le modèle de poteau d'un nœud (`nodes[].post`) ; `GetDetailsOfElements` donne le vrai parent des composants ; un composant changé seul est refusé avec un message qui renvoie vers le modèle.
2. **Commandes de champs** (PR #2900) : `GetElementFieldDefinitions`, `GetElementFields`, `SetElementFields` lisent et écrivent n'importe quel champ de la structure C++ d'un élément par son chemin (`note.noteFont`, `u.planeRoof.angle`…). Table générée depuis les DevKits officiels : 3 368 champs pour Archicad 29, 3 374 pour Archicad 30, 71 types d'éléments.
3. **Réglages par défaut des outils** (PR #2900) : `GetFieldsOfElementDefaults`, `SetFieldsOfElementDefaults`, avec la même table.
4. **Tests** (tous dans Archicad 29 et 30, version française) :
   - tests JSON du dépôt : `element_fields.json` 18/18 et `fields_of_element_defaults.json` 28/28 dans les deux versions ; `modify_railings_posts_panels.json` 24/24 dans Archicad 30 (sa version précédente : 28/28 dans Archicad 29) ;
   - grand test des éléments (53 types) et grand test des réglages par défaut (68 types) : **sans plantage**.
5. **Inventaires** de ce qui manque encore par rapport à l'API C++ : champs des éléments, attributs, mémo (voir la suite).

## Ce qui reste à faire (dans l'ordre conseillé)

1. **Escaliers** (mémo) : lire puis écrire les contours gauche et droit (`stairBoundary`), la ligne de foulée personnalisée (`stairCustomWalkLine`) et la ligne de foulée centrée (`stairCenterWalkLine`). Commencer par la lecture (sans risque), puis essayer l'écriture dans Archicad.
2. **Plans de découpe** (`gables` du mémo) d'un mur, poteau, poutre ou objet coupé par un plan : aujourd'hui seul leur matériau est renuméroté.
3. **Autres manques du mémo** : poignées de Bézier des splines (lues mais pas écrites), retraits et interlignes de chaque paragraphe d'un texte, ligne de la zone éloignée des coupes et élévations (`sectionSegmentDistCoords`), profil personnalisé d'origine (`customOrigProfile`), liens de caméra (`linkList`).
4. **Attributs** : profils d'utilisation de l'évaluation énergétique (31 réglages, rien n'est lu ni écrit) ; valeurs des paramètres du tampon d'une catégorie de zone ; détails (`fillCol` d'une surface, drapeaux de texture « décalage aléatoire » et « relief »).
5. **Champs d'éléments** :
   - 57 champs que la table ne sait pas encore lire ni écrire, parce que le générateur ne gère pas leur type : stylos « étendus » (`API_ExtendedPenType`, ex. `cutFillPen` d'un mur-rideau), matériaux remplacés (`API_OverriddenAttribute`, ex. matériaux d'un segment de poutre), textes `GS::UniString*` (contenu des notes de cote), données de symbole de la structure d'escalier ;
   - 169 champs dans la table mais jamais essayés, faute d'éléments dans le gabarit français : cote radiale, dessin, cercle, motif et raccords de garde-corps, jonctions et accessoires de mur-rideau… Il faut un projet qui contient ces éléments.
6. **Réglages par défaut** : les variations (objets, lampes) et les classes de coque et de toiture (le membre de l'union dépend de la classe des réglages lus).
7. **Connu, hors de nos changements** :
   - `modify_roof_holes.json` fait planter Archicad (bug #2897, correctif dans la PR #2898) ;
   - `snap_points_hotspots_and_hosted_elements.json` fait aussi planter Archicad ;
   - dans Archicad 30, `SetElementFields` avec `linkToSettings.homeStoryDifference` sur une zone ouvre la fenêtre « No Zones Found » : tant qu'elle est ouverte, Archicad refuse toutes les commandes (erreur 4001).

## Reprendre sur un autre ordinateur

### 1. Installer

- Git et **Git LFS** (le dépôt contient un gros fichier stocké avec LFS) ;
- Python 3.11 ou plus récent ;
- Visual Studio 2026 avec « Développement Desktop en C++ » et l'ensemble d'outils **v143** (CMake est fourni avec) ;
- Archicad 29 et/ou Archicad 30.

### 2. Récupérer le travail

```bat
git clone https://github.com/aziznacer3d-create/tapir-archicad-automation.git
cd tapir-archicad-automation
git checkout suivi-options-manquantes
git remote add upstream https://github.com/ENZYME-APD/tapir-archicad-automation.git
```

Si Windows bloque Python ou la compilation dans `Documents` (protection contre les rançongiciels), cloner ailleurs, par exemple dans `C:\ArchicadDev`.

### 3. Essayer sans compiler

`suivi/apx/` contient la version de test compilée (code de cette branche) :

1. fermer Archicad ;
2. dans `C:\Program Files\GRAPHISOFT\Archicad 29\Extensions\Tapir`, renommer `TapirAddOn_AC29_Win.apx` en `TapirAddOn_AC29_Win.apx.bak` (pour pouvoir revenir à la version officielle) ;
3. copier `suivi/apx/TapirAddOn_AC29_Win.apx` à sa place (droits d'administrateur) ;
4. même chose pour Archicad 30 avec `TapirAddOn_AC30_Win.apx`.

Pour revenir à la version officielle : supprimer le nouveau fichier et retirer « .bak » au nom de l'ancien.

### 4. Compiler

Toutes les versions (télécharge les DevKits listés dans `archicad-addon/devkits.json`, puis compile) :

```bat
cd archicad-addon\Tools
build_all_win.bat
```

Une seule version (exemple Archicad 29 ; l'adresse du DevKit est dans `archicad-addon/devkits.json`) :

```bat
cd archicad-addon
python Tools\download_and_unzip.py <adresse du DevKit> Build\DevKits\AC29
cmake -B Build/AC29 -G "Visual Studio 18 2026" -A x64 -T v143 -DAC_VERSION=29 -DAC_API_DEVKIT_DIR="Build\DevKits\AC29\Support" .
cmake --build Build/AC29 --config RelWithDebInfo
```

Si `cmake` n'est pas trouvé, il est dans `C:\Program Files\Microsoft Visual Studio\18\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe`.

La table des champs est générée depuis les DevKits officiels **29.3000** et **30.3000** (ceux de `devkits.json`). Pour la régénérer :

```bat
python tools/generate_element_field_table.py 29=Build/DevKits/AC29/Support 30=Build/DevKits/AC30/Support archicad-addon/Sources/ElementFieldTable.cpp
```

### 5. Tester

Toujours dans Archicad ouvert sur un **nouveau projet vide** (le test crée et efface des éléments). Si deux Archicad sont ouverts, le premier lancé répond sur le port 19723, le second sur 19724.

```bat
python tools\community-test-runner\tapir_test_runner.py check --port 19723 archicad-addon\Test\checks\fields_of_element_defaults.json
python -I suivi\outils\test_global.py --port 19723 --sortie C:\ArchicadDev\Tapir_test_global
python -I suivi\outils\test_defauts.py --port 19723 --sortie C:\ArchicadDev\Tapir_test_defauts
```

- `test_global.py` : crée des éléments de tous les types, lit, réécrit puis modifie un par un chaque champ (options `--sans-checks`, `--seulement-checks`, `--seulement-champs`). Il écrit chaque appel dans `journal.jsonl` avant de l'envoyer : si Archicad plante, la dernière ligne dit quel champ ; le champ est sauté au lancement suivant.
- `test_defauts.py` : même chose pour les réglages par défaut, puis remet les réglages d'origine (`--remettre` pour les remettre seulement). Certains ne reviennent pas (Archicad refuse de couper la visibilité automatique par étage, par exemple) : **fermer ensuite le projet sans l'enregistrer**.
- Si une fenêtre s'ouvre dans Archicad pendant un test, la fermer : le test attend puis reprend.

### 6. Mesurer ce qui manque encore

```bat
python -I suivi\outils\couverture_champs.py archicad-addon\Sources C:\ArchicadDev\Tapir_couverture Build\DevKits\AC29\Support\Inc
python -I suivi\outils\couverture_attributs.py Build\DevKits\AC29\Support\Inc archicad-addon\Sources C:\ArchicadDev\Tapir_couverture_attributs
python -I suivi\outils\couverture_memo.py Build\DevKits\AC29\Support\Inc archicad-addon\Sources C:\ArchicadDev\Tapir_couverture_memo
```

Ces mesures lisent le texte du code : elles ne voient pas une écriture faite par une fonction d'aide (`GetColor (..., attr.material.surfaceRGB)`). Un réglage classé « lecture seule » doit être vérifié à la main avant de conclure qu'il manque. Les résultats déjà obtenus sont dans `suivi/resultats/couverture/`, et la page en français des options manquantes dans `suivi/resultats/Options_manquantes_Tapir.html`.

## Pièges connus (à savoir avant de toucher au code)

- **Masque de modification** : Archicad ne lit le masque d'un membre que sur son premier octet. Pour changer `begC.y`, il faut aussi marquer le premier octet de `begC`.
- **Unions** (toiture, coque, étiquette, structure d'escalier) : seul le membre choisi par `roofClass`, `shellClass`, `labelClass` ou `structType` contient des valeurs. Écrire dans un autre a fait planter Archicad 29 : ces champs sont refusés, et les sélecteurs sont en lecture seule.
- **Composants de garde-corps** : ils sont générés depuis les modèles (motif du segment, modèle de poteau du nœud) ; on ne peut pas en changer un seul. Tous les segments d'un nouveau garde-corps suivent le motif du segment 0.
- **Réglages par défaut** : Archicad refuse `libInd` (l'objet de bibliothèque) dans les réglages par défaut des portes, fenêtres, fenêtres de toit, objets, lampes et zones, même inchangé, **mais écrit quand même les autres réglages donnés**. Les composants de garde-corps ne gardent aucun changement de leurs réglages par défaut.
- **Valeurs recalculées** : beaucoup de valeurs sont recalculées par Archicad (taille de texte, épaisseurs d'un composite, règles d'escalier…) ; « non gardé » n'est alors pas un défaut. Caméras et images refusent toute modification directe.
- **Fenêtre ouverte dans Archicad** : tant qu'une fenêtre (avertissement, réglages) est ouverte, Archicad refuse toutes les commandes avec l'erreur 4001.
- **Testeur du dépôt** (`tapir_test_runner.py`) : un chemin de résultat ne peut pas viser une clé qui contient un point (`fields.openingBase.pen`) ; utiliser des champs sans point dans les tests.
- **Gabarit** : les tests du dépôt supposent le gabarit international ; avec le gabarit français, certains échouent (pas de main courante dans le garde-corps par défaut, par exemple) sans lien avec le code.
- **Git** : pour pousser depuis un clone partiel, faire d'abord `git fetch` de la branche `main` de la copie (sinon le crochet LFS cherche des objets absents). Auteur des commits : `Aziz Nacer <270993008+aziznacer3d-create@users.noreply.github.com>` (adresse masquée de GitHub).

## Reprendre avec Claude Code

Ouvrir Claude Code dans le dossier du dépôt cloné et lui dire, en français :

> Lis `suivi/README.md` et `suivi/BILAN.md`, puis continue par le point 1 de « Ce qui reste à faire ». Parle-moi uniquement en français.
