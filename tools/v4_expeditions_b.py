#!/usr/bin/env python3
"""
The expeditions page, option B, "The season" (owner, 19 Oct 2026): "expeditions
standalone tab needs to be a redesigned page, it's just an off copy of leftover
material at homepage, I want it to be a bit different."

    prototypes/v4/expeditions-b.html

The home page's #destinations section keeps its four trip cards over one held
picture, its dates-and-prices table and its book-a-call band. This page repeats
none of them. It is for a pilot choosing a trip, and it is decision-first: you
choose by when you can travel, then compare.

  - the opening is the year itself, October 2026 to November 2027, drawn as
    one horizon to scale, day by day (the signature): weeks as hairline ticks,
    months marked and named, each flying season a brighter stretch of the line,
    every departure an orange bar exactly as long as the trip, the planned
    trips dotted at their month. The year is lit where we fly: each place's
    photograph stands as the sky over its own season and dissolves into the
    next (India over October and November, Kenya over December to March), and
    the months still to be photographed stay dark, with the heading in them.
    Each expedition's name hangs from the line at its first departure with its
    dates, and leads to that trip's dates (or, planned, to Register interest).
    On wide screens the line runs across; below 1100px it runs down the page,
    months on the left, each photograph beside its months and clear of the
    words;
  - below it the four expeditions side by side, in the order they fly, one
    column each (four across on wide screens with the row names once at the
    left; India beside Kenya, then the two planned trips, on tablets and
    phones): the flying, level, season (with the year line again in miniature,
    so the four seasons step across the page), length, group, price and
    status, read across in seconds; each column leads to its trip page (or
    Register interest). Typography only: no cards, no panel, no departures
    table;
  - a quiet close: one photograph (last light) dissolving into the page, and
    the free call as a line of text with two links, not a band.

Facts only, each from the site as it stands (prototypes/v4/):
  - index.html #destinations: the departures (India Tour 1 21 to 30 Oct 2026,
    Tour 2 3 to 12 Nov 2026, 10 days, 6 places, £1,100, Guaranteed to run,
    skill level 4 of 5; Kenya Tour 1 18 to 29 Jan 2027, Tour 2 1 to 12 Feb 2027,
    12 days, 8 places, from US$2,100, Booking open, skill level 2 of 5;
    Kazakhstan, the steppe, planned June 2027, 10 days, small group, €2,100;
    Peru, Lima and the Andes, planned November 2027, 14 days, small group,
    €1,850; both Register interest), the regions under each name, and "Prices
    are per pilot";
  - destinations/india.html: Big Mountain Flying, cloudbase 3 to 3.6 km on the
    front range, IPPI 2 or equivalent, season October to November, 1 guide to
    3 pilots;
  - destinations/kenya.html: six sites down the Rift, thermals 4 to 6 m/s at
    the midday peaks, IPPI 2 or equivalent, season December to March, a
    maximum ratio of one to three, starting from US$2,100;
  - the free 30-minute call and its link: the home and trip pages.
  The planned trips' prices are shown as the home page shows them (€2,100,
  €1,850). Unknowns (the planned trips' flying and level) show as [to supply].

Photographs: only the trip pages' own, each with the alt text its trip page
gives it, none called a place or a person: India, hero/snowline (the red wing
over snow); Kenya, hero/equator (the yellow wing in low golden light); the
close, india/gallery/last-light. No stock, no video. Every edge dissolves over
long smootherstep masks (eased(), mask()); no text ever sits on a picture.

Motion only answers the visitor. Pointing along the year (a month, a season's
photograph, an expedition's name), or tabbing to an expedition, brings that
season forward (its photograph, its marks on the line, its name) and lets the
others recede, and names the month pointed at; a month with no expedition
lets everything rest. Nothing runs on a timer or loops. With reduced motion the
same happens without the fade; with JavaScript off everything is there and
nothing moves. No libraries.

The page takes the v4 shell (head, menu, footer) from partners.html and writes
its own <main>, <style> and <script>. Prototype-only until the owner approves;
the menu is wired by the owner.

    python3 tools/v4_expeditions_b.py
"""
import datetime
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "expeditions-b.html")

TITLE = "Expeditions"
DESC = ("Every Paragliding Atlas expedition on one line, October 2026 to November 2027: India and Kenya, "
        "and the planned Kazakhstan and Peru trips, side by side.")
URL = "https://paraglidingatlas.com/expeditions.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/india/hero/snowline.jpg"

CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
TBD = '<span class="v2-tbd">[to supply]</span>'

A = "../../assets/"
# key: (file without extension, width, height, alt as the trip page gives it)
IMG = {
    "india": (A + "destinations/india/hero/snowline", 1800, 1200,
              "A pilot on a red wing flying over snow-covered mountains"),
    "kenya": (A + "destinations/kenya/hero/equator", 1152, 768,
              "A yellow paraglider on a long glide over arid rock outcrops in low golden light"),
    "close": (A + "destinations/india/gallery/last-light", 1400, 933,
              "A paraglider silhouetted against a burning sunset"),
}

# the year line: the first of October 2026 to the end of November 2027
Y0 = datetime.date(2026, 10, 1)
Y1 = datetime.date(2027, 12, 1)
SPAN = (Y1 - Y0).days
D = datetime.date


def at(day):
    """a date as a fraction of the year line"""
    return round((day - Y0).days / SPAN, 4)


def months():
    out, m = [], Y0
    while m < Y1:
        n = D(m.year + (m.month == 12), m.month % 12 + 1, 1)
        out.append((m, n))
        m = n
    return out


