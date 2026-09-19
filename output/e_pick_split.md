# P1. Selectia modelului lui B, mutata de pe trial pe splitul de evaluare

Generat 2026-08-19 10:31:41 de `analysis_pick_split.py`. Nicio inferenta LLM, nicio cifra recalculata aici: cele doua configuratii vin din `fuse_ab.py`, iar diferentele se construiesc din predictiile lor per instanta. Date brute: `output/pick_split.csv`, o linie per limba.

```
azi  fuse_ab.py --arm lolo --fit test --ens --tag ens \
         --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv \
         --vs output/fusion_preds_lolo_fittest_lemma.csv
nou  fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag ens_picktest \
         --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv \
         --vs output/fusion_preds_lolo_ens.csv
```

## Ce se schimba, si numai atat

`fuse_ab.py` alegea modelul lui B din tabelul de **trial**, prin `pick_model(tab_pick, ...)` in `load_signals`, in timp ce ponderea `w` se potrivea pe **test**, prin `--fit test`. Asimetria e exact cea pe care docstringul fisierului o condamna cand motiveaza `--fit test`: cele doua componente ale aceluiasi sistem foloseau splituri diferite fara motiv. Motivul fusese eliminat pentru `w` si ramasese pentru model.

Sub `--pick-split test`, selectia pentru limba L se face pe randurile de TEST ale **celorlalte 9 limbi**, exact ca `w` si exact ca antrenarea bratului A, unde `Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` ruleaza peste aceleasi randuri de test. Zero etichete din L, la niciun nivel. Selectia imbricata a limbilor de potrivire foloseste acelasi tabel, deci nu se deschide o scurgere pe unde s-a inchis una. Garantiile linie cu linie sunt in tabelul de audit din `output/e_fusion_lolo_picktest.md`, care are acum si randul splitului de selectie.

**Distinctia care trebuie tinuta curata:** o selectie recalculata pe testul limbii **L** ar fi tuning pe scorul raportat, si comentariul din `bakeoff_trial.aggregate` are dreptate cand o refuza. Asta nu e aia. Aici L e exclusa chiar din media care alege, ca peste tot altundeva in protocol.

## Rezultatul, diferente PERECHE pe contexte

Aceleasi randuri de test pe ambele brate, verificat rand cu rand pe `idx`. 2000 de reesantionari ale CONTEXTELOR prin `mlsp_common.boot_r_ci`, cu acelasi seed si acelasi vector de contexte, deci reesantionarea k e aceeasi pe ambele configuratii si intervalul e al diferentei, nu al sumei incertitudinilor.

| limba | n | ctx | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.5283 | **+0.5246** | -0.0037 | [-0.0087, +0.0016] | 8.5% |
| de | 570 | 193 | +0.7324 | **+0.7324** | +0.0000 | [+0.0000, +0.0000] | identic |
| en | 570 | 190 | +0.8663 | **+0.8635** | -0.0028 | [-0.0048, -0.0009] | 0.1% |
| es | 593 | 208 | +0.7486 | **+0.7495** | +0.0008 | [-0.0001, +0.0018] | 95.3% |
| fil | 570 | 555 | +0.5171 | **+0.5171** | +0.0000 | [+0.0000, +0.0000] | identic |
| fr | 569 | 191 | +0.5857 | **+0.6440** | +0.0583 | [+0.0309, +0.0869] | 100.0% |
| it | 570 | 192 | +0.6625 | **+0.6591** | -0.0034 | [-0.0061, -0.0008] | 0.6% |
| ja | 570 | 190 | +0.7887 | **+0.7910** | +0.0024 | [-0.0015, +0.0063] | 88.0% |
| pt | 567 | 562 | +0.8375 | **+0.8374** | -0.0001 | [-0.0007, +0.0005] | 35.1% |
| si | 600 | 578 | +0.3786 | **+0.3786** | +0.0000 | [+0.0000, +0.0000] | identic |
| **medie** | 5624 | | +0.664581 | **+0.669735** | +0.005154 | [+0.0023, +0.0081] | 100.0% |

