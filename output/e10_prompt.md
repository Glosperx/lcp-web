# E.10. Optimizarea promptului pentru semnalul B

Generat 2026-08-17 21:18:14 de `prompt_lab.py --aggregate`. Pe cele 300 de instante de trial, niciodata pe test. Datele brute: `output/promptlab_<model>.csv`.

Selectia variantei e tratata ca selectia modelului din §5.1: leave-one-language-out. Altfel, alegerea promptului pe trial-ul tuturor celor 10 limbi ar fi tuning pe limba tinuta deoparte.

## `gemma4-12b-4bit`

### r per limba, per varianta de prompt

| model | ca | de | en | es | fil | fr | it | ja | pt | si | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `v0a_expert` | +0.651 | +0.637 | +0.751 | +0.622 | +0.507 | +0.616 | +0.657 | +0.792 | +0.876 | +0.304 | **+0.641** |
| `v0b_short` | +0.780 | +0.787 | +0.701 | +0.733 | +0.553 | +0.525 | +0.802 | +0.823 | +0.826 | +0.049 | **+0.658** |
| `v1_learner` | +0.577 | +0.427 | +0.549 | +0.640 | +0.437 | +0.655 | +0.530 | +0.762 | +0.752 | +0.691 | **+0.602** |
| `v2_rubrica` | +0.663 | +0.819 | +0.798 | +0.615 | +0.580 | +0.503 | +0.709 | +0.746 | +0.737 | +0.279 | **+0.645** |
| `v3_fewshot` | +0.671 | +0.780 | +0.857 | +0.789 | +0.592 | +0.670 | +0.667 | +0.827 | +0.772 | +0.346 | **+0.697** |
| `v4_cot` | +0.638 | +0.759 | +0.749 | +0.487 | +0.179 | +0.398 | +0.730 | +0.677 | +0.804 | +0.137 | **+0.556** |
| `v7_proportie` | +0.510 | +0.771 | +0.733 | +0.656 | +0.192 | +0.385 | +0.620 | +0.548 | +0.514 | +0.132 | **+0.506** |
| `v8_marcat` | +0.677 | +0.835 | +0.842 | +0.673 | +0.341 | +0.585 | +0.718 | +0.717 | +0.779 | +0.147 | **+0.631** |
| `e2_ansamblu` | +0.743 | +0.753 | +0.737 | +0.709 | +0.642 | +0.609 | +0.770 | +0.834 | +0.893 | +0.170 | **+0.686** |
| `e3_ansamblu` | +0.716 | +0.734 | +0.707 | +0.730 | +0.591 | +0.661 | +0.736 | +0.844 | +0.871 | +0.184 | **+0.677** |
| `e4_ansamblu` | +0.713 | +0.775 | +0.738 | +0.713 | +0.610 | +0.645 | +0.740 | +0.836 | +0.856 | +0.227 | **+0.685** |
| `e5_ansamblu` | +0.718 | +0.787 | +0.780 | +0.740 | +0.620 | +0.666 | +0.738 | +0.847 | +0.849 | +0.260 | **+0.700** |
| `e6_ansamblu` | +0.716 | +0.805 | +0.784 | +0.710 | +0.603 | +0.655 | +0.752 | +0.842 | +0.869 | +0.228 | **+0.696** |
| `e7_ansamblu` | +0.707 | +0.815 | +0.796 | +0.712 | +0.540 | +0.640 | +0.758 | +0.832 | +0.847 | +0.214 | **+0.686** |
| `e8_ansamblu` | +0.711 | +0.828 | +0.812 | +0.710 | +0.531 | +0.647 | +0.763 | +0.823 | +0.844 | +0.208 | **+0.688** |

### Cost

| varianta | s per item | total | n |
|---|---|---|---|
| `v0a_expert` | 0.65 s | 3.2 min | 300 |
| `v0b_short` | 0.52 s | 2.6 min | 300 |
| `v1_learner` | 0.74 s | 3.7 min | 300 |
| `v2_rubrica` | 0.91 s | 4.5 min | 300 |
| `v3_fewshot` | 2.44 s | 12.2 min | 300 |
| `v7_proportie` | 0.61 s | 3.1 min | 300 |
| `v8_marcat` | 0.77 s | 3.8 min | 300 |
| `v4_cot` | 6.02 s | 30.1 min | 300 |

### Selectia LOLO peste variante

| limba | varianta aleasa pe celelalte 9 | media pe 9 | r pe L |
|---|---|---|---|
| ca | `v3_fewshot` | +0.7000 | +0.6705 |
| de | `e5_ansamblu` | +0.6908 | +0.7866 |
| en | `e5_ansamblu` | +0.6916 | +0.7797 |
| es | `e5_ansamblu` | +0.6959 | +0.7405 |
| fil | `e5_ansamblu` | +0.7093 | +0.6202 |
| fr | `e5_ansamblu` | +0.7043 | +0.6657 |
| it | `v3_fewshot` | +0.7003 | +0.6673 |
| ja | `e5_ansamblu` | +0.6842 | +0.8466 |
| pt | `v3_fewshot` | +0.6887 | +0.7715 |
| si | `e5_ansamblu` | +0.7494 | +0.2598 |

**r mediu sub selectie LOLO peste variante: +0.6808**.

Prag de zgomot: la n = 30, intervalul de 95% pentru r = 0.60 e [0.31, 0.79]. O varianta care castiga mai putin decat atat pe o limba nu a castigat nimic masurabil acolo; media pe 10 limbi e mai stabila.

## `qwen3-8b-4bit`

### r per limba, per varianta de prompt

