# Distributia peste 1..5, masurata ca semnal

Generat 2026-08-20 01:10:06 de `analysis_dist.py`. Date: `output/dist/gemma4-12b-4bit_test.csv` (distributiile salvate de `rate_parts`, aceeasi rulare care reproduce bit cu bit coloana B din `output/bakeoff_test/gemma4-12b-4bit.csv`) si `output/fusion_preds_lolo_adoptat.csv` (predictiile per instanta ale sistemului de 0.674946). Nicio inferenta LLM: tot ce urmeaza e aritmetica peste cifre deja masurate.

Semnalul B al sistemului vine de la `gemma4-12b-4bit` pe toate cele zece limbi, ales leave-one-language-out pe test (`output/e_fusion_lolo_adoptat.md`), deci distributiile unui singur model acopera tot sistemul.

**Nimic de aici nu e adoptat.** Cifra publicata ramane 0.674946, produsa de comanda din `output/e_fusion_lolo_adoptat.md`, nemodificata.

## (a) Linia de baza se reproduce

B se reconstruieste din coloanele noi cu aceeasi aritmetica din `solution_bert._score_msgs`: media pe cele doua prompturi a `((sum p_i * i) - 1) / 4`. Daca nu iese coloana B, restul raportului nu inseamna nimic si nu se scrie.

- randuri: **5624**, din care **5624** identice cu coloana `B` la 8 zecimale
- abaterea maxima: **5.000e-09**, adica rotunjirea la 8 zecimale cu care coloana e scrisa pe disc (`f"{b:.8f}"`), nu o pierdere de precizie: probabilitatile sunt scrise cu `repr(float)`, care face roundtrip exact
- r per limba fata de cel publicat in `output/fusion_lolo_adoptat.csv`: abatere maxima **2.22e-16**

## (b) Temperatura, linia de baza imprumutata de la G-Scale

`p_T` proportional cu `p^(1/T)`, renormalizat, apoi aceeasi valoare asteptata si aceeasi mediere pe cele doua prompturi. E chiar softmax-ul cu temperatura al lui G-Scale: `softmax(logit/T)` e proportional cu `exp(logit)^(1/T)`, iar p e deja normalizat peste cele cinci cifre. Constructia coincide literal, nu doar in spirit: `output/d4_sanity.md` arata ca `gemma4-12b-4bit` are cate un SINGUR id per cifra, deci p_i nu aduna nimic si temperatura cade pe logiti, nu pe o distributie agregata. Grila: `0.5`, `0.75`, `1`, `1.25`, `1.5`, `2`, `2.5`, `3`, `4`.

**T se alege leave-one-language-out**, cu criteriul identic in forma cu `fuse_ab.pick_model` si cu cel al lui `w`: pentru limba L, T e argmaxul mediei lui r peste randurile de test ale CELORLALTE 9 limbi. Nicio eticheta din L nu intra in alegere. La Nohejl, T = 2.0 e ales pe media trial-urilor tuturor celor 10 limbi, deci si pe a limbii evaluate.

`latime criteriu` e r maxim minus r minim pe grila, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai mult zgomot. Acelasi diagnostic ca `latime w` din `output/e_fusion_lolo_adoptat.md`.

| limba | T ales LOLO | la marginea grilei | latime criteriu | r la T=1 | r la T ales | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|---|---|---|
| ca | 4 | DA | 0.0215 | +0.4829 | +0.5115 | **+0.0286** | [+0.0096, +0.0491] | 99.9% |
| de | 4 | DA | 0.0239 | +0.6544 | +0.6682 | **+0.0138** | [+0.0009, +0.0263] | 98.0% |
| en | 4 | DA | 0.0241 | +0.8377 | +0.8468 | **+0.0091** | [+0.0009, +0.0174] | 98.4% |
| es | 4 | DA | 0.0245 | +0.7432 | +0.7491 | **+0.0059** | [-0.0026, +0.0149] | 90.8% |
| fil | 4 | DA | 0.0255 | +0.5173 | +0.5215 | **+0.0043** | [-0.0068, +0.0154] | 77.4% |
| fr | 4 | DA | 0.0225 | +0.6424 | +0.6634 | **+0.0210** | [+0.0080, +0.0344] | 100.0% |
| it | 4 | DA | 0.0230 | +0.6127 | +0.6306 | **+0.0180** | [+0.0064, +0.0287] | 99.9% |
| ja | 4 | DA | 0.0235 | +0.7676 | +0.7787 | **+0.0110** | [+0.0027, +0.0206] | 99.2% |
| pt | 4 | DA | 0.0234 | +0.8213 | +0.8350 | **+0.0137** | [+0.0062, +0.0212] | 100.0% |
| si | 4 | DA | 0.0214 | +0.3407 | +0.3741 | **+0.0334** | [+0.0168, +0.0500] | 100.0% |
| **medie** | | | | **+0.6420** | **+0.6579** | **+0.0158** | [+0.0119, +0.0198] | 100.0% |

Pe medie, temperatura aleasa LOLO **muta** semnalul B: +0.0158, interval pereche [+0.0119, +0.0198], deci **exclude zero**. Castiga pe 10 limbi din 10.

**Dar alegerea cade la marginea de sus a grilei pe 10 limbi din 10.** Un argmax pe margine nu localizeaza un optim, spune doar ca grila s-a terminat inainte de varf, si cifra de mai sus e o margine inferioara a ce poate da temperatura, nu efectul celui mai bun T. De aceea urmeaza diagnosticul cu grila extinsa. Latimea medie a criteriului e 0.0233.

### Ce ar fi dat protocolul lui Nohejl, si de ce nu se raporteaza ca al nostru

Un singur T ales pe media celor 10 limbi de TEST da T = 4 si r mediu +0.6579. Cifra foloseste scorul de test al fiecarei limbi ca sa aleaga hiperparametrul limbii respective, deci e o margine superioara, la fel ca celula `oracol` din `output/e_bakeoff_test.md`, nu o alternativa disponibila sub §5.1.

