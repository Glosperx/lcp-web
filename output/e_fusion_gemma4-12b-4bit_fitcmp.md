# Ponderea potrivita pe trial fata de potrivita pe test, brat `gemma4-12b-4bit`

Generat 2026-08-18 00:59:50 de `fuse_ab.py --arm gemma4-12b-4bit --fit both`. Date brute: `output/fusion_gemma4-12b-4bit_fitcmp.csv`.

Ce se compara: acelasi sistem, aceleasi predictii A si B, acelasi bootstrap, aceleasi randuri de test. Se schimba un singur lucru, splitul pe care se potriveste ponderea w pentru limba tinuta deoparte:

- **potrivire pe trial**, protocolul de pana acum: w maximizeaza r mediu peste cele 30 de instante de trial ale fiecareia dintre celelalte 9 limbi;
- **potrivire pe test**: acelasi argmax, dar peste randurile de TEST ale acelorasi 9 limbi.

Motivul pentru care a doua varianta nu e o largire a protocolului, ci o reparatie a lui: bratul A foloseste DEJA etichetele de test ale celorlalte 9 limbi, la `finetune_xlmr.py:446`, `Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` peste randurile de test. Ponderea se potrivea insa pe trial-ul acelorasi limbi. Doua componente ale aceluiasi sistem foloseau splituri diferite. In plus, `e_split_gap.md` masoara ca trial-ul supraestimeaza semnalul B cu 0.191, deci w acorda sistematic prea putin lui A.

Intervalele sunt bootstrap pe contexte, 2000 de reesantionari. Coloana de diferenta e **PERECHE**: aceeasi reesantionare pe ambele potriviri, deci intervalul e al diferentei, nu al sumei incertitudinilor.

## Cele doua potriviri, per limba

| limba | model B | n | ctx | r A | r B | w trial | r fuziune, fit trial | CI 95% | w test | r fuziune, fit test | CI 95% | test − trial | CI 95% pereche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | +0.4281 | +0.4829 | 0.20 | +0.5121 | [+0.4448, +0.5748] | 0.30 | **+0.5208** | [+0.4537, +0.5808] | +0.0087 | [-0.0005, +0.0178] |
| de | `gemma4-12b-4bit` | 570 | 193 | +0.6314 | +0.6544 | 0.15 | +0.6861 | [+0.6438, +0.7259] | 0.30 | **+0.7084** | [+0.6683, +0.7460] | +0.0223 | [+0.0136, +0.0306] |
| en | `gemma4-12b-4bit` | 570 | 190 | +0.8197 | +0.8377 | 0.15 | +0.8556 | [+0.8240, +0.8834] | 0.30 | **+0.8670** | [+0.8383, +0.8923] | +0.0114 | [+0.0066, +0.0168] |
| es | `gemma4-12b-4bit` | 593 | 208 | +0.6341 | +0.7432 | 0.15 | +0.7481 | [+0.7099, +0.7839] | 0.30 | **+0.7457** | [+0.7080, +0.7816] | -0.0024 | [-0.0081, +0.0036] |
| fil | `gemma4-12b-4bit` | 568 | 553 | +0.4047 | +0.5190 | 0.10 | +0.5228 | [+0.4576, +0.5847] | 0.30 | **+0.5210** | [+0.4564, +0.5826] | -0.0018 | [-0.0137, +0.0108] |
| fr | `gemma4-12b-4bit` | 566 | 191 | +0.5153 | +0.6457 | 0.20 | +0.6510 | [+0.5958, +0.7008] | 0.30 | **+0.6478** | [+0.5931, +0.6973] | -0.0031 | [-0.0086, +0.0023] |
| it | `gemma4-12b-4bit` | 562 | 192 | +0.6136 | +0.6106 | 0.15 | +0.6299 | [+0.5836, +0.6766] | 0.30 | **+0.6436** | [+0.5976, +0.6903] | +0.0137 | [+0.0066, +0.0210] |
| ja | `gemma4-12b-4bit` | 570 | 190 | +0.4880 | +0.7676 | 0.20 | +0.7853 | [+0.7431, +0.8199] | 0.35 | **+0.7754** | [+0.7315, +0.8110] | -0.0099 | [-0.0190, -0.0011] |
| pt | `gemma4-12b-4bit` | 562 | 557 | +0.7663 | +0.8222 | 0.15 | +0.8330 | [+0.7990, +0.8613] | 0.30 | **+0.8375** | [+0.8038, +0.8648] | +0.0045 | [-0.0003, +0.0094] |
| si | `gemma4-12b-4bit` | 600 | 578 | +0.2216 | +0.3407 | 0.20 | +0.3495 | [+0.2982, +0.4012] | 0.30 | **+0.3483** | [+0.2972, +0.4004] | -0.0012 | [-0.0089, +0.0068] |
| **medie** | | | | +0.5523 | +0.6424 | 0.16 | +0.6573 | | 0.30 | **+0.6616** | | +0.0042 | |

