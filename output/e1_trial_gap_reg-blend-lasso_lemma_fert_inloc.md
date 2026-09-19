# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:29:33 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4330 | [+0.3497, +0.5076] | 30 | 11 | +0.3212 | [-0.2039, +0.7099] | -0.1118 | [-0.6460, +0.2884] |
| de | 570 | 193 | +0.6526 | [+0.5991, +0.7025] | 23 | 11 | +0.8156 | [+0.5626, +0.9226] | +0.1630 | [-0.1021, +0.2905] |
| en | 570 | 190 | +0.8196 | [+0.7816, +0.8510] | 30 | 10 | +0.7075 | [+0.4703, +0.8634] | -0.1121 | [-0.3521, +0.0486] |
| es | 593 | 208 | +0.6772 | [+0.6328, +0.7171] | 30 | 10 | +0.6959 | [+0.4107, +0.8655] | +0.0187 | [-0.2703, +0.1927] |
| fil | 570 | 555 | +0.4074 | [+0.3363, +0.4749] | 30 | 30 | +0.6165 | [+0.3999, +0.7877] | +0.2091 | [-0.0147, +0.4033] |
| fr | 569 | 191 | +0.5489 | [+0.4816, +0.6083] | 30 | 11 | +0.3977 | [+0.0200, +0.6720] | -0.1512 | [-0.5271, +0.1411] |
| it | 570 | 192 | +0.6315 | [+0.5781, +0.6839] | 30 | 10 | +0.6675 | [+0.4230, +0.8290] | +0.0361 | [-0.2128, +0.2163] |
| ja | 570 | 190 | +0.5947 | [+0.5318, +0.6523] | 30 | 10 | +0.5033 | [+0.2911, +0.6572] | -0.0914 | [-0.3136, +0.0747] |
| pt | 567 | 562 | +0.7659 | [+0.7267, +0.8022] | 30 | 30 | +0.8083 | [+0.6558, +0.9159] | +0.0423 | [-0.1145, +0.1554] |
| si | 600 | 578 | +0.2505 | [+0.1858, +0.3188] | 30 | 30 | -0.1028 | [-0.5287, +0.4368] | -0.3533 | [-0.7864, +0.1899] |
| **medie** | | | **+0.5781** | | | | **+0.5431** | | **-0.0351** | |

**Δ split mediu -0.0351**, sd intre limbi 0.1642, interval -0.3533 pana la +0.2091. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3212 | +0.2840 | -0.0372 |
| de | +0.8156 | +0.8067 | -0.0089 |
| en | +0.7075 | +0.6920 | -0.0155 |
| es | +0.6959 | +0.6833 | -0.0126 |
| fil | +0.6165 | +0.6183 | +0.0018 |
| fr | +0.3977 | +0.3655 | -0.0322 |
| it | +0.6675 | +0.6634 | -0.0041 |
| ja | +0.5033 | +0.4691 | -0.0342 |
| pt | +0.8083 | +0.8071 | -0.0012 |
| si | -0.1028 | -0.0412 | +0.0616 |

**Diferenta medie -0.0083**, interval -0.0372 pana la +0.0616.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4014 | +0.2024 | +0.0316 | +0.1188 |
| de | +0.6749 | +0.8292 | -0.0223 | -0.0136 |
| en | +0.8046 | +0.6888 | +0.0150 | +0.0187 |
| es | +0.6511 | +0.6610 | +0.0261 | +0.0349 |
| fil | +0.4028 | +0.5659 | +0.0046 | +0.0506 |
| fr | +0.5511 | +0.4025 | -0.0022 | -0.0048 |
| it | +0.6276 | +0.6987 | +0.0039 | -0.0312 |
| ja | +0.5914 | +0.5014 | +0.0033 | +0.0019 |
| pt | +0.7756 | +0.7849 | -0.0097 | +0.0234 |
| si | +0.2334 | -0.0628 | +0.0171 | -0.0400 |
