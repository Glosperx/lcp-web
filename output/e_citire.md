# E.11. Pozitia de citire, cernere pe trial

Generat 2026-08-21 21:36:50 de `analysis_citire.py`. 300 instante de trial per brat, 10 limbi, ambele prompturi. Datele brute: `output/dist/pref_*_trial.csv`.

Ultima parghie chiar netestata din `output/e_prioritate.md`. Pana acum `digit_mass` citeste logits-urile
la ultima poziție a sablonului de chat, adica exact acolo unde modelul mai are de ales si FORMA
raspunsului, nu doar nota: poate deschide o propozitie, poate pune un semn, poate pune cifra. Masa
care pleaca pe deschideri de propozitie nu e masa peste note, si totusi ea intra in numitorul
normalizarii. Ipoteza e ca dupa un inceput de raspuns fortat, „Rating:", alegerea de format e deja
facuta si ce rams e chiar nota.

Ipoteza asta are o marime observabila care o testeaza direct, si nu e `r`: **masa bruta** peste cele
cinci cifre, adica `raw1` si `raw2`. Daca prefixul curata citirea, masa bruta trebuie sa urce. Daca
urca masa dar `r` nu se mișcă, atunci masa care se pierdea era pierduta uniform si normalizarea o
scotea oricum, iar parghia e nula prin construcție, nu prin ghinion. Se raporteaza amandoua.

Cernere pe cele 300 de instante de trial, ~6 minute per brat. Bratul de referinta e fisierul CANONIC
de trial, nu o rulare noua: prefixul gol trece prin `_read_ids` fara sa adune nimic, si controlul de
30 de randuri o verifica la octet.

Temperatura se realege pentru FIECARE brat, pe grila extinsa, in doua forme raportate amandoua:
argmaxul pe MEDIA celor zece limbi, care e un oracol dar acelasi oracol pentru toate bratele, deci nu
favorizeaza niciunul; si alegerea LOLO, care e protocolul lucrarii. Un prefix schimba ascutimea
distributiei, deci o comparatie la T = 1 ar masura ascutimea, nu pozitia de citire.

Cifra de trial nu e o predictie a cifrei de test. Numai ordinea supravietuieste, si numai castigatorul
urca pe test.

## 1. Bratele, fiecare la temperatura lui

`T* pe medie` e argmaxul mediei pe cele zece limbi, deci un ORACOL: e in tabel fiindca e acelasi oracol pentru toate bratele si nu favorizeaza niciunul. `T LOLO` e protocolul lucrarii, temperatura limbii L aleasa pe celelalte noua. `masa bruta` e marimea care testeaza direct ipoteza prefixului, si e mediata peste ambele prompturi si toate instantele.

| prefix | ce schimba | masa bruta | r la T=1 | T* pe medie | r la T* | T LOLO, r | atomi efectivi la T=1 |
|---|---|---|---|---|---|---|---|
| `niciunul` | ultima poziție a sablonului de chat, adica semnalul B publicat | 1.0000 | +0.6860 | 8 | **+0.7067** | +0.7013 | 1.75 din 5 |
| `Rating: ` | numeste chiar marimea cerută, si e cuvantul din instructiune | 1.0000 | +0.6859 | 2 | **+0.6879** | +0.6836 | 1.78 din 5 |
| `Answer: ` | neutru fata de marime: forteaza formatul, nu sensul | 1.0000 | +0.6800 | 3 | **+0.6869** | +0.6838 | 1.76 din 5 |
| `Difficulty: ` | numeste constructul, nu nota; mai lung, deci si un control de lungime | 0.9999 | +0.6869 | 2.5 | **+0.6896** | +0.6856 | 1.78 din 5 |

## 2. Comparatia pereche fata de citirea de acum

Fiecare brat la temperatura lui, aleasa LOLO, adica protocolul lucrarii. Reesantionarea e pe CONTEXTE si are seed fix, deci perechea vede aceeasi reesantionare in ambele brate si zgomotul comun se anuleaza. Intervalele sunt late si trebuie sa fie: 30 de instante per limba, nu 560.

**Coloana `limbi stricate` se citeste INAINTEA mediei.** Asa a fost respins `distTpp` la 0.685763 si asa a fost respins `prio_KW` la 0.685727, desi amandoua aveau media mai mare.

| prefix | diferenta pe medie | CI 95% pereche | P(>0) | limbi stricate cu CI care exclude zero | limbi urcate cu CI care exclude zero |
|---|---|---|---|---|---|
| `Rating: ` | **-0.0166** | [-0.0345, +0.0021] | 3.9% | niciuna | niciuna |
| `Answer: ` | **-0.0162** | [-0.0312, -0.0008] | 2.0% | fr | niciuna |
| `Difficulty: ` | **-0.0147** | [-0.0309, +0.0024] | 4.3% | niciuna | niciuna |

### Per limba, fiecare brat fata de citirea de acum

| prefix | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| `Rating: ` | -0.009 | -0.019 | -0.031 | +0.022 | -0.008 | -0.057 | +0.005 | +0.012 | +0.001 | -0.081 |
| `Answer: ` | +0.004 | -0.008 | -0.016 | +0.014 | -0.005 | -0.069 | -0.008 | +0.008 | +0.002 | -0.082 |
| `Difficulty: ` | -0.008 | -0.015 | -0.033 | +0.023 | -0.008 | -0.052 | +0.003 | +0.011 | +0.001 | -0.068 |

## 3. Capul distributiei fata de coada

Bloc adaugat dupa ce cifrele de sus au ieșit toate negative, ca sa se vada UNDE. `masa pe argmax`, `atomi efectivi` si `r la T=1` descriu capul distributiei, adica partea vizibila. `r al coadei` e semnalul la T -> infinit in forma inchisa, `analysis_dist.s_limit`, adica `suma_i (i-3) log p_i`: exact marimea din care temperatura scoate cand urca de la T=1 la T=8. Daca in coada nu e semnal, un T mare nu are ce sa extraga, oricat de curat ar fi capul.

| prefix | masa pe argmax | atomi efectivi | r la T=1 | r la T=8 | r al COADEI | r al cifrei generate |
|---|---|---|---|---|---|---|
| `niciunul` | 0.752 | 1.75 din 5 | +0.6860 | +0.7067 | **+0.6852** | +0.6777 |
| `Rating: ` | 0.752 | 1.78 din 5 | +0.6859 | +0.6719 | **+0.6358** | +0.6730 |
| `Answer: ` | 0.754 | 1.76 din 5 | +0.6800 | +0.6795 | **+0.6481** | +0.6723 |
| `Difficulty: ` | 0.757 | 1.78 din 5 | +0.6869 | +0.6738 | **+0.6363** | +0.6744 |

## Verdict

Cel mai bun brat e `Difficulty: `: -0.0147 fata de citirea de acum, interval pereche [-0.0309, +0.0024], deci include zero, P(>0) = 4.3%. Limbi stricate cu interval care exclude zero: niciuna.

Masa bruta trece de la 1.0000 la 0.9999, adica -0.0000. Prefixul deci NU curata citirea in sensul ipotezei: masa care pleca pe format nu se recupereaza, si atunci nici nu era de recuperat.

**Nu se propune confirmarea pe test**: pe trial nu se vede nimic care sa merite cele ~102 minute, si cifra de trial nu e oricum o predictie a celei de test, doar ordinea supravietuieste.

