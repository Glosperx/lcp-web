Continuam documentatia de curs din `Paper/Articol_Multilingv/documentatie_overleaf.tex` (titlu: "Lexical Complexity
Prediction Without Target-Language Labels", sablon ACL). Experimentele sunt gata. Nu rulam experimente noi.

In sesiunea asta scriem Abstractul si revizuim keywords. Intai il scrii tu si il aprobam in chat. Abia dupa ce e ok, il
rescrie Gemma 4, cu un prompt care contine textul aprobat si faptele care trebuie sa ramana adevarate. Textul final din
.tex e cel al lui Gemma, pus neschimbat. Pas cu pas, cu aprobarea mea inainte de pasul urmator.

## Starea

- .tex sha **05155e79** (verifici cu `shasum`), urcat de mine in Overleaf pe 11 oct noaptea. Daca sha-ul difera,
  intrebi inainte sa faci orice.
- Acceptate de mine: Introduction (scrisa de Gemma 4), Related Work, Method, Experimental Results, What Did Not Work
  (Gemma 4), Conclusions (Gemma 4, patru paragrafe), Implementation, Acknowledgments. Nu le atingi fara cerere.
- Abstractul e gol (doar un comentariu). Keywords exista deasupra lui, de revizuit la final.
- Limitations e inca nescris. Nu-l scrii in sesiunea asta; la final intrebi daca il facem acum sau separat.
- Dupa asta urmeaza scurtarea la 8 pagini fara anexe, sesiune SEPARATA. Acum: 14 pagini, corpul se termina pe pagina 12.
- Starea completa: primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md`.

## Ce citesti intai

1. Memoriile: `cerere-sesiune-documentatie`, `text-final-rescris-de-gemma`, `preferinte-de-scriitura-paper`,
   `scrie-uman-nu-overexplain`, `lista-utilizatorului-nu-se-reformuleaza`, `fara-agenti-multipli-tokeni`,
   `model-rals-emnlp-2025`, `baseline-claude-opus-bate-sistemul`, `noutate-si-precedente-lcp-multilingv`,
   `eye-tracking-cat-a-adus-in-r`.
2. Din .tex: comentariul din `\begin{abstract}`, keywords, Introduction, Conclusions, What Did Not Work si 4.4
   (Comparison with Published Results). Abstractul nu are voie sa contrazica nimic de acolo.
3. Abstractul RALS, modelul de forma: `pdftotext ~/Downloads/2025.emnlp-main.1603.pdf -` (incepe cu "We introduce...",
   un paragraf, ~100 de cuvinte, fara cifre de detaliu).

## Pasul 1: Abstractul scris de tine

Comentariul din .tex cere: problema, ce propunem, ce e inghetat si ce se antreneaza, cifra principala pe 11 limbi cu
intervalul, o fraza despre comparatia cu cifrele publicate. Un paragraf, cel mult ~150 de cuvinte.

Cifre permise (sursa in comentariu LaTeX in engleza, langa fraza):
- 11 limbi: 0.693, interval 0.679-0.706 (`output/doc_fuse_ro11.txt`, 0.692521 [0.6789, 0.7057]).
- Cele zece limbi MLSP: 0.690 (`output/doc_fuse_mlsp10.txt`, 0.689745 [0.6751, 0.7035]).
- Comparatia permisa: cea mai mare medie publicata, G-Scale 0.669, citeste 30 de etichete din fiecare limba evaluata;
  noi zero. Daca o pui, spui si cate etichete.
- Nu citezi 0.674946, 0.683849, 0.690001, 0.692527, 0.693718, 0.687831.

Atentie la revendicari:
- "Zero-label" se spune precis: nicio eticheta a limbii de test nu intra in antrenare sau in alegerea setarilor.
- Fara "cei mai buni" in general: Claude Opus 5.5 zero-shot da 0.721 pe 11 limbi, peste noi. Comparatia e doar cu
  metodele publicate pe MLSP 2024.
- Ce e inghetat: cele trei encodere (XLM-R base, LaBSE, multilingual E5 base) si LLM-ul (Gemma 4 12B, zero-shot, fara
  fine-tuning). Ce se antreneaza: ridge si HGB ale semnalului A, pe etichetele celorlalte limbi. Temperatura, gruparea,
  LLM-ul si ponderile se aleg pe celelalte limbi. Verifici formularea in Method inainte sa o scrii.
- Nicio idee care nu e deja in text. Nicio cifra in afara celor de sus.

**Intai imi dai abstractul in chat**, cu sursa fiecarei cifre. Il pui in .tex abia dupa OK-ul meu. Reformularile mele
le pui cuvant cu cuvant; daca vezi o problema, o semnalezi separat.

## Pasul 2: Rescrierea cu Gemma 4

Dupa ce abstractul e aprobat, il dai lui Gemma 4 sa-l rescrie. Procedura folosita deja la Introduction, What Did Not
Work si Conclusions (prompturile `docs/PROMPT_gemma_*.txt` sunt exemple de forma):

- Prompt nou: `docs/PROMPT_gemma_abstract.txt`, in engleza. Structura: (1) ce e textul si ce trebuie facut ("Rewrite it
  so that it reads more naturally: change the wording and the sentence structure, not the facts"); (2) textul aprobat
  intre `<<<` si `>>>`; (3) "Facts that must stay true", fiecare fapt pe o linie, cu cifrele exact; (4) "Rules": doar
  faptele date, nicio cifra schimbata sau scoasa, lungime cel mult cat originalul, fara em-dash/en-dash, propozitii
  scurte, o idee pe propozitie, fara "X, and Y, so Z", fara figuri de stil, fara "the system", "we" pentru autori, fara
  revendicarea ca suntem cei mai buni; (5) "Output only the rewritten abstract in LaTeX, with no title, no comments and
  no explanations."
- Rulare (Mac, MLX, offline):
  `HF_HUB_OFFLINE=1 /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python docs/gemma_introducere.py docs/PROMPT_gemma_abstract.txt <scratchpad>/gemma_abstract_seed0.txt`
  Scriptul: `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit`, revizia 63912b88, temperatura 0.7, top-p 0.95, seed 0,
  gandirea oprita. Dureaza ~1 minut.
- Verifici raspunsul fata de lista de fapte: fiecare cifra, nicio afirmatie noua, nicio ambiguitate noua (la What Did
  Not Work, Gemma a scris ca MultiplEYE "nu include alte limbi", fals pentru proiect). Imi dai in chat textul lui Gemma
  si ce ai gasit, si intrebi daca il pui.
- Daca Gemma doar copiaza textul (s-a intamplat la Conclusions), spui asta si propui o rerulare care cere explicit sa
  schimbe structura frazelor.
- La OK, il pui in .tex NESCHIMBAT (rupt la ~100 de caractere), cu sursele cifrelor in comentarii la capat de rand si un
  comentariu deasupra: modelul, revizia, promptul, scriptul, seed-ul, data. Verifici cu un script ca textul din .tex,
  fara comentarii, e identic cu raspunsul lui Gemma.
- Daca eu cer schimbari dupa asta, nu le faci de mana: modifici promptul (textul curent = ultimul raspuns al lui Gemma,
  plus faptul sau cerinta mea noua), il salvezi ca `_v2`, `_v3` si rerulezi Gemma. Exceptie: schimbari de forma pe care
  le cer explicit (titluri, enter-uri), pe care le faci direct si le notezi in comentariul de deasupra.

## Pasul 3: Keywords

Lista de acum: Lexical Complexity Prediction, Cross-Lingual Transfer, Zero-Label Evaluation, Leave-One-Language-Out,
Multilingual Encoders, Large Language Models. Propui in chat ce ramane si ce se schimba, cu motivul pe scurt (de
exemplu "Zero-Label Evaluation" descrie protocolul, nu metoda). Nu schimbi nimic fara OK.

## Stil (din review-urile mele)

- Fara em-dash, fara deschidere de tip definitie, fara aforisme, fara "the system" pentru lucrarea noastra, fara
  formule, nicio idee spusa de doua ori, nimic adaugat necerut, fara cadru de competitie sau de tema de facultate.
- Propozitii scurte si concrete, o idee pe propozitie, fara deductii inlantuite ("X, and Y, so Z").
- In chat: romana, fara diacritice, fara tabele markdown, propozitii scurte.

## Compilare si reguli

- Inainte de fiecare scriere: backup al .tex-ului in scratchpad. Compilezi intr-un director gol din scratchpad
  (.tex + acl.sty + acl_natbib.bst + figures/ din `Paper/Articol_Multilingv/`, pdflatex, bibtex, pdflatex de doua ori).
  Conditii: 0 erori, 0 Undefined, 0 `??`, 0 Overfull. Spui cate pagini are documentul si pe ce pagina se termina corpul.
- Nu atingi paper_full.tex, Paper/documentation_overleaf.tex sau release/. Nu faci git add si nici commit.
- Fara subagenti; verifici singur, cu grep.
- La final actualizezi primul bloc din `docs/PROMPT_sesiune_documentatie_continuare.md` si memoria
  `cerere-sesiune-documentatie`, cu sha-ul nou si ce ramane (Limitations, verificarea finala cu scoaterea lui
  `\nocite{*}`, autori si emailuri, apoi scurtarea la 8 pagini).
