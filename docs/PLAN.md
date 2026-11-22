# Site LCP multilingv: text in 11 limbi, fiecare cuvant colorat dupa complexitate

## Context

Sistemul din paper (A + B fuzionate LOLO, r medie 0.692521 pe 11 limbi) exista doar ca evaluare pe
setul de test (`ia-sahistii/release/`). Nu poti da un text nou si primi scorul fiecarui cuvant.
Scopul: o platforma pentru lingvisti. Utilizatorul alege limba, lipeste un text, iar in caseta de
iesire fiecare cuvant de continut e colorat dupa complexitate; click pe cuvant arata detaliile.
Totul (A, B, fuziune, site) intr-o singura imagine Docker, pusa pe un server ales dupa benchmark.

**Acum se face doar Etapa 1: cat dureaza inferenta fara placa video.** Din cifra asta decidem cat de
necesar e un GPU pe server. Restul etapelor raman in plan si vin dupa.

Decizii luate de Alexandru (21 nov):
- cele 11 limbi evaluate in paper, nu "orice limba";
- pe site ruleaza exact sistemul din paper: pentru limba L, A antrenat fara L, parametrii de
  fuziune alesi LOLO;
- se scoreaza doar cuvintele de continut, ca tintele MLSP; restul ramane text normal;
- timpii se masoara intai pe CPU (Docker pe Mac), apoi nativ pe Metal si pe PC-ul cu RTX 2070 SUPER;
- frontend dupa skill-ul `apple-design`, asezare ca DeepL, colorare ca FleLex;
- codul sta intr-un repo GitHub NOU, separat de cel al paperului.

De stiut pentru site (se afiseaza pe pagina):
- scorul e relativ la limba (fuziunea lucreaza pe z-score in limba), nu se compara intre limbi;
- increderea difera pe limbi: en 0.87, pt 0.84, de 0.77 fata de si 0.43, fil 0.50, ca 0.56;
- in perioada de review ARR, link-ul site-ului nu se pune in paper.

## Alegerea tehnica: llama.cpp cu GGUF-ul QAT oficial pentru B

Docker pe Mac nu vede GPU-ul (Metal), deci calea paperului (MLX pe Metal) nu exista in container.
Calea `--backend hf` (transformers + bitsandbytes) cere CUDA, iar Gemma 12B in bf16 (24 GB) nu
incape in VM-ul Docker al unui Mac de 24 GB. llama.cpp (`llama-cpp-python` 0.3.37) merge in toate
locurile: CPU in Docker, Metal nativ, CUDA in Docker pe PC si pe server. Un singur runtime inseamna
aceleasi cifre de B peste tot.

Modelul: `google/gemma-4-12B-it-qat-q4_0-gguf`, revizia `29d097773436b69ff9feafd636ab4cf873786537`,
6.98 GB, Apache-2.0, negated. E cuantizarea q4_0 pentru care a fost antrenat QAT-ul din care vin si
checkpoint-urile MLX ale paperului.

Pe RTX 2070 SUPER (8 GB): 6.98 GB plus contextul CUDA plus ecranul Windows probabil NU incap
integral; llama.cpp pune majoritatea straturilor pe GPU si restul pe CPU. Corect, doar mai incet.

Consecinta: B pe site nu e bit-identic cu paperul (alta cuantizare; calea hf pe T4 dadea r 0.97 cu
B-ul stocat). Etapa 3 recalculeaza statisticile lui B si cifra de fuziune cu llama.cpp, iar cifra
afisata pe site e aceea. Fallback daca spike-ul pica: transformers + bitsandbytes pe CUDA (verificat
pe T4) si MLX nativ pe Mac; atunci pe CPU in Docker se masoara doar A.

## Repo-ul nou

Creat de Alexandru pe 21 nov: `https://github.com/Glosperx/lcp-web` (privat, gol). Se cloneaza cu
`git clone git@github.com:Glosperx/lcp-web.git ~/Documents/GitHub/lcp-web` si se lucreaza acolo.
Commit-urile si push-ul le da el.

```
lcp-web/
  lcp_model/   data.py, signal_a.py, signal_b.py, fuse.py, copiate NESCHIMBATE din
               ia-sahistii/release/ (import cu PYTHONPATH=lcp_model, ca in release)
  lcp/         segment.py, encoders.py, rater.py            (etapa 1)
               pipeline.py                                   (etapa 4)
  scripts/     spike_llama.py, fetch_texts.py, bench_cpu.py  (etapa 1)
               export_model.py, b_reference.py, benchmark.py (etapele 2, 3, 7)
  artifacts/   params.json + modelele sklearn, cativa MB      (etapa 2)
  static/      index.html, app.css, app.js                   (etapa 5)
  bench/       texts/, results/
  docker/      Dockerfile.cpu (etapa 1), Dockerfile final cpu|cuda (etapa 6)
  server.py, docker-compose.yml, requirements.txt, .gitignore, README.md
```

