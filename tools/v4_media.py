#!/usr/bin/env python3
"""Media: comp coverage for organisers and sponsors (chat 17, 3 Nov 2026).

Owner, 3 Nov: "this is my face to asking people to trust my site ... where I convert eyeballs into customers ... in
an elegant and effective way." The page speaks to comp organisers and the brands that sponsor them, nobody else
(pilots and fans are served by the event pages). Its design is designer E's (Cloudbase) mock "Pull Back To The
Coverage", picked by all three judges, built here with the fixes and the parts taken from F and D that
docs/designers/media-build-spec.md lists (each item has an id, quoted in the comments below):

  media.html                       the opening (one shot of a race, the promise, who hired him, three numbers with
                                   their sources); scrolling pulls the camera back until that shot is the second of
                                   the four posters; the packages (no prices); the reach (31,250 over the gaggle, the
                                   2026 season on its dates with a Today mark); the quote (EXAMPLE); the work (13
                                   videos that play in place, 10 stills in the viewer); delivery; the questions; the
                                   dates form that hands over to enquire.html?trip=media; the newsletter in one line
  media-srs-piedrahita-2026.html   one comp, for pilots: its videos and every chosen still, by task (A5: kept as it
                                   was, now on the shared CSS and JS; its photo pick is still with the owner)

Shared files: prototypes/v4/v4-media.css (both pages, A1) and prototypes/v4/v4-media.js (play in place, the reel,
the chips, the justified rows, the photo viewer, and on this page the pull-back, the slate, the package picks, the
hand-off and the phone bar). Both are linked with ?v= their content hash. Reduced motion and no JavaScript show the
finished page.

Facts, each from the owner (3 Nov), their Canva pitches, or their YouTube videos (vidIQ, 3 Nov); nothing else. A
missing fact is [to supply] (class v2-tbd); example data is marked EXAMPLE. Photos are web copies only: WebP 800,
1600 and 2400 px on the long side (tools/v4_media_photos.py), served from MEDIA below.

    python3 tools/v4_media.py                 # writes the two pages
    python3 tools/v4_media.py --media URL/    # with the photos served from URL/ (the preview: img/media-tmp/)
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SHELL = os.path.join(V4, "about.html")
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
WA = "https://wa.me/4796757456"
MEDIA = "https://paraglidingatlas-maker.github.io/media-2026/srs-piedrahita/"
if "--media" in sys.argv:
    MEDIA = sys.argv[sys.argv.index("--media") + 1]
E = html.escape
BUILT = datetime.date.today()
TBD = '<i class="v2-tbd">[to supply]</i>'


def ver(name):
    """the ?v= of a shared file: its content hash, so a change reaches every visitor"""
    return hashlib.md5(open(os.path.join(V4, name), "rb").read()).hexdigest()[:8]


def day(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d").date() if "-" in s else datetime.datetime.strptime(s, "%d %b %Y").date()


# ---------------------------------------------------------------- the photos ----
# stem: (width, height, task, alt)   sizes of the originals; web copies keep the ratio
PH = {
    "SRS_5_T1_9": (3726, 2484, 1, "An orange wing high over a patchwork of fields under cloud"),
    "SRS_5_T2_133-2": (4000, 6000, 2, "An orange and black wing between white clouds"),
    "SRS_5_T2_64": (3625, 2651, 2, "A red and white wing alone in a blue sky"),
    "SRS_5_T2_76": (4000, 6000, 2, "A lime wing above a forested slope"),
    "SRS_5_T2_83": (4000, 6000, 2, "A white wing with a red edge against a deep blue sky"),
    "SRS_5_T3_121": (6000, 4000, 3, "A white wing with a red edge, the pilot seen from below"),
    "SRS_5_T3_127": (1571, 2190, 3, "A red wing seen from below"),
    "SRS_5_T3_150": (2485, 1696, 3, "An orange wing banking in a clear blue sky"),
    "SRS_5_T3_166": (6000, 4000, 3, "A blue and white wing in a deep blue sky"),
    "SRS_5_T3_172": (5373, 3582, 3, "A yellow wing overhead in a blue sky"),
    "SRS_5_T3_21": (5143, 3008, 3, "A red and blue wing over the valley and its winding road"),
    "SRS_5_T3_27": (6000, 4000, 3, "A white and blue wing over the dry plain"),
    "SRS_5_T3_38": (3215, 3802, 3, "An orange wing over fields and trees"),
    "SRS_5_T3_47": (4000, 6000, 3, "A green wing above a winding road"),
    "SRS_5_T3_57": (6000, 4000, 3, "A white wing over the scrub"),
    "SRS_5_T3_63": (6000, 4000, 3, "The gaggle, dozens of wings in the blue"),
    "SRS_5_T3_64": (4000, 6000, 3, "Wings stacked in a climb"),
    "SRS_5_T3_66": (6000, 4000, 3, "The race spread high across the sky"),
    "SRS_5_T3_86": (1809, 2714, 3, "A red wing over the plain"),
    "SRS_5_T3_92": (3394, 2263, 3, "A yellow wing over a green hillside"),
}
SHOT = "SRS_5_T2_133-2"          # the opening's shot, which becomes the Daily Highlights poster
BAND, QUOTE = "SRS_5_T3_63", "SRS_5_T3_66"   # the reach band (the gaggle) and the quote band (the race)
STILLS = ["SRS_5_T3_21", "SRS_5_T3_64", "SRS_5_T3_150", "SRS_5_T1_9", "SRS_5_T3_47", "SRS_5_T3_92",
          "SRS_5_T3_166", "SRS_5_T3_38", "SRS_5_T3_27", "SRS_5_T2_83"]


def src(stem, w):
    return MEDIA + "%s-%d.webp" % (stem, w)


def wide(stem, w):
    """the real width of a web copy: the long side is w, so a portrait copy is narrower"""
    pw, ph = PH[stem][:2]
    return w if pw >= ph else round(w * pw / ph)


def srcset(stem, ws=(800, 1600, 2400)):
    return ", ".join("%s %dw" % (src(stem, w), wide(stem, w)) for w in ws)


def figure(stem, where="Piedrahita 2026"):
    w, h, t, alt = PH[stem]
    r = w / h
    return ('<figure class="md-ph" style="--r:%.4f"><a href="%s" data-full="%s"><img src="%s" srcset="%s" '
            'sizes="(max-width:700px) 70vw, 40vw" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></a>'
            '<figcaption><b>%s, Task %d</b></figcaption></figure>'
            % (r, src(stem, 2400), src(stem, 2400), src(stem, 800), srcset(stem, (800, 1600)),
               1600 if r >= 1 else round(1600 * r), round(1600 / r) if r >= 1 else 1600, E(alt), where, t))


def grid(stems, label):
    return '<div class="md-grid" data-zoom aria-label="%s">%s</div>' % (E(label), "".join(figure(s) for s in stems))


# ---------------------------------------------------------------- the videos ----
# id: (comp, title, views, length, published, episode page or None)
V = {
    "BRAX1XMU390": ("pwc", "Task 1 Highlights", 7342, "6:53", "14 May 2026", "task-1-highlights-15th-paragliding-world-cup-super-final"),
    "7il6yV1vdIc": ("pwc", "Task 2 Highlights", 4034, "8:17", "16 May 2026", "task-2-highlights-15th-paragliding-world-cup-super-final"),
    "FOuAWMeoxs4": ("pwc", "Day 1 Highlights", 3537, "6:44", "13 May 2026", "highlights-day-1-pwca-superfinal-2026"),
    "op1-O01xkH4": ("pwc", "Task 4 Highlights", 3437, "7:47", "18 May 2026", "task-4-highlights-15th-paragliding-world-cup-super-final"),
    "vPnIYYKcvEg": ("pwc", "Task 5 Highlights", 3340, "8:08", "20 May 2026", "task-5-highlights-15th-paragliding-world-cup-super-final"),
    "NXUEyPQ3V4E": ("srs5", "Task 2 Highlights", 2303, "13:46", "6 Sep 2026", "srs-piedrahita-bgd-edition-task-2-highlights"),
    "uCEfssE40u8": ("srs5", "Task 1 Highlights", 1970, "7:38", "27 Aug 2026", "srs-piedrahita-bgd-edition-task-1-highlights"),
    "cuGs7Lk6Dt4": ("srs5", "Day 1: Registration and the Peñas", 1206, "9:04", "23 Aug 2026", "srs-bgd-edition-2026-day-1-registration-pilots-penas-de"),
    "ZL9B5eXip5o": ("srs4", "Live: Task 2", 1145, "5 h 41 min", "25 May 2026", None),
    "SZWQjcO_fWk": ("srs4", "Live: Task 3", 890, "4 h 59 min", "26 May 2026", None),
    "x8sSBSBy4dI": ("srs4", "Live: Task 4, part 1", 853, "1 h 57 min", "29 May 2026", None),
    "PEyO6MXngUw": ("srs4", "Live: Task 5, the final day", 680, "5 h 8 min", "30 May 2026", None),
    "DA4nGop3i9g": ("srs4", "Live: Task 4, part 2", 513, "3 h 55 min", "30 May 2026", None),
}
# the showreel lists them in this order: by comp, the most watched comp first, and by views inside each (buyer-2-3)
_order = [c for c in dict.fromkeys(v[0] for v in V.values())]
assert _order == sorted(_order, key=lambda c: -sum(v[2] for v in V.values() if v[0] == c)), _order
for _c in _order:
    _k = [v[2] for v in V.values() if v[0] == _c]
    assert _k == sorted(_k, reverse=True), (_c, _k)
COMPS = {"pwc": "PWC Super Final, Pegalajar", "srs5": "SRS Piedrahita", "srs4": "SRS Bassano, live"}
REEL = "BRAX1XMU390"
TOTAL = sum(v[2] for v in V.values())             # 31,250 on 3 Nov 2026
assert TOTAL == 31250, TOTAL
COUNTED = "3 Nov 2026"                            # when the views were read (YouTube, vidIQ)


def views(comp):
    return sum(v[2] for v in V.values() if v[0] == comp)


def n(x):
    return "{:,}".format(x)


PLAY = ('<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 1.2v7.6c0 .5.5.8.9.5l5.9-3.8c.4-.2.4-.8 0-1L2.9.7C2.5.4 '
        '2 .7 2 1.2z"/></svg>')


def thumb(v, q="maxresdefault"):
    return "https://i.ytimg.com/vi/%s/%s.jpg" % (v, q)


def frame(v, eager=False):
    c, t, k, ln, d, ep = V[v]
    return ('<div class="md-frame" data-vid="%s"><img src="%s" alt="" width="1280" height="720"%s decoding="async">'
            '<a class="md-play" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" '
            'aria-label="Play %s, %s">%s</a></div>'
            % (v, thumb(v), "" if eager else ' loading="lazy"', v, E(t), E(COMPS[c]), PLAY))


def vmeta(v):
    c, t, k, ln, d, ep = V[v]
    return "%s views &middot; %s" % (n(k), ln)


def now_line(v, with_ep=True):
    """the line under the big frame: short pieces that wrap between them, never inside one, all with the same
    separator (Q2); the episode link on its own row on a phone"""
    c, t, k, ln, d, ep = V[v]
    return ('<p class="md-meta"><span data-m>%s views</span><span data-l>%s</span><span data-d>%s</span>'
            '<span class="md-ep"%s><a href="%s">Read the episode <i aria-hidden="true">&rarr;</i></a></span></p>'
            % (n(k), ln, d, "" if ep else " hidden", "episodes/%s.html" % ep if ep else "#"))


def now_title(v):
    """the big frame's title as the reel list sets it: the film, then its comp on a quieter line (critic-1-6)"""
    c, t, k, ln, d, ep = V[v]
    return '<h3><span data-t>%s</span><small data-c>%s</small></h3>' % (E(t), E(COMPS[c]))


