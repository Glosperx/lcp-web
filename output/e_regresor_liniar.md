# Axa LINIARA a semnalului A, pe toate encoderele

Generat de `analysis_regresor_multi.py`. Coloana `p_multi`, splitul test, configuratia `--lemma-freq --afeat fert_inloc`. Bratul B nu intra nicaieri.

Jumatatea liniara a blend-ului a fost `Ridge(alpha=300)` in absolut toate variantele masurate vreodata pe axa regresorului; tot ce s-a schimbat pana acum a fost jumatatea de arbori. Aici se schimba liniarul, cu ACELASI partener `hgb` si pe ACELASI encoder.

Controlul, per encoder, e `ridge+hgb` ca medie standardizata:

```
  xlmr   0.575296   (10 limbi)
  e5     0.571931   (10 limbi)
  labse  0.574504   (10 limbi)
```

Bara pe fuziune e +0.0045 si factorul de transmisie A -> fuziune e 0.259 mediu, deci un candidat trebuie sa urce A cu +0.0174 ca sa fie chiar si optimist adoptabil.

## delta pe A fata de `ridge+hgb`, per encoder

`sus` e pe cate encodere din `n` diferenta e pozitiva. Trei din trei la +0.002 e un efect; unu din trei la +0.006 e o loterie cu trei bilete.

```
  candidat              xlmr        e5     labse     medie   sus
  lasso-a1e-3        +0.0015   +0.0043   +0.0028   +0.0029   3/3
  lasso-a3e-4        +0.0006   +0.0027   +0.0031   +0.0022   3/3
  ridge-a1000        +0.0001   +0.0011   +0.0014   +0.0009   3/3
  bayesridge         -0.0001   +0.0008   +0.0008   +0.0005   2/3
  lasso-a1e-4        -0.0002   -0.0000   +0.0004   +0.0000   1/3
  ridge              +0.0000   +0.0000   +0.0000   +0.0000   <- controlul
  pls-k16            +0.0003   -0.0004   -0.0006   -0.0002   1/3
  ridge-a3000        -0.0022   +0.0001   +0.0004   -0.0006   2/3
  ridge-a100         -0.0005   -0.0009   -0.0012   -0.0009   0/3
  ridge-a30          -0.0009   -0.0014   -0.0018   -0.0014   0/3
  huber              -0.0016   -0.0014   -0.0013   -0.0014   0/3
  pls-k64            -0.0011   -0.0017   -0.0021   -0.0016   0/3
  pls-k32            -0.0010   -0.0017   -0.0028   -0.0018   0/3
  lasso-a3e-3        -0.0019   -0.0008   -0.0032   -0.0020   0/3
  pls-k8             -0.0031   -0.0045   -0.0019   -0.0032   0/3
  svr-lin            -0.0057   -0.0023   -0.0065   -0.0048   0/3
  elasticnet         -0.0032   -0.0063   -0.0065   -0.0053   0/3
  ridge-a10000       -0.0085   -0.0048   -0.0046   -0.0060   0/3
  krr-rbf            -0.0050   -0.0043   -0.0122   -0.0072   0/3
  extratrees         -0.0061   -0.0075   -0.0102   -0.0079   0/3
  lasso              -0.0061   -0.0151   -0.0098   -0.0103   0/3
  ridge-a30000       -0.0163   -0.0117   -0.0116   -0.0132   0/3
  pls-k4             -0.0159   -0.0113   -0.0130   -0.0134   0/3
  ard                -0.0159   -0.0135   -0.0159   -0.0151   0/3
  hgb-adanc          -0.0309         -         -   -0.0309   0/1
  lasso-a3e-2        -0.0317   -0.0316   -0.0344   -0.0326   0/3
```

Candidatii pozitivi pe TOATE encoderele pe care s-au rulat:

```
  lasso-a1e-3      medie +0.0029   fuziune implicata +0.0007 (optimist)
  lasso-a3e-4      medie +0.0022   fuziune implicata +0.0006 (optimist)
  ridge-a1000      medie +0.0009   fuziune implicata +0.0002 (optimist)
```

Bara e +0.0045 pe fuziune. Cei care o trec chiar si pe estimarea optimista: **niciunul**.

## rho fata de `hgb`, per encoder

Podeaua de rho de 0.80 n-a fost coborata de niciun candidat NELINIAR. Intrebarea acestei sesiuni a fost daca un liniar rar (L1) o coboara, fiindca are alt bias inductiv decat unul dens (L2). `ridge` e reperul.

