"""Fuziunea semnalului A cu semnalul B, cu ponderi alese leave-one-language-out.

Niciuna din cifrele de pana acum nu e sistemul final. A singur e bratul inghetat, r mediu 0.552 pe
test. B singur e nota LLM. Aici se pun impreuna, si aici se vede daca trecem de 0.657.

  A = predictia bratului inghetat EN + MLSP∖L, din `output/e1_frozen_preds.csv` (`--frozentrial`)
  B = nota LLM, din `output/bakeoff_<model>.csv` (trial) si `output/bakeoff_test/<model>.csv` (test)
  C nu intra: r mediu intre -0.080 si +0.072 pe 7 modele, cu semnul schimbandu-se intre limbi.

Protocolul, si e acelasi §5.1 aplicat inca o data, la al treilea nivel de alegere:

  1. Per limba, ambele semnale se standardizeaza in interiorul limbii, fara etichete. r e invariant la
     transformari afine, deci standardizarea nu schimba nimic pentru A singur sau B singur; conteaza
     doar in amestec, unde pune cele doua scale in acelasi spatiu.
  2. p = w·z_A + (1−w)·z_B, cu w pe grila 0, 0.05, ..., 1.
  3. Pentru limba L, w*(L) e argmaxul lui r mediu peste CELELALTE 9 limbi, pe splitul de potrivire.
  4. w*(L) se aplica randurilor de TEST ale lui L.

Ponderea nu vede niciodata limba L.

`--fit` alege splitul de potrivire, si asta e singura intrebare noua la care raspunde fisierul.
Implicit `trial`, adica protocolul de pana acum. `test` potriveste w pe randurile de TEST ale celorlalte
9 limbi, adica pe exact protocolul pe care il foloseste DEJA bratul A: la `finetune_xlmr.py:446`,
`Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` peste randurile de test. Cele doua componente
ale aceluiasi sistem foloseau splituri diferite fara motiv, iar `e_split_gap.md` arata ca trial-ul
supraestimeaza semnalul B cu 0.191, deci w acorda sistematic prea putin lui A. `both` calculeaza ambele
si scrie raportul de comparatie, cu intervale PERECHE.

Nici la `--fit test` limba L nu e folosita nicaieri: nici trial, nici test, nici la alegerea modelului,
nici la potrivirea ponderii. Zero etichete in limba tinta. Garantiile, linie cu linie, sunt in raport.

Bratul B poate fi un model fix (`--arm qwen3-8b-4bit`) sau harta selectata LOLO (`--arm lolo`). La
`lolo`, selectia modelului pentru limbile de potrivire a ponderii e NESTED: modelul pentru limba L' se
alege excluzand si pe L, si pe L'. Altfel w(L) ar depinde indirect de splitul de selectie al lui L,
prin modelul ales pentru L', care s-ar fi ales folosind si randurile lui L.

`--pick-split` alege splitul pe care se selecteaza modelul lui B, si e a treia intrebare noua la care
raspunde fisierul. Implicit `trial`, adica tot ce e publicat reproduce fara niciun flag. `test` face
selectia pe randurile de TEST ale celorlalte 9 limbi, exact ca w sub `--fit test` si exact ca
antrenarea bratului A. Pana acum modelul se alegea pe trial in timp ce w se potrivea pe test, adica
exact asimetria pe care paragraful de mai sus o condamna cand motiveaza `--fit test`: motivul a fost
eliminat pentru w si a ramas pentru model. Limba L nu intra nici asa nicaieri, la niciun nivel:
`pick_model` o exclude chiar ea, iar selectia imbricata a limbilor de potrivire foloseste ACELASI
tabel, deci nu se deschide o scurgere noua pe unde s-a inchis una veche. O selectie recalculata pe
testul lui L ar fi tuning pe scorul raportat; asta nu e, si distincta trebuie tinuta curata.
Filtrul de disponibilitate ramane pe splitul de EVALUARE, fiindca e o constatare de acoperire, nu o
alegere pe scor. Pe test bazinul are efectiv doi candidati din trei, `qwen35-9b-8bit` fiind rulat
acolo doar pe franceza, iar limitarea se scrie in raport.

`--ens` schimba semnalul A, si e a doua intrebare noua la care raspunde fisierul. Cele doua brate de
transfer existau deja amandoua in fisierul de predictii: `p_en`, antrenat NUMAI pe CompLex EN, si
`p_multi`, antrenat pe CompLex EN plus testul celorlalte noua limbi. Pana acum fuziunea folosea doar
al doilea. Cu `--ens`, A devine `z(w_src·z(p_en) + (1−w_src)·z(p_multi))`, iar `w_src` trece prin
exact aceeasi selectie leave-one-language-out prin care trece w. `--a-set` adauga al treilea lucru de
ales, setul de trasaturi al lui A. Amandoua cer `--tag`, deci scriu pe cai proprii si nu ating nimic
din ce e publicat.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python fuse_ab.py --arm qwen3-8b-4bit
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python fuse_ab.py --arm lolo --fit both
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python fuse_ab.py --arm lolo --fit test \
      --ens --tag ens --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv \
      --vs output/fusion_preds_lolo_fittest_lemma.csv
"""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
PREDS_A = os.path.join(OUT, "e1_frozen_preds.csv")
# Raportul si predictiile sunt per BRAT: rulate una dupa alta, o cale fixa ar sterge tacut rezultatul
# bratului precedent.
REPORT = os.path.join(OUT, "e_fusion_{arm}{suf}.md")
PREDS_OUT = os.path.join(OUT, "fusion_preds_{arm}{suf}.csv")
TABLE = os.path.join(OUT, "fusion_{arm}{suf}.csv")
CMP_REPORT = os.path.join(OUT, "e_fusion_{arm}_fitcmp.md")
CMP_TABLE = os.path.join(OUT, "fusion_{arm}_fitcmp.csv")
SUMMARY = os.path.join(OUT, "e_fusion_fitcmp.md")
# Configuratiile cu ansamblu de surse scriu pe cai proprii, cu `--tag`, ca sa nu intre in mașinaria
# de sufixe a lui SUF si sa nu atinga nimic din ce e publicat.
ENS_REPORT = os.path.join(OUT, "e_fusion_{arm}_{tag}.md")
ENS_PREDS = os.path.join(OUT, "fusion_preds_{arm}_{tag}.csv")
ENS_TABLE = os.path.join(OUT, "fusion_{arm}_{tag}.csv")
GRID = np.round(np.arange(0.0, 1.0001, 0.05), 2)
# Grila ponderii dintre cele doua surse ale semnalului A. Mai groasa decat a lui w fiindca alegerea e
# imbricata sub ea, deci fiecare punct costa o selectie intreaga de w.
SRC_GRID = np.round(np.arange(0.0, 1.0001, 0.125), 3)
# {nume: cale} pentru sursele semnalului A. Un singur set, pe PREDS_A, e comportamentul de pana acum.
A_SETS = {}

# Sufixul de fisier per split de potrivire. Potrivirea pe trial scrie unde scria si inainte, deci
# rezultatele etapei 2 nu se pierd si reproducerea lor e verificabila cu `cmp`.
SUF = {"trial": "", "test": "_fittest"}
BARA = {"baseline frecventa": 0.4775, "Archaeology": 0.4864, "TMU-HIT": 0.6538,
        "G-Eval cu GPT-4o": 0.6571}

# Cache pe split pentru CSV-urile de bake-off deja imbogatite cu `context_id`. La `--arm lolo --fit
# both` setul de potrivire se reincarca o data per limba tinuta deoparte si per split, adica de 20 de
# ori aceleasi fisiere plus 20 de apeluri `load_mlsp`. Cache-ul nu atinge nicio cifra.
_RUNS = {}

# Cazurile in care filtrul de disponibilitate a schimbat modelul ales. Se aduna, nu se tipareste pe loc:
# aceeasi pereche apare de mai multe ori, si oricum trebuie sa ajunga in raport, nu doar pe ecran.
_POOL_FALLBACK = {}


_A_FRAMES = {}

# Directorul din care se citesc CSV-urile semnalului B, cand nu e cel canonic al splitului. Setat
# numai de `--b-dir`. None inseamna comportamentul de pana acum, deci cifra publicata nu depinde de
# existenta variabilei astea.
B_DIR = None

# PONDEREA PER ITEM. Implicit un singur punct, `a = 0`, adica ponderea scalara de pana acum, si
# atunci `fit_choice` merge pe ramura cu forma inchisa `_r_mom`, neatinsa. Cu grila largita,
# `w_i = clip(w + a*h_i, 0, 1)`, unde `h` e o marime observabila per item standardizata in interiorul
# limbii. Forma inchisa NU se mai poate folosi acolo: ea presupune w constant peste itemi, iar aici
# amestecul difera de la un rand la altul, deci Pearson se calculeaza direct, vectorizat peste grila.
A_GRID = np.array([0.0])
# {idx: h}, umplut de `--h-src`. None inseamna h identic nul, deci ramura de pondere per item nu se
# poate activa din greseala fara sursa.
H_MAP = None
H_NUME = ""


def a_frames(split):
    """{nume set: cadrul de predictii A al splitului}, citit o singura data per set.

    Seturile sunt variantele de trasaturi ale semnalului A, scrise de `finetune_xlmr.py --afeat`.
    Fiecare aduce DOUA brate: `p_en`, antrenat numai pe CompLex EN, si `p_multi`, antrenat pe CompLex
    EN plus testul celorlalte noua limbi.
    """
    if split not in _A_FRAMES:
        out = {}
        for name, path in A_SETS.items():
            d = pd.read_csv(path)
            d = d[d["split"] == split]
            if d.empty:
                raise SystemExit(f"{path} n-are randuri de {split}. Ruleaza intai "
                                 "finetune_xlmr.py --frozentrial")
            miss = [c for c in ("p_en", "p_multi") if c not in d.columns]
            if miss:
                raise SystemExit(f"{path} n-are coloanele {miss}")
            out[name] = d
        _A_FRAMES[split] = out
    return _A_FRAMES[split]


def runs_for(split):
    """CSV-urile de bake-off ale splitului, cu `context_id` si `idx`, citite o singura data.

    `B_DIR`, cand e setat, se aplica numai splitului de TEST: variantele masurate ale semnalului B se
    scriu pe test, iar trial-ul ramane cel canonic, ca harta de selectie sa nu se mute din greseala.
    """
    if split not in _RUNS:
        from bakeoff_trial import load_runs, with_context
        d = B_DIR if (B_DIR and split == "test") else None
        _RUNS[split] = {k: with_context(df, split) for k, df in load_runs(split, d).items()}
    return _RUNS[split]


def zscore(v):
    """Standardizare in interiorul limbii. NaN devine 0, adica media: un item fara semnal nu trage
    predictia intr-o directie, o lasa pe seama celuilalt semnal."""
    v = np.asarray(v, float)
    m = np.isfinite(v)
    if m.sum() < 2 or np.std(v[m]) == 0:
        return np.zeros(len(v))
    z = np.zeros(len(v))
    z[m] = (v[m] - v[m].mean()) / v[m].std()
    return z


