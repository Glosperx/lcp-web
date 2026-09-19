# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:55:57 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3691 | [+0.2921, +0.4432] | 30 | 11 | +0.4066 | [-0.1335, +0.7759] | +0.0375 | [-0.5019, +0.4318] |
| de | 570 | 193 | +0.6199 | [+0.5669, +0.6694] | 23 | 11 | +0.7786 | [+0.5312, +0.9096] | +0.1587 | [-0.0971, +0.2986] |
| en | 570 | 190 | +0.7968 | [+0.7567, +0.8311] | 30 | 10 | +0.6886 | [+0.4932, +0.8840] | -0.1082 | [-0.3079, +0.0876] |
| es | 593 | 208 | +0.6639 | [+0.6201, +0.7048] | 30 | 10 | +0.6824 | [+0.3967, +0.8606] | +0.0185 | [-0.2658, +0.2006] |
| fil | 570 | 555 | +0.4163 | [+0.3488, +0.4806] | 30 | 30 | +0.5648 | [+0.3127, +0.7785] | +0.1485 | [-0.1106, +0.3734] |
| fr | 569 | 191 | +0.5632 | [+0.4937, +0.6231] | 30 | 11 | +0.3112 | [-0.0342, +0.5949] | -0.2521 | [-0.6057, +0.0359] |
| it | 570 | 192 | +0.6024 | [+0.5468, +0.6588] | 30 | 10 | +0.7029 | [+0.5453, +0.8203] | +0.1005 | [-0.0731, +0.2338] |
| ja | 570 | 190 | +0.5561 | [+0.4918, +0.6131] | 30 | 10 | +0.5857 | [+0.4178, +0.7358] | +0.0296 | [-0.1477, +0.1946] |
| pt | 567 | 562 | +0.7560 | [+0.7174, +0.7936] | 30 | 30 | +0.7871 | [+0.5974, +0.9212] | +0.0311 | [-0.1591, +0.1677] |
| si | 600 | 578 | +0.2188 | [+0.1547, +0.2832] | 30 | 30 | -0.2176 | [-0.5455, +0.2027] | -0.4364 | [-0.7765, -0.0188] |
| **medie** | | | **+0.5563** | | | | **+0.5290** | | **-0.0272** | |

**Δ split mediu -0.0272**, sd intre limbi 0.1883, interval -0.4364 pana la +0.1587. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4066 | +0.3700 | -0.0366 |
| de | +0.7786 | +0.7460 | -0.0326 |
| en | +0.6886 | +0.6828 | -0.0058 |
| es | +0.6824 | +0.7010 | +0.0186 |
| fil | +0.5648 | +0.6145 | +0.0497 |
| fr | +0.3112 | +0.2983 | -0.0129 |
| it | +0.7029 | +0.6920 | -0.0109 |
| ja | +0.5857 | +0.5312 | -0.0545 |
| pt | +0.7871 | +0.7799 | -0.0072 |
| si | -0.2176 | -0.1001 | +0.1175 |

**Diferenta medie +0.0025**, interval -0.0545 pana la +0.1175.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3859 | +0.3059 | -0.0168 | +0.1007 |
| de | +0.6229 | +0.8167 | -0.0030 | -0.0381 |
| en | +0.8000 | +0.7302 | -0.0032 | -0.0416 |
| es | +0.6613 | +0.6680 | +0.0026 | +0.0144 |
| fil | +0.3994 | +0.5752 | +0.0169 | -0.0104 |
| fr | +0.5421 | +0.3526 | +0.0211 | -0.0414 |
| it | +0.6110 | +0.6962 | -0.0086 | +0.0067 |
| ja | +0.6009 | +0.5029 | -0.0448 | +0.0828 |
| pt | +0.7733 | +0.7315 | -0.0173 | +0.0556 |
| si | +0.2141 | -0.1882 | +0.0047 | -0.0294 |
