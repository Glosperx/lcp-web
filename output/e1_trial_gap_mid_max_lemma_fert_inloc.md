# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-23 12:15:43 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4400 | [+0.3566, +0.5134] | 30 | 11 | +0.2651 | [-0.2100, +0.7111] | -0.1749 | [-0.6649, +0.2764] |
| de | 570 | 193 | +0.6485 | [+0.5941, +0.6999] | 23 | 11 | +0.7804 | [+0.5021, +0.9336] | +0.1318 | [-0.1499, +0.2938] |
| en | 570 | 190 | +0.8177 | [+0.7814, +0.8491] | 30 | 10 | +0.6572 | [+0.4619, +0.7916] | -0.1606 | [-0.3566, -0.0183] |
| es | 593 | 208 | +0.6584 | [+0.6120, +0.7006] | 30 | 10 | +0.7106 | [+0.4544, +0.8599] | +0.0522 | [-0.2035, +0.2053] |
| fil | 570 | 555 | +0.4027 | [+0.3341, +0.4680] | 30 | 30 | +0.5801 | [+0.3456, +0.7612] | +0.1774 | [-0.0586, +0.3695] |
| fr | 569 | 191 | +0.5334 | [+0.4650, +0.5972] | 30 | 11 | +0.3772 | [+0.0112, +0.6751] | -0.1562 | [-0.5355, +0.1566] |
| it | 570 | 192 | +0.6254 | [+0.5704, +0.6810] | 30 | 10 | +0.6189 | [+0.3877, +0.7918] | -0.0064 | [-0.2439, +0.1828] |
| ja | 570 | 190 | +0.5786 | [+0.5200, +0.6327] | 30 | 10 | +0.5223 | [+0.3046, +0.6858] | -0.0563 | [-0.2763, +0.1150] |
| pt | 567 | 562 | +0.7621 | [+0.7210, +0.7977] | 30 | 30 | +0.7797 | [+0.6021, +0.9100] | +0.0176 | [-0.1710, +0.1523] |
| si | 600 | 578 | +0.2117 | [+0.1496, +0.2782] | 30 | 30 | -0.1195 | [-0.4130, +0.2138] | -0.3313 | [-0.6345, +0.0030] |
| **medie** | | | **+0.5678** | | | | **+0.5172** | | **-0.0507** | |

**Δ split mediu -0.0507**, sd intre limbi 0.1563, interval -0.3313 pana la +0.1774. Trial-ul e mai mare pe 4 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.2651 | +0.2621 | -0.0030 |
| de | +0.7804 | +0.7690 | -0.0114 |
| en | +0.6572 | +0.6455 | -0.0117 |
| es | +0.7106 | +0.7132 | +0.0026 |
| fil | +0.5801 | +0.5847 | +0.0046 |
| fr | +0.3772 | +0.3466 | -0.0306 |
| it | +0.6189 | +0.6272 | +0.0083 |
| ja | +0.5223 | +0.5036 | -0.0187 |
| pt | +0.7797 | +0.7868 | +0.0071 |
| si | -0.1195 | -0.0089 | +0.1106 |

**Diferenta medie +0.0058**, interval -0.0306 pana la +0.1106.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.4203 | +0.2029 | +0.0197 | +0.0622 |
| de | +0.6648 | +0.8453 | -0.0163 | -0.0649 |
| en | +0.8164 | +0.6280 | +0.0013 | +0.0292 |
| es | +0.6374 | +0.6946 | +0.0210 | +0.0160 |
| fil | +0.4096 | +0.5518 | -0.0069 | +0.0283 |
| fr | +0.5217 | +0.4073 | +0.0117 | -0.0301 |
| it | +0.6323 | +0.6466 | -0.0069 | -0.0277 |
| ja | +0.5939 | +0.4596 | -0.0153 | +0.0627 |
| pt | +0.7709 | +0.7655 | -0.0088 | +0.0142 |
| si | +0.1972 | -0.0815 | +0.0145 | -0.0380 |
