# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:48:50 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4180 | [+0.3313, +0.5021] | 30 | 11 | +0.2789 | [-0.1460, +0.6832] | -0.1391 | [-0.5737, +0.2777] |
| de | 570 | 193 | +0.6189 | [+0.5601, +0.6730] | 23 | 11 | +0.6763 | [+0.3842, +0.8264] | +0.0574 | [-0.2405, +0.2205] |
| en | 570 | 190 | +0.8041 | [+0.7629, +0.8389] | 30 | 10 | +0.6806 | [+0.4460, +0.8552] | -0.1235 | [-0.3660, +0.0532] |
| es | 593 | 208 | +0.6432 | [+0.5966, +0.6861] | 30 | 10 | +0.6735 | [+0.3668, +0.8367] | +0.0303 | [-0.2660, +0.2011] |
| fil | 570 | 555 | +0.4237 | [+0.3545, +0.4867] | 30 | 30 | +0.4973 | [+0.2363, +0.7046] | +0.0736 | [-0.1959, +0.3001] |
| fr | 569 | 191 | +0.5164 | [+0.4473, +0.5776] | 30 | 11 | +0.3162 | [-0.0722, +0.6220] | -0.2002 | [-0.5910, +0.1203] |
| it | 570 | 192 | +0.5886 | [+0.5297, +0.6487] | 30 | 10 | +0.6466 | [+0.3812, +0.8267] | +0.0580 | [-0.2092, +0.2535] |
| ja | 570 | 190 | +0.6273 | [+0.5671, +0.6812] | 30 | 10 | +0.5758 | [+0.4146, +0.6988] | -0.0515 | [-0.2218, +0.0796] |
| pt | 567 | 562 | +0.7321 | [+0.6888, +0.7703] | 30 | 30 | +0.7837 | [+0.6296, +0.9000] | +0.0516 | [-0.1078, +0.1744] |
| si | 600 | 578 | +0.2825 | [+0.2253, +0.3389] | 30 | 30 | +0.1048 | [-0.2481, +0.4629] | -0.1778 | [-0.5418, +0.1865] |
| **medie** | | | **+0.5655** | | | | **+0.5234** | | **-0.0421** | |

**Δ split mediu -0.0421**, sd intre limbi 0.1090, interval -0.2002 pana la +0.0736. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2789 | +0.2678 | -0.0111 |
| de | +0.6763 | +0.6847 | +0.0084 |
| en | +0.6806 | +0.6815 | +0.0009 |
| es | +0.6735 | +0.6860 | +0.0125 |
| fil | +0.4973 | +0.5034 | +0.0061 |
| fr | +0.3162 | +0.2809 | -0.0353 |
| it | +0.6466 | +0.6352 | -0.0114 |
| ja | +0.5758 | +0.5439 | -0.0319 |
| pt | +0.7837 | +0.7889 | +0.0052 |
| si | +0.1048 | +0.1204 | +0.0156 |

**Diferenta medie -0.0041**, interval -0.0353 pana la +0.0156.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3923 | +0.3181 | +0.0257 | -0.0392 |
| de | +0.5870 | +0.6355 | +0.0319 | +0.0408 |
| en | +0.7989 | +0.6579 | +0.0052 | +0.0227 |
| es | +0.6298 | +0.7125 | +0.0134 | -0.0390 |
| fil | +0.4190 | +0.4507 | +0.0047 | +0.0466 |
| fr | +0.4960 | +0.3393 | +0.0204 | -0.0231 |
| it | +0.5610 | +0.6473 | +0.0276 | -0.0007 |
| ja | +0.5967 | +0.4514 | +0.0306 | +0.1244 |
| pt | +0.7216 | +0.7358 | +0.0105 | +0.0479 |
| si | +0.2928 | +0.1756 | -0.0103 | -0.0708 |
