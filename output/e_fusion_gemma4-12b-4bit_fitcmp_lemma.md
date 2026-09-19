# Ponderea potrivita pe trial fata de potrivita pe test, brat `gemma4-12b-4bit`

Generat 2026-08-18 10:24:53 de `fuse_ab.py --arm gemma4-12b-4bit --fit both`. Date brute: `output/fusion_gemma4-12b-4bit_fitcmp.csv`.

Ce se compara: acelasi sistem, aceleasi predictii A si B, acelasi bootstrap, aceleasi randuri de test. Se schimba un singur lucru, splitul pe care se potriveste ponderea w pentru limba tinuta deoparte:

- **potrivire pe trial**, protocolul de pana acum: w maximizeaza r mediu peste cele 30 de instante de trial ale fiecareia dintre celelalte 9 limbi;
- **potrivire pe test**: acelasi argmax, dar peste randurile de TEST ale acelorasi 9 limbi.

Motivul pentru care a doua varianta nu e o largire a protocolului, ci o reparatie a lui: bratul A foloseste DEJA etichetele de test ale celorlalte 9 limbi, la `finetune_xlmr.py:446`, `Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` peste randurile de test. Ponderea se potrivea insa pe trial-ul acelorasi limbi. Doua componente ale aceluiasi sistem foloseau splituri diferite. In plus, `e_split_gap.md` masoara ca trial-ul supraestimeaza semnalul B cu 0.191, deci w acorda sistematic prea putin lui A.

Intervalele sunt bootstrap pe contexte, 2000 de reesantionari. Coloana de diferenta e **PERECHE**: aceeasi reesantionare pe ambele potriviri, deci intervalul e al diferentei, nu al sumei incertitudinilor.

## Cele doua potriviri, per limba

| limba | model B | n | ctx | r A | r B | w trial | r fuziune, fit trial | CI 95% | w test | r fuziune, fit test | CI 95% | test − trial | CI 95% pereche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | +0.4470 | +0.4829 | 0.20 | +0.5161 | [+0.4498, +0.5788] | 0.30 | **+0.5270** | [+0.4624, +0.5857] | +0.0109 | [+0.0019, +0.0197] |
| de | `gemma4-12b-4bit` | 570 | 193 | +0.6551 | +0.6544 | 0.15 | +0.6898 | [+0.6479, +0.7292] | 0.30 | **+0.7160** | [+0.6767, +0.7539] | +0.0262 | [+0.0180, +0.0345] |
| en | `gemma4-12b-4bit` | 570 | 190 | +0.8147 | +0.8377 | 0.15 | +0.8549 | [+0.8231, +0.8823] | 0.30 | **+0.8655** | [+0.8366, +0.8902] | +0.0106 | [+0.0056, +0.0160] |
| es | `gemma4-12b-4bit` | 593 | 208 | +0.6686 | +0.7432 | 0.15 | +0.7519 | [+0.7136, +0.7878] | 0.35 | **+0.7531** | [+0.7149, +0.7882] | +0.0012 | [-0.0061, +0.0088] |
| fil | `gemma4-12b-4bit` | 568 | 553 | +0.4091 | +0.5190 | 0.10 | +0.5228 | [+0.4571, +0.5846] | 0.35 | **+0.5186** | [+0.4531, +0.5802] | -0.0042 | [-0.0188, +0.0112] |
| fr | `gemma4-12b-4bit` | 566 | 191 | +0.5305 | +0.6457 | 0.20 | +0.6531 | [+0.5975, +0.7027] | 0.35 | **+0.6488** | [+0.5949, +0.6976] | -0.0043 | [-0.0127, +0.0039] |
| it | `gemma4-12b-4bit` | 562 | 192 | +0.6336 | +0.6106 | 0.20 | +0.6409 | [+0.5951, +0.6868] | 0.30 | **+0.6521** | [+0.6066, +0.6978] | +0.0112 | [+0.0062, +0.0164] |
| ja | `gemma4-12b-4bit` | 570 | 190 | +0.4890 | +0.7676 | 0.25 | +0.7810 | [+0.7386, +0.8164] | 0.35 | **+0.7709** | [+0.7268, +0.8069] | -0.0102 | [-0.0165, -0.0042] |
| pt | `gemma4-12b-4bit` | 562 | 557 | +0.7705 | +0.8222 | 0.20 | +0.8360 | [+0.8027, +0.8638] | 0.35 | **+0.8388** | [+0.8053, +0.8659] | +0.0028 | [-0.0022, +0.0079] |
| si | `gemma4-12b-4bit` | 600 | 578 | +0.2119 | +0.3407 | 0.20 | +0.3480 | [+0.2962, +0.3994] | 0.35 | **+0.3430** | [+0.2933, +0.3951] | -0.0050 | [-0.0171, +0.0074] |
| **medie** | | | | +0.5630 | +0.6424 | 0.18 | +0.6594 | | 0.33 | **+0.6634** | | +0.0039 | |

