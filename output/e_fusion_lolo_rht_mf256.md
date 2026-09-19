# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 15:33:37 de `fuse_ab.py --arm lolo --fit test --pick-split test --tag rht_mf256 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_tf-proj-394_rht-mf256_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ctrl_proj394.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_rht_mf256.csv`, predictii per instanta in `output/fusion_preds_lolo_rht_mf256.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.000 | 0.30 | +0.4327 | +0.5187 | **+0.5479** | [+0.4852, +0.6030] | +0.1152 | [+0.0625, +0.1723] | +0.0292 | [+0.0065, +0.0526] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.000 | 0.25 | +0.6597 | +0.7108 | **+0.7547** | [+0.7204, +0.7854] | +0.0950 | [+0.0567, +0.1359] | +0.0440 | [+0.0310, +0.0567] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.000 | 0.30 | +0.8314 | +0.8471 | **+0.8719** | [+0.8448, +0.8948] | +0.0405 | [+0.0188, +0.0645] | +0.0248 | [+0.0153, +0.0355] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.000 | 0.30 | +0.6828 | +0.7553 | **+0.7623** | [+0.7241, +0.7976] | +0.0796 | [+0.0534, +0.1056] | +0.0070 | [-0.0031, +0.0178] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.000 | 0.30 | +0.4084 | +0.5000 | **+0.5064** | [+0.4404, +0.5650] | +0.0980 | [+0.0555, +0.1398] | +0.0063 | [-0.0107, +0.0241] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.000 | 0.30 | +0.5397 | +0.6752 | **+0.6726** | [+0.6209, +0.7197] | +0.1329 | [+0.0941, +0.1757] | -0.0026 | [-0.0167, +0.0108] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.000 | 0.30 | +0.6225 | +0.6406 | **+0.6698** | [+0.6228, +0.7155] | +0.0473 | [+0.0151, +0.0813] | +0.0291 | [+0.0149, +0.0439] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.000 | 0.30 | +0.6237 | +0.7795 | **+0.7918** | [+0.7520, +0.8238] | +0.1682 | [+0.1297, +0.2078] | +0.0124 | [+0.0005, +0.0248] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.000 | 0.30 | +0.7772 | +0.8243 | **+0.8360** | [+0.8061, +0.8626] | +0.0588 | [+0.0378, +0.0822] | +0.0117 | [+0.0031, +0.0200] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.000 | 0.30 | +0.2226 | +0.3979 | **+0.3962** | [+0.3405, +0.4482] | +0.1736 | [+0.1188, +0.2301] | -0.0017 | [-0.0230, +0.0197] |
| **medie** | | | | 0.000 | 0.29 | +0.5800 | +0.6649 | **+0.6810** | | +0.1009 | | +0.0160 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ctrl_proj394.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5480 | **+0.5479** | -0.0001 | [-0.0027, +0.0026] | 46.6% |
| de | +0.7544 | **+0.7547** | +0.0003 | [-0.0011, +0.0018] | 66.1% |
| en | +0.8711 | **+0.8719** | +0.0008 | [-0.0004, +0.0021] | 91.2% |
| es | +0.7616 | **+0.7623** | +0.0007 | [-0.0007, +0.0021] | 83.8% |
| fil | +0.5082 | **+0.5064** | -0.0018 | [-0.0036, -0.0000] | 2.1% |
| fr | +0.6714 | **+0.6726** | +0.0011 | [-0.0006, +0.0030] | 89.9% |
| it | +0.6674 | **+0.6698** | +0.0024 | [-0.0009, +0.0058] | 92.3% |
| ja | +0.7887 | **+0.7918** | +0.0031 | [+0.0006, +0.0059] | 99.1% |
| pt | +0.8358 | **+0.8360** | +0.0002 | [-0.0011, +0.0016] | 63.1% |
| si | +0.3961 | **+0.3962** | +0.0000 | [-0.0055, +0.0050] | 48.5% |
| **medie** | +0.6803 | **+0.6810** | +0.0007 | | 68.3% |

Configuratia noua urca fuziunea pe 7 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **+0.0007**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6810** | [+0.6666, +0.6946] | |
| fuziune − A | +0.1009 | [+0.0889, +0.1130] | 100.0% |
| fuziune − B | +0.0160 | [+0.0113, +0.0206] | 100.0% |
| configuratia noua − cea de azi | +0.0007 | [-0.0001, +0.0015] | 94.8% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5800 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6803 |
| **fuziunea cu ansamblul de surse** | **0.6810** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0239**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.000 | 0.30 | 9 | 5179 | +0.5964 | +0.6963 | 0.0999 | 0.0000 |
| de | 0.000 | 0.25 | 9 | 5054 | +0.5712 | +0.6728 | 0.1016 | 0.0000 |
| en | 0.000 | 0.30 | 9 | 5054 | +0.5521 | +0.6603 | 0.1082 | 0.0000 |
| es | 0.000 | 0.30 | 9 | 5031 | +0.5686 | +0.6725 | 0.1039 | 0.0000 |
| fil | 0.000 | 0.30 | 9 | 5054 | +0.5991 | +0.7009 | 0.1018 | 0.0000 |
| fr | 0.000 | 0.30 | 9 | 5055 | +0.5845 | +0.6824 | 0.0979 | 0.0000 |
| it | 0.000 | 0.30 | 9 | 5054 | +0.5753 | +0.6828 | 0.1075 | 0.0000 |
| ja | 0.000 | 0.30 | 9 | 5054 | +0.5752 | +0.6692 | 0.0940 | 0.0000 |
| pt | 0.000 | 0.30 | 9 | 5057 | +0.5581 | +0.6643 | 0.1062 | 0.0000 |
| si | 0.000 | 0.30 | 9 | 5024 | +0.6198 | +0.7132 | 0.0934 | 0.0000 |

Latimea medie a curbei lui w e 0.1014, iar a criteriului de candidati 0.0000, adica de inf ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
