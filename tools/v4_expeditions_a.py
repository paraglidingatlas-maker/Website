#!/usr/bin/env python3
"""
The expeditions page, option A, "Two skies" (owner, 19 Oct 2026: "expeditions
standalone tab needs to be a redesigned page, it's just an off copy of
leftover material at homepage, I want it to be a bit different").

    prototypes/v4/expeditions-a.html   (canonical /expeditions.html)

For pilots choosing a trip, and plainly not the home page's #destinations
section: no card grid, no departures table, no call band (the home page keeps
those). Photography-led, editorial and calm:
  - the opening is the page's one signature moment: two photographs, the
    snow above Bir and the gold of the Rift, meeting in a long soft dissolve
    under the title. Each half is the way into its chapter, named with its
    trip's own name (Big Mountain Flying, Explore the Cradle). Under a fine
    pointer (or a key) the sky you point at leans open, slowly, and the other
    gives way. Only the masks move, so leaning never shifts the layout;
  - the chooser is the year ahead drawn to scale, October 2026 to November
    2027: each departure sits on the line on its real days, the planned two
    on their months, so it reads by place and by month at once. Each place
    jumps to its chapter; it stays at the top as the page goes by and marks
    the chapter you are in. On phones the places and the month initials stay,
    the dates move into the chapters;
  - India and Kenya are full-bleed chapters: one photograph dissolving into
    the page, the place in large type (the photograph's own name level with
    its foot, or under it when the two cannot share a line), one line on what
    the flying is like (each trip page's own words), and four quiet facts
    (when, how long, how many, from what price) with the status, then the
    air in three lines;
  - Kazakhstan and Peru follow as quieter "planned" chapters, type only, with
    only what the home page says and "Register interest";
  - a closing line points to the full trip pages and the call.

Facts, each from the site (nothing here is new):
  - the home page's #destinations section (prototypes/v4/index.html): the
    departures (21 to 30 Oct 2026, 3 to 12 Nov 2026; 18 to 29 Jan 2027, 1 to 12
    Feb 2027), lengths (10 days, 12 days), group sizes (6 places, 8 places,
    planned "Small group"), prices with currency (India £1,100, Kenya
    US$2,100, Kazakhstan €2,100, Peru €1,850), status ("Guaranteed to run",
    "Booking open", "Register interest"), places ("Bir Billing, Himalaya",
    "Kerio Valley, Rift Valley", "The steppe", "Lima and the Andes"), the
    planned months (June 2027, November 2027), "Planned", and "Small groups,
    fixed dates. Prices are per pilot."
  - destinations/india.html: the trip's name, "Big Mountain Flying"; the
    flying line (its overview sequence: "launch from the meadow at Billing,
    climb the knobs of the Dhauladhar and run west towards Dharamshala, then
    turn for Bir with the light going"); season October to November; front
    range cloudbase "3 to 3.6 km on the front range"; pilot rating "IPPI 2 or
    equivalent"; the routes, FAQ and "What This Trip Is Actually Like".
  - destinations/kenya.html: the trip's name, "Explore the Cradle"; the flying
    line ("launch from the lush green takeoffs in Kerio, chase thermals over
    the flatlands, and set your sights on the distant shores of Lake
    Naivasha"); season December to March; thermals "4 to 6 m/s at the midday
    peaks"; pilot rating "IPPI 2 or equivalent".
  - "Hold a place" goes to the enquiry form with the trip chosen, as the trip
    pages do (enquire.html?trip=...); "Register interest" as the home page.
  - the call: the site's calendar link and the home page's "free 30-minute".
Nothing on the page is unknown, so nothing shows "[to supply]"; a fact added
later without a source should use the site's <span class="v2-tbd">.

Photographs: only the trips' own (assets/destinations/...), each alt the one
its trip page gives it. The opening: India snowline and Kenya equator, no
place named on them (each half is named by its trip, not its photograph).
The chapters: India front-range, named "The front range" (the India overview
pairs it with its step "02 The front range"), and Kenya longonot, named
"Mount Longonot" (the Kenya hero's own label).
Sizes checked with PIL: snowline 1800x1200, equator 1152x768, front-range
1400x933, longonot 1153x768. No video (owner, 8 Oct: footage only on trip
pages and the home page), no stock, no pilot presented as the owner. Peru and
Kazakhstan have no trip photographs yet, so their chapters are type only.

Restraint (the record page's lessons): few words (checked here, under 400 in
<main>), the photographs and the type are the graphics, long eased masks
instead of seams, one signature moment. Motion only answers the visitor
(pointer, key, scroll, tap): nothing runs on a timer or loops. Reduced
motion: nothing moves. JavaScript off: everything is there, the chooser still
stays at the top and jumps; only the "you are here" mark needs the script.
Small grey words use a mix of the two grey tokens that holds 4.5:1 on the
page (--gray alone is 3.8:1 on --bg), and no small word sits on a photograph
that has not yet dissolved: the kicker runs along the dark top of the
opening, the photographs' names sit at the foot of the place names.

The page takes the v4 shell (head, menu, footer) from partners.html and is
prototype-only (noindex) until the owner approves it; the menu is not
touched here.

    python3 tools/v4_expeditions_a.py
"""
import calendar
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "expeditions-a.html")

