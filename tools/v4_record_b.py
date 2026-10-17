#!/usr/bin/env python3
"""
The record attempt page, design B: "Instrument panel" (owner, 17 Oct 2026:
"The design feels very robotic, too much text, difficult to navigate, make
it stunning", and "Add elements which awwwards worthy websites use").

    prototypes/v4/record-b.html

The page reads like a flight instrument: a dial as the opening (the mark to
beat against his best), the out-and-return course flown kilometre by
kilometre as the visitor scrolls, Kerio Valley with the photograph inside its
own name, the plan as a strip moved sideways by the scroll, and the
partnership as glass cards. A compact chapter bar (Record, Course, Kerio,
Plan, Partner) stays under the site's menu and fills as each chapter is read.

Facts are the ones in tools/v4_record.py (each from a source named on the
page or already on the site); anything not known shows as [to supply] or
[to confirm]. No new image files, no libraries, no video.

Motion only answers the visitor (scroll, pointer, tap, key): nothing loops
or runs on a timer. Reduced motion shows every finished state; with
JavaScript off everything is readable and the 100/200 km switch still works
(it is two radio buttons and CSS).

    python3 tools/v4_record_b.py
"""
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "record-b.html")

TITLE = "The Speed Record Attempt"
DESC = ("Aninder Singh's attempt on the paragliding world records for speed over a "
        "100 km and a 200 km out-and-return course, from Kerio Valley, Kenya, in "
        "January and February 2027. The marks, the course, the plan, and how to partner on it.")
URL = "https://paraglidingatlas.com/record-attempt.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/kenya/hero/kerio-valley.jpg"

REC100 = 35.94          # km/h, Michel Macquet (FRA), 23 Jan 2025, status to confirm
BEST = 36               # km/h, about, over 198.86 km, 6 Feb 2025 (not a record course)

A = "../../assets/"
KG = A + "destinations/kenya/gallery/"

TBD = '<span class="wr-tbd">[to supply]</span>'
TBC = '<span class="wr-tbd">[to confirm]</span>'

# a fine, still film grain (SVG noise, drawn once, never animated)
GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E"
         "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")")


