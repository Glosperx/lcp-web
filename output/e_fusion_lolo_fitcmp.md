# Ponderea potrivita pe trial fata de potrivita pe test, brat `lolo`

Generat 2026-08-18 01:00:01 de `fuse_ab.py --arm lolo --fit both`. Date brute: `output/fusion_lolo_fitcmp.csv`.

Ce se compara: acelasi sistem, aceleasi predictii A si B, acelasi bootstrap, aceleasi randuri de test. Se schimba un singur lucru, splitul pe care se potriveste ponderea w pentru limba tinuta deoparte:

- **potrivire pe trial**, protocolul de pana acum: w maximizeaza r mediu peste cele 30 de instante de trial ale fiecareia dintre celelalte 9 limbi;
- **potrivire pe test**: acelasi argmax, dar peste randurile de TEST ale acelorasi 9 limbi.

Motivul pentru care a doua varianta nu e o largire a protocolului, ci o reparatie a lui: bratul A foloseste DEJA etichetele de test ale celorlalte 9 limbi, la `finetune_xlmr.py:446`, `Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` peste randurile de test. Ponderea se potrivea insa pe trial-ul acelorasi limbi. Doua componente ale aceluiasi sistem foloseau splituri diferite. In plus, `e_split_gap.md` masoara ca trial-ul supraestimeaza semnalul B cu 0.191, deci w acorda sistematic prea putin lui A.

Intervalele sunt bootstrap pe contexte, 2000 de reesantionari. Coloana de diferenta e **PERECHE**: aceeasi reesantionare pe ambele potriviri, deci intervalul e al diferentei, nu al sumei incertitudinilor.

## Cele doua potriviri, per limba

| limba | model B | n | ctx | r A | r B | w trial | r fuziune, fit trial | CI 95% | w test | r fuziune, fit test | CI 95% | test − trial | CI 95% pereche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | +0.4281 | +0.4829 | 0.25 | +0.5171 | [+0.4495, +0.5785] | 0.30 | **+0.5208** | [+0.4537, +0.5808] | +0.0037 | [-0.0009, +0.0083] |
| de | `gemma4-12b-4bit` | 570 | 193 | +0.6314 | +0.6544 | 0.20 | +0.6948 | [+0.6533, +0.7342] | 0.30 | **+0.7084** | [+0.6683, +0.7460] | +0.0136 | [+0.0078, +0.0192] |
| en | `gemma4-12b-4bit` | 570 | 190 | +0.8197 | +0.8377 | 0.20 | +0.8602 | [+0.8296, +0.8871] | 0.30 | **+0.8670** | [+0.8383, +0.8923] | +0.0068 | [+0.0036, +0.0104] |
| es | `gemma4-12b-4bit` | 593 | 208 | +0.6341 | +0.7432 | 0.20 | +0.7482 | [+0.7100, +0.7838] | 0.35 | **+0.7432** | [+0.7050, +0.7793] | -0.0050 | [-0.0109, +0.0011] |
| fil | `gemma4-12b-4bit` | 568 | 553 | +0.4047 | +0.5190 | 0.10 | +0.5228 | [+0.4576, +0.5847] | 0.30 | **+0.5210** | [+0.4564, +0.5826] | -0.0018 | [-0.0137, +0.0108] |
| fr | `qwen35-9b-8bit` | 566 | 191 | +0.5153 | +0.5440 | 0.25 | +0.5715 | [+0.5169, +0.6270] | 0.30 | **+0.5745** | [+0.5188, +0.6296] | +0.0031 | [-0.0003, +0.0065] |
| it | `gemma4-12b-4bit` | 562 | 192 | +0.6136 | +0.6106 | 0.25 | +0.6398 | [+0.5939, +0.6865] | 0.30 | **+0.6436** | [+0.5976, +0.6903] | +0.0038 | [+0.0014, +0.0063] |
| ja | `gemma4-12b-4bit` | 570 | 190 | +0.4880 | +0.7676 | 0.30 | +0.7814 | [+0.7387, +0.8161] | 0.35 | **+0.7754** | [+0.7315, +0.8110] | -0.0060 | [-0.0092, -0.0030] |
| pt | `gemma4-12b-4bit` | 562 | 557 | +0.7663 | +0.8222 | 0.25 | +0.8367 | [+0.8031, +0.8641] | 0.35 | **+0.8374** | [+0.8038, +0.8648] | +0.0007 | [-0.0025, +0.0039] |
| si | `gemma4-12b-4bit` | 600 | 578 | +0.2216 | +0.3407 | 0.20 | +0.3495 | [+0.2982, +0.4012] | 0.30 | **+0.3483** | [+0.2972, +0.4004] | -0.0012 | [-0.0089, +0.0068] |
| **medie** | | | | +0.5523 | +0.6322 | 0.22 | +0.6522 | | 0.32 | **+0.6540** | | +0.0018 | |

