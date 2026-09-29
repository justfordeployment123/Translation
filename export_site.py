"""Build a static website from generated recordings, ready to upload to any web server.

Usage:
    python3 export_site.py out/page_001_axee [out/page_002_axee ...]

Creates site/ and site.zip. The site is plain HTML + MP3 + PNG: no Python, no API key and no
backend are needed on the server. Upload the contents of site/ (or unzip site.zip) into any
folder your web server serves, or run ./deploy.sh.
"""
import argparse
import html
import json
import shutil
import sys
from pathlib import Path

from make_sample import render_player

MARKER = ".generated-by-export-site"

INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --bg: #f7f4ee; --card: #fffdf8; --ink: #2b2118; --line: #e4dccd; --accent: #7a1f2b; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #17130f; --card: #211b16; --ink: #efe6d8; --line: #3a3129; --accent: #e59aa4; }}
  }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: system-ui, sans-serif; }}
  main {{ max-width: 640px; margin: 0 auto; padding: 32px 16px; }}
  h1 {{ font-size: 1.3rem; margin: 0 0 20px; }}
  a {{ display: block; padding: 14px 18px; margin-bottom: 10px; background: var(--card); border: 1px solid var(--line);
       border-radius: 10px; color: var(--accent); text-decoration: none; font-weight: 600; }}
</style>
</head>
<body>
<main>
  <h1>{title}</h1>
  {links}
</main>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recordings", nargs="+", help="folders made by make_sample.py, e.g. out/page_001_axee")
    ap.add_argument("--out", default="site", help="output folder (default: site)")
    ap.add_argument("--title", default="Audio Library")
    args = ap.parse_args()

    site = Path(args.out)
    if site.exists():
        if not (site / MARKER).exists():
            sys.exit(f"{site}/ already exists and was not made by this script; choose another --out.")
        shutil.rmtree(site)
    site.mkdir(parents=True)
    (site / MARKER).touch()

    links = []
    for folder in map(Path, args.recordings):
        sync_file = folder / "sync.json"
        if not sync_file.exists():
            sys.exit(f"{sync_file} not found: generate the recording with make_sample.py first.")
        sync = json.loads(sync_file.read_text(encoding="utf-8"))
        name = sync["page"] if not (site / sync["page"]).exists() else folder.name
        dest = site / name
        dest.mkdir()
        for file in [s["audio"] for s in sync["segments"]] + ([sync["image"]] if "image" in sync else []):
            shutil.copy(folder / file, dest / file)
        page_html = render_player(sync["title"], sync["segments"], sync.get("image", ""), '<a class="nav" href="../">← All pages</a>')
        (dest / "index.html").write_text(page_html, encoding="utf-8")
        links.append(f'<a href="{name}/">{html.escape(sync["title"])}</a>')
        print(f"Added {folder} -> {dest}/")

    (site / "index.html").write_text(INDEX.format(title=html.escape(args.title), links="\n  ".join(links)), encoding="utf-8")
    archive = shutil.make_archive(str(site), "zip", site)
    print(f"Done: {site}/ and {archive}")


if __name__ == "__main__":
    main()
