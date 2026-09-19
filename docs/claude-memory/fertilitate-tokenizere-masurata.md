---
name: fertilitate-tokenizere-masurata
description: "Masurat 16 aug: Qwen3-8B cade pe byte fallback pe sinhaleza desi o listeaza oficial; Gemma 4 are cel mai bun tokenizer LLM; metoda se valideaza singura"
metadata: 
  node_type: memory
  type: project
  originSessionId: 70704065-2767-4d0f-af75-97c5215eba41
  modified: 2026-08-16T12:18:14.494Z
---

Rulat pe **16 august 2026**, etapa 0 din bake-off. Script: `measure_fertility.py`, rezultate în
`output/fertility_by_lang.csv`. Doar tokenizere, nicio greutate de model, minute pe Mac.

## Verificarea de sănătate trece

XLM-R pe română dă **1.948** subword-uri per țintă, față de **1.95** măsurat anterior în proiect
(§1.11 din raportul de fezabilitate). Deci convenția e `prefix_space=True`, adică ținta se tokenizează
cu spațiu în față, ca în mijlocul propoziției. Orice recalculare care nu reproduce 1.95 e greșită.

## Rezultatul, sinhaleză, subword-uri per octet

1.0 înseamnă un token per octet UTF-8, adică byte fallback pur. Sinhaleza are 3.00 octeți per caracter.

| Model | Listează oficial si? | tok/octet | tok/țintă |
|---|---|---|---|
| XLM-R base | da | **0.169** | 3.32 |
| **Gemma 4 12B** | **nu publică listă** | **0.214** | 4.19 |
| Qwen3.5-9B | nu publică listă | 0.345 | 6.98 |
| **Qwen3-8B** | **da, explicit în blog** | **0.573** | **11.56** |
| Aya Expanse 8B | **nu** | 0.647 | 13.04 |
| EuroLLM-9B | **nu** | **1.041** | 21.08 |

## De ce e concludent: metoda se validează singură

Cele două modele care **declară** că nu au sinhaleză, Aya Expanse și EuroLLM, cad amândouă pe octeți.
Deci măsurătoarea reproduce independent listele publicate acolo unde ele există. Asta face ca celelalte
două rânduri să fie interpretabile:

- **Gemma 4 nu publică listă, dar tokenizează sinhaleza aproape ca XLM-R.** Acoperirea există, Google
  n-o declară. Măsurătoarea suplinește declarația, și e dovadă mai directă decât o listă de producător.
- **Qwen3-8B listează explicit sinhaleza și o tokenizează ca un model care n-o are.** E mai aproape de
  Aya Expanse, care declară absența, decât de Gemma 4.

Diagnostic pe o țintă de 5 caractere: Qwen3-8B produce `[' �','�','�','�','�','ස','�','�']`, adică
fragmente UTF-8 rupte. XLM-R produce `['රූ','ස්ස']`, morfeme reale.

**Fraza de reținut: prezența pe lista de preantrenare nu implică acoperire de tokenizer.** Sunt două
lucruri diferite, iar la Qwen3 se contrazic. E un rezultat publicabil în sine.

## Alte constatări

- **Qwen3-8B e cel mai prost tokenizer pe toate cele 10 limbi MLSP plus româna**, nu doar pe sinhaleză.
  Vocabularul de 151.669 e prea mic. Gemma 4 (262.144) și Qwen3.5 (248.077) sunt sistematic mai bune.
- **Filipineza e în regulă peste tot**, 0.318 la 0.400, fără byte fallback nicăieri. Deci **sinhaleza e
  singura limbă efectiv ruptă**, ceea ce susține direct C4.
- Aya Expanse are cel mai bun tokenizer pe **română** din tot bazinul, 0.241, sub XLM-R la 0.252.
- Lovitura cea mai grea e pe **semnalul C**: surprisal-ul se calculează peste subword-urile țintei, iar
  11.56 fragmente de octeți fac mărimea aproape lipsită de sens. Semnalul B e afectat indirect.

## Consecința pentru alegerea modelului

Redeschide decizia din [[brate-llm-per-limba]]. Argumentul de acoperire se mută **de pe citarea unei
liste pe măsurătoarea noastră**, care are acum și grup de control. Cu criteriul ăsta, **Gemma 4 12B
trece în față** pentru brațul principal.

**Why:** planul aprobat alesese Qwen3-8B exclusiv fiindcă era singurul care publica o listă enumerată
conținând sinhaleza și tagalogul. Măsurătoarea arată că lista aia nu se traduce în capacitate, deci
criteriul care a produs alegerea era greșit, nu doar alegerea.

**How to apply:** nu fixa Gemma 4 încă. Fertilitatea e **poartă de screening, nu test**. Un tokenizer
mai bun nu garantează corelație mai bună. Testul e etapa 1, bake-off pe cele 300 de instanțe de trial.
Qwen3-8B rămâne în bazin tocmai fiindcă discrepanța lui listă-vs-tokenizer e un rezultat de raportat.
Vezi [[rute-rulare-logits]], [[paper-extensie-multilingva-arr-octombrie]].
