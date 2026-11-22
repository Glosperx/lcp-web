// lcp-web: the page. Plain JavaScript, no build, no dependencies.
//
// The API (server.py) runs on the PC's GPU behind Tailscale Funnel. The page is hosted on Vercel
// and also served by the server itself; served from the server it talks to its own origin.
//
// Protocol (POST /api/analyze, application/x-ndjson, one JSON object per line): optionally
// "queued", "ping" (ignored), "paragraphs", per paragraph "sentences", one "sentence" per finished
// sentence (its words), "done", or "error". A stream that ends without "done" or "error" was cut.
// Offsets count Unicode code points (Python string indices); they are converted to UTF-16 indices
// once per text (cpMap), otherwise every emoji would shift what follows it.
"use strict";
(() => {
const PUBLIC_API = "https://lcp.tail6e4ef5.ts.net";
const API = /^(localhost|127\.0\.0\.1|lcp\.tail6e4ef5\.ts\.net)$/.test(location.hostname)
  && location.protocol.startsWith("http") ? "" : PUBLIC_API;

// ------------------------------------------------------------------------------ storage
const store = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  del(k) { try { localStorage.removeItem(k); } catch (e) { /* private mode */ } },
};

// ------------------------------------------------------------------------------ text
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c =>
  ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
// The API counts characters as code points; JavaScript strings count UTF-16 units.
const cpLen = s => { let n = 0; for (const _ of s) n++; return n; };
function cpMap(text) {                 // cpMap(text)[i] = UTF-16 index of code point i
  const m = [0];
  let u = 0;
  for (const ch of text) { u += ch.length; m.push(u); }
  return m;
}

// ------------------------------------------------------------------------------ strings
// Romanian plural: "1 cuvânt", "2 cuvinte", "20 de cuvinte" ("de" from 20, and after 100, 200...).
const roDe = n => n !== 0 && (n % 100 === 0 || n % 100 >= 20);
const roN = (n, one, many) => n === 1 ? `1 ${one}` : `${fmtInt(n)} ${roDe(n) ? "de " : ""}${many}`;
const enN = (n, one, many) => `${fmtInt(n)} ${n === 1 ? one : many}`;

const LANG_NAMES = {
  ro: {ca: "Catalană", de: "Germană", en: "Engleză", es: "Spaniolă", fil: "Filipineză",
       fr: "Franceză", it: "Italiană", ja: "Japoneză", pt: "Portugheză", ro: "Română",
       si: "Sinhaleză"},
  en: {ca: "Catalan", de: "German", en: "English", es: "Spanish", fil: "Filipino", fr: "French",
       it: "Italian", ja: "Japanese", pt: "Portuguese", ro: "Romanian", si: "Sinhala"},
};
const UPOS = {
  ro: {NOUN: "substantiv", VERB: "verb", ADJ: "adjectiv", ADV: "adverb", DET: "determinant",
       ADP: "prepoziție", CCONJ: "conjuncție coordonatoare", SCONJ: "conjuncție subordonatoare",
       PRON: "pronume", AUX: "verb auxiliar", PART: "particulă", PROPN: "nume propriu",
       NUM: "numeral", X: "cuvânt neclasificat", INTJ: "interjecție", SYM: "simbol",
       PUNCT: "punctuație"},
  en: {NOUN: "noun", VERB: "verb", ADJ: "adjective", ADV: "adverb", DET: "determiner",
       ADP: "adposition", CCONJ: "coordinating conjunction", SCONJ: "subordinating conjunction",
       PRON: "pronoun", AUX: "auxiliary", PART: "particle", PROPN: "proper noun",
       NUM: "numeral", X: "other", INTJ: "interjection", SYM: "symbol", PUNCT: "punctuation"},
};

const I18N = {
  ro: {
    title: "Complexitate lexicală", subtitle: "11 limbi", uiLang: "Limba interfeței",
    logout: "Ieși", retry: "Reîncearcă",
    loginTitle: "Cod de acces", codeLabel: "Cod de acces", enter: "Intră",
    loginText: "Site-ul e deocamdată în test. Scrie codul primit; îl cerem o singură dată pe acest dispozitiv.",
    loginWrong: "Cod greșit.", loginExpired: "Codul nu mai e valid; scrie-l din nou.",
    loginMany: "Prea multe încercări greșite; revino peste câteva minute.",
    inTitle: "Textul tău", outTitle: "Textul analizat", textLang: "Limba textului",
    placeholder: "Scrie sau lipește un text…", clear: "Șterge textul",
    analyze: "Analizează", stop: "Oprește", legendLabel: "Niveluri; alege unul ca să rămână colorate doar cuvintele lui",
    empty: "Aici apare textul, cu fiecare cuvânt colorat după cât de dificil e. Apasă pe un cuvânt pentru detalii.",
    levels: {1: "Foarte ușor", 2: "Ușor", 3: "Neutru", 4: "Dificil", 5: "Foarte dificil"},
    conf: {hi: "încredere mare", mid: "încredere medie", lo: "încredere mică"},
    rchipTitle: v => `Corelația cu adnotările umane pe setul de test (${v.n} cuvinte, interval 95%: ${v.lo}–${v.hi}). Detalii mai jos.`,
    count: v => `${v.n} / ${v.max}`,
    countWarn: "text lung: cerem confirmare", countOver: "peste limită",
    shortcut: v => v.mac ? "⌘ ↵" : "Ctrl ↵",
    longTitle: "Text lung", cancel: "Renunță",
    longText: v => `Textul are ${roN(v.n, "caracter", "caractere")}. Analiza durează aproximativ ${v.est}` +
      `${v.slow ? ", poate mai mult acum, pentru că serverul merge mai încet" : ""}` +
      `${v.busy ? `; serverul mai lucrează la ${roN(v.busy, "text", "texte")}` : ""}. Poți opri oricând.`,
    sec: v => `${v.n} s`, min: v => `${v.n} min`,
    stQueued: v => `Ești la coadă (locul ${v.n}); analiza pornește când se eliberează un loc…`,
    stStart: "Se pregătește textul…",
    stRun: v => `Se analizează · ${v.pct}% · ${v.s} s`,
    stSlow: " · serverul merge mai încet acum",
    stDone: v => `Gata: ${roN(v.n, "cuvânt evaluat", "cuvinte evaluate")} în ${fmtDec(v.s, 1)} s` +
      (v.fn ? ` · ${roN(v.fn, "cuvânt funcțional", "cuvinte funcționale")} (nivel 1, fără model)` : "") +
      (v.other ? ` · ${roN(v.other, "nume propriu, numeral sau cuvânt străin", "nume proprii, numerale sau cuvinte străine")}, necolorate` : "") + ".",
    stStopped: v => `Oprită după ${roN(v.n, "propoziție", "propoziții")}; restul textului (estompat) nu a fost analizat.`,
    stStopped0: "Analiză oprită.",
    stCut: "Analiza s-a întrerupt: serverul a închis conexiunea. Partea estompată nu a fost analizată.",
    stFailed: v => `Analiza a eșuat pe server (${v.m}).`,
    stStale: "Textul sau limba s-au schimbat de la ultima analiză.",
    errNet: "Serverul nu răspunde (poate e oprit momentan). Încearcă din nou mai târziu.",
    errEmpty: "Textul e gol.", errLang: "Serverul nu cunoaște limba aleasă.",
    errLong: v => `Textul e prea lung: limita e de ${fmtInt(v.max)} de caractere.`,
    errBusyIp: "Ai deja două texte în analiză; așteaptă să se termine unul.",
    errQueue: "Sunt prea multe texte la coadă; încearcă din nou peste un minut.",
    errLoading: "Serverul pornește; încearcă din nou în aproximativ un minut.",
    errHttp: v => `Serverul a răspuns cu eroarea ${v.code}.`,
    bnDown: "Serverul e oprit momentan. Pagina se poate folosi din nou când revine.",
    bnLoading: "Serverul pornește (durează cam un minut)…",
    bnSlow: "Serverul merge mai încet decât de obicei; analizele pot dura de până la două ori mai mult.",
    popClose: "Închide", popScore: "Scor de complexitate", popLemma: "Lemă",
    popEasy: "ușor", popHard: "dificil",
    popFn: "Cuvânt funcțional: e afișat ca nivel 1, neevaluat de model.",
    popOther: "Neevaluat de model: sistemul evaluează doar cuvintele de conținut, așa că numele proprii, numeralele și cuvintele străine rămân necolorate.",
    popFnLv: "Nivel 1 · fără model",
    aboutTitle: "Cum se citește",
    note1: "<b>Scorul (0–1) e relativ la limbă</b>: arată unde cade cuvântul față de cuvintele evaluate în aceeași limbă. Nu compara scoruri între limbi.",
    note2: "Nivelul 1–5 e nota cea mai apropiată pe scala adnotărilor: foarte ușor, ușor, neutru, dificil, foarte dificil. Pe texte obișnuite iese mai ales verde: cuvintele alese pentru adnotare sunt în medie mai grele decât cele dintr-un text oarecare.",
    note3: "Sunt evaluate cuvintele de conținut (substantive, verbe, adjective, adverbe). Cuvintele funcționale (articole, prepoziții, pronume…) apar ca nivel 1, fără model; numele proprii, numeralele și cuvintele străine rămân necolorate.",
    note4: "Sistemul fuzionează două semnale, encodere multilingve și modelul de limbaj Gemma 4 12B, evaluate pe 11 limbi. Încrederea diferă mult de la o limbă la alta: vezi corelațiile pe limbi.",
    note5: "Analiza rulează pe un singur GPU: prima propoziție apare după câteva secunde, un paragraf durează de obicei sub o jumătate de minut. Textele nu sunt păstrate pe server.",
    rTitle: "Cât de bine urmează adnotările umane",
    rSub: "Corelația Pearson (r) pe setul de test al fiecărei limbi; 1 ar fi o potrivire perfectă. Linia subțire: intervalul de încredere 95%.",
    rMean: "Media pe 11 limbi",
    rRowTitle: v => `r = ${v.r}, interval 95%: ${v.lo}–${v.hi}, ${v.n} cuvinte de test`,
  },
  en: {
    title: "Lexical complexity", subtitle: "11 languages", uiLang: "Interface language",
    logout: "Sign out", retry: "Retry",
    loginTitle: "Access code", codeLabel: "Access code", enter: "Enter",
    loginText: "The site is still in testing. Type the code you were given; it is asked for only once on this device.",
    loginWrong: "Wrong code.", loginExpired: "The code is no longer valid; please type it again.",
    loginMany: "Too many wrong attempts; come back in a few minutes.",
    inTitle: "Your text", outTitle: "Analysed text", textLang: "Language of the text",
    placeholder: "Type or paste a text…", clear: "Clear the text",
    analyze: "Analyse", stop: "Stop", legendLabel: "Levels; pick one to keep only its words coloured",
    empty: "The text appears here, every word coloured by how difficult it is. Tap a word for details.",
    levels: {1: "Very easy", 2: "Easy", 3: "Neutral", 4: "Difficult", 5: "Very difficult"},
    conf: {hi: "high confidence", mid: "moderate confidence", lo: "low confidence"},
    rchipTitle: v => `Correlation with human annotations on the test set (${v.n} words, 95% interval ${v.lo}–${v.hi}). Details below.`,
    count: v => `${v.n} / ${v.max}`,
    countWarn: "long text: asks to confirm", countOver: "over the limit",
    shortcut: v => v.mac ? "⌘ ↵" : "Ctrl ↵",
    longTitle: "Long text", cancel: "Cancel",
    longText: v => `The text has ${enN(v.n, "character", "characters")}. The analysis takes about ${v.est}` +
      `${v.slow ? ", possibly longer now, as the server is running slower" : ""}` +
      `${v.busy ? `; the server is also working on ${enN(v.busy, "other text", "other texts")}` : ""}. You can stop it at any time.`,
    sec: v => `${v.n} s`, min: v => `${v.n} min`,
    stQueued: v => `You are in the queue (place ${v.n}); the analysis starts when a slot frees up…`,
    stStart: "Preparing the text…",
    stRun: v => `Analysing · ${v.pct}% · ${v.s} s`,
    stSlow: " · the server is slower right now",
    stDone: v => `Done: ${enN(v.n, "word", "words")} scored in ${fmtDec(v.s, 1)} s` +
      (v.fn ? ` · ${enN(v.fn, "function word", "function words")} (level 1, no model)` : "") +
      (v.other ? ` · ${enN(v.other, "proper noun, numeral or foreign word", "proper nouns, numerals or foreign words")}, not coloured` : "") + ".",
    stStopped: v => `Stopped after ${enN(v.n, "sentence", "sentences")}; the rest of the text (faded) was not analysed.`,
    stStopped0: "Analysis stopped.",
    stCut: "The analysis was cut off: the server closed the connection. The faded part was not analysed.",
    stFailed: v => `The analysis failed on the server (${v.m}).`,
    stStale: "The text or the language changed since the last analysis.",
    errNet: "The server does not answer (it may be switched off). Please try again later.",
    errEmpty: "The text is empty.", errLang: "The server does not know the chosen language.",
    errLong: v => `The text is too long: the limit is ${fmtInt(v.max)} characters.`,
    errBusyIp: "You already have two texts being analysed; wait for one to finish.",
    errQueue: "Too many texts are waiting; try again in a minute.",
    errLoading: "The server is starting; try again in about a minute.",
    errHttp: v => `The server answered with error ${v.code}.`,
    bnDown: "The server is switched off right now. The page works again when it is back.",
    bnLoading: "The server is starting (about a minute)…",
    bnSlow: "The server is running slower than usual; analyses may take up to twice as long.",
    popClose: "Close", popScore: "Complexity score", popLemma: "Lemma",
    popEasy: "easy", popHard: "difficult",
    popFn: "Function word: shown as level 1, not scored by the model.",
    popOther: "Not scored by the model: the system scores content words only, so proper nouns, numerals and foreign words stay uncoloured.",
    popFnLv: "Level 1 · no model",
    aboutTitle: "How to read it",
    note1: "<b>The score (0–1) is relative to the language</b>: it places the word among the words scored in the same language. Do not compare scores across languages.",
    note2: "The level 1–5 is the nearest rating on the annotation scale: very easy, easy, neutral, difficult, very difficult. Ordinary texts come out mostly green: the words chosen for annotation are on average harder than those of an ordinary text.",
    note3: "Content words (nouns, verbs, adjectives, adverbs) are scored. Function words (articles, prepositions, pronouns…) are shown as level 1 without the model; proper nouns, numerals and foreign words stay uncoloured.",
    note4: "The system fuses two signals, multilingual encoders and the language model Gemma 4 12B, evaluated on 11 languages. Confidence varies a lot between languages: see the correlations per language.",
    note5: "The analysis runs on a single GPU: the first sentence appears after a few seconds, and a paragraph usually takes under half a minute. Texts are not kept on the server.",
    rTitle: "How closely it follows human annotations",
    rSub: "Pearson correlation (r) on each language's test set; 1 would be a perfect match. The thin line: the 95% confidence interval.",
    rMean: "Mean over 11 languages",
    rRowTitle: v => `r = ${v.r}, 95% interval ${v.lo}–${v.hi}, ${v.n} test words`,
  },
};

const pickUi = () => {
  const s = store.get("lcp_ui");
  if (s === "ro" || s === "en") return s;
  return (navigator.languages || [navigator.language || "en"]).some(l => /^ro\b/i.test(l)) ? "ro" : "en";
};
let UI = pickUi();
const T = () => I18N[UI];
function t(key, vars) {
  const s = I18N[UI][key] ?? I18N.en[key];
  return typeof s === "function" ? s(vars || {}) : s;
}
const locale = () => UI === "ro" ? "ro-RO" : "en-GB";
const fmtInt = n => new Intl.NumberFormat(locale()).format(n);
const fmtDec = (x, d) => new Intl.NumberFormat(locale(), {minimumFractionDigits: d, maximumFractionDigits: d})
  .format(x);
const levelName = k => T().levels[k];   // the server's labels ("very easy"...) are the English ones
const langName = code => LANG_NAMES[UI][code] || code;

// ------------------------------------------------------------------------------ state
let INFO = null;                       // /api/languages
let CODE = store.get("lcp_code") || "";
let HEALTH = null;                     // last /api/health answer (null: unknown or unreachable)
let RUN = null;                        // the analysis streaming now
let RES = null;                        // the text shown on the right: {text, lang, words, ...}
let STATUS = null;                     // {key, vars, kind} of the status line (re-rendered on UI change)
let FILTER = 0;                        // legend filter: 0 = every level
let SEL = -1;                          // index in RES.words of the word whose popover is open
let healthTimer = 0;

const IS_MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || "");

