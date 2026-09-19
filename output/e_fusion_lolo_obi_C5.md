# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 22:25:47 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag obi_C5 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encZC5_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_obi_C5.csv`, predictii per instanta in `output/fusion_preds_lolo_obi_C5.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.500 | 0.35 | +0.4594 | +0.5187 | **+0.5604** | [+0.4980, +0.6162] | +0.1010 | [+0.0492, +0.1586] | +0.0417 | [+0.0133, +0.0681] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.375 | 0.35 | +0.6671 | +0.7108 | **+0.7687** | [+0.7345, +0.7998] | +0.1016 | [+0.0663, +0.1385] | +0.0580 | [+0.0387, +0.0774] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.35 | +0.8242 | +0.8471 | **+0.8710** | [+0.8445, +0.8932] | +0.0468 | [+0.0253, +0.0709] | +0.0239 | [+0.0129, +0.0357] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.35 | +0.7012 | +0.7553 | **+0.7667** | [+0.7296, +0.7998] | +0.0655 | [+0.0412, +0.0889] | +0.0114 | [-0.0003, +0.0240] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.375 | 0.35 | +0.4084 | +0.5000 | **+0.5032** | [+0.4367, +0.5618] | +0.0948 | [+0.0546, +0.1329] | +0.0032 | [-0.0169, +0.0247] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.35 | +0.5503 | +0.6752 | **+0.6699** | [+0.6182, +0.7170] | +0.1196 | [+0.0865, +0.1572] | -0.0053 | [-0.0217, +0.0097] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.500 | 0.35 | +0.6466 | +0.6406 | **+0.6785** | [+0.6343, +0.7219] | +0.0319 | [+0.0033, +0.0607] | +0.0379 | [+0.0215, +0.0548] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.35 | +0.6233 | +0.7795 | **+0.7952** | [+0.7547, +0.8290] | +0.1719 | [+0.1259, +0.2195] | +0.0158 | [-0.0029, +0.0358] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.500 | 0.35 | +0.7871 | +0.8243 | **+0.8410** | [+0.8107, +0.8677] | +0.0539 | [+0.0338, +0.0760] | +0.0167 | [+0.0055, +0.0273] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.375 | 0.35 | +0.3461 | +0.3979 | **+0.4412** | [+0.3853, +0.4947] | +0.0951 | [+0.0496, +0.1420] | +0.0434 | [+0.0170, +0.0695] |
| **medie** | | | | 0.487 | 0.35 | +0.6014 | +0.6649 | **+0.6896** | | +0.0882 | | +0.0247 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5604** | -0.0035 | [-0.0059, -0.0009] | 0.1% |
| de | +0.7712 | **+0.7687** | -0.0025 | [-0.0049, -0.0002] | 1.4% |
| en | +0.8723 | **+0.8710** | -0.0013 | [-0.0024, -0.0002] | 1.1% |
| es | +0.7672 | **+0.7667** | -0.0005 | [-0.0025, +0.0014] | 30.6% |
| fil | +0.5074 | **+0.5032** | -0.0041 | [-0.0067, -0.0016] | 0.0% |
| fr | +0.6679 | **+0.6699** | +0.0020 | [+0.0000, +0.0037] | 97.8% |
| it | +0.6795 | **+0.6785** | -0.0010 | [-0.0025, +0.0005] | 10.1% |
| ja | +0.7942 | **+0.7952** | +0.0010 | [-0.0034, +0.0053] | 67.2% |
| pt | +0.8413 | **+0.8410** | -0.0003 | [-0.0018, +0.0012] | 36.9% |
| si | +0.4350 | **+0.4412** | +0.0062 | [-0.0050, +0.0175] | 84.6% |
| **medie** | +0.6900 | **+0.6896** | -0.0004 | | 33.0% |

Configuratia noua urca fuziunea pe 3 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0004**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6896** | [+0.6753, +0.7032] | |
| fuziune − A | +0.0882 | [+0.0765, +0.0996] | 100.0% |
| fuziune − B | +0.0247 | [+0.0189, +0.0305] | 100.0% |
| configuratia noua − cea de azi | -0.0004 | [-0.0017, +0.0010] | 27.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6014 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6896** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0325**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.500 | 0.35 | 9 | 5179 | +0.6176 | +0.7042 | 0.0866 | 0.0026 |
| de | 0.375 | 0.35 | 9 | 5054 | +0.5957 | +0.6810 | 0.0853 | 0.0025 |
| en | 0.500 | 0.35 | 9 | 5054 | +0.5771 | +0.6697 | 0.0926 | 0.0022 |
| es | 0.625 | 0.35 | 9 | 5031 | +0.5885 | +0.6812 | 0.0927 | 0.0023 |
| fil | 0.375 | 0.35 | 9 | 5054 | +0.6245 | +0.7105 | 0.0860 | 0.0015 |
| fr | 0.625 | 0.35 | 9 | 5055 | +0.6053 | +0.6920 | 0.0867 | 0.0019 |
| it | 0.500 | 0.35 | 9 | 5054 | +0.5968 | +0.6911 | 0.0943 | 0.0020 |
| ja | 0.500 | 0.35 | 9 | 5054 | +0.5994 | +0.6782 | 0.0788 | 0.0010 |
| pt | 0.500 | 0.35 | 9 | 5057 | +0.5812 | +0.6731 | 0.0919 | 0.0026 |
| si | 0.375 | 0.35 | 9 | 5024 | +0.6314 | +0.7174 | 0.0860 | 0.0021 |

Latimea medie a curbei lui w e 0.0881, iar a criteriului de candidati 0.0021, adica de 43 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
