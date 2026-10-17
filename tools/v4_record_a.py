#!/usr/bin/env python3
"""
The speed record attempt, told as a cinematic scroll story (owner, 17 Oct
2026: "The design feels very robotic, too much text, difficult to navigate,
make it stunning" and "Add elements which awwwards worthy websites use").

    prototypes/v4/record-a.html

Direction A, "Cinematic story": each screen carries one idea and very few
words, set big over full-bleed photography and dark space. Seven chapters
(the goal, the mark to beat, the course, the place, the window, the
audience, the offer), a slim chapter rail that shows where you are and jumps
between them, and the numbers as the heroes.

The facts are the ones tools/v4_record.py documents, and only those: the
FAI CIVL class O-3 speed records over a 100 km and a 200 km out-and-return
course; the 100 km mark (35.94 km/h, Michel Macquet, FRA, 23 Jan 2025,
status to confirm); the 200 km mark (to supply); the owner's 198.86 km flight
in Kenya on 6 Feb 2025 at about 36 km/h on a UP Trango X (EN C), logged on
XContest (UP Paragliders news), never called a record; Kerio Valley and its
season and air (the Kenya page); the window, 18 Jan to 12 Feb 2027, with the
two Kenya expeditions; the audience (the v4 partners page); the owner's
three partnership tiers. Anything unknown shows as [to supply] or
[to confirm].

The effects, each one in answer to the visitor and each with a still
fallback (reduced motion shows the finished state; with JavaScript off
everything is readable; phones get the simplest version):
  - kinetic type: the headlines rise word by word, line by line, once, as
    they come into view; the hero lifts away with the scroll;
  - the photograph seen through the letters of "Kerio Valley";
  - the course pinned while it is flown kilometre by kilometre with the
    scroll, the distance and two clocks counting alongside (100 or 200 km,
    both drawn to one scale);
  - the window as a horizontal film strip moved by the vertical scroll (a
    swipeable scroll-snap row on a phone);
  - the numbers count up once when they arrive (tabular figures);
  - photographs uncovered by a clip-path and drifting with the scroll
    (animation-timeline, transform only);
  - a ticker that moves only while the page scrolls;
  - a chapter rail with the reading progress, smooth jumps;
  - a ring cursor and magnetic buttons under a fine pointer only;
  - a still film grain over the dark chapters.

The page takes the v4 shell (head, menu, footer) from partners.html, as
tools/v4_record.py does. Prototype only; not linked from anywhere.

    python3 tools/v4_record_a.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "record-a.html")

TITLE = "The Speed Record Attempt"
DESC = ("Aninder Singh's attempt on two paragliding world records for speed, over a 100 km "
        "and a 200 km out-and-return course, from Kerio Valley, Kenya, between 18 January "
        "and 12 February 2027, and how to partner on it.")
URL = "https://paraglidingatlas.com/record-attempt.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/kenya/gallery/kenya-hero.jpg"

REC100 = 35.94      # km/h, the 100 km mark to beat, status to confirm
BEST = 36           # km/h, about, over 198.86 km (not a record course)

MAIL = "mailto:aninder@paraglidingatlas.com?subject=Partnering%20on%20the%20speed%20record%20attempt"
UP_NEWS = "https://www.up-paragliders.com/news/almost-200km-with-an-average-of-36kph"
FAI_LIST = "https://www.fai.org/page/civl-records"
FAI_CODE = "https://www.fai.org/sites/default/files/civl/documents/sporting_code_s7_d_-_records_and_badges_2025.pdf"

A = "../../assets/"
IMG = {
    "hero": (A + "destinations/kenya/gallery/kenya-hero", 1400, 788, "Paragliding in Kenya"),
    "kerio": (A + "destinations/kenya/hero/kerio-valley", 1152, 768, "Paragliding at Kerio Valley, Kenya"),
    "kerio_p": ("img/hero/kenya-kerio-valley-p", 512, 768, "Paragliding at Kerio Valley, Kenya"),
    "high": (A + "destinations/kenya/gallery/kenya-high", 1400, 933, "Paragliding in Kenya"),
    "aninder": (A + "images/partners-aninder", 720, 900, "Aninder Singh"),
    "icare": (A + "images/partners-coupe-icare-wide", 1920, 1372,
              "Aninder shaking hands with a brand representative at a harness test stand, "
              "camera in hand, at Coupe Icare"),
}

TBD = '<span class="wr-tbd">[to supply]</span>'
TBC = '<span class="wr-tbd">[to confirm]</span>'

# the course drawing: km out from the start to x in a 1000 x 200 box
X0, PX_PER_KM = 40, 9.2


def X(km):
    return X0 + km * PX_PER_KM


def hm(km, kmh):
    m = round(km / kmh * 60)
    return "%d h %02d min" % (m // 60, m % 60)


def pic(key, cls="", lazy=True, phone=None, fetch=False):
    base, w, h, alt = IMG[key]
    src = ""
    if phone:
        pb = IMG[phone][0]
        src += '<source media="(max-width: 560px)" srcset="%s.webp" type="image/webp">' % pb
    src += '<source srcset="%s.webp" type="image/webp">' % base
    att = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if fetch else "")
    return ('<picture%s>%s<img src="%s.jpg" width="%d" height="%d" alt="%s"%s></picture>'
            % (' class="%s"' % cls if cls else "", src, base, w, h, alt, att))


def kin(text):
    """A headline that rises word by word: each word in its own mask."""
    out = []
    for i, w in enumerate(text.split(" ")):
        out.append('<span class="wr-w"><span style="--i:%d">%s</span></span>' % (i, w))
    return " ".join(out)


def count(final, to, dec=0, comma=False, suf=""):
    return ('<span class="wr-count" data-final="%s" data-count="%s" data-dec="%d"%s%s><span>%s</span></span>'
            % (final, to, dec, ' data-comma="1"' if comma else "", ' data-suf="%s"' % suf if suf else "", final))


CSS = r"""
/* ===== The speed record attempt, cinematic (tools/v4_record_a.py) ===== */
.wr{--wr-top:92px;
  --wr-deep:color-mix(in srgb,var(--bg) 58%,var(--ink));
  --wr-shade:color-mix(in srgb,var(--bg) 84%,transparent);
  --wr-mega:min(calc(var(--fs-display) * 2.1),14.6vw);
  --wr-giga:min(calc(var(--fs-display) * 3.3),23vw);
  --wr-h2:calc(var(--fs-h1) * 1.2);
  --wr-pad:calc(var(--sp-section) * 1.7);
  --wr-x:var(--gutter);
  position:relative;overflow-x:clip;}
@media (max-width:560px){.wr,.wr-rail{--wr-x:var(--sp-2);}}
.wr-in{box-sizing:border-box;width:100%;max-width:var(--measure);margin:0 auto;padding-inline:var(--wr-x);}
.wr-tbd{font-style:italic;font-weight:400;color:var(--gray);white-space:nowrap;}

/* the chapter number, the headline, the one line under it */
.wr-no{display:flex;align-items:center;gap:var(--sp-2);margin:0 0 var(--sp-3);font-family:var(--font-mono);font-size:var(--fs-small);letter-spacing:.08em;color:var(--gray);}
.wr-no::after{content:"";flex:0 0 clamp(2.5rem,6vw,5rem);height:1px;background:var(--edge-hi);}
.wr-h2{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-h2);line-height:1.02;letter-spacing:-.035em;color:var(--white);text-wrap:balance;max-width:14ch;}
.wr-lede{margin:var(--sp-3) 0 0;max-width:31rem;font-size:var(--fs-lead);line-height:1.55;color:var(--gray-light);text-wrap:pretty;}

/* kinetic type: each word (or line) rises inside its own mask, once */
.wr-w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.12em;margin-bottom:-.12em;}
.wr-w>span,.wr-ln>span{display:inline-block;}
.wr-ln{display:block;overflow:hidden;padding-bottom:.07em;margin-bottom:-.07em;}
.wr-ln>span{display:block;}

