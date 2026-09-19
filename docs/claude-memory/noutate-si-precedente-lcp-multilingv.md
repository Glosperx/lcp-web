---
name: noutate-si-precedente-lcp-multilingv
description: "Verificarea de noutate din 16 aug 2026, completata 18 aug: G-Scale ne ia doua argumente (logits ieftini, complementaritate LLM-frecventa), run 1 al lui Archaeology e singurul reper zero-label, frozen-vs-finetuned e replicare"
metadata: 
  node_type: memory
  type: project
  originSessionId: f92e8d7e-2eca-4649-a573-d0cd5dc259e5
  modified: 2026-08-16T11:18:11.732Z
---

Făcut pe **16 august 2026**, cu doi agenți de research și lectura integrală a unui PDF. A costat
aproximativ 70 de apeluri web plus citirea lucrării japoneze. **Nu reface asta**, e scump și e aici.
Planul complet: `~/.claude/plans/cite-te-claude-plans-cite-te-claude-plan-eager-pine.md`, secțiunea V2.

## Lucrarea care părea să ne ia contribuția, și de fapt ne-o întărește

**Nohejl, Hayakawa, Ide, Watanabe (2025)**, *Journal of Natural Language Processing* 32(4):1129,
„A Japanese Dataset and Efficient Multilingual LLM-Based Methods for LS and LCP". Introduc **G-Scale**,
scoring calibrat din probabilități de token pentru LCP, pe toate cele 10 limbi MultiLS.

Părea că ne ia mecanismul semnalului B. **Nu ne-l ia**, fiindcă metoda lor **cere 30 de etichete în
limba țintă**, verbatim din §5: „The parameters β were fitted separately using the trial set for each
language", plus „3-shot examples sampled from the trial data for each language", plus temperatura
aleasă pe trial-urile tuturor limbilor. A noastră cere zero.

**Semnalul nostru B e G-Eval (Liu et al. 2023), nu G-Scale.** Formula din `solution_bert.py:281`,
`(Σ p·[1..5] − 1)/4`, e formula (1) a lor. G-Scale adaugă softmax cu temperatură calibrată plus o
regresie liniară antrenată pe trial.

**Cifra de reținut, din Tabelul 10 al lor, R² mediu peste 10 limbi:**

| Variantă | R² mediu |
|---|---|
| G-Eval simplu = **semnalul nostru B** | **−0.499** |
| + regresie pe trial-ul limbii țintă | +0.284 |
| G-Scale complet | +0.293 |

Deci nota brută a unui LLM e **grav decalibrată ca scară**, iar aproape tot câștigul lor vine din cele
30 de etichete țintă. Consecință: calibrarea noastră se antrenează pe trial-ul **limbilor rămase în
antrenare**, niciodată pe limba țintă. Diferența dintre cele două calibrări e un experiment nou, E12,
care măsoară direct cât valorează 30 de etichete țintă.

Ei folosesc **GPT-4o**, model închis și plătit. Noi folosim greutăți deschise. Axă de contrast curată.

Ablația lor de prompt: rolul explicit „You are an intermediate learner of {language}" duce R² mediu de
la 0.360 la 0.498. Deci conținutul promptului are efect mare.

**CORECȚIE, Appendix G citit în aceeași sesiune.** Cifrele de mai sus sunt R². **În Pearson,
diferența e +0.012**, nu uriașă: G-Eval 0.657, G-Scale 0.669, medie pe 10 limbi. Ei explică de ce:
corelațiile sunt invariante la o funcție liniară cu pantă pozitivă, deci ablațiile de regresie nu se
văd în ele. Prăpastia de la R² era pur un efect de scară.

**Fiindcă noi raportăm r, nu compozitul, decalibrarea nu ne atinge.** Costul lipsei etichetelor țintă,
în metrica noastră, e de ordinul a 0.012, și e deja publicat. Argument puternic pentru zero-label.

**Dar bara e mai sus decât credeam.** G-Eval simplu cu GPT-4o dă medie **0.657** pe 10 limbi, peste
TMU-HIT (0.654) și mult peste Archaeology (0.487).

> **CORECȚIE 19 august 2026, și e capcana care a produs deja o afirmație falsă într-un document.**
> Cifra de **0.657 a lui G-Eval NU e zero-label, e 3-shot.** Promptul lui Nohejl ia „3-shot examples
> sampled from the trial data for each language" la AMÂNDOUĂ variantele; G-Scale adaugă peste ele
> temperatura și cele 30 de etichete pentru β. Deci nici G-Eval nu se compară de protocol cu noi, iar
> „semnalul nostru B e G-Eval" e adevărat despre **formulă**, nu despre setare: a noastră e zero-shot.
> Se citește greșit tocmai fiindcă G-Eval e „doar promptul", și exact așa a ajuns în
> `output/update_paper_draft.txt` propoziția „comparabil corect fiindcă e tot zero-label", ștearsă
> între timp. **Singura bară comparabilă rămâne TMU-HIT zero-shot uniform la 0.610**, iar în lucrare
> revendicarea e +0.065 față de ea. `output/repere_publicate.md` avea eticheta corectă tot timpul. Tabelul complet Pearson per limbă, pentru baseline
de frecvență, Archaeology, GMU, TMU-HIT, G-Eval și G-Scale, e în planul din 16 august, §V2.a-bis.

**Atenție:** coloana „Archaeology" din tabelul lor amestecă run 1 și run 2 per limbă, fiindcă vine din
shared task findings. Când citezi run 1 ca baseline zero-label, ia cifrele din Tabelul 2 al lucrării
Archaeology, nu din findings.

