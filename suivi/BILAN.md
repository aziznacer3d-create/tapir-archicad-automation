# Bilan — options de l'API C++ ajoutées à Tapir (17/11/2026)

Journal détaillé du travail, dans l'ordre. Pour reprendre, lire d'abord `README.md` (même dossier `suivi/` de la branche `suivi-options-manquantes`).

Publié : PR #2899 (garde-corps) et PR #2900 (commandes de champs + réglages par défaut), depuis la copie GitHub `aziznacer3d-create/tapir-archicad-automation`.

## Ce qui a été ajouté

1. **Trois commandes génériques** (`ElementFieldCommands.cpp`, table générée `ElementFieldTable.cpp`) :
   - `GetElementFieldDefinitions` : la liste des champs d'un type d'élément (chemin, type, lecture seule, variante) ;
   - `GetElementFields` : lit les champs d'éléments par leur chemin C++ (ex. `note.noteFont`, `u.planeRoof.angle`) ;
   - `SetElementFields` : écrit les champs donnés, puis les relit et signale ceux qu'Archicad n'a pas gardés.
   - 3 368 champs de 71 types d'éléments ; 3 146 modifiables (les 222 autres : propriétaires et compteurs calculés par Archicad).
   - Couvre les 589 réglages « Absentes » et rend modifiables les réglages « Lecture seule ».
   - Table générée depuis le DevKit 29 par `tools/generate_element_field_table.py` : Archicad 29 seulement.
2. **Garde-corps** (`ModifyRailings`) :
   - `segments[].pattern` : poteaux intermédiaires, panneaux, jeux de balustres et répartition du motif ;
   - `nodes[].post` : modèle des poteaux d'un nœud ;
   - un poteau ou poteau intermédiaire isolé est refusé avec un message qui renvoie vers `pattern` / `post` ;
   - `GetDetailsOfElements` donne le vrai propriétaire (nœud, segment, motif) des composants.

## Ce que les tests ont appris sur Archicad 29 (build 5101, version française)

- Le champ `owner` des composants d'un garde-corps donne le garde-corps lui-même : le vrai parent se lit par la hiérarchie.
- Archicad ne lit un masque de modification que sur le **premier octet** d'un membre : il faut marquer aussi les parents (`begC` pour `begC.y`).
- Toiture, coque, étiquette, structure d'escalier ont des **variantes** qui partagent la même mémoire : écrire dans la mauvaise faisait planter Archicad. Elles sont maintenant protégées.
- Les composants d'un garde-corps sont **générés** : on ne peut pas en changer un seul. Tous les segments suivent le motif du **segment 0**.
- Beaucoup de valeurs sont recalculées par Archicad (taille d'un texte, épaisseurs d'un mur composite, règles d'escalier, géométrie d'un mur-rideau…) : « non gardé » n'est alors pas un défaut.
- Caméras et images : Archicad refuse toute modification directe.

## Résultats des tests

- Test des champs : 136 éléments et sous-éléments de 47 types, sans plantage (détail : `resultats_tests\rapport.md`).
- Tests du dépôt : 290 fichiers sur 292 lancés ; 172 entièrement réussis. Les 2 non lancés font planter Archicad à cause de bugs connus de Tapir (`modify_roof_holes.json` = #2897, `snap_points_hotspots_and_hosted_elements.json`), sans lien avec ces changements. Les autres échecs viennent du gabarit français ou de l'environnement (modèle analytique, MEP, bibliothèques…), hors du code modifié.
- Nouveaux tests : `element_fields.json` 18/18, `modify_railings_posts_panels.json` réécrit 28/28.

## Test dans Archicad 30 (17/11/2026, 02:28)

Version compilée avec le DevKit officiel 30.3000, testée dans Archicad 30 FRA build 3001 (fichier de test : `fichier_Archicad_30\TapirAddOn_AC30_Win.apx` ; ton Tapir 2.0.0 est gardé à côté en `.bak`).

- Test des champs : 183 éléments et sous-éléments de 53 types, **sans plantage** (31 min ; détail : `C:\ArchicadDev\Tapir_test_global_AC30\rapport.md`).
- Résultats presque identiques à Archicad 29 ; Archicad 30 garde même un peu plus de valeurs (poutres 43 au lieu de 40, poteaux 47 au lieu de 42, murs-rideaux 73 au lieu de 68). Les 6 champs de cote propres à Archicad 30 sont lus et réécrits.
- Modèles de garde-corps : mêmes résultats qu'Archicad 29 (segment 0 et poteau de nœud gardés ; le motif du segment 1 seul n'est pas gardé par Archicad ; un poteau intermédiaire seul renvoie vers `pattern`).
- Tests JSON : `element_fields.json` 18/18, `modify_railings_posts_panels.json` 24/24 (version corrigée pour le robot), et les 9 autres tests de garde-corps exactement comme dans Archicad 29 (mêmes échecs, dus au gabarit français).
- Deux fenêtres d'Archicad 30 ont bloqué le test et il a fallu les fermer à la main : « des éléments ont été créés sur des étages non visibles » (avertissement normal) et « No Zones Found », ouverte par Archicad quand on change `linkToSettings.homeStoryDifference` d'une zone. Le test attend maintenant qu'une fenêtre soit fermée au lieu de s'arrêter.
- Le fichier testé contient le code des deux PR réunies (branche locale `options-absentes`, ee7ab8e1) ; il ne diffère de chaque branche de PR que par des textes de message.
- 17/11 vers 07:00 : ce résultat est publié en commentaire sur les PR #2899 et #2900 (avec ton accord). Dernière relecture du robot sur les deux PR : « Looks correct, nothing blocking » (aucun point bloquant) ; il précisait que le comportement devait être confirmé dans un vrai Archicad, ce que font ces commentaires. Les compilations attendent toujours l'accord d'un mainteneur.

