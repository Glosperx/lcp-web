# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:00:35 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4380 | [+0.3550, +0.5111] | 30 | 11 | +0.2959 | [-0.2388, +0.6795] | -0.1421 | [-0.6756, +0.2512] |
| de | 570 | 193 | +0.6276 | [+0.5733, +0.6787] | 23 | 11 | +0.7634 | [+0.4790, +0.9057] | +0.1358 | [-0.1570, +0.2879] |
| en | 570 | 190 | +0.8100 | [+0.7709, +0.8421] | 30 | 10 | +0.6917 | [+0.4406, +0.8615] | -0.1183 | [-0.3659, +0.0546] |
| es | 593 | 208 | +0.6725 | [+0.6280, +0.7119] | 30 | 10 | +0.6603 | [+0.3254, +0.8505] | -0.0121 | [-0.3447, +0.1851] |
| fil | 570 | 555 | +0.4117 | [+0.3410, +0.4795] | 30 | 30 | +0.6366 | [+0.4334, +0.8139] | +0.2249 | [+0.0148, +0.4188] |
| fr | 569 | 191 | +0.5301 | [+0.4629, +0.5903] | 30 | 11 | +0.3489 | [-0.0360, +0.6440] | -0.1812 | [-0.5649, +0.1270] |
| it | 570 | 192 | +0.6355 | [+0.5841, +0.6882] | 30 | 10 | +0.6554 | [+0.4362, +0.8174] | +0.0199 | [-0.2106, +0.1930] |
| ja | 570 | 190 | +0.5739 | [+0.5092, +0.6320] | 30 | 10 | +0.5856 | [+0.3984, +0.7093] | +0.0117 | [-0.1879, +0.1536] |
| pt | 567 | 562 | +0.7684 | [+0.7282, +0.8046] | 30 | 30 | +0.8108 | [+0.6498, +0.9260] | +0.0424 | [-0.1245, +0.1613] |
| si | 600 | 578 | +0.2611 | [+0.1994, +0.3284] | 30 | 30 | -0.0694 | [-0.5028, +0.4658] | -0.3305 | [-0.7686, +0.2155] |
| **medie** | | | **+0.5729** | | | | **+0.5379** | | **-0.0350** | |

**Δ split mediu -0.0350**, sd intre limbi 0.1618, interval -0.3305 pana la +0.2249. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2959 | +0.2870 | -0.0089 |
| de | +0.7634 | +0.7643 | +0.0009 |
| en | +0.6917 | +0.6914 | -0.0003 |
| es | +0.6603 | +0.6570 | -0.0033 |
| fil | +0.6366 | +0.6407 | +0.0041 |
| fr | +0.3489 | +0.3203 | -0.0286 |
| it | +0.6554 | +0.6591 | +0.0037 |
| ja | +0.5856 | +0.5403 | -0.0453 |
| pt | +0.8108 | +0.8043 | -0.0065 |
| si | -0.0694 | -0.0251 | +0.0443 |

**Diferenta medie -0.0040**, interval -0.0453 pana la +0.0443.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4089 | +0.2181 | +0.0291 | +0.0778 |
| de | +0.6521 | +0.8325 | -0.0245 | -0.0691 |
| en | +0.7986 | +0.6718 | +0.0114 | +0.0199 |
| es | +0.6562 | +0.6711 | +0.0163 | -0.0108 |
| fil | +0.4036 | +0.5617 | +0.0081 | +0.0749 |
| fr | +0.5053 | +0.3004 | +0.0248 | +0.0485 |
| it | +0.6311 | +0.6780 | +0.0044 | -0.0226 |
| ja | +0.5674 | +0.4443 | +0.0065 | +0.1413 |
| pt | +0.7644 | +0.7995 | +0.0040 | +0.0113 |
| si | +0.2174 | -0.1314 | +0.0437 | +0.0620 |
