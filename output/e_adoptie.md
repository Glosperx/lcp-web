# Dosarul adoptiei. Cele doua parghii neadoptate, si combinatia lor

Generat 2026-08-19 13:09:21 de `analysis_adoptie.py`. Nicio inferenta LLM, nicio fuziune recalculata aici: cele patru configuratii vin din `fuse_ab.py`, iar toate diferentele se construiesc din predictiile lor per instanta. Date brute: `output/adoptie.csv`, o linie per limba.

**Nu se adopta nimic in fisierul asta.** Fiecare cifra sta pe tagul ei, sistemul publicat reproduce bit cu bit fara niciun flag, iar decizia o ia Alexandru. Ce urmeaza sunt cifrele puse una langa alta, inclusiv cele care incurca.

## 1. Cele patru configuratii

```
sistem      fuse_ab.py --arm lolo --fit test --ens --tag ens \
                --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv
encmean     idem, --a-set fert_inloc=output/e1_frozen_preds_encmean-fara-xlmr-large_lemma_fert_inloc.csv
picktest    idem sistem, plus --pick-split test
combinatia  --pick-split test SI bratul A pe media de encodere
```

| configuratie | r mediu pe 10 limbi | fata de sistem | ce schimba |
|---|---|---|---|
| sistemul publicat | **0.664581** | referinta | |
| media a trei encodere | **0.669223** | +0.004642 | bratul A devine media neponderata a trei encodere standardizate in interiorul limbii, fara `xlmr-large` |
| selectia lui B pe test | **0.669735** | +0.005154 | modelul lui B se alege pe randurile de test ale celorlalte 9 limbi, ca `w` |
| **combinatia** | **0.674946** | **+0.010365** | amandoua |

### Cele patru, per limba

| limba | n | ctx | sistem | encmean | picktest | **combinatia** |
|---|---|---|---|---|---|---|
| ca | 445 | 150 | +0.5283 | **+0.5413** | +0.5246 | +0.5411 |
| de | 570 | 193 | +0.7324 | **+0.7357** | +0.7324 | +0.7333 |
| en | 570 | 190 | +0.8663 | **+0.8718** | +0.8635 | +0.8702 |
| es | 593 | 208 | +0.7486 | +0.7589 | +0.7495 | **+0.7606** |
| fil | 570 | 555 | **+0.5171** | +0.5121 | +0.5171 | +0.5121 |
| fr | 569 | 191 | +0.5857 | +0.5863 | +0.6440 | **+0.6450** |
| it | 570 | 192 | +0.6625 | **+0.6651** | +0.6591 | +0.6647 |
| ja | 570 | 190 | +0.7887 | +0.7835 | **+0.7910** | +0.7835 |
| pt | 567 | 562 | +0.8375 | +0.8413 | +0.8374 | **+0.8427** |
| si | 600 | 578 | +0.3786 | **+0.3962** | +0.3786 | +0.3962 |
| **medie** | 5624 | | 0.664581 | 0.669223 | 0.669735 | **0.674946** |

Ingrosat e maximul randului; egalitatile se numara la ambele configuratii. Pe cate limbi e fiecare configuratie cea mai buna: sistemul de dinainte 1, media a trei encodere 5, selectia lui B pe test 2, sistemul ADOPTAT, amandoua 4 din 10.

**Si asta e cifra care incurca.** Combinatia are media cea mai mare, dar nu e cea mai buna pe cele mai multe limbi: media a trei encodere singura o bate pe 4 limbi. Din castigul de +0.0104 pe medie, franceza singura duce +0.0059, adica 57%, dintr-o limba din zece. Restul se imprastie subtire peste celelalte noua. Cifra pe medie e reala, dar nu e uniforma, si asta trebuie citit impreuna cu tabelul de mai jos, nu separat.

### Cele patru comparatii perechi

