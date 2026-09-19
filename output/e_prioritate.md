# Prioritizarea parghiilor rams pe lista

Generat 2026-08-21 19:10:02 de `analysis_prioritate.py`. Referinta e `fusion_preds_lolo_adoptat_temp.csv`, adica sistemul CU temperatura.

**Verificarea referintei:** r recalculat din predictiile per instanta e **0.683849**, iar cifra declarata in `output/e_fusion_lolo_adoptat_temp.md` e **0.683849**. Diferenta 2.88e-07. Coincid, deci referinta raportului e chiar sistemul.

Temperaturile adoptate, per limba, pe grila extinsa: ca T=12, de T=8, en T=12, es T=12, fil T=16, fr T=12, it T=12, ja T=12, pt T=12, si T=8.

Agregarea e media pe cele zece limbi, nu pooled, in tot raportul. Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari, si cele ale diferentelor sunt PERECHE.

## 1. Agregarea celor doua prompturi, masurata cap la cap

Semnalul B mediaza azi 50/50 valorile asteptate ale celor doua prompturi. Media aia e demonstrat gresita ca alegere: in `output/e_dist.md`, cu T-ul lor, promptul 2 singur da +0.6536 si promptul 1 doar +0.6256. Trei variante, toate pe fisierele deja pe disc:

- `pondere`: `w*E(p1^(1/T)) + (1-w)*E(p2^(1/T))`, cu T **fixat** la valoarea adoptata per limba si numai `w` ales LOLO pe 7 puncte.
- `produs`: media geometrica a celor doua distributii, renormalizata. **Puterea si produsul comuta**, `(p^(1/T) q^(1/T))^(1/2) = (pq)^(1/(2T))`, deci produsul la T fix ar fi confundat cu temperatura; T se realege pe aceeasi grila extinsa, deci acelasi numar de candidati.
- `pondere-produs`: media geometrica ponderata, amandoua.

Alegerea lui `w` pentru limba L foloseste, pentru fiecare limba de potrivire l', temperatura lui l' aleasa fara L si fara l'. Al doilea nivel din `fuse_ab.fit_choice`: fara el, `w`-ul lui L ar trece prin etichetele lui L.

Coloana **`limbi stricate`** e criteriul care a respins `distTpp` la 0.685763: o configuratie care urca media dar strica o limba cu interval pereche care exclude zero nu se adopta, oricat de mare e media. Se citeste inaintea coloanei cu media.

| configuratie | ce schimba | r mediu | fata de sistem | CI 95% pereche | P(>0) | limbi peste | limbi urcate, CI exclude 0 | limbi stricate, CI exclude 0 | latime criteriu | margine peste neutru |
|---|---|---|---|---|---|---|---|---|---|---|
| `prio_W05` | control: modul `pondere` redus la punctul neutru w = 0.5 | **0.683849** | identic | interval de latime 0 | control trecut | 0/10 | 0 | **0** | 0.0000 | +0.00000 |
| `prio_W` | pondere intre prompturi, `w` ales LOLO, T fixat la valoarea adoptata | **0.684331** | +0.0005 | [-0.0002, +0.0012] | 90.0% | 6/10 | 1 | **1** | 0.0368 | +0.00121 |
| `prio_G` | media geometrica a celor doua distributii, T propriu ales LOLO | **0.683541** | -0.0003 | [-0.0008, +0.0002] | 10.0% | 3/10 | 1 | **2** | 0.0000 | +0.00000 |
| `prio_WG` | media geometrica PONDERATA, `w` si T alese LOLO | **0.684432** | +0.0006 | [-0.0003, +0.0015] | 88.4% | 6/10 | 1 | **1** | 0.0376 | +0.00115 |
| `prio_K` | cifrele vecine UNITE, partitia aleasa LOLO din 15 candidate | **0.685530** | +0.0017 | [+0.0007, +0.0027] | 100.0% | 8/10 | 3 | **0** | 0.3908 | +0.00208 |
| `prio_KW` | unirea cifrelor plus ponderea intre prompturi, in ordine prespecificata | **0.685727** | +0.0019 | [+0.0005, +0.0033] | 99.6% | 7/10 | 3 | **1** | 0.0372 | +0.00167 |

