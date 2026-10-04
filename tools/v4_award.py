#!/usr/bin/env python3
"""
The award pass (owner, 4 Oct 2026: "go ahead with 1, 3, 4, 5, 6 and 9" of
the review in docs/v4-report.md). The page changes that live in HTML; the
header, the labels and the motion language are CSS and script (src/v2.css,
src/v2-immersive.js, "THE AWARD PASS").

6. THE KNOWLEDGE BASE LANDING, CALM. The hyperspace door (a full-screen
   starburst shown once a visit) is switched off, and the scrolling wall of
   episode stills behind the title gives way to one Gold line drawing: a
   thermal climb up an altitude scale, the five levels of the page marked on
   it at their own heights (600 m to 4,000 m, from the page's sections), each
   a link to its level. Drawn from the page's own figures; nothing new.

1. EVERY PAGE ITS OWN OPENING. Home and the trips keep the full-bleed film:
   that is their moment. Two pages stop copying it:
   - About: an editorial split, the words on the plain page and the
     photograph framed beside them (CSS only, src/v2.css);
   - Podcast: the people first. Every guest's name, from episode-meta.json,
     set as a quiet wall of type behind the title; one name at a time
     brightens. The field of gliders photograph leaves the header.

Every block sits between markers, so a rerun replaces it.

    python3 tools/v4_award.py
"""
import html as H
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


# ---------------------------------------------------------------- 6. KB landing
DOOR_ON = "if(!deep&&!calm&&!seen){"
DOOR_OFF = "if(false){ /* v4, the award pass: the door is off (tools/v4_award.py) */"


def climb_svg(levels):
    """levels: [(n, alt_m, name, count_text)] low to high."""
    W, Hh, top, bot, axis = 700, 660, 50, 610, 640
    amax = 4500.0
    y = lambda a: bot - a / amax * (bot - top)
    # the climb: a thermal turning as it rises, drawn as one line
    pts = []
    for i in range(0, 361):
        t = i / 360.0
        alt = 80 + t * (4300 - 80)
        r = 46 + 22 * math.sin(t * math.pi)
        x = 470 + r * math.sin(t * math.pi * 2 * 6.5) + (t - 0.5) * 40
        pts.append((x, y(alt)))
    d = "M" + "L".join("%.1f,%.1f" % p for p in pts)
    out = ['<svg class="v4-climb" viewBox="0 0 %d %d" role="group" aria-label="The five levels of the knowledge base, as a climb from 600 m to 4,000 m">' % (W, Hh)]
    # the altitude scale
    ticks = []
    for a in range(0, 4501, 250):
        big = a % 1000 == 0
        ticks.append("M%d,%.1fL%d,%.1f" % (axis, y(a), axis + (14 if big else 7), y(a)))
    out.append('<path class="v4-climb-axis" d="M%d,%d L%d,%d"/>' % (axis, top - 10, axis, bot))
    out.append('<path class="v4-climb-ticks" d="%s"/>' % "".join(ticks))
    for a in range(1000, 4501, 1000):
        out.append('<text class="v4-climb-km" x="%d" y="%.1f">%s</text>' % (axis + 20, y(a) + 4, "{:,}".format(a)))
    out.append('<path class="v4-climb-line" d="%s"/>' % d)
    # the levels, where the climb crosses their height
    for k, (n, alt, name, count) in enumerate(levels):
        ly = y(alt)
        # the point of the climb nearest that height
        px = min(pts, key=lambda p: abs(p[1] - ly))[0]
        out.append(
            '<a class="v4-climb-lv" href="#lvl-%d" style="--k:%d" aria-label="%s m, %s, %s">'
            '<path class="v4-climb-dash" d="M%.1f,%.1fL%d,%.1f"/>'
            '<circle class="v4-climb-dot" cx="%.1f" cy="%.1f" r="5"/>'
            '<text class="v4-climb-alt" x="%d" y="%.1f">%s m</text>'
            '<text class="v4-climb-name" x="%d" y="%.1f">%s</text>'
            '<text class="v4-climb-n" x="%d" y="%.1f">%s</text></a>'
            % (n, k, "{:,}".format(alt), H.escape(name), H.escape(count),
               275, ly, axis, ly, px, ly,
               0, ly - 6, "{:,}".format(alt),
               0, ly + 14, H.escape(name),
               0, ly + 31, H.escape(count)))
    out.append("</svg>")
    return "".join(out)


