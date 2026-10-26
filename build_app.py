"""Build the reading app (bookshelf, synced text, docked controls) as a static website.

Usage:
    python3 build_app.py                       # every book in BOOKS, all its pages
    python3 build_app.py --out site_test

For each book and page it uses out/page_NNN_<suffix> (one suffix per edition, see BOOKS). Creates
<out>/ (index.html, audio/, images/) and <out>.zip, plus <out>_chapters/ with one audio file per chapter
for download. The chapter files are published as GitHub Release assets (see --chapters-url), not on
GitHub Pages, so the site stays well under the Pages size limit. The site is plain HTML + MP3 + images:
no backend and no API key are needed on the server.
"""
import argparse
import html
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from make_sample import mp3_seconds, parse_page

ROOT = Path(__file__).parent
MARKER = ".generated-by-export-site"
SHELF_SIZE = 15
RELEASE = "https://github.com/justfordeployment123/Translation/releases/download/chapters"
BOOKS = [
    {
        "id": "zindagi-aur-waqt", "title": "زندگی اور وقت", "subtitle": "Zindagi Aur Waqt", "en_title": "Life and Time",
        "author": "ابو محمد عزیر یونس السلفی المدنی", "en_author": "Abu Muhammad Uzair Younus as-Salafi al-Madani",
        "publisher": "مکتبہ دار التوحید الاسلامیہ", "en_publisher": "Maktaba Dar at-Tawhid al-Islamiyyah",
        "blurb": "وقت کی قدر و قیمت پر قرآن، احادیث اور اقوالِ سلف کی روشنی میں ایک جامع کتاب۔",
        "en_blurb": "A guide to the value of time, drawn from the Quran, the hadith and the words of the righteous predecessors.",
        # build settings (not sent to the page): edition -> out/ folder suffix, page range, and the folder
        # prefix for its audio and images ("" keeps the first book's URLs as they were)
        "_editions": {"ur": "george", "en": "en"}, "_pages": (13, 178), "_prefix": "",
    },
    {
        "id": "shab-o-roz", "title": "شب و روز کے مسنون اعمال", "subtitle": "Shab o Roz ke Masnoon Amaal",
        "en_title": "Sunnahs of Day and Night",
        "author": "ڈاکٹر عبداللہ بن حمود الفریح", "en_author": "Dr. Abdullah bin Hamood al-Furaih",
        "blurb": "دن اور رات کی ثابت شدہ قولی و فعلی سنتیں، صحیح احادیث کے دلائل کے ساتھ۔",
        "en_blurb": "The established sunnahs of day and night, each with its proof from authentic hadith.",
        "_editions": {"ur": "sr"}, "_pages": (17, 170), "_prefix": "shab-o-roz/",
        "_scans": "books/shab-o-roz/scans/page_{n:03d}.jpg",
        # this book has no "باب" chapters: its contents are these sections (book page -> label), and the
        # chapter downloads start at the pages listed in _parts
        "_toc": {
            17: "تقریظ", 19: "مقدمہ", 22: "تمہید", 29: "خاص اوقات کی سنتیں",
            30: "فجر سے پہلے کرنے والے اعمال اور سنتیں", 52: "فجر کے وقت کرنے والے اعمال اور سنتیں",
            100: "چاشت کے وقت کرنے والے اعمال اور سنتیں", 103: "ظہر کے وقت کرنے والے اعمال اور سنتیں",
            105: "عصر کے وقت کرنے والے اعمال اور سنتیں", 108: "مغرب کے وقت کرنے والے اعمال اور سنتیں",
            111: "وقتِ عشاء", 113: "نیند کی سنتیں", 129: "روزمرہ کے غیر مقید اعمال اور سنتیں",
            130: "کھانے کے وقت کی سنتیں", 140: "سلام، ملاقات اور مجلس کے اوقات کی سنتیں",
            149: "لباس اور زیب و زینت کے اوقات کی سنتیں", 152: "چھینک اور جمائی کے اوقات کی سنتیں",
            156: "عام روز مرہ کی سنتیں",
        },
        "_parts": {
            17: "تقریظ، مقدمہ و تمہید", 29: "فجر سے پہلے کی سنتیں", 52: "فجر کے وقت کی سنتیں",
            100: "چاشت، ظہر اور عصر کی سنتیں", 108: "مغرب اور عشاء کی سنتیں", 113: "نیند کی سنتیں",
            129: "کھانے پینے کی سنتیں", 140: "سلام، ملاقات اور مجلس کی سنتیں",
            149: "لباس، چھینک اور جمائی کی سنتیں", 156: "عام روز مرہ کی سنتیں",
        },
    },
    {
        "id": "salaf-aqaid", "title": "سلف صالحین کے عقائد و نظریات", "subtitle": "Salaf-e-Saliheen ke Aqaid o Nazariyat",
        "en_title": "The Beliefs and Doctrines of the Righteous Predecessors",
        "author": "الشیخ عبداللہ بن عبدالحمید اثری", "en_author": "Shaykh Abdullah ibn Abd al-Hamid al-Athari",
        "publisher": "دارالسلام", "en_publisher": "Darussalam",
        "blurb": "اہل سنت والجماعت کا عقیدہ، اصول بہ اصول، قرآن و حدیث کے دلائل کے ساتھ۔",
        "en_blurb": "The creed of Ahl as-Sunnah wal-Jama'ah, principle by principle, with its proofs from the Quran and the hadith.",
        "_editions": {"ur": "sa", "en": "saen"}, "_pages": (10, 196), "_prefix": "salaf-aqaid/",
        "_scans": "books/salaf-aqaid/scans/page_{n:03d}.jpg",
        # the book's sections are its principles («پہلا اصول»), not «باب» chapters; labels per edition
        "_toc": {
            10: {"ur": "عرضِ ناشر", "en": "Publisher's Note"}, 13: {"ur": "پیش لفظ", "en": "Foreword"},
            26: {"ur": "مقدمہ", "en": "Introduction"}, 31: {"ur": "ضروری تعریفیں", "en": "Essential Definitions"},
            60: {"ur": "پہلا اصول: ایمان اور ارکانِ ایمان", "en": "The First Principle: Faith and the Pillars of Faith"},
            126: {"ur": "دوسرا اصول: حقیقتِ ایمان", "en": "The Second Principle: The Reality of Faith"},
            139: {"ur": "تیسرا اصول: مسئلہ تکفیر", "en": "The Third Principle: Takfir"},
            150: {"ur": "چوتھا اصول: وعدہ وعید کی نصوص پر ایمان", "en": "The Fourth Principle: The Promises and the Warnings"},
            159: {"ur": "پانچواں اصول: دوستی اور دشمنی", "en": "The Fifth Principle: Loyalty and Disavowal"},
            170: {"ur": "چھٹا اصول: کراماتِ اولیاء کی تصدیق", "en": "The Sixth Principle: The Karamat of the Friends of Allah"},
            179: {"ur": "ساتواں اصول: احکام و مسائل اخذ کرنے کے ذرائع", "en": "The Seventh Principle: The Sources of Rulings"},
            188: {"ur": "آٹھواں اصول: مسلمان حکمرانوں کی اطاعت", "en": "The Eighth Principle: Obeying Muslim Rulers"},
        },
        "_parts": {
            10: {"ur": "عرضِ ناشر، پیش لفظ و مقدمہ", "en": "Publisher's Note, Foreword and Introduction"},
            31: {"ur": "ضروری تعریفیں", "en": "Essential Definitions"},
            60: {"ur": "پہلا اصول", "en": "The First Principle"}, 126: {"ur": "دوسرا اصول", "en": "The Second Principle"},
            139: {"ur": "تیسرا اصول", "en": "The Third Principle"}, 150: {"ur": "چوتھا اصول", "en": "The Fourth Principle"},
            159: {"ur": "پانچواں اصول", "en": "The Fifth Principle"}, 170: {"ur": "چھٹا اصول", "en": "The Sixth Principle"},
            179: {"ur": "ساتواں اصول", "en": "The Seventh Principle"}, 188: {"ur": "آٹھواں اصول", "en": "The Eighth Principle"},
        },
    },
]
TOC_WORDS = ("باب", "مقدمہ", "تمہید", "Chapter", "Introduction", "Preface")


