# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:22:08 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4020 | [+0.3228, +0.4710] | 30 | 11 | +0.4241 | [-0.0535, +0.7397] | +0.0221 | [-0.4657, +0.3517] |
| de | 570 | 193 | +0.5993 | [+0.5480, +0.6475] | 23 | 11 | +0.7051 | [+0.3429, +0.9011] | +0.1057 | [-0.2603, +0.3190] |
| en | 570 | 190 | +0.7919 | [+0.7528, +0.8263] | 30 | 10 | +0.7577 | [+0.5600, +0.8765] | -0.0343 | [-0.2376, +0.0914] |
| es | 593 | 208 | +0.6557 | [+0.6129, +0.6943] | 30 | 10 | +0.6779 | [+0.4109, +0.8459] | +0.0222 | [-0.2480, +0.1942] |
| fil | 570 | 555 | +0.4151 | [+0.3465, +0.4812] | 30 | 30 | +0.5914 | [+0.3514, +0.8128] | +0.1763 | [-0.0779, +0.4069] |
| fr | 569 | 191 | +0.5517 | [+0.4885, +0.6105] | 30 | 11 | +0.3260 | [-0.0144, +0.5948] | -0.2257 | [-0.5762, +0.0501] |
| it | 570 | 192 | +0.6017 | [+0.5511, +0.6524] | 30 | 10 | +0.7347 | [+0.5634, +0.8528] | +0.1330 | [-0.0469, +0.2667] |
| ja | 570 | 190 | +0.6136 | [+0.5526, +0.6711] | 30 | 10 | +0.6310 | [+0.3510, +0.8157] | +0.0174 | [-0.2631, +0.2100] |
| pt | 567 | 562 | +0.7668 | [+0.7275, +0.8028] | 30 | 30 | +0.7671 | [+0.5933, +0.8965] | +0.0002 | [-0.1721, +0.1323] |
| si | 600 | 578 | +0.1248 | [+0.0582, +0.1914] | 30 | 30 | +0.0196 | [-0.4002, +0.3685] | -0.1052 | [-0.5221, +0.2406] |
| **medie** | | | **+0.5523** | | | | **+0.5635** | | **+0.0112** | |

**Δ split mediu +0.0112**, sd intre limbi 0.1170, interval -0.2257 pana la +0.1763. Trial-ul e mai mare pe 7 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4241 | +0.3431 | -0.0810 |
| de | +0.7051 | +0.7017 | -0.0034 |
| en | +0.7577 | +0.7694 | +0.0117 |
| es | +0.6779 | +0.6715 | -0.0064 |
| fil | +0.5914 | +0.5971 | +0.0057 |
| fr | +0.3260 | +0.3252 | -0.0008 |
| it | +0.7347 | +0.7395 | +0.0048 |
| ja | +0.6310 | +0.6419 | +0.0109 |
| pt | +0.7671 | +0.7618 | -0.0053 |
| si | +0.0196 | +0.0434 | +0.0238 |

**Diferenta medie -0.0040**, interval -0.0810 pana la +0.0238.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4008 | +0.4362 | +0.0012 | -0.0121 |
| de | +0.6233 | +0.7849 | -0.0240 | -0.0798 |
| en | +0.8048 | +0.7438 | -0.0129 | +0.0139 |
| es | +0.6737 | +0.7109 | -0.0180 | -0.0330 |
| fil | +0.4018 | +0.6023 | +0.0133 | -0.0109 |
| fr | +0.5326 | +0.2923 | +0.0191 | +0.0337 |
| it | +0.6018 | +0.7332 | -0.0001 | +0.0015 |
| ja | +0.5739 | +0.5793 | +0.0397 | +0.0517 |
| pt | +0.7665 | +0.7612 | +0.0003 | +0.0059 |
| si | +0.0713 | +0.0557 | +0.0535 | -0.0361 |
