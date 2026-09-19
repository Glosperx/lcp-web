# TabFM la MAXFEAT=256: latimea urca semnalul A, dar nu si fuziunea

Sinteza rularii de pe Colab din 25-26 august 2026. Intrebarea: la o latime mai mare per membru
(256 de coloane in loc de 160, din 400 disponibile), se decoreleaza TabFM mai bine de ridge si hgb,
si trece atunci fuziunea peste controlul `ridge+hgb`?

Rapoartele din spate: `e_fusion_lolo_rt_mf160.md`, `e_fusion_lolo_rt_mf256.md`,
`e_fusion_lolo_rt_mf256_vsctrl.md`, `e_regresor_a_proj-394_mf160.md`,
`e_regresor_a_proj-394_mf256.md`. Predictiile brute: `data/preds_proj394_maxfeat256/`.

## Rularea

12 cereri x 8 membri pe un T4, in doua sesiuni Colab gratuite, 56 de minute de GPU in a doua.
`setari.json` confirma ca **`max_num_features` e singura diferenta** fata de rularea de la 160:
acelasi `n_estimators=8`, aceleasi patru familii de normalizare, acelasi `crosses=sqrt`, acelasi
dtype. Toate cele 12 chei de cerere se potrivesc cu blocurile locale, deci blocul de intrare e
identic bit cu bit.

## Cifrele

Semnalul A singur, `--frozentrial`, r mediu pe test peste 10 limbi:

    tabfm @160    0.5541
    tabfm @256    0.5673      +0.0132

Fuziunea, `--arm lolo --fit test --pick-split test`, acelasi B (M3K), doar A variaza:

    ctrl     A = ridge+hgb      0.6803
    rt@160   A = ridge+tabfm    0.6798     -0.0005 fata de control
    rt@256   A = ridge+tabfm    0.6806     +0.0003 fata de control

Comparatia PERECHE fata de control, pe reesantionari de contexte:

    rt@256 vs ctrl   diferenta +0.0003   P(>0) = 51.8%
    pe limbi         5 in sus / 5 in jos; `ja` +0.0050 (P 96.0%), dar `fil` -0.0059 (P 0.0%)
                     si `en` -0.0023 (P 3.2%), amandoua semnificativ MAI RELE

51.8% e o moneda. Nu exista dovada ca rt@256 difera de control.

## De ce nu s-a miscat: cele doua efecte se anuleaza

    A a urcat        +0.0132 pe tabfm singur, +0.0037 pe bratul compus ridge+tabfm
    rho a urcat si el

               rho(tabfm, ridge)   rho(tabfm, hgb)   mediu
    proj-200                                         0.829
    proj-394 @160        0.877             0.851     0.864
    proj-394 @256        0.900             0.873     0.887

Pragul cerut de frontiera, calculat de `analysis_regresor.py` pe r-ul masurat al lui tabfm, e
**0.813** la 256. Masurat: **0.887**. Verdictul scriptului: `CADE`.

Transmisia se verifica singura: A a urcat cu +0.0037 pe bratul compus si fuziunea cu +0.0008,
adica un factor de 0.22, in intervalul 0.09-0.26 stabilit anterior pentru transmisia A -> fuziune.
Nimic nu se comporta neasteptat; pur si simplu castigul pe A e mancat de corelatia mai mare.

## Ce inchide asta

Ipoteza care a motivat rularea era ca latimea mai mare ar putea decorela membrii fata de ridge si
hgb. **E acum al treilea punct pe aceeasi tendinta, si toate trei merg in directia gresita:**
200 -> 394 de coloane a urcat rho de la 0.829 la 0.864, iar 160 -> 256 per membru l-a urcat mai
departe la 0.887. Mai multa capacitate face TabFM mai bun **si mai asemanator** cu ce avem deja.

Nu e o surpriza in raport cu ce se stia: capacitatea mai mare stricase deja blend-ul o data
(`hgb-adanc` pierde 0.046), iar podeaua de rho la 0.80 tinuse peste cinci algoritmi cu biasuri
inductive complet diferite. Rularea asta adauga singurul lucru care lipsea: masuratoarea directa
pe axa pe care ipoteza era inca deschisa.

## Ce ramane pe disc si se poate refolosi

`data/preds_proj394_maxfeat256/_ckpt/` tine cei 96 de membri separat, deci ablatia pe
`n_estimators` (media primilor k) se poate calcula fara nicio rulare noua, daca vreodata conteaza
cat aduce membrul 8 peste membrul 4.

---

# Adaos: ar ajuta hiperparametri mai mari? Masurat, nu argumentat.

