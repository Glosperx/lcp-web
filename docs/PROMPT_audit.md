# Prompt pentru o sesiune noua Claude Code pe PC: auditul a tot ce s-a facut pana acum

Scris pe PC pe 22 nov 2026, dupa Etapa 8 (commit `4d4c655`). Sesiunea asta NU construieste etape
noi. Verifica ce exista: buguri, cerinte din plan care lipsesc sau sunt facute pe jumatate,
documentatie care nu se potriveste cu codul. La final pregateste promptul pentru sesiunea urmatoare
(Etapa 5).

## Unde suntem

- Facute: Etapa 1 (timpi pe CPU, Mac), Etapa 7 pe PC (configuratia GPU), Etapele 2 si 3 (modelul
  exportat si B-ul site-ului), Etapa 4 (pipeline si API in flux) si Etapa 8 (serverul si hostingul).
  Raman Etapa 5 (frontend-ul adevarat), Etapa 6 (imaginea finala) si benchmark-ul final prin API.
- Fiecare etapa facuta are o concluzie in `bench/results/concluzie_*.txt`, cu cifrele si deciziile.
- Site-ul e live 24/7:
  - pagina statica pe Vercel: https://lcp-web-static.vercel.app (proiectul `lcp-web`, Root
    Directory `static`, deploy automat la push);
  - API-ul pe GPU-ul acestui PC, in `docker compose` (`docker-compose.yml`), expus doar prin
    Tailscale Funnel: https://lcp.tail6e4ef5.ts.net -> 127.0.0.1:8000;
  - UptimeRobot verifica `/api/health` la 5 minute si trimite mail cand pica.
- Cifra site-ului: media r pe 11 limbi 0.691328 (paperul are 0.692521), din B calculat cu
  llama.cpp pe GPU in modul site-ului.

Citeste intai, intregi:
- `docs/PLAN.md` (cerintele initiale pe etape), `docs/PROMPT_etapa2_3_pc.md`,
  `docs/PROMPT_etapa7_pc.md`, `README.md`, toate `bench/results/concluzie_*.txt`;
- codul: `lcp/*.py`, `server.py`, `static/index.html`, `scripts/export_model.py`,
  `scripts/b_reference.py`, `scripts/pipeline_check.py`, `scripts/api_check.py`,
  `scripts/site_start.ps1`, `scripts/site_stop.ps1`, `docker/*`, `docker-compose.yml`,
  `.env.example`, `.gitignore`, `.gitattributes`;
- `git log --oneline` pentru istoric.

