# E.12. Few-shot din celelalte limbi, pe test

Generat 2026-08-22 13:59:05 de `analysis_fewshot.py`. Referinta e sistemul adoptat, **r = 0.683849**, din `output/fusion_lolo_adoptat_temp.csv`. Toate cifrele pe cele 10 limbi de test, agregate ca MEDIE pe limbi, nu pooled.

`fuse_ab.py` scrie cate un raport per configuratie, si in fiecare raport apar DOUA statistici `P(>0)`
diferite: media pe limbi a lui P(>0) in tabelul per limba, si P(>0) al MEDIEI in secțiunea
"Intervalele mediei". A doua e cea care se citeaza. Aici se recalculeaza a doua, o singura data,
pentru toate configuratiile, din predictiile per instanta, ca sa nu se poata citi din greseala
cealalta.

Ordinea coloanelor e ordinea in care se citesc: **`limbi stricate` INAINTE de `medie`**. Asa a fost
respins `distTpp` la 0.685763 si `prio_KW` la 0.685727, desi amandoua aveau media mai mare decat
sistemul.

## 1. Semnalul B singur, inainte de fuziune

Fuziunea amesteca B cu A si cu ponderea, deci un castig pe B se poate dilua sau se poate amplifica. Coloana asta spune cat a mutat promptul in chiar marimea pe care o schimba.

| configuratie | ce e | B mediu | fata de B-ul de acum |
|---|---|---|---|
| sistemul de acum | doua prompturi zero-shot, temperatura LOLO | +0.659202 | - |
| `FS` | few-shot singur, temperatura LOLO | +0.634641 | -0.024560 |
| `FSK` | few-shot singur, plus unirea cifrelor | +0.631345 | -0.027857 |
| `FS3` | media celor trei prompturi, temperatura LOLO | +0.664449 | +0.005247 |
| `FS3K` | media celor trei, plus unirea cifrelor | +0.666461 | +0.007259 |
| `FS3P` | cele trei, cate un T per prompt | +0.666577 | +0.007376 |
| `FS3KP` | cele trei, T per prompt, plus unirea cifrelor | +0.666782 | +0.007580 |

## 2. Fuziunea, cu intervalul PERECHE al mediei

`limbi stricate` e coloana care se citeste PRIMA: o limba stricata cu interval pereche care exclude zero respinge configuratia oricare ar fi media. `P(>0)` de aici e al MEDIEI, nu media pe limbi a lui P(>0) din tabelele lui `fuse_ab`.

| configuratie | de ce e in tabel | limbi stricate | limbi urcate | r mediu | fata de 0.683849 | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|---|---|
| `FS` | ceruta in brief | de, en, fil, pt, si | fr | **0.671531** | -0.012282 | [-0.018383, -0.006463] | 0.0% |
| `FSK` | ceruta in brief | de, en, fil, pt, si | fr | **0.670010** | -0.013800 | [-0.019693, -0.007921] | 0.0% |
| `FS3` | cernuta pe trial inainte de test | de | fr, ja | **0.686736** | +0.002880 | [+0.001055, +0.004796] | 99.9% |
| `FS3K` | cernuta pe trial inainte de test | **niciuna** | fr, ja | **0.688506** | +0.004642 | [+0.002619, +0.006756] | 100.0% |
| `FS3P` | cerută de Alexandru, 22 aug | pt | fr, ja | **0.687241** | +0.003396 | [+0.000679, +0.005997] | 99.3% |
| `FS3KP` | cerută de Alexandru, 22 aug | pt | fr, ja | **0.687604** | +0.003728 | [+0.001030, +0.006506] | 99.6% |

### Per limba, fata de sistemul de acum

| configuratie | ca | de | en | es | fil | fr | it | ja | pt | si |
|---|---|---|---|---|---|---|---|---|---|---|
| `FS` | -0.0021 | -0.0332 | -0.0198 | -0.0123 | -0.0227 | +0.0264 | -0.0107 | +0.0038 | -0.0229 | -0.0293 |
| `FSK` | -0.0004 | -0.0515 | -0.0198 | -0.0118 | -0.0219 | +0.0251 | -0.0107 | +0.0038 | -0.0225 | -0.0281 |
| `FS3` | +0.0035 | -0.0110 | +0.0024 | +0.0004 | +0.0032 | +0.0206 | -0.0011 | +0.0161 | -0.0006 | -0.0044 |
| `FS3K` | +0.0059 | -0.0055 | +0.0033 | +0.0007 | +0.0050 | +0.0208 | -0.0009 | +0.0166 | -0.0005 | +0.0012 |
| `FS3P` | +0.0086 | -0.0079 | +0.0020 | -0.0024 | +0.0067 | +0.0229 | +0.0029 | +0.0177 | -0.0053 | -0.0111 |
| `FS3KP` | +0.0102 | +0.0010 | +0.0020 | -0.0079 | +0.0071 | +0.0228 | -0.0023 | +0.0151 | -0.0085 | -0.0021 |

Aceleasi diferente, cu intervalul lor, numai unde intervalul exclude zero:

| configuratie | limba | diferenta | CI 95% pereche |
|---|---|---|---|
| `FS` | de | -0.0332 | [-0.0517, -0.0141] |
| `FS` | en | -0.0198 | [-0.0353, -0.0040] |
| `FS` | fil | -0.0227 | [-0.0430, -0.0033] |
| `FS` | fr | +0.0264 | [+0.0062, +0.0466] |
| `FS` | pt | -0.0229 | [-0.0352, -0.0118] |
| `FS` | si | -0.0293 | [-0.0570, -0.0030] |
| `FSK` | de | -0.0515 | [-0.0705, -0.0320] |
| `FSK` | en | -0.0198 | [-0.0353, -0.0040] |
| `FSK` | fil | -0.0219 | [-0.0420, -0.0026] |
| `FSK` | fr | +0.0251 | [+0.0048, +0.0452] |
| `FSK` | pt | -0.0225 | [-0.0348, -0.0113] |
| `FSK` | si | -0.0281 | [-0.0553, -0.0032] |
| `FS3` | de | -0.0110 | [-0.0174, -0.0044] |
| `FS3` | fr | +0.0206 | [+0.0136, +0.0275] |
| `FS3` | ja | +0.0161 | [+0.0099, +0.0228] |
| `FS3K` | fr | +0.0208 | [+0.0137, +0.0282] |
| `FS3K` | ja | +0.0166 | [+0.0100, +0.0232] |
| `FS3P` | fr | +0.0229 | [+0.0148, +0.0314] |
| `FS3P` | ja | +0.0177 | [+0.0099, +0.0255] |
| `FS3P` | pt | -0.0053 | [-0.0103, -0.0006] |
| `FS3KP` | fr | +0.0228 | [+0.0150, +0.0311] |
| `FS3KP` | ja | +0.0151 | [+0.0070, +0.0222] |
| `FS3KP` | pt | -0.0085 | [-0.0146, -0.0026] |

## Verdict

Cel mai mare castig pe medie il da `FS3K`: r = 0.688506, adica +0.004642 fata de 0.683849, interval pereche [+0.002619, +0.006756], deci exclude zero, P(>0) = 100.0%. Limbi stricate cu interval care exclude zero: niciuna.

Configuratii care trec AMBELE conditii, adica interval pereche care exclude zero in sus si nicio limba stricata: `FS3K`.

Nu se adopta nimic aici. Cele patru configuratii sunt patru intervale pe aceleasi randuri de test, iar alegerea intre ele pe cifra de test e chiar bifurcatia declarata in `output/e_prioritate.md`.

