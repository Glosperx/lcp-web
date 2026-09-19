"""Axa REGRESORULUI pe semnalul A, masurata sub protocolul LOLO real.

De ce exista. Bratul A foloseste `blend_ridge_hgb` de la inceput, iar alegerea n-a fost niciodata
masurata pe splitul care conteaza. Singura cifra de pana acum, din docstringul lui
`analysis_lasso.py`, e pe free-gate-ul romanesc vechi (EN <-> MLSP romanic, CV 5-fold), unde lasso
da 0.5688 fata de 0.5512 pentru blend. `e_split_gap.md` arata insa ca nicio cifra de pe alt split nu
e predictie, deci axa era deschisa, nu promitatoare.

Intrebarea care a pornit-o a fost concreta: ar da TabFM (Google Research) mai mult decat HGB. TabFM
NU e boosting, e atentie pe randuri si coloane in stil TabPFN plus invatare in context in stil
TabICL, deci nu se substituie lui HGB, ar fi un al treilea membru al blend-ului. Fisierul asta
raspunde la intrebarea de dinaintea lui: cat de mult misca in general schimbarea estimatorului, si
ce i-ar trebui unui membru nou ca sa treaca bara.

Ce face, si totul din predictii de pe disc, nicio constanta scrisa de mana:
  1. tabelul r pe cele 10 limbi pentru fiecare regresor rulat cu `--regressor`;
  2. matricea rho intre estimatori, mediata pe limbi;
  3. r al mediei standardizate pentru TOATE submultimile, deci ansamblurile ies gratis;
  4. curba de prag: pentru un al treilea membru de calitate r3, ce rho maxim admite bara.

Punctul 4 foloseste aceeasi identitate ca `analysis_frontiera_enc.py`, si din acelasi motiv: pentru
media STANDARDIZATA a membrilor,

    r_ens = (suma r_i) / sqrt(k + 2 * suma_{i<j} rho_ij)

nu e o aproximare, e o identitate algebrica. Aici se verifica din nou, pe limba, la ordinul 1e-16.

Adaugat pe 26 august, pentru axa LINIARA. Tot ce s-a masurat pe axa asta pana acum a schimbat
jumatatea de ARBORI a blend-ului; jumatatea liniara a ramas `Ridge(alpha=300)` in absolut toate
variantele, iar `alpha` e mostenit si nu s-a re-potrivit niciodata sub LOLO. De aici:

  5. sectiunea de INLOCUIRE. Poarta de la punctul 4 e scrisa pentru un al TREILEA membru si nu
     raspunde la intrebarea "ce se intampla daca schimb jumatatea liniara". Pentru fiecare candidat
     se tipareste `r(candidat + hgb)` fata de `r(ridge + hgb)`, si castigul implicat in fuziune.
  6. sectiunea de GRILA. Pentru fiecare familie parametrica, punctul ales leave-one-language-out,
     langa media predictiilor intregii grile si langa LATIMEA CRITERIULUI, fiindca regula
     transversala a proiectului e ca argmaxul pe un criteriu plat e zgomot si atunci se mediaza.

`--spatiu` serveste si axa encoderului fara nicio linie noua: sufixul de encoder din `_p()` sta pe
aceeasi pozitie ca prefixul de spatiu, deci `--spatiu _e5` citeste bratul e5, iar `--spatiu _labse`
pe labse. `--extra` e pentru cazul in care un singur membru vine din alt spatiu decat ceilalti.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_regresor.py
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_regresor.py --spatiu _e5
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_regresor.py \
      --extra tabfm256=output/e1_frozen_preds_tf-proj-394_reg-tabfm-cache_mf256_lemma_fert_inloc.csv
"""
import argparse
import itertools
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

# Numele scurt -> sufixul din `_p()`. `blend` e incumbentul si are sufix gol, ca fisierul publicat.
CANDIDATI = {"blend": "", "blend-lasso": "_reg-blend-lasso", "ridge": "_reg-ridge", "hgb": "_reg-hgb", "hgb-adanc": "_reg-hgb-adanc",
             "extratrees": "_reg-extratrees", "blend-et": "_reg-blend-et",
             "tabfm": "_reg-tabfm-cache"}
# Axa liniara. Numele scurt E numele dat lui `--regressor`, deci nu exista nicio harta de tradus si
# nici loc de nepotrivire intre ce scrie in tabel si ce s-a rulat.
LINIARI = ("lasso", "elasticnet",
           "ridge-a30", "ridge-a100", "ridge-a1000", "ridge-a3000", "ridge-a10000", "ridge-a30000",
           "lasso-a1e-4", "lasso-a3e-4", "lasso-a1e-3", "lasso-a3e-3", "lasso-a3e-2",
           "pls-k4", "pls-k8", "pls-k16", "pls-k32", "pls-k64",
           "huber", "bayesridge", "ard", "krr-rbf", "svr-lin")
CANDIDATI.update({n: f"_reg-{n}" for n in LINIARI})

# Sesiunea OBIECTIVULUI. Tot ce e mai sus schimba FAMILIA de functii sau REGULARIZAREA, pe aceeasi
# tinta si cu aceeasi pierdere patratica. Ce urmeaza schimba pierderea, tinta, incadrarea problemei si
# informatia pe care o vede modelul.
OBIECTIV = ("lgbm-l8", "lgbmlin-l8", "cat-d3", "rf-n300", "mlp-h128", "knn-k50",
            "hgb-abs", "hgb-q50",
            "tt-rank-ridge", "tt-rank-hgb", "ttz-rank-ridge", "ttz-rank-hgb",
            "tt-logit2-ridge", "tt-logit2-hgb", "tt-logit005-ridge",
            "ord-lin-k5", "ord-hgb-k5", "ord-lin-k10", "ord-hgb-k10",
            "orde-lin-k5", "orde-hgb-k5", "clf-lin-k5", "clf-hgb-k5",
            "rs-ridge-f3-n10", "rs-hgb-f3-n10", "w-ridge-c1", "w-hgb-c1",
            "tt-id-ridge", "rs-ridge-f10-n1")
