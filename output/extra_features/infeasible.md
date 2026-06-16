# Trasaturi sugerate dar INFEZABILE pe romana (justificare raport)

Sergiu a listat si corelate psiholingvistice clasice. Pe RO lipsesc resursele:

- **Frecventa in corpus de copii** (analog AOCHILDES/CHILDES, BabyLM): exista pe ENGLEZA, NU pe romana.
  wordfreq nu are split child-directed. Construirea unui corpus child-RO = proiect separat (Sergiu a
  sugerat-o ca posibila contributie). Proxy via wordfreq high-freq = doar frecventa generala (redundant).
- **Varsta de achizitie (AoA)**: lexicoane mari (Kuperman EN) exista pe EN; pe RO ~inexistent public.
  Maparea EN->RO prin traducere/embedding = zgomotoasa, out of scope.
- **Imaginabilitate / concretete**: la fel — norme MRC/Brysbaert pe EN, lipsa pe RO.
- **Cuvinte similare in alte propozitii** (semantic contextual): definitie vaga; cel mai apropiat masurabil
  = relatiile RoWordNet (polisemie/sinonime) — TESTATE in analysis_features.py, redundante cu frecventa.

Concluzie: corelatele psiholingvistice RO necesita resurse care nu exista; construirea lor = directie de
cercetare, nu lever de scor pe termen scurt. Cele DISPONIBILE (POS/dep/NER spaCy-RO, RoWordNet semantic)
au fost testate si sunt redundante cu frecventa (vezi feature_eval.csv).
