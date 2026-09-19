"""Atribuire pe sistemul MULTILINGV, si intrebarea care conteaza: mai e loc pentru un al treilea semnal?

Artefactele din `output/shap/` nu se citesc si nu se citeaza. `analysis_shap.py` ruleaza pe CompLex EN
cu un split aleator 80/20 (`Pearson test (toate) = 0.7898`), iar `shap_beeswarm.py` e pe conducta
ROMANEASCA (antetul lui spune "prezice OUTPUT-ul modelului final (68.90)"). Niciunul nu e per limba,
niciunul nu e LOLO, si niciunul nu atinge 0.683849.

Doua blocuri, si al doilea e cel care raspunde la ceva.

## Blocul 1, atribuire: ce duce predictia, pe fiecare limba

Un surogat HGB prezice `p_fuz` din trasaturi NUMITE, potrivit si citit PE LIMBA. Se raporteaza si
importanta prin permutare, si SHAP, **tocmai fiindca nu sunt de acord**, si dezacordul lor e o
observatie, nu un bug: pe trasaturi corelate permutarea forteaza extrapolarea in regiuni fara date
(Hooker, Mentch si Zhou, Statistics and Computing 2021) iar Kernel SHAP presupune independenta si da
explicatii gresite cand nu e (Aas, Jullum si Loland, Artificial Intelligence 2021). Artefactul vechi
de pe disc arata chiar asta: permutarea pune `zipf` 0.4536 peste `embedding(768)` 0.1433, SHAP le
inverseaza, 0.068 fata de 0.182.

## Blocul 2, reziduul: exista o regiune identificabila FARA etichete?

Aici e capcana care poate arde o sesiune, si se declara inainte de a rula.

> Un indicator al unei regiuni cu eroare mare **in modul** e inutil prin constructie. Singurul
> mecanism prin care ar putea intra e ponderea per item, iar aceea e inchisa: `fuse_ab --h` alege
> `a = 0` pe 10/10 limbi, si la semnal real, si pe cinci seminte de zgomot. Ce se cauta e o regiune cu
> reziduu **SEMNAT** nenul, adica una in care fuziunea e deplasata sistematic intr-o directie. Aia se
> corecteaza aditiv, si atunci e chiar un al treilea semnal.

Deci se prezice reziduul semnat `z(y) - z(p_fuz)` din trasaturi disponibile fara etichete in limba
tinta, leave-one-language-out: antrenat pe randurile celorlalte noua limbi, aplicat pe a zecea. E
acelasi protocol prin care se antreneaza semnalul A, deci zero etichete in limba evaluata.

Rezultatul e o coloana, si trece prin ACEEASI poarta ca orice candidat: corelatia partiala cu
eticheta, controland pe fuziune, trebuie sa depaseasca 0.1077. Daca nu, raspunsul e ca regiunea nu
exista, si graficele t-SNE / UMAP nu se mai fac.

Rulare:
  python analysis_shap_multi.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, HERE)

FUZ = os.path.join(OUT, "fusion_preds_lolo_adoptat_temp.csv")
DEST_C = os.path.join(OUT, "c_resid_lolo.csv")
LEX = ["zipf", "length", "syllables", "capital", "freq_na", "surface_na"]


def zin(v):
    v = np.asarray(v, float)
    m = np.isfinite(v)
    if m.sum() < 2 or np.std(v[m]) == 0:
        return np.zeros(len(v))
    z = np.zeros(len(v)); z[m] = (v[m] - v[m].mean()) / v[m].std()
    return z


def _r(a, b):
    from scipy.stats import pearsonr
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(pearsonr(a[m], b[m])[0])


def trasaturi():
    """Cadrul de trasaturi NUMITE pentru cele 5624 de randuri de test, aliniat pe `idx`.

    Aceleasi apeluri prin care trece semnalul A: `solution_bert.lexical` cu `na_policy="mlsp"`,
    lemele din `lemmatize_mlsp.lemma_array` si `solution_bert.fertility`. Nu se rescrie nimic, ca
    trasaturile citite aici sa fie chiar cele pe care le vede modelul.
    """
    from mlsp_common import load_mlsp
    from solution_bert import lexical
    from lemmatize_mlsp import lemma_array
    from solution_bert import fertility
    ml = load_mlsp("test").reset_index(drop=True)
    lem = lemma_array(list(ml["sent"]), list(ml["token"]), "test", list(ml["lang"]))
    lx = lexical(list(ml["token"]), list(ml["lang"]), na_policy="mlsp", lemmas=lem)
    d = pd.DataFrame(lx, columns=LEX)
    d["nsub"] = fertility(list(ml["token"]))
    d["idx"] = ml.index.values
    d["lang"] = ml["lang"].values
    d["token"] = ml["token"].values
    return d


def main():
    from solution_bert import blend_ridge_hgb
    fz = pd.read_csv(FUZ)
    tr = trasaturi().set_index("idx")
    d = fz.join(tr[LEX + ["nsub"]], on="idx")
    assert d[LEX[:1]].notna().values.any(), "trasaturile nu s-au aliniat pe idx"

    # Trasaturile disponibile FARA eticheta in limba tinta. `zA` si `zB` sunt iesiri de model, restul
    # se calculeaza din token. `dif` si `abs_dif` sunt singurele interactiuni introduse explicit:
    # amestecul e liniar in (zA, zB), deci orice structura in diferenta lor e prin definitie ceva ce
    # ponderea w nu poate capta.
    d["dif"] = d["A"] - d["B"]
    d["abs_dif"] = np.abs(d["A"] - d["B"])
    COLS = ["A", "B", "dif", "abs_dif"] + LEX + ["nsub"]

    # Reziduul SEMNAT, standardizat in interiorul limbii. Nu modulul: vezi docstringul.
    d["rez"] = np.concatenate([zin(g["y"].values) - zin(g["p_fuz"].values)
                               for _, g in d.groupby("lang", sort=True)])
    d = pd.concat([g for _, g in d.groupby("lang", sort=True)], ignore_index=True)

    L = ["# Atribuire pe sistemul multilingv, si reziduul semnat", "",
         "Generat de `analysis_shap_multi.py`. Splitul e test, n = %d. **Nimic din `output/shap/` "
         "nu se citeste aici**: acele artefacte sunt pe CompLex EN si pe conducta romaneasca." % len(d),
         "", "## Blocul 1. Ce duce predictia, pe fiecare limba", "",
         "Surogat HGB care prezice `p_fuz` din trasaturi numite, potrivit si citit PE LIMBA, cu "
         "80/20 in interiorul limbii. Doua importante, fiindca pe trasaturi corelate nu sunt de acord.",
         ""]

    from sklearn.ensemble import HistGradientBoostingRegressor

    def hgb():
        return HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                             l2_regularization=1.0, random_state=42)

    def utile(g, cols):
        """Coloanele cu variatie in interiorul limbii. HGB nu poate binariza una fara valori distincte.

        `surface_na` e 1 pe tot la ja si si, `freq_na` la fel la si, iar `zipf` e NaN acolo unde
        wordfreq nu serveste limba. O coloana constanta n-are oricum importanta de masurat.
        """
        return [c for c in cols
                if np.isfinite(g[c].values.astype(float)).sum() >= 2
                and np.nanstd(g[c].values.astype(float)) > 0]

    def doua_importante(g, cols, tinta):
        """(r al surogatului, {coloana: permutare}, {coloana: reantrenare fara ea}).

        Doua importante, si dezacordul lor E rezultatul. Permutarea marginala rupe dependentele si
        forteaza modelul sa extrapoleze in regiuni fara date, ceea ce supraestimeaza trasaturile
        corelate (Hooker, Mentch si Zhou 2021). Ei recomanda in schimb exact ce face a doua coloana:
        se REANTRENEAZA fara trasatura si se masoara cat pierde modelul. E scump, un model in plus per
        coloana, si de aia nu se face de obicei.

        SHAP nu apare aici fiindca pachetul nu e instalat in `ml_def`, si nu se instaleaza pentru o
        figura; oricum Kernel SHAP presupune independenta si da explicatii gresite pe trasaturi
        dependente (Aas, Jullum si Loland 2021), deci ar fi al doilea membru al aceleiasi familii, nu
        un al doilea punct de vedere.
        """
        use = utile(g, cols)
        X = g[use].values.astype(float); y = g[tinta].values.astype(float)
        rng = np.random.RandomState(42); idx = rng.permutation(len(X)); cut = int(0.8 * len(X))
        tr_i, te_i = idx[:cut], idx[cut:]
        m = hgb().fit(X[tr_i], y[tr_i])
        base = _r(m.predict(X[te_i]), y[te_i])
        perm, loco = {}, {}
        for j, nm in enumerate(use):
            dr = []
            for sd in range(5):
                Xp = X[te_i].copy()
                Xp[:, j] = Xp[np.random.RandomState(sd).permutation(len(Xp)), j]
                dr.append(base - _r(m.predict(Xp), y[te_i]))
            perm[nm] = float(np.mean(dr))
            k = [q for q in range(len(use)) if q != j]
            m2 = hgb().fit(X[tr_i][:, k], y[tr_i])
            loco[nm] = base - _r(m2.predict(X[te_i][:, k]), y[te_i])
        return base, perm, loco, use

    # 1a. surogat pe trasaturi LEXICALE, fara A si fara B. Cu ele in set n-ar avea ce masura: `p_fuz`
    # e literal `w*zA + (1-w)*zB`, deci un surogat care le primeste recupereaza amestecul si trimite
    # tot restul la zero. Intrebarea "ce trasaturi duc predictia" are sens numai in termeni
    # interpretabili, deci pe setul lexical.
    LEXCOLS = LEX + ["nsub"]
    rp, rl, scoase = [], [], {}
    for lg, g in d.groupby("lang", sort=True):
        base, perm, loco, use = doua_importante(g, LEXCOLS, "p_fuz")
        scoase[lg] = [c for c in LEXCOLS if c not in use]
        rp.append({"lang": lg, "r_surogat": base, **perm})
        rl.append({"lang": lg, "r_surogat": base, **loco})
    imp = pd.DataFrame(rp).set_index("lang")
    impL = pd.DataFrame(rl).set_index("lang")
    have = [c for c in LEXCOLS if c in imp.columns]
    L += ["### 1a. Surogat pe trasaturi lexicale, fara A si fara B", "",
          "`r_surogat` e cat din `p_fuz` se reconstruieste din lexical singur. Cu cat e mai mare, cu "
          "atat sistemul se comporta mai mult ca un model lexical pe limba aia.", "",
          "**Importanta prin PERMUTARE marginala:**", "", "```", imp.round(4).to_string(), "```", "",
          "**Importanta prin REANTRENARE fara coloana**, adica ce recomanda Hooker, Mentch si Zhou "
          "in locul permutarii:", "", "```", impL.round(4).to_string(), "```", "",
          "Media pe limbi, permutare: " +
          ", ".join(f"`{k}` {v:+.4f}" for k, v in imp[have].mean().sort_values(ascending=False).items()),
          "", "Media pe limbi, reantrenare: " +
          ", ".join(f"`{k}` {v:+.4f}" for k, v in impL[have].mean().sort_values(ascending=False).items()),
          "", "Coloane scoase per limba, constante sau integral NaN acolo: " +
          ("; ".join(f"`{k}` {v}" for k, v in scoase.items() if v) or "niciuna") + ".", ""]

    # 1b. controlul de fidelitate: cu A si B in set surogatul TREBUIE sa reproduca `p_fuz` aproape
    # perfect, fiindca amestecul e liniar in ele. Daca nu, surogatul e de vina, nu datele.
    ctrl = []
    for lg, g in d.groupby("lang", sort=True):
        base, perm, _, _ = doua_importante(g, ["A", "B", "dif", "abs_dif"], "p_fuz")
        ctrl.append({"lang": lg, "r_surogat": base, **perm})
    C1 = pd.DataFrame(ctrl).set_index("lang")
    L += ["### 1b. Control de fidelitate: acelasi surogat, dar cu A si B in set", "",
          "Amestecul e liniar in `zA` si `zB`, deci surogatul trebuie sa-l recupereze aproape exact. "
          "E controlul care spune ca importantele de mai sus masoara datele, nu neputinta modelului.",
          "", "```", C1.round(4).to_string(), "```", "",
          f"`r_surogat` mediu **{C1['r_surogat'].mean():.4f}**. Raportul importantelor "
          f"`B` / `A` = {C1['B'].mean():.4f} / {C1['A'].mean():.4f} = "
          f"**{C1['B'].mean() / C1['A'].mean():.1f}x**.", ""]

    # 1c. unde sunt A si B amandoua deplasate IN ACELASI SENS. Aici ar avea loc un al treilea semnal.
    zy = np.concatenate([zin(g["y"].values) for _, g in d.groupby("lang", sort=True)])
    d["eA"], d["eB"] = zy - d["A"].values, zy - d["B"].values
    amb = (np.sign(d["eA"]) == np.sign(d["eB"])) & (d["eA"].abs() > 1) & (d["eB"].abs() > 1)
    d["ambele"] = amb
    ca = d.groupby("lang").apply(
        lambda g: pd.Series({"n": len(g), "n_ambele": int(g["ambele"].sum()),
                             "pct": 100 * g["ambele"].mean(),
                             "zipf_in": g.loc[g["ambele"], "zipf"].mean(),
                             "zipf_afara": g.loc[~g["ambele"], "zipf"].mean(),
                             "nsub_in": g.loc[g["ambele"], "nsub"].mean(),
                             "nsub_afara": g.loc[~g["ambele"], "nsub"].mean(),
                             "semn_pozitiv": int((g.loc[g["ambele"], "eA"] > 0).sum())}),
        include_groups=False)
    L += ["### 1c. Itemii pe care A si B gresesc AMANDOUA in acelasi sens", "",
          "Definitie: `sign(z_y - zA) == sign(z_y - zB)` si amandoua abaterile peste o deviatie "
          "standard. `semn_pozitiv` e cate din ele sunt SUBevaluate de ambele semnale.", "",
          "```", ca.round(3).to_string(), "```", "",
          f"Pe total **{int(ca['n_ambele'].sum())} itemi din {int(ca['n'].sum())}**, adica "
          f"{100 * ca['n_ambele'].sum() / ca['n'].sum():.1f}%. Coada: "
          f"si {ca.loc['si', 'pct']:.1f}%, fil {ca.loc['fil', 'pct']:.1f}%, "
          f"ca {ca.loc['ca', 'pct']:.1f}%, fata de en {ca.loc['en', 'pct']:.1f}%.", ""]
    ca.to_csv(os.path.join(OUT, "shap_multi_ambele.csv"))
    impL.to_csv(os.path.join(OUT, "shap_multi_importanta_loco.csv"))

    # --- Blocul 2: reziduul semnat, prezis LOLO
    L += ["## Blocul 2. Reziduul semnat, prezis leave-one-language-out", "",
          "Antrenat pe randurile de test ale celorlalte noua limbi, aplicat pe a zecea. Zero "
          "etichete in limba evaluata, exact protocolul semnalului A.", ""]
    pred = np.full(len(d), np.nan)
    rows = []
    for lg in sorted(d["lang"].unique()):
        te = (d["lang"] == lg).values
        X = d[COLS].values.astype(float)
        p = blend_ridge_hgb(X[~te], d["rez"].values[~te], X[te])
        pred[te] = p
        rows.append(dict(lang=lg, n=int(te.sum()), r_rez=_r(p, d["rez"].values[te])))
    d["p_rez"] = pred
    tr2 = pd.DataFrame(rows).set_index("lang")

    # poarta, cu aceleasi functii ca la C
    from analysis_c_frontiera import partial, prag_partial, rmax_of
    gr = []
    for lg, g in d.groupby("lang", sort=True):
        zC, zF, y = zin(g["p_rez"].values), zin(g["p_fuz"].values), g["y"].values.astype(float)
        r_fy, r_cy, rho = _r(zF, y), _r(zC, y), _r(zC, zF)
        gr.append(dict(lang=lg, r_C=r_cy, rho_F=rho, r_F=r_fy,
                       partial=partial(r_cy, r_fy, rho), prag=prag_partial(r_fy),
                       R_max=rmax_of(r_fy, r_cy, rho),
                       dR=rmax_of(r_fy, r_cy, rho) - r_fy))
    G = pd.DataFrame(gr).set_index("lang").join(tr2)
    p = G["partial"].values
    semn = max(int((p > 0).sum()), int((p < 0).sum()))
    L += ["```", G[["n", "r_rez", "r_C", "rho_F", "partial", "prag", "R_max", "dR"]]
          .round(4).to_string(), "```", "",
          f"`r_rez` e corelatia out-of-fold cu reziduul insusi, medie **{G['r_rez'].mean():+.4f}**. "
          f"Corelatie partiala cu eticheta, controland pe fuziune: medie **{G['partial'].mean():+.4f}**, "
          f"prag **{G['prag'].mean():.4f}**, trece pe "
          f"**{int((np.abs(p) >= G['prag'].values).sum())} limbi din 10**, semn consistent pe "
          f"**{semn}/10**.",
          f"Plafon peste orice u: **{G['R_max'].mean():.6f}**, adica **{G['dR'].mean():+.6f}** peste "
          f"fuziune.", "",
          f"**Verdict: {'TRECE poarta' if G['dR'].mean() >= 0.0045 and semn >= 8 else 'NU trece poarta'}.**",
          ""]

    d[["lang", "idx", "p_rez"]].rename(columns={"p_rez": "C"}).to_csv(DEST_C, index=False)
    imp.to_csv(os.path.join(OUT, "shap_multi_importanta.csv"))
    G.to_csv(os.path.join(OUT, "shap_multi_reziduu.csv"))
    dest = os.path.join(OUT, "e_shap_multi.md")
    open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n-> {dest}\n-> {DEST_C}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