// ------------------------------------------------------------------------------ i18n on the page
function applyI18n() {
  document.documentElement.lang = UI;
  document.title = t("title");
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-html]").forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
  document.querySelectorAll("[data-i18n-attr]").forEach(el => {
    for (const pair of el.dataset.i18nAttr.split(";")) {
      const [attr, key] = pair.split(":");
      el.setAttribute(attr, t(key));
    }
  });
  document.querySelectorAll(".seg [data-ui]").forEach(b =>
    b.setAttribute("aria-pressed", String(b.dataset.ui === UI)));
  $("kbd").textContent = t("shortcut", {mac: IS_MAC});
  $("kbd").title = IS_MAC ? "Cmd+Enter" : "Ctrl+Enter";
  if (INFO) { fillLangs(); showLang(); renderLegend(); renderRList(); }
  setBusyButton();
  renderStatus();
  if (BANNER) showBanner(BANNER.key, BANNER.kind, BANNER.retry, BANNER.vars);
  if (!$("confirm").open) closePop();
  else if (CONFIRM) CONFIRM.update();
}
function setUi(ui) {
  if (ui === UI) return;
  UI = ui;
  store.set("lcp_ui", ui);
  applyI18n();
}

// ------------------------------------------------------------------------------ banner, status
let BANNER = null;
function showBanner(key, kind = "", retry = false, vars = null) {
  BANNER = {key, kind, retry, vars};
  $("bannerText").textContent = t(key, vars);
  $("banner").className = "banner" + (kind ? " " + kind : "");
  $("retry").hidden = !retry;
  $("banner").hidden = false;
}
function hideBanner(key) {
  if (BANNER && (!key || BANNER.key === key)) { BANNER = null; $("banner").hidden = true; }
}
function setStatus(key, vars, kind = "") {
  STATUS = key ? {key, vars, kind} : null;
  renderStatus();
}
function renderStatus() {
  const el = $("status");
  // the running status changes every second: screen readers hear only the queue and the end
  el.setAttribute("aria-live", RUN && STATUS && STATUS.key !== "stQueued" ? "off" : "polite");
  if (!STATUS) { el.textContent = ""; el.className = "status"; return; }
  let s = t(STATUS.key, STATUS.vars);
  if (STATUS.slow) s += t("stSlow");
  el.textContent = s;
  el.className = "status" + (STATUS.kind ? " " + STATUS.kind : "");
}

