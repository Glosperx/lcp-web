# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 23:52:55 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4074 | [+0.3170, +0.4906] | 30 | 11 | +0.4321 | [+0.1607, +0.6783] | +0.0247 | [-0.2529, +0.2830] |
| de | 570 | 193 | +0.5373 | [+0.4754, +0.5926] | 23 | 11 | +0.7502 | [+0.5002, +0.8816] | +0.2129 | [-0.0378, +0.3669] |
| en | 570 | 190 | +0.7901 | [+0.7539, +0.8234] | 30 | 10 | +0.6832 | [+0.3682, +0.8823] | -0.1069 | [-0.4268, +0.0976] |
| es | 593 | 208 | +0.6836 | [+0.6388, +0.7226] | 30 | 10 | +0.6740 | [+0.3317, +0.8825] | -0.0096 | [-0.3577, +0.2066] |
| fil | 570 | 555 | +0.4111 | [+0.3428, +0.4760] | 30 | 30 | +0.5084 | [+0.2269, +0.7254] | +0.0973 | [-0.1876, +0.3308] |
| fr | 569 | 191 | +0.5299 | [+0.4689, +0.5892] | 30 | 11 | +0.3865 | [+0.1385, +0.6041] | -0.1433 | [-0.4061, +0.0853] |
| it | 570 | 192 | +0.5607 | [+0.5077, +0.6155] | 30 | 10 | +0.6557 | [+0.4322, +0.8181] | +0.0950 | [-0.1361, +0.2688] |
| ja | 570 | 190 | +0.5734 | [+0.5045, +0.6386] | 30 | 10 | +0.6883 | [+0.5060, +0.8190] | +0.1150 | [-0.0818, +0.2579] |
| pt | 567 | 562 | +0.7312 | [+0.6829, +0.7721] | 30 | 30 | +0.7094 | [+0.5116, +0.8597] | -0.0219 | [-0.2220, +0.1343] |
| si | 600 | 578 | +0.2535 | [+0.1950, +0.3093] | 30 | 30 | +0.2722 | [+0.0096, +0.5244] | +0.0187 | [-0.2520, +0.2828] |
| **medie** | | | **+0.5478** | | | | **+0.5760** | | **+0.0282** | |

**Δ split mediu +0.0282**, sd intre limbi 0.1068, interval -0.1433 pana la +0.2129. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4321 | +0.4281 | -0.0040 |
| de | +0.7502 | +0.7379 | -0.0123 |
| en | +0.6832 | +0.7040 | +0.0208 |
| es | +0.6740 | +0.6720 | -0.0020 |
| fil | +0.5084 | +0.5209 | +0.0125 |
| fr | +0.3865 | +0.3771 | -0.0094 |
| it | +0.6557 | +0.6464 | -0.0093 |
| ja | +0.6883 | +0.6673 | -0.0210 |
| pt | +0.7094 | +0.7149 | +0.0055 |
| si | +0.2722 | +0.2900 | +0.0178 |

**Diferenta medie -0.0001**, interval -0.0210 pana la +0.0208.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3861 | +0.4958 | +0.0213 | -0.0637 |
| de | +0.5297 | +0.7412 | +0.0076 | +0.0090 |
| en | +0.7810 | +0.5740 | +0.0091 | +0.1092 |
| es | +0.6794 | +0.7139 | +0.0042 | -0.0399 |
| fil | +0.4015 | +0.5386 | +0.0096 | -0.0302 |
| fr | +0.5101 | +0.2882 | +0.0198 | +0.0983 |
| it | +0.5406 | +0.6530 | +0.0201 | +0.0027 |
| ja | +0.4972 | +0.5187 | +0.0762 | +0.1696 |
| pt | +0.7312 | +0.7085 | +0.0000 | +0.0009 |
| si | +0.2376 | +0.2617 | +0.0159 | +0.0105 |
