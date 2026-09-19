# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:25:56 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4163 | [+0.3438, +0.4851] | 30 | 11 | +0.4140 | [-0.0507, +0.7614] | -0.0023 | [-0.4852, +0.3530] |
| de | 570 | 193 | +0.5924 | [+0.5422, +0.6418] | 23 | 11 | +0.7810 | [+0.5337, +0.9110] | +0.1886 | [-0.0727, +0.3355] |
| en | 570 | 190 | +0.7973 | [+0.7600, +0.8313] | 30 | 10 | +0.7162 | [+0.4719, +0.8583] | -0.0811 | [-0.3305, +0.0690] |
| es | 593 | 208 | +0.6728 | [+0.6303, +0.7124] | 30 | 10 | +0.7096 | [+0.4477, +0.8695] | +0.0367 | [-0.2292, +0.2046] |
| fil | 570 | 555 | +0.3887 | [+0.3216, +0.4557] | 30 | 30 | +0.5565 | [+0.2681, +0.8065] | +0.1678 | [-0.1332, +0.4331] |
| fr | 569 | 191 | +0.5530 | [+0.4901, +0.6120] | 30 | 11 | +0.4061 | [+0.1050, +0.6144] | -0.1469 | [-0.4516, +0.0701] |
| it | 570 | 192 | +0.5977 | [+0.5456, +0.6501] | 30 | 10 | +0.7495 | [+0.6031, +0.8500] | +0.1519 | [-0.0126, +0.2710] |
| ja | 570 | 190 | +0.2975 | [+0.2169, +0.3749] | 30 | 10 | +0.4131 | [-0.0156, +0.7110] | +0.1156 | [-0.3176, +0.4115] |
| pt | 567 | 562 | +0.7628 | [+0.7203, +0.8009] | 30 | 30 | +0.7369 | [+0.5597, +0.8734] | -0.0259 | [-0.2039, +0.1117] |
| si | 600 | 578 | +0.1689 | [+0.1005, +0.2376] | 30 | 30 | +0.0080 | [-0.3413, +0.3697] | -0.1609 | [-0.5092, +0.2016] |
| **medie** | | | **+0.5247** | | | | **+0.5491** | | **+0.0244** | |

**Δ split mediu +0.0244**, sd intre limbi 0.1292, interval -0.1609 pana la +0.1886. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4140 | +0.3520 | -0.0620 |
| de | +0.7810 | +0.7660 | -0.0150 |
| en | +0.7162 | +0.7157 | -0.0005 |
| es | +0.7096 | +0.7006 | -0.0090 |
| fil | +0.5565 | +0.5882 | +0.0317 |
| fr | +0.4061 | +0.3516 | -0.0545 |
| it | +0.7495 | +0.7361 | -0.0134 |
| ja | +0.4131 | +0.4069 | -0.0062 |
| pt | +0.7369 | +0.7457 | +0.0088 |
| si | +0.0080 | +0.1068 | +0.0988 |

**Diferenta medie -0.0021**, interval -0.0620 pana la +0.0988.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4242 | +0.3917 | -0.0079 | +0.0223 |
| de | +0.6428 | +0.8520 | -0.0504 | -0.0710 |
| en | +0.7991 | +0.7390 | -0.0018 | -0.0228 |
| es | +0.6904 | +0.6757 | -0.0176 | +0.0339 |
| fil | +0.4011 | +0.5721 | -0.0124 | -0.0156 |
| fr | +0.5446 | +0.2740 | +0.0084 | +0.1321 |
| it | +0.6208 | +0.6917 | -0.0231 | +0.0578 |
| ja | +0.5632 | +0.5044 | -0.2657 | -0.0913 |
| pt | +0.7716 | +0.7458 | -0.0088 | -0.0089 |
| si | +0.1388 | -0.0133 | +0.0301 | +0.0213 |