def load_signals(arm, split, tab_pick=None, exclude=()):
    """{limba: DataFrame cu y, zA, zB, context_id} pentru splitul dat.

    `arm` e o cheie de model sau "lolo". La "lolo", modelul limbii se alege din `tab_pick`, tabelul
    de r al splitului de SELECTIE, excluzand limbile din `exclude` plus limba insasi. Splitul de
    selectie e cel al lui `--pick-split`, si nu e neaparat `split`, care e splitul de pe care se
    citesc randurile.
    """
    a = a_frames(split)[next(iter(A_SETS))]     # primul set da grila de limbi si coloana A de baza
    runs = runs_for(split)
    if not runs:
        raise SystemExit(f"niciun CSV de bake-off pentru splitul {split}")

    out = {}
    for lg, ga in a.groupby("lang", sort=True):
        key = arm
        if arm == "lolo":
            # Pool-ul de candidati: doar modelele masurate EFECTIV pe limba asta, pe splitul asta. Fara
            # filtru, la potrivirea pe test cu fr tinuta deoparte selectia ar cere `qwen35-9b-8bit` pe
            # sapte limbi de potrivire, model rulat pe test doar pe franceza, iar cele sapte limbi ar
            # cadea TACIT din setul de potrivire. Pe trial filtrul e no-op, toate cele 7 modele au toate
            # cele 10 limbi, deci potrivirea pe trial ramane bit cu bit ce era. Filtrul se uita la
            # splitul incarcat AICI, nu la cel de selectie: cu `--pick-split test` se schimba tabelul
            # din care se alege, nu bazinul din care se poate alege.
            pool = {k for k, df in runs.items() if (df["lang"].astype(str) == lg).any()}
            key = pick_model(tab_pick, set(exclude) | {lg}, pool=pool)
            free = pick_model(tab_pick, set(exclude) | {lg})
            if key != free:
                _POOL_FALLBACK[(split, tuple(sorted(exclude)), lg)] = (free, key)
        if key not in runs:
            continue
        gb = runs[key]
        gb = gb[gb["lang"] == lg]
        if gb.empty:
            continue
        m = ga.merge(gb[["idx", "B"]], on="idx", how="inner")   # cheia e pozitia in cadrul nefiltrat
        if m.empty:
            continue
        cols = {"lang": lg, "model": key, "idx": m["idx"].values,
                "y": m["complexity"].values, "ctx": m["context_id"].values,
                "A": m["p_multi"].values, "B": m["B"].values,
                "zA": zscore(m["p_multi"].values), "zB": zscore(m["B"].values)}
        # `h` se standardizeaza in interiorul limbii, ca `zA` si `zB`: altfel grila lui `a` ar
        # insemna altceva de la o limba la alta si un singur `a` n-ar putea fi ales pentru toate.
        if H_MAP is None:
            cols["h"] = np.zeros(len(m))
        else:
            hv = np.array([H_MAP.get(int(i), np.nan) for i in m["idx"].values], float)
            if not np.isfinite(hv).all():
                raise SystemExit(f"sursa lui h n-acopera {int((~np.isfinite(hv)).sum())} randuri "
                                 f"din {lg} pe splitul {split}")
            cols["h"] = zscore(hv)
        # Celelalte seturi de trasaturi, aliniate pe `idx`, adica pe pozitia in cadrul nefiltrat.
        # `reindex` in loc de merge: pastreaza ordinea lui `m` si lasa NaN unde lipseste un rand, iar
        # NaN-ul e prins imediat, nu propagat tacit intr-o corelatie.
        for name, fr in a_frames(split).items():
            g2 = fr[fr["lang"] == lg].drop_duplicates("idx").set_index("idx")
            for src, pre in (("p_en", "pe"), ("p_multi", "pm")):
                v = g2[src].reindex(m["idx"].values).values
                if not np.isfinite(v).all():
                    raise SystemExit(f"setul {name!r} n-acopera {int((~np.isfinite(v)).sum())} "
                                     f"randuri din {lg} pe splitul {split}")
                cols[f"{pre}_{name}"] = v
        out[lg] = pd.DataFrame(cols)
    return out


def pick_model(tab, exclude, pool=None):
    """Modelul cu cel mai bun r mediu peste limbile din afara lui `exclude`. §5.1.

    `pool` restrange candidatii la modelele care au masuratori pe limba pentru care se alege, pe splitul
    curent. Restrangerea nu foloseste nicio eticheta: e o constatare de acoperire, nu o alegere pe scor.
    """
    best, best_mean = None, -np.inf
    langs = sorted({l for per in tab.values() for l in per})
    for key, per in tab.items():
        if pool is not None and key not in pool:
            continue
        vals = [per[l][0] for l in langs if l not in exclude and l in per and np.isfinite(per[l][0])]
        if not vals:
            continue
        m = float(np.mean(vals))
        if m > best_mean:
            best, best_mean = key, m
    return best


def r_at(d, w):
    from bakeoff_trial import pearson
    return pearson(w * d["zA"].values + (1 - w) * d["zB"].values, d["y"].values)[0]


def fit_weight(arm, fit_split, lg, tab_pick, base):
    """w pentru limba L, potrivit pe CELELALTE limbi ale splitului `fit_split`.

    Singurul loc unde limba L e tinuta deoparte la potrivirea ponderii e filtrul `l2 != lg` de mai jos.
    La bratul LOLO, modelul limbii de potrivire se re-alege excluzand si pe L, si pe L': altfel w(L) ar
    vedea limba L prin usa din spate, prin modelul ales pentru L'.
    """
    fit = base[fit_split] if arm != "lolo" else load_signals(arm, fit_split, tab_pick, exclude={lg})
    others = [d for l2, d in fit.items() if l2 != lg]
    if not others:
        return None
    curve = [float(np.mean([r_at(d, w) for d in others])) for w in GRID]
    return {"w": float(GRID[int(np.argmax(curve))]), "curve": curve,
            "n_langs": len(others), "n_items": int(sum(len(d) for d in others)),
            "langs": sorted(l2 for l2 in fit if l2 != lg)}


def zA_of(d, aset, w_src):
    """Semnalul A al unei limbi, standardizat in interiorul ei, pentru un set si o pondere de surse.

    `w_src = 0` intoarce exact `zscore(p_multi)`, adica bratul de pana acum, bit cu bit. Trecerea prin
    formula generala ar da acelasi numar matematic, prin dubla standardizare, dar nu aceiasi biti, iar
    poarta de reproducere se uita la biti. `w_src = 1` e bratul EN-only singur.
    """
    pm = d[f"pm_{aset}"].values
    if w_src == 0.0:
        return zscore(pm)
    return zscore(w_src * zscore(d[f"pe_{aset}"].values) + (1 - w_src) * zscore(pm))


def _moments(zA, zB, y):
    """Cele sase momente din care r-ul amestecului iese EXACT, pentru orice w.

    Selectia are trei niveluri imbricate, deci grila se parcurge de sute de mii de ori. Pentru
    r = corr(w·a + (1−w)·b, y):

      numarator = w·cov(a,y) + (1−w)·cov(b,y)
      numitor   = sqrt(w²·var(a) + (1−w)²·var(b) + 2w(1−w)·cov(a,b)) · sd(y)

    Nu e o aproximare, e aceeasi cantitate rearanjata. Singura precondtie e sa nu existe valori
    nefinite care ar activa masca lui `bakeoff_trial.pearson`, iar `zscore` duce orice NaN in 0, deci
    nu exista. `_check_moments` verifica egalitatea pe date reale inainte de orice cifra.
    """
    a = np.asarray(zA, float); b = np.asarray(zB, float); y = np.asarray(y, float)
    a = a - a.mean(); b = b - b.mean(); y = y - y.mean()
    k = 1.0 / len(y)
    return (float(a @ y) * k, float(b @ y) * k, float(a @ a) * k, float(b @ b) * k,
            float(a @ b) * k, float(np.sqrt(float(y @ y) * k)))


def _r_mom(M, w):
    cay, cby, va, vb, cab, sy = M
    den = w * w * va + (1 - w) * (1 - w) * vb + 2 * w * (1 - w) * cab
    if den <= 0 or sy <= 0:
        return float("nan")
    return (w * cay + (1 - w) * cby) / (np.sqrt(den) * sy)


def h_from_dist(kind, path, seed=0):
    """{idx: h} dintr-un CSV de distributii, pentru ponderea per item. -> (harta, descriere)

    Temperatura la care se citeste distributia e chiar cea aleasa LOLO de `make_fs_runs.pick_params`
    pe acelasi fisier, adica exact T-ul prin care trece semnalul B adoptat: controlul de octet arata
    ca reconstructia pe calea aia da `output/bakeoff_test_Text/` bit cu bit. A citi entropia la T = 1
    ar descrie alta distributie decat cea pe care o citeste B.

      `entropie`  media entropiilor celor doua distributii temperate. Mare = B nesigur pe itemul asta.
      `dezacord`  divergenta Jensen-Shannon intre cele doua prompturi temperate. Mare = prompturile nu
                  sunt de acord. A murit ca TRASATURA la controlul flexibil, cu exces ~+0.0011 peste
                  podeaua de zgomot; ca pondere e alt obiect si se remasoara.
      `zgomot`    o coloana de numere aleatoare. NU e un candidat, e podeaua: spune cat scoate
                  procedura din grila largita cand `h` nu contine nicio informatie.

    Atomii efectivi, `exp(entropie)`, sunt deliberat absenti: sunt o transformare monotona a primei
    marimi, deci ar fi al treilea candidat fara sa fie o a treia ipoteza.
    """
    import analysis_dist as ad
    from bakeoff_trial import with_context
    from make_fs_runs import load_srcs, pick_params
    d = with_context(pd.read_csv(path), "test")
    need = [f"p{i}_{k}" for i in (1, 2) for k in "12345"]
    miss = [c for c in need if c not in d.columns]
    if miss:
        raise SystemExit(f"{path} n-are coloanele {miss}, deci n-are doua sloturi de prompt")
    PL, _ = load_srcs([path])
    params, _ = pick_params(PL, "temperatura", ad.T_GRID_EXT)
    out = {}
    rng = np.random.default_rng(int(seed))
    for lg, g in d.groupby(d["lang"].astype(str), sort=True):
        T = params[lg][0]
        P1 = ad.temper(g[[f"p1_{k}" for k in "12345"]].values.astype(float), T)
        P2 = ad.temper(g[[f"p2_{k}" for k in "12345"]].values.astype(float), T)
        if kind == "entropie":
            v = 0.5 * (ad.entropy(P1) + ad.entropy(P2))
        elif kind == "dezacord":
            v = ad.js_div(P1, P2)
        elif kind == "zgomot":
            v = rng.standard_normal(len(g))
        else:
            raise SystemExit(f"h necunoscut: {kind!r}")
        for i, x in zip(g["idx"].values, v):
            out[int(i)] = float(x)
    return out, f"{kind} la T ales LOLO" + (f", seed {seed}" if kind == "zgomot" else "")


def _r_grid(zA, zB, y, h, agrid, wgrid):
    """Matricea (len(agrid), len(wgrid)) cu r al amestecului cu pondere per item.

    `w_i = clip(w + a*h_i, 0, 1)`. Taierea la [0, 1] e ce face marimea asta neliniara in `a` si de
    aceea forma inchisa pe momente nu se aplica: la `a = 0` insa nu taie nimic si iese exact
    `w*zA + (1-w)*zB`, deci punctul neutru e reprodus bit cu bit si controlul de reproducere are sens.

    Se calculeaza vectorizat, o singura data per (limba, candidat): 147 de corelatii intr-un apel, nu
    147 de apeluri. Fara asta cele trei niveluri imbricate ar face sute de mii de apeluri Pearson.
    """
    a = np.asarray(zA, float); b = np.asarray(zB, float)
    y = np.asarray(y, float) - np.mean(y)
    sy = np.sqrt(float(y @ y))
    out = np.empty((len(agrid), len(wgrid)))
    for i, aa in enumerate(agrid):
        W = np.clip(np.asarray(wgrid, float)[None, :] + aa * np.asarray(h, float)[:, None], 0.0, 1.0)
        P = W * a[:, None] + (1.0 - W) * b[:, None]
        P = P - P.mean(axis=0, keepdims=True)
        den = np.sqrt((P * P).sum(axis=0)) * sy
        num = y @ P
        out[i] = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)
    return out


