"""Frontiera de decorelare aplicata la MEMBRII semnalului A, ca POARTA inainte de a rula ceva.

De ce exista. Sesiunea pe semnalul B a stabilit ca formula

    r_ens = (suma r_i) / sqrt(n + 2 * suma_{i<j} rho_ij)

nu e o aproximare, e o IDENTITATE algebrica pentru corelatia mediei STANDARDIZATE a membrilor
(verificata la 3.3e-16). Membrii semnalului A, adica encoderele, sunt exact in acelasi regim:
corelatii intre 0.846 si 0.887. Deci se poate spune INAINTE de a descarca un model ce r si ce rho
i-ar trebui ca sa mute media, in loc sa se descarce si sa se vada dupa.

Ce face:
  1. reproduce frontiera pe membrii de acum si verifica identitatea PE LIMBA, nu doar pe medie;
  2. masoara factorul de transmisie A -> fuziune din rapoartele existente, deci din fisier, nu dintr-o
     constanta scrisa de mana;
  3. scoate curbele de prag: pentru un membru nou cu calitatea r4, care e rho maxim ca sa treaca bara;
  4. daca i se da un candidat real cu `--candidat NUME=CALE`, ii calculeaza r si rho fata de membrii
     de acum si prezice castigul, INAINTE de a rula fuziunea.

Rulare:
  python analysis_frontiera_enc.py
  python analysis_frontiera_enc.py --candidat glot500=output/e1_frozen_preds_glot500_lemma_fert_inloc.csv
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

# Membrii ADOPTATI, cei trei din `encmean-fara-xlmr-large`. Nu se citeste o constanta: caile sunt
# aceleasi pe care `make_enc_mean.py` le mediaza.
MEMBRI = {"xlmr": "", "labse": "_labse", "e5": "_e5"}
COL = "p_multi"
BARA = 0.0045          # castigul onest, dupa scaderea optimismului de selectie de +0.001937


def _p(suf):
    return os.path.join(OUT, f"e1_frozen_preds{suf}_lemma_fert_inloc.csv")


def zin(v):
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std()


def per_lang(frames, col=COL):
    """{limba: (matrice n x k de membri standardizati, y)} pe splitul de test."""
    langs = sorted(next(iter(frames.values()))["lang"].unique())
    out = {}
    for lg in langs:
        cols, y = [], None
        for k, d in frames.items():
            g = d[d["lang"] == lg]
            cols.append(zin(g[col].values))
            y = g["complexity"].values.astype(float)
        out[lg] = (np.column_stack(cols), y)
    return out


def frontiera(Z, y):
    """(r prezis de formula, r masurat al mediei standardizate, r_i, rho_ij)."""
    k = Z.shape[1]
    r = np.array([pearsonr(Z[:, i], y)[0] for i in range(k)])
    rho = {(i, j): pearsonr(Z[:, i], Z[:, j])[0] for i, j in itertools.combinations(range(k), 2)}
    pred = r.sum() / np.sqrt(k + 2 * sum(rho.values()))
    masurat = pearsonr(Z.mean(1), y)[0]
    return pred, masurat, r, rho


def transmisia():
    """Factorul A -> fuziune, citit din rapoartele de pe disc. NU o constanta scrisa de mana.

    Cele trei rulari au ACELASI brat B si acelasi protocol `--pick-split test`, deci singura
    diferenta e sursa lui A. Media pe limbi a lui `r_A_raw` si `r_fuz_raw`, ca peste tot.
    """
    surse = {"un xlmr": "fusion_lolo_ens_picktest.csv",
             "media a 3": "fusion_lolo_ens_encmean-fara-large_picktest.csv",
             "media a 4": "fusion_lolo_encmean4_picktest.csv"}
    rows = []
    for nume, f in surse.items():
        p = os.path.join(OUT, f)
        if not os.path.exists(p):
            print(f"  [!] {f} lipseste, se sare")
            continue
        d = pd.read_csv(p)
        rows.append(dict(sursa=nume, r_A=d["r_A_raw"].mean(), r_fuz=d["r_fuz_raw"].mean()))
    t = pd.DataFrame(rows)
    if len(t) < 2:
        return t, np.nan, np.nan
    baza = t.iloc[0]
    t["d_A"] = t["r_A"] - baza["r_A"]
    t["d_fuz"] = t["r_fuz"] - baza["r_fuz"]
    t["factor"] = np.where(t["d_A"] > 1e-9, t["d_fuz"] / t["d_A"], np.nan)
    mediu = float(t["factor"].dropna().mean())
    # factorul MARGINAL, de la ultima configuratie la cea dinaintea ei: e cel care guverneaza
    # urmatorul pas, fiindca de acolo pornim
    marg = np.nan
    if len(t) >= 3:
        dA = t.iloc[2]["r_A"] - t.iloc[1]["r_A"]
        dF = t.iloc[2]["r_fuz"] - t.iloc[1]["r_fuz"]
        marg = dF / dA if abs(dA) > 1e-9 else np.nan
    return t, mediu, marg


def prag_rho(r_sum, rho_sum, k, r_now, r4, dA_cerut):
    """Rho mediu maxim al unui membru nou cu calitate r4, ca media sa urce cu `dA_cerut`."""
    tinta = r_now + dA_cerut
    num = r_sum + r4
    den = (num / tinta) ** 2
    rest = den - (k + 1) - 2 * rho_sum
    return rest / (2 * k)                      # rho mediu fata de cei k membri existenti


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidat", action="append", default=None, metavar="NUME=CALE")
    ap.add_argument("--col", default=COL)
    a = ap.parse_args(argv)

    frames = {}
    for k, suf in MEMBRI.items():
        p = _p(suf)
        if not os.path.exists(p):
            sys.exit(f"{p} lipseste")
        d = pd.read_csv(p)
        frames[k] = d[d["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)

    L = ["# Frontiera de decorelare pe membrii semnalului A", "",
         "Generat de `analysis_frontiera_enc.py`. Coloana e `%s`, splitul e test." % a.col, ""]

    # --- 1. identitatea, PE LIMBA
    pl = per_lang(frames, a.col)
    rows = []
    for lg, (Z, y) in pl.items():
        pred, mas, r, rho = frontiera(Z, y)
        rows.append(dict(lang=lg, n=len(y), prezis=pred, masurat=mas, eroare=pred - mas,
                         rho_med=np.mean(list(rho.values())), **{f"r_{k}": v for k, v in zip(frames, r)}))
    t = pd.DataFrame(rows).set_index("lang")
    L += ["## Identitatea se verifica pe fiecare limba, nu doar pe medie", "",
          "```", t.round(6).to_string(), "```", "",
          f"Eroarea maxima in valoare absoluta: **{t['eroare'].abs().max():.2e}**. "
          "Nu e o aproximare buna, e o identitate algebrica.", "",
          f"Media pe limbi: prezis {t['prezis'].mean():.6f}, masurat {t['masurat'].mean():.6f}.", ""]

    # --- 2. transmisia A -> fuziune
    tt, mediu, marg = transmisia()
    L += ["## Factorul de transmisie A -> fuziune, citit din rapoarte", "",
          "Cele trei rulari au acelasi brat B si acelasi protocol, deci singura diferenta e A.", "",
          "```", tt.round(6).to_string(index=False), "```", "",
          f"Factor mediu **{mediu:.3f}**, factor MARGINAL de la media a 3 la media a 4 **{marg:.3f}**.",
          "Factorul scade pe masura ce A se imbunatateste, deci cel marginal e cel care guverneaza "
          "urmatorul pas.", ""]

    dA_opt = BARA / mediu
    dA_pes = BARA / marg
    L += [f"Ca fuziunea sa urce cu bara de +{BARA:.4f}, bratul A trebuie sa urce cu "
          f"**+{dA_opt:.4f}** (optimist, factorul mediu) pana la **+{dA_pes:.4f}** "
          f"(pesimist, factorul marginal).", ""]

    # --- 3. curbele de prag
    r_now = t["masurat"].mean()
    # sumele se iau pe MEDIA peste limbi, ca aproximare declarata a curbei de prag
    r_sum = float(np.mean([sum(pearsonr(Z[:, i], y)[0] for i in range(Z.shape[1]))
                           for Z, y in pl.values()]))
    rho_sum = float(np.mean([sum(frontiera(Z, y)[3].values()) for Z, y in pl.values()]))
    k = len(frames)
    L += ["## Ce r si ce rho ar trebui sa aiba un membru NOU. Scris inainte de a-l cauta", "",
          f"Membrii de acum: k = {k}, suma r = {r_sum:.4f}, suma rho pe perechi = {rho_sum:.4f}, "
          f"media lor = {r_now:.6f}.", "",
          "Rho maxim admis, ca sa treaca bara, pentru fiecare calitate a membrului nou:", "",
          "```", "r al membrului nou   rho max (optimist)   rho max (pesimist)"]
    for r4 in (0.45, 0.50, 0.55, 0.578, 0.60, 0.62, 0.65, 0.70):
        po = prag_rho(r_sum, rho_sum, k, r_now, r4, dA_opt)
        pp = prag_rho(r_sum, rho_sum, k, r_now, r4, dA_pes)
        f = lambda x: ("imposibil" if x < -1 else "orice" if x > 1 else f"{x:.3f}")
        L += [f"{r4:<20.3f} {f(po):<20} {f(pp)}"]
    L += ["```", "",
          "Membrii de acum sunt la rho 0.846-0.887. Citind tabelul: **un membru din aceeasi familie, "
          "cu aceeasi calitate, e mort inainte de a fi rulat.** Ce trebuie cautat nu e un encoder mai "
          "bun, e unul structural diferit.", ""]

    # --- 4. candidati reali
    if a.candidat:
        L += ["## Candidati evaluati", ""]
        for spec in a.candidat:
            nume, cale = spec.split("=", 1)
            if not os.path.exists(cale):
                L += [f"- `{nume}`: {cale} lipseste, nu s-a evaluat", ""]
                continue
            dc = pd.read_csv(cale)
            dc = dc[dc["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
            f2 = dict(frames); f2[nume] = dc
            pl2 = per_lang(f2, a.col)
            rr = []
            for lg, (Z, y) in pl2.items():
                pred, mas, r, rho = frontiera(Z, y)
                rho_new = np.mean([rho[(i, k)] for i in range(k)])
                rr.append(dict(lang=lg, r_nou=r[-1], rho_la_ceilalti=rho_new,
                               ens_prezis=pred, ens_masurat=mas, ens_acum=pl[lg] and
                               pearsonr(pl[lg][0].mean(1), pl[lg][1])[0]))
            tc = pd.DataFrame(rr).set_index("lang")
            tc["castig_A"] = tc["ens_masurat"] - tc["ens_acum"]
            dA = tc["castig_A"].mean()
            L += [f"### `{nume}`", "", "```", tc.round(4).to_string(), "```", "",
                  f"r mediu al membrului nou **{tc['r_nou'].mean():.4f}**, "
                  f"rho mediu fata de cei trei **{tc['rho_la_ceilalti'].mean():.4f}**.",
                  f"Castig pe bratul A: **{dA:+.4f}**. "
                  f"Prin factorul de transmisie, castig prezis pe fuziune intre "
                  f"**{dA*marg:+.4f}** si **{dA*mediu:+.4f}**.",
                  f"Verdict fata de bara de +{BARA:.4f}: "
                  f"**{'TRECE chiar si pesimist' if dA*marg > BARA else 'trece doar optimist' if dA*mediu > BARA else 'NU trece'}**.",
                  "", "Cifra de mai sus e o PREDICTIE a frontierei plus a transmisiei. "
                  "Nu inlocuieste rularea fuziunii cu interval pereche.", ""]

    dest = os.path.join(OUT, "e_frontiera_enc.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