Aceleasi randuri in toate patru, aliniate pe `idx` peste toate configuratiile deodata. 2000 de reesantionari ale CONTEXTELOR prin `mlsp_common.boot_r_ci`, cu acelasi seed si acelasi vector de contexte. Distributia bootstrap se calculeaza o data per configuratie si perechile se formeaza scazand distributii, deci reesantionarea k inseamna acelasi lucru in toate patru si comparatiile sunt consistente intre ele.

| comparatie | diferenta pe medie | CI 95% pereche | P(>0) |
|---|---|---|---|
| sistemul ADOPTAT, amandoua fata de sistemul de dinainte | +0.010365 | [+0.0060, +0.0146] | 100.0% |
| sistemul ADOPTAT, amandoua fata de media a trei encodere | +0.005724 | [+0.0029, +0.0087] | 100.0% |
| sistemul ADOPTAT, amandoua fata de selectia lui B pe test | +0.005211 | [+0.0017, +0.0084] | 100.0% |
| media a trei encodere fata de selectia lui B pe test | -0.000512 | [-0.0050, +0.0039] | 41.6% |

Detaliul fiecareia, per limba:

**sistemul ADOPTAT, amandoua fata de sistemul de dinainte.** cat valoreaza adoptia totala

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5283 | +0.5411 | +0.0128 | [+0.0037, +0.0217] | 99.8% |
| de | +0.7324 | +0.7333 | +0.0009 | [-0.0061, +0.0081] | 60.1% |
| en | +0.8663 | +0.8702 | +0.0039 | [-0.0001, +0.0083] | 97.2% |
| es | +0.7486 | +0.7606 | +0.0120 | [+0.0061, +0.0176] | 100.0% |
| fil | +0.5171 | +0.5121 | -0.0051 | [-0.0111, +0.0011] | 4.5% |
| fr | +0.5857 | +0.6450 | +0.0593 | [+0.0315, +0.0873] | 100.0% |
| it | +0.6625 | +0.6647 | +0.0021 | [-0.0036, +0.0076] | 76.2% |
| ja | +0.7887 | +0.7835 | -0.0051 | [-0.0137, +0.0037] | 12.9% |
| pt | +0.8375 | +0.8427 | +0.0052 | [+0.0018, +0.0088] | 99.9% |
| si | +0.3786 | +0.3962 | +0.0176 | [-0.0093, +0.0455] | 90.5% |
| **medie** | 0.664581 | **0.674946** | **+0.010365** | **[+0.0060, +0.0146]** | **100.0%** |

**sistemul ADOPTAT, amandoua fata de media a trei encodere.** **mai adauga selectia pe test ceva peste media de encodere?**

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5413 | +0.5411 | -0.0002 | [-0.0054, +0.0054] | 47.2% |
| de | +0.7357 | +0.7333 | -0.0024 | [-0.0034, -0.0014] | 0.0% |
| en | +0.8718 | +0.8702 | -0.0016 | [-0.0033, +0.0000] | 2.7% |
| es | +0.7589 | +0.7606 | +0.0017 | [-0.0010, +0.0042] | 89.0% |
| fil | +0.5121 | +0.5121 | +0.0000 | [+0.0000, +0.0000] | identic |
| fr | +0.5863 | +0.6450 | +0.0588 | [+0.0314, +0.0872] | 100.0% |
| it | +0.6651 | +0.6647 | -0.0004 | [-0.0014, +0.0005] | 17.8% |
| ja | +0.7835 | +0.7835 | +0.0000 | [+0.0000, +0.0000] | identic |
| pt | +0.8413 | +0.8427 | +0.0015 | [-0.0004, +0.0037] | 93.3% |
| si | +0.3962 | +0.3962 | +0.0000 | [+0.0000, +0.0000] | identic |
| **medie** | 0.669223 | **0.674946** | **+0.005724** | **[+0.0029, +0.0087]** | **100.0%** |

