# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 14:54:41 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3953 | [+0.3130, +0.4684] | 30 | 11 | +0.3069 | [-0.1940, +0.6683] | -0.0884 | [-0.5959, +0.2897] |
| de | 570 | 193 | +0.5869 | [+0.5307, +0.6434] | 23 | 11 | +0.7316 | [+0.4153, +0.8797] | +0.1448 | [-0.1730, +0.3039] |
| en | 570 | 190 | +0.7741 | [+0.7291, +0.8132] | 30 | 10 | +0.6364 | [+0.4250, +0.8471] | -0.1377 | [-0.3569, +0.0758] |
| es | 593 | 208 | +0.6877 | [+0.6450, +0.7264] | 30 | 10 | +0.6850 | [+0.4980, +0.8180] | -0.0027 | [-0.1975, +0.1332] |
| fil | 570 | 555 | +0.3665 | [+0.2949, +0.4357] | 30 | 30 | +0.5164 | [+0.2227, +0.7647] | +0.1499 | [-0.1544, +0.4096] |
| fr | 569 | 191 | +0.4870 | [+0.4143, +0.5560] | 30 | 11 | +0.2713 | [-0.1356, +0.5795] | -0.2157 | [-0.6285, +0.0969] |
| it | 570 | 192 | +0.5421 | [+0.4778, +0.6061] | 30 | 10 | +0.6596 | [+0.4488, +0.8321] | +0.1174 | [-0.1059, +0.3074] |
| ja | 570 | 190 | +0.5443 | [+0.4720, +0.6130] | 30 | 10 | +0.4985 | [+0.2406, +0.7529] | -0.0458 | [-0.3162, +0.2145] |
| pt | 567 | 562 | +0.7334 | [+0.6882, +0.7751] | 30 | 30 | +0.7500 | [+0.5750, +0.8914] | +0.0166 | [-0.1601, +0.1579] |
| si | 600 | 578 | +0.0049 | [-0.0685, +0.0861] | 30 | 30 | +0.1827 | [-0.1977, +0.5755] | +0.1778 | [-0.2168, +0.5699] |
| **medie** | | | **+0.5122** | | | | **+0.5238** | | **+0.0116** | |

**Δ split mediu +0.0116**, sd intre limbi 0.1346, interval -0.2157 pana la +0.1778. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3069 | +0.3034 | -0.0035 |
| de | +0.7316 | +0.6956 | -0.0360 |
| en | +0.6364 | +0.6089 | -0.0275 |
| es | +0.6850 | +0.6576 | -0.0274 |
| fil | +0.5164 | +0.4909 | -0.0255 |
| fr | +0.2713 | +0.2309 | -0.0404 |
| it | +0.6596 | +0.6251 | -0.0345 |
| ja | +0.4985 | +0.5292 | +0.0307 |
| pt | +0.7500 | +0.7327 | -0.0173 |
| si | +0.1827 | +0.1108 | -0.0719 |

**Diferenta medie -0.0253**, interval -0.0719 pana la +0.0307.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3273 | +0.0860 | +0.0680 | +0.2209 |
| de | +0.0592 | +0.7654 | +0.5277 | -0.0338 |
| en | +0.6758 | +0.5626 | +0.0983 | +0.0738 |
| es | +0.5744 | +0.6544 | +0.1133 | +0.0306 |
| fil | +0.3502 | +0.6120 | +0.0163 | -0.0956 |
| fr | -0.0475 | +0.2006 | +0.5345 | +0.0707 |
| it | +0.0236 | +0.6022 | +0.5185 | +0.0574 |
| ja | -0.0749 | +0.3546 | +0.6192 | +0.1439 |
| pt | +0.6547 | +0.5339 | +0.0787 | +0.2161 |
| si | -0.0167 | -0.2310 | +0.0216 | +0.4137 |
