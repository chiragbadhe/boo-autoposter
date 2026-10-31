#!/usr/bin/env python3
"""Render a Boo carousel from a post.json into 1080x1350 JPEGs.

Usage:  python3 studio/render.py path/to/post.json OUT_DIR
Writes OUT_DIR/01.jpg ... and OUT_DIR/caption.txt.
Exits 2 if any slide's content overflows (shorten the text and rerun).

post.json:
{
  "series": "ai" | "dsa" | "web" | "sysdesign" | "security" | "blockchain"
            | "data" | "cloud" | "careers",
  "palette": "aqua"   (optional; one of the PALETTES names below)
          or {"ground": "#hex", "shadow": "#hex", "highlight": "#hex"}
             (your own colours; shadow and highlight optional; the ground
              must keep the purple ink readable, else the render stops)
  "slides": [ ...slide objects, 3 to 8... ],
  "caption": "..."
}
In any title, wrap the key words in {braces} to highlight them in the
palette's highlight colour.
Palettes: sunny sky mint peach lilac pink lime aqua coral butter
(no palette given = the series default: ai sunny, web sky, data mint,
 cloud peach, security lilac, careers pink).

Slide types (all text fields are plain text):
  cover     tag, title, questions[2-4], bubble
  statement title, body, points[0-4] (optional), boo (bool, optional)
  steps     title, steps[{title,text}] (2-5), tip (optional)
  cards     title, cards[{icon,title,text}] (2-4)
  compare   title, left{label,items[2-4]}, right{label,items[2-4]}
  outro     title, text, cta
Every slide may set "mood" to change what Boo is doing (see studio/moods.py):
  curious idea thinking working celebrate study wow
  Defaults: cover curious, statement idea, outro celebrate.
  steps/cards/compare show a small Boo beside the title when "boo": true,
  in mood working, study or curious (default working).
Icons: chart palette bolt star lock cloud code database search globe cpu
       check link users key bug shield rocket book clock
"""
import html
from moods import MOODS, DEFAULT_BY_SLIDE, overlay
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HANDLE = "@chirag.zip"
INK, MUTED, OUTLINE = "#3B2468", "#5B4A8F", "#3B2468"
JACKET, JACKET_INK = "#F2A65A", "#B25E1C"
GROUND = {"ai": "#F9E38A", "web": "#BFE0FB", "data": "#BDEFC9",
          "cloud": "#FFD3B0", "security": "#DCD5FA", "careers": "#FBD0E6"}
SHADOW = {"ai": "#E2C26F", "web": "#9CC4E8", "data": "#93D3A5",
          "cloud": "#E8B48C", "security": "#B9AEE8", "careers": "#E5A9C6"}
# name: (ground, floor shadow, highlight, ground for the closing slide)
PALETTES = {
    "sunny":  ("#F9E38A", "#E2C26F", "#F2A65A", "sky"),
    "sky":    ("#BFE0FB", "#9CC4E8", "#F2A65A", "sunny"),
    "mint":   ("#BDEFC9", "#93D3A5", "#F2A65A", "lilac"),
    "peach":  ("#FFD3B0", "#E8B48C", "#5AA9F0", "aqua"),
    "lilac":  ("#DCD5FA", "#B9AEE8", "#F2A65A", "mint"),
    "pink":   ("#FBD0E6", "#E5A9C6", "#5AA9F0", "butter"),
    "lime":   ("#DDF2A8", "#BCD782", "#F2A65A", "pink"),
    "aqua":   ("#B8EEEA", "#8ED3CD", "#F2A65A", "peach"),
    "coral":  ("#FFC9BD", "#E8A595", "#5AA9F0", "sky"),
    "butter": ("#FFF1C2", "#E8D493", "#5AA9F0", "lilac"),
}
SERIES_PALETTE = {"ai": "sunny", "web": "sky", "data": "mint", "cloud": "peach",
                  "security": "lilac", "careers": "pink", "dsa": "lime",
                  "sysdesign": "aqua", "blockchain": "coral"}