/* links: the underline draws in under the pointer */
.wr-u{color:inherit;text-decoration:underline;text-decoration-color:var(--edge-hi);text-underline-offset:.22em;text-decoration-thickness:1px;
  background:linear-gradient(var(--orange),var(--orange)) 0 100%/0 1px no-repeat;padding-bottom:1px;
  transition:background-size .6s var(--ease),color .3s var(--ease),text-decoration-color .3s var(--ease);}
.wr-u:hover,.wr-u:focus-visible{color:var(--white);text-decoration-color:transparent;background-size:100% 1px;}
.wr :focus-visible{outline:2px solid var(--white);outline-offset:3px;}

/* still film grain over the dark chapters (an SVG noise, never animated) */
.wr-grain{position:relative;isolation:isolate;}
.wr-grain::after{content:"";position:absolute;inset:0;z-index:4;pointer-events:none;opacity:.32;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3CfeComponentTransfer%3E%3CfeFuncA type='linear' slope='.55'/%3E%3C/feComponentTransfer%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23g)'/%3E%3C/svg%3E");
  background-size:220px 220px;}

/* ---------- 01 the goal: the opening ---------- */
.wr-hero{position:relative;min-height:calc(100svh - var(--wr-top));display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;background:var(--bg);}
.wr-hero-pic{position:absolute;inset:0;z-index:-2;}
.wr-hero-pic img{width:100%;height:100%;object-fit:cover;object-position:66% 46%;}
.wr-hero::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:
  linear-gradient(90deg,color-mix(in srgb,var(--bg) 80%,transparent) 0%,color-mix(in srgb,var(--bg) 38%,transparent) 46%,transparent 72%),
  linear-gradient(180deg,color-mix(in srgb,var(--bg) 45%,transparent) 0%,transparent 24%,transparent 52%,var(--bg) 100%);}
.wr-hero-in{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;gap:var(--sp-5);padding-block:var(--sp-5) calc(var(--sp-section) * 1.15);}
.wr-kick{margin:0 0 var(--sp-3);text-wrap:balance;font-size:var(--fs-micro);font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--orange-lite);
  text-shadow:0 1px 2px color-mix(in srgb,var(--bg) 85%,transparent);}
.wr-mega{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-mega);line-height:.9;letter-spacing:-.045em;color:var(--white);}
.wr-mega .is-hollow{color:transparent;-webkit-text-stroke:max(1px,.011em) var(--white);}
.wr-hero-sub{margin:var(--sp-4) 0 0;max-width:27rem;font-size:var(--fs-lead);line-height:1.5;color:var(--gray-light);}
.wr-hero-meta{margin:0;display:grid;gap:var(--sp-3);min-width:13rem;padding:0 0 .3rem var(--sp-3);border-left:1px solid var(--edge-hi);}
.wr-hero-meta dt{font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray-light);}
.wr-hero-meta dd{margin:.25rem 0 0;font-family:var(--font-mono);font-size:var(--fs-body-s);color:var(--white);}
.wr-cue{position:absolute;left:50%;bottom:var(--sp-3);z-index:5;display:grid;place-items:center;width:44px;height:44px;margin-left:-22px;border-radius:50%;
  border:1px solid var(--edge-hi);color:var(--white);transition:border-color .4s var(--ease),background-color .4s var(--ease);}
.wr-cue:hover{border-color:var(--orange);background:var(--wash);}
.wr-cue svg{width:14px;height:14px;}

/* ---------- the ticker: moves only while the page scrolls ---------- */
.wr-tick{overflow:hidden;padding-block:clamp(1.1rem,2.6vw,2.2rem);border-block:1px solid var(--line);}
.wr-tick-in{display:flex;width:max-content;}
.wr-tick-in>span{display:flex;align-items:center;flex:none;white-space:nowrap;font-family:var(--font-display);font-weight:700;
  font-size:min(calc(var(--fs-display) * 1.45),15vw);line-height:1.02;letter-spacing:-.035em;color:transparent;-webkit-text-stroke:1px var(--edge-hi);}
.wr-tick em{font-style:normal;color:var(--white);-webkit-text-stroke:0;}
.wr-tick i{flex:none;width:.14em;height:.14em;margin:0 .5em;border-radius:50%;background:var(--orange);}

/* ---------- 02 the mark to beat ---------- */
.wr-mark{padding-block:var(--wr-pad);}
.wr-duel{display:grid;margin-top:var(--sp-5);}
.wr-big{min-width:0;}
.wr-big.is-mine{justify-self:end;text-align:right;margin-top:calc(var(--wr-giga) * -.2);}
.wr-cap{margin:0 0 .4rem;font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.wr-giga{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wr-giga);line-height:.84;letter-spacing:-.055em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.is-theirs .wr-giga{color:transparent;-webkit-text-stroke:max(1px,.005em) color-mix(in srgb,var(--white) 72%,transparent);}
.wr-giga small{font-size:.15em;font-weight:600;letter-spacing:0;margin-left:.35em;color:var(--gray-light);-webkit-text-stroke:0;}
.wr-meta{list-style:none;margin:var(--sp-3) 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.35rem 0;font-size:var(--fs-body-s);color:var(--gray-light);}
.wr-meta li{display:flex;align-items:center;}
.wr-meta li+li::before{content:"";width:4px;height:4px;border-radius:50%;background:var(--gray);margin:0 .75rem;}
.is-mine .wr-meta{justify-content:flex-end;}
.wr-meta b{font-weight:500;color:var(--white);}
.wr-also{margin:var(--sp-5) 0 0;padding-top:var(--sp-3);border-top:1px solid var(--line);font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
/* a number that counts keeps the width of its final value */
.wr-count{display:inline-grid;}
.wr-count>span,.wr-count::after{grid-area:1/1;}
.wr-count::after{content:attr(data-final);visibility:hidden;}
.is-mine .wr-count>span{text-align:right;}

/* ---------- 03 the course, pinned and flown ---------- */
.wr-course{background:var(--wr-deep);}
.wr-course .wr-stage{padding-block:var(--wr-pad);}
.wr-course-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:var(--sp-3) var(--sp-4);}
.wr-seg{display:inline-flex;gap:3px;padding:3px;border:1px solid var(--edge);}
.wr-seg button{min-height:44px;min-width:5.6rem;padding:0 1rem;border:0;background:transparent;color:var(--gray-light);
  font:600 var(--fs-body-s)/1 var(--font-body);cursor:pointer;transition:background-color .35s var(--ease),color .35s var(--ease);}
.wr-seg button:hover{color:var(--white);}
.wr-seg button[aria-pressed="true"]{background:var(--white);color:var(--bg);}
.wr-map{margin:clamp(3.2rem,8vh,5rem) 0 clamp(2rem,5vh,3.5rem);}
.wr-box{position:relative;}
.wr-box svg{display:block;width:100%;height:clamp(104px,20vh,190px);overflow:visible;}
.wr-lane{fill:none;stroke:var(--edge-hi);stroke-width:1;vector-effect:non-scaling-stroke;}
.wr-lane.is-far{stroke:var(--edge);stroke-dasharray:2 6;}
.wr-flown{fill:none;stroke:var(--orange);stroke-width:3;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;}
.wr-gate{stroke:var(--white);stroke-width:2;vector-effect:non-scaling-stroke;}
.wr-tk{stroke:var(--edge-hi);stroke-width:1;vector-effect:non-scaling-stroke;}
.wr-dot{position:absolute;left:4%;top:65%;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--orange);
  box-shadow:0 0 0 6px var(--wash),0 0 28px 4px color-mix(in srgb,var(--orange) 45%,transparent);}