Coloana `T pe L singur` de mai jos e acelasi lucru dus la capat, per limba, si spune cat pierde protocolul: T ales chiar pe limba evaluata.

| limba | T ales LOLO | r sub LOLO | T ales pe L insasi | r acolo | pretul protocolului |
|---|---|---|---|---|---|
| ca | 4 | +0.5115 | 4 | +0.5115 | +0.0000 |
| de | 4 | +0.6682 | 4 | +0.6682 | +0.0000 |
| en | 4 | +0.8468 | 4 | +0.8468 | +0.0000 |
| es | 4 | +0.7491 | 4 | +0.7491 | +0.0000 |
| fil | 4 | +0.5215 | 4 | +0.5215 | +0.0000 |
| fr | 4 | +0.6634 | 4 | +0.6634 | +0.0000 |
| it | 4 | +0.6306 | 4 | +0.6306 | +0.0000 |
| ja | 4 | +0.7787 | 3 | +0.7792 | -0.0005 |
| pt | 4 | +0.8350 | 4 | +0.8350 | +0.0000 |
| si | 4 | +0.3741 | 4 | +0.3741 | +0.0000 |
| **medie** | | **+0.6579** | | **+0.6579** | **-0.0001** |

### Grila specificata se termina inainte de varf

Sectiunea asta e un DIAGNOSTIC, si exista pentru un singur motiv: argmaxul de mai sus a cazut la marginea de sus pe zece limbi din zece. Nu s-a extins grila fiindca rezultatul ar fi fost nesatisfacator, ci fiindca un argmax pe margine nu localizeaza nimic. Grila extinsa e un superset strict al celei specificate, alegerea ramane leave-one-language-out, si **cifra de referinta ramane cea de pe grila specificata**.

r mediu pe cele 10 limbi, la T fix, fara nicio alegere:

| T | 0.5 | 0.75 | 1 | 1.25 | 1.5 | 2 | 2.5 | 3 | 4 | 6 | 8 | 12 | 16 | 24 | 32 | 64 | limita |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r mediu | +0.6346 | +0.6386 | +0.6420 | +0.6449 | +0.6473 | +0.6511 | +0.6537 | +0.6556 | +0.6579 | +0.6598 | +0.6604 | +0.6607 | +0.6605 | +0.6597 | +0.6590 | +0.6574 | +0.6550 |

Curba are un varf INTERIOR, la T = 12 cu +0.6607, si coboara apoi catre limita analitica +0.6550. Limita nu e o extrapolare numerica: la T mare, valoarea asteptata minus 3 e proportionala cu `sum_i (i-3) log p_i`, iar Pearson e invariant la transformari afine. Toate cele 0 celule cu p = 0 din setul intreg fac logaritmul sigur, adica nu e niciuna.

Alegerea LOLO refacuta pe grila extinsa:

| limba | T ales LOLO, extins | la marginea grilei | r la T ales | fata de T=1 | CI 95% |
|---|---|---|---|---|---|
| ca | 12 | nu | +0.5159 | +0.0330 | [+0.0084, +0.0601] |
| de | 8 | nu | +0.6812 | +0.0268 | [+0.0098, +0.0435] |
| en | 12 | nu | +0.8463 | +0.0086 | [-0.0031, +0.0200] |
| es | 12 | nu | +0.7499 | +0.0068 | [-0.0059, +0.0203] |
| fil | 16 | nu | +0.5082 | -0.0091 | [-0.0249, +0.0073] |
| fr | 12 | nu | +0.6655 | +0.0231 | [+0.0052, +0.0413] |
| it | 12 | nu | +0.6354 | +0.0227 | [+0.0053, +0.0383] |
| ja | 12 | nu | +0.7715 | +0.0038 | [-0.0081, +0.0165] |
| pt | 12 | nu | +0.8322 | +0.0109 | [+0.0004, +0.0214] |
| si | 8 | nu | +0.3860 | +0.0453 | [+0.0235, +0.0665] |
| **medie** | | | **+0.6592** | **+0.0171** | [+0.0119, +0.0227] |

Pe grila extinsa nicio limba nu mai alege marginea, iar castigul fata de T = 1 e +0.0171, interval [+0.0119, +0.0227], adica exclude zero. Diferenta fata de grila specificata, +0.0013, e mica fata de latimea intervalului: curba e practic plata intre T = 6 si T = 24, deci alegerea exacta a lui T conteaza mult mai putin decat faptul CA se aplica o temperatura.

## (c) Dezacordul modelului: alt canal, sau aceeasi medie in alta haina?

Eticheta MLSP e media notelor mai multor adnotatori, deci un cuvant pe care oamenii nu cad de acord e prin constructie un cuvant de mijloc. Daca incertitudinea capului de notare urmeaza acelasi tipar, ea ar trebui sa prezica eticheta. Intrebarea nu e daca o prezice, e daca o prezice printr-un canal DIFERIT de media distributiei, care e chiar semnalul B.

Testul nu e corelatia bruta, e **validitate incrementala**: corelatie partiala cu eticheta, cu ambele laturi rezidualizate pe acelasi control, si interval bootstrap pe CONTEXTE, 2000 de reesantionari. Acelasi tipar cu ce face `analysis_fr.py` pentru fertilitate. Reziduurile se calculeaza o data pe esantionul intreg si abia apoi se reesantioneaza, ca acolo, deci intervalul nu contine incertitudinea potrivirii controlului.

### De ce controlul liniar pe B nu e destul, si de ce e chiar controlul gresit aici

