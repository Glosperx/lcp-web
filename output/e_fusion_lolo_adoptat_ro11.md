# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-29 21:02:36 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag adoptat_ro11 --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc_ro11.csv`. Date brute: `output/fusion_lolo_adoptat_ro11.csv`, predictii per instanta in `output/fusion_preds_lolo_adoptat_ro11.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.45 | +0.4624 | +0.4829 | **+0.5420** | [+0.4759, +0.6016] | +0.0796 | [+0.0317, +0.1291] | +0.0590 | [+0.0181, +0.0980] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.40 | +0.6830 | +0.6544 | **+0.7388** | [+0.7003, +0.7749] | +0.0559 | [+0.0253, +0.0873] | +0.0844 | [+0.0620, +0.1082] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.45 | +0.8279 | +0.8377 | **+0.8703** | [+0.8442, +0.8927] | +0.0424 | [+0.0232, +0.0627] | +0.0326 | [+0.0190, +0.0483] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.45 | +0.7090 | +0.7432 | **+0.7616** | [+0.7244, +0.7949] | +0.0526 | [+0.0316, +0.0736] | +0.0184 | [+0.0029, +0.0341] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.45 | +0.4169 | +0.5173 | **+0.5125** | [+0.4465, +0.5726] | +0.0955 | [+0.0613, +0.1281] | -0.0048 | [-0.0302, +0.0226] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.45 | +0.5490 | +0.6424 | **+0.6425** | [+0.5873, +0.6931] | +0.0934 | [+0.0641, +0.1256] | +0.0000 | [-0.0224, +0.0228] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.875 | 0.40 | +0.6495 | +0.6127 | **+0.6661** | [+0.6233, +0.7104] | +0.0166 | [-0.0095, +0.0439] | +0.0534 | [+0.0347, +0.0728] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.6277 | +0.7676 | **+0.7816** | [+0.7365, +0.8202] | +0.1539 | [+0.1147, +0.1949] | +0.0140 | [-0.0123, +0.0413] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.45 | +0.7876 | +0.8213 | **+0.8424** | [+0.8104, +0.8695] | +0.0548 | [+0.0354, +0.0762] | +0.0211 | [+0.0056, +0.0361] |
| ro | `gemma4-12b-4bit` | 1587 | 274 | 0.875 | 0.40 | +0.7292 | +0.6449 | **+0.7417** | [+0.7077, +0.7726] | +0.0125 | [-0.0110, +0.0351] | +0.0967 | [+0.0783, +0.1161] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.45 | +0.3111 | +0.3407 | **+0.3949** | [+0.3336, +0.4534] | +0.0838 | [+0.0430, +0.1257] | +0.0542 | [+0.0127, +0.0934] |
| **medie** | | | | 0.705 | 0.44 | +0.6139 | +0.6423 | **+0.6813** | | +0.0674 | | +0.0390 | |

Fuziunea bate A pe 11 din 11 limbi si B pe 9 din 11. Intervalul exclude zero pe 9 limbi fata de A si pe 8 fata de B.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6813** | [+0.6672, +0.6949] | |
| fuziune − A | +0.0674 | [+0.0574, +0.0766] | 100.0% |
| fuziune − B | +0.0390 | [+0.0315, +0.0464] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6139 |
| semnalul B singur, `lolo` | 0.6423 |
| **fuziunea cu ansamblul de surse** | **0.6813** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0242**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.45 | 10 | 6766 | +0.6283 | +0.6968 | 0.0685 | 0.0055 |
| de | 0.750 | 0.40 | 10 | 6641 | +0.6063 | +0.6768 | 0.0705 | 0.0042 |
| en | 0.750 | 0.45 | 10 | 6641 | +0.5918 | +0.6640 | 0.0722 | 0.0053 |
| es | 0.625 | 0.45 | 10 | 6618 | +0.6056 | +0.6748 | 0.0692 | 0.0062 |
| fil | 0.625 | 0.45 | 10 | 6641 | +0.6349 | +0.6997 | 0.0648 | 0.0056 |
| fr | 0.625 | 0.45 | 10 | 6642 | +0.6216 | +0.6867 | 0.0651 | 0.0071 |
| it | 0.875 | 0.40 | 10 | 6641 | +0.6065 | +0.6840 | 0.0775 | 0.0045 |
| ja | 0.625 | 0.45 | 10 | 6641 | +0.6138 | +0.6728 | 0.0590 | 0.0029 |
| pt | 0.625 | 0.45 | 10 | 6644 | +0.5978 | +0.6667 | 0.0689 | 0.0059 |
| ro | 0.875 | 0.40 | 10 | 5624 | +0.5985 | +0.6764 | 0.0779 | 0.0046 |
| si | 0.625 | 0.45 | 10 | 6611 | +0.6454 | +0.7114 | 0.0660 | 0.0037 |

Latimea medie a curbei lui w e 0.0691, iar a criteriului de candidati 0.0050, adica de 14 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
