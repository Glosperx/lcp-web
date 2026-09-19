# =============================================================================
# Fine-tune XLM-R cap-la-cap pentru complexitate lexicala (vs embedding INGHETAT + Ridge/HGB).
# Schimbare de ARHITECTURA: encoder antrenabil + cap de regresie, pool pe subword-urile tinta, MSE.
#
#   --gate    : 1 config -> train EN -> test MLSP (+ invers), transfer_avg vs frozen 0.5512.
#   --sweep   : grila de configs (lr x epoci x freeze x base/large), fiecare evaluat pe transfer EN->MLSP.
#               Logheaza progresiv in data/finetune_sweep.csv, SARE configs deja facute (rezumabil ore).
#   --final   : config dat, ensemble multi-seed pe EN+MLSP -> prezice RO test -> data/finetune_test.csv.
#
# Separat de solution_bert.py (NU atinge best-ul bit-exact 64.81). GPU. transformers==4.46.3.
# =============================================================================
import os
import sys
import glob
import time
import argparse
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)
from solution_bert import (normalize_token, find_char_span, crop_around, SEED, EMB_CONFIGS,
                           REGRESSORS, regressor_kind)


def _emb_tf_kind(v):
    """Valideaza `--emb-tf`. Multimea fixa plus familia `proj-N`, care nu se poate enumera."""
    import argparse as _ap
    if v in ("nu", "pca1", "pca5", "zca"):
        return v
    if v.startswith("proj-") and v[5:].isdigit() and int(v[5:]) > 0:
        return v
    raise _ap.ArgumentTypeError(f"{v!r}: asteptat nu|pca1|pca5|zca|proj-<N>")

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODELS = {"base": "xlm-roberta-base", "large": "xlm-roberta-large"}


def set_seed(s):
    torch.manual_seed(s); np.random.seed(s)
    if DEVICE == "cuda":
        torch.cuda.manual_seed_all(s)


# ----------------------------------------------------------------------------- date brute (local)
def load_complex_en():
    """CompLex EN. Descarca daca lipseste (A.0): varianta veche doar citea, deci --frozenmulti crapa
    cu FileNotFoundError pe orice masina fara data/complex_en/."""
    from mlsp_common import ensure_complex_en
    return ensure_complex_en()


def load_mlsp(split="test", include_ro=False):
    """MLSP pe cele 10 limbi (11 cu `include_ro`), din data/mlsp_full/ (A.1 + A.2).

    Varianta veche deriva limba din numele fisierului cu split("_")[0], ceea ce pe fisierele care
    exista azi da "multils" pentru toate zece: bucla de holdout ar sari toate limbile si ar scrie
    tacut un CSV gol. Limba vine acum din coloana `language`, cu eroare la nemapare.

    `include_ro`, implicit False: adauga RoLCP ca a 11-a limba, prin `mlsp_common.load_rolcp()`."""
    from mlsp_common import load_mlsp as _load
    return _load(split, include_ro=include_ro)


# ----------------------------------------------------------------------------- dataset
class WordReg(Dataset):
    def __init__(self, df, tok, has_label=True, max_len=256):
        self.rows = df.reset_index(drop=True); self.tok = tok
        self.has_label = has_label; self.max_len = max_len

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, i):
        r = self.rows.iloc[i]
        text = str(r["sent"]).replace("\n", " ").strip()
        span = find_char_span(text, str(r["token"]))
        if span is None:
            text2 = normalize_token(r["token"]); span = (0, len(text2)); text = text2 or text
        ctx, cs, ce = crop_around(text, span[0], span[1])
        enc = self.tok(ctx, return_offsets_mapping=True, truncation=True, max_length=self.max_len)
        offs = enc["offset_mapping"]
        tgt = [j for j, (a, b) in enumerate(offs) if b > a and a < ce and b > cs] or [0]
        mask = np.zeros(len(enc["input_ids"]), np.float32)
        for j in tgt:
            mask[j] = 1.0
        item = {"input_ids": enc["input_ids"], "attention_mask": enc["attention_mask"], "tmask": mask}
        if self.has_label:
            item["label"] = float(r["complexity"])
        return item


def collate(batch):
    maxlen = max(len(b["input_ids"]) for b in batch)
    ids = torch.zeros(len(batch), maxlen, dtype=torch.long)
    am = torch.zeros(len(batch), maxlen, dtype=torch.long)
    tm = torch.zeros(len(batch), maxlen, dtype=torch.float)
    for i, b in enumerate(batch):
        n = len(b["input_ids"])
        ids[i, :n] = torch.tensor(b["input_ids"]); am[i, :n] = torch.tensor(b["attention_mask"])
        tm[i, :n] = torch.tensor(b["tmask"])
    out = {"input_ids": ids, "attention_mask": am, "tmask": tm}
    if "label" in batch[0]:
        out["label"] = torch.tensor([b["label"] for b in batch], dtype=torch.float)
    return out


# ----------------------------------------------------------------------------- model
class XLMRRegressor(nn.Module):
    def __init__(self, model_name, freeze=0, grad_ckpt=False, lora=0):
        super().__init__()
        self.enc = AutoModel.from_pretrained(model_name)
        h = self.enc.config.hidden_size                  # capteaza inainte de wrap LoRA
        if grad_ckpt:
            self.enc.gradient_checkpointing_enable()
        if lora > 0:                         # adaptere LoRA pe atentie; baza inghetata (capacitate minima)
            from peft import LoraConfig, get_peft_model
            lc = LoraConfig(r=lora, lora_alpha=2 * lora, target_modules=["query", "value"],
                            lora_dropout=0.1, bias="none")
            self.enc = get_peft_model(self.enc, lc)
        elif freeze > 0:                     # ingheata embeddings + primele `freeze` layere (mai putin overfit)
            for p in self.enc.embeddings.parameters():
                p.requires_grad = False
            for lay in self.enc.encoder.layer[:freeze]:
                for p in lay.parameters():
                    p.requires_grad = False
        self.head = nn.Sequential(nn.Dropout(0.1), nn.Linear(h, 1))

    def forward(self, input_ids, attention_mask, tmask):
        out = self.enc(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        pooled = (out * tmask.unsqueeze(-1)).sum(1) / tmask.sum(1, keepdim=True).clamp(min=1.0)
        return torch.sigmoid(self.head(pooled)).squeeze(-1)


def train(df, tok, cfg, seed=SEED, verbose=True):
    set_seed(seed)
    big = cfg["model"] == "large"
    bs = cfg.get("bs", 4 if big else 16)
    accum = cfg.get("accum", 2 if big else 1)        # acumulare gradient => batch efectiv = bs*accum
    max_len = cfg.get("max_len", 192 if big else 256)
    model = XLMRRegressor(MODELS[cfg["model"]], freeze=cfg.get("freeze", 0), grad_ckpt=big,
                          lora=cfg.get("lora", 0)).to(DEVICE)
    dl = DataLoader(WordReg(df, tok, max_len=max_len), batch_size=bs, shuffle=True, collate_fn=collate)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=cfg["lr"], weight_decay=0.01)
    lossf = nn.MSELoss()
    scaler = torch.cuda.amp.GradScaler(enabled=DEVICE == "cuda")
    model.train()
    for ep in range(cfg["epochs"]):
        tot = 0.0; opt.zero_grad()
        for i, b in enumerate(dl):
            with torch.cuda.amp.autocast(enabled=DEVICE == "cuda"):
                pred = model(b["input_ids"].to(DEVICE), b["attention_mask"].to(DEVICE), b["tmask"].to(DEVICE))
                loss = lossf(pred, b["label"].to(DEVICE)) / accum
            scaler.scale(loss).backward()
            if (i + 1) % accum == 0:
                scaler.step(opt); scaler.update(); opt.zero_grad()
            tot += loss.item() * accum * len(b["label"])
        if verbose:
            print(f"    epoca {ep+1}/{cfg['epochs']} MSE={tot/len(df):.5f}", flush=True)
    return model, max_len


