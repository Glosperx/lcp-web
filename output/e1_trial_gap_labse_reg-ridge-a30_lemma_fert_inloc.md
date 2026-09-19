# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:59:12 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4532 | [+0.3653, +0.5316] | 30 | 11 | +0.3798 | [+0.0502, +0.6057] | -0.0734 | [-0.4035, +0.1696] |
| de | 570 | 193 | +0.5672 | [+0.5058, +0.6251] | 23 | 11 | +0.7852 | [+0.4692, +0.9167] | +0.2180 | [-0.1041, +0.3641] |
| en | 570 | 190 | +0.7694 | [+0.7295, +0.8043] | 30 | 10 | +0.6505 | [+0.5097, +0.7929] | -0.1189 | [-0.2655, +0.0346] |
| es | 593 | 208 | +0.6298 | [+0.5765, +0.6780] | 30 | 10 | +0.6501 | [+0.3796, +0.8241] | +0.0203 | [-0.2470, +0.2039] |
| fil | 570 | 555 | +0.3842 | [+0.3129, +0.4548] | 30 | 30 | +0.4812 | [+0.2093, +0.6909] | +0.0970 | [-0.1804, +0.3202] |
| fr | 569 | 191 | +0.5103 | [+0.4484, +0.5673] | 30 | 11 | +0.4688 | [+0.2563, +0.6721] | -0.0416 | [-0.2603, +0.1605] |
| it | 570 | 192 | +0.5956 | [+0.5401, +0.6516] | 30 | 10 | +0.6787 | [+0.4686, +0.8239] | +0.0831 | [-0.1286, +0.2469] |
| ja | 570 | 190 | +0.5546 | [+0.4807, +0.6220] | 30 | 10 | +0.6687 | [+0.3833, +0.8275] | +0.1141 | [-0.1799, +0.2895] |
| pt | 567 | 562 | +0.7167 | [+0.6746, +0.7547] | 30 | 30 | +0.6958 | [+0.4550, +0.8815] | -0.0208 | [-0.2608, +0.1659] |
| si | 600 | 578 | +0.3412 | [+0.2637, +0.4138] | 30 | 30 | +0.2821 | [-0.2054, +0.5797] | -0.0591 | [-0.5597, +0.2453] |
| **medie** | | | **+0.5522** | | | | **+0.5741** | | **+0.0219** | |

**Δ split mediu +0.0219**, sd intre limbi 0.1042, interval -0.1189 pana la +0.2180. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3798 | +0.3798 | +0.0000 |
| de | +0.7852 | +0.7852 | +0.0000 |
| en | +0.6505 | +0.6505 | +0.0000 |
| es | +0.6501 | +0.6501 | +0.0000 |
| fil | +0.4812 | +0.4812 | +0.0000 |
| fr | +0.4688 | +0.4688 | +0.0000 |
| it | +0.6787 | +0.6787 | +0.0000 |
| ja | +0.6687 | +0.6687 | +0.0000 |
| pt | +0.6958 | +0.6958 | +0.0000 |
| si | +0.2821 | +0.2821 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4068 | +0.3233 | +0.0464 | +0.0565 |
| de | +0.6168 | +0.8431 | -0.0496 | -0.0579 |
| en | +0.7591 | +0.6633 | +0.0103 | -0.0128 |
| es | +0.6367 | +0.5530 | -0.0069 | +0.0971 |
| fil | +0.3934 | +0.4801 | -0.0092 | +0.0011 |
| fr | +0.4471 | +0.2393 | +0.0632 | +0.2295 |
| it | +0.5995 | +0.6752 | -0.0039 | +0.0035 |
| ja | +0.5177 | +0.5193 | +0.0369 | +0.1494 |
| pt | +0.7228 | +0.7536 | -0.0061 | -0.0578 |
| si | +0.2655 | +0.2877 | +0.0757 | -0.0056 |
