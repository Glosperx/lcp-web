# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 21:46:38 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag obi_ctrl --b-dir output/bakeoff_test_M3K --a-set A=output/e1_frozen_preds.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_obi_ctrl.csv`, predictii per instanta in `output/fusion_preds_lolo_obi_ctrl.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi e fixat la `A`, prin argument si nu prin scor: lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio eticheta.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 9 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.25 | +0.3932 | +0.5187 | **+0.5360** | [+0.4714, +0.5921] | +0.1429 | [+0.0851, +0.2037] | +0.0173 | [-0.0018, +0.0363] |
| de | `gemma4-12b-4bit` | 570 | 193 | 1.000 | 0.25 | +0.6359 | +0.7108 | **+0.7514** | [+0.7166, +0.7819] | +0.1155 | [+0.0737, +0.1593] | +0.0406 | [+0.0266, +0.0542] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.25 | +0.8253 | +0.8471 | **+0.8672** | [+0.8386, +0.8918] | +0.0419 | [+0.0192, +0.0658] | +0.0201 | [+0.0123, +0.0290] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.30 | +0.6055 | +0.7553 | **+0.7450** | [+0.7056, +0.7813] | +0.1394 | [+0.1052, +0.1706] | -0.0103 | [-0.0210, +0.0006] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.750 | 0.30 | +0.4146 | +0.5016 | **+0.5104** | [+0.4471, +0.5718] | +0.0959 | [+0.0518, +0.1387] | +0.0089 | [-0.0081, +0.0270] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.875 | 0.30 | +0.5178 | +0.6778 | **+0.6707** | [+0.6190, +0.7165] | +0.1529 | [+0.1137, +0.1942] | -0.0071 | [-0.0208, +0.0064] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.875 | 0.25 | +0.5918 | +0.6394 | **+0.6593** | [+0.6123, +0.7060] | +0.0675 | [+0.0319, +0.1027] | +0.0199 | [+0.0086, +0.0316] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.30 | +0.5797 | +0.7795 | **+0.8017** | [+0.7642, +0.8344] | +0.2220 | [+0.1770, +0.2704] | +0.0222 | [+0.0064, +0.0385] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.750 | 0.30 | +0.7786 | +0.8275 | **+0.8399** | [+0.8087, +0.8666] | +0.0613 | [+0.0404, +0.0831] | +0.0123 | [+0.0034, +0.0214] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.30 | +0.2565 | +0.3979 | **+0.4152** | [+0.3600, +0.4667] | +0.1587 | [+0.1018, +0.2166] | +0.0173 | [-0.0058, +0.0396] |
| **medie** | | | | 0.838 | 0.28 | +0.5599 | +0.6655 | **+0.6797** | | +0.1198 | | +0.0141 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 5 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5360** | -0.0279 | [-0.0422, -0.0121] | 0.0% |
| de | +0.7712 | **+0.7514** | -0.0199 | [-0.0304, -0.0103] | 0.0% |
| en | +0.8723 | **+0.8672** | -0.0051 | [-0.0104, +0.0001] | 2.7% |
| es | +0.7672 | **+0.7450** | -0.0223 | [-0.0302, -0.0145] | 0.0% |
| fil | +0.5083 | **+0.5104** | +0.0021 | [-0.0030, +0.0070] | 80.5% |
| fr | +0.6711 | **+0.6707** | -0.0004 | [-0.0088, +0.0083] | 46.7% |
| it | +0.6788 | **+0.6593** | -0.0195 | [-0.0287, -0.0105] | 0.0% |
| ja | +0.7942 | **+0.8017** | +0.0075 | [-0.0072, +0.0213] | 84.7% |
| pt | +0.8457 | **+0.8399** | -0.0058 | [-0.0120, -0.0004] | 1.7% |
| si | +0.4350 | **+0.4152** | -0.0198 | [-0.0416, +0.0017] | 3.6% |
| **medie** | +0.6908 | **+0.6797** | -0.0111 | | 22.0% |

Configuratia noua urca fuziunea pe 2 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0111**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6797** | [+0.6654, +0.6933] | |
| fuziune − A | +0.1198 | [+0.1064, +0.1331] | 100.0% |
| fuziune − B | +0.0141 | [+0.0094, +0.0190] | 100.0% |
| configuratia noua − cea de azi | -0.0111 | [-0.0146, -0.0075] | 0.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5599 |
| semnalul B singur, `lolo` | 0.6655 |
| fuziunea de azi, A = `p_multi` | 0.6908 |
| **fuziunea cu ansamblul de surse** | **0.6797** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0226**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.25 | 9 | 5161 | +0.5749 | +0.6974 | 0.1225 | 0.0045 |
| de | 1.000 | 0.25 | 9 | 5036 | +0.5480 | +0.6735 | 0.1255 | 0.0042 |
| en | 0.875 | 0.25 | 9 | 5036 | +0.5314 | +0.6607 | 0.1293 | 0.0040 |
| es | 0.875 | 0.30 | 9 | 5013 | +0.5558 | +0.6744 | 0.1186 | 0.0059 |
| fil | 0.750 | 0.30 | 9 | 5038 | +0.5801 | +0.7004 | 0.1203 | 0.0026 |
| fr | 0.875 | 0.30 | 9 | 5040 | +0.5655 | +0.6826 | 0.1171 | 0.0051 |
| it | 0.875 | 0.25 | 9 | 5044 | +0.5573 | +0.6838 | 0.1265 | 0.0042 |
| ja | 0.750 | 0.30 | 9 | 5036 | +0.5617 | +0.6681 | 0.1064 | 0.0023 |
| pt | 0.750 | 0.30 | 9 | 5044 | +0.5396 | +0.6638 | 0.1242 | 0.0028 |
| si | 0.625 | 0.30 | 9 | 5006 | +0.5993 | +0.7108 | 0.1115 | 0.0015 |

Latimea medie a curbei lui w e 0.1202, iar a criteriului de candidati 0.0037, adica de 32 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
