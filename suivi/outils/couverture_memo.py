"""Couverture du MEMO des elements (API_ElementMemo) : chaque donnee est-elle lue / ecrite par Tapir ?

Le memo tient les donnees de taille variable d'un element : contour (coords, pends, parcs), parametres
GDL (params), pignons, aretes, materiaux des cotes, texte, sous-elements d'un mur-rideau, d'un escalier,
d'un garde-corps, segments d'une poutre... Pour chaque membre :
- lu    : le code atteint memo.<membre> (ou une variable API_ElementMemo) ;
- ecrit : le membre recoit une valeur (memo.coords = ..., (*memo.coords)[i].x = ..., data.Get (..., memo.x)) ;
et pour les membres qui sont des tableaux de petites structures (API_Gable, API_EdgeTrim...), chacun de leurs champs.
Les masques APIMemoMask_* utilises par le code sont aussi releves.

Usage : python -I couverture_memo.py <dossier Inc du DevKit> <dossier Sources de Tapir> <dossier de sortie>
"""
import collections
import csv
import json
import pathlib
import re
import sys

sys.path.insert (0, str (pathlib.Path (__file__).resolve ().parent))
INC = pathlib.Path (sys.argv[1])
SRC = pathlib.Path (sys.argv[2])
OUT = pathlib.Path (sys.argv[3])
OUT.mkdir (parents=True, exist_ok=True)


def brief_of (doc):
    m = re.search (r'@brief\s+(.*?)(?:\n\s*\*\s*@|\Z)', doc, re.S)
    return re.sub (r'\s*\n\s*\*\s*', ' ', m.group (1)).strip () if m else ''


def find_matching (text, i):
    depth = 0
    for j in range (i, len (text)):
        if text[j] == '{':
            depth += 1
        elif text[j] == '}':
            depth -= 1
            if depth == 0:
                return j
    return -1


def parse_members (body):
    members, i, pending_doc, stmt = [], 0, '', ''
    while i < len (body):
        if body.startswith ('/**', i):
            j = body.find ('*/', i + 3)
            pending_doc = body[i + 3:j]
            i = j + 2
            continue
        if body.startswith ('/*', i):
            i = body.find ('*/', i + 2) + 2
            continue
        if body.startswith ('//', i):
            j = body.find ('\n', i)
            i = len (body) if j < 0 else j
            continue
        c = body[i]
        if c == '{':
            j = find_matching (body, i)
            if '(' not in stmt:
                members.extend (parse_members (body[i + 1:j]))
            k = body.find (';', j)
            i = j + 1 if ('(' in stmt or k < 0) else k + 1
            stmt, pending_doc = '', ''
            continue
        if c == ';':
            decl = ' '.join (stmt.split ())
            stmt = ''
            if decl and '(' not in decl and not decl.startswith (('static', 'typedef', 'using', 'friend', 'enum', 'public', 'private', 'protected')):
                decl = re.sub (r'\[[^\]]*\]', '', decl)
                # Les virgules des modeles (GS::HashTable<A, B>) ne separent pas des noms.
                decl_sans_modeles = re.sub (r'<[^<>]*(?:<[^<>]*>[^<>]*)*>', lambda m: m.group (0).replace (',', ';'), decl)
                toks = [t for t in decl_sans_modeles.replace ('*', ' * ').replace ('&', ' ').split () if t not in ('const', 'volatile', 'mutable', 'struct', 'union', 'unsigned')]
                if len (toks) >= 2:
                    names = [n.strip () for n in ' '.join (toks).split (',')]
                    typ = ' '.join (toks[:-1]) if len (names) == 1 else ' '.join (names[0].split ()[:-1])
                    for n in names:
                        members.append ((typ.replace (';', ','), n.split ()[-1], brief_of (pending_doc)))
            pending_doc = ''
            i += 1
            continue
        stmt += c
        i += 1
    return members


structs = {}
for h in sorted (INC.glob ('APIdefs*.h')):
    t = h.read_text (encoding='utf-8', errors='replace')
    for m in re.finditer (r'\bstruct\s+(API_\w+)\s*(?::[^{]*)?\{', t):
        j = find_matching (t, m.end () - 1)
        structs.setdefault (m.group (1), parse_members (t[m.end ():j]))
ALLH = '\n'.join (h.read_text (encoding='utf-8', errors='replace') for h in INC.glob ('APIdefs*.h'))
memo = structs['API_ElementMemo']

src = {}
for f in sorted (list (SRC.glob ('*.cpp')) + list (SRC.glob ('*.hpp'))):
    t = f.read_text (encoding='utf-8', errors='replace')
    t = re.sub (r'/\*.*?\*/', ' ', t, flags=re.S)
    t = re.sub (r'//[^\n]*', ' ', t)
    t = re.sub (r'R"\((.*?)\)"', '""', t, flags=re.S)
    src[f.name] = t
ALL = '\n'.join (src.values ())

# Les noms qui designent un memo : variables declarees API_ElementMemo, et les noms usuels.
memo_vars = {'memo'}
for m in re.finditer (r'\bAPI_ElementMemo\s*(?:const\s*)?[&*]?\s*(\w+)\s*(?=[=;,)\[{(:])', ALL):
    memo_vars.add (m.group (1))
memo_vars -= {'const', 'return', 'operator'}
OWN = '(?:' + '|'.join (sorted (re.escape (v) for v in memo_vars)) + ')'