// ------------------------------------------------------------------------------ API
function api(path, opts = {}) {
  const headers = {...(opts.headers || {})};
  if (CODE) headers["X-Access-Code"] = CODE;
  return fetch(API + path, {...opts, headers});
}
async function checkHealth() {
  // /api/health needs no code; a plain GET (no custom header) needs no CORS preflight.
  try {
    const r = await fetch(API + "/api/health", {cache: "no-store"});
    const j = await r.json().catch(() => ({}));
    HEALTH = {http: r.status, ...j};
  } catch (e) {
    HEALTH = null;
  }
  return HEALTH;
}
function watchHealth() {
  // While the server loads its models (503), ask again every 8 s; then load the languages.
  clearTimeout(healthTimer);
  healthTimer = setTimeout(async () => {
    const h = await checkHealth();
    if (h && h.status === "ok") {
      hideBanner("bnLoading");
      if (!INFO_FRESH) loadLanguages();
      noteSlow();
    } else if (h && h.http === 503) {
      watchHealth();
    } else if (!h) {
      showBanner("bnDown", "warn", true);
    }
  }, 8000);
}
function noteSlow() {
  if (HEALTH && HEALTH.status === "ok" && HEALTH.slow) showBanner("bnSlow", "warn");
  else hideBanner("bnSlow");
}

