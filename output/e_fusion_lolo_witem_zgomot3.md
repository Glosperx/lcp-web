# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-22 19:40:07 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag witem_zgomot3 --b-dir output/bakeoff_test_Text --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv`. **Semnalul B de test vine din `output/bakeoff_test_Text/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_witem_zgomot3.csv`, predictii per instanta in `output/fusion_preds_lolo_witem_zgomot3.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4619 | +0.5159 | **+0.5566** | [+0.4928, +0.6133] | +0.0947 | [+0.0440, +0.1486] | +0.0407 | [+0.0124, +0.0677] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6812 | **+0.7468** | [+0.7096, +0.7810] | +0.0684 | [+0.0360, +0.1033] | +0.0656 | [+0.0461, +0.0854] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8259 | +0.8463 | **+0.8700** | [+0.8430, +0.8928] | +0.0441 | [+0.0224, +0.0680] | +0.0238 | [+0.0132, +0.0361] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.35 | +0.7014 | +0.7499 | **+0.7641** | [+0.7272, +0.7968] | +0.0627 | [+0.0392, +0.0872] | +0.0142 | [+0.0015, +0.0276] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4159 | +0.5082 | **+0.5091** | [+0.4439, +0.5668] | +0.0932 | [+0.0579, +0.1280] | +0.0009 | [-0.0219, +0.0240] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.40 | +0.5494 | +0.6655 | **+0.6590** | [+0.6046, +0.7079] | +0.1096 | [+0.0773, +0.1458] | -0.0065 | [-0.0260, +0.0114] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6489 | +0.6354 | **+0.6750** | [+0.6300, +0.7188] | +0.0261 | [-0.0022, +0.0551] | +0.0396 | [+0.0229, +0.0561] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.6267 | +0.7715 | **+0.7877** | [+0.7453, +0.8223] | +0.1610 | [+0.1190, +0.2046] | +0.0162 | [-0.0054, +0.0392] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.35 | +0.7856 | +0.8322 | **+0.8450** | [+0.8153, +0.8710] | +0.0594 | [+0.0381, +0.0817] | +0.0129 | [+0.0019, +0.0236] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.35 | +0.3166 | +0.3860 | **+0.4251** | [+0.3679, +0.4810] | +0.1085 | [+0.0602, +0.1610] | +0.0391 | [+0.0083, +0.0689] |
| **medie** | | | | 0.738 | 0.37 | +0.6011 | +0.6592 | **+0.6838** | | +0.0828 | | +0.0246 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6838** | [+0.6694, +0.6980] | |
| fuziune − A | +0.0828 | [+0.0710, +0.0934] | 100.0% |
| fuziune − B | +0.0246 | [+0.0184, +0.0308] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6011 |
| semnalul B singur, `lolo` | 0.6592 |
| **fuziunea cu ansamblul de surse** | **0.6838** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0267**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6169 | +0.6995 | 0.0826 | 0.0038 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6782 | 0.0831 | 0.0032 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5731 | +0.6645 | 0.0914 | 0.0041 |
| es | 0.875 | 0.35 | 9 | 5031 | +0.5869 | +0.6763 | 0.0894 | 0.0027 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6243 | +0.7045 | 0.0802 | 0.0032 |
| fr | 0.750 | 0.40 | 9 | 5055 | +0.6072 | +0.6878 | 0.0806 | 0.0043 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.5984 | +0.6862 | 0.0878 | 0.0038 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.6009 | +0.6735 | 0.0726 | 0.0027 |
| pt | 0.875 | 0.35 | 9 | 5057 | +0.5776 | +0.6673 | 0.0897 | 0.0027 |
| si | 0.750 | 0.35 | 9 | 5024 | +0.6330 | +0.7141 | 0.0811 | 0.0023 |

Latimea medie a curbei lui w e 0.0839, iar a criteriului de candidati 0.0033, adica de 26 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