# ---------------------------------------------------------------- the comps ----
# the next comps, in order (H3): the slate and the season line read this list against the visitor's date
UPCOMING = [
    {"key": "tapalpa", "name": "SRS Tapalpa", "place": "Mexico", "edition": "SRS Advance Edition", "where": "Tapalpa, Mexico",
     "first": "2026-11-08", "last": "2026-11-14", "dates": "8 to 14 Nov 2026", "short": "8 to 14 Nov",
     "facts": "7 tasks, up to 120 pilots, 44 countries"},
]
# the comps covered in 2026, in date order (R1); span: the days on the season line (Piedrahita: the comp's own dates;
# the other two: the days their films and broadcasts came out)
SEASON = [
    {"comp": "pwc", "name": "PWC Super Final", "edition": "15th Paragliding World Cup Super Final", "where": "Pegalajar, Spain",
     "when": "May 2026", "made": "5 highlight videos"},
    {"comp": "srs4", "name": "SRS Bassano", "edition": "SRS Skywalk Bassano Edition", "where": "Monte&nbsp;Grappa, Italy",
     "when": "May 2026", "made": "Live commentary: 5 broadcasts, 21&nbsp;h&nbsp;42&nbsp;min on air"},
    {"comp": "srs5", "name": "SRS Piedrahita", "edition": "SRS BGD Edition", "where": "Piedrahita, &Aacute;vila, Spain",
     "when": "22 to 29 Aug 2026", "made": "Stills and 3 highlight videos", "span": ("2026-08-22", "2026-08-29")},
]
LINE = (datetime.date(2026, 5, 1), datetime.date(2026, 12, 1))   # the 2026 season line, 1 May to 1 Dec


