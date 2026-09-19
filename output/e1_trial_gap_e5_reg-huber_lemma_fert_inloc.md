# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:42:35 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4258 | [+0.3277, +0.5126] | 30 | 11 | +0.3841 | [-0.0123, +0.6642] | -0.0417 | [-0.4554, +0.2483] |
| de | 570 | 193 | +0.5835 | [+0.5206, +0.6394] | 23 | 11 | +0.8306 | [+0.6042, +0.9337] | +0.2470 | [+0.0051, +0.3702] |
| en | 570 | 190 | +0.7760 | [+0.7369, +0.8112] | 30 | 10 | +0.6322 | [+0.4128, +0.7971] | -0.1438 | [-0.3683, +0.0276] |
| es | 593 | 208 | +0.6904 | [+0.6486, +0.7277] | 30 | 10 | +0.6697 | [+0.3235, +0.8811] | -0.0207 | [-0.3624, +0.1978] |
| fil | 570 | 555 | +0.3995 | [+0.3273, +0.4664] | 30 | 30 | +0.5507 | [+0.2861, +0.7530] | +0.1512 | [-0.1197, +0.3668] |
| fr | 569 | 191 | +0.5317 | [+0.4681, +0.5925] | 30 | 11 | +0.2884 | [+0.0860, +0.4875] | -0.2433 | [-0.4554, -0.0425] |
| it | 570 | 192 | +0.6155 | [+0.5602, +0.6708] | 30 | 10 | +0.6031 | [+0.3634, +0.7882] | -0.0124 | [-0.2546, +0.1882] |
| ja | 570 | 190 | +0.5857 | [+0.5175, +0.6477] | 30 | 10 | +0.7268 | [+0.5329, +0.8590] | +0.1411 | [-0.0620, +0.2937] |
| pt | 567 | 562 | +0.7263 | [+0.6766, +0.7686] | 30 | 30 | +0.6991 | [+0.4873, +0.8511] | -0.0273 | [-0.2437, +0.1334] |
| si | 600 | 578 | +0.1860 | [+0.1168, +0.2550] | 30 | 30 | +0.3828 | [+0.1746, +0.6109] | +0.1968 | [-0.0224, +0.4407] |
| **medie** | | | **+0.5520** | | | | **+0.5767** | | **+0.0247** | |

**Δ split mediu +0.0247**, sd intre limbi 0.1561, interval -0.2433 pana la +0.2470. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3841 | +0.3841 | +0.0000 |
| de | +0.8306 | +0.8306 | +0.0000 |
| en | +0.6322 | +0.6322 | +0.0000 |
| es | +0.6697 | +0.6697 | +0.0000 |
| fil | +0.5507 | +0.5507 | +0.0000 |
| fr | +0.2884 | +0.2884 | +0.0000 |
| it | +0.6031 | +0.6031 | +0.0000 |
| ja | +0.7268 | +0.7268 | +0.0000 |
| pt | +0.6991 | +0.6991 | +0.0000 |
| si | +0.3828 | +0.3828 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4122 | +0.4120 | +0.0136 | -0.0279 |
| de | +0.6306 | +0.8378 | -0.0471 | -0.0072 |
| en | +0.7433 | +0.5374 | +0.0327 | +0.0948 |
| es | +0.6357 | +0.6235 | +0.0547 | +0.0462 |
| fil | +0.3963 | +0.5236 | +0.0032 | +0.0271 |
| fr | +0.5103 | +0.1580 | +0.0214 | +0.1304 |
| it | +0.5996 | +0.6356 | +0.0159 | -0.0325 |
| ja | +0.4878 | +0.6109 | +0.0979 | +0.1159 |
| pt | +0.7260 | +0.7212 | +0.0003 | -0.0221 |
| si | +0.1537 | +0.2127 | +0.0323 | +0.1701 |
