# =============================================================================
# Studiu eye-tracking ORTOGONAL (unghi cercetare).
# Intrebare: poarta semnalul ET informatie de complexitate DINCOLO de semnalele
# noastre ieftine (frecventa + cross-lingual + LLM + surprisal)? Care metrici ET
# (timpurii ~ acces lexical/frecventa vs tarzii ~ integrare/regresii) sunt ortogonale?
#
# NU atinge solutia de submisie. Doar citeste data/ + output/, scrie output/et_analysis/.
# Limitare cheie: doar 2/14 cuvinte etichetate au ET => nu se poate valida ET->complexitate
# pe ground-truth. Folosim predictia noastra (exp_surp_w08, public 64.81) ca PROXY de
# complexitate pe cele 1587 (acoperire ET 95%). Onest raportat.
# =============================================================================
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output", "et_analysis")
os.makedirs(OUT, exist_ok=True)


def _read(p):
    return pd.read_csv(os.path.join(DATA, p))


def residual(y, Z):
    """Rezidualul lui y dupa regresie liniara pe Z (cu intercept)."""
    y = np.asarray(y, float)
    Zc = np.column_stack([np.ones(len(Z)), np.asarray(Z, float)])
    beta, *_ = np.linalg.lstsq(Zc, y, rcond=None)
    return y - Zc @ beta


