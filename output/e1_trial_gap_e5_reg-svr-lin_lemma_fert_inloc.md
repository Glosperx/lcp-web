# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:51:55 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4200 | [+0.3256, +0.5079] | 30 | 11 | +0.3958 | [-0.0345, +0.6771] | -0.0243 | [-0.4553, +0.2720] |
| de | 570 | 193 | +0.5710 | [+0.5081, +0.6291] | 23 | 11 | +0.8104 | [+0.5543, +0.9244] | +0.2394 | [-0.0275, +0.3675] |
| en | 570 | 190 | +0.7619 | [+0.7214, +0.7985] | 30 | 10 | +0.5800 | [+0.3681, +0.7463] | -0.1819 | [-0.3953, -0.0072] |
| es | 593 | 208 | +0.6808 | [+0.6387, +0.7195] | 30 | 10 | +0.6443 | [+0.2919, +0.8609] | -0.0365 | [-0.3830, +0.1875] |
| fil | 570 | 555 | +0.3935 | [+0.3206, +0.4599] | 30 | 30 | +0.5389 | [+0.2745, +0.7371] | +0.1454 | [-0.1219, +0.3616] |
| fr | 569 | 191 | +0.5280 | [+0.4618, +0.5908] | 30 | 11 | +0.2425 | [-0.0223, +0.4727] | -0.2855 | [-0.5610, -0.0438] |
| it | 570 | 192 | +0.6111 | [+0.5570, +0.6663] | 30 | 10 | +0.6104 | [+0.3952, +0.7852] | -0.0007 | [-0.2240, +0.1887] |
| ja | 570 | 190 | +0.5832 | [+0.5156, +0.6455] | 30 | 10 | +0.7074 | [+0.4978, +0.8498] | +0.1242 | [-0.0916, +0.2770] |
| pt | 567 | 562 | +0.7157 | [+0.6665, +0.7604] | 30 | 30 | +0.6705 | [+0.4507, +0.8331] | -0.0452 | [-0.2786, +0.1217] |
| si | 600 | 578 | +0.1950 | [+0.1267, +0.2643] | 30 | 30 | +0.3470 | [+0.0771, +0.6451] | +0.1520 | [-0.1284, +0.4606] |
| **medie** | | | **+0.5460** | | | | **+0.5547** | | **+0.0087** | |

**Δ split mediu +0.0087**, sd intre limbi 0.1615, interval -0.2855 pana la +0.2394. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3958 | +0.3958 | +0.0000 |
| de | +0.8104 | +0.8104 | +0.0000 |
| en | +0.5800 | +0.5800 | +0.0000 |
| es | +0.6443 | +0.6443 | +0.0000 |
| fil | +0.5389 | +0.5389 | +0.0000 |
| fr | +0.2425 | +0.2425 | +0.0000 |
| it | +0.6104 | +0.6104 | +0.0000 |
| ja | +0.7074 | +0.7074 | +0.0000 |
| pt | +0.6705 | +0.6705 | +0.0000 |
| si | +0.3470 | +0.3470 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4034 | +0.3216 | +0.0166 | +0.0742 |
| de | +0.6113 | +0.7973 | -0.0403 | +0.0131 |
| en | +0.7222 | +0.4891 | +0.0397 | +0.0909 |
| es | +0.6095 | +0.6229 | +0.0713 | +0.0214 |
| fil | +0.4048 | +0.4926 | -0.0113 | +0.0463 |
| fr | +0.4909 | +0.1359 | +0.0371 | +0.1066 |
| it | +0.5934 | +0.6720 | +0.0177 | -0.0616 |
| ja | +0.4547 | +0.6062 | +0.1285 | +0.1012 |
| pt | +0.7021 | +0.6838 | +0.0136 | -0.0133 |
| si | +0.1101 | +0.0552 | +0.0849 | +0.2918 |