# the expeditions, in the order they fly. Every value is quoted from the page named in the docstring.
TRIPS = [
    {"k": "india", "name": "India", "where": "Bir Billing, Himalaya",
     "dates": "destinations/india.html#dates",
     "season": (D(2026, 10, 1), D(2026, 12, 1)), "season_txt": "October to November",
     "deps": [("Tour 1", D(2026, 10, 21), D(2026, 10, 31), "21 to 30 Oct 2026"),
              ("Tour 2", D(2026, 11, 3), D(2026, 11, 13), "3 to 12 Nov 2026")],
     "flying": ("Big Mountain Flying", "Cloudbase 3 to 3.6 km on the front range"),
     "level": 4, "rating": "IPPI 2 or equivalent",
     "length": "10 days", "group": ("6 places", "1 guide to 3 pilots"),
     "price": "&pound;1,100", "status": ("Guaranteed to run", "go"),
     "go": ("See the trip", "destinations/india.html")},
    {"k": "kenya", "name": "Kenya", "where": "Kerio Valley, Rift Valley",
     "dates": "destinations/kenya.html#dates",
     "season": (D(2026, 12, 1), D(2027, 4, 1)), "season_txt": "December to March",
     "deps": [("Tour 1", D(2027, 1, 18), D(2027, 1, 30), "18 to 29 Jan 2027"),
              ("Tour 2", D(2027, 2, 1), D(2027, 2, 13), "1 to 12 Feb 2027")],
     "flying": ("Six sites down the Rift", "Thermals 4 to 6 m/s at the midday peaks"),
     "level": 2, "rating": "IPPI 2 or equivalent",
     "length": "12 days", "group": ("8 places", "1 guide to 3 pilots at most"),
     "price": "From US$2,100", "status": ("Booking open", "open"),
     "go": ("See the trip", "destinations/kenya.html")},
    {"k": "kazakhstan", "name": "Kazakhstan", "where": "The steppe",
     "dates": "enquire.html?trip=kazakhstan",
     "plan": (D(2027, 6, 1), D(2027, 7, 1), "June 2027"),
     "flying": None, "level": None, "rating": None,
     "length": "10 days", "group": ("Small group", ""),
     "price": "&euro;2,100", "status": ("Planned", "plan"),
     "go": ("Register interest", "enquire.html?trip=kazakhstan")},
    {"k": "peru", "name": "Peru", "where": "Lima and the Andes",
     "dates": "enquire.html?trip=peru",
     "plan": (D(2027, 11, 1), D(2027, 12, 1), "November 2027"),
     "flying": None, "level": None, "rating": None,
     "length": "14 days", "group": ("Small group", ""),
     "price": "&euro;1,850", "status": ("Planned", "plan"),
     "go": ("Register interest", "enquire.html?trip=peru")},
]

# where each season's photograph stands, as fractions of the year line:
# across on wide screens (left, right), down the page below 1100px (top, bottom); and what each crop keeps
PHOTO = {
    "india": {"h": (None, 0.235), "v": (-0.07, 0.205), "hpos": "72% 60%", "vpos": "70% 62%"},
    "kenya": {"h": (0.105, 0.565), "v": (0.115, 0.475), "hpos": "66% 44%", "vpos": "70% 44%"},
}
HMASK = {  # wide screens: (horizontal edges, vertical edges), each (from %, to %, rising?)
    "india": ([(0, 24, True), (60, 100, False)], [(0, 34, True), (58, 100, False)]),
    "kenya": ([(0, 30, True), (70, 100, False)], [(0, 30, True), (60, 100, False)]),
}
VMASK = {  # phones and tablets: the photograph runs off the right edge, so only its left and its ends dissolve
    "india": ([(0, 56, True)], [(0, 36, True), (62, 100, False)]),
    "kenya": ([(0, 56, True)], [(0, 26, True), (70, 100, False)]),
}
CLOSE_MASK = ([(0, 18, True), (82, 100, False)], [(0, 40, True), (50, 100, False)])

ROWS = [("flying", "Flying"), ("level", "Level"), ("season", "Season"), ("length", "Length"),
        ("group", "Group"), ("price", "Price"), ("status", "Status")]

ARROW = ('<svg class="xb-arr" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M2 7h10M7.5 2.5 12 7l-4.5 4.5" '
         'fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')
DOWN = ('<svg class="xb-arr xb-down" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M7 2v10M2.5 7.5 7 12l4.5-4.5" '
        'fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')
EXT = ('<svg class="xb-arr" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M4 3h7v7M11 3 3 11" '
       'fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')


def eased(direction, edges, n=8):
    """A mask that dissolves over long eased ramps (smootherstep), never a hard edge.
    edges: [(from %, to %, rising?)...] in order along the gradient; opaque between a rise and a fall."""
    stops = []
    for p0, p1, rising in edges:
        for i in range(n + 1):
            t = i / n
            a = t * t * t * (t * (t * 6 - 15) + 10)
            a = a if rising else 1 - a
            stops.append((p0 + (p1 - p0) * t, a))
    parts = []
    for pos, a in stops:
        if a < 0.005:
            c = "transparent"
        elif a > 0.995:
            c = "var(--bg)"
        else:
            c = "color-mix(in srgb,var(--bg) %d%%,transparent)" % round(a * 100)
        parts.append("%s %.1f%%" % (c, pos))
    return "linear-gradient(%s,%s)" % (direction, ",".join(parts))


def mask(*layers):
    m = ",".join(layers)
    comp = "source-in" if len(layers) > 1 else "source-over"
    return ("-webkit-mask-image:%s;-webkit-mask-composite:%s;mask-image:%s;mask-composite:%s;"
            % (m, comp, m, "intersect" if len(layers) > 1 else "add"))


