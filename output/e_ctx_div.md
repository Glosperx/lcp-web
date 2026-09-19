# Diversitate contextuala, din Wikipedia

Generat de `build_ctx_div.py`. In cate DOCUMENTE distincte apare cuvantul, normalizat ca rata, pe aceeasi scara ca `zipf`. Sursa: `wikimedia/wikipedia`, dump 20231101, un shard per limba pentru cele opt mari si dump-ul intreg pentru `si` si `fil`.

```
     wiki  documente   tipuri  tinte  acoperite  acoperire
lang                                                      
ca     ca     184353   484700    445        404       90.8
de     de     142266  1345184    570        536       94.0
en     en     156289   438554    570        564       98.9
es     es     141628   602555    593        587       99.0
fr     fr     150862   642330    569        557       97.9
it     it     183364   569866    570        542       95.1
ja     ja      92632  1619738    570        315       55.3
pt     pt     185375   459833    567        550       97.0
si     si      23065   179185    600        525       87.5
fil    tl      45341   148515    570        471       82.6
```

`acoperire` e procentul tintelor de test gasite ca forma EXACTA in tabel. Fara backoff: diversitatea contextuala a unui prefix nu e diversitatea cuvantului, iar `build_freq_tail` a masurat deja ca backoff-ul pe prefix pierde pe filipineza (-0.0097), care foloseste infixe si reduplicare.

