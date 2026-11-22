"""Split a raw text into sentences and words, and mark the content words to be scored.

The paper scores MLSP targets, which are content words given in a context. On raw text:
  - for the nine languages the paper lemmatises with stanza (data.STANZA_LANGS: ca de en es fr it
    ja pt ro), stanza tokenize, mwt, pos and lemma, with the same models `data._lemmatize` loads
    (the default package of each processor). A token is a content word when one of its words is
    tagged NOUN, VERB, ADJ or ADV. Its lemma is the lemmas of its words joined by spaces, as in
    `data._lemmatize` (so French "du" gives "de le");
  - for Filipino and Sinhala, which have no stanza lemmatiser in the paper (their lemma is empty
    there too), a regex tokeniser: a word is a content word when it contains a letter and is not
    in a short list of function words below. The lists are provisional (stage 1 only needs a
    realistic number of content words); the share of content words is reported by the benchmark.
A token without any letter (numbers, symbols) is never a content word.

Words, not tokens. Stanza's tokeniser sometimes cuts one written word in two with nothing between
the pieces (Romanian "liturghie" at the end of a text without final punctuation gives "liturghi" +
"e"). Adjacent tokens with a letter or digit on both sides of the cut are joined into one word
(except in Japanese, written without spaces), and that word gets its UPOS and lemma from tagging
the sentence again with it as a single token. Cuts at a hyphen or an apostrophe (Romanian "s-a",
French "l'homme") are left as they are.

Romanian typed without diacritics. The stanza Romanian models are trained on text with diacritics:
on "Maine ma gandesc" they tag "Maine" as the US state (PROPN), "daca" as a noun, "acasa" as a
proper noun. When a Romanian text has no diacritic at all, stanza is given a copy with them
restored word by word: each word becomes its most frequent form in wordfreq's Romanian list that
differs from it only by ă â î ș ț (ties and unknown words stay as typed). The copy has the same
length, so the offsets hold; the words shown, their context and the forms scored stay the user's,
only the UPOS and the lemma come from the copy.

The context of a word is its sentence. Stanza pipelines are loaded lazily, one per language.

Prepare the stanza models once (unpacks the default packages cached on Hugging Face into
STANZA_RESOURCES_DIR, exactly what `data._lemmatize` does):
  python -m lcp.segment --prepare
"""
import argparse
import re
import time
import unicodedata
from dataclasses import dataclass, field

import data

LANGS = ("ca", "de", "en", "es", "fil", "fr", "it", "ja", "pt", "ro", "si")
CONTENT_UPOS = frozenset({"NOUN", "VERB", "ADJ", "ADV"})
# Closed classes: the tokens shown as level 1 without the model ("function" words). The other
# non-content tokens with a letter (PROPN, NUM, X, INTJ, SYM...) are left unscored and uncoloured.
FUNCTION_UPOS = frozenset({"DET", "ADP", "CCONJ", "SCONJ", "PRON", "AUX", "PART"})

# Closed-class words: case markers, linkers, conjunctions, pronouns, particles. Deictic adverbs
# (dito, doon, ganito...) are kept as content words: they are MLSP targets in Filipino.
FUNCTION_WORDS = {
    "fil": frozenset("""
        ang mga ng nang sa si sina ni nina kay kina na at ay o pero ngunit subalit dahil
        kasi kung kapag pag upang para tulad gaya bilang mula hanggang tungkol ayon kaysa nasa
        ako ko akin aking ikaw ka mo iyo iyong siya niya kanya kaniya kanyang kaniyang kami namin
        amin aming tayo natin atin ating kayo ninyo inyo inyong sila nila kanila kanilang ito iyan
        iyon nito niyan niyon ba pa din rin daw raw lamang lang po ho man nga naman pala yata sana
        may mayroon isang isa
    """.split()),
    "si": frozenset("""
        සහ හා හෝ ද ත් නමුත් එහෙත් නිසා විසින් සඳහා මගින් සමග සමඟ තුළ මත අතර පසු පෙර දක්වා සිට ලෙස
        පරිදි වැනි පමණ යන යනු බව මෙම එම මේ ඒ එය මෙය ඔහු ඇය ඔවුන් ඔහුගේ ඇයගේ ඔවුන්ගේ මම මා මගේ
        අපි අප අපගේ ඔබ ඔබේ වේ වෙයි ය යි ඇත ඇති නැත නැති විය වූ වන කර කළ ලදී ලද ඉතා වඩා එක් එක
        සියලු සෑම
    """.split()),
}