Toate cele cinci masuri sunt functii de ACEEASI distributie din care se calculeaza B. Entropia unei distributii pe 1..5 e legata mecanic de medie: o medie extrema forteaza masa spre un capat, deci entropie mica. Masa pe capete e si mai rau, coreleaza peste 0.9 cu B in toate limbile. Asta e avertismentul cerut, si coloana `r cu B` il masoara.

Dar sectiunea (b) adauga un motiv mai tare, care nu se vedea inainte de ea: temperatura imbunatateste r pe toate cele zece limbi, adica **B e misspecificat ca predictor LINIAR al etichetei**. O forma mai plata a aceleiasi distributii prezice mai bine. Atunci orice marime corelata cu curbura aia va parea ca aduce un canal nou, cand de fapt reciteste acelasi canal. Un control liniar pe B nu poate distinge cele doua lucruri. De aceea se raporteaza cinci controale, de la cel naiv la cel flexibil:

- `B`: B, liniar
- `B3`: B, B^2, B^3
- `BT`: B la temperatura aleasa LOLO
- `sys`: predictia sistemului, liniar
- `sys3`: predictia sistemului, plus patrat si cub

Un semnal care supravietuieste lui `B3` si lui `BT` spune ceva ce media distributiei nu spune, oricum ai citi-o. Unul care se stinge intre `B` si `B3` era curbura, nu canal.

### Sinteza: media pe cele 10 limbi, per control

| semnal | r brut | r cu B (mecanic) | vs `B` | vs `B3` | vs `BT` | vs `sys` | vs `sys3` |
|---|---|---|---|---|---|---|---|
| `entropie` | -0.0402 | -0.0314 | -0.0480<br>[-0.0746, -0.0219] * | -0.0086<br>[-0.0349, +0.0176] | -0.0481<br>[-0.0745, -0.0226] * | -0.0446<br>[-0.0707, -0.0174] * | -0.0212<br>[-0.0475, +0.0054] |
| `capat_sus` | +0.5982 | +0.9158 | +0.0512<br>[+0.0247, +0.0788] * | +0.0194<br>[-0.0114, +0.0499] | +0.0523<br>[+0.0248, +0.0798] * | +0.0452<br>[+0.0172, +0.0740] * | +0.0324<br>[+0.0001, +0.0649] * |
| `capat_jos` | -0.5978 | -0.9547 | +0.0685<br>[+0.0424, +0.0941] * | +0.0022<br>[-0.0253, +0.0296] | +0.0592<br>[+0.0316, +0.0863] * | +0.0232<br>[-0.0052, +0.0521] | +0.0036<br>[-0.0273, +0.0333] |
| `dezacord_E` | -0.1067 | -0.0817 | -0.0858<br>[-0.1128, -0.0577] * | -0.0434<br>[-0.0699, -0.0153] * | -0.0558<br>[-0.0825, -0.0286] * | -0.0605<br>[-0.0866, -0.0331] * | -0.0360<br>[-0.0626, -0.0086] * |
| `dezacord_JS` | -0.1194 | -0.0952 | -0.0813<br>[-0.1067, -0.0547] * | -0.0420<br>[-0.0668, -0.0150] * | -0.0529<br>[-0.0784, -0.0275] * | -0.0567<br>[-0.0820, -0.0311] * | -0.0354<br>[-0.0607, -0.0100] * |

`*` = intervalul mediei exclude zero. Intervalele sunt ale MEDIEI pe cele zece limbi: se mediaza limbile la fiecare reesantionare, ca in `fuse_ab._agg_boot`.

### `entropie`: entropia lui p, mediata pe cele doua prompturi

| limba | n | medie | r brut | r cu B | partial vs `B` | CI 95% | partial vs `B3` | CI 95% | partial vs `sys3` | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 0.383 | -0.1308 | -0.1137 | -0.0873 | [-0.1818, +0.0043] | -0.0234 | [-0.1160, +0.0656] | -0.0918 | [-0.1925, +0.0068] |
| de | 570 | 0.303 | -0.2039 | -0.3051 | -0.0059 | [-0.0936, +0.0759] | +0.1166 | [+0.0289, +0.1942] * | +0.1223 | [+0.0333, +0.2049] * |
| en | 570 | 0.252 | +0.1553 | +0.2165 | -0.0489 | [-0.1343, +0.0388] | +0.0097 | [-0.0756, +0.0933] | -0.0168 | [-0.1077, +0.0702] |
| es | 593 | 0.285 | +0.0225 | +0.1355 | -0.1180 | [-0.1972, -0.0421] * | -0.0228 | [-0.1424, +0.0829] | -0.0435 | [-0.1274, +0.0401] |
| fil | 570 | 0.338 | +0.1094 | +0.0871 | +0.0754 | [-0.0192, +0.1709] | +0.0244 | [-0.0644, +0.1143] | +0.0292 | [-0.0621, +0.1216] |
| fr | 569 | 0.274 | +0.1017 | +0.1487 | +0.0082 | [-0.0818, +0.0964] | -0.0043 | [-0.0870, +0.0790] | +0.0123 | [-0.0760, +0.1010] |
| it | 570 | 0.314 | -0.1448 | -0.1506 | -0.0673 | [-0.1421, +0.0116] | -0.0033 | [-0.0760, +0.0696] | +0.0179 | [-0.0576, +0.0932] |
| ja | 570 | 0.358 | -0.0667 | -0.0380 | -0.0586 | [-0.1490, +0.0298] | -0.0378 | [-0.1232, +0.0457] | -0.0723 | [-0.1599, +0.0130] |
| pt | 567 | 0.285 | -0.0146 | +0.0071 | -0.0357 | [-0.1233, +0.0511] | -0.0072 | [-0.0891, +0.0721] | -0.0299 | [-0.1238, +0.0575] |
| si | 600 | 0.388 | -0.2299 | -0.3010 | -0.1421 | [-0.2124, -0.0714] * | -0.1375 | [-0.2079, -0.0628] * | -0.1389 | [-0.2138, -0.0651] * |
| **medie** | 5624 | | **-0.0402** | **-0.0314** | **-0.0480** | [-0.0746, -0.0219] | **-0.0086** | [-0.0349, +0.0176] | **-0.0212** | [-0.0475, +0.0054] |

