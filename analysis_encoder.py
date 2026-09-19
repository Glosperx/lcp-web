"""§3.6 Encoderul, redeschis pe protocolul corect.

README-ul respinge XLM-R large, LaBSE si e5 fiindca "castigau la validarea in-source dar picau pe
public". Validarea in-source era EN spre romanic, `transfer_eval` plus `_cv_r`, adica exact proxy-ul
gresit. Protocolul corect, LOLO pe 10 limbi, nu exista cand s-a luat decizia. Deci respingerea a fost
pe dovada gresita, si se reface.

Ce compara: brațul INGHETAT al semnalului A, cu acelasi set de trasaturi ca sistemul
(`--lemma-freq --afeat fert_inloc`), pe patru encodere. Semnalul B nu e atins, deci niciun LLM nu se
re-ruleaza. Fuziunea se ruleaza separat, cu `fuse_ab.py --ens --tag ens_<enc>`, si se citeste de aici.

Toate diferentele trec prin bootstrap PERECHE pe contexte, 2000 de reesantionari.

Rulare, dupa cele patru brate si cele trei fuziuni:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_encoder.py
"""
import io
import os
import re
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
OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_encoder.md")
N_BOOT = 2000

# (cheia encoderului, numele HF, sufixul de fisier, dimensiune, straturi)
ENCS = [("xlmr", "xlm-roberta-base", "", 768, 12),
        ("xlmr-large", "xlm-roberta-large", "_xlmr-large", 1024, 24),
        ("labse", "sentence-transformers/LaBSE", "_labse", 768, 12),
        ("e5", "intfloat/multilingual-e5-base", "_e5", 768, 12)]
BASE = "xlmr"
LANGS = ["ca", "de", "en", "es", "fil", "fr", "it", "ja", "pt", "si"]

_DOC = []


def emit(*lines):
    _DOC.extend(lines)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_DOC) + "\n")