// ------------------------------------------------------------------------------ start, login
let INFO_FRESH = false;                // INFO came from the server in this visit
function showLogin(msgKey) {
  $("app").hidden = true;
  $("login").hidden = false;
  if ($("logout")) $("logout").hidden = true;
  $("loginMsg").textContent = msgKey ? t(msgKey) : "";
  $("code").value = "";
  setTimeout(() => $("code").focus(), 0);
}
function showApp() {
  const first = $("app").hidden;
  $("login").hidden = true;
  $("app").hidden = false;
  if ($("logout")) $("logout").hidden = false;
  fillLangs();
  showLang();
  renderLegend();
  renderRList();
  grow();
  if (first && !RES) $("text").focus({preventScroll: true});
}
async function loadLanguages() {
  let r;
  try { r = await api("/api/languages", {cache: "no-store"}); }
  catch (e) {
    showBanner("bnDown", "warn", true);
    return;
  }
  if (r.status === 401) { forgetCode(); showLogin(CODE_WAS_SAVED ? "loginExpired" : ""); return; }
  if (r.status === 429) { showLogin("loginMany"); return; }
  if (r.status === 503) { showBanner("bnLoading"); watchHealth(); return; }
  if (!r.ok) { showBanner("errHttp", "err", true, {code: r.status}); return; }
  INFO = await r.json();
  INFO_FRESH = true;
  store.set("lcp_info", JSON.stringify(INFO));
  hideBanner("bnDown");
  hideBanner("bnLoading");
  showApp();
}
let CODE_WAS_SAVED = !!CODE;
function forgetCode() { CODE = ""; store.del("lcp_code"); }

async function start() {
  // The access code form appears only when the server asks for a code (401). With LCP_ACCESS_CODE
  // unset on the server (temporarily, from 22 Nov 2026) the page opens directly.
  applyI18n();
  try { INFO = JSON.parse(store.get("lcp_info") || "null"); } catch (e) { INFO = null; }
  if (INFO && Array.isArray(INFO.languages) && INFO.languages.length) showApp();
  else INFO = null;
  loadLanguages();
  const h = await checkHealth();
  if (!h) { if (!INFO_FRESH) showBanner("bnDown", "warn", true); }
  else if (h.http === 503) { showBanner("bnLoading"); watchHealth(); }
  else noteSlow();
}

