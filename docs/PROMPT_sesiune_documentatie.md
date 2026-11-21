Vreau sa scriem impreuna documentatia proiectului, pas cu pas, ca un fisier .tex intreg pe care il
lipesc direct in Overleaf. Template-ul e cel ACL, folosit si de NAACL 2027 (acl.sty). Tu scrii textul,
eu il reformulez dupa. Nu treci la pasul urmator pana nu aprob pasul curent.

## Ce citesti intai

Memoria proiectului, in special:
- `sistemul-e-0692527-en-curat` si `release-anonim-pentru-paper`: cifrele de citat; codul din release/
  e sursa de adevar.
- `semnale-a-b-ce-se-antreneaza`: ce e inghetat si ce se antreneaza in fiecare semnal.
- `diagrama-pipeline-drawio` si `diagrame-doc-doar-titluri`: diagrama de documentatie, deja aprobata.
- `shap-semnal-a-adoptat` si `proiectii-centrare-rezultat`: cele doua figuri de analiza.
- `paper-naacl-2027-lucru-7-oct`: cifrele gresite deja semnalate in draftul de paper.
- `bifurcatii-de-declarat`, `selectia-modelului-b-e-pe-splitul-gresit`, `optimismul-de-selectie-masurat`:
  ce trebuie declarat onest.
- `preferinte-de-scriitura-paper`, `scrie-uman-nu-overexplain`, `lista-utilizatorului-nu-se-reformuleaza`,
  `paper-overleaf-workflow`: stilul si capcanele Overleaf.

Apoi fisierele:
- `docs/instructions_documentation.md`: sablonul de documentatie al cursului. Sectiunile obligatorii
  (Abstract, Introduction, Approach, Conclusions and Future Work, References) si punctele cerute in
  fiecare trebuie acoperite.
- `~/Downloads/Authors__Instructions__Preparation_of_Camera_Ready_Contributions_to_SCITEPRESS_Proceedings-1.pdf`:
  paperul meu anterior (glioma, conferinta de rang B). E modelul de structura si de ton: Keywords
  inaintea abstractului; intro cu problema, abordarile anterioare, ce propunem in pasi, contributiile si
  organizarea; Related Work cu titluri in bold; Method cu figura de pipeline, pasi numerotati si o
  subsectiune Evaluation Protocol; Experimental Results cu tabele si SHAP; Conclusions, Limitations,
  Future Work; o sectiune Implementation cu link-ul de repo.
- `release/` (README.md, data.py, signal_a.py, signal_b.py, fuse.py): codul din repo-ul anonim. Tot ce
  descrie documentatia trebuie sa corespunda cu el.
- `Paper/Articol_Multilingv/paper_full.tex` (19 sep) si `fragmente_noi.tex`: draftul de paper. Poti
  refolosi bibliografia, keywords si argumentul, dar cifrele lui sunt vechi (0.674946), deci nicio cifra
  nu se copiaza de acolo.
- `Paper/documentation_overleaf.tex`: documentatia veche, doar pe romana. O folosesti doar pentru
  bibliografie si istoricul experimentelor.

Link-ul repo-ului anonim: https://anonymous.4open.science/r/zero-label-lcp

## Reguli

- Fisierul nou e `Paper/Articol_Multilingv/documentatie_overleaf.tex`. Nu atingi paper_full.tex,
  Paper/documentation_overleaf.tex sau release/.
- Textul documentatiei e in engleza. Ce imi scrii in chat e in romana, fara diacritice si fara tabele
  markdown.
- Fiecare cifra din text iese dintr-o comanda rulata in sesiune (`release/fuse.py` cu python-ul din
  envs/ml_def) sau dintr-un fisier din output/ numit explicit. Langa fiecare cifra pui un comentariu
  LaTeX scurt cu sursa. Cifrele de baza: 0.689745 pe 10 limbi si 0.692521 pe 11. 0.692527 e media
  valorilor rotunjite si nu se citeaza; 0.674946, 0.683849, 0.690001 si 0.693718 sunt istorice.
