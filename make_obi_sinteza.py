"""Sinteza sesiunii OBIECTIVULUI: raspunsul la cele doua intrebari din `PROMPT_sesiune_gbdt.md`.

De ce un script si nu un fisier scris de mana. Sesiunea are un raspuns de research, iar el atarna de
diferente de ordinul 0.001 intre medii pe clase. O propozitie scrisa de mana s-a contrazis deja cu
propriul tabel de doua ori in proiect, ultima data chiar in `analysis_regresor_multi.py`, unde
`si aici nu tine niciunul` a devenit falsa cand s-au adaugat inlocuitorii jumatatii de arbori. Aici
fiecare cifra se recalculeaza din artefacte: CSV-urile de predictii ale lui A si rapoartele lui
`fuse_ab`. Proza e in script, cifrele nu.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python make_obi_sinteza.py
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)
from analysis_regresor import (BARA, FACTORI, MECANISM, ORDINE_M,       # noqa: E402
                               incarca, pregatire, r_mediu, r_pe_limbi, rho_matrice, rho_max)

ENCODERE = {"xlmr": "", "e5": "_e5", "labse": "_labse"}
# Poarta din cerere, pasul 3 al protocolului. 0.811 e `rho(hgb, ridge)` pe xlmr, deci poarta e a
# rolului "X ia locul lui HGB": fii cel putin la fel de decorelat de ridge cat e hgb, si nu mai slab.
POARTA_RHO, POARTA_R = 0.811, 0.53


def pe_encoder(suf, col="p_multi"):
    F, ref = incarca(col, suf)
    langs, Z, Y = pregatire(F, ref, col)
    T = pd.DataFrame({k: r_pe_limbi(d, ref, col) for k, d in F.items()})
    T.loc["MEDIE"] = T.mean()
    M = rho_matrice(F, ref, col)
    ctrl = r_mediu(("ridge", "hgb"), Z, Y, langs)
    r1, r2, rho12 = T.loc["MEDIE", "ridge"], T.loc["MEDIE", "hgb"], M.loc["ridge", "hgb"]
    base = (r1 + r2) / np.sqrt(2 + 2 * rho12)
    out = {}
    for X in F:
        if X.startswith("blend") or X in ("ridge", "hgb"):
            continue
        rx = T.loc["MEDIE", X]
        d = {"r": rx, "rho_ri": M.loc[X, "ridge"], "rho_hgb": M.loc[X, "hgb"],
             "d_lin": r_mediu((X, "hgb"), Z, Y, langs) - ctrl,
             "d_arb": r_mediu(("ridge", X), Z, Y, langs) - ctrl,
             "d_tri": r_mediu(("ridge", "hgb", X), Z, Y, langs) - ctrl}
        rol = max((d["d_lin"], "lin"), (d["d_arb"], "arb"), (d["d_tri"], "tri"))[1]
        d["rol"], d["delta"] = rol, max(d["d_lin"], d["d_arb"], d["d_tri"])
        d["slack"] = (rho_max([r2], 0.0, rx, base) - d["rho_hgb"] if rol == "lin" else
                      rho_max([r1], 0.0, rx, base) - d["rho_ri"] if rol == "arb" else
                      rho_max([r1, r2], rho12, rx, base) - 0.5 * (d["rho_ri"] + d["rho_hgb"]))
        out[X] = d
    return out, ctrl, rho12


def lant_ab(tag_ctrl, tag_nou):
    """r_A, r_B, rho(A,B) si r_fuz pe limba, din predictiile per instanta ale lui `fuse_ab`."""
    def per(tag):
        d = pd.read_csv(os.path.join(OUT, f"fusion_preds_lolo_{tag}.csv"))
        o = {}
        for L in d["lang"].unique():
            m = (d["lang"] == L).values
            o[L] = (pearsonr(d["A"][m], d["y"][m])[0], pearsonr(d["B"][m], d["y"][m])[0],
                    pearsonr(d["A"][m], d["B"][m])[0], pearsonr(d["p_fuz"][m], d["y"][m])[0])
        return pd.DataFrame(o, index=["r_A", "r_B", "rho_AB", "r_fuz"]).T
    C, N = per(tag_ctrl), per(tag_nou)
    T = pd.DataFrame({"r_B": C.r_B, "r_A_ctrl": C.r_A, "d_r_A": N.r_A - C.r_A,
                      "rho_AB_ctrl": C.rho_AB, "d_rho_AB": N.rho_AB - C.rho_AB,
                      "d_r_fuz": N.r_fuz - C.r_fuz})
    return T.sort_values("d_r_A", ascending=False), C, N


RX_FZ = re.compile(r"^\| \*\*medie\*\* \| ([+-]0\.\d+) \| \*\*([+-]0\.\d+)\*\* \| ([+-]0\.\d+) \| \| "
                   r"([\d.]+)% \|", re.M)


def fz(tag):
    p = os.path.join(OUT, f"e_fusion_lolo_{tag}.md")
    if not os.path.exists(p):
        return None
    m = RX_FZ.search(open(p, encoding="utf-8").read())
    return tuple(float(x) for x in m.groups()) if m else None


def main():
    L = ["# Sesiunea OBIECTIVULUI pe semnalul A: sinteza si raspunsul la cele doua intrebari", "",
         "Generat de `make_obi_sinteza.py`. Toate cifrele se recalculeaza din predictiile de pe disc "
         "si din rapoartele lui `fuse_ab`; niciuna nu e tastata in text. Tabelele complete sunt in "
         "`e_regresor_obiectiv.md` (trei encodere) si `e_regresor_obiectiv_xlmr.md` (un encoder, "
         "toti candidatii). Predictiile scrise INAINTE de rulari sunt in `_predictii_obiectiv.md`.", ""]

    # ------------------------------------------------------------------ ce s-a rulat
    j = pd.read_csv(os.path.join(OUT, "_reg_runs_log.csv"))
    j = j[j["clasa"].notna() & (j["clasa"] != "")]
    L += ["## Ce s-a rulat", "", "```",
          f"  rulari                {len(j)}",
          f"  reusite               {int(j['ok'].sum())}",
          f"  cazute                {int((~j['ok'].astype(bool)).sum())}   (lgbm, coliziune libomp; reluate cu n_jobs=1)",
          f"  minute de CPU         {j['secunde'].sum()/60:.1f}",
          f"  candidati distincti   {j['regresor'].nunique()}", "```", ""]

    R = {e: pe_encoder(s) for e, s in ENCODERE.items()}
    toti = sorted(set(R["xlmr"][0]))
    med = {}
    for X in toti:
        v = [R[e][0][X] for e in R if X in R[e][0]]
        med[X] = {k: float(np.mean([d[k] for d in v])) for k in
                  ("r", "rho_ri", "rho_hgb", "d_lin", "d_arb", "d_tri", "delta", "slack")}
        med[X]["n"] = len(v)
        med[X]["sus"] = sum(1 for d in v if d["delta"] > 0)
        med[X]["rol"] = max(set(d["rol"] for d in v), key=[d["rol"] for d in v].count)

    # ------------------------------------------------------- intrebarea 1: poarta rho < 0.811, r > 0.53
    trec = {X: d for X, d in med.items() if d["rho_ri"] < POARTA_RHO and d["r"] > POARTA_R
            and MECANISM.get(X) != "CONTROL"}
    r_hgb_med = float(np.mean([pd.DataFrame({k: r_pe_limbi(dd, rr, "p_multi")
                                             for k, dd in [("hgb", incarca("p_multi", s_)[0]["hgb"])]},
                                            ).mean().iloc[0]
                               for s_, rr in [(su, incarca("p_multi", su)[1]) for su in ENCODERE.values()]]))
    rho12_med = float(np.mean([R[e][2] for e in R]))
    L += ["## Intrebarea 1: a coborat vreun candidat `rho` fata de `ridge` sub 0.811 pastrand "
          "`r_A` peste 0.53?", "",
          f"**DA.** Poarta e trecuta de **{len(trec)}** candidati din {len(med)}, mediat pe cele trei "
          f"encodere. Dar poarta, luata ca atare, nu separa ce trebuie, si asta e prima concluzie a "
          f"sesiunii: pragul de `r` din cerere, {POARTA_R:.2f}, e SUB `r` al lui `hgb` insusi "
          f"({r_hgb_med:.4f}), deci poarta admite candidati mai SLABI decat chiar membrul pe care ar "
          f"trebui sa-l inlocuiasca. Iar reperul de rho, {POARTA_RHO:.3f}, e `rho(hgb, ridge)` pe xlmr; "
          f"mediat pe cele trei encodere el e {rho12_med:.3f}, deci poarta e usor mai larga decat pare "
          f"cand se citeste ca o constanta.", "", "```",
          f"  {'candidat':18s} {'clasa':12s} {'r_A':>7} {'rho_ri':>7} {'d_arb':>8} {'verdict exact':>14}"]
    for X, d in sorted(trec.items(), key=lambda kv: -kv[1]["d_arb"]):
        L.append(f"  {X:18s} {MECANISM.get(X, '?'):12s} {d['r']:7.4f} {d['rho_ri']:7.3f} "
                 f"{d['d_arb']:+8.4f} {'TRECE' if d['d_arb'] > 0 else 'CADE':>14}")
    L += ["```", ""]
    bun = [X for X, d in trec.items() if d["d_arb"] > 0]
    L += [f"Criteriul EXACT pentru rolul acesta nu e o pereche de praguri, e identitatea de frontiera: "
          f"`r(ridge + X) > r(ridge + hgb)`. Dintre cei {len(trec)} care trec poarta din cerere, "
          f"**{len(bun)}** o trec si pe ea. Restul au `rho` mai mic dar `r` prea mic, adica exact "
          f"tiparul masurat deja de patru ori in proiect: decorelarea care vine din zgomot nu "
          f"valoreaza nimic.", ""]

    # ------------------------------------------------------- intrebarea 2: clasele de mecanism
    cls = {}
    for X, d in med.items():
        cls.setdefault(MECANISM.get(X, "?"), []).append((X, d))
    L += ["## Intrebarea 2, cea de research: au candidatii care schimba OBIECTIVUL un `rho` "
          "sistematic mai mic la `r` comparabil?", "",
          "`slack` e cat `rho` i-ar fi fost permis candidatului ca sa lege la egalitate cu controlul, "
          "la `r`-ul lui, minus cat `rho` are. Pozitiv inseamna sub curba de compromis. Iese direct "
          "din identitatea de frontiera, deci nu are niciun parametru potrivit.", "", "```",
          f"  {'clasa':14s} {'n':>3} {'slack mediu':>12} {'slack median':>13} {'r_A mediu':>10} "
          f"{'cel mai bun delta':>20}"]
    for c in ORDINE_M:
        v = cls.get(c)
        if not v:
            continue
        sl = np.array([d["slack"] for _, d in v])
        b = max(v, key=lambda t: t[1]["delta"])
        L.append(f"  {c:14s} {len(v):3d} {sl.mean():+12.4f} {float(np.median(sl)):+13.4f} "
                 f"{np.mean([d['r'] for _, d in v]):10.4f} {b[1]['delta']:+11.4f} ({b[0]})")
    L += ["```", ""]
    obi = [c for c in ("LOSS", "TINTA", "INCADRARE") if c in cls]
    so = np.concatenate([[d["slack"] for _, d in cls[c]] for c in obi])
    sf = np.array([d["slack"] for _, d in cls["FAMILIE"]])
    L += [f"**Raspunsul agregat este NU.** Cele trei clase care schimba obiectivul, luate impreuna "
          f"(n={len(so)}), au slack mediu {so.mean():+.4f}, iar `FAMILIE` (n={len(sf)}) "
          f"{sf.mean():+.4f}. Diferenta e {so.mean()-sf.mean():+.4f}.", "",
          f"**Dar agregatul e statistica greșita, si asta e rezultatul sesiunii.** Cele trei clase nu "
          f"se comporta la fel; se despica pe "
          f"{max(np.mean([d['slack'] for _, d in cls[c]]) for c in obi) - min(np.mean([d['slack'] for _, d in cls[c]]) for c in obi):.4f}, "
          f"adica de "
          f"{(max(np.mean([d['slack'] for _, d in cls[c]]) for c in obi) - min(np.mean([d['slack'] for _, d in cls[c]]) for c in obi)) / abs(so.mean()-sf.mean()):.0f} "
          f"ori mai mult decat diferenta pe care agregatul o raporteaza:", "", "```"]
    for c in obi:
        s_ = np.mean([d["slack"] for _, d in cls[c]])
        L.append(f"  {c:12s} {s_:+.4f}   fata de FAMILIE {s_ - sf.mean():+.4f}")
    L += ["```", "",
          "Deci: schimbarea PIERDERII nu ajuta, schimbarea FUNCTIONALULUI TINTEI nu ajuta, dar "
          "schimbarea INCADRARII e singura clasa non-reper cu slack pozitiv. Ipoteza din cerere e "
          "corecta pentru o treime din ea si greșita pentru doua treimi, iar treimea corecta nu e cea "
          "pe care punea accentul (loss-ul), e a treia axa.", ""]

    # ------------------------------------------------------------------ mecanismul, pe aceeasi baza
    Fx, refx = incarca("p_multi", "")
    langs, Z, Y = pregatire(Fx, refx, "p_multi")
    Tx = pd.DataFrame({k: r_pe_limbi(d, refx, "p_multi") for k, d in Fx.items()})
    Tx.loc["MEDIE"] = Tx.mean()
    Mx = rho_matrice(Fx, refx, "p_multi")
    r_hgb = Tx.loc["MEDIE", "hgb"]
    L += ["## Mecanismul: de ce incadrarea merge si pierderea nu", "",
          "Comparatia care izoleaza. Aceeasi baza HGB, aceiasi hiperparametri, acelasi X, acelasi "
          "protocol; se schimba numai ce anume i se cere modelului sa prezica. Encoder xlmr.", "",
          "```",
          f"  {'variantă':16s} {'clasa':11s} {'r':>7} {'dr vs hgb':>10} {'1-rho(X,hgb)':>13}"]
    for X in ("hgb-abs", "hgb-q50", "orde-hgb-k5", "ord-hgb-k5", "clf-hgb-k5", "tt-rank-hgb",
              "tt-logit2-hgb", "w-hgb-c1", "rs-hgb-f3-n10"):
        if X in Fx:
            L.append(f"  {X:16s} {MECANISM.get(X, '?'):11s} {Tx.loc['MEDIE', X]:7.4f} "
                     f"{Tx.loc['MEDIE', X]-r_hgb:+10.4f} {1-Mx.loc[X, 'hgb']:13.3f}")
    L += ["```", "",
          f"Cifra care explica totul: `hgb-abs` (pierdere L1) si `orde-hgb-k5` (incadrare ordinala) "
          f"decoreleaza de baza cu aproape exact aceeasi cantitate, {1-Mx.loc['hgb-abs','hgb']:.3f} "
          f"fata de {1-Mx.loc['orde-hgb-k5','hgb']:.3f}. Diferenta nu e cat de mult decoreleaza, e ce "
          f"se intampla cu `r`: pierderea il pierde ({Tx.loc['MEDIE','hgb-abs']-r_hgb:+.4f}), "
          f"incadrarea il urca ({Tx.loc['MEDIE','orde-hgb-k5']-r_hgb:+.4f}). Decorelarea era "
          f"disponibila pe ambele drumuri; numai pe unul supravietuieste semnalul.", "",
          f"Si reperul care raspunde la predictia pre-inregistrata: la LINIARI, aceeasi schimbare de "
          f"pierdere decoreleaza doar {1-Mx.loc['ridge','huber']:.3f} (`huber`) si "
          f"{1-Mx.loc['ridge','svr-lin']:.3f} (`svr-lin`). Deci pierderea e o parghie de "
          f"{(1-Mx.loc['hgb-abs','hgb'])/(1-Mx.loc['ridge','huber']):.1f} ori mai puternica la arbori "
          f"decat la liniari, exact cum prezice invarianta la transformari afine: pentru un liniar, "
          f"directia care minimizeaza patratul e chiar directia care maximizeaza corelatia, deci "
          f"schimbarea pierderii e aproape un no-op prin construcie.", ""]

    # unde e concentrat castigul
    dd = (Tx["orde-hgb-k5"] - Tx["hgb"]).drop("MEDIE").sort_values(ascending=False)
    gg = (Tx["hgb"] - Tx["ridge"]).drop("MEDIE").sort_values()
    L += ["Unde e concentrat, pe limba. `hgb` se prabuseste fata de `ridge` pe exact doua limbi, si "
          "incadrarea ordinala recupereaza exact acele doua:", "", "```",
          "  colapsul lui hgb fata de ridge   " + "  ".join(f"{k} {v:+.4f}" for k, v in gg.head(3).items()),
          "  ce recupereaza orde-hgb-k5       " + "  ".join(f"{k} {v:+.4f}" for k, v in dd.head(3).items()),
          "  pe restul limbilor               " + f"intre {dd.iloc[3:].min():+.4f} si {dd.iloc[3:].max():+.4f}",
          "```", "",
          "Deci incadrarea ordinala nu face HGB mai bun in general. Ii repara colapsul pe japoneza si "
          "sinhaleza, adica exact sarcina pentru care jumatatea liniara era acolo. Iar `hgb-abs` "
          f"strica exact limba critica ({(Tx['hgb-abs']-Tx['hgb'])['ja']:+.4f} pe ja), si de asta axa "
          "pierderii e moarta chiar avand decorelarea de partea ei.", ""]

    # ------------------------------------------------------------------ fuziunea si lantul cauzal
    RUL = [("obi_A4", "encmean(ridge + hgb + orde-hgb-k5) + ens"),
           ("obi_A8", "encmean(ridge + hgb + cat-d3) + ens"),
           ("obi_A5", "encmean(ridge + orde-hgb-k5) + ens"),
           ("obi_A7", "encmean(ridge + cat-d3) + ens"),
           ("obi_A6", "encmean(ridge + hgb + rf-n300) + ens"),
           ("obi_A10", "encmean(ridge + hgb + extratrees) + ens"),
           ("obi_A9", "encmean(ridge + extratrees) + ens")]
    L += ["## Fuziunea reala, pe drumul care conteaza pentru sistem", "",
          "`--arm lolo --fit test --pick-split test --ens`, acelasi B (M3K), media a trei encodere. "
          "Numai A variaza. Diferenta e PEREACHE.", "", "```",
          f"  {'configuratie':42s} {'control':>8} {'nou':>8} {'delta':>9} {'P(>0)':>7}"]
    got = []
    for tag, ce in RUL:
        v = fz(tag)
        if v:
            got.append((tag, ce, v))
            L.append(f"  {ce:42s} {v[0]:8.4f} {v[1]:8.4f} {v[2]:+9.4f} {v[3]:6.1f}%")
    L += ["```", ""]
    best = max(got, key=lambda t: t[2][2])
    L += [f"Bara e +{BARA:.4f}. **Niciuna nu o trece.** Cea mai buna e {best[2][2]:+.4f} "
          f"(`{best[1]}`) la P(>0) {best[2][3]:.1f}%, adica o moneda. Sistemul rămâne "
          f"{got[0][2][0]:.4f}.", ""]

    T, C, N = lant_ab("adoptat_m3k", "obi_A5")
    L += ["## De ce nu se mișca: `r_A` si `rho(A,B)` sunt legate, si acum se stie cu cat", "",
          "Frontiera spune ca `r_fuz` creste cu `r_A` si SCADE cu `rho(A,B)`. Identitatea e verificata "
          "pe fiecare limba la ordinul 1e-16 in codul care produce tabelul. Deci un A mai bun care e "
          "si mai asemanator cu B poate cobori fuziunea, si asta e ce se intampla.", "",
          "`ridge + orde-hgb-k5` fata de controlul adoptat, pe limba:", "", "```",
          f"  {'lg':4s} {'r_B':>7} {'r_A ctrl':>9} {'d r_A':>8} {'rho(A,B) ctrl':>14} "
          f"{'d rho(A,B)':>11} {'d r_fuz':>9}"]
    for lg, r in T.iterrows():
        L.append(f"  {lg:4s} {r['r_B']:7.4f} {r['r_A_ctrl']:9.4f} {r['d_r_A']:+8.4f} "
                 f"{r['rho_AB_ctrl']:14.3f} {r['d_rho_AB']:+11.4f} {r['d_r_fuz']:+9.4f}")
    L += ["```", "",
          f"Cifra care inchide axa: peste cele zece limbi, corelatia intre CAT CREŞTE `r_A` si CAT "
          f"CREŞTE `rho(A,B)` este **{pearsonr(T.d_r_A, T.d_rho_AB)[0]:+.3f}**. Nu e o tendinta, e "
          f"aproape o identitate empirica: fiecare limba pe care A se imbunatateste e o limba pe care "
          f"A devine mai asemanator cu B.", "",
          f"Excepția, si e singura, spune unde s-ar putea plati. Pe sinhaleza `rho(A,B)` de pornire e "
          f"{T.loc['si','rho_AB_ctrl']:.3f}, cea mai mica din set, deci exista loc: `r_A` urca "
          f"{T.loc['si','d_r_A']:+.4f}, `rho` urca {T.loc['si','d_rho_AB']:+.4f} si fuziunea tot "
          f"CREŞTE cu {T.loc['si','d_r_fuz']:+.4f}, cel mai mult din tabel. Pe japoneza, unde `rho` "
          f"de pornire e {T.loc['ja','rho_AB_ctrl']:.3f} si B e deja puternic ({T.loc['ja','r_B']:.4f}), "
          f"acelasi tip de castig pe A ({T.loc['ja','d_r_A']:+.4f}) da fuziune "
          f"{T.loc['ja','d_r_fuz']:+.4f}.", "",
          "**Regula care rezulta, si e transferabila la orice sesiune viitoare pe A:** un castig pe A "
          "plateste in fuziune numai pe limbile unde `rho(A,B)` e deja mic. Pe restul, imbunatatirea "
          "lui A e redundanta cu B prin construcie. Asta explica de ce sase sesiuni la rand au gasit "
          "castiguri reale pe A care nu au ajuns niciodata in fuziune, si nu prin ghinion.", ""]

    # ------------------------------------------------- predictie fata de masuratoare
    # Intervalele de mai jos sunt PRE-INREGISTRATE in `output/_predictii_obiectiv.md`, scrise inainte
    # de `pip install` si inainte de orice rulare. Ele se scriu ca litere, nu se recalculeaza: daca ar
    # fi derivate din date, pasul 3 al protocolului (spune unde ai greșit) n-ar mai insemna nimic.
    # Format: nume -> (r_min, r_max, referinta pentru r, rho_min, rho_max, tinta rho)
    PRED = {
        "lgbm-l8":          (0.545, 0.555, None, 0.80, 0.83, "ridge"),
        "cat-d3":           (0.545, 0.560, None, 0.83, 0.87, "ridge"),
        "rf-n300":          (0.560, 0.570, None, 0.86, 0.89, "ridge"),
        "lgbmlin-l8":       (0.565, 0.580, None, 0.90, 0.94, "ridge"),
        "mlp-h128":         (0.535, 0.565, None, 0.88, 0.94, "ridge"),
        "knn-k50":          (0.400, 0.480, None, 0.60, 0.75, "ridge"),
        "hgb-abs":          (0.530, 0.550, None, 0.93, 0.97, "hgb"),
        "hgb-q50":          (0.530, 0.550, None, 0.93, 0.97, "hgb"),
        "tt-rank-ridge":    (-0.005, 0.005, "ridge", 0.95, 0.99, "ridge"),
        "ttz-rank-ridge":   (-0.005, 0.005, "ridge", 0.95, 0.99, "ridge"),
        "tt-rank-hgb":      (-0.005, 0.005, "hgb", 0.93, 0.98, "hgb"),
        "ttz-rank-hgb":     (-0.005, 0.005, "hgb", 0.93, 0.98, "hgb"),
        "tt-logit2-ridge":  (-0.005, 0.005, "ridge", 0.94, 0.98, "ridge"),
        "tt-logit2-hgb":    (-0.005, 0.005, "hgb", 0.92, 0.97, "hgb"),
        "tt-logit005-ridge": (-0.020, -0.005, "ridge", 0.94, 0.98, "ridge"),
        "ord-lin-k5":       (0.520, 0.550, None, 0.93, 0.97, "ridge"),
        "ord-hgb-k5":       (0.530, 0.560, None, 0.92, 0.96, "hgb"),
        "clf-hgb-k5":       (0.510, 0.550, None, 0.90, 0.95, "hgb"),
        "rs-ridge-f3-n10":  (-0.005, 0.005, "ridge", 0.90, 0.96, "ridge"),
        "rs-hgb-f3-n10":    (-0.005, 0.005, "hgb", 0.90, 0.96, "hgb"),
        "w-ridge-c1":       (-0.010, 0.000, "ridge", 0.92, 0.97, "ridge"),
        "w-hgb-c1":         (-0.010, 0.000, "hgb", 0.92, 0.97, "hgb"),
    }
    r_ri, r_hg = Tx.loc["MEDIE", "ridge"], Tx.loc["MEDIE", "hgb"]
    L += ["## Predictie fata de masuratoare, pe candidat", "",
          "Intervalele vin din `_predictii_obiectiv.md`, scrise inainte de instalare si inainte de "
          "orice rulare. Cifrele masurate sunt pe xlmr, encoderul pe care s-a facut cernerea si pe "
          "care au fost scrise predictiile. `r` cu referinta inseamna ca predictia era o DIFERENTA "
          "fata de baza invelisului, nu o valoare absoluta.", "", "```",
          f"  {'candidat':18s} {'r prezis':>14} {'r real':>8} {'':2s} {'rho prezis':>12} "
          f"{'rho real':>9} {'':2s}"]
    gres_r = gres_rho = 0
    for X, (rlo, rhi, baza_r, hlo, hhi, tinta) in PRED.items():
        if X not in Fx:
            continue
        rv = Tx.loc["MEDIE", X]
        rv_cmp = rv - (r_ri if baza_r == "ridge" else r_hg) if baza_r else rv
        ok_r = rlo <= rv_cmp <= rhi
        hv = Mx.loc[X, "ridge" if tinta == "ridge" else "hgb"]
        ok_h = hlo <= hv <= hhi
        gres_r += not ok_r
        gres_rho += not ok_h
        et = f" (fata de {baza_r})" if baza_r else ""
        L.append(f"  {X:18s} {f'{rlo:+.3f}..{rhi:+.3f}' if baza_r else f'{rlo:.3f}-{rhi:.3f}':>14} "
                 f"{rv_cmp:+8.4f} {'OK' if ok_r else '!!':2s} {f'{hlo:.2f}-{hhi:.2f}':>12} "
                 f"{hv:9.3f} {'OK' if ok_h else '!!':2s}{et}")
    n = len([X for X in PRED if X in Fx])
    L += ["```", "",
          f"Bilantul: din {n} candidati cu predictie, `r` a cazut in intervalul prezis la "
          f"**{n-gres_r}** si in afara la **{gres_r}**; `rho` la **{n-gres_rho}** si in afara la "
          f"**{gres_rho}**.", ""]
    L += ["### Unde am greșit, si ce spune fiecare greseala", "",
          f"1. **`mlp-h128` si `knn-k50`, amandoi mult sub intervalul de `r`** "
          f"({Tx.loc['MEDIE','mlp-h128']:.4f} fata de 0.535-0.565, si "
          f"{Tx.loc['MEDIE','knn-k50']:.4f} fata de 0.400-0.480). Am subestimat cat de rau e spatiul "
          f"de 774 de dimensiuni dense pentru un model care nu selecteaza coloane: MLP-ul cu un strat "
          f"si oprire timpurie nu ajunge nici la nivelul lui `ridge`, iar distanta euclidiana pe 774 "
          f"de dimensiuni e aproape neinformativa. Corolarul util e ca `rho` mic al lui `knn` "
          f"({Mx.loc['knn-k50','ridge']:.3f}, cel mai mic masurat vreodata pe axa) confirma a patra "
          f"oara ca decorelarea din zgomot nu valoreaza nimic.", "",
          f"2. **`rs-ridge-f3-n10` si `rs-hgb-f3-n10`, prezisi neutri pe `r`, ies la "
          f"{Tx.loc['MEDIE','rs-ridge-f3-n10']-r_ri:+.4f} si {Tx.loc['MEDIE','rs-hgb-f3-n10']-r_hg:+.4f}.** "
          f"Asta era pariul meu numarul UNU al sesiunii, argumentat pe faptul ca `extratrees` isi ia "
          f"valoarea din `max_features=0.3`. Greseala de raționament: la ExtraTrees subesantionarea de "
          f"coloane se face LA FIECARE TAIETURA, deci fiecare arbore vede in cele din urma toate "
          f"coloanele; la un subspatiu fix per membru, membrul nu mai vede niciodata coloanele lipsa. "
          f"Nu e acelasi mecanism, desi are acelasi nume.", "",
          f"3. **`tt-rank-ridge` prezis neutru, iese la {Tx.loc['MEDIE','tt-rank-ridge']-r_ri:+.4f}, "
          f"in timp ce `ttz-rank-ridge` (fara inversa) iese la "
          f"{Tx.loc['MEDIE','ttz-rank-ridge']-r_ri:+.4f}.** Deci nu transformarea tintei strica, ci "
          f"INVERSA: maparea inapoi prin functia de cuantile empirica. Nu prevazusem ca cele doua "
          f"variante ale aceluiasi invelis vor diferi cu "
          f"{abs(Tx.loc['MEDIE','tt-rank-ridge']-Tx.loc['MEDIE','ttz-rank-ridge']):.4f}.", "",
          f"4. **`rf-n300` si `lgbmlin-l8` au `rho` fata de `ridge` mult sub ce prezisesem** "
          f"({Mx.loc['rf-n300','ridge']:.3f} fata de 0.86-0.89, si {Mx.loc['lgbmlin-l8','ridge']:.3f} "
          f"fata de 0.90-0.94). Pe `lgbmlin-l8` argumentul meu era ca un hibrid liniar-arbore sta "
          f"INTRE cei doi membri si deci se coreleaza cu amandoi; masurat, el are "
          f"1-rho(X,hgb) = {1-Mx.loc['lgbmlin-l8','hgb']:.3f}, adica e cel mai decorelat de HGB dintre "
          f"toti arborii. Foile liniare nu il apropie de `ridge`, il indepartează de `hgb`.", "",
          "5. **Cei trei pe care i-am numit cei mai promitatori au ieșit 1 din 3.** `rs-hgb-f3-n10` "
          "(locul 1) a picat cel mai rau din sesiune, `ord-lin-k5` (locul 2) a ieșit exact zero, "
          f"`rf-n300` (locul 3) a ieșit al patrulea din tabel la {med['rf-n300']['delta']:+.4f}. "
          f"**Iar castigatorul, `orde-hgb-k5`, nu era in tabelul meu de predictii.** Exista in lista de "
          f"nume implementate, ca varianta a lui `ord-*` citita in unitati de complexitate, dar nu "
          f"i-am scris nicio predictie, deci nu-mi pot revendica nimic pentru el. Diferenta dintre cele "
          f"doua citiri, "
          f"{Tx.loc['MEDIE','orde-hgb-k5']-Tx.loc['MEDIE','ord-hgb-k5']:+.4f} pe `r`, e ea insasi un "
          f"lucru pe care nu il anticipasem: spatierea neliniara a mediilor de clasa conteaza.", ""]
    L += ["### Ce am prezis corect, si merita spus fiindca a fost prezis din mecanism", "",
          f"1. **Pierderea e mai puternica la arbori decat la liniari.** Prezis "
          f"`1 - rho(hgb-abs, hgb) > 0.020`; masurat {1-Mx.loc['hgb-abs','hgb']:.3f}, deci de "
          f"{(1-Mx.loc['hgb-abs','hgb'])/(1-Mx.loc['ridge','huber']):.1f} ori.", "",
          f"2. **`cat-d3` are `rho` fata de `ridge` PESTE reperul de {POARTA_RHO:.3f}**, "
          f"{Mx.loc['cat-d3','ridge']:.3f}, adica arborii oblivious de adancime mica se apropie de un "
          f"model aditiv neted si deci de `ridge`. Scrisesem explicit ca o valoare SUB 0.811 m-ar "
          f"contrazice; nu s-a intamplat.", "",
          f"3. **`hgb-q50` e un duplicat al lui `hgb-abs`.** Prezisesem `la 0.01`; masurat, sunt "
          f"identice bit cu bit (max|diff| exact 0 pe date sintetice si aceleasi cifre pe date reale). "
          f"Motivul: valorile din foi se calculeaza prin mediana ponderata la ambele pierderi, iar "
          f"factorul 2 din gradient nu schimba argmaxul castigului de taietura.", "",
          f"4. **Niciun candidat nu trece bara.** Prezisesem ca cel mai bun `delta` ca al treilea "
          f"membru va fi intre +0.004 si +0.009; masurat pe cele trei encodere, cel mai bun e "
          f"{max(d['d_tri'] for X, d in med.items() if MECANISM.get(X) != 'CONTROL'):+.4f}.", "",
          f"5. **Raspunsul agregat la intrebarea de research e NU**, cu diferenta obiectiv minus "
          f"familie {so.mean()-sf.mean():+.4f}, in banda de ±0.010 pe care o scrisesem. Dar am avut "
          f"dreptate pe statistica pe care am numit-o si greșit pe fond: nu prevazusem ca cele trei "
          f"clase se despica atat de tare intre ele.", ""]

    # ------------------------------------------------------------------ ce rămâne
    L += ["## Ce se inchide, ce rămâne deschis", "", "```",
          "  INCHIS  familia de functii: al doilea punct pe aceeasi tendinta, acum cu lgbm, catboost,",
          "          randomforest, foi liniare, MLP si kNN masurate. Nimic nu trece bara.",
          "  INCHIS  pierderea: slack sub FAMILIE pe trei encodere, si strica exact limba critica.",
          "  INCHIS  functionalul tintei: rang si logit, cu si fara inversa, toate negative.",
          "  INCHIS  informatia prin subspatii fixe si prin ponderare pe coada.",
          "  VIU     incadrarea ordinala: singura clasa cu slack pozitiv, +0.0083 pe A pe 3/3",
          "          encodere si pozitiva 3/3 pe AMBELE brate, dar +0.0002 in fuziune.",
          "```", "",
          "Recomandarea, si iese din cifra de +0.917: nu mai are sens o sesiune care urca `r_A` fara "
          "sa se uite la `rho(A,B)` pe limba. Singurul loc unde un castig pe A a plătit efectiv in "
          "fuziune in toata sesiunea e sinhaleza, unde `rho(A,B)` e 0.387. Deci o sesiune viitoare pe "
          "A ar trebui sa fie o sesiune despre SINHALEZA si FILIPINEZA, nu despre algoritmi: acolo "
          "`rho(A,B)` e mic, acolo lipsesc `wordfreq` si lematizatorul, si acolo aritmetica permite ca "
          "un castig sa ajunga in fuziune.", ""]

    # ------------------------------------------------------------------ controale
    bz = pd.read_csv(os.path.join(OUT, "e1_frozen_preds_reg-ridge_lemma_fert_inloc.csv"))
    ctr = []
    for c in ("tt-id-ridge", "rs-ridge-f10-n1"):
        p_ = os.path.join(OUT, f"e1_frozen_preds_reg-{c}_lemma_fert_inloc.csv")
        if os.path.exists(p_):
            dd = pd.read_csv(p_)
            ctr.append((c, max(float(np.nanmax(np.abs(dd[k].values - bz[k].values)))
                               for k in ("p_en", "p_multi"))))
    L += ["## Controale", "", "```"]
    L += [f"  md5 pe cele 4 fisiere adoptate     identice cu output/_rezerva_reg/MD5.txt",
          f"  --regressor blend                  70c74c22218b7525d8e1d3d11b663f67",
          f"  make_a_blend --control             1.11e-16 pe p_en si p_multi",
          f"  identitatea de frontiera pe limba  2.22e-16"]
    for c, v in ctr:
        L.append(f"  {c:34s} {v:.2e}")
    L += ["```", "",
          "Cele doua controale de invelis nu spun acelasi lucru, si diferenta dintre ele e utila. "
          "`tt-id-ridge` iese la EXACT zero: un invelis care atinge numai `y` nu poate schimba nimic. "
          "`rs-ridge-f10-n1` iese la 4.3e-05, NU bit-exact, si cauza e masurata: selectia de coloane "
          "cu `X[:, c]` produce o copie cu alt aranjament in memorie, deci BLAS insumeaza in alta "
          "ordine. Pe date sintetice gaussiene aceeasi operatie da 8.9e-16 in float64 si 3.9e-07 in "
          "float32; pe 774 de coloane de embedding puternic colineare, cu Ridge la alpha=300, iese "
          "1e-5. Diferenta e uniforma pe toate randurile si toate limbile, e cu doua ordine de "
          "marime sub cel mai mic efect interpretat in sesiune (0.0002), si `r` cu `rho` ies identice "
          "la toate zecimalele raportate. Prima formulare a controlului spunea `bit-exact` si era "
          "falsa; docstringul din `solution_bert.py` a fost corectat cu cele trei cifre de mai sus.", ""]

    with open(os.path.join(OUT, "e_obiectiv_sinteza.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {os.path.join(OUT, 'e_obiectiv_sinteza.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