def _check_moments(sig, tol=1e-10):
    """Forma inchisa fata de `bakeoff_trial.pearson`, pe date reale, la capetele si la mijlocul grilei."""
    lg = sorted(sig)[0]; d = sig[lg]
    M = _moments(d["zA"].values, d["zB"].values, d["y"].values)
    bad = [(w, _r_mom(M, w), r_at(d, w)) for w in (0.0, 0.35, 0.5, 1.0)
           if abs(_r_mom(M, w) - r_at(d, w)) > tol]
    if bad:
        raise SystemExit(f"forma inchisa nu reproduce pearson pe {lg}: {bad}")


def fit_choice(arm, fit_split, lg, tab_pick, base, asets, src_grid):
    """`(set de trasaturi, w_src, w)` pentru limba L, alese pe CELELALTE limbi ale splitului.

    Trei niveluri, si al doilea e cel care conteaza pentru scurgere:

      1. candidatii sunt perechile (set de trasaturi, w_src);
      2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al fuziunii
         pe L', unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte opt, adica
         excluzand si L si L'. Fara nivelul asta, criteriul ar judeca un candidat cu o pondere
         potrivita pe chiar limba pe care il masoara;
      3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat.

    Modelul lui B al limbilor de potrivire se re-alege ca pana acum, cu `exclude={lg}`, si pe ACELASI
    `tab_pick` ca selectia principala: altfel schimbarea splitului de selectie ar deschide o scurgere
    exact pe unde selectia imbricata a inchis una. Nu se coboara si el la al treilea nivel; scrie asa
    in tabelul de audit al raportului.
    """
    fit = base[fit_split] if arm != "lolo" else load_signals(arm, fit_split, tab_pick, exclude={lg})
    others = {l2: d for l2, d in fit.items() if l2 != lg}
    if not others:
        return None
    per_item = len(A_GRID) > 1 or float(A_GRID[0]) != 0.0
    if per_item:
        # Aceleasi TREI niveluri, doar ca al doilea si al treilea aleg perechea (a, w), nu doar w.
        # `R[l2]` e matricea de r peste toata grila, deci nivelul imbricat e o medie si un argmax pe
        # matrice, nu o bucla de apeluri Pearson.
        cands, crit = [], []
        for aset in asets:
            for sv in src_grid:
                R = {l2: _r_grid(zA_of(d, aset, sv), d["zB"].values, d["y"].values,
                                 d["h"].values, A_GRID, GRID) for l2, d in others.items()}
                vals = []
                for l2 in others:
                    inner = np.mean([R[l3] for l3 in others if l3 != l2], axis=0)
                    ia, iw = np.unravel_index(int(np.nanargmax(inner)), inner.shape)
                    vals.append(float(R[l2][ia, iw]))
                cands.append((aset, float(sv), R)); crit.append(float(np.mean(vals)))
        k = int(np.argmax(crit))
        aset, w_src, R = cands[k]
        M = np.mean([R[l2] for l2 in others], axis=0)
        ia, iw = np.unravel_index(int(np.nanargmax(M)), M.shape)
        return {"aset": aset, "w_src": w_src, "w": float(GRID[iw]), "a": float(A_GRID[ia]),
                "curve": list(M[ia]), "crit": crit, "crit_best": crit[k],
                "n_cand": len(cands), "n_langs": len(others),
                "n_items": int(sum(len(d) for d in others.values())),
                "langs": sorted(others)}
    cands, crit = [], []
    for aset in asets:
        for s in src_grid:
            M = {l2: _moments(zA_of(d, aset, s), d["zB"].values, d["y"].values)
                 for l2, d in others.items()}
            vals = []
            for l2 in others:
                inner = [float(np.mean([_r_mom(M[l3], w) for l3 in others if l3 != l2]))
                         for w in GRID]
                vals.append(_r_mom(M[l2], float(GRID[int(np.argmax(inner))])))
            cands.append((aset, float(s), M)); crit.append(float(np.mean(vals)))
    k = int(np.argmax(crit))
    aset, w_src, M = cands[k]
    curve = [float(np.mean([_r_mom(M[l2], w) for l2 in others])) for w in GRID]
    return {"aset": aset, "w_src": w_src, "w": float(GRID[int(np.argmax(curve))]), "a": 0.0,
            "curve": curve, "crit": crit, "crit_best": crit[k],
            "n_cand": len(cands), "n_langs": len(others),
            "n_items": int(sum(len(d) for d in others.values())),
            "langs": sorted(others)}


def fuse(arm="qwen3-8b-4bit", n_boot=2000, fit_split="trial", pick_split="trial"):
    from bakeoff_trial import r_table
    from mlsp_common import boot_r_ci
    tab_pick = r_table({k: v for k, v in runs_for(pick_split).items()}, "B")

    fits = ["trial", "test"] if fit_split == "both" else [fit_split]
    base = {s: load_signals(arm, s, tab_pick) for s in dict.fromkeys(fits + ["test"])}
    te = base["test"]
    if not te:
        raise SystemExit("niciun rand de test. Ruleaza intai bake-off-ul cu --split test.")
    print(f"[F] brat={arm} | potrivire pe {'+'.join(fits)} | selectia lui B pe {pick_split} | "
          + " | ".join(f"{s} {len(base[s])} limbi" for s in base), flush=True)

    rows = {s: [] for s in fits}
    preds = {s: [] for s in fits}
    cmp_rows = []
    for lg in sorted(te):
        W = {s: fit_weight(arm, s, lg, tab_pick, base) for s in fits}
        if any(v is None for v in W.values()):
            continue

        d = te[lg]
        bA = boot_r_ci(d["y"].values, d["zA"].values, d["ctx"].values, n_boot=n_boot)
        bB = boot_r_ci(d["y"].values, d["zB"].values, d["ctx"].values, n_boot=n_boot)
        P, B = {}, {}
        for s in fits:
            w = W[s]["w"]
            P[s] = w * d["zA"].values + (1 - w) * d["zB"].values
            B[s] = boot_r_ci(d["y"].values, P[s], d["ctx"].values, n_boot=n_boot)

        for s in fits:
            w, b, curve = W[s]["w"], B[s], W[s]["curve"]
            # Diferentele sunt PERECHE: aceeasi reesantionare aplicata ambelor brate, deci zgomotul
            # comun al esantionului se anuleaza si intervalul e al diferentei, nu al sumei
            # incertitudinilor. `boot_r_ci` are seed fix si primeste acelasi vector de contexte, deci
            # reesantionarile sunt aceleasi de la un apel la altul.
            n = min(len(b["boot"]), len(bA["boot"]), len(bB["boot"]))
            dA = b["boot"][:n] - bA["boot"][:n]
            dB = b["boot"][:n] - bB["boot"][:n]
            rows[s].append({"lang": lg, "model_B": d["model"].iloc[0], "n": int(len(d)),
                            "n_ctx": b["n_ctx"], "w": w,
                            "r_A": round(bA["r"], 4), "r_B": round(bB["r"], 4),
                            "r_fuz": round(b["r"], 4),
                            "fuz_lo": round(b["lo"], 4), "fuz_hi": round(b["hi"], 4),
                            "d_A": round(b["r"] - bA["r"], 4),
                            "d_A_lo": round(float(np.percentile(dA, 2.5)), 4),
                            "d_A_hi": round(float(np.percentile(dA, 97.5)), 4),
                            "d_B": round(b["r"] - bB["r"], 4),
                            "d_B_lo": round(float(np.percentile(dB, 2.5)), 4),
                            "d_B_hi": round(float(np.percentile(dB, 97.5)), 4),
                            "w_curba_min": round(float(min(curve)), 4),
                            "w_curba_max": round(float(max(curve)), 4)})
            preds[s].append(pd.DataFrame({"lang": lg, "idx": d["idx"].values, "y": d["y"].values,
                                          "ctx": d["ctx"].values, "A": d["A"].values,
                                          "B": d["B"].values, "w": w, "p_fuz": P[s]}))
            print(f"  {lg:4s} fit={s:5s} w={w:.2f} pe {W[s]['n_langs']} limbi / "
                  f"{W[s]['n_items']} itemi | A {bA['r']:+.4f} | B {bB['r']:+.4f} | "
                  f"fuziune {b['r']:+.4f} [{b['lo']:+.4f},{b['hi']:+.4f}]", flush=True)

        if len(fits) > 1:
            n = min(len(B["test"]["boot"]), len(B["trial"]["boot"]), len(bA["boot"]))
            dfit = B["test"]["boot"][:n] - B["trial"]["boot"][:n]
            row = {"lang": lg, "model_B": d["model"].iloc[0], "n": int(len(d)),
                   "n_ctx": B["test"]["n_ctx"],
                   "r_A": round(bA["r"], 4), "r_B": round(bB["r"], 4)}
            for s in fits:
                dS = B[s]["boot"][:n] - bA["boot"][:n]
                row |= {f"w_{s}": W[s]["w"], f"nfit_langs_{s}": W[s]["n_langs"],
                        f"nfit_items_{s}": W[s]["n_items"],
                        f"r_fuz_{s}": round(B[s]["r"], 4),
                        f"fuz_lo_{s}": round(B[s]["lo"], 4), f"fuz_hi_{s}": round(B[s]["hi"], 4),
                        f"d_A_{s}": round(B[s]["r"] - bA["r"], 4),
                        f"d_A_lo_{s}": round(float(np.percentile(dS, 2.5)), 4),
                        f"d_A_hi_{s}": round(float(np.percentile(dS, 97.5)), 4),
                        f"curba_min_{s}": round(float(min(W[s]["curve"])), 4),
                        f"curba_max_{s}": round(float(max(W[s]["curve"])), 4)}
            row |= {"d_fit": round(B["test"]["r"] - B["trial"]["r"], 4),
                    "d_fit_lo": round(float(np.percentile(dfit, 2.5)), 4),
                    "d_fit_hi": round(float(np.percentile(dfit, 97.5)), 4)}
            cmp_rows.append(row)

    out = {}
    for s in fits:
        d = pd.DataFrame(rows[s])
        d.to_csv(TABLE.format(arm=arm, suf=SUF[s]), index=False)
        pd.concat(preds[s], ignore_index=True).to_csv(PREDS_OUT.format(arm=arm, suf=SUF[s]),
                                                      index=False)
        _report(d, arm, s, pick_split)
        out[s] = d
        print(f"\n[F] fit={s} | r mediu: A {d['r_A'].mean():+.4f} | B {d['r_B'].mean():+.4f} | "
              f"fuziune {d['r_fuz'].mean():+.4f}")
        print(f"-> {REPORT.format(arm=arm, suf=SUF[s])}")

    if cmp_rows:
        c = pd.DataFrame(cmp_rows)
        c.to_csv(CMP_TABLE.format(arm=arm), index=False)
        _report_cmp(c, arm, pick_split)
        _summary()
        print(f"\n[F] potrivire pe trial {c['r_fuz_trial'].mean():+.4f} | pe test "
              f"{c['r_fuz_test'].mean():+.4f} | diferenta {c['d_fit'].mean():+.4f}")
        print(f"-> {CMP_REPORT.format(arm=arm)}\n-> {SUMMARY}")
    return 0


