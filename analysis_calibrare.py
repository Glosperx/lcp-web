"""E.15. Calibrare monotona a lui B inainte de fuziune, cu podeaua de zgomot.

Intrebarea. `B` e UN anume functional liniar al distributiei, cel cu notele 1..5 EGAL spatiate.
Doua alternative au fost deja masurate si stau la capete opuse:

  - unirea cifrelor vecine (`prio_K`), adica 15 citiri monotone in trepte, aleasa LOLO: B urca de la
    +0.659202 la +0.661254, si fuziunea cu +0.001682;
  - citirea liniara NECONSTRANSA a celor cinci probabilitati, cu 5 coeficienti alesi LOLO: B COBOARA
    la +0.6407, desi plafonul ei in-sample e +0.6760 (`output/e_prioritate.md` §3b).

Deci scorul LOLO are un maxim undeva sub 15 candidati si se prabuseste pana la 5 parametri liberi.
Intre cele doua nu s-a masurat nimic, iar acolo se afla intrebarea: exista o regularizare intermediara
care sa scoata mai mult decat treptele?

Ce e familia, si de ce nu e o spline. Pearson e invariant la orice transformare afina cu panta
pozitiva a vectorului de valori `v`, fiindca randurile lui P insumeaza 1. Deci `v` se normalizeaza cu
v0 = 0 si v4 = 1, si raman exact TREI parametri liberi, cu constrangerea de monotonie. Cu cinci atomi,
o spline monotona cu 3-4 noduri nu are unde sa adauge ceva peste o grila pe simplexul cresterilor, iar
grila are avantajul ca numarul de candidati se declara exact. Familia de colaps e o submultime a
aceleiasi familii monotone, dar NU cade pe grila discreta (mediile de bloc dau numere ca 3/7), deci
cele doua se raporteaza separat.

Podeaua de zgomot e chiar punctul experimentului, nu un accesoriu. Un bazin de 455 de candidati
castiga ceva si daca toti candidatii sunt zgomot pur. Pentru fiecare marime de familie se construieste
un bazin ALEATOR de aceeasi marime, care contine si el citirea neutra, se trece prin selectia LOLO
IDENTICA, cu mai multe seminte, si se raporteaza cat da norocul singur. Un castig sub podea nu e
castig.

Asteptare declarata INAINTE de rulare, si e negativa. Dilutia masurata de la B la fuziune e intre
0.55 si 0.82, deci ca sa treaca bara de +0.0045 pe fuziune familia ar trebui sa dea +0.0055..+0.0082
pe B, adica de trei ori cat da colapsul si peste tot ce s-a masurat pe axa asta.

Controlul care valideaza codul, si a trecut inainte de a se scrie orice cifra: `--mod calibrare
--pas 0`, adica cele 15 partitii de colaps scrise ca vectori, reproduce `--mod colaps` pe toate zece
limbile la 1.9e-09, si alege aceeasi partitie 1|23|45 unanim.

Rulare:
  python analysis_calibrare.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_calibrare.md")
SYS_DIST = os.path.join(OUT, "dist", "gemma4-12b-4bit_test.csv")
SEMINTE = 10          # bazine aleatoare per marime de familie
FAMILII = [("colaps, 15 trepte", 0), ("grila 1/4", 4), ("grila 1/8", 8), ("grila 1/12", 12)]

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def r_family(PL, vlist):
    """(r mediu, r per limba, esantioane bootstrap, tabelul de parametri) pentru o familie de citiri.

    Trece prin `make_fs_runs.pick_params_v`, adica prin exact selectia care scrie fisierele de
    bake-off, nu printr-o reimplementare. Altfel cifra de aici si cea a fuziunii ar putea diverge.
    """
    import analysis_dist as ad
    from make_fs_runs import pick_params_v, b_of
    params, tab = pick_params_v(PL, vlist, ad.T_GRID_EXT)
    rs, boots = [], []
    for lg in sorted(PL):
        T, v = params[lg]
        b = b_of(PL[lg]["Ps"], T, vals=v)
        rs.append(ad.r_of(b, PL[lg]["y"]))
        boots.append(ad.boot_one(PL[lg]["y"], b, PL[lg]["ctx"])["boot"])
    return float(np.mean(rs)), rs, boots, tab


def bazin_aleator(n, rng):
    """`n` citiri monotone aleatoare de pe simplexul cresterilor, dintre care UNA e cea neutra.

    Neutra e in bazin fiindca e si in familiile reale: fara ea selectia n-ar avea voie sa nu schimbe
    nimic, si comparatia n-ar mai fi like-for-like. Cresterile vin din Dirichlet(1,1,1,1), adica
    uniform pe simplex, deci bazinul are aceeasi geometrie cu familia reala, doar ca punctele nu sunt
    pe grila.
    """
    out = [np.arange(5.0) / 4.0]
    d = rng.dirichlet(np.ones(4), size=max(0, n - 1))
    for row in d:
        out.append(np.concatenate([[0.0], np.cumsum(row)]))
    return out


def main():
    import analysis_dist as ad
    from make_fs_runs import load_srcs, mono_grid, colaps_vals, b_of

    PL, names = load_srcs([SYS_DIST])
    if len(names) != 2:
        raise SystemExit(f"se asteptau cele doua prompturi ale sistemului, s-au gasit {names}")
    langs = sorted(PL)

    # linia de baza: citirea neutra, cu T ales LOLO. Trebuie sa dea B-ul sistemului.
    neutru = [np.arange(5.0) / 4.0]
    r0, rs0, B0, _ = r_family(PL, neutru)
    b_sis = float(pd.read_csv(os.path.join(OUT, "fusion_lolo_adoptat_temp.csv"))["r_B_raw"].mean())

    emit("# E.15. Calibrare monotona a lui B, cu podeaua de zgomot\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_calibrare.py`. "
         f"{sum(PL[l]['n'] for l in langs)} randuri de test, {len(langs)} limbi, media pe limbi. "
         "Zero inferenta: aceleasi distributii de pe disc, alta citire a lor.\n",
         __doc__.split("Rulare:")[0].split("\n", 2)[2].strip() + "\n",
         "## 0. Linia de baza se reproduce\n",
         f"Citirea neutra, cu T ales LOLO prin aceeasi conducta: **{r0:.6f}**. "
         f"Semnalul B al sistemului, citit din `output/fusion_lolo_adoptat_temp.csv`: "
         f"**{b_sis:.6f}**. Abatere: **{abs(r0 - b_sis):.2e}**.\n")
    if abs(r0 - b_sis) > 1e-6:
        emit("**PICAT.** Familia cu un singur candidat nu reproduce B-ul sistemului. "
             "Restul raportului nu se scrie.\n")
        raise SystemExit("linia de baza nu se reproduce")
    print(f"[cal] neutru {r0:.6f} fata de B sistem {b_sis:.6f}", flush=True)

    # --- familiile reale
    emit("## 1. Familiile reale\n",
         "`margine` e criteriul castigatorului minus criteriul citirii neutre, mediat pe limbi; "
         "`latime` e cat separa criteriul cel mai bun candidat de cel mai slab. O margine mica pe un "
         "criteriu lat e tiparul pe care l-a avut `distTpp`, adica alegere pe zgomot.\n",
         "| familie | candidati | r mediu pe B | fata de neutru | CI 95% pereche | P(>0) | "
         "limbi cu citire neutra | margine medie | latime medie |",
         "|---|---|---|---|---|---|---|---|---|")
    REAL = {}
    for nume, pas in FAMILII:
        vlist = colaps_vals() if pas == 0 else mono_grid(pas)
        t0 = time.time()
        r, rs, Bk, tab = r_family(PL, vlist)
        dm, lo, hi, pp = ad.mean_diff_ci(Bk, B0)
        REAL[nume] = dict(pas=pas, n=len(vlist), r=r, rs=rs, boots=Bk, dm=dm, lo=lo, hi=hi, pp=pp,
                          tab=tab)
        emit(f"| {nume} | {len(vlist)} | **{r:.6f}** | {dm:+.6f} | [{lo:+.6f}, {hi:+.6f}] | {pp:.1%} "
             f"| {int(tab['neutru'].sum())}/10 | {tab['margine'].mean():+.5f} | "
             f"{tab['crit_lat'].mean():.5f} |")
        print(f"[cal] {nume:20s} n={len(vlist):4d}  r={r:.6f}  d={dm:+.6f}  "
              f"[{lo:+.6f},{hi:+.6f}]  {time.time()-t0:.0f}s", flush=True)
    emit("")

    # --- citirile alese, per limba
    emit("### Ce citire s-a ales, per limba\n",
         "| familie | " + " | ".join(langs) + " |", "|---|" + "---|" * len(langs))
    for nume in REAL:
        tab = REAL[nume]["tab"].set_index("lang")
        emit(f"| {nume} | " + " | ".join(
            "neutru" if bool(tab.loc[l, "neutru"]) else
            "/".join(f"{float(x):.2f}"[1:] if float(x) < 1 else "1" for x in
                     tab.loc[l, "partitie"].split("/")) for l in langs) + " |")
    emit("")

    # --- podeaua de zgomot
    emit("## 2. Podeaua de zgomot\n",
         f"Pentru fiecare marime de familie, {SEMINTE} bazine ALEATOARE de aceeasi marime, fiecare "
         "continand si citirea neutra, trecute prin selectia LOLO identica. `podea` e castigul mediu "
         "peste cele "f"{SEMINTE} de seminte, adica **cat da norocul singur** la marimea aia de bazin. "
         "`exces` e castigul real minus podeaua, si e singura coloana care spune ceva.\n",
         "| familie | candidati | castig real | podea de zgomot | interval al podelei | exces |",
         "|---|---|---|---|---|---|")
    for nume in REAL:
        n = REAL[nume]["n"]
        g = []
        for sd in range(SEMINTE):
            rng = np.random.default_rng(1000 + sd)
            rz, _, _, _ = r_family(PL, bazin_aleator(n, rng))
            g.append(rz - r0)
        g = np.asarray(g)
        REAL[nume]["podea"] = float(g.mean())
        REAL[nume]["exces"] = REAL[nume]["dm"] - float(g.mean())
        emit(f"| {nume} | {n} | {REAL[nume]['dm']:+.6f} | **{g.mean():+.6f}** | "
             f"[{g.min():+.6f}, {g.max():+.6f}] | **{REAL[nume]['exces']:+.6f}** |")
        print(f"[cal] podea {nume:20s} n={n:4d}  {g.mean():+.6f}  exces {REAL[nume]['exces']:+.6f}",
              flush=True)
    emit("")

    # --- verdict, dedus din cifre
    best = max(REAL, key=lambda k: REAL[k]["exces"])
    R = REAL[best]
    # Dilutia de la B la fuziune, masurata pe configuratiile deja rulate, nu presupusa.
    DIL = [("prio_K", 0.002052, 0.001682), ("FS3", 0.005247, 0.002880), ("FS3K", 0.007259, 0.004642)]
    lo_d = min(f / b for _, b, f in DIL)
    hi_d = max(f / b for _, b, f in DIL)
    prev_lo, prev_hi = R["exces"] * lo_d, R["exces"] * hi_d
    emit("## Verdict\n",
         f"Cel mai mare exces peste podea il da **{best}**, cu {R['n']} candidati: castig real "
         f"{R['dm']:+.6f} pe B, podea {R['podea']:+.6f}, exces **{R['exces']:+.6f}**.\n",
         f"Dilutia de la B la fuziune, masurata pe cele trei configuratii deja rulate cap la cap "
         f"({', '.join(f'`{k}` {f/b:.2f}' for k, b, f in DIL)}), e intre {lo_d:.2f} si {hi_d:.2f}. "
         f"Deci excesul de mai sus s-ar traduce in **{prev_lo:+.6f} .. {prev_hi:+.6f}** pe fuziune.\n",
         ("**Bate bara de +0.0045.** Merita dus prin fuziune cap la cap."
          if prev_lo >= 0.0045 else
          f"**NU bate bara de +0.0045**, nici la capatul favorabil al dilutiei ({prev_hi:+.6f}). "
          "Asteptarea declarata inainte de rulare era chiar asta, si se confirma. Parghia se inchide "
          "ca sursa de castig, dar cifra ramane utila ca argument: familia monotona generala, cu de "
          f"pana la {max(R2['n'] for R2 in REAL.values())} de candidati, nu scoate mai mult decat "
          "cele 15 trepte, deci spatierea nu mai are ce da.") + "\n")
    print(f"[cal] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
