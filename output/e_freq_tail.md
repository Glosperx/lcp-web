# Frecventa pentru limbile de coada, din Wikipedia

Generat de `build_freq_tail.py`. Sursa: `wikimedia/wikipedia`, dump 20231101.

## `si` (wiki `si`)

- 8,033,151 tokeni, 491,077 tipuri distincte
- cele mai frecvente 8: `සහ` (7.01), `අතර` (6.89), `වන` (6.86), `හා` (6.84), `ලෙස` (6.8), `මෙම` (6.73), `වූ` (6.71), `විය` (6.67)

## `fil` (wiki `tl`)

- 12,265,578 tokeni, 377,474 tipuri distincte
- cele mai frecvente 8: `ng` (7.81), `sa` (7.78), `ang` (7.64), `na` (7.63), `mga` (7.57), `ay` (7.4), `at` (7.38), `isang` (7.11)

## Acoperirea pe tintele de test, in trepte de backoff

Treapta 1 e forma exacta. Treapta 2 e cel mai lung PREFIX de cel putin 4 caractere care apare in tabel, ca inlocuitor de stem pentru limbile aglutinante care sufixeaza. Treapta 3 e primul subword al tokenizerului XLM-R, care e o segmentare invatata si nu cere niciun lematizator.

Exemple de backoff pe prefix, `si`: `අහස්දිය` -> `අහස්` (4.24); `මගඩිය` -> `මගඩි` (2.4); `දෙනෙත්වල` -> `දෙනෙත්` (3.48); `බොජුන්හලක` -> `බොජුන්` (3.6)

Exemple de backoff pe prefix, `fil`: `dumilat` -> `dumila` (1.91); `hayan` -> `haya` (3.48); `kalikutin` -> `kali` (3.65); `mamaos` -> `mama` (4.1)

```
        n  wordfreq_ok  exact  plus_prefix  plus_subword  ramase  pct_exact  pct_plus_prefix  pct_plus_subword
lang                                                                                                          
si    600            0    539          598           600       0       89.8             99.7             100.0
fil   570          418    513          557           570       0       90.0             97.7             100.0
```

`wordfreq_ok` e cate tinte aveau frecventa NENULA in sistemul de acum. Pe `si` e zero prin constructie, fiindca limba nu e servita deloc.

