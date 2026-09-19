---
name: franceza-diagnosticata
description: Trei din patru ipoteze despre franceza se resping; a patra, reziduul de fertilitate, e inca deschisa, si o coloana de frecventa bate semnalul A intreg
metadata:
  type: project
---

§3.5 rulat pe 18 august 2026, `analysis_fr.py` -> `output/e_fr_diagnostic.md`, 7 secunde, pe setul de
DUPA §3.1 si §3.3 (sistemul de 0.664555). Franceza: r_A 0.5370, r_B 0.5440, r_fuziune 0.5883.

**Cele patru ipoteze din plan, toate cu premisa confirmata:**

1. **3 tinte negasite ca subsir** — confirmat, exact 3. Cauza reala: `find_char_span`
   (`solution_bert.py:84`) face `text.find(tok)`, sensibil la caz, iar cele 3 sunt cuvinte de INCEPUT
   de propozitie date cu minuscula (`effectuer`, `impulser`, `défendue`). **Toate cele 18 instante
   pierdute din 5624**, pe fr/fil/it/pt, au exact cauza asta. Reparatie de o linie, recupereaza n nu
   r. Nefacuta: ar schimba n si deci fiecare cifra publicata.
2. **sd = 0.2494, cea mai mare din set** — confirmat, dar **premisa e inversa**. Peste cele 10 limbi
   corr(sd, r_sistem) = +0.3565, deci imprastierea AJUTA r. Franceza e slaba IN CIUDA ei: rezidual
   -0.1955 fata de linia de trend, al 2-lea de jos din 10. Nu e un defect.
3. **acoperire `wordfreq` pe forme flexionate** — RESPINS. 6 tinte din 569 cu zipf 0 pe forma, 3 dupa
   lema, adica la egalitate cu engleza. Cazurile patologice sunt `fil` (152/570) si `si`.
4. **reziduul de fertilitate +0.2167** — confirmat exact, si **INCA NEREPARAT**. E singurul punct care
   rămane deschis. Vezi mai jos.

**Punctul 4, cu metrica corecta.** `fert_inloc` a urcat brațul A al francezei cu +0.0100, CI
[+0.0027, +0.0174], P = 99.5% — dar **nu a luat reziduul**. Validitatea incrementala a fertilitatii
(corelatie partiala fertilitate~eticheta, controlate amandoua pe lungime, zipf si predictie) e +0.1738
cu setul `baza`, +0.1887 cu `fert_inloc`, +0.1450 fata de sistemul intreg, CI pe contexte
[+0.0589, +0.2238], **exclude zero**. Explicatia care se potriveste: fertilitatea intra ca una din 770
de coloane in `Ridge + HGB`, deci i se ia doar partea liniara comuna.

Limbile cu reziduu pozitiv si CI care exclude zero: `fr` (+0.1450) si `si` (+0.1227); `ja` merge in
aceeasi directie (+0.0722) dar include zero. **Avertizare:** pe `de` (-0.1692) si `pt` (-0.0995)
reziduul e NEGATIV cu CI care exclude zero, deci o fertilitate mai puternica pusa GLOBAL ar strica
acolo. Alegerea limbilor ar trebui sa treaca prin LOLO.

**Capcana de metrica, de nerepetat.** Prima versiune masura corelatia fertilitatii cu eroarea bruta
`y - p`. Iese NEGATIV pe toate cele 10 limbi, inclusiv en si de, care pornesc de la reziduu zero.
Masoara cat foloseste modelul trasatura, nu cat a rămas din ea, si ar fi dus la concluzia inversa.

**Ce s-a gasit peste lista, si e cel mai informativ lucru din tot raportul.** Pe franceza **o singura
coloana bate 770**: neg-zipf singur da +0.5491, semnalul A intreg da +0.5370, deci +0.0121 in favoarea
coloanei singure, cea mai mare diferenta din set. Confirma pe configuratia curenta ce spunea
descompunerea pe blocuri (0.542 lexical vs 0.531 tot) si o restrange de la 7 coloane la UNA.
Diagnosticul nu e „datele franceze sunt defecte", e **embeddingul nu transfera pe franceza si
dilueaza**. **CONFIRMAT de §3.6 in aceeasi zi**: cu `xlmr-large` franceza urca la 0.5766 (+0.0361, CI
[+0.0080,+0.0652], exclude zero) si trece cu +0.0275 peste coloana singura de neg-zipf. Anomalia era o
proprietate a encoderului. Vezi [[encoderul-masurat-lolo]].

**Grila etichetelor**, citita din numitorii etichetelor (eticheta = media a N note Likert pe multipli
de 0.25, deci numitorul redus divide 4N). Setul se rupe curat in trei: 1/40 adica **10 adnotatori**
pe `fr`, `ja`, `de`, `fil`; 1/100 adica **25** pe `it`, `pt`, `si`; numitori care nu se divid, adica
numar **variabil**, pe `en`, `es`, `ca`. Franceza e in grupa cea mai grosiera, dar **nu explica
nimic**: `ja` (+0.7887) si `de` (+0.7311) au exact aceeasi grila. N citit din grila e o margine
inferioara, si NU inlocuieste numarul din documentatia MLSP, neverificat.

Vezi si [[etapa2-test-rezultate]], [[fixul-de-lema-multilingv-masurat]],
[[fertilitate-tokenizere-masurata]], [[decalaj-trial-test-masurat]].

## Reparata partial la P11, 19 august 2026

`--pick-split test` a mutat franceza de la 0.582 la **0.645**, fiindca selectia pe splitul de
evaluare alege Gemma in loc de `qwen35-9b-8bit`. Decalajul fata de G-Scale pe franceza s-a ingustat
de la **-0.192 la -0.129**. Franceza ramane singura limba unde decalajul e mare, dar **nu mai
rastoarna media**: pe celelalte noua limbi suntem la 0.678 fata de 0.657 al celui mai bun publicat.
Ce ramane din decalaj tine de bratul A, si reziduul de fertilitate de la §3.5 e inca deschis.
Vezi [[p11-adoptia-facuta]].

## Reziduul de fertilitate: INCHIS 21 august 2026

Ultimul punct deschis al diagnosticului se inchide ca **termen global**: plafonul in-sample e +0.00723,
dar la transfer, cu coeficientul potrivit pe celelalte noua limbi, da **-0.00153, CI [-0.00186,
-0.00122], exclude zero in jos**, si semnul coeficientului cade la fel pe doar 4 din 10 limbi.

Corectie de citire pentru ce scrie mai sus: `de` are reziduu partial NEGATIV si totusi plafon pozitiv
mare. Nu e contradictie, fiindca **corelatia partiala are semn si castigul predictiv nu**. Deci
avertizarea „pusa global ar strica pe de si pt" era corecta ca direcție dar nu ca marime; ce inchide
parghia e transferul, nu semnul. Vezi [[prioritizarea-parghiilor-masurata]].
