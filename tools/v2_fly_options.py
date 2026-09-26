#!/usr/bin/env python3
"""
Five ways to redesign the homepage block between "See where we fly" and
"Every departure" (the India and Kenya features and the two Coming 2027 cards).

prototypes/v2/fly-options.html  (hidden: noindex, never linked from the site)
prototypes/v2/fly-options.js    the page's behaviour

Every fact and picture is the site's own (the v2 homepage and the destination
pages); anything the site does not state yet shows as [to supply]. The nav and
footer are taken from prototypes/v2/index.html so the page sits in the real
v2 shell. Run tools/v2_localize.py afterwards.

    python3 tools/v2_fly_options.py
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = S.DIR
A = "../../assets/"
e = html.escape
TBD = '<i class="v2-tbd">[to supply]</i>'

TRIPS = [
    dict(key="india", place="India", region="Bir Billing, Himalaya", kicker="Sky Is Not The Limit",
         title="The Majestic Himalayas", short="The Majestic Himalayas", line="Drift over ancient monasteries while exploring your limits in thin air.",
         img="images/himalayas-1", alt="Paraglider over snow-capped Himalayan peaks", video="video/bir",
         next="21 to 30 Oct 2026", days="10 days", level=4, group="6 pilots", price="&pound;1,100",
         status="Guaranteed to run", go=True, href="destinations/india.html", cta="See dates", cta_href="#dates"),
    dict(key="kenya", place="Kenya", region="Kerio Valley, Rift Valley", kicker="Explore East Africa From Above",
         title="A Journey Over The Cradle Of Humankind", short="A Journey Over The Cradle Of Humankind", line="Glide over thousand year old baobabs, with zebras and giraffes below.",
         img="images/kenya-3", alt="Paraglider over a green Kenyan crater", video="",
         next="18 to 29 Jan 2027", days="12 days", level=2, group="8 pilots", price="US$2,100",
         status="Booking open", go=False, href="destinations/kenya.html", cta="See dates", cta_href="#dates"),
    dict(key="peru", place="Peru", region="Lima and the Andes", kicker="Planned for November 2027",
         title="A Multi-Day Soaring Adventure Through Iconic Flying Corridors", short="Soar The Land Of The Incas",
         line="Let the calm Pacific breezes carry you into long, graceful, and endlessly rewarding flights.",
         img="images/peru-1", alt="Paraglider above the Peruvian desert coastline", video="",
         next="November 2027", days=None, level=None, group=None, price=None,
         status="Register interest", go=False, href="enquire.html?trip=peru", cta="Register interest", cta_href="enquire.html?trip=peru"),
    dict(key="kazakhstan", place="Kazakhstan", region="The steppe", kicker="Planned for June 2027",
         title="Beyond Roads, Beyond Maps, Beyond The Unknown", short="Beyond Roads, Beyond Maps",
         line="Our Flagship Offering. Floating over a landscape untouched, unhurried, and utterly otherworldly.",
         img="images/kazakhstan-1", alt="Paragliders over striped canyon terrain in Kazakhstan", video="",
         next="June 2027", days=None, level=None, group=None, price=None,
         status="Register interest", go=False, href="enquire.html?trip=kazakhstan", cta="Register interest", cta_href="enquire.html?trip=kazakhstan"),
]

OPTIONS = [
    ("wings", "Wing panels", "Four tall photo panels. Point at one, or tap it, and it opens out with its dates and price. On a phone they stack and open downwards."),
    ("fly", "Fly-through", "One full-screen picture that changes as you scroll, with each trip's details written straight onto it. A small altimeter shows where you are."),
    ("swipe", "Swipe strip", "Wide, film-like slides you swipe or drag sideways, one trip at a time. Arrows and a progress line on desktop."),
    ("board", "Departure board", "One full-bleed stage and a board of four departures along the bottom. Choosing one changes the picture and the details."),
    ("mosaic", "Mosaic", "An uneven grid of pictures, India largest. The details slide up on hover; on a phone they are always shown."),
]


def pic(t, cls="", eager=False):
    lz = "" if eager else ' loading="lazy"'
    c = ' class="%s"' % cls if cls else ""
    return ('<picture%s><source srcset="%s%s.webp" type="image/webp"><img src="%s%s.jpg" alt="%s"%s></picture>'
            % (c, A, t["img"], A, t["img"], e(t["alt"]), lz))


def video(t):
    if not t["video"]:
        return ""
    return ('<video data-loop="%s%s" data-loop-size="720" muted loop playsinline preload="none" '
            'aria-hidden="true" tabindex="-1"></video>' % (A, t["video"]))


def meter(n):
    if n is None:
        return TBD
    segs = "".join('<i class="skill-seg%s"></i>' % (" filled" if k < n else "") for k in range(5))
    return '<b class="skill-meter" role="img" aria-label="Skill level %d of 5">%s</b>' % (n, segs)


def v(x):
    return x if x else TBD


def facts(t, cls="fo-facts"):
    if not t["price"]:   # the site gives only the month so far
        return ('<dl class="%s"><div><dt>Planned</dt><dd><b>%s</b></dd></div>'
                '<div><dt>Length, group, price</dt><dd>%s</dd></div></dl>' % (cls, t["next"], TBD))
    price = '<b class="v2-price">%s</b>' % t["price"] if t["price"] else "<b>%s</b>" % TBD
    return ('<dl class="%s">'
            '<div><dt>Next</dt><dd><b>%s</b></dd></div>'
            '<div><dt>Length</dt><dd><b>%s</b></dd></div>'
            '<div><dt>Level</dt><dd>%s</dd></div>'
            '<div><dt>Group</dt><dd><b>%s</b></dd></div>'
            '<div><dt>From</dt><dd>%s</dd></div></dl>'
            % (cls, t["next"], v(t["days"]), meter(t["level"]), v(t["group"]), price))


def lean_facts(t):
    """The four facts that decide a booking; the group size is in Every departure."""
    if not t["price"]:
        return ('<dl class="fo-facts"><div><dt>Planned</dt><dd><b>%s</b></dd></div>'
                '<div><dt>Details</dt><dd>%s</dd></div></dl>' % (t["next"], TBD))
    return ('<dl class="fo-facts"><div><dt>Next</dt><dd><b>%s</b></dd></div>'
            '<div><dt>Length</dt><dd><b>%s</b></dd></div>'
            '<div><dt>Level</dt><dd>%s</dd></div>'
            '<div><dt>From</dt><dd><b class="v2-price">%s</b></dd></div></dl>'
            % (t["next"], t["days"], meter(t["level"]), t["price"]))


def status(t):
    c = "is-go" if t["go"] else ("is-soon" if t["price"] is None else "")
    return '<span class="v2-status %s">%s</span>' % (c, t["status"])


def actions(t):
    more = '<a class="btn-lines" href="%s" data-hover>Learn More</a>' % t["href"] if t["price"] else ""
    return ('<div class="kit-actions fo-actions"><a class="btn-solid" href="%s" data-hover><span>%s</span></a>%s%s</div>'
            % (t["cta_href"], t["cta"], more, status(t) if t["price"] else ""))


# ---- 1. wing panels ---------------------------------------------------------
def opt_wings():
    out = []
    for i, t in enumerate(TRIPS):
        out.append(
            '<article class="fo1-p%s" data-key="%s">'
            '<div class="fo1-media">%s%s</div>'
            '<button type="button" class="fo1-tab" aria-expanded="%s" aria-controls="fo1-%s">'
            '<span class="fo1-n">0%d</span><span class="fo1-place">%s</span><span class="fo1-when">%s</span></button>'
            '<div class="fo1-body" id="fo1-%s">'
            '<span class="kit-kicker">%s</span><h3 class="fo-title">%s</h3><p class="fo-line">%s</p>%s%s</div>'
            '</article>'
            % (" is-open" if i == 0 else "", t["key"], pic(t), video(t), "true" if i == 0 else "false", t["key"],
               i + 1, t["place"], t["next"], t["key"], t["region"], t["title"], t["line"], facts(t), actions(t)))
    return '<div class="fo1" data-fo1>%s</div>' % "".join(out)


# ---- 2. fly-through ---------------------------------------------------------
def opt_fly():
    stage = "".join('<div class="fo2-shot%s" data-shot="%d">%s%s</div>'
                    % (" is-on" if i == 0 else "", i, pic(t), video(t)) for i, t in enumerate(TRIPS))
    alt = "".join('<li data-alt="%d"%s><i></i><span>%s</span></li>'
                  % (i, ' class="is-on"' if i == 0 else "", t["place"]) for i, t in enumerate(TRIPS))
    steps = "".join(
        '<div class="fo2-step" data-step="%d"><div class="fo2-card">'
        '<span class="kit-kicker">%s &middot; %s</span>'
        '<h3 class="fo-title">%s</h3>%s%s</div></div>'
        % (i, t["place"], t["region"], t["short"], lean_facts(t), actions(t)) for i, t in enumerate(TRIPS))
    return ('<div class="fo2" data-fo2><div class="fo2-stage" aria-hidden="true">%s<div class="fo2-shade"></div></div>'
            '<ol class="fo2-alt" aria-hidden="true">%s</ol><div class="fo2-steps">%s</div></div>' % (stage, alt, steps))


# ---- 3. swipe strip ---------------------------------------------------------
def opt_swipe():
    slides = "".join(
        '<article class="fo3-s" data-slide="%d">%s%s<div class="fo3-shade"></div>'
        '<span class="fo3-big" aria-hidden="true">0%d</span>'
        '<div class="fo3-body"><span class="kit-kicker">%s &middot; %s</span><h3 class="fo-title">%s</h3>%s%s</div></article>'
        % (i, pic(t), video(t), i + 1, t["place"], t["next"], t["title"], facts(t), actions(t)) for i, t in enumerate(TRIPS))
    return ('<div class="fo3" data-fo3><div class="fo3-rail" tabindex="0" aria-label="Expeditions, swipe sideways">%s</div>'
            '<div class="fo3-bar kit-in"><span class="fo3-count"><b>01</b> / 04</span><span class="fo3-prog"><i></i></span>'
            '<button type="button" class="fo3-btn" data-dir="-1" aria-label="Previous">&larr;</button>'
            '<button type="button" class="fo3-btn" data-dir="1" aria-label="Next">&rarr;</button></div></div>' % slides)


# ---- 4. departure board -----------------------------------------------------
def opt_board():
    shots = "".join('<div class="fo4-shot%s" data-shot="%d">%s%s</div>'
                    % (" is-on" if i == 0 else "", i, pic(t), video(t)) for i, t in enumerate(TRIPS))
    panes = "".join(
        '<div class="fo4-pane" role="tabpanel" id="fo4-p%d" aria-labelledby="fo4-t%d"%s>'
        '<span class="kit-kicker">%s</span><h3 class="fo-title">%s</h3><p class="fo-line">%s</p>%s%s</div>'
        % (i, i, "" if i == 0 else " hidden", t["region"], t["title"], t["line"], facts(t), actions(t))
        for i, t in enumerate(TRIPS))
    tabs = "".join(
        '<button type="button" role="tab" class="fo4-tab" id="fo4-t%d" aria-controls="fo4-p%d" aria-selected="%s" tabindex="%s">'
        '<span class="fo4-code">0%d</span><b>%s</b><span>%s</span><em>%s</em></button>'
        % (i, i, "true" if i == 0 else "false", "0" if i == 0 else "-1", i + 1, t["place"], t["next"],
           t["price"] or "Register interest") for i, t in enumerate(TRIPS))
    return ('<div class="fo4" data-fo4><div class="fo4-stage" aria-hidden="true">%s<div class="fo4-shade"></div></div>'
            '<div class="fo4-in kit-in"><div class="fo4-panes">%s</div>'
            '<div class="fo4-tabs" role="tablist" aria-label="Expeditions">%s</div></div></div>' % (shots, panes, tabs))


# ---- 5. mosaic --------------------------------------------------------------
def opt_mosaic():
    tiles = "".join(
        '<a class="fo5-t fo5-%s" href="%s">%s%s<div class="fo5-shade"></div>'
        '<div class="fo5-body"><span class="kit-kicker">%s &middot; %s</span><h3 class="fo-title">%s</h3>'
        '<div class="fo5-more"><div>%s%s<span class="fo5-go">%s <i aria-hidden="true">&rarr;</i></span></div></div></div></a>'
        % (t["key"], t["href"], pic(t), video(t), t["place"], t["next"], t["title"], facts(t),
           status(t), "Learn more" if t["price"] else "Register interest") for t in TRIPS)
    return '<div class="fo5 kit-in">%s</div>' % tiles


BUILD = dict(wings=opt_wings, fly=opt_fly, swipe=opt_swipe, board=opt_board, mosaic=opt_mosaic)

CSS = """
/* ---- five ways to show where we fly (this page only) ---- */
.fo-top{padding-top:calc(var(--sp-section) + 5rem);}
.fo-opt .kit-in,.fo-top .kit-in{box-sizing:border-box;padding-left:var(--gutter);padding-right:var(--gutter);max-width:calc(var(--measure) + 2 * var(--gutter));}
.fo-opt{--edge-x:max(var(--gutter),calc((100% - var(--measure)) / 2));}
.fo-opt :is(.fo1-body,.fo2-card,.fo3-body,.fo4-pane,.fo5-body){text-shadow:0 1px 12px rgba(20,21,25,.6);}
.fo-jump{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.4rem;}
.fo-jump a{display:inline-flex;align-items:center;gap:.5rem;min-height:44px;padding:.5rem 1rem;border:1px solid var(--edge);
  color:var(--white);text-decoration:none;font-size:var(--fs-small);transition:border-color .2s,background .2s;}
