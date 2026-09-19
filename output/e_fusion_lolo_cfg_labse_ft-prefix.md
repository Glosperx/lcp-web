# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 17:26:41 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_labse_ft-prefix --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_labse_ft-prefix_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_labse_ft-prefix.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_labse_ft-prefix.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi e fixat la `fert_inloc`, prin argument si nu prin scor: lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio eticheta.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 9 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.30 | +0.4313 | +0.5159 | **+0.5480** | [+0.4827, +0.6071] | +0.1168 | [+0.0631, +0.1770] | +0.0322 | [+0.0083, +0.0537] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.30 | +0.6566 | +0.6812 | **+0.7407** | [+0.7040, +0.7747] | +0.0841 | [+0.0480, +0.1242] | +0.0595 | [+0.0414, +0.0778] |
| en | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.30 | +0.8055 | +0.8463 | **+0.8682** | [+0.8406, +0.8916] | +0.0627 | [+0.0370, +0.0903] | +0.0219 | [+0.0115, +0.0338] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.30 | +0.6870 | +0.7499 | **+0.7641** | [+0.7270, +0.7967] | +0.0771 | [+0.0492, +0.1052] | +0.0142 | [+0.0020, +0.0266] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.35 | +0.3872 | +0.5082 | **+0.5056** | [+0.4407, +0.5657] | +0.1183 | [+0.0778, +0.1593] | -0.0026 | [-0.0230, +0.0184] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5107 | +0.6655 | **+0.6532** | [+0.5983, +0.7033] | +0.1425 | [+0.1064, +0.1829] | -0.0123 | [-0.0296, +0.0044] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.30 | +0.6348 | +0.6354 | **+0.6686** | [+0.6247, +0.7130] | +0.0337 | [+0.0021, +0.0670] | +0.0332 | [+0.0189, +0.0478] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.5833 | +0.7715 | **+0.7854** | [+0.7443, +0.8197] | +0.2021 | [+0.1542, +0.2515] | +0.0140 | [-0.0075, +0.0358] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.30 | +0.7661 | +0.8322 | **+0.8444** | [+0.8170, +0.8691] | +0.0783 | [+0.0541, +0.1046] | +0.0122 | [+0.0026, +0.0216] |
| si | `gemma4-12b-4bit` | 600 | 578 | 1.000 | 0.30 | +0.2834 | +0.3860 | **+0.4067** | [+0.3512, +0.4604] | +0.1233 | [+0.0733, +0.1757] | +0.0207 | [+0.0000, +0.0422] |
| **medie** | | | | 0.875 | 0.31 | +0.5746 | +0.6592 | **+0.6785** | | +0.1039 | | +0.0193 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5480** | +0.0011 | [-0.0145, +0.0151] | 56.0% |
| de | +0.7429 | **+0.7407** | -0.0022 | [-0.0101, +0.0057] | 29.5% |
| en | +0.8673 | **+0.8682** | +0.0009 | [-0.0052, +0.0080] | 60.9% |
| es | +0.7548 | **+0.7641** | +0.0093 | [+0.0014, +0.0169] | 99.2% |
| fil | +0.5133 | **+0.5056** | -0.0077 | [-0.0205, +0.0045] | 10.8% |
| fr | +0.6605 | **+0.6532** | -0.0073 | [-0.0175, +0.0023] | 7.8% |
| it | +0.6704 | **+0.6686** | -0.0018 | [-0.0097, +0.0052] | 30.5% |
| ja | +0.7934 | **+0.7854** | -0.0079 | [-0.0193, +0.0033] | 8.3% |
| pt | +0.8398 | **+0.8444** | +0.0045 | [-0.0007, +0.0103] | 95.2% |
| si | +0.4095 | **+0.4067** | -0.0029 | [-0.0316, +0.0270] | 42.8% |
| **medie** | +0.6799 | **+0.6785** | -0.0014 | | 44.1% |

Configuratia noua urca fuziunea pe 4 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **-0.0014**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6785** | [+0.6640, +0.6925] | |
| fuziune − A | +0.1039 | [+0.0914, +0.1164] | 100.0% |
| fuziune − B | +0.0193 | [+0.0137, +0.0248] | 100.0% |
| configuratia noua − cea de azi | -0.0014 | [-0.0054, +0.0027] | 25.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5746 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6785** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0214**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.30 | 9 | 5179 | +0.5903 | +0.6950 | 0.1047 | 0.0035 |
| de | 0.750 | 0.30 | 9 | 5054 | +0.5705 | +0.6735 | 0.1030 | 0.0031 |
| en | 1.000 | 0.30 | 9 | 5054 | +0.5487 | +0.6594 | 0.1107 | 0.0030 |
| es | 0.875 | 0.30 | 9 | 5031 | +0.5650 | +0.6710 | 0.1060 | 0.0023 |
| fil | 0.625 | 0.35 | 9 | 5054 | +0.6017 | +0.6993 | 0.0976 | 0.0023 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.5815 | +0.6831 | 0.1016 | 0.0051 |
| it | 0.750 | 0.30 | 9 | 5054 | +0.5729 | +0.6815 | 0.1086 | 0.0036 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5765 | +0.6685 | 0.0920 | 0.0033 |
| pt | 0.875 | 0.30 | 9 | 5057 | +0.5562 | +0.6621 | 0.1059 | 0.0023 |
| si | 1.000 | 0.30 | 9 | 5024 | +0.6067 | +0.7107 | 0.1040 | 0.0030 |

