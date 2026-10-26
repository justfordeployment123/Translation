"""Build a local preview of a book's text: every page with its scan, Urdu and English side by side.

It needs no recordings, so a book can be read and reviewed before any credits are spent on it. The page
shows each block as it will be spoken (headings, Urdu, Arabic, references), the page file's header notes
("Proofreader please check" highlighted), and a chapter list.

Usage:
    python3 preview_book.py haraam-karobaar                      # writes preview/haraam-karobaar.html
    python3 -m http.server 8790 --bind 127.0.0.1                 # then open http://localhost:8790/preview/haraam-karobaar.html
"""
import html
import json
import re
import sys
from pathlib import Path

from make_sample import parse_page

ROOT = Path(__file__).parent
HEADINGS = {"haraam-karobaar": "100 حرام کاروبار", "salaf-aqaid": "سلف صالحین کے عقائد و نظریات"}
# headings that start a chapter or a front section, listed in the preview's contents
CHAPTER = re.compile(r"(\sباب\s*:|دورہ|اصول\s*:|^خلاصہ|^مقدمہ|^عرضِ ناشر|^پیش لفظ|^ضروری تعریفیں)")


def pages(book):
    folder = ROOT / "books" / book
    out = []
    for f in sorted(folder.glob("page_*.txt"), key=lambda p: int(p.stem[5:])):
        n = int(f.stem[5:])
        en = folder / "en" / f.name
        scan = next((s for s in (folder / "scans" / f"page_{n:03d}.jpg", folder / f"page_{n:03d}.png") if s.exists()), None)
        notes = [l[1:].strip() for l in f.read_text(encoding="utf-8").splitlines()
                 if l.startswith("#") and not l.startswith(("# title:", "# quran ", "# hadith "))
                 and not re.search(r"book page \d+ \(PDF page", l)]
        out.append({
            "n": n,
            "scan": f"../{scan.relative_to(ROOT)}" if scan else "",
            "notes": notes,
            "ur": parse_page(f),
            "en": parse_page(en) if en.exists() else [],
        })
    return out


def toc(book_pages):
    entries = []
    for i, p in enumerate(book_pages):
        heads = [t for tag, t in p["ur"] if tag == "h"]
        en_heads = [t for tag, t in p["en"] if tag == "hen"]
        for k, h in enumerate(heads):
            if CHAPTER.search(h):
                entries.append({"i": i, "ur": h, "en": en_heads[k] if k < len(en_heads) else ""})
    return entries


def main():
    book = sys.argv[1] if len(sys.argv) > 1 else "haraam-karobaar"
    data = pages(book)
    template = (ROOT / "preview_template.html").read_text(encoding="utf-8")
    page = template.replace("{{TITLE}}", html.escape(book)).replace("{{HEADING}}", html.escape(HEADINGS.get(book, book))).replace(
        "{{DATA}}", json.dumps({"book": book, "pages": data, "toc": toc(data)}, ensure_ascii=False).replace("</", "<\\/"))
    out = ROOT / "preview" / f"{book}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(data)} pages, {sum(1 for p in data if p['en'])} with English")


if __name__ == "__main__":
    main()
