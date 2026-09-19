"""E.16. Prompturi structural decorelate, cernute pe trial cu frontiera.

De ce directia asta si nu alta. Castigul unui al treilea prompt e EXACT formula de reducere a
variantei, `r_ens = (suma r_i)/sqrt(n + 2*suma_{i<j} rho_ij)`, verificata pe test cu eroare -0.000142
pe un ansamblu de patru prezis inainte de a fi construit. In formula, singura parghie care se poate
misca mult e `rho`: cele patru prompturi incercate pana acum stau toate intre 0.845 si 0.903, iar un
prompt cu r3 = +0.50, mult mai slab decat oricare dintre ele, bate perechea daca rho3 < 0.62. Deci
ce trebuie schimbat e CE conditioneaza modelul, nu cat de bine e formulata intrebarea.

**Capcana de masurare, si a fost verificata inainte de a scrie codul asta.** `analysis_al3lea.corel`
calculeaza rho la T = 1, unde cei patru membri cunoscuti dau 0.805 / 0.845 / 0.806 / 0.734. Frontiera
insa lucreaza pe semnalul TEMPERAT la T-ul ales LOLO, unde aceiasi patru dau 0.867 / 0.902 / 0.845 /
0.876. La few-shot diferenta e 0.062, adica destul cat sa rastoarne verdictul. Aici rho se masoara
mereu pe semnalul temperat, prin acelasi `make_fs_runs.pick_params` care alege T si pe test.

**Frontiera e o identitate in interiorul splitului, nu un predictor peste split.** Ordinea data de ea
pe trial, fata de castigul real pe B pe test, are Kendall +0.333 pe cei patru membri cunoscuti, deci
pe n = 4 nu inseamna nimic. Ce transfera, masurat, e `rho3`, cu corelatie trial-test +0.997; `r3`
transfera prost, +0.726, si se deplaseaza in JOS cu 0.025..0.097. De aceea cernerea NU e "duc pe test
ce prezice frontiera mai sus", ci doua porti scrise inainte de a vedea vreo cifra:

  1. `r3` pe trial cel putin +0.55, ca sa ramana peste +0.50 pe test dupa deplasare;
  2. dupa ce se aplica deplasarile in sensul cel mai NEFAVORABIL, `r3` minus 0.097 si `rho3` plus
     0.036, frontiera sa prezica in continuare castig peste perechea de acum.

Candidatii, si ce schimba fiecare:

  `v9_fara_context`     tinta singura, fara propozitie. Ambele prompturi ale sistemului conditioneaza
                        pe context. Predictie declarata: cade pe `si`, unde 214 tinte distincte din
                        600 de randuri inseamna 64% legaturi, iar legaturile plafoneaza Pearson.
  `v11_frecventa`       alt construct: cat de comun e cuvantul, nu cat de dificil.
  `v12_bin_*`           citire binara la trei praguri, agregata. Alta FORMA de citire.
  `v10_lema`            lema in loc de forma flexionata. Predictie declarata: cel mai putin decorelat
                        din toti, fiindca `fil` si `si` n-au lema deloc si pe restul lema difera de
                        forma pe 37-67% din randuri.
  `v7_proportie`        exista de la E.10 dar n-a fost dus mai departe, fiindca r-ul lui la T = 1 e
                        cel mai mic. E insa si cel mai decorelat masurat vreodata, rho 0.680 la T = 1.

Rulare:
  python prompt_lab.py --model gemma4-12b-4bit --variants v9_fara_context,v10_lema,v11_frecventa,\\
      v12_bin_necunoscut,v12_bin_dificil,v12_bin_dictionar,v7_proportie \\
      --out output/dist/promptlab_dist_trial.csv
  python analysis_frontiera.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_frontiera.md")
SRC = os.path.join(OUT, "dist", "promptlab_dist_trial.csv")
PAIR = os.path.join(OUT, "dist", "gemma4-12b-4bit_trial.csv")
SYS_DIST = os.path.join(OUT, "dist", "gemma4-12b-4bit_test.csv")

# Deplasarile trial -> test, masurate pe cei patru membri cunoscuti. Se aplica in sensul NEFAVORABIL.
DEP_R = -0.097
DEP_RHO = +0.036
PRAG_R = 0.55

# (eticheta, [variante], ce schimba)
CANDIDATI = [
    ("fara context", ["v9_fara_context"], "tinta singura, fara propozitie"),
    ("frecventa", ["v11_frecventa"], "alt construct: cat de comun, nu cat de dificil"),
    ("binar x3", ["v12_bin_necunoscut", "v12_bin_dificil", "v12_bin_dictionar"],
     "citire binara la trei praguri, agregata"),
    ("lema", ["v10_lema"], "lema in loc de forma flexionata"),
    ("proportie", ["v7_proportie"], "cati cititori din cinci, nu ce nota"),
]
# Membrii deja dusi pe test, pentru blocul de control. Nu adauga nicio configuratie noua pe test.
CUNOSCUTI = [("few-shot", "fewshot", +0.664449), ("rubrica", "rubrica", +0.660059),
             ("marcat", "marcat", +0.663347), ("learner", "learner", +0.659488)]
# Aceiasi patru, dar pe TRIAL, ca sa CALIBREZE poarta 2. Fara ei pragul ar fi arbitrar: aici se vede
# daca poarta separa membrii care au functionat pe test (few-shot +0.005247 si marcat +0.004146 pe B)
# de cei care n-au functionat (rubrica +0.000857, learner +0.000286). O poarta care ii respinge pe
# toti patru nu e conservatoare, e stricata, si nu are voie sa decida nimic despre candidatii noi.
CALIBRARE = [("few-shot", ["v3_fewshot"], +0.005247, "a functionat"),
             ("marcat", ["v8_marcat"], +0.004146, "a functionat"),
             ("rubrica", ["v2_rubrica"], +0.000857, "nu a functionat"),
             ("learner", ["v1_learner"], +0.000286, "nu a functionat")]

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def load_trial():
    from bakeoff_trial import with_context
    for q in (SRC, PAIR):
        if not os.path.exists(q):
            raise SystemExit(f"{q} lipseste")
    return pd.read_csv(SRC), with_context(pd.read_csv(PAIR), "trial")


def pl_of(d, pair, variante):
    """{limba: dict(Ps, y, ctx, n)} cu Ps = [membrii noi..., promptul expert, promptul scurt].

    Aceeasi forma pe care o consuma `make_fs_runs.pick_params`, deci criteriul de selectie e identic
    cu cel de pe test. Alinierea e POZITIONALA, cu verificare pe limba, tinta si complexitate, ca in
    `analysis_al3lea_trial.pl_of`.
    """
    Xs = []
    for v in variante:
        x = d[d["variant"] == v].reset_index(drop=True)
        if len(x) != len(pair):
            raise SystemExit(f"{v}: {len(x)} randuri, perechea are {len(pair)}")
        bad = ((x["lang"].astype(str).values != pair["lang"].astype(str).values)
               | (x["token"].astype(str).values != pair["token"].astype(str).values)
               | (np.abs(x["complexity"].values - pair["complexity"].values) > 1e-6))
        if bad.any():
            raise SystemExit(f"{v}: aliniere pozitionala esuata la randul {int(np.flatnonzero(bad)[0])}")
        Xs.append(x)
    out = {}
    for lg in sorted(pair["lang"].astype(str).unique()):
        gp = pair[pair["lang"].astype(str) == lg]
        m0 = (Xs[0]["lang"].astype(str).values == lg)
        Ps = [x[m0][[f"p1_{k}" for k in "12345"]].values.astype(float) for x in Xs]
        Ps += [gp[[f"p{j}_{k}" for k in "12345"]].values.astype(float) for j in (1, 2)]
        out[lg] = dict(Ps=Ps, y=Xs[0][m0]["complexity"].values.astype(float),
                       ctx=gp["context_id"].values, n=int(m0.sum()))
    return out


def sub(PL, idx):
    return {lg: dict(Ps=[v["Ps"][i] for i in idx], y=v["y"], ctx=v["ctx"], n=v["n"])
            for lg, v in PL.items()}


def r_under(PL, mod="temperatura"):
    """(r mediu, esantioane bootstrap, tabelul de parametri) cu T ales LOLO de `pick_params`."""
    import analysis_dist as ad
    from make_fs_runs import pick_params, b_of
    params, tab = pick_params(PL, mod, ad.T_GRID_EXT)
    rs, boots = [], []
    for lg in sorted(PL):
        T, bl = params[lg]
        b = b_of(PL[lg]["Ps"], T, bl)
        rs.append(ad.r_of(b, PL[lg]["y"]))
        boots.append(ad.boot_one(PL[lg]["y"], b, PL[lg]["ctx"])["boot"])
    return float(np.mean(rs)), boots, tab, params, rs


def frontiera(PL, params, k_nou):
    """(r_ens prezis, r per membru, rho3 mediu, matricea rho) pe semnalul TEMPERAT la T-ul ales.

    `k_nou` e cati dintre membri sunt noi; ultimii doi sunt mereu perechea sistemului. `rho3` e media
    corelatiilor dintre membrii noi si cele DOUA prompturi ale sistemului, adica exact marimea despre
    care s-a masurat ca transfera trial-test cu +0.997.
    """
    import analysis_dist as ad
    pred, rs_all, rho_new, rho_all = [], [], [], []
    for lg in sorted(PL):
        T = params[lg][0]
        S = [ad.expected(ad.temper(P, T)) for P in PL[lg]["Ps"]]
        r = [ad.r_of(s, PL[lg]["y"]) for s in S]
        n = len(S)
        rr = sum(ad.r_of(S[i], S[j]) for i in range(n) for j in range(i + 1, n))
        pred.append(sum(r) / np.sqrt(n + 2 * rr))
        rs_all.append(r)
        rho_new.append(np.mean([ad.r_of(S[i], S[j]) for i in range(k_nou)
                                for j in (n - 2, n - 1)]) if k_nou else 0.0)
        rho_all.append(rr)
    return (float(np.mean(pred)), list(np.mean(rs_all, axis=0)), float(np.mean(rho_new)),
            float(np.mean(rho_all)))


def frontiera_deplasata(r_membri, k_nou, rho_new, rho_pereche, rho_intre):
    """Frontiera recalculata cu deplasarile trial -> test.

    **Deplasarea lui `r` se aplica TUTUROR membrilor, nu doar celor noi.** Prima versiune o aplica
    numai membrilor noi si compara rezultatul cu perechea NEdeplasata, ceea ce nu e conservator, e
    incoerent: ar fi pus calitate de test in dreptul unei perechi de calitate de trial. Perechea
    coboara si ea de la +0.7013 pe trial la +0.6592 pe test. Deplasarea lui `rho` se aplica numai
    corelatiilor care implica membrii NOI, fiindca `rho12` al perechii e masurat pe acelasi split in
    amandoua cazurile si n-are de ce sa se deplaseze.

    `rho_intre` e corelatia medie intre membrii noi cand sunt mai multi. Nu se deplaseaza: e o
    proprietate a familiei, nu a transferului.
    """
    n = len(r_membri)
    r = [x + DEP_R for x in r_membri]
    rn = min(1.0, rho_new + DEP_RHO)
    n_sis = n - k_nou
    rr = rho_pereche                                   # perechea intre ea, nedeplasata
    rr += k_nou * n_sis * rn                           # membri noi cu perechea
    rr += (k_nou * (k_nou - 1) / 2) * rho_intre        # membri noi intre ei
    return sum(r) / np.sqrt(n + 2 * rr)


def main():
    import analysis_dist as ad
    d, pair = load_trial()
    langs = sorted(pair["lang"].astype(str).unique())
    lipsa = [v for _, vs, _ in CANDIDATI for v in vs if v not in set(d["variant"])]
    if lipsa:
        raise SystemExit(f"{SRC} n-are variantele {lipsa}")

    # perechea de acum, sub acelasi protocol
    PLp = sub(pl_of(d, pair, ["v9_fara_context"]), [1, 2])
    r_pair, B_pair, _, par_p, _ = r_under(PLp)
    _, r_pp, _, rho_pp = frontiera(PLp, par_p, 0)
    # Referinta pentru poarta 2: perechea trecuta prin ACEEASI deplasare, ca sa se compare
    # calitate-de-test cu calitate-de-test.
    r_pair_dep = frontiera_deplasata(r_pp, 0, 0.0, rho_pp, 0.0)

    emit("# E.16. Prompturi structural decorelate, cernute pe trial cu frontiera\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_frontiera.py`. "
         f"{sum(PLp[l]['n'] for l in langs)} instante de trial, {len(langs)} limbi. Criteriul de "
         "selectie e chiar `make_fs_runs.pick_params`, nerescris.\n",
         __doc__.split("Candidatii, si ce schimba")[0].split("\n", 2)[2].strip() + "\n",
         f"Perechea de acum, sub acelasi protocol: **{r_pair:+.6f}**, cu "
         f"r1 = {r_pp[0]:+.3f}, r2 = {r_pp[1]:+.3f}, rho12 = {rho_pp:.3f}.\n")

    # --- 0. verificarea de semn, inainte de orice agregare
    emit("## 0. Verificarea de semn\n",
         "Un membru cu r NEGATIV n-ar doar sa nu ajute, ar distruge ansamblul, iar formula frontierei "
         "presupune r pozitiv. `v11_frecventa` e singurul candidat la care semnul nu e garantat de "
         "constructie, fiindca intreaba despre frecventa, nu despre dificultate; scara lui e scrisa "
         "cu 5 = foarte rar tocmai ca semnul sa iasa pozitiv. Se verifica pe toate zece limbile, "
         "inainte de orice agregare.\n",
         "| candidat | r pe limba, min | max | limbi cu semn negativ |", "|---|---|---|---|")
    semn_ok = True
    for nume, vs, _ in CANDIDATI:
        PL = pl_of(d, pair, vs)
        rr = [ad.r_of(ad.expected(PL[lg]["Ps"][0]), PL[lg]["y"]) for lg in langs]
        neg = [lg for lg, x in zip(langs, rr) if x < 0]
        emit(f"| `{nume}` | {min(rr):+.4f} | {max(rr):+.4f} | "
             f"{', '.join(neg) if neg else '**niciuna**'} |")
        if len(neg) > len(langs) / 2:
            semn_ok = False
    emit("")
    if not semn_ok:
        emit("**PICAT pe semn.** Un candidat are r negativ pe majoritatea limbilor. Se opreste aici.\n")
        raise SystemExit("verificarea de semn a picat")

    def masoara(vs):
        """(dict cu toate marimile) pentru o lista de variante luate ca membri noi peste pereche."""
        PL = pl_of(d, pair, vs)
        k = len(vs)
        r3, B3, _, par3, _ = r_under(PL)
        pred, r_m, rho_new, _ = frontiera(PL, par3, k)
        rho_intre = 0.0
        if k > 1:
            acc = []
            for lg in langs:
                T = par3[lg][0]
                Sg = [ad.expected(ad.temper(P, T)) for P in PL[lg]["Ps"][:k]]
                acc.append(np.mean([ad.r_of(Sg[i], Sg[j])
                                    for i in range(k) for j in range(i + 1, k)]))
            rho_intre = float(np.mean(acc))
        pred_dep = frontiera_deplasata(r_m, k, rho_new, rho_pp, rho_intre)
        r3m = float(np.mean(r_m[:k]))
        # Raportul deviatiilor standard, membri noi fata de perechea sistemului. Conteaza fiindca
        # `b_of` mediaza valorile asteptate BRUTE, iar formula descrie media STANDARDIZATA: cand
        # variantele difera mult, un membru cu varianta mica primeste in practica mai putin decat
        # 1/n din greutate, si atunci cele doua marimi se despart.
        sd = []
        for lg in langs:
            T = par3[lg][0]
            Sg = [np.std(ad.expected(ad.temper(P, T))) for P in PL[lg]["Ps"]]
            sd.append([float(np.mean(Sg[:k])), float(np.mean(Sg[k:]))])
        sd = np.mean(sd, axis=0)
        return dict(k=k, r3=r3, B3=B3, pred=pred, r3m=r3m, rho=rho_new, rho_intre=rho_intre,
                    pred_dep=pred_dep, p1=bool(r3m >= PRAG_R), p2=bool(pred_dep > r_pair_dep),
                    vs=vs, sd_rap=float(sd[0] / sd[1]))

    # --- 0b. calibrarea portii 2 pe membrii cu rezultat CUNOSCUT pe test
    emit("## 1. Calibrarea portii, pe membrii cu rezultat cunoscut pe test\n",
         "Un prag ales de mine n-ar decide nimic. Cei patru membri de mai jos au fost dusi pana la "
         "capat pe test, deci se stie care a functionat: `few-shot` +0.005247 si `marcat` +0.004146 "
         "pe semnalul B, fata de `rubrica` +0.000857 si `learner` +0.000286. Aceleasi doua porti se "
         "aplica pe distributiile lor de TRIAL. Daca poarta ii respinge pe toti patru, e stricata si "
         "nu are voie sa decida nimic despre candidatii noi; daca ii separa, pragul e calibrat.\n",
         f"Referinta portii 2 e perechea trecuta prin aceeasi deplasare: **{r_pair_dep:+.6f}**, fata "
         f"de {r_pair:+.6f} nedeplasata.\n",
         "| membru | castig REAL pe B pe test | r3 | rho3 | frontiera dep. | poarta 1 | poarta 2 |",
         "|---|---|---|---|---|---|---|")
    CAL = {}
    for nume, vs, dtest, verd in CALIBRARE:
        if any(v not in set(d["variant"]) for v in vs):
            continue
        M = masoara(vs)
        CAL[nume] = dict(M, dtest=dtest, verd=verd)
        emit(f"| `{nume}` | {dtest:+.6f}, {verd} | {M['r3m']:+.3f} | {M['rho']:.3f} | "
             f"**{M['pred_dep']:+.6f}** | {'DA' if M['p1'] else 'nu'} | {'DA' if M['p2'] else 'nu'} |")
        print(f"    [cal] {nume:10s} r3={M['r3m']:+.3f} rho3={M['rho']:.3f} "
              f"dep {M['pred_dep']:+.6f} porti {int(M['p1'])}{int(M['p2'])}  (test {dtest:+.6f})",
              flush=True)
    emit("")
    trec_cal = [k for k in CAL if CAL[k]["p1"] and CAL[k]["p2"]]
    buni = [k for k in CAL if CAL[k]["dtest"] >= 0.004]
    if set(trec_cal) == set(buni) and buni:
        stare = (f"**Poarta separa exact.** Trec {', '.join('`'+k+'`' for k in trec_cal)}, adica "
                 "chiar cei doi care au functionat pe test, si cad ceilalti doi.")
    elif not trec_cal:
        stare = ("**Poarta e prea aspra si nu decide nimic.** Ii respinge si pe cei doi membri care "
                 "AU functionat pe test, deci un candidat nou respins de ea nu e respins de dovezi.")
    else:
        stare = (f"**Poarta separa partial.** Trec {', '.join('`'+k+'`' for k in trec_cal) or 'niciunul'}"
                 f", fata de cei care au functionat pe test, {', '.join('`'+k+'`' for k in buni)}.")
    emit(stare + "\n")

    # --- 1. cernerea
    emit("## 2. Cernerea, cu cele doua porti\n",
         f"`r3` si `rho3` sunt masurate pe semnalul TEMPERAT la T-ul ales LOLO. `r3 dupa dep.` e "
         f"`r3 {DEP_R:+.3f}`, `rho3 dupa dep.` e `rho3 {DEP_RHO:+.3f}`, adica deplasarile trial-test "
         "masurate, aplicate in sensul nefavorabil. `frontiera dep.` e formula recalculata cu ele, si "
         f"ea decide poarta 2, fata de perechea deplasata la fel, {r_pair_dep:+.6f}.\n",
         "| candidat | membri | r3 | rho3 | sd noi / sd sistem | ansamblu, media bruta | "
         "identitatea, media standardizata | brut - standardizat | r3 dupa dep. | rho3 dupa dep. | "
         "frontiera dep. | poarta 1 | poarta 2 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    S = {}
    for nume, vs, ce in CANDIDATI:
        M = masoara(vs)
        S[nume] = dict(M, ce=ce)
        emit(f"| `{nume}` | {M['k']} | {M['r3m']:+.3f} | {M['rho']:.3f} | {M['sd_rap']:.2f} | "
             f"**{M['r3']:+.6f}** | {M['pred']:+.6f} | {M['r3'] - M['pred']:+.6f} | "
             f"{M['r3m'] + DEP_R:+.3f} | {min(1.0, M['rho'] + DEP_RHO):.3f} | "
             f"**{M['pred_dep']:+.6f}** | {'DA' if M['p1'] else 'nu'} | {'DA' if M['p2'] else 'nu'} |")
        r3, pred, pred_dep, p1, p2, r3m, rho_new = (M['r3'], M['pred'], M['pred_dep'],
                                                    M['p1'], M['p2'], M['r3m'], M['rho'])
        print(f"    {nume:14s} r3={r3m:+.3f} rho3={rho_new:.3f} ansamblu {r3:+.6f} "
              f"(frontiera {pred:+.6f}) dep {pred_dep:+.6f} porti {int(p1)}{int(p2)}", flush=True)
    emit("")

    # --- 2. comparatiile perechi pe trial
    emit("### Fata de perechea de acum, pe trial\n",
         "Reesantionare pe contexte, seed fix, deci perechea vede aceeasi reesantionare. Intervalele "
         "sunt late si trebuie sa fie: 30 de instante per limba. Ce se citeste de aici e ORDINEA, nu "
         "cifrele.\n",
         "| candidat | in ansamblu fata de pereche | CI 95% pereche | P(>0) |", "|---|---|---|---|")
    for nume in S:
        dm, lo, hi, pp = ad.mean_diff_ci(S[nume]["B3"], B_pair)
        S[nume]["dm"] = dm
        emit(f"| `{nume}` | **{dm:+.6f}** | [{lo:+.6f}, {hi:+.6f}] | {pp:.1%} |")
    emit("")

    # --- 2b. ce e de fapt frontiera
    import analysis_dist as _ad
    def _z(v):
        v = np.asarray(v, float); sdv = v.std()
        return (v - v.mean()) / sdv if sdv > 0 else v * 0.0
    worst = 0.0
    for nume, vs, _ce in CANDIDATI:
        PL = pl_of(d, pair, vs)
        par, _ = __import__("make_fs_runs").pick_params(PL, "temperatura", ad.T_GRID_EXT)
        for lg in langs:
            T = par[lg][0]
            Sg = [ad.expected(ad.temper(P, T)) for P in PL[lg]["Ps"]]
            rr_ = [ad.r_of(x, PL[lg]["y"]) for x in Sg]
            nn = len(Sg)
            cc = sum(ad.r_of(Sg[i], Sg[j]) for i in range(nn) for j in range(i + 1, nn))
            worst = max(worst, abs(sum(rr_) / np.sqrt(nn + 2 * cc)
                                   - ad.r_of(np.mean([_z(x) for x in Sg], axis=0), PL[lg]["y"])))
    emit("### Ce e de fapt frontiera, si corectia unei formulari vechi\n",
         f"`r_ens = (suma r_i)/sqrt(n + 2*suma rho_ij)` **nu e o aproximare, e o identitate "
         f"algebrica**, si e identitatea mediei STANDARDIZATE a membrilor. Verificat pe toti "
         f"candidatii si toate limbile de aici: abatere maxima **{worst:.1e}**, adica precizia "
         "masinii.\n",
         "Ce se abate deci nu e formula, ci `make_fs_runs.b_of`, care mediaza valorile asteptate "
         "BRUTE, nu standardizate. Cand membrii au deviatii standard apropiate, cele doua marimi "
         "coincid pana la a treia zecimala, si de acolo vin `erorile` de 0.0003..0.0024 raportate "
         "pana acum in `output/e_al3lea.md`. Cand nu coincid, se despart mult: `binar x3` are "
         "membrii la 0.57 din deviatia standard a perechii, fiindca masa lui sta pe doua cifre din "
         "cinci, si atunci media bruta si cea standardizata difera cu 0.025.\n",
         "Consecinta practica, si e in favoarea codului de acum: media BRUTA a lui `b_of` e mai buna "
         "decat cea standardizata la exact acest candidat, +0.667746 fata de +0.642394, fiindca "
         "coboara singura greutatea unui membru slab. Deci `binar x3` nu cade dintr-un artefact de "
         "mediere; ar cadea si mai rau daca s-ar standardiza.\n")

    # --- 3. controlul: frontiera reproduce cifrele cunoscute de pe test
    emit("## 3. Control: frontiera reproduce cifrele cunoscute de pe test\n",
         "Pe date de test DEJA masurate, deci fara nicio configuratie noua pe test. Daca unealta de "
         "aici ar fi alta decat cea care a dat eroarea -0.000142 pe ansamblul de patru, cernerea de "
         "mai sus n-ar insemna nimic.\n",
         "| membru | r3 | rho3 | identitatea, media standardizata | observat, media bruta | "
         "brut - standardizat |", "|---|---|---|---|---|---|")
    from make_fs_runs import load_srcs, pick_params
    for nume, tag, obs in CUNOSCUTI:
        p = os.path.join(OUT, "dist", f"{tag}_gemma4-12b-4bit_test.csv")
        if not os.path.exists(p):
            continue
        PLt, _ = load_srcs([p, SYS_DIST])
        part, _ = pick_params(PLt, "temperatura", ad.T_GRID_EXT)
        pred, r_m, rho_new, _ = frontiera(PLt, part, 1)
        emit(f"| `{nume}` | {r_m[0]:+.3f} | {rho_new:.3f} | {pred:+.6f} | {obs:+.6f} | "
             f"{obs - pred:+.6f} |")
    emit("")

    # --- verdict
    trec = [k for k in S if S[k]["p1"] and S[k]["p2"]]
    emit("## Verdict\n")
    if trec:
        emit("Trec amandoua portile, deci merg pe test: "
             + ", ".join(f"`{k}` (r3 {S[k]['r3m']:+.3f}, rho3 {S[k]['rho']:.3f}, frontiera deplasata "
                         f"{S[k]['pred_dep']:+.6f} fata de {r_pair_dep:+.6f})" for k in trec) + ".\n")
    else:
        emit("**Niciun candidat nu trece amandoua portile.** Niciunul nu merge pe test, deci "
             "multiplicitatea de test nu creste cu nimic din raportul asta.\n")
    for k in sorted(S, key=lambda k: -S[k]["rho"]):
        why = []
        if not S[k]["p1"]:
            why.append(f"r3 = {S[k]['r3m']:+.3f}, sub pragul de {PRAG_R:+.2f}")
        if not S[k]["p2"]:
            why.append(f"frontiera deplasata {S[k]['pred_dep']:+.6f}, sub perechea "
                       f"deplasata {r_pair_dep:+.6f}")
        emit(f"- `{k}` ({S[k]['ce']}): rho3 = {S[k]['rho']:.3f}"
             + (f", rho intre membri {S[k]['rho_intre']:.3f}" if S[k]["k"] > 1 else "")
             + (". **Trece.**" if not why else ". Cade: " + "; ".join(why) + "."))
    emit("")
    rho_min = min(S[k]["rho"] for k in S)
    emit(f"Cel mai mic `rho3` obtinut e **{rho_min:.3f}**, la "
         f"`{min(S, key=lambda k: S[k]['rho'])}`, fata de 0.845 al celui mai decorelat prompt de pana "
         "acum. Pragul de care ar fi nevoie ca un membru slab sa bata perechea e `rho3` sub 0.62.\n")
    print(f"[E16] -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