## Réglages par défaut des outils (17/11/2026, 07:20)

Deux nouvelles commandes, **ajoutées à la PR #2900** le 17/11 vers 07:30 (2 commits, b9422b99 et 7c172857 ; description de la PR mise à jour). Relecture du robot : « Looks correct, nothing blocking » ; ses deux remarques (description qui ne citait que trois commandes, version Archicad 30 pas testée) sont réglées par la nouvelle description. Les compilations attendent toujours l'accord d'un mainteneur.

- `GetFieldsOfElementDefaults` : lit les réglages par défaut d'un ou plusieurs types d'éléments (tous, ou seulement ceux qu'on demande) ;
- `SetFieldsOfElementDefaults` : change seulement les réglages donnés, les relit et signale ceux qu'Archicad n'a pas gardés ; essai à blanc possible.

Elles utilisent la même table de réglages que `GetElementFields` / `SetElementFields`.

Test du dépôt `fields_of_element_defaults.json` : 18/18 dans Archicad 29 et dans Archicad 30 (un nouveau mur reçoit bien le stylo et le décalage par défaut donnés).

Grand test `test_defauts.py` (tous les types, chaque réglage modifié puis remis) : **sans plantage** dans Archicad 29 et 30, résultats presque identiques (rapports : `C:\ArchicadDev\Tapir_test_defauts_AC29\rapport.md` et `..._AC30\rapport.md`). Ce qu'il a appris :

- 68 types ont des réglages par défaut lisibles ; CamSet et SectElem n'en ont pas (Archicad refuse de les lire).
- La plupart des réglages sont gardés ; ceux qu'Archicad recalcule (profondeur des cadres de mur-rideau, marqueur source des coupes…) ne le sont pas.
- **Défaut trouvé et corrigé** : Archicad refuse `libInd` (l'objet de bibliothèque) dans les réglages par défaut des portes, fenêtres, fenêtres de toit, objets, lampes et zones, même inchangé, mais il écrit quand même les autres réglages donnés. La commande relit maintenant les réglages après un refus et dit lesquels ont changé quand même ; pour `libInd`, elle conseille d'appliquer un favori.
- Images et modules liés : Archicad refuse tout changement de leurs réglages par défaut.
- Composants de garde-corps (poteaux, lisses, segments, nœuds…) : Archicad ne garde aucun changement ; les modèles sont dans les réglages du garde-corps lui-même (`defSegment`, `defNode`), qui eux sont gardés.
- Certains changements ne peuvent pas être annulés par l'API : une fois la visibilité automatique par étage activée, Archicad ne la laisse pas couper ; un matériau de construction « 0 » ne revient pas à 0. Ces écarts ne concernent que les projets sans titre du test.

Après la correction (07:27, version réinstallée dans les deux Archicad) : `fields_of_element_defaults.json` **28/28** dans Archicad 29 et dans Archicad 30 (avec le cas de l'objet de bibliothèque refusé : le message nomme le stylo changé quand même et conseille un favori), `element_fields.json` 18/18 dans les deux. Le message des composants de garde-corps renvoie bien vers `defSegment` / `defNode`. Réglages d'origine revenus après le test (stylo du mur 27, décalage 0, stylo de l'objet 4).

## Inventaire des attributs (17/11/2026, 08:00)

Script `couverture_attributs.py` (DevKit officiel 29.3000), sortie `C:\ArchicadDev\Tapir_couverture_attributs\couverture_attributs.csv` / `.json`.

- 12 types d'attributs dans l'API (calque, type de ligne, motif de hachure, composite, surface, combinaison de calques, catégorie de zone, profil, table de stylos, système MEP, profil d'utilisation énergétique, matériau de construction) : 192 réglages, avec les éléments de leurs listes (traits d'un type de ligne, couches d'un composite, stylos d'une table…), plus les drapeaux de l'en-tête (calque caché, verrouillé…).
- **Correction** : contrairement à ce que j'avais dit, Tapir sait déjà modifier un attribut existant. Les 11 commandes `Create…` d'attributs (calques, types de ligne, hachures, composites, surfaces, matériaux de construction, profils, catégories de zone, combinaisons de calques, tables de stylos, systèmes MEP) ont l'option `overwriteExisting` : l'attribut désigné par son identifiant est modifié au lieu d'être créé.
- La mesure automatique classait une vingtaine de réglages en « lecture seule » ; vérifiés à la main, ils sont écrits par des fonctions d'aide (couleurs des surfaces et des catégories de zone, nom de texture, motif bitmap…). Presque tout est donc lu et écrit.
- **Ce qui manque vraiment** :
  1. les **profils d'utilisation de l'évaluation énergétique** : rien n'est lu ni écrit (6 réglages + profils journaliers, périodes d'utilisation et profils horaires : 31 réglages) ;
  2. les **valeurs des paramètres du tampon** d'une catégorie de zone : Tapir recopie celles de l'objet de bibliothèque, on ne peut pas les choisir ;
  3. des détails : couleur de hachure 3D d'une surface (`fillCol`), deux options de texture (décalage aléatoire, relief), et des informations en lecture seule (calque venant d'un module lié ou réservé par un autre utilisateur, attribut créé par GDL ou par un add-on).

## Inventaire du mémo des éléments (17/11/2026, 08:15)

Script `couverture_memo.py` (DevKit officiel 29.3000), sortie `C:\ArchicadDev\Tapir_couverture_memo\couverture_memo.csv` / `.json`. Le mémo tient les données de taille variable d'un élément. 89 parties ; Tapir en lit 78 et en écrit 40 (mesure automatique, puis vérification à la main des cas douteux).

- **Sous-éléments (29 parties)** : segments, cadres, panneaux, jonctions et accessoires des murs-rideaux, contremarches, marches et structures des escaliers, 17 sortes de composants de garde-corps, segments des poutres et poteaux. Ils sont atteints comme des éléments (GetSubelementsOfHierarchicalElements, puis GetElementFields / SetElementFields et les commandes Modify…).
- **Lus et écrits** : contours (coordonnées, arcs, identifiants), paramètres GDL, arêtes des dalles, hauteurs et niveaux des maillages, texte et lignes de texte, trous des poutres, image, cotes, segments des élévations intérieures, ligne de coupe et profondeur des coupes, motifs et cellules des murs-rideaux, ligne de base des escaliers, types d'arêtes et matériaux des côtés des toitures, contours des coques et des toitures multi-pans, corps et matériaux des formes libres, texte d'information, coupes et découpage des segments de poutre et de poteau, motifs des garde-corps.
- **Lus seulement** : poignées de Bézier des splines (la création ne fait que le lissage automatique), ligne de foulée des escaliers, contours et grille des segments de mur-rideau, profil étiré d'un élément à profil.
- **Ni lus ni écrits (vrai manque)** :
  1. **plans de découpe** (`gables`) d'un mur, poteau, poutre ou objet coupé par un plan : seul leur matériau est renuméroté ;
  2. **escaliers** : contours gauche et droit (`stairBoundary`), ligne de foulée personnalisée et ligne de foulée centrée ;
  3. **profil personnalisé d'origine** d'un mur, d'une poutre ou d'un poteau à profil modifié (`customOrigProfile`) ;
  4. **coupes et élévations** : ligne de la zone éloignée (`sectionSegmentDistCoords`) ;
  5. **paragraphes d'un texte** : retraits et interlignes de chaque paragraphe ;
  6. **liens de caméra** d'un parcours (`linkList`) ;
  7. contenu graphique interne d'un dessin (`drawingData`, format interne) et données d'éléments d'autres add-ons.
- Pas un manque : la liste des fenêtres et portes d'un mur (`wallWindows`, `wallDoors`, sortie seule) : chaque ouverture donne déjà son mur porteur.

## Lancer à nouveau le test global

Archicad 29 ouvert sur un nouveau projet vide, puis :

    python -I C:\Users\admin\Documents\RECHERCHE\Tapir_options_manquantes\test_global.py
    python -I C:\Users\admin\Documents\RECHERCHE\Tapir_options_manquantes\test_global.py --seulement-checks
