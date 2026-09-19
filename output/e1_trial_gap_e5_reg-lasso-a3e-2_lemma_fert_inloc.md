# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:39:46 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3043 | [+0.2166, +0.3859] | 30 | 11 | +0.3479 | [+0.1526, +0.5523] | +0.0436 | [-0.1678, +0.2559] |
| de | 570 | 193 | +0.4216 | [+0.3625, +0.4819] | 23 | 11 | +0.6877 | [+0.3266, +0.8829] | +0.2660 | [-0.1075, +0.4698] |
| en | 570 | 190 | +0.6833 | [+0.6353, +0.7264] | 30 | 10 | +0.5547 | [+0.4276, +0.7293] | -0.1285 | [-0.2544, +0.0546] |
| es | 593 | 208 | +0.6036 | [+0.5593, +0.6466] | 30 | 10 | +0.5686 | [+0.2157, +0.7954] | -0.0350 | [-0.3868, +0.1942] |
| fil | 570 | 555 | +0.4185 | [+0.3489, +0.4864] | 30 | 30 | +0.6302 | [+0.4707, +0.7723] | +0.2117 | [+0.0414, +0.3708] |
| fr | 569 | 191 | +0.5376 | [+0.4795, +0.5948] | 30 | 11 | +0.4505 | [+0.1310, +0.6640] | -0.0871 | [-0.4115, +0.1345] |
| it | 570 | 192 | +0.5282 | [+0.4634, +0.5871] | 30 | 10 | +0.5735 | [+0.3867, +0.7597] | +0.0453 | [-0.1473, +0.2476] |
| ja | 570 | 190 | +0.5209 | [+0.4491, +0.5898] | 30 | 10 | +0.5789 | [+0.2127, +0.8627] | +0.0579 | [-0.3074, +0.3507] |
| pt | 567 | 562 | +0.6882 | [+0.6445, +0.7297] | 30 | 30 | +0.6386 | [+0.3799, +0.8376] | -0.0496 | [-0.3102, +0.1493] |
| si | 600 | 578 | +nan | [+nan, +nan] | 30 | 30 | +nan | [+nan, +nan] | +nan | [+nan, +nan] |
| **medie** | | | **+0.5229** | | | | **+0.5590** | | **+nan** | |

**Δ split mediu +nan**, sd intre limbi nan, interval +nan pana la +nan. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3479 | +0.3479 | +0.0000 |
| de | +0.6877 | +0.6877 | +0.0000 |
| en | +0.5547 | +0.5547 | +0.0000 |
| es | +0.5686 | +0.5686 | +0.0000 |
| fil | +0.6302 | +0.6302 | +0.0000 |
| fr | +0.4505 | +0.4505 | +0.0000 |
| it | +0.5735 | +0.5735 | +0.0000 |
| ja | +0.5789 | +0.5789 | +0.0000 |
| pt | +0.6386 | +0.6386 | +0.0000 |
| si | +nan | +nan | +nan |

**Diferenta medie +nan**, interval +nan pana la +nan.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3213 | +0.2704 | -0.0170 | +0.0775 |
| de | +0.6295 | +0.8357 | -0.2079 | -0.1480 |
| en | +0.7372 | +0.6087 | -0.0539 | -0.0540 |
| es | +0.6082 | +0.5723 | -0.0046 | -0.0037 |
| fil | +0.3890 | +0.6175 | +0.0295 | +0.0127 |
| fr | +0.5491 | +0.3369 | -0.0115 | +0.1136 |
| it | +0.6029 | +0.6149 | -0.0747 | -0.0414 |
| ja | +0.5382 | +0.5734 | -0.0173 | +0.0055 |
| pt | +0.7419 | +0.7357 | -0.0537 | -0.0971 |
| si | +nan | +nan | +nan | +nan |
