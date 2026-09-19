# Diversitatea contextuala, si de ce sinhaleza rezista la tot

Rulat **24 august 2026**. Referinta e sistemul adoptat, **M3K, r = 0.690001**. Cod: `build_ctx_div.py`,
`mlsp_common.load_ctx_div` / `ctx_div_safe`, `solution_bert.lexical(ctxdiv=...)`, `--ctx-div`.

**Verdict: parghia e inchisa.** Dar masuratoarea a scos mecanismul care explica trei esecuri diferite
din ultimele doua sesiuni, si ala e rezultatul.

## 0. Ce s-a construit

Diversitate contextuala: in cate DOCUMENTE distincte apare cuvantul, nu de cate ori. Singurul candidat
lexical din literatura cu dovada ca **subsumeaza** frecventa: Adelman, Brown si Quesada
(Psychological Science 2006, 17:814-823) arata ca efectele de frecventa dispar cand se controleaza
diversitatea contextuala, dar nu si invers.

Sursa: `wikimedia/wikipedia`, dump 20231101, **un shard per limba** pentru cele opt mari si dump-ul
intreg pentru `si` si `tl`. Normalizata ca rata, pe aceeasi scara ca `zipf`. Diferenta de cod fata de
`build_freq_tail.numara` e un `set()`.

```
lang  documente   tipuri  tinte  acoperite  acoperire     acoperire wordfreq
ca       184353   484700    445        404      90.8%
de       142266  1345184    570        536      94.0%
en       156289   438554    570        564      98.9%
es       141628   602555    593        587      99.0%
fr       150862   642330    569        557      97.9%
it       183364   569866    570        542      95.1%
ja        92632  1619738    570        315      55.3%      (cere MeCab, la fel de slaba)
pt       185375   459833    567        550      97.0%
si        23065   179185    600        525      87.5%      0% -- limba nu e servita deloc
fil       45341   148515    570        471      82.6%      73.3%
```

Controlul de reproducere trece: fara `--ctx-div`, `e1_frozen_preds_lemma_fert_inloc.csv` iese bit cu
bit, `shasum 30272f99eb1a024d5dc424cd4bb748ed6dc881f7`.

## 1. Pe bratul A: inlocuirea pierde, adaugarea nu aduce

```
brat A, xlmr, r pe limba
lang      zipf    inloc     plus   d_inloc   d_plus
si      0.2586   0.2865   0.2727   +0.0279  +0.0141
ca      0.4426   0.4210   0.4474   -0.0216  +0.0047
it      0.6301   0.5852   0.6316   -0.0450  +0.0014
ja      0.6011   0.5788   0.6022   -0.0223  +0.0011
pt      0.7621   0.7236   0.7620   -0.0385  -0.0001
de      0.6540   0.6240   0.6536   -0.0300  -0.0004
fil     0.4083   0.3755   0.4079   -0.0328  -0.0004
en      0.8173   0.7986   0.8164   -0.0187  -0.0009
es      0.6665   0.6370   0.6640   -0.0295  -0.0025
fr      0.5372   0.5052   0.5340   -0.0320  -0.0031
medie   0.5778   0.5535   0.5792   -0.0242  +0.0014
```

**`inloc` pierde pe noua limbi din zece si castiga pe una: sinhaleza, +0.0279.** E exact limba unde
`zipf` nu exista deloc, deci acolo inlocuiesti nimic cu ceva; in rest inlocuiesti ceva bun cu ceva mai
slab.

**Rezultatul lui Adelman si colegii nu se transfera.** Dar comparatia e confundata si se declara ca
atare: `wordfreq` agrega subtitrari, web, stiri si Wikipedia peste un corpus mult mai mare, in timp ce
diversitatea noastra vine dintr-un singur shard de Wikipedia. Ce s-a masurat nu e "diversitate fata de
frecventa", e "diversitate dintr-un corpus mic fata de frecventa dintr-unul mare".

## 2. Pe fuziune, amandoua pierd

```
varianta   delta pe fuziune   limbi stricate (CI exclude zero)
inloc      -0.0062            -
plus       -0.00065           niciuna
```

## 3. Rezultatul care conteaza: de ce sinhaleza rezista la tot

Sinhaleza a castigat pe bratul A la **trei interventii independente** din ultimele doua sesiuni, si a
pierdut pe fuziune de fiecare data:

```
interventie   d pe bratul A al lui si   d pe fuziunea lui si
first             +0.0541                    +0.0177
freq-drop         +0.0233                    -0.0062
ctx-div plus      +0.0066                    -0.0023
```

Motivul se citeste direct, si e frontiera aplicata **in interiorul unei limbi**:

```
config     r_A      r_B      rho(A,B)   r_fuz    prezis de frontiera
M3K       0.3166   0.3979    0.3872    0.4350   0.4350
first     0.3707   0.3979    0.4195    0.4527   0.4527
fd015     0.3399   0.3979    0.5056    0.4289   0.4289
cdplus    0.3232   0.3979    0.4243    0.4327   0.4327
fdtinta   0.3388   0.3979    0.4972    0.4295   0.4295
```

Frontiera reproduce fiecare cifra cu eroare sub **5e-5**, deci nu e o explicatie, e o identitate.

**Sinhaleza are `rho(A, B) = 0.3872`, cea mai mica din toate cele zece limbi**, cand media e 0.687.
De asta fuziunea ei castiga +0.1184 peste bratul A, cel mai mult din tabel. Decorelarea aia e capitalul
ei, si e fragila.

Si acum se vede ce face fiecare interventie:

- **`first`** e o schimbare de REPREZENTARE, nu de frecventa. Urca `r_A` cu +0.0541 si `rho` cu doar
  +0.032. Castigul de calitate bate pierderea de decorelare. **E singura care castiga.**
- **`freq-drop`** si **`ctx-div`** sunt interventii pe FRECVENTA. Urca `r_A` cu +0.0233 si +0.0066, dar
  urca `rho` cu **+0.118** si +0.037. Pierderea de decorelare inghite castigul.

**Mecanismul, formulat:** semnalul B, nota unui LLM, codifica deja cunoastere de tip frecventa. Cand ii
dai lui A un semnal de frecventa pe care nu-l avea, A incepe sa **duplice** B in loc sa-l completeze.
Pe sinhaleza, unde tot avantajul fuziunii vine din faptul ca A si B gresesc diferit, duplicarea costa
mai mult decat aduce calitatea.

**Consecinta pentru orice incercare viitoare pe coada:** pe sinhaleza nu se cauta o trasatura de
frecventa mai buna. Frecventa e chiar directia in care A si B se suprapun. Se cauta ceva ce un LLM nu
stie sa citeasca din propozitie.

## 4. Ce ramane

Diversitatea contextuala nu se reia pe sursa asta. Ar merita reluata numai cu un corpus comparabil cu
al lui `wordfreq` ca marime si ca amestec de registre, si atunci ar fi o comparatie curata intre
constructe, nu intre corpusuri. Nu e o parghie pentru cifra: chiar si asa, ar intra prin bratul A,
unde transmisia masurata e 0.137, deci ar trebui sa urce A cu +0.033 ca fuziunea sa treaca bara.
