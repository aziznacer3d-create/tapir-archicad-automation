"""Test global des options de Tapir (version de test) dans Archicad 29.

A lancer quand Archicad 29 est ouvert sur un NOUVEAU PROJET VIDE, sans titre, avec la version de test
de Tapir chargee. Le script cree des elements, puis pour chaque type d'element :
  1. lit tous les champs (GetElementFields) ;
  2. reecrit tous les champs modifiables avec leur propre valeur (SetElementFields) ;
  3. modifie un par un les champs nombre et oui/non, verifie qu'Archicad les garde, puis remet l'ancienne valeur ;
puis teste les modeles des garde-corps (pattern, post) et lance tous les tests JSON du depot.

Chaque appel est note AVANT d'etre envoye dans journal.jsonl : si Archicad plante, la derniere ligne
dit quel champ l'a fait planter. Les resultats vont dans le dossier --sortie (rapport.md, resultats.json).

Usage : python -I test_global.py [--port 19723] [--sortie C:\\ArchicadDev\\Tapir_test_global] [--sans-checks]
"""
import argparse
import collections
import datetime
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ICI = pathlib.Path (__file__).resolve ().parent
# Le depot Tapir : celui qui contient ce script (suivi/outils dans la branche de suivi), sinon le clone de l'ordinateur d'origine.
DEPOT = next ((p for p in ICI.parents if (p / 'archicad-addon' / 'Test' / 'checks').is_dir ()),
              pathlib.Path (r'C:\Users\admin\Documents\RECHERCHE\tapir-archicad-automation'))
# Les recettes de creation des elements : a cote du script si elles y sont.
RECETTES = ICI / 'recettes_creation.json' if (ICI / 'recettes_creation.json').exists () else pathlib.Path (r'C:\ArchicadDev\Tapir_couverture\recettes_creation.json')


class ArchicadPlante (Exception):
    pass


class Session:
    def __init__ (self, port, sortie):
        self.port = port
        self.sortie = sortie
        self.journal = open (sortie / 'journal.jsonl', 'a', encoding='utf-8')

    def note (self, **kw):
        kw['t'] = datetime.datetime.now ().strftime ('%H:%M:%S')
        self.journal.write (json.dumps (kw, ensure_ascii=False) + '\n')
        self.journal.flush ()

    def tapir (self, name, params, contexte=''):
        self.note (appel=name, contexte=contexte, params=params if len (json.dumps (params)) < 2000 else '(long)')
        body = {'command': 'API.ExecuteAddOnCommand',
                'parameters': {'addOnCommandId': {'commandNamespace': 'TapirCommand', 'commandName': name},
                               'addOnCommandParameters': params}}
        req = urllib.request.Request (f'http://127.0.0.1:{self.port}', json.dumps (body).encode (), {'Content-Type': 'application/json'})
        attente = 0
        while True:
            try:
                with urllib.request.urlopen (req, timeout=180) as r:
                    res = json.load (r)
            except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
                raise ArchicadPlante (f'{name} ({contexte}) : {e}')
            err = res.get ('error') if not res.get ('succeeded') else None
            # Une fenetre ouverte dans Archicad (avertissement, reglages...) fait refuser tous les appels :
            # on attend qu'elle soit fermee au lieu de compter des refus qui n'en sont pas.
            if isinstance (err, dict) and err.get ('code') == 4001 and 'modal dialog' in str (err.get ('message', '')) and attente < 1800:
                if attente % 30 == 0:
                    print (f'\n   Une fenêtre est ouverte dans Archicad ({err.get ("message")}) : fermez-la, le test reprendra.')
                    self.note (fenetre_ouverte=err.get ('message'), appel=name)
                time.sleep (2)
                attente += 2
                continue
            break
        if not res.get ('succeeded'):
            self.note (reponse_erreur=res.get ('error', res))
            return {'ERREUR': res.get ('error', res)}
        out = res['result']['addOnCommandResponse']
        # Les erreurs renvoyees dans la reponse (resultats d'execution, elements en erreur) sont notees.
        txt = json.dumps (out, ensure_ascii=False)
        if '"error"' in txt and name != 'GetElementFields':
            self.note (reponse_erreur=txt[:1500])
        return out


