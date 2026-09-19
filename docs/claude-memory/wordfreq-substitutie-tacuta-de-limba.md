---
name: wordfreq-substitutie-tacuta-de-limba
description: "wordfreq nu ridica eroare pe limba neacoperita: cauta tacut in engleza (si -> en) si CRAPA pe japoneza fara MeCab; garda se scrie pe available_languages, nu pe valoare"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb1aa51e-afc5-4256-99a6-5e987e99a85d
  modified: 2026-08-16T13:10:21.998Z
---

Măsurat pe **16 august 2026**, `wordfreq` 3.1.1 în `ml_def`. Închide verificarea B.2. Cifrele complete
sunt în repo, la `output/b2_wordfreq_coverage.md`.

Cele trei lucruri neevidente, fiindcă niciunul nu e ce se aștepta planul:

1. **Pe o limbă neacoperită nu ridică `LookupError` și nu întoarce curat zero. Face substituție tăcută
   de limbă:** `si` este căutat în lista de frecvențe **engleză**, cu un simplu warning. Același
   mecanism trimite `tl` către `fil`, unde e benign.
2. **Deci garda se scrie pe `available_languages()`, nu pe valoarea întoarsă.** O gardă de forma
   „zipf == 0 deci indisponibil" ar marca greșit și cuvintele rare **real acoperite** din celelalte 9
   limbi. Azi sinhaleza iese uniform zero pe toate cele 600 de ținte doar fiindcă niciun cuvânt
   sinhalez nu apare în lista engleză, și fiindcă nu există nicio țintă pur ASCII în setul sinhalez.
   Un împrumut în alfabet latin ar primi o frecvență englezească reală, adică activ greșită.
3. **Pe japoneză CRAPĂ**, `ModuleNotFoundError: No module named 'MeCab'`. Nu degradează tăcut. Blochează
   E1 pe una din cele 10 limbi de holdout. Reparația e extra-ul `wordfreq[mecab]`, care aduce
   `mecab-python3`, `ipadic`, `mecab-ko-dic`. Neinstalat încă, cere aprobare.

`fil` e acoperit **nativ** de `wordfreq`, care acoperă 42 de limbi. `si` nu e.

**Why:** e exact tiparul de bug tăcut din [[rute-rulare-logits]] și din fallback-ul `lg if isinstance(lg, str) else "en"`
pe care reparația A.1 îl elimină: o valoare plauzibilă produsă prin mecanismul greșit. Aici biblioteca
însăși face substituția, deci reparația noastră trebuie să o preceadă, nu să o corecteze după.

**How to apply:** la orice trăsătură lexicală per limbă, verifică întâi acoperirea declarată a sursei,
nu ieșirea ei. Vezi [[lemele-ro-sunt-gold-primite]], [[fertilitate-tokenizere-masurata]].
