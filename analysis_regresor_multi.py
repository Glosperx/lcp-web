"""Axa liniara a semnalului A, citita pe TOATE cele trei encodere deodata.

De ce exista, si de ce nu e acelasi lucru cu a rula `analysis_regresor.py` de trei ori. Rapoartele
per encoder raspund fiecare la "cine e cel mai bun aici". Intrebarea care decide adoptarea e alta:
**acelasi candidat urca in toate trei, sau numai in unul?** Sistemul adoptat nu e un encoder, e media
a trei (`encmean-fara-xlmr-large`), deci un candidat care bate `ridge` doar pe xlmr n-are de unde sa
mute cifra de sistem, si un candidat care urca pe toate trei o mută chiar daca pe fiecare in parte
marginea e subtire.

Ce se compara, si de ce ASA. Pentru fiecare encoder si fiecare candidat X, controlul e `ridge+hgb`
pe ACELASI encoder, iar cifra e `r(X+hgb) - r(ridge+hgb)`, media celor zece r pe limba. Deci se
schimba numai jumatatea liniara, partenerul e acelasi, si encoderul e acelasi. Nu se compara niciodata
un candidat de pe un encoder cu un control de pe altul.

`semn` e cate encodere din cele disponibile merg in aceeasi directie. E cifra care conteaza mai mult
decat media: trei din trei la +0.002 e un efect, unul din trei la +0.006 e o loterie cu trei bilete.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_regresor_multi.py
"""
import argparse
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

from analysis_regresor import (FAMILII, BARA, FACTORI, COL, MECANISM, ORDINE_M,   # noqa: E402
                               incarca, pregatire, r_mediu, r_pe_limbi, rho_matrice, rho_max)

# Aceeasi harta ca `ENC_SUF` din `make_reg_runs.py` si ca `SUFFIXES` din `make_enc_mean.py`: sufixul
# de encoder din `_p()` sta pe aceeasi pozitie ca prefixul de spatiu, deci se da lui `--spatiu`.
ENCODERE = {"xlmr": "", "e5": "_e5", "labse": "_labse"}


