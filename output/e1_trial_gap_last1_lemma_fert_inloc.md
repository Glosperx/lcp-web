# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:18:41 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4125 | [+0.3301, +0.4855] | 30 | 11 | +0.2968 | [-0.2348, +0.6590] | -0.1157 | [-0.6532, +0.2491] |
| de | 570 | 193 | +0.6475 | [+0.5960, +0.6955] | 23 | 11 | +0.8074 | [+0.5480, +0.9164] | +0.1599 | [-0.0992, +0.2843] |
| en | 570 | 190 | +0.8107 | [+0.7711, +0.8423] | 30 | 10 | +0.6808 | [+0.4454, +0.8475] | -0.1299 | [-0.3646, +0.0404] |
| es | 593 | 208 | +0.6753 | [+0.6325, +0.7132] | 30 | 10 | +0.6606 | [+0.3239, +0.8580] | -0.0146 | [-0.3512, +0.1858] |
| fil | 570 | 555 | +0.4051 | [+0.3345, +0.4732] | 30 | 30 | +0.5716 | [+0.3366, +0.7595] | +0.1665 | [-0.0675, +0.3715] |
| fr | 569 | 191 | +0.5476 | [+0.4808, +0.6063] | 30 | 11 | +0.3284 | [-0.0472, +0.6213] | -0.2192 | [-0.6039, +0.0864] |
| it | 570 | 192 | +0.6081 | [+0.5519, +0.6657] | 30 | 10 | +0.6917 | [+0.5084, +0.8226] | +0.0836 | [-0.1074, +0.2361] |
| ja | 570 | 190 | +0.5652 | [+0.4979, +0.6247] | 30 | 10 | +0.5029 | [+0.2892, +0.6354] | -0.0623 | [-0.2799, +0.0854] |
| pt | 567 | 562 | +0.7547 | [+0.7151, +0.7914] | 30 | 30 | +0.7711 | [+0.5864, +0.9043] | +0.0164 | [-0.1761, +0.1541] |
| si | 600 | 578 | +0.2644 | [+0.2031, +0.3267] | 30 | 30 | -0.0894 | [-0.5069, +0.3951] | -0.3538 | [-0.7735, +0.1345] |
| **medie** | | | **+0.5691** | | | | **+0.5222** | | **-0.0469** | |

**Δ split mediu -0.0469**, sd intre limbi 0.1654, interval -0.3538 pana la +0.1665. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2968 | +0.2727 | -0.0241 |
| de | +0.8074 | +0.8032 | -0.0042 |
| en | +0.6808 | +0.6718 | -0.0090 |
| es | +0.6606 | +0.6657 | +0.0051 |
| fil | +0.5716 | +0.5930 | +0.0214 |
| fr | +0.3284 | +0.3128 | -0.0156 |
| it | +0.6917 | +0.7036 | +0.0119 |
| ja | +0.5029 | +0.4780 | -0.0249 |
| pt | +0.7711 | +0.7783 | +0.0072 |
| si | -0.0894 | +0.0072 | +0.0966 |

**Diferenta medie +0.0064**, interval -0.0249 pana la +0.0966.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3791 | +0.2420 | +0.0334 | +0.0548 |
| de | +0.6659 | +0.8511 | -0.0184 | -0.0437 |
| en | +0.8081 | +0.6148 | +0.0026 | +0.0660 |
| es | +0.6541 | +0.6684 | +0.0212 | -0.0078 |
| fil | +0.4033 | +0.5261 | +0.0018 | +0.0455 |
| fr | +0.5258 | +0.3238 | +0.0218 | +0.0046 |
| it | +0.6243 | +0.6972 | -0.0162 | -0.0055 |
| ja | +0.5778 | +0.4903 | -0.0126 | +0.0126 |
| pt | +0.7599 | +0.7625 | -0.0052 | +0.0086 |
| si | +0.2571 | +0.0140 | +0.0073 | -0.1034 |
