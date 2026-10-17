"""Build the reading app (bookshelf, synced text, docked controls) as a static website.

Usage:
    python3 build_app.py --pages 13-62            # Zindagi Aur Waqt, book pages 13 to 62
    python3 build_app.py --pages 13-62 --out site

For each page it uses out/page_NNN_george (Urdu edition) and, when it exists, out/page_NNN_en (English
edition). Creates <out>/ (index.html, audio/, images/, chapters/) and <out>.zip. The site is plain
HTML + MP3 + PNG: no backend and no API key are needed on the server.
"""
import argparse
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MARKER = ".generated-by-export-site"
SHELF_SIZE = 15
BOOK = {"id": "zindagi-aur-waqt", "title": "زندگی اور وقت", "subtitle": "Zindagi Aur Waqt"}
EDITIONS = {"ur": "george", "en": "en"}  # edition -> out/ folder suffix


def load_edition(site, lang, suffix, numbers):
    """Pages and segments of one edition, with its audio and scans copied into the site."""
    pages, segments = [], []
    for n in numbers:
        folder = ROOT / "out" / f"page_{n:03d}_{suffix}"
        if not (folder / "sync.json").exists():
            continue
        sync = json.loads((folder / "sync.json").read_text(encoding="utf-8"))
        index = len(pages)
        for seg in sync["segments"]:
            if "audio" in seg:
                dest = f"audio/{lang}/{n:03d}_{seg['audio']}"
                (site / dest).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(folder / seg["audio"], site / dest)
                seg = {**seg, "audio": dest}
            segments.append({**seg, "page": index})
        image = ""
        if "image" in sync:
            image = f"images/page_{n:03d}.png"
            if not (site / image).exists():
                shutil.copy(folder / sync["image"], site / image)
        pages.append({"number": n, "image": image})
    return {"pages": pages, "segments": segments} if pages else None


def chapter_mp3s(site, lang, edition):
    """One MP3 per chapter: a chapter starts on a page whose first segment is a heading starting with "باب"."""
    parts, page = [], None
    for seg in edition["segments"]:
        text = " ".join(w["w"] for w in seg.get("words", []))
        opens_page, page = seg["page"] != page, seg["page"]
        if opens_page and seg.get("style") == "h" and text.startswith("باب"):
            parts.append({"label": text.split(":")[0], "audio": []})
        elif not parts:
            parts.append({"label": "مقدمہ و تمہید", "audio": []})
        if "audio" in seg:
            parts[-1]["audio"].append(seg["audio"])
    links = []
    for n, part in enumerate(parts, 1):
        name = f"chapters/{lang}_part_{n:02d}.mp3"
        (site / name).parent.mkdir(exist_ok=True)
        # MP3 frames are self-contained, so joining the files byte-for-byte plays back fine
        (site / name).write_bytes(b"".join((site / a).read_bytes() for a in part["audio"]))
        links.append((part["label"], name))
    return links


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages", default="13-62", help="book page range, e.g. 13-62")
    ap.add_argument("--out", default="site")
    ap.add_argument("--title", default="کتب خانہ · Audio Library")
    args = ap.parse_args()
    first, last = map(int, args.pages.split("-"))
    numbers = range(first, last + 1)

    site = ROOT / args.out
    if site.exists():
        if not (site / MARKER).exists():
            sys.exit(f"{site}/ already exists and was not made by this script; choose another --out.")
        shutil.rmtree(site)
    (site / "images").mkdir(parents=True)
    (site / MARKER).touch()

    editions = {}
    for lang, suffix in EDITIONS.items():
        edition = load_edition(site, lang, suffix, numbers)
        if edition:
            editions[lang] = edition
            print(f"{lang}: {len(edition['pages'])} pages, {sum(1 for s in edition['segments'] if 'audio' in s)} audio parts")
    if "ur" not in editions:
        sys.exit("No Urdu recordings found for that page range.")

    downloads = chapter_mp3s(site, "ur", editions["ur"])
    if "en" in editions:
        downloads.append(("English · " + args.pages, f"chapters/en_pages.mp3"))
        (site / "chapters" / "en_pages.mp3").write_bytes(
            b"".join((site / s["audio"]).read_bytes() for s in editions["en"]["segments"] if "audio" in s))

    books = [{**BOOK, "editions": editions}] + [{"title": f"کتاب {n}"} for n in range(2, SHELF_SIZE + 1)]
    links = "".join(f'<a href="{href}" download>{html.escape(label)}</a>' for label, href in downloads)
    button = f'<details class="dl"><summary class="chip" style="display:inline-flex;align-items:center">⬇ MP3</summary><div class="menu">{links}</div></details>'
    as_json = lambda data: json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = (ROOT / "app_template.html").read_text(encoding="utf-8")
    page = page.replace("{{TITLE}}", html.escape(args.title)).replace("{{DOWNLOAD}}", button).replace("{{BOOKS}}", as_json(books))
    (site / "index.html").write_text(page, encoding="utf-8")
    archive = shutil.make_archive(str(site), "zip", site)
    print(f"Done: {site}/index.html and {archive}")


if __name__ == "__main__":
    main()
