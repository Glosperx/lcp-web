---
name: pondere-fuziune-potrivita-pe-test
description: "Ideea 1 executată 18 august: w potrivit pe testul celorlalte 9 limbi dă 0.6540 pe lolo (+0.0018) și 0.5676 pe brațul principal (+0.0356), care astfel trece peste A singur"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6eae725f-c7e6-4edc-b85c-6cc02850bd29
  modified: 2026-08-17T22:02:30.780Z
---

> **Cifrele de mai jos sunt pe `n = 5606`, dinainte de P11.** Sistemul e acum **0.674946 pe n = 5624**.
> Ce e mai jos ramane valabil ca rationament si ca ordine a efectelor, dar **cifrele nu se citeaza**.
> Vezi [[p11-adoptia-facuta]].


Rulat **18 august 2026**, sesiune scurtă de execuție. Ideea 1 din
`~/.claude/plans/idei-imbunatatire-dupa-etapa2.md`, singura care nu era o idee ci o reparație de
protocol. Zero inferență nouă, totul recalculat pe predicțiile deja pe disc. Rapoartele:
`output/e_fusion_fitcmp.md` peste brațe, `output/e_fusion_<braț>_fitcmp.md` per braț.

| braț B | fit trial | fit test | diferența | față de 0.6571 |
|---|---|---|---|---|
| `qwen3-8b-4bit`, principal | 0.5320 | **0.5676** | +0.0356 | −0.0895 |
| `gemma4-12b-4bit` | 0.6573 | **0.6616** | +0.0042 | +0.0045 |
| `lolo`, brațul citabil | 0.6522 | **0.6540** | +0.0018 | **−0.0031** |

**Ipoteza lui Alexandru s-a confirmat în ambele jumătăți.** Pe brațul principal w trece de la 0.43 la
0.74 și fuziunea trece de sub A singur (0.5320 față de 0.5523) la peste el, 0.5676. Deci simptomul era
într-adevăr un w prost estimat, nu un semnal B inutil. Pe `lolo` urcă puțin, iar deficitul față de
G-Eval scade de la 0.0049 la 0.0031.

**Media ascunde semne opuse, și asta contează la scris.** Pe `lolo`, potrivirea pe test urcă 6 limbi și
scade 4, cu intervalul pereche excluzând zero în sus pe 3 și **în jos pe 1**, japoneza cu −0.0060. Pe
brațul principal w-ul potrivit pe test iese uniform mare, 0.70 până la 0.80, și strică exact limbile
unde B chiar era bun: fil −0.069, ja −0.040. Vezi [[decalaj-trial-test-masurat]] pentru de ce.

## Două lucruri de protocol descoperite în sesiune

**Un caz care ar fi picat tăcut.** La `lolo` cu franceza ținută deoparte, selecția imbricată cere
`qwen35-9b-8bit` pentru 7 din cele 9 limbi de potrivire, iar modelul acela e rulat pe test doar pe
franceză. Codul dinainte le-ar fi aruncat fără niciun mesaj și w(fr) s-ar fi potrivit pe 2 limbi.
Rezolvat prin restrângerea pool-ului la modelele măsurate efectiv pe limba și splitul de potrivire,
decisă de Alexandru. Filtrul e **no-op pe trial**, fiindcă acolo toate cele 7 modele au toate cele 10
limbi, deci implicitul rămâne bit-exact. Cele 7 cazuri sunt listate nominal în raport.

**O dependență indirectă preexistentă, documentată nu reparată.** `zA` pentru o limbă de potrivire L'
vine din modelul iterației L' din `frozen_trial_gap`, care a inclus rândurile de test ale lui L. Deci
w(L) depinde indirect de etichetele lui L, prin predicțiile lui A pe alte limbi. **Există identic și la
`--fit trial`**, nu e introdusă de schimbare, fiindcă ambele folosesc aceleași predicții din
`e1_frozen_preds.csv`. Mărimea rămâne **neverificată**: ar cere un braț A dublu imbricat, 90 de
potriviri `blend_ridge_hgb` în loc de 10. Vezi [[lolo-exista-deja-in-cod]].

## Cele două puncte deschise, ÎNCHISE pe 18 august seara

**Potrivirea pe test e sistemul**, și întrebarea s-a mutat mai departe: cu fixul de lemă brațul `lolo`
cu `--fit test` dă 0.6568, iar peste el s-au adăugat ansamblul de surse și fertilitatea. Alexandru a
ales încadrarea: **`fert_inloc` fixat prin argument, 0.664555, e sistemul**, iar setul ales LOLO,
0.663602, e notă de robustețe. Vezi [[ansamblul-de-surse-pentru-semnalul-a]].

**Agregatul pereche se calculează acum de cod**, în `fuse_ab._agg_boot`: se mediază cele 10 limbi la
fiecare reeșantionare, deci iese o distribuție a mediei, nu o medie de distribuții. Apare în raport ca
secțiunea „Intervalele mediei, nu ale limbilor", cu CI și P(>0) pentru fuziune față de A, față de B și
față de configurația de azi.

Cod: `--fit {trial,test,both}` în `fuse_ab.py`, singurul fișier atins. Implicitul `trial` reproduce bit
cu bit cele 6 CSV-uri ale etapei 2, verificat cu `cmp` înainte și după.
