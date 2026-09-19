---
name: ansamblul-de-surse-pentru-semnalul-a
description: "ÎNCHIS 18 aug: ansamblul plus fertilitatea sunt în cod, sistemul e 0.6646 în output/e_fusion_lolo_ens.md; cifrele ad-hoc vechi (0.6628/0.6585/0.6637) NU se citează"
metadata: 
  node_type: memory
  type: project
  originSessionId: e32d25da-15bf-4d38-bed9-5f3f8f3b518f
  modified: 2026-08-18T12:40:00.000Z
---

> **Cifrele de mai jos sunt pe `n = 5606`, dinainte de P11.** Sistemul e acum **0.674946 pe n = 5624**.
> Ce e mai jos ramane valabil ca rationament si ca ordine a efectelor, dar **cifrele nu se citeaza**.
> Vezi [[p11-adoptia-facuta]].


**Portat în cod pe 18 august 2026 și rulat.** Nu mai e nimic ad-hoc: `--ens` și `--a-set` în
`fuse_ab.py`, `--afeat` în `finetune_xlmr.py`, parametri opționali pe `_Xc`. Raportul de sistem e
`output/e_fusion_lolo_ens.md`, cu bootstrap, agregat pe medie și tabel de audit extins.

| configurație | r | față de G-Eval 0.6571 |
|---|---|---|
| azi, A = `p_multi` | 0.656780 | −0.0003 |
| doar ansamblul de surse | 0.663553 | +0.0065 |
| doar `fert_inloc` | 0.659108 | +0.0020 |
| **sistemul: ansamblu + `fert_inloc`** | **0.664555** | **+0.0075** |
| notă de robustețe: setul ales și el LOLO | 0.663602 | +0.0065 |

Agregat pereche pe contexte, sistemul față de azi: **+0.0078, CI [+0.0047, +0.0110], P(>0) = 100%**.
Față de A singur +0.0842 și față de B singur +0.0323, ambele cu P = 100%.

## Cifrele ad-hoc din nota de pe 18 august dimineață nu se citează

Scriptul ad-hoc (pierdut) a refolosit coloana `B` din `fusion_preds_lolo_fittest_lemma.csv`, adică
modelul ales final per limbă, în loc să re-aleagă modelul lui B imbricat cu `exclude={L}` cum face
`fuse_ab`. Când `fil` sau `si` e ținută deoparte, selecția imbricată dă **francezei** alt model
(`gemma4-12b-4bit` în loc de `qwen35-9b-8bit`), ceea ce mută alegerile. De aceea 0.6628 → 0.6636,
0.6585 → 0.6591, 0.6637 → 0.6636. Numai sistemul cade pe aceeași cifră la 4 zecimale, 0.6646.
**Versiunea imbricată e cea curată**, flat-B lăsa modelul francezei să fie ales folosind trial-ul
limbii ținute deoparte.

## Regula de selecție, recuperată prin reverse-engineering

Nu era scrisă nicăieri; am testat patru ipoteze și una reproduce tabelul documentat 10 din 10.
E acum în `fuse_ab.fit_choice`, cu docstring. Esențialul: criteriul unui candidat `(set, w_src)` se
măsoară pe L' cu ponderea lui L' aleasă pe celelalte 8, deci **excluzând și L și L'**. Bucla
interioară nu e o precauție adăugată, e criteriul care a produs măsurătoarea.

**De ce funcționează:** brațul EN-only e în medie mai bun, r 0.5687 față de 0.5630, iar corelația
dintre brațe cade la 0.761 pe ja și 0.717 pe si, exact limbile unde A e slab. `w_src` ales cade între
0.625 și 1.000, deci brațul EN-only ia majoritatea ponderii peste tot. Replicare a lui run 1 peste
run 2 din Cristea și Nisioi.

Vezi [[pondere-fuziune-potrivita-pe-test]], [[fixul-de-lema-multilingv-masurat]],
[[fertilitate-tokenizere-masurata]], [[etapa2-test-rezultate]].
