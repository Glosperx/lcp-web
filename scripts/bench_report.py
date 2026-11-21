"""Plain-text summary of a bench_cpu.py run, per language and text size (no diacritics, no
markdown tables, so it pastes anywhere). Reads {prefix}.csv, {prefix}_readings.csv and
{prefix}_load.json from bench/results and writes {prefix}_rezumat.txt next to them.

  python scripts/bench_report.py --prefix cpu_docker_mac
  python scripts/bench_report.py --prefix cpu_docker_mac --rerun cpu_docker_mac_rerun_ca
The optional --rerun runs replace the rows of the same (lang, size, mode) in the main run.
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

LANG_NAMES = {"ca": "catalana", "de": "germana", "en": "engleza", "es": "spaniola",
              "fil": "filipineza", "fr": "franceza", "it": "italiana", "ja": "japoneza",
              "pt": "portugheza", "ro": "romana", "si": "sinhaleza"}


def mmss(s):
    if not np.isfinite(s):
        return "-"
    m, s = divmod(int(round(s)), 60)
    return f"{m}m{s:02d}s"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dir", default="bench/results")
    ap.add_argument("--prefix", default="cpu_docker_mac")
    ap.add_argument("--rerun", nargs="*", default=[])
    a = ap.parse_args()
    stem = os.path.join(a.dir, a.prefix)
    runs = pd.read_csv(stem + ".csv")
    reads = pd.read_csv(stem + "_readings.csv")
    load = json.load(open(stem + "_load.json"))
    replaced = []
    for rp in a.rerun:
        r2 = pd.read_csv(os.path.join(a.dir, rp + ".csv"))
        d2 = pd.read_csv(os.path.join(a.dir, rp + "_readings.csv"))
        keys = set(zip(r2["lang"], r2["size"], r2["mode"]))
        replaced += sorted(keys)
        runs = pd.concat([runs[[k not in keys for k in zip(runs["lang"], runs["size"], runs["mode"])]], r2])
        reads = pd.concat([reads[[k not in keys for k in zip(reads["lang"], reads["size"], reads["mode"])]], d2])
    t = runs[~runs["warmup"]].groupby(["lang", "size", "mode"]).median(numeric_only=True)
    # one timed pass per text: the first timed run of each (lang, size, mode), no warm-ups
    reads = reads[~reads["warmup"]]
    first = reads.groupby(["lang", "size", "mode"])["run"].transform("min")
    reads = reads[reads["run"] == first]

    L = []
    L.append("Etapa 1: inferenta doar pe CPU, in Docker pe Mac")
    L.append(f"masina: {load.get('machine')}, {load.get('cpus')} nuclee vizibile in container, "
             f"thread-uri llama.cpp {load.get('threads_llama')}, torch {load.get('threads_torch')}; "
             f"llama-cpp-python {load.get('llama_cpp_python')}, torch {load.get('torch')}")
    L.append("model B: Gemma 4 12B it QAT q4_0 (GGUF Google), 3 prompturi pe cuvant de continut")
    L.append("A: xlmr + labse + e5, un forward pe propozitie; regresorii si fuziunea (milisecunde) nu sunt inclusi")
    L.append("")
    L.append("Timpi pe text (mediana rularilor masurate; B a rulat o data pe text in fiecare mod).")
    L.append("'cu refol.' = KV-ul prefixului comun pastrat intre citiri (modul pentru site, probabilitati")
    L.append("bit-identice cu 'fara refol.' in spike); 'fara refol.' masurat doar la 1 paragraf.")
    if replaced:
        L.append("refacute separat (prima rulare era imediat dupa incarcare): "
                 + ", ".join(f"{lg} {sz} {md}" for lg, sz, md in replaced))
    L.append("")
    hdr = (f"{'limba':11s}{'marime':>7s}{'cuvinte':>9s}{'continut':>10s}{'citiri':>8s}{'segm':>7s}"
           f"{'A':>7s}{'total cu refol.':>17s}{'s/citire':>10s}{'prima prop.':>13s}"
           f"{'fara refol.':>13s}{'s/citire':>10s}")
    L.append(hdr)
    L.append("-" * len(hdr))
    rows = []
    for lg in sorted(set(runs["lang"])):
        for sz in sorted(set(runs[runs["lang"] == lg]["size"])):
            def g(md):
                return t.loc[(lg, sz, md)] if (lg, sz, md) in t.index else None
            ao, ru, nr = g("A-only"), g("reuse"), g("noreuse")
            if ru is None:
                continue
            seg = ao["t_segment"] if ao is not None else ru["t_segment"]
            A = ao["t_A"] if ao is not None else ru["t_A"]
            rows.append(dict(lang=lg, size=sz, words=ru["words"], content=ru["content_words"],
                             readings=ru["readings"], total=ru["total"], spr=ru["s_per_reading"],
                             first=ru["t_first_sentence"],
                             total_nr=nr["total"] if nr is not None else np.nan,
                             spr_nr=nr["s_per_reading"] if nr is not None else np.nan))
            L.append(f"{LANG_NAMES.get(lg, lg):11s}{sz:>7d}{ru['words']:>9.0f}{ru['content_words']:>10.0f}"
                     f"{ru['readings']:>8.0f}{seg:>6.2f}s{A:>6.2f}s{mmss(ru['total']):>17s}"
                     f"{ru['s_per_reading']:>10.2f}{ru['t_first_sentence']:>12.0f}s"
                     f"{mmss(nr['total']) if nr is not None else '-':>13s}"
                     f"{(nr['s_per_reading'] if nr is not None else np.nan):>10.2f}")
    R = pd.DataFrame(rows)
    L.append("")
    for sz in sorted(set(R["size"])):
        r = R[R["size"] == sz]
        L.append(f"{sz} paragraf(e), 11 limbi: total cu refol. median {mmss(r['total'].median())}, "
                 f"min {mmss(r['total'].min())} ({r.loc[r['total'].idxmin(), 'lang']}), "
                 f"max {mmss(r['total'].max())} ({r.loc[r['total'].idxmax(), 'lang']}); "
                 f"cuvinte {r['words'].min():.0f}-{r['words'].max():.0f}, "
                 f"citiri {r['readings'].min():.0f}-{r['readings'].max():.0f}")
    ru = reads[reads["mode"] == "reuse"]
    nr = reads[reads["mode"] == "noreuse"]
    L.append(f"pe toate citirile: cu refol. {ru['seconds'].sum() / len(ru):.2f} s/citire "
             f"({len(ru)} citiri), fara refol. {nr['seconds'].sum() / len(nr):.2f} s/citire "
             f"({len(nr)} citiri); prefill fara refol. "
             f"{nr['n_evaluated'].sum() / nr['seconds'].sum():.1f} tokeni/s, "
             f"{nr['n_tokens'].mean():.0f} tokeni pe prompt in medie; cu refol. se evalueaza "
             f"{ru['n_evaluated'].sum() / ru['n_tokens'].sum():.0%} din tokeni")
    both = R.dropna(subset=["total_nr"])
    if len(both):
        L.append(f"castigul refolosirii la 1 paragraf: {1 - (both['total'] / both['total_nr']).median():.0%} "
                 f"median (intre {1 - (both['total'] / both['total_nr']).max():.0%} si "
                 f"{1 - (both['total'] / both['total_nr']).min():.0%})")
    L.append("")
    L.append("Memorie (GB; anon = memorie proprie, file = pagini mapate din GGUF si safetensors,")
    L.append("pe care kernelul le poate elibera si reciti; VM-ul Docker are 16 GB si 1 GB swap)")

    def md(d):
        return ", ".join(f"{k} {v:.2f}" for k, v in d.items()) if isinstance(d, dict) else str(d)
    L.append(f"  dupa encodere: {md(load.get('mem_after_encoders_gb'))}")
    L.append(f"  dupa Gemma:    {md(load.get('mem_after_gemma_gb'))}")
    st = load.get("mem_stanza_gb", {})
    if st:
        an = {lg: v.get("anon", np.nan) for lg, v in st.items()}
        L.append("  anon dupa incarcarea stanza, pe limba: "
                 + ", ".join(f"{lg} {v:.2f}" for lg, v in an.items()))
    L.append(f"  varf RSS proces: {load.get('peak_rss_gb', float('nan')):.2f}; varf cgroup "
             f"(include page cache): {load.get('cgroup_peak_gb')}")
    L.append(f"  incarcare: encodere {load.get('load_encoders_s', float('nan')):.1f} s, "
             f"Gemma {load.get('load_gemma_s', float('nan')):.1f} s, stanza pe limba "
             + ", ".join(f"{lg} {v:.1f} s" for lg, v in load.get("load_stanza_s", {}).items()))
    out = stem + "_rezumat.txt"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
