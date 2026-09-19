"""Semnalul C (surprisal) trecut prin FRONTIERA, ca poarta, inainte de a rula orice fuziune.

De ce exista. C e calculat de la inceput, langa B, in fiecare CSV de bake-off. Dar r-ul lui cu
eticheta e intre -0.065 si +0.094 dupa model, cu semnul schimbandu-se intre limbi, si pe baza acelei
cifre a fost lasat afara ("C nu intra", `fuse_ab` docstring). **Corelatia lui cu A si cu B n-a fost
masurata niciodata**, deci decizia s-a luat pe calitate, nu pe decorelare, iar sesiunea din 23 august
a stabilit ca ce leaga e decorelarea.

Poarta, si e o singura cifra. Pentru fuziunea adoptata F si un candidat C, ambele standardizate,
plafonul peste orice pondere u a amestecului `(1-u)*zF + u*zC` e corelatia multipla

    R_max = sqrt( (r_F^2 + r_C^2 - 2*r_F*r_C*rho) / (1 - rho^2) )

care se rescrie exact ca `R_max^2 = r_F^2 + partial^2 * (1 - r_F^2)`, unde `partial` e corelatia
partiala a lui C cu eticheta controland pe F. Deci conditia `R_max >= r_F + bara` devine

    |partial| >= bara_in_partial = sqrt( ((r_F+bara)^2 - r_F^2) / (1 - r_F^2) )

adica **0.1077 la r_F = 0.683849 si bara = 0.0045**. E aceeasi algebra ca in `analysis_frontiera_enc`,
scrisa pentru doi membri cu pondere in loc de k membri neponderati.

Doua lucruri pe care poarta NU le acopera, si de aia scriptul le raporteaza separat:

  1. `R_max` e cu u optim IN-SAMPLE, per limba. Procedura reala alege un singur u global, LOLO. Deci
     R_max e plafon, nu predictie, si `analysis_c_fuse.py` masoara ce ramane din el.
  2. Un plafon pe medie nu autorizeaza o procedura care alege LOLO daca semnul corelatiei partiale se
     schimba de la limba la limba: media ar fi mare si u ales ar fi zero. De aia se numara **semnele
     pe limba**, exact criteriul care a separat poolingul (10/10) de straturi (7/10) in `e_encoder2`.

Alinierea. `output/fusion_preds_lolo_adoptat_temp.csv` are `A` = zA si `B` = zB deja standardizate in
interiorul limbii, plus `p_fuz`. CSV-urile de bake-off n-au `idx`, il capata pozitional din
`bakeoff_trial.with_context`, care verifica rand cu rand `lang`, `token` si `complexity`.

Rulare:
  python analysis_c_frontiera.py
  python analysis_c_frontiera.py --dir bakeoff_test_Text --dir surprisal_test
"""
import argparse
import glob
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

FUZ = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
BARA = 0.0045          # castigul onest, dupa scaderea optimismului de selectie de +0.001937
UGRID = np.round(np.arange(-0.60, 0.6001, 0.005), 4)


def zscore(v):
    """Exact `fuse_ab.zscore`: standardizare in limba, nefinit -> 0, adica pe medie.

    Se importa semantica, nu functia, ca sa nu se traga `fuse_ab` (si prin el `bakeoff_trial`) doar
    pentru trei linii. Egalitatea cu originalul se verifica in `_check_zscore`.
    """
    v = np.asarray(v, float)
    m = np.isfinite(v)
    if m.sum() < 2 or np.std(v[m]) == 0:
        return np.zeros(len(v))
    z = np.zeros(len(v))
    z[m] = (v[m] - v[m].mean()) / v[m].std()
    return z


def _check_zscore():
    from fuse_ab import zscore as zs0
    rng = np.random.RandomState(0)
    v = rng.randn(50); v[3] = np.nan; v[7] = np.inf
    assert np.array_equal(zscore(v), zs0(v)), "zscore local difera de fuse_ab.zscore"


