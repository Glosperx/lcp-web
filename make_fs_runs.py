"""Scrie CSV-uri de bake-off pe test cu semnalul B citit din MAI MULTE surse de distributii.

De ce un fisier nou si nu un flag in `make_bt_runs.py`. Acolo `B` e mereu media a DOUA distributii,
`p1` si `p2` din acelasi fisier, si toata selectia (`analysis_dist.per_lang`, `b_build`, `_r_cube`)
e scrisa pe cele doua nume. Configuratia few-shot are UN singur prompt, iar ansamblul cu ea are TREI:
few-shot plus cele doua prompturi ale sistemului, care sunt deja pe disc si nu se remasoara. A
generaliza `make_bt_runs` ar fi cerut atins fiecare loc din el prin care trece o cifra publicata.

Aici selectia e rescrisa in forma generala, pe o LISTA de distributii, iar increderea nu vine din
citirea codului: **controlul** e ca pe cele doua surse ale sistemului iese
`output/bakeoff_test_Text/gemma4-12b-4bit.csv` octet cu octet, adica exact directorul din care se
citeste cifra adoptata 0.683849. Daca reimplementarea s-ar fi abatut de la protocolul din
`make_bt_runs`, controlul ala cade.

Modurile, aceleasi doua din `make_bt_runs` care conteaza aici:

  `temperatura`   `B = media_j E(p_j^(1/T))`, cu T ales LOLO pe grila extinsa. La doua surse si
                  `w = 0.5` e chiar formula sistemului.
  `colaps`        acelasi lucru, plus partitia in blocuri contigue a celor cinci cifre, aleasa LOLO
                  dintre cele 15 candidate din `make_bt_runs.COLAPS`. Fiecare bloc primeste ca
                  valoare media notelor lui, deci `B` rams o citire liniara MONOTONA, doar cu alta
                  spatiere a nivelurilor.

Amandoi parametrii se aleg LOLO, adica pe celelalte noua limbi, si in ordinea prespecificata din
`make_bt_runs.pick_params`: intai T la partitia neutra, apoi partitia cu T fixat. Criteriul partitiei
foloseste, pentru fiecare limba de potrivire l', temperatura lui l' aleasa excluzand si L si l' - al
doilea nivel din `fuse_ab.fit_choice`. Nu se face un argmax pe cele 15 x 16 perechi.

`C` si `sec` se copiaza VERBATIM din `--base`, nu se recalculeaza: surprisal-ul nu depinde de prompt,
deci a-l remasura ar fi plata dubla pentru acelasi numar. Consecinta de citit in fisier: `sec` rams
timpul rularii sistemului, nu al rularii few-shot, iar timpul few-shot sta in
`output/promptlab_test/gemma4-12b-4bit.csv`. Nimic din aval nu citeste `sec`.

Tabelul de parametri se scrie LANGA director, ca in `make_bt_runs`: `bakeoff_trial.load_runs` ia
fiecare `*.csv` din director ca pe un model, deci un fisier in plus acolo ar intra tacut in bazinul de
candidati al lui `pick_model`.

Rulare:
  python make_fs_runs.py --dir bakeoff_test_CTRL --src output/dist/gemma4-12b-4bit_test.csv
      # CONTROL: trebuie sa iasa identic la octet cu output/bakeoff_test_Text/
  python make_fs_runs.py --dir bakeoff_test_FS  --src output/dist/fewshot_gemma4-12b-4bit_test.csv
  python make_fs_runs.py --dir bakeoff_test_FSK --mod colaps \
      --src output/dist/fewshot_gemma4-12b-4bit_test.csv
  python make_fs_runs.py --dir bakeoff_test_FS3 \
      --src output/dist/fewshot_gemma4-12b-4bit_test.csv \
      --src output/dist/gemma4-12b-4bit_test.csv
"""
import argparse
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
SRC_DIR = os.path.join(OUT, "bakeoff_test")
MODEL = "gemma4-12b-4bit"
BASE = os.path.join(OUT, "dist", f"{MODEL}_test.csv")
MODS = ("temperatura", "colaps", "calibrare")


