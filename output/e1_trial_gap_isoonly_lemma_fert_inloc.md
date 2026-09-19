# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:50:56 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3751 | [+0.2895, +0.4507] | 30 | 11 | +0.1665 | [-0.3488, +0.5833] | -0.2086 | [-0.7289, +0.2260] |
| de | 570 | 193 | +0.5708 | [+0.5182, +0.6211] | 23 | 11 | +0.7378 | [+0.4672, +0.9012] | +0.1670 | [-0.1119, +0.3387] |
| en | 570 | 190 | +0.7711 | [+0.7269, +0.8067] | 30 | 10 | +0.6848 | [+0.3897, +0.8001] | -0.0863 | [-0.3851, +0.0425] |
| es | 593 | 208 | +0.6264 | [+0.5774, +0.6707] | 30 | 10 | +0.6550 | [+0.3938, +0.8232] | +0.0286 | [-0.2379, +0.2053] |
| fil | 570 | 555 | +0.3855 | [+0.3153, +0.4547] | 30 | 30 | +0.6447 | [+0.4607, +0.7914] | +0.2592 | [+0.0675, +0.4278] |
| fr | 569 | 191 | +0.5373 | [+0.4757, +0.5970] | 30 | 11 | +0.3732 | [-0.0259, +0.6577] | -0.1641 | [-0.5644, +0.1319] |
| it | 570 | 192 | +0.5631 | [+0.5062, +0.6185] | 30 | 10 | +0.6727 | [+0.5152, +0.8228] | +0.1095 | [-0.0565, +0.2745] |
| ja | 570 | 190 | +0.3577 | [+0.2776, +0.4381] | 30 | 10 | +0.3355 | [+0.0166, +0.6227] | -0.0223 | [-0.3508, +0.2729] |
| pt | 567 | 562 | +0.7316 | [+0.6923, +0.7700] | 30 | 30 | +0.7376 | [+0.5566, +0.8754] | +0.0060 | [-0.1787, +0.1444] |
| si | 600 | 578 | +0.1015 | [+0.0344, +0.1688] | 30 | 30 | +0.0115 | [-0.3860, +0.4673] | -0.0901 | [-0.4900, +0.3767] |
| **medie** | | | **+0.5020** | | | | **+0.5019** | | **-0.0001** | |

**Δ split mediu -0.0001**, sd intre limbi 0.1470, interval -0.2086 pana la +0.2592. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1665 | +0.0730 | -0.0935 |
| de | +0.7378 | +0.7286 | -0.0092 |
| en | +0.6848 | +0.6655 | -0.0193 |
| es | +0.6550 | +0.6562 | +0.0012 |
| fil | +0.6447 | +0.6573 | +0.0126 |
| fr | +0.3732 | +0.3526 | -0.0206 |
| it | +0.6727 | +0.6705 | -0.0022 |
| ja | +0.3355 | +0.3179 | -0.0176 |
| pt | +0.7376 | +0.7362 | -0.0014 |
| si | +0.0115 | +0.0280 | +0.0165 |

**Diferenta medie -0.0134**, interval -0.0935 pana la +0.0165.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3454 | +0.1650 | +0.0297 | +0.0015 |
| de | +0.6112 | +0.8275 | -0.0404 | -0.0897 |
| en | +0.7672 | +0.7211 | +0.0039 | -0.0363 |
| es | +0.6064 | +0.5613 | +0.0200 | +0.0937 |
| fil | +0.3894 | +0.6335 | -0.0039 | +0.0112 |
| fr | +0.5183 | +0.3211 | +0.0190 | +0.0521 |
| it | +0.5849 | +0.6791 | -0.0218 | -0.0064 |
| ja | +0.4728 | +0.4388 | -0.1151 | -0.1033 |
| pt | +0.7313 | +0.7535 | +0.0003 | -0.0159 |
| si | +0.0454 | -0.0814 | +0.0561 | +0.0929 |
