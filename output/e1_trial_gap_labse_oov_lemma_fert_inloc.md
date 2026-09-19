# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:14:25 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4584 | [+0.3873, +0.5253] | 30 | 11 | +0.4057 | [-0.0190, +0.7250] | -0.0527 | [-0.4995, +0.2743] |
| de | 570 | 193 | +0.6093 | [+0.5550, +0.6590] | 23 | 11 | +0.7909 | [+0.5217, +0.9135] | +0.1816 | [-0.0942, +0.3226] |
| en | 570 | 190 | +0.8116 | [+0.7773, +0.8424] | 30 | 10 | +0.7087 | [+0.5856, +0.8306] | -0.1029 | [-0.2265, +0.0264] |
| es | 593 | 208 | +0.6705 | [+0.6252, +0.7120] | 30 | 10 | +0.6981 | [+0.4548, +0.8525] | +0.0277 | [-0.2184, +0.1923] |
| fil | 570 | 555 | +0.3933 | [+0.3205, +0.4604] | 30 | 30 | +0.5437 | [+0.2950, +0.7515] | +0.1504 | [-0.1078, +0.3792] |
| fr | 569 | 191 | +0.5526 | [+0.4918, +0.6095] | 30 | 11 | +0.4748 | [+0.2118, +0.6708] | -0.0777 | [-0.3492, +0.1304] |
| it | 570 | 192 | +0.6057 | [+0.5532, +0.6597] | 30 | 10 | +0.7164 | [+0.5567, +0.8311] | +0.1106 | [-0.0587, +0.2418] |
| ja | 570 | 190 | +0.5467 | [+0.4728, +0.6126] | 30 | 10 | +0.6472 | [+0.3683, +0.8147] | +0.1005 | [-0.1911, +0.2827] |
| pt | 567 | 562 | +0.7643 | [+0.7246, +0.8004] | 30 | 30 | +0.7468 | [+0.5509, +0.8911] | -0.0175 | [-0.2158, +0.1316] |
| si | 600 | 578 | +0.3517 | [+0.2751, +0.4216] | 30 | 30 | +0.2487 | [-0.1659, +0.5838] | -0.1030 | [-0.5192, +0.2401] |
| **medie** | | | **+0.5764** | | | | **+0.5981** | | **+0.0217** | |

**Δ split mediu +0.0217**, sd intre limbi 0.1077, interval -0.1030 pana la +0.1816. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4057 | +0.3447 | -0.0610 |
| de | +0.7909 | +0.7721 | -0.0188 |
| en | +0.7087 | +0.7128 | +0.0041 |
| es | +0.6981 | +0.6830 | -0.0151 |
| fil | +0.5437 | +0.5582 | +0.0145 |
| fr | +0.4748 | +0.4712 | -0.0036 |
| it | +0.7164 | +0.7237 | +0.0073 |
| ja | +0.6472 | +0.6135 | -0.0337 |
| pt | +0.7468 | +0.7462 | -0.0006 |
| si | +0.2487 | +0.2742 | +0.0255 |

**Diferenta medie -0.0081**, interval -0.0610 pana la +0.0255.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4333 | +0.4210 | +0.0251 | -0.0153 |
| de | +0.6452 | +0.8780 | -0.0359 | -0.0871 |
| en | +0.8082 | +0.7046 | +0.0034 | +0.0041 |
| es | +0.6836 | +0.6432 | -0.0131 | +0.0549 |
| fil | +0.4067 | +0.5630 | -0.0134 | -0.0193 |
| fr | +0.5112 | +0.3284 | +0.0414 | +0.1464 |
| it | +0.6195 | +0.7302 | -0.0138 | -0.0138 |
| ja | +0.5790 | +0.5003 | -0.0323 | +0.1469 |
| pt | +0.7616 | +0.7734 | +0.0027 | -0.0266 |
| si | +0.2601 | +0.2628 | +0.0916 | -0.0141 |
