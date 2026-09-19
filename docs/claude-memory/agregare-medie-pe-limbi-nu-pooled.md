---
name: agregare-medie-pe-limbi-nu-pooled
description: "Reperele se compara ca MEDIE a celor 10 Pearson per limba, nu ca Pearson pooled; 0.6241 al lui TMU-HIT e pooled si nu se pune langa 0.6568; bara zero-label reala e 0.6100"
metadata:
  node_type: memory
  type: project
---

Lamurit **18 august 2026**, dupa ce Alexandru a intrebat direct de ce TMU-HIT raporteaza 0.6241 dar
Nohejl scrie 0.654. Tabelul complet, cu surse si verificare reproductibila, e in repo la
**`output/repere_publicate.md`**. Nu re-deriva, citeste fisierul.

## Cele doua cantitati, si de ce nu se amesteca

- **Pooled / compozit:** un singur Pearson calculat o data peste toate instantele amalgamate. E
  trackul "combined" al shared task-ului. TMU-HIT raporteaza in propria lucrare 0.6241 (three-shot)
  si 0.5609 (zero-shot). **Astea sunt pooled.**
- **Media pe limbi:** media aritmetica neponderata a celor 10 corelatii. E ce foloseste Nohejl in
  Tabelul 13 si **e ce folosim si noi**.

Dovada ca nu sunt acelasi lucru: mediind aceleasi doua rulari per limba iese **0.6100** si **0.6372**,
nu 0.5609 si 0.6241. Verificat cu asserturi in `output/repere_publicate.md`.

**Noi nu putem produce un compozit deloc**, fiindca standardizam in interiorul limbii, ceea ce sterge
nivelul absolut intre limbi. De scris ca limitare in text, inainte s-o gaseasca un reviewer.

## Ce inseamna pentru revendicare

**0.654 al lui TMU-HIT e cel mai bun run PER LIMBA**, verificat exact pe toate 10 fata de Anexa B a
shared task-ului. La `fil` si `fr` cel mai bun e zero-shot, la restul three-shot. Deci bara amesteca
doua protocoale, alegand per limba ce a iesit mai bine pe test.

Bara corecta, comparabila ca protocol cu a noastra, e **TMU-HIT zero-shot uniform, 0.6100**. Fata de
ea suntem la **+0.047**, nu la -0.0003. Asta e propozitia din abstract, nu "suntem la 0.0003 sub
G-Eval". Vezi [[etapa2-test-rezultate]] si [[fixul-de-lema-multilingv-masurat]].

**Franceza explica singura tot deficitul fata de G-Scale.** Fara ea, pe 9 limbi, dam 0.665 fata de
0.657 al lui G-Scale si 0.645 al lui G-Eval, deci **peste tot ce s-a publicat**.

**Why:** doua cifre publicate care arata amandoua ca "media pe toate limbile" sunt de fapt metrici
diferite, iar punandu-le alaturi lucrarea ar fi aratat ca o comparatie masluita.

**How to apply:** orice cifra noua de reper trece prin `output/repere_publicate.md` inainte sa intre
in paper. Sinhaleza corecta e **0.3430**, nu 0.3495; aia era dinainte de lema.
Vezi [[noutate-si-precedente-lcp-multilingv]].

## Actualizat dupa P11, 19 august 2026

Sistemul e acum **0.674946** pe n=5624, deci fata de bara zero-label comparabila, TMU-HIT zero-shot
uniform la 0.6100, marginea e **+0.0649, castigand pe 9 limbi din 10**, nu +0.047. Fata de G-Scale
0.669 suntem cu **+0.0060 PESTE**, dar intervalul mediei noastre e [0.6597, 0.6890], lat de 0.0294,
deci diferenta e 20% dintr-o latime de interval si **„batem cel mai bun sistem publicat" tot nu se
sustine**. Tabelul actualizat e in `output/repere_publicate.md`. Vezi [[p11-adoptia-facuta]].