@torch.no_grad()
def predict(model, df, tok, bs=32, max_len=256):
    model.eval()
    dl = DataLoader(WordReg(df, tok, has_label=False, max_len=max_len), batch_size=bs,
                    shuffle=False, collate_fn=collate)
    out = []
    for b in dl:
        with torch.cuda.amp.autocast(enabled=DEVICE == "cuda"):
            p = model(b["input_ids"].to(DEVICE), b["attention_mask"].to(DEVICE), b["tmask"].to(DEVICE))
        out.append(p.float().cpu().numpy())
    return np.concatenate(out)


def pearson(a, b):
    from scipy.stats import pearsonr
    return float(pearsonr(np.asarray(a, float), np.asarray(b, float))[0])


def _cfg_key(c):
    base = f"{c['model']}_lr{c['lr']}_ep{c['epochs']}"
    return base + (f"_lora{c['lora']}" if c.get("lora", 0) else f"_fz{c.get('freeze',0)}")


# ----------------------------------------------------------------------------- sweep (rezumabil, ore)
SWEEP_GRID = (
    [{"model": "base", "lr": lr, "epochs": ep, "freeze": fz}
     for lr in (1e-5, 2e-5, 3e-5) for ep in (3, 5) for fz in (0, 6)] +
    [{"model": "large", "lr": lr, "epochs": 3, "freeze": fz} for lr in (1e-5, 2e-5) for fz in (0, 12)]
)
# LoRA: capacitate minima (rang mic), baza inghetata -> ar trebui sa pastreze alinierea multilinguala.
LORA_GRID = [{"model": "base", "lr": lr, "epochs": ep, "lora": r}
             for r in (4, 8, 16) for lr in (1e-4, 2e-4) for ep in (3,)]


def run_sweep(en, ml, tok, grid, path, epochs_override=None):
    done = set()
    if os.path.exists(path):
        d = pd.read_csv(path)
        done = set(d[d["transfer_en2ml"].notna()]["cfg"].tolist())   # retry NaN (OOM vechi)
    yml = ml["complexity"].values.astype(float)
    for c in grid:
        if epochs_override:
            c = {**c, "epochs": epochs_override}
        key = _cfg_key(c)
        if key in done:
            print(f"[sweep] {key} deja facut, sar"); continue
        t0 = time.time()
        print(f"[sweep] {key} : fine-tune EN ({len(en)}) -> test MLSP ...", flush=True)
        try:
            m, mlen = train(en, tok, c, verbose=False)
            r = pearson(predict(m, ml, tok, max_len=mlen), yml)
            del m; torch.cuda.empty_cache()
        except Exception as ex:
            print(f"  EROARE {key}: {ex}"); r = float("nan"); torch.cuda.empty_cache()
        dt = time.time() - t0
        row = {"cfg": key, "model": c["model"], "lr": c["lr"], "epochs": c["epochs"],
               "freeze": c.get("freeze", 0), "lora": c.get("lora", 0),
               "transfer_en2ml": round(r, 4), "sec": int(dt)}
        pd.DataFrame([row]).to_csv(path, mode="a", header=not os.path.exists(path), index=False)
        print(f"  -> transfer_en2ml={r:.4f}  ({int(dt)}s).  Frozen baseline 0.5148.", flush=True)
    print(f"\n[sweep] gata. Rezultate in {path}")
    res = (pd.read_csv(path).drop_duplicates("cfg", keep="last")
           .sort_values("transfer_en2ml", ascending=False))
    print(res.to_string(index=False))


def multilingual_gate(en, ml, tok, cfg, holdout=("it", "pt", "es")):
    """Testul tezei MULTILINGUAL: ajuta antrenarea pe EN+romanic (vs EN-only) transferul la o limba
    romanica NEVAZUTA? Pt fiecare limba L: train EN-only vs train EN+MLSP(fara L), test pe L."""
    print(f"Limbi MLSP: {sorted(ml['lang'].unique())}")
    rows = []
    for L in holdout:
        test = ml[ml["lang"] == L]
        rest = ml[ml["lang"] != L]
        if len(test) < 20:
            print(f"  {L}: prea putine ({len(test)}), sar"); continue
        yL = test["complexity"].values.astype(float)
        m1, l1 = train(en, tok, cfg, verbose=False)
        r_en = pearson(predict(m1, test, tok, max_len=l1), yL); del m1; torch.cuda.empty_cache()
        m2, l2 = train(pd.concat([en, rest], ignore_index=True), tok, cfg, verbose=False)
        r_multi = pearson(predict(m2, test, tok, max_len=l2), yL); del m2; torch.cuda.empty_cache()
        print(f"  held-out {L} (n={len(test)}): EN-only {r_en:.4f} | EN+romanic {r_multi:.4f} "
              f"(delta {r_multi-r_en:+.4f})", flush=True)
        rows.append({"holdout": L, "n": len(test), "lora": cfg.get("lora", 0),
                     "r_en_only": round(r_en, 4), "r_multilingual": round(r_multi, 4),
                     "delta": round(r_multi - r_en, 4)})
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "finetune_multi.csv"), index=False)
    print(f"\n-> data/finetune_multi.csv. Referinta frozen EN->ML 0.5148. "
          f"Intrebare: ajuta multilingual peste EN-only? bate frozen-ul?")


# Setul de trasaturi al semnalului A, ca (foloseste fertilitatea, anuleaza lungimea). `baza` e cel
# publicat. Inlocuirea lungimii cu numarul de subword-uri e o decizie de design, argumentata din
# numaratoarea de caractere (3.59 pe ja fata de 8.78 pe it, zero etichete implicate), nu un
# hiperparametru potrivit pe scor.
AFEATS = {"baza": (False, False), "fara_lung": (False, True),
          "fert_inloc": (True, True), "fert_plus": (True, False)}


def emb_transform(kind, blocks):
    """Transformari de IZOTROPIE pe spatiul de embedding, potrivite pe reuniunea blocurilor.

    De ce global si nu per limba: literatura de anizotropie scoate componentele dominante ale
    SPATIULUI intreg (Ethayarajh 2019; Timkey si van Schijndel 2021), iar centrarea pe media limbii,
    care e metoda 1 din Libovicky et al. 2020, se face oricum dupa, in `_Xc`. Cele doua sunt pasi
    diferiti si nu se inlocuiesc unul pe altul.

    Avertisment de transfer, scris fiindca e usor de citat gresit: cifrele din acea literatura sunt
    despre similaritate COSINUS. Aici vectorii intra ca sute de coloane in Ridge si HGB, deci
    motivul pentru care o rotatie ar putea conta e altul: Ridge penalizeaza in baza data, iar HGB
    taie pe axe.

      pca1 / pca5   scade proiectia pe primele 1 sau 5 componente principale
      zca           albire completa, adica decorelare plus scalare la varianta unu
    Nicio eticheta nu intra: se folosesc doar embedding-urile.
    """
    if kind == "nu":
        return blocks
    X = np.vstack(blocks).astype(np.float64)
    mu = X.mean(0, keepdims=True)
    Xc = X - mu
    C = (Xc.T @ Xc) / max(len(Xc) - 1, 1)
    w, V = np.linalg.eigh(C)
    order = np.argsort(w)[::-1]
    w, V = w[order], V[:, order]
    if kind.startswith("proj-"):
        # REDUCE latimea, nu doar scade componente: proiecteaza pe primele k componente si se
        # opreste acolo. E singurul `kind` care intoarce blocuri mai INGUSTE decat cele primite,
        # iar apelantul trebuie sa stie asta (vezi comentariul de la locul de scriere inapoi).
        k = int(kind.split("-", 1)[1])
        if not 0 < k <= X.shape[1]:
            raise ValueError(f"{kind}: k trebuie in 1..{X.shape[1]}")
        P = V[:, :k]
        f = lambda B: (B - mu) @ P
        print(f"[E1t] emb-tf {kind}: varianta pastrata {w[:k].sum()/w.sum():.1%}, "
              f"latime {X.shape[1]} -> {k}", flush=True)
    elif kind in ("pca1", "pca5"):
        k = 1 if kind == "pca1" else 5
        P = V[:, :k]
        f = lambda B: (B - mu) - ((B - mu) @ P) @ P.T + mu
        print(f"[E1t] emb-tf {kind}: varianta scoasa {w[:k].sum()/w.sum():.1%}", flush=True)
    elif kind == "zca":
        W = V @ np.diag(1.0 / np.sqrt(np.maximum(w, 1e-8))) @ V.T
        f = lambda B: (B - mu) @ W
        print(f"[E1t] emb-tf zca: cond {w[0]/max(w[-1],1e-12):.2e}", flush=True)
    else:
        raise ValueError(kind)
    return [f(B.astype(np.float64)).astype(np.float32) for B in blocks]