Dintre cele 10 limbi, 3 raman **identice rand cu rand** (de, fil, si): acolo se alegea deja acelasi model, acelasi set, acelasi `w_src` si acelasi `w`, deci predictiile nu se schimba deloc. Din restul, 3 urca si 4 coboara. Intervalul pereche exclude zero in sus pe 1 si in jos pe 2 (en, it), iar scaderile alea se raporteaza ca atare: sunt mici, en -0.0028, it -0.0034, si vin din `w_src` si `w`, care se re-aleg pe un set de potrivire in care franceza si-a schimbat modelul. Intervalul mediei se construieste mediind cele zece limbi la fiecare reesantionare, deci e o distributie a mediei, nu o medie de distributii; r-ul nou singur are [+0.6548, +0.6839].

**Franceza duce singura schimbarea:** +0.5857 -> +0.6440, adica +0.0583, cu interval [+0.0309, +0.0869] si P(>0) = 100.0%. E limba despre care `output/repere_publicate.md` spune ca explica singura tot deficitul fata de reperele publicate. Celelalte noua se misca doar prin `w_src` si `w`, care se re-aleg pe un set de potrivire in care franceza are alt model, iar acele miscari sunt de ordinul a cateva miimi, in ambele sensuri.

## Harta model-per-limba

Sub protocolul corect selectia **degenereaza la un singur model peste toate limbile**.

| limba | model ales pe trial | model ales pe test |
|---|---|---|
| ca | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| de | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| en | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| es | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| fil | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| fr | `qwen35-9b-8bit` | `gemma4-12b-4bit`  <- se schimba |
| it | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| ja | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| pt | `gemma4-12b-4bit` | `gemma4-12b-4bit` |
| si | `gemma4-12b-4bit` | `gemma4-12b-4bit` |

### Ce inseamna pentru revendicarea de noutate

Revendicarea „LOLO inclusiv la alegerea modelului" devine: **mecanismul de selectie exista si, pe splitul corect, alege acelasi model peste tot; selectia facuta pe trial e cea care difera, si e cea care costa 0.100 r pe franceza la semnalul B**, adica +0.0583 la fuziune. Asta e un rezultat, nu o pierdere. E a doua demonstratie a tezei ca trial-ul e un proxy prost pentru test pe semnalul B, prima fiind decalajul masurat in `output/e_split_gap.md`. Mecanismul ramane necesar in lucrare, fiindca fara el nu se poate arata ca alegerea e stabila; ce nu se mai poate revendica e o harta neomogena de modele.

## Cat de lat e criteriul care alege

`latime criteriu` e r maxim minus r minim peste candidatii pe care `pick_model` ii vede efectiv pentru limba L, unde valoarea unui candidat e media lui r peste celelalte 9 limbi. Cu cat e mai lata, cu atat argmaxul separa ceva real si nu zgomot.

| limba | candidati | criteriul castigatorului | cel mai slab | latime | toti candidatii |
|---|---|---|---|---|---|
| ca | 2 | +0.6597 | +0.3876 | **0.2721** | `gemma4-12b-4bit` +0.660, `qwen3-8b-4bit` +0.388 |
| de | 2 | +0.6406 | +0.3779 | **0.2628** | `gemma4-12b-4bit` +0.641, `qwen3-8b-4bit` +0.378 |
| en | 2 | +0.6203 | +0.3727 | **0.2475** | `gemma4-12b-4bit` +0.620, `qwen3-8b-4bit` +0.373 |
| es | 2 | +0.6308 | +0.3737 | **0.2571** | `gemma4-12b-4bit` +0.631, `qwen3-8b-4bit` +0.374 |
| fil | 2 | +0.6559 | +0.3615 | **0.2943** | `gemma4-12b-4bit` +0.656, `qwen3-8b-4bit` +0.362 |
| fr | 2 | +0.6420 | +0.3713 | **0.2706** | `gemma4-12b-4bit` +0.642, `qwen3-8b-4bit` +0.371 |
| it | 2 | +0.6453 | +0.3708 | **0.2744** | `gemma4-12b-4bit` +0.645, `qwen3-8b-4bit` +0.371 |
| ja | 2 | +0.6281 | +0.3653 | **0.2628** | `gemma4-12b-4bit` +0.628, `qwen3-8b-4bit` +0.365 |
| pt | 2 | +0.6221 | +0.3617 | **0.2604** | `gemma4-12b-4bit` +0.622, `qwen3-8b-4bit` +0.362 |
| si | 2 | +0.6755 | +0.4003 | **0.2752** | `gemma4-12b-4bit` +0.675, `qwen3-8b-4bit` +0.400 |
| **medie** | 2.0 | +0.6420 | +0.3743 | **0.2677** | |

