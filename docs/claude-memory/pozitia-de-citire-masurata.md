---
name: pozitia-de-citire-masurata
description: "21 aug 2026 - prefixul fortat de citire INCHIS pe trial: toate trei prefixele negative; mecanismul e ca lasa capul distributiei intact si strica COADA, de unde scoate temperatura"
metadata: 
  node_type: memory
  type: project
  originSessionId: c41c7657-b13d-4c6e-b16c-1f1864b8ecb1
  modified: 2026-08-21T18:37:27.161Z
---

Rulat **21 august 2026**, ultima parghie chiar netestata din [[prioritizarea-parghiilor-masurata]].
Raport: `output/e_citire.md`. Trei brate pe cele 300 de instante de trial, ~5 minute fiecare.

## Verdict: se inchide, cu semn negativ pe toate trei bratele

| prefix | r la T LOLO | diferenta pereche | CI 95% | P(>0) | limbi stricate |
|---|---|---|---|---|---|
| niciunul | +0.7013 | - | - | - | - |
| `Rating: ` | +0.6836 | **-0.0166** | [-0.0345, +0.0021] | 3.9% | niciuna |
| `Answer: ` | +0.6838 | **-0.0162** | [-0.0312, -0.0008] | 2.0% | fr |
| `Difficulty: ` | +0.6856 | **-0.0147** | [-0.0309, +0.0024] | 4.3% | niciuna |

Aceeasi forma ca la scara 0-9: semn negativ pe toate contrastele, doua din trei intervale includ zero.
Franceza si sinhaleza iau -0.05 pana la -0.08 in toate trei bratele.

## Ipoteza declarata a fost respinsa INAINTE de rulare, pe fisierele de pe disc

Ipoteza era „masa pleaca pe deschideri de propozitie si prefixul o recupereaza". Masa bruta peste cele
cinci cifre la bratul de acum e **1.0000**, si D.4 arata 9.999208e-01. Nu se pierde nimic care sa fie
recuperat. A rams deschisa doar ruta de RECALIBRARE, adica prefixul sa schimbe forma distributiei. Si
ea s-a inchis.

## Mecanismul, si e cel care conteaza pentru altele

Prefixul lasa **capul distributiei neatins** si strica **coada**:

| brat | masa pe argmax | atomi efectivi | r la T=1 | r la T=8 | r al COADEI |
|---|---|---|---|---|---|
| niciunul | 0.752 | 1.75 din 5 | +0.6860 | +0.7067 | **+0.6852** |
| `Rating: ` | 0.752 | 1.78 din 5 | +0.6859 | +0.6719 | **+0.6358** |
| `Answer: ` | 0.754 | 1.76 din 5 | +0.6800 | +0.6795 | **+0.6481** |
| `Difficulty: ` | 0.757 | 1.78 din 5 | +0.6869 | +0.6738 | **+0.6363** |

`r al coadei` e semnalul la T -> infinit in forma inchisa, `analysis_dist.s_limit`, adica
`suma_i (i-3) log p_i`. Capul e identic peste toate patru bratele: masa pe argmax 0.752-0.757, atomi
efectivi 1.75-1.78, r la T=1 in 0.6800-0.6869. Coada scade cu ~0.05. De aceea T* cade de la **8** la
**2-3**: temperatura nu mai are de unde sa scoata.

**Consecinta transversala, de tinut minte, si formularea corecta e a doua.** Prima formulare a fost
„tot castigul temperaturii sta in coada", si e greasita. Capul si coada sunt doua citiri **aproape la
fel de bune si parțial independente** ale aceleiasi distributii: pe trial capul da +0.6860 si coada
+0.6852, iar amestecul lor la T=8 da +0.7067, deci amestecul bate AMBELE capete. Pe test la fel: cap
+0.6420, coada +0.6550, amestec la T adoptat +0.6592. Temperatura nu muta greutatea de la cap la
coada, gaseste proportia.

Ce rams valabil e consecinta practica: o intervenție care strica log-probabilitatile mici poate anula
tot castigul temperaturii **fara sa se vada in niciun diagnostic de forma** - masa pe argmax si
entropia rams identice, cum s-a intamplat aici. Diagnosticul care o vede e `analysis_dist.s_limit`,
si e gratis. Vezi [[distributia-b-temperatura]].

## Capcana de implementare, si D.4 a prins-o

Prima rulare a picat pe toate trei prefixele cu masa 5.5e-08. Motivul: dupa `"Rating:"` Gemma pune
**0.9999 pe un token de spatiu simplu**, iar cifra vine abia dupa. Prefixul trebuie sa se termine cu
SPATIU. Detaliile in [[cod-nou-fewshot-si-prefix]].

Codul rams in arbore, cu implicit prefix gol, deci semnalul publicat nu se schimba:
`solution_bert.LLMRater(read_prefix=...)` si `bakeoff_trial.py --prefix`, care cere `--out`.