def at(dt):
    return (dt - LINE[0]).days / (LINE[1] - LINE[0]).days


def span(ev):
    if "span" in ev:
        a, b = day(ev["span"][0]), day(ev["span"][1])
    else:
        ds = [day(v[4]) for v in V.values() if v[0] == ev["comp"]]
        a, b = min(ds), max(ds)
    return a, b


def next_up():
    for u in UPCOMING:
        if day(u["last"]) >= BUILT:
            return u
    return None


# ---------------------------------------------------------------- the shell ----
ICON_WA = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.3-18.1C18.1 1.5 15.1.2 12 .2 5.5.2.2 5.5.2 12c0 2.1.5 4.1 1.6 5.9L.1 24l6.3-1.6c1.7.9 3.7 1.4 5.6 1.4 6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.5-8.3z"/></svg>')

VIEWER = ('<dialog class="v4i-fl-lb" id="v4i-fl-lb" aria-label="The photograph, enlarged"><div class="v4i-fl-lbs"><img alt="" draggable="false"></div>'
          '<button class="v4i-fl-lbx" type="button" aria-label="Close the photograph"></button><span class="v4i-fl-lbc"></span>'
          '<button class="v4i-fl-lbn v4i-fl-lbp" type="button" hidden aria-label="Previous photograph"><svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg></button>'
          '<button class="v4i-fl-lbn v4i-fl-lbnx" type="button" hidden aria-label="Next photograph"><svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg></button>'
          '<span class="v4i-fl-lbh" aria-hidden="true">Click to come closer &middot; Scroll or pinch for more &middot; Drag to move &middot; Arrows for the next &middot; Click outside to close</span></dialog>')


def shell(title, desc, canon, og_img, name, main, enquire=None):
    """the About page's head, nav and footer around main; enquire: where the header's Enquire Now goes (H5)"""
    s = open(SHELL).read()

    def rep(a, b, k=1):
        nonlocal s
        assert s.count(a) == k, (a[:80], s.count(a))
        s = s.replace(a, b)
    rep('{"k":"page","n":"About Me"}', json.dumps({"k": "page", "n": name}, separators=(",", ":")))
    rep("<title>About Me: Paragliding Atlas</title>", "<title>%s: Paragliding Atlas</title>" % E(title))
    d0 = "Immersive flying safaris guided by seasoned experts in the world&#x27;s most exotic skies."
    rep('<meta name="description" content="%s">' % d0, '<meta name="description" content="%s">' % E(desc))
    rep('<meta property="og:description" content="%s">' % d0, '<meta property="og:description" content="%s">' % E(desc))
    rep('<meta property="og:title" content="About Me">', '<meta property="og:title" content="%s">' % E(title))
    # the About page's own structured data and styles go; the site's schema stays
    s = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*about\.html#webpage(?:(?!</script>).)*</script>\n?', "", s, count=1, flags=re.S)
    rep("https://paraglidingatlas.com/about.html", "https://paraglidingatlas.com/" + canon, 2)
    rep('<meta property="og:image" content="https://paraglidingatlas.com/assets/images/hero.jpg">', '<meta property="og:image" content="%s">' % og_img)
    s = re.sub(r'<style>\s*\.about-hero.*?</style>\n?', "", s, count=1, flags=re.S)
    s = re.sub(r'<style>/\* five trips.*?</style>\n?', "", s, count=1, flags=re.S)
    # A4: the About page's polish (a count-up on its hero figures, the trips' tilt) is not for these pages
    s, k = re.subn(r'<!--v4p:polish-->.*?<!--/v4p:polish-->\n?', "", s, count=1, flags=re.S)
    assert k == 1, "the About page's polish block has moved"
    ld = {"@context": "https://schema.org", "@type": "WebPage", "@id": "https://paraglidingatlas.com/%s#webpage" % canon,
          "name": title, "url": "https://paraglidingatlas.com/" + canon, "description": desc,
          "isPartOf": {"@id": "https://paraglidingatlas.com/#website"}, "publisher": {"@id": "https://paraglidingatlas.com/#organization"},
          "inLanguage": "en", "dateModified": "2026-11-03"}
    rep("<!-- site-schema -->", '<script type="application/ld+json">%s</script>\n<link rel="stylesheet" href="v4-media.css?v=%s">\n<!-- site-schema -->'
        % (json.dumps(ld, ensure_ascii=False), ver("v4-media.css")))
    rep('<a href="about.html" aria-current="page" class="is-here">About</a>', '<a href="about.html">About</a>')
    if enquire:
        rep('<a href="enquire.html" class="nav-cta" data-hover><span>Enquire Now</span></a>',
            '<a href="%s" class="nav-cta" data-hover><span>Enquire Now</span></a>' % enquire)
    a, b = s.index('<main id="v4-main">'), s.index("</main>")
    s = s[:a] + '<main id="v4-main">\n' + main + "\n" + s[b:]
    if '<a href="media.html">Media</a>' not in s:     # tools/v4_footer.py has it once the site carries it
        rep('<a href="partners.html">Partner With Me</a>', '<a href="partners.html">Partner With Me</a>\n      <a href="media.html">Media</a>')
    rep("</body>", '<script defer src="../../newsletter.js?v=d28c01a5"></script>\n<script defer src="v4-media.js?v=%s"></script>\n</body>' % ver("v4-media.js"))
    return s


