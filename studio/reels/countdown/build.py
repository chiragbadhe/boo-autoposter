"""Countdown-list reel in Boo's style: card carousel on top, Boo + word-by-word captions below."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, HERE)
from moods import overlay  # noqa: E402
from script import LINES, ITEMS, MOODS, TITLE  # noqa: E402

meta = json.load(open(os.path.join(HERE, "timing.json")))
GAP, T0 = 0.22, 0.35
T = []
t = T0
for m in meta:
    T.append(round(t, 3))
    t += m["dur"] + GAP
TE = round(T[-1] + meta[-1]["dur"] + 0.2, 3)
DUR = round(TE + 4.6, 2)

INK, MUTED, OL = "#3B2468", "#5B4A8F", "#3B2468"
BG, SH, GRID = "#DDF2A8", "#BCD782", "rgba(59,36,104,0.07)"
JK, BL, GR, CO, LI, YE = "#F2A65A", "#5AA9F0", "#A6E8A0", "#FF9E8A", "#DCD5FA", "#F9E38A"


def clean(w):
    return w.rstrip(".,")


# ---------- caption chunks with absolute word times ----------
chunks = []
for li, line in enumerate(LINES):
    k = 0
    for ch in line:
        words = []
        for (txt, _ph, big) in ch:
            words.append({"t": round(T[li] + meta[li]["starts"][k], 3), "txt": clean(txt), "big": big})
            k += 1
        chunks.append({"words": words})
# end chunks (no voice): shown during the jingle
chunks.append({"words": [{"t": TE + 0.35, "txt": "Save", "big": 0}, {"t": TE + 0.55, "txt": "this!", "big": 1}]})
chunks.append({"words": [{"t": TE + 2.0, "txt": "follow", "big": 0}, {"t": TE + 2.2, "txt": "@chirag.zip", "big": 1}]})
for i, c in enumerate(chunks):
    c["start"] = c["words"][0]["t"]
    c["end"] = chunks[i + 1]["words"][0]["t"] if i + 1 < len(chunks) else DUR
WORD_TIMES = sorted(w["t"] for c in chunks[:-2] for w in c["words"])

# ---------- icons (white strokes on dark tiles) ----------
ICON = {
    "array": '<path d="M2 8.5h6v7H2zM9 8.5h6v7H9zM16 8.5h6v7h-6z"/>',
    "stack": '<rect x="4" y="5" width="16" height="3.4" rx="1.6"/><rect x="4" y="10.3" width="16" height="3.4" rx="1.6"/><rect x="4" y="15.6" width="16" height="3.4" rx="1.6"/>',
    "queue": '<circle cx="5" cy="10" r="2.4"/><circle cx="12" cy="10" r="2.4"/><circle cx="19" cy="10" r="2.4"/><path d="M21 17H3m3-2.5L3.5 17 6 19.5"/>',
    "hash": '<circle cx="6.5" cy="12" r="3.3"/><path d="M9.8 12h4.5m-2-2 2 2-2 2"/><rect x="15.5" y="8" width="6" height="8" rx="1.5"/>',
    "tree": '<circle cx="12" cy="4.5" r="2.3"/><circle cx="6" cy="12" r="2.3"/><circle cx="18" cy="12" r="2.3"/><circle cx="3.5" cy="19.5" r="2"/><circle cx="9" cy="19.5" r="2"/><path d="M10.5 6.3 7.3 10.2M13.5 6.3l3.2 3.9M5.1 14.1 4 17.6M7 14.1l1.3 3.5"/>',
    "graph": '<circle cx="5" cy="6" r="2.2"/><circle cx="18.5" cy="5" r="2.2"/><circle cx="12" cy="13" r="2.2"/><circle cx="5.5" cy="19" r="2.2"/><circle cx="19" cy="18.5" r="2.2"/><path d="M7 7.2l3.3 4.3M16.8 6.6l-3.3 4.6M10.3 14.4 7.1 17.6M13.8 14.2l3.5 3.2M7.2 6l9.1-.8"/>',
}


def icon(name, size, stroke="#fff", sw=2.1):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


# ---------- card illustrations (520 x 250) ----------
def t_(x, y, s, size=40, fill=INK, w=700, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="Fredoka" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="central">{s}</text>'


def illo(kind):
    o = f'stroke="{OL}" stroke-width="6" stroke-linejoin="round"'
    if kind == "array":
        g = ""
        for i, v in enumerate([7, 3, 9, 4, 1]):
            x = 22 + i * 96
            g += f'<rect x="{x}" y="60" width="86" height="86" rx="12" fill="{JK if i == 3 else "#fff"}" {o}/>' + t_(x + 43, 103, v, 46)
            g += t_(x + 43, 178, i, 28, MUTED, 600)
        return g + t_(260, 222, "array[3] → instant", 26, MUTED, 600)
    if kind == "stack":
        g = ""
        cols = [GR, BL, JK, LI]
        for i in range(4):
            y = 196 - i * 44
            g += f'<rect x="150" y="{y}" width="220" height="36" rx="18" fill="{cols[i]}" {o}/>'
        g += f'<path d="M110 30 V96 M92 78 L110 98 L128 78" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' + t_(70, 40, "push", 28, MUTED, 600)
        g += f'<path d="M410 98 V32 M392 50 L410 30 L428 50" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' + t_(460, 40, "pop", 28, MUTED, 600)
        return g
    if kind == "queue":
        g = ""
        cols = [GR, BL, JK, LI]
        for i in range(4):
            x = 150 + i * 80
            g += f'<circle cx="{x}" cy="100" r="30" fill="{cols[i]}" {o}/><rect x="{x-34}" y="138" width="68" height="40" rx="18" fill="{cols[i]}" {o}/>'
        g += f'<path d="M80 120 H24 M42 102 L22 120 L42 138" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' + t_(52, 74, "out", 28, MUTED, 600)
        g += f'<path d="M500 120 H444 M462 102 L442 120 L462 138" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' + t_(472, 74, "in", 28, MUTED, 600)
        return g + t_(260, 226, "first in, first out", 26, MUTED, 600)
    if kind == "hash":
        g = ""
        for i, (k, v) in enumerate([("name", "Boo"), ("job", "AI agent")]):
            y = 50 + i * 100
            g += f'<rect x="20" y="{y}" width="170" height="70" rx="35" fill="{YE}" {o}/>' + t_(105, y + 35, k, 34)
            g += f'<path d="M206 {y+35} H286 M266 {y+17} L288 {y+35} L266 {y+53}" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            g += f'<rect x="304" y="{y}" width="196" height="70" rx="14" fill="#fff" {o}/>' + t_(402, y + 35, v, 32)
        return g
    if kind == "tree":
        nodes = [(260, 44, JK), (150, 128, BL), (370, 128, BL), (90, 210, GR), (210, 210, GR), (320, 210, GR), (430, 210, GR)]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        g = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{OL}" stroke-width="6"/>' for a, b in edges)
        g += "".join(f'<circle cx="{x}" cy="{y}" r="{30 if i == 0 else 26}" fill="{c}" {o}/>' for i, (x, y, c) in enumerate(nodes))
        return g + t_(260, 44, "root", 18, INK, 700)
    if kind == "graph":
        nodes = [(70, 70, JK), (230, 36, BL), (420, 70, GR), (150, 190, LI), (330, 160, YE), (470, 210, BL)]
        edges = [(0, 1), (1, 2), (0, 3), (1, 4), (3, 4), (2, 4), (4, 5), (2, 5)]
        g = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{OL}" stroke-width="6" stroke-linecap="round"/>' for a, b in edges)
        return g + "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{c}" {o}/>' for (x, y, c) in nodes)
    return ""


# ---------- cards ----------
CARD_W, CARD_H, CARD_L, CARD_T = 620, 680, 230, 300
cards = ""
for i, (name, _num, desc, _tag, ic) in enumerate(ITEMS):
    cards += f'''<div id="card{i}" class="card" style="left:{CARD_L}px;top:{CARD_T}px;width:{CARD_W}px;height:{CARD_H}px">
  <div class="crow"><div class="tile">{icon(ic, 64)}</div><span class="cnum">{i+1:02d}</span></div>
  <svg class="illo" width="520" height="250" viewBox="0 0 520 250" aria-hidden="true">{illo(ic)}</svg>
  <div class="ctitle">{name}</div>
  <div class="cdesc">{desc}</div>
  <div class="cfoot"><span class="fdot"></span>DSA · @chirag.zip</div>
</div>'''

tiles = ""
for i, (_n, _num, _d, _tag, ic) in enumerate(ITEMS):
    x, y = 300 + (i % 3) * 240 - 80, 400 + (i // 3) * 240
    inner = icon(ic, 92) if i < 5 else '<span class="qm">?</span>'
    tiles += f'<div id="tile{i}" class="htile" style="left:{x}px;top:{y}px">{inner}</div>'
tiles += f'<div id="lastTag" class="lasttag" style="left:{300 + 2*240 - 80 + 70}px;top:{400 + 240 - 40}px">LAST</div>'

summary = '<div id="summary" class="summary"><div class="stitle">6 data structures <span class="hl">to know</span></div><div class="sgrid">'
for i, (name, _num, _d, tag, ic) in enumerate(ITEMS):
    summary += f'<div id="srow{i}" class="srow"><div class="stile">{icon(ic, 62)}</div><div><div class="sname">{name}</div><div class="stag">{tag}</div></div></div>'
summary += "</div></div>"

dots = '<div id="dots" class="dots">' + "".join(f'<span id="dot{i}" class="dot"></span>' for i in range(6)) + "</div>"

# ---------- Boo with one prop layer per mood ----------
BOO_L, BOO_T, BOO_W = 50, 1200, 400
BOO_H = int(BOO_W * 1033 / 864)
ALL_MOODS = MOODS + ["celebrate"]
backs = "".join(f'<div id="mb{k}" class="mlay">{overlay("back", m, BOO_L, BOO_T, BOO_W)}</div>' for k, m in enumerate(ALL_MOODS))
fronts = "".join(f'<div id="mf{k}" class="mlay">{overlay("front", m, BOO_L, BOO_T, BOO_W)}</div>' for k, m in enumerate(ALL_MOODS))
boo = (f'<div id="booSh" class="booSh" style="left:{BOO_L + 60}px;top:{BOO_T + BOO_H + 6}px;width:{BOO_W - 120}px"></div>'
       f'<div id="booWrap" class="layer" style="transform-origin:{BOO_L + BOO_W/2}px {BOO_T + BOO_H}px">{backs}'
       f'<img class="boo" src="boo.png" alt="" style="left:{BOO_L}px;top:{BOO_T}px;width:{BOO_W}px;height:{BOO_H}px">{fronts}</div>')

CSS = f"""
@font-face{{font-family:Fredoka;src:url('Fredoka.ttf');font-weight:300 700}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:Fredoka,sans-serif;color:{INK};
  background-color:{BG};background-image:linear-gradient({GRID} 2px,transparent 2px),linear-gradient(90deg,{GRID} 2px,transparent 2px);background-size:54px 54px}}
