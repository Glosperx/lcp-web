# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:36:11 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3807 | [+0.2927, +0.4609] | 30 | 11 | +0.0236 | [-0.3781, +0.3105] | -0.3571 | [-0.7665, -0.0595] |
| de | 570 | 193 | +0.5861 | [+0.5237, +0.6433] | 23 | 11 | +0.7834 | [+0.5488, +0.8884] | +0.1973 | [-0.0500, +0.3184] |
| en | 570 | 190 | +0.7396 | [+0.6913, +0.7798] | 30 | 10 | +0.5635 | [+0.3239, +0.7408] | -0.1760 | [-0.4127, +0.0079] |
| es | 593 | 208 | +0.6152 | [+0.5627, +0.6625] | 30 | 10 | +0.5474 | [+0.1913, +0.7551] | -0.0677 | [-0.4323, +0.1503] |
| fil | 570 | 555 | +0.3851 | [+0.3138, +0.4536] | 30 | 30 | +0.6054 | [+0.3986, +0.7538] | +0.2204 | [+0.0063, +0.3902] |
| fr | 569 | 191 | +0.4810 | [+0.4164, +0.5419] | 30 | 11 | +0.2713 | [-0.1939, +0.6537] | -0.2097 | [-0.6803, +0.1841] |
| it | 570 | 192 | +0.5917 | [+0.5355, +0.6448] | 30 | 10 | +0.5938 | [+0.3772, +0.8050] | +0.0021 | [-0.2262, +0.2212] |
| ja | 570 | 190 | +0.5839 | [+0.5209, +0.6430] | 30 | 10 | +0.5366 | [+0.3679, +0.6560] | -0.0473 | [-0.2281, +0.0839] |
| pt | 567 | 562 | +0.7314 | [+0.6875, +0.7706] | 30 | 30 | +0.7378 | [+0.5394, +0.8879] | +0.0064 | [-0.1965, +0.1620] |
| si | 600 | 578 | +0.2562 | [+0.1968, +0.3160] | 30 | 30 | +0.0610 | [-0.2928, +0.4843] | -0.1952 | [-0.5552, +0.2284] |
| **medie** | | | **+0.5351** | | | | **+0.4724** | | **-0.0627** | |

**Δ split mediu -0.0627**, sd intre limbi 0.1812, interval -0.3571 pana la +0.2204. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.0236 | +0.0236 | +0.0000 |
| de | +0.7834 | +0.7834 | +0.0000 |
| en | +0.5635 | +0.5635 | +0.0000 |
| es | +0.5474 | +0.5474 | +0.0000 |
| fil | +0.6054 | +0.6054 | +0.0000 |
| fr | +0.2713 | +0.2713 | +0.0000 |
| it | +0.5938 | +0.5938 | +0.0000 |
| ja | +0.5366 | +0.5366 | +0.0000 |
| pt | +0.7378 | +0.7378 | +0.0000 |
| si | +0.0610 | +0.0610 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3315 | +0.0753 | +0.0492 | -0.0517 |
| de | +0.6023 | +0.8402 | -0.0162 | -0.0568 |
| en | +0.7212 | +0.5790 | +0.0184 | -0.0155 |
| es | +0.5439 | +0.5177 | +0.0713 | +0.0297 |
| fil | +0.3951 | +0.4777 | -0.0100 | +0.1277 |
| fr | +0.4564 | +0.2580 | +0.0246 | +0.0133 |
| it | +0.5384 | +0.5487 | +0.0533 | +0.0451 |
| ja | +0.4749 | +0.3356 | +0.1090 | +0.2010 |
| pt | +0.7201 | +0.7505 | +0.0113 | -0.0127 |
| si | +0.1965 | +0.0032 | +0.0597 | +0.0578 |
