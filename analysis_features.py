# =============================================================================
# Studiu trasaturi suplimentare (sugestiile lui Sergiu): adauga POS / dependenta /
# morfologie / entitate numita (spaCy-RO) si polisemie / sinonime / antonime /
# adancime hiperonim (RoWordNet) ceva PESTE frecventa la predictia complexitatii?
#
# Metodologie = aceeasi ca la rarity (sect F) si ET (sect D): CONTRIBUTIE UNICA
# controlata pe frecventa+lungime. Lipsa etichete RO (doar 14, zgomot) => proxy de adevar =
# predictia best (output/exp_lemmafreq.csv, public 68.90, r~0.78). Pt fiecare trasatura:
#   corr_raw           = corr(trasatura, best)
#   corr_ctrl_freqlen  = corr(resid(trasatura|zipf,len), resid(best|zipf,len)) = unic peste frecventa
# Daca corr_ctrl ~ 0 => redundant cu frecventa (confirma SHAP: frecventa domina).
#
# NU atinge solutia. Doar citeste, scrie output/extra_features/ + cache data/extra_features_test.csv.
# Ruleaza CPU (spaCy ro_core_news_sm + rowordnet), fara GPU/LLM.
# =============================================================================
import os
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from solution_bert import find_input, DATA, HERE, normalize_token, find_char_span, crop_around
from analysis_et import residual, pr

OUT = os.path.join(HERE, "output", "extra_features")
os.makedirs(OUT, exist_ok=True)
CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}


# ----------------------------------------------------------------------------- spaCy (POS/dep/morph/NER)
def spacy_features(texts, tokens):
    import spacy
    nlp = spacy.load("ro_core_news_sm", disable=["lemmatizer"])
    ctxs, offs = [], []
    for text, token in zip(texts, tokens):
        text = str(text).replace("\n", " ").strip()
        span = find_char_span(text, str(token))
        if span is None:
            ctxs.append(str(token).strip()); offs.append(None)
        else:
            ctx, cs, ce = crop_around(text, span[0], span[1])
            ctxs.append(ctx); offs.append((cs, ce))
    rows = []
    for doc, off in zip(nlp.pipe(ctxs, batch_size=64), offs):
        t = None
        if off is not None:
            sp = doc.char_span(off[0], off[1], alignment_mode="expand")
            if sp is not None and len(sp):
                t = sp.root
        if t is None:                          # fallback: primul token de continut, altfel primul
            cand = [w for w in doc if w.pos_ in CONTENT_POS]
            t = (cand or list(doc) or [None])[0]
        if t is None:
            rows.append(dict(pos="X", is_content=0, is_noun=0, is_verb=0, is_adj=0, is_adv=0,
                             is_propn=0, dep="", n_morph=0, is_entity=0, ent_type=""))
            continue
        pos = t.pos_
        rows.append(dict(pos=pos, is_content=int(pos in CONTENT_POS), is_noun=int(pos == "NOUN"),
                         is_verb=int(pos == "VERB"), is_adj=int(pos == "ADJ"), is_adv=int(pos == "ADV"),
                         is_propn=int(pos == "PROPN"), dep=t.dep_, n_morph=len(t.morph),
                         is_entity=int(bool(t.ent_type_)), ent_type=t.ent_type_))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- RoWordNet (semantic, pe lema)
def wordnet_features(lemmas):
    import rowordnet
    wn = rowordnet.RoWordNet()

    def syns(lit):
        for cand in (lit, lit.lower(), lit.capitalize()):
            try:
                ids = wn.synsets(literal=cand)
            except Exception:
                ids = []
            if ids:
                return ids
        return []

    def hyper_depth(sid, cap=20):
        d = 0; cur = sid; seen = set()
        while d < cap:
            try:
                ups = [tgt for (tgt, rel) in wn.outbound_relations(cur) if "hypernym" in rel]
            except Exception:
                break
            ups = [u for u in ups if u not in seen]
            if not ups:
                break
            seen.add(cur); cur = ups[0]; d += 1
        return d

    rows = []
    for lem in lemmas:
        l = normalize_token(lem)
        ids = syns(l) if l else []
        synset_words, n_ant = set(), 0
        for sid in ids:
            try:
                s = wn.synset(sid)
                synset_words.update(x.replace("_", " ") for x in s.literals)
                for (_, rel) in wn.outbound_relations(sid):
                    if "antonym" in rel:
                        n_ant += 1
            except Exception:
                pass
        rows.append(dict(polysemy=len(ids), in_wordnet=int(bool(ids)),
                         n_synonyms=max(len(synset_words) - 1, 0), n_antonyms=n_ant,
                         hyper_depth=hyper_depth(ids[0]) if ids else 0))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- evaluare contributie unica
