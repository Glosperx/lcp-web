---
name: selectia-modelului-b-e-pe-splitul-gresit
description: "IMPLEMENTAT 18 aug ca --pick-split: selectia pe test da 0.669591, +0.005036 cu CI care exclude zero, franceza +0.0582; neadoptat, implicitul ramane trial"
metadata:
  type: project
---

> **Cifrele de mai jos sunt pe `n = 5606`, dinainte de P11.** Sistemul e acum **0.674946 pe n = 5624**.
> Ce e mai jos ramane valabil ca rationament si ca ordine a efectelor, dar **cifrele nu se citeaza**.
> Vezi [[p11-adoptia-facuta]].


Gasit pe **19 august 2026**, in sesiunea de research care a produs
`~/.claude/plans/cite-te-claude-plans-prompt-research-urm-keen-turing.md`. Nu era in niciun tabel de
„ce ramane deschis".

`fuse_ab.py` alege modelul pentru semnalul B din tabelul de **trial**, prin
`pick_model(tab_trial, ...)` la `fuse_ab.py:200`, apelat din `load_signals` la `fuse_ab.py:147`. In
acelasi timp ponderea `w` se potriveste pe **test**, prin `--fit test`. Asimetria e exact cea pe care
docstring-ul propriu al lui `fuse_ab.py` o condamna cand motiveaza `--fit test`: „Cele doua componente
ale aceluiasi sistem foloseau splituri diferite fara motiv." Motivul a fost eliminat pentru `w` si a
ramas pentru model.

**Ce costa, din `output/e_bakeoff_test.md`, r al lui B pe franceza:** `qwen35-9b-8bit`, cel ales de
selectia pe trial, da **+0.542**; `gemma4-12b-4bit` da **+0.642**. Pierdere de **0.100 pe franceza**,
adica pe limba care explica singura tot deficitul fata de reperele publicate. Pe celelalte noua limbi
selectia alege oricum Gemma, deci reparatia atinge o singura limba.

**Magnitudinea castigului, din comparatia pereche care exista deja pe disc:**
`e_fusion_gemma4-12b-4bit_fittest_lemma.md` da 0.6634 si `e_fusion_lolo_fittest_lemma.md` da 0.6568,
**ambele cu acelasi A (0.5630), acelasi `--fit test`, aceleasi randuri**, deci +0.0066 e curat ca
ordin de marime. Nu e o predictie pentru A-ul curent.

**Reparatia e legala si costa zero inferenta:** selectia pentru limba L pe randurile de TEST ale
celorlalte 9 limbi, exact ca `w` si exact ca antrenarea bratului A. Comentariul din
`bakeoff_trial.aggregate` care spune ca „o selectie recalculata pe test ar fi tuning pe scorul
raportat" e adevarat numai pentru o selectie care foloseste testul lui L.

**Doua capcane.** Bazinul de pe test are efectiv doi candidati, fiindca `qwen35-9b-8bit` e rulat pe
test doar pe franceza; un reviewer poate spune ca s-a selectat dintre modelele care se intamplau sa
fie rulate. Si sub protocolul corect selectia degenereaza la un singur model peste tot, deci
revendicarea „LOLO inclusiv la alegerea modelului" trebuie rescrisa ca rezultat, nu stearsa.

**Coerent cu [[criteriu-plat-mediaza-nu-alege]], si o intareste:** latimea criteriului pentru alegerea
modelului pe test e 0.268 (0.642 fata de 0.374), de trei ori mai LATA decat curba lui `w` (0.0847),
deci aici regula spune corect „selecteaza", in timp ce la encodere (0.0077 fata de 0.082) spune
„mediaza". Aceeasi regula, doua verdicte opuse, ambele confirmate.

**Why:** e cel mai mare castig per ora ramas si nu costa nicio rulare de LLM, iar tinta lui e exact
limba care tine in loc comparatia cu reperele.

**How to apply:** RULAT. Tot ce urmeaza inlocuieste planul de mai sus.

## IMPLEMENTAT si MASURAT, 18 august 2026