@dataclass
class Word:
    text: str
    start: int            # character offsets in the sentence text
    end: int
    lemma: str = ""
    upos: str = ""
    content: bool = False


@dataclass
class Sentence:
    text: str             # the input text between start and end, newlines replaced by spaces
    start: int            # character offsets in the input text
    end: int
    words: list = field(default_factory=list)

    @property
    def content_words(self):
        return [w for w in self.words if w.content]


def _has_letter(s):
    return any(c.isalpha() for c in s)


# ----------------------------------------------------------------------------- Romanian diacritics
_RO_DIACRITICS = frozenset("ăâîșțşţĂÂÎȘȚŞŢ")
_RO_STRIP = str.maketrans("ăâîșțşţ", "aaistst")
_RO_WORD = re.compile(r"[^\W\d_]+")
_ro_map = None


def _ro_restore_map():
    """{word without diacritics: its most frequent form with diacritics}, from wordfreq."""
    global _ro_map
    if _ro_map is None:
        from wordfreq import get_frequency_dict
        fd = get_frequency_dict("ro")
        best = {}
        for w, f in fd.items():
            if not any(c in _RO_DIACRITICS for c in w):
                continue
            k = w.translate(_RO_STRIP)
            if len(k) == len(w) and f > fd.get(k, 0.0) and f > best.get(k, ("", 0.0))[1]:
                best[k] = (w, f)
        _ro_map = {k: w for k, (w, _) in best.items()}
    return _ro_map


def restore_ro(text):
    """`text` with the Romanian diacritics restored word by word if it has none (same length),
    else `text` unchanged."""
    if any(c in _RO_DIACRITICS for c in text):
        return text
    m = _ro_restore_map()

    def fix(mo):
        w = mo.group(0)
        r = m.get(w.lower())
        if r is None or len(r) != len(w):
            return w
        return "".join(b.upper() if a.isupper() else b for a, b in zip(w, r))
    return _RO_WORD.sub(fix, text)


# ----------------------------------------------------------------------------- stanza
class Segmenter:
    def __init__(self):
        self._nlp = {}
        self.load_seconds = {}

    def pipeline(self, lang):
        if lang not in self._nlp:
            import stanza
            from stanza.resources.common import load_resources_json
            t0 = time.perf_counter()
            # Same processors as data._lemmatize, without downloading anything at run time.
            have = load_resources_json()[lang]["default_processors"]
            procs = ",".join(x for x in ("tokenize", "mwt", "pos", "lemma") if x in have)
            self._nlp[lang] = stanza.Pipeline(lang, processors=procs, verbose=False,
                                              download_method=None)
            self.load_seconds[lang] = time.perf_counter() - t0
        return self._nlp[lang]

    def segment(self, lang, text):
        """[Sentence] for `text` in `lang`."""
        if lang not in LANGS:
            raise ValueError(f"unsupported language {lang!r}")
        if lang in data.STANZA_LANGS:
            return self._stanza(lang, text)
        return _regex(lang, text)

    def _stanza(self, lang, text):
        src = restore_ro(text) if lang == "ro" else text
        nlp = self.pipeline(lang)
        doc = nlp(src)

        def glued(t, u):     # u continues the written word that t ends
            i = u.start_char
            return (lang != "ja" and t.end_char == i and 0 < i < len(text)
                    and _word_char(text[i - 1]) and _word_char(text[i]))

        sents = []
        for sn in doc.sentences:
            toks = [t for t in sn.tokens if t.start_char is not None and t.end_char is not None]
            if not toks:
                continue
            if sents and glued(sents[-1][-1], toks[0]):    # a word cut across two sentences
                sents[-1] += toks
            else:
                sents.append(toks)
        out = []
        for toks in sents:
            groups = []                                    # the tokens of each written word
            for t in toks:
                if groups and glued(groups[-1][-1], t):
                    groups[-1].append(t)
                else:
                    groups.append([t])
            retag = _retag(nlp, src, groups) if len(groups) < len(toks) else None
            s0, s1 = toks[0].start_char, toks[-1].end_char
            sent = Sentence(text[s0:s1].replace("\n", " "), s0, s1)
            for k, g in enumerate(groups):
                a, b = g[0].start_char, g[-1].end_char
                ws = [retag[k]] if len(g) > 1 and retag else [w for t in g for w in t.words]
                upos = [w.upos or "" for w in ws]
                content = [u for u in upos if u in CONTENT_UPOS]
                form = text[a:b]
                sent.words.append(Word(
                    form, a - s0, b - s0,
                    lemma=" ".join(w.lemma for w in ws if w.lemma),
                    upos=(content or upos or [""])[0],
                    content=bool(content) and _has_letter(form)))
            out.append(sent)
        return out


