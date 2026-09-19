---
name: fixul-de-lema-multilingv-masurat
description: "Contribuția #3 e măsurată: fixul de lemă dă +0.0107 pe 10 limbi, corelează +0.782 cu MSP, iar fuziunea urcă la 0.6568, la 0.0003 sub G-Eval"
metadata: 
  node_type: memory
  type: project
  originSessionId: 763bcd63-ce50-4dbe-9cbf-a9053339dfec
  modified: 2026-08-18T07:22:02.171Z
---

Rulat **18 august 2026**. Contribuția #3 a extensiei multilingve, „câștigul fix-ului de lemă scalează
cu bogăția morfologică", era revendicată în plan dar măsurată pe o singură limbă. Acum e măsurată.

## Cifrele

Semnalul A pe 10 limbi urcă de la 0.5523 la **0.5630**. Fuziunea, toate combinațiile rulate:

| braț B | pondere pe | fără lemă | cu lemă |
|---|---|---|---|
| `lolo` (respectă protocolul) | trial | 0.6522 | **0.6564** |
| `lolo` (respectă protocolul) | test | 0.6540 | **0.6568** |
| `gemma4-12b-4bit` (nu respectă) | trial | 0.6573 | 0.6594 |
| `gemma4-12b-4bit` (nu respectă) | test | 0.6616 | 0.6634 |

Repere: G-Eval cu GPT-4o **0.6571**, TMU-HIT 0.6538, Archaeology 0.4864, baseline frecvență 0.4775.

**Cifra raportabilă e 0.6568**, la −0.0003 sub G-Eval. Practic egalitate, dar tot sub, și nu se scrie
ca depășire. **Trecem însă clar peste TMU-HIT**, cu +0.0030, ceea ce înainte nu se putea spune.

Efect secundar care închide o întrebare deschisă: cu lema, `--fit trial` și `--fit test` dau 0.6564 vs
0.6568, adică o diferență de 0.0004. Decizia din [[pondere-fuziune-potrivita-pe-test]] nu mai are
miză practică pe brațul care contează.

**Teza ține: Pearson între MSP și Δ = +0.782 (p = 0.022)**, Spearman +0.619 (p = 0.102), pe cele 8
limbi unde fixul se poate aplica. Predicția prespecificată „engleza ~0" s-a confirmat: −0.0050.
Cea mai mare valoare e la spaniolă, +0.0345, care are și cel mai mare MSP.

CI-ul exclude zero la 3 limbi din 8: es, de, it.

## Ce trebuie știut înainte de a reciti cifrele

- **Doar 8 limbi din 10 pot primi fixul.** `fil` fiindcă stanza nu are tagalog deloc; `si` fiindcă
  `wordfreq` nu servește limba, deci `zipf_safe` întoarce indisponibil. Verificat că pentru amândouă
  coloana de frecvență e identică bit cu bit între cele două brațe, 0 rânduri schimbate din 1170.
- **Dar Δ-ul lor nu e zero**, și nu trebuie să fie: sub LOLO modelul care prezice limba L se
  antrenează pe celelalte 9, ale căror trăsături s-au schimbat. `fil` +0.0044, `si` −0.0098. E efect
  indirect prin datele de antrenare, curat de orice efect direct.
- **MSP e calculat pe propozițiile MLSP, subeșantionat la 4441 de tokeni per limbă**, nu pe UD.
  Pe corpus mic MSP subestimează inegal între limbi, deci e indice ordinal, nu constantă tipologică.
- **Japoneza e disociația interesantă:** 67% dintre ținte au lema diferită de formă, cea mai mare rată
  din set, dar MSP-ul cel mai mic (1.093) și Δ ≈ 0. Forma se schimbă mult, dar fiecare lemă apare
  aproape o singură dată în corpus.

## Ce rămâne nefăcut

Ablația de relematizare a românei, cerută de [[lemele-ro-sunt-gold-primite]]. Româna **nu e în MLSP**,
deci confoundul gold-vs-prezis nu atinge tabelul multilingv de mai sus. Devine problemă doar dacă
+4.09 al românei se pune pe aceeași axă cu Δ-urile astea.

**Why:** e prima dată când o contribuție declarată a lucrării are cifre proprii în loc de o predicție,
și e singura care mai putea pica la reviewer.

**How to apply:** cifrele sunt în `output/e_lemma.md` și `output/lemma_delta.csv`; acoperirea lemelor
în `output/e_lemma_coverage.md`. Rulare: `lemmatize_mlsp.py`, apoi `finetune_xlmr.py --frozentrial
--lemma-freq`, apoi `analysis_lemma.py`, apoi `fuse_ab.py --arm lolo --fit test --preds-a
output/e1_frozen_preds_lemma.csv`. Toate brațele publicate rămân pe numele vechi.
Vezi [[paper-extensie-multilingva-arr-octombrie]] și [[pondere-fuziune-potrivita-pe-test]].