def hm(km, kmh):
    m = int(round(km / kmh * 60))
    return "%d h %02d min" % (m // 60, m % 60)


def kin(text, tag="h2", hid=None, cls=""):
    """A heading whose words rise out of their own line as it comes into view.
    '|' starts a new line. The words are all in the markup, so search, screen
    readers and a page without JavaScript read the heading as it is."""
    out, i = [], 0
    for line in text.split("|"):
        ws = []
        for w in line.strip().split(" "):
            ws.append('<span class="w"><span style="--i:%d">%s</span></span>' % (i, w))
            i += 1
        out.append(" ".join(ws))
    return '<%s class="rb-k %s"%s>%s</%s>' % (
        tag, cls, (' id="%s"' % hid) if hid else "", "<br>".join(out), tag)


# ---------------------------------------------------------------- the dial
D_C, D_R = 250, 186            # centre and the photograph's radius (viewBox 500)
D_MAX, D_SWEEP, D_START = 50, 270.0, -135.0


def d_ang(v):
    return D_START + v / D_MAX * D_SWEEP


def d_xy(v, r):
    a = math.radians(d_ang(v))
    return D_C + r * math.sin(a), D_C - r * math.cos(a)


def d_arc(v0, v1, r):
    x0, y0 = d_xy(v0, r)
    x1, y1 = d_xy(v1, r)
    large = 1 if (v1 - v0) / D_MAX * D_SWEEP > 180 else 0
    return "M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f" % (x0, y0, r, r, large, x1, y1)


def dial_svg():
    p = []
    p.append('<path class="d-trk" d="%s"/>' % d_arc(0, D_MAX, 198))
    p.append('<path class="d-zone" d="%s"/>' % d_arc(REC100, D_MAX, 198))
    for v in range(0, D_MAX + 1):
        maj, mid = v % 10 == 0, v % 5 == 0
        r1 = 204 if maj else (206 if mid else 207)
        r2 = 222 if maj else (216 if mid else 212)
        x1, y1 = d_xy(v, r1)
        x2, y2 = d_xy(v, r2)
        p.append('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (
            "d-maj" if maj else "d-tk", x1, y1, x2, y2))
        if maj:
            tx, ty = d_xy(v, 238)
            p.append('<text class="d-n" x="%.1f" y="%.1f">%d</text>' % (tx, ty + 4, v))
    # the mark to beat: a white index across the ring
    x1, y1 = d_xy(REC100, 190)
    x2, y2 = d_xy(REC100, 228)
    p.append('<line class="d-mark" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x1, y1, x2, y2))
    # his best: the orange fill and pointer, turned by --a (final state in the markup)
    p.append('<path class="d-fill" pathLength="%d" d="%s"/>' % (D_MAX, d_arc(0, D_MAX, 198)))
    p.append('<g class="d-ptr"><path d="M%d %d L%d %d L%d %d Z"/><line x1="%d" y1="%d" x2="%d" y2="%d"/></g>' % (
        D_C - 6, D_C - 236, D_C + 6, D_C - 236, D_C, D_C - 224, D_C, D_C - 224, D_C, D_C - 190))
    p.append('<text class="d-u" x="%d" y="%d">km/h</text>' % (D_C, D_C + 226))
    return ('<svg class="rb-bezel" viewBox="0 0 500 500" aria-hidden="true">%s</svg>' % "".join(p))


# --------------------------------------------------------------- the course
def course_svg(kind):
    """The out-and-return course to scale: out along the top line, round the
    turnpoint, home along the bottom. The script flies the glider along it
    with the scroll; the markup holds the finished flight."""
    if kind == "wide":
        W, H, x0, x1, yo, yb, step, gs = 1000, 300, 110, 860, 128, 198, 50, 1.6
    else:
        W, H, x0, x1, yo, yb, step, gs = 360, 270, 52, 290, 112, 168, 30, 1.15
    r = (yb - yo) / 2.0
    my = (yo + yb) / 2.0
    cyl = r + (22 if kind == "wide" else 16)
    tid = "rbCT" + ("w" if kind == "wide" else "n")
    p = ['<title id="%s">An out-and-return course drawn to scale: from the start to a turnpoint at half the distance and straight back</title>' % tid]
    for gx in range(0, W + 1, step):
        p.append('<line class="g" x1="%d" y1="0" x2="%d" y2="%d"/>' % (gx, gx, H))
    for gy in range(0, H + 1, step):
        p.append('<line class="g" x1="0" y1="%d" x2="%d" y2="%d"/>' % (gy, W, gy))
    p.append('<circle class="cyl" cx="%d" cy="%g" r="%g"/>' % (x0, my, cyl))
    p.append('<circle class="cyl" cx="%d" cy="%g" r="%g"/>' % (x1, my, cyl))
    p.append('<path class="ghost" d="M%d %d H%d A%g %g 0 0 1 %d %d H%d"/>' % (x0, yo, x1, r, r, x1, yb, x0))
    p.append('<path class="fl" data-seg="o" pathLength="1" d="M%d %d H%d"/>' % (x0, yo, x1))
    p.append('<path class="fl" data-seg="t" pathLength="1" d="M%d %d A%g %g 0 0 1 %d %d"/>' % (x1, yo, r, r, x1, yb))
    p.append('<path class="fl" data-seg="b" pathLength="1" d="M%d %d H%d"/>' % (x1, yb, x0))
    for i in range(11):
        x = x0 + i * (x1 - x0) / 10.0
        ln = 9 if i % 5 == 0 else 5
        p.append('<line class="tk" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, yo - 10 - ln, x, yo - 10))
        p.append('<line class="tk" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, yb + 10, x, yb + 10 + ln))
    for i, (a, b) in ((0, ("0", "0")), (5, ("25", "50")), (10, ("50 km", "100 km"))):
        x = x0 + i * (x1 - x0) / 10.0
        anc = "start" if i == 0 else ("end" if i == 10 else "middle")
        dx = -4 if i == 0 else (6 if i == 10 else 0)
        p.append('<text class="lb v100" x="%.1f" y="%d" text-anchor="%s">%s</text>' % (x + dx, yo - 30, anc, a))
        p.append('<text class="lb v200" x="%.1f" y="%d" text-anchor="%s">%s</text>' % (x + dx, yo - 30, anc, b))
    p.append('<text class="pl" x="%d" y="%g" text-anchor="middle">Start, finish</text>' % (x0, my + cyl + 26))
    p.append('<text class="pl" x="%d" y="%g" text-anchor="middle">Turnpoint</text>' % (x1, my + cyl + 26))
    p.append('<g class="gl" transform="translate(%d %d) rotate(180) scale(%g)">'
             '<circle class="gl-h" r="15"/><path class="gl-l" d="M-5 -13 L-14 0 L-5 13"/>'
             '<path class="gl-w" d="M-5 -13 Q8 0 -5 13"/><circle class="gl-p" cx="-14" r="2.6"/></g>' % (x0, yb, gs))
    return ('<svg class="rb-trk is-%s" viewBox="0 0 %d %d" role="img" aria-labelledby="%s" '
            'data-x0="%d" data-x1="%d" data-yo="%d" data-yb="%d" data-gs="%g">%s</svg>') % (
        kind, W, H, tid, x0, x1, yo, yb, gs, "".join(p))


def vario_svg():
    # 0 to 8 m/s; the midday peaks 4 to 6, the rare surges 6 to 7
    x0, x1, y = 6, 234, 22
    u = (x1 - x0) / 8.0
    p = ['<line class="v-base" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x0, y, x1, y)]
    for v in range(9):
        x = x0 + v * u
        p.append('<line class="v-tk" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, y - (6 if v % 2 == 0 else 3), x, y + (6 if v % 2 == 0 else 3)))
        if v in (0, 4, 6, 8):
            p.append('<text class="v-n" x="%.1f" y="%d">%d</text>' % (x, y + 20, v))
    p.append('<rect class="v-pk" x="%.1f" y="%d" width="%.1f" height="8"/>' % (x0 + 4 * u, y - 4, 2 * u))
    p.append('<rect class="v-rr" x="%.1f" y="%d" width="%.1f" height="8"/>' % (x0 + 6 * u, y - 4, u))
    return '<svg class="rb-vario" viewBox="0 0 240 46" aria-hidden="true">%s</svg>' % "".join(p)


ICO = {
    "prep": '<path d="M7 9h3M7 16h3M7 23h3"/><path d="M14 9h11M14 16h11M14 23h7"/>',
    "wing": '<path d="M4 13 Q16 3 28 13"/><path d="M5 13 L16 27 L27 13M10 9.5 L16 27 L22 9.5"/><circle cx="16" cy="27" r="1.6"/>',
    "team": '<path d="M3 16 Q16 5 29 16 Q16 27 3 16Z"/><circle cx="16" cy="16" r="4.5"/>',
    "claim": '<path d="M8 4h11l6 6v18H8Z"/><path d="M19 4v6h6"/><path d="M12 19l3 3 6-7"/>',
}


def ico(k):
    return ('<svg class="rb-ico" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICO[k])


def days():
    # 18 Jan to 12 Feb 2027, one cell a day: two expeditions and the two days between
    cells = []
    for i in range(26):
        exp = i < 12 or i >= 14
        cells.append('<i class="%s"></i>' % ("on" if exp else "off"))
    return '<div class="rb-days" aria-hidden="true">%s</div>' % "".join(cells)


CSS = r"""
/* ===== The record attempt, design B: the instrument panel (tools/v4_record_b.py) ===== */
.rb{--rb-bar:56px;--rb-mono:var(--font-mono,ui-monospace,monospace);
  --rb-glass:color-mix(in srgb,var(--card) 52%,transparent);
  --rb-sheen:linear-gradient(180deg,color-mix(in srgb,var(--white) 5%,transparent),transparent 42%);
  --rb-grain:__GRAIN__;
  position:relative;overflow-x:clip;}
html{scroll-padding-top:calc(var(--rb-bar,56px) + 1.25rem);}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth;}}
.rb *{-webkit-tap-highlight-color:transparent;}
.rb-in{max-width:var(--measure);margin:0 auto;padding:0 var(--gutter);}
.wr-tbd{font-style:italic;font-weight:400;color:var(--gray);white-space:nowrap;letter-spacing:0;text-transform:none;font-family:var(--font-body);}
.rb-lab{display:block;font-family:var(--rb-mono);font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--gray-light);font-weight:400;}
.rb-num{font-family:var(--font-display);font-variant-numeric:tabular-nums;letter-spacing:-.03em;}
.rb-ct{display:inline-block;text-align:left;font-variant-numeric:tabular-nums;}

/* film grain over the dark bands: still, drawn once */
.rb-grain{position:relative;isolation:isolate;}
.rb-grain::after{content:"";position:absolute;inset:0;z-index:3;pointer-events:none;background:var(--rb-grain);background-size:180px 180px;opacity:.07;}

/* headings whose words rise out of their own line */
.rb-k .w{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .02em .16em;margin:0 -.02em -.16em;}
.rb-k .w > span{display:inline-block;}
@media (prefers-reduced-motion:no-preference){
  .rb-js .rb-k .w > span{transform:translateY(112%);transition:transform 1.15s var(--ease);transition-delay:calc(var(--i) * 70ms);}
  .rb-js .rb-k.is-in .w > span{transform:none;}
  .rb-js:not(.rb-live) .rb-k .w > span{animation:rb-safe 0s 2.5s forwards;}
}
@keyframes rb-safe{to{transform:none;clip-path:inset(0);opacity:1;}}

/* ---------------------------------------------------------------- the opening */
.rb-hero{min-height:min(calc(100svh - 93px - var(--rb-bar)),1000px);display:flex;align-items:center;overflow:hidden;
  background:radial-gradient(ellipse 55% 60% at 74% 46%,var(--sky-warm),transparent 70%),
             radial-gradient(ellipse 45% 50% at 8% 100%,var(--sky-cool),transparent 70%),
             linear-gradient(180deg,var(--bg),color-mix(in srgb,var(--bg) 70%,var(--card)) 60%,var(--bg));}
.rb-hero-in{position:relative;z-index:1;width:100%;max-width:var(--measure);margin:0 auto;padding:clamp(2rem,5vh,4rem) var(--gutter) clamp(2.5rem,6vh,4.5rem);
  display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"txt dial" "pair dial";column-gap:clamp(1.5rem,4vw,4.5rem);align-items:center;}
.rb-hero-txt{grid-area:txt;align-self:end;}
.rb-dial{grid-area:dial;}
.rb-pair{grid-area:pair;align-self:start;}
.rb-kick{display:block;margin:0 0 1.4rem;color:var(--orange);font-family:var(--font-body);font-size:var(--fs-micro);font-weight:600;letter-spacing:.18em;text-transform:uppercase;}
.rb-h1{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * 1.62);line-height:.9;letter-spacing:-.045em;color:var(--white);}
.rb-lede{margin:1.6rem 0 0;max-width:27rem;font-size:var(--fs-lead);line-height:1.55;color:var(--gray-light);}
.rb-pair{display:grid;grid-template-columns:repeat(2,minmax(0,max-content));gap:0;margin:2.4rem 0 0;border-top:1px solid var(--line);width:max-content;max-width:100%;}
.rb-pair > div{padding:1.1rem 2.4rem 0 0;}
.rb-pair > div + div{padding-left:2.4rem;border-left:1px solid var(--line);}
.rb-pair dt{display:flex;align-items:center;gap:.55rem;}
.rb-pair dt::before{content:"";width:14px;height:2px;background:var(--white);}
.rb-pair .is-best dt::before{background:var(--orange);}
.rb-pair dd{margin:.55rem 0 0;}
.rb-pair .v{font-family:var(--font-display);font-weight:600;font-size:calc(var(--fs-h1) * .95);line-height:1;color:var(--white);letter-spacing:-.03em;}
.rb-pair .is-best .v{color:var(--orange);}
.rb-pair small{font-family:var(--rb-mono);font-size:var(--fs-small);color:var(--gray-light);margin-left:.4rem;letter-spacing:0;}
.rb-pair .s{margin-top:.5rem;font-size:var(--fs-small);color:var(--gray);}

.rb-dial{position:relative;margin:0;width:min(42vw,560px,calc(100svh - 93px - var(--rb-bar) - 6rem));min-width:300px;aspect-ratio:1;}
.rb-dial::before{content:"";position:absolute;inset:4%;border-radius:50%;z-index:-1;
  background:url(__KG__kenya-hero.webp) 64% 58%/cover;filter:blur(56px) saturate(1.25);opacity:.38;}
.rb-port{position:absolute;inset:12.8%;border-radius:50%;overflow:hidden;
  box-shadow:0 0 0 1px var(--edge),0 30px 80px -30px color-mix(in srgb,var(--bg) 90%,transparent);}
.rb-port picture,.rb-port img{display:block;width:100%;height:100%;}
.rb-port img{object-fit:cover;object-position:64% 58%;transform:scale(1.12);transform-origin:60% 55%;}
.rb-port::after{content:"";position:absolute;inset:0;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle at 50% 50%,transparent 58%,color-mix(in srgb,var(--bg) 55%,transparent) 100%),
             linear-gradient(160deg,color-mix(in srgb,var(--white) 10%,transparent),transparent 38%);}
.rb-bezel{position:absolute;inset:0;width:100%;height:100%;overflow:visible;}
.rb-bezel .d-trk{fill:none;stroke:var(--edge);stroke-width:2;}
.rb-bezel .d-zone{fill:none;stroke:color-mix(in srgb,var(--white) 30%,transparent);stroke-width:2;stroke-dasharray:1 3;}
.rb-bezel .d-tk{stroke:var(--edge-hi);stroke-width:1;}
.rb-bezel .d-maj{stroke:var(--gray-light);stroke-width:1.6;}
.rb-bezel .d-n{fill:var(--gray);font-family:var(--rb-mono);font-size:14px;text-anchor:middle;}
.rb-bezel .d-u{fill:var(--gray-light);font-family:var(--rb-mono);font-size:13px;letter-spacing:.14em;text-anchor:middle;text-transform:uppercase;}
.rb-bezel .d-mark{stroke:var(--white);stroke-width:2.5;stroke-linecap:round;}
.rb-bezel .d-fill{fill:none;stroke:var(--orange);stroke-width:3;stroke-linecap:round;stroke-dasharray:var(--f,36) 60;}
.rb-bezel .d-ptr{transform:rotate(var(--a,59.4deg));transform-origin:250px 250px;}
.rb-bezel .d-ptr path{fill:var(--orange);}
.rb-bezel .d-ptr line{stroke:var(--orange);stroke-width:2;}

/* ------------------------------------------------------------- the chapter bar */
.rb-bar{position:sticky;top:0;z-index:50;height:var(--rb-bar);
  background:color-mix(in srgb,var(--bg) 84%,transparent);-webkit-backdrop-filter:blur(14px) saturate(1.2);backdrop-filter:blur(14px) saturate(1.2);
  border-top:1px solid var(--line);border-bottom:1px solid var(--line);transition:transform .38s var(--ease);}
html.v2-nav-up .rb-bar{transform:translateY(var(--v2-nav-h,77px));}
.rb-bar ol{list-style:none;margin:0 auto;padding:0 var(--gutter);max-width:var(--measure);height:100%;display:flex;}
.rb-bar li{flex:1 1 0;min-width:0;}
.rb-bar a{position:relative;display:flex;align-items:center;gap:.6rem;height:100%;min-height:44px;padding:0 .2rem;text-decoration:none;color:var(--gray);
  font-family:var(--rb-mono);font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;transition:color .3s var(--ease);}
.rb-bar a::before{content:"";width:5px;height:5px;border-radius:50%;border:1px solid currentColor;transition:background-color .3s var(--ease),border-color .3s var(--ease);}
.rb-bar a[aria-current]::before{background:var(--orange);border-color:var(--orange);}
.rb-bar a:hover,.rb-bar a[aria-current]{color:var(--white);}
.rb-bar a:focus-visible{outline:2px solid var(--white);outline-offset:-6px;}
.rb-bar a i{position:absolute;left:0;right:.9rem;bottom:-1px;height:2px;background:var(--orange);transform:scaleX(var(--p,0));transform-origin:0 50%;}

/* ---------------------------------------------------------- the scroll ticker */
.rb-tick{overflow:hidden;padding:clamp(1.8rem,4vw,3rem) 0;border-bottom:1px solid var(--line);}
.rb-tick-tr{display:flex;align-items:center;gap:clamp(1.2rem,3vw,2.6rem);width:max-content;white-space:nowrap;padding-left:var(--gutter);will-change:transform;}
.rb-tick span{font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * 1.35);line-height:1;letter-spacing:-.035em;
  color:transparent;-webkit-text-stroke:1px var(--edge-hi);}
.rb-tick span.is-on{color:var(--white);-webkit-text-stroke:0;}
.rb-tick i{flex:none;width:.7rem;height:.7rem;border-radius:50%;background:var(--orange);}

/* ---------------------------------------------------------------- chapters */
.rb-ch{position:relative;padding:var(--sp-section) 0;}
.rb-ch + .rb-ch{border-top:1px solid var(--line);}
.rb-head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem 2rem;align-items:end;margin:0 0 clamp(2rem,4vw,3.2rem);}
.rb-head .rb-lab{grid-column:1 / -1;display:flex;align-items:center;gap:.9rem;}
.rb-head .rb-lab::after{content:"";flex:0 0 3rem;height:1px;background:var(--edge-hi);}
.rb-h2{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-h1) * 1.08);line-height:.98;letter-spacing:-.035em;color:var(--white);max-width:15ch;}
.rb-cap{margin:0;max-width:24rem;font-size:var(--fs-body-s);line-height:1.55;color:var(--gray-light);}
.rb-head .rb-cap{justify-self:end;text-align:right;max-width:30rem;}
.rb-a{color:var(--gray-light);text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 100%/100% 1px no-repeat;
  transition:color .3s var(--ease),background-size .45s var(--ease);}
.rb-a:hover{color:var(--white);background-size:0 1px;background-position:100% 100%;}
.rb-a:focus-visible{outline:2px solid var(--white);outline-offset:3px;}

/* glass cards, read like a cockpit display */
.rb-card{position:relative;padding:clamp(1.2rem,2vw,1.6rem);background:var(--rb-sheen),var(--rb-glass);border:1px solid var(--line);
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);}
.rb-card::before{content:"";position:absolute;inset:-1px;pointer-events:none;--c:var(--edge-hi);
  background:linear-gradient(var(--c),var(--c)) 0 0/12px 1px no-repeat,linear-gradient(var(--c),var(--c)) 0 0/1px 12px no-repeat,
    linear-gradient(var(--c),var(--c)) 100% 0/12px 1px no-repeat,linear-gradient(var(--c),var(--c)) 100% 0/1px 12px no-repeat,
    linear-gradient(var(--c),var(--c)) 0 100%/12px 1px no-repeat,linear-gradient(var(--c),var(--c)) 0 100%/1px 12px no-repeat,
    linear-gradient(var(--c),var(--c)) 100% 100%/12px 1px no-repeat,linear-gradient(var(--c),var(--c)) 100% 100%/1px 12px no-repeat;}
.rb-card.is-lit::before{--c:var(--orange);}

/* 01 the record */
.rb-marks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(.8rem,1.6vw,1.25rem);}
.rb-mark{display:flex;flex-direction:column;min-height:14.5rem;}
.rb-mark .big{margin:auto 0 0;padding-top:2rem;font-family:var(--font-display);font-weight:600;font-size:calc(var(--fs-h1) * 1.2);line-height:1;color:var(--white);letter-spacing:-.035em;}
.rb-mark .big small{font-family:var(--rb-mono);font-size:var(--fs-small);font-weight:400;letter-spacing:0;color:var(--gray-light);margin-left:.5rem;}
.rb-mark .big .wr-tbd{font-size:var(--fs-h3);letter-spacing:0;}
.rb-mark .big .sub{display:block;margin-top:.55rem;font-family:var(--rb-mono);font-size:var(--fs-small);font-weight:400;letter-spacing:0;color:var(--gray-light);}
.rb-mark.is-lit .big{color:var(--orange);}
.rb-mark .ft{margin:1rem 0 0;padding-top:.9rem;border-top:1px solid var(--line);font-size:var(--fs-small);line-height:1.6;color:var(--gray-light);}
.rb-mark .ft span{color:var(--gray);}

/* 02 the course */
.rb-course .rb-pin,.rb-pin > .rb-in{width:100%;}
.rb-mfd{position:relative;padding:clamp(1rem,2.4vw,2rem);}
.rb-seg{position:absolute;z-index:2;top:clamp(1rem,2.4vw,2rem);right:clamp(1rem,2.4vw,2rem);display:inline-flex;border:1px solid var(--edge);padding:3px;margin:0;min-width:0;background:color-mix(in srgb,var(--bg) 70%,transparent);}
.rb-seg legend{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}
.rb-seg input{position:absolute;opacity:0;width:1px;height:1px;margin:0;}
.rb-seg label{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:5.6rem;padding:0 1rem;cursor:pointer;
  font-family:var(--rb-mono);font-size:var(--fs-small);color:var(--gray-light);transition:color .3s var(--ease),background-color .3s var(--ease);}
.rb-seg input:checked + label{background:var(--orange);color:var(--ink);}
.rb-seg input:focus-visible + label{outline:2px solid var(--white);outline-offset:2px;}
.rb-seg label:hover{color:var(--white);}
.rb-seg input:checked + label:hover{color:var(--ink);}
.rb-course .v200{display:none;}
.rb-course:has(#rbk200:checked) .v200{display:inline;}
.rb-course:has(#rbk200:checked) .v100{display:none;}
.rb-trk{display:block;width:100%;height:auto;overflow:visible;}
.rb-trk.is-narrow{display:none;}
.rb-trk .g{stroke:color-mix(in srgb,var(--white) 4%,transparent);stroke-width:1;}
.rb-trk .cyl{fill:color-mix(in srgb,var(--white) 2%,transparent);stroke:var(--edge);stroke-width:1;stroke-dasharray:3 4;}
.rb-trk .ghost{fill:none;stroke:var(--edge);stroke-width:2;}
.rb-trk .fl{fill:none;stroke:var(--orange);stroke-width:3;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:0;}
.rb-trk .tk{stroke:var(--edge-hi);stroke-width:1;}
.rb-trk .lb{fill:var(--gray);font-family:var(--rb-mono);font-size:13px;}
.rb-trk .pl{fill:var(--gray-light);font-family:var(--rb-mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;}
.rb-trk .gl-h{fill:var(--wash);}
.rb-trk .gl-w{fill:none;stroke:var(--orange);stroke-width:3.5;stroke-linecap:round;}
.rb-trk .gl-l{fill:none;stroke:var(--gray-light);stroke-width:.8;}
.rb-trk .gl-p{fill:var(--white);}
.rb-ro{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin:1.2rem 0 0;border-top:1px solid var(--line);}
.rb-ro > div{padding:1rem 1rem 0 0;}
.rb-ro > div + div{padding-left:1.1rem;border-left:1px solid var(--line);}
.rb-ro dd{margin:.45rem 0 0;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);line-height:1.1;color:var(--white);font-variant-numeric:tabular-nums;letter-spacing:-.02em;white-space:nowrap;}
.rb-ro dd small{font-family:var(--rb-mono);font-weight:400;font-size:var(--fs-small);color:var(--gray-light);letter-spacing:0;margin-left:.35rem;}
.rb-ro .is-lit dd{color:var(--orange);}
.rb-ro .wr-tbd{font-size:var(--fs-body);}

/* 03 Kerio Valley */
.rb-kerio{overflow-x:clip;background:radial-gradient(ellipse 60% 50% at 80% 10%,var(--sky-horizon),transparent 70%);}
.rb-kt{margin:0;font-family:var(--font-display);font-weight:800;font-size:min(calc(var(--fs-display) * 3.7),27vw);line-height:.8;letter-spacing:-.055em;color:var(--white);padding:.16em 0 .08em;}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
  .rb-kt{background:url(__KG__kenya-ridge.webp) 50% 96%/135% auto no-repeat;-webkit-background-clip:text;background-clip:text;color:transparent;filter:saturate(1.35) contrast(1.12) brightness(1.18);}
}
.rb-kt-mask{overflow:hidden;}
.rb-kerio .rb-head{margin-bottom:1.2rem;}
.rb-kerio-sub{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,24rem);gap:2rem;align-items:start;margin:0 0 clamp(2rem,5vw,4rem);}
.rb-kerio-sub .rb-cap{grid-column:2;max-width:none;}
.rb-stage{position:relative;margin-bottom:clamp(2rem,6vw,5rem);display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:clamp(1rem,3vw,3rem);align-items:start;}
.rb-phs{position:relative;}
.rb-ph{position:relative;margin:0;overflow:hidden;}
.rb-ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease);}
.rb-ph-a{aspect-ratio:3 / 2;}
.rb-ph-b{position:absolute;z-index:2;left:calc(61% - 9rem);bottom:-4.5rem;width:clamp(9rem,17vw,15rem);aspect-ratio:4 / 5;box-shadow:0 30px 60px -20px color-mix(in srgb,var(--bg) 85%,transparent);border:1px solid var(--edge);}
.rb-ph-b img{object-position:52% 40%;}
@media (hover:hover) and (pointer:fine){ .rb-ph:hover img{transform:scale(1.04);} }
.rb-kd{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(.7rem,1.2vw,1rem);margin:0;}
.rb-kd .rb-card{padding:1.05rem 1.2rem 1.15rem;}
.rb-kd dd{margin:.5rem 0 0;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);line-height:1.25;color:var(--white);}
.rb-kd dd small{display:block;margin-top:.2rem;font-family:var(--font-body);font-weight:400;font-size:var(--fs-small);color:var(--gray-light);}
.rb-vario{display:block;width:100%;max-width:17rem;height:auto;margin:.8rem 0 0;overflow:visible;}
.rb-vario .v-base{stroke:var(--edge-hi);stroke-width:1;}
.rb-vario .v-tk{stroke:var(--edge-hi);stroke-width:1;}
.rb-vario .v-n{fill:var(--gray);font-family:var(--rb-mono);font-size:11px;text-anchor:middle;}
.rb-vario .v-pk{fill:var(--orange);}
.rb-vario .v-rr{fill:color-mix(in srgb,var(--orange) 35%,transparent);stroke:var(--orange);stroke-width:1;stroke-dasharray:2 2;}

/* 04 the plan, a strip the scroll moves sideways */
.rb-hz-vp{position:relative;}
.rb-hz-tr{display:flex;flex-wrap:wrap;gap:clamp(.8rem,1.6vw,1.25rem);}
.rb-phase{flex:1 1 16rem;display:flex;flex-direction:column;min-width:0;}
.rb-phase.is-3{flex:1 1 100%;}
.rb-phase.is-w{flex:2 1 30rem;}
.rb-phase-h{display:flex;align-items:baseline;gap:.9rem;flex-wrap:wrap;margin:0 0 .9rem;padding:0 0 .9rem;border-bottom:1px solid var(--edge);font-size:var(--fs-small);color:var(--gray-light);position:relative;}
.rb-phase-h::before{content:"";position:absolute;left:0;bottom:-4px;width:7px;height:7px;border-radius:50%;background:var(--bg);border:1px solid var(--gray-light);}
.rb-phase.is-w .rb-phase-h::before{background:var(--orange);border-color:var(--orange);box-shadow:0 0 0 5px var(--wash);}
.rb-phase.is-w .rb-phase-h{border-bottom-color:var(--live);}
.rb-wps{list-style:none;margin:0;padding:0;display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);gap:clamp(.8rem,1.6vw,1.25rem);flex:1;}
.rb-wp{display:flex;flex-direction:column;min-height:12.5rem;}
.rb-plan.is-pin .rb-wp{min-height:clamp(13rem,40vh,22rem);}
.rb-ch.is-pin{padding-bottom:0;}
.rb-wp h3{margin:auto 0 0;padding-top:1.4rem;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);line-height:1.15;color:var(--white);letter-spacing:-.01em;}
.rb-wp p{margin:.5rem 0 0;font-size:var(--fs-small);color:var(--gray-light);line-height:1.5;}
.rb-wp .rb-lab{color:var(--gray);}
.rb-ico{display:block;width:2.1rem;height:2.1rem;color:var(--gray-light);}
.rb-wp:hover .rb-ico{color:var(--orange);}
.rb-ico{transition:color .4s var(--ease);}
.rb-days{display:grid;grid-template-columns:repeat(26,minmax(0,1fr));gap:3px;margin:1.6rem 0 0;}
.rb-days i{display:block;height:2.2rem;background:var(--orange);opacity:.9;}
.rb-days i.off{background:none;border:1px dashed var(--edge-hi);opacity:1;}
.rb-dayl{display:grid;grid-template-columns:12fr 2fr 12fr;gap:3px;margin:.55rem 0 0;font-family:var(--rb-mono);font-size:var(--fs-micro);color:var(--gray-light);letter-spacing:.06em;}
.rb-dayl span:last-child{grid-column:3;}
.rb-hz-prog{display:none;}

/* 05 partner */
.rb-aud{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--edge);border-bottom:1px solid var(--line);margin:0 0 clamp(2rem,4vw,3rem);}
.rb-aud > div{padding:1.3rem 1rem 1.3rem 0;}
.rb-aud > div + div{padding-left:1.4rem;border-left:1px solid var(--line);}
.rb-aud dd{margin:0;font-family:var(--font-display);font-weight:600;font-size:calc(var(--fs-h1) * .92);line-height:1;color:var(--white);letter-spacing:-.035em;}
.rb-aud dt{margin:.6rem 0 0;}
.rb-tiers{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) minmax(0,1fr);gap:clamp(.8rem,1.6vw,1.25rem);}
.rb-tier{display:flex;flex-direction:column;transition:transform .5s var(--ease),border-color .5s var(--ease);}
.rb-tier h3{margin:0 0 1.2rem;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-h3) * 1.18);line-height:1.05;color:var(--white);letter-spacing:-.025em;}
.rb-tier ul{list-style:none;margin:0;padding:0;}
.rb-tier li{position:relative;padding:.6rem 0 .6rem 1.4rem;border-top:1px solid var(--line);font-size:var(--fs-body-s);line-height:1.45;color:var(--gray-light);}
.rb-tier li::before{content:"";position:absolute;left:0;top:1.15em;width:.7rem;height:1px;background:var(--orange);}
.rb-tier.is-lit{background:radial-gradient(ellipse 80% 60% at 0 0,var(--wash),transparent 70%),var(--rb-sheen),var(--rb-glass);}
@media (hover:hover) and (pointer:fine){ .rb-tier:hover{transform:translateY(var(--lift));border-color:var(--edge);} }
.rb-tier .rb-chip{position:absolute;top:clamp(1.2rem,2vw,1.6rem);right:clamp(1.2rem,2vw,1.6rem);}
.rb-chip{display:inline-flex;align-items:center;min-height:1.6rem;padding:0 .6rem;border:1px solid var(--edge-hi);font-family:var(--rb-mono);font-size:var(--fs-micro);color:var(--gray-light);letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;}
.rb-tier.is-lit .rb-chip{border-color:var(--live);color:var(--white);}
.rb-close{position:relative;margin:clamp(2.5rem,5vw,4rem) 0 0;display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:clamp(1.2rem,3vw,2.5rem);align-items:center;
  padding:clamp(1.4rem,3vw,2.2rem);border:1px solid var(--edge);overflow:hidden;
  background:radial-gradient(ellipse 50% 120% at 100% 50%,var(--sky-warm),transparent 70%),var(--card);}
.rb-close img{display:block;width:clamp(5rem,9vw,7.5rem);height:auto;aspect-ratio:4 / 5;object-fit:cover;object-position:50% 22%;}
.rb-who b{display:block;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);color:var(--white);}
.rb-who p{margin:.4rem 0 0;font-size:var(--fs-small);line-height:1.6;color:var(--gray-light);max-width:30rem;}
.rb-cta{display:flex;flex-wrap:wrap;gap:.8rem;justify-content:flex-end;position:relative;z-index:4;}
.rb-btn{display:inline-flex;align-items:center;gap:.7rem;min-height:52px;padding:0 1.5rem;font-family:var(--font-body);font-weight:600;font-size:var(--fs-body-s);text-decoration:none;
  color:var(--white);border:1px solid var(--edge-hi);background:color-mix(in srgb,var(--bg) 40%,transparent);
  transition:transform .55s var(--ease),border-color .3s var(--ease),background-color .3s var(--ease),color .3s var(--ease);}
.rb-btn svg{width:16px;height:16px;flex:none;transition:transform .45s var(--ease);}
.rb-btn:hover{border-color:var(--white);}
.rb-btn:hover svg{transform:translateX(3px);}
.rb-btn.is-main{background:var(--orange);border-color:var(--orange);color:var(--ink);}
.rb-btn.is-main:hover{background:color-mix(in srgb,var(--orange) 88%,var(--white));}
.rb-btn:focus-visible{outline:2px solid var(--white);outline-offset:3px;}
.rb-src{margin:1.4rem 0 0;font-size:var(--fs-small);line-height:1.9;color:var(--gray);}
.rb-src .rb-a{color:var(--gray-light);}

/* the cursor: a small ring that follows a mouse, never a finger */
.rb-cur{position:fixed;left:0;top:0;z-index:95;width:34px;height:34px;margin:-17px 0 0 -17px;pointer-events:none;opacity:0;transition:opacity .3s var(--ease);}
.rb-cur.is-on{opacity:1;}
.rb-cur i{display:block;width:100%;height:100%;border-radius:50%;border:1px solid color-mix(in srgb,var(--white) 55%,transparent);transition:transform .45s var(--ease),border-color .3s var(--ease),background-color .3s var(--ease);}
.rb-cur.is-big i{transform:scale(1.7);border-color:var(--orange);background:color-mix(in srgb,var(--orange) 8%,transparent);}
.rb-cur.is-trk i{transform:scale(2.4);border-color:var(--orange);}

/* ---------------------------------------------- motion (only with the scroll) */
@media (prefers-reduced-motion:no-preference){
  /* the porthole opens on arrival, as part of the visitor's first look */
  .rb-js .rb-port{clip-path:circle(0% at 50% 50%);transition:clip-path 1.6s var(--ease) .15s;}
  .rb-js .rb-dial.is-in .rb-port{clip-path:circle(50% at 50% 50%);}
  .rb-js:not(.rb-live) .rb-port{animation:rb-safe 0s 2.5s forwards;}
  .rb-js .rb-bezel .d-ptr{transition:none;}
  /* depth: photographs drift at their own speed while they pass */
  @supports (animation-timeline:view()){
    .rb-port img{animation:rb-port linear both;animation-timeline:view();animation-range:exit -20% exit 100%;}
    @keyframes rb-port{from{transform:scale(1.12) translateY(0);}to{transform:scale(1.25) translateY(6%);}}
    .rb-tick-tr{animation:rb-tick linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
    @keyframes rb-tick{from{transform:translateX(0);}to{transform:translateX(-38%);}}
    .rb-kt-mask .rb-kt{animation:rb-rise linear both;animation-timeline:view();animation-range:entry 0% entry 90%;}
    @keyframes rb-rise{from{transform:translateY(55%);}to{transform:none;}}
    .rb-clip{animation:rb-clip linear both;animation-timeline:view();animation-range:entry 0% cover 42%;}
    @keyframes rb-clip{from{clip-path:inset(16% 18% 16% 0);}to{clip-path:inset(0 0 0 0);}}
    .rb-clip img{animation:rb-zoom linear both;animation-timeline:view();animation-range:entry 0% exit 100%;}
    @keyframes rb-zoom{from{transform:scale(1.25) translateY(-3%);}to{transform:scale(1.04) translateY(3%);}}
    .rb-ph-b{animation:rb-float linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
    @keyframes rb-float{from{transform:translateY(var(--rb-float,5rem));}to{transform:translateY(calc(var(--rb-float,5rem) * -1));}}
  }
  @supports not (animation-timeline:view()){
    .rb-js .rb-clip{clip-path:inset(16% 18% 16% 0);transition:clip-path 1.5s var(--ease);}
    .rb-js .rb-clip.is-in{clip-path:inset(0 0 0 0);}
    .rb-js:not(.rb-live) .rb-clip{animation:rb-safe 0s 2.5s forwards;}
  }
  /* cards come up into place once, as they are reached */
  .rb-js .rb-up{opacity:0;transform:translateY(28px);transition:opacity .9s var(--ease),transform 1.1s var(--ease);transition-delay:calc(var(--d,0) * 90ms);}
  .rb-js .rb-up.is-in{opacity:1;transform:none;}
  .rb-js:not(.rb-live) .rb-up{animation:rb-safe 0s 2.5s forwards;}
}
/* the course is pinned and flown with the scroll, the plan slides sideways: wide screens, motion allowed, script running */
.rb-course.is-pin{height:calc(100vh + 150vh);}
.rb-course.is-pin .rb-pin{position:sticky;top:var(--rb-bar);height:calc(100vh - var(--rb-bar));padding:clamp(.5rem,2vh,1.5rem) 0;}
.rb-course.is-pin .rb-head{margin-bottom:clamp(1rem,2.4vh,2rem);}
.rb-plan.is-pin .rb-pin{position:sticky;top:var(--rb-bar);height:calc(100vh - var(--rb-bar));overflow:hidden;}
.rb-plan.is-pin .rb-hz-vp{overflow:visible;}
.rb-plan.is-pin .rb-hz-tr{flex-wrap:nowrap;width:max-content;will-change:transform;}
.rb-plan.is-pin .rb-phase{flex:none;width:clamp(19rem,25vw,23rem);}
.rb-plan.is-pin .rb-phase.is-3{width:calc(3 * clamp(15rem,20vw,19rem) + 2.5rem);}
.rb-plan.is-pin .rb-phase.is-w{width:clamp(30rem,40vw,38rem);}
.rb-plan.is-pin .rb-hz-prog{display:block;position:relative;height:1px;margin:2rem 0 0;background:var(--line);}
.rb-plan.is-pin .rb-hz-prog i{position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--p,0));transform-origin:0 50%;}

@media (prefers-reduced-motion:reduce){
  .rb *,.rb *::before,.rb *::after{transition:none!important;animation:none!important;}
}

/* ---------------------------------------------------------------- widths */
@media (max-width:1100px){
  .rb-tiers{grid-template-columns:repeat(2,minmax(0,1fr));}
  .rb-tier.is-lit{grid-column:1 / -1;}
  .rb-close{grid-template-columns:auto minmax(0,1fr);}
  .rb-cta{grid-column:1 / -1;justify-content:flex-start;}
}
@media (max-width:820px){
  .rb{--rb-bar:50px;}
  .rb-hero{min-height:0;display:block;}
  .rb-hero-in{grid-template-columns:minmax(0,1fr);grid-template-areas:"txt" "dial" "pair";row-gap:1.4rem;padding-top:1.4rem;padding-bottom:2rem;}
  .rb-h1{font-size:calc(var(--fs-display) * 1.42);}
  .rb-lede{margin-top:1.1rem;}
  .rb-dial{width:min(84%,22rem);min-width:0;margin:0 auto;}
  .rb-pair{margin-top:0;grid-template-columns:repeat(2,minmax(0,1fr));width:auto;}
  .rb-pair > div{padding-right:1rem;}
  .rb-pair > div + div{padding-left:1rem;}
  .rb-pair .v{font-size:calc(var(--fs-h1) * 1.05);}
  .rb-bar ol{padding:0 .5rem;}
  .rb-bar a{justify-content:center;gap:0;padding:0;letter-spacing:.08em;}
  .rb-bar a::before{display:none;}
  .rb-bar a i{right:.35rem;left:.35rem;}
  .rb-head{grid-template-columns:minmax(0,1fr);}
  .rb-head .rb-cap{justify-self:start;text-align:left;}
  .rb-marks{grid-template-columns:minmax(0,1fr);}
  .rb-mark{min-height:0;}
  .rb-seg{position:relative;top:auto;right:auto;margin:0 0 .6rem;}
  .rb-ro{grid-template-columns:repeat(2,minmax(0,1fr));}
  .rb-ro > div:nth-child(3){padding-left:0;border-left:0;}
  .rb-ro > div:nth-child(n+3){border-top:1px solid var(--line);margin-top:1rem;}
  .rb-kerio-sub{grid-template-columns:minmax(0,1fr);}
  .rb-kerio-sub .rb-cap{grid-column:1;}
  .rb-stage{grid-template-columns:minmax(0,1fr);}
  .rb{--rb-float:1.6rem;}
  .rb-ph-b{position:relative;left:auto;bottom:auto;width:40%;margin:-16% 0 0 auto;}
  .rb-kd{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:1.8rem;}
  .rb-stage{margin-bottom:0;}
  .rb-kd > .is-wide{grid-column:1 / -1;}
  .rb-wp{min-height:9.5rem;}
  /* the plan: a row the thumb swipes */
  .rb-hz-vp{margin:0 calc(var(--gutter) * -1);overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain;}
  .rb-hz-vp::-webkit-scrollbar{display:none;}
  .rb-hz-tr{flex-wrap:nowrap;width:max-content;padding:0 var(--gutter);}
  .rb-phase,.rb-phase.is-3,.rb-phase.is-w{flex:none;width:auto;}
  .rb-wps{grid-auto-columns:min(78vw,17rem);}
  .rb-phase.is-w .rb-wps{grid-auto-columns:min(86vw,22rem);}
  .rb-wp{scroll-snap-align:start;scroll-margin-left:var(--gutter);}
  .rb-hz-prog{display:block;position:relative;height:1px;margin:1.4rem 0 0;background:var(--line);}
  .rb-hz-prog i{position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--p,.2));transform-origin:0 50%;}
  .rb-aud{grid-template-columns:repeat(2,minmax(0,1fr));}
  .rb-aud > div:nth-child(3){padding-left:0;border-left:0;}
  .rb-aud > div:nth-child(n+3){border-top:1px solid var(--line);}
  .rb-close{grid-template-columns:auto minmax(0,1fr);}
  .rb-cta{flex-direction:column;align-items:stretch;}
  .rb-btn{justify-content:space-between;}
}
@media (max-width:560px){
  .rb-in,.rb-hero-in{padding-left:16px;padding-right:16px;}
  .rb{--gutter:16px;}
  .rb-tick span{font-size:calc(var(--fs-display) * 1.15);}
  .rb-pair .v{font-size:calc(var(--fs-h1) * .95);}
  .rb-ro dd{font-size:var(--fs-h4);}
  .rb-trk.is-wide{display:none;}
  .rb-trk.is-narrow{display:block;}
  .rb-kd .rb-card{padding:.9rem 1rem 1rem;}
  .rb-kd dd{font-size:var(--fs-body);}
  .rb-tiers{grid-template-columns:minmax(0,1fr);}
  .rb-close{grid-template-columns:minmax(0,1fr);}
  .rb-close img{width:4.5rem;}
}
@media (pointer:coarse){
  .rb-a{display:inline-block;padding:13px 0;margin:-13px 0;background-position:0 calc(100% - 13px);}
}
""".replace("__GRAIN__", GRAIN).replace("__KG__", KG)


ARROW = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4"/></svg>')
EXT = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" '
       'style="width:.7em;height:.7em;margin-left:.25em;vertical-align:.05em"><path d="M5 3h8v8M13 3L3 13"/></svg>')


def main_html():
    t100r, t100b, t200b = hm(100, REC100), hm(100, BEST), hm(200, BEST)
    up_news = "https://www.up-paragliders.com/news/almost-200km-with-an-average-of-36kph"
    fai_list = "https://www.fai.org/page/civl-records"
    fai_code = "https://www.fai.org/sites/default/files/civl/documents/sporting_code_s7_d_-_records_and_badges_2025.pdf"
    mail = "mailto:aninder@paraglidingatlas.com?subject=Partnering%20on%20the%20speed%20record%20attempt"
    ext = lambda href, text: '<a class="rb-a" href="%s" target="_blank" rel="noopener">%s%s</a>' % (href, text, EXT)
    return """<main id="v4-main" class="rb">
<script>document.documentElement.classList.add('rb-js')</script>

<header class="rb-hero rb-grain">
  <div class="rb-hero-in">
    <div class="rb-hero-txt">
      <span class="rb-kick">FAI World Record Attempt &middot; Kenya 2027</span>
      """ + kin("Against|The Clock", "h1", cls="rb-h1") + """
      <p class="rb-lede">Speed over 100 km and 200 km, out and return.</p>
    </div>
    <figure class="rb-dial" style="--a:""" + "%.1fdeg" % d_ang(BEST) + """;--f:""" + str(BEST) + """">
      <div class="rb-port"><picture><source srcset=\"""" + KG + """kenya-hero.webp" type="image/webp"><img src=\"""" + KG + """kenya-hero.jpg" width="1400" height="788" alt="Paragliding in Kenya" fetchpriority="high"></picture></div>
      """ + dial_svg() + """
    </figure>
    <dl class="rb-pair">
      <div><dt class="rb-lab">To beat, 100 km</dt><dd><span class="v rb-num"><b class="rb-ct" data-to="35.94" data-dec="2">35.94</b></span><small>km/h</small></dd><dd class="s">""" + TBC + """</dd></div>
      <div class="is-best"><dt class="rb-lab">My best, about</dt><dd><span class="v rb-num"><b class="rb-ct" data-to="36">36</b></span><small>km/h</small></dd><dd class="s">Over 198.86 km</dd></div>
    </dl>
  </div>
</header>

<nav class="rb-bar" aria-label="Chapters">
  <ol>
    <li><a href="#record">Record<i aria-hidden="true"></i></a></li>
    <li><a href="#course">Course<i aria-hidden="true"></i></a></li>
    <li><a href="#kerio">Kerio<i aria-hidden="true"></i></a></li>
    <li><a href="#plan">Plan<i aria-hidden="true"></i></a></li>
    <li><a href="#partner">Partner<i aria-hidden="true"></i></a></li>
  </ol>
</nav>

<div class="rb-tick" aria-hidden="true"><div class="rb-tick-tr"><span>100 km</span><i></i><span class="is-on">200 km</span><i></i><span>Kerio Valley</span><i></i><span>2027</span><i></i></div></div>

<section class="rb-ch" id="record" aria-labelledby="rb-h-rec" data-ch>
  <div class="rb-in">
    <div class="rb-head">
      <span class="rb-lab" aria-hidden="true"></span>
      """ + kin("Two Marks|To Beat", "h2", "rb-h-rec", "rb-h2") + """
      <p class="rb-cap">FAI CIVL, class O-3. """ + ext(fai_list, "Records") + """</p>
    </div>
    <div class="rb-marks">
      <article class="rb-card rb-mark rb-up" style="--d:0" aria-label="The 100 km mark">
        <span class="rb-lab">100 km out and return</span>
        <p class="big rb-num"><b class="rb-ct" data-to="35.94" data-dec="2">35.94</b><small>km/h</small></p>
        <p class="ft">Michel Macquet (FRA), 23 Jan 2025<br>Status """ + TBC + """</p>
      </article>
      <article class="rb-card rb-mark rb-up" style="--d:1" aria-label="The 200 km mark">
        <span class="rb-lab">200 km out and return</span>
        <p class="big">""" + TBD + """</p>
      </article>
      <article class="rb-card rb-mark is-lit rb-up" style="--d:2" aria-label="My best flight">
        <span class="rb-lab">My best, not a record course</span>
        <p class="big rb-num"><b class="rb-ct" data-to="198.86" data-dec="2">198.86</b><small>km</small><span class="sub">at about 36 km/h</span></p>
        <p class="ft">Kenya, 6 Feb 2025, UP Trango X (EN C)<br>""" + ext(up_news, "Source") + """</p>
      </article>
    </div>
  </div>
</section>

<section class="rb-ch rb-course" id="course" aria-labelledby="rb-h-course" data-ch>
  <div class="rb-pin">
    <div class="rb-in">
      <div class="rb-head">
        <span class="rb-lab" aria-hidden="true"></span>
        """ + kin("To The Turnpoint|And Back", "h2", "rb-h-course", "rb-h2") + """
        <p class="rb-cap">Speed is distance over time.</p>
      </div>
      <div class="rb-card rb-mfd" data-cur>
        <fieldset class="rb-seg"><legend>Course length</legend>
          <input type="radio" name="rbk" id="rbk100" value="100" checked><label for="rbk100">100 km</label>
          <input type="radio" name="rbk" id="rbk200" value="200"><label for="rbk200">200 km</label>
        </fieldset>
        """ + course_svg("wide") + course_svg("narrow") + """
        <dl class="rb-ro">
          <div><dt class="rb-lab">Distance</dt><dd><span id="rbDist"><span class="v100">100</span><span class="v200">200</span></span><small>km</small></dd></div>
          <div class="is-lit"><dt class="rb-lab">At 36 km/h</dt><dd id="rbClock"><span class="v100">""" + t100b + """</span><span class="v200">""" + t200b + """</span></dd></div>
          <div><dt class="rb-lab">At the mark</dt><dd><span class="v100">""" + t100r + """</span><span class="v200">""" + TBD + """</span></dd></div>
          <div><dt class="rb-lab">Leg</dt><dd id="rbLeg">Finish</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="rb-ch rb-kerio rb-grain" id="kerio" aria-labelledby="rb-h-kerio" data-ch>
  <div class="rb-in">
    <div class="rb-head"><span class="rb-lab rb-num">0.72&deg;N &nbsp;35.65&deg;E</span></div>
    <div class="rb-kt-mask"><h2 class="rb-kt" id="rb-h-kerio">Kerio<br>Valley</h2></div>
    <div class="rb-kerio-sub"><p class="rb-cap">Base of my <a class="rb-a" href="destinations/kenya.html">Kenya expeditions</a>, where the world speed records are chased.</p></div>
    <div class="rb-stage">
      <div class="rb-phs">
        <figure class="rb-ph rb-ph-a rb-clip"><picture><source srcset=\"""" + A + """destinations/kenya/hero/kerio-valley.webp" type="image/webp"><img src=\"""" + A + """destinations/kenya/hero/kerio-valley.jpg" width="1152" height="768" alt="Paragliding at Kerio Valley, Kenya" loading="lazy" decoding="async"></picture></figure>
        <figure class="rb-ph rb-ph-b"><picture><source srcset=\"""" + KG + """kenya-high.webp" type="image/webp"><img src=\"""" + KG + """kenya-high.jpg" width="1400" height="933" alt="Paragliding in Kenya" loading="lazy" decoding="async"></picture></figure>
      </div>
      <dl class="rb-kd">
        <div class="rb-card rb-up is-wide" style="--d:0"><dt class="rb-lab">Season</dt><dd>December to March</dd></div>
        <div class="rb-card rb-up is-wide" style="--d:1"><dt class="rb-lab">Thermals, m/s</dt><dd>4 to 6 at midday peaks<small>Rare surges 6 to 7</small></dd>""" + vario_svg() + """</div>
        <div class="rb-card rb-up is-wide" style="--d:2"><dt class="rb-lab">Flights</dt><dd>2 to 7 hours over the Rift Valley</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="rb-ch rb-plan" id="plan" aria-labelledby="rb-h-plan" data-ch>
  <div class="rb-pin">
    <div class="rb-in">
      <div class="rb-head">
        <span class="rb-lab" aria-hidden="true"></span>
        """ + kin("From Now|To The Window", "h2", "rb-h-plan", "rb-h2") + """
      </div>
      <div class="rb-hz-vp">
        <div class="rb-hz-tr">
          <div class="rb-phase is-3">
            <p class="rb-phase-h"><span class="rb-lab">Before</span>Build-up episodes, newsletter</p>
            <ol class="rb-wps">
              <li class="rb-card rb-wp">""" + ico("prep") + """<h3>Preparation</h3><p>""" + TBD + """</p></li>
              <li class="rb-card rb-wp">""" + ico("wing") + """<h3>Wing And Instruments</h3><p>""" + TBD + """</p></li>
              <li class="rb-card rb-wp">""" + ico("team") + """<h3>Team And FAI Observer</h3><p>""" + TBD + """</p></li>
            </ol>
          </div>
          <div class="rb-phase is-w">
            <p class="rb-phase-h"><span class="rb-lab">During</span>Live tracking, daily updates</p>
            <ol class="rb-wps">
              <li class="rb-card rb-wp is-lit"><span class="rb-lab">18 Jan to 12 Feb 2027</span><h3>The Attempt Window</h3>""" + days() + """
                <div class="rb-dayl"><span>Expedition, 18 to 29 Jan</span><span>Expedition, 1 to 12 Feb</span></div></li>
            </ol>
          </div>
          <div class="rb-phase">
            <p class="rb-phase-h"><span class="rb-lab">After</span>Film, debrief, flight data</p>
            <ol class="rb-wps">
              <li class="rb-card rb-wp">""" + ico("claim") + """<h3>The Claim</h3><p>""" + ext(fai_code, "FAI Sporting Code 7D") + """</p></li>
            </ol>
          </div>
        </div>
      </div>
      <div class="rb-hz-prog" aria-hidden="true"><i></i></div>
    </div>
  </div>
</section>

<section class="rb-ch rb-partner" id="partner" aria-labelledby="rb-h-partner" data-ch>
  <div class="rb-in">
    <div class="rb-head">
      <span class="rb-lab" aria-hidden="true"></span>
      """ + kin("Put Your Name|On The Attempt", "h2", "rb-h-partner", "rb-h2") + """
      <p class="rb-cap">Podcast, YouTube, newsletter about four times a month.</p>
    </div>
    <dl class="rb-aud">
      <div><dd class="rb-num"><b class="rb-ct" data-to="100000" data-sep="1" data-suf="+">100,000+</b></dd><dt class="rb-lab">Podcast streams</dt></div>
      <div><dd class="rb-num"><b class="rb-ct" data-to="130" data-suf="+">130+</b></dd><dt class="rb-lab">Countries</dt></div>
      <div><dd class="rb-num"><b class="rb-ct" data-to="80">80</b></dd><dt class="rb-lab">Interviews</dt></div>
      <div><dd class="rb-num"><b class="rb-ct" data-to="10" data-suf="+">10+</b></dd><dt class="rb-lab">Years flying</dt></div>
    </dl>
    <div class="rb-tiers">
      <article class="rb-card rb-tier is-lit rb-up" style="--d:0" aria-labelledby="rb-t1">
        <span class="rb-chip">One only</span>
        <h3 id="rb-t1">Title Partner</h3>
        <ul><li>Name in the attempt&rsquo;s title</li><li>Mark on kit and camera</li><li>Build-up and debrief segments</li><li>First film credit</li><li>Logo on live tracking</li></ul>
      </article>
      <article class="rb-card rb-tier rb-up" style="--d:1" aria-labelledby="rb-t2">
        <h3 id="rb-t2">Equipment Partner</h3>
        <ul><li>Used and shown in the air</li><li>Honest, disclosed review</li><li>On my expeditions</li><li>Credits</li></ul>
      </article>
      <article class="rb-card rb-tier rb-up" style="--d:2" aria-labelledby="rb-t3">
        <h3 id="rb-t3">Supporter</h3>
        <ul><li>Name on this page</li><li>Newsletter and debrief thanks</li><li>Film credit</li></ul>
      </article>
    </div>
    <div class="rb-close rb-grain">
      <picture><source srcset=\"""" + A + """images/partners-aninder.webp" type="image/webp"><img src=\"""" + A + """images/partners-aninder.jpg" width="720" height="900" alt="Aninder Singh" loading="lazy" decoding="async"></picture>
      <div class="rb-who"><b>Aninder Singh</b><p>Media kit and prices on request. Every sponsorship <a class="rb-a" href="safety-and-disclosure.html">clearly marked as sponsored</a>.</p></div>
      <div class="rb-cta">
        <a class="rb-btn is-main rb-mag" href=\"""" + mail + """\">Partner On The Attempt""" + ARROW + """</a>
        <a class="rb-btn rb-mag" href="partners.html#pwForm">Other Ways To Partner""" + ARROW + """</a>
      </div>
    </div>
  </div>
</section>

</main>"""


SCRIPT = r"""<script>
/* The record attempt, design B (tools/v4_record_b.py). Everything here answers
   the visitor: a scroll, a pointer, a tap. Nothing runs while the page is still.
   Reduced motion: the finished states, as in the markup. */
(function () {
  'use strict';
  var d = document, w = window, root = d.documentElement;
  var mq = function (q) { return w.matchMedia && w.matchMedia(q).matches; };
  var still = mq('(prefers-reduced-motion: reduce)');
  var fine = mq('(hover: hover) and (pointer: fine)');
  var IO = 'IntersectionObserver' in w;
  var BEST = __BEST__, D_START = -135, D_SWEEP = 270, D_MAX = 50;
  root.classList.add('rb-live');

  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(t) { return 1 - Math.pow(1 - t, 3); }
  function hm(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + ' h ' + ('0' + (m % 60)).slice(-2) + ' min'; }
  function fmt(v, el) {
    var dec = +(el.getAttribute('data-dec') || 0), s = v.toFixed(dec);
    if (el.hasAttribute('data-sep')) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return s + (el.getAttribute('data-suf') || '');
  }

  /* 1. one-shot arrivals: headings rise, cards come up, numbers count, the dial sweeps */
  var counts = [].slice.call(d.querySelectorAll('.rb-ct'));
  var dial = d.querySelector('.rb-dial');
  function count(el, dur) {
    var to = +el.getAttribute('data-to'), t0 = performance.now();
    (function step(t) {
      var p = clamp((t - t0) / dur, 0, 1);
      el.textContent = fmt(to * ease(p), el);
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }
  function sweep() {
    var t0 = performance.now(), dur = 1900;
    (function step(t) {
      var p = clamp((t - t0) / dur, 0, 1), v = BEST * ease(p);
      dial.style.setProperty('--a', (D_START + v / D_MAX * D_SWEEP).toFixed(2) + 'deg');
      dial.style.setProperty('--f', v.toFixed(2));
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }
  function fit() {
    counts.forEach(function (el) {
      var t = el.textContent; el.style.minWidth = '';
      el.textContent = fmt(+el.getAttribute('data-to'), el);
      el.style.minWidth = el.getBoundingClientRect().width.toFixed(1) + 'px';
      el.textContent = t;
    });
  }
  if (still || !IO) {
    d.querySelectorAll('.rb-k,.rb-up,.rb-clip,.rb-dial').forEach(function (e) { e.classList.add('is-in'); });
  } else {
    fit(); if (d.fonts && d.fonts.ready) d.fonts.ready.then(fit);
    counts.forEach(function (el) { el.textContent = fmt(0, el); });
    if (dial) { dial.style.setProperty('--a', D_START + 'deg'); dial.style.setProperty('--f', '0'); }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; io.unobserve(el);
        if (el.classList.contains('rb-ct')) { count(el, el.closest('.rb-dial, .rb-hero') ? 1900 : 1500); return; }
        el.classList.add('is-in');
        if (el === dial) sweep();
      });
    }, { threshold: 0.35, rootMargin: '0px 0px -6% 0px' });
    d.querySelectorAll('.rb-k,.rb-up,.rb-clip,.rb-dial,.rb-ct').forEach(function (e) { io.observe(e); });
  }

  /* 2. the course: flown kilometre by kilometre with the scroll */
  var course = d.getElementById('course'), plan = d.getElementById('plan');
  var trks = course ? [].slice.call(course.querySelectorAll('.rb-trk')) : [];
  var elDist = d.getElementById('rbDist'), elClock = d.getElementById('rbClock'), elLeg = d.getElementById('rbLeg');
  var K = 100, lastP = 1;
  trks.forEach(function (s) {
    var g = function (k) { return +s.getAttribute('data-' + k); };
    s._g = { x0: g('x0'), x1: g('x1'), yo: g('yo'), yb: g('yb'), gs: g('gs') };
    s._f = {}; [].forEach.call(s.querySelectorAll('.fl'), function (p) { s._f[p.getAttribute('data-seg')] = p; });
    s._gl = s.querySelector('.gl');
  });
  function fly(p) {
    lastP = p;
    var km = 0, leg = 'Out';
    trks.forEach(function (s) {
      if (!s.getBoundingClientRect().width) return;
      var G = s._g, L = G.x1 - G.x0, r = (G.yb - G.yo) / 2, T = Math.PI * r, tot = 2 * L + T, at = p * tot, x, y, rot;
      var fo = clamp(at / L, 0, 1), ft = clamp((at - L) / T, 0, 1), fb = clamp((at - L - T) / L, 0, 1);
      s._f.o.style.strokeDashoffset = 1 - fo; s._f.t.style.strokeDashoffset = 1 - ft; s._f.b.style.strokeDashoffset = 1 - fb;
      if (at <= L) { x = G.x0 + fo * L; y = G.yo; rot = 0; km = fo * K / 2; leg = 'Out'; }
      else if (at <= L + T) { var th = -Math.PI / 2 + ft * Math.PI; x = G.x1 + r * Math.cos(th); y = G.yo + r + r * Math.sin(th); rot = ft * 180; km = K / 2; leg = 'Turnpoint'; }
      else { x = G.x1 - fb * L; y = G.yb; rot = 180; km = K / 2 + fb * K / 2; leg = fb >= 1 ? 'Finish' : 'Home'; }
      s._gl.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') rotate(' + rot.toFixed(1) + ') scale(' + G.gs + ')');
    });
    if (elDist) elDist.textContent = Math.round(km);
    if (elClock) elClock.textContent = hm(km / BEST);
    if (elLeg) elLeg.textContent = leg;
  }
  d.querySelectorAll('input[name="rbk"]').forEach(function (r) {
    r.addEventListener('change', function () { K = +r.value; fly(lastP); });
  });
  var k2 = d.getElementById('rbk200'); if (k2 && k2.checked) K = 200;

  /* 3. pinned on wide screens: the course flies while it holds, the plan slides sideways */
  var wide = w.matchMedia('(min-width: 821px)');
  var hz = plan && plan.querySelector('.rb-hz-tr'), hzVp = plan && plan.querySelector('.rb-hz-vp'), hzBar = plan && plan.querySelector('.rb-hz-prog i');
  var hzDist = 0, pinned = false, barH = 56;
  function layout() {
    pinned = !still && wide.matches;
    if (course) course.classList.toggle('is-pin', pinned);
    if (plan) plan.classList.toggle('is-pin', pinned);
    barH = (d.querySelector('.rb-bar') || {}).offsetHeight || 56;
    if (plan) {
      if (pinned) { hz.style.transform = ''; hzDist = Math.max(0, hz.scrollWidth - hzVp.clientWidth); plan.style.height = (innerHeight + hzDist) + 'px'; }
      else { plan.style.height = ''; hz.style.transform = ''; }
    }
    frame();
  }
  if (still) fly(1);

  /* 4. the chapter bar: which chapter is open, and how far through each one */
  var chs = [].slice.call(d.querySelectorAll('[data-ch]'));
  var tabs = chs.map(function (c) { return d.querySelector('.rb-bar a[href="#' + c.id + '"]'); });
  var tick = d.querySelector('.rb-tick-tr'), tickSel = !(w.CSS && CSS.supports && CSS.supports('animation-timeline: view()'));
  var queued = false;
  function frame() {
    queued = false;
    var vh = innerHeight, line = vh * 0.38, cur = -1, i, r;
    for (i = 0; i < chs.length; i++) {
      r = chs[i].getBoundingClientRect();
      var pc = clamp((line - r.top) / r.height, 0, 1);
      if (r.top <= line && r.bottom > line) cur = i;
      if (tabs[i]) tabs[i].style.setProperty('--p', pc.toFixed(3));
    }
    tabs.forEach(function (t, j) { if (!t) return; if (j === cur) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
    if (!still && course) {
      r = course.getBoundingClientRect();
      var p;
      if (pinned) p = clamp((barH - r.top) / Math.max(1, r.height - (vh - barH)), 0, 1);
      else { var box = course.querySelector('.rb-mfd').getBoundingClientRect(); p = clamp((vh * 0.88 - box.top) / (vh * 0.5 + box.height * 0.5), 0, 1); }
      if (Math.abs(p - lastP) > 0.0005 || p === 0 || p === 1) fly(p);
    }
    if (pinned && plan) {
      r = plan.getBoundingClientRect();
      var q = clamp((barH - r.top) / Math.max(1, r.height - (vh - barH)), 0, 1);
      hz.style.transform = 'translate3d(' + (-q * hzDist).toFixed(1) + 'px,0,0)';
      if (hzBar) hzBar.style.setProperty('--p', q.toFixed(3));
    }
    if (tickSel && tick && !still) {
      r = tick.parentNode.getBoundingClientRect();
      var tp = clamp((vh - r.top) / (vh + r.height), 0, 1);
      tick.style.transform = 'translate3d(' + (-tp * 0.38 * tick.scrollWidth).toFixed(1) + 'px,0,0)';
    }
  }
  w.addEventListener('scroll', function () { if (!queued) { queued = true; requestAnimationFrame(frame); } }, { passive: true });
  w.addEventListener('resize', function () { requestAnimationFrame(layout); }, { passive: true });
  if (wide.addEventListener) wide.addEventListener('change', layout);
  w.addEventListener('load', layout);
  layout();
  if (!still) fly(0); frame();

  /* the plan on a phone: the bar under the row follows the thumb */
  if (hzVp) hzVp.addEventListener('scroll', function () {
    if (pinned) return;
    var m = hzVp.scrollWidth - hzVp.clientWidth;
    if (hzBar) hzBar.style.setProperty('--p', (0.2 + 0.8 * (m > 0 ? hzVp.scrollLeft / m : 1)).toFixed(3));
  }, { passive: true });

  /* 5. a mouse gets a ring that follows it and buttons that lean toward it; touch gets neither */
  if (fine && !still) {
    var cur = d.createElement('div'); cur.className = 'rb-cur'; cur.setAttribute('aria-hidden', 'true'); cur.innerHTML = '<i></i>';
    d.body.appendChild(cur);
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, on = false;
    var loop = function () {
      cx += (tx - cx) * 0.24; cy += (ty - cy) * 0.24;
      cur.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
      raf = (Math.abs(tx - cx) + Math.abs(ty - cy) > 0.2) ? requestAnimationFrame(loop) : 0;
    };
    d.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX; ty = e.clientY;
      if (!on) { on = true; cx = tx; cy = ty; cur.classList.add('is-on'); }
      var t = e.target.closest ? e.target : null;
      var hit = t && t.closest('a,button,label,input');
      cur.classList.toggle('is-big', !!hit);
      cur.classList.toggle('is-trk', !hit && !!(t && t.closest('[data-cur]')));
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: true });
    d.documentElement.addEventListener('mouseleave', function () { on = false; cur.classList.remove('is-on'); });
    d.querySelectorAll('.rb-mag').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        if (e.pointerType !== 'mouse') return;
        var r = b.getBoundingClientRect();
        var mx = clamp((e.clientX - r.left - r.width / 2) * 0.16, -9, 9), my = clamp((e.clientY - r.top - r.height / 2) * 0.3, -6, 6);
        b.style.transform = 'translate(' + mx.toFixed(1) + 'px,' + my.toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
  }
})();
</script>""".replace("__BEST__", str(BEST))


def ld():
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":"%s#webpage","name":"%s","url":"%s","description":"%s",'
            '"isPartOf":{"@id":"https://paraglidingatlas.com/#website"},'
            '"publisher":{"@id":"https://paraglidingatlas.com/#organization"},"inLanguage":"en"}\n</script>'
            % (URL, TITLE, URL, DESC))


def main():
    s = open(SHELL, encoding="utf-8").read()
    head, rest = s.split('<main id="v4-main">', 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % TITLE, head, 1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, head, 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', r"\g<1>" + URL, head, 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + TITLE, head, 1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, head, 1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', r"\g<1>" + OG_IMG, head, 1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + URL, head, 1)
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "WebPage".*?</script>',
                  lambda m: ld(), head, 1, flags=re.S)
    head = re.sub(r"<!--v4u-css-->.*?<!--/v4u-css-->", "", head, 1, flags=re.S)
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + CSS + "</style>\n", head, 1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    if "rb-hero" not in head or "Partner With Me" in head.split("<body")[0]:
        raise SystemExit("v4_record_b: the partners shell has changed; check the head")
    page = head + main_html() + tail.replace("</body>", SCRIPT + "\n</body>", 1)
    if "\u2014" in page:
        raise SystemExit("v4_record_b: an em dash got into the page")
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_record_b: %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