CANDIDATI.update({n: f"_reg-{n}" for n in OBIECTIV})

# CLASA DE MECANISM a fiecarui candidat, adica CE anume s-a schimbat fata de `ridge`. E tabelul de care
# atarna intreaga intrebare de research a sesiunii: au candidatii care schimba OBIECTIVUL un rho
# sistematic mai mic la r comparabil decat cei care schimba doar forma functiei.
#
# Scrisa in `output/_predictii_obiectiv.md` INAINTE de orice rulare a sesiunii, si copiata aici ca sa
# poata fi citita de cod. Nu se rescrie dupa ce se vad reziduurile: o clasa atribuita post-hoc face
# comparatia pe clase fara nicio semnificatie, fiindca oricare candidat poate fi mutat in clasa care il
# avantajeaza.
#
#   REGULARIZARE  pierdere patratica, liniar dens, se schimba numai penalizarea sau puterea ei.
#                 E norul de REFERINTA fata de care se citeste orice altceva.
#   FAMILIE       alta forma de functie, acelasi loss, aceeasi tinta.
#   LOSS          aceeasi familie si aceeasi tinta, alta functie de cost. Tot un parametru de LOCATIE.
#   TINTA         se prezice alt functional al aceleiasi etichete.
#   INCADRARE     problema nu mai e regresie: clase plus valoare asteptata.
#   INFORMATIE    acelasi obiectiv si aceeasi familie, dar modelul e potrivit pe altceva.
#   CONTROL       invelis cu transformare identica; trebuie sa reproduca baza bit-exact.
_M = {
    "REGULARIZARE": ["ridge", "ridge-a30", "ridge-a100", "ridge-a1000", "ridge-a3000",
                     "ridge-a10000", "ridge-a30000", "lasso", "lasso-a1e-4", "lasso-a3e-4",
                     "lasso-a1e-3", "lasso-a3e-3", "lasso-a3e-2", "elasticnet", "bayesridge", "ard"],
    "FAMILIE": ["hgb", "hgb-adanc", "extratrees", "krr-rbf", "pls-k4", "pls-k8", "pls-k16",
                "pls-k32", "pls-k64", "tabfm", "lgbm-l8", "lgbmlin-l8", "cat-d3", "rf-n300",
                "mlp-h128", "knn-k50"],
    "LOSS": ["huber", "svr-lin", "hgb-abs", "hgb-q50"],
    "TINTA": ["tt-rank-ridge", "tt-rank-hgb", "ttz-rank-ridge", "ttz-rank-hgb",
              "tt-logit2-ridge", "tt-logit2-hgb", "tt-logit005-ridge"],
    "INCADRARE": ["ord-lin-k5", "ord-hgb-k5", "ord-lin-k10", "ord-hgb-k10",
                  "orde-lin-k5", "orde-hgb-k5", "clf-lin-k5", "clf-hgb-k5"],
    "INFORMATIE": ["rs-ridge-f3-n10", "rs-hgb-f3-n10", "w-ridge-c1", "w-hgb-c1"],
    "CONTROL": ["tt-id-ridge", "rs-ridge-f10-n1"],
}
MECANISM = {n: c for c, ns in _M.items() for n in ns}
# Ordinea de tiparire: reperul primul, apoi forma functiei, apoi cele trei axe ale obiectivului.
ORDINE_M = ["REGULARIZARE", "FAMILIE", "LOSS", "TINTA", "INCADRARE", "INFORMATIE", "CONTROL"]

# Familiile parametrice, cu punctul de grila deja existent inclus la locul lui: `ridge` E alpha=300 si
# `lasso` E alpha=1e-2, deci grila lor nu are gauri. Ordinea e crescatoare in parametru, ca sa se
# vada pe ce latura a grilei cade optimul si daca e la marginea ei.
FAMILII = {
    "ridge (alpha)": [("ridge-a30", 30.0), ("ridge-a100", 100.0), ("ridge", 300.0),
                      ("ridge-a1000", 1000.0), ("ridge-a3000", 3000.0),
                      ("ridge-a10000", 10000.0), ("ridge-a30000", 30000.0)],
    "lasso (alpha)": [("lasso-a1e-4", 1e-4), ("lasso-a3e-4", 3e-4), ("lasso-a1e-3", 1e-3),
                      ("lasso-a3e-3", 3e-3), ("lasso", 1e-2), ("lasso-a3e-2", 3e-2)],
    "pls (k)":       [("pls-k4", 4.0), ("pls-k8", 8.0), ("pls-k16", 16.0), ("pls-k32", 32.0),
                      ("pls-k64", 64.0)],
}
COL = "p_multi"
# Bara pe fuziune si factorii de transmisie A -> fuziune, din `output/e_frontiera_enc.md`.
BARA = 0.0045
FACTORI = {"optimist": 0.259, "pesimist": 0.091}


def _p(suf, spatiu=""):
    """`spatiu` e prefixul de transformare a embeddingului, ex. `_tf-proj-200`.

    Exista fiindca TabFM nu incape pe latimea intreaga (774 de coloane fata de 500 documentate), deci
    comparatia cu el se face pe un spatiu redus. Si atunci TOTI estimatorii trebuie cititi de pe
    acelasi spatiu: altfel diferenta amesteca regresorul cu reducerea si nu se poate atribui."""
    return os.path.join(OUT, f"e1_frozen_preds{spatiu}{suf}_lemma_fert_inloc.csv")


def zl(v):
    """Standardizare, cu podea pe deviatie. O predictie CONSTANTA nu e o ipoteza teoretica: pe e5,
    `lasso` la alpha=0.03 zeroeste toti coeficientii pe sinhaleza si ramane doar interceptul, deci
    `std` iese exact 0 si impartirea da `inf`/`nan`, care apoi se plimba tacut in toata coloana de
    ansambluri. Se intoarce zero, adica media, exact conventia lui `fuse_ab.zscore` si
    `make_enc_mean.zscore`, iar apelantul RAPORTEAZA cazul in loc sa-l ascunda."""
    v = np.asarray(v, float)
    sd = v.std()
    if not np.isfinite(sd) or sd < 1e-12:
        return np.zeros(len(v))
    return (v - v.mean()) / sd


