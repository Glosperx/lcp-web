import sys, re
# usage: q.py file.txt "quote" ...  -> prints PDF page where the whitespace-normalised quote occurs
path = sys.argv[1]
pages = open(path, encoding='utf-8', errors='replace').read().split('\f')
def norm(s):
    s = s.replace('­', '')
    s = re.sub(r'-\s*\n\s*', '', s)  # join hyphenated line breaks
    return re.sub(r'\s+', ' ', s).strip().lower()
np_ = [norm(p) for p in pages]
for q in sys.argv[2:]:
    nq = norm(q)
    hits = [i + 1 for i, p in enumerate(np_) if nq in p]
    if not hits:  # try across page boundary / without hyphen join
        nq2 = re.sub(r'\s+', ' ', q).strip().lower()
        hits = [i + 1 for i, p in enumerate(pages) if nq2 in re.sub(r'\s+', ' ', p).lower()]
    print(('OK  p' + ','.join(map(str, hits))) if hits else 'MISSING', '|', q[:90])
