#!/usr/bin/env python3
"""Build Shaun's Osaka guide page (Yulia-style)."""
import json, pathlib, urllib.parse

HERE = pathlib.Path(__file__).parent
PAGE_URL = "https://yukitchy.github.io/osaka-guide-shaun/"
OG_IMAGE = PAGE_URL + "img/og-1.jpg"  # PROVISIONAL (candidate 1) until Yuuki picks

CSS = """
:root{--ink:#111;--paper:#faf8f4;--red:#c8102e;--line:#111;--mut:#5a554d}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Verdana,Geneva,sans-serif;background:var(--paper);color:var(--ink);line-height:1.55;-webkit-text-size-adjust:100%}
img{display:block;max-width:100%}
a{color:inherit}
.hero{border-bottom:3px solid var(--ink)}
.hero-grid{display:grid;grid-template-columns:1.35fr 1fr 1fr;gap:3px;background:var(--ink)}
.hero-grid img{width:100%;height:300px;object-fit:cover}
.hero-txt{padding:26px 20px 22px;text-align:left;max-width:860px;margin:0 auto}
.kicker{font-size:11px;letter-spacing:.28em;font-weight:bold;color:var(--red)}
h1{font-family:Georgia,'Times New Roman',serif;font-size:52px;line-height:1.02;letter-spacing:.01em;margin:8px 0 6px;font-weight:700;white-space:nowrap}
h1 .accent{color:var(--red)}
.sub{font-size:13px;letter-spacing:.14em;font-weight:bold;color:var(--ink)}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
.facts{border:2.5px solid var(--ink);margin:26px auto;background:#fff}
.facts div{display:flex;gap:14px;padding:11px 16px;border-bottom:1px solid #ddd6c9;font-size:14.5px}
.facts div:last-child{border-bottom:none}
.facts b{flex:0 0 64px;font-size:11px;letter-spacing:.18em;color:var(--red);padding-top:3px}
h2{font-family:Georgia,serif;font-size:27px;margin:38px 0 4px;white-space:nowrap}
.lede{font-size:14.5px;color:var(--mut);margin-bottom:16px}
.mapbox{border:2.5px solid var(--ink);background:#101426;position:relative}
.mapbox svg{width:100%;height:auto;display:block}
.pin{cursor:pointer}
.pin .hd{fill:#111}
.pin text{fill:#fff;font-family:Verdana,sans-serif;font-weight:bold}
.pin .ph{stroke:#fff;stroke-width:2}
.pin .tail{fill:#fff}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:20px}
.card{border:2.5px solid var(--ink);background:#fff}
.card .ph{position:relative}
.card .ph img{width:100%;height:190px;object-fit:cover}
.gmap{position:absolute;top:10px;right:10px;width:40px;height:40px;background:#fff;border:2px solid var(--ink);display:flex;align-items:center;justify-content:center;text-decoration:none}
.gmap svg{width:20px;height:20px}
.card .bd{padding:13px 15px 15px}
.card .no{font-size:11px;letter-spacing:.2em;color:var(--red);font-weight:bold}
.card h3{font-family:Georgia,serif;font-size:19px;line-height:1.2;margin:3px 0 2px}
.card .rowline{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.card .hrs{font-size:12px;font-weight:bold;white-space:nowrap}
.card .hrs svg{width:12px;height:12px;vertical-align:-1px;margin-right:3px}
.card .genre{font-size:10.5px;letter-spacing:.16em;font-weight:bold;color:var(--mut)}
.card p{font-size:13.5px;margin-top:7px}
.card .area{font-size:12px;color:var(--mut);margin-top:6px}
.foodsec{background:#101426;color:#f5f1e8;margin-top:44px;padding:30px 0 36px;border-top:3px solid var(--ink);border-bottom:3px solid var(--ink)}
.foodsec h2{color:#fff;margin-top:0}
.foodsec .lede{color:#b9b2a4}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.tile{position:relative;border:2px solid #f5f1e8;text-decoration:none;color:#fff}
.tile img{width:100%;height:150px;object-fit:cover}
.tile .tg{position:absolute;top:8px;left:8px;background:var(--red);color:#fff;font-size:10px;font-weight:bold;letter-spacing:.14em;padding:3px 8px}
.tile .tm{position:absolute;left:0;right:0;bottom:0;padding:22px 10px 8px;background:linear-gradient(transparent,rgba(0,0,0,.82));display:flex;justify-content:space-between;align-items:flex-end;gap:8px}
.tile .tn{font-family:Georgia,serif;font-size:15.5px;font-weight:700;line-height:1.15}
.tile .tc{font-size:10.5px;font-weight:bold;background:#fff;color:#111;padding:2px 7px;white-space:nowrap}
.notes{margin:30px 0 8px}
.notes li{font-size:14px;margin:0 0 8px 18px}
.foot{border-top:3px solid var(--ink);margin-top:36px;padding:18px 0 30px;font-size:11.5px;color:var(--mut)}
.foot p{margin-bottom:6px}
@media(max-width:640px){
 .hero-grid img{height:190px}
 h1{font-size:37px}
 h2{font-size:22px}
 .cards{grid-template-columns:1fr}
 .tiles{grid-template-columns:1fr 1fr}
 .card .ph img{height:200px}
 .tile .tm{flex-direction:column;align-items:flex-start;gap:4px}
 .tile .tn{font-size:14px}
}
"""

CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="#c8102e"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg>'

def gmap_url(q):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)

# lat/lng -> static map projection (viewBox 600x460)
def proj(lat, lng):
    x = (lng - 135.495) / 0.040 * 600
    y = (34.695 - lat) / 0.055 * 460
    return x, y

SPOTS = [
    dict(n=1, name="MANDARAKE GRAND CHAOS", genre="USED MANGA & TOYS", hrs="12:00–20:00",
         img="img/mandarake.jpg", alt="A side street in Den Den Town, Osaka, lined with electronics and hobby shops (photo by Yuuki)",
         text="Den Den Town's Mandarake: floors of second-hand manga, figures and toys. If you collect, this is the one to dig through.",
         area="Nipponbashi 4-12-6, Den Den Town", q="Mandarake Grand Chaos Osaka", lat=34.6569, lng=135.5047, dx=-10, dy=11),
    dict(n=2, name="ANIMATE OSAKA NIPPONBASHI", genre="NEW RELEASES & GOODS", hrs="11:00–20:00",
         img="img/anime-shop.jpg", alt="Character standees and goods shelves inside an anime shop in Den Den Town, Osaka (photo by Yuuki)",
         text="The big Osaka animate, right in Den Den Town: new releases, character goods and event corners. Opens at 10:00 on weekends and holidays.",
         area="Nipponbashinishi 1-1-3, Den Den Town", q="Animate Osaka Nipponbashi", lat=34.6617, lng=135.5007, dx=-37, dy=-13),
    dict(n=3, name="SUPER POTATO OTAROAD", genre="RETRO GAMES", hrs="11:00–20:00",
         img="img/superpotato.jpg", alt="Retro game shelves inside Super Potato — photo of the same chain's Akihabara shop (Wikimedia Commons)",
         text="Retro game heaven on Otaroad: Famicom to PlayStation, boxed and loose. Opens at 10:00 on weekends and holidays. (Photo shows the same chain's Akihabara shop.)",
         area="Nipponbashi 3-8-18, Otaroad", q="Super Potato Otaroad Osaka", lat=34.6627, lng=135.5033, dx=60, dy=-55),
    dict(n=4, name="DOTONBORI", genre="NEON, SIGNS & STREET FOOD", hrs="Always open",
         img="img/dotonbori.jpg", alt="The Dotonbori canal and the Glico running man sign at night (Wikimedia Commons)",
         text="The canal, the Glico runner and a wall of giant signs: Osaka's postcard. Best after dark, and the food streets around it never really sleep.",
         area="Ebisu Bridge, Namba", q="Dotonbori Glico Sign Osaka", lat=34.6689, lng=135.5012, dx=-23, dy=-38),
    dict(n=5, name="OSAKA CASTLE", genre="CASTLE & MUSEUM", hrs="9:00–18:00",
         img="img/castle.jpg", alt="The Osaka Castle keep (photo by Yuuki)",
         text="The keep is a museum inside and the best lookout in Osaka. Last entry 17:30, and the keep is closed Dec 28 – Jan 1.",
         area="Osaka Castle Park", q="Osaka Castle", lat=34.6873, lng=135.5262, dx=0, dy=0),
    dict(n=6, name="TSUTENKAKU & SHINSEKAI", genre="TOWER & OLD OSAKA", hrs="9:00–21:45",
         img="img/tsutenkaku.jpg", alt="Tsutenkaku tower lit up over a Shinsekai street at night (photo by Yuuki)",
         text="A retro tower over Shinsekai's kushikatsu alleys. Go up for the view (last entry 21:15), then eat underneath it.",
         area="Ebisuhigashi 1-18-6, Shinsekai", q="Tsutenkaku Osaka", lat=34.6523, lng=135.5063, dx=55, dy=11),
]

