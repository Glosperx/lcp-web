# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 12:49:03 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4005 | [+0.3228, +0.4758] | 30 | 11 | +0.4343 | [-0.0293, +0.7426] | +0.0338 | [-0.4419, +0.3577] |
| de | 570 | 193 | +0.6438 | [+0.5926, +0.6923] | 23 | 11 | +0.7246 | [+0.4157, +0.8784] | +0.0807 | [-0.2343, +0.2459] |
| en | 570 | 190 | +0.8065 | [+0.7669, +0.8392] | 30 | 10 | +0.6887 | [+0.4498, +0.8490] | -0.1177 | [-0.3657, +0.0470] |
| es | 593 | 208 | +0.6355 | [+0.5862, +0.6801] | 30 | 10 | +0.6880 | [+0.4569, +0.8317] | +0.0525 | [-0.1817, +0.2027] |
| fil | 570 | 555 | +0.4249 | [+0.3563, +0.4910] | 30 | 30 | +0.5390 | [+0.2917, +0.7531] | +0.1140 | [-0.1395, +0.3355] |
| fr | 569 | 191 | +0.5666 | [+0.5010, +0.6262] | 30 | 11 | +0.3755 | [+0.0385, +0.6381] | -0.1912 | [-0.5430, +0.0796] |
| it | 570 | 192 | +0.6093 | [+0.5509, +0.6666] | 30 | 10 | +0.7028 | [+0.4701, +0.8553] | +0.0934 | [-0.1460, +0.2610] |
| ja | 570 | 190 | +0.6350 | [+0.5785, +0.6884] | 30 | 10 | +0.5845 | [+0.3274, +0.7827] | -0.0505 | [-0.3112, +0.1599] |
| pt | 567 | 562 | +0.7586 | [+0.7198, +0.7940] | 30 | 30 | +0.7707 | [+0.5897, +0.9029] | +0.0121 | [-0.1677, +0.1478] |
| si | 600 | 578 | +0.2099 | [+0.1359, +0.2823] | 30 | 30 | +0.0237 | [-0.3142, +0.4046] | -0.1863 | [-0.5297, +0.1973] |
| **medie** | | | **+0.5691** | | | | **+0.5532** | | **-0.0159** | |

**Δ split mediu -0.0159**, sd intre limbi 0.1142, interval -0.1912 pana la +0.1140. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4343 | +0.3758 | -0.0585 |
| de | +0.7246 | +0.7379 | +0.0133 |
| en | +0.6887 | +0.6721 | -0.0166 |
| es | +0.6880 | +0.6913 | +0.0033 |
| fil | +0.5390 | +0.5552 | +0.0162 |
| fr | +0.3755 | +0.3657 | -0.0098 |
| it | +0.7028 | +0.7049 | +0.0021 |
| ja | +0.5845 | +0.5205 | -0.0640 |
| pt | +0.7707 | +0.7691 | -0.0016 |
| si | +0.0237 | -0.0375 | -0.0612 |

**Diferenta medie -0.0177**, interval -0.0640 pana la +0.0162.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3903 | +0.3201 | +0.0102 | +0.1142 |
| de | +0.6461 | +0.7926 | -0.0023 | -0.0680 |
| en | +0.8130 | +0.7180 | -0.0065 | -0.0293 |
| es | +0.6567 | +0.6667 | -0.0212 | +0.0213 |
| fil | +0.4308 | +0.5800 | -0.0059 | -0.0410 |
| fr | +0.5593 | +0.4103 | +0.0073 | -0.0348 |
| it | +0.6154 | +0.7165 | -0.0061 | -0.0137 |
| ja | +0.6352 | +0.5810 | -0.0002 | +0.0035 |
| pt | +0.7682 | +0.7534 | -0.0096 | +0.0173 |
| si | +0.2023 | -0.0809 | +0.0076 | +0.1046 |
