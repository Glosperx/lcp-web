---
name: cerere-sesiune-al-treilea-semnal
description: "INCHISA 23 aug 2026 seara: sesiunea s-a facut, raspunsul e NU; punctul de reluare e in al3lea-semnal-ce-ramane-deschis"
metadata:
  type: project
---

Cerut pe **23 august 2026**, la finalul sesiunii pe semnalul A. Continutul cerut, in cuvintele lui:

- daca se mai poate pune **inca un semnal** pe langa cel cu encoderele (A) si nota de complexitate de
  la LLM (B);
- **surprisal-ul** de la LLM a mai fost testat si poate ajuta (vezi [[semnalul-c-surprisal-stare]]);
- **eye-tracking-ul e stabilit ca nu ajuta**, nu se reia (vezi [[eye-tracking-cat-a-adus-in-r]]);
- analiza cu **SHAP** si o privire pe **distributia t-SNE / UMAP**, ca sa se vada daca se mai poate
  pune un semnal;
- **gandit pas cu pas**, ca sesiunea precedenta;
- **cautare in paper-uri deja publicate, NU neaparat despre complexitatea cuvintelor.**

Promptul complet pentru sesiune a fost scris si i-a fost dat in chat pe 23 august. Protocolul ramane
cel din [[transmisia-a-fuziune-masurata]]: bara +0.0045, interval pereche fata de 0.683849, nicio
limba stricata cu CI care exclude zero, totul LOLO, validare pe limba nu pe medie.

---

## INCHISA, 23 august 2026 seara

Sesiunea s-a facut cap la cap. **Raspunsul e NU**, cu treisprezece candidati masurati prin poarta si
sapte prin fuziune. Fiecare punct al cererii are un raspuns:

- **surprisal**: inchis definitiv, [[semnalul-c-surprisal-stare]]. Si coloana lui gemma s-a dovedit
  degenerata, [[gemma-nu-poate-da-surprisal]].
- **SHAP pe multilingv**: refacut, dar cu reantrenare in loc de SHAP, si dezacordul dintre masuri a
  devenit el insusi rezultatul, [[atribuirea-cere-doua-masuri]].
- **t-SNE / UMAP**: **NU s-au rulat**, conform criteriului scris inainte, fiindca pasul numeric a iesit
  negativ. Nu e o omisiune, e decizia.
- **literatura din afara domeniului**: `output/e_literatura_al3lea.md`, sapte teme cu referinte, cifre
  si coloana "ce nu se transfera".
- **gandit pas cu pas**: planul a fost scris si aprobat inainte de prima rulare.

Punctul de reluare: [[al3lea-semnal-ce-ramane-deschis]].
