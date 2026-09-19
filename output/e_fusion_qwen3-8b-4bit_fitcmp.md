# Ponderea potrivita pe trial fata de potrivita pe test, brat `qwen3-8b-4bit`

Generat 2026-08-18 00:59:39 de `fuse_ab.py --arm qwen3-8b-4bit --fit both`. Date brute: `output/fusion_qwen3-8b-4bit_fitcmp.csv`.

Ce se compara: acelasi sistem, aceleasi predictii A si B, acelasi bootstrap, aceleasi randuri de test. Se schimba un singur lucru, splitul pe care se potriveste ponderea w pentru limba tinuta deoparte:

- **potrivire pe trial**, protocolul de pana acum: w maximizeaza r mediu peste cele 30 de instante de trial ale fiecareia dintre celelalte 9 limbi;
- **potrivire pe test**: acelasi argmax, dar peste randurile de TEST ale acelorasi 9 limbi.

Motivul pentru care a doua varianta nu e o largire a protocolului, ci o reparatie a lui: bratul A foloseste DEJA etichetele de test ale celorlalte 9 limbi, la `finetune_xlmr.py:446`, `Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` peste randurile de test. Ponderea se potrivea insa pe trial-ul acelorasi limbi. Doua componente ale aceluiasi sistem foloseau splituri diferite. In plus, `e_split_gap.md` masoara ca trial-ul supraestimeaza semnalul B cu 0.191, deci w acorda sistematic prea putin lui A.

Intervalele sunt bootstrap pe contexte, 2000 de reesantionari. Coloana de diferenta e **PERECHE**: aceeasi reesantionare pe ambele potriviri, deci intervalul e al diferentei, nu al sumei incertitudinilor.

## Cele doua potriviri, per limba

| limba | model B | n | ctx | r A | r B | w trial | r fuziune, fit trial | CI 95% | w test | r fuziune, fit test | CI 95% | test − trial | CI 95% pereche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `qwen3-8b-4bit` | 445 | 150 | +0.4281 | +0.2543 | 0.45 | +0.3927 | [+0.3129, +0.4680] | 0.75 | **+0.4339** | [+0.3510, +0.5103] | +0.0413 | [+0.0111, +0.0710] |
| de | `qwen3-8b-4bit` | 570 | 193 | +0.6314 | +0.3420 | 0.45 | +0.5532 | [+0.4921, +0.6100] | 0.70 | **+0.6207** | [+0.5639, +0.6723] | +0.0675 | [+0.0468, +0.0874] |
| en | `qwen3-8b-4bit` | 570 | 190 | +0.8197 | +0.3882 | 0.45 | +0.7039 | [+0.6592, +0.7477] | 0.70 | **+0.8066** | [+0.7723, +0.8357] | +0.1027 | [+0.0759, +0.1247] |
| es | `qwen3-8b-4bit` | 593 | 208 | +0.6341 | +0.3799 | 0.40 | +0.5604 | [+0.5100, +0.6131] | 0.75 | **+0.6396** | [+0.5924, +0.6823] | +0.0792 | [+0.0491, +0.1092] |
| fil | `qwen3-8b-4bit` | 568 | 553 | +0.4047 | +0.4910 | 0.40 | +0.5350 | [+0.4623, +0.6019] | 0.80 | **+0.4664** | [+0.3955, +0.5333] | -0.0686 | [-0.1058, -0.0272] |
| fr | `qwen3-8b-4bit` | 566 | 191 | +0.5153 | +0.4011 | 0.45 | +0.5141 | [+0.4538, +0.5693] | 0.75 | **+0.5345** | [+0.4732, +0.5896] | +0.0204 | [-0.0056, +0.0453] |
| it | `qwen3-8b-4bit` | 562 | 192 | +0.6136 | +0.3997 | 0.40 | +0.5733 | [+0.5132, +0.6281] | 0.75 | **+0.6349** | [+0.5803, +0.6884] | +0.0615 | [+0.0265, +0.0976] |
| ja | `qwen3-8b-4bit` | 570 | 190 | +0.4880 | +0.4553 | 0.45 | +0.5914 | [+0.5248, +0.6454] | 0.80 | **+0.5516** | [+0.4866, +0.6104] | -0.0398 | [-0.0835, +0.0028] |
| pt | `qwen3-8b-4bit` | 562 | 557 | +0.7663 | +0.4878 | 0.40 | +0.6734 | [+0.6284, +0.7158] | 0.70 | **+0.7550** | [+0.7167, +0.7891] | +0.0816 | [+0.0599, +0.1027] |
| si | `qwen3-8b-4bit` | 600 | 578 | +0.2216 | +0.1405 | 0.50 | +0.2222 | [+0.1531, +0.2899] | 0.75 | **+0.2328** | [+0.1672, +0.3005] | +0.0106 | [-0.0143, +0.0367] |
| **medie** | | | | +0.5523 | +0.3740 | 0.43 | +0.5320 | | 0.74 | **+0.5676** | | +0.0356 | |