```
  candidat              xlmr        e5     labse
  ridge                0.811     0.799     0.770   <- reperul
  ard                  0.787     0.776     0.775
  bayesridge           0.822     0.804     0.776
  elasticnet           0.870     0.852     0.823
  extratrees           0.914     0.884     0.866
  hgb-adanc            0.951         -         -
  huber                0.801     0.797     0.760
  krr-rbf              0.771     0.748     0.726
  lasso                0.855     0.824     0.815
  lasso-a1e-3          0.858     0.846     0.814
  lasso-a1e-4          0.813     0.805     0.774
  lasso-a3e-2          0.739     0.783     0.778
  lasso-a3e-3          0.871     0.857     0.827
  lasso-a3e-4          0.831     0.823     0.791
  pls-k16              0.804     0.793     0.767
  pls-k32              0.799     0.793     0.758
  pls-k4               0.803     0.745     0.731
  pls-k64              0.799     0.793     0.758
  pls-k8               0.799     0.775     0.755
  ridge-a100           0.804     0.796     0.764
  ridge-a1000          0.822     0.803     0.777
  ridge-a10000         0.829     0.782     0.759
  ridge-a30            0.800     0.794     0.760
  ridge-a3000          0.830     0.799     0.774
  ridge-a30000         0.815     0.759     0.736
  svr-lin              0.793     0.783     0.747
```

`rho(ridge, hgb)` e 0.811, 0.799, 0.770 pe cele 3 encodere. Candidati cu rho STRICT mai mic pe toate: `huber`, `krr-rbf`, `pls-k16`, `pls-k32`, `pls-k4`, `pls-k64`, `pls-k8`, `ridge-a100`, `ridge-a30`, `svr-lin`.

## Grilele parametrice, punctul cel mai bun pe fiecare encoder

Aici e doar cine iese in fata pe fiecare encoder, ca sa se vada daca optimul e STABIL. Selectia onesta, leave-one-language-out, plus latimea criteriului, e in rapoartele per encoder (`e_regresor_a.md`, `e_regresor_a_e5.md`, `e_regresor_a_labse.md`).

```
  ridge (alpha)
    xlmr   cel mai bun `ridge-a1000` la +0.0001   ridge-a30=-0.0009 ridge-a100=-0.0005 ridge=+0.0000 ridge-a1000=+0.0001 ridge-a3000=-0.0022 ridge-a10000=-0.0085 ridge-a30000=-0.0163
    e5     cel mai bun `ridge-a1000` la +0.0011   ridge-a30=-0.0014 ridge-a100=-0.0009 ridge=+0.0000 ridge-a1000=+0.0011 ridge-a3000=+0.0001 ridge-a10000=-0.0048 ridge-a30000=-0.0117
    labse  cel mai bun `ridge-a1000` la +0.0014   ridge-a30=-0.0018 ridge-a100=-0.0012 ridge=+0.0000 ridge-a1000=+0.0014 ridge-a3000=+0.0004 ridge-a10000=-0.0046 ridge-a30000=-0.0116
  lasso (alpha)
    xlmr   cel mai bun `lasso-a1e-3` la +0.0015   lasso-a1e-4=-0.0002 lasso-a3e-4=+0.0006 lasso-a1e-3=+0.0015 lasso-a3e-3=-0.0019 lasso=-0.0061 lasso-a3e-2=-0.0317
    e5     cel mai bun `lasso-a1e-3` la +0.0043   lasso-a1e-4=-0.0000 lasso-a3e-4=+0.0027 lasso-a1e-3=+0.0043 lasso-a3e-3=-0.0008 lasso=-0.0151 lasso-a3e-2=-0.0316
    labse  cel mai bun `lasso-a3e-4` la +0.0031   lasso-a1e-4=+0.0004 lasso-a3e-4=+0.0031 lasso-a1e-3=+0.0028 lasso-a3e-3=-0.0032 lasso=-0.0098 lasso-a3e-2=-0.0344
  pls (k)
    xlmr   cel mai bun `pls-k16` la +0.0003   pls-k4=-0.0159 pls-k8=-0.0031 pls-k16=+0.0003 pls-k32=-0.0010 pls-k64=-0.0011
    e5     cel mai bun `pls-k16` la -0.0004   pls-k4=-0.0113 pls-k8=-0.0045 pls-k16=-0.0004 pls-k32=-0.0017 pls-k64=-0.0017
    labse  cel mai bun `pls-k16` la -0.0006   pls-k4=-0.0130 pls-k8=-0.0019 pls-k16=-0.0006 pls-k32=-0.0028 pls-k64=-0.0021
```

## Cele doua brate ale lui A sunt INDEPENDENTE

Tot ce e mai sus e pe `p_multi`. Dar semnalul A al sistemului nu e `p_multi`, e `z(w_src . z(p_en) + (1 - w_src) . z(p_multi))`, cu `w_src` ales LOLO. Deci un candidat trebuie sa tina pe AMBELE coloane, si aici nu tine niciunul.

`p_en` e o SINGURA potrivire care prezice zece limbi nevazute; `p_multi` e o potrivire per limba, cu noua limbi de test in antrenare. Doua regimuri diferite, deci nu e de la sine inteles ca vor acelasi regresor, si masuratoarea de mai jos spune ca intr-adevar nu se informeaza reciproc.

