"""Din `output/promptlab_<split>/<model>.csv` scoate un CSV de distributii pe care il citeste
`make_fs_runs.py`.

`prompt_lab` scrie un rand per (instanta, varianta) si nu are coloana `C`: surprisal-ul nu depinde de
prompt, deci nu se remasoara. Aici se lipesc cele doua: distributia noua din `prompt_lab` si `C`
copiat VERBATIM din CSV-ul de bake-off al sistemului. Plata dubla pentru acelasi numar nu se face.

Fisierul iese cu UN SINGUR slot de prompt, `p1_* / raw1`, fiindca varianta are un singur soft-read.
`make_fs_runs.prompt_cols` citeste asta din date si trateaza sursa ca un prompt, nu ca doi.

Alinierea randurilor e POZITIONALA, cu verificare pe limba, tinta si complexitate rand cu rand, exact
ca `bakeoff_trial.with_context`: `prompt_lab.measure` parcurge `load_mlsp(split)` cu `itertuples` si
scrie fiecare rand, deci pozitia e o cheie exacta, iar tinta singura nu ar fi (se repeta).

Controlul care se ruleaza de la sine: `B` recalculat din coloanele `p1_*` trebuie sa dea EXACT
`score`-ul scris de `prompt_lab`, fiindca celulele sunt scrise cu `repr(float(x))`, adica
reprezentarea scurta care face roundtrip exact. Daca acolo apare o diferenta, altceva s-a rupt.

Rulare:
  python make_fs_dist.py --variant v3_fewshot --tag fewshot
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
MODEL = "gemma4-12b-4bit"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--variant", required=True, help="varianta din prompt_lab.VARIANTS")
    ap.add_argument("--split", default="test", choices=("trial", "test"))
    ap.add_argument("--tag", required=True, help="prefixul fisierului scris in output/dist/")
    a = ap.parse_args()

    from prompt_lab import csv_path
    src = csv_path(a.model, a.split)
    from bakeoff_trial import csv_path as bt_path
    base = bt_path(a.model, a.split)
    for q in (src, base):
        if not os.path.exists(q):
            raise SystemExit(f"{q} lipseste")

    d = pd.read_csv(src)
    d = d[d["variant"] == a.variant].reset_index(drop=True)
    if not len(d):
        raise SystemExit(f"{src} n-are randuri cu varianta {a.variant!r}. Variante: "
                         f"{sorted(pd.read_csv(src)['variant'].unique())}")
    b = pd.read_csv(base)
    if len(d) != len(b):
        raise SystemExit(f"{a.variant} are {len(d)} randuri, {base} are {len(b)}. Rularea nu e "
                         "completa, si un fisier de distributii pe jumatate nu are voie sa iasa.")
    bad = ((d["lang"].astype(str).values != b["lang"].astype(str).values)
           | (d["token"].astype(str).values != b["token"].astype(str).values)
           | (np.abs(d["complexity"].values - b["complexity"].values) > 1e-6))
    if bad.any():
        i = int(np.flatnonzero(bad)[0])
        raise SystemExit(f"alinierea pozitionala a esuat la randul {i}: prompt_lab are "
                         f"({d['lang'][i]}, {d['token'][i]}), bake-off are "
                         f"({b['lang'][i]}, {b['token'][i]})")

    pc = [f"p1_{k}" for k in "12345"]
    P = d[pc].values.astype(float)
    deg = ~np.isfinite(P).all(axis=1)
    if deg.any():
        raise SystemExit(f"{int(deg.sum())} randuri cu masa degenerata (distributie goala), primul "
                         f"la {int(np.flatnonzero(deg)[0])}. Se decide ce se face cu ele inainte de "
                         "a scrie fisierul, nu se mediaza pe jumatati de coloana.")
    # Controlul de roundtrip: B recalculat din coloane fata de `score`-ul scris de prompt_lab.
    rec = (P @ np.arange(1.0, 6.0) - 1.0) / 4.0
    got = d["score"].values.astype(float)
    same = int(sum(f"{x:.8f}" == f"{y:.8f}" for x, y in zip(rec, got)))
    mx = float(np.abs(rec - got).max())
    print(f"[FSD] roundtrip: {same}/{len(d)} randuri identice la 8 zecimale, max |dif| = {mx:.3e}")
    # Pragul e 1e-8 si nu egalitate de siruri: `score` e scris cu `.8f`, deci pierde de la a noua
    # zecimala in jos, iar o valoare care cade pe granita de rotunjire ar da un sir diferit fara ca
    # nimic sa fie rupt. Ce trebuie sa fie exact sunt CELULELE, si ele trec prin `repr(float(x))`.
    if not (mx <= 1e-8):
        raise SystemExit(f"coloanele de distributie nu reproduc `score`: max |dif| = {mx:.3e} > 1e-8. "
                         "Nu se scrie nimic.")
    nrm = np.abs(P.sum(axis=1) - 1.0).max()
    print(f"[FSD] normalizare: max |sum(p) - 1| = {nrm:.3e}")
    print(f"[FSD] masa bruta: medie {d['raw1'].mean():.6f}, minim {d['raw1'].min():.6e}")

    out = pd.DataFrame({
        "lang": b["lang"].astype(str).values,
        "token": b["token"].values,
        "complexity": [f"{v:.6f}" for v in b["complexity"].values],
        "B": [f"{v:.8f}" for v in rec],
        # `C` VERBATIM din bake-off-ul sistemului, cu tot cu cele 31 de goluri: surprisal-ul nu
        # depinde de prompt, deci recalcularea lui ar fi plata dubla pentru acelasi numar.
        "C": ["" if not np.isfinite(v) else f"{v:.8f}" for v in b["C"].values],
        # `sec` e timpul rularii NOI, nu al sistemului: e singura coloana in care fisierul asta are
        # dreptul sa vorbeasca despre costul lui.
        "sec": [f"{v:.4f}" for v in d["sec"].values]})
    for k in "12345":
        out[f"p1_{k}"] = [repr(float(x)) for x in d[f"p1_{k}"].values]
    out["raw1"] = [repr(float(x)) for x in d["raw1"].values]

    q = os.path.join(OUT, "dist", f"{a.tag}_{a.model}_{a.split}.csv")
    os.makedirs(os.path.dirname(q), exist_ok=True)
    out.to_csv(q, index=False, lineterminator="\r\n")
    print(f"[FSD] {len(out)} randuri, un slot de prompt -> {q}")
    print(f"[FSD] C: {int((~np.isfinite(b['C'].values)).sum())} goluri, copiate ca goluri")
    return 0


if __name__ == "__main__":
    sys.exit(main())
