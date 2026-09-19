"""Genereaza paper_full_copy-paste.tex din paper_full.tex: scoate blocul de
comentariu din cap si comentariile noastre in romana, pastreaza comentariile
proprii ale template-ului ACL.

Siguranta: la final compara liniile NON-comentariu ale celor doua fisiere. Daca
difera cu un singur caracter, pica. Deci nu se poate pierde continut, oricat de
aproximativa ar fi detectia de limba.
"""
import re, sys

SRC, DST = sys.argv[1], sys.argv[2]
lines = open(SRC).read().split('\n')

# --- 1. taie tot inaintea lui \begin{filecontents*} ---
start = next(i for i, l in enumerate(lines) if l.startswith('\\begin{filecontents*}'))
body = lines[start:]

# Cuvinte care apar in comentariile noastre si in niciunul al template-ului.
# "Anthology" NU e in lista: apare si in comentariul template-ului.
RO = re.compile(
    r'\b(pentru|care|acum|scos|scoase|sunt|este|nu|si|de|din|cele|fisier\w*|'
    r'lucrari\w*|template-ului|abaterea|abaterile|comentariu|comentariile|'
    r'intrari\w*|intrarea|randeaza|randa|pagina|pagini|continut\w*|'
    r'formatting|verificat\w*|masurat|adaugat\w*|mutat|reparat\w*|'
    r'coordonatorul\w*|autor\w* nu|gol|regula|corectii|corectia|'
    r'sectiunea|sectiunile|captionul|tabel\w*|figur\w*|'
    r'fractiile|dedicau|relaxate|incapa|coloan\w*|spatiu|intregi|doar|'
    r'aceeasi|urmatoarele|lasate|asamblarea|repus|apendice\w*|blocul)\b',
    re.IGNORECASE)

def is_ours(run):
    """run = lista de linii de comentariu consecutive."""
    text = ' '.join(l.lstrip('% ').strip() for l in run)
    if not text.strip('- ='):          # separatoare pure % ----- : le judecam cu vecinii
        return None
    return bool(RO.search(text))

# --- 2. parcurge in runde de comentarii consecutive ---
out, i = [], 0
while i < len(body):
    if body[i].lstrip().startswith('%'):
        j = i
        while j < len(body) and body[j].lstrip().startswith('%'):
            j += 1
        run = body[i:j]
        verdict = is_ours(run)
        if verdict is None:            # numai separatoare, fara text
            verdict = False
        if not verdict:
            out.extend(run)
        i = j
    else:
        out.append(body[i])
        i += 1

# --- 3. normalizeaza liniile goale lasate in urma ---
text = '\n'.join(out)
text = re.sub(r'\n{4,}', '\n\n\n', text)
text = text.lstrip('\n')
open(DST, 'w').write(text)

# --- 4. PLASA DE SIGURANTA: continutul non-comentariu trebuie identic ---
def code_only(path):
    """Linii de cod, fara comentarii si fara linii goale. Liniile goale se
    compara separat: scoaterea comentariilor schimba inevitabil cite sunt,
    iar LaTeX are nevoie doar sa RAMINA cel putin una intre paragrafe."""
    return [l for l in open(path).read().split('\n')
            if l.strip() and not l.lstrip().startswith('%')]

a, b = code_only(SRC), code_only(DST)
if a != b:
    import difflib
    print('EROARE: continutul difera. Primele diferente:')
    for d in list(difflib.unified_diff(a, b, 'paper_full', 'copy-paste', lineterm=''))[:30]:
        print(' ', d)
    sys.exit(1)

print(f'ok. {len(lines)} -> {len(text.split(chr(10)))} linii, '
      f'{len(a)} linii de cod identice.')
