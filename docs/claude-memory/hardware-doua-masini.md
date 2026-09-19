---
name: hardware-doua-masini
description: "Proiectul are două mașini neinterschimbabile: MacBook M5 cu 24 GB fără CUDA, și PC Windows cu RTX 2070 SUPER 8 GB unde rulează codul existent; data/mlsp/ lipsește pe Mac"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d525f31-ed64-403d-bcae-3932e312db13
  modified: 2026-08-16T12:20:41.668Z
---

Verificat direct pe **15 august 2026**. Alexandru a confirmat că le poate folosi pe amândouă.

## Cele două mașini

**MacBook Pro:** Apple M5, 10 nuclee (4 performance + 6 efficiency), **24 GB memorie unificată**,
Metal 4, 740 GB liberi, Python de sistem 3.9.6. **Niciun pachet ML instalat**, verificat unul câte
unul: torch, numpy, pandas, scikit-learn, scipy, transformers, wordfreq, stanza, spacy, bitsandbytes,
huggingface_hub, datasets, conllu, sentencepiece. Niciun venv.

**PC Windows:** RTX 2070 SUPER, 8 GB VRAM. Calea e `C:\Users\glosper\Documents\pred_eye\`, vizibilă
în căile absolute din logurile versionate în repo (`lemmafreq_log.txt`, `e5_log.txt`,
`finetune_multi_log.txt`).

## De ce nu sunt interschimbabile

**Codul existent nu pornește pe Mac.** `recompute_gpu.py` încarcă LLM-ul prin
`BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")`, iar cuantizarea NF4 din
`bitsandbytes` **e CUDA-only**. PC-ul e deci mașina continuității, singura pe care se reproduc
cifrele deja obținute, cu `transformers` fixat la 4.46.3.

**Dar plafonul de memorie e invers.** 24 GB unificați față de 8 GB VRAM: un model de 8B în fp16 cere
~16 GB, deci încape pe Mac și **nu încape deloc** pe 2070, care e obligat la 4 biți (~5 GB).
Plafonul de 8 GB e exact ce face configurația (ii) din designul multilingv dureroasă, fiindcă
fiecare model monolingv de 7-9B trebuie cuantizat și verificat individual.

**Împărțirea pe roluri, propusă dar NEverificată:** PC pentru trecerile LLM care trebuie să rămână
comparabile cu cifrele existente plus ablațiile de fine-tuning; Mac pentru tot restul, care e
majoritatea muncii (stanza pe 11 limbi, statistici UD, wordfreq, sklearn, bootstrap, figuri, scris).
XLM-R-base e destul de mic încât embedding-urile să meargă și pe CPU sau MPS.

**Nemăsurat:** debitul real al M5 la inferență LLM, dacă ruta MLX sau llama.cpp/GGUF dă rezultate
destul de apropiate de NF4 ca să fie comparabile, și dacă merită duplicat pipeline-ul.

## Datele

**`data/mlsp/` NU există pe Mac.** `_load_mlsp()` returnează `None` fără el, deci semnalul A nu poate
fi recalculat acolo. `.gitignore` îl exclude explicit ca gated pe HuggingFace. **Nu s-a verificat
dacă mai există pe Windows**; dacă nu, gate-ul HuggingFace revine pe calea critică cu timp de
aprobare necunoscut.

Există local: cache-urile de semnale per `datapointID`, `data/test_set.csv` cu coloană `lemma` deja
calculată, și `data/bert_cache/`. Deci calea rapidă pe română se reproduce, dar nimic nou nu se
calculează fără MLSP.

Dimensiuni confirmate din loguri: CompLex EN = **8423** instanțe, MLSP romanic (5 limbi) = **2827**,
adică ~565 pe limbă.

**Why:** orice estimare de compute pentru grila de 11 limbi × 2 configurații e greșită dacă
presupune o singură mașină, iar prima verificare de făcut nu e despre modele, ci despre dacă datele
MLSP mai există undeva.

