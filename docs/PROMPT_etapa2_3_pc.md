# Prompt pentru urmatoarea sesiune Claude Code pe PC: Etapele 2 si 3 (exportul modelului si B de referinta)

Scris pe PC pe 22 nov 2026, dupa Etapa 7 pe PC. Tot ce trebuie e aici, in `docs/PLAN.md`, in
`README.md` si in `bench/results/`.

## Ce s-a decis si unde suntem

- Serverul site-ului e, deocamdata, chiar PC-ul acesta, cu GPU-ul lui. Configuratia lui B e fixata la
  Etapa 7: `--gpu-layers 49 --flash-attn --n-ctx 1024 --n-batch 256`, ~7.4 GB VRAM, 0.08 s/citire cu
  refolosirea KV. Concluzia e in `bench/results/concluzie_etapa7_pc.txt`.
- Pe GPU, refolosirea KV NU da probabilitati bit-identice cu citirea fara refolosire (r 0.9991;
  pe CPU erau identice). De aceea statisticile lui B se calculeaza cu exact backend-ul si modul
  site-ului: GPU, aceeasi configuratie, cu refolosire, in aceeasi ordine a citirilor.
- Datele paperului sunt pe branch-ul `lcp_model` (repo-ul vechi `ia-sahistii`, alt istoric, nu se
  face niciodata merge in main). E scos ca worktree in `C:\Users\glosper\Documents\lcp-paper`, iar
  `docker/run_cuda.sh` ii monteaza `release/` read-only la `/paper/release`. Detaliile sunt in
  README, in sectiunea Stage 7.

Citeste intai, intregi: `docs/PLAN.md` (etapele 2 si 3 sunt cele de acum), `README.md`,
`bench/results/concluzie_etapa7_pc.txt`, `lcp_model/fuse.py`, `lcp_model/signal_a.py`,
`lcp_model/data.py`, `lcp_model/signal_b.py`, `lcp/rater.py`, `lcp/paper.py`, `scripts/spike_llama.py`,
`scripts/bench_cpu.py` (functia `analyze`) si `/paper/release/README.md` (in worktree:
`../lcp-paper/release/README.md`).

## Verificat deja pe 22 nov, nu mai trebuie redescoperit

- In container (`GPU=0 docker/run_cuda.sh ...`), `use_release("/paper/release")` merge:
  - `load_eval` da 5624 de randuri, iar cu romana 7211 (ro 1587, celelalte 445-600);
  - CompLex are 8423 de randuri, din `cache/`, fara descarcare;
  - `signal_a.csv` are 51340 de randuri (setarile mlsp si mlsp+ro, encoderele xlmr, labse, e5 si
    xlmr-large);
  - `signal_b.csv` are 32881 de randuri: gemma4-12b-4bit cu prompturile expert, short si marked, plus
    doua modele Qwen cu media expert+short;
  - in `cache/` sunt toate embedding-urile, `emb_{enc}_{complex_en_8423|eval_5624|eval_ro_7211}`
    pentru cele 4 encodere, plus `lemmas.csv`. Etapa 2 nu are nevoie de encodere si nici de stanza.
- `fuse.py --with-ro --boot 2000`, rulat din predictiile stocate, da exact media pe 11 limbi
  **0.692521** pe x86, cu CI [0.6789, 0.7057]. Gemma e ales la toate limbile, T e 4 sau 6, partitia e
  1|23|45, w e 0.35-0.40, w_src e 0.625-1.0.
- Fisierele de date au CRLF chiar in blob-urile din git (asa au fost puse pe GitHub). Pandas le
  citeste corect si nu ramane niciun `\r` in text.
- Montarea `/paper/release` e read-only. Pentru rulari `fuse` cu B nou, pui `data.PRED_DIR` pe un
  folder in care se poate scrie (in `/app`). `data.lemmas` scrie in `cache/lemmas.csv` doar daca ii
  lipsesc leme. Daca ajunge sa scrie, inseamna ca randurile nu sunt cele asteptate: te opresti si
  raportezi.
