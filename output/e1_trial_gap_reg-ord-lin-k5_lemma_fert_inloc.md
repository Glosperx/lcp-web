# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:46:18 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3886 | [+0.3062, +0.4646] | 30 | 11 | +0.1348 | [-0.3157, +0.5519] | -0.2538 | [-0.7047, +0.1664] |
| de | 570 | 193 | +0.5765 | [+0.5172, +0.6291] | 23 | 11 | +0.7397 | [+0.5313, +0.8886] | +0.1631 | [-0.0492, +0.3205] |
| en | 570 | 190 | +0.7609 | [+0.7179, +0.7964] | 30 | 10 | +0.6421 | [+0.3714, +0.7755] | -0.1188 | [-0.3900, +0.0241] |
| es | 593 | 208 | +0.6231 | [+0.5760, +0.6646] | 30 | 10 | +0.5913 | [+0.2618, +0.7924] | -0.0318 | [-0.3736, +0.1775] |
| fil | 570 | 555 | +0.4132 | [+0.3418, +0.4794] | 30 | 30 | +0.5678 | [+0.3052, +0.7530] | +0.1546 | [-0.1128, +0.3619] |
| fr | 569 | 191 | +0.4963 | [+0.4280, +0.5615] | 30 | 11 | +0.2885 | [-0.1104, +0.6345] | -0.2078 | [-0.6211, +0.1417] |
| it | 570 | 192 | +0.5960 | [+0.5417, +0.6528] | 30 | 10 | +0.5877 | [+0.3560, +0.7994] | -0.0083 | [-0.2429, +0.2155] |
| ja | 570 | 190 | +0.5226 | [+0.4516, +0.5865] | 30 | 10 | +0.5503 | [+0.3483, +0.7011] | +0.0277 | [-0.1871, +0.1814] |
| pt | 567 | 562 | +0.7311 | [+0.6873, +0.7696] | 30 | 30 | +0.7473 | [+0.5376, +0.8860] | +0.0162 | [-0.1903, +0.1634] |
| si | 600 | 578 | +0.2556 | [+0.2132, +0.3003] | 30 | 30 | +0.1875 | [-0.0406, +0.4457] | -0.0681 | [-0.3041, +0.1884] |
| **medie** | | | **+0.5364** | | | | **+0.5037** | | **-0.0327** | |

**Δ split mediu -0.0327**, sd intre limbi 0.1367, interval -0.2538 pana la +0.1631. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1348 | +0.1417 | +0.0069 |
| de | +0.7397 | +0.7350 | -0.0047 |
| en | +0.6421 | +0.6416 | -0.0005 |
| es | +0.5913 | +0.5993 | +0.0080 |
| fil | +0.5678 | +0.5588 | -0.0090 |
| fr | +0.2885 | +0.2939 | +0.0054 |
| it | +0.5877 | +0.5910 | +0.0033 |
| ja | +0.5503 | +0.5494 | -0.0009 |
| pt | +0.7473 | +0.7447 | -0.0026 |
| si | +0.1875 | +0.1893 | +0.0018 |

**Diferenta medie +0.0008**, interval -0.0090 pana la +0.0080.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3572 | +0.0951 | +0.0314 | +0.0397 |
| de | +0.5709 | +0.7825 | +0.0056 | -0.0428 |
| en | +0.7299 | +0.6022 | +0.0310 | +0.0399 |
| es | +0.5809 | +0.5584 | +0.0422 | +0.0329 |
| fil | +0.4145 | +0.5204 | -0.0013 | +0.0474 |
| fr | +0.4802 | +0.3158 | +0.0161 | -0.0273 |
| it | +0.5590 | +0.6395 | +0.0370 | -0.0518 |
| ja | +0.5796 | +0.4776 | -0.0570 | +0.0727 |
| pt | +0.7227 | +0.7126 | +0.0084 | +0.0347 |
| si | +0.1519 | +0.0899 | +0.1037 | +0.0976 |
