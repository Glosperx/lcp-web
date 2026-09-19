# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:42:24 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3879 | [+0.3071, +0.4622] | 30 | 11 | +0.3410 | [-0.0748, +0.6899] | -0.0469 | [-0.4761, +0.3060] |
| de | 570 | 193 | +0.5911 | [+0.5426, +0.6399] | 23 | 11 | +0.7648 | [+0.4730, +0.9095] | +0.1737 | [-0.1279, +0.3341] |
| en | 570 | 190 | +0.8010 | [+0.7662, +0.8323] | 30 | 10 | +0.7488 | [+0.5977, +0.8582] | -0.0522 | [-0.2012, +0.0633] |
| es | 593 | 208 | +0.6548 | [+0.6120, +0.6947] | 30 | 10 | +0.6395 | [+0.3684, +0.8229] | -0.0153 | [-0.2943, +0.1720] |
| fil | 570 | 555 | +0.3753 | [+0.3029, +0.4429] | 30 | 30 | +0.5813 | [+0.3270, +0.7968] | +0.2059 | [-0.0469, +0.4302] |
| fr | 569 | 191 | +0.5463 | [+0.4849, +0.6031] | 30 | 11 | +0.4714 | [+0.1573, +0.6777] | -0.0749 | [-0.4043, +0.1329] |
| it | 570 | 192 | +0.5805 | [+0.5277, +0.6355] | 30 | 10 | +0.7351 | [+0.5793, +0.8468] | +0.1546 | [-0.0094, +0.2840] |
| ja | 570 | 190 | +0.2682 | [+0.1889, +0.3489] | 30 | 10 | +0.4109 | [-0.1860, +0.7548] | +0.1427 | [-0.4413, +0.4816] |
| pt | 567 | 562 | +0.7558 | [+0.7179, +0.7920] | 30 | 30 | +0.7268 | [+0.5492, +0.8692] | -0.0290 | [-0.2055, +0.1150] |
| si | 600 | 578 | +0.2899 | [+0.2105, +0.3606] | 30 | 30 | +0.1492 | [-0.1646, +0.4856] | -0.1406 | [-0.4555, +0.2107] |
| **medie** | | | **+0.5251** | | | | **+0.5569** | | **+0.0318** | |

**Δ split mediu +0.0318**, sd intre limbi 0.1239, interval -0.1406 pana la +0.2059. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3410 | +0.2873 | -0.0537 |
| de | +0.7648 | +0.7351 | -0.0297 |
| en | +0.7488 | +0.7403 | -0.0085 |
| es | +0.6395 | +0.6424 | +0.0029 |
| fil | +0.5813 | +0.6003 | +0.0190 |
| fr | +0.4714 | +0.4027 | -0.0687 |
| it | +0.7351 | +0.7190 | -0.0161 |
| ja | +0.4109 | +0.3427 | -0.0682 |
| pt | +0.7268 | +0.7205 | -0.0063 |
| si | +0.1492 | +0.3151 | +0.1659 |

**Diferenta medie -0.0063**, interval -0.0687 pana la +0.1659.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3955 | +0.3567 | -0.0076 | -0.0157 |
| de | +0.6242 | +0.8597 | -0.0331 | -0.0949 |
| en | +0.8046 | +0.6873 | -0.0036 | +0.0615 |
| es | +0.6687 | +0.6023 | -0.0139 | +0.0372 |
| fil | +0.3902 | +0.5896 | -0.0149 | -0.0083 |
| fr | +0.5203 | +0.3490 | +0.0260 | +0.1224 |
| it | +0.6130 | +0.7503 | -0.0325 | -0.0152 |
| ja | +0.5599 | +0.4567 | -0.2917 | -0.0458 |
| pt | +0.7504 | +0.7580 | +0.0054 | -0.0312 |
| si | +0.1154 | +0.0892 | +0.1745 | +0.0600 |
