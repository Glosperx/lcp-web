# Studiu ET ortogonal — cifre (proza o scrie omul, fara LLM)

## Acoperire
Acoperire ET pe test: 1509/1587 (95.1%) au fixatii.
Cuvinte FARA ET (n=78): zipf mediu 4.45 vs 4.20 (cu ET); lungime 6.91 vs 7.57. => ET lipseste sistematic la cuvinte mai frecvente/scurte (skipped) = bias de acoperire.
GROUND-TRUTH: doar 2/14 cuvinte etichetate au ET => imposibil de validat ET->complexitate pe etichete reale. Folosim predictia (exp_surp_w08, public 64.81) ca proxy de complexitate pe cele 1509 cu ET.

## ET proxy
corr(et_proxy, zipf)=-0.555; corr(et_proxy, predictie)=0.622; corr(et_proxy, surprisalC)=0.188

## Ortogonalitate per metrica
```
            et_metric group  corr_vs_pred_raw  corr_vs_pred_ctrl_freqlen  corr_vs_surprisalC_raw  corr_vs_surprisalC_ctrl    n
  et_complexity_proxy proxy            0.6221                     0.3336                  0.1878                   0.1722 1509
        FFD_mean_norm early            0.4393                     0.1955                  0.0770                   0.0341 1509
       FPRT_mean_norm early            0.5942                     0.2400                  0.0888                   0.0497 1509
       skip_rate_norm early           -0.3569                    -0.1535                 -0.0396                  -0.1238 1509
  ffd_fprt_ratio_norm early           -0.5538                    -0.2410                 -0.0525                  -0.0686 1509
        RRT_mean_norm  late            0.5084                     0.2832                  0.2190                   0.1737 1509
     TRC_in_mean_norm  late            0.1750                     0.1478                  0.2626                   0.2363 1509
 refixation_rate_norm  late            0.3093                     0.2420                  0.2081                   0.1672 1509
tft_per_fixation_norm  late            0.5486                     0.2992                  0.2300                   0.1309 1509
        TFT_mean_norm other            0.6258                     0.3161                  0.1741                   0.1415 1509
        TFC_mean_norm other            0.5755                     0.2914                  0.1287                   0.1353 1509
       FPFC_mean_norm other            0.5258                     0.1812                  0.0206                   0.0216 1509
         TFT_std_norm other            0.5621                     0.2768                  0.1708                   0.1477 1509
         FFD_std_norm other            0.3443                     0.1839                  0.2217                   0.1238 1509
          TFT_cv_norm other            0.0630                     0.0437                  0.0522                   0.0617 1509
```

## Timpuriu vs tarziu
```
       corr_vs_pred_raw  corr_vs_pred_ctrl_freqlen  corr_vs_surprisalC_raw  corr_vs_surprisalC_ctrl
group                                                                                              
early            0.0307                     0.0103                  0.0184                  -0.0271
late             0.3853                     0.2430                  0.2299                   0.1770
```

## Ground-truth (14)
Pe cele 14 etichete: corr(zipf, complexity)=0.092 (n=14). corr(ET, complexity) NU se poate (doar 2 au ET).
