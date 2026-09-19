# §3.5 Franceza, diagnosticata

Generat 2026-08-18 13:34:44 de `analysis_fr.py`. Setul e cel de DUPA §3.1 si §3.3, adica sistemul de 0.664555 din `output/e_fusion_lolo_ens.md`, reprodus bit cu bit inainte de orice masuratoare de aici.

## De ce franceza, si de ce nu poate fi un defect de brat

| | r pe franceza |
|---|---|
| semnalul A, ansamblu de surse plus `fert_inloc` | +0.5370 |
| semnalul B, nota LLM, `qwen35-9b-8bit` | +0.5440 |
| fuziunea, adica sistemul | +0.5883 |

Franceza e printre cele mai slabe limbi ale sistemului: peste `si` si `ca` in r absolut, sub restul. Prin fertilitate a urcat de la 0.5823 la 0.5883, deci +0.0060, dar intervalul pereche al acelei imbunatatiri, [-0.0020, +0.0142], include zero, deci singura nu se sustine.

Constatarea care restrange caut area: **A si B eseueaza CORELAT**. A e o regresie peste embedding XLM-R inghetat plus lexical, B e o nota ceruta unui LLM. Nu au nicio componenta comuna in afara de datele si de etichete. Doua semnale fara nimic comun care cad amandoua pe o singura limba arata spre date sau spre protocolul de adnotare, nu spre un brat.

## 1. Cele 3 tinte negasite ca subsir. Confirmate, si fara efect

Contabilitatea completa a francezei: fisierul oficial `multils_test_french_lcp_labels.tsv` are **569** randuri, `load_mlsp` incarca **569**, iar sistemul evalueaza **566**.

Cele **3** randuri pierdute sunt exact tintele pe care `find_char_span` nu le gaseste in propriul context, nici brut, nici dupa `normalize_token`:

| tinta | dupa normalizare | complexitate | de ce nu se gaseste |
|---|---|---|---|
| `effectuer` | `effectuer` | 0.400 | contextul are `Effectuer`, la inceput de propozitie, iar `find_char_span` compara sensibil la caz |
| `impulser` | `impulser` | 0.250 | contextul are `Impulser`, la inceput de propozitie, iar `find_char_span` compara sensibil la caz |
| `défendue` | `défendue` | 0.350 | contextul are `Défendue`, la inceput de propozitie, iar `find_char_span` compara sensibil la caz |

Ele cad din evaluare prin masca `ok` a lui `embed_frame`, la fel ca cele 18 instante din 5624 despre care raportul spune deja ca rama in afara evaluarii. Deci **nu sunt o pierdere de r, sunt o pierdere de n**: 569 minus 3 da exact 566, numarul evaluat.

Si nu e un fenomen francez. Aceeasi numaratoare pe toate cele 10 limbi:

| limba | incarcate de `load_mlsp` | negasite ca subsir | din care doar din CAZ | evaluate de sistem |
|---|---|---|---|---|
| ca | 445 | 0 | 0 | 445 |
| de | 570 | 0 | 0 | 570 |
| en | 570 | 0 | 0 | 570 |
| es | 593 | 0 | 0 | 593 |
| fil | 570 | 2 | 2 | 568 |
| **fr** | 569 | **3** | 3 | 566 |
| it | 570 | 8 | 8 | 562 |
| ja | 570 | 0 | 0 | 570 |
| pt | 567 | 5 | 5 | 562 |
| si | 600 | 0 | 0 | 600 |

Italiana pierde 8 si portugheza 5, adica mai mult ca franceza, si amandoua stau mult mai bine in r. **Punctul 1 se inchide negativ:** cele 3 tinte sunt reale, sunt explicate, si nu explica nimic din deficitul francez.