### `capat_sus`: masa pe capatul greu, `p4 + p5`, mediata pe prompturi

| limba | n | medie | r brut | r cu B | partial vs `B` | CI 95% | partial vs `B3` | CI 95% | partial vs `sys3` | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 0.348 | +0.4534 | +0.9306 | +0.0123 | [-0.0736, +0.0976] | +0.0054 | [-0.0868, +0.0962] | +0.0158 | [-0.0825, +0.1173] |
| de | 570 | 0.524 | +0.6837 | +0.9346 | +0.2682 | [+0.1929, +0.3433] * | +0.1341 | [+0.0422, +0.2260] * | +0.0633 | [-0.0211, +0.1503] |
| en | 570 | 0.128 | +0.7657 | +0.8858 | +0.0931 | [-0.0036, +0.1916] | -0.0305 | [-0.1410, +0.0792] | -0.0506 | [-0.1708, +0.0695] |
| es | 593 | 0.189 | +0.7193 | +0.9184 | +0.1389 | [+0.0565, +0.2260] * | +0.1003 | [-0.0299, +0.2315] | +0.1381 | [+0.0474, +0.2294] * |
| fil | 570 | 0.245 | +0.4178 | +0.9055 | -0.1393 | [-0.2268, -0.0514] * | -0.0706 | [-0.1695, +0.0287] | +0.0230 | [-0.0672, +0.1183] |
| fr | 569 | 0.104 | +0.5135 | +0.8421 | -0.0665 | [-0.1545, +0.0211] | +0.0177 | [-0.0733, +0.1179] | +0.0558 | [-0.0435, +0.1502] |
| it | 570 | 0.380 | +0.5830 | +0.9268 | +0.0512 | [-0.0360, +0.1316] | -0.0673 | [-0.1534, +0.0086] | -0.0963 | [-0.1859, -0.0034] * |
| ja | 570 | 0.311 | +0.7183 | +0.9310 | +0.0155 | [-0.0719, +0.1005] | -0.0116 | [-0.1056, +0.0795] | +0.1421 | [+0.0335, +0.2449] * |
| pt | 567 | 0.293 | +0.7714 | +0.9323 | +0.0274 | [-0.0644, +0.1207] | +0.0012 | [-0.0838, +0.0899] | -0.0002 | [-0.1041, +0.1084] |
| si | 600 | 0.559 | +0.3562 | +0.9511 | +0.1110 | [+0.0395, +0.1857] * | +0.1151 | [+0.0368, +0.1918] * | +0.0332 | [-0.0510, +0.1142] |
| **medie** | 5624 | | **+0.5982** | **+0.9158** | **+0.0512** | [+0.0247, +0.0788] | **+0.0194** | [-0.0114, +0.0499] | **+0.0324** | [+0.0001, +0.0649] |

### `capat_jos`: masa pe capatul usor, `p1 + p2`, mediata pe prompturi

| limba | n | medie | r brut | r cu B | partial vs `B` | CI 95% | partial vs `B3` | CI 95% | partial vs `sys3` | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 0.492 | -0.4473 | -0.9657 | +0.0836 | [-0.0079, +0.1711] | -0.0922 | [-0.1858, +0.0033] | +0.0307 | [-0.0670, +0.1237] |
| de | 570 | 0.298 | -0.5820 | -0.9578 | +0.2062 | [+0.1284, +0.2894] * | +0.0907 | [+0.0062, +0.1723] * | +0.0980 | [+0.0162, +0.1796] * |
| en | 570 | 0.797 | -0.7808 | -0.9341 | +0.0089 | [-0.0832, +0.0956] | +0.0315 | [-0.0694, +0.1270] | +0.0899 | [-0.0190, +0.1963] |
| es | 593 | 0.705 | -0.6975 | -0.9594 | +0.0822 | [+0.0015, +0.1560] * | -0.0075 | [-0.0929, +0.0745] | -0.0269 | [-0.1202, +0.0655] |
| fil | 570 | 0.639 | -0.4968 | -0.9518 | -0.0169 | [-0.0957, +0.0626] | -0.0851 | [-0.1819, +0.0083] | -0.1193 | [-0.2061, -0.0278] * |
| fr | 569 | 0.777 | -0.5727 | -0.9223 | +0.0670 | [-0.0244, +0.1505] | +0.0577 | [-0.0342, +0.1477] | -0.0402 | [-0.1375, +0.0470] |
| it | 570 | 0.433 | -0.5777 | -0.9645 | +0.0630 | [-0.0245, +0.1429] | -0.0602 | [-0.1420, +0.0101] | +0.0441 | [-0.0317, +0.1171] |
| ja | 570 | 0.515 | -0.7265 | -0.9643 | +0.0810 | [+0.0043, +0.1583] * | -0.0124 | [-0.0933, +0.0717] | -0.1313 | [-0.2285, -0.0287] * |
| pt | 567 | 0.604 | -0.7862 | -0.9655 | +0.0456 | [-0.0327, +0.1265] | +0.0063 | [-0.0806, +0.0935] | +0.0513 | [-0.0609, +0.1561] |
| si | 600 | 0.310 | -0.3109 | -0.9613 | +0.0640 | [-0.0113, +0.1438] | +0.0930 | [+0.0203, +0.1615] * | +0.0401 | [-0.0278, +0.1079] |
| **medie** | 5624 | | **-0.5978** | **-0.9547** | **+0.0685** | [+0.0424, +0.0941] | **+0.0022** | [-0.0253, +0.0296] | **+0.0036** | [-0.0273, +0.0333] |

### `dezacord_E`: diferenta valorilor asteptate ale celor doua prompturi, in modul

