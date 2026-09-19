---
name: alinierea-tinta-subword-masurata
description: Cum se aleg subword-urile țintei (suprapunere de offset-uri, nu word_ids) plus măsurătorile pe tokenizere și pe ambiguitatea span-ului
metadata:
  node_type: memory
  type: reference
---

Măsurat pe **20 august 2026**, în `envs/ml_def` (transformers 5.13.1), pentru o întrebare a lui Nisioi.
Nimic din cifrele de mai jos nu e în `output/`.

## Mecanismul, ca să nu fie descris greșit

`XLMR.embed_frame`, [solution_bert.py:308](solution_bert.py#L308), selectează prin **suprapunere de
intervale de caractere**, nu prin cuvinte:

```python
tgt = [j for j, (a, b) in enumerate(offs) if b > a and a < ce and b > cs]
```

`b > a` aruncă token-urile speciale, care au offset (0,0). **`word_ids()` nu e folosit nicăieri** în
proiect, deși există și funcționează. Descrierea „se sparge propoziția în cuvinte și se mapează
token-urile" e a lui `word_ids()`, deci e greșită pentru acest cod. Contează: pe japoneză, 570 din 570
de instanțe, nu există cuvinte separate de spații.

## Offset-urile diferă între tokenizere, iar regula de suprapunere e ce le acoperă

Pe „Prevalenta afectiunilor cardiovasculare creste.", țintă `afectiunilor`, span (11,23):

- **multilingual-e5 / XLM-R**: `▁afectiuni` la (11,20), `lor` la (20,23). Exclude spațiul, span exact.
- **Gemma 4**: `▁afect` la **(10,16)**, deci include spațiul din față.
- **Qwen3-8B**: `Ġafect` la (10,16), la fel.
- **Qwen3-8B pe sinhaleză**: byte fallback, 37 de token-uri pentru 26 de caractere, și **mai multe
  token-uri cu offset identic**, de exemplu (1,2) de două ori.

O regulă de tip „offset egal cu span-ul" ar fi picat tăcut pe Gemma și Qwen. Intersecția le trece pe
toate. Legat de [[fertilitate-tokenizere-masurata]].

## `return_offsets_mapping` nu mai e o restricție în env-ul curent

Cerea un tokenizer fast (backend Rust); pe unul lent, transformers 4.x ridica `NotImplementedError`.
Măsurat: în **transformers 5.13.1, `use_fast=False` întoarce tot `is_fast=True`**, deci tokenizerele
lente nu mai există și toate cele 4 encodere din `ENCODERS` merg. Atenție: antetul lui
[recompute_gpu.py:15](recompute_gpu.py#L15) declară `transformers==4.46.3`, unde distincția ar conta.

## Ambiguitatea span-ului, pe testul MLSP (n = 5624)

- **span negăsit: 0**, după fixul de caz din `find_char_span`.
- **88 de instanțe (1.6%)** au ținta de mai multe ori în context, iar `text.find` ia prima apariție.
  Datele MLSP nu dau indexul, doar șirul, deci nu se poate repara fără altă sursă. Exemplu: `sobreoferta`,
  de două ori în același context catalan.
- Span care **se termină în interiorul unui cuvânt scris**: ja 558/570 (normal, fără spații),
  si 37/600 (sufixe aglutinate, ex. ținta `හස්තියා` continuată cu `ග`), și doar **6 în limbile latine**
  (en 1, es 1, pt 4).

**How to apply:** la orice întrebare despre alinierea țintă-subword, mecanismul e suprapunerea de
offset-uri, nu `word_ids`. Scripturile de măsurare nu au fost păstrate; se refac în câteva minute cu
`AutoTokenizer` plus `load_mlsp("test")` și `find_char_span`.
