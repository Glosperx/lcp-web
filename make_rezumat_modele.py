"""Jurnalul configuratiilor masurate, `output/e_rezumat_modele.csv`, generat din artefactele de pe disc.

**De ce nu mai e tinut de mana.** A fost, si a ramas in urma tacut de fiecare data: pe 18 august
arata 0.6646 ca maxim in timp ce pe disc existau deja 0.6720 si 0.6696, iar la P11 toate cele 84 de
randuri au devenit istorice deodata, fiindca `n` s-a schimbat. Un jurnal care ramane in urma e mai
rau decat niciun jurnal, fiindca il citesti crezand ca stii ce s-a masurat. Acum se regenereaza, si
`analysis_audit_jurnal.py` ramane ca verificare incrucisata.

Ce scrie, o linie per artefact si per componenta:

  fuziune         media lui `r_fuz_raw` din `output/fusion_lolo_*.csv`
  brat A          media lui `r_A_raw` din acelasi tabel, adica semnalul A dupa `w_src`
  brat inghetat   r al lui `p_multi` per limba din `output/e1_frozen_preds*.csv`, mediat

Pentru fiecare fuziune se calculeaza si diferenta PERECHE fata de sistemul adoptat, prin
`mlsp_common.boot_r_ci` pe contexte, ca sa se vada dintr-o privire care configuratie chiar difera de
el si care e in zgomot. Coloana `stare` marcheaza sistemul adoptat si configuratia cu r maxim, iar
cele doua **nu sunt aceeasi**: adoptata e cea cu trei encodere, maxima e cea cu patru, iar diferenta
dintre ele nu se distinge de zero.

Fuziunile se filtreaza la `n` curent: una pe alt `n` n-ar fi comparabila si diferenta pereche n-ar
avea sens. Bratele inghetate mai vechi se pastreaza chiar daca sunt pe `n` vechi, fiindca sunt ablatii
de trasaturi inca informative, dar primesc marcaj in `stare` si `n_itemi` le arata. Jurnalul complet
de dinainte de P11 e `output/e_rezumat_modele_pre-p11_n5606.csv`.

Rulare, ~40 de secunde:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python make_rezumat_modele.py
"""
import glob
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
DEST = os.path.join(OUT, "e_rezumat_modele.csv")
ADOPTAT = "fusion_preds_lolo_adoptat.csv"
N_BOOT = 2000

# tag -> (model B, descrierea metodei). Ce nu e aici primeste tagul ca descriere.
ETICHETE = {
    "ens": ("gemma4-12b-4bit + qwen35-9b-8bit",
            "xlmr + nota 1-5 + lema + ansamblu + fertilitate (w pe test)"),
    "picktest": ("gemma4-12b-4bit",
                 "xlmr + nota 1-5 + lema + ansamblu + fertilitate (w si model pe test)"),
    "encmean": ("gemma4-12b-4bit + qwen35-9b-8bit",
                "media a patru encodere + nota 1-5 + lema + ansamblu + fertilitate (w pe test)"),
    "encmean3": ("gemma4-12b-4bit + qwen35-9b-8bit",
                 "media a trei encodere fara xlmr-large + nota 1-5 + lema + ansamblu + fertilitate "
                 "(w pe test)"),
    "adoptat": ("gemma4-12b-4bit",
                "media a trei encodere fara xlmr-large + nota 1-5 + lema + ansamblu + fertilitate "
                "(w si model pe test)"),
    "encmean4_picktest": ("gemma4-12b-4bit",
                          "media a patru encodere + nota 1-5 + lema + ansamblu + fertilitate "
                          "(w si model pe test)"),
    "enc": ("gemma4-12b-4bit + qwen35-9b-8bit",
            "encoder ales LOLO per limba + nota 1-5 + lema + ansamblu + fertilitate (w pe test)"),
}
for _e in ("xlmr", "labse", "e5", "xlmr-large"):
    ETICHETE[f"encmean-fara-{_e}"] = (
        "gemma4-12b-4bit + qwen35-9b-8bit",
        f"media a trei encodere fara {_e} + nota 1-5 + lema + ansamblu + fertilitate (w pe test)")
    ETICHETE[f"ens_{_e}"] = (
        "gemma4-12b-4bit + qwen35-9b-8bit",
        f"{_e} singur + nota 1-5 + lema + ansamblu + fertilitate (w pe test)")


def _boot(preds, langs):
    """Distributia bootstrap a mediei pe limbi, plus r per limba, pe randuri aliniate."""
    from mlsp_common import boot_r_ci
    B, R = [], []
    for lg in langs:
        g = preds[preds["lang"] == lg].drop_duplicates("idx").sort_values("idx")
        b = boot_r_ci(g["y"].values, g["p_fuz"].values, g["ctx"].values, n_boot=N_BOOT)
        B.append(b["boot"]); R.append(b["r"])
    m = min(len(x) for x in B)
    return float(np.mean(R)), np.vstack([x[:m] for x in B]).mean(axis=0)


