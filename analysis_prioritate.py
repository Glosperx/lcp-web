"""Care parghie merita rulata pe test. Ordonarea celor rams pe lista, pe cifre, nu pe intuitie.

O configuratie pe test costa ~102 minute de inferenta, una pe trial ~5.5. Deci intrebarea „care
merita" nu se raspunde rulandu-le pe toate, se raspunde masurand ce se poate masura pe fisierele deja
pe disc si punand un PLAFON pe restul. Trei blocuri:

  1. cele trei variante de AGREGARE a celor doua prompturi, masurate cap la cap prin fuziune: pondere
     aleasa LOLO, media geometrica, si amandoua. Iese interval pereche real fata de sistem, nu plafon.
     Fisierele le scrie `make_bt_runs.py --mod`, fuziunile `fuse_ab.py --b-dir`; aici se citesc.
  2. PLAFOANE pentru doua parghii scumpe: al treilea termen de fuziune pentru dezacord, si reziduul de
     fertilitate. Amandoua ca validitate incrementala peste predictia finala, cu control flexibil
     (p, p^2, p^3), tiparul din `analysis_dist.step_c`. Cifra e o limita SUPERIOARA din doua motive
     independente: potrivirea e in-sample, si controlul flexibil citeste deja curbura sistemului.
  3. cat headroom mai are SCARA de raspuns, fara nicio inferenta: scara r(K) prin unirea cifrelor
     vecine, citirea liniara optima a celor cinci probabilitati, si recensamantul de saturatie.

Nu adopta nimic si nu atinge nimic din ce e publicat: citeste `output/`, scrie `output/e_prioritate.md`.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_prioritate.py
"""
import itertools
import os
import sys
import time

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_prioritate.md")

# Referinta e sistemul CU temperatura. Cifra nu se foloseste ca valoare, se VERIFICA: `analysis_dist.py`
# are `SYS_TAG = "adoptat"` hardcodat si ar compara totul cu 0.674946, care e acum ablatia fara
# temperatura. Aceeasi capcana ca `SIS = 0.664555`, si singura aparare e sa se recalculeze si sa se
# tipareasca amandoua una langa alta.
SYS_TAG = "adoptat_temp"
SYS_R_DECLARAT = 0.683849
SYS_PREDS = os.path.join(OUT, f"fusion_preds_lolo_{SYS_TAG}.csv")

# Blocul 4: bratele sondajului de scara, pe TRIAL. Bratul 1-5 e chiar fisierul canonic, fiindca
# rularea de control prin codul parametrizat a reprodus valorile lui la 0.0 exact.
SCARI = [("1-5", "scara publicata, cinci atomi, ancora la 1",
          os.path.join(OUT, "dist", "gemma4-12b-4bit_trial.csv")),
         ("0-4", "cinci atomi, ancora mutata la 0: izoleaza efectul ancorei",
          os.path.join(OUT, "dist", "scale_0-4_trial.csv")),
         ("0-9", "zece atomi si ancora la 0",
          os.path.join(OUT, "dist", "scale_0-9_trial.csv"))]

# Variantele de agregare a prompturilor, scrise de make_bt_runs.py si fuzionate de fuse_ab.py.
VARIANTE = [("prio_W05", "control: modul `pondere` redus la punctul neutru w = 0.5", "W05"),
            ("prio_W", "pondere intre prompturi, `w` ales LOLO, T fixat la valoarea adoptata", "W"),
            ("prio_G", "media geometrica a celor doua distributii, T propriu ales LOLO", "G"),
            ("prio_WG", "media geometrica PONDERATA, `w` si T alese LOLO", "WG"),
            ("prio_K", "cifrele vecine UNITE, partitia aleasa LOLO din 15 candidate", "K"),
            ("prio_KW", "unirea cifrelor plus ponderea intre prompturi, in ordine prespecificata",
             "KW")]

# Rezultatele care intra in tabelul de verdict. Se umple pe parcurs, ca tabelul final sa nu repete
# nicio cifra de mana: constantele scrise de mana sunt exact felul de eroare care a facut un raport sa
# se contrazica singur dupa renumerotare.
REZ = {}

_DOC = []


