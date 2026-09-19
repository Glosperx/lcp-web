"""Costul de inferenta al fiecarei componente, masurat pe exact randurile de test MLSP.

Decizia de adoptare a mediei de encodere are un singur argument contra care se poate cuantifica,
costul: sistemul ar cere patru encodere in loc de unul. Argumentul nu se poate cantari pe estimari,
deci aici se masoara, si se masoara lucrul care s-ar plati la inferenta pe date noi:

  encodere  `XLMR.embed_frame` peste cele 5624 de contexte de test, incarcarea modelului cronometrata
            separat de forward. NU trece prin `_embed_cached`, altfel ar citi .npy-ul si ar masura
            viteza discului. Nu scrie nimic in `data/`.
  LLM       coloana `sec` din `output/bakeoff_test/<model>.csv`, adica timpul real per item al
            rularilor care au produs semnalul B. Nu se re-ruleaza nimic.

`--pick-split test` nu apare in tabel fiindca nu are cost: schimba ce model se alege, nu cate modele
se ruleaza, iar ambele candidate erau deja rulate.

Rezultatul se scrie in `output/cost_inferenta.csv` si e citit de `analysis_adoptie.py`.

Rulare, ~6 minute, fara descarcari daca modelele sunt in cache-ul HuggingFace:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_cost_inferenta.py
"""
import os
import sys
import time

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
BAKEOFF = os.path.join(OUT, "bakeoff_test")
TABLE = os.path.join(OUT, "cost_inferenta.csv")
ENCODERE = ("xlmr", "labse", "e5", "xlmr-large")


def cost_encodere(sents, tokens):
    """Incarcare plus forward, per encoder, pe randurile date. Fara cache, fara scriere in data/."""
    from solution_bert import XLMR
    rows = []
    for enc in ENCODERE:
        t0 = time.time(); xr = XLMR("last4", enc); t_load = time.time() - t0
        t0 = time.time(); E, _ = xr.embed_frame(sents, tokens); t_fwd = time.time() - t0
        rows.append({"componenta": "encoder", "nume": enc, "n": len(sents), "dim": int(E.shape[1]),
                     "sec_incarcare": round(t_load, 1), "sec_forward": round(t_fwd, 1),
                     "ms_per_rand": round(1000 * t_fwd / len(sents), 2)})
        print(f"  {enc:<12} incarcare {t_load:6.1f}s | forward {t_fwd:7.1f}s = {t_fwd/60:5.2f} min | "
              f"{1000*t_fwd/len(sents):6.2f} ms/rand")
        del xr, E
    return rows


def cost_llm():
    """Timpul real al brațului B, din coloana `sec` a rularilor deja facute. Nicio inferenta noua."""
    rows = []
    for f in sorted(os.listdir(BAKEOFF)):
        if not f.endswith(".csv"):
            continue
        d = pd.read_csv(os.path.join(BAKEOFF, f))
        if "sec" not in d.columns:
            continue
        tot = float(d["sec"].sum())
        rows.append({"componenta": "llm", "nume": f[:-4], "n": len(d), "dim": "",
                     "sec_incarcare": "", "sec_forward": round(tot, 1),
                     "ms_per_rand": round(1000 * tot / len(d), 2)})
        print(f"  {f[:-4]:<20} n={len(d):5d} | {tot:8.1f}s = {tot/60:6.1f} min | "
              f"{tot/len(d):5.3f} s/rand")
    return rows


def main():
    from mlsp_common import load_mlsp
    ml = load_mlsp("test")
    sents, tokens = list(ml["sent"]), list(ml["token"])
    print(f"[cost] randuri de test: {len(sents)}")
    print("[cost] encodere, forward pe toate randurile de test:")
    rows = cost_encodere(sents, tokens)
    print("[cost] brațul B, din coloana `sec` a rularilor deja facute:")
    rows += cost_llm()
    pd.DataFrame(rows).to_csv(TABLE, index=False)
    print(f"-> {TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
