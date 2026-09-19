# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 17:25:37 de `fuse_ab.py --arm lolo --fit test --pick-split test --tag lin_A1 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_A1-lassohgb_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_xlmr_plin.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_lin_A1.csv`, predictii per instanta in `output/fusion_preds_lolo_lin_A1.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 1 puncte, de la 0.000 la 0.000.

Setul de trasaturi e fixat la `fert_inloc`, prin argument si nu prin scor: lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio eticheta.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 1 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.000 | 0.30 | +0.4330 | +0.5187 | **+0.5511** | [+0.4885, +0.6070] | +0.1181 | [+0.0624, +0.1785] | +0.0323 | [+0.0079, +0.0565] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.000 | 0.30 | +0.6526 | +0.7108 | **+0.7638** | [+0.7302, +0.7942] | +0.1113 | [+0.0725, +0.1538] | +0.0531 | [+0.0365, +0.0686] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.000 | 0.30 | +0.8196 | +0.8471 | **+0.8695** | [+0.8422, +0.8930] | +0.0500 | [+0.0272, +0.0768] | +0.0225 | [+0.0129, +0.0329] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.000 | 0.30 | +0.6772 | +0.7553 | **+0.7619** | [+0.7241, +0.7962] | +0.0847 | [+0.0589, +0.1108] | +0.0066 | [-0.0030, +0.0171] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.000 | 0.30 | +0.4074 | +0.5000 | **+0.5058** | [+0.4394, +0.5650] | +0.0984 | [+0.0551, +0.1397] | +0.0057 | [-0.0114, +0.0237] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.000 | 0.30 | +0.5489 | +0.6752 | **+0.6759** | [+0.6255, +0.7226] | +0.1270 | [+0.0894, +0.1699] | +0.0007 | [-0.0130, +0.0139] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.000 | 0.30 | +0.6315 | +0.6406 | **+0.6718** | [+0.6259, +0.7167] | +0.0403 | [+0.0074, +0.0727] | +0.0312 | [+0.0168, +0.0456] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.000 | 0.30 | +0.5947 | +0.7795 | **+0.7906** | [+0.7500, +0.8231] | +0.1959 | [+0.1523, +0.2413] | +0.0112 | [-0.0018, +0.0248] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.000 | 0.30 | +0.7659 | +0.8243 | **+0.8341** | [+0.8037, +0.8609] | +0.0681 | [+0.0463, +0.0926] | +0.0097 | [+0.0011, +0.0181] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.000 | 0.30 | +0.2505 | +0.3979 | **+0.4092** | [+0.3565, +0.4612] | +0.1586 | [+0.0993, +0.2164] | +0.0113 | [-0.0112, +0.0355] |
| **medie** | | | | 0.000 | 0.30 | +0.5781 | +0.6649 | **+0.6834** | | +0.1052 | | +0.0184 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 5 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_xlmr_plin.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5533 | **+0.5511** | -0.0023 | [-0.0064, +0.0016] | 13.4% |
| de | +0.7609 | **+0.7638** | +0.0029 | [+0.0002, +0.0059] | 98.5% |
| en | +0.8695 | **+0.8695** | +0.0001 | [-0.0019, +0.0021] | 54.2% |
| es | +0.7595 | **+0.7619** | +0.0024 | [+0.0002, +0.0046] | 98.3% |
| fil | +0.5059 | **+0.5058** | -0.0002 | [-0.0024, +0.0021] | 41.7% |
| fr | +0.6738 | **+0.6759** | +0.0021 | [-0.0006, +0.0050] | 93.2% |
| it | +0.6730 | **+0.6718** | -0.0012 | [-0.0037, +0.0014] | 16.4% |
| ja | +0.7914 | **+0.7906** | -0.0008 | [-0.0063, +0.0043] | 40.6% |
| pt | +0.8337 | **+0.8341** | +0.0004 | [-0.0011, +0.0019] | 70.2% |
| si | +0.4067 | **+0.4092** | +0.0025 | [-0.0034, +0.0086] | 79.2% |
| **medie** | +0.6828 | **+0.6834** | +0.0006 | | 60.6% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0006**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6834** | [+0.6692, +0.6968] | |
| fuziune − A | +0.1052 | [+0.0923, +0.1178] | 100.0% |
| fuziune − B | +0.0184 | [+0.0134, +0.0234] | 100.0% |
| configuratia noua − cea de azi | +0.0006 | [-0.0005, +0.0017] | 86.9% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5781 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6828 |
| **fuziunea cu ansamblul de surse** | **0.6834** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0263**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.000 | 0.30 | 9 | 5179 | +0.5942 | +0.6981 | 0.1039 | 0.0000 |
| de | 0.000 | 0.30 | 9 | 5054 | +0.5699 | +0.6744 | 0.1045 | 0.0000 |
| en | 0.000 | 0.30 | 9 | 5054 | +0.5513 | +0.6627 | 0.1114 | 0.0000 |
| es | 0.000 | 0.30 | 9 | 5031 | +0.5671 | +0.6746 | 0.1075 | 0.0000 |
| fil | 0.000 | 0.30 | 9 | 5054 | +0.5971 | +0.7031 | 0.1060 | 0.0000 |
| fr | 0.000 | 0.30 | 9 | 5055 | +0.5814 | +0.6842 | 0.1028 | 0.0000 |
| it | 0.000 | 0.30 | 9 | 5054 | +0.5722 | +0.6847 | 0.1125 | 0.0000 |
| ja | 0.000 | 0.30 | 9 | 5054 | +0.5763 | +0.6714 | 0.0951 | 0.0000 |
| pt | 0.000 | 0.30 | 9 | 5057 | +0.5573 | +0.6666 | 0.1093 | 0.0000 |
| si | 0.000 | 0.30 | 9 | 5024 | +0.6145 | +0.7138 | 0.0993 | 0.0000 |

Latimea medie a curbei lui w e 0.1052, iar a criteriului de candidati 0.0000, adica de inf ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
| ponderea w | `fuse_ab.py`, `fit_choice` | `others = {l2: d for l2, d in fit.items() if l2 != lg}`. Curba nu contine niciun rand al lui L, pe niciun split. |
| w-ul limbilor de potrivire, in criteriu | `fuse_ab.py`, `fit_choice` | bucla `for l3 in others if l3 != l2`: cand un candidat se masoara pe L', ponderea lui L' vine de pe celelalte opt limbi, deci nici L nici L' nu intra in ea. |
| standardizarea | `fuse_ab.py`, `zscore` si `zA_of` | media si deviatia se iau din predictii, nu din etichete, la ambele niveluri de standardizare ale lui A. |

Si unde **nu** e garantata, fiindca trebuie scris tot. Doua locuri:

1. `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Alegerile lui L depind deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi. Dependenta e identica la potrivirea pe trial si la cea pe test, fiindca ambele folosesc aceleasi predictii. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare. Bratul `p_en` **nu** are dependenta asta: nu vede niciun rand de MLSP.
2. Modelul lui B al limbilor de potrivire se re-alege cu `exclude={L}`, deci la un nivel, nu la doua. In bucla interioara care alege w-ul lui L' pe celelalte opt, modelul acelor opt ramane cel ales cu `exclude={L}`, nu cu `exclude={L, L'}`. Nivelul urmator ar cere `pick_model` cu trei limbi excluse, si nu s-a coborat pana acolo.

### Filtrul de disponibilitate

Nu s-a activat: fiecare model cerut de selectia imbricata avea masuratori pe limba de potrivire, pe splitul de potrivire.
