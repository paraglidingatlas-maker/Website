#!/usr/bin/env python3
"""Designer D (Trim), event landing pages, contest round 1: builds samples/event-d/index.html (SRS Piedrahita)
and pwc.html (PWC Super Final) from one template. Facts only from tools/v4_media.py, tools/v4_comp_gallery.py,
photos.json on the media host and the owner's YouTube (frames i.ytimg.com/vi/ID/maxresN.jpg are frames of the
owner's own films)."""
import json, re, html, os, urllib.request

REPO = "/home/user/website"
V4 = REPO + "/prototypes/v4"
OUT = V4 + "/samples/event-d"
SCR = os.path.dirname(os.path.abspath(__file__))
E = lambda s: html.escape(s, quote=True)
MEDIA = "https://paraglidingatlas-maker.github.io/media-2026/"

# the films (tools/v4_media.py V): id: (title, views, length, published)
V = {
    "BRAX1XMU390": ("Task 1 Highlights", 7342, "6:53", "14 May 2026"),
    "7il6yV1vdIc": ("Task 2 Highlights", 4034, "8:17", "16 May 2026"),
    "FOuAWMeoxs4": ("Day 1 Highlights", 3537, "6:44", "13 May 2026"),
    "op1-O01xkH4": ("Task 4 Highlights", 3437, "7:47", "18 May 2026"),
    "vPnIYYKcvEg": ("Task 5 Highlights", 3340, "8:08", "20 May 2026"),
    "NXUEyPQ3V4E": ("Task 2 Highlights", 2303, "13:46", "6 Sep 2026"),
    "uCEfssE40u8": ("Task 1 Highlights", 1970, "7:38", "27 Aug 2026"),
    "cuGs7Lk6Dt4": ("Day 1: Registration and the Peñas", 1206, "9:04", "23 Aug 2026"),
}
COUNTED = "3 Nov 2026"


