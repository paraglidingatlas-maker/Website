#!/usr/bin/env python3
"""
The speed record attempt, direction C: "Luxury editorial" (owner, 17 Oct
2026: "The design feels very robotic, too much text, difficult to navigate,
make it stunning" and "Add elements which awwwards worthy websites use").

    prototypes/v4/record-c.html

A sponsorship deck read like a luxury watch brand's: huge display type, a lot
of dark space, a few large photographs, numbers set as typography, one line
per section and the detail folded away. A quiet chapter bar (a dock at the
foot of a phone) keeps every chapter and the Partner button one tap away.

The facts are the ones tools/v4_record.py documents, and only those: the
FAI CIVL class O-3 speed records over a 100 km and a 200 km out-and-return
course; the 100 km mark (35.94 km/h, Michel Macquet, FRA, 23 Jan 2025, status
to confirm); the 200 km mark (to supply); the owner's 198.86 km flight in
Kenya on 6 Feb 2025 at about 36 km/h on a UP Trango X (EN C), logged on
XContest (UP Paragliders news), never called a record; Kerio Valley, its
season and its air (the Kenya page); the window, 18 Jan to 12 Feb 2027, with
the two Kenya expeditions; the audience (the v4 partners page); the owner's
three partnership tiers. Anything unknown shows as [to supply] or
[to confirm]. The times are distance over speed, rounded to the minute.

The effects, each one answering the visitor (scroll, pointer, tap, key) and
each with a still fallback: reduced motion shows the finished page, with
JavaScript off everything is there and readable, phones get the simplest
version.
  1. kinetic type: chapter titles rise word by word, once, as they arrive;
     "Kerio Valley" is set with the valley seen through its letters;
  2. the course, pinned on a wide screen and flown kilometre by kilometre
     with the scroll, both courses to one scale, a clock counting beside
     each (on a phone it is flown once when it comes into view);
  3. the partnership tiers as a horizontal row moved by the vertical scroll
     (wide screens with a mouse); a swipeable scroll-snap row on a phone;
  4. the record, the pace and the audience count up once when they arrive,
     in the display face with tabular figures;
  5. photographs uncovered by a clip-path as they enter and drifting at
     their own depth (animation-timeline: view(), transform only);
  6. a ring cursor on mouse screens that grows over what can be pressed and
     over the course, and call-to-action buttons that lean to the pointer;
  7. the chapter bar fills chapter by chapter as you read; anchor jumps are
     smooth (instant under reduced motion);
  8. a still film grain over the dark bands, asymmetric layouts where photo
     and type overlap, and underline and zoom micro-interactions on --ease.

The page takes the v4 shell (head, menu, footer) from partners.html, the way
tools/v4_record.py does, and is prototype-only.

    python3 tools/v4_record_c.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "partners.html")
OUT = os.path.join(V4, "record-c.html")

TITLE = "The Speed Record Attempt"
DESC = ("Aninder Singh's attempt on the paragliding world records for speed over a "
        "100 km and a 200 km out-and-return course, from Kerio Valley, Kenya, in "
        "January and February 2027. The marks, the course, the window, and how to partner on it.")
URL = "https://paraglidingatlas.com/record-attempt.html"
OG_IMG = "https://paraglidingatlas.com/assets/destinations/kenya/hero/kerio-valley.jpg"

REC100 = 35.94          # km/h, the 100 km mark, status to confirm
BEST = 36               # km/h, as reported, over 198.86 km

KENYA = "../../assets/destinations/kenya"
MAIL = "mailto:aninder@paraglidingatlas.com?subject=Partnering%20on%20the%20speed%20record%20attempt"
FAI_CODE = "https://www.fai.org/sites/default/files/civl/documents/sporting_code_s7_d_-_records_and_badges_2025.pdf"
FAI_LIST = "https://www.fai.org/page/civl-records"
UP_NEWS = "https://www.up-paragliders.com/news/almost-200km-with-an-average-of-36kph"

TBD = '<span class="wr-tbd">[to supply]</span>'
TBC = '<span class="wr-tbd">[to confirm]</span>'

CHAPTERS = [("record", "Record"), ("course", "Course"), ("valley", "Valley"),
            ("window", "Window"), ("audience", "Audience"), ("partner", "Partner")]


def mins(km, kmh):
    """The flying time in whole minutes."""
    return int(round(km / kmh * 60))


def clock(km, kmh):
    t = mins(km, kmh)
    return "%d<small>h</small> %02d<small>min</small>" % (t // 60, t % 60)


def rise(text, tag, cls, hid):
    """A title whose words rise once, one after another, as it arrives.
    Every word stays a word of the heading; '|' breaks the line."""
    out, i = [], 0
    for line in text.split("|"):
        ws = []
        for w in line.strip().split(" "):
            ws.append('<span class="w"><span style="--i:%d">%s</span></span>' % (i, w))
            i += 1
        out.append(" ".join(ws))
    return '<%s class="%s wrc-rise" id="%s">%s</%s>' % (tag, cls, hid, "<br>".join(out), tag)


def label(n, name):
    return '<p class="wrc-lab"><span>%02d</span>%s</p>' % (n, name)


GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E"
         "%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1.4 -.55'/%3E%3C/filter%3E"
         "%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E\")")

CSS = r"""
/* ===== The speed record attempt, C: luxury editorial (tools/v4_record_c.py) ===== */
.wrc{--wrc-navh:93px;--wrc-bar:60px;
  --wrc-mega:calc(var(--fs-display) * 2.05);
  --wrc-huge:calc(var(--fs-display) * 1.55);
  --wrc-big:calc(var(--fs-h1) * 1.1);
  --wrc-mono:var(--font-mono,var(--font-body));
  --wrc-shade:color-mix(in srgb,var(--bg) 84%,transparent);
  --wrc-grain:__GRAIN__;
  position:relative;overflow-x:clip;background:var(--bg);color:var(--gray-light);}
.wrc *,.wrc *::before,.wrc *::after{box-sizing:border-box;}
.wrc-in{width:100%;max-width:var(--measure);margin:0 auto;padding:0 var(--gutter);}
.wrc-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
.wr-tbd{font-style:italic;font-weight:400;color:var(--gray);white-space:nowrap;letter-spacing:0;}
.wrc a{color:inherit;}
.wrc :focus-visible{outline:2px solid var(--white);outline-offset:3px;}

/* type */
.wrc-kick{margin:0 0 1.4rem;color:var(--orange);font-size:var(--fs-micro);font-weight:600;letter-spacing:.2em;text-transform:uppercase;}
.wrc-lab{display:flex;align-items:baseline;gap:.9rem;margin:0 0 1.6rem;color:var(--gray);font-size:var(--fs-micro);font-weight:600;letter-spacing:.2em;text-transform:uppercase;}
.wrc-lab span{font-family:var(--wrc-mono);font-weight:400;letter-spacing:.05em;color:var(--gray-light);}
.wrc-lab::after{content:"";flex:0 0 3rem;height:1px;background:var(--edge-hi);align-self:center;order:-1;}
.wrc-h{margin:0;font-family:var(--font-display);font-weight:600;font-size:var(--wrc-big);line-height:1.02;letter-spacing:-.03em;color:var(--white);text-wrap:balance;}
.wrc-line.wrc-sub{margin-top:var(--sp-3);}
.wrc-line{margin:0;max-width:34rem;font-size:var(--fs-lead);line-height:1.6;color:var(--gray-light);text-wrap:pretty;}
.wrc-rise .w{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .04em .14em;margin:0 -.04em -.14em;}
.wrc-rise .w>span{display:inline-block;}
@media (prefers-reduced-motion:no-preference){
  .wrc-js .wrc-rise .w>span{transform:translateY(112%);transition:transform 1s var(--ease) calc(var(--i) * 70ms);}
  .wrc-js .wrc-rise.is-in .w>span{transform:none;}
}

