---
name: al3lea-semnal-ce-ramane-deschis
description: "Punct de reluare, actualizat 24 aug 2026: sistemul e 0.690001, si TOATE pistele inginerest identificate sunt inchise cu cifre; ce ramane e scrisul"
metadata: 
  node_type: memory
  type: project
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T17:17:26.129Z
---

Starea la finalul zilei de **23 august 2026**. Sistemul ramane **0.683849**, nimic adoptat.

## Ce s-a inchis

**Intrebarea sesiunii e inchisa cu NU.** Treisprezece candidati prin poarta, sapte dusi cap la capat
prin fuziune, niciunul peste zero. Vezi [[poarta-al-treilea-semnal-0107]] pentru cifra care decide
(0.1077) si [[semnalul-c-surprisal-stare]] pentru surprisal, inchis definitiv.

Rapoartele: `output/e_al3lea_semnal.md` (491 linii, cu tabelul de prioritizare ordonat dupa raport),
`output/e_literatura_al3lea.md`, `output/e_c_sanatate.md`, `output/e_c_frontiera_6modele.md`,
`output/e_shap_multi.md`, `output/e_c3_*.md`.

## Cele trei decizii lasate lui Alexandru, nediscutate inca

1. **Imputarea zerourilor de frecventa pe filipineza** din `data/freq_tail/`, care exista deja pe disc.
   E testul direct al mecanismului din [[filipineza-mecanismul-frecventei]] si costa sub 30 de minute.
   Varianta rulata pe 23 august dimineata **inlocuia coloana peste tot** si a pierdut pe medie
   (-0.0009); asta ar umple **numai cele 152 de zerouri**, ceea ce e alt obiect.
2. **Poarta de sanatate rulata pe `RoLlama3-8b-Instruct`**, calea romaneasca. Paperul romanesc
   foloseste surprisal de la el (`solutie_finala.py`, `W_SURP = 0.08`), riscul e din aceeasi clasa ca
   la Gemma, si `analysis_c_sanatate.py` e deja agnostic de backend. Nerulat ca sa nu concureze cu
   inferenta mlx. Costa ~5 minute.
3. **Ce din sesiune intra in paper.** Defectul Gemma e o propozitie de reproductibilitate; mecanismul
   filipinezei e o contributie; poarta de 0.1077 e o unealta metodologica.

## Piste declarate si NERULATE

- **Diversitatea contextuala** (numarul de contexte distincte in care apare cuvantul). Singurul
  candidat lexical din literatura cu dovada ca **subsumeaza** frecventa: Adelman, Brown si Quesada,
  Psychological Science 2006, 17:814-823, unde efectele de frecventa dispar cand se controleaza
  diversitatea contextuala, dar nu si invers. Cere corpusuri segmentate in documente pentru toate cele
  zece limbi, nu doua. ~3 ore, ~200 de linii. Avertisment din literatura mai noua (Johns si colegii,
  JML 2021): numararea bruta a documentelor nu ajunge, conteaza continutul semantic.
- **Surprisal din capul de MLM al lui XLM-R**, §4.4 din `e_encoder2.md`. Singura cale prin care un
  model monolingv incape in protocolul zero-label. ~15 min, ~60 de linii.
- **C de la un model sub 4B**, care ar testa ipoteza de inverse scaling (Oh si Schuler, TACL 2023).
  **La noi ipoteza ramane netestata**, fiindca marimile distincte din bazin sunt doar 8B, 9B si 12B,
  iar cea de 12B a cazut din alt motiv, incarcarea. ~25 min.
- **Normele psiholingvistice sunt inchise ca pista**, nu doar nerulate: AoA multilingv are 299 de
  cuvinte pe 25 de limbi si **toate judecate ca achizitionate inainte de 6 ani**, iar concretetea lui
  Brysbaert (37.058 de cuvinte) e numai engleza. Nu servesc coada, care e unde ne trebuie.

## Ce trebuie corectat pe disc, si inca nu s-a facut

`output/e_bakeoff_test.md`, verdictul 4: "Semnalul C pe test: r mediu per model intre -0.065 si +0.094".
Capatul de **-0.065 e al unei coloane degenerate**, nu al unui surprisal slab. Vezi
[[gemma-nu-poate-da-surprisal]].

