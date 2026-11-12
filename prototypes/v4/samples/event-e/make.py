"""Designer E (Cloudbase), contest round 1 for the event landing pages: "Pull Back to the Race".

Writes index.html (SRS Piedrahita, photos and films) and pwc.html (PWC Super Final, films only) beside this file.
The page is the event's gallery page made immersive (same URL in the real build): the event's lead frame fills the
first screen; one screen of scroll pulls the camera back until that frame sits in its place on the race's line, task
by task; a tap on a task flies in to its photos and films; the foot pulls back once more, to the 2026 season, with
the event before and after.

Per event the chat fills in only EVENTS[...] below (in the real build: one entry beside COMPS in
tools/v4_comp_gallery.py); everything else (event-e.css, event-e.js, the shared gallery and viewer, v4-media.js's
play in place) is shared.

Facts: tools/v4_media.py (V, SEASON, UPCOMING), tools/v4_comp_gallery.py (COMPS) and the owner's YouTube frames.
Nothing else. Run: python3 prototypes/v4/samples/event-e/make.py
"""
import html
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
V4 = os.path.join(REPO, "prototypes", "v4")
sys.path.insert(0, os.path.join(REPO, "tools"))
import v4_media as M            # noqa: E402  V, SEASON, UPCOMING (read only)
import v4_comp_gallery as G     # noqa: E402  COMPS (read only)

E = html.escape
TBD = '<i class="v2-tbd">[to supply]</i>'
BASE = "https://paraglidingatlas-maker.github.io/media-2026/"
YT = "https://i.ytimg.com/vi/%s/%s.jpg"
PLAY = M.PLAY


def yt(v, q="maxresdefault"):
    return YT % (v, q)


def ph(folder, stem, w):
    return "%s%s/%s-%d.webp" % (BASE, folder, stem, w)


def srcset(folder, stem):
    return ", ".join("%s %dw" % (ph(folder, stem, w), w) for w in (800, 1600, 2400))


def secs(s):
    m, x = s.split(":")
    return int(m) * 60 + int(x)


# ---------------------------------------------------------------- the season (one list, every event page) ----
# the order of the Media page's "The 2026 season" (SEASON, then UPCOMING); "page" is where each event's landing
# page lives in this sample; Bassano has none yet, so its frame goes to the Media page's films
SEASON = [
    dict(key="pwc", name="PWC Super Final", short="PWC Super Final", when="May 2026", where="Pegalajar, Spain",
         made="5 films", page="pwc.html", img=yt("BRAX1XMU390", "maxres1"), fly=True),
    dict(key="srs4", name="SRS Bassano", short="SRS Bassano", when="May 2026", where="Monte Grappa, Italy",
         made="5 live broadcasts", page="../../media.html#watch", img=yt("PEyO6MXngUw", "maxres2"), fly=False,
         note="Films on the Media page"),
    dict(key="srs5", name="SRS Piedrahita", short="SRS Piedrahita", when="22 to 29 Aug 2026", where="Piedrahita, Spain",
         made="325 photos, 3 films", page="index.html", img=ph("srs-piedrahita", "SRS_5_T3_63", 800), fly=True),
    dict(key="tapalpa", name="SRS Tapalpa", short="SRS Tapalpa", when="8 to 14 Nov 2026", where="Tapalpa, Mexico",
         made="Photos and films every task day", page="../../media-srs-tapalpa-2026.html",
         img=ph("srs-tapalpa", "SRS_6_T1_62", 800), fly=True, window=["2026-11-08", "2026-11-14"], tz="America/Mexico_City"),
]