def _retag(nlp, src, groups):
    """Stanza words of a sentence tagged again (pos, lemma) with each group of tokens as one token:
    one word per group, or None if the pipeline has no tagger."""
    if "pos" not in nlp.processors:
        return None
    from stanza.models.common.doc import Document
    doc = Document([[{"id": i + 1, "text": src[g[0].start_char:g[-1].end_char]}
                     for i, g in enumerate(groups)]])
    for p in ("pos", "lemma"):
        if p in nlp.processors:
            nlp.processors[p].process(doc)
    return doc.sentences[0].words


# ----------------------------------------------------------------------------- regex (fil, si)
_END = re.compile(r"[.!?…]+[\"'”’»)\]]*(?=\s|$)|\n+")
_JOIN = "-'’"


def _word_char(c):
    # Letters and digits, plus combining marks and ZWJ/ZWNJ: Sinhala vowel signs are marks, which
    # Python's \w does not match, so a \w+ regex would cut Sinhala words apart.
    return c.isalnum() or unicodedata.category(c)[0] == "M" or c in "‌‍"


def _strip_span(text, a, b):
    while a < b and text[a].isspace():
        a += 1
    while b > a and text[b - 1].isspace():
        b -= 1
    return a, b


def _regex(lang, text):
    spans, s = [], 0
    for m in _END.finditer(text):
        e = m.start() if text[m.start()] == "\n" else m.end()
        spans.append(_strip_span(text, s, e))
        s = m.end()
    spans.append(_strip_span(text, s, len(text)))
    stop = FUNCTION_WORDS.get(lang, frozenset())
    out = []
    for a, b in spans:
        if a >= b:
            continue
        st = text[a:b].replace("\n", " ")
        sent = Sentence(st, a, b)
        i, n = 0, len(st)
        while i < n:
            if not _word_char(st[i]):
                i += 1
                continue
            j = i + 1
            while j < n and (_word_char(st[j]) or (st[j] in _JOIN and j + 1 < n
                                                   and _word_char(st[j + 1]))):
                j += 1
            w = st[i:j]
            sent.words.append(Word(w, i, j, content=_has_letter(w) and w.lower() not in stop))
            i = j
        out.append(sent)
    return out


# ----------------------------------------------------------------------------- prepare
def prepare(langs=data.STANZA_LANGS):
    """Unpack the stanza default packages, as `data._lemmatize` does (stanza.download)."""
    import stanza
    for lg in langs:
        t0 = time.perf_counter()
        stanza.download(lg, verbose=False)
        print(f"[stanza] {lg} ready in {time.perf_counter() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--prepare", action="store_true", help="unpack the stanza models once")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--text", default=None, help="print the segmentation of this text")
    a = ap.parse_args()
    if a.prepare:
        prepare()
    if a.text:
        for s in Segmenter().segment(a.lang, a.text):
            print(f"[{s.start}:{s.end}] {s.text}")
            print("   ", " ".join(f"{w.text}/{w.upos or '-'}{'*' if w.content else ''}"
                                  for w in s.words))