# ---------------------------------------------------------------- media.html, part by part ----
def hero():
    up = next_up()
    slate = ("%s, %s &middot; %s" % (E(up["name"]), E(up["place"]), up["dates"])) if up else TBD
    return '''<header class="e-hero" aria-labelledby="e-h1">
    <div class="e-cam" aria-hidden="true">
      <img class="e-cam-img" src="%(s16)s" srcset="%(ss)s" sizes="100vw" width="1600" height="2400" alt="" fetchpriority="high">
      <div class="e-shade"></div>
      <span class="e-cam-foot"></span>
      <span class="e-cam-lab"><span class="e-p-t">Daily Highlights</span><span class="e-p-tags">%(tags)s</span><span class="e-p-go">Watch an example <i aria-hidden="true">&rarr;</i></span></span>
      <i class="e-cam-tally"></i>
    </div>
    <div class="e-hero-in">
      <div class="e-copy">
        <p class="e-slate" data-slate><i class="e-tally" aria-hidden="true"></i><span class="e-slate-k" data-slate-k>Next</span><span data-slate-e>%(slate)s</span><span class="e-slate-n" data-slate-n></span></p>
        <span class="e-kick">Media &middot; For organisers and sponsors</span>
        <h1 id="e-h1">Your Comp, <span class="e-seen">Seen.</span></h1>
        <p class="e-deck">Highlights every task day, live commentary and stills, as joint posts on your channels and ours.</p>
        <div class="e-actions">
          <a class="btn-solid" href="#dates" data-cd data-hover><span>Check dates for your event</span></a>
          <a class="btn-lines" href="%(call)s" target="_blank" rel="noopener" data-hover>Book a Call</a>
        </div>
        <div class="e-for">
          <span class="e-for-k">Covered for</span>
          <span class="e-logo e-logo-srs"><img src="img/media/logo-srs.png" width="340" height="240" alt="SRS, the Sports-Class Racing Series" decoding="async"></span>
          <span class="e-logo e-logo-pwca"><img src="img/media/logo-pwca.png" width="113" height="130" alt="The Paragliding World Cup" decoding="async"></span>
        </div>
      </div>
      <div class="kit-stats e-bug">
        <div class="kit-stat"><b>%(pv)s</b><span class="e-cr"><span>views</span><span class="e-cr-sep">, </span><span class="e-cr-s">PWC Super Final</span></span><em>5 highlight videos, May 2026</em></div>
        <div class="kit-stat"><b>%(rv)s</b><span class="e-cr"><span>views</span><span class="e-cr-sep">, </span><span class="e-cr-s">one task day film</span></span><em>Task 1, an 86.5&nbsp;km sprint</em></div>
        <div class="kit-stat"><b>21<small>&nbsp;h</small> 42<small>&nbsp;min</small></b><span class="e-cr"><span>live</span><span class="e-cr-sep">, </span><span class="e-cr-s">SRS Bassano</span></span><em>5 broadcasts, May 2026</em></div>
      </div>
    </div>
  </header>''' % dict(s16=src(SHOT, 1600), ss=srcset(SHOT), tags=POSTERS[1][4], slate=slate, call=CALL,
                      pv=n(views("pwc")), rv=n(V[REEL][2]))


# key, number, moment, title, what is in it (the owner's pitch and Canva board), link, link attributes, link text,
# the packages it is in (P5, P6)
POSTERS = [
    ("pre-race-show", "01", "Before the race", "Pre-Race Show", "A podcast episode on your venue and its conditions",
     "episodes/pre-pwc-kenya-nikolay-yotov.html", "", "Hear an example", ["full"]),
    ("daily-highlights", "02", "Every task day", "Daily Highlights", "A video each task day, social clips and a results newsletter",
     "#watch", ' data-play="%s"' % REEL, "Watch an example", ["daily", "full"]),
    ("aftermovie", "03", "After the race", "Aftermovie", "Task details, racing strategies, leaderboard standings, fun factor",
     "#pk-full", ' data-pkg="full"', "See the package", ["full"]),
    ("race-behind-the-race", "04", "Mid-season", "Race Behind The Race", "Behind the scenes and athlete showreels",
     "#pk-season", ' data-pkg="season"', "See the package", ["season"]),
]
POSTER_ALT = {"pre-race-show": "The host of the Paragliding Atlas podcast", "aftermovie": "The gaggle, dozens of wings in the blue",
              "race-behind-the-race": "A pilot in harness at launch among the crowd"}
PKG = {"daily": "Daily", "full": "Full Event", "season": "Season", "unsure": "Not sure yet"}
SIZES = "(max-width:700px) 280px, (max-width:900px) 40vw, 24vw"


def poster_img(k):
    if k == "daily-highlights":
        return ('<img class="e-p2-img" src="%s" srcset="%s" sizes="%s" width="1067" height="1600" alt="%s, SRS Piedrahita 2026" decoding="async">'
                % (src(SHOT, 1600), srcset(SHOT, (800, 1600)), SIZES, E(PH[SHOT][3])))
    base = MEDIA + "poster-%s-" % k
    if k == "race-behind-the-race":       # only a 540 px copy exists of this one
        return '<img src="%s600.webp" width="540" height="720" alt="%s" decoding="async">' % (base, E(POSTER_ALT[k]))
    return ('<img src="%s600.webp" srcset="%s600.webp 600w, %s900.webp 900w" sizes="%s" width="600" height="800" alt="%s" decoding="async">'
            % (base, base, base, SIZES, E(POSTER_ALT[k])))


def four():
    items = []
    for k, num, when, t, tags, href, attrs, go, pks in POSTERS:
        cam = k == "daily-highlights"
        ins = " and ".join('<a href="#pk-%s" data-pkg="%s">%s</a>' % (p, p, PKG[p]) for p in pks)
        items.append('<li class="e-pl%s" data-k="%s"><p class="e-when"><i class="e-dot" aria-hidden="true"></i><b>%s</b><span>%s</span></p>'
                     '<a class="e-poster" href="%s"%s>%s<span class="e-p-t">%s</span><span class="e-p-tags">%s</span>'
                     '<span class="e-p-go">%s <i aria-hidden="true">&rarr;</i></span><i class="e-p-tally" aria-hidden="true"></i></a>'
                     '<p class="e-in">In %s</p></li>'
                     % (" is-cam" if cam else "", num, num, when, href, attrs, poster_img(k), t, tags, go, ins))
    return '''<section class="e-four" id="coverage" aria-labelledby="e-four-t">
    <div class="e-four-in">
      <div class="kit-head e-four-head">
        <span class="kit-kicker">What your event gets</span>
        <h2 class="kit-title" id="e-four-t">Four Pieces Of Coverage</h2>
      </div>
      <ol class="e-posters">%s</ol>
      <p class="e-four-note">Everything goes out as joint posts on your channels and on Paragliding Atlas.</p>
    </div>
  </section>''' % "".join(items)


def cover(on, season=False):
    """what a package covers, as a bar (K1)"""
    if season:      # one bar with ticks, no count: the facts do not say how many stops a series has (critic-1-15)
        return ('<div class="e-cov is-season" role="img" aria-label="Covers every stop of the series">'
                '<span class="is-on">Every stop of the series</span></div>')
    parts = [("before", "Before"), ("days", "Task days"), ("after", "After")]
    label = {("days",): "Covers the task days", ("before", "days", "after"): "Covers before the race, the task days and after the race"}[tuple(on)]
    return '<div class="e-cov" role="img" aria-label="%s">%s</div>' % (label, "".join(
        '<span%s>%s</span>' % (' class="is-on"' if p in on else "", w) for p, w in parts))


