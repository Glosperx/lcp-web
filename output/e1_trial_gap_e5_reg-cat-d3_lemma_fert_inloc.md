# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:22:44 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4272 | [+0.3537, +0.4920] | 30 | 11 | +0.4062 | [-0.0362, +0.7439] | -0.0209 | [-0.4675, +0.3197] |
| de | 570 | 193 | +0.6075 | [+0.5547, +0.6582] | 23 | 11 | +0.8031 | [+0.5520, +0.9318] | +0.1956 | [-0.0599, +0.3434] |
| en | 570 | 190 | +0.8052 | [+0.7702, +0.8374] | 30 | 10 | +0.7468 | [+0.4724, +0.8711] | -0.0584 | [-0.3308, +0.0721] |
| es | 593 | 208 | +0.6813 | [+0.6382, +0.7206] | 30 | 10 | +0.7074 | [+0.4913, +0.8544] | +0.0261 | [-0.1958, +0.1791] |
| fil | 570 | 555 | +0.3912 | [+0.3241, +0.4577] | 30 | 30 | +0.5235 | [+0.2021, +0.7929] | +0.1323 | [-0.1933, +0.4116] |
| fr | 569 | 191 | +0.5508 | [+0.4831, +0.6111] | 30 | 11 | +0.3642 | [+0.0279, +0.6237] | -0.1865 | [-0.5298, +0.0854] |
| it | 570 | 192 | +0.6127 | [+0.5632, +0.6632] | 30 | 10 | +0.7294 | [+0.5601, +0.8425] | +0.1167 | [-0.0639, +0.2475] |
| ja | 570 | 190 | +0.5238 | [+0.4527, +0.5957] | 30 | 10 | +0.5623 | [+0.2281, +0.8024] | +0.0385 | [-0.3116, +0.2862] |
| pt | 567 | 562 | +0.7646 | [+0.7238, +0.8028] | 30 | 30 | +0.7677 | [+0.5905, +0.9070] | +0.0030 | [-0.1796, +0.1425] |
| si | 600 | 578 | +0.2450 | [+0.1698, +0.3133] | 30 | 30 | +0.1953 | [-0.1496, +0.5331] | -0.0496 | [-0.3937, +0.2945] |
| **medie** | | | **+0.5609** | | | | **+0.5806** | | **+0.0197** | |

**Δ split mediu +0.0197**, sd intre limbi 0.1099, interval -0.1865 pana la +0.1956. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4062 | +0.3673 | -0.0389 |
| de | +0.8031 | +0.8081 | +0.0050 |
| en | +0.7468 | +0.7464 | -0.0004 |
| es | +0.7074 | +0.7044 | -0.0030 |
| fil | +0.5235 | +0.5603 | +0.0368 |
| fr | +0.3642 | +0.3505 | -0.0137 |
| it | +0.7294 | +0.7250 | -0.0044 |
| ja | +0.5623 | +0.5771 | +0.0148 |
| pt | +0.7677 | +0.7753 | +0.0076 |
| si | +0.1953 | +0.2862 | +0.0909 |

**Diferenta medie +0.0095**, interval -0.0389 pana la +0.0909.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4281 | +0.3622 | -0.0009 | +0.0440 |
| de | +0.6386 | +0.8202 | -0.0311 | -0.0171 |
| en | +0.7989 | +0.7171 | +0.0063 | +0.0297 |
| es | +0.6947 | +0.7152 | -0.0134 | -0.0078 |
| fil | +0.4002 | +0.5687 | -0.0090 | -0.0452 |
| fr | +0.5341 | +0.2643 | +0.0167 | +0.0999 |
| it | +0.6246 | +0.7511 | -0.0119 | -0.0217 |
| ja | +0.5719 | +0.5330 | -0.0481 | +0.0293 |
| pt | +0.7760 | +0.7478 | -0.0114 | +0.0199 |
| si | +0.1848 | +0.1722 | +0.0602 | +0.0231 |
