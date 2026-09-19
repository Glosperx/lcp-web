# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:24:49 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4149 | [+0.3277, +0.4953] | 30 | 11 | +0.1627 | [-0.2798, +0.5854] | -0.2522 | [-0.7047, +0.1839] |
| de | 570 | 193 | +0.6056 | [+0.5454, +0.6602] | 23 | 11 | +0.7475 | [+0.4925, +0.8621] | +0.1418 | [-0.1263, +0.2718] |
| en | 570 | 190 | +0.7660 | [+0.7220, +0.8026] | 30 | 10 | +0.6518 | [+0.4004, +0.7840] | -0.1142 | [-0.3684, +0.0301] |
| es | 593 | 208 | +0.6163 | [+0.5635, +0.6620] | 30 | 10 | +0.5745 | [+0.2080, +0.7838] | -0.0418 | [-0.4102, +0.1777] |
| fil | 570 | 555 | +0.3865 | [+0.3167, +0.4541] | 30 | 30 | +0.5915 | [+0.3599, +0.7494] | +0.2050 | [-0.0376, +0.3807] |
| fr | 569 | 191 | +0.4958 | [+0.4321, +0.5556] | 30 | 11 | +0.2302 | [-0.1726, +0.5936] | -0.2656 | [-0.6825, +0.0969] |
| it | 570 | 192 | +0.6058 | [+0.5509, +0.6602] | 30 | 10 | +0.5929 | [+0.3650, +0.7924] | -0.0130 | [-0.2477, +0.1930] |
| ja | 570 | 190 | +0.5995 | [+0.5408, +0.6547] | 30 | 10 | +0.5939 | [+0.4294, +0.7006] | -0.0056 | [-0.1810, +0.1109] |
| pt | 567 | 562 | +0.7260 | [+0.6817, +0.7659] | 30 | 30 | +0.7784 | [+0.6075, +0.9029] | +0.0524 | [-0.1197, +0.1809] |
| si | 600 | 578 | +0.2527 | [+0.1893, +0.3180] | 30 | 30 | +0.0245 | [-0.3360, +0.4576] | -0.2282 | [-0.5943, +0.2108] |
| **medie** | | | **+0.5469** | | | | **+0.4948** | | **-0.0521** | |

**Δ split mediu -0.0521**, sd intre limbi 0.1629, interval -0.2656 pana la +0.2050. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1627 | +0.1627 | +0.0000 |
| de | +0.7475 | +0.7475 | +0.0000 |
| en | +0.6518 | +0.6518 | +0.0000 |
| es | +0.5745 | +0.5745 | +0.0000 |
| fil | +0.5915 | +0.5915 | +0.0000 |
| fr | +0.2302 | +0.2302 | +0.0000 |
| it | +0.5929 | +0.5929 | +0.0000 |
| ja | +0.5939 | +0.5939 | +0.0000 |
| pt | +0.7784 | +0.7784 | +0.0000 |
| si | +0.0245 | +0.0245 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3739 | +0.1512 | +0.0410 | +0.0115 |
| de | +0.6163 | +0.7911 | -0.0107 | -0.0436 |
| en | +0.7545 | +0.6071 | +0.0115 | +0.0447 |
| es | +0.5907 | +0.6363 | +0.0256 | -0.0618 |
| fil | +0.4003 | +0.5128 | -0.0138 | +0.0787 |
| fr | +0.4741 | +0.2042 | +0.0217 | +0.0260 |
| it | +0.5770 | +0.5690 | +0.0288 | +0.0239 |
| ja | +0.5284 | +0.3718 | +0.0711 | +0.2221 |
| pt | +0.7300 | +0.7857 | -0.0040 | -0.0073 |
| si | +0.2465 | -0.0117 | +0.0062 | +0.0362 |
