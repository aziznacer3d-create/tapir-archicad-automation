"""Couverture par champ des ATTRIBUTS : chaque champ des structures d'attributs du DevKit est-il lu / ecrit par Tapir ?

Meme methode que couverture_champs.py (elements), sur l'union API_Attribute et sur les donnees
complementaires API_AttributeDefExt (lignes d'un type de ligne, couches d'un composite, stylos d'une
table de stylos...).

Usage : python -I couverture_attributs.py <dossier Inc du DevKit> <dossier Sources de Tapir> <dossier de sortie>
Detection par le texte (approximative) :
- lu    : le champ est atteint par  .<membre>.<champ>  (ex. attrib.layer.lockStatus), par une variable
          du type de la structure, ou le champ parent entier est lu ;
- ecrit : affectation  ... .<champ> = ...
"""
import collections
import csv
import json
import pathlib
import re
import sys

INC = pathlib.Path (sys.argv[1])
SRC = pathlib.Path (sys.argv[2])
OUT = pathlib.Path (sys.argv[3])
OUT.mkdir (parents=True, exist_ok=True)


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
            if '(' not in stmt:
                members.extend (parse_members (body[i + 1:j]))
            k = body.find (';', j)
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
                arr = re.search (r'\[([^\]]*)\]', decl)
                decl = re.sub (r'\[[^\]]*\]', '', decl).replace ('*', ' * ').replace ('&', ' ')
                toks = [t for t in decl.split () if t not in ('const', 'volatile', 'mutable', 'struct', 'union', 'unsigned')]
                if len (toks) >= 2:
                    names = [n.strip () for n in ' '.join (toks).split (',')]
                    typ = ' '.join (toks[:-1]) if len (names) == 1 else ' '.join (names[0].split ()[:-1])
                    if arr:
                        typ += f'[{arr.group (1)}]'
                    for n in names:
                        members.append ((typ, n.split ()[-1], brief_of (pending_doc)))
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

at = (INC / 'APIdefs_Attributes.h').read_text (encoding='utf-8', errors='replace')
u = at.find ('union API_Attribute {')
attributs = [(t, n) for t, n, _ in parse_members (at[u + len ('union API_Attribute {'):find_matching (at, u + len ('union API_Attribute '))]) if n != 'header']

SKIP = re.compile (r'^(filler|reserved|head$|header$|dummy|unused)', re.I)
SKIP_BRIEF = re.compile (r'\b(unused|reserved|filler|obsolete|deprecated|do not use|internal use)\b', re.I)

src = {}
for f in sorted (list (SRC.glob ('*.cpp')) + list (SRC.glob ('*.hpp'))):
    t = f.read_text (encoding='utf-8', errors='replace')
    t = re.sub (r'/\*.*?\*/', ' ', t, flags=re.S)
    t = re.sub (r'//[^\n]*', ' ', t)
    t = re.sub (r'R"\((.*?)\)"', '""', t, flags=re.S)
    src[f.name] = t
ALL = '\n'.join (src.values ())


def vars_of (typ):
    names = set ()
    for m in re.finditer (r'\b' + re.escape (typ) + r'\s*(?:const\s*)?[&*]?\s*(?:const\s*)?(\w+)\s*(?=[=;,)\[{(:])', ALL):
        if m.group (1) not in ('const', 'operator', 'return'):
            names.add (m.group (1))
    # for (const API_X& x : ...) et auto& x = ... ne sont pas tous vus : approximatif.
    return names


SIMPLE = {'double', 'float', 'bool', 'char', 'short', 'int', 'Int32', 'UInt32', 'Int16', 'UInt16', 'Int8', 'UInt8', 'Int64', 'UInt64',
          'GSSize', 'GS::Int32', 'API_Guid', 'API_AttributeIndex', 'API_AttributeIndexType', 'GS::UniString', 'GSFlags', 'short int'}

CHAIN = re.compile (r'\b[A-Za-z_]\w*(?:\s*(?:\[[^\]\n]*\])?\s*(?:\.|->)\s*[A-Za-z_]\w*)+')
ASSIGN = re.compile (r'(?:\s*\[[^\]\n]*\])*\s*(?:=(?!=)|\+=|-=|\|=|&=)')
pair_read, pair_write, pair_tail = set (), set (), set ()
trip_read, trip_write = set (), set ()
# Ecritures sans « = » : lecture du JSON directement dans le champ (data.Get ("thickness", comp.fillThick)),
# ou champ passe par adresse a une fonction qui le remplit (&attr.zoneCat.rgb).
GET_INTO = re.compile (r'\.Get\s*\(\s*"[^"]*"\s*,\s*$')
ADDRESS = re.compile (r'&\s*$')
for m in CHAIN.finditer (ALL):
    ids = [x for x in re.split (r'\s*(?:\[[^\]\n]*\])?\s*(?:\.|->)\s*', m.group (0)) if x]
    if len (ids) < 2:
        continue
    avant = ALL[max (0, m.start () - 120):m.start ()]
    assigned = ASSIGN.match (ALL, m.end ()) is not None or GET_INTO.search (avant) is not None or ADDRESS.search (avant) is not None
    for p in range (len (ids) - 1):
        pair_read.add ((ids[p], ids[p + 1]))
        if p + 2 < len (ids):
            trip_read.add ((ids[p], ids[p + 1], ids[p + 2]))
    pair_tail.add ((ids[-2], ids[-1]))
    if assigned:
        pair_write.add ((ids[-2], ids[-1]))
        if len (ids) >= 3:
            trip_write.add ((ids[-3], ids[-2], ids[-1]))

