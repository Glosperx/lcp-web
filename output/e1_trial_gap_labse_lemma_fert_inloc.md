# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-19 01:12:51 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4728 | [+0.3964, +0.5436] | 30 | 11 | +0.3958 | [-0.0129, +0.7081] | -0.0770 | [-0.5006, +0.2434] |
| de | 570 | 193 | +0.6163 | [+0.5645, +0.6651] | 23 | 11 | +0.8249 | [+0.5434, +0.9362] | +0.2086 | [-0.0811, +0.3445] |
| en | 570 | 190 | +0.8131 | [+0.7796, +0.8431] | 30 | 10 | +0.7153 | [+0.5876, +0.8391] | -0.0978 | [-0.2242, +0.0325] |
| es | 593 | 208 | +0.6713 | [+0.6263, +0.7111] | 30 | 10 | +0.7023 | [+0.4647, +0.8523] | +0.0310 | [-0.2057, +0.1867] |
| fil | 570 | 555 | +0.3950 | [+0.3223, +0.4628] | 30 | 30 | +0.5433 | [+0.2927, +0.7492] | +0.1483 | [-0.1104, +0.3735] |
| fr | 569 | 191 | +0.5460 | [+0.4859, +0.6036] | 30 | 11 | +0.4885 | [+0.2307, +0.6826] | -0.0575 | [-0.3246, +0.1455] |
| it | 570 | 192 | +0.6149 | [+0.5630, +0.6661] | 30 | 10 | +0.7198 | [+0.5567, +0.8341] | +0.1049 | [-0.0643, +0.2376] |
| ja | 570 | 190 | +0.5282 | [+0.4527, +0.5962] | 30 | 10 | +0.6463 | [+0.3681, +0.8151] | +0.1181 | [-0.1765, +0.3005] |
| pt | 567 | 562 | +0.7647 | [+0.7248, +0.8001] | 30 | 30 | +0.7459 | [+0.5499, +0.8957] | -0.0187 | [-0.2192, +0.1334] |
| si | 600 | 578 | +0.3580 | [+0.2806, +0.4291] | 30 | 30 | +0.2604 | [-0.1639, +0.5983] | -0.0976 | [-0.5326, +0.2452] |
| **medie** | | | **+0.5780** | | | | **+0.6042** | | **+0.0262** | |

**Δ split mediu +0.0262**, sd intre limbi 0.1122, interval -0.0978 pana la +0.2086. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3958 | +0.3395 | -0.0563 |
| de | +0.8249 | +0.8083 | -0.0166 |
| en | +0.7153 | +0.7198 | +0.0045 |
| es | +0.7023 | +0.6865 | -0.0158 |
| fil | +0.5433 | +0.5587 | +0.0154 |
| fr | +0.4885 | +0.4861 | -0.0024 |
| it | +0.7198 | +0.7275 | +0.0077 |
| ja | +0.6463 | +0.6060 | -0.0403 |
| pt | +0.7459 | +0.7451 | -0.0008 |
| si | +0.2604 | +0.2825 | +0.0221 |

**Diferenta medie -0.0083**, interval -0.0563 pana la +0.0221.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4313 | +0.4211 | +0.0415 | -0.0253 |
| de | +0.6567 | +0.8861 | -0.0404 | -0.0612 |
| en | +0.8055 | +0.7044 | +0.0076 | +0.0109 |
| es | +0.6848 | +0.6430 | -0.0135 | +0.0593 |
| fil | +0.4061 | +0.5582 | -0.0111 | -0.0149 |
| fr | +0.5107 | +0.3288 | +0.0353 | +0.1597 |
| it | +0.6289 | +0.7304 | -0.0140 | -0.0106 |
| ja | +0.5791 | +0.5001 | -0.0509 | +0.1462 |
| pt | +0.7636 | +0.7735 | +0.0011 | -0.0276 |
| si | +0.2602 | +0.2633 | +0.0978 | -0.0029 |