def packages():
    run = lambda rows: '<ol class="e-run">%s</ol>' % "".join(
        '<li><span>%s</span><b>%s</b>%s</li>' % (a, b, '<em>%s</em>' % c if c else "") for a, b, c in rows)
    foot = lambda key, solid: ('<div class="e-pk-foot"><span class="e-pk-price">Priced per event</span>%s</div>'
                               % (('<a class="btn-solid" href="#dates" data-pkg="%s" data-cd data-hover><span>Check dates</span></a>' if solid
                                   else '<a class="btn-lines" href="#dates" data-pkg="%s" data-cd data-hover>Check dates</a>') % key))
    return '''<section class="kit-band e-pk" id="packages" aria-labelledby="e-pk-t">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">Packages</span>
      <h2 class="kit-title" id="e-pk-t">Pick Your Coverage, Grow It Later</h2>
      <p class="kit-intro">Each package shows what you get. The price is agreed per event, on a call. Start with what your budget allows and add pieces as it grows.</p>
    </div>
    <div class="e-pk-grid">
      <article class="e-pk-card" id="pk-daily" aria-labelledby="pk-daily-t">
        <div class="e-pk-top"><span class="e-pk-n">01</span><h3 id="pk-daily-t">Daily</h3><p>Every task day of one event.</p></div>
        %(c1)s
        %(r1)s
        %(f1)s
      </article>
      <article class="e-pk-card is-pick" id="pk-full" aria-labelledby="pk-full-t">
        <div class="e-pk-top"><span class="e-pk-n">02</span><h3 id="pk-full-t">Full Event</h3><p>Before, during and after your event.</p><span class="e-pick">Most chosen <span class="e-eg">Example</span></span></div>
        %(c2)s
        %(r2)s
        %(f2)s
      </article>
      <article class="e-pk-card" id="pk-season" aria-labelledby="pk-season-t">
        <div class="e-pk-top"><span class="e-pk-n">03</span><h3 id="pk-season-t">Season</h3><p>Every event of your series.</p></div>
        %(c3)s
        %(r3)s
        %(f3)s
      </article>
    </div>
    <p class="e-addons"><b>Also offered</b><span>Live commentary, as at SRS Bassano: 5 broadcasts, 21&nbsp;h&nbsp;42&nbsp;min on air</span><span>Stills, as at SRS Piedrahita</span></p>
    <div class="e-spons" aria-labelledby="e-spons-t">
      <h3 id="e-spons-t">Where your sponsors appear</h3>
      <ul>
        <li><b>In the joint posts</b><span>On your channels and on Paragliding Atlas</span></li>
        <li><b>In the films, the live commentary and the results newsletter</b><span>Banners, footnotes and premium spaces, depending on the collaboration</span></li>
      </ul>
    </div>
  </div>
</section>''' % dict(
        c1=cover(["days"]), c2=cover(["before", "days", "after"]), c3=cover([], season=True),
        r1=run([("Task days", "Daily Highlights", "A long-form video each task day"),
                ("Task days", "Social clips", "9:16, %s per task day" % TBD),
                ("Task days", "Results newsletter", "The results, by email")]),
        r2=run([("Before", "Pre-Race Show", "A podcast episode on your venue and its conditions"),
                ("Task days", "Daily Highlights", "With social clips and a results newsletter"),
                ("After", "Aftermovie", "The event in one highlights film")]),
        r3=run([("Each event", "Coverage at every stop", "The pieces you pick, at each event of the series"),
                ("Mid-season", "Race Behind The Race", "Behind the scenes and athlete showreels")]),
        f1=foot("daily", False), f2=foot("full", True), f3=foot("season", False), tbd=TBD)


def reach():
    top = max(views(e["comp"]) for e in SEASON)
    marks, rows = [], []
    for i, ev in enumerate(SEASON, 1):
        a, b = span(ev)
        marks.append('<span class="e-tl-k" data-i="%d" style="--x:%.4f;--w:%.4f"></span>' % (i, at(a), (b - a).days / (LINE[1] - LINE[0]).days))
        v = views(ev["comp"])
        rows.append('<li class="e-row" data-i="%d" style="--v:%.4f"><span class="e-row-d">%s</span>'
                    '<span class="e-row-n"><b>%s</b><small><span>%s</span><span class="e-row-sep"> &middot; </span><span class="e-row-w">%s</span></small></span><span class="e-row-m">%s</span>'
                    '<span class="e-row-bar" aria-hidden="true"><i></i></span><span class="e-row-v">%s<small> views</small></span>'
                    '<a class="e-watch" href="#watch" data-comp="%s" aria-label="Watch the %s videos">Watch <i aria-hidden="true">&rarr;</i></a></li>'
                    % (i, v / top, ev["when"], ev["name"], ev["edition"], ev["where"], ev["made"], n(v), ev["comp"], ev["name"]))
    up = next_up()
    if up:
        a, b = day(up["first"]), day(up["last"])
        marks.append('<span class="e-tl-k is-next" data-i="%d" style="--x:%.4f;--w:%.4f"></span>' % (len(SEASON) + 1, at(a), (b - a).days / (LINE[1] - LINE[0]).days))
        rows.append('<li class="e-row is-next" data-i="%d" data-up-row><span class="e-row-d"><i class="e-tally" aria-hidden="true"></i><b data-up-k>Next</b> %s</span>'
                    '<span class="e-row-n"><b>%s</b><small><span>%s</span><span class="e-row-sep"> &middot; </span><span class="e-row-w">%s</span></small></span><span class="e-row-m">%s</span>'
                    '<span class="e-row-bar" aria-hidden="true"></span><span class="e-row-v"></span>'
                    '<a class="e-watch" href="#dates" data-cd>Your comp next? Check dates <i aria-hidden="true">&rarr;</i></a></li>'
                    % (len(SEASON) + 1, up["short"], E(up["name"]), E(up["edition"]), E(up["where"]), E(up["facts"])))
    months = "".join('<span class="e-tl-m" style="--x:%.4f">%s</span>' % (at(datetime.date(2026, m, 1)), datetime.date(2026, m, 1).strftime("%b"))
                     for m in range(5, 12))
    c, t, k, ln, d, ep = V[REEL]
    return '''<section class="e-reach" id="reach" aria-labelledby="e-reach-t">
  <div class="e-reach-band">
    <img src="%(b16)s" srcset="%(bss)s" sizes="100vw" width="1600" height="1067" alt="%(balt)s" loading="lazy" decoding="async">
    <div class="e-reach-in">
      <div class="kit-head">
        <span class="kit-kicker">Reach</span>
        <h2 class="kit-title" id="e-reach-t">Your Audience, Not Just Your Video</h2>
        <p class="kit-intro">Every piece goes out as one joint post on your channels and on Paragliding Atlas. One post, two audiences.</p>
      </div>
      <div class="e-total">
        <p class="e-total-n"><b>%(total)s</b><span>views on 13 comp videos in 2026</span><small>Counted on YouTube, %(counted)s</small></p>
        <p class="e-most"><b>Most watched</b> Task 1 Highlights, PWC&nbsp;Super&nbsp;Final, %(rv)s&nbsp;views for %(ln)s of an 86.5&nbsp;km sprint</p>
      </div>
    </div>
  </div>
  <div class="kit-band e-reach-b">
    <div class="kit-in">
      <div class="e-two">
        <p class="e-two-h">One joint post, <span>two audiences</span></p>
        <div class="e-two-l">
          <div class="e-aud"><b>Your channels</b><span>Your event&rsquo;s own followers</span></div>
          <span class="e-plus" aria-hidden="true">+</span>
          <div class="e-aud"><b>Paragliding Atlas</b>
            <dl class="e-base"><div><dt>YouTube subscribers</dt><dd>2,160 <small>(4 Nov 2026)</small></dd></div><div><dt>YouTube views</dt><dd>294,561 <small>all videos</small></dd></div></dl>
          </div>
        </div>
        <p class="e-pod">The podcast: about 80 episodes, listened to in 136 countries.</p>
      </div>
      <figure class="e-season" aria-labelledby="e-season-t">
        <figcaption class="e-season-h"><b id="e-season-t">The 2026 season</b><span>Views on YouTube, %(counted)s</span></figcaption>
        <div class="e-tl" aria-hidden="true" data-from="%(l0)s" data-to="%(l1)s">%(months)s%(marks)s<span class="e-tl-today" data-today hidden><i>Today</i></span></div>
        <ol class="e-rows">%(rows)s</ol>
        <p class="e-season-f"><span>13 videos</span><span>%(total)s views in all</span></p>
      </figure>
    </div>
  </div>
</section>''' % dict(b16=src(BAND, 1600), bss=srcset(BAND), balt="%s, SRS Piedrahita 2026" % E(PH[BAND][3]), total=n(TOTAL),
                     counted=COUNTED, rv=n(k), ln=ln, tbd=TBD, months=months, marks="".join(marks), rows="".join(rows),
                     l0=LINE[0].isoformat(), l1=LINE[1].isoformat())