- Stilul: regulile din `preferinte-de-scriitura-paper` (fara em-dash, fara "the system" pentru lucrarea
  noastra, fara deschidere de dictionar, fara formule in intro, nicio idee spusa de doua ori, nimic
  adaugat necerut). Propozitii scurte si concrete, ca in paperul de glioma.
- Cand paperul de glioma si regulile din memorie se contrazic (de exemplu contributiile cu buline din
  glioma fata de paragraful narativ din preferinte), ma intrebi.
- Cand iti dau inapoi un paragraf reformulat de mine, il pui cuvant cu cuvant. Daca vezi o problema in
  el, o semnalezi separat.
- Diagrama e `docs/pipeline.drawio`, aprobata; nu o redesenezi. Pentru Overleaf o exporti in PDF cu
  `drawio -x -f pdf --crop`.
- La fiecare pas compilezi intr-un director gol din scratchpad (pdflatex, bibtex, pdflatex de doua ori)
  cu acl.sty si acl_natbib.bst din Paper/Articol_Multilingv: 0 erori, 0 Undefined, 0 `??` in PDF,
  0 Overfull. Imi spui cate pagini are.
- Bibliografia sta in blocul `filecontents*[overwrite]{custom.bib}` din .tex, fara Unicode, cu acronimele
  protejate cu acolade. Orice intrare noua o verifici (titlu, autori, an, venue) inainte s-o pui.
- Commit-ul il dau eu. Nu faci git add si nici commit.

## Pasii

## Decizii deja luate (8 oct), nu le mai intrebi

- Documentatia e pentru curs, cu nume de autori: optiunea `final` din acl.sty, fara `review`. Link-ul de
  repo ramane cel anonim.
- Autorii, emailurile si paragraful "who did what" se completeaza ULTIMELE, dupa ce restul documentatiei
  e scris si aprobat (pasul 9). Pana atunci pui in .tex placeholder-e vizibile (de exemplu
  `\author{AUTHOR 1 \\ \texttt{EMAIL} \And AUTHOR 2 \\ \texttt{EMAIL}}` si un paragraf `[WHO DID WHAT]`).
- Cifra principala e pe 11 limbi, cu romana: 0.692521. Cifra pe 10 limbi MLSP (0.689745) apare ca
  ablatie in tabel.
- Titlul: "Lexical Complexity Prediction Without Target-Language Labels", fara subtitlu.
- Cercurile numerotate 1-8 din diagrama raman, iar textul din Method se refera la pasi dupa numar
  (step 1 ... step 8), ca in paperul de glioma.

## Decizii luate pe 9 oct, au prioritate fata de cele de mai sus

- Fisierul sta pe TOT sablonul oficial `acl_latex.tex` (master acl-org/acl-style-files, folosit si de
  NAACL): comentariile din preambul, blocurile de autori, `\section*{Limitations}`,
  `\section*{Acknowledgments}`, liniile de bibliografie si `\appendix`. Textul nostru se pune peste
  sablon. Nu se scoate nimic din cadrul sablonului.
- Overleaf: proiect din sablonul ACL, .tex-ul lipit peste `acl_latex.tex`, plus `figures/`.
  `acl.sty` si `acl_natbib.bst` vin cu sablonul.
- Placeholder-ul de autori e cel al sablonului (First Author, Affiliation, email@domain), nu AUTHOR 1.
- "Who did what" nu apare deloc (decis pe 8 oct), deci nu exista `[WHO DID WHAT]`.
- Limitations e `\section*{Limitations}` din sablon, nu paragraf in Conclusions.
- Acknowledgments e scris: doua buline ca in glioma, Conflicts of Interest si Data Sharing (MLSP 2024,
  CompLex 2.0, RoLCP).
- Deschis: ce intra in anexa (prompturile lui B au fost oferite).

## Decizii luate pe 10 oct, au prioritate fata de cele de mai sus

- Modelul principal dupa care ne ghidam e RALS: Anghel, Cristea, Creanga si Nisioi, EMNLP 2025 main,
  pp. 31481-31492 (`~/Downloads/2025.emnlp-main.1603.pdf`, citat deja ca `anghel-etal-2025-rals`).
  Structura, tonul, sectiunea de date si Related Work se iau de acolo.
