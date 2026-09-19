# E.13. Controlul de al treilea prompt

Generat 2026-08-22 15:48:39 de `analysis_al3lea.py`. Referinta e sistemul adoptat, **r = 0.683849**, cu B = 0.659202 din doua prompturi.

Intrebarea, si e de identificare a mecanismului, nu de gasire a unei configuratii mai bune.
`FS3K` urca fuziunea cu +0.004642, dar few-shot-ul SINGUR pierde pe test, -0.0246 pe B. Deci castigul
nu vine din faptul ca promptul few-shot ar fi bun, si prima explicație plauzibila e reducerea de
varianta de la doi la trei membri. Daca asa e, atunci **orice** al treilea prompt de calitate
comparabila da acelasi castig, si nimic din rezultat nu e despre few-shot cross-lingual.

Asta conteaza pentru ce se poate SCRIE, nu doar pentru ce se adopta. Motivul pentru care few-shot
merita rulat, din rândul 10 al lui `output/e_prioritate.md`, era revendicarea fata de G-Eval, care e
3-shot in limba tinta. Revendicarea cere ca exemplele sa ajute. Daca rubrica da acelasi castig fara
nicio eticheta, revendicarea nu exista si fraza corecta in paper e „trei prompturi bat doua".

## 1. Semnalul B: promptul singur, si acelasi prompt ca al treilea membru

`B solo` e promptul singur, cu T ales LOLO prin exact aceeasi conducta. `B in trei` e perechea de acum plus el. `castig` e cat aduce ca al treilea membru. Coloanele de corelatie spun daca membrul e decorelat de cele doua de acum, adica daca aduce informatie sau doar mediere.

| membru | ce era pe trial | B solo | B in trei | B in trei + colaps | castig pe B | r cu expert | r cu scurt |
|---|---|---|---|---|---|---|---|
| `few-shot` | +0.7109 ca al treilea pe trial, cel mai bun | +0.634641 | +0.664449 | +0.666461 | **+0.005247** | 0.786 | 0.824 |
| `rubrica` | +0.6904 pe trial, al doilea | +0.633849 | +0.660059 | +0.662119 | **+0.000857** | 0.832 | 0.858 |
| `marcat` | +0.6895 pe trial, egal cu rubrica | +0.619089 | +0.663347 | +0.664934 | **+0.004146** | 0.744 | 0.868 |
| `learner` | +0.6773 pe trial, SUB perechea de doua: control negativ | +0.621406 | +0.659488 | +0.658812 | **+0.000286** | 0.744 | 0.725 |

## 2. Fuziunea, interval PERECHE al mediei fata de sistemul de acum

`limbi stricate` se citeste PRIMA, ca in `output/e_fewshot.md`.

| configuratie | membru al treilea | colaps | limbi stricate | r mediu | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|---|---|
| `FS3` | few-shot | nu | de | **0.686736** | +0.002880 | [+0.001055, +0.004796] | 99.9% |
| `FS3K` | few-shot | da | **niciuna** | **0.688506** | +0.004642 | [+0.002619, +0.006756] | 100.0% |
| `R3` | rubrica | nu | it | **0.684254** | +0.000384 | [-0.001544, +0.002272] | 66.0% |
| `R3K` | rubrica | da | **niciuna** | **0.685921** | +0.002030 | [-0.000013, +0.004214] | 97.2% |
| `M3` | marcat | nu | pt | **0.688407** | +0.004576 | [+0.002022, +0.006953] | 100.0% |
| `M3K` | marcat | da | **niciuna** | **0.690001** | +0.006153 | [+0.003436, +0.008713] | 100.0% |
| `L3` | learner | nu | es, it | **0.684598** | +0.000721 | [-0.000997, +0.002400] | 80.2% |
| `L3K` | learner | da | es, it | **0.683912** | +0.000040 | [-0.001656, +0.001800] | 51.2% |

## Verdict: e specific few-shot-ului?

Pe semnalul B, few-shot ca al treilea membru aduce **+0.005247**. Cel mai bun membru alternativ, `marcat`, aduce **+0.004146**, adica -0.001102 fata de el. Ordinea membrilor pe test, dupa castigul pe B: `few-shot` +0.005247, `marcat` +0.004146, `rubrica` +0.000857, `learner` +0.000286.

Corelatia dintre castigul ca al treilea membru si calitatea membrului luat SINGUR, peste cei 4 membri: r = +0.151. Daca e mare, ce conteaza e calitatea promptului, nu ce fel de prompt e.

**Castigul e specific few-shot-ului**: cel mai bun membru alternativ rams sub 80% din el, desi pe trial era la 97%. Deci exemplele etichetate din celelalte limbi aduc ceva ce un prompt oarecare nu aduce, si revendicarea fata de G-Eval se poate scrie chiar daca promptul singur pierde.

