# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:12:43 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4265 | [+0.3436, +0.5023] | 30 | 11 | +0.1228 | [-0.4660, +0.5827] | -0.3038 | [-0.8965, +0.1702] |
| de | 570 | 193 | +0.6075 | [+0.5567, +0.6558] | 23 | 11 | +0.7253 | [+0.4987, +0.8760] | +0.1178 | [-0.1116, +0.2783] |
| en | 570 | 190 | +0.8026 | [+0.7634, +0.8365] | 30 | 10 | +0.6730 | [+0.5100, +0.8070] | -0.1297 | [-0.2927, +0.0149] |
| es | 593 | 208 | +0.6581 | [+0.6106, +0.7006] | 30 | 10 | +0.6947 | [+0.4051, +0.8660] | +0.0366 | [-0.2519, +0.2100] |
| fil | 570 | 555 | +0.4071 | [+0.3359, +0.4732] | 30 | 30 | +0.6217 | [+0.4165, +0.7912] | +0.2145 | [-0.0036, +0.4003] |
| fr | 569 | 191 | +0.5090 | [+0.4396, +0.5722] | 30 | 11 | +0.3369 | [-0.0063, +0.6269] | -0.1721 | [-0.5238, +0.1346] |
| it | 570 | 192 | +0.6138 | [+0.5587, +0.6668] | 30 | 10 | +0.6310 | [+0.4297, +0.7920] | +0.0171 | [-0.1861, +0.1895] |
| ja | 570 | 190 | +0.5260 | [+0.4630, +0.5871] | 30 | 10 | +0.4385 | [+0.2092, +0.6109] | -0.0875 | [-0.3198, +0.0927] |
| pt | 567 | 562 | +0.7575 | [+0.7161, +0.7944] | 30 | 30 | +0.7721 | [+0.6056, +0.9005] | +0.0145 | [-0.1638, +0.1455] |
| si | 600 | 578 | +0.1837 | [+0.1106, +0.2563] | 30 | 30 | -0.0223 | [-0.4007, +0.5037] | -0.2060 | [-0.5916, +0.3151] |
| **medie** | | | **+0.5492** | | | | **+0.4994** | | **-0.0499** | |

**Δ split mediu -0.0499**, sd intre limbi 0.1584, interval -0.3038 pana la +0.2145. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1228 | +0.0815 | -0.0413 |
| de | +0.7253 | +0.7183 | -0.0070 |
| en | +0.6730 | +0.6597 | -0.0133 |
| es | +0.6947 | +0.6853 | -0.0094 |
| fil | +0.6217 | +0.6178 | -0.0039 |
| fr | +0.3369 | +0.3151 | -0.0218 |
| it | +0.6310 | +0.6145 | -0.0165 |
| ja | +0.4385 | +0.4426 | +0.0041 |
| pt | +0.7721 | +0.7862 | +0.0141 |
| si | -0.0223 | +0.0167 | +0.0390 |

**Diferenta medie -0.0056**, interval -0.0413 pana la +0.0390.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3949 | +0.0560 | +0.0316 | +0.0668 |
| de | +0.6540 | +0.8059 | -0.0465 | -0.0806 |
| en | +0.7999 | +0.6830 | +0.0027 | -0.0100 |
| es | +0.6416 | +0.7101 | +0.0165 | -0.0154 |
| fil | +0.4135 | +0.6335 | -0.0064 | -0.0118 |
| fr | +0.5098 | +0.2867 | -0.0008 | +0.0502 |
| it | +0.6310 | +0.6692 | -0.0172 | -0.0382 |
| ja | +0.5673 | +0.3947 | -0.0413 | +0.0438 |
| pt | +0.7644 | +0.7892 | -0.0069 | -0.0171 |
| si | +0.1376 | -0.1347 | +0.0461 | +0.1124 |