/* bands */
.wrc-sec{position:relative;padding:calc(var(--sp-section) * 1.6) 0;scroll-margin-top:calc(var(--wrc-bar) + 1rem);}
.wrc-grain::after{content:"";position:absolute;inset:0;pointer-events:none;background-image:var(--wrc-grain);background-size:200px 200px;opacity:.07;z-index:0;
  -webkit-mask-image:linear-gradient(transparent,var(--bg) 18%,var(--bg) 82%,transparent);mask-image:linear-gradient(transparent,var(--bg) 18%,var(--bg) 82%,transparent);}
.wrc-grain>*{position:relative;z-index:1;}

/* buttons: the site's two kinds, solid (orange, skewed) and lines */
.wrc-btn{position:relative;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;gap:.6rem;min-height:52px;padding:0 1.7rem;
  font-family:var(--font-body);font-size:var(--fs-body-s);font-weight:600;letter-spacing:.02em;text-decoration:none;color:var(--white);
  transition:transform .45s var(--ease),color .3s var(--ease);will-change:transform;}
.wrc-btn.is-solid{color:var(--ink);}
.wrc-btn.is-solid::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--orange);transform:skewX(-10deg);transition:filter .3s var(--ease);}
.wrc-btn.is-solid:hover::before{filter:brightness(1.08);}
.wrc-btn.is-line{border-top:1px solid var(--edge-hi);border-bottom:1px solid var(--edge-hi);padding:0 .3rem;}
.wrc-btn.is-line::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;background:var(--orange);transform:scaleX(0);transform-origin:0 50%;transition:transform .5s var(--ease);}
.wrc-btn.is-line:hover::after,.wrc-btn.is-line:focus-visible::after{transform:scaleX(1);}
.wrc-btn svg{width:16px;height:16px;flex:none;transition:transform .45s var(--ease);}
.wrc-btn:hover svg{transform:translateX(4px);}
.wrc-link{text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;transition:background-size .5s var(--ease),color .3s var(--ease);padding-bottom:2px;}
.wrc-link:hover,.wrc-link:focus-visible{background-size:100% 1px;color:var(--white);}

/* folded detail */
.wrc-more{margin-top:var(--sp-4);border-top:1px solid var(--line);border-bottom:1px solid var(--line);max-width:46rem;}
.wrc-more summary{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:52px;cursor:pointer;list-style:none;color:var(--gray-light);font-size:var(--fs-small);font-weight:600;letter-spacing:.14em;text-transform:uppercase;}
.wrc-more summary::-webkit-details-marker{display:none;}
.wrc-more summary::after{content:"";width:11px;height:11px;flex:none;background:linear-gradient(currentColor,currentColor) 50% 50%/100% 1px no-repeat,linear-gradient(currentColor,currentColor) 50% 50%/1px 100% no-repeat;transition:transform .45s var(--ease);}
.wrc-more[open] summary::after{transform:rotate(45deg);}
.wrc-more summary:hover{color:var(--white);}
.wrc-more p{margin:0 0 1.1rem;font-size:var(--fs-body-s);line-height:1.65;color:var(--gray-light);max-width:44rem;}

/* ---------- the opening ---------- */
.wrc-hero{position:relative;min-height:max(600px,calc(100svh - var(--wrc-navh)));display:flex;align-items:flex-end;overflow:clip;isolation:isolate;}
.wrc-hero-media{position:absolute;inset:0;z-index:-2;overflow:hidden;}
.wrc-hero-media picture,.wrc-hero-media img{display:block;width:100%;height:100%;}
.wrc-hero-media img{object-fit:cover;object-position:60% 50%;}
.wrc-hero::before{content:"";position:absolute;inset:0;z-index:-1;
  background:linear-gradient(90deg,color-mix(in srgb,var(--bg) 82%,transparent) 0%,color-mix(in srgb,var(--bg) 35%,transparent) 55%,transparent 100%),
    linear-gradient(180deg,color-mix(in srgb,var(--bg) 40%,transparent) 0%,transparent 28%,transparent 52%,var(--bg) 100%);}
.wrc-hero::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background-image:var(--wrc-grain);background-size:200px 200px;opacity:.09;}
.wrc-hero-in{width:100%;max-width:var(--measure);margin:0 auto;padding:var(--sp-5) var(--gutter) clamp(2.5rem,7vh,4.5rem);}
.wrc-title{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--wrc-mega);line-height:.9;letter-spacing:-.045em;color:var(--white);}
.wrc-title .ln{display:block;}
.wrc-title .ln + .ln{padding-left:1.4em;}
.wrc-hero-foot{display:flex;justify-content:space-between;align-items:flex-end;gap:var(--sp-5);margin-top:clamp(1.8rem,4vh,2.8rem);padding-top:1.4rem;border-top:1px solid var(--edge);}
.wrc-hero-foot .wrc-line{max-width:31rem;color:var(--white);}
.wrc-spec{display:flex;gap:clamp(1.5rem,3vw,3rem);margin:0;}
.wrc-spec div{display:flex;flex-direction:column-reverse;gap:.35rem;}
.wrc-spec dt{color:var(--gray);font-size:var(--fs-micro);font-weight:600;letter-spacing:.2em;text-transform:uppercase;}
.wrc-spec dd{margin:0;font-family:var(--wrc-mono);font-size:var(--fs-body-s);color:var(--white);white-space:nowrap;}

/* ---------- the chapter bar (wide) and dock (phone) ---------- */
.wrc-bar{position:sticky;top:0;z-index:40;height:var(--wrc-bar);background:var(--wrc-shade);-webkit-backdrop-filter:blur(14px) saturate(1.1);backdrop-filter:blur(14px) saturate(1.1);
  border-bottom:1px solid var(--line);transition:translate .38s var(--ease);}
html.v2-nav-up .wrc-bar{translate:0 var(--v2-nav-h,var(--wrc-navh));}
.wrc-bar-in{height:100%;display:flex;align-items:center;gap:var(--sp-4);}
.wrc-bar-t{flex:none;font-family:var(--font-display);font-weight:600;font-size:var(--fs-body-s);color:var(--white);text-decoration:none;letter-spacing:-.01em;}
.wrc-bar ol{display:flex;gap:.2rem;margin:0 auto 0 -.8rem;padding:0;list-style:none;}
.wrc-bar ol a{position:relative;display:flex;align-items:center;gap:.5rem;min-height:44px;padding:0 .8rem;color:var(--gray);text-decoration:none;font-size:var(--fs-small);font-weight:500;transition:color .3s var(--ease);}
.wrc-bar ol a span{font-family:var(--wrc-mono);font-size:var(--fs-micro);}
.wrc-bar ol a i{position:absolute;left:.8rem;right:.8rem;bottom:6px;height:1px;background:var(--edge);overflow:hidden;}
.wrc-bar ol a i::after{content:"";position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--f,0));transform-origin:0 50%;}
.wrc-bar ol a:hover,.wrc-bar ol a[aria-current]{color:var(--white);}
.wrc-bar .wrc-btn{min-height:44px;padding:0 1.3rem;font-size:var(--fs-small);}
.wrc-dock{display:none;}

/* ---------- 01 the record ---------- */
.wrc-recs{margin-top:var(--sp-5);border-top:1px solid var(--edge);}
.wrc-rec{display:grid;grid-template-columns:minmax(0,13rem) minmax(0,1fr) minmax(0,17rem);gap:var(--sp-4);align-items:center;padding:clamp(1.4rem,3vw,2.4rem) 0;border-bottom:1px solid var(--line);}
.wrc-rec-k{margin:0;color:var(--gray);font-size:var(--fs-small);line-height:1.5;}
.wrc-rec-k b{display:block;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);color:var(--white);letter-spacing:-.01em;}
.wrc-num{margin:0;font-family:var(--font-display);font-weight:500;font-size:var(--wrc-huge);line-height:.92;letter-spacing:-.04em;color:var(--white);font-variant-numeric:tabular-nums;white-space:nowrap;}
.wrc-num .v{display:inline-block;}
.wrc-num small{font-size:.2em;font-weight:500;letter-spacing:.02em;color:var(--gray-light);margin-left:.5em;}
.wrc-num .wr-tbd{font-size:.34em;letter-spacing:0;}
.wrc-rec.is-me .wrc-num{color:var(--orange);}
.wrc-rec-v{margin:0;color:var(--gray-light);font-size:var(--fs-body-s);line-height:1.6;}
.wrc-rec-v b{color:var(--white);font-weight:500;}
.wrc-say{margin:var(--sp-5) 0 0;font-family:var(--font-display);font-weight:500;font-size:var(--fs-h2);line-height:1.2;letter-spacing:-.02em;color:var(--white);}
.wrc-say em{font-style:normal;color:var(--orange);font-variant-numeric:tabular-nums;}

