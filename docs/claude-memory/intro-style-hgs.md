---
name: intro-style-hgs
description: Coordonatorul cere ca introducerea paperului să urmeze modelul Columbia hgs pe 5 paragrafe
metadata: 
  node_type: memory
  type: reference
  originSessionId: d9a89e1a-84a5-41a4-a6ef-303bfbb5b38f
  modified: 2026-07-27T13:37:05.162Z
---

<https://www.cs.columbia.edu/~hgs/etc/intro-style.html> — modelul de introducere cerut explicit de
profesorul coordonator prin email (iulie 2026).

Structura: **P1 motivație** (de ce contează pentru comunitate) → **P2 problema specifică** →
**P3 contribuții** (paragraful-cheie, „really really good", rezultate multiple în listă numerotată) →
**P4 diferențiere** față de literatură, la nivel înalt → **P5 roadmap**.

Reguli: fără „ce nu face lucrarea"; propoziție-temă la începutul fiecărui paragraf; timpuri verbale
consistente în interiorul unui paragraf. Numărul de paragrafe e flexibil dacă elementele sunt acoperite.

**Paper-model, adăugat pe 27 iulie 2026:** `2605.07466_6048.pdf` din rădăcina repo-ului (Anghel et al.,
fatty pancreas, tot de la FMI Unibuc). Se împrumută **retorica, nu formatarea** — e template SciTePress,
nu ACL. Ce s-a preluat efectiv la revizia 3: motivația stratificată pe două paragrafe (miza → rețeta
standard și presupoziția ei) în loc de unul; contribuții cu lead-in bold, 3–5 rânduri, o revendicare
și o cifră fiecare; claim explicit de noutate; fraze de gap la finalul blocurilor din Related Work.
Ce **nu** s-a preluat: paperul-model n-are paragraf de roadmap, dar tutorialul îl cere, deci a rămas.

**Clarificat pe 27 iulie 2026, la întrebarea lui Alexandru: ghidul guvernează DOAR Secțiunea 1.**
Cele cinci paragrafe sunt structura din interiorul introducerii, nu numărul de secțiuni al lucrării.
Structura `1. Introduction` + `2. Related Work` **bifează ghidul**, pentru că P4 o cere textual:
*„Keep this at a high level, you can refer to a future section where specific details and differences
will be given."* Adică ghidul presupune o secțiune Related Work separată. Ambele papere-model fac la
fel. Maparea de arătat coordonatorului: P1 → ¶1, P2 → ¶2 + ¶3, P3 → ¶4 cu contribuțiile,
P4 → ¶5 diferențiere care se închide cu trimitere la Secțiunea 2, P5 → ¶6 roadmap.

**Anti-tipar prins tot atunci.** Ghidul interzice explicit *„Avoid redundant phrasing, 'In Section 2,
In section 3, ... In Section 4, ...'"*, iar roadmap-ul nostru făcea exact asta pe patru secțiuni la
rând. Rescris ca să enumere conținutul, nu secțiunile.

**Cele două sfaturi generale de la finalul ghidului** (frază-temă per paragraf, concordanța
timpurilor) sunt singurele care se transferă în afara introducerii; le-am folosit ca listă de
verificare și pe Related Work.

Vezi [[paper-target-mrl-emnlp-2026]], [[paper-overleaf-workflow]] și
[[preferinte-de-scriitura-paper]] pentru regulile de formulare care s-au adăugat peste ghid.
