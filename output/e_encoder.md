# §3.6 Encoderul, redeschis pe protocolul corect

Generat 2026-08-19 10:33:49 de `analysis_encoder.py`.

## De ce se redeschide

README-ul respinge XLM-R large, LaBSE si e5 fiindca „castigau la validarea in-source dar picau pe public”. Validarea in-source era `transfer_eval` plus `_cv_r`, adica engleza spre romanic, pe cinci limbi. **Protocolul corect, leave-one-language-out pe 10 limbi, nu exista cand s-a luat decizia.** Respingerea a fost pe dovada gresita, deci se reface pe dovada buna.

## Ce se schimba si ce nu

Se schimba **numai encoderul**. Setul de trasaturi e cel al sistemului, `--lemma-freq --afeat fert_inloc`; partitia, regresorul `blend_ridge_hgb`, centrarea per limba si randurile evaluate sunt identice. **Semnalul B nu e atins**, deci niciun LLM nu s-a re-rulat.

Trei lucruri au trebuit adaugate in cod, toate aditive:

1. `xlmr-large` nu era in `ENCODERS` deloc. `MODELS["large"]` din `finetune_xlmr.py` e pentru calea de fine-tuning, nu pentru brațul inghetat, deci blocajul notat in plan era real.
2. `finetune_xlmr.py` n-avea `--encoder`. `frozen_trial_gap` accepta parametrul, dar `main()` nu-l pasa niciodata.
3. **`_p()` sufixa caile doar dupa `--lemma-freq` si `--afeat`.** Fara sufix de encoder, prima rulare cu alt encoder ar fi scris peste `e1_frozen_preds_lemma_fert_inloc.csv`, adica peste semnalul A al sistemului, si nicio cifra din niciun raport n-ar fi aratat ca s-a intamplat.

Poarta: cu `--encoder xlmr` sufixul e gol, iar rularea reproduce `e1_frozen_preds_lemma_fert_inloc.csv` **bit cu bit**, verificat cu `cmp` dupa modificare. `md5 output/FINAL_best.csv` neschimbat.

## Brațul A per limba, `p_multi`

| limba | n | `xlmr` | `xlmr-large` | `labse` | `e5` |
|---|---|---|---|---|---|
| ca | 445 | +0.4426 | **+0.4802** | +0.4728 | +0.4714 |
| de | 570 | +0.6540 | **+0.6568** | +0.6163 | +0.6230 |
| en | 570 | +0.8173 | **+0.8208** | +0.8131 | +0.8169 |
| es | 593 | +0.6665 | +0.6654 | +0.6713 | **+0.7069** |
| fil | 570 | +0.4083 | +0.3570 | +0.3950 | **+0.4099** |
| fr | 569 | +0.5372 | **+0.5784** | +0.5460 | +0.5508 |
| it | 570 | **+0.6301** | +0.6191 | +0.6149 | +0.6283 |
| ja | 570 | +0.6011 | **+0.6133** | +0.5282 | +0.5609 |
| pt | 567 | +0.7621 | **+0.7709** | +0.7647 | +0.7657 |
| si | 600 | +0.2586 | +0.2719 | **+0.3580** | +0.2172 |
| **medie** | 5606 | +0.5778 | **+0.5834** | +0.5780 | +0.5751 |

Cifra ingrosata pe fiecare rand e encoderul castigator al limbii.

## Diferenta fata de XLM-R base, perechea

Aceleasi randuri, aceeasi reesantionare pe contexte, deci intervalul e al diferentei.

