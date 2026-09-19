# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 22:25:59 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag obi_C6 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encZC6_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_obi_C6.csv`, predictii per instanta in `output/fusion_preds_lolo_obi_C6.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.35 | +0.4786 | +0.5187 | **+0.5682** | [+0.5068, +0.6223] | +0.0896 | [+0.0385, +0.1440] | +0.0495 | [+0.0227, +0.0763] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.35 | +0.6561 | +0.7108 | **+0.7575** | [+0.7225, +0.7894] | +0.1014 | [+0.0676, +0.1368] | +0.0467 | [+0.0291, +0.0644] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.35 | +0.8363 | +0.8471 | **+0.8744** | [+0.8484, +0.8962] | +0.0381 | [+0.0187, +0.0592] | +0.0273 | [+0.0161, +0.0397] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.500 | 0.35 | +0.7067 | +0.7553 | **+0.7685** | [+0.7317, +0.8013] | +0.0618 | [+0.0385, +0.0867] | +0.0132 | [+0.0018, +0.0247] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.35 | +0.4197 | +0.5000 | **+0.5059** | [+0.4415, +0.5654] | +0.0861 | [+0.0469, +0.1238] | +0.0058 | [-0.0144, +0.0268] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.40 | +0.5586 | +0.6752 | **+0.6682** | [+0.6156, +0.7152] | +0.1097 | [+0.0792, +0.1441] | -0.0069 | [-0.0251, +0.0104] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.500 | 0.35 | +0.6267 | +0.6406 | **+0.6742** | [+0.6297, +0.7179] | +0.0475 | [+0.0176, +0.0781] | +0.0336 | [+0.0164, +0.0516] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.500 | 0.40 | +0.6396 | +0.7795 | **+0.7925** | [+0.7525, +0.8247] | +0.1529 | [+0.1129, +0.1926] | +0.0131 | [-0.0058, +0.0327] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.500 | 0.35 | +0.7843 | +0.8243 | **+0.8401** | [+0.8105, +0.8670] | +0.0558 | [+0.0365, +0.0780] | +0.0158 | [+0.0049, +0.0262] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.3540 | +0.3979 | **+0.4369** | [+0.3791, +0.4884] | +0.0829 | [+0.0409, +0.1284] | +0.0390 | [+0.0141, +0.0625] |
| **medie** | | | | 0.550 | 0.36 | +0.6061 | +0.6649 | **+0.6886** | | +0.0826 | | +0.0237 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5682** | +0.0043 | [-0.0039, +0.0131] | 84.4% |
| de | +0.7712 | **+0.7575** | -0.0138 | [-0.0194, -0.0081] | 0.0% |
| en | +0.8723 | **+0.8744** | +0.0020 | [-0.0008, +0.0049] | 93.0% |
| es | +0.7672 | **+0.7685** | +0.0013 | [-0.0036, +0.0065] | 68.7% |
| fil | +0.5074 | **+0.5059** | -0.0015 | [-0.0086, +0.0052] | 33.5% |
| fr | +0.6679 | **+0.6682** | +0.0003 | [-0.0063, +0.0070] | 53.4% |
| it | +0.6795 | **+0.6742** | -0.0053 | [-0.0111, +0.0004] | 3.5% |
| ja | +0.7942 | **+0.7925** | -0.0017 | [-0.0125, +0.0095] | 39.7% |
| pt | +0.8413 | **+0.8401** | -0.0012 | [-0.0042, +0.0019] | 22.6% |
| si | +0.4350 | **+0.4369** | +0.0019 | [-0.0157, +0.0186] | 56.8% |
| **medie** | +0.6900 | **+0.6886** | -0.0014 | | 45.6% |

Configuratia noua urca fuziunea pe 5 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0014**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6886** | [+0.6744, +0.7023] | |
| fuziune − A | +0.0826 | [+0.0716, +0.0930] | 100.0% |
| fuziune − B | +0.0237 | [+0.0181, +0.0292] | 100.0% |
| configuratia noua − cea de azi | -0.0014 | [-0.0040, +0.0012] | 14.6% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6061 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6886** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0315**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.35 | 9 | 5179 | +0.6212 | +0.7032 | 0.0820 | 0.0029 |
| de | 0.500 | 0.35 | 9 | 5054 | +0.6017 | +0.6822 | 0.0805 | 0.0018 |
| en | 0.625 | 0.35 | 9 | 5054 | +0.5815 | +0.6692 | 0.0877 | 0.0020 |
| es | 0.500 | 0.35 | 9 | 5031 | +0.5960 | +0.6810 | 0.0850 | 0.0006 |
| fil | 0.500 | 0.35 | 9 | 5054 | +0.6279 | +0.7102 | 0.0823 | 0.0013 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.6123 | +0.6918 | 0.0795 | 0.0019 |
| it | 0.500 | 0.35 | 9 | 5054 | +0.6049 | +0.6915 | 0.0866 | 0.0016 |
| ja | 0.500 | 0.40 | 9 | 5054 | +0.6035 | +0.6780 | 0.0745 | 0.0010 |
| pt | 0.500 | 0.35 | 9 | 5057 | +0.5874 | +0.6731 | 0.0857 | 0.0003 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6351 | +0.7178 | 0.0827 | 0.0021 |

Latimea medie a curbei lui w e 0.0827, iar a criteriului de candidati 0.0016, adica de 53 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
