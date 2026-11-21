# Prompt pentru sesiunea Claude Code de pe PC: Etapa 7 adusa inainte (GPU RTX 2070 SUPER + CPU x86)

Scris pe Mac pe 21 nov 2026, la sfarsitul Etapei 1. Sesiunea de pe PC nu are memoria si nici fisierul
de plan de pe Mac, deci tot ce trebuie e aici, in `docs/PLAN.md` si in `bench/results/`.

## Ce vrem

Etapa 1 a masurat inferenta doar pe CPU, in Docker pe Mac (M5). Concluzia e in
`bench/results/concluzie_etapa1.txt`: B (3 citiri Gemma pe cuvant de continut) ia aproape tot timpul,
1.32 s/citire cu refolosirea KV, deci 1 paragraf ~3.5 minute, 2 paragrafe ~6 minute. Pentru decizia
"server CPU sau GPU" ne mai trebuie doua cifre, pe PC:
1. cat dureaza pe RTX 2070 SUPER (8 GB VRAM), cu Gemma impartit intre GPU si CPU daca nu incape tot;
2. cat dureaza B doar pe procesorul x86 al PC-ului, ca reper pentru un server cloud fara GPU.

Citeste intai, intregi: `docs/PLAN.md` (planul complet; acum facem doar partea de PC a Etapei 7,
etapele 2-6 raman pentru mai tarziu), `bench/results/concluzie_etapa1.txt`, `README.md`,
`lcp/rater.py`, `scripts/bench_cpu.py`, `scripts/bench_report.py`, `docker/Dockerfile.cpu`,
`docker/run_cpu.sh`.

## PC-ul

- Windows, Ryzen 7 3700X (8 nuclee Zen 2, 16 thread-uri, AVX2, fara AVX-512), 16 GB RAM,
  RTX 2070 SUPER 8 GB (Turing, sm_75), Docker Desktop cu WSL2, driver NVIDIA actualizat de Alexandru.
- `%UserProfile%\.wslconfig` ar trebui sa aiba `[wsl2]`, `memory=12GB`, `swap=8GB` (verifica cu
  `free -g` in WSL; daca VM-ul are 8 GB, spune-i si asteapta).
- Repo-ul e clonat in sistemul de fisiere WSL (`~/lcp-web`). Cache-ul Hugging Face trebuie sa stea tot
  acolo (de exemplu `~/.cache/huggingface/hub`), nu pe /mnt/c: GGUF-ul de 7 GB s-ar citi foarte incet.

## Pasii, in ordine

0. Verificari: `docker run --rm --gpus all nvidia/cuda:12.6.0-base-ubuntu24.04 nvidia-smi` (driver,
   VRAM libera cu ecranul pornit), `docker info` (CPU, memorie), `free -g`, `df -h ~`.
1. `docker/Dockerfile.cuda` (linux/amd64): baza `nvidia/cuda` devel, Python 3.11, aceleasi pinuri ca
   `docker/requirements.cpu.txt`, torch 2.13.0 CPU de pe indexul PyTorch CPU (encoderele lui A raman pe
   CPU, iau ~1 s pe text), `llama-cpp-python==0.3.37` compilat cu
   `CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=75"`. Aceleasi variabile de mediu ca imaginea
   CPU (PYTHONPATH, HF_HUB_CACHE, HF_HUB_OFFLINE=1, STANZA_RESOURCES_DIR). Plus `docker/run_cuda.sh`
   dupa modelul lui `run_cpu.sh`, cu `--gpus all`, fara montarile paperului (nu sunt necesare aici).
   Cere aprobare inainte de `docker build`.
2. Descarcarile, cu aprobare inainte (in cache-ul HF din WSL, cu HF_HUB_OFFLINE=0 doar pentru ele):
   - GGUF: `google/gemma-4-12B-it-qat-q4_0-gguf`, fisierul `gemma-4-12b-it-qat-q4_0.gguf`, revizia
     `29d097773436b69ff9feafd636ab4cf873786537`, 6.98 GB, sha256
     `93567e57a8fe10b23569b9d9ec38cd005deedf71e29477c421a4b83f418a538b` (verifica-l). Fara mmproj.
   - tokenizer-ul Gemma: `google/gemma-4-12B-it-qat-q4_0-unquantized`, revizia
     `b6ed86275a6a5735884e208bfed95b445a684ca2`, doar tokenizer.json, tokenizer_config.json,
     chat_template.jinja, config.json.
   - encoderele, reviziile din `lcp_model/signal_a.py` (ENCODERS): xlm-roberta-base, LaBSE,
     multilingual-e5-base, ~4 GB.
   - stanza: `python -m lcp.segment --prepare` (descarca default.zip pentru 9 limbi, ~5 GB, in volumul
     stanza; pe Mac le avea deja in cache).
