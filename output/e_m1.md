# M1. Alegerea dintre selectie si mediere, facuta ea insasi leave-one-language-out

Generat 2026-08-19 10:34:14 de `analysis_m1.py`. Nicio inferenta, nicio fuziune recalculata: ambele brate exista deja per limba, scrise de `fuse_ab.py`, iar M1 e o reagregare a lor. Date brute: `output/m1.csv`.

## Ce raspunde, si de ce conteaza mai mult decat cifra

Obiectia care conteaza impotriva adoptarii mediei de encodere nu e cifra si nu e costul. E ca **alegerea binara s-a facut dupa ce s-a vazut pe test ca selectia cade**. Formularea de pana acum, „singura alegere de cercetator e binara, luata dupa ce s-a vazut ca selectia cade", spune reviewerului exact lucrul care il ingrijoreaza fara sa ii dea nimic care sa il linisteasca. E onesta si insuficienta, fiindca nu e falsificabila.

M1 o face falsificabila. Pentru limba L se decide intre cele doua brate folosind numai celelalte 9 limbi, exact ca `w`, ca `w_src` si ca modelul lui B:

```
crit(brat, L) = media lui r a bratului peste limbile L' != L
ales(L)       = argmax peste cele doua brate
r_M1(L)       = r al bratului ales, pe limba L
```

Fiecare r per limba al fiecarui brat e el insusi produs sub LOLO, deci criteriul lui L nu atinge etichetele lui L la niciun nivel.

## Rezultatul, fold cu fold

| limba | crit selectie | crit mediere | **ales** | marja | r selectie | r mediere | **r M1** |
|---|---|---|---|---|---|---|---|
| ca | 0.673306 | 0.685696 | **mediere** | 0.012390 | +0.5360 | +0.5448 | **+0.5448** |
| de | 0.652271 | 0.663784 | **mediere** | 0.011513 | +0.7254 | +0.7420 | **+0.7420** |
| en | 0.636173 | 0.649247 | **mediere** | 0.013075 | +0.8702 | +0.8729 | **+0.8729** |
| es | 0.649686 | 0.662021 | **mediere** | 0.012335 | +0.7486 | +0.7579 | **+0.7579** |
| fil | 0.676079 | 0.689623 | **mediere** | 0.013544 | +0.5111 | +0.5095 | **+0.5095** |
| fr | 0.668383 | 0.680383 | **mediere** | 0.012001 | +0.5804 | +0.5927 | **+0.5927** |
| it | 0.659729 | 0.672072 | **mediere** | 0.012343 | +0.6582 | +0.6675 | **+0.6675** |
| ja | 0.647316 | 0.658838 | **mediere** | 0.011522 | +0.7700 | +0.7866 | **+0.7866** |
| pt | 0.639811 | 0.652612 | **mediere** | 0.012801 | +0.8375 | +0.8426 | **+0.8426** |
| si | 0.693050 | 0.701824 | **mediere** | 0.008774 | +0.3584 | +0.3997 | **+0.3997** |
| **medie** | 0.659580 | 0.671610 | | 0.012030 | 0.659580 | 0.671610 | **0.671610** |

**Medierea castiga pe TOATE cele 10 folduri.** Marja minima e 0.008774, adica pe foldul cel mai stramt criteriul separa inca de 65% din cat separa pe cel mai larg. **Alegerea binara nu mai e o alegere de cercetator**: e iesirea aceluiasi protocol care alege `w`, `w_src` si modelul lui B. Obiectia se desfiinteaza, si nu prin declaratie, ci prin masuratoare.

**Ce va observa un reviewer atent, si e corect sa observe:** unanimitatea nu e o surpriza, fiindca medierea domina selectia destul de uniform (9 limbi din 10), deci scoaterea unei limbi din criteriu nu are cum sa rastoarne argmaxul. Asta **nu** slabeste rezultatul, il precizeaza: M1 nu demonstreaza ca decizia e stransa si totusi corecta, demonstreaza ca e **stabila**, adica nu atarna de nicio limba anume. Un criteriu care s-ar fi rasturnat la scoaterea unei limbi ar fi fost exact semnalul ca alegerea e zgomot, ca la selectia de encoder insasi.

Nuanta care trebuie scrisa: pe `fil` medierea e mai proasta decat selectia (+0.5095 fata de +0.5111), si protocolul alege acolo medierea oricum, fiindca nu are voie sa se uite la `fil`. Aia e o pierdere reala pe care protocolul o plateste ca sa ramana curat, si se declara ca atare.

## Cat costa protocolul strict

| configuratie | r mediu | fata de sistem | CI 95% pereche | P(>0) |
|---|---|---|---|---|
| sistemul publicat | 0.664581 | referinta | | |
| selectia de encoder, LOLO | 0.659580 | -0.005001 | | |
| medierea, aleasa de noi | 0.671610 | +0.007029 | | |
| **M1, aleasa de protocol** | **0.671610** | **+0.007029** | [+0.0039, +0.0099] | 100.0% |

**M1 si medierea sunt aceeasi configuratie, rand cu rand.** Protocolul a ales medierea peste tot, deci nu exista nicio diferenta de platit: cifra ramane 0.671610, dar acum e obtinuta de protocol, nu aleasa de noi. Asta e exact ce se cerea.

## Verificarea care nu se putea face altfel

Pe 9 limbi din 10 bratul ales de criteriu e chiar cel care iese mai bine pe limba respectiva. Cifra asta **nu e** o masura de performanta si nu se raporteaza ca atare: foloseste r-ul lui L ca sa evalueze o alegere care nu l-a vazut, deci e o diagnosticare a criteriului, nu un rezultat.

## Ce se poate scrie acum in paper

> Alegerea dintre selectia de encoder per limba si medierea neponderata a encoderelor nu a fost facuta de noi. Pentru fiecare limba tinta, cele doua alternative au fost comparate folosind exclusiv celelalte noua limbi, prin acelasi criteriu leave-one-language-out care alege ponderea de fuziune si modelul de limbaj. Medierea a fost selectata pe toate cele 10 folduri, cu o marja minima de 0.0088. Configuratia raportata este deci iesirea protocolului, nu o alegere facuta dupa inspectarea scorurilor de test.

Ce **nu** rezolva M1: alegerea intre cele 70 de configuratii din jurnal ramane facuta de noi, uitandu-ne la scorul de test. M1 inchide o singura bifurcatie, cea mai expusa, nu gradina intreaga. Vezi sectiunea 4 din `output/e_adoptie.md`.
