# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:28:50 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4426 | [+0.3640, +0.5161] | 30 | 11 | +0.3064 | [-0.2211, +0.7040] | -0.1362 | [-0.6639, +0.2738] |
| de | 570 | 193 | +0.6540 | [+0.6002, +0.7030] | 23 | 11 | +0.7970 | [+0.5352, +0.9066] | +0.1430 | [-0.1277, +0.2722] |
| en | 570 | 190 | +0.8173 | [+0.7798, +0.8490] | 30 | 10 | +0.7112 | [+0.4778, +0.8577] | -0.1061 | [-0.3421, +0.0467] |
| es | 593 | 208 | +0.6665 | [+0.6214, +0.7075] | 30 | 10 | +0.6972 | [+0.4000, +0.8602] | +0.0307 | [-0.2584, +0.1985] |
| fil | 570 | 555 | +0.4083 | [+0.3369, +0.4746] | 30 | 30 | +0.6081 | [+0.3786, +0.7770] | +0.1998 | [-0.0430, +0.3870] |
| fr | 569 | 191 | +0.5372 | [+0.4696, +0.5985] | 30 | 11 | +0.3429 | [-0.0495, +0.6518] | -0.1943 | [-0.5955, +0.1248] |
| it | 570 | 192 | +0.6301 | [+0.5759, +0.6846] | 30 | 10 | +0.6590 | [+0.4229, +0.8232] | +0.0288 | [-0.2149, +0.2040] |
| ja | 570 | 190 | +0.6011 | [+0.5381, +0.6556] | 30 | 10 | +0.5351 | [+0.3470, +0.6513] | -0.0661 | [-0.2656, +0.0613] |
| pt | 567 | 562 | +0.7621 | [+0.7218, +0.7984] | 30 | 30 | +0.8007 | [+0.6478, +0.9126] | +0.0386 | [-0.1197, +0.1551] |
| si | 600 | 578 | +0.2586 | [+0.1968, +0.3261] | 30 | 30 | -0.0624 | [-0.4829, +0.4468] | -0.3210 | [-0.7505, +0.1888] |
| **medie** | | | **+0.5778** | | | | **+0.5395** | | **-0.0383** | |

**Δ split mediu -0.0383**, sd intre limbi 0.1577, interval -0.3210 pana la +0.1998. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3064 | +0.2711 | -0.0353 |
| de | +0.7970 | +0.7896 | -0.0074 |
| en | +0.7112 | +0.6953 | -0.0159 |
| es | +0.6972 | +0.6848 | -0.0124 |
| fil | +0.6081 | +0.6063 | -0.0018 |
| fr | +0.3429 | +0.3070 | -0.0359 |
| it | +0.6590 | +0.6553 | -0.0037 |
| ja | +0.5351 | +0.5012 | -0.0339 |
| pt | +0.8007 | +0.7998 | -0.0009 |
| si | -0.0624 | -0.0114 | +0.0510 |

**Diferenta medie -0.0096**, interval -0.0359 pana la +0.0510.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4162 | +0.2369 | +0.0264 | +0.0695 |
| de | +0.6623 | +0.8200 | -0.0083 | -0.0230 |
| en | +0.8077 | +0.6797 | +0.0096 | +0.0315 |
| es | +0.6520 | +0.6824 | +0.0145 | +0.0148 |
| fil | +0.4149 | +0.5580 | -0.0066 | +0.0501 |
| fr | +0.5274 | +0.3432 | +0.0098 | -0.0003 |
| it | +0.6245 | +0.6814 | +0.0056 | -0.0224 |
| ja | +0.6004 | +0.4658 | +0.0007 | +0.0693 |
| pt | +0.7672 | +0.7801 | -0.0051 | +0.0206 |
| si | +0.2760 | -0.0210 | -0.0174 | -0.0414 |