def r_of(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def partial(r_cy, r_fy, rho):
    """Corelatia partiala a lui C cu y, controland pe F."""
    den = np.sqrt(max(1e-12, (1 - r_fy ** 2) * (1 - rho ** 2)))
    return (r_cy - r_fy * rho) / den


def rmax_of(r_fy, r_cy, rho):
    """Corelatia multipla: plafonul peste ORICE u, in-sample."""
    num = r_fy ** 2 + r_cy ** 2 - 2 * r_fy * r_cy * rho
    return float(np.sqrt(max(0.0, num / max(1e-12, 1 - rho ** 2))))


def prag_partial(r_fy, bara=BARA):
    """|partial| minim ca plafonul sa depaseasca r_fy + bara."""
    t = r_fy + bara
    if t >= 1.0:
        return float("inf")
    return float(np.sqrt(max(0.0, (t ** 2 - r_fy ** 2) / (1 - r_fy ** 2))))


def prag_rc(r_fy, rho, bara=BARA):
    """(r_C minim pe ramura normala, r_C maxim pe ramura de supresor)."""
    p = prag_partial(r_fy, bara)
    d = p * np.sqrt(max(0.0, (1 - r_fy ** 2) * (1 - rho ** 2)))
    return r_fy * rho + d, r_fy * rho - d


def best_u(r_fy, r_cy, rho):
    """u care maximizeaza r al amestecului, pe grila. -> (u, r la acel u)."""
    num = (1 - UGRID) * r_fy + UGRID * r_cy
    den = np.sqrt((1 - UGRID) ** 2 + UGRID ** 2 + 2 * UGRID * (1 - UGRID) * rho)
    v = np.where(den > 1e-9, num / den, -np.inf)
    i = int(np.argmax(v))
    return float(UGRID[i]), float(v[i])


def load_c(dirs, n_astept=None):
    """{nume candidat: Series C indexata pe idx} din CSV-urile de bake-off.

    Fisierele PARTIALE se sar, si asta nu e o precautie teoretica: `measure` scrie rand cu rand cu
    flush, deci un CSV citit in timp ce rularea inca merge are un prefix de randuri. Un asemenea
    fisier nu crapa nimic, fiindca `reindex` pune NaN pe restul si `zscore` duce NaN in zero: candidatul
    iese pur si simplu aproape constant. In prima rulare asa a intrat `aya-expanse-8b-4bit` cu 255 din
    5624 de randuri si a raportat R_max 0.0558 si dR -0.628, cifre care arata a rezultat.
    """
    from bakeoff_trial import with_context
    out, partiale = {}, {}
    for d in dirs:
        for p in sorted(glob.glob(os.path.join(OUT, d, "*.csv"))):
            b = os.path.basename(p)
            if b.startswith("_"):
                continue                      # fisiere de control, nu modele
            df = pd.read_csv(p)
            if "C" not in df.columns:
                continue
            if n_astept is not None and len(df) < n_astept:
                partiale[b[:-4]] = (len(df), n_astept)
                continue
            df = with_context(df, "test")
            out[b[:-4]] = df.set_index("idx")["C"]
    for k, (a, b2) in partiale.items():
        print(f"  [!] {k}: {a} din {b2} randuri, fisier PARTIAL, se sare")
    return out


def derivati(cser, baza):
    """Candidati derivati din C-urile brute, adaugati la dictionar. -> dict imbogatit.

    `medie`   media celor `baza` C standardizate PE LIMBA. Un ansamblu de surprisal-uri, deci exact
              obiectul pe care frontiera din `analysis_frontiera_enc` il descrie: castigul lui e
              reducerea de varianta intre membri.
    `dezacord` abaterea standard intre aceleasi C standardizate. E o cantitate de ordin DOI, deci alt
              obiect decat oricare membru, si e varianta ADITIVA a dezacordului. Varianta-pondere,
              `fuse_ab --h dezacord`, e moarta cu a = 0 pe 10/10 limbi si pe zgomot; asta nu e ea.

    Standardizarea e per limba, deci se face in `tabel`, unde limba e cunoscuta. Aici se pastreaza
    doar lista membrilor.
    """
    return {"medie": baza, "dezacord": baza}


def tabel(fz, cser, nume, membri=None):
    """Un rand per limba pentru un candidat. `membri` != None inseamna candidat derivat."""
    rows = []
    for lg, g in fz.groupby("lang", sort=True):
        y = g["y"].values.astype(float)
        zA, zB, pf = g["A"].values, g["B"].values, g["p_fuz"].values
        if membri is None:
            raw = cser[nume].reindex(g["idx"].values).values.astype(float)
            nfin = int((~np.isfinite(raw)).sum())
            zC = zscore(raw)
            r_fin = r_of(raw, y)                     # r pe randurile cu semnal, ca in e_bakeoff_test
        else:
            Z = np.column_stack([zscore(cser[m].reindex(g["idx"].values).values.astype(float))
                                 for m in membri])
            nfin = int(sum((~np.isfinite(cser[m].reindex(g["idx"].values).values.astype(float))).sum()
                           for m in membri))
            zC = zscore(Z.mean(1) if nume == "medie" else Z.std(1))
            r_fin = float("nan")
        r_fy, r_cy = r_of(pf, y), r_of(zC, y)
        rho = r_of(zC, pf)
        pc = partial(r_cy, r_fy, rho)
        rm = rmax_of(r_fy, r_cy, rho)
        u, ru = best_u(r_fy, r_cy, rho)
        lo, hi = prag_rc(r_fy, rho)
        rows.append(dict(lang=lg, n=len(g), n_nefinit=nfin, r_C=r_cy, r_C_finite=r_fin,
                         rho_A=r_of(zC, zA), rho_B=r_of(zC, zB), rho_F=rho, r_F=r_fy,
                         partial=pc, prag=prag_partial(r_fy), R_max=rm, dR=rm - r_fy,
                         u_opt=u, rC_prag_sus=lo, rC_prag_jos=hi))
    return pd.DataFrame(rows).set_index("lang")


def verdict(t):
    """(text de verdict, castig plafon pe medie, semne consistente)."""
    dR = float(t["dR"].mean())
    p = t["partial"].values
    trec = int((np.abs(p) >= t["prag"].values).sum())
    poz, neg = int((p > 0).sum()), int((p < 0).sum())
    semn = max(poz, neg)
    ok_semn = semn >= 8
    ok_bara = dR >= BARA
    if ok_bara and ok_semn:
        v = "TRECE plafonul si semnul e consistent"
    elif ok_bara:
        v = f"trece plafonul dar SEMNUL SE SCHIMBA ({poz} pozitive, {neg} negative), deci u ales LOLO va fi ~0"
    else:
        v = "NU trece plafonul"
    return v, dR, trec, semn, ok_semn


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", action="append", default=None,
                    help="director de CSV-uri de bake-off, relativ la output/ (implicit "
                         "bakeoff_test_Text)")
    ap.add_argument("--c-csv", action="append", default=None, metavar="NUME=CALE",
                    help="candidat dintr-un CSV cu `lang, idx, C`, nu dintr-un bake-off. E calea "
                         "prin care intra candidatii care nu sunt iesirea unui LLM.")
    ap.add_argument("--exclude", action="append", default=None,
                    help="model care NU poate furniza C (pica poarta din analysis_c_sanatate.py). "
                         "Se scoate si din candidatii proprii, si din cei derivati.")
    ap.add_argument("--out", default="e_c_frontiera.md")
    a = ap.parse_args(argv)
    dirs = a.dir or ["bakeoff_test_Text"]

    _check_zscore()
    fz = pd.read_csv(FUZ)
    cser = load_c(dirs, n_astept=len(fz)) if dirs else {}
    for spec in (a.c_csv or []):
        nume, cale = spec.split("=", 1)
        cser[nume] = pd.read_csv(cale).set_index("idx")["C"]
    if not cser:
        sys.exit(f"niciun CSV cu coloana C in {dirs}")
    exc = set(a.exclude or [])
    lipsa = exc - set(cser)
    if lipsa:
        sys.exit(f"--exclude numeste modele care nu sunt in {dirs}: {sorted(lipsa)}")
    baza = sorted(set(cser) - exc)
    if not baza:
        sys.exit("toate modelele au fost excluse")
    r_F = float(fz.groupby("lang").apply(lambda g: r_of(g["p_fuz"], g["y"]),
                                         include_groups=False).mean())

    L = ["# Semnalul C prin frontiera, ca poarta", "",
         (f"**Excluse ca degenerate pe text brut, prin `analysis_c_sanatate.py`: "
          f"{sorted(exc)}.**\n" if exc else "") +
         f"Generat de `analysis_c_frontiera.py`, directoare {dirs}. Splitul e test, "
         f"n = {len(fz)}. Fuziunea de referinta e `{os.path.basename(FUZ)}`, "
         f"r mediu pe limbi **{r_F:.6f}**.", "",
         "## Poarta, scrisa inainte de a citi vreo cifra a candidatilor", "",
         f"Bara e +{BARA:.4f}. Din `R_max^2 = r_F^2 + partial^2 * (1 - r_F^2)`, conditia "
         f"`R_max >= r_F + bara` cere, la r_F = {r_F:.6f}:", "",
         f"> **|corelatia partiala a lui C cu y, controland pe fuziune| >= "
         f"{prag_partial(r_F):.4f}**", "",
         "Echivalent, ce r_C ii trebuie unui candidat in functie de cat de corelat e cu fuziunea. "
         "Ramura de jos e cea de SUPRESOR: un semnal care coreleaza cu fuziunea dar NU cu eticheta "
         "corecteaza scazandu-se.", "", "```",
         "rho cu fuziunea   r_C minim (normala)   r_C maxim (supresor)"]
    for rho in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50):
        lo, hi = prag_rc(r_F, rho)
        L.append(f"{rho:<17.2f} {lo:+.4f}{'':<14} {hi:+.4f}")
    L += ["```", "",
          "Praguri pentru alte ambitii, ca sa nu se citeasca doar bara:", "", "```",
          "castig tinta   |partial| necesar"]
    for b in (0.0022, BARA, 0.0089):
        L.append(f"{b:+.4f}{'':<8} {prag_partial(r_F, b):.4f}")
    L += ["```", ""]

    # Candidatii din CSV nu intra in cei DERIVATI: media si dezacordul au sens intre marimi de
    # acelasi fel, adica intre surprisal-uri, nu intre un surprisal si o densitate de vecinatate.
    din_csv = [spec.split("=", 1)[0] for spec in (a.c_csv or [])]
    baza = [b for b in baza if b not in din_csv]
    cand = [(n, None) for n in baza + din_csv]
    if len(baza) >= 2:
        cand += [("medie", baza), ("dezacord", baza)]

    rez = []
    L += ["## Candidati, fiecare cu tabelul lui pe limba", ""]
    for nume, membri in cand:
        t = tabel(fz, cser, nume, membri)
        v, dR, trec, semn, ok_semn = verdict(t)
        show = t[["n", "n_nefinit", "r_C", "rho_A", "rho_B", "rho_F", "r_F", "partial",
                  "prag", "R_max", "dR", "u_opt"]]
        L += [f"### `{nume}`" + ("" if membri is None else f"  (derivat din {len(membri)} membri)"),
              "", "```", show.round(4).to_string(), "```", "",
              f"r_C mediu **{t['r_C'].mean():+.4f}**, rho cu fuziunea **{t['rho_F'].mean():+.4f}**, "
              f"rho cu A **{t['rho_A'].mean():+.4f}**, rho cu B **{t['rho_B'].mean():+.4f}**.",
              f"Corelatie partiala medie **{t['partial'].mean():+.4f}**, prag "
              f"**{t['prag'].mean():.4f}**; trece pe **{trec} limbi din {len(t)}**, "
              f"semn consistent pe **{semn}/{len(t)}**.",
              f"Plafon peste orice u, mediat pe limbi: **{t['R_max'].mean():.6f}**, adica "
              f"**{dR:+.6f}** peste fuziune.",
              f"**Verdict: {v}.**", "",
              "Cifra de mai sus e un PLAFON cu u optim in-sample per limba. Ce ramane dupa alegerea "
              "LOLO a unui singur u global se masoara in `analysis_c_fuse.py`.", ""]
        rez.append(dict(candidat=nume, r_C=t["r_C"].mean(), rho_F=t["rho_F"].mean(),
                        partial=t["partial"].mean(), prag=t["prag"].mean(),
                        R_max=t["R_max"].mean(), dR=dR, limbi_trec=trec,
                        semn=semn, verdict=v))
        t.to_csv(os.path.join(OUT, f"c_frontiera_{nume}.csv"))

    s = pd.DataFrame(rez).set_index("candidat").sort_values("dR", ascending=False)
    L += ["## Sinteza, ordonata dupa plafon", "", "```",
          s[["r_C", "rho_F", "partial", "prag", "R_max", "dR", "limbi_trec", "semn"]]
          .round(6).to_string(), "```", "",
          f"Bara e +{BARA:.4f}. Coloana `dR` e plafonul, nu castigul: cu u optim in-sample per limba. "
          "Coloana `semn` e numarul de limbi pe care corelatia partiala are semnul majoritar; sub 8 "
          "din 10, selectia LOLO a unui u global il duce la zero indiferent ce spune media.", ""]

    dest = os.path.join(OUT, a.out)
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