def degenerate(F, ref, col):
    """(candidat, limba) cu predictie constanta pe limba aceea. Vezi `zl`."""
    out = []
    for k, d in F.items():
        for lg in sorted(ref["lang"].unique()):
            v = d[col].values[(ref["lang"] == lg).values]
            sd = float(np.std(np.asarray(v, float)))
            if not np.isfinite(sd) or sd < 1e-12:
                out.append((k, lg, len(np.unique(v))))
    return out


# Cvintetul care identifica un rand. Aceeasi lista ca `META` din `make_a_blend.py`, si din acelasi
# motiv: doua rulari cu alt `--afeat` sau alt encoder dau fisiere de aceeasi FORMA, cu aceleasi
# coloane si acelasi `idx`, iar o comparatie intre ele ar ieși fara nicio eroare si fara nicio
# semnificatie. `token` si `context_id` sunt ce le distinge. Verificarea pe `idx` singur nu ajunge.
META = ["split", "idx", "lang", "token", "context_id"]


def _citeste(p):
    d = pd.read_csv(p)
    return d[d["split"] == "test"].sort_values(["lang", "idx"]).reset_index(drop=True)


def incarca(col, spatiu="", extra=None):
    """Predictiile de test ale fiecarui candidat existent pe disc, aliniate pe cvintetul `META`.

    `extra` e o harta NUME -> CALE pentru membri care vin din ALT spatiu decat ceilalti. Exista
    fiindca `_p()` are un singur prefix de spatiu pentru toti, iar TabFM nu incape pe embeddingul
    plin si trainiaste numai pe `proj-394`. Ruta hibrida (liniarul si arborii pe embeddingul plin,
    TabFM din cache-ul proiectat) se poate masura numai daca cele doua spatii intra in acelasi tabel,
    si se poate masura ONEST numai daca randurile se verifica, ce face bucla de mai jos."""
    F, ref, prim = {}, None, None
    surse = [(nume, _p(suf, spatiu)) for nume, suf in CANDIDATI.items()]
    surse += [(nume, cale) for nume, cale in (extra or {}).items()]
    for nume, p in surse:
        if not os.path.exists(p):
            if extra and nume in extra:
                sys.exit(f"--extra {nume}: {p} lipseste")
            continue
        d = _citeste(p)
        if ref is None:
            ref, prim = d, nume
        else:
            if len(d) != len(ref):
                sys.exit(f"{p}: {len(d)} randuri de test fata de {len(ref)} la `{prim}`.")
            for m in META:
                if not (d[m].astype(str).values == ref[m].astype(str).values).all():
                    sys.exit(f"{p}: coloana `{m}` nu coincide cu `{prim}`. Nu sunt aceleasi randuri, "
                             f"deci nu se compara si nu se mediaza.")
        F[nume] = d
    if not F:
        sys.exit("niciun fisier de candidat pe disc; ruleaza finetune_xlmr.py --regressor ...")
    return F, ref


def r_pe_limbi(d, ref, col):
    return {lg: pearsonr(d[col][ref["lang"] == lg], ref["complexity"][ref["lang"] == lg])[0]
            for lg in sorted(ref["lang"].unique())}


def pregatire(F, ref, col):
    """`z` per (candidat, limba) si `y` per limba, calculate O SINGURA DATA.

    Enumerarea de submultimi e 2^k, iar cu axa liniara adaugata k trece de 20. Recalcularea lui `zl`
    in interiorul buclei ar fi de mii de ori mai scumpa fara nicio cifra in plus, si a fost singurul
    lucru care facea enumerarea completa impracticabila."""
    langs = sorted(ref["lang"].unique())
    M = {lg: (ref["lang"] == lg).values for lg in langs}
    Z = {k: {lg: zl(F[k][col].values[M[lg]]) for lg in langs} for k in F}
    Y = {lg: ref["complexity"].values[M[lg]] for lg in langs}
    return langs, Z, Y


def r_ansamblu(membri, Z, Y, langs):
    """r al mediei standardizate in interiorul limbii, per limba."""
    out = {}
    for lg in langs:
        s = Z[membri[0]][lg].copy()
        for k in membri[1:]:
            s = s + Z[k][lg]
        out[lg] = pearsonr(s, Y[lg])[0]
    return out


def r_mediu(membri, Z, Y, langs):
    return float(np.mean(list(r_ansamblu(tuple(membri), Z, Y, langs).values())))


def rho_matrice(F, ref, col):
    ks = list(F)
    M = pd.DataFrame(np.eye(len(ks)), index=ks, columns=ks)
    for a, b in itertools.combinations(ks, 2):
        # `nanmean`, nu `mean`. Pe o limba cu predictie constanta (vezi `zl` si `degenerate`)
        # `pearsonr` intoarce corect `nan`, fiindca rho nu e definit acolo, iar o singura valoare de
        # asta ar otravi media si ar face intreaga linie ilizibila. Se mediaza limbile pe care rho
        # EXISTA, iar cazurile lipsa sunt listate in sectiunea de predictii degenerate.
        v = np.nanmean([pearsonr(F[a][col].values[(ref["lang"] == lg).values],
                                 F[b][col].values[(ref["lang"] == lg).values])[0]
                        for lg in sorted(ref["lang"].unique())])
        M.loc[a, b] = M.loc[b, a] = v
    return M


