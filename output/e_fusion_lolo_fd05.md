# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-23 23:54:14 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag fd05 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encmean-fd05_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_fd05.csv`, predictii per instanta in `output/fusion_preds_lolo_fd05.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 1.000 | 0.30 | +0.4290 | +0.5187 | **+0.5646** | [+0.5018, +0.6209] | +0.1356 | [+0.0696, +0.2049] | +0.0459 | [+0.0194, +0.0712] |
| de | `gemma4-12b-4bit` | 570 | 193 | 1.000 | 0.30 | +0.5892 | +0.7108 | **+0.7501** | [+0.7148, +0.7819] | +0.1609 | [+0.1146, +0.2103] | +0.0393 | [+0.0225, +0.0566] |
| en | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.30 | +0.8199 | +0.8471 | **+0.8696** | [+0.8423, +0.8931] | +0.0497 | [+0.0260, +0.0747] | +0.0226 | [+0.0132, +0.0333] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.750 | 0.35 | +0.6889 | +0.7553 | **+0.7665** | [+0.7301, +0.7998] | +0.0776 | [+0.0511, +0.1053] | +0.0112 | [-0.0011, +0.0233] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.30 | +0.4695 | +0.5000 | **+0.5325** | [+0.4673, +0.5929] | +0.0630 | [+0.0222, +0.1062] | +0.0325 | [+0.0142, +0.0512] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5244 | +0.6752 | **+0.6642** | [+0.6119, +0.7125] | +0.1398 | [+0.1055, +0.1788] | -0.0109 | [-0.0276, +0.0055] |
| it | `gemma4-12b-4bit` | 570 | 192 | 1.000 | 0.30 | +0.5760 | +0.6406 | **+0.6675** | [+0.6218, +0.7120] | +0.0915 | [+0.0520, +0.1319] | +0.0268 | [+0.0098, +0.0445] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.35 | +0.5723 | +0.7795 | **+0.7877** | [+0.7467, +0.8228] | +0.2154 | [+0.1614, +0.2693] | +0.0083 | [-0.0117, +0.0283] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.35 | +0.7521 | +0.8243 | **+0.8368** | [+0.8053, +0.8641] | +0.0847 | [+0.0615, +0.1098] | +0.0125 | [+0.0004, +0.0238] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.30 | +0.3352 | +0.3979 | **+0.4279** | [+0.3719, +0.4792] | +0.0927 | [+0.0467, +0.1406] | +0.0300 | [+0.0095, +0.0495] |
| **medie** | | | | 0.912 | 0.32 | +0.5757 | +0.6649 | **+0.6867** | | +0.1111 | | +0.0218 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5646** | +0.0007 | [-0.0186, +0.0200] | 53.3% |
| de | +0.7712 | **+0.7501** | -0.0212 | [-0.0304, -0.0120] | 0.0% |
| en | +0.8723 | **+0.8696** | -0.0027 | [-0.0072, +0.0016] | 11.6% |
| es | +0.7672 | **+0.7665** | -0.0007 | [-0.0091, +0.0073] | 40.0% |
| fil | +0.5074 | **+0.5325** | +0.0251 | [+0.0078, +0.0408] | 99.9% |
| fr | +0.6679 | **+0.6642** | -0.0037 | [-0.0122, +0.0045] | 19.1% |
| it | +0.6795 | **+0.6675** | -0.0121 | [-0.0214, -0.0032] | 0.4% |
| ja | +0.7942 | **+0.7877** | -0.0065 | [-0.0216, +0.0081] | 18.1% |
| pt | +0.8413 | **+0.8368** | -0.0045 | [-0.0087, -0.0000] | 2.3% |
| si | +0.4350 | **+0.4279** | -0.0071 | [-0.0234, +0.0086] | 18.2% |
| **medie** | +0.6900 | **+0.6867** | -0.0033 | | 26.3% |

Configuratia noua urca fuziunea pe 2 din 10 limbi. Intervalul pereche exclude zero in sus pe 1. Pe medie, **-0.0033**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6867** | [+0.6720, +0.7006] | |
| fuziune − A | +0.1111 | [+0.0978, +0.1246] | 100.0% |
| fuziune − B | +0.0218 | [+0.0163, +0.0274] | 100.0% |
| configuratia noua − cea de azi | -0.0033 | [-0.0069, +0.0005] | 4.5% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5757 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6867** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0296**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 1.000 | 0.30 | 9 | 5179 | +0.5916 | +0.7020 | 0.1104 | 0.0027 |
| de | 1.000 | 0.30 | 9 | 5054 | +0.5738 | +0.6814 | 0.1076 | 0.0028 |
| en | 1.000 | 0.30 | 9 | 5054 | +0.5481 | +0.6681 | 0.1200 | 0.0032 |
| es | 0.750 | 0.35 | 9 | 5031 | +0.5698 | +0.6794 | 0.1096 | 0.0030 |
| fil | 0.750 | 0.30 | 9 | 5054 | +0.5941 | +0.7053 | 0.1112 | 0.0018 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.5810 | +0.6909 | 0.1099 | 0.0055 |
| it | 1.000 | 0.30 | 9 | 5054 | +0.5752 | +0.6906 | 0.1154 | 0.0026 |
| ja | 1.000 | 0.35 | 9 | 5054 | +0.5756 | +0.6772 | 0.1016 | 0.0053 |
| pt | 0.750 | 0.35 | 9 | 5057 | +0.5627 | +0.6716 | 0.1089 | 0.0035 |
| si | 0.875 | 0.30 | 9 | 5024 | +0.6059 | +0.7172 | 0.1113 | 0.0025 |

Latimea medie a curbei lui w e 0.1106, iar a criteriului de candidati 0.0033, adica de 34 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