def _load_vs(path):
    """Predictiile per instanta ale configuratiei de comparat, {limba: Series indexata pe idx}."""
    q = path if os.path.isabs(path) else os.path.join(HERE, path)
    if not os.path.exists(q):
        raise SystemExit(f"{q} lipseste")
    d = pd.read_csv(q)
    miss = [c for c in ("lang", "idx", "p_fuz") if c not in d.columns]
    if miss:
        raise SystemExit(f"{q} n-are coloanele {miss}")
    return {lg: g.drop_duplicates("idx").set_index("idx")["p_fuz"] for lg, g in d.groupby("lang")}


def fuse_ens(arm="lolo", n_boot=2000, fit_split="test", asets=("A",), src_grid=(0.0,),
             tag="ens", vs=None, pick_split="trial"):
    """Fuziunea cu semnalul A ca ansamblu de surse, si eventual cu setul de trasaturi ales si el LOLO.

    Fata de `fuse`, un singur lucru se schimba: A nu mai e o coloana fixa, e
    `z(w_src·z(p_en) + (1−w_src)·z(p_multi))`, iar `w_src` si setul de trasaturi trec prin aceeasi
    selectie leave-one-language-out prin care trece deja w. Bootstrap-ul pe contexte, selectia
    modelului lui B si randurile de test sunt neatinse. Cu `src_grid = (0.0,)` si un singur set,
    rezultatul e cel de pana acum.
    """
    from bakeoff_trial import r_table
    from mlsp_common import boot_r_ci
    # Prin `runs_for`, nu prin `load_runs` direct: altfel `--b-dir` ar schimba randurile citite dar nu
    # si tabelul pe care se alege modelul, adica selectia s-ar face pe alt semnal decat fuziunea.
    tab_pick = r_table({k: v for k, v in runs_for(pick_split).items()}, "B")
    base = {sp: load_signals(arm, sp, tab_pick) for sp in dict.fromkeys([fit_split, "test"])}
    te = base["test"]
    if not te:
        raise SystemExit("niciun rand de test. Ruleaza intai bake-off-ul cu --split test.")
    _check_moments(te)
    ref = _load_vs(vs) if vs else None
    print(f"[F] brat={arm} | potrivire pe {fit_split} | selectia lui B pe {pick_split} | "
          f"seturi {list(asets)} | w_src pe "
          f"{len(src_grid)} puncte | test {len(te)} limbi", flush=True)

    # Esantioanele bootstrap se pastreaza per limba, ca sa se poata construi si intervalul MEDIEI:
    # se mediaza cele zece limbi la fiecare reesantionare, deci iese o distributie a mediei, nu o
    # medie de distributii. Reesantionarea k a fiecarei limbi e independenta de celelalte, `boot_r_ci`
    # avand seed fix si contexte proprii, deci medierea pe index e legitima.
    agg = {"fuz": [], "A": [], "B": [], "azi": []}
    rows, preds = [], []
    for lg in sorted(te):
        W = fit_choice(arm, fit_split, lg, tab_pick, base, asets, src_grid)
        if W is None:
            continue
        d = te[lg]
        zA = zA_of(d, W["aset"], W["w_src"])
        w = W["w"]
        aa = float(W.get("a", 0.0))
        # La `a = 0` taierea nu taie nimic si expresia e literal `w*zA + (1-w)*zB`, deci ramura asta
        # reproduce bit cu bit configuratia publicata. Controlul se ruleaza, nu se presupune.
        wi = np.clip(w + aa * d["h"].values, 0.0, 1.0) if aa != 0.0 else w
        P = wi * zA + (1 - wi) * d["zB"].values
        bA = boot_r_ci(d["y"].values, zA, d["ctx"].values, n_boot=n_boot)
        bB = boot_r_ci(d["y"].values, d["zB"].values, d["ctx"].values, n_boot=n_boot)
        b = boot_r_ci(d["y"].values, P, d["ctx"].values, n_boot=n_boot)
        # Diferentele sunt PERECHE: `boot_r_ci` are seed fix si primeste acelasi vector de contexte,
        # deci reesantionarile sunt aceleasi de la un apel la altul si zgomotul comun se anuleaza.
        k = min(len(b["boot"]), len(bA["boot"]), len(bB["boot"]))
        dA, dB = b["boot"][:k] - bA["boot"][:k], b["boot"][:k] - bB["boot"][:k]
        row = {"lang": lg, "model_B": d["model"].iloc[0], "n": int(len(d)), "n_ctx": b["n_ctx"],
               "aset": W["aset"], "w_src": W["w_src"], "w": w, "a": aa,
               "h": H_NUME,
               "r_A": round(bA["r"], 4), "r_B": round(bB["r"], 4), "r_fuz": round(b["r"], 4),
               "r_A_raw": bA["r"], "r_B_raw": bB["r"], "r_fuz_raw": b["r"],
               "fuz_lo": round(b["lo"], 4), "fuz_hi": round(b["hi"], 4),
               "d_A": round(b["r"] - bA["r"], 4),
               "d_A_lo": round(float(np.percentile(dA, 2.5)), 4),
               "d_A_hi": round(float(np.percentile(dA, 97.5)), 4),
               "d_B": round(b["r"] - bB["r"], 4),
               "d_B_lo": round(float(np.percentile(dB, 2.5)), 4),
               "d_B_hi": round(float(np.percentile(dB, 97.5)), 4),
               "w_curba_min": round(float(min(W["curve"])), 4),
               "w_curba_max": round(float(max(W["curve"])), 4),
               "crit_min": round(float(min(W["crit"])), 4),
               "crit_max": round(float(max(W["crit"])), 4), "n_cand": W["n_cand"],
               "nfit_langs": W["n_langs"], "nfit_items": W["n_items"]}
        if ref is not None:
            if lg not in ref:
                raise SystemExit(f"{vs} n-are limba {lg}")
            p0 = ref[lg].reindex(d["idx"].values).values
            if not np.isfinite(p0).all():
                raise SystemExit(f"{vs} n-acopera toate randurile lui {lg}")
            b0 = boot_r_ci(d["y"].values, p0, d["ctx"].values, n_boot=n_boot)
            k0 = min(len(b["boot"]), len(b0["boot"]))
            dv = b["boot"][:k0] - b0["boot"][:k0]
            row |= {"r_azi": round(b0["r"], 4), "r_azi_raw": b0["r"],
                   "d_azi": round(b["r"] - b0["r"], 4),
                    "d_azi_lo": round(float(np.percentile(dv, 2.5)), 4),
                    "d_azi_hi": round(float(np.percentile(dv, 97.5)), 4),
                    "d_azi_p": round(float((dv > 0).mean()), 4)}
        agg["fuz"].append(b["boot"]); agg["A"].append(bA["boot"]); agg["B"].append(bB["boot"])
        if ref is not None:
            agg["azi"].append(b0["boot"])
        rows.append(row)
        preds.append(pd.DataFrame({"lang": lg, "idx": d["idx"].values, "y": d["y"].values,
                                   "ctx": d["ctx"].values, "aset": W["aset"],
                                   "pe": d[f"pe_{W['aset']}"].values,
                                   "pm": d[f"pm_{W['aset']}"].values,
                                   "A": zA, "B": d["zB"].values,
                                   "w_src": W["w_src"], "w": w, "a": aa,
                                   "h": d["h"].values, "p_fuz": P}))
        ex = f" | azi {row['r_azi']:+.4f} ({row['d_azi']:+.4f})" if ref is not None else ""
        print(f"  {lg:4s} set={W['aset']:11s} w_src={W['w_src']:.3f} w={w:.2f} pe {W['n_langs']} "
              f"limbi / {W['n_items']} itemi | A {bA['r']:+.4f} | B {bB['r']:+.4f} | fuziune "
              f"{b['r']:+.4f} [{b['lo']:+.4f},{b['hi']:+.4f}]{ex}", flush=True)

    t = pd.DataFrame(rows)
    os.makedirs(OUT, exist_ok=True)
    t.to_csv(ENS_TABLE.format(arm=arm, tag=tag), index=False)
    pd.concat(preds, ignore_index=True).to_csv(ENS_PREDS.format(arm=arm, tag=tag), index=False)
    _report_ens(t, arm, tag, asets, src_grid, fit_split, vs, n_boot, _agg_boot(agg), pick_split)
    print(f"\n[F] r mediu: A {t['r_A'].mean():+.4f} | B {t['r_B'].mean():+.4f} | "
          f"fuziune {t['r_fuz'].mean():+.4f}")
    if ref is not None:
        print(f"[F] azi {t['r_azi'].mean():+.4f} | diferenta {t['d_azi'].mean():+.4f}")
    print(f"-> {ENS_REPORT.format(arm=arm, tag=tag)}")
    print(f"-> {ENS_TABLE.format(arm=arm, tag=tag)}")
    print(f"-> {ENS_PREDS.format(arm=arm, tag=tag)}")
    return 0


def _agg_boot(agg):
    """Intervalele MEDIEI pe cele zece limbi, din esantioanele per limba deja calculate.

    -> {nume: (lo, hi, P(>0))}. Punctul estimat NU vine de aici, vine din r-ul masurat: media
    esantioanelor bootstrap e deplasata, iar in raport ar aparea ca a doua cifra pentru acelasi lucru.
    """
    keys = [k for k in agg if agg[k]]
    if not keys:
        return {}
    m = min(len(v) for k in keys for v in agg[k])
    if m < 2:
        return {}
    M = {k: np.vstack([v[:m] for v in agg[k]]).mean(axis=0) for k in keys}
    out = {"fuz": (float(np.percentile(M["fuz"], 2.5)), float(np.percentile(M["fuz"], 97.5)),
                   float("nan"))}
    for k in ("A", "B", "azi"):
        if k not in M:
            continue
        dv = M["fuz"] - M[k]
        out[k] = (float(np.percentile(dv, 2.5)), float(np.percentile(dv, 97.5)),
                  float((dv > 0).mean()))
    return out


