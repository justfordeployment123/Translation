"""Build English page files from the English translation and the Urdu page files.

Each file in books/zindagi-aur-waqt/en_src/ holds only the English blocks of a page: one [en] block for
every [ur] block of the Urdu page, and one [hen] block for every [h] heading, in the same order. This
script interleaves them with the Urdu page's [ar] and [ref] blocks (copied unchanged, so the Arabic is
never retyped) and writes books/zindagi-aur-waqt/en/page_NNN.txt.

Inside an [en] block, a line {{QEN 23:112 23:113}} is replaced with the Sahih International English
translation of those ayat (from api.alquran.cloud), so Quran translations are never our own wording.

Usage:
    python3 build_english.py 13-24
"""
import json
import re
import sys
import urllib.request
from functools import lru_cache
from pathlib import Path

from make_sample import parse_page

BOOK = Path(__file__).parent / "books" / "zindagi-aur-waqt"
PAIRS = {"ur": "en", "h": "hen"}
QEN = re.compile(r"\{\{QEN ([\d: ]+)\}\}")


@lru_cache(maxsize=None)
def sahih(ref):
    url = f"https://api.alquran.cloud/v1/ayah/{ref}/en.sahih"
    with urllib.request.urlopen(url, timeout=60) as resp:
        text = json.load(resp)["data"]["text"]
    return " ".join(text.replace("[", "").replace("]", "").split())


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
            etext = QEN.sub(lambda m: " ".join(sahih(r) for r in m.group(1).split()), etext)
            blocks.append(f"[{etag}]\n{' '.join(etext.split())}")
        else:  # [ar] and [ref] are copied from the Urdu page unchanged
            blocks.append(f"[{tag}]\n{' '.join(text.split())}")
    out = BOOK / "en" / f"page_{n:03d}.txt"
    out.parent.mkdir(exist_ok=True)
    header = f"# title: Page {n}\n# English edition of book page {n}, built by build_english.py from en_src/ and page_{n:03d}.txt\n\n"
    out.write_text(header + "\n\n".join(blocks) + "\n", encoding="utf-8")
    return out


def main():
    first, last = map(int, sys.argv[1].split("-"))
    for n in range(first, last + 1):
        print(build(n).relative_to(BOOK.parent.parent))


if __name__ == "__main__":
    main()