**How to apply:** înainte de orice plan de rulare, întreabă pe care mașină și verifică `data/mlsp/`
pe Windows. Nu presupune că `pip install` de pe Mac reproduce pipeline-ul. Vezi și
[[lolo-exista-deja-in-cod]].

---

## ACTUALIZARE 16 august 2026: două afirmații de mai sus sunt acum greșite

Verificat direct pe Mac în sesiunea din 16 august.

**1. „Niciun pachet ML instalat" era adevărat doar pentru Python-ul de sistem.** Există două medii
conda cu tot ce trebuie:

| | `envs/ml_def` | `envs/glioma` |
|---|---|---|
| Python | 3.11.15 | 3.12.13 |
| torch | **2.13.0**, `mps.is_available()` **True** | idem |
| transformers | **5.13.1** | idem |
| sklearn, pandas | da | da |

Calea: `/opt/homebrew/Caskroom/miniforge/base/envs/<nume>/bin/python`. **Lipsesc în continuare**:
`mlx`, `mlx_lm`, `llama_cpp`, `stanza`, `spacy`, `wordfreq`.

**2. „Codul existent nu pornește pe Mac" e prea tare. Pornește, cu trei linii schimbate.**
`model(ids).logits[0, -1]`, adică fix ce cer semnalele B și C, e PyTorch curat și rulează pe MPS
neschimbat. Cele două blocaje sunt amândouă în `LLMRater.__init__`, `solution_bert.py:249-254`:
selecția de device nu ia în calcul `mps`, deci cade pe CPU; și `BitsAndBytesConfig` NF4 e CUDA-only.
Reparația: `mps` în selecție, cuantizare condiționată de `dev == "cuda"`, altfel `float16`. Un model
de 8B în fp16 încape în 24 GB.

Consecință de raportat în paper: pe Mac fp16, pe Windows NF4, deci **nu sunt numeric identice** și nu
se amestecă rezultate din cele două mașini în același tabel fără notă.

**MLX și llama.cpp expun amândouă logits**, verificat la sursă: `mlx_lm.generate_step` produce
`logprobs = logits - mx.logsumexp(...)`, vector complet peste vocabular; `llama-cpp-python` are
`logits_all=True` cu `self.scores` de forma `(n_ctx, n_vocab)`. **Dar nu sunt necesare.** Rămân planul
B și C pentru viteză.

**3. Datele s-au schimbat.** `data/mlsp/` **există acum** pe Mac, cu cele 5 fișiere romanice, iar
`data/mlsp_full/` are **toate cele 10 limbi**, test și trial, cu etichete. În schimb
**`data/complex_en/` lipsește**, și atenție: `finetune_xlmr.py:46` doar citește, **nu descarcă**, spre
deosebire de `baseline_surface.py:71` și `recompute_gpu.py:168`, care descarcă. Deci
`finetune_xlmr.py --frozenmulti` crapă azi cu `FileNotFoundError`.

**Rămâne nemăsurat, la fel ca înainte:** debitul real al M5 în fp16 față de 2070 SUPER în NF4. De asta
depinde dacă Mac-ul preia un braț întreg de LLM sau doar depanarea. Plus compatibilitatea
`transformers` 5.13.1 cu cod scris pe 4.46.3, care e o verificare de zece minute.

**CORECȚIE 16 august, seara.** „Pornește cu trei linii schimbate" e adevărat pentru Qwen3-8B și orice
transformer dens, dar **fals pentru Qwen3.5**, a cărui atenție liniară Gated DeltaNet cere kernel-uri
CUDA și cade tăcut pe referința PyTorch cu regresie de latență ~14x. Pe Mac, Qwen3.5 și Gemma 4 cer
ruta **MLX**, unde ambele au build-uri gata făcute. Detaliile și rutele valide pentru citirea logits
sunt în [[rute-rulare-logits]].

Confirmat tot atunci, prin rulare reală în `envs/ml_def`: Python 3.11.15, `transformers` 5.13.1,
`pandas` 3.0.3, iar `huggingface_hub` e autentificat ca utilizatorul **Glosper**, cu token în
`~/.cache/huggingface/token`.
