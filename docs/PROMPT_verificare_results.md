Verifici si rescrii sectiunea 4, Experimental Results, din `Paper/Articol_Multilingv/documentatie_overleaf.tex`
(documentatia de curs, sablon ACL). Experimentele sunt gata. In sesiunea asta nu rulezi experimente noi: nu
rulezi modele de limbaj, nu reantrenezi nimic. Ai voie sa citesti fisierele de rezultate, sa rulezi
`release/fuse.py` si sa recalculezi din CSV-urile existente.

Lucrezi in trei faze. Faza 1 e auditul, numai in chat. Nu modifici fisierul pana nu iti dau "go".

## Starea

- .tex-ul are sha1 110df127 si se compileaza curat, pe 9 pagini. Daca sha-ul difera, imi spui intai ce s-a
  schimbat. Daca am editat eu, textul meu ramane cuvant cu cuvant.
- **Sectiunea 3, Method, e APROBATA.** N-o modifici. E modelul de stil pentru sectiunea 4.
- Sectiunea 4 (liniile ~838-1103) are 5 subsectiuni: 4.1 Per-Language Results (Tabel 1), 4.2 Ablations and
  Baselines (Tabel 2), 4.3 Comparison with Published Results (Tabel 3), 4.4 Feature Attribution (Figura
  SHAP si tabelul tab:shap), 4.5 Representation Geometry (Figura t-SNE).
- Paperul-model e RALS: Anghel et al., EMNLP 2025, `~/Downloads/2025.emnlp-main.1603.pdf`.

## Ce citesti intai

1. Memoria: `cerere-sesiune-documentatie`, `baseline-claude-opus-bate-sistemul`, `model-rals-emnlp-2025`,
   `preferinte-de-scriitura-paper`, `scrie-uman-nu-overexplain`, `raspunsuri-fara-diacritice-fara-tabele-md`,
   `noutate-si-precedente-lcp-multilingv`, `engleza-nu-e-zero-label`, `shap-semnal-a-adoptat`,
   `proiectii-centrare-rezultat`.
2. `docs/PROMPT_sesiune_documentatie_continuare.md`, pentru stilul cerut si pentru sursele cifrelor.
3. .tex-ul intreg: Method cu atentie, apoi sectiunea 4.
4. RALS, in intregime: sectiunea 4 Results, tabelele, Limitations si anexele.
5. `docs/instructions_documentation.md`, pentru ce cere cursul.

## Faza 1: auditul (doar in chat)

### A. E adevarat?

Verifici fiecare cifra si fiecare afirmatie din sectiunea 4, inclusiv caption-urile si comentariile LaTeX.
Fiecare cifra are langa ea un comentariu cu sursa: verifici ca sursa chiar contine cifra si ca rotunjirea e
corecta. Afirmatiile despre metoda le verifici in `release/` (fisier:linie). Afirmatiile despre alte lucrari
le verifici in PDF-uri.

Sursele:
- `output/doc_fuse_ro11.{txt,csv}`: rularea pe 11 limbi, 0.692521 [0.6789, 0.7057], n 7211.
- `output/doc_fuse_mlsp10.{txt,csv}`: rularea pe 10 limbi, fara romana, 0.689745 [0.6751, 0.7035], n 5624.
- `output/doc_ablations.txt`: ablatiile din `release/fuse.py`.
- `output/doc_ablations_qwen_ro.txt`: cele doua Qwen pe 11 limbi. Au fost rulate pe 10 oct intr-o copie a
  release/, iar randurile pentru romana sunt in `output/doc_qwen_ro_signal_b.csv`. release/ nu le contine,
  deci nu le poate reproduce. Asta e o problema cunoscuta, nu o semnala din nou.
- `output/doc_claude_baseline.txt`: baseline-ul Claude, lipit de mine dintr-o alta sesiune. Predictiile si
  promptul Claude nu sunt in repo. Combinatiile cu Claude sunt calculate pe versiunea veche a predictiilor
  noastre (0.6900 pe 10 limbi, fata de 0.6897); am decis ca raman, cu comentariul LaTeX.
- `output/shap_signal_a_per_encoder_importance.csv` si `_correlations.csv`, pentru 4.4.
- `output/doc_counts.txt` si `output/repere_publicate.md`.
- Pentru Tabelul 3: Nohejl et al. 2025 (Tabel 13), Shardlow et al. 2024 (Anexa B), Cristea si Nisioi 2024
  (Tabel 2), Enomoto et al. 2024. Daca PDF-urile nu sunt local, le descarci de pe ACL Anthology intr-un
  director nou din scratchpad. Ce s-a verificat deja pe 9 oct e scris in comentariul de deasupra tabelului.
  Il reverifici, nu il copiezi.
- Nu se citeaza nicaieri: 0.674946, 0.683849, 0.690001, 0.692527, 0.693718, 0.687831.