.fo-jump a b{color:var(--orange);font-family:var(--font-display);}
.fo-jump a:hover{border-color:var(--orange);background:var(--wash);}
.fo-opt{padding:var(--sp-section) 0;border-top:1px solid var(--line);}
.fo-label{display:flex;flex-wrap:wrap;align-items:baseline;gap:.4rem 1.2rem;margin-bottom:clamp(1.4rem,3vw,2.2rem);}
.fo-label .fo-num{font-family:var(--font-display);font-weight:700;font-size:clamp(2.4rem,5vw,3.6rem);line-height:1;
  color:transparent;-webkit-text-stroke:1px var(--orange);}
.fo-label h2{margin:0;font-size:clamp(1.5rem,3vw,2.1rem);}
.fo-label p{flex-basis:100%;margin:0;color:var(--gray-light);max-width:60ch;}
.fo-opt .fo-title{font-family:var(--font-display);font-weight:700;color:var(--white);font-size:clamp(1.35rem,2.4vw,2rem);line-height:1.15;margin:.35rem 0 .5rem;text-wrap:balance;}
.fo-line{color:var(--gray-light);margin:0 0 1.1rem;max-width:46ch;}
.fo-facts{display:flex;flex-wrap:wrap;gap:.9rem 1.6rem;margin:0 0 1.3rem;padding:.9rem 0;border-top:1px solid var(--edge);border-bottom:1px solid var(--edge);}
.fo-facts div{display:grid;gap:.25rem;}
.fo-facts dt{font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--orange);}
.fo-facts dd{margin:0;color:var(--white);}
.fo-actions{margin-top:0;align-items:center;}
.fo-opt picture,.fo-opt picture img{display:block;width:100%;height:100%;object-fit:cover;}
.fo-opt video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}

