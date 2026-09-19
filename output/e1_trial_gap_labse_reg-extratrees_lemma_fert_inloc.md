# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:18:47 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4212 | [+0.3435, +0.4920] | 30 | 11 | +0.4510 | [+0.0497, +0.7666] | +0.0298 | [-0.3952, +0.3523] |
| de | 570 | 193 | +0.5946 | [+0.5450, +0.6412] | 23 | 11 | +0.7717 | [+0.4824, +0.9276] | +0.1771 | [-0.1157, +0.3476] |
| en | 570 | 190 | +0.7946 | [+0.7572, +0.8282] | 30 | 10 | +0.6396 | [+0.4472, +0.7927] | -0.1551 | [-0.3546, +0.0045] |
| es | 593 | 208 | +0.6313 | [+0.5828, +0.6747] | 30 | 10 | +0.6015 | [+0.3682, +0.7791] | -0.0298 | [-0.2677, +0.1569] |
| fil | 570 | 555 | +0.4236 | [+0.3543, +0.4886] | 30 | 30 | +0.5701 | [+0.3223, +0.7658] | +0.1465 | [-0.1036, +0.3582] |
| fr | 569 | 191 | +0.5475 | [+0.4837, +0.6077] | 30 | 11 | +0.4490 | [+0.1527, +0.6756] | -0.0985 | [-0.4066, +0.1400] |
| it | 570 | 192 | +0.5856 | [+0.5281, +0.6422] | 30 | 10 | +0.6791 | [+0.5125, +0.8078] | +0.0935 | [-0.0817, +0.2398] |
| ja | 570 | 190 | +0.5897 | [+0.5218, +0.6512] | 30 | 10 | +0.6002 | [+0.2385, +0.8499] | +0.0105 | [-0.3560, +0.2717] |
| pt | 567 | 562 | +0.7641 | [+0.7260, +0.7987] | 30 | 30 | +0.7435 | [+0.5512, +0.9016] | -0.0205 | [-0.2114, +0.1418] |
| si | 600 | 578 | +0.3232 | [+0.2365, +0.4010] | 30 | 30 | +0.4241 | [+0.0793, +0.6659] | +0.1009 | [-0.2492, +0.3521] |
| **medie** | | | **+0.5675** | | | | **+0.5930** | | **+0.0254** | |

**Δ split mediu +0.0254**, sd intre limbi 0.1061, interval -0.1551 pana la +0.1771. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4510 | +0.4486 | -0.0024 |
| de | +0.7717 | +0.7896 | +0.0179 |
| en | +0.6396 | +0.6358 | -0.0038 |
| es | +0.6015 | +0.5934 | -0.0081 |
| fil | +0.5701 | +0.5859 | +0.0158 |
| fr | +0.4490 | +0.4153 | -0.0337 |
| it | +0.6791 | +0.6946 | +0.0155 |
| ja | +0.6002 | +0.5356 | -0.0646 |
| pt | +0.7435 | +0.7407 | -0.0028 |
| si | +0.4241 | +0.4432 | +0.0191 |

**Diferenta medie -0.0047**, interval -0.0646 pana la +0.0191.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3923 | +0.4244 | +0.0289 | +0.0266 |
| de | +0.6144 | +0.8021 | -0.0198 | -0.0304 |
| en | +0.8024 | +0.6658 | -0.0078 | -0.0262 |
| es | +0.6565 | +0.5787 | -0.0252 | +0.0228 |
| fil | +0.4333 | +0.6164 | -0.0097 | -0.0463 |
| fr | +0.5355 | +0.4032 | +0.0120 | +0.0458 |
| it | +0.6094 | +0.7017 | -0.0238 | -0.0226 |
| ja | +0.5930 | +0.5670 | -0.0033 | +0.0332 |
| pt | +0.7587 | +0.7453 | +0.0054 | -0.0018 |
| si | +0.2162 | +0.2594 | +0.1070 | +0.1647 |
