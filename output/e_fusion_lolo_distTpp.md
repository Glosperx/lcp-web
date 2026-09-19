# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-20 01:09:55 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag distTpp --b-dir output/bakeoff_test_Tpp --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat.csv`. **Semnalul B de test vine din `output/bakeoff_test_Tpp/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_distTpp.csv`, predictii per instanta in `output/fusion_preds_lolo_distTpp.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.35 | +0.4668 | +0.5207 | **+0.5594** | [+0.4954, +0.6155] | +0.0927 | [+0.0431, +0.1470] | +0.0388 | [+0.0111, +0.0648] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6910 | **+0.7520** | [+0.7155, +0.7860] | +0.0736 | [+0.0411, +0.1080] | +0.0609 | [+0.0421, +0.0804] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.35 | +0.8287 | +0.8483 | **+0.8713** | [+0.8446, +0.8941] | +0.0426 | [+0.0213, +0.0658] | +0.0231 | [+0.0125, +0.0354] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.7014 | +0.7463 | **+0.7616** | [+0.7247, +0.7942] | +0.0602 | [+0.0362, +0.0855] | +0.0152 | [+0.0024, +0.0287] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4166 | +0.5171 | **+0.5174** | [+0.4527, +0.5754] | +0.1008 | [+0.0634, +0.1380] | +0.0004 | [-0.0194, +0.0208] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.35 | +0.5460 | +0.6689 | **+0.6638** | [+0.6100, +0.7128] | +0.1178 | [+0.0831, +0.1572] | -0.0052 | [-0.0220, +0.0104] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6487 | +0.6390 | **+0.6769** | [+0.6316, +0.7203] | +0.0282 | [-0.0002, +0.0571] | +0.0379 | [+0.0213, +0.0542] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.6140 | +0.7719 | **+0.7909** | [+0.7492, +0.8248] | +0.1769 | [+0.1316, +0.2249] | +0.0190 | [-0.0007, +0.0397] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7856 | +0.8294 | **+0.8416** | [+0.8105, +0.8686] | +0.0560 | [+0.0356, +0.0776] | +0.0122 | [+0.0013, +0.0227] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.3242 | +0.3830 | **+0.4227** | [+0.3656, +0.4766] | +0.0985 | [+0.0515, +0.1488] | +0.0396 | [+0.0101, +0.0683] |
| **medie** | | | | 0.762 | 0.35 | +0.6010 | +0.6616 | **+0.6858** | | +0.0847 | | +0.0242 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5411 | **+0.5594** | +0.0183 | [+0.0027, +0.0344] | 99.1% |
| de | +0.7333 | **+0.7520** | +0.0187 | [+0.0080, +0.0296] | 100.0% |
| en | +0.8702 | **+0.8713** | +0.0011 | [-0.0063, +0.0084] | 62.2% |
| es | +0.7606 | **+0.7616** | +0.0009 | [-0.0073, +0.0090] | 58.4% |
| fil | +0.5121 | **+0.5174** | +0.0054 | [-0.0055, +0.0162] | 83.7% |
| fr | +0.6450 | **+0.6638** | +0.0187 | [+0.0071, +0.0313] | 100.0% |
| it | +0.6647 | **+0.6769** | +0.0123 | [+0.0013, +0.0222] | 98.6% |
| ja | +0.7835 | **+0.7909** | +0.0074 | [-0.0033, +0.0181] | 91.2% |
| pt | +0.8427 | **+0.8416** | -0.0011 | [-0.0084, +0.0058] | 36.7% |
| si | +0.3962 | **+0.4227** | +0.0265 | [+0.0087, +0.0441] | 99.9% |
| **medie** | +0.6749 | **+0.6858** | +0.0108 | | 83.0% |

Configuratia noua urca fuziunea pe 9 din 10 limbi. Intervalul pereche exclude zero in sus pe 5. Pe medie, **+0.0108**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6858** | [+0.6713, +0.6997] | |
| fuziune − A | +0.0847 | [+0.0727, +0.0958] | 100.0% |
| fuziune − B | +0.0242 | [+0.0184, +0.0300] | 100.0% |
| configuratia noua − cea de azi | +0.0108 | [+0.0072, +0.0145] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6010 |
| semnalul B singur, `lolo` | 0.6616 |
| fuziunea de azi, A = `p_multi` | 0.6749 |
| **fuziunea cu ansamblul de surse** | **0.6858** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0287**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.35 | 9 | 5179 | +0.6186 | +0.7000 | 0.0814 | 0.0047 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6786 | 0.0835 | 0.0028 |
| en | 0.750 | 0.35 | 9 | 5054 | +0.5761 | +0.6654 | 0.0893 | 0.0049 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5869 | +0.6774 | 0.0905 | 0.0028 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6219 | +0.7047 | 0.0828 | 0.0027 |
| fr | 0.875 | 0.35 | 9 | 5055 | +0.6042 | +0.6883 | 0.0841 | 0.0037 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5961 | +0.6870 | 0.0909 | 0.0035 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5966 | +0.6742 | 0.0776 | 0.0023 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5776 | +0.6685 | 0.0909 | 0.0030 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6345 | +0.7152 | 0.0807 | 0.0038 |

Latimea medie a curbei lui w e 0.0852, iar a criteriului de candidati 0.0034, adica de 25 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
