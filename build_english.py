"""Build English page files from the English translation and the Urdu page files.

Each file in books/zindagi-aur-waqt/en_src/ holds only the English blocks of a page: one [en] block for
every [ur] block of the Urdu page, one [hen] block for every [h] heading, and one [fen] block for every
[fn] footnote, in the same order. This script interleaves them with the Urdu page's [ar] and [ref] blocks
(copied unchanged, so the Arabic is never retyped) and writes books/zindagi-aur-waqt/en/page_NNN.txt.

Inside an [en] block, a line {{QEN 23:112 23:113}} is replaced with the Sahih International English
translation of those ayat (from api.alquran.cloud), so Quran translations are never our own wording.

Usage:
    python3 build_english.py 13-24                          # Zindagi Aur Waqt
    python3 build_english.py 17-564 --book haraam-karobaar --parens  # another book, by its folder in books/
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from functools import lru_cache
from pathlib import Path

from make_sample import parse_page

BOOKS = Path(__file__).parent / "books"
BOOK = BOOKS / "zindagi-aur-waqt"  # set by --book
PARENS = False  # set by --parens: keep Sahih International's [added words] as (added words)
PAIRS = {"ur": "en", "h": "hen", "fn": "fen"}
QEN = re.compile(r"\{\{QEN ([\d: ]+)\}\}")


@lru_cache(maxsize=None)
def sahih_raw(ref):
    url = f"https://api.alquran.cloud/v1/ayah/{ref}/en.sahih"
    for attempt in range(5):  # the API sometimes times out or returns 503 for a moment
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                text = json.load(resp)["data"]["text"]
            break
        except OSError:
            if attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))
    return text


def sahih(*refs):
    """Sahih International's text of one or more ayat, joined before the quote marks are made curly, so a
    quotation that runs from one ayah into the next opens and closes correctly."""
    texts = [sahih_raw(r).strip() for r in refs]
    if PARENS:  # an ayah that ends with no punctuation gets Sahih's own dash before the next one, so the voice pauses
        texts = [x if k == len(texts) - 1 or re.search(r"[.,;:!?\"”’)—–-]$", x) else x + " -" for k, x in enumerate(texts)]
    text = " ".join(texts)
    if PARENS:  # this book's style: Sahih's [added words] as (added words), and curly quote marks
        text = text.replace("[", "(").replace("]", ")")
        # a mark at the start or after a space, dash or bracket opens a quotation, any other closes one, so an
        # ayah that closes a quotation opened in the ayah before it still gets a closing mark
        text = re.sub(r'(^|(?<=[\s(—–-]))"', "“", text).replace('"', "”")
        text = balance(text)
        # an ayah whose sentence runs on into the next ends with Sahih's dash or comma: end the block with a full stop
        text = re.sub(r"\s*[-–—,;]\s*$", ".", text.strip())
    else:
        text = text.replace("[", "").replace("]", "")
    return " ".join(text.split())


def balance(text):
    """Drop curly quote marks that have no partner in the block (a quotation that Sahih opens or closes in
    another ayah), so a verse quoted on its own does not show a stray mark."""
    keep, opened = [], []
    for k, ch in enumerate(text):
        if ch == "“":
            opened.append(k)
        elif ch == "”":
            if opened:
                opened.pop()
            else:
                keep.append(k)
    drop = set(keep) | set(opened)
    return "".join(ch for k, ch in enumerate(text) if k not in drop).replace("  ", " ")


def build(n):
    urdu = parse_page(BOOK / f"page_{n:03d}.txt")
    src = BOOK / "en_src" / f"page_{n:03d}.txt"
    english = parse_page(src)
    wanted = [PAIRS[tag] for tag, _ in urdu if tag in PAIRS]
    got = [tag for tag, _ in english]
    if wanted != got:
        sys.exit(f"page {n}: the Urdu page needs blocks {wanted}, but {src.name} has {got}")
    blocks, k = [], 0
    for tag, text in urdu:
        if tag in PAIRS:
            etag, etext = english[k]
            k += 1
            etext = QEN.sub(lambda m: sahih(*m.group(1).split()), etext)
            blocks.append(f"[{etag}]\n{' '.join(etext.split())}")
        else:  # [ar] and [ref] are copied from the Urdu page unchanged
            blocks.append(f"[{tag}]\n{' '.join(text.split())}")
    out = BOOK / "en" / f"page_{n:03d}.txt"
    out.parent.mkdir(exist_ok=True)
    header = f"# title: Page {n}\n# English edition of book page {n}, built by build_english.py from en_src/ and page_{n:03d}.txt\n\n"
    out.write_text(header + "\n\n".join(blocks) + "\n", encoding="utf-8")
    return out


def main():
    global BOOK, PARENS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", help="book page range, e.g. 13-24")
    ap.add_argument("--book", default=BOOK.name, help="the book's folder in books/ (default: %(default)s)")
    ap.add_argument("--parens", action="store_true",
                    help="keep Sahih International's bracketed added words, as (words), instead of dropping the brackets")
    args = ap.parse_args()
    BOOK = BOOKS / args.book
    PARENS = args.parens
    first, last = map(int, args.pages.split("-"))
    for n in range(first, last + 1):
        if not (BOOK / f"page_{n:03d}.txt").exists():
            continue  # a page with no text of its own (a photo, a blank page)
        print(build(n).relative_to(BOOK.parent.parent))


if __name__ == "__main__":
    main()
