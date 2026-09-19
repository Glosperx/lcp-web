---
name: coada-frecventa-masurata
description: "23 aug 2026 - tabel de frecventa din Wikipedia duce sinhaleza de la 0 la 89.8% acoperire dar PIERDE pe fuziune; si doua descoperiri neasteptate: pe filipineza frecventa strica activ (+0.0225 daca se scoate) si pe sinhaleza dauneaza dependenta celorlalte limbi de ea"
metadata:
  type: project
---

Masurat **23 august 2026**. `build_freq_tail.py`, `analysis_coada.py` -> `output/e_coada.md`,
`output/e_freq_tail.md`. Corpusuri: `wikimedia/wikipedia` 20231101, si 8.03M tokeni / 491k tipuri,
tl 12.27M / 377k.

## Acoperirea se repara, cifra nu

```
limba   inainte              exact   plus prefix   plus subword
si      0 din 600            89.8%   99.7%         100%
fil     418 din 570 (73.3%)  90.0%   97.7%         100%
```

Pe bratul A sinhaleza urca cu +0.0147 la treapta `prefix`. **Pe fuziune toate trei treptele PIERD**:
-0.0021, -0.0009, -0.0009 fata de xlmr singur, si sinhaleza chiar scade (0.4095 -> 0.4025).
In ansamblu de trei: 0.6813 / 0.6823 / 0.6821, toate sub sistemul de 0.683849.

Predictia tipologica scrisa INAINTE in docstring s-a confirmat: backoff-ul pe prefix e motivat pentru
sinhaleza (aglutinanta, sufixeaza) si nu pentru tagalog (infixe, reduplicare). Masurat: si +0.0147,
fil **-0.0097**, si cu cat backoff-ul e mai agresiv cu atat pierde mai mult.

## Cele doua lucruri neasteptate, si sunt mai valoroase decat cifra

1. **Pe filipineza coloana de frecventa STRICA activ.** Ablatia `--no-freq` urca fuziunea filipinezei
   cu **+0.0225, CI [+0.0060, +0.0381], P = 99.5%**. E singura limba unde scoaterea ajuta
   semnificativ (4 limbi sunt stricate). Are 152 din 570 de tinte cu zipf 0, de patru ori mai mult
   decat urmatoarea. **Indicatorul de OOV per token NU repara** (0.678914 singur, 0.683647 in
   ansamblu, ambele sub referinta), deci mecanismul nu e "confunda rar cu negasit". Ramane deschis.
2. **Pe sinhaleza, scoaterea frecventei din CELELALTE noua limbi urca bratul A cu +0.0243.** Un model
   antrenat pe limbi care AU frecventa se sprijina pe o trasatura pe care sinhaleza n-o poate furniza.
   Problema cozii nu e doar coloana lipsa, e dependenta invatata in alta parte.

Plafonul: frecventa valoreaza +0.0597 pe bratul A al celor opt limbi care o au.

## Capcane platite

- `re.findall(r"[^\W\d_]+")` **sparge cuvintele sinhaleze in consoane**: `\w` din Python nu cuprinde
  semnele vocalice (categoria Mn). Se foloseste `regex` cu `[\p{L}\p{M}]`, care pastreaza si ZWJ.
- Controlul "celelalte opt limbi neatinse" trebuie facut **constient de NaN**: `ja` si `si` au
  coloanele de suprafata NaN si `!=` le raporteaza schimbate la fiecare rulare. Corect: 0 din 14082.
- Podeaua de rezolutie: cu 8.03M tokeni, un cuvant care apare o data primeste zipf 2.10, deci
  sinhaleza nu poate cobori sub atat, pe cand celelalte opt ajung la 0.

Vezi [[prioritate-contributie-si-drumul-la-07]] si [[transmisia-a-fuziune-masurata]].
