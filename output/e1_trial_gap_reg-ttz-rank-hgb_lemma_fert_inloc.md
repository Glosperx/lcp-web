# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:44:16 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3934 | [+0.3146, +0.4644] | 30 | 11 | +0.4694 | [-0.0371, +0.7771] | +0.0760 | [-0.4393, +0.3946] |
| de | 570 | 193 | +0.5905 | [+0.5372, +0.6400] | 23 | 11 | +0.7192 | [+0.4544, +0.8694] | +0.1286 | [-0.1507, +0.2878] |
| en | 570 | 190 | +0.7968 | [+0.7604, +0.8298] | 30 | 10 | +0.7136 | [+0.5086, +0.8757] | -0.0832 | [-0.2987, +0.0820] |
| es | 593 | 208 | +0.6565 | [+0.6136, +0.6945] | 30 | 10 | +0.7003 | [+0.4263, +0.8601] | +0.0438 | [-0.2323, +0.2093] |
| fil | 570 | 555 | +0.3907 | [+0.3219, +0.4570] | 30 | 30 | +0.6067 | [+0.3591, +0.8208] | +0.2161 | [-0.0370, +0.4443] |
| fr | 569 | 191 | +0.5422 | [+0.4738, +0.6017] | 30 | 11 | +0.3878 | [+0.0249, +0.6528] | -0.1544 | [-0.5295, +0.1200] |
| it | 570 | 192 | +0.5871 | [+0.5336, +0.6424] | 30 | 10 | +0.6587 | [+0.4301, +0.8129] | +0.0715 | [-0.1656, +0.2401] |
| ja | 570 | 190 | +0.3228 | [+0.2500, +0.3947] | 30 | 10 | +0.3775 | [+0.0035, +0.6332] | +0.0547 | [-0.3193, +0.3182] |
| pt | 567 | 562 | +0.7477 | [+0.7074, +0.7850] | 30 | 30 | +0.7644 | [+0.5822, +0.8983] | +0.0166 | [-0.1650, +0.1507] |
| si | 600 | 578 | +0.2525 | [+0.1929, +0.3136] | 30 | 30 | +0.0373 | [-0.3519, +0.4958] | -0.2152 | [-0.6086, +0.2465] |
| **medie** | | | **+0.5280** | | | | **+0.5435** | | **+0.0154** | |

**Δ split mediu +0.0154**, sd intre limbi 0.1308, interval -0.2152 pana la +0.2161. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4694 | +0.3215 | -0.1479 |
| de | +0.7192 | +0.7146 | -0.0046 |
| en | +0.7136 | +0.7061 | -0.0075 |
| es | +0.7003 | +0.6993 | -0.0010 |
| fil | +0.6067 | +0.6137 | +0.0070 |
| fr | +0.3878 | +0.3496 | -0.0382 |
| it | +0.6587 | +0.6639 | +0.0052 |
| ja | +0.3775 | +0.2990 | -0.0785 |
| pt | +0.7644 | +0.7605 | -0.0039 |
| si | +0.0373 | +0.1488 | +0.1115 |

**Diferenta medie -0.0158**, interval -0.1479 pana la +0.1115.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3878 | +0.3055 | +0.0056 | +0.1639 |
| de | +0.6123 | +0.7748 | -0.0218 | -0.0556 |
| en | +0.7902 | +0.6735 | +0.0066 | +0.0401 |
| es | +0.6541 | +0.6647 | +0.0024 | +0.0356 |
| fil | +0.4055 | +0.5672 | -0.0148 | +0.0395 |
| fr | +0.5296 | +0.3476 | +0.0126 | +0.0402 |
| it | +0.5993 | +0.7066 | -0.0122 | -0.0479 |
| ja | +0.6144 | +0.5229 | -0.2916 | -0.1454 |
| pt | +0.7631 | +0.7810 | -0.0154 | -0.0166 |
| si | +0.2456 | -0.0590 | +0.0069 | +0.0963 |
