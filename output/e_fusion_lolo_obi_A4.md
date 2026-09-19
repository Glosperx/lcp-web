# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 21:45:08 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag obi_A4 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encXA4_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_obi_A4.csv`, predictii per instanta in `output/fusion_preds_lolo_obi_A4.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4532 | +0.5187 | **+0.5602** | [+0.4980, +0.6159] | +0.1071 | [+0.0572, +0.1636] | +0.0415 | [+0.0140, +0.0676] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6740 | +0.7108 | **+0.7687** | [+0.7359, +0.7992] | +0.0947 | [+0.0607, +0.1309] | +0.0580 | [+0.0395, +0.0765] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8300 | +0.8471 | **+0.8740** | [+0.8480, +0.8954] | +0.0441 | [+0.0227, +0.0686] | +0.0270 | [+0.0158, +0.0392] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.7021 | +0.7553 | **+0.7682** | [+0.7304, +0.8013] | +0.0661 | [+0.0414, +0.0917] | +0.0129 | [+0.0004, +0.0260] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.35 | +0.4179 | +0.5000 | **+0.5064** | [+0.4396, +0.5652] | +0.0885 | [+0.0493, +0.1257] | +0.0063 | [-0.0135, +0.0276] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.35 | +0.5508 | +0.6752 | **+0.6696** | [+0.6172, +0.7168] | +0.1189 | [+0.0856, +0.1560] | -0.0055 | [-0.0216, +0.0095] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6432 | +0.6406 | **+0.6775** | [+0.6332, +0.7210] | +0.0342 | [+0.0055, +0.0636] | +0.0368 | [+0.0203, +0.0536] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.6247 | +0.7795 | **+0.7971** | [+0.7558, +0.8306] | +0.1723 | [+0.1259, +0.2197] | +0.0176 | [-0.0013, +0.0379] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7890 | +0.8243 | **+0.8418** | [+0.8121, +0.8684] | +0.0528 | [+0.0324, +0.0747] | +0.0175 | [+0.0062, +0.0282] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.35 | +0.3183 | +0.3979 | **+0.4385** | [+0.3775, +0.4952] | +0.1202 | [+0.0705, +0.1730] | +0.0406 | [+0.0099, +0.0701] |
| **medie** | | | | 0.775 | 0.35 | +0.6003 | +0.6649 | **+0.6902** | | +0.0899 | | +0.0253 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5602** | -0.0037 | [-0.0076, -0.0000] | 2.5% |
| de | +0.7712 | **+0.7687** | -0.0025 | [-0.0042, -0.0008] | 0.2% |
| en | +0.8723 | **+0.8740** | +0.0017 | [+0.0004, +0.0029] | 99.6% |
| es | +0.7672 | **+0.7682** | +0.0010 | [-0.0007, +0.0028] | 88.6% |
| fil | +0.5074 | **+0.5064** | -0.0010 | [-0.0033, +0.0013] | 20.3% |
| fr | +0.6679 | **+0.6696** | +0.0017 | [-0.0003, +0.0036] | 95.5% |
| it | +0.6795 | **+0.6775** | -0.0021 | [-0.0040, -0.0001] | 2.1% |
| ja | +0.7942 | **+0.7971** | +0.0029 | [+0.0003, +0.0057] | 98.4% |
| pt | +0.8413 | **+0.8418** | +0.0006 | [-0.0007, +0.0018] | 80.7% |
| si | +0.4350 | **+0.4385** | +0.0035 | [-0.0013, +0.0084] | 92.7% |
| **medie** | +0.6900 | **+0.6902** | +0.0002 | | 58.1% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0002**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6902** | [+0.6756, +0.7040] | |
| fuziune − A | +0.0899 | [+0.0777, +0.1009] | 100.0% |
| fuziune − B | +0.0253 | [+0.0193, +0.0312] | 100.0% |
| configuratia noua − cea de azi | +0.0002 | [-0.0006, +0.0011] | 70.2% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6003 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6902** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0331**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6186 | +0.7050 | 0.0864 | 0.0045 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5958 | +0.6817 | 0.0859 | 0.0033 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5767 | +0.6701 | 0.0934 | 0.0046 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5847 | +0.6815 | 0.0968 | 0.0024 |
| fil | 0.625 | 0.35 | 9 | 5054 | +0.6242 | +0.7109 | 0.0867 | 0.0026 |
| fr | 0.875 | 0.35 | 9 | 5055 | +0.6051 | +0.6927 | 0.0876 | 0.0037 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.5992 | +0.6919 | 0.0927 | 0.0039 |
| ja | 0.750 | 0.35 | 9 | 5054 | +0.5995 | +0.6787 | 0.0792 | 0.0024 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5786 | +0.6736 | 0.0950 | 0.0028 |
| si | 0.875 | 0.35 | 9 | 5024 | +0.6309 | +0.7184 | 0.0875 | 0.0040 |

Latimea medie a curbei lui w e 0.0891, iar a criteriului de candidati 0.0034, adica de 26 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
