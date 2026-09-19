# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:23:49 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.2890 | [+0.2004, +0.3758] | 30 | 11 | +0.2700 | [+0.0845, +0.5425] | -0.0190 | [-0.2152, +0.2686] |
| de | 570 | 193 | +0.5450 | [+0.4916, +0.5951] | 23 | 11 | +0.7050 | [+0.4368, +0.8402] | +0.1600 | [-0.1162, +0.3086] |
| en | 570 | 190 | +0.6486 | [+0.5947, +0.6938] | 30 | 10 | +0.5858 | [+0.4376, +0.7524] | -0.0628 | [-0.2091, +0.1176] |
| es | 593 | 208 | +0.5291 | [+0.4745, +0.5833] | 30 | 10 | +0.6120 | [+0.3786, +0.7827] | +0.0829 | [-0.1575, +0.2597] |
| fil | 570 | 555 | +0.3727 | [+0.3015, +0.4407] | 30 | 30 | +0.4252 | [+0.1090, +0.6507] | +0.0525 | [-0.2641, +0.2880] |
| fr | 569 | 191 | +0.5618 | [+0.5031, +0.6195] | 30 | 11 | +0.4866 | [+0.0755, +0.7383] | -0.0752 | [-0.4980, +0.1818] |
| it | 570 | 192 | +0.5321 | [+0.4675, +0.5931] | 30 | 10 | +0.5282 | [+0.2729, +0.7422] | -0.0039 | [-0.2620, +0.2216] |
| ja | 570 | 190 | +0.5150 | [+0.4476, +0.5825] | 30 | 10 | +0.4768 | [+0.2091, +0.6818] | -0.0382 | [-0.3049, +0.1715] |
| pt | 567 | 562 | +0.6312 | [+0.5818, +0.6763] | 30 | 30 | +0.6257 | [+0.3766, +0.8257] | -0.0055 | [-0.2542, +0.1977] |
| si | 600 | 578 | +0.1211 | [+0.0448, +0.1956] | 30 | 30 | -0.1020 | [-0.3983, +0.2062] | -0.2231 | [-0.5211, +0.1034] |
| **medie** | | | **+0.4746** | | | | **+0.4613** | | **-0.0132** | |

**Δ split mediu -0.0132**, sd intre limbi 0.1026, interval -0.2231 pana la +0.1600. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2700 | +0.2700 | +0.0000 |
| de | +0.7050 | +0.7050 | +0.0000 |
| en | +0.5858 | +0.5858 | +0.0000 |
| es | +0.6120 | +0.6120 | +0.0000 |
| fil | +0.4252 | +0.4252 | +0.0000 |
| fr | +0.4866 | +0.4866 | +0.0000 |
| it | +0.5282 | +0.5282 | +0.0000 |
| ja | +0.4768 | +0.4768 | +0.0000 |
| pt | +0.6257 | +0.6257 | +0.0000 |
| si | -0.1020 | -0.1020 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3213 | +0.2704 | -0.0323 | -0.0004 |
| de | +0.6295 | +0.8357 | -0.0845 | -0.1307 |
| en | +0.7372 | +0.6087 | -0.0886 | -0.0229 |
| es | +0.6082 | +0.5723 | -0.0791 | +0.0397 |
| fil | +0.3890 | +0.6175 | -0.0163 | -0.1923 |
| fr | +0.5491 | +0.3369 | +0.0127 | +0.1497 |
| it | +0.6029 | +0.6149 | -0.0708 | -0.0867 |
| ja | +0.5382 | +0.5734 | -0.0232 | -0.0966 |
| pt | +0.7419 | +0.7357 | -0.1107 | -0.1100 |
| si | +nan | +nan | +nan | +nan |
