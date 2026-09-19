# M3. Leave-one-encoder-out pe medie

Generat 2026-08-19 10:34:29 de `analysis_m3.py`. Nicio inferenta: fisierele de predictii per encoder existau deja, deci `make_enc_mean.py` doar mediaza CSV-uri. Cele patru variante s-au rulat toate si se raporteaza toate; **alegerea uneia pe scorul de test ar fi acordare pe test si nu se face aici**. Date brute: `output/m3.csv`.

## Rezultatul

| configuratie | r fuziune | fata de sistem | CI 95% pereche | fata de media celor patru | CI 95% pereche |
|---|---|---|---|---|---|
| sistemul publicat, un encoder | **0.664581** | referinta |  | -0.007029 | [-0.0099, -0.0039] |
| media celor patru | **0.671610** | +0.007029 | [+0.0039, +0.0099] | referinta |  |
| media celor trei, fara `xlmr` | **0.670608** | +0.006027 | [+0.0019, +0.0098] | -0.001002 | [-0.0022, +0.0000] |
| media celor trei, fara `xlmr-large` | **0.669223** | +0.004642 | [+0.0011, +0.0079] | -0.002387 | [-0.0039, -0.0009] |
| media celor trei, fara `labse` | **0.670077** | +0.005496 | [+0.0030, +0.0079] | -0.001533 | [-0.0033, +0.0002] |
| media celor trei, fara `e5` | **0.671066** | +0.006485 | [+0.0036, +0.0092] | -0.000544 | [-0.0017, +0.0006] |

## Ce raspunde la fragilitate

**Niciun encoder nu duce singur castigul.** Toate cele patru medii de cate trei bat sistemul cu interval pereche care exclude zero, de la +0.004642 la +0.006485. Scoaterea oricarui encoder lasa castigul in picioare, deci medierea nu atarna de niciunul si argumentul „mediaza fiindca sunt decorelati" se sustine: **e robusta, nu norocoasa**. Cel mai mult se pierde scotand `xlmr-large`, si chiar si atunci raman +0.004642 fata de sistem.

## Ce raspunde la cost, si aici e cifra care conteaza

| configuratie | encodere la inferenta | forward pe test | fata de un encoder | castig pastrat |
|---|---|---|---|---|
| sistemul publicat, un encoder | 1 | 50s = 0.8 min | 1.0x | referinta |
| media celor patru | 4 | 281s = 4.7 min | 5.7x | 100% |
| media celor trei, fara `xlmr` | 3 | 232s = 3.9 min | 4.7x | 86% |
| media celor trei, fara `xlmr-large` | 3 | 150s = 2.5 min | 3.0x | 66% |
| media celor trei, fara `labse` | 3 | 231s = 3.8 min | 4.7x | 78% |
| media celor trei, fara `e5` | 3 | 232s = 3.9 min | 4.7x | 92% |

**Scoaterea lui `xlmr-large` e schimbul care conteaza.** Media celor trei ieftine da 0.669223, adica +0.004642 fata de sistem cu interval [+0.0011, +0.0079], deci **pastreaza 66% din castig**. Costul scade de la 4.7 la 2.5 minute, adica 47% mai putin, fiindca `xlmr-large` singur e 132s din 281s. Ce se pierde fata de media celor patru e -0.002387, cu interval [-0.0039, -0.0009].

**Dar obiectia de cost era deja slaba.** Pe conducta intreaga, cu LLM-ul la 102 minute, diferenta dintre patru encodere si trei e sub doua minute din o suta si sapte. Cine scoate `xlmr-large` o face ca sa piarda un model de 24 de straturi din dependinte, nu ca sa castige timp.

## Per limba, si `fil`

| limba | sistem | toate 4 | fara large |
|---|---|---|---|
| ca | +0.5283 | +0.5448 | +0.5413 |
| de | +0.7324 | +0.7420 | +0.7357 |
| en | +0.8663 | +0.8729 | +0.8718 |
| es | +0.7486 | +0.7579 | +0.7589 |
| fil | +0.5171 | +0.5095 | +0.5121 |
| fr | +0.5857 | +0.5927 | +0.5863 |
| it | +0.6625 | +0.6675 | +0.6651 |
| ja | +0.7887 | +0.7866 | +0.7835 |
| pt | +0.8375 | +0.8426 | +0.8413 |
| si | +0.3786 | +0.3997 | +0.3962 |
| **medie** | 0.664581 | 0.671610 | 0.669223 |

`fil` era limba care scadea, cu -0.0077 sub media celor patru, si cauza era localizata: `xlmr-large` e cel mai prost din patru acolo, cu -0.0554 pe brațul A. Scotandu-l, `fil` trece la -0.0051 fata de sistem, deci scaderea se ATENUEAZA cu +0.0026 dar **nu dispare**: `fil` ramane sub sistem si cu trei encodere, deci `xlmr-large` explica doar o parte din ea. Asta e un argument pentru varianta cu trei care nu e de cost, ci de comportament.

## Ce nu decide M3

M3 nu alege nimic. Daca varianta cu trei encodere s-ar adopta pentru ca are cifra convenabila, ar fi exact acordarea pe test pe care restul protocolului o evita. Alegerea dintre `toate patru` si `fara large` trebuie sa treaca prin acelasi criteriu leave-one-language-out ca la M1, sau sa fie declarata ca decizie de inginerie luata pe cost, nu pe scor. Cele doua sunt formulari oneste; a alege pe scor si a nu spune nu e.
