#!/usr/bin/env python3
"""
Build prototypes/v6/: the live site with the owner's flying footage in place.

The owner gave twelve clips (3 Oct 2026) and asked to see them used "in a new
proto site". v6 is a copy of only the pages that get footage, taken from the
live pages as they stand, so it shows exactly what the change would look like.
Every link in a copied page is pointed back at the live file, except links
between two v6 pages, which stay inside v6. Pages are noindex.

The clips are encoded once (tools/data/v6-footage, see FOOTAGE below) into
assets/video/: 1080p and 720p, WebM and MP4, no sound, each under
4 MB, plus a still. They play through the site's own looping footage code
(script.js, LOOPING FOOTAGE): only while on screen, never for reduced motion,
Save-Data or a slow connection, fading in over the still.

Captions and alt text say only what is visible: where the clips were filmed is
not known yet.

    python3 tools/v6_build.py
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V6 = os.path.join(ROOT, "prototypes", "v6")
SRC = os.environ.get("V6_FOOTAGE", "")   # folder of encoded clips, only needed to (re)copy them

# page -> (clip, where it goes, what the clip shows)
PLAN = {
    "index.html": (11, "bg:.newsletter", "Flying above a glacier, the wing tip in view"),
    "about.html": (2, "media:.ab2-hero-media", "A pilot in an ATLAS harness above a green valley"),
    "mission.html": (12, "bg:.pol-hero", "Flying over pale limestone peaks under a wide sky"),
    "podcast.html": (8, "media:.pod-hero-media", "The wing overhead and lakes below a rocky ridge"),
    "enquire.html": (7, "bg:.enq-hero", "Turning over a green basin with a turquoise lake"),
    "knowledge-base/meteorology.html": (1, "media:.k-hero-media", "Climbing out of cloud as the valley opens up below"),
    "knowledge-base/weather-patterns.html": (4, "media:.k-hero-media", "Flying along a wall of cloud above a wide plain"),
    "knowledge-base/risk-vs-reward.html": (3, "media:.k-hero-media", "Soaring close along a limestone cliff, a second wing alongside"),
    "knowledge-base/flight-mechanics.html": (10, "media:.k-hero-media", "Looking straight down the lines to cliffs and a valley"),
}

SKIP = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/|\{|\$|%|data:)", re.I)
ATTR = re.compile(r'(\s(?:href|src|poster|data-loop)=")([^"]*)(")', re.I)
SRCSET = re.compile(r'(\s(?:srcset)=")([^"]*)(")', re.I)
CSSURL = re.compile(r'(url\((["\']?))([^)"\']+)(\2\))')


def fix(url, rel):
    """A link in the live page `rel`, made to work from prototypes/v6/`rel`."""
    if not url or SKIP.match(url):
        return url
    path, sep, rest = re.match(r"([^?#]*)([?#]?)(.*)", url).groups()
    if not path:
        return url
    live_dir = os.path.dirname(rel)
    target = os.path.normpath(os.path.join(live_dir, path)).replace(os.sep, "/")
    if target in PLAN:                         # another v6 page: stay inside v6
        out = os.path.relpath(target, live_dir or ".")
    else:                                      # anything else: the live file
        out = os.path.relpath(os.path.join(ROOT, target), os.path.join(V6, live_dir))
    return out.replace(os.sep, "/") + sep + rest


def rewrite(html, rel):
    parts = re.split(r"(<script\b[^>]*>.*?</script>)", html, flags=re.S | re.I)
    for i, part in enumerate(parts):
        if i % 2:
            parts[i] = re.sub(r"^<script\b[^>]*>", lambda m: ATTR.sub(
                lambda a: a.group(1) + fix(a.group(2), rel) + a.group(3), m.group(0)), part)
            continue
        part = ATTR.sub(lambda a: a.group(1) + fix(a.group(2), rel) + a.group(3), part)
        part = SRCSET.sub(lambda a: a.group(1) + ", ".join(
            " ".join([fix(c.strip().split()[0], rel)] + c.strip().split()[1:])
            for c in a.group(2).split(",") if c.strip()) + a.group(3), part)
        part = CSSURL.sub(lambda a: a.group(1) + fix(a.group(3), rel) + a.group(4), part)
        parts[i] = part
    return "".join(parts)


def footage(rel, n, where, alt):
    # The clips live where the live site would use them, assets/video/, so
    # going live later adds no second copy of 30 MB of video.
    base = os.path.relpath(os.path.join(ROOT, "assets", "video", "alps-%d" % n),
                           os.path.join(V6, os.path.dirname(rel))).replace(os.sep, "/")
    vid = ('<video data-loop="%s" muted loop playsinline preload="none" aria-hidden="true" '
           'tabindex="-1"></video>' % base)
    kind, sel = where.split(":", 1)
    if kind == "media":
        # Over the photograph or drawing the header already has.
        return sel, vid
    # A backdrop for a band that has none: the still, the clip over it, and a
    # shade so the words stay readable.
    return sel, ('<div class="v6-bg" aria-hidden="true"><img src="%s-poster.jpg" alt="" loading="lazy" '
                 'decoding="async">%s<span class="v6-shade"></span></div>' % (base, vid))


def place(html, sel, block):
    cls = sel.lstrip(".")
    m = re.search(r'<(\w+)[^>]*class="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(cls), html)
    if not m:
        raise SystemExit("v6: no %s" % sel)
    return html[:m.end()] + block + html[m.end():]


def ribbon(rel):
    up = os.path.relpath(V6, os.path.join(V6, os.path.dirname(rel))).replace(os.sep, "/")
    up = "" if up == "." else up + "/"
    names = [("index.html", "Home"), ("about.html", "About"), ("mission.html", "Mission"),
             ("podcast.html", "Podcast"), ("enquire.html", "Enquire"),
             ("knowledge-base/meteorology.html", "Meteorology"),
             ("knowledge-base/weather-patterns.html", "Weather Patterns"),
             ("knowledge-base/risk-vs-reward.html", "Risk vs Reward"),
             ("knowledge-base/flight-mechanics.html", "Flight Mechanics")]
    links = "".join('<a href="%s%s"%s>%s</a>' % (up, p, ' aria-current="page"' if p == rel else "", t)
                    for p, t in names)
    return ('<nav class="v6-ribbon" aria-label="v6 preview pages"><b>v6 footage preview</b>%s</nav>' % links)


def main():
    os.makedirs(os.path.join(ROOT, "assets", "video"), exist_ok=True)
    if SRC:
        for n in sorted({c for c, _, _ in PLAN.values()}):
            for suf in ("1080.mp4", "1080.webm", "720.mp4", "720.webm", "poster.jpg"):
                shutil.copyfile(os.path.join(SRC, "alps-%d-%s" % (n, suf)),
                                os.path.join(ROOT, "assets", "video", "alps-%d-%s" % (n, suf)))
    for rel, (n, where, alt) in PLAN.items():
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        html = rewrite(html, rel)
        # Run-time paths inside the page's own scripts (the homepage hero
        # builds its video path in script) point at the live files too.
        up_live = os.path.relpath(ROOT, os.path.join(V6, os.path.dirname(rel))).replace(os.sep, "/") + "/"
        html = html.replace("'assets/video/", "'" + up_live + "assets/video/")
        sel, block = footage(rel, n, where, alt)
        html = place(html, sel, block)
        up = os.path.relpath(V6, os.path.join(V6, os.path.dirname(rel))).replace(os.sep, "/")
        up = "" if up == "." else up + "/"
        if 'name="robots"' in html:
            html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, nofollow">', html)
        else:
            html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
        html = html.replace("</head>", '<link rel="stylesheet" href="%sv6.css">\n</head>' % up, 1)
        html = html.replace("</body>", ribbon(rel) + "\n</body>", 1)
        dest = os.path.join(V6, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(html)
        print("v6: %-40s clip %d" % (rel, n))


if __name__ == "__main__":
    main()
