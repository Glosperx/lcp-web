"""Signal A: a regressor over a frozen multilingual encoder, evaluated leave-one-language-out.

For each target the encoder's last four layers are averaged and pooled over the target's subwords,
then centred on the mean of its language. Fertility (subword count, centred the same way) and the
lexical columns of `data.lexical` are appended. The regressor is the mean of a ridge regression and
a gradient-boosted tree.

Two arms are written for every row:
  p_en     fitted on CompLex English only, a single fit for all languages;
  p_multi  fitted on CompLex plus the other evaluation languages, refitted per held-out language.
When English is held out, CompLex is removed from training as well and p_en is set to p_multi, so
no English label is ever used to predict English.

Usage:
  python signal_a.py --encoder xlmr            # 10 MLSP languages
  python signal_a.py --encoder xlmr --with-ro  # plus RoLCP as an 11th language
Results are written to predictions/signal_a.csv, replacing earlier rows for the same setting.
"""
import argparse
import os
import time

import numpy as np
import pandas as pd

import data

# key: (Hugging Face repo, revision)
ENCODERS = {"xlmr": ("xlm-roberta-base", data.XLMR_REVISION),
            "xlmr-large": ("xlm-roberta-large", "c23d21b0620b635a76227c604d44e43a9f0ee389"),
            "labse": ("sentence-transformers/LaBSE", "836121a0533e5664b21c7aacc5d22951f2b8b25b"),
            "e5": ("intfloat/multilingual-e5-base", "d128750597153bb5987e10b1c3493a34e5a4502a")}
OUT = os.path.join(data.PRED_DIR, "signal_a.csv")


# ----------------------------------------------------------------------------- embeddings
class Encoder:
    def __init__(self, key):
        import torch
        from transformers import AutoModel, AutoTokenizer
        self.torch = torch
        self.dev = ("cuda" if torch.cuda.is_available()
                    else "mps" if torch.backends.mps.is_available() else "cpu")
        self.key = key
        repo, rev = ENCODERS[key]
        self.tok = AutoTokenizer.from_pretrained(repo, revision=rev)
        self.model = AutoModel.from_pretrained(repo, revision=rev, dtype=torch.float32)
        self.model = self.model.to(self.dev).eval()
        self.dim = self.model.config.hidden_size

    def embed(self, sents, tokens):
        """(vectors, ok). `ok` is False where the target cannot be located in its context."""
        X = np.zeros((len(sents), self.dim), np.float32)
        ok = np.zeros(len(sents), bool)
        with self.torch.no_grad():
            for i, (sent, token) in enumerate(zip(sents, tokens)):
                text = str(sent).replace("\n", " ").strip()
                span = data.find_char_span(text, str(token))
                if span is None:
                    continue
                ctx, cs, ce = data.crop_around(text, *span)
                enc = self.tok(ctx, return_offsets_mapping=True, return_tensors="pt",
                               truncation=True, max_length=512)
                tgt = [j for j, (a, b) in enumerate(enc["offset_mapping"][0].tolist())
                       if b > a and a < ce and b > cs]
                if not tgt:
                    continue
                ids = enc["input_ids"][0].to(self.dev)
                hs = self.model(ids.unsqueeze(0), output_hidden_states=True).hidden_states
                vec = self.torch.stack([hs[k][0] for k in (-4, -3, -2, -1)]).mean(0)[tgt].mean(0)
                X[i] = vec.float().cpu().numpy()
                ok[i] = True
        return X, ok


def embed_cached(enc, frame, part):
    stem = os.path.join(data.CACHE_DIR, f"emb_{enc.key}_{part}_{len(frame)}")
    if os.path.exists(stem + "_ok.npy"):             # written last, so the pair is complete
        return np.load(stem + ".npy"), np.load(stem + "_ok.npy")
    t0 = time.time()
    E, ok = enc.embed(list(frame["sent"]), list(frame["token"]))
    os.makedirs(data.CACHE_DIR, exist_ok=True)
    np.save(stem + ".npy", E)
    np.save(stem + "_ok.npy", ok)
    print(f"[A] {enc.key}: embedded {ok.sum()}/{len(frame)} {part} rows in {time.time()-t0:.0f}s",
          flush=True)
    return E, ok


