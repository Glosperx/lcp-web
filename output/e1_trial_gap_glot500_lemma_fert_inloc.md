# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:56:43 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4249 | [+0.3489, +0.4921] | 30 | 11 | +0.3775 | [-0.1392, +0.7254] | -0.0474 | [-0.5634, +0.3202] |
| de | 570 | 193 | +0.6106 | [+0.5549, +0.6631] | 23 | 11 | +0.7611 | [+0.4650, +0.9266] | +0.1505 | [-0.1468, +0.3286] |
| en | 570 | 190 | +0.8173 | [+0.7817, +0.8487] | 30 | 10 | +0.6508 | [+0.4634, +0.8161] | -0.1665 | [-0.3624, +0.0014] |
| es | 593 | 208 | +0.6586 | [+0.6098, +0.7028] | 30 | 10 | +0.6444 | [+0.3447, +0.8271] | -0.0143 | [-0.3102, +0.1799] |
| fil | 570 | 555 | +0.3945 | [+0.3247, +0.4595] | 30 | 30 | +0.6329 | [+0.3945, +0.8103] | +0.2384 | [-0.0112, +0.4311] |
| fr | 569 | 191 | +0.5668 | [+0.5073, +0.6215] | 30 | 11 | +0.4589 | [+0.0926, +0.7306] | -0.1079 | [-0.4787, +0.1719] |
| it | 570 | 192 | +0.6129 | [+0.5572, +0.6679] | 30 | 10 | +0.6379 | [+0.4003, +0.7965] | +0.0250 | [-0.2210, +0.1960] |
| ja | 570 | 190 | +0.5466 | [+0.4789, +0.6109] | 30 | 10 | +0.6227 | [+0.4110, +0.7743] | +0.0760 | [-0.1417, +0.2402] |
| pt | 567 | 562 | +0.7459 | [+0.7043, +0.7821] | 30 | 30 | +0.6906 | [+0.4782, +0.8544] | -0.0552 | [-0.2658, +0.1122] |
| si | 600 | 578 | +0.2468 | [+0.1821, +0.3105] | 30 | 30 | +0.2851 | [+0.0336, +0.5034] | +0.0383 | [-0.2230, +0.2717] |
| **medie** | | | **+0.5625** | | | | **+0.5762** | | **+0.0137** | |

**Δ split mediu +0.0137**, sd intre limbi 0.1203, interval -0.1665 pana la +0.2384. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3775 | +0.3501 | -0.0274 |
| de | +0.7611 | +0.7675 | +0.0064 |
| en | +0.6508 | +0.6472 | -0.0036 |
| es | +0.6444 | +0.6488 | +0.0044 |
| fil | +0.6329 | +0.6438 | +0.0109 |
| fr | +0.4589 | +0.4431 | -0.0158 |
| it | +0.6379 | +0.6397 | +0.0018 |
| ja | +0.6227 | +0.6000 | -0.0227 |
| pt | +0.6906 | +0.7079 | +0.0173 |
| si | +0.2851 | +0.2905 | +0.0054 |

**Diferenta medie -0.0023**, interval -0.0274 pana la +0.0173.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4221 | +0.2627 | +0.0028 | +0.1148 |
| de | +0.6455 | +0.8321 | -0.0349 | -0.0710 |
| en | +0.8158 | +0.6619 | +0.0015 | -0.0111 |
| es | +0.6606 | +0.6911 | -0.0020 | -0.0467 |
| fil | +0.4153 | +0.6215 | -0.0208 | +0.0114 |
| fr | +0.5613 | +0.3916 | +0.0055 | +0.0673 |
| it | +0.6241 | +0.6890 | -0.0112 | -0.0511 |
| ja | +0.5799 | +0.5278 | -0.0333 | +0.0949 |
| pt | +0.7537 | +0.6980 | -0.0078 | -0.0074 |
| si | +0.2365 | +0.1229 | +0.0103 | +0.1622 |
