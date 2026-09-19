# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 12:41:28 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4097 | [+0.3284, +0.4806] | 30 | 11 | +0.3986 | [-0.1584, +0.7594] | -0.0112 | [-0.5728, +0.3654] |
| de | 570 | 193 | +0.6347 | [+0.5825, +0.6853] | 23 | 11 | +0.7774 | [+0.4918, +0.9135] | +0.1427 | [-0.1460, +0.2941] |
| en | 570 | 190 | +0.8179 | [+0.7789, +0.8511] | 30 | 10 | +0.7169 | [+0.4960, +0.8854] | -0.1010 | [-0.3275, +0.0726] |
| es | 593 | 208 | +0.6638 | [+0.6204, +0.7029] | 30 | 10 | +0.7072 | [+0.4485, +0.8672] | +0.0433 | [-0.2205, +0.2087] |
| fil | 570 | 555 | +0.4085 | [+0.3378, +0.4738] | 30 | 30 | +0.6074 | [+0.3685, +0.8184] | +0.1988 | [-0.0452, +0.4169] |
| fr | 569 | 191 | +0.5401 | [+0.4698, +0.6029] | 30 | 11 | +0.4081 | [+0.0381, +0.6723] | -0.1320 | [-0.5022, +0.1505] |
| it | 570 | 192 | +0.6115 | [+0.5548, +0.6687] | 30 | 10 | +0.7089 | [+0.4800, +0.8559] | +0.0974 | [-0.1340, +0.2607] |
| ja | 570 | 190 | +0.4312 | [+0.3577, +0.4994] | 30 | 10 | +0.2943 | [-0.0460, +0.5282] | -0.1369 | [-0.4771, +0.1091] |
| pt | 567 | 562 | +0.7562 | [+0.7177, +0.7931] | 30 | 30 | +0.7851 | [+0.6241, +0.8998] | +0.0289 | [-0.1388, +0.1476] |
| si | 600 | 578 | +0.1983 | [+0.1328, +0.2675] | 30 | 30 | -0.1796 | [-0.6052, +0.3840] | -0.3778 | [-0.8050, +0.1833] |
| **medie** | | | **+0.5472** | | | | **+0.5224** | | **-0.0248** | |

**Δ split mediu -0.0248**, sd intre limbi 0.1684, interval -0.3778 pana la +0.1988. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3986 | +0.3266 | -0.0720 |
| de | +0.7774 | +0.7683 | -0.0091 |
| en | +0.7169 | +0.6899 | -0.0270 |
| es | +0.7072 | +0.6850 | -0.0222 |
| fil | +0.6074 | +0.6133 | +0.0059 |
| fr | +0.4081 | +0.3563 | -0.0518 |
| it | +0.7089 | +0.7032 | -0.0057 |
| ja | +0.2943 | +0.2126 | -0.0817 |
| pt | +0.7851 | +0.7826 | -0.0025 |
| si | -0.1796 | -0.0629 | +0.1167 |

**Diferenta medie -0.0149**, interval -0.0817 pana la +0.1167.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4128 | +0.2885 | -0.0031 | +0.1101 |
| de | +0.6421 | +0.8056 | -0.0074 | -0.0282 |
| en | +0.8116 | +0.7062 | +0.0063 | +0.0107 |
| es | +0.6552 | +0.6624 | +0.0086 | +0.0448 |
| fil | +0.4062 | +0.5521 | +0.0023 | +0.0553 |
| fr | +0.5325 | +0.4016 | +0.0076 | +0.0065 |
| it | +0.6145 | +0.7536 | -0.0030 | -0.0447 |
| ja | +0.6058 | +0.4828 | -0.1746 | -0.1885 |
| pt | +0.7674 | +0.7493 | -0.0112 | +0.0358 |
| si | +0.1905 | -0.1137 | +0.0078 | -0.0659 |