def season(here):
    i = [s["key"] for s in SEASON].index(here)
    items = []
    for k, s in enumerate(SEASON):
        st = "here" if k == i else ("before" if k < i else "after")
        extra = ' data-window="%s" data-tz="%s"' % (",".join(s["window"]), s["tz"]) if s.get("window") else ""
        tag = '<em class="ev-s-here">You are here</em>' if st == "here" else ('<em class="ev-s-now" data-now hidden>On now</em>' if s.get("window") else "")
        inner = ('<span class="ev-s-f"><img src="%s" alt="" width="800" height="533" loading="lazy" decoding="async"></span>'
                 '<span class="ev-s-t"><small>%s</small><b>%s</b><span>%s</span><span class="ev-s-m">%s</span>%s</span>'
                 % (s["img"], E(s["when"]), E(s["short"]), E(s["where"]), E(s.get("note") or s["made"]), tag))
        if st == "here":
            items.append('<li class="ev-s is-here"%s><span class="ev-s-a" aria-current="page">%s</span></li>' % (extra, inner))
        else:
            items.append('<li class="ev-s"%s><a class="ev-s-a" href="%s"%s>%s</a></li>'
                         % (extra, s["page"], " data-fly" if s["fly"] else "", inner))
    prev = SEASON[i - 1] if i > 0 else None
    nxt = SEASON[i + 1] if i + 1 < len(SEASON) else None

    def pn(s, cls, word, arrow):
        if not s:
            return ('<a class="ev-pn-a %s" href="../../media.html#e-season-t"><small>%s</small><b>The 2026 season</b>'
                    '<span>Every comp on the Media page</span></a>' % (cls, word))
        return ('<a class="ev-pn-a %s" href="%s"%s><small>%s</small><b>%s</b><span>%s, %s</span></a>'
                % (cls, s["page"], " data-fly" if s["fly"] else "", word, E(s["name"]), E(s["when"]), E(s["where"])))
    return '''
<section class="ev-season" id="season" aria-labelledby="ev-season-t">
  <div class="ev-season-in">
    <div class="ev-season-h">
      <p class="ev-k">Pull back once more</p>
      <h2 id="ev-season-t">The 2026 season</h2>
      <p class="ev-season-p">Four comps on our cameras, May to November. Tap one to fly in.</p>
    </div>
    <ol class="ev-ss" style="--k:%d">%s</ol>
    <nav class="ev-pn" aria-label="The comp before and after">%s%s</nav>
    <p class="ev-season-f"><a href="../../media.html">All our comp coverage on the Media page <i aria-hidden="true">&rarr;</i></a></p>
  </div>
</section>''' % (len(SEASON), "".join(items), pn(prev, "is-prev", "Before", "&larr;"), pn(nxt, "is-next", "Next", "&rarr;"))


# ---------------------------------------------------------------- the opening and the race line (shared) ----
def opening(ev):
    img = ev["lead_img"]
    return '''
<div class="ev-stage%(film)s" data-ev-stage>
 <div class="ev-cam">
  <header class="ev-open">
    <div class="ev-shot" data-shot aria-hidden="true"><div class="ev-shot-in"><img src="%(src)s"%(srcset)s sizes="100vw" width="%(w)d" height="%(h)d" alt="" fetchpriority="high" decoding="async"></div></div>
    <div class="ev-scrim" aria-hidden="true"></div>
    <a class="ev-back" href="#season"><i aria-hidden="true">&larr;</i> The 2026 season</a>
    <div class="ev-copy">
      <p class="ev-kicker">%(kicker)s</p>
      <h1 class="ev-name">%(name)s&nbsp;<span>%(year)s</span></h1>
      <p class="ev-facts">%(facts)s</p>
      <p class="ev-made">%(made)s</p>
      <p class="ev-acts">%(acts)s</p>
      <p class="ev-cue" aria-hidden="true"><i></i>Scroll to pull back to the race</p>
    </div>
  </header>
  <section class="ev-route" id="race" aria-labelledby="ev-route-t">
    <div class="ev-route-in">
      <div class="ev-route-h"><p class="ev-k">%(rk)s</p><h2 id="ev-route-t">%(rt)s</h2><p class="ev-route-p">%(rp)s</p></div>
      <ol class="ev-legs" style="--k:%(k)d">%(legs)s</ol>
    </div>
  </section>
 </div>
</div>''' % dict(film=" is-film" if ev.get("film_open") else "", src=img["src"],
                 srcset=(' srcset="%s"' % img["srcset"]) if img.get("srcset") else "", w=img["w"], h=img["h"],
                 kicker=ev["kicker"], name=ev["name"], year=ev["year"], facts="".join("<span>%s</span>" % f for f in ev["facts"]),
                 made=ev["made"], acts=ev["acts"], rk=ev["route_k"], rt=ev["route_t"], rp=ev["route_p"],
                 k=len(ev["legs"]), legs="".join(leg(x) for x in ev["legs"]))


