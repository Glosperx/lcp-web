# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:22:34 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4116 | [+0.3240, +0.4959] | 30 | 11 | +0.1710 | [-0.2363, +0.5989] | -0.2406 | [-0.6604, +0.1915] |
| de | 570 | 193 | +0.6206 | [+0.5619, +0.6733] | 23 | 11 | +0.6900 | [+0.4637, +0.8396] | +0.0694 | [-0.1673, +0.2293] |
| en | 570 | 190 | +0.7822 | [+0.7372, +0.8190] | 30 | 10 | +0.6678 | [+0.4587, +0.8214] | -0.1144 | [-0.3257, +0.0434] |
| es | 593 | 208 | +0.6306 | [+0.5807, +0.6751] | 30 | 10 | +0.6790 | [+0.3761, +0.8423] | +0.0484 | [-0.2598, +0.2198] |
| fil | 570 | 555 | +0.4057 | [+0.3370, +0.4710] | 30 | 30 | +0.5002 | [+0.2200, +0.7018] | +0.0944 | [-0.1946, +0.3178] |
| fr | 569 | 191 | +0.4912 | [+0.4237, +0.5522] | 30 | 11 | +0.2459 | [-0.1185, +0.5873] | -0.2453 | [-0.6165, +0.1015] |
| it | 570 | 192 | +0.5989 | [+0.5402, +0.6558] | 30 | 10 | +0.6152 | [+0.3521, +0.8001] | +0.0163 | [-0.2483, +0.2130] |
| ja | 570 | 190 | +0.6159 | [+0.5544, +0.6718] | 30 | 10 | +0.5344 | [+0.3644, +0.6557] | -0.0815 | [-0.2620, +0.0506] |
| pt | 567 | 562 | +0.7172 | [+0.6679, +0.7605] | 30 | 30 | +0.7665 | [+0.5924, +0.8918] | +0.0493 | [-0.1278, +0.1819] |
| si | 600 | 578 | +0.2599 | [+0.2011, +0.3221] | 30 | 30 | +0.0682 | [-0.2967, +0.4468] | -0.1917 | [-0.5610, +0.1936] |
| **medie** | | | **+0.5534** | | | | **+0.4938** | | **-0.0596** | |

**Δ split mediu -0.0596**, sd intre limbi 0.1324, interval -0.2453 pana la +0.0944. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1710 | +0.1710 | +0.0000 |
| de | +0.6900 | +0.6900 | +0.0000 |
| en | +0.6678 | +0.6678 | +0.0000 |
| es | +0.6790 | +0.6790 | +0.0000 |
| fil | +0.5002 | +0.5002 | +0.0000 |
| fr | +0.2459 | +0.2459 | +0.0000 |
| it | +0.6152 | +0.6152 | +0.0000 |
| ja | +0.5344 | +0.5344 | +0.0000 |
| pt | +0.7665 | +0.7665 | +0.0000 |
| si | +0.0682 | +0.0682 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3862 | +0.1734 | +0.0254 | -0.0024 |
| de | +0.6376 | +0.7727 | -0.0170 | -0.0827 |
| en | +0.7849 | +0.6252 | -0.0027 | +0.0426 |
| es | +0.6234 | +0.7272 | +0.0072 | -0.0482 |
| fil | +0.4090 | +0.4756 | -0.0033 | +0.0246 |
| fr | +0.5020 | +0.3203 | -0.0108 | -0.0744 |
| it | +0.6014 | +0.6336 | -0.0025 | -0.0184 |
| ja | +0.5792 | +0.4585 | +0.0367 | +0.0759 |
| pt | +0.7314 | +0.7630 | -0.0142 | +0.0035 |
| si | +0.2658 | +0.1777 | -0.0059 | -0.1095 |
