Vreau sa rulezi local, pe setul de test, doua modele de limbaj care au fost incercate doar pe trial:
Llama 3.1 8B si Aya Expanse 8B. Cifrele lor intra in Tabelul 3 din documentatie (modelele pentru
semnalul B), unde acum au "--" pe coloanele de test. Nu scrii documentatia: o actualizez in alta
sesiune, cu cifrele tale.

## Context

- Semnalul B e o nota de la 1 la 5 citita din probabilitatile primului token al raspunsului, cu trei
  prompturi (expert, short, marked), fara niciun exemplu etichetat. Codul e `release/signal_b.py`.
- Pe test exista deja Gemma 4 12B (4-bit), Qwen3 8B (4-bit) si Qwen3.5 9B (8-bit). Pe trial (300 de
  instante, 10 limbi, doua prompturi, T = 1) au fost si `llama31-8b-4bit` (r mediu 0.547) si
  `aya-expanse-8b-4bit` (0.514); raportul e `output/e_bakeoff.md`.
- `release/signal_b.py` are deja ambele chei in `MODELS`, cu revizii fixate (MLX pe Apple silicon).
- Sistemul de referinta: `release/fuse.py --with-ro` da 0.692521 pe 11 limbi (`output/doc_fuse_ro11.txt`).
  Cifrele pe care le vreau sunt pe aceleasi 7.211 instante (10 limbi MLSP + RoLCP).

## Ce rulezi

1. Copiezi `release/` intr-un director de lucru in afara repo-ului (de exemplu `~/lcp-llm-extra/release`).
   **Nu atingi `release/` din repo**: `signal_b.py` scrie in `cache/` si suprascrie
   `predictions/signal_b.csv` la sfarsitul unei rulari complete.
2. Control inainte de rulare: in copie, `python signal_b.py --model gemma4-12b-4bit --limit 3` trebuie
   sa dea pentru primele randuri exact valorile p1..p5 din `predictions/signal_b.csv` pentru Gemma.
   Daca nu se potrivesc, te opresti si imi spui.
3. Rulezi, cate un model o data (Mac M5, 24 GB):
   `python signal_b.py --model llama31-8b-4bit --with-ro`
   `python signal_b.py --model aya-expanse-8b-4bit --with-ro`
   Fiecare are 21.633 de citiri (7.211 x 3 prompturi). Gemma face 0.36 s pe citire pe M5, deci socoteste
   cam 2 ore pe model. Rulezi in fundal; cache-ul reia de unde s-a oprit.
4. Optional, doar daca timpul permite si dupa ce iti confirm: celelalte cuantizari de pe trial,
   `qwen35-9b-4bit` (0.622 pe trial) si `qwen3-8b-8bit` (0.584).

## Ce calculezi

Scrii un script `analysis_doc_llm_extra.py` la radacina repo-ului, dupa modelul lui
`analysis_doc_correlations.py` si `analysis_doc_ablations_extra.py` (importa `release/`, nu il modifica).
Randurile noi le pui intai in `output/doc_llm_extra_signal_b.csv` (acelasi format ca
`predictions/signal_b.csv`), iar scriptul le citeste de acolo, ca la `output/doc_qwen_ro_signal_b.csv`.
Iesirea merge in `output/doc_llm_extra.txt`. Pentru fiecare model nou:

- **Citirea din Tabelul 3**, aceeasi ca la Qwen: primele doua prompturi, T = 1, fara grupare. Raportezi
  r-ul lui B pe fiecare limba si media pe 11, plus fuziunea cu semnalul A cand modelul e singurul
  candidat (logica din `fuse.py`: w_src si w alese pe celelalte limbi), cu intervalul pereche fata de
  sistem (0.692521).
- **Citirea completa**: trei prompturi, T si gruparea alese pe celelalte limbi, ca pentru Gemma
  (`fuse.py --with-ro --models <cheie>` in copie).
- Corelatia semnalului B (citirea din Tabelul 3) cu Gemma 4 si cu Qwen3.5 9B, Pearson in fiecare
  limba, media pe 11 (ca partea 2 din `output/doc_correlations.txt`).
- Controlul ca sistemul nu se misca: cu toate cele cinci modele in bazin, `pick_model` trebuie sa aleaga
  tot Gemma 4 pe fiecare limba, iar media sa ramana 0.692521. Daca se schimba, te opresti si imi spui.

## Capcane cunoscute

- Un CSV citit in timpul rularii e partial; NaN-urile devin zero dupa standardizare si dau cifre care
  arata plauzibil. Citesti doar dupa o rulare completa si verifici ca fiecare limba are toate randurile.
- Ollama si serverul `mlx_lm` trunchiaza distributia, deci nu pot servi semnalul B. Folosesti doar
  `signal_b.py`, care citeste logitii direct.
- Verifici ca masa de probabilitate pe cifrele 1..5 nu e degenerata (`score` NaN sau p-uri toate zero),
  mai ales pe sinhaleza, unde tokenizerul lui Aya cade pe octeti.
- In zsh nu pui comentarii `#` pe aceeasi linie cu o comanda.

## Reguli

- Nu atingi `Paper/`, `release/` din repo si nu faci git add sau commit.
- Langa fiecare cifra din `output/doc_llm_extra.txt` scrii de unde vine (fisier, comanda).
- La final imi dai in chat, in romana, fara diacritice si fara tabele markdown: pe fiecare model, B si
  fuziunea pe 11 limbi (citirea din Tabelul 3 si citirea completa), intervalul fata de sistem, cele doua
  corelatii si timpul real pe citire. Spui si pe ce limbi un model nou bate Gemma.