def per_encoder(enc, spatiu, col):
    F, ref = incarca(col, spatiu)
    if not {"ridge", "hgb"} <= set(F):
        return None
    langs, Z, Y = pregatire(F, ref, col)
    T = pd.DataFrame({k: r_pe_limbi(d, ref, col) for k, d in F.items()})
    T.loc["MEDIE"] = T.mean()
    M = rho_matrice(F, ref, col)
    ctrl = r_mediu(("ridge", "hgb"), Z, Y, langs)
    out = {}
    r1, r2 = T.loc["MEDIE", "ridge"], T.loc["MEDIE", "hgb"]
    rho12 = M.loc["ridge", "hgb"]
    base = (r1 + r2) / np.sqrt(2 + 2 * rho12)
    for X in F:
        # `blend*` sunt ele insele medii care CONTIN hgb, deci `X + hgb` l-ar pune de doua ori.
        if X.startswith("blend") or X == "hgb":
            continue
        # CELE TREI ROLURI. Pana pe 26 august aici era numai primul, fiindca sesiunea de atunci era
        # despre liniari. Pe `extratrees` cele trei dau -0.0079, +0.0086 si +0.0080: rolul muta
        # verdictul cu 0.017, deci un tabel cu un singur rol nu masoara ce spune.
        d_lin = r_mediu((X, "hgb"), Z, Y, langs) - ctrl        # X in locul lui ridge
        d_arb = (r_mediu(("ridge", X), Z, Y, langs) - ctrl) if X != "ridge" else 0.0
        d_tri = (r_mediu(("ridge", "hgb", X), Z, Y, langs) - ctrl) if X != "ridge" else 0.0
        rol = max((d_lin, "lin"), (d_arb, "arb"), (d_tri, "tri"))[1]
        rx = T.loc["MEDIE", X]
        if rol == "lin":
            sl = rho_max([r2], 0.0, rx, base) - M.loc[X, "hgb"]
        elif rol == "arb":
            sl = rho_max([r1], 0.0, rx, base) - M.loc[X, "ridge"]
        else:
            sl = rho_max([r1, r2], rho12, rx, base) - 0.5 * (M.loc[X, "ridge"] + M.loc[X, "hgb"])
        out[X] = {"r_A": rx, "rho_hgb": M.loc[X, "hgb"], "rho_ridge": M.loc[X, "ridge"],
                  "d_lin": d_lin, "d_arb": d_arb, "d_tri": d_tri,
                  "delta": max(d_lin, d_arb, d_tri), "rol": rol, "slack": sl}
    return {"enc": enc, "ctrl": ctrl, "cand": out, "n_lang": len(langs)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--col", default=COL)
    ap.add_argument("--out", default=os.path.join(OUT, "e_regresor_liniar.md"))
    a = ap.parse_args(argv)

    R = {}
    for enc, suf in ENCODERE.items():
        r = per_encoder(enc, suf, a.col)
        if r is None:
            print(f"[multi] {enc}: lipsesc `ridge` sau `hgb`, encoderul se sare", flush=True)
            continue
        R[enc] = r
        print(f"[multi] {enc}: {len(r['cand'])} candidati, control ridge+hgb {r['ctrl']:.6f}",
              flush=True)
    if not R:
        sys.exit("niciun encoder complet pe disc")

    encs = list(R)
    toti = sorted({X for r in R.values() for X in r["cand"]})
    L = ["# Axa LINIARA a semnalului A, pe toate encoderele", "",
         "Generat de `analysis_regresor_multi.py`. Coloana `%s`, splitul test, configuratia "
         "`--lemma-freq --afeat fert_inloc`. Bratul B nu intra nicaieri." % a.col, "",
         "Jumatatea liniara a blend-ului a fost `Ridge(alpha=300)` in absolut toate variantele "
         "masurate vreodata pe axa regresorului; tot ce s-a schimbat pana acum a fost jumatatea de "
         "arbori. Aici se schimba liniarul, cu ACELASI partener `hgb` si pe ACELASI encoder.", "",
         "Controlul, per encoder, e `ridge+hgb` ca medie standardizata:", "", "```"]
    L += [f"  {e:6s} {R[e]['ctrl']:.6f}   ({R[e]['n_lang']} limbi)" for e in encs]
    L += ["```", "",
          f"Bara pe fuziune e +{BARA:.4f} si factorul de transmisie A -> fuziune e "
          f"{FACTORI['optimist']:.3f} mediu, deci un candidat trebuie sa urce A cu "
          f"+{BARA/FACTORI['optimist']:.4f} ca sa fie chiar si optimist adoptabil.", ""]

    # ------------------------------------------------------- tabelul transversal, ordonat pe medie
    rows = []
    for X in toti:
        d = {e: R[e]["cand"][X]["delta"] for e in encs if X in R[e]["cand"]}
        if not d:
            continue
        v = list(d.values())
        roluri = [R[e]["cand"][X]["rol"] for e in encs if X in R[e]["cand"]]
        rows.append({"cand": X, "n": len(v), "medie": float(np.mean(v)),
                     "rol": max(set(roluri), key=roluri.count),
                     "sus": sum(1 for x in v if x > 0), **{f"d_{e}": d.get(e) for e in encs}})
    D = pd.DataFrame(rows).sort_values("medie", ascending=False)

    L += ["## delta pe A fata de `ridge+hgb`, per encoder", "",
          "`sus` e pe cate encodere din `n` diferenta e pozitiva. Trei din trei la +0.002 e un efect; "
          "unu din trei la +0.006 e o loterie cu trei bilete.", "",
          "`delta` e cel mai bun dintre CELE TREI ROLURI in care poate intra candidatul: in locul "
          "jumatatii liniare, in locul jumatatii de arbori, sau ca al treilea membru. Rolul ales e in "
          "coloana `rol` (`lin`, `arb`, `tri`), si e majoritar peste encodere. Un arbore judecat numai "
          "in rol de liniar iese cel mai prost din tabel chiar cand e cel mai bun al treilea membru; "
          "pe `extratrees` diferenta intre roluri e 0.017.", "", "```",
          f"  {'candidat':16s} {'clasa':12s} {'rol':4s}" + "".join(f"{e:>10}" for e in encs)
          + f"{'medie':>10}{'sus':>6}"]
    for _, r in D.iterrows():
        # `ridge` e chiar controlul, deci delta lui e zero prin construcie si `sus` n-are sens acolo.
        # Se marcheaza, ca randul sa nu se citeasca drept "candidat care pierde pe 3 din 3".
        coada = "   <- controlul" if r["cand"] == "ridge" else \
                f"{int(r['sus']):>4}/{int(r['n'])}"
        L.append(f"  {r['cand']:16s} {MECANISM.get(r['cand'], '?'):12s} {r['rol']:4s}"
                 + "".join(f"{r[f'd_{e}']:+10.4f}" if pd.notna(r[f"d_{e}"]) else f"{'-':>10}"
                           for e in encs)
                 + f"{r['medie']:+10.4f}" + coada)
    L += ["```", ""]

    # ---------------------------------------------------- clasa de mecanism, pe toate encoderele
    # Intrebarea de research a sesiunii din 26 august, pusa pe cifra care conteaza: nu care candidat e
    # cel mai bun, ci daca schimbarea OBIECTIVULUI coboara rho sistematic la r comparabil, fata de
    # schimbarea formei functiei. Clasele sunt scrise in `output/_predictii_obiectiv.md` INAINTE de
    # rulari; daca ar fi atribuite dupa, comparatia n-ar insemna nimic.
    cls = {}
    for X in toti:
        v = [R[e]["cand"][X] for e in encs if X in R[e]["cand"]]
        if not v or X == "ridge":
            continue
        cls.setdefault(MECANISM.get(X, "?"), []).append(
            (X, float(np.mean([d["r_A"] for d in v])), float(np.mean([d["slack"] for d in v])),
             float(np.mean([d["delta"] for d in v]))))
    L += ["## Clasa de mecanism: intrebarea de research", "",
          "`slack` e cat rho i-ar fi fost PERMIS candidatului ca sa lege la egalitate cu controlul, la "
          "r-ul lui, minus cat rho are. Pozitiv inseamna sub curba de compromis. Iese direct din "
          "identitatea de frontiera, deci nu are niciun parametru potrivit, si e formulat in exact "
          "unitatile in care e pusa intrebarea: rho, la r comparabil.", "",
          "`REGULARIZARE` e norul de referinta: pierdere patratica, liniar dens, numai penalizarea "
          "variaza.", "", "```",
          f"  {'clasa':14s} {'n':>3} {'slack mediu':>12} {'slack median':>13} {'r_A mediu':>10} "
          f"{'cel mai bun delta':>20}"]
    for c in ORDINE_M:
        v = cls.get(c)
        if not v:
            continue
        sl = np.array([x[2] for x in v])
        bst = max(v, key=lambda x: x[3])
        L.append(f"  {c:14s} {len(v):3d} {sl.mean():+12.4f} {float(np.median(sl)):+13.4f} "
                 f"{float(np.mean([x[1] for x in v])):10.4f} {bst[3]:+11.4f} ({bst[0]})")
    L += ["```", ""]
    obi = [c for c in ("LOSS", "TINTA", "INCADRARE") if c in cls]
    if obi and "FAMILIE" in cls:
        so = np.concatenate([[x[2] for x in cls[c]] for c in obi])
        sf = np.array([x[2] for x in cls["FAMILIE"]])
        sr = np.array([x[2] for x in cls.get("REGULARIZARE", [])])
        L += [f"Raspunsul direct: clasele care schimba OBIECTIVUL (`" + "`, `".join(obi)
              + f"`, n={len(so)}) au slack mediu **{so.mean():+.4f}**; clasa `FAMILIE` (n={len(sf)}) "
              f"**{sf.mean():+.4f}**"
              + (f"; norul de referinta `REGULARIZARE` (n={len(sr)}) **{sr.mean():+.4f}**"
                 if len(sr) else "") + f". Diferenta obiectiv minus familie e "
              f"**{so.mean()-sf.mean():+.4f}**, iar imprastierea in interiorul norului de referinta e "
              + (f"de la {sr.min():+.4f} la {sr.max():+.4f}" if len(sr) else "necalculabila") + ".", ""]

    cast = D[(D["sus"] == D["n"]) & (D["medie"] > 0) & (D["cand"] != "ridge")]
    if len(cast):
        L += ["Candidatii pozitivi pe TOATE encoderele pe care s-au rulat:", "", "```"]
        L += [f"  {r['cand']:16s} medie {r['medie']:+.4f}   "
              f"fuziune implicata {r['medie']*FACTORI['optimist']:+.4f} (optimist)"
              for _, r in cast.iterrows()]
        L += ["```", "",
              f"Bara e +{BARA:.4f} pe fuziune. Cei care o trec chiar si pe estimarea optimista: "
              + (", ".join(f"`{r['cand']}`" for _, r in cast.iterrows()
                           if r["medie"] * FACTORI["optimist"] >= BARA) or "**niciunul**") + ".", ""]
    else:
        L += ["**Niciun candidat nu e pozitiv pe toate encoderele.** Adica pe axa asta nu exista un "
              "efect care sa se transfere; ce se vede pe un encoder nu se vede pe celelalte.", ""]

    # ------------------------------------------------------------------- rho, cifra care de fapt decide
    L += ["## rho fata de AMBII membri, per encoder", "",
          "Conteaza amandoua, si care anume depinde de rol: `rho(X, hgb)` decide daca X poate lua locul "
          "jumatatii LINIARE, `rho(X, ridge)` daca poate lua locul celei de ARBORI, si amandoua daca "
          "intra ca al treilea. Reperul e `rho(ridge, hgb)`, adica exact cat de decorelati sunt cei doi "
          "membri de acum.", "", "```",
          f"  {'candidat':16s} {'clasa':12s}" + "".join(f"{e+' ri':>10}" for e in encs)
          + "".join(f"{e+' hgb':>11}" for e in encs)]
    for X in ["ridge"] + [x for x in toti if x != "ridge"]:
        if not any(X in R[e]["cand"] for e in encs):
            continue
        vr = [R[e]["cand"][X].get("rho_ridge") if X in R[e]["cand"] else None for e in encs]
        vh = [R[e]["cand"][X]["rho_hgb"] if X in R[e]["cand"] else None for e in encs]
        L.append(f"  {X:16s} {MECANISM.get(X, '?'):12s}"
                 + "".join(f"{x:10.3f}" if x is not None else f"{'-':>10}" for x in vr)
                 + "".join(f"{x:11.3f}" if x is not None else f"{'-':>11}" for x in vh)
                 + ("   <- reperul, rho(ridge,hgb) e coloana hgb" if X == "ridge" else ""))
    L += ["```", ""]
    rho_ridge = [R[e]["cand"]["ridge"]["rho_hgb"] for e in encs if "ridge" in R[e]["cand"]]
    mai_jos = [X for X in toti
               if all(X in R[e]["cand"] and R[e]["cand"][X]["rho_hgb"] < R[e]["cand"]["ridge"]["rho_hgb"]
                      for e in encs)]
    L += [f"`rho(ridge, hgb)` e {', '.join(f'{x:.3f}' for x in rho_ridge)} pe cele "
          f"{len(rho_ridge)} encodere. Candidati cu rho STRICT mai mic pe toate: "
          + (", ".join(f"`{x}`" for x in mai_jos) if mai_jos else "**niciunul**") + ".", ""]

    # ------------------------------------------------------------------- grilele, cate un rand fiecare
    L += ["## Grilele parametrice, punctul cel mai bun pe fiecare encoder", "",
          "Aici e doar cine iese in fata pe fiecare encoder, ca sa se vada daca optimul e STABIL. "
          "Selectia onesta, leave-one-language-out, plus latimea criteriului, e in rapoartele per "
          "encoder (`e_regresor_a.md`, `e_regresor_a_e5.md`, `e_regresor_a_labse.md`).", "", "```"]
    for nume, grila in FAMILII.items():
        L.append(f"  {nume}")
        for e in encs:
            pd_ = [(n, R[e]["cand"][n]["delta"]) for n, _ in grila if n in R[e]["cand"]]
            if not pd_:
                continue
            b = max(pd_, key=lambda t: t[1])
            L.append(f"    {e:6s} cel mai bun `{b[0]}` la {b[1]:+.4f}   "
                     + " ".join(f"{n}={v:+.4f}" for n, v in pd_))
    L += ["```", ""]

    # ------------------------------------------- cele doua brate ale lui A vor regularizare OPUSA
    # Motivul pentru care merita o sectiune proprie: toata axa a fost masurata pe `p_multi`, si acolo
    # castigatorul e un L1 slab regularizat. Dar A al sistemului nu e `p_multi`, e
    # z(w_src*z(p_en) + (1-w_src)*z(p_multi)), deci un candidat trebuie sa tina pe AMBELE coloane.
    if a.col == "p_multi":
        Rp = {}
        for enc, suf in ENCODERE.items():
            r = per_encoder(enc, suf, "p_en")
            if r is not None:
                Rp[enc] = r
        if Rp:
            comun = sorted(set(toti) & {X for r in Rp.values() for X in r["cand"]})
            L += ["## Cele doua brate ale lui A sunt INDEPENDENTE", "",
                  "Tot ce e mai sus e pe `p_multi`. Dar semnalul A al sistemului nu e `p_multi`, e "
                  "`z(w_src . z(p_en) + (1 - w_src) . z(p_multi))`, cu `w_src` ales LOLO. Deci un "
                  "candidat trebuie sa tina pe AMBELE coloane. Cati tin se CALCULEAZA mai jos si nu "
                  "se afirma aici: propozitia care spunea `si aici nu tine niciunul` era corecta pe "
                  "axa liniara din 26 august si a devenit FALSA cand s-au adaugat inlocuitorii "
                  "jumatatii de arbori, fara sa crape nimic. Exact tiparul "
                  "`constante-hardcodate-mint-dupa-renumerotare`.", "",
                  "`p_en` e o SINGURA potrivire care prezice zece limbi nevazute; `p_multi` e o "
                  "potrivire per limba, cu noua limbi de test in antrenare. Doua regimuri diferite, "
                  "deci nu e de la sine inteles ca vor acelasi regresor, si masuratoarea de mai jos "
                  "spune ca intr-adevar nu se informeaza reciproc.",
                  "", "```",
                  f"  {'candidat':16s} {'p_multi':>10} {'sus':>5}   {'p_en':>10} {'sus':>5}"]
            def _m(R_, X):
                v = [R_[e]["cand"][X]["delta"] for e in R_ if X in R_[e]["cand"]]
                return (float(np.mean(v)), sum(1 for x in v if x > 0), len(v)) if v else None
            linii = []
            for X in comun:
                m1, m2 = _m(R, X), _m(Rp, X)
                if m1 and m2:
                    linii.append((m1[0], X, m1, m2))
            for _, X, m1, m2 in sorted(linii, reverse=True):
                L.append(f"  {X:16s} {m1[0]:+10.4f} {m1[1]:3d}/{m1[2]}   "
                         f"{m2[0]:+10.4f} {m2[1]:3d}/{m2[2]}"
                         + ("   <- controlul" if X == "ridge" else ""))
            L += ["```", ""]
            # Cat de tare se bat cap in cap cele doua brate, ca numar si nu ca impresie.
            if len(linii) > 2:
                v1 = np.array([m1[0] for _, _, m1, _ in linii])
                v2 = np.array([m2[0] for _, _, _, m2 in linii])
                from scipy.stats import pearsonr as _pr
                # Corelatia pe TOATI candidatii e o capcana: candidatii catastrofali (`ard`,
                # `lasso-a3e-2`, `svr-lin`) sunt prosti pe ambele brate si fabrica singuri o corelatie
                # pozitiva mare, care spune doar "prost e prost peste tot". Ce intereseaza e banda in
                # care candidatul e plauzibil, adica acolo unde s-ar putea alege ceva.
                L += [f"Corelatia intre cele doua coloane de delta, peste "
                      f"{len(linii)} candidati: **{_pr(v1, v2)[0]:+.3f}**. Dar cifra asta e "
                      f"inselatoare: candidatii catastrofali sunt prosti pe AMBELE brate si fabrica "
                      f"singuri o corelatie pozitiva care spune numai `prost e prost peste tot`. "
                      f"Restransa la banda in care s-ar putea alege ceva:", "", "```"]
                for prag in (0.010, 0.005):
                    k = [i for i in range(len(v1)) if abs(v1[i]) <= prag and abs(v2[i]) <= prag]
                    if len(k) > 3:
                        L.append(f"  |delta| <= {prag:.3f}   n={len(k):2d}   "
                                 f"pearson {_pr(v1[k], v2[k])[0]:+.3f}")
                L += ["```", "",
                      "Adica in banda utila cele doua brate sunt in mare masura **independente**: "
                      "cat ajuta un candidat pe un brat nu spune mult despre celalalt. Exemplul "
                      "canonic, de pe axa liniara, e `lasso-a1e-3`, cel mai bun pe `p_multi` si "
                      "negativ pe `p_en`. Cifrele concrete se citesc din tabelul de deasupra, nu de "
                      "aici: cand s-au adaugat rulari noi, o pereche de cifre scrisa in propozitie "
                      "a incetat sa mai fie perechea extrema si propozitia a devenit inselatoare "
                      "fara sa crape nimic.", ""]
            # Pragul e 1e-6, nu 0, si CONTROALELE se scot explicit. `rs-<baza>-f10-n1` si
            # `tt-id-<baza>` reproduc baza bit-exact, deci delta lor e zero pana la ~1e-16, iar un
            # `> 0` pe float ii ridica in lista de castigatori. Un control care apare drept candidat
            # pozitiv e exact felul de rand care face un tabel sa mintă fara sa greseasca nimic.
            amb = [X for _, X, m1, m2 in linii
                   if X != "ridge" and MECANISM.get(X) != "CONTROL"
                   and m1[1] == m1[2] and m2[1] == m2[2] and m1[0] > 1e-6 and m2[0] > 1e-6]
            L += ["Pozitivi pe 3/3 encodere pe AMBELE brate: "
                  + (", ".join(f"`{x}`" for x in amb) if amb else "**niciunul**") + ".", "",
                  "Consecinta practica, si e parghia pe care nicio configuratie de pana acum n-o "
                  "foloseste: `p_en` si `p_multi` sunt COLOANE separate in CSV, deci alpha se poate "
                  "alege pe brat, nu pe model. Asta se masoara mai jos ca `lin_A7` si `lin_A8`.", ""]

    # ------------------------------------------------------------------ fuziunea reala, daca s-a rulat
    # Cifrele se CITESC din rapoartele lui `fuse_ab`, nu se scriu de mana. O constanta scrisa de mana
    # a facut deja un raport din proiect sa se contrazica singur dupa o renumerotare, fara nicio
    # eroare. Daca un raport lipseste, randul lipseste; nu se inventeaza.
    RULARI = [
        ("lin_A1", "mean(lasso-a1e-3, hgb)", "xlmr", "xlmr_plin"),
        ("lin_A2", "mean(hgb, extratrees, pls-k16)", "xlmr", "xlmr_plin"),
        ("lin_A5", "mean(lasso-a1e-3, lasso-a3e-4, hgb)", "xlmr", "xlmr_plin"),
        ("lin_A3", "mean(lasso-a1e-3, hgb, tabfm@256)", "hibrid", "hibrid_rht"),
        ("lin_A4", "encmean(mean(lasso-a1e-3, hgb)) + ens", "3 encodere", "adoptat_m3k"),
        ("lin_A6", "encmean(mean(ridge-a1000, hgb)) + ens", "3 encodere", "adoptat_m3k"),
        ("lin_A8", "p_en de la ridge-a3000, p_multi neatins", "3 encodere", "adoptat_m3k"),
        ("lin_A7", "p_en ridge-a3000 + p_multi lasso-a1e-3", "3 encodere", "adoptat_m3k"),
        # Sesiunea OBIECTIVULUI. `obi_A1` si `obi_A2` sunt perechiri PRE-SPECIFICATE (rolul e unul din
        # cele trei declarate inainte de rulari), `obi_A3` e submultimea cea mai buna PE TEST din 6017,
        # deci poarta optimismul de selectie masurat la +0.0081 si nu se citeaza ca rezultat.
        ("obi_A1", "mean(ridge, orde-hgb-k5)", "xlmr", "xlmr_plin"),
        ("obi_A2", "mean(ridge, hgb, orde-hgb-k5)", "xlmr", "xlmr_plin"),
        ("obi_A3", "mean(rf-n300, orde-lin-k5, orde-hgb-k5) [ales pe test]", "xlmr", "xlmr_plin"),
        ("obi_A4", "encmean(mean(ridge, hgb, orde-hgb-k5)) + ens", "3 encodere", "adoptat_m3k"),
        ("obi_A5", "encmean(mean(ridge, orde-hgb-k5)) + ens", "3 encodere", "adoptat_m3k"),
        ("obi_A6", "encmean(mean(ridge, hgb, rf-n300)) + ens", "3 encodere", "adoptat_m3k"),
        ("obi_A7", "encmean(mean(ridge, cat-d3)) + ens", "3 encodere", "adoptat_m3k"),
        ("obi_A8", "encmean(mean(ridge, hgb, cat-d3)) + ens", "3 encodere", "adoptat_m3k"),
        ("obi_A9", "encmean(mean(ridge, extratrees)) + ens", "3 encodere", "adoptat_m3k"),
        ("obi_A10", "encmean(mean(ridge, hgb, extratrees)) + ens", "3 encodere", "adoptat_m3k"),
    ]
    rx = re.compile(r"^\| \*\*medie\*\* \| ([+-]0\.\d+) \| \*\*([+-]0\.\d+)\*\* \| "
                    r"([+-]0\.\d+) \| \| ([\d.]+)% \|", re.M)
    fz = []
    for tag, ce, spatiu, ctrl in RULARI:
        q = os.path.join(OUT, f"e_fusion_lolo_{tag}.md")
        if not os.path.exists(q):
            continue
        m = rx.search(open(q, encoding="utf-8").read())
        if m:
            fz.append((tag, ce, spatiu, ctrl, *m.groups()))
    if fz:
        L += ["## Fuziunea REALA cu semnalul B, pentru ansamblurile de top", "",
              "`--arm lolo --fit test --pick-split test`, acelasi B (M3K) peste tot, numai A variaza. "
              "Diferenta e PEREACHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e "
              "al diferentei. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese "
              "peste control.", "", "```",
              f"  {'ce':40s} {'spatiu':11s} {'control':>7} {'nou':>7} {'delta':>8} {'P(>0)':>7}"]
        for tag, ce, spatiu, ctrl, r0, r1, dd, pp in fz:
            L.append(f"  {ce:40s} {spatiu:11s} {float(r0):7.4f} {float(r1):7.4f} "
                     f"{float(dd):+8.4f} {float(pp):6.1f}%")
        # Concluzia se CALCULEAZA din tabel. Scrisa de mana, s-a contrazis deja cu propriul tabel
        # dupa ce s-au adaugat doua rulari: exact tiparul din `constante-hardcodate-mint`.
        best = max(fz, key=lambda t: float(t[6]))   # pe DELTA, ca eticheta sa nu minta
        sis = [t for t in fz if t[3] == "adoptat_m3k"]
        trec = [t for t in fz if float(t[6]) >= BARA]
        peste = [t for t in sis if float(t[6]) > 0]
        L += ["```", "",
              f"Bara pe fuziune e +{BARA:.4f}. "
              + (f"**Niciuna nu o trece.** Cea mai mare diferenta e {float(best[6]):+.4f} "
                 f"(`{best[1]}`), la P(>0) {float(best[7]):.1f}%, adica o moneda."
                 if not trec else
                 f"O trec: " + ", ".join(f"`{t[1]}` la {float(t[6]):+.4f}" for t in trec) + "."), "",
              f"Pe drumul care conteaza pentru sistem, media a trei encodere cu `--ens`, "
              f"{len(peste)} din {len(sis)} configuratii ies peste controlul adoptat, si cea mai buna "
              f"dintre ele e {max((float(t[6]) for t in sis), default=0.0):+.4f} la "
              f"P(>0) {max(sis, key=lambda t: float(t[6]))[7]}%. Nicio adoptare nu se sprijina pe "
              f"asta.", "",
              "Cifra care duce concluzia nu e nici una din diferentele de fuziune, e raportul dintre "
              "ele si castigul pe A. Reperul, masurat pe axa LINIARA in sesiunea din 26 august si "
              "citabil din `e_regresor_liniar.md`: A a urcat de la 0.5993 la 0.6023, adica +0.0030 "
              "constant si reproductibil pe toate trei encoderele, si fuziunea nu s-a miscat, deci "
              "transmisia pe acea axa a ieșit **~zero** fata de 0.09-0.26 masurat in general. Cele doua "
              "cifre 0.5993 si 0.6023 sunt ale acelei sesiuni si NU se recalculeaza aici; sunt scrise "
              "ca reper istoric, nu ca rezultat al tabelului de mai sus. Raportul de transmisie al "
              "sesiunii CURENTE se citeste din coloanele `delta` de mai sus impartite la delta pe A al "
              "configuratiei corespunzatoare.", ""]

    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
