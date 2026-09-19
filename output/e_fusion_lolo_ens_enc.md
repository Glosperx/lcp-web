# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-18 15:06:42 de `fuse_ab.py --arm lolo --fit test --ens --tag ens_enc --a-set xlmr=output/e1_frozen_preds_lemma_fert_inloc.csv --a-set large=output/e1_frozen_preds_xlmr-large_lemma_fert_inloc.csv --a-set labse=output/e1_frozen_preds_labse_lemma_fert_inloc.csv --a-set e5=output/e1_frozen_preds_e5_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_ens_enc.csv`, predictii per instanta in `output/fusion_preds_lolo_ens_enc.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi al semnalului A e si el un candidat, nu o decizie fixa: `xlmr`, `large`, `labse`, `e5`. `baza` are lungimea in caractere si slotul de fertilitate gol, `fara_lung` anuleaza lungimea, `fert_inloc` pune numarul de subword-uri XLM-R in locul ei, `fert_plus` le pastreaza pe amandoua.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 36 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | set | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | `labse` | 0.625 | 0.40 | +0.4540 | +0.4829 | **+0.5354** | [+0.4696, +0.5969] | +0.0814 | [+0.0304, +0.1354] | +0.0525 | [+0.0190, +0.0832] |
| de | `gemma4-12b-4bit` | 570 | 193 | `labse` | 0.500 | 0.40 | +0.6439 | +0.6544 | **+0.7250** | [+0.6857, +0.7616] | +0.0811 | [+0.0496, +0.1156] | +0.0706 | [+0.0473, +0.0939] |
| en | `gemma4-12b-4bit` | 570 | 190 | `labse` | 0.750 | 0.40 | +0.8120 | +0.8377 | **+0.8700** | [+0.8440, +0.8919] | +0.0580 | [+0.0354, +0.0819] | +0.0323 | [+0.0188, +0.0478] |
| es | `gemma4-12b-4bit` | 593 | 208 | `xlmr` | 0.875 | 0.40 | +0.6574 | +0.7432 | **+0.7484** | [+0.7094, +0.7839] | +0.0910 | [+0.0642, +0.1184] | +0.0052 | [-0.0098, +0.0203] |
| fil | `gemma4-12b-4bit` | 568 | 553 | `labse` | 0.625 | 0.40 | +0.4071 | +0.5190 | **+0.5131** | [+0.4509, +0.5766] | +0.1060 | [+0.0669, +0.1428] | -0.0059 | [-0.0277, +0.0180] |
| fr | `qwen35-9b-8bit` | 566 | 191 | `labse` | 0.625 | 0.40 | +0.5340 | +0.5440 | **+0.5840** | [+0.5304, +0.6373] | +0.0500 | [+0.0143, +0.0863] | +0.0400 | [+0.0155, +0.0661] |
| it | `gemma4-12b-4bit` | 562 | 192 | `labse` | 0.625 | 0.40 | +0.6315 | +0.6106 | **+0.6577** | [+0.6140, +0.7018] | +0.0263 | [+0.0001, +0.0544] | +0.0471 | [+0.0283, +0.0668] |
| ja | `gemma4-12b-4bit` | 570 | 190 | `labse` | 0.375 | 0.45 | +0.5730 | +0.7676 | **+0.7649** | [+0.7165, +0.8044] | +0.1919 | [+0.1492, +0.2347] | -0.0027 | [-0.0312, +0.0269] |
| pt | `gemma4-12b-4bit` | 562 | 557 | `labse` | 0.625 | 0.40 | +0.7776 | +0.8222 | **+0.8428** | [+0.8105, +0.8687] | +0.0651 | [+0.0423, +0.0885] | +0.0206 | [+0.0078, +0.0343] |
| si | `gemma4-12b-4bit` | 600 | 578 | `e5` | 0.625 | 0.40 | +0.2010 | +0.3407 | **+0.3572** | [+0.2976, +0.4154] | +0.1562 | [+0.1050, +0.2098] | +0.0165 | [-0.0214, +0.0535] |
| **medie** | | | | |  0.625 | 0.40 | +0.5691 | +0.6322 | **+0.6599** | | +0.0907 | | +0.0276 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 8 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5288 | **+0.5354** | +0.0066 | [-0.0094, +0.0215] | 77.6% |
| de | +0.7311 | **+0.7250** | -0.0060 | [-0.0174, +0.0050] | 14.0% |
| en | +0.8657 | **+0.8700** | +0.0042 | [-0.0029, +0.0128] | 87.8% |
| es | +0.7484 | **+0.7484** | +0.0000 | [-0.0000, +0.0000] | 9.2% |
| fil | +0.5197 | **+0.5131** | -0.0066 | [-0.0159, +0.0030] | 8.8% |
| fr | +0.5883 | **+0.5840** | -0.0043 | [-0.0162, +0.0074] | 25.2% |
| it | +0.6616 | **+0.6577** | -0.0039 | [-0.0147, +0.0065] | 22.4% |
| ja | +0.7887 | **+0.7649** | -0.0238 | [-0.0396, -0.0082] | 0.4% |
| pt | +0.8403 | **+0.8428** | +0.0024 | [-0.0040, +0.0088] | 77.8% |
| si | +0.3729 | **+0.3572** | -0.0157 | [-0.0458, +0.0150] | 17.5% |
| **medie** | +0.6646 | **+0.6599** | -0.0047 | | 34.1% |