Doua intrebari puse dupa rulare: (a) ar da `n_estimators` sau `MAXFEAT` mai mari o fuziune mai
buna; (b) se poate face media pe encodere cu `ridge+tabfm` in loc de `ridge+hgb`. Amandoua au
raspuns din date deja pe disc.

## Corectie factuala: TabFM nu e boosting

Se repeta destul de des ca sa merite scris langa cifre. Boosting inseamna membri secventiali,
fiecare potrivit pe reziduul celor dinainte. TabFM nu face asta: `_batch_forward` trece membrii
INDEPENDENT (`batch_size=1`) si `_combine_predictions` face `np.mean(...)`. E bagging peste invatare
in context, nu boosting. Dovada operationala: checkpointul pe membru functioneaza: daca membrii ar
fi secventiali, membrul 5 n-ar putea fi calculat fara 1-4 in memorie. Si `fit()` nu antreneaza —
cele 1.65 miliarde de greutati vin inghetate din checkpoint.

## Rolul: inlocuitor pentru hgb, sau al treilea membru?

    rho mediat pe limbi, proj-394 @256
           ridge    hgb  tabfm
    ridge  1.000  0.815  0.900
    hgb    0.815  1.000  0.873
    tabfm  0.900  0.873  1.000

`ridge` si `hgb` sunt perechea cea mai decorelata din tabel. Valoarea lui hgb in blend nu e familia
de algoritm, e distanta fata de ridge, si tabfm nu o atinge. De aceea:

    ctrl                 ridge+hgb           0.6803
    inlocuire            ridge+tabfm         0.6806   +0.0003   P(>0) 51.8%
    adaugare             ridge+hgb+tabfm     0.6810   +0.0007   P(>0) 68.3%

Ca inlocuitor pierde, ca al treilea membru castiga marginal si nesemnificativ.

## `n_estimators`: curba, din cei 96 de membri salvati separat

Subseturi ECHILIBRATE (cate unul din fiecare familie de normalizare; m0,m1=none, m2,m3=power,
m4,m5=quantile_rtdl, m6,m7=robust, fiindca `prepare_ensemble_tensors` grupeaza pe norma). `4b` e
complementul lui `4`, ca margine pe zgomotul de selectie a subsetului.

       k     r_A   rho(t,ridge)  rho(t,hgb)  rho mediu   prag   distanta
       1  0.4755      0.788        0.740       0.764    0.601    0.163
       2  0.5479      0.885        0.850       0.868    0.767    0.101
       4  0.5586      0.895        0.857       0.876    0.792    0.084
      4b  0.5603      0.878        0.864       0.871    0.796    0.075
       8  0.5673      0.900        0.873       0.887    0.813    0.074

**Mecanismul, masurat.** Un SINGUR membru are rho 0.764, adica sub pragul de watch de 0.78-0.80 —
cel mai decorelat lucru de pe axa asta. Dar are r 0.4755. De la 1 la 2 membri rho sare la 0.868.
Partea din TabFM care e decorelata de ridge e ZGOMOTUL lui, nu semnalul; medierea sterge exact acel
zgomot, deci r urca si rho urca odata cu el. Nu e un efect secundar al lui `n_estimators`, e ce
face `n_estimators`.

**Extrapolarea, pe metrica directa.** Distanta in rho e greu de citit; deficitul de CALITATE e
direct interpretabil: la rho-ul pe care il are, ce `r3` i-ar fi trebuit ca sa atinga tinta?

       k   r3 are     rho   r3 CERUT   deficit   r_A(3 membri)   vs blend
       1   0.4755   0.764    0.5467    0.0712      0.566592      -0.008291
       2   0.5479   0.868    0.5905    0.0426      0.577290      +0.002407
       4   0.5592   0.874    0.5928    0.0336      0.580473      +0.005589
       8   0.5673   0.887    0.5984    0.0311      0.581386      +0.006502

Si r3 si rho converg ca 1/k la mediere, deci deficitul se potriveste contra 1/k:
`deficit(k) = 0.04696/k + 0.02260`, reziduu maxim 0.0035 pe patru puncte. Extrapolat:

       k=16  +0.0255    k=32  +0.0241    k=64  +0.0233    k=inf  **+0.0226**

**Deficitul ramane POZITIV la orice `n_estimators`.** 8 -> infinit cumpara 0.008 dintr-un deficit de
0.031. Nu e o limita de tuning, e limita a ce poate medierea.

Randul cu k=1 e cel mai instructiv: e cel mai decorelat lucru masurat vreodata pe axa asta (0.764,
sub pragul de watch de 0.78-0.80), si totusi adaugarea lui in blend face A **mai prost** cu 0.0083.
Decorelarea nu valoreaza nimic daca vine din zgomot.

