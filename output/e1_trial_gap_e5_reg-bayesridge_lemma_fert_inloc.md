# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:43:02 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4366 | [+0.3400, +0.5195] | 30 | 11 | +0.3885 | [+0.0465, +0.6480] | -0.0481 | [-0.4074, +0.2276] |
| de | 570 | 193 | +0.5783 | [+0.5166, +0.6346] | 23 | 11 | +0.8228 | [+0.6058, +0.9257] | +0.2446 | [+0.0219, +0.3648] |
| en | 570 | 190 | +0.7855 | [+0.7479, +0.8197] | 30 | 10 | +0.6713 | [+0.4073, +0.8616] | -0.1141 | [-0.3806, +0.0773] |
| es | 593 | 208 | +0.6945 | [+0.6506, +0.7331] | 30 | 10 | +0.6669 | [+0.3090, +0.8855] | -0.0276 | [-0.3810, +0.1996] |
| fil | 570 | 555 | +0.4156 | [+0.3429, +0.4811] | 30 | 30 | +0.5428 | [+0.2791, +0.7401] | +0.1272 | [-0.1465, +0.3356] |
| fr | 569 | 191 | +0.5341 | [+0.4726, +0.5956] | 30 | 11 | +0.3139 | [+0.0954, +0.5116] | -0.2202 | [-0.4496, -0.0130] |
| it | 570 | 192 | +0.6073 | [+0.5552, +0.6610] | 30 | 10 | +0.6134 | [+0.3563, +0.8065] | +0.0061 | [-0.2570, +0.2100] |
| ja | 570 | 190 | +0.5923 | [+0.5254, +0.6567] | 30 | 10 | +0.7321 | [+0.5472, +0.8600] | +0.1397 | [-0.0585, +0.2843] |
| pt | 567 | 562 | +0.7219 | [+0.6702, +0.7642] | 30 | 30 | +0.6831 | [+0.4721, +0.8378] | -0.0388 | [-0.2579, +0.1238] |
| si | 600 | 578 | +0.2144 | [+0.1505, +0.2819] | 30 | 30 | +0.3728 | [+0.1431, +0.5893] | +0.1584 | [-0.0932, +0.3882] |
| **medie** | | | **+0.5580** | | | | **+0.5808** | | **+0.0227** | |

**Δ split mediu +0.0227**, sd intre limbi 0.1420, interval -0.2202 pana la +0.2446. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3885 | +0.3885 | +0.0000 |
| de | +0.8228 | +0.8228 | +0.0000 |
| en | +0.6713 | +0.6713 | +0.0000 |
| es | +0.6669 | +0.6669 | +0.0000 |
| fil | +0.5428 | +0.5428 | +0.0000 |
| fr | +0.3139 | +0.3139 | +0.0000 |
| it | +0.6134 | +0.6134 | +0.0000 |
| ja | +0.7321 | +0.7321 | +0.0000 |
| pt | +0.6831 | +0.6831 | +0.0000 |
| si | +0.3728 | +0.3728 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4235 | +0.4704 | +0.0131 | -0.0819 |
| de | +0.6271 | +0.8368 | -0.0488 | -0.0140 |
| en | +0.7743 | +0.6062 | +0.0112 | +0.0651 |
| es | +0.6747 | +0.6519 | +0.0198 | +0.0150 |
| fil | +0.4128 | +0.5420 | +0.0028 | +0.0008 |
| fr | +0.5207 | +0.2379 | +0.0134 | +0.0760 |
| it | +0.6048 | +0.6702 | +0.0025 | -0.0568 |
| ja | +0.5079 | +0.6052 | +0.0844 | +0.1269 |
| pt | +0.7417 | +0.7152 | -0.0198 | -0.0321 |
| si | +0.2129 | +0.2863 | +0.0015 | +0.0865 |
