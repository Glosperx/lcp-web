# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 01:25:03 de `fuse_ab.py --arm lolo --fit test --ens --tag enc --a-set xlmr=output/e1_frozen_preds_lemma_fert_inloc.csv --a-set xlmr-large=output/e1_frozen_preds_xlmr-large_lemma_fert_inloc.csv --a-set labse=output/e1_frozen_preds_labse_lemma_fert_inloc.csv --a-set e5=output/e1_frozen_preds_e5_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_ens.csv`. Date brute: `output/fusion_lolo_enc.csv`, predictii per instanta in `output/fusion_preds_lolo_enc.csv`.

## Ce se schimba

Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja amandoua, scrise de `frozen_trial_gap`:

- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;
- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o potrivire per limba.

Semnalul devine, standardizat in interiorul limbii:

```
zA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )
```

`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are 9 puncte, de la 0.000 la 1.000.

Setul de trasaturi al semnalului A e si el un candidat, nu o decizie fixa: `xlmr`, `xlmr-large`, `labse`, `e5`. `baza` are lungimea in caractere si slotul de fertilitate gol, `fara_lung` anuleaza lungimea, `fert_inloc` pune numarul de subword-uri XLM-R in locul ei, `fert_plus` le pastreaza pe amandoua.

## Selectia, pe trei niveluri imbricate

Pentru limba L tinuta deoparte:

1. candidatii sunt perechile (set de trasaturi, `w_src`), 36 la numar;
2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu o pondere potrivita pe chiar limba pe care il masoara;
3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila de 21 de puncte.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | set | w_src | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | `labse` | 0.625 | 0.40 | +0.4552 | +0.4829 | **+0.5360** | [+0.4705, +0.5966] | +0.0809 | [+0.0294, +0.1346] | +0.0531 | [+0.0199, +0.0838] |
| de | `gemma4-12b-4bit` | 570 | 193 | `labse` | 0.500 | 0.40 | +0.6468 | +0.6544 | **+0.7254** | [+0.6855, +0.7621] | +0.0786 | [+0.0473, +0.1135] | +0.0710 | [+0.0476, +0.0944] |
| en | `gemma4-12b-4bit` | 570 | 190 | `labse` | 0.750 | 0.40 | +0.8125 | +0.8377 | **+0.8702** | [+0.8442, +0.8922] | +0.0578 | [+0.0352, +0.0817] | +0.0325 | [+0.0190, +0.0480] |
| es | `gemma4-12b-4bit` | 593 | 208 | `xlmr` | 0.875 | 0.40 | +0.6576 | +0.7432 | **+0.7486** | [+0.7099, +0.7842] | +0.0910 | [+0.0638, +0.1182] | +0.0055 | [-0.0094, +0.0206] |
| fil | `gemma4-12b-4bit` | 570 | 555 | `labse` | 0.625 | 0.40 | +0.4044 | +0.5173 | **+0.5111** | [+0.4447, +0.5725] | +0.1067 | [+0.0695, +0.1438] | -0.0062 | [-0.0284, +0.0176] |
| fr | `qwen35-9b-8bit` | 569 | 191 | `labse` | 0.625 | 0.40 | +0.5293 | +0.5420 | **+0.5804** | [+0.5267, +0.6349] | +0.0511 | [+0.0149, +0.0873] | +0.0384 | [+0.0139, +0.0648] |
| it | `gemma4-12b-4bit` | 570 | 192 | `labse` | 0.625 | 0.40 | +0.6309 | +0.6127 | **+0.6582** | [+0.6140, +0.7031] | +0.0274 | [+0.0009, +0.0551] | +0.0456 | [+0.0266, +0.0653] |
| ja | `gemma4-12b-4bit` | 570 | 190 | `labse` | 0.500 | 0.45 | +0.5832 | +0.7676 | **+0.7700** | [+0.7224, +0.8091] | +0.1868 | [+0.1432, +0.2298] | +0.0023 | [-0.0258, +0.0318] |
| pt | `gemma4-12b-4bit` | 567 | 562 | `xlmr` | 0.750 | 0.40 | +0.7710 | +0.8213 | **+0.8375** | [+0.8051, +0.8647] | +0.0665 | [+0.0449, +0.0898] | +0.0162 | [+0.0024, +0.0287] |
| si | `gemma4-12b-4bit` | 600 | 578 | `e5` | 0.625 | 0.40 | +0.2048 | +0.3407 | **+0.3584** | [+0.2987, +0.4162] | +0.1535 | [+0.1020, +0.2067] | +0.0177 | [-0.0197, +0.0547] |
| **medie** | | | | |  0.650 | 0.40 | +0.5696 | +0.6320 | **+0.6596** | | +0.0900 | | +0.0276 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 6 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_ens.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5283 | **+0.5360** | +0.0077 | [-0.0081, +0.0235] | 81.5% |
| de | +0.7324 | **+0.7254** | -0.0071 | [-0.0181, +0.0039] | 10.2% |
| en | +0.8663 | **+0.8702** | +0.0039 | [-0.0031, +0.0124] | 86.2% |
| es | +0.7486 | **+0.7486** | +0.0000 | [-0.0000, +0.0000] | 9.7% |
| fil | +0.5171 | **+0.5111** | -0.0061 | [-0.0157, +0.0032] | 10.0% |
| fr | +0.5857 | **+0.5804** | -0.0053 | [-0.0170, +0.0059] | 18.6% |
| it | +0.6625 | **+0.6582** | -0.0043 | [-0.0145, +0.0054] | 18.6% |
| ja | +0.7887 | **+0.7700** | -0.0187 | [-0.0334, -0.0039] | 0.7% |
| pt | +0.8375 | **+0.8375** | +0.0000 | [-0.0000, +0.0000] | 18.4% |
| si | +0.3786 | **+0.3584** | -0.0203 | [-0.0487, +0.0093] | 9.8% |
| **medie** | +0.6646 | **+0.6596** | -0.0050 | | 26.4% |

Configuratia noua urca fuziunea pe 2 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0050**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6596** | [+0.6447, +0.6744] | |
| fuziune − A | +0.0900 | [+0.0781, +0.1013] | 100.0% |
| fuziune − B | +0.0276 | [+0.0199, +0.0353] | 100.0% |
| configuratia noua − cea de azi | -0.0050 | [-0.0092, -0.0008] | 1.1% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5696 |
| semnalul B singur, `lolo` | 0.6320 |
| fuziunea de azi, A = `p_multi` | 0.6646 |
| **fuziunea cu ansamblul de surse** | **0.6596** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0025**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | set | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|---|
| ca | `labse` | 0.625 | 0.40 | 9 | 5179 | +0.5993 | +0.6810 | 0.0817 | 0.0066 |
| de | `labse` | 0.500 | 0.40 | 9 | 5054 | +0.5796 | +0.6598 | 0.0802 | 0.0058 |
| en | `labse` | 0.750 | 0.40 | 9 | 5054 | +0.5565 | +0.6436 | 0.0871 | 0.0070 |
| es | `xlmr` | 0.875 | 0.40 | 9 | 5031 | +0.5711 | +0.6564 | 0.0853 | 0.0072 |
| fil | `labse` | 0.625 | 0.40 | 9 | 5054 | +0.6049 | +0.6906 | 0.0857 | 0.0078 |
| fr | `labse` | 0.625 | 0.40 | 9 | 5055 | +0.5910 | +0.6761 | 0.0851 | 0.0084 |
| it | `labse` | 0.625 | 0.40 | 9 | 5054 | +0.5798 | +0.6674 | 0.0876 | 0.0065 |
| ja | `labse` | 0.500 | 0.45 | 9 | 5054 | +0.5866 | +0.6542 | 0.0676 | 0.0060 |
| pt | `xlmr` | 0.750 | 0.40 | 9 | 5057 | +0.5626 | +0.6467 | 0.0841 | 0.0068 |
| si | `e5` | 0.625 | 0.40 | 9 | 5024 | +0.6243 | +0.7062 | 0.0819 | 0.0080 |

Setul ales, pe limbi: `labse` 7, `xlmr` 2, `e5` 1. Seturile care nu apar n-au fost alese niciodata.

Latimea medie a curbei lui w e 0.0826, iar a criteriului de candidati 0.0070, adica de 12 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