`latime criteriu` e `max - min` al criteriului LOLO peste grila lui `w`, si `margine peste neutru` e cu cat bate `w` ales punctul `w = 0.5` pe ACELASI criteriu. Sunt coloanele care spun daca alegerea cumpara ceva sau doar da voie argmaxului sa se plimbe pe un criteriu plat, si sunt exact cele care au permis respingerea argumentata a lui `distTpp` la 0.685763.

**De declarat, si e o bifurcatie, nu un detaliu.** Ultimele doua configuratii nu erau pe lista de la inceput: `prio_K` a iesit din blocul 3 de mai jos, adica dintr-o scara r(K) calculata pe TEST. Hiperparametrii ei sunt alesi LOLO ca la orice altceva, dar decizia de a o incerca vine de la o cifra de test, exact ca celelalte bifurcatii ale lucrarii. Intra in Limitations pe aceeasi lista.

### `prio_W`, per limba

| limba | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| diferenta | +0.0010 | +0.0044 | +0.0009 | -0.0011 | +0.0011 | +0.0011 | +0.0017 | -0.0006 | -0.0026 | -0.0011 |
| CI exclude 0 | - | urcata | - | - | - | - | - | - | **stricata** | - |

### `prio_G`, per limba

| limba | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| diferenta | -0.0005 | -0.0029 | +0.0001 | -0.0000 | +0.0020 | -0.0007 | -0.0008 | -0.0001 | -0.0001 | +0.0001 |
| CI exclude 0 | - | **stricata** | - | - | urcata | **stricata** | - | - | - | - |

### `prio_WG`, per limba

| limba | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| diferenta | +0.0016 | +0.0031 | +0.0011 | -0.0011 | +0.0030 | +0.0017 | +0.0013 | -0.0009 | -0.0029 | -0.0010 |
| CI exclude 0 | - | - | - | - | urcata | - | - | - | **stricata** | - |

### `prio_K`, per limba

| limba | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| diferenta | +0.0027 | -0.0004 | +0.0004 | +0.0023 | +0.0060 | -0.0012 | +0.0002 | +0.0023 | +0.0016 | +0.0028 |
| CI exclude 0 | - | - | - | urcata | urcata | - | - | - | urcata | - |

### `prio_KW`, per limba

| limba | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| diferenta | +0.0039 | +0.0047 | +0.0009 | -0.0016 | +0.0072 | +0.0030 | +0.0018 | +0.0051 | -0.0056 | -0.0008 |
| CI exclude 0 | - | urcata | - | - | urcata | - | - | urcata | **stricata** | - |

`w` ales LOLO la `prio_W`: [0.4] pe toate cele zece limbi. `w` e ponderea promptului 1, deci sub 0.5 inseamna ca promptul 2 primeste mai mult, coerent cu +0.6536 fata de +0.6256.

## 2. Plafoane pentru doua parghii scumpe

Amandoua se masoara la fel: cat ar putea urca r daca marimea s-ar adauga peste o citire FLEXIBILA a predictiei finale, `(p, p^2, p^3)`. Cifra e o limita SUPERIOARA din doua motive independente. Intai, coeficientii se potrivesc pe chiar randurile pe care se masoara r, deci castigul e in-sample; un termen ales LOLO nu poate da mai mult. Apoi, controlul flexibil citeste deja curbura sistemului, deci ce rams e strict canal nou. **Sub +0.002 parghia se inchide fara sa se scrie codul.**

`r cub` e r-ul citirii flexibile singure, si e peste sistem prin construcție: coloana spune cat din distanta pana la plafon vine din citirea neliniara a sistemului, nu din marimea noua.

### 2a. Al treilea termen de fuziune, pentru dezacordul intre prompturi

`dezacord_E` si `dezacord_JS` sunt singurele doua masuri din `output/e_dist.md` care au supravietuit controlului flexibil fata de sistemul intreg. Costul lor nu e inferenta, e cod: `fuse_ab.fit_choice` are azi o singura pondere si o selectie pe trei niveluri.