def _center_per_lang(E, lex, langs, fert=None, drop_len=False):
    """_Xc pe blocuri: FIECARE limba centrata pe media EI (C.2).

    Varianta veche dadea o singura medie pentru tot MLSP∖L, deci doar testul era centrat per limba,
    iar antrenarea amesteca deplasarile de limba intr-un singur centru.

    `fert` se centreaza pe media ACELUIASI bloc de limba ca embeddingul, nu pe media globala: e o
    trasatura de tip lungime, deci deplasarea intre limbi e exact ce trebuie scos din ea."""
    from solution_bert import _Xc
    X = None
    for lg in pd.unique(langs):
        m = (langs == lg)
        blk = _Xc(E[m], lex[m], E[m].mean(0, keepdims=True),
                  fert=None if fert is None else fert[m],
                  fert_mu=None if fert is None else float(fert[m].mean()),
                  drop_len=drop_len)
        if X is None:
            X = np.zeros((len(E), blk.shape[1]), np.float32)
        X[m] = blk
    return X


def _boot_delta(y, p_en, p_multi, groups, n_boot=1000, seed=SEED):
    """CI si sigma pentru Δ, prin reesantionarea CONTEXTELOR, nu a itemilor (C.2).

    Sapte limbi din zece au in medie 3 tinte per context, iar fil/pt/si au practic una. Un bootstrap
    pe itemi ar da CI-uri prea inguste la primul grup si corecte la al doilea, adica ar denatura exact
    comparatia intre limbi care e obiectul lucrarii.

    Aceeasi reesantionare se aplica ambelor brate, deci intervalul lui Δ e PERECHE: zgomotul comun al
    esantionului se anuleaza. Nu cere nicio refitare, doar recalcularea lui r pe predictiile facute."""
    rng = np.random.default_rng(seed)
    codes = pd.factorize(groups)[0]
    idx_by_g = [np.flatnonzero(codes == k) for k in range(codes.max() + 1)]
    G = len(idx_by_g)
    d, re_, rm_ = [], [], []
    for _ in range(n_boot):
        sel = np.concatenate([idx_by_g[k] for k in rng.integers(0, G, G)])
        if np.unique(y[sel]).size < 2:
            continue
        a = pearson(p_en[sel], y[sel]); b = pearson(p_multi[sel], y[sel])
        re_.append(a); rm_.append(b); d.append(b - a)
    d = np.asarray(d)
    return dict(delta_lo=float(np.percentile(d, 2.5)), delta_hi=float(np.percentile(d, 97.5)),
                sigma_delta=float(d.std(ddof=1)), n_boot_ok=len(d),
                r_en_lo=float(np.percentile(re_, 2.5)), r_en_hi=float(np.percentile(re_, 97.5)),
                r_multi_lo=float(np.percentile(rm_, 2.5)), r_multi_hi=float(np.percentile(rm_, 97.5)))