def evaluate(feat_df, proxy, ctrl, names):
    """corr_raw + corr_ctrl_freqlen (resid pe zipf+len) pt fiecare trasatura numerica."""
    proxy_res = residual(proxy, ctrl)
    rows = []
    for nm in names:
        f = feat_df[nm].astype(float).values
        raw, n = pr(f, proxy)
        try:
            f_res = residual(f, ctrl)
            ctrl_r, _ = pr(f_res, proxy_res)
        except Exception:
            ctrl_r = np.nan
        rows.append({"feature": nm, "corr_raw_vs_best": round(raw, 4),
                     "corr_ctrl_freqlen": round(ctrl_r, 4), "n": n,
                     "verdict": "redundant" if abs(ctrl_r) < 0.10 else "candidate"})
    return pd.DataFrame(rows)


def main():
    test = pd.read_csv(find_input(["test_data.csv", "test_set.csv"]))
    X = pd.read_csv(os.path.join(DATA, "X_test.csv"))[["datapointID", "zipf_best", "word_length"]]
    best = pd.read_csv(os.path.join(HERE, "output", "exp_lemmafreq.csv"))[["datapointID", "answer"]]
    df = test.merge(X, on="datapointID").merge(best, on="datapointID")
    print(f"[date] test={len(df)} | proxy=exp_lemmafreq (68.90)")

    cache = os.path.join(DATA, "extra_features_test.csv")
    if os.path.exists(cache):
        feat = pd.read_csv(cache)
        print(f"[cache] {cache}")
    else:
        print("[spaCy] extragere POS/dep/morph/NER ...")
        sf = spacy_features(list(df["text"]), list(df["token"]))
        print("[RoWordNet] extragere polisemie/sinonime/antonime/adancime ...")
        wf = wordnet_features(list(df["lemma"]))
        feat = pd.concat([df[["datapointID"]].reset_index(drop=True), sf, wf], axis=1)
        feat.to_csv(cache, index=False)
        print(f"[cache scris] {cache}")
    df = df.merge(feat, on="datapointID")

    ctrl = df[["zipf_best", "word_length"]].values
    proxy = df["answer"].values
    NUM = ["is_content", "is_noun", "is_verb", "is_adj", "is_adv", "is_propn", "n_morph",
           "is_entity", "polysemy", "in_wordnet", "n_synonyms", "n_antonyms", "hyper_depth"]
    ev = evaluate(df, proxy, ctrl, NUM)
    ev.to_csv(os.path.join(OUT, "feature_eval.csv"), index=False)

    # distributii informative
    pos_tab = df.groupby("pos")["answer"].agg(["mean", "count"]).sort_values("mean", ascending=False)
    ent_cov = df["is_entity"].mean(); wn_cov = df["in_wordnet"].mean()

    print("\n=== Contributie unica peste frecventa+lungime (proxy = best 68.90) ===")
    print(ev.to_string(index=False))
    print(f"\nAcoperire: entitate numita {100*ent_cov:.1f}% din test | in RoWordNet {100*wn_cov:.1f}%")
    print("\nComplexitate medie (proxy) pe clasa POS:")
    print(pos_tab.to_string())

    with open(os.path.join(OUT, "summary.md"), "w", encoding="utf-8") as f:
        f.write("# Trasaturi suplimentare — contributie unica peste frecventa (cifre; proza = om)\n\n")
        f.write(f"proxy = exp_lemmafreq (public 68.90, r~0.78); n={len(df)}; control = zipf_best + word_length\n\n")
        try:
            f.write(ev.to_markdown(index=False) + "\n\n")
            f.write("## Complexitate medie (proxy) pe POS\n" + pos_tab.to_markdown() + "\n\n")
        except Exception:
            f.write("```\n" + ev.to_string(index=False) + "\n```\n\n")
            f.write("## POS\n```\n" + pos_tab.to_string() + "\n```\n\n")
        f.write(f"acoperire entitate numita {100*ent_cov:.1f}%; in RoWordNet {100*wn_cov:.1f}%\n")
    print(f"\nArtefacte -> {OUT} (feature_eval.csv, summary.md)")


if __name__ == "__main__":
    main()
