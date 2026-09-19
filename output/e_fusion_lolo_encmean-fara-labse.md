# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 01:25:26 de `fuse_ab.py --arm lolo --fit test --ens --tag encmean-fara-labse --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-labse_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_encmean-fara-labse.csv`, predictii per instanta in `output/fusion_preds_lolo_encmean-fara-labse.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.45 | +0.4746 | +0.4829 | **+0.5442** | [+0.4781, +0.6024] | +0.0697 | [+0.0248, +0.1164] | +0.0613 | [+0.0217, +0.1002] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.40 | +0.6921 | +0.6544 | **+0.7392** | [+0.7015, +0.7756] | +0.0472 | [+0.0181, +0.0775] | +0.0848 | [+0.0639, +0.1069] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.45 | +0.8343 | +0.8377 | **+0.8714** | [+0.8450, +0.8939] | +0.0372 | [+0.0190, +0.0565] | +0.0337 | [+0.0203, +0.0493] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.625 | 0.45 | +0.6973 | +0.7432 | **+0.7568** | [+0.7183, +0.7915] | +0.0594 | [+0.0382, +0.0807] | +0.0136 | [-0.0015, +0.0289] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.45 | +0.4067 | +0.5173 | **+0.5098** | [+0.4426, +0.5695] | +0.1031 | [+0.0679, +0.1364] | -0.0075 | [-0.0344, +0.0203] |
| fr | `qwen35-9b-8bit` | 569 | 191 | 0.750 | 0.45 | +0.5617 | +0.5420 | **+0.5952** | [+0.5412, +0.6486] | +0.0334 | [+0.0020, +0.0657] | +0.0532 | [+0.0255, +0.0812] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.45 | +0.6516 | +0.6127 | **+0.6690** | [+0.6241, +0.7140] | +0.0174 | [-0.0075, +0.0435] | +0.0563 | [+0.0352, +0.0778] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.45 | +0.6450 | +0.7676 | **+0.7876** | [+0.7437, +0.8245] | +0.1427 | [+0.1063, +0.1803] | +0.0200 | [-0.0052, +0.0470] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.500 | 0.45 | +0.7898 | +0.8213 | **+0.8419** | [+0.8088, +0.8696] | +0.0521 | [+0.0336, +0.0732] | +0.0207 | [+0.0050, +0.0355] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.40 | +0.3053 | +0.3407 | **+0.3856** | [+0.3303, +0.4383] | +0.0804 | [+0.0407, +0.1239] | +0.0449 | [+0.0143, +0.0747] |
| **medie** | | | | 0.662 | 0.44 | +0.6058 | +0.6320 | **+0.6701** | | +0.0643 | | +0.0381 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 9 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5283 | **+0.5442** | +0.0159 | [+0.0065, +0.0248] | 100.0% |
| de | +0.7324 | **+0.7392** | +0.0068 | [+0.0018, +0.0120] | 99.4% |
| en | +0.8663 | **+0.8714** | +0.0051 | [+0.0011, +0.0093] | 99.7% |
| es | +0.7486 | **+0.7568** | +0.0081 | [+0.0030, +0.0134] | 100.0% |
| fil | +0.5171 | **+0.5098** | -0.0074 | [-0.0139, -0.0007] | 1.6% |
| fr | +0.5857 | **+0.5952** | +0.0095 | [+0.0017, +0.0169] | 99.1% |
| it | +0.6625 | **+0.6690** | +0.0065 | [+0.0010, +0.0121] | 98.7% |
| ja | +0.7887 | **+0.7876** | -0.0010 | [-0.0083, +0.0064] | 39.9% |
| pt | +0.8375 | **+0.8419** | +0.0044 | [+0.0005, +0.0086] | 98.7% |
| si | +0.3786 | **+0.3856** | +0.0070 | [-0.0086, +0.0220] | 81.2% |
| **medie** | +0.6646 | **+0.6701** | +0.0055 | | 81.8% |

Configuratia noua urca fuziunea pe 8 din 10 limbi. Intervalul pereche exclude zero in sus pe 7. Pe medie, **+0.0055**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6701** | [+0.6551, +0.6841] | |
| fuziune − A | +0.0643 | [+0.0539, +0.0741] | 100.0% |
| fuziune − B | +0.0381 | [+0.0302, +0.0457] | 100.0% |
| configuratia noua − cea de azi | +0.0055 | [+0.0030, +0.0079] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6058 |
| semnalul B singur, `lolo` | 0.6320 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6701** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0130**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.45 | 9 | 5179 | +0.6197 | +0.6847 | 0.0650 | 0.0044 |
| de | 0.750 | 0.40 | 9 | 5054 | +0.5956 | +0.6627 | 0.0671 | 0.0030 |
| en | 0.625 | 0.45 | 9 | 5054 | +0.5818 | +0.6483 | 0.0665 | 0.0050 |
| es | 0.625 | 0.45 | 9 | 5031 | +0.5970 | +0.6611 | 0.0641 | 0.0060 |
| fil | 0.625 | 0.45 | 9 | 5054 | +0.6293 | +0.6944 | 0.0651 | 0.0043 |
| fr | 0.750 | 0.45 | 9 | 5055 | +0.6100 | +0.6790 | 0.0690 | 0.0046 |
| it | 0.625 | 0.45 | 9 | 5054 | +0.6021 | +0.6708 | 0.0687 | 0.0037 |
| ja | 0.750 | 0.45 | 9 | 5054 | +0.6008 | +0.6577 | 0.0569 | 0.0035 |
| pt | 0.500 | 0.45 | 9 | 5057 | +0.5876 | +0.6512 | 0.0636 | 0.0054 |
| si | 0.625 | 0.40 | 9 | 5024 | +0.6405 | +0.7084 | 0.0679 | 0.0024 |

Latimea medie a curbei lui w e 0.0654, iar a criteriului de candidati 0.0042, adica de 15 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
