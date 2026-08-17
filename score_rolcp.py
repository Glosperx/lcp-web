"""Scoreaza submission.csv pe etichetele RoLCP publicate in RALS.

RULAT PE 30 IULIE 2026. Rezultat, join 1587/1587 pe cheie completa:
    r        = 0.7770   CI 95% [0.7568, 0.7958]
    R^2      = 0.6028
    compozit = 68.99    (raportat pe leaderboard: 69.74, diferenta 0.75)
    gold: medie 0.2701, std 0.1674
RALS raporteaza pe acelasi set r = 0.71 +/- 0.05, Ridge supervizat, 10-fold CV.
Deci sistemul nostru, fara nicio eticheta de antrenare romaneasca, il depaseste.

CIFRELE NU SUNT IN PAPER. Vezi blocul de TODO din
Paper/Articol_Complexity/paper_full.tex, punctul 2: de decis cu Sergiu daca se
raporteaza, pentru ca intra in tensiune cu revendicarea "fara etichete cap la cap".

CUM SE OBTIN DATELE:
    curl -sL -o data.zip https://github.com/senisioi/RALS/raw/main/data.zip
    unzip -P ralsresources data.zip        # parola e publicata in README-ul lor
    # apoi pune calea catre data/RoLCP.csv in RALS de mai jos

Afiseaza NUMAI agregate. Etichetele individuale nu se tiparesc niciodata:
data.zip e protejat cu parola tocmai ca sa nu ajunga per-item intr-un context de
LLM, si regula asta se respecta si aici.

Validarea alinierii: daca compozitul iese ~69.74, joinul e corect. Daca nu,
cifrele nu se raporteaza.
"""
import csv, math, sys, statistics as st
from collections import defaultdict
import os

REPO = os.path.dirname(os.path.abspath(__file__))
RALS = os.environ.get('ROLCP_CSV', os.path.join(REPO, 'data', 'RoLCP.csv'))

def norm(s):
    return (s or '').strip()

# --- predictiile noastre ---
pred = {}
for r in csv.DictReader(open(f'{REPO}/submission.csv')):
    pred[int(r['datapointID'])] = float(r['answer'])

# --- setul de test, ca sa avem cheile ---
test = {}
for r in csv.DictReader(open(f'{REPO}/data/test_set.csv')):
    test[int(r['datapointID'])] = (norm(r['text_name']), norm(r['token']), norm(r['text']))
print(f'submission: {len(pred)} rinduri   test_set: {len(test)} rinduri')

# --- gold RoLCP, indexat pe mai multe chei, cu fallback ---
by_full, by_pair = {}, defaultdict(list)
n_gold = 0
for r in csv.DictReader(open(RALS)):
    c = norm(r.get('complexity'))
    if not c:
        continue
    try:
        v = float(c)
    except ValueError:
        continue
    n_gold += 1
    tn, tok, txt = norm(r.get('text_name')), norm(r.get('token')), norm(r.get('text'))
    by_full[(tn, tok, txt)] = v
    by_pair[(tn, tok)].append(v)
print(f'RoLCP: {n_gold} rinduri cu eticheta')

# --- join: mai intai pe (text_name, token, text), apoi pe (text_name, token) unic ---
xs, ys, how = [], [], defaultdict(int)
for dpid, (tn, tok, txt) in test.items():
    if dpid not in pred:
        how['fara predictie'] += 1; continue
    v = by_full.get((tn, tok, txt))
    if v is not None:
        how['cheie completa'] += 1
    else:
        cand = by_pair.get((tn, tok), [])
        if len(cand) == 1:
            v = cand[0]; how['pereche unica'] += 1
        elif len(cand) > 1:
            v = st.mean(cand); how['pereche ambigua (media)'] += 1
        else:
            how['NEGASIT'] += 1; continue
    xs.append(pred[dpid]); ys.append(v)

print('potriviri:', dict(how))
n = len(xs)
if n < 100:
    sys.exit(f'\nOPRIT: doar {n} potriviri, joinul nu e de incredere.')

# --- statistici ---
mx, my = st.mean(xs), st.mean(ys)
sx, sy = st.pstdev(xs), st.pstdev(ys)
cov = sum((a-mx)*(b-my) for a, b in zip(xs, ys)) / n
r = cov / (sx*sy)
sse = sum((b-a)**2 for a, b in zip(xs, ys))
sst = sum((b-my)**2 for b in ys)
r2 = 1 - sse/sst
comp = 50*(abs(r) + max(0.0, r2))

print(f'\n=== n = {n} ===')
print(f'predictii  medie={mx:.4f}  std={sx:.4f}  min={min(xs):.4f}  max={max(xs):.4f}')
print(f'gold       medie={my:.4f}  std={sy:.4f}  min={min(ys):.4f}  max={max(ys):.4f}')
print(f'\nPearson r = {r:.4f}')
print(f'R^2       = {r2:.4f}')
print(f'compozit 50(|r| + max(0,R^2)) = {comp:.2f}      [raportat: 69.74]')

# --- cit ar da o recalibrare la distributia reala, fara sa schimbe r ---
z = [(a-mx)/sx for a in xs]
best = [my + sy*t for t in z]
sse2 = sum((b-a)**2 for a, b in zip(best, ys))
r2b = 1 - sse2/sst
print(f'\nCu media si std reale ale gold-ului in loc de mu=0.27, sigma=0.125:')
print(f'  R^2 = {r2b:.4f}   compozit = {50*(abs(r)+max(0.0,r2b)):.2f}   (r neschimbat)')