.wr-map.is-live .wr-dot{left:0;top:0;will-change:transform;}
.wr-tp{position:absolute;top:0;bottom:0;width:0;transition:left .7s var(--ease);}
.wr-tp::after{content:"";position:absolute;left:-7px;top:calc(50% - 7px);width:14px;height:14px;box-sizing:border-box;border-radius:50%;border:1.5px solid var(--white);background:var(--wr-deep);}
.wr-pl{position:absolute;bottom:calc(100% + .7rem);left:0;white-space:nowrap;font-size:var(--fs-small);line-height:1.3;color:var(--white);}
.wr-pl i{display:block;font-style:normal;font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray-light);}
.wr-tp .wr-pl{transform:translateX(-50%);text-align:center;}
.is-k200 .wr-tp .wr-pl{transform:translateX(-100%);text-align:right;}
.wr-scale{position:relative;height:1.5em;margin-top:.7rem;font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray);}
.wr-scale span{position:absolute;top:0;transform:translateX(-50%);white-space:nowrap;}
.wr-scale span:first-child{transform:none;}
.wr-scale span:last-child{transform:translateX(-100%);}
.wr-read{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--sp-4);margin:0;padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.wr-read dt{font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray-light);}
.wr-read dd{margin:.55rem 0 0;font-family:var(--font-display);font-weight:600;font-size:calc(var(--fs-h2) * 1.25);line-height:1;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.wr-read dd small{font-size:.5em;font-weight:500;color:var(--gray-light);}
.wr-read dd .wr-tbd{font-size:.55em;}
.wr-read .is-mark dd{color:var(--gray-light);}
.wr-read .is-me dt::before{content:"";display:inline-block;width:6px;height:6px;margin-right:.45rem;border-radius:50%;background:var(--orange);vertical-align:middle;}

/* ---------- 04 the place ---------- */
.wr-place{padding-top:var(--wr-pad);}
.wr-cut{width:fit-content;max-width:100%;margin:0;font-family:var(--font-display);font-weight:700;font-size:min(calc(var(--fs-display) * 3),22vw);
  line-height:.86;letter-spacing:-.05em;color:var(--white);}
.wr-cut span{display:block;}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
  .wr-cut{color:transparent;background:url("../../assets/destinations/kenya/hero/kerio-valley.webp") 50% 58%/cover no-repeat;
    -webkit-background-clip:text;background-clip:text;filter:saturate(1.15) brightness(1.2);}
  .wr-js .wr-cut:not(.is-near){background-image:none;}
}
.wr-plate{position:relative;margin:var(--sp-5) 0 0;}
.wr-plate-img{position:relative;height:min(80svh,54rem);overflow:hidden;}
.wr-par{position:absolute;inset:0;}
.wr-par img{width:100%;height:100%;object-fit:cover;}
.wr-plate-img::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,var(--bg) 0%,transparent 22%,transparent 50%,color-mix(in srgb,var(--bg) 92%,transparent) 100%);}
.wr-facts{position:absolute;left:0;right:0;bottom:0;z-index:2;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-4);
  box-sizing:border-box;max-width:var(--measure);margin:0 auto;padding:0 var(--wr-x) var(--sp-5);}
.wr-facts div{padding-top:var(--sp-2);border-top:1px solid var(--edge-hi);}
.wr-facts dt{font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--gray-light);}
.wr-facts dd{margin:.45rem 0 0;font-size:var(--fs-body);line-height:1.35;color:var(--white);}

/* ---------- 05 the window: a film strip moved by the scroll ---------- */
.wr-win .wr-stage{padding-block:var(--wr-pad);}
.wr-win-in{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--sp-4);}
.wr-win .wr-h2{max-width:9ch;}
.wr-vp{min-width:0;}
.wr-track{display:flex;align-items:stretch;gap:0;}
.wr-steps{list-style:none;margin:0;padding:0;display:flex;}
.wr-step{position:relative;flex:0 0 min(21rem,72vw);box-sizing:border-box;padding:var(--sp-4) var(--sp-5) 0 0;border-top:1px solid var(--edge);}
.wr-step::before{content:"";position:absolute;left:0;top:-5px;width:9px;height:9px;box-sizing:border-box;border-radius:50%;background:var(--bg);border:1px solid var(--gray-light);}
.wr-step.is-win{border-top-color:var(--orange);}
.wr-step.is-win::before{background:var(--orange);border-color:var(--orange);box-shadow:0 0 0 5px var(--wash);}
.wr-when{display:block;margin:0 0 var(--sp-2);font-family:var(--font-mono);font-size:var(--fs-small);color:var(--gray-light);}
.is-win .wr-when{font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-h1) * .95);line-height:1;letter-spacing:-.035em;color:var(--white);}
.wr-step h3{margin:0;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);line-height:1.15;color:var(--white);}
.wr-step p{margin:.6rem 0 0;max-width:15rem;font-size:var(--fs-body-s);line-height:1.5;color:var(--gray-light);}
.wr-step h3 a{display:inline-flex;align-items:center;min-height:44px;}
.wr-step p a{display:inline-flex;align-items:center;min-height:44px;}
.wr-fig{position:relative;flex:0 0 min(19rem,64vw);margin:0 var(--sp-5) 0 0;overflow:hidden;align-self:stretch;min-height:16rem;}
.wr-fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:56% 50%;transition:transform 1.4s var(--ease);}
.wr-fig:hover img{transform:scale(1.05);}

/* ---------- 06 the audience ---------- */
.wr-aud{padding-block:var(--wr-pad);}
.wr-aud-in{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,.85fr);grid-template-areas:"copy pic" "stats pic";column-gap:clamp(2rem,6vw,6rem);}
.wr-aud-copy{grid-area:copy;}
.wr-portrait{grid-area:pic;position:relative;margin:calc(var(--sp-5) * 1.6) 0 0;align-self:start;aspect-ratio:4/5;overflow:hidden;}
.wr-portrait figcaption{position:absolute;left:var(--sp-3);bottom:var(--sp-3);z-index:1;font-family:var(--font-mono);font-size:var(--fs-micro);color:var(--white);
  text-shadow:0 1px 3px color-mix(in srgb,var(--bg) 90%,transparent);}
.wr-portrait::after{content:"";position:absolute;inset:55% 0 0;background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--bg) 70%,transparent));pointer-events:none;}
.wr-stats{grid-area:stats;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-5) var(--sp-4);margin:var(--sp-5) 0 0;}
.wr-stats div{display:flex;flex-direction:column-reverse;justify-content:flex-end;padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.wr-stats dd{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * .95);line-height:1;letter-spacing:-.04em;color:var(--white);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.wr-stats dt{margin-top:.6rem;font-size:var(--fs-body-s);color:var(--gray-light);}

/* ---------- 07 the offer ---------- */
.wr-offer{padding-block:var(--wr-pad) var(--sp-section);background:radial-gradient(70% 60% at 85% 0%,var(--sky-warm),transparent 70%);}
.wr-offer-head{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(2rem,6vw,6rem);align-items:end;}
.wr-offer-pic{position:relative;margin:0;aspect-ratio:4/3;overflow:hidden;}
.wr-offer-pic img{transition:transform 1.4s var(--ease);}
.wr-offer-pic:hover img{transform:scale(1.04);}
.wr-tiers{display:grid;grid-template-columns:minmax(0,1.2fr) repeat(2,minmax(0,1fr));gap:var(--sp-3);margin-top:var(--sp-5);}
.wr-tier{position:relative;padding:var(--sp-4);background:linear-gradient(180deg,color-mix(in srgb,var(--white) 6%,transparent),color-mix(in srgb,var(--white) 1.5%,transparent) 70%);
  transition:background-color .5s var(--ease);}
.wr-tier.is-lead{background:linear-gradient(180deg,color-mix(in srgb,var(--white) 9%,transparent),color-mix(in srgb,var(--white) 2%,transparent) 70%);}
.wr-tier::before{content:"";position:absolute;left:0;top:0;width:0;height:2px;background:var(--orange);transition:width .6s var(--ease);}
.wr-tier::after{content:"";position:absolute;left:0;top:0;width:2px;height:0;background:var(--orange);transition:height .6s var(--ease);}
.wr-tier:hover::before,.wr-tier:focus-within::before{width:3rem;}
.wr-tier:hover::after,.wr-tier:focus-within::after{height:3rem;}
.wr-tier-k{position:absolute;top:var(--sp-4);right:var(--sp-4);margin:0;padding:.2rem .5rem;border:1px solid var(--edge);font-family:var(--font-mono);font-size:var(--fs-micro);line-height:1.4;color:var(--gray-light);}
.wr-tier h3{margin:0 0 var(--sp-3);font-family:var(--font-display);font-weight:700;font-size:var(--fs-h3);line-height:1.1;color:var(--white);}
.wr-tier ul{list-style:none;margin:0;padding:0;display:grid;gap:.6rem;}
.wr-tier li{position:relative;padding-left:1.1rem;font-size:var(--fs-body-s);line-height:1.45;color:var(--gray-light);}
.wr-tier li::before{content:"";position:absolute;left:0;top:.62em;width:.45rem;height:2px;background:var(--orange);}
.wr-cta{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-3) var(--sp-5);margin-top:var(--sp-5);}
.wr-mag{display:inline-block;padding:16px;margin:-16px;transition:transform .7s var(--ease);}
.wr-cta .btn-solid{font-size:var(--fs-lead);padding:1.05rem 2.3rem;}
.wr-cta .btn-lines{display:inline-flex;align-items:center;min-height:48px;box-sizing:border-box;font-size:var(--fs-lead);}
.wr-cta .btn-lines:hover{color:var(--orange);border-color:var(--orange);}
.wr-src{margin:var(--sp-5) 0 0;font-size:var(--fs-small);line-height:1.8;color:var(--gray);}