def prompt_cols(df):
    """Sloturile de prompt prezente si NEVIDE intr-un CSV de distributii, in ordine.

    Un fisier scris de `bakeoff_trial` are mereu doua sloturi. Unul scris de `prompt_lab` pentru o
    varianta cu un singur soft-read are slotul 2 gol pe toate randurile, si atunci sursa contribuie
    UN prompt, nu doi. Se citeste din date, nu din numele fisierului: un slot pe jumatate gol ar fi o
    rulare intrerupta si trebuie sa crape, nu sa fie tacut mediat cu jumatati de coloana.
    """
    out = []
    for j in (1, 2):
        cols = [f"p{j}_{k}" for k in "12345"]
        if not all(c in df.columns for c in cols):
            continue
        ok = np.isfinite(df[cols].values.astype(float)).all(axis=1)
        if ok.all():
            out.append(cols)
        elif ok.any():
            raise SystemExit(f"slotul p{j}_* e plin pe {int(ok.sum())}/{len(df)} randuri. O rulare "
                             "intrerupta nu se mediaza pe jumatati de coloana.")
    if not out:
        raise SystemExit("CSV-ul n-are niciun slot p1_*/p2_* plin. E de dinainte de `rate_parts`.")
    return out


def load_srcs(paths):
    """({limba: dict(Ps, y, ctx, n)}, numele sursei per prompt).

    Randurile si `idx` se recupereaza exact ca in `analysis_dist.load()`: `with_context` face joinul
    POZITIONAL cu `load_mlsp("test")`, verificand limba, tinta si complexitatea rand cu rand, iar apoi
    se face inner join cu predictiile sistemului pe `idx`, cu cerinta ca toate randurile sistemului sa
    supravietuiasca. Deci multimea de randuri pe care se aleg parametrii e aceeasi cu a sistemului, si
    controlul de octet are voie sa fie exact.
    """
    from bakeoff_trial import with_context
    import analysis_dist as ad
    sysp = pd.read_csv(ad.SYS_PREDS)
    m = sysp.copy()
    names = []
    for p in paths:
        d = with_context(pd.read_csv(p), "test")
        slots = prompt_cols(d)
        tag = os.path.basename(p)[:-len(".csv")]
        ren, off = {}, len(names)
        for j, cols in enumerate(slots):
            for k, c in zip("12345", cols):
                ren[c] = f"q{off + j}_{k}"
            names.append(f"{tag}:{cols[0][:2]}")
        d = d.rename(columns=ren)
        m = m.merge(d[["idx"] + list(ren.values())], on="idx", how="inner")
        if len(m) != len(sysp):
            raise SystemExit(f"{p}: joinul pe idx a pastrat {len(m)} din {len(sysp)} randuri ale "
                             "sistemului")
    out = {}
    for lg, g in m.groupby("lang", sort=True):
        Ps = [g[[f"q{i}_{k}" for k in "12345"]].values.astype(float) for i in range(len(names))]
        out[lg] = dict(Ps=Ps, y=g["y"].values.astype(float), ctx=g["ctx"].values, n=len(g))
    return out, names


