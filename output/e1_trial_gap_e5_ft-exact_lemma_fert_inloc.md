# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:10:33 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4743 | [+0.3902, +0.5454] | 30 | 11 | +0.3389 | [-0.0966, +0.6782] | -0.1354 | [-0.5736, +0.2108] |
| de | 570 | 193 | +0.6199 | [+0.5633, +0.6748] | 23 | 11 | +0.8309 | [+0.6086, +0.9427] | +0.2110 | [-0.0209, +0.3433] |
| en | 570 | 190 | +0.8196 | [+0.7865, +0.8495] | 30 | 10 | +0.7264 | [+0.4382, +0.8860] | -0.0932 | [-0.3840, +0.0713] |
| es | 593 | 208 | +0.7044 | [+0.6624, +0.7404] | 30 | 10 | +0.7343 | [+0.4816, +0.8893] | +0.0299 | [-0.2198, +0.1898] |
| fil | 570 | 555 | +0.3890 | [+0.3182, +0.4561] | 30 | 30 | +0.5457 | [+0.2504, +0.7673] | +0.1567 | [-0.1348, +0.3875] |
| fr | 569 | 191 | +0.5474 | [+0.4849, +0.6085] | 30 | 11 | +0.3807 | [+0.1263, +0.5952] | -0.1667 | [-0.4253, +0.0585] |
| it | 570 | 192 | +0.6376 | [+0.5886, +0.6880] | 30 | 10 | +0.7013 | [+0.5092, +0.8326] | +0.0637 | [-0.1396, +0.2168] |
| ja | 570 | 190 | +0.5850 | [+0.5125, +0.6509] | 30 | 10 | +0.7026 | [+0.4982, +0.8619] | +0.1175 | [-0.0970, +0.2918] |
| pt | 567 | 562 | +0.7654 | [+0.7203, +0.8041] | 30 | 30 | +0.7377 | [+0.5451, +0.8706] | -0.0277 | [-0.2190, +0.1149] |
| si | 600 | 578 | +0.2358 | [+0.1672, +0.3021] | 30 | 30 | +0.0091 | [-0.2800, +0.3483] | -0.2267 | [-0.5219, +0.1161] |
| **medie** | | | **+0.5778** | | | | **+0.5708** | | **-0.0071** | |

**Δ split mediu -0.0071**, sd intre limbi 0.1469, interval -0.2267 pana la +0.2110. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3389 | +0.3107 | -0.0282 |
| de | +0.8309 | +0.8338 | +0.0029 |
| en | +0.7264 | +0.7337 | +0.0073 |
| es | +0.7343 | +0.7126 | -0.0217 |
| fil | +0.5457 | +0.5463 | +0.0006 |
| fr | +0.3807 | +0.3410 | -0.0397 |
| it | +0.7013 | +0.6980 | -0.0033 |
| ja | +0.7026 | +0.6970 | -0.0056 |
| pt | +0.7377 | +0.7493 | +0.0116 |
| si | +0.0091 | +0.0416 | +0.0325 |

**Diferenta medie -0.0044**, interval -0.0397 pana la +0.0325.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4563 | +0.4084 | +0.0180 | -0.0695 |
| de | +0.6647 | +0.8674 | -0.0448 | -0.0365 |
| en | +0.8019 | +0.6779 | +0.0177 | +0.0485 |
| es | +0.6981 | +0.7042 | +0.0063 | +0.0301 |
| fil | +0.4154 | +0.5784 | -0.0264 | -0.0327 |
| fr | +0.5399 | +0.2626 | +0.0075 | +0.1181 |
| it | +0.6330 | +0.7180 | +0.0046 | -0.0167 |
| ja | +0.5707 | +0.6054 | +0.0143 | +0.0972 |
| pt | +0.7752 | +0.7533 | -0.0098 | -0.0156 |
| si | +0.2329 | -0.0018 | +0.0029 | +0.0109 |