Potrivirea pe test urca fuziunea pe 5 din 10 limbi si o scade pe 5. Intervalul pereche exclude zero in sus pe 3 limbi si in jos pe 1. Pe medie, **+0.0042**.

## Fata de semnalele singure si de reperele publicate

| sistem | r mediu |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `gemma4-12b-4bit` | 0.6424 |
| fuziunea, w potrivit pe trial | 0.6573 |
| **fuziunea, w potrivit pe test** | **0.6616** |

Fata de cel mai bun reper publicat, 0.6571: potrivirea pe trial **+0.0002**, potrivirea pe test **+0.0045**.

## Fuziunea fata de A singur, la fiecare potrivire

Coloana care conteaza cand fuziunea iese sub A singur: daca w e prost estimat, amestecul strica un semnal bun.

| limba | fit trial − A | CI 95% | fit test − A | CI 95% |
|---|---|---|---|---|
| ca | +0.0840 | [+0.0139, +0.1556] | +0.0927 | [+0.0306, +0.1560] |
| de | +0.0547 | [+0.0097, +0.1027] | +0.0770 | [+0.0397, +0.1167] |
| en | +0.0359 | [+0.0095, +0.0640] | +0.0473 | [+0.0249, +0.0714] |
| es | +0.1140 | [+0.0775, +0.1515] | +0.1116 | [+0.0805, +0.1444] |
| fil | +0.1181 | [+0.0626, +0.1720] | +0.1163 | [+0.0720, +0.1605] |
| fr | +0.1356 | [+0.0901, +0.1837] | +0.1325 | [+0.0919, +0.1761] |
| it | +0.0163 | [-0.0234, +0.0558] | +0.0300 | [-0.0029, +0.0637] |
| ja | +0.2973 | [+0.2420, +0.3562] | +0.2874 | [+0.2397, +0.3405] |
| pt | +0.0668 | [+0.0393, +0.0940] | +0.0712 | [+0.0480, +0.0949] |
| si | +0.1278 | [+0.0683, +0.1874] | +0.1267 | [+0.0751, +0.1779] |
| **medie** | +0.1050 | | +0.1093 | |

## Setul de potrivire si forma curbei

`limbi` si `itemi` spun pe ce s-a potrivit efectiv w. `latime` e r maxim minus r minim pe grila de 21 de puncte, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot.

| limba | limbi fit | itemi trial | itemi test | latime curba trial | latime curba test |
|---|---|---|---|---|---|
| ca | 9 | 260 | 5161 | 0.1524 | 0.1118 |
| de | 9 | 267 | 5036 | 0.1935 | 0.1135 |
| en | 9 | 260 | 5036 | 0.2021 | 0.1168 |
| es | 9 | 262 | 5013 | 0.2099 | 0.1097 |
| fil | 9 | 260 | 5038 | 0.1960 | 0.1091 |
| fr | 9 | 260 | 5040 | 0.1742 | 0.1074 |
| it | 9 | 261 | 5044 | 0.1957 | 0.1187 |
| ja | 9 | 260 | 5036 | 0.1560 | 0.0896 |
| pt | 9 | 260 | 5044 | 0.1964 | 0.1142 |
| si | 9 | 260 | 5006 | 0.1857 | 0.1080 |
| **total** | | 2610 | 50454 | | |

## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie

| ce se alege | unde | cum |
|---|---|---|
| semnalul A | `finetune_xlmr.py:444-446` | `te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. |
| tot A, pe trial | `finetune_xlmr.py:449-450` | trial-ul lui L intra doar in `Xpred`, niciodata in `Xtr`. |
| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_trial, set(exclude) \| {lg})`: limba pentru care se alege intra chiar ea in multimea exclusa. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_weight` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Fara asta w(L) ar vedea limba L prin modelul ales pentru L'. |
| ponderea w | `fuse_ab.py`, `fit_weight` | `others = [d for l2, d in fit.items() if l2 != lg]`. Curba nu contine niciun rand al lui L, pe niciun split. |
| standardizarea | `fuse_ab.py`, `zscore` | media si deviatia se iau din predictii, nu din etichete. |

Si unde **nu** e garantata, fiindca trebuie scris tot: `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Ponderea lui L depinde deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi.

Dependenta asta e **identica la potrivirea pe trial si la cea pe test**, fiindca ambele folosesc aceleasi predictii A din `output/e1_frozen_preds.csv`. Trecerea la potrivirea pe test nu adauga nimic si nu inrautateste nimic. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L, si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare.