**`zgomot_1` si `zgomot_2` sunt calibrarea pe zero, si fara ele tabelul nu se poate citi.** Sunt una, respectiv doua coloane de zgomot gaussian, cu seed fix, puse prin exact aceeasi procedura. Orice coloana adaugata in-sample urca r si daca nu contine nimic, cu atat mai mult cu cat sunt mai multe: la n ~ 562 pe limba, inflatia asteptata e de ordinul `(1 - R^2) * k / n`. Un plafon care nu bate randul de zgomot cu acelasi numar de coloane nu spune nimic.

| marime | coloane | r sistem | r cub | r cub + marime | plafonul castigului | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|---|---|
| `dezacord_E` | 1 | 0.6838 | 0.6885 | 0.6891 | **+0.00055** | [-0.00042, +0.00154] | 85.9% |
| `dezacord_JS` | 1 | 0.6838 | 0.6885 | 0.6888 | **+0.00029** | [-0.00023, +0.00082] | 84.0% |
| `ambele` | 2 | 0.6838 | 0.6885 | 0.6908 | **+0.00231** | [+0.00045, +0.00436] | 99.0% |
| `zgomot_1` | 1 | 0.6838 | 0.6885 | 0.6892 | **+0.00063** | [-0.00040, +0.00157] | 89.1% |
| `zgomot_2` | 2 | 0.6838 | 0.6885 | 0.6897 | **+0.00121** | [-0.00008, +0.00249] | 96.6% |

### 2b. Reziduul de fertilitate

Din `output/e_fr_diagnostic.md`: fertilitatea mai are validitate incrementala peste sistem pe franceza, +0.1450 cu CI care exclude zero. Dar pe `de` si `pt` reziduul e NEGATIV cu CI care exclude zero, deci o fertilitate pusa global ar strica acolo. De aceea plafonul se da per limba, si abia apoi agregat.

| limba | fertilitate medie | r sistem | r cub | r cub + fertilitate | plafon | CI 95% | P(>0) |
|---|---|---|---|---|---|---|---|
| ca | 2.61 | 0.5566 | 0.5614 | 0.5614 | **+0.00005** | [-0.00098, +0.00107] | 55.2% |
| de | 2.56 | 0.7468 | 0.7611 | 0.7778 | **+0.01669** | [+0.00661, +0.02656] * | 100.0% |
| en | 1.88 | 0.8700 | 0.8715 | 0.8718 | **+0.00030** | [-0.00077, +0.00150] | 70.0% |
| es | 1.96 | 0.7641 | 0.7673 | 0.7687 | **+0.00135** | [-0.00187, +0.00446] | 79.7% |
| fil | 2.37 | 0.5091 | 0.5139 | 0.5524 | **+0.03844** | [+0.00828, +0.06856] * | 99.2% |
| fr | 2.02 | 0.6590 | 0.6627 | 0.6628 | **+0.00013** | [-0.00107, +0.00140] | 57.5% |
| it | 2.36 | 0.6750 | 0.6825 | 0.6853 | **+0.00280** | [-0.00327, +0.00854] | 83.3% |
| ja | 3.37 | 0.7877 | 0.7904 | 0.7938 | **+0.00338** | [-0.00248, +0.00964] | 87.2% |
| pt | 2.08 | 0.8450 | 0.8454 | 0.8470 | **+0.00166** | [-0.00117, +0.00448] | 88.0% |
| si | 3.32 | 0.4251 | 0.4290 | 0.4374 | **+0.00839** | [-0.00426, +0.02062] | 90.2% |
| **medie** | 2.45 | 0.6838 | 0.6885 | 0.6958 | **+0.00723** | [+0.00365, +0.01092] | 100.0% |

`*` = intervalul limbii exclude zero. Aplicata global, cu coeficient potrivit pe limba ei, fertilitatea are plafonul **+0.00723**.

**Atentie la citirea semnului.** In `output/e_fr_diagnostic.md` reziduul lui `de` e NEGATIV cu CI care exclude zero, si totusi aici `de` are plafon pozitiv mare. Nu e o contradictie: corelatia partiala are semn, iar castigul predictiv nu, fiindca regresia potriveste coeficientul. De aceea coloana care decide nu e nici una din cele de sus, e transferul.

