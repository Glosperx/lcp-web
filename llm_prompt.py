# =============================================================================
# Imbunatatire prompt LLM (parghia mare). Reutilizeaza RoLlama3 din LLMRater.
#   zeroshot : promptul actual (baseline, 2 sabloane, soft-read P(1..5) la primul token).
#   fewshot  : k exemple etichetate in prompt (calibreaza scala). Tot un singur forward.
#   cot      : genereaza rubrica (factori) apoi soft-read P(1..5) la final (Wei et al. 2022).
#   cot_sc   : self-consistency CoT (Wang et al. 2022) — k rationale esantionate, scoruri mediate.
#
#   --llm-gate    : rateaza esantion CompLex EN + MLSP Romance (au etichete) -> corelatie cu complexitatea
#                   reala = gate GRATIS de calitate prompt. + sanity pe cele 14 RO.
#   --predict-ro  : rateaza RO test cu --mode -> data/llm_<mode>_test.csv (semnal pt fuziune).
# NU atinge calea bit-exact a lui best. transformers==4.46.3 (RoLlama3 deja incarcat).
# =============================================================================
import os
import sys
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
from solution_bert import LLMRater, SEED
from finetune_xlmr import load_complex_en, load_mlsp

RUBRIC = ("frecventa, lungime/silabe, daca e termen tehnic/specializat, complexitate morfologica")


def c2s(c):
    """complexitate [0,1] -> intreg 1-5 (pt exemplele few-shot)."""
    return int(np.clip(round(1 + 4 * float(c)), 1, 5))


class PromptRater(LLMRater):
    """Extinde LLMRater cu few-shot si CoT, pastrand soft-read-ul P(1..5)."""

    def _soft_msgs(self, messages):
        ids = self.tok.apply_chat_template(messages, add_generation_prompt=True,
                                           return_tensors="pt").to(self.dev)
        with self.torch.no_grad():
            logits = self.model(ids).logits[0, -1].float()
        probs = self.F.softmax(logits, dim=-1)
        p = np.array([float(probs[self.digit[d]].sum()) for d in "12345"])
        if p.sum() < 1e-9:
            return None
        p /= p.sum()
        return (float((p * np.arange(1, 6)).sum()) - 1.0) / 4.0

    def rate_fewshot(self, sent, tok_str, shots):
        ex = "\n".join(f'- cuvant "{w}" in "{s}" -> {sc}' for (s, w, sc) in shots)
        content = (f"Evalueaza complexitatea lexicala pe o scara 1-5 (1=foarte familiar, 5=foarte dificil).\n"
                   f"Exemple:\n{ex}\n\n"
                   f'Acum evalueaza cuvantul "{str(tok_str).strip()}" in propozitia:\n'
                   f'"{str(sent).replace(chr(10), " ").strip()}"\nRaspunde DOAR cu o cifra 1-5.')
        return self._soft_msgs([{"role": "user", "content": content}])

    def rate_cot(self, sent, tok_str):
        sent = str(sent).replace("\n", " ").strip(); tok_str = str(tok_str).strip()
        ask = ({"role": "user",
                "content": f'In propozitia: "{sent}"\nAnalizeaza pe scurt factorii de complexitate ai '
                           f'cuvantului "{tok_str}" ({RUBRIC}). Maxim 2 propozitii. NU da scorul inca.'})
        ids = self.tok.apply_chat_template([ask], add_generation_prompt=True, return_tensors="pt").to(self.dev)
        with self.torch.no_grad():
            gen = self.model.generate(ids, max_new_tokens=70, do_sample=False,
                                      pad_token_id=self.tok.eos_token_id)
        rationale = self.tok.decode(gen[0, ids.shape[1]:], skip_special_tokens=True).strip()
        msgs = [ask, {"role": "assistant", "content": rationale},
                {"role": "user", "content": "Pe baza analizei, pe scara 1-5 (1=foarte familiar, "
                                            "5=foarte dificil) raspunde DOAR cu cifra:"}]
        return self._soft_msgs(msgs)

    def rate_cot_sc(self, sent, tok_str, k=None, temperature=0.7, top_p=0.9):
        """Self-consistency CoT (Wang et al. 2022): esantioneaza k rationale cu temperatura,
        face soft-read P(1..5) dupa fiecare, mediaza cele k scoruri. Analogul continuu al votului
        majoritar. Fix-ul standard cand CoT greedy pierde pe un model mic (RoLlama3 8B)."""
        k = k if k is not None else getattr(self, "cot_k", 5)
        sent = str(sent).replace("\n", " ").strip(); tok_str = str(tok_str).strip()
        ask = ({"role": "user",
                "content": f'In propozitia: "{sent}"\nAnalizeaza pe scurt factorii de complexitate ai '
                           f'cuvantului "{tok_str}" ({RUBRIC}). Maxim 2 propozitii. NU da scorul inca.'})
        ids = self.tok.apply_chat_template([ask], add_generation_prompt=True, return_tensors="pt").to(self.dev)
        scores = []
        for i in range(k):
            self.torch.manual_seed(SEED + i)          # reproductibil per esantion
            with self.torch.no_grad():
                gen = self.model.generate(ids, max_new_tokens=70, do_sample=True,
                                          temperature=temperature, top_p=top_p,
                                          pad_token_id=self.tok.eos_token_id)
            rationale = self.tok.decode(gen[0, ids.shape[1]:], skip_special_tokens=True).strip()
            msgs = [ask, {"role": "assistant", "content": rationale},
                    {"role": "user", "content": "Pe baza analizei, pe scara 1-5 (1=foarte familiar, "
                                                "5=foarte dificil) raspunde DOAR cu cifra:"}]
            v = self._soft_msgs(msgs)
            if v is not None:
                scores.append(v)
        return float(np.mean(scores)) if scores else np.nan

    def rate_mode(self, sent, tok, mode, shots=None):
        if mode == "zeroshot":
            return self.rate(sent, tok)
        if mode == "fewshot":
            return self.rate_fewshot(sent, tok, shots)
        if mode == "cot":
            return self.rate_cot(sent, tok)
        if mode == "cot_sc":
            return self.rate_cot_sc(sent, tok)
        raise ValueError(mode)


