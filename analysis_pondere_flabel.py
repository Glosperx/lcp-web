"""Se poate exploata un efect per limba fara selectie si fara etichete?

Intrebarea vine dintr-o cifra: pe sinhaleza LaBSE da +0.3580 fata de +0.2586 al lui XLM-R base, adica
+0.0994, cel mai mare efect de encoder din tot experimentul. Selectia LOLO a aruncat exact acel
castig (a ales e5, cel mai prost acolo) fiindca criteriul e de zece ori mai plat decat curba lui `w`.
Medierea, care a fost raspunsul corect, il dilueaza si ea.

Ideea testata: nu alegem si nu mediem uniform, ci PONDERAM membrii per limba, cu o pondere care nu se
uita la nicio eticheta. Trei candidati de pondere, toti masurabili fara `y`:

  fert    fertilitatea tokenizerului modelului pe limba respectiva. Un model care sparge limba in
          multe bucati probabil o reprezinta mai prost. Zero inferenta, doar tokenizerul.
  zipf    corelatia predictiilor membrului cu MINUS frecventa, in interiorul limbii. Frecventa e cel
          mai bun predictor unic al complexitatii, deci un membru care o urmareste mai bine e probabil
          mai bun. Foloseste doar trasaturi, nu etichete.
  acord   corelatia medie a membrului cu ceilalti membri. Un membru care se abate de la consens e ori
          mai bun ori mai prost; se masoara in ce directie.

Poarta metodologica, din lectia sesiunii trecute: o pondere care prezice bine pe MEDIA limbilor nu
autorizeaza o procedura care alege PER LIMBA. Validarea e deci pe cele 3 x 10 = 30 de puncte
individuale, nu pe medii.

Rulare, ~30 secunde, zero inferenta:
  python analysis_pondere_flabel.py
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

MEMBRI = {"xlmr": "", "labse": "_labse", "e5": "_e5"}
TOKENIZERE = {"xlmr": "xlm-roberta-base", "labse": "sentence-transformers/LaBSE",
              "e5": "intfloat/multilingual-e5-base"}


def zin(v):
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std()


def main():
    from solution_bert import normalize_token
    from mlsp_common import zipf_safe, load_tail_freq
    from transformers import AutoTokenizer

    frames = {}
    for k, suf in MEMBRI.items():
        d = pd.read_csv(os.path.join(OUT, f"e1_frozen_preds{suf}_lemma_fert_inloc.csv"))
        frames[k] = d[d["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)
    ref = frames["xlmr"]
    langs = sorted(ref["lang"].unique())

    # frecventa: cu tabelul de coada incarcat, ca proxy-ul sa existe SI pe sinhaleza
    load_tail_freq("subword")
    zipf = np.array([zipf_safe(normalize_token(str(t)), lg)[0]
                     for t, lg in zip(ref["token"], ref["lang"])], float)

    toks = {k: AutoTokenizer.from_pretrained(v) for k, v in TOKENIZERE.items()}
    fert = {k: np.array([len(t.tokenize(" " + normalize_token(str(x)))) for x in ref["token"]], float)
            for k, t in toks.items()}

    rows = []
    for lg in langs:
        m = (ref["lang"] == lg).values
        y = ref.loc[m, "complexity"].values.astype(float)
        Z = {k: zin(frames[k].loc[m, "p_multi"].values) for k in MEMBRI}
        for k in MEMBRI:
            altii = [Z[j] for j in MEMBRI if j != k]
            rows.append(dict(
                lang=lg, membru=k,
                r_adevarat=pearsonr(Z[k], y)[0],                       # ce vrem sa prezicem
                fert=float(fert[k][m].mean()),
                zipf=pearsonr(Z[k], -zipf[m])[0] if np.std(zipf[m]) > 0 else np.nan,
                acord=float(np.mean([pearsonr(Z[k], a)[0] for a in altii]))))
    T = pd.DataFrame(rows)

    L = ["# Ponderare per limba fara etichete", "",
         "Generat de `analysis_pondere_flabel.py`. Zero inferenta.", "",
         "## Cei trei candidati de pondere, langa calitatea adevarata", "",
         "```", T.set_index(["lang", "membru"]).round(4).to_string(), "```", ""]

    # --- validarea, si se face PE LIMBA, nu pe medie
    L += ["## Prezic ceva? Validare pe limba, nu pe medie", "",
          "Trei niveluri, si numai al treilea autorizeaza o procedura care alege per limba:", ""]
    val = []
    for prox in ("fert", "zipf", "acord"):
        pool = T.dropna(subset=[prox])
        r_pool = pearsonr(pool[prox], pool["r_adevarat"])[0]
        # in interiorul limbii: prezice ORDINEA membrilor?
        inner = []
        for lg in langs:
            g = T[(T["lang"] == lg)].dropna(subset=[prox])
            if len(g) > 2 and g[prox].nunique() > 1:
                inner.append(spearmanr(g[prox], g["r_adevarat"]).statistic)
        # pe medii peste limbi
        mn = T.groupby("membru")[[prox, "r_adevarat"]].mean()
        val.append(dict(pondere=prox, pe_medii=pearsonr(mn[prox], mn["r_adevarat"])[0],
                        pooled_30=r_pool, in_limba_spearman=float(np.nanmean(inner)),
                        n_limbi_utile=len(inner)))
    V = pd.DataFrame(val).set_index("pondere")
    L += ["```", V.round(4).to_string(), "```", "",
          "`pe_medii` e corelatia peste cei 3 membri, dupa mediere pe limbi: 3 puncte, deci nu "
          "inseamna nimic singura. `pooled_30` e peste toate cele 30 de perechi (limba, membru). "
          "**`in_limba_spearman` e cifra care conteaza**: cat de bine ordoneaza ponderea membrii "
          "INAUNTRUL unei limbi, mediat peste limbi. O procedura care alege per limba are nevoie "
          "exact de asta.", ""]

    # --- cazul care a motivat intrebarea
    si = T[T["lang"] == "si"].set_index("membru")
    L += ["## Cazul care a pus intrebarea: sinhaleza", "", "```", si.round(4).to_string(), "```", ""]
    best_true = si["r_adevarat"].idxmax()
    for prox, sens in (("fert", "min"), ("zipf", "max"), ("acord", "min")):
        pick = si[prox].idxmin() if sens == "min" else si[prox].idxmax()
        L += [f"- pondere `{prox}` (sens {sens}) ar alege **{pick}**; adevaratul castigator e "
              f"**{best_true}**. {'NIMERESTE' if pick == best_true else 'greseste'}."]
    L += [""]

    # --- ponderarea efectiva, cu exponentul ales LOLO
    L += ["## Ponderarea efectiva, cu exponentul ales LOLO", "",
          "Ponderea unui membru pe limba L e `p_i ∝ exp(beta * s_i)`, unde `s_i` e proxy-ul "
          "standardizat in interiorul limbii. `beta = 0` e medierea uniforma de acum. `beta` se alege "
          "leave-one-language-out, ca orice alt hiperparametru.", ""]
    GRID = np.round(np.arange(-2.0, 2.01, 0.25), 2)
    rez = []
    for prox, semn in (("fert", -1.0), ("zipf", +1.0), ("acord", -1.0)):
        # r al mediei ponderate, per limba, pentru fiecare beta
        R = {}
        for lg in langs:
            m = (ref["lang"] == lg).values
            y = ref.loc[m, "complexity"].values.astype(float)
            Z = np.column_stack([zin(frames[k].loc[m, "p_multi"].values) for k in MEMBRI])
            s = T[(T["lang"] == lg)].set_index("membru").loc[list(MEMBRI), prox].values * semn
            if not np.isfinite(s).all() or np.std(s) == 0:
                s = np.zeros(len(s))
            else:
                s = (s - s.mean()) / s.std()
            R[lg] = [pearsonr(Z @ (np.exp(b * s) / np.exp(b * s).sum()), y)[0] for b in GRID]
        # alegerea LOLO a lui beta
        vals, betas = [], []
        for lg in langs:
            crit = np.mean([R[l2] for l2 in langs if l2 != lg], axis=0)
            b = int(np.argmax(crit))
            betas.append(GRID[b]); vals.append(R[lg][b])
        i0 = int(np.where(GRID == 0.0)[0][0])
        rez.append(dict(pondere=prox, r_uniform=np.mean([R[l][i0] for l in langs]),
                        r_ponderat=float(np.mean(vals)), beta_mediu=float(np.mean(betas)),
                        r_oracol=float(np.mean([max(R[l]) for l in langs]))))
    P = pd.DataFrame(rez).set_index("pondere")
    P["castig_A"] = P["r_ponderat"] - P["r_uniform"]
    L += ["```", P.round(6).to_string(), "```", "",
          "`r_uniform` e medierea de acum (beta = 0). `r_oracol` foloseste etichetele limbii tinute "
          "deoparte, deci e un plafon, nu o optiune.", ""]

    dest = os.path.join(OUT, "e_pondere_flabel.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
