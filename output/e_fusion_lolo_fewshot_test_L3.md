# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-22 15:48:25 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fewshot_test_L3 --b-dir output/bakeoff_test_L3 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_L3/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fewshot_test_L3.csv`, predictii per instanta in `output/fusion_preds_lolo_fewshot_test_L3.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.35 | +0.4504 | +0.5097 | **+0.5519** | [+0.4876, +0.6104] | +0.1016 | [+0.0500, +0.1553] | +0.0423 | [+0.0134, +0.0702] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6799 | **+0.7478** | [+0.7113, +0.7817] | +0.0694 | [+0.0381, +0.1038] | +0.0680 | [+0.0481, +0.0882] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8455 | **+0.8711** | [+0.8444, +0.8935] | +0.0424 | [+0.0205, +0.0659] | +0.0256 | [+0.0147, +0.0377] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.7014 | +0.7432 | **+0.7596** | [+0.7218, +0.7930] | +0.0582 | [+0.0345, +0.0830] | +0.0164 | [+0.0038, +0.0302] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4159 | +0.5087 | **+0.5096** | [+0.4441, +0.5683] | +0.0938 | [+0.0584, +0.1297] | +0.0009 | [-0.0222, +0.0244] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.40 | +0.5494 | +0.6768 | **+0.6666** | [+0.6145, +0.7150] | +0.1172 | [+0.0850, +0.1538] | -0.0102 | [-0.0292, +0.0079] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6487 | +0.6252 | **+0.6698** | [+0.6238, +0.7143] | +0.0211 | [-0.0085, +0.0506] | +0.0445 | [+0.0275, +0.0620] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.40 | +0.6220 | +0.7812 | **+0.7927** | [+0.7521, +0.8270] | +0.1708 | [+0.1279, +0.2153] | +0.0115 | [-0.0112, +0.0344] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7856 | +0.8281 | **+0.8443** | [+0.8157, +0.8699] | +0.0587 | [+0.0365, +0.0820] | +0.0162 | [+0.0046, +0.0274] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3166 | +0.3965 | **+0.4324** | [+0.3744, +0.4892] | +0.1157 | [+0.0672, +0.1674] | +0.0358 | [+0.0056, +0.0652] |
| **medie** | | | | 0.775 | 0.37 | +0.5997 | +0.6595 | **+0.6846** | | +0.0849 | | +0.0251 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5519** | -0.0046 | [-0.0128, +0.0035] | 11.9% |
| de | +0.7468 | **+0.7478** | +0.0010 | [-0.0061, +0.0085] | 57.6% |
| en | +0.8700 | **+0.8711** | +0.0011 | [-0.0028, +0.0050] | 70.6% |
| es | +0.7641 | **+0.7596** | -0.0044 | [-0.0079, -0.0011] | 0.5% |
| fil | +0.5091 | **+0.5096** | +0.0006 | [-0.0036, +0.0045] | 60.7% |
| fr | +0.6590 | **+0.6666** | +0.0076 | [+0.0029, +0.0126] | 100.0% |
| it | +0.6750 | **+0.6698** | -0.0052 | [-0.0107, -0.0000] | 2.5% |
| ja | +0.7877 | **+0.7927** | +0.0050 | [+0.0010, +0.0094] | 99.5% |
| pt | +0.8450 | **+0.8443** | -0.0007 | [-0.0034, +0.0022] | 31.4% |
| si | +0.4251 | **+0.4324** | +0.0072 | [+0.0006, +0.0139] | 98.2% |
| **medie** | +0.6838 | **+0.6846** | +0.0007 | | 53.3% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 3. Pe medie, **+0.0007**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6846** | [+0.6699, +0.6989] | |
| fuziune − A | +0.0849 | [+0.0732, +0.0956] | 100.0% |
| fuziune − B | +0.0251 | [+0.0188, +0.0314] | 100.0% |
| configuratia noua − cea de azi | +0.0007 | [-0.0010, +0.0024] | 80.2% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5997 |
| semnalul B singur, `lolo` | 0.6595 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6846** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0275**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.35 | 9 | 5179 | +0.6105 | +0.7006 | 0.0901 | 0.0039 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6792 | 0.0841 | 0.0027 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6656 | 0.0895 | 0.0036 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5869 | +0.6779 | 0.0910 | 0.0026 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6243 | +0.7055 | 0.0812 | 0.0033 |
| fr | 0.750 | 0.40 | 9 | 5055 | +0.6072 | +0.6881 | 0.0809 | 0.0045 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5961 | +0.6880 | 0.0919 | 0.0036 |
| ja | 0.750 | 0.40 | 9 | 5054 | +0.5991 | +0.6741 | 0.0750 | 0.0028 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5776 | +0.6685 | 0.0909 | 0.0026 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6330 | +0.7143 | 0.0813 | 0.0020 |

Latimea medie a curbei lui w e 0.0856, iar a criteriului de candidati 0.0032, adica de 27 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
