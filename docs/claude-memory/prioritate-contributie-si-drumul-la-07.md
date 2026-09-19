---
name: prioritate-contributie-si-drumul-la-07
description: "22 aug 2026 - prioritatea lui Alexandru e contributia publicabila la o conferinta de top, cifra vine dupa; 0.700 nu se atinge prin configuratii, doar prin coada de limbi slabe, si acolo lipsesc resursele"
metadata:
  type: project
---

Spus explicit de Alexandru pe **22 august 2026**: cel mai important e o contributie publicabila la o
conferinta de top; cifra vine dupa, desi si-ar fi dorit sa se apropie de 0.7.

## Drumul la 0.700, aritmetic

Sistemul e 0.683849, media pe zece limbi. Per limba: en .8700, pt .8450, ja .7877, es .7641, de .7468,
it .6750, fr .6590, **ca .5566, fil .5091, si .4251**. Primele sapte fac media .764, ultimele trei .497.

Ca sa treci de .700 iti trebuie **+0.0162 pe medie**, adica +0.162 insumat peste limbi. Nicio parghie
de configuratie nu da atat: cea mai mare masurata vreodata e +0.006153 (`M3K`), iar castigul onest al
intregii linii de configuratii sub selectie LOLO e +0.0045.

**Dar sinhaleza singura ajunge.** De la .4251 la .5866 pune media exact la .700. Sinhaleza plus
filipineza, la .55 si .60, dau .7054. Deci drumul la 0.7 nu trece prin inca o configuratie, trece prin
coada.

## Ce blocheaza coada, si de ce e o observatie publicabila

Pe sinhaleza, unde sistemul e cel mai slab, **doua din cele trei trasaturi lexicale ale bratului A pur
si simplu nu exista**: `wordfreq` nu serveste sinhaleza (`output/e_lemma_coverage.md`, coloana
frecventa = nu) si stanza n-are lematizator pentru ea (600 din 600 randuri fara lema). In plus 214
tinte distincte din 600 de randuri, deci repetitie mare. Amandoua semnalele sunt slabe acolo: A .3166,
B .3860.

Asta nu e un esec de modelare, e o lipsa de resurse, si formulata asa e o observatie in sine: pe limba
pe care mergem cel mai prost, doua din trei trasaturi lexicale nu exista in ecosistem.

**Falsul indiciu de retinut, ca sa nu se reia:** `v11_frecventa` parea sa fie exact raspunsul, cu r3
solo +0.456 pe sinhaleza pe trial fata de +0.050..+0.161 la ceilalti candidati. Pe test da +0.310, sub
B-ul sistemului de .3860. Nu e o pista. Vezi [[prompturi-decorelate-cernute]].

## Cerere deschisa

Alexandru vrea o sesiune separata in care sa i se explice in detaliu cum functioneaza tot proiectul,
cap la cap. Nu s-a facut inca. Regula din [[explicatii-tehnice-in-profunzime]] se aplica: la "ce
inseamna X mai exact" se coboara la cod, fisier si linie, plus exemplu numeric.

Vezi [[cifra-de-raportat-in-paper]] pentru ce se raporteaza si de ce.