TITLE = "Expeditions"
DESC = ("Small-group paragliding expeditions with Paragliding Atlas: Bir Billing in the Indian "
        "Himalaya and Kerio Valley in Kenya, with Kazakhstan and Peru planned for 2027. "
        "Dates, lengths, group sizes and prices per pilot.")
URL = "https://paraglidingatlas.com/expeditions.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/india/hero/snowline.jpg"
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
MODIFIED = "2026-10-19"
MAX_WORDS = 400

A = "../../assets/destinations/"
# key: (path without extension, width, height, alt from the trip page, the trip page's label for it,
#       object-position wide, object-position at 900px and under)
IMG = {
    "snowline": (A + "india/hero/snowline", 1800, 1200,
                 "A pilot on a red wing flying over snow-covered mountains", "Above the snowline",
                 "100% 55%", "66% 55%"),
    "equator": (A + "kenya/hero/equator", 1152, 768,
                "A yellow paraglider on a long glide over arid rock outcrops in low golden light", "The Equator",
                "58% 45%", "62% 45%"),
    "front-range": (A + "india/gallery/front-range", 1400, 933,
                    "A pilot flying along the forested front range, snow peaks behind", "The front range",
                    "50% 40%", "12% 50%"),
    "longonot": (A + "kenya/hero/longonot", 1153, 768,
                 "A pink and yellow paraglider turning above the deep green crater of Mount Longonot",
                 "Mount Longonot", "50% 18%", "24% 40%"),
}

# the two expeditions that run, in time order; every value is quoted from the site (see the docstring).
# "deps" are the departures as (year, month, first day, last day), for the chooser's year line.
TRIPS = [
    {
        "id": "india", "place": "India", "trip": "Big Mountain Flying", "where": "Bir Billing, Himalaya",
        "pic": "front-range", "side": "l", "half": "snowline",
        "line": ("Launch from the meadow at Billing, climb the knobs of the Dhauladhar and run west "
                 "towards Dharamshala, then turn for Bir with the light going."),
        "when": ["21 to 30 Oct 2026", "3 to 12 Nov 2026"], "pick": "Oct, Nov 2026",
        "deps": [(2026, 10, 21, 30), (2026, 11, 3, 12)],
        "length": "10 days", "group": "6 places", "from": "&pound;1,100",
        "status": "Guaranteed to run",
        "air": [("Season", "October to November"), ("Cloudbase", "3 to 3.6 km on the front range"),
                ("Rating", "IPPI 2 or equivalent")],
        "hold": "enquire.html?trip=india", "page": "destinations/india.html",
    },
    {
        "id": "kenya", "place": "Kenya", "trip": "Explore the Cradle", "where": "Kerio Valley, Rift Valley",
        "pic": "longonot", "side": "r", "half": "equator",
        "line": ("Launch from the lush green takeoffs in Kerio, chase thermals over the flatlands, and "
                 "set your sights on the distant shores of Lake Naivasha."),
        "when": ["18 to 29 Jan 2027", "1 to 12 Feb 2027"], "pick": "Jan, Feb 2027",
        "deps": [(2027, 1, 18, 29), (2027, 2, 1, 12)],
        "length": "12 days", "group": "8 places", "from": "US$2,100",
        "status": "Booking open",
        "air": [("Season", "December to March"), ("Thermals", "4 to 6 m/s at the midday peaks"),
                ("Rating", "IPPI 2 or equivalent")],
        "hold": "enquire.html?trip=kenya", "page": "destinations/kenya.html",
    },
]

# the planned two, in time order, with only what the home page says (a month, no days)
PLANNED = [
    {"id": "kazakhstan", "place": "Kazakhstan", "where": "The steppe", "when": "June 2027", "pick": "Jun 2027",
     "deps": [(2027, 6, 1, 30)],
     "length": "10 days", "group": "Small group", "from": "&euro;2,100", "go": "enquire.html?trip=kazakhstan"},
    {"id": "peru", "place": "Peru", "where": "Lima and the Andes", "when": "November 2027", "pick": "Nov 2027",
     "deps": [(2027, 11, 1, 30)],
     "length": "14 days", "group": "Small group", "from": "&euro;1,850", "go": "enquire.html?trip=peru"},
]

# the chooser's year: October 2026 to November 2027, fourteen months
Y0, M0, NMONTHS = 2026, 10, 14

ARROW = ('<svg class="ex-arr" viewBox="0 0 16 10" aria-hidden="true" focusable="false">'
         '<path d="M0 5h14.5M10.5 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')
DOWN = ('<svg class="ex-dn" viewBox="0 0 10 14" aria-hidden="true" focusable="false">'
        '<path d="M5 0v12.5M1 8.5l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')
EXT = ('<svg class="ex-ext" viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
       '<path d="M3.5 2.5h6v6M9.5 2.5l-7 7" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>')


# ---------- the long eased masks ----------
# a photograph never meets the page at an edge: its alpha runs from nothing to whole along a
# smootherstep, over a long distance, written out as many stops of the page colour mixed with transparent
# (a mask reads only the alpha, so the colour is the token's and never matters)