def pic(key, cls="", lazy=True, priority=False):
    base, w, h, alt = IMG[key]
    att = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if priority else ' decoding="async"')
    return ('<picture%s><source srcset="%s.webp" type="image/webp"><img src="%s.jpg" width="%d" height="%d" alt="%s"%s></picture>'
            % (' class="%s"' % cls if cls else "", base, base, w, h, html.escape(alt, quote=True), att))


def span(a, b):
    return "--a:%s;--b:%s" % (a, b)


def weeks_svg(vertical):
    """the weeks, as hairline ticks on Mondays: one path drawn in days, stretched to the line"""
    d, day = [], D(2026, 10, 5)
    while day < Y1:
        x = (day - Y0).days
        d.append(("M0 %d h1" if vertical else "M%d 0 v1") % x)
        day += datetime.timedelta(days=7)
    vb = "0 0 1 %d" % SPAN if vertical else "0 0 %d 1" % SPAN
    return ('<svg class="xb-weeks xb-weeks-%s" viewBox="%s" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<path d="%s" vector-effect="non-scaling-stroke"/></svg>' % ("v" if vertical else "h", vb, "".join(d)))


def zones():
    """what pointing at the year selects: each season (or planned month), as fractions of the line"""
    out = []
    for t in TRIPS:
        a, b = t["season"] if "season" in t else t["plan"][:2]
        out.append([t["k"], at(a), at(b)])
    return json.dumps(out, separators=(",", ":"))


# ---------------------------------------------------------------- the year
def year():
    sky = []
    for t in TRIPS:
        if t["k"] not in PHOTO:
            continue
        ph = PHOTO[t["k"]]
        ha, hb = ph["h"]
        va, vb = ph["v"]
        sky.append('<div class="xb-ph" data-k="%s" style="--ha:%s;--hb:%s;--va:%s;--vb:%s;--hpos:%s;--vpos:%s">%s</div>'
                   % (t["k"], 0 if ha is None else ha, hb, va, vb, ph["hpos"], ph["vpos"],
                      pic(t["k"], lazy=False, priority=(t["k"] == "india"))))
    flags, marks = [], []
    for t in TRIPS:
        if "deps" in t:
            first = t["deps"][0][1]
            lines = "".join('<span class="xb-when"><span class="xb-vh">%s, </span>%s</span>' % (n, txt) for n, _, _, txt in t["deps"])
            sa, sb = t["season"]
            marks.append('<i class="xb-season" data-k="%s" style="%s"></i>' % (t["k"], span(at(sa), at(sb))))
            for n, d0, d1, txt in t["deps"]:
                marks.append('<i class="xb-dep" data-k="%s" style="%s"></i>' % (t["k"], span(at(d0), at(d1))))
        else:
            d0, d1, txt = t["plan"]
            first = d0
            lines = '<span class="xb-when">%s, planned</span>' % txt
            marks.append('<i class="xb-plan" data-k="%s" style="%s"></i>' % (t["k"], span(at(d0), at(d1))))
        end = ' is-end' if at(first) > 0.8 else ''
        flags.append('<li class="xb-flag%s" data-k="%s" style="--a:%s"><a href="%s"><b>%s</b>%s</a></li>'
                     % (end, t["k"], at(first), t["dates"], t["name"], lines))
    ms = []
    for i, (m0, m1) in enumerate(months()):
        yr = '<small>%d</small>' % m0.year if (m0 == Y0 or m0.month == 1) else ''
        ms.append('<li data-m="%d" style="%s"><span>%s%s</span></li>' % (i, span(at(m0), at(m1)), m0.strftime("%b"), yr))
    return """
<section class="xb-year" id="xb-year" aria-labelledby="xb-title" data-zones='""" + zones() + """'>
  <div class="xb-in xb-year-in">
    <header class="xb-head">
      <p class="xb-kick">Expeditions</p>
      <h1 id="xb-title">Choose Your Season</h1>
      <p class="xb-lede">Every departure from October 2026 to November 2027, on one line. Find when you can travel, then compare.</p>
      <p class="xb-jump"><a href="#xb-compare">Compare all four""" + DOWN + """</a></p>
    </header>
    <div class="xb-cal">
      <h2 class="xb-vh">Departures, October 2026 To November 2027</h2>
      <div class="xb-sky">""" + "".join(sky) + """</div>
      <div class="xb-axis" aria-hidden="true"><i class="xb-base"></i>""" + weeks_svg(False) + weeks_svg(True) + "".join(marks) + """</div>
      <ol class="xb-months" aria-hidden="true">""" + "".join(ms) + """</ol>
      <ol class="xb-flags">""" + "".join(flags) + """</ol>
    </div>
    <ul class="xb-key" aria-hidden="true"><li><i class="is-season"></i>Flying season</li><li><i class="is-dep"></i>Departure</li><li><i class="is-plan"></i>Planned</li></ul>
  </div>
</section>
"""


# ---------------------------------------------------------------- side by side
def meter(n):
    segs = "".join('<i%s></i>' % (' class="is-on"' if i < n else '') for i in range(5))
    return '<span class="xb-meter" role="img" aria-label="Skill level %d of 5">%s</span>' % (n, segs)


def mini(t):
    """the year line again, in miniature: this expedition's season and departures in their place"""
    if "deps" in t:
        sa, sb = t["season"]
        body = '<i class="xb-mini-s" style="%s"></i>' % span(at(sa), at(sb))
        body += "".join('<i class="xb-mini-d" style="%s"></i>' % span(at(d0), at(d1)) for _, d0, d1, _ in t["deps"])
    else:
        d0, d1, _ = t["plan"]
        body = '<i class="xb-mini-p" style="%s"></i>' % span(at(d0), at(d1))
    return '<span class="xb-mini" aria-hidden="true">%s</span>' % body


