# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:42:45 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4519 | [+0.3634, +0.5306] | 30 | 11 | +0.3845 | [+0.0487, +0.6406] | -0.0674 | [-0.4008, +0.2037] |
| de | 570 | 193 | +0.5269 | [+0.4588, +0.5907] | 23 | 11 | +0.7605 | [+0.4096, +0.9079] | +0.2336 | [-0.1268, +0.3972] |
| en | 570 | 190 | +0.7886 | [+0.7496, +0.8227] | 30 | 10 | +0.6977 | [+0.5320, +0.8234] | -0.0908 | [-0.2703, +0.0420] |
| es | 593 | 208 | +0.6342 | [+0.5787, +0.6843] | 30 | 10 | +0.6708 | [+0.3948, +0.8383] | +0.0366 | [-0.2349, +0.2235] |
| fil | 570 | 555 | +0.3947 | [+0.3235, +0.4643] | 30 | 30 | +0.4744 | [+0.1979, +0.6896] | +0.0797 | [-0.1937, +0.3110] |
| fr | 569 | 191 | +0.5115 | [+0.4503, +0.5701] | 30 | 11 | +0.5415 | [+0.3164, +0.7280] | +0.0300 | [-0.2022, +0.2266] |
| it | 570 | 192 | +0.5952 | [+0.5375, +0.6507] | 30 | 10 | +0.6763 | [+0.4702, +0.8237] | +0.0812 | [-0.1302, +0.2431] |
| ja | 570 | 190 | +0.5549 | [+0.4731, +0.6269] | 30 | 10 | +0.6473 | [+0.3195, +0.8364] | +0.0924 | [-0.2479, +0.2979] |
| pt | 567 | 562 | +0.7222 | [+0.6770, +0.7616] | 30 | 30 | +0.6772 | [+0.4224, +0.8749] | -0.0450 | [-0.2995, +0.1548] |
| si | 600 | 578 | +0.3481 | [+0.2816, +0.4125] | 30 | 30 | +0.2821 | [-0.1836, +0.5590] | -0.0660 | [-0.5179, +0.2168] |
| **medie** | | | **+0.5528** | | | | **+0.5812** | | **+0.0284** | |

**Δ split mediu +0.0284**, sd intre limbi 0.0997, interval -0.0908 pana la +0.2336. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3845 | +0.3843 | -0.0002 |
| de | +0.7605 | +0.7604 | -0.0001 |
| en | +0.6977 | +0.6978 | +0.0001 |
| es | +0.6708 | +0.6708 | +0.0000 |
| fil | +0.4744 | +0.4725 | -0.0019 |
| fr | +0.5415 | +0.5414 | -0.0001 |
| it | +0.6763 | +0.6767 | +0.0004 |
| ja | +0.6473 | +0.6461 | -0.0012 |
| pt | +0.6772 | +0.6771 | -0.0001 |
| si | +0.2821 | +0.2784 | -0.0037 |

**Diferenta medie -0.0007**, interval -0.0037 pana la +0.0004.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4177 | +0.4301 | +0.0342 | -0.0456 |
| de | +0.6163 | +0.8387 | -0.0894 | -0.0782 |
| en | +0.7822 | +0.7068 | +0.0064 | -0.0091 |
| es | +0.6560 | +0.5823 | -0.0218 | +0.0885 |
| fil | +0.4076 | +0.4946 | -0.0129 | -0.0202 |
| fr | +0.4481 | +0.3312 | +0.0634 | +0.2103 |
| it | +0.5956 | +0.6957 | -0.0004 | -0.0194 |
| ja | +0.5394 | +0.5415 | +0.0155 | +0.1058 |
| pt | +0.7281 | +0.7488 | -0.0059 | -0.0716 |
| si | +0.2820 | +0.3436 | +0.0661 | -0.0615 |