Scripturile care au nevoie de date (spike, export, B de referinta) le citesc din repo-ul paperului
prin `--paper-release ~/Documents/GitHub/ia-sahistii/release` (seteaza `MLSP_DIR`, `ROLCP_CSV`,
`data.CACHE_DIR`, `data.PRED_DIR`, pe care `data.py` le citeste la apel). Datele MLSP nu intra in
repo-ul nou. Artefactele nu contin text din MLSP, deci se comit in repo-ul privat; daca repo-ul
devine public, se verifica intai licenta MLSP.

Ce se refoloseste din `lcp_model/`, fara rescriere: `find_char_span`, `crop_around`,
`normalize_token`, `lexical`, `fertility`, `zscore` (data.py); `ENCODERS`, `Encoder`, `features` si
hiperparametrii din `blend_ridge_hgb` (signal_a.py); `PROMPTS`, `render`, `LANG_NAMES`, `GEMMA4_QAT`
si logica id-urilor de cifre din `Rater` (signal_b.py); `temper`, `b_of`, `load_a`, `load_b`,
`signals`, `fit`, `z_a` (fuse.py).

## Etapa 1 (ACUM): inferenta fara placa video, in Docker pe Mac

Ce costa pe un text: segmentarea stanza, 3 encodere (un forward pe propozitie) si B = 3 citiri
Gemma pe fiecare cuvant de continut. Regresorii sklearn si fuziunea costa milisecunde, deci intra
abia la etapa 2.

1. **Imaginea CPU de lucru** (`docker/Dockerfile.cpu`, `python:3.11-slim`, linux/arm64): pinurile
   din `release/requirements.txt` (torch CPU, transformers 5.13.1, stanza 1.14.0, wordfreq,
   mecab-python3, ipadic) plus `llama-cpp-python==0.3.37` compilat pentru CPU. Modelele nu se coc
   inca: se monteaza cache-ul HF de pe Mac (encoderele sunt deja acolo) si un volum pentru stanza.
2. **GGUF-ul** descarcat in cache-ul HF, revizia fixata de mai sus.
3. **Modulele**: `lcp/segment.py` (stanza tokenize, mwt, pos, lemma pentru ca de en es fr it ja pt
   ro; regex pentru fil, cu o lista mica de cuvinte functionale, si pentru si; continut = UPOS NOUN,
   VERB, ADJ, ADV; contextul unui cuvant = propozitia lui; stanza incarcat lenes, pe limba).
   `lcp/encoders.py` (cele 3 encodere prin `signal_a.Encoder`, un forward pe propozitie, pooling pe
   spanul fiecarui cuvant: aceeasi intrare ca `Encoder.embed`, deci acelasi vector).
   `lcp/rater.py` (prompt cu `PROMPTS`/`render` si tokenizer-ul HF al `GEMMA4_QAT` prin
   `apply_chat_template`, id-urile date lui llama.cpp, logits pe ultima pozitie, masa pe cifre ca
   in `signal_b.Rater`).
4. **Spike-ul raterului, in container** (`scripts/spike_llama.py`). Porti: vocabularul GGUF da
   aceleasi id-uri ca tokenizer-ul HF; masa pe cifre >= 0.5, fara NaN; pe 10 randuri pe limba x 3
   prompturi, corelatia cu `predictions/signal_b.csv` per limba, asteptat ~0.97. Datele se monteaza
   read-only din `ia-sahistii/release/data`. Daca o poarta pica, ma opresc si raportez.
5. **Textele** (`scripts/fetch_texts.py`): primul paragraf si primele doua paragrafe din acelasi
   articol Wikipedia in toate cele 11 limbi (filipineza = tl.wikipedia), cu sursa si licenta
   CC BY-SA. Tinta ~100 si ~200 de cuvinte; daca un articol e prea scurt intr-o limba, se alege
   altul pentru toate.
