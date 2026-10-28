#!/usr/bin/env python3
"""
Partner With Me, less but better (owner, 20 Oct 2026). The record page's pass
(tools/v4_record.py; docs/v4-design-rules.md, Motion) carried to the sponsor
funnel, prototypes/v4/partners.html. The owner called the record page's first
version "a cheap rip-off feeling rather than a premium one"; what fixed it was
one easing curve, motion with weight that settles (never a loop), typography
and real photographs as the graphics, no count-ups, and photographs that never
meet the page at a hard edge. The blind judges of India's pass (docs/v4-report.md,
"India, less but better") added: big confident figures beat rows of small
labels; anything moving on its own reads templated; a visible [to supply]
hurts trust where a buyer decides. The owner named three ideas for Partners:
the four formats laid out with the clarity of the record page's offer, the
audience numbers big and still with a fold that says where each comes from
(left out until the owner gives the source of the 100,000+ streams: a fold
that explains two of four figures read as hedging to a blind judge), and a
prominent link to the record attempt. On the countries figure (owner,
20 Oct 2026): "130 plus is the correct figure".

A fix round the same day (owner, 20 Oct 2026; a checker passed the first build
and two blind judges preferred it, but narrowly on looks) brought back what the
pushed page did better and tightened the rest: the four formats are the pushed
page's editorial list again (without its arrows, its sliding hover and its
outlined numerals); the figures' labels are small capitals again, as on the
pushed page, and their fold is left out until every figure has its source;
the record block has room above the flight line and one line of what a partner
gets; the portrait is as clear as it was; the enquiry sits over the pushed
page's blurred photograph again (without its orange corner marks); the figures
keep a clear gap; every numeral is in the display face, none in the slashed-zero
mono; the band in the air follows the episodes with no dead dark between.

What this does to the page, in place (the look is the page's own <style>
block, the one right before <!-- site-schema -->, which this rewrites whole and
recognises by its leading /* v4p */ comment; v2.css and v2-immersive.js are as
they were, so no other page changes):

  - The opening holds still: the handshake is there at first paint (its
    arrival fade and its 16 s push-in with no input go), with no orange glow
    behind the words, and it dissolves into the page's dark on its left, top
    and foot in eight eased steps (a smoothstep, as v4-calm.css draws India's
    edges). The hero is the first screen under the header, so nothing of the
    figures pokes into its foot. The caption's orange is --orange-lite, with a
    tight shadow made from the tokens.
  - The audience: the four figures (100,000+ podcast streams, 130+ countries
    reached, 80 long-form interviews, 10+ years flying) leave the blurred
    glass band across the photograph and stand on the page's dark under the
    opening, laid out like the record page's .wr-stats: a <dl>, each figure
    in Poppins 700 with tabular numerals as large as its column allows, a
    hairline over it, its label under it in small capitals; the columns' gap is
    3rem four across (2rem two by two), so 100,000+ stands at least 2.5rem
    clear of 130+ and on one line from 360 to 1440 px. No count-up: the
    script, data-count and data-suffix go; the figures are final at first
    paint. No fold under them yet: the site states where 80 (the podcast
    feed) and 130+ (the podcast page's 136 countries) come from, but not the
    100,000+ streams or the 10+ years, and a fold that explains two of four
    read as hedging. With the owner's sources it goes back under the figures.
  - The episodes: the reel stops drifting. Two still rows of 14, each of the
    28 episode links once (the loop's duplicate half goes), each row moved
    only by the visitor's own swipe (a native scroll that snaps to a tile,
    its bar hidden); the edge fade stays; a tile takes its colour back under
    the pointer on --ease, without the zoom.
  - The Name Flies With Me holds still (its 16 s push when first seen and the
    observer that started it go) and follows the episodes straight away (the
    rows' own 8 px between, no margin), coming out of the page's dark at its
    top on a short eased shade (the top 18 %) and going back into it at its
    foot on a long one, with a pool of the page's dark behind its words; their
    shadows are made from the tokens.
  - The record attempt, directly after that band: type only, on the page's
    dark, every word the record page's own (its kicker, its title, its line,
    its window, one line of what a partner gets from its offer, "Title
    Partner: Your mark on kit and on camera", and "Partner on the attempt" to
    record-attempt.html); not its 35.94, which reads [to confirm] there. Room
    under it (a section's space and 1.5rem), so the flight line, which starts
    below it, never meets its title or its button. The record page is prototype-only
    (tools/v2_site.py PROTO_ONLY) until the owner's go, so the block sits
    between <!-- v4:needs record-attempt.html --> and <!-- /v4:needs -->:
    the switch (tools/v2_switch.py) drops it whole while that page is not
    switched, and the search (tools/v4_search.py) does not offer its heading,
    both through v2_site.needs. Once the record page goes live the block
    appears on the switched page by itself.
  - The flight line stays the page's one moment, now with weight: one
    requestAnimationFrame loop eases --jp toward the scroll (each frame closes
    a share of the gap by the time passed, the record page's glide) and stops
    when settled; a chapter's node lights when the line reaches it. The
    finished state is the default: without the script, and with reduced
    motion, the line is drawn whole and both nodes lit; only the script adds
    .pw-glide, which starts the line empty. No glow, the ring in color-mix().
  - The four formats as the pushed page's editorial list: full-width rows
    under hairlines, the number, the format in label type over its name, the
    sentence in a column on the right (the sentence under the name below
    1100 px), every word as pushed. The number is a plain numeral in the
    display face, in --gray; the outlined numerals, the arrows (which promised
    a link that was not there) and the hover that slid the row go. Under them
    one quiet action, "Start a conversation" (the form's own kicker) to
    #enquire, so Send Enquiry stays the page's only solid button.
  - The trust: the policy word for word, its counters quiet numerals in the
    display face in --gray; the portrait as clear as the pushed page shows it
    (no grade), a crisp frame with its hairline and no orange bracket.
  - The close: the card sits over the pushed page's blurred photograph of the
    handshake again (partners-coupe-icare-soft.webp, blurred 16 px), which
    comes out of the page's dark and goes back into it in eased steps under an
    even veil of the dark; the card's frame a hairline, its two orange corner
    marks gone, no backdrop blur (the photograph is blurred already).
    Every field, chip, label, the mailto link, the status line and the inline
    form script stay byte for byte; the chips are 44 px tall. The footer
    follows the form closely, with no drawn ridge and no glow left alone above
    it (as on India), set in this page's own <style>, so the footer markup and
    every other page's footer are untouched.
  - One curve: every transition and animation in the page and its footer
    eases on --ease (cubic-bezier(.2,.8,.2,1)); reduced motion turns every
    transition off. The site's time-of-day tokens change at once here
    instead of blending for 2 s on arrival (nothing on the page draws with
    them once the footer's glow is off). Colours only through the tokens and
    color-mix(). Every numeral is in the display face (Poppins), none in the
    slashed-zero mono.

Every change inside <main> sits between <!--v4p:NAME--> and <!--/v4p:NAME-->
marks, written in place of what the marks hold (or, the first time, of a
pattern that must match exactly once), so a changed upstream page fails
loudly instead of half patching; the <style> block is rewritten whole. Never
an HTML comment inside <style> (a CDO token there swallows the next rule),
never a second <style> or a new <link> in the head: partners.html is also the
shell (head, menu, footer) that tools/v4_record.py, v4_record_a/b/c.py,
v4_expeditions.py and v4_expeditions_a/b/c.py copy, replacing this <style>
block and the <main>; so nothing else before <main id="v4-main"> and nothing
after </main> is touched, the Partners-only script stays inside <main>, and
their pages come out byte for byte as before. Running it twice leaves the page
byte-identical; run on the pushed page it gives the built page. Nothing is
invented: every word, number and photograph is one the site already has.

Run it after tools/v4_ux.py (tools/v4_build.py runs it right after its v4_ux
step, beside v4_trip_calm india); then the search files:

    python3 tools/v4_partners.py
    python3 tools/v4_search.py

It asserts, on the page it writes: no em dash; no raw colour (hex, rgb(),
rgba(), hsl()) in its CSS or its markup; the h1, every id (plus pwRecord, the
record block's title) and the set of link targets (plus record-attempt.html
and #enquire) as they were; the head unchanged outside the one
<style> block and everything after </main> unchanged; the form script byte for
byte; no [to supply] anywhere, and no half-sourced fold under the figures; what a partner gets still word for word on
the record page; no mono or outlined numeral, no arrow or hover in the
formats, no filter on the portrait, no corner marks on the card; the v4:needs
marks sound. It never touches prototypes/v2/, the live pages, rss-feed.js,
src/v2.css, src/v2-immersive.js or any other v4 page.
"""
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site  # noqa: E402  (the v4:needs marks, as the switch and the search read them)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
PAGE = os.path.join(V4, "partners.html")

