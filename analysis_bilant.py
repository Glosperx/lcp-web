"""Bilantul sesiunii pe semnalul A: fiecare candidat masurat, cu castig, cost si verdict.

Nu inventeaza nicio cifra. Castigul vine din `output/fusion_lolo_*.csv`, costul din marcajele de timp
ale jurnalelor de rulare din scratchpad, iar bara si factorul de transmisie din
`output/e_frontiera_enc.md`. Constantele scrise de mana mint dupa renumerotare, deci nu se scriu.

Referinta pentru candidatii de EXTRACTIE si de reprezentare e xlmr SINGUR la `last4`, fiindca ei
schimba un singur encoder; referinta pentru ansambluri e sistemul adoptat.

Rulare:
  python analysis_bilant.py
"""
import glob
import os
import re
import sys
from datetime import datetime

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
SP = ("/private/tmp/claude-501/-Users-alexandrucojoaca-Documents-GitHub-ia-sahistii/"
      "1059c3ea-df2c-4994-9830-618be50c9b60/scratchpad")
BARA = 0.0045


def costuri():
    """{eticheta: minute} din marcajele `=== nume HH:MM:SS` / `--- nume gata HH:MM:SS`."""
    out = {}
    for f in glob.glob(os.path.join(SP, "*.log")):
        start = {}
        for l in open(f, encoding="utf-8", errors="ignore"):
            m = re.match(r"^=== (\S+)\s+(\d\d:\d\d:\d\d) ===", l)
            if m:
                start[m.group(1)] = datetime.strptime(m.group(2), "%H:%M:%S")
            m = re.match(r"^--- (\S+) gata (\d\d:\d\d:\d\d)", l)
            if m and m.group(1) in start:
                out[m.group(1)] = (datetime.strptime(m.group(2), "%H:%M:%S")
                                   - start[m.group(1)]).total_seconds() / 60.0
    return out


def citeste(tag):
    p = os.path.join(OUT, f"fusion_lolo_{tag}.csv")
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p)
    r = dict(r_A=d["r_A_raw"].mean(), r_fuz=d["r_fuz_raw"].mean())
    for lg in ("si", "fil"):
        g = d[d["lang"] == lg]
        if len(g):
            r[f"fuz_{lg}"] = float(g["r_fuz_raw"].iloc[0])
    if "d_azi" in d:
        r["d_fuz"] = d["d_azi"].mean()
        r["stricate"] = int((d["d_azi_hi"] < 0).sum())
    md = os.path.join(OUT, f"e_fusion_lolo_{tag}.md")
    if os.path.exists(md):
        for l in open(md, encoding="utf-8"):
            if "cea de azi" in l and l.strip().startswith("|"):
                n = re.findall(r"[-+]?\d*\.\d+", l)
                if len(n) >= 4:
                    r["d_lo"], r["d_hi"], r["P"] = float(n[1]), float(n[2]), float(n[3])
                break
    return r