Potrivirea pe test urca fuziunea pe 6 din 10 limbi si o scade pe 4. Intervalul pereche exclude zero in sus pe 4 limbi si in jos pe 1. Pe medie, **+0.0039**.

## Fata de semnalele singure si de reperele publicate

| sistem | r mediu |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5630 |
| semnalul B singur, `gemma4-12b-4bit` | 0.6424 |
| fuziunea, w potrivit pe trial | 0.6594 |
| **fuziunea, w potrivit pe test** | **0.6634** |

Fata de cel mai bun reper publicat, 0.6571: potrivirea pe trial **+0.0023**, potrivirea pe test **+0.0063**.

## Fuziunea fata de A singur, la fiecare potrivire

Coloana care conteaza cand fuziunea iese sub A singur: daca w e prost estimat, amestecul strica un semnal bun.

| limba | fit trial − A | CI 95% | fit test − A | CI 95% |
|---|---|---|---|---|
| ca | +0.0691 | [+0.0016, +0.1397] | +0.0800 | [+0.0203, +0.1423] |
| de | +0.0346 | [-0.0097, +0.0810] | +0.0608 | [+0.0241, +0.1015] |
| en | +0.0402 | [+0.0126, +0.0700] | +0.0508 | [+0.0280, +0.0767] |
| es | +0.0833 | [+0.0503, +0.1172] | +0.0845 | [+0.0584, +0.1112] |
| fil | +0.1137 | [+0.0589, +0.1676] | +0.1094 | [+0.0701, +0.1494] |
| fr | +0.1226 | [+0.0790, +0.1710] | +0.1183 | [+0.0817, +0.1594] |
| it | +0.0074 | [-0.0302, +0.0450] | +0.0185 | [-0.0139, +0.0519] |
| ja | +0.2921 | [+0.2404, +0.3498] | +0.2819 | [+0.2345, +0.3347] |
| pt | +0.0656 | [+0.0375, +0.0935] | +0.0683 | [+0.0452, +0.0921] |
| si | +0.1361 | [+0.0771, +0.1963] | +0.1311 | [+0.0827, +0.1807] |
| **medie** | +0.0965 | | +0.1004 | |

## Setul de potrivire si forma curbei

`limbi` si `itemi` spun pe ce s-a potrivit efectiv w. `latime` e r maxim minus r minim pe grila de 21 de puncte, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot.

| limba | limbi fit | itemi trial | itemi test | latime curba trial | latime curba test |
|---|---|---|---|---|---|
| ca | 9 | 260 | 5161 | 0.1443 | 0.1043 |
| de | 9 | 267 | 5036 | 0.1777 | 0.1064 |
| en | 9 | 260 | 5036 | 0.1894 | 0.1076 |
| es | 9 | 262 | 5013 | 0.1966 | 0.1038 |
| fil | 9 | 260 | 5038 | 0.1816 | 0.1011 |
| fr | 9 | 260 | 5040 | 0.1598 | 0.1001 |
| it | 9 | 261 | 5044 | 0.1797 | 0.1112 |
| ja | 9 | 260 | 5036 | 0.1434 | 0.0820 |
| pt | 9 | 260 | 5044 | 0.1825 | 0.1057 |
| si | 9 | 260 | 5006 | 0.1793 | 0.0987 |
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