def kb_landing():
    p = os.path.join(V4, "knowledge-base.html")
    s = read(p)
    if DOOR_ON in s:
        s = s.replace(DOOR_ON, DOOR_OFF, 1)
    elif DOOR_OFF not in s:
        raise SystemExit("v4_award: the door switch was not found")
    levels = []
    for m in re.finditer(r'class="iris-node" data-lv="(\d+)" href="#lvl-(\d+)" aria-label="([\d,]+) m, ([^,"]+(?:, [^0-9"][^,"]*)*?), (\d+ episodes?)"', s):
        levels.append((int(m.group(2)), int(m.group(3).replace(",", "")), H.unescape(m.group(4)), m.group(5)))
    if len(levels) != 5:
        raise SystemExit("v4_award: expected five levels, found %d" % len(levels))
    block = "<!-- v4-climb -->" + climb_svg(levels) + "<!-- /v4-climb -->"
    if "<!-- v4-climb -->" in s:
        s = re.sub(r"<!-- v4-climb -->.*?<!-- /v4-climb -->", lambda m: block, s, count=1, flags=re.S)
    else:
        a = s.index('<div class="clb-wall" id="clbWall">')
        b = s.index('<div class="clb-scrim"', a)
        s = s[:a] + block + "\n    " + s[b:]
    write(p, s)
    print("v4_award: knowledge base landing: the door off, the climb in (%s)" % ", ".join("%d m" % l[1] for l in levels))


POD_OLD = ('<div class="kit-hero-media">\n    <picture><source srcset="../../assets/images/pod-hero-gemona.webp" type="image/webp">'
           '<img src="../../assets/images/pod-hero-gemona.jpg" width="1920" height="1080" '
           'alt="A field of paragliders climbing through broken cloud above a valley" fetchpriority="high"></picture>\n  </div>')


def podcast_voices():
    import json
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    names, seen = [], set()
    for m in sorted(meta, key=lambda m: m.get("published") or "", reverse=True):
        for g in re.split(r"\s*(?:&| and |,)\s*", m.get("guest") or ""):
            g = g.strip()
            if g and g != "Aninder Singh" and g.lower() not in seen:
                seen.add(g.lower())
                names.append(g)
    lit = set(range(3, len(names), max(1, len(names) // 9)))
    # the lit ones numbered in order, for the CSS sequence
    out, j = [], 0
    for i, n in enumerate(names):
        if i in lit:
            out.append('<span class="is-lit" style="--n:%d">%s</span>' % (j, H.escape(n))); j += 1
        else:
            out.append("<span>%s</span>" % H.escape(n))
    block = ('<!-- v4-voices --><div class="kit-hero-media v4-voices" aria-hidden="true" style="--lit:%d"><p>%s</p></div><!-- /v4-voices -->'
             % (j, " ".join(out)))
    p = os.path.join(V4, "podcast.html")
    s = read(p)
    if "<!-- v4-voices -->" in s:
        s = re.sub(r"<!-- v4-voices -->.*?<!-- /v4-voices -->", lambda m: block, s, count=1, flags=re.S)
    elif POD_OLD in s:
        s = s.replace(POD_OLD, block, 1)
    else:
        raise SystemExit("v4_award: podcast hero not found")
    s = s.replace('<header class="kit-hero v2-pod-hero">', '<header class="kit-hero v2-pod-hero v4-voices-hero">', 1)
    write(p, s)
    print("v4_award: podcast opening: %d guests, %d lit in turn" % (len(names), j))


def main():
    kb_landing()
    podcast_voices()


if __name__ == "__main__":
    main()