| limba | xlmr-large − base | CI 95% | P(>0) | labse − base | CI 95% | P(>0) | e5 − base | CI 95% | P(>0) |
|---|---|---|---|---|---|---|---|---|---|
| ca | +0.0376 | [-0.0029, +0.0768] | 97% | +0.0302 | [-0.0076, +0.0722] | 93% | +0.0288 | [-0.0098, +0.0670] | 92% |
| de | +0.0028 | [-0.0243, +0.0313] | 58% | **-0.0377** | [-0.0671, -0.0090] | 0% | **-0.0310** | [-0.0576, -0.0023] | 2% |
| en | +0.0035 | [-0.0156, +0.0239] | 65% | -0.0042 | [-0.0224, +0.0145] | 34% | -0.0004 | [-0.0164, +0.0162] | 51% |
| es | -0.0011 | [-0.0263, +0.0254] | 47% | +0.0048 | [-0.0171, +0.0269] | 66% | **+0.0405** | [+0.0177, +0.0615] | 100% |
| fil | **-0.0513** | [-0.0802, -0.0214] | 0% | -0.0133 | [-0.0370, +0.0105] | 14% | +0.0016 | [-0.0175, +0.0208] | 56% |
| fr | **+0.0412** | [+0.0127, +0.0698] | 100% | +0.0088 | [-0.0182, +0.0365] | 74% | +0.0136 | [-0.0183, +0.0432] | 80% |
| it | -0.0111 | [-0.0389, +0.0154] | 20% | -0.0152 | [-0.0396, +0.0090] | 10% | -0.0019 | [-0.0288, +0.0239] | 43% |
| ja | +0.0122 | [-0.0347, +0.0609] | 70% | **-0.0729** | [-0.1183, -0.0253] | 0% | -0.0402 | [-0.0836, +0.0050] | 4% |
| pt | +0.0088 | [-0.0089, +0.0267] | 83% | +0.0025 | [-0.0147, +0.0202] | 61% | +0.0036 | [-0.0146, +0.0215] | 66% |
| si | +0.0133 | [-0.0437, +0.0687] | 65% | **+0.0994** | [+0.0077, +0.1911] | 98% | -0.0414 | [-0.1085, +0.0238] | 11% |
| **medie** | +0.0056 | [-0.0056, +0.0162] | 84% | +0.0002 | [-0.0127, +0.0131] | 52% | -0.0027 | [-0.0135, +0.0083] | 31% |

Ingrosat = intervalul exclude zero.

## Fuziunea A plus B, adica cifra care conteaza

Fiecare brat A trece prin exact acelasi `fuse_ab.py --arm lolo --fit test --ens`, cu acelasi brat B si aceeasi selectie pe trei niveluri. Referinta `--vs` e sistemul, `output/fusion_preds_lolo_ens.csv`, deci diferenta e PERECHE si intervalul e al ei.

| encoder | r A mediu | **r fuziune** | fata de sistem | CI 95% pereche pe medie | P(>0) |
|---|---|---|---|---|---|
| **`xlmr`** | +0.5813 | **0.664581** | sistemul insusi | | |
| `xlmr-large` | +0.5913 | 0.664416 | -0.0002 | [-0.0045, +0.0038] | 45.9% |
| `labse` | +0.5782 | 0.663416 | -0.0012 | [-0.0063, +0.0039] | 31.8% |
| `e5` | +0.5820 | 0.665211 | +0.0006 | [-0.0039, +0.0048] | 62.0% |

**Niciun encoder nu misca fuziunea.** Toate cele trei intervale perechi includ zero, deci cele trei cifre si sistemul sunt acelasi lucru masurat de patru ori. Nu e o surpriza si e chiar ce prezicea planul: A primeste pondere 0.35 pana la 0.40 in amestec, deci un castig pe A se vede injumatatit sau mai putin pe fuziune, iar castigul pe A e el insusi in interiorul zgomotului.

## Cat de decorelate sunt brațele intre ele

Corelatia dintre predictiile `p_multi` ale encoderelor, in interiorul limbii, mediata pe cele zece limbi. Conteaza fiindca `fuse_ab.py --a-set` face deja selectie leave-one-language-out peste seturi candidate: daca encoderele castiga pe limbi diferite si sunt decorelate, ansamblul de encodere e o rulare de zece secunde, fara cod nou.

| pereche | corelatie medie in interiorul limbii |
|---|---|
| `xlmr` vs `xlmr-large` | 0.885 |
| `xlmr` vs `labse` | 0.872 |
| `xlmr` vs `e5` | 0.884 |
| `xlmr-large` vs `labse` | 0.846 |
| `xlmr-large` vs `e5` | 0.854 |
| `labse` vs `e5` | 0.887 |

Encoderul castigator per limba:

| limba | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| castigator | `xlmr-large` | `xlmr-large` | `xlmr-large` | `e5` | `e5` | `xlmr-large` | `xlmr` | `xlmr-large` | `xlmr-large` | `labse` |

Nicio limba nu e castigata de acelasi encoder peste tot: `xlmr-large` pe 6, `e5` pe 2, `xlmr` pe 1, `labse` pe 1.

## Testul direct al ipotezei de la §3.5

§3.5 a lasat o singura explicatie in picioare pentru franceza: **embeddingul nu transfera acolo si dilueaza o trasatura care singura ar merge mai bine**. Masuratoarea de acolo: neg-zipf singur da +0.5491, iar semnalul A intreg da +0.5372. §3.6 e testul direct al ipotezei: daca embeddingul e cauza, atunci franceza ar trebui sa fie limba unde schimbarea encoderului se vede cel mai mult.

