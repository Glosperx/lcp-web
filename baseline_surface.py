# =============================================================================
# BASELINE FARA RESURSE EXTERNE (lower bound pentru raport).
# Cuantifica cat aduc resursele externe APROBATE (wordfreq, XLM-R, RoLlama3/surprisal,
# CompLex/MLSP ca semnal de transfer) peste niste trasaturi banale de suprafata.
# Solutia finala = 68.90; aici stabilim podeaua => ablatie floor -> surface-only -> 68.90.
#
# "Fara resurse externe" = ZERO wordfreq, ZERO embedding XLM-R, ZERO LLM/surprisal.
# Trasaturile sunt calculate DOAR din string-ul cuvantului tinta (lungime, silabe, consoane,
# vowel-ratio, majuscula, diacritice RO, sufix latinat). CompLex/MLSP raman doar ca ETICHETE de
# antrenare (substratul distant-supervision al proiectului), exact ca in solutia finala — singura
# diferenta fata de 68.90 e setul de trasaturi.
#
# Variante:
#   (a) constant = media calibrata 0.27  -> floor analitic score ~ 0 (Pearson nedefinit pe varianta
#       constanta, R2<=0). Scris pe disc, dar NU necesita submisie.
#   (b) regresie liniara (Ridge) doar pe trasaturi de suprafata, antrenata pe CompLex EN si MLSP
#       Romanic, prezisa zero-shot pe RO, ensemble 50/50, calibrata. -> submisie reala (user submite).
#   + free gate surface-only (transfer_eval EN<->MLSP) ca proxy onest fara etichete RO.
#
# NU atinge solution_bert.py => default-ul ramane bit-exact 68.90.
# Metrica oficiala: score = 50*(|Pearson| + max(0, R2)).
# Rulare (CPU, rapid):
#   TQDM_DISABLE=1 PYTHONIOENCODING=utf-8 python baseline_surface.py
# =============================================================================

import os
import sys
import glob
import urllib.request
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from solution_bert import (
    normalize_token, n_syllables, max_consonant_run, vowel_ratio, latinate_suffix,
    zscore, CALIB_MEAN, CALIB_STD, find_input, DATA, HERE, MLSP_LANGS, SEED,
)

# Diacritice romanesti (comma-below + cedila + majuscule). Pentru EN feature-ul e mereu 0 (constant)
# => Ridge ii da pondere ~0; pentru RO/romanic e informativ. Calculat identic pe toate limbile.
RO_DIACRITICS = set("ăâîșțĂÂÎȘȚşţŞŢ")

SURF_NAMES = ("len", "n_syllables", "max_consonant_run", "vowel_ratio",
              "capital", "n_diacritics", "latinate_suffix")


def surface_features(tokens):
    """Matrice Nx7 de trasaturi de suprafata, calculate DOAR din string (zero resurse externe)."""
    out = np.zeros((len(tokens), len(SURF_NAMES)), np.float32)
    for i, tok in enumerate(tokens):
        t = normalize_token(tok)
        if not t:
            continue
        out[i] = [
            len(t),
            n_syllables(t),
            max_consonant_run(t),
            vowel_ratio(t),
            1.0 if t[:1].isupper() else 0.0,
            sum(1 for ch in t if ch in RO_DIACRITICS),
            latinate_suffix(t),
        ]
    return out


# ----------------------------------------------------------------------------- loadere (FARA embed)
def load_complex_en_surface():
    """CompLex EN (descarca daca lipseste). -> (X_surface, y). Doar TSV + trasaturi, fara XLM-R."""
    en_dir = os.path.join(DATA, "complex_en"); os.makedirs(en_dir, exist_ok=True)
    base = "https://raw.githubusercontent.com/MMU-TDMLab/CompLex/master"
    files = {"train": "train/lcp_single_train.tsv", "trial": "trial/lcp_single_trial.tsv",
             "test": "test-labels/lcp_single_test.tsv"}
    dfs = []
    for k, rel in files.items():
        p = os.path.join(en_dir, f"lcp_single_{k}.tsv")
        if not os.path.exists(p):
            urllib.request.urlretrieve(f"{base}/{rel}", p)
        dfs.append(pd.read_csv(p, sep="\t").dropna(subset=["sentence", "token", "complexity"]))
    en = pd.concat(dfs, ignore_index=True)
    return surface_features(list(en["token"])), en["complexity"].values.astype(float)


def load_mlsp_surface():
    """MLSP/MultiLS Romance (gated). -> (X_surface, y) sau None daca data/mlsp/ lipseste."""
    mlsp_dir = os.path.join(DATA, "mlsp")
    if not os.path.isdir(mlsp_dir):
        return None
    dfs = []
    for f in glob.glob(os.path.join(mlsp_dir, "*.tsv")):
        x = pd.read_csv(f, sep="\t")
        if {"context", "target", "complexity"}.issubset(x.columns):
            dfs.append(x.rename(columns={"context": "sentence", "target": "token"}))
    if not dfs:
        return None
    ml = pd.concat(dfs, ignore_index=True)
    ml = ml[~ml["token"].astype(str).str.contains(" ", na=False)].reset_index(drop=True)
    return surface_features(list(ml["token"])), ml["complexity"].values.astype(float)


