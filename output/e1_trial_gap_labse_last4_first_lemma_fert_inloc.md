# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:05:02 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4716 | [+0.3957, +0.5426] | 30 | 11 | +0.4011 | [+0.0174, +0.7016] | -0.0704 | [-0.4691, +0.2392] |
| de | 570 | 193 | +0.6184 | [+0.5647, +0.6687] | 23 | 11 | +0.8188 | [+0.5528, +0.9329] | +0.2004 | [-0.0602, +0.3354] |
| en | 570 | 190 | +0.8114 | [+0.7762, +0.8413] | 30 | 10 | +0.7462 | [+0.5808, +0.8559] | -0.0652 | [-0.2320, +0.0496] |
| es | 593 | 208 | +0.6787 | [+0.6339, +0.7170] | 30 | 10 | +0.6522 | [+0.3814, +0.8190] | -0.0266 | [-0.3039, +0.1478] |
| fil | 570 | 555 | +0.3932 | [+0.3199, +0.4604] | 30 | 30 | +0.5215 | [+0.2627, +0.7303] | +0.1283 | [-0.1440, +0.3558] |
| fr | 569 | 191 | +0.5565 | [+0.4952, +0.6140] | 30 | 11 | +0.4646 | [+0.1808, +0.6684] | -0.0919 | [-0.3899, +0.1255] |
| it | 570 | 192 | +0.6150 | [+0.5640, +0.6671] | 30 | 10 | +0.7206 | [+0.5499, +0.8393] | +0.1056 | [-0.0688, +0.2389] |
| ja | 570 | 190 | +0.5077 | [+0.4304, +0.5782] | 30 | 10 | +0.6232 | [+0.3414, +0.7951] | +0.1155 | [-0.1789, +0.3010] |
| pt | 567 | 562 | +0.7705 | [+0.7323, +0.8047] | 30 | 30 | +0.7549 | [+0.5525, +0.9008] | -0.0156 | [-0.2159, +0.1341] |
| si | 600 | 578 | +0.3469 | [+0.2762, +0.4132] | 30 | 30 | +0.2167 | [-0.2193, +0.5797] | -0.1302 | [-0.5685, +0.2403] |
| **medie** | | | **+0.5770** | | | | **+0.5920** | | **+0.0150** | |

**Δ split mediu +0.0150**, sd intre limbi 0.1128, interval -0.1302 pana la +0.2004. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4011 | +0.3516 | -0.0495 |
| de | +0.8188 | +0.8025 | -0.0163 |
| en | +0.7462 | +0.7421 | -0.0041 |
| es | +0.6522 | +0.6480 | -0.0042 |
| fil | +0.5215 | +0.5566 | +0.0351 |
| fr | +0.4646 | +0.4392 | -0.0254 |
| it | +0.7206 | +0.7156 | -0.0050 |
| ja | +0.6232 | +0.5852 | -0.0380 |
| pt | +0.7549 | +0.7638 | +0.0089 |
| si | +0.2167 | +0.2602 | +0.0435 |

**Diferenta medie -0.0055**, interval -0.0495 pana la +0.0435.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4313 | +0.4495 | +0.0403 | -0.0484 |
| de | +0.6563 | +0.8788 | -0.0379 | -0.0600 |
| en | +0.8012 | +0.7063 | +0.0102 | +0.0399 |
| es | +0.6882 | +0.5986 | -0.0095 | +0.0536 |
| fil | +0.4027 | +0.5422 | -0.0095 | -0.0207 |
| fr | +0.5093 | +0.3735 | +0.0472 | +0.0911 |
| it | +0.6266 | +0.7255 | -0.0116 | -0.0049 |
| ja | +0.5717 | +0.4828 | -0.0640 | +0.1404 |
| pt | +0.7650 | +0.7767 | +0.0055 | -0.0218 |
| si | +0.2722 | +0.2364 | +0.0747 | -0.0197 |