Potrivirea pe test urca fuziunea pe 6 din 10 limbi si o scade pe 4. Intervalul pereche exclude zero in sus pe 3 limbi si in jos pe 1. Pe medie, **+0.0018**.

## Fata de semnalele singure si de reperele publicate

| sistem | r mediu |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5523 |
| semnalul B singur, `lolo` | 0.6322 |
| fuziunea, w potrivit pe trial | 0.6522 |
| **fuziunea, w potrivit pe test** | **0.6540** |

Fata de cel mai bun reper publicat, 0.6571: potrivirea pe trial **-0.0049**, potrivirea pe test **-0.0031**.

## Fuziunea fata de A singur, la fiecare potrivire

Coloana care conteaza cand fuziunea iese sub A singur: daca w e prost estimat, amestecul strica un semnal bun.

| limba | fit trial − A | CI 95% | fit test − A | CI 95% |
|---|---|---|---|---|
| ca | +0.0890 | [+0.0234, +0.1562] | +0.0927 | [+0.0306, +0.1560] |
| de | +0.0634 | [+0.0207, +0.1090] | +0.0770 | [+0.0397, +0.1167] |
| en | +0.0405 | [+0.0155, +0.0672] | +0.0473 | [+0.0249, +0.0714] |
| es | +0.1141 | [+0.0794, +0.1502] | +0.1091 | [+0.0798, +0.1397] |
| fil | +0.1181 | [+0.0626, +0.1720] | +0.1163 | [+0.0720, +0.1605] |
| fr | +0.0561 | [+0.0078, +0.1055] | +0.0592 | [+0.0143, +0.1057] |
| it | +0.0262 | [-0.0087, +0.0620] | +0.0300 | [-0.0029, +0.0637] |
| ja | +0.2935 | [+0.2429, +0.3487] | +0.2874 | [+0.2397, +0.3405] |
| pt | +0.0705 | [+0.0457, +0.0954] | +0.0711 | [+0.0495, +0.0932] |
| si | +0.1278 | [+0.0683, +0.1874] | +0.1267 | [+0.0751, +0.1779] |
| **medie** | +0.0999 | | +0.1017 | |

## Setul de potrivire si forma curbei

`limbi` si `itemi` spun pe ce s-a potrivit efectiv w. `latime` e r maxim minus r minim pe grila de 21 de puncte, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot.

| limba | limbi fit | itemi trial | itemi test | latime curba trial | latime curba test |
|---|---|---|---|---|---|
| ca | 9 | 260 | 5161 | 0.1263 | 0.1036 |
| de | 9 | 267 | 5036 | 0.1655 | 0.1054 |
| en | 9 | 260 | 5036 | 0.1744 | 0.1087 |
| es | 9 | 262 | 5013 | 0.1817 | 0.1019 |
| fil | 9 | 260 | 5038 | 0.1960 | 0.1091 |
| fr | 9 | 260 | 5040 | 0.1412 | 0.1074 |
| it | 9 | 261 | 5044 | 0.1689 | 0.1106 |
| ja | 9 | 260 | 5036 | 0.1307 | 0.0821 |
| pt | 9 | 260 | 5044 | 0.1693 | 0.1061 |
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

### Filtrul de disponibilitate

Selectia imbricata poate cere un model care nu a fost rulat pe limba de potrivire, pe splitul de potrivire. Candidatii se restrang atunci la modelele masurate efectiv acolo. Restrangerea se uita la ACOPERIRE, nu la scor, deci nu introduce nicio eticheta. Cazurile, toate:

| split de potrivire | limba tinuta deoparte | limba de potrivire | cerut | folosit |
|---|---|---|---|---|
| test | fr | ca | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | de | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | en | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | es | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | it | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | ja | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | pt | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
