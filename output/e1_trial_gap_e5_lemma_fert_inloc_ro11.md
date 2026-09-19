# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-29 21:02:01 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4850 | [+0.4062, +0.5544] | 30 | 11 | +0.3900 | [-0.0094, +0.6933] | -0.0950 | [-0.4974, +0.2205] |
| de | 570 | 193 | +0.6347 | [+0.5772, +0.6895] | 23 | 11 | +0.8349 | [+0.6234, +0.9401] | +0.2002 | [-0.0258, +0.3263] |
| en | 570 | 190 | +0.8174 | [+0.7833, +0.8485] | 30 | 10 | +0.7233 | [+0.4678, +0.8612] | -0.0941 | [-0.3558, +0.0516] |
| es | 593 | 208 | +0.7229 | [+0.6828, +0.7572] | 30 | 10 | +0.7335 | [+0.4577, +0.8950] | +0.0105 | [-0.2610, +0.1768] |
| fil | 570 | 555 | +0.4094 | [+0.3386, +0.4759] | 30 | 30 | +0.5580 | [+0.2869, +0.7634] | +0.1486 | [-0.1340, +0.3715] |
| fr | 569 | 191 | +0.5406 | [+0.4782, +0.6007] | 30 | 11 | +0.3078 | [+0.0548, +0.5475] | -0.2328 | [-0.4974, +0.0111] |
| it | 570 | 192 | +0.6462 | [+0.5985, +0.6957] | 30 | 10 | +0.7004 | [+0.5117, +0.8347] | +0.0543 | [-0.1426, +0.2017] |
| ja | 570 | 190 | +0.5297 | [+0.4620, +0.5929] | 30 | 10 | +0.6663 | [+0.4096, +0.8364] | +0.1366 | [-0.1278, +0.3188] |
| pt | 567 | 562 | +0.7694 | [+0.7250, +0.8079] | 30 | 30 | +0.7769 | [+0.6134, +0.8890] | +0.0075 | [-0.1608, +0.1301] |
| ro | 1587 | 274 | +0.7044 | [+0.6704, +0.7370] | 0 | 0 | +nan | [+nan, +nan] | +nan | [+nan, +nan] |
| si | 600 | 578 | +0.1871 | [+0.1160, +0.2573] | 30 | 30 | +0.4253 | [+0.1553, +0.6431] | +0.2381 | [-0.0316, +0.4662] |
| **medie** | | | **+0.5861** | | | | **+0.6116** | | **+nan** | |

**Δ split mediu +nan**, sd intre limbi nan, interval +nan pana la +nan. Trial-ul e mai mare pe 7 din 11 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3900 | +0.3709 | -0.0191 |
| de | +0.8349 | +0.8325 | -0.0024 |
| en | +0.7233 | +0.7241 | +0.0008 |
| es | +0.7335 | +0.7313 | -0.0022 |
| fil | +0.5580 | +0.5740 | +0.0160 |
| fr | +0.3078 | +0.2960 | -0.0118 |
| it | +0.7004 | +0.7003 | -0.0001 |
| ja | +0.6663 | +0.6202 | -0.0461 |
| pt | +0.7769 | +0.7835 | +0.0066 |
| ro | +nan | +nan | +nan |
| si | +0.4253 | +0.4240 | -0.0013 |

**Diferenta medie +nan**, interval +nan pana la +nan.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4538 | +0.4062 | +0.0312 | -0.0162 |
| de | +0.6639 | +0.8565 | -0.0292 | -0.0216 |
| en | +0.8035 | +0.6785 | +0.0139 | +0.0448 |
| es | +0.6981 | +0.7092 | +0.0248 | +0.0243 |
| fil | +0.4103 | +0.5822 | -0.0009 | -0.0242 |
| fr | +0.5399 | +0.2438 | +0.0007 | +0.0640 |
| it | +0.6322 | +0.7140 | +0.0140 | -0.0136 |
| ja | +0.5707 | +0.6002 | -0.0410 | +0.0661 |
| pt | +0.7750 | +0.7505 | -0.0056 | +0.0264 |
| ro | +0.7110 | +nan | -0.0066 | +nan |
| si | +0.1854 | +0.2213 | +0.0017 | +0.2040 |
