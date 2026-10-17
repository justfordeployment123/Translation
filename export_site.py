"""Build a one-page static website with all recordings, ready to upload to any web server.

Usage:
    python3 export_site.py out/page_001_axee out/page_002_axee [...]
    python3 export_site.py out/page_001_axee out/page_002_axee --single-file download/all_pages.html

The recordings are played in the order given, on one page, with each page's scan shown beside
the text. Creates site/ (index.html, audio/, images/, chapters/ with one MP3 per chapter) and site.zip.
The site is plain HTML + MP3 + PNG: no Python, no API key and no backend are needed on the server.
Upload the contents of site/ (or unzip site.zip) into any folder your web server serves, or run
./deploy.sh. --single-file also writes the same page as one self-contained HTML file.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

from make_sample import data_uri, render_player

MARKER = ".generated-by-export-site"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recordings", nargs="+", help="folders made by make_sample.py, e.g. out/page_001_axee")
    ap.add_argument("--out", default="site", help="output folder (default: site)")
    ap.add_argument("--title", default="Audio Sample")
    ap.add_argument("--single-file", help="also write a self-contained HTML file to this path")
    args = ap.parse_args()

    site = Path(args.out)
    if site.exists():
        if not (site / MARKER).exists():
            sys.exit(f"{site}/ already exists and was not made by this script; choose another --out.")
        shutil.rmtree(site)
    (site / "audio").mkdir(parents=True)
    (site / "images").mkdir()
    (site / MARKER).touch()

    segments, pages, names = [], [], set()
    for folder in map(Path, args.recordings):
        sync_file = folder / "sync.json"
        if not sync_file.exists():
            sys.exit(f"{sync_file} not found: generate the recording with make_sample.py first.")
        sync = json.loads(sync_file.read_text(encoding="utf-8"))
        name = sync["page"] if sync["page"] not in names else folder.name
        names.add(name)
        page = len(pages)
        for seg in sync["segments"]:
            if "audio" not in seg:  # [ref] blocks are text only
                segments.append({**seg, "page": page})
                continue
            dest = f"audio/{name}_{seg['audio']}"
            shutil.copy(folder / seg["audio"], site / dest)
            segments.append({**seg, "audio": dest, "page": page})
        image = ""
        if "image" in sync:
            image = f"images/{name}.png"
            shutil.copy(folder / sync["image"], site / image)
        pages.append({"title": sync["title"], "image": image})
        print(f"Added {folder}")

    # One MP3 per chapter: a new chapter starts on a page whose first heading begins with "باب"
    # (pages before the first chapter form the introduction). MP3 frames are self-contained, so
    # joining the files byte-for-byte plays back fine.
    parts, page = [], None
    for seg in segments:
        text = " ".join(w["w"] for w in seg.get("words", []))
        opens_page, page = seg["page"] != page, seg["page"]
        if opens_page and seg.get("style") == "h" and text.startswith("باب"):
            parts.append({"label": text.split(":")[0], "audio": []})
        elif not parts:
            parts.append({"label": "مقدمہ و تمہید", "audio": []})
        if "audio" in seg:
            parts[-1]["audio"].append(seg["audio"])
    (site / "chapters").mkdir()
    downloads = []
    for n, part in enumerate(parts, 1):
        name = f"chapters/part_{n:02d}.mp3"
        (site / name).write_bytes(b"".join((site / a).read_bytes() for a in part["audio"]))
        downloads.append((part["label"], name))
    (site / "index.html").write_text(render_player(args.title, segments, pages, downloads), encoding="utf-8")
    archive = shutil.make_archive(str(site), "zip", site)
    print(f"Done: {site}/index.html, {len(downloads)} chapter MP3s in {site}/chapters/ and {archive}")

    if args.single_file:
        embedded = [{**s, "audio": data_uri(site / s["audio"], "audio/mpeg")} if "audio" in s else s for s in segments]
        embedded_pages = [{**p, "image": data_uri(site / p["image"], "image/png") if p["image"] else ""} for p in pages]
        Path(args.single_file).parent.mkdir(parents=True, exist_ok=True)
        Path(args.single_file).write_text(render_player(args.title, embedded, embedded_pages), encoding="utf-8")
        print(f"Single file: {args.single_file}")

if __name__ == "__main__":
    main()
