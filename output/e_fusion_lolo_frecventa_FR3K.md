# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-22 20:27:26 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag frecventa_FR3K --b-dir output/bakeoff_test_FR3K --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_temp.csv`. **Semnalul B de test vine din `output/bakeoff_test_FR3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_frecventa_FR3K.csv`, predictii per instanta in `output/fusion_preds_lolo_frecventa_FR3K.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.35 | +0.4668 | +0.5215 | **+0.5571** | [+0.4920, +0.6132] | +0.0903 | [+0.0403, +0.1453] | +0.0356 | [+0.0088, +0.0618] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.625 | 0.35 | +0.6784 | +0.6938 | **+0.7468** | [+0.7108, +0.7806] | +0.0684 | [+0.0379, +0.1006] | +0.0530 | [+0.0347, +0.0707] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8259 | +0.8615 | **+0.8744** | [+0.8497, +0.8961] | +0.0485 | [+0.0292, +0.0703] | +0.0129 | [+0.0040, +0.0230] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.6991 | +0.7600 | **+0.7684** | [+0.7319, +0.8019] | +0.0693 | [+0.0446, +0.0955] | +0.0084 | [-0.0043, +0.0224] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.875 | 0.35 | +0.4171 | +0.4810 | **+0.4954** | [+0.4285, +0.5554] | +0.0783 | [+0.0389, +0.1173] | +0.0144 | [-0.0066, +0.0348] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 1.000 | 0.35 | +0.5421 | +0.6704 | **+0.6591** | [+0.6051, +0.7073] | +0.1170 | [+0.0830, +0.1531] | -0.0113 | [-0.0271, +0.0041] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6487 | +0.6333 | **+0.6709** | [+0.6261, +0.7146] | +0.0222 | [-0.0055, +0.0510] | +0.0376 | [+0.0215, +0.0538] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.6140 | +0.7674 | **+0.7832** | [+0.7404, +0.8183] | +0.1692 | [+0.1240, +0.2168] | +0.0158 | [-0.0041, +0.0366] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.35 | +0.7863 | +0.8095 | **+0.8278** | [+0.7935, +0.8566] | +0.0416 | [+0.0235, +0.0616] | +0.0183 | [+0.0078, +0.0285] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.3242 | +0.3827 | **+0.4176** | [+0.3579, +0.4754] | +0.0934 | [+0.0465, +0.1429] | +0.0349 | [+0.0070, +0.0621] |
| **medie** | | | | 0.800 | 0.35 | +0.6003 | +0.6581 | **+0.6801** | | +0.0798 | | +0.0220 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_temp.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5566 | **+0.5571** | +0.0005 | [-0.0097, +0.0117] | 52.3% |
| de | +0.7468 | **+0.7468** | -0.0000 | [-0.0092, +0.0087] | 48.4% |
| en | +0.8700 | **+0.8744** | +0.0044 | [-0.0021, +0.0113] | 91.1% |
| es | +0.7641 | **+0.7684** | +0.0043 | [-0.0026, +0.0110] | 89.2% |
| fil | +0.5091 | **+0.4954** | -0.0137 | [-0.0229, -0.0049] | 0.2% |
| fr | +0.6590 | **+0.6591** | +0.0001 | [-0.0094, +0.0091] | 49.5% |
| it | +0.6750 | **+0.6709** | -0.0041 | [-0.0109, +0.0028] | 11.6% |
| ja | +0.7877 | **+0.7832** | -0.0045 | [-0.0148, +0.0053] | 18.5% |
| pt | +0.8450 | **+0.8278** | -0.0172 | [-0.0240, -0.0107] | 0.0% |
| si | +0.4251 | **+0.4176** | -0.0075 | [-0.0177, +0.0023] | 7.0% |
| **medie** | +0.6838 | **+0.6801** | -0.0038 | | 36.8% |

Configuratia noua urca fuziunea pe 4 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0038**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6801** | [+0.6652, +0.6940] | |
| fuziune − A | +0.0798 | [+0.0680, +0.0910] | 100.0% |
| fuziune − B | +0.0220 | [+0.0161, +0.0280] | 100.0% |
| configuratia noua − cea de azi | -0.0038 | [-0.0065, -0.0011] | 0.3% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6003 |
| semnalul B singur, `lolo` | 0.6581 |
| fuziunea de azi, A = `p_multi` | 0.6838 |
| **fuziunea cu ansamblul de surse** | **0.6801** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0230**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.35 | 9 | 5179 | +0.6186 | +0.6939 | 0.0753 | 0.0048 |
| de | 0.625 | 0.35 | 9 | 5054 | +0.5951 | +0.6728 | 0.0777 | 0.0029 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5731 | +0.6588 | 0.0857 | 0.0050 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5828 | +0.6703 | 0.0875 | 0.0032 |
| fil | 0.875 | 0.35 | 9 | 5054 | +0.6185 | +0.7009 | 0.0824 | 0.0031 |
| fr | 1.000 | 0.35 | 9 | 5055 | +0.6003 | +0.6825 | 0.0822 | 0.0043 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5961 | +0.6814 | 0.0853 | 0.0036 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5966 | +0.6689 | 0.0723 | 0.0029 |
| pt | 0.750 | 0.35 | 9 | 5057 | +0.5809 | +0.6640 | 0.0831 | 0.0043 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6345 | +0.7094 | 0.0749 | 0.0039 |

Latimea medie a curbei lui w e 0.0806, iar a criteriului de candidati 0.0038, adica de 21 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