def b_of(Ps, T, bl=None, vals=None):
    """Semnalul B: media peste prompturi a valorii asteptate, la temperatura T.

    `T` e un scalar, adica aceeasi temperatura pentru toate prompturile, sau o lista de lungimea lui
    `Ps`, adica cate una per prompt. Scalarul e calea implicita si e cea prin care trece controlul de
    octet, deci ramura cu lista nu poate atinge nicio cifra deja produsa.

    UN SINGUR loc unde se scrie aritmetica, chemat si de criteriul de selectie si de scrierea
    fisierului, ca sa nu se poata intampla ca parametrul sa fie ales pe o formula si aplicat pe alta.
    Aceeasi regula ca in `make_bt_runs.b_build`, si aceeasi aritmetica: la doua prompturi si partitie
    neutra iese chiar `0.5*(E(p1^(1/T)) + E(p2^(1/T)))`, adica formula sistemului.

    `bl` e o partitie a celor cinci cifre in blocuri contigue. Fiecare bloc primeste ca valoare media
    notelor lui, deci nivelurile se respatiaza, dar ordinea lor nu se poate schimba. Aceeasi partitie
    pentru toate prompturile.
    """
    import analysis_dist as ad
    Ts = [float(T)] * len(Ps) if np.isscalar(T) else [float(t) for t in T]
    if len(Ts) != len(Ps):
        raise SystemExit(f"{len(Ts)} temperaturi pentru {len(Ps)} prompturi")
    if vals is not None:
        # Citire MONOTONA generala. Pearson e invariant la orice transformare afina cu panta pozitiva
        # a lui `vals`, fiindca randurile lui P insumeaza 1, deci `vals` se normalizeaza cu v0 = 0 si
        # v4 = 1 si raman TREI parametri liberi. Familia de colaps e o submultime a aceleiasi familii
        # monotone (blocurile dau paliere cu egalitati), dar NU cade pe grila discreta de aici, fiindca
        # mediile de bloc dau numere ca 3/7. De aceea cele doua familii se raporteaza separat.
        if bl is not None:
            raise SystemExit("b_of: `bl` si `vals` se exclud, sunt doua parametrizari ale aceluiasi lucru")
        w = np.asarray(vals, float)
        if w.shape != (5,) or np.any(np.diff(w) < -1e-12):
            raise SystemExit(f"vals trebuie sa fie 5 valori nedescrescatoare, primit {vals!r}")
        return np.mean([ad.temper(P, t) @ w for P, t in zip(Ps, Ts)], axis=0)
    if bl is None:
        return np.mean([ad.expected(ad.temper(P, t)) for P, t in zip(Ps, Ts)], axis=0)
    v = np.array([np.mean([i + 1 for i in b]) for b in bl], float)
    E = []
    for P, t in zip(Ps, Ts):
        Q = ad.temper(P, t)
        E.append(np.column_stack([Q[:, b].sum(axis=1) for b in bl]) @ v)
    return (np.mean(E, axis=0) - 1.0) / 4.0


def _r_cube(PL, t_grid, cols):
    """{limba: matrice (len(t_grid), len(cols))} cu r al lui B(limba, T, partitie).

    `cols` e lista de partitii; la modul `temperatura` e `[None]`, adica o singura coloana.
    """
    import analysis_dist as ad
    out = {}
    for lg, D in PL.items():
        M = np.empty((len(t_grid), len(cols)))
        for i, T in enumerate(t_grid):
            for j, bl in enumerate(cols):
                M[i, j] = ad.r_of(b_of(D["Ps"], T, bl), D["y"])
        out[lg] = M
    return out


def _argmax_T(R, langs, jb, exclude):
    """Indexul lui T ales pe limbile din `langs` fara cele din `exclude`, la coloana `jb`.
    Aceeasi forma cu `make_bt_runs._argmax_T` si cu `analysis_dist.temp_pick`."""
    keep = [l for l in langs if l not in exclude]
    crit = np.mean([R[l][:, jb] for l in keep], axis=0)
    return int(np.argmax(crit)), crit


def mono_grid(pas):
    """Toti vectorii monotoni de 5 valori cu v0 = 0, v4 = 1 si cresteri multipli de 1/`pas`.

    Sunt `C(pas+3, 3)` candidati: 35 la pas 4, 165 la pas 8, 455 la pas 12. `pas` trebuie divizibil
    cu 4, altfel spatierea EGALA (0, 1/4, 1/2, 3/4, 1), adica citirea publicata, n-ar fi in grila si
    selectia n-ar putea sa nu schimbe nimic. Punctul neutru in grila e conditia care face din
    experimentul asta un test, nu o cautare.
    """
    import itertools as it
    if int(pas) % 4:
        raise SystemExit(f"pas={pas}: trebuie divizibil cu 4, ca spatierea egala sa fie in grila")
    m = int(pas)
    out = []
    for d in it.product(range(m + 1), repeat=3):
        if sum(d) <= m:
            c = np.cumsum([0] + list(d) + [m - sum(d)]) / m
            out.append(np.asarray(c, float))
    return out


