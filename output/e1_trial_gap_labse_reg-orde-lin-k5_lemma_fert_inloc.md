# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:28:57 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4451 | [+0.3612, +0.5208] | 30 | 11 | +0.2172 | [-0.1222, +0.4908] | -0.2279 | [-0.5731, +0.0640] |
| de | 570 | 193 | +0.5552 | [+0.4926, +0.6153] | 23 | 11 | +0.7819 | [+0.4892, +0.9028] | +0.2268 | [-0.0716, +0.3658] |
| en | 570 | 190 | +0.7813 | [+0.7418, +0.8161] | 30 | 10 | +0.6177 | [+0.4625, +0.8111] | -0.1635 | [-0.3294, +0.0371] |
| es | 593 | 208 | +0.6174 | [+0.5619, +0.6676] | 30 | 10 | +0.6645 | [+0.4110, +0.8284] | +0.0471 | [-0.2171, +0.2179] |
| fil | 570 | 555 | +0.3956 | [+0.3223, +0.4666] | 30 | 30 | +0.4852 | [+0.2249, +0.6964] | +0.0896 | [-0.1796, +0.3135] |
| fr | 569 | 191 | +0.5087 | [+0.4433, +0.5707] | 30 | 11 | +0.5089 | [+0.2453, +0.7209] | +0.0002 | [-0.2692, +0.2174] |
| it | 570 | 192 | +0.5706 | [+0.5075, +0.6306] | 30 | 10 | +0.6619 | [+0.4005, +0.8269] | +0.0913 | [-0.1699, +0.2741] |
| ja | 570 | 190 | +0.5165 | [+0.4296, +0.5942] | 30 | 10 | +0.5366 | [+0.1230, +0.8216] | +0.0201 | [-0.4165, +0.3178] |
| pt | 567 | 562 | +0.7432 | [+0.7021, +0.7785] | 30 | 30 | +0.7075 | [+0.4487, +0.9229] | -0.0358 | [-0.2974, +0.1835] |
| si | 600 | 578 | +0.2837 | [+0.2304, +0.3294] | 30 | 30 | +0.0409 | [-0.3288, +0.3964] | -0.2427 | [-0.6078, +0.1224] |
| **medie** | | | **+0.5417** | | | | **+0.5222** | | **-0.0195** | |

**Δ split mediu -0.0195**, sd intre limbi 0.1511, interval -0.2427 pana la +0.2268. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2172 | +0.2133 | -0.0039 |
| de | +0.7819 | +0.7753 | -0.0066 |
| en | +0.6177 | +0.6216 | +0.0039 |
| es | +0.6645 | +0.6741 | +0.0096 |
| fil | +0.4852 | +0.4746 | -0.0106 |
| fr | +0.5089 | +0.5091 | +0.0002 |
| it | +0.6619 | +0.6593 | -0.0026 |
| ja | +0.5366 | +0.5338 | -0.0028 |
| pt | +0.7075 | +0.7076 | +0.0001 |
| si | +0.0409 | +0.0026 | -0.0383 |

**Diferenta medie -0.0051**, interval -0.0383 pana la +0.0096.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4343 | +0.2554 | +0.0108 | -0.0382 |
| de | +0.6076 | +0.8566 | -0.0524 | -0.0747 |
| en | +0.7506 | +0.6985 | +0.0307 | -0.0808 |
| es | +0.6331 | +0.5936 | -0.0157 | +0.0709 |
| fil | +0.4065 | +0.5227 | -0.0109 | -0.0375 |
| fr | +0.4701 | +0.3215 | +0.0386 | +0.1874 |
| it | +0.5493 | +0.6292 | +0.0213 | +0.0327 |
| ja | +0.5388 | +0.4507 | -0.0223 | +0.0859 |
| pt | +0.7411 | +0.7090 | +0.0021 | -0.0015 |
| si | +0.1875 | +0.0052 | +0.0962 | +0.0357 |
