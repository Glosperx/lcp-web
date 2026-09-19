---
name: r-si-r2-masurate-pe-rolcp
description: "r și R² pe RoLCP (0.777 / 0.603) sunt ACUM ÎN paper_full.tex, în trei locuri, lângă baseline-ul RALS 0.71±0.05. Diferența de compozit 68.99 vs 69.74 rămâne neexplicată și NU e scrisă în text."
metadata:
  node_type: memory
  type: project
  originSessionId: 6df5edc7-10be-4071-bfae-d4dea4467d43
  modified: 2026-07-30T11:04:44.036Z
---

Calculat pe **30 iulie 2026**. Script salvat în repo: `score_rolcp.py`, cu procedura în docstring.
Scris în lucrare în aceeași zi, la cererea explicită a lui Alexandru, după ce a respins două
variante mai lungi (vezi „How to apply").

## Rezultatul

Join **1587/1587 pe cheie completă** (`text_name`, `token`, `text`) între `submission.csv`,
`data/test_set.csv` și `RoLCP.csv` din RALS. Zero nepotriviri, setul nostru de test e RoLCP exact.

| | |
|---|---|
| Pearson `r` | **0.7770**, CI 95% [0.7568, 0.7958] |
| `R²` | **0.6028** |
| compozit `50(\|r\|+max(0,R²))` recalculat | 68.99, față de **69.74** returnat de evaluare |
| gold RoLCP (coloana `complexity`) | medie 0.2701, std 0.1674 |
| RALS, Ridge supervizat, 10-fold CV grupat | `r = 0.71 ± 0.05` |

**RALS raportează în Tabelul 2 numai Pearson, niciun R².** Restul tabelului lor: HT `0.56 ± .11`,
WT `0.68 ± .04`, transfer WT→RoLCP `0.60`, RoLCP→WT `0.61`. Verificat direct în PDF-ul lor
(aclanthology.org/2025.emnlp-main.1603), nu din memorie.

**Sistemul nostru, fără nicio etichetă de antrenare românească, ajunge în intervalul baseline-ului
supervizat al autorilor datelor.** Intervalele abia se ating: al lor pleacă de la 0.66/urcă la 0.76,
al nostru pleacă de la 0.757.

## Unde e scris, exact (trei locuri, cerute explicit)

1. **§2 Related Work**, paragraful `Lexical complexity prediction`: cifra RALS inline,
   `r = 0.71 ± 0.05`, plus „They report correlation only, not $R^2$".
2. **§2**, paragraf nou imediat după, `\paragraph{Our result on the same set.}`: `r = 0.777`,
   CI, `R² = 0.603`, plus o singură frază despre când s-au citit etichetele („after the predictor
   was frozen, in order to score it").
3. **§3.1** (finalul paragrafului de metrică) și **§4.1** (paragraful reperului, rescris):
   cifrele repetate a treia oară, lângă cea a RALS.

Limitations: două paragrafe devenite false au fost **șterse integral**: „The reported metric
cannot be decomposed" și „No score on the target labels is reported at all". Al treilea,
„partly circular", a rămas, cu o frază ajustată de la „could not be validated" la „was not
validated", fiindcă acum e o alegere, nu o imposibilitate.

## Calibrarea iese confirmată, nu suspectă (verificat, nu se schimbă)

`R²` se maximizează la `σ = r·σ_gold = 0.1301`; noi am folosit `0.125`, la 0.001 de optim.
`μ = 0.27` cade pe media reală `0.2701`. Media/std `0.23`/`0.23` din Tabelul 1 al RALS descriu
coloana `complexity_b`, NU `complexity` (media reală). Calibrarea nu e greșită, nu se comentează
în Limitations.

## Diferența 68.99 vs 69.74: rămâne neexplicată, deliberat nescrisă în paper

Verificat exhaustiv, nimic din ce s-a testat o explică:
- `submission.csv` scorează identic cu `output/et_pca_w20.csv`, exact configurația `w_D=0.20`
  pentru care evaluarea a returnat 69.74. **Nu e fișierul greșit.**
- Nu e coloana greșită de gold, nu e mediere per-text (59.85), nu e rotunjire (69.00), clipul e
  inactiv.
- **Nu e offset fix**: recalculând tot tabelul de ablație, diferența își schimbă semnul (surface
  10.27 vs 9.64, ET-baseline 41.76 vs **42.98**, surprisal 64.81 vs 64.17, lemma 68.90 vs 67.89).
- Niciunul din cele 88 de fișiere de predicție din `output/` nu ajunge la 69.74; maximul e 69.18.

Cauza probabilă: fișierele din `output/` sunt re-rulări, nu exact ce s-a trimis la evaluare atunci.
Neverificabil, scorerul evaluării nu e accesibil. Decizie: compozitele din tabele rămân cele
returnate; `r` și `R²` sunt cifrele noastre; cele două nu se amestecă în text.

**How to apply:** dacă vine o cerere similară pe altă cifră a lucrării, verifică mai întâi ce
raportează sursa citată (nu presupune din memorie — RALS nu are R² deloc, aflat abia verificând
PDF-ul). Când propui text nou pentru paper, ține variantele scurte: Alexandru a respins de două ori
o formulare mai lungă/mai „explicativă" cu „ai complicat", cerând enumerare directă (cifra lor,
cifra noastră, fără fraze de tip „comparison is between two settings rather than two systems").
Vezi [[rals-rolcp-datele-sunt-ale-lui-nisioi]], [[paper-slabiciuni-de-reviewer]],
[[preferinte-de-scriitura-paper]].