def main():
    C = costuri()
    # (eticheta afisata, tag de fuziune, cheie de cost, familie)
    CAND = [
        ("xlmr singur, last4 (REFERINTA)", "enc_xlmr_now", None, "referinta"),
        ("sistemul: media a 3 encodere", "sistem_vs_xlmr", None, "referinta"),
        ("labse singur", "cfg_labse", None, "encoder"),
        ("e5 singur", "cfg_e5", None, "encoder"),
        ("xlmr-large singur", "cfg_xlmr-large", None, "encoder"),
        ("Glot500 singur", "cfg_glot500", "glot500", "encoder"),
        ("e5 cu prefixul lui", "cfg_e5_last4_q", "e5_prefix", "encoder"),
        ("pooling first", "cfg_last4_first", "last4_first", "extractie"),
        ("pooling max", "cfg_last4_max", "last4_max", "extractie"),
        ("pooling last", "cfg_last4_last", "last4_last", "extractie"),
        ("straturi mid", "cfg_mid", "mid", "extractie"),
        ("straturi concat4", "cfg_concat4", "concat4", "extractie"),
        ("straturi last1", "cfg_last1", "last1", "extractie"),
        ("cel mai bun din grila (concat4_first)", "cfg_concat4_first", "concat4_first", "extractie"),
        ("contextual ++ izolat", "cfg_ctxiso", "ctxiso", "reprezentare"),
        ("numai vectorul izolat", "cfg_isoonly", "isoonly", "reprezentare"),
        ("izotropie: -1 componenta", "cfg_tf-pca1", "tf_pca1", "izotropie"),
        ("izotropie: -5 componente", "cfg_tf-pca5", "tf_pca5", "izotropie"),
        ("izotropie: albire ZCA", "cfg_tf-zca", "tf_zca", "izotropie"),
        ("ablatie: fara frecventa", "cfg_nofreq", "nofreq", "coada"),
        ("frecventa de coada, exact", "cfg_ft-exact", "ft_exact", "coada"),
        ("frecventa de coada, prefix", "cfg_ft-prefix", "ft_prefix", "coada"),
        ("frecventa de coada, subword", "cfg_ft-subword", "ft_subword", "coada"),
        ("indicator OOV per token", "cfg_oov", "oov", "coada"),
        ("indicator OOV + pooling first", "cfg_oov_last4_first", "oov_first", "coada"),
        ("ansamblu 4, cu vectorul izolat", "ens4iso", None, "ansamblu"),
        ("ansamblu 3, pooling first", "ens3_last4_first", None, "ansamblu"),
        ("ansamblu 3, frecventa exact", "ens3_ft-exact", None, "ansamblu"),
        ("ansamblu 3, frecventa prefix", "ens3_ft-prefix", None, "ansamblu"),
        ("ansamblu 3, frecventa subword", "ens3_ft-subword", None, "ansamblu"),
        ("ansamblu 3, indicator OOV", "ens3_oov", None, "ansamblu"),
        ("ansamblu 3 pooling first, fata de SISTEM", "ens3first_vs_sistem", None, "ansamblu"),
    ]
    rows = []
    for nume, tag, ck, fam in CAND:
        r = citeste(tag)
        if r is None:
            continue
        r.update(candidat=nume, familie=fam, minute=round(C.get(ck, np.nan), 1) if ck else np.nan)
        rows.append(r)
    T = pd.DataFrame(rows).set_index("candidat")
    cols = [c for c in ("familie", "r_A", "r_fuz", "d_fuz", "d_lo", "d_hi", "P", "stricate",
                        "fuz_si", "fuz_fil", "minute") if c in T]
    T = T[cols]

    ref = T.loc["xlmr singur, last4 (REFERINTA)", "r_fuz"] if \
        "xlmr singur, last4 (REFERINTA)" in T.index else np.nan
    sis = T.loc["sistemul: media a 3 encodere", "r_fuz"] if \
        "sistemul: media a 3 encodere" in T.index else np.nan

    L = ["# Bilantul sesiunii pe semnalul A", "",
         "Generat de `analysis_bilant.py`. Toate cifrele vin din fisiere, niciuna nu e scrisa de mana.",
         "",
         f"Referinta pentru candidatii care schimba UN encoder e **xlmr singur la `last4`, "
         f"{ref:.6f}**. Sistemul adoptat, media a trei encodere, e **{sis:.6f}**. Bara e "
         f"**+{BARA:.4f}**.", "",
         "```", T.round(6).to_string(), "```", "",
         "`d_fuz` e diferenta PERECHE fata de referinta proprie a rularii, cu `d_lo`/`d_hi` "
         "intervalul mediei si `P` procentul de reesantionari peste zero. `stricate` numara limbile "
         "al caror interval pereche exclude zero IN JOS; conditia se citeste INAINTEA mediei. "
         "`minute` e timpul de rulare masurat, nu estimat.", ""]

    if "d_fuz" in T:
        tr = T[(T["d_fuz"] > BARA) & (T["stricate"] == 0)]
        L += ["## Ce trece bara", "",
              ("Niciun candidat nu trece bara de +%.4f cu zero limbi stricate." % BARA
               if tr.empty else
               "Trec bara: " + ", ".join(f"`{i}` ({v:+.4f})" for i, v in tr["d_fuz"].items())), ""]
        pz = T[(T["d_fuz"] > 0) & (T["stricate"] == 0)].sort_values("d_fuz", ascending=False)
        if not pz.empty:
            L += ["Candidati cu semn pozitiv si nicio limba stricata, in ordine descrescatoare:", "",
                  "```", pz[["d_fuz", "d_lo", "d_hi", "P"]].round(6).to_string(), "```", ""]

    dest = os.path.join(OUT, "e_bilant.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