---

## Actualizat 23 aug noaptea

Alexandru a cerut sa continue cautarea de cifra, nu scrisul la paper, si a **respins scalarea
modelului** ca nefiind solutie inginereasca. Ce s-a facut dupa:

- **M3K adoptat**, sistemul e acum 0.690001. Vezi [[sistemul-e-0690001-m3k]].
- **`first` pe A plus M3K pe B**: 0.691001, +0.0010, dar strica filipineza (-0.0068, CI exclude zero).
  Respins. A dat totusi cea mai buna sinhaleza din proiect, **0.4527**.
- **Transmisia lui B masurata pentru prima data: 0.6865, fata de 0.3946 al lui A**, deci B e de 1.74
  ori mai eficient. B trebuie sa urce cu +0.007..+0.028 ca fuziunea sa treaca bara, A cu +0.017..+0.049.
- **Axa prompturilor e saturata**: al 4-lea membru (FM4K) da +0.0003 peste al 3-lea si strica pt.
- **Dropout pe frecventa**: inchis in trei variante. Vezi [[dropout-frecventa-inchis]].

**Nu mai am o parghie inginereasca cu valoare asteptata pozitiva.** Ce ramane, declarat: diversitatea
contextuala (~3h, partea A unde transmisia e 0.14), poolingul cu atentie antrenat LOLO (dismisat prea
strict in `e_encoder2` §"Ce ramane deschis": A e oricum antrenat pe etichetele celorlalte noua limbi,
deci un pooling invatat sub acelasi protocol e la fel de zero-label), si modele pe octeti.

---

## Actualizat 24 august 2026: pistele s-au terminat

Alexandru a cerut sa continue cautarea de cifra si a respins scalarea modelului. S-au rulat, in ordine,
toate pistele care mai aveau un argument:

    incercare                        rezultat pe fuziune   de ce a picat
    M3K (al 3-lea prompt)            +0.006153             ADOPTAT, sistemul e 0.690001
    `first` pe A + M3K pe B          +0.0010               strica fil (CI exclude zero)
    dropout pe frecventa, 3 variante  -0.0002 .. -0.0034   strica limbi; LOLO alege 0 din 9 corect
    diversitate contextuala, 2 var.   -0.0062 si -0.00065  inlocuirea lui zipf pierde pe 9 din 10

**Nu mai am nicio parghie inginereasca cu valoare asteptata pozitiva**, si motivul e aritmetic, nu de
imaginatie: A trebuie sa urce cu **+0.033** ca fuziunea sa treaca bara (transmisie 0.137 masurata), iar
cea mai mare parghie de encoder din tot proiectul e +0.027. Axa prompturilor e saturata (al 4-lea
membru: +0.0003 si strica pt). Al treilea semnal e inchis cu 13 candidati. Vezi
[[transmisia-a-fuziune-masurata]].

Ce ramane declarat si nerulat, cu odds mici si motivul lor:
- **poolingul cu atentie antrenat LOLO** -- dismisat prea strict in `e_encoder2`, fiindca A e oricum
  antrenat pe etichetele celorlalte noua limbi; dar intra prin A, unde transmisia e 0.137;
- **modele pe octeti sau caractere** (CANINE, ByT5, MYTE) -- arhitecturi, nu greutati de pus intr-un
  `AutoModel`;
- **diversitate contextuala pe un corpus comparabil cu al lui `wordfreq`** -- ar fi o comparatie curata
  intre constructe, nu intre corpusuri, dar tot prin A.

Si o directie NOUA, iesita din masuratoarea de azi si singura care nu e o reluare: pe sinhaleza,
**orice trasatura de frecventa strica prin duplicarea lui B**. Ce trebuie cautat acolo e ceva ce un LLM
nu poate citi din propozitie. Vezi [[sinhaleza-decorelarea-e-capitalul]].

## Ce trebuie corectat pe disc, si tot nu s-a facut

`output/e_bakeoff_test.md`, verdictul 4, citeaza inca -0.065 al coloanei C degenerate a lui Gemma.
