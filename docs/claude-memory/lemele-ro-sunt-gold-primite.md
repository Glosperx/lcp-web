---
name: lemele-ro-sunt-gold-primite
description: "Coloana lemma din test_set.csv vine gata de la organizatori; PARȚIAL REZOLVAT 18 aug, stanza lematizează acum celelalte 8 limbi, dar ablația de relematizare a românei rămâne nefăcută"
metadata: 
  node_type: memory
  type: project
  originSessionId: e08431aa-2ae9-4ac3-9cca-3fb270ef6022
  modified: 2026-08-16T05:54:44.986Z
---

**ACTUALIZAT 18 august 2026.** `stanza` 1.14 e instalat, modelele pentru 8 limbi sunt jos (1.4 GB), iar
`lemmatize_mlsp.py` produce lemele pentru MLSP plus CompLex EN. Teza morfologică e măsurată, cu
rezultat pozitiv, în [[fixul-de-lema-multilingv-masurat]]. **Confoundul descris mai jos NU atinge acel
tabel**, fiindcă româna nu e printre cele 10 limbi MLSP: toate cifrele de acolo sunt pe leme prezise.
Confoundul redevine activ în clipa în care +4.09 al românei se pune pe aceeași axă cu ele, iar
reparația cerută mai jos, relematizarea automată a românei, **e în continuare nefăcută**.

Verificat pe **16 august 2026**, prin căutare pe tot repo-ul.

Fix-ul de frecvență pe lemă e cel mai mare câștig unic al lucrării, **+4.09 din 69.74**. Mecanismul
lui depinde de o coloană `lemma` care **nu e calculată de proiect, ci primită**.

- Zero apariții de `stanza`, `udpipe`, `simplemma`, `MeCab` în tot repo-ul. *(Depășit: `stanza` a fost instalat pe 18 august, dar numai pentru cele 8 limbi MLSP, nu pentru română.)*
- Singura apariție de spaCy, `analysis_features.py:39`, e explicit
  `spacy.load("ro_core_news_sm", disable=["lemmatizer"])`.
- Coloana `lemma` există gata în `data/test_set.csv` (`text, token, text_name, lemma, datapointID`)
  și în `data/labeled_examples.csv`.
- Calitate verificată pe cele 1587 de rânduri: 67,9% dintre leme diferă de token, cu diacritice
  corecte și cazuri grele rezolvate bine (`trebuie` la `trebui`, `disprețuirea` la `disprețuire`).
  Sunt leme curatoriate, nu produse de un lematizator rulat de noi.

## De ce contează pentru extensia multilingvă

Contribuția 3 din planul multilingv, „câștigul fix-ului de lemă scalează cu bogăția morfologică", se
măsoară comparând câștigul între limbi. Dar româna ar fi singura cu leme gold; orice altă limbă
primește leme prezise, cu rata lor de eroare.

**Direcția confoundului e exact cea proastă.** Leme greșite dau căutări de frecvență greșite, deci
câștig mai mic. Româna, cu leme perfecte, ar arăta cel mai mare câștig. Iar teza prezice tot româna
ca având cel mai mare câștig, fiind cea mai flexionată. **Confoundul și ipoteza prezic același
rezultat**, deci un rezultat pozitiv nu distinge între ele, iar contribuția pică la primul reviewer
care observă.

**Reparația, obligatorie și absentă din orice plan:** româna se **relematizează automat** cu același
lematizator ca restul, iar teza se măsoară pe leme prezise peste tot. Lemele gold rămân doar ca
sus-limită, într-o ablație separată care măsoară cât din +4.09 se pierde din cauza lematizatorului.
Ablația aia e un rezultat în sine, iar româna e singura limbă unde se poate face, având ambele
variante.

Notă: `Paper/documentation_overleaf.tex` nu spune nicăieri de unde vin lemele. Linia 827 introduce
`max(zipf(form), zipf(lemma))` fără proveniență, iar Limitations la linia 1159 cere „a frequency list
with lemma coverage" fără să menționeze că lematizarea a fost primită. E o gaură de reproductibilitate
în textul existent.

**Why:** e singura constatare care invalidează o contribuție declarată, nu doar o complică.

**How to apply:** înainte de a planifica orice despre teza morfologică, planifică relematizarea
românei. Vezi [[lolo-exista-deja-in-cod]] și [[paper-extensie-multilingva-arr-octombrie]]. Raportul
complet de fezabilitate:
`~/.claude/plans/cite-te-claude-plans-e-ti-pe-proiectul-d-delegated-glade.md`.