def smoother(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def alpha(a):
    if a <= 0.004:
        return "transparent"
    if a >= 0.996:
        return "var(--bg)"
    return "color-mix(in srgb,var(--bg) %.1f%%,transparent)" % (a * 100)


def pos(p0, p1, t):
    if isinstance(p0, (int, float)) and isinstance(p1, (int, float)):
        return "%.2f%%" % (p0 + (p1 - p0) * t)
    return "calc(%s + (%s - %s) * %.4f)" % (p0, p1, p0, t)


def ramp(p0, p1, a0, a1, n=10):
    return ["%s %s" % (alpha(a0 + (a1 - a0) * smoother(i / n)), pos(p0, p1, i / n)) for i in range(n + 1)]


def vmask(top_in, hold, bottom_out):
    """Down the photograph: in from the page over [0, top_in], whole to hold, out to the page by bottom_out."""
    return "linear-gradient(180deg,%s)" % ",".join(ramp(0, top_in, 0, 1) + ramp(hold, bottom_out, 1, 0))


# the two halves of the opening: both layers span the whole width and cross-fade over a band 2 x --ex-w
# wide centred on the split; leaning moves only the band (a repaint, never a layout shift)
MASK_A = "linear-gradient(90deg,var(--bg) 0%%,%s,transparent 100%%)" % ",".join(
    ramp("(var(--ex-split) - var(--ex-w))", "(var(--ex-split) + var(--ex-w))", 1, 0, 12))
MASK_B = "linear-gradient(90deg,transparent 0%%,%s,var(--bg) 100%%)" % ",".join(
    ramp("(var(--ex-split) - var(--ex-w))", "(var(--ex-split) + var(--ex-w))", 0, 1, 12))
MASK_TOP = vmask(24, 44, 97)
MASK_TOP_S = vmask(34, 50, 97)
SHADE = ",".join(ramp(0, 100, 0.7, 0, 12))
MASK_CH = vmask(20, 46, 100)
MASK_CH_S = vmask(16, 52, 100)


def pic(key, lazy=True, fetch=False):
    base, w, h, alt, cap, xy, xym = IMG[key]
    att = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if fetch else "")
    return ('<picture><source srcset="%s.webp" type="image/webp"><img src="%s.jpg" width="%d" height="%d" '
            'alt="%s" style="--xy:%s;--xym:%s"%s></picture>' % (base, base, w, h, alt, xy, xym, att))


def facts(t, small=False):
    when = "".join("<span>%s</span>" % d for d in (t["when"] if isinstance(t["when"], list) else [t["when"]]))
    return ('<dl class="ex-facts%s">'
            '<div><dt>When</dt><dd>%s</dd></div>'
            '<div><dt>Length</dt><dd>%s</dd></div>'
            '<div><dt>Group</dt><dd>%s</dd></div>'
            '<div><dt>From</dt><dd>%s<small>per pilot</small></dd></div>'
            '</dl>' % (" is-s" if small else "", when, t["length"], t["group"], t["from"]))


# ---------- the opening ----------

def opening():
    a, b = TRIPS
    return """
<header class="ex-top">
  <p class="ex-kick">Expeditions</p>
  <div class="ex-head">
    <h1 class="ex-h1">Two Skies</h1>
    <p class="ex-sub">Small groups, fixed dates. Prices are per pilot.</p>
  </div>
  <div class="ex-two">
    <div class="ex-pic is-a">""" + pic(a["half"], lazy=False, fetch=True) + """</div>
    <div class="ex-pic is-b">""" + pic(b["half"], lazy=False) + """</div>
    <a class="ex-half is-a" href="#""" + a["id"] + """\"><span class="ex-cap"><b>""" + a["place"] + DOWN + """</b> <span>""" + a["trip"] + """</span></span></a>
    <a class="ex-half is-b" href="#""" + b["id"] + """\"><span class="ex-cap"><b>""" + b["place"] + DOWN + """</b> <span>""" + b["trip"] + """</span></span></a>
  </div>
</header>
"""


# ---------- the chooser: the year ahead, to scale ----------

def frac(y, m, day, end=False):
    """Where a day falls on the chooser's line, 0 at 1 October 2026 and 1 at the end of November 2027."""
    i = (y - Y0) * 12 + (m - M0)
    n = calendar.monthrange(y, m)[1]
    return (i + (day if end else day - 1) / n) / NMONTHS


def chooser():
    links, bars = [], []
    for t in TRIPS + PLANNED:
        x0 = frac(*t["deps"][0][:3])
        last = t["deps"][-1]
        x1 = frac(last[0], last[1], last[3], end=True)
        # each place sits over its first departure; the last one is held to the end of the line
        anchor = ("right:%.3f%%" % ((1 - x1) * 100)) if x1 > 0.9 else ("left:%.3f%%" % (x0 * 100))
        links.append('<li style="%s"><a href="#%s"><b>%s</b> <span class="ex-mo">%s</span></a></li>'
                     % (anchor, t["id"], t["place"], t["pick"]))
        for (y, m, d0, d1) in t["deps"]:
            s, e = frac(y, m, d0), frac(y, m, d1, end=True)
            bars.append('<i class="ex-bar%s" data-t="%s" style="left:%.3f%%;width:%.3f%%"></i>'
                        % (" is-plan" if t in PLANNED else "", t["id"], s * 100, (e - s) * 100))
    months = []
    for k in range(NMONTHS):
        y, m = Y0 + (M0 - 1 + k) // 12, (M0 - 1 + k) % 12 + 1
        name = calendar.month_abbr[m]
        months.append('<span%s><b>%s</b><i>%s</i></span>' % (' class="is-y"' if m == 1 else "", name, name[0]))
    return ("""
<nav class="ex-pick" aria-label="Expeditions, by place and month">
  <div class="ex-pick-in">
    <div class="ex-line" aria-hidden="true">""" + "".join(bars) + """</div>
    <div class="ex-months" aria-hidden="true">""" + "".join(months) + """</div>
    <ol class="ex-places">""" + "".join(links) + """</ol>
  </div>
</nav>
""")