def proof():
    items = []
    for v, (c, t, k, ln, d, ep) in V.items():
        items.append('<li data-comp="%s"><button type="button" data-vid="%s" data-date="%s" data-title="%s" data-comp-name="%s" data-views="%s views" data-len="%s" data-still="%s"%s%s>'
                     '<img src="%s" alt="" width="320" height="180" loading="lazy"><span class="md-li"><b><i class="md-tally" aria-hidden="true"></i>%s</b><small><span>%s</span><span>%s</span></small></span></button></li>'
                     % (c, v, d, E(t), E(COMPS[c]), n(k), ln, thumb(v), ' data-ep="episodes/%s.html"' % ep if ep else "",
                        ' aria-current="true"' if v == REEL else "", thumb(v, "mqdefault"), E(t), E(COMPS[c]), vmeta(v)))
    chips = ('<div class="v2-chips" role="group" aria-label="Show the videos from">'
             '<button class="v2-chip" type="button" aria-pressed="true" data-comp="">All <i>13</i></button>'
             '<button class="v2-chip" type="button" aria-pressed="false" data-comp="pwc">Pegalajar <i>5</i></button>'
             '<button class="v2-chip" type="button" aria-pressed="false" data-comp="srs5">Piedrahita <i>3</i></button>'
             '<button class="v2-chip" type="button" aria-pressed="false" data-comp="srs4">Bassano live <i>5</i></button></div>')
    c, t, k, ln, d, ep = V[REEL]
    reel = ('<div class="md-reel"><div class="md-main">%s<div class="md-now">%s%s</div></div>'
            '<div class="md-side"><div class="md-side-in">%s<ul class="md-list">%s</ul></div></div></div>'
            % (frame(REEL), now_title(REEL), now_line(REEL), chips, "".join(items)))
    return '''<section class="e-qband" aria-label="A word from an organiser">
  <div class="e-qband-media" aria-hidden="true"><img src="%(q16)s" srcset="%(qss)s" sizes="100vw" width="1600" height="1067" alt="" loading="lazy" decoding="async"></div>
  <figure class="e-quote">
    <span class="e-eg">Example</span>
    <blockquote><p>&ldquo;Every task day our pilots and sponsors had the race in their feeds the same evening. The week felt bigger than the field.&rdquo;</p></blockquote>
    <figcaption>%(tbd)s <span>Organiser, event</span></figcaption>
  </figure>
</section>

<section class="kit-band e-proof" id="proof" aria-labelledby="e-watch-t">
  <div class="kit-in">
    <div class="kit-head e-watch-head" id="watch">
      <span class="kit-kicker">The work</span>
      <h2 class="kit-title" id="e-watch-t">Watch The Coverage</h2>
      <p class="kit-intro">The 13 comp videos of 2026, by comp and the most watched first: Task 1 of the Super&nbsp;Final, %(rv)s&nbsp;views. Every one plays here.</p>
    </div>
    %(reel)s
    <div class="e-stills-head">
      <h3>Stills from SRS Piedrahita 2026</h3>
      <p>Every frame shown whole. Open one to see it full size and zoom in.</p>
    </div>
    %(grid)s
    <div class="e-more"><a class="btn-lines" href="media-srs-piedrahita-2026.html" data-hover>All 20 from Piedrahita, by task</a></div>
  </div>
</section>''' % dict(q16=src(QUOTE, 1600), qss=srcset(QUOTE), tbd=TBD, rv=n(V[REEL][2]), reel=reel,
                     grid=grid(STILLS, "Stills from SRS Piedrahita 2026"))


