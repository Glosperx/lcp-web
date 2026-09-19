---
name: paper-slabiciuni-de-reviewer
description: "Punctele slabe ale paperului RO LCP față de un reviewer de workshop: cum au fost tratate și ce a rămas"
metadata:
  node_type: memory
  type: project
  originSessionId: d9a89e1a-84a5-41a4-a6ef-303bfbb5b38f
  modified: 2026-07-30T10:29:24.593Z
---

Identificate pe 23 iulie 2026 la trecerea raportului de curs în paper de workshop; tratate în
aceeași zi, în fișierele de paste din `Paper/Articol_Complexity/`.

**Decizia pe tuning (punctul cel mai serios).** Ponderile nu se retrag și 69.74 rămâne cifra
principală, dar încadrată: divulgare completă a celor 5 cantități tunate pe scorul public (3 ponderi
de fuziune + 2 constante de calibrare) și Pearson *r* ca metrică principală. **Argumentul cheie:**
calibrarea `clip(0.27 + 0.125·z)` e afină, iar clipul e inactiv pe predicțiile reale (interval
0.014–0.845), deci *r* e invariant la ea — cele două constante ating exclusiv termenul `R²`.

**CELE 14 EXEMPLE AU FOST SCOASE COMPLET din paper, 30 iulie 2026.** Alexandru a respins ideea pe
fond, nu pe formulare: „nu am testat pe acele 14, am testat pe setul RALS". Verificat în cod și are
dreptate — se numesc **`calib`** în tot proiectul (`crosslingual_cwi_calib.csv`, `X_calib.csv`,
`labeled_examples.csv`, toate cu 14 rânduri), `analysis_hardset.py` le exclude explicit („proxy onest,
**NU cele 14**"), iar `solutie_finala.py` nu citește niciun fișier `calib`, calibrarea folosește
constante hardcodate.

Ce a dispărut odată cu ele: subsecțiunea de Results, `tab:ro14`, `r = 0.913`, `0.894`, bootstrap-ul,
testul de permutare, și **limita de tuning `0.019`**. §3.5 păstrează doar argumentul algebric și
faptul că sweep-ul se întinde pe 0.84 puncte. Verificare de rulat: `grep -in 'fourteen\|14 items\|
0.913\|0.894\|0.019'` pe paper trebuie să dea **zero**.

**Condiția de scop a corecției pe lemă a rămas, dar reîncadrată** ca ilustrare calitativă pe un
singur cuvânt, în §3.3 (A), cu eticheta `sec:scope`: `putu`, perfect simplu al lui `putea`, rar și
arhaic, a cărui lemă e foarte frecventă; corecția îi ridică frecvența cu 2.76 unități Zipf și îl
prezice ușor. **Fără nicio corelație calculată pe 14 puncte** — alea erau exact obiecția, mutată cu
două secțiuni mai sus. Limitations spune acum, verificabil: „No number anywhere in this paper is
computed on Romanian gold labels."

**Ce nu se poate face în text, prin decizie:** *r* și *R²* nu sunt raportate. Lucrarea are, prin
construcție, **o singură cifră proprie pe română**, compozitul 69.74. Măsurate există, vezi
[[r-si-r2-masurate-pe-rolcp]], dar nu sunt în paper.

**Limita pe claim-ul de noutate (descoperit pe 27 iulie 2026, verificat pe ACL Anthology).**
Shared task-ul CWI 2018 (`yimam-etal-2018-report`) a avut patru piste: EN/DE/ES monolingv **plus
„a multilingual track with a French test set"**, adică exact un setup zero-shot cross-lingual.
Deci **nu se poate revendica „primul sistem LCP fără etichete în limba țintă"** — un reviewer care
știe CWI 2018 ar respinge-o imediat. Diferențierea față de pista franceză e explicită în Related
Work: ei cereau clasificare binară și probabilistică, nu predicție continuă, și ofereau date de
antrenare în trei limbi, una romanică.

**CORECȚIE, tot pe 27 iulie 2026: claim-ul de rezervă era și el fals și a fost scos.**
Formularea „no prior system predicts lexical complexity for Romanian", pe care o foloseam ca variantă
limitată la română, e neadevărată: setul nostru de test **este** RoLCP, iar autorii lui raportează un
baseline supervizat. **Nu mai există niciun claim de noutate prin absență în lucrare** și nu trebuie
reintrodus. Detaliile complete, inclusiv de ce lucrarea contrazisă e a coordonatorului, în
[[rals-rolcp-datele-sunt-ale-lui-nisioi]]. Revendicarea corectă e strict metodologică: nu folosim
etichete în limba țintă.

**Lecție de proces.** Cele cinci afirmații false au stat în text prin patru revizii, pentru că
verificam formularea, nu adevărul. Căutarea care le-a găsit, de rulat înainte de orice submisie:
`grep -iE "no prior|no published|first (system|to)|only .*(available|exist)|entirety|aware of no"`
peste toate fișierele de paste.

**REZOLVAT pe 30 iulie 2026: proveniența datelor.** RALS e citată, cu licența CC BY-NC-SA 4.0 și
detaliile setului (1587 de ținte, 274 de propoziții, 10 adnotatori din 80) în §3.1. Paragraful de mai
jos rămâne doar ca istoric al problemei.

**Agravat pe 27 iulie 2026, la revizia 11: setul de test a rămas fără nicio proveniență.**
Alexandru a cerut să nu se mai prezinte lucrarea ca proiect de facultate, deci a ieșit „shared-task
metric" din abstract și din introducere. Consecința: cât timp scria „shared task", cititorul înțelegea
măcar de unde vin datele; acum introducerea spune „our test set" și nimic nu mai indică sursa celor
1587 de exemple, deși ACL cere proveniența. **Nu se rezolvă prin reformulare**, e același fir cu
decizia amânată despre citarea RALS. Vezi [[rals-rolcp-datele-sunt-ale-lui-nisioi]].

**Rămas de verificat înainte de submisie:** valoarea in-source 0.569 pentru Lasso din `tab:fail` —
singura fără log salvat. `analysis_lasso.py` afișează ambele metrici. Restul coloanei e verificat, dar
atenție: `0.515` e `EN→ML`, iar `0.586`/`0.556` sunt `transfer_avg` — în raportul vechi erau amestecate.

**How to apply:** vezi [[paper-target-mrl-emnlp-2026]] pentru deadline și
[[paper-overleaf-workflow]] pentru capcanele de compilare.