def frozen_multi_gate(en, ml, holdout=None, emb_cfg="last4", encoder="xlmr", n_boot=1000,
                      lemma_freq=False, afeat="baza", regressor="blend",
                      out=os.path.join(HERE, "output", "e1_lolo_frozen.csv")):
    """E1: Δ_frozen(L) = r(EN+MLSP∖L → L) − r(EN-only → L), pe toate cele 10 limbi.

    Trei diferente fata de varianta veche, toate necesare ca sa produca un Δ, nu un r:
      1. holdout pe toate cele 10 limbi, nu doar ("it","pt","es");
      2. embedding prin `_embed_cached`, nu `embed_frame` direct, deci rularile urmatoare sunt aproape
         instantanee;
      3. al doilea brat, antrenat DOAR pe EN, care da termenul de scazut.

    Bratul EN-only se potriveste O SINGURA DATA si prezice toate limbile deodata: modelul nu depinde de
    L, doar partitia de test depinde. 11 potriviri in loc de 20, cifre identice.
    """
    from solution_bert import (XLMR, lexical as slex, _Xc, _embed_cached, fertility,
                               _make_regressor)
    reg = _make_regressor(regressor)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()
    xr = XLMR(emb_cfg, encoder)
    print(f"[E1] device={xr.dev} encoder={encoder} cfg={emb_cfg} dim={xr.dim} reg={regressor}",
          flush=True)

    Een, oken = _embed_cached(xr, list(en["sent"]), list(en["token"]), "en")
    Em, okm = _embed_cached(xr, list(ml["sent"]), list(ml["token"]), "mlsp10")
    print(f"[E1] embedding gata in {time.time()-t0:.0f}s | EN {oken.sum()}/{len(en)} "
          f"MLSP {okm.sum()}/{len(ml)}", flush=True)

    # na_policy="mlsp": garda de frecventa pe sinhaleza (A.3) + NaN pe suprafata la ja/si (A.4).
    kw_en, kw_ml = {}, {}
    if lemma_freq:
        from lemmatize_mlsp import lemma_array
        kw_en = dict(lemmas=lemma_array(list(en["sent"]), list(en["token"]), "complex_en", "en"))
        kw_ml = dict(lemmas=lemma_array(list(ml["sent"]), list(ml["token"]), "test", list(ml["lang"])))
    lex_en = slex(list(en["token"]), ["en"] * len(en), na_policy="mlsp", **kw_en)
    lex_ml = slex(list(ml["token"]), list(ml["lang"]), na_policy="mlsp", **kw_ml)
    use_fert, drop_len = AFEATS[afeat]
    fert_en = fertility(list(en["token"])) if use_fert else None
    fert_ml = fertility(list(ml["token"])) if use_fert else None
    yen = en["complexity"].values.astype(float)[oken]
    Xen = _Xc(Een[oken], lex_en[oken], Een[oken].mean(0, keepdims=True),
              fert=None if fert_en is None else fert_en[oken],
              fert_mu=None if fert_en is None else float(fert_en[oken].mean()),
              drop_len=drop_len)

    y = ml["complexity"].values.astype(float)[okm]
    lang = ml["lang"].values[okm]
    ctx = ml["context_id"].values[okm]
    Xml = _center_per_lang(Em[okm], lex_ml[okm], lang,
                           fert=None if fert_ml is None else fert_ml[okm], drop_len=drop_len)

    p_en_all = blend_ridge_hgb(Xen, yen, Xml)          # bratul EN-only, o singura potrivire
    print(f"[E1] brat EN-only potrivit ({time.time()-t0:.0f}s)", flush=True)

    rows = []
    for L in (holdout or sorted(pd.unique(lang))):
        te = (lang == L); tr = ~te
        Xtr = np.vstack([Xen, Xml[tr]]); ytr = np.concatenate([yen, y[tr]])
        p_multi = reg(Xtr, ytr, Xml[te])
        r_en = pearson(p_en_all[te], y[te]); r_multi = pearson(p_multi, y[te])
        b = _boot_delta(y[te], p_en_all[te], p_multi, ctx[te], n_boot=n_boot)
        rows.append({"lang": L, "n": int(te.sum()), "n_contexte": int(pd.unique(ctx[te]).size),
                     "r_en_only": round(r_en, 4), "r_multi": round(r_multi, 4),
                     "delta": round(r_multi - r_en, 4),
                     "delta_lo": round(b["delta_lo"], 4), "delta_hi": round(b["delta_hi"], 4),
                     "sigma_delta": round(b["sigma_delta"], 4),
                     "r_en_lo": round(b["r_en_lo"], 4), "r_en_hi": round(b["r_en_hi"], 4),
                     "r_multi_lo": round(b["r_multi_lo"], 4), "r_multi_hi": round(b["r_multi_hi"], 4)})
        pd.DataFrame(rows).to_csv(out, index=False)     # scris dupa FIECARE limba, nu la final
        print(f"  {L:4s} n={te.sum():4d} ctx={pd.unique(ctx[te]).size:4d} | EN-only {r_en:+.4f} | "
              f"+MLSP∖L {r_multi:+.4f} | Δ {r_multi-r_en:+.4f} "
              f"[{b['delta_lo']:+.4f},{b['delta_hi']:+.4f}] σ={b['sigma_delta']:.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)

    d = pd.DataFrame(rows)
    print(f"\n-> {out}")
    print(f"[E1] Δ mediu {d['delta'].mean():+.4f} | σ intre limbi {d['delta'].std(ddof=1):.4f} | "
          f"σ_Δ mediu in interiorul limbii {d['sigma_delta'].mean():.4f} | "
          f"limbi cu Δ>0: {(d['delta'] > 0).sum()}/{len(d)}")
    return d


def _freq_drop(X, dim_emb, p, seed):
    """Copie a lui X cu coloana de frecventa ANULATA pe o fractiune `p` din randuri.

    De ce exista, si nu e o intuitie: ablatia `--no-freq`, care anuleaza coloana peste tot, costa
    -0.0051 pe fuziune si strica patru limbi, DAR urca filipineza cu +0.0225 (CI exclude zero) si
    bratul A al sinhalezei cu +0.0243. Deci cele doua capete, p = 0 si p = 1, sunt masurate si au
    semne opuse. Intre ele exista un interior neexplorat.

    Mecanismul pe care il ataca, masurat pe 23 august in `output/e_al3lea_semnal.md` §5: modelul
    invata sa depinda de frecventa de la limbile care O AU, iar sinhaleza (100% tinte fara zipf) si
    filipineza (26.7%) platesc. Pe randurile filipineze cu zipf 0 fuziunea da +0.2320 fata de +0.4642
    pe restul. Anularea aleatoare in ANTRENARE il impiedica sa se co-adapteze pe o trasatura pe care
    un sfert din itemi n-o pot furniza, fara s-o piarda de tot ca la `--no-freq`.

    Se aplica NUMAI blocurilor de antrenare. Blocurile prezise raman neatinse: dropout-ul e o
    proprietate a potrivirii, nu a datelor.

    `dim_emb + 1` e indexul lui zipf: `_Xc` intoarce [embedding centrat] ++ [slot de fertilitate] ++
    [lexical], iar `lexical` are zipf pe coloana 0. `drop_len` scoate `lex[:, 1]`, deci nu muta zipf.

    La `p = 0` intoarce chiar obiectul primit, fara copie, deci calea de pana acum e bit-exact
    neatinsa si controlul de reproducere are ce verifica.
    """
    if p <= 0.0:
        return X
    X = X.copy()
    m = np.random.default_rng(seed).random(len(X)) < p
    X[m, dim_emb + 1] = 0.0
    return X


def frozen_trial_gap(en, ml, mlt, holdout=None, emb_cfg="last4", encoder="xlmr", n_boot=2000,
                     lemma_freq=False, afeat="baza", no_freq=False, emb_tf="nu", oov=False,
                     freq_drop=0.0, ctx_div=None, regressor="blend", export_blocks=None,
                     out=os.path.join(HERE, "output", "e1_frozen_trial.csv"),
                     preds=os.path.join(HERE, "output", "e1_frozen_preds.csv"),
                     report=os.path.join(HERE, "output", "e1_trial_gap.md"),
                     ref=os.path.join(HERE, "output", "e1_lolo_frozen.csv")):
    """Decalajul TRIAL fata de TEST pe acelasi brat inghetat, plus predictiile per instanta.

    De ce exista: tot ce s-a masurat la bake-off e pe trial, n = 30 per limba, iar bara publicata e pe
    test, n intre 445 si 600. Fara decalajul masurat pe acelasi model si aceeasi partitie, nicio cifra
    de trial nu se poate pune langa 0.657.

    Bratul e IDENTIC cu al lui `frozen_multi_gate`: EN plus MLSP-test fara limba L. Se schimba doar ce
    prezice, deci decalajul care iese e al splitului, nu al modelului. Trial-ul lui L n-a fost niciodata
    in antrenare, deci proprietatea zero-label ramane intacta.

    Al doilea lucru pe care-l produce, la fel de important: `e1_frozen_preds.csv`, semnalul A per
    instanta pentru AMBELE splituri. `frozen_multi_gate` scrie doar zece linii de r, deci fuziunea
    A plus B nu avea cu ce sa se faca.

    Centrarea blocului de trial se face in DOUA feluri, fiindca e gratis si separa doua cauze:
      selfmu = media propriului bloc de 30, adica ce s-ar face la desfasurare pe 30 de itemi;
      testmu = media blocului de test al aceleiasi limbi, deci fara zgomotul de centrare pe 30.
    Daca cele doua difera mult, o parte din decalaj vine din centrare, nu din split.

    Poarta: `r_test_multi` trebuie sa reproduca `r_multi` din `e1_lolo_frozen.csv`. Fitul e determinist
    (`random_state=SEED` in `blend_ridge_hgb`), deci orice diferenta inseamna ca bratul nu mai e acelasi
    si nu se scrie nicio cifra.
    """
    from solution_bert import (XLMR, lexical as slex, _Xc, _embed_cached, fertility,
                               _make_regressor)
    reg = _make_regressor(regressor)
    from mlsp_common import boot_r_ci
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()

    ref_r = {}
    if os.path.exists(ref):
        d = pd.read_csv(ref)
        ref_r = dict(zip(d["lang"].astype(str), d["r_multi"].astype(float)))
        print(f"[E1t] referinta: {len(ref_r)} limbi din {os.path.basename(ref)}", flush=True)
    else:
        print(f"[E1t] ATENTIE: {ref} lipseste, poarta de reproducere nu se poate aplica", flush=True)

    xr = XLMR(emb_cfg, encoder)
    print(f"[E1t] device={xr.dev} encoder={encoder} cfg={emb_cfg} dim={xr.dim} reg={regressor}",
          flush=True)

    Een, oken = _embed_cached(xr, list(en["sent"]), list(en["token"]), "en")
    Em, okm = _embed_cached(xr, list(ml["sent"]), list(ml["token"]), "mlsp10")
    # Cheie proprie, NU "mlsp10": exista deja un emb_mlsp10_..._300.npy dintr-o rulare veche, iar
    # `_embed_cached` verifica doar dimensiunea, nu continutul. 300 de randuri se re-embedeaza in
    # cateva secunde, deci nu merita riscul de a corela predictii cu embedding-uri straine.
    Et, okt = _embed_cached(xr, list(mlt["sent"]), list(mlt["token"]), "mlsp10trial")
    print(f"[E1t] embedding gata in {time.time()-t0:.0f}s | EN {oken.sum()}/{len(en)} "
          f"test {okm.sum()}/{len(ml)} trial {okt.sum()}/{len(mlt)}", flush=True)

    if emb_tf != "nu":
        # Potrivita pe reuniunea randurilor VALIDE, fara etichete. Blocul de trial intra si el, ca
        # sa nu existe doua spatii diferite intre splituri.
        Een2, Em2, Et2 = emb_transform(emb_tf, [Een[oken], Em[okm], Et[okt]])
        if Een2.shape[1] == Een.shape[1]:
            Een = Een.copy(); Em = Em.copy(); Et = Et.copy()
            Een[oken], Em[okm], Et[okt] = Een2, Em2, Et2
        else:
            # `proj-N` intoarce blocuri mai inguste, deci scrierea la loc in matricea veche ar crapa
            # pe forma. Se realoca la latimea noua si se umple NUMAI pe `ok`; randurile invalide
            # raman zero, exact ca inainte nefolosite, fiindca mastile le exclud peste tot mai jos.
            def _lat(B2, ok, n):
                Z = np.zeros((n, B2.shape[1]), np.float32); Z[ok] = B2; return Z
            Een = _lat(Een2, oken, len(Een)); Em = _lat(Em2, okm, len(Em)); Et = _lat(Et2, okt, len(Et))

    # `lemma_freq`: frecventa devine max(zipf_forma, zipf_lema), fixul care pe romana a adus cel mai
    # mare castig unic al lucrarii. Sub `na_policy="mlsp"` lema trece si ea prin `zipf_safe`, deci pe
    # limbile neservite de wordfreq (si) inlocuirea nu se aplica si coloana ramane bit-identica.
    kw_en, kw_ml, kw_t = {}, {}, {}
    if lemma_freq:
        from lemmatize_mlsp import lemma_array
        kw_en = dict(lemmas=lemma_array(list(en["sent"]), list(en["token"]), "complex_en", "en"))
        kw_ml = dict(lemmas=lemma_array(list(ml["sent"]), list(ml["token"]), "test", list(ml["lang"])))
        kw_t = dict(lemmas=lemma_array(list(mlt["sent"]), list(mlt["token"]), "trial", list(mlt["lang"])))
    if ctx_div:
        from mlsp_common import load_ctx_div
        print(f"[E1t] --ctx-div {ctx_div}: tabele incarcate, tipuri per limba {load_ctx_div()}",
              flush=True)
        kw_en["ctxdiv"] = kw_ml["ctxdiv"] = kw_t["ctxdiv"] = ctx_div
    fe = ("oov",) if oov else ()
    lex_en = slex(list(en["token"]), ["en"] * len(en), fe, na_policy="mlsp", **kw_en)
    lex_ml = slex(list(ml["token"]), list(ml["lang"]), fe, na_policy="mlsp", **kw_ml)
    lex_t = slex(list(mlt["token"]), list(mlt["lang"]), fe, na_policy="mlsp", **kw_t)
    if oov:
        print(f"[E1t] --oov: coloana indicator per token adaugata, latime {lex_ml.shape[1]}",
              flush=True)

    # Ablatie de plafon: coloana 0 e zipf. Se anuleaza, nu se scoate, ca latimea sa ramana aceeasi si
    # cifra sa fie comparabila cu bratul intreg fara nicio alta schimbare.
    if no_freq:
        for _L in (lex_en, lex_ml, lex_t):
            _L[:, 0] = 0.0
        print("[E1t] ABLATIE --no-freq: coloana de frecventa anulata pe toate cele trei blocuri",
              flush=True)

    # `afeat`: slotul de fertilitate lasat gol in `_Xc` se umple, si lungimea in caractere se
    # anuleaza. Fertilitatea se centreaza in interiorul limbii pentru MLSP si pe media blocului
    # intreg pentru CompLex EN, exact ca embeddingul de langa ea.
    use_fert, drop_len = AFEATS[afeat]
    fert_en = fert_ml = fert_t = None
    if use_fert:
        fert_en = fertility(list(en["token"]))
        fert_ml = fertility(list(ml["token"]))
        fert_t = fertility(list(mlt["token"]))
        print(f"[E1t] afeat={afeat} | fertilitate medie: EN {fert_en.mean():.2f} "
              f"test {fert_ml.mean():.2f} trial {fert_t.mean():.2f}", flush=True)
    elif drop_len:
        print(f"[E1t] afeat={afeat} | lungimea in caractere anulata", flush=True)

    yen = en["complexity"].values.astype(float)[oken]
    Xen = _Xc(Een[oken], lex_en[oken], Een[oken].mean(0, keepdims=True),
              fert=None if fert_en is None else fert_en[oken],
              fert_mu=None if fert_en is None else float(fert_en[oken].mean()),
              drop_len=drop_len)

    y = ml["complexity"].values.astype(float)[okm]
    lang = ml["lang"].values[okm]
    ctx = ml["context_id"].values[okm]
    idx = np.flatnonzero(okm)                      # pozitia in load_mlsp("test"), pentru joinul de la §4
    Xml = _center_per_lang(Em[okm], lex_ml[okm], lang,
                           fert=None if fert_ml is None else fert_ml[okm], drop_len=drop_len)

    yt = mlt["complexity"].values.astype(float)[okt]
    langt = mlt["lang"].values[okt]
    ctxt = mlt["context_id"].values[okt]
    idxt = np.flatnonzero(okt)
    Xt_self = _center_per_lang(Et[okt], lex_t[okt], langt,
                               fert=None if fert_t is None else fert_t[okt], drop_len=drop_len)
    Xt_test = np.zeros_like(Xt_self)               # acelasi bloc, centrat pe media de TEST a limbii
    for lg in pd.unique(langt):
        mt, mm = (langt == lg), (lang == lg)
        # si fertilitatea se centreaza pe media de TEST a limbii, ca embeddingul de deasupra
        Xt_test[mt] = _Xc(Et[okt][mt], lex_t[okt][mt], Em[okm][mm].mean(0, keepdims=True),
                          fert=None if fert_t is None else fert_t[okt][mt],
                          fert_mu=None if fert_ml is None else float(fert_ml[okm][mm].mean()),
                          drop_len=drop_len)

    # Dropout pe frecventa, daca e cerut. Se aplica si bratului EN-only, ca amandoua bratele semnalului
    # A sa fie potrivite sub acelasi regim; altfel `w_src` ar amesteca doua conventii diferite.
    D = Een.shape[1]
    Xen_f = _freq_drop(Xen, D, freq_drop, SEED)
    if freq_drop > 0:
        print(f"[E1t] --freq-drop {freq_drop}: coloana de frecventa anulata pe o fractiune din "
              f"randurile de ANTRENARE, index {D + 1}", flush=True)

    if export_blocks:
        # Blocurile, o singura data, ca alt capat (venv izolat sau Colab) sa poata reconstrui cele
        # 12 cereri fara sa reia embeddingul si fara sa importe nimic din proiect. Se scriu BLOCURI,
        # nu cereri: cele 12 matrice de antrenare se suprapun aproape complet, deci exportul lor ar
        # fi de zece ori mai mare degeaba.
        if freq_drop > 0:
            raise SystemExit("--export-blocks refuza --freq-drop: masca depinde de limba tinuta "
                             "deoparte, deci celalalt capat ar reconstrui alte matrice.")
        # dtype de unicode explicit, nu `.astype(str)`: pe un array de obiecte pandas acela lasa
        # object, iar `np.load` refuza object fara `allow_pickle`, deci exportul ar fi ilizibil.
        _u = lambda v: np.asarray(list(v), dtype="U16")
        np.savez(export_blocks, Xen_f=Xen_f, yen=yen, Xml=Xml, y=y, lang=_u(lang),
                 Xt_self=Xt_self, Xt_test=Xt_test, langt=_u(langt))
        from tabfm_bridge import cereri, req_key
        print(f"[E1t] blocuri -> {export_blocks} "
              f"({os.path.getsize(export_blocks)/1e6:.1f} MB)", flush=True)
        for nume, a, b, c in cereri(np.load(export_blocks)):
            print(f"       {req_key(a, b, c)}  {nume:14s} ctx={a.shape} pred={c.shape}", flush=True)
        return None

    p_en_test = reg(Xen_f, yen, Xml)                # bratul EN-only, o singura potrivire
    p_en_trial = reg(Xen_f, yen, Xt_self)
    print(f"[E1t] brat EN-only potrivit ({time.time()-t0:.0f}s)", flush=True)

    rows, prows = [], []
    for L in (holdout or sorted(pd.unique(lang))):
        te, tr = (lang == L), (lang != L)
        tt = (langt == L)
        Xtr = np.vstack([Xen, Xml[tr]]); ytr = np.concatenate([yen, y[tr]])
        # Samanta depinde de limba tinuta deoparte, deci fiecare potrivire are propria realizare a
        # mastii, dar rularea intreaga e reproductibila. Numai Xtr se atinge; `Xpred` de mai jos, care
        # contine randurile lui L, ramane cu frecventa intacta.
        Xtr = _freq_drop(Xtr, D, freq_drop, SEED + hash(str(L)) % 100003)
        # O singura potrivire per limba, trei blocuri prezise deodata: test, trial centrat pe el
        # insusi, trial centrat pe media de test. Predictia pe test iese identica cu cea din E1.
        Xpred = np.vstack([Xml[te], Xt_self[tt], Xt_test[tt]])
        p = reg(Xtr, ytr, Xpred)
        n_te, n_tt = int(te.sum()), int(tt.sum())
        p_te, p_tt_self, p_tt_test = p[:n_te], p[n_te:n_te + n_tt], p[n_te + n_tt:]

        b_te = boot_r_ci(y[te], p_te, ctx[te], n_boot=n_boot, seed=SEED)
        b_tt = boot_r_ci(yt[tt], p_tt_self, ctxt[tt], n_boot=n_boot, seed=SEED)
        r_test, r_trial = b_te["r"], b_tt["r"]

        # POARTA. Se aplica INAINTE de a scrie orice, limba cu limba.
        if L in ref_r and abs(round(r_test, 4) - round(ref_r[L], 4)) > 1e-4:
            raise SystemExit(f"[E1t] {L}: r pe test {r_test:.6f} nu reproduce {ref_r[L]:.4f} din "
                             f"{os.path.basename(ref)}. Bratul nu mai e acelasi. Nu se scrie nimic.")

        # Diferenta trial minus test: doua esantioane practic disjuncte (zero contexte comune peste tot
        # cu exceptia fil 1 si fr 2), deci diferenta esantioanelor bootstrap independente e legitima.
        dboot = (b_tt["boot"] - b_te["boot"][:len(b_tt["boot"])]
                 if len(b_tt["boot"]) and len(b_te["boot"]) else np.array([]))
        # `n_tt == 0`: limba n-are randuri de trial (cazul romanei, RoLCP n-are split de trial).
        # `pearson()` de mai jos nu tolereaza tablouri goale, deci cele doua cifre de trial devin NaN
        # in loc sa creada rularea intreaga la limba respectiva.
        rows.append({"lang": L, "n_test": n_te, "n_ctx_test": b_te["n_ctx"],
                     "n_trial": n_tt, "n_ctx_trial": b_tt["n_ctx"],
                     "r_test_multi": round(r_test, 4), "r_trial_multi_selfmu": round(r_trial, 4),
                     "r_trial_multi_testmu": (round(pearson(p_tt_test, yt[tt]), 4)
                                              if n_tt >= 2 else float("nan")),
                     "r_test_en": round(pearson(p_en_test[te], y[te]), 4),
                     "r_trial_en": (round(pearson(p_en_trial[tt], yt[tt]), 4)
                                    if n_tt >= 2 else float("nan")),
                     "delta_split": round(r_trial - r_test, 4),
                     "delta_lo": round(float(np.percentile(dboot, 2.5)), 4) if len(dboot) else np.nan,
                     "delta_hi": round(float(np.percentile(dboot, 97.5)), 4) if len(dboot) else np.nan,
                     "r_test_lo": round(b_te["lo"], 4), "r_test_hi": round(b_te["hi"], 4),
                     "r_trial_lo": round(b_tt["lo"], 4), "r_trial_hi": round(b_tt["hi"], 4)})
        pd.DataFrame(rows).to_csv(out, index=False)          # dupa FIECARE limba, nu la final

        for j, k in enumerate(np.flatnonzero(te)):
            prows.append(("test", int(idx[k]), L, ml["token"].values[idx[k]], float(y[te][j]),
                          ctx[te][j], float(p_en_test[te][j]), float(p_te[j]), ""))
        for j, k in enumerate(np.flatnonzero(tt)):
            prows.append(("trial", int(idxt[k]), L, mlt["token"].values[idxt[k]], float(yt[tt][j]),
                          ctxt[tt][j], float(p_en_trial[tt][j]), float(p_tt_self[j]),
                          f"{float(p_tt_test[j]):.8f}"))
        pd.DataFrame(prows, columns=["split", "idx", "lang", "token", "complexity", "context_id",
                                     "p_en", "p_multi", "p_multi_testmu"]).to_csv(preds, index=False)
        print(f"  {L:4s} test n={n_te:4d} r={r_test:+.4f} [{b_te['lo']:+.4f},{b_te['hi']:+.4f}] | "
              f"trial n={n_tt:3d} r={r_trial:+.4f} [{b_tt['lo']:+.4f},{b_tt['hi']:+.4f}] | "
              f"Δ_split {r_trial - r_test:+.4f} | testmu {rows[-1]['r_trial_multi_testmu']:+.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)

    d = pd.DataFrame(rows)
    _trial_gap_report(d, report, ref_applied=len(ref_r) > 0)
    print(f"\n-> {out}\n-> {preds}\n-> {report}")
    print(f"[E1t] r mediu test {d['r_test_multi'].mean():+.4f} | trial {d['r_trial_multi_selfmu'].mean():+.4f} "
          f"| Δ_split mediu {d['delta_split'].mean():+.4f}, sd intre limbi {d['delta_split'].std(ddof=1):.4f}")
    return d


def _trial_gap_report(d, path, ref_applied=True):
    """Raportul decalajului. Nicio cifra nu se recalculeaza aici, doar se formateaza."""
    dl = d["delta_split"].values.astype(float)
    up = int((dl > 0).sum())
    L = ["# E1 pe trial. Decalajul trial fata de test, masurat pe acelasi brat\n\n",
         f"Generat {time.strftime('%Y-%m-%d %H:%M:%S')} de `finetune_xlmr.py --frozentrial`. "
         "Date brute: `output/e1_frozen_trial.csv`, predictii per instanta in "
         "`output/e1_frozen_preds.csv`.\n\n",
         "Bratul e cel din E1, nemodificat: EN plus MLSP-test fara limba L, embedding XLM-R inghetat "
         "plus patru trasaturi lexicale. Singura diferenta e ce prezice: pe langa instantele de test "
         "ale lui L, si cele 30 de instante de trial ale lui L. Trial-ul lui L nu e in antrenare, deci "
         "protocolul e neatins, iar decalajul care iese e al splitului, nu al modelului.\n\n"]
    if ref_applied:
        L.append("Poarta de reproducere a trecut: `r_test_multi` reproduce `r_multi` din "
                 "`output/e1_lolo_frozen.csv` pe toate limbile, deci e acelasi brat, nu unul refacut.\n\n")
    L += ["## r pe test fata de r pe trial\n\n",
          "| limba | n test | ctx | r test | CI 95% | n trial | ctx | r trial | CI 95% | Δ split | CI 95% |\n",
          "|---|---|---|---|---|---|---|---|---|---|---|\n"]
    for r in d.itertuples():
        L.append(f"| {r.lang} | {r.n_test} | {r.n_ctx_test} | {r.r_test_multi:+.4f} | "
                 f"[{r.r_test_lo:+.4f}, {r.r_test_hi:+.4f}] | {r.n_trial} | {r.n_ctx_trial} | "
                 f"{r.r_trial_multi_selfmu:+.4f} | [{r.r_trial_lo:+.4f}, {r.r_trial_hi:+.4f}] | "
                 f"{r.delta_split:+.4f} | [{r.delta_lo:+.4f}, {r.delta_hi:+.4f}] |\n")
    L.append(f"| **medie** | | | **{d['r_test_multi'].mean():+.4f}** | | | | "
             f"**{d['r_trial_multi_selfmu'].mean():+.4f}** | | **{dl.mean():+.4f}** | |\n")
    L += [f"\n**Δ split mediu {dl.mean():+.4f}**, sd intre limbi {dl.std(ddof=1):.4f}, "
          f"interval {dl.min():+.4f} pana la {dl.max():+.4f}. Trial-ul e mai mare pe {up} din "
          f"{len(dl)} limbi.\n\n",
          "Intervalele vin din bootstrap pe contexte, nu pe itemi. Cel al lui Δ e diferenta a doua "
          "reesantionari independente, ceea ce e legitim fiindca cele doua splituri sunt practic "
          "disjuncte pe contexte, cu exceptia unui context la fil si a doua la fr.\n\n",
          "## Centrarea per limba: cat din decalaj vine din ea\n\n",
          "`selfmu` centreaza cele 30 de instante de trial pe media lor, adica exact ce s-ar face la "
          "desfasurare pe un set de 30. `testmu` le centreaza pe media blocului de test al aceleiasi "
          "limbi, deci fara zgomotul de centrare pe 30 de randuri. Diferenta dintre cele doua e partea "
          "din decalaj care tine de centrare, nu de split.\n\n",
          "| limba | r trial selfmu | r trial testmu | diferenta |\n|---|---|---|---|\n"]
    for r in d.itertuples():
        L.append(f"| {r.lang} | {r.r_trial_multi_selfmu:+.4f} | {r.r_trial_multi_testmu:+.4f} | "
                 f"{r.r_trial_multi_testmu - r.r_trial_multi_selfmu:+.4f} |\n")
    dc = (d["r_trial_multi_testmu"] - d["r_trial_multi_selfmu"]).values.astype(float)
    L.append(f"\n**Diferenta medie {dc.mean():+.4f}**, interval {dc.min():+.4f} pana la {dc.max():+.4f}.\n")
    L += ["\n## Bratul EN-only, pe ambele splituri\n\n",
          "| limba | EN-only test | EN-only trial | Δ_frozen test | Δ_frozen trial |\n|---|---|---|---|---|\n"]
    for r in d.itertuples():
        L.append(f"| {r.lang} | {r.r_test_en:+.4f} | {r.r_trial_en:+.4f} | "
                 f"{r.r_test_multi - r.r_test_en:+.4f} | "
                 f"{r.r_trial_multi_selfmu - r.r_trial_en:+.4f} |\n")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--lorasweep", action="store_true", help="grila LoRA (rang mic) -> finetune_lora_sweep.csv")
    ap.add_argument("--multilora", action="store_true", help="gate multilingual held-out-language (EN-only vs EN+romanic)")
    ap.add_argument("--frozenmulti", action="store_true", help="baseline FROZEN pe split held-out-language")
    ap.add_argument("--lemma-freq", action="store_true", dest="lemma_freq",
                    help="frecventa = max(zipf_forma, zipf_lema) in semnalul A. Implicit OFF, ca "
                         "bratul publicat sa ramana cel implicit. Cere lemmatize_mlsp.py rulat intai. "
                         "Scrie in fisiere proprii, cu sufixul _lemma, si dezactiveaza poarta de "
                         "reproducere, fiindca r se schimba intentionat.")
    ap.add_argument("--afeat", choices=list(AFEATS), default="baza",
                    help="setul de trasaturi al semnalului A. `baza` e cel publicat: lungime in "
                         "caractere, slotul de fertilitate gol. `fert_inloc` pune numarul de "
                         "subword-uri XLM-R in locul lungimii, `fara_lung` doar anuleaza lungimea, "
                         "`fert_plus` le pune pe amandoua. Implicit `baza`, ca bratul publicat sa "
                         "ramana cel implicit. Scrie in fisiere proprii, cu sufixul numelui, si "
                         "dezactiveaza poarta de reproducere, fiindca r se schimba intentionat.")
    ap.add_argument("--encoder", default="xlmr",
                    help="encoderul bratului INGHETAT (§3.6): xlmr, xlmr-large, labse, e5. Nu are "
                         "legatura cu --model, care e pentru fine-tuning. Orice valoare diferita de "
                         "`xlmr` sufixeaza TOATE caile de iesire cu numele encoderului, deci nu poate "
                         "suprascrie semnalul A al sistemului.")
    ap.add_argument("--oov", action="store_true",
                    help="adauga indicatorul per TOKEN `zipf == 0`, adica `feats=(\"oov\",)` din "
                         "`solution_bert.lexical`. Exista de mult in cod dar n-a fost folosit "
                         "niciodata pe calea multilingva. Motivul pentru care intra acum e masurat: "
                         "ablatia `--no-freq` arata ca pe `fil`, unde 152 din 570 de tinte sunt OOV, "
                         "fuziunea URCA cu +0.0225 daca se scoate frecventa cu totul. Deci zerourile "
                         "de OOV induc in eroare, iar indicatorul le distinge de raritatea reala. "
                         "`freq_na` de la `na_policy` e per LIMBA, nu per token, deci nu acopera asta.")
    ap.add_argument("--emb-tf", dest="emb_tf", default="nu", type=_emb_tf_kind,
                    help="transformare pe spatiul de embedding, potrivita fara etichete pe reuniunea "
                         "blocurilor. `pca1`/`pca5` scad primele componente principale, `zca` albeste "
                         "complet, `proj-N` PROIECTEAZA pe primele N si reduce latimea la N. "
                         "Implicit `nu`.")
    ap.add_argument("--freq-tail", dest="freq_tail", default="nu",
                    choices=["nu", "exact", "prefix", "subword"],
                    help="a doua sursa de frecventa pentru limbile de coada, din `data/freq_tail/`. "
                         "Pe `si` wordfreq nu serveste limba deloc (600/600 fara frecventa), pe "
                         "`fil` 152/570 de tinte sunt OOV. Sursa se consulta NUMAI unde wordfreq da "
                         "0, deci nu schimba nicio valoare existenta. Treptele: `exact` doar forma, "
                         "`prefix` plus cel mai lung prefix-cuvant, `subword` plus primul subword "
                         "XLM-R. Implicit `nu`, deci bratul publicat ramane cel implicit.")
    ap.add_argument("--ctx-div", dest="ctx_div", default=None, choices=["plus", "inloc"],
                    help="diversitate contextuala din `data/ctx_div/`. `plus` adauga o coloana, "
                         "`inloc` inlocuieste zipf. Varianta fidela literaturii e `inloc`: Adelman, "
                         "Brown si Quesada (2006) arata ca frecventa dispare cand se controleaza "
                         "diversitatea, nu invers. Cere build_ctx_div.py rulat.")
    ap.add_argument("--freq-drop", dest="freq_drop", type=float, default=0.0,
                    help="fractiunea randurilor de ANTRENARE pe care coloana de frecventa se "
                         "anuleaza. 0 e comportamentul de pana acum, bit-exact; 1 ar fi --no-freq "
                         "aplicat doar la antrenare. Vezi `_freq_drop` pentru cele doua masuratori "
                         "care incadreaza intervalul.")
    ap.add_argument("--no-freq", dest="no_freq", action="store_true",
                    help="ABLATIE: anuleaza coloana de frecventa peste tot. Serveste la masurarea "
                         "plafonului, adica cat valoreaza frecventa acolo unde EXISTA, ca sa se "
                         "stie cat pierd si si fil unde nu exista.")
    ap.add_argument("--emb-cfg", dest="emb_cfg", choices=list(EMB_CONFIGS), default="last4",
                    help="configul de EXTRACTIE al bratului inghetat: ce straturi se combina, cum se "
                         "face pool peste subword-urile tintei, si daca intra vectorul cuvantului "
                         "izolat. `last4` e cel publicat. `frozen_trial_gap` accepta parametrul de "
                         "cand exista, dar main() nu-l pasa niciodata, deci niciuna din configuratii "
                         "n-a fost rulata. Orice valoare diferita de `last4` sufixeaza TOATE caile "
                         "de iesire, deci nu poate suprascrie semnalul A al sistemului.")
    # `type=` in loc de `choices=`: grila de alpha e continua si nu se poate enumera, exact ca
    # `proj-N` la `--emb-tf` mai sus. `regressor_kind` valideaza multimea fixa PLUS familiile, deci o
    # greseala de scriere cade la parsarea argumentelor, inainte de embedding si de cele 12 potriviri.
    ap.add_argument("--regressor", type=regressor_kind, default="blend",
                    help="regresorul semnalului A. `blend` (implicit) e Ridge300+HGB, bit-exact cel "
                         "publicat. `ridge` si `hgb` sunt cele doua jumatati ale lui, rulate separat. "
                         "`tabfm-cache` cere venv-ul izolat din `tabfm_bridge.py`. Fixe: "
                         + ", ".join(REGRESSORS) + ". Familii parametrice: ridge-a<A>, lasso-a<A>, "
                         "krr-a<A>, pls-k<K>, enet-a<A>-l<zecimi>, cu <A> scris fara punct "
                         "(30, 1e-3, 3e-2) fiindca numele intra ca atare in numele fisierului.")
    ap.add_argument("--export-blocks", dest="export_blocks", default=None, metavar="CALE.npz",
                    help="scrie blocurile semnalului A intr-un .npz si se opreste, fara sa "
                         "potriveasca nimic. Pentru `tabfm_runner.py` si pentru notebook-ul de "
                         "Colab. Vezi `tabfm_bridge.py`.")
    ap.add_argument("--frozentrial", action="store_true",
                    help="acelasi brat inghetat, evaluat SI pe cele 300 de instante de trial: da "
                         "decalajul trial-test plus predictiile per instanta pentru fuziune")
    ap.add_argument("--include-ro", dest="include_ro", action="store_true",
                    help="adauga RoLCP ca a 11-a limba (load_mlsp(include_ro=True)). Cerut de "
                         "coordonator pe 29 aug 2026. Implicit False, deci bratul publicat pe cele "
                         "10 limbi ramane neschimbat; scrie in fisiere proprii, cu sufixul _ro11, si "
                         "dezactiveaza poarta de reproducere fata de e1_lolo_frozen.csv, fiindca "
                         "antrenarea celorlalte 10 limbi include acum si randurile romanesti.")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--model", choices=list(MODELS), default="base")
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--freeze", type=int, default=0)
    ap.add_argument("--lora", type=int, default=0, help="rang LoRA (0=fara); pt --gate/--final")
    ap.add_argument("--seeds", type=int, default=4, help="nr seed-uri pt ensemble la --final")
    ap.add_argument("--out", default=os.path.join(DATA, "finetune_test.csv"))
    args = ap.parse_args()

    if args.freq_tail != "nu":
        from mlsp_common import load_tail_freq
        n = load_tail_freq(args.freq_tail)
        print("[freq-tail] mod=%s | %s" % (args.freq_tail,
              ", ".join(f"{k}: {v:,} tipuri" for k, v in n.items())), flush=True)

    tok = AutoTokenizer.from_pretrained(MODELS[args.model])
    en = load_complex_en(); ml = load_mlsp(include_ro=args.include_ro)
    print(f"Device {DEVICE} | EN={len(en)} MLSP={0 if ml is None else len(ml)}")
    cfg = {"model": args.model, "lr": args.lr, "epochs": args.epochs,
           "freeze": args.freeze, "lora": args.lora}

    if args.sweep or args.lorasweep:
        if ml is None:
            sys.exit("sweep are nevoie de data/mlsp/")
        grid = LORA_GRID if args.lorasweep else SWEEP_GRID
        path = os.path.join(DATA, "finetune_lora_sweep.csv" if args.lorasweep else "finetune_sweep.csv")
        run_sweep(en, ml, tok, grid, path)
        return

    if args.multilora:
        if ml is None:
            sys.exit("multilora are nevoie de data/mlsp/")
        mcfg = {"model": "base", "lr": args.lr if args.lora else 2e-4,
                "epochs": args.epochs, "lora": args.lora or 16}
        print(f"[multilingual gate] cfg={_cfg_key(mcfg)}")
        multilingual_gate(en, ml, tok, mcfg)
        return

    # Caile de iesire sunt disjuncte intre variante: cea publicata, fara lema si cu setul de
    # trasaturi `baza`, ramane pe numele vechi, iar fiecare varianta scrie langa ea. Nimic nu se suprascrie, deci cele doua se pot compara
    # oricand fara sa se re-ruleze niciunul. `ref` devine o cale inexistenta la varianta cu lema:
    # poarta compara r cu E1, iar fixul schimba r prin definitie, deci ar opri rularea pe buna dreptate.
    def _p(name):
        base, ext = os.path.splitext(name)
        # Encoderul intra PRIMUL in sufix, si e gol la `xlmr`. Fara el, o rulare cu alt encoder ar
        # scrie peste `e1_frozen_preds_lemma_fert_inloc.csv`, adica peste semnalul A al sistemului,
        # si nicio cifra din raport n-ar arata ca s-a intamplat.
        suf = ("" if args.encoder == "xlmr" else f"_{args.encoder}")
        suf += ("" if args.emb_cfg == "last4" else f"_{args.emb_cfg}")
        suf += ("_oov" if args.oov else "")
        suf += ("" if args.emb_tf == "nu" else f"_tf-{args.emb_tf}")
        suf += ("" if args.freq_tail == "nu" else f"_ft-{args.freq_tail}")
        suf += ("_nofreq" if args.no_freq else "")
        suf += ("" if args.freq_drop == 0.0 else f"_fd{args.freq_drop:g}".replace(".", ""))
        suf += ("" if not args.ctx_div else f"_cd-{args.ctx_div}")
        suf += ("" if args.regressor == "blend" else f"_reg-{args.regressor}")
        suf += ("_lemma" if args.lemma_freq else "") + ("" if args.afeat == "baza" else f"_{args.afeat}")
        suf += ("_ro11" if args.include_ro else "")
        return os.path.join(HERE, "output", f"{base}{suf}{ext}")

    if args.frozenmulti:
        if ml is None:
            sys.exit("frozenmulti are nevoie de data/mlsp/")
        frozen_multi_gate(en, ml, lemma_freq=args.lemma_freq, afeat=args.afeat,
                          encoder=args.encoder, emb_cfg=args.emb_cfg, regressor=args.regressor,
                          out=_p("e1_lolo_frozen.csv"))
        return

    if args.frozentrial:
        if ml is None:
            sys.exit("frozentrial are nevoie de data/mlsp/")
        # Poarta cere ca r pe test sa reproduca E1. `--lemma-freq` si `--afeat` schimba amandoua
        # r prin definitie, deci referinta devine o cale inexistenta si poarta se stinge singura.
        canonic = (not args.lemma_freq and args.afeat == "baza" and args.encoder == "xlmr"
                   and args.emb_cfg == "last4" and args.freq_tail == "nu" and not args.no_freq
                   and args.emb_tf == "nu" and not args.oov and args.freq_drop == 0.0
                   and args.ctx_div is None and args.regressor == "blend" and not args.include_ro)
        frozen_trial_gap(en, ml, load_mlsp("trial"), lemma_freq=args.lemma_freq, afeat=args.afeat,
                         encoder=args.encoder, emb_cfg=args.emb_cfg, no_freq=args.no_freq,
                         emb_tf=args.emb_tf, oov=args.oov, freq_drop=args.freq_drop,
                         ctx_div=args.ctx_div, regressor=args.regressor,
                         export_blocks=args.export_blocks,
                         out=_p("e1_frozen_trial.csv"), preds=_p("e1_frozen_preds.csv"),
                         report=_p("e1_trial_gap.md"),
                         ref=os.path.join(HERE, "output", "e1_lolo_frozen.csv") if canonic
                         else os.path.join(HERE, "output", "_fara_referinta"))
        return

    if args.gate:
        if ml is None:
            sys.exit("gate are nevoie de data/mlsp/")
        m1, l1 = train(en, tok, cfg); r1 = pearson(predict(m1, ml, tok, max_len=l1),
                                                   ml["complexity"].values.astype(float))
        del m1; torch.cuda.empty_cache()
        m2, l2 = train(ml, tok, cfg); r2 = pearson(predict(m2, en, tok, max_len=l2),
                                                   en["complexity"].values.astype(float))
        print(f"\n[FINETUNE gate {_cfg_key(cfg)}] EN->ML {r1:.4f} | ML->EN {r2:.4f} | "
              f"transfer_avg {0.5*(r1+r2):.4f} (frozen 0.5512)")
        return

    if args.final:
        train_df = en if ml is None else pd.concat([en, ml], ignore_index=True)
        test = pd.read_csv(os.path.join(DATA, "test_set.csv")).rename(columns={"text": "sent"})
        preds = []
        for s in range(args.seeds):
            print(f"[final] seed {s+1}/{args.seeds} fine-tune pe {len(train_df)} ({_cfg_key(cfg)}) ...", flush=True)
            m, mlen = train(train_df, tok, cfg, seed=SEED + s)
            preds.append(predict(m, test, tok, max_len=mlen)); del m; torch.cuda.empty_cache()
        pr = np.mean(preds, axis=0)
        pd.DataFrame({"datapointID": test["datapointID"], "ft_complexity": pr}).to_csv(args.out, index=False)
        print(f"Salvat {args.out}: {len(pr)} (ensemble {args.seeds} seed-uri; mean {pr.mean():.3f} std {pr.std():.3f})")
        return

    sys.exit("alege --gate / --sweep / --final")


if __name__ == "__main__":
    main()