**sistemul ADOPTAT, amandoua fata de selectia lui B pe test.** mai adauga media de encodere ceva peste selectia pe test?

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5246 | +0.5411 | +0.0165 | [+0.0071, +0.0255] | 100.0% |
| de | +0.7324 | +0.7333 | +0.0009 | [-0.0061, +0.0081] | 60.1% |
| en | +0.8635 | +0.8702 | +0.0067 | [+0.0024, +0.0112] | 100.0% |
| es | +0.7495 | +0.7606 | +0.0112 | [+0.0054, +0.0166] | 100.0% |
| fil | +0.5171 | +0.5121 | -0.0051 | [-0.0111, +0.0011] | 4.5% |
| fr | +0.6440 | +0.6450 | +0.0011 | [-0.0066, +0.0084] | 62.5% |
| it | +0.6591 | +0.6647 | +0.0055 | [-0.0002, +0.0111] | 97.2% |
| ja | +0.7910 | +0.7835 | -0.0075 | [-0.0155, +0.0010] | 4.2% |
| pt | +0.8374 | +0.8427 | +0.0053 | [+0.0018, +0.0090] | 99.8% |
| si | +0.3786 | +0.3962 | +0.0176 | [-0.0093, +0.0455] | 90.5% |
| **medie** | 0.669735 | **0.674946** | **+0.005211** | **[+0.0017, +0.0084]** | **100.0%** |

**media a trei encodere fata de selectia lui B pe test.** care parghie e mai mare, cu interval pereche

| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |
|---|---|---|---|---|---|
| ca | +0.5246 | +0.5413 | +0.0167 | [+0.0049, +0.0281] | 99.5% |
| de | +0.7324 | +0.7357 | +0.0033 | [-0.0036, +0.0102] | 81.7% |
| en | +0.8635 | +0.8718 | +0.0083 | [+0.0032, +0.0138] | 100.0% |
| es | +0.7495 | +0.7589 | +0.0095 | [+0.0041, +0.0149] | 100.0% |
| fil | +0.5171 | +0.5121 | -0.0051 | [-0.0111, +0.0011] | 4.5% |
| fr | +0.6440 | +0.5863 | -0.0577 | [-0.0884, -0.0272] | 0.0% |
| it | +0.6591 | +0.6651 | +0.0060 | [+0.0004, +0.0115] | 97.9% |
| ja | +0.7910 | +0.7835 | -0.0075 | [-0.0155, +0.0010] | 4.2% |
| pt | +0.8374 | +0.8413 | +0.0039 | [-0.0001, +0.0080] | 97.0% |
| si | +0.3786 | +0.3962 | +0.0176 | [-0.0093, +0.0455] | 90.5% |
| **medie** | 0.669735 | **0.669223** | **-0.000512** | **[-0.0050, +0.0039]** | **41.6%** |

## 2. Verdictul pe complementaritate

Cele doua parghii ating limbi aproape disjuncte, ceea ce sugera complementaritate. Suma naiva a castigurilor lor ar fi +0.009796, adica 0.674377. **Suma naiva nu e o predictie**, fiindca `w` realoca intre brate cand ambele urca: daca A devine mai bun, ponderea lui creste si castigul de pe B se vede mai putin.

Masurat, combinatia da **0.674946**, adica +0.010365 fata de sistem, deci **106% din suma naiva**.

**Se aduna, aproape complet.** Combinatia recupereaza 106% din suma naiva a celor doua castiguri, iar intervalul comparatiei care decide exclude zero: selectia pe test adauga ceva REAL peste media de encodere.

### Descompunerea per limba

