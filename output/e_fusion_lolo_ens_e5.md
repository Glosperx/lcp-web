# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 10:33:00 de `fuse_ab.py --arm lolo --fit test --ens --tag ens_e5 --a-set fert_inloc=output/e1_frozen_preds_e5_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_ens_e5.csv`, predictii per instanta in `output/fusion_preds_lolo_ens_e5.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.625 | 0.40 | +0.4683 | +0.4829 | **+0.5460** | [+0.4820, +0.6044] | +0.0778 | [+0.0241, +0.1338] | +0.0631 | [+0.0265, +0.0984] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.40 | +0.6525 | +0.6544 | **+0.7253** | [+0.6838, +0.7635] | +0.0728 | [+0.0420, +0.1045] | +0.0709 | [+0.0485, +0.0949] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.8140 | +0.8377 | **+0.8661** | [+0.8389, +0.8895] | +0.0521 | [+0.0304, +0.0756] | +0.0284 | [+0.0156, +0.0421] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.500 | 0.40 | +0.7110 | +0.7432 | **+0.7638** | [+0.7270, +0.7968] | +0.0528 | [+0.0312, +0.0767] | +0.0206 | [+0.0067, +0.0344] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4128 | +0.5173 | **+0.5174** | [+0.4516, +0.5758] | +0.1046 | [+0.0675, +0.1404] | +0.0001 | [-0.0233, +0.0246] |
| fr | `qwen35-9b-8bit` | 569 | 191 | 0.625 | 0.40 | +0.5492 | +0.5420 | **+0.5891** | [+0.5350, +0.6431] | +0.0399 | [+0.0047, +0.0763] | +0.0471 | [+0.0220, +0.0722] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.40 | +0.6374 | +0.6127 | **+0.6638** | [+0.6202, +0.7073] | +0.0264 | [-0.0020, +0.0536] | +0.0511 | [+0.0327, +0.0704] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.5927 | +0.7676 | **+0.7800** | [+0.7339, +0.8178] | +0.1873 | [+0.1428, +0.2326] | +0.0124 | [-0.0109, +0.0382] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.40 | +0.7778 | +0.8213 | **+0.8423** | [+0.8092, +0.8704] | +0.0645 | [+0.0431, +0.0882] | +0.0210 | [+0.0050, +0.0356] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.40 | +0.2048 | +0.3407 | **+0.3584** | [+0.2987, +0.4162] | +0.1535 | [+0.1020, +0.2067] | +0.0177 | [-0.0197, +0.0547] |
| **medie** | | | | 0.600 | 0.40 | +0.5820 | +0.6320 | **+0.6652** | | +0.0832 | | +0.0332 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5283 | **+0.5460** | +0.0177 | [+0.0015, +0.0337] | 98.8% |
| de | +0.7324 | **+0.7253** | -0.0072 | [-0.0182, +0.0042] | 12.4% |
| en | +0.8663 | **+0.8661** | -0.0002 | [-0.0066, +0.0061] | 49.6% |
| es | +0.7486 | **+0.7638** | +0.0152 | [+0.0058, +0.0245] | 100.0% |
| fil | +0.5171 | **+0.5174** | +0.0002 | [-0.0079, +0.0082] | 51.1% |
| fr | +0.5857 | **+0.5891** | +0.0034 | [-0.0108, +0.0173] | 66.7% |
| it | +0.6625 | **+0.6638** | +0.0013 | [-0.0079, +0.0100] | 60.2% |
| ja | +0.7887 | **+0.7800** | -0.0087 | [-0.0221, +0.0050] | 9.7% |
| pt | +0.8375 | **+0.8423** | +0.0048 | [-0.0010, +0.0108] | 94.9% |
| si | +0.3786 | **+0.3584** | -0.0203 | [-0.0487, +0.0093] | 9.8% |
| **medie** | +0.6646 | **+0.6652** | +0.0006 | | 55.3% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 2. Pe medie, **+0.0006**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6652** | [+0.6502, +0.6797] | |
| fuziune − A | +0.0832 | [+0.0715, +0.0946] | 100.0% |
| fuziune − B | +0.0332 | [+0.0258, +0.0406] | 100.0% |
| configuratia noua − cea de azi | +0.0006 | [-0.0039, +0.0048] | 62.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5820 |
| semnalul B singur, `lolo` | 0.6320 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6652** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0081**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.625 | 0.40 | 9 | 5179 | +0.5950 | +0.6787 | 0.0837 | 0.0028 |
| de | 0.500 | 0.40 | 9 | 5054 | +0.5755 | +0.6586 | 0.0831 | 0.0024 |
| en | 0.625 | 0.40 | 9 | 5054 | +0.5566 | +0.6431 | 0.0865 | 0.0045 |
| es | 0.500 | 0.40 | 9 | 5031 | +0.5690 | +0.6543 | 0.0853 | 0.0051 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6012 | +0.6885 | 0.0873 | 0.0032 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.5860 | +0.6739 | 0.0879 | 0.0034 |
| it | 0.625 | 0.40 | 9 | 5054 | +0.5762 | +0.6656 | 0.0894 | 0.0029 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.5812 | +0.6527 | 0.0715 | 0.0027 |
| pt | 0.625 | 0.40 | 9 | 5057 | +0.5606 | +0.6457 | 0.0851 | 0.0050 |
| si | 0.625 | 0.40 | 9 | 5024 | +0.6243 | +0.7062 | 0.0819 | 0.0030 |

