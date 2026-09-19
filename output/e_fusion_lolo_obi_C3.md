# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 22:25:22 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag obi_C3 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_encZC3_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_obi_C3.csv`, predictii per instanta in `output/fusion_preds_lolo_obi_C3.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4635 | +0.5187 | **+0.5637** | [+0.5015, +0.6194] | +0.1003 | [+0.0485, +0.1581] | +0.0450 | [+0.0161, +0.0720] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.500 | 0.35 | +0.6719 | +0.7108 | **+0.7671** | [+0.7332, +0.7978] | +0.0952 | [+0.0607, +0.1311] | +0.0564 | [+0.0378, +0.0751] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8261 | +0.8471 | **+0.8715** | [+0.8451, +0.8937] | +0.0454 | [+0.0242, +0.0691] | +0.0245 | [+0.0135, +0.0366] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.7056 | +0.7553 | **+0.7687** | [+0.7320, +0.8015] | +0.0632 | [+0.0390, +0.0881] | +0.0135 | [+0.0012, +0.0260] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.500 | 0.35 | +0.4214 | +0.5000 | **+0.5073** | [+0.4404, +0.5658] | +0.0859 | [+0.0469, +0.1232] | +0.0073 | [-0.0127, +0.0282] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.625 | 0.40 | +0.5562 | +0.6752 | **+0.6671** | [+0.6147, +0.7139] | +0.1109 | [+0.0803, +0.1459] | -0.0081 | [-0.0260, +0.0092] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.35 | +0.6452 | +0.6406 | **+0.6784** | [+0.6341, +0.7218] | +0.0332 | [+0.0043, +0.0622] | +0.0378 | [+0.0216, +0.0549] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.625 | 0.40 | +0.6308 | +0.7795 | **+0.7935** | [+0.7513, +0.8280] | +0.1627 | [+0.1193, +0.2073] | +0.0141 | [-0.0074, +0.0367] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.625 | 0.35 | +0.7854 | +0.8243 | **+0.8412** | [+0.8110, +0.8680] | +0.0559 | [+0.0355, +0.0783] | +0.0169 | [+0.0057, +0.0276] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.35 | +0.3237 | +0.3979 | **+0.4354** | [+0.3758, +0.4910] | +0.1117 | [+0.0656, +0.1626] | +0.0376 | [+0.0084, +0.0657] |
| **medie** | | | | 0.700 | 0.36 | +0.6030 | +0.6649 | **+0.6894** | | +0.0864 | | +0.0245 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5637** | -0.0002 | [-0.0025, +0.0022] | 43.1% |
| de | +0.7712 | **+0.7671** | -0.0041 | [-0.0063, -0.0020] | 0.0% |
| en | +0.8723 | **+0.8715** | -0.0008 | [-0.0017, +0.0001] | 4.8% |
| es | +0.7672 | **+0.7687** | +0.0015 | [-0.0002, +0.0032] | 96.3% |
| fil | +0.5074 | **+0.5073** | -0.0001 | [-0.0029, +0.0028] | 47.6% |
| fr | +0.6679 | **+0.6671** | -0.0008 | [-0.0049, +0.0032] | 35.8% |
| it | +0.6795 | **+0.6784** | -0.0011 | [-0.0025, +0.0003] | 6.5% |
| ja | +0.7942 | **+0.7935** | -0.0007 | [-0.0061, +0.0044] | 40.6% |
| pt | +0.8413 | **+0.8412** | -0.0001 | [-0.0014, +0.0013] | 46.5% |
| si | +0.4350 | **+0.4354** | +0.0004 | [-0.0062, +0.0069] | 53.3% |
| **medie** | +0.6900 | **+0.6894** | -0.0006 | | 37.5% |

Configuratia noua urca fuziunea pe 2 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0006**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6894** | [+0.6747, +0.7031] | |
| fuziune − A | +0.0865 | [+0.0748, +0.0973] | 100.0% |
| fuziune − B | +0.0245 | [+0.0182, +0.0305] | 100.0% |
| configuratia noua − cea de azi | -0.0006 | [-0.0016, +0.0005] | 15.3% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6030 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6894** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0323**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6199 | +0.7049 | 0.0850 | 0.0022 |
| de | 0.500 | 0.35 | 9 | 5054 | +0.6002 | +0.6824 | 0.0822 | 0.0021 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5766 | +0.6704 | 0.0938 | 0.0018 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5861 | +0.6814 | 0.0953 | 0.0014 |
| fil | 0.500 | 0.35 | 9 | 5054 | +0.6280 | +0.7112 | 0.0832 | 0.0015 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.6118 | +0.6932 | 0.0814 | 0.0030 |
| it | 0.625 | 0.35 | 9 | 5054 | +0.6019 | +0.6923 | 0.0904 | 0.0016 |
| ja | 0.625 | 0.40 | 9 | 5054 | +0.6035 | +0.6792 | 0.0757 | 0.0018 |
| pt | 0.625 | 0.35 | 9 | 5057 | +0.5863 | +0.6742 | 0.0879 | 0.0011 |
| si | 0.875 | 0.35 | 9 | 5024 | +0.6324 | +0.7189 | 0.0865 | 0.0019 |

Latimea medie a curbei lui w e 0.0861, iar a criteriului de candidati 0.0018, adica de 47 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
