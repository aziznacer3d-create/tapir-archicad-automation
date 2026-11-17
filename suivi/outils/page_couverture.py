"""Page HTML en francais : les options (champs) de l'API C++ d'Archicad 29 absentes ou en lecture seule dans Tapir."""
import html
import json
import pathlib
import sys

# Dossier qui contient couverture_champs.json et traduit_*.json (1er argument), par defaut celui de l'ordinateur d'origine.
DOS = pathlib.Path (sys.argv[1]) if len (sys.argv) > 1 else pathlib.Path (r'C:\ArchicadDev\Tapir_couverture')
d = json.load (open (DOS / 'couverture_champs.json', encoding='utf-8'))
tr = {}
for f in sorted (DOS.glob ('traduit_*.json')):
    tr.update (json.load (open (f, encoding='utf-8')))

NOMS = {
    'wall': 'Mur', 'column': 'Poteau', 'beam': 'Poutre', 'window': 'Fenêtre', 'door': 'Porte', 'object': 'Objet', 'lamp': 'Lampe',
    'slab': 'Dalle', 'roof': 'Toiture', 'mesh': 'Maillage', 'dimension': 'Cote linéaire', 'radialDimension': 'Cote radiale',
    'levelDimension': 'Cote de niveau', 'angleDimension': 'Cote angulaire', 'text': 'Texte', 'label': 'Étiquette', 'zone': 'Zone',
    'hatch': 'Hachure', 'line': 'Ligne', 'polyLine': 'Polyligne', 'arc': 'Arc', 'circle': 'Cercle', 'spline': 'Spline',
    'hotspot': 'Point chaud', 'cutPlane': 'Repère de coupe', 'elevation': 'Repère d\'élévation', 'interiorElevation': 'Élévation intérieure',
    'camera': 'Caméra', 'camset': 'Jeu de caméras', 'drawing': 'Dessin (mise en page)', 'sectElem': 'Élément de coupe',
    'detail': 'Repère de détail', 'worksheet': 'Feuille de travail', 'hotlink': 'Module lié (hotlink)', 'picture': 'Image',
    'changeMarker': 'Marqueur de modification', 'curtainWall': 'Mur-rideau', 'cwSegment': 'Segment de mur-rideau',
    'cwFrame': 'Cadre de mur-rideau', 'cwPanel': 'Panneau de mur-rideau', 'cwJunction': 'Jonction de mur-rideau',
    'cwAccessory': 'Accessoire de mur-rideau', 'shell': 'Coque', 'skylight': 'Fenêtre de toit', 'morph': 'Morph',
    'stair': 'Escalier', 'stairRiser': 'Contremarche', 'stairTread': 'Marche', 'stairStructure': 'Structure d\'escalier',
    'railing': 'Garde-corps', 'railingToprail': 'Lisse supérieure', 'railingHandrail': 'Main courante', 'railingRail': 'Lisse',
    'railingPost': 'Poteau de garde-corps', 'railingInnerPost': 'Poteau intermédiaire', 'railingBaluster': 'Balustre',
    'railingPanel': 'Panneau de garde-corps', 'railingSegment': 'Segment de garde-corps', 'railingNode': 'Nœud de garde-corps',
    'railingBalusterSet': 'Jeu de balustres', 'railingPattern': 'Motif de garde-corps', 'railingToprailEnd': 'Extrémité de lisse supérieure',
    'railingHandrailEnd': 'Extrémité de main courante', 'railingRailEnd': 'Extrémité de lisse',
    'railingToprailConnection': 'Raccord de lisse supérieure', 'railingHandrailConnection': 'Raccord de main courante',
    'railingRailConnection': 'Raccord de lisse', 'railingEndFinish': 'Finition d\'extrémité', 'beamSegment': 'Segment de poutre',
    'columnSegment': 'Segment de poteau', 'externalElem': 'Élément externe (autre add-on)', 'opening': 'Ouverture',
}

manque = []
elements = []
for s in d['resume']:
    e = s['element']
    rs = [r for r in d['champs'] if r['element'] == e]
    absents = [r for r in rs if not r['lu']]
    lecture = [r for r in rs if r['lu'] and not r['ecrit']]
    elements.append ({'id': e, 'nom': NOMS.get (e, e), 'struct': s['struct'], 'n': s['champs'], 'lus': s['lus'], 'ecrits': s['ecrits'],
                      'absents': len (absents), 'lecture': len (lecture)})
    for r in absents + lecture:
        manque.append ({'e': e, 'c': r['champ'], 't': r['type'], 's': 'A' if not r['lu'] else 'L',
                        'd': tr.get (r['description'], r['description'])})
elements.sort (key=lambda x: -(x['absents'] + x['lecture']))
non_traduites = sum (1 for r in d['champs'] if not (r['lu'] and r['ecrit']) and r['description'] and r['description'] not in tr)

