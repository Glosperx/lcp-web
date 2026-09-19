# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:08:19 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4221 | [+0.3445, +0.4925] | 30 | 11 | +0.3716 | [-0.1680, +0.7122] | -0.0505 | [-0.6052, +0.3010] |
| de | 570 | 193 | +0.6242 | [+0.5720, +0.6754] | 23 | 11 | +0.7785 | [+0.4988, +0.9124] | +0.1543 | [-0.1234, +0.3030] |
| en | 570 | 190 | +0.8228 | [+0.7848, +0.8554] | 30 | 10 | +0.7144 | [+0.4335, +0.8653] | -0.1085 | [-0.3926, +0.0439] |
| es | 593 | 208 | +0.6645 | [+0.6209, +0.7032] | 30 | 10 | +0.7180 | [+0.4312, +0.8840] | +0.0535 | [-0.2377, +0.2276] |
| fil | 570 | 555 | +0.4049 | [+0.3326, +0.4728] | 30 | 30 | +0.5720 | [+0.3295, +0.7902] | +0.1672 | [-0.0865, +0.4013] |
| fr | 569 | 191 | +0.5276 | [+0.4539, +0.5933] | 30 | 11 | +0.3802 | [+0.0227, +0.6471] | -0.1474 | [-0.5111, +0.1393] |
| it | 570 | 192 | +0.6104 | [+0.5539, +0.6699] | 30 | 10 | +0.6804 | [+0.4764, +0.8282] | +0.0699 | [-0.1467, +0.2337] |
| ja | 570 | 190 | +0.5559 | [+0.4885, +0.6176] | 30 | 10 | +0.5574 | [+0.2794, +0.7410] | +0.0015 | [-0.2764, +0.1948] |
| pt | 567 | 562 | +0.7499 | [+0.7104, +0.7866] | 30 | 30 | +0.7737 | [+0.5968, +0.8987] | +0.0239 | [-0.1556, +0.1497] |
| si | 600 | 578 | +0.1964 | [+0.1433, +0.2465] | 30 | 30 | +0.0110 | [-0.4133, +0.1870] | -0.1854 | [-0.6262, +0.0067] |
| **medie** | | | **+0.5579** | | | | **+0.5557** | | **-0.0022** | |

**Δ split mediu -0.0022**, sd intre limbi 0.1204, interval -0.1854 pana la +0.1672. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3716 | +0.2090 | -0.1626 |
| de | +0.7785 | +0.7625 | -0.0160 |
| en | +0.7144 | +0.6752 | -0.0392 |
| es | +0.7180 | +0.6974 | -0.0206 |
| fil | +0.5720 | +0.6179 | +0.0459 |
| fr | +0.3802 | +0.3070 | -0.0732 |
| it | +0.6804 | +0.6801 | -0.0003 |
| ja | +0.5574 | +0.4862 | -0.0712 |
| pt | +0.7737 | +0.7772 | +0.0035 |
| si | +0.0110 | -0.0084 | -0.0194 |

**Diferenta medie -0.0353**, interval -0.1626 pana la +0.0459.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4042 | +0.3048 | +0.0179 | +0.0668 |
| de | +0.6570 | +0.8225 | -0.0328 | -0.0440 |
| en | +0.8028 | +0.7101 | +0.0200 | +0.0043 |
| es | +0.6493 | +0.7176 | +0.0152 | +0.0004 |
| fil | +0.4003 | +0.5669 | +0.0046 | +0.0051 |
| fr | +0.5327 | +0.3609 | -0.0051 | +0.0193 |
| it | +0.6320 | +0.7303 | -0.0216 | -0.0499 |
| ja | +0.5935 | +0.4923 | -0.0376 | +0.0651 |
| pt | +0.7737 | +0.7492 | -0.0238 | +0.0245 |
| si | +0.1607 | -0.1471 | +0.0357 | +0.1581 |