def secs(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


def runtime(ids):
    t = sum(secs(V[i][2]) for i in ids)
    return "%d min %02d s" % (t // 60, t % 60)


def yt_frame(vid, k):
    return "https://i.ytimg.com/vi/%s/maxres%d.jpg" % (vid, k)


# the 2026 season (tools/v4_media.py SEASON + UPCOMING), in date order
SEASON = [
    dict(key="pwc", name="PWC Super Final", edition="15th Paragliding World Cup Super Final", where="Pegalajar, Spain",
         when="May 2026", made="5 highlight films", page="pwc.html"),
    dict(key="srs4", name="SRS Bassano", edition="SRS Skywalk Bassano Edition", where="Monte Grappa, Italy",
         when="May 2026", made="Live commentary: 5 broadcasts, 21 h 42 min on air", page="../../media.html#proof"),
    dict(key="srs5", name="SRS Piedrahita", edition="SRS BGD Edition", where="Piedrahita, Ávila, Spain",
         when="22 to 29 Aug 2026", made="325 photos and 3 films", page="index.html"),
    dict(key="tapalpa", name="SRS Tapalpa", edition="SRS Advance Edition", where="Tapalpa, Mexico",
         when="8 to 14 Nov 2026", made="Photos and films each task day", page="../../media-srs-tapalpa-2026.html"),
]

photos = json.load(open(SCR + "/ph/photos.json"))
colors = json.load(open(SCR + "/colors.json"))

# ---- the events: the only part the chat fills in per event ----
PIED = dict(
    key="srs5", file="index.html", title="Piedrahita 2026", loader="Piedrahita 2026",
    kicker="SRS BGD Edition &middot; Piedrahita, &Aacute;vila, Spain",
    h1="Piedrahita <span>2026</span>",
    facts=["22 to 29 Aug 2026", "FAI Category 2", "120 pilots, 54 countries"],
    made="325 photos by Aninder Singh &middot; 3 films, %s &middot; %s views on YouTube by %s"
         % (runtime(["cuGs7Lk6Dt4", "uCEfssE40u8", "NXUEyPQ3V4E"]), "{:,}".format(1206 + 1970 + 2303), COUNTED),
    official=("SRS BGD Edition, Piedrahita", "https://airtribune.com/srs-2026-5/info"),
    desc="SRS BGD Edition, Piedrahita, Spain, 22 to 29 Aug 2026: the three task days, all 325 photos, free to save, and the films.",
    folder="srs-piedrahita",
    chapters=[
        dict(id="day-1", word="Day", num="1", name="Day 1", films=["cuGs7Lk6Dt4"], day=None,
             story="Registration and the Pe\u00f1as, the day before the first task.",
             posters={"cuGs7Lk6Dt4": (yt_frame("cuGs7Lk6Dt4", 1), "60% 50%")}),
        dict(id="task-1", word="Task", num="1", name="Task 1", films=["uCEfssE40u8"], day="T1",
             story="59 km, humid air, a 2,100 m ceiling and a long leg into a westerly wind.",
             frame=dict(stem="SRS_5_T1_10", pos="78% 30%", alt="An orange wing under grey cloud over the plain, Task 1"),
             posters={"uCEfssE40u8": ("SRS_5_T1_39", "50% 45%")}),
        dict(id="task-2", word="Task", num="2", name="Task 2", films=["NXUEyPQ3V4E"], day="T2",
             story="75 km, and a flatland gamble that cut the course short.",
             frame=dict(stem="SRS_5_T2_55", pos="52% 40%", alt="A wing in every colour against a deep blue sky, Task 2"),
             posters={"NXUEyPQ3V4E": ("SRS_5_T2_65", "50% 40%")}),
        dict(id="task-3", word="Task", num="3", name="Task 3", films=[], day="T3",
             story="The race from the air.",
             frame=dict(stem="SRS_5_T3_63", pos="50% 50%", alt="The gaggle, dozens of wings in the blue, Task 3")),
    ],
)

PWC = dict(
    key="pwc", file="pwc.html", title="PWC Super Final 2026", loader="PWC Super Final 2026",
    kicker="15th Paragliding World Cup Super Final &middot; Pegalajar, Spain",
    h1="Pegalajar <span>2026</span>",
    facts=["May 2026", "Pilots <i class=\"v2-tbd\">[to supply]</i>", "Tasks flown <i class=\"v2-tbd\">[to supply]</i>"],
    made="5 films by Aninder Singh, %s &middot; %s views on YouTube by %s"
         % (runtime(["FOuAWMeoxs4", "BRAX1XMU390", "7il6yV1vdIc", "op1-O01xkH4", "vPnIYYKcvEg"]), "{:,}".format(21690), COUNTED),
    official=None,
    desc="15th Paragliding World Cup Super Final, Pegalajar, Spain, May 2026: the five highlight films, day by day.",
    folder=None,
    chapters=[
        dict(id="day-1", word="Day", num="1", name="Day 1", films=["FOuAWMeoxs4"], day=None, story=None,
             frame=dict(src=yt_frame("FOuAWMeoxs4", 3), pos="40% 40%", alt="Pilots walk with their flags through Pegalajar, a frame from the Day 1 film"),
             posters={"FOuAWMeoxs4": (yt_frame("FOuAWMeoxs4", 3), "50% 40%")}, strip={"FOuAWMeoxs4": [1, 2]}),
        dict(id="task-1", word="Task", num="1", name="Task 1", films=["BRAX1XMU390"], day=None, story=None,
             frame=dict(src=yt_frame("BRAX1XMU390", 1), pos="45% 40%", alt="A pilot in his harness on launch, a frame from the Task 1 film"),
             posters={"BRAX1XMU390": (yt_frame("BRAX1XMU390", 1), "50% 40%")}, strip={"BRAX1XMU390": [2, 3]}),
        dict(id="task-2", word="Task", num="2", name="Task 2", films=["7il6yV1vdIc"], day=None, story=None,
             frame=dict(src=yt_frame("7il6yV1vdIc", 2), pos="50% 30%", alt="A pilot in an orange shirt in Pegalajar, a frame from the Task 2 film"),
             posters={"7il6yV1vdIc": (yt_frame("7il6yV1vdIc", 2), "50% 30%")}, strip={"7il6yV1vdIc": [1, 3]}),
        dict(id="task-3", word="Task", num="3", name="Task 3", films=[], day=None, story=None, tbd=True),
        dict(id="task-4", word="Task", num="4", name="Task 4", films=["op1-O01xkH4"], day=None, story=None,
             frame=dict(src=yt_frame("op1-O01xkH4", 3), pos="30% 40%", alt="A pilot holds up a small camera on launch, a frame from the Task 4 film"),
             posters={"op1-O01xkH4": (yt_frame("op1-O01xkH4", 3), "40% 40%")}, strip={"op1-O01xkH4": [1, 2]}),
        dict(id="task-5", word="Task", num="5", name="Task 5", films=["vPnIYYKcvEg"], day=None, story=None,
             frame=dict(src=yt_frame("vPnIYYKcvEg", 3), pos="40% 40%", alt="A pilot on the landing field, wings in the sky, a frame from the Task 5 film"),
             posters={"vPnIYYKcvEg": (yt_frame("vPnIYYKcvEg", 3), "50% 40%")}, strip={"vPnIYYKcvEg": [2]}),
    ],
)


def ph(folder, stem, w):
    return "%s%s/%s-%d.webp" % (MEDIA, folder, stem, w)


def pic(ev, src_or_stem, pos, alt, sizes="100vw", cls="", eager=False, prio=False):
    """a photo from the media host (srcset 800/1600/2400) or a film frame (one 1280 jpg)"""
    lz = "" if eager else ' loading="lazy"'
    fp = ' fetchpriority="high"' if prio else ""
    if src_or_stem.startswith("http"):
        return ('<img%s src="%s" width="1280" height="720" alt="%s" style="object-position:%s" decoding="async"%s%s>'
                % (cls, src_or_stem, E(alt), pos, lz, fp))
    f = ev["folder"]
    p = next(x for x in photos if x["stem"] == src_or_stem)
    return ('<img%s src="%s" srcset="%s 800w, %s 1600w, %s 2400w" sizes="%s" width="%d" height="%d" alt="%s" '
            'style="object-position:%s" decoding="async"%s%s>'
            % (cls, ph(f, src_or_stem, 1600), ph(f, src_or_stem, 800), ph(f, src_or_stem, 1600), ph(f, src_or_stem, 2400),
               sizes, p["w"], p["h"], E(alt), pos, lz, fp))


PLAY = ('<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 1.2v7.6c0 .5.5.8.9.5l5.9-3.8c.4-.2.4-.8 0-1L2.9.7C2.5.4 '
        '2 .7 2 1.2z"/></svg>')


def cover(ev):
    chs = [c for c in ev["chapters"] if c.get("frame")]
    last = len(chs) - 1
    frames = []
    for i, c in enumerate(chs):
        f = c["frame"]
        frames.append('<div class="ev-f" data-i="%d"%s>%s</div>' % (
            i, ' data-rest' if i == last else "",
            pic(ev, f.get("src") or f["stem"], f["pos"], f["alt"], eager=(i in (0, last)), prio=(i == last))))
    off = ('<p class="ev-off">Official event: <a href="%s" target="_blank" rel="noopener">%s</a></p>' % (ev["official"][1], E(ev["official"][0]))
           if ev["official"] else '<p class="ev-off">Official event: <i class="v2-tbd">[to supply]</i></p>')
    return ('<header class="ev-cover" aria-labelledby="ev-h1">\n'
            '  <div class="ev-frames" aria-hidden="false">%s</div>\n'
            '  <div class="ev-title">\n'
            '    <p class="ev-kick">%s</p>\n'
            '    <h1 id="ev-h1" class="ev-h1">%s</h1>\n'
            '    <p class="ev-facts">%s</p>\n'
            '    <p class="ev-made">%s</p>\n'
            '    %s\n'
            '  </div>\n'
            '</header>\n' % ("".join(frames), ev["kicker"], ev["h1"], "".join("<span>%s</span>" % x for x in ev["facts"]), ev["made"], off))


def slate(ev):
    chs = ev["chapters"]
    fi = 0
    items = []
    for c in chs:
        if c.get("tbd"):
            items.append('<li class="ev-s is-tbd"><a href="#%s"><small>%s</small><b>%s</b><i class="ev-s-l" aria-hidden="true"><i></i></i>'
                         '<span class="ev-s-n">to supply</span></a></li>' % (c["id"], c["word"], c["num"]))
            continue
        n = []
        if c["day"]:
            n.append("%d photos" % sum(1 for p in photos if p["day"] == c["day"]))
        if c["films"]:
            n.append("film")
        items.append('<li class="ev-s"%s><a href="#%s" aria-label="%s, %s"><small aria-hidden="true">%s</small><b aria-hidden="true">%s</b>'
                     '<i class="ev-s-l" aria-hidden="true"><i></i></i><span class="ev-s-n" aria-hidden="true">%s</span></a></li>'
                     % (' data-f="%d"' % fi if c.get("frame") else "", c["id"], c["name"], ", ".join(n), c["word"], c["num"], " &middot; ".join(n)))
        fi += 1 if c.get("frame") else 0
    return ('<nav class="ev-slate" aria-label="%s, day by day">\n'
            '  <div class="ev-slate-in">\n'
            '    <a class="ev-season-k" href="#season" aria-label="The 2026 season: the events before and after"><i aria-hidden="true">&larr;</i><span>2026</span></a>\n'
            '    <ol class="ev-ss">%s</ol>\n'
            '    <button class="ev-pp" type="button" aria-label="Pause the cut" hidden><svg viewBox="0 0 10 10" aria-hidden="true"><path class="ev-pp-p" d="M3 1.5v7M7 1.5v7"/><path class="ev-pp-g" d="M2.6 1.4v7.2L8.6 5z"/></svg></button>\n'
            '  </div>\n'
            '</nav>\n' % (E(ev["title"]), "".join(items)))


def film(ev, c, vid):
    t, views, ln, pub = V[vid]
    src, pos = c["posters"][vid]
    alt = ""
    img = pic(ev, src, pos, alt, sizes="(max-width:900px) 100vw, 60vw")
    strip = ""
    if c.get("strip", {}).get(vid):
        strip = ('<ol class="ev-strip" aria-label="Frames from the film">%s</ol>'
                 % "".join('<li><a href="https://www.youtube.com/watch?v=%s" data-vid="%s" aria-label="Play %s">'
                           '<img src="%s" width="1280" height="720" alt="" loading="lazy" decoding="async"></a></li>'
                           % (vid, vid, E(t), yt_frame(vid, k)) for k in c["strip"][vid]))
    return ('<figure class="ev-film">'
            '<div class="ev-fr" data-vid="%s">%s<a class="ev-play" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" '
            'aria-label="Play %s, %s">%s<span>Play</span></a></div>'
            '<figcaption><b>%s</b><span>%s &middot; %s views &middot; %s</span></figcaption>%s</figure>'
            % (vid, img, vid, E(t), ln, PLAY, E(t), ln, "{:,}".format(views), pub, strip))


def sheet(ev, c):
    L = [p for p in photos if p["day"] == c["day"]]
    out = []
    for i, p in enumerate(L, 1):
        r = p["w"] / p["h"]
        s = p["stem"]
        out.append('<figure class="ev-ph" id="%s" style="--r:%.4f;--c:%s"><a href="%s" data-stem="%s" data-i="%d">'
                   '<img src="%s" width="800" height="%d" alt="%s, photo %d of %d" loading="lazy" decoding="async"></a></figure>'
                   % (s, r, colors.get(s, "#2a2b30"), ph(ev["folder"], s, 2400), s, i, ph(ev["folder"], s, 800), round(800 / r),
                      c["name"], i, len(L)))
    return ('<div class="ev-sheet" data-day="%s" aria-label="The %d photos of %s, in the order shot">%s</div>'
            % (c["name"], len(L), c["name"], "".join(out)))


def chapters(ev):
    out = []
    for c in ev["chapters"]:
        if c.get("tbd"):
            out.append('<section class="ev-ch is-tbd" id="%s" aria-labelledby="h-%s"><header class="ev-ch-h"><p class="ev-ch-k">%s</p>'
                       '<h2 id="h-%s">%s</h2><p class="ev-ch-s">No film of this task in the season list. What happened: <i class="v2-tbd">[to supply]</i></p></header></section>'
                       % (c["id"], c["id"], "", c["id"], c["name"]))
            continue
        n = []
        if c["day"]:
            n.append("%d photos" % sum(1 for p in photos if p["day"] == c["day"]))
        if c["films"]:
            n.append("1 film" if len(c["films"]) == 1 else "%d films" % len(c["films"]))
        if not c["day"] and ev["folder"]:
            n.append("no photos this day")
        body = "".join(film(ev, c, v) for v in c["films"])
        if c["day"]:
            body += sheet(ev, c)
        out.append('<section class="ev-ch%s" id="%s" aria-labelledby="h-%s">'
                   '<header class="ev-ch-h"><p class="ev-ch-k">%s</p><h2 id="h-%s">%s</h2>%s</header>'
                   '<div class="ev-ch-b">%s</div></section>'
                   % (" has-sheet" if c["day"] else "", c["id"], c["id"], " &middot; ".join(n), c["id"], c["name"],
                      '<p class="ev-ch-s">%s</p>' % E(c["story"]) if c.get("story") else "", body))
    return "\n".join(out)


def season(ev):
    i = [s["key"] for s in SEASON].index(ev["key"])
    rows = []
    for j, s in enumerate(SEASON):
        lab = "Here" if j == i else ("Before" if j == i - 1 else ("Next" if j == i + 1 else ""))
        here = j == i
        inner = ('<span class="ev-r-k">%s</span><span class="ev-r-d">%s</span><span class="ev-r-n"><b>%s</b><small>%s &middot; %s</small></span>'
                 '<span class="ev-r-m">%s</span>' % (lab, s["when"], s["name"], s["edition"], s["where"], s["made"]))
        if here:
            rows.append('<li class="ev-r is-here" aria-current="page"><div class="ev-r-a">%s<span class="ev-r-go">You are here</span></div></li>' % inner)
        else:
            rows.append('<li class="ev-r%s"><a class="ev-r-a" href="%s">%s<span class="ev-r-go" aria-hidden="true">&rarr;</span></a></li>'
                        % (" is-adj" if lab else "", s["page"], inner))
    return ('<section class="ev-season" id="season" aria-labelledby="ev-season-t">'
            '<div class="ev-season-in"><header class="ev-season-h"><h2 id="ev-season-t">The 2026 season</h2>'
            '<a href="../../media.html#reach">The season on the Media page <i aria-hidden="true">&rarr;</i></a></header>'
            '<ol class="ev-rows">%s</ol></div></section>' % "".join(rows))


CTA = re.search(r'<section class="cta-band" id="book">.*?</section>', open(V4 + "/media-srs-piedrahita-2026.html").read(), re.S).group(0)

VIEWER = '''<dialog class="evv" id="evv" aria-label="The photo, enlarged">
  <div class="evv-top"><span class="evv-pos" aria-live="polite"></span><button class="evv-x" type="button" aria-label="Close the photo"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3 3 13"/></svg></button></div>
  <div class="evv-stage"><img alt="" draggable="false"><button class="evv-n evv-prev" type="button" aria-label="Previous photo"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg></button><button class="evv-n evv-next" type="button" aria-label="Next photo"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg></button></div>
  <div class="evv-foot">
    <p class="evv-name"><b></b><span></span></p>
    <div class="evv-acts"><a class="btn-lines evv-save" href="#" download data-hover>Save, free</a><a class="btn-solid" href="https://www.patreon.com/15133612/join" target="_blank" rel="noopener" data-hover><span>Join me on Patreon</span></a></div>
    <p class="evv-terms">Free web copy under <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="license noopener">CC BY-NC 4.0</a>: share it with the credit &ldquo;Photo: Aninder Singh, Paragliding Atlas&rdquo;, not for commercial use.</p>
  </div>
</dialog>'''


def page(ev):
    src = open(V4 + "/media-srs-piedrahita-2026.html").read()
    head, rest = src.split('<main id="v4-main"', 1)
    tail = rest.split("</main>", 1)[1]
    head = head.replace('"n":"Piedrahita 2026"', '"n":"%s"' % ev["loader"])
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % E(ev["title"]), head)
    head = head.replace('<link rel="stylesheet" href="v4-media.css?v=cbab97dd">\n<link rel="stylesheet" href="v4-gallery.css?v=cacda6f4">',
                        '<link rel="stylesheet" href="event-d.css">\n<script>document.documentElement.classList.add("ev-js");'
                        'if(!(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches))document.documentElement.classList.add("ev-run")</script>')
    if ev["key"] == "pwc":
        head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % E(ev["desc"]), head)
        head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % E(ev["desc"]), head)
        head = head.replace('<meta property="og:title" content="Piedrahita 2026">', '<meta property="og:title" content="%s">' % E(ev["title"]))
    tail = tail.replace('<script defer src="v4-media.js?v=7a7c7644"></script>\n<script defer src="v4-gallery.js?v=42d67cbc"></script>',
                        '<script defer src="event-d.js"></script>')
    def fix(m):
        a, u = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|tel:|#|data:|//)", u) or u in ("event-d.css", "event-d.js"):
            return m.group(0)
        return '%s="../../%s"' % (a, u)
    rel = lambda t: re.sub(r'\b(href|src)="([^"]*)"', fix, t)
    main = ('<main id="v4-main" class="ev ev-%s%s">\n%s%s<div class="ev-body">\n%s\n</div>\n%s\n%s\n%s\n</main>'
            % (ev["key"], " is-screen" if not ev["folder"] else "", cover(ev), slate(ev), chapters(ev), season(ev), rel(CTA), VIEWER if ev["folder"] else ""))
    s = rel(head) + main + rel(tail)
    open(OUT + "/" + ev["file"], "w").write(s)
    print("wrote", ev["file"], len(s))


os.makedirs(OUT, exist_ok=True)
for ev in (PIED, PWC):
    page(ev)
