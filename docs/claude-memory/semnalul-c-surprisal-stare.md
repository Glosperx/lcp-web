---
name: semnalul-c-surprisal-stare
description: "INCHIS 23 aug 2026: C a trecut prin frontiera si prin fuziune, -0.000363 cu fil stricata; coloana lui gemma era degenerata; nu se mai redeschide"
metadata:
  type: project
---

Verificat **23 august 2026**, pentru pregatirea sesiunii pe al treilea semnal.

## C exista deja pe disc, si nu costa nicio inferenta

Coloana `C` din `output/bakeoff_test_Text/*.csv`, alaturi de `B`. **5593 din 5624 de randuri au
valoare finita.** Deci intreaga analiza se poate face cu zero rulari de LLM.

r al lui C cu eticheta, pe test, mediat pe zece limbi (`output/e_bakeoff_test.md`):

    qwen3-8b-4bit    +0.094
    qwen35-9b-8bit   +0.003
    gemma4-12b-4bit  -0.065     <- ASTA e modelul adoptat pentru B

**Semnul se schimba si intre modele si intre limbi.** La `qwen3-8b-4bit`: de +0.265, si +0.186,
en -0.055. La gemma, care e modelul lui B: ja -0.143, fil -0.136, en +0.043.

Pe romana, in `solutie_finala.py`, `W_SURP = 0.08` peste A+B a produs 68.90, deci acolo a ajutat.
Nota din `e_bakeoff.md`: "pentru C se raporteaza r cu semn, fara selectie: surprisal-ul e o statistica
bruta, nu o nota, si intra in fuziune abia daca aduce ceva peste B".

## De ce nu e inchis, desi r e aproape zero

Sesiunea din 23 august a stabilit ca **constrangerea care leaga nu e calitatea, e decorelarea**
(vezi [[transmisia-a-fuziune-masurata]]). C e o cantitate fundamental diferita de A si de B:
previzibilitate contextuala dintr-un LM cauzal, nu trasaturi dintr-un encoder inghetat si nici o nota
explicita. **Corelatia lui cu A si cu B n-a fost niciodata masurata**, deci n-a trecut niciodata prin
frontiera. Costul de a afla e zero.

## SHAP-ul de pe disc e STALE

`output/shap/` e din **23 iulie** si e pe conducta **romaneasca**: antetul spune
"Pearson test (toate) = 0.7898", care e cifra romaneasca, nu 0.683849 al multilingvului. Trasaturile
listate sunt zipf 0.4536, embedding(768) 0.1433, length 0.0377. Scriptul e `analysis_shap.py`.
**Se reface pe multilingv inainte de a cita ceva de acolo.**

Eye-tracking-ul ramane inchis definitiv, vezi [[eye-tracking-cat-a-adus-in-r]].

---

## INCHIS, 23 august 2026

C a trecut prin frontiera si prin fuziune, cap la cap. **Nu se mai redeschide.**

- **Coloana lui gemma era DEGENERATA**, nu slaba: surprisal mediu 23.95 peste ln|V| = 12.48. Deci cifra
  de -0.065 din fisa asta nu masura surprisal. Vezi [[gemma-nu-poate-da-surprisal]].
- **rho cu fuziunea e MIC**, cum se banuia: +0.125 la qwen3, +0.069 la llama31, +0.011 la qwen35. Deci
  premisa "r mic, rho probabil mic" era corecta. **Si tot nu ajunge:** corelatia partiala cu eticheta,
  controland pe fuziune, e +0.038 la cel mai bun candidat, fata de o poarta de 0.1077. Vezi
  [[poarta-al-treilea-semnal-0107]].
- **Masurat cap la cap**, cu u ales LOLO pe grila care contine zero si negativul: **-0.000363**, CI
  pereche [-0.001264, +0.000517], P(>0) = 21%, cu **filipineza stricata**. Podeaua de zgomot: -0.000140.
- **Cauza nu e taria semnalului, e semnul**: germana vrea u = +0.18 si filipineza u = -0.36, amandoua
  peste pragul lor, in directii opuse. Iar tiparul e o proprietate a LIMBII, nu a modelului (trei
  familii coreleaza intre ele la 0.95-0.99 peste limbi), deci **un ansamblu de surprisal-uri nu-l poate
  repara.**
- Literatura prezicea asta: Oh si Schuler, JML 2025, arata ca **frecventa si surprisal-ul sunt
  compensatorii**. Sistemul nostru are deja frecventa si se sprijina puternic pe ea.

Ce ramane declarat si nerulat: surprisal din capul de MLM al lui XLM-R, si C de la un model sub 4B,
care ar testa inverse scaling (marimile disponibile sunt doar 8B, 9B, 12B, iar cea de 12B a cazut din
alt motiv).