def cell(t, key):
    if key == "flying":
        if not t["flying"]:
            return TBD
        return '<b>%s</b><span class="xb-sub">%s</span>' % t["flying"]
    if key == "level":
        if t["level"] is None:
            return TBD
        return ('<span class="xb-lv">%s<span aria-hidden="true">%d of 5</span></span><span class="xb-sub">%s</span>'
                % (meter(t["level"]), t["level"], t["rating"]))
    if key == "season":
        txt = t["plan"][2] if "plan" in t else t["season_txt"]
        return txt + mini(t)
    if key == "length":
        return t["length"]
    if key == "group":
        g, sub = t["group"]
        return g + ('<span class="xb-sub">%s</span>' % sub if sub else "")
    if key == "price":
        return '<b class="xb-price">%s</b>' % t["price"]
    if key == "status":
        s, kind = t["status"]
        return '<span class="xb-st is-%s"><i aria-hidden="true"></i>%s</span>' % (kind, s)
    raise KeyError(key)


def compare():
    labels = '<li></li>' + "".join('<li>%s</li>' % name for _, name in ROWS) + '<li></li>'
    cols = []
    for t in TRIPS:
        rows = "".join('<div class="xb-r xb-r-%s"><dt>%s</dt><dd>%s</dd></div>' % (key, name, cell(t, key)) for key, name in ROWS)
        go_txt, go_href = t["go"]
        cols.append("""
    <article class="xb-col%s" data-k="%s" aria-labelledby="xb-c-%s">
      <header class="xb-col-h"><h3 id="xb-c-%s">%s</h3><p>%s</p></header>
      <dl>%s</dl>
      <p class="xb-go"><a href="%s">%s<span class="xb-vh"> %s %s</span>%s</a></p>
    </article>""" % (" is-plan" if "plan" in t else "", t["k"], t["k"], t["k"], t["name"], t["where"],
                     rows, go_href, go_txt, "in" if "plan" in t else "to", t["name"], ARROW))
    return """
<section class="xb-cmpw" id="xb-compare" aria-labelledby="xb-cmp-h">
  <div class="xb-in">
    <div class="xb-cmp-head">
      <h2 id="xb-cmp-h">Side By Side</h2>
      <p>In the order they fly. Prices are per pilot.</p>
    </div>
    <div class="xb-cmp">
    <ol class="xb-labels" aria-hidden="true">""" + labels + "</ol>" + "".join(cols) + """
    </div>
  </div>
</section>
"""


def close():
    return """
<section class="xb-close" aria-labelledby="xb-close-h">
  <div class="xb-close-ph">""" + pic("close") + """</div>
  <div class="xb-in xb-close-in">
    <h2 id="xb-close-h">Still Deciding?</h2>
    <p>A free 30-minute call: the right tour for your skill, with dates and costs.</p>
    <p class="xb-close-go"><a href=\"""" + CALL + """\" target="_blank" rel="noopener">Book a Call""" + EXT + """<span class="xb-vh"> (opens in a new tab)</span></a><a href="enquire.html">Enquire""" + ARROW + """</a></p>
  </div>
</section>
"""


def main_html():
    return '<main id="v4-main" class="xb">\n' + year() + compare() + close() + "\n</main>"


# ---------------------------------------------------------------- styles
def photo_css():
    out = []
    for k, (hx, hy) in HMASK.items():
        out.append('@media (min-width:1100px){.xb-ph[data-k="%s"]{%s}}' % (k, mask(eased("90deg", hx), eased("180deg", hy))))
    for k, (vx, vy) in VMASK.items():
        out.append('@media (max-width:1099.98px){.xb-ph[data-k="%s"]{%s}}' % (k, mask(eased("90deg", vx), eased("180deg", vy))))
    out.append(".xb-close-ph{%s}" % mask(eased("90deg", CLOSE_MASK[0]), eased("180deg", CLOSE_MASK[1])))
    out.append("@media (min-width:1100px){.xb-year::before{%s}}" % mask(eased("180deg", [(0, 18, True), (58, 97, False)])))
    on = []
    for t in TRIPS:
        k = t["k"]
        on.append('.xb-year[data-on="{k}"] :is(.xb-ph,.xb-dep,.xb-season,.xb-plan,.xb-flag)[data-k="{k}"]'.format(k=k))
    out.append(",\n".join(on) + "{--on:1;}")
    return "\n".join(out)