$("loginForm").addEventListener("submit", async ev => {
  ev.preventDefault();
  const code = $("code").value.trim();
  if (!code) { $("code").focus(); return; }
  const btn = ev.target.querySelector("button");
  btn.disabled = true;
  $("loginMsg").textContent = "";
  let r;
  try {
    r = await fetch(API + "/api/auth", {method: "POST", headers: {"Content-Type": "application/json"},
                                        body: JSON.stringify({code})});
  } catch (e) {
    $("loginMsg").textContent = t("errNet");
    btn.disabled = false;
    return;
  }
  btn.disabled = false;
  if (r.ok) {
    CODE = code;
    CODE_WAS_SAVED = true;
    store.set("lcp_code", code);
    loadLanguages();
  } else {
    $("loginMsg").textContent = t(r.status === 429 ? "loginMany" : "loginWrong");
    $("code").select();
  }
});
// Sign out: its button is commented out in index.html while no access code is needed.
if ($("logout")) $("logout").addEventListener("click", () => {
  if (RUN) RUN.ctrl.abort();
  forgetCode();
  CODE_WAS_SAVED = false;
  showLogin();
});
$("retry").addEventListener("click", async () => {
  $("retry").disabled = true;
  const h = await checkHealth();
  $("retry").disabled = false;
  if (!h) return;
  hideBanner();
  if (h.http === 503) { showBanner("bnLoading"); watchHealth(); return; }
  loadLanguages();
  noteSlow();
});
document.querySelectorAll(".seg [data-ui]").forEach(b => b.addEventListener("click", () => setUi(b.dataset.ui)));

// ------------------------------------------------------------------------------ input pane
function lang() {
  return INFO.languages.find(l => l.code === $("lang").value) || INFO.languages[0];
}
function fillLangs() {
  const sel = $("lang");
  const cur = sel.value || store.get("lcp_lang") || (UI === "ro" ? "ro" : "en");
  const ls = [...INFO.languages].sort((a, b) => langName(a.code).localeCompare(langName(b.code), locale()));
  sel.innerHTML = ls.map(l => `<option value="${esc(l.code)}">${esc(langName(l.code))}</option>`).join("");
  sel.value = INFO.languages.some(l => l.code === cur) ? cur : INFO.languages[0].code;
}
const confKey = r => r >= 0.75 ? "hi" : r >= 0.6 ? "mid" : "lo";
function showLang() {
  const l = lang();
  const r = fmtDec(l.r, 2);
  $("rchip").innerHTML = `r = <b>${esc(r)}</b> · ${esc(T().conf[confKey(l.r)])}`;
  $("rchip").title = t("rchipTitle", {n: fmtInt(l.n_test), lo: fmtDec(l.ci[0], 2), hi: fmtDec(l.ci[1], 2)});
  $("text").lang = l.code;
  store.set("lcp_lang", l.code);
  renderRList();
  count();
}
function renderRList() {
  // a meter list: one bar per language on a 0-1 axis, sorted by r, the chosen language in the
  // accent colour, the 95% interval as a thin line, the mean of the 11 languages last
  if (!INFO) return;
  const cur = $("lang").value;
  const row = (name, r, ci, title, cls) =>
    `<li class="rrow ${cls}" title="${esc(title)}"><span>${esc(name)}</span>` +
    `<span class="rtrack" aria-hidden="true"><i style="width:${(r * 100).toFixed(1)}%"></i>` +
    `<s style="left:${(ci[0] * 100).toFixed(1)}%;width:${((ci[1] - ci[0]) * 100).toFixed(1)}%"></s></span>` +
    `<span class="rv">${fmtDec(r, 2)}</span></li>`;
  const ls = [...INFO.languages].sort((a, b) => b.r - a.r);
  $("rlist").innerHTML = ls.map(l => row(langName(l.code), l.r, l.ci,
    t("rRowTitle", {r: fmtDec(l.r, 2), lo: fmtDec(l.ci[0], 2), hi: fmtDec(l.ci[1], 2), n: fmtInt(l.n_test)}),
    l.code === cur ? "cur" : "")).join("") +
    row(t("rMean"), INFO.mean_r, INFO.mean_ci, `r = ${fmtDec(INFO.mean_r, 3)}`, "mean");
}
function count() {
  if (!INFO) return;
  const text = $("text").value, n = cpLen(text), l = lang();
  const el = $("count");
  let s = t("count", {n: fmtInt(n), max: fmtInt(INFO.max_chars)});
  el.className = "count";
  if (n > INFO.max_chars) { s += " · " + t("countOver"); el.className = "count over"; }
  else if (n > l.warn_chars) { s += " · " + t("countWarn"); el.className = "count warn"; }
  el.textContent = s;
  $("clear").hidden = n === 0;
  setBusyButton();
  if (RES && !RUN && RES.final) {
    const stale = text !== RES.text || l.code !== RES.lang;
    if (stale && (!STATUS || STATUS.key !== "stStale")) setStatus("stStale");
    else if (!stale && STATUS && STATUS.key === "stStale") setStatus(...RES.final);
  }
}
function setBusyButton() {
  const go = $("go");
  if (RUN) {
    go.textContent = t("stop");
    go.className = "btn stop";
    go.disabled = false;
    return;
  }
  go.textContent = t("analyze");
  go.className = "btn primary";
  const n = INFO ? cpLen($("text").value) : 0;
  go.disabled = !INFO || !$("text").value.trim() || n > INFO.max_chars;
}
function grow() {
  // the text box grows with its text, like the output next to it (the page scrolls, not the box)
  const ta = $("text"), y = window.scrollY;
  ta.style.height = "auto";
  ta.style.height = ta.scrollHeight + "px";
  if (window.scrollY !== y) window.scrollTo(0, y);
}
$("lang").addEventListener("change", showLang);
$("text").addEventListener("input", () => { grow(); count(); });
window.addEventListener("resize", grow);
$("text").addEventListener("keydown", e => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    if (!RUN && !$("go").disabled) analyze();
  }
});
$("clear").addEventListener("click", () => {
  $("text").value = "";
  grow();
  count();
  $("text").focus();
});
$("go").addEventListener("click", () => { if (RUN) RUN.ctrl.abort(); else analyze(); });