def delivery():
    fr = lambda cls, stem, b, s: ('<li class="e-fr %s"><span class="e-fr-box"><img src="%s" width="%d" height="%d" alt="" loading="lazy" decoding="async"></span>'
                                  '<span class="e-fr-t"><b>%s</b><small>%s</small></span></li>'
                                  % (cls, src(stem, 800), wide(stem, 800), round(wide(stem, 800) * PH[stem][1] / PH[stem][0]), b, s))
    return '''<section class="kit-band e-del" id="delivery" aria-labelledby="e-del-t">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">Delivery</span>
      <h2 class="kit-title" id="e-del-t">What You Get, What We Need</h2>
    </div>
    <div class="e-del-grid">
      <div class="e-get">
        <h3>What you get</h3>
        <ul class="e-frames">%s%s%s</ul>
      </div>
      <div class="e-need">
        <h3>What we need from you</h3>
        <ol class="e-needs">
          <li><b>Internet on site</b><span>For same-day delivery</span></li>
          <li><b>Access to footage</b><span>The daily timing depends on it too</span></li>
          <li><b>%s</b><span>Anything else an event provides</span></li>
        </ol>
      </div>
    </div>
    <p class="e-rider"><b>Delivery</b><span>The same day or at the end of the week, as you need, subject to the internet on site, the task finish time and access to footage.</span></p>
  </div>
</section>''' % (fr("is-169", "SRS_5_T3_57", "16:9", "Videos"), fr("is-916", "SRS_5_T2_76", "9:16", "Social clips"),
                 fr("is-still", "SRS_5_T3_121", "Stills", "Web and full size"), TBD)


FAQ = [
    ("What does it cost?", "Every package is priced per event. We agree the price with you on a call, once we know your event, its dates and what you would like from it."),
    ("Can we start small?", "Yes. Start with the resources you have and grow the coverage as your budget allows."),
    ("When does it come out?", "The same day or at the end of the week, as you need. Same-day delivery depends on the internet on site, when the task finishes and access to footage."),
    ("Where is it published?", "As joint posts on your channels and on Paragliding Atlas, so both audiences see it."),
    ("Can you cover a whole season?", "Yes. The Season package covers every event of your series, with Race Behind The Race mid-season."),
    ("How does travel work?", TBD),
    ("Who can use the videos and photos?", TBD),
    ("How far ahead should we book?", TBD),
]

# the 2027 season, EXAMPLE data until the owner sends the real calendar (S1): open, held or booked
MONTHS = [("Jan", "open"), ("Feb", "open"), ("Mar", "held"), ("Apr", "open"), ("May", "booked"), ("Jun", "open"),
          ("Jul", "held"), ("Aug", "booked"), ("Sep", "open"), ("Oct", "open"), ("Nov", "held"), ("Dec", "open")]