**Transferul, adica singura varianta pe care o poate produce o procedura onesta.** Coeficientul fertilitatii se potriveste pe celelalte noua limbi si se aplica pe L, exact cum se aleg `w`, `w_src` si setul de trasaturi. Coloana `semn` e semnul coeficientului potrivit pe limba ei, si daca semnele nu cad la fel transferul nu are ce sa duca.

| limba | ca | de | en | es | fil | fr | it | ja | pt | si | **medie** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| semn coeficient | - | - | + | - | + | + | - | - | - | + | 4/10 pozitive |
| castig la transfer | +0.0000 | -0.0063 | +0.0000 | -0.0006 | -0.0043 | -0.0001 | -0.0010 | -0.0011 | -0.0005 | -0.0017 | **-0.00153** |

La transfer, fertilitatea da **-0.00153**, interval pereche [-0.00186, -0.00122], P(>0) = 0.0%, adica exclude zero.

## 3. Cat headroom mai are scara de raspuns

Scara e 1-5, deci citirea soft are cinci atomi, pe o eticheta continua. Intrebarea e daca cei cinci atomi sunt constrangerea care leaga, si se pune de trei ori, fara nicio inferenta.

### 3a. Scara r(K): ce se pierde la scari mai grosiere

Se unesc cifrele VECINE in K blocuri, fiecare bloc luand ca valoare media notelor lui, si se reciteste valoarea asteptata. Se raporteaza `max` peste toate partitiile contigue, deci scarile grosiere sunt aratate in cea mai buna lumina posibila. **Se declara ca proxy, nu ca predictie:** unirea binurilor nu e acelasi lucru cu a intreba modelul pe o scara mai grosiera, fiindca modelul s-ar recalibra. Ce e informativ e forma curbei, nu valoarea.

Trei coloane, si numai a treia e o cifra pe care o poate produce o procedura onesta. `max` alege partitia uitandu-se la chiar limba pe care o masoara, deci e oracol. `LOLO` alege partitia pe celelalte noua limbi, ca orice hiperparametru din lucrare.

| K | partitii | `max` peste partitii, oracol | media peste partitii | **partitie aleasa LOLO** | LOLO fata de K=5 |
|---|---|---|---|---|---|
| 2 | 4 | +0.6581 | +0.5323 | **+0.6263** | -0.0329 |
| 3 | 6 | +0.6662 | +0.6437 | **+0.6613** | +0.0021 |
| 4 | 4 | +0.6632 | +0.6566 | **+0.6578** | -0.0014 |
| 5 | 1 | +0.6592 | +0.6592 | **+0.6592** | referinta |

### 3b. Citirea liniara optima a celor cinci probabilitati

`B` e UN anume functional liniar al distributiei, cel cu notele 1..5 egal spatiate. Cel mai bun functional liniar se obtine regresand eticheta pe chiar cele cinci probabilitati, si se alege LOLO ca orice hiperparametru: coeficientii limbii L vin de la celelalte noua. Distinctia pe care o face coloana asta e cea care conteaza pentru decizie: daca citirea optima bate `B` cu mult, informatia e ACOLO si o risipeste citirea, deci nu ai nevoie de mai multi atomi, ai nevoie de alta citire, si aia e gratis. Daca nu o bate, cei cinci atomi sunt chiar plafonul si numai o scara mai fina il muta.

Raspunde in acelasi timp la parghia `distributia intreaga ca trasaturi in bratul A`, care e chiar functionalul asta pus in fuziune.

| limba | r `B` la T adoptat | r citire optima LOLO | diferenta | r citire optima in-sample |
|---|---|---|---|---|
| ca | +0.5159 | +0.4977 | **-0.0182** | +0.5302 |
| de | +0.6812 | +0.6031 | **-0.0781** | +0.7287 |
| en | +0.8463 | +0.8299 | **-0.0164** | +0.8532 |
| es | +0.7499 | +0.7309 | **-0.0190** | +0.7711 |
| fil | +0.5082 | +0.5089 | **+0.0007** | +0.5365 |
| fr | +0.6655 | +0.6563 | **-0.0092** | +0.6768 |
| it | +0.6354 | +0.6123 | **-0.0231** | +0.6433 |
| ja | +0.7715 | +0.7572 | **-0.0143** | +0.7768 |
| pt | +0.8322 | +0.8280 | **-0.0041** | +0.8359 |
| si | +0.3860 | +0.3831 | **-0.0029** | +0.4073 |
| **medie** | **+0.6592** | **+0.6407** | **-0.0185** | +0.6760 |