/* 1. wing panels */
.fo1{display:flex;gap:6px;height:min(86vh,800px);min-height:560px;padding:0 var(--edge-x);}
.fo1-p{position:relative;flex:1 1 0;min-width:0;overflow:hidden;background:var(--card);transition:flex-grow .7s var(--ease-out);}
.fo1-p.is-open{flex-grow:4.2;}
.fo1-media{position:absolute;inset:0;}
.fo1-media picture img{transition:scale 1.2s var(--ease-out),filter .7s;filter:saturate(.75) brightness(.7);}
.fo1-p.is-open .fo1-media picture img{scale:1.04;filter:none;}
.fo1-p::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,rgba(20,21,25,.35) 0%,rgba(20,21,25,.05) 25%,rgba(20,21,25,.55) 55%,rgba(20,21,25,.96) 100%);}
.fo1-tab{position:absolute;z-index:2;left:0;right:0;top:0;display:flex;flex-direction:column;align-items:flex-start;gap:.3rem;
  padding:1.4rem;background:none;border:0;color:var(--white);text-align:left;cursor:pointer;font:inherit;}
.fo1-n{font-family:var(--font-display);font-weight:700;font-size:1.6rem;color:transparent;-webkit-text-stroke:1px var(--orange);}
.fo1-place{font-family:var(--font-display);font-weight:700;font-size:1.25rem;}
.fo1-when{font-size:var(--fs-small);color:var(--gray-light);}
.fo1-body{position:absolute;z-index:2;left:0;bottom:0;width:min(100%,640px);padding:clamp(1.4rem,3vw,2.4rem);
  opacity:0;translate:0 24px;pointer-events:none;transition:opacity .45s,translate .6s var(--ease-out);}