| limba | n | medie | r brut | r cu B | partial vs `B` | CI 95% | partial vs `B3` | CI 95% | partial vs `sys3` | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 0.108 | -0.0708 | -0.0296 | -0.0646 | [-0.1589, +0.0385] | +0.0036 | [-0.0932, +0.1051] | -0.0622 | [-0.1631, +0.0441] |
| de | 570 | 0.152 | -0.2789 | -0.2229 | -0.1805 | [-0.2717, -0.0927] * | -0.0290 | [-0.1277, +0.0673] | -0.0123 | [-0.1112, +0.0788] |
| en | 570 | 0.124 | -0.1186 | -0.0342 | -0.1649 | [-0.2599, -0.0608] * | -0.1374 | [-0.2318, -0.0370] * | -0.1073 | [-0.1938, -0.0100] * |
| es | 593 | 0.139 | -0.1283 | -0.1114 | -0.0684 | [-0.1596, +0.0305] | +0.0017 | [-0.0944, +0.0967] | +0.0072 | [-0.0806, +0.0942] |
| fil | 570 | 0.087 | +0.0625 | +0.0796 | +0.0250 | [-0.0666, +0.1158] | -0.0183 | [-0.1024, +0.0715] | -0.0087 | [-0.0905, +0.0750] |
| fr | 569 | 0.101 | -0.0217 | -0.0094 | -0.0204 | [-0.1090, +0.0726] | -0.0142 | [-0.0995, +0.0752] | -0.0111 | [-0.0950, +0.0749] |
| it | 570 | 0.149 | -0.1930 | -0.1668 | -0.1166 | [-0.1890, -0.0368] * | -0.0437 | [-0.1147, +0.0316] | -0.0171 | [-0.0886, +0.0598] |
| ja | 570 | 0.139 | -0.1470 | -0.0623 | -0.1551 | [-0.2253, -0.0767] * | -0.1206 | [-0.1905, -0.0446] * | -0.1391 | [-0.2117, -0.0556] * |
| pt | 567 | 0.149 | -0.0975 | -0.0397 | -0.1138 | [-0.1939, -0.0266] * | -0.0952 | [-0.1753, -0.0127] * | -0.0262 | [-0.1143, +0.0632] |
| si | 600 | 0.132 | -0.0738 | -0.2208 | +0.0016 | [-0.0616, +0.0734] | +0.0191 | [-0.0449, +0.0931] | +0.0167 | [-0.0499, +0.0880] |
| **medie** | 5624 | | **-0.1067** | **-0.0817** | **-0.0858** | [-0.1128, -0.0577] | **-0.0434** | [-0.0699, -0.0153] | **-0.0360** | [-0.0626, -0.0086] |

### `dezacord_JS`: divergenta Jensen-Shannon intre cele doua distributii

| limba | n | medie | r brut | r cu B | partial vs `B` | CI 95% | partial vs `B3` | CI 95% | partial vs `sys3` | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | 0.172 | -0.0264 | +0.0048 | -0.0328 | [-0.1235, +0.0597] | +0.0508 | [-0.0432, +0.1434] | -0.0192 | [-0.1093, +0.0729] |
| de | 570 | 0.253 | -0.2923 | -0.1833 | -0.2319 | [-0.3111, -0.1522] * | -0.0956 | [-0.1887, -0.0061] * | -0.0853 | [-0.1740, -0.0039] * |
| en | 570 | 0.237 | -0.1521 | -0.1202 | -0.0947 | [-0.1851, -0.0022] * | -0.0794 | [-0.1732, +0.0139] | -0.0424 | [-0.1319, +0.0511] |
| es | 593 | 0.263 | -0.1800 | -0.1970 | -0.0513 | [-0.1346, +0.0366] | -0.0050 | [-0.0848, +0.0753] | -0.0003 | [-0.0819, +0.0793] |
| fil | 570 | 0.142 | +0.0631 | +0.0980 | +0.0146 | [-0.0752, +0.1012] | -0.0279 | [-0.1143, +0.0567] | -0.0191 | [-0.1046, +0.0654] |
| fr | 569 | 0.183 | -0.0743 | -0.0490 | -0.0560 | [-0.1314, +0.0219] | -0.0476 | [-0.1169, +0.0267] | -0.0428 | [-0.1119, +0.0303] |
| it | 570 | 0.260 | -0.1923 | -0.1749 | -0.1094 | [-0.1833, -0.0263] * | -0.0366 | [-0.1066, +0.0422] | -0.0176 | [-0.0903, +0.0629] |
| ja | 570 | 0.243 | -0.1248 | -0.0531 | -0.1313 | [-0.2053, -0.0540] * | -0.0867 | [-0.1614, -0.0044] * | -0.1078 | [-0.1809, -0.0260] * |
| pt | 567 | 0.262 | -0.1346 | -0.0934 | -0.1018 | [-0.1788, -0.0241] * | -0.0821 | [-0.1557, -0.0122] * | -0.0161 | [-0.0915, +0.0618] |
| si | 600 | 0.201 | -0.0799 | -0.1840 | -0.0187 | [-0.0864, +0.0576] | -0.0094 | [-0.0783, +0.0675] | -0.0031 | [-0.0723, +0.0728] |
| **medie** | 5624 | | **-0.1194** | **-0.0952** | **-0.0813** | [-0.1067, -0.0547] | **-0.0420** | [-0.0668, -0.0150] | **-0.0354** | [-0.0607, -0.0100] |

## (d) Fuziunea, pe tag nou

Se schimba UN SINGUR lucru fata de sistem: coloana `B` a lui `gemma4-12b-4bit` pe test e citita la temperatura, prin `fuse_ab.py --b-dir`. Celelalte doua CSV-uri de test se copiaza verbatim, deci bazinul de candidati al lui `pick_model` ramane acelasi, iar selectia alege in continuare gemma pe toate cele zece limbi. Fisierele se scriu cu `make_bt_runs.py`.