def _report_ens(t, arm, tag, asets, src_grid, fit_split, vs, n_boot, agg=None,
                pick_split="trial"):
    """Raportul configuratiei cu ansamblu. Nicio cifra nu se recalculeaza aici, doar se formateaza."""
    multi = len(asets) > 1
    ens = len(src_grid) > 1 or float(src_grid[0]) != 0.0
    top = max(BARA.values())
    mf = t["r_fuz_raw"].mean()
    cmdset = " ".join(f"--a-set {k}={os.path.relpath(v, HERE)}" for k, v in A_SETS.items())
    L = [f"# Fuziunea A plus B, brat `{arm}`, semnalul A ca ansamblu de surse\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `fuse_ab.py --arm {arm} --fit "
         f"{fit_split}"
         + ("" if pick_split == "trial" else f" --pick-split {pick_split}")
         + f"{' --ens' if ens else ''} --tag {tag}"
         + (f" --b-dir output/{B_DIR}" if B_DIR else "") + f" {cmdset}"
         + (f" --vs {vs}" if vs else "") + "`. "
         + (f"**Semnalul B de test vine din `output/{B_DIR}/`, nu din `output/bakeoff_test/`.** "
            if B_DIR else "")
         + f"Date brute: `output/{os.path.basename(ENS_TABLE.format(arm=arm, tag=tag))}`, predictii "
         + f"per instanta in `output/{os.path.basename(ENS_PREDS.format(arm=arm, tag=tag))}`.\n\n",
         "## Ce se schimba\n\n",
         "Semnalul A nu mai e o singura potrivire. Cele doua brate de transfer existau deja "
         "amandoua, scrise de `frozen_trial_gap`:\n\n",
         "- `p_en`, antrenat NUMAI pe CompLex EN, o singura potrivire, prezice toate limbile;\n",
         "- `p_multi`, antrenat pe CompLex EN plus randurile de TEST ale celorlalte noua limbi, o "
         "potrivire per limba.\n\n",
         "Semnalul devine, standardizat in interiorul limbii:\n\n",
         "```\nzA = z( w_src · z(p_en) + (1 − w_src) · z(p_multi) )\n```\n\n",
         "`w_src = 0` e bratul de pana acum, `w_src = 1` e bratul EN-only singur. Grila are "
         f"{len(src_grid)} puncte, de la {min(src_grid):.3f} la {max(src_grid):.3f}.\n\n"]
    if multi:
        L.append("Setul de trasaturi al semnalului A e si el un candidat, nu o decizie fixa: "
                 + ", ".join(f"`{a}`" for a in asets) + ". `baza` are lungimea in caractere si "
                 "slotul de fertilitate gol, `fara_lung` anuleaza lungimea, `fert_inloc` pune "
                 "numarul de subword-uri XLM-R in locul ei, `fert_plus` le pastreaza pe amandoua.\n\n")
    else:
        L.append(f"Setul de trasaturi e fixat la `{asets[0]}`, prin argument si nu prin scor: "
                 "lungimea in caractere nu e comparabila intre sisteme de scriere, o tinta japoneza "
                 "avand 3.59 caractere si una italiana 8.78, iar numarul de subword-uri e prin "
                 "constructie in aceeasi unitate peste tot. Argumentul nu foloseste nicio "
                 "eticheta.\n\n")
    L += ["## Selectia, pe trei niveluri imbricate\n\n",
          "Pentru limba L tinuta deoparte:\n\n",
          "1. candidatii sunt perechile (set de trasaturi, `w_src`), "
          f"{int(t['n_cand'].max())} la numar;\n",
          "2. criteriul unui candidat e media, peste cele noua limbi de potrivire L', a lui r al "
          "fuziunii pe L', **unde ponderea w folosita pentru L' e ea insasi aleasa pe celelalte "
          "opt, adica excluzand si L si L'**. Fara nivelul asta criteriul ar judeca un candidat cu "
          "o pondere potrivita pe chiar limba pe care il masoara;\n",
          "3. w pentru L se alege apoi pe cele noua limbi, cu candidatul castigator fixat, pe grila "
          f"de {len(GRID)} de puncte.\n\n",
          f"Toate intervalele vin din bootstrap pe contexte, {n_boot} de reesantionari. Cele ale "
          "diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.\n\n",
          "## Rezultatul pe test\n\n",
          "| limba | model B | n | ctx |" + (" set |" if multi else "") + " w_src | w | r A | r B | "
          "r fuziune | CI 95% | fuziune − A | CI 95% | fuziune − B | CI 95% |\n",
          "|---|---|---|---|" + ("---|" if multi else "") + "---|---|---|---|---|---|---|---|---|---|\n"]
    for r in t.itertuples():
        L.append(f"| {r.lang} | `{r.model_B}` | {r.n} | {r.n_ctx} | "
                 + (f"`{r.aset}` | " if multi else "")
                 + f"{r.w_src:.3f} | {r.w:.2f} | {r.r_A:+.4f} | {r.r_B:+.4f} | "
                   f"**{r.r_fuz:+.4f}** | [{r.fuz_lo:+.4f}, {r.fuz_hi:+.4f}] | {r.d_A:+.4f} | "
                   f"[{r.d_A_lo:+.4f}, {r.d_A_hi:+.4f}] | {r.d_B:+.4f} | "
                   f"[{r.d_B_lo:+.4f}, {r.d_B_hi:+.4f}] |\n")
    L.append(f"| **medie** | | | |" + (" | " if multi else "")
             + f" {t['w_src'].mean():.3f} | {t['w'].mean():.2f} | {t['r_A_raw'].mean():+.4f} | "
               f"{t['r_B_raw'].mean():+.4f} | **{mf:+.4f}** | | {t['d_A'].mean():+.4f} | | "
               f"{t['d_B'].mean():+.4f} | |\n")
    upA, upB = int((t["d_A"] > 0).sum()), int((t["d_B"] > 0).sum())
    sigA = int(((t["d_A_lo"] > 0) | (t["d_A_hi"] < 0)).sum())
    sigB = int(((t["d_B_lo"] > 0) | (t["d_B_hi"] < 0)).sum())
    L.append(f"\nFuziunea bate A pe {upA} din {len(t)} limbi si B pe {upB} din {len(t)}. Intervalul "
             f"exclude zero pe {sigA} limbi fata de A si pe {sigB} fata de B.\n\n")

    if "d_azi" in t.columns:
        md, up = (t["r_fuz_raw"] - t["r_azi_raw"]).mean(), int((t["d_azi"] > 0).sum())
        sig = int((t["d_azi_lo"] > 0).sum())
        L += ["## Configuratia noua fata de cea de azi\n\n",
              "Aceleasi randuri de test, acelasi bootstrap, acelasi brat B. Se schimba numai "
              f"semnalul A. Referinta e `{vs}`, iar diferenta e PERECHE: aceeasi reesantionare pe "
              "ambele configuratii, deci intervalul e al diferentei, nu al sumei incertitudinilor. "
              "`P(>0)` e ponderea reesantionarilor in care noua configuratie iese peste cea de "
              "azi.\n\n",
              "| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |\n|---|---|---|---|---|---|\n"]
        for r in t.itertuples():
            L.append(f"| {r.lang} | {r.r_azi:+.4f} | **{r.r_fuz:+.4f}** | {r.d_azi:+.4f} | "
                     f"[{r.d_azi_lo:+.4f}, {r.d_azi_hi:+.4f}] | {100*r.d_azi_p:.1f}% |\n")
        L.append(f"| **medie** | {t['r_azi_raw'].mean():+.4f} | **{mf:+.4f}** | {md:+.4f} | | "
                 f"{100*t['d_azi_p'].mean():.1f}% |\n")
        L.append(f"\nConfiguratia noua urca fuziunea pe {up} din {len(t)} limbi. Intervalul pereche "
                 f"exclude zero in sus pe {sig}. Pe medie, **{md:+.4f}**.\n\n")

    if agg:
        L += ["## Intervalele mediei, nu ale limbilor\n\n",
              "Tabelele de mai sus dau cate un interval per limba. Cifra care se citeaza e insa media "
              "pe cele zece limbi, si ea are propriul interval: se mediaza cele zece limbi la fiecare "
              "reesantionare, deci iese o distributie a mediei. Diferentele sunt tot PERECHE.\n\n",
              "| ce se compara | pe medie | CI 95% | P(>0) |\n|---|---|---|---|\n"]
        f0 = agg["fuz"]
        L.append(f"| r al fuziunii | **{mf:+.4f}** | [{f0[0]:+.4f}, {f0[1]:+.4f}] | |\n")
        pts = {"A": mf - t["r_A_raw"].mean(), "B": mf - t["r_B_raw"].mean()}
        if "r_azi_raw" in t.columns:
            pts["azi"] = mf - t["r_azi_raw"].mean()
        for k, lab in (("A", "fuziune − A"), ("B", "fuziune − B"),
                       ("azi", "configuratia noua − cea de azi")):
            if k in agg and k in pts:
                v = agg[k]
                L.append(f"| {lab} | {pts[k]:+.4f} | [{v[0]:+.4f}, {v[1]:+.4f}] | "
                         f"{100 * v[2]:.1f}% |\n")
        L.append("\n")
    L += ["## Fata de reperele publicate, toate pe test\n\n", "| sistem | r mediu pe 10 limbi |\n|---|---|\n"]
    for k, v in sorted(BARA.items(), key=lambda kv: kv[1]):
        L.append(f"| {k} | {v:.4f} |\n")
    L.append(f"| semnalul A singur, ansamblul de surse | {t['r_A_raw'].mean():.4f} |\n")
    L.append(f"| semnalul B singur, `{arm}` | {t['r_B_raw'].mean():.4f} |\n")
    if "r_azi_raw" in t.columns:
        L.append(f"| fuziunea de azi, A = `p_multi` | {t['r_azi_raw'].mean():.4f} |\n")
    L.append(f"| **fuziunea cu ansamblul de surse** | **{mf:.4f}** |\n")
    L.append(f"\nFata de cel mai bun reper publicat, {top:.4f}: **{mf - top:+.4f}**. "
             + ("Trecem de el.\n" if mf > top else "Nu trecem de el.\n"))
    if len(t) < 10:
        L.append(f"\n**Atentie: media e pe {len(t)} limbi, nu pe 10.**\n")

    L += ["\n## Ce s-a ales, si cat de plata e alegerea\n\n",
          "`latime w` e r maxim minus r minim pe grila lui w, pe limbile de potrivire: cu cat e mai "
          "plata, cu atat argmaxul e mai mult zgomot. `latime criteriu` e acelasi lucru peste "
          "candidatii (set, `w_src`), deci spune cat separa criteriul candidatul castigator de cel "
          "mai slab.\n\n",
          "| limba |" + (" set |" if multi else "") + " w_src | w | limbi fit | itemi fit | "
          "curba w min | curba w max | latime w | latime criteriu |\n",
          "|---|" + ("---|" if multi else "") + "---|---|---|---|---|---|---|---|\n"]
    for r in t.itertuples():
        L.append(f"| {r.lang} | " + (f"`{r.aset}` | " if multi else "")
                 + f"{r.w_src:.3f} | {r.w:.2f} | {r.nfit_langs} | {r.nfit_items} | "
                   f"{r.w_curba_min:+.4f} | {r.w_curba_max:+.4f} | "
                   f"{r.w_curba_max - r.w_curba_min:.4f} | {r.crit_max - r.crit_min:.4f} |\n")
    if multi:
        cnt = t["aset"].value_counts()
        L.append("\nSetul ales, pe limbi: "
                 + ", ".join(f"`{k}` {v}" for k, v in cnt.items())
                 + ". Seturile care nu apar n-au fost alese niciodata.\n")
    lw = (t["w_curba_max"] - t["w_curba_min"]).mean()
    lc = (t["crit_max"] - t["crit_min"]).mean()
    L.append(f"\nLatimea medie a curbei lui w e {lw:.4f}, iar a criteriului de candidati "
             f"{lc:.4f}, adica de {lw / lc:.0f} ori mai mica. Alegerea candidatului e deci mult mai "
             "plata decat alegerea lui w: separa ceva, fiindca diferenta pe test merge in aceeasi "
             "directie, dar marginea e subtire si o parte din ea e zgomot.\n")
    L.append("\n" + _ladder_text(arm))
    L.append("\n" + _audit_text_ens(arm, multi, ens, pick_split))
    with open(ENS_REPORT.format(arm=arm, tag=tag), "w", encoding="utf-8") as fh:
        fh.write("".join(L))


