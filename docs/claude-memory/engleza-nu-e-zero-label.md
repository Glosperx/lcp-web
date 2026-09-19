---
name: engleza-nu-e-zero-label
description: Sub LOLO, CompLex EN rămâne în antrenare și când limba evaluată e engleza, deci pentru engleza proprietatea zero-label nu se ține
metadata:
  node_type: memory
  type: project
---

Observat pe **20 august 2026**, la explicarea protocolului pentru Nisioi. Nu era scris nicăieri.

Bucla LOLO, [finetune_xlmr.py:359-363](finetune_xlmr.py#L359-L363):

```python
te = (lang == L); tr = ~te
Xtr = np.vstack([Xen, Xml[tr]])
```

`Xen` e CompLex engleză și **nu depinde de L**. Deci la `L = "en"` se scot doar cele 570 de rânduri
englezești din MLSP, iar cele **8422 de rânduri etichetate din CompLex rămân în antrenare**.

Mărimea, ca să nu fie tratată ca detaliu: pentru orice limbă, CompLex EN e **8422 din 13462 de rânduri
de antrenare, adică 63%**, cel mai mare bloc unic. Pentru engleză asta înseamnă 63% etichete în limba
țintă.

Se vede în cifre, `output/e1_lolo_frozen.csv`: engleza are cel mai mare `r_multi` din tot tabelul,
0.8197, și **Δ = −0.0024**, adică adăugarea celorlalte nouă limbi nu mai aduce nimic peste 8422 de
etichete englezești. Δ-ul aproape nul la engleză nu e un rezultat despre transfer, e un artefact al
protocolului.

Pentru celelalte nouă limbi proprietatea e curată.

**Why:** revendicarea „fără etichete în limba țintă" din extensia multilingvă e falsă exact pe o limbă
din zece, iar engleza e prima pe care s-ar uita un reviewer, fiind și linia cu cel mai bun r. Formularea
corectă e „fără etichete în limba țintă, cu excepția englezei, unde CompLex rămâne în antrenare".

**How to apply:** de declarat explicit înainte de submisie, în același loc unde se declară setarea
transductivă din [[lolo-exista-deja-in-cod]]. Nu se repară prin cod: scoaterea lui CompLex la `L = "en"`
ar schimba brațul EN-only, care e o singură potrivire pentru toate limbile. Vezi și
[[paper-slabiciuni-de-reviewer]] și [[nisioi-fir-monolingv-lolo]].