def main():
    ref_p = os.path.join(OUT, ADOPTAT)
    if not os.path.exists(ref_p):
        raise SystemExit(f"{ref_p} lipseste: fara sistemul adoptat nu se pot calcula diferentele")
    ref = pd.read_csv(ref_p)
    langs = sorted(ref["lang"].unique())
    r_ref, M_ref = _boot(ref, langs)   # punctul estimat, nu media distributiei bootstrap

    rows = []
    for p in sorted(glob.glob(os.path.join(OUT, "fusion_lolo_*.csv"))):
        b = os.path.basename(p)
        if b.startswith("fusion_preds_"):
            continue
        t = pd.read_csv(p)
        if "n" not in t.columns or "r_fuz_raw" not in t.columns:
            continue
        n = int(t["n"].sum())
        tag = b[len("fusion_lolo_"):-len(".csv")]
        pp = os.path.join(OUT, f"fusion_preds_lolo_{tag}.csv")
        if not os.path.exists(pp):
            continue
        pr = pd.read_csv(pp)
        if len(pr) != len(ref):
            continue                       # alt `n`, deci nu se compara si nu intra
        model, metoda = ETICHETE.get(tag, ("", tag))
        r, M = _boot(pr, langs)
        d = M - M_ref
        ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))
        acelasi = tag == "adoptat"
        rows.append({"data": ts, "componenta": "fuziune", "model": model, "metoda": metoda,
                     "artefact": b, "split": "test", "selectie": "LOLO", "n_limbi": len(t),
                     "n_itemi": n, "r_mediu": round(r, 6),
                     "d_vs_adoptat": 0.0 if acelasi else round(r - r_ref, 6),
                     "ci_lo": "" if acelasi else round(float(np.percentile(d, 2.5)), 4),
                     "ci_hi": "" if acelasi else round(float(np.percentile(d, 97.5)), 4),
                     "p_gt0": "" if acelasi else round(float((d > 0).mean()), 3), "stare": ""})
        rows.append({"data": ts, "componenta": "brat A", "model": "",
                     "metoda": "bratul A al configuratiei de mai sus", "artefact": b,
                     "split": "test", "selectie": "LOLO", "n_limbi": len(t), "n_itemi": n,
                     "r_mediu": round(float(t["r_A_raw"].mean()), 6), "d_vs_adoptat": "",
                     "ci_lo": "", "ci_hi": "", "p_gt0": "", "stare": ""})

    for p in sorted(glob.glob(os.path.join(OUT, "e1_frozen_preds*.csv"))):
        d = pd.read_csv(p)
        if not {"lang", "p_multi", "complexity", "split"} <= set(d.columns):
            continue
        d = d[d["split"] == "test"]
        if len(d) != len(ref) + 0 and len(d) != int(ref.groupby("lang").size().sum()):
            pass                            # brațul A are toate randurile, fuziunea le are pe cele evaluate
        rs = [np.corrcoef(g["p_multi"], g["complexity"])[0, 1] for _, g in d.groupby("lang")
              if len(g) > 2 and g["p_multi"].std() > 0]
        if not rs:
            continue
        rows.append({"data": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p))),
                     "componenta": "brat inghetat", "model": "",
                     "metoda": f"p_multi, {os.path.basename(p)}", "artefact": os.path.basename(p),
                     "split": "test", "selectie": "", "n_limbi": len(rs), "n_itemi": len(d),
                     "r_mediu": round(float(np.mean(rs)), 6), "d_vs_adoptat": "", "ci_lo": "",
                     "ci_hi": "", "p_gt0": "", "stare": ""})

    j = pd.DataFrame(rows)
    # Aceeasi configuratie poate exista sub doua taguri: `encmean3` si `encmean-fara-xlmr-large`
    # sunt aceeasi rulare, cerute de doua analize diferite. In jurnal e o singura configuratie, cu
    # ambele artefacte listate, altfel ar parea ca s-a masurat de doua ori.
    cheie = ["componenta", "metoda", "r_mediu"]
    art = j.groupby(cheie, sort=False)["artefact"].apply(lambda v: ", ".join(sorted(set(v))))
    j = j.drop_duplicates(cheie, keep="first").set_index(cheie)
    j["artefact"] = art
    j = j.reset_index()
    j = j[["data", "componenta", "model", "metoda", "artefact", "split", "selectie", "n_limbi",
           "n_itemi", "r_mediu", "d_vs_adoptat", "ci_lo", "ci_hi", "p_gt0", "stare"]]
    fuz = j[j["componenta"] == "fuziune"]
    if len(fuz):
        j.loc[fuz["r_mediu"].idxmax(), "stare"] = "r MAXIM masurat"
        idx_ad = fuz.index[fuz["artefact"] == "fusion_lolo_adoptat.csv"]
        if len(idx_ad):
            i = idx_ad[0]
            j.loc[i, "stare"] = ("ADOPTAT si r maxim" if j.loc[i, "stare"] == "r MAXIM masurat"
                                 else "ADOPTAT, raportat")
    n_max = int(j["n_itemi"].max())
    vechi = (j["n_itemi"] != n_max) & (j["stare"] == "")
    j.loc[vechi, "stare"] = j.loc[vechi, "n_itemi"].map(
        lambda v: f"n vechi ({v}), ablatie neactualizata, NU se compara")
    ordine = {"fuziune": 0, "brat A": 1, "brat inghetat": 2}
    j = j.sort_values(["componenta", "r_mediu"], key=lambda c: c.map(ordine) if c.name == "componenta"
                      else -c.astype(float), kind="stable")
    j.to_csv(DEST, index=False)
    print(f"[jurnal] {len(j)} de randuri, {len(fuz)} configuratii de fuziune, "
          f"n = {int(j['n_itemi'].max())}")
    for r in j[j["stare"] != ""].itertuples():
        print(f"[jurnal] {r.stare}: {r.r_mediu:.6f}  {r.artefact}")
    print(f"-> {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
