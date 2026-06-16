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
from solution_bert import (normalize_token, find_char_span, crop_around, SEED)

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
    en = []
    for k in ("train", "trial", "test"):
        p = os.path.join(DATA, "complex_en", f"lcp_single_{k}.tsv")
        en.append(pd.read_csv(p, sep="\t").dropna(subset=["sentence", "token", "complexity"]))
    en = pd.concat(en, ignore_index=True)
    return en.rename(columns={"sentence": "sent"})[["sent", "token", "complexity"]]


def load_mlsp():
    dfs = []
    for f in glob.glob(os.path.join(DATA, "mlsp", "*.tsv")):
        x = pd.read_csv(f, sep="\t")
        if {"context", "target", "complexity"}.issubset(x.columns):
            x = x.rename(columns={"context": "sent", "target": "token"})
            x["lang"] = os.path.basename(f).split("_")[0].lower()    # cod limba din numele fisierului
            dfs.append(x)
    if not dfs:
        return None
    ml = pd.concat(dfs, ignore_index=True)
    ml = ml[~ml["token"].astype(str).str.contains(" ", na=False)].reset_index(drop=True)
    return ml[["sent", "token", "complexity", "lang"]].dropna(subset=["sent", "token", "complexity"])


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


def frozen_multi_gate(en, ml, holdout=("it", "pt", "es")):
    """Baseline FROZEN pe acelasi split held-out-language: embedding inghetat + blend Ridge/HGB,
    train EN+MLSP(fara L) -> test L. Comparatie directa cu LoRA-multilingual."""
    from solution_bert import XLMR, lexical as slex, _Xc, blend_ridge_hgb
    xr = XLMR("last4", "xlmr")
    Een, oken = xr.embed_frame(list(en["sent"]), list(en["token"]))
    lex_en = slex(list(en["token"]), ["en"] * len(en)); yen = en["complexity"].values.astype(float)
    Em, okm = xr.embed_frame(list(ml["sent"]), list(ml["token"]))
    lex_ml = slex(list(ml["token"]), list(ml["lang"])); yml = ml["complexity"].values.astype(float)
    langs = ml["lang"].values
    rows = []
    for L in holdout:
        te = (langs == L) & okm; tr = (langs != L) & okm
        Xtr = np.vstack([_Xc(Een[oken], lex_en[oken], Een.mean(0, keepdims=True)),
                         _Xc(Em[tr], lex_ml[tr], Em[tr].mean(0, keepdims=True))])
        ytr = np.concatenate([yen[oken], yml[tr]])
        Xte = _Xc(Em[te], lex_ml[te], Em[te].mean(0, keepdims=True))
        r = pearson(blend_ridge_hgb(Xtr, ytr, Xte), yml[te])
        print(f"  FROZEN held-out {L}: r={r:.4f} (n={int(te.sum())})", flush=True)
        rows.append({"holdout": L, "n": int(te.sum()), "r_frozen_multi": round(r, 4)})
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "frozen_multi.csv"), index=False)
    print("-> data/frozen_multi.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--lorasweep", action="store_true", help="grila LoRA (rang mic) -> finetune_lora_sweep.csv")
    ap.add_argument("--multilora", action="store_true", help="gate multilingual held-out-language (EN-only vs EN+romanic)")
    ap.add_argument("--frozenmulti", action="store_true", help="baseline FROZEN pe split held-out-language")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--model", choices=list(MODELS), default="base")
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--freeze", type=int, default=0)
    ap.add_argument("--lora", type=int, default=0, help="rang LoRA (0=fara); pt --gate/--final")
    ap.add_argument("--seeds", type=int, default=4, help="nr seed-uri pt ensemble la --final")
    ap.add_argument("--out", default=os.path.join(DATA, "finetune_test.csv"))
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(MODELS[args.model])
    en = load_complex_en(); ml = load_mlsp()
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

    if args.frozenmulti:
        if ml is None:
            sys.exit("frozenmulti are nevoie de data/mlsp/")
        frozen_multi_gate(en, ml)
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
