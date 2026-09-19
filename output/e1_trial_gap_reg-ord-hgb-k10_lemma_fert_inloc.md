# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 20:52:07 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.4018 | [+0.3279, +0.4687] | 30 | 11 | +0.4169 | [-0.1569, +0.7867] | +0.0151 | [-0.5584, +0.3995] |
| de | 570 | 193 | +0.5910 | [+0.5390, +0.6405] | 23 | 11 | +0.7290 | [+0.4623, +0.8725] | +0.1380 | [-0.1402, +0.2928] |
| en | 570 | 190 | +0.7939 | [+0.7579, +0.8264] | 30 | 10 | +0.6943 | [+0.4866, +0.8624] | -0.0996 | [-0.3124, +0.0733] |
| es | 593 | 208 | +0.6601 | [+0.6170, +0.6990] | 30 | 10 | +0.6717 | [+0.3765, +0.8515] | +0.0116 | [-0.2797, +0.1939] |
| fil | 570 | 555 | +0.4047 | [+0.3361, +0.4680] | 30 | 30 | +0.5948 | [+0.3527, +0.8031] | +0.1901 | [-0.0581, +0.4080] |
| fr | 569 | 191 | +0.5583 | [+0.4919, +0.6168] | 30 | 11 | +0.3836 | [+0.0591, +0.6366] | -0.1747 | [-0.5144, +0.0922] |
| it | 570 | 192 | +0.5939 | [+0.5396, +0.6487] | 30 | 10 | +0.6855 | [+0.4928, +0.8223] | +0.0916 | [-0.1116, +0.2430] |
| ja | 570 | 190 | +0.5576 | [+0.4949, +0.6168] | 30 | 10 | +0.5514 | [+0.3052, +0.7088] | -0.0062 | [-0.2565, +0.1564] |
| pt | 567 | 562 | +0.7597 | [+0.7209, +0.7954] | 30 | 30 | +0.7742 | [+0.5973, +0.9096] | +0.0145 | [-0.1624, +0.1493] |
| si | 600 | 578 | +0.2359 | [+0.1719, +0.3021] | 30 | 30 | -0.0810 | [-0.4395, +0.3036] | -0.3169 | [-0.6805, +0.0608] |
| **medie** | | | **+0.5557** | | | | **+0.5420** | | **-0.0136** | |

**Δ split mediu -0.0136**, sd intre limbi 0.1503, interval -0.3169 pana la +0.1901. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4169 | +0.3608 | -0.0561 |
| de | +0.7290 | +0.7253 | -0.0037 |
| en | +0.6943 | +0.6860 | -0.0083 |
| es | +0.6717 | +0.6758 | +0.0041 |
| fil | +0.5948 | +0.6197 | +0.0249 |
| fr | +0.3836 | +0.3554 | -0.0282 |
| it | +0.6855 | +0.6857 | +0.0002 |
| ja | +0.5514 | +0.4948 | -0.0566 |
| pt | +0.7742 | +0.7704 | -0.0038 |
| si | -0.0810 | +0.0133 | +0.0943 |

**Diferenta medie -0.0033**, interval -0.0566 pana la +0.0943.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3894 | +0.3151 | +0.0124 | +0.1018 |
| de | +0.6271 | +0.7847 | -0.0361 | -0.0557 |
| en | +0.7946 | +0.6896 | -0.0007 | +0.0047 |
| es | +0.6574 | +0.6539 | +0.0027 | +0.0178 |
| fil | +0.4076 | +0.5759 | -0.0029 | +0.0189 |
| fr | +0.5514 | +0.3412 | +0.0069 | +0.0424 |
| it | +0.6051 | +0.7189 | -0.0112 | -0.0334 |
| ja | +0.6151 | +0.5280 | -0.0575 | +0.0234 |
| pt | +0.7767 | +0.7869 | -0.0170 | -0.0127 |
| si | +0.2658 | -0.1371 | -0.0299 | +0.0561 |
