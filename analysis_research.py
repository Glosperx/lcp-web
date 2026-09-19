"""Raportul sesiunii de research: ce configuratii mai merita testate, cu cifre.

Referinta e sistemul adoptat, citit din fisier, nu hardcodat. Bara pe care trebuie s-o bata o parghie
noua e **+0.0045**, castigul onest de asteptat pe o limba noua dupa scaderea optimismului de selectie
de +0.001937 masurat peste bazinul de 23 de configuratii. Sub atat nu merita mutata cifra din paper,
fiindca intervalul propriu al lui r pe sistem e deja plus/minus 0.015.

Raportul nu recalculeaza nimic care exista deja intr-un raport propriu: aduna verdictele si le pune
in aceeasi unitate de masura, ca sa se poata compara intre ele. Fiecare directie are aceleasi coloane:
ce s-a masurat, cifra, intervalul PERECHE fata de sistem, cate limbi stricate, costul pana la o cifra
pe test, si daca bate bara.

Rulare:
  python analysis_research.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_research.md")
REF_TAB = os.path.join(OUT, "fusion_lolo_adoptat_temp.csv")
REF_PREDS = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
BARA = 0.0045

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def fuziune(path, langs, Bref):
    """(r mediu, diferenta, lo, hi, P(>0), [limbi stricate]) pentru un fisier de predictii.

    `limbi stricate` sunt cele al caror interval PERECHE fata de sistem exclude zero IN JOS. Coloana
    se citeste inaintea mediei: asa au fost respinse `distTpp`, `prio_KW`, `FM4`, `FM4K` si varianta
    cu configuratia aleasa LOLO, toate cu media mai mare decat a sistemului.
    """
    import analysis_dist as ad
    from analysis_fewshot import boots_of
    Bk, rk = boots_of(path, langs)
    dm, lo, hi, pp = ad.mean_diff_ci(Bk, Bref)
    rele = []
    for i, lg in enumerate(langs):
        m = min(len(Bk[i]), len(Bref[i]))
        dv = Bk[i][:m] - Bref[i][:m]
        if float(np.percentile(dv, 97.5)) < 0:
            rele.append(lg)
    return float(rk.mean()), dm, lo, hi, pp, rele, Bk


def main():
    from analysis_fewshot import boots_of
    ref = pd.read_csv(REF_TAB)
    sis = float(ref["r_fuz_raw"].mean())
    b_sis = float(ref["r_B_raw"].mean())
    langs = sorted(pd.read_csv(REF_PREDS)["lang"].unique())
    Bref, _ = boots_of(REF_PREDS, langs)

    emit("# Sesiunea de research: ce mai merita testat, cu cifre\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_research.py`. Referinta e "
         f"sistemul adoptat, **r = {sis:.6f}** pe {int(ref['n'].sum())} de randuri, cu "
         f"B = {b_sis:.6f}, citita din `output/fusion_lolo_adoptat_temp.csv`.\n",
         __doc__.split("Rulare:")[0].split("\n", 2)[2].strip() + "\n",
         "**Directia care putea muta cifra cu mai mult de 0.005 a fost scoasa din domeniu.** Un model "
         "mai mare ca B a fost respins ca solutie ne-inginereasca. Costul lui a fost totusi verificat "
         "si e mai jos, fiindca era cerut. Cu ea afara, niciuna dintre parghiile ramase nu putea, "
         "inainte de a fi masurata, sa treaca bara cu mult, si asta se citeste in rezultate.\n")

    RANDURI = []

    # ---------------------------------------------------------------- 1. prompturi decorelate
    emit("## 1. Prompturi structural decorelate\n",
         "Raport propriu: `output/e_frontiera.md`. Cinci candidati pe trial, ~16 minute de inferenta "
         "in total, o singura incarcare de model. Cernerea e pe doua porti scrise inainte de a vedea "
         "vreo cifra, si **calibrate pe cei patru membri cu rezultat cunoscut pe test**: poarta trece "
         "`few-shot` (+0.005247 pe B pe test) si cade pe `rubrica` si `learner` (+0.000857 si "
         "+0.000286), deci separa, chiar daca il pierde si pe `marcat`. E o poarta cu recall mic, nu "
         "una stricata, si asta se declara.\n",
         "Ce s-a masurat pe trial, in ordinea decorelarii:\n",
         "| candidat | ce schimba | r3 | rho3 | ansamblu pe trial | fata de pereche | porti |",
         "|---|---|---|---|---|---|---|",
         "| `frecventa` | alt construct: cat de comun, nu cat de dificil | +0.641 | **0.770** | "
         "+0.713418 | **+0.012996** | **trece** |",
         "| `fara context` | tinta singura, fara propozitie | +0.643 | 0.825 | +0.701538 | -0.001037 "
         "| cade |",
         "| `lema` | lema in loc de forma flexionata | +0.663 | 0.869 | +0.700942 | -0.000377 | cade |",
         "| `binar x3` | citire binara la trei praguri | +0.521 | 0.722 | +0.667746 | -0.030719 | cade |",
         "| `proportie` | cati cititori din cinci, nu ce nota | +0.520 | 0.733 | +0.681556 | -0.019157 "
         "| cade |\n",
         "Perechea de acum, sub acelasi protocol: +0.701251. Cel mai decorelat prompt de dinainte avea "
         "rho3 = 0.845, deci trei dintre candidati chiar au coborat decorelarea sub tot ce se masurase, "
         "confirmand ca parghia exista. Dar numai unul a facut-o pastrand r3 peste prag.\n",
         "### Trei predictii declarate inainte de rulare, si ce s-a intamplat\n",
         "1. **`lema` va fi cel mai putin decorelat.** CONFIRMAT: rho3 = 0.869, cel mai mare din cinci. "
         "Motivul scris dinainte era ca `fil` si `si` n-au lema deloc, deci pe doua limbi din zece "
         "intrebarea e despre acelasi sir, iar pe restul lema difera de forma pe 37-67% din randuri.\n",
         "2. **`fara context` va cadea pe sinhaleza.** CONFIRMAT, si prin alt mecanism decat cel "
         "prezis. Prezicerea era despre legaturi: pe test sinhaleza are 214 tinte distincte din 600 de "
         "randuri, deci 64% legaturi, iar legaturile plafoneaza Pearson. Dar pe TRIAL, unde sunt 299 de "
         "tinte distincte din 300 si deci zero legaturi, `fara context` da pe sinhaleza r3 solo "
         "**+0.050**, adica practic nimic, si scade ansamblul cu -0.056, cel mai rau din toate limbile. "
         "Deci intrebarea in sine nu functioneaza pe sinhaleza fara context; legaturile ar fi venit "
         "peste asta. Predictia s-a adeverit, motivul scris era doar unul din doua.\n",
         "3. **`frecventa` e cel mai promitator pe hartie**, fiindca frecventa e cel mai bun corelat "
         "cunoscut al complexitatii lexicale si e o intrebare complet alta. CONFIRMAT, si cu un tipar "
         "care nu era prezis: **singura limba pe care o urca mult e chiar sinhaleza, +0.073**, cel mai "
         "mare castig pe o limba dintre toti candidatii. r3 solo pe sinhaleza e +0.456, fata de +0.050 "
         "la `fara context`, +0.095 la `binar`, +0.132 la `lema` si +0.161 la `proportie`. Sinhaleza e "
         "limba cea mai slaba a sistemului, cu fuziunea la +0.4251. Citirea mecanica: pe o limba cu "
         "resurse putine modelul nu poate nota dificultatea, dar poate inca spune cat de comun e "
         "cuvantul.\n",
         "### De ce cad ceilalti, mecanic\n",
         "`binar x3` are cel mai mic rho3 fata de pereche, 0.722, dar corelatia INTRE cele trei praguri "
         "e 0.883: sunt trei copii aproape identice, deci trei membri costa trei inferente si aduc cat "
         "unul, iar r3-ul lor individual e prea mic. `proportie` are rho3 = 0.733 si cade tot pe r3, "
         "+0.520. Amandoua confirma exact ce spune frontiera: decorelarea singura nu ajunge, si nici "
         "calitatea singura.\n")

    # rezultatul pe test, daca exista
    fr = {}
    for pre, kd in (("FR3", "nu"), ("FR3K", "da")):
        p = os.path.join(OUT, f"fusion_preds_lolo_frecventa_{pre}.csv")
        if os.path.exists(p):
            fr[pre] = fuziune(p, langs, Bref) + (kd,)
    if fr:
        emit("### Rezultatul pe test: cade\n",
             "**`frecventa` pierde pe test, desi trecuse amandoua portile pe trial.** E a patra "
             "rasturnare trial-test din acelasi fir, dupa few-shot singur, dupa ordinea celor patru "
             "membri, si dupa `marcat`.\n",
             "Si e cazul cel mai informativ dintre toate, fiindca **amandoua ipotezele portii au tinut "
             "pe medie**:\n",
             "- `r3` a coborat de la +0.641 pe trial la **+0.583** pe test, adica -0.058, bine in "
             "interiorul podelei de -0.097 pe care o presupunea poarta; pragul cerut era +0.544;\n",
             "- `rho3` a urcat de la 0.770 la **0.798**, adica +0.028, sub plafonul de +0.036; pragul "
             "cerut era 0.806.\n",
             "Deci nu ipotezele s-au dovedit gresite, ci marimea pe care erau puse.\n",
             "### De ce a cazut: transferul se masoara pe limba, nu pe medie\n",
             "Cifra din fisa de metoda, `rho3` transfera trial-test cu +0.997 iar `r3` cu +0.726, e "
             "corelatia peste PROMPTURI a mediilor pe limbi. Recalculata acum pe cinci membri, ea se "
             "confirma: pe medii, `rho3` da +0.980 si `r3` +0.519. Dar fiecare hiperparametru din "
             "conducta se alege LEAVE-ONE-LANGUAGE-OUT, deci ce guverneaza e transferul PE LIMBA, si "
             "acolo ordinea se inverseaza:\n",
             "| marime | corelatie peste medii, 5 membri | corelatie pe limba, 5 x 10 = 50 puncte |",
             "|---|---|---|",
             "| `rho3`, decorelarea | **+0.980** | **+0.643** |",
             "| `r3`, calitatea | +0.519 | **+0.791** |",
             "",
             "Per membru, corelatia pe limba a lui `rho3` e intre +0.125 si +0.524, adica aproape "
             "nimic. Deplasarea per limba a lui `rho3` are media +0.017 dar abaterea 0.051 si "
             "intervalul [-0.087, +0.143]; a lui `r3` are media -0.042, abaterea 0.098 si intervalul "
             "[-0.196, +0.261]. Media ascunde deci exact ce conteaza.\n",
             "**Si se vede pe limba care purta tot castigul.** Pe sinhaleza, `frecventa` avea pe trial "
             "`r3` = +0.478 si `rho3` = 0.655, cele mai bune valori ale ei; pe test are `r3` = +0.310 "
             "si `rho3` = 0.763. Amandoua s-au mutat in sensul rau in acelasi timp, si sunt cele mai "
             "mari deplasari din tot tabelul, -0.169 si +0.108.\n",
             "### Un castig pe B nu inseamna un castig pe fuziune\n",
             "`FR3` **urca** semnalul B cu +0.001217, de la 0.659202 la 0.660418, si totusi coboara "
             "fuziunea cu -0.002386. Dilutia e **-1.96**, adica semnul se inverseaza. Cele trei "
             "configuratii masurate pana acum cap la cap aveau dilutia intre +0.55 si +0.82, si de "
             "acolo venea obiceiul de a extrapola un castig pe B intr-unul pe fuziune. **Obiceiul e "
             "gresit**: cand castigul pe B cade pe limbi unde A duce oricum greutatea, iar pierderile "
             "cad unde B conteaza, fuziunea merge in sens contrar.\n",
             "### Cifrele\n",
             "`limbi stricate` se citeste PRIMA. `FR3` e ansamblul de trei prompturi, `FR3K` e acelasi "
             "plus unirea cifrelor vecine, adica exact perechea de configuratii prin care au trecut si "
             "`FS3`/`FS3K`.\n",
             "| configuratie | colaps | limbi stricate | r mediu | fata de sistem | CI 95% pereche | "
             "P(>0) | bate +0.0045 |", "|---|---|---|---|---|---|---|---|")
        for pre in ("FR3", "FR3K"):
            if pre not in fr:
                continue
            r, dm, lo, hi, pp, rele, _ = fr[pre][:7]
            kd = fr[pre][7]
            bate = "**DA**" if (lo > 0 and not rele and dm >= BARA) else "nu"
            emit(f"| `{pre}` | {kd} | {', '.join(rele) if rele else '**niciuna**'} | **{r:.6f}** | "
                 f"{dm:+.6f} | [{lo:+.6f}, {hi:+.6f}] | {pp:.1%} | {bate} |")
            RANDURI.append((f"prompturi decorelate, `{pre}`", "masurat pe test", f"{dm:+.6f}",
                            f"[{lo:+.6f}, {hi:+.6f}]", str(len(rele)),
                            "0, e rulata", bate))
        emit("")
        # per limba
        emit("Per limba, fata de sistem:\n", "| configuratie | " + " | ".join(langs) + " |",
             "|---|" + "---|" * len(langs))
        for pre in ("FR3", "FR3K"):
            if pre not in fr:
                continue
            Bk = fr[pre][6]
            row = []
            for i, lg in enumerate(langs):
                m = min(len(Bk[i]), len(Bref[i]))
                row.append(float(np.mean(Bk[i][:m] - Bref[i][:m])))
            emit(f"| `{pre}` | " + " | ".join(f"{x:+.4f}" for x in row) + " |")
        emit("")
    else:
        emit("### Rezultatul pe test\n", "Inca nerulat.\n")
        RANDURI.append(("prompturi decorelate, `frecventa`", "cernut pe trial", "trece portile",
                        "", "-", "~38 min pe test", "de vazut"))

    # ---------------------------------------------------------------- 2. calibrare monotona
    emit("## 2. Calibrare monotona a lui B\n",
         "Raport propriu: `output/e_calibrare.md`. Zero inferenta. Cu cinci atomi familia monotona are "
         "exact trei parametri liberi, deci o spline cu 3-4 noduri n-are unde sa adauge ceva peste o "
         "grila pe simplexul cresterilor, iar grila are avantajul ca numarul de candidati se declara.\n",
         "Coloana care decide e **podeaua de zgomot**: acelasi numar de candidati, dar generati "
         "aleator, trecuti prin selectia LOLO identica, cu 10 seminte.\n",
         "| familie | candidati | castig pe B | podea de zgomot | exces | pe fuziune, la dilutia "
         "0.55-0.82 |", "|---|---|---|---|---|---|")
    CAL = [("colaps, 15 trepte", 15, +0.002044, +0.000563),
           ("grila 1/4", 35, -0.001979, +0.001162),
           ("grila 1/8", 165, +0.002309, +0.001587),
           ("grila 1/12", 455, +0.000339, +0.001568)]
    for nume, n, d_, pod in CAL:
        ex = d_ - pod
        emit(f"| {nume} | {n} | {d_:+.6f} | {pod:+.6f} | **{ex:+.6f}** | "
             f"{ex*0.55:+.6f} .. {ex*0.82:+.6f} |")
    best = max(CAL, key=lambda x: x[2] - x[3])
    ex = best[2] - best[3]
    emit("",
         f"Cel mai mare exces peste podea il da tot **{best[0]}**, cu {ex:+.6f}. Coloana de "
         "extrapolare la fuziune de mai sus se citeste cu rezerva, fiindca sesiunea asta a masurat o "
         "dilutie NEGATIVA la `FR3`, -1.96: un castig pe B poate cobori fuziunea. Pentru familia de "
         "colaps insa nu e nevoie de extrapolare, fiindca a fost masurata cap la cap ca `prio_K` si a "
         "dat +0.001682 pe fuziune, tot sub bara. Grila de 165 are castigul brut cel mai mare, "
         "+0.002309, dar si podeaua cea mai mare, +0.001587, deci excesul ei e mai MIC decat al celor "
         "15 trepte. Podeaua creste cu marimea bazinului, exact cum trebuie.\n",
         "**Doua lucruri de retinut dincolo de verdict.** Intai, familia monotona generala, cu pana la "
         "455 de candidati, nu scoate mai mult decat cele 15 trepte: spatierea nivelurilor nu mai are "
         "ce da, si `prio_K` era deja optimul practic al axei. Apoi, si asta e de scris in paper: "
         "castigul lui `prio_K` insusi, +0.002044 pe B, e doar **+0.001480 peste podeaua de zgomot a "
         "unui bazin de 15 candidati**, adica peste un sfert din el e noroc de selectie.\n")
    RANDURI.append(("calibrare monotona a lui B", "masurat, LOLO, cu podea de zgomot",
                    f"{ex:+.6f} pe B", "exces peste podea", "0",
                    "0, zero inferenta", "**nu**"))

    # ---------------------------------------------------------------- 4. pondere per item
    emit("## 3. Ponderare per item in fuziune\n",
         "Zero inferenta. `w_i = clip(w + a*h_i, 0, 1)`, cu `a` ales LOLO impreuna cu `w` pe o grila de "
         "7x21 = 147 de perechi care CONTINE `a = 0`, deci sistemul de acum e in grila. Controlul de "
         "reproducere a trecut: cu grila lui `a` redusa la zero, `p_fuz` iese identic la 0.0 fata de "
         "`output/fusion_preds_lolo_adoptat_temp.csv` si r pana la a zecea zecimala.\n",
         "| h | ce e | r mediu | fata de sistem | `a` ales |", "|---|---|---|---|---|")
    W = [("entropie", "entropia distributiei lui B la T ales LOLO"),
         ("dezacord", "divergenta JS intre cele doua prompturi")] + \
        [(f"zgomot{s}", f"coloana aleatoare, samanta {s}") for s in range(5)]
    for tag, ce in W:
        p = os.path.join(OUT, f"fusion_lolo_witem_{tag}.csv")
        if not os.path.exists(p):
            continue
        t = pd.read_csv(p)
        r = float(t["r_fuz_raw"].mean())
        emit(f"| `{tag}` | {ce} | {r:.6f} | {r - sis:+.6f} | "
             f"{'zero pe toate zece' if (t['a'].abs() < 1e-12).all() else list(t['a'])} |")
    emit("",
         "**Selectia alege `a = 0` pe toate zece limbile, si la semnal real si la zgomot pur.** Nu e o "
         "cifra mica, e zero exact: procedura imbricata, cu punctul neutru in grila, nu urmareste "
         "zgomotul. Podeaua de zgomot a acestei parghii e chiar 0.000000, pe cinci seminte.\n",
         "**Un efect secundar care merita scris, fiindca e general.** `dezacord` iese la -0.000331 "
         "desi `a = 0` peste tot. Pierderea nu vine din parghie, vine din faptul ca grila largita "
         "schimba criteriul de la nivelul al doilea al selectiei: acolo argmaxul peste matricea (a, w) "
         "al unei limbi de potrivire poate cadea pe `a` nenul, ceea ce muta `w_src` ales pentru limba "
         "tinuta deoparte. Pe sinhaleza `w_src` sare de la 0.750 la 0.250 si limba pierde -0.0031. "
         "Deci **un grad de libertate in plus poate strica si atunci cand ajunge sa nu fie folosit**, "
         "prin criteriul imbricat, nu prin parametrul insusi.\n")
    RANDURI.append(("pondere per item in fuziune", "masurat, LOLO, cu podea de zgomot",
                    "+0.000000", "a = 0 ales pe 10/10", "0 la entropie, 1 la dezacord",
                    "0, zero inferenta", "**nu**"))

    # ---------------------------------------------------------------- 3. model mai mare
    emit("## 4. Un model mai mare ca B: evaluat si declinat\n",
         "Respinsa ca solutie ne-inginereasca. Costul a fost verificat oricum, ca sa fie scris odata "
         "si sa nu se redeschida din memorie. Pe 24 GB de memorie unificata, cu limita implicita "
         "`iogpu.wired_limit_mb` la ~18 GB, exista trei candidate reale in mlx-community:\n",
         "| model | greutati | model_type | incape la limita implicita | cost estimat pe test |",
         "|---|---|---|---|---|",
         "| `gemma-3-text-27b-it-4bit` | 15.99 GB | gemma3, fara remap | da | ~4 h |",
         "| `Qwen3.5-27B-4bit` | 15.97 GB | qwen3 | da | ~4 h |",
         "| `gemma-4-31b-it-4bit` | 18.41 GB | gemma4, fara remap | **nu**, cere sysctl | ~5 h |",
         "",
         "`gemma-4-31B-it-qat-OptiQ-4bit` exista si el, dar are 22.4 GB de greutati plus un turn de "
         "viziune de 1.15 GB, deci nu intra deloc. De notat ca varianta simpla `gemma-4-31b-it-4bit` "
         "declara `model_type: gemma4` direct, deci NU are nevoie de remaparea `model_config` de care "
         "are nevoie checkpoint-ul de 12B din pool, care declara `gemma4_unified`.\n")
    RANDURI.append(("model mai mare ca B", "declinat, cost verificat", "-", "", "-",
                    "4-5 h pe test plus descarcare", "scos din domeniu"))

    # ---------------------------------------------------------------- 5. cuantizare 8 biti
    emit("## 5. Cuantizare 8 biti pentru Gemma: BLOCATA de disponibilitate\n",
         "Control de confound, nu parghie: raspunde daca cuantizarea de 4 biti costa ceva, nu propune "
         "un castig. **Nu se poate rula asa cum e conducta acum**, si motivul e concret.\n",
         "Modelul lui B din sistem e `mlx-community/gemma-4-12B-it-qat-OptiQ-4bit`, si e o "
         "reimpachetare NUMAI TEXT: are doua shard-uri si niciun `processor_config.json`. Toate "
         "celelalte variante Gemma 4 12B din mlx-community sunt multimodale, cu tensorii de viziune "
         "inline:\n",
         "| repo | 8 biti | numai text | se incarca sub mlx_lm 0.31.3 |", "|---|---|---|---|",
         "| `gemma-4-12B-it-qat-OptiQ-4bit` | nu | **da** | da, cu remaparea `model_config` |",
         "| `gemma-4-12B-it-qat-8bit` | da | nu | **nu** |",
         "| `gemma-4-12B-it-8bit` | da | nu | nu |",
         "| `gemma-4-12B-it-4bit` | nu | nu | nu |",
         "",
         "OptiQ exista numai la 4 biti, verificat pe API: cautarea dupa `gemma-4-12B-it-OptiQ` "
         "intoarce doua repo-uri, amandoua 4bit. Deci **analogul exact de 8 biti al checkpoint-ului "
         "sistemului nu exista**.\n",
         "S-a descarcat totusi `gemma-4-12B-it-qat-8bit`, 12.72 GB, si incarcarea pica zgomotos cu "
         "`Received 11 parameters not in model: vision_embedder.*`, fiindca `load_weights` e strict "
         "iar turnul de text al lui mlx_lm nu are unde pune tensorii de viziune. O intrare de pool cu "
         "`model_config={\"model_type\": \"gemma4\"}` e necesara si insuficienta; e in cod, cu "
         "comentariul care spune ca prima presupunere, ca n-ar avea nevoie de remapare, era gresita.\n",
         "Doua cai mai departe, si amandoua ating calea prin care trece fiecare cifra publicata, deci "
         "nu se aleg fara aprobare:\n",
         "1. filtrarea explicita a celor 11 tensori `vision_embedder.*` la incarcare, cu verificarea "
         "ca nimic altceva nu se pierde si cu D.4 ca plasa de siguranta. E corecta ca substanta, "
         "fiindca turnul de text e complet si cel de viziune e nefolosit, dar e chirurgie pe "
         "`solution_bert`;\n",
         "2. urcarea lui mlx_lm peste 0.31.3, ceea ce schimba mediul in care s-au produs toate "
         "cifrele de pana acum.\n")
    RANDURI.append(("cuantizare 8 biti", "blocata de disponibilitate", "-", "", "-",
                    "descarcat, dar nu se incarca", "control, nu parghie"))

    # ---------------------------------------------------------------- multiplicitate
    emit("## Multiplicitatea, declarata\n",
         "Pe aceleasi 5624 de randuri de test, sesiunea asta a adaugat **sapte configuratii "
         "candidate** si **treisprezece controale**. Niciuna nu s-a adoptat, si toate raman in "
         "jurnal, inclusiv cele care au pierdut.\n",
         "Candidate: `FR3` si `FR3K` pe fuziune; `witem entropie` si `witem dezacord` pe fuziune; "
         "grilele monotone la pas 1/4, 1/8 si 1/12 pe semnalul B.\n",
         "Controale: reproducerea de octet a lui `bakeoff_test_Text`; `--mod calibrare --pas 0` fata "
         "de `--mod colaps`; `witem` cu grila lui `a` redusa la zero; cinci seminte de zgomot pentru "
         "ponderea per item; si cate zece bazine aleatoare pentru fiecare dintre cele patru familii "
         "de calibrare, care nu produc configuratii de sistem ci podeaua lor de zgomot.\n",
         "Inainte de sesiune erau 23 de configuratii de semnal B numarate in "
         "[[optimismul-de-selectie-masurat]] si 51 de configuratii de sistem in "
         "`output/e_adoptie.md` §4. **Cifra care se citeaza in paper se recalculeaza din "
         "`output/e_rezumat_modele.csv` cu `make_rezumat_modele.py`, nu se copiaza de aici**: "
         "`analysis_audit_jurnal.py` a fost rulat dupa toate configuratiile de mai sus si iese curat, "
         "cu 115 cifre pe n curent si 102 randuri in jurnal, zero lipsa.\n",
         "**Si un lucru care se aplica la tot ce e mai sus.** Nicio configuratie noua din sesiunea "
         "asta nu trece bara, deci maximul peste bazin nu s-a mutat si optimismul de selectie de "
         "+0.001937 ramane cifra buna. Ce s-a schimbat e ca bazinul e mai mare, deci daca in viitor "
         "ceva TREBE bara, optimismul lui va trebui recalculat pe bazinul nou.\n")

    # ---------------------------------------------------------------- corectii
    emit("## 6. Doua corectii la rapoarte existente\n",
         "Amandoua au iesit din munca de sesiunea asta si niciuna nu s-a aplicat: se raporteaza si "
         "se intreaba.\n",
         "### 6.1. `output/e_al3lea.md` se contrazice cu propriul tabel\n",
         "Verdictul lui, generat automat, spune **castigul e specific few-shot-ului**. Se sprijina pe "
         "un prag de 80% aplicat castigului pe semnalul B: `marcat` aduce +0.004146 fata de +0.005247 "
         "al lui `few-shot`, adica **79.0%**, deci cade sub prag cu un punct procentual. La un prag de "
         "78% verdictul s-ar fi inversat.\n",
         "Iar la nivelul FUZIUNII, care e cifra care ajunge in paper, `marcat` **castiga**: `M3K` "
         "0.690001 fata de `FS3K` 0.688506. Deci raportul afirma in proza contrariul a ce arata "
         "tabelul lui de mai sus. Formularea care supravietuieste amandurora e cea din fisa de "
         "memorie: cele doua nu se disting (+0.001510 [-0.001142, +0.004239]), iar revendicarea fata "
         "de G-Eval nu se poate scrie. Verdictul din `e_al3lea.md` nu trebuie citat asa cum e.\n",
         "**Si sesiunea asta adauga un al doilea argument in aceeasi directie.** `frecventa` nu "
         "foloseste nicio eticheta, ca si `marcat`. Daca trece pe test, va fi al doilea prompt "
         "zero-label care aduce cat aduce few-shot-ul, deci ipoteza ca exemplele etichetate aduc ceva "
         "propriu slabeste inca o data.\n",
         "### 6.2. Frontiera nu e o aproximare, e o identitate\n",
         "`r_ens = (suma r_i)/sqrt(n + 2*suma rho_ij)` reproduce media STANDARDIZATA a membrilor la "
         "**3.3e-16**, adica exact. Ce s-a numit pana acum eroarea ei, 0.0003..0.0024 in "
         "`output/e_al3lea.md` si -0.000142 pe ansamblul de patru, e de fapt distanta dintre media "
         "standardizata si media BRUTA pe care o calculeaza `make_fs_runs.b_of`, si ea creste cu cat "
         "membrii au deviatii standard mai diferite. La `binar x3`, cu membrii la 0.57 din deviatia "
         "perechii, distanta ajunge la 0.025.\n",
         "Conteaza pentru ce se scrie: propozitia corecta nu e `formula prezice ansamblul cu eroare "
         "sub 0.001`, ci `agregarea e reducere de varianta si nimic altceva, iar aritmetica ei e "
         "exacta`. A doua e mai tare si e adevarata. Prima invita intrebarea de unde vine eroarea, "
         "care are un raspuns prozaic si care nu e despre prompturi.\n")

    # ---------------------------------------------------------------- tabelul cerut
    emit("## Tabelul cerut\n",
         f"`bate +{BARA:.4f}` e coloana care decide daca merita mutata cifra din paper. Bara e "
         "castigul onest de asteptat pe o limba noua, adica maximul observat minus optimismul de "
         "selectie de +0.001937.\n",
         "| directie | tip de dovada | delta | interval | limbi stricate | cost pana la o cifra pe "
         f"test | bate +{BARA:.4f} |", "|---|---|---|---|---|---|---|")
    for row in RANDURI:
        emit("| " + " | ".join(row) + " |")
    emit("")
    print(f"[res] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
