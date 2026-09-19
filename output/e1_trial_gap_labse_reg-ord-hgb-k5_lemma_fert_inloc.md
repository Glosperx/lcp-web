# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat

Generat 2026-08-26 21:30:27 de `finetune_xlmr.py --frozentrial`. Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in `output/e1_frozen_preds.csv`.

Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.

## r pe test fata de r pe trial

| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.3906 | [+0.3165, +0.4604] | 30 | 11 | +0.4184 | [-0.0602, +0.7555] | +0.0279 | [-0.4596, +0.3727] |
| de | 570 | 193 | +0.5715 | [+0.5210, +0.6208] | 23 | 11 | +0.7505 | [+0.4970, +0.8887] | +0.1790 | [-0.0742, +0.3305] |
| en | 570 | 190 | +0.7833 | [+0.7495, +0.8149] | 30 | 10 | +0.6897 | [+0.5143, +0.8205] | -0.0937 | [-0.2695, +0.0440] |
| es | 593 | 208 | +0.6479 | [+0.6057, +0.6877] | 30 | 10 | +0.6346 | [+0.3910, +0.8186] | -0.0133 | [-0.2615, +0.1714] |
| fil | 570 | 555 | +0.4059 | [+0.3363, +0.4698] | 30 | 30 | +0.5663 | [+0.3074, +0.7841] | +0.1604 | [-0.0994, +0.3898] |
| fr | 569 | 191 | +0.5546 | [+0.4914, +0.6132] | 30 | 11 | +0.4743 | [+0.1754, +0.6905] | -0.0802 | [-0.3888, +0.1484] |
| it | 570 | 192 | +0.5824 | [+0.5305, +0.6354] | 30 | 10 | +0.7013 | [+0.5495, +0.8216] | +0.1189 | [-0.0448, +0.2551] |
| ja | 570 | 190 | +0.4845 | [+0.4164, +0.5497] | 30 | 10 | +0.4693 | [+0.0636, +0.7356] | -0.0152 | [-0.4235, +0.2446] |
| pt | 567 | 562 | +0.7652 | [+0.7292, +0.7998] | 30 | 30 | +0.7784 | [+0.5989, +0.9147] | +0.0132 | [-0.1650, +0.1501] |
| si | 600 | 578 | +0.3199 | [+0.2503, +0.3858] | 30 | 30 | +0.4432 | [+0.0636, +0.6935] | +0.1233 | [-0.2516, +0.3810] |
| **medie** | | | **+0.5506** | | | | **+0.5926** | | **+0.0420** | |

**Δ split mediu +0.0420**, sd intre limbi 0.0978, interval -0.0937 pana la +0.1790. Trial-ul e mai mare pe 6 din 10 limbi.

Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.

## Centrarea per limba: cat din decalaj vine din ea

`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea din decalaj care tine de centrare, nu de split.

| limba | r trial selfmu | r trial testmu | diferenta |
|---|---|---|---|
| ca | +0.4184 | +0.3676 | -0.0508 |
| de | +0.7505 | +0.7352 | -0.0153 |
| en | +0.6897 | +0.6852 | -0.0045 |
| es | +0.6346 | +0.6264 | -0.0082 |
| fil | +0.5663 | +0.5902 | +0.0239 |
| fr | +0.4743 | +0.4567 | -0.0176 |
| it | +0.7013 | +0.7034 | +0.0021 |
| ja | +0.4693 | +0.4247 | -0.0446 |
| pt | +0.7784 | +0.7835 | +0.0051 |
| si | +0.4432 | +0.5119 | +0.0687 |

**Diferenta medie -0.0041**, interval -0.0508 pana la +0.0687.

## Bratul EN-only, pe ambele splituri

| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |
|---|---|---|---|---|
| ca | +0.3984 | +0.4037 | -0.0078 | +0.0147 |
| de | +0.6109 | +0.8014 | -0.0394 | -0.0509 |
| en | +0.7895 | +0.6915 | -0.0062 | -0.0018 |
| es | +0.6701 | +0.5754 | -0.0222 | +0.0592 |
| fil | +0.4017 | +0.5907 | +0.0042 | -0.0244 |
| fr | +0.5161 | +0.3561 | +0.0385 | +0.1182 |
| it | +0.5883 | +0.7073 | -0.0059 | -0.0060 |
| ja | +0.5889 | +0.4916 | -0.1044 | -0.0223 |
| pt | +0.7643 | +0.7516 | +0.0009 | +0.0268 |
| si | +0.2103 | +0.2111 | +0.1096 | +0.2321 |
