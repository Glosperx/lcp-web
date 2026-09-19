---
name: atribuirea-cere-doua-masuri
description: "Regula transversala: importanta trasaturilor nu se raporteaza cu o singura masura; pe datele noastre permutarea da lui zipf de 2.5 ori mai mult decat reantrenarea, si SHAP inverseaza ordinea fata de permutare"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df3472df-2d54-4cc5-a11a-fc31f9833de3
  modified: 2026-08-23T17:16:52.030Z
---

Masurat **23 august 2026** in `analysis_shap_multi.py` -> `output/e_shap_multi.md`, dar regula e
generala si se aplica oriunde apare un tabel de importanta.

## Regula

**Nicio propozitie de forma "trasatura X conteaza de N ori mai mult decat Y" nu se scrie pe baza unei
singure masuri de importanta.** Se raporteaza cel putin doua, iar cand difera, dezacordul E observatia.

## Cifrele proprii, acelasi model si aceleasi date

Surogat lexical care prezice `p_fuz`, per limba:

    masura                zipf     nsub     length
    permutare marginala  +0.7472  +0.0570  +0.0300
    reantrenare fara ea  +0.2942  +0.0367  +0.0167

Factor **2.5** pe `zipf`. Si artefactul vechi de pe disc arata acelasi tip de dezacord in cealalta
directie, intre permutare si SHAP: `output/shap/feature_importance.txt` pune `zipf` 0.4536 peste
`embedding(768)` 0.1433 prin permutare, iar SHAP le **inverseaza**, 0.068 fata de 0.182.

## De ce, si e in literatura

- **Hooker, Mentch si Zhou, Statistics and Computing 2021, 31:82.** Permutarea nerestrictionata rupe
  dependentele si **forteaza modelul sa extrapoleze in regiuni fara date**, ceea ce supraestimeaza
  trasaturile corelate. Recomandarea lor e in titlu: importanta corecta cere **inca un model**, adica
  reantrenare fara trasatura.
- **Aas, Jullum si Loland, Artificial Intelligence 2021, 298:103502.** Kernel SHAP presupune
  independenta trasaturilor si poate da explicatii foarte gresite cand nu e cazul.

Deci SHAP si permutarea sunt **doi membri ai aceleiasi familii** (amandoua marginale), nu doua puncte
de vedere. Al doilea punct de vedere real e reantrenarea.

**How to apply:** `shap` nu e instalat in `envs/ml_def` si nu merita instalat pentru o figura;
reantrenarea fara coloana e mai ieftina de argumentat si e chiar ce recomanda literatura. Costul ei e
un model in plus per coloana, ceea ce la 6-10 trasaturi si HGB inseamna secunde.

Vezi [[cod-nou-al-treilea-semnal]] si [[criteriu-plat-mediaza-nu-alege]].