def colaps_vals():
    """Cele 15 partitii `COLAPS`, scrise ca vectori de valori normalizati, pentru comparatie
    like-for-like cu grila monotona. Media de bloc, adusa la v0 = 0 si v4 = 1."""
    from make_bt_runs import COLAPS
    out = []
    for bl in COLAPS:
        v = np.array([np.mean([i + 1 for i in b]) for b in bl], float)
        w = np.concatenate([[v[j]] * len(b) for j, b in enumerate(bl)])
        out.append((w - w[0]) / (w[-1] - w[0]))
    return out


def pick_params_v(PL, vlist, t_grid):
    """({limba: (T, vals)}, tabelul de diagnostic), pentru o familie de citiri monotone.

    Oglindeste `pick_params` la nivel de STRUCTURA, nu doar de rezultat: intai T la citirea neutra,
    apoi citirea cu T fixat, iar criteriul unei citiri foloseste, pentru fiecare limba de potrivire
    l', temperatura lui l' aleasa excluzand si L si l'. Al doilea nivel din `fuse_ab.fit_choice`.
    Numarul de candidati e `len(t_grid) + len(vlist)`, nu produsul lor.
    """
    import analysis_dist as ad
    neutru = np.arange(5.0) / 4.0
    jn = next((i for i, v in enumerate(vlist) if np.allclose(v, neutru)), None)
    if jn is None:
        raise SystemExit("citirea neutra (0, .25, .5, .75, 1) nu e in familia de candidati")
    langs = sorted(PL)
    R = {}
    for lg, D in PL.items():
        M = np.empty((len(t_grid), len(vlist)))
        for i, T in enumerate(t_grid):
            Q = [ad.temper(P, T) for P in D["Ps"]]
            for j, v in enumerate(vlist):
                M[i, j] = ad.r_of(np.mean([q @ v for q in Q], axis=0), D["y"])
        R[lg] = M

    def pick_v(exclude):
        keep = [l for l in langs if l not in exclude]
        crit = np.zeros(len(vlist))
        for l in keep:
            i, _ = _argmax_T(R, langs, jn, exclude=tuple(exclude) + (l,))
            crit += R[l][i, :]
        crit /= len(keep)
        return int(np.argmax(crit)), crit

    rows, params = [], {}
    for lg in langs:
        iT, critT = _argmax_T(R, langs, jn, exclude=(lg,))
        jv, crit = pick_v((lg,))
        params[lg] = (t_grid[iT], vlist[jv])
        rows.append(dict(lang=lg, T1=t_grid[iT], T2=t_grid[iT], w=0.5, K=5,
                         partitie="/".join(f"{x:.4f}" for x in vlist[jv]),
                         crit_lat=float(crit.max() - crit.min()),
                         margine=float(crit[jv] - crit[jn]),
                         la_limita=bool(iT in (0, len(t_grid) - 1)),
                         crit_lat_T=float(critT.max() - critT.min()),
                         n_cand=len(vlist), neutru=bool(jv == jn)))
    return params, pd.DataFrame(rows)


