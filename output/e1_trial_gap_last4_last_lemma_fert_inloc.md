# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:01:20 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4283 | [+0.3445, +0.5064] | 30 | 11 | +0.2009 | [-0.2733, +0.5992] | -0.2274 | [-0.7209, +0.1899] |
| de | 570 | 193 | +0.6198 | [+0.5642, +0.6719] | 23 | 11 | +0.7536 | [+0.4988, +0.8935] | +0.1338 | [-0.1217, +0.2821] |
| en | 570 | 190 | +0.8014 | [+0.7621, +0.8349] | 30 | 10 | +0.6986 | [+0.4606, +0.8688] | -0.1029 | [-0.3416, +0.0727] |
| es | 593 | 208 | +0.6548 | [+0.6073, +0.6981] | 30 | 10 | +0.6629 | [+0.3663, +0.8506] | +0.0081 | [-0.2870, +0.2013] |
| fil | 570 | 555 | +0.4053 | [+0.3332, +0.4737] | 30 | 30 | +0.5870 | [+0.3387, +0.7722] | +0.1817 | [-0.0762, +0.3874] |
| fr | 569 | 191 | +0.5265 | [+0.4584, +0.5872] | 30 | 11 | +0.2981 | [-0.0929, +0.6128] | -0.2285 | [-0.6196, +0.1030] |
| it | 570 | 192 | +0.6133 | [+0.5618, +0.6657] | 30 | 10 | +0.6659 | [+0.4734, +0.8244] | +0.0526 | [-0.1472, +0.2225] |
| ja | 570 | 190 | +0.5486 | [+0.4831, +0.6099] | 30 | 10 | +0.5535 | [+0.2885, +0.7273] | +0.0049 | [-0.2717, +0.1872] |
| pt | 567 | 562 | +0.7505 | [+0.7113, +0.7867] | 30 | 30 | +0.7679 | [+0.5907, +0.9023] | +0.0174 | [-0.1731, +0.1547] |
| si | 600 | 578 | +0.1945 | [+0.1166, +0.2627] | 30 | 30 | -0.0526 | [-0.3618, +0.4125] | -0.2471 | [-0.5603, +0.2241] |
| **medie** | | | **+0.5543** | | | | **+0.5136** | | **-0.0407** | |

**Δ split mediu -0.0407**, sd intre limbi 0.1539, interval -0.2471 pana la +0.1817. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2009 | +0.1397 | -0.0612 |
| de | +0.7536 | +0.7366 | -0.0170 |
| en | +0.6986 | +0.6932 | -0.0054 |
| es | +0.6629 | +0.6642 | +0.0013 |
| fil | +0.5870 | +0.6140 | +0.0270 |
| fr | +0.2981 | +0.2666 | -0.0315 |
| it | +0.6659 | +0.6628 | -0.0031 |
| ja | +0.5535 | +0.5409 | -0.0126 |
| pt | +0.7679 | +0.7785 | +0.0106 |
| si | -0.0526 | +0.0022 | +0.0548 |

**Diferenta medie -0.0037**, interval -0.0612 pana la +0.0548.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3924 | +0.2226 | +0.0359 | -0.0217 |
| de | +0.6445 | +0.8194 | -0.0247 | -0.0658 |
| en | +0.7883 | +0.7259 | +0.0131 | -0.0273 |
| es | +0.6444 | +0.6408 | +0.0104 | +0.0221 |
| fil | +0.4150 | +0.6009 | -0.0097 | -0.0139 |
| fr | +0.5375 | +0.2451 | -0.0110 | +0.0530 |
| it | +0.6173 | +0.6852 | -0.0040 | -0.0193 |
| ja | +0.5859 | +0.4641 | -0.0373 | +0.0894 |
| pt | +0.7554 | +0.7585 | -0.0049 | +0.0094 |
| si | +0.1711 | -0.1282 | +0.0234 | +0.0756 |
