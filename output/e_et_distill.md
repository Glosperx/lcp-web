# §1.5 Poarta de distilare a privirii. Adauga embeddingul ceva la prezicerea privirii?

Generat 2026-08-18 13:22:08 de `analysis_et_distill.py`, 101 secunde. Nicio descarcare.

## Ce se masoara, si de ce cifra asta decide

Verdictul V4 respinge privirea ca TRASATURA. Unghiul pe care nu l-a considerat e privirea ca TINTA DE TRANSFER: se distileaza un predictor de privire peste embeddingul XLM-R inghetat pe romana, apoi se aplica pe tintele MLSP in toate cele 10 limbi. Ar ocoli complet problema de acoperire, fiindca nu cere gaze in nicio limba tinta.

Poarta e urmatoarea. Daca embeddingul nu adauga nimic peste lungime si frecventa **cand tinta e privirea**, atunci un predictor de privire construit peste el nu poate purta nimic ce semnalul A nu poarta deja, fiindca lungimea si frecventa sunt amandoua in A. Calea moare inainte sa inceapa, si moare cu o masuratoare a noastra, nu cu o citare.

## Protocolul

- **Randuri:** 1509 tinte romanesti cu privire, din `data/X_test.csv`, 10 texte, 263 contexte. Aceleasi randuri pe toate bratele.

- **Tinta:** `TFT_mean_norm`, timpul total de fixare per token, mediat peste 95 de participanti. Doua tinte de control mai jos.

- **Bratele:** `lex` = 2 coloane, lungime in caractere si `zipf_best`. `lex+emb` = aceleasi 2 plus embeddingul XLM-R contextual, 770 coloane. `emb` = numai embeddingul.

- **Regresorul:** `solution_bert.blend_ridge_hgb`, neschimbat, adica exact regresorul semnalului A. Nu se acordeaza nimic pe tinta asta.

- **Split pe TEXTE**, leave-one-text-out, un fold per text. Predictiile raportate sunt out-of-fold, iar r se ia pe ele adunate, nu ca medie de folduri.

- **Intervale:** bootstrap pe CONTEXTE, propozitii, 2000 de reesantionari. Diferenta e PERECHE, aceeasi reesantionare pe ambele brate, deci intervalul e al diferentei.

## Provenienta tintei. Chiar e TRT?

`TFT_mean_norm` vine gata agregat in `data/X_test.csv`, si codul care l-a scris nu mai e in repo. Deci se reagrega independent din sursa bruta, `data/train_et.csv`, 95 de participanti pe 10 texte: media lui `TFT` per pereche (text, cuvant).

| reagregare | r cu `TFT_mean_norm` | n |
|---|---|---|
| media lui TFT peste toti participantii | **+0.9869** | 1336 |
| media lui TFT numai peste fixarile reale | **+0.9933** | 1336 |

Deci tinta e TRT. Nu iese exact 1.000 din doua motive care nu se pot elimina din datele de pe disc: `data/X_test.csv` nu pastreaza `word_idx`, deci reagregarea trebuie sa lege pe (text, cuvant), iar un cuvant care apare de mai multe ori in acelasi text primeste media peste toate pozitiile lui; si potrivirea pe sir reuseste pe 1336 din 1509 randuri, restul fiind tokeni cu punctuatie lipita.

## Rezultatul

| tinta de privire | r `lex` | r `lex+emb` | **increment** | CI 95% pereche | P(>0) | r `emb` singur |
|---|---|---|---|---|---|---|
| **`TFT_mean_norm`** | +0.6262 | +0.6222 | **-0.0040** | [-0.0303, +0.0226] | 39.4% | +0.5167 |
| `FFD_mean_norm` | +0.4429 | +0.4558 | +0.0129 | [-0.0191, +0.0469] | 77.7% | +0.4073 |
| `et_complexity_proxy` | +0.6147 | +0.6227 | +0.0081 | [-0.0185, +0.0354] | 70.2% | +0.5292 |

Randul de sus e cel care decide. Pe TRT, cele doua coloane lexicale singure dau **+0.6262**. Cu 768 de dimensiuni de embedding pe langa ele se ajunge la **+0.6222**, adica un increment de **-0.0040**, cu intervalul pereche [-0.0303, +0.0226] si P(>0) = 39.4%.

| brat | r out-of-fold pe TRT |
|---|---|
| lungime + frecventa, 2 coloane | +0.6262 |
| embedding singur, 768 coloane | +0.5167 |
| amandoua, 770 coloane | +0.6222 |

## Pe folduri, ca sa se vada ca increment mediu nu ascunde un text unde embeddingul salveaza ceva

| text | n | r `lex` | r `lex+emb` | diferenta |
|---|---|---|---|---|
| `Arg_PISACowsMilk` | 239 | +0.6464 | +0.6292 | -0.0172 |
| `Arg_PISARapaNui` | 197 | +0.5123 | +0.4521 | -0.0603 |
| `Ins_HumanRights` | 9 | +0.8894 | +0.8036 | -0.0857 |
| `Ins_LearningMobility` | 152 | +0.6546 | +0.5545 | -0.1001 |
| `Lit_Alchemist` | 118 | +0.5431 | +0.5623 | +0.0192 |
| `Lit_BrokenApril` | 124 | +0.7189 | +0.7434 | +0.0245 |
| `Lit_MagicMountain` | 88 | +0.8283 | +0.7056 | -0.1227 |
| `Lit_Solaris` | 225 | +0.7454 | +0.7278 | -0.0176 |
| `PopSci_Caveman` | 109 | +0.7263 | +0.7091 | -0.0172 |
| `PopSci_MultiplEYE` | 248 | +0.6757 | +0.6865 | +0.0108 |

## Verdictul

**Calea moare aici.** Incrementul e -0.0040 in r si intervalul pereche [-0.0303, +0.0226] include zero, deci nu se poate distinge de zgomot. Cele 768 de dimensiuni ale encoderului nu adauga nimic masurabil peste doua coloane, lungime si frecventa, cand tinta e privirea.

Ce sprijina verdictul, dincolo de cifra de sus:

1. **Embeddingul singur prezice privirea mai prost decat doua coloane lexicale**, +0.5167 fata de +0.6262. Nu e o problema de capacitate a regresorului, e ca privirea e, in prima aproximatie, o functie de lungime si frecventa. E acelasi lucru pe care il spune si rezultatul subtaskului multilingv de la CMCL 2022, castigat de o regresie pe trasaturi lexicale, doar ca aici e masurat pe datele noastre.
1. **Aceeasi concluzie pe `FFD_mean_norm`**, FFD, prima fixare, control de metrica timpurie: increment +0.0129, [-0.0191, +0.0469]. Verdictul nu depinde de care metrica de privire se ia ca tinta.
1. **Aceeasi concluzie pe `et_complexity_proxy`**, compozitul ET al proiectului, 8 metrici ponderate: increment +0.0081, [-0.0185, +0.0354]. Verdictul nu depinde de care metrica de privire se ia ca tinta.

Consecinta pentru lucrare: semnalul de privire se inchide cu **doua** masuratori proprii, nu cu o citare. Prima, din §1.1, spune ca privirea REALA, cu gaze peste exact textele din care vin tintele si acoperire de 95.1%, a adus +0.0067 in r pe romana. A doua, asta, spune ca puntea care ar fi dus privirea in celelalte 9 limbi nu exista: ce s-ar putea distila din embedding despre privire e deja in semnalul A, sub forma de lungime si frecventa.