.fo1-p.is-open .fo1-body{opacity:1;translate:0 0;pointer-events:auto;transition-delay:.25s;}
.fo1-p.is-open .fo1-when{opacity:0;}
@media (min-width:761px){
  .fo1-p:not(.is-open) .fo1-tab{top:auto;bottom:0;}
  .fo1-p:not(.is-open) .fo1-place{writing-mode:vertical-rl;rotate:180deg;font-size:1.5rem;}
}
@media (max-width:760px){
  .fo1{flex-direction:column;height:auto;min-height:0;padding:0;gap:4px;}
  .fo1-p{flex:none;height:112px;transition:height .6s var(--ease-out);}
  .fo1-p.is-open{height:min(640px,calc(100svh - 60px));}
  .fo1-tab{flex-direction:row;align-items:center;gap:.9rem;padding:1.1rem 1.25rem;}
  .fo1-when{margin-left:auto;}
  .fo1-body{width:100%;padding:1.25rem;}
  .fo1-body .fo-line{display:none;}
}

/* 2. fly-through */
.fo2{position:relative;overflow:clip;isolation:isolate;}
.fo2-stage{position:sticky;top:0;height:100vh;height:100svh;margin-bottom:-100vh;margin-bottom:-100svh;overflow:hidden;}
.fo2-shot{position:absolute;inset:0;opacity:0;transition:opacity 1s;}
.fo2-shot picture img{scale:1.08;transition:scale 6s linear;}
.fo2-shot.is-on{opacity:1;}
.fo2-shot.is-on picture img{scale:1;}
.fo2-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,21,25,.9) 0%,rgba(20,21,25,.6) 45%,rgba(20,21,25,.15) 100%),
  linear-gradient(180deg,var(--bg) 0%,rgba(20,21,25,0) 14%,rgba(20,21,25,0) 86%,var(--bg) 100%);}
