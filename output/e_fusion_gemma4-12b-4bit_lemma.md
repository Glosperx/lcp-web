# Fuziunea A plus B, brat `gemma4-12b-4bit`

Generat 2026-08-18 10:24:53 de `fuse_ab.py --arm gemma4-12b-4bit`. Date brute: `output/fusion_gemma4-12b-4bit_lemma.csv`, predictii per instanta in `output/fusion_preds_gemma4-12b-4bit_lemma.csv`.

Ponderea w e aleasa leave-one-language-out pe TRIAL, apoi aplicata pe TEST. Pentru limba L, w maximizeaza r mediu peste celelalte 9 limbi de trial. Nu vede nici limba L, nici testul. Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la transformari afine, asta nu schimba nimic pentru A singur sau B singur.

Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.

## Rezultatul pe test

| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | `gemma4-12b-4bit` | 445 | 150 | 0.20 | +0.4470 | +0.4829 | **+0.5161** | [+0.4498, +0.5788] | +0.0691 | [+0.0016, +0.1397] | +0.0332 | [+0.0169, +0.0490] |
| de | `gemma4-12b-4bit` | 570 | 193 | 0.15 | +0.6551 | +0.6544 | **+0.6898** | [+0.6479, +0.7292] | +0.0346 | [-0.0097, +0.0810] | +0.0353 | [+0.0274, +0.0436] |
| en | `gemma4-12b-4bit` | 570 | 190 | 0.15 | +0.8147 | +0.8377 | **+0.8549** | [+0.8231, +0.8823] | +0.0402 | [+0.0126, +0.0700] | +0.0172 | [+0.0121, +0.0232] |
| es | `gemma4-12b-4bit` | 593 | 208 | 0.15 | +0.6686 | +0.7432 | **+0.7519** | [+0.7136, +0.7878] | +0.0833 | [+0.0503, +0.1172] | +0.0088 | [+0.0034, +0.0145] |
| fil | `gemma4-12b-4bit` | 568 | 553 | 0.10 | +0.4091 | +0.5190 | **+0.5228** | [+0.4571, +0.5846] | +0.1137 | [+0.0589, +0.1676] | +0.0038 | [-0.0015, +0.0097] |
| fr | `gemma4-12b-4bit` | 566 | 191 | 0.20 | +0.5305 | +0.6457 | **+0.6531** | [+0.5975, +0.7027] | +0.1226 | [+0.0790, +0.1710] | +0.0074 | [-0.0029, +0.0182] |
| it | `gemma4-12b-4bit` | 562 | 192 | 0.20 | +0.6336 | +0.6106 | **+0.6409** | [+0.5951, +0.6868] | +0.0074 | [-0.0302, +0.0450] | +0.0303 | [+0.0205, +0.0403] |
| ja | `gemma4-12b-4bit` | 570 | 190 | 0.25 | +0.4890 | +0.7676 | **+0.7810** | [+0.7386, +0.8164] | +0.2921 | [+0.2404, +0.3498] | +0.0134 | [-0.0003, +0.0267] |
| pt | `gemma4-12b-4bit` | 562 | 557 | 0.20 | +0.7705 | +0.8222 | **+0.8360** | [+0.8027, +0.8638] | +0.0656 | [+0.0375, +0.0935] | +0.0138 | [+0.0071, +0.0207] |
| si | `gemma4-12b-4bit` | 600 | 578 | 0.20 | +0.2119 | +0.3407 | **+0.3480** | [+0.2962, +0.3994] | +0.1361 | [+0.0771, +0.1963] | +0.0073 | [-0.0063, +0.0214] |
| **medie** | | | | 0.18 | +0.5630 | +0.6424 | **+0.6594** | | +0.0965 | | +0.0171 | |

Fuziunea bate A pe 10 din 10 limbi si B pe 10 din 10. Intervalul exclude zero pe 8 limbi fata de A si pe 6 fata de B.

## Fata de reperele publicate, toate pe test

| sistem | r mediu pe 10 limbi |
|---|---|
| baseline frecventa | 0.4775 |
| Archaeology | 0.4864 |
| TMU-HIT | 0.6538 |
| G-Eval cu GPT-4o | 0.6571 |
| semnalul A singur, bratul inghetat | 0.5630 |
| semnalul B singur, `gemma4-12b-4bit` | 0.6424 |
| **fuziunea A plus B, w ales LOLO** | **0.6594** |

Fata de cel mai bun reper publicat, 0.6571: **+0.0023**. Trecem de el.

## Ponderea aleasa

Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.

| limba | w | r minim pe curba | r maxim pe curba | latime |
|---|---|---|---|---|
| ca | 0.20 | +0.5601 | +0.7044 | 0.1443 |
| de | 0.15 | +0.5084 | +0.6861 | 0.1777 |
| en | 0.15 | +0.5148 | +0.7042 | 0.1894 |
| es | 0.15 | +0.5082 | +0.7048 | 0.1966 |
| fil | 0.10 | +0.5295 | +0.7111 | 0.1816 |
| fr | 0.20 | +0.5629 | +0.7227 | 0.1598 |
| it | 0.20 | +0.5220 | +0.7017 | 0.1797 |
| ja | 0.25 | +0.5541 | +0.6975 | 0.1434 |
| pt | 0.20 | +0.5059 | +0.6884 | 0.1825 |
| si | 0.20 | +0.5913 | +0.7706 | 0.1793 |