def _shots_from(df, k, lang_label):
    """k exemple few-shot dintr-un df cu (sent, token, complexity)."""
    s = df.sample(min(k, len(df)), random_state=SEED)
    return [(r.sent, r.token, c2s(r.complexity)) for r in s.itertuples()], s.index


def llm_gate(rater, modes, n=300, kshots=6):
    from scipy.stats import pearsonr
    en = load_complex_en(); ml = load_mlsp()
    sources = {"EN": en.rename(columns={"sent": "sent"}),
               "Romance": ml.rename(columns={"sent": "sent"})}
    rows = []
    for name, df in sources.items():
        df = df.dropna(subset=["sent", "token", "complexity"]).reset_index(drop=True)
        shots, shot_idx = _shots_from(df, kshots, name)
        pool = df.drop(index=shot_idx).sample(min(n, len(df) - kshots), random_state=SEED).reset_index(drop=True)
        y = pool["complexity"].values.astype(float)
        for mode in modes:
            pred = np.array([rater.rate_mode(r.sent, r.token, mode, shots) for r in pool.itertuples()])
            m = np.isfinite(pred)
            r = float(pearsonr(pred[m], y[m])[0]) if m.sum() > 3 else float("nan")
            rows.append({"source": name, "mode": mode, "n": int(m.sum()), "pearson": round(r, 4)})
            print(f"[gate] {name:8s} {mode:9s} pearson={r:.4f} (n={int(m.sum())})", flush=True)
    # sanity pe cele 14 RO
    lab = pd.read_csv(os.path.join(DATA, "labeled_examples.csv"))
    sents = pd.read_csv(os.path.join(DATA, "test_set.csv"))[["text_name", "text"]].drop_duplicates("text_name")
    lab = lab.merge(sents, on="text_name", how="left")
    ro_shots = [(r.text, r.token, c2s(r.complexity)) for r in lab.itertuples()][:6]
    for mode in modes:
        pred = np.array([rater.rate_mode(r.text, r.token, mode,
                         [s for s in ro_shots if s[1] != r.token][:5]) for r in lab.itertuples()])
        m = np.isfinite(pred)
        r = float(pearsonr(pred[m], lab["complexity"].values.astype(float)[m])[0]) if m.sum() > 3 else np.nan
        rows.append({"source": "RO14", "mode": mode, "n": int(m.sum()), "pearson": round(r, 4)})
        print(f"[gate] {'RO14':8s} {mode:9s} pearson={r:.4f} (n={int(m.sum())})", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(DATA, "llm_gate.csv"), index=False)
    print("\n", out.pivot(index="mode", columns="source", values="pearson").to_string())
    print("-> data/llm_gate.csv")


def predict_ro(rater, mode):
    lab = pd.read_csv(os.path.join(DATA, "labeled_examples.csv"))
    sents = pd.read_csv(os.path.join(DATA, "test_set.csv"))[["text_name", "text"]].drop_duplicates("text_name")
    lab = lab.merge(sents, on="text_name", how="left")
    shots = [(r.text, r.token, c2s(r.complexity)) for r in lab.itertuples()][:6]
    test = pd.read_csv(os.path.join(DATA, "test_set.csv"))
    pred = np.array([rater.rate_mode(r.text, r.token, mode, shots) for r in test.itertuples()])
    path = os.path.join(DATA, f"llm_{mode}_test.csv")
    pd.DataFrame({"datapointID": test["datapointID"], "llm_cx": pred}).to_csv(path, index=False)
    print(f"Salvat {path}: {len(pred)} (NaN={int(np.isnan(pred).sum())}, "
          f"mean {np.nanmean(pred):.3f})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm-gate", action="store_true", dest="gate")
    ap.add_argument("--predict-ro", action="store_true", dest="predict")
    ap.add_argument("--mode", choices=["zeroshot", "fewshot", "cot", "cot_sc"], default="fewshot")
    ap.add_argument("--modes", default="zeroshot,fewshot,cot,cot_sc", help="moduri pt gate")
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--cot-k", type=int, default=5, dest="cot_k",
                    help="nr. esantioane self-consistency pt cot_sc (mai mic = mai rapid)")
    args = ap.parse_args()

    rater = PromptRater()
    rater.cot_k = args.cot_k
    if args.gate:
        llm_gate(rater, [m.strip() for m in args.modes.split(",")], n=args.n)
    elif args.predict:
        predict_ro(rater, args.mode)
    else:
        sys.exit("alege --llm-gate sau --predict-ro --mode <mode>")


if __name__ == "__main__":
    main()
