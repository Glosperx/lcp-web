---
name: nisioi-fir-monolingv-lolo
description: Firul din 20 august cu Nisioi despre encodere monolingve vs LOLO, ce s-a răspuns și oferta rămasă deschisă de a rula monolingv pe japoneză
metadata:
  node_type: memory
  type: project
---

Discuție pe WhatsApp, **20 august 2026**, pornită de la cum se obține embeddingul unui cuvânt. Nisioi a
pus patru întrebări: nu ar merge mai bine modele preantrenate pe limba respectivă (RoBERT pe română);
dacă folosim XLM-R antrenăm de fapt pe toate limbile; LOLO pare o variantă doar pentru XLM-R; antrenăm
și monolingv.

## Ce s-a răspuns, verificat în cod

- Encoder multilingv **înghețat**, cap Ridge+HGB antrenat pe CompLex EN plus MLSP fără limba L.
  Pentru franceză: 8422 + 5040 = 13462 rânduri, prezice 566. **11 potriviri, nu 20**: 10 pentru brațul
  multilingv, una pentru EN-only, care nu depinde de L.
- **LOLO nu e legat de XLM-R.** Toate cele patru encodere au trecut prin același LOLO, cu fișiere de
  predicții sufixate pe encoder. r mediu pe brațul A: xlmr 0.5778, xlmr-large 0.5834, labse 0.5780,
  e5 0.5751. LOLO cere doar un spațiu comun, ceea ce LaBSE și e5 îndeplinesc.
- **Monolingv nu s-a antrenat niciodată, nicăieri.** Singurul in-language e `_cv_r`
  ([solution_bert.py:720](solution_bert.py#L720)), folosit ca diagnostic, cu `cv_ml` pe MLSP *pooled*,
  nu per limbă.
- Argumentul corect pentru de ce monolingv nu încape, formulat pentru el: Ridge învață coeficienți
  **în baza encoderului**, deci un spațiu monolingv face imposibil împrumutul de etichete din alte
  limbi. Nu e „BERT are nevoie de labels", și XLM-R are. Detaliul tehnic era deja în
  [[lolo-exista-deja-in-cod]] („configurația (ii) nu e definibilă pentru semnalul A").
- Cifrele care îi susțin intuiția: ja Δ = −0.0896 cu CI care exclude zero; si LaBSE 0.3613 față de e5
  0.2090; fr xlmr-large +0.0412. Plus capcana de selecție, din [[encoderul-masurat-lolo]]: alegerea per
  limbă pierde −0.0050, medierea câștigă +0.0070 și atinge plafonul oracol.

## Rămas deschis

**Oferta făcută explicit: rulez un encoder monolingv, și locul cel mai informativ e japoneza**, nu
româna, pentru că acolo Δ negativ spune deja că mai puțin multilingvism ar fi mai bine. Iese din
protocolul zero-label, deci s-ar raporta separat. Nu s-a rulat.

Două variante distincte, de nu confundat dacă se rulează: (a) același XLM-R, cap antrenat pe etichetele
limbii, care măsoară strict valoarea etichetelor in-language; (b) encoder monolingv plus cap in-language,
care schimbă două lucruri deodată. MLSP nu are split de antrenare per limbă, deci obligatoriu CV în
interiorul a 445-600 de rânduri.

## Corecții făcute în draftul lui, de reținut ca tipar

Alexandru scrie el răspunsurile și cere verificarea lor. Două erori au apărut de două ori: exemplul cu
engleza (vezi [[engleza-nu-e-zero-label]], e singura limbă unde afirmația nu se ține) și confuzia
„BERT are nevoie de date etichetate, XLM-R nu". A treia: la schimbarea exemplului din engleză în
franceză, finalul propoziției a rămas pe engleză.

**How to apply:** la orice draft de răspuns către Nisioi, verifică întâi dacă exemplul e engleza, apoi
dacă afirmația confundă „supervizat" cu „in-language". Vezi și
[[raspunsuri-fara-diacritice-fara-tabele-md]] pentru forma textului.
