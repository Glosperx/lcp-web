"""Stage 4 check of the running API (server.py), standard library only (runs on the host).

  1. /api/health until "ok", then /api/languages: 11 languages with r, warn_chars, estimates;
  2. errors: unknown language 400, empty text 400, one character over max_chars (20000) 413;
  3. every benchmark text (bench/texts, 1 and 2 paragraphs, 11 languages) through POST /api/analyze,
     one at a time: the stream must be "paragraphs", per paragraph "sentences" then its "sentence"
     events in order, then "done"; every word's offsets must point at its text in the input,
     level in 1..5, score in [0, 1]. Timings from the server and the client, next to the stage 7
     benchmark (same texts, reuse);
  4. a single sentence without sentence ends (a benchmark text repeated) in ja (1000 characters)
     and si (~1990), longer than the 192 tokens of a piece: it must come back in pieces, its
     words flagged `cropped`;
  5. interleaving: a multi-paragraph English text of ~5100 characters runs; meanwhile a short text
     and a 1-paragraph text are sent and must finish in about their own time (each sentence of the
     long text is one turn), while the long one goes on and completes with every paragraph;
  6. queue: 7 texts at once; with LCP_ACTIVE_MAX 6 the last gets {"type": "queued"} first;
  7. cancel: a client that disconnects after its first sentence leaves no active text behind.
Writes bench/results/api_check.txt and api_check.csv. Prints no text from the inputs.

  python scripts/api_check.py --url http://localhost:8000
"""
import argparse
import csv
import json
import os
import re
import threading
import time
import urllib.error
import urllib.request

LOG = []
FAILS = []
PARTS = ["access", "texts", "long", "interleave", "queue", "cancel"]


def say(msg=""):
    print(msg, flush=True)
    LOG.append(msg)


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        say(f"  [FAIL] {msg}")
    return cond


HEADERS = {}                     # X-Access-Code when --code is given