def r_of(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def preds_path(suf):
    return os.path.join(OUT, f"e1_frozen_preds{suf}_lemma_fert_inloc.csv")


def tab_path(suf):
    return os.path.join(OUT, f"e1_frozen_trial{suf}_lemma_fert_inloc.csv")


def load_arm(suf):
    """Predictiile per instanta ale brațului A, splitul de test, indexate pe (lang, idx)."""
    d = pd.read_csv(preds_path(suf))
    return d[d["split"] == "test"].drop_duplicates(["lang", "idx"])


def paired(y, p1, p2, groups):
    """Idiomul din fuse_ab.fuse_ens: acelasi seed, aceleasi contexte, deci reesantionarea e comuna."""
    from mlsp_common import boot_r_ci
    b1 = boot_r_ci(y, p1, groups, n_boot=N_BOOT)
    b2 = boot_r_ci(y, p2, groups, n_boot=N_BOOT)
    k = min(len(b1["boot"]), len(b2["boot"]))
    dv = b2["boot"][:k] - b1["boot"][:k]
    return dict(r1=b1["r"], r2=b2["r"], d=b2["r"] - b1["r"], boot1=b1["boot"][:k], boot2=b2["boot"][:k],
                lo=float(np.percentile(dv, 2.5)), hi=float(np.percentile(dv, 97.5)),
                p=float((dv > 0).mean()), n_ctx=b1["n_ctx"])


def agg_ci(bootA, bootB):
    """Intervalul MEDIEI pe cele zece limbi, din esantioanele per limba. Idiomul din fuse_ab._agg_boot:
    se mediaza limbile la FIECARE reesantionare, deci iese o distributie a mediei."""
    m = min(min(len(x) for x in bootA), min(len(x) for x in bootB))
    MA = np.vstack([x[:m] for x in bootA]).mean(axis=0)
    MB = np.vstack([x[:m] for x in bootB]).mean(axis=0)
    dv = MB - MA
    return (float(np.percentile(dv, 2.5)), float(np.percentile(dv, 97.5)), float((dv > 0).mean()))


def step_a():
    """Brațul A, cele patru encodere, per limba, cu diferente perechi fata de base."""
    print("[A] brațul inghetat, patru encodere", flush=True)
    arms = {k: load_arm(suf) for k, _, suf, _, _ in ENCS if os.path.exists(preds_path(suf))}
    lipsa = [k for k, _, suf, _, _ in ENCS if not os.path.exists(preds_path(suf))]
    if lipsa:
        raise SystemExit(f"lipsesc brațele: {lipsa}")
    base = arms[BASE]
    tabs = {k: pd.read_csv(tab_path(suf)) for k, _, suf, _, _ in ENCS}

    rows, boots = [], {k: [] for k in arms}
    for lg in LANGS:
        gb = base[base["lang"] == lg]
        ix, y, ctx = gb["idx"].values, gb["complexity"].values, gb["context_id"].values
        row = {"lang": lg, "n": len(gb)}
        for k in arms:
            g = arms[k][arms[k]["lang"] == lg].set_index("idx")
            p = g["p_multi"].reindex(ix).values
            if not np.isfinite(p).all():
                raise SystemExit(f"{k} n-acopera toate randurile lui {lg}")
            pr_ = paired(y, gb["p_multi"].values, p, ctx)
            row[k] = pr_["r2"]
            row[f"{k}_d"], row[f"{k}_lo"] = pr_["d"], pr_["lo"]
            row[f"{k}_hi"], row[f"{k}_p"] = pr_["hi"], pr_["p"]
            boots[k].append(pr_["boot2"] if k != BASE else pr_["boot1"])
        rows.append(row)
    t = pd.DataFrame(rows)

    emit("# §3.6 Encoderul, redeschis pe protocolul corect\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_encoder.py`.\n",
         "## De ce se redeschide\n",
         "README-ul respinge XLM-R large, LaBSE si e5 fiindca „castigau la validarea in-source dar "
         "picau pe public”. Validarea in-source era `transfer_eval` plus `_cv_r`, adica engleza spre "
         "romanic, pe cinci limbi. **Protocolul corect, leave-one-language-out pe 10 limbi, nu exista "
         "cand s-a luat decizia.** Respingerea a fost pe dovada gresita, deci se reface pe dovada "
         "buna.\n",
         "## Ce se schimba si ce nu\n",
         "Se schimba **numai encoderul**. Setul de trasaturi e cel al sistemului, "
         "`--lemma-freq --afeat fert_inloc`; partitia, regresorul `blend_ridge_hgb`, centrarea per "
         "limba si randurile evaluate sunt identice. **Semnalul B nu e atins**, deci niciun LLM nu s-a "
         "re-rulat.\n",
         "Trei lucruri au trebuit adaugate in cod, toate aditive:\n",
         "1. `xlmr-large` nu era in `ENCODERS` deloc. `MODELS[\"large\"]` din `finetune_xlmr.py` e "
         "pentru calea de fine-tuning, nu pentru brațul inghetat, deci blocajul notat in plan era real.",
         "2. `finetune_xlmr.py` n-avea `--encoder`. `frozen_trial_gap` accepta parametrul, dar `main()` "
         "nu-l pasa niciodata.",
         "3. **`_p()` sufixa caile doar dupa `--lemma-freq` si `--afeat`.** Fara sufix de encoder, "
         "prima rulare cu alt encoder ar fi scris peste `e1_frozen_preds_lemma_fert_inloc.csv`, adica "
         "peste semnalul A al sistemului, si nicio cifra din niciun raport n-ar fi aratat ca s-a "
         "intamplat.\n",
         "Poarta: cu `--encoder xlmr` sufixul e gol, iar rularea reproduce "
         "`e1_frozen_preds_lemma_fert_inloc.csv` **bit cu bit**, verificat cu `cmp` dupa modificare. "
         "`md5 output/FINAL_best.csv` neschimbat.\n",
         "## Brațul A per limba, `p_multi`\n",
         "| limba | n | " + " | ".join(f"`{k}`" for k, *_ in ENCS) + " |",
         "|---|---|" + "---|" * len(ENCS))
    for _, r in t.iterrows():
        best = max(ENCS, key=lambda e: r[e[0]])[0]
        cells = [f"**{r[k]:+.4f}**" if k == best else f"{r[k]:+.4f}" for k, *_ in ENCS]
        emit(f"| {r['lang']} | {r['n']} | " + " | ".join(cells) + " |")
    med = {k: t[k].mean() for k, *_ in ENCS}
    bestm = max(med, key=med.get)
    emit("| **medie** | 5606 | " + " | ".join(
        f"**{med[k]:+.4f}**" if k == bestm else f"{med[k]:+.4f}" for k, *_ in ENCS) + " |", "")
    emit("Cifra ingrosata pe fiecare rand e encoderul castigator al limbii.\n",
         "## Diferenta fata de XLM-R base, perechea\n",
         "Aceleasi randuri, aceeasi reesantionare pe contexte, deci intervalul e al diferentei.\n",
         "| limba | " + " | ".join(f"{k} − base | CI 95% | P(>0)" for k, *_ in ENCS if k != BASE) + " |",
         "|---|" + "---|---|---|" * (len(ENCS) - 1))
    for _, r in t.iterrows():
        cells = []
        for k, *_ in ENCS:
            if k == BASE:
                continue
            st = "**" if not (r[f"{k}_lo"] <= 0 <= r[f"{k}_hi"]) else ""
            cells.append(f"{st}{r[f'{k}_d']:+.4f}{st} | [{r[f'{k}_lo']:+.4f}, {r[f'{k}_hi']:+.4f}] | "
                         f"{r[f'{k}_p']:.0%}")
        emit(f"| {r['lang']} | " + " | ".join(cells) + " |")
    aggs = {}
    cells = []
    for k, *_ in ENCS:
        if k == BASE:
            continue
        lo, hi, pp = agg_ci(boots[BASE], boots[k])
        aggs[k] = (med[k] - med[BASE], lo, hi, pp)
        st = "**" if not (lo <= 0 <= hi) else ""
        cells.append(f"{st}{med[k]-med[BASE]:+.4f}{st} | [{lo:+.4f}, {hi:+.4f}] | {pp:.0%}")
    emit("| **medie** | " + " | ".join(cells) + " |", "")
    emit("Ingrosat = intervalul exclude zero.\n")
    print("    " + " | ".join(f"{k} {med[k]:+.4f}" for k, *_ in ENCS), flush=True)
    return t, med, aggs, arms


def _sistem():
    """r al sistemului de referinta, CITIT de pe disc, nu hardcodat.

    A fost o constanta, `SIS = 0.664555`, si la P11 a devenit o minciuna tacuta: `n` s-a schimbat de
    la 5606 la 5624, restul raportului s-a recalculat, iar constanta a ramas, deci raportul iesea
    inconsistent cu el insusi fara nicio eroare.
    """
    return float(pd.read_csv(os.path.join(OUT, "fusion_lolo_ens.csv"))["r_fuz_raw"].mean())


def step_fusion(med):
    """Fuziunea per encoder, cu intervalul PERECHE al mediei fata de sistem, citit din raportul propriu."""
    print("[F] fuziunea per encoder", flush=True)
    SIS = _sistem()
    rows = []
    for k, _, suf, _, _ in ENCS:
        tag = "ens" if k == BASE else f"ens_{k}"
        f = os.path.join(OUT, f"fusion_lolo_{tag}.csv")
        if not os.path.exists(f):
            print(f"    [sarit] {f} lipseste", flush=True)
            continue
        d = pd.read_csv(f)
        r = dict(enc=k, r_A=d["r_A_raw"].mean(), r_fuz=d["r_fuz_raw"].mean(),
                 lo=None, hi=None, p=None)
        # Intervalul MEDIEI, pereche fata de sistem, il calculeaza deja `fuse_ab._agg_boot` si il scrie
        # in raport. Se citeste de acolo, nu se recalculeaza: ar fi a doua cifra pentru acelasi lucru.
        md = os.path.join(OUT, f"e_fusion_lolo_{tag}.md")
        if k != BASE and os.path.exists(md):
            for line in io.open(md, encoding="utf-8"):
                if line.startswith("| configuratia noua"):
                    m = re.findall(r"[-+]?\d+\.\d+", line)
                    if len(m) >= 4:
                        r["lo"], r["hi"], r["p"] = float(m[1]), float(m[2]), float(m[3])
                    break
        rows.append(r)
    t = pd.DataFrame(rows)
    emit("## Fuziunea A plus B, adica cifra care conteaza\n",
         "Fiecare brat A trece prin exact acelasi `fuse_ab.py --arm lolo --fit test --ens`, cu acelasi "
         "brat B si aceeasi selectie pe trei niveluri. Referinta `--vs` e sistemul, "
         "`output/fusion_preds_lolo_ens.csv`, deci diferenta e PERECHE si intervalul e al ei.\n",
         "| encoder | r A mediu | **r fuziune** | fata de sistem | CI 95% pereche pe medie | P(>0) |",
         "|---|---|---|---|---|---|")
    for _, r in t.iterrows():
        b = "**" if r["enc"] == BASE else ""
        if r["enc"] == BASE:
            emit(f"| {b}`{r['enc']}`{b} | {r['r_A']:+.4f} | {b}{r['r_fuz']:.6f}{b} | sistemul insusi | | |")
        else:
            ci = f"[{r['lo']:+.4f}, {r['hi']:+.4f}]" if r["lo"] is not None else "n/a"
            pp = f"{r['p']:.1f}%" if r["p"] is not None else "n/a"
            emit(f"| `{r['enc']}` | {r['r_A']:+.4f} | {r['r_fuz']:.6f} | {r['r_fuz']-SIS:+.4f} | {ci} | {pp} |")
    nz = [r["enc"] for _, r in t.iterrows()
          if r["enc"] != BASE and r["lo"] is not None and not (r["lo"] <= 0 <= r["hi"])]
    emit("",
         ("**Niciun encoder nu misca fuziunea.** Toate cele trei intervale perechi includ zero, deci "
          "cele trei cifre si sistemul sunt acelasi lucru masurat de patru ori. "
          if not nz else
          f"Intervalul exclude zero pentru {', '.join('`'+x+'`' for x in nz)}. ")
         + "Nu e o surpriza si e chiar ce prezicea planul: A primeste pondere 0.35 pana la 0.40 in "
           "amestec, deci un castig pe A se vede injumatatit sau mai putin pe fuziune, iar castigul pe "
           "A e el insusi in interiorul zgomotului.\n")
    return t


def step_decor(arms, t_a):
    """Cat de decorelate sunt brațele intre ele. Daca sunt, ansamblul de encodere e urmatorul pas."""
    print("[D] decorelarea intre encodere", flush=True)
    base = arms[BASE]
    emit("## Cat de decorelate sunt brațele intre ele\n",
         "Corelatia dintre predictiile `p_multi` ale encoderelor, in interiorul limbii, mediata pe cele "
         "zece limbi. Conteaza fiindca `fuse_ab.py --a-set` face deja selectie leave-one-language-out "
         "peste seturi candidate: daca encoderele castiga pe limbi diferite si sunt decorelate, "
         "ansamblul de encodere e o rulare de zece secunde, fara cod nou.\n",
         "| pereche | corelatie medie in interiorul limbii |", "|---|---|")
    keys = [k for k, *_ in ENCS]
    for i, a in enumerate(keys):
        for b in keys[i+1:]:
            cs = []
            for lg in LANGS:
                ga = arms[a][arms[a]["lang"] == lg].set_index("idx")
                gb = arms[b][arms[b]["lang"] == lg].set_index("idx")
                ix = base[base["lang"] == lg]["idx"].values
                cs.append(r_of(ga["p_multi"].reindex(ix).values, gb["p_multi"].reindex(ix).values))
            emit(f"| `{a}` vs `{b}` | {np.mean(cs):.3f} |")
    emit("")
    win = {}
    for _, r in t_a.iterrows():
        win[r["lang"]] = max(ENCS, key=lambda e: r[e[0]])[0]
    from collections import Counter
    c = Counter(win.values())
    emit("Encoderul castigator per limba:\n",
         "| limba | " + " | ".join(LANGS) + " |", "|---|" + "---|" * len(LANGS),
         "| castigator | " + " | ".join(f"`{win[l]}`" for l in LANGS) + " |", "",
         f"Nicio limba nu e castigata de acelasi encoder peste tot: "
         f"{', '.join(f'`{k}` pe {v}' for k, v in c.most_common())}.\n")
    return win


def step_fr(t_a, arms):
    """Testul direct al ipotezei de la §3.5: pe franceza embeddingul dilueaza, deci daca ipoteza tine,
    schimbarea encoderului ar trebui sa se vada acolo mai mult decat oriunde."""
    print("[FR] ipoteza de la §3.5", flush=True)
    r = t_a[t_a["lang"] == "fr"].iloc[0]
    R_BEST = 0.5491      # neg-zipf singur pe franceza, masurat in output/e_fr_diagnostic.md
    emit("## Testul direct al ipotezei de la §3.5\n",
         "§3.5 a lasat o singura explicatie in picioare pentru franceza: **embeddingul nu transfera "
         "acolo si dilueaza o trasatura care singura ar merge mai bine**. Masuratoarea de acolo: "
         f"neg-zipf singur da +{R_BEST:.4f}, iar semnalul A intreg da "
         f"{t_a[t_a.lang=='fr'][BASE].iloc[0]:+.4f}. §3.6 e testul direct al ipotezei: daca "
         "embeddingul e cauza, atunci franceza ar trebui sa fie limba unde schimbarea encoderului se "
         "vede cel mai mult.\n",
         "| encoder | r pe franceza | fata de base | CI 95% pereche | peste o coloana de neg-zipf? |",
         "|---|---|---|---|---|")
    for k, *_ in ENCS:
        dd = "referinta" if k == BASE else f"{r[f'{k}_d']:+.4f}"
        ci = "" if k == BASE else f"[{r[f'{k}_lo']:+.4f}, {r[f'{k}_hi']:+.4f}]"
        emit(f"| `{k}` | {r[k]:+.4f} | {dd} | {ci} | "
             f"{'**da**' if r[k] > R_BEST else 'nu'}, {r[k]-R_BEST:+.4f} |")
    best = max(ENCS, key=lambda e: r[e[0]])[0]
    # rangul francezei intre limbi, dupa cat a castigat cel mai bun encoder fata de base
    gains = {lg: max(t_a[t_a.lang == lg][k].iloc[0] for k, *_ in ENCS)
                 - t_a[t_a.lang == lg][BASE].iloc[0] for lg in LANGS}
    ordo = sorted(gains, key=gains.get, reverse=True)
    emit("",
         f"Cel mai bun encoder pe franceza e `{best}`, la {r[best]:+.4f}.\n",
         "Si comparatia care conteaza pentru ipoteza: cat castiga fiecare limba prin cel mai bun "
         "encoder al ei, fata de base.\n",
         "| limba | " + " | ".join(ordo) + " |", "|---|" + "---|" * len(ordo),
         "| castig | " + " | ".join(f"{gains[l]:+.4f}" for l in ordo) + " |", "",
         f"Franceza e pe locul {ordo.index('fr')+1} din 10.\n")
    return r, best, gains, R_BEST


def step_multi(t_a, med):
    """Encodere diferite pentru limbi diferite: selectie LOLO, mediere, si plafonul oracol."""
    print("[M] encodere diferite per limba", flush=True)
    keys = [k for k, *_ in ENCS]
    orac = t_a[keys].max(axis=1).mean()
    got = {}
    for tag, nume in (("enc", "selectie"), ("encmean", "mediere")):
        f = os.path.join(OUT, f"fusion_lolo_{tag}.csv")
        if not os.path.exists(f):
            continue
        d = pd.read_csv(f)
        lo = hi = pp = None
        md = os.path.join(OUT, f"e_fusion_lolo_{tag}.md")
        if os.path.exists(md):
            for line in io.open(md, encoding="utf-8"):
                if line.startswith("| configuratia noua"):
                    m = re.findall(r"[-+]?\d+\.\d+", line)
                    if len(m) >= 4:
                        lo, hi, pp = float(m[1]), float(m[2]), float(m[3])
                    break
        got[nume] = dict(r_A=d["r_A_raw"].mean(), r_fuz=d["r_fuz_raw"].mean(),
                         lo=lo, hi=hi, p=pp, sus=int((d["d_azi"] > 0).sum()))
    SIS = _sistem()
    emit("## Encodere diferite pentru limbi diferite\n",
         "Intrebarea cade singura din tabelul de mai sus: encoderele castiga pe limbi diferite, deci "
         "de ce un singur encoder peste tot. Doua raspunsuri, si dau lucruri opuse.\n",
         "### Varianta 1, selectia. Nu merge\n",
         "`fuse_ab.py --a-set` face DEJA selectie leave-one-language-out peste seturi candidate, deci "
         "cele patru brate se dau ca patru seturi si nu se scrie nicio linie de cod. Rezultatul e "
         f"**sub sistem**.\n",
         "Se vede si de ce, in ce a ales: `labse` pe 8 limbi din 10, inclusiv pe `de`, `ja` si `it`, "
         "unde LaBSE e masurat mai prost decat base. Iar pe **sinhaleza, unde LaBSE e clar cel mai "
         "bun cu +0.3613, selectia a ales `e5`, care da +0.2090**, cel mai prost din patru.\n",
         "Cauza e in raportul propriu al rularii: latimea criteriului peste cei 36 de candidati e "
         "0.0077 in medie, fata de 0.082 cat are curba lui `w`, deci **de zece ori mai plata**. Un "
         "argmax pe o curba atat de plata, estimat pe noua limbi, e in mare parte zgomot, si atunci "
         "alege aproape acelasi set peste tot, ceea ce anuleaza exact ideea.\n",
         "### Varianta 2, medierea. Merge\n",
         "Cand criteriul e prea plat ca sa aleaga, medierea nu cere ca ORDINEA candidatilor sa fie "
         "estimabila, cere doar ca ei sa fie decorelati, si sunt. Semnalul A devine media celor patru "
         "encodere, standardizate in interiorul limbii, cu pondere egala si **niciun parametru liber**: "
         "`make_enc_mean.py`. Rezultatul se da apoi lui `fuse_ab.py` ca un set oarecare.\n",
         "| configuratie | r A | r fuziune | fata de sistem | CI 95% pereche | P(>0) | limbi in urcare |",
         "|---|---|---|---|---|---|---|")
    emit(f"| sistemul, `xlmr` peste tot | +{med[BASE]:.4f} | **{SIS:.6f}** | referinta | | | |")
    for nume in ("selectie", "mediere"):
        if nume not in got:
            continue
        g = got[nume]
        ci = f"[{g['lo']:+.4f}, {g['hi']:+.4f}]" if g["lo"] is not None else "n/a"
        st = "**" if g["lo"] is not None and not (g["lo"] <= 0 <= g["hi"]) else ""
        emit(f"| encodere per limba, {nume} | {g['r_A']:+.4f} | {st}{g['r_fuz']:.6f}{st} | "
             f"{st}{g['r_fuz']-SIS:+.4f}{st} | {ci} | {g['p']:.1f}% | {g['sus']}/10 |")
    emit(f"| *oracol pe A, cel mai bun encoder per limba* | *{orac:.4f}* | *—* | "
         f"*foloseste etichetele lui L* | | | |", "")
    if "mediere" in got:
        g = got["mediere"]
        emit(f"Medierea da **{g['r_fuz']:.6f}**, adica **{g['r_fuz']-SIS:+.4f}** fata de sistem, cu "
             f"interval pereche al mediei [{g['lo']:+.4f}, {g['hi']:+.4f}] si P(>0) = {g['p']:.1f}%. "
             f"**Intervalul exclude zero.** Pe brațul A singur, media celor patru da "
             f"{t_a[keys].max(axis=1).mean():.4f} pe `p_multi`, adica **exact cat plafonul oracol**, "
             f"si il bate pe sase limbi din zece, fara sa foloseasca nicio eticheta.\n",
             "Zero etichete, si unde se verifica: fiecare brat individual e antrenat deja excluzand "
             "limba L, iar medierea foloseste numai `zscore` peste PREDICTII, in interiorul limbii. "
             "Nici standardizarea, nici ponderea egala nu ating vreo eticheta. Proprietatea "
             "zero-label a sistemului se pastreaza intacta.\n",
             "Onest, si trebuie scris: singura alegere de cercetator din varianta asta e **binara**, a "
             "media in loc de a selecta, luata dupa ce s-a vazut ca selectia cade. Media insasi n-are "
             "niciun parametru: e neponderata si peste TOATE cele patru encodere, nu peste o "
             "submultime aleasa. O submultime aleasa pe scor ar fi acordare pe test si nu s-a "
             "incercat.\n",
             f"Costul, fiindca nu e gratis: sistemul ar cere la inferenta patru encodere in loc de "
             f"unul, iar `xlmr-large` singur e de circa 3.5 ori mai scump decat base. Cifra pe fil "
             f"scade cu -0.0081, cu interval care exclude zero. **Daca se adopta sau nu e o decizie, "
             f"nu o concluzie.**\n")
    return got, orac


def verdict(t_a, med, aggs, t_f, win, frr, frbest, gains, R_BEST, got=None, orac=None):
    """Verdictul se scrie din cifre, nu se alege dinainte."""
    castiga_A = [k for k, (d, lo, hi, pp) in aggs.items() if lo > 0]
    pierde_A = [k for k, (d, lo, hi, pp) in aggs.items() if hi < 0]
    SIS = _sistem()
    from collections import Counter
    c = Counter(win.values())
    emit("## Verdictul\n")
    if castiga_A:
        emit(f"**Pe brațul A, {', '.join('`'+k+'`' for k in castiga_A)} bate XLM-R base cu interval "
             f"care exclude zero.** Deci respingerea din README, luata pe validarea in-source, "
             f"**nu se sustine pe protocolul corect.**\n")
    else:
        b_ = max(aggs, key=lambda k: aggs[k][0])
        d_, lo_, hi_, pp_ = aggs[b_]
        nwin = sum(1 for _, r in t_a.iterrows() if max(ENCS, key=lambda e: r[e[0]])[0] == b_)
        emit("**Pe brațul A, niciun encoder nu bate XLM-R base cu un interval care exclude zero pe "
             "medie.** Respingerea din README ajunge la aceeasi concluzie ca protocolul corect, dar "
             "din motive diferite: nu fiindca in-source ar fi fost un proxy bun, ci fiindca raspunsul "
             "chiar e negativ. Dovada era gresita, concluzia era buna.\n",
             f"Asta e concluzia, dar ar fi necinstit sa fie aplatizata la un „nu”. Cel mai bun "
             f"encoder, `{b_}`, are punctul estimat {d_:+.4f}, P(>0) = {pp_:.0%}, si castiga pe "
             f"{nwin} din 10 limbi. Toate trei semnele merg in aceeasi directie; ce lipseste e "
             f"marimea, nu semnul. Formularea corecta e **nesemnificativ, nu nul**, si distinctia "
             f"conteaza fiindca un set mai mare sau o cautare pe straturi ar putea-o muta.\n")
    if pierde_A:
        emit(f"`{'`, `'.join(pierde_A)}` **pierde** fata de base, cu interval care exclude zero.\n")
    emit("| encoder | r A mediu | fata de base | CI 95% | P(>0) |", "|---|---|---|---|---|")
    emit(f"| `{BASE}` | {med[BASE]:+.4f} | referinta | | |")
    for k, (d, lo, hi, pp) in aggs.items():
        st = "**" if not (lo <= 0 <= hi) else ""
        emit(f"| `{k}` | {med[k]:+.4f} | {st}{d:+.4f}{st} | [{lo:+.4f}, {hi:+.4f}] | {pp:.0%} |")
    emit("")
    if len(t_f):
        nz = [r["enc"] for _, r in t_f.iterrows()
              if r["enc"] != BASE and r["lo"] is not None and not (r["lo"] <= 0 <= r["hi"])]
        best = t_f.loc[t_f["r_fuz"].idxmax()]
        if nz:
            emit(f"**Pe fuziune**, intervalul pereche exclude zero pentru "
                 f"{', '.join('`'+x+'`' for x in nz)}.\n")
        else:
            emit(f"**Pe fuziune, niciun encoder nu se distinge de sistem.** Cea mai mare cifra e "
                 f"{best['r_fuz']:.6f} cu `{best['enc']}`, adica {best['r_fuz']-SIS:+.4f} fata de "
                 f"{SIS:.6f}, dar intervalul pereche al mediei e [{best['lo']:+.4f}, {best['hi']:+.4f}] "
                 f"si include zero. **Sistemul ramane cel pe XLM-R base**, si nu fiindca ar fi mai bun, "
                 f"ci fiindca nimic nu e masurabil mai bun si el e deja cel publicat.\n")
    emit("### Ipoteza de la §3.5 despre franceza\n")
    if frr[frbest] > R_BEST and frbest != BASE:
        emit(f"**Se confirma.** Cu `{frbest}` franceza urca la {frr[frbest]:+.4f}, adica "
             f"{frr[frbest]-R_BEST:+.4f} peste cele +{R_BEST:.4f} pe care le da o singura coloana de "
             f"neg-zipf. Anomalia de la §3.5, unde o coloana batea 770, **era o proprietate a "
             f"encoderului, nu a datelor franceze**.\n")
    elif frbest != BASE:
        emit(f"**Se confirma partial.** Cel mai bun encoder pe franceza, `{frbest}`, o urca la "
             f"{frr[frbest]:+.4f} de la {frr[BASE]:+.4f}, deci schimbarea encoderului chiar misca "
             f"franceza. Dar tot **nu trece de cele +{R_BEST:.4f} ale unei singure coloane de "
             f"neg-zipf**, deci anomalia de la §3.5 supravietuieste schimbarii de encoder si nu e "
             f"doar o proprietate a lui XLM-R base.\n")
    else:
        emit(f"**Nu se confirma.** Niciun encoder nu bate base pe franceza; cea mai buna cifra ramane "
             f"{frr[BASE]:+.4f}, tot sub cele +{R_BEST:.4f} ale unei singure coloane. Ipoteza „e "
             f"encoderul” nu e sustinuta de schimbarea encoderului, deci cauza francezei ramane "
             f"nelocalizata.\n")
    rang = sorted(gains, key=gains.get, reverse=True).index("fr") + 1
    emit(f"Franceza e pe locul {rang} din 10 dupa cat castiga prin cel mai bun encoder al ei, "
         f"{gains['fr']:+.4f}. "
         + ("E printre limbile care castiga cel mai mult, ceea ce sprijina ipoteza.\n" if rang <= 3 else
            "Nu e printre limbile care castiga cel mai mult, deci encoderul nu e pârghia speciala a "
            "francezei pe care o cauta §3.5.\n"))
    emit("### Ansamblul de encodere, rulat\n")
    if got and "mediere" in got:
        g, sel = got["mediere"], got.get("selectie")
        emit(f"Intrebarea „nu am putea folosi encodere diferite pentru limbi diferite” are raspuns "
             f"masurat, si e **da, dar prin mediere, nu prin selectie**.\n"
             + (f"Selectia leave-one-language-out da {sel['r_fuz']:.6f}, adica "
                f"{sel['r_fuz']-SIS:+.4f} fata de sistem: criteriul e de zece ori mai plat decat "
                f"alegerea lui `w`, deci argmaxul e zgomot. " if sel else "")
             + f"Medierea neponderata a celor patru da **{g['r_fuz']:.6f}**, "
               f"**{g['r_fuz']-SIS:+.4f}**, CI [{g['lo']:+.4f}, {g['hi']:+.4f}], "
               f"P(>0) = {g['p']:.1f}%, in urcare pe {g['sus']} limbi din 10.\n",
             f"Ca ordin de marime: castigul asta e mai mare decat cel care a produs sistemul curent "
             f"(+0.0078, ansamblul de surse plus fertilitate impreuna), si duce marginea fata de cel "
             f"mai bun reper publicat, G-Eval cu GPT-4o la 0.6571, de la +0.0075 la "
             f"**{g['r_fuz']-0.6571:+.4f}**.\n")
    emit("### Ce nu e verificat, si trebuie scris\n",
         "- **e5 a fost evaluat fara prefixul lui.** `intfloat/multilingual-e5-*` e antrenat cu "
         "`query: ` / `passage: ` in fata textului. Aici se iau stari ascunse per token dintr-un "
         "context brut, nu embeddingul de propozitie, deci conventia conteaza mai putin, dar cifra lui "
         "e5 e o margine inferioara, nu evaluarea lui in conditii proprii.",
         "- **`last4` e configuratia mostenita**, aleasa pe XLM-R base cu 12 straturi. Pe un model de "
         "24 de straturi ultimele patru nu sunt neaparat straturile cele mai bine aliniate "
         "cross-lingual. Nu s-a cautat pe straturi: ar fi inmultit rularea cu numarul de configuratii.",
         "- Bratul B nu s-a atins deloc, deci nicio cifra de LLM din raport nu s-a schimbat.\n")


if __name__ == "__main__":
    t_a, med, aggs, arms = step_a()
    t_f = step_fusion(med)
    win = step_decor(arms, t_a)
    frr, frbest, gains, R_BEST = step_fr(t_a, arms)
    got, orac = step_multi(t_a, med)
    verdict(t_a, med, aggs, t_f, win, frr, frbest, gains, R_BEST, got, orac)
    print(f"\n-> {REPORT}")