| model | ca | de | en | es | fil | fr | it | ja | pt | si | medie |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `v0_zeroshot` | +0.367 | +0.795 | +0.748 | +0.528 | +0.481 | +0.406 | +0.573 | +0.576 | +0.615 | +0.561 | **+0.565** |
| `v0a_expert` | +0.129 | +0.699 | +0.768 | +0.499 | +0.511 | +0.472 | +0.522 | +0.376 | +0.444 | +0.392 | **+0.481** |
| `v0b_short` | +0.508 | +0.708 | +0.475 | +0.369 | +0.401 | -0.057 | +0.510 | +0.621 | +0.671 | +0.594 | **+0.480** |
| `v1_learner` | +0.157 | +0.741 | +0.715 | +0.566 | +0.518 | +0.488 | +0.449 | +0.484 | +0.558 | +0.389 | **+0.507** |
| `v2_rubrica` | +0.199 | +0.629 | +0.614 | +0.535 | +0.340 | +0.446 | +0.586 | +0.430 | +0.222 | +0.518 | **+0.452** |
| `v3_fewshot` | +0.308 | +0.276 | +0.444 | +0.629 | +0.321 | +0.554 | +0.593 | +0.644 | +0.614 | +0.460 | **+0.484** |
| `v4_cot` | +0.416 | +0.590 | +0.125 | +0.407 | +0.206 | +0.291 | +0.255 | +0.252 | +0.430 | +0.494 | **+0.347** |
| `v7_proportie` | +0.158 | +0.769 | +0.600 | +0.545 | +0.281 | +0.616 | +0.477 | +0.407 | +0.499 | +0.181 | **+0.453** |
| `v8_marcat` | +0.602 | +0.297 | +0.387 | +0.349 | +0.132 | +0.369 | +0.181 | +0.335 | +0.321 | +0.187 | **+0.316** |
| `e2_ansamblu` | +0.367 | +0.795 | +0.748 | +0.528 | +0.481 | +0.406 | +0.573 | +0.576 | +0.615 | +0.561 | **+0.565** |
| `e3_ansamblu` | +0.302 | +0.792 | +0.743 | +0.556 | +0.531 | +0.461 | +0.545 | +0.582 | +0.606 | +0.528 | **+0.564** |
| `e4_ansamblu` | +0.271 | +0.767 | +0.772 | +0.583 | +0.504 | +0.467 | +0.586 | +0.551 | +0.518 | +0.554 | **+0.557** |
| `e5_ansamblu` | +0.298 | +0.767 | +0.717 | +0.653 | +0.462 | +0.585 | +0.631 | +0.623 | +0.610 | +0.551 | **+0.590** |
| `e6_ansamblu` | +0.443 | +0.804 | +0.659 | +0.649 | +0.458 | +0.603 | +0.629 | +0.619 | +0.625 | +0.586 | **+0.608** |
| `e7_ansamblu` | +0.395 | +0.826 | +0.706 | +0.657 | +0.465 | +0.668 | +0.633 | +0.661 | +0.624 | +0.559 | **+0.619** |
| `e8_ansamblu` | +0.441 | +0.826 | +0.708 | +0.673 | +0.432 | +0.675 | +0.610 | +0.678 | +0.639 | +0.547 | **+0.623** |

### Cost

| varianta | s per item | total | n |
|---|---|---|---|
| `v0_zeroshot` | 0.62 s | 3.1 min | 300 |
| `v1_learner` | 0.34 s | 1.7 min | 300 |
| `v2_rubrica` | 0.34 s | 1.7 min | 300 |
| `v3_fewshot` | 0.76 s | 3.8 min | 300 |
| `v4_cot` | 3.17 s | 15.9 min | 300 |
| `v0a_expert` | 0.33 s | 1.7 min | 300 |
| `v0b_short` | 0.30 s | 1.5 min | 300 |
| `v7_proportie` | 0.34 s | 1.7 min | 300 |
| `v8_marcat` | 0.37 s | 1.8 min | 300 |

### Selectia LOLO peste variante

| limba | varianta aleasa pe celelalte 9 | media pe 9 | r pe L |
|---|---|---|---|
| ca | `e7_ansamblu` | +0.6444 | +0.3953 |
| de | `e8_ansamblu` | +0.6002 | +0.8258 |
| en | `e8_ansamblu` | +0.6133 | +0.7080 |
| es | `e8_ansamblu` | +0.6173 | +0.6725 |
| fil | `e8_ansamblu` | +0.6439 | +0.4324 |
| fr | `e8_ansamblu` | +0.6170 | +0.6747 |
| it | `e8_ansamblu` | +0.6242 | +0.6097 |
| ja | `e8_ansamblu` | +0.6167 | +0.6778 |
| pt | `e8_ansamblu` | +0.6209 | +0.6395 |
| si | `e8_ansamblu` | +0.6313 | +0.5465 |

**r mediu sub selectie LOLO peste variante: +0.6182**, fata de +0.5650 al baseline-ului `v0_zeroshot`. Castig: +0.0532.

Comparatie pereche fata de baseline, limba cu limba: **7 din 10 limbi se imbunatatesc**, medie +0.0532, sd 0.0960, deci 1.8 erori standard. Sugestiv, nu stabilit: la 9 grade de libertate asta nu trece pragul obisnuit. Per limba: ca +0.029, de +0.031, en -0.040, es +0.144, fil -0.049, fr +0.269, it +0.036, ja +0.102, pt +0.024, si -0.014.

Prag de zgomot: la n = 30, intervalul de 95% pentru r = 0.60 e [0.31, 0.79]. O varianta care castiga mai putin decat atat pe o limba nu a castigat nimic masurabil acolo; media pe 10 limbi e mai stabila.
