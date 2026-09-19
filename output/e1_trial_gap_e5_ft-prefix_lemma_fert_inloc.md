# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:11:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4635 | [+0.3737, +0.5392] | 30 | 11 | +0.3372 | [-0.0802, +0.6699] | -0.1263 | [-0.5548, +0.2131] |
| de | 570 | 193 | +0.6350 | [+0.5794, +0.6879] | 23 | 11 | +0.8358 | [+0.6218, +0.9435] | +0.2008 | [-0.0201, +0.3273] |
| en | 570 | 190 | +0.8174 | [+0.7827, +0.8471] | 30 | 10 | +0.7036 | [+0.4077, +0.8754] | -0.1138 | [-0.4173, +0.0626] |
| es | 593 | 208 | +0.7038 | [+0.6613, +0.7402] | 30 | 10 | +0.7352 | [+0.4829, +0.8905] | +0.0314 | [-0.2189, +0.1894] |
| fil | 570 | 555 | +0.3714 | [+0.3005, +0.4379] | 30 | 30 | +0.5531 | [+0.2626, +0.7688] | +0.1817 | [-0.1060, +0.4097] |
| fr | 569 | 191 | +0.5501 | [+0.4880, +0.6100] | 30 | 11 | +0.3925 | [+0.1339, +0.6090] | -0.1576 | [-0.4168, +0.0668] |
| it | 570 | 192 | +0.6424 | [+0.5916, +0.6924] | 30 | 10 | +0.6833 | [+0.4765, +0.8306] | +0.0409 | [-0.1701, +0.2055] |
| ja | 570 | 190 | +0.5934 | [+0.5233, +0.6595] | 30 | 10 | +0.6911 | [+0.4602, +0.8640] | +0.0977 | [-0.1371, +0.2848] |
| pt | 567 | 562 | +0.7646 | [+0.7182, +0.8037] | 30 | 30 | +0.7348 | [+0.5400, +0.8761] | -0.0298 | [-0.2269, +0.1162] |
| si | 600 | 578 | +0.2581 | [+0.1890, +0.3228] | 30 | 30 | +0.0561 | [-0.2621, +0.4018] | -0.2019 | [-0.5248, +0.1598] |
| **medie** | | | **+0.5800** | | | | **+0.5723** | | **-0.0077** | |

**Δ split mediu -0.0077**, sd intre limbi 0.1416, interval -0.2019 pana la +0.2008. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3372 | +0.3010 | -0.0362 |
| de | +0.8358 | +0.8355 | -0.0003 |
| en | +0.7036 | +0.7189 | +0.0153 |
| es | +0.7352 | +0.7098 | -0.0254 |
| fil | +0.5531 | +0.5476 | -0.0055 |
| fr | +0.3925 | +0.3669 | -0.0256 |
| it | +0.6833 | +0.6722 | -0.0111 |
| ja | +0.6911 | +0.6844 | -0.0067 |
| pt | +0.7348 | +0.7480 | +0.0132 |
| si | +0.0561 | +0.0858 | +0.0297 |

**Diferenta medie -0.0053**, interval -0.0362 pana la +0.0297.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4563 | +0.4084 | +0.0072 | -0.0712 |
| de | +0.6647 | +0.8674 | -0.0297 | -0.0316 |
| en | +0.8019 | +0.6779 | +0.0155 | +0.0257 |
| es | +0.6981 | +0.7042 | +0.0057 | +0.0310 |
| fil | +0.4031 | +0.5784 | -0.0317 | -0.0253 |
| fr | +0.5399 | +0.2626 | +0.0102 | +0.1299 |
| it | +0.6330 | +0.7180 | +0.0094 | -0.0347 |
| ja | +0.5707 | +0.6054 | +0.0227 | +0.0857 |
| pt | +0.7752 | +0.7533 | -0.0106 | -0.0185 |
| si | +0.2586 | +0.0658 | -0.0005 | -0.0097 |