.fo2-alt{position:sticky;top:50vh;z-index:2;float:right;margin:0 var(--gutter) 0 0;padding:0;list-style:none;translate:0 -50%;display:grid;gap:1.1rem;}
.fo2-alt li{display:flex;align-items:center;justify-content:flex-end;gap:.7rem;color:var(--gray-light);font-size:var(--fs-small);transition:color .4s;}
.fo2-alt li i{display:block;width:18px;height:1px;background:var(--edge-hi);transition:width .5s var(--ease-out),background .4s;}
.fo2-alt li.is-on{color:var(--white);}
.fo2-alt li.is-on i{width:44px;background:var(--orange);}
.fo2-steps{position:relative;z-index:1;}
.fo2-step{min-height:100vh;min-height:100svh;display:flex;align-items:center;padding:12vh var(--gutter);}
.fo2-card{max-width:760px;opacity:.2;translate:0 30px;transition:opacity .6s,translate .8s var(--ease-out);}
.fo-opt .fo2-card .fo-title{font-size:clamp(2rem,4.4vw,3.4rem);margin:.5rem 0 1.4rem;}
.fo2-card .fo-facts{gap:1rem clamp(1.4rem,3vw,2.6rem);}
.fo2-card .fo-facts dd b{font-size:clamp(1.05rem,1.5vw,1.3rem);}
.fo2-step.is-on .fo2-card{opacity:1;translate:0 0;}
@media (max-width:760px){
  .fo2-alt{display:none;}
  .fo2-shade{background:linear-gradient(180deg,var(--bg) 0%,rgba(20,21,25,.1) 16%,rgba(20,21,25,.75) 42%,rgba(20,21,25,.97) 66%);}
  .fo2-step{align-items:flex-end;padding:0 1rem 8vh;}
  .fo2-card .fo-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.9rem 1.2rem;}
}

