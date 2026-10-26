"""Render a book page from its PDF as a large image plus two overlapping halves, for reading it closely.

The halves (top and bottom, overlapping by a tenth of the page) keep small words, harakat and
footnotes readable. Use a higher dpi for anything still too small.

Usage:
    python3 render_page.py 100-Haraam-Karobaar.pdf 37 --offset 1 --out /tmp/pages        # book page 37
    python3 render_page.py 100-Haraam-Karobaar.pdf 37 --offset 1 --out /tmp/pages --dpi 300

--offset is PDF page minus book page (1 for 100 Haraam Karobaar and Shab o Roz, 2 for Zindagi Aur Waqt).
Writes pNNN.png, pNNN_top.png and pNNN_bot.png into --out.
"""
import argparse
import subprocess
from pathlib import Path

from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("page", type=int, help="book page number, as printed")
    ap.add_argument("--offset", type=int, required=True, help="PDF page number minus book page number")
    ap.add_argument("--out", required=True, help="folder for the images")
    ap.add_argument("--dpi", type=int, default=220)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = out / f"p{args.page:03d}"
    pdf_page = str(args.page + args.offset)
    subprocess.run(["pdftoppm", "-f", pdf_page, "-l", pdf_page, "-r", str(args.dpi), "-png", "-gray", "-singlefile",
                    args.pdf, str(stem)], check=True)
    image = Image.open(f"{stem}.png")
    width, height = image.size
    image.crop((0, 0, width, int(height * 0.55))).save(f"{stem}_top.png")
    image.crop((0, int(height * 0.45), width, height)).save(f"{stem}_bot.png")
    print(f"{stem}_top.png\n{stem}_bot.png")


if __name__ == "__main__":
    main()
