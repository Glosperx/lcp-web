# Dropout pe coloana de frecventa in antrenarea semnalului A

Rulat **23 august 2026**, la finalul sesiunii pe al treilea semnal. Referinta e sistemul adoptat in
aceeasi zi, **M3K, r = 0.690001**. Cod: `finetune_xlmr._freq_drop` plus `--freq-drop`.

**Verdict: parghia e inchisa.** Mecanismul se confirma pe bratul A, dar nu trece in fuziune, strica
doua limbi, iar selectia LOLO alege sistematic invers.

## De ce a fost incercata

Doua masuratori care incadreaza intervalul de ambele capete, deci nu o intuitie:

```
p = 0   sistemul de acum                    referinta
p = 1   ablatia --no-freq, coloana anulata  fuziune -0.0051 pe medie, 4 limbi stricate
        peste tot, si in antrenare si la    DAR filipineza +0.0225, CI [+0.0060, +0.0381]
        predictie                           SI bratul A al sinhalezei +0.0243
```

Mecanismul, masurat in `e_al3lea_semnal.md` §5: modelul invata sa depinda de frecventa de la limbile
care O AU, iar sinhaleza (100% tinte fara zipf) si filipineza (26,7%) platesc. Anularea aleatoare a
coloanei pe o fractiune `p` din randurile de ANTRENARE il impiedica sa se co-adapteze, fara s-o piarda
de tot. Blocurile prezise raman neatinse: dropout-ul e o proprietate a potrivirii, nu a datelor.

Controlul de reproducere: la `p = 0`, `e1_frozen_preds_lemma_fert_inloc.csv` iese **bit cu bit**
identic, `shasum 30272f99eb1a024d5dc424cd4bb748ed6dc881f7`.

## 1. Pe bratul A mecanismul se confirma, si mai precis decat s-a prezis

r pe limba, encoderul `xlmr`, trei valori de `p`:

```
lang       p=0   p=0.15   p=0.30   p=0.50    delta la p=0.15
ja      0.6011   0.6369   0.6273   0.6059            +0.0357
si      0.2586   0.2815   0.2825   0.2736            +0.0229
fil     0.4083   0.4270   0.4237   0.4114            +0.0187
en      0.8173   0.8128   0.8041   0.8020            -0.0045
ca      0.4426   0.4326   0.4180   0.4072            -0.0100
fr      0.5372   0.5221   0.5164   0.5052            -0.0151
es      0.6665   0.6458   0.6432   0.6301            -0.0207
pt      0.7621   0.7381   0.7321   0.7195            -0.0240
de      0.6540   0.6283   0.6189   0.6041            -0.0257
it      0.6301   0.5988   0.5886   0.5763            -0.0314
medie   0.5778   0.5724   0.5655   0.5535            -0.0054
```

**Exact trei limbi castiga, si sunt exact cele trei unde coloana de frecventa e stricata:**

- `si`, unde `wordfreq` nu serveste limba deloc, 600 din 600 de tinte cu zipf 0;
- `fil`, unde 152 din 570 de tinte au zipf 0, de sapte ori mai mult decat urmatoarea limba;
- `ja`, unde `wordfreq` **are nevoie de MeCab** si fara el segmentarea japoneza nu e cea presupusa,
  deci valorile exista dar nu sunt de incredere.

A treia n-a fost prezisa si se explica singura. Predictia scrisa inainte era `si` si `fil`; a iesit
`si`, `fil` si a treia limba cu coloana stricata, din al treilea motiv posibil.

## 2. Pe fuziune nu trece, si strica doua limbi

Cu `p` FIXAT, fata de M3K:

```
p      diferenta pe fuziune
0.15   -0.0002
0.30   -0.0015
0.50   -0.0033
```

La `p = 0.15`, unde media e practic zero, per limba:

```
limba   r M3K    r p=0.15   diferenta   CI 95% pereche          P(>0)
fil     0.5074   0.5259     +0.0185     [-0.0006, +0.0366]      97.1%
ca      0.5639   0.5728     +0.0089     [-0.0078, +0.0249]      86.2%
ja      0.7942   0.7967     +0.0025     [-0.0074, +0.0116]      68.7%
en      0.8723   0.8734     +0.0011     [-0.0021, +0.0047]      74.2%
es      0.7672   0.7680     +0.0008     [-0.0051, +0.0065]      59.2%
fr      0.6679   0.6658     -0.0021     [-0.0087, +0.0041]      25.8%
pt      0.8413   0.8385     -0.0028     [-0.0061, +0.0006]       6.2%
it      0.6795   0.6721     -0.0074     [-0.0153, -0.0002]       2.1%
de      0.7712   0.7557     -0.0156     [-0.0241, -0.0080]       0.0%
```

**Doua limbi stricate cu interval care exclude zero, `de` si `it`.** Conditia se citeste inaintea
mediei, deci configuratia pica indiferent ce face media.

## 3. Rezultatul metodologic, si e mai tare decat cel de mai sus

`p` nu are voie sa fie ales uitandu-ne la test. Varianta onesta il trece prin `fuse_ab --a-set`, adica
prin exact acelasi criteriu leave-one-language-out prin care trec `w`, `w_src` si modelul lui B.

**Rezultat: -0.0034 pe medie.** Mai rau decat orice `p` fixat.

Si motivul se vede rand cu rand:

