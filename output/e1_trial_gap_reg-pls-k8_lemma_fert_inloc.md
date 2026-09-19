# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 17:20:38 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3945 | [+0.3057, +0.4800] | 30 | 11 | +0.1594 | [-0.2932, +0.6714] | -0.2350 | [-0.6917, +0.2883] |
| de | 570 | 193 | +0.6015 | [+0.5396, +0.6552] | 23 | 11 | +0.6614 | [+0.4208, +0.8246] | +0.0599 | [-0.1806, +0.2376] |
| en | 570 | 190 | +0.7623 | [+0.7155, +0.8020] | 30 | 10 | +0.6389 | [+0.3987, +0.8127] | -0.1233 | [-0.3689, +0.0557] |
| es | 593 | 208 | +0.6020 | [+0.5481, +0.6495] | 30 | 10 | +0.6033 | [+0.2323, +0.8118] | +0.0013 | [-0.3756, +0.2169] |
| fil | 570 | 555 | +0.4243 | [+0.3554, +0.4863] | 30 | 30 | +0.5065 | [+0.2143, +0.7163] | +0.0822 | [-0.2193, +0.3102] |
| fr | 569 | 191 | +0.4821 | [+0.4171, +0.5444] | 30 | 11 | +0.2052 | [-0.1724, +0.5682] | -0.2769 | [-0.6669, +0.0983] |
| it | 570 | 192 | +0.5780 | [+0.5178, +0.6366] | 30 | 10 | +0.5900 | [+0.3447, +0.7733] | +0.0120 | [-0.2346, +0.2106] |
| ja | 570 | 190 | +0.6169 | [+0.5580, +0.6712] | 30 | 10 | +0.5499 | [+0.3996, +0.6611] | -0.0671 | [-0.2285, +0.0593] |
| pt | 567 | 562 | +0.6926 | [+0.6439, +0.7353] | 30 | 30 | +0.7405 | [+0.5534, +0.8728] | +0.0479 | [-0.1429, +0.1904] |
| si | 600 | 578 | +0.2660 | [+0.2074, +0.3271] | 30 | 30 | +0.0486 | [-0.3479, +0.4680] | -0.2174 | [-0.6029, +0.2067] |
| **medie** | | | **+0.5420** | | | | **+0.4704** | | **-0.0716** | |

**Δ split mediu -0.0716**, sd intre limbi 0.1335, interval -0.2769 pana la +0.0822. Trial-ul e mai mare pe 5 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.1594 | +0.1594 | +0.0000 |
| de | +0.6614 | +0.6614 | +0.0000 |
| en | +0.6389 | +0.6389 | +0.0000 |
| es | +0.6033 | +0.6033 | +0.0000 |
| fil | +0.5065 | +0.5065 | +0.0000 |
| fr | +0.2052 | +0.2052 | +0.0000 |
| it | +0.5900 | +0.5900 | +0.0000 |
| ja | +0.5499 | +0.5499 | +0.0000 |
| pt | +0.7405 | +0.7405 | +0.0000 |
| si | +0.0486 | +0.0486 | +0.0000 |

**Diferenta medie +0.0000**, interval +0.0000 pana la +0.0000.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3826 | +0.1812 | +0.0119 | -0.0218 |
| de | +0.6152 | +0.7714 | -0.0137 | -0.1100 |
| en | +0.7701 | +0.5618 | -0.0078 | +0.0771 |
| es | +0.6012 | +0.7169 | +0.0008 | -0.1136 |
| fil | +0.4188 | +0.4761 | +0.0055 | +0.0304 |
| fr | +0.4924 | +0.2795 | -0.0103 | -0.0743 |
| it | +0.5811 | +0.6149 | -0.0031 | -0.0249 |
| ja | +0.5784 | +0.4756 | +0.0385 | +0.0743 |
| pt | +0.7204 | +0.7497 | -0.0278 | -0.0092 |
| si | +0.2452 | +0.1862 | +0.0208 | -0.1376 |
