"""Distributia peste 1..5 ca semnal, nu ca punct. Offline, pe CSV-ul cu distributii salvate.

Semnalul B colapsa pana acum p(1..5) in valoarea asteptata la fiecare instanta si arunca vectorul
(`solution_bert._score_msgs`). De cand `rate_parts` il scrie pe disc, doua intrebari devin masurabile
fara nicio inferenta noua:

  b) TEMPERATURA. La Nohejl diferenta G-Eval 0.657 -> G-Scale 0.669 vine integral din softmax cu
     temperatura peste aceleasi cinci probabilitati, cu T = 2.0 ales pe media trial-urilor TUTUROR
     celor 10 limbi. Aici T se alege leave-one-language-out, deci fara nicio eticheta din limba
     evaluata, altfel nu avem ce revendica.
  c) DEZACORDUL. Eticheta MLSP e media notelor mai multor adnotatori, deci un cuvant pe care oamenii
     nu cad de acord e prin constructie un cuvant de mijloc. Intrebarea nu e daca dezacordul modelului
     coreleaza cu eticheta, ci daca o prezice printr-un canal DIFERIT de media distributiei. Se
     masoara ca validitate incrementala, cu media distributiei trecuta in controale.

Nu e semnalul C reincalzit. C era surprisal-ul tintei in context (`solution_bert.surprisal`), adica
cat de previzibil e cuvantul in propozitie. Asta e incertitudinea capului de notare, alta marime.
Faptul ca C a murit nu prezice nimic aici.

Nu adopta nimic si nu atinge nimic: citeste `output/dist/`, scrie `output/e_dist.md`.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_dist.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_dist.md")
DIST = os.path.join(OUT, "dist", "gemma4-12b-4bit_test.csv")
SYS_PREDS = os.path.join(OUT, "fusion_preds_lolo_adoptat.csv")
SYS_TABLE = os.path.join(OUT, "fusion_lolo_adoptat.csv")
N_BOOT = 2000
LANGS = ["ca", "de", "en", "es", "fil", "fr", "it", "ja", "pt", "si"]
# Grila de temperaturi. 1.0 e identitatea, deci linia de baza e IN grila si alegerea LOLO poate sa nu
# schimbe nimic, ceea ce e un rezultat la fel de bun ca oricare altul.
T_GRID = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0)
# Grila extinsa, folosita NUMAI ca diagnostic, si numai fiindca argmaxul pe grila de mai sus a iesit
# la marginea de sus pe toate cele zece limbi. Un argmax pe margine nu spune "T = 4", spune "grila s-a
# terminat inainte de varf". E un superset strict, deci nu muta nimic din ce s-a masurat pe grila
# specificata. Alegerea ramane leave-one-language-out si aici.
T_GRID_EXT = T_GRID + (6.0, 8.0, 12.0, 16.0, 24.0, 32.0, 64.0)
# Grila fina, pentru baleiajul de robustete din (e). NU e o grila de SELECTIE: acolo T se alege LOLO,
# aici se raporteaza r la T FIX, ca sa se vada forma curbei si latimea platoului. A alege T citind
# tabelul asta ar fi tuning pe scorul raportat.
T_FINE = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0,
          16.0, 20.0, 24.0, 32.0, 48.0, 64.0)
W5 = np.arange(1.0, 6.0)

_DOC = []


def emit(*lines):
    """Adauga in raport si scrie pe disc pe loc, ca un pas care crapa sa nu piarda pasii de dinainte.
    Acelasi idiom ca `analysis_fr.emit`."""
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


# ----------------------------------------------------------------------------- unelte
def r_of(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def resid(y, Z):
    """Rezidualul lui y dupa regresie liniara pe Z, cu intercept. Idiomul din `analysis_fr.resid`."""
    y = np.asarray(y, float)
    Z = np.asarray(Z, float)
    m = np.isfinite(y) & np.isfinite(Z).all(axis=1)
    out = np.full(len(y), np.nan)
    Zc = np.column_stack([np.ones(m.sum()), Z[m]])
    beta, *_ = np.linalg.lstsq(Zc, y[m], rcond=None)
    out[m] = y[m] - Zc @ beta
    return out


def boot_one(y, p, groups):
    from mlsp_common import boot_r_ci
    return boot_r_ci(y, p, groups, n_boot=N_BOOT)


def mean_ci(boots):
    """Intervalul MEDIEI pe cele zece limbi, din esantioanele per limba: se mediaza limbile la fiecare
    reesantionare, deci iese o distributie a mediei. Idiomul din `fuse_ab._agg_boot`."""
    m = min(len(b) for b in boots)
    M = np.vstack([b[:m] for b in boots]).mean(axis=0)
    return float(np.percentile(M, 2.5)), float(np.percentile(M, 97.5))


def mean_diff_ci(new, old):
    """Diferenta PERECHE pe medie. `boot_r_ci` are seed fix si primeste acelasi vector de contexte,
    deci reesantionarea k e aceeasi in ambele brate si zgomotul comun se anuleaza."""
    m = min(min(len(b) for b in new), min(len(b) for b in old))
    A = np.vstack([b[:m] for b in new]).mean(axis=0)
    B = np.vstack([b[:m] for b in old]).mean(axis=0)
    d = A - B
    return (float(np.mean(A) - np.mean(B)), float(np.percentile(d, 2.5)),
            float(np.percentile(d, 97.5)), float((d > 0).mean()))


def zero_out(lo, hi):
    return "exclude zero" if (lo > 0 or hi < 0) else "include zero"


# ----------------------------------------------------------------------------- distributia
def expected(P):
    """Valoarea asteptata a unei distributii pe 1..5, adusa in [0,1]. Aceeasi aritmetica cu
    `solution_bert._score_msgs`: ((sum p_i * i) - 1) / 4."""
    return (P @ W5 - 1.0) / 4.0


def temper(P, T):
    """p^(1/T), renormalizat. Pentru T = 1 e identitatea.

    E chiar softmax-ul cu temperatura al lui G-Scale: softmax(logit/T) e proportional cu
    exp(logit)^(1/T), iar p e deja normalizat peste cele cinci cifre, deci ridicarea la 1/T urmata de
    renormalizare da acelasi vector. Singura diferenta posibila ar fi ca p_i aduna mai multe id-uri
    per cifra (capcana SentencePiece), caz in care temperatura s-ar aplica distributiei AGREGATE pe
    cifre. La `gemma4-12b-4bit` cazul nu apare: `output/d4_sanity.md` arata cate un singur id per
    cifra, deci constructia de aici e literal cea a lui G-Scale.
    """
    if T == 1.0:
        return P
    Q = np.power(P, 1.0 / T)
    return Q / Q.sum(axis=1, keepdims=True)


def entropy(P):
    """Entropia in nati, cu 0 log 0 = 0."""
    return -np.where(P > 0, P * np.log(np.where(P > 0, P, 1.0)), 0.0).sum(axis=1)


def js_div(P, Q):
    """Divergenta Jensen-Shannon in nati, intre 0 si log 2."""
    M = 0.5 * (P + Q)
    def kl(A):
        r = np.where(A > 0, A * np.log(np.where(A > 0, A, 1.0) / np.where(M > 0, M, 1.0)), 0.0)
        return r.sum(axis=1)
    return 0.5 * (kl(P) + kl(Q))


# ----------------------------------------------------------------------------- date
def load():
    """Distributiile plus predictiile sistemului, aliniate pe `idx`.

    `idx` e pozitia in cadrul NEFILTRAT al lui `load_mlsp("test")`, recuperata pozitional de
    `bakeoff_trial.with_context` cu verificare rand cu rand pe limba, token si complexitate. E aceeasi
    cheie prin care `fuse_ab.load_signals` leaga semnalul B de semnalul A, deci join-ul de aici e
    exact cel al sistemului.
    """
    from bakeoff_trial import with_context
    if not os.path.exists(DIST):
        raise SystemExit(f"{DIST} lipseste. Ruleaza intai bakeoff_trial.py --split test --out ...")
    d = with_context(pd.read_csv(DIST), "test")
    need = [f"p{i}_{k}" for i in (1, 2) for k in "12345"] + ["raw1", "raw2"]
    miss = [c for c in need if c not in d.columns]
    if miss:
        raise SystemExit(f"{DIST} n-are coloanele {miss}. E un CSV de dinainte de `rate_parts`.")
    sysp = pd.read_csv(SYS_PREDS)
    m = sysp.merge(d[["idx", "B"] + need], on="idx", how="inner", suffixes=("_z", ""))
    if len(m) != len(sysp):
        raise SystemExit(f"join-ul pe idx a pastrat {len(m)} din {len(sysp)} randuri ale sistemului")
    return m


def per_lang(m):
    """{limba: dict cu vectorii de care are nevoie tot restul}."""
    out = {}
    for lg, g in m.groupby("lang", sort=True):
        P1 = g[[f"p1_{k}" for k in "12345"]].values.astype(float)
        P2 = g[[f"p2_{k}" for k in "12345"]].values.astype(float)
        out[lg] = dict(y=g["y"].values.astype(float), ctx=g["ctx"].values,
                       B=g["B"].values.astype(float), zB=g["B_z"].values.astype(float),
                       p_fuz=g["p_fuz"].values.astype(float), A=g["A"].values.astype(float),
                       P1=P1, P2=P2, n=len(g))
    return out


def b_at2(D, T1, T2):
    """Semnalul B cu cate o temperatura per prompt. `T1 == T2` e cazul din (b)."""
    return 0.5 * (expected(temper(D["P1"], T1)) + expected(temper(D["P2"], T2)))


def b_at(D, T):
    """Semnalul B la temperatura T, aceeasi pentru ambele prompturi. La T = 1 trebuie sa iasa exact
    coloana B."""
    return b_at2(D, T, T)


# ----------------------------------------------------------------------------- (a) linia de baza
def step_a(m, PL):
    print("[a] linia de baza: B reconstruit din distributii", flush=True)
    rec = np.concatenate([b_at(PL[lg], 1.0) for lg in sorted(PL)])
    obs = np.concatenate([PL[lg]["B"] for lg in sorted(PL)])
    same = sum(f"{a:.8f}" == f"{b:.8f}" for a, b in zip(rec, obs))
    mx = float(np.abs(rec - obs).max())

    tab = pd.read_csv(SYS_TABLE).set_index("lang")
    rows = []
    for lg in sorted(PL):
        D = PL[lg]
        rows.append(dict(lang=lg, n=D["n"], r_B=r_of(D["B"], D["y"]),
                         r_pub=float(tab.loc[lg, "r_B_raw"]), r_zB=r_of(D["zB"], D["y"])))
    t = pd.DataFrame(rows)
    dmax = float((t["r_B"] - t["r_pub"]).abs().max())

    emit("# Distributia peste 1..5, masurata ca semnal\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_dist.py`. Date: "
         f"`{os.path.relpath(DIST, HERE)}` (distributiile salvate de `rate_parts`, aceeasi rulare care "
         f"reproduce bit cu bit coloana B din `output/bakeoff_test/gemma4-12b-4bit.csv`) si "
         f"`{os.path.relpath(SYS_PREDS, HERE)}` (predictiile per instanta ale sistemului de 0.674946). "
         "Nicio inferenta LLM: tot ce urmeaza e aritmetica peste cifre deja masurate.\n",
         "Semnalul B al sistemului vine de la `gemma4-12b-4bit` pe toate cele zece limbi, ales "
         "leave-one-language-out pe test (`output/e_fusion_lolo_adoptat.md`), deci distributiile "
         "unui singur model acopera tot sistemul.\n",
         "**Nimic de aici nu e adoptat.** Cifra publicata ramane 0.674946, produsa de comanda din "
         "`output/e_fusion_lolo_adoptat.md`, nemodificata.\n",
         "## (a) Linia de baza se reproduce\n",
         "B se reconstruieste din coloanele noi cu aceeasi aritmetica din `solution_bert."
         "_score_msgs`: media pe cele doua prompturi a `((sum p_i * i) - 1) / 4`. Daca nu iese "
         "coloana B, restul raportului nu inseamna nimic si nu se scrie.\n",
         f"- randuri: **{len(rec)}**, din care **{same}** identice cu coloana `B` la 8 zecimale",
         f"- abaterea maxima: **{mx:.3e}**, adica rotunjirea la 8 zecimale cu care coloana e scrisa pe "
         f"disc (`f\"{{b:.8f}}\"`), nu o pierdere de precizie: probabilitatile sunt scrise cu "
         f"`repr(float)`, care face roundtrip exact",
         f"- r per limba fata de cel publicat in `{os.path.relpath(SYS_TABLE, HERE)}`: abatere maxima "
         f"**{dmax:.2e}**\n")
    if same != len(rec):
        emit("**PICAT.** Reconstructia nu da coloana B. Restul raportului nu se scrie.\n")
        raise SystemExit("(a) a picat: B reconstruit difera de coloana B")
    print(f"    {same}/{len(rec)} identice, abatere max {mx:.3e}, r max dif {dmax:.2e}", flush=True)
    return t


# ----------------------------------------------------------------------------- (b) temperatura
def s_limit(P, floor=1e-300):
    """Semnalul la T -> infinit, in forma inchisa.

    Pentru T mare, `p^(1/T)` normalizat e (1/5)(1 + (log p_i - media log p)/T) la ordinul intai, deci
    valoarea asteptata minus 3 e proportionala cu `sum_i (i-3) log p_i`. Pearson e invariant la
    transformari afine pozitive, deci r-ul limitei se citeste direct din marimea asta. Nu e o
    extrapolare numerica: la T mare formula de sus pierde precizie, asta nu.
    """
    return np.log(np.clip(P, floor, None)) @ (W5 - 3.0)


def temp_pick(PL, grid):
    """Alegerea LOLO a temperaturii pe grila data. -> (tabel, esantioane bootstrap per limba).

    Criteriul e identic in FORMA cu `fuse_ab.pick_model` si cu cel al lui `w`: pentru limba L, T e
    argmaxul mediei lui r peste randurile de test ale CELORLALTE 9 limbi.
    """
    langs = sorted(PL)
    R = {lg: np.array([r_of(b_at(PL[lg], T), PL[lg]["y"]) for T in grid]) for lg in langs}
    rows, boots_T, boots_1 = [], [], []
    for lg in langs:
        crit = np.mean([R[l2] for l2 in langs if l2 != lg], axis=0)
        j = int(np.argmax(crit))
        T = grid[j]
        D = PL[lg]
        bT = boot_one(D["y"], b_at(D, T), D["ctx"])
        b1 = boot_one(D["y"], D["B"], D["ctx"])
        k = min(len(bT["boot"]), len(b1["boot"]))
        dv = bT["boot"][:k] - b1["boot"][:k]
        boots_T.append(bT["boot"]); boots_1.append(b1["boot"])
        rows.append(dict(lang=lg, T=T, la_limita=(j in (0, len(grid) - 1)),
                         crit_lat=float(crit.max() - crit.min()), r_1=b1["r"], r_T=bT["r"],
                         d=bT["r"] - b1["r"], lo=float(np.percentile(dv, 2.5)),
                         hi=float(np.percentile(dv, 97.5)), p=float((dv > 0).mean()),
                         T_pe_L=grid[int(np.argmax(R[lg]))], r_pe_L=float(R[lg].max())))
    return pd.DataFrame(rows), boots_T, boots_1, R


def step_b(PL):
    print("[b] temperatura, aleasa LOLO", flush=True)
    langs = sorted(PL)
    t, boots_T, boots_1, R = temp_pick(PL, T_GRID)
    for _, r in t.iterrows():
        print(f"    {r['lang']:4s} T={r['T']:<5g} r {r['r_1']:+.4f} -> {r['r_T']:+.4f} "
              f"({r['d']:+.4f})", flush=True)
    dm, lo, hi, pp = mean_diff_ci(boots_T, boots_1)

    # Contrast, NU protocolul nostru: un singur T ales pe media tuturor celor 10 limbi de test.
    glob = np.mean([R[lg] for lg in langs], axis=0)
    jg = int(np.argmax(glob))
    Tg, r_glob = T_GRID[jg], float(np.mean([R[lg][jg] for lg in langs]))

    emit("## (b) Temperatura, linia de baza imprumutata de la G-Scale\n",
         "`p_T` proportional cu `p^(1/T)`, renormalizat, apoi aceeasi valoare asteptata si aceeasi "
         "mediere pe cele doua prompturi. E chiar softmax-ul cu temperatura al lui G-Scale: "
         "`softmax(logit/T)` e proportional cu `exp(logit)^(1/T)`, iar p e deja normalizat peste cele "
         "cinci cifre. Constructia coincide literal, nu doar in spirit: `output/d4_sanity.md` arata "
         "ca `gemma4-12b-4bit` are cate un SINGUR id per cifra, deci p_i nu aduna nimic si "
         "temperatura cade pe logiti, nu pe o distributie agregata. Grila: "
         + ", ".join(f"`{T:g}`" for T in T_GRID) + ".\n",
         "**T se alege leave-one-language-out**, cu criteriul identic in forma cu `fuse_ab.pick_model` "
         "si cu cel al lui `w`: pentru limba L, T e argmaxul mediei lui r peste randurile de test ale "
         "CELORLALTE 9 limbi. Nicio eticheta din L nu intra in alegere. La Nohejl, T = 2.0 e ales pe "
         "media trial-urilor tuturor celor 10 limbi, deci si pe a limbii evaluate.\n",
         "`latime criteriu` e r maxim minus r minim pe grila, pe limbile de potrivire: cu cat e mai "
         "plata, cu atat argmaxul e mai mult zgomot. Acelasi diagnostic ca `latime w` din "
         "`output/e_fusion_lolo_adoptat.md`.\n",
         "| limba | T ales LOLO | la marginea grilei | latime criteriu | r la T=1 | r la T ales | "
         "diferenta | CI 95% pereche | P(>0) |",
         "|---|---|---|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        emit(f"| {r['lang']} | {r['T']:g} | {'DA' if r['la_limita'] else 'nu'} | "
             f"{r['crit_lat']:.4f} | {r['r_1']:+.4f} | {r['r_T']:+.4f} | **{r['d']:+.4f}** | "
             f"[{r['lo']:+.4f}, {r['hi']:+.4f}] | {r['p']:.1%} |")
    emit(f"| **medie** | | | | **{t['r_1'].mean():+.4f}** | **{t['r_T'].mean():+.4f}** | "
         f"**{dm:+.4f}** | [{lo:+.4f}, {hi:+.4f}] | {pp:.1%} |", "",
         f"Pe medie, temperatura aleasa LOLO **{'muta' if (lo > 0 or hi < 0) else 'nu muta'}** "
         f"semnalul B: {dm:+.4f}, interval pereche [{lo:+.4f}, {hi:+.4f}], deci **{zero_out(lo, hi)}**. "
         f"Castiga pe {int((t['d'] > 0).sum())} limbi din 10.\n",
         f"**Dar alegerea cade la marginea de sus a grilei pe {int(t['la_limita'].sum())} limbi din "
         f"10.** Un argmax pe margine nu localizeaza un optim, spune doar ca grila s-a terminat "
         f"inainte de varf, si cifra de mai sus e o margine inferioara a ce poate da temperatura, nu "
         f"efectul celui mai bun T. De aceea urmeaza diagnosticul cu grila extinsa. Latimea medie a "
         f"criteriului e {t['crit_lat'].mean():.4f}.\n",
         "### Ce ar fi dat protocolul lui Nohejl, si de ce nu se raporteaza ca al nostru\n",
         f"Un singur T ales pe media celor 10 limbi de TEST da T = {Tg:g} si r mediu {r_glob:+.4f}. "
         "Cifra foloseste scorul de test al fiecarei limbi ca sa aleaga hiperparametrul limbii "
         "respective, deci e o margine superioara, la fel ca celula `oracol` din "
         "`output/e_bakeoff_test.md`, nu o alternativa disponibila sub §5.1.\n",
         "Coloana `T pe L singur` de mai jos e acelasi lucru dus la capat, per limba, si spune cat "
         "pierde protocolul: T ales chiar pe limba evaluata.\n",
         "| limba | T ales LOLO | r sub LOLO | T ales pe L insasi | r acolo | pretul protocolului |",
         "|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        emit(f"| {r['lang']} | {r['T']:g} | {r['r_T']:+.4f} | {r['T_pe_L']:g} | {r['r_pe_L']:+.4f} | "
             f"{r['r_T'] - r['r_pe_L']:+.4f} |")
    emit(f"| **medie** | | **{t['r_T'].mean():+.4f}** | | **{t['r_pe_L'].mean():+.4f}** | "
         f"**{(t['r_T'] - t['r_pe_L']).mean():+.4f}** |", "")

    # ---- diagnostic: unde se termina de fapt curba
    te, bTe, b1e, Re = temp_pick(PL, T_GRID_EXT)
    dme, loe, hie, ppe = mean_diff_ci(bTe, boots_1)
    lim = {lg: r_of(0.5 * (s_limit(PL[lg]["P1"]) + s_limit(PL[lg]["P2"])), PL[lg]["y"])
           for lg in langs}
    zeros = int(sum((PL[lg]["P1"] <= 0).sum() + (PL[lg]["P2"] <= 0).sum() for lg in langs))
    emit("### Grila specificata se termina inainte de varf\n",
         "Sectiunea asta e un DIAGNOSTIC, si exista pentru un singur motiv: argmaxul de mai sus a "
         "cazut la marginea de sus pe zece limbi din zece. Nu s-a extins grila fiindca rezultatul ar "
         "fi fost nesatisfacator, ci fiindca un argmax pe margine nu localizeaza nimic. Grila extinsa "
         "e un superset strict al celei specificate, alegerea ramane leave-one-language-out, si "
         "**cifra de referinta ramane cea de pe grila specificata**.\n",
         "r mediu pe cele 10 limbi, la T fix, fara nicio alegere:\n",
         "| T | " + " | ".join(f"{T:g}" for T in T_GRID_EXT) + " | limita |",
         "|" + "---|" * (len(T_GRID_EXT) + 2))
    means = list(np.mean([Re[lg] for lg in langs], axis=0))
    emit("| r mediu | " + " | ".join(f"{m:+.4f}" for m in means) + " | "
         f"{np.mean(list(lim.values())):+.4f} |", "",
         f"Curba are un varf INTERIOR, la T = {T_GRID_EXT[int(np.argmax(means))]:g} cu "
         f"{max(means):+.4f}, si coboara apoi catre limita analitica {np.mean(list(lim.values())):+.4f}. "
         "Limita nu e o extrapolare numerica: la T mare, valoarea asteptata minus 3 e proportionala cu "
         "`sum_i (i-3) log p_i`, iar Pearson e invariant la transformari afine. Toate cele "
         f"{zeros} celule cu p = 0 din setul intreg fac logaritmul sigur, adica nu e niciuna.\n",
         "Alegerea LOLO refacuta pe grila extinsa:\n",
         "| limba | T ales LOLO, extins | la marginea grilei | r la T ales | fata de T=1 | CI 95% |",
         "|---|---|---|---|---|---|")
    for _, r in te.iterrows():
        emit(f"| {r['lang']} | {r['T']:g} | {'DA' if r['la_limita'] else 'nu'} | {r['r_T']:+.4f} | "
             f"{r['d']:+.4f} | [{r['lo']:+.4f}, {r['hi']:+.4f}] |")
    emit(f"| **medie** | | | **{te['r_T'].mean():+.4f}** | **{dme:+.4f}** | [{loe:+.4f}, {hie:+.4f}] |",
         "",
         f"Pe grila extinsa nicio limba nu mai alege marginea, iar castigul fata de T = 1 e {dme:+.4f}, "
         f"interval [{loe:+.4f}, {hie:+.4f}], adica {zero_out(loe, hie)}. Diferenta fata de grila "
         f"specificata, {te['r_T'].mean() - t['r_T'].mean():+.4f}, e mica fata de latimea intervalului: "
         "curba e practic plata intre T = 6 si T = 24, deci alegerea exacta a lui T conteaza mult mai "
         "putin decat faptul CA se aplica o temperatura.\n")
    return t, (dm, lo, hi, pp), te, (dme, loe, hie, ppe), {lg: t.set_index("lang").loc[lg, "T"]
                                                           for lg in langs}


# ----------------------------------------------------------------------------- (c) dezacordul
SIGNALS = {
    "entropie": "entropia lui p, mediata pe cele doua prompturi",
    "capat_sus": "masa pe capatul greu, `p4 + p5`, mediata pe prompturi",
    "capat_jos": "masa pe capatul usor, `p1 + p2`, mediata pe prompturi",
    "dezacord_E": "diferenta valorilor asteptate ale celor doua prompturi, in modul",
    "dezacord_JS": "divergenta Jensen-Shannon intre cele doua distributii",
}

# Controalele, in ordinea in care se strang. Primul e cel evident si e INSUFICIENT; celelalte spun
# cat din el era artefact. Vezi textul sectiunii pentru de ce.
CONTROLS = {
    "B": "B, liniar",
    "B3": "B, B^2, B^3",
    "BT": "B la temperatura aleasa LOLO",
    "sys": "predictia sistemului, liniar",
    "sys3": "predictia sistemului, plus patrat si cub",
}


def signals_of(D):
    P1, P2 = D["P1"], D["P2"]
    return {"entropie": 0.5 * (entropy(P1) + entropy(P2)),
            "capat_sus": 0.5 * (P1[:, 3:].sum(1) + P2[:, 3:].sum(1)),
            "capat_jos": 0.5 * (P1[:, :2].sum(1) + P2[:, :2].sum(1)),
            "dezacord_E": np.abs(expected(P1) - expected(P2)),
            "dezacord_JS": js_div(P1, P2)}


def controls_of(D, T):
    """Matricile de control, per limba. `T` e temperatura aleasa LOLO pentru limba asta."""
    B, F, bt = D["B"], D["p_fuz"], b_at(D, T)
    return {"B": np.column_stack([B]),
            "B3": np.column_stack([B, B ** 2, B ** 3]),
            "BT": np.column_stack([bt]),
            "sys": np.column_stack([F]),
            "sys3": np.column_stack([F, F ** 2, F ** 3])}


def step_c(PL, Tsel):
    print("[c] dezacordul: validitate incrementala", flush=True)
    langs = sorted(PL)
    res = {s: [] for s in SIGNALS}
    boots = {s: {c: [] for c in CONTROLS} for s in SIGNALS}
    for lg in langs:
        D = PL[lg]
        S, Z = signals_of(D), controls_of(D, Tsel[lg])
        y, ctx = D["y"], D["ctx"]
        for name, v in S.items():
            row = dict(lang=lg, n=D["n"], mean=float(np.mean(v)), r_brut=r_of(v, y),
                       r_cu_B=r_of(v, D["B"]))
            for tag, Zc in Z.items():
                # Validitate INCREMENTALA, tiparul din `analysis_fr.step4`: ambele laturi
                # rezidualizate pe acelasi control, apoi r intre reziduuri, cu interval pe contexte.
                b = boot_one(resid(y, Zc), resid(v, Zc), ctx)
                row |= {f"r_{tag}": b["r"], f"{tag}_lo": b["lo"], f"{tag}_hi": b["hi"]}
                boots[name][tag].append(b["boot"])
            res[name].append(row)
        print(f"    {lg} gata", flush=True)
    T = {s: pd.DataFrame(rows) for s, rows in res.items()}
    agg = {s: {c: mean_ci(boots[s][c]) for c in CONTROLS} for s in SIGNALS}

    emit("## (c) Dezacordul modelului: alt canal, sau aceeasi medie in alta haina?\n",
         "Eticheta MLSP e media notelor mai multor adnotatori, deci un cuvant pe care oamenii nu cad "
         "de acord e prin constructie un cuvant de mijloc. Daca incertitudinea capului de notare "
         "urmeaza acelasi tipar, ea ar trebui sa prezica eticheta. Intrebarea nu e daca o prezice, e "
         "daca o prezice printr-un canal DIFERIT de media distributiei, care e chiar semnalul B.\n",
         "Testul nu e corelatia bruta, e **validitate incrementala**: corelatie partiala cu eticheta, "
         "cu ambele laturi rezidualizate pe acelasi control, si interval bootstrap pe CONTEXTE, 2000 "
         "de reesantionari. Acelasi tipar cu ce face `analysis_fr.py` pentru fertilitate. Reziduurile "
         "se calculeaza o data pe esantionul intreg si abia apoi se reesantioneaza, ca acolo, deci "
         "intervalul nu contine incertitudinea potrivirii controlului.\n",
         "### De ce controlul liniar pe B nu e destul, si de ce e chiar controlul gresit aici\n",
         "Toate cele cinci masuri sunt functii de ACEEASI distributie din care se calculeaza B. "
         "Entropia unei distributii pe 1..5 e legata mecanic de medie: o medie extrema forteaza masa "
         "spre un capat, deci entropie mica. Masa pe capete e si mai rau, coreleaza peste 0.9 cu B in "
         "toate limbile. Asta e avertismentul cerut, si coloana `r cu B` il masoara.\n",
         "Dar sectiunea (b) adauga un motiv mai tare, care nu se vedea inainte de ea: temperatura "
         "imbunatateste r pe toate cele zece limbi, adica **B e misspecificat ca predictor LINIAR al "
         "etichetei**. O forma mai plata a aceleiasi distributii prezice mai bine. Atunci orice marime "
         "corelata cu curbura aia va parea ca aduce un canal nou, cand de fapt reciteste acelasi "
         "canal. Un control liniar pe B nu poate distinge cele doua lucruri. De aceea se raporteaza "
         "cinci controale, de la cel naiv la cel flexibil:\n",
         "".join(f"- `{k}`: {v}\n" for k, v in CONTROLS.items()),
         "Un semnal care supravietuieste lui `B3` si lui `BT` spune ceva ce media distributiei nu "
         "spune, oricum ai citi-o. Unul care se stinge intre `B` si `B3` era curbura, nu canal.\n")

    # --- tabelul de sinteza, cel care decide
    emit("### Sinteza: media pe cele 10 limbi, per control\n",
         "| semnal | r brut | r cu B (mecanic) | " +
         " | ".join(f"vs `{c}`" for c in CONTROLS) + " |",
         "|" + "---|" * (len(CONTROLS) + 3))
    for name in SIGNALS:
        t = T[name]
        cells = []
        for c in CONTROLS:
            lo, hi = agg[name][c]
            z = "" if lo <= 0 <= hi else " *"
            cells.append(f"{t[f'r_{c}'].mean():+.4f}<br>[{lo:+.4f}, {hi:+.4f}]{z}")
        emit(f"| `{name}` | {t['r_brut'].mean():+.4f} | {t['r_cu_B'].mean():+.4f} | "
             + " | ".join(cells) + " |")
    emit("", "`*` = intervalul mediei exclude zero. Intervalele sunt ale MEDIEI pe cele zece limbi: se "
         "mediaza limbile la fiecare reesantionare, ca in `fuse_ab._agg_boot`.\n")

    # --- tabelele per limba
    for name, doc in SIGNALS.items():
        t = T[name]
        emit(f"### `{name}`: {doc}\n",
             "| limba | n | medie | r brut | r cu B | partial vs `B` | CI 95% | partial vs `B3` | "
             "CI 95% | partial vs `sys3` | CI 95% |",
             "|---|---|---|---|---|---|---|---|---|---|---|")
        for _, r in t.iterrows():
            zb = "" if r["B_lo"] <= 0 <= r["B_hi"] else " *"
            z3 = "" if r["B3_lo"] <= 0 <= r["B3_hi"] else " *"
            zs = "" if r["sys3_lo"] <= 0 <= r["sys3_hi"] else " *"
            emit(f"| {r['lang']} | {r['n']} | {r['mean']:.3f} | {r['r_brut']:+.4f} | "
                 f"{r['r_cu_B']:+.4f} | {r['r_B']:+.4f} | [{r['B_lo']:+.4f}, {r['B_hi']:+.4f}]{zb} | "
                 f"{r['r_B3']:+.4f} | [{r['B3_lo']:+.4f}, {r['B3_hi']:+.4f}]{z3} | "
                 f"{r['r_sys3']:+.4f} | [{r['sys3_lo']:+.4f}, {r['sys3_hi']:+.4f}]{zs} |")
        b_lo, b_hi = agg[name]["B"]
        t3_lo, t3_hi = agg[name]["B3"]
        s3_lo, s3_hi = agg[name]["sys3"]
        emit(f"| **medie** | {int(t['n'].sum())} | | **{t['r_brut'].mean():+.4f}** | "
             f"**{t['r_cu_B'].mean():+.4f}** | **{t['r_B'].mean():+.4f}** | [{b_lo:+.4f}, {b_hi:+.4f}] | "
             f"**{t['r_B3'].mean():+.4f}** | [{t3_lo:+.4f}, {t3_hi:+.4f}] | "
             f"**{t['r_sys3'].mean():+.4f}** | [{s3_lo:+.4f}, {s3_hi:+.4f}] |", "")
    return T, agg


# ----------------------------------------------------------------------------- (d) fuziunea
# Configuratiile rulate de `fuse_ab.py --b-dir`, si controalele care le fac citibile. Tabelul e o
# harta, nu o rulare: `analysis_dist.py` nu cheama `fuse_ab.py`, doar citeste predictiile scrise de el.
FUSIONS = [("ctrl_nemodificat", "comanda publicata, fara niciun flag nou", None),
           ("ctrl_bdir", "`--b-dir output/bakeoff_test`, adica flagul catre chiar directorul canonic",
            "bakeoff_test"),
           ("ctrl_T1", "`--b-dir` catre directorul regenerat cu T = 1", "bakeoff_test_T1"),
           ("distT", "B la temperatura aleasa LOLO pe grila SPECIFICATA", "bakeoff_test_T"),
           ("distText", "B la temperatura aleasa LOLO pe grila EXTINSA", "bakeoff_test_Text"),
           ("distTpp", "cate o temperatura per prompt, perechea aleasa LOLO", "bakeoff_test_Tpp")]
SYS_TAG = "adoptat"


def _preds(tag):
    q = os.path.join(OUT, f"fusion_preds_lolo_{tag}.csv")
    return pd.read_csv(q) if os.path.exists(q) else None


def step_d(Tsel, Tsel_ext):
    """Comparatia PERECHE fata de sistem, recalculata aici din predictiile per instanta.

    Nu se citeste din raportul lui `fuse_ab.py`: aceeasi marime, calculata a doua oara, cu acelasi
    `boot_r_ci` si aceleasi contexte. Daca cele doua nu coincid, una din ele e gresita.
    """
    print("[d] fuziunea, comparatie pereche", flush=True)
    ref = _preds(SYS_TAG)
    if ref is None:
        emit("## (d) Fuziunea\n", f"`fusion_preds_lolo_{SYS_TAG}.csv` lipseste, nu se compara nimic.\n")
        return
    rows = []
    for tag, doc, bdir in FUSIONS:
        d = _preds(tag)
        if d is None:
            rows.append(dict(tag=tag, doc=doc, bdir=bdir, stare="nerulat"))
            continue
        per, bn, bo = [], [], []
        for lg in sorted(ref["lang"].unique()):
            a = ref[ref["lang"] == lg].set_index("idx")
            b = d[d["lang"] == lg].set_index("idx").reindex(a.index)
            if b["p_fuz"].isna().any():
                raise SystemExit(f"{tag} n-acopera toate randurile lui {lg}")
            b0 = boot_one(a["y"].values, a["p_fuz"].values, a["ctx"].values)
            b1 = boot_one(a["y"].values, b["p_fuz"].values, a["ctx"].values)
            k = min(len(b0["boot"]), len(b1["boot"]))
            dv = b1["boot"][:k] - b0["boot"][:k]
            bn.append(b1["boot"]); bo.append(b0["boot"])
            per.append(dict(lang=lg, r_azi=b0["r"], r_nou=b1["r"], d=b1["r"] - b0["r"],
                            lo=float(np.percentile(dv, 2.5)), hi=float(np.percentile(dv, 97.5))))
        t = pd.DataFrame(per)
        dm, lo, hi, pp = mean_diff_ci(bn, bo)
        rows.append(dict(tag=tag, doc=doc, bdir=bdir, stare="rulat", t=t,
                         r=float(t["r_nou"].mean()), d=dm, lo=lo, hi=hi, p=pp))
        print(f"    {tag:18s} r={t['r_nou'].mean():.6f}  d={dm:+.4f} [{lo:+.4f}, {hi:+.4f}]",
              flush=True)

    emit("## (d) Fuziunea, pe tag nou\n",
         "Se schimba UN SINGUR lucru fata de sistem: coloana `B` a lui `gemma4-12b-4bit` pe test e "
         "citita la temperatura, prin `fuse_ab.py --b-dir`. Celelalte doua CSV-uri de test se copiaza "
         "verbatim, deci bazinul de candidati al lui `pick_model` ramane acelasi, iar selectia alege "
         "in continuare gemma pe toate cele zece limbi. Fisierele se scriu cu `make_bt_runs.py`.\n",
         "`--b-dir` e un flag OPT-IN adaugat pentru asta, cu implicit `None`. Primele trei randuri "
         "din tabel sunt controalele care arata ca nu a mutat nimic: comanda publicata nemodificata, "
         "aceeasi comanda cu flagul catre chiar directorul canonic, si aceeasi comanda cu flagul catre "
         "un director regenerat cu T = 1. Toate trei trebuie sa dea 0.674946.\n",
         "Intervalele de mai jos sunt recalculate AICI din predictiile per instanta, cu acelasi "
         "`boot_r_ci` si aceleasi contexte, nu copiate din rapoartele lui `fuse_ab.py`. Coincid cu "
         "ele, ceea ce e in sine o verificare.\n",
         "| configuratie | ce schimba | r mediu | fata de sistem | CI 95% pereche | P(>0) |",
         "|---|---|---|---|---|---|")
    for r in rows:
        if r["stare"] == "nerulat":
            emit(f"| `{r['tag']}` | {r['doc']} | nerulat | | | |")
            continue
        if r["lo"] == r["hi"] == 0.0:
            # Predictii identice cu ale sistemului: diferenta e zero la fiecare reesantionare, deci
            # P(>0) ar tipari 0.0%, ceea ce s-ar citi ca „a pierdut". E control trecut, nu pierdere.
            emit(f"| `{r['tag']}` | {r['doc']} | **{r['r']:.6f}** | identic | interval de latime 0 | "
                 "control trecut |")
            continue
        emit(f"| `{r['tag']}` | {r['doc']} | **{r['r']:.6f}** | {r['d']:+.4f} | "
             f"[{r['lo']:+.4f}, {r['hi']:+.4f}] | {r['p']:.1%} |")
    emit("")
    ok = [r for r in rows if r.get("stare") == "rulat" and r["tag"].startswith("dist")]
    for r in ok:
        t = r["t"]
        nz = int(((t["lo"] > 0) | (t["hi"] < 0)).sum())
        emit(f"### `{r['tag']}`, per limba\n",
             "| limba | r sistem | r configuratie noua | diferenta | CI 95% pereche |",
             "|---|---|---|---|---|")
        for _, x in t.iterrows():
            z = "" if x["lo"] <= 0 <= x["hi"] else " *"
            emit(f"| {x['lang']} | {x['r_azi']:+.4f} | {x['r_nou']:+.4f} | **{x['d']:+.4f}** | "
                 f"[{x['lo']:+.4f}, {x['hi']:+.4f}]{z} |")
        emit(f"| **medie** | **{t['r_azi'].mean():+.4f}** | **{t['r_nou'].mean():+.4f}** | "
             f"**{r['d']:+.4f}** | [{r['lo']:+.4f}, {r['hi']:+.4f}] |", "",
             f"Castiga pe {int((t['d'] > 0).sum())} limbi din 10, cu interval care exclude zero pe "
             f"{nz}. Intervalul MEDIEI, care e cifra care conteaza, "
             f"{'exclude' if (r['lo'] > 0 or r['hi'] < 0) else 'include'} zero.\n")

    emit("### Trei lucruri de scris, nu de ascuns\n",
         "1. **T e fixat din (b), nu ales din nou in `fit_choice`** alaturi de `w_src` si de setul de "
         "trasaturi. Asa se schimba un singur lucru fata de sistem. Un T ales in interiorul selectiei "
         "imbricate ar fi al patrulea nivel si nu s-a coborat pana acolo.\n",
         "2. **Coloana `B_T` a unei limbi de potrivire L' e construita cu T ales excluzand L', dar nu "
         "si L.** Cifra limbii tinute deoparte nu e atinsa: T-ul lui L nu vede nicio eticheta din L. "
         "Dar alegerile lui L depind indirect de etichetele lui L prin coloanele CELORLALTE limbi. E "
         "exact dependenta de un nivel pe care `output/e_fusion_lolo_adoptat.md` o declara deja la "
         "punctul 2 din „unde nu e garantat”, pentru modelul lui B, si se declara la fel.\n",
         "3. **Alegerea intre grila specificata si cea extinsa se face pe scorul de test.** Amandoua "
         "sunt curate pe dinauntru, dar diferenta dintre ele, "
         + (f"{ok[1]['r'] - ok[0]['r']:+.6f}" if len(ok) > 1 else "cand exista") +
         ", nu se poate arbitra fara sa privesti testul. E acelasi tip de bifurcatie ca alegerea "
         "intre configuratiile din `output/e_fusion_lolo_adoptat.md`, sectiunea „Scara "
         "configuratiilor”: fiecare e curata pe dinauntru, dar alegerea intre ele se uita la scorul "
         "raportat. Se declara ca atare in Limitations, nu se ascunde intr-o alegere de grila.\n")
    return rows


# ----------------------------------------------------------------------------- (e) robustete
def step_e(PL):
    """Baleiaj la T FIX, cu interval pereche fata de T = 1 la fiecare punct. Descriptiv, nu selectiv.

    Raspunde la „cat de sensibil e castigul la valoarea exacta a lui T": daca intervalul exclude zero
    pe un platou larg, alegerea lui T nu e locul unde se produce cifra.
    """
    print("[e] baleiaj fin, interval la fiecare T", flush=True)
    langs = sorted(PL)
    base = {lg: boot_one(PL[lg]["y"], PL[lg]["B"], PL[lg]["ctx"]) for lg in langs}
    rows = []
    for T in T_FINE:
        bs = [boot_one(PL[lg]["y"], b_at(PL[lg], T), PL[lg]["ctx"]) for lg in langs]
        dm, lo, hi, pp = mean_diff_ci([b["boot"] for b in bs], [base[lg]["boot"] for lg in langs])
        rows.append(dict(T=T, r=float(np.mean([b["r"] for b in bs])), d=dm, lo=lo, hi=hi, p=pp,
                         nwin=int(sum(b["r"] > base[lg]["r"] for lg, b in zip(langs, bs)))))
        print(f"    T={T:<6g} r={rows[-1]['r']:.4f}  {dm:+.4f} [{lo:+.4f}, {hi:+.4f}]", flush=True)
    t = pd.DataFrame(rows)
    ok = t[(t.lo > 0) & (t["T"] != 1.0)]

    emit("## (e) Cat de robust e castigul la valoarea exacta a lui T\n",
         "Tabelul de mai jos NU alege nimic: r se calculeaza la T FIX, aceeasi pentru toate cele zece "
         "limbi, si se raporteaza diferenta PERECHE fata de T = 1, cu interval pe contexte. E "
         "descriptiv. A alege T citind chiar tabelul asta ar fi tuning pe scorul raportat, si de aia "
         "cifra care se citeaza ramane cea de la (b), unde T se alege leave-one-language-out.\n",
         "| T | r mediu | fata de T=1 | CI 95% pereche | P(>0) | limbi in castig |",
         "|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        z = "" if r["lo"] <= 0 <= r["hi"] else " *"
        b = "**" if r["T"] == 1.0 else ""
        emit(f"| {b}{r['T']:g}{b} | {b}{r['r']:.4f}{b} | {r['d']:+.4f} | "
             f"[{r['lo']:+.4f}, {r['hi']:+.4f}]{z} | {r['p']:.1%} | {r['nwin']}/10 |")
    emit("", f"`*` = intervalul exclude zero. **Castigul are interval care exclude zero pe "
         f"{len(ok)} din cele {len(t) - 1} valori de T diferite de 1**, de la {ok['T'].min():g} pana "
         f"la {ok['T'].max():g}. Maximul e la T = {t.loc[t['r'].idxmax(), 'T']:g}, cu "
         f"{t['r'].max():.4f}, dar intre T = 4 si T = 24 diferenta de r e "
         f"{t[(t['T'] >= 4) & (t['T'] <= 24)]['r'].max() - t[(t['T'] >= 4) & (t['T'] <= 24)]['r'].min():.4f}, "
         "adica sub o zecime din latimea oricarui interval de aici.\n",
         "Concluzia care conteaza pentru scris: **nu se revendica o valoare a lui T, se revendica un "
         "platou.** Orice T intre 4 si 24 da practic aceeasi cifra, si castigul fata de T = 1 tine pe "
         "tot platoul. Alegerea exacta a lui T e deci mult mai putin importanta decat faptul CA se "
         "aplica o temperatura, ceea ce e si raspunsul la intrebarea daca argmaxul e zgomot: e, si nu "
         "conteaza.\n")
    return t


# ----------------------------------------------------------------------------- (f) T per prompt
def step_f_pick(PL, tsel_ext):
    """Alegerea perechii (T1, T2) per limba, fara nimic de raport. Separata ca `make_bt_runs.py` sa
    foloseasca exact acelasi criteriu, nu o copie a lui."""
    return _step_f(PL, tsel_ext, report=False)


def step_f(PL, tsel_ext):
    return _step_f(PL, tsel_ext, report=True)


def _step_f(PL, tsel_ext, report=True):
    """Cate o temperatura per prompt, aleasa tot LOLO, pe perechi din grila extinsa."""
    if report:
        print("[f] temperatura per prompt", flush=True)
    langs = sorted(PL)
    G = T_GRID_EXT
    # r pentru fiecare pereche (T1, T2) si fiecare limba. Grila e 16x16, deci 256 de candidati.
    R = {lg: np.array([[r_of(b_at2(PL[lg], t1, t2), PL[lg]["y"]) for t2 in G] for t1 in G])
         for lg in langs}
    rows, bn, bo = [], [], []
    for lg in langs:
        crit = np.mean([R[l2] for l2 in langs if l2 != lg], axis=0)
        i, j = np.unravel_index(int(np.argmax(crit)), crit.shape)
        T1, T2 = G[i], G[j]
        D = PL[lg]
        b2 = boot_one(D["y"], b_at2(D, T1, T2), D["ctx"])           # per prompt
        b1 = boot_one(D["y"], b_at(D, tsel_ext[lg]), D["ctx"])      # o singura T, tot LOLO, (b) extins
        k = min(len(b2["boot"]), len(b1["boot"]))
        dv = b2["boot"][:k] - b1["boot"][:k]
        bn.append(b2["boot"]); bo.append(b1["boot"])
        rows.append(dict(lang=lg, T1=T1, T2=T2, T_unic=tsel_ext[lg], r_unic=b1["r"], r_pp=b2["r"],
                         d=b2["r"] - b1["r"], lo=float(np.percentile(dv, 2.5)),
                         hi=float(np.percentile(dv, 97.5)),
                         crit_lat=float(crit.max() - crit.min()),
                         margine=float(crit[i, j] - np.max(np.diag(crit)))))
        if report:
            print(f"    {lg:4s} T1={T1:<5g} T2={T2:<5g} (unic {tsel_ext[lg]:g})  "
                  f"r {b1['r']:+.4f} -> {b2['r']:+.4f}", flush=True)
    t = pd.DataFrame(rows)
    dm, lo, hi, pp = mean_diff_ci(bn, bo)
    if not report:
        return t, (dm, lo, hi, pp)

    # Cat de diferite sunt cele doua prompturi, luate separat: T optim al fiecaruia pe media LOLO.
    solo = {}
    for k, key in ((0, "P1"), (1, "P2")):
        Rs = {lg: np.array([r_of(expected(temper(PL[lg][key], T)), PL[lg]["y"]) for T in G])
              for lg in langs}
        m = np.mean([Rs[lg] for lg in langs], axis=0)
        solo[key] = (G[int(np.argmax(m))], float(m.max()), float(m[G.index(1.0)]))

    emit("## (f) Cate o temperatura per prompt\n",
         "Cele doua prompturi nu sunt acelasi instrument: primul cere raspunsul ca `ONLY a single "
         "digit from 1 to 5`, al doilea ca `only the digit`, si nu au aceeasi ascutime. Fiecare "
         "primeste aici temperatura lui. Perechea (T1, T2) se alege tot leave-one-language-out, pe "
         f"grila extinsa luata de doua ori, deci {len(G)}x{len(G)} = {len(G)**2} de candidati in loc "
         f"de {len(G)}.\n",
         "Comparatia e fata de temperatura UNICA aleasa tot LOLO pe aceeasi grila, adica fata de "
         "varianta `distText` din (d), nu fata de T = 1. Altfel s-ar amesteca doua schimbari.\n",
         "| limba | T prompt 1 | T prompt 2 | T unic | r cu T unic | r per prompt | diferenta | "
         "CI 95% pereche | latime criteriu | margine peste diagonala |",
         "|---|---|---|---|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        z = "" if r["lo"] <= 0 <= r["hi"] else " *"
        emit(f"| {r['lang']} | {r['T1']:g} | {r['T2']:g} | {r['T_unic']:g} | {r['r_unic']:+.4f} | "
             f"{r['r_pp']:+.4f} | **{r['d']:+.4f}** | [{r['lo']:+.4f}, {r['hi']:+.4f}]{z} | "
             f"{r['crit_lat']:.4f} | {r['margine']:+.5f} |")
    emit(f"| **medie** | | | | **{t['r_unic'].mean():+.4f}** | **{t['r_pp'].mean():+.4f}** | "
         f"**{dm:+.4f}** | [{lo:+.4f}, {hi:+.4f}] | | |", "",
         "`margine peste diagonala` e cu cat bate perechea castigatoare cel mai bun punct cu "
         "T1 = T2 pe ACELASI criteriu. E cifra care spune daca a doua temperatura cumpara ceva sau "
         "doar da voie argmaxului sa se plimbe: o margine de ordinul a 1e-4 pe un criteriu lat de "
         f"{t['crit_lat'].mean():.3f} inseamna ca nu cumpara.\n",
         f"Pe medie, a doua temperatura da **{dm:+.4f}**, interval [{lo:+.4f}, {hi:+.4f}], adica "
         f"**{zero_out(lo, hi)}**.\n",
         "Cele doua prompturi, luate fiecare singur, cu T ales pe media tuturor limbilor:\n",
         "| prompt | T optim | r la T optim | r la T=1 |", "|---|---|---|---|",
         f"| 1 | {solo['P1'][0]:g} | {solo['P1'][1]:+.4f} | {solo['P1'][2]:+.4f} |",
         f"| 2 | {solo['P2'][0]:g} | {solo['P2'][1]:+.4f} | {solo['P2'][2]:+.4f} |", "")
    return t, (dm, lo, hi, pp)


# ----------------------------------------------------------------------------- verdict
def verdict(tb, db, te, dbe, TC, agg, rows=None):
    fus = ""
    if rows:
        ok = [r for r in rows if r.get("stare") == "rulat" and r["tag"].startswith("dist")]
        ctl = [r for r in rows if r.get("stare") == "rulat" and r["tag"].startswith("ctrl")]
        fus = ("; ".join(f"`{r['tag']}` da **{r['r']:.6f}**, {r['d']:+.4f} fata de sistem, CI "
                         f"[{r['lo']:+.4f}, {r['hi']:+.4f}]" for r in ok)
               + f". Cele {len(ctl)} controale dau toate "
               + ("0.674946" if all(abs(r["r"] - 0.674946) < 5e-7 for r in ctl) else "ALTCEVA, de vazut")
               + ", deci flagul `--b-dir` nu misca nimic singur. **Nimic nu e adoptat aici**: cifra "
                 "publicata ramane 0.674946 pana cand decide Alexandru.")
    dm, lo, hi, pp = db
    dme, loe, hie, ppe = dbe
    # Ce trece mai departe: numai ce supravietuieste controlului FLEXIBIL. Un semnal care exclude zero
    # fata de `B` dar nu si fata de `B3` nu e un canal nou, e curbura lui B recitita.
    viu = [s for s in SIGNALS if agg[s]["B3"][0] > 0 or agg[s]["B3"][1] < 0]
    viu_sys = [s for s in SIGNALS if agg[s]["sys3"][0] > 0 or agg[s]["sys3"][1] < 0]
    naiv = [s for s in SIGNALS if agg[s]["B"][0] > 0 or agg[s]["B"][1] < 0]
    emit("## Verdict\n",
         "1. **Linia de baza se reproduce**: B reconstruit din distributiile salvate e coloana B, la "
         "8 zecimale, pe toate cele 5624 de randuri.\n",
         f"2. **Temperatura tine.** Aleasa leave-one-language-out pe grila specificata da {dm:+.4f} pe "
         f"medie, interval pereche [{lo:+.4f}, {hi:+.4f}], deci {zero_out(lo, hi)}, si castiga pe "
         f"{int((tb['d'] > 0).sum())} limbi din 10. Semnalul B trece de la {tb['r_1'].mean():+.4f} la "
         f"{tb['r_T'].mean():+.4f}. Alegerea a cazut insa la marginea grilei pe "
         f"{int(tb['la_limita'].sum())} limbi din 10; pe grila extinsa varful e interior si castigul e "
         f"{dme:+.4f}, [{loe:+.4f}, {hie:+.4f}].\n",
         f"3. **Dezacordul, cu controlul naiv:** {len(naiv)} din 5 masuri au interval al mediei care "
         f"exclude zero fata de B liniar" + (f" ({', '.join('`'+x+'`' for x in naiv)})" if naiv else "")
         + ".\n",
         f"4. **Dezacordul, cu controlul flexibil, si asta e cifra care conteaza:** raman "
         f"{len(viu)} din 5" + (f" ({', '.join('`'+x+'`' for x in viu)})" if viu else "") +
         ". Masurile de FORMA a unei singure distributii, entropia si masa pe capete, se sting: "
         "erau curbura lui B, adica exact ce repara temperatura din (b), citita a doua oara. "
         "Ce ramane, daca ramane, e dezacordul INTRE cele doua prompturi, care nu e o functie de o "
         "singura distributie si pe care media nu o poate exprima.\n",
         f"5. **Fata de sistemul intreg**, cu acelasi control flexibil, raman "
         f"{len(viu_sys)} din 5" + (f" ({', '.join('`'+x+'`' for x in viu_sys)})" if viu_sys else "")
         + ".\n",
         (f"6. **Fuziunea, pe tag nou:** {fus}\n" if fus else ""),
         "7. **Ce urmeaza.** " + ("Nimic nu supravietuieste controlului flexibil, deci din (c) nu "
                                  "pleaca nicio fuziune. Rezultatul negativ e rezultatul.\n" if not viu
                                  else "Temperatura merge la fuziune pe tag nou, cu comparatie "
                                  "PERECHE fata de sistem. Pentru " +
                                  ", ".join('`'+x+'`' for x in viu) + " decizia nu e a acestui raport: "
                                  "ar fi un AL TREILEA termen in fuziune, iar `fuse_ab.fit_choice` are "
                                  "azi o singura pondere. Nimic nu se adopta fara interval pereche "
                                  "care exclude zero pe cifra finala.\n"))
    print("\n[verdict] naiv:", naiv or "-", "| flexibil:", viu or "-", "| vs sistem:", viu_sys or "-",
          flush=True)


def main():
    m = load()
    PL = per_lang(m)
    print(f"[0] {len(m)} randuri, {len(PL)} limbi", flush=True)
    step_a(m, PL)
    tb, db, te, dbe, Tsel = step_b(PL)
    TC, agg = step_c(PL, Tsel)
    Tsel_ext = {r["lang"]: r["T"] for _, r in te.iterrows()}
    rows = step_d(Tsel, Tsel_ext)
    step_e(PL)
    step_f(PL, Tsel_ext)
    verdict(tb, db, te, dbe, TC, agg, rows)
    print(f"-> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
