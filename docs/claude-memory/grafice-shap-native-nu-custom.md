---
name: grafice-shap-native-nu-custom
description: "Un grafic cerut ca 'SHAP' trebuie generat cu shap.plots.* (beeswarm de preferat, nu bar), nu recreat cu matplotlib; fiecare grafic are titlu explicit despre scopul datelor (o limba vs media)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 61c4f607-25b4-4e50-9827-f13f53d75c5c
  modified: 2026-08-29T18:40:28.046Z
---

Descoperit in [[shap-signal-a-feature-importance]], 29 aug 2026. Am facut intai un bar chart de
feature importance CUSTOM (matplotlib, culori din skill-ul de dataviz), calculat corect din valori
SHAP reale (TreeSHAP+LinearSHAP). Alexandru l-a respins: "asta nu e un grafic shap ! trebuie shap
asa cum e in documentatia oficiala !". Am refacut cu `shap.plots.bar()` NATIV (tot respins) si
`shap.plots.beeswarm()` NATIV (acceptat explicit: "asa ar trebui sa arate").

**Why:** cand cineva cere explicit un grafic "SHAP" (nu doar "feature importance"), asteapta
semnatura vizuala a bibliotecii `shap` insasi - stilul roz/magenta, coloana "High/Low" pe dreapta,
formatul de beeswarm - nu o reinterpretare custom, chiar daca aceea respecta perfect un ghid de
design intern si e calculata identic din punct de vedere numeric. Identitatea vizuala a
bibliotecii conteaza mai mult decat consistenta cu restul graficelor proiectului, in cazul asta
specific.

**How to apply:**
- La orice cerere de "grafic SHAP": foloseste `shap.plots.beeswarm()` sau `shap.plots.bar()` din
  pachetul `shap`, nu o recreare manuala. Beeswarm pare preferatul implicit pentru feature
  importance (barul a fost respins de doua ori la rand); daca ambiguu, intreaba sau incepe cu
  beeswarm.
- Beeswarm cere o valoare scalara reala per rand de colorat (feature value); o trasatura agregata
  (ex: embedding de 768 dimensiuni sumat intr-un singur "feature") NU poate intra intr-un beeswarm -
  se exclude din el si se raporteaza separat (text sau alt grafic) daca importanta ei conteaza.
- `shap.plots.bar()` accepta un DICTIONAR de `shap.Explanation` pentru comparatie intre cohorte
  (ex: `{"All languages": expl_all, "Romanian": expl_ro}`) - util de stiut chiar daca in cazul asta
  bar-ul a fost respins oricum.
- Fiecare grafic livrat trebuie sa aiba titlu explicit sus, care sa spuna clar pe ce date e calculat
  (o singura limba, sau media/agregatul pe toate) - cerut explicit dupa ce primele grafice nu aveau
  aceasta distinctie vizibila.
- Regula probabil se generalizeaza si la alte "semnaturi vizuale de bibliotecă" cerute explicit pe
  nume (ex: un grafic "seaborn", un grafic "plotly") - verifica intai daca exista un modul de plot
  nativ al bibliotecii respective inainte sa recreezi manual stilul.