/* 3. swipe strip */
.fo3-rail{display:grid;grid-auto-flow:column;grid-auto-columns:min(80vw,1180px);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;
  padding:0 var(--edge-x);scroll-padding:0 var(--edge-x);scrollbar-width:none;overscroll-behavior-x:contain;cursor:grab;}
.fo3-rail::-webkit-scrollbar{display:none;}
.fo3-rail.is-drag{cursor:grabbing;scroll-snap-type:none;}
.fo3-s{position:relative;scroll-snap-align:start;height:min(78vh,720px);min-height:520px;overflow:hidden;background:var(--card);}
.fo3-s picture img{transition:scale 1.4s var(--ease-out);scale:1.06;}
.fo3-s.is-on picture img{scale:1;}
.fo3-shade{position:absolute;inset:0;background:linear-gradient(0deg,rgba(20,21,25,.97) 0%,rgba(20,21,25,.75) 35%,rgba(20,21,25,.15) 70%,rgba(20,21,25,.3) 100%);}
.fo3-big{position:absolute;right:clamp(1rem,3vw,2.5rem);top:clamp(.5rem,2vw,1.5rem);font-family:var(--font-display);font-weight:700;
  font-size:clamp(5rem,14vw,12rem);line-height:1;color:transparent;-webkit-text-stroke:1px rgba(246,244,244,.45);pointer-events:none;}
.fo3-body{position:absolute;left:0;bottom:0;width:min(100%,760px);padding:clamp(1.3rem,3.5vw,3rem);
  opacity:.4;translate:0 16px;transition:opacity .5s,translate .7s var(--ease-out);}
.fo3-s.is-on .fo3-body{opacity:1;translate:0 0;}
.fo3-bar{display:flex;align-items:center;gap:1rem;margin-top:1.2rem;}
.fo3-count{font-family:var(--font-display);color:var(--gray-light);font-size:var(--fs-small);min-width:4.2em;}
.fo3-count b{color:var(--white);}
.fo3-prog{flex:1;height:1px;background:var(--edge);position:relative;}
.fo3-prog i{position:absolute;left:0;top:-1px;height:3px;width:25%;background:var(--orange);transition:width .4s var(--ease-out);}
.fo3-btn{width:48px;height:48px;border:1px solid var(--edge);background:none;color:var(--white);font-size:1.1rem;cursor:pointer;transition:border-color .2s,background .2s;}
.fo3-btn:hover{border-color:var(--orange);background:var(--wash);}
.fo3-btn:disabled{opacity:.3;cursor:default;}
@media (max-width:760px){
  .fo3-rail{grid-auto-columns:86vw;gap:10px;cursor:auto;}
  .fo3-s{height:auto;aspect-ratio:3/4.4;min-height:0;}
  .fo3-btn{display:none;}
  .fo3-body .fo-facts{gap:.7rem 1.1rem;}
  .fo3-body .fo-facts div:nth-child(3){display:none;}
}

