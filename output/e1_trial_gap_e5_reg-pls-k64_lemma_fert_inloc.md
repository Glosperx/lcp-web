# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:41:17 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4327 | [+0.3332, +0.5183] | 30 | 11 | +0.3489 | [-0.0137, +0.6212] | -0.0837 | [-0.4584, +0.2001] |
| de | 570 | 193 | +0.5843 | [+0.5232, +0.6405] | 23 | 11 | +0.8235 | [+0.5915, +0.9283] | +0.2392 | [-0.0005, +0.3615] |
| en | 570 | 190 | +0.7776 | [+0.7382, +0.8128] | 30 | 10 | +0.6444 | [+0.3768, +0.8342] | -0.1332 | [-0.4030, +0.0609] |
| es | 593 | 208 | +0.6842 | [+0.6406, +0.7233] | 30 | 10 | +0.6487 | [+0.2810, +0.8855] | -0.0355 | [-0.3978, +0.2068] |
| fil | 570 | 555 | +0.3991 | [+0.3273, +0.4669] | 30 | 30 | +0.5374 | [+0.2714, +0.7373] | +0.1384 | [-0.1347, +0.3542] |
| fr | 569 | 191 | +0.5298 | [+0.4676, +0.5911] | 30 | 11 | +0.3190 | [+0.0846, +0.5357] | -0.2108 | [-0.4539, +0.0208] |
| it | 570 | 192 | +0.6105 | [+0.5569, +0.6640] | 30 | 10 | +0.5972 | [+0.3392, +0.7965] | -0.0133 | [-0.2807, +0.1966] |
| ja | 570 | 190 | +0.5913 | [+0.5255, +0.6527] | 30 | 10 | +0.7408 | [+0.5697, +0.8552] | +0.1495 | [-0.0350, +0.2854] |
| pt | 567 | 562 | +0.7145 | [+0.6626, +0.7582] | 30 | 30 | +0.6763 | [+0.4607, +0.8312] | -0.0381 | [-0.2622, +0.1217] |
| si | 600 | 578 | +0.1827 | [+0.1137, +0.2543] | 30 | 30 | +0.3724 | [+0.1776, +0.6125] | +0.1897 | [-0.0182, +0.4473] |
| **medie** | | | **+0.5507** | | | | **+0.5709** | | **+0.0202** | |

**Δ split mediu +0.0202**, sd intre limbi 0.1501, interval -0.2108 pana la +0.2392. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3489 | +0.3489 | +0.0000 |
| de | +0.8235 | +0.8235 | +0.0000 |
| en | +0.6444 | +0.6444 | +0.0000 |
| es | +0.6487 | +0.6487 | +0.0000 |
| fil | +0.5374 | +0.5374 | +0.0000 |
| fr | +0.3190 | +0.3190 | +0.0000 |
| it | +0.5972 | +0.5972 | +0.0000 |
| ja | +0.7408 | +0.7408 | +0.0000 |
| pt | +0.6763 | +0.6763 | +0.0000 |
| si | +0.3724 | +0.3724 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4146 | +0.3905 | +0.0181 | -0.0416 |
| de | +0.6337 | +0.8425 | -0.0494 | -0.0190 |
| en | +0.7556 | +0.5565 | +0.0220 | +0.0879 |
| es | +0.6378 | +0.6124 | +0.0464 | +0.0363 |
| fil | +0.3977 | +0.5153 | +0.0014 | +0.0221 |
| fr | +0.5151 | +0.1793 | +0.0147 | +0.1397 |
| it | +0.5862 | +0.6416 | +0.0243 | -0.0444 |
| ja | +0.4876 | +0.6505 | +0.1037 | +0.0903 |
| pt | +0.7304 | +0.7128 | -0.0159 | -0.0365 |
| si | +0.1732 | +0.2391 | +0.0095 | +0.1333 |