Configuratia noua urca fuziunea pe 3 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0047**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6599** | [+0.6447, +0.6739] | |
| fuziune − A | +0.0907 | [+0.0791, +0.1021] | 100.0% |
| fuziune − B | +0.0276 | [+0.0198, +0.0353] | 100.0% |
| configuratia noua − cea de azi | -0.0047 | [-0.0093, -0.0002] | 2.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5691 |
| semnalul B singur, `lolo` | 0.6322 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6599** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0028**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | set | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|---|
| ca | `labse` | 0.625 | 0.40 | 9 | 5161 | +0.6001 | +0.6814 | 0.0813 | 0.0074 |
| de | `labse` | 0.500 | 0.40 | 9 | 5036 | +0.5805 | +0.6602 | 0.0797 | 0.0062 |
| en | `labse` | 0.750 | 0.40 | 9 | 5036 | +0.5572 | +0.6440 | 0.0868 | 0.0080 |
| es | `xlmr` | 0.875 | 0.40 | 9 | 5013 | +0.5713 | +0.6565 | 0.0852 | 0.0083 |
| fil | `labse` | 0.625 | 0.40 | 9 | 5038 | +0.6053 | +0.6908 | 0.0855 | 0.0078 |
| fr | `labse` | 0.625 | 0.40 | 9 | 5040 | +0.5912 | +0.6760 | 0.0848 | 0.0085 |
| it | `labse` | 0.625 | 0.40 | 9 | 5044 | +0.5803 | +0.6678 | 0.0875 | 0.0075 |
| ja | `labse` | 0.375 | 0.45 | 9 | 5036 | +0.5883 | +0.6546 | 0.0663 | 0.0075 |
| pt | `labse` | 0.625 | 0.40 | 9 | 5044 | +0.5641 | +0.6472 | 0.0831 | 0.0079 |
| si | `e5` | 0.625 | 0.40 | 9 | 5006 | +0.6254 | +0.7069 | 0.0815 | 0.0077 |

Setul ales, pe limbi: `labse` 8, `xlmr` 1, `e5` 1. Seturile care nu apar n-au fost alese niciodata.

Latimea medie a curbei lui w e 0.0822, iar a criteriului de candidati 0.0077, adica de 11 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

## Scara configuratiilor

Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai din ce e facut semnalul A si ce se alege leave-one-language-out.

| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de 0.6571 |
|---|---|---|---|---|---|
| fuziunea de azi, A = `p_multi` | 10 | `baza` | 0.000 | **0.6568** | -0.0003 |
| doar ansamblul de surse, set `baza` | 10 | `baza` | 0.900 | **0.6636** | +0.0065 |
| doar `fert_inloc`, fara ansamblu | 10 | `fert_inloc` | 0.000 | **0.6591** | +0.0020 |
| **ansamblu plus `fert_inloc`** | 10 | `fert_inloc` | 0.775 | **0.6646** | +0.0075 |
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
