"""Draw the app icons (an open book on a pink gradient) into app_assets/icons/."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).parent / "icons"


def icon(size, maskable=False, radius=0.22):
    s = 1024
    img = Image.new("RGB", (s, s))
    px = img.load()
    top, bottom = (255, 141, 176), (122, 36, 72)
    for y in range(s):
        for x in range(s):
            t = (x + y) / (2 * s)
            px[x, y] = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
    d = ImageDraw.Draw(img)
    scale = 0.62 if maskable else 0.74            # maskable icons keep the art inside the safe zone
    w, h = s * scale, s * scale * 0.62
    cx, cy = s / 2, s / 2 + s * 0.02
    left, right, topy = cx - w / 2, cx + w / 2, cy - h / 2
    shadow = Image.new("L", (s, s), 0)
    ImageDraw.Draw(shadow).rounded_rectangle([left, topy + 26, right, topy + h + 26], 40, fill=120)
    img.paste((70, 20, 45), mask=shadow.filter(ImageFilter.GaussianBlur(28)))
    page = (253, 240, 245)
    d.rounded_rectangle([left, topy, cx - 8, topy + h], 34, fill=page)
    d.rounded_rectangle([cx + 8, topy, right, topy + h], 34, fill=page)
    line = (214, 120, 158)
    for k in range(4):
        y = topy + h * (0.25 + k * 0.17)
        d.rounded_rectangle([left + w * 0.08, y, cx - w * 0.06, y + 12], 6, fill=line)
        d.rounded_rectangle([cx + w * 0.06, y, right - w * 0.08, y + 12], 6, fill=line)
    d.ellipse([cx - 26, topy - 70, cx + 26, topy - 18], fill=page)  # a small light above the book
    if not maskable:
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, s, s], int(s * radius), fill=255)
        bg = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        bg.paste(img, mask=mask)
        img = bg
    return img.resize((size, size), Image.LANCZOS)


OUT.mkdir(exist_ok=True)
icon(192).save(OUT / "icon-192.png")
icon(512).save(OUT / "icon-512.png")
icon(512, maskable=True).save(OUT / "icon-maskable-512.png")
icon(180, maskable=True).save(OUT / "apple-touch-icon.png")   # iOS rounds the corners itself
print("icons written")
