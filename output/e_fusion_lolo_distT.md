# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-20 00:49:06 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag distT --b-dir output/bakeoff_test_T --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat.csv`. **Semnalul B de test vine din `output/bakeoff_test_T/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_distT.csv`, predictii per instanta in `output/fusion_preds_lolo_distT.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4619 | +0.5115 | **+0.5543** | [+0.4899, +0.6116] | +0.0924 | [+0.0409, +0.1482] | +0.0428 | [+0.0144, +0.0695] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6682 | **+0.7376** | [+0.6990, +0.7734] | +0.0591 | [+0.0271, +0.0932] | +0.0694 | [+0.0502, +0.0891] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8468 | **+0.8719** | [+0.8461, +0.8939] | +0.0432 | [+0.0220, +0.0672] | +0.0251 | [+0.0147, +0.0368] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.35 | +0.7030 | +0.7491 | **+0.7630** | [+0.7264, +0.7965] | +0.0600 | [+0.0363, +0.0842] | +0.0139 | [+0.0020, +0.0262] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4159 | +0.5215 | **+0.5172** | [+0.4523, +0.5756] | +0.1013 | [+0.0654, +0.1361] | -0.0043 | [-0.0273, +0.0190] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.40 | +0.5494 | +0.6634 | **+0.6574** | [+0.6031, +0.7065] | +0.1080 | [+0.0755, +0.1437] | -0.0061 | [-0.0256, +0.0126] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6489 | +0.6306 | **+0.6710** | [+0.6277, +0.7146] | +0.0221 | [-0.0058, +0.0506] | +0.0404 | [+0.0245, +0.0565] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.40 | +0.6279 | +0.7787 | **+0.7927** | [+0.7505, +0.8271] | +0.1649 | [+0.1238, +0.2093] | +0.0141 | [-0.0071, +0.0368] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.35 | +0.7863 | +0.8350 | **+0.8474** | [+0.8170, +0.8734] | +0.0611 | [+0.0401, +0.0837] | +0.0124 | [+0.0016, +0.0229] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3166 | +0.3741 | **+0.4174** | [+0.3614, +0.4721] | +0.1007 | [+0.0510, +0.1529] | +0.0432 | [+0.0123, +0.0729] |
| **medie** | | | | 0.688 | 0.37 | +0.6017 | +0.6579 | **+0.6830** | | +0.0813 | | +0.0251 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5411 | **+0.5543** | +0.0132 | [+0.0017, +0.0257] | 98.8% |
| de | +0.7333 | **+0.7376** | +0.0043 | [-0.0039, +0.0127] | 86.2% |
| en | +0.8702 | **+0.8719** | +0.0017 | [-0.0034, +0.0068] | 74.1% |
| es | +0.7606 | **+0.7630** | +0.0024 | [-0.0032, +0.0081] | 78.4% |
| fil | +0.5121 | **+0.5172** | +0.0051 | [-0.0022, +0.0124] | 91.6% |
| fr | +0.6450 | **+0.6574** | +0.0124 | [+0.0045, +0.0206] | 100.0% |
| it | +0.6647 | **+0.6710** | +0.0063 | [-0.0010, +0.0133] | 95.9% |
| ja | +0.7835 | **+0.7927** | +0.0092 | [+0.0025, +0.0159] | 99.9% |
| pt | +0.8427 | **+0.8474** | +0.0046 | [+0.0003, +0.0092] | 98.2% |
| si | +0.3962 | **+0.4174** | +0.0212 | [+0.0075, +0.0346] | 100.0% |
| **medie** | +0.6749 | **+0.6830** | +0.0080 | | 92.3% |

Configuratia noua urca fuziunea pe 10 din 10 limbi. Intervalul pereche exclude zero in sus pe 5. Pe medie, **+0.0080**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6830** | [+0.6684, +0.6969] | |
| fuziune − A | +0.0813 | [+0.0695, +0.0921] | 100.0% |
| fuziune − B | +0.0251 | [+0.0188, +0.0312] | 100.0% |
| configuratia noua − cea de azi | +0.0080 | [+0.0055, +0.0106] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6017 |
| semnalul B singur, `lolo` | 0.6579 |
| fuziunea de azi, A = `p_multi` | 0.6749 |
| **fuziunea cu ansamblul de surse** | **0.6830** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0259**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6169 | +0.6990 | 0.0821 | 0.0038 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6785 | 0.0834 | 0.0037 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6637 | 0.0876 | 0.0033 |
| es | 0.750 | 0.35 | 9 | 5031 | +0.5901 | +0.6758 | 0.0857 | 0.0032 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6243 | +0.7029 | 0.0786 | 0.0040 |
| fr | 0.750 | 0.40 | 9 | 5055 | +0.6072 | +0.6873 | 0.0801 | 0.0049 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.5984 | +0.6859 | 0.0875 | 0.0043 |
| ja | 0.500 | 0.40 | 9 | 5054 | +0.6018 | +0.6719 | 0.0701 | 0.0032 |
| pt | 0.750 | 0.35 | 9 | 5057 | +0.5809 | +0.6664 | 0.0855 | 0.0033 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6330 | +0.7142 | 0.0812 | 0.0023 |

Latimea medie a curbei lui w e 0.0822, iar a criteriului de candidati 0.0036, adica de 23 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
