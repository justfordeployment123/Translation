"""Fill hadith text into page files from the authoritative collections, and check it.

In an [ar] block, write the parts you type yourself (the narrator, "قَالَ رَسُولُ اللَّهِ ...") and put the
Prophet's words in as placeholders, which may share a line with typed text:
    عَنْ أَبِي هُرَيْرَةَ رَضِيَ اللَّهُ عَنْهُ قَالَ: {{H bukhari:6419 from أَعْذَرَ to سَنَةً}}
    {{H muslim:296 from ثَلَاثَةٌ to يُزَكِّيهِمْ}} {{H muslim:296 from وَلَا يَنْظُرُ to مُسْتَكْبِرٌ}}
Phrases are matched by their letters only (harakat and punctuation are ignored).

Usage:
    python3 fill_hadith.py books/zindagi-aur-waqt/page_054.txt [...]   # fill, then check
    python3 fill_hadith.py --check books/zindagi-aur-waqt/*.txt        # check only

The text comes from the hadith-api Arabic editions (github.com/fawazahmed0/hadith-api), with the
numbering used by sunnah.com. Changes made: "صلى الله عليه وسلم" is written with full harakat, quote
marks are dropped, and the last word before each pause gets its stopping form (waqf). Each filled line
keeps its template in a "# hadith ..." comment above it, so --check can rebuild and compare it later.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.request
from functools import lru_cache
from pathlib import Path

from fill_quran import waqf

PLACEHOLDER = re.compile(r"\{\{H (\w+):(\d+)(?: from (.+?))?(?: to (.+?))?\}\}")
MARKER = "# hadith "
MARKS = re.compile("[ً-ٰٟـ]")
PUNCT = "،.:؟؛"
CACHE = Path(__file__).parent / "cache" / "hadith"
URLS = [
    "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-{book}/{number}.json",
    "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1/editions/ara-{book}/{number}.json",
]
SALLA = unicodedata.normalize("NFC", "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ")


@lru_cache(maxsize=None)
def hadith(book, number):
    """The hadith's Arabic text (isnad and matn), downloaded once and cached."""
    cached = CACHE / f"{book}_{number}.json"
    if not cached.exists():
        for attempt in range(6):
            url = URLS[attempt % len(URLS)].format(book=book, number=number)
            try:
                with urllib.request.urlopen(url, timeout=30) as resp:
                    data = json.load(resp)
                break
            except Exception:
                time.sleep(3)
        else:
            sys.exit(f"could not download {book}:{number}")
        CACHE.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    text = json.loads(cached.read_text(encoding="utf-8"))["hadiths"][0]["text"]
    text = unicodedata.normalize("NFC", text).replace("صلى الله عليه وسلم", SALLA)
    for ch in "‏\"":
        text = text.replace(ch, "")
    # some editions write yeh as ى even where it carries a vowel ("أَىُّ"); that is always ي
    text = re.sub("ى(?=[ً-ْ])", "ي", text)
    return " ".join(text.replace(" ـ ", " ").split())


SAME_LETTERS = str.maketrans({"ى": "ي", "أ": "ا", "إ": "ا", "آ": "ا"})


def _skeleton(word):
    """The word's letters only, for matching: no harakat or punctuation, and ى أ إ آ read as ي ا."""
    return MARKS.sub("", word).strip(PUNCT).translate(SAME_LETTERS)


def _find(words, phrase, ref, after=0):
    """(start, end) word indexes of the first occurrence of `phrase` at or after word `after`."""
    skeletons = [_skeleton(w) for w in words]
    want = [_skeleton(w) for w in phrase.split()]
    for i in range(after, len(skeletons) - len(want) + 1):
        if skeletons[i : i + len(want)] == want:
            return i, i + len(want)
    sys.exit(f"'{phrase}' not found in {ref}: {' '.join(words)}")


def _words(text):
    """Split into words; a stray punctuation mark (" . " or " - ") is attached to the word before it,
    so the pause it marks is kept, and other non-letter tokens are dropped."""
    words = []
    for token in text.split(" "):
        if re.search("[ء-ي]", token):
            words.append(token)
        elif words and any(p in token for p in PUNCT):
            words[-1] = words[-1].rstrip(PUNCT) + next(p for p in token if p in PUNCT)
    return words


def excerpt(book, number, start=None, end=None):
    """The words of the hadith from `start` to `end`, with waqf at every pause and at the end."""
    words = _words(hadith(book, number))
    ref = f"{book}:{number}"
    first = _find(words, start, ref)[0] if start else 0
    last = _find(words, end, ref, first)[1] if end else len(words)
    out = []
    for k, word in enumerate(words[first:last]):
        bare = word.rstrip(PUNCT)
        is_last = k == last - first - 1
        if is_last or bare != word:  # a pause: stopping form, and a comma for the voice
            out.append(waqf(bare) + ("" if is_last else "،"))
        else:
            out.append(word)
    return " ".join(out)


def render(template):
    return PLACEHOLDER.sub(lambda m: excerpt(*m.groups()), template)


def fill(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    out, skip = [], False
    for line in lines:
        if skip:
            skip = False
            continue
        if line.startswith(MARKER):  # refresh a line filled earlier
            out += [line, render(line[len(MARKER):])]
            skip = True
        elif PLACEHOLDER.search(line):
            out += [MARKER + line.strip(), render(line.strip())]
        else:
            out.append(line)
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8")


def check(path):
    """Return the number of hadith lines in `path` that differ from the source text."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    bad = 0
    for i, line in enumerate(lines):
        if not line.startswith("#") and PLACEHOLDER.search(line):
            print(f"{path}: unfilled placeholder: {line.strip()}")
            bad += 1
        if line.startswith(MARKER):
            refs = ", ".join(f"{m.group(1)}:{m.group(2)}" for m in PLACEHOLDER.finditer(line))
            ok = lines[i + 1].strip() == render(line[len(MARKER):])
            print(f"{path}: {refs} {'OK, identical to the source text' if ok else 'DIFFERENT from the source text'}")
            bad += not ok
    return bad


def main():
    args = sys.argv[1:]
    paths = [a for a in args if a != "--check"]
    if "--check" not in args:
        for p in paths:
            fill(p)
    sys.exit(1 if sum(check(p) for p in paths) else 0)


if __name__ == "__main__":
    main()
