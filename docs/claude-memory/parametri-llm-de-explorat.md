---
name: parametri-llm-de-explorat
description: Agenda cerută pe 20 aug pentru o sesiune viitoare de explorare: ce parametri ai LLM-ului nu au fost incercati inca, in ce ordine, si de ce screening-ul se face pe trial.
metadata:
  type: project
---

Alexandru a cerut pe 20 august 2026 o sesiune separata de explorare pe **ce alti parametri ai
LLM-ului ar mai putea urca scorul**. Punctul de plecare e sistemul de 0.683849 din
[[distributia-b-temperatura]].

**Protocolul de screening, si e cheia intregii sesiuni.** Pe test o configuratie costa ~102 minute;
pe trial costa ~5.5 minute. Deci se cerne pe TRIAL, si numai castigatorul se confirma pe test. Are
acoperire in [[decalaj-trial-test-masurat]]: cifrele de trial nu sunt predictii, dar ORDINEA
supravietuieste, si pentru cernere ordinea e destul. Intr-o ora se pot incerca zece configuratii.

**Gratis, pe fisierele deja pe disc, fara nicio inferenta:**
1. ponderea intre cele doua prompturi, aleasa LOLO. Media 50/50 e demonstrat gresita: promptul 2
   singur da 0.6536 la T-ul lui, promptul 1 doar 0.6256, iar promptul 1 vrea T dublu.
2. combinarea prin produs, adica media geometrica a celor doua distributii renormalizata, in loc de
   media valorilor asteptate. Foloseste automat dezacordul, singurul semnal care a supravietuit
   controlului flexibil.

**Cer inferenta noua, ~5.5 min per configuratie pe trial:**
3. **scara de raspuns.** Acum e 1-5, deci soft-read-ul are cinci atomi si rezolutia e plafonata
   acolo. Eticheta e continua. De incercat 0-9, sau doua pozitii de cifra pentru 0-99. E parametrul
   cel mai putin explorat si cel mai ieftin de schimbat.
