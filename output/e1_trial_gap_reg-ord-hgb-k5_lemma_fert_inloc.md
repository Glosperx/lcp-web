# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:47:53 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3958 | [+0.3219, +0.4627] | 30 | 11 | +0.3985 | [-0.1828, +0.7699] | +0.0026 | [-0.5788, +0.3928] |
| de | 570 | 193 | +0.5927 | [+0.5406, +0.6416] | 23 | 11 | +0.7166 | [+0.4521, +0.8637] | +0.1239 | [-0.1585, +0.2781] |
| en | 570 | 190 | +0.7858 | [+0.7494, +0.8188] | 30 | 10 | +0.7048 | [+0.4869, +0.8678] | -0.0810 | [-0.2999, +0.0878] |
| es | 593 | 208 | +0.6630 | [+0.6195, +0.7018] | 30 | 10 | +0.6665 | [+0.3759, +0.8506] | +0.0035 | [-0.2865, +0.1931] |
| fil | 570 | 555 | +0.4093 | [+0.3411, +0.4728] | 30 | 30 | +0.5948 | [+0.3474, +0.8041] | +0.1855 | [-0.0687, +0.4051] |
| fr | 569 | 191 | +0.5598 | [+0.4933, +0.6184] | 30 | 11 | +0.3663 | [+0.0256, +0.6233] | -0.1935 | [-0.5353, +0.0728] |
| it | 570 | 192 | +0.5924 | [+0.5399, +0.6457] | 30 | 10 | +0.6890 | [+0.4931, +0.8296] | +0.0967 | [-0.1092, +0.2480] |
| ja | 570 | 190 | +0.5470 | [+0.4800, +0.6081] | 30 | 10 | +0.5493 | [+0.3243, +0.7094] | +0.0023 | [-0.2280, +0.1740] |
| pt | 567 | 562 | +0.7591 | [+0.7213, +0.7953] | 30 | 30 | +0.7756 | [+0.5937, +0.9115] | +0.0165 | [-0.1636, +0.1553] |
| si | 600 | 578 | +0.2928 | [+0.2280, +0.3584] | 30 | 30 | -0.0795 | [-0.4496, +0.3179] | -0.3723 | [-0.7449, +0.0298] |
| **medie** | | | **+0.5598** | | | | **+0.5382** | | **-0.0216** | |

**Δ split mediu -0.0216**, sd intre limbi 0.1624, interval -0.3723 pana la +0.1855. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3985 | +0.3787 | -0.0198 |
| de | +0.7166 | +0.7012 | -0.0154 |
| en | +0.7048 | +0.6947 | -0.0101 |
| es | +0.6665 | +0.6759 | +0.0094 |
| fil | +0.5948 | +0.6312 | +0.0364 |
| fr | +0.3663 | +0.3373 | -0.0290 |
| it | +0.6890 | +0.6917 | +0.0027 |
| ja | +0.5493 | +0.5010 | -0.0483 |
| pt | +0.7756 | +0.7763 | +0.0007 |
| si | -0.0795 | +0.0362 | +0.1157 |

**Diferenta medie +0.0042**, interval -0.0483 pana la +0.1157.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3787 | +0.3313 | +0.0171 | +0.0672 |
| de | +0.6220 | +0.7846 | -0.0293 | -0.0680 |
| en | +0.7856 | +0.6719 | +0.0002 | +0.0329 |
| es | +0.6589 | +0.6441 | +0.0041 | +0.0224 |
| fil | +0.4058 | +0.5908 | +0.0035 | +0.0040 |
| fr | +0.5563 | +0.3388 | +0.0035 | +0.0275 |
| it | +0.6013 | +0.7179 | -0.0089 | -0.0289 |
| ja | +0.6116 | +0.5299 | -0.0646 | +0.0194 |
| pt | +0.7748 | +0.7775 | -0.0157 | -0.0019 |
| si | +0.2547 | -0.1889 | +0.0381 | +0.1094 |
