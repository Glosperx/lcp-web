"""Setul de predictii al semnalului A ca MEDIE a celor patru encodere, in interiorul limbii.

De ce mediere si nu selectie. `fuse_ab.py --a-set` alege UN set per limba, leave-one-language-out, si
asta s-a rulat: da 0.6599, adica sub sistem. Motivul se vede in raport: latimea criteriului peste cei
36 de candidati e 0.0077, de zece ori mai mica decat latimea curbei lui w, deci argmaxul e in mare
parte zgomot. Consecinta concreta e ca pe sinhaleza, unde LaBSE da 0.3613 si e clar cel mai bun,
selectia a ales e5, care da 0.2090.

Cand criteriul e prea plat ca sa aleaga, medierea e raspunsul: nu cere ca ordinea candidatilor sa fie
estimabila, cere doar ca ei sa fie decorelati, si sunt (corelatii 0.847 pana la 0.884).

Ce face: pentru fiecare split, limba si coloana (`p_en`, `p_multi`), standardizeaza coloana FIECARUI
encoder in interiorul limbii, apoi mediaza cele patru. Standardizarea foloseste numai predictii, deci
nicio eticheta nu intra, si e acelasi `zscore` pe care `fuse_ab` il aplica oricum mai jos.

Scrie un CSV cu exact aceleasi coloane ca brațele individuale, deci `fuse_ab.py --a-set` il primeste
ca pe orice alt set, fara nicio linie de cod noua acolo.

`--encodere` alege submultimea mediata si `--dest` unde se scrie, fiindca M3, leave-one-encoder-out,
cere patru medii de cate trei. Fara argumente e media celor patru si calea de pana acum, deci
`e1_frozen_preds_encmean_lemma_fert_inloc.csv` iese bit cu bit la fel. **O submultime aleasa pe scor
ar fi acordare pe test**; M3 nu alege nimic, le ruleaza pe toate patru si le raporteaza pe toate.

`--cai NUME=CALE ...` mediaza fisiere date explicit, in loc de cele patru encodere canonice. E nevoie
fiindca membrii pot diferi acum si prin configuratia de EXTRACTIE sau prin sursa de frecventa, nu
doar prin encoder, iar `SUFFIXES` e o harta fixa de patru nume. Media insasi e neschimbata: aceeasi
standardizare in interiorul limbii, aceeasi pondere egala, niciun parametru liber.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python make_enc_mean.py
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python make_enc_mean.py \
      --encodere xlmr labse e5 --dest output/e1_frozen_preds_encmean_fara-large_lemma_fert_inloc.csv
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python make_enc_mean.py \
      --cai xlmr=output/A.csv labse=output/B.csv e5=output/C.csv --dest output/D.csv
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
SUFFIXES = {"xlmr": "", "xlmr-large": "_xlmr-large", "labse": "_labse", "e5": "_e5"}
COLS = ["p_en", "p_multi", "p_multi_testmu"]
DEST = os.path.join(OUT, "e1_frozen_preds_encmean_lemma_fert_inloc.csv")
KEY = ["split", "lang", "idx"]


def zscore(v):
    """Acelasi contract ca `fuse_ab.zscore`: NaN devine 0, adica media."""
    v = np.asarray(v, float)
    m = np.isfinite(v)
    if m.sum() < 2 or np.std(v[m]) == 0:
        return np.zeros(len(v))
    z = np.zeros(len(v))
    z[m] = (v[m] - v[m].mean()) / v[m].std()
    return z


def main(argv=None):
    ap = argparse.ArgumentParser(description="Media predictiilor unei submultimi de encodere.")
    ap.add_argument("--encodere", nargs="+", choices=list(SUFFIXES), default=list(SUFFIXES),
                    help="ce encodere intra in medie (implicit toate patru)")
    ap.add_argument("--cai", nargs="+", default=None, metavar="NUME=CALE",
                    help="mediaza fisierele date explicit, in loc de cele patru encodere canonice")
    ap.add_argument("--dest", default=DEST, help="unde se scrie CSV-ul rezultat")
    a = ap.parse_args(argv)
    dest = a.dest
    frames = {}
    if a.cai:
        for spec in a.cai:
            if "=" not in spec:
                sys.exit(f"--cai vrea NUME=CALE, am primit {spec!r}")
            k, p = spec.split("=", 1)
            if not os.path.exists(p):
                sys.exit(f"{p} lipseste")
            frames[k] = pd.read_csv(p).drop_duplicates(KEY).set_index(KEY).sort_index()
    else:
        for k in a.encodere:
            suf = SUFFIXES[k]
            p = os.path.join(OUT, f"e1_frozen_preds{suf}_lemma_fert_inloc.csv")
            if not os.path.exists(p):
                sys.exit(f"{p} lipseste")
            frames[k] = pd.read_csv(p).drop_duplicates(KEY).set_index(KEY).sort_index()

    ref = frames[next(iter(frames))]
    for k, d in frames.items():
        if not d.index.equals(ref.index):
            sys.exit(f"{k} n-are aceleasi randuri ca {next(iter(frames))}: {len(d)} fata de {len(ref)}")
    print(f"[enc] {len(ref)} randuri, aceleasi pe toate cele {len(frames)} encodere")

    out = ref.copy()
    for c in COLS:
        acc = np.zeros(len(ref))
        for k, d in frames.items():
            z = np.zeros(len(d))
            for (sp, lg), g in d.groupby(level=["split", "lang"], sort=False):
                pos = d.index.get_indexer(g.index)
                z[pos] = zscore(g[c].values)
            acc += z
        out[c] = acc / len(frames)
    out.reset_index().to_csv(dest, index=False)
    print(f"-> {dest}")

    # Verificare: r al mediei per limba, pe test, langa cele patru brate individuale.
    te = out.reset_index()
    te = te[te["split"] == "test"]
    from scipy.stats import pearsonr
    rows = []
    for lg, g in te.groupby("lang"):
        r = {"lang": lg, "medie": pearsonr(g["p_multi"], g["complexity"])[0]}
        for k, d in frames.items():
            h = d.reset_index()
            h = h[(h["split"] == "test") & (h["lang"] == lg)]
            r[k] = pearsonr(h["p_multi"], h["complexity"])[0]
        rows.append(r)
    t = pd.DataFrame(rows).set_index("lang")
    t["oracol"] = t[list(frames)].max(axis=1)
    print("\n" + t.round(4).to_string())
    print("\nmedii:", t.mean().round(4).to_dict())
    return 0


if __name__ == "__main__":
    sys.exit(main())
