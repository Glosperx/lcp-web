# Prompt pentru o sesiune noua Claude Code pe PC: Etapa 6, imaginile Docker portabile

Scris pe PC pe 22 nov 2026, dupa Etapa 5 (commit bd2d8e9, pagina noua live pe Vercel). Completat
in aceeasi seara intr-o sesiune de planificare, fara build: deciziile lui Alexandru, ce s-a
verificat deja in surse si in imaginile de pe PC, si planul pas cu pas. Sesiunea asta construieste
doua imagini Docker cu care site-ul se poate muta pe alt server. Nu schimba nimic la site-ul care
ruleaza acum pe acest PC, in afara de restartul de la teste (pasul 9).

## Unde suntem

- Facute: Etapele 1-5, 7 (partea de PC) si 8, plus auditul. Concluziile sunt in `bench/results/`
  (`concluzie_etapa*.txt`, `audit.txt`).
- Site-ul e live 24/7 de pe acest PC: pagina pe Vercel (https://lcp-web-static.vercel.app),
  API-ul in `docker compose` (`docker-compose.yml`) pe imaginea `lcp-web:cuda`, cu modelele in
  volumele `lcp-hf` si `lcp-stanza` si codul montat din repo, expus prin Tailscale Funnel la
  https://lcp.tail6e4ef5.ts.net.
- Codul de acces e oprit temporar (linia `LCP_ACCESS_CODE` comentata in `.env`); API-ul e deschis.
- Etapa 7 din PLAN (benchmark-ul prin API pe Mac si PC) nu se mai face acum: serverul a fost ales
  (PC-ul cu GPU), iar cifrele PC-ului exista (api_check: ~15 s pe un paragraf).
- In seara planificarii site-ul era in spill: `/api/health` dadea `tok_s` 372 si `slow: true`
  (placa 7745/8192 MiB, Firefox inchis). Alexandru a ales sa nu fie repornit atunci; restartul se
  face la teste (pasul 9), cand site-ul se opreste oricum. La inceput citeste `tok_s` si spune-i
  cifra.

Citeste intai, intregi: `docs/PLAN.md` (Etapa 6), `README.md`, `docker/Dockerfile.cuda`,
`docker/Dockerfile.cpu`, `docker/requirements.*.txt`, `docker/run_cuda.sh`, `docker-compose.yml`,
`scripts/fetch_models.py`, `server.py`, `lcp/pipeline.py` (constructorul `Pipeline`, `probe`,
`languages`), `lcp/rater.py`, `lcp/segment.py` (`Segmenter.pipeline`, `prepare`),
`lcp/encoders.py`, `static/app.js` (`PUBLIC_API`, `estimate`, `noteSlow`), `scripts/api_check.py`,
`bench/results/concluzie_etapa7_pc.txt` (sectiunile 4 si 5) si `bench/results/concluzie_etapa5.txt`.

## Deciziile lui Alexandru (22 nov)

- Doua imagini, ambele doar linux/amd64 (x86-64). Fara arm64.
- Una cu GPU, doar pentru placi NVIDIA (CUDA), compilata pentru mai multe generatii de placi. Una
  doar pe CPU, ca rezerva.
- Site-ul de pe acest PC ramane cum e: `lcp-web:cuda`, volumele, repo-ul montat,
  `docker-compose.yml` neschimbat. Imaginile noi sunt pentru alt server.
- Modelele intra in imagine: porneste fara internet, cu revizii fixate.
- CUDA 12.6.3 si `CMAKE_CUDA_ARCHITECTURES=75-real;80-real;86-real;89-real;90-real;90-virtual`:
  cod nativ pentru sm_75 (T4, RTX 20xx), sm_80 (A100, A30), sm_86 (A10, A40, RTX 30xx, A6000),
  sm_89 (L4, L40, RTX 40xx), sm_90 (H100), plus PTX compute_90, din care driverul compileaza la
  prima pornire pentru placi mai noi (Blackwell: B200, RTX 50xx). Fara CUDA 12.8.
- Restartul site-ului se face la teste, nu inainte.
- In sesiunea de planificare nu s-a construit nimic; aprobarile se cer in sesiunea de executie.

## De intrebat la inceput, inainte de cod

1. Aprobare pentru fiecare dintre:
   - curatarea cache-ului de build vechi: `docker builder prune` (16.24 GB, 25 de inregistrari,
     niciuna activa). Imaginea `lcp-web:cuda` a site-ului ramane, doar un rebuild al ei ar dura
     apoi mai mult;
   - exportul modelelor in `build/models` (~13 GB pe C:, din volume, fara descarcari);
   - `docker build` cuda si `docker build` cpu. Descarcarile lor: nvidia/cuda:12.6.3-runtime
     (1.53 GB comprimat), python:3.11-slim (~50 MB), pachetele pip (~1 GB pe imagine), sdist-ul
     llama-cpp-python (81 MB). Baza devel 12.6.3 (4.08 GB) e deja pe disc, in straturile lui
     `lcp-web:cuda`.
2. Ora la care se poate opri site-ul pentru teste (~1 ora, cu mail "Down" de la UptimeRobot);
   Firefox inchis inainte.

## Ce s-a verificat deja (22 nov, nu mai trebuie refacut)

1. llama-cpp-python 0.3.37: sdist 80.9 MB, sha256
   `bf4108fc76e933ea4969b61b1e281a2d232dd3e43361d1fdca5e2e029d62f729`, cu llama.cpp la commit
   a956a852 (15 nov 2026). L-am citit in scratchpad, fara sa rulez nimic din el:
   - are `GGML_BACKEND_DL` si `GGML_CPU_ALL_VARIANTS`. Pe x86 se compileaza 14 variante ale
     backend-ului CPU (x64, sse42, sandybridge, ivybridge, piledriver, haswell = AVX2, skylakex,
     cannonlake, cascadelake, icelake, cooperlake, zen4, alderlake, sapphirerapids). La rulare se
     incarca cea mai buna pe care o suporta procesorul (pe 3700X: haswell). Varianta x64 merge pe
     orice x86-64, deci nu apare "illegal instruction";
   - `Llama.__init__` cheama `llama_backend_init()`, care cheama `ggml_backend_load_all()` cand nu
     e inregistrat niciun backend. Bibliotecile se cauta in `GGML_BACKEND_DIR` (fixat la
     compilare), apoi in folderul executabilului (pentru Python, /usr/bin) si in folderul curent.
     Deci se compileaza cu
     `-DGGML_BACKEND_DIR=/opt/venv/lib/python3.11/site-packages/llama_cpp/lib`, iar regula de
     install a ggml pune acolo modulele (cuda si variantele CPU). CMakeLists-ul llama-cpp-python
     instaleaza doar tintele cu nume fix (ggml-cpu, ggml-cuda...), deci variantele
     `ggml-cpu-<nume>` ajung in folder numai prin `GGML_BACKEND_DIR`;
   - fara GPU (fara libcuda.so.1), libggml-cuda.so nu se poate incarca si e sarita fara mesaj.
     Imaginea cuda merge deci si pe CPU, fara stub-ul din Dockerfile.cuda;
   - mtmd (multimodal) se importa doar intr-un handler de chat multimodal, deci
     `-DLLAVA_BUILD=OFF` e sigur (mai putin de compilat);
   - modulele variantelor CPU nu au RPATH spre libggml-base. Cand se deschid, ea e insa deja
     incarcata (dupa soname). Se verifica la build (pasul 3, poarta b);
   - lista implicita de arhitecturi a llama.cpp, fara GGML_NATIVE, e 50/61/70/75/80-virtual,
     86-real, 89-real, 90-virtual. O inlocuim cu lista din decizii.
2. Imaginea de acum (`lcp-web:cuda`, 16.2 GB) are venv-ul de 3.1 GB: torch 754 MB, llama_cpp
   765 MB si site-packages/lib 778 MB. Roata pune fiecare biblioteca de 3 ori, ca fisiere copiate,
   nu ca symlink-uri (libggml-cuda.so are 257 MB doar pentru sm_75, de 3 ori). Regulile de install
   ale llama.cpp mai pun un set complet in site-packages/lib (plus include/, lib/cmake,
   lib/pkgconfig), pe care nu il foloseste nimeni: Python incarca din llama_cpp/lib. Cu 6 tinte
   CUDA ar fi ~1.3-1.5 GB pe copie, adica ~8 GB doar de copii. In imaginile noi setul din
   site-packages/lib si include se sterge, iar copiile identice din llama_cpp/lib devin
   symlink-uri.
3. Volumele (`lcp-hf` montat la /hf/hub):
   - GGUF-ul: 6.5 GiB;
   - google/gemma-4-12B-it-qat-q4_0-unquantized: 31 MB (doar tokenizer-ul);
   - encoderele: intfloat/multilingual-e5-base 1.1 GB, sentence-transformers/LaBSE 1.8 GB,
     xlm-roberta-base 1.1 GB (encoderul si tokenizer-ul fertilitatii, aceeasi revizie);
   - stanfordnlp/stanza-<limba> pentru 9 limbi: ~3.9 GB de zip-uri. Ele NU intra in imagine:
     Pipeline foloseste `download_method=None` si citeste doar `STANZA_RESOURCES_DIR`.
   `lcp-stanza` are 8.1 GB dezarhivati, cu toate procesoarele implicite (ner, depparse,
   sentiment, constituency...). In imagine intra doar fisierele deschise de tokenize, mwt, pos si
   lemma; marimea se masoara la export (estimat 2-3 GB).
4. Bazele. Marimi comprimate: nvidia/cuda:12.6.3-runtime-ubuntu24.04 1.53 GB, -devel 4.08 GB,
   12.8.1-runtime 2.16 GB. Runtime 12.6.3 cere `NVIDIA_REQUIRE_CUDA=cuda>=12.6`, cu exceptii
   pentru ramurile de driver 470, 535 si 550 (placi de datacenter, cu compatibilitate inainte).
   Pe server trebuie deci un driver >= 560, sau un driver 535/550 de datacenter; altfel
   nvidia-container-toolkit refuza pornirea. Ocolirea: `NVIDIA_DISABLE_REQUIRE=1`, cu
   compatibilitatea de versiune minora a CUDA 12 (driver >= 525). python:3.11-slim are acum Python
   3.11.18 (digest sha256:07d4824036af...).
5. Docker pe PC: 29.9.3, image store containerd (snapshotter), BuildKit 0.34.2, buildx 0.38.1. Cu
   containerd, `COPY --link` face straturi care nu depind de baza. Straturile cu modele au deci
   acelasi digest in ambele imagini: se pastreaza o data si se urca o data. Disc: C: are 75 GB
   liberi. In VM: imagini 16.6 GB, volume 23.9 GB, cache de build 16.2 GB.
6. Pagina (`static/app.js`), doua lucruri care conteaza pe alt server:
   - adresa API-ului: pagina vorbeste cu propria origine doar pe localhost, 127.0.0.1 si
     lcp.tail6e4ef5.ts.net. Servita de imagine pe alt domeniu, ar chema PC-ul (`PUBLIC_API`);
   - `estimate()` dubleaza estimarea cand `/api/health` spune `slow`, iar banner-ul `bnSlow` apare
     cat timp `slow` e true. Daca serverul scaleaza estimarea dupa `tok_s` (cerinta etapei),
     dublarea ar numara incetinirea de doua ori. Pe CPU (`tok_s` ~27, sub pragul de 700) `slow`
     ar fi mereu true.
7. `server.py`, `client_ip`: ia ultima intrare din X-Forwarded-For. E corect in spatele Funnel sau
   al unui proxy care adauga XFF (nginx cu `$proxy_add_x_forwarded_for`, Caddy). Cu portul expus
   direct, un client si-ar putea alege singur adresa: ar ocoli limita de 2 texte pe adresa si pe
   cea de 10 coduri gresite.
8. Python-ul de pe host merge cu `py -3 -I`, doar cu biblioteca standard. In Git Bash, `python`
   s-a blocat (aliasul Windows Store).

## Planul, pas cu pas

### Pas 1. .dockerignore si .gitignore

- `.dockerignore` la radacina, ca lista permisa: `*`, apoi `!lcp_model/`, `!lcp/`, `!server.py`,
  `!artifacts/`, `!static/`, `!docker/requirements.cpu.txt`, `!docker/requirements.server.txt`,
  apoi `**/__pycache__` si `**/*.pyc`. Asa `.env`, `bench/`, `reference/`, `build/`, `docs/` si
  `.git` nu ajung in context nici din greseala. Dockerfile.cuda si Dockerfile.cpu copiaza doar
  `docker/requirements.*.txt`, deci merg in continuare.
- Verificare: un build de proba care listeaza contextul (`FROM busybox`, `COPY . /ctx`,
  `RUN find /ctx -type f`, `--progress=plain --no-cache`).
- `.gitignore`: se adauga `build/`.

### Pas 2. scripts/export_models.py (in lcp-web:cuda, fara GPU)

    GPU=0 docker/run_cuda.sh python scripts/export_models.py --out /app/build/models

- HF: doar repo-urile si reviziile din cod:
  - `rater.GGUF`: doar fisierul .gguf, cu sha256 = `fetch_models.GGUF_SHA256`;
  - `signal_b.GEMMA4_QAT`: fisierele din `fetch_models.TOKENIZER_FILES`;
  - `signal_a.ENCODERS` pentru `lcp.encoders.DEFAULT`. xlmr are revizia `data.XLMR_REVISION`,
    folosita si la fertilitate.
  Se copiaza `snapshots/<rev>/*` ca fisiere reale (fara blobs/ si fara symlink-uri, care pe C: nu
  merg), plus `.no_exist/<rev>/` daca exista. Cu revizii fixate (hash), HF offline gaseste
  fisierele direct in `snapshots/<rev>/`, fara refs/. Daca in snapshot apare alt fisier, il
  afisezi si nu il copiezi pana nu e explicat.
- stanza: pentru fiecare limba din `data.STANZA_LANGS`, intr-un proces separat cu
  `sys.addaudithook` (evenimentul "open"), rulezi `Segmenter().pipeline(lang)` si segmentarea lui
  `bench/texts/<lang>_1.txt` si `_2.txt`. Se copiaza fisierele deschise de sub /stanza, plus
  `resources.json`. Se incarca o limba odata, ca sa nu iei memorie de la site.
- Poarta a (stanza): un proces nou, cu `STANZA_RESOURCES_DIR=build/models/stanza` si
  `HF_HUB_CACHE` spre un folder gol. Segmentarea textelor bench (1 si 2 paragrafe, 9 limbi)
  trebuie sa iasa identica cu cea din /stanza complet: text, start, end, lemma, upos si content pe
  fiecare cuvant. Altfel te opresti si raportezi.
- Poarta b (HF): un proces nou, cu `HF_HUB_CACHE=build/models/hf` si `HF_HUB_OFFLINE=1`. Se
  incarca tokenizer-ul Gemma (id-urile cifrelor 236770, 236778, 236800, 236812, 236810), cele 3
  encodere (`signal_a.Encoder`) si tokenizer-ul xlm-roberta-base; se verifica calea GGUF-ului si
  sha256-ul lui. Gemma nu se incarca (RAM; site-ul ruleaza).
- `build/models/MANIFEST.txt`: cale, marime si sha256 pe fiecare fisier, plus totaluri pe parte.
  O copie merge in `bench/results/etapa6_models_manifest.txt` (fara text). Containerul nu atinge
  placa.

### Pas 3. docker/Dockerfile

`# syntax=docker/dockerfile:1`, `ARG TARGET=cuda`. Etapele:

- build-cuda: `FROM --platform=linux/amd64 nvidia/cuda:12.6.3-devel-ubuntu24.04`, Python 3.11 din
  deadsnakes (python3.11, -venv, -dev), build-essential, cmake, git (ca in Dockerfile.cuda).
- build-cpu: `FROM --platform=linux/amd64 python:3.11-slim`, build-essential, cmake, git.
- build: `FROM build-${TARGET}`, `ARG TARGET`. Venv in /opt/venv (`python3.11 -m venv`), torch
  2.13.0 din indexul CPU, `requirements.cpu.txt`, apoi llama-cpp-python 0.3.37 cu `--no-binary`
  si `CMAKE_ARGS`:
  - pentru ambele: `-DGGML_NATIVE=OFF -DGGML_BACKEND_DL=ON -DGGML_CPU_ALL_VARIANTS=ON
    -DGGML_BACKEND_DIR=/opt/venv/lib/python3.11/site-packages/llama_cpp/lib -DLLAVA_BUILD=OFF`;
  - pentru cuda, in plus: `-DGGML_CUDA=on` si
    `-DCMAKE_CUDA_ARCHITECTURES='75-real;80-real;86-real;89-real;90-real;90-virtual'`. Pune lista
    in ghilimele (CMAKE_ARGS se imparte la spatii) si verifica in log-ul cmake ca a ajuns intreaga;
  - `CMAKE_BUILD_PARALLEL_LEVEL=4`: site-ul ruleaza in acelasi VM de 12 GB, iar nvcc ia ~1-2 GB pe
    job.
  La sfarsit `requirements.server.txt`, tot ultimul, ca acum.
- Curatarea, in etapa build, inainte de copiere:
  - din site-packages/lib se sterg doar libggml*, libllama*, libmtmd*, cmake/ si pkgconfig/, iar
    din site-packages/include doar ggml*, gguf*, llama* si mtmd*. Listeaza intai; un folder ramane
    doar daca mai are altceva;
  - in llama_cpp/lib, fisierele identice devin symlink-uri (libX.so -> libX.so.1 ->
    libX.so.1.0.0).
- Portile la build (build-ul pica daca nu trec):
  - a) cuda: `cuobjdump --list-elf libggml-cuda.so` contine exact sm_75, sm_80, sm_86, sm_89 si
    sm_90, iar `cuobjdump --list-ptx` contine sm_90 (PTX compute_90);
  - b) ambele: `llama_cpp.llama_backend_init()`, apoi prin ctypes pe `llama_cpp.llama_cpp._lib`
    (`ggml_backend_reg_count`, `ggml_backend_reg_get`, `ggml_backend_reg_name`) se verifica faptul
    ca backend-ul CPU e incarcat. Din /proc/self/maps se citeste varianta incarcata (la build:
    haswell pe 3700X). In folder trebuie sa fie 14 fisiere libggml-cpu-*.so, plus libggml-cuda.so
    la cuda. In build nu exista GPU, deci CUDA nu se incarca; e normal.