# ---------- the two that run ----------

def chapter(t):
    cap = IMG[t["pic"]][4]
    air = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in t["air"])
    return """
<section class="ex-ch is-""" + t["side"] + '" id="' + t["id"] + '" aria-labelledby="' + t["id"] + """-h">
  <div class="ex-ph">""" + pic(t["pic"]) + """</div>
  <div class="ex-body ex-in">
    <p class="ex-where">""" + t["where"] + """</p>
    <div class="ex-name">
      <h2 class="ex-place" id=\"""" + t["id"] + """-h">""" + t["place"] + """</h2>
      <p class="ex-photo"><span class="ex-vh">The photograph: </span><span>""" + cap + """</span></p>
    </div>
    <div class="ex-grid">
      <p class="ex-line-s">""" + t["line"] + """</p>
      <div class="ex-info">
        """ + facts(t) + """
        <p class="ex-status"><i aria-hidden="true"></i>""" + t["status"] + """</p>
      </div>
      <dl class="ex-air">""" + air + """</dl>
      <div class="ex-acts">
        <a class="ex-btn" href=\"""" + t["hold"] + """\">Hold a place<span class="ex-vh"> on the """ + t["place"] + """ expedition</span></a>
        <a class="ex-more" href=\"""" + t["page"] + """\">The full trip<span class="ex-vh"> for """ + t["place"] + """</span>""" + ARROW + """</a>
      </div>
    </div>
  </div>
</section>
"""


# ---------- the planned two ----------

def planned():
    arts = []
    for t in PLANNED:
        arts.append("""
    <article class="ex-plan" id=\"""" + t["id"] + '" aria-labelledby="' + t["id"] + """-h">
      <p class="ex-where">""" + t["where"] + """</p>
      <h3 class="ex-place-s" id=\"""" + t["id"] + """-h">""" + t["place"] + """</h3>
      """ + facts(t, small=True) + """
      <a class="ex-more" href=\"""" + t["go"] + """\">Register interest<span class="ex-vh"> in """ + t["place"] + """</span>""" + ARROW + """</a>
    </article>""")
    return """
<section class="ex-later" aria-labelledby="ex-later-h">
  <div class="ex-in">
    <h2 class="ex-later-h" id="ex-later-h">Planned For 2027</h2>
    <div class="ex-later-grid">""" + "".join(arts) + """
    </div>
  </div>
</section>
"""


def closing():
    return """
<section class="ex-end" aria-labelledby="ex-end-h">
  <div class="ex-in">
    <h2 class="ex-end-h" id="ex-end-h">Not Sure Which Sky?</h2>
    <p>Each trip page has the routes, the questions pilots ask and what the trip is actually like. Or book a free 30-minute call.</p>
    <p class="ex-links">
      <a class="ex-more" href="destinations/india.html">India in full""" + ARROW + """</a>
      <a class="ex-more" href="destinations/kenya.html">Kenya in full""" + ARROW + """</a>
      <a class="ex-more" href=\"""" + CALL + """\" target="_blank" rel="noopener">Book a call""" + EXT + """<span class="ex-vh"> (opens a new tab)</span></a>
    </p>
  </div>
</section>
"""


def main_html():
    return ('<main id="v4-main" class="ex">\n' + opening() + chooser() + "".join(chapter(t) for t in TRIPS)
            + planned() + closing() + "</main>")


