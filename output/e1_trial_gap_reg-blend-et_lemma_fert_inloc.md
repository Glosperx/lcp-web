# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-24 12:56:12 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4277 | [+0.3465, +0.5069] | 30 | 11 | +0.2905 | [-0.1794, +0.6839] | -0.1372 | [-0.6086, +0.2691] |
| de | 570 | 193 | +0.6505 | [+0.5965, +0.7000] | 23 | 11 | +0.7625 | [+0.4935, +0.8785] | +0.1119 | [-0.1611, +0.2409] |
| en | 570 | 190 | +0.8103 | [+0.7714, +0.8421] | 30 | 10 | +0.6947 | [+0.4519, +0.8349] | -0.1155 | [-0.3543, +0.0323] |
| es | 593 | 208 | +0.6496 | [+0.6007, +0.6931] | 30 | 10 | +0.6783 | [+0.3859, +0.8420] | +0.0286 | [-0.2591, +0.1950] |
| fil | 570 | 555 | +0.4107 | [+0.3405, +0.4773] | 30 | 30 | +0.5729 | [+0.3271, +0.7479] | +0.1622 | [-0.0916, +0.3541] |
| fr | 569 | 191 | +0.5477 | [+0.4819, +0.6050] | 30 | 11 | +0.3114 | [-0.0721, +0.6257] | -0.2363 | [-0.6275, +0.0850] |
| it | 570 | 192 | +0.6259 | [+0.5699, +0.6810] | 30 | 10 | +0.6479 | [+0.4081, +0.8203] | +0.0220 | [-0.2221, +0.2080] |
| ja | 570 | 190 | +0.6361 | [+0.5776, +0.6898] | 30 | 10 | +0.6115 | [+0.4472, +0.7223] | -0.0247 | [-0.2006, +0.1002] |
| pt | 567 | 562 | +0.7613 | [+0.7209, +0.7967] | 30 | 30 | +0.7927 | [+0.6316, +0.9158] | +0.0313 | [-0.1346, +0.1547] |
| si | 600 | 578 | +0.2622 | [+0.1998, +0.3288] | 30 | 30 | +0.0352 | [-0.3448, +0.4577] | -0.2270 | [-0.6106, +0.1967] |
| **medie** | | | **+0.5782** | | | | **+0.5398** | | **-0.0385** | |

**Δ split mediu -0.0385**, sd intre limbi 0.1360, interval -0.2363 pana la +0.1622. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2905 | +0.2593 | -0.0312 |
| de | +0.7625 | +0.7653 | +0.0028 |
| en | +0.6947 | +0.6871 | -0.0076 |
| es | +0.6783 | +0.6812 | +0.0029 |
| fil | +0.5729 | +0.5794 | +0.0065 |
| fr | +0.3114 | +0.3080 | -0.0034 |
| it | +0.6479 | +0.6488 | +0.0009 |
| ja | +0.6115 | +0.5922 | -0.0193 |
| pt | +0.7927 | +0.7903 | -0.0024 |
| si | +0.0352 | +0.0107 | -0.0245 |

**Diferenta medie -0.0075**, interval -0.0312 pana la +0.0065.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4031 | +0.2330 | +0.0246 | +0.0575 |
| de | +0.6600 | +0.8137 | -0.0095 | -0.0512 |
| en | +0.8077 | +0.6728 | +0.0026 | +0.0219 |
| es | +0.6478 | +0.6816 | +0.0018 | -0.0033 |
| fil | +0.4228 | +0.5530 | -0.0121 | +0.0199 |
| fr | +0.5368 | +0.3387 | +0.0109 | -0.0273 |
| it | +0.6233 | +0.6496 | +0.0026 | -0.0017 |
| ja | +0.6056 | +0.5048 | +0.0305 | +0.1067 |
| pt | +0.7636 | +0.7807 | -0.0023 | +0.0120 |
| si | +0.2783 | +0.0203 | -0.0161 | +0.0149 |