def get(url, headers=None):
    req = urllib.request.Request(url, headers={**HEADERS, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


def post(url, body, headers=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", **HEADERS,
                                          **(headers or {})})
    return urllib.request.urlopen(req, timeout=900)


def status_of(url, body=None, headers=None, method=None):
    try:
        if method == "GET":
            return get(url, headers)[0]
        with post(url, body, headers) as r:
            r.read()
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def analyze(url, lang, text, stop_after_first=False, headers=None):
    """(events, client timings). Reads the NDJSON stream line by line."""
    t0 = time.perf_counter()
    ev, t_first = [], None
    with post(url + "/api/analyze", {"lang": lang, "text": text}, headers) as r:
        for line in r:
            e = json.loads(line.decode("utf-8"))
            ev.append(e)
            if e["type"] == "sentence" and e["words"] and t_first is None:
                t_first = time.perf_counter() - t0
                if stop_after_first:
                    break
    return ev, {"client_total_s": time.perf_counter() - t0, "client_first_s": t_first}


def validate(lang, text, ev):
    evs = [e for e in ev if e["type"] not in ("queued", "ping")]
    if not check(evs and evs[0]["type"] == "paragraphs" and evs[-1]["type"] == "done",
                 f"{lang}: stream must start with paragraphs and end with done"):
        return False
    n_par = len(evs[0]["paragraphs"])
    expect, nxt_i, par_seen = [], 0, []
    for e in evs[1:-1]:
        if e["type"] == "sentences":
            par_seen.append(e["paragraph"])
            if not check(not expect, f"{lang}: new paragraph before the previous one finished"):
                return False
            expect = [s["i"] for s in e["sentences"]]
        elif e["type"] == "sentence":
            if not check(expect and e["i"] == expect[0] == nxt_i,
                         f"{lang}: sentence {e['i']} out of order"):
                return False
            expect.pop(0)
            nxt_i += 1
            for w in e["words"]:
                if not (check(text[w["start"]:w["end"]] == w["text"], f"{lang}: word offsets")
                        and check(1 <= w["level"] <= 5 and (w.get("function") and w["level"] == 1
                                                            or 0.0 <= w["score"] <= 1.0),
                                  f"{lang}: level/score out of range")):
                    return False
        else:
            check(False, f"{lang}: unexpected event {e['type']}")
            return False
    return (check(par_seen == list(range(n_par)), f"{lang}: paragraphs {par_seen} of {n_par}")
            and check(evs[-1]["sentences"] == nxt_i, f"{lang}: sentence count"))


def stage7(path):
    """{(lang, size): total_s} of the stage 7 GPU benchmark, mode reuse."""
    out = {}
    if not os.path.exists(path):
        return out
    for ln in open(path, encoding="utf-8"):
        p = ln.split()
        if len(p) > 12 and p[2] == "reuse":               # column 11: total_s
            out[(p[0], int(p[1]))] = float(p[11])
    return out


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--texts", default="bench/texts")
    ap.add_argument("--sizes", nargs="+", type=int, default=[1, 2])
    ap.add_argument("--out", default="bench/results/api_check")
    ap.add_argument("--parts", nargs="+", default=PARTS, choices=PARTS)
    ap.add_argument("--code", default=os.environ.get("LCP_ACCESS_CODE", ""),
                    help="access code (default: the environment variable LCP_ACCESS_CODE)")
    a = ap.parse_args()
    U = a.url.rstrip("/")
    if a.code:
        HEADERS["X-Access-Code"] = a.code
    T = lambda lg, sz: read(os.path.join(a.texts, f"{lg}_{sz}.txt"))      # noqa: E731

    # ------------------------------------------------------------ 1. health, languages
    t0 = time.time()
    while True:
        try:
            st, h = get(U + "/api/health")
            if h.get("status") == "ok":
                break
        except (urllib.error.URLError, ConnectionError, OSError):
            pass
        if time.time() - t0 > 300:
            raise SystemExit("server not ready after 300 s")
        time.sleep(2)
    say(f"[api] health ok after {time.time() - t0:.0f}s of waiting")
    _, L = get(U + "/api/languages")
    langs = [x["code"] for x in L["languages"]]
    check(len(langs) == 11, f"{len(langs)} languages")
    say("[api] languages: " + "  ".join(
        f"{x['code']} r {x['r']:.3f} warn {x['warn_chars']} ~{x['est_s_per_1000_chars']}s/1000"
        for x in L["languages"]) + f" | mean {L['mean_r']} (paper {L['paper_mean_r']}), "
        f"max_chars {L['max_chars']}")

    # ------------------------------------------------------------ 2. errors
    e1 = status_of(U + "/api/analyze", {"lang": "xx", "text": "abc"})
    e2 = status_of(U + "/api/analyze", {"lang": "en", "text": "   "})
    e3 = status_of(U + "/api/analyze", {"lang": "ja", "text": "あ" * (L["max_chars"] + 1)})
    say(f"[api] errors: unknown language {e1}, empty {e2}, {L['max_chars'] + 1} chars {e3}")
    check((e1, e2, e3) == (400, 400, 413), "error codes")
    if "access" in a.parts:
        access_test(U, h)

    # ------------------------------------------------------------ 3. benchmark texts
    ref = stage7("bench/results/gpu_docker_pc_summary.txt")
    rows, solo = [], {}
    for sz in (a.sizes if "texts" in a.parts else []):
        for lg in langs:
            text = T(lg, sz)
            ev, cl = analyze(U, lg, text)
            if not validate(lg, text, ev):
                continue
            done = ev[-1]
            t = done["timings"]
            lv = [w["level"] for e in ev if e["type"] == "sentence" for w in e["words"]
                  if not w.get("function")]                 # content words only, as before
            row = dict(lang=lg, size=sz, chars=len(text), paragraphs=done["paragraphs"],
                       sentences=done["sentences"], content_words=done["content_words"],
                       function_words=done.get("function_words"),
                       readings=t["readings"], cropped=done["cropped"],
                       stanza_loaded=t["stanza_loaded"], segment_s=t["segment_s"], A_s=t["A_s"],
                       B_s=t["B_s"], total_s=t["total_s"], first_s=t["first_sentence_s"],
                       s_per_reading=t["s_per_reading"],
                       client_first_s=round(cl["client_first_s"], 3),
                       client_total_s=round(cl["client_total_s"], 3),
                       stage7_total_s=ref.get((lg, sz)),
                       s_per_1000_chars=round(1000 * t["total_s"] / len(text), 1),
                       levels="/".join(str(lv.count(k)) for k in range(1, 6)))
            rows.append(row)
            solo[(lg, sz)] = row["client_total_s"]
            say(f"[api] {lg} {sz}: {row['chars']} chars, {row['paragraphs']} par., "
                f"{row['content_words']} words, {row['readings']} readings, total "
                f"{row['total_s']:.1f}s (stage 7 {row['stage7_total_s']}), first sentence "
                f"{row['first_s']}s, {row['s_per_reading']}s/reading, seg {row['segment_s']}s"
                f"{' incl. stanza load' if row['stanza_loaded'] else ''}, A {row['A_s']}s, "
                f"{row['s_per_1000_chars']}s/1000 chars, levels {row['levels']}")
    if rows:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    for sz in a.sizes:
        rs = sorted(r["total_s"] for r in rows if r["size"] == sz)
        r7 = sorted(r["stage7_total_s"] for r in rows if r["size"] == sz and r["stage7_total_s"])
        if rs:
            say(f"[api] size {sz}: median total {rs[len(rs) // 2]:.1f}s over {len(rs)} languages"
                + (f" (stage 7 median {r7[len(r7) // 2]:.1f}s)" if r7 else ""))

    # ------------------------------------------------------------ 4. long sentence, pieces
    for lg, n in ((("ja", 1000), ("si", 1990)) if "long" in a.parts else ()):
        t = re.sub(r"[.!?。！？…\n]+", " ", T(lg, 2)).strip()
        while len(t) < n:
            t = t + " " + t
        t = t[:n].rsplit(" ", 1)[0] if lg == "si" else t[:n]
        ev, cl = analyze(U, lg, t)
        ok = validate(lg, t, ev)
        done = ev[-1]
        say(f"[api] long {lg}: {len(t)} chars, {done.get('sentences')} pieces, "
            f"{done.get('content_words')} words, cropped {done.get('cropped')}, total "
            f"{done['timings']['total_s']:.1f}s, {done['timings']['s_per_reading']}s/reading, "
            f"first piece after {cl['client_first_s']:.1f}s")
        check(ok and done.get("cropped", 0) > 0 and done["sentences"] > 1,
              f"long {lg}: not split into pieces")

    # ------------------------------------------------------------ 5. interleaving
    if ("en", 1) not in solo and {"interleave", "queue"} & set(a.parts):
        solo[("en", 1)] = analyze(U, "en", T("en", 1))[1]["client_total_s"]
    res = {}

    def run(key, lang, text, ip=None):
        res[key] = analyze(U, lang, text, headers={"X-Forwarded-For": ip} if ip else None)

    if "interleave" in a.parts:
        interleave(U, T, solo, res, run)
    if "queue" in a.parts:
        queue_test(T, res, run)
    if "cancel" in a.parts:
        cancel_test(U, T)
    finish(a)


def access_test(U, h):
    """Access code, wrong-code limit, CORS, at most 2 texts per address."""
    if not h.get("access_code"):
        say("[api] access: no access code configured on the server, skipped")
        return
    nobody = {"X-Access-Code": ""}
    a1 = status_of(U + "/api/languages", headers=nobody, method="GET")
    a2 = status_of(U + "/api/analyze", {"lang": "en", "text": "A test."}, headers=nobody)
    a3 = status_of(U + "/api/languages", headers={"X-Access-Code": "wrong"}, method="GET")
    a4 = status_of(U + "/api/auth", {"code": HEADERS.get("X-Access-Code", "")}, headers=nobody)
    a5 = status_of(U + "/api/health", headers=nobody, method="GET")
    say(f"[api] access: no code languages {a1} analyze {a2}, wrong code {a3}, /api/auth with the "
        f"right code {a4}, health without code {a5}")
    check((a1, a2, a3, a4, a5) == (401, 401, 401, 200, 200), "access codes")
    # 10 wrong codes from one (simulated) address block it; another address is not affected
    bad = {"X-Access-Code": "wrong", "X-Forwarded-For": "198.51.100.66"}
    codes = [status_of(U + "/api/languages", headers=bad, method="GET") for _ in range(11)]
    other = status_of(U + "/api/languages", headers={"X-Forwarded-For": "198.51.100.67"},
                      method="GET")
    right_blocked = status_of(U + "/api/languages", headers={"X-Forwarded-For": "198.51.100.66"},
                              method="GET")
    say(f"[api] access: 11 wrong codes from one address -> {codes}; right code from that address "
        f"{right_blocked}, from another {other}")
    check(codes[:10] == [401] * 10 and codes[10] == 429 and right_blocked == 429 and other == 200,
          "wrong-code limit")

    def preflight(origin):
        req = urllib.request.Request(U + "/api/analyze", method="OPTIONS", headers={
            "Origin": origin, "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-access-code"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.headers.get("access-control-allow-origin")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("access-control-allow-origin")
    c1 = preflight("https://lcp-web-static.vercel.app")
    c2 = preflight("https://lcp-web-static-abc123-glosperx.vercel.app")
    c3 = preflight("https://evil.example")
    c4 = preflight("https://lcp-web-static.vercel.app.evil.example")
    say(f"[api] cors: lcp-web-static.vercel.app {c1}, a preview deployment {c2}, another origin "
        f"{c3}, the site's name as a prefix {c4}")
    check(c1 == (200, "https://lcp-web-static.vercel.app")
          and c2[1] == "https://lcp-web-static-abc123-glosperx.vercel.app" and c3[1] is None
          and c4[1] is None, "cors")
    # at most 2 texts at once from one address
    ip = {"X-Forwarded-For": "198.51.100.70"}
    res = {}

    def run(k):
        try:
            res[k] = analyze(U, "en", read("bench/texts/en_1.txt"), headers=ip)
        except urllib.error.HTTPError as e:
            res[k] = e.code
    ths = [threading.Thread(target=run, args=(k,)) for k in range(2)]
    for th in ths:
        th.start()
    time.sleep(1.5)
    third = status_of(U + "/api/analyze", {"lang": "en", "text": "A test."}, headers=ip)
    for th in ths:
        th.join()
    after = status_of(U + "/api/analyze", {"lang": "en", "text": "A test."}, headers=ip)
    say(f"[api] per address: third text while two run -> {third}; after they finish -> {after}")
    check(third == 429 and after == 200 and all(isinstance(res[k], tuple) for k in res),
          "per-address limit")


def interleave(U, T, solo, res, run):
    big = "\n\n".join([T("en", 2), T("en", 1)] * 3)
    th = threading.Thread(target=run, args=("big", "en", big, "198.51.100.30"))
    th.start()
    time.sleep(4.0)
    ev_s, cl_s = analyze(U, "en", "The committee postponed the ratification of the treaty.")
    ev_p, cl_p = analyze(U, "en", T("en", 1))
    big_running = th.is_alive()
    th.join()
    ev_b, cl_b = res["big"]
    ok_b = validate("en big", big, ev_b)
    say(f"[api] interleave: long text {len(big)} chars, {ev_b[-1].get('paragraphs')} paragraphs, "
        f"{ev_b[-1].get('content_words')} words, done in {cl_b['client_total_s']:.1f}s "
        f"(server {ev_b[-1]['timings']['total_s']:.1f}s); meanwhile a short text took "
        f"{cl_s['client_total_s']:.1f}s and en 1 paragraph {cl_p['client_total_s']:.1f}s "
        f"(alone {solo.get(('en', 1), float('nan')):.1f}s); long text still running then: "
        f"{big_running}")
    check(ok_b and validate("en short", "The committee postponed the ratification of the treaty.",
                            ev_s) and validate("en 1", T("en", 1), ev_p), "interleave: streams")
    check(big_running and cl_s["client_total_s"] < 10
          and cl_p["client_total_s"] < 3 * solo.get(("en", 1), 15), "interleave: texts held up")


def queue_test(T, res, run):
    ths = [threading.Thread(target=run, args=(k, "en", T("en", 1), f"198.51.100.{10 + k}"))
           for k in range(7)]
    for k, th in enumerate(ths):
        th.start()
        time.sleep(0.3)
    for th in ths:
        th.join()
    queued = [k for k in range(7) if res[k][0][0]["type"] == "queued"]
    tt = [round(res[k][1]["client_total_s"], 1) for k in range(7)]
    say(f"[api] queue: 7 texts at once, queued {queued} "
        f"(positions {[res[k][0][0].get('position') for k in queued]}), client times {tt}s")
    pings = sum(1 for e in res[6][0] if e["type"] == "ping")
    say(f"[api] queue: the queued text got {pings} ping(s) while waiting")
    check(queued == [6] and all(validate("en q", T("en", 1), res[k][0]) for k in range(7)),
          "queue: expected only the 7th text queued")
    check(pings > 0, "queue: no ping while waiting")


def cancel_test(U, T):
    ev, cl = analyze(U, "ca", T("ca", 2), stop_after_first=True)
    t0 = time.perf_counter()
    active = None
    while time.perf_counter() - t0 < 20:
        _, h = get(U + "/api/health")
        active = h["active"]
        if active == 0 and h["waiting"] == 0:
            break
        time.sleep(0.5)
    say(f"[api] cancel: disconnected after the first sentence ({cl['client_first_s']:.1f}s); "
        f"active texts back to {active} after {time.perf_counter() - t0:.1f}s")
    check(active == 0, "cancel: the text kept running")


def finish(a):
    say(f"\n[api] {'PASS' if not FAILS else 'FAIL: ' + '; '.join(FAILS)}")
    with open(a.out + ".txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(LOG) + "\n")
    print(f"-> {a.out}.txt, {a.out}.csv")
    if FAILS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