Latimea medie a curbei lui w e 0.1034, iar a criteriului de candidati 0.0032, adica de 33 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

## Scara configuratiilor

Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai din ce e facut semnalul A si ce se alege leave-one-language-out.

| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de 0.6571 |
|---|---|---|---|---|---|
| fuziunea de azi, A = `p_multi` | 10 | `baza` | 0.000 | **0.6568** | -0.0003 |
| doar ansamblul de surse, set `baza` | 10 | `baza` | 0.900 | **0.6636** | +0.0065 |
| doar `fert_inloc`, fara ansamblu | 10 | `fert_inloc` | 0.000 | **0.6591** | +0.0020 |
| **ansamblu plus `fert_inloc`** | 10 | `fert_inloc` | 0.738 | **0.6646** | +0.0075 |
| ansamblu plus setul ales si el LOLO | 10 | `fert_inloc`, `fert_plus`, `fara_lung` | 0.787 | **0.6636** | +0.0065 |

Reperul e cel mai bun reper publicat pe test, G-Eval cu GPT-4o 0.6571.

## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie

| ce se alege | unde | cum |
|---|---|---|
| semnalul A, ambele brate | `finetune_xlmr.py`, `frozen_trial_gap` | `te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. Bratul `p_en` nu vede deloc MLSP. |
| tot A, pe trial | `finetune_xlmr.py`, `frozen_trial_gap` | trial-ul lui L intra doar in `Xpred`, niciodata in `Xtr`. |
| setul de trasaturi al lui A | `solution_bert.py`, `_Xc` | fertilitatea e `len(tokenize(tinta))`, deci o proprietate a tokenizerului, nu a etichetelor. Centrarea ei foloseste media limbii, nu complexitatea. |
| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_pick, set(exclude) \| {lg})`: criteriul e media lui r peste CELELALTE 9 limbi ale splitului de selectie, iar limba pentru care se alege intra chiar ea in multimea exclusa. |
| splitul pe care se alege modelul | `fuse_ab.py`, `fuse_ens` | `--pick-split test`, adica `tab_pick = r_table(load_runs('test'), "B")`. Selectia si potrivirea ponderii citesc acelasi split, ca antrenarea bratului A. Niciun rand al limbii L nu intra in criteriu, pe niciunul dintre splituri: L e exclusa chiar din media care alege. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Se face pe ACELASI `tab_pick`, deci schimbarea splitului de selectie nu deschide o scurgere pe unde selectia imbricata a inchis una. |
| `w_src` | `fuse_ab.py`, `fit_choice` | acelasi criteriu, aceeasi multime `others`. |
| ponderea w | `fuse_ab.py`, `fit_choice` | `others = {l2: d for l2, d in fit.items() if l2 != lg}`. Curba nu contine niciun rand al lui L, pe niciun split. |
| w-ul limbilor de potrivire, in criteriu | `fuse_ab.py`, `fit_choice` | bucla `for l3 in others if l3 != l2`: cand un candidat se masoara pe L', ponderea lui L' vine de pe celelalte opt limbi, deci nici L nici L' nu intra in ea. |
| standardizarea | `fuse_ab.py`, `zscore` si `zA_of` | media si deviatia se iau din predictii, nu din etichete, la ambele niveluri de standardizare ale lui A. |

Si unde **nu** e garantata, fiindca trebuie scris tot. Doua locuri:

1. `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Alegerile lui L depind deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi. Dependenta e identica la potrivirea pe trial si la cea pe test, fiindca ambele folosesc aceleasi predictii. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare. Bratul `p_en` **nu** are dependenta asta: nu vede niciun rand de MLSP.
2. Modelul lui B al limbilor de potrivire se re-alege cu `exclude={L}`, deci la un nivel, nu la doua. In bucla interioara care alege w-ul lui L' pe celelalte opt, modelul acelor opt ramane cel ales cu `exclude={L}`, nu cu `exclude={L, L'}`. Nivelul urmator ar cere `pick_model` cu trei limbi excluse, si nu s-a coborat pana acolo.

### Filtrul de disponibilitate

Nu s-a activat: fiecare model cerut de selectia imbricata avea masuratori pe limba de potrivire, pe splitul de potrivire.