def montrer_calques (s, rapport):
    """Affiche et deverrouille tous les calques : Archicad refuse de modifier un element sur un calque masque."""
    calques = s.tapir ('GetAttributesByType', {'attributeType': 'Layer'}, 'calques').get ('attributes', [])
    r = s.tapir ('ModifyLayers', {'layers': [{'attributeId': c['attributeId'], 'isHidden': False, 'isLocked': False} for c in calques]}, 'calques visibles')
    rapport['calques'] = f'{len (calques)} calques affiches et deverrouilles' if 'ERREUR' not in r else 'echec : ' + json.dumps (r, ensure_ascii=False)[:300]


# Recettes de secours (exemples du depot) pour les creations sans recette dans les tests JSON.
SECOURS = {
    'CreateCurtainWalls': [{'curtainWallsData': [{'coordinates': [{'x': 1300.0, 'y': 1300.0}, {'x': 1306.0, 'y': 1300.0}], 'zCoordinate': 0.0, 'height': 3.0,
                                                   'primaryPattern': {'sizes': [1.5], 'logic': 'FixedSizes'},
                                                   'secondaryPattern': {'sizes': [1.0, 2.0], 'logic': 'FixedSizes'}}]}],
}


def ids (r):
    return [e['elementId'] for e in (r.get ('elements') or []) if isinstance (e, dict) and 'elementId' in e] if isinstance (r, dict) else []


def creer_supplementaires (s, rapport):
    """Les types qui demandent un hote, un element de bibliotheque ou un jeu de cameras (exemples du depot)."""
    crees = []

    def note (nom, liste):
        rapport['creation'][nom] = f'ok ({len (liste)})' if liste else 'echec'
        crees.extend (liste)
        return liste

    mur = ids (s.tapir ('CreateWalls', {'wallsData': [{'begCoordinate': {'x': 1400.0, 'y': 1400.0}, 'endCoordinate': {'x': 1410.0, 'y': 1400.0},
                                                        'height': 3.0, 'thickness': 0.3}]}, 'creation hote'))
    if mur:
        note ('CreateWindows', ids (s.tapir ('CreateWindows', {'windowsData': [{'ownerWallId': mur[0], 'centerOffset': 2.0, 'sillHeight': 0.9,
                                                                                  'width': 1.0, 'height': 1.5}]}, 'creation')))
        note ('CreateDoors', ids (s.tapir ('CreateDoors', {'doorsData': [{'ownerWallId': mur[0], 'centerOffset': 5.0, 'width': 1.0, 'height': 2.1}]}, 'creation')))
        note ('CreateOpenings', ids (s.tapir ('CreateOpenings', {'openingsData': [{'ownerElementId': mur[0], 'basePoint': {'x': 1408.0, 'y': 1400.0, 'z': 1.0},
                                                                                     'width': 0.8, 'height': 0.8}]}, 'creation')))
    toit = ids (s.tapir ('CreateRoofs', {'roofsData': [{'level': 3.0, 'polygonCoordinates': [{'x': 1420.0, 'y': 1400.0}, {'x': 1428.0, 'y': 1400.0},
                                                                                             {'x': 1428.0, 'y': 1408.0}, {'x': 1420.0, 'y': 1408.0}],
                                                        'pivotLine': {'begCoordinate': {'x': 1420.0, 'y': 1400.0}, 'endCoordinate': {'x': 1428.0, 'y': 1400.0}},
                                                        'angle': 0.5}]}, 'creation hote'))
    if toit:
        note ('CreateSkylights', ids (s.tapir ('CreateSkylights', {'skylightsData': [{'ownerId': toit[0], 'anchorPosition': {'x': 1424.0, 'y': 1403.0}}]}, 'creation')))
    for cmd, cle, typ, extra in (('CreateObjects', 'objectsData', 'Object', {'coordinates': {'x': 1440.0, 'y': 1400.0, 'z': 0.0}}),
                                 ('CreateLamps', 'lampsData', 'Lamp', {'coordinates': {'x': 1444.0, 'y': 1400.0, 'z': 2.5}})):
        parts = s.tapir ('GetAvailableLibraryParts', {'filterByTypeId': typ}, 'bibliotheque').get ('libraryParts', [])
        # Les accessoires, maitres et macros de la bibliotheque ne se posent pas : on les saute.
        parts = [lp for lp in parts if not re.search (r'accessoire|master|macro|_m$|rhino', lp.get ('documentName', ''), re.I)]
        liste = []
        for lp in parts[:25]:
            liste = ids (s.tapir (cmd, {cle: [dict (extra, libraryPartName=lp['documentName'])]}, 'creation'))
            if liste:
                break
        note (cmd, liste)
    jeu = ids (s.tapir ('CreateCameraSets', {'cameraSets': [{'name': 'Tapir test global', 'isActive': True}]}, 'creation'))
    if jeu:
        crees.extend (jeu)
        note ('CreateCameras', ids (s.tapir ('CreateCameras', {'cameras': [{'cameraSetElementId': jeu[0], 'cameraPosition': {'x': 1450.0, 'y': 1390.0, 'z': 1.7},
                                                                              'targetPosition': {'x': 1450.0, 'y': 1400.0, 'z': 1.5}}]}, 'creation')))
    s.tapir ('ChangeWindow', {'windowType': 'FloorPlan'}, 'plan')
    note ('CreateElevations', ids (s.tapir ('CreateElevations', {'elevationsData': [{'startCoordinate': {'x': 1400.0, 'y': 1380.0},
                                                                                       'endCoordinate': {'x': 1410.0, 'y': 1380.0}, 'depth': 20.0,
                                                                                       'name': 'Tapir test global', 'id': 'TG-1'}]}, 'creation')))
    # Un garde-corps dont le motif montre ses panneaux : il en a alors, que le test lit aussi.
    gc = ids (s.tapir ('CreateRailings', {'railingsData': [{'coordinates': [{'x': 1460.0, 'y': 1400.0}, {'x': 1464.0, 'y': 1400.0}],
                                                            'floorIndex': 0, 'bottomOffset': 0.0, 'height': 1.0}]}, 'creation'))
    if gc:
        s.tapir ('ModifyRailings', {'railingsWithDetails': [{'elementId': gc[0], 'segments': [{'index': 0, 'pattern': {'panel': {'visible': True}}}]}]}, 'panneaux visibles')
        note ('Garde-corps avec panneaux', gc)
    return crees


