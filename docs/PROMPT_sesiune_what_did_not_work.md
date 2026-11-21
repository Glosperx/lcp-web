Continuam documentatia de curs din `Paper/Articol_Multilingv/documentatie_overleaf.tex` (titlu: "Lexical Complexity
Prediction Without Target-Language Labels", sablon ACL). Experimentele sunt gata. Nu rulam experimente noi.

Ordinea pe care o vreau, cate un pas, cu aprobarea mea inainte de pasul urmator:
1. What Did Not Work (sectiunea 5, acum goala), incepand cu eye-tracking-ul.
2. Conclusions and Future Work.
3. Abstract si keywords.
Scurtarea paperului la 8 pagini fara anexe e o sesiune SEPARATA, dupa asta. Dar limita exista deja: corpul se
termina acum pe pagina 11 (~10,5 pagini), deci tot ce scrii aici trebuie sa fie scurt.

## Starea

- .tex sha **1083d9ee** (verifici cu `shasum`), urcat de mine in Overleaf pe 11 oct noaptea. Daca sha-ul difera,
  intrebi inainte sa faci orice.
- Acceptate de mine: Method, Experimental Results, Related Work, Introduction. Nu le atingi fara cerere.
- Introduction e scrisa de Gemma 4 (vezi comentariul de deasupra ei). Nu o modifici.
- Detaliile si ordinea ramasa: primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md`. Regulile si pasii
  0-9: `docs/PROMPT_sesiune_documentatie.md` (pasii 4, 6, 7 sunt cei de acum).

## Ce citesti intai

1. Memoriile: `cerere-sesiune-documentatie`, `preferinte-de-scriitura-paper`, `scrie-uman-nu-overexplain`,
   `lista-utilizatorului-nu-se-reformuleaza`, `fara-agenti-multipli-tokeni`, `model-rals-emnlp-2025`,
   `baseline-claude-opus-bate-sistemul`, `tabele-un-subiect-pe-tabel`.
2. Pentru eye-tracking: `eye-tracking-cat-a-adus-in-r` (intreaga) si `output/e_et_distill.md`.
3. Pentru restul listei, memoriile axelor inchise: `fine-tuning-exista-cifre`, `semnalul-c-surprisal-stare`,
   `poarta-al-treilea-semnal-0107`, `gemma-nu-poate-da-surprisal`, `fewshot-pe-test-masurat`,
   `pozitia-de-citire-masurata`, `prompturi-decorelate-cernute`, `update-paper-mesaj2-punctul7`,
   `prioritizarea-parghiilor-masurata`, `calibrarea-monotona-inchisa`, `ponderea-per-item-inchisa`,
   `dropout-frecventa-inchis`, `diversitatea-contextuala-inchisa`, `coada-frecventa-masurata`,
   `sesiunea-obiectivului-rezultatul`, `axa-liniara-inchisa`, `ansamblul-de-modele-nu-se-transfera`,
   `wsrc-e-decorelare-nu-transfer`, `pooling-first-inverseaza-literatura`.
4. Din .tex: Experimental Results intreg (ca sa nu repeti ce e deja acolo), comentariile din What Did Not Work,
   Conclusions, Limitations si din abstract.
5. Paperul model RALS: `~/Downloads/2025.emnlp-main.1603.pdf` (abstractul si Conclusions; `pdftotext -layout`).

## Pasul 1: What Did Not Work

Cursul cere "a bullet point list of experiments tried". Forma: lista cu buline, fiecare experiment intr-o
propozitie sau doua, cu cifra lui. RALS nu are sectiunea asta; o cere cursul.

**Eye-tracking-ul e primul si cel mai dezvoltat punct** (asa vreau eu). Faptele sunt in memoria
`eye-tracking-cat-a-adus-in-r`. Pe scurt:
- Ca semnal, pe romana, cu privirea reala din MultiplEYE (95 de participanti), a adus +0.0067 in r. E un plafon,
  nu o estimare: ponderea a fost aleasa pe scorul public.
- Ca tinta de transfer (`analysis_et_distill.py` -> `output/e_et_distill.md`): embeddingul singur prezice timpul
  de citire mai prost decat doua coloane lexicale (lungime si frecventa).
- Datele de privire exista doar pentru romana, deci nu pot fi un semnal sub LOLO pe celelalte limbi. Verifici
  formularea exacta inainte sa o scrii.
- Daca citezi MultiplEYE sau Kuvshynova et al., intrarile nu sunt in bib-ul din .tex. Le verifici pe ACL
  Anthology sau arXiv inainte sa le adaugi.

Restul listei: doar experimentele care NU sunt deja in Results. Acolo sunt deja: straturile encoderului, TabFM,
regresorii alternativi, XLM-R large, Qwen3/Qwen3.5/Llama/Aya, prompturile luate cate unul, temperatura,
gruparea, regresorul englez sau multilingv singur, baseline-ul Claude. Candidati din memorii: fine-tuning-ul
encoderului, surprisal-ul (semnalul C), few-shot, prefixul de citire, promptul de frecventa decorelat, scara de
raspuns, calibrarea monotona, ponderea per item, dropout-ul pe frecventa, diversitatea contextuala, incadrarea
ordinala a obiectivului, ansamblul de modele de limba.

Atentie la cifre:
- Multe axe au fost masurate pe configuratii vechi. Fiecare cifra o iei din fisierul din `output/` (nu doar din
  memorie), spui pe ce configuratie a fost masurata si o pui ca diferenta ("lowered the fusion by 0.012"), nu ca
  scor absolut.
- Nu citezi 0.674946, 0.683849, 0.690001, 0.692527, 0.693718, 0.687831.
- Fine-tuning-ul e pe EN -> MLSP, nu sub LOLO (memoria `fine-tuning-exista-cifre`). Spui asta.
- Sursa fiecarei cifre intra in comentariu LaTeX langa ea, in engleza, ca in restul fisierului.

**Intai imi dai lista in chat** (o linie pe experiment: ce, cifra, sursa, configuratia), ca s-o tai. Scrii in .tex
abia dupa OK. Tinta: cel mult ~250 de cuvinte pentru toata sectiunea.

## Pasul 2: Conclusions and Future Work

Comentariul din .tex: Conclusions = ce am facut si cifrele principale, fara idei noi; Future Work = buline. RALS
are Conclusions intr-un singur paragraf. Intrebi la inceput daca Future Work ramane (si cate buline), fiindca suntem
peste 8 pagini. Fara afirmatia ca suntem cei mai buni in general: Claude Opus 5.5 zero-shot e peste noi.

Intrebi tot la pasul asta daca scriem acum si Limitations (`\section*`, in ACL nu intra in cele 8 pagini). Ce
trebuie sa contina e in comentariul din .tex si in memoria `cerere-sesiune-documentatie`: al treilea prompt ales in
dezvoltare cu scorurile de test la vedere, lista scurta de LLM-uri comparata pe trial-ul celor zece limbi,
dependenta de ordinul doi din LOLO, efectul centrarii pe r nemasurat, testul curatat (5.624) fata de cel publicat
(5.627). README-ul din release/ NU are "Known limitations", desi pasul 6 o cere ca sursa.

## Pasul 3: Abstract si keywords

Modelul e RALS ("We introduce..."). Comentariul din .tex cere: problema, ce propunem, ce e inghetat si ce se
antreneaza, cifra principala pe 11 limbi cu intervalul, o fraza despre comparatia cu cifrele publicate.
Cifre: 0.693 pe 11 limbi, interval 0.679-0.706 (`output/doc_fuse_ro11.txt`, 0.692521 [0.6789, 0.7057]); pe cele
zece limbi MLSP 0.690 (`output/doc_fuse_mlsp10.txt`, 0.689745 [0.6751, 0.7035]). Comparatia permisa: cea mai mare
medie publicata, G-Scale 0.669, citeste 30 de etichete din fiecare limba evaluata; noi zero. Daca o pui, spui si
cate etichete. "Zero-label" se spune precis: nicio eticheta a limbii de test nu intra in antrenare sau in alegerea
setarilor. Keywords-urile le revizuiesti la final.

## Stil (din review-urile mele)

- Fara em-dash, fara deschidere de tip definitie, fara aforisme, fara "the system" pentru lucrarea noastra, fara
  formule, nicio idee spusa de doua ori, nimic adaugat necerut, fara cadru de competitie sau de tema de facultate.
- Propozitii scurte si concrete, o idee pe propozitie, fara deductii inlantuite ("X, and Y, so Z").
- Reformularile mele le pui cuvant cu cuvant. Daca vezi o problema, o semnalezi separat.
- In chat: romana, fara diacritice, fara tabele markdown, propozitii scurte.

## Compilare si reguli

- Inainte de fiecare scriere: backup al .tex-ului in scratchpad. Compilezi intr-un director gol din scratchpad
  (.tex + acl.sty + acl_natbib.bst + figures/, pdflatex, bibtex, pdflatex de doua ori). Conditii: 0 erori,
  0 Undefined, 0 `??`, 0 Overfull. Spui cate pagini are documentul si pe ce pagina se termina corpul.
- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Fara subagenti; verifici singur, cu grep.
- La final actualizezi primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md` si memoria
  `cerere-sesiune-documentatie`, cu sha-ul nou si ce ramane (urmatoarea: scurtarea la 8 pagini).