/* ---------- image reveals and depth ---------- */
.wr-rv{clip-path:inset(0);}
.wr-par img,.wr-offer-pic img,.wr-portrait img{display:block;width:100%;height:100%;object-fit:cover;}

/* ---------- the chapter rail ---------- */
.wr-rail{position:fixed;z-index:30;}
.wr-rail ol{list-style:none;margin:0;padding:0;}
.wr-rail a{text-decoration:none;}
.wr-rail-bar{position:absolute;pointer-events:none;background:var(--orange);}
@media (min-width:1100px){
  .wr-rail{right:clamp(.4rem,1.2vw,1.4rem);top:50%;transform:translateY(-50%);transition:opacity .45s var(--ease);}
  .wr-rail ol{position:relative;}
  .wr-rail ol::before{content:"";position:absolute;right:21px;top:22px;bottom:22px;width:1px;background:var(--edge);}
  .wr-rail-bar{right:21px;top:22px;bottom:22px;width:1px;transform-origin:50% 0;transform:scaleY(var(--p,0));}
  .wr-rail a{position:relative;display:flex;align-items:center;justify-content:flex-end;height:44px;padding-right:44px;
    font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.05em;color:var(--gray-light);}
  .wr-rail a::after{content:"";position:absolute;right:18px;top:18px;width:7px;height:7px;border-radius:50%;background:var(--bg);border:1px solid var(--gray);
    transition:transform .45s var(--ease),background-color .45s var(--ease),border-color .45s var(--ease);}
  .wr-rail a span{padding:.25rem .55rem;background:var(--wr-shade);opacity:0;transform:translateX(.5rem);transition:opacity .35s var(--ease),transform .35s var(--ease);}
  .wr-rail a:hover span,.wr-rail a:focus-visible span,.wr-rail a[aria-current] span{opacity:1;transform:none;}
  .wr-rail a[aria-current]{color:var(--white);}
  .wr-rail a[aria-current]::after,.wr-rail a:hover::after{background:var(--orange);border-color:var(--orange);transform:scale(1.45);}
  .wr-rail.is-off,.wr-js .wr-rail:not(.is-on){opacity:0;pointer-events:none;}
}
@media (max-width:1099.98px){
  .wr-rail{left:0;right:0;bottom:0;background:var(--wr-shade);border-top:1px solid var(--edge);padding-bottom:env(safe-area-inset-bottom,0px);transition:transform .45s var(--ease);}
  @supports (backdrop-filter:blur(2px)){.wr-rail{-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);}}
  .wr-js .wr-rail:not(.is-on){transform:translateY(110%);}
  .wr-rail ol{display:flex;overflow-x:auto;scrollbar-width:none;padding:0 var(--sp-1);}
  .wr-rail ol::-webkit-scrollbar{display:none;}
  .wr-rail a{display:flex;align-items:center;gap:.5rem;min-height:48px;padding:0 .8rem;white-space:nowrap;font-size:var(--fs-small);color:var(--gray-light);}
  .wr-rail a::before{content:"";flex:none;width:6px;height:6px;border-radius:50%;background:var(--gray);}
  .wr-rail a[aria-current]{color:var(--white);}
  .wr-rail a[aria-current]::before{background:var(--orange);}
  .wr-rail-bar{left:0;right:0;top:-1px;height:2px;transform-origin:0 50%;transform:scaleX(var(--p,0));}
}

/* ---------- the ring cursor (fine pointers only; made by the script) ---------- */
.wr-cursor{position:fixed;left:0;top:0;z-index:250;width:0;height:0;pointer-events:none;opacity:0;transition:opacity .3s var(--ease);}
.wr-cursor.is-on{opacity:1;}
.wr-cursor i{position:absolute;left:-17px;top:-17px;width:34px;height:34px;box-sizing:border-box;border-radius:50%;border:1px solid color-mix(in srgb,var(--white) 55%,transparent);
  transition:transform .5s var(--ease),background-color .5s var(--ease),border-color .5s var(--ease);}
.wr-cursor.is-big i{transform:scale(1.75);background:color-mix(in srgb,var(--orange) 12%,transparent);border-color:var(--live);}
.wr-cursor.is-map i{transform:scale(2.5);background:transparent;border-color:color-mix(in srgb,var(--orange) 70%,transparent);}

/* ---------- motion: only where the visitor asked for none of it to be still ---------- */
@media (prefers-reduced-motion:no-preference){
  .wr-js .wr-k :is(.wr-w,.wr-ln)>span{transform:translateY(112%);transition:transform 1.05s var(--ease);transition-delay:calc(var(--i,0) * 70ms);}
  .wr-js .wr-k.is-in :is(.wr-w,.wr-ln)>span{transform:none;}
  .wr-js .wr-fade{opacity:0;transform:translateY(1.4rem);transition:opacity 1s var(--ease) .3s,transform 1s var(--ease) .3s;}
  .wr-js .wr-fade.is-in{opacity:1;transform:none;}
  .wr-js .wr-cut{transition:clip-path 1.3s var(--ease),transform 1.3s var(--ease);}
  .wr-js .wr-cut:not(.is-in){clip-path:inset(0 0 100% 0);transform:translateY(10%);}
  .wr-js .wr-rv{transition:clip-path 1.5s var(--ease);}
  .wr-js .wr-rv:not(.is-in){clip-path:inset(14% 9% 14% 9%);}
  .wr-js .wr-rv img{transition:transform 1.8s var(--ease);}
  .wr-js .wr-rv:not(.is-in) img{transform:scale(1.18);}
  html{scroll-behavior:smooth;}
}
@supports (animation-timeline:view()){
  @media (prefers-reduced-motion:no-preference){
    .wr-hero-pic{animation:wr-sink linear both;animation-timeline:view();animation-range:exit 0% exit 100%;}
    .wr-hero-in{animation:wr-lift linear both;animation-timeline:view();animation-range:exit 0% exit 100%;}
    @keyframes wr-sink{to{transform:translateY(16%) scale(1.06);}}
    @keyframes wr-lift{to{transform:translateY(-12vh);opacity:0;}}
    .wr-par{animation:wr-drift linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
    @keyframes wr-drift{from{transform:translateY(-7%) scale(1.15);}to{transform:translateY(7%) scale(1.15);}}
  }
}
@media (prefers-reduced-motion:reduce){
  .wr *,.wr-rail,.wr-rail *{transition:none !important;}
}

/* ---------- pinned chapters (set before the first paint by the script at the top of main) ---------- */
.wr-pin .wr-course{height:250vh;}
.wr-pin .wr-course .wr-stage{position:sticky;top:var(--wr-top);box-sizing:border-box;height:calc(100svh - var(--wr-top));padding-block:var(--sp-3);display:flex;align-items:center;}
.wr-hz .wr-win{height:300vh;}
.wr-hz .wr-win .wr-stage{position:sticky;top:var(--wr-top);box-sizing:border-box;height:calc(100svh - var(--wr-top));padding-block:var(--sp-4);display:flex;align-items:center;overflow:hidden;}

/* ---------- wide screens: the window's title holds while the strip passes ---------- */
@media (min-width:900px){
  .wr-win-in{grid-template-columns:minmax(0,22rem) minmax(0,1fr);gap:var(--sp-5);align-items:center;}
  :root:not(.wr-hz) .wr-track{flex-wrap:wrap;row-gap:var(--sp-5);}
  :root:not(.wr-hz) .wr-steps{flex:1 1 100%;}
  :root:not(.wr-hz) .wr-step{flex:1 1 0;}
  :root:not(.wr-hz) .wr-fig{flex:1 1 100%;height:16rem;margin:0;}
  :root:not(.wr-hz) .is-win .wr-when{font-size:var(--fs-h2);}
  .wr-hz .wr-vp{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,var(--bg) 4%,var(--bg) 92%,transparent);mask-image:linear-gradient(90deg,transparent,var(--bg) 4%,var(--bg) 92%,transparent);}
  .wr-hz .wr-track{padding:var(--sp-4) 0 var(--sp-2) var(--sp-4);width:max-content;will-change:transform;}
  .wr-hz .wr-fig{min-height:0;height:min(50svh,26rem);align-self:flex-start;}
  .wr-hz .wr-step{min-height:min(50svh,26rem);}
}