3. Optiuni noi, fara sa schimbi comportamentul implicit: in `LlamaRater` si in `bench_cpu.py`,
   `--gpu-layers N`, `--flash-attn`, `--n-ctx` (Mac-ul a folosit 4096; cel mai lung prompt din spike a
   avut 675 de tokeni, deci 2048 ajunge si economiseste VRAM), `--no-mmap`, si in bench `--skip-a`
   (fara encodere, pentru masuratoarea doar pe CPU). In llama-cpp-python 0.3.37 parametrii exista:
   `n_gpu_layers`, `flash_attn`, `op_offload`, `use_mmap`, `type_k`, `type_v`, `swa_full`.
4. Cate straturi incap: un script mic (`scripts/fit_gpu_layers.py`) care incearca n_gpu_layers de sus
   in jos (toate straturile, apoi mai putine) pana cand Gemma se incarca si face o citire fara eroare de
   memorie, si noteaza VRAM-ul folosit (nvidia-smi) si s/citire pentru cateva valori. Gemma 4 12B are 48
   de straturi; 6.98 GB plus KV plus contextul CUDA plus ecranul probabil nu incap toate in 8 GB.
   Incearca si cu flash attention (elimina umplutura cache-ului V; pe Mac aparea "padding V cache to
   2048").
5. Poarta de paritate, fixata dinainte: aceleasi prompturi ca pe Mac, comparate cu
   `bench/results/cpu_docker_mac_readings.csv` (cheie: lang, size, sent, word, prompt; mode reuse,
   run 0). Pe un subset (de exemplu primele 2 propozitii din fiecare text de 1 paragraf), scorul
   (nota asteptata reascalata la 0-1, ca `lcp/rater.py:score`) trebuie sa coreleze cu cel de pe Mac la
   r >= 0.99 pe toate citirile, iar masa pe cifre >= 0.5 fara NaN. Raporteaza si max |dp|. Daca pica,
   te opresti si raportezi cifra. Nu e nevoie de datele MLSP pe PC.
6. Bench GPU: acelasi protocol ca pe Mac, ca sa se compare direct (vezi comanda din README, cu
   `--gpu-layers` ales la pasul 4 si `--prefix gpu_docker_pc`). Pe GPU o trecere ar trebui sa fie
   scurta, deci daca timpul permite, adauga repetarile din plan (1 incalzire + 3) macar pentru modul
   reuse. Apoi `python scripts/bench_report.py --prefix gpu_docker_pc`.
7. Reper CPU x86: containerul FARA `--gpus` (altfel llama.cpp muta inmultirile mari pe GPU chiar cu
   n_gpu_layers=0), `--skip-a`, doar modul reuse, pe 3 limbi la 1 paragraf (en, ro, si), prefix
   `cpu_docker_pc`. Atentie la memorie: pe Mac tot sistemul a avut ~10 GB memorie proprie cu varf de
   15.7 GB la incarcare; pe PC VM-ul are 12 GB, de aici `--skip-a` si eventual `--no-mmap`.
8. Concluzia: `bench/results/concluzie_etapa7_pc.txt`, in romana fara diacritice, fara tabele
   markdown: timpi pe limba si marime pe GPU, reperul CPU x86 (s/citire, tokeni/s), comparatia cu
   Mac-ul, VRAM si RAM de varf, si ce inseamna pentru server (GPU de cata memorie, sau CPU cu cate
   nuclee, sau mod asincron).

## Ce stim deja si nu trebuie redescoperit

- `Llama.eval` ignora rezultatul lui `kv_cache_seq_rm`; `lcp/rater.py` il verifica singur si reia de
  la zero daca e refuzat (cache-ul SWA al Gemma). Refolosirea KV a dat probabilitati bit-identice.
- Tokenizer-ul HF al QAT-ului si template-ul de chat sunt identice cu ale checkpoint-ului MLX din
  paper; llama.cpp primeste id-uri, nu text. Id-urile cifrelor: 236770, 236778, 236800, 236812, 236810.
- In bench, pipeline-ul stanza se elibereaza dupa fiecare limba (altfel, pe 16 GB, Gemma intra in swap).
- Pe Mac, primele ~15 minute dupa incarcare au fost cu ~20% mai lente (memoria se aseaza); de aceea
  catalana la 1 paragraf a fost refacuta. Pe GPU efectul ar trebui sa fie mic, dar verifica-l.
- Textele de bench sunt deja in `bench/texts/` (Wikipedia, "Soarele"); nu le descarca din nou.
- Pe Mac, `docker/run_cpu.sh` monteaza cache-ul HF read-only; `python -` cu heredoc nu merge prin el
  (fara `-i`), scrie scripturile de proba in fisiere.

## Reguli

- Cere aprobare inainte de `docker build` si de orice descarcare mare.
- Nu da commit si nu face push; pregatesti fisierele si staging-ul, iar commit-ul il da Alexandru.
  Comenzile de git i le dai in engleza, cu mesaje scurte.
- Fara subagenti; verifici singur.
- In chat: romana fara diacritice, fara tabele markdown, explicatii scurte.
- Daca o poarta pica sau ceva nu incape in memorie, te opresti si raportezi cifra, fara sa ocolesti.
