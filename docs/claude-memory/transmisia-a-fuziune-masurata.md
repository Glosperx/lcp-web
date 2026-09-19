---
name: transmisia-a-fuziune-masurata
description: "A transmite cu 0.09-0.28, B cu 0.6865, deci B e de 1.74 ori mai eficient; A trebuie sa urce cu +0.017..+0.049 ca fuziunea sa treaca bara, B doar cu +0.007..+0.028"
metadata:
  type: project
---

Masurat **23 august 2026** de `analysis_frontiera_enc.py` -> `output/e_frontiera_enc.md`, citind
cifrele din rapoartele de pe disc, nu dintr-o constanta. Trei rulari cu ACELASI brat B (0.6424) si
acelasi protocol `--pick-split test`, deci singura diferenta e sursa lui A:

    sursa lui A            r_A        r_fuziune   factor
    un singur xlmr         0.580723   0.669591    referinta
    media a 3 (fara large) 0.601244   0.675391    0.283
    media a 4              0.607890   0.675996    0.236
    marginal, de la 3 la 4                        0.091

**Factorul SCADE pe masura ce A se imbunatateste.** La punctul de operare de acum, media a trei,
factorul marginal e **0.091**.

Consecinta, si guverneaza tot ce se planifica pe partea A: ca fuziunea sa urce cu bara de +0.0045,
bratul A trebuie sa urce cu **+0.017 (optimist, factorul mediu 0.259) pana la +0.049 (pesimist,
factorul marginal)**. Pentru scara: trecerea de la un encoder la patru a adus +0.027 pe A.
**Deci nicio parghie singura de encoder nu ajunge, prin aritmetica.**

Pe sistemul CURENT (cu temperatura pe B, `bakeoff_test_Text`), reperele de fuziune cu A dintr-un
singur encoder: xlmr 0.6799, e5 0.6802, labse 0.6807, xlmr-large 0.6792, iar media celor trei
**0.6838**. Deci ansamblul de encodere valoreaza **+0.0040** pe sistemul de acum, nu +0.0058 ca pe
cel vechi. `xlmr-large` are cel mai bun brat A (0.5915) si cea mai proasta fuziune (0.6792), ceea ce
e ilustrarea directa a decuplarii.

**How to apply:** orice cifra noua pe A se inmulteste cu 0.09..0.28 inainte de a fi numita castig.
`fuse_ab.py` costa 11 secunde, deci nu exista motiv sa se raporteze vreodata numai cifra pe A.
Vezi [[frontiera-e-identitate-nu-aproximare]] si [[cifra-de-raportat-in-paper]].

---

## Transmisia lui B, masurata 23 aug seara. Reordoneaza tot ce se planifica

Pana acum se masurase numai A. Derivata lui `r_fuz` fata de fiecare brat, la `w` si `rho` fixate, pe
cele zece limbi ale sistemului M3K:

    brat   factor analitic   cat trebuie sa urce ca fuziunea sa treaca bara de +0.0045
    A      0.3946            +0.017 .. +0.049
    B      0.6865            +0.007 .. +0.028

**B e de 1.74 ori mai eficient.** Intervalele de mai sus aplica lui B aceeasi corectie empirica pe care
a suferit-o A: analiticul supraestimeaza cu un factor intre 1.5 si 4.3, masurat pe rularile reale.

Si diferentele care apar EFECTIV pe axa B sunt de alt ordin: intre modele, B merge de la 0.374
(qwen3-8b) la 0.642 (gemma-12b), adica **+0.268**. Cea mai mare parghie masurata vreodata pe A e +0.027.

**How to apply:** orice sesiune de cautare de cifra se planifica pe B, nu pe A. O confirmare
independenta, masurata pe 23 aug noaptea: `first` pe A a urcat A cu +0.0073 si fuziunea cu +0.0010,
adica factor **0.137**, in banda cunoscuta.

Alexandru a respins explicit directia "un model de evaluare mai mare" ca nefiind solutie inginereasca.
Nu se repropune. Vezi [[sistemul-e-0690001-m3k]].
