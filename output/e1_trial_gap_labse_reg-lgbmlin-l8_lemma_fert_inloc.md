# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:40:36 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3873 | [+0.3095, +0.4592] | 30 | 11 | +0.3453 | [-0.1087, +0.6911] | -0.0421 | [-0.5085, +0.3158] |
| de | 570 | 193 | +0.6043 | [+0.5533, +0.6531] | 23 | 11 | +0.7656 | [+0.5488, +0.8808] | +0.1613 | [-0.0638, +0.2912] |
| en | 570 | 190 | +0.8108 | [+0.7750, +0.8412] | 30 | 10 | +0.7133 | [+0.5692, +0.8317] | -0.0975 | [-0.2387, +0.0278] |
| es | 593 | 208 | +0.6570 | [+0.6128, +0.6983] | 30 | 10 | +0.6884 | [+0.4528, +0.8451] | +0.0314 | [-0.2086, +0.1923] |
| fil | 570 | 555 | +0.3817 | [+0.3078, +0.4497] | 30 | 30 | +0.5394 | [+0.2685, +0.7693] | +0.1577 | [-0.1189, +0.4036] |
| fr | 569 | 191 | +0.5209 | [+0.4533, +0.5832] | 30 | 11 | +0.4308 | [+0.0961, +0.6664] | -0.0901 | [-0.4322, +0.1557] |
| it | 570 | 192 | +0.6036 | [+0.5508, +0.6582] | 30 | 10 | +0.7324 | [+0.5829, +0.8401] | +0.1288 | [-0.0327, +0.2526] |
| ja | 570 | 190 | +0.5038 | [+0.4348, +0.5699] | 30 | 10 | +0.5270 | [+0.2242, +0.7552] | +0.0232 | [-0.2921, +0.2646] |
| pt | 567 | 562 | +0.7600 | [+0.7208, +0.7961] | 30 | 30 | +0.7582 | [+0.5752, +0.9114] | -0.0018 | [-0.1925, +0.1528] |
| si | 600 | 578 | +0.1886 | [+0.1352, +0.2370] | 30 | 30 | +0.0568 | [-0.2204, +0.2780] | -0.1317 | [-0.4075, +0.0942] |
| **medie** | | | **+0.5418** | | | | **+0.5557** | | **+0.0139** | |

**Δ split mediu +0.0139**, sd intre limbi 0.1074, interval -0.1317 pana la +0.1613. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.3453 | +0.1807 | -0.1646 |
| de | +0.7656 | +0.7292 | -0.0364 |
| en | +0.7133 | +0.7205 | +0.0072 |
| es | +0.6884 | +0.6538 | -0.0346 |
| fil | +0.5394 | +0.5805 | +0.0411 |
| fr | +0.4308 | +0.3720 | -0.0588 |
| it | +0.7324 | +0.7332 | +0.0008 |
| ja | +0.5270 | +0.4840 | -0.0430 |
| pt | +0.7582 | +0.7599 | +0.0017 |
| si | +0.0568 | +0.1095 | +0.0527 |

**Diferenta medie -0.0234**, interval -0.1646 pana la +0.0527.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3978 | +0.3948 | -0.0105 | -0.0495 |
| de | +0.6438 | +0.8541 | -0.0395 | -0.0885 |
| en | +0.7825 | +0.6295 | +0.0283 | +0.0838 |
| es | +0.6585 | +0.6502 | -0.0015 | +0.0382 |
| fil | +0.3705 | +0.5291 | +0.0112 | +0.0103 |
| fr | +0.5178 | +0.3214 | +0.0031 | +0.1094 |
| it | +0.6387 | +0.7124 | -0.0351 | +0.0200 |
| ja | +0.5608 | +0.4598 | -0.0570 | +0.0672 |
| pt | +0.7524 | +0.7873 | +0.0076 | -0.0291 |
| si | +0.0989 | -0.1314 | +0.0897 | +0.1882 |