Memoria din `C:\Users\glosper\.claude\projects\c--Users-glosper-Documents-lcp-web\memory\` are
starea pe etape, dar verifici totul in cod, nu in memorie.

## Decizii luate de Alexandru dupa PLAN.md (nu sunt buguri)

Planul e din 21 nov. Abaterile de mai jos sunt cerute explicit. Verifici doar ca sunt implementate
corect si documentate:
- Nu exista limita fixa de 2000 de caractere. Peste `warn_chars` (2000, ja 700) frontend-ul cere
  confirmare, cu estimarea de timp `est_s_per_1000_chars`. Limita dura e 20000 (413).
- Pana la 6 texte ruleaza alternat, propozitie cu propozitie, cu coada de 16. Textul e segmentat
  pe paragrafe. Propozitiile lungi se impart in bucati (<= 192 tokeni, <= 40 de cuvinte).
- Cuvintele functionale SUNT colorate, ca nivel 1, fara model (`"function": true`). Planul spunea
  "raman text normal".
- Serverul e PC-ul de acasa, nu un server in cloud. Pagina e pe Vercel, iar API-ul trece prin
  Tailscale Funnel. Etapa 8 s-a facut inaintea Etapei 5.
- Accesul se face cu cod: antetul `X-Access-Code` si `POST /api/auth`. 10 coduri gresite de la o
  adresa in 10 minute dau 429. O adresa poate avea cel mult 2 texte deodata. Nu exista limita pe
  ora.
- Pagina din `static/index.html` e o pagina de test, nu frontend-ul Etapei 5. Etapa 5 nu e inceputa.
- Scala de afisare (percentila in limba, trecuta prin cuantilele etichetelor) iese mai ales verde
  pe texte reale: niveluri 50/35/10/3/2%. E o decizie deschisa pentru Etapa 5, nu un bug.
- Pe GPU, refolosirea KV nu e bit-identica (r 0.9991). De aceea statisticile lui B s-au calculat
  in modul site-ului.

## Ce verifici, in ordine

### 1. Acoperirea cerintelor

Pentru fiecare etapa din `docs/PLAN.md` (si din prompturile etapelor 2-3 si 7) faci o lista:
cerinta, unde e implementata (fisier:linie), si starea ei: facuta, partiala, lipsa, sau schimbata
prin decizie. Fara presupuneri: fiecare "facuta" are dovada in cod sau in rezultate. Exemple de
urmarit:
- nota de pe site ca scorurile se compara doar in aceeasi limba si r-ul pe limba;
- "fara text din MLSP pe site";
- `lcp_model/` copiat NESCHIMBAT din release: compari cu `../lcp-paper/release/`;
- Etapa 6, profilele cpu/gpu din compose si `scripts/benchmark.py` din Etapa 7 (probabil lipsa,
  confirmi).

### 2. Buguri in cod

Cauti buguri reale, cu un scenariu concret: ce intrare sau ce stare duce la ce rezultat gresit.
Fiecare suspiciune o confirmi cu un test mic inainte s-o declari bug. Puncte de verificat (sunt
ipoteze, nu concluzii):
- **Pozitiile cuvintelor:** Python numara caractere (code points), JavaScript numara unitati
  UTF-16. Cu emoji sau caractere din afara BMP in text, colorarea se poate decala. Testezi pe
  server si in logica paginii.
- **Escaparea HTML in pagina:** textul utilizatorului, lema si orice camp venit de la server.
- **Citirea fluxului NDJSON:** linii taiate intre doua bucati de date, evenimentele ping/queued,
  `error`, un al doilea Analizeaza pornit cat ruleaza primul.
- **server.py:**
  - slotul pe adresa se elibereaza pe toate caile (413, 429, 503, exceptii, deconectare);
  - dictionarele pe adresa (esecuri, sloturi) se golesc in timp, nu cresc la nesfarsit;
  - `hmac.compare_digest` cu un cod non-ASCII (in antet sau in JSON) da 500 in loc de 401?
  - un corp de cerere foarte mare (MB) e citit intreg inainte de verificarea lungimii?
  - dupa o eroare in firul de lucru (`W.error`), cum isi revine serverul? Docker NU reporneste un
    container unhealthy, il reporneste doar daca procesul iese;
  - ce rute sunt publice prin Funnel (de exemplu `/openapi.json`, alte fisiere servite static)?
  - regex-ul CORS se potriveste pe toata originea, nu doar pe un prefix?
- **lcp/pipeline.py si lcp/fusion.py:**
  - rotunjirea nivelului (`round` in Python rotunjeste .5 la par) e aceeasi ca in Etapa 3?
  - offseturile dupa impartirea propozitiilor lungi si dupa crop;
  - cuvintele functionale pe fiecare limba (si fil/si, care merg pe regex);
  - text gol, doar spatii, doar punctuatie, un singur cuvant, paragrafe goale;
  - anularea la deconectare chiar opreste citirile.
- **scripts/site_start.ps1 si site_stop.ps1:** cazurile in care Docker, nvidia-smi sau Tailscale
  lipsesc sau nu raspund. ATENTIE: `site_stop.cmd` nu are optiune de ajutor; orice rulare opreste
  site-ul de-adevaratelea.
- **Documentatia fata de cod:** cifre si comportamente din README, din docstring-urile din
  `server.py` si din concluzii. De exemplu, docstring-ul spune ~40 s de incarcare, iar acum se
  masoara 65-79 s.

### 3. Securitate si regulile datelor

- Codul de acces sta doar in `.env` (gitignored). Verifici ca nu apare in niciun fisier urmarit si
  in tot istoricul git (`git log -p --all`, cu `grep -F` pe valoarea citita in variabila).
  Valoarea nu o afisezi niciodata.
- Nimic din MLSP, RoLCP sau CompLex in fisierele urmarite din `main`. Metoda: incarci propozitiile
  din `/paper/release` in container si cauti potriviri (de exemplu secvente de 8 cuvinte) in
  fisierele text urmarite. Raportezi doar numarul de potriviri si fisierele, nu textul. Exceptie
  cunoscuta: branch-ul `lcp_model` e repo-ul vechi al paperului (cu date). Nu se face merge in
  main si nu-l auditezi. Textele din `bench/texts/` sunt de pe Wikipedia (CC BY-SA), deci sunt in
  regula.
- Logurile serverului nu contin textele trimise. Verifici in cod si in `docker compose logs api`.
- Portul e legat la 127.0.0.1, X-Forwarded-For nu se poate falsifica prin Funnel, CORS e corect.

### 4. Teste

- Site-ul e folosit. NU il opresti fara sa intrebi. Orice test care ia GPU-ul (de exemplu
  `pipeline_check.py`) cere oprirea lui:
  - intrebi intai;
  - opresti cu `scripts\site_stop.cmd` si pornesti la loc cu `scripts\site_start.cmd`;
  - la final verifici `/api/health`;
  - ii spui lui Alexandru ca va primi mail "Down".
- Fara GPU: `GPU=0 docker/run_cuda.sh python ...`. Python-ul de pe host (3.14) are numpy stricat,
  asa ca rulezi Python in container. Ai grija la RAM: containerul live ia ~7.2 GB din 12 GB de WSL.
  Verifici `docker stats` inainte sa pornesti al doilea container cu encodere.
- `scripts/api_check.py` merge pe serverul live (`--url http://127.0.0.1:8000`, codul cu
  `--code "$CODE"` citit din `.env` intr-o variabila). Partile lungi tin serverul ocupat cateva
  minute, deci incepi cu `--parts access texts`.