| limba | encmean singur | picktest singur | suma naiva | combinatia | recuperat |
|---|---|---|---|---|---|
| ca | +0.0130 | -0.0037 | +0.0094 | **+0.0128** | 137% |
| de | +0.0033 | +0.0000 | +0.0033 | **+0.0009** | 26% |
| en | +0.0055 | -0.0028 | +0.0028 | **+0.0039** | 143% |
| es | +0.0103 | +0.0008 | +0.0111 | **+0.0120** | 108% |
| fil | -0.0051 | +0.0000 | -0.0051 | **-0.0051** | 100% |
| fr | +0.0006 | +0.0583 | +0.0589 | **+0.0593** | 101% |
| it | +0.0026 | -0.0034 | -0.0008 | **+0.0021** | -265% |
| ja | -0.0051 | +0.0024 | -0.0028 | **-0.0051** | 186% |
| pt | +0.0038 | -0.0001 | +0.0036 | **+0.0052** | 143% |
| si | +0.0176 | +0.0000 | +0.0176 | **+0.0176** | 100% |
| **medie** | +0.0046 | +0.0052 | +0.0098 | **+0.0104** | **106%** |

### Franceza, separat, fiindca acolo lucreaza amandoua

Franceza e singura limba unde ambele parghii misca ceva mare: encmean +0.0006, picktest +0.0583, suma naiva +0.0589. Combinatia da **+0.0593**, cu interval [+0.0315, +0.0873] si P(>0) = 100.0%, adica 101% din suma. Acolo suprapunerea era cea mai probabila. **Nu s-a materializat.** Recuperarea pe franceza, 101%, e practic aceeasi cu cea de pe medie, 106%, deci suprapunerea nu e concentrata acolo: e mica si uniforma. Ce se pierde din suma naiva pe franceza, +0.0005, e mecanismul prezis, realocarea lui `w`, si se vede in ponderi: `w` mediu peste cele zece limbi e 0.390 la sistem, urca la 0.430 cand A se face mai bun prin encodere, coboara la 0.375 cand B se face mai bun prin selectie, si iese 0.410 la combinatie, adica intre ele. Cele doua parghii chiar trag ponderea in sensuri opuse, dar nu destul cat sa se anuleze. Restul castigului combinatiei, +0.0044 din medie, vine de pe celelalte noua limbi.

## 3. Costul de inferenta al fiecarei variante

Masurat, nu estimat. Encoderele: `XLMR.embed_frame` peste exact cele 5624 de randuri de test, fara cache, deci se cronometreaza forward-ul, nu discul. LLM-ul: coloana `sec` a rularilor care au produs semnalul B, adica timpul lor real. Cifrele sunt din `output/cost_inferenta.csv`.

| componenta | incarcare | forward pe test | ms per rand | fata de `xlmr` |
|---|---|---|---|---|
| encoder `xlmr` | 5s | 50s = 0.8 min | 8.8 | 1.0x |
| encoder `labse` | 2s | 50s = 0.8 min | 9.0 | 1.0x |
| encoder `e5` | 2s | 50s = 0.8 min | 8.8 | 1.0x |
| encoder `xlmr-large` | 3s | 132s = 2.2 min | 23.4 | 2.7x |
| LLM `gemma4-12b-4bit` | | 102 min pe 5624 randuri | 1091 | 124x |
| LLM `qwen3-8b-4bit` | | 79 min pe 5624 randuri | 839 | 95x |
| LLM `qwen35-9b-8bit` | | 7 min pe 569 randuri | 776 | 9x |

**Ce costa fiecare varianta la inferenta, pe cele 5624 de randuri de test:**

| varianta | encodere | LLM | total conducta | partea de encodere |
|---|---|---|---|---|
| sistemul publicat, un encoder | 0.8 min | 102 min | 103 min | 0.8% |
| selectia lui B pe test | 0.8 min | 102 min | 103 min | 0.8% |
| media a trei encodere | 2.5 min | 102 min | 105 min | 2.4% |
| combinatia, adica sistemul adoptat | 2.5 min | 102 min | 105 min | 2.4% |

**Cele trei lucruri pe care le spun cifrele.** Media de encodere inmulteste partea de encodere cu 3.0, de la 0.8 la 2.5 minute, iar `xlmr-large`, encoderul ramas pe dinafara, ar fi adaugat singur inca 2.7x. Dar LLM-ul ramane dominant: partea de encodere trece de la 0.8% la 2.4% din conducta, deci conducta totala creste cu 2%, nu se dubleaza. **`--pick-split test` costa exact zero in plus**: schimba ce model se alege, nu cate modele se ruleaza, iar ambele candidate erau deja rulate.