FOODS = [
    dict(tag="TAKOYAKI", name="WANAKA SENNICHIMAE", hrs="10:00–23:00", img="img/food-takoyaki.jpg",
         alt="Takoyaki being grilled on a big iron plate in Osaka (photo by Yuuki)", q="たこ焼道楽 わなか 千日前本店"),
    dict(tag="OKONOMIYAKI", name="MIZUNO", hrs="11:00–22:00", img="img/food-okonomiyaki.jpg",
         alt="Okonomiyaki at a counter in Osaka (photo by Yuuki)", q="お好み焼 美津の 道頓堀"),
    dict(tag="KUSHIKATSU", name="DARUMA SHINSEKAI", hrs="11:00–22:30", img="img/food-kushikatsu.jpg",
         alt="Kushikatsu skewers at Daruma (Wikimedia Commons)", q="串かつ だるま 新世界総本店"),
    dict(tag="PORK BUNS", name="551 HORAI MAIN STORE", hrs="10:00–21:30", img="img/food-551.jpg",
         alt="The 551 Horai head store in Namba (Wikimedia Commons)", q="551蓬莱 本店 難波"),
    dict(tag="CHEESECAKE", name="RIKURO'S NAMBA", hrs="9:00–20:00", img="img/food-cheesecake.jpg",
         alt="A soufflé-style cheesecake (Wikimedia Commons)", q="りくろーおじさんの店 なんば本店"),
    dict(tag="RAMEN", name="KINRYU RAMEN DOTONBORI", hrs="24 HOURS", img="img/food-ramen.jpg",
         alt="A bowl of tonkotsu ramen at Kinryu Ramen, Dotonbori (Wikimedia Commons)", q="金龍ラーメン 道頓堀店"),
]

def pin_svg(s):
    x, y = proj(s["lat"], s["lng"])
    x += s.get("dx", 0); y += s.get("dy", 0)
    w, h, hd = 84, 56, 15
    return f'''<g class="pin" transform="translate({x-w/2:.0f},{y-h-12:.0f})">
<rect class="hd" x="0" y="0" width="{w}" height="{hd}"/><text x="{w/2}" y="12" font-size="11" text-anchor="middle">{s["n"]:02d}</text>
<image class="ph" href="{s["img"]}" x="2" y="{hd+2}" width="{w-4}" height="{h-hd-2}" preserveAspectRatio="xMidYMid slice"/>
<path class="tail" d="M{w/2-7},{h} L{w/2+7},{h} L{w/2},{h+12} Z"/></g>'''

def card(s):
    return f'''<article class="card"><div class="ph"><img src="{s["img"]}" alt="{s["alt"]}" loading="lazy">
<a class="gmap" href="{gmap_url(s["q"])}" target="_blank" rel="noopener" aria-label="Open {s["name"]} in Google Maps">{PIN}</a></div>
<div class="bd"><div class="no">{s["n"]:02d} · {s["genre"]}</div>
<div class="rowline"><h3>{s["name"]}</h3><span class="hrs">{CLOCK}{s["hrs"]}</span></div>
<p>{s["text"]}</p><p class="area">{s["area"]}</p></div></article>'''