Exemple de afirmatii de recalculat din CSV (nu e o lista completa):
- "above both of its signals in ten languages";
- "Signal B is the stronger signal in nine languages";
- "a temperature of 4 or 6", "w is 0.35 or 0.40", "w_src lies between 0.625 and 1";
- "A single encoder ... loses between 0.003 and 0.005": pe ce coloana, si e adevarat pe amandoua?
- "On seven languages our value is the highest in Table 3", si ce e ingrosat in Tabelul 3;
- in 4.4, "signal A is an affine function of the ridge and HGB predictions, so its Shapley values follow
  exactly": verifici in `release/signal_a.py` si in `analysis_shap_signal_a_per_encoder.py`;
- in 4.5, cifrele 0.57 / 0.33 / 0.11: se pot reproduce din fisierele numite in comentariu?

### B. Ce lipseste si ce ar trebui adaugat

Compari sectiunea 4 cu sectiunea Results din RALS si cu ce cere cursul ("an evaluation report of your
method", tabele si figuri "that may convince a reader"). Pentru fiecare propunere spui ce aduce si unde ar
merge: in Results, in Limitations, in What Did Not Work (pasul 4) sau in Implementation (pasul 6). Nu
propui continut fara sursa in repo.

Candidati pe care ii evaluezi tu (pot fi respinsi):
- intervale de incredere sau un test pereche pentru ablatii, care acum n-au niciunul;
- timpul de rulare si costul (README-ul din release/ are 0.36 s pe citire pentru Gemma 4, ~2 h 10 min);
- o analiza de erori sau exemple concrete, daca RALS are asa ceva;
- engleza nu e complet fara etichete: CompLex EN intra in antrenarea lui A si la L = en (vezi memoria
  `engleza-nu-e-zero-label`). Results spune asta?
- pe romana, Qwen3.5 9B bate Gemma 4 (B .684 fata de .659, fuziunea .784 fata de .739,
  `output/doc_ablations_qwen_ro.txt`), dar selectia LOLO alege Gemma. Acum nu e in text.
- Opus zero-shot e PESTE metoda noastra. Results nu are voie sa sugereze ca suntem cei mai buni fara
  etichete. Tabelul 3 contine doar metode publicate pe MLSP; verifici ca textul din 4.3 nu spune mai mult.

### C. Stilul, dupa Method si dupa RALS

Method e modelul. Regulile cerute de mine pe 10 oct:
- propozitii simple si concrete; spui direct ce am facut, apoi pe scurt de ce;
- fara trimiteri vagi de tipul "as described below": metoda concreta se spune pe loc;
- fara deductii inlantuite de tipul "X, and Y, so Z"; faptele se spun separat;
- expresii respinse: "To this end", "held out (in turn)", "unweighted", "Two adjustments follow",
  "neighbouring", "on their own", "complementary", "gold", "the system";
- fara em-dash si fara adaugiri pe care nu le-am cerut;
- termenii din text sunt aceiasi ca in Method, in figuri si in tabele;
- un termen nou pentru un incepator se explica scurt la prima mentiune.

Inconsistente deja observate, de confirmat sau respins:
- 4.5 spune "target vectors" / "vectors", iar Method spune "embeddings";
- trimiterile la pasi: "step~8" si "step~2" cu litera mica in Results, dar titlurile din Method sunt
  "Step 8: Weighted Average";
- in 4.1, 0.6925 are patru zecimale, iar restul cifrelor din text trei;
- "signal~A/B" cu litera mica in text, "Signal A" in figuri. Am zis ca e ok; nu mai insista.

De la RALS iei structura si tonul sectiunii Results: cum introduce un tabel, cum justifica un baseline, cat
de lungi sunt paragrafele, ce pune in caption si ce pune in text. Spui concret ce preiei si ce nu.

### Formatul auditului

O lista in chat, grupata asa: (1) Fals, (2) Prea tare sau neclar, (3) Lipseste, (4) Stil si termeni,
(5) Inconsistente cu Method. Pentru fiecare punct dai linia din .tex, textul actual citat scurt, sursa
verificarii si propunerea. La final, un rezumat de 3-4 randuri: ce e grav si ce e cosmetic.

## Faza 2: planul

Dupa ce raspund la audit, propui planul pe paragrafe pentru fiecare subsectiune: ce ramane, ce se scoate,
ce se adauga, ce se reformuleaza. Astepti "go".

## Faza 3: rescrierea, dupa "go"

- Inainte de orice modificare faci un backup al .tex-ului in scratchpad.
- Modifici doar sectiunea 4, plus caption-urile tabelelor si figurilor ei. Method nu se atinge. Daca o
  corectura cere o schimbare in alta parte, intrebi intai.
- Frazele reformulate de mine raman cuvant cu cuvant.
- Langa fiecare cifra si fiecare detaliu de metoda pui un comentariu LaTeX scurt, in engleza, cu sursa.
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