Coloana in-sample e a doua limita superioara, cu coeficienti potriviti pe chiar limba masurata: nici ea nu e atinsa de o procedura onesta.

### 3c. Recensamant de saturatie

`atomi efectivi` e `exp(entropie)`, adica peste cate cifre e imprastiata efectiv masa. Daca la T adoptat masa e imprastiata pe aproape toate cele cinci, atunci `B` e deja o marime fina si cei cinci atomi nu leaga; daca sta pe una singura, leaga. `legaturi` e cate randuri au o valoare a lui `B` care se repeta, fiindca legaturile plafoneaza Pearson.

| limba | masa pe argmax, T=1 | masa pe argmax, T adoptat | atomi efectivi, T=1 | atomi efectivi, T adoptat | valori distincte ale `B` | legaturi |
|---|---|---|---|---|---|---|
| ca | 0.741 | 0.314 | 1.83 | 4.59 | 445/445 | 0 |
| de | 0.725 | 0.378 | 1.84 | 4.23 | 570/570 | 0 |
| en | 0.747 | 0.358 | 1.70 | 4.40 | 570/570 | 0 |
| es | 0.719 | 0.333 | 1.80 | 4.51 | 593/593 | 0 |
| fil | 0.775 | 0.296 | 1.69 | 4.73 | 570/570 | 0 |
| fr | 0.773 | 0.345 | 1.64 | 4.44 | 569/569 | 0 |
| it | 0.712 | 0.327 | 1.87 | 4.54 | 570/570 | 0 |
| ja | 0.703 | 0.314 | 1.90 | 4.58 | 570/570 | 0 |
| pt | 0.724 | 0.332 | 1.81 | 4.54 | 567/567 | 0 |
| si | 0.729 | 0.353 | 1.90 | 4.37 | 600/600 | 0 |
| **medie** | **0.735** | **0.335** | **1.80** | **4.49** | 5624/5624 | 0 |

## 4. Sondajul de scara pe trial

Blocul 3 spune ca cei cinci atomi nu leaga si prezice deci **negativ** pentru o scara mai fina. Proxy-ul de acolo nu poate insa vedea RECALIBRAREA: cand modelul e chiar intrebat pe 0-9, distributia lui nu e distributia de pe 1-5 reeșantionata, e alta. Trei brate, 300 instante de trial fiecare, ~6 minute per brat.

**Design 2x2 incomplet, si de aia e nevoie de trei brate, nu doua.** `0-9` schimba doua lucruri fata de `1-5`: numarul de atomi SI ancora. `0-4` schimba numai ancora. Deci efectul ancorei e `(0-4) - (1-5)` si efectul atomilor e `(0-9) - (0-4)`. Fara bratul din mijloc cele doua sunt confundate, si oricare rezultat ar fi fost necitibil.

**De ce nu 1-10 si de ce nu 0-99.** Soft-read-ul citeste o SINGURA pozitie de token, iar `10` sunt doi tokeni si primul se ciocneste cu nota 1, deci 0-9 e singura scara de zece atomi citibila asa. 0-99 ar cere fie o a doua trecere inainte per rand, fie 11 treceri pentru valoarea asteptata conditionata, deci nu mai e o configuratie de 6 minute si nu intra in sondaj.

Temperatura se realege pentru FIECARE brat, pe aceeasi grila extinsa, si se raporteaza atat argmaxul pe medie cat si r la T = 1: o scara mai fina schimba ascutimea distributiei, deci comparatia la T = 1 ar masura ascutimea, nu scara. Argmaxul pe medie e un oracol, NU protocolul LOLO al lucrarii, si e deliberat: e acelasi oracol pentru toate trei bratele, deci nu favorizeaza niciunul, iar aici se cerne, nu se adopta.

