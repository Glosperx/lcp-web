# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:38:35 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4282 | [+0.3340, +0.5135] | 30 | 11 | +0.4223 | [+0.0944, +0.6776] | -0.0058 | [-0.3497, +0.2604] |
| de | 570 | 193 | +0.5642 | [+0.5010, +0.6202] | 23 | 11 | +0.8064 | [+0.6065, +0.9143] | +0.2422 | [+0.0339, +0.3667] |
| en | 570 | 190 | +0.7864 | [+0.7507, +0.8199] | 30 | 10 | +0.6743 | [+0.4313, +0.8659] | -0.1121 | [-0.3574, +0.0845] |
| es | 593 | 208 | +0.6949 | [+0.6494, +0.7341] | 30 | 10 | +0.6789 | [+0.3362, +0.8890] | -0.0160 | [-0.3450, +0.2000] |
| fil | 570 | 555 | +0.4299 | [+0.3599, +0.4935] | 30 | 30 | +0.5210 | [+0.2441, +0.7300] | +0.0912 | [-0.1923, +0.3142] |
| fr | 569 | 191 | +0.5310 | [+0.4702, +0.5926] | 30 | 11 | +0.3101 | [+0.0638, +0.5181] | -0.2209 | [-0.4810, -0.0092] |
| it | 570 | 192 | +0.5919 | [+0.5394, +0.6465] | 30 | 10 | +0.6278 | [+0.3687, +0.8213] | +0.0358 | [-0.2341, +0.2423] |
| ja | 570 | 190 | +0.5776 | [+0.5087, +0.6442] | 30 | 10 | +0.7030 | [+0.5034, +0.8405] | +0.1254 | [-0.0879, +0.2778] |
| pt | 567 | 562 | +0.7230 | [+0.6709, +0.7664] | 30 | 30 | +0.6832 | [+0.4733, +0.8371] | -0.0398 | [-0.2544, +0.1246] |
| si | 600 | 578 | +0.2250 | [+0.1618, +0.2906] | 30 | 30 | +0.3546 | [+0.0681, +0.5829] | +0.1296 | [-0.1687, +0.3740] |
| **medie** | | | **+0.5552** | | | | **+0.5782** | | **+0.0230** | |

**Δ split mediu +0.0230**, sd intre limbi 0.1328, interval -0.2209 pana la +0.2422. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4223 | +0.4223 | +0.0000 |
| de | +0.8064 | +0.8064 | +0.0000 |
| en | +0.6743 | +0.6743 | +0.0000 |
| es | +0.6789 | +0.6789 | +0.0000 |
| fil | +0.5210 | +0.5210 | +0.0000 |
| fr | +0.3101 | +0.3101 | +0.0000 |
| it | +0.6278 | +0.6278 | +0.0000 |
| ja | +0.7030 | +0.7030 | +0.0000 |
| pt | +0.6832 | +0.6832 | +0.0000 |
| si | +0.3546 | +0.3546 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4152 | +0.5008 | +0.0130 | -0.0785 |
| de | +0.6043 | +0.8198 | -0.0401 | -0.0134 |
| en | +0.7782 | +0.6219 | +0.0082 | +0.0524 |
| es | +0.6841 | +0.6813 | +0.0108 | -0.0024 |
| fil | +0.4201 | +0.5216 | +0.0098 | -0.0006 |
| fr | +0.5158 | +0.2598 | +0.0152 | +0.0503 |
| it | +0.5999 | +0.6706 | -0.0080 | -0.0428 |
| ja | +0.5014 | +0.5415 | +0.0762 | +0.1615 |
| pt | +0.7415 | +0.7045 | -0.0185 | -0.0213 |
| si | +0.2312 | +0.3010 | -0.0062 | +0.0536 |