- Bugurile confirmate primesc un test mic de reproducere. Il tii in scratchpad, nu in repo, daca
  nu e util pe termen lung.

## Ce livrezi

1. `bench/results/audit.txt` (romana fara diacritice):
   - acoperirea cerintelor, pe etape;
   - apoi constatarile, de la cea mai grava la cea mai mica: bug confirmat, bug probabil, cerinta
     lipsa, documentatie gresita, detaliu;
   - la fiecare constatare: fisier:linie, scenariul, cum s-a confirmat, repararea propusa.
2. In chat, un rezumat scurt. Apoi il intrebi pe Alexandru ce repari acum.
3. Repari ce alege el. Verifici fiecare reparatie cu testul ei si pui in staging. Daca reparatia
   atinge `server.py` sau `lcp/`, repornesti containerul (`docker compose restart api`, ~75 s jos,
   dupa ce intrebi) si verifici `/api/health` local si public.
4. La final scrii `docs/PROMPT_etapa5.md`, promptul pentru sesiunea urmatoare:
   - starea dupa audit si ce a ramas nereparat;
   - protocolul NDJSON si campurile pe care se construieste frontend-ul;
   - cerintele Etapei 5 din PLAN, cu deciziile de mai sus;
   - cele trei decizii de cerut lui Alexandru inainte de cod: scala de culori (cum e acum sau
     recalibrata pe texte obisnuite), limba interfetei (ro, en sau ambele) si skill-ul
     `apple-design` (nu e instalat; il instaleaza el sau se lucreaza fara);
   - regulile de mai jos.
5. Actualizezi memoria (fisierele de stare pe etape) cu rezultatul auditului.

## Mediul (verificat, nu mai trebuie redescoperit)

- RTX 2070 SUPER 8 GB, Ryzen 7 3700X, 16 GB RAM, Docker Desktop cu WSL2 (12 GB). Imaginea
  `lcp-web:cuda` si volumele `lcp-hf` si `lcp-stanza` sunt pline: nu e nevoie de build sau
  descarcari.
- VRAM-ul liber inainte de GPU trebuie sa fie sub ~700 MiB folosit, altfel modelul trece in
  memoria shared (WDDM), fara eroare, iar citirile merg ~2x mai incet. Urmaresti
  `\GPU Process Memory(*)\Shared Usage` (procesul `vmwp`; ~110-190 MiB e normal). Firefox poate
  lua sute de MiB de VRAM.
- Git Bash: `MSYS_NO_PATHCONV=1` si `pwd -W` (deja in `docker/run_cuda.sh`).
- Tailscale CLI: `"C:\Program Files\Tailscale\tailscale.exe"`. Pe PC, MagicDNS raspunde cu adresa
  din tailnet, deci calea publica o testezi asa:
  `curl --resolve lcp.tail6e4ef5.ts.net:443:<IP A din DNS public, de ex. prin cloudflare-dns.com> ...`
- Tunelul Funnel trece mereu prin releul DERP (Frankfurt). Dupa restartul PC-ului a fost mai lent:
  0.8-7 s pe o conexiune noua, ~0.2 s pe una deja deschisa. E cunoscut si nu e bug in cod.

## Reguli (neschimbate)

- Nu da commit si nu face push. Pregatesti fisierele si staging-ul, iar commit-ul il da Alexandru.
  Comenzile de git i le dai in engleza, cu mesaje scurte, FARA linii `Co-Authored-By` sau alta
  atribuire.
- Cere aprobare inainte de `docker build` si de orice descarcare mare.
- Nu intra in git text din MLSP, RoLCP sau CompLex (repo-ul e privat, dar regula ramane). In
  loguri, nu printezi propozitii din date.
- Codul de acces nu apare in git, in memorie, in `static/` sau in chat. In teste il citesti din
  `.env` intr-o variabila.
- Nu opresti si nu repornesti site-ul fara sa intrebi.
- Fara subagenti; verifici singur.
- In chat: romana fara diacritice, fara tabele markdown, explicatii scurte. La rularile lungi dai
  statusuri dese: progres, s/citire, VRAM.
- Daca o poarta pica sau ceva nu incape in memorie, te opresti si raportezi cifra, fara sa ocolesti.