CSS = r"""
/* ===== Expeditions, option A: two skies (tools/v4_expeditions_a.py) ===== */
@property --ex-split{syntax:"<percentage>";inherits:true;initial-value:50%;}
.ex{--ex-x:var(--gutter);--ex-pick:76px;--ex-w:7vw;--ex-foot:clamp(2.2rem,6vh,4rem);
  --ex-in:max(var(--ex-x),calc((100% - var(--measure)) / 2));
  --ex-giant:min(calc(var(--fs-display) * 2.75),22vw);
  /* the small grey words: --gray alone is 3.8:1 on the page, this mix holds 5.5:1 */
  --ex-dim:color-mix(in srgb,var(--gray-light) 40%,var(--gray));
  position:relative;overflow-x:clip;color:var(--gray-light);}
@media (max-width:759px){.ex{--ex-pick:64px;}}
@media (max-width:560px){.ex{--ex-x:var(--sp-2);--ex-w:9vw;--ex-foot:1.25rem;}}
@media (prefers-reduced-motion:no-preference){html:has(.ex){scroll-behavior:smooth;}}
.ex-in{box-sizing:border-box;width:100%;padding-inline:var(--ex-in);}
.ex-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
.ex :focus-visible{outline:2px solid var(--white);outline-offset:3px;}
:where(.ex) :where(p,h1,h2,h3,dl,dd,figure,ul,ol){margin:0;}

/* links: an arrow that moves on, and an underline that draws in under the pointer */
.ex-more{position:relative;display:inline-flex;align-items:center;gap:.6rem;min-height:44px;font-size:var(--fs-body-s);font-weight:600;color:var(--white);text-decoration:none;
  background:linear-gradient(var(--edge-hi),var(--edge-hi)) 0 calc(100% - 9px)/100% 1px no-repeat;}
.ex-more::before{content:"";position:absolute;left:0;right:0;bottom:9px;height:1px;background:var(--orange);transform:scaleX(0);transform-origin:left;transition:transform .7s var(--ease);}
.ex-more:hover::before,.ex-more:focus-visible::before{transform:scaleX(1);}
.ex-arr{width:16px;height:10px;flex:none;transition:transform .6s var(--ease);}
.ex-more:hover .ex-arr,.ex-more:focus-visible .ex-arr{transform:translateX(4px);}
.ex-ext{width:11px;height:11px;flex:none;}

/* the button: the site's orange, skewed like the menu's, quiet until pointed at */
.ex-btn{position:relative;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 1.6rem;
  font-size:var(--fs-body-s);font-weight:700;letter-spacing:.01em;color:var(--ink);text-decoration:none;white-space:nowrap;}
.ex-btn::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--orange);transform:skewX(-10deg);transition:transform .5s var(--ease),filter .4s var(--ease);}
.ex-btn:hover::before{transform:skewX(-10deg) scaleX(1.04);filter:brightness(1.06);}

/* ---------- the opening: two skies, one dissolve ---------- */
.ex-top{position:relative;isolation:isolate;display:flex;flex-direction:column;justify-content:flex-end;
  min-height:clamp(560px,calc(100svh - 93px - var(--ex-pick)),1000px);}
.ex-two{position:absolute;inset:0;z-index:-1;--ex-split:50%;}
.ex-pic{position:absolute;inset:0;overflow:hidden;-webkit-mask-composite:source-in;mask-composite:intersect;}
/* each photograph sits in the part of the width it can ever show (to a 60% lean), a little taller than
   the opening and held to its foot, so the wing rides above the title */
.ex-pic picture{position:absolute;top:-12%;bottom:0;width:calc(60% + var(--ex-w));height:auto;}
.ex-pic.is-a picture{left:0;top:-20%;}
.ex-pic.is-b picture{right:0;}
.ex-pic.is-a{-webkit-mask-image:__MASK_A__,__MASK_TOP__;mask-image:__MASK_A__,__MASK_TOP__;}
.ex-pic.is-b{-webkit-mask-image:__MASK_B__,__MASK_TOP__;mask-image:__MASK_B__,__MASK_TOP__;}
:where(.ex) picture{display:block;width:100%;height:100%;}
.ex picture img{display:block;width:100%;height:100%;object-fit:cover;object-position:var(--xy);}
.ex-half{position:absolute;top:0;bottom:0;color:var(--white);text-decoration:none;}
.ex-half.is-a{left:0;width:50%;}
.ex-half.is-b{left:50%;right:0;}
.ex-half:focus-visible{outline:none;}
.ex-half:focus-visible .ex-cap{outline:2px solid var(--white);outline-offset:8px;}
/* each half's name sits under its own photograph, on ground the photograph has already dissolved into */
.ex-cap{position:absolute;bottom:var(--ex-foot);display:flex;flex-direction:column;gap:.2rem;}
.ex-half.is-a .ex-cap{left:var(--ex-in);}
.ex-half.is-b .ex-cap{right:var(--ex-in);align-items:flex-end;text-align:right;}
.ex-cap b{display:inline-flex;align-items:center;gap:.55rem;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);letter-spacing:-.01em;color:var(--white);}
.ex-cap>span{font-size:var(--fs-small);color:var(--gray-light);}
.ex-dn{width:10px;height:14px;transition:transform .6s var(--ease);}
.ex-half:hover .ex-dn,.ex-half:focus-visible .ex-dn{transform:translateY(3px);}
.ex-head{position:relative;z-index:1;padding:0 var(--ex-x) var(--ex-foot);text-align:center;pointer-events:none;}
/* a long eased shade under the title, so the words stand on the photographs without a box */
.ex-head::before{content:"";position:absolute;z-index:-1;left:50%;bottom:-10%;width:min(1180px,135%);height:165%;transform:translateX(-50%);
  background:radial-gradient(closest-side at 50% 58%,__SHADE__);pointer-events:none;}
/* the page's kicker runs along the top, on the dark the two photographs rise out of */
.ex-kick{position:absolute;z-index:1;top:clamp(1.25rem,3.4vh,2rem);left:50%;transform:translateX(-50%);padding-left:.2em;
  font-size:var(--fs-micro);font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--orange);pointer-events:none;}
.ex-h1{font-family:var(--font-display);font-weight:700;font-size:min(calc(var(--fs-display) * 2.05),17vw);line-height:.9;letter-spacing:-.05em;color:var(--white);}
.ex-sub{max-width:31rem;margin:var(--sp-3) auto 0;font-size:var(--fs-lead);line-height:1.6;color:var(--gray-light);text-wrap:balance;}
/* the signature: point at a sky and it leans open, slowly; the other gives way */
@media (hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference){
  .ex-two{transition:--ex-split 1.6s var(--ease);}
  .ex-two:has(.ex-half.is-a:is(:hover,:focus-visible)){--ex-split:60%;}
  .ex-two:has(.ex-half.is-b:is(:hover,:focus-visible)){--ex-split:40%;}
}

/* ---------- the chooser: the year ahead, to scale ---------- */
.ex-pick{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--bg) 97%,transparent);
  -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);transition:top .38s var(--ease);}
/* when the menu comes back (scrolling up), the chooser steps down under it, as the site's other sticky bars do */
html.v2-nav-up .ex-pick{top:var(--v2-nav-h,93px);}
.ex-pick-in{position:relative;box-sizing:border-box;height:var(--ex-pick);margin-inline:var(--ex-in);}
/* the line: a hairline year, a tick at each month, a taller one where 2027 begins */
.ex-line{position:absolute;left:0;right:0;top:46px;height:1px;background:var(--edge);}
.ex-bar{position:absolute;top:-2px;height:5px;border-radius:1px;background:var(--gray-light);transition:background-color .5s var(--ease);}
.ex-bar.is-plan{box-sizing:border-box;background:transparent;border:1px solid var(--gray-light);}
.ex-months{position:absolute;left:0;right:0;top:46px;display:grid;grid-template-columns:repeat(14,minmax(0,1fr));}
.ex-months span{position:relative;padding-top:8px;text-align:center;font-size:var(--fs-micro);line-height:1.2;color:var(--gray-light);}
.ex-months span::before{content:"";position:absolute;left:0;top:-3px;width:1px;height:4px;background:var(--edge);}
.ex-months span.is-y::before{top:-9px;height:13px;background:var(--edge-hi);}
.ex-months b{font-weight:400;}
.ex-months i{display:none;font-style:normal;}
/* the places: each over its first departure, the whole height of the bar its target */
.ex-places{list-style:none;padding:0;}
.ex-places li{position:absolute;top:0;}
.ex-places a{display:flex;align-items:baseline;gap:.55rem;box-sizing:border-box;min-width:44px;height:var(--ex-pick);padding-top:14px;
  text-decoration:none;white-space:nowrap;}
.ex-places b{font-family:var(--font-display);font-weight:600;font-size:var(--fs-body-s);color:var(--gray-light);transition:color .5s var(--ease);}
.ex-mo{font-size:var(--fs-small);color:var(--gray-light);font-variant-numeric:tabular-nums;}
.ex-places a:hover b,.ex-places a:focus-visible b,.ex-places a[aria-current] b{color:var(--white);}
.ex-places a:focus-visible{outline-offset:-2px;}
__BAR_RULES__

/* ---------- a chapter: one photograph, the place, one line, four facts ---------- */
.ex-ch{position:relative;padding-bottom:calc(var(--sp-section) * 1.6);}
.ex-ph{position:relative;height:min(92svh,62vw);min-height:460px;}
.ex-ph picture{position:absolute;inset:0;}
.ex-ph picture{-webkit-mask-image:__MASK_CH__;mask-image:__MASK_CH__;}
/* the place, and on the side it leaves free, level with its foot, the photograph's own name from its trip
   page (where the photograph has all but dissolved, so the small grey words keep their contrast); when
   the two cannot share a line the name of the photograph goes under */
.ex-name{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:.9rem 2rem;}
.ex-ch.is-r .ex-name{flex-direction:row-reverse;}
.ex-photo{display:flex;align-items:center;gap:.6rem;padding-bottom:.2rem;font-size:var(--fs-small);color:var(--gray-light);}
.ex-photo::before{content:"";width:1.4rem;height:1px;background:var(--edge-hi);}
.ex-body{position:relative;margin-top:calc(var(--ex-giant) * -1.06);}
.ex-where{font-size:var(--fs-small);font-weight:500;color:var(--white);margin-bottom:.7rem;}
.ex-ch.is-r .ex-where{text-align:right;}
.ex-place{font-family:var(--font-display);font-weight:700;font-size:var(--ex-giant);line-height:.8;letter-spacing:-.055em;color:var(--white);margin-left:-.04em;}
.ex-ch.is-r .ex-place{margin:0 -.02em 0 0;}
.ex-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);grid-template-areas:"line info" "air acts";
  gap:var(--sp-5) clamp(2rem,6vw,6rem);margin-top:clamp(2.4rem,5vw,4.5rem);align-items:start;}
.ex-line-s{grid-area:line;font-family:var(--font-display);font-weight:500;font-size:var(--fs-h3);line-height:1.42;letter-spacing:-.012em;color:var(--white);text-wrap:pretty;max-width:24em;}
.ex-info{grid-area:info;}
.ex-air{grid-area:air;}
.ex-acts{grid-area:acts;}
.ex-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-3);padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.ex-facts dt{font-size:var(--fs-small);color:var(--ex-dim);margin-bottom:.5rem;}
.ex-facts dd{font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);line-height:1.35;color:var(--white);font-variant-numeric:tabular-nums;}
.ex-facts dd>span{display:block;white-space:nowrap;}
.ex-facts small{display:block;margin-top:.15rem;font-family:var(--font-body);font-weight:400;font-size:var(--fs-small);color:var(--gray-light);}
.ex-status{display:flex;align-items:center;gap:.65rem;margin-top:var(--sp-3);font-size:var(--fs-body-s);font-weight:500;color:var(--white);}
.ex-status i{flex:none;width:7px;height:7px;border-radius:50%;background:var(--orange);}
.ex-air{display:grid;gap:.5rem;font-size:var(--fs-small);color:var(--gray-light);}
.ex-air>div{display:grid;grid-template-columns:6.5rem minmax(0,1fr);gap:var(--sp-2);}
.ex-air dt{color:var(--ex-dim);}
.ex-acts{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-2) var(--sp-5);padding-left:.35rem;}

/* ---------- planned: quieter, type only ---------- */
.ex-later{position:relative;isolation:isolate;padding:calc(var(--sp-section) * .6) 0 calc(var(--sp-section) * 1.4);}
.ex-later-h{font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);letter-spacing:-.01em;color:var(--white);margin-bottom:clamp(2rem,4vw,3rem);}
.ex-later-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));}
.ex-plan{padding-right:clamp(1.5rem,5vw,5rem);scroll-margin-top:calc(var(--ex-pick) + 6.5rem);}
.ex-plan+.ex-plan{padding:0 0 0 clamp(1.5rem,5vw,5rem);border-left:1px solid var(--line);}
.ex-plan .ex-where{color:var(--gray-light);margin-bottom:.5rem;}
.ex-place-s{font-family:var(--font-display);font-weight:600;font-size:min(calc(var(--fs-display) * 1.25),13vw);line-height:.95;letter-spacing:-.045em;color:var(--gray-light);margin-bottom:var(--sp-4);}
.ex-facts.is-s dd{font-size:var(--fs-body);}
@media (max-width:1100px){.ex-facts.is-s{grid-template-columns:repeat(2,minmax(0,1fr));}}
.ex-plan .ex-more{margin-top:var(--sp-3);}

/* ---------- the close ---------- */
.ex-end{padding:calc(var(--sp-section) * .8) 0 calc(var(--sp-section) * 1.6);text-align:center;}
.ex-end-h{font-family:var(--font-display);font-weight:700;font-size:var(--fs-h1);line-height:1.05;letter-spacing:-.035em;color:var(--white);text-wrap:balance;}
.ex-end p:not(.ex-links){max-width:32rem;margin:var(--sp-3) auto 0;font-size:var(--fs-lead);line-height:1.6;color:var(--gray-light);text-wrap:balance;}
.ex-links{display:flex;justify-content:center;flex-wrap:wrap;gap:0 var(--sp-5);margin-top:var(--sp-4);}

/* ---------- tablets: the places stack over their months ---------- */
@media (max-width:1023px){
  .ex-places a{flex-direction:column;gap:0;padding-top:8px;}
  .ex-places b{line-height:1.25;}
  .ex-mo{font-size:var(--fs-micro);line-height:1.3;}
  .ex-line,.ex-months{top:50px;}
  .ex{--ex-pick:84px;}
}
/* ---------- tablets and phones: the names go to the top corners, over a longer dissolve ---------- */
@media (max-width:900px){
  .ex-pic.is-a{-webkit-mask-image:__MASK_A__,__MASK_TOP_S__;mask-image:__MASK_A__,__MASK_TOP_S__;}
  .ex-pic.is-b{-webkit-mask-image:__MASK_B__,__MASK_TOP_S__;mask-image:__MASK_B__,__MASK_TOP_S__;}
  .ex-cap{bottom:auto;top:clamp(1rem,2.6vh,1.6rem);}
  .ex picture img{object-position:var(--xym);}
  .ex-grid{grid-template-columns:minmax(0,1fr);grid-template-areas:"line" "info" "air" "acts";gap:var(--sp-4);}
  .ex-line-s{max-width:30em;}
}
/* ---------- small screens: the places alone, the months as initials ---------- */
@media (max-width:759px){
  .ex{--ex-pick:64px;}
  .ex-places a{padding-top:10px;}
  .ex-mo{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
  .ex-line,.ex-months{top:36px;}
  .ex-months span{padding-top:6px;}
  .ex-months b{display:none;}
  .ex-months i{display:inline;}
}
/* ---------- phones ---------- */
@media (max-width:560px){
  .ex-top{min-height:clamp(540px,calc(100svh - 93px - var(--ex-pick)),760px);}
  .ex-head{padding-bottom:calc(var(--ex-foot) + .8rem);}
  .ex-cap b{font-size:var(--fs-body);}
  .ex-cap>span{font-size:var(--fs-micro);}
  .ex-sub{font-size:var(--fs-body);}
  .ex-places b{font-size:var(--fs-small);}
  .ex-ph{height:auto;min-height:0;aspect-ratio:4/5;}
  .ex-ph picture{-webkit-mask-image:__MASK_CH_S__;mask-image:__MASK_CH_S__;}
  .ex-body{margin-top:calc(var(--ex-giant) * -.92);}
  .ex-facts{grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-3) var(--sp-2);}
  .ex-acts{gap:var(--sp-1) var(--sp-4);}
  .ex-later-grid{grid-template-columns:minmax(0,1fr);}
  .ex-plan{padding:0 0 var(--sp-5);}
  .ex-plan+.ex-plan{padding:var(--sp-5) 0 0;border-left:0;border-top:1px solid var(--line);}
  .ex-links{flex-direction:column;align-items:center;}
}
@media (prefers-reduced-motion:reduce){
  .ex *,.ex *::before,.ex *::after,.ex-two,.ex-pick{transition:none!important;}
}
"""