def leg(x):
    if x.get("gap"):
        return ('<li class="ev-leg is-gap"><span class="ev-leg-a"><span class="ev-leg-f" aria-hidden="true"></span>'
                '<span class="ev-leg-t"><b>%s</b><span class="ev-leg-n">%s</span></span></span></li>' % (x["name"], x["n"]))
    return ('<li class="ev-leg"><a class="ev-leg-a" href="#%s"%s><span class="ev-leg-f"%s><img src="%s" alt="" width="%d" height="%d" '
            'decoding="async"></span><span class="ev-leg-t"><b>%s</b>%s<span class="ev-leg-n">%s</span></span></a></li>'
            % (x["id"], (' data-go="%d"' % x["go"]) if "go" in x else "", " data-target" if x.get("target") else "",
               x["img"], x["w"], x["h"], x["name"], ('<span class="ev-leg-l">%s</span>' % x["line"]) if x.get("line") else "", x["n"]))


# ---------------------------------------------------------------- the shell: the live Piedrahita page ----
SHELL = os.path.join(V4, "media-srs-piedrahita-2026.html")


def rel(s):
    """the shell lives in prototypes/v4/; this sample two folders down: re-point every relative href/src"""
    def fix(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(https?:|#|data:|mailto:|tel:|//|javascript:)", val) or not val:
            return m.group(0)
        if val.startswith("../../"):
            return '%s=%s../../%s%s' % (attr, q, val, q)
        return '%s=%s../../%s%s' % (attr, q, val, q)
    return re.sub(r'\b(href|src)=(["\'])([^"\']*)\2', fix, s)


def shell_parts():
    s = open(SHELL, encoding="utf-8").read()
    a = s.index('<main id="v4-main"')
    b = s.index("</main>")
    return s[:a], s[a:b], s[b:]


def head_tweak(head, title, desc, extra_css, drop_gallery=False):
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % E(title), head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % E(desc), head, count=1)
    head = head.replace('{"k":"page","n":"Piedrahita 2026"}', json.dumps({"k": "page", "n": title.split(":")[0]}))
    if drop_gallery:
        head = re.sub(r'<link rel="stylesheet" href="v4-gallery\.css[^"]*">\n?', "", head)
    head = head.replace("</head>", '<link rel="stylesheet" href="event-e.css">\n</head>', 1)
    return head


def tail_tweak(tail, drop_gallery=False):
    if drop_gallery:
        tail = re.sub(r'<script defer src="v4-gallery\.js[^"]*"></script>\n?', "", tail)
    tail = tail.replace("</body>", '<script defer src="event-e.js"></script>\n</body>', 1)
    return tail


def write(name, head, main, tail):
    out = rel(head) + main + rel(tail)
    # the event script and stylesheet sit beside the page: undo the re-pointing for those two
    out = out.replace('href="../../event-e.css"', 'href="event-e.css"').replace('src="../../event-e.js"', 'src="event-e.js"')
    out = re.sub(r'(href|src)="\.\./\.\./(pwc\.html|index\.html)"', r'\1="\2"', out)
    open(os.path.join(HERE, name), "w", encoding="utf-8").write(out)
    print("wrote", name, len(out))


# ---------------------------------------------------------------- SRS Piedrahita: the gallery made immersive ----
def piedrahita():
    c = G.COMPS["piedrahita"]
    head, main, tail = shell_parts()
    folder = c["folder"]
    try:
        photos = json.load(urllib.request.urlopen(BASE + folder + "/photos.json", timeout=20))
    except Exception:
        photos = G.photos("piedrahita")
    count = {}
    for p in photos:
        count[p["day"]] = count.get(p["day"], 0) + 1
    total = sum(count.values())
    films = sum(len(v) for v in c["videos"].values())
    # per task: its own frame (chosen from that task's photos), its line (COMPS stories), its counts
    pick = {"T1": "SRS_5_T1_10", "T2": "SRS_5_T2_55", "T3": "SRS_5_T3_63"}
    legs = []
    for i, t in enumerate(c["tasks"]):
        nf = len(c["videos"].get(t, []))
        n = "%d photos" % count.get(t, 0) + (" &middot; %d film%s" % (nf, "" if nf == 1 else "s") if nf else "")
        legs.append(dict(id="task-%d" % (i + 1), go=i, name="Task %d" % (i + 1), line=E(c["stories"][t]), n=n,
                         img=ph(folder, pick[t], 800), w=800, h=533, target=pick[t] == c["lead"]))
    ev = dict(kicker=c["kicker"], name="Piedrahita", year="2026",
              facts=["22 to 29 Aug 2026", "FAI Category 2", "120 pilots, 54 countries"],
              made='<span><b>%d</b> photos</span><span><b>%d</b> films</span><span>by Aninder Singh</span>' % (total, films),
              acts=('<a class="btn-solid" href="#race" data-ev-race data-hover><span>Find your photos</span></a>'
                    '<a class="btn-lines" href="#task-1" data-go="0" data-ev-to data-hover>Watch the films</a>'),
              lead_img=dict(src=ph(folder, c["lead"], 1600), srcset=srcset(folder, c["lead"]), w=2400, h=1600),
              route_k="The race", route_t="Three tasks, %d photos" % total,
              route_p="Tap a task for its photos and films. The photo you opened on is from Task 3.",
              legs=legs)
    body = main.replace('href="enquire.html', 'href="../../enquire.html')
    # the gallery's own lead goes; the opening and the race line take its place
    body = re.sub(r'<header class="gf-lead">.*?</header>\n', opening(ev) + "\n", body, count=1, flags=re.S)
    # the season, once the photos are done (inside main, before the viewer)
    body = body.replace('<dialog class="gfv"', season("srs5") + '\n\n<dialog class="gfv"', 1)
    # a way back to the season from the sticky task line
    body = body.replace('<div class="gf-line-in">',
                        '<a class="ev-line-s" href="#season" aria-label="The 2026 season: the comps before and after">'
                        '<span>2026</span><small>Season</small></a>\n  <div class="gf-line-in">', 1)
    head = head_tweak(head, "SRS Piedrahita 2026: Paragliding Atlas",
                      "SRS BGD Edition, Piedrahita, Spain, 22 to 29 Aug 2026: the race task by task, %d photos free to save and the films." % total,
                      "event-e.css")
    write("index.html", head, body, tail_tweak(tail))


# ---------------------------------------------------------------- PWC Super Final: films only ----
PWC_FILMS = [   # in the order flown; each film's three frames are YouTube's own stills from the owner's footage
    dict(v="FOuAWMeoxs4", id="day-1", name="Day 1", frame="maxres3"),
    dict(v="BRAX1XMU390", id="task-1", name="Task 1", frame="maxres1", line="An 86.5&nbsp;km sprint, and the most watched of our 13 comp films of 2026."),
    dict(v="7il6yV1vdIc", id="task-2", name="Task 2", frame="maxres1"),
    dict(gap=True, name="Task 3"),
    dict(v="op1-O01xkH4", id="task-4", name="Task 4", frame="maxres3"),
    dict(v="vPnIYYKcvEg", id="task-5", name="Task 5", frame="maxres3"),
]


def pwc():
    head, main, tail = shell_parts()
    films = [f for f in PWC_FILMS if not f.get("gap")]
    total_s = sum(secs(M.V[f["v"]][3]) for f in films)
    views = sum(M.V[f["v"]][2] for f in films)
    lead = max(films, key=lambda f: M.V[f["v"]][2])
    legs = []
    for f in PWC_FILMS:
        if f.get("gap"):
            legs.append(dict(gap=True, name=f["name"], n="Film " + TBD))
            continue
        c, t, k, ln, d, ep = M.V[f["v"]]
        legs.append(dict(id=f["id"], name=f["name"], n="%s &middot; %s views" % (ln, M.n(k)), img=yt(f["v"], f["frame"]),
                         w=1280, h=720, target=f is lead, line="On YouTube %s" % d))
    ev = dict(kicker="15th Paragliding World Cup Super Final &middot; Pegalajar, Spain", name="Super Final", year="2026",
              facts=["May 2026", "Pegalajar, Spain", "Pilots and countries " + TBD],
              made='<span><b>%d</b> films</span><span><b>%d</b> minutes</span><span>%s views on YouTube</span>' % (len(films), round(total_s / 60), M.n(views)),
              acts=('<a class="btn-solid" href="#%s" data-ev-play="%s" data-hover><span>Play %s, %s</span></a>'
                    '<a class="btn-lines" href="#race" data-ev-race data-hover>All five films</a>')
                   % (lead["id"], lead["v"], lead["name"], M.V[lead["v"]][3]),
              lead_img=dict(src=yt(lead["v"], lead["frame"]), w=1280, h=720), film_open=True,
              route_k="The race on film", route_t="Five films, %d minutes" % round(total_s / 60),
              route_p="Tap a day to play it. Each film opens on a frame from its own footage.",
              legs=legs)
    chips = "".join('<a href="#%s">%s</a>' % (f["id"], f["name"]) for f in films)
    chs = []
    for f in PWC_FILMS:
        if f.get("gap"):
            chs.append('\n<p class="ev-gap" id="task-3"><b>%s</b><span>Film %s</span></p>' % (f["name"], TBD))
            continue
        c, t, k, ln, d, ep = M.V[f["v"]]
        stills = "".join('<li><a href="https://www.youtube.com/watch?v=%s" data-ev-still="%s" aria-label="Play %s from here">'
                         '<img src="%s" alt="" width="1280" height="720" loading="lazy" decoding="async"></a></li>'
                         % (f["v"], f["v"], E(t), yt(f["v"], q)) for q in ("maxres1", "maxres2", "maxres3"))
        chs.append('''
<section class="ev-ch" id="%(id)s" aria-labelledby="ev-ch-%(id)s">
  <header class="ev-ch-h">
    <p class="ev-k">On YouTube %(d)s</p>
    <h2 id="ev-ch-%(id)s">%(name)s</h2>
    <p class="ev-ch-m"><span>%(t)s</span><span>%(ln)s</span><span>%(k)s views</span></p>
    %(line)s
    <p class="ev-ch-x">%(ep)s<a href="https://www.youtube.com/watch?v=%(v)s" target="_blank" rel="noopener">On YouTube <i aria-hidden="true">&nearr;</i></a></p>
  </header>
  <div class="ev-ch-film">
    <div class="md-frame" data-vid="%(v)s"><img src="%(poster)s" alt="" width="1280" height="720" loading="lazy" decoding="async"><a class="md-play" href="https://www.youtube.com/watch?v=%(v)s" target="_blank" rel="noopener" aria-label="Play %(t)s, PWC Super Final">%(play)s</a></div>
    <ul class="ev-stills" aria-label="Three frames from the film">%(stills)s</ul>
  </div>
</section>''' % dict(id=f["id"], d=d, name=f["name"], t=E(t), ln=ln, k=M.n(k), v=f["v"], poster=yt(f["v"], f["frame"]),
                     play=PLAY, stills=stills,
                     line=('<p class="ev-ch-l">%s</p>' % f["line"]) if f.get("line") else "",
                     ep=('<a href="../../episodes/%s.html">Read the episode <i aria-hidden="true">&rarr;</i></a>' % ep) if ep else ""))
    body = '<main id="v4-main" class="ev-films">\n' + opening(ev) + '''
<div class="ev-body">
<nav class="ev-bar" aria-label="The Super Final, day by day">
  <a class="ev-line-s" href="#season" aria-label="The 2026 season: the comps before and after"><span>2026</span><small>Season</small></a>
  <div class="ev-bar-in">%s</div>
</nav>
<div class="ev-chs">%s
</div>
</div>
''' % (chips, "".join(chs)) + season("pwc") + "\n"
    head = head_tweak(head, "PWC Super Final 2026: Paragliding Atlas",
                      "15th Paragliding World Cup Super Final, Pegalajar, Spain, May 2026: the race on film, %d films, every one plays here." % len(films),
                      "event-e.css", drop_gallery=True)
    write("pwc.html", head, body, tail_tweak(tail, drop_gallery=True))


if __name__ == "__main__":
    piedrahita()
    pwc()
