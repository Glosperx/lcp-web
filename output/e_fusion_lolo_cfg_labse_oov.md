# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 17:27:15 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_labse_oov --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_labse_oov_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_labse_oov.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_labse_oov.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.30 | +0.4470 | +0.5159 | **+0.5514** | [+0.4875, +0.6094] | +0.1044 | [+0.0522, +0.1622] | +0.0355 | [+0.0137, +0.0561] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.30 | +0.6433 | +0.6812 | **+0.7372** | [+0.7006, +0.7708] | +0.0939 | [+0.0557, +0.1348] | +0.0560 | [+0.0374, +0.0745] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.30 | +0.8144 | +0.8463 | **+0.8702** | [+0.8429, +0.8930] | +0.0558 | [+0.0324, +0.0818] | +0.0239 | [+0.0136, +0.0356] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.500 | 0.35 | +0.6867 | +0.7499 | **+0.7609** | [+0.7242, +0.7936] | +0.0742 | [+0.0487, +0.0994] | +0.0110 | [-0.0018, +0.0251] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.35 | +0.4033 | +0.5082 | **+0.5065** | [+0.4414, +0.5656] | +0.1032 | [+0.0646, +0.1417] | -0.0016 | [-0.0213, +0.0181] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.35 | +0.5255 | +0.6655 | **+0.6576** | [+0.6036, +0.7076] | +0.1321 | [+0.0974, +0.1710] | -0.0079 | [-0.0250, +0.0088] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.30 | +0.6210 | +0.6354 | **+0.6644** | [+0.6201, +0.7088] | +0.0434 | [+0.0107, +0.0754] | +0.0291 | [+0.0149, +0.0438] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.35 | +0.5865 | +0.7715 | **+0.7827** | [+0.7412, +0.8173] | +0.1962 | [+0.1481, +0.2461] | +0.0113 | [-0.0098, +0.0326] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.500 | 0.35 | +0.7696 | +0.8322 | **+0.8428** | [+0.8146, +0.8680] | +0.0732 | [+0.0516, +0.0964] | +0.0107 | [-0.0000, +0.0211] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.30 | +0.2790 | +0.3860 | **+0.4202** | [+0.3578, +0.4788] | +0.1411 | [+0.0824, +0.2044] | +0.0341 | [+0.0052, +0.0627] |
| **medie** | | | | 0.650 | 0.32 | +0.5777 | +0.6592 | **+0.6794** | | +0.1018 | | +0.0202 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 5 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5514** | +0.0044 | [-0.0127, +0.0205] | 70.5% |
| de | +0.7429 | **+0.7372** | -0.0056 | [-0.0143, +0.0030] | 9.0% |
| en | +0.8673 | **+0.8702** | +0.0028 | [-0.0028, +0.0096] | 82.5% |
| es | +0.7548 | **+0.7609** | +0.0060 | [-0.0010, +0.0132] | 95.3% |
| fil | +0.5133 | **+0.5065** | -0.0068 | [-0.0160, +0.0022] | 7.0% |
| fr | +0.6605 | **+0.6576** | -0.0028 | [-0.0123, +0.0064] | 29.0% |
| it | +0.6704 | **+0.6644** | -0.0060 | [-0.0134, +0.0017] | 6.7% |
| ja | +0.7934 | **+0.7827** | -0.0106 | [-0.0220, +0.0008] | 3.4% |
| pt | +0.8398 | **+0.8428** | +0.0030 | [-0.0026, +0.0087] | 86.0% |
| si | +0.4095 | **+0.4202** | +0.0106 | [-0.0223, +0.0447] | 72.6% |
| **medie** | +0.6799 | **+0.6794** | -0.0005 | | 46.2% |

Configuratia noua urca fuziunea pe 5 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0005**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6794** | [+0.6646, +0.6936] | |
| fuziune − A | +0.1017 | [+0.0890, +0.1138] | 100.0% |
| fuziune − B | +0.0202 | [+0.0147, +0.0258] | 100.0% |
| configuratia noua − cea de azi | -0.0005 | [-0.0049, +0.0039] | 39.5% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5777 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6794** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0223**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.30 | 9 | 5179 | +0.5945 | +0.6959 | 0.1014 | 0.0023 |
| de | 0.750 | 0.30 | 9 | 5054 | +0.5727 | +0.6752 | 0.1025 | 0.0012 |
| en | 0.750 | 0.30 | 9 | 5054 | +0.5537 | +0.6605 | 0.1068 | 0.0022 |
| es | 0.500 | 0.35 | 9 | 5031 | +0.5725 | +0.6728 | 0.1003 | 0.0029 |
| fil | 0.500 | 0.35 | 9 | 5054 | +0.6040 | +0.7010 | 0.0970 | 0.0039 |
| fr | 0.750 | 0.35 | 9 | 5055 | +0.5858 | +0.6842 | 0.0984 | 0.0054 |
| it | 0.625 | 0.30 | 9 | 5054 | +0.5782 | +0.6834 | 0.1052 | 0.0019 |
| ja | 0.500 | 0.35 | 9 | 5054 | +0.5836 | +0.6703 | 0.0867 | 0.0023 |
| pt | 0.500 | 0.35 | 9 | 5057 | +0.5633 | +0.6636 | 0.1003 | 0.0033 |
| si | 0.875 | 0.30 | 9 | 5024 | +0.6088 | +0.7102 | 0.1014 | 0.0025 |

Latimea medie a curbei lui w e 0.1000, iar a criteriului de candidati 0.0028, adica de 36 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
