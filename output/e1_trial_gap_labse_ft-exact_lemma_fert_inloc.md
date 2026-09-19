# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:08:27 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4724 | [+0.3945, +0.5441] | 30 | 11 | +0.3803 | [-0.0413, +0.6892] | -0.0921 | [-0.5284, +0.2277] |
| de | 570 | 193 | +0.6162 | [+0.5638, +0.6663] | 23 | 11 | +0.8464 | [+0.5600, +0.9553] | +0.2302 | [-0.0665, +0.3634] |
| en | 570 | 190 | +0.8106 | [+0.7765, +0.8412] | 30 | 10 | +0.7060 | [+0.5616, +0.8355] | -0.1045 | [-0.2513, +0.0274] |
| es | 593 | 208 | +0.6669 | [+0.6205, +0.7073] | 30 | 10 | +0.6946 | [+0.4445, +0.8511] | +0.0277 | [-0.2254, +0.1926] |
| fil | 570 | 555 | +0.3750 | [+0.3001, +0.4440] | 30 | 30 | +0.5243 | [+0.2680, +0.7425] | +0.1492 | [-0.1159, +0.3818] |
| fr | 569 | 191 | +0.5499 | [+0.4887, +0.6074] | 30 | 11 | +0.4834 | [+0.2280, +0.6743] | -0.0666 | [-0.3423, +0.1387] |
| it | 570 | 192 | +0.6223 | [+0.5695, +0.6739] | 30 | 10 | +0.7200 | [+0.5507, +0.8394] | +0.0978 | [-0.0753, +0.2342] |
| ja | 570 | 190 | +0.5744 | [+0.4969, +0.6407] | 30 | 10 | +0.6294 | [+0.3452, +0.7968] | +0.0549 | [-0.2379, +0.2397] |
| pt | 567 | 562 | +0.7580 | [+0.7179, +0.7939] | 30 | 30 | +0.7420 | [+0.5488, +0.8980] | -0.0160 | [-0.2112, +0.1398] |
| si | 600 | 578 | +0.2756 | [+0.2134, +0.3356] | 30 | 30 | +0.0264 | [-0.2653, +0.3224] | -0.2492 | [-0.5408, +0.0380] |
| **medie** | | | **+0.5721** | | | | **+0.5753** | | **+0.0031** | |

**Δ split mediu +0.0031**, sd intre limbi 0.1393, interval -0.2492 pana la +0.2302. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3803 | +0.3643 | -0.0160 |
| de | +0.8464 | +0.8270 | -0.0194 |
| en | +0.7060 | +0.7063 | +0.0003 |
| es | +0.6946 | +0.6834 | -0.0112 |
| fil | +0.5243 | +0.5352 | +0.0109 |
| fr | +0.4834 | +0.5043 | +0.0209 |
| it | +0.7200 | +0.7230 | +0.0030 |
| ja | +0.6294 | +0.6241 | -0.0053 |
| pt | +0.7420 | +0.7415 | -0.0005 |
| si | +0.0264 | +0.0427 | +0.0163 |

**Diferenta medie -0.0001**, interval -0.0194 pana la +0.0209.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4313 | +0.4211 | +0.0411 | -0.0408 |
| de | +0.6567 | +0.8861 | -0.0405 | -0.0397 |
| en | +0.8055 | +0.7044 | +0.0051 | +0.0016 |
| es | +0.6848 | +0.6430 | -0.0179 | +0.0516 |
| fil | +0.4140 | +0.5631 | -0.0390 | -0.0388 |
| fr | +0.5107 | +0.3288 | +0.0392 | +0.1546 |
| it | +0.6289 | +0.7304 | -0.0066 | -0.0104 |
| ja | +0.5791 | +0.5001 | -0.0047 | +0.1293 |
| pt | +0.7636 | +0.7735 | -0.0056 | -0.0315 |
| si | +0.2488 | +0.0341 | +0.0268 | -0.0077 |