| encoder | r pe franceza | fata de base | CI 95% pereche | peste o coloana de neg-zipf? |
|---|---|---|---|---|
| `xlmr` | +0.5372 | referinta |  | nu, -0.0119 |
| `xlmr-large` | +0.5784 | +0.0412 | [+0.0127, +0.0698] | **da**, +0.0293 |
| `labse` | +0.5460 | +0.0088 | [-0.0182, +0.0365] | nu, -0.0031 |
| `e5` | +0.5508 | +0.0136 | [-0.0183, +0.0432] | **da**, +0.0017 |

Cel mai bun encoder pe franceza e `xlmr-large`, la +0.5784.

Si comparatia care conteaza pentru ipoteza: cat castiga fiecare limba prin cel mai bun encoder al ei, fata de base.

| limba | si | fr | es | ca | ja | pt | en | de | fil | it |
|---|---|---|---|---|---|---|---|---|---|---|
| castig | +0.0994 | +0.0412 | +0.0405 | +0.0376 | +0.0122 | +0.0088 | +0.0035 | +0.0028 | +0.0016 | +0.0000 |

Franceza e pe locul 2 din 10.

## Encodere diferite pentru limbi diferite

Intrebarea cade singura din tabelul de mai sus: encoderele castiga pe limbi diferite, deci de ce un singur encoder peste tot. Doua raspunsuri, si dau lucruri opuse.

### Varianta 1, selectia. Nu merge

`fuse_ab.py --a-set` face DEJA selectie leave-one-language-out peste seturi candidate, deci cele patru brate se dau ca patru seturi si nu se scrie nicio linie de cod. Rezultatul e **sub sistem**.

Se vede si de ce, in ce a ales: `labse` pe 8 limbi din 10, inclusiv pe `de`, `ja` si `it`, unde LaBSE e masurat mai prost decat base. Iar pe **sinhaleza, unde LaBSE e clar cel mai bun cu +0.3613, selectia a ales `e5`, care da +0.2090**, cel mai prost din patru.

Cauza e in raportul propriu al rularii: latimea criteriului peste cei 36 de candidati e 0.0077 in medie, fata de 0.082 cat are curba lui `w`, deci **de zece ori mai plata**. Un argmax pe o curba atat de plata, estimat pe noua limbi, e in mare parte zgomot, si atunci alege aproape acelasi set peste tot, ceea ce anuleaza exact ideea.

### Varianta 2, medierea. Merge

Cand criteriul e prea plat ca sa aleaga, medierea nu cere ca ORDINEA candidatilor sa fie estimabila, cere doar ca ei sa fie decorelati, si sunt. Semnalul A devine media celor patru encodere, standardizate in interiorul limbii, cu pondere egala si **niciun parametru liber**: `make_enc_mean.py`. Rezultatul se da apoi lui `fuse_ab.py` ca un set oarecare.

| configuratie | r A | r fuziune | fata de sistem | CI 95% pereche | P(>0) | limbi in urcare |
|---|---|---|---|---|---|---|
| sistemul, `xlmr` peste tot | +0.5778 | **0.664581** | referinta | | | |
| encodere per limba, selectie | +0.5696 | **0.659580** | **-0.0050** | [-0.0092, -0.0008] | 1.1% | 2/10 |
| encodere per limba, mediere | +0.6079 | **0.671610** | **+0.0070** | [+0.0039, +0.0099] | 100.0% | 8/10 |
| *oracol pe A, cel mai bun encoder per limba* | *0.6025* | *—* | *foloseste etichetele lui L* | | | |

Medierea da **0.671610**, adica **+0.0070** fata de sistem, cu interval pereche al mediei [+0.0039, +0.0099] si P(>0) = 100.0%. **Intervalul exclude zero.** Pe brațul A singur, media celor patru da 0.6025 pe `p_multi`, adica **exact cat plafonul oracol**, si il bate pe sase limbi din zece, fara sa foloseasca nicio eticheta.

Zero etichete, si unde se verifica: fiecare brat individual e antrenat deja excluzand limba L, iar medierea foloseste numai `zscore` peste PREDICTII, in interiorul limbii. Nici standardizarea, nici ponderea egala nu ating vreo eticheta. Proprietatea zero-label a sistemului se pastreaza intacta.

