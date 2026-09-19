# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:15:52 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4303 | [+0.3532, +0.5012] | 30 | 11 | +0.3691 | [-0.1222, +0.7005] | -0.0613 | [-0.5602, +0.2922] |
| de | 570 | 193 | +0.6442 | [+0.5904, +0.6925] | 23 | 11 | +0.6990 | [+0.4636, +0.8149] | +0.0548 | [-0.1868, +0.1827] |
| en | 570 | 190 | +0.8097 | [+0.7709, +0.8419] | 30 | 10 | +0.7038 | [+0.4836, +0.8343] | -0.1058 | [-0.3388, +0.0333] |
| es | 593 | 208 | +0.6726 | [+0.6265, +0.7148] | 30 | 10 | +0.6883 | [+0.3533, +0.8832] | +0.0157 | [-0.3151, +0.2136] |
| fil | 570 | 555 | +0.4078 | [+0.3351, +0.4740] | 30 | 30 | +0.5964 | [+0.3676, +0.7889] | +0.1886 | [-0.0461, +0.3941] |
| fr | 569 | 191 | +0.5456 | [+0.4793, +0.6071] | 30 | 11 | +0.3325 | [-0.0593, +0.6252] | -0.2130 | [-0.6224, +0.0971] |
| it | 570 | 192 | +0.6189 | [+0.5638, +0.6747] | 30 | 10 | +0.6730 | [+0.4502, +0.8300] | +0.0541 | [-0.1761, +0.2270] |
| ja | 570 | 190 | +0.6028 | [+0.5408, +0.6571] | 30 | 10 | +0.5101 | [+0.2677, +0.6718] | -0.0926 | [-0.3416, +0.0826] |
| pt | 567 | 562 | +0.7616 | [+0.7203, +0.7988] | 30 | 30 | +0.8052 | [+0.6411, +0.9122] | +0.0435 | [-0.1234, +0.1584] |
| si | 600 | 578 | +0.2942 | [+0.2319, +0.3561] | 30 | 30 | +0.0051 | [-0.3844, +0.4255] | -0.2891 | [-0.6944, +0.1378] |
| **medie** | | | **+0.5788** | | | | **+0.5383** | | **-0.0405** | |

**Δ split mediu -0.0405**, sd intre limbi 0.1413, interval -0.2891 pana la +0.1886. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3691 | +0.3182 | -0.0509 |
| de | +0.6990 | +0.7153 | +0.0163 |
| en | +0.7038 | +0.7163 | +0.0125 |
| es | +0.6883 | +0.6915 | +0.0032 |
| fil | +0.5964 | +0.5968 | +0.0004 |
| fr | +0.3325 | +0.3142 | -0.0183 |
| it | +0.6730 | +0.6770 | +0.0040 |
| ja | +0.5101 | +0.5034 | -0.0067 |
| pt | +0.8052 | +0.8067 | +0.0015 |
| si | +0.0051 | +0.0459 | +0.0408 |

**Diferenta medie +0.0003**, interval -0.0509 pana la +0.0408.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4090 | +0.3100 | +0.0213 | +0.0591 |
| de | +0.6502 | +0.8101 | -0.0060 | -0.1111 |
| en | +0.8072 | +0.6439 | +0.0025 | +0.0599 |
| es | +0.6407 | +0.6571 | +0.0319 | +0.0312 |
| fil | +0.4095 | +0.5000 | -0.0017 | +0.0964 |
| fr | +0.5340 | +0.3951 | +0.0116 | -0.0626 |
| it | +0.6113 | +0.6639 | +0.0076 | +0.0091 |
| ja | +0.5852 | +0.4061 | +0.0176 | +0.1040 |
| pt | +0.7591 | +0.8267 | +0.0025 | -0.0215 |
| si | +0.2322 | -0.0123 | +0.0620 | +0.0174 |