def rho_max(r_membri, rho_sum, r3, tinta):
    """rho mediu maxim fata de membrii existenti, ca ansamblul de k+1 sa atinga `tinta`."""
    k = len(r_membri)
    den = ((sum(r_membri) + r3) / tinta) ** 2
    return (den - (k + 1) - 2 * rho_sum) / (2 * k)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--col", default=COL)
    ap.add_argument("--spatiu", default="",
                    help="prefixul de spatiu, ex. `_tf-proj-200`. Gol = embeddingul plin.")
    ap.add_argument("--out", default=None)
    ap.add_argument("--extra", action="append", default=None, metavar="NUME=CALE",
                    help="membru dintr-un ALT spatiu decat `--spatiu`, repetabil. Pentru ruta "
                         "hibrida: liniarul si arborii pe embeddingul plin, TabFM din `proj-394`. "
                         "Randurile se verifica pe cvintetul `split, idx, lang, token, context_id`.")
    ap.add_argument("--membri", default=None,
                    help="lista, separata prin virgula, a candidatilor care intra in enumerarea de "
                         "submultimi. Fara ea intra toti, si cu grila de alpha pe disc capul "
                         "tabelului se umple de combinatii `ridge-a30+ridge-a100` fara sens.")
    ap.add_argument("--max-k", dest="max_k", type=int, default=3,
                    help="dimensiunea maxima a unei submultimi enumerate. Implicit 3, fiindca "
                         "enumerarea e 2^k si cu grila de alpha pe disc k trece de 20, adica un "
                         "milion de submultimi si ore de calcul pentru combinatii care oricum n-au "
                         "sens (`ridge-a30+ridge-a100`). `0` inseamna toate, si atunci se cere "
                         "explicit `--membri` daca ar ieși prea multe.")
    ap.add_argument("--top", type=int, default=25,
                    help="cate submultimi se tiparesc. Enumerarea e 2^k si se calculeaza intreaga; "
                         "asta taie numai LISTAREA, iar cate au fost lasate afara se spune explicit.")
    a = ap.parse_args(argv)
    if a.out is None:
        a.out = os.path.join(OUT, f"e_regresor_a{a.spatiu.replace('_tf-', '_')}.md")
    extra = {}
    for spec in (a.extra or []):
        if "=" not in spec:
            sys.exit(f"--extra vrea NUME=CALE, am primit {spec!r}")
        nume, cale = spec.split("=", 1)
        extra[nume] = cale if os.path.isabs(cale) else os.path.join(HERE, cale)

    F, ref = incarca(a.col, a.spatiu, extra)
    langs, Z, Y = pregatire(F, ref, a.col)
    L = ["# Axa regresorului pe semnalul A", "",
         "Generat de `analysis_regresor.py`. Coloana `%s`, splitul test, encoder xlmr, "
         "configuratia `--lemma-freq --afeat fert_inloc`%s." % (
             a.col, f", spatiu `{a.spatiu.lstrip('_')}`" if a.spatiu else ", embedding plin"), "",
         "Toate cifrele vin din predictiile de pe disc. Bratul B nu intra nicaieri: aici se masoara "
         "numai A.", ""]
    if extra:
        L += ["Membri adusi din alt spatiu cu `--extra`, cu randurile verificate pe cvintetul "
              "`split, idx, lang, token, context_id`:", "", "```"]
        L += [f"  {k:12s} {os.path.relpath(v, HERE)}" for k, v in extra.items()]
        L += ["```", ""]

    deg = degenerate(F, ref, a.col)
    if deg:
        L += ["## Predictii degenerate", "",
              "Candidati care dau o predictie CONSTANTA pe o limba, deci `r` nu e definit acolo si "
              "standardizarea ar da `inf`. Se trateaza ca zero, adica media limbii, exact conventia "
              "lui `fuse_ab.zscore`. Pe limba respectiva ansamblul e deci partenerul SINGUR, si "
              "cifrele care il includ trebuie citite cu asta in minte.", "", "```"]
        L += [f"  {k:16s} {lg:4s}  {n} valoare unica pe {lg}" for k, lg, n in deg]
        L += ["```", "",
              "Mecanismul, cand candidatul e `lasso` cu alpha mare: penalizarea L1 zeroeste TOTI "
              "coeficientii si ramane doar interceptul. Nu e o eroare numerica, e regresorul care "
              "renunta.", ""]

    # ---------------------------------------------------------------- 1. r per limba, per regresor
    T = pd.DataFrame({k: r_pe_limbi(d, ref, a.col) for k, d in F.items()})
    T.loc["MEDIE"] = T.mean()
    if "blend" in T.columns:
        T = T[["blend"] + [c for c in T.columns if c != "blend"]]
    L += ["## r pe test, per limba", "", "```", T.round(4).to_string(), "```", ""]
    if "blend" in T.columns:
        d = (T.loc["MEDIE"] - T.loc["MEDIE", "blend"]).drop("blend")
        L += ["Fata de incumbentul `blend` (Ridge300 + HGB), pe medie:", "", "```"]
        L += [f"  {k:12s} {v:+.4f}" for k, v in d.sort_values(ascending=False).items()]
        L += ["```", ""]

    # ------------------------------------------------------------------------------ 2. matricea rho
    M = rho_matrice(F, ref, a.col)
    L += ["## rho intre estimatori, mediat pe limbi", "", "```", M.round(3).to_string(), "```", ""]

    # ------------------------------------------- 3. toate ansamblurile, plus verificarea identitatii
    baza = [k for k in F if k not in ("blend", "blend-et", "blend-lasso")]     # `blend` e deja un ansamblu
    if a.membri:
        cerut = [x.strip() for x in a.membri.split(",") if x.strip()]
        lipsa = [x for x in cerut if x not in F]
        if lipsa:
            sys.exit(f"--membri: {', '.join(lipsa)} nu sunt pe disc. Existente: {', '.join(F)}")
        baza = [k for k in cerut if k not in ("blend", "blend-et", "blend-lasso")]
    L += ["## r al mediei standardizate, pe toate submultimile estimatorilor de baza", "",
          "`blend` si `blend-et` sunt excluse din combinatii: sunt ele insele medii, deci ar intra "
          "de doua ori.", ""]
    if a.membri:
        L += [f"Restrans cu `--membri` la {len(baza)} estimatori: `{'`, `'.join(baza)}`.", ""]
    kmax = len(baza) if a.max_k <= 0 else min(a.max_k, len(baza))
    # Garda de cost. 2^k creste mai repede decat rabdarea: la k=20 sunt un milion de submultimi si
    # ~10 milioane de apeluri `pearsonr`, adica ore. A picat o data exact asa. Se refuza inainte de a
    # incepe, cu ce anume sa dai ca sa treaca, in loc sa se atarne.
    n_comb = sum(math.comb(len(baza), k) for k in range(1, kmax + 1))
    if n_comb > 200000:
        sys.exit(f"enumerarea ar avea {n_comb} submultimi din {len(baza)} estimatori (max-k {kmax}). "
                 f"Da `--max-k 3` sau restrange cu `--membri`.")
    if kmax < len(baza):
        L += [f"Enumerate submultimile de pana la **{kmax}** membri ({n_comb} din "
              f"{2**len(baza) - 1} posibile). Motivul e cost, dar si sens: cu grila de alpha pe disc, "
              f"combinatiile mari sunt in majoritate doua puncte ale ACELEIASI familii puse "
              f"impreuna, ceea ce nu e un ansamblu de biasuri diferite.", ""]
    L += ["```"]
    rez, rez_lg = {}, {}
    for k in range(1, kmax + 1):
        for c in itertools.combinations(baza, k):
            # r PE LIMBA se pastreaza, nu doar media: fara el nu se poate face selectia
            # leave-one-language-out de la sectiunea de optimism, iar maximul pe test singur nu e
            # o cifra citabila.
            d = r_ansamblu(c, Z, Y, langs)
            rez_lg[c] = d
            rez[c] = float(np.mean(list(d.values())))
    ordonat = sorted(rez.items(), key=lambda kv: -kv[1])
    for c, v in ordonat[:a.top]:
        L.append(f"  {'+'.join(c):40s} {v:.6f}")
    L += ["```", ""]
    if len(ordonat) > a.top:
        L += [f"Calculate toate **{len(ordonat)}** submultimile, listate primele {a.top}. Cea mai "
              f"slaba e `{'+'.join(ordonat[-1][0])}` la {ordonat[-1][1]:.6f}.", ""]

    # ---------------------------------------------- 3b. OPTIMISMUL de selectie al ansamblului
    # Maximul peste mii de submultimi NU e o cifra citabila: e ales pe splitul pe care e raportat.
    # Proiectul a masurat deja tiparul o data, pe 23 de configuratii, si umflarea era +0.0019; aici
    # sunt cu trei ordine de marime mai multe submultimi, deci umflarea e mai mare, nu mai mica.
    #
    # Cifra onesta e selectia leave-one-language-out: pentru limba L se alege submultimea cu cel mai
    # bun r mediu pe CELELALTE noua, si se evalueaza pe L. Langa ea se pun latimea criteriului si de
    # cate ori argmaxul LOLO a nimerit optimul de test, fiindca regula transversala a proiectului e ca
    # un criteriu plat face argmaxul zgomot, si atunci se mediaza in loc sa se aleaga.
    if len(rez_lg) > 1:
        combos = list(rez_lg)
        alese, r_lolo, latimi, nimerit = {}, [], [], 0
        for lg in langs:
            crit = {c: float(np.mean([rez_lg[c][l2] for l2 in langs if l2 != lg])) for c in combos}
            best = max(combos, key=lambda c: crit[c])
            alese[lg] = best
            r_lolo.append(rez_lg[best][lg])
            v = list(crit.values())
            latimi.append(max(v) - min(v))
            nimerit += int(best == max(combos, key=lambda c: rez_lg[c][lg]))
        r_sel = float(np.mean(r_lolo))
        top = [c for c, _ in ordonat[:5]]
        # medierea celor cinci de sus, ca alternativa la a alege una singura
        membri_top = sorted({m for c in top for m in c})
        r_med5 = r_mediu(tuple(membri_top), Z, Y, langs)
        maxim = ordonat[0][1]
        L += ["## Optimismul de selectie al ansamblului", "",
              f"Maximul de mai sus e ales peste **{len(combos)}** submultimi, pe acelasi split pe care "
              f"e raportat, deci nu e o cifra citabila. Selectia onesta e leave-one-language-out.", "",
              "```",
              f"  maximul pe test                    {maxim:.6f}   ({'+'.join(ordonat[0][0])})",
              f"  selectie LOLO a submultimii        {r_sel:.6f}",
              f"  optimismul de selectie             {maxim - r_sel:+.6f}",
              f"  media membrilor din top 5          {r_med5:.6f}   ({'+'.join(membri_top)})",
              f"  controlul ridge+hgb                {r_mediu(('ridge', 'hgb'), Z, Y, langs):.6f}"
              if {"ridge", "hgb"} <= set(F) else "",
              f"  latimea criteriului                {float(np.mean(latimi)):.4f}",
              f"  LOLO a nimerit optimul de test     {nimerit}/{len(langs)} limbi", "```", ""]
        distincte = len(set(alese.values()))
        L += [f"Argmaxul LOLO alege **{distincte}** submultimi distincte peste cele {len(langs)} taieri. "
              + ("Deci sare de la o limba la alta, adica e in mare parte zgomot, si atunci regula "
                 "transversala a proiectului cere sa se MEDIEZE in loc sa se aleaga."
                 if distincte > len(langs) // 2 else
                 "Deci nu sare aproape deloc, si selectia chiar separa ceva.") , "",
              f"Cifra care se citeaza pentru un ansamblu nou e **{r_sel:.6f}** (selectie LOLO) sau "
              f"**{r_med5:.6f}** (medierea membrilor din top 5), nu {maxim:.6f}.", ""]
        L = [x for x in L if x is not None]

    # verificarea identitatii pe limba, pe perechea ridge+hgb daca exista
    if {"ridge", "hgb"} <= set(F):
        er = []
        for lg in langs:
            m = (ref["lang"] == lg).values
            y = ref["complexity"].values[m]
            r1 = pearsonr(F["ridge"][a.col].values[m], y)[0]
            r2 = pearsonr(F["hgb"][a.col].values[m], y)[0]
            rho = pearsonr(F["ridge"][a.col].values[m], F["hgb"][a.col].values[m])[0]
            mas = pearsonr(zl(F["ridge"][a.col].values[m]) + zl(F["hgb"][a.col].values[m]), y)[0]
            er.append(abs(mas - (r1 + r2) / np.sqrt(2 + 2 * rho)))
        L += [f"Identitatea de frontiera, verificata pe fiecare limba pentru `ridge+hgb`: "
              f"eroarea maxima **{max(er):.2e}**. Nu e o aproximare buna, e o identitate algebrica.",
              ""]

    # ----------------------------------------------------------------- 4. curba de prag pentru unul nou
    if {"ridge", "hgb"} <= set(F):
        r1 = T.loc["MEDIE", "ridge"]; r2 = T.loc["MEDIE", "hgb"]; rho12 = M.loc["ridge", "hgb"]
        base = (r1 + r2) / np.sqrt(2 + 2 * rho12)
        L += ["## Ce i-ar trebui unui al treilea estimator. Scris inainte de a-l cauta", "",
              f"Blend-ul de acum, prin frontiera: r_ridge {r1:.4f}, r_hgb {r2:.4f}, rho {rho12:.4f}, "
              f"deci **{base:.6f}**.", "",
              f"Bara pe fuziune e +{BARA:.4f}, iar factorul de transmisie A -> fuziune e "
              f"{FACTORI['optimist']:.3f} mediu si {FACTORI['pesimist']:.3f} marginal "
              f"(`e_frontiera_enc.md`). Deci blend-ul trebuie sa urce cu "
              f"+{BARA/FACTORI['optimist']:.4f} (optimist) pana la +{BARA/FACTORI['pesimist']:.4f} "
              f"(pesimist).", "",
              "rho mediu MAXIM admis fata de `ridge` si `hgb`:", "", "```",
              f"{'r3':>6}  {'rho max optimist':>18}  {'rho max pesimist':>18}"]
        for r3 in (0.35, 0.40, 0.45, 0.50, 0.55, 0.58, 0.62, 0.65):
            row = [f"{r3:6.3f}"]
            for et in ("optimist", "pesimist"):
                v = rho_max([r1, r2], rho12, r3, base + BARA / FACTORI[et])
                row.append(f"{'orice':>18}" if v >= 1 else f"{v:18.3f}")
            L.append("  ".join(row))
        L += ["```", ""]
        alti = [k for k in M.index if k not in ("ridge", "hgb", "blend", "blend-et")]
        if alti:
            L += ["Candidatii masurati, rho mediu fata de cei doi membri:", "", "```"]
            for k in alti:
                rm = 0.5 * (M.loc[k, "ridge"] + M.loc[k, "hgb"])
                pr = rho_max([r1, r2], rho12, T.loc["MEDIE", k], base + BARA / FACTORI["optimist"])
                L.append(f"  {k:12s} r {T.loc['MEDIE', k]:.4f}  rho {rm:.3f}  "
                         f"prag optimist {pr:.3f}  ->  {'TRECE' if rm <= pr else 'CADE'}")
            L += ["```", ""]

    # ------------------------------------------- 5. CELE TREI ROLURI in care poate intra un candidat
    # Poarta de la punctul 4 raspunde la "ce i-ar trebui unui al TREILEA membru". Pana pe 26 august,
    # acest fisier raspundea numai la o singura alta intrebare, "ce se intampla daca X ia locul
    # jumatatii LINIARE", fiindca sesiunea de atunci era despre liniari.
    #
    # Rolul schimba verdictul, si nu putin. Masurat pe `extratrees`, media pe 3 encodere: -0.0079 in
    # locul lui `ridge`, +0.0086 in locul lui `hgb`, +0.0080 ca al treilea. Adica un tabel cu un singur
    # rol arata cel mai bun al treilea membru masurat vreodata pe axa asta drept cel mai prost candidat
    # din tabel. Un arbore nou pus in locul jumatatii liniare lasa blend-ul cu DOI arbori si fara niciun
    # liniar, deci pierde exact decorelarea care da valoare blend-ului. De aici cele trei coloane.
    #
    # `slack` e aceeasi informatie ca `delta`, dar in unitati de rho si la r-ul candidatului: cat rho i-ar
    # fi PERMIS ca sa lege la egalitate, minus cat rho are. Pozitiv = candidatul e SUB curba de compromis.
    # E instrumentul cerut de intrebarea de research, care e formulata in rho la r comparabil, si nu are
    # niciun parametru potrivit: iese direct din identitatea de frontiera verificata mai sus la 1e-16.
    if {"ridge", "hgb"} <= set(F):
        ctrl = r_mediu(("ridge", "hgb"), Z, Y, langs)
        cand = [k for k in F if k not in ("blend", "blend-et", "blend-lasso", "ridge", "hgb")]
        L += ["## Cele trei roluri in care poate intra un candidat", "",
              f"Controlul e `ridge+hgb` = **{ctrl:.6f}** in toate trei rolurile, adica blend-ul de acum "
              f"scris ca media standardizata a celor doua jumatati ale lui.", "",
              "`in locul lui ridge` inlocuieste jumatatea LINIARA, `in locul lui hgb` pe cea de ARBORI, "
              "`al treilea` il adauga langa amandoua. Un candidat trebuie judecat in rolul care i se "
              "potriveste: un arbore pus in locul jumatatii liniare lasa blend-ul cu doi arbori si "
              "pierde chiar decorelarea care ii da valoare. Pe `extratrees` cele trei roluri dau "
              "-0.0079, +0.0086 si +0.0080, deci alegerea rolului muta verdictul cu 0.017.", "",
              f"De ce {ctrl:.6f} aici si {base:.6f} la punctul 4, pentru acelasi `ridge+hgb`. "
              f"Identitatea de frontiera e exacta PE LIMBA, si asta s-a verificat mai sus la ordinul "
              f"1e-16. Punctul 4 o aplica insa pe `r` si `rho` deja MEDIATE peste limbi, ca sa poata "
              f"desena o curba de prag cu un singur numar, iar media unei functii neliniare nu e "
              f"functia mediei: iese cu {base - ctrl:+.4f} pe langa. Cifrele `delta` de mai jos sunt "
              f"medii ale celor zece r pe limba, deci exacte; coloanele `slack` folosesc marimile "
              f"mediate si de aceea au ca referinta {base:.6f}, nu {ctrl:.6f}. Un decalaj constant pe "
              f"toate randurile nu atinge comparatia intre candidati sau intre clase.", "",
              f"`fuz.opt` e `delta` cea mai buna din cele trei roluri inmultita cu factorul de "
              f"transmisie optimist {FACTORI['optimist']:.3f}. Verdictul e fata de bara de "
              f"+{BARA:.4f} pe fuziune, deci un `CADE` e un cade si pe cea mai buna ipoteza.", "",
              "```",
              f"  {'candidat':18s} {'clasa':12s} {'r_A':>7} {'rho_ri':>7} {'rho_hgb':>7} "
              f"{'d_lin':>8} {'d_arb':>8} {'d_al3':>8} {'slack':>8} {'fuz.opt':>8}  verdict"]
        r1 = T.loc["MEDIE", "ridge"]; r2 = T.loc["MEDIE", "hgb"]; rho12 = M.loc["ridge", "hgb"]
        randuri = []
        for X in cand:
            rx = T.loc["MEDIE", X]
            d_lin = r_mediu((X, "hgb"), Z, Y, langs) - ctrl       # X in locul lui ridge
            d_arb = r_mediu(("ridge", X), Z, Y, langs) - ctrl     # X in locul lui hgb
            d_tri = r_mediu(("ridge", "hgb", X), Z, Y, langs) - ctrl
            # `slack` se raporteaza in rolul cu cel mai bun `delta`, adica in rolul in care candidatul
            # chiar ar fi folosit. Altfel un arbore ar fi judecat in rol de liniar si invers.
            rol = max((d_lin, "lin"), (d_arb, "arb"), (d_tri, "tri"))[1]
            if rol == "lin":
                sl = rho_max([r2], 0.0, rx, base) - M.loc[X, "hgb"]
            elif rol == "arb":
                sl = rho_max([r1], 0.0, rx, base) - M.loc[X, "ridge"]
            else:
                sl = rho_max([r1, r2], rho12, rx, base) - 0.5 * (M.loc[X, "ridge"] + M.loc[X, "hgb"])
            randuri.append((max(d_lin, d_arb, d_tri), X, rx, d_lin, d_arb, d_tri, sl, rol))
        for dmax, X, rx, d_lin, d_arb, d_tri, sl, rol in sorted(randuri, reverse=True):
            vd = "TRECE" if dmax * FACTORI["optimist"] >= BARA else "CADE"
            L.append(f"  {X:18s} {MECANISM.get(X, '?'):12s} {rx:7.4f} {M.loc[X, 'ridge']:7.3f} "
                     f"{M.loc[X, 'hgb']:7.3f} {d_lin:+8.4f} {d_arb:+8.4f} {d_tri:+8.4f} "
                     f"{sl:+8.4f} {dmax*FACTORI['optimist']:+8.4f}  {vd} ({rol})")
        L += ["```", "",
              f"Ca sa treaca bara, un candidat trebuie sa urce A cu +{BARA/FACTORI['optimist']:.4f} "
              f"(optimist) pana la +{BARA/FACTORI['pesimist']:.4f} (pesimist). Cifra care decide e "
              f"`rho`, nu `r`: un candidat cu r mai bun dar rho mai mare pierde, si s-a intamplat de "
              f"trei ori in proiect.", ""]

        # ------------------------------------------------- 5b. media pe CLASA DE MECANISM
        # Sectiunea care raspunde la intrebarea de research, si singura din fisier a carei valoare
        # atarna de faptul ca apartenenta la clasa a fost scrisa INAINTE de rulari.
        cls = {}
        for dmax, X, rx, d_lin, d_arb, d_tri, sl, rol in randuri:
            cls.setdefault(MECANISM.get(X, "?"), []).append((X, rx, sl, dmax))
        L += ["## Media pe clasa de mecanism. Intrebarea de research", "",
              "Intrebarea nu e care candidat e cel mai bun, e daca schimbarea OBIECTIVULUI coboara `rho` "
              "sistematic la `r` comparabil, fata de schimbarea formei functiei. Clasele sunt scrise in "
              "`output/_predictii_obiectiv.md` inainte de orice rulare a sesiunii, tocmai ca sa nu se "
              "poata muta un candidat in clasa care il avantajeaza dupa ce i se vede cifra.", "",
              "`REGULARIZARE` e norul de referinta: pierdere patratica, liniar dens, numai penalizarea "
              "variaza. `slack` pozitiv inseamna sub curba de compromis, adica `rho` mai mic decat i-ar "
              "fi fost permis la `r`-ul lui.", "", "```",
              f"  {'clasa':14s} {'n':>3} {'slack mediu':>12} {'slack median':>13} {'r_A mediu':>10} "
              f"{'cel mai bun delta':>18}"]
        for c in ORDINE_M:
            v = cls.get(c)
            if not v:
                continue
            sl = np.array([x[2] for x in v]); rr = np.array([x[1] for x in v])
            bst = max(v, key=lambda x: x[3])
            L.append(f"  {c:14s} {len(v):3d} {sl.mean():+12.4f} {float(np.median(sl)):+13.4f} "
                     f"{rr.mean():10.4f} {bst[3]:+9.4f} ({bst[0]})")
        L += ["```", ""]
        obiectiv = [c for c in ("LOSS", "TINTA", "INCADRARE") if c in cls]
        if obiectiv and "FAMILIE" in cls:
            so = np.concatenate([[x[2] for x in cls[c]] for c in obiectiv])
            sf = np.array([x[2] for x in cls["FAMILIE"]])
            L += [f"Diferenta care raspunde direct: clasele care schimba OBIECTIVUL (`"
                  + "`, `".join(obiectiv) + f"`, n={len(so)}) au slack mediu **{so.mean():+.4f}**, iar "
                  f"clasa `FAMILIE` (n={len(sf)}) **{sf.mean():+.4f}**. Diferenta e "
                  f"**{so.mean()-sf.mean():+.4f}**.", ""]

    # ------------------------------------------------ 6. grila parametrica, aleasa LEAVE-ONE-LANGUAGE-OUT
    # Regula transversala a proiectului: cand latimea criteriului de selectie e mult mai mica decat
    # latimea efectului, argmaxul e zgomot si atunci se MEDIAZA. Deci pentru fiecare familie se
    # tiparesc trei lucruri langa: punctul ales LOLO, media predictiilor intregii grile, si cel mai
    # bun punct fix - care e selectie PE TEST si e acolo doar ca plafon, nu ca variantă de rulat.
    for nume, grila in FAMILII.items():
        pe_disc = [(n, v) for n, v in grila if n in F]
        if len(pe_disc) < 2:
            continue
        nume_g = [n for n, _ in pe_disc]
        # criteriul: r mediu al candidatului pe cele NOUA limbi de potrivire, adica fara L
        crit = {n: {lg: float(np.mean([T.loc[l2, n] for l2 in langs if l2 != lg])) for lg in langs}
                for n in nume_g}
        alese, r_lolo, latimi, nimerit = {}, [], [], 0
        for lg in langs:
            best = max(nume_g, key=lambda n: crit[n][lg])
            alese[lg] = best
            r_lolo.append(T.loc[lg, best])
            vals = [crit[n][lg] for n in nume_g]
            latimi.append(max(vals) - min(vals))
            nimerit += int(best == max(nume_g, key=lambda n: T.loc[lg, n]))
        r_sel = float(np.mean(r_lolo))
        r_med = r_mediu(tuple(nume_g), Z, Y, langs)
        fix = {n: T.loc["MEDIE", n] for n in nume_g}
        best_fix = max(fix, key=fix.get)
        L += [f"## Grila `{nume}`, aleasa leave-one-language-out", "", "```",
              f"  {'punct':14s} {'parametru':>10} {'r_A':>8}"]
        for n, v in pe_disc:
            L.append(f"  {n:14s} {v:10g} {fix[n]:8.4f}" + ("   <- cel mai bun pe test" if n == best_fix else ""))
        L += ["```", "", "```",
              f"  selectie LOLO                {r_sel:.6f}",
              f"  media predictiilor grilei    {r_med:.6f}",
              f"  cel mai bun punct fix        {fix[best_fix]:.6f}   ({best_fix}, dar e ales PE TEST)",
              f"  latimea criteriului          {float(np.mean(latimi)):.4f}",
              f"  LOLO a nimerit optimul       {nimerit}/{len(langs)} limbi", "```", "",
              f"Punctul ales per limba: " + ", ".join(f"{lg}={alese[lg]}" for lg in langs) + ".", ""]
        unanim = len(set(alese.values())) == 1
        if unanim:
            u = next(iter(alese.values()))
            L += [f"**Criteriul e UNANIM**: toate cele {len(langs)} taieri LOLO aleg `{u}`. Deci aici "
                  f"nu e o selectie per limba, e o SINGURA valoare globala de hiperparametru, "
                  f"estimata din limbile de potrivire. Doua consecinte care conteaza pentru cum se "
                  f"citeste cifra:", "",
                  f"- regula `criteriu plat -> mediaza` nu se aplica: ea e despre cazul in care "
                  f"argmaxul SARE de la o limba la alta, adica despre zgomot in ordine. Aici nu sare "
                  f"deloc.",
                  f"- `cel mai bun punct fix` iese acelasi lucru cu selectia LOLO, dar NU fiindca s-ar "
                  f"fi ales pe test: alegerea s-a facut pe celelalte noua limbi si a nimerit peste. "
                  f"Coincidenta e un semn bun, nu o scurgere.", ""]
            if r_med < r_sel:
                L += [f"Medierea grilei iese cu {r_med - r_sel:+.6f} sub punctul unic, ceea ce e de "
                      f"asteptat: grila contine si puncte clar proaste, iar medierea le tine pe toate "
                      f"cu pondere egala. Medierea e raspunsul cand nu se poate ALEGE, nu cand se "
                      f"poate.", ""]
        elif r_med >= r_sel:
            L += [f"Medierea bate selectia cu {r_med - r_sel:+.6f}. Tiparul cunoscut: criteriul e plat "
                  f"({float(np.mean(latimi)):.4f}) si argmaxul sare intre limbi "
                  f"({len(set(alese.values()))} puncte distincte alese), deci e in mare parte zgomot.",
                  ""]
        else:
            L += [f"Selectia bate medierea cu {r_sel - r_med:+.6f}, cu "
                  f"{len(set(alese.values()))} puncte distincte alese peste limbi. Merita privit "
                  f"inainte de a fi crezut: e cazul in care selectia chiar separa.", ""]
        # Optimul la MARGINEA grilei nu e un optim, e o grila prea scurta.
        capete = (pe_disc[0][0], pe_disc[-1][0])
        if best_fix in capete:
            L += [f"**`{best_fix}` e la marginea grilei.** Cifra lui nu e un optim, e cel mai departe "
                  f"unde s-a privit. Grila trebuie prelungita in acea directie inainte ca valoarea sa "
                  f"fie citita ca maxim.", ""]

    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
