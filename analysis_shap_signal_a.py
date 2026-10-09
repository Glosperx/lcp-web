"""SHAP exact pe semnalul A ADOPTAT: media celor trei encodere (XLM-R base, LaBSE, mE5 base), cu
bratele p_en si p_multi amestecate prin w_src per limba, adica exact predictiile LOLO care intra in
fuziunea pe 11 limbi cu engleza curata (0.692527).

De ce nu o potrivire noua pe tot bazinul, ca SHAP-ul din 29 aug (doar XLM-R): graficul trebuie sa
explice predictiile care intra efectiv in fuziune. In interiorul unei limbi L, A e o functie AFINA de
sase predictii de baza, 3 encodere x {p_en, p_multi}:
  make_enc_mean.py   z in (split, limba) pe fiecare encoder, apoi media celor trei;
  fuse_ab.zA_of      A = z( w_src z(pe) + (1 - w_src) z(pm) ), z in interiorul limbii.
Valorile Shapley sunt liniare in functia explicata, deci SHAP(A) e aceeasi combinatie liniara a
SHAP-urilor celor sase modele, fara nicio aproximare. Fiecare model e blendul Ridge+HGB, media lor:
  Ridge (imputer + scaler + ridge) e afin in intrarea scalata, deci phi_j = coef_j (z_j - media z_j);
  HGB prin TreeExplainer interventional, exact.

Referinta e media LIMBII, nu distributia de antrenare: fundalul fiecarei explicatii sunt toate
randurile limbii explicate. A e standardizat in interiorul limbii, deci un decalaj constant pe o limba
nu muta nicio predictie fata de celelalte din ea. Cu referinta de antrenare (prima rulare,
tree_path_dependent) frecventa primea 6.5 unitati z pe sinhaleza, unde coloana e constanta (zipf 0, nu
exista lista): un decalaj pe care z-ul il anuleaza. Cu fundalul limbii, o coloana constanta pe limba
primeste exact 0, iar baza lui A iese 0 pe fiecare rand. Masker-ul implicit al lui shap esantioneaza
fundalul la 100 de randuri; aici se da explicit `max_samples` = toata limba.

Matricele vin din `frozen_trial_gap(export_blocks=...)`, adica din acelasi cod care a produs
predictiile adoptate, nu dintr-o copie. Exportul refuza `--en-fara-complex`, dar blocurile nu depind
de flag: el schimba numai multimea de antrenare la L = en, care se reface aici ca in bucla originala.

Controale, toate inainte de grafic; scriptul se opreste daca pica vreunul:
  1. p_en si p_multi refacute == CSV-urile adoptate, pe fiecare encoder;
  2. A compus == coloana A din output/fusion_preds_lolo_en_fara_complex_ro11.csv;
  3. suma SHAP + baza == A, pe fiecare rand.
Tolerantele 1 si 2 sunt de ordinul 1e-12. A treia nu poate fi: blocurile sunt float32, ca in fluxul
adoptat, deci Ridge-ul e potrivit si prezice in float32, cu rotunjire de ~1e-7 pe predictie (masurat:
1.2e-7; TreeSHAP pe HGB reconstituie la 1e-15). SHAP-ul e calculat in float64, deci e exact pana la
acea rotunjire, care trece prin coeficientii de standardizare in A.

Rulare (envs/ml_def, ~15 minute, embeddingurile sunt in cache):
  python analysis_shap_signal_a.py --blocks DIR
  python analysis_shap_signal_a.py --plot-only     # doar graficul, din valorile salvate
Iesiri: output/shap_signal_a_adopted.{pdf,png}, output/shap_signal_a_adopted_importance.csv,
output/shap_signal_a_adopted_raw.npz, plus copia pentru paper
Paper/Articol_Multilingv/figures/fig_shap_signal_a.pdf.
"""
import argparse
import os
import shutil
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
FIG = os.path.join(HERE, "Paper", "Articol_Multilingv", "figures")
ENCODERS = ("xlmr", "labse", "e5")
PREDS = {e: os.path.join(OUT, "e1_frozen_preds" + ("" if e == "xlmr" else f"_{e}")
                         + "_lemma_fert_inloc_en-fara-complex_ro11.csv") for e in ENCODERS}