// ------------------------------------------------------------------------------ confirmation
function estimate(n, l) {
  let s = n / 1000 * (l.est_s_per_1000_chars || 25);
  if (HEALTH && HEALTH.slow) s *= 2;
  if (s < 60) return t("sec", {n: Math.max(5, Math.round(s / 5) * 5)});
  return t("min", {n: Math.round(s / 60)});
}
let CONFIRM = null;                    // the open confirmation: {update()}
function confirmLong(n, l) {
  // Shown at once with the last known server state; a fresh /api/health updates the text when
  // it arrives (the tunnel can take seconds on a new connection).
  const dlg = $("confirm");
  const update = () => {
    $("dlgText").textContent = t("longText", {
      n, est: estimate(n, l), slow: !!(HEALTH && HEALTH.slow),
      busy: HEALTH && HEALTH.status === "ok" ? (HEALTH.active || 0) + (HEALTH.waiting || 0) : 0});
  };
  update();
  if (typeof dlg.showModal !== "function") return Promise.resolve(window.confirm($("dlgText").textContent));
  CONFIRM = {update};
  checkHealth().then(() => { if (CONFIRM && CONFIRM.update === update) update(); });
  return new Promise(resolve => {
    dlg.returnValue = "";
    dlg.addEventListener("close", () => { CONFIRM = null; resolve(dlg.returnValue === "ok"); }, {once: true});
    dlg.showModal();
  });
}

// ------------------------------------------------------------------------------ output pane
// The text on the right is built once per event: the paragraph list makes one faded span per
// paragraph; a paragraph's "sentences" splits it into faded sentence spans; a finished
// "sentence" replaces its span with the coloured words. Spans are found by data attributes.
function kindOf(w) {                   // servers before the "kind" field sent "function" only
  return w.kind || (w.function ? "function" : "content");
}
function wordsHtml(text, a, b, words, k0) {
  // text[a:b] with the given words (UTF-16 offsets, sorted, inside [a, b], not overlapping) as
  // spans; k0: index of words[0] in RES.words
  let html = "", pos = a;
  words.forEach((w, j) => {
    html += esc(text.slice(pos, w.start));
    const kind = kindOf(w);
    const cls = kind === "content" ? `w l${w.level}` : kind === "function" ? "w l1 fn" : "w o";
    const tab = kind === "content" ? 0 : -1;
    html += `<span class="${cls}" data-k="${k0 + j}" tabindex="${tab}" role="button">` +
            `${esc(text.slice(w.start, w.end))}</span>`;
    pos = w.end;
  });
  return html + esc(text.slice(pos, b));
}
function spansHtml(text, a, b, spans, attr) {
  // text[a:b] with the given spans (sorted) wrapped as faded <span data-attr=i>;
  // returns the html and the spans as drawn (clipped to [a, b], without overlaps)
  let html = "", pos = a;
  const drawn = [];
  for (const s of spans) {
    const s0 = Math.max(pos, s.start), s1 = Math.min(b, s.end);
    if (s1 <= s0) continue;
    html += esc(text.slice(pos, s0));
    html += `<span class="${attr === "p" ? "para" : "sent"} pending" data-${attr}="${s.i}">` +
            `${esc(text.slice(s0, s1))}</span>`;
    drawn.push({i: s.i, start: s0, end: s1});
    pos = s1;
  }
  return {html: html + esc(text.slice(pos, b)), drawn};
}

function beginOutput(text, code) {
  closePop();
  RES = {text, lang: code, cp: cpMap(text), words: [], paras: [], sentSpan: {}, n_sent: 0,
         done: null, final: null, upto: 0};
  FILTER = 0;
  const out = $("out");
  out.lang = code;
  delete out.dataset.filter;
  out.innerHTML = `<span class="para pending" data-p="all">${esc(text)}</span>`;
  $("empty").hidden = true;
  renderLegend();
  progress(0);
}
const at = i => RES.cp[i] ?? RES.text.length;      // API offset -> UTF-16
function onParagraphs(ev) {
  const ps = ev.paragraphs.map(p => ({i: p.i, start: at(p.start), end: at(p.end)}));
  const {html, drawn} = spansHtml(RES.text, 0, RES.text.length, ps, "p");
  RES.paras = drawn;
  $("out").innerHTML = html;
}
function onSentences(ev) {
  const p = RES.paras.find(x => x.i === ev.paragraph);
  const el = $("out").querySelector(`[data-p="${ev.paragraph}"]`);
  if (!p || !el) return;
  const ss = ev.sentences.map(s => ({i: s.i, start: at(s.start), end: at(s.end)}));
  const {html, drawn} = spansHtml(RES.text, p.start, p.end, ss, "s");
  el.classList.remove("pending");
  el.innerHTML = html;
  for (const s of drawn) RES.sentSpan[s.i] = s;
  if (!drawn.length) RES.upto = Math.max(RES.upto, p.end);
}
function onSentence(ev) {
  const el = $("out").querySelector(`[data-s="${ev.i}"]`);
  const span = RES.sentSpan[ev.i];
  // words outside the sentence as drawn are dropped (wordsHtml), so they never get an index
  const ws = ev.words.map(w => ({...w, start: at(w.start), end: at(w.end)}))
    .sort((x, y) => x.start - y.start)
    .filter(w => span && w.start >= span.start && w.end <= span.end && w.start < w.end);
  const kept = [];
  let pos = span ? span.start : 0;
  for (const w of ws) if (w.start >= pos) { kept.push(w); pos = w.end; }
  const k0 = RES.words.length;
  RES.words.push(...kept);
  RES.n_sent++;
  if (el && span) {
    el.innerHTML = wordsHtml(RES.text, span.start, span.end, kept, k0);
    el.classList.remove("pending");
    el.classList.add("fresh");
  }
  if (span) RES.upto = Math.max(RES.upto, span.end);
  progress(RES.upto / Math.max(1, RES.text.length));
  renderLegend();
}
function progress(f) {
  const bar = $("prog");
  if (f === null) { bar.hidden = true; return; }
  bar.hidden = false;
  bar.firstElementChild.style.transform = `scaleX(${Math.min(1, Math.max(0, f))})`;
}

