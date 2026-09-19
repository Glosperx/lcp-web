---
name: shap-signal-a-feature-importance
description: "29 aug 2026 - SHAP real (TreeSHAP+LinearSHAP) pe semnalul A: frecventa cuvantului si embeddingul sunt aproape la egalitate ca importanta, restul cu un ordin de marime mai mic; beeswarm-uri native in output/shap_beeswarm_native*.png"
metadata:
  node_type: memory
  type: project
  originSessionId: 61c4f607-25b4-4e50-9827-f13f53d75c5c
  modified: 2026-08-29T18:40:05.806Z
---

Continuarea lui [[rolcp-a-11a-limba-lolo]] in aceeasi sesiune. Alexandru a cerut un grafic SHAP de
feature importance pentru semnalul A, cu toate numele de trasaturi in engleza.

## Descoperire inainte de a incepe

`analysis_shap_multi.py` are deja un comentariu explicit care RESPINGE SHAP: "Kernel SHAP presupune
independenta si da explicatii gresite pe trasaturi dependente" (Aas, Jullum, Loland 2021), plus
"pachetul nu e instalat in ml_def". Verificat: `shap` 0.51.0 chiar E instalat acum. Dar obiectia
metodologica e specifica KERNEL SHAP; pentru modelul HGB (arbori) din blend, TreeSHAP calculeaza
valori Shapley EXACTE, fara presupunerea de independenta. Deci SHAP e defendabil aici, doar nu prin
Kernel SHAP.

## Ce s-a construit

Model: Ridge(alpha=300, in pipeline cu SimpleImputer+StandardScaler) + HGB(depth=3, lr=0.05,
max_iter=400, l2=1.0) - EXACT hiperparametrii din `solution_bert.blend_ridge_hgb` - antrenat pe tot
poolul de 11 limbi (fara protocol LOLO, fiindca scopul e interpretabilitate, nu evaluare). Trasaturi:
embedding xlmr-base centrat pe limba (768 dim) + fertilitate centrata + lexical cu `na_policy="mlsp"`
si lema (`max(zipf_forma, zipf_lema)`), lungimea scoasa (`--afeat fert_inloc`). Latime totala 774,
exact ca in sistemul adoptat.

SHAP = media TreeSHAP(HGB) + LinearExplainer(Ridge pe spatiul scalat) - exact, nu aproximare: Shapley
e liniar in functia de valoare, iar predictia blend E media celor doua predictii. Verificat numeric:
eroarea de reconstructie (suma SHAP + valoarea de baza vs predictia reala) e ~1e-15 pentru ambele.

Cele 768 de dimensiuni de embedding s-au ADUNAT per rand intr-o singura contributie de grup
("embedding"): valid, fiindca valorile SHAP sunt aditive, deci suma unei submultimi de coloane e
contributia combinata exacta a submultimii aia pentru randul respectiv.

## Rezultat (mean |SHAP value|)

```
feature                        toate 11 limbi   doar romana
word_frequency                      0.057           0.062
embedding (768 dim)                 0.055           0.061
frequency_unavailable (indicator)   0.033           0.017
is_capitalized                      0.016           0.022
num_subwords (fertilitate)          0.015           0.014
surface_features_unavailable        0.006           0.003
syllable_count                      0.003           0.004
```

Frecventa cuvantului si embeddingul sunt aproape la egalitate, cu o distanta clara fata de tot
restul. Pe romana, `is_capitalized` conteaza putin mai mult decat media, iar `frequency_unavailable`
mai putin (normal: wordfreq acopera complet romana, indicatorul e activ mai ales pe sinhaleza).

## Iteratia pe formatul graficului, cerut explicit de Alexandru

1. Prima incercare: bar chart CUSTOM, cu matplotlib, culori din skill-ul de dataviz. **Respins**:
   "nu asa arata un grafic shap".
2. A doua: `shap.plots.bar()` (nativ, cu comparatie de cohorte prin dictionar
   `{"All 11 languages": expl_all, "Romanian": expl_ro}`) plus `shap.plots.beeswarm()` pe cele 6
   trasaturi lexicale (embeddingul EXCLUS din beeswarm: n-are o singura valoare de colorat per
   punct). **Bar chart-ul tot respins** ("nu asa arata"), beeswarm-ul **acceptat explicit** ca fiind
   corect ("asa ar trebui sa arate").
3. Cerut in plus: titlu sus pe fiecare grafic, care sa spuna daca e pe romana sau pe media limbilor.

**Rezultat final, singurele fisiere pastrate:**
`output/shap_beeswarm_native.png/pdf` - titlu "All 11 languages, mean (n=7211)"
`output/shap_beeswarm_native_ro.png/pdf` - titlu "Romanian only (n=1587)"

Date brute pastrate pentru refolosire fara re-antrenare:
`output/shap_signalA_raw.npz` (valori SHAP + date + nume trasaturi + limba, per rand),
`output/shap_signalA_feature_importance.csv` (tabelul de mai sus).
Scripturile (nu in repo, doar in scratchpad-ul sesiunii):
`run_shap_signalA.py` (calculul), `plot_shap_native.py` (graficele).

**Why:** urmatoarea cerere de genul asta trebuie sa mearga direct la `shap.plots.beeswarm()`, nu la
un bar chart custom, chiar daca bar chart-ul respecta perfect ghidul de dataviz al proiectului -
pentru un grafic explicit numit "SHAP", forma oficiala a bibliotecii conteaza mai mult decat
consistenta vizuala cu restul graficelor. Vezi [[grafice-shap-native-nu-custom]] pentru regula
generala extrasa de aici.

**How to apply:** daca se cere alt grafic SHAP (alt semnal, alta limba, alt subset de trasaturi),
reia tiparul: TreeSHAP pentru arbori, LinearExplainer pentru liniar, media lor pentru blend,
`shap.plots.beeswarm()` doar pe trasaturile cu o valoare scalara reala per rand, titlu explicit sus.
