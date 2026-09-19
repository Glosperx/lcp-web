"""P1. Selectia modelului lui B mutata de pe trial pe splitul de evaluare.

Nu ruleaza nicio inferenta si nu recalculeaza nicio fuziune: citeste cele doua configuratii deja
scrise de `fuse_ab.py` si le pune fata in fata.

  azi  `--arm lolo --fit test --ens --tag ens`               -> selectia modelului pe TRIAL
  nou  `--arm lolo --fit test --pick-split test --ens ...`   -> selectia modelului pe TEST

Diferentele sunt PERECHE: aceleasi randuri, acelasi vector de contexte, acelasi seed, deci
`boot_r_ci` reesantioneaza identic pe ambele brate si zgomotul comun al esantionului se anuleaza.
Intervalul mediei se construieste mediind cele zece limbi la fiecare reesantionare, nu mediind
intervale.

Perechea se poate da si din linia de comanda, prin `--azi` si `--nou`, fiindca aceeasi diferenta
pereche se cere si intre alte doua configuratii: `analysis_adoptie.py` o foloseste de patru ori.
Cele trei campuri sunt eticheta, tabelul `fusion_*.csv` si predictiile `fusion_preds_*.csv`, ultimele
doua ca nume de fisier in `output/`. Fara argumente perechea ramane cea de mai sus, iar raportul si
tabelul ies identice bit cu bit, in afara liniei de generare.

Narativul din raport e scris pentru perechea lui P1 si numai pentru ea. Pe alta pereche propozitiile
ar fi false, deci se scrie doar partea calculata, iar comentariul il face cine a cerut comparatia.

Rulare:
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_pick_split.py
  /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python analysis_pick_split.py \
      --azi sistem fusion_lolo_ens.csv fusion_preds_lolo_ens.csv \
      --nou combinatia fusion_lolo_ens_encmean_picktest.csv \
            fusion_preds_lolo_ens_encmean_picktest.csv \
      --report output/e_x.md --table output/x.csv
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
REPORT = os.path.join(OUT, "e_pick_split.md")
TABLE = os.path.join(OUT, "pick_split.csv")
# Dupa P11 tagurile s-au simplificat: `ens` a ramas configuratia de dinainte, iar `picktest` a
# pierdut prefixul. Ambele sunt pe n = 5624.
AZI = ("azi, selectie pe trial", "fusion_lolo_ens.csv", "fusion_preds_lolo_ens.csv")
NOU = ("nou, selectie pe test", "fusion_lolo_picktest.csv", "fusion_preds_lolo_picktest.csv")
N_BOOT = 2000
# Latimile de la §3.6, din `output/e_encoder.md`: acolo aceeasi regula a dat verdictul opus.
ENC_CRIT, ENC_W = 0.0077, 0.082


def _read(spec):
    tab, preds = (os.path.join(OUT, x) for x in spec[1:])
    for q in (tab, preds):
        if not os.path.exists(q):
            raise SystemExit(f"{q} lipseste. Ruleaza intai fuse_ab.py pentru configuratia {spec[0]!r}")
    return pd.read_csv(tab), pd.read_csv(preds)


def paired(a_pred, b_pred):
    """Per limba si pe medie, diferenta PERECHE dintre cele doua configuratii.

    Randurile se aliniaza pe `idx`, cheia pozitiei in cadrul nefiltrat. Daca un rand lipseste
    dintr-una din configuratii, se opreste: o medie pe seturi diferite de randuri n-ar fi o
    diferenta, ar fi doua cifre.
    """
    from mlsp_common import boot_r_ci
    rows, boots = [], {"azi": [], "nou": []}
    for lg in sorted(b_pred["lang"].unique()):
        g0 = a_pred[a_pred["lang"] == lg].drop_duplicates("idx").set_index("idx")
        g1 = b_pred[b_pred["lang"] == lg].drop_duplicates("idx").set_index("idx")
        if set(g0.index) != set(g1.index):
            raise SystemExit(f"{lg}: cele doua configuratii n-au aceleasi randuri "
                             f"({len(g0)} fata de {len(g1)}), diferenta n-ar fi pereche")
        g0 = g0.reindex(g1.index)
        if not np.allclose(g0["y"].values, g1["y"].values):
            raise SystemExit(f"{lg}: etichetele nu coincid dupa aliniere")
        y, ctx = g1["y"].values, g1["ctx"].values
        b0 = boot_r_ci(y, g0["p_fuz"].values, ctx, n_boot=N_BOOT)
        b1 = boot_r_ci(y, g1["p_fuz"].values, ctx, n_boot=N_BOOT)
        k = min(len(b0["boot"]), len(b1["boot"]))
        d = b1["boot"][:k] - b0["boot"][:k]
        rows.append({"lang": lg, "n": len(g1), "n_ctx": b1["n_ctx"], "r_azi": b0["r"], "r_nou": b1["r"],
                     "d": b1["r"] - b0["r"], "lo": float(np.percentile(d, 2.5)),
                     "hi": float(np.percentile(d, 97.5)), "p": float((d > 0).mean())})
        boots["azi"].append(b0["boot"][:k]); boots["nou"].append(b1["boot"][:k])
    m = min(len(v) for k in boots for v in boots[k])
    M = {k: np.vstack([v[:m] for v in boots[k]]).mean(axis=0) for k in boots}
    dm = M["nou"] - M["azi"]
    agg = {"lo": float(np.percentile(dm, 2.5)), "hi": float(np.percentile(dm, 97.5)),
           "p": float((dm > 0).mean()),
           "nou_lo": float(np.percentile(M["nou"], 2.5)),
           "nou_hi": float(np.percentile(M["nou"], 97.5))}
    return pd.DataFrame(rows), agg


def criteriu(split):
    """Per limba: candidatii vazuti de `pick_model` pe splitul dat, valoarea criteriului si latimea.

    Criteriul unui candidat pentru limba L e media lui r peste CELELALTE 9 limbi, exact cantitatea
    pe care `pick_model` o maximizeaza. Bazinul e restrans la modelele masurate efectiv pe L, ca in
    `load_signals`, fiindca un model nemasurat pe L nu e o alternativa disponibila acolo.
    """
    from bakeoff_trial import load_runs, r_table
    runs = load_runs(split)
    tab = r_table(runs, "B")
    cover = {k: {str(l) for l in df["lang"].unique()} for k, df in runs.items()}
    langs = sorted({l for per in tab.values() for l in per})
    rows = []
    for L in langs:
        vals = {}
        for k, per in tab.items():
            if L not in cover.get(k, set()):
                continue                      # nemasurat pe L, deci indisponibil acolo
            v = [per[l][0] for l in langs if l != L and l in per and np.isfinite(per[l][0])]
            if v:
                vals[k] = float(np.mean(v))
        if not vals:
            continue
        best = max(vals, key=vals.get)
        rows.append({"lang": L, "n_cand": len(vals), "ales": best, "crit_best": vals[best],
                     "crit_min": min(vals.values()),
                     "latime": max(vals.values()) - min(vals.values()),
                     "toti": ", ".join(f"`{k}` {v:+.3f}" for k, v in
                                       sorted(vals.items(), key=lambda kv: -kv[1]))})
    return pd.DataFrame(rows), cover, langs


def acoperire(cover, langs):
    """Cine e masurat unde, pe splitul de evaluare. Bazinul real, nu cel nominal."""
    return pd.DataFrame([{"model": k, "limbi": len(v & set(langs)),
                          "unde": ", ".join(sorted(v & set(langs)))} for k, v in cover.items()])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Diferenta PERECHE intre doua configuratii de fuziune.")
    ap.add_argument("--azi", nargs=3, metavar=("ETICHETA", "TABEL", "PREDS"), default=list(AZI),
                    help="configuratia de referinta; TABEL si PREDS sunt nume de fisier in output/")
    ap.add_argument("--nou", nargs=3, metavar=("ETICHETA", "TABEL", "PREDS"), default=list(NOU),
                    help="configuratia comparata, aceleasi trei campuri")
    ap.add_argument("--report", default=REPORT, help="unde se scrie raportul markdown")
    ap.add_argument("--table", default=TABLE, help="unde se scrie tabelul brut, o linie per limba")
    a = ap.parse_args(argv)
    azi, nou = tuple(a.azi), tuple(a.nou)
    report, table = a.report, a.table
    # Narativul de mai jos afirma lucruri adevarate doar despre perechea lui P1. Pe alta pereche se
    # scrie numai ce e calculat, ca sa nu ramana in raport propozitii care nu mai corespund datelor.
    p1 = (azi == AZI and nou == NOU)
    t_azi, p_azi = _read(azi)
    t_nou, p_nou = _read(nou)
    d, agg = paired(p_azi, p_nou)
    r_azi, r_nou = t_azi["r_fuz_raw"].mean(), t_nou["r_fuz_raw"].mean()
    c_test, cover_test, langs = criteriu("test")
    c_trial, _, _ = criteriu("trial")
    cov = acoperire(cover_test, langs)
    w_lat = (t_nou["w_curba_max"] - t_nou["w_curba_min"]).mean()
    lat = c_test["latime"].mean()

    raw = d.merge(c_test[["lang", "n_cand", "crit_best", "crit_min", "latime"]], on="lang")
    raw["model_trial"] = raw["lang"].map(dict(zip(t_azi["lang"], t_azi["model_B"])))
    raw["model_test"] = raw["lang"].map(dict(zip(t_nou["lang"], t_nou["model_B"])))
    raw["w_src"] = raw["lang"].map(dict(zip(t_nou["lang"], t_nou["w_src"])))
    raw["w"] = raw["lang"].map(dict(zip(t_nou["lang"], t_nou["w"])))
    raw["w_latime"] = raw["lang"].map(dict(zip(t_nou["lang"],
                                              t_nou["w_curba_max"] - t_nou["w_curba_min"])))
    raw = raw.rename(columns={"d": "d_pereche", "lo": "d_lo", "hi": "d_hi", "p": "d_p",
                              "latime": "crit_latime", "n_cand": "crit_n_cand"})
    raw = raw[["lang", "n", "n_ctx", "model_trial", "model_test", "w_src", "w", "r_azi", "r_nou",
               "d_pereche", "d_lo", "d_hi", "d_p", "crit_n_cand", "crit_best", "crit_min",
               "crit_latime", "w_latime"]]
    os.makedirs(OUT, exist_ok=True)
    raw.to_csv(table, index=False)

    L = ["# P1. Selectia modelului lui B, mutata de pe trial pe splitul de evaluare\n\n" if p1
         else f"# Diferenta pereche: {nou[0]} fata de {azi[0]}\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `analysis_pick_split.py`. Nicio inferenta "
         "LLM, nicio cifra recalculata aici: cele doua configuratii vin din `fuse_ab.py`, iar "
         "diferentele se construiesc din predictiile lor per instanta. Date brute: "
         f"`output/{os.path.basename(table)}`, o linie per limba.\n\n"]
    if p1:
        L += ["```\n"
              "azi  fuse_ab.py --arm lolo --fit test --ens --tag ens \\\n"
              "         --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv \\\n"
              "         --vs output/fusion_preds_lolo_fittest_lemma.csv\n"
              "nou  fuse_ab.py --arm lolo --fit test --pick-split test --ens --tag ens_picktest \\\n"
              "         --a-set fert_inloc=output/e1_frozen_preds_lemma_fert_inloc.csv \\\n"
              "         --vs output/fusion_preds_lolo_ens.csv\n```\n\n",
              "## Ce se schimba, si numai atat\n\n",
              "`fuse_ab.py` alegea modelul lui B din tabelul de **trial**, prin `pick_model(tab_pick, ...)` "
              "in `load_signals`, in timp ce ponderea `w` se potrivea pe **test**, prin `--fit test`. "
              "Asimetria e exact cea pe care docstringul fisierului o condamna cand motiveaza `--fit "
              "test`: cele doua componente ale aceluiasi sistem foloseau splituri diferite fara motiv. "
              "Motivul fusese eliminat pentru `w` si ramasese pentru model.\n\n",
              "Sub `--pick-split test`, selectia pentru limba L se face pe randurile de TEST ale "
              "**celorlalte 9 limbi**, exact ca `w` si exact ca antrenarea bratului A, unde "
              "`Xtr = np.vstack([Xen, Xml[tr]])` cu `tr = (lang != L)` ruleaza peste aceleasi randuri de "
              "test. Zero etichete din L, la niciun nivel. Selectia imbricata a limbilor de potrivire "
              "foloseste acelasi tabel, deci nu se deschide o scurgere pe unde s-a inchis una. Garantiile "
              "linie cu linie sunt in tabelul de audit din `output/e_fusion_lolo_picktest.md`, care "
              "are acum si randul splitului de selectie.\n\n",
              "**Distinctia care trebuie tinuta curata:** o selectie recalculata pe testul limbii **L** ar "
              "fi tuning pe scorul raportat, si comentariul din `bakeoff_trial.aggregate` are dreptate "
              "cand o refuza. Asta nu e aia. Aici L e exclusa chiar din media care alege, ca peste tot "
              "altundeva in protocol.\n\n"]
    else:
        L += [f"```\nazi  {azi[0]}: output/{azi[1]}, output/{azi[2]}\n"
              f"nou  {nou[0]}: output/{nou[1]}, output/{nou[2]}\n```\n\n",
              "Narativul lui P1 lipseste de aici intentionat: propozitiile lui sunt despre perechea lui "
              "si pe alta pereche ar fi false. Mai jos e numai ce se calculeaza din predictiile celor "
              "doua configuratii de mai sus.\n\n"]
    L += ["## Rezultatul, diferente PERECHE pe contexte\n\n",
         f"Aceleasi randuri de test pe ambele brate, verificat rand cu rand pe `idx`. {N_BOOT} de "
         "reesantionari ale CONTEXTELOR prin `mlsp_common.boot_r_ci`, cu acelasi seed si acelasi "
         "vector de contexte, deci reesantionarea k e aceeasi pe ambele configuratii si intervalul e "
         "al diferentei, nu al sumei incertitudinilor.\n\n",
         "| limba | n | ctx | r azi | r nou | diferenta | CI 95% pereche | P(>0) |\n"
         "|---|---|---|---|---|---|---|---|\n"]
    for r in d.itertuples():
        # Diferenta exact zero inseamna predictii identice, nu P(>0) = 0: aceleasi rand cu rand,
        # fiindca limba a primit acelasi model, acelasi set, acelasi w_src si acelasi w.
        pcol = "identic" if r.lo == r.hi == 0.0 else f"{100*r.p:.1f}%"
        L.append(f"| {r.lang} | {r.n} | {r.n_ctx} | {r.r_azi:+.4f} | **{r.r_nou:+.4f}** | "
                 f"{r.d:+.4f} | [{r.lo:+.4f}, {r.hi:+.4f}] | {pcol} |\n")
    L.append(f"| **medie** | {int(d['n'].sum())} | | {r_azi:+.6f} | **{r_nou:+.6f}** | "
             f"{r_nou - r_azi:+.6f} | [{agg['lo']:+.4f}, {agg['hi']:+.4f}] | {100*agg['p']:.1f}% |\n")
    ident = d[(d["lo"] == 0) & (d["hi"] == 0)]["lang"].tolist()
    up = int(((d["d"] > 0) & ~d["lang"].isin(ident)).sum())
    dnl = d[d["hi"] < 0]["lang"].tolist()
    sig = int((d["lo"] > 0).sum())
    L.append(f"\nDintre cele {len(d)} limbi, {len(ident)} raman **identice rand cu rand** "
             f"({', '.join(ident)}): acolo se alegea deja acelasi model, acelasi set, acelasi "
             f"`w_src` si acelasi `w`, deci predictiile nu se schimba deloc. Din restul, {up} urca "
             f"si {len(d) - len(ident) - up} coboara. Intervalul pereche exclude zero in sus pe "
             f"{sig} si in jos pe {len(dnl)}"
             + (f" ({', '.join(dnl)}), iar scaderile alea se raporteaza ca atare: sunt mici, "
                f"{', '.join(f'{r.lang} {r.d:+.4f}' for r in d[d.lang.isin(dnl)].itertuples())}, "
                "si vin din `w_src` si `w`, care se re-aleg pe un set de potrivire in care "
                "franceza si-a schimbat modelul" if dnl else "")
             + f". Intervalul mediei se construieste mediind cele zece limbi la fiecare "
             f"reesantionare, deci e o distributie a mediei, nu o medie de distributii; r-ul nou "
             f"singur are [{agg['nou_lo']:+.4f}, {agg['nou_hi']:+.4f}].\n\n")
    if p1:
        fr = d[d["lang"] == "fr"]
        if len(fr):
            f0 = fr.iloc[0]
            L.append(f"**Franceza duce singura schimbarea:** {f0.r_azi:+.4f} -> {f0.r_nou:+.4f}, adica "
                     f"{f0.d:+.4f}, cu interval [{f0.lo:+.4f}, {f0.hi:+.4f}] si P(>0) = {100*f0.p:.1f}%. "
                     "E limba despre care `output/repere_publicate.md` spune ca explica singura tot "
                     "deficitul fata de reperele publicate. Celelalte noua se misca doar prin `w_src` si "
                     "`w`, care se re-aleg pe un set de potrivire in care franceza are alt model, iar "
                     "acele miscari sunt de ordinul a cateva miimi, in ambele sensuri.\n\n")

        bfr = (float(t_nou.loc[t_nou["lang"] == "fr", "r_B_raw"].iloc[0])
               - float(t_azi.loc[t_azi["lang"] == "fr", "r_B_raw"].iloc[0]))
        L += ["## Harta model-per-limba\n\n",
              "Sub protocolul corect selectia **degenereaza la un singur model peste toate limbile**.\n\n",
              "| limba | model ales pe trial | model ales pe test |\n|---|---|---|\n"]
        m0 = dict(zip(t_azi["lang"], t_azi["model_B"]))
        for r in t_nou.itertuples():
            mark = "" if m0.get(r.lang) == r.model_B else "  <- se schimba"
            L.append(f"| {r.lang} | `{m0.get(r.lang)}` | `{r.model_B}`{mark} |\n")
        L += ["\n### Ce inseamna pentru revendicarea de noutate\n\n",
              "Revendicarea „LOLO inclusiv la alegerea modelului\" devine: **mecanismul de selectie "
              "exista si, pe splitul corect, alege acelasi model peste tot; selectia facuta pe trial e "
              f"cea care difera, si e cea care costa {bfr:.3f} r pe franceza la semnalul B**, adica "
              f"{f0.d:+.4f} la fuziune. Asta e un rezultat, nu o "
              "pierdere. E a doua demonstratie a tezei ca trial-ul e un proxy prost pentru test pe "
              "semnalul B, prima fiind decalajul masurat in `output/e_split_gap.md`. Mecanismul ramane "
              "necesar "
              "in lucrare, fiindca fara el nu se poate arata ca alegerea e stabila; ce nu se mai poate "
              "revendica e o harta neomogena de modele.\n\n",
              "## Cat de lat e criteriul care alege\n\n",
              "`latime criteriu` e r maxim minus r minim peste candidatii pe care `pick_model` ii vede "
              "efectiv pentru limba L, unde valoarea unui candidat e media lui r peste celelalte 9 limbi. "
              "Cu cat e mai lata, cu atat argmaxul separa ceva real si nu zgomot.\n\n",
              "| limba | candidati | criteriul castigatorului | cel mai slab | latime | toti candidatii |\n"
              "|---|---|---|---|---|---|\n"]
        for r in c_test.itertuples():
            L.append(f"| {r.lang} | {r.n_cand} | {r.crit_best:+.4f} | {r.crit_min:+.4f} | "
                     f"**{r.latime:.4f}** | {r.toti} |\n")
        L.append(f"| **medie** | {c_test['n_cand'].mean():.1f} | {c_test['crit_best'].mean():+.4f} | "
                 f"{c_test['crit_min'].mean():+.4f} | **{lat:.4f}** | |\n")
        L += [f"\n### Aceeasi regula, doua verdicte opuse, si amandoua masurate\n\n",
              "Regula transversala a proiectului e „cand criteriul e plat, mediaza, nu alege\". Aici ea "
              "spune **selecteaza**, si o spune cu cifre:\n\n",
              "| alegere | latime criteriu | latime curba `w` | raport | verdictul regulii |\n"
              "|---|---|---|---|---|\n",
              f"| modelul lui B, pe test | **{lat:.4f}** | {w_lat:.4f} | de {lat/w_lat:.1f} ori mai LAT | "
              "selecteaza |\n",
              f"| encoderul, §3.6 | {ENC_CRIT:.4f} | {ENC_W:.3f} | de {ENC_W/ENC_CRIT:.1f} ori mai plat | "
              "mediaza |\n",
              "\nCele doua randuri vin din aceeasi regula aplicata la doua alegeri diferite si dau "
              "verdicte opuse, fiecare confirmat de masuratoare: la encodere selectia chiar a cazut si "
              "medierea a castigat, aici selectia chiar separa si franceza urca. O regula care ar spune "
              "acelasi lucru peste tot n-ar spune nimic.\n\n",
              "## Limitare, declarata fara sa fie intrebat nimeni\n\n",
              "Bazinul de pe splitul de test nu e cel de pe trial. Acoperirea, masurata:\n\n",
              "| model | limbi pe test | unde |\n|---|---|---|\n"]
        for r in cov.sort_values("limbi", ascending=False).itertuples():
            L.append(f"| `{r.model}` | {r.limbi} | {r.unde} |\n")
        nfull = int((cov["limbi"] == len(langs)).sum())
        L += [f"\n`qwen35-9b-8bit` e rulat pe test **doar pe franceza**, deci pentru fiecare limba "
              f"bazinul are efectiv {nfull} candidati, nu {len(cov)}. Un reviewer poate spune, pe drept, "
              "„ati selectat pe test dintre modelele pe care s-a intamplat sa le rulati pe test\". "
              "Restrangerea nu foloseste nicio eticheta, e o constatare de acoperire, dar ingusteaza "
              "alegerea si trebuie scrisa ca limitare, nu ca detaliu.\n\n",
              "Reparatia e o rulare separata a lui `qwen35-9b-8bit` pe testul complet, ~75 de minute de "
              "inferenta la 0.78 s per item pe cele 5055 de instante ramase, si **cere aprobarea lui "
              "Alexandru**. Pana atunci cifra de mai sus se citeaza cu bazinul declarat.\n\n",
              "Al doilea lucru de tinut minte: pe trial bazinul e mai larg, cu 7 modele pe toate cele 10 "
              "limbi, iar acolo criteriul are alta forma. Latimea lui pe trial e "
              f"{c_trial['latime'].mean():.4f} in medie, dar **nicio cifra de trial nu se citeaza ca "
              "predictie pentru test**: decalajul dintre splituri e masurat, depinde de semnal si de "
              "model, si are semne opuse.\n\n",
              "## Ce nu s-a facut\n\n",
              "Nu s-a adoptat nimic. Implicitul lui `--pick-split` ramane `trial`, deci sistemul "
              f"publicat, {r_azi:.6f}, reproduce bit cu bit fara niciun flag, verificat cu `cmp` pe "
              "`fusion_lolo_ens.csv` si `fusion_preds_lolo_ens.csv`. Cifra noua sta pe tagul ei, "
              "`ens_picktest`. Adoptia se face intr-un singur eveniment de renumerotare, impreuna cu "
              "media de encodere si cu fixul de caz din `find_char_span`.\n"]
    else:
        L.append("Sectiunile care urmau aici in raportul lui P1, harta model-per-limba, "
                 "latimea criteriului, limitarea de bazin si nota de neadoptare, sunt scrise "
                 "despre perechea aceea si nu se transfera. Comparatia de fata se citeste din "
                 "tabelul de mai sus.\n")
    with open(report, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    print(f"[P1] r mediu: azi {r_azi:.6f} | nou {r_nou:.6f} | diferenta {r_nou - r_azi:+.6f} "
          f"[{agg['lo']:+.4f}, {agg['hi']:+.4f}] P(>0)={100*agg['p']:.1f}%")
    print(f"[P1] latime criteriu {lat:.4f} fata de latime curba w {w_lat:.4f}")
    print(f"-> {report}")
    print(f"-> {table}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