- Imaginea `lcp-web:cuda` exista si are scikit-learn 1.6.1 si wordfreq 3.1.1. Volumele `lcp-hf` (GGUF,
  tokenizer, encodere) si `lcp-stanza` sunt pline. Nu e nevoie de build si nici de descarcari.
- Din README-ul release: pe alt hardware decat Apple silicon, embedding-urile se misca cu ~1e-6 si
  pot schimba split-uri in HGB. Aici embedding-urile vin din cache, deci se schimba doar
  arhitectura pe care se fac fit-urile (x86 in loc de arm64).

## Pasii, in ordine

### Etapa 2: exportul modelului (`scripts/export_model.py` si `lcp/fusion.py`)

1. Pentru fiecare encoder din sistem (xlmr, labse, e5, setarea mlsp+ro), cu aceleasi date ca
   `signal_a.run`:
   - un model `p_en`, fitat doar pe CompLex;
   - 11 modele `p_multi_L`: CompLex plus celelalte 10 limbi; la en, fara CompLex.
   Hiperparametrii sunt exact cei din `blend_ridge_hgb`. Pentru ca functia intoarce predictii, nu
   modele, construiesti cei doi estimatori la fel in `lcp/`. Verifici ca media lor da bit cu bit
   acelasi rezultat ca `blend_ridge_hgb` pe aceleasi date. `lcp_model/` ramane neschimbat.
2. Constantele, salvate per limba si encoder:
   - `mu_L` si `fert_mu_L` (centrarea din `per_language`, pe randurile ok ale limbii) si centrarea
     CompLex din `features`;
   - constantele de z-score exact ca in `fuse.load_a` si `fuse.z_a`: pe encoder si brat, apoi pe media
     encoderelor, apoi pe amestecul cu `w_src`. Atentie la `data.zscore`, care pune 0 la valorile
     nefinite.
3. Artefactele merg in `artifacts/`: modelele cu joblib (scikit-learn 1.6.1, fixat) si `params.json`,
   cu reviziile modelelor si hash-ul fisierelor de date folosite. Fara text din MLSP, RoLCP sau
   CompLex: doar numere.
4. In `lcp/fusion.py`: functiile care, din artefacte, dau A (z), B (z), scorul fuzionat, scorul 0-1 si
   nivelul pentru niste randuri date. Etapa 4 le refoloseste.
5. **Poarta de paritate, fixata dinainte:**
   - pe fiecare encoder, predictiile modelelor exportate pe randurile de test fata de `p_en` si
     `p_multi` din `signal_a.csv`: raportezi max |dp| si r pe limba;
   - fuziunea calculata cu `lcp/fusion.py` (cu B-ul paperului si parametrii LOLO luati cu functiile
     din `fuse.py`) fata de `fuse.py --with-ro --out` pe fiecare rand: raportezi max |d|;
   - media pe 11 limbi trebuie sa iasa 0.692521. Daca nu e bit-identic, se accepta r >= 0.9999 pe
     fiecare limba si encoder si o medie fuzionata in +-0.0005 fata de 0.692521, cu cifrele raportate.
   Altfel te opresti si raportezi.

### Etapa 3: B de referinta cu llama.cpp pe GPU (`scripts/b_reference.py`)

6. **Poarta de lungime, inainte de orice citire:** tokenizezi toate cele 21.633 de prompturi (7211
   randuri x 3 prompturi, `render` plus `apply_chat_template`, ca in `lcp/rater.py`), fara model.
   Raportezi maximul si p99 pe limba. Daca vreun prompt nu incape in n_ctx 1024 (lasa si o margine
   mica), te opresti si raportezi cate sunt si in ce limbi. Cifra asta decide si limita din Etapa 4.