def load_edition(site, book, lang, suffix):
    """Pages and segments of one edition, with its audio and scans copied into the site."""
    pages, segments = [], []
    prefix = book["_prefix"]
    first, last = book["_pages"]
    for n in range(first, last + 1):
        folder = ROOT / "out" / f"page_{n:03d}_{suffix}"
        if not (folder / "sync.json").exists():
            continue
        sync = json.loads((folder / "sync.json").read_text(encoding="utf-8"))
        index = len(pages)
        # explanatory footnotes ([fn] / [fen]) are shown as footnote paragraphs, not centred like a reference
        source = ROOT / "books" / book["id"] / ("en" if lang == "en" else "") / f"page_{n:03d}.txt"
        notes = {" ".join(x.split()) for tag, x in parse_page(source) if tag in ("fn", "fen")} if source.exists() else set()
        for seg in sync["segments"]:
            if seg.get("style") == "ref" and seg["text"] in notes:
                seg = {**seg, "fn": 1}
            if "audio" in seg:
                dest = f"audio/{prefix}{lang}/{n:03d}_{seg['audio']}"
                (site / dest).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(folder / seg["audio"], site / dest)
                seg = {**seg, "audio": dest, "d": round(mp3_seconds(folder / seg["audio"]), 2)}
            segments.append({**seg, "page": index})
        scan = folder / sync["image"] if "image" in sync else ROOT / book.get("_scans", "-").format(n=n)
        image = ""
        if scan.exists():
            image = f"images/{prefix}page_{n:03d}{scan.suffix}"
            if not (site / image).exists():
                (site / image).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(scan, site / image)
        pages.append({"number": n, "image": image})
    if not pages:
        return None
    toc = []
    if "_toc" in book:  # the book's own list of sections
        for number, label in book["_toc"].items():
            index = next((k for k, pg in enumerate(pages) if pg["number"] == number), None)
            if index is not None:  # sections not recorded yet are left out
                toc.append({"label": label[lang] if isinstance(label, dict) else label, "page": index})
    else:  # chapter, introduction and preface headings
        for seg in segments:
            text = " ".join(w["w"] for w in seg.get("words", []))
            if seg.get("style") == "h" and text.startswith(TOC_WORDS):
                toc.append({"label": text, "page": seg["page"]})
    seconds = sum(s.get("d", 0) for s in segments)
    return {"pages": pages, "segments": segments, "toc": toc, "seconds": round(seconds)}


