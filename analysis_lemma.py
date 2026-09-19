"""Cat aduce fixul de lema, limba cu limba, si daca efectul urmeaza bogatia morfologica.

Doua brate ale aceluiasi semnal A, deja pe disc, care difera printr-un singur lucru: frecventa e
`zipf(forma)` la unul si `max(zipf(forma), zipf(lema))` la celalalt. Embeddingul, regresorul, partitia
si semintele sunt identice, deci diferenta care iese e a fixului, nu a rularii.

Teza pe care o testeaza, contributia #3 a lucrarii: **castigul scaleaza cu bogatia morfologica**.
Predictia prespecificata e engleza ~0 si germana mult. Engleza e deci control, nu exceptie: daca iese
un Δ mare acolo, prima ipoteza e o eroare de aliniere, nu o descoperire.

Axa morfologica e **MSP, mean size of paradigm** (Xanthos si Gillis 2010), tipuri de forme impartit la
tipuri de leme. Nu e un indice propus de noi.

MSP creste cu marimea corpusului, iar corpusurile MLSP au intre 161 si 578 de propozitii per limba.
Un MSP brut ar masura deci si cate propozitii are limba in set. Se subesantioneaza la un numar comun
de tokeni, de mai multe ori, si se mediaza.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_lemma.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
BASE = os.path.join(OUT, "e1_frozen_preds.csv")
LEMMA = os.path.join(OUT, "e1_frozen_preds_lemma.csv")
PAIRS = os.path.join(OUT, "msp_pairs.csv")
LEMCSV = os.path.join(OUT, "lemmas_mlsp.csv")
REPORT = os.path.join(OUT, "e_lemma.md")

SEED = 42
N_BOOT = 2000
MSP_REPS = 200


def msp_table(seed=SEED, reps=MSP_REPS):
    """-> DataFrame [lang, msp, n_tok, n_forme, n_leme], la un numar comun de tokeni per limba."""
    d = pd.read_csv(PAIRS)
    if d.empty:
        raise SystemExit(f"{PAIRS} e gol. Ruleaza intai lemmatize_mlsp.py")
    n = int(d.groupby("lang").size().min())
    rng = np.random.default_rng(seed)
    rows = []
    for lg, g in d.groupby("lang", sort=True):
        f, l = g["form"].values, g["lemma"].values
        vals = []
        for _ in range(reps):
            k = rng.choice(len(g), n, replace=False)
            vals.append(len(set(f[k])) / max(len(set(l[k])), 1))
        rows.append((lg, float(np.mean(vals)), n, len(set(f)), len(set(l))))
    return pd.DataFrame(rows, columns=["lang", "msp", "n_tok", "n_forme", "n_leme"])


def delta_table(n_boot=N_BOOT):
    """-> DataFrame [lang, n, ctx, r_base, r_lemma, delta, lo, hi], bootstrap PERECHE pe contexte."""
    from mlsp_common import boot_r_ci
    if not os.path.exists(LEMMA):
        raise SystemExit(f"{LEMMA} lipseste. Ruleaza intai "
                         "finetune_xlmr.py --frozentrial --lemma-freq")
    a = pd.read_csv(BASE); b = pd.read_csv(LEMMA)
    a, b = (x[x["split"] == "test"].reset_index(drop=True) for x in (a, b))
    # Aceleasi randuri, in aceeasi ordine. Masca `okm` vine din embedding, pe care lema nu-l atinge,
    # deci egalitatea e asteptata; daca totusi difera, perechile de mai jos ar fi false si diferenta
    # n-ar mai fi a fixului.
    if not (a["idx"].equals(b["idx"]) and a["lang"].equals(b["lang"])):
        raise SystemExit("cele doua brate n-au aceleasi randuri: perechea nu se poate forma")

    rows = []
    for lg in sorted(a["lang"].unique()):
        m = (a["lang"] == lg).values
        y, ctx = a["complexity"].values[m], a["context_id"].values[m]
        pa, pb = a["p_multi"].values[m], b["p_multi"].values[m]
        # Acelasi seed si aceleasi contexte => `boot_r_ci` reesantioneaza IDENTIC pe ambele brate, deci
        # scaderea celor doua vectori de esantioane e un bootstrap pereche, fara a reesantiona o data.
        ba = boot_r_ci(y, pa, ctx, n_boot=n_boot, seed=SEED)
        bb = boot_r_ci(y, pb, ctx, n_boot=n_boot, seed=SEED)
        k = min(len(ba["boot"]), len(bb["boot"]))
        dd = bb["boot"][:k] - ba["boot"][:k]
        rows.append((lg, ba["n"], ba["n_ctx"], ba["r"], bb["r"], bb["r"] - ba["r"],
                     float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))))
    return pd.DataFrame(rows, columns=["lang", "n", "ctx", "r_base", "r_lemma", "delta", "lo", "hi"])


def report():
    from mlsp_common import freq_available
    from scipy.stats import pearsonr, spearmanr

    dl = delta_table()
    ms = msp_table()
    lem = pd.read_csv(LEMCSV, keep_default_na=False)
    lem = lem[lem["split"] == "test"]
    dif = lem.assign(d=(lem["lemma"].astype(str).str.lower().str.strip()
                        != lem["token"].astype(str).str.lower().str.strip())
                     & (lem["lemma"].astype(str).str.strip() != "")
                     ).groupby("lang")["d"].mean()

    d = dl.merge(ms, on="lang", how="left")
    d["dif"] = d["lang"].map(dif)
    d["freq"] = d["lang"].map(lambda l: freq_available(l))
    d.to_csv(os.path.join(OUT, "lemma_delta.csv"), index=False)

    # Corelatia se calculeaza DOAR pe limbile unde fixul se poate aplica. Includerea celor doua limbi
    # unde e no-op prin constructie ar adauga doua zerouri care nu masoara morfologie, ci absenta unui
    # lematizator, si ar umfla artificial orice corelatie pozitiva.
    ok = d[d["msp"].notna() & d["freq"]].dropna(subset=["delta"])
    rp = pearsonr(ok["msp"], ok["delta"]) if len(ok) > 2 else (float("nan"),) * 2
    rs = spearmanr(ok["msp"], ok["delta"]) if len(ok) > 2 else (float("nan"),) * 2

    L = ["# Fixul de lema pe limbile MLSP. Cat aduce, si daca urmeaza morfologia\n\n",
         f"Generat de `analysis_lemma.py`. Date brute: `output/lemma_delta.csv`.\n\n",
         "Cele doua brate difera printr-un singur lucru, frecventa formei fata de "
         "`max(forma, lema)`. Embedding, regresor, partitie si seminte identice.\n\n",
         f"Bootstrap **pereche** pe contexte, {N_BOOT} reesantionari, aceeasi reesantionare pe ambele "
         "brate. MSP e mediat peste "
         f"{MSP_REPS} subesantioane de cate {int(ms['n_tok'].iloc[0])} de tokeni per limba, "
         "numar comun ales ca minimul peste limbi.\n\n",
         "## Rezultatul\n\n",
         "| limba | n | ctx | MSP | tinte cu lema != forma | r fara lema | r cu lema | Δ | CI 95% |\n",
         "|---|---|---|---|---|---|---|---|---|\n"]
    for _, r in d.sort_values("msp", ascending=False, na_position="last").iterrows():
        msp = f"{r['msp']:.3f}" if pd.notna(r["msp"]) else "-"
        dd = f"{r['dif']*100:.0f}%" if pd.notna(r["dif"]) else "-"
        star = "**" if (r["lo"] > 0 or r["hi"] < 0) else ""
        L.append(f"| `{r['lang']}` | {r['n']} | {r['ctx']} | {msp} | {dd} | {r['r_base']:+.4f} | "
                 f"{r['r_lemma']:+.4f} | {star}{r['delta']:+.4f}{star} | "
                 f"[{r['lo']:+.4f}, {r['hi']:+.4f}] |\n")
    L.append(f"| **medie** | | | | | **{d['r_base'].mean():+.4f}** | **{d['r_lemma'].mean():+.4f}** "
             f"| **{d['delta'].mean():+.4f}** | |\n\n")
    L.append("Δ ingrosat = intervalul exclude zero.\n\n")

    L += ["## Teza morfologica\n\n",
          f"Pe cele {len(ok)} limbi unde fixul se poate aplica:\n\n",
          f"- Pearson intre MSP si Δ: **{rp[0]:+.3f}** (p = {rp[1]:.3f})\n",
          f"- Spearman: **{rs[0]:+.3f}** (p = {rs[1]:.3f})\n\n",
          f"La n = {len(ok)} nu se revendica semnificatie. Coeficientul se raporteaza cu punctele "
          "alaturi, iar cititorul vede singur cat de mult atarna fiecare limba.\n\n"]

    excl = d[~d["freq"] | d["msp"].isna()]
    if len(excl):
        L.append("## Limbile unde fixul nu se poate aplica\n\n")
        L.append("| limba | Δ masurat | motiv |\n|---|---|---|\n")
        for _, r in excl.iterrows():
            why = ("`wordfreq` nu serveste limba, deci `zipf_safe` intoarce indisponibil"
                   if not r["freq"] else "stanza nu are lematizator pentru limba")
            L.append(f"| `{r['lang']}` | {r['delta']:+.4f} | {why} |\n")
        L.append("\nΔ **nu** e zero acolo, si nu trebuie sa fie. Coloana lor de frecventa e identica bit "
                 "cu bit intre cele doua brate, verificat pe toate cele 1170 de randuri, deci fixul "
                 "chiar nu li se aplica. Dar sub LOLO modelul care prezice limba L se antreneaza pe "
                 "CELELALTE noua, ale caror trasaturi s-au schimbat. Ce se masoara la `fil` si `si` e "
                 "deci efectul indirect, prin datele de antrenare, si el e informativ tocmai fiindca "
                 "e curat de orice efect direct.\n\n")

    L.append("## Limitari\n\n")
    L.append(f"MSP e calculat pe propozitiile MLSP, {int(ms['n_tok'].iloc[0])} de tokeni per limba, nu "
             "pe treebank-uri UD. Pe un corpus mic MSP subestimeaza, iar subestimarea nu e la fel de "
             "mare pentru toate limbile. Cifra e deci un indice ordinal pentru clasarea limbilor, nu o "
             "constanta tipologica citabila in afara lucrarii.\n\n")
    L.append("Lemele vin de la stanza, deci sunt prezise, nu gold. Pe romana, unde lemele erau gold de "
             "la shared task, fixul a adus cel mai mare castig unic al lucrarii; o parte din diferenta "
             "fata de limbile de aici poate veni din calitatea lemelor, nu din morfologie.\n")

    with open(REPORT, "w", encoding="utf-8") as f:
        f.writelines(L)
    print(f"[lem] raport -> {REPORT}", flush=True)
    print(d.to_string(index=False))


if __name__ == "__main__":
    report()
