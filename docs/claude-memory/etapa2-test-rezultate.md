---
name: etapa2-test-rezultate
description: "Etapa 2 închisă pe 18 august: fuziunea A+B sub protocol LOLO dă 0.6522 pe testul complet, la 0.0049 sub G-Eval; franceza singură explică tot deficitul"
metadata: 
  node_type: memory
  type: project
  originSessionId: 881f8b35-360d-445f-8f36-3dfe03afca8e
  modified: 2026-08-17T22:02:44.310Z
---

Rulat **17 spre 18 august 2026**, sesiunea de execuție a săptămânii 4. Toate cifrele sunt pe **testul
complet**, 5624 de ținte, n între 445 și 600 per limbă, deci **astea sunt primele cifre ale lucrării
care se compară legitim cu bara publicată**. Rapoartele: `output/e_fusion_lolo.md`,
`output/e_bakeoff_test.md`, `output/e_split_gap.md`.

| sistem, pe test | r mediu pe 10 limbi |
|---|---|
| semnalul A singur, brațul înghețat | 0.5523 |
| semnalul B singur, sub selecție LOLO | 0.6322 |
| **fuziunea A + B, w ales LOLO** | **0.6522** |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |

**Nu trecem de 0.657, suntem la 0.0049 sub.** Fuziunea bate A pe 10 limbi din 10, cu intervalul pereche
excluzând zero pe 9, și bate B pe 10 din 10, cu intervalul excluzând zero pe 6. Ponderea medie a lui A
iese 0.22, aleasă leave-one-language-out pe trial.

## Franceza explică singură tot deficitul

Față de G-Eval, limbă cu limbă, **câștigăm pe 7 din 10 și pierdem pe 3**: ca −0.056, de −0.016,
**fr −0.193**. Fără franceză am fi net deasupra. Cauza e dublă și cunoscută: selecția LOLO alege pe
franceză `qwen35-9b-8bit`, care dă 0.542 acolo, în loc de Gemma cu 0.642, iar chiar și Gemma e mult sub
cei 0.764 ai lui G-Eval. **Franceza e pârghia, nu sinhaleza.** Pe sinhaleză deja batem tot ce s-a
publicat, 0.3495 față de 0.328 și 0.308.

## Tensiunea deschisă, care cere o decizie de la Alexandru

**§5.2 s-a înrăutățit de trei ori la scară.** Costul brațului principal era −0.0901 pe trial și e
**−0.2580 pe test**. Fuziunea cu brațul principal dă 0.5320, adică **sub semnalul A singur**, 0.5523.
Formulat direct: pe testul complet, brațul ales pe acoperire face sistemul mai prost decât dacă n-ar
exista niciun LLM în el. Revendicarea de acoperire și cea de performanță nu mai pot fi susținute de
același braț. Vezi [[brate-llm-per-limba]] și [[decalaj-trial-test-masurat]].

Margine superioară, etichetată ca atare fiindcă încalcă §5.1: Gemma peste tot dă 0.6573 la fuziune.
Protocolul costă deci 0.0051, plătit integral pe franceză.

Cod nou în sesiune: `fuse_ab.py`, plus `--split`/`--langs` în `bakeoff_trial.py`, `--frozentrial` în
`finetune_xlmr.py`, `boot_r_ci` în `mlsp_common.py`. Nimic nu e comis, branch `alex_llm`.

## Ce urmează, notat dar nedecis

Cele cinci idei de îmbunătățire, cu costuri și cu ce e neverificat la fiecare, sunt în
**`~/.claude/plans/idei-imbunatatire-dupa-etapa2.md`**.

**Ideea 1 e RULATĂ pe 18 august**, iar cifrele de mai sus nu mai sunt singurele: cu ponderea potrivită
pe testul celorlalte 9 limbi, `lolo` dă **0.6540** în loc de 0.6522, iar brațul principal urcă de la
0.5320 la 0.5676, adică **peste A singur**, ceea ce desface parțial tensiunea §5.2 de mai sus. Detaliile
și ce rămâne de decis sunt în [[pondere-fuziune-potrivita-pe-test]]. Ideile 2 până la 5 rămân
neîncepute.
