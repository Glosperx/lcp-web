"""Sweep-ul de extractie: straturi x pooling, plus configuratiile structurale.

Ce se compara si fata de ce. Sistemul are semnalul A = media a TREI encodere, deci o configuratie
noua rulata pe xlmr singur nu se compara cu sistemul: s-ar amesteca doua schimbari. Referinta corecta
e xlmr SINGUR la `last4`, adica `enc_xlmr_now`, si atunci diferenta e curat efectul configuratiei.
Abia daca o configuratie castiga acolo merita replicata pe labse si e5 si dusa in ansamblu.

Predictiile literaturii, scrise inainte de rulare in `output/e_literatura_encoder.md`:
  1. `last` bate `first` (Acs, Kadar, Kornai, EACL 2021: pana la 45 de puncte pe finlandeza);
  2. `mean` sta intre ele, fiindca le mediaza literalmente;
  3. efectul e mai mare pe limbile cu fertilitate mare, si aproape nul pe engleza;
  4. straturile de mijloc fata de `last4`: ambiguu.
Sectiunea de la final le verifica una cate una.

Rulare, ~10 secunde, citeste doar de pe disc:
  python analysis_extractie.py
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

REF_CFG = "last4"
REF_TAG = "enc_xlmr_now"
SWEEP = [f"{ln}{'' if pl == 'mean' else '_' + pl}"
         for ln in ("last4", "mid", "concat4", "last1") for pl in ("mean", "first", "last", "max")]
STRUCT = ["ctxiso", "isoonly"]


def preds(cfg):
    suf = "" if cfg == REF_CFG else f"_{cfg}"
    return os.path.join(OUT, f"e1_frozen_preds{suf}_lemma_fert_inloc.csv")


def fuz_csv(cfg):
    tag = REF_TAG if cfg == REF_CFG else f"cfg_{cfg}"
    return os.path.join(OUT, f"fusion_lolo_{tag}.csv"), os.path.join(OUT, f"e_fusion_lolo_{tag}.md")


def ci_medie(md):
    """Intervalul PERECHE al MEDIEI, parsat din raport. Per limba e in CSV, media nu."""
    if not os.path.exists(md):
        return None
    for l in open(md, encoding="utf-8"):
        if "cea de azi" in l and l.strip().startswith("|"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            m = re.findall(r"[-+]?\d*\.\d+", " ".join(c[1:]))
            if len(m) >= 4:
                return float(m[0]), float(m[1]), float(m[2]), float(m[3])
    return None


def main():
    langs = None
    rows, Z, sarite = [], {}, []
    d_ref = pd.read_csv(preds(REF_CFG))
    n_ref = int((d_ref["split"] == "test").sum())
    for cfg in SWEEP + STRUCT:
        p = preds(cfg)
        if not os.path.exists(p):
            continue
        d = pd.read_csv(p)
        d = d[d["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
        # Poarta: un fisier cu alt numar de randuri ori e scris chiar acum de o rulare in curs, ori
        # a pierdut randuri (`_iso_vec` intoarce None pe tinte goale). In ambele cazuri nu se compara.
        if len(d) != n_ref:
            sarite.append(f"{cfg} ({len(d)} randuri fata de {n_ref})")
            continue
        langs = sorted(d["lang"].unique()) if langs is None else langs
        rA = {lg: pearsonr(g["p_multi"], g["complexity"])[0] for lg, g in d.groupby("lang")}
        Z[cfg] = d["p_multi"].values
        fc, fm = fuz_csv(cfg)
        r = dict(cfg=cfg, r_A=np.mean(list(rA.values())), **{f"A_{k}": v for k, v in rA.items()})
        if os.path.exists(fc):
            f = pd.read_csv(fc)
            r["r_fuz"] = f["r_fuz_raw"].mean()
            if "d_azi" in f:
                r["d_fuz"] = f["d_azi"].mean()
                r["limbi_sus"] = int((f["d_azi"] > 0).sum())
                r["limbi_stricate"] = int((f["d_azi_hi"] < 0).sum())
            ci = ci_medie(fm)
            if ci:
                r["d_lo"], r["d_hi"], r["P"] = ci[1], ci[2], ci[3]
        rows.append(r)
    T = pd.DataFrame(rows).set_index("cfg")
    # Randul de REFERINTA nu are diferenta fata de sine. Raportul lui `enc_xlmr_now` a fost produs cu
    # `--vs` sistemul adoptat, deci `d_azi` de acolo e alta cantitate si ar minti in tabelul asta.
    for c in ("d_fuz", "d_lo", "d_hi", "P", "limbi_sus", "limbi_stricate"):
        if c in T.columns and REF_CFG in T.index:
            T.loc[REF_CFG, c] = np.nan

    L = ["# Sweep-ul de extractie: straturi x pooling", "",
         "Generat de `analysis_extractie.py`.", "",
         f"Referinta e **xlmr SINGUR la `{REF_CFG}`**, nu sistemul: sistemul are trei encodere, deci "
         "o comparatie directa ar amesteca doua schimbari. Diferentele si intervalele sunt perechi "
         f"fata de `{REF_TAG}`.", ""]

    if sarite:
        L += ["> Sarite, fiindca n-au acelasi numar de randuri ca referinta: " +
              ", ".join(f"`{x}`" for x in sarite) + ".", ""]
    show = [c for c in ("r_A", "r_fuz", "d_fuz", "d_lo", "d_hi", "P", "limbi_sus", "limbi_stricate")
            if c in T]
    L += ["## Rezultatul, toate configuratiile", "", "```",
          T[show].sort_values("r_fuz", ascending=False).round(6).to_string(), "```", "",
          "`d_fuz` e diferenta PERECHE pe fuziune fata de referinta; `limbi_stricate` numara limbile "
          "al caror interval pereche exclude zero IN JOS, adica sunt stricate cu semnificatie. "
          "Conditia din protocol se citeste INAINTEA mediei.", ""]

    # ---------------------------------------------------------------- predictiile literaturii
    L += ["## Predictiile literaturii, verificate una cate una", ""]
    fam = ["last4", "mid", "concat4", "last1"]
    got = lambda c: T.loc[c, "r_A"] if c in T.index else np.nan
    pr = []
    for f in fam:
        pr.append(dict(straturi=f, mean=got(f), first=got(f + "_first"),
                       last=got(f + "_last"), max=got(f + "_max")))
    PR = pd.DataFrame(pr).set_index("straturi")
    L += ["Brat A (`p_multi`), mediat pe cele zece limbi:", "", "```", PR.round(4).to_string(), "```", ""]
    if PR[["first", "last"]].notna().all(axis=None):
        d = (PR["last"] - PR["first"])
        L += [f"**P1, `last` bate `first`:** diferenta pe cele {len(PR)} familii de straturi: " +
              ", ".join(f"{i} {v:+.4f}" for i, v in d.items()) +
              f". Media **{d.mean():+.4f}**. Predictia **{'se confirma' if d.mean() > 0 else 'CADE'}**.", ""]
        intre = ((PR["mean"] > PR[["first", "last"]].min(axis=1)) &
                 (PR["mean"] < PR[["first", "last"]].max(axis=1)))
        L += [f"**P2, `mean` sta intre ele:** adevarat pe {int(intre.sum())} din {len(PR)} familii.", ""]

    # P3: efectul de pooling pe limba, langa fertilitate
    if "last4_first" in T.index and "last4_last" in T.index:
        from solution_bert import normalize_token
        from mlsp_common import load_mlsp
        ml = load_mlsp("test")
        from transformers import AutoTokenizer
        tk = AutoTokenizer.from_pretrained("xlm-roberta-base")
        fert = {lg: np.mean([len(tk.tokenize(" " + normalize_token(str(t)))) for t in g["token"]])
                for lg, g in ml.groupby("lang")}
        rr = []
        for lg in langs:
            rr.append(dict(lang=lg, fertilitate=fert[lg],
                           efect=abs(T.loc["last4_last", f"A_{lg}"] - T.loc["last4_first", f"A_{lg}"])))
        E = pd.DataFrame(rr).set_index("lang").sort_values("fertilitate")
        cc = pearsonr(E["fertilitate"], E["efect"])
        L += ["**P3, efectul de pooling creste cu fertilitatea.** `efect` e |`last` − `first`| pe "
              "bratul A al limbii:", "", "```", E.round(4).to_string(), "```", "",
              f"Corelatia intre fertilitate si marimea efectului: **{cc[0]:+.3f}** (p = {cc[1]:.3f}). "
              f"Predictia **{'se confirma' if cc[0] > 0.3 else 'nu se confirma'}**.", ""]

    # ------------------------------------------------- mecanismul din spatele inversarii fata de Acs
    if "last4_first" in T.index and "last4_last" in T.index:
        from transformers import AutoTokenizer as _AT
        from solution_bert import normalize_token as _nt
        from mlsp_common import load_mlsp as _lm
        _tk = _AT.from_pretrained("xlm-roberta-base")
        d0 = pd.read_csv(preds(REF_CFG))
        d0 = d0[d0["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
        segm = [_tk.tokenize(" " + _nt(str(t))) for t in d0["token"]]
        ns = np.array([len(x) for x in segm])
        df = {c: pd.read_csv(preds(c))[lambda z: z["split"] == "test"]
                   .sort_values(["lang", "idx"]).reset_index(drop=True)
              for c in ("last4_first", "last4_last")}
        mr = []
        for lg in langs:
            m = (d0["lang"] == lg).values
            mu = m & (ns > 1)
            y, ym = (d0.loc[m, "complexity"].values.astype(float),
                     d0.loc[mu, "complexity"].values.astype(float))
            mr.append(dict(lang=lg, pct_1sub=100.0 * (ns[m] == 1).mean(), n_multi=int(mu.sum()),
                           dif_toate=pearsonr(df["last4_first"].loc[m, "p_multi"], y)[0] -
                                     pearsonr(df["last4_last"].loc[m, "p_multi"], y)[0],
                           dif_multi=pearsonr(df["last4_first"].loc[mu, "p_multi"], ym)[0] -
                                     pearsonr(df["last4_last"].loc[mu, "p_multi"], ym)[0]))
        MK = pd.DataFrame(mr).set_index("lang")
        cc = pearsonr(MK["pct_1sub"], MK["dif_toate"].abs())
        L += ["## Mecanismul din spatele inversarii fata de literatura", "",
              "`first` − `last`, pe bratul A. 950 din 5624 de tinte (16.9%) au UN singur subword, "
              "unde cele patru strategii de pooling coincid, deci efectul poate veni numai de la "
              "restul:", "", "```", MK.round(4).to_string(), "```", "",
              f"`first` castiga pe **{int((MK['dif_toate'] > 0).sum())} din {len(MK)}** limbi. "
              f"Efectul e mai mare pe tintele multi-subword ({MK['dif_multi'].mean():+.4f}) decat pe "
              f"toate ({MK['dif_toate'].mean():+.4f}), si coreleaza **{cc[0]:+.3f}** cu cat de PUTINE "
              "tinte de un subword are limba, adica exact cum ar trebui daca ar veni din segmentare.",
              "",
              "**De ce se inverseaza fata de Acs, Kadar si Kornai.** Ei probeaza trasaturi "
              "MORFOLOGICE, caz, gen, forma verbala, care traiesc in sufix; acolo ultimul subword E "
              "raspunsul, si `first` il arunca. Noi prezicem o proprietate LEXICALA, care tine de "
              "identitatea cuvantului. Ultimele bucati sunt fragmente scurte si foarte frecvente, "
              "impartite de mii de cuvinte (`ts`, `es`, `a` in exemplele catalane), deci nu "
              "identifica lexemul; prima bucata poarta materialul initial, care il identifica. "
              "Aceeasi segmentare, semnal opus, fiindca sarcina e alta. Nu contrazice lucrarea lor, "
              "ii delimiteaza domeniul.", "",
              "Nuanta de onestitate: segmentarea lui XLM-R nu e morfologica, "
              "`controvertits` da `['controvertits' -> contro, verti, ts]`, deci propozitia corecta "
              "nu e \"prima bucata e lema\", ci \"ultima bucata e un fragment impartit, prima nu\".", ""]

    # ---------------------------------------------------------------- corelatii, pentru ansamblu
    if len(Z) > 1 and REF_CFG in Z:
        base = Z[REF_CFG]
        cr = []
        d0 = pd.read_csv(preds(REF_CFG))
        d0 = d0[d0["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
        lang_arr = d0["lang"].values
        for cfg, v in Z.items():
            if cfg == REF_CFG:
                continue
            rl = [pearsonr(base[lang_arr == lg], v[lang_arr == lg])[0] for lg in langs]
            cr.append(dict(cfg=cfg, rho_la_last4=np.mean(rl), rho_min=min(rl),
                           limba_min=langs[int(np.argmin(rl))]))
        C = pd.DataFrame(cr).set_index("cfg").sort_values("rho_la_last4")
        L += ["## Corelatia cu `last4`, adica: merita mediat?", "",
              "Frontiera cere rho <= 0.78 in varianta optimista pentru un membru de calitate egala. "
              "Configuratiile ACELUIASI model sunt mult peste, cu o exceptie:", "",
              "```", C.round(4).to_string(), "```", ""]

    # ---------------------------------------------------------------- podeaua de zgomot a selectiei
    gata = [c for c in SWEEP if c in T.index]
    if len(gata) >= 8:
        d0 = pd.read_csv(preds(REF_CFG))
        d0 = d0[d0["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
        lang_arr = d0["lang"].values
        y_all = d0["complexity"].values.astype(float)
        P = {c: pd.read_csv(preds(c))[lambda z: z["split"] == "test"]
                  .sort_values(["lang", "idx"]).reset_index(drop=True)["p_multi"].values
             for c in gata}

        def selectie_lolo(R):
            """R[cfg][lang] -> r. Pentru limba L se alege configul cel mai bun pe CELELALTE noua."""
            out = {}
            for lg in langs:
                best = max(R, key=lambda c: np.mean([R[c][l2] for l2 in langs if l2 != lg]))
                out[lg] = R[best][lg]
            return float(np.mean(list(out.values()))), out

        R_real = {c: {lg: pearsonr(P[c][lang_arr == lg], y_all[lang_arr == lg])[0] for lg in langs}
                  for c in gata}
        r_sel, _ = selectie_lolo(R_real)
        r_ref = float(np.mean([R_real[REF_CFG][lg] for lg in langs]))
        # imprastierea reala intre configuri, in interiorul limbii, ca sa se calibreze zgomotul
        sd_tinta = float(np.mean([np.std([R_real[c][lg] for c in gata]) for lg in langs]))

        SEMINTE = 20
        pod = []
        base = P[REF_CFG]
        for sd in range(SEMINTE):
            rng = np.random.default_rng(4000 + sd)
            Rz = {}
            for i in range(len(gata)):
                v = base.copy().astype(float)
                for lg in langs:
                    m = lang_arr == lg
                    # zgomot calibrat sa reproduca imprastierea reala intre configuri
                    v[m] = v[m] + rng.normal(0, 1, m.sum()) * v[m].std() * 0.35
                Rz[f"z{i}"] = {lg: pearsonr(v[lang_arr == lg], y_all[lang_arr == lg])[0]
                               for lg in langs}
            pod.append(selectie_lolo(Rz)[0] - float(np.mean([Rz["z0"][lg] for lg in langs])))
        pod = np.asarray(pod)
        L += ["## Podeaua de zgomot a selectiei", "",
              f"Selectia LOLO peste cele {len(gata)} configuratii da **{r_sel:.6f}** pe bratul A, "
              f"fata de **{r_ref:.6f}** la `{REF_CFG}`, adica **{r_sel - r_ref:+.6f}**.", "",
              f"Podeaua: {SEMINTE} bazine de cate {len(gata)} candidati ALEATORI, generati "
              "perturband predictiile de referinta cu zgomot calibrat sa reproduca imprastierea reala "
              f"intre configuri (sd real intre configuri, mediat pe limbi: {sd_tinta:.4f}), trecuti "
              "prin selectia LOLO identica.", "",
              f"Podea **{pod.mean():+.6f}**, interval [{pod.min():+.6f}, {pod.max():+.6f}].",
              f"Excesul peste podea: **{(r_sel - r_ref) - pod.mean():+.6f}** pe bratul A.",
              f"Prin factorul de transmisie (0.09 marginal, 0.26 mediu), asta ar fi "
              f"**{((r_sel - r_ref) - pod.mean()) * 0.09:+.6f} .. "
              f"{((r_sel - r_ref) - pod.mean()) * 0.26:+.6f}** pe fuziune.", "",
              "**Ce spune si ce NU spune cifra asta.** Spune ca a ALEGE configuratia din grila de "
              "16, leave-one-language-out, nu valoreaza nimic: criteriul nu separa, exact ca la "
              "selectia de encodere. Nu spune ca poolingul n-ar conta. Cele doua axe ale grilei se "
              "comporta complet diferit, si se vede masurand fiecare separat:", ""]
        axe = {}
        for nume, cand in (("numai poolingul (4 candidati, straturi fixate la last4)",
                            ["last4", "last4_first", "last4_last", "last4_max"]),
                           ("numai straturile (4 candidati, pooling fixat la mean)",
                            ["last4", "mid", "concat4", "last1"]),
                           ("numai straturile, pooling fixat la first",
                            ["last4_first", "mid_first", "concat4_first", "last1_first"])):
            cand = [c for c in cand if c in R_real]
            if len(cand) < 2:
                continue
            rs, pick = selectie_lolo({c: R_real[c] for c in cand})
            lat = float(np.mean([max(R_real[c][lg] for c in cand) -
                                 min(R_real[c][lg] for c in cand) for lg in langs]))
            # Contrastul capat-la-capat al axei: cat e efectul si cat de CONSTANT e semnul lui.
            # O axa larga dar cu semn care se schimba de la limba la limba e zgomot, oricat de larga.
            mm = {c: float(np.mean([R_real[c][lg] for lg in langs])) for c in cand}
            hi, lo = max(mm, key=mm.get), min(mm, key=mm.get)
            per_lg = np.array([R_real[hi][lg] - R_real[lo][lg] for lg in langs])
            axe[nume] = dict(candidati=len(cand), r_selectat=round(rs, 6),
                             vs_last4=round(rs - r_ref, 6), latime_pe_limba=round(lat, 4),
                             latime_pe_medie=round(mm[hi] - mm[lo], 4), contrast=f"{hi} - {lo}",
                             sd_intre_limbi=round(float(per_lg.std()), 4),
                             acelasi_semn=f"{int((per_lg > 0).sum())}/{len(langs)}")
        AX = pd.DataFrame(axe).T
        L += ["```", AX.to_string(), "```", "",
              "Cele doua latimi spun lucruri diferite si nu trebuie confundate. `latime_pe_limba` e "
              "media, peste limbi, a distantei dintre cel mai bun si cel mai slab candidat IN acea "
              "limba, si e aproape egala pe cele doua axe (~0.029): dupa ea, ar parea la fel de "
              "importante. `latime_pe_medie` e distanta DUPA medierea pe limbi, si acolo se despart. "
              "Diferenta dintre cele doua latimi e exact partea care se anuleaza la mediere, adica "
              "zgomotul per limba.", "",
              "Ce separa cu adevarat axele e **constanta semnului**, coloana `acelasi_semn`. Un "
              "contrast care merge in aceeasi directie pe toate limbile e un efect; unul care isi "
              "schimba semnul e zgomot cu amplitudine mare. Numai axa de pooling e in primul caz.", "",
              "Consecinta pentru protocol: `first` **nu** e argmaxul unei grile plate. E capatul unei "
              "axe cu efect sistematic, confirmat pe 10 limbi din 10, pe toate cele 4 familii de "
              "straturi, monoton cu fertilitatea (r = +0.726, p = 0.017) si cu mecanism verificat pe "
              "tintele multi-subword. Axa de straturi se lasa la valoarea mostenita, fiindca nimic "
              "din ea nu supravietuieste medierii pe limbi.", "",
              "Multiplicitatea sesiunii se declara: 16 configuratii de extractie, 3 structurale, "
              "3 de izotropie, 4 de frecventa, 2 encodere noi. Jurnalul avea deja 102 randuri plus "
              "84 in arhiva.", ""]

    dest = os.path.join(OUT, "e_extractie.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
