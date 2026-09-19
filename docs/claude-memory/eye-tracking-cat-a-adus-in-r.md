---
name: eye-tracking-cat-a-adus-in-r
description: Eye-tracking-ul a adus +0.0067 in r pe romana, nu "+0.84"; conversia compozit-r e exacta si inchide V4 cu o masuratoare proprie
metadata:
  type: project
---

Verdictul V4 (nu intra ca semnal) **rezista**, dar argumentul lui de ordin de marime era scris in
unitatea gresita. Cele "+0.84" din README sunt compozit de competitie, nu r, care e metrica lucrarii
multilingve.

**Conversia e exacta**, fiindca calibrarea romaneasca e fixa, `clip(0.27 + 0.125*z, 0, 1)` la
`solution_bert.py:875`, deci predictia are mereu aceeasi medie si deviatie indiferent de ponderi.
Cu gold RoLCP `mu_y = 0.2701`, `sd_y = 0.1674`:

    R2 = 2*r*(sd_p/sd_y) - (sd_p/sd_y)^2 - ((mu_y-mu_p)/sd_y)^2
    compozit = 50*(r + R2) = 124.67*r - 27.88

Se valideaza pe ea insasi: r = 0.7770 da R2 = 0.6028, exact ce tipareste `score_rolcp.py`.
**Un punct de compozit = 0.0080 in r.** Deci:

| pas | compozit | r derivat | delta r |
|---|---|---|---|
| A+B+C fara fix de lema | 64.81 | 0.7435 | |
| + fix de lema | 68.90 | 0.7763 | **+0.0328** |
| + eye-tracking | 69.74 | 0.7830 | **+0.0067** |

Fixul de lema a adus de cinci ori mai mult decat privirea. Si +0.0067 e **plafonul**, nu estimarea:
gaze real, 95 de participanti, peste exact aceleasi texte, 95.1% acoperire, lookup per token, iar
w_ET = 0.20 a fost ales pe scorul public.

Trei lucruri masurate in plus, 18 august 2026:
- `data/train_et.csv` (585.573 randuri, 95 participanti, 10 texte) **e setul MultiplEYE romanesc**,
  dupa numele stimulilor (Arg_PISACowsMilk, PopSci_MultiplEYE). Exact ce au folosit Kuvshynova et al.
- Semnalul chiar e ortogonal, corr 0.334 cu predictia dupa control pe frecventa si lungime. Deci
  ortogonalitatea nu e constrangerea care leaga.
- Conditia de rasturnare din V4, "+0.5", e scara de compozit, adica +0.004 in r, sub latimea
  propriului nostru bootstrap. **Reformulata la +0.02 in r pe cel putin doua limbi non-romane.**

**INCHIS DEFINITIV, 18 august 2026.** Ultima poarta, privirea ca **tinta de transfer** in loc de
trasatura, a fost rulata: `analysis_et_distill.py` -> `output/e_et_distill.md`, 101 secunde. Se
prezice TRT-ul romanesc (`TFT_mean_norm`, 1509 randuri, 10 texte, 263 contexte) din (lungime, zipf)
si separat din (lungime, zipf, embedding XLM-R), leave-one-text-out, cu `blend_ridge_hgb` neschimbat.

| brat | r out-of-fold pe TRT |
|---|---|
| lungime + frecventa, 2 coloane | +0.6262 |
| embedding singur, 768 coloane | **+0.5167** |
| amandoua, 770 coloane | +0.6222 |

Incrementul embeddingului e **-0.0040**, CI pereche pe contexte [-0.0303, +0.0226], P(>0) = 39.4%.
Aceeasi concluzie pe FFD (+0.0129) si pe compozitul ET (+0.0081), amandoua cu CI care include zero.
**Embeddingul singur prezice privirea mai PROST decat doua coloane lexicale**, deci un predictor de
privire distilat peste el nu poate purta nimic ce semnalul A nu poarta deja. Calea moare cu doua
masuratori proprii, nu cu o citare. Nu se mai deschide.

Provenienta tintei e verificata, fiindca codul care a scris `data/X_test.csv` nu mai e in repo:
reagregarea independenta a lui `TFT` din `data/train_et.csv` da r = 0.9869 brut si 0.9933 doar pe
fixari, pe cele 1336 de randuri legabile pe (text, cuvant).

`data/RoLCP.csv` NU mai e pe disc; comanda de readucere e in docstringul lui `score_rolcp.py`.
Vezi si [[rals-rolcp-datele-sunt-ale-lui-nisioi]], [[fixul-de-lema-multilingv-masurat]].