/* ---------- tablets and phones ---------- */
@media (max-width:899.98px){
  .wr-hero-in{grid-template-columns:minmax(0,1fr);gap:var(--sp-4);}
  .wr-hero-meta{grid-template-columns:repeat(2,minmax(0,1fr));border-left:0;padding:var(--sp-2) 0 0;border-top:1px solid var(--edge-hi);}
  .wr-big.is-mine{margin-top:var(--sp-5);}
  .wr-read{grid-template-columns:minmax(0,1fr);gap:0;}
  .wr-read div{display:flex;align-items:baseline;justify-content:space-between;gap:var(--sp-2);padding:.65rem 0;border-bottom:1px solid var(--line);}
  .wr-read dd{margin:0;font-size:calc(var(--fs-h2) * 1.05);}
  .wr-facts{position:static;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-3);padding-top:var(--sp-3);padding-bottom:0;}
  .wr-plate-img{height:62svh;}
  .wr-plate-img::after{background:linear-gradient(180deg,var(--bg) 0%,transparent 18%,transparent 75%,var(--bg) 100%);}
  .wr-vp{margin-inline:calc(var(--wr-x) * -1);}
  .wr-track{overflow-x:auto;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;scrollbar-width:none;padding:var(--sp-3) var(--wr-x) var(--sp-2);scroll-padding-inline:var(--wr-x);}
  .wr-track::-webkit-scrollbar{display:none;}
  .wr-step,.wr-fig{scroll-snap-align:start;}
  .wr-aud-in{grid-template-columns:minmax(0,1fr);grid-template-areas:"copy" "pic" "stats";}
  .wr-portrait{justify-self:end;width:min(62%,20rem);margin-top:var(--sp-4);}
  .wr-offer-head{grid-template-columns:minmax(0,1fr);}
  .wr-tiers{grid-template-columns:repeat(2,minmax(0,1fr));}
  .wr-tier.is-lead{grid-column:1/-1;}
}
@media (max-width:1099.98px){
  .wr-pin .wr-course .wr-stage{padding-bottom:calc(var(--sp-3) + 52px);}
  .wr-rail ol{-webkit-mask-image:linear-gradient(90deg,transparent,var(--bg) 1.25rem,var(--bg) calc(100% - 1.25rem),transparent);mask-image:linear-gradient(90deg,transparent,var(--bg) 1.25rem,var(--bg) calc(100% - 1.25rem),transparent);}
}
@media (max-width:560px){
  .wr-kick span{display:block;}
  .wr-kick .wr-sep{display:none;}
  .wr-hero-meta{grid-template-columns:minmax(0,1fr);}
  .wr-meta{flex-direction:column;gap:.25rem;}
  .wr-meta li+li::before{display:none;}
  .is-mine .wr-meta{align-items:flex-end;}
  .wr-map{margin:var(--sp-5) 0 var(--sp-3);}
  .wr-hero-sub{margin-top:var(--sp-3);}
  .wr-cue{display:none;}
  .wr-pin .wr-course{height:210vh;}
  .wr-course-head .wr-h2{font-size:calc(var(--fs-h1) * 1.05);}
  .wr-pl{font-size:var(--fs-micro);}
  .wr-facts{grid-template-columns:minmax(0,1fr);}
  .wr-stats{gap:var(--sp-4) var(--sp-3);}
  .wr-stats dd{font-size:calc(var(--fs-display) * .82);}
  .wr-tiers{grid-template-columns:minmax(0,1fr);}
  .wr-cta{flex-direction:column;align-items:flex-start;}
}
@media print{
  .wr-pin .wr-course,.wr-hz .wr-win{height:auto !important;}
  .wr .wr-stage{position:static !important;height:auto !important;}
  .wr-rail,.wr-tick,.wr-cursor,.wr-cue{display:none !important;}
  .wr-track{transform:none !important;flex-wrap:wrap;}
  .wr-cut{color:var(--white) !important;background:none !important;filter:none !important;}
}
"""


def hero():
    return """
<header class="wr-hero wr-grain" id="wr-goal">
  """ + pic("hero", "wr-hero-pic", lazy=False, fetch=True) + """
  <div class="wr-in wr-hero-in">
    <div>
      <p class="wr-kick"><span>World Record Attempt</span> <span class="wr-sep" aria-hidden="true">&middot;</span> <span>Kerio Valley, Kenya</span></p>
      <h1 class="wr-mega wr-k"><span class="wr-ln"><span style="--i:0">The Speed</span></span> <span class="wr-ln"><span class="is-hollow" style="--i:1">Record</span></span> <span class="wr-ln"><span style="--i:2">Attempt</span></span></h1>
      <p class="wr-hero-sub wr-fade">Two world records for speed: 100 km and 200 km, out and return.</p>
    </div>
    <dl class="wr-hero-meta wr-fade">
      <div><dt>Window</dt><dd>18 Jan to 12 Feb 2027</dd></div>
    </dl>
  </div>
  <a class="wr-cue" href="#wr-mark" aria-label="Go to the mark to beat"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1v11M2.5 7.5 7 12l4.5-4.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></a>
</header>
"""


def ticker():
    one = '<span>100 km<i></i>200 km<i></i><em>Kerio Valley</em><i></i></span>'
    return '\n<div class="wr-tick" aria-hidden="true"><div class="wr-tick-in">' + one + one + '</div></div>\n'


def mark():
    return """