```
lang   ce a ales LOLO   ce ar fi trebuit   corect?
ca     p0               p015 (+0.0089)     NU
de     p015             p0   (-0.0156)     NU
en     p0               p015 (+0.0011)     NU
es     p0               p015 (+0.0008)     NU
fil    p0               p015 (+0.0185)     NU
fr     p015             p0   (-0.0021)     NU
it     p015             p0   (-0.0074)     NU
ja     p0               p015 (+0.0025)     NU
pt     p015             p0   (-0.0028)     NU
```

**Selectia LOLO a nimerit alegerea buna pe 0 limbi din 9.** Nu aproape de zero: exact zero, si
sistematic pe dos. A ales dropout tocmai pentru limbile care pierd din el, si l-a evitat tocmai pentru
filipineza, care castiga cel mai mult.

Nu e zgomot, e anticorelatie, si are un motiv: **ce face dropout-ul potrivit pentru limba L e o
proprietate A LUI L**, anume ca propria ei coloana de frecventa e stricata. Celelalte noua limbi n-au
cum s-o stie, fiindca la majoritatea dintre ele coloana e in regula. Criteriul nu e doar plat, e
orientat gresit.

E cea mai curata instanta din tot proiectul a regulii deja formulate: pana acum recordul era selectia
de encoder, care nimerea 0 din 10 dar cu un criteriu plat. Aici criteriul separa, si separa invers.

## 4. Regula tintita, rulata: +0.000456, si strica doua limbi care n-au fost atinse

Concluzia naturala a mecanismului: dropout **numai** pe limbile unde coloana e nesigura, prin trei
criterii **fara eticheta**, declarate inainte:

    si   `wordfreq` nu serveste limba deloc
    fil  26,7% din tinte au zipf 0, de sapte ori mai mult decat urmatoarea limba
    ja   `wordfreq` cere MeCab, care lipseste, deci segmentarea nu e cea presupusa

Nu e selectie pe scor: toate trei se pot citi fara sa vezi o eticheta. Setul de predictii s-a construit
prin imbinare, 1830 de randuri de la `p = 0.15` si 4087 de la `p = 0`, cu control ca randurile din
afara setului sunt identice bit cu bit.

**Rezultat: +0.000456 pe medie. Si strica `en` si `fr`, amandoua cu interval care exclude zero.**

```
limba   r M3K    r tinta   diferenta   CI 95% pereche         w_src M3K -> tinta
fil     0.5074   0.5251    +0.0177     [-0.0009, +0.0353]     1.000 -> 0.750
it      0.6795   0.6800    +0.0005     [-0.0011, +0.0021]     0.625 -> 0.875
de      0.7712   0.7712    +0.0000     [-0.0000, +0.0000]     0.625 -> 0.625
es      0.7672   0.7671    -0.0001     [-0.0008, +0.0006]     0.875 -> 0.750
pt      0.8413   0.8410    -0.0002     [-0.0007, +0.0002]     0.875 -> 0.750
en      0.8723   0.8717    -0.0006     [-0.0011, -0.0002]     0.750 -> 0.875
ja      0.7942   0.7932    -0.0010     [-0.0121, +0.0094]     1.000 -> 0.875
ca      0.5639   0.5624    -0.0015     [-0.0040, +0.0007]     0.625 -> 0.875
fr      0.6679   0.6633    -0.0046     [-0.0072, -0.0022]     0.875 -> 0.875, w 0.35 -> 0.40
si      0.4350   0.4295    -0.0055     [-       ,        ]    0.750 -> 0.750
```

**Cum pot pierde `en` si `fr` cand datele lor n-au fost atinse deloc?** Prin criteriul imbricat.
`w_src` si `w` pentru limba L se aleg pe celelalte noua limbi, iar acele noua includ acum `si`, `fil`
si `ja` modificate. **La 8 limbi din 10 s-a mutat `w_src` sau `w`**, desi la sapte dintre ele
predictiile proprii sunt identice bit cu bit. Franceza trece de la `w = 0.35` la `w = 0.40` si pierde
-0.0046.

E a treia instanta a aceleiasi patologii, si cea mai curata: pe 22 august, `dezacord` a pierdut
-0.000331 desi `a = 0` peste tot; aici sapte limbi neatinse isi schimba ponderea fiindca s-au schimbat
datele altor trei.

**Si sinhaleza e ilustrarea decuplarii A-fuziune inca o data:** urca +0.0229 pe bratul A si coboara
-0.0055 pe fuziune.

## Ce ramane de spus

Parghia se inchide, in toate cele trei variante: `p` global fixat (-0.0002 la cel mai bun, doua limbi
stricate), `p` ales LOLO (-0.0034, si 0 alegeri corecte din 9), si regula tintita pe limbi
(+0.000456, doua limbi stricate). **Nimic nu trece bara de +0.0045 si nimic nu trece nici conditia de
limba.**

Dar observatia despre coada se intareste a treia oara, si acum are trei limbi si trei mecanisme
diferite prin care aceeasi coloana e stricata: **absenta** (si), **gauri** (fil) si **nesiguranta de
segmentare** (ja). Cifra care le leaga: scapand partial de frecventa, **exact acele trei limbi urca pe
bratul A, si numai ele**, cu +0.0229, +0.0187 si +0.0357.

Asta e o propozitie pentru paper, nu o parghie pentru cifra.