/* ---------- 02 the course ---------- */
.wrc-course{background:radial-gradient(ellipse 70% 60% at 80% 40%,var(--sky-cool),transparent 70%),var(--bg);}
.wrc-stage{position:relative;}
.wrc-course-head{display:flex;justify-content:space-between;align-items:flex-end;gap:var(--sp-4);flex-wrap:wrap;}
.wrc-course-head .wrc-line{max-width:19rem;text-wrap:balance;}
.wrc-fly{position:relative;margin:var(--sp-5) 0 0;}
.wrc-km{display:none;}
.wrc-row,.wrc-scale{display:grid;grid-template-columns:minmax(0,9rem) minmax(0,1fr) minmax(0,13rem);gap:var(--sp-4);align-items:center;}
.wrc-row{padding:var(--sp-2) 0;transition:opacity .5s var(--ease);}
.wrc-row-k{margin:0;color:var(--gray);font-size:var(--fs-small);line-height:1.5;}
.wrc-row-k b{display:block;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h3);color:var(--white);}
.wrc-row-t{margin:0;text-align:right;color:var(--gray);font-size:var(--fs-micro);letter-spacing:.06em;}
.wrc-clock{display:block;font-family:var(--font-display);font-weight:500;font-size:var(--fs-h1);line-height:1;color:var(--white);font-variant-numeric:tabular-nums;letter-spacing:-.035em;white-space:nowrap;}
.wrc-clock small{font-size:.32em;font-weight:500;letter-spacing:.02em;color:var(--gray);margin:0 .35em 0 .2em;}
.wrc-clock small:last-child{margin-right:0;}
.wrc-row-d{position:relative;height:104px;}
.wrc-row-d svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;}
.wrc-row-d .g{fill:none;stroke:var(--edge);stroke-width:1.5;vector-effect:non-scaling-stroke;}
.wrc-row-d .t{fill:none;stroke:var(--white);stroke-width:2;stroke-linecap:round;vector-effect:non-scaling-stroke;}
.wrc-row[data-km="200"] .t{stroke:var(--orange);}
.wrc-row-d .s{stroke:var(--white);stroke-width:2;vector-effect:non-scaling-stroke;}
.wrc-tp{position:absolute;left:var(--x);top:-.4rem;transform:translateX(-50%);color:var(--gray);font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;}
.wrc-tp.is-end{transform:translateX(-80%);}
.wrc-gl{position:absolute;left:0;top:0;width:13px;height:13px;margin:-6.5px 0 0 -6.5px;border-radius:50%;background:var(--white);box-shadow:0 0 0 5px color-mix(in srgb,var(--white) 14%,transparent);opacity:0;transition:opacity .3s var(--ease);}
.wrc-row[data-km="200"] .wrc-gl{background:var(--orange);box-shadow:0 0 0 5px var(--wash);}
.is-live .wrc-gl{opacity:1;}
.wrc-scale{margin-top:var(--sp-1);}
.wrc-scale div{grid-column:2;position:relative;height:2.2rem;border-top:1px solid var(--line);}
.wrc-scale span{position:absolute;top:.55rem;left:var(--x);transform:translateX(-50%);font-family:var(--wrc-mono);font-size:var(--fs-micro);color:var(--gray);white-space:nowrap;}
.wrc-scale span:first-child{transform:none;}
.wrc-scale span:last-child{transform:translateX(-70%);}
.wrc-scale span::before{content:"";position:absolute;left:50%;top:-.6rem;width:1px;height:.4rem;background:var(--edge-hi);}
.wrc-scale span:first-child::before{left:0;}
.wrc-fly figcaption{position:absolute;left:0;bottom:.35rem;width:9rem;color:var(--gray);font-size:var(--fs-small);line-height:1.4;}
.wrc-course.is-pin{padding:0;height:290vh;}
.wrc-course.is-pin .wrc-stage{position:sticky;top:0;height:100vh;min-height:620px;display:flex;align-items:center;padding-top:var(--wrc-bar);overflow:clip;}
.wrc-course.is-pin .wrc-km{display:block;position:absolute;left:0;right:0;bottom:-.14em;margin:0;padding:0 var(--gutter);text-align:right;pointer-events:none;white-space:nowrap;
  font-family:var(--font-display);font-weight:700;font-size:min(30vh,calc(var(--wrc-mega) * 1.7));line-height:.8;letter-spacing:-.06em;color:transparent;
  -webkit-text-stroke:1px color-mix(in srgb,var(--white) 10%,transparent);font-variant-numeric:tabular-nums;z-index:0;}
.wrc-course.is-pin .wrc-km small{font-size:.2em;letter-spacing:0;margin-left:.15em;}
.wrc-course.is-pin .wrc-stage .wrc-in{position:relative;z-index:1;}
.wrc-course.is-pin .wrc-row:not(.is-on){opacity:.4;}

/* ---------- 03 the valley ---------- */
.wrc-valley{padding-bottom:calc(var(--sp-section) * 1.4);}
.wrc-cut{margin:0;padding-bottom:.06em;font-family:var(--font-display);font-weight:800;font-size:calc((min(100vw,var(--measure)) - 2 * var(--gutter)) / 5.95);line-height:.9;letter-spacing:-.055em;color:var(--white);white-space:nowrap;}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
  .wrc-cut{color:transparent;background:url("../../assets/destinations/kenya/hero/kerio-valley.webp") 30% 26%/115% auto no-repeat,var(--gray-light);-webkit-background-clip:text;background-clip:text;}
}
.wrc-valley-grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:clamp(2rem,5vw,5rem);align-items:end;margin-top:var(--sp-5);}
.wrc-ph{position:relative;margin:0;overflow:hidden;background:var(--card);}
.wrc-ph img{display:block;width:100%;height:100%;object-fit:cover;transition:scale 1.2s var(--ease);}
.wrc-valley .wrc-ph{aspect-ratio:16/10;margin-left:calc(-1 * (max(0px,(100vw - var(--measure)) / 2) + var(--gutter)));}
.wrc-valley-copy{padding-bottom:var(--sp-2);}
.wrc-facts{margin:var(--sp-4) 0 0;border-top:1px solid var(--edge);}
.wrc-facts div{display:grid;grid-template-columns:6.5rem minmax(0,1fr);gap:1rem;padding:.85rem 0;border-bottom:1px solid var(--line);font-size:var(--fs-body-s);line-height:1.5;}
.wrc-facts dt{color:var(--gray);font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;padding-top:.2em;}
.wrc-facts dd{margin:0;color:var(--white);}
.wrc-facts .m{font-family:var(--wrc-mono);}

