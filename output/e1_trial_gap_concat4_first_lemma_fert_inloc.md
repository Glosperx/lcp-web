# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:35:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4081 | [+0.3258, +0.4849] | 30 | 11 | +0.3314 | [-0.1130, +0.6890] | -0.0767 | [-0.5235, +0.2889] |
| de | 570 | 193 | +0.6329 | [+0.5772, +0.6833] | 23 | 11 | +0.7670 | [+0.5748, +0.8727] | +0.1341 | [-0.0768, +0.2580] |
| en | 570 | 190 | +0.8027 | [+0.7618, +0.8372] | 30 | 10 | +0.6904 | [+0.4707, +0.8834] | -0.1123 | [-0.3396, +0.0827] |
| es | 593 | 208 | +0.6657 | [+0.6226, +0.7060] | 30 | 10 | +0.6863 | [+0.3544, +0.8642] | +0.0206 | [-0.3032, +0.2102] |
| fil | 570 | 555 | +0.4098 | [+0.3362, +0.4752] | 30 | 30 | +0.5791 | [+0.3591, +0.7630] | +0.1693 | [-0.0631, +0.3651] |
| fr | 569 | 191 | +0.5621 | [+0.5021, +0.6196] | 30 | 11 | +0.3660 | [-0.0606, +0.6913] | -0.1961 | [-0.6232, +0.1338] |
| it | 570 | 192 | +0.6145 | [+0.5591, +0.6673] | 30 | 10 | +0.7067 | [+0.5065, +0.8502] | +0.0922 | [-0.1142, +0.2517] |
| ja | 570 | 190 | +0.5475 | [+0.4800, +0.6097] | 30 | 10 | +0.4494 | [+0.2657, +0.5875] | -0.0981 | [-0.2888, +0.0516] |
| pt | 567 | 562 | +0.7564 | [+0.7136, +0.7943] | 30 | 30 | +0.7572 | [+0.5969, +0.8739] | +0.0008 | [-0.1641, +0.1244] |
| si | 600 | 578 | +0.2809 | [+0.2075, +0.3545] | 30 | 30 | +0.0157 | [-0.3337, +0.3907] | -0.2652 | [-0.6381, +0.1243] |
| **medie** | | | **+0.5681** | | | | **+0.5349** | | **-0.0331** | |

**Δ split mediu -0.0331**, sd intre limbi 0.1420, interval -0.2652 pana la +0.1693. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3314 | +0.2983 | -0.0331 |
| de | +0.7670 | +0.7602 | -0.0068 |
| en | +0.6904 | +0.6984 | +0.0080 |
| es | +0.6863 | +0.6821 | -0.0042 |
| fil | +0.5791 | +0.5640 | -0.0151 |
| fr | +0.3660 | +0.3466 | -0.0194 |
| it | +0.7067 | +0.7061 | -0.0006 |
| ja | +0.4494 | +0.4558 | +0.0064 |
| pt | +0.7572 | +0.7535 | -0.0037 |
| si | +0.0157 | +0.0532 | +0.0375 |

**Diferenta medie -0.0031**, interval -0.0331 pana la +0.0375.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3806 | +0.3876 | +0.0275 | -0.0562 |
| de | +0.6390 | +0.7762 | -0.0061 | -0.0092 |
| en | +0.8120 | +0.5783 | -0.0093 | +0.1121 |
| es | +0.6276 | +0.6221 | +0.0381 | +0.0642 |
| fil | +0.4187 | +0.3233 | -0.0089 | +0.2558 |
| fr | +0.5271 | +0.3732 | +0.0350 | -0.0072 |
| it | +0.6127 | +0.6691 | +0.0018 | +0.0376 |
| ja | +0.5700 | +0.4430 | -0.0225 | +0.0064 |
| pt | +0.7510 | +0.8045 | +0.0054 | -0.0473 |
| si | +0.2312 | +0.0171 | +0.0497 | -0.0014 |
