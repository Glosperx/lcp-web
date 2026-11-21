"""Benchmark texts: the first paragraph and the first two paragraphs of one Wikipedia article, in
the 11 languages (Filipino from tl.wikipedia).

The article is the first of CANDIDATES (Wikidata items, fixed order) whose first paragraph and first
two paragraphs have a usable length in every language, so all languages get the same article
(--pick forces one; the languages outside the ranges are then recorded in sources.json):
  space-delimited languages: 50-200 words in paragraph 1, 120-400 in paragraphs 1+2 (target ~100
  and ~200); Japanese: 100-500 characters and 250-1000 characters.
Paragraphs are the lines of the article's plain-text extract, skipping section headings and any line
under 40 characters (so the second paragraph may come from the first section when the lead has one).

Writes bench/texts/{lang}_1.txt, {lang}_2.txt and bench/texts/sources.json (title, permanent link
to the revision used, licence). Wikipedia text is CC BY-SA 4.0; see bench/texts/README.md.
Standard library only, runs on the host:  python3 scripts/fetch_texts.py
"""
import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

LANGS = ("ca", "de", "en", "es", "fil", "fr", "it", "ja", "pt", "ro", "si")
WIKI = {lg: ("tl" if lg == "fil" else lg) for lg in LANGS}
# water, Sun, Moon, Earth, rice, coffee, tree, bread, tea, honey, elephant, cat, dog, horse,
# association football (none passes, 21 Nov), then physics, chemistry, biology, mathematics,
# science, linguistics, language, Paris, Rome, Berlin, London, Tokyo
CANDIDATES = ("Q283", "Q525", "Q405", "Q2", "Q5090", "Q8486", "Q10884", "Q7802", "Q6097",
              "Q10987", "Q7378", "Q146", "Q144", "Q726", "Q2736",
              "Q413", "Q2329", "Q420", "Q395", "Q336", "Q8162", "Q315", "Q90", "Q220", "Q64",
              "Q84", "Q1490")
UA = "lcp-web-bench/0.1 (research benchmark script)"
LICENSE = "CC BY-SA 4.0"


def get(url, params):
    q = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(q, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if attempt == 5 or e.code not in (429, 500, 502, 503, 504):
                raise
            wait = e.headers.get("Retry-After")
            time.sleep(float(wait) if wait and wait.isdigit() else 5 * 2 ** attempt)
        except OSError:
            if attempt == 5:
                raise
            time.sleep(5 * 2 ** attempt)


def sitelinks(qid):
    d = get("https://www.wikidata.org/w/api.php",
            {"action": "wbgetentities", "ids": qid, "props": "sitelinks", "format": "json"})
    sl = d["entities"][qid].get("sitelinks", {})
    return {lg: sl[f"{WIKI[lg]}wiki"]["title"] for lg in LANGS if f"{WIKI[lg]}wiki" in sl}


def article(lg, title):
    w = WIKI[lg]
    d = get(f"https://{w}.wikipedia.org/w/api.php",
            {"action": "query", "prop": "extracts|revisions", "explaintext": 1,
             "exsectionformat": "wiki", "rvprop": "ids|timestamp", "redirects": 1,
             "titles": title, "format": "json", "formatversion": 2})
    page = d["query"]["pages"][0]
    paras = [ln.strip() for ln in page.get("extract", "").split("\n")]
    paras = [p for p in paras if p and not p.startswith("=") and len(p) >= 40]
    rev = page["revisions"][0]
    return dict(wiki=f"{w}.wikipedia.org", title=page["title"],
                url=f"https://{w}.wikipedia.org/wiki/{urllib.parse.quote(page['title'].replace(' ', '_'))}",
                oldid=rev["revid"], timestamp=rev["timestamp"],
                permalink=f"https://{w}.wikipedia.org/w/index.php?oldid={rev['revid']}",
                paragraphs=paras[:2])


def size(lg, text):
    return len(text) if lg == "ja" else len(text.split())


def usable(lg, p):
    if len(p) < 2:
        return False
    a, b = size(lg, p[0]), size(lg, p[0] + " " + p[1])
    if lg == "ja":
        return 100 <= a <= 500 and 250 <= b <= 1000
    return 50 <= a <= 200 and 120 <= b <= 400


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="bench/texts")
    ap.add_argument("--start", default=None, help="skip the candidates before this one")
    ap.add_argument("--pick", default=None,
                    help="take this candidate even if some languages are outside the ranges "
                         "(recorded in sources.json)")
    a = ap.parse_args()
    chosen = None
    cands = ((a.pick,) if a.pick else
             CANDIDATES[CANDIDATES.index(a.start):] if a.start else CANDIDATES)
    for qid in cands:
        links = sitelinks(qid)
        if len(links) < len(LANGS):
            print(f"{qid} {links.get('en', '?')}: missing in {sorted(set(LANGS) - set(links))}")
            continue
        arts = {}
        for lg in LANGS:
            arts[lg] = article(lg, links[lg])
            time.sleep(1.0)
        report = "  ".join(
            f"{lg} " + "/".join(str(size(lg, " ".join(arts[lg]["paragraphs"][:k])))
                                for k in (1, 2))
            + ("" if usable(lg, arts[lg]["paragraphs"]) else "!")
            for lg in LANGS)
        print(f"{qid} {links['en']}: {report}", flush=True)
        if a.pick or all(usable(lg, arts[lg]["paragraphs"]) for lg in LANGS):
            chosen = (qid, arts)
            break
    if chosen is None:
        raise SystemExit("no candidate article has usable paragraphs in all 11 languages")

    qid, arts = chosen
    os.makedirs(a.out, exist_ok=True)
    meta = {"wikidata": qid, "license": LICENSE,
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "fetched": time.strftime("%Y-%m-%d"),
            "selection": ("first of CANDIDATES within the ranges in every language" if not a.pick
                          else f"--pick {a.pick}: no candidate was within the ranges in all 11 "
                               "languages; this one was the closest"),
            "outside_ranges": [lg for lg in LANGS if not usable(lg, arts[lg]["paragraphs"])],
            "texts": {}}
    for lg in LANGS:
        p = arts[lg]["paragraphs"]
        for k in (1, 2):
            with open(os.path.join(a.out, f"{lg}_{k}.txt"), "w", encoding="utf-8") as fh:
                fh.write("\n\n".join(p[:k]) + "\n")
        meta["texts"][lg] = {kk: v for kk, v in arts[lg].items() if kk != "paragraphs"} | {
            "size_1": size(lg, p[0]), "size_2": size(lg, p[0] + " " + p[1]),
            "size_unit": "characters" if lg == "ja" else "words"}
    with open(os.path.join(a.out, "sources.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Benchmark texts\n\nThe first paragraph (`{{lang}}_1.txt`) and the first two "
                 f"paragraphs (`{{lang}}_2.txt`) of the Wikipedia article for Wikidata item "
                 f"{qid} ({arts['en']['title']}) in each language, from the revisions linked "
                 f"below, as plain text. Text from Wikipedia, licensed under {LICENSE} "
                 f"(https://creativecommons.org/licenses/by-sa/4.0/); authors are listed in each "
                 f"article's history.\n\n")
        for lg in LANGS:
            m = meta["texts"][lg]
            fh.write(f"- {lg}: \"{m['title']}\", {m['wiki']}, revision {m['oldid']} "
                     f"({m['timestamp']}): {m['permalink']}\n")
    print(f"-> {a.out}: article {qid} ({arts['en']['title']})")


if __name__ == "__main__":
    main()