/* ---------- 04 the window ---------- */
.wrc-when{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2.2fr) minmax(0,1fr);margin-top:var(--sp-5);border-top:1px solid var(--edge);}
.wrc-when>div{padding:var(--sp-3) var(--sp-3) 0 0;}
.wrc-when>div + div{padding-left:var(--sp-3);border-left:1px solid var(--line);}
.wrc-when h3{margin:0 0 .5rem;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);color:var(--white);}
.wrc-when p{margin:0;font-size:var(--fs-body-s);line-height:1.55;color:var(--gray-light);}
.wrc-days{display:flex;justify-content:space-between;align-items:flex-end;height:58px;margin:var(--sp-4) 0 .7rem;}
.wrc-days i{flex:none;width:2px;height:100%;background:var(--orange);transform-origin:50% 100%;transition:transform .8s var(--ease) calc(var(--d) * 30ms),background-color .8s var(--ease) calc(var(--d) * 30ms);}
.wrc-days i.o{height:28%;background:var(--edge-hi);}
@media (prefers-reduced-motion:no-preference){
  .wrc-js .wrc-days:not(.is-in) i{transform:scaleY(.06);background:var(--edge);}
}
.wrc-days-l{position:relative;height:1.3em;font-family:var(--wrc-mono);font-size:var(--fs-micro);color:var(--gray);}
.wrc-days-l span{position:absolute;top:0;left:var(--x);white-space:nowrap;}
.wrc-days-l span.r{transform:translateX(-100%);}
.wrc-open{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--sp-3);margin:var(--sp-5) 0 0;padding:0;list-style:none;}
.wrc-open li{padding-top:.9rem;border-top:1px solid var(--line);font-size:var(--fs-small);line-height:1.5;color:var(--gray);}
.wrc-open li b{display:block;color:var(--white);font-weight:500;font-size:var(--fs-body-s);margin-bottom:.15rem;}

/* ---------- 05 the audience ---------- */
.wrc-aud{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(2rem,6vw,6rem);align-items:center;}
.wrc-portrait{aspect-ratio:4/5;max-width:30rem;}
.wrc-portrait figcaption{position:absolute;left:1rem;bottom:.9rem;color:var(--white);font-size:var(--fs-small);font-weight:500;}
.wrc-portrait::after{content:"";position:absolute;inset:60% 0 0;background:linear-gradient(transparent,color-mix(in srgb,var(--bg) 88%,transparent));pointer-events:none;}
.wrc-portrait figcaption{z-index:1;}
.wrc-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));margin:var(--sp-5) 0 var(--sp-4);border-top:1px solid var(--edge);}
.wrc-stats div{display:flex;flex-direction:column-reverse;gap:.5rem;padding:1.4rem 0 1.5rem;border-bottom:1px solid var(--line);}
.wrc-stats div:nth-child(odd){padding-right:var(--sp-3);border-right:1px solid var(--line);}
.wrc-stats div:nth-child(even){padding-left:var(--sp-4);}
.wrc-stats dt{color:var(--gray);font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;}
.wrc-stats dd{margin:0;font-family:var(--font-display);font-weight:500;font-size:calc(var(--fs-h1) * 1.05);line-height:1;letter-spacing:-.035em;color:var(--white);font-variant-numeric:tabular-nums;}
.wrc-stats dd .v{display:inline-block;}

/* ---------- 06 partner: the tiers ---------- */
.wrc-partner{padding:calc(var(--sp-section) * 1.6) 0;}
.wrc-hz-track{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--sp-3);}
.wrc-hz-intro{margin-bottom:var(--sp-5);}
.wrc-hz-intro .wrc-line{margin-top:var(--sp-3);}
.wrc-tier{position:relative;display:flex;flex-direction:column;min-height:27rem;padding:clamp(1.6rem,2.6vw,2.4rem);overflow:hidden;
  background:linear-gradient(180deg,color-mix(in srgb,var(--card) 92%,var(--white)) 0%,var(--card) 40%,color-mix(in srgb,var(--card) 70%,var(--bg)) 100%);
  border-top:1px solid var(--edge-hi);transition:transform .6s var(--ease);}
.wrc-tier.is-lead{border-top-color:var(--orange);}
.wrc-tier-n{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * 1.5);line-height:.9;color:transparent;-webkit-text-stroke:1px var(--edge-hi);letter-spacing:-.04em;}
.wrc-tier.is-lead .wrc-tier-n{-webkit-text-stroke-color:var(--live);}
.wrc-tier-tag{position:absolute;top:clamp(1.6rem,2.6vw,2.4rem);right:clamp(1.6rem,2.6vw,2.4rem);color:var(--gray-light);font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;}
.wrc-tier h3{margin:clamp(3rem,9vh,6rem) 0 var(--sp-3);font-family:var(--font-display);font-weight:600;font-size:var(--fs-h2);line-height:1.1;letter-spacing:-.02em;color:var(--white);}
.wrc-tier-one{margin:0 0 var(--sp-3);color:var(--gray-light);font-size:var(--fs-body-s);}
.wrc-tier ul{margin:0;padding:0;list-style:none;border-top:1px solid var(--line);}
.wrc-tier li{padding:.6rem 0;border-bottom:1px solid var(--line);font-size:var(--fs-small);line-height:1.45;color:var(--gray-light);}
.wrc-hz-prog{display:none;}
.wrc-hz.is-pin .wrc-hz-stage{position:sticky;top:0;height:100vh;min-height:640px;overflow:clip;display:flex;flex-direction:column;justify-content:center;padding-top:var(--wrc-bar);}
.wrc-hz.is-pin .wrc-hz-track{display:flex;gap:var(--sp-3);width:max-content;max-width:none;margin:0;padding:0 max(var(--gutter),calc((100vw - var(--measure)) / 2 + var(--gutter)));will-change:transform;}
.wrc-hz.is-pin .wrc-hz-intro{flex:0 0 min(32rem,38vw);margin:0 var(--sp-5) 0 0;padding:0;align-self:center;}
.wrc-hz.is-pin .wrc-tier{flex:0 0 min(27rem,32vw);min-height:min(31rem,58vh);}
.wrc-hz.is-pin .wrc-hz-prog{display:block;position:relative;width:min(20rem,40vw);height:1px;margin:var(--sp-4) 0 0 max(var(--gutter),calc((100vw - var(--measure)) / 2 + var(--gutter)));background:var(--edge);}
.wrc-hz-prog i{position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--p,0));transform-origin:0 50%;}

/* ---------- the close ---------- */
.wrc-end{position:relative;isolation:isolate;overflow:clip;min-height:min(92vh,880px);display:flex;align-items:flex-end;padding:calc(var(--sp-section) * 2) 0 var(--sp-section);}
.wrc-end-media{position:absolute;inset:0;z-index:-2;margin:0;}
.wrc-end-media img{display:block;width:100%;height:100%;object-fit:cover;object-position:62% 40%;}
.wrc-end::before{content:"";position:absolute;inset:0;z-index:-1;
  background:linear-gradient(180deg,var(--bg) 0%,color-mix(in srgb,var(--bg) 50%,transparent) 26%,color-mix(in srgb,var(--bg) 62%,transparent) 60%,var(--bg) 100%),
    linear-gradient(90deg,color-mix(in srgb,var(--bg) 80%,transparent),color-mix(in srgb,var(--bg) 30%,transparent) 62%,transparent 85%);}
.wrc-end::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background-image:var(--wrc-grain);background-size:200px 200px;opacity:.08;}
.wrc-end .wrc-h{font-size:var(--wrc-huge);max-width:12ch;letter-spacing:-.045em;line-height:.95;}
.wrc-cta{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-3) var(--sp-4);margin-top:var(--sp-5);}
.wrc-end .wrc-line{margin-top:var(--sp-4);color:var(--gray-light);font-size:var(--fs-body-s);}
.wrc-end .wrc-more{margin-top:var(--sp-3);}

/* ---------- the cursor (mouse screens only, made by the script) ---------- */
.wrc-cur{position:fixed;left:0;top:0;z-index:90;width:34px;height:34px;margin:-17px 0 0 -17px;pointer-events:none;opacity:0;transition:opacity .3s var(--ease);}
.wrc-cur i{display:block;width:100%;height:100%;border:1px solid color-mix(in srgb,var(--white) 70%,transparent);border-radius:50%;transition:transform .45s var(--ease),border-color .3s var(--ease),background-color .3s var(--ease);}
.wrc-cur.is-on{opacity:1;}
.wrc-cur.is-big i{transform:scale(1.9);border-color:color-mix(in srgb,var(--white) 85%,transparent);background:color-mix(in srgb,var(--white) 6%,transparent);}

