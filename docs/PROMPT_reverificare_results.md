Verifici a doua oara sectiunea 4, Experimental Results, din `Paper/Articol_Multilingv/documentatie_overleaf.tex`
(documentatia de curs, sablon ACL). O sesiune anterioara a auditat-o si a rescris-o pe 10 oct. Tu verifici
daca ce a scris e corect si daca textul nu a iesit intr-o forma ciudata. Textul trebuie sa fie in acord cu
paperul-model, RALS, si cu stilul sectiunii 3, Method, pe care am aprobat-o.

Nu rulezi experimente noi: nu rulezi modele de limbaj si nu reantrenezi nimic. Ai voie sa citesti fisierele
de rezultate, sa rulezi `release/fuse.py` si `analysis_doc_ablations_extra.py` si sa recalculezi din
CSV-urile existente.

Lucrezi in trei faze. Faza 1 e auditul, numai in chat. Nu modifici fisierul pana nu iti dau "go".

## Starea

- .tex-ul are sha1 2283b75a, compileaza curat (0 erori, 0 Undefined, 0 Overfull, 0 `??`) si are 10 pagini.
  Paginile 9-10 sunt bibliografia si anexa, umflate de `\nocite{*}`. Daca sha-ul difera, imi spui intai ce
  s-a schimbat. Daca am editat eu, textul meu ramane cuvant cu cuvant.
- **Sectiunea 3, Method, e APROBATA.** N-o modifici. E modelul de stil.
- Sectiunea 4 incepe la `\section{Experimental Results}` si se termina inainte de `\section{What Did Not
  Work}`. Are 5 subsectiuni: 4.1 Per-Language Results (Tabel 1), 4.2 Ablations and Baselines (Tabel 2),
  4.3 Comparison with Published Results (Tabel 3), 4.4 Feature Attribution (figura SHAP si tab:shap),
  4.5 Representation Geometry (figura t-SNE).
- Versiunea de dinainte de rescriere (sha 110df127) e in
  `/private/tmp/claude-501/-Users-alexandrucojoaca-Documents-GitHub-ia-sahistii/bd5805f4-946c-41af-a068-b63ab34c961a/scratchpad/bak/`.
  Daca nu mai exista, foloseste `git diff` pe .tex (ultimul commit e mai vechi; diferentele din afara
  sectiunii 4 nu te privesc).
- Paperul-model e RALS: Anghel et al., EMNLP 2025, `~/Downloads/2025.emnlp-main.1603.pdf`.

## Ce s-a schimbat la rescriere (de verificat, nu de crezut)

- 4.1: trei zecimale; pe filipineza "26.7% din tinte au frecventa 0, fata de cel mult 7.4% in celelalte
  noua limbi" (in loc de "fara leme"); deductiile "X, so Y" sparte in propozitii separate.
- 4.2: Tabelul 2 are 8 randuri noi (English regressor only, Multilingual regressor only, Temperature fixed
  at 1, No grouping, Expert/Short/Marked prompt only, "Gemma 4, Qwen reading"), intervale bootstrap
  pereche si doua paragrafe noi (regresorii; partile lui B). La Qwen s-au adaugat Gemma citit ca Qwen si
  fraza despre romana.
- 4.3: garda Opus (Opus 0.711 e peste orice medie din Tabelul 3) si fraza despre predictiile publicate.
- 4.4: explicatia SHAP pentru incepator; lamurirea dintre 0.31 si 0.12-0.13.
- 4.5: "target embeddings"; explicatia t-SNE si a numaratorii de vecini; figura refacuta fara titlu.

## Ce citesti intai

1. Memoria: `cerere-sesiune-documentatie`, `ablatii-documentatie-10-oct`, `baseline-claude-opus-bate-sistemul`,
   `model-rals-emnlp-2025`, `preferinte-de-scriitura-paper`, `scrie-uman-nu-overexplain`,
   `raspunsuri-fara-diacritice-fara-tabele-md`, `noutate-si-precedente-lcp-multilingv`,
   `shap-semnal-a-adoptat`, `proiectii-centrare-rezultat`.
2. `docs/PROMPT_verificare_results.md`: promptul primei verificari, cu regulile de stil si sursele.
3. .tex-ul intreg: Method cu atentie, apoi sectiunea 4, inclusiv caption-urile si comentariile LaTeX.
4. RALS, in intregime: sectiunea 4 Results, tabelele si caption-urile lor.
5. PDF-ul compilat (il compilezi tu, vezi mai jos), ca sa vezi cum arata textul si tabelele in pagina.