// legend: the five levels with their counts; a click keeps only that level coloured
function levelCounts() {
  const n = [0, 0, 0, 0, 0, 0];
  if (RES) for (const w of RES.words) if (kindOf(w) !== "other") n[w.level]++;
  return n;
}
function renderLegend() {
  // the buttons are made once and then updated in place, so focus and transitions survive
  const lg = $("legend");
  if (!lg.children.length) {
    lg.innerHTML = [1, 2, 3, 4, 5].map(k =>
      `<button type="button" class="lv" data-level="${k}" aria-pressed="false">` +
      `<i class="sw" style="background:var(--l${k})"></i><span class="name"></span>` +
      `<span class="n"></span></button>`).join("");
  }
  const n = levelCounts(), has = !!(RES && RES.words.length);
  for (const b of lg.children) {
    const k = +b.dataset.level;
    b.querySelector(".name").textContent = levelName(k);
    const c = b.querySelector(".n");
    c.textContent = has ? fmtInt(n[k]) : "";
    c.hidden = !has;
    b.setAttribute("aria-pressed", String(FILTER === k));
  }
  lg.classList.toggle("filtering", FILTER > 0);
}
$("legend").addEventListener("click", e => {
  const b = e.target.closest(".lv");
  if (!b) return;
  const k = +b.dataset.level;
  FILTER = FILTER === k ? 0 : k;
  if (FILTER) $("out").dataset.filter = String(FILTER); else delete $("out").dataset.filter;
  renderLegend();
});

// ------------------------------------------------------------------------------ popover
function closePop(refocus) {
  const pop = $("pop");
  if (pop.hidden) { SEL = -1; return; }
  pop.classList.remove("show");
  pop.hidden = true;
  const el = document.querySelector(".w.sel");
  if (el) {
    el.classList.remove("sel");
    el.setAttribute("aria-expanded", "false");
    if (refocus) el.focus();
  }
  SEL = -1;
}
function popHtml(w) {
  // the word, its part of speech, the level and the 0-1 score, the lemma
  const kind = kindOf(w);
  const pos = w.upos && UPOS[UI][w.upos] ? UPOS[UI][w.upos] : "";
  const lemma = w.lemma
    ? `<div class="pop-row"><span>${esc(t("popLemma"))}</span><span>${esc(w.lemma)}</span></div>` : "";
  const h = `<button type="button" class="icon-btn pop-x" aria-label="${esc(t("popClose"))}">` +
    `<svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M5.5 5.5l9 9m0-9l-9 9" ` +
    `stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/></svg></button>` +
    `<p class="pop-word" id="popWord">${esc(w.text)}</p><div class="pop-pos">${esc(pos)}</div>`;
  if (kind === "function") {
    return h + `<span class="pop-lv fn">${esc(t("popFnLv"))}</span>${lemma}<p class="pop-note">${esc(t("popFn"))}</p>`;
  }
  if (kind === "other") return h + lemma + `<p class="pop-note">${esc(t("popOther"))}</p>`;
  return h +
    `<span class="pop-lv l${w.level}">${w.level} · ${esc(levelName(w.level))}</span>` +
    `<div class="scale" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i>` +
    `<b style="left:${(Math.min(1, Math.max(0, w.score)) * 100).toFixed(1)}%"></b></div>` +
    `<div class="scale-ends" aria-hidden="true"><span>0 · ${esc(t("popEasy"))}</span>` +
    `<span>${esc(t("popHard"))} · 1</span></div>` +
    `<div class="pop-row"><span>${esc(t("popScore"))}</span><span>${fmtDec(w.score, 2)}</span></div>` +
    lemma;
}
function openPop(el) {
  const k = +el.dataset.k, w = RES && RES.words[k];
  if (!w) return;
  const pop = $("pop"), wrap = el.closest(".out-wrap");
  const reopen = !pop.hidden;
  document.querySelectorAll(".w.sel").forEach(x => { x.classList.remove("sel"); x.setAttribute("aria-expanded", "false"); });
  SEL = k;
  el.classList.add("sel");
  el.setAttribute("aria-expanded", "true");
  el.setAttribute("aria-controls", "pop");
  pop.innerHTML = popHtml(w);
  pop.hidden = false;
  // place it under the word (above when there is no room below), inside the pane
  const wr = wrap.getBoundingClientRect();
  const rects = el.getClientRects(), r = rects.length ? rects[0] : el.getBoundingClientRect();
  const pw = pop.offsetWidth, ph = pop.offsetHeight;
  let left = r.left - wr.left + r.width / 2 - Math.min(pw / 2, 40);
  left = Math.max(8, Math.min(left, wr.width - pw - 8));
  const below = window.innerHeight - r.bottom, above = r.top;
  const up = below < ph + 16 && above > below;
  const top = up ? r.top - wr.top - ph - 8 : r.bottom - wr.top + 8;
  pop.style.left = left + "px";
  pop.style.top = Math.max(0, top) + "px";
  pop.style.transformOrigin = `${Math.round(r.left - wr.left + r.width / 2 - left)}px ${up ? "100%" : "0"}`;
  pop.classList.toggle("up", up);
  if (!reopen) {
    pop.classList.remove("show");
    void pop.offsetWidth;                                      // start the transition from here
  }
  pop.classList.add("show");
  pop.querySelector(".pop-x").addEventListener("click", ev => { ev.stopPropagation(); closePop(true); });
}
$("out").addEventListener("click", e => {
  const el = e.target.closest(".w");
  if (!el) return;
  e.stopPropagation();
  if (+el.dataset.k === SEL && !$("pop").hidden) closePop();
  else openPop(el);
});
$("out").addEventListener("keydown", e => {
  const el = e.target.closest(".w");
  if (!el) return;
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    if (+el.dataset.k === SEL && !$("pop").hidden) closePop(); else openPop(el);
    return;
  }
  const dir = {ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1}[e.key];
  if (!dir && e.key !== "Home" && e.key !== "End") return;
  const all = [...$("out").querySelectorAll(".w")];
  let i = all.indexOf(el);
  i = e.key === "Home" ? 0 : e.key === "End" ? all.length - 1 : i + dir;
  if (i < 0 || i >= all.length) return;
  e.preventDefault();
  all[i].focus();
  if (!$("pop").hidden) openPop(all[i]);
});
$("pop").addEventListener("click", e => e.stopPropagation());
document.addEventListener("click", e => { if (!e.target.closest("#pop")) closePop(); });
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && !$("pop").hidden) { e.preventDefault(); closePop(true); }
});
window.addEventListener("resize", () => {
  const el = SEL >= 0 && document.querySelector(".w.sel");
  if (el) openPop(el);
});

