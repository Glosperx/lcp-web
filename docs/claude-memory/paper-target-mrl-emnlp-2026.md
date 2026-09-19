---
name: paper-target-mrl-emnlp-2026
description: "Paperul de complexitate lexicală RO țintește workshopul MRL @ EMNLP 2026, deadline 10 august 2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: d9a89e1a-84a5-41a4-a6ef-303bfbb5b38f
  modified: 2026-08-15T19:03:02.921Z
---

Paperul `Cross-Lingual Transfer for Romanian Lexical Complexity Prediction` (scris inițial ca raport
de curs unibuc/ia-cti-2026) este pregătit pentru submisie la **MRL — 6th Workshop on Multilingual
Representation Learning** (cu SIGTYP), la EMNLP 2026, Budapesta.

- Deadline submisie directă: **10 august 2026** AoE. Notificare 20 sep, camera-ready 30 sep.
- **NU S-A TRIMIS NIMIC. Confirmat de Alexandru pe 15 august 2026.** Nici lucrarea completă, nici
  abstractul non-arhival de 2 pagini din planul de pe 8 august. Nu există `abstract_mrl.tex`.
  Restul memoriei de mai jos descrie pregătirea, care a rămas nefolosită, nu o submisie făcută.
  Consecința bună: nu există publicație anterioară, deci regula ARR de suprapunere nu blochează
  submisia multilingvă din 12 octombrie. Vezi [[paper-extensie-multilingva-arr-octombrie]].
- Decis pe 23 iulie 2026 împreună cu Alexandru; alternativele cu fit bun (Insights — negative
  results, deadline 8 iunie; BlackboxNLP — 17 iulie) erau deja închise. BabyLM (15 aug) a fost
  discutat ca al doilea, dar respins: politica ACL de multiple submission interzice aceeași lucrare
  la două venue-uri cu review-uri suprapuse.
- **Recomandat long paper (8p), nu short (4p)** — măsurat la compilare: introducerea ~2.8
  coloane + Related Work ~1.6, iar figurile și tabelele existente umplu ~2 pagini (cifră
  corectată pe 27 iulie; estimarea inițială de 1.25/0.9 coloane era de peste două ori prea mică).
- Workshopul e double-blind → scos link-ul de GitHub din Conclusions.
- **Introducerea e la revizia 11** (27 iulie 2026), după unsprezece runde de review frază cu frază.
  Starea curentă: **Introduction 625 + Related Work 394 de cuvinte**, terminate pe pagina 2.
  Compilează curat: 0 erori, 0 citări nerezolvate, 0 em-dash, 0 `Overfull`. Istoricul complet al
  reviziilor e în header-ul lui `paste_intro.tex`, nu îl duplica aici. Regulile de formulare
  rezultate sunt în [[preferinte-de-scriitura-paper]]; structura cerută, în [[intro-style-hgs]].
- **Metrica oficială**, pentru când e nevoie de ea: `100 · ½(|ρ| + max(0, R²))`, media dintre
  Pearson în valoare absolută și R² clipat la 0, pe scară 0–100. Sursa e pagina task-ului,
  salvată în rădăcina repo-ului ca `Nitro AI Judge_metrica.html`, secțiunea „Evaluarea", cu tot
  cu implementarea sklearn/scipy. Formula din `paste_body.tex` e algebric identică, verificat.
  Aceeași pagină listează resursele permise (XLM-R local, LLM ≤ 8B rulat local, surprisal, liste
  de frecvențe), adică exact cele patru semnale ale noastre.
- **La revizia 8 au fost scoase cinci afirmații false** despre inexistența datelor și sistemelor
  LCP pentru română. Vezi [[rals-rolcp-datele-sunt-ale-lui-nisioi]] — e cel mai important lucru
  aflat în sesiunea din 27 iulie.
- **Preview-ul se compilează cu abstractul inclus** (`build/intro_only.tex`), altfel paginarea e
  falsă și măsurătoarea „încape în 2 pagini" ar fi greșită.
- **EMNLP 2026 main conference nu e o opțiune** (verificat pe 27 iulie 2026): e ARR-only, iar
  ciclurile care îl alimentează — martie și mai 2026 — sunt închise, și nu avem recenzii ARR de
  comitat până pe 2 august. ACL 2026 s-a ținut deja. Întrebarea „workshop sau conferință mare"
  nu se pune pentru 2026.

**Why:** alegerea workshopului dictează cum se scrie introducerea — CFP-ul MRL cere textual
*zero-/few-shot multilingual*, *transfer learning for under-studied, morphologically-rich languages*
și *analysis and probing of multilingual representations*, adică exact fix-ul de frecvență pe lemă,
sistemul fără etichete RO și analiza SHAP.

**How to apply:** orice text nou pentru paper se scrie pentru MRL și anonimizat. Detaliile complete
(deadline-uri, de ce nu celelalte workshopuri, de ce EMNLP main e închis, unde se poate merge după
MRL) sunt în `Paper/Articol_Complexity/NOTES_workshop.md`. Vezi și [[paper-overleaf-workflow]] și
[[paper-slabiciuni-de-reviewer]].

**Ce urmează după MRL — DECIS pe 8 august 2026, vezi
[[paper-extensie-multilingva-arr-octombrie]].** Extensie la 11 limbi, submisie ARR pe **12 oct
2026** (ciclul octombrie), de unde se comite la NAACL 2027 / COLING 2027 (20 dec) sau ACL 2027
(ianuarie). EACL 2027 confirmat închis. Publicarea la MRL nu arde lucrarea, dar versiunea de
conferință trebuie să fie o extindere reală — experimente noi, nu reformatare.
