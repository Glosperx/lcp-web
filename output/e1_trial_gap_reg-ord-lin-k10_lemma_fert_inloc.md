# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:49:21 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3964 | [+0.3122, +0.4735] | 30 | 11 | +0.1662 | [-0.2944, +0.6038] | -0.2301 | [-0.6971, +0.2069] |
| de | 570 | 193 | +0.5663 | [+0.5059, +0.6194] | 23 | 11 | +0.7413 | [+0.5464, +0.8872] | +0.1750 | [-0.0172, +0.3313] |
| en | 570 | 190 | +0.7635 | [+0.7193, +0.8004] | 30 | 10 | +0.6396 | [+0.3813, +0.7733] | -0.1239 | [-0.3780, +0.0181] |
| es | 593 | 208 | +0.6261 | [+0.5785, +0.6692] | 30 | 10 | +0.5994 | [+0.2662, +0.8100] | -0.0266 | [-0.3777, +0.1895] |
| fil | 570 | 555 | +0.4159 | [+0.3445, +0.4818] | 30 | 30 | +0.6094 | [+0.3608, +0.7878] | +0.1936 | [-0.0650, +0.3909] |
| fr | 569 | 191 | +0.4930 | [+0.4244, +0.5581] | 30 | 11 | +0.2969 | [-0.1151, +0.6480] | -0.1961 | [-0.6181, +0.1532] |
| it | 570 | 192 | +0.5930 | [+0.5387, +0.6501] | 30 | 10 | +0.5783 | [+0.3457, +0.7947] | -0.0147 | [-0.2496, +0.2099] |
| ja | 570 | 190 | +0.5237 | [+0.4543, +0.5872] | 30 | 10 | +0.5214 | [+0.3561, +0.6512] | -0.0022 | [-0.1769, +0.1402] |
| pt | 567 | 562 | +0.7278 | [+0.6825, +0.7668] | 30 | 30 | +0.7454 | [+0.5378, +0.8858] | +0.0176 | [-0.1879, +0.1660] |
| si | 600 | 578 | +0.2563 | [+0.2031, +0.3087] | 30 | 30 | +0.0575 | [-0.2175, +0.3435] | -0.1988 | [-0.4818, +0.0953] |
| **medie** | | | **+0.5362** | | | | **+0.4955** | | **-0.0406** | |

**Δ split mediu -0.0406**, sd intre limbi 0.1487, interval -0.2301 pana la +0.1936. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1662 | +0.1722 | +0.0060 |
| de | +0.7413 | +0.7299 | -0.0114 |
| en | +0.6396 | +0.6394 | -0.0002 |
| es | +0.5994 | +0.6052 | +0.0058 |
| fil | +0.6094 | +0.6050 | -0.0044 |
| fr | +0.2969 | +0.3031 | +0.0062 |
| it | +0.5783 | +0.5816 | +0.0033 |
| ja | +0.5214 | +0.5208 | -0.0006 |
| pt | +0.7454 | +0.7421 | -0.0033 |
| si | +0.0575 | +0.0533 | -0.0042 |

**Diferenta medie -0.0003**, interval -0.0114 pana la +0.0062.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3667 | +0.0859 | +0.0297 | +0.0803 |
| de | +0.5774 | +0.8033 | -0.0111 | -0.0620 |
| en | +0.7403 | +0.6164 | +0.0232 | +0.0232 |
| es | +0.5872 | +0.5904 | +0.0389 | +0.0090 |
| fil | +0.4144 | +0.5011 | +0.0015 | +0.1083 |
| fr | +0.4836 | +0.3251 | +0.0094 | -0.0282 |
| it | +0.5707 | +0.6397 | +0.0223 | -0.0614 |
| ja | +0.5901 | +0.4653 | -0.0664 | +0.0561 |
| pt | +0.7217 | +0.7062 | +0.0061 | +0.0392 |
| si | +0.2829 | +0.1367 | -0.0266 | -0.0792 |
