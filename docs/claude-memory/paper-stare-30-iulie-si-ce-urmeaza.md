---
name: paper-stare-30-iulie-si-ce-urmeaza
description: Unde a rămas paperul pe 30 iulie 2026 (r/R² scrise în text) și cele două lucruri rămase de rezolvat înainte de deadline-ul din 10 august
metadata: 
  node_type: memory
  type: project
  originSessionId: 6df5edc7-10be-4071-bfae-d4dea4467d43
  modified: 2026-07-30T11:05:12.543Z
---

Punct de reluare pentru o sesiune nouă.

## Starea

`Paper/Articol_Complexity/paper_full_copy-paste.tex`, generat din `paper_full.tex`. **8 pagini**
compilate curat: 0 erori, 0 citări nerezolvate, 0 `??`, 0 overfull hbox.

Structura: 1 Introduction, 2 Related Work, 3 Approach (3.5 What was tuned), 4 Results, 5 What Did Not
Work, 6 Conclusions, Limitations. **Fără Acknowledgments, fără apendice.** Titlul e pus, `\author{}`
e gol, anonimizarea o face template-ul.

Sesiunea din 30 iulie, a doua trecere: `r` și `R²` pe RoLCP (0.777/0.603) sunt acum **scrise în
text**, în trei locuri (§2, §3.1, §4.1), lângă baseline-ul RALS `0.71 ± 0.05`. Detaliu complet și
formulările exacte în [[r-si-r2-masurate-pe-rolcp]]. Două paragrafe din Limitations, devenite
false, șterse.

## Ce a rămas de rezolvat

1. **`tab:fail`, rândul Lasso, in-source `0.569`.** Singura valoare fără log salvat.
   `analysis_lasso.py` afișează ambele metrici, o rulare confirmă dacă e `transfer_avg` sau `EN→ML`.
2. **Kuvshynova et al. 2026 (ETRA)**, tot necitată. Combină RoLCP cu eye-tracking românesc
   MultiplEYE, adică exact unghiul nostru.

Rezolvate: întrebarea despre `r`/`R²` (scrise, cu grijă la formulare — cine a citit etichetele și
când), diferența 68.99 vs 69.74 (investigată exhaustiv, rămâne neexplicată **deliberat** nescrisă
în text, vezi [[r-si-r2-masurate-pe-rolcp]]).

Înainte de submisie mai rămân: titlul e pus dar autorii trebuie completați la camera-ready,
Acknowledgments repus atunci, și opțiunea `review` scoasă.

## Unde e istoricul

**Blocul de comentariu din capul lui `paper_full.tex`** e sursa de adevăr pentru decizii: opt abateri
de la template, fiecare cu motivul și cu regula din `formatting.md` la care se supune, plus lista de
dinainte de submisie cu cifrele din punctul 1 transcrise. `README_paste.md` are aceeași informație în
formă de documentație. Scripturile sunt în repo, nu în scratchpad: `score_rolcp.py` la rădăcină și
`Paper/Articol_Complexity/make_copypaste.py`.

**Why:** deciziile din sesiunea asta au fost multe și interdependente, iar câteva au fost luate
împotriva primului meu instinct, corect. Fără notele din fișier, o sesiune nouă le-ar reface prost.

**How to apply:** citește blocul din capul lui `paper_full.tex` înainte de a atinge textul. Vezi
[[paper-overleaf-workflow]] pentru cum se regenerează fișierul de Overleaf,
[[preferinte-de-scriitura-paper]] pentru reguli de stil, [[paper-slabiciuni-de-reviewer]] pentru ce
s-a scos și de ce.