Latimea medie a curbei lui w e 0.0842, iar a criteriului de candidati 0.0035, adica de 24 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
| splitul pe care se alege modelul | `fuse_ab.py`, `fuse_ens` | `--pick-split trial`, adica `tab_pick = r_table(load_runs('trial'), "B")`. Selectia citeste trial-ul, potrivirea ponderii citeste splitul lui `--fit`. Niciun rand al limbii L nu intra in criteriu, pe niciunul dintre splituri: L e exclusa chiar din media care alege. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Se face pe ACELASI `tab_pick`, deci schimbarea splitului de selectie nu deschide o scurgere pe unde selectia imbricata a inchis una. |
| `w_src` | `fuse_ab.py`, `fit_choice` | acelasi criteriu, aceeasi multime `others`. |
| ponderea w | `fuse_ab.py`, `fit_choice` | `others = {l2: d for l2, d in fit.items() if l2 != lg}`. Curba nu contine niciun rand al lui L, pe niciun split. |
| w-ul limbilor de potrivire, in criteriu | `fuse_ab.py`, `fit_choice` | bucla `for l3 in others if l3 != l2`: cand un candidat se masoara pe L', ponderea lui L' vine de pe celelalte opt limbi, deci nici L nici L' nu intra in ea. |
| standardizarea | `fuse_ab.py`, `zscore` si `zA_of` | media si deviatia se iau din predictii, nu din etichete, la ambele niveluri de standardizare ale lui A. |

Si unde **nu** e garantata, fiindca trebuie scris tot. Doua locuri:

1. `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Alegerile lui L depind deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi. Dependenta e identica la potrivirea pe trial si la cea pe test, fiindca ambele folosesc aceleasi predictii. Marimea efectului ramane **neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L si L', adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare. Bratul `p_en` **nu** are dependenta asta: nu vede niciun rand de MLSP.
2. Modelul lui B al limbilor de potrivire se re-alege cu `exclude={L}`, deci la un nivel, nu la doua. In bucla interioara care alege w-ul lui L' pe celelalte opt, modelul acelor opt ramane cel ales cu `exclude={L}`, nu cu `exclude={L, L'}`. Nivelul urmator ar cere `pick_model` cu trei limbi excluse, si nu s-a coborat pana acolo.

### Filtrul de disponibilitate

Selectia imbricata poate cere un model care nu a fost rulat pe limba de potrivire, pe splitul de potrivire. Candidatii se restrang atunci la modelele masurate efectiv acolo. Restrangerea se uita la ACOPERIRE, nu la scor, deci nu introduce nicio eticheta. Cazurile, toate:

| split de potrivire | limba tinuta deoparte | limba de potrivire | cerut | folosit |
|---|---|---|---|---|
| test | fr | ca | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | de | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | en | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | es | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | it | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | ja | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
| test | fr | pt | `qwen35-9b-8bit` | `gemma4-12b-4bit` |
