# Potrivirea ponderii pe trial fata de pe test, toate bratele

Generat 2026-08-18 01:00:01 de `fuse_ab.py --fit both`. Detaliile per brat in `output/e_fusion_<brat>_fitcmp.md`.

| brat B | limbi | r A | r B | w trial | fuziune, fit trial | w test | fuziune, fit test | test − trial | fata de 0.6571 |
|---|---|---|---|---|---|---|---|---|---|
| `qwen3-8b-4bit` | 10 | +0.5523 | +0.3740 | 0.43 | +0.5320 | 0.74 | **+0.5676** | +0.0356 | -0.0895 |
| `gemma4-12b-4bit` | 10 | +0.5523 | +0.6424 | 0.16 | +0.6573 | 0.30 | **+0.6616** | +0.0042 | +0.0045 |
| `lolo` | 10 | +0.5523 | +0.6322 | 0.22 | +0.6522 | 0.32 | **+0.6540** | +0.0018 | -0.0031 |

Reperul de comparatie e cel mai bun reper publicat pe test, G-Eval cu GPT-4o 0.6571. `lolo` e singurul brat care respecta protocolul si pe alegerea modelului: `gemma4-12b-4bit` peste tot ar fi o alegere care nu se poate face fara sa vezi testul.