/* ---------- hover (mouse) ---------- */
@media (hover:hover) and (pointer:fine){
  .wrc-ph:hover img{scale:1.04;}
  .wrc-tier:hover{transform:translateY(-6px);}
}

/* ---------- motion with the scroll (still where it is not supported or not wanted) ---------- */
@supports (animation-timeline: view()){
  @media (prefers-reduced-motion:no-preference){
    .wrc-hero-media img{animation:wrc-drift linear both;animation-timeline:view();animation-range:exit 0% exit 100%;}
    .wrc-hero-in{animation:wrc-lift linear both;animation-timeline:view();animation-range:exit 0% exit 90%;}
    @keyframes wrc-drift{from{transform:scale(1.02);}to{transform:scale(1.14) translateY(9%);}}
    @keyframes wrc-lift{from{transform:none;opacity:1;}to{transform:translateY(-22%);opacity:0;}}
    .wrc-reveal{animation:wrc-unveil linear both;animation-timeline:view();animation-range:entry 5% cover 42%;}
    .wrc-reveal img{animation:wrc-depth linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
    @keyframes wrc-unveil{from{clip-path:inset(22% 14% 22% 0);}to{clip-path:inset(0);}}
    @keyframes wrc-depth{from{transform:translateY(-7%) scale(1.16);}to{transform:translateY(7%) scale(1.16);}}
    .wrc-cut{animation:wrc-cutin linear both;animation-timeline:view();animation-range:entry 10% cover 40%;}
    @keyframes wrc-cutin{from{clip-path:inset(0 0 100% 0);transform:translateY(12%);}to{clip-path:inset(0 0 -10% 0);transform:none;}}
    .wrc-end-media img{animation:wrc-depth2 linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
    @keyframes wrc-depth2{from{transform:translateY(-6%) scale(1.12);}to{transform:translateY(4%) scale(1.12);}}
  }
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto!important;}
  .wrc *,.wrc *::before,.wrc *::after{transition:none!important;}
}
@media print{
  .wrc-js .wrc-rise .w>span,.wrc-js .wrc-days i{transform:none!important;}
  .wrc-bar,.wrc-dock,.wrc-cur{display:none!important;}
}

/* ---------- narrower screens ---------- */
@media (max-width:1100px){
  .wrc-rec{grid-template-columns:minmax(0,10rem) minmax(0,1fr);}
  .wrc-rec-v{grid-column:2;}
}
@media (max-width:900px){
  .wrc-hero-foot{flex-direction:column;align-items:flex-start;gap:var(--sp-3);}
  .wrc-row,.wrc-scale{grid-template-columns:minmax(0,1fr) auto;gap:.2rem var(--sp-3);}
  .wrc-row-d{grid-column:1/-1;grid-row:2;height:76px;margin-top:.5rem;}
  .wrc-row-t{grid-column:2;grid-row:1;}
  .wrc-scale div{grid-column:1/-1;}
  .wrc-fly figcaption{position:static;width:auto;margin-top:var(--sp-2);}
  .wrc-valley-grid{grid-template-columns:minmax(0,1fr);margin-top:var(--sp-4);}
  .wrc-valley .wrc-ph{margin-right:calc(var(--gutter) * -1);}
  .wrc-valley-copy{padding-top:0;}
  .wrc-when{grid-template-columns:minmax(0,1fr);}
  .wrc-when>div,.wrc-when>div + div{padding:var(--sp-3) 0;border-left:0;border-bottom:1px solid var(--line);}
  .wrc-aud{grid-template-columns:minmax(0,1fr);}
  .wrc-portrait{max-width:24rem;order:2;}
  .wrc-hz-track{display:flex;gap:var(--sp-2);overflow-x:auto;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;scrollbar-width:none;
    margin:0 calc(var(--gutter) * -1);padding:0 var(--gutter) var(--sp-2);scroll-padding:0 var(--gutter);flex-wrap:nowrap;}
  .wrc-hz-track::-webkit-scrollbar{display:none;}
  .wrc-tier{flex:0 0 min(84%,24rem);scroll-snap-align:start;min-height:0;}
  .wrc-tier h3{margin-top:var(--sp-5);}
}
@media (max-width:760px){
  .wrc{--wrc-mega:calc(var(--fs-display) * 1.62);--wrc-huge:calc(var(--fs-display) * 1.3);--wrc-big:var(--fs-h1);}
  .wrc-bar{display:none;}
  .wrc-dock{display:flex;position:sticky;bottom:0;z-index:40;margin-top:-68px;align-items:center;justify-content:space-between;gap:.5rem;
    padding:8px var(--gutter) calc(8px + env(safe-area-inset-bottom));background:var(--wrc-shade);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-top:1px solid var(--line);
    transition:translate .4s var(--ease);}
  .wrc-dock.is-away{translate:0 110%;}
  .wrc-dock ol{display:flex;margin:0;padding:0;list-style:none;}
  .wrc-dock ol a{position:relative;display:grid;place-items:center;width:44px;height:44px;font-family:var(--wrc-mono);font-size:var(--fs-small);color:var(--gray);text-decoration:none;}
  .wrc-dock ol a i{position:absolute;left:12px;right:12px;bottom:7px;height:1px;background:var(--edge);overflow:hidden;}
  .wrc-dock ol a i::after{content:"";position:absolute;inset:0;background:var(--orange);transform:scaleX(var(--f,0));transform-origin:0 50%;}
  .wrc-dock ol a[aria-current]{color:var(--white);}
  .wrc-dock .wrc-btn{min-height:44px;padding:0 1.25rem;font-size:var(--fs-small);}
  .wrc-sec{scroll-margin-top:var(--sp-3);padding:calc(var(--sp-section) * 1.5) 0;}
  .wrc-title .ln + .ln{padding-left:0;}
  .wrc-kick{letter-spacing:.12em;}
  .wrc-rec{grid-template-columns:minmax(0,1fr);gap:.5rem;}
  .wrc-rec-v{grid-column:auto;}
  .wrc-tp{font-size:.62rem;letter-spacing:.1em;}
  .wrc-tp.is-end{transform:translateX(-92%);}
  .wrc-open{grid-template-columns:minmax(0,1fr);gap:0;}
  .wrc-open li{padding:.8rem 0;}
  .wrc-stats div:nth-child(even){padding-left:var(--sp-3);}
  .wrc-end{min-height:0;padding:calc(var(--sp-section) * 3) 0 calc(var(--sp-section) + 76px);}
  .wrc-cta{flex-direction:column;align-items:stretch;gap:var(--sp-2);}
  .wrc-cta .wrc-btn{width:100%;}
  .wrc-cta .wrc-btn.is-line{justify-content:space-between;}
}
@media (max-width:560px){
  .wrc{--gutter:16px;}
  .wrc-facts div{grid-template-columns:5.5rem minmax(0,1fr);}
}
""".replace("__GRAIN__", GRAIN)


ARROW = ('<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M1 8h13M9 3l5 5-5 5" '
         'fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')


def course_row(km):
    """One course drawn to scale: 100 km out is the full width (x 0 to 960),
    out along the top line, round the turnpoint, back along the bottom."""
    tx = 960 * (km / 2) / 100
    d = "M0 30H%gA20 20 0 0 1 %g 70H0" % (tx, tx)
    pct = tx / 10
    t = mins(km, BEST)
    return (
        '<div class="wrc-row" data-km="%d" data-tx="%g">' % (km, tx)
        + '<p class="wrc-row-k"><b>%d&nbsp;km</b></p>' % km
        + '<div class="wrc-row-d" role="img" aria-label="The %d km course, drawn to scale: %d km out to a turnpoint, then straight back">' % (km, km // 2)
        + '<svg viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
        + '<path class="g" d="%s"/><path class="t" d="%s"/><path class="s" d="M0 22V78"/></svg>' % (d, d)
        + ('<span class="wrc-tp" style="--x:%g%%" aria-hidden="true">Turnpoint</span>' % pct if km == 100 else '')
        + '<i class="wrc-gl" aria-hidden="true"></i></div>'
        + '<p class="wrc-row-t"><span class="wrc-clock" data-min="%d">%s</span></p>' % (t, clock(km, BEST))
        + "</div>"
    )


def days():
    # 18 January to 12 February 2027: 26 days; the expeditions are 18 to 29 January and 1 to 12 February
    out = []
    for i in range(26):
        cls = "x" if (i <= 11 or i >= 14) else "o"
        out.append('<i class="%s" style="--d:%d"></i>' % (cls, i))
    return "".join(out)


def bar():
    lis = []
    for n, (cid, name) in enumerate(CHAPTERS[:5], 1):
        lis.append('<li><a href="#%s" data-ch="%s"><span>%02d</span>%s<i></i></a></li>' % (cid, cid, n, name))
    return ('<nav class="wrc-bar" aria-label="Chapters of this page"><div class="wrc-in wrc-bar-in">'
            '<ol>' + "".join(lis) + '</ol>'
            '<a class="wrc-btn is-solid" href="#partner" data-ch="partner">Partner</a></div></nav>')


def dock():
    lis = []
    for n, (cid, name) in enumerate(CHAPTERS[:5], 1):
        lis.append('<li><a href="#%s" data-ch="%s">%02d<span class="wrc-vh"> %s</span><i></i></a></li>' % (cid, cid, n, name))
    return ('<nav class="wrc-dock" aria-label="Chapters of this page (phone)"><ol>' + "".join(lis) + '</ol>'
            '<a class="wrc-btn is-solid" href="#partner" data-ch="partner">Partner</a></nav>')


def tiers():
    data = [
        ("is-lead", "01", "One only", "Title Partner",
         ["Name in the title", "Mark on kit and camera", "Segments in build-up and debrief",
          "First film credit", "Logo on live tracking"]),
        ("", "02", "Kit", "Equipment Partner",
         ["Used and shown", "Honest, disclosed review", "With my expedition pilots", "Credits"]),
        ("", "03", "Brands, people", "Supporter",
         ["Name on this page", "Newsletter and debrief thanks", "Film credit"]),
    ]
    out = []
    for cls, n, tag, name, items in data:
        out.append('<article class="wrc-tier %s"><p class="wrc-tier-n" aria-hidden="true">%s</p>'
                   '<p class="wrc-tier-tag">%s</p><h3>%s</h3><ul>%s</ul></article>'
                   % (cls, n, tag, name, "".join("<li>%s</li>" % i for i in items)))
    return "".join(out)


def main_html():
    partner_intro = (label(6, "Partner") + rise("Three Ways On Board", "h2", "wrc-h", "partner-h")
                     + '<p class="wrc-line">Always marked as sponsored. Prices in the media kit, on request.</p>')
    return """<main id="v4-main" class="wrc">
<script>document.documentElement.classList.add('wrc-js')</script>

<header class="wrc-hero" id="wrc-top">
  <div class="wrc-hero-media"><picture><source media="(max-aspect-ratio: 2/3)" srcset="img/hero/kenya-kerio-valley-p.webp" type="image/webp"><source media="(max-aspect-ratio: 2/3)" srcset="img/hero/kenya-kerio-valley-p.jpg"><source srcset="__K__/hero/kerio-valley.webp" type="image/webp"><img src="__K__/hero/kerio-valley.jpg" width="1152" height="768" alt="Paragliding at Kerio Valley, Kenya" fetchpriority="high"></picture></div>
  <div class="wrc-hero-in">
    <p class="wrc-kick">World record attempt &middot; Kerio Valley, Kenya</p>
    <h1 class="wrc-title"><span class="ln">Against</span> <span class="ln">The Clock</span></h1>
    <div class="wrc-hero-foot">
      <p class="wrc-line">Two paragliding world records for speed, 100&nbsp;km and 200&nbsp;km out and return.</p>
      <dl class="wrc-spec"><div><dt>Window</dt><dd>18 Jan to 12 Feb 2027</dd></div></dl>
    </div>
  </div>
</header>

__BAR__

<section class="wrc-sec" id="record" aria-labelledby="record-h">
  <div class="wrc-in">
    __L1__
    __H1__
    <div class="wrc-recs">
      <div class="wrc-rec">
        <p class="wrc-rec-k"><b>100&nbsp;km</b></p>
        <p class="wrc-num"><span class="v" data-count="35.94" data-dec="2">35.94</span><small>km/h</small></p>
        <p class="wrc-rec-v"><b>Michel Macquet (FRA)</b><br>23&nbsp;Jan&nbsp;2025 &middot; __TBC__</p>
      </div>
      <div class="wrc-rec">
        <p class="wrc-rec-k"><b>200&nbsp;km</b></p>
        <p class="wrc-num">__TBD__</p>
        <p class="wrc-rec-v"></p>
      </div>
      <div class="wrc-rec is-me">
        <p class="wrc-rec-k"><b>My pace</b>Not a record course</p>
        <p class="wrc-num"><span class="v" data-count="36">36</span><small>km/h</small></p>
        <p class="wrc-rec-v"><b>198.86&nbsp;km in Kenya</b><br>6&nbsp;Feb&nbsp;2025</p>
      </div>
    </div>
    <p class="wrc-say">The time to beat: 100&nbsp;km in <em>2&nbsp;h&nbsp;47&nbsp;min</em>.</p>
    <details class="wrc-more"><summary>About these numbers</summary>
      <p>Class O-3 is paragliders. Speed is the course distance over the time.</p>
      <p>One FAI listing shows the 100&nbsp;km mark as a claim under review, another as the record: <a class="wrc-link" href="__FAI_LIST__" target="_blank" rel="noopener">FAI CIVL records</a>.</p>
      <p>My 198.86&nbsp;km flight, about 36&nbsp;km/h on a UP Trango X (EN C), was logged on XContest. It was not a record course: <a class="wrc-link" href="__UP__" target="_blank" rel="noopener">UP Paragliders</a>.</p>
      <p>The claim goes to the FAI under the <a class="wrc-link" href="__CODE__" target="_blank" rel="noopener">Sporting Code, Section 7D</a>.</p>
    </details>
  </div>
</section>

<section class="wrc-sec wrc-course wrc-grain" id="course" aria-labelledby="course-h">
  <div class="wrc-stage">
    <p class="wrc-km" aria-hidden="true"><span class="v">0</span><small>km</small></p>
    <div class="wrc-in">
      <div class="wrc-course-head">
        <div>__L2__
        __H2__</div>
        <p class="wrc-line">Speed is distance over time.</p>
      </div>
      <figure class="wrc-fly" data-cur>
        __ROW100__
        __ROW200__
        <div class="wrc-scale" aria-hidden="true"><div><span style="--x:0%">0</span><span style="--x:24%"></span><span style="--x:48%">50</span><span style="--x:72%"></span><span style="--x:96%">100&nbsp;km</span></div></div>
        <figcaption>To scale, at my 36&nbsp;km/h.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="wrc-sec wrc-valley" id="valley" aria-labelledby="valley-h">
  <div class="wrc-in">
    __L3__
    <h2 class="wrc-cut" id="valley-h">Kerio Valley</h2>
  </div>
  <div class="wrc-in wrc-valley-grid">
    <figure class="wrc-ph wrc-reveal"><picture><source srcset="__K__/gallery/kenya-ridge.webp" type="image/webp"><img src="__K__/gallery/kenya-ridge.jpg" width="1400" height="600" alt="Paragliding in Kenya" loading="lazy" decoding="async"></picture></figure>
    <div class="wrc-valley-copy">
      <p class="wrc-line">My Kenya base, and the site where the world speed records are chased.</p>
      <dl class="wrc-facts">
        <div><dt>Season</dt><dd>December to March</dd></div>
        <div><dt>Thermals</dt><dd>4 to 6&nbsp;m/s at midday, rare surges 6&nbsp;to&nbsp;7</dd></div>
        <div><dt>Flights</dt><dd>2 to 7 hours over the Rift Valley</dd></div>
        <div><dt>Where</dt><dd class="m">0.72&deg;N 35.65&deg;E</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="wrc-sec wrc-grain" id="window" aria-labelledby="window-h">
  <div class="wrc-in">
    __L4__
    __H4__
    <p class="wrc-line wrc-sub">Alongside my two Kenya expeditions.</p>
    <div class="wrc-when">
      <div><h3>Before</h3><p>Build-up episodes, newsletter</p></div>
      <div class="is-now"><h3>During</h3><p>Live tracking, daily updates</p>
        <div class="wrc-days" role="img" aria-label="The window, 26 days, flown alongside my two Kenya expeditions: 18 to 29 January and 1 to 12 February 2027">__DAYS__</div>
        <div class="wrc-days-l" aria-hidden="true"><span style="--x:0%">18&nbsp;Jan</span><span class="r" style="--x:100%">12&nbsp;Feb</span></div>
      </div>
      <div><h3>After</h3><p>Film, debrief episode, flight data</p></div>
    </div>
    <ul class="wrc-open">
      <li><b>Wing, instruments</b>__TBD__</li>
      <li><b>Team, FAI observer</b>__TBD__</li>
      <li><b>Preparation</b>__TBD__</li>
    </ul>
  </div>
</section>

<section class="wrc-sec" id="audience" aria-labelledby="audience-h">
  <div class="wrc-in wrc-aud">
    <figure class="wrc-ph wrc-portrait wrc-reveal"><picture><source srcset="../../assets/images/partners-aninder.webp" type="image/webp"><img src="../../assets/images/partners-aninder.jpg" width="720" height="900" alt="Aninder Singh" loading="lazy" decoding="async"></picture><figcaption>Aninder Singh</figcaption></figure>
    <div>
      __L5__
      __H5__
      <dl class="wrc-stats">
        <div><dt>Podcast streams</dt><dd><span class="v" data-count="100000" data-suf="+">100,000+</span></dd></div>
        <div><dt>Countries reached</dt><dd><span class="v" data-count="130" data-suf="+">130+</span></dd></div>
        <div><dt>Long-form interviews</dt><dd><span class="v" data-count="80">80</span></dd></div>
        <div><dt>Years flying</dt><dd><span class="v" data-count="10" data-suf="+">10+</span></dd></div>
      </dl>
      <p class="wrc-line">On the podcast, its YouTube channel and a newsletter about four times a month.</p>
    </div>
  </div>
</section>

<section class="wrc-partner" id="partner" aria-labelledby="partner-h">
  <div class="wrc-hz">
    <div class="wrc-hz-stage">
      <div class="wrc-in wrc-hz-intro">__PINTRO__</div>
      <div class="wrc-in wrc-hz-track">
        __TIERS__
      </div>
      <div class="wrc-hz-prog" aria-hidden="true"><i></i></div>
    </div>
  </div>
</section>

<section class="wrc-end" aria-labelledby="end-h">
  <figure class="wrc-end-media"><picture><source srcset="../../assets/images/partners-coupe-icare-wide.webp" type="image/webp"><img src="../../assets/images/partners-coupe-icare-wide.jpg" width="1920" height="1372" alt="Aninder shaking hands with a brand representative at a harness test stand, camera in hand, at Coupe Icare" loading="lazy" decoding="async"></picture></figure>
  <div class="wrc-in">
    __HEND__
    <div class="wrc-cta">
      <a class="wrc-btn is-solid wrc-mag" href="__MAIL__">Partner on the attempt __ARROW__</a>
      <a class="wrc-btn is-line wrc-mag" href="partners.html#pwForm">Other ways to work together __ARROW__</a>
    </div>
    <details class="wrc-more"><summary>Sources</summary>
      <p><a class="wrc-link" href="__UP__" target="_blank" rel="noopener">My flight, UP Paragliders</a> &middot; <a class="wrc-link" href="__FAI_LIST__" target="_blank" rel="noopener">FAI CIVL records</a> &middot; <a class="wrc-link" href="__CODE__" target="_blank" rel="noopener">FAI Sporting Code, Section 7D</a> &middot; <a class="wrc-link" href="destinations/kenya.html">The Kenya expedition</a> &middot; <a class="wrc-link" href="safety-and-disclosure.html">Safety &amp; Disclosure</a></p>
    </details>
  </div>
</section>

__DOCK__
</main>""".replace("__BAR__", bar()).replace("__DOCK__", dock()) \
        .replace("__L1__", label(1, "Record")).replace("__H1__", rise("The Number To Beat", "h2", "wrc-h", "record-h")) \
        .replace("__L2__", label(2, "Course")).replace("__H2__", rise("Out And Back, Flat Out", "h2", "wrc-h", "course-h")) \
        .replace("__L3__", label(3, "Valley")) \
        .replace("__L4__", label(4, "Window")).replace("__H4__", rise("18 January To|12 February 2027", "h2", "wrc-h", "window-h")) \
        .replace("__L5__", label(5, "Audience")).replace("__H5__", rise("Pilots Who Come Here To Learn", "h2", "wrc-h", "audience-h")) \
        .replace("__HEND__", rise("Put Your Name On The Clock", "h2", "wrc-h", "end-h")) \
        .replace("__PINTRO__", partner_intro) \
        .replace("__TIERS__", tiers()).replace("__ROW100__", course_row(100)).replace("__ROW200__", course_row(200)) \
        .replace("__DAYS__", days()).replace("__TBD__", TBD).replace("__TBC__", TBC) \
        .replace("__K__", KENYA).replace("__MAIL__", MAIL).replace("__CODE__", FAI_CODE) \
        .replace("__FAI_LIST__", FAI_LIST).replace("__UP__", UP_NEWS).replace("__ARROW__", ARROW)


SCRIPT = r"""<script>
/* The speed record attempt, C (tools/v4_record_c.py). Everything here answers the
   visitor's scroll or pointer; with reduced motion or without this script the
   page is complete and still. */
(function () {
  var d = document, w = window, root = d.documentElement;
  var mm = function (q) { return w.matchMedia && w.matchMedia(q).matches; };
  var still = mm('(prefers-reduced-motion: reduce)');
  var fine = mm('(hover: hover) and (pointer: fine)');
  var BEST = __BEST__;
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(t) { return 1 - Math.pow(1 - t, 3); }

  /* 1. titles rise and the window's days fill, once, as they arrive */
  var once = d.querySelectorAll('.wrc-rise, .wrc-days');
  if (still || !('IntersectionObserver' in w)) once.forEach(function (el) { el.classList.add('is-in'); });
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.2 });
    once.forEach(function (el) { io.observe(el); });
  }

  /* 2. numbers count up once, in place (their width is held so nothing moves) */
  function fmt(v, dec) { return v.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }); }
  var nums = d.querySelectorAll('.wrc [data-count]');
  if (!still && 'IntersectionObserver' in w) {
    nums.forEach(function (el) { el.style.minWidth = el.getBoundingClientRect().width + 'px'; });
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        nio.unobserve(e.target);
        var el = e.target, to = parseFloat(el.dataset.count), dec = +(el.dataset.dec || 0), suf = el.dataset.suf || '', t0 = 0;
        (function step(t) {
          if (!t0) t0 = t;
          var p = clamp((t - t0) / 1600, 0, 1);
          el.textContent = fmt(to * ease(p), dec) + (p >= 1 ? suf : '');
          if (p < 1) requestAnimationFrame(step);
        })(performance.now());
      });
    }, { threshold: 0.6 });
    nums.forEach(function (el) { el.textContent = fmt(0, +(el.dataset.dec || 0)); nio.observe(el); });
  }

  /* 3. the course: two to one scale, each flown with a clock beside it */
  var course = d.getElementById('course');
  var rows = [].slice.call(d.querySelectorAll('.wrc-row')).map(function (r) {
    var t = r.querySelector('.t'), L = t.getTotalLength(), tx = parseFloat(r.dataset.tx);
    t.style.strokeDasharray = L + ' ' + L;
    return { el: r, t: t, L: L, km: +r.dataset.km, tx: tx, arc: L - 2 * tx,
      svg: r.querySelector('svg'), gl: r.querySelector('.wrc-gl'), clock: r.querySelector('.wrc-clock') };
  });
  var kmBig = d.querySelector('.wrc-km .v');
  function hm(km) { var t = Math.round(km / BEST * 60); return Math.floor(t / 60) + '<small>h</small> ' + ('0' + (t % 60)).slice(-2) + '<small>min</small>'; }
  function flyRow(r, f) {
    // f 0..1 along the course; the km stand still while the glider rounds the turnpoint
    var len = r.L * f, half = r.km / 2, km;
    if (len <= r.tx) km = len / r.tx * half;
    else if (len < r.tx + r.arc) km = half;
    else km = half + (len - r.tx - r.arc) / r.tx * half;
    r.t.style.strokeDashoffset = r.L - len;
    var pt = r.t.getPointAtLength(len), b = r.svg.getBoundingClientRect();
    r.gl.style.transform = 'translate(' + (pt.x / 1000 * b.width).toFixed(1) + 'px,' + (pt.y / 100 * b.height).toFixed(1) + 'px)';
    r.clock.innerHTML = hm(km);
    return km;
  }
  function flyAll(p) {
    // the 100 km course in the first part of the scroll, the 200 km course in the second
    var a = clamp(p / 0.42, 0, 1), b = clamp((p - 0.5) / 0.42, 0, 1);
    var k1 = flyRow(rows[0], a), k2 = flyRow(rows[1], b), on = p < 0.48 ? 0 : 1;
    rows[0].el.classList.toggle('is-on', on === 0); rows[1].el.classList.toggle('is-on', on === 1);
    if (kmBig) kmBig.textContent = Math.round(on ? k2 : k1);
  }
  var pinCourse = false, WIDE = '(min-width: 901px) and (min-height: 600px)';
  if (course && rows.length === 2 && !still) {
    course.classList.add('is-live');
    pinCourse = mm(WIDE);
    if (pinCourse) course.classList.add('is-pin');
    flyAll(0);
    if (!pinCourse && 'IntersectionObserver' in w) {
      // a phone: flown once, when the drawing comes into view
      var cio = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return; cio.disconnect();
        var t0 = 0;
        (function step(t) {
          if (!t0) t0 = t;
          var p = clamp((t - t0) / 4200, 0, 1);   // the 100 km course in the first half, the 200 km course in the second
          flyAll(p < 0.5 ? p * 0.84 : 0.5 + (p - 0.5) * 0.84);
          if (p < 1) requestAnimationFrame(step);
        })(performance.now());
      }, { threshold: 0.55 });
      cio.observe(course.querySelector('.wrc-fly'));
    }
  }

  /* 4. the tiers: a row moved sideways by the scroll on a wide screen with a mouse */
  var hz = d.querySelector('.wrc-hz'), track = hz && hz.querySelector('.wrc-hz-track'), prog = hz && hz.querySelector('.wrc-hz-prog');
  var intro = hz && hz.querySelector('.wrc-hz-intro'), pinHz = false, D = 0;
  function sizeHz() {
    if (!hz) return;
    var want = !still && fine && mm(WIDE);
    if (want !== pinHz) {
      pinHz = want;
      hz.classList.toggle('is-pin', want);
      // pinned, the intro is the row's first panel; otherwise it heads the section
      if (want) track.insertBefore(intro, track.firstChild); else track.parentNode.insertBefore(intro, track);
    }
    track.style.transform = '';
    hz.style.height = '';
    D = 0;
    if (!pinHz) return;
    D = Math.max(0, track.scrollWidth - hz.querySelector('.wrc-hz-stage').clientWidth);
    hz.style.height = (w.innerHeight + D) + 'px';
  }
  function sizeCourse() {
    if (!course || still || rows.length !== 2) return;
    var want = mm(WIDE);
    if (want === pinCourse) return;
    pinCourse = want;
    course.classList.toggle('is-pin', want);
    if (!want) flyAll(1);   // a narrow window shows the courses flown
  }
  sizeHz();

  /* 5. the chapter bar: each chapter fills as it is read; the one on screen is marked */
  var links = [].slice.call(d.querySelectorAll('.wrc-bar [data-ch], .wrc-dock [data-ch]'));
  var chs = ['record', 'course', 'valley', 'window', 'audience', 'partner'].map(function (id) { return d.getElementById(id); });
  var hero = d.querySelector('.wrc-hero'), dock = d.querySelector('.wrc-dock');

  var queued = false;
  function frame() {
    queued = false;
    var vh = w.innerHeight, cur = -1;
    chs.forEach(function (c, i) {
      if (!c) return;
      var r = c.getBoundingClientRect(), f = clamp((vh * 0.5 - r.top) / Math.max(1, r.height), 0, 1);
      if (r.top < vh * 0.5) cur = i;
      links.forEach(function (a) { if (a.dataset.ch === c.id) { var i2 = a.querySelector('i'); if (i2) i2.style.setProperty('--f', f.toFixed(3)); } });
    });
    links.forEach(function (a) {
      if (cur >= 0 && chs[cur] && a.dataset.ch === chs[cur].id) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
    if (dock && hero) dock.classList.toggle('is-away', hero.getBoundingClientRect().bottom > vh * 0.55);
    if (pinCourse) {
      var r = course.getBoundingClientRect();
      flyAll(clamp(-r.top / Math.max(1, r.height - vh), 0, 1));
    }
    if (pinHz && D) {
      var p = clamp(-hz.getBoundingClientRect().top / D, 0, 1);
      track.style.transform = 'translate3d(' + (-p * D).toFixed(1) + 'px,0,0)';
      if (prog) prog.style.setProperty('--p', p.toFixed(3));
    }
  }
  function ask() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  w.addEventListener('scroll', ask, { passive: true });
  w.addEventListener('resize', function () { sizeCourse(); sizeHz(); ask(); }, { passive: true });
  w.addEventListener('load', function () { sizeHz(); ask(); });
  frame();

  /* 6. a ring cursor and buttons that lean to the pointer (mouse screens only) */
  if (fine && !still) {
    var ring = d.createElement('div'); ring.className = 'wrc-cur'; ring.setAttribute('aria-hidden', 'true'); ring.innerHTML = '<i></i>';
    d.body.appendChild(ring);
    var x = 0, y = 0, tx = 0, ty = 0, raf = 0, seen = false;
    function glide() {
      x += (tx - x) * 0.28; y += (ty - y) * 0.28;
      ring.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
      raf = (Math.abs(tx - x) + Math.abs(ty - y) > 0.4) ? requestAnimationFrame(glide) : 0;
    }
    d.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX; ty = e.clientY;
      if (!seen) { seen = true; x = tx; y = ty; }
      ring.classList.add('is-on');
      var t = e.target.closest ? e.target.closest('a, button, summary, [data-cur]') : null;
      ring.classList.toggle('is-big', !!t);
      if (!raf) raf = requestAnimationFrame(glide);
    }, { passive: true });
    root.addEventListener('pointerleave', function () { ring.classList.remove('is-on'); });
    d.querySelectorAll('.wrc-mag').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.22).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.35).toFixed(1) + 'px)';
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
    if "wrc-hero" not in head or "Partner With Me" in head.split("<body")[0] or URL not in head:
        raise SystemExit("v4_record_c: the partners shell has changed; check the head")
    page = head + main_html() + tail.replace("</body>", SCRIPT + "\n</body>", 1)
    if "\u2014" in page:
        raise SystemExit("v4_record_c: an em dash slipped into the page")
    open(OUT, "w", encoding="utf-8").write(page)
    print("v4_record_c: %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