# Scara configuratiilor, ca fiecare raport sa spuna singur unde se afla. Se citesc CSV-urile surori
# care exista pe disc; ce n-a fost rulat lipseste din tabel, nu se inventeaza.
LADDER = (("fuziunea de azi, A = `p_multi`", "fusion_{arm}_fittest_lemma.csv"),
          ("doar ansamblul de surse, set `baza`", "fusion_{arm}_ens_baza.csv"),
          ("doar `fert_inloc`, fara ansamblu", "fusion_{arm}_src.csv"),
          ("**ansamblu plus `fert_inloc`**", "fusion_{arm}_ens.csv"),
          ("ansamblu plus setul ales si el LOLO", "fusion_{arm}_ens_lolo.csv"))


def _ladder_text(arm):
    """Cele cinci configuratii una langa alta, fiecare cu r-ul ei mediu si cu ce alege."""
    top = max(BARA.values())
    rows = []
    for label, patt in LADDER:
        q = os.path.join(OUT, patt.format(arm=arm))
        if not os.path.exists(q):
            continue
        c = pd.read_csv(q)
        ws = f"{c['w_src'].mean():.3f}" if "w_src" in c.columns else "0.000"
        sets = ", ".join(f"`{k}`" for k in dict.fromkeys(c["aset"])) if "aset" in c.columns else "`baza`"
        col = "r_fuz_raw" if "r_fuz_raw" in c.columns else "r_fuz"
        rows.append((label, len(c), sets, ws, float(c[col].mean())))
    if not rows:
        return ""
    T = ["## Scara configuratiilor\n\n",
         "Toate pe aceleasi randuri de test, cu acelasi brat B si acelasi protocol. Se schimba numai "
         "din ce e facut semnalul A si ce se alege leave-one-language-out.\n\n",
         "| configuratie | limbi | set de trasaturi | w_src mediu | r mediu | fata de "
         f"{top:.4f} |\n|---|---|---|---|---|---|\n"]
    for label, nl, sets, ws, r in rows:
        T.append(f"| {label} | {nl} | {sets} | {ws} | **{r:.4f}** | {r - top:+.4f} |\n")
    T.append(f"\nReperul e cel mai bun reper publicat pe test, G-Eval cu GPT-4o {top:.4f}.\n")
    return "".join(T)


def _audit_text_ens(arm, multi, ens, pick_split="trial"):
    """Unde e garantata proprietatea zero-label, si unde nu e. Linii de cod, nu afirmatii."""
    T = ["## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie\n\n",
         "| ce se alege | unde | cum |\n|---|---|---|\n",
         "| semnalul A, ambele brate | `finetune_xlmr.py`, `frozen_trial_gap` | "
         "`te, tr = (lang == L), (lang != L)`, apoi `Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de "
         "test ale lui L sunt in afara antrenarii. Bratul `p_en` nu vede deloc MLSP. |\n",
         "| tot A, pe trial | `finetune_xlmr.py`, `frozen_trial_gap` | trial-ul lui L intra doar in "
         "`Xpred`, niciodata in `Xtr`. |\n",
         "| setul de trasaturi al lui A | `solution_bert.py`, `_Xc` | fertilitatea e "
         "`len(tokenize(tinta))`, deci o proprietate a tokenizerului, nu a etichetelor. Centrarea ei "
         "foloseste media limbii, nu complexitatea. |\n",
         "| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_pick, set(exclude) \\| "
         "{lg})`: criteriul e media lui r peste CELELALTE 9 limbi ale splitului de selectie, iar "
         "limba pentru care se alege intra chiar ea in multimea exclusa. |\n",
         "| splitul pe care se alege modelul | `fuse_ab.py`, `fuse_ens` | `--pick-split "
         f"{pick_split}`, adica `tab_pick = r_table(load_runs({pick_split!r}), \"B\")`. "
         + ("Selectia si potrivirea ponderii citesc acelasi split, ca antrenarea bratului A. "
            if pick_split != "trial" else
            "Selectia citeste trial-ul, potrivirea ponderii citeste splitul lui `--fit`. ")
         + "Niciun rand al limbii L nu intra in criteriu, pe niciunul dintre splituri: L e "
           "exclusa chiar din media care alege. |\n",
         "| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_choice` | apelul cu "
         "`exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Se face pe "
         "ACELASI `tab_pick`, deci schimbarea splitului de selectie nu deschide o scurgere pe "
         "unde selectia imbricata a inchis una. |\n"]
    if multi:
        T.append("| setul de trasaturi al lui L | `fuse_ab.py`, `fit_choice` | candidatul se alege pe "
                 "`others`, care nu contine L pe niciun split. |\n")
    if ens:
        T.append("| `w_src` | `fuse_ab.py`, `fit_choice` | acelasi criteriu, aceeasi multime "
                 "`others`. |\n")
    T += ["| ponderea w | `fuse_ab.py`, `fit_choice` | `others = {l2: d for l2, d in fit.items() if "
          "l2 != lg}`. Curba nu contine niciun rand al lui L, pe niciun split. |\n",
          "| w-ul limbilor de potrivire, in criteriu | `fuse_ab.py`, `fit_choice` | bucla "
          "`for l3 in others if l3 != l2`: cand un candidat se masoara pe L', ponderea lui L' vine "
          "de pe celelalte opt limbi, deci nici L nici L' nu intra in ea. |\n",
          "| standardizarea | `fuse_ab.py`, `zscore` si `zA_of` | media si deviatia se iau din "
          "predictii, nu din etichete, la ambele niveluri de standardizare ale lui A. |\n",
          "\nSi unde **nu** e garantata, fiindca trebuie scris tot. Doua locuri:\n\n",
          "1. `zA` pentru o limba de potrivire L' vine din iteratia L' a lui `frozen_trial_gap`, "
          "adica dintr-un model antrenat pe toate limbile in afara de L'. Acel model a inclus "
          "randurile de test ale lui L. Alegerile lui L depind deci indirect de etichetele lui L, "
          "prin predictiile lui A pe alte limbi. Dependenta e identica la potrivirea pe trial si la "
          "cea pe test, fiindca ambele folosesc aceleasi predictii. Marimea efectului ramane "
          "**neverificata**; ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L si L', "
          "adica 90 de potriviri `blend_ridge_hgb` in loc de 10, deci o rulare separata cu "
          "aprobare. Bratul `p_en` **nu** are dependenta asta: nu vede niciun rand de MLSP.\n",
          "2. Modelul lui B al limbilor de potrivire se re-alege cu `exclude={L}`, deci la un "
          "nivel, nu la doua. In bucla interioara care alege w-ul lui L' pe celelalte opt, modelul "
          "acelor opt ramane cel ales cu `exclude={L}`, nu cu `exclude={L, L'}`. Nivelul urmator "
          "ar cere `pick_model` cu trei limbi excluse, si nu s-a coborat pana acolo.\n"]
    fb = [(sp, ex, lg, free, key) for (sp, ex, lg), (free, key) in sorted(_POOL_FALLBACK.items())]
    if arm == "lolo":
        T.append("\n### Filtrul de disponibilitate\n\n")
        if fb:
            T.append("Selectia imbricata poate cere un model care nu a fost rulat pe limba de "
                     "potrivire, pe splitul de potrivire. Candidatii se restrang atunci la modelele "
                     "masurate efectiv acolo. Restrangerea se uita la ACOPERIRE, nu la scor, deci nu "
                     "introduce nicio eticheta. Cazurile, toate:\n\n"
                     "| split de potrivire | limba tinuta deoparte | limba de potrivire | cerut | "
                     "folosit |\n|---|---|---|---|---|\n")
            for sp, ex, lg, free, key in fb:
                T.append(f"| {sp} | {', '.join(ex) or 'niciuna'} | {lg} | `{free}` | `{key}` |\n")
        else:
            T.append("Nu s-a activat: fiecare model cerut de selectia imbricata avea masuratori pe "
                     "limba de potrivire, pe splitul de potrivire.\n")
    return "".join(T)


def _report(d, arm, fit="trial", pick_split="trial"):
    bara = BARA
    suf = SUF[fit]
    cap = ("Ponderea w e aleasa leave-one-language-out pe TRIAL, apoi aplicata pe TEST. Pentru limba "
           "L, w maximizeaza r mediu peste celelalte 9 limbi de trial. Nu vede nici limba L, nici "
           "testul. " if fit == "trial" else
           "Ponderea w e aleasa leave-one-language-out pe TESTUL celorlalte 9 limbi, apoi aplicata pe "
           "testul limbii L. Nu vede limba L, pe niciun split. Acelasi protocol pe care il foloseste "
           "deja bratul A, antrenat pe etichetele de test ale celorlalte 9 limbi la "
           "`finetune_xlmr.py:446`. ")
    L = [f"# Fuziunea A plus B, brat `{arm}`" + ("" if fit == "trial" else ", pondere potrivita pe test")
         + "\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `fuse_ab.py --arm {arm}"
         + ("" if fit == "trial" else " --fit test") + "`. "
         f"Date brute: `output/fusion_{arm}{suf}.csv`, predictii per instanta in "
         f"`output/fusion_preds_{arm}{suf}.csv`.\n\n",
         cap +
         "Semnalele sunt standardizate in interiorul limbii, fara etichete; r fiind invariant la "
         "transformari afine, asta nu schimba nimic pentru A singur sau B singur.\n\n",
         "Toate intervalele vin din bootstrap pe contexte, 2000 de reesantionari. Cele ale "
         "diferentelor sunt PERECHE, cu aceeasi reesantionare pe ambele brate.\n\n",
         "## Rezultatul pe test\n\n",
         "| limba | model B | n | ctx | w | r A | r B | r fuziune | CI 95% | fuziune − A | CI 95% | "
         "fuziune − B | CI 95% |\n", "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"]
    for r in d.itertuples():
        L.append(f"| {r.lang} | `{r.model_B}` | {r.n} | {r.n_ctx} | {r.w:.2f} | {r.r_A:+.4f} | "
                 f"{r.r_B:+.4f} | **{r.r_fuz:+.4f}** | [{r.fuz_lo:+.4f}, {r.fuz_hi:+.4f}] | "
                 f"{r.d_A:+.4f} | [{r.d_A_lo:+.4f}, {r.d_A_hi:+.4f}] | {r.d_B:+.4f} | "
                 f"[{r.d_B_lo:+.4f}, {r.d_B_hi:+.4f}] |\n")
    L.append(f"| **medie** | | | | {d['w'].mean():.2f} | {d['r_A'].mean():+.4f} | "
             f"{d['r_B'].mean():+.4f} | **{d['r_fuz'].mean():+.4f}** | | {d['d_A'].mean():+.4f} | | "
             f"{d['d_B'].mean():+.4f} | |\n")

    upA = int((d["d_A"] > 0).sum()); upB = int((d["d_B"] > 0).sum())
    sigA = int(((d["d_A_lo"] > 0) | (d["d_A_hi"] < 0)).sum())
    sigB = int(((d["d_B_lo"] > 0) | (d["d_B_hi"] < 0)).sum())
    L += [f"\nFuziunea bate A pe {upA} din {len(d)} limbi si B pe {upB} din {len(d)}. Intervalul "
          f"exclude zero pe {sigA} limbi fata de A si pe {sigB} fata de B.\n\n",
          "## Fata de reperele publicate, toate pe test\n\n",
          "| sistem | r mediu pe 10 limbi |\n|---|---|\n"]
    for k, v in sorted(bara.items(), key=lambda kv: kv[1]):
        L.append(f"| {k} | {v:.4f} |\n")
    L.append(f"| semnalul A singur, bratul inghetat | {d['r_A'].mean():.4f} |\n")
    L.append(f"| semnalul B singur, `{arm}` | {d['r_B'].mean():.4f} |\n")
    L.append(f"| **fuziunea A plus B, w ales LOLO pe {fit}** | **{d['r_fuz'].mean():.4f}** |\n"
             if fit != "trial" else
             f"| **fuziunea A plus B, w ales LOLO** | **{d['r_fuz'].mean():.4f}** |\n")
    top = max(bara.values())
    dif = d["r_fuz"].mean() - top
    L.append(f"\nFata de cel mai bun reper publicat, {top:.4f}: **{dif:+.4f}**. "
             + ("Trecem de el.\n" if dif > 0 else "Nu trecem de el.\n"))
    if len(d) < 10:
        L.append(f"\n**Atentie: media e pe {len(d)} limbi, nu pe 10.** Reperele sunt pe 10, deci "
                 "comparatia de mai sus nu e inca pe picior de egalitate.\n")
    L += ["\n## Ponderea aleasa\n\n",
          "Coloana `w` e ponderea semnalului A. w = 1 inseamna A singur, w = 0 inseamna B singur. "
          "Curba lui r peste grila, pe limbile de potrivire, arata cat de plata e alegerea: daca "
          "maximul e cu putin peste capete, w-ul ales e in mare parte zgomot.\n\n",
          "| limba | w | r minim pe curba | r maxim pe curba | latime |\n|---|---|---|---|---|\n"]
    for r in d.itertuples():
        L.append(f"| {r.lang} | {r.w:.2f} | {r.w_curba_min:+.4f} | {r.w_curba_max:+.4f} | "
                 f"{r.w_curba_max - r.w_curba_min:.4f} |\n")
    if fit != "trial":
        L.append("\n" + _audit_text(arm, pick_split))
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT.format(arm=arm, suf=suf), "w", encoding="utf-8") as fh:
        fh.write("".join(L))


