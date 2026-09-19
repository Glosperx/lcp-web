# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:44:37 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3990 | [+0.3112, +0.4806] | 30 | 11 | +0.1517 | [-0.3217, +0.5977] | -0.2474 | [-0.7204, +0.2125] |
| de | 570 | 193 | +0.5898 | [+0.5231, +0.6510] | 23 | 11 | +0.7231 | [+0.4325, +0.8540] | +0.1334 | [-0.1725, +0.2812] |
| en | 570 | 190 | +0.7810 | [+0.7365, +0.8188] | 30 | 10 | +0.7073 | [+0.4295, +0.8380] | -0.0738 | [-0.3511, +0.0665] |
| es | 593 | 208 | +0.6239 | [+0.5685, +0.6731] | 30 | 10 | +0.6223 | [+0.2878, +0.7997] | -0.0016 | [-0.3384, +0.1870] |
| fil | 570 | 555 | +0.3991 | [+0.3278, +0.4680] | 30 | 30 | +0.5803 | [+0.3386, +0.7442] | +0.1812 | [-0.0737, +0.3644] |
| fr | 569 | 191 | +0.4925 | [+0.4234, +0.5564] | 30 | 11 | +0.2493 | [-0.1551, +0.5983] | -0.2432 | [-0.6558, +0.1132] |
| it | 570 | 192 | +0.5972 | [+0.5376, +0.6545] | 30 | 10 | +0.5848 | [+0.3549, +0.7953] | -0.0124 | [-0.2462, +0.2026] |
| ja | 570 | 190 | +0.5974 | [+0.5348, +0.6547] | 30 | 10 | +0.5789 | [+0.4061, +0.7005] | -0.0184 | [-0.1987, +0.1154] |
| pt | 567 | 562 | +0.7271 | [+0.6841, +0.7657] | 30 | 30 | +0.7830 | [+0.6003, +0.9053] | +0.0559 | [-0.1284, +0.1816] |
| si | 600 | 578 | +0.2672 | [+0.2073, +0.3289] | 30 | 30 | +0.0762 | [-0.3071, +0.5405] | -0.1910 | [-0.5785, +0.2736] |
| **medie** | | | **+0.5474** | | | | **+0.5057** | | **-0.0417** | |

**Δ split mediu -0.0417**, sd intre limbi 0.1487, interval -0.2474 pana la +0.1812. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1517 | +0.1540 | +0.0023 |
| de | +0.7231 | +0.7245 | +0.0014 |
| en | +0.7073 | +0.7079 | +0.0006 |
| es | +0.6223 | +0.6227 | +0.0004 |
| fil | +0.5803 | +0.5780 | -0.0023 |
| fr | +0.2493 | +0.2496 | +0.0003 |
| it | +0.5848 | +0.5832 | -0.0016 |
| ja | +0.5789 | +0.5789 | +0.0000 |
| pt | +0.7830 | +0.7822 | -0.0008 |
| si | +0.0762 | +0.0728 | -0.0034 |

**Diferenta medie -0.0003**, interval -0.0034 pana la +0.0023.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3721 | +0.1758 | +0.0269 | -0.0241 |
| de | +0.6151 | +0.7657 | -0.0253 | -0.0426 |
| en | +0.7775 | +0.6490 | +0.0035 | +0.0583 |
| es | +0.6019 | +0.6263 | +0.0220 | -0.0040 |
| fil | +0.4150 | +0.4845 | -0.0159 | +0.0958 |
| fr | +0.4623 | +0.2468 | +0.0302 | +0.0025 |
| it | +0.5863 | +0.5926 | +0.0109 | -0.0078 |
| ja | +0.5464 | +0.3922 | +0.0510 | +0.1867 |
| pt | +0.7346 | +0.7862 | -0.0075 | -0.0032 |
| si | +0.2681 | +0.1042 | -0.0009 | -0.0280 |
