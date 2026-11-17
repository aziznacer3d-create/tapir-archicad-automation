"""Test des reglages par defaut des outils (GetFieldsOfElementDefaults / SetFieldsOfElementDefaults).

A lancer quand Archicad est ouvert sur un NOUVEAU PROJET VIDE, avec la version de test de Tapir.
Pour chaque type d'element :
  1. lit tous les champs des reglages par defaut et les garde dans defauts_origine.json ;
  2. reecrit tous les champs modifiables avec leur propre valeur ;
  3. modifie un par un les champs, verifie qu'Archicad les garde, puis remet l'ancienne valeur ;
puis remet tous les reglages d'origine et verifie qu'ils sont revenus.

Chaque appel est note AVANT d'etre envoye dans journal.jsonl (dossier --sortie) : si Archicad plante,
la derniere ligne dit quel champ l'a fait planter, et le champ est saute au lancement suivant.

Usage : python -I test_defauts.py [--port 19723] [--sortie C:\\ArchicadDev\\Tapir_test_defauts]
        python -I test_defauts.py --remettre    (remet seulement les reglages de defauts_origine.json)
"""
import argparse
import json
import pathlib
import sys

sys.path.insert (0, str (pathlib.Path (__file__).resolve ().parent))
from test_global import Session, ArchicadPlante, nouvelle_valeur, GENRES_MODIFIES, charger_dangereux, marquer_en_cours, fin_en_cours, DEPOT  # noqa: E402


def types_d_elements ():
    schema = json.loads ((DEPOT / 'archicad-addon' / 'Sources' / 'RFIX' / 'Images' / 'CommonSchemaDefinitions.json').read_text (encoding='utf-8'))
    return schema['ElementType']['enum']


def resultat (out):
    return (out.get ('executionResults') or [{}])[0] if isinstance (out, dict) else {}


def remettre (s, origine, defs_cache):
    """Remet les reglages d'origine de chaque type, puis compare a une nouvelle lecture."""
    bilan = {}
    for typ, valeurs in origine.items ():
        defs = defs_cache.get (typ) or {d['path']: d for d in s.tapir ('GetElementFieldDefinitions', {'elementType': typ}, 'definitions').get ('fields', [])}
        modifiables = {p: v for p, v in valeurs.items () if p in defs and not defs[p]['readOnly']}
        if not modifiables:
            continue
        e = resultat (s.tapir ('SetFieldsOfElementDefaults', {'fieldsOfElementDefaults': [{'elementType': typ, 'fields': modifiables}]}, f'{typ} remise generale'))

        def encore_differents ():
            relu = s.tapir ('GetFieldsOfElementDefaults', {'elementTypes': [typ]}, f'{typ} relecture apres remise')
            item = (relu.get ('fieldsOfElementDefaults') or [{}])[0] if isinstance (relu, dict) else {}
            return [p for p, v in valeurs.items () if p in item.get ('fields', {}) and not meme (v, item['fields'][p])]

        differents = encore_differents ()
        # Un seul champ refuse fait refuser tout le bloc : les champs encore differents sont remis un par un.
        if differents:
            for p in differents:
                if p in modifiables:
                    s.tapir ('SetFieldsOfElementDefaults', {'fieldsOfElementDefaults': [{'elementType': typ, 'fields': {p: modifiables[p]}}]}, f'{typ} remise seule {p}')
            differents = encore_differents ()
        bilan[typ] = {'remise': 'ok' if e.get ('success') else json.dumps (e.get ('error', e), ensure_ascii=False)[:300], 'differents': differents}
    return bilan


def meme (a, b):
    if isinstance (a, float) or isinstance (b, float):
        try:
            return abs (float (a) - float (b)) <= 1e-6 * max (1.0, abs (float (a)), abs (float (b)))
        except (TypeError, ValueError):
            return False
    return a == b