def creer_elements (s, rapport):
    recettes = json.loads (RECETTES.read_text (encoding='utf-8'))
    for cmd, params in SECOURS.items ():
        recettes.setdefault (cmd, [])
        recettes[cmd] = recettes[cmd] + [{'fichier': 'secours', 'params': p} for p in params]
    crees = []
    for cmd, liste in sorted (recettes.items ()):
        if cmd.startswith (('CreateElectrical', 'CreateMEP', 'CreateElementsFromAnalytical')):
            continue
        ok = False
        derniere_erreur = ''
        for rec in liste:
            r = s.tapir (cmd, rec['params'], 'creation')
            elems = [e['elementId'] for e in (r.get ('elements') or []) if isinstance (e, dict) and 'elementId' in e]
            if elems:
                crees.extend (elems[:4])  # jusqu'a 4 : plus de variantes (toits plan / multi-pans, coques...)
                ok = True
                break
            derniere_erreur = json.dumps (r, ensure_ascii=False)[:300]
        rapport['creation'][cmd] = 'ok' if ok else 'echec : ' + derniere_erreur
    crees.extend (creer_supplementaires (s, rapport))
    # Sous-elements (murs-rideaux, escaliers, garde-corps, segments de poutres et poteaux...).
    r = s.tapir ('GetSubelementsOfHierarchicalElements', {'elements': [{'elementId': e} for e in crees]}, 'sous-elements')
    for sub in r.get ('subelements', []) if isinstance (r, dict) else []:
        if not isinstance (sub, dict):
            continue
        for cle, liste in sub.items ():
            if isinstance (liste, list):
                crees.extend ([x['elementId'] for x in liste[:2] if isinstance (x, dict) and 'elementId' in x])
    return crees


