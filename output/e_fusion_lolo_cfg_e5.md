# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 12:17:16 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag cfg_e5 --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_e5_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_enc_xlmr_now.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_cfg_e5.csv`, predictii per instanta in `output/fusion_preds_lolo_cfg_e5.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.30 | +0.4563 | +0.5159 | **+0.5577** | [+0.4942, +0.6138] | +0.1013 | [+0.0443, +0.1616] | +0.0418 | [+0.0174, +0.0659] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.30 | +0.6572 | +0.6812 | **+0.7351** | [+0.6965, +0.7706] | +0.0778 | [+0.0424, +0.1152] | +0.0538 | [+0.0367, +0.0709] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.30 | +0.8108 | +0.8463 | **+0.8664** | [+0.8384, +0.8906] | +0.0556 | [+0.0316, +0.0824] | +0.0201 | [+0.0110, +0.0304] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.35 | +0.7094 | +0.7499 | **+0.7668** | [+0.7303, +0.7998] | +0.0574 | [+0.0345, +0.0820] | +0.0169 | [+0.0048, +0.0290] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.35 | +0.4128 | +0.5082 | **+0.5126** | [+0.4472, +0.5712] | +0.0998 | [+0.0601, +0.1391] | +0.0044 | [-0.0162, +0.0248] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.35 | +0.5492 | +0.6655 | **+0.6661** | [+0.6130, +0.7150] | +0.1169 | [+0.0801, +0.1585] | +0.0006 | [-0.0172, +0.0172] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.30 | +0.6330 | +0.6354 | **+0.6712** | [+0.6259, +0.7151] | +0.0382 | [+0.0045, +0.0708] | +0.0358 | [+0.0210, +0.0504] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.35 | +0.5927 | +0.7715 | **+0.7848** | [+0.7424, +0.8192] | +0.1921 | [+0.1460, +0.2408] | +0.0133 | [-0.0068, +0.0344] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.35 | +0.7778 | +0.8322 | **+0.8452** | [+0.8143, +0.8722] | +0.0675 | [+0.0455, +0.0922] | +0.0131 | [+0.0009, +0.0244] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.2048 | +0.3860 | **+0.3960** | [+0.3404, +0.4499] | +0.1912 | [+0.1344, +0.2511] | +0.0100 | [-0.0216, +0.0413] |
| **medie** | | | | 0.713 | 0.33 | +0.5804 | +0.6592 | **+0.6802** | | +0.0998 | | +0.0210 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_enc_xlmr_now.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5470 | **+0.5577** | +0.0107 | [-0.0024, +0.0237] | 93.8% |
| de | +0.7429 | **+0.7351** | -0.0078 | [-0.0161, +0.0007] | 4.0% |
| en | +0.8673 | **+0.8664** | -0.0009 | [-0.0066, +0.0043] | 37.2% |
| es | +0.7548 | **+0.7668** | +0.0119 | [+0.0041, +0.0196] | 100.0% |
| fil | +0.5133 | **+0.5126** | -0.0007 | [-0.0078, +0.0063] | 42.0% |
| fr | +0.6605 | **+0.6661** | +0.0056 | [-0.0054, +0.0172] | 83.7% |
| it | +0.6704 | **+0.6712** | +0.0008 | [-0.0066, +0.0074] | 59.2% |
| ja | +0.7934 | **+0.7848** | -0.0086 | [-0.0195, +0.0021] | 5.9% |
| pt | +0.8398 | **+0.8452** | +0.0054 | [+0.0005, +0.0106] | 98.3% |
| si | +0.4095 | **+0.3960** | -0.0136 | [-0.0388, +0.0119] | 16.2% |
| **medie** | +0.6799 | **+0.6802** | +0.0003 | | 54.0% |

Configuratia noua urca fuziunea pe 5 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0003**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6802** | [+0.6658, +0.6941] | |
| fuziune − A | +0.0998 | [+0.0871, +0.1118] | 100.0% |
| fuziune − B | +0.0210 | [+0.0151, +0.0268] | 100.0% |
| configuratia noua − cea de azi | +0.0003 | [-0.0035, +0.0037] | 55.5% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5804 |
| semnalul B singur, `lolo` | 0.6592 |
| fuziunea de azi, A = `p_multi` | 0.6799 |
| **fuziunea cu ansamblul de surse** | **0.6802** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0231**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.30 | 9 | 5179 | +0.5859 | +0.6946 | 0.1087 | 0.0025 |
| de | 0.625 | 0.30 | 9 | 5054 | +0.5740 | +0.6754 | 0.1014 | 0.0022 |
| en | 0.750 | 0.30 | 9 | 5054 | +0.5547 | +0.6608 | 0.1061 | 0.0020 |
| es | 0.625 | 0.35 | 9 | 5031 | +0.5682 | +0.6720 | 0.1038 | 0.0018 |
| fil | 0.625 | 0.35 | 9 | 5054 | +0.6012 | +0.7002 | 0.0990 | 0.0027 |
| fr | 0.625 | 0.35 | 9 | 5055 | +0.5860 | +0.6832 | 0.0972 | 0.0039 |
| it | 1.000 | 0.30 | 9 | 5054 | +0.5663 | +0.6820 | 0.1157 | 0.0018 |
| ja | 0.625 | 0.35 | 9 | 5054 | +0.5812 | +0.6700 | 0.0888 | 0.0025 |
| pt | 0.625 | 0.35 | 9 | 5057 | +0.5606 | +0.6633 | 0.1027 | 0.0023 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6243 | +0.7132 | 0.0889 | 0.0034 |

Latimea medie a curbei lui w e 0.1012, iar a criteriului de candidati 0.0025, adica de 40 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
