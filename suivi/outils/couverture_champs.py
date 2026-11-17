"""Couverture par champ : chaque champ des structures d'elements du DevKit 29 est-il lu / ecrit par Tapir ?

Usage : python -I couverture_champs.py <dossier Sources de Tapir> <dossier de sortie>
Detection par le texte (approximative) :
- lu    : le champ est atteint par  .<membre>.<champ>  (ex. element.wall.thickness), par une variable
          du type de la structure (const API_WallType& wall ... wall.thickness), ou le champ parent
          entier est lu (element.wall.begC passe a une fonction).
- ecrit : affectation  ... .<champ> = ...  ou  ACAPI_ELEMENT_MASK_SET (mask, API_WallType, <champ>).
"""
import collections
import csv
import json
import pathlib
import re
import sys
import time
T0 = time.time ()
def etape (n): print (f'[{time.time () - T0:6.1f} s] {n}', file=sys.stderr, flush=True)

# Le dossier Inc du DevKit : 3e argument, sinon celui de l'ordinateur d'origine.
INC = pathlib.Path (sys.argv[3]) if len (sys.argv) > 3 else pathlib.Path (r'C:\Program Files\GRAPHISOFT\API Development Kit 29.3100\Support\Inc')
SRC = pathlib.Path (sys.argv[1])
OUT = pathlib.Path (sys.argv[2])
OUT.mkdir (parents=True, exist_ok=True)

DOC = re.compile (r'/\*\*(.*?)\*/', re.S)


def brief_of (doc):
    m = re.search (r'@brief\s+(.*?)(?:\n\s*\*\s*@|\Z)', doc, re.S)
    if not m:
        return ''
    return re.sub (r'\s*\n\s*\*\s*', ' ', m.group (1)).strip ()


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
    """(type, nom, brief) des membres d'un corps de struct ; les unions anonymes sont aplaties."""
    members = []
    i = 0
    pending_doc = ''
    stmt = ''
    while i < len (body):
        if body.startswith ('/**', i):
            j = body.find ('*/', i + 3)
            if j < 0:
                break
            pending_doc = body[i + 3:j]
            i = j + 2
            continue
        if body.startswith ('/*', i):
            j = body.find ('*/', i + 2)
            if j < 0:
                break
            i = j + 2
            continue
        if body.startswith ('//', i):
            j = body.find ('\n', i)
            i = len (body) if j < 0 else j
            continue
        c = body[i]
        if c == '{':
            j = find_matching (body, i)
            if j < 0:
                break
            # Corps de methode (constructeur, operateur...) : pas de membres. Union/struct anonyme : aplatie.
            if '(' not in stmt:
                members.extend (parse_members (body[i + 1:j]))
            k = body.find (';', j)
            nxt = body.find ('\n', j)
            # Une methode se termine par } sans ; : on reprend juste apres l'accolade.
            if '(' in stmt or k < 0:
                i = j + 1
            else:
                i = k + 1
            stmt = ''
            pending_doc = ''
            continue
        if c == ';':
            decl = ' '.join (stmt.split ())
            stmt = ''
            if decl and '(' not in decl and not decl.startswith (('static', 'typedef', 'using', 'friend', 'enum', 'public', 'private', 'protected')):
                decl = re.sub (r'\[[^\]]*\]', '', decl).replace ('*', ' * ').replace ('&', ' ')
                toks = [t for t in decl.split () if t not in ('const', 'volatile', 'mutable', 'struct', 'union', 'unsigned')]
                if len (toks) >= 2:
                    names = [n.strip () for n in ' '.join (toks).split (',')]
                    typ = ' '.join (toks[:-1]) if len (names) == 1 else ' '.join (names[0].split ()[:-1])
                    for n in names:
                        nm = n.split ()[-1]
                        members.append ((typ, nm, brief_of (pending_doc)))
            pending_doc = ''
            i += 1
            continue
        if c == ':' and body.startswith (('public:', 'private:', 'protected:'), max (0, i - 9)):
            stmt = ''
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
    for m in re.finditer (r'typedef\s+struct\s*\w*\s*\{', t):
        j = find_matching (t, m.end () - 1)
        nm = re.match (r'\s*(API_\w+)\s*;', t[j + 1:j + 120])
        if nm:
            structs.setdefault (nm.group (1), parse_members (t[m.end ():j]))

