#!/usr/bin/env python3
"""Make 5 OGP candidates (1200x630) + comparison board for the Osaka guide."""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).parent
IMG = HERE.parent / "img"
OUT = HERE
OUT.mkdir(exist_ok=True)
W, H = 1200, 630
NAVY = (11, 16, 38)
PINK = (255, 62, 154)
CYAN = (55, 230, 255)
RED = (200, 16, 46)
WHITE = (255, 255, 255)

def font(bold_serif, size):
    names = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold_serif else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            continue
    return ImageFont.load_default()

def cover(im, w, h):
    im = im.convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)))
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def chip(d, x, y, text, bg, fg=WHITE, size=30, pad=16):
    f = font(False, size)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + size + pad * 1.5], radius=10, fill=bg)
    d.text((x + pad, y + pad * 0.72), text, font=f, fill=fg)
    return x + tw + pad * 2

def darken(im, box, alpha=170):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    dd.rectangle(box, fill=(5, 8, 20, alpha))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

castle = Image.open(IMG / "hero-castle.jpg")
street = Image.open(IMG / "hero-street.jpg")
tsuten = Image.open(IMG / "tsutenkaku.jpg")
doton = Image.open(IMG / "dotonbori.jpg")

# 1 — Castle Panel: photo left, navy panel right
im = Image.new("RGB", (W, H), NAVY)
im.paste(cover(castle, 660, H), (0, 0))
d = ImageDraw.Draw(im)
chip(d, 710, 120, "OSAKA · CITY GUIDE", RED)
d.text((706, 220), "Osaka", font=font(True, 120), fill=WHITE)
d.text((706, 352), "Shortlist", font=font(True, 120), fill=PINK)
d.text((710, 500), "Den Den Town first,\nthen the classics", font=font(False, 34), fill=(200, 208, 235))
im.save(OUT / "ogp-1.jpg", quality=90)

# 2 — Neon Full: Dotonbori full-bleed, big title bottom-left
im = cover(doton, W, H)
im = darken(im, (0, 380, W, H), 165)
d = ImageDraw.Draw(im)
chip(d, 48, 404, "OSAKA · CITY GUIDE", PINK, size=28)
d.text((44, 452), "Osaka Shortlist", font=font(True, 96), fill=WHITE)
d.text((48, 566), "Anime streets, classic sights & the food between", font=font(False, 30), fill=(225, 232, 255))
im.save(OUT / "ogp-2.jpg", quality=90)

# 3 — Triptych: one photo per area + navy band
im = Image.new("RGB", (W, H), NAVY)
im.paste(cover(castle, 400, 470), (0, 0))
im.paste(cover(street, 400, 470), (400, 0))
im.paste(cover(tsuten, 400, 470), (800, 0))
d = ImageDraw.Draw(im)
d.rectangle([0, 470, W, H], fill=NAVY)
d.text((44, 492), "Osaka Shortlist", font=font(True, 72), fill=WHITE)
chip(d, 800, 508, "FOR SHAUN", PINK, size=30)
d.text((48, 578), "Castle · Dotonbori · Shinsekai — and Den Den Town", font=font(False, 28), fill=(200, 208, 235))
im.save(OUT / "ogp-3.jpg", quality=90)

# 4 — Tower Type: navy, giant OSAKA, tower photo right
im = Image.new("RGB", (W, H), NAVY)
im.paste(cover(tsuten, 430, H), (770, 0))
d = ImageDraw.Draw(im)
d.text((52, 96), "OSAKA", font=font(True, 170), fill=WHITE)
d.text((56, 290), "SHORTLIST", font=font(False, 74), fill=CYAN)
chip(d, 56, 410, "OSAKA · CITY GUIDE", RED, size=28)
d.text((56, 500), "Six stops, one map,\nzero wasted yen", font=font(False, 34), fill=(200, 208, 235))
im.save(OUT / "ogp-4.jpg", quality=90)

# 5 — Street Chip: Shinsaibashi street full-bleed, oversized pink chip
im = cover(street, W, H)
im = darken(im, (0, 0, W, 240), 120)
im = darken(im, (0, 420, W, H), 170)
d = ImageDraw.Draw(im)
chip(d, 48, 52, "OSAKA · CITY GUIDE", PINK, size=40, pad=22)
d.text((44, 448), "Osaka Shortlist", font=font(True, 100), fill=WHITE)
d.text((48, 566), "For Shaun — by Yuuki, Anime Sensei", font=font(False, 30), fill=(225, 232, 255))
im.save(OUT / "ogp-5.jpg", quality=90)

# provisional og image on the page = candidate 1
import shutil
shutil.copy(OUT / "ogp-1.jpg", IMG / "og-1.jpg")

board = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OGP candidates — Osaka Shortlist</title>
<style>body{font-family:Verdana,sans-serif;background:#faf8f4;color:#111;margin:0;padding:24px}
h1{font-family:Georgia,serif;font-size:26px} .c{max-width:860px;margin:0 auto 30px}
img{width:100%;border:2.5px solid #111} .n{font-weight:bold;letter-spacing:.15em;color:#c8102e;font-size:12px;margin-bottom:6px}
p{font-size:13.5px;color:#5a554d}</style></head><body>
<h1>OGP candidates — Osaka Shortlist for Shaun</h1>
<p>Provisional og:image on the live page is No. 1 until Yuuki picks. Tell me the number and I swap it.</p>
"""
desc = [
    ("1 · Castle Panel", "Osaka Castle photo on the left, navy panel with the title on the right. Calm and classic."),
    ("2 · Neon Full", "Dotonbori at night, full-bleed, title across the bottom. The loudest of the five."),
    ("3 · Triptych", "One photo per area — castle, Shinsaibashi street, Tsutenkaku — over a navy title band."),
    ("4 · Tower Type", "Giant OSAKA type on navy with the lit-up Tsutenkaku on the right."),
    ("5 · Street Chip", "Yuuki's Shinsaibashi night shot full-bleed with an oversized pink chip."),
]
for i, (t, s) in enumerate(desc, 1):
    board += f'<div class="c"><div class="n">{t}</div><img src="ogp-{i}.jpg" alt="OGP candidate {i}"><p>{s}</p></div>\n'
board += "</body></html>"
(OUT / "index.html").write_text(board)
print("ogp done")