<section class="wr-mark" id="wr-mark" aria-labelledby="wr-mark-h">
  <div class="wr-in">
    <p class="wr-no">02</p>
    <h2 class="wr-h2 wr-k" id="wr-mark-h">""" + kin("The Mark To Beat") + """</h2>
    <div class="wr-duel">
      <div class="wr-big is-theirs">
        <p class="wr-cap">100 km mark, class O-3</p>
        <p class="wr-giga">""" + count("35.94", REC100, 2) + """<small>km/h</small></p>
        <ul class="wr-meta"><li><b>Michel Macquet (FRA)</b></li><li>23 Jan 2025</li><li>Status&nbsp;""" + TBC + """</li></ul>
      </div>
      <div class="wr-big is-mine">
        <p class="wr-cap">My best average, about</p>
        <p class="wr-giga">""" + count("36", BEST) + """<small>km/h</small></p>
        <ul class="wr-meta"><li><b>198.86 km</b></li><li>Kenya, 6 Feb 2025</li><li>UP Trango X (EN C)</li><li>Not a record course</li></ul>
      </div>
    </div>
    <p class="wr-also">200 km mark: """ + TBD + """</p>
  </div>
</section>
"""


def course_svg():
    ticks = []
    for k in range(0, 101, 10):
        big = k % 50 == 0
        ticks.append('<line class="wr-tk" x1="%g" y1="%d" x2="%g" y2="200"/>' % (X(k), 184 if big else 192, X(k)))
    return (
        '<svg viewBox="0 0 1000 200" preserveAspectRatio="none" role="img" aria-labelledby="wrMapT">'
        '<title id="wrMapT">The 100 km and 200 km out-and-return courses drawn to one scale: out from the start '
        'to a turnpoint at half the distance, then straight back</title>'
        '<path class="wr-lane is-far" d="M%g 70H%gV130H%g"/>' % (X0, X(100), X0)
        + '<path class="wr-lane" id="wrLane" d="M%g 70H%gV130H%g"/>' % (X0, X(50), X0)
        + '<path class="wr-flown" id="wrFlown" d="M%g 70H%gV130H%g"/>' % (X0, X(50), X0)
        + "".join(ticks)
        + '<path class="wr-gate" d="M%g 50V150"/>' % X0
        + "</svg>"
    )


def course():
    pct = lambda km: "%g%%" % (X(km) / 10)
    return """
<section class="wr-course wr-grain" id="wr-course" aria-labelledby="wr-course-h">
  <div class="wr-stage">
    <div class="wr-in">
      <div class="wr-course-head">
        <div><p class="wr-no">03</p><h2 class="wr-h2 wr-k" id="wr-course-h">""" + kin("Out And Back, To Scale") + """</h2></div>
        <div class="wr-seg" role="group" aria-label="Course length"><button type="button" aria-pressed="true" data-km="100">100 km</button><button type="button" aria-pressed="false" data-km="200">200 km</button></div>
      </div>
      <div class="wr-map" data-cursor="map">
        <div class="wr-box">
          """ + course_svg() + """
          <span class="wr-pl" style="left:""" + pct(0) + """">Start, finish</span>
          <span class="wr-tp" id="wrTp" style="left:""" + pct(50) + """"><span class="wr-pl">Turnpoint<i id="wrTpKm">50 km out</i></span></span>
          <span class="wr-dot" id="wrDot" aria-hidden="true"></span>
        </div>
        <div class="wr-scale" aria-hidden="true"><span style="left:""" + pct(0) + """">0</span><span style="left:""" + pct(100) + """">100 km</span></div>
      </div>
      <dl class="wr-read">
        <div><dt>Flown</dt><dd><span id="wrKm">100</span> <small>km</small></dd></div>
        <div class="is-me"><dt>My best, 36 km/h</dt><dd id="wrT1">""" + hm(100, BEST) + """</dd></div>
        <div class="is-mark"><dt>The mark, """ + ("%.2f" % REC100) + """ km/h</dt><dd id="wrT2">""" + hm(100, REC100) + """</dd></div>
      </dl>
      <noscript><p class="wr-also">200 km: """ + hm(200, BEST) + """ at 36 km/h; at the mark """ + TBD + """</p></noscript>
    </div>
  </div>
</section>
"""


def place():
    return """
<section class="wr-place" id="wr-place" aria-labelledby="wr-place-h">
  <div class="wr-in">
    <p class="wr-no">04</p>
    <h2 class="wr-cut" id="wr-place-h"><span>Kerio</span> <span>Valley</span></h2>
    <p class="wr-lede wr-fade">Base of my Kenya expeditions, where world speed records are chased.</p>
  </div>
  <figure class="wr-plate">
    <div class="wr-plate-img wr-rv"><div class="wr-par">""" + pic("kerio", phone="kerio_p") + """</div></div>
    <dl class="wr-facts">
      <div><dt>Where</dt><dd>0.72&deg;N 35.65&deg;E</dd></div>
      <div><dt>Season</dt><dd>December to March</dd></div>
      <div><dt>Thermals</dt><dd>4 to 6 m/s; rare surges 6 to 7</dd></div>
      <div><dt>Flights</dt><dd>2 to 7 hours over the Rift Valley</dd></div>
    </dl>
  </figure>
</section>
"""


def window():
    # the timeline is also the media plan: before, during and after
    return """
<section class="wr-win" id="wr-window" aria-labelledby="wr-win-h">
  <div class="wr-stage">
    <div class="wr-in wr-win-in">
      <div class="wr-win-head">
        <p class="wr-no">05</p>
        <h2 class="wr-h2 wr-k" id="wr-win-h">""" + kin("18 Jan To 12 Feb 2027") + """</h2>
      </div>
      <div class="wr-vp">
        <div class="wr-track">
          <ol class="wr-steps">
            <li class="wr-step"><span class="wr-when">Before</span><h3>Preparation</h3><p>Wing, instruments, team, FAI observer """ + TBD + """</p></li>
            <li class="wr-step"><span class="wr-when">Before</span><h3>Build-Up Episodes</h3><p>Plus the newsletter</p></li>
          </ol>
          <figure class="wr-fig">""" + pic("high") + """</figure>
          <ol class="wr-steps" start="3">
            <li class="wr-step is-win"><span class="wr-when">18 to 29 Jan</span><h3><a class="wr-u" href="destinations/kenya.html">Expedition One</a></h3><p>Live tracking, daily updates</p></li>
            <li class="wr-step is-win"><span class="wr-when">1 to 12 Feb</span><h3><a class="wr-u" href="destinations/kenya.html">Expedition Two</a></h3></li>
            <li class="wr-step"><span class="wr-when">After</span><h3>The Claim</h3><p><a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">FAI Sporting Code, Section 7D</a></p></li>
            <li class="wr-step"><span class="wr-when">After</span><h3>The Film</h3><p>Debrief episode, flight data</p></li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def audience():
    return """
<section class="wr-aud" id="wr-audience" aria-labelledby="wr-aud-h">
  <div class="wr-in wr-aud-in">
    <div class="wr-aud-copy">
      <p class="wr-no">06</p>
      <h2 class="wr-h2 wr-k" id="wr-aud-h">""" + kin("Who Flies It With You") + """</h2>
      <p class="wr-lede wr-fade">Podcast, YouTube and a newsletter about four times a month.</p>
    </div>
    <figure class="wr-portrait wr-rv"><div class="wr-par">""" + pic("aninder") + """</div><figcaption>Aninder Singh</figcaption></figure>
    <dl class="wr-stats">
      <div><dt>Podcast streams</dt><dd>""" + count("100,000+", 100000, comma=True, suf="+") + """</dd></div>
      <div><dt>Countries reached</dt><dd>""" + count("130+", 130, suf="+") + """</dd></div>
      <div><dt>Long-form interviews</dt><dd>""" + count("80", 80) + """</dd></div>
      <div><dt>Years flying</dt><dd>""" + count("10+", 10, suf="+") + """</dd></div>
    </dl>
  </div>
</section>
"""


def offer():
    return """