CSS = r"""
/* ===== Expeditions, option B: the season (tools/v4_expeditions_b.py) ===== */
.xb{--xb-x:var(--gutter);
  --xb-dim:color-mix(in srgb,var(--gray-light) 58%,var(--gray));
  --xb-text:color-mix(in srgb,var(--white) 88%,var(--gray-light));
  --xb-gap:clamp(1rem,2.2vw,2rem);
  /* from the edge of the screen to the start of the year: photographs and the horizon run out to the edge */
  --xb-out:max(var(--xb-x),calc((100vw - var(--measure)) / 2 + var(--xb-x)));
  position:relative;overflow-x:clip;color:var(--xb-text);}
@media (max-width:560px){.xb{--xb-x:var(--sp-2);}}
.xb-in{box-sizing:border-box;width:100%;max-width:var(--measure);margin:0 auto;padding-inline:var(--xb-x);}
.xb-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
.xb .v2-tbd{color:var(--xb-dim);font-size:var(--fs-small);}
.xb a{color:inherit;text-decoration:none;}
/* the site's growing underline for plain links in text is not used here: these links carry their own */
.xb a:not([class]),.xb a:not([class]):hover,.xb a:not([class]):focus-visible{background:none;}
.xb :focus-visible{outline:2px solid var(--white);outline-offset:3px;border-radius:2px;}
.xb-arr{display:inline-block;flex:none;width:.8em;height:.8em;margin-left:.45em;vertical-align:-.04em;transition:translate .5s var(--ease);}

/* ---------- the opening: the heading and the year ---------- */
.xb-year{position:relative;isolation:isolate;padding:clamp(2.25rem,6vh,4.5rem) 0 clamp(1.5rem,4vh,3rem);}
/* the months still dark carry the evening of the visitor's own sky (the site's --sky tokens follow their clock) */
.xb-year::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;opacity:.75;
  background:radial-gradient(46% 70% at 80% 70%,var(--sky-horizon),transparent 74%),
             radial-gradient(36% 52% at 94% 26%,var(--sky-cool),transparent 72%);}
.xb-head{position:relative;z-index:2;max-width:34rem;}
.xb-kick{margin:0 0 var(--sp-2);font-size:var(--fs-micro);font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);}
.xb-head h1{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--fs-display);line-height:1;letter-spacing:-.035em;color:var(--white);text-wrap:balance;}
.xb-lede{margin:var(--sp-3) 0 0;max-width:27rem;font-size:var(--fs-lead);line-height:1.6;color:var(--gray-light);text-wrap:pretty;}
.xb-jump{margin:var(--sp-1) 0 0;}
.xb-jump a{display:inline-flex;align-items:center;min-height:44px;font-size:var(--fs-body-s);color:var(--gray-light);}
.xb-jump a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.3em;text-decoration-color:var(--edge);transition:text-decoration-color .4s var(--ease),color .4s var(--ease);}
.xb-jump a:hover,.xb-jump a:focus-visible{color:var(--white);text-decoration-color:var(--orange);}
.xb-jump a:hover .xb-down,.xb-jump a:focus-visible .xb-down{translate:0 .2rem;}

.xb-cal{position:relative;}
.xb-sky{position:absolute;inset:0;pointer-events:none;}
.xb-ph{position:absolute;opacity:calc(.9 + .1 * var(--on,0));transition:opacity .9s var(--ease),filter .9s var(--ease);}
.xb-ph picture,.xb-ph img{display:block;width:100%;height:100%;}
.xb-ph img{object-fit:cover;object-position:var(--hpos);}
@media (max-width:1099.98px){.xb-ph img{object-position:var(--vpos);}}
.xb-year[data-on] .xb-ph{opacity:calc(.26 + .74 * var(--on,0));filter:saturate(calc(.5 + .5 * var(--on,0)));}

.xb-axis{position:absolute;color:var(--edge);}
.xb-axis i{position:absolute;display:block;}
.xb-base{background:var(--edge);}
.xb-weeks{position:absolute;display:block;overflow:visible;}
.xb-weeks path{stroke:var(--edge);stroke-width:1;fill:none;}
.xb-season{background:color-mix(in srgb,var(--white) calc(55% + 45% * var(--on,0)),transparent);transition:background-color .6s var(--ease);}
.xb-dep{background:var(--orange);border-radius:3px;}
.xb-plan{border:0 dotted var(--gray-light);}
.xb-year[data-on] :is(.xb-dep,.xb-plan){opacity:calc(.3 + .7 * var(--on,0));transition:opacity .6s var(--ease);}

.xb-months{list-style:none;margin:0;padding:0;position:absolute;}
.xb-months li{position:absolute;display:block;}
.xb-months span{display:block;font-size:var(--fs-micro);letter-spacing:.06em;line-height:1.35;color:var(--xb-dim);font-variant-numeric:tabular-nums;transition:color .4s var(--ease);}
.xb-months small{display:block;font-size:var(--fs-micro);letter-spacing:.04em;color:var(--gray-light);}
.xb-months li.is-at span{color:var(--white);}

.xb-flags{list-style:none;margin:0;padding:0;}
.xb-flag{position:absolute;}
.xb-flag a{position:relative;display:flex;flex-direction:column;gap:.15rem;min-height:44px;justify-content:center;
  padding:.35rem .25rem .35rem .9rem;color:var(--xb-text);transition:color .5s var(--ease),opacity .6s var(--ease);}
.xb-flag b{font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);letter-spacing:-.01em;color:var(--white);line-height:1.2;}
.xb-when{font-size:var(--fs-body-s);line-height:1.35;color:var(--gray-light);font-variant-numeric:tabular-nums;white-space:nowrap;}
.xb-flag a::before{content:"";position:absolute;background:var(--edge-hi);transition:background-color .5s var(--ease);}
.xb-year[data-on] .xb-flag a::before{background:color-mix(in srgb,var(--white) calc(100% * var(--on,0)),var(--edge-hi));}
.xb-flag a:hover::before,.xb-flag a:focus-visible::before{background:var(--white);}
.xb-flag a:hover b,.xb-flag a:focus-visible b{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.2em;text-decoration-color:var(--edge-hi);}
.xb-year[data-on] .xb-flag{opacity:calc(.7 + .3 * var(--on,0));transition:opacity .6s var(--ease);}

/* wide screens: the year runs across as a horizon, the heading in the months still dark */
@media (min-width:1100px){
  .xb-year{--xb-top:clamp(16rem,44vh,26rem);--xb-fz:6.6rem;--xb-mz:2.7rem;--xb-pad:clamp(2.25rem,6vh,4.5rem);}
  .xb-year-in{display:grid;grid-template-columns:57fr 43fr;}
  .xb-head{grid-column:2;grid-row:1;min-height:var(--xb-top);display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:var(--sp-3);}
  .xb-cal{grid-column:1 / -1;grid-row:2;height:calc(var(--xb-fz) + var(--xb-mz));}
  .xb-sky{inset:auto 0 auto 0;top:calc(-1 * var(--xb-top) - var(--xb-pad));height:calc(var(--xb-top) + var(--xb-pad) + 1.2rem);}
  .xb-ph{top:0;bottom:0;left:calc(var(--ha) * 100%);width:calc((var(--hb) - var(--ha)) * 100%);}
  .xb-ph[data-k="india"]{left:calc(-1 * var(--xb-out));width:calc(var(--xb-out) + var(--hb) * 100%);}
  .xb-axis{left:0;right:0;top:var(--xb-fz);height:0;}
  .xb-axis i{top:0;left:calc(var(--a) * 100%);width:calc((var(--b) - var(--a)) * 100%);}
  /* the horizon itself runs out to both edges of the screen and fades there: the year goes on */
  .xb-base{left:calc(-1 * var(--xb-out))!important;width:calc(100% + 2 * var(--xb-out))!important;height:1px;
    background:linear-gradient(90deg,transparent,var(--edge) var(--xb-out),var(--edge) calc(100% - var(--xb-out)),transparent);}
  .xb-weeks-v{display:none;}
  .xb-weeks-h{left:0;top:0;width:100%;height:5px;}
  .xb-season{height:2px;top:-.5px!important;}
  .xb-dep{height:6px;top:-2.5px!important;}
  .xb-plan{height:0;border-top-width:3px;top:-1px!important;}
  .xb-months{left:0;right:0;top:calc(var(--xb-fz) + .8rem);height:var(--xb-mz);}
  .xb-months li{top:0;left:calc(var(--a) * 100%);width:calc((var(--b) - var(--a)) * 100%);padding-left:.45rem;}
  .xb-months li::before{content:"";position:absolute;left:0;top:-.8rem;height:.6rem;width:1px;background:var(--edge-hi);}
  .xb-flag{bottom:calc(var(--xb-mz) + .55rem);left:calc(var(--a) * 100%);}
  .xb-flag a{padding-bottom:.9rem;}
  .xb-flag a::before{left:0;top:.45rem;bottom:-.55rem;width:1px;}
  .xb-flag.is-end{left:auto;right:calc((1 - var(--a)) * 100%);}
  .xb-flag.is-end a{align-items:flex-end;text-align:right;padding-left:.25rem;padding-right:.9rem;}
  .xb-flag.is-end a::before{left:auto;right:0;}
  .xb-key{grid-column:1 / -1;grid-row:3;justify-content:flex-end;margin-top:.2rem;}
}
/* phones and tablets: the year runs down the page, each photograph beside its months */
@media (max-width:1099.98px){
  .xb-year{--xb-mh:clamp(3rem,7vw,3.75rem);--xb-ax:3.3rem;}
  .xb-year::before{display:none;}
  .xb-head{margin-bottom:clamp(2rem,6vw,3rem);}
  .xb-cal{height:calc(var(--xb-mh) * 14);margin-bottom:var(--sp-3);}
  .xb-sky{inset:0 calc(-1 * var(--xb-x)) 0 0;}
  .xb-ph{left:max(50%,13rem);right:0;top:calc(var(--va) * 100%);height:calc((var(--vb) - var(--va)) * 100%);}
  .xb-axis{top:0;bottom:0;left:var(--xb-ax);width:0;}
  .xb-axis i{left:0;top:calc(var(--a) * 100%);height:calc((var(--b) - var(--a)) * 100%);}
  .xb-base{top:0!important;height:100%!important;width:1px;
    background:linear-gradient(180deg,var(--edge) 92%,transparent);}
  .xb-weeks-h{display:none;}
  .xb-weeks-v{left:-4px;top:0;width:4px;height:100%;}
  .xb-season{width:2px;left:-.5px!important;}
  .xb-dep{width:6px;left:-2.5px!important;}
  .xb-plan{width:0;border-left-width:3px;left:-1px!important;}
  .xb-months{top:0;bottom:0;left:0;width:calc(var(--xb-ax) - .9rem);}
  .xb-months li{left:0;right:0;top:calc(var(--a) * 100%);height:calc((var(--b) - var(--a)) * 100%);}
  .xb-months li::before{content:"";position:absolute;right:-.9rem;top:0;width:.55rem;height:1px;background:var(--edge-hi);}
  .xb-months span{margin-top:-.45em;text-align:right;}
  .xb-flag{left:var(--xb-ax);top:calc(var(--a) * 100%);transform:translateY(-1.05rem);}
  .xb-flag a{padding-left:1.15rem;}
  .xb-flag a::before{left:0;top:1.05rem;width:.8rem;height:1px;}
  .xb-key{padding-left:calc(var(--xb-ax) - 1.6rem);}
}

/* ---------- side by side ---------- */
.xb-cmpw{padding:clamp(2rem,5vw,4rem) 0 clamp(3rem,8vw,6rem);}
.xb-cmp-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:var(--sp-1) var(--sp-4);margin:0 0 clamp(2rem,4vw,3.25rem);}
.xb-cmp-head h2{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-h2) * 1.25);line-height:1.05;letter-spacing:-.03em;color:var(--white);}
.xb-cmp-head p{margin:0;font-size:var(--fs-small);color:var(--xb-dim);}

.xb-cmp{display:grid;column-gap:0;}
.xb-labels{list-style:none;margin:0;padding:0;display:none;}
.xb-col{display:grid;grid-template-rows:subgrid;position:relative;isolation:isolate;}
.xb-col dl{display:grid;grid-template-rows:subgrid;margin:0;}
.xb-col-h{padding:0 0 var(--sp-3);}
.xb-col-h h3{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--fs-h3);letter-spacing:-.02em;line-height:1.15;color:var(--white);}
.xb-col-h h3{display:flex;align-items:center;min-height:44px;}
.xb-col-h p{margin:.1rem 0 0;font-size:var(--fs-small);color:var(--xb-dim);}
.xb-r{padding:var(--sp-2) 0;border-top:1px solid var(--line);min-width:0;}
.xb-r dt{font-size:var(--fs-micro);letter-spacing:.06em;color:var(--xb-dim);margin:0 0 .3rem;}
.xb-r dd{margin:0;font-size:var(--fs-body);line-height:1.45;color:var(--xb-text);}
.xb-r dd b{font-weight:500;color:var(--white);}
.xb-sub{display:block;margin-top:.2rem;font-size:var(--fs-body-s);line-height:1.45;color:var(--gray-light);}
.xb-lv{display:flex;align-items:center;gap:.6rem;font-variant-numeric:tabular-nums;}
.xb-meter{display:inline-flex;gap:3px;}
.xb-meter i{display:block;width:14px;height:5px;border-radius:1px;background:var(--edge);}
.xb-meter i.is-on{background:var(--white);}
/* the season again, in miniature: the year line with only this expedition on it */
.xb-mini{position:relative;display:block;height:6px;margin-top:.7rem;max-width:15rem;}
.xb-mini::before{content:"";position:absolute;left:0;right:0;top:2.5px;height:1px;background:var(--line);}
.xb-mini i{position:absolute;display:block;left:calc(var(--a) * 100%);width:calc((var(--b) - var(--a)) * 100%);}
.xb-mini-s{top:2px;height:2px;background:color-mix(in srgb,var(--white) 55%,transparent);}
.xb-mini-d{top:0;height:6px;border-radius:2px;background:var(--orange);}
.xb-mini-p{top:1.5px;height:0;border-top:3px dotted var(--gray-light);}
.xb-price{display:block;font-family:var(--font-display);font-weight:600!important;font-size:var(--fs-h3);letter-spacing:-.015em;line-height:1.2;font-variant-numeric:tabular-nums;}
.xb-key{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font-size:var(--fs-micro);letter-spacing:.04em;color:var(--xb-dim);}
.xb-key li{display:inline-flex;align-items:center;gap:.5rem;}
.xb-key i{display:block;width:1.1rem;}
.xb-key .is-season{height:2px;background:color-mix(in srgb,var(--white) 55%,transparent);}
.xb-key .is-dep{height:6px;border-radius:3px;background:var(--orange);}
.xb-key .is-plan{height:0;border-top:3px dotted var(--gray-light);}
.xb-st{display:inline-flex;align-items:center;gap:.5rem;}
.xb-st i{display:block;width:7px;height:7px;border-radius:50%;border:1px solid var(--orange);}
.xb-st.is-go i{background:var(--orange);}
.xb-st.is-plan i{border:1px dashed var(--xb-dim);}
.xb-go{margin:0;padding:var(--sp-1) 0 0;border-top:1px solid var(--line);}
.xb-go a{display:inline-flex;align-items:center;min-height:44px;font-weight:500;color:var(--white);
  text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.3em;text-decoration-color:var(--edge-hi);transition:text-decoration-color .4s var(--ease);}
.xb-go a:hover,.xb-go a:focus-visible{text-decoration-color:var(--orange);}
/* the whole column answers: its link stretches over it */
.xb-go a::after{content:"";position:absolute;inset:-.75rem 0;}
.xb-col:hover .xb-go a{text-decoration-color:var(--orange);}
.xb-col:hover .xb-go .xb-arr{translate:.25rem 0;}
.xb-go a:hover .xb-arr,.xb-go a:focus-visible .xb-arr{translate:.25rem 0;}
.xb-col.is-plan .xb-col-h h3{color:var(--gray-light);}

/* four across, the row names once at the left */
@media (min-width:1100px){
  .xb-cmp{grid-template-columns:minmax(6.5rem,.62fr) repeat(4,minmax(0,1fr));grid-template-rows:repeat(9,auto);}
  .xb-labels{display:grid;grid-template-rows:subgrid;grid-row:1 / span 9;grid-column:1;}
  .xb-labels li{padding:var(--sp-2) var(--sp-2) 0 0;border-top:1px solid var(--line);font-size:var(--fs-small);color:var(--xb-dim);}
  .xb-labels li:first-child{border-top:0;}
  .xb-col{grid-row:1 / span 9;padding-inline:clamp(1rem,2vw,1.75rem);border-left:1px solid var(--line);}
  .xb-col dl{grid-row:2 / span 7;}
  .xb-r dt{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
  .xb-col::before{content:"";position:absolute;inset:-.75rem 0;z-index:-1;background:var(--card);opacity:0;transition:opacity .5s var(--ease);border-radius:2px;}
  .xb-col:hover::before,.xb-col:focus-within::before{opacity:.45;}
}
/* two by two below that: India beside Kenya, then the two planned trips */
@media (max-width:1099.98px){
  .xb-cmp{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:repeat(18,auto);column-gap:var(--xb-gap);}
  .xb-col{grid-row:1 / span 9;}
  .xb-col:nth-of-type(n+3){grid-row:10 / span 9;}
  .xb-col:nth-of-type(n+3) .xb-col-h{padding-top:clamp(2.5rem,7vw,3.5rem);}
  .xb-col dl{grid-row:2 / span 7;}
}

/* ---------- the close ---------- */
.xb-close{position:relative;padding-bottom:clamp(3.5rem,9vw,7rem);}
.xb-close-ph{height:clamp(12rem,28vw,22rem);margin-bottom:calc(-1 * clamp(.5rem,2vw,2rem));opacity:.8;}
.xb-close-ph picture,.xb-close-ph img{display:block;width:100%;height:100%;}
.xb-close-ph img{object-fit:cover;object-position:50% 46%;}
.xb-close-in{position:relative;}
.xb-close h2{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-h2) * 1.25);letter-spacing:-.03em;line-height:1.05;color:var(--white);}
.xb-close-in>p{margin:var(--sp-2) 0 0;max-width:30rem;font-size:var(--fs-lead);line-height:1.6;color:var(--gray-light);}
.xb-close-go{display:flex;flex-wrap:wrap;gap:0 var(--sp-4);}
.xb-close .xb-close-go a{display:inline-flex;align-items:center;min-height:44px;font-weight:500;color:var(--white);
  text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.3em;text-decoration-color:var(--edge-hi);transition:text-decoration-color .4s var(--ease);}
.xb-close .xb-close-go a:hover,.xb-close .xb-close-go a:focus-visible{text-decoration-color:var(--orange);}
.xb-close-go a:hover .xb-arr,.xb-close-go a:focus-visible .xb-arr{translate:.2rem 0;}

@media (prefers-reduced-motion:reduce){
  .xb *,.xb *::before{transition:none!important;}
}
__PHOTOS__
"""


