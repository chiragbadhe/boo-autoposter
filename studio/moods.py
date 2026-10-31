"""Boo moods: props drawn around Boo's artwork in his outline style.

Each mood is SVG content in Boo's own coordinate space (the art is 864 x 1033),
drawn on an overlay that extends 260 units beyond the art on every side, so
props can sit above or beside him. Layers: "back" draws behind Boo, "front"
over him.
"""

OL = "#3B2468"          # outline
W = 14                  # outline width in art units

def _star(cx, cy, r, fill="#F2A65A"):
    pts = []
    import math
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.0f},{cy - rr * math.sin(a):.0f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{OL}" stroke-width="{W*0.7}" stroke-linejoin="round"/>'

def _q(x, y, s=1.0, fill="#F2A65A"):
    return (f'<text x="{x}" y="{y}" font-family="Fredoka, sans-serif" font-weight="700" font-size="{int(260*s)}" '
            f'fill="{fill}" stroke="{OL}" stroke-width="{W*0.8}" paint-order="stroke fill" text-anchor="middle">?</text>')

def _bang(x, y, s=1.0, fill="#F2A65A"):
    return (f'<text x="{x}" y="{y}" font-family="Fredoka, sans-serif" font-weight="700" font-size="{int(280*s)}" '
            f'fill="{fill}" stroke="{OL}" stroke-width="{W*0.8}" paint-order="stroke fill" text-anchor="middle">!</text>')

MOODS = {
    # holding a magnifier up in the waving hand, question marks floating
    "curious": {
        "back": "",
        "front": (
            f'<path d="M842 560 L900 690" stroke="{OL}" stroke-width="{W*3.2}" stroke-linecap="round"/>'
            f'<path d="M842 560 L900 690" stroke="#7E6BD6" stroke-width="{W*1.6}" stroke-linecap="round"/>'
            f'<circle cx="800" cy="440" r="128" fill="#D6ECFF" fill-opacity="0.55" stroke="{OL}" stroke-width="{W*2.6}"/>'
            f'<circle cx="800" cy="440" r="128" fill="none" stroke="#5AA9F0" stroke-width="{W*1.2}"/>'
            f'<path d="M730 390 Q750 345 800 335" fill="none" stroke="#fff" stroke-width="{W*1.2}" stroke-linecap="round"/>'
            + _q(700, -40, 1.0) + _q(910, 80, 0.7, "#5AA9F0")
        ),
    },
    # lightbulb moment above his head
    "idea": {
        "back": "",
        "front": (
            '<g stroke-linecap="round">'
            f'<path d="M640 -120 L600 -170 M760 -150 L760 -215 M880 -120 L920 -170 M560 -20 L500 -40 M960 -20 L1020 -40" stroke="{OL}" stroke-width="{W*1.1}"/>'
            '</g>'
            f'<path d="M700 70 L700 30 Q620 0 620 -70 A140 140 0 1 1 900 -70 Q900 0 820 30 L820 70 Z" fill="#FCD87A" stroke="{OL}" stroke-width="{W}" stroke-linejoin="round"/>'
            f'<rect x="700" y="70" width="120" height="60" rx="18" fill="#B9AEE8" stroke="{OL}" stroke-width="{W}"/>'
            f'<path d="M705 100 H815" stroke="{OL}" stroke-width="{W*0.6}"/>'
            f'<path d="M700 -90 Q705 -150 760 -160" fill="none" stroke="#fff" stroke-width="{W*1.2}" stroke-linecap="round"/>'
        ),
    },
    # thought bubble with dots
    "thinking": {
        "back": "",
        "front": (
            f'<circle cx="720" cy="130" r="26" fill="#fff" stroke="{OL}" stroke-width="{W*0.8}"/>'
            f'<circle cx="790" cy="40" r="40" fill="#fff" stroke="{OL}" stroke-width="{W*0.9}"/>'
            f'<path d="M760 -60 Q720 -150 810 -175 Q850 -250 950 -215 Q1050 -250 1080 -160 Q1150 -110 1080 -40 Q1060 20 960 0 Q880 40 830 -10 Q740 0 760 -60 Z" fill="#fff" stroke="{OL}" stroke-width="{W}" stroke-linejoin="round"/>'
            f'<circle cx="860" cy="-100" r="20" fill="{OL}"/><circle cx="940" cy="-100" r="20" fill="{OL}"/><circle cx="1020" cy="-100" r="20" fill="{OL}"/>'
        ),
    },
    # typing on a laptop, code tag floating
    "working": {
        "back": "",
        "front": (
            f'<rect x="150" y="560" width="560" height="340" rx="28" fill="#DCD5FA" stroke="{OL}" stroke-width="{W}" stroke-linejoin="round"/>'
            f'<rect x="170" y="840" width="520" height="40" rx="10" fill="#B9AEE8"/>'
            f'<circle cx="430" cy="720" r="44" fill="#fff" stroke="{OL}" stroke-width="{W*0.7}"/>'
            f'<path d="M60 900 H800 L760 960 H100 Z" fill="#9C92C9" stroke="{OL}" stroke-width="{W}" stroke-linejoin="round"/>'
            f'<rect x="880" y="170" width="250" height="150" rx="40" fill="#fff" stroke="{OL}" stroke-width="{W}"/>'
            f'<path d="M960 210 L920 245 L960 280 M1050 210 L1090 245 L1050 280 M1025 200 L985 290" fill="none" stroke="#5AA9F0" stroke-width="{W*1.1}" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
    },
    # party: stars and confetti
    "celebrate": {
        "back": "",
        "front": (
            _star(-60, 120, 95) + _star(980, 60, 85, "#5AA9F0") + _star(1030, 640, 70, "#A6E8A0")
            + _star(-90, 640, 65, "#F6B6D8")
            + f'<rect x="80" y="-120" width="70" height="34" rx="12" fill="#5AA9F0" stroke="{OL}" stroke-width="{W*0.6}" transform="rotate(-25 100 -110)"/>'
            + f'<rect x="420" y="-170" width="70" height="34" rx="12" fill="#F2A65A" stroke="{OL}" stroke-width="{W*0.6}" transform="rotate(20 440 -160)"/>'
            + f'<rect x="760" y="-120" width="70" height="34" rx="12" fill="#A6E8A0" stroke="{OL}" stroke-width="{W*0.6}" transform="rotate(40 780 -110)"/>'
            + f'<circle cx="260" cy="-60" r="24" fill="#F6B6D8" stroke="{OL}" stroke-width="{W*0.6}"/>'
            + f'<circle cx="1080" cy="340" r="24" fill="#F2A65A" stroke="{OL}" stroke-width="{W*0.6}"/>'
            + f'<circle cx="-120" cy="380" r="24" fill="#5AA9F0" stroke="{OL}" stroke-width="{W*0.6}"/>'
        ),
    },
    # graduation cap: learning / study topics
    "study": {
        "back": "",
        "front": (
            f'<path d="M260 150 L260 70 Q430 30 600 70 L600 150 Q430 120 260 150 Z" fill="#3B2468" stroke="{OL}" stroke-width="{W}" stroke-linejoin="round"/>'
            f'<path d="M430 -60 L760 40 L430 140 L100 40 Z" fill="#4A3880" stroke="{OL}" stroke-width="{W}" stroke-linejoin="round"/>'
            f'<circle cx="430" cy="40" r="18" fill="#F2A65A" stroke="{OL}" stroke-width="{W*0.6}"/>'
            f'<path d="M430 40 L690 70 L690 210" fill="none" stroke="#F2A65A" stroke-width="{W*0.9}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect x="666" y="200" width="48" height="70" rx="14" fill="#F2A65A" stroke="{OL}" stroke-width="{W*0.6}"/>'
            f'<rect x="880" y="380" width="200" height="150" rx="16" fill="#fff" stroke="{OL}" stroke-width="{W}" transform="rotate(12 980 455)"/>'
            f'<path d="M920 430 H1040 M915 470 H1020 M910 505 H1030" stroke="#9C92C9" stroke-width="{W*0.8}" stroke-linecap="round" transform="rotate(12 980 455)"/>'
        ),
    },
    # surprised: exclamation marks and motion lines
    "wow": {
        "back": "",
        "front": (
            _bang(960, 160, 1.1) + _bang(1080, 260, 0.75, "#5AA9F0")
            + f'<path d="M-40 260 L-130 220 M-50 360 L-150 360 M-40 460 L-130 500" stroke="{OL}" stroke-width="{W*1.1}" stroke-linecap="round"/>'
        ),
    },
}

DEFAULT_BY_SLIDE = {"cover": "curious", "statement": "idea", "steps": "working",
                    "cards": "thinking", "compare": "thinking", "outro": "celebrate"}

PAD = 260

def overlay(layer, mood, left, top, w):
    """Absolutely positioned SVG for one layer of a mood, aligned to Boo's box."""
    m = MOODS.get(mood)
    if not m or not m.get(layer):
        return ""
    s = w / 864
    ow, oh = (864 + 2 * PAD) * s, (1033 + 2 * PAD) * s
    return (f'<svg aria-hidden="true" class="boo" style="left:{left - PAD * s:.0f}px;top:{top - PAD * s:.0f}px;'
            f'width:{ow:.0f}px;height:{oh:.0f}px;overflow:visible" viewBox="{-PAD} {-PAD} {864 + 2 * PAD} {1033 + 2 * PAD}">'
            f'{m[layer]}</svg>')