## Faza 1: auditul (doar in chat)

### A. E corect?

Nu te increde in comentariile LaTeX si nici in memoria sesiunii anterioare. Recalculezi.

- Fiecare cifra din sectiunea 4, inclusiv caption-urile: sursa din comentariu chiar contine cifra, iar
  rotunjirea e corecta.
- Sursele: `output/doc_fuse_ro11.{txt,csv}`, `output/doc_fuse_mlsp10.{txt,csv}`, `output/doc_ablations.txt`,
  `output/doc_ablations_qwen_ro.txt`, `output/doc_ablations_extra.txt`, `output/doc_claude_baseline.txt`,
  `output/shap_signal_a_per_encoder_{importance,correlations}.csv`, `output/doc_counts.txt`,
  `output/repere_publicate.md`.
- **Scriptul nou `analysis_doc_ablations_extra.py` il verifici independent, nu doar iesirea lui:**
  - schimba setarile lui fuse.py pe modul la rulare (T_GRID, PARTITIONS, NEUTRAL, SRC_GRID) si filtreaza
    prompturile prin `pd.read_csv`. Ajung modificarile chiar acolo unde le citeste fuse.py? Se refac
    setarile implicite intre rulari?
  - intervalele sunt numite "pereche": `data.boot_r` are samanta fixa, deci esantionul k ar trebui sa fie
    acelasi set de contexte in fiecare rulare. E adevarat? Ce se intampla daca `boot_r` arunca un esantion
    degenerat intr-o rulare si nu in alta?
  - controalele: metoda completa trebuie sa dea 0.692521 / 0.689745, iar encoderele si Qwen trebuie sa
    reproduca `doc_ablations.txt` si `doc_ablations_qwen_ro.txt`.
- Afirmatiile noi, de verificat una cate una (lista nu e completa):
  - "Every one of these intervals excludes zero" (un singur encoder, pe ambele coloane);
  - "Its interval excludes zero only on eleven languages" (XLM-R large);
  - "using the English regressor alone changes the fusion by less than 0.001 on both columns";
  - "mixing the two raises signal A by 0.004 on eleven languages and 0.005 on ten, but not the fusion";
  - "With T = 1, the choice of the grouping in step 6 also keeps the five ratings apart";
  - "A single prompt loses 0.006 to 0.017 ... and 0.009 to 0.019 on ten";
  - "26.7% ... against at most 7.4% in the remaining nine languages";
  - "Gemma 4 is chosen because it is better on the other languages" (verifici in `release/fuse.py`);
  - "The shared task releases the predictions of its participants and of the baseline" (Shardlow et al.
    2024, Sec. 8; PDF-ul il descarci de pe ACL Anthology intr-un director nou din scratchpad);
  - "Claude Opus 5.5 ... also reads no label, and its mean on the ten languages, 0.711, is higher than
    every mean in the table";
  - in 4.4, explicatia SHAP (referinta = media limbii, suma = predictia minus referinta) si "These three
    values add up to more than 0.31, because the contributions of the three encoders partly cancel"
    (verifici in `analysis_shap_signal_a.py` si `analysis_shap_signal_a_per_encoder.py`);
  - in 4.5, descrierea t-SNE si a numaratorii de vecini, fata de `output/umap_concat3.py` si
    `output/tsne_concat_fara_knn.py`.
- Termenii din text trebuie sa fie aceiasi ca in tabele, figuri si Method (nume de randuri, de trasaturi,
  de pasi, de prompturi).

### B. Forma e ciudata?

Rescrierea a spart mecanic deductiile in propozitii separate. Verifici daca asta a produs un text sacadat
sau robotic. Cauti:
- propozitii foarte scurte puse una dupa alta, care citite cu voce tare suna ca o lista;
- aceeasi formula repetata ("on eleven languages and ... on ten", "Both intervals include zero.",
  "always gets the larger weight");
- paragrafe care incep la fel ("Within signal~A", "Within signal~B");
- fraze lungi cu multe cifre, greu de urmarit;
- explicatii pentru incepator care sunt prea lungi sau care se repeta cu Method;
- orice fraza care nu aduce nimic nou sau repeta o idee deja spusa (in Results sau in Method).

