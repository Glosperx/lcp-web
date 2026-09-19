# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-29 20:18:36 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4514 | [+0.3676, +0.5237] | 30 | 11 | +0.3292 | [-0.2113, +0.7233] | -0.1222 | [-0.6828, +0.2858] |
| de | 570 | 193 | +0.6610 | [+0.6083, +0.7113] | 23 | 11 | +0.7974 | [+0.5480, +0.9081] | +0.1364 | [-0.1375, +0.2627] |
| en | 570 | 190 | +0.8156 | [+0.7786, +0.8468] | 30 | 10 | +0.7004 | [+0.4552, +0.8469] | -0.1151 | [-0.3583, +0.0390] |
| es | 593 | 208 | +0.6814 | [+0.6370, +0.7216] | 30 | 10 | +0.7151 | [+0.4211, +0.8775] | +0.0336 | [-0.2684, +0.2048] |
| fil | 570 | 555 | +0.4125 | [+0.3414, +0.4801] | 30 | 30 | +0.6028 | [+0.3712, +0.7662] | +0.1903 | [-0.0512, +0.3727] |
| fr | 569 | 191 | +0.5396 | [+0.4732, +0.5972] | 30 | 11 | +0.3038 | [-0.0922, +0.6332] | -0.2359 | [-0.6378, +0.1033] |
| it | 570 | 192 | +0.6446 | [+0.5930, +0.6952] | 30 | 10 | +0.6515 | [+0.4310, +0.8103] | +0.0069 | [-0.2207, +0.1785] |
| ja | 570 | 190 | +0.5867 | [+0.5226, +0.6416] | 30 | 10 | +0.5319 | [+0.3330, +0.6775] | -0.0548 | [-0.2613, +0.0971] |
| pt | 567 | 562 | +0.7703 | [+0.7293, +0.8059] | 30 | 30 | +0.8003 | [+0.6551, +0.9126] | +0.0299 | [-0.1209, +0.1482] |
| ro | 1587 | 274 | +0.7131 | [+0.6811, +0.7432] | 0 | 0 | +nan | [+nan, +nan] | +nan | [+nan, +nan] |
| si | 600 | 578 | +0.2353 | [+0.1719, +0.3021] | 30 | 30 | +0.0141 | [-0.3640, +0.4212] | -0.2212 | [-0.6017, +0.1852] |
| **medie** | | | **+0.5920** | | | | **+0.5446** | | **+nan** | |

**Δ split mediu +nan**, sd intre limbi nan, interval +nan pana la +nan. Trial-ul e mai mare pe 5 din 11 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3292 | +0.3133 | -0.0159 |
| de | +0.7974 | +0.7841 | -0.0133 |
| en | +0.7004 | +0.6782 | -0.0222 |
| es | +0.7151 | +0.6990 | -0.0161 |
| fil | +0.6028 | +0.6037 | +0.0009 |
| fr | +0.3038 | +0.2649 | -0.0389 |
| it | +0.6515 | +0.6402 | -0.0113 |
| ja | +0.5319 | +0.4751 | -0.0568 |
| pt | +0.8003 | +0.7934 | -0.0069 |
| ro | +nan | +nan | +nan |
| si | +0.0141 | +0.0411 | +0.0270 |

**Diferenta medie +nan**, interval +nan pana la +nan.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4143 | +0.2181 | +0.0371 | +0.1111 |
| de | +0.6629 | +0.8346 | -0.0019 | -0.0372 |
| en | +0.8075 | +0.6869 | +0.0081 | +0.0135 |
| es | +0.6516 | +0.6903 | +0.0298 | +0.0248 |
| fil | +0.4158 | +0.5589 | -0.0033 | +0.0439 |
| fr | +0.5296 | +0.3348 | +0.0100 | -0.0310 |
| it | +0.6243 | +0.6861 | +0.0203 | -0.0346 |
| ja | +0.6027 | +0.4618 | -0.0160 | +0.0701 |
| pt | +0.7669 | +0.7842 | +0.0034 | +0.0161 |
| ro | +0.7148 | +nan | -0.0017 | +nan |
| si | +0.2737 | -0.0412 | -0.0384 | +0.0553 |
