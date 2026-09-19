"""E.14. Al treilea prompt, cernut pe TRIAL sub protocolul complet.

Intrebarea, si e una de procedura, nu de performanta. Pe test, `M3K` cu `marcat` da 0.690001 si `FS3K`
cu `few-shot` da 0.688506, iar diferenta e +0.001510 [-0.001142, +0.004239], adica nu se distinge.
Atunci singurul lucru care le separa e CUM a fost ales al treilea membru: few-shot era clar primul pe
trial, marcat era al treilea. Deci `FS3K` e „ales pe trial, evaluat o data pe test", iar `M3K` are o
decizie de test in plus.

Dar clasamentul de trial pe care se sprijină afirmatia aia a fost calculat din
`output/promptlab_gemma4-12b-4bit.csv`, care are numai scorul scalar, deci **la T = 1 si fara nicio
selecție**. Pe test, protocolul e altul: distributii, temperatura aleasa LOLO, si opțional partitia de
unire a cifrelor. Comparatia corecta cere acelasi protocol pe trial.

Daca sub protocolul complet marcat iese primul si pe trial, atunci `M3K` devine si el „ales pe trial"
si cele doua configuratii nu mai difera prin nimic care sa se poata apara. Daca few-shot rams primul,
atunci `FS3K` pastreaza avantajul de procedura.

Criteriul de selectie NU e rescris aici: se cheama chiar `make_fs_runs.pick_params`, deci T si partitia
se aleg pe trial in exact aceeasi forma ca pe test. Singura diferenta e cadrul de intrare.

Intervalele de trial sunt late si trebuie sa fie: 30 de instante per limba, nu 560. Ce se citeste de
aici e ORDINEA, nu cifrele.

Rulare:
  python prompt_lab.py --model gemma4-12b-4bit \\
      --variants v3_fewshot,v8_marcat,v2_rubrica,v1_learner \\
      --out output/dist/promptlab_dist_trial.csv
  python analysis_al3lea_trial.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_al3lea_trial.md")
SRC = os.path.join(OUT, "dist", "promptlab_dist_trial.csv")
PAIR = os.path.join(OUT, "dist", "gemma4-12b-4bit_trial.csv")

# (eticheta, varianta din prompt_lab, castigul pe B pe TEST, ce era pe trial la T=1)
MEMBRI = [("few-shot", "v3_fewshot", +0.005247, "+0.7109, primul"),
          ("marcat", "v8_marcat", +0.004146, "+0.6895, al treilea"),
          ("rubrica", "v2_rubrica", +0.000857, "+0.6904, al doilea"),
          ("learner", "v1_learner", +0.000286, "+0.6773, sub perechea de doua")]

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def load_trial():
    """(cadrul cu cele patru variante, cadrul cu perechea zero-shot), amandoua cu `context_id`."""
    from bakeoff_trial import with_context
    for q in (SRC, PAIR):
        if not os.path.exists(q):
            raise SystemExit(f"{q} lipseste")
    d = pd.read_csv(SRC)
    pair = with_context(pd.read_csv(PAIR), "trial")
    return d, pair


def pl_of(d, pair, varianta):
    """{limba: dict(Ps, y, ctx, n)} cu Ps = [membrul al treilea, promptul expert, promptul scurt].

    Forma e chiar cea pe care o consuma `make_fs_runs.pick_params`, deci criteriul de selectie e
    identic la forma cu cel de pe test si nu se rescrie nimic. Alinierea e POZITIONALA, cu verificare
    pe limba, tinta si complexitate: `prompt_lab.measure` parcurge `load_mlsp("trial")` cu
    `itertuples`, la fel ca `bakeoff_trial.measure`.
    """
    x = d[d["variant"] == varianta].reset_index(drop=True)
    if len(x) != len(pair):
        raise SystemExit(f"{varianta}: {len(x)} randuri, perechea are {len(pair)}")
    bad = ((x["lang"].astype(str).values != pair["lang"].astype(str).values)
           | (x["token"].astype(str).values != pair["token"].astype(str).values)
           | (np.abs(x["complexity"].values - pair["complexity"].values) > 1e-6))
    if bad.any():
        raise SystemExit(f"{varianta}: aliniere pozitionala esuata la randul "
                         f"{int(np.flatnonzero(bad)[0])}")
    x = x.assign(ctx=pair["context_id"].values)
    out = {}
    for lg in sorted(pair["lang"].astype(str).unique()):
        m = (x["lang"].astype(str).values == lg)
        g, gp = x[m], pair[pair["lang"].astype(str) == lg]
        P3 = g[[f"p1_{k}" for k in "12345"]].values.astype(float)
        P1 = gp[[f"p1_{k}" for k in "12345"]].values.astype(float)
        P2 = gp[[f"p2_{k}" for k in "12345"]].values.astype(float)
        out[lg] = dict(Ps=[P3, P1, P2], y=g["complexity"].values.astype(float),
                       ctx=g["ctx"].values, n=len(g))
    return out


def r_under(PL, mod):
    """(r mediu, esantioane bootstrap per limba) pentru ansamblul lui `PL`, cu parametrii alesi LOLO
    de `make_fs_runs.pick_params`. `mod` e `temperatura` sau `colaps`."""
    import analysis_dist as ad
    from make_fs_runs import pick_params, b_of
    params, tab = pick_params(PL, mod, ad.T_GRID_EXT)
    langs = sorted(PL)
    boots, rs = [], []
    for lg in langs:
        T, bl = params[lg]
        b = b_of(PL[lg]["Ps"], T, bl)
        rs.append(ad.r_of(b, PL[lg]["y"]))
        boots.append(ad.boot_one(PL[lg]["y"], b, PL[lg]["ctx"])["boot"])
    return float(np.mean(rs)), boots, tab


def main():
    import analysis_dist as ad
    from make_fs_runs import pick_params, b_of
    d, pair = load_trial()
    prezente = [m for m in MEMBRI if m[1] in set(d["variant"])]
    if not prezente:
        raise SystemExit(f"{SRC} n-are niciuna din variantele {[m[1] for m in MEMBRI]}")
    langs = sorted(pair["lang"].astype(str).unique())

    # linia de baza: perechea de acum, sub acelasi protocol
    PLp = {lg: dict(Ps=v["Ps"][1:], y=v["y"], ctx=v["ctx"], n=v["n"])
           for lg, v in pl_of(d, pair, prezente[0][1]).items()}
    r_pair, B_pair, _ = r_under(PLp, "temperatura")
    r_pairK, B_pairK, _ = r_under(PLp, "colaps")

    emit("# E.14. Al treilea prompt, cernut pe trial sub protocolul complet\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_al3lea_trial.py`. "
         f"{sum(PLp[lg]['n'] for lg in langs)} instante de trial, {len(langs)} limbi. "
         f"Criteriul de selectie e chiar `make_fs_runs.pick_params`, nerescris.\n",
         __doc__.split("Criteriul de selectie")[0].split("\n", 2)[2].strip() + "\n",
         f"Perechea de acum, sub acelasi protocol: **{r_pair:+.6f}** cu T ales LOLO, "
         f"**{r_pairK:+.6f}** cu T plus partitia.\n")

    emit("## Clasamentul, si ce se compara cu ce\n",
         "`la T=1, fara selecție` e clasamentul vechi, din `output/promptlab_gemma4-12b-4bit.csv`, pe "
         "care s-a sprijinit afirmatia `few-shot a fost ales pe trial`. `sub protocol complet` e "
         "acelasi lucru masurat cum se masoara pe test. `castig pe B, pe TEST` e coloana cu care se "
         "compara ordinea.\n",
         "| membru | la T=1, fara selecție | solo, protocol complet | in trei, T LOLO | "
         "in trei, T + partitie | castig peste pereche | castig pe B, pe TEST |",
         "|---|---|---|---|---|---|---|")
    S = {}
    for nm, var, d_test, vechi in prezente:
        PL = pl_of(d, pair, var)
        PLs = {lg: dict(Ps=[v["Ps"][0]], y=v["y"], ctx=v["ctx"], n=v["n"]) for lg, v in PL.items()}
        r_solo, _, _ = r_under(PLs, "temperatura")
        r3, B3, tab3 = r_under(PL, "temperatura")
        r3k, B3k, tab3k = r_under(PL, "colaps")
        S[nm] = dict(solo=r_solo, r3=r3, r3k=r3k, B3=B3, B3k=B3k, d_test=d_test,
                     part=tab3k["partitie"].tolist())
        emit(f"| `{nm}` | {vechi} | {r_solo:+.6f} | {r3:+.6f} | {r3k:+.6f} | "
             f"**{r3 - r_pair:+.6f}** | {d_test:+.6f} |")
        print(f"    {nm:9s} solo {r_solo:+.4f}  in trei {r3:+.4f}  +partitie {r3k:+.4f}  "
              f"castig {r3 - r_pair:+.6f}", flush=True)
    emit("")

    emit("### Comparatii perechi pe trial, fata de perechea de acum\n",
         "Reesantionare pe contexte, seed fix, deci perechea vede aceeasi reesantionare. Intervalele "
         "sunt late fiindca sunt 30 de instante per limba.\n",
         "| membru | in trei fata de pereche | CI 95% pereche | P(>0) |", "|---|---|---|---|")
    for nm in S:
        dm, lo, hi, pp = ad.mean_diff_ci(S[nm]["B3"], B_pair)
        emit(f"| `{nm}` | **{dm:+.6f}** | [{lo:+.6f}, {hi:+.6f}] | {pp:.1%} |")
    emit("")

    # --- verdictul de procedura, fara nicio cifra scrisa de mana
    ord_trial = sorted(S, key=lambda k: -S[k]["r3"])
    ord_test = sorted(S, key=lambda k: -S[k]["d_test"])
    kt = float(pd.Series([S[k]["r3"] for k in S]).corr(
        pd.Series([S[k]["d_test"] for k in S]), method="kendall"))
    emit("## Verdict de procedura\n",
         f"Ordinea pe trial, sub protocolul complet: " + " > ".join(f"`{k}`" for k in ord_trial) + ".\n",
         f"Ordinea pe test, dupa castigul pe B: " + " > ".join(f"`{k}`" for k in ord_test) + ".\n",
         f"Concordanta Kendall intre cele doua ordini, pe cei {len(S)} membri: **{kt:+.3f}**.\n")
    prim_trial, prim_test = ord_trial[0], ord_test[0]
    if prim_trial == prim_test:
        emit(f"**Primul e acelasi in ambele, `{prim_trial}`.** Deci configuratia cu el e aleasa pe "
             "trial si evaluata o data pe test, si nu are nicio decizie de test in alegerea membrului. "
             "Celalalt candidat rams cu o decizie de test in plus, si asta e singurul lucru care le "
             "separa, fiindca cifrele lor nu se distinge.\n")
    else:
        emit(f"**Primul difera:** pe trial iese `{prim_trial}`, pe test `{prim_test}`. Deci selecția pe "
             f"trial sub protocolul complet ar fi ales `{prim_trial}`, iar orice preferinta pentru "
             f"`{prim_test}` rams o decizie luata pe setul de test. A treia rasturnare trial-test in "
             "acelasi fir.\n")
    print(f"[E14] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
