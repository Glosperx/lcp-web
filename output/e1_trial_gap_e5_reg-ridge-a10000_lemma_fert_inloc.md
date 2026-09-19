# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:33:20 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4094 | [+0.3174, +0.4971] | 30 | 11 | +0.4586 | [+0.1458, +0.7037] | +0.0493 | [-0.2689, +0.3088] |
| de | 570 | 193 | +0.5434 | [+0.4794, +0.6022] | 23 | 11 | +0.7679 | [+0.5814, +0.8935] | +0.2245 | [+0.0347, +0.3655] |
| en | 570 | 190 | +0.7770 | [+0.7392, +0.8108] | 30 | 10 | +0.6576 | [+0.4464, +0.8410] | -0.1194 | [-0.3304, +0.0711] |
| es | 593 | 208 | +0.6882 | [+0.6415, +0.7284] | 30 | 10 | +0.6817 | [+0.3509, +0.8899] | -0.0065 | [-0.3326, +0.2095] |
| fil | 570 | 555 | +0.4080 | [+0.3394, +0.4727] | 30 | 30 | +0.4694 | [+0.1740, +0.6978] | +0.0614 | [-0.2396, +0.3036] |
| fr | 569 | 191 | +0.5240 | [+0.4627, +0.5865] | 30 | 11 | +0.2986 | [+0.0007, +0.5413] | -0.2254 | [-0.5273, +0.0203] |
| it | 570 | 192 | +0.5704 | [+0.5162, +0.6269] | 30 | 10 | +0.6309 | [+0.3653, +0.8261] | +0.0605 | [-0.2123, +0.2697] |
| ja | 570 | 190 | +0.5439 | [+0.4723, +0.6132] | 30 | 10 | +0.6170 | [+0.3946, +0.7759] | +0.0731 | [-0.1601, +0.2478] |
| pt | 567 | 562 | +0.7172 | [+0.6637, +0.7613] | 30 | 30 | +0.6753 | [+0.4625, +0.8341] | -0.0419 | [-0.2579, +0.1239] |
| si | 600 | 578 | +0.2297 | [+0.1674, +0.2923] | 30 | 30 | +0.3047 | [-0.0473, +0.5675] | +0.0750 | [-0.2802, +0.3496] |
| **medie** | | | **+0.5411** | | | | **+0.5562** | | **+0.0151** | |

**Δ split mediu +0.0151**, sd intre limbi 0.1228, interval -0.2254 pana la +0.2245. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4586 | +0.4586 | +0.0000 |
| de | +0.7679 | +0.7679 | +0.0000 |
| en | +0.6576 | +0.6576 | +0.0000 |
| es | +0.6817 | +0.6817 | +0.0000 |
| fil | +0.4694 | +0.4694 | +0.0000 |
| fr | +0.2986 | +0.2986 | +0.0000 |
| it | +0.6309 | +0.6309 | +0.0000 |
| ja | +0.6170 | +0.6170 | +0.0000 |
| pt | +0.6753 | +0.6753 | +0.0000 |
| si | +0.3047 | +0.3047 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3999 | +0.4985 | +0.0095 | -0.0399 |
| de | +0.5739 | +0.7873 | -0.0305 | -0.0194 |
| en | +0.7664 | +0.6106 | +0.0106 | +0.0470 |
| es | +0.6811 | +0.6945 | +0.0071 | -0.0128 |
| fil | +0.4066 | +0.4667 | +0.0014 | +0.0027 |
| fr | +0.5108 | +0.2475 | +0.0132 | +0.0511 |
| it | +0.5839 | +0.6553 | -0.0135 | -0.0244 |
| ja | +0.4805 | +0.4444 | +0.0634 | +0.1726 |
| pt | +0.7302 | +0.6928 | -0.0130 | -0.0175 |
| si | +0.2371 | +0.2858 | -0.0074 | +0.0189 |
