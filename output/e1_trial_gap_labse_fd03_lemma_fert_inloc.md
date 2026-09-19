# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:49:36 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4768 | [+0.3966, +0.5512] | 30 | 11 | +0.4589 | [+0.1721, +0.6971] | -0.0179 | [-0.3103, +0.2350] |
| de | 570 | 193 | +0.5567 | [+0.4965, +0.6108] | 23 | 11 | +0.7697 | [+0.4725, +0.9108] | +0.2130 | [-0.0769, +0.3766] |
| en | 570 | 190 | +0.8047 | [+0.7693, +0.8363] | 30 | 10 | +0.6987 | [+0.6009, +0.8599] | -0.1060 | [-0.2094, +0.0609] |
| es | 593 | 208 | +0.6447 | [+0.5984, +0.6862] | 30 | 10 | +0.6883 | [+0.4887, +0.8190] | +0.0436 | [-0.1617, +0.1806] |
| fil | 570 | 555 | +0.3923 | [+0.3215, +0.4628] | 30 | 30 | +0.4496 | [+0.1961, +0.6671] | +0.0572 | [-0.2000, +0.2834] |
| fr | 569 | 191 | +0.5365 | [+0.4775, +0.5948] | 30 | 11 | +0.5406 | [+0.2980, +0.7213] | +0.0041 | [-0.2543, +0.1936] |
| it | 570 | 192 | +0.5640 | [+0.5071, +0.6196] | 30 | 10 | +0.7075 | [+0.5202, +0.8282] | +0.1435 | [-0.0520, +0.2819] |
| ja | 570 | 190 | +0.5567 | [+0.4835, +0.6241] | 30 | 10 | +0.6273 | [+0.3305, +0.8010] | +0.0706 | [-0.2352, +0.2589] |
| pt | 567 | 562 | +0.7335 | [+0.6931, +0.7696] | 30 | 30 | +0.7071 | [+0.4837, +0.9080] | -0.0264 | [-0.2445, +0.1676] |
| si | 600 | 578 | +0.3587 | [+0.2868, +0.4240] | 30 | 30 | +0.3240 | [-0.1179, +0.5938] | -0.0346 | [-0.4724, +0.2536] |
| **medie** | | | **+0.5625** | | | | **+0.5972** | | **+0.0347** | |

**Δ split mediu +0.0347**, sd intre limbi 0.0928, interval -0.1060 pana la +0.2130. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4589 | +0.4196 | -0.0393 |
| de | +0.7697 | +0.7410 | -0.0287 |
| en | +0.6987 | +0.6896 | -0.0091 |
| es | +0.6883 | +0.6980 | +0.0097 |
| fil | +0.4496 | +0.4931 | +0.0435 |
| fr | +0.5406 | +0.5462 | +0.0056 |
| it | +0.7075 | +0.7097 | +0.0022 |
| ja | +0.6273 | +0.6013 | -0.0260 |
| pt | +0.7071 | +0.7077 | +0.0006 |
| si | +0.3240 | +0.3587 | +0.0347 |

**Diferenta medie -0.0007**, interval -0.0393 pana la +0.0435.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4317 | +0.5202 | +0.0451 | -0.0613 |
| de | +0.5387 | +0.7948 | +0.0180 | -0.0251 |
| en | +0.7998 | +0.7241 | +0.0049 | -0.0254 |
| es | +0.6661 | +0.6673 | -0.0214 | +0.0210 |
| fil | +0.4278 | +0.5149 | -0.0355 | -0.0653 |
| fr | +0.4975 | +0.4163 | +0.0390 | +0.1243 |
| it | +0.5432 | +0.7209 | +0.0208 | -0.0134 |
| ja | +0.5491 | +0.5242 | +0.0076 | +0.1031 |
| pt | +0.7230 | +0.7268 | +0.0105 | -0.0197 |
| si | +0.3352 | +0.3823 | +0.0235 | -0.0583 |
