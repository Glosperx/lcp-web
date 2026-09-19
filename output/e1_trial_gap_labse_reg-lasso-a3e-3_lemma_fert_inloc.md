# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:01:00 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4254 | [+0.3322, +0.5058] | 30 | 11 | +0.3663 | [-0.0680, +0.6998] | -0.0592 | [-0.4905, +0.2949] |
| de | 570 | 193 | +0.6069 | [+0.5556, +0.6562] | 23 | 11 | +0.8332 | [+0.5769, +0.9571] | +0.2263 | [-0.0397, +0.3638] |
| en | 570 | 190 | +0.7724 | [+0.7370, +0.8053] | 30 | 10 | +0.6376 | [+0.5365, +0.7711] | -0.1348 | [-0.2433, +0.0049] |
| es | 593 | 208 | +0.6601 | [+0.6118, +0.7011] | 30 | 10 | +0.6253 | [+0.3833, +0.7991] | -0.0347 | [-0.2921, +0.1473] |
| fil | 570 | 555 | +0.3912 | [+0.3194, +0.4616] | 30 | 30 | +0.5459 | [+0.2961, +0.7384] | +0.1547 | [-0.1008, +0.3610] |
| fr | 569 | 191 | +0.5599 | [+0.5010, +0.6147] | 30 | 11 | +0.4685 | [+0.1645, +0.6998] | -0.0914 | [-0.4060, +0.1480] |
| it | 570 | 192 | +0.6137 | [+0.5609, +0.6659] | 30 | 10 | +0.6538 | [+0.4807, +0.8054] | +0.0401 | [-0.1347, +0.2063] |
| ja | 570 | 190 | +0.5850 | [+0.5166, +0.6486] | 30 | 10 | +0.6283 | [+0.3060, +0.8350] | +0.0433 | [-0.2891, +0.2631] |
| pt | 567 | 562 | +0.7562 | [+0.7167, +0.7911] | 30 | 30 | +0.7235 | [+0.5353, +0.8874] | -0.0327 | [-0.2201, +0.1326] |
| si | 600 | 578 | +0.3260 | [+0.2492, +0.3971] | 30 | 30 | +0.4474 | [+0.1615, +0.6768] | +0.1214 | [-0.1644, +0.3694] |
| **medie** | | | **+0.5697** | | | | **+0.5930** | | **+0.0233** | |

**Δ split mediu +0.0233**, sd intre limbi 0.1156, interval -0.1348 pana la +0.2263. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3663 | +0.3663 | +0.0000 |
| de | +0.8332 | +0.8332 | +0.0000 |
| en | +0.6376 | +0.6376 | +0.0000 |
| es | +0.6253 | +0.6253 | +0.0000 |
| fil | +0.5459 | +0.5459 | +0.0000 |
| fr | +0.4685 | +0.4685 | +0.0000 |
| it | +0.6538 | +0.6538 | +0.0000 |
| ja | +0.6283 | +0.6283 | +0.0000 |
| pt | +0.7235 | +0.7235 | +0.0000 |
| si | +0.4474 | +0.4474 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3726 | +0.3424 | +0.0528 | +0.0239 |
| de | +0.6375 | +0.8471 | -0.0306 | -0.0139 |
| en | +0.7638 | +0.6307 | +0.0086 | +0.0069 |
| es | +0.6444 | +0.5645 | +0.0157 | +0.0608 |
| fil | +0.3874 | +0.5443 | +0.0038 | +0.0016 |
| fr | +0.5298 | +0.3242 | +0.0301 | +0.1443 |
| it | +0.6159 | +0.6220 | -0.0022 | +0.0318 |
| ja | +0.5440 | +0.5202 | +0.0410 | +0.1081 |
| pt | +0.7573 | +0.7293 | -0.0011 | -0.0058 |
| si | +0.1984 | +0.0998 | +0.1276 | +0.3476 |