6. **Masuratoarea** (`scripts/bench_cpu.py`, toate cele 10 nuclee):
   - o data: incarcarea stanza, encodere, Gemma, si memoria de varf;
   - pe limba x marime, 1 incalzire + 3 repetari: cuvinte, cuvinte de continut, propozitii, citiri
     B, tokeni de prompt, timp segmentare, timp A, timp B, total, s/citire, tokeni/s la prefill,
     timp pana la prima propozitie terminata;
   - B fara si cu refolosirea prefixului KV intre citiri cu aceeasi propozitie.
   Rezultat: `bench/results/cpu_docker_mac.csv` si un rezumat pe limba.
7. **Concluzia**: tabelul de timpi plus extrapolarea. Tokenii/s la prefill permit estimarea pe alt
   CPU (un server cloud cu 8 vCPU e de obicei mai lent decat un M5). Decidem: server CPU (eventual
   cu mod asincron, rezultatul vine dupa cateva minute) sau server cu GPU.

Ordin de marime asteptat (estimare, nemasurat), 2 paragrafe ~ 110 cuvinte de continut ~ 330
citiri: Docker CPU 10-20 minute, Metal ~2 minute (MLX a dat 0.36 s/citire), GPU de server de 24 GB
20-50 de secunde.

## Etapa 2. Exportul modelului: `scripts/export_model.py`

- Per encoder (xlmr, labse, e5): ridge + HGB fitate pentru `p_en` (doar CompLex) si 11 modele
  `p_multi_L` (CompLex + celelalte limbi; la en fara CompLex), aceiasi hiperparametri.
- Per limba si encoder: `mu_L` (media embedding-ului) si `fert_mu_L`.
- Constantele de z-score exact cum le calculeaza `fuse.py` (pe encoder, media encoderelor, amestecul
  cu `w_src_L`), plus parametrii LOLO per limba, luati cu aceleasi functii ca `fuse.main`. Pe 11
  limbi: T 4 sau 6, partitia 1|23|45 peste tot, w 0.35-0.40, w_src 0.625-1.0.
- Paritate: predictiile modelelor fitate == `p_en`/`p_multi` din `signal_a.csv` (mlsp+ro), iar
  fuziunea din pipeline pe randurile de test == `fuse.py --with-ro --out`.

## Etapa 3. B de referinta cu llama.cpp: `scripts/b_reference.py`

B pe tot setul de test cu RoLCP (21.633 citiri, peste noapte, nativ pe Metal). Da media si
deviatia lui B per limba pentru z-score, r per limba si media pe 11 limbi cu backend-ul site-ului
(comparata cu 0.692521, cifra afisata pe site), si distributia fuziunii per limba.

Scala de afisare: percentila cuvantului in distributia fuziunii din limba lui (fara etichete),
trecuta prin cuantilele etichetelor din toate limbile la un loc, da un scor 0-1 pe scala
adnotarilor MLSP. Transformarea e monotona, deci ordinea cuvintelor e exact a sistemului. Nivelul
1-5 e nota cea mai apropiata (1 foarte usor, 2 usor, 3 neutru, 4 dificil, 5 foarte dificil), aceeasi
scara ca la adnotare si in prompturile lui B. O regresie liniara ar fi tras scorurile spre medie si
culorile n-ar mai varia.

## Etapa 4. Pipeline si API

- `lcp/pipeline.py`: segmentare, A, B, fuziune cu constantele exportate, scor 0-1, nivel.
- `server.py`, FastAPI: `POST /api/analyze {lang, text}` raspunde in flux, cate o linie JSON pe
  propozitie terminata, ultima linie cu timpii pe etape. `GET /api/languages` (11 limbi + r).
  Un singur lock pe model, limita de 2000 de caractere, textele nu se logheaza.

## Etapa 5. Frontend (`static/`, HTML + CSS + JS simplu, fara build)

Se incarca skill-ul `apple-design` inainte de primul rand de cod.
- Asezare ca DeepL: doua panouri egale, unul langa altul (unul sub altul pe telefon). Stanga: bara
  cu selectorul de limba si r-ul limbii, caseta mare de text, contor 0/2000, butonul Analizeaza
  (si Cmd/Ctrl+Enter). Dreapta: acelasi text, cu cuvintele de continut colorate.
- Colorare ca FleLex: fundal colorat pe cuvant, cinci culori de la verde (nivel 1) prin galben si
  portocaliu la rosu (nivel 5), cu variante pentru dark mode. Deasupra, legenda cu cele cinci
  niveluri si cate cuvinte are fiecare; click pe un nivel lasa colorate doar cuvintele lui.
  Cuvintele functionale raman text normal.
- Propozitiile inca in lucru apar estompate si se coloreaza pe masura ce sosesc din flux.
- Click pe cuvant (sau Enter, cuvintele sunt focusabile): popover cu nivelul si eticheta, scorul
  0-1, lema, frecventa Zipf, si pe un rand mic A si B. Escape sau click in afara il inchide.
