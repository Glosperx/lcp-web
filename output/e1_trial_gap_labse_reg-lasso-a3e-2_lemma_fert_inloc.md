# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:01:21 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3216 | [+0.2334, +0.4020] | 30 | 11 | +0.3412 | [+0.1445, +0.5436] | +0.0196 | [-0.1908, +0.2406] |
| de | 570 | 193 | +0.4109 | [+0.3510, +0.4695] | 23 | 11 | +0.6668 | [+0.2767, +0.8853] | +0.2559 | [-0.1440, +0.4827] |
| en | 570 | 190 | +0.6846 | [+0.6368, +0.7292] | 30 | 10 | +0.5277 | [+0.3906, +0.7138] | -0.1569 | [-0.2972, +0.0408] |
| es | 593 | 208 | +0.6085 | [+0.5616, +0.6534] | 30 | 10 | +0.6074 | [+0.3358, +0.7898] | -0.0011 | [-0.2798, +0.1809] |
| fil | 570 | 555 | +0.4317 | [+0.3635, +0.4975] | 30 | 30 | +0.6275 | [+0.4585, +0.7662] | +0.1958 | [+0.0195, +0.3560] |
| fr | 569 | 191 | +0.5393 | [+0.4784, +0.5980] | 30 | 11 | +0.4238 | [+0.0898, +0.6576] | -0.1155 | [-0.4634, +0.1305] |
| it | 570 | 192 | +0.5280 | [+0.4655, +0.5850] | 30 | 10 | +0.6024 | [+0.4276, +0.7817] | +0.0744 | [-0.1104, +0.2642] |
| ja | 570 | 190 | +0.5044 | [+0.4345, +0.5730] | 30 | 10 | +0.5829 | [+0.1832, +0.8562] | +0.0785 | [-0.3370, +0.3609] |
| pt | 567 | 562 | +0.6987 | [+0.6548, +0.7398] | 30 | 30 | +0.6476 | [+0.3991, +0.8417] | -0.0511 | [-0.3018, +0.1479] |
| si | 600 | 578 | +nan | [+nan, +nan] | 30 | 30 | +nan | [+nan, +nan] | +nan | [+nan, +nan] |
| **medie** | | | **+0.5253** | | | | **+0.5586** | | **+nan** | |

**Δ split mediu +nan**, sd intre limbi nan, interval +nan pana la +nan. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3412 | +0.3412 | +0.0000 |
| de | +0.6668 | +0.6668 | +0.0000 |
| en | +0.5277 | +0.5277 | +0.0000 |
| es | +0.6074 | +0.6074 | +0.0000 |
| fil | +0.6275 | +0.6275 | +0.0000 |
| fr | +0.4238 | +0.4238 | +0.0000 |
| it | +0.6024 | +0.6024 | +0.0000 |
| ja | +0.5829 | +0.5829 | +0.0000 |
| pt | +0.6476 | +0.6476 | +0.0000 |
| si | +nan | +nan | +nan |

**Diferenta medie +nan**, interval +nan pana la +nan.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3213 | +0.2704 | +0.0003 | +0.0708 |
| de | +0.6295 | +0.8357 | -0.2186 | -0.1689 |
| en | +0.7372 | +0.6087 | -0.0526 | -0.0810 |
| es | +0.6082 | +0.5723 | +0.0003 | +0.0351 |
| fil | +0.3890 | +0.6175 | +0.0427 | +0.0100 |
| fr | +0.5491 | +0.3369 | -0.0098 | +0.0869 |
| it | +0.6029 | +0.6149 | -0.0749 | -0.0125 |
| ja | +0.5382 | +0.5734 | -0.0338 | +0.0095 |
| pt | +0.7419 | +0.7357 | -0.0432 | -0.0881 |
| si | +nan | +nan | +nan | +nan |
