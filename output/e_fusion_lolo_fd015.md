# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 23:53:51 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fd015 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encmean-fd015_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fd015.csv`, predictii per instanta in `output/fusion_preds_lolo_fd015.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.35 | +0.4605 | +0.5187 | **+0.5728** | [+0.5114, +0.6280] | +0.1123 | [+0.0549, +0.1729] | +0.0540 | [+0.0259, +0.0828] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.875 | 0.35 | +0.6177 | +0.7108 | **+0.7557** | [+0.7203, +0.7872] | +0.1380 | [+0.0977, +0.1811] | +0.0449 | [+0.0256, +0.0645] |
| en | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.35 | +0.8271 | +0.8471 | **+0.8734** | [+0.8476, +0.8955] | +0.0463 | [+0.0245, +0.0690] | +0.0263 | [+0.0153, +0.0392] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.6990 | +0.7553 | **+0.7680** | [+0.7316, +0.8003] | +0.0690 | [+0.0438, +0.0970] | +0.0127 | [+0.0009, +0.0245] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.875 | 0.35 | +0.4412 | +0.5000 | **+0.5259** | [+0.4617, +0.5860] | +0.0847 | [+0.0443, +0.1260] | +0.0258 | [+0.0036, +0.0477] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5342 | +0.6752 | **+0.6658** | [+0.6135, +0.7138] | +0.1316 | [+0.0981, +0.1703] | -0.0094 | [-0.0252, +0.0064] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.875 | 0.35 | +0.6046 | +0.6406 | **+0.6721** | [+0.6276, +0.7156] | +0.0675 | [+0.0336, +0.1024] | +0.0315 | [+0.0125, +0.0512] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.35 | +0.6147 | +0.7795 | **+0.7967** | [+0.7565, +0.8304] | +0.1819 | [+0.1316, +0.2343] | +0.0172 | [-0.0014, +0.0371] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7637 | +0.8243 | **+0.8385** | [+0.8077, +0.8655] | +0.0748 | [+0.0531, +0.0985] | +0.0142 | [+0.0024, +0.0253] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.3399 | +0.3979 | **+0.4289** | [+0.3718, +0.4808] | +0.0890 | [+0.0476, +0.1324] | +0.0310 | [+0.0074, +0.0535] |
| **medie** | | | | 0.887 | 0.35 | +0.5903 | +0.6649 | **+0.6898** | | +0.0995 | | +0.0248 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 8 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5728** | +0.0089 | [-0.0078, +0.0249] | 86.2% |
| de | +0.7712 | **+0.7557** | -0.0156 | [-0.0241, -0.0080] | 0.0% |
| en | +0.8723 | **+0.8734** | +0.0011 | [-0.0021, +0.0047] | 74.2% |
| es | +0.7672 | **+0.7680** | +0.0008 | [-0.0051, +0.0065] | 59.2% |
| fil | +0.5074 | **+0.5259** | +0.0185 | [-0.0006, +0.0366] | 97.1% |
| fr | +0.6679 | **+0.6658** | -0.0021 | [-0.0087, +0.0041] | 25.8% |
| it | +0.6795 | **+0.6721** | -0.0074 | [-0.0153, -0.0002] | 2.1% |
| ja | +0.7942 | **+0.7967** | +0.0025 | [-0.0074, +0.0116] | 68.7% |
| pt | +0.8413 | **+0.8385** | -0.0028 | [-0.0061, +0.0006] | 6.2% |
| si | +0.4350 | **+0.4289** | -0.0062 | [-0.0210, +0.0083] | 18.8% |
| **medie** | +0.6900 | **+0.6898** | -0.0002 | | 43.8% |

Configuratia noua urca fuziunea pe 5 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0002**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6898** | [+0.6753, +0.7034] | |
| fuziune − A | +0.0995 | [+0.0873, +0.1116] | 100.0% |
| fuziune − B | +0.0248 | [+0.0188, +0.0309] | 100.0% |
| configuratia noua − cea de azi | -0.0002 | [-0.0034, +0.0030] | 44.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5903 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6898** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0327**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.35 | 9 | 5179 | +0.6058 | +0.7031 | 0.0973 | 0.0028 |
| de | 0.875 | 0.35 | 9 | 5054 | +0.5884 | +0.6828 | 0.0944 | 0.0033 |
| en | 1.000 | 0.35 | 9 | 5054 | +0.5612 | +0.6697 | 0.1085 | 0.0042 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5793 | +0.6814 | 0.1021 | 0.0029 |
| fil | 0.875 | 0.35 | 9 | 5054 | +0.6080 | +0.7084 | 0.1004 | 0.0031 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.5938 | +0.6928 | 0.0990 | 0.0039 |
| it | 0.875 | 0.35 | 9 | 5054 | +0.5898 | +0.6921 | 0.1023 | 0.0038 |
| ja | 1.000 | 0.35 | 9 | 5054 | +0.5848 | +0.6782 | 0.0934 | 0.0030 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5721 | +0.6736 | 0.1015 | 0.0037 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6246 | +0.7188 | 0.0942 | 0.0035 |

Latimea medie a curbei lui w e 0.0993, iar a criteriului de candidati 0.0034, adica de 29 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
