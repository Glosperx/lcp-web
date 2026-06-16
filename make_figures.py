# Genereaza figurile pentru raport (regresie => NU AUC/PRC; folosim ablatie/curbe/corelatii).
import os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output", "raport"); os.makedirs(OUT, exist_ok=True)

# --- Fig 1: ablatie baseline -> full (scor public) ---
labels = ["constant\n0.27", "surface-only", "eye-tracking\n(date competitie)", "sistem complet\n(extern+LLM)"]
scores = [0.0, 10.27, 41.76, 68.90]
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(labels, scores, color=["#bbb", "#7aa6c2", "#5b9e6f", "#c2562a"])
for b, s in zip(bars, scores):
    ax.text(b.get_x() + b.get_width()/2, s + 1, f"{s:.2f}", ha="center", fontsize=10)
ax.set_ylabel("Scor public  (50·(|r| + max(0,R²)))")
ax.set_title("Ablatie: contributia surselor de semnal")
ax.set_ylim(0, 78)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_ablation.png"), dpi=150); plt.close(fig)

# --- Fig 2: curba ponderii surprisal (public) ---
w = [0.0, 0.08, 0.10, 0.12, 0.15, 0.20]
pub = [64.52, 64.81, 64.79, 64.71, 64.50, 63.84]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(w, pub, "-o", color="#c2562a")
ax.axvline(0.08, ls="--", color="gray", lw=1)
ax.annotate("varf w=0.08", (0.08, 64.81), textcoords="offset points", xytext=(20, -2), fontsize=9)
ax.set_xlabel("pondere surprisal (w)"); ax.set_ylabel("scor public")
ax.set_title("Calibrarea ponderii semnalului de surprisal")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_surprisal_curve.png"), dpi=150); plt.close(fig)

# --- Fig 3: corelatia metricilor ET cu complexitatea (IN proxy vs out) ---
p = os.path.join(HERE, "output", "extra_features", "et_metric_eval.csv")
if os.path.exists(p):
    d = pd.read_csv(p).sort_values("corr_vs_complex")
    colors = ["#5b9e6f" if v == "IN" else "#bbb" for v in d["in_proxy"]]
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.barh(d["metric"], d["corr_vs_complex"], color=colors)
    ax.set_xlabel("corelatie cu complexitatea (proxy)")
    ax.set_title("Metrici ET: semnal de complexitate (verde=in proxy, gri=exclus)")
    ax.axvline(0, color="k", lw=0.6)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_et_metrics.png"), dpi=150); plt.close(fig)

print("Figuri scrise in", OUT)
print(os.listdir(OUT))
