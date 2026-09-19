# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:07:03 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4160 | [+0.3350, +0.4873] | 30 | 11 | +0.4045 | [-0.1287, +0.7497] | -0.0115 | [-0.5607, +0.3428] |
| de | 570 | 193 | +0.6262 | [+0.5736, +0.6762] | 23 | 11 | +0.7691 | [+0.4766, +0.9139] | +0.1429 | [-0.1558, +0.2985] |
| en | 570 | 190 | +0.8212 | [+0.7821, +0.8542] | 30 | 10 | +0.7305 | [+0.4524, +0.8792] | -0.0907 | [-0.3670, +0.0571] |
| es | 593 | 208 | +0.6656 | [+0.6228, +0.7047] | 30 | 10 | +0.7220 | [+0.4710, +0.8724] | +0.0564 | [-0.1911, +0.2129] |
| fil | 570 | 555 | +0.4097 | [+0.3387, +0.4758] | 30 | 30 | +0.6028 | [+0.3731, +0.8112] | +0.1931 | [-0.0485, +0.4151] |
| fr | 569 | 191 | +0.5319 | [+0.4609, +0.5979] | 30 | 11 | +0.3826 | [+0.0327, +0.6449] | -0.1493 | [-0.5020, +0.1329] |
| it | 570 | 192 | +0.6104 | [+0.5543, +0.6692] | 30 | 10 | +0.6841 | [+0.4719, +0.8360] | +0.0737 | [-0.1490, +0.2416] |
| ja | 570 | 190 | +0.5133 | [+0.4392, +0.5774] | 30 | 10 | +0.3675 | [+0.0470, +0.5826] | -0.1458 | [-0.4767, +0.0748] |
| pt | 567 | 562 | +0.7565 | [+0.7169, +0.7941] | 30 | 30 | +0.7709 | [+0.5952, +0.8946] | +0.0144 | [-0.1654, +0.1445] |
| si | 600 | 578 | +0.1763 | [+0.1088, +0.2440] | 30 | 30 | -0.1940 | [-0.5684, +0.3733] | -0.3703 | [-0.7570, +0.1927] |
| **medie** | | | **+0.5527** | | | | **+0.5240** | | **-0.0287** | |

**Δ split mediu -0.0287**, sd intre limbi 0.1658, interval -0.3703 pana la +0.1931. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4045 | +0.2884 | -0.1161 |
| de | +0.7691 | +0.7709 | +0.0018 |
| en | +0.7305 | +0.6943 | -0.0362 |
| es | +0.7220 | +0.7034 | -0.0186 |
| fil | +0.6028 | +0.6203 | +0.0175 |
| fr | +0.3826 | +0.2926 | -0.0900 |
| it | +0.6841 | +0.6773 | -0.0068 |
| ja | +0.3675 | +0.3091 | -0.0584 |
| pt | +0.7709 | +0.7748 | +0.0039 |
| si | -0.1940 | +0.0146 | +0.2086 |

**Diferenta medie -0.0094**, interval -0.1161 pana la +0.2086.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4122 | +0.2871 | +0.0038 | +0.1174 |
| de | +0.6402 | +0.8346 | -0.0140 | -0.0655 |
| en | +0.8105 | +0.7233 | +0.0107 | +0.0072 |
| es | +0.6596 | +0.6745 | +0.0060 | +0.0475 |
| fil | +0.4017 | +0.5484 | +0.0080 | +0.0544 |
| fr | +0.5342 | +0.3842 | -0.0023 | -0.0016 |
| it | +0.6102 | +0.7590 | +0.0002 | -0.0749 |
| ja | +0.6008 | +0.4762 | -0.0875 | -0.1087 |
| pt | +0.7677 | +0.7511 | -0.0112 | +0.0198 |
| si | +0.1880 | -0.1549 | -0.0117 | -0.0391 |