// ------------------------------------------------------------------------------ the analysis
class StreamCut extends Error {}
class ServerError extends Error {}
function httpErrorKey(status, detail) {
  const d = (detail || "").toLowerCase();
  if (status === 400) return d.includes("language") ? ["errLang"] : ["errEmpty"];
  if (status === 413) return ["errLong", {max: INFO.max_chars}];
  if (status === 429) return d.includes("access code") ? ["loginMany"] : ["errBusyIp"];
  if (status === 503) return d.includes("loading") ? ["errLoading"] : ["errQueue"];
  return ["errHttp", {code: status}];
}
async function readStream(r, onEvent) {
  const reader = r.body.getReader(), dec = new TextDecoder();
  let buf = "";
  const take = () => {
    let k;
    while ((k = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, k).trim();
      buf = buf.slice(k + 1);
      if (line) onEvent(JSON.parse(line));
    }
  };
  for (;;) {
    const {value, done} = await reader.read();
    if (done) break;
    buf += dec.decode(value, {stream: true});
    take();
  }
  buf += dec.decode();
  if (buf.trim()) { buf += "\n"; take(); }
}
function runStatus() {
  if (!RUN || RUN.queued) return;
  const s = Math.round((performance.now() - RUN.t0) / 1000);
  if (!RUN.started) { setStatus("stStart", null, ""); }
  else {
    setStatus("stRun", {pct: Math.round(100 * RES.upto / Math.max(1, RES.text.length)), s});
  }
  STATUS.slow = !!(HEALTH && HEALTH.status === "ok" && HEALTH.slow);
  renderStatus();
}
async function analyze() {
  if (RUN || !INFO) return;
  const text = $("text").value, l = lang(), n = cpLen(text);
  if (!text.trim() || n > INFO.max_chars) return;
  if (n > l.warn_chars) {
    if (!(await confirmLong(n, l))) { $("go").focus(); return; }
    if (RUN) return;
  } else {
    checkHealth().then(() => { noteSlow(); runStatus(); });
  }
  RUN = {ctrl: new AbortController(), t0: performance.now(), started: false, queued: false,
         finished: false};
  const run = RUN;
  setBusyButton();
  beginOutput(text, l.code);
  setStatus("stStart");
  const tick = setInterval(runStatus, 1000);
  let final = null;
  try {
    const r = await api("/api/analyze", {method: "POST", headers: {"Content-Type": "application/json"},
                                         body: JSON.stringify({lang: l.code, text}),
                                         signal: run.ctrl.signal});
    if (r.status === 401) {
      forgetCode();
      showLogin("loginExpired");
      final = null;
      throw Object.assign(new Error("401"), {silent: true});
    }
    if (!r.ok) {
      const e = await r.json().catch(() => ({}));
      final = [...httpErrorKey(r.status, e.detail), "err"];
      if (final.length === 2) final.splice(1, 0, null);
      throw Object.assign(new Error("http"), {silent: true});
    }
    await readStream(r, ev => {
      switch (ev.type) {
        case "queued":
          run.queued = true;
          setStatus("stQueued", {n: ev.position});
          return;
        case "ping": return;
        case "paragraphs": run.queued = false; run.started = true; onParagraphs(ev); break;
        case "sentences": onSentences(ev); break;
        case "sentence": onSentence(ev); break;
        case "done":
          run.finished = true;
          RES.done = ev;
          final = ["stDone", {n: ev.content_words, s: ev.timings.total_s,
                              fn: ev.function_words || 0, other: ev.other_words || 0}, ""];
          break;
        case "error":
          throw new ServerError(ev.message || "error");
        default: return;
      }
      runStatus();
    });
    if (!run.finished) throw new StreamCut();
  } catch (e) {
    if (e.silent) { /* status already decided */ }
    else if (e.name === "AbortError") final = ["stStopped", {n: RES.n_sent}, ""];
    else if (e instanceof StreamCut) final = ["stCut", null, "err"];
    else if (e instanceof ServerError) {
      const m = /\(([^)]+)\)/.exec(e.message);
      final = ["stFailed", {m: m ? m[1] : e.message}, "err"];
    }
    else if (e instanceof TypeError) final = ["errNet", null, "err"];
    else final = ["stFailed", {m: e.message}, "err"];
  } finally {
    clearInterval(tick);
    RUN = null;
    progress(null);
    if (RES) {
      if (!RES.n_sent && (!final || final[0] !== "stDone")) {
        // nothing came back: show the empty pane again, not a faded copy of the text
        $("out").innerHTML = "";
        $("empty").hidden = false;
        if (final && final[0] === "stStopped") final = ["stStopped0", null, ""];
        RES = null;
      } else {
        RES.final = final;
      }
    }
    if (final) setStatus(final[0], final[1], final[2]);
    else setStatus(null);
    setBusyButton();
    count();
    renderLegend();
  }
}

start();
})();