def faq():
    return '''<section class="kit-band e-faq" id="faq" aria-labelledby="e-faq-t">
  <div class="kit-in e-faq-in">
    <div class="kit-head">
      <span class="kit-kicker">Questions</span>
      <h2 class="kit-title" id="e-faq-t">What Organisers Ask First</h2>
      <p class="e-faq-more">Another question? <a href="%s" target="_blank" rel="noopener">Book a Call</a> or <a href="%s" target="_blank" rel="noopener">send a WhatsApp</a>.</p>
    </div>
    <div class="e-qs">%s</div>
  </div>
</section>''' % (CALL, WA, "".join("<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in FAQ))


def dates():
    cells = []
    for m, st in MONTHS:
        word = {"open": "Open", "held": "Held", "booked": "Booked"}[st]
        if st == "open":
            cells.append('<li class="is-open"><button type="button" data-when="%s 2027" aria-label="%s 2027, open: put it in the dates"><b>%s</b><span>%s</span></button></li>' % (m, m, m, word))
        else:
            cells.append('<li class="is-%s"><span class="e-mo"><b>%s</b><span>%s</span></span></li>' % (st, m, word))
    opts = "".join('<option value="%s">%s</option>' % (k, PKG[k]) for k in ("unsure", "daily", "full", "season"))
    # the order is the phone's: the heading, the form at once (a Check dates lands where you type, buyer-1-4), the
    # talk-first line under the form, then the example season; on a wide screen the form stands on the right
    return '''<section class="cta-band e-dates" id="dates" aria-labelledby="e-dates-t">
  <div class="cta-card e-dates-card">
    <div class="kit-head e-dates-head">
      <span class="kit-kicker">Coverage for your comp</span>
      <h2 class="kit-title" id="e-dates-t">Check Dates For Your Event</h2>
      <p class="kit-intro">Send the event, its dates and its place, and we will reply about availability.</p>
    </div>
    <form class="e-form" id="e-form" action="enquire.html" method="get" aria-labelledby="e-dates-t" data-md-form>
      <input type="hidden" name="trip" value="media">
      <div class="e-f-row">
        <div class="e-field"><label for="e-event">Event</label><input id="e-event" name="event" type="text" placeholder="Its name" autocomplete="off" required></div>
        <div class="e-field"><label for="e-when">Dates <span class="e-opt">(optional)</span></label><input id="e-when" name="when" type="text" placeholder="Task days, or a rough window" autocomplete="off"></div>
      </div>
      <div class="e-f-row">
        <div class="e-field"><label for="e-place">Place <span class="e-opt">(optional)</span></label><input id="e-place" name="place" type="text" placeholder="Site and country" autocomplete="off"></div>
        <div class="e-field e-sel"><label for="e-pkg">Package</label><select id="e-pkg" name="package">%(opts)s</select></div>
      </div>
      <div class="e-f-row">
        <div class="e-field"><label for="e-name">Your name</label><input id="e-name" type="text" placeholder="Full name" autocomplete="name" required></div>
        <div class="e-field"><label for="e-email">Email</label><input id="e-email" type="email" placeholder="you@example.com" autocomplete="email" required></div>
      </div>
      <div class="e-f-go">
        <button type="submit" class="btn-solid" data-cd data-hover><span>Check dates</span></button>
        <p><b>Step 1 of 2.</b> Next you check the details and send them. Used only to answer you: see the <a href="privacy-policy.html">Privacy Policy</a>.</p>
      </div>
    </form>
    <div class="e-or">
      <span>Or talk first</span>
      <a class="btn-lines" href="%(call)s" target="_blank" rel="noopener" data-hover>Book a Call</a>
      <a class="btn-lines" href="%(wa)s" target="_blank" rel="noopener" data-hover>WhatsApp</a>
    </div>
    <div class="e-cal" aria-labelledby="e-cal-t">
      <p class="e-cal-h"><b id="e-cal-t">The 2027 season</b><span class="e-eg">Example</span></p>
      <ol class="e-months">%(cells)s</ol>
      <p class="e-cal-note">Example data, to show how it will read. The real 2027 calendar: %(tbd)s</p>
    </div>
  </div>
</section>''' % dict(cells="".join(cells), tbd=TBD, call=CALL, wa=WA, opts=opts)


def media_page():
    main = '''
<!-- Designer E (Cloudbase), "Pull Back To The Coverage": the first screen is one shot of a race, the way an audience
     sees it; scrolling pulls the camera back until that shot is the second of four pieces of coverage. Reduced motion
     and no JavaScript show the finished page: the opening, then the four. -->
<script type="application/json" id="md-up">%(up)s</script>
<div class="e-pull" id="top">
 <div class="e-stage">
  %(hero)s
  %(four)s
 </div>
</div>

%(packages)s

%(reach)s

%(proof)s

%(delivery)s

%(faq)s

%(dates)s

<section class="e-nl" id="newsletter" aria-label="Newsletter">
  <div class="v2-nl e-nl-in" data-nl>
    <p class="e-nl-t"><b>Not organising?</b> Follow the races in the newsletter.</p>
    <label class="e-sr" for="newsletterEmail">Email Address</label>
    <div class="v2-nl-row">
      <input id="newsletterEmail" type="email" placeholder="you@example.com" autocomplete="email">
      <button class="btn-lines" type="button" data-hover>Sign Up</button>
    </div>
    <p class="nl-status" data-nl-status role="status" aria-live="polite"></p>
  </div>
</section>

<div class="e-bar" id="eBar">
  <span class="e-bar-l"><b>Your comp, seen.</b><small>Priced per event</small></span>
  <a class="btn-solid" href="#dates" data-hover><span>Check dates</span></a>
</div>

%(viewer)s
''' % dict(up=json.dumps(UPCOMING, separators=(",", ":")), hero=hero(), four=four(), packages=packages(), reach=reach(),
           proof=proof(), delivery=delivery(), faq=faq(), dates=dates(), viewer=VIEWER)
    return shell("Media", "Comp coverage by Paragliding Atlas for organisers and sponsors: daily highlight videos, live commentary and stills, published as joint posts on your channels and ours.",
                 "media.html", src(SHOT, 1600), "Media", main, enquire="#dates")


# ---------------------------------------------------------------- the Piedrahita page (A5: as it was) ----
def cta(title, tag, body):
    return ('<section class="cta-band" id="book">\n  <div class="cta-card">\n  <span class="cta-hud-tag">%s</span>\n  <h2>%s</h2>\n'
            '  <div class="cta-buttons">\n    <a href="%s" target="_blank" rel="noopener" class="btn-solid" data-hover><span>Book a Call</span></a>\n'
            '    <a href="%s" target="_blank" rel="noopener" class="listen-btn" data-hover><span>%s WhatsApp</span></a>\n'
            '    <a href="enquire.html?trip=media" class="btn-lines" data-hover>Send a Media Enquiry</a>\n  </div>\n'
            '  <p class="cta-body">%s</p>\n  </div>\n</section>\n' % (tag, title, CALL, WA, ICON_WA, body))


def piedrahita_page():
    days = [("Day 1", "Registration, the pilots and the Peñas de Piedrahíta fiesta", "cuGs7Lk6Dt4", 0),
            ("Task 1", "59 km, humid air, a 2,100 m ceiling and a long leg into a westerly wind", "uCEfssE40u8", 1),
            ("Task 2", "75 km, and a flatland gamble that cut the course short", "NXUEyPQ3V4E", 2),
            ("Task 3", "The race from the air", None, 3)]
    out = []
    for k, (lab, line, v, t) in enumerate(days):
        # the opening's two shots (wide and phone) are not shown again in the grids (no photo twice, owner 21 Oct)
        stems = [s for s in PH if PH[s][2] == t and s not in ("SRS_5_T3_63", "SRS_5_T2_133-2")] if t else []
        vid = ""
        if v:
            vid = '%s<div class="md-now"><h3>%s</h3>%s</div>' % (frame(v), E("Piedrahita, " + V[v][1]), now_line(v))
        out.append('<section class="kit-band md-day%s" id="%s"><div class="kit-in"><div class="kit-head"><span class="kit-kicker">%s</span>'
                   '<h2 class="kit-title">%s</h2></div>%s%s</div></section>'
                   % (" v2-topo" if k % 2 else "", lab.lower().replace(" ", "-"), lab, E(line), vid,
                      grid(stems, "Stills from %s" % lab) if stems else ""))
    w, h = PH["SRS_5_T3_63"][:2]
    main = '''
<header class="kit-hero md-hero">
  <div class="kit-hero-media">
    <picture><source media="(max-aspect-ratio: 2/3)" srcset="%(hp)s"><img src="%(h)s" srcset="%(hs)s" sizes="100vw" width="1600" height="%(hh)d" alt="%(alt)s" fetchpriority="high"></picture>
  </div>
  <div class="kit-hero-copy">
    <a class="md-back" href="media.html">&larr; Media</a>
    <span class="kit-kicker">SRS BGD Edition &middot; Piedrahita, Ávila, Spain</span>
    <h1>Piedrahita 2026</h1>
    <p class="kit-intro">22 to 29 Aug 2026, FAI Category 2: 120 pilots from 54 countries. Stills from all three tasks, and highlight videos of Day 1, Task 1 and Task 2.</p>
    <div class="kit-stats">
      <div class="kit-stat"><b>20</b><span>Chosen stills</span></div>
      <div class="kit-stat"><b>3</b><span>Highlight videos</span></div>
      <div class="kit-stat"><b>5,479</b><span>Views</span></div>
    </div>
  </div>
</header>
%(days)s
%(cta)s
%(viewer)s
''' % dict(hp=src("SRS_5_T2_133-2", 1600), h=src("SRS_5_T3_63", 1600), hs=srcset("SRS_5_T3_63"),
           hh=round(1600 * h / w), alt=E(PH["SRS_5_T3_63"][3]), days="\n".join(out),
           cta=cta("Coverage Like This For <span class=\"v4-nw\">Your Event</span>", "Coverage For Your Comp",
                   "A free 30-minute call: tell me the event, the dates and the place, and what you would like to come out of it."),
           viewer=VIEWER)
    return shell("Piedrahita 2026", "SRS BGD Edition, Piedrahita, Spain, 22 to 29 Aug 2026: the stills and highlight videos by Paragliding Atlas.",
                 "media-srs-piedrahita-2026.html", src("SRS_5_T3_63", 1600), "Piedrahita 2026", main)


def check(name, page):
    body = page.split('<main id="v4-main">')[1].split("</main>")[0]
    assert "—" not in body and "&mdash;" not in body, "an em dash in " + name
    for m in re.finditer(r"\[to supply\]", body):          # every missing fact is marked as one
        assert body[max(0, m.start() - 22):m.start()].endswith('<i class="v2-tbd">'), ("an unmarked [to supply] in " + name, body[m.start() - 80:m.end()])


if __name__ == "__main__":
    for name, page in (("media.html", media_page()), ("media-srs-piedrahita-2026.html", piedrahita_page())):
        check(name, page)
        open(os.path.join(V4, name), "w").write(page)
        print("wrote prototypes/v4/" + name, len(page))
