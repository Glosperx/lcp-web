Continuam documentatia de curs din `Paper/Articol_Multilingv/documentatie_overleaf.tex` (titlu: "Lexical Complexity
Prediction Without Target-Language Labels", sablon ACL). Experimentele sunt gata. Nu rulam experimente noi.

In sesiunea asta scriem sectiunea Limitations (`\section*{Limitations}`, acum goala, doar un comentariu). Intai lista de
puncte in chat, aleasa de mine. Apoi textul scris de tine, aprobat in chat. Abia dupa aceea il rescrie Gemma 4, cu un
prompt care contine textul aprobat si faptele care trebuie sa ramana adevarate. Textul final din .tex e cel al lui
Gemma, pus neschimbat. Pas cu pas, cu aprobarea mea inainte de pasul urmator.

## Starea

- .tex sha **04022d88** (verifici cu `shasum`), urcat de mine in Overleaf pe 11 oct seara. Daca sha-ul difera,
  intrebi inainte sa faci orice.
- Acceptate de mine: Abstract si Keywords (Gemma 4, `_v5`), Introduction, Related Work, Method, Experimental Results,
  What Did Not Work, Conclusions, Implementation, Acknowledgments. Nu le atingi fara cerere.
- Dupa Limitations raman: verificarea finala cu scoaterea lui `\nocite{*}`, autori si emailuri, apoi scurtarea la 8
  pagini fara anexe, sesiune SEPARATA. Acum: 14 pagini, corpul se termina pe pagina 12.
- Starea completa: primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md`.

## Ce citesti intai

1. Memoriile: `cerere-sesiune-documentatie`, `text-final-rescris-de-gemma`, `preferinte-de-scriitura-paper`,
   `scrie-uman-nu-overexplain`, `lista-utilizatorului-nu-se-reformuleaza`, `fara-agenti-multipli-tokeni`,
   `model-rals-emnlp-2025`, `bifurcatii-de-declarat`, `optimismul-de-selectie-masurat`,
   `ansamblul-de-prompturi-formula`, `baseline-claude-opus-bate-sistemul`, `noutate-si-precedente-lcp-multilingv`,
   `engleza-nu-e-zero-label`, `paper-slabiciuni-de-reviewer`.
2. Din .tex: comentariul de sub `\section*{Limitations}`; comentariile de sursa din Introduction (liniile cu "not
   claimed") si din Related Work; Evaluation Protocol (3.5); in Results, comparatia LLM-urilor pe trial (4.2, Signal B)
   si alegerea straturilor in dezvoltare (Signal A); Comparison with Published Results (4.4); What Did Not Work;
   Conclusions; Data Sharing din Acknowledgments. Limitations nu are voie sa contrazica nimic de acolo.
3. Limitations din RALS, modelul de forma: `pdftotext ~/Downloads/2025.emnlp-main.1603.pdf -`, sectiunea "Limitations"
   (proza, fara buline, ~200 de cuvinte, lucruri concrete despre date si metoda, se termina cu bugetul).

## Pasul 1: Lista in chat

Imi dai lista de puncte candidate. Pentru fiecare: o propozitie in romana, sursa (fisier si linie, sau memorie
verificata in fisierul de output), si daca e deja spus in text (unde). Ce e deja in text intra cel mult ca trimitere
scurta, fara sa repete ideea. Eu aleg ce intra si in ce ordine. Nu scrii nimic in .tex la pasul asta.

Candidati de verificat (nu toti intra; verifici fiecare inainte sa-l propui):
- Al treilea prompt a fost ales in dezvoltare, cu scorurile de test la vedere (comentariul din Introduction,
  memoria `ansamblul-de-prompturi-formula`).
- Setarile fixate in cod (alpha-ul ridge, arborii HGB, fereastra de 500 de caractere, ultimele patru straturi, cele trei
  encodere, cele trei prompturi) au fost fixate in dezvoltare, pe versiuni mai vechi ale metodei, unele cu scorurile de
  test la vedere. Method spune ca sunt "fixed values, the same for every language"; Results spune ca straturile s-au
  ales in dezvoltare.
- Lista scurta de LLM-uri a fost comparata pe etichetele de trial ale celor zece limbi MLSP, inclusiv ale limbii
  evaluate. E deja in 4.2; in Limitations ar fi singura exceptie de la "nicio eticheta a limbii de test".
- Alegerea intre configuratiile masurate am facut-o noi, uitandu-ne la scorul de test (`bifurcatii-de-declarat`,
  `output/e_adoptie.md` sectiunea 4). Numarul de configuratii din memorie (51) e din august si e pe un n vechi: nu-l
  citezi decat daca il renumeri din fisierele de jurnal de acum si imi spui cum; altfel fraza fara cifra.
- Dependenta de ordinul doi din LOLO: e deja in 3.5 (Evaluation Protocol). Cel mult trimitere.
- Testul curatat (5.624) fata de cel publicat (5.627) si comparatia fara intervale pereche: deja in 4.4. Cel mult
  trimitere.
- Trasaturile lexicale lipsesc sau sunt slabe pe unele limbi (frecventa indisponibila pe sinhaleza, silabele si
  majusculele pe japoneza si sinhaleza); corelatiile cele mai mici sunt pe sinhaleza si filipineza (deja in
  Conclusions). Verifici in Method ce e spus deja.
- Efectul centrarii embeddingurilor pe corelatie nu e masurat separat (de verificat ca e asa si ca nu e deja in text).
- Pe romana singura, Qwen3.5 9B da mai mult decat Gemma 4, dar selectia LOLO alege Gemma (`output/doc_ablations_qwen_ro.txt`;
  verifici daca e deja in 4.2).
- Claude Opus 5.5 zero-shot e peste metoda noastra: deja in Conclusions si 4.4. Nu se repeta.
- Eye-tracking doar pe romana: deja in What Did Not Work si Conclusions. Nu se repeta.
- Bugetul / resursele, ca in RALS: doar daca exista o sursa (README, jurnale de timp). Fara estimari inventate.

Semnalezi separat, nu in Limitations: "All experiments use publicly released datasets" din Data Sharing (nu s-a
verificat ca partea romaneasca MultiplEYE e publica).

Cifre: doar cele cu sursa intr-un fisier de output de acum. Nu citezi 0.674946, 0.683849, 0.690001, 0.692527,
0.693718, 0.687831 si nici cifrele de pe n=5606. Cifrele din memorii se verifica in fisierul lor inainte de folosire.

## Pasul 2: Textul scris de tine

Dupa ce aleg lista: un paragraf sau doua de proza, ca RALS, fara buline, ~150-250 de cuvinte. Fiecare fapt are
sursa in comentariu LaTeX in engleza, la capat de rand. Intai mi-l dai in chat, cu sursele. Il pui in .tex abia dupa
OK-ul meu. Reformularile mele le pui cuvant cu cuvant; daca vezi o problema, o semnalezi separat.

Atentie la revendicari: Limitations nu slabeste ce e adevarat si nici nu iarta ce nu e. "Zero-label" ramane precis:
nicio eticheta a limbii de test nu intra in antrenare sau in alegerea setarilor; exceptiile reale (lista
scurta de LLM-uri pe trial, al treilea prompt, setarile fixate in dezvoltare, alegerea intre configuratii) se spun
direct, fara infrumusetare si fara dramatizare.

## Pasul 3: Rescrierea cu Gemma 4

Aceeasi procedura ca la Abstract (`docs/PROMPT_gemma_abstract*.txt` sunt exemplul cel mai recent):

- Prompt nou: `docs/PROMPT_gemma_limitations.txt`, in engleza: (1) ce e textul si "Rewrite it so that it reads more
  naturally: change the wording and the sentence structure, not the facts"; (2) textul aprobat intre `<<<` si `>>>`;
  (3) "Facts that must stay true", fiecare fapt pe o linie, cu cifrele exact; (4) "Rules": doar faptele date, nicio
  cifra schimbata sau scoasa, lungime cel mult cat originalul, fara em-dash/en-dash, propozitii scurte, o idee pe
  propozitie, fara "X, and Y, so Z", fara figuri de stil, fara "the system", "we" pentru autori; (5) "Output only the
  rewritten section in LaTeX, with no title, no comments and no explanations."
- Rulare (Mac, MLX, offline):
  `HF_HUB_OFFLINE=1 /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python docs/gemma_introducere.py docs/PROMPT_gemma_limitations.txt <scratchpad>/gemma_limitations_seed0.txt`
  (gemma-4-12B-it-qat-OptiQ-4bit, revizia 63912b88, temperatura 0.7, top-p 0.95, seed 0, gandirea oprita, ~1 minut).
- Verifici raspunsul fata de lista de fapte: fiecare cifra, nicio afirmatie noua, nicio ambiguitate noua. Imi dai in
  chat textul lui Gemma si ce ai gasit, si intrebi daca il pui.
- Daca Gemma doar copiaza textul, spui asta si propui o rerulare care cere explicit sa schimbe structura frazelor.
- La OK, il pui in .tex NESCHIMBAT (rupt la ~100 de caractere), cu sursele in comentarii la capat de rand si un
  comentariu deasupra: modelul, revizia, promptul, scriptul, seed-ul, data. Verifici cu un script ca textul din .tex,
  fara comentarii, e identic cu raspunsul lui Gemma.
- Schimbarile cerute de mine dupa asta trec tot prin Gemma: prompt `_v2`, `_v3`, pornind de la ultimul raspuns al lui
  Gemma, cu "Make only this change. Every other sentence stays word for word." Exceptie: schimbari de forma cerute
  explicit (titluri, enter-uri), facute direct si notate in comentariul de deasupra.

## Stil (din review-urile mele)

- Fara em-dash, fara deschidere de tip definitie, fara aforisme, fara "the system" pentru lucrarea noastra, fara
  formule, nicio idee spusa de doua ori, nimic adaugat necerut, fara cadru de competitie sau de tema de facultate.
- Propozitii scurte si concrete, o idee pe propozitie, fara deductii inlantuite ("X, and Y, so Z").
- "test language", nu "target language" ("target" e cuvantul tinta). "grouping", nu "blocks".
- In chat: romana, fara diacritice, fara tabele markdown, propozitii scurte.

## Compilare si reguli

- Inainte de fiecare scriere: backup al .tex-ului in scratchpad. Compilezi intr-un director gol din scratchpad
  (.tex + acl.sty + acl_natbib.bst + figures/ din `Paper/Articol_Multilingv/`, pdflatex, bibtex, pdflatex de doua ori;
  daca logul zice "Label(s) may have changed", inca o trecere). Conditii: 0 erori, 0 Undefined, 0 `??`, 0 Overfull.
  Atentie: hook-ul rtk poate goli iesirea lui `grep -c`; numara in log cu python. Spui cate pagini are documentul si pe
  ce pagina se termina corpul.
- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Fara subagenti; verifici singur, cu grep.
- La final actualizezi primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md` si memoria
  `cerere-sesiune-documentatie`, cu sha-ul nou si ce ramane (verificarea finala cu scoaterea lui `\nocite{*}`, autori
  si emailuri, apoi scurtarea la 8 pagini).
