# Fuziunea A plus B, brat `lolo`, semnalul A ca ansamblu de surse

Generat 2026-08-19 01:22:50 de `fuse_ab.py --arm lolo --fit test --ens --tag ens --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv`. Date brute: `output/fusion_lolo_ens.csv`, predictii per instanta in `output/fusion_preds_lolo_ens.csv`.

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
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.750 | 0.40 | +0.4279 | +0.4829 | **+0.5283** | [+0.4605, +0.5867] | +0.1004 | [+0.0463, +0.1557] | +0.0454 | [+0.0090, +0.0813] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.750 | 0.35 | +0.6677 | +0.6544 | **+0.7324** | [+0.6939, +0.7699] | +0.0647 | [+0.0309, +0.1024] | +0.0780 | [+0.0580, +0.0984] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.750 | 0.40 | +0.8158 | +0.8377 | **+0.8663** | [+0.8384, +0.8904] | +0.0505 | [+0.0298, +0.0741] | +0.0286 | [+0.0160, +0.0427] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.875 | 0.40 | +0.6576 | +0.7432 | **+0.7486** | [+0.7099, +0.7842] | +0.0910 | [+0.0638, +0.1182] | +0.0055 | [-0.0094, +0.0206] |
| fil | `gemma4-12b-4bit` | 570 | 555 | 0.625 | 0.40 | +0.4149 | +0.5173 | **+0.5171** | [+0.4522, +0.5765] | +0.1022 | [+0.0639, +0.1378] | -0.0001 | [-0.0231, +0.0240] |
| fr | `qwen35-9b-8bit` | 569 | 191 | 0.625 | 0.40 | +0.5375 | +0.5420 | **+0.5857** | [+0.5316, +0.6395] | +0.0482 | [+0.0110, +0.0878] | +0.0437 | [+0.0173, +0.0707] |
| it | `gemma4-12b-4bit` | 570 | 192 | 0.625 | 0.40 | +0.6339 | +0.6127 | **+0.6625** | [+0.6173, +0.7078] | +0.0286 | [+0.0011, +0.0559] | +0.0499 | [+0.0312, +0.0694] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 1.000 | 0.40 | +0.6004 | +0.7676 | **+0.7887** | [+0.7451, +0.8262] | +0.1882 | [+0.1445, +0.2354] | +0.0210 | [-0.0037, +0.0463] |
| pt | `gemma4-12b-4bit` | 567 | 562 | 0.750 | 0.40 | +0.7710 | +0.8213 | **+0.8375** | [+0.8051, +0.8647] | +0.0665 | [+0.0449, +0.0898] | +0.0162 | [+0.0024, +0.0287] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.625 | 0.35 | +0.2858 | +0.3407 | **+0.3786** | [+0.3273, +0.4306] | +0.0928 | [+0.0471, +0.1405] | +0.0379 | [+0.0116, +0.0635] |
| **medie** | | | | 0.738 | 0.39 | +0.5813 | +0.6320 | **+0.6646** | | +0.0833 | | +0.0326 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 9 din 10. Intervalul exclude zero pe 10 limbi fata de A si pe 7 fata de B.

## Intervalele mediei, nu ale limbilor

Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.

| ce se compara | pe medie | CI 95% | P(>0) |
|---|---|---|---|
| r al fuziunii | **+0.6646** | [+0.6496, +0.6789] | |
| fuziune − A | +0.0833 | [+0.0711, +0.0950] | 100.0% |
| fuziune − B | +0.0326 | [+0.0254, +0.0398] | 100.0% |

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, ansamblul de surse | 0.5813 |
| semnalul B singur, `lolo` | 0.6320 |
| **fuziunea cu ansamblul de surse** | **0.6646** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0075**. Trecem de el.

## Ce s-a ales, si cat de plata e alegerea

`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel mai slab.

| limba | w_src | w | limbi fit | itemi fit | curba w min | curba w max | latime w | latime criteriu |
|---|---|---|---|---|---|---|---|---|
| ca | 0.750 | 0.40 | 9 | 5179 | +0.6008 | +0.6811 | 0.0803 | 0.0065 |
| de | 0.750 | 0.35 | 9 | 5054 | +0.5741 | +0.6578 | 0.0837 | 0.0036 |
| en | 0.750 | 0.40 | 9 | 5054 | +0.5577 | +0.6435 | 0.0858 | 0.0068 |
| es | 0.875 | 0.40 | 9 | 5031 | +0.5711 | +0.6564 | 0.0853 | 0.0069 |
| fil | 0.625 | 0.40 | 9 | 5054 | +0.6049 | +0.6886 | 0.0837 | 0.0052 |
| fr | 0.625 | 0.40 | 9 | 5055 | +0.5913 | +0.6745 | 0.0832 | 0.0056 |
| it | 0.625 | 0.40 | 9 | 5054 | +0.5806 | +0.6660 | 0.0854 | 0.0053 |
| ja | 1.000 | 0.40 | 9 | 5054 | +0.5720 | +0.6514 | 0.0794 | 0.0039 |
| pt | 0.750 | 0.40 | 9 | 5057 | +0.5626 | +0.6467 | 0.0841 | 0.0068 |
| si | 0.625 | 0.35 | 9 | 5024 | +0.6192 | +0.7040 | 0.0848 | 0.0020 |

Latimea medie a curbei lui w e 0.0836, iar a criteriului de candidati 0.0053, adica de 16 ori mai mica. Alegerea candidatului e deci mult mai plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi directie, dar marginea e subtire si o parte din ea e zgomot.

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
