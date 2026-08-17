# B.2 închisă: ce face `wordfreq` pe limbile MLSP

Măsurat pe 16 august 2026, `wordfreq` 3.1.1, în `ml_def`. Verificarea A2 din raport, care bloca A.3.

## Răspunsul la întrebarea pusă

Întrebarea era dacă `wordfreq` întoarce 0.0 sau ridică `LookupError` pe o limbă neacoperită.
**Niciuna din două.** Face **substituție tăcută de limbă**:

```
You asked for word frequencies in language 'si'. Using the nearest match, which is 'en'.
```

Sinhaleza e căutată în lista de frecvențe **engleză**. E un `warning`, nu o excepție, deci în
producție dispare complet.

## Cele 10 limbi, măsurat

| Limbă | Acoperită nativ | Comportament | Note |
|---|---|---|---|
| en, de, fr, it, es, ca, pt | da | corect | |
| fil | **da** | corect | `tl` e rezolvat automat către `fil` de `wordfreq` |
| si | **nu** | **substituție tăcută către `en`** | |
| ja | da | **CRAPĂ** | `ModuleNotFoundError: No module named 'MeCab'` |

`wordfreq` acoperă nativ 42 de limbi. `si` nu e printre ele, `fil` da.

## Sinhaleza: azi produce zerouri, dar prin mecanismul greșit

Măsurat pe toate cele 600 de ținte sinhaleze din `multils_test_sinhala_lcp_labels.tsv`:

- ținte cu zipf nenul, adică găsite în lista **engleză**: **0 din 600**
- ținte pur ASCII în setul sinhalez: **0**

Deci azi coloana de frecvență e uniform zero pe sinhaleză. **Dar nu fiindcă limba e declarată
neacoperită, ci fiindcă niciun cuvânt sinhalez nu apare în lista engleză.** Distincția contează:
mecanismul e o căutare în limba greșită, iar dacă setul ar conține un împrumut în alfabet latin sau
un număr, ar primi o frecvență englezească reală, adică activ greșită, nu zero.

Garda din A.3 trebuie deci să verifice **acoperirea limbii**, cu `available_languages()`, nu valoarea
întoarsă. O gardă scrisă ca „dacă zipf == 0 atunci indisponibil" ar fi greșită: ar marca și cuvintele
rare real acoperite din celelalte 9 limbi.

## Japoneza: blocant nou, nu e în niciun plan

`zipf_frequency(w, "ja")` ridică `ModuleNotFoundError: No module named 'MeCab'`. `wordfreq` are nevoie
de un tokenizator extern pentru japoneză, declarat ca extra:

```
mecab-python3, ipadic, mecab-ko-dic   ; extra == "cjk" or extra == "mecab"
jieba                                 ; extra == "cjk" or extra == "jieba"
```

Deci `lexical()` la [solution_bert.py:147](solution_bert.py#L147) **crapă** pe japoneză, nu degradează
tăcut. Blochează E1 pe una din cele 10 limbi de holdout.

Reparația e o instalare, `wordfreq[mecab]`, **de aprobat înainte**. Varianta `[cjk]` aduce în plus
`jieba` pentru chineză, de care nu avem nevoie.

## Aliasul fil/tl

`wordfreq` rezolvă singur `tl` către `fil`, tot printr-un warning de „nearest match". Ambele dau
`zipf('bahay') = 6.0`. Harta noastră de aliasuri trebuie deci să normalizeze explicit la `fil`, ca să
nu depindem de mecanismul de „nearest match", care e același cu cel care trimite sinhaleza pe engleză.
