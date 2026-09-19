# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:54:41 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3759 | [+0.2886, +0.4525] | 30 | 11 | +0.0497 | [-0.3919, +0.4955] | -0.3261 | [-0.7773, +0.1281] |
| de | 570 | 193 | +0.5703 | [+0.5082, +0.6284] | 23 | 11 | +0.7431 | [+0.5843, +0.8579] | +0.1728 | [+0.0068, +0.3012] |
| en | 570 | 190 | +0.7638 | [+0.7172, +0.8035] | 30 | 10 | +0.6551 | [+0.3132, +0.8158] | -0.1087 | [-0.4438, +0.0604] |
| es | 593 | 208 | +0.6274 | [+0.5793, +0.6715] | 30 | 10 | +0.5974 | [+0.2520, +0.7931] | -0.0301 | [-0.3676, +0.1763] |
| fil | 570 | 555 | +0.4031 | [+0.3324, +0.4676] | 30 | 30 | +0.4949 | [+0.2121, +0.7279] | +0.0918 | [-0.1904, +0.3372] |
| fr | 569 | 191 | +0.4875 | [+0.4174, +0.5552] | 30 | 11 | +0.3112 | [-0.1306, +0.6528] | -0.1763 | [-0.6375, +0.1763] |
| it | 570 | 192 | +0.5892 | [+0.5313, +0.6500] | 30 | 10 | +0.5528 | [+0.2941, +0.7881] | -0.0364 | [-0.3025, +0.2083] |
| ja | 570 | 190 | +0.4757 | [+0.4047, +0.5432] | 30 | 10 | +0.5209 | [+0.3257, +0.6779] | +0.0453 | [-0.1614, +0.2106] |
| pt | 567 | 562 | +0.7231 | [+0.6795, +0.7631] | 30 | 30 | +0.7596 | [+0.5474, +0.8894] | +0.0365 | [-0.1728, +0.1736] |
| si | 600 | 578 | +0.2164 | [+0.1630, +0.2699] | 30 | 30 | +0.1713 | [-0.1670, +0.4087] | -0.0451 | [-0.3906, +0.2052] |
| **medie** | | | **+0.5232** | | | | **+0.4856** | | **-0.0376** | |

**Δ split mediu -0.0376**, sd intre limbi 0.1418, interval -0.3261 pana la +0.1728. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.0497 | +0.0620 | +0.0123 |
| de | +0.7431 | +0.7442 | +0.0011 |
| en | +0.6551 | +0.6564 | +0.0013 |
| es | +0.5974 | +0.6055 | +0.0081 |
| fil | +0.4949 | +0.4897 | -0.0052 |
| fr | +0.3112 | +0.3235 | +0.0123 |
| it | +0.5528 | +0.5568 | +0.0040 |
| ja | +0.5209 | +0.5255 | +0.0046 |
| pt | +0.7596 | +0.7637 | +0.0041 |
| si | +0.1713 | +0.1695 | -0.0018 |

**Diferenta medie +0.0041**, interval -0.0052 pana la +0.0123.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3366 | +0.0203 | +0.0393 | +0.0294 |
| de | +0.5238 | +0.8373 | +0.0465 | -0.0942 |
| en | +0.7340 | +0.5541 | +0.0298 | +0.1010 |
| es | +0.5851 | +0.5378 | +0.0423 | +0.0596 |
| fil | +0.4048 | +0.4481 | -0.0017 | +0.0468 |
| fr | +0.4605 | +0.3783 | +0.0270 | -0.0671 |
| it | +0.5399 | +0.5968 | +0.0493 | -0.0440 |
| ja | +0.5511 | +0.4431 | -0.0754 | +0.0778 |
| pt | +0.7128 | +0.7044 | +0.0103 | +0.0552 |
| si | +0.1049 | +0.0657 | +0.1115 | +0.1056 |
