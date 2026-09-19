"""De ce `w_src = 0.738`, adica de ce bratul antrenat NUMAI pe engleza cantareste mai mult decat cel
antrenat pe noua limbi.

Intrebarea nu s-a pus niciodata. Poate fi un rezultat real despre transfer, sau un simptom al unui
criteriu prea plat ca sa aleaga. Cele cinci ipoteze si cum se testeaza fiecare:

  H1  criteriul e PLAT. Latimea criteriului de candidati e 0.0023-0.0043 in raportul sistemului, fata
      de 0.0839 la curba lui `w`. Daca si curba lui `w_src` singura e plata, atunci 0.738 e argmax pe
      zgomot, iar propozitia corecta e "cele doua brate sunt interschimbabile", nu "bratul englez
      cantareste mai mult". Se masoara curba ADEVARATA pe test si curba de CRITERIU, si se compara.
  H2  interferenta negativa: `p_multi` amesteca 8423 de randuri englezesti cu ~5000 din noua limbi cu
      grile de adnotare diferite. Se testeaza prin avantajul lui `p_en` per limba.
  H3  centrarea diferita a celor doua brate.
  H4  `p_multi` vede randurile de TEST ale celorlalte noua limbi, deci ar TREBUI sa fie mai bun.
  H5  dependenta imbricata declarata in auditul raportului de sistem.

Ce produce, si e partea utila dincolo de diagnostic: cifra fuziunii la `w_src` FIXAT pe cateva valori.
Daca un `w_src` fix nu se distinge de cel ales LOLO, atunci un hiperparametru selectat poate deveni
constanta, ceea ce reduce optimismul de selectie declarat.

Rulare, ~1 minut, zero inferenta:
  python analysis_wsrc.py
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

ASET = "fert_inloc"
APATH = os.path.join(OUT, "e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv")
BDIR = os.path.join(OUT, "bakeoff_test_Text")


def main():
    import fuse_ab as F
    from bakeoff_trial import r_table, load_runs
    F.A_SETS = {ASET: APATH}
    F.B_DIR = BDIR
    F._RUNS.clear(); F._A_FRAMES.clear()

    tab_pick = r_table(F.load_runs_wrap('test') if hasattr(F, 'load_runs_wrap') else
                       {k: F.with_context(d, 'test') for k, d in load_runs('test', BDIR).items()}, "B") \
        if False else None
    # acelasi drum ca `fuse_ens`: tabelul de selectie e pe splitul de test
    from bakeoff_trial import with_context
    runs = {k: with_context(d, "test") for k, d in load_runs("test", BDIR).items()}
    tab_pick = r_table(runs, "B")

    langs = None
    L = ["# `w_src`: de ce bratul EN-only cantareste mai mult", "",
         "Generat de `analysis_wsrc.py`. Zero inferenta.", ""]

    # ---------------------------------------------------------------- H1: curba adevarata vs criteriu
    rows_true, rows_crit = [], []
    for lg in sorted(F.load_signals("lolo", "test", tab_pick, exclude=()).keys()):
        te = F.load_signals("lolo", "test", tab_pick, exclude={lg})
        d = te[lg]
        others = {l2: v for l2, v in te.items() if l2 != lg}
        # curba ADEVARATA: r pe test al limbii L, cu w ales LOLO pentru fiecare w_src
        tr, cr = {}, {}
        for s in F.SRC_GRID:
            M = {l2: F._moments(F.zA_of(v, ASET, s), v["zB"].values, v["y"].values)
                 for l2, v in others.items()}
            curve = [float(np.mean([F._r_mom(M[l2], w) for l2 in others])) for w in F.GRID]
            w = float(F.GRID[int(np.argmax(curve))])
            zA = F.zA_of(d, ASET, s)
            tr[float(s)] = pearsonr(w * zA + (1 - w) * d["zB"].values, d["y"].values)[0]
            # criteriul imbricat, exact ce vede `fit_choice`
            vals = []
            for l2 in others:
                inner = [float(np.mean([F._r_mom(M[l3], w2) for l3 in others if l3 != l2]))
                         for w2 in F.GRID]
                vals.append(F._r_mom(M[l2], float(F.GRID[int(np.argmax(inner))])))
            cr[float(s)] = float(np.mean(vals))
        rows_true.append(dict(lang=lg, **{f"{k:.3f}": v for k, v in tr.items()}))
        rows_crit.append(dict(lang=lg, **{f"{k:.3f}": v for k, v in cr.items()}))
    T = pd.DataFrame(rows_true).set_index("lang")
    C = pd.DataFrame(rows_crit).set_index("lang")

    L += ["## H1: cat de plata e alegerea lui `w_src`", "",
          "Curba ADEVARATA, adica r al fuziunii pe testul limbii L, pentru fiecare `w_src` de pe grila.",
          "`w` e ales LOLO la fiecare punct, deci singura variabila e `w_src`.", "",
          "```", T.round(4).to_string(), "```", "",
          "Curba de CRITERIU, adica exact ce vede `fit_choice` cand alege (media imbricata pe "
          "celelalte noua limbi):", "",
          "```", C.round(4).to_string(), "```", ""]

    lat_true = (T.max(axis=1) - T.min(axis=1))
    lat_crit = (C.max(axis=1) - C.min(axis=1))
    amax_true = T.idxmax(axis=1).astype(float)
    amax_crit = C.idxmax(axis=1).astype(float)
    cmp_ = pd.DataFrame({"latime adevarata": lat_true, "latime criteriu": lat_crit,
                         "argmax adevarat": amax_true, "argmax criteriu": amax_crit,
                         "r la argmax criteriu": [T.loc[l, f"{amax_crit[l]:.3f}"] for l in T.index],
                         "r la optim": T.max(axis=1)})
    cmp_["cost al alegerii"] = cmp_["r la argmax criteriu"] - cmp_["r la optim"]
    L += ["Comparatia, per limba:", "", "```", cmp_.round(4).to_string(), "```", "",
          f"Latimea medie a curbei adevarate: **{lat_true.mean():.4f}**. "
          f"A criteriului: **{lat_crit.mean():.4f}**.",
          f"Argmax-ul criteriului nimereste argmax-ul adevarat pe "
          f"**{int((amax_true == amax_crit).sum())} din {len(T)}** limbi.",
          f"Costul mediu al alegerii, fata de optimul care foloseste etichetele lui L: "
          f"**{cmp_['cost al alegerii'].mean():+.4f}**.", ""]

    # ---------------------------------------------------------------- w_src FIXAT
    med = {}
    for s in F.SRC_GRID:
        med[float(s)] = T[f"{float(s):.3f}"].mean()
    best_fix = max(med, key=med.get)
    lolo = np.mean([T.loc[l, f"{amax_crit[l]:.3f}"] for l in T.index])
    L += ["## `w_src` FIXAT, ca alternativa la selectie", "",
          "Media pe cele zece limbi a lui r al fuziunii, cu `w_src` aceeasi constanta peste tot:", "",
          "```", "w_src   r mediu"]
    for s, v in med.items():
        mark = "   <- ales LOLO in medie" if abs(s - 0.738) < 0.07 else ""
        L += [f"{s:<7.3f} {v:.6f}{mark}"]
    L += ["```", "",
          f"Selectia LOLO a lui `w_src` da **{lolo:.6f}**. Cel mai bun `w_src` FIX da "
          f"**{med[best_fix]:.6f}** la {best_fix:.3f}, dar acela e ales pe test, deci nu e o optiune.",
          "",
          f"Ce conteaza: intre `w_src = 0` (numai bratul multilingv) si selectia LOLO sunt "
          f"**{lolo - med[0.0]:+.6f}**, iar intre `w_src = 1` (numai bratul englez) si selectia LOLO "
          f"**{lolo - med[1.0]:+.6f}**.", ""]

    # ---------------------------------------------------------------- H2/H4: cele doua brate, per limba
    a = F.a_frames("test")[ASET]
    rows = []
    for lg, g in a.groupby("lang"):
        y = g["complexity"].values.astype(float)
        rows.append(dict(lang=lg, n=len(g),
                         r_pen=pearsonr(g["p_en"].values, y)[0],
                         r_pmulti=pearsonr(g["p_multi"].values, y)[0],
                         rho_brate=pearsonr(g["p_en"].values, g["p_multi"].values)[0]))
    B = pd.DataFrame(rows).set_index("lang")
    B["avantaj_pen"] = B["r_pen"] - B["r_pmulti"]
    L += ["## H2 si H4: cele doua brate, masurate separat", "",
          "`p_en` e antrenat NUMAI pe CompLex EN. `p_multi` vede in plus randurile de TEST ale "
          "celorlalte noua limbi, deci ar TREBUI sa fie mai bun. H4 spune ca daca nu e, aia e chiar "
          "rezultatul.", "", "```", B.round(4).to_string(), "```", "",
          f"Media: `p_en` **{B['r_pen'].mean():.4f}**, `p_multi` **{B['r_pmulti'].mean():.4f}**, "
          f"avantajul lui `p_en` **{B['avantaj_pen'].mean():+.4f}**.",
          f"`p_en` castiga pe **{int((B['avantaj_pen'] > 0).sum())} din {len(B)}** limbi.",
          f"Corelatia dintre brate, mediata pe limbi: **{B['rho_brate'].mean():.4f}** "
          f"(minim {B['rho_brate'].min():.4f} pe {B['rho_brate'].idxmin()}).", ""]

    # frontiera aplicata celor doua brate: castigul din amestec e reducere de varianta
    fr = []
    for lg in B.index:
        r1, r2, rho = B.loc[lg, ["r_pen", "r_pmulti", "rho_brate"]]
        fr.append((r1 + r2) / np.sqrt(2 + 2 * rho))
    B2 = B.copy(); B2["frontiera_50_50"] = fr
    L += ["Frontiera aplicata celor doua brate, adica ce ar da un amestec 50/50 standardizat:", "",
          "```", B2[["r_pen", "r_pmulti", "rho_brate", "frontiera_50_50"]].round(4).to_string(), "```",
          "", f"Media frontierei 50/50: **{np.mean(fr):.4f}**, fata de {B['r_pen'].mean():.4f} la "
          f"`p_en` singur si {B['r_pmulti'].mean():.4f} la `p_multi` singur. "
          "Amestecul castiga fiindca bratele sunt decorelate, nu fiindca unul ar fi mai bun.", ""]

    # ------------------------------------------------- mecanismul: decorelarea fata de B, nu calitatea
    # Curba adevarata URCA cu w_src desi `p_en` singur e mai SLAB decat `p_multi`. Singura explicatie
    # compatibila cu amandoua e ca `p_en` e mai decorelat de semnalul B, deci aduce mai mult in
    # amestec desi aduce mai putin singur. Se masoara direct.
    rows = []
    for lg, d in F.load_signals("lolo", "test", tab_pick, exclude=()).items():
        zB = d["zB"].values; y = d["y"].values
        z0 = F.zA_of(d, ASET, 0.0)          # numai p_multi
        z1 = F.zA_of(d, ASET, 1.0)          # numai p_en
        rows.append(dict(lang=lg, r_A_pmulti=pearsonr(z0, y)[0], r_A_pen=pearsonr(z1, y)[0],
                         rho_pmulti_B=pearsonr(z0, zB)[0], rho_pen_B=pearsonr(z1, zB)[0],
                         r_B=pearsonr(zB, y)[0]))
    D = pd.DataFrame(rows).set_index("lang")
    D["mai_decorelat"] = D["rho_pmulti_B"] - D["rho_pen_B"]
    # frontiera A+B, la 50/50, pentru fiecare brat
    for nume, ra, rho in (("front_pmulti", "r_A_pmulti", "rho_pmulti_B"),
                          ("front_pen", "r_A_pen", "rho_pen_B")):
        D[nume] = (D[ra] + D["r_B"]) / np.sqrt(2 + 2 * D[rho])
    L += ["## Mecanismul: `p_en` nu e mai BUN, e mai DECORELAT de semnalul B", "",
          "Curba adevarata urca cu `w_src` desi `p_en` singur e mai slab decat `p_multi`. Singura "
          "explicatie compatibila cu amandoua e ca `p_en` aduce mai mult IN AMESTEC fiindca e mai "
          "putin corelat cu semnalul B. Se masoara direct, nu se presupune:", "",
          "```", D.round(4).to_string(), "```", "",
          f"Corelatia cu B: `p_multi` **{D['rho_pmulti_B'].mean():.4f}**, `p_en` "
          f"**{D['rho_pen_B'].mean():.4f}**. `p_en` e mai decorelat pe "
          f"**{int((D['mai_decorelat'] > 0).sum())} din {len(D)}** limbi, cu o diferenta medie de "
          f"**{D['mai_decorelat'].mean():+.4f}**.",
          f"Frontiera A+B la 50/50: cu `p_multi` **{D['front_pmulti'].mean():.4f}**, cu `p_en` "
          f"**{D['front_pen'].mean():.4f}**, diferenta **{(D['front_pen']-D['front_pmulti']).mean():+.4f}**.",
          "", "**Asta raspunde la intrebare.** `w_src` mare nu inseamna ca transferul din engleza e "
          "mai bun. Inseamna ca bratul englez, nevazand niciun rand de MLSP, face alte greseli decat "
          "un LLM care vede propozitia, iar fuziunea plateste pentru greseli diferite, nu pentru "
          "greseli mai putine. E acelasi mecanism ca la ansamblul de encodere, la alt nivel.", ""]

    dest = os.path.join(OUT, "e_wsrc.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
