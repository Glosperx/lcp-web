---
name: constante-hardcodate-mint-dupa-renumerotare
description: "Dupa o renumerotare, orice cifra de referinta hardcodata intr-un script de raport devine o minciuna TACUTA; raportul iese inconsistent cu el insusi fara nicio eroare"
metadata:
  type: feedback
---

Descoperit **19 august 2026**, dupa P11, in `analysis_encoder.py`.

Scriptul avea `SIS = 0.664555` hardcodat in trei locuri. Cand `n` s-a schimbat de la 5606 la 5624,
**restul raportului s-a recalculat si constanta a ramas**, deci `output/e_encoder.md` a iesit
contrazicandu-se singur: un tabel spunea 0.664581, altul 0.664555, si niciun mesaj de eroare.
**Asta e mai rau decat un raport complet invechit**, fiindca invechitul se vede, iar inconsistentul
se citeste ca adevarat.

Acelasi fisier avea a doua forma a aceleiasi probleme: citea tagurile `ens_enc` si `ens_encmean`,
adica fisiere ramase pe `n` vechi, in timp ce restul citea fisierele noi. Amestecul a produs un tabel
cu jumatate din randuri pe 5606 si jumatate pe 5624.

**Why:** intr-un proiect unde cifra de sistem se schimba la fiecare adoptie, orice referinta scrisa
in cod expira fara sa spuna. Cifra trebuie CITITA de pe disc, iar `n` trebuie verificat, nu presupus.

**How to apply:** cand se schimba `n` sau cifra de sistem, cauta in scripturile de raport, in ordinea
asta:
1. constante numerice care sunt cifre de referinta (`SIS = ...`, praguri, marje), si inlocuieste-le
   cu o citire de pe disc;
2. nume de fisiere sau taguri scrise in cod, care pot arata catre artefacte pe `n` vechi;
3. dupa regenerare, verifica un numar care apare in DOUA locuri din acelasi raport, ca sa prinzi
   inconsistenta interna.

Reparat prin `_sistem()` in `analysis_encoder.py`, care citeste `fusion_lolo_ens.csv`. Aceeasi
protectie e in `analysis_audit_jurnal.py`, care acum distinge artefactele pe `n` vechi de cele lipsa,
si in `make_rezumat_modele.py`, care filtreaza fuziunile la `n` curent.

Vezi [[p11-adoptia-facuta]] si [[bifurcatii-de-declarat]].