def nouvelle_valeur (kind, v, size):
    """Une valeur voisine de v pour un champ : oui/non inverse, nombre +5 %, entier ou liste +1, texte + « T »."""
    if kind == 'Bool':
        return not v
    if kind == 'Real':
        if abs (v) < 1e-9:
            return 0.01
        return round (v * 1.05 if abs (v) > 0.2 else v + 0.01, 6)
    if kind in ('SignedInt', 'UnsignedInt', 'AttributeIndex'):
        if not isinstance (v, int) or isinstance (v, bool):
            return None
        if kind == 'UnsignedInt':
            maxi = (1 << (8 * size)) - 1
        elif kind == 'SignedInt':
            maxi = (1 << (8 * size - 1)) - 1
        else:
            maxi = 2 ** 31 - 1
        return v - 1 if v >= maxi else v + 1
    if kind in ('CString', 'UString') and isinstance (v, str):
        place = size - 1 if kind == 'CString' else size // 2 - 1
        longueur = len (v.encode ('utf-8')) if kind == 'CString' else len (v)
        if place <= 0:
            return None
        return v + 'T' if longueur + 1 <= place else (v[:-1] + 'T' if v else 'T')
    return None


GENRES_MODIFIES = ('Real', 'Bool', 'SignedInt', 'UnsignedInt', 'AttributeIndex', 'CString', 'UString')


def charger_dangereux (sortie):
    """Les champs qui ont fait planter Archicad lors d'un test precedent (« Type:chemin »)."""
    f = sortie / 'champs_dangereux.json'
    dangereux = set (json.loads (f.read_text (encoding='utf-8'))) if f.exists () else set ()
    en_cours = sortie / 'en_cours.json'
    if en_cours.exists ():
        dangereux.add (json.loads (en_cours.read_text (encoding='utf-8')))
        en_cours.unlink ()
        f.write_text (json.dumps (sorted (dangereux), ensure_ascii=False, indent=0), encoding='utf-8')
    return dangereux


def marquer_en_cours (s, cle):
    (s.sortie / 'en_cours.json').write_text (json.dumps (cle, ensure_ascii=False), encoding='utf-8')


def fin_en_cours (s):
    f = s.sortie / 'en_cours.json'
    if f.exists ():
        f.unlink ()


def tester_element (s, guid, defs_cache, res):
    lu = s.tapir ('GetElementFields', {'elements': [{'elementId': guid}]}, 'lecture')
    item = (lu.get ('elementFields') or [{}])[0] if isinstance (lu, dict) else {}
    if 'fields' not in item:
        return None
    typ = item['elementType']
    if typ not in defs_cache:
        defs_cache[typ] = {d['path']: d for d in s.tapir ('GetElementFieldDefinitions', {'elementType': typ}, 'definitions').get ('fields', [])}
    defs = defs_cache[typ]
    valeurs = item['fields']
    r = res.setdefault (typ, {'struct': item['structName'], 'champs': len (defs), 'lus': len (valeurs), 'elements': 0,
                              'reecriture': {}, 'modification': {}})
    r['elements'] += 1
    modifiables = {p: v for p, v in valeurs.items () if p in defs and not defs[p]['readOnly']}

    dangereux = s.dangereux
    for p in list (modifiables):
        if f'{typ}:{p}' in dangereux:
            del modifiables[p]
            r['reecriture'][p] = 'ignore : a fait planter Archicad lors d un test precedent'

    # 2. Reecriture identique de tous les champs, d'un bloc ; en cas d'echec, champ par champ.
    er = {}
    if f'{typ}:*reecriture' not in dangereux:
        marquer_en_cours (s, f'{typ}:*reecriture')
        out = s.tapir ('SetElementFields', {'elementsWithFields': [{'elementId': guid, 'fields': modifiables}]}, f'{typ} reecriture globale')
        fin_en_cours (s)
        er = (out.get ('executionResults') or [{}])[0] if isinstance (out, dict) else {}
    if er.get ('success'):
        for p in modifiables:
            r['reecriture'].setdefault (p, 'ok')
    else:
        for p, v in modifiables.items ():
            marquer_en_cours (s, f'{typ}:{p}')
            o = s.tapir ('SetElementFields', {'elementsWithFields': [{'elementId': guid, 'fields': {p: v}}]}, f'{typ} reecriture {p}')
            fin_en_cours (s)
            e = (o.get ('executionResults') or [{}])[0] if isinstance (o, dict) else {}
            r['reecriture'][p] = 'ok' if e.get ('success') else ('refuse : ' + json.dumps (e.get ('error', o), ensure_ascii=False)[:300])

    # 3. Modification un par un (nombres, oui/non, entiers, listes, index d'attributs, textes), puis
    #    remise de l'ancienne valeur. Les identifiants (guid) ne sont pas changes au hasard.
    for p, v in modifiables.items ():
        kind = defs[p]['kind']
        if kind not in GENRES_MODIFIES or p in r['modification'] and r['modification'][p] == 'garde':
            continue
        nv = nouvelle_valeur (kind, v, defs[p]['size'])
        if nv is None:
            continue
        r.setdefault ('genres', {})[p] = kind
        marquer_en_cours (s, f'{typ}:{p}')
        o = s.tapir ('SetElementFields', {'elementsWithFields': [{'elementId': guid, 'fields': {p: nv}}]}, f'{typ} modification {p}')
        e = (o.get ('executionResults') or [{}])[0] if isinstance (o, dict) else {}
        if e.get ('success'):
            r['modification'][p] = 'garde'
        else:
            msg = json.dumps (e.get ('error', o), ensure_ascii=False)
            r['modification'][p] = ('non garde : ' if 'did not keep' in msg else 'refuse : ') + msg[:300]
        s.tapir ('SetElementFields', {'elementsWithFields': [{'elementId': guid, 'fields': {p: v}}]}, f'{typ} remise {p}')
        fin_en_cours (s)
    return typ