7. Rularea, cu configuratia site-ului si cu refolosire:
   - aceeasi ordine ca `analyze` din `bench_cpu.py`: propozitie, cuvant, prompt; pe datele de test,
     randurile grupate dupa context, in ordinea idx;
   - se poate relua dupa o intrerupere: un fisier `.part` in `reference/`;
   - iesirea e `reference/signal_b_llamacpp.csv`, in formatul `signal_b.csv` (model, prompt, lang, idx,
     p1..p5, score), cu cheia de model `gemma4-12b-qat-gguf`, fara text. Plus un log cu s/citire,
     tokeni/s si VRAM.
   Estimare: 0.08-0.11 s/citire, deci ~30-40 de minute. Promptii MLSP pot fi mai lungi decat cei din
   Wikipedia, asa ca da statusuri dese.
   Inainte de pornire, Alexandru inchide aplicatiile care folosesc GPU-ul (jocuri, browser cu
   accelerare). Verifici sa nu apara spill: contorul Windows "\GPU Process Memory(*)\Shared Usage"
   trebuie sa ramana la ~100 MiB. Daca urca la sute de MiB, te opresti si raportezi.
8. **Portile, aceleasi ca in spike:**
   - masa pe cifre >= 0.5, fara NaN;
   - r intre media celor 3 prompturi (scor la T = 1) si B-ul MLX stocat (gemma4-12b-4bit): >= 0.90 pe
     fiecare limba si >= 0.95 pe toate randurile, cu cifrele per prompt raportate.
9. Fuziunea cu B-ul nou: un folder de predictii in care se poate scrie, cu `signal_a.csv` copiat si
   un `signal_b.csv` care contine doar `gemma4-12b-qat-gguf`. Pe el rulezi `fuse.py --with-ro --out`,
   cu aceeasi procedura LOLO, deci T, partitia, w_src si w sunt alese din nou.
   - Raportezi r pe limba, media pe 11 limbi si CI-ul, langa 0.692521, plus parametrii fata de cei ai
     paperului.
   - Daca media scade cu mai mult de 0.01 (sub 0.6825), te opresti si discuti cu Alexandru inainte sa
     scrii artefactele finale.
10. Artefactele finale (`params.json` actualizat), din rularea de la pasul 9:
   - parametrii LOLO per limba si media si deviatia lui B per limba, cu T si partitia ei;
   - scala de afisare din PLAN, Etapa 3: distributia fuziunii pe limba (cuantile, de exemplu 1001 de
     puncte) si cuantilele etichetelor din toate cele 11 limbi la un loc. Scorul 0-1 e cuantila
     etichetelor la percentila cuvantului in limba lui, iar nivelul e nota cea mai apropiata de
     1 + 4 x scor;
   - r-ul fuzionat pe limba, pentru `GET /api/languages`.
   Verificare: `lcp/fusion.py` aplicat pe randurile de test cu artefactele finale reproduce fuziunea
   de la pasul 9.
11. Concluzia: `bench/results/concluzie_etapa2_3.txt`, in romana fara diacritice si fara tabele
   markdown:
   - paritatea exportului;
   - lungimea prompturilor fata de n_ctx;
   - timpii lui B pe GPU;
   - portile lui B;
   - r-ul pe limba si media cu llama.cpp, fata de paper;
   - parametrii schimbati;
   - ce inseamna pentru site, inclusiv cifrele care vor fi afisate pe site.

## Reguli

- Cere aprobare inainte de `docker build` si de orice descarcare mare (n-ar trebui sa fie nevoie de
  niciuna).
- Nu da commit si nu face push. Pregatesti fisierele si staging-ul, iar commit-ul il da Alexandru.
  Comenzile de git i le dai in engleza, cu mesaje scurte, FARA linii `Co-Authored-By` sau alta
  atribuire.
- Nu intra in git text din MLSP, RoLCP sau CompLex (repo-ul e privat, dar regula ramane). In loguri,
  nu printezi propozitii din date.
- Fara subagenti; verifici singur.
- In chat: romana fara diacritice, fara tabele markdown, explicatii scurte. La rularile lungi dai
  statusuri dese: progres, s/citire, VRAM.
- Daca o poarta pica sau ceva nu incape in memorie, te opresti si raportezi cifra, fara sa ocolesti.
- Rulezi din Git Bash: `MSYS_NO_PATHCONV=1` e deja pus in `docker/run_cuda.sh`. Scripturile de proba
  le scrii in fisiere si le stergi dupa.