4. **pozitia de citire.** Acum e ultima pozitie a sablonului de chat. De incercat un prefix fortat
   („Rating:") dupa care distributia peste cifre e mai curata.
5. **few-shot din CELELALTE limbi.** Pastreaza revendicarea „zero etichete in limba tinta" si ar fi
   diferenta reala fata de G-Eval, care e 3-shot in limba tinta. Vezi
   [[noutate-si-precedente-lcp-multilingv]].
6. **cuantizare 8 biti pentru Gemma.** E.4 a masurat costul cuantizarii doar pe perechile Qwen;
   bratul principal e 4-bit QAT si n-a fost controlat.
7. prompturi 3 si 4, decorelate. Vezi [[prompt-ansamblu-decorelat]]: parghia e ansamblul, nu promptul
   singur.

**Structurale, nu parametri:** al treilea termen in fuziune pentru dezacord (cere schimbare in
`fuse_ab.fit_choice`, care are azi o singura pondere), si distributia intreaga ca trasaturi in bratul
A. Amandoua schimba arhitectura, deci nu intra intr-o sesiune de explorare de parametri.

**Regula care ramane in picioare peste tot:** nimic nu devine sistem fara interval PERECHE fata de
configuratia curenta care exclude zero, si orice hiperparametru se alege LOLO. Vezi
[[bifurcatii-de-declarat]] pentru ce se declara cand se aleg configuratii uitandu-se la test.

## RULATA pe 21 august 2026

Vezi [[prioritizarea-parghiilor-masurata]] pentru cifre. Starea fiecarui punct de mai sus:

- 1 (ponderea intre prompturi): **inchis**, +0.00048, CI include zero, si redundant cu unirea cifrelor.
- 2 (combinarea prin produs): **inchis**, -0.00031. Puterea si produsul comuta, deci cere T propriu.
- 3 (scara de raspuns): **inchis**, sondaj rulat pe trial, -0.0099, semn negativ pe toate contrastele.
  0-9 e singura scara de zece atomi citibila; 1-10 e imposibila.
- 4 (pozitia de citire): **INCHIS pe 21 aug**, trei prefixe pe trial, toate negative, -0.0147
  pana la -0.0166, doua din trei intervale includ zero. Vezi [[pozitia-de-citire-masurata]]:
  prefixul lasa CAPUL distributiei intact si strica COADA, de unde scoate temperatura, deci T*
  cade de la 8 la 2-3. Prefixul trebuie sa se termine cu spatiu, altfel D.4 pica.
- 5 (few-shot din celelalte limbi): **NU era netestat.** `prompt_lab.lolo_shots` ia exemplele numai
  din celelalte limbi, deci varianta `v3_fewshot` din E.10 ESTE chiar asta, si e deja rulata pe trial:
  **+0.697 pe Gemma, fata de +0.686 al lui `e2_ansamblu`, care e semnalul B de acum**. Cea mai buna
  varianta individuala pe Gemma. Ce a rams nu e o incercare pe trial de 5.5 min, e **rularea pe test,
  2.44 s per item deci ~3.8 ore**, plus trecerea prin fuziune. De rulat ca **configuratie FIXA pe toate
  limbile**, nu prin selectie LOLO peste variante: selectia peste variante a pierdut (+0.6808 fata de
  +0.6860), varianta fixa nu are penalizarea aia. **RULAT pe 21 aug, in 1.6 ore si nu 3.8, si
  few-shot SINGUR PIERDE pe test: -0.0123, cu cinci limbi stricate.** Ce trece bara e ansamblul de
  TREI prompturi (few-shot plus cele doua de acum) plus unirea cifrelor: **0.688506**, +0.004642.
  Vezi [[fewshot-pe-test-masurat]].
- 6 (cuantizare 8 biti): rams, control de confound, nu parghie.
- 7 (prompturi 3 si 4): rams ultimul, e10 a masurat deja de ce nu.
- structurale: al treilea termen pentru dezacord **inchis** (excedent peste zgomot sub prag);
  distributia intreaga ca trasaturi **inchisa** (citirea optima LOLO e sub B).

Gasit peste lista, si e singurul castig al sesiunii de pe 21 aug dimineata: **unirea cifrelor
vecine**, 0.685530. Sesiunea de seara a mai gasit unul, mai mare si aditiv cu el: **ansamblul de
trei prompturi**, care duce totul la 0.688506. Lista de mai sus e acum goala in afara de 6 si 7.

## AGENDA E EXECUTATA, 22 august 2026

Toate cele cinci directii au fost duse pana la capat. Raport de sinteza: `output/e_research.md`.
Niciuna nu bate bara de +0.0045.

1. **Prompturi structural decorelate** - cinci candidati cernuti pe trial, `frecventa` trece portile si
   CADE pe test cu -0.0024. Vezi [[prompturi-decorelate-cernute]].
2. **Calibrare monotona a lui B** - inchisa, podeaua de zgomot mananca tot. Vezi
   [[calibrarea-monotona-inchisa]].
3. **Model mai mare ca B** - declinat de Alexandru ca solutie ne-inginereasca, cu costul verificat si
   scris in raport.
4. **Pondere per item in fuziune** - inchisa, `a = 0` ales pe 10/10 si pe zgomot. Vezi
   [[ponderea-per-item-inchisa]].
5. **Cuantizare 8 biti** - BLOCATA: analogul de 8 biti al checkpoint-ului sistemului nu exista. OptiQ,
   singura reimpachetare numai-text a lui Gemma 4 12B, exista doar la 4 biti; toate variantele de 8
   biti sunt multimodale si `load_weights` le respinge cu 11 tensori `vision_embedder.*` in plus.

**Lista e goala.** Ce a rams deschis nu e o parghie, ci o decizie: vezi ultimul paragraf din
`output/e_research.md` §5.
