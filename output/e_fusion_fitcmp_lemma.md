# Potrivirea ponderii pe trial fata de pe test, toate bratele

Generat 2026-08-18 10:24:53 de `fuse_ab.py --fit both`. Detaliile per brat in `output/e_fusion_<brat>_fitcmp.md`.

| brat B | limbi | r A | r B | w trial | fuziune, fit trial | w test | fuziune, fit test | test − trial | fata de 0.6571 |
|---|---|---|---|---|---|---|---|---|---|
| `gemma4-12b-4bit` | 10 | +0.5630 | +0.6424 | 0.18 | +0.6594 | 0.33 | **+0.6634** | +0.0039 | +0.0063 |
| `lolo` | 10 | +0.5630 | +0.6322 | 0.25 | +0.6564 | 0.35 | **+0.6568** | +0.0003 | -0.0003 |

Reperul de comparatie e cel mai bun reper publicat pe test, G-Eval cu GPT-4o 0.6571. `lolo` e singurul brat care respecta protocolul si pe alegerea modelului: `gemma4-12b-4bit` peste tot ar fi o alegere care nu se poate face fara sa vezi testul.