def tester_garde_corps (s, rapport):
    r = s.tapir ('CreateRailings', {'railingsData': [{'coordinates': [{'x': 1200.0, 'y': 1200.0}, {'x': 1204.0, 'y': 1200.0}, {'x': 1204.0, 'y': 1203.0}],
                                                      'floorIndex': 0, 'bottomOffset': 0.0, 'height': 1.0}]}, 'garde-corps')
    rg = r['elements'][0]['elementId']['guid']
    essais = [
        ('motif du segment 1 : poteau intermediaire double', {'segments': [{'index': 1, 'pattern': {'innerPost': {'doublePostOffset': 0.06, 'postCount': 2}}}]}),
        ('motif du segment 0 : balustres par longueur 0,12', {'segments': [{'index': 0, 'pattern': {'balusterSet': {'distribution': {'type': 'PatternLength', 'length': 0.12}}}}]}),
        ('motif du segment 1 : repartition du motif', {'segments': [{'index': 1, 'pattern': {'distribution': {'type': 'PatternLength', 'length': 1.5}}}]}),
        ('modele de poteau du noeud 1 : jusqu a la lisse 1', {'nodes': [{'index': 1, 'post': {'verticalPosition': {'bottomRailIndex': 0, 'topRailIndex': 1}}}]}),
        ('poteau intermediaire seul (doit renvoyer vers pattern)', {'segments': [{'index': 1, 'innerPosts': [{'index': 0, 'doublePostOffset': 0.05}]}]}),
    ]
    for titre, entree in essais:
        o = s.tapir ('ModifyRailings', {'railingsWithDetails': [dict (entree, elementId={'guid': rg})]}, f'garde-corps {titre}')
        e = (o.get ('executionResults') or [{}])[0] if isinstance (o, dict) else {}
        rapport['garde_corps'][titre] = 'ok' if e.get ('success') else json.dumps (e.get ('error', o), ensure_ascii=False)[:400]