# ----------------------------------------------------------------------------- regresor liniar
def fit_predict(Xtr, ytr, Xpred):
    """Regresie LINIARA: StandardScaler + Ridge(alpha=1.0). Simpla, fara componenta neliniara."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    m = Pipeline([("s", StandardScaler()), ("r", Ridge(alpha=1.0, random_state=SEED))])
    m.fit(Xtr, ytr)
    return m.predict(Xpred)


def cv_r(X, y, k=5):
    """Pearson r prin K-fold in-sursa (proxy secundar)."""
    from sklearn.model_selection import KFold
    from scipy.stats import pearsonr
    pred = np.zeros(len(y))
    for tr, te in KFold(n_splits=k, shuffle=True, random_state=SEED).split(X):
        pred[te] = fit_predict(X[tr], y[tr], X[te])
    return pearsonr(pred, y)[0]


def write_submission(test, ans, name):
    out_dir = os.path.join(HERE, "output"); os.makedirs(out_dir, exist_ok=True)
    out = pd.DataFrame({"subtaskID": 1, "datapointID": test["datapointID"], "answer": ans})
    p = os.path.join(out_dir, name)
    out.to_csv(p, index=False)
    print(f"  scris {p}: {len(out)} randuri, mean={ans.mean():.3f} std={ans.std():.3f} "
          f"(NaN={int(np.isnan(ans).sum())})")
    return p


def main():
    from scipy.stats import pearsonr

    test_path = find_input(["test_data.csv", "test_set.csv"])
    if test_path is None:
        sys.exit("Nu gasesc test_set.csv")
    test = pd.read_csv(test_path)
    if "datapointID" not in test.columns:
        test = test.reset_index().rename(columns={"index": "datapointID"})
    if "text" not in test.columns and "sentence" in test.columns:
        test = test.rename(columns={"sentence": "text"})
    Xro = surface_features(list(test["token"]))

    # --- date de antrenare (doar etichete + trasaturi de suprafata) ---
    Xen, yen = load_complex_en_surface()
    mlsp = load_mlsp_surface()
    print(f"[date] CompLex EN: {len(yen)} | MLSP Romanic: {len(mlsp[1]) if mlsp else 0} | RO test: {len(test)}")

    # --- (a) constant = media calibrata 0.27 (floor analitic score ~ 0) ---
    print("\n[(a) constant 0.27]  floor analitic: predictor constant => Pearson nedefinit, R2<=0 => score ~ 0")
    ans_const = np.full(len(test), CALIB_MEAN, np.float32)
    write_submission(test, ans_const, "exp_baseline_const.csv")

    # --- (b) regresie liniara surface-only, antrenata pe CompLex+MLSP, zero-shot RO ---
    print("\n[(b) surface-only regression]  Ridge pe trasaturi de suprafata, ensemble EN+MLSP, calibrat")
    pred_en = fit_predict(Xen, yen, Xro)
    if mlsp is not None:
        Xml, yml = mlsp
        pred_ml = fit_predict(Xml, yml, Xro)
        xl_ens = 0.5 * zscore(pred_en) + 0.5 * zscore(pred_ml)
        print(f"  ensemble EN+MLSP (corr predictii RO = {np.corrcoef(pred_en, pred_ml)[0,1]:.3f})")
    else:
        xl_ens = zscore(pred_en)
        print("  ATENTIE: MLSP lipseste => doar-EN")
    ans_surf = np.clip(CALIB_MEAN + CALIB_STD * zscore(xl_ens), 0, 1)
    write_submission(test, ans_surf, "exp_baseline_surface.csv")

    # --- free gate surface-only (transfer EN<->MLSP), proxy onest fara etichete RO ---
    print("\n[free gate surface-only]  transfer_eval pe CompLex<->MLSP (proxy, ca in solution_bert)")
    if mlsp is not None:
        Xml, yml = mlsp
        r_en2ml = pearsonr(fit_predict(Xen, yen, Xml), yml)[0]
        r_ml2en = pearsonr(fit_predict(Xml, yml, Xen), yen)[0]
        t_avg = 0.5 * (r_en2ml + r_ml2en)
        cv_en, cv_ml = cv_r(Xen, yen), cv_r(Xml, yml)
        print(f"  EN->ML {r_en2ml:.4f} | ML->EN {r_ml2en:.4f} | transfer_avg {t_avg:.4f} | "
              f"cvEN {cv_en:.4f} | cvML {cv_ml:.4f}")
    else:
        t_avg = float("nan")
        print("  MLSP lipseste => gate indisponibil")

    # --- rezumat pentru raport ---
    print("\n================ REZUMAT ABLATIE (lower bound -> full) ================")
    print(f"  (a) constant 0.27                : score ~ 0.00   (floor analitic, fara submisie)")
    print(f"  (b) surface-only free-gate       : transfer_avg = {t_avg:.4f}   (vs full last4 base 0.5512)")
    print(f"      surface-only public          : SUBMITE output/exp_baseline_surface.csv -> Y")
    print(f"  full system (semnale externe)    : public 68.90")
    print("  => liftul resurselor externe (wordfreq + XLM-R + LLM + surprisal) = (68.90 - Y).")
    print("=======================================================================")


if __name__ == "__main__":
    main()
