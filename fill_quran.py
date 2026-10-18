"""Fill Quran verses into page files from the official text, and check them.

In a page file, write a verse as a placeholder inside an [ar] block:
    {{Q 23:99}}                     the whole ayah
    {{Q 18:28 from وَلَا تُطِعْ}}     the ayah from that phrase to the end, when the book quotes only part
    {{Q 35:37 to كُنَّا نَعْمَلُ}}     the ayah from its start up to and including that phrase
Phrases are matched by their letters only, so their harakat don't have to match exactly.

Usage:
    python3 fill_quran.py books/zindagi-aur-waqt/page_021.txt [...]   # fill placeholders, then check
    python3 fill_quran.py --check books/zindagi-aur-waqt/*.txt        # check only

The text comes from api.alquran.cloud (Tanzil "quran-simple": standard spelling with full harakat).
The only change made is the stopping form (waqf) of the last word, as a qari reads at the end of an
ayah. Each filled verse is marked with a "# quran ..." comment so --check can verify it later.
"""
import json
import re
import sys
import time
import urllib.request
from functools import lru_cache
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{Q (\d+:\d+)(?: from (.+?))?(?: to (.+?))?\}\}")
MARKER = re.compile(r"^# quran (\d+:\d+)(?: from (.+?))?(?: to (.+))?$")
MARKS = re.compile("[ً-ٰٟۖ-ۭ]")  # harakat and Quranic pause signs
VOWELS = re.compile("[ً-ِ]")


BISMILLAH = ["بسم", "الله", "الرحمن", "الرحيم"]


@lru_cache(maxsize=None)
def ayah(ref):
    url = f"https://api.alquran.cloud/v1/ayah/{ref}/quran-simple"
    for attempt in range(5):  # the API sometimes times out or returns 503 for a moment
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                text = json.load(resp)["data"]["text"]
            break
        except OSError:
            if attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))
    # the API puts the Bismillah in front of ayah 1 of every surah; it is not part of that ayah
    # (except in Al-Fatiha, where it is ayah 1 itself)
    words = text.split(" ")
    surah, number = ref.split(":")
    if number == "1" and surah != "1" and [MARKS.sub("", w) for w in words[:4]] == BISMILLAH:
        text = " ".join(words[4:])
    return text


def waqf(text):
    """The last word as read when stopping: tanween fath + alif -> fatha + alif; any other final
    vowel -> sukun, or just dropped when the letter has a shadda."""
    match = re.search("([ً-ْ]+)([اى]?)$", text)
    if not match:
        return text
    marks, alif = match.groups()
    if alif:
        return text[: match.start()] + marks.replace("ً", "َ") + alif
    if not VOWELS.search(marks):
        return text
    kept = VOWELS.sub("", marks)
    return text[: match.start()] + (kept if "ّ" in kept else kept + "ْ")


def _find(words, phrase, ref):
    """(start, end) indexes into `words` where `phrase` occurs, comparing letters only and
    skipping standalone pause signs."""
    real = [i for i, w in enumerate(words) if MARKS.sub("", w)]
    skeletons = [MARKS.sub("", words[i]) for i in real]
    want = [MARKS.sub("", w) for w in phrase.split()]
    for k in range(len(skeletons) - len(want) + 1):
        if skeletons[k : k + len(want)] == want:
            return real[k], real[k + len(want) - 1] + 1
    sys.exit(f"'{phrase}' not found in {ref}: {ayah(ref)}")


def verse(ref, start=None, end=None):
    words = ayah(ref).split(" ")
    first = _find(words, start, ref)[0] if start else 0
    last = _find(words, end, ref)[1] if end else len(words)
    return waqf(" ".join(words[first:last]))


def fill(path):
    """Replace placeholders with verses, and refresh verses already filled in (the line after
    each "# quran" marker) so a fix to this script reaches every page."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    out = []
    skip = False
    for line in lines:
        if skip:
            skip = False
            continue
        match = PLACEHOLDER.fullmatch(line.strip())
        marker = MARKER.match(line)
        if match:
            ref, start, end = match.groups()
            out.append(f"# quran {ref}" + (f" from {start}" if start else "") + (f" to {end}" if end else ""))
            out.append(verse(ref, start, end))
        elif marker:
            out.append(line)
            out.append(verse(*marker.groups()))
            skip = True
        else:
            out.append(line)
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8")


def check(path):
    """Return the number of verses in `path` that differ from the official text."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    bad = 0
    for i, line in enumerate(lines):
        if PLACEHOLDER.search(line):
            print(f"{path}: unfilled placeholder: {line.strip()}")
            bad += 1
        match = MARKER.match(line)
        if match:
            ref, start, end = match.groups()
            ok = lines[i + 1].strip() == verse(ref, start, end)
            print(f"{path}: {ref} {'OK, identical to the official text' if ok else 'DIFFERENT from the official text'}")
            bad += not ok
    return bad


def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    paths = [a for a in args if a != "--check"]
    if not check_only:
        for p in paths:
            fill(p)
    bad = sum(check(p) for p in paths)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