def usages (member):
    """(lu, ecrit, fichiers) pour un membre du memo."""
    acces = re.compile (r'\b' + OWN + r'\s*(?:\.|->)\s*' + re.escape (member) + r'\b')
    lu, ec, fichiers = False, False, set ()
    for nom, t in src.items ():
        for m in acces.finditer (t):
            lu = True
            fichiers.add (nom)
            apres = t[m.end ():m.end () + 200]
            avant = t[max (0, m.start () - 120):m.start ()]
            if re.match (r'\s*(?:\[[^\]\n]*\])?\s*(?:=(?!=)|\+=)', apres) \
               or re.search (r'\(\s*\*\s*$', avant) and re.match (r'\s*\)\s*\[[^\]\n]*\]\s*(?:\.\s*\w+\s*)*(?:\.\s*\w+\s*)?(?:\[[^\]\n]*\]\s*)?=(?!=)', apres) \
               or re.search (r'&\s*$', avant) or re.search (r'\.Get\s*\(\s*"[^"]*"\s*,\s*$', avant) \
               or re.search (r'BMhSetSize\w*\s*\(\s*\(?\s*\w*\s*\**\s*\)?\s*$', avant) or re.search (r'BMReallocHandle\s*\(\s*\(?\s*\w*\s*\**\s*\)?\s*$', avant):
                ec = True
    return lu, ec, sorted (fichiers)


SIMPLE = {'double', 'float', 'bool', 'char', 'short', 'int', 'Int32', 'UInt32', 'Int16', 'UInt16', 'Int8', 'UInt8', 'Int64', 'UInt64',
          'GSSize', 'API_Guid', 'API_AttributeIndex', 'GS::UniString', 'GSFlags', 'API_Coord', 'API_Coord3D', 'API_PolyArc', 'API_ElemType'}
ELEMENT_TYPES = {t for t, n, _ in parse_members (ALLH[ALLH.find ('union API_Element {') + len ('union API_Element {'):find_matching (ALLH, ALLH.find ('union API_Element {') + len ('union API_Element '))])}

rows = []
for ftyp, fname, fbrief in memo:
    if re.match (r'^(filler|reserved|dummy|unused)', fname, re.I):
        continue
    lu, ec, fichiers = usages (fname)
    m = re.search (r'(API_\w+)', ftyp)
    item = m.group (1) if m else None
    genre = 'tableau de sous-elements' if item in ELEMENT_TYPES else ('tableau de structures' if item in structs and item not in SIMPLE else 'donnee simple')
    rows.append ({'membre': fname, 'type': ftyp, 'genre': genre, 'lu': lu, 'ecrit': ec, 'fichiers': ' '.join (fichiers), 'description': fbrief, 'champs': ''})
    if genre == 'tableau de structures':
        champs = []
        for styp, sname, sbrief in structs.get (item, []):
            if re.match (r'^(filler|reserved|dummy|unused)', sname, re.I):
                continue
            # (*memo.gables)[i].a, memo.gables[0][i].a, ou une variable du type de l'element (const API_Gable& g ... g.a).
            vars_item = {fname}
            for mm in re.finditer (r'\b' + re.escape (item) + r'\s*(?:const\s*)?[&*]?\s*(?:const\s*)?(\w+)\s*(?=[=;,)\[{(:])', ALL):
                vars_item.add (mm.group (1))
            vi = '(?:' + '|'.join (sorted (re.escape (v) for v in vars_item)) + ')'
            pat = re.compile (r'(?:\b' + vi + r'\s*\)?\s*(?:\[[^\]\n]*\]\s*)*(?:\.|->)\s*' + re.escape (sname) + r'\b)')
            s_lu = s_ec = False
            for t in src.values ():
                for x in pat.finditer (t):
                    s_lu = True
                    apres = t[x.end ():x.end () + 80]
                    avant = t[max (0, x.start () - 120):x.start ()]
                    if re.match (r'\s*(?:\[[^\]\n]*\])?\s*(?:=(?!=)|\+=|-=)', apres) or re.search (r'\.Get\s*\(\s*"[^"]*"\s*,\s*\(?\s*\*?\s*$', avant) or re.search (r'&\s*\(?\s*\*?\s*$', avant):
                        s_ec = True
            champs.append (f"{sname}:{'L' if s_lu else '-'}{'E' if s_ec else '-'}")
            rows.append ({'membre': f'{fname}[].{sname}', 'type': styp, 'genre': 'champ d un element du tableau', 'lu': s_lu, 'ecrit': s_ec, 'fichiers': '', 'description': sbrief, 'champs': ''})
        rows[-1 - len (champs)]['champs'] = ' '.join (champs)

masques = []
for m in re.finditer (r'#define\s+(APIMemoMask_\w+)', ALLH):
    nom = m.group (1)
    masques.append ({'masque': nom, 'utilise': re.search (r'\b' + nom + r'\b', ALL) is not None})

with open (OUT / 'couverture_memo.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter (f, fieldnames=['membre', 'type', 'genre', 'lu', 'ecrit', 'fichiers', 'description', 'champs'], delimiter=';')
    w.writeheader ()
    for r in rows:
        w.writerow (dict (r, lu='oui' if r['lu'] else 'non', ecrit='oui' if r['ecrit'] else 'non'))
(OUT / 'couverture_memo.json').write_text (json.dumps ({'membres': rows, 'masques': masques}, ensure_ascii=False, indent=1), encoding='utf-8')

hauts = [r for r in rows if r['genre'] != 'champ d un element du tableau']
print (f'{len (hauts)} membres du memo ; lus {sum (r["lu"] for r in hauts)} ; ecrits {sum (r["ecrit"] for r in hauts)}')
for r in hauts:
    print (f"{r['membre']:32s} {r['genre']:26s} {'LU' if r['lu'] else '--'} {'ECRIT' if r['ecrit'] else '-----'}  {r['champs'][:150]}")
print ('masques non utilises : ' + ', '.join (x['masque'] for x in masques if not x['utilise']))
