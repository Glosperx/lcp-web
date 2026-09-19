# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-18 12:02:04 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4470 | [+0.3672, +0.5208] | 30 | 11 | +0.3161 | [-0.2285, +0.7015] | -0.1309 | [-0.6794, +0.2642] |
| de | 570 | 193 | +0.6551 | [+0.6016, +0.7039] | 23 | 11 | +0.7817 | [+0.5185, +0.8995] | +0.1266 | [-0.1540, +0.2616] |
| en | 570 | 190 | +0.8147 | [+0.7765, +0.8459] | 30 | 10 | +0.7240 | [+0.5023, +0.8534] | -0.0907 | [-0.3133, +0.0486] |
| es | 593 | 208 | +0.6686 | [+0.6213, +0.7114] | 28 | 10 | +0.7833 | [+0.6267, +0.8887] | +0.1147 | [-0.0417, +0.2269] |
| fil | 568 | 553 | +0.4091 | [+0.3392, +0.4758] | 30 | 30 | +0.5920 | [+0.3555, +0.7659] | +0.1828 | [-0.0658, +0.3702] |
| fr | 566 | 191 | +0.5305 | [+0.4634, +0.5908] | 30 | 11 | +0.2909 | [-0.1045, +0.6177] | -0.2396 | [-0.6392, +0.1009] |
| it | 562 | 192 | +0.6336 | [+0.5792, +0.6880] | 29 | 10 | +0.6591 | [+0.4246, +0.8200] | +0.0256 | [-0.2117, +0.2017] |
| ja | 570 | 190 | +0.4890 | [+0.4149, +0.5531] | 30 | 10 | +0.3704 | [+0.1039, +0.5670] | -0.1185 | [-0.3919, +0.0954] |
| pt | 562 | 557 | +0.7705 | [+0.7283, +0.8067] | 30 | 30 | +0.8038 | [+0.6542, +0.9151] | +0.0333 | [-0.1215, +0.1530] |
| si | 600 | 578 | +0.2119 | [+0.1446, +0.2820] | 30 | 30 | +0.0358 | [-0.3623, +0.4500] | -0.1760 | [-0.5786, +0.2455] |
| **medie** | | | **+0.5630** | | | | **+0.5357** | | **-0.0273** | |

**Δ split mediu -0.0273**, sd intre limbi 0.1433, interval -0.2396 pana la +0.1828. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3161 | +0.2883 | -0.0278 |
| de | +0.7817 | +0.7785 | -0.0032 |
| en | +0.7240 | +0.7065 | -0.0175 |
| es | +0.7833 | +0.7837 | +0.0004 |
| fil | +0.5920 | +0.5888 | -0.0032 |
| fr | +0.2909 | +0.2704 | -0.0205 |
| it | +0.6591 | +0.6653 | +0.0062 |
| ja | +0.3704 | +0.3608 | -0.0096 |
| pt | +0.8038 | +0.8024 | -0.0014 |
| si | +0.0358 | +0.0316 | -0.0042 |

**Diferenta medie -0.0081**, interval -0.0278 pana la +0.0062.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4163 | +0.2375 | +0.0307 | +0.0786 |
| de | +0.6615 | +0.8247 | -0.0064 | -0.0430 |
| en | +0.8094 | +0.6859 | +0.0053 | +0.0381 |
| es | +0.6565 | +0.7789 | +0.0121 | +0.0044 |
| fil | +0.4151 | +0.5493 | -0.0060 | +0.0427 |
| fr | +0.5292 | +0.3264 | +0.0013 | -0.0355 |
| it | +0.6265 | +0.6871 | +0.0071 | -0.0280 |
| ja | +0.5346 | +0.3824 | -0.0456 | -0.0120 |
| pt | +0.7792 | +0.7928 | -0.0087 | +0.0110 |
| si | +0.2591 | -0.1102 | -0.0472 | +0.1460 |
