---
name: preferinte-de-scriitura-paper
description: "Regulile de scriitură pe care le cere Alexandru la textul paperului: fără em-dash, fără definiții de dicționar, fără repetiții, maximum 2 pagini intro+related work"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 22f6ea41-f9db-4e9e-aac2-9a0b5065c375
  modified: 2026-07-27T16:46:44.908Z
---

Stabilite la reviziile 4–9 ale introducerii, pe 27 iulie 2026, prin respingeri succesive.

**Fără em-dash, nicăieri.** Nici `---`, nici caracterul Unicode. Se înlocuiește cu virgulă, punct și
virgulă, două puncte sau reformulare. `paste_intro.tex` e curat; `paste_body.tex` și
`paste_limitations.tex` **încă nu sunt**.

**Fără deschideri de tip definiție de dicționar.** „Lexical complexity prediction (LCP) is the task
of estimating…" a fost respinsă cu „se vede că nu e scrisă de om".

**Fără aforisme și figuri de stil** — Alexandru le numește „vrăjeală". Respinse pe rând: „Text is only
as accessible as its hardest words", „Whether a text can be read by the audience it was written
for…" (prea multe subordonate), „Children, language learners, and readers with limited literacy…"
(nu vrea să înceapă cu copii). A căzut și formularea „The systems built to help them".

Deschiderea acceptată pornește de la o afirmație concretă despre vocabular, apoi cine e afectat, apoi
numele sarcinii, apoi ce permite.

**Maximum 2 pagini pentru Introduction + Related Work împreună**, cu RALS ca reper. Măsurat cu
abstractul inclus în build, altfel paginarea e falsă.

**Nicio idee spusă de două ori.** Formularea lui: „nu mă interesează să fie mult scris care repetă
aceeași idee și nu spune nimic nou". Verificare utilă: dacă o citare apare în două paragrafe
diferite, aproape sigur e o repetiție. La revizia 9, toate cele 10 citări recurente apăreau de 2–3
ori; textul a scăzut de la 1.466 la 1.024 de cuvinte fără să piardă nicio idee.

**Layout, ca în RALS:** fără listă cu buline la contribuții, care devin un paragraf narativ cu
First/Second/Third/Fourth, și fără subsecțiuni numerotate în Related Work, doar `\paragraph{}`.
Contribuțiile rămân la persoana I („We combine", „We introduce", „We show", „We report").

**Papere-model, cu roluri diferite:**

| Fișier / lucrare | Pentru ce |
|---|---|
| `2605.07466_6048.pdf` (Anghel et al., fatty pancreas) | retorică, structura contribuțiilor |
| Kuvshynova et al., ETRA 2026 | mișcarea primului paragraf |
| RALS (`arxiv.org/abs/2607.20078`) | lungime și layout |

Atenție, **modelele se contrazic**: ETRA are subsecțiuni în Related Work, RALS nu. Când se ciocnesc,
întreabă.

**Adăugate la reviziile 10–11, pe 27 iulie 2026.**

**Fără „the system" ca desemnare a lucrării noastre.** Interzis explicit. Se înlocuiește cu ce e
concret: „a single predictor", „it", „the largest single gain we measure". „Nearly every LCP system
is built the same way" rămâne, acolo desemnează sistemele altora.

**Nu se prezintă ca proiect de facultate, ci ca lucrare de workshop.** „shared-task metric" a fost
respins pentru asta: încadrează lucrarea ca sarcină primită și rezolvată. Evaluarea se prezintă ca a
noastră, pe setul nostru („on our test set, under a metric that combines Pearson correlation with
$R^2$"). Consecință semnalată, netratată: `paste_body.tex` și `paste_limitations.tex` mai au 16
apariții de „shared task", „leaderboard", „submission". Atenție, cele din Limitations sunt
**portante**: divulgarea că cele cinci cantități au fost alese pe scorul public depinde de numirea
leaderboardului. Alea se reîncadrează, nu se șterg.

**Fără formule în introducere.** Varianta „$50(|r| + \max(0, R^2))$" a fost respinsă: iese din
registrul high level cerut de ghid la paragraful de contribuții. Formulele au locul lor în Approach.

**În contribuții, revendicarea plus cel mult cifra de titlu.** Cifrele de sprijin (`r = 0.07`,
`0.461/0.462/0.515 in-source`, `41.76`) au fost scoase din introducere: la pagina 1 nu pot fi
interpretate. Dovada e treaba secțiunii de rezultate.

**Nu adăuga nimic nececut.** Tiparul care a costat cele mai multe runde: „out of 100" pus ca să facă
`69.74` interpretabil, când cerința era doar să fie numită metrica. Fă exact ce s-a cerut, semnalează
separat ce crezi că mai lipsește.

**Why:** Alexandru revizuiește frază cu frază și respinge rapid tot ce sună generat. Ghicitul costă
runde întregi; la prima frază am greșit de trei ori, iar la fraza cu metrica de patru ori la rând,
fiecare dată pentru că am adăugat ceva peste ce s-a cerut.

**How to apply:** la orice text nou pentru paper, aplică regulile astea din start. Vezi și
[[intro-style-hgs]] pentru structura cerută de coordonator și [[paper-overleaf-workflow]].