Fiindca intervalul comparatiei care decide exclude zero, argumentul de cost nu mai decide singur: cele doua parghii cumpara lucruri diferite, iar intrebarea devine daca +0.005724 merita 1.7 minute in plus per rulare de test.

## 4. Declararea bifurcatiilor, si e o chestiune de integritate

S-au masurat **51 de configuratii de sistem** pe splitul de test, listate in `output/e_rezumat_modele.csv` plus arhiva `output/e_rezumat_modele_pre-p11_n5606.csv`, de dinainte de renumerotare. Fiecare e curata pe dinauntru: limba evaluata e exclusa la fiecare nivel de alegere, la antrenarea bratului A, la alegerea setului de trasaturi, la alegerea modelului lui B, la `w_src` si la `w`. Niciuna nu foloseste vreo eticheta din limba pe care o evalueaza.

**Dar alegerea INTRE ele o facem noi, uitandu-ne la scorul de test.** Asta nu se repara cu inca un nivel de leave-one-language-out, fiindca nu e un nivel de protocol, e o decizie de cercetator: care experiment se raporteaza ca sistem. Se repara declarand-o.

Regula dupa care s-ar alege configuratia raportata, scrisa ca sa fie verificabila:

1. Configuratia raportata e cea cu r mediu maxim pe test dintre cele masurate.
2. O configuratie noua se adopta doar daca intervalul ei PERECHE fata de cea curenta exclude zero. Punctul estimat mai mare nu ajunge.
3. Fiecare configuratie masurata ramane in jurnal, inclusiv cele care au pierdut, si jurnalul se publica.

**Ce propun ca formulare pentru paper**, in Limitations, nu ascuns intr-o nota de subsol:

> Am masurat 51 de configuratii de sistem pe splitul de test, listate integral in materialul suplimentar. Fiecare respecta protocolul leave-one-language-out la toate nivelurile de alegere, deci nicio cifra per limba nu foloseste etichete din limba respectiva. Alegerea configuratiei raportate a fost insa facuta de noi, uitandu-ne la scorul mediu de test, si nu e ea insasi rezultatul unui protocol automat. Cifra raportata trebuie citita ca maximul unei cautari de dimensiunea de mai sus, nu ca un rezultat obtinut la prima incercare. Intervalele de incredere raportate sunt perechi fata de configuratia precedenta si nu sunt corectate pentru comparatii multiple.

E slabiciunea de reviewer cunoscuta deja din etapa cu scorul public, si aceeasi reparatie: se declara, nu se ascunde. Ce ar face-o falsificabila, si nu doar onesta, e M1 din planul de research, adica alegerea intre brate facuta ea insasi leave-one-language-out.

## 5. Pozitionarea fata de repere, fara infrumusetare

Reperele sunt transcrise in `output/repere_publicate.md`, toate pe acelasi test si toate ca medie NEPONDERATA a celor 10 corelatii per limba.

| sistem | etichete in limba tinta | medie |
|---|---|---|
| baseline frecventa | 0 | 0.4780 |
| Archaeology | 0 | 0.4870 |
| TMU-HIT zero-shot, run uniform | 0 | 0.6100 |
| TMU-HIT la Nohejl, mixt | mixt | 0.6540 |
| G-Eval cu GPT-4o | 3-shot | 0.6571 |
| G-Scale cu GPT-4o | 3-shot + T + beta pe 30 | 0.6690 |
| **al nostru, sistemul de dinainte** | **0** | **0.6646** |
| **al nostru, media a trei encodere** | **0** | **0.6692** |
| **al nostru, selectia lui B pe test** | **0** | **0.6697** |
| **al nostru, sistemul ADOPTAT, amandoua** | **0** | **0.6749** |