etape ('structures lues')
el = (INC / 'APIdefs_Elements.h').read_text (encoding='utf-8', errors='replace')
u = el.find ('union API_Element {')
elements = [(t, n) for t, n, _ in parse_members (el[u + len ('union API_Element {'):find_matching (el, u + len ('union API_Element '))]) if n != 'header']

SKIP = re.compile (r'^(filler|reserved|head$|header$|dummy|unused)', re.I)
SKIP_BRIEF = re.compile (r'\b(unused|reserved|filler|obsolete|deprecated|do not use|internal use)\b', re.I)

etape ('union lue')
src = {}
for f in sorted (list (SRC.glob ('*.cpp')) + list (SRC.glob ('*.hpp'))):
    t = f.read_text (encoding='utf-8', errors='replace')
    t = re.sub (r'/\*.*?\*/', ' ', t, flags=re.S)
    t = re.sub (r'//[^\n]*', ' ', t)
    t = re.sub (r'R"\((.*?)\)"', '""', t, flags=re.S)  # schemas JSON
    src[f.name] = t
ALL = '\n'.join (src.values ())


def vars_of (typ):
    """Noms de variables / parametres declares avec ce type dans les sources."""
    names = set ()
    for m in re.finditer (r'\b' + re.escape (typ) + r'\s*(?:const\s*)?[&*]?\s*(?:const\s*)?(\w+)\s*(?=[=;,)\[{(])', ALL):
        if m.group (1) not in ('const', 'operator', 'return'):
            names.add (m.group (1))
    return names


SIMPLE = {'double', 'float', 'bool', 'char', 'short', 'int', 'Int32', 'UInt32', 'Int16', 'UInt16', 'Int8', 'UInt8', 'Int64', 'UInt64',
          'GSSize', 'GS::Int32', 'API_Guid', 'API_AttributeIndex', 'API_AttributeIndexType', 'GS::UniString', 'GSFlags', 'short int'}

etape ('sources lues')
# --- Index des acces du code, construit en une seule lecture -------------------------------------
# Chaines d'acces  a.b.c  (ou a->b) ; pour chaque paire (A, B) et triplet (A, B, C) consecutifs :
#   lu      : la paire / le triplet apparait ;
#   ecrit   : la chaine se termine sur cette paire / ce triplet et est suivie d'une affectation ;
#   bout    : la chaine se termine sur cette paire (le champ est utilise en entier, pas un sous-champ).
CHAIN = re.compile (r'\b[A-Za-z_]\w*(?:\s*(?:\.|->)\s*[A-Za-z_]\w*)+')
ASSIGN = re.compile (r'(?:\s*\[[^\]\n]*\])*\s*(?:=(?!=)|\+=|-=|\|=|&=)')
pair_read, pair_write, pair_tail = set (), set (), set ()
trip_read, trip_write = set (), set ()
for m in CHAIN.finditer (ALL):
    ids = [x for x in re.split (r'\s*(?:\.|->)\s*', m.group (0)) if x != 'u']  # union nommee u (roof.u.planeRoof) : transparente
    if len (ids) < 2:
        continue
    assigned = ASSIGN.match (ALL, m.end ()) is not None
    for p in range (len (ids) - 1):
        pair_read.add ((ids[p], ids[p + 1]))
        if p + 2 < len (ids):
            trip_read.add ((ids[p], ids[p + 1], ids[p + 2]))
    pair_tail.add ((ids[-2], ids[-1]))
    if assigned:
        pair_write.add ((ids[-2], ids[-1]))
        if len (ids) >= 3:
            trip_write.add ((ids[-3], ids[-2], ids[-1]))
masks = set ()
for m in re.finditer (r'ACAPI_ELEMENT_MASK_SET\s*\(\s*\w+\s*,\s*(\w+)\s*,\s*([\w\s.\[\]]+?)\s*\)', ALL):
    masks.add ((m.group (1), re.sub (r'^u\.', '', re.sub (r'\s+', '', m.group (2)))))

etape ('index construit')
var_cache = {}


def owners_of (member, typ):
    """Noms qui designent une structure de ce type : le membre de l'union (element.wall) et les variables du type."""
    if typ not in var_cache:
        var_cache[typ] = vars_of (typ)
    return {member} | var_cache[typ]


