# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:45:32 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3982 | [+0.3112, +0.4791] | 30 | 11 | +0.1599 | [-0.3168, +0.5947] | -0.2383 | [-0.7129, +0.2157] |
| de | 570 | 193 | +0.5849 | [+0.5184, +0.6453] | 23 | 11 | +0.7221 | [+0.4293, +0.8507] | +0.1372 | [-0.1683, +0.2845] |
| en | 570 | 190 | +0.7788 | [+0.7338, +0.8171] | 30 | 10 | +0.7024 | [+0.4132, +0.8333] | -0.0764 | [-0.3655, +0.0647] |
| es | 593 | 208 | +0.6189 | [+0.5634, +0.6689] | 30 | 10 | +0.6258 | [+0.2979, +0.8041] | +0.0070 | [-0.3228, +0.1941] |
| fil | 570 | 555 | +0.3971 | [+0.3266, +0.4662] | 30 | 30 | +0.5736 | [+0.3260, +0.7439] | +0.1765 | [-0.0789, +0.3609] |
| fr | 569 | 191 | +0.4938 | [+0.4246, +0.5571] | 30 | 11 | +0.2522 | [-0.1526, +0.5958] | -0.2416 | [-0.6512, +0.1119] |
| it | 570 | 192 | +0.5929 | [+0.5338, +0.6505] | 30 | 10 | +0.5871 | [+0.3618, +0.7962] | -0.0058 | [-0.2365, +0.2076] |
| ja | 570 | 190 | +0.5972 | [+0.5346, +0.6554] | 30 | 10 | +0.5782 | [+0.4038, +0.6988] | -0.0190 | [-0.2038, +0.1151] |
| pt | 567 | 562 | +0.7274 | [+0.6845, +0.7661] | 30 | 30 | +0.7794 | [+0.5897, +0.9062] | +0.0520 | [-0.1448, +0.1797] |
| si | 600 | 578 | +0.2645 | [+0.2030, +0.3275] | 30 | 30 | +0.0828 | [-0.2978, +0.5380] | -0.1817 | [-0.5725, +0.2747] |
| **medie** | | | **+0.5454** | | | | **+0.5063** | | **-0.0390** | |

**Δ split mediu -0.0390**, sd intre limbi 0.1460, interval -0.2416 pana la +0.1765. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1599 | +0.1622 | +0.0023 |
| de | +0.7221 | +0.7234 | +0.0013 |
| en | +0.7024 | +0.7030 | +0.0006 |
| es | +0.6258 | +0.6263 | +0.0005 |
| fil | +0.5736 | +0.5716 | -0.0020 |
| fr | +0.2522 | +0.2527 | +0.0005 |
| it | +0.5871 | +0.5857 | -0.0014 |
| ja | +0.5782 | +0.5783 | +0.0001 |
| pt | +0.7794 | +0.7786 | -0.0008 |
| si | +0.0828 | +0.0794 | -0.0034 |

**Diferenta medie -0.0002**, interval -0.0034 pana la +0.0023.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3684 | +0.1874 | +0.0298 | -0.0275 |
| de | +0.6113 | +0.7535 | -0.0264 | -0.0314 |
| en | +0.7762 | +0.6464 | +0.0026 | +0.0560 |
| es | +0.5969 | +0.6119 | +0.0220 | +0.0139 |
| fil | +0.4137 | +0.4676 | -0.0166 | +0.1060 |
| fr | +0.4594 | +0.2399 | +0.0344 | +0.0123 |
| it | +0.5848 | +0.5998 | +0.0081 | -0.0127 |
| ja | +0.5444 | +0.3923 | +0.0528 | +0.1859 |
| pt | +0.7362 | +0.7904 | -0.0088 | -0.0110 |
| si | +0.2627 | +0.1116 | +0.0018 | -0.0288 |
