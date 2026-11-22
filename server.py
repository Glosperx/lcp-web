"""lcp-web API: the paper's system on raw text, one language at a time.

  GET  /api/languages   the 11 languages, the system's Pearson r on each (B through llama.cpp, as
                        here) and on average, the levels, the hard limit (max_chars, 20000) and per
                        language the length above which the frontend asks for confirmation
                        (warn_chars: 2000, 700 for Japanese, which has ~3 times more content words
                        per character) with an estimate of the time per 1000 characters
  GET  /api/health      "loading" while the models load (~70 s), then "ok" with the active and
                        waiting texts and the GPU's speed: "tok_s" from a fixed probe (3 readings
                        without KV reuse, at start and after every PROBE_IDLE_S idle seconds) and
                        "slow" when it is below SLOW_TOK_S (the model partly paged into shared
                        memory by Windows; ~1000 tokens/s is normal on the RTX 2070 SUPER),
                        plus "last_text_tok_s" of the last finished text (HEAD too, for uptime
                        monitors)
  POST /api/analyze     {"lang": "en", "text": "..."} -> application/x-ndjson, one JSON object per
                        line: optionally {"type": "queued", "position": n}, then "paragraphs", per
                        paragraph "sentences" (its sentence spans) and one "sentence" per finished
                        sentence (its content words with offsets, level, score 0-1, lemma, Zipf
                        frequency, A, B), and "done" with the timings; {"type": "error"} if
                        something fails. Offsets count Unicode code points (Python str indices),
                        not UTF-16 units.

  POST /api/auth        {"code": "..."} -> 200 if the access code is right, 401 if not

One worker thread owns the models (llama.cpp and torch are not used concurrently). Up to
ACTIVE_MAX texts run at once, taking turns sentence by sentence, so a short text is not held up by
a long one; further texts wait in a queue of at most QUEUE_MAX, and one address may have at most
PER_IP_MAX texts running or waiting. A stream that has nothing to say for 15 s sends
{"type": "ping"}. A client that disconnects cancels its text at the next reading. Texts are never
logged. Static files (stage 5) are served from static/ when it exists. A request body larger than
MAX_BODY (256 KiB; 20000 characters take at most ~240 KB of JSON) gets 413 before it is read. If
the models fail to load, the process exits, so that Docker's restart policy starts it again.

Access: with LCP_ACCESS_CODE set, /api/languages and /api/analyze need the header X-Access-Code;
10 wrong codes from one address in 10 minutes block it for the rest of the window. /api/health
stays open. CORS: LCP_CORS_ORIGINS (comma-separated) and LCP_CORS_REGEX (Vercel previews).
The visitor's address is the last entry of X-Forwarded-For, set by Tailscale Funnel; the port is
bound to 127.0.0.1 (docker-compose.yml), so nothing else can reach the server.

  docker compose up -d          (docker-compose.yml, secrets in .env)
Environment: LCP_STANZA_KEEP (stanza pipelines kept in memory, least recently used dropped; default
0 = all nine; the container then uses ~4.2 GB after loading, ~7.4 GB after some use),
LCP_ACTIVE_MAX (6), LCP_QUEUE_MAX (16),
LCP_PER_IP_MAX (2), LCP_ACCESS_CODE, LCP_CORS_ORIGINS, LCP_CORS_REGEX, LCP_PROBE_IDLE_S (600),
LCP_SLOW_TOK_S (700).
"""
import asyncio
import collections
import hmac
import json
import logging
import os
import queue
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

from lcp.pipeline import MAX_CHARS, Cancelled, Pipeline