<section class="wr-offer" id="wr-partner" aria-labelledby="wr-offer-h">
  <div class="wr-in">
    <div class="wr-offer-head">
      <div>
        <p class="wr-no">07</p>
        <h2 class="wr-h2 wr-k" id="wr-offer-h">""" + kin("Put Your Name On The Attempt") + """</h2>
        <p class="wr-lede wr-fade">Prices in the media kit, on request. Every sponsorship is <a class="wr-u" href="safety-and-disclosure.html">clearly marked as sponsored</a>.</p>
      </div>
      <figure class="wr-offer-pic wr-rv">""" + pic("icare") + """</figure>
    </div>
    <div class="wr-tiers">
      <article class="wr-tier is-lead">
        <p class="wr-tier-k">One only</p>
        <h3>Title Partner</h3>
        <ul><li>Your name in the attempt's title</li><li>Your mark on kit and camera</li><li>Sponsored build-up and debrief segments</li><li>First film credit</li><li>Logo on the live tracking page</li></ul>
      </article>
      <article class="wr-tier">
        <h3>Equipment Partner</h3>
        <ul><li>Your product used and shown</li><li>An honest, disclosed review</li><li>With my Kenya expedition pilots</li><li>Credits</li></ul>
      </article>
      <article class="wr-tier">
        <h3>Supporter</h3>
        <ul><li>Your name on this page</li><li>Newsletter and debrief thanks</li><li>Film credit</li></ul>
      </article>
    </div>
    <div class="wr-cta">
      <span class="wr-mag"><a class="btn-solid" href=\"""" + MAIL + """\"><span>Partner on the attempt</span></a></span>
      <span class="wr-mag"><a class="btn-lines" href="partners.html#pwForm">Other ways to work together</a></span>
    </div>
    <p class="wr-src">Sources: <a class="wr-u" href=\"""" + UP_NEWS + """\" target="_blank" rel="noopener">UP Paragliders</a>, <a class="wr-u" href=\"""" + FAI_LIST + """\" target="_blank" rel="noopener">FAI records</a>, <a class="wr-u" href=\"""" + FAI_CODE + """\" target="_blank" rel="noopener">Sporting Code 7D</a></p>
  </div>
</section>
"""


def rail():
    items = [("wr-goal", "Goal"), ("wr-mark", "Mark"), ("wr-course", "Course"), ("wr-place", "Place"),
             ("wr-window", "Window"), ("wr-audience", "Audience"), ("wr-partner", "Partner")]
    lis = "".join('<li><a href="#%s"><span>%s</span></a></li>' % (i, t) for i, t in items)
    return ('\n<div class="wr-rail" role="navigation" aria-label="Chapters"><ol>' + lis
            + '</ol><span class="wr-rail-bar" aria-hidden="true"></span></div>\n')


EARLY = ('<script>(function(r,m){r.classList.add("wr-js");if(!m("(prefers-reduced-motion: reduce)").matches)'
         '{r.classList.add("wr-pin");if(m("(min-width: 900px)").matches)r.classList.add("wr-hz");}})'
         '(document.documentElement,function(q){return window.matchMedia(q);});</script>')


def main_html():
    return ('<main id="v4-main" class="wr">\n' + EARLY + hero() + ticker() + mark() + course()
            + place() + window() + audience() + offer() + "\n</main>" + rail())


