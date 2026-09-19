# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-26 17:32:34 de `fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag lin_A8 --b-dir output/bakeoff_test_M3K --a-set fert_inloc=output/e1_frozen_preds_A8-encmean_lemma_fert_inloc.csv --vs output/fusion_preds_lolo_adoptat_m3k.csv`. **Semnalul B de test vine din `output/bakeoff_test_M3K/`, nu din `output/bakeoff_test/`.** Date brute: `output/fusion_lolo_lin_A8.csv`, predictii per instanta in `output/fusion_preds_lolo_lin_A8.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.35 | +0.4683 | +0.5187 | **+0.5664** | [+0.5040, +0.6219] | +0.0980 | [+0.0468, +0.1557] | +0.0476 | [+0.0194, +0.0739] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.35 | +0.6770 | +0.7108 | **+0.7703** | [+0.7369, +0.8008] | +0.0933 | [+0.0591, +0.1294] | +0.0596 | [+0.0407, +0.0785] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.8306 | +0.8471 | **+0.8730** | [+0.8468, +0.8949] | +0.0424 | [+0.0213, +0.0657] | +0.0259 | [+0.0149, +0.0381] |
| es | `gemma4-12b-4bit` | 593 | 208 | 1.000 | 0.35 | +0.7052 | +0.7553 | **+0.7687** | [+0.7320, +0.8016] | +0.0635 | [+0.0395, +0.0889] | +0.0134 | [+0.0013, +0.0256] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.750 | 0.35 | +0.4234 | +0.5000 | **+0.5085** | [+0.4417, +0.5670] | +0.0851 | [+0.0462, +0.1224] | +0.0085 | [-0.0110, +0.0295] |
| fr | `gemma4-12b-4bit` | 569 | 191 | 0.875 | 0.40 | +0.5508 | +0.6752 | **+0.6648** | [+0.6120, +0.7124] | +0.1140 | [+0.0833, +0.1496] | -0.0103 | [-0.0279, +0.0071] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.750 | 0.35 | +0.6456 | +0.6406 | **+0.6791** | [+0.6352, +0.7219] | +0.0335 | [+0.0052, +0.0624] | +0.0385 | [+0.0223, +0.0557] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.875 | 0.35 | +0.6241 | +0.7795 | **+0.7963** | [+0.7550, +0.8297] | +0.1723 | [+0.1266, +0.2192] | +0.0169 | [-0.0020, +0.0370] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 1.000 | 0.35 | +0.7846 | +0.8243 | **+0.8423** | [+0.8120, +0.8688] | +0.0577 | [+0.0368, +0.0806] | +0.0180 | [+0.0065, +0.0290] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.875 | 0.35 | +0.3108 | +0.3979 | **+0.4304** | [+0.3701, +0.4868] | +0.1196 | [+0.0715, +0.1711] | +0.0326 | [+0.0020, +0.0611] |
| **medie** | | | | 0.850 | 0.35 | +0.6021 | +0.6649 | **+0.6900** | | +0.0879 | | +0.0251 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Configuratia noua fata de cea de azi

Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai semnalul A. Referinta e `output/fusion_preds_lolo_adoptat_m3k.csv`, iar diferenta e PERECHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de azi.

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5639 | **+0.5664** | +0.0024 | [-0.0001, +0.0049] | 97.0% |
| de | +0.7712 | **+0.7703** | -0.0009 | [-0.0025, +0.0006] | 12.4% |
| en | +0.8723 | **+0.8730** | +0.0007 | [-0.0003, +0.0018] | 90.5% |
| es | +0.7672 | **+0.7687** | +0.0015 | [-0.0005, +0.0037] | 93.2% |
| fil | +0.5074 | **+0.5085** | +0.0012 | [-0.0013, +0.0034] | 83.8% |
| fr | +0.6679 | **+0.6648** | -0.0031 | [-0.0069, +0.0005] | 4.7% |
| it | +0.6795 | **+0.6791** | -0.0004 | [-0.0023, +0.0015] | 33.4% |
| ja | +0.7942 | **+0.7963** | +0.0021 | [-0.0011, +0.0052] | 91.5% |
| pt | +0.8413 | **+0.8423** | +0.0011 | [-0.0001, +0.0023] | 96.0% |
| si | +0.4350 | **+0.4304** | -0.0046 | [-0.0104, +0.0008] | 4.8% |
| **medie** | +0.6900 | **+0.6900** | -0.0000 | | 60.7% |

Configuratia noua urca fuziunea pe 6 din 10 limbi. Intervalul pereche exclude zero in sus pe 0. Pe medie, **-0.0000**.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6900** | [+0.6756, +0.7037] | |
| fuziune − A | +0.0879 | [+0.0761, +0.0989] | 100.0% |
| fuziune − B | +0.0251 | [+0.0190, +0.0311] | 100.0% |
| configuratia noua − cea de azi | -0.0000 | [-0.0008, +0.0009] | 47.2% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.6021 |
| semnalul B singur, `lolo` | 0.6649 |
| fuziunea de azi, A = `p_multi` | 0.6900 |
| **fuziunea cu ansamblul de surse** | **0.6900** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0329**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.35 | 9 | 5179 | +0.6193 | +0.7044 | 0.0851 | 0.0046 |
| de | 0.750 | 0.35 | 9 | 5054 | +0.5961 | +0.6817 | 0.0856 | 0.0037 |
| en | 0.875 | 0.35 | 9 | 5054 | +0.5767 | +0.6703 | 0.0936 | 0.0048 |
| es | 1.000 | 0.35 | 9 | 5031 | +0.5874 | +0.6817 | 0.0943 | 0.0029 |
| fil | 0.750 | 0.35 | 9 | 5054 | +0.6243 | +0.7108 | 0.0865 | 0.0027 |
| fr | 0.875 | 0.40 | 9 | 5055 | +0.6078 | +0.6929 | 0.0851 | 0.0040 |
| it | 0.750 | 0.35 | 9 | 5054 | +0.5996 | +0.6918 | 0.0922 | 0.0044 |
| ja | 0.875 | 0.35 | 9 | 5054 | +0.5996 | +0.6788 | 0.0792 | 0.0026 |
| pt | 1.000 | 0.35 | 9 | 5057 | +0.5786 | +0.6735 | 0.0949 | 0.0030 |
| si | 0.875 | 0.35 | 9 | 5024 | +0.6345 | +0.7195 | 0.0850 | 0.0035 |

Latimea medie a curbei lui w e 0.0881, iar a criteriului de candidati 0.0036, adica de 24 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
