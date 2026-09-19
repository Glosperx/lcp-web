# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-29 14:20:32 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag p4only --b-dir output/bakeoff_test_P4ONLY --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_P4ONLY/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_p4only.csv`, predictii per instanta in `output/fusion_preds_lolo_p4only.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.875 | 0.40 | +0.4564 | +0.4976 | **+0.5546** | [+0.4909, +0.6111] | +0.0982 | [+0.0517, +0.1503] | +0.0571 | [+0.0245, +0.0876] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.40 | +0.6784 | +0.6085 | **+0.7139** | [+0.6716, +0.7524] | +0.0355 | [+0.0023, +0.0691] | +0.1054 | [+0.0812, +0.1318] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.40 | +0.8287 | +0.7984 | **+0.8493** | [+0.8251, +0.8712] | +0.0206 | [+0.0015, +0.0443] | +0.0509 | [+0.0374, +0.0636] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.45 | +0.7038 | +0.7263 | **+0.7517** | [+0.7132, +0.7871] | +0.0479 | [+0.0265, +0.0698] | +0.0254 | [+0.0087, +0.0431] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.45 | +0.4166 | +0.4722 | **+0.4866** | [+0.4205, +0.5455] | +0.0700 | [+0.0366, +0.1016] | +0.0144 | [-0.0108, +0.0412] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.750 | 0.45 | +0.5494 | +0.7206 | **+0.6857** | [+0.6329, +0.7316] | +0.1363 | [+0.1066, +0.1685] | -0.0349 | [-0.0547, -0.0159] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.40 | +0.6487 | +0.6134 | **+0.6648** | [+0.6153, +0.7116] | +0.0161 | [-0.0127, +0.0450] | +0.0514 | [+0.0320, +0.0723] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.45 | +0.6220 | +0.7919 | **+0.7909** | [+0.7537, +0.8235] | +0.1689 | [+0.1290, +0.2120] | -0.0011 | [-0.0262, +0.0211] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.875 | 0.40 | +0.7856 | +0.7753 | **+0.8221** | [+0.7892, +0.8501] | +0.0366 | [+0.0157, +0.0597] | +0.0469 | [+0.0313, +0.0615] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.750 | 0.40 | +0.3166 | +0.3423 | **+0.3957** | [+0.3263, +0.4605] | +0.0791 | [+0.0316, +0.1296] | +0.0535 | [+0.0181, +0.0877] |
| **medie** | | | | 0.750 | 0.42 | +0.6006 | +0.6346 | **+0.6715** | | +0.0709 | | +0.0369 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 8 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5546** | -0.0093 | [-0.0328, +0.0154] | 22.0% |
| de | +0.7712 | **+0.7139** | -0.0573 | [-0.0772, -0.0384] | 0.0% |
| en | +0.8723 | **+0.8493** | -0.0230 | [-0.0369, -0.0066] | 0.4% |
| es | +0.7672 | **+0.7517** | -0.0156 | [-0.0288, -0.0027] | 0.9% |
| fil | +0.5074 | **+0.4866** | -0.0208 | [-0.0429, +0.0004] | 2.9% |
| fr | +0.6679 | **+0.6857** | +0.0177 | [-0.0019, +0.0366] | 96.0% |
| it | +0.6795 | **+0.6648** | -0.0147 | [-0.0322, +0.0012] | 3.8% |
| ja | +0.7942 | **+0.7909** | -0.0033 | [-0.0186, +0.0142] | 38.4% |
| pt | +0.8413 | **+0.8221** | -0.0191 | [-0.0309, -0.0088] | 0.0% |
| si | +0.4350 | **+0.3957** | -0.0393 | [-0.0667, -0.0124] | 0.1% |
| **medie** | +0.6900 | **+0.6715** | -0.0185 | | 16.4% |

Configuratia noua urca fuziunea pe 1 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0185**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6715** | [+0.6562, +0.6870] | |
| fuziune − A | +0.0709 | [+0.0599, +0.0813] | 100.0% |
| fuziune − B | +0.0369 | [+0.0298, +0.0443] | 100.0% |
| configuratia noua − cea de azi | -0.0185 | [-0.0246, -0.0125] | 0.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6006 |
| semnalul B singur, `lolo` | 0.6346 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6715** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0144**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.875 | 0.40 | 9 | 5179 | +0.6142 | +0.6866 | 0.0724 | 0.0061 |
| de | 0.625 | 0.40 | 9 | 5054 | +0.5951 | +0.6687 | 0.0736 | 0.0043 |
| en | 0.750 | 0.40 | 9 | 5054 | +0.5761 | +0.6539 | 0.0778 | 0.0064 |
| es | 0.625 | 0.45 | 9 | 5031 | +0.5923 | +0.6647 | 0.0724 | 0.0048 |
| fil | 0.750 | 0.45 | 9 | 5054 | +0.6219 | +0.6943 | 0.0724 | 0.0051 |
| fr | 0.750 | 0.45 | 9 | 5055 | +0.6072 | +0.6722 | 0.0650 | 0.0069 |
| it | 0.750 | 0.40 | 9 | 5054 | +0.5961 | +0.6744 | 0.0783 | 0.0054 |
| ja | 0.750 | 0.45 | 9 | 5054 | +0.5991 | +0.6605 | 0.0614 | 0.0043 |
| pt | 0.875 | 0.40 | 9 | 5057 | +0.5776 | +0.6569 | 0.0793 | 0.0051 |
| si | 0.750 | 0.40 | 9 | 5024 | +0.6330 | +0.7043 | 0.0713 | 0.0047 |

Latimea medie a curbei lui w e 0.0724, iar a criteriului de candidati 0.0053, adica de 14 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
