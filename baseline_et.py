# =============================================================================
# BASELINE MAI MARE fara resurse externe = EYE-TRACKING + surface self-sup.
# ET = datele competitiei (NU resursa externa; sugestia #1 Sergiu: "folositi intai ET, singura
# data etichetata la care aveti acces"). Mult peste surface-only (10.27) fiindca ET e proxy
# comportamental real de complexitate.
#
# Semnal = `et_complexity_proxy` (din data/X_test.csv) = suma ponderata a 8 metrici ET normalizate
# (TFT/RRT/FFD/RPD/TRC/FPFC/TFC/skip; ponderi literatura) => ET-ONLY, zero extern. Acoperire 95.1%.
# Cele ~78 randuri FARA ET: gap-fill self-supervised — Ridge pe trasaturi de suprafata -> tinta
# et_complexity_proxy (antrenat pe cele 1509 cu ET). Tinta = ET, trasaturi = string => ZERO resurse
# externe (fara CompLex/MLSP/wordfreq/embed/LLM).
#
# NU atinge solution_bert.py / baseline_surface.py. CPU, rapid. Calibrare clip(0.27+0.125*z,0,1).
# Limitare onesta: ET->complexitate NU se poate valida pe cele 14 etichete (doar 2 au ET) => proxy
# de adevar pt estimare = predictia best (exp_lemmafreq, 68.90).
# =============================================================================
import os
import sys
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from solution_bert import find_input, DATA, HERE, zscore, CALIB_MEAN, CALIB_STD
from baseline_surface import surface_features, fit_predict, write_submission


def main():
    test = pd.read_csv(find_input(["test_data.csv", "test_set.csv"]))
    if "datapointID" not in test.columns:
        test = test.reset_index().rename(columns={"index": "datapointID"})
    et = pd.read_csv(os.path.join(DATA, "X_test.csv"))[
        ["datapointID", "et_complexity_proxy", "has_et_features"]]
    df = test.merge(et, on="datapointID")

    surf = surface_features(list(df["token"]))
    proxy = df["et_complexity_proxy"].values.astype(float)
    mask = (df["has_et_features"] == 1).values & np.isfinite(proxy)
    n_et, n_gap = int(mask.sum()), int((~mask).sum())
    print(f"[ET] acoperire {n_et}/{len(df)} ({100*n_et/len(df):.1f}%) | gap-fill self-sup {n_gap} fara ET")

    # gap-fill self-supervised: surface -> et_complexity_proxy (tinta ET, fara etichete externe)
    signal = proxy.copy()
    if n_gap:
        signal[~mask] = fit_predict(surf[mask], proxy[mask], surf[~mask])

    ans = np.clip(CALIB_MEAN + CALIB_STD * zscore(signal), 0, 1)
    write_submission(df, ans, "exp_baseline_et.csv")

    # estimare onesta vs best (ET nevalidabil pe cele 14: doar 2 au ET)
    best = pd.read_csv(os.path.join(HERE, "output", "exp_lemmafreq.csv"))[["datapointID", "answer"]]
    m = df[["datapointID"]].assign(et_pred=ans).merge(best, on="datapointID")
    r_best = np.corrcoef(m["et_pred"], m["answer"])[0, 1]
    # contributie unica peste surface: corr et-proxy cu surface-pred (cat e ET dincolo de suprafata)
    surf_only = fit_predict(surf[mask], proxy[mask], surf)   # surface prezice proxy peste tot
    r_surf = np.corrcoef(zscore(signal), zscore(surf_only))[0, 1]
    print(f"\ncorr(ET-baseline, best 68.90) = {r_best:.3f}  (estimare; nu adevar)")
    print(f"corr(ET-signal, surface-pred-de-ET) = {r_surf:.3f}  => ET aduce semnal peste suprafata"
          f" (cu cat e mai mic, cu atat ET e mai independent de string)")

    print("\n================ ABLATIE no-external -> full ================")
    print("  (a) constant 0.27                : public ~0.00   (floor)")
    print("  (b) surface-only (CompLex/MLSP)  : public 10.27   (r~0.175)")
    print("  (c) ET + surface self-sup [ASTA] : SUBMITE output/exp_baseline_et.csv -> Y")
    print("  full system (resurse externe)    : public 68.90   (r~0.776)")
    print("=============================================================")


if __name__ == "__main__":
    main()