| brat | atomi | ce schimba | r la T=1 | T* pe medie | r la T* | atomi efectivi la T=1 | masa pe argmax la T=1 |
|---|---|---|---|---|---|---|---|
| `1-5` | 5 | scara publicata, cinci atomi, ancora la 1 | +0.6860 | 8 | **+0.7067** | 1.75 din 5 | 0.752 |
| `0-4` | 5 | cinci atomi, ancora mutata la 0: izoleaza efectul ancorei | +0.6921 | 6 | **+0.6990** | 1.91 din 5 | 0.686 |
| `0-9` | 10 | zece atomi si ancora la 0 | +0.6791 | 8 | **+0.6974** | 2.51 din 10 | 0.587 |

### Cele doua efecte, separate

Comparatie PERECHE pe contexte, fiecare brat citit la temperatura lui. Intervalele sunt late si trebuie sa fie: sunt 30 de instante per limba, nu 560. Cifra de trial nu e o predictie a cifrei de test, ordinea e.

| efect | brate | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|
| ancora, 1 -> 0 | `0-4` fata de `1-5` | **-0.0081** | [-0.0225, +0.0054] | 12.4% |
| atomii, 5 -> 10 | `0-9` fata de `0-4` | **-0.0018** | [-0.0159, +0.0122] | 40.1% |
| amandoua, 1-5 -> 0-9 | `0-9` fata de `1-5` | **-0.0099** | [-0.0259, +0.0052] | 9.8% |

**Verdictul sondajului.** Cele zece atomi dau +0.6974 fata de +0.7067, adica -0.0099, interval [-0.0259, +0.0052], deci include zero. Modelul foloseste efectiv 2.51 din cele zece cifre, fata de 1.75 din cinci, deci **nu deschide rezolutie, o imparte**. Asteptarea declarata inainte de rulare era negativa, si se confirma.

## Verdict: ordinea, pe cifre

`masurat` = configuratie rulata cap la cap prin fuziune, cu interval pereche fata de sistem. `plafon` = limita superioara in-sample, deci o procedura onesta da mai putin. `proxy` = diagnostic pe disc care nu poate inlocui o rulare, doar sa spuna in ce direcție sa te aștepti. `cost declarat` = nu s-a masurat nimic, se da doar pretul.

