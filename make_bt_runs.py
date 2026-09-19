"""Scrie CSV-uri de bake-off pe test cu semnalul B recitit altfel, pentru `fuse_ab --b-dir`.

Nu masoara nimic si nu cheama niciun model: ia distributiile deja salvate de `rate_parts` in
`output/dist/gemma4-12b-4bit_test.csv` si rescrie coloana `B`. Restul CSV-urilor de test se copiaza
verbatim, ca bazinul de candidati al lui `pick_model` sa ramana exact acelasi si sa se schimbe UN
SINGUR lucru fata de sistem.

Patru moduri de reconstructie a lui B, prin `--mod`:

  `temperatura`     ce era pana acum: `0.5*(E(p1^(1/T1)) + E(p2^(1/T2)))`, T ales LOLO pe `--grid`.
  `pondere`         `w*E(p1^(1/T)) + (1-w)*E(p2^(1/T))`, cu T FIXAT la valoarea adoptata per limba
                    (grila extinsa, ce foloseste sistemul) si numai `w` ales LOLO. Media 50/50 e in
                    grila lui w, deci modul se poate reduce la configuratia adoptata, si asta e
                    controlul de reproducere.
  `produs`          media geometrica a celor doua distributii, renormalizata, apoi valoarea
                    asteptata, cu T propriu ales LOLO. **Puterea si produsul comuta**:
                    `(p^(1/T) q^(1/T))^(1/2) = (pq)^(1/(2T))`, deci produsul la T fix ar fi confundat
                    cu temperatura, si nu ar fi comparabil cu media aritmetica. De aceea T se realege
                    pe ACEEASI grila extinsa: acelasi numar de candidati, alt agregator.
  `pondere-produs`  media geometrica PONDERATA, `p1^w * p2^(1-w)` renormalizata, cu T ca la `produs`
                    si `w` ales LOLO ca la `pondere`.

Cum se alege `w`, si de ce nu e la fel de simplu ca T. T se alege pentru limba L ca argmaxul mediei
lui r peste randurile de test ale CELORLALTE 9 limbi, exact forma din `analysis_dist.temp_pick`.
Pentru `w` criteriul ar avea nevoie de un B al limbii l' de potrivire, iar B-ul acela depinde el insusi
de o temperatura care a fost aleasa uitandu-se si la L. Deci criteriul lui `w` foloseste, pentru
fiecare pereche (L, l'), temperatura lui l' aleasa pe cele 8 limbi rams, adica excluzand si L si l'.
E al doilea nivel din `fuse_ab.fit_choice`, aceeasi grija, si fara el alegerea lui `w` pentru L ar
trece prin etichetele lui L.

Randurile pastreaza ORDINEA fisierului sursa, fiindca `bakeoff_trial.with_context` recupereaza
`context_id` si `idx` pozitional. De aceea nu se trece prin cadrul reordonat pe cod de limba al lui
`analysis_dist.load`, ci se aplica harta de parametri pe CSV-ul brut.

Parametrii alesi, plus latimea criteriului si marginea peste punctul neutru, se scriu langa director
in `output/bt_params_<dir>.md`, NU in el: `bakeoff_trial.load_runs` ia fiecare `*.csv` din director ca
pe un model, deci un fisier in plus acolo ar intra tacut in bazinul de candidati al lui `pick_model`.

Rulare:
  python make_bt_runs.py --grid identitate --dir bakeoff_test_T1   # control: trebuie sa dea 0.674946
  python make_bt_runs.py --grid specificata --dir bakeoff_test_T
  python make_bt_runs.py --grid extinsa --dir bakeoff_test_Text
  python make_bt_runs.py --mod pondere --w-grid 0.5 --dir bakeoff_test_W05   # control: = _Text
  python make_bt_runs.py --mod pondere --dir bakeoff_test_W
  python make_bt_runs.py --mod produs --dir bakeoff_test_G
  python make_bt_runs.py --mod pondere-produs --dir bakeoff_test_WG
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
# Grila lui w. 0.5 e media aritmetica de pana acum, deci punctul neutru e IN grila si alegerea LOLO
# poate sa nu schimbe nimic. 0 si 1 sunt cele doua prompturi luate singure.
W_GRID = (0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0)
MODS = ("temperatura", "pondere", "produs", "pondere-produs", "colaps",
        "colaps-pondere")
# Toate partitiile CONTIGUE ale celor cinci cifre in 2..5 blocuri, adica 15 candidati.
# O scara mai grosiera nu poate reordona notele, doar sa le uneasca pe cele vecine.
import itertools as _it
COLAPS = [[list(range(a, b)) for a, b in zip((0,) + c, c + (5,))]
          for K in (2, 3, 4, 5) for c in _it.combinations(range(1, 5), K - 1)]


def gmean(P1, P2, w=0.5):
    """Media geometrica PONDERATA a doua distributii, renormalizata. `w = 0.5` e cea obisnuita.

    Clip la 1e-300 inainte de ridicare la putere: o probabilitate exact 0 la un prompt ar duce toata
    coloana la 0, deci produsul ar fi nedefinit acolo unde un singur prompt e sigur pe o cifra.
    """
    G = (np.power(np.clip(P1, 1e-300, None), w)
         * np.power(np.clip(P2, 1e-300, None), 1.0 - w))
    return G / G.sum(axis=1, keepdims=True)


def b_build(P1, P2, mod, T1, T2=None, w=0.5, bl=None):
    """Semnalul B, pentru oricare din cele cinci moduri. UN SINGUR loc unde se scrie aritmetica.

    Se cheama si de criteriul de selectie si de scrierea fisierului, deci nu se poate intampla ca
    parametrul sa fie ales pe o formula si aplicat pe alta.

    `bl` e o partitie a celor cinci cifre in blocuri contigue, folosita numai de modul `colaps`:
    fiecare bloc primeste ca valoare media notelor lui, deci `B` ramane o citire liniara MONOTONA a
    distributiei, doar cu alta spatiere a nivelurilor. Aceeasi partitie pentru ambele prompturi.
    """
    import analysis_dist as ad
    if mod.startswith("colaps"):
        v = np.array([np.mean([i + 1 for i in b]) for b in bl], float)
        ww = 0.5 if mod == "colaps" else w
        Q1, Q2 = ad.temper(P1, T1), ad.temper(P2, T1)
        C1 = np.column_stack([Q1[:, b].sum(axis=1) for b in bl])
        C2 = np.column_stack([Q2[:, b].sum(axis=1) for b in bl])
        return (ww * (C1 @ v) + (1.0 - ww) * (C2 @ v) - 1.0) / 4.0
    if mod.endswith("produs"):
        # Puterea si produsul comuta, deci o singura temperatura, aplicata mediei geometrice.
        return ad.expected(ad.temper(gmean(P1, P2, w), T1))
    T2 = T1 if T2 is None else T2
    return (w * ad.expected(ad.temper(P1, T1))
            + (1.0 - w) * ad.expected(ad.temper(P2, T2)))


def _r_cube(PL, mod, t_grid, w_grid):
    """{limba: matrice (len(t_grid), len(coloane))} cu r al lui B(limba, T, coloana).

    A doua axa e grila lui `w`, sau lista de partitii la modul `colaps`: in ambele cazuri e „al doilea
    parametru", si tot restul selectiei o trateaza la fel.
    """
    import analysis_dist as ad
    cols = COLAPS if mod.startswith("colaps") else list(w_grid)
    out = {}
    for lg, D in PL.items():
        M = np.empty((len(t_grid), len(cols)))
        for i, T in enumerate(t_grid):
            for j, c in enumerate(cols):
                M[i, j] = ad.r_of(
                    b_build(D["P1"], D["P2"], "colaps", T, T, 0.5, c)
                    if mod.startswith("colaps")
                    else b_build(D["P1"], D["P2"], mod, T, T, c), D["y"])
        out[lg] = M
    return out


def _argmax_T(R, langs, jw, exclude):
    """Indexul lui T ales pe limbile din `langs` fara cele din `exclude`, la coloana `jw` a lui w."""
    keep = [l for l in langs if l not in exclude]
    crit = np.mean([R[l][:, jw] for l in keep], axis=0)
    return int(np.argmax(crit)), crit


def pick_params(mod, grid_name, w_grid):
    """{limba: (T1, T2, w)}, tabelul de diagnostic si grila de T folosita.

    `temperatura` deleaga la `analysis_dist.temp_pick` prin `pick_temps`, ca fisierele deja produse sa
    se reproduca bit cu bit. Celelalte trei moduri isi aleg parametrii aici. Grila lui w se intoarce
    ca a PATRA valoare, fiindca modul o poate reduce: la `produs` e (0.5,) orice s-ar cere.
    """
    import analysis_dist as ad
    if mod == "temperatura":
        temps, grid = pick_temps(grid_name)
        t = pd.DataFrame([dict(lang=lg, T1=t1, T2=t2, w=0.5, crit_lat=float("nan"),
                               margine=float("nan"), la_limita=False)
                          for lg, (t1, t2) in sorted(temps.items())])
        return {lg: (t1, t2, 0.5) for lg, (t1, t2) in temps.items()}, t, grid, (0.5,)

    if grid_name != "extinsa":
        raise SystemExit(f"--mod {mod} cere --grid extinsa: T-ul adoptat de sistem e cel de pe grila "
                         "extinsa, iar o alta grila ar schimba doua lucruri deodata")
    t_grid = ad.T_GRID_EXT
    if mod == "produs":
        # Media geometrica SIMPLA: `w` nu e parametrul modului, e fixat la punctul neutru. Ponderarea
        # celor doua prompturi e modul `pondere-produs`, si separarea e deliberata: altfel n-am putea
        # spune daca a castigat agregatorul sau ponderea.
        w_grid = (0.5,)
    PL = ad.per_lang(ad.load())
    langs = sorted(PL)
    R = _r_cube(PL, mod, t_grid, w_grid)
    j05 = list(w_grid).index(0.5) if 0.5 in w_grid else 0

    jn = COLAPS.index([[0], [1], [2], [3], [4]]) if mod.startswith("colaps") else None

    def pick_bl(exclude):
        """(indexul partitiei, criteriul) pe limbile rams dupa `exclude`.

        Criteriul unei partitii e media lui r peste limbile de potrivire, iar B-ul fiecarei limbi de
        potrivire l' se citeste la temperatura lui l' aleasa EXCLUZAND si l'. Al doilea nivel din
        `fuse_ab.fit_choice`. Ajutorul e unul singur fiindca amandoua modurile cu partitie trebuie sa
        aleaga la fel: prima versiune avea doua criterii usor diferite si dadea alta partitie pe
        japoneza, exact felul de divergenta care nu s-ar vedea in nicio cifra.
        """
        keep = [l for l in langs if l not in exclude]
        crit = np.zeros(len(COLAPS))
        for l in keep:
            i, _ = _argmax_T(R, langs, jn, exclude=tuple(exclude) + (l,))
            crit += R[l][i, :]
        return int(np.argmax(crit / len(keep))), crit / len(keep)

    if mod == "colaps":
        # Doi parametri, alesi in aceeasi forma: T pe grila extinsa la partitia neutra (cele cinci
        # cifre separate), apoi partitia pe cele 15 candidate. Punctul neutru e in grila, deci modul se
        # poate reduce la sistem, si `b_build` la partitia neutra da chiar B la temperatura.
        rows, params = [], {}
        for lg in langs:
            iT, critT = _argmax_T(R, langs, jn, exclude=(lg,))
            T = t_grid[iT]
            jb, crit = pick_bl((lg,))
            params[lg] = (T, T, 0.5, COLAPS[jb])
            rows.append(dict(lang=lg, T1=T, T2=T, w=0.5, K=len(COLAPS[jb]),
                             partitie="|".join("".join(str(i + 1) for i in b) for b in COLAPS[jb]),
                             crit_lat=float(crit.max() - crit.min()),
                             margine=float(crit[jb] - crit[jn]),
                             la_limita=bool(iT in (0, len(t_grid) - 1)),
                             crit_lat_T=float(critT.max() - critT.min())))
        return params, pd.DataFrame(rows), t_grid, (0.5,)

    if mod == "colaps-pondere":
        # Doua parghii, in ordine PRESPECIFICATA: intai partitia, ca la `colaps`, apoi `w` cu partitia
        # fixata. 15 + 7 candidati, nu 105: un argmax pe 105 perechi cu un criteriu lat de 0.08 e chiar
        # eroarea pentru care s-a respins `distTpp`.
        rows, params, vazute = [], {}, set()
        # r al lui B(l', T_i, w_k) cu partitia lui l' fixata: se recalculeaza, fiindca a doua axa nu
        # mai e aceeasi pentru toate limbile.
        for lg in langs:
            iTL, _ = _argmax_T(R, langs, jn, exclude=(lg,))
            jbL, _ = pick_bl((lg,))
            T = t_grid[iTL]
            crit = np.zeros(len(w_grid))
            for l2 in langs:
                if l2 == lg:
                    continue
                jb2, _ = pick_bl((lg, l2))
                i2, _ = _argmax_T(R, langs, jn, exclude=(lg, l2))
                vazute.add(jb2)
                D2 = PL[l2]
                crit += np.array([ad.r_of(b_build(D2["P1"], D2["P2"], "colaps-pondere",
                                                  t_grid[i2], t_grid[i2], w, COLAPS[jb2]),
                                          D2["y"]) for w in w_grid])
            crit /= (len(langs) - 1)
            jw = int(np.argmax(crit))
            params[lg] = (T, T, w_grid[jw], COLAPS[jbL])
            rows.append(dict(lang=lg, T1=T, T2=T, w=w_grid[jw], K=len(COLAPS[jbL]),
                             partitie="|".join("".join(str(i + 1) for i in b) for b in COLAPS[jbL]),
                             crit_lat=float(crit.max() - crit.min()),
                             margine=float(crit[jw] - crit[list(w_grid).index(0.5)]),
                             la_limita=bool(jw in (0, len(w_grid) - 1)),
                             crit_lat_T=float("nan")))
        print(f"[B] partitii distincte peste toate perechile imbricate: {len(vazute)}", flush=True)
        return params, pd.DataFrame(rows), t_grid, w_grid

    rows, params = [], {}
    for lg in langs:
        # T pentru L: forma din temp_pick, la punctul neutru al lui w.
        iT, critT = _argmax_T(R, langs, j05, exclude=(lg,))
        T = t_grid[iT]
        # w pentru L: criteriul foloseste, pentru fiecare limba de potrivire l', temperatura lui l'
        # aleasa fara L si fara l'. Al doilea nivel din fuse_ab.fit_choice.
        crit = np.zeros(len(w_grid))
        for l2 in langs:
            if l2 == lg:
                continue
            i2, _ = _argmax_T(R, langs, j05, exclude=(lg, l2))
            crit += R[l2][i2, :]
        crit /= (len(langs) - 1)
        jw = int(np.argmax(crit))
        w = w_grid[jw]
        params[lg] = (T, T, w)
        rows.append(dict(lang=lg, T1=T, T2=T, w=w,
                         crit_lat=float(crit.max() - crit.min()),
                         margine=float(crit[jw] - crit[j05]),
                         la_limita=bool(iT in (0, len(t_grid) - 1) or jw in (0, len(w_grid) - 1)),
                         T_la_limita=bool(iT in (0, len(t_grid) - 1)),
                         crit_lat_T=float(critT.max() - critT.min())))
    return params, pd.DataFrame(rows), t_grid, w_grid


def pick_temps(grid_name):
    """{limba: (T1, T2)} sub selectia LOLO, plus grila folosita.

    `identitate` nu alege nimic: T = 1 peste tot, deci fisierul rezultat trebuie sa fie identic cu cel
    de pornire, si asta e controlul. `per-prompt` alege o pereche, deci cele doua prompturi primesc
    temperaturi diferite; celelalte doua grile dau aceeasi temperatura amandurora.
    """
    import analysis_dist as ad
    if grid_name == "identitate":
        return {lg: (1.0, 1.0) for lg in ad.LANGS}, (1.0,)
    PL = ad.per_lang(ad.load())
    if grid_name == "per-prompt":
        te, *_ = ad.temp_pick(PL, ad.T_GRID_EXT)
        t, _ = ad.step_f_pick(PL, {r["lang"]: float(r["T"]) for _, r in te.iterrows()})
        return {r["lang"]: (float(r["T1"]), float(r["T2"])) for _, r in t.iterrows()}, ad.T_GRID_EXT
    grid = ad.T_GRID if grid_name == "specificata" else ad.T_GRID_EXT
    t, *_ = ad.temp_pick(PL, grid)
    return {r["lang"]: (float(r["T"]), float(r["T"])) for _, r in t.iterrows()}, grid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mod", default="temperatura", choices=MODS)
    ap.add_argument("--grid", default=None,
                    choices=("identitate", "specificata", "extinsa", "per-prompt"),
                    help="grila lui T. Implicit `specificata` la --mod temperatura, `extinsa` la "
                         "celelalte, care e grila T-ului adoptat de sistem.")
    ap.add_argument("--w-grid", dest="w_grid", default=None,
                    help="grila lui w, valori separate prin virgula. Implicit "
                         + ",".join(f"{w:g}" for w in W_GRID)
                         + ". `--w-grid 0.5` reduce modul la punctul neutru, deci e controlul de "
                           "reproducere.")
    ap.add_argument("--dir", required=True, help="numele directorului din output/, nu calea")
    ap.add_argument("--src", default=os.path.join(OUT, "dist", f"{MODEL}_test.csv"),
                    help="CSV-ul cu distributii salvate")
    a = ap.parse_args()
    grid_name = a.grid or ("specificata" if a.mod == "temperatura" else "extinsa")
    w_grid = (tuple(float(x) for x in a.w_grid.split(",")) if a.w_grid else W_GRID)

    dst = os.path.join(OUT, os.path.basename(a.dir))
    if os.path.abspath(dst) == os.path.abspath(SRC_DIR):
        raise SystemExit("--dir nu are voie sa fie chiar output/bakeoff_test/")
    os.makedirs(dst, exist_ok=True)

    params, tab, grid, w_grid = pick_params(a.mod, grid_name, w_grid)
    # `w_grid` se reia din pick_params, nu de la linia de comanda: `--mod produs` o reduce la punctul
    # neutru, si tiparirea grilei cerute in loc de cea folosita ar minti exact in jurnal.
    print(f"[B] mod {a.mod}, grila T {grid_name}, grila w "
          + ",".join(f"{w:g}" for w in w_grid), flush=True)
    for lg, (t1, t2, w, *rest) in sorted(params.items()):
        extra = ("  " + "|".join("".join(str(i + 1) for i in b) for b in rest[0])) if rest else ""
        print(f"    {lg:4s} T={t1:g}/{t2:g}  w={w:g}{extra}", flush=True)

    d = pd.read_csv(a.src)
    P1 = d[[f"p1_{k}" for k in "12345"]].values.astype(float)
    P2 = d[[f"p2_{k}" for k in "12345"]].values.astype(float)
    lg = d["lang"].astype(str).values
    # Parametrii sunt per LIMBA, iar `b_build` ia scalari, deci se aplica pe grupe.
    B = np.empty(len(d))
    for k in np.unique(lg):
        m = (lg == k)
        t1, t2, w, *rest = params[k]
        B[m] = b_build(P1[m], P2[m], a.mod, t1, t2, w, rest[0] if rest else None)

    out = d[["lang", "token", "complexity", "B", "C", "sec"]].copy()
    old = out["B"].values.copy()
    out["B"] = [f"{v:.8f}" for v in B]
    out["complexity"] = [f"{v:.6f}" for v in out["complexity"].values]
    out["C"] = ["" if not np.isfinite(v) else f"{v:.8f}" for v in out["C"].values]
    out["sec"] = [f"{v:.4f}" for v in out["sec"].values]
    p = os.path.join(dst, f"{MODEL}.csv")
    # `lineterminator="\r\n"`: aceeasi conventie cu `csv.writer` din `bakeoff_trial.measure`, ca
    # fisierele sa fie comparabile la nivel de octet cu cele canonice.
    out.to_csv(p, index=False, lineterminator="\r\n")
    print(f"[B] {len(out)} randuri -> {p}")
    print(f"[B] B: max |dif| fata de sursa = {np.abs(B - old).max():.6f}, "
          f"identitate asteptata = {a.mod == 'temperatura' and grid_name == 'identitate'}")

    # Tabelul de parametri se scrie LANGA director, nu in el: load_runs ia fiecare *.csv din director
    # ca pe un model si l-ar pune in bazinul lui pick_model.
    q = os.path.join(OUT, f"bt_params_{os.path.basename(a.dir)}.csv")
    tab.to_csv(q, index=False)
    print(f"[B] parametri -> {q}")

    for f in sorted(os.listdir(SRC_DIR)):
        if f.endswith(".csv") and f != f"{MODEL}.csv":
            shutil.copyfile(os.path.join(SRC_DIR, f), os.path.join(dst, f))
            print(f"[B] copiat verbatim: {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
