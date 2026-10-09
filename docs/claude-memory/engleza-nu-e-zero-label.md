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
transductivă din [[lolo-exista-deja-in-cod]]. Vechea obiectie ca nu se repara prin cod (bratul EN-only e o
singura potrivire) s-a rezolvat pe 26 sep: pe randurile en, p_en se inlocuieste cu p_multi curat. Vezi și
[[paper-slabiciuni-de-reviewer]] și [[nisioi-fir-monolingv-lolo]].

## Varianta curata, rulata 26 sep 2026

Flag nou `finetune_xlmr.py --frozentrial --en-fara-complex` (default neschimbat): la L = en, p_multi fara
Xen, si p_en al randurilor en = acelasi p_multi. Control fara flag: bit-identic pe cele 3 encodere, pe
media lor si pe fuziune (0.693718). Rezultat, tag `en_fara_complex_ro11`, A in
`output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc_en-fara-complex_ro11.csv`:
engleza fuziune 0.8732 -> 0.8695 (d -0.0037, CI [-0.0107, +0.0026]), A 0.8301 -> 0.8064, B neschimbat;
media pe 11 limbi 0.693718 -> 0.692527 (d -0.0012 [-0.0020, -0.0005]); pe 10 MLSP 0.68908 -> 0.68783.
Celelalte limbi se misca prin criteriul LOLO (w_src), cel mai mult it -0.0037; es, fil, si exact 0.
Nimic comis. Vezi [[rolcp-a-11a-limba-lolo]].

**ADOPTAT 26 sep 2026** de Alexandru: "tot paperul se invarte in jurul la zero label". Sistemul pe 11 limbi e
de acum 0.692527 (comanda adoptata + `--en-fara-complex` la cele 3 rulari --frozentrial). Varianta pe 10
limbi (0.690001) are aceeasi scurgere pe engleza si NU a fost rulata curat.
