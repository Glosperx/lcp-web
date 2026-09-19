# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:33:43 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3921 | [+0.3014, +0.4798] | 30 | 11 | +0.4760 | [+0.1620, +0.7209] | +0.0838 | [-0.2420, +0.3478] |
| de | 570 | 193 | +0.5231 | [+0.4576, +0.5826] | 23 | 11 | +0.7300 | [+0.5480, +0.8689] | +0.2069 | [+0.0154, +0.3626] |
| en | 570 | 190 | +0.7561 | [+0.7172, +0.7920] | 30 | 10 | +0.6204 | [+0.4379, +0.8001] | -0.1358 | [-0.3231, +0.0504] |
| es | 593 | 208 | +0.6753 | [+0.6287, +0.7161] | 30 | 10 | +0.6697 | [+0.3374, +0.8857] | -0.0056 | [-0.3363, +0.2180] |
| fil | 570 | 555 | +0.3649 | [+0.2960, +0.4320] | 30 | 30 | +0.4101 | [+0.0951, +0.6542] | +0.0451 | [-0.2676, +0.3048] |
| fr | 569 | 191 | +0.5193 | [+0.4562, +0.5829] | 30 | 11 | +0.2735 | [-0.0546, +0.5495] | -0.2458 | [-0.5799, +0.0356] |
| it | 570 | 192 | +0.5525 | [+0.4969, +0.6105] | 30 | 10 | +0.6261 | [+0.3702, +0.8203] | +0.0736 | [-0.1899, +0.2828] |
| ja | 570 | 190 | +0.5105 | [+0.4356, +0.5833] | 30 | 10 | +0.4988 | [+0.2386, +0.6942] | -0.0117 | [-0.2784, +0.1962] |
| pt | 567 | 562 | +0.7037 | [+0.6498, +0.7475] | 30 | 30 | +0.6623 | [+0.4456, +0.8238] | -0.0414 | [-0.2618, +0.1272] |
| si | 600 | 578 | +0.2237 | [+0.1619, +0.2843] | 30 | 30 | +0.2479 | [-0.1423, +0.5396] | +0.0242 | [-0.3628, +0.3263] |
| **medie** | | | **+0.5221** | | | | **+0.5215** | | **-0.0007** | |

**Δ split mediu -0.0007**, sd intre limbi 0.1241, interval -0.2458 pana la +0.2069. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4760 | +0.4760 | +0.0000 |
| de | +0.7300 | +0.7300 | +0.0000 |
| en | +0.6204 | +0.6204 | +0.0000 |
| es | +0.6697 | +0.6697 | +0.0000 |
| fil | +0.4101 | +0.4101 | +0.0000 |
| fr | +0.2735 | +0.2735 | +0.0000 |
| it | +0.6261 | +0.6261 | +0.0000 |
| ja | +0.4988 | +0.4988 | +0.0000 |
| pt | +0.6623 | +0.6623 | +0.0000 |
| si | +0.2479 | +0.2479 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3862 | +0.4745 | +0.0059 | +0.0015 |
| de | +0.5463 | +0.7580 | -0.0232 | -0.0280 |
| en | +0.7408 | +0.5825 | +0.0153 | +0.0379 |
| es | +0.6671 | +0.6823 | +0.0082 | -0.0126 |
| fil | +0.3742 | +0.3987 | -0.0093 | +0.0114 |
| fr | +0.5115 | +0.2220 | +0.0078 | +0.0515 |
| it | +0.5674 | +0.6416 | -0.0149 | -0.0155 |
| ja | +0.4607 | +0.3471 | +0.0498 | +0.1517 |
| pt | +0.7106 | +0.6789 | -0.0069 | -0.0166 |
| si | +0.2282 | +0.2486 | -0.0045 | -0.0007 |