ACTIVE_MAX = int(os.environ.get("LCP_ACTIVE_MAX", "6"))
QUEUE_MAX = int(os.environ.get("LCP_QUEUE_MAX", "16"))
PER_IP_MAX = int(os.environ.get("LCP_PER_IP_MAX", "2"))
ACCESS_CODE = os.environ.get("LCP_ACCESS_CODE", "")
FAIL_MAX, FAIL_WINDOW = 10, 600              # wrong access codes per address per 10 minutes
PING_S = 15.0
MAX_BODY = 256 * 1024
PROBE_IDLE_S = float(os.environ.get("LCP_PROBE_IDLE_S", "600"))
SLOW_TOK_S = float(os.environ.get("LCP_SLOW_TOK_S", "700"))
CORS_ORIGINS = [o.strip() for o in os.environ.get(
    "LCP_CORS_ORIGINS", "https://lcp-web-static.vercel.app,https://lcp.tail6e4ef5.ts.net,"
    "http://localhost:8000,http://127.0.0.1:8000"
).split(",") if o.strip()]
# Vercel's preview deployments of the project: lcp-web-static-<hash>-<team>.vercel.app
CORS_REGEX = os.environ.get("LCP_CORS_REGEX", r"https://lcp-web-static(-[a-z0-9-]+)?\.vercel\.app")
STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
log = logging.getLogger("lcp")


class Job:
    def __init__(self, lang, text):
        self.lang, self.text = lang, text
        self.events = queue.Queue()
        self.cancel = threading.Event()


class Worker:
    """The single thread that runs the pipeline. Up to ACTIVE_MAX texts are active at once and
    take turns one step at a time (a paragraph's segmentation or one sentence), so a short text
    sent while a long one runs is done in about its own time; further texts wait in a queue."""

    def __init__(self):
        self.pipeline = None
        self.error = None
        self.jobs = queue.Queue()
        self.active = 0
        self.waiting = 0
        self.last_text_tok_s = None
        self.lock = threading.Lock()
        threading.Thread(target=self._run, name="lcp-worker", daemon=True).start()

    def _probe(self):
        try:
            sp = self.pipeline.probe()
            if sp["tok_s"] < SLOW_TOK_S:
                log.warning("GPU slow: %.0f tokens/s in the speed probe (model partly in shared "
                            "GPU memory?)", sp["tok_s"])
        except Exception as e:                       # noqa: BLE001
            log.error("speed probe failed: %s", type(e).__name__)

    def _finish(self, job, ev=None):
        if ev is not None:
            job.events.put(ev)
        job.events.put(None)
        with self.lock:
            self.active -= 1

    def _run(self):
        try:
            self.pipeline = Pipeline(
                stanza_keep=int(os.environ.get("LCP_STANZA_KEEP", "0")),
                preload_stanza=os.environ.get("LCP_PRELOAD_STANZA", "1") == "1")
            log.warning("models loaded in %.1fs %s", self.pipeline.load_seconds["total"],
                        {k: round(v, 1) for k, v in self.pipeline.load_seconds.items()})
        except Exception as e:                       # noqa: BLE001
            self.error = f"{type(e).__name__}: {e}"
            # Docker restarts a container whose process exits, not one that is only unhealthy.
            log.exception("loading the models failed; exiting so that the container restarts")
            logging.shutdown()
            os._exit(1)
        if self.pipeline.speed["tok_s"] < SLOW_TOK_S:
            log.warning("GPU slow: %.0f tokens/s in the speed probe (model partly in shared GPU "
                        "memory?)", self.pipeline.speed["tok_s"])
        turn = collections.deque()

        def admit(block, room=ACTIVE_MAX):
            # Admit waiting texts while fewer than `room` are in `turn` (block only when nothing is
            # running; after PROBE_IDLE_S idle seconds the GPU's speed is measured again).
            while len(turn) < room:
                wait = block and not turn
                try:
                    job = self.jobs.get(block=wait, timeout=PROBE_IDLE_S if wait else None)
                except queue.Empty:
                    if wait:
                        self._probe()
                        continue
                    return
                with self.lock:
                    self.waiting -= 1
                    self.active += 1
                job.gen = self.pipeline.analyze(job.lang, job.text, job.cancel)
                job.t0 = time.perf_counter()
                turn.append(job)

        while True:
            admit(block=True)
            job = turn.popleft()
            if job.cancel.is_set():
                job.gen.close()
                log.warning("analysis cancelled (client gone)")
                self._finish(job)
                continue
            try:
                ev = next(job.gen)
            except StopIteration:
                log.warning("analyzed %s: %d chars in %.1fs", job.lang, len(job.text),
                            time.perf_counter() - job.t0)
                self._finish(job)
                continue
            except Cancelled:
                log.warning("analysis cancelled (client gone)")
                self._finish(job)
                continue
            except Exception as e:                   # noqa: BLE001  (message only, never the text)
                log.error("analysis failed: %s", type(e).__name__)
                self._finish(job, {"type": "error",
                                   "message": f"analysis failed ({type(e).__name__})"})
                continue
            job.events.put(ev)
            if ev.get("type") == "done":
                t = ev.get("timings", {})
                if t.get("B_s"):
                    self.last_text_tok_s = t["evaluated_tokens"] / t["B_s"]
            # Only a scored sentence ends a turn: the paragraph list and a paragraph's
            # segmentation are cheap, so the same text goes on to its next sentence at once.
            if ev.get("type") in ("paragraphs", "sentences"):
                turn.appendleft(job)
            else:
                # a text sent meanwhile goes before this one; this one is out of `turn` now
                admit(block=False, room=ACTIVE_MAX - 1)
                turn.append(job)

    def submit(self, lang, text):
        with self.lock:
            if self.waiting >= QUEUE_MAX:
                return None, None
            ahead = max(0, self.waiting + self.active - ACTIVE_MAX + 1)
            self.waiting += 1
        job = Job(lang, text)
        self.jobs.put(job)
        return job, ahead