Pentru fiecare problema dai o varianta concreta, cu aceleasi fapte si aceleasi cifre.

### C. E in acord cu Method si cu RALS?

Regulile mele (din review-urile pe Method, 10 oct):
- propozitii simple si concrete; spui direct ce am facut, apoi pe scurt de ce;
- fara trimiteri vagi de tipul "as described below";
- fara deductii inlantuite de tipul "X, and Y, so Z", dar si fara text tocat marunt;
- expresii respinse: "To this end", "held out (in turn)", "unweighted", "Two adjustments follow",
  "neighbouring", "on their own", "complementary", "gold", "the system";
- fara em-dash si fara adaugiri pe care nu le-am cerut;
- un termen nou pentru un incepator se explica scurt la prima mentiune.

De la RALS compari structura si tonul sectiunii Results: cum introduce un tabel, cum justifica un
baseline, cat de lungi sunt paragrafele, ce pune in caption si ce in text, cum da cifrele in proza. Spui
concret unde sectiunea 4 se abate si daca abaterea e justificata (documentatia de curs cere "an
evaluation report" si tabele care "may convince a reader", deci poate fi mai lunga decat RALS).

### Ce NU semnalezi din nou (decis sau cunoscut)

- release/ nu reproduce randurile Qwen pe 11 limbi si nici ablatiile noi (fuse.py nu are flag-uri); se
  decide la pasul 8.
- Combinatiile cu Claude sunt calculate pe versiunea veche a predictiilor; au ramas, cu comentariu.
- Predictiile si promptul Claude nu sunt in repo.
- "signal~A/B" cu litera mica; "step~8" cu litera mica in text (la fel ca in Method).
- Cele 4 avertismente Underfull vbox din log.
- **Textul meu, cuvant cu cuvant, nu se reformuleaza:** paragraful Claude din 4.2 ("We also built a
  baseline with current foundation models..." pana la "...almost no gain, 0.001.") si fraza Qwen
  ("With Qwen3 8B as the only candidate, signal~B alone falls from 0.663 to 0.381 and the fusion from
  0.693 to 0.622 on eleven languages. With Qwen3.5 9B they fall to 0.599 and 0.661."). In ele semnalezi
  doar erori de fapt.

### Formatul auditului

O lista in chat, grupata asa:
(1) Fals,
(2) Prea tare sau neclar,
(3) Forma ciudata,
(4) Abateri de la Method (stil si termeni),
(5) Abateri de la RALS.
Pentru fiecare punct dai linia din .tex, textul actual citat scurt, sursa verificarii si propunerea
concreta (fraza noua). Daca o subsectiune e in regula, spui asta intr-un rand. La final, un rezumat de
3-4 randuri: ce e grav si ce e cosmetic.

## Faza 2: planul

Dupa ce raspund la audit, propui planul pe paragrafe: ce ramane, ce se scoate, ce se reformuleaza. Astepti
"go".

## Faza 3: rescrierea, dupa "go"

- Inainte de orice modificare faci un backup al .tex-ului in scratchpad.
- Modifici doar sectiunea 4, plus caption-urile tabelelor si figurilor ei. Method nu se atinge. Daca o
  corectura cere o schimbare in alta parte, intrebi intai.
- Frazele mele raman cuvant cu cuvant.
- Langa fiecare cifra si fiecare detaliu de metoda ramane sau se pune un comentariu LaTeX scurt, in
  engleza, cu sursa.
- Compilezi intr-un director gol din scratchpad: pdflatex, bibtex, apoi pdflatex de doua ori, cu acl.sty si
  acl_natbib.bst din `Paper/Articol_Multilingv` plus `figures/`. Rezultatul trebuie sa aiba 0 erori,
  0 Undefined, 0 `??` si 0 Overfull. Imi spui sha-ul nou, numarul de pagini si ce s-a schimbat, pe
  subsectiuni.

## Reguli

- Nu atingi `paper_full.tex`, `Paper/documentation_overleaf.tex` sau `release/`. Nu faci git add si nici
  commit.
- In chat scrii in romana, fara diacritice si fara tabele markdown.
- La final, sau cand ramane putin context, actualizezi memoria `cerere-sesiune-documentatie` cu punctul de
  reluare si sectiunea "Unde am ramas" din `docs/PROMPT_sesiune_documentatie_continuare.md`.