/* 4. departure board */
.fo4{position:relative;min-height:min(92vh,860px);display:flex;overflow:hidden;}
.fo4-stage{position:absolute;inset:0;}
.fo4-shot{position:absolute;inset:0;opacity:0;transition:opacity .9s;}
.fo4-shot.is-on{opacity:1;}
.fo4-shot picture img{scale:1.06;transition:scale 8s ease-out;}
.fo4-shot.is-on picture img{scale:1;}
.fo4-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,21,25,.92) 0%,rgba(20,21,25,.55) 55%,rgba(20,21,25,.2) 100%),
  linear-gradient(180deg,var(--bg) 0%,rgba(20,21,25,0) 16%,rgba(20,21,25,0) 55%,rgba(20,21,25,.95) 100%);}
.fo4-in{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:space-between;gap:2rem;width:100%;padding-top:clamp(3rem,8vh,6rem);padding-bottom:clamp(1.5rem,4vh,2.5rem);}
.fo4-pane{max-width:600px;animation:fo4-in .7s var(--ease-out);}
@keyframes fo4-in{from{opacity:0;translate:0 18px;}to{opacity:1;translate:0 0;}}
.fo4-tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--edge);}
.fo4-tab{position:relative;display:grid;gap:.2rem;justify-items:start;padding:1.1rem 1.2rem 1.2rem;background:rgba(20,21,25,.35);
  border:0;border-right:1px solid var(--line);color:var(--gray-light);font:inherit;font-size:var(--fs-small);text-align:left;cursor:pointer;
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);transition:background .3s,color .3s;}
.fo4-tab:last-child{border-right:0;}
.fo4-tab::before{content:"";position:absolute;left:0;right:0;top:-1px;height:3px;background:var(--orange);scale:0 1;transform-origin:left;transition:scale .5s var(--ease-out);}
.fo4-tab b{font-family:var(--font-display);font-size:1.1rem;color:var(--white);}
.fo4-tab em{font-style:normal;color:var(--orange);}
.fo4-code{font-family:var(--font-display);font-size:var(--fs-micro);letter-spacing:.14em;}
.fo4-tab:hover{background:rgba(20,21,25,.6);}
.fo4-tab[aria-selected="true"]{background:rgba(20,21,25,.75);color:var(--white);}
.fo4-tab[aria-selected="true"]::before{scale:1 1;}
@media (max-width:760px){
  .fo4{min-height:0;}
  .fo4-in{padding:14rem 1rem 1rem;}
  .fo4-shade{background:linear-gradient(180deg,var(--bg) 0%,rgba(20,21,25,.1) 16%,rgba(20,21,25,.7) 36%,rgba(20,21,25,.97) 58%);}
  .fo4-pane .fo-line{display:none;}
  .fo4-tabs{grid-template-columns:repeat(2,minmax(0,1fr));}
  .fo4-tab:nth-child(2){border-right:0;}
  .fo4-tab:nth-child(-n+2){border-bottom:1px solid var(--line);}
}

/* 5. mosaic */
.fo5{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(2,minmax(280px,34vh)) minmax(300px,36vh);gap:10px;
  grid-template-areas:"in in ke" "in in ke" "pe kz kz";}