Dar iese altceva, si e un defect adevarat, doar nu al francezei. **Toate cele 18** instante pierdute pe tot setul, in toate cele patru limbi, se pierd dintr-un singur motiv: litera mare de inceput de propozitie. `find_char_span` la [solution_bert.py:84](solution_bert.py#L84) face `text.find(tok)`, sensibil la caz, deci o tinta data cu minuscula care apare prima in propozitie nu se gaseste niciodata. E o reparatie de o linie care recupereaza 18 instante din 5624. **Nu se atinge aici**, fiindca ar schimba n si deci fiecare cifra publicata, si nu e sarcina de acum; se raporteaza ca de facut.

## 2. Cea mai mare deviatie standard din set. Tine, dar premisa e inversa

| limba | n | medie | **sd** | valori distincte | numitorul grilei | adnotatori | pas | r sistem |
|---|---|---|---|---|---|---|---|---|
| **fr** | 569 | 0.3200 | **0.2494** | 40 | 1/40 | 10.0 | 0.0250 | +0.5883 |
| ja | 570 | 0.3411 | 0.2080 | 37 | 1/40 | 10.0 | 0.0250 | +0.7887 |
| en | 570 | 0.2383 | 0.1918 | 69 | 1/3960 | variabil | 0.0003 | +0.8657 |
| es | 593 | 0.3546 | 0.1882 | 53 | 1/520 | variabil | 0.0019 | +0.7484 |
| it | 570 | 0.2772 | 0.1677 | 62 | 1/100 | 25.0 | 0.0100 | +0.6616 |
| de | 570 | 0.5019 | 0.1645 | 32 | 1/40 | 10.0 | 0.0250 | +0.7311 |
| ca | 445 | 0.3912 | 0.1543 | 92 | 1/1180080 | variabil | 0.0000 | +0.5288 |
| pt | 567 | 0.2557 | 0.1482 | 60 | 1/100 | 25.0 | 0.0100 | +0.8403 |
| fil | 570 | 0.2528 | 0.1475 | 28 | 1/40 | 10.0 | 0.0250 | +0.5197 |
| si | 600 | 0.2024 | 0.1274 | 50 | 1/100 | 25.0 | 0.0100 | +0.3729 |

**Cifra tine.** Franceza are sd = 0.2494, cea mai mare din tot setul, exact ca in planul vechi.

Dar planul o trecea in dreptul defectelor, si asta nu se susține. O eticheta mai imprastiata da in principiu **mai mult** semnal de corelat, nu mai puțin: imprastierea etichetei e la numitorul lui r. Deci se testeaza direct, peste cele 10 limbi.

Corelatia dintre sd al etichetei si r al sistemului e **+0.3565**, cu panta +1.5956 r pe unitate de sd. Adica imprastierea chiar ajuta, si franceza are cea mai multa.

| limba | sd | r sistem | r prezis din sd | **rezidual** |
|---|---|---|---|---|
| si | 0.1274 | +0.3729 | +0.5890 | -0.2162 |
| **fr** | 0.2494 | +0.5883 | +0.7837 | **-0.1955** |
| ca | 0.1543 | +0.5288 | +0.6320 | -0.1031 |
| fil | 0.1475 | +0.5197 | +0.6212 | -0.1015 |
| it | 0.1677 | +0.6616 | +0.6534 | +0.0082 |
| es | 0.1882 | +0.7484 | +0.6860 | +0.0623 |
| ja | 0.2080 | +0.7887 | +0.7176 | +0.0710 |
| de | 0.1645 | +0.7311 | +0.6483 | +0.0827 |
| en | 0.1918 | +0.8657 | +0.6919 | +0.1738 |
| pt | 0.1482 | +0.8403 | +0.6223 | +0.2181 |

Franceza are rezidualul **-0.1955**, al 2-lea de jos din 10. Deci franceza nu e slaba pentru ca eticheta ei e imprastiata; e slaba **in ciuda** faptului ca eticheta ei e cea mai imprastiata din set, adica cea mai usor de corelat. **Punctul 2 se inchide cu premisa confirmata si consecinta respinsa.**

### Ce iese in schimb din grila etichetelor

Coloanele de grila nu erau in plan si se citesc gratis din aceleasi etichete. Eticheta MLSP e media a N note pe o scara Likert de 5 puncte mapata pe multiplii de 0.25, deci fiecare eticheta e un multiplu de 1/(4N) si numitorul ei redus divide 4N. Cel mai mic multiplu comun al numitorilor din limba da grila, iar grila da N.

Setul se rupe in trei grupe curate:

- grila 1/40, adica **10 adnotatori** pe fiecare item: `de`, `fil`, `fr`, `ja`;
- grila 1/100, adica **25 de adnotatori**: `it`, `pt`, `si`;
- numitori care nu se divid intre ei, adica numar **variabil** de adnotatori de la un item la altul: `ca`, `en`, `es`.

Franceza e in grupa cea mai grosiera. Media a N note are eroarea standard proportionala cu 1/sqrt(N), deci o limba cu 10 adnotatori are o eticheta mai zgomotoasa per item si un plafon de r mai jos decat una cu 25, **independent de orice model**.

**Dar nici asta nu explica franceza**, si se vede in aceeasi coloana. In grupa de 10 adnotatori intra si `ja` (+0.7887), `de` (+0.7311), `fr` (+0.5883), `fil` (+0.5197). Doua limbi cu exact aceeasi grila ca franceza trec de 0.73. Grila e o constrangere reala si masurata, dar nu e cea care leaga aici.

Onest, fiindca altfel cifra ar fi supravanduta: N citit din grila e o margine INFERIOARA. Se citeste din cel mai fin pas prezent efectiv in etichete, deci o limba unde nicio medie n-a cazut pe o fractie fina iese cu N mai mic decat cel real. Nu inlocuieste numarul de adnotatori din documentatia MLSP, care **n-a fost verificat**.

## 3. Acoperirea `wordfreq` pe formele flexionate franceze

`r` e dat cu semnul intors, adica corelatia lui **neg-zipf** cu complexitatea, ca sa fie pozitiv si comparabil cu restul lucrarii: un cuvant rar e greu. `forma` e tokenul asa cum apare, `lema` e lema lui `stanza`, `best` e `max(zipf_forma, zipf_lema)`, adica exact ce primeste sistemul prin `--lemma-freq`.

| limba | n | limba acoperita | zipf 0 pe forma | zipf 0 dupa lema | salvate de lema | lema difera | r forma | r lema | **r best** | castigul lemei |
|---|---|---|---|---|---|---|---|---|---|---|
| ca | 445 | da | 31 | 16 | 15 | 215 | +0.3014 | +0.3139 | +0.3213 | +0.0199 |
| de | 570 | da | 31 | 19 | 12 | 276 | +0.5912 | +0.6191 | +0.6295 | +0.0383 |
| en | 570 | da | 6 | 6 | 0 | 214 | +0.7472 | +0.6943 | +0.7372 | -0.0100 |
| es | 593 | da | 5 | 2 | 3 | 339 | +0.5513 | +0.5440 | +0.6082 | +0.0569 |
| fil | 570 | da | 152 | 152 | 0 | 0 | +0.3890 | n/a | +0.3890 | +0.0000 |
| **fr** | 569 | da | **6** | 3 | 3 | 275 | +0.5192 | +0.5349 | **+0.5491** | +0.0299 |
| it | 570 | da | 18 | 9 | 9 | 305 | +0.5195 | +0.5627 | +0.6029 | +0.0834 |
| ja | 570 | da | 4 | 0 | 4 | 384 | +0.6042 | +0.3858 | +0.5382 | -0.0659 |
| pt | 567 | da | 8 | 3 | 5 | 220 | +0.7247 | +0.7069 | +0.7419 | +0.0172 |
| si | 600 | **nu** | 600 | 600 | 0 | 0 | n/a | n/a | n/a | n/a |

**Punctul 3 se inchide negativ pe intrebarea pusa, dar scoate la iveala altceva.**

Pe acoperire, nimic. Franceza are 6 tinte din 569 cu zipf zero pe forma, adica 1.1%, si 3 dupa ce lema actioneaza. E la egalitate cu engleza, care e cea mai buna limba a sistemului. Cazurile patologice ale setului sunt `fil`, cu 152 din 570, si `si`, unde limba nu e servita deloc. Franceza nu are o gaura de acoperire.

Pe informativitate, tot nimic in defavoarea francezei: `r best` e +0.5491, si 3 din celelalte limbi stau mai jos. Frecventa franceza functioneaza normal. Lema aduce +0.0299 desi 275 din 569 tinte, adica 48.3%, au lema diferita de forma. Deci franceza chiar e flexionata si lematizarea chiar muta formele, doar ca nu era nimic de recuperat.

### Ce iese in schimb: o singura coloana bate 770

Comparatia care nu era cerută dar cade din acelasi tabel. `r best` e **o singura trasatura**, neg-zipf. `r A` e semnalul A intreg: embedding XLM-R de 768 de dimensiuni, plus lexicalul, plus ansamblul celor doua brate de transfer, plus fertilitatea in locul lungimii.

| limba | `r best`, o coloana | `r A`, semnalul intreg | **best − A** | r sistem |
|---|---|---|---|---|
| **fr** | +0.5491 | +0.5370 | **+0.0121** | +0.5883 |
| it | +0.6029 | +0.6311 | -0.0282 | +0.6616 |
| fil | +0.3890 | +0.4174 | -0.0284 | +0.5197 |
| de | +0.6295 | +0.6666 | -0.0371 | +0.7311 |
| pt | +0.7419 | +0.7804 | -0.0386 | +0.8403 |
| es | +0.6082 | +0.6574 | -0.0492 | +0.7484 |
| ja | +0.5382 | +0.6012 | -0.0630 | +0.7887 |
| en | +0.7372 | +0.8139 | -0.0767 | +0.8657 |
| ca | +0.3213 | +0.4297 | -0.1083 | +0.5288 |
| si | n/a | +0.2693 | n/a | +0.3729 |

Pe franceza o singura coloana de frecventa da +0.5491, iar semnalul A intreg da +0.5370, deci **+0.0121 in favoarea coloanei singure**. Limbile unde asta se intampla sunt `fr`, iar franceza e cea mai clara.

E acelasi lucru pe care il spunea deja descompunerea pe blocuri, cu alte cifre si pe configuratia veche: pe franceza blocul lexical singur bate sistemul intreg, 0.542 fata de 0.531. Aici se confirma pe configuratia curenta, cu ansamblu de surse si fertilitate in cod, si se restrange: nu e blocul lexical de 7 coloane, e **o coloana**.

Ce inseamna. Diagnosticul pe care il sprijina masuratorile nu e „datele franceze sunt defecte”, e **embeddingul nu transfera pe franceza**, si pe deasupra dilueaza o trasatura care singura ar merge mai bine. Nu contrazice constatarea ca A si B cad corelat, fiindca B nu foloseste embeddingul; le pune insa in ordine, prima cauza fiind brațul A.

## 4. Reziduul de fertilitate, cat a mai ramas dupa `fert_inloc`

`r orig` e masuratoarea din §3.3, refacuta: corelatia fertilitatii cu ETICHETA, dupa ce se scot lungimea si zipf din amandoua. E reziduul de dinainte de reparatie.

Celelalte trei coloane raspund la intrebarea „cat a mai ramas” prin **validitate incrementala**: aceeasi corelatie partiala, dar cu predictia adaugata la controale, pe ambele laturi. Zero inseamna ca predictia a luat deja tot ce avea de dat fertilitatea. Se face asa, si nu ca corelatie a fertilitatii cu eroarea bruta `y − p`, fiindca varianta cu eroarea bruta iese NEGATIVA pe toate cele zece limbi, inclusiv pe engleza si germana, care pornesc de la un reziduu de zero. Adica masoara cat de mult foloseste modelul trasatura, nu cat a rămas din ea. A fost calculata, si nu se raporteaza.

| limba | n | fertilitate medie | `r orig`, vs eticheta | partial vs A `baza` | partial vs A `fert_inloc` | **partial vs sistem** | CI 95% pe contexte |
|---|---|---|---|---|---|---|---|
| si | 600 | 3.32 | +0.2657 | +0.2122 | +0.1757 | +0.1227 | [+0.0585, +0.1861] (exclude zero) |
| **fr** | 569 | 2.02 | **+0.2167** | +0.1738 | +0.1887 | **+0.1450** | [+0.0589, +0.2238] (exclude zero) |
| ja | 570 | 3.37 | +0.1951 | +0.1515 | +0.1700 | +0.0722 | [-0.0219, +0.1598] |
| es | 593 | 1.96 | +0.1717 | +0.0274 | +0.0833 | -0.0242 | [-0.1119, +0.0631] |
| ca | 445 | 2.61 | +0.0822 | +0.0072 | +0.0297 | +0.0039 | [-0.0922, +0.0962] |
| pt | 567 | 2.08 | +0.0341 | -0.0897 | -0.0937 | -0.0995 | [-0.1863, -0.0179] (exclude zero) |
| it | 570 | 2.36 | +0.0335 | -0.0572 | -0.0441 | -0.0550 | [-0.1366, +0.0305] |
| fil | 570 | 2.37 | +0.0144 | -0.0309 | -0.0221 | -0.0410 | [-0.1396, +0.0532] |
| en | 570 | 1.88 | -0.0111 | -0.0763 | -0.0456 | -0.0182 | [-0.1094, +0.0813] |
| de | 570 | 2.56 | -0.0212 | -0.1029 | -0.0782 | -0.1692 | [-0.2370, -0.0951] (exclude zero) |

**Cifra din plan se confirma exact:** franceza are `r orig` = **+0.2167**, al 2-lea din set, adica +0.2167 de acolo.

**Dar reziduul NU e consumat, si asta e singurul lucru din toata lista care mai e de facut.** Fata de sistemul intreg fertilitatea are inca validitate incrementala **+0.1450**, cu intervalul pe contexte [+0.0589, +0.2238], care **exclude zero**. Adica fertilitatea mai spune ceva despre eticheta franceza pe care sistemul nu il ia.

Si nu scade prin `fert_inloc`. Cu brațul A de dinainte, setul `baza`, corelatia partiala e +0.1738; cu setul `fert_inloc`, care e chiar cel din sistem, e +0.1887, adica la fel sau puțin mai sus. Coboara doar la +0.1450, si asta prin amestecul cu semnalul B, nu prin coloana de fertilitate.

Ce a facut totusi `fert_inloc` pe franceza, masurat direct pe brațul A cu bootstrap pereche pe 191 contexte:

| brat A pe franceza | r |
|---|---|
| set `baza`, lungime in caractere | +0.5305 |
| set `fert_inloc`, fertilitate in locul lungimii | +0.5406 |
| **diferenta** | **+0.0100**, CI [+0.0027, +0.0174], P(>0) = 99.5% |

Deci a ajutat, +0.0100 cu interval care exclude zero, dar a ajutat **fara sa ia reziduul**. Cele doua nu se contrazic: `fert_inloc` pune fertilitatea ca una din 770 de coloane intr-un `Ridge + HGB`, deci ii ia partea liniara comuna, nu tot ce are de dat pe franceza.

**Punctul 4 se inchide ca DESCHIS.** E singurul din cele patru care rămane. Limbile cu reziduu POZITIV si interval care exclude zero sunt `fr`, `si`, iar franceza are cel mai mare dintre ele. `ja` e a treia din trioul prezis de §3.3 si merge in aceeasi directie, +0.0722, dar intervalul ei include zero.

Si o avertizare pentru orice reparatie care ar urma. Pe `de` (-0.1692) si `pt` (-0.0995) reziduul e NEGATIV cu interval care exclude zero, adica acolo sistemul foloseste fertilitatea prea mult. O forma mai puternica de fertilitate, pusa global, ar strica exact pe limbile alea. Daca se face, se face pe limbile unde reziduul e pozitiv, si alegerea limbilor trebuie sa treaca prin LOLO ca tot restul.

## Verdictul

**Trei din cele patru ipoteze se resping, a patra rămane deschisa.** Cele trei se confirma ca cifra si se resping ca explicatie, ceea ce nu e acelasi lucru cu a fi false.

| punct | ce spunea planul | ce iese | consecinta |
|---|---|---|---|
| 1, tinte negasite | 3 tinte franceze nu se gasesc ca subsir | **confirmat, exact 3** | pierdere de n, nu de r. `it` pierde 8 si `pt` 5, amandoua cu r mai bun |
| 2, imprastierea etichetei | sd 0.2494, cea mai mare din set | **confirmat, 0.2494** | premisa inversa: peste cele 10 limbi imprastierea AJUTA r, deci franceza e slaba in ciuda ei |
| 3, acoperire `wordfreq` | formele flexionate franceze ar putea cadea | **respins**, 6/569 zipf zero, la egalitate cu engleza | frecventa franceza functioneaza normal |
| 4, reziduu de fertilitate | +0.2167 partial nereparat | **confirmat, si inca nereparat**: +0.1450 validitate incrementala peste sistem, interval [+0.0589, +0.2238], exclude zero | **singurul punct care rămane deschis** |

### Ce rămane de facut, si e un singur lucru

Punctul 4. Fertilitatea are inca **+0.1450** validitate incrementala peste sistem pe franceza, interval [+0.0589, +0.2238] care exclude zero, si `fert_inloc` nu a schimbat asta: corelatia partiala e +0.1738 cu setul `baza` si +0.1887 cu `fert_inloc`. Coloana a intrat, r-ul brațului A a urcat cu +0.0100, dar reziduul a rămas. Explicatia care se potriveste cifrelor e ca fertilitatea intra ca una din 770 de coloane intr-un `Ridge + HGB`, deci i se ia doar partea comuna liniar. Ce ar testa asta e o forma neliniara sau interactiva a fertilitatii pe cele trei limbi unde intervalul exclude zero. **Nu s-a rulat**, e o modificare de trasaturi cu efect pe toate cifrele publicate.

### Ce s-a mai gasit, si nu era pe lista

**1. O coloana bate 770 pe franceza.** Neg-zipf singur da +0.5491, semnalul A intreg da +0.5370, deci +0.0121 in favoarea coloanei singure, cea mai mare diferenta din set. Diagnosticul pe care il sprijina masuratorile nu e ca datele franceze sunt defecte, e ca **embeddingul nu transfera pe franceza si dilueaza o trasatura care singura ar merge mai bine**. Se potriveste cu descompunerea pe blocuri de dinainte, 0.542 lexical fata de 0.531 tot, si o restrange de la 7 coloane la una.

**2. Grila etichetelor rupe setul in trei grupe.** Franceza e in cea mai grosiera, 1/40, adica 10 adnotatori per item, contra 25 la `it`, `pt`, `si` si numar variabil la `en`, `es`, `ca`. Plafonul de r scade cu 1/sqrt(N), deci constrangerea e reala. **Dar nu explica franceza:** in aceeasi grupa de 10 adnotatori stau `ja` (+0.7887), `de` (+0.7311), `fil` (+0.5197), deci doua limbi cu exact aceeasi grila trec de 0.73.

**3. Un defect de cod adevarat, dar nu al francezei.** Toate cele 18 instante pierdute pe tot setul, in `fr`, `fil`, `it` si `pt`, se pierd numai fiindca `find_char_span` e sensibil la caz si tinta e primul cuvant din propozitie. Reparatie de o linie, recupereaza n, nu r. Nu s-a atins: ar schimba n si deci fiecare cifra publicata.

### Ce se scrie in lucrare

Franceza rămane o limba slaba a sistemului, la +0.5883, **fara un defect de date identificat**. Trei din cele patru ipoteze verificabile se resping. A patra, reziduul de fertilitate, nu se respinge: e inca acolo, +0.1450 peste sistem cu interval care exclude zero, si e singurul lucru masurat care mai promite ceva.

Ce a ieșit peste lista muta a doua cauza dinspre date inspre brațul A: pe franceza o singura trasatura de frecventa bate semnalul A intreg, +0.5491 fata de +0.5370, ceea ce inseamna ca embeddingul XLM-R nu doar ca nu transfera acolo, ci dilueaza.

Asta nu contrazice constatarea de la care s-a plecat, ca A si B cad corelat, fiindca B nu foloseste embeddingul si cade independent. Le pune in ordine: sunt **doua** cauze, nu una, iar cea din brațul A e cea masurata si localizata aici.

**Ce ar testa direct ipoteza asta, si nu s-a rulat:** §3.6, encoder mai mare sau alt encoder sub LOLO. Daca embeddingul e problema pe franceza, atunci exact acolo ar trebui sa se vada cel mai mult diferenta intre encodere. E o rulare separata, cu aprobare.

**Trei din patru premise s-au confirmat in cifre si au fost respinse in consecinta.** Fara masuratoare, oricare din ele s-ar fi scris ca explicatie. A patra a supravietuit, dar numai dupa ce metrica a fost schimbata: prima versiune, corelatia fertilitatii cu eroarea bruta `y − p`, dadea negativ pe toate cele zece limbi si ar fi dus la concluzia inversa, ca reziduul e consumat.

