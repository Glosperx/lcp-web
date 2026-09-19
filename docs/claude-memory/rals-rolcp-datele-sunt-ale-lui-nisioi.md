---
name: rals-rolcp-datele-sunt-ale-lui-nisioi
description: "Setul de test de 1587 de exemple e RoLCP din RALS (EMNLP 2025), al cărui ultim autor e Sergiu Nisioi, coordonatorul lui Alexandru"
metadata: 
  node_type: memory
  type: project
  originSessionId: 22f6ea41-f9db-4e9e-aac2-9a0b5065c375
  modified: 2026-07-30T10:28:42.221Z
---

Descoperit pe **27 iulie 2026**, plecând de la paperul-model ETRA pe care l-a dat chiar Alexandru.

Setul de test de **1.587 de cuvinte-țintă este RoLCP**, publicat în *RALS: Resources and Baselines
for Romanian Automatic Lexical Simplification* (Fabian Anghel, Petru Theodor Cristea, Claudiu
Creangă, **Sergiu Nisioi**), **EMNLP 2025 main conference**, Universitatea din București. Cheia ACL
Anthology: `anghel-etal-2025-rals`. Potrivirea exactă a dimensiunii plus formularea continuă în
[0,1] nu lasă loc de dubiu.

**Sergiu Nisioi este coordonatorul lui Alexandru.** Shared task-ul e cel mai probabil construit de
grupul lui, prin proiectul InstRead (nlp.unibuc.ro). Alexandru nu știa pe ce date lucrează.

Fapte verificate direct:

- **3.921 de exemple adnotate** public pentru română: 569 HT + 1.765 WT + **1.587 RoLCP**.
  `github.com/senisioi/RALS`, `data.zip`, arhivă cu parola `ralsresources` publicată chiar în README
  ca să nu fie crawl-uită de LLM-uri. Licență CC BY-NC-SA 4.0.
- Ei raportează un **baseline supervizat Ridge cu r = 0.71** pe RoLCP, cross-validat.
- Cea mai apropiată lucrare de unghiul nostru: **Kuvshynova et al., ETRA 2026**, *Analyzing the
  Relationship Between Reading Times and Lexical Complexity Prediction in Romanian*, care combină
  RoLCP cu eye-tracking MultiplEYE românesc. Necitată și ea.

**Distincția care contează.** „Nu folosim nicio etichetă românească" e **adevărat** și e chiar
înțelegerea cu Sergiu, setarea fără etichete fiind o constrângere metodologică deliberată. „Nu există
etichete românești" și „niciun sistem anterior nu prezice complexitatea lexicală pentru română" sunt
**false**. Primul enunț e despre ce facem noi, celelalte două despre lume.

Ca urmare, la revizia 8 au fost scoase cinci afirmații false din `paste_intro.tex`, `paste_body.tex`
și `paste_limitations.tex`. Detaliile exacte sunt în header-ul lui `paste_intro.tex`.

**ACTUALIZARE, 30 iulie 2026: RALS ESTE ACUM CITATĂ.** Sergiu a confirmat că trebuie citată, iar
integrarea a fost făcută. Nu a fost o linie în bibliografie: **cinci afirmații din text deveneau false
în momentul citării** și au fost reparate, plus trei adăugiri care întăresc lucrarea. Detaliile
complete sunt în blocul de comentariu din `Paper/Articol_Complexity/paper_full.tex`, abaterea 7.

Cheile de citare: `anghel-etal-2025-rals` și `cristea-nisioi-2024-machine`. A doua e *Archaeology at
MLSP 2024*, muncă anterioară pe transfer cross-lingual de complexitate pentru română, prin traducere
în engleză, necitată până atunci. **Trei corecții față de metadatele Anthology**, altfel numele ies
greșit: al doilea autor RALS e despicat prost (`Petru-Theodor, Cristea` → `Cristea, Petru Theodor`),
`Creanga` primește diacritica (`Creang{\u a}`), și `MLSP` se bracket-ează ca să nu iasă „mlsp".

Rămâne deschis doar **Kuvshynova et al. 2026 (ETRA)**, tot necitată.

**Concluzia lor pe care lucrarea o contrazice:** RALS scrie explicit că „cross-lingual transfer of
complexity scores is not a viable resource creation procedure, causing distribution shifts", iar
`cristea-nisioi-2024-machine` obține `r ≈ 0.3` pe ruta prin traducere. Rezultatul nostru e
contraexemplul. **Alexandru a cerut să NU se facă polemică din asta**: în 2.2 se menționează doar
munca anterioară și diferența de rută, fără „our result is the counterexample" și fără concluzia lor
negativă. Un recenzent care citește RALS vede tensiunea; dacă apare la recenzii, se adaugă o frază
atunci.

**Why:** invalidează orice revendicare de noutate prin absență și schimbă teza lucrării. Riscul e
mare tocmai pentru că lucrarea contrazisă e la EMNLP main și aparține grupului propriu; un reviewer
din comunitatea aia o vede imediat.

**How to apply:** nu scrie niciodată că nu există date sau sisteme LCP pentru română. Formularea
corectă e că noi alegem să nu folosim etichetele. Scorarea pe etichetele RoLCP **a fost făcută** pe 30
iulie 2026, cu rezultate în [[r-si-r2-masurate-pe-rolcp]]; cifrele nu sunt în paper și intrarea lor
depinde de acordul lui Sergiu. Vezi și [[paper-slabiciuni-de-reviewer]] și
[[paper-target-mrl-emnlp-2026]].