INTRO = {"ur": "مقدمہ و تمہید", "en": "Introduction and Preface"}
CHAPTER = {"ur": "باب", "en": "Chapter"}


def chapter_mp3s(site, chapters, book, lang, edition, url):
    """One audio file per chapter, named in the edition's language, written to the chapters folder and
    linked at url/<file>. A chapter starts on the page of a table of contents entry that begins with "باب" /
    "Chapter" (or, for a book with _parts, on each listed page); the pages before it are the introduction."""
    if "_parts" in book:
        numbers = [pg["number"] for pg in edition["pages"]]
        starts = {numbers.index(k): v[lang] if isinstance(v, dict) else v for k, v in book["_parts"].items() if k in numbers}
    else:
        starts = {t["page"]: t["label"].split(":")[0] for t in edition["toc"] if t["label"].startswith(CHAPTER[lang])}
    parts = []
    for seg in edition["segments"]:
        if seg["page"] in starts and (not parts or parts[-1]["start"] != seg["page"]):
            parts.append({"label": starts[seg["page"]], "start": seg["page"], "audio": []})
        elif not parts:
            parts.append({"label": INTRO[lang], "start": seg["page"], "audio": []})
        if "audio" in seg:
            parts[-1]["audio"].append(seg["audio"])
    links = []
    for n, part in enumerate(parts, 1):
        joined = chapters / f"{book['id']}_{lang}_part_{n:02d}.mp3"
        # MP3 frames are self-contained, so joining the files byte-for-byte plays back fine
        joined.write_bytes(b"".join((site / a).read_bytes() for a in part["audio"]))
        name = compress(joined).name
        seconds = round(sum(seg.get("d", 0) for seg in edition["segments"] if seg.get("audio") in part["audio"]))
        links.append({"label": part["label"], "href": f"{url.rstrip('/')}/{name}", "seconds": seconds})
    return links