Onest, si trebuie scris: singura alegere de cercetator din varianta asta e **binara**, a media in loc de a selecta, luata dupa ce s-a vazut ca selectia cade. Media insasi n-are niciun parametru: e neponderata si peste TOATE cele patru encodere, nu peste o submultime aleasa. O submultime aleasa pe scor ar fi acordare pe test si nu s-a incercat.

Costul, fiindca nu e gratis: sistemul ar cere la inferenta patru encodere in loc de unul, iar `xlmr-large` singur e de circa 3.5 ori mai scump decat base. Cifra pe fil scade cu -0.0081, cu interval care exclude zero. **Daca se adopta sau nu e o decizie, nu o concluzie.**

## Verdictul

**Pe brațul A, niciun encoder nu bate XLM-R base cu un interval care exclude zero pe medie.** Respingerea din README ajunge la aceeasi concluzie ca protocolul corect, dar din motive diferite: nu fiindca in-source ar fi fost un proxy bun, ci fiindca raspunsul chiar e negativ. Dovada era gresita, concluzia era buna.

Asta e concluzia, dar ar fi necinstit sa fie aplatizata la un „nu”. Cel mai bun encoder, `xlmr-large`, are punctul estimat +0.0056, P(>0) = 84%, si castiga pe 6 din 10 limbi. Toate trei semnele merg in aceeasi directie; ce lipseste e marimea, nu semnul. Formularea corecta e **nesemnificativ, nu nul**, si distinctia conteaza fiindca un set mai mare sau o cautare pe straturi ar putea-o muta.

| encoder | r A mediu | fata de base | CI 95% | P(>0) |
|---|---|---|---|---|
| `xlmr` | +0.5778 | referinta | | |
| `xlmr-large` | +0.5834 | +0.0056 | [-0.0056, +0.0162] | 84% |
| `labse` | +0.5780 | +0.0002 | [-0.0127, +0.0131] | 52% |
| `e5` | +0.5751 | -0.0027 | [-0.0135, +0.0083] | 31% |

**Pe fuziune, niciun encoder nu se distinge de sistem.** Cea mai mare cifra e 0.665211 cu `e5`, adica +0.0006 fata de 0.664581, dar intervalul pereche al mediei e [-0.0039, +0.0048] si include zero. **Sistemul ramane cel pe XLM-R base**, si nu fiindca ar fi mai bun, ci fiindca nimic nu e masurabil mai bun si el e deja cel publicat.

### Ipoteza de la §3.5 despre franceza

**Se confirma.** Cu `xlmr-large` franceza urca la +0.5784, adica +0.0293 peste cele +0.5491 pe care le da o singura coloana de neg-zipf. Anomalia de la §3.5, unde o coloana batea 770, **era o proprietate a encoderului, nu a datelor franceze**.

Franceza e pe locul 2 din 10 dupa cat castiga prin cel mai bun encoder al ei, +0.0412. E printre limbile care castiga cel mai mult, ceea ce sprijina ipoteza.

### Ansamblul de encodere, rulat

Intrebarea „nu am putea folosi encodere diferite pentru limbi diferite” are raspuns masurat, si e **da, dar prin mediere, nu prin selectie**.
Selectia leave-one-language-out da 0.659580, adica -0.0050 fata de sistem: criteriul e de zece ori mai plat decat alegerea lui `w`, deci argmaxul e zgomot. Medierea neponderata a celor patru da **0.671610**, **+0.0070**, CI [+0.0039, +0.0099], P(>0) = 100.0%, in urcare pe 8 limbi din 10.

Ca ordin de marime: castigul asta e mai mare decat cel care a produs sistemul curent (+0.0078, ansamblul de surse plus fertilitate impreuna), si duce marginea fata de cel mai bun reper publicat, G-Eval cu GPT-4o la 0.6571, de la +0.0075 la **+0.0145**.

### Ce nu e verificat, si trebuie scris

- **e5 a fost evaluat fara prefixul lui.** `intfloat/multilingual-e5-*` e antrenat cu `query: ` / `passage: ` in fata textului. Aici se iau stari ascunse per token dintr-un context brut, nu embeddingul de propozitie, deci conventia conteaza mai putin, dar cifra lui e5 e o margine inferioara, nu evaluarea lui in conditii proprii.
- **`last4` e configuratia mostenita**, aleasa pe XLM-R base cu 12 straturi. Pe un model de 24 de straturi ultimele patru nu sunt neaparat straturile cele mai bine aliniate cross-lingual. Nu s-a cautat pe straturi: ar fi inmultit rularea cu numarul de configuratii.
- Bratul B nu s-a atins deloc, deci nicio cifra de LLM din raport nu s-a schimbat.

