# Acoperirea lemelor, pe limbile MLSP plus CompLex EN

Generat 2026-08-29 20:09:55 de `lemmatize_mlsp.py`. Date brute: `output/lemmas_mlsp.csv` si `output/lemmas_complex_en.csv`.

Coloana care conteaza e **lema difera de forma**. Daca lema egaleaza forma, fixul nu are ce repara: `max(zipf_forma, zipf_lema)` intoarce aceeasi valoare. Ea e predictia directa a tezei morfologice, inainte de a masura vreun r.

`frecventa` spune daca `wordfreq` serveste real limba. Unde e nu, fixul e no-op indiferent de lema, fiindca `zipf_safe` intoarce indisponibil si `lexical()` nu aplica inlocuirea.

| split | limba | n | context | izolat | gol | lema difera de forma | frecventa |
|---|---|---|---|---|---|---|---|
| complex_en | `en` | 8423 | 8423 | 0 | 0 | **2292** (27.2%) | da |
| test | `ca` | 445 | 445 | 0 | 0 | **214** (48.1%) | da |
| test | `de` | 570 | 570 | 0 | 0 | **271** (47.5%) | da |
| test | `en` | 570 | 570 | 0 | 0 | **214** (37.5%) | da |
| test | `es` | 593 | 593 | 0 | 0 | **338** (57.0%) | da |
| test | `fil` | 570 | 0 | 0 | 570 | **0** (0.0%) | da |
| test | `fr` | 569 | 569 | 0 | 0 | **275** (48.3%) | da |
| test | `it` | 570 | 570 | 0 | 0 | **304** (53.3%) | da |
| test | `ja` | 570 | 570 | 0 | 0 | **384** (67.4%) | da |
| test | `pt` | 567 | 567 | 0 | 0 | **216** (38.1%) | da |
| test | `ro` | 1587 | 1587 | 0 | 0 | **1159** (73.0%) | da |
| test | `si` | 600 | 0 | 0 | 600 | **0** (0.0%) | **nu** |
| trial | `ca` | 30 | 30 | 0 | 0 | **11** (36.7%) | da |
| trial | `de` | 30 | 23 | 7 | 0 | **1** (3.3%) | da |
| trial | `en` | 30 | 30 | 0 | 0 | **10** (33.3%) | da |
| trial | `es` | 30 | 30 | 0 | 0 | **22** (73.3%) | da |
| trial | `fil` | 30 | 0 | 0 | 30 | **0** (0.0%) | da |
| trial | `fr` | 30 | 30 | 0 | 0 | **13** (43.3%) | da |
| trial | `it` | 30 | 30 | 0 | 0 | **15** (50.0%) | da |
| trial | `ja` | 30 | 30 | 0 | 0 | **20** (66.7%) | da |
| trial | `pt` | 30 | 30 | 0 | 0 | **17** (56.7%) | da |
| trial | `si` | 30 | 0 | 0 | 30 | **0** (0.0%) | **nu** |