`--b-dir` e un flag OPT-IN adaugat pentru asta, cu implicit `None`. Primele trei randuri din tabel sunt controalele care arata ca nu a mutat nimic: comanda publicata nemodificata, aceeasi comanda cu flagul catre chiar directorul canonic, si aceeasi comanda cu flagul catre un director regenerat cu T = 1. Toate trei trebuie sa dea 0.674946.

Intervalele de mai jos sunt recalculate AICI din predictiile per instanta, cu acelasi `boot_r_ci` si aceleasi contexte, nu copiate din rapoartele lui `fuse_ab.py`. Coincid cu ele, ceea ce e in sine o verificare.

| configuratie | ce schimba | r mediu | fata de sistem | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| `ctrl_nemodificat` | comanda publicata, fara niciun flag nou | **0.674946** | identic | interval de latime 0 | control trecut |
| `ctrl_bdir` | `--b-dir output/bakeoff_test`, adica flagul catre chiar directorul canonic | **0.674946** | identic | interval de latime 0 | control trecut |
| `ctrl_T1` | `--b-dir` catre directorul regenerat cu T = 1 | **0.674946** | identic | interval de latime 0 | control trecut |
| `distT` | B la temperatura aleasa LOLO pe grila SPECIFICATA | **0.682977** | +0.0080 | [+0.0055, +0.0106] | 100.0% |
| `distText` | B la temperatura aleasa LOLO pe grila EXTINSA | **0.683849** | +0.0089 | [+0.0056, +0.0124] | 100.0% |
| `distTpp` | cate o temperatura per prompt, perechea aleasa LOLO | **0.685763** | +0.0108 | [+0.0072, +0.0145] | 100.0% |

### `distT`, per limba

| limba | r sistem | r configuratie noua | diferenta | CI 95% pereche |
|---|---|---|---|---|
| ca | +0.5411 | +0.5543 | **+0.0132** | [+0.0017, +0.0257] * |
| de | +0.7333 | +0.7376 | **+0.0043** | [-0.0039, +0.0127] |
| en | +0.8702 | +0.8719 | **+0.0017** | [-0.0034, +0.0068] |
| es | +0.7606 | +0.7630 | **+0.0024** | [-0.0032, +0.0081] |
| fil | +0.5121 | +0.5172 | **+0.0051** | [-0.0022, +0.0124] |
| fr | +0.6450 | +0.6574 | **+0.0124** | [+0.0045, +0.0206] * |
| it | +0.6647 | +0.6710 | **+0.0063** | [-0.0010, +0.0133] |
| ja | +0.7835 | +0.7927 | **+0.0092** | [+0.0025, +0.0159] * |
| pt | +0.8427 | +0.8474 | **+0.0046** | [+0.0003, +0.0092] * |
| si | +0.3962 | +0.4174 | **+0.0212** | [+0.0075, +0.0346] * |
| **medie** | **+0.6749** | **+0.6830** | **+0.0080** | [+0.0055, +0.0106] |

Castiga pe 10 limbi din 10, cu interval care exclude zero pe 5. Intervalul MEDIEI, care e cifra care conteaza, exclude zero.

### `distText`, per limba

| limba | r sistem | r configuratie noua | diferenta | CI 95% pereche |
|---|---|---|---|---|
| ca | +0.5411 | +0.5566 | **+0.0155** | [+0.0007, +0.0312] * |
| de | +0.7333 | +0.7468 | **+0.0135** | [+0.0029, +0.0247] * |
| en | +0.8702 | +0.8700 | **-0.0002** | [-0.0074, +0.0071] |
| es | +0.7606 | +0.7641 | **+0.0035** | [-0.0044, +0.0116] |
| fil | +0.5121 | +0.5091 | **-0.0030** | [-0.0131, +0.0073] |
| fr | +0.6450 | +0.6590 | **+0.0140** | [+0.0030, +0.0251] * |
| it | +0.6647 | +0.6750 | **+0.0104** | [-0.0008, +0.0203] |
| ja | +0.7835 | +0.7877 | **+0.0042** | [-0.0038, +0.0125] |
| pt | +0.8427 | +0.8450 | **+0.0023** | [-0.0045, +0.0091] |
| si | +0.3962 | +0.4251 | **+0.0289** | [+0.0124, +0.0452] * |
| **medie** | **+0.6749** | **+0.6838** | **+0.0089** | [+0.0056, +0.0124] |

Castiga pe 8 limbi din 10, cu interval care exclude zero pe 4. Intervalul MEDIEI, care e cifra care conteaza, exclude zero.

### `distTpp`, per limba

| limba | r sistem | r configuratie noua | diferenta | CI 95% pereche |
|---|---|---|---|---|
| ca | +0.5411 | +0.5594 | **+0.0183** | [+0.0027, +0.0344] * |
| de | +0.7333 | +0.7520 | **+0.0187** | [+0.0080, +0.0296] * |
| en | +0.8702 | +0.8713 | **+0.0011** | [-0.0063, +0.0084] |
| es | +0.7606 | +0.7616 | **+0.0009** | [-0.0073, +0.0090] |
| fil | +0.5121 | +0.5174 | **+0.0054** | [-0.0055, +0.0162] |
| fr | +0.6450 | +0.6638 | **+0.0187** | [+0.0071, +0.0313] * |
| it | +0.6647 | +0.6769 | **+0.0123** | [+0.0013, +0.0222] * |
| ja | +0.7835 | +0.7909 | **+0.0074** | [-0.0033, +0.0181] |
| pt | +0.8427 | +0.8416 | **-0.0011** | [-0.0084, +0.0058] |
| si | +0.3962 | +0.4227 | **+0.0265** | [+0.0087, +0.0441] * |
| **medie** | **+0.6749** | **+0.6858** | **+0.0108** | [+0.0072, +0.0145] |

