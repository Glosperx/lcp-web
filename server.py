"""lcp-web API: the paper's system on raw text, one language at a time.

  GET  /api/languages   the 11 languages, the system's Pearson r on each (B through llama.cpp, as
                        here) and on average, the levels, the hard limit (max_chars, 20000) and per
                        language the length above which the frontend asks for confirmation
                        (warn_chars: 2000, 700 for Japanese, which has ~3 times more content words
                        per character) with an estimate of the time per 1000 characters
  GET  /api/health      "loading" while the models load (~40 s), then "ok" with the active and
                        waiting texts
  POST /api/analyze     {"lang": "en", "text": "..."} -> application/x-ndjson, one JSON object per
                        line: optionally {"type": "queued", "position": n}, then "paragraphs", per
                        paragraph "sentences" (its sentence spans) and one "sentence" per finished
                        sentence (its content words with offsets, level, score 0-1, lemma, Zipf
                        frequency, A, B), and "done" with the timings; {"type": "error"} if
                        something fails.

  POST /api/auth        {"code": "..."} -> 200 if the access code is right, 401 if not

One worker thread owns the models (llama.cpp and torch are not used concurrently). Up to
ACTIVE_MAX texts run at once, taking turns sentence by sentence, so a short text is not held up by
a long one; further texts wait in a queue of at most QUEUE_MAX, and one address may have at most
PER_IP_MAX texts running or waiting. A stream that has nothing to say for 15 s sends
{"type": "ping"}. A client that disconnects cancels its text at the next reading. Texts are never
logged. Static files (stage 5) are served from static/ when it exists.

Access: with LCP_ACCESS_CODE set, /api/languages and /api/analyze need the header X-Access-Code;
10 wrong codes from one address in 10 minutes block it for the rest of the window. /api/health
stays open. CORS: LCP_CORS_ORIGINS (comma-separated) and LCP_CORS_REGEX (Vercel previews).
The visitor's address is the last entry of X-Forwarded-For, set by Tailscale Funnel; the port is
bound to 127.0.0.1 (docker-compose.yml), so nothing else can reach the server.

  docker compose up -d          (docker-compose.yml, secrets in .env)
Environment: LCP_STANZA_KEEP (stanza pipelines kept in memory, least recently used dropped; default
0 = all nine, ~7.2 GB for the container in all), LCP_ACTIVE_MAX (6), LCP_QUEUE_MAX (16),
LCP_PER_IP_MAX (2), LCP_ACCESS_CODE, LCP_CORS_ORIGINS, LCP_CORS_REGEX.
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
        self.lock = threading.Lock()
        threading.Thread(target=self._run, name="lcp-worker", daemon=True).start()

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
            log.exception("loading the models failed")
            return
        turn = collections.deque()

        def admit(block):
            # admit waiting texts while there is room (block only when nothing is running)
            while len(turn) < ACTIVE_MAX:
                try:
                    job = self.jobs.get(block=block and not turn)
                except queue.Empty:
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
            # Only a scored sentence ends a turn: the paragraph list and a paragraph's
            # segmentation are cheap, so the same text goes on to its next sentence at once.
            if ev.get("type") in ("paragraphs", "sentences"):
                turn.appendleft(job)
            else:
                admit(block=False)                   # a text sent meanwhile goes before this one
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


app = FastAPI(title="lcp-web", lifespan=lifespan, docs_url=None, redoc_url=None)
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
        self.fails = collections.defaultdict(collections.deque)
        self.per_ip = collections.Counter()

    def check(self, ip, given):
        if not ACCESS_CODE:
            return
        now = time.time()
        with self.lock:
            f = self.fails[ip]
            while f and now - f[0] > FAIL_WINDOW:
                f.popleft()
            if len(f) >= FAIL_MAX:
                raise HTTPException(429, "too many wrong access codes; try again later")
            if hmac.compare_digest(given.encode("utf-8"), ACCESS_CODE.encode("utf-8")):
                return
            if given:                                # an empty header is not an attempt
                f.append(now)
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


@app.get("/api/health")
def health():
    if W.error:
        return JSONResponse({"status": "error"}, status_code=500)
    if W.pipeline is None:
        return JSONResponse({"status": "loading"}, status_code=503)
    return {"status": "ok", "active": W.active, "waiting": W.waiting,
            "access_code": bool(ACCESS_CODE)}


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