def compress(mp3):
    """Re-encode a chapter as 48 kbps mono AAC (.m4a) with macOS afconvert: about 40% of the size, the
    same quality for speech, and players see the true length (a joined MP3 reports only its first
    part's length). Without afconvert the MP3 is kept."""
    if not shutil.which("afconvert"):
        return mp3
    m4a = mp3.with_suffix(".m4a")
    subprocess.run(["afconvert", str(mp3), "-o", str(m4a), "-f", "m4af", "-d", "aac", "-b", "48000", "-c", "1"], check=True)
    mp3.unlink()
    return m4a


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="site")
    ap.add_argument("--title", default="Noor Library · نور لائبریری")
    ap.add_argument("--chapters-url", default=RELEASE, help="where the chapter files are published")
    args = ap.parse_args()

    site = ROOT / args.out
    chapters = ROOT / f"{args.out}_chapters"
    for folder in (site, chapters):
        if folder.exists():
            if not (folder / MARKER).exists():
                sys.exit(f"{folder}/ already exists and was not made by this script; choose another --out.")
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        (folder / MARKER).touch()
    (site / "images").mkdir()

    shelf, downloads = [], {}
    for book in BOOKS:
        editions = {}
        for lang, suffix in book["_editions"].items():
            edition = load_edition(site, book, lang, suffix)
            if edition:
                editions[lang] = edition
                print(f"{book['id']} {lang}: {len(edition['pages'])} pages, {sum(1 for s in edition['segments'] if 'audio' in s)} audio parts")
        if "ur" not in editions:
            sys.exit(f"{book['id']}: no Urdu recordings found.")
        downloads[len(shelf)] = {lang: chapter_mp3s(site, chapters, book, lang, ed, args.chapters_url) for lang, ed in editions.items()}
        shelf.append({**{k: v for k, v in book.items() if not k.startswith("_")}, "editions": editions})

    books = shelf + [{"soon": True} for _ in range(len(shelf) + 1, SHELF_SIZE + 1)]
    as_json = lambda data: json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = (ROOT / "app_template.html").read_text(encoding="utf-8")
    page = page.replace("{{TITLE}}", html.escape(args.title)).replace("{{DOWNLOADS}}", as_json(downloads)).replace("{{BOOKS}}", as_json(books))
    (site / "index.html").write_text(page, encoding="utf-8")
    # installable-app files: manifest, icons and the offline service worker (versioned per build)
    assets = ROOT / "app_assets"
    shutil.copy(assets / "manifest.webmanifest", site / "manifest.webmanifest")
    shutil.copytree(assets / "icons", site / "icons")
    version = str(int(time.time()))
    (site / "sw.js").write_text((assets / "sw.js").read_text(encoding="utf-8").replace("{{VERSION}}", version), encoding="utf-8")
    archive = shutil.make_archive(str(site), "zip", site)
    print(f"Done: {site}/index.html, {archive} and the chapter files in {chapters}/")


if __name__ == "__main__":
    main()