Castiga pe 9 limbi din 10, cu interval care exclude zero pe 5. Intervalul MEDIEI, care e cifra care conteaza, exclude zero.

### Trei lucruri de scris, nu de ascuns

1. **T e fixat din (b), nu ales din nou in `fit_choice`** alaturi de `w_src` si de setul de trasaturi. Asa se schimba un singur lucru fata de sistem. Un T ales in interiorul selectiei imbricate ar fi al patrulea nivel si nu s-a coborat pana acolo.

2. **Coloana `B_T` a unei limbi de potrivire L' e construita cu T ales excluzand L', dar nu si L.** Cifra limbii tinute deoparte nu e atinsa: T-ul lui L nu vede nicio eticheta din L. Dar alegerile lui L depind indirect de etichetele lui L prin coloanele CELORLALTE limbi. E exact dependenta de un nivel pe care `output/e_fusion_lolo_adoptat.md` o declara deja la punctul 2 din „unde nu e garantat”, pentru modelul lui B, si se declara la fel.

3. **Alegerea intre grila specificata si cea extinsa se face pe scorul de test.** Amandoua sunt curate pe dinauntru, dar diferenta dintre ele, +0.000872, nu se poate arbitra fara sa privesti testul. E acelasi tip de bifurcatie ca alegerea intre configuratiile din `output/e_fusion_lolo_adoptat.md`, sectiunea „Scara configuratiilor”: fiecare e curata pe dinauntru, dar alegerea intre ele se uita la scorul raportat. Se declara ca atare in Limitations, nu se ascunde intr-o alegere de grila.

## (e) Cat de robust e castigul la valoarea exacta a lui T

Tabelul de mai jos NU alege nimic: r se calculeaza la T FIX, aceeasi pentru toate cele zece limbi, si se raporteaza diferenta PERECHE fata de T = 1, cu interval pe contexte. E descriptiv. A alege T citind chiar tabelul asta ar fi tuning pe scorul raportat, si de aia cifra care se citeaza ramane cea de la (b), unde T se alege leave-one-language-out.

| T | r mediu | fata de T=1 | CI 95% pereche | P(>0) | limbi in castig |
|---|---|---|---|---|---|
| 0.5 | 0.6346 | -0.0074 | [-0.0091, -0.0059] * | 0.0% | 1.0/10 |
| 0.75 | 0.6386 | -0.0034 | [-0.0042, -0.0027] * | 0.0% | 0.0/10 |
| **1** | **0.6420** | -0.0000 | [-0.0000, +0.0000] | 25.9% | 4.0/10 |
| 1.25 | 0.6449 | +0.0029 | [+0.0022, +0.0035] * | 100.0% | 10.0/10 |
| 1.5 | 0.6473 | +0.0053 | [+0.0041, +0.0065] * | 100.0% | 10.0/10 |
| 1.75 | 0.6493 | +0.0073 | [+0.0057, +0.0090] * | 100.0% | 10.0/10 |
| 2 | 0.6511 | +0.0090 | [+0.0070, +0.0111] * | 100.0% | 10.0/10 |
| 2.5 | 0.6537 | +0.0117 | [+0.0090, +0.0145] * | 100.0% | 10.0/10 |
| 3 | 0.6556 | +0.0136 | [+0.0104, +0.0169] * | 100.0% | 10.0/10 |
| 3.5 | 0.6569 | +0.0149 | [+0.0113, +0.0185] * | 100.0% | 10.0/10 |
| 4 | 0.6579 | +0.0158 | [+0.0119, +0.0198] * | 100.0% | 10.0/10 |
| 5 | 0.6591 | +0.0170 | [+0.0126, +0.0214] * | 100.0% | 10.0/10 |
| 6 | 0.6598 | +0.0177 | [+0.0131, +0.0224] * | 100.0% | 10.0/10 |
| 8 | 0.6604 | +0.0183 | [+0.0133, +0.0235] * | 100.0% | 9.0/10 |
| 10 | 0.6607 | +0.0186 | [+0.0134, +0.0240] * | 100.0% | 9.0/10 |
| 12 | 0.6607 | +0.0186 | [+0.0132, +0.0243] * | 100.0% | 9.0/10 |
| 16 | 0.6605 | +0.0184 | [+0.0128, +0.0242] * | 100.0% | 9.0/10 |
| 20 | 0.6601 | +0.0180 | [+0.0123, +0.0240] * | 100.0% | 9.0/10 |
| 24 | 0.6597 | +0.0176 | [+0.0118, +0.0237] * | 100.0% | 8.0/10 |
| 32 | 0.6590 | +0.0169 | [+0.0110, +0.0232] * | 100.0% | 8.0/10 |
| 48 | 0.6580 | +0.0159 | [+0.0097, +0.0224] * | 100.0% | 8.0/10 |
| 64 | 0.6574 | +0.0153 | [+0.0090, +0.0219] * | 100.0% | 8.0/10 |

`*` = intervalul exclude zero. **Castigul are interval care exclude zero pe 19 din cele 21 valori de T diferite de 1**, de la 1.25 pana la 64. Maximul e la T = 12, cu 0.6607, dar intre T = 4 si T = 24 diferenta de r e 0.0028, adica sub o zecime din latimea oricarui interval de aici.

Concluzia care conteaza pentru scris: **nu se revendica o valoare a lui T, se revendica un platou.** Orice T intre 4 si 24 da practic aceeasi cifra, si castigul fata de T = 1 tine pe tot platoul. Alegerea exacta a lui T e deci mult mai putin importanta decat faptul CA se aplica o temperatura, ceea ce e si raspunsul la intrebarea daca argmaxul e zgomot: e, si nu conteaza.

## (f) Cate o temperatura per prompt