def pick_params(PL, mod, t_grid):
    """({limba: (T, partitie)}, tabelul de diagnostic).

    Ordinea e PRESPECIFICATA, ca in `make_bt_runs.pick_params`: intai T la partitia neutra, apoi
    partitia cu T fixat. 16 + 15 candidati, nu 240.
    """
    from make_bt_runs import COLAPS
    cols = COLAPS if mod == "colaps" else [None]
    jn = COLAPS.index([[0], [1], [2], [3], [4]]) if mod == "colaps" else 0
    langs = sorted(PL)
    R = _r_cube(PL, t_grid, cols)

    def pick_bl(exclude):
        """(indexul partitiei, criteriul) pe limbile rams dupa `exclude`.

        Criteriul unei partitii e media lui r peste limbile de potrivire, iar B-ul fiecarei limbi de
        potrivire l' se citeste la temperatura lui l' aleasa EXCLUZAND si l'. Al doilea nivel din
        `fuse_ab.fit_choice`, copiat din `make_bt_runs.pick_bl`.
        """
        keep = [l for l in langs if l not in exclude]
        crit = np.zeros(len(cols))
        for l in keep:
            i, _ = _argmax_T(R, langs, jn, exclude=tuple(exclude) + (l,))
            crit += R[l][i, :]
        return int(np.argmax(crit / len(keep))), crit / len(keep)

    rows, params = [], {}
    for lg in langs:
        iT, critT = _argmax_T(R, langs, jn, exclude=(lg,))
        T = t_grid[iT]
        jb, crit = pick_bl((lg,))
        bl = cols[jb]
        params[lg] = (T, bl)
        rows.append(dict(lang=lg, T1=T, T2=T, w=0.5,
                         K=len(bl) if bl else 5,
                         partitie=("|".join("".join(str(i + 1) for i in b) for b in bl)
                                   if bl else "1|2|3|4|5"),
                         crit_lat=float(crit.max() - crit.min()) if mod == "colaps" else float("nan"),
                         margine=float(crit[jb] - crit[jn]) if mod == "colaps" else float("nan"),
                         la_limita=bool(iT in (0, len(t_grid) - 1)),
                         crit_lat_T=float(critT.max() - critT.min())))
    return params, pd.DataFrame(rows)


