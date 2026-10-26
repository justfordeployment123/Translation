"""Find where a quoted hadith or Quran passage is in the official sources, from a phrase of it.

Books often cite a hadith by volume and page ("سنن الترمذي [491/5]") instead of its number, and the
number is what fill_hadith.py needs. Type a few words as printed and this lists every hadith (or ayah)
whose text contains them, with its number in the sunnah.com numbering that fill_hadith.py uses:

    python3 find_source.py "مَنْ دَخَلَ السُّوقَ فَقَالَ"                    # all collections
    python3 find_source.py "مَنْ دَخَلَ السُّوقَ" --books tirmidhi,ibnmajah
    python3 find_source.py "إِنَّهُ لَكُمْ عَدُوٌّ مُبِينٌ" --quran           # Quran ayat instead

Matching uses letters only, like fill_hadith.py, so harakat and punctuation don't have to match.
Each whole collection is downloaded once into cache/hadith_full/ (and the Quran into cache/).
"""
import argparse
import json
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

from fill_hadith import _skeleton, _words, clean

CACHE = Path(__file__).parent / "cache"
COLLECTIONS = ["bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah", "malik"]
URLS = [
    "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-{book}.min.json",
    "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1/editions/ara-{book}.min.json",
]
QURAN_URL = "https://api.alquran.cloud/v1/quran/quran-simple"


def download(urls, path):
    """The JSON at the first URL that answers, saved to `path` so it is downloaded only once."""
    if not path.exists():
        for attempt in range(6):
            try:
                with urllib.request.urlopen(urls[attempt % len(urls)], timeout=120) as resp:
                    data = resp.read()
                json.loads(data)
                break
            except Exception:
                time.sleep(3)
        else:
            sys.exit(f"could not download {urls[0]}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return json.loads(path.read_text(encoding="utf-8"))


def collection(book):
    """[(number, text)] for every hadith of the collection."""
    data = download([u.format(book=book) for u in URLS], CACHE / "hadith_full" / f"{book}.json")
    return [(h["hadithnumber"], h["text"]) for h in data["hadiths"] if h.get("text")]


def quran():
    """[("surah:ayah", text)] for the whole Quran."""
    data = download([QURAN_URL], CACHE / "quran_simple.json")
    return [(f"{s['number']}:{a['numberInSurah']}", a["text"]) for s in data["data"]["surahs"] for a in s["ayahs"]]


def search(entries, phrase):
    """Entries whose text contains the phrase's letters, word for word, with the matched words."""
    want = [_skeleton(w) for w in _words(unicodedata.normalize("NFC", phrase))]
    for ref, text in entries:
        words = _words(clean(text))
        skeletons = [_skeleton(w) for w in words]
        for i in range(len(skeletons) - len(want) + 1):
            if skeletons[i : i + len(want)] == want:
                yield ref, words, i, i + len(want)
                break


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("phrase", help="a few words of the passage, as printed")
    ap.add_argument("--books", default=",".join(COLLECTIONS), help="collections to search, comma-separated")
    ap.add_argument("--quran", action="store_true", help="search the Quran instead of the hadith collections")
    args = ap.parse_args()
    sources = [("quran", quran())] if args.quran else [(b, collection(b)) for b in args.books.split(",")]
    found = 0
    for name, entries in sources:
        for ref, words, start, end in search(entries, args.phrase):
            found += 1
            context = " ".join(words[max(0, start - 8) : end + 12])
            print(f"{ref if args.quran else f'{name}:{ref}'}  ...{context}...")
    print(f"{found} match(es)")


if __name__ == "__main__":
    main()