### Aceeasi regula, doua verdicte opuse, si amandoua masurate

Regula transversala a proiectului e „cand criteriul e plat, mediaza, nu alege". Aici ea spune **selecteaza**, si o spune cu cifre:

| alegere | latime criteriu | latime curba `w` | raport | verdictul regulii |
|---|---|---|---|---|
| modelul lui B, pe test | **0.2677** | 0.0888 | de 3.0 ori mai LAT | selecteaza |
| encoderul, §3.6 | 0.0077 | 0.082 | de 10.6 ori mai plat | mediaza |

Cele doua randuri vin din aceeasi regula aplicata la doua alegeri diferite si dau verdicte opuse, fiecare confirmat de masuratoare: la encodere selectia chiar a cazut si medierea a castigat, aici selectia chiar separa si franceza urca. O regula care ar spune acelasi lucru peste tot n-ar spune nimic.

## Limitare, declarata fara sa fie intrebat nimeni

Bazinul de pe splitul de test nu e cel de pe trial. Acoperirea, masurata:

| model | limbi pe test | unde |
|---|---|---|
| `qwen3-8b-4bit` | 10 | ca, de, en, es, fil, fr, it, ja, pt, si |
| `gemma4-12b-4bit` | 10 | ca, de, en, es, fil, fr, it, ja, pt, si |
| `qwen35-9b-8bit` | 1 | fr |

`qwen35-9b-8bit` e rulat pe test **doar pe franceza**, deci pentru fiecare limba bazinul are efectiv 2 candidati, nu 3. Un reviewer poate spune, pe drept, „ati selectat pe test dintre modelele pe care s-a intamplat sa le rulati pe test". Restrangerea nu foloseste nicio eticheta, e o constatare de acoperire, dar ingusteaza alegerea si trebuie scrisa ca limitare, nu ca detaliu.

Reparatia e o rulare separata a lui `qwen35-9b-8bit` pe testul complet, ~75 de minute de inferenta la 0.78 s per item pe cele 5055 de instante ramase, si **cere aprobarea lui Alexandru**. Pana atunci cifra de mai sus se citeaza cu bazinul declarat.

Al doilea lucru de tinut minte: pe trial bazinul e mai larg, cu 7 modele pe toate cele 10 limbi, iar acolo criteriul are alta forma. Latimea lui pe trial e 0.1734 in medie, dar **nicio cifra de trial nu se citeaza ca predictie pentru test**: decalajul dintre splituri e masurat, depinde de semnal si de model, si are semne opuse.

## Ce nu s-a facut

Nu s-a adoptat nimic. Implicitul lui `--pick-split` ramane `trial`, deci sistemul publicat, 0.664581, reproduce bit cu bit fara niciun flag, verificat cu `cmp` pe `fusion_lolo_ens.csv` si `fusion_preds_lolo_ens.csv`. Cifra noua sta pe tagul ei, `ens_picktest`. Adoptia se face intr-un singur eveniment de renumerotare, impreuna cu media de encodere si cu fixul de caz din `find_char_span`.