# ----------------------------------------------------------------------------- regressor
def blend_ridge_hgb(Xtr, ytr, Xpred):
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    ridge = Pipeline([("i", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("s", StandardScaler()), ("r", Ridge(alpha=300, random_state=data.SEED))])
    hgb = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=400,
                                        l2_regularization=1.0, random_state=data.SEED)
    return np.mean([m.fit(Xtr, ytr).predict(Xpred) for m in (ridge, hgb)], axis=0)


def features(E, lex, fert, mu, fert_mu):
    """[embedding - language mean, fertility - language mean, lexical columns]."""
    col = (np.asarray(fert, float).reshape(-1, 1) - float(fert_mu)).astype(np.float32)
    return np.hstack([E - mu, col, lex])


def per_language(E, lex, fert, langs):
    """`features` with every language centred on its own mean."""
    X = np.zeros((len(E), E.shape[1] + 1 + lex.shape[1]), np.float32)
    for lg in pd.unique(langs):
        m = langs == lg
        X[m] = features(E[m], lex[m], fert[m], E[m].mean(0, keepdims=True), fert[m].mean())
    return X


# ----------------------------------------------------------------------------- main
def run(encoder, with_ro):
    ev = data.load_eval(with_ro)
    en = data.load_complex_en()
    lem_ev, lem_en = data.lemmas([("test", ev), ("complex_en", en.assign(lang="en"))])

    enc = Encoder(encoder)
    Een, oken = embed_cached(enc, en, "complex_en")
    Eev, okev = embed_cached(enc, ev, "eval_ro" if with_ro else "eval")
    print(f"[A] encoder {encoder} on {enc.dev} | CompLex {oken.sum()}/{len(en)} | "
          f"eval {okev.sum()}/{len(ev)}", flush=True)

    lex_en = data.lexical(list(en["token"]), ["en"] * len(en), lem_en)
    lex_ev = data.lexical(list(ev["token"]), list(ev["lang"]), lem_ev)
    fert_en = data.fertility(list(en["token"]))
    fert_ev = data.fertility(list(ev["token"]))

    yen = en["complexity"].values.astype(float)[oken]
    Xen = features(Een[oken], lex_en[oken], fert_en[oken], Een[oken].mean(0, keepdims=True),
                   fert_en[oken].mean())
    y = ev["complexity"].values.astype(float)[okev]
    lang = ev["lang"].values[okev]
    X = per_language(Eev[okev], lex_ev[okev], fert_ev[okev], lang)

    p_en_all = blend_ridge_hgb(Xen, yen, X)
    p_en, p_multi = np.empty(len(X)), np.empty(len(X))
    for L in sorted(pd.unique(lang)):
        te, tr = lang == L, lang != L
        if L == "en":
            Xtr, ytr = X[tr], y[tr]
        else:
            Xtr, ytr = np.vstack([Xen, X[tr]]), np.concatenate([yen, y[tr]])
        p_multi[te] = blend_ridge_hgb(Xtr, ytr, X[te])
        p_en[te] = p_multi[te] if L == "en" else p_en_all[te]
        print(f"  {L:4s} n={te.sum():4d}  r(p_en)={data.pearson(p_en[te], y[te]):+.4f}  "
              f"r(p_multi)={data.pearson(p_multi[te], y[te]):+.4f}", flush=True)

    new = pd.DataFrame({"setting": "mlsp+ro" if with_ro else "mlsp", "encoder": encoder,
                        "lang": lang, "idx": ev["idx"].values[okev], "p_en": p_en,
                        "p_multi": p_multi})
    # round_trip: the default parser can move the last bit of the rows that are kept
    old = pd.read_csv(OUT, float_precision="round_trip") if os.path.exists(OUT) else new.iloc[:0]
    old = old[~((old["setting"] == new["setting"][0]) & (old["encoder"] == encoder))]
    os.makedirs(data.PRED_DIR, exist_ok=True)
    out = pd.concat([old, new], ignore_index=True).sort_values(["setting", "encoder", "idx"],
                                                               kind="stable")
    out.to_csv(OUT, index=False)
    print(f"-> {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--encoder", choices=list(ENCODERS), required=True)
    ap.add_argument("--with-ro", action="store_true", help="add RoLCP as an 11th language")
    a = ap.parse_args()
    run(a.encoder, a.with_ro)