SCRIPT = r"""<script>
/* Expeditions, option B (tools/v4_expeditions_b.py). One behaviour, and only in
   answer to the visitor: pointing along the year (a month, a photograph, an
   expedition's name) or tabbing to an expedition brings that season forward,
   lets the others recede and names the month pointed at. Nothing runs on a
   timer. Without this script the page is complete. */
(function () {
  var year = document.getElementById("xb-year");
  if (!year) return;
  var cal = year.querySelector(".xb-cal"), flags = year.querySelector(".xb-flags");
  var months = year.querySelectorAll(".xb-months li"), zones = [];
  try { zones = JSON.parse(year.getAttribute("data-zones")) || []; } catch (e) {}
  if (!cal || !flags) return;
  var on = null, at = -1;
  function set(k, m) {
    if (k !== on) { on = k; if (k) year.setAttribute("data-on", k); else year.removeAttribute("data-on"); }
    if (m !== at) { if (months[at]) months[at].classList.remove("is-at"); at = m; if (months[at]) months[at].classList.add("is-at"); }
  }
  function key(el) { var f = el && el.closest && el.closest(".xb-flag"); return f ? f.getAttribute("data-k") : null; }
  function zone(f) {
    for (var i = 0; i < zones.length; i++) if (f >= zones[i][1] && f < zones[i][2]) return zones[i][0];
    return null;
  }
  function month(f) {
    for (var i = 0; i < months.length; i++) {
      var s = months[i].style, a = parseFloat(s.getPropertyValue("--a")), b = parseFloat(s.getPropertyValue("--b"));
      if (f >= a && f < b) return i;
    }
    return -1;
  }
  /* the season under the pointer: across the year on wide screens, down it below that */
  year.addEventListener("pointermove", function (e) {
    if (e.pointerType === "touch") return;
    var f = key(e.target);
    var r = cal.getBoundingClientRect(), across = r.width > r.height, x, inside;
    if (across) {
      x = (e.clientX - r.left) / r.width;
      /* the band of the line, or the photographs above it (not the heading over the dark months) */
      inside = e.clientY <= r.bottom && (e.clientY >= r.top || x < 0.56);
    } else {
      x = (e.clientY - r.top) / r.height;
      inside = e.clientY >= r.top && e.clientY <= r.bottom;
    }
    if (!inside || x < 0 || x >= 1) { set(f, -1); return; }
    set(f || zone(x), month(x));
  });
  year.addEventListener("pointerleave", function () { set(null, -1); });
  flags.addEventListener("focusin", function (e) { set(key(e.target), -1); });
  flags.addEventListener("focusout", function (e) { if (!flags.contains(e.relatedTarget)) set(null, -1); });
})();
</script>"""


