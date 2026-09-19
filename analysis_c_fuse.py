"""Semnalul C ca AL TREILEA termen peste fuziunea adoptata, cu u ales leave-one-language-out.

Ce face, si de ce nu atinge `fuse_ab.py`. Fuziunea adoptata ramane inghetata, exact cum e scrisa in
`output/fusion_preds_lolo_adoptat_temp.csv`, si peste ea se adauga un singur termen:

    p3 = (1 - u) * z(p_fuz) + u * z(C)

`u` se alege pentru limba L ca argmaxul mediei lui r peste randurile de TEST ale celorlalte noua
limbi, adica exact criteriul prin care se aleg `w`, `w_src` si setul de trasaturi. Limba L nu intra
nicaieri.

Motivul pentru care u NU se alege impreuna cu w intr-o grila 2D in `fuse_ab.fit_choice`: pe 22 august
s-a masurat ca un grad de libertate in plus poate strica **si atunci cand ajunge sa nu fie folosit**,
prin criteriul imbricat. Ponderea per item a iesit `a = 0` pe 10/10 limbi si totusi varianta
`dezacord` a pierdut -0.000331, fiindca argmaxul peste matricea largita al unei limbi de potrivire a
cazut pe `a` nenul si a mutat `w` ales pentru limba tinuta deoparte. Aici grila lui `w` nu se atinge,
deci efectul acela nu poate aparea.

Grila lui `u` cuprinde **zero si valori negative**. Negativul nu e o extravaganta: frontiera arata ca
un semnal poate intra ca SUPRESOR, adica corelat cu fuziunea si necorelat cu eticheta, si atunci
scaderea lui corecteaza. Semnul e ales o singura data, global, prin acelasi criteriu LOLO, deci nu e
selectie de semn per limba.

Trei controale, si niciunul nu e optional:

  `--u-grid 0`      reproducerea. Cu grila redusa la {0}, `p3` trebuie sa iasa identic la 0.0 fata de
                    `p_fuz` si r pana la a zecea zecimala. Fara el nu se citeste nicio alta cifra.
  `--zgomot N`      podeaua. Aceeasi grila, cu C inlocuit de o coloana aleatoare, pe N seminte. Spune
                    cat scoate PROCEDURA cand semnalul nu contine nimic.
  conditia de limba Nicio limba stricata cu interval care exclude zero. Se citeste INAINTEA mediei.

Candidatul trebuie sa fi trecut intai `analysis_c_sanatate.py`: `gemma4-12b-4bit` produce o coloana C
cu surprisal mediu peste ln|V|, deci degenerata, si ea nu se masoara aici.

Rulare:
  python analysis_c_fuse.py --cand qwen3-8b-4bit
  python analysis_c_fuse.py --cand qwen3-8b-4bit --u-grid 0      # controlul de reproducere
  python analysis_c_fuse.py --cand qwen3-8b-4bit --zgomot 5      # podeaua de zgomot
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

FUZ = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
BARA = 0.0045
UGRID = np.round(np.arange(-0.30, 0.3001, 0.05), 2)


def _r(a, b):
    from scipy.stats import pearsonr
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def mix(zF, zC, u):
    return (1 - u) * zF + u * zC


def rulare(per, ugrid, n_boot=2000):
    """{limba: (zF, zC, y, ctx)} -> (tabel per limba, esantioane bootstrap pentru medie)."""
    from mlsp_common import boot_r_ci
    rows, boots = [], {"nou": [], "azi": []}
    for lg in sorted(per):
        zF, zC, y, ctx = per[lg]
        altele = [l2 for l2 in per if l2 != lg]
        curba = [float(np.mean([_r(mix(per[l2][0], per[l2][1], u), per[l2][2]) for l2 in altele]))
                 for u in ugrid]
        u = float(ugrid[int(np.argmax(curba))])
        p3 = mix(zF, zC, u)
        b1 = boot_r_ci(y, p3, ctx, n_boot=n_boot)
        b0 = boot_r_ci(y, zF, ctx, n_boot=n_boot)
        k = min(len(b1["boot"]), len(b0["boot"]))
        d = b1["boot"][:k] - b0["boot"][:k]
        rows.append(dict(lang=lg, n=len(y), n_ctx=b1["n_ctx"], u=u,
                         r_azi=b0["r"], r_nou=b1["r"], delta=b1["r"] - b0["r"],
                         d_lo=float(np.percentile(d, 2.5)), d_hi=float(np.percentile(d, 97.5)),
                         d_p=float((d > 0).mean()),
                         curba_min=min(curba), curba_max=max(curba),
                         latime=max(curba) - min(curba)))
        boots["nou"].append(b1["boot"][:k]); boots["azi"].append(b0["boot"][:k])
    t = pd.DataFrame(rows).set_index("lang")
    k = min(len(x) for x in boots["nou"])
    mn = np.mean([x[:k] for x in boots["nou"]], axis=0)
    ma = np.mean([x[:k] for x in boots["azi"]], axis=0)
    return t, mn, ma


def build(cand, dirs, seed=None, csv=None):
    """{limba: (zF, zC, y, ctx)}. `seed` != None inlocuieste C cu zgomot, pentru podea.

    `csv` citeste candidatul dintr-un fisier cu coloanele `lang, idx, C` in loc de dintr-un CSV de
    bake-off. E calea prin care intra candidati care nu sunt iesirea unui LLM, de pilda predictorul de
    reziduu din `analysis_shap_multi.py`. Alinierea ramane pe `idx`, aceeasi cheie.
    """
    from analysis_c_frontiera import load_c, zscore
    fz = pd.read_csv(FUZ)
    per = {}
    if csv is not None:
        dc = pd.read_csv(csv)
        cser = {cand: dc.set_index("idx")["C"]}
    else:
        cser = None if seed is not None else load_c(dirs)
    if cser is not None and cand not in cser:
        sys.exit(f"{cand!r} nu e in {dirs}; gasite: {sorted(cser)}")
    for lg, g in fz.groupby("lang", sort=True):
        if seed is None or csv is not None:
            raw = cser[cand].reindex(g["idx"].values).values.astype(float)
        else:
            # Zgomotul se genereaza per (samanta, limba), nu o data pentru tot: altfel o singura
            # realizare ar decide toate cele zece limbi si podeaua ar avea varianta unui singur numar.
            raw = np.random.default_rng(seed * 1000 + hash(lg) % 997).standard_normal(len(g))
        per[lg] = (zscore(g["p_fuz"].values), zscore(raw),
                   g["y"].values.astype(float), g["ctx"].values)
    return per


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cand", required=True, help="numele coloanei C, adica al modelului")
    ap.add_argument("--dir", action="append", default=None)
    ap.add_argument("--u-grid", dest="u_grid", default=None,
                    help="'0' reduce grila la {0}: controlul de reproducere")
    ap.add_argument("--c-csv", dest="c_csv", default=None,
                    help="citeste candidatul dintr-un CSV cu `lang, idx, C` in loc de bake-off")
    ap.add_argument("--zgomot", type=int, default=0, help="numarul de seminte pentru podea")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args(argv)
    dirs = a.dir or ["bakeoff_test_Text", "surprisal_test"]
    ugrid = np.array([0.0]) if a.u_grid == "0" else UGRID

    per = build(a.cand, dirs, csv=a.c_csv)
    t, mn, ma = rulare(per, ugrid, a.boot)
    d = mn - ma
    med_nou, med_azi = float(t["r_nou"].mean()), float(t["r_azi"].mean())
    stricate = t[(t["delta"] < 0) & (t["d_hi"] < 0)]

    L = [f"# Semnalul C ca al treilea termen: `{a.cand}`", "",
         f"Generat de `analysis_c_fuse.py`, directoare {dirs}, grila lui u "
         f"[{ugrid.min():+.2f}, {ugrid.max():+.2f}] cu {len(ugrid)} puncte. "
         f"Fuziunea de referinta e inghetata din `{os.path.basename(FUZ)}`.", "",
         "## Rezultatul pe test, cu u ales LOLO", "", "```",
         t[["n", "n_ctx", "u", "r_azi", "r_nou", "delta", "d_lo", "d_hi", "d_p",
            "latime"]].round(6).to_string(), "```", "",
         f"Media pe limbi: azi **{med_azi:.6f}**, cu C **{med_nou:.6f}**, diferenta "
         f"**{med_nou - med_azi:+.6f}**, interval PERECHE "
         f"[{np.percentile(d, 2.5):+.6f}, {np.percentile(d, 97.5):+.6f}], "
         f"P(>0) = {100 * (d > 0).mean():.1f}%.", "",
         "## Conditia care se citeste INAINTEA mediei", "",
         (f"**{len(stricate)} limbi stricate cu interval care exclude zero: "
          f"{sorted(stricate.index)}.**" if len(stricate) else
          "**Nicio limba stricata cu interval care exclude zero.**"), "",
         f"Fata de bara de +{BARA:.4f}: "
         f"**{'trece' if med_nou - med_azi >= BARA else 'NU trece'}**.", "",
         "## Cat de plat e criteriul", "",
         f"Latimea curbei lui u pe limbile de potrivire, adica r maxim minus r minim peste grila: "
         f"medie **{t['latime'].mean():.6f}**, interval "
         f"[{t['latime'].min():.6f}, {t['latime'].max():.6f}]. "
         f"u ales: {dict(t['u'].items())}.", ""]

    if a.zgomot:
        L += ["## Podeaua de zgomot", "",
              "Aceeasi grila si acelasi criteriu, cu C inlocuit de o coloana aleatoare. Spune cat "
              "scoate procedura cand semnalul nu contine nimic.", "", "```",
              "samanta   delta pe medie   u ales"]
        zs = []
        for s in range(1, a.zgomot + 1):
            pz = build(a.cand, dirs, seed=s)
            tz, mnz, maz = rulare(pz, ugrid, n_boot=200)
            dz = float(tz["r_nou"].mean() - tz["r_azi"].mean())
            zs.append(dz)
            L.append(f"{s:<9d} {dz:+.6f}        {sorted(set(tz['u']))}")
        L += ["```", "",
              f"Podeaua: medie **{np.mean(zs):+.6f}**, maxim **{np.max(zs):+.6f}** pe "
              f"{a.zgomot} seminte. Castigul peste podea al candidatului: "
              f"**{med_nou - med_azi - float(np.mean(zs)):+.6f}**.", ""]

    suf = "_ugrid0" if a.u_grid == "0" else ""
    t.to_csv(os.path.join(OUT, f"c3_{a.cand}{suf}.csv"))
    dest = os.path.join(OUT, f"e_c3_{a.cand}{suf}.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {dest}")

    if a.u_grid == "0":
        # Controlul de reproducere: cu u = 0 amestecul e literal z(p_fuz), deci r trebuie sa fie
        # bit cu bit cel al fuziunii adoptate. Se verifica AICI, nu se presupune in raport.
        fz = pd.read_csv(FUZ)
        rr = [_r(g["p_fuz"], g["y"]) for _, g in fz.groupby("lang", sort=True)]
        dd = np.abs(np.array(rr) - t["r_nou"].values).max()
        print(f"[control] |r_nou - r(p_fuz)| maxim pe limbi = {dd:.2e}  "
              f"-> {'TRECE' if dd < 1e-12 else 'PICA'}")
        return 0 if dd < 1e-12 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
