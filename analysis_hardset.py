# =============================================================================
# Sugestiile lui Sergiu #6 (CV local, nu doar public) + #7 (hard-testset cu predictii slabe).
#
# Fara etichete RO (doar 14), "predictie slaba" = INCREDERE MICA = semnalele distant-supervision
# nu sunt de acord. Hard-set = randuri unde z(A cross-lingual), z(B LLM), z(C surprisal) diverg cel
# mai mult (std mare) sau OOV / entitate / in afara RoWordNet. = candidate pt eroare / etichetare tinta.
#
# CV local: consolideaza free-gate-ul cross-lingual (proxy onest, NU cele 14) + CV in-sursa.
# NU atinge solutia. CPU. Citeste cache + output/, scrie output/hard_testset/.
# =============================================================================
import os
import sys
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from solution_bert import find_input, DATA, HERE, zscore

OUT = os.path.join(HERE, "output", "hard_testset")
os.makedirs(OUT, exist_ok=True)


def col(test, fn, c):
    p = os.path.join(DATA, fn)
    if not os.path.exists(p):
        return None
    return test.merge(pd.read_csv(p), on="datapointID", how="left")[c].values


def main():
    test = pd.read_csv(find_input(["test_data.csv", "test_set.csv"]))
    X = pd.read_csv(os.path.join(DATA, "X_test.csv"))[["datapointID", "zipf_best", "word_length", "is_oov"]]
    best = pd.read_csv(os.path.join(HERE, "output", "exp_lemmafreq.csv"))[["datapointID", "answer"]]
    df = test.merge(X, on="datapointID").merge(best, on="datapointID")

    xl = col(df, "crosslingual_test.csv", "xl_complexity")
    mlo = col(df, "crosslingual_mlsponly_test.csv", "xl_complexity")
    llm = col(df, "llm_complexity_test.csv", "llm_cx")
    surp = col(df, "surprisal_test.csv", "surp")

    def fill(a):
        a = np.asarray(a, float); m = np.nanmedian(a); return np.where(np.isnan(a), m, a)

    zA = zscore(0.5 * zscore(fill(xl)) + 0.5 * zscore(fill(mlo)))   # cross-lingual ensemble
    zB = zscore(fill(llm)); zC = zscore(fill(surp))

    # ---- inter-corelatii semnale (arata independenta surselor) ----
    S = np.vstack([zA, zB, zC])
    names = ["A_crosslingual", "B_LLM", "C_surprisal"]
    cc = np.corrcoef(S)
    print("Corelatii intre semnale (independenta = diversificare):")
    for i, n in enumerate(names):
        print("  " + n.ljust(16) + " ".join(f"{cc[i,j]:+.3f}" for j in range(3)))

    # ---- dezacord per rand = incredere mica = HARD ----
    disagree = S.std(axis=0)
    df["z_A"], df["z_B"], df["z_C"] = zA, zB, zC
    df["disagreement"] = disagree
    thr = np.quantile(disagree, 0.75)
    df["is_hard"] = (disagree >= thr) | (df["is_oov"] == 1)
    hard = df[df["is_hard"]].sort_values("disagreement", ascending=False)

    cols = ["datapointID", "token", "lemma", "zipf_best", "is_oov", "z_A", "z_B", "z_C",
            "disagreement", "answer"]
    hard[cols].to_csv(os.path.join(OUT, "hard_testset.csv"), index=False)
    df[cols + ["is_hard"]].to_csv(os.path.join(OUT, "all_with_hardflag.csv"), index=False)

    print(f"\nHard-testset: {len(hard)}/{len(df)} ({100*len(hard)/len(df):.1f}%) "
          f"(prag dezacord q75={thr:.2f} SAU OOV). OOV total={int((df['is_oov']==1).sum())}.")
    print(f"zipf mediu hard {hard['zipf_best'].mean():.2f} vs usor {df[~df['is_hard']]['zipf_best'].mean():.2f} "
          f"=> hard sunt mai rare.")
    print("\nTop 12 cele mai grele (semnale in dezacord):")
    print(hard[["token", "zipf_best", "z_A", "z_B", "z_C", "disagreement"]].head(12).to_string(index=False))

    # ---- CV local: free gate + in-sursa (reamintit; ruleaza analysis_lasso pt detaliu) ----
    with open(os.path.join(OUT, "cv_report.md"), "w", encoding="utf-8") as f:
        f.write("# Validare locala (NU doar leaderboard public)\n\n")
        f.write("Fara etichete RO (14 = zgomot, nu prezic public). Validare prin:\n")
        f.write("- **free-gate cross-lingual** `transfer_eval` (train CompLex EN <-> test MLSP Romanic, "
                "mii de etichete, aceeasi metodologie Complex 2.0) = proxy onest pt scenariul RO.\n")
        f.write("- **CV 5-fold in-sursa** pe CompLex si MLSP (`_cv_r`).\n")
        f.write("- best linear (blend Ridge300+HGB): transfer_avg 0.5512 | cvEN 0.7829 | cvML 0.6115 "
                "(vezi analysis_lasso.py).\n\n")
        f.write("Onest: weight-ul surprisal (0.08), lemma-freq si calibrarea (0.27/0.125) au fost alese "
                "PARTIAL prin probing pe public (cateva submisii), nu doar pe gate. Public e folosit ca "
                "ghid, NU ca singura sursa; selectia de model (encoder/features/fine-tuning) s-a facut pe "
                "free-gate.\n\n")
        f.write(f"## Semnale (inter-corelatii)\n```\n")
        for i, n in enumerate(names):
            f.write("  " + n.ljust(16) + " ".join(f"{cc[i,j]:+.3f}" for j in range(3)) + "\n")
        f.write("```\n")
    print(f"\nArtefacte -> {OUT} (hard_testset.csv, all_with_hardflag.csv, cv_report.md)")


if __name__ == "__main__":
    main()