Potrivirea pe test urca fuziunea pe 8 din 10 limbi si o scade pe 2. Intervalul pereche exclude zero in sus pe 6 limbi si in jos pe 1. Pe medie, **+0.0356**.

## Fata de semnalele singure si de reperele publicate

| sistem | r mediu |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `qwen3-8b-4bit` | 0.3740 |
| fuziunea, w potrivit pe trial | 0.5320 |
| **fuziunea, w potrivit pe test** | **0.5676** |

Fata de cel mai bun reper publicat, 0.6571: potrivirea pe trial **-0.1251**, potrivirea pe test **-0.0895**.

## Fuziunea fata de A singur, la fiecare potrivire

Coloana care conteaza cand fuziunea iese sub A singur: daca w e prost estimat, amestecul strica un semnal bun.

| limba | fit trial − A | CI 95% | fit test − A | CI 95% |
|---|---|---|---|---|
| ca | -0.0354 | [-0.0854, +0.0143] | +0.0058 | [-0.0159, +0.0269] |
| de | -0.0782 | [-0.1161, -0.0375] | -0.0107 | [-0.0290, +0.0089] |
| en | -0.1158 | [-0.1534, -0.0732] | -0.0131 | [-0.0298, +0.0039] |
| es | -0.0737 | [-0.1186, -0.0305] | +0.0055 | [-0.0096, +0.0202] |
| fil | +0.1303 | [+0.0664, +0.1883] | +0.0616 | [+0.0380, +0.0881] |
| fr | -0.0012 | [-0.0420, +0.0425] | +0.0192 | [+0.0027, +0.0367] |
| it | -0.0403 | [-0.0964, +0.0123] | +0.0213 | [+0.0002, +0.0414] |
| ja | +0.1034 | [+0.0468, +0.1625] | +0.0636 | [+0.0462, +0.0822] |
| pt | -0.0928 | [-0.1287, -0.0561] | -0.0112 | [-0.0271, +0.0050] |
| si | +0.0006 | [-0.0447, +0.0458] | +0.0112 | [-0.0091, +0.0311] |
| **medie** | -0.0203 | | +0.0153 | |

## Setul de potrivire si forma curbei

`limbi` si `itemi` spun pe ce s-a potrivit efectiv w. `latime` e r maxim minus r minim pe grila de 21 de puncte, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot.

| limba | limbi fit | itemi trial | itemi test | latime curba trial | latime curba test |
|---|---|---|---|---|---|
| ca | 9 | 260 | 5161 | 0.1284 | 0.2007 |
| de | 9 | 267 | 5036 | 0.1393 | 0.1891 |
| en | 9 | 260 | 5036 | 0.1349 | 0.1736 |
| es | 9 | 262 | 5013 | 0.1557 | 0.1918 |
| fil | 9 | 260 | 5038 | 0.1385 | 0.2219 |
| fr | 9 | 260 | 5040 | 0.1240 | 0.2058 |
| it | 9 | 261 | 5044 | 0.1440 | 0.1946 |
| ja | 9 | 260 | 5036 | 0.1163 | 0.2086 |
| pt | 9 | 260 | 5044 | 0.1523 | 0.1904 |
| si | 9 | 260 | 5006 | 0.1163 | 0.2104 |
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
