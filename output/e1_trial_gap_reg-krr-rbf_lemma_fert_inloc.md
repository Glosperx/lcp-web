# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 16:29:13 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3788 | [+0.2947, +0.4611] | 30 | 11 | +0.2607 | [-0.1444, +0.6726] | -0.1182 | [-0.5367, +0.2975] |
| de | 570 | 193 | +0.5647 | [+0.4998, +0.6235] | 23 | 11 | +0.6513 | [+0.3808, +0.8349] | +0.0866 | [-0.1791, +0.2786] |
| en | 570 | 190 | +0.7773 | [+0.7321, +0.8163] | 30 | 10 | +0.6284 | [+0.4274, +0.7896] | -0.1489 | [-0.3511, +0.0163] |
| es | 593 | 208 | +0.6213 | [+0.5709, +0.6690] | 30 | 10 | +0.6539 | [+0.2922, +0.8439] | +0.0326 | [-0.3155, +0.2267] |
| fil | 570 | 555 | +0.3832 | [+0.3139, +0.4475] | 30 | 30 | +0.3590 | [+0.0354, +0.6189] | -0.0242 | [-0.3610, +0.2490] |
| fr | 569 | 191 | +0.4789 | [+0.4107, +0.5443] | 30 | 11 | +0.2811 | [-0.1418, +0.6163] | -0.1978 | [-0.6271, +0.1585] |
| it | 570 | 192 | +0.5309 | [+0.4611, +0.5999] | 30 | 10 | +0.5501 | [+0.2854, +0.7647] | +0.0193 | [-0.2511, +0.2490] |
| ja | 570 | 190 | +0.6100 | [+0.5521, +0.6632] | 30 | 10 | +0.6275 | [+0.3433, +0.8004] | +0.0175 | [-0.2662, +0.1959] |
| pt | 567 | 562 | +0.6796 | [+0.6291, +0.7261] | 30 | 30 | +0.7624 | [+0.5927, +0.8786] | +0.0828 | [-0.0914, +0.2064] |
| si | 600 | 578 | +0.2974 | [+0.2353, +0.3579] | 30 | 30 | +0.1152 | [-0.2410, +0.4950] | -0.1821 | [-0.5438, +0.2109] |
| **medie** | | | **+0.5322** | | | | **+0.4890** | | **-0.0432** | |

**Δ split mediu -0.0432**, sd intre limbi 0.1087, interval -0.1978 pana la +0.0866. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2607 | +0.2538 | -0.0069 |
| de | +0.6513 | +0.6520 | +0.0007 |
| en | +0.6284 | +0.6716 | +0.0432 |
| es | +0.6539 | +0.6376 | -0.0163 |
| fil | +0.3590 | +0.3566 | -0.0024 |
| fr | +0.2811 | +0.2687 | -0.0124 |
| it | +0.5501 | +0.5434 | -0.0067 |
| ja | +0.6275 | +0.6593 | +0.0318 |
| pt | +0.7624 | +0.7733 | +0.0109 |
| si | +0.1152 | +0.1153 | +0.0001 |

**Diferenta medie +0.0042**, interval -0.0163 pana la +0.0432.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3163 | +0.2869 | +0.0625 | -0.0262 |
| de | +0.5529 | +0.7759 | +0.0118 | -0.1246 |
| en | +0.7449 | +0.5995 | +0.0324 | +0.0289 |
| es | +0.5256 | +0.6280 | +0.0957 | +0.0259 |
| fil | +0.4060 | +0.3910 | -0.0228 | -0.0320 |
| fr | +0.4664 | +0.3732 | +0.0125 | -0.0921 |
| it | +0.4876 | +0.4993 | +0.0433 | +0.0508 |
| ja | +0.5049 | +0.5931 | +0.1051 | +0.0344 |
| pt | +0.6971 | +0.7437 | -0.0175 | +0.0187 |
| si | +0.2748 | +0.1514 | +0.0226 | -0.0362 |
