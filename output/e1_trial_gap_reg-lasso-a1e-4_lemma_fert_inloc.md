# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:19:23 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4132 | [+0.3248, +0.4944] | 30 | 11 | +0.1585 | [-0.2923, +0.5811] | -0.2546 | [-0.7026, +0.1829] |
| de | 570 | 193 | +0.6134 | [+0.5559, +0.6674] | 23 | 11 | +0.7596 | [+0.5058, +0.8690] | +0.1462 | [-0.1107, +0.2726] |
| en | 570 | 190 | +0.7750 | [+0.7321, +0.8109] | 30 | 10 | +0.6558 | [+0.4025, +0.7931] | -0.1191 | [-0.3661, +0.0300] |
| es | 593 | 208 | +0.6286 | [+0.5761, +0.6732] | 30 | 10 | +0.5880 | [+0.2198, +0.7899] | -0.0406 | [-0.4057, +0.1724] |
| fil | 570 | 555 | +0.3890 | [+0.3184, +0.4570] | 30 | 30 | +0.5911 | [+0.3626, +0.7483] | +0.2022 | [-0.0343, +0.3766] |
| fr | 569 | 191 | +0.5002 | [+0.4377, +0.5600] | 30 | 11 | +0.2462 | [-0.1489, +0.6050] | -0.2540 | [-0.6690, +0.1076] |
| it | 570 | 192 | +0.6096 | [+0.5554, +0.6633] | 30 | 10 | +0.5873 | [+0.3581, +0.7877] | -0.0224 | [-0.2629, +0.1859] |
| ja | 570 | 190 | +0.6094 | [+0.5500, +0.6634] | 30 | 10 | +0.5824 | [+0.4252, +0.6879] | -0.0270 | [-0.1997, +0.0904] |
| pt | 567 | 562 | +0.7309 | [+0.6865, +0.7698] | 30 | 30 | +0.7835 | [+0.6140, +0.9078] | +0.0525 | [-0.1206, +0.1804] |
| si | 600 | 578 | +0.2542 | [+0.1920, +0.3194] | 30 | 30 | +0.0129 | [-0.3605, +0.4545] | -0.2413 | [-0.6268, +0.2045] |
| **medie** | | | **+0.5524** | | | | **+0.4965** | | **-0.0558** | |

**Δ split mediu -0.0558**, sd intre limbi 0.1628, interval -0.2546 pana la +0.2022. Trial-ul e mai mare pe 3 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1585 | +0.1585 | +0.0000 |
| de | +0.7596 | +0.7596 | +0.0000 |
| en | +0.6558 | +0.6558 | +0.0000 |
| es | +0.5880 | +0.5880 | +0.0000 |
| fil | +0.5911 | +0.5911 | +0.0000 |
| fr | +0.2462 | +0.2462 | +0.0000 |
| it | +0.5873 | +0.5873 | +0.0000 |
| ja | +0.5824 | +0.5824 | +0.0000 |
| pt | +0.7835 | +0.7835 | +0.0000 |
| si | +0.0129 | +0.0129 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3744 | +0.1374 | +0.0388 | +0.0211 |
| de | +0.6280 | +0.7978 | -0.0146 | -0.0382 |
| en | +0.7668 | +0.6034 | +0.0082 | +0.0524 |
| es | +0.6018 | +0.6288 | +0.0268 | -0.0408 |
| fil | +0.3989 | +0.5278 | -0.0099 | +0.0633 |
| fr | +0.4960 | +0.2429 | +0.0042 | +0.0033 |
| it | +0.5919 | +0.5776 | +0.0177 | +0.0097 |
| ja | +0.5450 | +0.4271 | +0.0644 | +0.1553 |
| pt | +0.7396 | +0.7928 | -0.0087 | -0.0093 |
| si | +0.2554 | +0.0217 | -0.0012 | -0.0088 |