Cele doua prompturi nu sunt acelasi instrument: primul cere raspunsul ca `ONLY a single digit from 1 to 5`, al doilea ca `only the digit`, si nu au aceeasi ascutime. Fiecare primeste aici temperatura lui. Perechea (T1, T2) se alege tot leave-one-language-out, pe grila extinsa luata de doua ori, deci 16x16 = 256 de candidati in loc de 16.

Comparatia e fata de temperatura UNICA aleasa tot LOLO pe aceeasi grila, adica fata de varianta `distText` din (d), nu fata de T = 1. Altfel s-ar amesteca doua schimbari.

| limba | T prompt 1 | T prompt 2 | T unic | r cu T unic | r per prompt | diferenta | CI 95% pereche | latime criteriu | margine peste diagonala |
|---|---|---|---|---|---|---|---|---|---|
| ca | 16 | 8 | 12 | +0.5159 | +0.5207 | **+0.0048** | [-0.0024, +0.0121] | 0.0816 | +0.00127 |
| de | 12 | 6 | 8 | +0.6812 | +0.6910 | **+0.0098** | [+0.0039, +0.0157] * | 0.0781 | +0.00086 |
| en | 16 | 8 | 12 | +0.8463 | +0.8483 | **+0.0020** | [-0.0022, +0.0064] | 0.0858 | +0.00157 |
| es | 16 | 8 | 12 | +0.7499 | +0.7463 | **-0.0036** | [-0.0075, -0.0000] * | 0.0884 | +0.00219 |
| fil | 16 | 8 | 16 | +0.5082 | +0.5171 | **+0.0089** | [+0.0032, +0.0147] * | 0.0918 | +0.00108 |
| fr | 16 | 8 | 12 | +0.6655 | +0.6689 | **+0.0034** | [-0.0022, +0.0092] | 0.0834 | +0.00142 |
| it | 16 | 8 | 12 | +0.6354 | +0.6390 | **+0.0036** | [-0.0017, +0.0092] | 0.0827 | +0.00139 |
| ja | 16 | 8 | 12 | +0.7715 | +0.7719 | **+0.0004** | [-0.0034, +0.0040] | 0.0848 | +0.00175 |
| pt | 16 | 8 | 12 | +0.8322 | +0.8294 | **-0.0027** | [-0.0063, +0.0004] | 0.0863 | +0.00210 |
| si | 12 | 6 | 8 | +0.3860 | +0.3830 | **-0.0030** | [-0.0089, +0.0027] | 0.0840 | +0.00229 |
| **medie** | | | | **+0.6592** | **+0.6616** | **+0.0024** | [+0.0008, +0.0041] | | |

`margine peste diagonala` e cu cat bate perechea castigatoare cel mai bun punct cu T1 = T2 pe ACELASI criteriu. E cifra care spune daca a doua temperatura cumpara ceva sau doar da voie argmaxului sa se plimbe: o margine de ordinul a 1e-4 pe un criteriu lat de 0.085 inseamna ca nu cumpara.

Pe medie, a doua temperatura da **+0.0024**, interval [+0.0008, +0.0041], adica **exclude zero**.

Cele doua prompturi, luate fiecare singur, cu T ales pe media tuturor limbilor:

| prompt | T optim | r la T optim | r la T=1 |
|---|---|---|---|
| 1 | 16 | +0.6256 | +0.5820 |
| 2 | 6 | +0.6536 | +0.6402 |

## Verdict

1. **Linia de baza se reproduce**: B reconstruit din distributiile salvate e coloana B, la 8 zecimale, pe toate cele 5624 de randuri.

2. **Temperatura tine.** Aleasa leave-one-language-out pe grila specificata da +0.0158 pe medie, interval pereche [+0.0119, +0.0198], deci exclude zero, si castiga pe 10 limbi din 10. Semnalul B trece de la +0.6420 la +0.6579. Alegerea a cazut insa la marginea grilei pe 10 limbi din 10; pe grila extinsa varful e interior si castigul e +0.0171, [+0.0119, +0.0227].

3. **Dezacordul, cu controlul naiv:** 5 din 5 masuri au interval al mediei care exclude zero fata de B liniar (`entropie`, `capat_sus`, `capat_jos`, `dezacord_E`, `dezacord_JS`).

4. **Dezacordul, cu controlul flexibil, si asta e cifra care conteaza:** raman 2 din 5 (`dezacord_E`, `dezacord_JS`). Masurile de FORMA a unei singure distributii, entropia si masa pe capete, se sting: erau curbura lui B, adica exact ce repara temperatura din (b), citita a doua oara. Ce ramane, daca ramane, e dezacordul INTRE cele doua prompturi, care nu e o functie de o singura distributie si pe care media nu o poate exprima.

5. **Fata de sistemul intreg**, cu acelasi control flexibil, raman 3 din 5 (`capat_sus`, `dezacord_E`, `dezacord_JS`).

6. **Fuziunea, pe tag nou:** `distT` da **0.682977**, +0.0080 fata de sistem, CI [+0.0055, +0.0106]; `distText` da **0.683849**, +0.0089 fata de sistem, CI [+0.0056, +0.0124]; `distTpp` da **0.685763**, +0.0108 fata de sistem, CI [+0.0072, +0.0145]. Cele 3 controale dau toate 0.674946, deci flagul `--b-dir` nu misca nimic singur. **Nimic nu e adoptat aici**: cifra publicata ramane 0.674946 pana cand decide Alexandru.

7. **Ce urmeaza.** Temperatura merge la fuziune pe tag nou, cu comparatie PERECHE fata de sistem. Pentru `dezacord_E`, `dezacord_JS` decizia nu e a acestui raport: ar fi un AL TREILEA termen in fuziune, iar `fuse_ab.fit_choice` are azi o singura pondere. Nimic nu se adopta fara interval pereche care exclude zero pe cifra finala.