| configuratie | fata de TMU-HIT zero-shot 0.6100 | fata de G-Eval 0.6571 | fata de G-Scale 0.669 |
|---|---|---|---|
| sistemul de dinainte | +0.0546 | +0.0075 | -0.0044 |
| media a trei encodere | +0.0592 | +0.0121 | +0.0002 |
| selectia lui B pe test | +0.0597 | +0.0126 | +0.0007 |
| sistemul ADOPTAT, amandoua | +0.0649 | +0.0178 | +0.0059 |

**Ce NU se poate spune.** Intervalul mediei noastre pe combinatie e [0.6597, 0.6890], adica lat de 0.0294. Diferenta fata de G-Scale, +0.0059, e cu un ordin de marime sub latimea aia. Orice cifra a noastra intre 0.669 si 0.670 **nu** inseamna ca am trecut de cea mai buna cifra publicata: diferenta e sub rezolutia masuratorii. In plus nu se poate testa statistic, fiindca nu avem predictiile per instanta ale lui Nohejl.

**Si comparatia se scrie in ambele sensuri.** G-Scale foloseste 30 de etichete in limba tinta plus o temperatura aleasa pe trial-urile tuturor celor 10 limbi; noi folosim zero etichete si modele open-weight rulate local. A fi sub el nu e un esec de protocol, si a fi peste el nu e o victorie de protocol. Dar **G-Scale ramane obligatoriu in tabel**, fiindca e cea mai mare cifra publicata si un reviewer din domeniu observa absenta.

**Revendicarea sigura** e fata de singura bara comparabila ca protocol, TMU-HIT zero-shot uniform la 0.6100: sistemul de dinainte +0.0546, media a trei encodere +0.0592, selectia lui B pe test +0.0597, sistemul ADOPTAT, amandoua +0.0649. Comparatia de protocol se castiga detasat in toate cele patru variante, deci propozitia din abstract nu depinde de decizia de adoptare.

## 6. Ce ramane deschis inainte de adoptie

**P10, `qwen35-9b-8bit` pe testul complet.** Modelul e rulat pe test doar pe ca, de, en, es, fil, fr, it, ja, pt, si, 5624 de randuri in 81.4 minute, adica 0.869 s per item in medie si 0.795 s median. Raman **0 de randuri**, deci **0 de minute** la media masurata, 0 la mediana. Cifra de ~75 de minute din `output/e_pick_split.md` e mai mare decat aritmetica propriei ei ipoteze; masurata acum, e ~0. Ce cumpara: bazinul lui `pick_model` pe test trece de la doi candidati efectivi la trei, deci selectia pe test nu mai e restransa de acoperire, si limitarea declarata in raportul lui P1 dispare. **Nu se porneste fara aprobarea lui Alexandru.**

**Fixul de sensibilitate la caz din `find_char_span`**, care recupereaza 18 instante din 5624 si deci schimba `n`. Intra in acelasi eveniment de renumerotare, fiindca schimba toate cifrele per limba.

**M1 si M3 din planul de research**, care nu costa inferenta si care fac adoptia apararabila: M3 e leave-one-encoder-out pe medie, adica raspunde daca `xlmr-large` e necesar sau daca cele trei encodere ieftine duc castigul; M1 e alegerea intre selecteaza si mediaza facuta ea insasi leave-one-language-out, care transforma singura alegere de cercetator ramasa in consecinta de protocol.

## Ce nu s-a facut aici

Nu s-a adoptat nimic. Implicitul lui `--pick-split` ramane `trial` si bratul A implicit ramane `xlmr`, deci sistemul publicat, 0.664581, reproduce bit cu bit fara niciun flag, verificat cu `cmp` pe `fusion_lolo_ens.csv` si `fusion_preds_lolo_ens.csv`. Cifra combinatiei sta pe tagul ei, `ens_encmean_picktest`. Adoptia se face intr-un singur eveniment de renumerotare, dupa ce Alexandru decide.