def bar_rules():
    """The chooser's bars answer their place: white under the pointer, orange for the chapter you are in."""
    out = []
    for t in TRIPS + PLANNED:
        k = t["id"]
        out.append('.ex-pick-in:has(a[href="#%s"]:is(:hover,:focus-visible)) .ex-bar[data-t="%s"]{background:var(--white);}' % (k, k))
        out.append('.ex-pick-in:has(a[href="#%s"][aria-current]) .ex-bar[data-t="%s"]{background:var(--orange);border-color:var(--orange);}' % (k, k))
    return "\n".join(out)


SCRIPT = r"""<script>
/* Expeditions: the chooser marks the chapter you are in. Nothing else needs a script. */
(function () {
  var d = document, w = window, pick = d.querySelector(".ex-pick");
  if (!pick) return;
  var links = Array.prototype.slice.call(pick.querySelectorAll('a[href^="#"]'));
  var parts = links.map(function (a) { return d.getElementById(a.getAttribute("href").slice(1)); });
  var on = -1, chosen = -1, queued = false;
  function mark(i) {
    if (i === on) return;
    if (on > -1) links[on].removeAttribute("aria-current");
    on = i;
    if (i > -1) links[i].setAttribute("aria-current", "location");
  }
  // each chapter owns the page from its top to the next chapter's top (or the end of its section),
  // and the one crossing a line a little above the middle of the screen is the one you are in
  function update() {
    queued = false;
    var line = w.innerHeight * 0.42, hit = [];
    var tops = parts.map(function (el) { return el ? el.getBoundingClientRect().top : Infinity; });
    parts.forEach(function (el, i) {
      if (!el) return;
      var top = tops[i], end = el.closest("section").getBoundingClientRect().bottom;
      tops.forEach(function (t) { if (t > top + 1 && t < end) end = t; });
      if (top <= line && end > line) hit.push(i);
    });
    // side by side (the planned two on a wide screen): the one chosen, else the first
    mark(hit.length ? (hit.indexOf(chosen) > -1 ? chosen : hit[0]) : -1);
  }
  function soon() { if (!queued) { queued = true; w.requestAnimationFrame(update); } }
  links.forEach(function (a, i) { a.addEventListener("click", function () { chosen = i; soon(); }); });
  w.addEventListener("scroll", soon, { passive: true });
  w.addEventListener("resize", soon);
  update();
})();
</script>"""


