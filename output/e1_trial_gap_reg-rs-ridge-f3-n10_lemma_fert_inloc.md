# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:56:33 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3597 | [+0.2671, +0.4496] | 30 | 11 | +0.1703 | [-0.1772, +0.6000] | -0.1893 | [-0.5615, +0.2451] |
| de | 570 | 193 | +0.5697 | [+0.5033, +0.6296] | 23 | 11 | +0.5695 | [+0.2396, +0.8080] | -0.0002 | [-0.3306, +0.2458] |
| en | 570 | 190 | +0.7525 | [+0.7021, +0.7948] | 30 | 10 | +0.5633 | [+0.3986, +0.7742] | -0.1891 | [-0.3628, +0.0279] |
| es | 593 | 208 | +0.6156 | [+0.5656, +0.6627] | 30 | 10 | +0.6760 | [+0.3468, +0.8550] | +0.0604 | [-0.2574, +0.2469] |
| fil | 570 | 555 | +0.3251 | [+0.2531, +0.3926] | 30 | 30 | +0.3968 | [+0.1000, +0.6292] | +0.0717 | [-0.2299, +0.3169] |
| fr | 569 | 191 | +0.4750 | [+0.4026, +0.5422] | 30 | 11 | +0.2983 | [-0.0480, +0.5949] | -0.1767 | [-0.5329, +0.1240] |
| it | 570 | 192 | +0.5501 | [+0.4884, +0.6131] | 30 | 10 | +0.6328 | [+0.3689, +0.8245] | +0.0826 | [-0.1872, +0.2872] |
| ja | 570 | 190 | +0.5708 | [+0.5064, +0.6331] | 30 | 10 | +0.4951 | [+0.3180, +0.7249] | -0.0757 | [-0.2594, +0.1489] |
| pt | 567 | 562 | +0.6788 | [+0.6243, +0.7263] | 30 | 30 | +0.7364 | [+0.5505, +0.8697] | +0.0576 | [-0.1282, +0.2026] |
| si | 600 | 578 | +0.2356 | [+0.1695, +0.3034] | 30 | 30 | +0.0935 | [-0.2128, +0.3946] | -0.1421 | [-0.4545, +0.1614] |
| **medie** | | | **+0.5133** | | | | **+0.4632** | | **-0.0501** | |

**Δ split mediu -0.0501**, sd intre limbi 0.1167, interval -0.1893 pana la +0.0826. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1703 | +0.1703 | +0.0000 |
| de | +0.5695 | +0.5695 | +0.0000 |
| en | +0.5633 | +0.5633 | +0.0000 |
| es | +0.6760 | +0.6760 | +0.0000 |
| fil | +0.3968 | +0.3968 | +0.0000 |
| fr | +0.2983 | +0.2983 | +0.0000 |
| it | +0.6328 | +0.6328 | +0.0000 |
| ja | +0.4951 | +0.4951 | +0.0000 |
| pt | +0.7364 | +0.7364 | +0.0000 |
| si | +0.0935 | +0.0935 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3361 | +0.1602 | +0.0236 | +0.0101 |
| de | +0.5687 | +0.6156 | +0.0010 | -0.0461 |
| en | +0.7526 | +0.5641 | -0.0001 | -0.0008 |
| es | +0.6053 | +0.7190 | +0.0103 | -0.0430 |
| fil | +0.3462 | +0.3839 | -0.0211 | +0.0129 |
| fr | +0.4766 | +0.3780 | -0.0016 | -0.0797 |
| it | +0.5524 | +0.6529 | -0.0023 | -0.0201 |
| ja | +0.5248 | +0.5129 | +0.0460 | -0.0178 |
| pt | +0.6900 | +0.7276 | -0.0112 | +0.0088 |
| si | +0.2452 | +0.1761 | -0.0096 | -0.0826 |