SCRIPT = r"""<script>
/* The speed record attempt (tools/v4_record_a.py). Every frame here is caused
   by a scroll, a pointer, a tap or a key, and stops when they do. Reduced
   motion: the finished state, nothing pinned, nothing counting. */
(function () {
  var d = document, w = window, root = d.documentElement;
  var main = d.getElementById("v4-main");
  if (!main || !main.classList.contains("wr")) return;
  var mq = function (q) { return w.matchMedia(q); };
  var still = mq("(prefers-reduced-motion: reduce)").matches;
  var IO = "IntersectionObserver" in w;
  var REC = @@REC@@, BEST = @@BEST@@, TBD = '<span class="wr-tbd">[to supply]</span>';
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function absTop(el) { return el.getBoundingClientRect().top + w.scrollY; }
  function hm(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + " h " + (m % 60 < 10 ? "0" : "") + (m % 60) + " min"; }
  function all(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }
  function showAll() { all(".wr-k,.wr-fade,.wr-rv,.wr-cut").forEach(function (el) { el.classList.add("is-in"); }); }

  try {
  /* 1. headlines, lines and photographs arrive once, as they come into view */
  var rv = all(".wr-k,.wr-fade,.wr-rv,.wr-cut");
  if (still || !IO) showAll();
  else {
    /* an element clipped shut to begin with has no area to intersect, so its
       parent is watched for it */
    var hosts = [];
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        ro.unobserve(e.target);
        hosts.forEach(function (h) { if (h[0] === e.target) h[1].classList.add("is-in"); });
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    rv.forEach(function (el) {
      var host = el.classList.contains("wr-cut") ? el.parentNode : el;
      hosts.push([host, el]); ro.observe(host);
    });
  }
  /* the photograph inside the letters loads only when its chapter is near */
  var cut = d.querySelector(".wr-cut");
  if (cut && IO) {
    var no = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { cut.classList.add("is-near"); no.disconnect(); } }, { rootMargin: "120% 0px 120% 0px" });
    no.observe(cut);
  } else if (cut) cut.classList.add("is-near");

  /* 2. the numbers count up once, in the display face, at their final width */
  function fmt(el, v) {
    var dec = +el.getAttribute("data-dec") || 0, s = v.toFixed(dec);
    if (el.hasAttribute("data-comma")) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return s + (el.getAttribute("data-suf") || "");
  }
  if (!still && IO) {
    var counts = all("[data-count]");
    counts.forEach(function (el) { el.firstElementChild.textContent = fmt(el, 0); });
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        co.unobserve(e.target);
        var el = e.target, to = +el.getAttribute("data-count"), t = el.firstElementChild, t0 = performance.now(), dur = 1700;
        (function step(now) {
          var p = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - p, 4);
          t.textContent = p < 1 ? fmt(el, to * k) : el.getAttribute("data-final");
          if (p < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: 0.6 });
    counts.forEach(function (el) { co.observe(el); });
  }

  /* 3. the course: 100 or 200 km on one scale, flown by the scroll */
  var C = d.getElementById("wr-course"), Cst = C.querySelector(".wr-stage"), map = C.querySelector(".wr-map");
  var box = C.querySelector(".wr-box svg"), flown = d.getElementById("wrFlown"), lane = d.getElementById("wrLane"), dot = d.getElementById("wrDot");
  var tp = d.getElementById("wrTp"), tpKm = d.getElementById("wrTpKm"), kmEl = d.getElementById("wrKm");
  var t1 = d.getElementById("wrT1"), t2 = d.getElementById("wrT2");
  var K = 100, F = 1, lastKm = -1, lastT = "";
  function X(km) { return @@X0@@ + km * @@PX@@; }
  var geo = { mapW: 1, mapH: 1 };
  function render(f) {
    F = f;
    var x0 = X(0), xT = X(K / 2), ts = 0.04, half = (1 - ts) / 2, x, y, km, dd;
    if (f <= half) { var u = f / half; x = x0 + (xT - x0) * u; y = 70; km = K / 2 * u; dd = "M" + x0 + " 70H" + x.toFixed(1); }
    else if (f <= half + ts) { var v = (f - half) / ts; x = xT; y = 70 + 60 * v; km = K / 2; dd = "M" + x0 + " 70H" + xT + "V" + y.toFixed(1); }
    else { var u2 = Math.min(1, (f - half - ts) / half); x = xT - (xT - x0) * u2; y = 130; km = K / 2 + K / 2 * u2; dd = "M" + x0 + " 70H" + xT + "V130H" + x.toFixed(1); }
    flown.setAttribute("d", dd);
    dot.style.transform = "translate(" + (x / 1000 * geo.mapW).toFixed(1) + "px," + (y / 200 * geo.mapH).toFixed(1) + "px)";
    var k = Math.round(km);
    if (k !== lastKm) { lastKm = k; kmEl.textContent = k; }
    var s1 = hm(km / BEST);
    if (s1 !== lastT) { lastT = s1; t1.textContent = s1; if (K === 100) t2.textContent = hm(km / REC); }
  }
  function setK(k) {
    K = k; lastKm = -1; lastT = "";
    all(".wr-seg button").forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-km") === k)); });
    lane.setAttribute("d", "M" + X(0) + " 70H" + X(k / 2) + "V130H" + X(0));
    tp.style.left = (X(k / 2) / 10) + "%";
    tpKm.textContent = (k / 2) + " km out";
    map.classList.toggle("is-k200", k === 200);
    if (k === 200) t2.innerHTML = TBD;
    render(F);
  }
  all(".wr-seg button").forEach(function (b) { b.addEventListener("click", function () { setK(+b.getAttribute("data-km")); }); });
  map.classList.add("is-live");

  /* 4. the window: a strip moved sideways by the vertical scroll (wide screens) */
  var W = d.getElementById("wr-window"), Wst = W.querySelector(".wr-stage"), Wvp = W.querySelector(".wr-vp"), Wtr = W.querySelector(".wr-track");
  var hzMq = mq("(min-width: 900px)");
  function hzOn() { return root.classList.contains("wr-hz"); }

  /* 5. the ticker, the rail */
  var tick = d.querySelector(".wr-tick-in"), tickBox = d.querySelector(".wr-tick");
  var railEl = d.querySelector(".wr-rail"), railOl = railEl && railEl.querySelector("ol"), bar = railEl && railEl.querySelector(".wr-rail-bar");
  var links = railEl ? all("a", railEl) : [], chaps = links.map(function (a) { return d.getElementById(a.getAttribute("href").slice(1)); });
  var foot = d.querySelector("footer"), hero = d.getElementById("wr-goal"), cur = -1;

  function measure() {
    var vh = w.innerHeight;
    var r = box.getBoundingClientRect(); geo.mapW = r.width; geo.mapH = r.height;
    var cTop = parseFloat(getComputedStyle(Cst).top) || 0;
    geo.cStart = absTop(C) - cTop; geo.cLen = Math.max(1, C.offsetHeight - Cst.offsetHeight);
    geo.pin = root.classList.contains("wr-pin");
    if (hzOn()) {
      W.style.height = "";
      geo.over = Math.max(0, Wtr.scrollWidth - Wvp.clientWidth);
      W.style.height = Math.round(Wst.offsetHeight + geo.over * 1.1 + vh * 0.2) + "px";
      geo.wStart = absTop(W) - (parseFloat(getComputedStyle(Wst).top) || 0);
      geo.wLen = Math.max(1, W.offsetHeight - Wst.offsetHeight);
    } else { W.style.height = ""; Wtr.style.transform = ""; }
    geo.seg = tick ? tick.firstElementChild.offsetWidth : 0;
    geo.tickTop = tickBox ? absTop(tickBox) : 0;
    geo.tops = chaps.map(function (c) { return c ? absTop(c) : 0; });
    geo.mainTop = absTop(main); geo.mainEnd = geo.mainTop + main.offsetHeight;
    geo.foot = foot ? absTop(foot) : 1e9;
    geo.heroEnd = hero ? absTop(hero) + hero.offsetHeight : 0;
    geo.vh = vh;
  }

  var queued = false;
  function frame() {
    queued = false;
    var y = w.scrollY, vh = geo.vh;
    if (geo.pin) {
      var p = clamp((y - geo.cStart) / geo.cLen);
      render(clamp((p - 0.04) / 0.86));
    }
    if (hzOn() && geo.over) {
      var q = clamp((y - geo.wStart) / geo.wLen);
      Wtr.style.transform = "translate3d(" + (-q * geo.over).toFixed(1) + "px,0,0)";
    }
    if (tick && !still && geo.seg && y + vh > geo.tickTop - 200 && y < geo.tickTop + 600) {
      tick.style.transform = "translate3d(" + (-((y * 0.55) % geo.seg)).toFixed(1) + "px,0,0)";
    }
    if (railEl) {
      var i = 0;
      for (var n = 0; n < geo.tops.length; n++) if (geo.tops[n] <= y + vh * 0.4) i = n;
      if (i !== cur) {
        cur = i;
        links.forEach(function (a, k) { if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
        if (railOl && railOl.scrollWidth > railOl.clientWidth) {
          var a = links[i].parentNode; railOl.scrollTo({ left: a.offsetLeft - 24, behavior: still ? "auto" : "smooth" });
        }
      }
      bar.style.setProperty("--p", clamp((y - geo.mainTop) / Math.max(1, geo.mainEnd - geo.mainTop - vh)).toFixed(4));
      var nearFoot = y + vh > geo.foot + vh * 0.15;
      railEl.classList.toggle("is-off", nearFoot);
      railEl.classList.toggle("is-on", y > geo.heroEnd - vh * 0.5 && !nearFoot);
    }
  }
  function onScroll() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  function refresh() { measure(); if (!geo.pin) render(1); frame(); }

  if (!geo.pin) render(1);
  measure(); frame();
  w.addEventListener("scroll", onScroll, { passive: true });
  var rz = 0;
  w.addEventListener("resize", function () { cancelAnimationFrame(rz); rz = requestAnimationFrame(refresh); }, { passive: true });
  w.addEventListener("load", refresh);
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(refresh);
  if (hzMq.addEventListener) hzMq.addEventListener("change", function (e) { if (!still) root.classList.toggle("wr-hz", e.matches); refresh(); });
  /* a key that moves into the strip brings its step on screen */
  Wtr.addEventListener("focusin", function (e) {
    if (!hzOn() || !geo.over) return;
    var item = e.target.closest(".wr-step,.wr-fig") || e.target;
    var q = clamp((item.offsetLeft - Wvp.clientWidth * 0.3) / geo.over);
    w.scrollTo(0, geo.wStart + q * geo.wLen);
  });

  /* 6. a ring cursor and magnetic buttons, under a fine pointer only */
  if (!still && mq("(hover: hover) and (pointer: fine)").matches) {
    var ring = d.createElement("div"); ring.className = "wr-cursor"; ring.setAttribute("aria-hidden", "true"); ring.innerHTML = "<i></i>";
    d.body.appendChild(ring);
    var cx = 0, cy = 0, craf = 0;
    function paint() { craf = 0; ring.style.transform = "translate3d(" + cx + "px," + cy + "px,0)"; }
    d.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      cx = e.clientX; cy = e.clientY; if (!craf) craf = requestAnimationFrame(paint);
      ring.classList.add("is-on");
      var t = e.target.closest ? e.target.closest("a,button,[data-cursor]") : null;
      ring.classList.toggle("is-big", !!t && !t.hasAttribute("data-cursor"));
      ring.classList.toggle("is-map", !!t && t.hasAttribute("data-cursor"));
    }, { passive: true });
    d.addEventListener("pointerleave", function () { ring.classList.remove("is-on"); });
    w.addEventListener("blur", function () { ring.classList.remove("is-on"); });
    all(".wr-mag").forEach(function (m) {
      m.addEventListener("pointermove", function (e) {
        var r = m.getBoundingClientRect();
        var dx = Math.max(-10, Math.min(10, (e.clientX - (r.left + r.width / 2)) * 0.12)), dy = Math.max(-6, Math.min(6, (e.clientY - (r.top + r.height / 2)) * 0.2));
        m.style.transform = "translate3d(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px,0)";
      });
      m.addEventListener("pointerleave", function () { m.style.transform = ""; });
    });
  }
  } catch (err) {
    root.classList.remove("wr-pin", "wr-hz");
    showAll();
  }
})();
</script>"""


def script():
    return (SCRIPT.replace("@@REC@@", repr(REC100)).replace("@@BEST@@", repr(BEST))
            .replace("@@X0@@", repr(X0)).replace("@@PX@@", repr(PX_PER_KM)))


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
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + CSS + "</style>\n", head, 1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    if ".wr-hero" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_record_a: the partners shell has changed; check the head")
    page = head + main_html() + tail.replace("</body>", script() + "\n</body>", 1)
    if "\u2014" in page:
        raise SystemExit("v4_record_a: an em dash crept in")
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_record_a: %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