W = None


@asynccontextmanager
async def lifespan(app):
    global W
    W = Worker()
    yield


class BodyLimit:
    """413 for a request body over MAX_BODY, before the route reads and parses it (which FastAPI
    does before the access code is checked): by Content-Length at once, and for a chunked body
    as soon as the bytes received pass the limit."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        for k, v in scope["headers"]:
            if k == b"content-length" and (not v.isdigit() or int(v) > MAX_BODY):
                return await JSONResponse({"detail": f"request body over {MAX_BODY} bytes"},
                                          status_code=413)(scope, receive, send)
        seen = 0

        async def limited():
            nonlocal seen
            msg = await receive()
            if msg["type"] == "http.request":
                seen += len(msg.get("body", b""))
                if seen > MAX_BODY:          # FastAPI passes an HTTPException from here through
                    raise HTTPException(413, f"request body over {MAX_BODY} bytes")
            return msg

        return await self.app(scope, limited, send)


app = FastAPI(title="lcp-web", lifespan=lifespan, docs_url=None, redoc_url=None,
              openapi_url=None)
app.add_middleware(BodyLimit)                  # inside CORS, so a 413 still has the CORS headers
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_origin_regex=CORS_REGEX,
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-Access-Code"],
                   max_age=600)


class AnalyzeIn(BaseModel):
    lang: str
    text: str


class AuthIn(BaseModel):
    code: str


def client_ip(request):
    """The visitor's address. The port is bound to 127.0.0.1, so every request comes through the
    tunnel on this machine (Tailscale Funnel), which puts the visitor's address last in
    X-Forwarded-For; earlier entries could be sent by the client and are ignored."""
    xff = request.headers.get("x-forwarded-for", "")
    parts = [x.strip() for x in xff.split(",") if x.strip()]
    return parts[-1] if parts else (request.client.host if request.client else "?")


class Gate:
    """The access code (LCP_ACCESS_CODE; no code = open) with a limit on wrong attempts, and the
    number of texts each address has running or waiting."""

    def __init__(self):
        self.lock = threading.Lock()
        self.fails = {}                 # address -> deque of the times of its recent wrong codes
        self.per_ip = collections.Counter()
        self.swept = time.time()

    def _sweep(self, now):
        """Forget the addresses whose wrong codes are all older than the window (at most once per
        window), so the dictionary does not grow with every address ever seen."""
        if now - self.swept < FAIL_WINDOW:
            return
        self.swept = now
        for ip in [ip for ip, f in self.fails.items() if now - f[-1] > FAIL_WINDOW]:
            del self.fails[ip]

    def check(self, ip, given):
        if not ACCESS_CODE:
            return
        now = time.time()
        with self.lock:
            self._sweep(now)
            f = self.fails.get(ip)
            while f and now - f[0] > FAIL_WINDOW:
                f.popleft()
            if f is not None and not f:
                del self.fails[ip]
            elif f and len(f) >= FAIL_MAX:
                raise HTTPException(429, "too many wrong access codes; try again later")
            if hmac.compare_digest(given.encode("utf-8"), ACCESS_CODE.encode("utf-8")):
                return
            if given:                                # an empty header is not an attempt
                self.fails.setdefault(ip, collections.deque()).append(now)
        raise HTTPException(401, "access code required")

    def acquire(self, ip):
        with self.lock:
            if self.per_ip[ip] >= PER_IP_MAX:
                return False
            self.per_ip[ip] += 1
            return True

    def release(self, ip):
        with self.lock:
            self.per_ip[ip] -= 1
            if self.per_ip[ip] <= 0:
                del self.per_ip[ip]


G = Gate()


def _ready():
    if W.error:
        raise HTTPException(500, "the models failed to load")
    if W.pipeline is None:
        raise HTTPException(503, "the models are still loading")
    return W.pipeline


@app.api_route("/api/health", methods=["GET", "HEAD"])  # HEAD: uptime monitors
def health():
    if W.error:
        return JSONResponse({"status": "error"}, status_code=500)
    if W.pipeline is None:
        return JSONResponse({"status": "loading"}, status_code=503)
    sp = W.pipeline.speed
    return {"status": "ok", "active": W.active, "waiting": W.waiting,
            "access_code": bool(ACCESS_CODE), "tok_s": round(sp["tok_s"]),
            "slow": sp["tok_s"] < SLOW_TOK_S, "probe_age_s": round(time.time() - sp["at"]),
            "last_text_tok_s": None if W.last_text_tok_s is None else round(W.last_text_tok_s)}


@app.post("/api/auth")
def auth(body: AuthIn, request: Request):
    """Checks an access code (the frontend asks for it once and then sends it as X-Access-Code)."""
    G.check(client_ip(request), body.code)
    return {"ok": True}


@app.get("/api/languages")
def languages(request: Request):
    G.check(client_ip(request), request.headers.get("x-access-code", ""))
    return _ready().languages()


@app.post("/api/analyze")
async def analyze(body: AnalyzeIn, request: Request):
    G.check(client_ip(request), request.headers.get("x-access-code", ""))
    p = _ready()
    if body.lang not in p.langs:
        raise HTTPException(400, f"unsupported language; one of {p.langs}")
    text = body.text
    if not text.strip():
        raise HTTPException(400, "empty text")
    if len(text) > MAX_CHARS:
        raise HTTPException(413, f"text longer than {MAX_CHARS} characters ({len(text)})")
    ip = client_ip(request)
    if not G.acquire(ip):
        raise HTTPException(429, f"at most {PER_IP_MAX} texts at once from one address")
    job, ahead = W.submit(body.lang, text)
    if job is None:
        G.release(ip)
        raise HTTPException(503, "too many texts waiting; try again in a minute")

    def next_event():
        # A ping when nothing happened for PING_S seconds: the tunnel and browsers may close a
        # connection that stays silent, and a queued text can wait longer than that.
        try:
            return job.events.get(timeout=PING_S)
        except queue.Empty:
            return {"type": "ping"}

    async def stream():
        try:
            if ahead:
                yield json.dumps({"type": "queued", "position": ahead}) + "\n"
            while True:
                ev = await asyncio.to_thread(next_event)
                if ev is None:
                    break
                yield json.dumps(ev, ensure_ascii=False) + "\n"
        finally:
            job.cancel.set()                         # no-op if the text is finished
            G.release(ip)

    return StreamingResponse(stream(), media_type="application/x-ndjson",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


if os.path.isdir(STATIC):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
else:
    @app.get("/", response_class=HTMLResponse)
    def root():
        return ("<!doctype html><meta charset=utf-8><title>lcp-web API</title>"
                "<p>lcp-web API. Status: <a href=/api/health>/api/health</a>.</p>")