var_cache = {}


def owners_of (member, typ):
    if typ not in var_cache:
        var_cache[typ] = vars_of (typ)
    return {member} | var_cache[typ]


def champs_de (owner_names, struct_name, prefix, groupe, structure, rows, profondeur=0):
    """Ajoute les champs de struct_name atteints par les noms owner_names (sous-structures depliees une fois)."""
    for ftyp, fname, fbrief in structs.get (struct_name, []):
        if SKIP.match (fname) or SKIP_BRIEF.search (fbrief):
            continue
        base = re.sub (r'\[.*\]', '', ftyp).replace ('*', '').strip ()
        sub = structs.get (base)
        if sub and base not in SIMPLE and '*' not in ftyp and len (sub) <= 40 and profondeur == 0:
            own_sub = owners_of (fname, base)
            for styp, sname, sbrief in sub:
                if SKIP.match (sname) or SKIP_BRIEF.search (sbrief):
                    continue
                lu = any ((o, fname, sname) in trip_read for o in owner_names) or any ((o, fname) in pair_tail for o in owner_names) \
                    or any ((o, sname) in pair_read for o in var_cache.get (base, set ()))
                ec = any ((o, fname, sname) in trip_write for o in owner_names) or any ((o, fname) in pair_write for o in owner_names)
                rows.append ({'groupe': groupe, 'struct': structure, 'champ': f'{prefix}{fname}.{sname}', 'type': styp, 'lu': lu, 'ecrit': ec,
                              'description': (fbrief + ' > ' + sbrief).strip (' >')})
        else:
            lu = any ((o, fname) in pair_read for o in owner_names)
            ec = any ((o, fname) in pair_write for o in owner_names)
            rows.append ({'groupe': groupe, 'struct': structure, 'champ': f'{prefix}{fname}', 'type': ftyp, 'lu': lu, 'ecrit': ec, 'description': fbrief})


rows = []
# 1. Les structures de l'union API_Attribute (attrib.layer.xxx, ou une variable API_LayerType).
for atyp, amember in attributs:
    champs_de (owners_of (amember, atyp), atyp, '', amember, atyp, rows)

# 2. Les donnees complementaires (API_AttributeDefExt) : le membre lui-meme, puis les champs de ses elements.
defs_vars = owners_of ('defs', 'API_AttributeDefExt') | owners_of ('defs', 'API_AttributeDef')
ext = structs.get ('API_AttributeDefExt', [])
for ftyp, fname, fbrief in ext:
    if SKIP.match (fname):
        continue
    lu = any ((o, fname) in pair_read for o in defs_vars) or re.search (r'\b' + fname + r'\b', ALL) is not None
    ec = any ((o, fname) in pair_write for o in defs_vars)
    rows.append ({'groupe': 'donnees:' + fname, 'struct': 'API_AttributeDefExt', 'champ': fname, 'type': ftyp, 'lu': lu, 'ecrit': ec, 'description': fbrief})
    m = re.search (r'(API_\w+)', ftyp)
    item = m.group (1) if m else None
    if item and item in structs and item != 'API_AttributeIndex':
        # Les elements d'un tableau : (*defs.cwall_compItems)[i].fillPen, ou une variable du type de l'element.
        owners = owners_of (fname, item)
        for line in ALL.split ('\n'):
            if fname in line:
                for mm in re.finditer (r'\]\s*\)?\s*(?:\.|->)\s*(\w+)', line):
                    pair_read.add ((fname, mm.group (1)))
                    if ASSIGN.match (line, mm.end ()):
                        pair_write.add ((fname, mm.group (1)))
        champs_de (owners, item, fname + '[].', 'donnees:' + fname, item, rows)

with open (OUT / 'couverture_attributs.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter (f, fieldnames=['groupe', 'struct', 'champ', 'type', 'lu', 'ecrit', 'description'], delimiter=';')
    w.writeheader ()
    for r in rows:
        w.writerow (dict (r, lu='oui' if r['lu'] else 'non', ecrit='oui' if r['ecrit'] else 'non'))

par = collections.OrderedDict ()
for r in rows:
    par.setdefault (r['groupe'], []).append (r)
resume = []
for g, rs in par.items ():
    resume.append ({'groupe': g, 'struct': rs[0]['struct'], 'champs': len (rs), 'lus': sum (r['lu'] for r in rs), 'ecrits': sum (r['ecrit'] for r in rs),
                    'absents': [r['champ'] for r in rs if not r['lu']],
                    'lecture_seule': [r['champ'] for r in rs if r['lu'] and not r['ecrit']]})
(OUT / 'couverture_attributs.json').write_text (json.dumps ({'resume': resume, 'champs': rows}, ensure_ascii=False, indent=1), encoding='utf-8')

print (f'{len (par)} groupes, {len (rows)} champs ; lus {sum (r["lu"] for r in rows)} ; ecrits {sum (r["ecrit"] for r in rows)}')
for s in resume:
    print (f"{s['groupe']:34s} {s['struct']:28s} {s['champs']:4d} champs  lus {s['lus']:4d}  ecrits {s['ecrits']:4d}")
