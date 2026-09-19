# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:09:49 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4479 | [+0.3660, +0.5207] | 30 | 11 | +0.3909 | [-0.0506, +0.7170] | -0.0570 | [-0.5084, +0.2780] |
| de | 570 | 193 | +0.6465 | [+0.5926, +0.6959] | 23 | 11 | +0.7674 | [+0.5055, +0.8887] | +0.1209 | [-0.1520, +0.2541] |
| en | 570 | 190 | +0.8214 | [+0.7856, +0.8504] | 30 | 10 | +0.7136 | [+0.4758, +0.8279] | -0.1078 | [-0.3496, +0.0121] |
| es | 593 | 208 | +0.6705 | [+0.6228, +0.7124] | 30 | 10 | +0.7169 | [+0.4123, +0.8830] | +0.0464 | [-0.2472, +0.2178] |
| fil | 570 | 555 | +0.4030 | [+0.3325, +0.4699] | 30 | 30 | +0.5477 | [+0.3121, +0.7536] | +0.1447 | [-0.1118, +0.3628] |
| fr | 569 | 191 | +0.5414 | [+0.4741, +0.6025] | 30 | 11 | +0.4052 | [+0.0414, +0.6711] | -0.1362 | [-0.5108, +0.1441] |
| it | 570 | 192 | +0.6262 | [+0.5716, +0.6798] | 30 | 10 | +0.6748 | [+0.4883, +0.8168] | +0.0486 | [-0.1414, +0.2067] |
| ja | 570 | 190 | +0.5624 | [+0.5019, +0.6187] | 30 | 10 | +0.4188 | [+0.2208, +0.5731] | -0.1436 | [-0.3500, +0.0191] |
| pt | 567 | 562 | +0.7700 | [+0.7293, +0.8059] | 30 | 30 | +0.7971 | [+0.6390, +0.9088] | +0.0271 | [-0.1372, +0.1439] |
| si | 600 | 578 | +0.2693 | [+0.2019, +0.3360] | 30 | 30 | -0.0680 | [-0.4310, +0.3242] | -0.3372 | [-0.7065, +0.0512] |
| **medie** | | | **+0.5759** | | | | **+0.5364** | | **-0.0394** | |

**Δ split mediu -0.0394**, sd intre limbi 0.1464, interval -0.3372 pana la +0.1447. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3909 | +0.3646 | -0.0263 |
| de | +0.7674 | +0.7681 | +0.0007 |
| en | +0.7136 | +0.7139 | +0.0003 |
| es | +0.7169 | +0.7161 | -0.0008 |
| fil | +0.5477 | +0.5561 | +0.0084 |
| fr | +0.4052 | +0.3748 | -0.0304 |
| it | +0.6748 | +0.6766 | +0.0018 |
| ja | +0.4188 | +0.4001 | -0.0187 |
| pt | +0.7971 | +0.8018 | +0.0047 |
| si | -0.0680 | +0.0223 | +0.0903 |

**Diferenta medie +0.0030**, interval -0.0304 pana la +0.0903.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4142 | +0.2537 | +0.0337 | +0.1372 |
| de | +0.6640 | +0.8238 | -0.0175 | -0.0564 |
| en | +0.8226 | +0.6353 | -0.0012 | +0.0783 |
| es | +0.6435 | +0.7152 | +0.0270 | +0.0017 |
| fil | +0.3961 | +0.4317 | +0.0069 | +0.1160 |
| fr | +0.5524 | +0.4371 | -0.0110 | -0.0319 |
| it | +0.6302 | +0.6510 | -0.0040 | +0.0238 |
| ja | +0.5659 | +0.3915 | -0.0035 | +0.0273 |
| pt | +0.7745 | +0.8179 | -0.0045 | -0.0208 |
| si | +0.2413 | -0.0761 | +0.0280 | +0.0081 |