def _report_cmp(c, arm, pick_split="trial"):
    """Cele doua potriviri una langa alta, per limba si pe medie. Asta e livrabilul sesiunii."""
    mt, mT = c["r_fuz_trial"].mean(), c["r_fuz_test"].mean()
    top = max(BARA.values())
    up = int((c["d_fit"] > 0).sum())
    sig_up = int((c["d_fit_lo"] > 0).sum())
    sig_dn = int((c["d_fit_hi"] < 0).sum())
    L = [f"# Ponderea potrivita pe trial fata de potrivita pe test, brat `{arm}`\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `fuse_ab.py --arm {arm} --fit both`. "
         f"Date brute: `output/fusion_{arm}_fitcmp.csv`.\n\n",
         "Ce se compara: acelasi sistem, aceleasi predictii A si B, acelasi bootstrap, aceleasi randuri "
         "de test. Se schimba un singur lucru, splitul pe care se potriveste ponderea w pentru limba "
         "tinuta deoparte:\n\n",
         "- **potrivire pe trial**, protocolul de pana acum: w maximizeaza r mediu peste cele 30 de "
         "instante de trial ale fiecareia dintre celelalte 9 limbi;\n",
         "- **potrivire pe test**: acelasi argmax, dar peste randurile de TEST ale acelorasi 9 limbi.\n\n",
         "Motivul pentru care a doua varianta nu e o largire a protocolului, ci o reparatie a lui: "
         "bratul A foloseste DEJA etichetele de test ale celorlalte 9 limbi, la `finetune_xlmr.py:446`, "
         "`Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` peste randurile de test. Ponderea se "
         "potrivea insa pe trial-ul acelorasi limbi. Doua componente ale aceluiasi sistem foloseau "
         "splituri diferite. In plus, `e_split_gap.md` masoara ca trial-ul supraestimeaza semnalul B cu "
         "0.191, deci w acorda sistematic prea putin lui A.\n\n",
         "Intervalele sunt bootstrap pe contexte, 2000 de reesantionari. Coloana de diferenta e "
         "**PERECHE**: aceeasi reesantionare pe ambele potriviri, deci intervalul e al diferentei, nu "
         "al sumei incertitudinilor.\n\n",
         "## Cele doua potriviri, per limba\n\n",
         "| limba | model B | n | ctx | r A | r B | w trial | r fuziune, fit trial | CI 95% | w test | "
         "r fuziune, fit test | CI 95% | test − trial | CI 95% pereche |\n",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"]
    for r in c.itertuples():
        L.append(f"| {r.lang} | `{r.model_B}` | {r.n} | {r.n_ctx} | {r.r_A:+.4f} | {r.r_B:+.4f} | "
                 f"{r.w_trial:.2f} | {r.r_fuz_trial:+.4f} | [{r.fuz_lo_trial:+.4f}, "
                 f"{r.fuz_hi_trial:+.4f}] | {r.w_test:.2f} | **{r.r_fuz_test:+.4f}** | "
                 f"[{r.fuz_lo_test:+.4f}, {r.fuz_hi_test:+.4f}] | {r.d_fit:+.4f} | "
                 f"[{r.d_fit_lo:+.4f}, {r.d_fit_hi:+.4f}] |\n")
    L.append(f"| **medie** | | | | {c['r_A'].mean():+.4f} | {c['r_B'].mean():+.4f} | "
             f"{c['w_trial'].mean():.2f} | {mt:+.4f} | | {c['w_test'].mean():.2f} | **{mT:+.4f}** | | "
             f"{c['d_fit'].mean():+.4f} | |\n")
    L += [f"\nPotrivirea pe test urca fuziunea pe {up} din {len(c)} limbi si o scade pe {len(c) - up}. "
          f"Intervalul pereche exclude zero in sus pe {sig_up} limbi si in jos pe {sig_dn}. Pe medie, "
          f"**{mT - mt:+.4f}**.\n\n",
          "## Fata de semnalele singure si de reperele publicate\n\n",
          "| sistem | r mediu |\n|---|---|\n"]
    for k, v in sorted(BARA.items(), key=lambda kv: kv[1]):
        L.append(f"| {k} | {v:.4f} |\n")
    L += [f"| semnalul A singur, bratul inghetat | {c['r_A'].mean():.4f} |\n",
          f"| semnalul B singur, `{arm}` | {c['r_B'].mean():.4f} |\n",
          f"| fuziunea, w potrivit pe trial | {mt:.4f} |\n",
          f"| **fuziunea, w potrivit pe test** | **{mT:.4f}** |\n",
          f"\nFata de cel mai bun reper publicat, {top:.4f}: potrivirea pe trial "
          f"**{mt - top:+.4f}**, potrivirea pe test **{mT - top:+.4f}**.\n\n",
          "## Fuziunea fata de A singur, la fiecare potrivire\n\n",
          "Coloana care conteaza cand fuziunea iese sub A singur: daca w e prost estimat, amestecul "
          "strica un semnal bun.\n\n",
          "| limba | fit trial − A | CI 95% | fit test − A | CI 95% |\n|---|---|---|---|---|\n"]
    for r in c.itertuples():
        L.append(f"| {r.lang} | {r.d_A_trial:+.4f} | [{r.d_A_lo_trial:+.4f}, {r.d_A_hi_trial:+.4f}] | "
                 f"{r.d_A_test:+.4f} | [{r.d_A_lo_test:+.4f}, {r.d_A_hi_test:+.4f}] |\n")
    L.append(f"| **medie** | {c['d_A_trial'].mean():+.4f} | | {c['d_A_test'].mean():+.4f} | |\n")
    L += ["\n## Setul de potrivire si forma curbei\n\n",
          "`limbi` si `itemi` spun pe ce s-a potrivit efectiv w. `latime` e r maxim minus r minim pe "
          "grila de 21 de puncte, pe limbile de potrivire: cu cat e mai plata, cu atat argmaxul e mai "
          "mult zgomot.\n\n",
          "| limba | limbi fit | itemi trial | itemi test | latime curba trial | latime curba test |\n",
          "|---|---|---|---|---|---|\n"]
    for r in c.itertuples():
        lgs = (f"{r.nfit_langs_trial}" if r.nfit_langs_trial == r.nfit_langs_test
               else f"trial {r.nfit_langs_trial}, test {r.nfit_langs_test}")
        L.append(f"| {r.lang} | {lgs} | {r.nfit_items_trial} | {r.nfit_items_test} | "
                 f"{r.curba_max_trial - r.curba_min_trial:.4f} | "
                 f"{r.curba_max_test - r.curba_min_test:.4f} |\n")
    L.append(f"| **total** | | {int(c['nfit_items_trial'].sum())} | "
             f"{int(c['nfit_items_test'].sum())} | | |\n")
    L.append("\n" + _audit_text(arm, pick_split))
    os.makedirs(OUT, exist_ok=True)
    with open(CMP_REPORT.format(arm=arm), "w", encoding="utf-8") as fh:
        fh.write("".join(L))


def _summary():
    """Tabelul peste brate, refacut din CSV-urile de comparatie existente pe disc."""
    import glob
    order = ["qwen3-8b-4bit", "gemma4-12b-4bit", "lolo"]
    files = sorted(glob.glob(CMP_TABLE.format(arm="*")))
    pre, post = os.path.basename(CMP_TABLE).split("{arm}")
    arms = [os.path.basename(f)[len(pre):-len(post)] for f in files]
    arms = [a for a in order if a in arms] + sorted(a for a in arms if a not in order)
    top = max(BARA.values())
    L = ["# Potrivirea ponderii pe trial fata de pe test, toate bratele\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `fuse_ab.py --fit both`. Detaliile per brat "
         "in `output/e_fusion_<brat>_fitcmp.md`.\n\n",
         "| brat B | limbi | r A | r B | w trial | fuziune, fit trial | w test | fuziune, fit test | "
         f"test − trial | fata de {top:.4f} |\n|---|---|---|---|---|---|---|---|---|---|\n"]
    for a in arms:
        c = pd.read_csv(CMP_TABLE.format(arm=a))
        mt, mT = c["r_fuz_trial"].mean(), c["r_fuz_test"].mean()
        L.append(f"| `{a}` | {len(c)} | {c['r_A'].mean():+.4f} | {c['r_B'].mean():+.4f} | "
                 f"{c['w_trial'].mean():.2f} | {mt:+.4f} | {c['w_test'].mean():.2f} | "
                 f"**{mT:+.4f}** | {mT - mt:+.4f} | {mT - top:+.4f} |\n")
    L.append("\nReperul de comparatie e cel mai bun reper publicat pe test, G-Eval cu GPT-4o "
             f"{top:.4f}. `lolo` e singurul brat care respecta protocolul si pe alegerea modelului: "
             "`gemma4-12b-4bit` peste tot ar fi o alegere care nu se poate face fara sa vezi testul.\n")
    os.makedirs(OUT, exist_ok=True)
    with open(SUMMARY, "w", encoding="utf-8") as fh:
        fh.write("".join(L))


def _audit_text(arm, pick_split="trial"):
    """Unde e garantata proprietatea zero-label, si unde nu e. Linii de cod, nu afirmatii."""
    fb = [(sp, ex, lg, free, key) for (sp, ex, lg), (free, key) in sorted(_POOL_FALLBACK.items())]
    T = ["## Limba tinuta deoparte nu e folosita nicaieri. Unde e garantat, linie cu linie\n\n",
         "| ce se alege | unde | cum |\n|---|---|---|\n",
         "| semnalul A | `finetune_xlmr.py:444-446` | `te, tr = (lang == L), (lang != L)`, apoi "
         "`Xtr = np.vstack([Xen, Xml[tr]])`. Randurile de test ale lui L sunt in afara antrenarii. |\n",
         "| tot A, pe trial | `finetune_xlmr.py:449-450` | trial-ul lui L intra doar in `Xpred`, "
         "niciodata in `Xtr`. |\n",
         "| modelul lui B | `fuse_ab.py`, `load_signals` | `pick_model(tab_pick, set(exclude) \\| "
         "{lg})`: criteriul e media lui r peste CELELALTE 9 limbi ale splitului de selectie, iar "
         "limba pentru care se alege intra chiar ea in multimea exclusa. |\n",
         "| splitul pe care se alege modelul | `fuse_ab.py`, `fuse` | `--pick-split "
         f"{pick_split}`, adica `tab_pick = r_table(load_runs({pick_split!r}), \"B\")`. "
         + ("Selectia si potrivirea ponderii citesc acelasi split, ca antrenarea bratului A. "
            if pick_split != "trial" else
            "Selectia citeste trial-ul, potrivirea ponderii citeste splitul lui `--fit`. ")
         + "Niciun rand al limbii L nu intra in criteriu, pe niciunul dintre splituri: L e "
           "exclusa chiar din media care alege. |\n",
         "| modelul lui B la limbile de potrivire | `fuse_ab.py`, `fit_weight` | apelul cu "
         "`exclude={lg}` face selectia IMBRICATA: pentru L' se exclud si L, si L'. Fara asta w(L) ar "
         "vedea limba L prin modelul ales pentru L'. Se face pe ACELASI `tab_pick`. |\n",
         "| ponderea w | `fuse_ab.py`, `fit_weight` | `others = [d for l2, d in fit.items() if "
         "l2 != lg]`. Curba nu contine niciun rand al lui L, pe niciun split. |\n",
         "| standardizarea | `fuse_ab.py`, `zscore` | media si deviatia se iau din predictii, nu din "
         "etichete. |\n",
         "\nSi unde **nu** e garantata, fiindca trebuie scris tot: `zA` pentru o limba de potrivire L' "
         "vine din iteratia L' a lui `frozen_trial_gap`, adica dintr-un model antrenat pe toate "
         "limbile in afara de L'. Acel model a inclus randurile de test ale lui L. Ponderea lui L "
         "depinde deci indirect de etichetele lui L, prin predictiile lui A pe alte limbi.\n\n",
         "Dependenta asta e **identica la potrivirea pe trial si la cea pe test**, fiindca ambele "
         "folosesc aceleasi predictii A din `output/e1_frozen_preds.csv`. Trecerea la potrivirea pe "
         "test nu adauga nimic si nu inrautateste nimic. Marimea efectului ramane **neverificata**; "
         "ar lamuri-o un brat A dublu imbricat, antrenat excluzand si L, si L', adica 90 de potriviri "
         "`blend_ridge_hgb` in loc de 10, deci o rulare separata cu aprobare.\n"]
    if arm == "lolo":
        T.append("\n### Filtrul de disponibilitate\n\n")
        if fb:
            T.append("Selectia imbricata poate cere un model care nu a fost rulat pe limba de "
                     "potrivire, pe splitul de potrivire. Candidatii se restrang atunci la modelele "
                     "masurate efectiv acolo. Restrangerea se uita la ACOPERIRE, nu la scor, deci nu "
                     "introduce nicio eticheta. Cazurile, toate:\n\n"
                     "| split de potrivire | limba tinuta deoparte | limba de potrivire | "
                     "cerut | folosit |\n|---|---|---|---|---|\n")
            for sp, ex, lg, free, key in fb:
                T.append(f"| {sp} | {', '.join(ex) or 'niciuna'} | {lg} | `{free}` | `{key}` |\n")
        else:
            T.append("Nu s-a activat: fiecare model cerut de selectia imbricata avea masuratori pe "
                     "limba de potrivire, pe splitul de potrivire.\n")
    return "".join(T)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="qwen3-8b-4bit",
                    help="cheie de model pentru semnalul B, sau 'lolo' pentru harta selectata LOLO")
    ap.add_argument("--boot", type=int, default=2000, help="reesantionari de contexte")
    ap.add_argument("--fit", default="trial", choices=["trial", "test", "both"],
                    help="splitul celorlalte 9 limbi pe care se potriveste ponderea w")
    ap.add_argument("--pick-split", dest="pick_split", default="trial", choices=["trial", "test"],
                    help="splitul celorlalte 9 limbi pe care se ALEGE modelul lui B la --arm lolo. "
                         "Implicit trial, adica protocolul de pana acum. `test` il aliniaza cu w si "
                         "cu bratul A, care se potrivesc deja pe testul celorlalte 9 limbi.")
    ap.add_argument("--ens", action="store_true",
                    help="semnalul A devine ansamblul celor doua brate de transfer, "
                         "z(w_src*z(p_en) + (1-w_src)*z(p_multi)), cu w_src ales LOLO pe grila de "
                         "9 puncte. Fara el w_src = 0, adica A = p_multi, adica exact ce era.")
    ap.add_argument("--a-set", dest="a_set", action="append", default=None, metavar="NUME=CALE",
                    help="set candidat de trasaturi pentru semnalul A, repetabil. Dat de mai multe "
                         "ori, setul limbii L se alege si el LOLO, ca w_src si w.")
    ap.add_argument("--tag", default=None,
                    help="numele configuratiei. Scrie in output/e_fusion_<brat>_<tag>.md si in "
                         "CSV-urile alaturate, deci nu atinge nimic din ce e publicat. Obligatoriu "
                         "pentru --ens si --a-set.")
    ap.add_argument("--vs", default=None,
                    help="predictii per instanta ale configuratiei de comparat, de exemplu "
                         "output/fusion_preds_lolo_fittest_lemma.csv. Adauga in raport bootstrap-ul "
                         "pereche al diferentei, cu P(>0).")
    ap.add_argument("--b-dir", dest="b_dir", default=None,
                    help="director alternativ, relativ la output/, din care se citesc CSV-urile "
                         "semnalului B pe TEST. Fara el, cele canonice din output/bakeoff_test/, deci "
                         "cifra publicata se reproduce fara niciun flag. Cere --tag.")
    ap.add_argument("--h", default=None, choices=["entropie", "dezacord", "zgomot"],
                    help="activeaza ponderea PER ITEM: w_i = clip(w + a*h_i, 0, 1), cu `a` ales LOLO "
                         "impreuna cu w, pe o grila care CONTINE zero. Fara el, ponderea scalara de "
                         "pana acum, si `fit_choice` merge pe forma inchisa, neatinsa. Cere --h-src "
                         "si --tag.")
    ap.add_argument("--h-src", dest="h_src", default=None,
                    help="CSV de distributii din care se calculeaza h, de exemplu "
                         "output/dist/gemma4-12b-4bit_test.csv")
    ap.add_argument("--h-seed", dest="h_seed", type=int, default=0,
                    help="samanta pentru --h zgomot, adica pentru podeaua de zgomot")
    ap.add_argument("--a-pas", dest="a_pas", type=float, default=0.1,
                    help="pasul grilei lui a; grila e de la -3*pas la +3*pas, sapte puncte, cu zero "
                         "in mijloc")
    ap.add_argument("--preds-a", dest="preds_a", default=None,
                    help="alt fisier pentru semnalul A, de exemplu output/e1_frozen_preds_lemma.csv. "
                         "Toate iesirile primesc sufixul _lemma, deci fuziunea publicata nu se atinge.")
    a = ap.parse_args()
    global A_SETS, B_DIR, A_GRID, H_MAP, H_NUME
    if a.h:
        if not a.h_src:
            raise SystemExit("--h cere --h-src")
        if not a.tag:
            raise SystemExit("--h cere --tag: o pondere schimbata n-are voie sa scrie peste "
                             "raportul configuratiei publicate")
        q = a.h_src if os.path.isabs(a.h_src) else os.path.join(HERE, a.h_src)
        if not os.path.exists(q):
            raise SystemExit(f"--h-src: {q} lipseste")
        H_MAP, H_NUME = h_from_dist(a.h, q, a.h_seed)
        A_GRID = np.round(np.arange(-3, 4) * float(a.a_pas), 6)
        print(f"[F] pondere per item: h = {H_NUME}, grila lui a "
              f"{list(A_GRID)} ({len(A_GRID)}x{len(GRID)} perechi)", flush=True)
    if a.b_dir:
        if not a.tag:
            raise SystemExit("--b-dir cere --tag: un semnal B schimbat nu are voie sa scrie peste "
                             "raportul configuratiei publicate")
        d = a.b_dir if os.path.isabs(a.b_dir) else os.path.join(OUT, os.path.basename(a.b_dir))
        if not os.path.isdir(d):
            raise SystemExit(f"--b-dir: {d} nu e un director")
        B_DIR = os.path.basename(d.rstrip(os.sep))
        print(f"[F] semnalul B de test din output/{B_DIR}/, nu din output/bakeoff_test/", flush=True)
    if a.preds_a:
        # Se schimba si sursa lui A, si numele iesirilor. Doar prima ar suprascrie tacit fuziunea
        # publicata cu una calculata pe alt semnal, adica exact felul de eroare care nu s-ar vedea in
        # nicio cifra din raport.
        global PREDS_A, SUF
        PREDS_A = a.preds_a if os.path.isabs(a.preds_a) else os.path.join(HERE, a.preds_a)
        if not os.path.exists(PREDS_A):
            raise SystemExit(f"{PREDS_A} lipseste. Ruleaza intai finetune_xlmr.py --frozentrial --lemma-freq")
        SUF = {k: v + "_lemma" for k, v in SUF.items()}
        global CMP_REPORT, CMP_TABLE, SUMMARY
        CMP_REPORT, CMP_TABLE, SUMMARY = (f"{a}_lemma{b}" for a, b in
                                          (os.path.splitext(x) for x in (CMP_REPORT, CMP_TABLE, SUMMARY)))
        print(f"[F] semnalul A din {os.path.basename(PREDS_A)}, iesiri cu sufixul _lemma", flush=True)

    A_SETS = {"A": PREDS_A}
    if a.a_set:
        A_SETS = {}
        for spec in a.a_set:
            if "=" not in spec:
                raise SystemExit(f"--a-set vrea NUME=CALE, am primit {spec!r}")
            name, path = spec.split("=", 1)
            q = path if os.path.isabs(path) else os.path.join(HERE, path)
            if not os.path.exists(q):
                raise SystemExit(f"--a-set {name}: {q} lipseste. Ruleaza intai "
                                 f"finetune_xlmr.py --frozentrial --afeat {name}")
            A_SETS[name] = q
    if (a.ens or a.a_set) and not a.tag:
        raise SystemExit("--ens si --a-set cer --tag, ca sa nu suprascrie fuziunea publicata")
    if a.tag:
        if a.fit == "both":
            raise SystemExit("--tag nu merge cu --fit both: configuratia cu ansamblu se raporteaza "
                             "pe un singur split de potrivire")
        return fuse_ens(a.arm, a.boot, a.fit, asets=tuple(A_SETS),
                        src_grid=SRC_GRID if a.ens else np.array([0.0]), tag=a.tag, vs=a.vs,
                        pick_split=a.pick_split)
    return fuse(a.arm, a.boot, a.fit, a.pick_split)


if __name__ == "__main__":
    raise SystemExit(main())