`fuse_ab.py --pick-split {trial,test}`, **implicit `trial`**, deci tot ce e publicat reproduce fara
flag: 0.664555 exact, cu `fusion_lolo_ens.csv` si `fusion_preds_lolo_ens.csv` identice bit cu bit,
verificat cu `cmp`. `tab_trial` s-a redenumit in `tab_pick` peste tot. Selectia imbricata din
`fit_weight` si `fit_choice` foloseste acelasi tabel, iar filtrul de disponibilitate a ramas pe
splitul de evaluare.

**Cifra:** `--pick-split test` da **0.669591** fata de 0.664555, adica **+0.005036**, CI pereche
**[+0.0021, +0.0081]**, P(>0) = 100%, bootstrap pe contexte cu aceleasi randuri pe ambele brate.
Magnitudinea prezisa de +0.0066 a fost apropiata, dar nu identica, si nu era o predictie.

**Ambele porti au trecut:** harta alege Gemma pe toate cele 10 limbi, iar franceza urca de la +0.5883
la **+0.6465**, adica +0.0582 cu CI [+0.0305, +0.0869]. Trei limbi (de, fil, si) raman identice rand
cu rand. Doua coboara cu interval care exclude zero, **en −0.0028 si it −0.0035**, prin `w_src` si `w`
re-alesi pe un set de potrivire in care franceza si-a schimbat modelul.

Latimile masurate confirma cifrele prezise: criteriul de selectie **0.2677**, curba lui `w` **0.0901**,
deci de 3.0 ori mai lat.

**Nimic nu s-a adoptat.** Cifra sta pe tagul `ens_picktest`, in `output/e_pick_split.md`, generat de
`analysis_pick_split.py`. Adoptia ramane pentru evenimentul unic de renumerotare, impreuna cu media de
encodere si fixul din `find_char_span`. Atentie: `fuse_ab.py` **nu e urmarit de git** pe `alex_llm`,
deci un `git add` explicit e necesar.

**INCHIS pe 19 august 2026, prin P10.** Bazinul de pe test e acum **3 candidati din 3 pe fiecare
limba**: `qwen35-9b-8bit` a fost rulat pe toate cele 5624 de randuri, in 81.5 min la 0.87 s/item.
Costul real a depasit estimarea de ~73 min fiindca cei 0.776 s/item masurati pe franceza nu se
extrapoleaza la celelalte noua limbi. **Selectia nu s-a schimbat nicaieri** si cifra de sistem a
ramas 0.674946 exact. Marja lui Gemma la criteriul LOLO e intre +0.0448 si +0.0597 la toate cele
zece alegeri, iar `qwen35-9b-8bit` e acum locul doi peste tot, cu media B +0.591. Obiectia „am
selectat dintre modelele care se intamplau sa fie rulate" nu mai exista. Vezi
[[paper-extensie-multilingva-arr-octombrie]].

## Costuri de rulare, masurate, pentru orice estimare viitoare

Din coloana `sec` a CSV-urilor de bake-off: **trial e doar 300 de randuri per model, ~5 minute**, deci
re-rularea completa a trial-ului pe toate cele 7 modele e ~36 de minute, nu ore. Pe test:
`gemma4-12b-4bit` **102 min** pentru 5624 de randuri, `qwen3-8b-4bit` 79 min, `qwen35-9b-8bit` 7.4 min
pe cele 569 de randuri de franceza. Embedding, MASURAT pe randurile de test (`output/cost_inferenta.csv`):
`xlmr` 49.5s, `labse` 50.4s, `e5` 49.6s, `xlmr-large` 131.8s, deci patru encodere 4.7 min fata de 0.8.
**LLM-ul e peste 95% din timpul conductei**, ceea ce face obiectia de cost impotriva mediei de
encodere slaba cantitativ: conducta creste cu +4%. Vezi [[encoderul-masurat-lolo]].

## Combinata cu media de encodere: P9, rulat 19 august

Combinatia da **0.676253**, iar `--pick-split test` **adauga +0.004302 peste media de encodere**, CI
[+0.0017, +0.0070], deci cele doua parghii nu sunt redundante. Recomandarea: `--pick-split test` se
adopta necondiționat, fiind reparatie de corectitudine cu cost zero. Vezi [[combinatia-p9-masurata]].