def tile(f):
    return f'''<a class="tile" href="{gmap_url(f["q"])}" target="_blank" rel="noopener"><img src="{f["img"]}" alt="{f["alt"]}" loading="lazy">
<span class="tg">{f["tag"]}</span><span class="tm"><span class="tn">{f["name"]}</span><span class="tc">{f["hrs"]}</span></span></a>'''

map_pins = "\n".join(pin_svg(s) for s in SPOTS)
cards = "\n".join(card(s) for s in SPOTS)
tiles = "\n".join(tile(f) for f in FOODS)

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Osaka Shortlist for Shaun — Anime Sensei</title>
<meta name="description" content="Yuuki's Osaka picks for Shaun: Den Den Town anime and retro game shops, Dotonbori, Osaka Castle, Shinsekai, and the food to eat between them.">
<meta property="og:type" content="website">
<meta property="og:title" content="Osaka Shortlist for Shaun">
<meta property="og:description" content="Den Den Town first, then the classics: Dotonbori, Osaka Castle, Shinsekai — and takoyaki, okonomiyaki and kushikatsu in between.">
<meta property="og:url" content="{PAGE_URL}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23111426'/><text x='50' y='70' font-size='58' text-anchor='middle' fill='%23ffffff' font-family='Georgia'>O</text></svg>">
<style>{CSS}</style></head>
<body>
<header class="hero">
<div class="hero-grid">
<img src="img/hero-castle.jpg" alt="Osaka Castle keep seen across the moat (photo by Yuuki)">
<img src="img/hero-street.jpg" alt="Shinsaibashi-suji at the Dotonbori entrance, packed at night (photo by Yuuki)">
<img src="img/tsutenkaku.jpg" alt="Tsutenkaku tower lit up over a Shinsekai street at night (photo by Yuuki)">
</div>
<div class="hero-txt">
<div class="kicker">OSAKA · CITY GUIDE · BY YUUKI, ANIME SENSEI</div>
<h1>Osaka <span class="accent">Shortlist</span></h1>
<div class="sub">FOR SHAUN — DEN DEN TOWN FIRST, THEN THE CLASSICS</div>
</div></header>

<div class="wrap">
<div class="facts">
<div><b>FOR</b><span>Shaun — you asked what Osaka is worth seeing. This is my answer.</span></div>
<div><b>FOCUS</b><span>Den Den Town for anime, manga and retro games, plus the classic sights around it.</span></div>
<div><b>START</b><span>Den Den Town and Dotonbori sit side by side in Namba — you can walk between them.</span></div>
<div><b>EAT</b><span>Takoyaki, okonomiyaki and kushikatsu. Osaka runs on them.</span></div>
<div><b>TIP</b><span>Do the castle on a clear morning, and Den Den Town after 11:00 when the shops open.</span></div>
</div>

<h2>Six stops on one map</h2>
<p class="lede">Tap a pin or a card — everything opens in Google Maps.</p>
<div class="mapbox"><svg viewBox="0 0 600 460" role="img" aria-label="Map of the six stops in Osaka">
<rect width="600" height="460" fill="#101426"/>
<g stroke="#232c4d" stroke-width="1"><path d="M0,80 H600M0,170 H600M0,260 H600M0,350 H600M0,430 H600M90,0 V460M200,0 V460M310,0 V460M420,0 V460M520,0 V460"/></g>
<path d="M468,72 C380,120 260,180 150,300" stroke="#37e6ff" stroke-width="2.5" fill="none" stroke-dasharray="7 6" opacity="0.65"/>
<text x="18" y="34" fill="#8fa3d9" font-size="13" font-family="Verdana" letter-spacing="2">OSAKA</text>
<text x="592" y="440" fill="#5b6b99" font-size="10.5" font-family="Verdana" text-anchor="end">castle → east · namba → south-west</text>
{map_pins}
</svg></div>

