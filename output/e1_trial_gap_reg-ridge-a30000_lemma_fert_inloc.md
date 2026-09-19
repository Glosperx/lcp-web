# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:32:56 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3741 | [+0.2816, +0.4636] | 30 | 11 | +0.1896 | [-0.1590, +0.6000] | -0.1845 | [-0.5381, +0.2401] |
| de | 570 | 193 | +0.5906 | [+0.5296, +0.6482] | 23 | 11 | +0.6142 | [+0.2990, +0.8286] | +0.0236 | [-0.2984, +0.2434] |
| en | 570 | 190 | +0.7530 | [+0.7002, +0.7960] | 30 | 10 | +0.5974 | [+0.4234, +0.8134] | -0.1555 | [-0.3341, +0.0623] |
| es | 593 | 208 | +0.6158 | [+0.5672, +0.6629] | 30 | 10 | +0.6771 | [+0.3696, +0.8503] | +0.0613 | [-0.2422, +0.2426] |
| fil | 570 | 555 | +0.3324 | [+0.2613, +0.3984] | 30 | 30 | +0.3779 | [+0.0697, +0.6222] | +0.0455 | [-0.2656, +0.3042] |
| fr | 569 | 191 | +0.4972 | [+0.4288, +0.5600] | 30 | 11 | +0.3145 | [-0.0309, +0.6296] | -0.1828 | [-0.5380, +0.1256] |
| it | 570 | 192 | +0.5659 | [+0.5052, +0.6267] | 30 | 10 | +0.6425 | [+0.3710, +0.8271] | +0.0766 | [-0.1973, +0.2776] |
| ja | 570 | 190 | +0.5750 | [+0.5128, +0.6381] | 30 | 10 | +0.4230 | [+0.1760, +0.6399] | -0.1519 | [-0.3998, +0.0706] |
| pt | 567 | 562 | +0.6943 | [+0.6448, +0.7393] | 30 | 30 | +0.7412 | [+0.5537, +0.8778] | +0.0469 | [-0.1442, +0.1916] |
| si | 600 | 578 | +0.2248 | [+0.1608, +0.2901] | 30 | 30 | +0.0599 | [-0.2531, +0.3626] | -0.1649 | [-0.4829, +0.1469] |
| **medie** | | | **+0.5223** | | | | **+0.4637** | | **-0.0586** | |

**Δ split mediu -0.0586**, sd intre limbi 0.1165, interval -0.1845 pana la +0.0766. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1896 | +0.1896 | +0.0000 |
| de | +0.6142 | +0.6142 | +0.0000 |
| en | +0.5974 | +0.5974 | +0.0000 |
| es | +0.6771 | +0.6771 | +0.0000 |
| fil | +0.3779 | +0.3779 | +0.0000 |
| fr | +0.3145 | +0.3145 | +0.0000 |
| it | +0.6425 | +0.6425 | +0.0000 |
| ja | +0.4230 | +0.4230 | +0.0000 |
| pt | +0.7412 | +0.7412 | +0.0000 |
| si | +0.0599 | +0.0599 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3544 | +0.1831 | +0.0197 | +0.0065 |
| de | +0.6025 | +0.6698 | -0.0119 | -0.0556 |
| en | +0.7494 | +0.6146 | +0.0036 | -0.0172 |
| es | +0.6022 | +0.6930 | +0.0136 | -0.0159 |
| fil | +0.3415 | +0.3749 | -0.0091 | +0.0030 |
| fr | +0.5089 | +0.3733 | -0.0117 | -0.0588 |
| it | +0.5751 | +0.6575 | -0.0092 | -0.0150 |
| ja | +0.5392 | +0.3905 | +0.0358 | +0.0325 |
| pt | +0.6982 | +0.7370 | -0.0039 | +0.0042 |
| si | +0.2350 | +0.1036 | -0.0102 | -0.0437 |