def main ():
    ap = argparse.ArgumentParser ()
    ap.add_argument ('--port', type=int, default=19723)
    ap.add_argument ('--sortie', default=r'C:\ArchicadDev\Tapir_test_defauts')
    ap.add_argument ('--remettre', action='store_true')
    a = ap.parse_args ()
    sortie = pathlib.Path (a.sortie)
    sortie.mkdir (parents=True, exist_ok=True)
    s = Session (a.port, sortie)
    s.dangereux = charger_dangereux (sortie)
    f_origine = sortie / 'defauts_origine.json'
    defs_cache = {}

    if a.remettre:
        bilan = remettre (s, json.loads (f_origine.read_text (encoding='utf-8')), defs_cache)
        print (json.dumps (bilan, ensure_ascii=False, indent=1))
        return

    # 1. Lecture de tous les reglages par defaut ; la premiere lecture est gardee pour pouvoir tout remettre.
    origine = json.loads (f_origine.read_text (encoding='utf-8')) if f_origine.exists () else {}
    res = {}
    for typ in types_d_elements ():
        out = s.tapir ('GetFieldsOfElementDefaults', {'elementTypes': [typ]}, f'{typ} lecture')
        item = (out.get ('fieldsOfElementDefaults') or [{}])[0] if isinstance (out, dict) else {}
        if 'fields' not in item:
            res[typ] = {'lecture': 'erreur : ' + json.dumps (item.get ('error', out), ensure_ascii=False)[:200]}
            continue
        origine.setdefault (typ, item['fields'])
        res[typ] = {'lecture': 'ok', 'lus': len (item['fields']), 'reecriture': {}, 'modification': {}}
    f_origine.write_text (json.dumps (origine, ensure_ascii=False, indent=0), encoding='utf-8')
    print (f'Reglages lus : {sum (1 for r in res.values () if r["lecture"] == "ok")} types sur {len (res)}', flush=True)

    try:
        for typ, r in res.items ():
            if r['lecture'] != 'ok':
                continue
            print (f'  {typ}', flush=True)
            defs = defs_cache.setdefault (typ, {d['path']: d for d in s.tapir ('GetElementFieldDefinitions', {'elementType': typ}, 'definitions').get ('fields', [])})
            valeurs = origine[typ]
            modifiables = {p: v for p, v in valeurs.items () if p in defs and not defs[p]['readOnly'] and f'{typ}:{p}' not in s.dangereux}

            # 2. Reecriture identique d'un bloc ; en cas d'echec, champ par champ.
            marquer_en_cours (s, f'{typ}:*reecriture')
            e = resultat (s.tapir ('SetFieldsOfElementDefaults', {'fieldsOfElementDefaults': [{'elementType': typ, 'fields': modifiables}]}, f'{typ} reecriture globale')) if f'{typ}:*reecriture' not in s.dangereux else {}
            fin_en_cours (s)
            if e.get ('success'):
                for p in modifiables:
                    r['reecriture'][p] = 'ok'
            else:
                for p, v in modifiables.items ():
                    marquer_en_cours (s, f'{typ}:{p}')
                    e1 = resultat (s.tapir ('SetFieldsOfElementDefaults', {'fieldsOfElementDefaults': [{'elementType': typ, 'fields': {p: v}}]}, f'{typ} reecriture {p}'))
                    fin_en_cours (s)
                    r['reecriture'][p] = 'ok' if e1.get ('success') else 'refuse : ' + json.dumps (e1.get ('error', e1), ensure_ascii=False)[:300]

            # 3. Modification un par un, puis remise de l'ancienne valeur.
            for p, v in modifiables.items ():
                kind = defs[p]['kind']
                if kind not in GENRES_MODIFIES:
                    continue
                nv = nouvelle_valeur (kind, v, defs[p]['size'])
                if nv is None:
                    continue
                marquer_en_cours (s, f'{typ}:{p}')
                e1 = resultat (s.tapir ('SetFieldsOfElementDefaults', {'fieldsOfElementDefaults': [{'elementType': typ, 'fields': {p: nv}}]}, f'{typ} modification {p}'))
                if e1.get ('success'):
                    r['modification'][p] = 'garde'
                else:
                    msg = json.dumps (e1.get ('error', e1), ensure_ascii=False)
                    r['modification'][p] = ('non garde : ' if 'did not keep' in msg else 'refuse : ') + msg[:300]
                s.tapir ('SetFieldsOfElementDefaults', {'fieldsOfElementDefaults': [{'elementType': typ, 'fields': {p: v}}]}, f'{typ} remise {p}')
                fin_en_cours (s)
    except ArchicadPlante as ex:
        print (f'\nArchicad ne repond plus : {ex}')
        (sortie / 'resultats.json').write_text (json.dumps (res, ensure_ascii=False, indent=1), encoding='utf-8')
        sys.exit (1)

    # 4. Remise de tous les reglages d'origine, et verification.
    bilan = remettre (s, origine, defs_cache)
    (sortie / 'resultats.json').write_text (json.dumps ({'types': res, 'remise': bilan}, ensure_ascii=False, indent=1), encoding='utf-8')

    lignes = ['| Type | Lus | Reecrits OK | Modifies gardes | Non gardes | Refuses | Remis a l origine |', '|---|---|---|---|---|---|---|']
    for typ, r in res.items ():
        if r['lecture'] != 'ok':
            continue
        m = r['modification'].values ()
        b = bilan.get (typ, {})
        remis = 'oui' if b.get ('remise', 'ok') == 'ok' and not b.get ('differents') else f'NON ({", ".join (b.get ("differents", [])[:5])})'
        lignes.append (f'| {typ} | {r["lus"]} | {sum (1 for x in r["reecriture"].values () if x == "ok")} / {len (r["reecriture"])} | '
                       f'{sum (1 for x in m if x == "garde")} | {sum (1 for x in m if x.startswith ("non garde"))} | {sum (1 for x in m if x.startswith ("refuse"))} | {remis} |')
    sans = [f'- {typ} : {r["lecture"]}' for typ, r in res.items () if r['lecture'] != 'ok']
    texte = '# Test des reglages par defaut\n\n' + '\n'.join (lignes) + '\n\n## Types sans reglages lus\n\n' + '\n'.join (sans) + '\n'
    (sortie / 'rapport.md').write_text (texte, encoding='utf-8')
    print ('\nTermine sans plantage. Rapport : ' + str (sortie / 'rapport.md'))


if __name__ == '__main__':
    main ()
