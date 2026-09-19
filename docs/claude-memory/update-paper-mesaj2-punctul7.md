---
name: update-paper-mesaj2-punctul7
description: "29 aug 2026 - al doilea mesaj de update pentru paper (punctul 7) a fost TRIMIS efectiv catre coordonator (text finalizat in output/update_paper_draft.txt); contine descompunerea pe prompt a semnalului B, testul de al 4-lea prompt (fewshot) care NU decoreleaza mai mult, si coada de limbi ca singura pista ramasa"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1882d839-10eb-4e29-beee-2a034d917ceb
  modified: 2026-08-29T12:56:28.481Z
---

Continuarea lui [[cifra-de-raportat-in-paper]] si [[sistemul-e-0690001-m3k]]. Sectiunile 1-6 din
`output/update_paper_draft.txt` erau deja trimise inainte de aceasta sesiune; sectiunea 7 (si tot ce
urmeaza) s-a scris acum, iterativ, direct in fisier, ca mesaj de sine statator (nu mai reia contextul
lui A/B/LOLO).

## Ce contine punctul 7

- Rezultatul: 0.674946 -> 0.690001, prin al treilea prompt (target word / marcat).
- Tabel cu familiile de regresori incercate pentru A (liniare, arbori, TabFM), cu r_A individual si
  delta fata de Ridge+HGB in pereche. LightGBM si CatBoost confirmate ca fiind testate (nu doar HGB).
- TabFM: 774 -> 256 coloane (PCA), bfloat16 (float32 nu incape, float16 da NaN), 8 membri, 2 sesiuni
  Colab cu checkpoint.
- Cele 3 prompturi ale sistemului, cu textul exact, plus explicatia soft-read (softmax pe logits din
  etapa de prefill, nu pe textul generat).

## Ce s-a masurat NOU in aceasta sesiune (nu era in nicio memorie de dinainte)

Rulat direct prin `make_fs_runs.py` + `fuse_ab.py` (nu presupus), pe acelasi protocol LOLO/test ca
sistemul adoptat:

```
  prompt (solo, ca singur B)   r_B      fuziune A + acest prompt
  expert                       0.6239   0.6699
  varianta scurta              0.6531   0.6801   <- cel mai bun solo
  target word (marcat)         0.6191   0.6731
  few-shot                     0.6346   0.6715
```

Corelatia bruta (T=1) intre cele 4 prompturi:

```
              expert  scurt  target word  few-shot
  expert       1.000  0.831    0.765       0.813
  scurt        0.831  1.000    0.879       0.830
  target word  0.765  0.879    1.000       0.816
  few-shot     0.813  0.830    0.816       1.000
```

Few-shot NU e mai decorelat decat target word - e mai corelat cu toate celelalte trei (0.81-0.83) decat
e target word cu expert (0.765, cea mai mica pereche din tabel).

**Testul cerut de Alexandru**: ansamblu de 4 prompturi (expert+scurt+target word+few-shot, mod colaps).

```
                            3 prompturi (adoptat)   4 prompturi (+few-shot)
  B                              0.6649                   0.6679
  rho(A,B), medie pe limba       0.6870                   0.6934   <- URCA, nu scade
  fuziune finala                 0.690001                 0.6903
```

Diferenta fuziunii: +0.0003, CI [-0.0010, +0.0016], P(>0)=67.3% - zgomot pur. **Mecanismul**: B urca
putin, dar rho(A,B) urca si el (mai corelat cu A, nu mai putin), deci cele doua efecte se anuleaza.
Urca semnificativ pe franceza (+0.0122) si japoneza (+0.0072), scade semnificativ pe germana (-0.0123).
**Al 4-lea prompt nu s-a adoptat.**

## Artefacte pe disc (nu adoptate, doar de test)

`output/bakeoff_test_P1ONLY/`, `_P2ONLY/`, `_P3ONLY/`, `_P4ONLY/`, `_FSM4K/`, plus rapoartele
`e_fusion_lolo_p{1,2,3,4}only.md` si `e_fusion_lolo_fsm4k.md`. CSV-urile temporare (p1only/p2only cu un
slot NaN-uit) sunt in scratchpad, nu in repo.

## Discutia despre "ce mai raman de incercat", inchisa din nou

Confirmat din [[al3lea-semnal-ce-ramane-deschis]]: la nivel de model/prompt/semnal, e inchis - "nu mai
am nicio parghie inginereasca cu valoare asteptata pozitiva". Singura pista cu potential real ramasa:
coada de limbi (sinhaleza 0.4350, filipineza 0.5074, fata de 0.77 media celorlalte sapte) - lipsa de
resurse (wordfreq si lematizator lipsesc pe sinhaleza), nu problema de modelare. Vezi
[[prioritate-contributie-si-drumul-la-07]].

## Trimis efectiv, 29 aug 2026

Alexandru a confirmat ca a trimis mesajul (punctul 7, cu tot cu ce urmeaza dupa el in fisier) catre
coordonator. E acum asteptare de raspuns/feedback pe acest al doilea update; nu se stie inca daca
coordonatorul cere altceva sau accepta ca sistemul ramane la 0.690001.
