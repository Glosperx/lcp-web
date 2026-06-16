# =============================================================================
# Genereaza candidatii de SUBMIS pe public pentru semnalul D (eye-tracking).
# Sweep: 2 forme ET (PCA reading_effort vs proxy ponderat manual) x 3 ponderi de fuziune.
# Scopul: free-gate-ul NU poate testa ET => doar public-ul decide daca al 4-lea semnal ajuta peste 68.90.
# Toate variantele impart EXACT acelasi scor de baza (3 semnale = 68.90); difera doar forma+ponderea ET.
#
# Refoloseste functiile din solutie_finala.py (importabil, nu ruleaza nimic la import).
# Output: output/et_{pca,manual}_w{05,10,20}.csv  (3 coloane: subtaskID, datapointID, answer)
#
# Rulare:  python make_et_candidates.py
# =============================================================================
import os
import numpy as np
import pandas as pd

from solutie_finala import (HERE, DATA, citeste_semnale_cache, semnal_et,
                            semnal_et_manual, combina_semnale)

WEIGHTS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]   # grila fina; et_pca_w10=69.66 public (+0.76 vs 68.90)
BASELINE = os.path.join(HERE, "output", "exp_lemmafreq.csv")   # 68.90 (3 semnale, W_ET=0)


def main():
    out_dir = os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)

    test = pd.read_csv(os.path.join(DATA, "test_set.csv"))
    if "text" not in test.columns and "sentence" in test.columns:
        test = test.rename(columns={"sentence": "text"})

    A_en, A_mlsp, B_llm, C_surp = citeste_semnale_cache(test)   # semnalele A/B/C din cache (CPU)
    forme = {"pca": semnal_et(test), "manual": semnal_et_manual(test)}

    base = None
    if os.path.exists(BASELINE):
        base = pd.read_csv(BASELINE).sort_values("datapointID")["answer"].values

    print(f"\n{'fisier':28s} {'media':>6s} {'std':>6s} {'corr_68.90':>11s} {'randuri>0.01':>13s}")
    print("-" * 70)
    rezumat = []
    for forma, et in forme.items():
        if et is None:
            print(f"[atentie] forma '{forma}' indisponibila (lipseste data/X_test.csv) — sar")
            continue
        for w in WEIGHTS:
            ans = combina_semnale(A_en, A_mlsp, B_llm, C_surp, et=et, w_et=w)
            name = f"et_{forma}_w{int(round(w*100)):02d}.csv"
            pd.DataFrame({"subtaskID": 1, "datapointID": test["datapointID"], "answer": ans}).to_csv(
                os.path.join(out_dir, name), index=False)
            if base is not None:
                aligned = pd.DataFrame({"datapointID": test["datapointID"], "a": ans}).sort_values(
                    "datapointID")["a"].values
                corr = float(np.corrcoef(aligned, base)[0, 1])
                changed = int((np.abs(aligned - base) > 0.01).sum())
            else:
                corr, changed = float("nan"), -1
            print(f"{name:28s} {ans.mean():6.3f} {ans.std():6.3f} {corr:11.4f} {changed:13d}")
            rezumat.append((name, w, forma, corr, changed))

    print("\nBaseline 68.90 (W_ET=0, 3 semnale) = output/exp_lemmafreq.csv")
    print("Submite candidatii pe public, noteaza scorurile, alege forma+pondere care bate 68.90 CLAR.")
    print("Reminder: finalele se dau pe PRIVATE => ET intr-un final doar daca castigul public e peste zgomot.")


if __name__ == "__main__":
    main()