ALLH = '\n'.join (p.read_text (encoding='utf-8', errors='replace') for p in INC.glob ('APIdefs*.h'))

rows = []
for etyp, emember in elements:
    fields = structs.get (etyp)
    alias = None
    if not fields:
        # Types alias : typedef API_WindowType API_DoorType ; la porte a les champs de la fenetre.
        m = (re.search (r'typedef\s+(\w+)\s+' + re.escape (etyp) + r'\s*;', ALLH) or
             re.search (r'using\s+' + re.escape (etyp) + r'\s*=\s*(\w+)\s*;', ALLH))
        alias = m.group (1) if m else None
        fields = structs.get (alias) if alias else None
    if not fields:
        continue
    own = owners_of (emember, etyp) | (owners_of (emember, alias) if alias else set ())
    if alias:
        # Le code passe souvent par le membre de base de l'union (une lampe par element.object).
        for btyp, bname in elements:
            if btyp == alias:
                own |= owners_of (bname, btyp)
    for ftyp, fname, fbrief in fields:
        if SKIP.match (fname) or SKIP_BRIEF.search (fbrief):
            continue
        whole_read = any ((o, fname) in pair_read for o in own)
        whole_tail = any ((o, fname) in pair_tail for o in own)
        whole_write = any ((o, fname) in pair_write for o in own) or (etyp, fname) in masks
        sub = structs.get (ftyp.replace ('*', '').strip ())
        if sub and ftyp not in SIMPLE and '*' not in ftyp and len (sub) <= 40:
            subtype_vars = owners_of (fname, ftyp.strip ()) if len (sub) <= 40 else {fname}
            for styp, sname, sbrief in sub:
                if SKIP.match (sname) or SKIP_BRIEF.search (sbrief):
                    continue
                exp_read = any ((o, fname, sname) in trip_read for o in own)
                exp_write = any ((o, fname, sname) in trip_write for o in own) or (etyp, f'{fname}.{sname}') in masks
                rows.append ({'element': emember, 'struct': etyp, 'champ': f'{fname}.{sname}', 'type': styp,
                              # Le champ parent utilise en entier (passe a une fonction, copie) compte pour ses sous-champs.
                              'lu': exp_read or whole_tail,
                              'ecrit': exp_write or (etyp, fname) in masks or any ((o, fname) in pair_write for o in own),
                              'description': (fbrief + ' > ' + sbrief).strip (' >')})
        else:
            rows.append ({'element': emember, 'struct': etyp, 'champ': fname, 'type': ftyp, 'lu': whole_read, 'ecrit': whole_write, 'description': fbrief})

etape ('champs classes')
with open (OUT / 'couverture_champs.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter (f, fieldnames=['element', 'struct', 'champ', 'type', 'lu', 'ecrit', 'description'], delimiter=';')
    w.writeheader ()
    for r in rows:
        w.writerow (dict (r, lu='oui' if r['lu'] else 'non', ecrit='oui' if r['ecrit'] else 'non'))

par = collections.OrderedDict ()
for r in rows:
    par.setdefault (r['element'], []).append (r)
resume = []
for e, rs in par.items ():
    n = len (rs)
    lu = sum (r['lu'] for r in rs)
    ec = sum (r['ecrit'] for r in rs)
    resume.append ({'element': e, 'struct': rs[0]['struct'], 'champs': n, 'lus': lu, 'ecrits': ec,
                    'absents': [r['champ'] for r in rs if not r['lu']],
                    'lecture_seule': [r['champ'] for r in rs if r['lu'] and not r['ecrit']]})
(OUT / 'couverture_champs.json').write_text (json.dumps ({'resume': resume, 'champs': rows}, ensure_ascii=False, indent=1), encoding='utf-8')

tot = len (rows)
print (f'{len (par)} types d elements, {tot} champs ; lus {sum (r["lu"] for r in rows)} ; ecrits {sum (r["ecrit"] for r in rows)}')
for s in sorted (resume, key=lambda s: -s['champs']):
    print (f"{s['element']:24s} {s['champs']:4d} champs  lus {100 * s['lus'] // max (1, s['champs']):3d} %  ecrits {100 * s['ecrits'] // max (1, s['champs']):3d} %  absents {len (s['absents']):3d}")




