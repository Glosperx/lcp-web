---
name: anatomia-cifrei-0690001
description: "Ce FACE de fapt sistemul care da 0.690001, cu cifre: r_fuz e o functie EXACTA de (r_A, r_B, rho(A,B), w) verificata la 3.3e-16; ponderea optima per limba ar aduce doar +0.0027, deci combinarea nu are joc; plus doua etichete pe care le-am citit greșit"
metadata:
  type: project
---

Scris 26 aug 2026, ca raspuns la "cand scot 0.69, ce fac de fapt si de ce nu-l pot bate". Toate
cifrele sunt recalculate din `output/fusion_preds_lolo_adoptat_m3k.csv` si din `output/dist/`.

## Ce e sistemul, pe un rand real (sinhaleza, idx 4431, y = 0.12)

```
  A: doua potriviri separate pe embedding, per limba
     p_en    = 1.2142   Ridge(300)+HGB(d3) potrivit NUMAI pe CompLex EN, prezice toate 10 limbile
     p_multi = 0.7455   acelasi blend, potrivit pe CompLex EN + testul celorlalte NOUA limbi
     A = z(0.75*z(p_en) + 0.25*z(p_multi)) = 1.4062      w_src ales LOLO
     pe TREI encodere (xlmr, e5, labse), mediat pe z in interiorul limbii
  B = 0.9606           gemma4-12b-4bit, TREI prompturi, colaps de clase, temperatura 6.0
  p_fuz = 0.35*1.4062 + 0.65*0.9606 = 1.1166             w ales LOLO
```

Deci predictia finala e **0.35 ori un numar plus 0.65 ori alt numar**. 72 de potriviri de model si 30
de apeluri de LLM produc doua coloane, iar ele se amesteca liniar.

## DOUA etichete pe care le-am citit greșit, si merita retinute ca sa nu se repete

1. Modelul e **`gemma4-12b-4bit`**, nu gemma3.
2. In `M3K`, **cifra 3 e numarul de PROMPTURI**, iar `K` e modul `colaps`. Capcana: fisierul
   `output/bt_params_bakeoff_test_M3K.csv` are o coloana `K=3` care e numarul de BLOCURI de nota dupa
   colaps (partitia `1|23|45`). Sunt **doi de 3 diferiti** in aceeasi eticheta, si citind numai
   fisierul de parametri am concluzionat greșit ca sunt doua prompturi.
   Structura reala, din `make_fs_runs.py`: fiecare sursa alternativa are UN prompt, fisierul sistemului
   are DOUA, deci `M3 = marcat + cele doua prompturi ale sistemului`. `FS3`, `L3`, `FR3`, `R3` sunt
   acelasi lucru cu alta a treia sursa. **Reconstruit exact**: media celor trei, la T=6.0 cu colaps
   `1|23|45` si fiecare bloc valorat cu media notelor lui, da r = 0.664934, identic cu B din
   `bakeoff_test_M3K/` la sase zecimale.

## De ce trei prompturi si nu unul, masurat

```
  prompt 1 (sistem)   0.625598
  prompt 2 (sistem)   0.655658      <- cel mai bun singur
  prompt 3 (marcat)   0.624046      <- cel mai SLAB singur
  media celor doua    0.661415
  media celor TREI    0.664934      <- B-ul adoptat, +0.0093 peste cel mai bun singur
  corelatii: p1-p2 0.880   p1-marcat 0.831   p2-marcat 0.907
```

Al treilea prompt e cel mai slab si totusi adauga +0.0035, fiindca e cel mai decorelat de p1. Pura
reducere de varianta, ca la [[prompt-ansamblu-decorelat]] si [[ansamblul-de-prompturi-formula]].

## Cifra e o functie EXACTA de patru numere, verificat la 3.3e-16

    r_fuz(L) = (w*r_A + (1-w)*r_B) / sqrt(w^2 + (1-w)^2 + 2*w*(1-w)*rho(A,B))

Nu e aproximare. Consecinta: orice imbunatatire trebuie sa treaca prin `r_A`, `r_B`, `rho(A,B)` sau
`w`. **Nu exista al cincilea loc.** Pentru +0.01 pe fuziune:

```
  r_A        +0.0264    derivata 0.38
  r_B        +0.0142    derivata 0.70
  rho(A,B)   -0.0537
```

Scara: cea mai mare parghie gasita vreodata pe A e +0.027 (un encoder -> patru). Adica TOATA munca pe A
valoreaza +0.01 pe fuziune.

## Plafoane, si randul care inchide discutia despre fuziune

```
  sistemul de acum                                  0.690001
  w optim PE LIMBA, oracol imposibil                0.692708   <- +0.0027, adica NIMIC
  fuziunea = numai B                                0.664934
  fuziunea = numai A                                0.599290
  rho(A,B) = 0.387 peste tot (cat e pe si)          0.755987
  rho(A,B) = 0 peste tot, r_A si r_B neatinse       0.869579
  A perfect (r_A = 1), rho neatins                  0.843654
  B perfect (r_B = 1), rho neatins                  0.928710
```

**Combinarea nu are joc in ea** (+0.0027 la oracol). Tot spatiul e in cele doua semnale. Iar randul cu
`rho = 0` spune ce se plateste: cu ACELEASI doua semnale, decorelate, ai avea 0.8696. Diferenta de 0.18
e strict redundanta, fiindca A si B sunt doua masuratori ale aceluiasi lucru: A citeste dificultatea din
embedding plus tabelul de frecvente, B din priorul LLM-ului.

## Distributia pe limbi, unde e singurul spatiu liber

```
  si 0.4350   fil 0.5074   ca 0.5639   |   media celorlalte sapte 0.7705   |   en 0.8723
  cele trei de jos ridicate la media celorlalte sapte    +0.0805
  cele trei de jos, fiecare +0.05                        +0.0150
  cele SAPTE de sus, fiecare +0.05                       +0.0350   (imposibil, en e la 0.87)
```

Si acolo se aliniaza cu [[castigul-pe-a-plateste-doar-unde-rho-ab-e-mic]]: pe sinhaleza `rho(A,B)` e
0.387, cel mai mic din set.