FUSION = os.path.join(OUT, "fusion_preds_lolo_en_fara_complex_ro11.csv")
D = 768
# Coloanele de dupa embedding, in ordinea din solution_bert._Xc cu afeat fert_inloc (lungimea scoasa):
# fertilitatea centrata, apoi lexical() fara lungime, apoi cei doi indicatori de disponibilitate.
LEX = ["Subword count", "Word frequency (form or lemma)", "Syllable count", "Capitalised",
       "No frequency list (flag)", "No surface features (flag)"]
EMB = "Embedding (3 encoders, summed)"
RAW = os.path.join(OUT, "shap_signal_a_adopted_raw.npz")
TOL_PRED, TOL_A = 1e-12, 1e-9
TOL_MODEL, TOL_SUM = 1e-6, 1e-5            # rotunjirea float32 a Ridge-ului, vezi docstring


def zscore(v):
    """Acelasi contract ca make_enc_mean.zscore si fuse_ab.zscore (std de populatie)."""
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std()


def blocks(enc, cache, _date={}):
    """Matricele exacte ale lui frozen_trial_gap pentru un encoder, fara nicio potrivire."""
    path = os.path.join(cache, f"blocks_{enc}.npz")
    if not os.path.exists(path):
        import finetune_xlmr as fx
        if not _date:
            _date.update(en=fx.load_complex_en(), ml=fx.load_mlsp(include_ro=True),
                         mlt=fx.load_mlsp("trial"))
        fx.frozen_trial_gap(_date["en"], _date["ml"], _date["mlt"], lemma_freq=True,
                            afeat="fert_inloc", encoder=enc, export_blocks=path)
    z = np.load(path)
    ok = np.load(os.path.join(HERE, "data", f"emb_mlsp10_{enc}_last4_7211_ok.npy"))
    idx = np.flatnonzero(ok)                       # pozitia in load_mlsp("test", include_ro=True)
    assert len(idx) == len(z["Xml"]), (enc, len(idx), z["Xml"].shape)
    return z["Xen_f"], z["yen"], z["Xml"], z["y"], z["lang"].astype(str), idx


