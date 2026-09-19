# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 13:15:10 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4636 | [+0.3851, +0.5305] | 30 | 11 | +0.4001 | [-0.0208, +0.7211] | -0.0635 | [-0.4952, +0.2662] |
| de | 570 | 193 | +0.6202 | [+0.5656, +0.6735] | 23 | 11 | +0.8011 | [+0.5785, +0.9175] | +0.1809 | [-0.0487, +0.3166] |
| en | 570 | 190 | +0.8155 | [+0.7799, +0.8461] | 30 | 10 | +0.7253 | [+0.4360, +0.8704] | -0.0902 | [-0.3907, +0.0615] |
| es | 593 | 208 | +0.7030 | [+0.6615, +0.7399] | 30 | 10 | +0.7154 | [+0.4477, +0.8806] | +0.0125 | [-0.2516, +0.1834] |
| fil | 570 | 555 | +0.4096 | [+0.3388, +0.4763] | 30 | 30 | +0.5631 | [+0.2909, +0.7692] | +0.1535 | [-0.1297, +0.3720] |
| fr | 569 | 191 | +0.5535 | [+0.4914, +0.6125] | 30 | 11 | +0.3711 | [+0.1231, +0.5893] | -0.1824 | [-0.4398, +0.0548] |
| it | 570 | 192 | +0.6177 | [+0.5666, +0.6710] | 30 | 10 | +0.6953 | [+0.5038, +0.8320] | +0.0776 | [-0.1245, +0.2284] |
| ja | 570 | 190 | +0.5709 | [+0.5041, +0.6355] | 30 | 10 | +0.7134 | [+0.4769, +0.8593] | +0.1425 | [-0.1048, +0.3027] |
| pt | 567 | 562 | +0.7664 | [+0.7218, +0.8046] | 30 | 30 | +0.7553 | [+0.5722, +0.8846] | -0.0111 | [-0.1974, +0.1244] |
| si | 600 | 578 | +0.2176 | [+0.1480, +0.2853] | 30 | 30 | +0.1690 | [-0.1050, +0.4536] | -0.0486 | [-0.3372, +0.2534] |
| **medie** | | | **+0.5738** | | | | **+0.5909** | | **+0.0171** | |

**Δ split mediu +0.0171**, sd intre limbi 0.1191, interval -0.1824 pana la +0.1809. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4001 | +0.3703 | -0.0298 |
| de | +0.8011 | +0.7935 | -0.0076 |
| en | +0.7253 | +0.7272 | +0.0019 |
| es | +0.7154 | +0.7039 | -0.0115 |
| fil | +0.5631 | +0.5676 | +0.0045 |
| fr | +0.3711 | +0.3588 | -0.0123 |
| it | +0.6953 | +0.6936 | -0.0017 |
| ja | +0.7134 | +0.6703 | -0.0431 |
| pt | +0.7553 | +0.7640 | +0.0087 |
| si | +0.1690 | +0.2817 | +0.1127 |

**Diferenta medie +0.0022**, interval -0.0431 pana la +0.1127.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4586 | +0.4082 | +0.0050 | -0.0081 |
| de | +0.6614 | +0.8646 | -0.0412 | -0.0635 |
| en | +0.8028 | +0.6781 | +0.0127 | +0.0472 |
| es | +0.6969 | +0.7042 | +0.0061 | +0.0112 |
| fil | +0.4107 | +0.5766 | -0.0011 | -0.0135 |
| fr | +0.5406 | +0.2624 | +0.0129 | +0.1087 |
| it | +0.6277 | +0.7181 | -0.0100 | -0.0228 |
| ja | +0.5706 | +0.6055 | +0.0003 | +0.1079 |
| pt | +0.7746 | +0.7532 | -0.0082 | +0.0021 |
| si | +0.1786 | +0.2761 | +0.0390 | -0.1071 |