<div class="cards">
{cards}
</div>
</div>

<section class="foodsec"><div class="wrap">
<h2>Eat like Osaka</h2>
<p class="lede">Six names to remember. Tap a tile to open it in Google Maps.</p>
<div class="tiles">
{tiles}
</div>
</div></section>

<div class="wrap">
<h2>Good to know</h2>
<ul class="notes">
<li>Den Den Town is Osaka's Akihabara — the same shop chains, often calmer than Tokyo.</li>
<li>Most Den Den Town shops open late morning. Arrive after 11:00 and nothing is shuttered.</li>
<li>Kushikatsu rule: one dip per skewer. Never double-dip in the shared sauce pot.</li>
<li>Osaka Castle keep is closed Dec 28 – Jan 1, and last entry is 17:30 — don't leave it to the end of the day.</li>
<li>Everything here is a short metro ride from Namba. The castle is the only longer hop.</li>
</ul>

<footer class="foot">
<p>Picked by Yuuki (Anime Sensei) for Shaun, November 2026. Opening hours checked against official shop and facility sites in November 2026 — they can change, so a quick check on the day is wise. No prices on this page: they move too fast to print.</p>
<p>Photo credits — Yuuki's own photos: hero (Osaka Castle, Shinsaibashi-suji, Tsutenkaku), Mandarake card (a Den Den Town side street), animate card (an anime shop in Den Den Town), Osaka Castle card, Tsutenkaku card, takoyaki and okonomiyaki tiles. Wikimedia Commons: Dotonbori card — Martin Falbisoner, CC BY-SA 4.0; Super Potato card — IQRemix, CC BY-SA 2.0 (the chain's Akihabara shop); kushikatsu tile — Aiko99ann, CC BY-SA 3.0; 551 Horai tile — Tokumeigakarinoaoshima, CC BY-SA 4.0; cheesecake tile — Ocdp, CC0; ramen tile — Guilhem Vellut, CC BY 2.0.</p>
</footer>
</div>
</body></html>'''

(HERE / "index.html").write_text(html)
credits = {
    "img/hero-castle.jpg": "Yuuki (Immich d920aaa0)",
    "img/hero-street.jpg": "Yuuki (Immich d8bacbdc)",
    "img/tsutenkaku.jpg": "Yuuki (Immich 0f91b9b0)",
    "img/mandarake.jpg": "Yuuki (Immich cc6b6c4d) — Den Den Town side street",
    "img/anime-shop.jpg": "Yuuki (Immich 57764c4f) — anime shop interior in Den Den Town",
    "img/castle.jpg": "Yuuki (Immich 2f0bb069)",
    "img/food-takoyaki.jpg": "Yuuki (Immich 4e2f7766) — takoyaki on the grill",
    "img/dotonbori.jpg": "Wikimedia Commons — Martin Falbisoner, CC BY-SA 4.0",
    "img/superpotato.jpg": "Wikimedia Commons — IQRemix, CC BY-SA 2.0 (Super Potato Akihabara shop)",
    "img/food-okonomiyaki.jpg": "Yuuki (Immich 3b9f2560) — okonomiyaki at a counter in Osaka",
    "img/food-kushikatsu.jpg": "Wikimedia Commons — Aiko99ann, CC BY-SA 3.0 (Kushikatsu Daruma)",
    "img/food-551.jpg": "Wikimedia Commons — Tokumeigakarinoaoshima, CC BY-SA 4.0 (551 Horai head store)",
    "img/food-cheesecake.jpg": "Wikimedia Commons — Ocdp, CC0 (soufflé-style cheesecake)",
    "img/food-ramen.jpg": "Wikimedia Commons — Guilhem Vellut, CC BY 2.0 (Kinryu Ramen, Dotonbori)",
}
(HERE / "credits.json").write_text(json.dumps(credits, indent=1, ensure_ascii=False))
print("index.html bytes:", len(html))
