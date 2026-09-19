---
name: frequency-unavailable-e-flag-de-sinhaleza
description: "Mecanismul exact al feature-ului frequency_unavailable din SHAP: e constant per limba (nu per cuvant), si in cele 11 limbi ale proiectului practic un flag de sinhaleza"
metadata:
  node_type: memory
  type: project
  originSessionId: 61c4f607-25b4-4e50-9827-f13f53d75c5c
  modified: 2026-08-29T18:47:39.090Z
---

Continuarea lui [[shap-signal-a-feature-importance]]: Alexandru a intrebat ce inseamna exact
"frequency_unavailable" dupa ce am semnalat ca amplitudinea lui in beeswarm (~-0.20) pare mare
pentru un indicator care ar trebui sa fie doar despre cuvinte rare.

## Mecanismul, verificat in cod

`solution_bert.lexical()` (linia 199), cu `na_policy="mlsp"`, cheama `zipf_safe(t, lg)` din
`mlsp_common.py:388`, care intoarce `(z, disponibil)`. Coloana `frequency_unavailable`
(`solution_bert.py:278`) = `1.0` exact cand `disponibil=False`.

`disponibil` vine din `freq_available(lg)` (`mlsp_common.py:260`) care se uita DOAR la limba, nu
la cuvant: verifica `lg in wordfreq.available_languages()`, apoi face o proba
`zipf_frequency("a", lg)` in try/except (prinde cazul unde limba e listata dar tokenizatorul
extern lipseste, ex. MeCab pentru japoneza). Rezultatul e memoizat per limba in `_PROBED[lg]`
(`mlsp_common.py:257`) — deci in interiorul unei rulari, flag-ul e CONSTANT pentru toate
tokenurile aceleiasi limbi, niciodata per-cuvant, cu o singura exceptie: daca `TAIL_FREQ` (din
`build_freq_tail.py`, incarcat explicit prin `load_tail_freq()`) are o intrare pentru limba aia,
`zipf_safe` intoarce mereu `disponibil=True` pentru ea, indiferent daca tail-lookup-ul gaseste sau
nu cuvantul (vezi docstring-ul functiei: "un 0 inseamna rar real").

Verificat direct in `ml_def` (29 aug 2026), pe cele 11 limbi ale proiectului:

```
si:  NU e in available_languages()  -> freq_available = False
ja, fil, ro, en, ca, fr, de, it, pt, es: toate True (MeCab e instalat, deci ja trece proba)
```

Deci in acest mediu, singura limba unde wordfreq n-are acoperire nativa e sinhaleza. Daca
`TAIL_FREQ` n-a fost incarcat cu "si" in rularea de SHAP, `frequency_unavailable` = 1.0 pentru
100% din tokenurile sinhaleze si 0.0 pentru restul celor 10 limbi, punct. Asta explica clusterul
rosu compact din beeswarm (o banda ingusta la o singura valoare, nu o imprastiere continua ca la
word_frequency) si de ce importanta lui scade aproape la zero pe subsetul doar-romana (reziduul de
~0.017 ramas e doar interactiune SHAP cu celelalte trasaturi ale randului, nu semnal propriu,
fiindca pe romana coloana e mereu 0).

`surface_features_unavailable` e din aceeasi familie dar cu alta cheie: `SURFACE_APPLICABLE`
(`mlsp_common.py:35`, limbile cu alfabet latin) — deci practic un flag "e japoneza sau sinhaleza?"
(scriere non-latina), nu latin vs non-latin per cuvant.

**Why:** confirma cu cod, nu doar cu banuiala, riscul semnalat in analiza SHAP: aceste doua
"unavailable" nu sunt semnale lexicale de complexitate, sunt indicatori de identitate de limba
deghizati in feature de disponibilitate a datelor. Relevant pentru orice discutie despre ce sa
scrii in paper legat de interpretabilitatea modelului A.

**How to apply:** daca apare intrebarea "modelul invata complexitate sau invata sa recunoasca
limba?", raspunsul concret e aici: `frequency_unavailable` e constant per limba prin constructie
(`_PROBED`), deci orice importanta SHAP pe el trebuie citita ca "modelul a gasit ca sinhaleza (sau
alta limba neacoperita) se comporta diferit", nu ca "acest cuvant anume e rar". Daca se incarca
`load_tail_freq()` intr-o rulare viitoare, flag-ul se stinge pentru limbile din `TAIL_FREQ` si
semnalul de frecventa real vine din tabelul de rezerva in loc de indicator.