NEW_IDS = {"pwRecord"}
NEW_LINKS = {"record-attempt.html", "#enquire"}
RAW = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(")


def fail(msg):
    raise SystemExit("v4_partners: " + msg + " (the page has changed upstream; check it before patching)")


def marked(src, name, new, find):
    """Put `new` between <!--v4p:NAME--> marks: in place of what the marks hold when the page already has
    them (so a second run writes the same bytes), or the first time in place of `find`, a pattern that must
    match exactly once."""
    a, b = "<!--v4p:%s-->" % name, "<!--/v4p:%s-->" % name
    if src.count(a) == 1 and src.count(b) == 1:
        i, j = src.index(a), src.index(b) + len(b)
        return src[:i] + a + new + b + src[j:]
    if a in src or b in src:
        fail("the marks for %s are not a pair" % name)
    ms = list(re.finditer(find, src, re.S))
    if len(ms) != 1:
        fail("%s: expected one match, found %d" % (name, len(ms)))
    return src[:ms[0].start()] + a + new + b + src[ms[0].end():]


def held(src, name):
    """What the v4p marks hold, or None before the first run."""
    a, b = "<!--v4p:%s-->" % name, "<!--/v4p:%s-->" % name
    if src.count(a) == 1 and src.count(b) == 1:
        return src[src.index(a) + len(a):src.index(b)]
    return None


# ---------- the eased steps: a smoothstep from the page's dark to clear in eight (v4-calm.css's --v4c-*) ----------
S8 = (0, 4.3, 15.6, 31.6, 50, 68.4, 84.4, 95.7, 100)


def tone(p):
    p = round(p, 1)
    if p <= 0:
        return "transparent"
    if p >= 100:
        return "var(--bg)"
    return "color-mix(in srgb,var(--bg) %g%%,transparent)" % p


def eased(head, a, b, fall=True, strength=100):
    """A gradient opened by `head` (e.g. "linear-gradient(180deg") in eight eased steps between a% and b%:
    fall, the page's dark (at `strength`) at a and clear at b; else clear at a and the dark at b. As a mask
    only the strength counts."""
    stops = []
    for k, s in enumerate(S8):
        v = (100 - s) if fall else s
        stops.append("%s %g%%" % (tone(v * strength / 100), round(a + (b - a) * k / 8, 2)))
    return head + "," + ",".join(stops) + ")"


# the handshake dissolves on its left, top and foot (a phone: on its foot; its top meets the header bar)
HERO_MASK = ",".join([eased("linear-gradient(90deg", 0, 28, fall=False),
                      eased("linear-gradient(180deg", 0, 22, fall=False),
                      eased("linear-gradient(0deg", 0, 42, fall=False)])
HERO_MASK_P = eased("linear-gradient(0deg", 0, 46, fall=False)
# the band as a split (the OverOslo photograph): no shade at its top (owner, 28 Oct 2026: the sky over the festival
# stays clear; the band sits a gap below the episodes instead), a short one at its foot, no pool (the words stand
# on the page's dark beside the photograph, not on it)
AIR_SHADE = eased("linear-gradient(0deg", 0, 26)
# the close: the pushed page's blurred handshake comes out of the page's dark at its top and goes back into it
# at its foot in eased steps, under an even veil of the dark (the pushed page's 70%), so the card sits on the
# photograph and the footer follows on one dark
VEIL = "color-mix(in srgb,var(--bg) 70%,transparent)"
CLOSE_SHADE = ",".join([eased("linear-gradient(180deg", 0, 24),
                        eased("linear-gradient(0deg", 0, 24),
                        "linear-gradient(%s,%s)" % (VEIL, VEIL)])
EDGE_FADE = "linear-gradient(90deg,transparent,var(--bg) 8%,var(--bg) 92%,transparent)"

CSS = r"""/* v4p: Partner With Me, less but better (owner, 20 Oct 2026). tools/v4_partners.py writes this block whole.
   One story: the handshake opens it, still; the four audience figures stand big and still on the page's dark,
   the episodes wait in two still rows the visitor can swipe; the name
   flies; the record attempt; then the flight line, the page's one moment, eased with weight, through the four
   formats and the trust; the form closes it over the blurred handshake. One curve; numerals in the display
   face; colours only through the tokens and color-mix(). */

/* the site's time-of-day tokens: nothing on this page draws with them (the footer's glow is off, below), so
   they change at once instead of blending for two seconds on arrival */
:root{transition:none;}

/* one curve: every transition and animation in the page and its footer eases on --ease (the header and the
   menu keep their own); the :is() carries an id, so this outranks the class rules it corrects */
:is(#v4-main,footer),:is(#v4-main,footer) *,:is(#v4-main,footer) *::before,:is(#v4-main,footer) *::after{transition-timing-function:var(--ease);animation-timing-function:var(--ease);}

/* the opening: the handshake holds still, there at first paint, and dissolves into the page's dark on its
   left, top and foot in eased steps; the hero is the first screen under the header (93px), so the figures
   start below it */
.pw-hero{--pw-top:93px;position:relative;min-height:calc(100svh - var(--pw-top));display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;isolation:isolate;}
.pw-hero-photo{position:absolute;inset:0 0 0 auto;width:66%;z-index:-1;overflow:hidden;
  -webkit-mask-image:@@HERO_MASK@@;-webkit-mask-composite:source-in,source-in;
  mask-image:@@HERO_MASK@@;mask-composite:intersect;}
.pw-hero-photo picture{display:block;width:100%;height:100%;}
.pw-hero-photo img{width:100%;height:100%;object-fit:cover;object-position:52% 40%;}
.pw-hero-copy{position:relative;max-width:var(--measure);width:100%;margin:0 auto;padding:5.5rem var(--gutter) 2.2rem;}
.pw-hero-copy .kicker{display:block;margin-bottom:1rem;}
.pw-hero-copy h1{font-family:var(--font-display);font-weight:800;font-size:var(--fs-display);line-height:1.02;color:var(--white);margin:0 0 1.2rem;max-width:11ch;letter-spacing:-.01em;}
.pw-hero-copy h1 em{font-style:normal;color:var(--orange);}
.pw-hero-copy p{color:var(--gray-light);font-size:var(--fs-lead);line-height:1.75;max-width:30rem;margin:0 0 .9rem;}
.pw-hero-copy p strong{color:var(--white);font-weight:500;}
.pw-caption{position:absolute;right:var(--gutter);bottom:var(--sp-5);z-index:1;text-align:right;color:var(--white);font-size:var(--fs-small);
  text-shadow:0 1px 2px color-mix(in srgb,var(--bg) 85%,transparent);}
.pw-caption span{display:block;color:var(--orange-lite);font-size:var(--fs-micro);letter-spacing:.16em;text-transform:uppercase;margin-bottom:.25rem;}

/* the audience: four figures, big and still, each under a hairline with its label beneath (the record page's
   .wr-stats); each sized to its own column, so 100,000+ stays on one line at every width, with the columns'
   gap (3rem four across, 2rem two by two) clear between it and 130+; the labels in small capitals, as on the
   pushed page */
.pw-stats{max-width:var(--measure);margin:0 auto;padding:var(--sp-4) var(--gutter) 0;}
.pw-figs{margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-4);}
@media (min-width:1100px){.pw-figs{grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-4) var(--sp-5);}}
.pw-figs > div{container-type:inline-size;min-width:0;display:flex;flex-direction:column-reverse;justify-content:flex-end;padding-top:var(--sp-3);border-top:1px solid var(--edge);}
.pw-figs dd{margin:0;font-family:var(--font-display);font-weight:700;font-size:calc(var(--fs-display) * .95);font-size:min(calc(var(--fs-display) * .95),22.6cqi);
  line-height:1;letter-spacing:-.04em;color:var(--white);font-variant-numeric:tabular-nums;white-space:nowrap;}
.pw-figs dt{margin-top:.75rem;font-size:var(--fs-micro);font-weight:600;line-height:1.4;letter-spacing:.14em;text-transform:uppercase;color:var(--gray-light);}
/* a link inside a sentence keeps the line as it is and still takes a whole fingertip */
.pw-note a,.pw-direct a{display:inline-block;padding:.75rem 0;margin:-.75rem 0;}

/* the episodes: two still rows, each the visitor's own to swipe (a native scroll that snaps to a tile, its
   bar hidden); nothing drifts. A tile takes its colour back under the pointer */
.pw-reel{padding:clamp(2.2rem,5vw,3.4rem) 0 0;}
.pw-reel-h{max-width:var(--measure);margin:0 auto 1.2rem;padding:0 var(--gutter);display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;}
.pw-reel-h p{margin:0;color:var(--gray-light);font-size:var(--fs-body-s);}
.pw-reel-h a{color:var(--orange);font-size:var(--fs-small);text-decoration:none;}
.pw-rows{display:flex;flex-direction:column;gap:8px;-webkit-mask-image:@@EDGE_FADE@@;mask-image:@@EDGE_FADE@@;}
.pw-row{overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:var(--gutter);scrollbar-width:none;}
.pw-row::-webkit-scrollbar{display:none;}
.pw-track{display:flex;gap:8px;width:max-content;padding-inline:var(--gutter);}
.pw-tile{flex:none;width:clamp(150px,15vw,240px);aspect-ratio:16/9;overflow:hidden;background:var(--card);border:1px solid var(--edge);scroll-snap-align:start;}
.pw-tile img{width:100%;height:100%;object-fit:cover;display:block;filter:grayscale(1) brightness(.75);transition:filter var(--dur-m) var(--ease);}
.pw-tile:hover img,.pw-tile:focus-visible img{filter:none;}

/* in the air: the Oslo festival photograph (owner, 28 Oct 2026), upright, so the band is a split: the words on
   the page's dark at the left, the photograph standing on the right and dissolving into the dark at its left
   edge; still, straight under the episodes (the rows' own 8px between), out of the page's dark at its top on a
   short shade and back into it at its foot on a long one */
.pw-air{position:relative;overflow:hidden;isolation:isolate;display:grid;grid-template-columns:minmax(0,44fr) minmax(0,56fr);
  align-items:end;min-height:clamp(560px,88vh,900px);margin-top:clamp(3rem,6vw,5rem);}
.pw-air-photo{position:relative;grid-column:2;grid-row:1;align-self:stretch;z-index:-2;overflow:hidden;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,var(--bg) 24%);mask-image:linear-gradient(90deg,transparent 0,var(--bg) 24%);}
.pw-air-photo picture{display:block;width:100%;height:100%;}
.pw-air-photo img{width:100%;height:100%;object-fit:cover;object-position:50% 34%;display:block;}
.pw-air::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:@@AIR_SHADE@@;}
.pw-air-copy{grid-column:1;grid-row:1;width:100%;max-width:36rem;justify-self:end;padding:0 var(--gutter) clamp(2rem,6vw,4.5rem);}
.pw-air-copy p+p{margin-top:.9rem;}
.pw-air-cap{position:absolute;right:var(--gutter);bottom:clamp(1.5rem,4vw,3rem);z-index:1;grid-column:2;margin:0;text-align:right;color:var(--white);font-size:var(--fs-small);
  text-shadow:0 1px 2px color-mix(in srgb,var(--bg) 85%,transparent);}
.pw-air-cap span{display:block;color:var(--orange-lite);font-size:var(--fs-micro);letter-spacing:.16em;text-transform:uppercase;margin-bottom:.25rem;}
.pw-air-copy .kicker{display:block;margin-bottom:.6rem;}
.pw-air-copy h2{font-family:var(--font-display);font-weight:800;font-size:var(--fs-h1);line-height:1.05;color:var(--white);margin:0 0 .7rem;
  text-shadow:0 2px 24px color-mix(in srgb,var(--bg) 45%,transparent);}
.pw-air-copy p{color:var(--white);opacity:.85;font-size:var(--fs-lead);margin:0;max-width:34rem;text-shadow:0 1px 12px color-mix(in srgb,var(--bg) 60%,transparent);}

/* the record attempt: type only, on the page's dark, every word the record page's own; the switch leaves it
   out until the record page itself goes live (its mark in the markup, tools/v2_site.py). Room under it, so the
   flight line, which starts below it, never meets its title or its button */
.pw-rec{padding:var(--sp-section) 0 calc(var(--sp-section) + var(--sp-3));}
.pw-rec-in{max-width:var(--measure);margin:0 auto;padding:0 var(--gutter);display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:var(--sp-3) clamp(2rem,6vw,6rem);align-items:end;}
.pw-rec .kicker{display:flex;margin-bottom:var(--sp-2);}
.pw-rec h2{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--fs-h1);line-height:1.02;letter-spacing:-.03em;color:var(--white);max-width:12ch;text-wrap:balance;}
.pw-rec-in p{margin:0;max-width:30rem;font-size:var(--fs-lead);line-height:1.55;color:var(--gray-light);text-wrap:pretty;}
.pw-rec-w{display:grid;grid-template-columns:auto minmax(0,1fr);gap:.45rem 1rem;align-items:baseline;max-width:30rem;margin:var(--sp-2) 0 0;font-size:var(--fs-body-s);line-height:1.5;}
.pw-rec-w dt{color:var(--gray-light);}
.pw-rec-w dd{margin:0;font-weight:500;color:var(--white);font-variant-numeric:tabular-nums;}
.pw-rec .btn-lines{display:inline-flex;align-items:center;min-height:44px;margin-top:var(--sp-3);}
.pw-rec .btn-lines:hover{color:var(--orange);border-color:var(--orange);}

/* the flight line, the page's one moment: one track down the page, a node at each chapter. Drawn whole by
   default (no script, reduced motion); the script adds .pw-glide, which starts it where the scroll is and
   eases it toward the scroll with weight, and lights a node when the line reaches it */
.pw-journey{--jp:1;position:relative;max-width:var(--measure);margin:0 auto;padding:0 var(--gutter);}
.pw-journey::before,.pw-fill{content:"";position:absolute;left:calc(var(--gutter) + 13px);top:0;bottom:0;width:1px;}
.pw-journey::before{background:linear-gradient(180deg,var(--rule),var(--rule) 90%,transparent);}
.pw-fill{background:linear-gradient(180deg,transparent,var(--orange));transform-origin:50% 0;}
.pw-glide .pw-fill{transform:scaleY(var(--jp));}
.pw-chapter{position:relative;padding:var(--sp-section) 0 var(--sp-section) 4rem;}
.pw-node{position:absolute;left:0;top:calc(var(--sp-section) - .1rem);width:27px;height:27px;border-radius:50%;border:1px solid var(--orange);background:var(--bg);
  display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:.62rem;font-weight:600;color:var(--white);
  box-shadow:0 0 0 5px color-mix(in srgb,var(--orange) 12%,transparent);
  transition:border-color var(--dur-m) var(--ease),color var(--dur-m) var(--ease),box-shadow var(--dur-m) var(--ease);}
.pw-glide .pw-chapter:not(.is-on) .pw-node{border-color:var(--edge);color:var(--gray);box-shadow:0 0 0 0 transparent;}
.pw-still .pw-node{transition:none;}
.pw-chapter > .kicker{display:block;margin-bottom:.7rem;}
.pw-chapter h2{font-family:var(--font-display);font-weight:800;font-size:var(--fs-h1);line-height:1.05;color:var(--white);margin:0 0 1rem;max-width:18ch;}
.pw-lead{color:var(--gray-light);font-size:var(--fs-lead);line-height:1.75;max-width:60ch;margin:0 0 var(--sp-4);}

/* the four formats as the pushed page's editorial list: full-width rows under hairlines, the number, the
   format in label type over its name, the sentence in a column on the right. The number plain, in the display
   face; no arrow, and nothing moves under the pointer */
.pw-list{border-top:1px solid var(--rule);}
.pw-item{display:grid;grid-template-columns:4.5rem minmax(0,1fr) minmax(0,1.1fr);gap:1.2rem;align-items:center;padding:1.6rem .4rem;border-bottom:1px solid var(--rule);}
.pw-item .n{font-family:var(--font-display);font-weight:600;font-size:2.4rem;line-height:1;letter-spacing:-.02em;color:var(--gray);font-variant-numeric:tabular-nums;}
.pw-item h3{margin:0;font-family:var(--font-display);font-weight:700;font-size:var(--fs-h3);line-height:1.15;color:var(--white);}
.pw-item h3 small{display:block;color:var(--orange);font-family:var(--font-body);font-weight:500;font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;margin-bottom:.35rem;}
.pw-item p{margin:0;color:var(--gray-light);font-size:var(--fs-body-s);line-height:1.65;}
@media (max-width:1100px){.pw-item{grid-template-columns:3.6rem minmax(0,1fr);row-gap:.8rem;} .pw-item p{grid-column:2;}}
@media (max-width:560px){.pw-item{grid-template-columns:2.8rem minmax(0,1fr);} .pw-item .n{font-size:1.8rem;}}
.pw-act{margin:var(--sp-4) 0 0;}
.pw-act .btn-lines{display:inline-flex;align-items:center;min-height:44px;}
.pw-act .btn-lines:hover{color:var(--orange);border-color:var(--orange);}

/* the trust: the policy as a statement, its numbers quiet, in the display face; the portrait as clear as the
   photograph is, in a crisp frame with a hairline edge */
.pw-trust{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:clamp(2rem,5vw,4.5rem);align-items:start;}
.pw-rules{list-style:none;margin:0;padding:0;counter-reset:pw;}
.pw-rules li{display:grid;grid-template-columns:2.2rem minmax(0,1fr);gap:.6rem;padding:1.05rem 0;border-bottom:1px solid var(--rule);color:var(--gray-light);line-height:1.6;font-size:var(--fs-body);}
.pw-rules li:first-child{border-top:1px solid var(--rule);}
.pw-rules li::before{content:counter(pw,decimal-leading-zero);counter-increment:pw;color:var(--gray);font-family:var(--font-display);font-weight:600;font-size:var(--fs-small);letter-spacing:.04em;font-variant-numeric:tabular-nums;padding-top:.2em;}
.pw-sign{display:flex;align-items:center;gap:.8rem;margin-top:1.4rem;}
.pw-sign img{width:44px;height:44px;border-radius:50%;object-fit:cover;object-position:50% 20%;background:var(--card);border:1px solid var(--edge);}
.pw-sign span{color:var(--white);font-family:var(--font-display);font-weight:600;font-size:var(--fs-body-s);}
.pw-sign span small{display:block;color:var(--gray);font-family:var(--font-body);font-weight:400;font-size:var(--fs-micro);letter-spacing:.1em;text-transform:uppercase;}
.pw-note{color:var(--gray);font-size:var(--fs-small);margin:1rem 0 0;}
.pw-note a{color:var(--gray-light);}
.pw-portrait{margin:var(--sp-3) 0 0;max-width:22rem;position:relative;border:1px solid var(--edge);overflow:hidden;}
.pw-portrait img{display:block;width:100%;height:auto;}

/* the close: the card over the pushed page's blurred photograph of the handshake (a real photograph, blurred
   and veiled so the form reads), which comes out of the page's dark and goes back into it in eased steps; a
   hairline frame, no corner marks; the form as it was */
.pw-contact{position:relative;isolation:isolate;overflow:hidden;padding:clamp(4rem,9vw,7rem) var(--gutter) clamp(3.5rem,8vw,6rem);}
.pw-contact-bg{position:absolute;inset:-40px;z-index:-2;background:url('../../assets/images/partners-coupe-icare-soft.webp') 58% 45%/cover no-repeat;filter:blur(16px) saturate(1.1);transform:scale(1.05);}
.pw-contact::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:@@CLOSE_SHADE@@;}
.pw-contact-in{position:relative;max-width:var(--measure);margin:0 auto;display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(2rem,5vw,4.5rem);
  padding:clamp(1.8rem,4.5vw,3.4rem);border:1px solid color-mix(in srgb,var(--white) 10%,transparent);background:color-mix(in srgb,var(--bg) 66%,transparent);}
.pw-contact-copy .kicker{display:block;margin-bottom:.8rem;}
.pw-contact-copy h2{font-family:var(--font-display);font-weight:800;font-size:var(--fs-h2);line-height:1.12;color:var(--white);margin:0 0 1rem;}
.pw-contact-copy > p{color:var(--gray-light);font-size:var(--fs-body);line-height:1.7;margin:0;}
.pw-direct{margin-top:1.4rem!important;font-size:var(--fs-small)!important;color:var(--gray)!important;}
.pw-direct a{color:var(--gray-light);}
.pw-form{display:flex;flex-direction:column;gap:1.1rem;}
.pw-row2{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem;}
.pw-field{display:flex;flex-direction:column;gap:.45rem;}
.pw-field > span{font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--gray-light);}
.pw-field > span em{font-style:normal;letter-spacing:0;text-transform:none;color:var(--gray);}
.pw-field input,.pw-field textarea{width:100%;font:inherit;font-size:var(--fs-body);color:var(--white);background:color-mix(in srgb,var(--bg) 75%,transparent);border:1px solid var(--edge);
  padding:.85rem .95rem;border-radius:0;outline:none;transition:border-color var(--dur-s) var(--ease),background var(--dur-s) var(--ease);}
.pw-field textarea{resize:vertical;min-height:8.5rem;line-height:1.6;}
.pw-field input::placeholder,.pw-field textarea::placeholder{color:var(--gray);}
.pw-field input:focus,.pw-field textarea:focus{border-color:var(--live);background:color-mix(in srgb,var(--bg) 95%,transparent);}
.pw-interest{border:0;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem;}
.pw-interest legend{font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase;color:var(--gray-light);margin-bottom:.55rem;padding:0;}
.pw-interest label{position:relative;cursor:pointer;}
.pw-interest input{position:absolute;opacity:0;width:1px;height:1px;}
.pw-interest span{display:inline-flex;align-items:center;min-height:44px;padding:.45rem .9rem;border:1px solid var(--edge);color:var(--gray-light);font-size:var(--fs-small);
  background:color-mix(in srgb,var(--bg) 50%,transparent);transition:border-color var(--dur-s) var(--ease),color var(--dur-s) var(--ease),background var(--dur-s) var(--ease);}
.pw-interest input:checked + span{border-color:var(--orange);color:var(--white);background:color-mix(in srgb,var(--orange) 14%,transparent);}
.pw-interest input:focus-visible + span{outline:2px solid var(--orange);outline-offset:2px;}
.pw-send{display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;margin-top:.3rem;}
.pw-status{margin:0;font-size:var(--fs-small);color:var(--gray-light);flex:1;min-width:12rem;}
.pw-status[data-state="bad"]{color:var(--orange);}

/* the footer follows the form closely on the page's own dark: no drawn ridge, no glow left alone above it
   (as on India); here alone, so the footer markup and every other page's footer are as they were */
html footer{padding-top:0;background:none;}
html footer .footer-content{padding-top:var(--sp-4);}
html footer::after{display:none;}

@media (max-width:820px){
  /* phones: the photograph gets its own screen space at the top, the words follow beneath it */
  .pw-hero{display:block;min-height:0;}
  .pw-hero-photo{position:relative;inset:auto;width:auto;height:58svh;min-height:320px;
    -webkit-mask-image:@@HERO_MASK_P@@;mask-image:@@HERO_MASK_P@@;}
  .pw-hero-photo img{object-position:64% 40%;}
  .pw-hero-copy{padding:0 var(--gutter) 2rem;margin-top:-3.2rem;}
  .pw-caption{display:none;}
  .pw-air{display:block;min-height:0;}
  .pw-air-photo{aspect-ratio:9/10;-webkit-mask-image:linear-gradient(0deg,transparent 0,var(--bg) 26%);mask-image:linear-gradient(0deg,transparent 0,var(--bg) 26%);}
  .pw-air-photo img{object-position:50% 40%;}
  .pw-air-copy{max-width:none;margin-top:1.4rem;padding-bottom:2.5rem;}
  .pw-air-cap{position:relative;right:auto;bottom:auto;text-align:left;margin:-2.4rem var(--gutter) 0;}
  .pw-rec-in{grid-template-columns:minmax(0,1fr);align-items:start;}
  .pw-journey::before,.pw-fill{left:calc(var(--gutter) + 10px);}
  .pw-chapter{padding-left:2.8rem;}
  .pw-node{width:21px;height:21px;font-size:.55rem;}
  .pw-trust,.pw-contact-in{grid-template-columns:1fr;}
  .pw-portrait{max-width:none;}
}
@media (max-width:560px){ .pw-row2{grid-template-columns:1fr;} }
@media (prefers-reduced-motion:reduce){
  :is(#v4-main,footer) *,:is(#v4-main,footer) *::before,:is(#v4-main,footer) *::after{transition:none;}
}
"""
CSS = (CSS.replace("@@HERO_MASK@@", HERO_MASK).replace("@@HERO_MASK_P@@", HERO_MASK_P)
       .replace("@@AIR_SHADE@@", AIR_SHADE).replace("@@CLOSE_SHADE@@", CLOSE_SHADE).replace("@@EDGE_FADE@@", EDGE_FADE))
if "@@" in CSS:
    raise SystemExit("v4_partners: a placeholder left in the CSS")

# ---------- the page's own words, as the pushed page has them ----------
FIGS = [("Podcast streams", "100,000+"), ("Countries reached", "130+"),
        ("Long-form interviews", "80"), ("Years flying", "10+")]
FORMATS = [
    ("01", "Podcast", "Sponsored segments",
     "A segment in a long-form episode, disclosed at the start, heard by pilots who stay for the whole conversation."),
    ("02", "Newsletter", "The Atlas list",
     "A sponsor slot in my newsletter, which goes out about four times a month with new episodes, trip updates and field notes."),
    ("03", "Video", "YouTube episodes",
     "An integration in the video edition of an episode on my YouTube channel."),
    ("04", "Expeditions", "Tour partners",
     "Gear, instruments or services in the hands of pilots on my Kenya and India expeditions."),
]


AIR = ('<section class="pw-air" aria-label="In the air">\n'
       '  <div class="pw-air-photo"><picture><source type="image/webp" srcset="img/partners/oslo-festival-900.webp 900w, img/partners/oslo-festival-1600.webp 1600w" sizes="(max-width: 820px) 100vw, 56vw">'
       '<img src="img/partners/oslo-festival-1600.jpg" srcset="img/partners/oslo-festival-900.jpg 900w, img/partners/oslo-festival-1600.jpg 1600w" sizes="(max-width: 820px) 100vw, 56vw" width="1600" height="1777" loading="lazy" '
       'alt="A paraglider flying low over the OverOslo festival crowd at Grefsenkollen, Oslo, a forest behind"></picture>'
       '</div>\n'
       '  <p class="pw-air-cap"><span>OverOslo, June 2025</span>Over the festival crowd at Grefsenkollen</p>\n'
       '  <div class="pw-air-copy">\n'
       '    <span class="kicker">In the air</span>\n'
       '    <h2>The Name Flies With Me</h2>\n'
       '    <p>Every flight carries the Paragliding Atlas name, on the harness and on camera.</p>\n'
       '    <p>Above the OverOslo festival in 2025, a whole crowd looked up at once. A brand in the air reaches people in a way no feed can.</p>\n'
       '  </div>\n'
       '</section>')


def figures():
    """The figures under the opening, big and still. Their fold waits for the owner's sources (the docstring)."""
    rows = "\n".join('    <div><dt>%s</dt><dd>%s</dd></div>' % f for f in FIGS)
    return ('</header>\n\n<section class="pw-stats" aria-label="Audience at a glance">\n'
            '  <dl class="pw-figs">\n%s\n  </dl>\n</section>' % rows)


TILE = re.compile(r'<a class="pw-tile" href="[^"]+"[^>]*>.*?</a>', re.S)


def reel(region):
    """Two still rows of 14: each of the 28 episode tiles once, in the pushed page's order (its loop showed
    each row twice). The tiles' own markup is kept as it is."""
    tiles = []
    for t in TILE.findall(region):
        if t not in tiles:
            tiles.append(t)
    if len(tiles) != 28:
        fail("reel: expected 28 episode tiles, found %d" % len(tiles))
    # each row scrolls sideways, so it takes keyboard focus (arrow keys scroll it) and a name (27 Oct, axe)
    rows = ['    <div class="pw-row" tabindex="0" role="region" aria-label="Partners, row %d"><div class="pw-track">%s</div></div>'
            % (k + 1, "".join(tiles[i:i + 14])) for k, i in enumerate((0, 14))]
    return '<div class="pw-rows">\n%s\n  </div>' % "\n".join(rows)


def formats():
    """The pushed page's editorial list, row for row and word for word, without its arrows (they promised a
    link that was not there); one quiet action under it."""
    rows = "\n".join('      <div class="pw-item"><span class="n">%s</span><h3><small>%s</small>%s</h3><p>%s</p></div>' % f
                     for f in FORMATS)
    return ('<div class="pw-list">\n%s\n    </div>\n'
            '    <p class="pw-act"><a class="btn-lines" href="#enquire">Start a conversation</a></p>' % rows)


# what a partner gets, in the record page's own words (its offer: the Title Partner and one line of what that
# partner gets, word for word)
RECORD_GETS = ("Title Partner", "Your mark on kit and on camera")


def record():
    """The record attempt, in the record page's own words (prototypes/v4/record-attempt.html: its kicker,
    title, line, window, what its Title Partner gets and its "Partner on the attempt"); between v4:needs
    marks, so the switch drops it whole while the record page is prototype-only."""
    return ('<!-- v4:needs record-attempt.html -->\n'
            '<section class="pw-rec" aria-labelledby="pwRecord">\n'
            '  <div class="pw-rec-in">\n'
            '    <div>\n'
            '      <span class="kicker">World Record Attempt &middot; Kerio Valley, Kenya</span>\n'
            '      <h2 id="pwRecord">The Speed Record Attempt</h2>\n'
            '    </div>\n'
            '    <div>\n'
            '      <p>Two world records for speed: 100 km and 200 km, out and return.</p>\n'
            '      <dl class="pw-rec-w"><dt>Window</dt><dd>18 Jan to 12 Feb 2027</dd><dt>%s</dt><dd>%s</dd></dl>\n'
            '      <a class="btn-lines" href="record-attempt.html">Partner on the attempt</a>\n'
            '    </div>\n'
            '  </div>\n'
            '</section>\n'
            '<!-- /v4:needs -->' % RECORD_GETS)


# the close keeps the pushed page's blurred photograph behind its card
CLOSE = '<div class="pw-contact-bg" aria-hidden="true"></div>\n  '

MOTION = r"""<script>
/* The flight line, the page's one moment (tools/v4_partners.py). One loop eases --jp toward the scroll: each
   frame closes a share of the gap by the time passed, so a flick of the wheel becomes a glide with weight that
   settles, and the loop stops once it has arrived; the next scroll starts it again. A chapter's node lights
   when the line reaches it. Without this script, and with reduced motion, the line is drawn whole and both
   nodes lit (.pw-glide is added only here). Nothing else on the page moves on its own. */
(function(){
  var j=document.getElementById('pwJourney');
  if(!j||!window.requestAnimationFrame||matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var cs=[].slice.call(j.querySelectorAll('.pw-chapter')), top=0, h=1, vh=1, at=[], now=-1, raf=0, last=0;
  function measure(){
    var y=scrollY, r=j.getBoundingClientRect(); top=r.top+y; h=Math.max(1,r.height); vh=innerHeight;
    at=cs.map(function(c){ var n=c.querySelector('.pw-node'), b=(n||c).getBoundingClientRect(); return (b.top+y+b.height/2-top)/h; });
  }
  function frame(t){
    raf=0; var dt=last?Math.min(64,Math.max(1,t-last)):16; last=t;
    var to=Math.max(0,Math.min(1,(scrollY+vh*.6-top)/h));
    var v=(now<0||Math.abs(to-now)<.0005)?to:now+(to-now)*(1-Math.exp(-dt/140));
    if(v!==now){ now=v; j.style.setProperty('--jp',v.toFixed(4)); cs.forEach(function(c,i){ c.classList.toggle('is-on',v>=at[i]); }); }
    if(v!==to) raf=requestAnimationFrame(frame); else last=0;
  }
  function go(){ if(!raf) raf=requestAnimationFrame(frame); }
  function again(){ measure(); last=0; go(); }
  /* the line starts where the scroll is, its nodes already as they should be: no transition on arrival */
  measure(); j.classList.add('pw-glide','pw-still'); frame(performance.now()); void j.offsetWidth; j.classList.remove('pw-still');
  addEventListener('scroll',go,{passive:true});
  addEventListener('resize',again,{passive:true});
  addEventListener('load',again);
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(again);
})();
</script>
"""

# ---------- what the first run checks on the pushed page ----------
PUSHED_STYLE = "\n  /* Partner With Me. One continuous story: the Coupe Icare handshake opens it and closes it,"
FORM_SCRIPT = re.compile(r"<script>\n/\* The enquiry opens a ready-written email to Aninder,.*?</script>\n", re.S)
STYLE = re.compile(r"(\n<style>)(.*?)(</style>\n)(?=<!-- site-schema -->)", re.S)


def ids(s):
    return set(re.findall(r'\sid="([^"]+)"', s))


def links(s):
    return set(re.findall(r'\shref="([^"]+)"', s))


def h1(s):
    return re.findall(r"<h1\b[^>]*>.*?</h1>", s, re.S)


def blank_style(head):
    return STYLE.sub(lambda m: m.group(1) + m.group(3), head, 1)


def patch(src):
    if src.count('<main id="v4-main">') != 1 or src.count("</main>") != 1:
        fail("expected one <main id=\"v4-main\"> and one </main>")
    head, rest = src.split('<main id="v4-main">', 1)
    main, tail = rest.split("</main>", 1)

    # the page's own <style>, right before <!-- site-schema -->, rewritten whole
    st = list(STYLE.finditer(head))
    if len(st) != 1:
        fail("the page's own <style> before <!-- site-schema --> was not found once")
    if not (st[0].group(2).startswith("/* v4p") or st[0].group(2).startswith(PUSHED_STYLE)):
        fail("the page's own <style> is neither the pushed one nor this tool's")
    if "<!--" in CSS or "</style" in CSS:
        fail("an HTML mark in the CSS")
    head = head[:st[0].start(2)] + CSS + head[st[0].end(2):]

    # the opening's figures leave the photograph: they stand under it
    if held(main, "figures") is None:
        old = re.search(r'<section class="pw-stats" aria-label="Audience at a glance">(.*?)</section>', main, re.S)
        if not old:
            fail("figures: the stats band was not found")
        got = re.findall(r"<b[^>]*>([^<]*)</b><span>([^<]*)</span>", old.group(1))
        if [(b, a) for a, b in got] != FIGS:
            fail("figures: the stats band does not hold the four figures as expected: %r" % got)
    main = marked(main, "figures", figures(), r'(?<=\n)  <section class="pw-stats" aria-label="Audience at a glance">\n.*?</section>\n</header>')

    # the reel: two still rows, each tile once
    region = held(main, "reel")
    if region is None:
        m = re.search(r'<div class="pw-rows">\n.*?</div></div>\n  </div>', main, re.S)
        if not m:
            fail("reel: the rows were not found")
        region = m.group(0)
        if len(TILE.findall(region)) != 56:
            fail("reel: expected the loop's 56 tiles, found %d" % len(TILE.findall(region)))
    main = marked(main, "reel", reel(region), r'<div class="pw-rows">\n.*?</div></div>\n  </div>')

    # the band in the air: the Oslo festival photograph and its caption, a line for brands
    main = marked(main, "air", AIR, r'<section class="pw-air" aria-label="In the air">\n.*?</section>')

    # the record attempt, after the band in the air, before the flight line
    main = marked(main, "record", record(), r'(?<=</section>\n)(?=\n<div class="pw-journey" id="pwJourney">)')

    # the formats, the pushed list without its arrows; one quiet action under them
    if held(main, "formats") is None:
        old = re.search(r'<div class="pw-list">\n(.*?)\n    </div>\n  </section>', main, re.S)
        if not old:
            fail("formats: the list was not found")
        got = re.findall(r'<div class="pw-item"><span class="n">(\d\d)</span><h3><small>([^<]*)</small>([^<]*)</h3><p>([^<]*)</p>', old.group(1))
        if [tuple(g) for g in got] != FORMATS:
            fail("formats: the four formats are not as expected: %r" % got)
    main = marked(main, "formats", formats(), r'<div class="pw-list">\n.*?\n    </div>(?=\n  </section>)')

    # the close: the blurred photograph stays behind the card (an earlier run of this tool took it out; its
    # marks now hold it as the pushed page has it)
    main = marked(main, "close", CLOSE, r'<div class="pw-contact-bg" aria-hidden="true"></div>\n  ')

    # the scripts: the count-up goes; the flight line's loop takes the old scroll handler's place
    main = marked(main, "motion", MOTION,
                  r'<script>\n/\* Count the audience figures up once.*?</script>\n<script>\n/\* Scroll fills the flight line.*?</script>\n')

    out = head + '<main id="v4-main">' + main + "</main>" + tail

    # ---- the checks ----
    if "—" in out:
        fail("an em dash crept in")
    mine = CSS + figures() + reel(held(main, "reel")) + record() + formats() + MOTION
    if RAW.search(mine):
        fail("a raw colour crept in: %s; use the design tokens" % RAW.search(mine).group(0))
    if h1(out) != h1(src):
        fail("the h1 changed")
    if ids(out) != ids(src) | NEW_IDS:
        fail("the ids changed: %r" % sorted(ids(out) ^ (ids(src) | NEW_IDS)))
    if links(out) != links(src) | NEW_LINKS:
        fail("the link targets changed: %r" % sorted(links(out) ^ (links(src) | NEW_LINKS)))
    o_head = out.split('<main id="v4-main">', 1)[0]
    if blank_style(o_head) != blank_style(src.split('<main id="v4-main">', 1)[0]) or o_head.count("<style>") != src.split('<main id="v4-main">', 1)[0].count("<style>"):
        fail("the head changed outside the page's own <style>")
    if out.split("</main>", 1)[1] != src.split("</main>", 1)[1]:
        fail("something after </main> changed")
    fs = FORM_SCRIPT.findall(src)
    if len(fs) != 1 or FORM_SCRIPT.findall(out) != fs:
        fail("the form script is not byte for byte as it was")
    if "v2-tbd" in out or "[to supply]" in out:
        fail("a [to supply] mark: the page speaks to a brand, in the site's own words only")
    if "About these numbers" in out or "v4-fold" in held(out, "figures"):
        fail("the figures' fold waits for the owner's sources (100,000+ streams, 10+ years)")
    rec_page = os.path.join(V4, "record-attempt.html")
    if os.path.exists(rec_page):
        rp = open(rec_page, encoding="utf-8").read()
        if "<h3>%s</h3>" % RECORD_GETS[0] not in rp or "<li>%s</li>" % RECORD_GETS[1] not in rp:
            fail("what a partner gets is no longer the record page's own words")
    if "font-mono" in CSS or "text-stroke" in CSS:
        fail("a mono or outlined numeral: numerals are in the display face")
    if "<svg" in formats() or ":hover" in "".join(re.findall(r"\.pw-item[^{]*\{", CSS)):
        fail("the formats keep no arrow and nothing moves under the pointer")
    if "filter" in "".join(re.findall(r"\.pw-portrait[^{]*\{[^}]*\}", CSS)):
        fail("the portrait is shown as clear as it is")
    if "::before" in "".join(re.findall(r"\.pw-contact-in[^{]*\{", CSS)) or "::after" in "".join(re.findall(r"\.pw-contact-in[^{]*\{", CSS)):
        fail("the enquiry card has no corner marks")
    if v2_site.needs(out, V4)[1]:
        fail("the v4:needs marks: %s" % "; ".join(v2_site.needs(out, V4)[1]))
    if "data-count" in out or "pwDrift" in out or "pwPush" in out or "pwArrive" in out:
        fail("a count-up or a self-running animation is still there")
    return out


def main():
    src = open(PAGE, encoding="utf-8").read()
    out = patch(src)
    if out != src:
        open(PAGE, "w", encoding="utf-8").write(out)
    print("v4_partners: partners.html %s, sha256 %s" % ("patched" if out != src else "unchanged",
                                                      hashlib.sha256(out.encode("utf-8")).hexdigest()[:16]))


if __name__ == "__main__":
    main()
