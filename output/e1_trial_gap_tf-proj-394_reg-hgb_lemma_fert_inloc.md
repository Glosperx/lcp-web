# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 13:55:31 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3824 | [+0.3025, +0.4543] | 30 | 11 | +0.3339 | [-0.2244, +0.7591] | -0.0485 | [-0.6190, +0.3858] |
| de | 570 | 193 | +0.6206 | [+0.5693, +0.6679] | 23 | 11 | +0.7151 | [+0.4833, +0.8343] | +0.0944 | [-0.1363, +0.2242] |
| en | 570 | 190 | +0.8120 | [+0.7732, +0.8460] | 30 | 10 | +0.7292 | [+0.4764, +0.8620] | -0.0828 | [-0.3417, +0.0587] |
| es | 593 | 208 | +0.6611 | [+0.6153, +0.7034] | 30 | 10 | +0.7136 | [+0.4935, +0.8636] | +0.0526 | [-0.1721, +0.2102] |
| fil | 570 | 555 | +0.4349 | [+0.3666, +0.5008] | 30 | 30 | +0.6061 | [+0.3618, +0.8122] | +0.1712 | [-0.0857, +0.3824] |
| fr | 569 | 191 | +0.5360 | [+0.4639, +0.6014] | 30 | 11 | +0.3911 | [+0.0345, +0.6596] | -0.1448 | [-0.5096, +0.1339] |
| it | 570 | 192 | +0.6038 | [+0.5499, +0.6590] | 30 | 10 | +0.6939 | [+0.4597, +0.8450] | +0.0901 | [-0.1454, +0.2594] |
| ja | 570 | 190 | +0.3885 | [+0.3149, +0.4594] | 30 | 10 | +0.4329 | [+0.0421, +0.6799] | +0.0444 | [-0.3440, +0.2990] |
| pt | 567 | 562 | +0.7596 | [+0.7212, +0.7950] | 30 | 30 | +0.7639 | [+0.5837, +0.8939] | +0.0043 | [-0.1799, +0.1375] |
| si | 600 | 578 | +0.1275 | [+0.0612, +0.2009] | 30 | 30 | -0.1554 | [-0.4604, +0.2048] | -0.2830 | [-0.5956, +0.0852] |
| **medie** | | | **+0.5326** | | | | **+0.5224** | | **-0.0102** | |

**Δ split mediu -0.0102**, sd intre limbi 0.1335, interval -0.2830 pana la +0.1712. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3339 | +0.2234 | -0.1105 |
| de | +0.7151 | +0.7358 | +0.0207 |
| en | +0.7292 | +0.7178 | -0.0114 |
| es | +0.7136 | +0.7020 | -0.0116 |
| fil | +0.6061 | +0.6521 | +0.0460 |
| fr | +0.3911 | +0.3357 | -0.0554 |
| it | +0.6939 | +0.6858 | -0.0081 |
| ja | +0.4329 | +0.3493 | -0.0836 |
| pt | +0.7639 | +0.7615 | -0.0024 |
| si | -0.1554 | -0.0668 | +0.0886 |

**Diferenta medie -0.0128**, interval -0.1105 pana la +0.0886.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3823 | +0.2095 | +0.0001 | +0.1244 |
| de | +0.6510 | +0.8362 | -0.0304 | -0.1211 |
| en | +0.8216 | +0.7347 | -0.0096 | -0.0055 |
| es | +0.6598 | +0.6723 | +0.0013 | +0.0413 |
| fil | +0.4019 | +0.6082 | +0.0330 | -0.0021 |
| fr | +0.5157 | +0.3861 | +0.0203 | +0.0050 |
| it | +0.5970 | +0.7251 | +0.0068 | -0.0312 |
| ja | +0.6027 | +0.4700 | -0.2142 | -0.0371 |
| pt | +0.7636 | +0.7708 | -0.0040 | -0.0069 |
| si | +0.0564 | -0.1172 | +0.0711 | -0.0382 |