## COMPLETARE, 18 august 2026: ce NU mai putem revendica

Recitind Nohejl integral, doua argumente pe care le aveam in minte sunt deja ale lui si **nu pot intra
ca noutate**:

1. **"Citim logits in loc sa esantionam, deci de 20 de ori mai ieftin."** E motivatia (1) declarata a
   lui, sectiunea 4. TMU-HIT foloseau n=20 esantioane la temperature 0.7; el a taiat-o la o singura
   trecere. Noi facem la fel, dar dupa el.
2. **"LLM-ul si frecventa sunt decorelate si se completeaza."** E Tabelul 12 al lui: R^2 urca de la
   0.498 la 0.575 adaugand log-frecventa, cu concluzia lui explicita ca semnalele sunt
   "relatively uncorrelated, complementing each other". Teza fuziunii A+B e anticipata conceptual.

**Ce ramane al nostru:** modele open-weight rulate local (el foloseste doar GPT-4o, iar TMU-HIT cer
explicit in Limitations o varianta open-source), **zero etichete in limba tinta**, LOLO inclusiv la
alegerea modelului, encoder inghetat in loc de log-frecventa simpla, si **teza morfologica a fixului
de lema**, pe care n-o are nimeni.

**Doua lucruri de luat de la el, ieftine:**

- **Scalarea cu temperatura**, T=2.0, valoreaza +0.012 Pearson mediu si o putem alege LOLO, deci sub
  un protocol mai strict decat al lui. Cere re-rulare: `bakeoff_trial.py` scrie doar scalarul `B`,
  nu vectorul de 5 probabilitati.
- **TUBELEX log-range** bate log-frecventa wordfreq (R^2 0.456 fata de 0.387 pe en/ja/es). Si o lista
  de frecvente pentru sinhaleza, Fernando & Dias 2021, acolo unde `zipf_safe` renunta acum.

Apendicele H al lui coboreaza independent ca log-frecventa **strica** pe ca, fil si si, "low quality
of the respective corpora". Alea sunt exact cele trei limbi slabe ale noastre.

Agregarea reperelor si tabelul complet: [[agregare-medie-pe-limbi-nu-pooled]] si
`output/repere_publicate.md`.

## Lucrarea coordonatorului e descrisă greșit în planurile vechi

[2024.bea-1.55](https://aclanthology.org/2024.bea-1.55/), Cristea și Nisioi, are **trei run-uri**, nu
unul. Traducerea e cel mai slab. **Run 1 a fost antrenat doar pe engleză, dintr-un bug declarat în
nota de subsol 1**, și e **singurul rezultat publicat pe MLSP obținut fără etichete în limba țintă**.

Pearson run 1: pt 0.7143, de 0.5508, it 0.5341, fr 0.5335, es 0.5274, fil 0.3620, ca 0.2960,
ja 0.2803, si −0.0290.

**Îl batem pe toate cele trei limbi unde avem cifre**: it 0.6006, pt 0.7775, es 0.6185. E o comparație
mult mai bună decât cea cu leaderboard-ul, fiindcă e la același protocol.

Bonus: run 1 bate run 2 exact pe romanice (ca, fr, it, pt, es), adică etichetele țintă **strică** pe
limbile apropiate tipologic. Dovadă independentă, publicată, în favoarea tezei noastre.

## „Frozen bate fine-tuned" e replicare, nu contribuție

Stabilit de Peters, Ruder, Smith 2019 ([W19-4302](https://aclanthology.org/W19-4302/)) pentru monolingv
și de **Liu, Winata, Xu, Fung 2021** ([2021.repl4nlp-1.8](https://aclanthology.org/2021.repl4nlp-1.8/))
pentru cross-lingv, care e citarea canonică pentru „fine-tuning distruge alinierea cross-lingvă".

Se reformulează ca **„cuantificăm marja, nu descoperim semnul"**, pe regresie cu țintă continuă, unde
relația nu a fost măsurată. Linia 719 din `Paper/documentation_overleaf.tex` trebuie să citeze acum
Liu et al. 2021, altfel arată ca omisiune.

## Precedentul care amenință Δ

**Wilcox, Pimentel, Meister, Cotterell, Levy (2023)**, TACL, [arXiv 2307.03667](https://arxiv.org/abs/2307.03667),
măsoară exact Δ per limbă, mGPT față de monolingve, pe 11 limbi, pentru surprisal, și concluzionează
„multilingual and monolingual language models may be equally viable options". Dacă Δ-ul nostru iese
zero, ei ne-au anticipat.

## Ce nu are precedent

**Nimeni nu a rulat leave-one-language-out pe MLSP.** De asta e revendicarea centrală.

**Rezervă:** graful de citări Semantic Scholar a întors 404 și 429, deci lista lucrărilor care citează
MLSP 2024 e **incompletă**. De reconfirmat manual înainte de submit.

**Why:** două sesiuni au murit pe limita contului încercând research-ul ăsta; a treia l-a terminat.
Re-derivarea costă o sesiune întreagă.

**How to apply:** citează Nohejl et al. ca reper „cu 30 de etichete țintă", nu ca amenințare. Citează
run 1 al lui Archaeology ca baseline obligatoriu. Nu vinde rezultatul negativ ca descoperire.
Vezi [[paper-extensie-multilingva-arr-octombrie]], [[brate-llm-per-limba]],
[[rals-rolcp-datele-sunt-ale-lui-nisioi]].
