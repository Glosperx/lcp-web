# Validare locala (NU doar leaderboard public)

Fara etichete RO (14 = zgomot, nu prezic public). Validare prin:
- **free-gate cross-lingual** `transfer_eval` (train CompLex EN <-> test MLSP Romanic, mii de etichete, aceeasi metodologie Complex 2.0) = proxy onest pt scenariul RO.
- **CV 5-fold in-sursa** pe CompLex si MLSP (`_cv_r`).
- best linear (blend Ridge300+HGB): transfer_avg 0.5512 | cvEN 0.7829 | cvML 0.6115 (vezi analysis_lasso.py).

Onest: weight-ul surprisal (0.08), lemma-freq si calibrarea (0.27/0.125) au fost alese PARTIAL prin probing pe public (cateva submisii), nu doar pe gate. Public e folosit ca ghid, NU ca singura sursa; selectia de model (encoder/features/fine-tuning) s-a facut pe free-gate.

## Semnale (inter-corelatii)
```
  A_crosslingual  +1.000 +0.570 +0.255
  B_LLM           +0.570 +1.000 +0.068
  C_surprisal     +0.255 +0.068 +1.000
```