| # | parghie | tip de dovada | delta | CI 95% pereche | P(>0) | cost pana la o cifra pe test | verdict |
|---|---|---|---|---|---|---|---|
| 1 | unirea cifrelor vecine, partitie LOLO (`prio_K`) | masurat | **+0.00168** | [+0.00072, +0.00269] | 100.0% | 0, e rulata deja | **trece**: interval care exclude zero, urca 3 limbi semnificativ, strica zero, si partitia `1|23|45` e aleasa unanim pe toate zece limbile, pe un criteriu lat de 0.39 |
| 2 | unirea cifrelor + pondere (`prio_KW`) | masurat | **+0.00186** | [+0.00050, +0.00330] | 99.6% | 0, e rulata deja | **respinsa**: media urca, dar strica pt cu interval pereche care exclude zero, acelasi motiv ca `distTpp`. Peste `prio_K` adauga doar +0.00018, deci cele doua parghii sunt redundante, ceea ce era de asteptat: amandoua respatiaza aceeasi citire liniara |
| 3 | pondere intre prompturi (`prio_W`) | masurat | **+0.00048** | [-0.00022, +0.00121] | 90.0% | 0, e rulata deja | nesemnificativa, nu nula: P(>0) = 90.0%, CI include zero; strica in plus pt cu interval care exclude zero |
| 4 | media geometrica (`prio_G`) | masurat | **-0.00031** | [-0.00080, +0.00017] | 10.0% | 0, e rulata deja | nesemnificativa, nu nula: P(>0) = 10.0%, CI include zero; strica in plus de, fr cu interval care exclude zero |
| 5 | al treilea termen pentru dezacord | plafon | +0.00231 | [+0.00045, +0.00436] | 99.0% | o zi de cod in `fit_choice` | podeaua de zgomot pe 2 coloane e +0.00121, deci excedentul real e ~+0.00110; **sub pragul de +0.002**, se inchide |
| 6 | reziduul de fertilitate, global | plafon | +0.00723 | [+0.00365, +0.01092] | 100.0% | re-antrenarea bratului A | plafonul e mare, dar la TRANSFER da -0.00153 [-0.00186, -0.00122], adica **strica cu interval care exclude zero**; semnul coeficientului cade la fel pe doar 4/10 limbi. Se inchide ca termen global. |
| 7 | distributia intreaga ca trasaturi | masurat, LOLO | -0.0185 pe bratul B |  |  | o zi de cod in bratul A | citirea liniara optima a celor 5 probabilitati, aleasa LOLO, e SUB `B` (+0.6407 fata de +0.6592); in-sample da +0.6760, deci nu transfera. Se inchide. |
| 8 | scara de raspuns 0-9 | masurat pe trial | **-0.0099** | [-0.0259, +0.0052] | 9.8% | sondajul de trial e rulat; confirmarea pe test ar fi ~102 min | **se inchide**: proxy-ul prezicea negativ, curba r(K) avand varful la K=3 si nu la K=5, si sondajul confirma: -0.0099 cu CI care include zero, si semn negativ pe toate trei contrastele. Efectul ancorei -0.0081, al atomilor -0.0018 |
| 9 | pozitia de citire, prefix fortat | cost declarat | - |  |  | ~5.5 min trial | nemasurabil pe disc: schimba distributia, nu citirea ei |
| 10 | few-shot din CELELALTE limbi | masurat pe trial in E.10 | +0.011 pe bratul B |  |  | ~3.8 ore pe test, la 2.44 s per item | **NU e netestata**: `prompt_lab.lolo_shots` ia exemplele numai din celelalte limbi, deci `v3_fewshot` din `output/e10_prompt.md` E chiar asta, si da +0.697 fata de +0.686 al semnalului B de acum, cea mai buna varianta individuala pe Gemma. Lipseste doar rularea pe TEST si trecerea prin fuziune, ca **configuratie fixa** pe toate limbile: selectia LOLO peste variante a pierdut deja (+0.6808 fata de +0.6860), varianta fixa nu are penalizarea aia. Singura de pe lista cu valoare de REVENDICARE peste cifra, fiindca G-Eval e 3-shot in limba tinta |
| 11 | cuantizare 8 biti pentru Gemma | cost declarat | - |  |  | ore de inferenta | control de confound, nu parghie de castig |
| 12 | prompturi 3 si 4, decorelate | cost declarat | - |  |  | 8.2 ore per model pe test | `output/e10_verdict.md` a masurat deja de ce nu: corelatia medie intre prompturile Gemmei e 0.772, si medierea repara un model slab, nu unul bun |

**Ce s-a mutat.** `prio_K` trece bara pe care lucrarea a folosit-o de fiecare data: r = **0.685530**, adica **+0.00168** fata de 0.683849, interval pereche [+0.00072, +0.00269], P(>0) = 100.0%, hiperparametrul ales LOLO, zero limbi stricate. **Nu se adopta in acest raport**: decizia e a lui Alexandru, si vine cu bifurcatia declarata mai sus, fiindca parghia a fost gasita uitandu-se la o cifra de test.

Pretul ei e zero: aceeasi inferenta, aceleasi distributii de pe disc, doar alta citire a lor. Iar mecanismul e citibil, si e chiar cel din blocul 3: nu adauga informatie, RESPATIAZA nivelurile, si respatierea grosiera bate spatierea egala fiindca eticheta nu e liniara in nota.

**Ce se inchide definitiv**, cu cifra care le inchide: al treilea termen pentru dezacord (excedentul peste podeaua de zgomot, ~+0.00110, e sub pragul de +0.002), fertilitatea ca termen global (-0.00153 la transfer, cu CI care exclude zero in jos), distributia intreaga ca trasaturi (citirea optima LOLO e sub `B`), media geometrica (negativa), si scara de raspuns 0-9 (-0.0099 pe trial, semn negativ pe toate trei contrastele).

**Ce rams de rulat**, in ordine: few-shot din celelalte limbi PE TEST, ~3.8 ore, fiindca pe trial e deja cea mai buna varianta individuala si e singura cu valoare de revendicare; pozitia de citire, ~6 min pe trial. Sondajul de scara e rulat si inchis.


---
Rulat in 74.0 s.
