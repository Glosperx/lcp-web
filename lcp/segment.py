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
        doc = self.pipeline(lang)(text)
        out = []
        for sn in doc.sentences:
            toks = [t for t in sn.tokens if t.start_char is not None and t.end_char is not None]
            if not toks:
                continue
            s0, s1 = toks[0].start_char, toks[-1].end_char
            sent = Sentence(text[s0:s1].replace("\n", " "), s0, s1)
            for t in toks:
                upos = [w.upos or "" for w in t.words]
                content = [u for u in upos if u in CONTENT_UPOS]
                form = text[t.start_char:t.end_char]
                sent.words.append(Word(
                    form, t.start_char - s0, t.end_char - s0,
                    lemma=" ".join(w.lemma for w in t.words if w.lemma),
                    upos=(content or upos or [""])[0],
                    content=bool(content) and _has_letter(form)))
            out.append(sent)
        return out


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