La k=8, ca sa treaca bara, TabFM ar trebui sa aiba r=0.5984: mai bun decat ridge (0.5627), decat hgb
(0.5326), si decat blend-ul intreg (0.5749). Un al treilea membru ar trebui sa bata ansamblul de doi
in care intra. 16 si 32 de membri costa 7 si 14 ore
de GPU pentru ~0.003 dintr-o distanta de 0.074.

Pe `MAXFEAT` acelasi calcul: distanta a scazut cu 0.009 la +96 de coloane (0.083 la 160, 0.074 la
256), mai sunt maximum 144 disponibile, deci latimea plina ar da ~0.060.

## Media pe encodere cu ridge+tabfm: aritmetica

TabFM nu incape pe cele 774 de coloane ale lui A pe un T4 (ar cere ~18-23 GiB fata de 14.6), deci
fiecare brat trebuie mutat pe `proj-394`. Cat costa mutarea, masurat pe acelasi B si acelasi
protocol, doar A variind:

    A = blend pe xlmr PLIN (774)     fuziune  0.6828
    A = blend pe xlmr proj-394       fuziune  0.6803
    proiectia costa                          -0.0025

Deci: **-0.0025 platit sigur pe fiecare encoder, ca sa vanezi +0.0007 nedovedit.** Raport de 3.5 la
1 impotriva, inainte de cele ~14 ore de GPU pentru patru encodere. (Cifra de -0.0025 e masurata pe
xlmr; pe alte encodere poate diferi.)

Singura ruta care ar evita handicapul e TabFM pe embeddingul plin, adica o placa de 40 GB. Si tot
ar ramane un +0.0007 la P=68%.

## Plafonul intregii axe, calculat din cele sase configuratii masurate

Ultima intrebare: daca s-ar putea rula orice pe Colab, cat s-ar scoate maxim? Intai o precizare —
TabFM nu se poate **antrena**: greutatile vin inghetate, iar potrivirea lor ar cere in fp32 6.1 GiB
greutati + 6.1 gradienti + 12.3 stari Adam, adica 24.6 GiB inainte de orice activare, pe o placa de
14.6. Nici cu LoRA, fiindca backprop-ul prin cele 24 de blocuri ICL la T=14107 ar cere pastrate
activarile care acum consuma 7.9 GiB si se arunca. Deci doar configuratia la inferenta.

    scenariu                             r_A tabfm     rho   r_A(3)  vs blend   fuziune
    masurat azi    MAXFEAT 256, k=8         0.5673   0.887   0.5814   +0.0065   +0.0017
    k -> infinit   MAXFEAT 256              0.5729   0.890   0.5829   +0.0081   +0.0021
    MAXFEAT 400, k=8                        0.5871   0.921   0.5834   +0.0085   +0.0022
    PLAFON: 400 si k -> infinit             0.5927   0.925   0.5849   +0.0101   +0.0026

Bara pe fuziune e +0.0045: **plafonul nu o trece nici optimist.** Si mai exista o calibrare: la
configuratia de azi identitatea prezicea +0.0017 iar `fuse_ab` a masurat +0.0007, factor 0.41.
Aplicat pe plafon, castigul realist e **+0.0011**.

Extrapolarea pe `n_estimators` e potrivita pe trei puncte contra 1/k (reziduu 0.0043); cea pe
`MAXFEAT` e liniara pe doua puncte si e probabil OPTIMISTA, fiindca la 400 din 400 nu mai exista
subesantionare de coloane si membrii difera doar prin permutare si normalizare.

Ce inseamna in fuziune, pe `proj-394`:

    control ridge+hgb                                        0.6803
    plafon TabFM, realist                                    0.6814
    plafon TabFM, optimist                                   0.6829
    blend pe xlmr PLIN, fara TabFM, zero ore de GPU          0.6828

**Plafonul optimist al intregii axe e exact unde esti deja gratis daca nu proiectezi embeddingul.**
Tot calculul ar cumpara inapoi ce s-a pierdut ca sa poata rula TabFM.

Costul plafonului: `MAXFEAT` 256->400 e x1.41 (exponentul 0.79 masurat pe T4), `n_estimators` 8->32
e x4, patru encodere e x4, deci 3.5 x 22.6 = **~79 ore de GPU**. Si nu pe T4: la 420 de coloane
reale varful ar fi ~15.3 GiB din 14.6, deci cere A100 40 GB. Pe ruta completa cu embedding plin,
sistemul ar merge de la 0.690001 la ~0.6911 realist, ~0.6926 optimist.
