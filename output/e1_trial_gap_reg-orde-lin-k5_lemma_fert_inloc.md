# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:52:53 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3762 | [+0.2918, +0.4534] | 30 | 11 | +0.1121 | [-0.2985, +0.5038] | -0.2641 | [-0.6823, +0.1293] |
| de | 570 | 193 | +0.5934 | [+0.5332, +0.6473] | 23 | 11 | +0.7778 | [+0.6176, +0.8889] | +0.1844 | [+0.0154, +0.3076] |
| en | 570 | 190 | +0.7758 | [+0.7300, +0.8136] | 30 | 10 | +0.6578 | [+0.3651, +0.8056] | -0.1180 | [-0.4164, +0.0394] |
| es | 593 | 208 | +0.6353 | [+0.5875, +0.6791] | 30 | 10 | +0.5812 | [+0.2312, +0.7912] | -0.0542 | [-0.4078, +0.1642] |
| fil | 570 | 555 | +0.4100 | [+0.3396, +0.4760] | 30 | 30 | +0.5399 | [+0.2645, +0.7363] | +0.1299 | [-0.1500, +0.3450] |
| fr | 569 | 191 | +0.4921 | [+0.4222, +0.5581] | 30 | 11 | +0.2849 | [-0.1229, +0.6272] | -0.2072 | [-0.6256, +0.1434] |
| it | 570 | 192 | +0.5984 | [+0.5412, +0.6583] | 30 | 10 | +0.5574 | [+0.3002, +0.7956] | -0.0410 | [-0.2994, +0.2033] |
| ja | 570 | 190 | +0.5229 | [+0.4529, +0.5881] | 30 | 10 | +0.5492 | [+0.3448, +0.7073] | +0.0262 | [-0.1904, +0.1888] |
| pt | 567 | 562 | +0.7359 | [+0.6930, +0.7739] | 30 | 30 | +0.7624 | [+0.5589, +0.8927] | +0.0265 | [-0.1776, +0.1625] |
| si | 600 | 578 | +0.2581 | [+0.2127, +0.3035] | 30 | 30 | +0.1995 | [-0.0068, +0.4200] | -0.0586 | [-0.2581, +0.1669] |
| **medie** | | | **+0.5398** | | | | **+0.5022** | | **-0.0376** | |

**Δ split mediu -0.0376**, sd intre limbi 0.1386, interval -0.2641 pana la +0.1844. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1121 | +0.1209 | +0.0088 |
| de | +0.7778 | +0.7776 | -0.0002 |
| en | +0.6578 | +0.6576 | -0.0002 |
| es | +0.5812 | +0.5866 | +0.0054 |
| fil | +0.5399 | +0.5411 | +0.0012 |
| fr | +0.2849 | +0.3017 | +0.0168 |
| it | +0.5574 | +0.5572 | -0.0002 |
| ja | +0.5492 | +0.5503 | +0.0011 |
| pt | +0.7624 | +0.7629 | +0.0005 |
| si | +0.1995 | +0.2028 | +0.0033 |

**Diferenta medie +0.0036**, interval -0.0002 pana la +0.0168.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3569 | +0.0925 | +0.0193 | +0.0196 |
| de | +0.5763 | +0.8162 | +0.0171 | -0.0384 |
| en | +0.7580 | +0.6123 | +0.0178 | +0.0455 |
| es | +0.5951 | +0.5795 | +0.0402 | +0.0017 |
| fil | +0.4178 | +0.5180 | -0.0078 | +0.0219 |
| fr | +0.4800 | +0.3597 | +0.0121 | -0.0748 |
| it | +0.5605 | +0.6009 | +0.0379 | -0.0435 |
| ja | +0.5651 | +0.4946 | -0.0422 | +0.0546 |
| pt | +0.7315 | +0.7355 | +0.0044 | +0.0269 |
| si | +0.1466 | +0.0906 | +0.1115 | +0.1089 |