def pick_params_pp(PL, mod, t_grid, n_p):
    """Ca `pick_params`, dar cu cate o temperatura PER PROMPT. -> ({limba: (Ts, partitie)}, tabel).

    **Ordinea e prespecificata si numarul de candidati e mic deliberat.** `analysis_dist.step_f_pick`
    face argmax pe grila plina 16x16 pentru doua prompturi, adica 256 de perechi, si exact asa a fost
    respins `distTpp`: marginea 0.001 pe un criteriu lat de 0.085. Pentru trei prompturi grila plina ar
    avea 4096 de candidati, deci nu se face. Aici:

      1. T comun, ales LOLO la partitia neutra. 16 candidati. E chiar `pick_params`.
      2. partitia, cu T comun fixat. 15 candidati. Numai la `--mod colaps`.
      3. pentru FIECARE prompt separat, o deviație de la T comun, cu celelalte prompturi lasate la T
         comun. 16 candidati per prompt, deci 48. Rafinarile sunt INDEPENDENTE intre ele, nu o coborare
         pe coordonate, si de aceea nu e nevoie de nicio ordine intre prompturi: ordinea ar fi fost un
         grad de libertate in plus, iar aici nu exista.

    16 + 15 + 48 = 79 de candidati, nu 4096 x 15. Criteriul unei deviații foloseste, pentru fiecare
    limba de potrivire l', T-ul comun al lui l' ales EXCLUZAND si L si l', al doilea nivel din
    `fuse_ab.fit_choice`. `crit_lat` si `margine` se scriu in tabel ca sa se vada daca alegerea e pe un
    criteriu plat, adica daca e chiar tiparul lui `distTpp`.
    """
    import analysis_dist as ad
    from make_bt_runs import COLAPS
    cols = COLAPS if mod == "colaps" else [None]
    jn = COLAPS.index([[0], [1], [2], [3], [4]]) if mod == "colaps" else 0
    langs = sorted(PL)
    R = _r_cube(PL, t_grid, cols)

    def pick_bl(exclude):
        keep = [l for l in langs if l not in exclude]
        crit = np.zeros(len(cols))
        for l in keep:
            i, _ = _argmax_T(R, langs, jn, exclude=tuple(exclude) + (l,))
            crit += R[l][i, :]
        return int(np.argmax(crit / len(keep))), crit / len(keep)

    rows, params = [], {}
    for lg in langs:
        iT, critT = _argmax_T(R, langs, jn, exclude=(lg,))
        Tc = t_grid[iT]
        jb, critB = pick_bl((lg,))
        bl = cols[jb]
        Ts, lat, marg, lim = [], [], [], []
        for j in range(n_p):
            crit = np.zeros(len(t_grid))
            for l2 in langs:
                if l2 == lg:
                    continue
                i2, _ = _argmax_T(R, langs, jn, exclude=(lg, l2))
                base = [t_grid[i2]] * n_p
                for k, T in enumerate(t_grid):
                    cand = list(base)
                    cand[j] = T
                    crit[k] += ad.r_of(b_of(PL[l2]["Ps"], cand, bl), PL[l2]["y"])
            crit /= (len(langs) - 1)
            k = int(np.argmax(crit))
            Ts.append(t_grid[k])
            lat.append(float(crit.max() - crit.min()))
            marg.append(float(crit[k] - crit[iT]))
            lim.append(bool(k in (0, len(t_grid) - 1)))
        params[lg] = (Ts, bl)
        rows.append(dict(lang=lg, T_comun=Tc,
                         **{f"T{j + 1}": Ts[j] for j in range(n_p)},
                         K=len(bl) if bl else 5,
                         partitie=("|".join("".join(str(i + 1) for i in b) for b in bl)
                                   if bl else "1|2|3|4|5"),
                         crit_lat=float(np.max(lat)), margine=float(np.sum(marg)),
                         la_limita=bool(any(lim) or iT in (0, len(t_grid) - 1)),
                         crit_lat_T=float(critT.max() - critT.min()),
                         crit_lat_B=float(critB.max() - critB.min()) if mod == "colaps" else float("nan")))
    return params, pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mod", default="temperatura", choices=MODS)
    ap.add_argument("--src", action="append", required=True,
                    help="CSV cu distributii; se poate da de mai multe ori. Fiecare contribuie "
                         "sloturile lui p1_*/p2_* nevide, in ordine.")
    ap.add_argument("--base", default=BASE,
                    help="CSV de la care se iau lang/token/complexity/C/sec. C nu se recalculeaza: "
                         "surprisal-ul nu depinde de prompt.")
    ap.add_argument("--per-prompt", dest="pp", action="store_true",
                    help="cate o temperatura per prompt, ca deviație de la T comun. 79 de candidati, "
                         "nu 4096: vezi pick_params_pp. Fara el, o singura temperatura, si atunci "
                         "trece controlul de octet.")
    ap.add_argument("--pas", type=int, default=8,
                    help="numai la --mod calibrare: numitorul grilei de cresteri, divizibil cu 4. "
                         "4 da 35 de candidati, 8 da 165, 12 da 455. 0 inseamna cele 15 partitii de "
                         "colaps scrise ca vectori, adica un control care trebuie sa dea `--mod colaps`.")
    ap.add_argument("--dir", required=True, help="numele directorului din output/, nu calea")
    a = ap.parse_args()

    import analysis_dist as ad
    dst = os.path.join(OUT, os.path.basename(a.dir))
    if os.path.abspath(dst) == os.path.abspath(SRC_DIR):
        raise SystemExit("--dir nu are voie sa fie chiar output/bakeoff_test/")
    os.makedirs(dst, exist_ok=True)

    PL, names = load_srcs(a.src)
    t_grid = ad.T_GRID_EXT
    print(f"[FS] mod {a.mod}{' , T per prompt' if a.pp else ''}, {len(names)} prompturi: "
          + ", ".join(names), flush=True)
    if a.mod == "calibrare":
        if a.pp:
            raise SystemExit("--per-prompt nu se combina cu --mod calibrare")
        vlist = colaps_vals() if a.pas == 0 else mono_grid(a.pas)
        print(f"[FS] familie de citiri monotone: {len(vlist)} candidati "
              f"({'colaps, scrise ca vectori' if a.pas == 0 else f'grila cu pas 1/{a.pas}'})",
              flush=True)
        params, tab = pick_params_v(PL, vlist, t_grid)
    else:
        params, tab = (pick_params_pp(PL, a.mod, t_grid, len(names)) if a.pp
                       else pick_params(PL, a.mod, t_grid))
    for lg, (T, bl) in sorted(params.items()):
        Tt = ("/".join(f"{t:g}" for t in T) if not np.isscalar(T) else f"{T:g}")
        if a.mod == "calibrare":
            extra = "  v=" + "/".join(f"{x:.3f}" for x in bl)
        else:
            extra = ("  " + "|".join("".join(str(i + 1) for i in b) for b in bl)) if bl else ""
        print(f"    {lg:4s} T={Tt}{extra}", flush=True)

    # Scrierea trece prin CSV-ul BRUT, nu prin cadrul reordonat pe cod de limba: `with_context`
    # recupereaza `idx` pozitional, deci ordinea fisierului e cheia si nu are voie sa se schimbe.
    base = pd.read_csv(a.base)
    srcs = [pd.read_csv(p) for p in a.src]
    Ps_all = []
    for p, d in zip(a.src, srcs):
        if len(d) != len(base):
            raise SystemExit(f"{p} are {len(d)} randuri, --base are {len(base)}")
        bad = ((d["lang"].astype(str).values != base["lang"].astype(str).values)
               | (d["token"].astype(str).values != base["token"].astype(str).values)
               | (np.abs(d["complexity"].values - base["complexity"].values) > 1e-6))
        if bad.any():
            i = int(np.flatnonzero(bad)[0])
            raise SystemExit(f"{p} nu e in aceeasi ordine cu --base, prima diferenta la randul {i}")
        for cols in prompt_cols(d):
            Ps_all.append(d[cols].values.astype(float))
    if len(Ps_all) != len(names):
        raise SystemExit(f"{len(Ps_all)} prompturi la scriere, {len(names)} la selectie")

    lg = base["lang"].astype(str).values
    B = np.empty(len(base))
    for k in np.unique(lg):
        m = (lg == k)
        T, bl = params[k]
        B[m] = (b_of([P[m] for P in Ps_all], T, vals=bl) if a.mod == "calibrare"
                else b_of([P[m] for P in Ps_all], T, bl))

    out = base[["lang", "token", "complexity", "B", "C", "sec"]].copy()
    old = out["B"].values.copy()
    out["B"] = [f"{v:.8f}" for v in B]
    out["complexity"] = [f"{v:.6f}" for v in out["complexity"].values]
    out["C"] = ["" if not np.isfinite(v) else f"{v:.8f}" for v in out["C"].values]
    out["sec"] = [f"{v:.4f}" for v in out["sec"].values]
    p = os.path.join(dst, f"{MODEL}.csv")
    # `lineterminator="\r\n"`: aceeasi conventie cu `csv.writer` din `bakeoff_trial.measure` si cu
    # `make_bt_runs`, ca fisierele sa fie comparabile la nivel de octet.
    out.to_csv(p, index=False, lineterminator="\r\n")
    print(f"[FS] {len(out)} randuri -> {p}")
    print(f"[FS] B: max |dif| fata de --base = {np.abs(B - old).max():.6f}")

    q = os.path.join(OUT, f"bt_params_{os.path.basename(a.dir)}.csv")
    tab.to_csv(q, index=False)
    print(f"[FS] parametri -> {q}")

    for f in sorted(os.listdir(SRC_DIR)):
        if f.endswith(".csv") and f != f"{MODEL}.csv":
            shutil.copyfile(os.path.join(SRC_DIR, f), os.path.join(dst, f))
            print(f"[FS] copiat verbatim: {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
