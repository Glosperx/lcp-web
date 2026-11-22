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

One worker thread owns the models (llama.cpp and torch are not used concurrently). Up to
ACTIVE_MAX texts run at once, taking turns sentence by sentence, so a short text is not held up by
a long one; further texts wait in a queue of at most QUEUE_MAX. A client that disconnects cancels
its text at the next reading. Texts are never logged. Static files (stage 5) are served from
static/ when it exists.

  docker run ... uvicorn server:app --host 0.0.0.0 --port 8000
Environment: LCP_STANZA_KEEP (stanza pipelines kept in memory, least recently used dropped; default
0 = all nine, ~7.2 GB for the container in all), LCP_ACTIVE_MAX (6), LCP_QUEUE_MAX (16).
"""
import asyncio
import collections
import json
import logging
import os
import queue
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from lcp.pipeline import MAX_CHARS, Cancelled, Pipeline

ACTIVE_MAX = int(os.environ.get("LCP_ACTIVE_MAX", "6"))
QUEUE_MAX = int(os.environ.get("LCP_QUEUE_MAX", "16"))
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
            self.pipeline = Pipeline(stanza_keep=int(os.environ.get("LCP_STANZA_KEEP", "0")))
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


class AnalyzeIn(BaseModel):
    lang: str
    text: str


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
    return {"status": "ok", "active": W.active, "waiting": W.waiting}


@app.get("/api/languages")
def languages():
    return _ready().languages()


@app.post("/api/analyze")
async def analyze(body: AnalyzeIn):
    p = _ready()
    if body.lang not in p.langs:
        raise HTTPException(400, f"unsupported language; one of {p.langs}")
    text = body.text
    if not text.strip():
        raise HTTPException(400, "empty text")
    if len(text) > MAX_CHARS:
        raise HTTPException(413, f"text longer than {MAX_CHARS} characters ({len(text)})")
    job, ahead = W.submit(body.lang, text)
    if job is None:
        raise HTTPException(503, "too many texts waiting; try again in a minute")

    async def stream():
        try:
            if ahead:
                yield json.dumps({"type": "queued", "position": ahead}) + "\n"
            while True:
                ev = await asyncio.to_thread(job.events.get)
                if ev is None:
                    break
                yield json.dumps(ev, ensure_ascii=False) + "\n"
        finally:
            job.cancel.set()                         # no-op if the text is finished

    return StreamingResponse(stream(), media_type="application/x-ndjson",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


if os.path.isdir(STATIC):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