- Model secundar: Ispas si Nisioi, Archaeology la SemEval-2026 Task 13
  (`~/Downloads/2026.semeval-1.383.pdf`), doar pentru ce RALS nu are: Results and Analysis cu Error
  Analysis si anexa de hiperparametri. Ghidul hgs ramane pentru introducere. Glioma ramane doar pentru
  ce nu acopera RALS (keywords, Implementation, declaratiile din Acknowledgments).
- Figurile din corp sunt trei: diagrama de pipeline (verticala), SHAP (`fig_shap_signal_a.pdf`) si
  t-SNE-ul principal (`fig_tsne_encoders.png`). Orice alta figura merge in anexa.
- Consecintele propuse, care se aplica abia dupa "go": Data devine sectiune proprie, inainte de Method,
  cu tabel de statistici per limba ca Tabelul 1 din RALS; Related Work devine "Challenges and Related
  Work", in proza, fara subtitluri, fiecare paragraf inchis cu pozitia noastra; anexa A hiperparametri,
  anexa B prompturile lui B cuvant cu cuvant.
- Deschise: Ethics Statement (RALS are, cursul nu cere); grantul InstRead/HRIA la Acknowledgments.

## Pasii

Pas 0. Citesti tot ce e mai sus si rulezi fuse.py pe 10 si pe 11 limbi, cu `--out` pentru cifrele per
limba. Imi dai in chat cifrele de baza cu sursa lor. Nu scrii .tex inca.

Pas 1. Scheletul: verifici ca acl.sty local e versiunea curenta din github.com/acl-org/acl-style-files,
apoi scrii preambulul, titlul, autorii ca placeholder, keywords, toate sectiunile cu cate un comentariu
de plan (ce intra, ce figura, ce tabel) si bibliografia de pornire. Compilat. Imi arati planul pe
sectiuni, nu text.

Pas 2. Method: datele (MLSP 2024 pe 10 limbi, RoLCP pe romana, CompLex 2.0 pe engleza), semnalul A,
semnalul B, fuziunea, protocolul LOLO si bootstrap-ul. Figura de pipeline la inceputul sectiunii,
referita pe pasi dupa numarul din cerc. Spui clar ce e inghetat si ce se antreneaza.

Pas 3. Experimental Results: tabelul per limba (A, B, fuziune) pe 11 limbi, ablatiile pe care le scoate
fuse.py (10 limbi, un encoder, patru encodere, un singur LLM), comparatia cu cifrele publicate (vezi
`agregare-medie-pe-limbi-nu-pooled` si `noutate-si-precedente-lcp-multilingv`),
SHAP si t-SNE.

Pas 4. Ce am incercat si n-a mers. Sablonul cursului cere lista de experimente. Le iei din memorie
(axele inchise: fine-tuning, eye-tracking, surprisal, TabFM, alti regresori, calibrare, few-shot,
prefix, ansambluri de modele etc.), fiecare cu o propozitie si cifra lui. Imi dai intai lista in chat,
ca s-o tai.

Pas 5. Introduction si Related Work, dupa modelul glioma.

Pas 6. Conclusions and Future Work, Limitations (selectia pe test a celui de-al treilea prompt,
bifurcatiile, Known limitations din README) si sectiunea Implementation (link, unelte, timpi de rulare
din README, masinile pe care s-a rulat).

Pas 7. Abstractul si keywords, la final, cand restul e fixat.

Pas 8. Verificarea finala: compilare, numar de pagini, fiecare cifra reverificata fata de sursa,
cautare de em-dash si de "the system", plus lista exacta de fisiere de urcat in Overleaf (figuri,
acl.sty, acl_natbib.bst). Imi listezi si placeholder-ele ramase (autori, `[WHO DID WHAT]`).

Pas 9. Abia acum ma intrebi de autori, emailuri si cine ce a facut, si completezi placeholder-ele.
Compilezi din nou.

La sfarsitul sesiunii, sau daca ramanem fara context, scrii in memorie un punct de reluare: ce pas e
gata, ce e aprobat si ce asteapta.