.fo5-india{grid-area:in;}.fo5-kenya{grid-area:ke;}.fo5-peru{grid-area:pe;}.fo5-kazakhstan{grid-area:kz;}
.fo5-t{position:relative;overflow:hidden;display:block;color:inherit;text-decoration:none;background:var(--card);isolation:isolate;}
.fo5-t picture img{transition:scale 1.2s var(--ease-out);}
.fo5-t:hover picture img,.fo5-t:focus-visible picture img{scale:1.05;}
.fo5-shade{position:absolute;inset:0;background:linear-gradient(0deg,rgba(20,21,25,.97) 0%,rgba(20,21,25,.6) 42%,rgba(20,21,25,.05) 78%);transition:background .5s;}
.fo5-t::after{content:"";position:absolute;inset:0;pointer-events:none;border:1px solid transparent;transition:border-color .3s;}
.fo5-t:hover::after,.fo5-t:focus-visible::after{border-color:var(--live);}
.fo5-body{position:absolute;left:0;right:0;bottom:0;padding:clamp(1.1rem,2.4vw,2rem);}
.fo5-t .fo-title{font-size:clamp(1.15rem,1.8vw,1.6rem);max-width:28ch;}
.fo5-india .fo-title{font-size:clamp(1.5rem,2.8vw,2.3rem);}
.fo5-more{display:grid;grid-template-rows:0fr;transition:grid-template-rows .55s var(--ease-out);}
.fo5-more>div{min-height:0;overflow:hidden;}
.fo5-t:hover .fo5-more,.fo5-t:focus-visible .fo5-more{grid-template-rows:1fr;}
.fo5-more .fo-facts{margin:.4rem 0 .9rem;}
.fo5-go{display:inline-flex;align-items:center;gap:.5rem;color:var(--orange);font-weight:600;margin-top:.4rem;}
.fo5-more .v2-status{margin-right:1rem;}
@media (hover:none),(max-width:760px){ .fo5-more{grid-template-rows:1fr;} }
@media (max-width:760px){
  .fo5{grid-template-columns:minmax(0,1fr);grid-template-rows:none;grid-template-areas:none;grid-auto-rows:auto;}
  .fo5-t{grid-area:auto;aspect-ratio:4/5;}
  .fo5-india{aspect-ratio:3/4;}
  .fo5-peru,.fo5-kazakhstan{aspect-ratio:1/1;}
  .fo5-peru .fo-facts,.fo5-kazakhstan .fo-facts{display:none;}
}

@media (prefers-reduced-motion:reduce){
  .fo-opt *,.fo-opt *::before{transition:none !important;animation:none !important;}
}
"""


def main():
    src = open(os.path.join(V2, "index.html"), encoding="utf-8").read()
    head = src[:src.index("</head>")]
    head = re.sub(r"<title>.*?</title>", "<title>Where we fly: five ways (v2 prototype)</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Five layouts for the homepage expedition block. Prototype, not linked.">', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    head = re.sub(r"<!-- site-schema -->.*?<!-- /site-schema -->", "", head, flags=re.S)
    head = head.replace('<link rel="canonical" href="https://paraglidingatlas.com/">', '<link rel="canonical" href="https://paraglidingatlas.com/">')
    body = src[src.index("<body>"):]
    nav = body[:body.index('<header class="kit-hero')]
    foot = body[body.index("<footer>"):body.index("</footer>") + len("</footer>")]

    jump = "".join('<a href="#fo-%s"><b>%d</b>%s</a>' % (k, i + 1, n) for i, (k, n, _) in enumerate(OPTIONS))
    opts = "".join(
        '<section class="fo-opt" id="fo-%s"><div class="kit-in fo-label"><span class="fo-num">0%d</span><h2>%s</h2><p>%s</p></div>%s</section>'
        % (k, i + 1, n, e(d), BUILD[k]()) for i, (k, n, d) in enumerate(OPTIONS))
    page = (head + "<style>" + CSS + "</style>\n</head>\n" + nav +
            '<main>\n<section class="kit-band fo-top"><div class="kit-in"><div class="kit-head">'
            '<span class="kit-kicker">Prototype &middot; not on the live site</span>'
            '<h1 class="kit-title">Where we fly, <em class="v2-accent">five ways</em></h1>'
            '<p class="kit-intro">The homepage block between &ldquo;See where we fly&rdquo; and &ldquo;Every departure&rdquo;. Same trips, same facts.</p>'
            '</div><nav class="fo-jump" aria-label="Options">' + jump + '</nav></div></section>\n' + opts +
            '\n<div id="dates"></div>\n</main>\n' + foot + "\n</div>\n"
            '<script src="../../script.js"></script>\n<script defer src="../../nav-menu.js"></script>\n'
            '<script src="fly-options.js"></script>\n</body>\n</html>\n')
    open(os.path.join(V2, "fly-options.html"), "w", encoding="utf-8").write(page)
    print("v2 fly options: %d layouts" % len(OPTIONS))


if __name__ == "__main__":
    main()
