"""Poarta de frontiera pentru TabFM, citita direct din predictiile brute.

De ce exista separat de `analysis_regresor.py`. Lantul complet (`--regressor tabfm-cache`) cheama
regresorul de DOUASPREZECE ori, deci ii trebuie si cele doua brate EN-only, iar `en_only_test`
singur costa cat 5.6 limbi. Dar verdictul nu depinde de ele: poarta se uita la `p_multi`, adica
numai la cererile per limba. Fisierul asta citeste direct `.npy`-urile scrise de `tabfm_runner.py`
si da r si rho de indata ce limbile sunt gata, cu ore inainte de restul.

Ce citeste. Fiecare cerere per limba prezice, in ordinea din `frozen_trial_gap`:

    [randurile de TEST ale lui L] ++ [trial centrat pe el insusi] ++ [trial centrat pe media de test]

deci primele `n_test(L)` valori sunt `p_multi`, si numai ele intra aici.

Pragul cu care se compara e cel din `output/e_regresor_a*.md`: un al treilea estimator la calitatea
r intra in blend numai daca rho fata de `ridge` si `hgb` e sub prag. Nu se inventeaza nimic aici,
se citeste aceeasi identitate de frontiera.

Rulare:
  python analysis_tabfm_poarta.py --preds data/tabfm_preds_proj200 \
      --blocuri data/tabfm_blocks_proj200.npz --spatiu _tf-proj-200
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)
BARA, FACTORI = 0.0045, {"optimist": 0.259, "pesimist": 0.091}


def zl(v):
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--preds", default="data/tabfm_preds_proj200")
    ap.add_argument("--blocuri", default="data/tabfm_blocks_proj200.npz")
    ap.add_argument("--spatiu", default="_tf-proj-200")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    if a.out is None:
        a.out = os.path.join(OUT, f"e_tabfm_poarta{a.spatiu.replace('_tf-', '_')}.md")

    from tabfm_bridge import cereri, req_key
    B = np.load(a.blocuri)
    lang = np.asarray(B["lang"], str)

    # referintele: aceiasi estimatori, ACELASI spatiu, altfel diferenta amesteca doua cauze
    def ref(suf):
        p = os.path.join(OUT, f"e1_frozen_preds{a.spatiu}{suf}_lemma_fert_inloc.csv")
        if not os.path.exists(p):
            sys.exit(f"lipseste referinta {p}")
        d = pd.read_csv(p)
        return d[d["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
    R = {k: ref(s) for k, s in (("ridge", "_reg-ridge"), ("hgb", "_reg-hgb"), ("blend", ""))}
    baza = R["ridge"]

    rows = []
    for nume, Xtr, ytr, Xp in cereri(B):
        if nume.startswith("en_only"):
            continue
        p = os.path.join(a.preds, req_key(Xtr, ytr, Xp) + ".npy")
        if not os.path.exists(p):
            continue
        m = (baza["lang"] == nume).values
        v = np.load(p)[:int(m.sum())]              # primele n_test valori = p_multi
        y = baza["complexity"].values[m]
        r = {"lang": nume, "n": int(m.sum()), "r_tabfm": pearsonr(v, y)[0]}
        for k, d in R.items():
            r[f"r_{k}"] = pearsonr(d["p_multi"].values[m], y)[0]
            if k != "blend":
                r[f"rho_{k}"] = pearsonr(v, d["p_multi"].values[m])[0]
        # ce ar da blend-ul daca TabFM ar intra ca al treilea membru, prin frontiera exacta
        r["ens3"] = pearsonr(zl(v) + zl(R["ridge"]["p_multi"].values[m])
                             + zl(R["hgb"]["p_multi"].values[m]), y)[0]
        r["ens2"] = pearsonr(zl(R["ridge"]["p_multi"].values[m])
                             + zl(R["hgb"]["p_multi"].values[m]), y)[0]
        rows.append(r)

    if not rows:
        sys.exit(f"nicio limba gata in {a.preds}")
    T = pd.DataFrame(rows).set_index("lang")
    T.loc["MEDIE"] = T.mean()
    M = T.loc["MEDIE"]
    rho_med = 0.5 * (M["rho_ridge"] + M["rho_hgb"])
    castig = M["ens3"] - M["ens2"]

    L = ["# Poarta de frontiera pentru TabFM", "",
         f"Generat de `analysis_tabfm_poarta.py`, spatiu `{a.spatiu.lstrip('_')}`, "
         f"{len(rows)}/10 limbi gata. Citit direct din `{a.preds}`.", "",
         "```", T.round(4).to_string(), "```", "",
         f"TabFM singur: **{M['r_tabfm']:.6f}**, fata de ridge {M['r_ridge']:.6f} si "
         f"hgb {M['r_hgb']:.6f} pe acelasi spatiu.", "",
         f"rho mediu fata de cei doi membri: **{rho_med:.4f}**. "
         f"Pentru scara, rho(ridge, hgb) e 0.811 si membrii encoderelor stau la 0.846-0.887.", "",
         f"Blend de doi (ridge+hgb): {M['ens2']:.6f}. Cu TabFM ca al treilea: "
         f"**{M['ens3']:.6f}**, adica **{castig:+.6f}**.", "",
         f"Bara ceruta pe brat, ca fuziunea sa urce cu +{BARA:.4f}: "
         f"+{BARA/FACTORI['optimist']:.4f} (optimist) pana la +{BARA/FACTORI['pesimist']:.4f} "
         f"(pesimist).", "",
         f"**VERDICT: {'TRECE' if castig >= BARA/FACTORI['optimist'] else 'CADE'}** "
         f"chiar si la factorul optimist de transmisie.", ""]
    if len(rows) < 10:
        L += [f"Atentie: numai {len(rows)} din 10 limbi sunt gata, deci mediile inca se misca.", ""]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