def pr(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan, int(m.sum())
    return float(pearsonr(a[m], b[m])[0]), int(m.sum())


def main():
    X = _read("X_test.csv")
    xl = _read("crosslingual_test.csv")          # datapointID, xl_complexity (semnal A)
    llm = _read("llm_complexity_test.csv")        # datapointID, llm_cx       (semnal B)
    surp = _read("surprisal_test.csv")            # datapointID, surp         (semnal C)
    pred = pd.read_csv(os.path.join(HERE, "output", "exp_surp_w08.csv"))[["datapointID", "answer"]]

    df = (X.merge(xl, on="datapointID").merge(llm, on="datapointID")
          .merge(surp, on="datapointID").merge(pred, on="datapointID"))

    FREQ, LEN = "zipf_best", "word_length"
    # Grupe ET (filtrate la coloanele prezente). Timpuriu ~ acces lexical; tarziu ~ integrare/regresii.
    EARLY = [c for c in ["FFD_mean_norm", "FPRT_mean_norm", "skip_rate_norm", "ffd_fprt_ratio_norm"]
             if c in df.columns]
    LATE = [c for c in ["RRT_mean_norm", "RPD_inc_norm", "TRC_in_mean_norm", "refixation_rate_norm",
                        "tft_per_fixation_norm"] if c in df.columns]
    OTHER = [c for c in ["TFT_mean_norm", "TFC_mean_norm", "FPFC_mean_norm", "TFT_std_norm",
                        "FFD_std_norm", "TFT_cv_norm"] if c in df.columns]
    ET_COLS = EARLY + LATE + OTHER
    GROUP = {**{c: "early" for c in EARLY}, **{c: "late" for c in LATE}, **{c: "other" for c in OTHER}}

    has_et = df["has_et_features"] == 1
    e = df[has_et].copy()
    ctrl = e[[FREQ, LEN]].values

    # ---- 1. Acoperire ET ----
    lines = []
    tot, nlbl = len(df), int(has_et.sum())
    lines.append(f"Acoperire ET pe test: {nlbl}/{tot} ({100*nlbl/tot:.1f}%) au fixatii.")
    noet = df[~has_et]
    lines.append(f"Cuvinte FARA ET (n={len(noet)}): zipf mediu {noet[FREQ].mean():.2f} vs {e[FREQ].mean():.2f} "
                 f"(cu ET); lungime {noet[LEN].mean():.2f} vs {e[LEN].mean():.2f}. "
                 f"=> ET lipseste sistematic la cuvinte mai frecvente/scurte (skipped) = bias de acoperire.")
    calib = _read("X_calib.csv")
    lines.append(f"GROUND-TRUTH: doar {int(calib['has_et_features'].sum())}/{len(calib)} cuvinte etichetate "
                 f"au ET => imposibil de validat ET->complexitate pe etichete reale. Folosim predictia "
                 f"(exp_surp_w08, public 64.81) ca proxy de complexitate pe cele {nlbl} cu ET.")
    with open(os.path.join(OUT, "coverage.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))

    # ---- 2. Matrice de corelatii ----
    cm_cols = (["et_complexity_proxy"] + ET_COLS + [FREQ, LEN,
               "xl_complexity", "llm_cx", "surp", "answer"])
    cm_cols = [c for c in cm_cols if c in e.columns]
    cm = e[cm_cols].astype(float).corr()
    cm.to_csv(os.path.join(OUT, "corr_matrix.csv"))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(11, 9))
        im = ax.imshow(cm.values, vmin=-1, vmax=1, cmap="RdBu_r")
        ax.set_xticks(range(len(cm_cols))); ax.set_xticklabels(cm_cols, rotation=90, fontsize=7)
        ax.set_yticks(range(len(cm_cols))); ax.set_yticklabels(cm_cols, fontsize=7)
        fig.colorbar(im); fig.tight_layout()
        fig.savefig(os.path.join(OUT, "corr_heatmap.png"), dpi=130)
        print("  heatmap -> output/et_analysis/corr_heatmap.png")
    except Exception as ex:
        print(f"  (matplotlib indisponibil: {ex}; sar figura, corr_matrix.csv scris)")

    # ---- 3. ET proxy vs frecventa/predictie ----
    r_proxy_freq, _ = pr(e["et_complexity_proxy"], e[FREQ])
    r_proxy_pred, _ = pr(e["et_complexity_proxy"], e["answer"])
    r_proxy_surp, _ = pr(e["et_complexity_proxy"], e["surp"])
    print(f"\net_complexity_proxy: corr cu zipf={r_proxy_freq:.3f}, cu predictia={r_proxy_pred:.3f}, "
          f"cu surprisal(C)={r_proxy_surp:.3f}")

    # ---- 4. Ortogonalitate per metrica ET (brut vs controlat pe zipf+lungime) ----
    rows = []
    pred_res = residual(e["answer"].values, ctrl)
    surp_res = residual(e["surp"].values, ctrl)
    for c in ["et_complexity_proxy"] + ET_COLS:
        raw_pred, n = pr(e[c], e["answer"])
        try:
            cres = residual(e[c].values, ctrl)
            ctrl_pred, _ = pr(cres, pred_res)
            ctrl_surp, _ = pr(cres, surp_res)
        except Exception:
            ctrl_pred = ctrl_surp = np.nan
        raw_surp, _ = pr(e[c], e["surp"])
        rows.append({"et_metric": c, "group": GROUP.get(c, "proxy"),
                     "corr_vs_pred_raw": round(raw_pred, 4),
                     "corr_vs_pred_ctrl_freqlen": round(ctrl_pred, 4),
                     "corr_vs_surprisalC_raw": round(raw_surp, 4),
                     "corr_vs_surprisalC_ctrl": round(ctrl_surp, 4), "n": n})
    orth = pd.DataFrame(rows)
    orth.to_csv(os.path.join(OUT, "et_orthogonality.csv"), index=False)
    print("\n--- Ortogonalitate ET (vs predictie, brut vs controlat pe zipf+lungime) ---")
    print(orth.to_string(index=False))

    # ---- 5. Agregat timpuriu vs tarziu ----
    agg = (orth[orth["group"].isin(["early", "late"])]
           .groupby("group")[["corr_vs_pred_raw", "corr_vs_pred_ctrl_freqlen",
                              "corr_vs_surprisalC_raw", "corr_vs_surprisalC_ctrl"]].mean().round(4))
    agg.to_csv(os.path.join(OUT, "et_early_vs_late.csv"))
    print("\n--- Timpuriu vs tarziu (medie pe grup) ---")
    print(agg.to_string())

    # ---- 6. Cele 14 etichete (ground-truth lexical; ET n=2 = doar mentiune) ----
    lab14 = []
    if "complexity" in calib.columns:
        r_zipf14, n14 = pr(calib[FREQ], calib["complexity"])
        lab14.append(f"Pe cele 14 etichete: corr(zipf, complexity)={r_zipf14:.3f} (n={n14}). "
                     f"corr(ET, complexity) NU se poate (doar 2 au ET).")
    with open(os.path.join(OUT, "ground_truth_14.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lab14) + "\n")

    # ---- summary.md (DOAR cifre/tabele; proza o scrie omul in LaTeX) ----
    def md(d, index=True):
        try:
            return d.to_markdown(index=index)
        except Exception:
            return "```\n" + d.to_string(index=index) + "\n```"
    with open(os.path.join(OUT, "summary.md"), "w", encoding="utf-8") as f:
        f.write("# Studiu ET ortogonal — cifre (proza o scrie omul, fara LLM)\n\n")
        f.write("## Acoperire\n" + "\n".join(lines) + "\n\n")
        f.write(f"## ET proxy\ncorr(et_proxy, zipf)={r_proxy_freq:.3f}; "
                f"corr(et_proxy, predictie)={r_proxy_pred:.3f}; corr(et_proxy, surprisalC)={r_proxy_surp:.3f}\n\n")
        f.write("## Ortogonalitate per metrica\n" + md(orth, index=False) + "\n\n")
        f.write("## Timpuriu vs tarziu\n" + md(agg) + "\n\n")
        f.write("## Ground-truth (14)\n" + "\n".join(lab14) + "\n")
    print("\nGata. Artefacte in output/et_analysis/ (coverage.txt, corr_matrix.csv, et_orthogonality.csv, "
          "et_early_vs_late.csv, summary.md).")


if __name__ == "__main__":
    main()
