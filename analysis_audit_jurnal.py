"""Auditul jurnalului de configuratii. `output/e_rezumat_modele.csv` NU e generat de niciun script.

Se tine de mana, deci ramane in urma tacut: pe 18 august arata 0.6646 ca maxim, in timp ce pe disc
existau deja si 0.6720, si 0.6696. Un jurnal care ramane in urma e mai rau decat niciun jurnal,
fiindca il citesti crezand ca stii ce s-a masurat.

Auditul, si e simplu: pentru fiecare artefact de pe disc se calculeaza cifra lui si se cauta in
coloana `r_mediu` a jurnalului, la a patra zecimala.

  `output/fusion_*.csv`            media lui `r_fuz_raw` peste limbi, adica fuziunea
                                   media lui `r_A_raw` peste limbi, adica bratul A al ei
  `output/e1_frozen_preds_*.csv`   r Pearson al lui `p_multi` per limba pe test, mediat peste limbi

Nu repara nimic si nu scrie in jurnal: raporteaza ce lipseste, ca sa se adauge de mana. Iesire 0 daca
totul e acoperit, 1 daca lipseste ceva.

Rulare, ~15 secunde:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_audit_jurnal.py
"""
import glob
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
JURNAL = os.path.join(OUT, "e_rezumat_modele.csv")
TOL = 5e-5           # jurnalul are patru zecimale, deci toleranta e a rotunjirii lui


def cifre_fuziune():
    """Din fiecare `fusion_*.csv`: fuziunea si bratul ei A, ca medii peste limbi."""
    out = []
    for p in sorted(glob.glob(os.path.join(OUT, "fusion_*.csv"))):
        b = os.path.basename(p)
        if b.startswith("fusion_preds_"):
            continue                       # predictii per instanta, nu tabel per limba
        d = pd.read_csv(p)
        # Tabelele vechi n-au sufixul `_raw`, care a aparut cand s-a separat r brut de r bootstrap.
        # Fara alternativa asta auditul sarea tacut peste 15 fisiere, adica exact esecul pe care il
        # cauta: sa arate curat pentru ca n-a citit.
        n = int(d["n"].sum()) if "n" in d.columns else 0
        for cols, ce in ((("r_fuz_raw", "r_fuz"), "fuziune"), (("r_A_raw", "r_A"), "brat A")):
            col = next((c for c in cols if c in d.columns), None)
            if col:
                out.append({"artefact": b, "ce": ce, "r": float(d[col].mean()), "n_limbi": len(d),
                            "n": n})
    return out


def cifre_brat_a():
    """Din fiecare `e1_frozen_preds_*.csv`: r al lui `p_multi` per limba pe test, mediat."""
    out = []
    for p in sorted(glob.glob(os.path.join(OUT, "e1_frozen_preds*.csv"))):
        d = pd.read_csv(p)
        if not {"lang", "p_multi", "complexity"} <= set(d.columns):
            continue
        if "split" in d.columns:
            d = d[d["split"] == "test"]
        rs = []
        for lg, g in d.groupby("lang"):
            g = g.dropna(subset=["p_multi", "complexity"])
            if len(g) > 2 and g["p_multi"].std() > 0:
                rs.append(np.corrcoef(g["p_multi"], g["complexity"])[0, 1])
        if rs:
            out.append({"artefact": os.path.basename(p), "ce": "p_multi pe test",
                        "r": float(np.mean(rs)), "n_limbi": len(rs), "n": len(d)})
    return out


def main():
    if not os.path.exists(JURNAL):
        raise SystemExit(f"{JURNAL} lipseste")
    j = pd.read_csv(JURNAL)
    val = j["r_mediu"].astype(float).values
    art = cifre_fuziune() + cifre_brat_a()
    # `n` s-a schimbat la P11, de la 5606 la 5624, prin fixul de caz din `find_char_span`. Artefactele
    # ramase pe `n` vechi nu sunt „lipsa din jurnal", sunt VECHI, si a le confunda ar produce fie
    # randuri false in jurnal, fie un audit care nu iese niciodata curat. Se raporteaza separat.
    n_curent = int(j["n_itemi"].max()) if "n_itemi" in j.columns else max(
        (a["n"] for a in art), default=0)
    lipsa, vechi = [], []
    for a in art:
        if a["n"] and a["n"] != n_curent:
            vechi.append(a)
            continue
        gasit = bool(np.any(np.abs(val - a["r"]) < TOL))
        if not gasit:
            lipsa.append(a)
        print(f"  {a['r']:.6f}  {'in jurnal' if gasit else 'LIPSESTE':<10} {a['ce']:<16} "
              f"{a['artefact']}")
    print(f"[audit] n curent {n_curent} | {len(art) - len(vechi)} de cifre pe n curent, "
          f"{len(j)} de randuri in jurnal, {len(lipsa)} lipsa, {len(vechi)} artefacte pe n vechi")
    if vechi:
        ns = sorted({a["n"] for a in vechi})
        print(f"[audit] artefacte pe n vechi {ns}, ramase de dinainte de P11: "
              f"{len({a['artefact'] for a in vechi})} fisiere. Nu se adauga in jurnal; jurnalul lor e "
              "`output/e_rezumat_modele_pre-p11_n5606.csv`.")
    if lipsa:
        print("[audit] de adaugat de mana in output/e_rezumat_modele.csv:")
        for a in lipsa:
            print(f"        {a['r']:.4f}  {a['ce']}  {a['artefact']}  ({a['n_limbi']} limbi)")
        return 1
    print("[audit] curat")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
