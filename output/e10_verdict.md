# E.10 inchis. `v4_cot` pe Gemma, si ce decide

Rulat 17 august 2026, `prompt_lab.py --model gemma4-12b-4bit --variants v4_cot`. 300 de instante,
zero NaN, 30.1 minute la 6.02 s per item. Cifrele sunt in `output/e10_prompt.md`, regenerat.

Era ultimul lucru oprit la jumatate din Bloc E. Inchide singura rezerva a concluziei ca **ansamblul de
prompturi nu se transfera intre modele**: pana acum Gemma nu avea `v4_cot`, deci `e6`, `e7` si `e8` nu
se puteau calcula pentru ea, iar comparatia cu Qwen se facea pe seturi de candidati diferite.

## Scara ansamblurilor, acum pe set identic de candidati

Ordinea e prespecificata, "adauga urmatoarea varianta", nu aleasa dupa ce s-au vazut cifrele.

| ansamblu | ce adauga | Qwen3-8B | Gemma 4 |
|---|---|---|---|
| `e5` | cele 4 simple + fewshot | +0.590 | **+0.700** |
| `e6` | + `v4_cot` | +0.608 | +0.696 |
| `e7` | + `v7_proportie` | +0.619 | +0.686 |
| `e8` | + `v8_marcat` | **+0.623** | +0.688 |

**Imagine in oglinda, pe aceeasi scara.** Fiecare prompt adaugat urca Qwen monoton, de la 0.590 la
0.623, si coboara Gemma, de la 0.700 la 0.688. Qwen castiga +0.058 de la `e2` la `e8`; Gemma +0.002.

`v4_cot` singur da **+0.556** pe Gemma, fata de +0.347 pe Qwen. Deci CoT nu e inutil pe Gemma ca
varianta individuala, e al treilea din opt. Nu ajuta insa in ansamblu, ceea ce e exact opusul
mecanismului de pe Qwen, unde cele mai slabe variante individual erau cele mai valoroase in ansamblu.

## Selectia LOLO peste variante nu se misca

| model | baseline | sub selectie LOLO | castig |
|---|---|---|---|
| Qwen3-8B | +0.5650 (`v0_zeroshot`) | +0.6182 | **+0.053** |
| Gemma 4 | +0.6860 (`e2_ansamblu`) | +0.6808 | **-0.005** |

Tabelul de selectie al Gemmei e **identic cu cel dinainte de a exista `v4_cot`**: `e5_ansamblu` pe 7
limbi, `v3_fewshot` pe ca, it si pt. Niciunul din cele trei ansambluri nou deblocate nu castiga vreo
limba. Ca sa rastoarne concluzia, CoT ar fi trebuit sa aduca Gemmei mult mai mult decat cele +0.018
aduse lui Qwen; a adus -0.004.

## Teza care ramane

Medierea prompturilor decorelate repara un model slab, nu imbunatateste un model bun. Explicatia e
masurata: corelatia medie intre cele sapte prompturi e **0.541 pe Qwen si 0.772 pe Gemma**. Cand
prompturile spun acelasi lucru, medierea lor nu adauga informatie, doar dilueaza varianta cea mai buna.

Consecinta operationala: **ansamblul de prompturi pe test, 8.2 ore per model, nu se justifica pe
Gemma.** Pe bratul principal ramane o intrebare deschisa, fiindca acolo aduce +0.053, dar se decide cu
cifrele de la etapa 2 pe masa, nu acum.