def fit_blend(Xtr, ytr):
    """Aceleasi doua modele ca solution_bert.blend_ridge_hgb, dar intoarse potrivite."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from solution_bert import SEED
    ridge = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("s", StandardScaler()), ("r", Ridge(alpha=300, random_state=SEED))])
    hgb = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                        l2_regularization=1.0, random_state=SEED)
    return ridge.fit(Xtr, ytr), hgb.fit(Xtr, ytr)


def explain(models, X):
    """(predictie, phi, baza) ale blendului pe randurile X, cu fundalul = X insusi (o limba).
    Predictia e calculata ca in blend_ridge_hgb; phi + baza o reconstituie (verificat de apelant),
    iar baza e media predictiei pe limba."""
    import shap
    ridge, hgb = models
    pred = np.mean([ridge.predict(X), hgb.predict(X)], axis=0)
    Z = ridge[:-1].transform(X).astype(float)      # imputer + scaler, potrivite pe antrenare
    coef = ridge[-1].coef_.astype(float)
    mu = Z.mean(0)
    phi_r = (Z - mu) * coef
    base_r = float(ridge[-1].intercept_) + float(mu @ coef)
    # Masker explicit: cu matricea simpla shap ar esantiona fundalul la 100 de randuri.
    ex = shap.TreeExplainer(hgb, data=shap.maskers.Independent(X, max_samples=len(X)),
                            feature_perturbation="interventional")
    phi_h = np.asarray(ex.shap_values(X, check_additivity=False), float)
    base_h = float(np.ravel(ex.expected_value)[0])
    return pred, (phi_r + phi_h) / 2, (base_r + base_h) / 2


def encoder_arms(enc, cache):
    """p_en, p_multi si explicatiile lor pe cele 7211 randuri, refacute ca in bucla adoptata."""
    Xen, yen, Xml, y, lang, idx = blocks(enc, cache)
    n, w = Xml.shape
    p_en, p_mu = np.empty(n), np.empty(n)
    f_en, f_mu = np.empty((n, w)), np.empty((n, w))
    b_en, b_mu = np.empty(n), np.empty(n)
    m_en = fit_blend(Xen, yen)                     # bratul EN-only, o singura potrivire
    for L in sorted(pd.unique(lang)):
        te, tr = lang == L, lang != L
        if L == "en":                              # --en-fara-complex: CompLex iese la L = en
            Xtr, ytr = Xml[tr], y[tr]
        else:
            Xtr, ytr = np.vstack([Xen, Xml[tr]]), np.concatenate([yen, y[tr]])
        p, f, b = explain(fit_blend(Xtr, ytr), Xml[te])
        p_mu[te], f_mu[te], b_mu[te] = p, f, b
        # La L = en bratul EN-only ar aduce CompLex inapoi; fluxul adoptat il inlocuieste cu p_multi.
        # Altfel acelasi model EN-only, explicat cu fundalul limbii L.
        p_en[te], f_en[te], b_en[te] = (p, f, b) if L == "en" else explain(m_en, Xml[te])
        print(f"  {enc:5s} {L:4s} n={te.sum():4d}", flush=True)

    # Control 1: predictiile refacute trebuie sa fie cele adoptate.
    ref = pd.read_csv(PREDS[enc])
    ref = ref[ref["split"] == "test"].set_index("idx").loc[idx]
    for nume, mine, col in (("p_en", p_en, "p_en"), ("p_multi", p_mu, "p_multi")):
        err = np.abs(mine - ref[col].values).max()
        print(f"  control 1 {enc} {nume}: max |dif| = {err:.2e}", flush=True)
        if err > TOL_PRED:
            raise SystemExit(f"{enc} {nume} nu reproduce {os.path.basename(PREDS[enc])}")
    for nume, f, b, p in (("p_en", f_en, b_en, p_en), ("p_multi", f_mu, b_mu, p_mu)):
        err = np.abs(f.sum(1) + b - p).max()
        print(f"  SHAP {enc} {nume}: max |suma + baza - predictie| = {err:.2e}", flush=True)
        if err > TOL_MODEL:
            raise SystemExit(f"{enc} {nume}: SHAP + baza nu reconstituie predictia ({err:.2e})")
    return dict(idx=idx, lang=lang, X=Xml, p_en=p_en, p_mu=p_mu, f_en=f_en, f_mu=f_mu,
                b_en=b_en, b_mu=b_mu)


def compose(arms, fus):
    """SHAP-ul lui A: aceeasi combinatie afina, per limba, ca make_enc_mean + fuse_ab.zA_of."""
    idx, lang = arms[0]["idx"], arms[0]["lang"]
    n, w = arms[0]["X"].shape
    A, phi, base = np.empty(n), np.empty((n, w)), np.empty(n)
    k = len(arms)
    for L in sorted(pd.unique(lang)):
        m = lang == L
        w_src = fus.loc[idx[m], "w_src"].unique()
        assert len(w_src) == 1, (L, w_src)
        w_src = float(w_src[0])
        pe = sum(zscore(a["p_en"][m]) for a in arms) / k
        pm = sum(zscore(a["p_mu"][m]) for a in arms) / k
        mix = w_src * zscore(pe) + (1 - w_src) * zscore(pm)
        A[m] = zscore(mix)
        s_pe, s_pm, s_mix = pe.std(), pm.std(), mix.std()
        lin, f, b = 0.0, 0.0, 0.0
        for a in arms:
            c_en = w_src / (k * a["p_en"][m].std() * s_pe * s_mix)
            c_mu = (1 - w_src) / (k * a["p_mu"][m].std() * s_pm * s_mix)
            lin = lin + c_en * a["p_en"][m] + c_mu * a["p_mu"][m]
            f = f + c_en * a["f_en"][m] + c_mu * a["f_mu"][m]
            b = b + c_en * a["b_en"][m] + c_mu * a["b_mu"][m]
        const = A[m] - lin                         # termenul liber al aplicatiei afine
        assert np.ptp(const) < 1e-9, (L, np.ptp(const))
        phi[m], base[m] = f, b + const.mean()
        # Fundalul e limba insasi, iar A are media 0 in limba: baza trebuie sa fie 0.
        assert np.abs(base[m]).max() < TOL_SUM, (L, np.abs(base[m]).max())
    return A, phi, base


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--blocks", default=os.path.join(tempfile.gettempdir(), "shap_signal_a_blocks"),
                    help="director pentru blocurile exportate (~100 MB pe encoder, nu in repo)")
    ap.add_argument("--plot-only", action="store_true",
                    help="redeseneaza graficul din output/shap_signal_a_adopted_raw.npz, fara recalcul")
    a = ap.parse_args()
    if a.plot_only:
        return plot(RAW)
    os.makedirs(a.blocks, exist_ok=True)

    arms = [encoder_arms(e, a.blocks) for e in ENCODERS]
    for x in arms[1:]:                             # aceleasi randuri, aceleasi coloane lexicale
        assert np.array_equal(x["idx"], arms[0]["idx"])
        assert np.allclose(x["X"][:, D:], arms[0]["X"][:, D:], equal_nan=True, rtol=0, atol=1e-6)

    fus = pd.read_csv(FUSION).set_index("idx")
    assert set(fus.index) == set(arms[0]["idx"]), "fuziunea si semnalul A nu au aceleasi randuri"
    A, phi, base = compose(arms, fus)

    # Control 2: A compus e A-ul din fuziune. Control 3: SHAP + baza reconstituie A.
    err_a = np.abs(A - fus.loc[arms[0]["idx"], "A"].values).max()
    err_s = np.abs(phi.sum(1) + base - A).max()
    print(f"control 2: max |A - A fuziune| = {err_a:.2e}\ncontrol 3: max |SHAP + baza - A| = {err_s:.2e}")
    if err_a > TOL_A or err_s > TOL_SUM:
        raise SystemExit("controalele 2/3 au picat, graficul nu se face")

    # Grupurile: embeddingul celor trei encodere insumat (valorile SHAP sunt aditive), plus cele sase
    # coloane lexicale, aceleasi la toate encoderele.
    X, lang = arms[0]["X"], arms[0]["lang"]
    G = np.column_stack([phi[:, :D].sum(1), phi[:, D:]])
    names = [EMB] + LEX
    vals = X[:, D:].astype(float).copy()
    # zipf = 0 e doar un loc gol acolo unde nu exista lista de frecvente: gri, nu "frecventa mica".
    vals[vals[:, 4] == 1, 1] = np.nan
    data = np.column_stack([np.full(len(X), np.nan), vals])

    imp = pd.DataFrame({"feature": names, "all": np.abs(G).mean(0)})
    for L in sorted(pd.unique(lang)):
        imp[L] = np.abs(G[lang == L]).mean(0)
    imp = imp.sort_values("all", ascending=False)
    imp.to_csv(os.path.join(OUT, "shap_signal_a_adopted_importance.csv"), index=False)
    np.savez(RAW, shap=G, base=base, data=data,
             names=np.asarray(names), lang=np.asarray(lang, dtype="U8"), idx=arms[0]["idx"], A=A)
    print(imp.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    plot(RAW)


def plot(raw):
    """Beeswarm-ul nativ din valorile salvate, fara recalcul. Indicatorii de disponibilitate ies din
    grafic: sunt constanti in interiorul fiecarei limbi, deci cu fundalul limbii primesc exact 0 pe
    fiecare rand (verificat aici), si ar adauga doua randuri goale."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shap
    z = np.load(raw)
    G, data, names = z["shap"], z["data"], [str(v) for v in z["names"]]
    gol = [j for j, nm in enumerate(names) if nm.endswith("(flag)")]
    assert np.abs(G[:, gol]).max() == 0, "un indicator are SHAP nenul, nu se poate scoate"
    keep = [j for j in range(len(names)) if j not in gol]
    expl = shap.Explanation(values=G[:, keep], base_values=z["base"], data=data[:, keep],
                            feature_names=[names[j] for j in keep])
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    shap.plots.beeswarm(expl, max_display=len(keep), ax=ax, show=False, plot_size=None)
    ax.set_xlabel("SHAP value (relative to the language mean)", fontsize=11)
    fig.suptitle(f"Signal A as adopted: three encoders, all 11 languages (n={len(G)})", fontsize=12)
    stem = os.path.join(OUT, "shap_signal_a_adopted")
    fig.savefig(stem + ".pdf", bbox_inches="tight")
    fig.savefig(stem + ".png", dpi=200, bbox_inches="tight")
    os.makedirs(FIG, exist_ok=True)
    shutil.copyfile(stem + ".pdf", os.path.join(FIG, "fig_shap_signal_a.pdf"))
    print(f"-> {stem}.pdf, {stem}.png, {os.path.join(FIG, 'fig_shap_signal_a.pdf')}")


if __name__ == "__main__":
    main()