.layer{{position:absolute;left:0;top:0;width:1080px;height:1920px}} .boo{{position:absolute}} .mlay{{position:absolute;left:0;top:0}}
.head{{position:absolute;left:64px;top:62px;display:flex;gap:20px;align-items:stretch}}
.bar{{width:12px;border-radius:6px;background:{JK};border:3px solid {OL}}}
.htitle{{font-size:48px;font-weight:700;line-height:1.05}} .hhandle{{font-size:27px;font-weight:600;color:{MUTED};margin-top:4px}}
.hl{{color:{JK};-webkit-text-stroke:4px {OL};paint-order:stroke fill}}
.htile{{position:absolute;width:160px;height:160px;border-radius:38px;background:{INK};display:flex;align-items:center;justify-content:center;box-shadow:0 12px 0 {SH}}}
.qm{{font-size:110px;font-weight:700;color:{JK}}}
.lasttag{{position:absolute;font-size:34px;font-weight:700;background:{CO};border:5px solid {OL};border-radius:999px;padding:4px 20px;transform:rotate(-10deg)}}
.pill{{position:absolute;left:540px;top:212px;transform:translateX(-50%);display:flex;align-items:center;gap:14px;white-space:nowrap}}
.pnum{{font-size:32px;font-weight:700;background:{JK};border:5px solid {OL};border-radius:999px;padding:2px 18px}}
.pword{{font-size:34px;font-weight:600;color:{MUTED}}}
.card{{position:absolute;background:#fff;border:7px solid {OL};border-radius:44px;box-shadow:0 14px 0 {SH};padding:34px 44px;display:flex;flex-direction:column;gap:14px}}
.crow{{display:flex;justify-content:space-between;align-items:flex-start}}
.tile{{width:104px;height:104px;border-radius:28px;background:{INK};display:flex;align-items:center;justify-content:center}}
.cnum{{font-size:34px;font-weight:700;background:{YE};border:4px solid {OL};border-radius:999px;padding:2px 18px}}
.illo{{margin:6px 0 0 -6px}}
.ctitle{{font-size:64px;font-weight:700;line-height:1;align-self:flex-start;background:linear-gradient(transparent 70%,{JK} 70%)}}
.cdesc{{font-size:32px;font-weight:500;line-height:1.3;color:{MUTED}}}
.cfoot{{margin-top:auto;font-size:24px;font-weight:600;color:{MUTED};display:flex;align-items:center;gap:10px}}
.fdot{{width:16px;height:16px;border-radius:50%;background:{JK};border:3px solid {OL}}}
.dots{{position:absolute;left:540px;top:1036px;transform:translateX(-50%);display:flex;gap:12px;align-items:center}}
.dot{{width:16px;height:16px;border-radius:999px;background:{OL};opacity:.25}}
.spark{{position:absolute}}
.summary{{position:absolute;left:70px;top:190px;width:940px;height:880px;display:flex;flex-direction:column;justify-content:center;background:#fff;border:7px solid {OL};border-radius:48px;box-shadow:0 16px 0 {SH};padding:44px 48px}}
.stitle{{font-size:66px;font-weight:700;margin-bottom:48px;line-height:1.05}}
.sgrid{{display:grid;grid-template-columns:1fr 1fr;gap:52px 28px}}
.srow{{display:flex;gap:20px;align-items:center}}
.stile{{width:108px;height:108px;flex-shrink:0;border-radius:24px;background:{INK};display:flex;align-items:center;justify-content:center}}
.sname{{font-size:46px;font-weight:700;line-height:1.1}} .stag{{font-size:32px;font-weight:600;color:{MUTED}}}
.booSh{{position:absolute;height:34px;border-radius:50%;background:{SH}}}
#cap{{position:absolute;left:470px;top:1250px;width:570px;height:420px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:2px}}
.cs{{font-size:50px;font-weight:600;line-height:1.15;display:block}}
.cb{{font-size:118px;font-weight:700;line-height:1.02;color:{JK};-webkit-text-stroke:7px {OL};paint-order:stroke fill;text-transform:uppercase;display:block;white-space:nowrap}}
.w{{display:inline-block;margin:0 .12em}}
"""

JS = r"""
const T=%(T)s, TE=%(TE)s, CH=%(CH)s, WT=%(WT)s, NUMS=%(NUMS)s, NMOODS=%(NMOODS)s;
const $=id=>document.getElementById(id);
const cl=x=>Math.max(0,Math.min(1,x));
const back=p=>{const c=1.7;return 1+(c+1)*Math.pow(p-1,3)+c*Math.pow(p-1,2)};
const ease=p=>1-Math.pow(1-p,3);
const eio=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
let curChunk=-2;
function buildChunk(i){
  const cap=$('cap'); cap.innerHTML='';
  if(i<0) return;
  const ws=CH[i].words; let firstBig=ws.findIndex(w=>w.big), lastBig=-1;
  ws.forEach((w,j)=>{if(w.big) lastBig=j;});
  const lines=[[],[],[]];
  ws.forEach((w,j)=>{ const L = firstBig<0 ? 0 : (j<firstBig?0:(j<=lastBig?1:2)); lines[L].push([w,j]); });
  lines.forEach((ln,L)=>{ if(!ln.length) return; const d=document.createElement('div'); d.className=(L===1?'cb':'cs');
    ln.forEach(([w,j])=>{const s=document.createElement('span'); s.className='w'; s.id='w'+j; s.textContent=w.txt; if(w.txt.startsWith('@')) s.style.textTransform='none'; d.appendChild(s);});
    cap.appendChild(d);
    if(L===1){ let fs=118; d.style.fontSize=fs+'px'; while(d.scrollWidth>560 && fs>60){fs-=4; d.style.fontSize=fs+'px';} } });
}
window.render=function(t){
  // header
  $('head').style.opacity=cl((t-0.05)/0.3);
  // ---- hook tiles ----
  const out=cl((t-(T[1]-0.5))/0.22);
  for(let i=0;i<6;i++){ const p=cl((t-(CH[0].words[0].t+0.09*i))/0.4); const e=$('tile'+i);
    let wig = (i===5 && t>CH[4].words[1].t) ? Math.sin((t-CH[4].words[1].t)*22)*6*Math.exp(-(t-CH[4].words[1].t)*3) : 0;
    e.style.opacity=(p>0?1:0)*(1-out); e.style.transform=`translateY(${-120*ease(out)}px) rotate(${wig}deg) scale(${p>0?back(p):0})`; }
  const lp=cl((t-CH[4].words[1].t)/0.35); $('lastTag').style.opacity=(lp>0?1:0)*(1-out); $('lastTag').style.transform=`rotate(-10deg) scale(${lp>0?back(lp):0})`;
  // ---- carousel ----
  let c=0; for(let k=2;k<=6;k++) c+=eio(cl((t-(T[k]-0.35))/0.45));
  const inP=ease(cl((t-(T[1]-0.26))/0.45)); const endP=ease(cl((t-TE)/0.4));
  for(let i=0;i<6;i++){ const d=i-c, a=Math.abs(d); const e=$('card'+i);
    const sc=1-0.22*Math.min(1,a); let op= a<1 ? 1-0.55*a : Math.max(0,0.45*(1.7-a)/0.7);
    op*=inP*(1-endP);
    e.style.opacity=op; e.style.zIndex=String(100-Math.round(a*10));
    e.style.filter=`blur(${Math.min(6,a*5)}px)`;
    e.style.transform=`translateX(${d*590 + 700*(1-inP)}px) translateY(${-80*endP}px) scale(${sc})`; }
  // pill + dots
  const idx=Math.min(5,Math.round(c)); let lt=T[1]-0.1; for(let k=2;k<=6;k++) if(t>=T[k]-0.1) lt=T[k]-0.1;
  const pp=cl((t-lt)/0.35); const pill=$('pill'); pill.style.opacity=inP*(1-endP);
  pill.style.transform=`translateX(-50%) scale(${pp<1?0.8+0.2*back(pp):1})`;
  $('pnum').textContent='#0'+(idx+1); $('pword').textContent='Number '+NUMS[idx];
  $('dots').style.opacity=inP*(1-endP);
  for(let i=0;i<6;i++){ const e=$('dot'+i); const on=Math.max(0,1-Math.abs(i-c)); e.style.width=(16+30*on)+'px'; e.style.opacity=0.25+0.75*on; e.style.background=on>0.5?'%(JK)s':'%(OL)s'; }
  // sparkle on arrival
  const sp=cl((t-lt-0.1)/0.45); $('spark').style.opacity=(sp>0&&sp<1)?(1-sp):0; $('spark').style.transform=`scale(${0.7+0.6*sp})`;
  // ---- summary ----
  const sP=cl((t-(TE+0.15))/0.45); $('summary').style.opacity=sP>0?1:0; $('summary').style.transform=`scale(${sP>0?back(sP):0})`;
  for(let i=0;i<6;i++){ const p=cl((t-(TE+0.4+0.09*i))/0.35); const e=$('srow'+i); e.style.opacity=p; e.style.transform=`translateY(${20*(1-ease(p))}px)`; }
  // ---- Boo ----
  let line=0; for(let k=0;k<T.length;k++) if(t>=T[k]-0.05) line=k; const mood = t>=TE ? NMOODS-1 : line;
  for(let k=0;k<NMOODS;k++){ const o=k===mood?1:0; const b=$('mb'+k), f=$('mf'+k); if(b) b.style.opacity=o; if(f) f.style.opacity=o; }
  let lw=-9; for(const w of WT){ if(w<=t) lw=w; else break; }
  const bump=Math.exp(-Math.max(0,t-lw)/0.11)*(t-lw<0.6?1:0);
  let hop=0; if(t>TE+0.2){ const h=t-TE-0.2; hop=Math.abs(Math.sin(h*4.2))*28*Math.exp(-h*0.35); }
  const bob=Math.sin(t*2.6)*7;
  const bi=cl((t-0.0)/0.45);
  $('booWrap').style.transform=`translateY(${bob-hop}px) scale(${(bi>0?back(bi):0)*(1-0.03*bump)},${(bi>0?back(bi):0)*(1+0.045*bump)})`;
  $('booSh').style.opacity=bi; $('booSh').style.transform=`scaleX(${1-0.15*hop/28})`;
  // ---- captions ----
  let ci=-1; for(let i=0;i<CH.length;i++){ if(t>=CH[i].start-0.02 && t<CH[i].end) ci=i; }
  if(ci!==curChunk){ buildChunk(ci); curChunk=ci; }
  if(ci>=0){ CH[ci].words.forEach((w,j)=>{ const e=$('w'+j); if(!e) return; const p=cl((t-w.t+0.03)/(w.big?0.28:0.18));
      e.style.opacity=p>0?Math.min(1,p*2.5):0; e.style.transform = w.big ? `scale(${p>0?back(p):0.4})` : `translateY(${14*(1-ease(p))}px)`; }); }
};
"""


def fill_js(vals):
    out = JS
    for k, v in vals.items():
        out = out.replace('%(' + k + ')s', str(v))
    return out


def main():
    nums = [n for (_a, n, _b, _c, _d) in ITEMS]
    spark = ('<svg id="spark" class="spark" style="left:770px;top:250px" width="140" height="120" viewBox="0 0 140 120" aria-hidden="true">'
             f'<path d="M30 70 L8 84 M54 42 L44 14 M86 48 L110 22 M96 78 L128 74" stroke="{OL}" stroke-width="7" stroke-linecap="round"/></svg>')
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div id="head" class="head"><div class="bar"></div><div><div class="htitle">{TITLE}</div><div class="hhandle">@chirag.zip · explained by Boo</div></div></div>
{tiles}
<div id="pill" class="pill"><span id="pnum" class="pnum">#01</span><span id="pword" class="pword">Number one</span></div>
{cards}{spark}{dots}{summary}
{boo}
<div id="cap"></div>
<script>{fill_js(dict(T=json.dumps(T), TE=TE, CH=json.dumps(chunks), WT=json.dumps(WORD_TIMES), NUMS=json.dumps(nums), NMOODS=len(ALL_MOODS), JK=JK, OL=OL))}</script>
</body></html>"""
    open(os.path.join(HERE, "reel.html"), "w", encoding="utf-8").write(html)
    json.dump({"T": T, "TE": TE, "DUR": DUR}, open(os.path.join(HERE, "timeline.json"), "w"))
    print("built", "T", T, "TE", TE, "DUR", DUR)


if __name__ == "__main__":
    main()
