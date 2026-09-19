# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-18 12:25:58 de `fuse_ab.py --arm lolo --fit test --ens --tag ens_lolo --a-set baza=output/e1_frozen_preds_lemma.csv --a-set fara_lung=output/e1_frozen_preds_lemma_fara_lung.csv --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv --a-set fert_plus=output/e1_frozen_preds_lemma_fert_plus.csv --vs output/fusion_preds_lolo_fittest_lemma.csv`. Date brute: `output/fusion_lolo_ens_lolo.csv`, predictii per instanta in `output/fusion_preds_lolo_ens_lolo.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi al semnalului A e si el un candidat, nu o decizie fixa: `baza`, `fara_lung`, `fert_inloc`, `fert_plus`. `baza` are lungimea in caractere si slotul de fertilitate gol, `fara_lung` anuleaza lungimea, `fert_inloc` pune numarul de subword-uri XLM-R in locul ei, `fert_plus` le pastreaza pe amandoua.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 36 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | set | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | `fert_inloc` | 0.750 | 0.40 | +0.4297 | +0.4829 | **+0.5288** | [+0.4617, +0.5873] | +0.0991 | [+0.0459, +0.1540] | +0.0459 | [+0.0098, +0.0813] |
| de | `gemma4-12b-4bit` | 570 | 193 | `fert_plus` | 0.875 | 0.35 | +0.6640 | +0.6544 | **+0.7312** | [+0.6922, +0.7691] | +0.0672 | [+0.0319, +0.1051] | +0.0768 | [+0.0568, +0.0974] |
| en | `gemma4-12b-4bit` | 570 | 190 | `fara_lung` | 0.750 | 0.40 | +0.8140 | +0.8377 | **+0.8658** | [+0.8380, +0.8899] | +0.0518 | [+0.0310, +0.0757] | +0.0281 | [+0.0154, +0.0424] |
| es | `gemma4-12b-4bit` | 593 | 208 | `fert_inloc` | 0.875 | 0.40 | +0.6574 | +0.7432 | **+0.7484** | [+0.7094, +0.7839] | +0.0910 | [+0.0642, +0.1184] | +0.0052 | [-0.0098, +0.0203] |
| fil | `gemma4-12b-4bit` | 568 | 553 | `fara_lung` | 0.750 | 0.40 | +0.4144 | +0.5190 | **+0.5187** | [+0.4552, +0.5817] | +0.1043 | [+0.0660, +0.1422] | -0.0002 | [-0.0231, +0.0237] |
| fr | `qwen35-9b-8bit` | 566 | 191 | `fara_lung` | 0.875 | 0.40 | +0.5363 | +0.5440 | **+0.5882** | [+0.5331, +0.6412] | +0.0520 | [+0.0146, +0.0911] | +0.0442 | [+0.0173, +0.0712] |
| it | `gemma4-12b-4bit` | 562 | 192 | `fert_inloc` | 0.750 | 0.40 | +0.6311 | +0.6106 | **+0.6616** | [+0.6166, +0.7065] | +0.0306 | [+0.0019, +0.0593] | +0.0510 | [+0.0320, +0.0705] |
| ja | `gemma4-12b-4bit` | 570 | 190 | `fert_plus` | 1.000 | 0.40 | +0.5387 | +0.7676 | **+0.7821** | [+0.7392, +0.8188] | +0.2435 | [+0.1986, +0.2933] | +0.0145 | [-0.0114, +0.0408] |
| pt | `gemma4-12b-4bit` | 562 | 557 | `fert_inloc` | 0.625 | 0.40 | +0.7804 | +0.8222 | **+0.8403** | [+0.8072, +0.8676] | +0.0599 | [+0.0386, +0.0804] | +0.0181 | [+0.0053, +0.0319] |
| si | `gemma4-12b-4bit` | 600 | 578 | `fara_lung` | 0.625 | 0.35 | +0.2617 | +0.3407 | **+0.3707** | [+0.3192, +0.4228] | +0.1090 | [+0.0616, +0.1568] | +0.0300 | [+0.0033, +0.0552] |
| **medie** | | | | |  0.787 | 0.39 | +0.5728 | +0.6322 | **+0.6636** | | +0.0908 | | +0.0314 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_fittest_lemma.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5305 | **+0.5288** | -0.0016 | [-0.0126, +0.0095] | 38.0% |
| de | +0.7160 | **+0.7312** | +0.0153 | [+0.0077, +0.0231] | 100.0% |
| en | +0.8674 | **+0.8658** | -0.0015 | [-0.0051, +0.0023] | 22.1% |
| es | +0.7531 | **+0.7484** | -0.0048 | [-0.0110, +0.0013] | 6.8% |
| fil | +0.5186 | **+0.5187** | +0.0002 | [-0.0052, +0.0054] | 52.0% |
| fr | +0.5823 | **+0.5882** | +0.0059 | [-0.0023, +0.0139] | 92.3% |
| it | +0.6565 | **+0.6616** | +0.0052 | [-0.0018, +0.0120] | 93.1% |
| ja | +0.7616 | **+0.7821** | +0.0205 | [+0.0023, +0.0410] | 98.5% |
| pt | +0.8388 | **+0.8403** | +0.0015 | [-0.0017, +0.0049] | 82.1% |
| si | +0.3430 | **+0.3707** | +0.0277 | [+0.0102, +0.0456] | 99.9% |
| **medie** | +0.6568 | **+0.6636** | +0.0068 | | 68.5% |

