# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 11:59:22 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4736 | [+0.3946, +0.5447] | 30 | 11 | +0.4251 | [+0.0424, +0.7096] | -0.0485 | [-0.4442, +0.2478] |
| de | 570 | 193 | +0.6157 | [+0.5633, +0.6648] | 23 | 11 | +0.8448 | [+0.5763, +0.9510] | +0.2291 | [-0.0499, +0.3588] |
| en | 570 | 190 | +0.8096 | [+0.7754, +0.8404] | 30 | 10 | +0.6996 | [+0.5668, +0.8288] | -0.1100 | [-0.2440, +0.0242] |
| es | 593 | 208 | +0.6698 | [+0.6239, +0.7106] | 30 | 10 | +0.6927 | [+0.4580, +0.8374] | +0.0229 | [-0.2137, +0.1793] |
| fil | 570 | 555 | +0.3954 | [+0.3236, +0.4640] | 30 | 30 | +0.5359 | [+0.2753, +0.7468] | +0.1405 | [-0.1260, +0.3686] |
| fr | 569 | 191 | +0.5466 | [+0.4855, +0.6038] | 30 | 11 | +0.4772 | [+0.2084, +0.6734] | -0.0694 | [-0.3488, +0.1392] |
| it | 570 | 192 | +0.6149 | [+0.5631, +0.6670] | 30 | 10 | +0.7146 | [+0.5465, +0.8346] | +0.0997 | [-0.0745, +0.2396] |
| ja | 570 | 190 | +0.5298 | [+0.4550, +0.5966] | 30 | 10 | +0.6418 | [+0.3657, +0.8074] | +0.1120 | [-0.1775, +0.2876] |
| pt | 567 | 562 | +0.7619 | [+0.7215, +0.7979] | 30 | 30 | +0.7455 | [+0.5474, +0.9008] | -0.0164 | [-0.2177, +0.1403] |
| si | 600 | 578 | +0.3628 | [+0.2852, +0.4340] | 30 | 30 | +0.2304 | [-0.1769, +0.5594] | -0.1324 | [-0.5507, +0.2053] |
| **medie** | | | **+0.5780** | | | | **+0.6008** | | **+0.0227** | |

**Δ split mediu +0.0227**, sd intre limbi 0.1188, interval -0.1324 pana la +0.2291. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4251 | +0.3849 | -0.0402 |
| de | +0.8448 | +0.8325 | -0.0123 |
| en | +0.6996 | +0.7066 | +0.0070 |
| es | +0.6927 | +0.6764 | -0.0163 |
| fil | +0.5359 | +0.5540 | +0.0181 |
| fr | +0.4772 | +0.4780 | +0.0008 |
| it | +0.7146 | +0.7205 | +0.0059 |
| ja | +0.6418 | +0.6292 | -0.0126 |
| pt | +0.7455 | +0.7443 | -0.0012 |
| si | +0.2304 | +0.2684 | +0.0380 |

**Diferenta medie -0.0013**, interval -0.0402 pana la +0.0380.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4370 | +0.4351 | +0.0366 | -0.0100 |
| de | +0.6564 | +0.8870 | -0.0407 | -0.0422 |
| en | +0.8044 | +0.7021 | +0.0052 | -0.0025 |
| es | +0.6825 | +0.6283 | -0.0127 | +0.0644 |
| fil | +0.4070 | +0.5537 | -0.0116 | -0.0178 |
| fr | +0.5153 | +0.3209 | +0.0313 | +0.1563 |
| it | +0.6265 | +0.7292 | -0.0116 | -0.0146 |
| ja | +0.6053 | +0.5469 | -0.0755 | +0.0949 |
| pt | +0.7612 | +0.7767 | +0.0007 | -0.0312 |
| si | +0.2769 | +0.2434 | +0.0859 | -0.0130 |