def lancer_checks (sortie, port):
    """Lance les tests JSON du depot un fichier a la fois, en notant le fichier en cours : si Archicad
    plante, ce fichier est mis de cote et le test suivant reprend apres lui."""
    runner = DEPOT / 'tools' / 'community-test-runner' / 'tapir_test_runner.py'
    fichiers = sorted ((DEPOT / 'archicad-addon' / 'Test' / 'checks').glob ('*.json'))
    f_prog = sortie / 'checks_progression.json'
    f_dang = sortie / 'checks_dangereux.json'
    f_cours = sortie / 'check_en_cours.json'
    prog = json.loads (f_prog.read_text (encoding='utf-8')) if f_prog.exists () else {}
    dang = set (json.loads (f_dang.read_text (encoding='utf-8'))) if f_dang.exists () else set ()
    if f_cours.exists ():
        dang.add (json.loads (f_cours.read_text (encoding='utf-8')))
        f_cours.unlink ()
        f_dang.write_text (json.dumps (sorted (dang), ensure_ascii=False, indent=0), encoding='utf-8')
    plante = None
    for i, f in enumerate (fichiers):
        if f.name in prog or f.name in dang:
            continue
        print (f'   {i + 1}/{len (fichiers)} {f.name[:70]:70s}', end='\r')
        f_cours.write_text (json.dumps (f.name), encoding='utf-8')
        try:
            p = subprocess.run ([sys.executable, '-I', str (runner), 'check', '--port', str (port), '--brief', str (f)],
                                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
            sortie_txt = (p.stdout + p.stderr).strip ()
        except subprocess.TimeoutExpired:
            sortie_txt = 'stopped: timeout'
        if 'stopped:' in sortie_txt and ('no answer' in sortie_txt or 'timeout' in sortie_txt):
            plante = f.name
            break
        f_cours.unlink ()
        prog[f.name] = sortie_txt
        f_prog.write_text (json.dumps (prog, ensure_ascii=False, indent=0), encoding='utf-8')
    print ()
    ok = sum (1 for v in prog.values () if ' PASS ' in v.splitlines ()[0])
    lignes = [f'{len (prog)} fichiers lancés sur {len (fichiers)} : {ok} entièrement réussis, {len (prog) - ok} avec des échecs.']
    if dang:
        lignes.append ('Fichiers mis de côté car Archicad a planté pendant leur test : ' + ', '.join (sorted (dang)))
    if plante:
        lignes.append (f'ARCHICAD A PLANTÉ pendant le test {plante} : il sera mis de côté au prochain lancement.')
    detail = ['# Tests JSON du dépôt, fichier par fichier', ''] + lignes + ['']
    for nom, v in sorted (prog.items ()):
        if ' PASS ' not in v.splitlines ()[0]:
            detail += [f'## {nom}', '', '```', v[:3000], '```', '']
    (sortie / 'checks_depot.md').write_text ('\n'.join (detail), encoding='utf-8')
    return ' '.join (lignes)


def ecrire_rapport (sortie, rapport, res, fin):
    (sortie / 'resultats.json').write_text (json.dumps ({'rapport': rapport, 'types': res}, ensure_ascii=False, indent=1), encoding='utf-8')
    L = [f'# Test global de Tapir — {datetime.datetime.now ():%d/%m/%Y %H:%M}', '', fin, '', f"Calques : {rapport.get ('calques', '?')}", '']
    if rapport.get ('dangereux'):
        L += ['Champs ignorés car ils ont fait planter Archicad : ' + ', '.join (rapport['dangereux']), '']
    L += ['## Créations', ''] + [f'- {k} : {v}' for k, v in sorted (rapport['creation'].items ())] + ['']
    L += ['## Champs par type d\'élément', '', '| Type | Champs | Lus | Réécrits OK | Réécrits refusés | Modifiés gardés | Non gardés / refusés |', '|---|---|---|---|---|---|---|']
    for typ, r in sorted (res.items ()):
        rok = sum (1 for v in r['reecriture'].values () if v == 'ok')
        rko = len (r['reecriture']) - rok
        mok = sum (1 for v in r['modification'].values () if v == 'garde')
        mko = len (r['modification']) - mok
        L.append (f"| {typ} | {r['champs']} | {r['lus']} | {rok} | {rko} | {mok} | {mko} |")
    noms = {'Real': 'nombres', 'Bool': 'oui/non', 'SignedInt': 'entiers et listes', 'UnsignedInt': 'entiers sans signe',
            'AttributeIndex': 'index d\'attributs', 'CString': 'textes', 'UString': 'textes Unicode'}
    par_genre = collections.defaultdict (lambda: [0, 0, 0])
    for r in res.values ():
        for p, v in r['modification'].items ():
            g = r.get ('genres', {}).get (p, 'Real')
            par_genre[g][0 if v == 'garde' else (1 if v.startswith ('non garde') else 2)] += 1
    L += ['', '## Modifications par genre de champ', '', '| Genre | Gardés | Recalculés (non gardés) | Refusés |', '|---|---|---|---|']
    for g, (a, b, c) in sorted (par_genre.items (), key=lambda x: -sum (x[1])):
        L.append (f'| {noms.get (g, g)} | {a} | {b} | {c} |')
    L += ['', '## Garde-corps : modèles', ''] + [f'- {k} : {v}' for k, v in rapport['garde_corps'].items ()]
    L += ['', '## Tests JSON du dépôt', '', rapport.get ('vidage', ''), '', rapport.get ('checks', '(non lancés)'), '']
    L += ['## Détail des refus', '']
    for typ, r in sorted (res.items ()):
        for p, v in sorted (r['reecriture'].items ()):
            if v != 'ok':
                L.append (f'- {typ} `{p}` réécriture : {v}')
        for p, v in sorted (r['modification'].items ()):
            if v != 'garde':
                L.append (f'- {typ} `{p}` modification : {v}')
    (sortie / 'rapport.md').write_text ('\n'.join (L) + '\n', encoding='utf-8')


def main ():
    ap = argparse.ArgumentParser ()
    ap.add_argument ('--port', type=int, default=19723)
    ap.add_argument ('--sortie', default=r'C:\ArchicadDev\Tapir_test_global')
    ap.add_argument ('--sans-checks', action='store_true')
    ap.add_argument ('--seulement-checks', action='store_true', help='ne lance que les tests JSON du depot (reprend ou ils se sont arretes)')
    ap.add_argument ('--seulement-champs', action='store_true', help='ne lance que le test des champs et des modeles de garde-corps')
    a = ap.parse_args ()
    sortie = pathlib.Path (a.sortie)
    sortie.mkdir (parents=True, exist_ok=True)
    s = Session (a.port, sortie)
    s.dangereux = charger_dangereux (sortie)
    if s.dangereux:
        print ('Champs ignorés (ont fait planter Archicad) :', ', '.join (sorted (s.dangereux)))
    rapport = {'creation': {}, 'garde_corps': {}, 'dangereux': sorted (s.dangereux)}
    res = {}
    fin = 'Terminé sans plantage.'
    debut = time.time ()
    try:
        v = s.tapir ('GetAddOnVersion', {}, 'version')
        info = s.tapir ('GetProjectInfo', {}, 'projet')
        print ('Tapir', v.get ('version'), '| projet sans titre :', info.get ('isUntitled'))
        if not info.get ('isUntitled'):
            sys.exit ('Arrêt : ouvrez un NOUVEAU projet vide sans titre avant le test.')
        if a.seulement_checks:
            montrer_calques (s, rapport)
            print ('Tests JSON du dépôt seulement…')
            resultat = lancer_checks (sortie, a.port)
            print ('   ', resultat)
            (sortie / 'rapport_checks.md').write_text (f'# Tests JSON du dépôt — {datetime.datetime.now ():%d/%m/%Y %H:%M}\n\n{resultat}\n', encoding='utf-8')
            return
        montrer_calques (s, rapport)
        print ('Calques :', rapport['calques'])
        print ('1/4 Création des éléments…')
        elements = creer_elements (s, rapport)
        print (f'   {len (elements)} éléments et sous-éléments')
        print ('2/4 Lecture, réécriture et modification des champs…')
        defs_cache = {}
        vus = collections.Counter ()
        for i, guid in enumerate (elements):
            typ = tester_element (s, guid, defs_cache, res) if vus.total () < 10_000 else None
            if typ:
                vus[typ] += 1
            print (f'   {i + 1}/{len (elements)} {typ or "-"}', end='\r')
        print ()
        print ('3/4 Modèles des garde-corps…')
        tester_garde_corps (s, rapport)
        if not a.sans_checks and not a.seulement_champs:
            # Les tests du depot demandent un projet vide : tout ce que le test a cree est supprime.
            tous = s.tapir ('GetAllElements', {}, 'vider le projet').get ('elements', [])
            if tous:
                s.tapir ('DeleteElements', {'elements': tous}, 'vider le projet')
            reste = s.tapir ('GetAllElements', {}, 'projet vide ?').get ('elements', [])
            rapport['vidage'] = f'{len (tous)} éléments supprimés avant les tests du dépôt, {len (reste)} restants'
            print ('   ', rapport['vidage'])
            print ('4/4 Tests JSON du dépôt (quelques minutes)…')
            rapport['checks'] = lancer_checks (sortie, a.port)
            print ('   ', rapport['checks'])
    except ArchicadPlante as e:
        fin = f'ARCHICAD A PLANTÉ (ou ne répond plus) pendant : {e}. La dernière ligne de journal.jsonl donne l\'appel exact.'
        print (fin)
    fin += f' Durée : {int (time.time () - debut)} s.'
    ecrire_rapport (sortie, rapport, res, fin)
    print ('Rapport :', sortie / 'rapport.md')


if __name__ == '__main__':
    main ()