for _s, _p in SERIES_PALETTE.items():          # every series gets a default ground
    GROUND.setdefault(_s, PALETTES[_p][0])
    SHADOW.setdefault(_s, PALETTES[_p][1])
ACCENTS = ["#F2A65A", "#5AA9F0", "#A6E8A0", "#DCD5FA", "#F9E38A", "#FFD3B0"]
SERIES_LABEL = {"ai": "AI · explained by Boo", "web": "Web · explained by Boo",
                "data": "Data · explained by Boo", "cloud": "Cloud · explained by Boo",
                "security": "Security · explained by Boo", "careers": "Careers · tips from Boo",
                "dsa": "DSA · explained by Boo", "sysdesign": "System design · by Boo",
                "blockchain": "Blockchain · explained by Boo"}

ICONS = {
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-1 2-2 0-1.5-1.5-1.7-1.5-3s1-2 2.5-2H18a3 3 0 0 0 3-3c0-4.4-4-8-9-8z"/><circle cx="7.5" cy="11" r="1"/><circle cx="11" cy="7.5" r="1"/><circle cx="16" cy="8.5" r="1"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "cloud": '<path d="M7 18a5 5 0 0 1-.6-10A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9z"/>',
    "code": '<path d="M8 8l-5 4 5 4M16 8l5 4-5 4M14 4l-4 16"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.7-3.5 3.3-5.5 6.5-5.5s5.8 2 6.5 5.5M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5c2 .6 3.2 2.5 3.5 5.5"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
    "bug": '<rect x="7" y="8" width="10" height="12" rx="5"/><path d="M12 8v12M9 5l1.5 3M15 5l-1.5 3M3 13h4M17 13h4M4 19l3-2M20 19l-3-2M4 7l3 2M20 7l-3 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
    "rocket": '<path d="M12 15l-3-3c1-5 4-9 10-9 0 6-4 9-9 10zM9 12l-4 1-2 4 4-1M12 15l-1 4-4 2 1-4"/><circle cx="15" cy="9" r="1.5"/>',
    "book": '<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4zM20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}


def esc(s):
    return html.escape(str(s or ""), quote=True)


def hl(title):
    out = esc(title)
    return re.sub(r"\{([^{}]+)\}", r'<span class="hl">\1</span>', out)


def icon(name, size=52):
    path = ICONS.get(name, ICONS["star"])
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{path}</svg>')


CSS = """
@font-face{font-family:Fredoka;src:url('assets/Fredoka.ttf');font-weight:300 700}
*{box-sizing:border-box}
body{margin:0;width:1080px;height:1350px;overflow:hidden}
.s{width:1080px;height:1350px;padding:72px;display:flex;flex-direction:column;gap:36px;font-family:Fredoka,sans-serif;color:%(ink)s;position:relative;overflow:hidden}
.top{display:flex;justify-content:space-between;align-items:center;min-height:56px}
.pill{font-size:26px;font-weight:600;background:#fff;border:4px solid %(ol)s;border-radius:999px;padding:8px 24px}
h1{margin:0;font-size:108px;font-weight:700;line-height:1.02}
h2{margin:0;font-size:80px;font-weight:700;line-height:1.05}
.hl{color:var(--hl);-webkit-text-stroke:4px %(ol)s;paint-order:stroke fill}
h1 .hl{-webkit-text-stroke:5px %(ol)s}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px;min-height:0}
.card{background:#fff;border:5px solid %(ol)s;border-radius:36px;padding:26px 32px;box-shadow:0 10px 0 var(--sh)}
.q{font-size:36px;font-weight:500;line-height:1.25}
.q b{color:%(jki)s}
.body{font-size:38px;line-height:1.35;font-weight:500;margin:0}
.muted{color:%(mu)s}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:500;color:%(mu)s;min-height:36px}
.foot b{color:%(ink)s;font-weight:600}
.step{display:flex;gap:26px;align-items:center}
.num{width:88px;height:88px;flex-shrink:0;border-radius:50%%;border:5px solid %(ol)s;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:700}
.st{font-size:38px;font-weight:600;margin:0}
.sx{font-size:29px;line-height:1.3;margin:4px 0 0;color:%(mu)s}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.ic{width:92px;height:92px;border-radius:50%%;border:5px solid %(ol)s;display:flex;align-items:center;justify-content:center}
.tip{font-size:31px;font-weight:600;text-align:center;background:#F9E38A;border:5px solid %(ol)s;border-radius:999px;padding:14px 28px}
.boo{position:absolute}
.shadow{position:absolute;border-radius:50%%}
.bubble{font-size:34px;font-weight:600;text-align:center;background:#fff;border:5px solid %(ol)s;border-radius:36px;padding:14px 22px;box-shadow:0 10px 0 var(--sh)}
ul.pts{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:16px}
ul.pts li{font-size:34px;line-height:1.3;font-weight:500;display:flex;gap:16px;align-items:flex-start}
.dot{width:22px;height:22px;flex-shrink:0;border-radius:50%%;background:%(jk)s;border:4px solid %(ol)s;margin-top:10px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}
.lab{font-size:34px;font-weight:700;margin:0 0 14px;padding:8px 20px;border:4px solid %(ol)s;border-radius:999px;display:inline-block}
""" % {"ink": INK, "ol": OUTLINE, "jk": JACKET, "jki": JACKET_INK, "mu": MUTED}


def frame(inner, n, total, series, extra_top=""):
    swipe = "<b>Swipe →</b>" if n < total else "<b>Save this ✦</b>"
    return f"""<div class="s" style="background:{GROUND[series]};--sh:{SHADOW[series]};--hl:{HIGHLIGHT.get(series, JACKET)}">
<div class="top">{extra_top or '<span></span>'}<span class="pill">{n}/{total}</span></div>
{inner}
<div class="foot"><span>{HANDLE}</span>{swipe}</div></div>"""


def boo_img(left, top, w, series, mood=None):
    h = int(w * 1033 / 864)
    sw = int(w * 0.75)
    sh = max(14, int(30 * w / 370))
    return (f'<div class="shadow" style="left:{left + (w - sw)//2}px;top:{top + h + 4}px;width:{sw}px;height:{sh}px;background:{SHADOW[series]}"></div>'
            + overlay("back", mood, left, top, w)
            + f'<img class="boo" src="assets/boo.png" alt="Boo" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">'
            + overlay("front", mood, left, top, w))


MINI_MOODS = ("working", "study", "curious")


def mood_of(sl):
    m = sl.get("mood") or DEFAULT_BY_SLIDE.get(sl.get("type"))
    if m not in MOODS:
        sys.exit(f"Unknown mood {m!r}; use one of {', '.join(MOODS)}")
    return m


def mini_boo(sl, series):
    """Small Boo beside the title on steps/cards/compare slides when "boo": true."""
    if not sl.get("boo"):
        return "", ""
    m = mood_of(sl)
    if m not in MINI_MOODS:
        m = "working"
    return boo_img(890, 172, 118, series, m), ' style="padding-right:180px;min-height:170px"'



def slide_html(sl, n, total, series):
    t = sl.get("type")
    if t == "cover":
        qs = "".join(f'<div class="card q"><b>?</b> {esc(q)}</div>' for q in sl.get("questions", [])[:4])
        inner = f"""<h1>{hl(sl.get('title'))}</h1>
<div class="main" style="width:560px;justify-content:flex-start">{qs}</div>
<div class="bubble" style="position:absolute;left:676px;top:530px;width:330px">{esc(sl.get('bubble') or 'Let’s find out!')}</div>
{boo_img(650, 740, 350, series, mood_of(sl))}"""
        tag = f'<span class="pill" style="background:#fff">{esc(sl.get("tag") or SERIES_LABEL[series])}</span>'
        return frame(inner, n, total, series, tag)
    if t == "statement":
        pts = sl.get("points") or []
        plist = "".join(f'<li><span class="dot"></span><span>{esc(p)}</span></li>' for p in pts[:4])
        booblk = boo_img(800, 930, 200, series, mood_of(sl)) if sl.get("boo") else ""
        inner = f"""<h2>{hl(sl.get('title'))}</h2>
<div class="main"><div class="card"><p class="body">{esc(sl.get('body'))}</p></div>
{f'<ul class="pts" style="padding-right:{250 if sl.get("boo") else 0}px">{plist}</ul>' if plist else ''}</div>{booblk}"""
        return frame(inner, n, total, series)
    if t == "steps":
        steps = sl.get("steps", [])[:5]
        rows = "".join(
            f'<div class="card step"><div class="num" style="background:{ACCENTS[i % len(ACCENTS)]}">{i+1}</div>'
            f'<div><p class="st">{esc(s.get("title"))}</p><p class="sx">{esc(s.get("text"))}</p></div></div>'
            for i, s in enumerate(steps))
        tip = f'<div class="tip">{esc(sl["tip"])}</div>' if sl.get("tip") else ""
        mb, h2s = mini_boo(sl, series)
        inner = f'<h2{h2s}>{hl(sl.get("title"))}</h2><div class="main">{rows}{tip}</div>{mb}'
        return frame(inner, n, total, series)
    if t == "cards":
        cards = sl.get("cards", [])[:4]
        cells = "".join(
            f'<div class="card" style="display:flex;flex-direction:column;gap:14px;padding:32px">'
            f'<div class="ic" style="background:{ACCENTS[i % len(ACCENTS)]}">{icon(c.get("icon"))}</div>'
            f'<p class="st" style="font-size:36px;line-height:1.15">{esc(c.get("title"))}</p>'
            f'<p class="sx" style="margin:0">{esc(c.get("text"))}</p></div>'
            for i, c in enumerate(cards))
        mb, h2s = mini_boo(sl, series)
        inner = f'<h2{h2s}>{hl(sl.get("title"))}</h2><div class="main"><div class="grid">{cells}</div></div>{mb}'
        return frame(inner, n, total, series)
    if t == "compare":
        def col(side, bg):
            items = "".join(f'<li><span class="dot" style="background:{bg}"></span><span>{esc(x)}</span></li>' for x in side.get("items", [])[:4])
            return f'<div class="card"><p class="lab" style="background:{bg}">{esc(side.get("label"))}</p><ul class="pts">{items}</ul></div>'
        mb, h2s = mini_boo(sl, series)
        inner = (f'<h2{h2s}>{hl(sl.get("title"))}</h2><div class="main"><div class="cmp">'
                 f'{col(sl.get("left", {}), "#5AA9F0")}{col(sl.get("right", {}), JACKET)}</div></div>{mb}')
        return frame(inner, n, total, series)
    if t == "outro":
        series = "_alt"
        inner = f"""<div class="main" style="align-items:center;text-align:center;justify-content:flex-start;gap:28px">
<h2 style="font-size:92px">{hl(sl.get('title'))}</h2>
<p class="body muted" style="max-width:860px">{esc(sl.get('text'))}</p></div>
{boo_img(330, 560, 420, series, mood_of(sl))}
<div class="bubble" style="position:absolute;left:160px;top:1150px;width:760px;font-size:36px">{esc(sl.get('cta') or 'Follow ' + HANDLE + ' for more')}</div>"""
        return frame(inner, n, total, series)
    raise ValueError(f"Unknown slide type: {t}")


HIGHLIGHT = {}
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def luminance(hexcol):
    c = [int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def darken(hexcol, f=0.86):
    return "#" + "".join(f"{int(int(hexcol[i:i + 2], 16) * f):02X}" for i in (1, 3, 5))


def resolve_palette(pal, series):
    """Set this post's colours: GROUND/SHADOW/HIGHLIGHT for `series` and `_alt`."""
    if isinstance(pal, str):
        if pal not in PALETTES:
            sys.exit(f"Unknown palette {pal!r}; use one of {', '.join(PALETTES)} or a colour object")
        ground, shadow, hl, alt = PALETTES[pal]
        ag, ash, ahl, _ = PALETTES[alt]
    elif isinstance(pal, dict):
        ground = pal.get("ground", "")
        if not HEX.match(ground):
            sys.exit("palette.ground must be a #RRGGBB colour")
        shadow = pal.get("shadow") or darken(ground)
        hl = pal.get("highlight") or JACKET
        for k, v in (("shadow", shadow), ("highlight", hl)):
            if not HEX.match(v):
                sys.exit(f"palette.{k} must be a #RRGGBB colour")
        # closing slide: sunny, unless the custom ground is already close to it
        ag, ash, ahl, _ = PALETTES["sky" if contrast(ground, PALETTES["sunny"][0]) < 1.1 else "sunny"]
    else:
        sys.exit("palette must be a name or an object")
    if contrast(ground, INK) < 7 or contrast(ground, MUTED) < 4.5:
        sys.exit(f"palette ground {ground} is too dark for Boo's purple text; pick a lighter colour")
    GROUND[series], SHADOW[series], HIGHLIGHT[series] = ground, shadow, hl
    GROUND["_alt"], SHADOW["_alt"], HIGHLIGHT["_alt"] = ag, ash, ahl


def chrome_path():
    for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if os.path.exists(p):
            return p
    return None


OVERFLOW_JS = """() => {
  const s = document.querySelector('.s'); const bad = [];
  for (const el of s.querySelectorAll('.main, .card, .foot')) {
    if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) bad.push(el.className || el.tagName);
  }
  for (const el of s.querySelectorAll('h1, h2')) {
    if (el.scrollWidth > el.clientWidth + 2) bad.push(el.tagName + ' too wide');
    if (el.getBoundingClientRect().height > 3.4 * parseFloat(getComputedStyle(el).fontSize)) bad.push(el.tagName + ' more than 3 lines');
  }
  const m = s.querySelector('.main'); const f = s.querySelector('.foot');
  if (m && f && m.getBoundingClientRect().bottom > f.getBoundingClientRect().top + 1) bad.push('main overlaps footer');
  return bad;
}"""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec_path, out_dir = sys.argv[1], sys.argv[2]
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    series = spec.get("series", "ai")
    if series not in SERIES_PALETTE:
        sys.exit(f"Unknown series {series!r}; use one of {', '.join(SERIES_PALETTE)}")
    resolve_palette(spec.get("palette") or SERIES_PALETTE[series], series)
    slides = spec.get("slides", [])
    if not 3 <= len(slides) <= 8:
        sys.exit("A post needs 3 to 8 slides.")
    os.makedirs(out_dir, exist_ok=True)

    from playwright.sync_api import sync_playwright
    problems = []
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if chrome_path():
            kw["executable_path"] = chrome_path()
        browser = p.chromium.launch(**kw)
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        for i, sl in enumerate(slides, 1):
            doc = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
                   f"<body>{slide_html(sl, i, len(slides), series)}</body></html>")
            tmp = os.path.join(HERE, f"_slide{i}.html")
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(doc)
            page.goto("file://" + tmp)
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(250)
            bad = page.evaluate(OVERFLOW_JS)
            if bad:
                problems.append(f"slide {i} ({sl.get('type')}): overflow in {', '.join(bad)}")
            page.screenshot(path=os.path.join(out_dir, f"{i:02d}.jpg"), type="jpeg", quality=92)
            os.remove(tmp)
        browser.close()
    with open(os.path.join(out_dir, "caption.txt"), "w", encoding="utf-8") as fh:
        fh.write(spec.get("caption", "").strip() + "\n")
    if problems:
        print("OVERFLOW — shorten text and rerun:\n  " + "\n  ".join(problems))
        sys.exit(2)
    print(f"Rendered {len(slides)} slides to {out_dir}")


if __name__ == "__main__":
    main()