tot = sum (x['n'] for x in elements)
lus = sum (x['lus'] for x in elements)
ecr = sum (x['ecrits'] for x in elements)
nabs = sum (x['absents'] for x in elements)
nlec = sum (x['lecture'] for x in elements)

DATA = json.dumps ({'elements': elements, 'manque': manque}, ensure_ascii=False)

page = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Options manquantes Tapir</title>
<style>
:root {{
  --fond: #f7f6f2; --carte: #ffffff; --texte: #1d1d1b; --doux: #6b6a64; --ligne: #e3e1da;
  --accent: #2f6f4f; --absent: #b3412e; --absent-fond: #fbeae6; --lecture: #8a6410; --lecture-fond: #fbf1d9; --barre: #e9e7e0;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --fond: #171715; --carte: #22221f; --texte: #ecebe6; --doux: #a3a29b; --ligne: #34332f;
    --accent: #6fbf94; --absent: #ef8a74; --absent-fond: #3a221d; --lecture: #e2b553; --lecture-fond: #352b14; --barre: #34332f;
  }}
}}
:root[data-theme="dark"] {{
  --fond: #171715; --carte: #22221f; --texte: #ecebe6; --doux: #a3a29b; --ligne: #34332f;
  --accent: #6fbf94; --absent: #ef8a74; --absent-fond: #3a221d; --lecture: #e2b553; --lecture-fond: #352b14; --barre: #34332f;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--fond); color: var(--texte); font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 1080px; margin: 0 auto; padding: 28px 16px 64px; }}
h1 {{ font-size: 26px; margin: 0 0 6px; letter-spacing: -0.01em; }}
.sous {{ color: var(--doux); margin: 0 0 22px; }}
.chiffres {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 18px; }}
.chiffre {{ background: var(--carte); border: 1px solid var(--ligne); border-radius: 10px; padding: 12px 14px; }}
.chiffre b {{ display: block; font-size: 24px; font-variant-numeric: tabular-nums; }}
.chiffre span {{ color: var(--doux); font-size: 13px; }}
.note {{ background: var(--carte); border: 1px solid var(--ligne); border-radius: 10px; padding: 12px 16px; margin-bottom: 18px; color: var(--doux); font-size: 14px; }}
.note b {{ color: var(--texte); }}
.outils {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 14px; }}
input[type=search] {{ flex: 1 1 240px; min-width: 0; padding: 9px 12px; border-radius: 8px; border: 1px solid var(--ligne); background: var(--carte); color: var(--texte); font: inherit; }}
.puce {{ border: 1px solid var(--ligne); background: var(--carte); color: var(--texte); border-radius: 999px; padding: 6px 12px; font: inherit; font-size: 13px; cursor: pointer; }}
.puce[aria-pressed=true] {{ background: var(--accent); border-color: var(--accent); color: var(--fond); }}
details {{ background: var(--carte); border: 1px solid var(--ligne); border-radius: 10px; margin-bottom: 8px; }}
summary {{ cursor: pointer; padding: 10px 14px; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 4px 12px; align-items: center; list-style: none; }}
summary::-webkit-details-marker {{ display: none; }}
.nom {{ font-weight: 600; }}
.nom small {{ color: var(--doux); font-weight: 400; margin-left: 6px; font-family: ui-monospace, Consolas, monospace; font-size: 12px; }}
.compte {{ font-size: 13px; color: var(--doux); white-space: nowrap; font-variant-numeric: tabular-nums; }}
.barres {{ grid-column: 1 / -1; display: flex; gap: 10px; font-size: 12px; color: var(--doux); }}
.barre {{ flex: 1; display: flex; align-items: center; gap: 6px; }}
.barre i {{ flex: 1; height: 6px; background: var(--barre); border-radius: 3px; overflow: hidden; }}
.barre i::before {{ content: ""; display: block; height: 100%; width: var(--v); background: var(--accent); }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th, td {{ text-align: left; padding: 7px 14px; border-top: 1px solid var(--ligne); vertical-align: top; }}
th {{ font-size: 12px; color: var(--doux); font-weight: 600; }}
td code {{ font-family: ui-monospace, Consolas, monospace; font-size: 13px; overflow-wrap: anywhere; }}
td:nth-child(3) code {{ overflow-wrap: normal; white-space: nowrap; }}
.etat {{ display: inline-block; border-radius: 6px; padding: 1px 8px; font-size: 12px; white-space: nowrap; }}
.etat.A {{ background: var(--absent-fond); color: var(--absent); }}
.etat.L {{ background: var(--lecture-fond); color: var(--lecture); }}
.vide {{ color: var(--doux); padding: 20px 0; }}
@media (max-width: 640px) {{ th:nth-child(3), td:nth-child(3) {{ display: none; }} }}
</style>
</head>
<body>
<main>
<h1>Options de l'API C++ absentes de Tapir</h1>
<p class="sous">Archicad 29 (DevKit 29.3100) comparé au code de Tapir (branche main du 16/11/2026), champ par champ, pour chaque type d'élément.</p>

<div class="chiffres">
  <div class="chiffre"><b>{len (elements)}</b><span>types d'éléments</span></div>
  <div class="chiffre"><b>{tot}</b><span>options (champs) dans l'API</span></div>
  <div class="chiffre"><b>{round (100 * lus / tot)} %</b><span>lisibles depuis Python ({lus})</span></div>
  <div class="chiffre"><b>{round (100 * ecr / tot)} %</b><span>modifiables depuis Python ({ecr})</span></div>
  <div class="chiffre"><b>{nabs}</b><span>absentes (ni lues ni écrites)</span></div>
  <div class="chiffre"><b>{nlec}</b><span>en lecture seule</span></div>
</div>

<div class="note"><b>Comment lire cette page.</b> « Absente » : Tapir ne lit ni n'écrit ce champ, donc Python n'y a pas accès.
« Lecture seule » : Python peut le lire (GetDetailsOfElements…) mais pas le modifier.
Le repérage se fait en lisant le code C++ de Tapir. Il est donc approximatif : un champ traité par un chemin détourné peut apparaître à tort comme absent.
Ne sont pas comptés : les données hors des structures (polygones, profils, paramètres GDL, propriétés, classifications…) ni les champs réservés.
Les descriptions sont traduites de la documentation du DevKit.</div>

<div class="outils">
  <input type="search" id="q" placeholder="Rechercher un élément, un champ ou un mot (ex. plume, hauteur, Toiture)…" aria-label="Rechercher">
  <button class="puce" data-f="tout" aria-pressed="true">Tout</button>
  <button class="puce" data-f="A" aria-pressed="false">Absentes</button>
  <button class="puce" data-f="L" aria-pressed="false">Lecture seule</button>
  <button class="puce" id="ouvrir" aria-pressed="false">Tout déplier</button>
</div>
<div id="liste"></div>
</main>
<script>
const DATA = {DATA};
const ETAT = {{A: 'Absente', L: 'Lecture seule'}};
let filtre = 'tout', ouvert = false;
const esc = s => String (s).replace (/[&<>"]/g, c => ({{'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}})[c]);
function rendu () {{
  const q = document.getElementById ('q').value.trim ().toLowerCase ();
  const out = [];
  for (const e of DATA.elements) {{
    const nomOk = !q || (e.nom + ' ' + e.id + ' ' + e.struct).toLowerCase ().includes (q);
    const lignes = DATA.manque.filter (m => m.e === e.id && (filtre === 'tout' || m.s === filtre) &&
      (nomOk || (m.c + ' ' + m.d).toLowerCase ().includes (q)));
    if (!lignes.length) continue;
    const pl = Math.round (100 * e.lus / e.n), pe = Math.round (100 * e.ecrits / e.n);
    out.push (`<details ${{ouvert || q ? 'open' : ''}}><summary>
      <span class="nom">${{esc (e.nom)}}<small>${{esc (e.struct)}}</small></span>
      <span class="compte">${{e.absents}} absentes · ${{e.lecture}} lecture seule · ${{e.n}} champs</span>
      <span class="barres"><span class="barre">lus ${{pl}} % <i style="--v:${{pl}}%"></i></span><span class="barre">modifiables ${{pe}} % <i style="--v:${{pe}}%"></i></span></span>
    </summary><table><thead><tr><th>Champ</th><th>État</th><th>Type C++</th><th>Description</th></tr></thead><tbody>` +
      lignes.map (m => `<tr><td><code>${{esc (m.c)}}</code></td><td><span class="etat ${{m.s}}">${{ETAT[m.s]}}</span></td><td><code>${{esc (m.t)}}</code></td><td>${{esc (m.d)}}</td></tr>`).join ('') +
      `</tbody></table></details>`);
  }}
  document.getElementById ('liste').innerHTML = out.join ('') || '<p class="vide">Aucun résultat.</p>';
}}
document.getElementById ('q').addEventListener ('input', rendu);
document.querySelectorAll ('.puce[data-f]').forEach (b => b.addEventListener ('click', () => {{
  filtre = b.dataset.f;
  document.querySelectorAll ('.puce[data-f]').forEach (x => x.setAttribute ('aria-pressed', x === b));
  rendu ();
}}));
document.getElementById ('ouvrir').addEventListener ('click', e => {{
  ouvert = !ouvert; e.target.setAttribute ('aria-pressed', ouvert); e.target.textContent = ouvert ? 'Tout replier' : 'Tout déplier'; rendu ();
}});
rendu ();
</script>
</body>
</html>
'''
(DOS / 'Options_manquantes_Tapir.html').write_text (page, encoding='utf-8')
print ('page ecrite ;', len (manque), 'lignes ; descriptions non traduites :', non_traduites)