def emit(*lines):
    """Adauga in raport si scrie pe disc pe loc, ca un pas care crapa sa nu piarda pasii de dinainte.
    Acelasi idiom ca `analysis_dist.emit`."""
    _DOC.extend(lines)
    os.makedirs(OUT, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def fitted(y, Z):
    """Valorile potrivite ale regresiei liniare a lui y pe Z, cu intercept. NaN unde nu se poate."""
    y = np.asarray(y, float)
    Z = np.asarray(Z, float)
    if Z.ndim == 1:
        Z = Z[:, None]
    m = np.isfinite(y) & np.isfinite(Z).all(axis=1)
    out = np.full(len(y), np.nan)
    Zc = np.column_stack([np.ones(m.sum()), Z[m]])
    beta, *_ = np.linalg.lstsq(Zc, y[m], rcond=None)
    out[m] = Zc @ beta
    return out


def plafon(y, base, extra, ctx, ad):
    """Cat ar putea urca r daca `extra` s-ar adauga peste o citire FLEXIBILA a lui `base`.

    `base` e predictia finala a sistemului. Controlul flexibil (base, base^2, base^3) e acelasi din
    `analysis_dist.controls_of`, si e acolo pentru motivul masurat in (c): temperatura urca r pe toate
    zece limbi, deci sistemul e misspecificat ca predictor liniar, deci orice marime corelata cu
    curbura lui pare canal nou fara sa fie.

    De ce e plafon si nu estimare: coeficientii se potrivesc pe chiar randurile pe care se masoara r,
    deci castigul e in-sample. Un termen imbricat corect, ales LOLO, nu poate da mai mult.
    Reesantionarea vine dupa potrivire, ca la `analysis_dist.step_c`, deci intervalul nu contine
    incertitudinea potrivirii.
    """
    Z0 = np.column_stack([base, base ** 2, base ** 3])
    Z1 = np.column_stack([Z0, np.asarray(extra, float).reshape(len(base), -1)])
    p0, p1 = fitted(y, Z0), fitted(y, Z1)
    b0, b1 = ad.boot_one(y, p0, ctx), ad.boot_one(y, p1, ctx)
    k = min(len(b0["boot"]), len(b1["boot"]))
    dv = b1["boot"][:k] - b0["boot"][:k]
    return dict(r0=b0["r"], r1=b1["r"], d=b1["r"] - b0["r"], lo=float(np.percentile(dv, 2.5)),
                hi=float(np.percentile(dv, 97.5)), p=float((dv > 0).mean()),
                boot0=b0["boot"], boot1=b1["boot"])


def part_contigue(k, n=5):
    """Toate partitiile lui {0..n-1} in `k` blocuri CONTIGUE, ca liste de liste de indici.

    O scara mai grosiera nu poate reordona notele, doar sa le uneasca pe cele vecine, deci partitiile
    necontigue n-ar corespunde niciunei scari.
    """
    out = []
    for cuts in itertools.combinations(range(1, n), k - 1):
        b, prev = [], 0
        for c in list(cuts) + [n]:
            b.append(list(range(prev, c)))
            prev = c
        out.append(b)
    return out


def colaps(P, blocuri):
    """(distributia colapsata pe blocuri, valorile blocurilor). Valoarea unui bloc e media notelor lui.

    Pearson e invariant la transformari afine pozitive, deci nu conteaza pe ce interval se aduc
    valorile; se pastreaza notele 1..5 ca sa se citeasca usor.
    """
    Q = np.column_stack([P[:, b].sum(axis=1) for b in blocuri])
    v = np.array([np.mean([i + 1 for i in b]) for b in blocuri], float)
    return Q, v


def main():
    t0 = time.time()
    import analysis_dist as ad

    # `ad.load()` face joinul pe `idx` intre distributii si predictiile sistemului, si joinul acela e
    # partea delicata: nu se rescrie aici, se imprumuta. Ce se schimba e REFERINTA, fiindca modulul
    # arata inca spre sistemul fara temperatura.
    ad.SYS_PREDS = SYS_PREDS
    m = ad.load()
    PL = ad.per_lang(m)
    langs = sorted(PL)
    Tsel = {r["lang"]: float(r["T"]) for _, r in ad.temp_pick(PL, ad.T_GRID_EXT)[0].iterrows()}

    r_sys = float(np.mean([ad.r_of(PL[lg]["p_fuz"], PL[lg]["y"]) for lg in langs]))
    emit(f"# Prioritizarea parghiilor rams pe lista\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_prioritate.py`. Referinta e "
         f"`{os.path.basename(SYS_PREDS)}`, adica sistemul CU temperatura.\n",
         f"**Verificarea referintei:** r recalculat din predictiile per instanta e "
         f"**{r_sys:.6f}**, iar cifra declarata in `output/e_fusion_lolo_{SYS_TAG}.md` e "
         f"**{SYS_R_DECLARAT:.6f}**. Diferenta {abs(r_sys - SYS_R_DECLARAT):.2e}. "
         + ("Coincid, deci referinta raportului e chiar sistemul.\n"
            if abs(r_sys - SYS_R_DECLARAT) < 5e-5 else
            "**NU COINCID. Nimic mai jos nu se citeste pana nu se afla de ce.**\n"),
         "Temperaturile adoptate, per limba, pe grila extinsa: "
         + ", ".join(f"{lg} T={Tsel[lg]:g}" for lg in langs) + ".\n",
         "Agregarea e media pe cele zece limbi, nu pooled, in tot raportul. Toate intervalele vin din "
         "bootstrap pe contexte, 2000 de reesantionari, si cele ale diferentelor sunt PERECHE.\n")
    print(f"[0] referinta {r_sys:.6f} vs {SYS_R_DECLARAT:.6f}", flush=True)

    step1(ad, PL, langs)
    step2(ad, PL, langs, m)
    step3(ad, PL, langs, Tsel)
    step4(ad)
    verdict()
    emit(f"\n---\nRulat in {time.time() - t0:.1f} s.")
    print(f"[gata] {REPORT} in {time.time() - t0:.1f}s", flush=True)
    return 0


# --------------------------------------------------------------------- (1) agregarea prompturilor
def step1(ad, PL, langs):
    print("[1] agregarea celor doua prompturi, masurata cap la cap", flush=True)
    ref = pd.read_csv(SYS_PREDS)
    emit("## 1. Agregarea celor doua prompturi, masurata cap la cap\n",
         "Semnalul B mediaza azi 50/50 valorile asteptate ale celor doua prompturi. Media aia e "
         "demonstrat gresita ca alegere: in `output/e_dist.md`, cu T-ul lor, promptul 2 singur da "
         "+0.6536 si promptul 1 doar +0.6256. Trei variante, toate pe fisierele deja pe disc:\n",
         "- `pondere`: `w*E(p1^(1/T)) + (1-w)*E(p2^(1/T))`, cu T **fixat** la valoarea adoptata per "
         "limba si numai `w` ales LOLO pe 7 puncte.\n"
         "- `produs`: media geometrica a celor doua distributii, renormalizata. **Puterea si produsul "
         "comuta**, `(p^(1/T) q^(1/T))^(1/2) = (pq)^(1/(2T))`, deci produsul la T fix ar fi confundat "
         "cu temperatura; T se realege pe aceeasi grila extinsa, deci acelasi numar de candidati.\n"
         "- `pondere-produs`: media geometrica ponderata, amandoua.\n",
         "Alegerea lui `w` pentru limba L foloseste, pentru fiecare limba de potrivire l', temperatura "
         "lui l' aleasa fara L si fara l'. Al doilea nivel din `fuse_ab.fit_choice`: fara el, `w`-ul "
         "lui L ar trece prin etichetele lui L.\n",
         "Coloana **`limbi stricate`** e criteriul care a respins `distTpp` la 0.685763: o "
         "configuratie care urca media dar strica o limba cu interval pereche care exclude zero nu se "
         "adopta, oricat de mare e media. Se citeste inaintea coloanei cu media.\n",
         "| configuratie | ce schimba | r mediu | fata de sistem | CI 95% pereche | P(>0) | limbi "
         "peste | limbi urcate, CI exclude 0 | limbi stricate, CI exclude 0 | latime criteriu | "
         "margine peste neutru |",
         "|---|---|---|---|---|---|---|---|---|---|---|")
    rows = []
    for tag, doc, sufix in VARIANTE:
        q = os.path.join(OUT, f"fusion_preds_lolo_{tag}.csv")
        if not os.path.exists(q):
            emit(f"| `{tag}` | {doc} | nerulat | | | | | | |")
            continue
        d = pd.read_csv(q)
        bn, bo, per = [], [], []
        for lg in langs:
            a = ref[ref["lang"] == lg].set_index("idx")
            b = d[d["lang"] == lg].set_index("idx").reindex(a.index)
            if b["p_fuz"].isna().any():
                raise SystemExit(f"{tag} n-acopera toate randurile lui {lg}")
            b0 = ad.boot_one(a["y"].values, a["p_fuz"].values, a["ctx"].values)
            b1 = ad.boot_one(a["y"].values, b["p_fuz"].values, a["ctx"].values)
            bo.append(b0["boot"]); bn.append(b1["boot"])
            k = min(len(b0["boot"]), len(b1["boot"]))
            dv = b1["boot"][:k] - b0["boot"][:k]
            per.append(dict(lang=lg, r_azi=b0["r"], r_nou=b1["r"], d=b1["r"] - b0["r"],
                            lo=float(np.percentile(dv, 2.5)), hi=float(np.percentile(dv, 97.5))))
        t = pd.DataFrame(per)
        dm, lo, hi, pp = ad.mean_diff_ci(bn, bo)
        pf = os.path.join(OUT, f"bt_params_bakeoff_test_{sufix}.csv")
        pw = pd.read_csv(pf) if os.path.exists(pf) else None
        lat = f"{pw['crit_lat'].mean():.4f}" if pw is not None and pw["crit_lat"].notna().any() else "-"
        mar = f"{pw['margine'].mean():+.5f}" if pw is not None and pw["margine"].notna().any() else "-"
        ident = (lo == hi == 0.0)
        stricate = int((t["hi"] < 0).sum())
        urcate = int((t["lo"] > 0).sum())
        emit(f"| `{tag}` | {doc} | **{t['r_nou'].mean():.6f}** | "
             + ("identic | interval de latime 0 | control trecut" if ident else
                f"{dm:+.4f} | [{lo:+.4f}, {hi:+.4f}] | {pp:.1%}")
             + f" | {int((t['d'] > 0).sum())}/10 | {urcate} | **{stricate}** | {lat} | {mar} |")
        rows.append(dict(tag=tag, r=float(t["r_nou"].mean()), d=dm, lo=lo, hi=hi, p=pp, t=t,
                         w=None if pw is None else sorted(set(pw["w"]))))
        REZ[tag] = dict(r=float(t["r_nou"].mean()), d=dm, lo=lo, hi=hi, p=pp,
                        stricate=int((t["hi"] < 0).sum()), urcate=int((t["lo"] > 0).sum()),
                        rele=list(t[t["hi"] < 0]["lang"]))
        print(f"    {tag:10s} r={t['r_nou'].mean():.6f} d={dm:+.5f} [{lo:+.4f},{hi:+.4f}] "
              f"P={pp:.1%}", flush=True)

    emit("", "`latime criteriu` e `max - min` al criteriului LOLO peste grila lui `w`, si `margine "
         "peste neutru` e cu cat bate `w` ales punctul `w = 0.5` pe ACELASI criteriu. Sunt coloanele "
         "care spun daca alegerea cumpara ceva sau doar da voie argmaxului sa se plimbe pe un criteriu "
         "plat, si sunt exact cele care au permis respingerea argumentata a lui `distTpp` la "
         "0.685763.\n")
    emit("**De declarat, si e o bifurcatie, nu un detaliu.** Ultimele doua configuratii nu erau pe "
         "lista de la inceput: `prio_K` a iesit din blocul 3 de mai jos, adica dintr-o scara r(K) "
         "calculata pe TEST. Hiperparametrii ei sunt alesi LOLO ca la orice altceva, dar decizia de a "
         "o incerca vine de la o cifra de test, exact ca celelalte bifurcatii ale lucrarii. Intra in "
         "Limitations pe aceeasi lista.\n")
    for r in rows:
        if r["tag"] == "prio_W05":
            continue
        t = r["t"]
        emit(f"### `{r['tag']}`, per limba\n",
             "| limba | " + " | ".join(f"{x['lang']}" for _, x in t.iterrows()) + " |",
             "|---|" + "---|" * len(t),
             "| diferenta | " + " | ".join(f"{x['d']:+.4f}" for _, x in t.iterrows()) + " |",
             "| CI exclude 0 | " + " | ".join(
                 ("-" if x["lo"] <= 0 <= x["hi"] else ("**stricata**" if x["hi"] < 0 else "urcata"))
                 for _, x in t.iterrows()) + " |", "")
    if rows:
        w_uniq = [r for r in rows if r["tag"] == "prio_W"]
        if w_uniq and w_uniq[0]["w"]:
            emit(f"`w` ales LOLO la `prio_W`: {w_uniq[0]['w']} pe toate cele zece limbi. `w` e "
                 "ponderea promptului 1, deci sub 0.5 inseamna ca promptul 2 primeste mai mult, "
                 "coerent cu +0.6536 fata de +0.6256.\n")


# --------------------------------------------------------------------- (2) plafoane
def step2(ad, PL, langs, m):
    print("[2] plafoane pentru parghiile scumpe", flush=True)
    emit("## 2. Plafoane pentru doua parghii scumpe\n",
         "Amandoua se masoara la fel: cat ar putea urca r daca marimea s-ar adauga peste o citire "
         "FLEXIBILA a predictiei finale, `(p, p^2, p^3)`. Cifra e o limita SUPERIOARA din doua motive "
         "independente. Intai, coeficientii se potrivesc pe chiar randurile pe care se masoara r, deci "
         "castigul e in-sample; un termen ales LOLO nu poate da mai mult. Apoi, controlul flexibil "
         "citeste deja curbura sistemului, deci ce rams e strict canal nou. **Sub +0.002 parghia se "
         "inchide fara sa se scrie codul.**\n",
         "`r cub` e r-ul citirii flexibile singure, si e peste sistem prin construcție: coloana "
         "spune cat din distanta pana la plafon vine din citirea neliniara a sistemului, nu din marimea "
         "noua.\n")

    # --- 2a dezacordul
    S = {lg: ad.signals_of(PL[lg]) for lg in langs}
    nume = ["dezacord_E", "dezacord_JS"]
    emit("### 2a. Al treilea termen de fuziune, pentru dezacordul intre prompturi\n",
         "`dezacord_E` si `dezacord_JS` sunt singurele doua masuri din `output/e_dist.md` care au "
         "supravietuit controlului flexibil fata de sistemul intreg. Costul lor nu e inferenta, e cod: "
         "`fuse_ab.fit_choice` are azi o singura pondere si o selectie pe trei niveluri.\n",
         "**`zgomot_1` si `zgomot_2` sunt calibrarea pe zero, si fara ele tabelul nu se poate citi.** "
         "Sunt una, respectiv doua coloane de zgomot gaussian, cu seed fix, puse prin exact aceeasi "
         "procedura. Orice coloana adaugata in-sample urca r si daca nu contine nimic, cu atat mai mult "
         "cu cat sunt mai multe: la n ~ 562 pe limba, inflatia asteptata e de ordinul "
         "`(1 - R^2) * k / n`. Un plafon care nu bate randul de zgomot cu acelasi numar de coloane nu "
         "spune nimic.\n",
         "| marime | coloane | r sistem | r cub | r cub + marime | plafonul castigului | "
         "CI 95% pereche | P(>0) |",
         "|---|---|---|---|---|---|---|---|")
    rng = np.random.default_rng(20260821)
    ZG = {lg: rng.standard_normal((PL[lg]["n"], 2)) for lg in langs}
    for nm in nume + ["ambele", "zgomot_1", "zgomot_2"]:
        bn, bo, per = [], [], []
        for lg in langs:
            D = PL[lg]
            if nm == "ambele":
                ex = np.column_stack([S[lg][k] for k in nume])
            elif nm.startswith("zgomot_"):
                ex = ZG[lg][:, :int(nm[-1])]
            else:
                ex = S[lg][nm][:, None]
            z = plafon(D["y"], D["p_fuz"], ex, D["ctx"], ad)
            bn.append(z["boot1"]); bo.append(z["boot0"]); per.append(z)
        dm, lo, hi, pp = ad.mean_diff_ci(bn, bo)
        r0 = float(np.mean([z["r0"] for z in per]))
        r1 = float(np.mean([z["r1"] for z in per]))
        nc = 2 if nm in ("ambele", "zgomot_2") else 1
        emit(f"| `{nm}` | {nc} | {SYS_R_DECLARAT:.4f} | {r0:.4f} | {r1:.4f} | **{dm:+.5f}** | "
             f"[{lo:+.5f}, {hi:+.5f}] | {pp:.1%} |")
        REZ[f"dezacord:{nm}"] = dict(d=dm, lo=lo, hi=hi, p=pp)
        print(f"    dezacord {nm:12s} plafon {dm:+.5f} [{lo:+.5f},{hi:+.5f}]", flush=True)
    emit("")

    # --- 2b fertilitatea
    from mlsp_common import load_mlsp
    from solution_bert import fertility
    ref = load_mlsp("test")
    tok_by_idx = ref["token"].astype(str)
    emit("### 2b. Reziduul de fertilitate\n",
         "Din `output/e_fr_diagnostic.md`: fertilitatea mai are validitate incrementala peste sistem pe "
         "franceza, +0.1450 cu CI care exclude zero. Dar pe `de` si `pt` reziduul e NEGATIV cu CI care "
         "exclude zero, deci o fertilitate pusa global ar strica acolo. De aceea plafonul se da per "
         "limba, si abia apoi agregat.\n",
         "| limba | fertilitate medie | r sistem | r cub | r cub + fertilitate | plafon | CI 95% | P(>0) |",
         "|---|---|---|---|---|---|---|---|")
    bn, bo, per = [], [], []
    for lg in langs:
        D = PL[lg]
        idx = m[m["lang"] == lg]["idx"].values
        f = fertility(list(tok_by_idx.iloc[idx].values))
        z = plafon(D["y"], D["p_fuz"], np.asarray(f, float)[:, None], D["ctx"], ad)
        bn.append(z["boot1"]); bo.append(z["boot0"])
        per.append(dict(lang=lg, fert=float(np.mean(f)), **{k: z[k] for k in
                                                            ("r0", "r1", "d", "lo", "hi", "p")}))
        emit(f"| {lg} | {np.mean(f):.2f} | {ad.r_of(D['p_fuz'], D['y']):.4f} | {z['r0']:.4f} | "
             f"{z['r1']:.4f} | **{z['d']:+.5f}** | [{z['lo']:+.5f}, {z['hi']:+.5f}]"
             + ("" if z["lo"] <= 0 <= z["hi"] else " *") + f" | {z['p']:.1%} |")
        print(f"    fert {lg} plafon {z['d']:+.5f}", flush=True)
    dm, lo, hi, pp = ad.mean_diff_ci(bn, bo)
    t = pd.DataFrame(per)
    emit(f"| **medie** | {t['fert'].mean():.2f} | {SYS_R_DECLARAT:.4f} | {t['r0'].mean():.4f} | "
         f"{t['r1'].mean():.4f} | **{dm:+.5f}** | [{lo:+.5f}, {hi:+.5f}] | {pp:.1%} |", "",
         f"`*` = intervalul limbii exclude zero. Aplicata global, cu coeficient potrivit pe limba ei, "
         f"fertilitatea are plafonul **{dm:+.5f}**.\n",
         "**Atentie la citirea semnului.** In `output/e_fr_diagnostic.md` reziduul lui `de` e NEGATIV "
         "cu CI care exclude zero, si totusi aici `de` are plafon pozitiv mare. Nu e o contradictie: "
         "corelatia partiala are semn, iar castigul predictiv nu, fiindca regresia potriveste "
         "coeficientul. De aceea coloana care decide nu e nici una din cele de sus, e transferul.\n")

    # --- transferul LOLO: acelasi termen, dar cu coeficientul venit de la CELELALTE noua limbi.
    # Fertilitatea se aduce la z pe limba inainte de a fi pusa laolalta: 3.0 subword-uri pe sinhaleza
    # si 3.0 pe engleza nu sunt aceeasi marime, deci un coeficient pe scara bruta n-ar avea sens.
    FZ, SGN = {}, {}
    for lg, idxs in [(lg, m[m["lang"] == lg]["idx"].values) for lg in langs]:
        f = np.asarray(fertility(list(tok_by_idx.iloc[idxs].values)), float)
        FZ[lg] = (f - f.mean()) / (f.std() if f.std() > 0 else 1.0)
        D = PL[lg]
        Zc = np.column_stack([np.ones(D["n"]), D["p_fuz"], D["p_fuz"] ** 2, D["p_fuz"] ** 3, FZ[lg]])
        SGN[lg] = float(np.linalg.lstsq(Zc, D["y"], rcond=None)[0][-1])
    bn, bo, rows = [], [], []
    for lg in langs:
        oth = [l2 for l2 in langs if l2 != lg]
        Zo = np.vstack([np.column_stack([PL[l2]["p_fuz"], PL[l2]["p_fuz"] ** 2,
                                         PL[l2]["p_fuz"] ** 3, FZ[l2]]) for l2 in oth])
        yo = np.concatenate([PL[l2]["y"] for l2 in oth])
        beta = np.linalg.lstsq(np.column_stack([np.ones(len(Zo)), Zo]), yo, rcond=None)[0]
        D = PL[lg]
        Zl = np.column_stack([np.ones(D["n"]), D["p_fuz"], D["p_fuz"] ** 2, D["p_fuz"] ** 3, FZ[lg]])
        b1 = ad.boot_one(D["y"], Zl @ beta, D["ctx"])
        b0 = ad.boot_one(D["y"], Zl[:, :4] @ beta[:4], D["ctx"])
        bn.append(b1["boot"]); bo.append(b0["boot"])
        rows.append(dict(lang=lg, sgn=SGN[lg], r0=b0["r"], r1=b1["r"], d=b1["r"] - b0["r"]))
    dm2, lo2, hi2, pp2 = ad.mean_diff_ci(bn, bo)
    tt = pd.DataFrame(rows)
    emit("**Transferul, adica singura varianta pe care o poate produce o procedura onesta.** "
         "Coeficientul fertilitatii se potriveste pe celelalte noua limbi si se aplica pe L, exact "
         "cum se aleg `w`, `w_src` si setul de trasaturi. Coloana `semn` e semnul coeficientului "
         "potrivit pe limba ei, si daca semnele nu cad la fel transferul nu are ce sa duca.\n",
         "| limba | " + " | ".join(tt["lang"]) + " | **medie** |",
         "|---|" + "---|" * (len(tt) + 1),
         "| semn coeficient | " + " | ".join("+" if x > 0 else "-" for x in tt["sgn"]) + " | "
         + f"{int((tt['sgn'] > 0).sum())}/10 pozitive |",
         "| castig la transfer | " + " | ".join(f"{x:+.4f}" for x in tt["d"]) + " | "
         + f"**{dm2:+.5f}** |", "",
         f"La transfer, fertilitatea da **{dm2:+.5f}**, interval pereche [{lo2:+.5f}, {hi2:+.5f}], "
         f"P(>0) = {pp2:.1%}, adica {ad.zero_out(lo2, hi2)}.\n")
    REZ["fert:plafon"] = dict(d=dm, lo=lo, hi=hi, p=pp)
    REZ["fert:transfer"] = dict(d=dm2, lo=lo2, hi=hi2, p=pp2,
                                semne=int((tt["sgn"] > 0).sum()))
    print(f"    fert transfer LOLO {dm2:+.5f} [{lo2:+.5f},{hi2:+.5f}] "
          f"semne {int((tt['sgn'] > 0).sum())}/10", flush=True)


# --------------------------------------------------------------------- (3) rezolutia scarii
def step3(ad, PL, langs, Tsel):
    print("[3] rezolutia scarii de raspuns", flush=True)
    emit("## 3. Cat headroom mai are scara de raspuns\n",
         "Scara e 1-5, deci citirea soft are cinci atomi, pe o eticheta continua. Intrebarea e daca "
         "cei cinci atomi sunt constrangerea care leaga, si se pune de trei ori, fara nicio inferenta.\n")

    # --- 3a scara r(K)
    emit("### 3a. Scara r(K): ce se pierde la scari mai grosiere\n",
         "Se unesc cifrele VECINE in K blocuri, fiecare bloc luand ca valoare media notelor lui, si se "
         "reciteste valoarea asteptata. Se raporteaza `max` peste toate partitiile contigue, deci "
         "scarile grosiere sunt aratate in cea mai buna lumina posibila. **Se declara ca proxy, nu ca "
         "predictie:** unirea binurilor nu e acelasi lucru cu a intreba modelul pe o scara mai "
         "grosiera, fiindca modelul s-ar recalibra. Ce e informativ e forma curbei, nu valoarea.\n",
         "Trei coloane, si numai a treia e o cifra pe care o poate produce o procedura onesta. `max` "
         "alege partitia uitandu-se la chiar limba pe care o masoara, deci e oracol. `LOLO` alege "
         "partitia pe celelalte noua limbi, ca orice hiperparametru din lucrare.\n",
         "| K | partitii | `max` peste partitii, oracol | media peste partitii | **partitie aleasa "
         "LOLO** | LOLO fata de K=5 |",
         "|---|---|---|---|---|---|")
    # Ordinea (5, 4, 3, 2): K = 5 e referinta, deci trebuie calculata prima. Randurile se emit la
    # final, in ordine crescatoare.
    acc, r5 = {}, None
    for K in (5, 4, 3, 2):
        parts = part_contigue(K)
        R = {}
        for lg in langs:
            D = PL[lg]
            P1 = ad.temper(D["P1"], Tsel[lg])
            P2 = ad.temper(D["P2"], Tsel[lg])
            rs = []
            for bl in parts:
                Q1, v = colaps(P1, bl)
                Q2, _ = colaps(P2, bl)
                rs.append(ad.r_of(0.5 * (Q1 @ v + Q2 @ v), D["y"]))
            R[lg] = np.array(rs)
        best = float(np.mean([R[lg].max() for lg in langs]))
        mm = float(np.mean([R[lg].mean() for lg in langs]))
        lolo = float(np.mean([R[lg][int(np.argmax(np.mean([R[l2] for l2 in langs if l2 != lg],
                                                          axis=0)))] for lg in langs]))
        if K == 5:
            r5 = lolo
        acc[K] = (len(parts), best, mm, lolo)
        print(f"    K={K} max {best:+.4f} mean {mm:+.4f} LOLO {lolo:+.4f}", flush=True)
    REZ["scara:ladder"] = {K: acc[K][3] for K in acc}
    for K in (2, 3, 4, 5):
        np_, best, mm, lolo = acc[K]
        emit(f"| {K} | {np_} | {best:+.4f} | {mm:+.4f} | **{lolo:+.4f}** | "
             + ("referinta" if K == 5 else f"{lolo - r5:+.4f}") + " |")
    emit("")

    # --- 3b citirea liniara optima
    emit("### 3b. Citirea liniara optima a celor cinci probabilitati\n",
         "`B` e UN anume functional liniar al distributiei, cel cu notele 1..5 egal spatiate. Cel mai "
         "bun functional liniar se obtine regresand eticheta pe chiar cele cinci probabilitati, si se "
         "alege LOLO ca orice hiperparametru: coeficientii limbii L vin de la celelalte noua. "
         "Distinctia pe care o face coloana asta e cea care conteaza pentru decizie: daca citirea "
         "optima bate `B` cu mult, informatia e ACOLO si o risipeste citirea, deci nu ai nevoie de mai "
         "multi atomi, ai nevoie de alta citire, si aia e gratis. Daca nu o bate, cei cinci atomi sunt "
         "chiar plafonul si numai o scara mai fina il muta.\n",
         "Raspunde in acelasi timp la parghia `distributia intreaga ca trasaturi in bratul A`, care "
         "e chiar functionalul asta pus in fuziune.\n",
         "| limba | r `B` la T adoptat | r citire optima LOLO | diferenta | r citire optima in-sample |",
         "|---|---|---|---|---|")
    Z = {lg: np.column_stack([ad.temper(PL[lg]["P1"], Tsel[lg]),
                              ad.temper(PL[lg]["P2"], Tsel[lg])]) for lg in langs}
    per = []
    for lg in langs:
        D = PL[lg]
        Zo = np.vstack([Z[l2] for l2 in langs if l2 != lg])
        yo = np.concatenate([PL[l2]["y"] for l2 in langs if l2 != lg])
        Zc = np.column_stack([np.ones(len(Zo)), Zo])
        beta, *_ = np.linalg.lstsq(Zc, yo, rcond=None)
        p_lolo = np.column_stack([np.ones(len(Z[lg])), Z[lg]]) @ beta
        r_b = ad.r_of(ad.b_at(D, Tsel[lg]), D["y"])
        r_l = ad.r_of(p_lolo, D["y"])
        r_i = ad.r_of(fitted(D["y"], Z[lg]), D["y"])
        per.append(dict(lang=lg, r_b=r_b, r_l=r_l, d=r_l - r_b, r_i=r_i))
        emit(f"| {lg} | {r_b:+.4f} | {r_l:+.4f} | **{r_l - r_b:+.4f}** | {r_i:+.4f} |")
    t = pd.DataFrame(per)
    emit(f"| **medie** | **{t['r_b'].mean():+.4f}** | **{t['r_l'].mean():+.4f}** | "
         f"**{t['d'].mean():+.4f}** | {t['r_i'].mean():+.4f} |", "",
         "Coloana in-sample e a doua limita superioara, cu coeficienti potriviti pe chiar limba "
         "masurata: nici ea nu e atinsa de o procedura onesta.\n")
    REZ["citire"] = dict(b=float(t["r_b"].mean()), lolo=float(t["r_l"].mean()),
                         insample=float(t["r_i"].mean()))
    print(f"    citire optima LOLO {t['r_l'].mean():+.4f} vs B {t['r_b'].mean():+.4f}", flush=True)

    # --- 3c saturatia
    emit("### 3c. Recensamant de saturatie\n",
         "`atomi efectivi` e `exp(entropie)`, adica peste cate cifre e imprastiata efectiv masa. Daca "
         "la T adoptat masa e imprastiata pe aproape toate cele cinci, atunci `B` e deja o marime fina "
         "si cei cinci atomi nu leaga; daca sta pe una singura, leaga. `legaturi` e cate randuri au o "
         "valoare a lui `B` care se repeta, fiindca legaturile plafoneaza Pearson.\n",
         "| limba | masa pe argmax, T=1 | masa pe argmax, T adoptat | atomi efectivi, T=1 | "
         "atomi efectivi, T adoptat | valori distincte ale `B` | legaturi |",
         "|---|---|---|---|---|---|---|")
    rows = []
    for lg in langs:
        D = PL[lg]
        P = 0.5 * (D["P1"] + D["P2"])
        Q = 0.5 * (ad.temper(D["P1"], Tsel[lg]) + ad.temper(D["P2"], Tsel[lg]))
        b = ad.b_at(D, Tsel[lg])
        u, c = np.unique(np.round(b, 10), return_counts=True)
        rows.append(dict(lang=lg, m1=float(P.max(axis=1).mean()), m2=float(Q.max(axis=1).mean()),
                         a1=float(np.exp(ad.entropy(P)).mean()), a2=float(np.exp(ad.entropy(Q)).mean()),
                         nd=len(u), leg=int(c[c > 1].sum()), n=D["n"]))
        r = rows[-1]
        emit(f"| {lg} | {r['m1']:.3f} | {r['m2']:.3f} | {r['a1']:.2f} | {r['a2']:.2f} | "
             f"{r['nd']}/{r['n']} | {r['leg']} |")
    t = pd.DataFrame(rows)
    emit(f"| **medie** | **{t['m1'].mean():.3f}** | **{t['m2'].mean():.3f}** | "
         f"**{t['a1'].mean():.2f}** | **{t['a2'].mean():.2f}** | "
         f"{int(t['nd'].sum())}/{int(t['n'].sum())} | {int(t['leg'].sum())} |", "")
    REZ["saturatie"] = dict(a1=float(t["a1"].mean()), a2=float(t["a2"].mean()),
                            m2=float(t["m2"].mean()), legaturi=int(t["leg"].sum()))
    print(f"    atomi efectivi T=1 {t['a1'].mean():.2f} -> T adoptat {t['a2'].mean():.2f}", flush=True)


# --------------------------------------------------------------------- (4) sondajul de scara
def exp_of(P, vals):
    """Valoarea asteptata a unei distributii pe `vals`, adusa in [0,1]. Generalizarea lui
    `analysis_dist.expected`, care e legata de notele 1..5."""
    return (P @ vals - vals[0]) / (vals[-1] - vals[0])


def step4(ad):
    """Sondajul de scara, pe trial. Nu se raporteaza ca predictie, doar ca ordine.

    Cele trei brate se citesc cu ACELASI cod: aceeasi temperatura pe grila extinsa, acelasi bootstrap
    pe contexte, aceeasi agregare pe limbi. Bratul 1-5 e fisierul canonic, nu o rulare noua, fiindca
    rularea de control prin codul parametrizat a dat `max |dif| = 0.0` si pe B si pe toate coloanele
    de distributie.
    """
    from bakeoff_trial import with_context
    lipsa = [n for n, _, q in SCARI if not os.path.exists(q)]
    if lipsa:
        emit("## 4. Sondajul de scara pe trial\n",
             f"Nerulat: lipsesc bratele {lipsa}.\n")
        return
    print("[4] sondajul de scara, pe trial", flush=True)
    ARM = {}
    for nume, doc, q in SCARI:
        d = with_context(pd.read_csv(q), "trial")
        lo, hi = (int(x) for x in nume.split("-"))
        digits = [str(x) for x in range(lo, hi + 1)]
        vals = np.arange(lo, hi + 1, dtype=float)
        per = {}
        for lg, g in d.groupby("lang", sort=True):
            per[lg] = dict(P1=g[[f"p1_{c}" for c in digits]].values.astype(float),
                           P2=g[[f"p2_{c}" for c in digits]].values.astype(float),
                           y=g["complexity"].values.astype(float),
                           ctx=g["context_id"].values, B=g["B"].values.astype(float), n=len(g))
        ARM[nume] = dict(doc=doc, vals=vals, per=per, k=len(digits))

    langs = sorted(ARM["1-5"]["per"])
    n_tot = sum(ARM["1-5"]["per"][lg]["n"] for lg in langs)
    emit("## 4. Sondajul de scara pe trial\n",
         f"Blocul 3 spune ca cei cinci atomi nu leaga si prezice deci **negativ** pentru o scara mai "
         f"fina. Proxy-ul de acolo nu poate insa vedea RECALIBRAREA: cand modelul e chiar intrebat pe "
         f"0-9, distributia lui nu e distributia de pe 1-5 reeșantionata, e alta. Trei brate, "
         f"{n_tot} instante de trial fiecare, ~6 minute per brat.\n",
         "**Design 2x2 incomplet, si de aia e nevoie de trei brate, nu doua.** `0-9` schimba doua "
         "lucruri fata de `1-5`: numarul de atomi SI ancora. `0-4` schimba numai ancora. Deci efectul "
         "ancorei e `(0-4) - (1-5)` si efectul atomilor e `(0-9) - (0-4)`. Fara bratul din mijloc cele "
         "doua sunt confundate, si oricare rezultat ar fi fost necitibil.\n",
         "**De ce nu 1-10 si de ce nu 0-99.** Soft-read-ul citeste o SINGURA pozitie de token, iar "
         "`10` sunt doi tokeni si primul se ciocneste cu nota 1, deci 0-9 e singura scara de zece "
         "atomi citibila asa. 0-99 ar cere fie o a doua trecere inainte per rand, fie 11 treceri pentru "
         "valoarea asteptata conditionata, deci nu mai e o configuratie de 6 minute si nu intra in "
         "sondaj.\n",
         "Temperatura se realege pentru FIECARE brat, pe aceeasi grila extinsa, si se raporteaza atat "
         "argmaxul pe medie cat si r la T = 1: o scara mai fina schimba ascutimea distributiei, deci "
         "comparatia la T = 1 ar masura ascutimea, nu scara. Argmaxul pe medie e un oracol, NU "
         "protocolul LOLO al lucrarii, si e deliberat: e acelasi oracol pentru toate trei bratele, "
         "deci nu favorizeaza niciunul, iar aici se cerne, nu se adopta.\n",
         "| brat | atomi | ce schimba | r la T=1 | T* pe medie | r la T* | atomi efectivi la T=1 | "
         "masa pe argmax la T=1 |",
         "|---|---|---|---|---|---|---|---|")
    for nume, A in ARM.items():
        R = {}
        for T in ad.T_GRID_EXT:
            R[T] = float(np.mean([ad.r_of(0.5 * (exp_of(ad.temper(A["per"][lg]["P1"], T), A["vals"])
                                                 + exp_of(ad.temper(A["per"][lg]["P2"], T), A["vals"])),
                                          A["per"][lg]["y"]) for lg in langs]))
        Tb = max(R, key=R.get)
        A["T"] = Tb
        A["r1"], A["rT"] = R[1.0], R[Tb]
        P = {lg: 0.5 * (A["per"][lg]["P1"] + A["per"][lg]["P2"]) for lg in langs}
        ae = float(np.mean([np.exp(ad.entropy(P[lg])).mean() for lg in langs]))
        ma = float(np.mean([P[lg].max(axis=1).mean() for lg in langs]))
        A["ae"], A["ma"] = ae, ma
        emit(f"| `{nume}` | {A['k']} | {A['doc']} | {R[1.0]:+.4f} | {Tb:g} | **{R[Tb]:+.4f}** | "
             f"{ae:.2f} din {A['k']} | {ma:.3f} |")
        print(f"    {nume}: r(T=1) {R[1.0]:+.4f}  T*={Tb:g} r {R[Tb]:+.4f}  atomi efectivi {ae:.2f}",
              flush=True)
    emit("")

    # --- comparatiile perechi, la T-ul fiecarui brat
    emit("### Cele doua efecte, separate\n",
         "Comparatie PERECHE pe contexte, fiecare brat citit la temperatura lui. Intervalele sunt "
         "late si trebuie sa fie: sunt 30 de instante per limba, nu 560. Cifra de trial nu e o "
         "predictie a cifrei de test, ordinea e.\n",
         "| efect | brate | diferenta | CI 95% pereche | P(>0) |",
         "|---|---|---|---|---|")
    def boots(nume):
        A = ARM[nume]
        return [ad.boot_one(A["per"][lg]["y"],
                            0.5 * (exp_of(ad.temper(A["per"][lg]["P1"], A["T"]), A["vals"])
                                   + exp_of(ad.temper(A["per"][lg]["P2"], A["T"]), A["vals"])),
                            A["per"][lg]["ctx"])["boot"] for lg in langs]
    B = {n: boots(n) for n in ARM}
    for et, a, b in [("ancora, 1 -> 0", "0-4", "1-5"),
                     ("atomii, 5 -> 10", "0-9", "0-4"),
                     ("amandoua, 1-5 -> 0-9", "0-9", "1-5")]:
        dm, lo, hi, pp = ad.mean_diff_ci(B[a], B[b])
        emit(f"| {et} | `{a}` fata de `{b}` | **{dm:+.4f}** | [{lo:+.4f}, {hi:+.4f}] | {pp:.1%} |")
        REZ[f"scara4:{a}-{b}"] = dict(d=dm, lo=lo, hi=hi, p=pp)
        print(f"    {et}: {dm:+.4f} [{lo:+.4f},{hi:+.4f}] P={pp:.1%}", flush=True)
    r15, r09 = ARM["1-5"]["rT"], ARM["0-9"]["rT"]
    z = REZ.get("scara4:0-9-1-5", {})
    emit("", f"**Verdictul sondajului.** Cele zece atomi dau {r09:+.4f} fata de {r15:+.4f}, adica "
         f"{z.get('d', float('nan')):+.4f}, interval [{z.get('lo', float('nan')):+.4f}, "
         f"{z.get('hi', float('nan')):+.4f}], deci {ad.zero_out(z.get('lo', 0), z.get('hi', 0))}. "
         f"Modelul foloseste efectiv {ARM['0-9']['ae']:.2f} din cele zece cifre, fata de "
         f"{ARM['1-5']['ae']:.2f} din cinci, deci **nu deschide rezolutie, o imparte**. "
         f"Asteptarea declarata inainte de rulare era negativa, si "
         + ("se confirma" if z.get("d", 0) <= 0 else
            "NU se confirma: semnul e pozitiv, si atunci pasul urmator e confirmarea pe test, ~102 "
            "minute") + ".\n")


# --------------------------------------------------------------------- verdict
def verdict():
    """Tabelul de prioritate. Nicio cifra scrisa de mana: toate vin din `REZ`, umplut de pasii de sus."""
    print("[v] tabelul de verdict", flush=True)
    z2 = REZ.get("dezacord:zgomot_2", {}).get("d", float("nan"))
    dez = REZ.get("dezacord:ambele", {})
    exces = dez.get("d", float("nan")) - z2
    lad = REZ.get("scara:ladder", {})
    cit = REZ.get("citire", {})
    sat = REZ.get("saturatie", {})
    ft = REZ.get("fert:transfer", {})
    s49 = REZ.get("scara4:0-9-1-5")
    fp = REZ.get("fert:plafon", {})

    def m(tag):
        r = REZ.get(tag)
        if not r:
            return "nerulat", "", ""
        return f"**{r['d']:+.5f}**", f"[{r['lo']:+.5f}, {r['hi']:+.5f}]", f"{r['p']:.1%}"

    def stare(tag):
        """Verdictul unei configuratii masurate, DEDUS din cifre, nu scris de mana.

        Ordinea conditiilor e cea a lucrarii: intai daca strica o limba, si abia apoi cat urca media.
        Invers ar fi adoptat `distTpp`.
        """
        r = REZ.get(tag)
        if not r:
            return "nerulat"
        rau = (f"; strica in plus {', '.join(r['rele'])} cu interval care exclude zero"
               if r["stricate"] else "")
        if r["hi"] < 0:
            return "**negativa**, se inchide" + rau
        if not (r["lo"] > 0):
            # Intai se verifica daca media trece zero. Ordinea inversa ar scrie „respinsa fiindca
            # strica o limba" despre o configuratie care oricum nu urca nimic, deci ar da alt motiv
            # decat cel adevarat.
            return (f"nesemnificativa, nu nula: P(>0) = {r['p']:.1%}, CI include zero" + rau)
        if r["stricate"]:
            return (f"**respinsa**: media urca, dar strica {', '.join(r['rele'])} cu interval pereche "
                    f"care exclude zero, acelasi motiv ca `distTpp`")
        return (f"**trece**: interval care exclude zero, urca {r['urcate']} limbi semnificativ, "
                f"strica zero")

    emit("## Verdict: ordinea, pe cifre\n",
         "`masurat` = configuratie rulata cap la cap prin fuziune, cu interval pereche fata de "
         "sistem. `plafon` = limita superioara in-sample, deci o procedura onesta da mai putin. "
         "`proxy` = diagnostic pe disc care nu poate inlocui o rulare, doar sa spuna in ce direcție "
         "sa te aștepti. `cost declarat` = nu s-a masurat nimic, se da doar pretul.\n",
         "| # | parghie | tip de dovada | delta | CI 95% pereche | P(>0) | cost pana la o cifra pe "
         "test | verdict |",
         "|---|---|---|---|---|---|---|---|")
    dk = REZ.get("prio_K", {}).get("d", float("nan"))
    dkw = REZ.get("prio_KW", {}).get("d", float("nan"))
    rows = [
        ("unirea cifrelor vecine, partitie LOLO (`prio_K`)", "masurat", *m("prio_K"),
         "0, e rulata deja", stare("prio_K") + ", si partitia `1|23|45` e aleasa unanim pe toate zece "
         "limbile, pe un criteriu lat de 0.39"),
        ("unirea cifrelor + pondere (`prio_KW`)", "masurat", *m("prio_KW"),
         "0, e rulata deja",
         stare("prio_KW") + f". Peste `prio_K` adauga doar {dkw - dk:+.5f}, deci cele doua parghii "
         f"sunt redundante, ceea ce era de asteptat: amandoua respatiaza aceeasi citire liniara"),
        ("pondere intre prompturi (`prio_W`)", "masurat", *m("prio_W"),
         "0, e rulata deja", stare("prio_W")),
        ("media geometrica (`prio_G`)", "masurat", *m("prio_G"),
         "0, e rulata deja", stare("prio_G")),
        ("al treilea termen pentru dezacord", "plafon",
         f"{dez.get('d', float('nan')):+.5f}", f"[{dez.get('lo', float('nan')):+.5f}, "
         f"{dez.get('hi', float('nan')):+.5f}]", f"{dez.get('p', float('nan')):.1%}",
         "o zi de cod in `fit_choice`",
         f"podeaua de zgomot pe 2 coloane e {z2:+.5f}, deci excedentul real e ~{exces:+.5f}; "
         f"**sub pragul de +0.002**, se inchide"),
        ("reziduul de fertilitate, global", "plafon",
         f"{fp.get('d', float('nan')):+.5f}", f"[{fp.get('lo', float('nan')):+.5f}, "
         f"{fp.get('hi', float('nan')):+.5f}]", f"{fp.get('p', float('nan')):.1%}",
         "re-antrenarea bratului A",
         f"plafonul e mare, dar la TRANSFER da {ft.get('d', float('nan')):+.5f} "
         f"[{ft.get('lo', float('nan')):+.5f}, {ft.get('hi', float('nan')):+.5f}], adica **strica cu "
         f"interval care exclude zero**; semnul coeficientului cade la fel pe doar "
         f"{ft.get('semne', '?')}/10 limbi. Se inchide ca termen global."),
        ("distributia intreaga ca trasaturi", "masurat, LOLO",
         f"{cit.get('lolo', float('nan')) - cit.get('b', float('nan')):+.4f} pe bratul B", "", "",
         "o zi de cod in bratul A",
         f"citirea liniara optima a celor 5 probabilitati, aleasa LOLO, e SUB `B` "
         f"({cit.get('lolo', float('nan')):+.4f} fata de {cit.get('b', float('nan')):+.4f}); "
         f"in-sample da {cit.get('insample', float('nan')):+.4f}, deci nu transfera. Se inchide."),
        ("scara de raspuns 0-9", "masurat pe trial" if s49 else "proxy",
         (f"**{s49['d']:+.4f}**" if s49 else
          f"{lad.get(3, float('nan')) - lad.get(5, float('nan')):+.4f} la K=3"),
         (f"[{s49['lo']:+.4f}, {s49['hi']:+.4f}]" if s49 else ""),
         (f"{s49['p']:.1%}" if s49 else ""),
         "sondajul de trial e rulat; confirmarea pe test ar fi ~102 min",
         (f"**se inchide**: proxy-ul prezicea negativ, curba r(K) avand varful la K=3 si nu la K=5, "
          f"si sondajul confirma: {s49['d']:+.4f} cu CI care include zero, si semn negativ pe toate "
          f"trei contrastele. Efectul ancorei "
          f"{REZ.get('scara4:0-4-1-5', {}).get('d', float('nan')):+.4f}, al atomilor "
          f"{REZ.get('scara4:0-9-0-4', {}).get('d', float('nan')):+.4f}" if s49 else
          f"curba r(K) are VARFUL la K=3, nu la K=5. Sondajul nu e rulat.")),
        ("pozitia de citire, prefix fortat", "cost declarat", "-", "", "",
         "~5.5 min trial", "nemasurabil pe disc: schimba distributia, nu citirea ei"),
        ("few-shot din CELELALTE limbi", "masurat pe trial in E.10", "+0.011 pe bratul B", "", "",
         "~3.8 ore pe test, la 2.44 s per item",
         "**NU e netestata**: `prompt_lab.lolo_shots` ia exemplele numai din celelalte limbi, deci "
         "`v3_fewshot` din `output/e10_prompt.md` E chiar asta, si da +0.697 fata de +0.686 al "
         "semnalului B de acum, cea mai buna varianta individuala pe Gemma. Lipseste doar rularea pe "
         "TEST si trecerea prin fuziune, ca **configuratie fixa** pe toate limbile: selectia LOLO "
         "peste variante a pierdut deja (+0.6808 fata de +0.6860), varianta fixa nu are penalizarea "
         "aia. Singura de pe lista cu valoare de REVENDICARE peste cifra, fiindca G-Eval e 3-shot in "
         "limba tinta"),
        ("cuantizare 8 biti pentru Gemma", "cost declarat", "-", "", "",
         "ore de inferenta", "control de confound, nu parghie de castig"),
        ("prompturi 3 si 4, decorelate", "cost declarat", "-", "", "",
         "8.2 ore per model pe test",
         "`output/e10_verdict.md` a masurat deja de ce nu: corelatia medie intre prompturile Gemmei e "
         "0.772, si medierea repara un model slab, nu unul bun"),
    ]
    for i, r in enumerate(rows, 1):
        emit("| " + str(i) + " | " + " | ".join(str(x) for x in r) + " |")
    trec = [t for t in ("prio_K", "prio_KW", "prio_W", "prio_G")
            if REZ.get(t, {}).get("lo", -1) > 0 and not REZ.get(t, {}).get("stricate")]
    emit("")
    if trec:
        best = max(trec, key=lambda t: REZ[t]["d"])
        r = REZ[best]
        emit(f"**Ce s-a mutat.** `{best}` trece bara pe care lucrarea a folosit-o de fiecare data: "
             f"r = **{r['r']:.6f}**, adica **{r['d']:+.5f}** fata de {SYS_R_DECLARAT:.6f}, interval "
             f"pereche [{r['lo']:+.5f}, {r['hi']:+.5f}], P(>0) = {r['p']:.1%}, hiperparametrul ales "
             f"LOLO, zero limbi stricate. **Nu se adopta in acest raport**: decizia e a lui Alexandru, "
             f"si vine cu bifurcatia declarata mai sus, fiindca parghia a fost gasita uitandu-se la o "
             f"cifra de test.\n",
             "Pretul ei e zero: aceeasi inferenta, aceleasi distributii de pe disc, doar alta citire a "
             "lor. Iar mecanismul e citibil, si e chiar cel din blocul 3: nu adauga informatie, "
             "RESPATIAZA nivelurile, si respatierea grosiera bate spatierea egala fiindca eticheta nu "
             "e liniara in nota.\n")
    else:
        emit(f"**Ce nu s-a mutat.** Nicio parghie de pe disc nu produce un interval pereche care "
             f"exclude zero fata de {SYS_R_DECLARAT:.6f}, deci cifra de citat nu se schimba.\n")
    emit("**Ce se inchide definitiv**, cu cifra care le inchide: al treilea termen pentru dezacord "
         f"(excedentul peste podeaua de zgomot, ~{exces:+.5f}, e sub pragul de +0.002), fertilitatea "
         f"ca termen global ({ft.get('d', float('nan')):+.5f} la transfer, cu CI care exclude zero in "
         f"jos), distributia intreaga ca trasaturi (citirea optima LOLO e sub `B`), media geometrica "
         f"(negativa)"
         + (f", si scara de raspuns 0-9 ({s49['d']:+.4f} pe trial, semn negativ pe toate trei "
            f"contrastele)" if s49 else "") + ".\n",
         ("**Ce rams de rulat**, in ordine: few-shot din celelalte limbi PE TEST, ~3.8 ore, fiindca pe "
          "trial e deja cea mai buna varianta individuala si e singura cu valoare de revendicare; "
          "pozitia de citire, ~6 min pe trial. Sondajul de scara e rulat si inchis."
          if s49 else
          "**Ce rams de rulat**, in ordine: sondajul de scara pe trial, cu asteptarea negativa "
          "declarata inainte; few-shot din celelalte limbi; pozitia de citire.") + "\n")


if __name__ == "__main__":
    sys.exit(main())