def css():
    return CSS.replace("__PHOTOS__", photo_css())


def ld():
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":"%s#webpage","name":"%s","url":"%s","description":"%s",'
            '"isPartOf":{"@id":"https://paraglidingatlas.com/#website"},'
            '"publisher":{"@id":"https://paraglidingatlas.com/#organization"},"inLanguage":"en"}\n</script>'
            % (URL, TITLE, URL, DESC.replace('"', '\\"')))


def main():
    s = open(SHELL, encoding="utf-8").read()
    head, rest = s.split('<main id="v4-main">', 1)
    tail = rest.split("</main>", 1)[1]
    # the page's own title, description, address and picture
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % TITLE, head, 1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, head, 1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + DESC, head, 1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + OG_IMG, head, 1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, head, 1)
    # the partners page's own structured data and styles go; this page's come in
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "WebPage".*?</script>',
                  lambda m: ld(), head, 1, flags=re.S)
    head = re.sub(r"<!--v4u-css-->.*?<!--/v4u-css-->", "", head, 1, flags=re.S)
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + css() + "</style>\n", head, 1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    # the header's Expeditions tab leads here (owner, 19 Oct): marked as the page you are on
    head = head.replace('<a href="expeditions.html">Expeditions</a>',
                        '<a href="expeditions.html" aria-current="page" class="is-here">Expeditions</a>', 1)
    if 'aria-current="page" class="is-here">Expeditions</a>' not in head:
        raise SystemExit("v4_expeditions_b: the header has no Expeditions tab to mark")
    if ".xb-year" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_expeditions_b: the partners shell has changed; check the head")
    page = head + main_html() + tail.replace("</body>", SCRIPT + "\n</body>", 1)
    if "—" in page:
        raise SystemExit("v4_expeditions_b: an em dash crept in")
    # no colour written out: the styles, markup and script use only the design tokens
    if re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", css() + main_html() + SCRIPT):
        raise SystemExit("v4_expeditions_b: a raw colour crept in; use the design tokens")
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_expeditions_b: %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