```
  candidat            p_multi   sus         p_en   sus
  lasso-a1e-3         +0.0029   3/3      -0.0030   0/3
  lasso-a3e-4         +0.0022   3/3      -0.0007   1/3
  ridge-a1000         +0.0009   3/3      +0.0035   3/3
  bayesridge          +0.0005   2/3      +0.0026   3/3
  lasso-a1e-4         +0.0000   1/3      -0.0024   0/3
  ridge               +0.0000   0/3      +0.0000   0/3   <- controlul
  pls-k16             -0.0002   1/3      -0.0022   1/3
  ridge-a3000         -0.0006   2/3      +0.0045   3/3
  ridge-a100          -0.0009   0/3      -0.0027   0/3
  ridge-a30           -0.0014   0/3      -0.0043   0/3
  huber               -0.0014   0/3      -0.0072   0/3
  pls-k64             -0.0016   0/3      -0.0051   0/3
  pls-k32             -0.0018   0/3      -0.0052   0/3
  lasso-a3e-3         -0.0020   0/3      -0.0064   0/3
  pls-k8              -0.0032   0/3      +0.0007   1/3
  svr-lin             -0.0048   0/3      -0.0129   0/3
  elasticnet          -0.0053   0/3      -0.0091   0/3
  ridge-a10000        -0.0060   0/3      +0.0017   3/3
  krr-rbf             -0.0072   0/3      +0.0013   1/3
  extratrees          -0.0079   0/3      -0.0029   1/3
  lasso               -0.0103   0/3      -0.0140   0/3
  ridge-a30000        -0.0132   0/3      -0.0039   0/3
  pls-k4              -0.0134   0/3      -0.0045   0/3
  ard                 -0.0151   0/3      -0.0164   0/3
  hgb-adanc           -0.0309   0/1      -0.0076   0/1
  lasso-a3e-2         -0.0326   0/3      -0.0148   0/3
```

Corelatia intre cele doua coloane de delta, peste 26 candidati: **+0.564**. Dar cifra asta e inselatoare: candidatii catastrofali sunt prosti pe AMBELE brate si fabrica singuri o corelatie pozitiva care spune numai `prost e prost peste tot`. Restransa la banda in care s-ar putea alege ceva:

```
  |delta| <= 0.010   n=19   pearson +0.130
  |delta| <= 0.005   n=11   pearson -0.041
```

Adica in banda utila cele doua brate sunt **independente**: cat ajuta un candidat pe un brat nu spune practic nimic despre celalalt. Nu se cer lucruri contrare, dar nici nu se ajuta, si de asta cel mai bun pe `p_multi` (`lasso-a1e-3`, +0.0029) iese NEGATIV pe `p_en` (-0.0030), iar cel mai bun pe `p_en` (`ridge-a3000`, +0.0045) iese usor negativ pe `p_multi` (-0.0006).

Pozitivi pe 3/3 encodere pe AMBELE brate: `ridge-a1000`.

Consecinta practica, si e parghia pe care nicio configuratie de pana acum n-o foloseste: `p_en` si `p_multi` sunt COLOANE separate in CSV, deci alpha se poate alege pe brat, nu pe model. Asta se masoara mai jos ca `lin_A7` si `lin_A8`.

## Fuziunea REALA cu semnalul B, pentru ansamblurile de top

`--arm lolo --fit test --pick-split test`, acelasi B (M3K) peste tot, numai A variaza. Diferenta e PEREACHE: aceeasi reesantionare pe ambele configuratii, deci intervalul e al diferentei. `P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste control.

```
  ce                                       spatiu      control     nou    delta   P(>0)
  mean(lasso-a1e-3, hgb)                   xlmr         0.6828  0.6834  +0.0006   60.6%
  mean(hgb, extratrees, pls-k16)           xlmr         0.6828  0.6839  +0.0011   68.5%
  mean(lasso-a1e-3, lasso-a3e-4, hgb)      xlmr         0.6828  0.6828  +0.0000   51.3%
  mean(lasso-a1e-3, hgb, tabfm@256)        hibrid       0.6827  0.6830  +0.0003   58.1%
  encmean(mean(lasso-a1e-3, hgb)) + ens    3 encodere   0.6900  0.6887  -0.0013   28.0%
  encmean(mean(ridge-a1000, hgb)) + ens    3 encodere   0.6900  0.6896  -0.0004   53.8%
  p_en de la ridge-a3000, p_multi neatins  3 encodere   0.6900  0.6900  -0.0000   60.7%
  p_en ridge-a3000 + p_multi lasso-a1e-3   3 encodere   0.6900  0.6904  +0.0004   67.2%
```

Bara pe fuziune e +0.0045. **Niciuna nu o trece.** Cea mai mare diferenta e +0.0011 (`mean(hgb, extratrees, pls-k16)`), la P(>0) 68.5%, adica o moneda.

Pe drumul care conteaza pentru sistem, media a trei encodere cu `--ens`, 1 din 4 configuratii ies peste controlul adoptat, si cea mai buna dintre ele e +0.0004 la P(>0) 67.2%. Nicio adoptare nu se sprijina pe asta.

Cifra care duce toata concluzia nu e nici una din diferentele de fuziune, e raportul dintre ele si castigul pe A: A urca de la 0.5993 la 0.6023, adica +0.0030 constant si reproductibil pe toate trei encoderele, si fuziunea nu se misca. **Transmisia pe axa asta e ~zero**, fata de 0.09-0.26 masurat in general. Un castig pe A care nu ajunge in fuziune e al cincilea caz de acest fel in proiect.