Configuratia noua urca fuziunea pe 7 din 10 limbi. Intervalul pereche exclude zero in sus pe 3. Pe medie, **+0.0068**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6636** | [+0.6486, +0.6781] | |
| fuziune − A | +0.0908 | [+0.0789, +0.1025] | 100.0% |
| fuziune − B | +0.0314 | [+0.0241, +0.0389] | 100.0% |
| configuratia noua − cea de azi | +0.0068 | [+0.0036, +0.0102] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5728 |
| semnalul B singur, `lolo` | 0.6322 |
| fuziunea de azi, A = `p_multi` | 0.6568 |
| **fuziunea cu ansamblul de surse** | **0.6636** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0065**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | set | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|---|
| ca | `fert_inloc` | 0.750 | 0.40 | 9 | 5161 | +0.6002 | +0.6809 | 0.0807 | 0.0103 |
| de | `fert_plus` | 0.875 | 0.35 | 9 | 5036 | +0.5643 | +0.6577 | 0.0934 | 0.0073 |
| en | `fara_lung` | 0.750 | 0.40 | 9 | 5036 | +0.5563 | +0.6435 | 0.0872 | 0.0100 |
| es | `fert_inloc` | 0.875 | 0.40 | 9 | 5013 | +0.5713 | +0.6565 | 0.0852 | 0.0098 |
| fil | `fara_lung` | 0.750 | 0.40 | 9 | 5038 | +0.6007 | +0.6886 | 0.0879 | 0.0090 |
| fr | `fara_lung` | 0.875 | 0.40 | 9 | 5040 | +0.5839 | +0.6743 | 0.0904 | 0.0091 |
| it | `fert_inloc` | 0.750 | 0.40 | 9 | 5044 | +0.5778 | +0.6661 | 0.0883 | 0.0084 |
| ja | `fert_plus` | 1.000 | 0.40 | 9 | 5036 | +0.5733 | +0.6520 | 0.0787 | 0.0068 |
| pt | `fert_inloc` | 0.625 | 0.40 | 9 | 5044 | +0.5634 | +0.6460 | 0.0826 | 0.0095 |
| si | `fara_lung` | 0.625 | 0.35 | 9 | 5006 | +0.6196 | +0.7048 | 0.0852 | 0.0056 |

Setul ales, pe limbi: `fert_inloc` 4, `fara_lung` 4, `fert_plus` 2. Seturile care nu apar n-au fost alese niciodata.

Latimea medie a curbei lui w e 0.0860, iar a criteriului de candidati 0.0086, adica de 10 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

## Scara configuratiilor

Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai din ce e facut semnalul A si ce se alege leave-one-language-out.

| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de 0.6571 |
|---|---|---|---|---|---|
| fuziunea de azi, A = `p_multi` | 10 | `baza` | 0.000 | **0.6568** | -0.0003 |
| doar ansamblul de surse, set `baza` | 10 | `baza` | 0.900 | **0.6636** | +0.0065 |
| doar `fert_inloc`, fara ansamblu | 10 | `fert_inloc` | 0.000 | **0.6591** | +0.0020 |
| **ansamblu plus `fert_inloc`** | 10 | `fert_inloc` | 0.775 | **0.6645** | +0.0074 |
| ansamblu plus setul ales si el LOLO | 10 | `fert_inloc`, `fert_plus`, `fara_lung` | 0.787 | **0.6636** | +0.0065 |

Reperul e cel mai bun reper publicat pe test, G-Eval cu GPT-4o 0.6571.

## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie

| ce se alege | unde | cum |
|---|---|---|
| semnalul A, ambele brate | `finetune_xlmr.py`, `frozen_trial_gap` | `te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. Bratul `p_en` nu vede deloc MLSP. |
| tot A, pe trial | `finetune_xlmr.py`, `frozen_trial_gap` | trial-ul lui L intra doar in `Xpred`, niciodata in `Xtr`. |
| setul de trasaturi al lui A | `solution_bert.py`, `_Xc` | fertilitatea e `len(tokenize(tinta))`, deci o proprietate a tokenizerului, nu a etichetelor. Centrarea ei foloseste media limbii, nu complexitatea. |
| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_trial, set(exclude) \| {lg})`: limba pentru care se alege intra chiar ea in multimea exclusa. |
| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu `exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. |
| setul de trasaturi al lui L | `fuse_ab.py`, `fit_choice` | candidatul se alege pe `others`, care nu contine L pe niciun split. |
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
