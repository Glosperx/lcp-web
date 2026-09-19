# Poarta de sanatate pentru semnalul C

Generat de `analysis_c_sanatate.py`. Trei probe pe TEXT BRUT, fara sablon de chat, fiindca asa se calculeaza surprisal-ul. Un model care pica poarta **nu poate furniza C**, indiferent cat de bun e semnalul lui B.

```
                     SANATOS  surprisal_mediu  ln_vocab uniform  tokeni_distincti degenerare ordonare  n_itemi
model                                                                                                         
qwen3-8b-4bit           True             5.02     11.93    True               8.0       True     True     30.0
qwen3-8b-8bit           True             4.78     11.93    True               8.0       True     True     30.0
qwen35-9b-4bit          True             5.73     12.42    True               8.0       True     True     29.0
qwen35-9b-8bit          True             5.39     12.42    True               8.0       True     True     29.0
gemma4-12b-4bit        False            23.95     12.48   False               1.0      False    False     30.0
gemma4-12b-8bit        False              NaN       NaN     NaN               NaN        NaN      NaN      NaN
llama31-8b-4bit         True             4.22     11.76    True               7.0       True     True     30.0
aya-expanse-8b-4bit     True             5.66     12.45    True              10.0       True     True     30.0
```

## Detalii

```
                                                        continuare                                                                                                                                                     detaliu_ordonare
model                                                                                                                                                                                                                                  
qwen3-8b-4bit          ' Paris. The capital of Italy is Rome. The'                                                                                                              Paris 0.79 < Bucharest 5.27; water 0.35 < granite 14.91
qwen3-8b-8bit          ' Paris. The capital of Italy is Rome. The'                                                                                                              Paris 0.66 < Bucharest 5.74; water 0.42 < granite 16.33
qwen35-9b-4bit          ' Paris.\nThe capital of France is Paris.'                                                                                                              Paris 0.65 < Bucharest 5.82; water 0.92 < granite 15.06
qwen35-9b-8bit          ' Paris.\nThe capital of France is Paris.'                                                                                                              Paris 0.56 < Bucharest 5.87; water 0.81 < granite 15.03
gemma4-12b-4bit                                       '1111111111'                                                                                                         Paris 23.06 < Bucharest 28.79; water 26.67 !>= granite 25.96
gemma4-12b-8bit                                                NaN  EROARE: ValueError: Received 11 parameters not in model: \nvision_embedder.patch_dense.bias,\nvision_embedder.patch_dense.biases,\nvision_embedder.patch_dense.scal
llama31-8b-4bit      ' Paris. The capital of France is Paris. The'                                                                                                              Paris 0.81 < Bucharest 5.44; water 0.66 < granite 13.42
aya-expanse-8b-4bit   ' Paris. It is located in the north-central'                                                                                                             Paris 1.17 < Bucharest 12.75; water 1.17 < granite 13.30
```

**Sanatoase: 6 din 8.** Modele care NU pot furniza C: ['gemma4-12b-4bit', 'gemma4-12b-8bit'].

Pragul `uniform` e ln(|V|), adica surprisal-ul unei distributii uniforme. Nu e un prag de calitate, e granita imposibilului: un model peste ea e mai prost decat zarul.