- run-cuda: `FROM nvidia/cuda:12.6.3-runtime-ubuntu24.04`, python3.11 din deadsnakes
  (software-properties-common se scoate la loc in acelasi RUN), libgomp1.
- run-cpu: `FROM python:3.11-slim`, libgomp1, `ENV LCP_SLOW_TOK_S=0`. Pe CPU proba da ~27 de
  tokeni/s; fara asta banner-ul "server lent" ar sta mereu pe pagina.
- final: `FROM run-${TARGET}`, in ordinea asta (straturile mari si stabile primele):
  - `COPY --link --from=models`, cate un COPY pe folder: GGUF-ul (6.5 GiB), apoi fiecare din
    cele 4 repo-uri HF, apoi stanza si MANIFEST.txt, sub /models/hf si /models/stanza;
  - `COPY --link --from=build /opt/venv /opt/venv`;
  - `COPY --link` pentru lcp_model/, lcp/, server.py, artifacts/ si static/, in /app;
  - utilizatorul lcp (uid 10001, home /home/lcp), cu /home/lcp/.nv al lui, pentru cache-ul JIT
    CUDA;
  - `ENV PATH=/opt/venv/bin:$PATH PYTHONPATH=/app/lcp_model:/app PYTHONUNBUFFERED=1
    PYTHONDONTWRITEBYTECODE=1 HF_HUB_CACHE=/models/hf HF_HUB_OFFLINE=1
    STANZA_RESOURCES_DIR=/models/stanza`;
  - poarta c: `ldd` pe llama_cpp/lib/*.so fara "not found" si
    `python -c "import torch, transformers, stanza, llama_cpp, sklearn, MeCab, fastapi"`;
  - `EXPOSE 8000`; HEALTHCHECK pe /api/health ca in docker-compose.yml, cu start-period 300s (pe
    CPU, incarcarea plus proba iau ~2-3 min); `USER lcp`; `WORKDIR /app`;
    `CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]`.
- Comenzile de build:

      docker build -f docker/Dockerfile --build-arg TARGET=cuda --build-context models=build/models -t lcp-web:server-cuda .
      docker build -f docker/Dockerfile --build-arg TARGET=cpu --build-context models=build/models -t lcp-web:server-cpu .

  Numele `lcp-web:cuda` ramane al site-ului de pe PC.
- Dockerfile.cuda si Dockerfile.cpu raman (site-ul de aici si Mac-ul). In capul lor se scrie ca
  imaginea portabila e docker/Dockerfile.

### Pas 4. Codul: server.py, lcp/pipeline.py, static/app.js

Valorile implicite pastreaza exact site-ul de acum.

- `server.py`, setarile llama.cpp:
  - `LCP_GPU_LAYERS`, `LCP_N_CTX`, `LCP_N_BATCH` si `LCP_THREADS` sunt intregi, iar
    `LCP_FLASH_ATTN` e 1/0 sau true/false. Goale = None, deci raman valorile din
    `artifacts/params.json` (49, true, 1024, 256) si `os.cpu_count()` pentru thread-uri. Se dau
    constructorului `Pipeline`, care are deja parametrii;
  - configuratia efectiva se logheaza la incarcare si apare in /api/health: `"config"` (n_gpu_layers,
    n_ctx, n_batch, flash_attn, n_threads) si `"gpu"` (daca llama.cpp are un dispozitiv GPU, prin
    `llama_supports_gpu_offload`);
  - n_ctx sub 512 da eroare la pornire (PIECE_TOKENS 192 plus promptul);
  - `LCP_THREADS` conteaza cand containerul are limita de CPU: `os.cpu_count()` vede toate
    nucleele gazdei.
- `server.py`, `LCP_TRUST_XFF`: implicit 1, ca acum; 0 = adresa conexiunii (port expus direct,
  fara proxy).
- `lcp/pipeline.py`, `languages()`:
  - est = `EST_S_PER_1000[L] * (0.08 + 0.92 * 1000 / tok_s)`, cu tok_s = `self.speed["tok_s"]`
    (ultima proba). 1000 e proba placii de aici cand s-a masurat EST (974-1009 cand e sanatoasa).
    0.92 e partea lui B din total (etapa 7, median); segmentarea si A raman pe CPU;
  - raspunsul primeste si `"est_tok_s"`;
  - efectul: pe PC-ul sanatos estimarea ramane in +-3%; in spill (372) creste de 2.5 ori; pe CPU
    (~27) de 34 de ori, adica ~10 min la 1000 de caractere in engleza. Se potriveste cu etapa 7:
    GPU-ul a fost de 34-36 de ori mai rapid pe aceleasi texte.
- `static/app.js`:
  - `API = ""` (propria origine) pentru orice pagina http(s) care nu e pe *.vercel.app.
    `PUBLIC_API` ramane pentru Vercel si se schimba la mutare. Pe localhost, 127.0.0.1 si ts.net
    comportamentul ramane acelasi;
  - `estimate()` dubleaza la slow doar cand /api/languages nu are `est_tok_s` (server vechi).
  Pagina de pe ts.net le ia imediat (static din repo), cea de pe Vercel dupa push.
- Pe site-ul live, server.py si pipeline.py noi intra la restartul de la teste: la pasul 9,
  `docker compose start api` reporneste procesul din repo-ul montat. Imaginea cuda le testeaza
  inainte.
- Teste fara GPU, inainte de build:
  - sintaxa (py_compile);
  - un server cu pipeline fals in lcp-web:cuda fara GPU (ca la audit), pentru variabilele de
    mediu, `est_tok_s` si `LCP_TRUST_XFF`;
  - pagina in Chrome headless cu API-ul fals, pentru cele doua schimbari din app.js. Scripturile
    din Etapa 5 erau in scratchpad-ul vechi, probabil sterse: refa doar verificarile noi.

### Pas 5. scripts/compare_api.py (pe host, doar biblioteca standard)

- `--url U --save F.json`: trimite textele bench (implicit 1 paragraf, 11 limbi) la
  /api/analyze si pastreaza, pe fiecare cuvant: start, end, kind, level, score, A, B, fused, plus
  timpii. Textul cuvintelor nu se pastreaza (doar offseturi si numere), deci F.json poate sta in
  bench/results.
- `--url U --against F.json`: aceleasi cereri, apoi comparatia. Porti fixate dinainte, pentru GPU:
  - aceleasi cuvinte (offseturi si kind) peste tot;
  - |dA| maxim sub 1e-3 (acelasi torch, acelasi CPU);
  - r pe B si pe scor >= 0.999 (pe GPU rezultatul nu e bit-identic; in etapa 7, r 0.9991 intre
    moduri);
  - nivel identic pe >= 97% din cuvinte si niciodata o diferenta mai mare de 1 nivel.
  La imaginea cpu pragul e cel al paritatii din etapa 7, r pe scor >= 0.99; nivelurile doar se
  raporteaza.
- Referinta se ia de pe site-ul live, inainte de oprire:
  `bench/results/etapa6_ref_live.json`. Ramane si pentru serverul nou (acelasi test acolo).

### Pas 6. docker-compose.server.yml

- `name: lcp-web-server`. Un bloc comun (`x-api`): `restart: unless-stopped`, `env_file` .env
  (`required: false`), `ports: "${LCP_BIND:-127.0.0.1}:${LCP_PORT:-8000}:8000"`, healthcheck din
  imagine.
- Serviciul gpu (profilul gpu): `image: ${LCP_IMAGE_GPU:-lcp-web:server-cuda}`, placa NVIDIA
  (`deploy.resources.reservations.devices`, ca acum) si volumul `cuda-cache` la /home/lcp/.nv, cu
  `CUDA_CACHE_MAXSIZE=4294967296`. Astfel codul compilat JIT pentru placile fara cod nativ ramane
  intre porniri.
- Serviciul cpu (profilul cpu): `image: ${LCP_IMAGE_CPU:-lcp-web:server-cpu}`.
- Un singur profil odata (acelasi port). Pornirea:
  `docker compose -f docker-compose.server.yml --profile gpu up -d`.
- Nu atinge docker-compose.yml: e alt proiect, cu alt nume; la teste foloseste `LCP_PORT=8001`.

### Pas 7. Build-urile (dupa aprobare)

- Ordinea: prune, export, build cuda, build cpu. Da statusuri dese (Monitor filtrat pe pasii din
  Dockerfile, pe erori si pe timp). Intre build-uri verifica /api/health al site-ului (sa nu fie
  afectat) si memoria VM-ului.
- Timpi estimati, nemasurati: export 10-15 min; cuda 1-2 h (6 tinte CUDA plus 14 variante CPU, cu
  4 joburi); cpu 20-40 min.
- Disc:
  - build/models: ~13 GB pe C:;
  - in VM, cu containerd fiecare strat se tine si comprimat, si dezarhivat: modelele ~25 GB (o
    data pentru ambele imagini), bazele si venv-urile ~10 GB, cache-ul de build ~8 GB;
  - total ~45-55 GB, fata de 75 GB liberi pe C: plus 16 GB eliberati de prune.
  Dupa ce trec testele, build/models si cache-ul de build se pot sterge (cu aprobare).

### Pas 8. Verificari fara oprirea site-ului

- Marimile (`docker images`, `docker history`) si straturile comune ale celor doua imagini:
  acelasi digest la modele (`docker inspect`, RootFS.Layers).
- Continutul: /app are doar lcp_model, lcp, server.py, artifacts si static; /models corespunde
  exact cu MANIFEST.txt (find + du); nimic din bench/, reference/, .env sau .git.
- Codul de acces:
  - il citesti din .env intr-o variabila si nu il afisezi niciodata. Linia e comentata acum, cu
    "#";
  - `docker create` + `docker cp` pentru /app si /models/MANIFEST.txt, in scratchpad;
  - `grep -qF` pe host, cu rezultatul doar da/nu; apoi stergi copia.
- Imaginile nu se pornesc cu site-ul pornit: chiar fara GPU, Gemma ar lua ~10 GB de RAM. Toate
  rularile sunt la pasul 9.

### Pas 9. Testele, cu site-ul oprit, la ora aleasa de Alexandru

0. Inainte de oprire, cu site-ul pornit: noteaza `tok_s` din /api/health si ruleaza
   `compare_api.py --url http://127.0.0.1:8000 --save bench/results/etapa6_ref_live.json` (11
   texte de 1 paragraf). In spill dureaza de ~3 ori mai mult, dar numerele ies aceleasi.
1. Firefox inchis; `docker compose stop api` (sau `scripts\site_stop.cmd`); Alexandru primeste
   mail "Down"; nvidia-smi: VRAM sub ~500 MiB.
2. Imaginea cuda pe portul 8001: `LCP_PORT=8001 docker compose -f docker-compose.server.yml
   --profile gpu up -d` (sau `docker run --gpus all -p 127.0.0.1:8001:8000`). Verifici:
   - /api/health ok, `tok_s` ~1000, `"gpu": true`, config 49/1024/256 cu flash attention;
     incarcarea ~70 s;
   - varianta CPU incarcata: libggml-cpu-haswell.so in /proc/1/maps din container;
   - `scripts/api_check.py --url http://127.0.0.1:8001 --parts texts --sizes 1 --out
     <scratchpad>`: PASS, median ~15 s;
   - `compare_api.py --url http://127.0.0.1:8001 --against bench/results/etapa6_ref_live.json`:
     portile din pasul 5;
   - VRAM (nvidia-smi): ~7.4 GB.
3. Aceeasi imagine cu `--network none`: trebuie sa porneasca (health prin `docker exec` cu python
   urllib) si sa analizeze un text scurt tot prin `docker exec`. Asta dovedeste ca nu descarca
   nimic. Apoi o opresti.
4. Imaginea cpu pe 8001, fara `--gpus`:
   - health (`tok_s` ~27, `slow` false);
   - un text scurt si en_1 (`compare_api.py --langs en`);
   - memoria de varf: `memory.peak` din cgroup-ul containerului si `docker stats` la 5 s;
   - s/citire si estimarea din /api/languages fata de timpul masurat.
   Asteptat: ~10-11 GB; VM-ul are 12 GB plus 8 GB swap. Daca nu incape (OOM, sau swap care
   blocheaza progresul), te opresti si raportezi cifra. Optional: imaginea cuda fara `--gpus`
   (merge pe CPU, libggml-cuda e sarita), doar health.
5. `docker compose start api` (sau `scripts\site_start.cmd`). Verifici:
   - `tok_s` ~1000. Sub 700 inseamna spill: cu acordul lui Alexandru se inchid aplicatiile care
     folosesc placa si se reporneste;
   - `"config"` si `est_tok_s` in raspunsuri;
   - calea publica, cu `curl --resolve`.
   Acesta e si restartul cerut pentru spill-ul din 22 nov.
   Optional, daca ramane timp: `scripts/pipeline_check.py` in imaginea cuda, cu scripts/ si
   ../lcp-paper/release montate read-only (poarta din etapa 4, pe drumul codului din imagine).

### Pas 10. Documentele si staging-ul

- README, sectiunea Stage 6:
  - fisierele: docker/Dockerfile, .dockerignore, scripts/export_models.py, scripts/compare_api.py,
    docker-compose.server.yml;
  - build-ul: exportul plus cele doua build-uri;
  - rularea pe alt server: Docker >= 24 cu compose >= 2.24, nvidia-container-toolkit, driverul de
    la "Ce s-a verificat", punctul 4;
  - .env pe serverul nou: LCP_ACCESS_CODE, LCP_CORS_ORIGINS cu noul domeniu, LCP_TRUST_XFF,
    LCP_SLOW_TOK_S (~70% din `tok_s` normal al placii), LCP_N_CTX 2048 pe placi de 16 GB sau
    mai mari;
  - un proxy in fata (Caddy sau nginx) pentru HTTPS, si `PUBLIC_API` din static/app.js pentru
    pagina de pe Vercel;
  - testul pe serverul nou: compare_api `--against etapa6_ref_live.json` si api_check;
  - mutarea imaginii.
- Mutarea, doar documentata:
  - a) fara registry: `docker save lcp-web:server-cuda lcp-web:server-cpu | zstd` (straturile cu
    modele o singura data, ~13-15 GB), apoi scp/rsync si `docker load` pe server;
  - b) registry privat, de exemplu ghcr.io: docker login, docker tag, docker push (~15 GB de
    upload). Inainte verifici limitele de stocare pentru pachete private pe planul contului
    GitHub (Free avea 500 MB);
  - c) build pe server: cere build/models copiat, sau fetch_models.py online acolo, cu aceleasi
    revizii si sha256.
- `docs/PLAN.md`: Etapa 6 e actualizata din planificare; completeaza ce se schimba la executie.
- `bench/results/concluzie_etapa6.txt`: ce s-a construit, marimile, portile, testele (cu cifre),
  ce nu s-a testat (alte generatii de placi, Blackwell prin JIT, alt procesor) si ce urmeaza.
- `git add` pe fisierele noi si schimbate (fara build/, fara .env), apoi comenzile de git pentru
  Alexandru.

## Marimi estimate

- Modelele: ~13 GB (GGUF 6.5 GiB, encodere 4 GiB, tokenizer 31 MB, stanza 2-3 GB estimat).
- Imaginea cuda: ~19-20 GB (runtime ~3.5 GB dezarhivat, venv ~1.7 GB, libggml-cuda ~1.3-1.5 GB).
- Imaginea cpu: ~15 GB.
- Transfer sau upload: ~15 GB, cu modelele o singura data.

## De stiut

- Imaginea CPU e doar rezerva. Pe 8 nuclee x86 (3700X), B face ~27 de tokeni/s: un paragraf
  dureaza ~4-9 minute si doua ~12 minute (concluzie_etapa7_pc.txt, sectiunea 5), de ~35 de ori
  mai lent decat placa de aici. Memoria pe CPU: Gemma reimpachetat ~5.8 GB, plus encoderele si
  stanza, deci ~10-11 GB; incape in VM-ul de 12 GB doar cu site-ul oprit.
- Placa de aici e sm_75; celelalte generatii nu se pot testa pe PC. Se verifica doar ca biblioteca
  CUDA contine codul pentru toate (poarta a din pasul 3). Pe Blackwell, prin PTX, prima pornire
  compileaza JIT (durata nemasurata, probabil minute); cache-ul ramane in volumul cuda-cache.
- B pe alta placa nu e bit-identic (alt cod SASS, alte nuclee). Statisticile lui B (etapa 3) raman
  cele de pe 2070 SUPER. Pe serverul nou se ruleaza compare_api `--against`, cu pragurile din
  pasul 5.
- Mutarea propriu-zisa nu se face in sesiunea asta; doar se documenteaza.

## Mediul (verificat)

- RTX 2070 SUPER 8 GB (driver 621.24), Ryzen 7 3700X, 16 GB RAM, Docker Desktop cu WSL2 (12 GB,
  16 CPU). Python-ul de pe host (3.14) are numpy stricat; biblioteca standard merge (`py -3 -I`).
- Git Bash: `MSYS_NO_PATHCONV=1` si `pwd -W` (vezi `docker/run_cuda.sh`).
- Firefox deschis = spill la pornire (in 22 nov: 561 MiB ocupati, 557 tokeni/s; inchis: 478 MiB,
  1009).
- Chrome headless pentru pagina: `C:\Program Files\Google\Chrome\Application\chrome.exe` cu
  `--disable-gpu` (Edge nu are executabil pe acest PC).

## Reguli (neschimbate)

- Nu da commit si nu face push. Pregatesti fisierele si staging-ul; commit-ul il da Alexandru.
  Comenzile de git in engleza, cu mesaje scurte care descriu schimbarea, FARA prefixe de tipul
  "Stage 6:" si FARA linii `Co-Authored-By`.
- Cere aprobare inainte de `docker build`, de orice descarcare mare si de curatarea cache-ului.
- Nu opresti si nu repornesti site-ul fara sa intrebi; ii spui lui Alexandru ca va primi mail
  "Down".
- Nu intra in git sau in imagini text din MLSP, RoLCP sau CompLex. Codul de acces nu apare in git,
  in imagini, in memorie sau in chat.
- Fara subagenti; verifici singur.
- In chat: romana fara diacritice, fara tabele markdown, explicatii scurte. La rularile lungi
  (build, teste) dai statusuri dese.
- Daca o poarta pica sau ceva nu incape in memorie, te opresti si raportezi cifra.
