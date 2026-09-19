"""P9. Cele doua parghii neadoptate, combinate, si dosarul pe care se ia decizia de adoptare.

Nu ruleaza nicio inferenta si nu recalculeaza nicio fuziune: citeste cele PATRU configuratii deja
scrise de `fuse_ab.py` si le pune una langa alta.

  sistem     `--arm lolo --fit test --ens --tag ens`                              0.664581
  encmean    acelasi, cu bratul A pe media a TREI encodere, fara `xlmr-large`     0.669223
  picktest   acelasi, cu `--pick-split test`                                      0.669735
  combinatia amandoua deodata                                                     masurata aici

Intrebarea care decide nu e cat iese combinatia, ci daca selectia pe test mai adauga ceva PESTE media
de encodere. Daca intervalul acelei comparatii include zero, cele doua parghii sunt redundante si se
adopta una singura, cea mai ieftina la inferenta.

Toate diferentele sunt PERECHE. Distributia bootstrap se calculeaza o singura data per configuratie
per limba, cu acelasi seed si acelasi vector de contexte prin `mlsp_common.boot_r_ci`, iar perechile
se formeaza scazand distributiile. Asa reesantionarea k e aceeasi in toate cele patru comparatii si
ele sunt consistente intre ele, nu doar fiecare in parte.

Nu se adopta nimic aici. Fisierul scrie un raport si atat.

Rulare, ~20 de secunde:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_adoptie.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, "output")
REPORT = os.path.join(OUT, "e_adoptie.md")
TABLE = os.path.join(OUT, "adoptie.csv")
COST = os.path.join(OUT, "cost_inferenta.csv")
JURNAL = os.path.join(OUT, "e_rezumat_modele.csv")
BAKEOFF = os.path.join(OUT, "bakeoff_test")
N_BOOT = 2000

# cheie -> (eticheta, tabel, predictii). Ordinea e cea din raport.
# Dupa P11 pătratul e curat: o singura schimbare pe fiecare axa, deci descompunerea e interpretabila.
# `encmean` e media a TREI encodere, fara `xlmr-large`, fiindca aia e varianta adoptata: M3 a aratat
# ca al patrulea nu se distinge de zero in prezenta lui `--pick-split test`.
CFG = [
    ("sistem", "sistemul de dinainte", "fusion_lolo_ens.csv", "fusion_preds_lolo_ens.csv"),
    ("encmean", "media a trei encodere", "fusion_lolo_encmean3.csv",
     "fusion_preds_lolo_encmean3.csv"),
    ("picktest", "selectia lui B pe test", "fusion_lolo_picktest.csv",
     "fusion_preds_lolo_picktest.csv"),
    ("comb", "sistemul ADOPTAT, amandoua", "fusion_lolo_adoptat.csv",
     "fusion_preds_lolo_adoptat.csv"),
]
# (nou, azi, la ce raspunde). A doua e cea care decide.
PERECHI = [
    ("comb", "sistem", "cat valoreaza adoptia totala"),
    ("comb", "encmean", "**mai adauga selectia pe test ceva peste media de encodere?**"),
    ("comb", "picktest", "mai adauga media de encodere ceva peste selectia pe test?"),
    ("encmean", "picktest", "care parghie e mai mare, cu interval pereche"),
]
# Repere, transcrise din `output/repere_publicate.md`, care nu e generat de niciun script.
REPERE = [("baseline frecventa", 0.478, "0"), ("Archaeology", 0.487, "0"),
          ("TMU-HIT zero-shot, run uniform", 0.6100, "0"), ("TMU-HIT la Nohejl, mixt", 0.654, "mixt"),
          ("G-Eval cu GPT-4o", 0.6571, "3-shot"), ("G-Scale cu GPT-4o", 0.669, "3-shot + T + beta pe 30")]
G_EVAL, G_SCALE, TMU_0 = 0.6571, 0.669, 0.6100
N_TEST_TOTAL = 5624          # randuri de test MLSP, inainte de filtrul de acoperire


def citeste():
    """Cele patru configuratii, plus verificarea ca vorbesc despre aceleasi randuri."""
    d = {}
    for k, eticheta, tab, preds in CFG:
        pt, pp = os.path.join(OUT, tab), os.path.join(OUT, preds)
        for q in (pt, pp):
            if not os.path.exists(q):
                raise SystemExit(f"{q} lipseste. Ruleaza intai fuse_ab.py pentru configuratia {k!r}")
        d[k] = {"eticheta": eticheta, "tab": pd.read_csv(pt), "preds": pd.read_csv(pp),
                "fis_tab": tab, "fis_preds": preds}
    ref = d[CFG[0][0]]["preds"]
    chei_ref = set(zip(ref["lang"], ref["idx"]))
    for k in d:
        p = d[k]["preds"]
        if set(zip(p["lang"], p["idx"])) != chei_ref:
            raise SystemExit(f"{k}: alte randuri decat {CFG[0][0]}, diferentele n-ar fi perechi")
    return d


def distributii(d):
    """Per configuratie si per limba, r si distributia bootstrap, calculate o singura data.

    Randurile se aliniaza pe `idx` peste TOATE cele patru configuratii, nu doua cate doua, ca sa fie
    aceleasi in fiecare din cele patru comparatii. Distributiile se taie la lungime comuna, deci
    reesantionarea k inseamna acelasi lucru peste tot si scaderea lor e o diferenta pereche.
    """
    from mlsp_common import boot_r_ci
    langs = sorted(d[CFG[0][0]]["preds"]["lang"].unique())
    R = {k: {} for k in d}
    B = {k: {} for k in d}
    meta = {}
    for lg in langs:
        g = {}
        for k in d:
            gk = d[k]["preds"]
            gk = gk[gk["lang"] == lg].drop_duplicates("idx").set_index("idx")
            g[k] = gk
        ordine = g[CFG[0][0]].index
        for k in g:
            g[k] = g[k].reindex(ordine)
            if not np.allclose(g[k]["y"].values, g[CFG[0][0]]["y"].values):
                raise SystemExit(f"{lg}/{k}: etichetele nu coincid dupa aliniere")
        y, ctx = g[CFG[0][0]]["y"].values, g[CFG[0][0]]["ctx"].values
        for k in g:
            b = boot_r_ci(y, g[k]["p_fuz"].values, ctx, n_boot=N_BOOT)
            R[k][lg], B[k][lg] = b["r"], b["boot"]
            if k == CFG[0][0]:
                meta[lg] = {"n": len(ordine), "n_ctx": b["n_ctx"]}
    m = min(len(B[k][lg]) for k in B for lg in langs)
    B = {k: {lg: B[k][lg][:m] for lg in langs} for k in B}
    MED = {k: np.vstack([B[k][lg] for lg in langs]).mean(axis=0) for k in B}
    return langs, R, B, MED, meta


def compara(B, MED, R, nou, azi, langs):
    """Diferenta pereche per limba si pe medie, din distributiile deja calculate."""
    rows = []
    for lg in langs:
        dd = B[nou][lg] - B[azi][lg]
        rows.append({"lang": lg, "r_azi": R[azi][lg], "r_nou": R[nou][lg],
                     "d": R[nou][lg] - R[azi][lg], "lo": float(np.percentile(dd, 2.5)),
                     "hi": float(np.percentile(dd, 97.5)), "p": float((dd > 0).mean())})
    dm = MED[nou] - MED[azi]
    r_azi = float(np.mean([R[azi][l] for l in langs]))
    r_nou = float(np.mean([R[nou][l] for l in langs]))
    agg = {"r_azi": r_azi, "r_nou": r_nou, "d": r_nou - r_azi,
           "lo": float(np.percentile(dm, 2.5)), "hi": float(np.percentile(dm, 97.5)),
           "p": float((dm > 0).mean())}
    return pd.DataFrame(rows), agg


def _md_pereche(nume, intrebare, tab, agg, L):
    L.append(f"\n**{nume}.** {intrebare}\n\n")
    L.append("| limba | r azi | r nou | diferenta | CI 95% pereche | P(>0) |\n|---|---|---|---|---|---|\n")
    for r in tab.itertuples():
        # Diferenta exact zero inseamna predictii identice rand cu rand, nu P(>0) = 0.
        pcol = "identic" if r.lo == r.hi == 0.0 else f"{100*r.p:.1f}%"
        L.append(f"| {r.lang} | {r.r_azi:+.4f} | {r.r_nou:+.4f} | {r.d:+.4f} | "
                 f"[{r.lo:+.4f}, {r.hi:+.4f}] | {pcol} |\n")
    L.append(f"| **medie** | {agg['r_azi']:.6f} | **{agg['r_nou']:.6f}** | **{agg['d']:+.6f}** | "
             f"**[{agg['lo']:+.4f}, {agg['hi']:+.4f}]** | **{100*agg['p']:.1f}%** |\n")


def costuri():
    """Tabelul de cost masurat, daca exista. Altfel None, si raportul spune ca lipseste."""
    if not os.path.exists(COST):
        return None
    return pd.read_csv(COST)


def cost_p10():
    """Ce ar costa `qwen35-9b-8bit` pe testul complet, din propriul lui timp per item masurat."""
    p = os.path.join(BAKEOFF, "qwen35-9b-8bit.csv")
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p)
    tot, n = float(d["sec"].sum()), len(d)
    ram = N_TEST_TOTAL - n
    return {"n": n, "sec": tot, "s_per_item": tot / n, "mediana": float(d["sec"].median()),
            "ramase": ram, "min_medie": ram * (tot / n) / 60, "min_mediana": ram * float(d["sec"].median()) / 60,
            "limbi": sorted(d["lang"].unique()) if "lang" in d.columns else []}


def main():
    d = citeste()
    langs, R, B, MED, meta = distributii(d)
    rez = {}
    for nou, azi, intrebare in PERECHI:
        rez[(nou, azi)] = compara(B, MED, R, nou, azi, langs)
    rmed = {k: float(np.mean([R[k][l] for l in langs])) for k in R}

    # tabelul brut: o linie per limba, cele patru configuratii plus cele patru diferente
    raw = pd.DataFrame({"lang": langs, "n": [meta[l]["n"] for l in langs],
                        "n_ctx": [meta[l]["n_ctx"] for l in langs]})
    for k, eticheta, _, _ in CFG:
        raw[f"r_{k}"] = [R[k][l] for l in langs]
    for (nou, azi), (tab, agg) in rez.items():
        t = tab.set_index("lang")
        raw[f"d_{nou}_{azi}"] = [t.loc[l, "d"] for l in langs]
        raw[f"lo_{nou}_{azi}"] = [t.loc[l, "lo"] for l in langs]
        raw[f"hi_{nou}_{azi}"] = [t.loc[l, "hi"] for l in langs]
    os.makedirs(OUT, exist_ok=True)
    raw.to_csv(TABLE, index=False)

    d_enc = rmed["encmean"] - rmed["sistem"]
    d_pick = rmed["picktest"] - rmed["sistem"]
    d_comb = rmed["comb"] - rmed["sistem"]
    suma_naiva = d_enc + d_pick
    frac = d_comb / suma_naiva if suma_naiva else float("nan")
    _, a_ce = rez[("comb", "encmean")]        # comparatia care decide
    _, a_cp = rez[("comb", "picktest")]
    _, a_ep = rez[("encmean", "picktest")]
    _, a_cs = rez[("comb", "sistem")]

    L = ["# Dosarul adoptiei. Cele doua parghii neadoptate, si combinatia lor\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_adoptie.py`. Nicio inferenta LLM, "
         "nicio fuziune recalculata aici: cele patru configuratii vin din `fuse_ab.py`, iar toate "
         "diferentele se construiesc din predictiile lor per instanta. Date brute: "
         f"`output/{os.path.basename(TABLE)}`, o linie per limba.\n\n",
         "**Nu se adopta nimic in fisierul asta.** Fiecare cifra sta pe tagul ei, sistemul publicat "
         "reproduce bit cu bit fara niciun flag, iar decizia o ia Alexandru. Ce urmeaza sunt cifrele "
         "puse una langa alta, inclusiv cele care incurca.\n\n",
         "## 1. Cele patru configuratii\n\n",
         "```\n"
         "sistem      fuse_ab.py --arm lolo --fit test --ens --tag ens \\\n"
         "                --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv\n"
         "encmean     idem, --a-set fert_inloc=output/e1_frozen_preds"
         "_encmean-fara-xlmr-large_lemma_fert_inloc.csv\n"
         "picktest    idem sistem, plus --pick-split test\n"
         "combinatia  --pick-split test SI bratul A pe media de encodere\n```\n\n",
         "| configuratie | r mediu pe 10 limbi | fata de sistem | ce schimba |\n|---|---|---|---|\n",
         f"| sistemul publicat | **{rmed['sistem']:.6f}** | referinta | |\n",
         f"| media a trei encodere | **{rmed['encmean']:.6f}** | {d_enc:+.6f} | bratul A devine media "
         "neponderata a trei encodere standardizate in interiorul limbii, fara `xlmr-large` |\n",
         f"| selectia lui B pe test | **{rmed['picktest']:.6f}** | {d_pick:+.6f} | modelul lui B se "
         "alege pe randurile de test ale celorlalte 9 limbi, ca `w` |\n",
         f"| **combinatia** | **{rmed['comb']:.6f}** | **{d_comb:+.6f}** | amandoua |\n",
         "\n### Cele patru, per limba\n\n",
         "| limba | n | ctx | sistem | encmean | picktest | **combinatia** |\n|---|---|---|---|---|---|---|\n"]
    for lg in langs:
        best = max(("sistem", "encmean", "picktest", "comb"), key=lambda k: R[k][lg])
        cel = {k: (f"**{R[k][lg]:+.4f}**" if k == best else f"{R[k][lg]:+.4f}")
               for k in ("sistem", "encmean", "picktest", "comb")}
        L.append(f"| {lg} | {meta[lg]['n']} | {meta[lg]['n_ctx']} | {cel['sistem']} | "
                 f"{cel['encmean']} | {cel['picktest']} | {cel['comb']} |\n")
    L.append(f"| **medie** | {sum(meta[l]['n'] for l in langs)} | | {rmed['sistem']:.6f} | "
             f"{rmed['encmean']:.6f} | {rmed['picktest']:.6f} | **{rmed['comb']:.6f}** |\n")
    cate = {k: sum(1 for lg in langs if R[k][lg] >= max(R[j][lg] for j in R) - 1e-12) for k in R}
    L.append("\nIngrosat e maximul randului; egalitatile se numara la ambele configuratii. Pe cate "
             "limbi e fiecare configuratie cea mai buna: "
             + ", ".join(f"{dict((k, e) for k, e, _, _ in CFG)[k]} {cate[k]}" for k in
                         ("sistem", "encmean", "picktest", "comb"))
             + f" din {len(langs)}.\n\n"
             "**Si asta e cifra care incurca.** Combinatia are media cea mai mare, dar nu e cea mai "
             f"buna pe cele mai multe limbi: media a trei encodere singura o bate pe "
             + f"{sum(1 for lg in langs if R['encmean'][lg] > R['comb'][lg] + 1e-12)} limbi. "
             f"Din castigul de {d_comb:+.4f} pe medie, franceza singura duce "
             f"{(R['comb']['fr'] - R['sistem']['fr'])/len(langs):+.4f}, adica "
             f"{100*(R['comb']['fr'] - R['sistem']['fr'])/len(langs)/d_comb:.0f}%, dintr-o limba din "
             "zece. Restul se imprastie subtire peste celelalte noua. Cifra pe medie e reala, dar nu "
             "e uniforma, si asta trebuie citit impreuna cu tabelul de mai jos, nu separat.\n\n")

    L.append("### Cele patru comparatii perechi\n\n")
    L.append(f"Aceleasi randuri in toate patru, aliniate pe `idx` peste toate configuratiile deodata. "
             f"{N_BOOT} de reesantionari ale CONTEXTELOR prin `mlsp_common.boot_r_ci`, cu acelasi seed "
             "si acelasi vector de contexte. Distributia bootstrap se calculeaza o data per "
             "configuratie si perechile se formeaza scazand distributii, deci reesantionarea k "
             "inseamna acelasi lucru in toate patru si comparatiile sunt consistente intre ele.\n\n")
    L.append("| comparatie | diferenta pe medie | CI 95% pereche | P(>0) |\n|---|---|---|---|\n")
    for nou, azi, intrebare in PERECHI:
        _, agg = rez[(nou, azi)]
        et_n = dict((k, e) for k, e, _, _ in CFG)[nou]
        et_a = dict((k, e) for k, e, _, _ in CFG)[azi]
        semn = "exclude zero" if (agg["lo"] > 0 or agg["hi"] < 0) else "**include zero**"
        L.append(f"| {et_n} fata de {et_a} | {agg['d']:+.6f} | [{agg['lo']:+.4f}, {agg['hi']:+.4f}] "
                 f"| {100*agg['p']:.1f}% |\n")
    L.append("\nDetaliul fiecareia, per limba:\n")
    for nou, azi, intrebare in PERECHI:
        tab, agg = rez[(nou, azi)]
        et_n = dict((k, e) for k, e, _, _ in CFG)[nou]
        et_a = dict((k, e) for k, e, _, _ in CFG)[azi]
        _md_pereche(f"{et_n} fata de {et_a}", intrebare, tab, agg, L)

    # ---------------------------------------------------------------- 2. complementaritate
    decide_exclude = a_ce["lo"] > 0
    if rmed["comb"] < rmed["encmean"]:
        verdict = ("**Se anuleaza.** Combinatia iese sub media de encodere singura, deci cele doua "
                   "parghii se bat cap in cap si adoptia lor impreuna e mai proasta decat a uneia.")
    elif decide_exclude and frac > 0.85:
        verdict = ("**Se aduna, aproape complet.** Combinatia recupereaza "
                   f"{100*frac:.0f}% din suma naiva a celor doua castiguri, iar intervalul comparatiei "
                   "care decide exclude zero: selectia pe test adauga ceva REAL peste media de "
                   "encodere.")
    elif decide_exclude:
        verdict = ("**Se suprapun partial.** Combinatia recupereaza doar "
                   f"{100*frac:.0f}% din suma naiva, dar intervalul comparatiei care decide exclude "
                   "zero, deci ce ramane e real.")
    else:
        verdict = ("**Sunt redundante.** Intervalul comparatiei care decide include zero, deci "
                   "selectia pe test nu adauga nimic masurabil peste media de encodere.")

    L += ["\n## 2. Verdictul pe complementaritate\n\n",
          "Cele doua parghii ating limbi aproape disjuncte, ceea ce sugera complementaritate. Suma "
          f"naiva a castigurilor lor ar fi {suma_naiva:+.6f}, adica {rmed['sistem'] + suma_naiva:.6f}. "
          "**Suma naiva nu e o predictie**, fiindca `w` realoca intre brate cand ambele urca: daca A "
          "devine mai bun, ponderea lui creste si castigul de pe B se vede mai putin.\n\n",
          f"Masurat, combinatia da **{rmed['comb']:.6f}**, adica {d_comb:+.6f} fata de sistem, deci "
          f"**{100*frac:.0f}% din suma naiva**.\n\n",
          verdict + "\n\n",
          "### Descompunerea per limba\n\n",
          "| limba | encmean singur | picktest singur | suma naiva | combinatia | recuperat |\n"
          "|---|---|---|---|---|---|\n"]
    for lg in langs:
        de_ = R["encmean"][lg] - R["sistem"][lg]
        dp_ = R["picktest"][lg] - R["sistem"][lg]
        dc_ = R["comb"][lg] - R["sistem"][lg]
        s_ = de_ + dp_
        rec = f"{100*dc_/s_:.0f}%" if abs(s_) > 1e-9 else "-"
        L.append(f"| {lg} | {de_:+.4f} | {dp_:+.4f} | {s_:+.4f} | **{dc_:+.4f}** | {rec} |\n")
    s_tot = d_enc + d_pick
    L.append(f"| **medie** | {d_enc:+.4f} | {d_pick:+.4f} | {s_tot:+.4f} | **{d_comb:+.4f}** | "
             f"**{100*frac:.0f}%** |\n")

    w_sist, w_enc, w_pick, w_comb = (float(d[k]["tab"]["w"].mean())
                                     for k in ("sistem", "encmean", "picktest", "comb"))
    fr_e = R["encmean"]["fr"] - R["sistem"]["fr"]
    fr_p = R["picktest"]["fr"] - R["sistem"]["fr"]
    fr_c = R["comb"]["fr"] - R["sistem"]["fr"]
    t_cs = rez[("comb", "sistem")][0].set_index("lang")
    L.append("\n### Franceza, separat, fiindca acolo lucreaza amandoua\n\n"
             f"Franceza e singura limba unde ambele parghii misca ceva mare: encmean {fr_e:+.4f}, "
             f"picktest {fr_p:+.4f}, suma naiva {fr_e + fr_p:+.4f}. Combinatia da **{fr_c:+.4f}**, "
             f"cu interval [{t_cs.loc['fr', 'lo']:+.4f}, {t_cs.loc['fr', 'hi']:+.4f}] si "
             f"P(>0) = {100*t_cs.loc['fr', 'p']:.1f}%, adica "
             f"{100*fr_c/(fr_e + fr_p):.0f}% din suma. "
             "Acolo suprapunerea era cea mai probabila. **Nu s-a materializat.** Recuperarea pe "
             f"franceza, {100*fr_c/(fr_e + fr_p):.0f}%, e practic aceeasi cu cea de pe medie, "
             f"{100*frac:.0f}%, deci suprapunerea nu e concentrata acolo: e mica si uniforma. Ce se "
             f"pierde din suma naiva pe franceza, {fr_c - (fr_e + fr_p):+.4f}, e mecanismul prezis, "
             "realocarea lui `w`, si se vede in ponderi: `w` mediu peste cele zece limbi e "
             f"{w_sist:.3f} la sistem, urca la {w_enc:.3f} cand A se face mai bun prin encodere, "
             f"coboara la {w_pick:.3f} cand B se face mai bun prin selectie, si iese {w_comb:.3f} la "
             "combinatie, adica intre ele. Cele doua parghii chiar trag ponderea in sensuri opuse, "
             "dar nu destul cat sa se anuleze. "
             f"Restul castigului combinatiei, {d_comb - fr_c/len(langs):+.4f} din medie, vine de pe "
             "celelalte noua limbi.\n\n")

    # ---------------------------------------------------------------- 3. costul de inferenta
    L.append("## 3. Costul de inferenta al fiecarei variante\n\n")
    c = costuri()
    if c is None:
        L.append(f"`{os.path.basename(COST)}` lipseste. Ruleaza `analysis_cost_inferenta.py`, care "
                 "masoara forward-ul fiecarui encoder pe cele 5624 de randuri de test si citeste "
                 "coloana `sec` a rularilor de LLM deja facute.\n\n")
    else:
        enc = c[c["componenta"] == "encoder"].set_index("nume")
        llm = c[c["componenta"] == "llm"].set_index("nume")
        L.append("Masurat, nu estimat. Encoderele: `XLMR.embed_frame` peste exact cele "
                 f"{int(enc['n'].iloc[0])} de randuri de test, fara cache, deci se cronometreaza "
                 "forward-ul, nu discul. LLM-ul: coloana `sec` a rularilor care au produs semnalul B, "
                 "adica timpul lor real. Cifrele sunt din `output/cost_inferenta.csv`.\n\n")
        L.append("| componenta | incarcare | forward pe test | ms per rand | fata de `xlmr` |\n"
                 "|---|---|---|---|---|\n")
        baza = float(enc.loc["xlmr", "sec_forward"])
        for nume in enc.index:
            r = enc.loc[nume]
            L.append(f"| encoder `{nume}` | {float(r['sec_incarcare']):.0f}s | "
                     f"{float(r['sec_forward']):.0f}s = {float(r['sec_forward'])/60:.1f} min | "
                     f"{float(r['ms_per_rand']):.1f} | {float(r['sec_forward'])/baza:.1f}x |\n")
        for nume in llm.index:
            r = llm.loc[nume]
            L.append(f"| LLM `{nume}` | | {float(r['sec_forward'])/60:.0f} min pe "
                     f"{int(r['n'])} randuri | {float(r['ms_per_rand']):.0f} | "
                     f"{float(r['sec_forward'])/baza:.0f}x |\n")
        # Media ADOPTATA e pe TREI encodere, fara `xlmr-large`: M3 a aratat ca al patrulea nu se
        # distinge de zero in prezenta lui `--pick-split test`. Deci pretul variantei adoptate se
        # aduna pe cele trei, nu pe tot tabelul, care contine si encoderul masurat dar neadoptat.
        ENC_ADOPTATE = ["xlmr", "labse", "e5"]
        tot3 = float(enc.loc[[n for n in ENC_ADOPTATE if n in enc.index], "sec_forward"].sum())
        gemma = float(llm.loc["gemma4-12b-4bit", "sec_forward"]) if "gemma4-12b-4bit" in llm.index else 0.0
        L.append(f"\n**Ce costa fiecare varianta la inferenta, pe cele {int(enc['n'].iloc[0])} de "
                 "randuri de test:**\n\n"
                 "| varianta | encodere | LLM | total conducta | partea de encodere |\n"
                 "|---|---|---|---|---|\n")
        for nume, secs in [("sistemul publicat, un encoder", baza),
                           ("selectia lui B pe test", baza),
                           ("media a trei encodere", tot3),
                           ("combinatia, adica sistemul adoptat", tot3)]:
            tot = secs + gemma
            L.append(f"| {nume} | {secs/60:.1f} min | {gemma/60:.0f} min | {tot/60:.0f} min | "
                     f"{100*secs/tot:.1f}% |\n")
        L.append(f"\n**Cele trei lucruri pe care le spun cifrele.** Media de encodere inmulteste "
                 f"partea de encodere cu {tot3/baza:.1f}, de la {baza/60:.1f} la {tot3/60:.1f} minute, "
                 f"iar `xlmr-large`, encoderul ramas pe dinafara, ar fi adaugat singur inca "
                 f"{float(enc.loc['xlmr-large','sec_forward'])/baza:.1f}x. Dar LLM-ul ramane dominant: "
                 f"partea de encodere trece de la {100*baza/(baza+gemma):.1f}% la "
                 f"{100*tot3/(tot3+gemma):.1f}% din conducta, deci "
                 f"conducta totala creste cu {100*(tot3-baza)/(baza+gemma):.0f}%, nu se dubleaza. "
                 "**`--pick-split test` costa exact zero in plus**: schimba ce model se alege, nu cate "
                 "modele se ruleaza, iar ambele candidate erau deja rulate.\n\n")
        if not decide_exclude:
            L.append("Fiindca intervalul comparatiei care decide include zero, argumentul de cost "
                     "decide, si decide in favoarea variantei ieftine.\n\n")
        else:
            L.append("Fiindca intervalul comparatiei care decide exclude zero, argumentul de cost nu "
                     "mai decide singur: cele doua parghii cumpara lucruri diferite, iar intrebarea "
                     f"devine daca {a_ce['d']:+.6f} merita "
                     f"{(tot3-baza)/60:.1f} minute in plus per rulare de test.\n\n")

    # ---------------------------------------------------------------- 4. bifurcatiile
    # Ce conteaza pentru declararea bifurcatiilor e cate CONFIGURATII DE SISTEM s-au masurat, nu
    # cate randuri are jurnalul: fiecare configuratie scrie si un rand de brat A. Si se numara si
    # arhiva de dinainte de P11, altfel declaratia ar ascunde exact partea cea mai lunga a cautarii.
    ARHIVA = os.path.join(OUT, "e_rezumat_modele_pre-p11_n5606.csv")
    n_cfg = 0
    if os.path.exists(JURNAL):
        jj = pd.read_csv(JURNAL)
        n_cfg += int((jj["componenta"] == "fuziune").sum()) if "componenta" in jj.columns else len(jj)
    if os.path.exists(ARHIVA):
        n_cfg += int(pd.read_csv(ARHIVA)["metoda"].str.contains("nota 1-5", na=False).sum())
    L += ["## 4. Declararea bifurcatiilor, si e o chestiune de integritate\n\n",
          f"S-au masurat **{n_cfg} de configuratii de sistem** pe splitul de test, "
          "listate in `output/e_rezumat_modele.csv` plus arhiva "
          "`output/e_rezumat_modele_pre-p11_n5606.csv`, de dinainte de renumerotare. "
          "Fiecare e curata pe dinauntru: limba evaluata e exclusa la fiecare nivel de alegere, la "
          "antrenarea bratului A, la alegerea setului de trasaturi, la alegerea modelului lui B, la "
          "`w_src` si la `w`. Niciuna nu foloseste vreo eticheta din limba pe care o evalueaza.\n\n",
          "**Dar alegerea INTRE ele o facem noi, uitandu-ne la scorul de test.** Asta nu se repara cu "
          "inca un nivel de leave-one-language-out, fiindca nu e un nivel de protocol, e o decizie de "
          "cercetator: care experiment se raporteaza ca sistem. Se repara declarand-o.\n\n",
          "Regula dupa care s-ar alege configuratia raportata, scrisa ca sa fie verificabila:\n\n",
          "1. Configuratia raportata e cea cu r mediu maxim pe test dintre cele masurate.\n"
          "2. O configuratie noua se adopta doar daca intervalul ei PERECHE fata de cea curenta "
          "exclude zero. Punctul estimat mai mare nu ajunge.\n"
          "3. Fiecare configuratie masurata ramane in jurnal, inclusiv cele care au pierdut, si "
          "jurnalul se publica.\n\n",
          "**Ce propun ca formulare pentru paper**, in Limitations, nu ascuns intr-o nota de subsol:\n\n",
          "> Am masurat "
          f"{n_cfg} de configuratii de sistem pe splitul de test, listate integral in materialul "
          "suplimentar. Fiecare respecta protocolul leave-one-language-out la toate nivelurile de "
          "alegere, deci nicio cifra per limba nu foloseste etichete din limba respectiva. Alegerea "
          "configuratiei raportate a fost insa facuta de noi, uitandu-ne la scorul mediu de test, si "
          "nu e ea insasi rezultatul unui protocol automat. Cifra raportata trebuie citita ca "
          "maximul unei cautari de dimensiunea de mai sus, nu ca un rezultat obtinut la prima "
          "incercare. Intervalele de incredere raportate sunt perechi fata de configuratia "
          "precedenta si nu sunt corectate pentru comparatii multiple.\n\n",
          "E slabiciunea de reviewer cunoscuta deja din etapa cu scorul public, si aceeasi reparatie: "
          "se declara, nu se ascunde. Ce ar face-o falsificabila, si nu doar onesta, e M1 din planul "
          "de research, adica alegerea intre brate facuta ea insasi leave-one-language-out.\n\n"]

    # ---------------------------------------------------------------- 5. reperele
    L += ["## 5. Pozitionarea fata de repere, fara infrumusetare\n\n",
          "Reperele sunt transcrise in `output/repere_publicate.md`, toate pe acelasi test si toate "
          "ca medie NEPONDERATA a celor 10 corelatii per limba.\n\n",
          "| sistem | etichete in limba tinta | medie |\n|---|---|---|\n"]
    for nume, val, et in REPERE:
        L.append(f"| {nume} | {et} | {val:.4f} |\n")
    for k, eticheta, _, _ in CFG:
        L.append(f"| **al nostru, {eticheta}** | **0** | **{rmed[k]:.4f}** |\n")
    L.append(f"\n| configuratie | fata de TMU-HIT zero-shot {TMU_0:.4f} | fata de G-Eval {G_EVAL:.4f} "
             f"| fata de G-Scale {G_SCALE:.3f} |\n|---|---|---|---|\n")
    for k, eticheta, _, _ in CFG:
        L.append(f"| {eticheta} | {rmed[k]-TMU_0:+.4f} | {rmed[k]-G_EVAL:+.4f} | "
                 f"{rmed[k]-G_SCALE:+.4f} |\n")
    lo_comb = float(np.percentile(MED["comb"], 2.5))
    hi_comb = float(np.percentile(MED["comb"], 97.5))
    L.append(f"\n**Ce NU se poate spune.** Intervalul mediei noastre pe combinatie e "
             f"[{lo_comb:.4f}, {hi_comb:.4f}], adica lat de {hi_comb-lo_comb:.4f}. Diferenta fata de "
             f"G-Scale, {rmed['comb']-G_SCALE:+.4f}, e cu un ordin de marime sub latimea aia. Orice "
             "cifra a noastra intre 0.669 si 0.670 **nu** inseamna ca am trecut de cea mai buna cifra "
             "publicata: diferenta e sub rezolutia masuratorii. In plus nu se poate testa statistic, "
             "fiindca nu avem predictiile per instanta ale lui Nohejl.\n\n"
             "**Si comparatia se scrie in ambele sensuri.** G-Scale foloseste 30 de etichete in limba "
             "tinta plus o temperatura aleasa pe trial-urile tuturor celor 10 limbi; noi folosim zero "
             "etichete si modele open-weight rulate local. A fi sub el nu e un esec de protocol, si a "
             "fi peste el nu e o victorie de protocol. Dar **G-Scale ramane obligatoriu in tabel**, "
             "fiindca e cea mai mare cifra publicata si un reviewer din domeniu observa absenta.\n\n"
             f"**Revendicarea sigura** e fata de singura bara comparabila ca protocol, TMU-HIT "
             f"zero-shot uniform la {TMU_0:.4f}: "
             + ", ".join(f"{eticheta} {rmed[k]-TMU_0:+.4f}" for k, eticheta, _, _ in CFG)
             + ". Comparatia de protocol se castiga detasat in toate cele patru variante, deci "
             "propozitia din abstract nu depinde de decizia de adoptare.\n\n")

    # ---------------------------------------------------------------- 6. ce ramane deschis
    p10 = cost_p10()
    L.append("## 6. Ce ramane deschis inainte de adoptie\n\n")
    if p10:
        L.append(f"**P10, `qwen35-9b-8bit` pe testul complet.** Modelul e rulat pe test doar pe "
                 f"{', '.join(p10['limbi']) or 'o limba'}, {p10['n']} de randuri in "
                 f"{p10['sec']/60:.1f} minute, adica {p10['s_per_item']:.3f} s per item in medie si "
                 f"{p10['mediana']:.3f} s median. Raman **{p10['ramase']} de randuri**, deci "
                 f"**{p10['min_medie']:.0f} de minute** la media masurata, "
                 f"{p10['min_mediana']:.0f} la mediana. Cifra de ~75 de minute din "
                 "`output/e_pick_split.md` e mai mare decat aritmetica propriei ei ipoteze; masurata "
                 f"acum, e ~{p10['min_medie']:.0f}. Ce cumpara: bazinul lui `pick_model` pe test trece "
                 "de la doi candidati efectivi la trei, deci selectia pe test nu mai e restransa de "
                 "acoperire, si limitarea declarata in raportul lui P1 dispare. **Nu se porneste fara "
                 "aprobarea lui Alexandru.**\n\n")
    L.append("**Fixul de sensibilitate la caz din `find_char_span`**, care recupereaza 18 instante "
             "din 5624 si deci schimba `n`. Intra in acelasi eveniment de renumerotare, fiindca "
             "schimba toate cifrele per limba.\n\n"
             "**M1 si M3 din planul de research**, care nu costa inferenta si care fac adoptia "
             "apararabila: M3 e leave-one-encoder-out pe medie, adica raspunde daca `xlmr-large` e "
             "necesar sau daca cele trei encodere ieftine duc castigul; M1 e alegerea intre "
             "selecteaza si mediaza facuta ea insasi leave-one-language-out, care transforma singura "
             "alegere de cercetator ramasa in consecinta de protocol.\n\n"
             "## Ce nu s-a facut aici\n\n"
             "Nu s-a adoptat nimic. Implicitul lui `--pick-split` ramane `trial` si bratul A implicit "
             f"ramane `xlmr`, deci sistemul publicat, {rmed['sistem']:.6f}, reproduce bit cu bit fara "
             "niciun flag, verificat cu `cmp` pe `fusion_lolo_ens.csv` si `fusion_preds_lolo_ens.csv`. "
             "Cifra combinatiei sta pe tagul ei, `ens_encmean_picktest`. Adoptia se face intr-un "
             "singur eveniment de renumerotare, dupa ce Alexandru decide.\n")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    print(f"[P9] sistem {rmed['sistem']:.6f} | encmean {rmed['encmean']:.6f} | "
          f"picktest {rmed['picktest']:.6f} | combinatia {rmed['comb']:.6f}")
    for nou, azi, _ in PERECHI:
        _, agg = rez[(nou, azi)]
        print(f"[P9] {nou:>8} - {azi:<8} {agg['d']:+.6f} [{agg['lo']:+.4f}, {agg['hi']:+.4f}] "
              f"P(>0)={100*agg['p']:.1f}%")
    print(f"[P9] suma naiva {suma_naiva:+.6f}, masurat {d_comb:+.6f}, adica {100*frac:.0f}%")
    print(f"-> {REPORT}")
    print(f"-> {TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