- Nota sub iesire: scorurile se compara doar in aceeasi limba. Fara text din MLSP pe site.

## Etapa 6. Imaginile Docker portabile (planificata pe 22 nov, inca neconstruita)

Deciziile lui Alexandru (22 nov):
- Doua imagini, doar linux/amd64 (fara arm64), dintr-un `docker/Dockerfile` cu
  `ARG TARGET=cuda|cpu`:
  - cuda: nvidia/cuda 12.6.3 (devel pentru build, runtime la final), cu llama.cpp compilat pentru
    sm_75, 80, 86, 89 si 90, plus PTX compute_90 (Blackwell merge prin JIT);
  - cpu: python:3.11-slim, ca rezerva (de ~35 de ori mai lenta).
  In ambele, llama.cpp e compilat fara GGML_NATIVE, iar varianta de procesor se alege la rulare
  (GGML_BACKEND_DL, GGML_CPU_ALL_VARIANTS). Torch CPU ramane doar pentru encodere.
- Totul copt in imagine, cu revizii fixate, din volumele PC-ului, fara descarcari noi: GGUF-ul,
  tokenizer-ul Gemma, cele 3 encodere, stanza pentru 9 limbi (doar tokenize, mwt, pos, lemma),
  MeCab/ipadic, codul, artefactele si pagina. `HF_HUB_OFFLINE=1`, utilizator fara root,
  healthcheck. Marimi estimate: cuda ~19-20 GB, cpu ~15 GB, cu straturile de modele comune
  (`COPY --link`).
- `docker-compose.server.yml`, cu profilurile gpu si cpu, pentru serverul nou. Site-ul de pe PC
  ramane pe `lcp-web:cuda`, cu volumele si repo-ul montat (`docker-compose.yml` neschimbat).
- Schimbari mici in cod: setarile llama.cpp din variabile de mediu (implicit cele de acum);
  estimarea de timp scalata dupa `tok_s`; pagina vorbeste cu propria origine oriunde in afara de
  Vercel; `LCP_TRUST_XFF` pentru un port expus fara proxy.
- Planul detaliat, ce s-a verificat deja si testele sunt in `docs/PROMPT_etapa6.md`.

## Etapa 7. Benchmark-ul complet: `scripts/benchmark.py`

Aceleasi texte ca la etapa 1, prin API, in trei locuri: Docker CPU pe Mac, nativ pe Mac cu Metal,
Docker CUDA pe PC. Pe PC: Docker Desktop cu WSL2, driver NVIDIA recent, test cu
`docker run --rm --gpus all nvidia/cuda:12.6.0-base-ubuntu24.04 nvidia-smi`, repo-ul clonat de pe
GitHub.

## Etapa 8. Serverul (plan separat, dupa cifre)

## De ce e nevoie din partea ta

- Repo-ul GitHub nou (pasii sunt in chat) si URL-ul lui.
- Docker Desktop pornit (acum daemon-ul nu ruleaza); in Settings > Resources, memoria VM-ului la
  16 GB si toate cele 10 CPU-uri. Gemma 7 GB + encodere ~4 GB + stanza + torch.
- Aprobari pentru `docker build`, descarcarea GGUF-ului (7 GB) si a modelelor stanza.

## Verificare

- Etapa 1: portile spike-ului trec (sau ne oprim cu cifra care a picat); `bench_cpu.py` scrie
  CSV-ul pentru 11 limbi x 2 marimi, cu memoria de varf sub limita VM-ului; s/citire pe CPU in
  container > 0.36 s (MLX pe Metal), altfel ceva e masurat gresit.
- Etapa 2: A identic cu `signal_a.csv`, fuziunea identica cu `fuse.py --out`.
- Etapa 3: r de fuziune pe 11 limbi cu llama.cpp, raportat langa 0.692521.
- Etapele 4-5: `docker compose up -d`, `http://localhost:8000`, un paragraf in fiecare limba,
  culorile si popover-ul merg.
- Etapa 6: `docker compose -f docker-compose.server.yml --profile gpu up` (si `--profile cpu`) pe
  portul 8001, cu portile si testele din `docs/PROMPT_etapa6.md`.
- Etapa 7: tabelul de timpi din cele trei locuri.

Limitare cunoscuta: in japoneza tintele MLSP sunt unitati mai lungi (ex. 活躍した) decat tokenii
stanza (活躍, し, た); pe site se scoreaza tokenul de continut.
