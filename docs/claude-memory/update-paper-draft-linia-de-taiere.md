---
name: update-paper-draft-linia-de-taiere
description: "output/update_paper_draft.txt e explicatia in romana pe care Alexandru o corecteaza de mana de sus in jos; iti spune linia pana unde a ajuns si deasupra ei nu se atinge nimic, iar el editeaza in paralel"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c91d735-9e68-4319-b624-a2bf6fc90cbf
  modified: 2026-08-19T13:40:22.381Z
---

Constatat pe **19 august 2026**, in sesiunea P10.

`output/update_paper_draft.txt` e documentul in care Alexandru explica sistemul in limba romana,
pe intelesul cuiva care nu citeste cod: ce e semnalul A, ce e B, ce repere exista. Nu e generat de
niciun script si nu e lucrarea.

## Regula de lucru, data explicit

El il corecteaza **de sus in jos** si iti spune pana la ce linie a ajuns, citand pasajul. **Deasupra
liniei aleia nu se atinge nimic**, nici macar un `[]` lasat gol care evident cere o cifra. Daca
lipseste o cifra acolo, i-o dai in chat si o pune el.

**Editeaza fisierul in paralel cu tine.** In sesiunea P10 a completat singur un `[]` si a rescris un
paragraf cat rulau editarile mele. Deci:

- reciteste fisierul de pe disc **imediat inainte** de fiecare scriere, niciodata dintr-o copie tinuta
  in context;
- verifica programatic ca fiecare inlocuire cade **sub** linia de taiere, si nu scrie nimic daca una
  nu cade (asta a si prins ca pozitiile se mutasera);
- tine o copie de siguranta si compara la final cu `difflib`, ca sa poti arata exact ce linii ai
  atins si care sunt ale lui.

## Ce se repara acolo, de fapt

Documentul ramane in urma tacut dupa fiecare renumerotare, fiindca descrie sistemul in cuvinte si
nimic nu-l verifica. La P10 avea harta model-per-limba fixata pe trial, desi sistemul foloseste
`--pick-split test` de la P11, si atribuia „Qwen3.5 pe franceza" cifrei de 0.674946. Cand il atingi,
verifica fiecare cifra contra `output/`, nu contra unei sesiuni vechi.

**Why:** e singurul document al proiectului scris ca sa fie citit de un om, deci o cifra gresita acolo
ajunge intr-o discutie, nu intr-un log.

**How to apply:** intreaba pana unde a corectat daca nu ti-a spus, si trateaza raspunsul ca pe o
granita, nu ca pe o sugestie. Vezi [[preferinte-de-scriitura-paper]] si
[[constante-hardcodate-mint-dupa-renumerotare]].

## Actualizare, sesiune ulterioara: exact acelasi tipar de staleness s-a repetat

Documentul a ajuns din nou sa descrie gresit mecanismul (de data asta atribuia scorul mai mare al
lui Gemma pe franceza unei "reparari de bug", cand de fapt era descrierea corecta a parghiei
`--pick-split test` deja adoptate). Corectat impreuna cu Alexandru, verificat linie cu linie contra
codului inainte de a confirma. Cifrele si mecanismele finale, verificate, sunt acum in
[[update-paper-draft-semnale-a-b]]. Tiparul se repeta: la fiecare renumerotare, reciteste documentul
contra codului curent, nu presupune ca proza veche mai descrie sistemul curent.