def ld():
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":"%s#webpage","name":"%s","url":"%s","description":"%s",'
            '"isPartOf":{"@id":"https://paraglidingatlas.com/#website"},'
            '"publisher":{"@id":"https://paraglidingatlas.com/#organization"},"inLanguage":"en",'
            '"dateModified":"%s"}\n</script>'
            % (URL, TITLE, URL, DESC.replace('"', '\\"'), MODIFIED))


def css():
    return (CSS.replace("__SHADE__", SHADE).replace("__MASK_A__", MASK_A).replace("__MASK_B__", MASK_B)
            .replace("__MASK_TOP_S__", MASK_TOP_S).replace("__MASK_TOP__", MASK_TOP)
            .replace("__MASK_CH_S__", MASK_CH_S).replace("__MASK_CH__", MASK_CH)
            .replace("__BAR_RULES__", bar_rules()))


def words(markup):
    """The words a visitor sees in <main>: tags, scripts, visually hidden spans and the chooser's
    hidden months (phones) out; the chooser's months on wide screens counted once."""
    t = re.sub(r"<script.*?</script>", " ", markup, flags=re.S)
    t = re.sub(r'<span class="ex-vh">.*?</span>', " ", t)
    t = re.sub(r'<div class="ex-months".*?</div>', " ", t, flags=re.S)
    t = re.sub(r"<svg.*?</svg>", " ", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return [x for x in t.split() if re.search(r"\w", x)]


def main():
    s = open(SHELL, encoding="utf-8").read()
    head, rest = s.split('<main id="v4-main">', 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % TITLE, head, 1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, head, 1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + OG_IMG, head, 1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "WebPage".*?</script>',
                  lambda m: ld(), head, 1, flags=re.S)
    head = re.sub(r"<!--v4u-css-->.*?<!--/v4u-css-->", "", head, 1, flags=re.S)
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + css() + "</style>\n", head, 1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    if ".ex-top" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_expeditions_a: the partners shell has changed; check the head")
    body = main_html()
    page = head + body + tail.replace("</body>", SCRIPT + "\n</body>", 1)
    if "—" in page:
        raise SystemExit("v4_expeditions_a: an em dash crept in")
    if re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", css() + body + SCRIPT):
        raise SystemExit("v4_expeditions_a: a raw colour crept in; use the design tokens")
    n = len(words(body))
    if n > MAX_WORDS:
        raise SystemExit("v4_expeditions_a: %d words in <main>; keep it under %d" % (n, MAX_WORDS))
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_expeditions_a: %s (%d words in <main>)" % (os.path.relpath(OUT, ROOT), n))


if __name__ == "__main__":
    main()
