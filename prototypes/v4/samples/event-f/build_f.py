#!/usr/bin/env python3
"""Designer F (Turnpoint), event landing pages, contest round 1 (12 Nov 2026).
Writes prototypes/v4/samples/event-f/index.html (SRS Piedrahita) and pwc.html (PWC Super Final, films only).
The Piedrahita page IS today's gallery page (same markup, same v4-gallery.css/js), with a new opening, the season
line zooming into the task line, and the season at the foot. PWC is the same template with films in the stops."""
import datetime
import html
import re

REPO = "/home/user/website"
V4 = REPO + "/prototypes/v4/"
OUT = V4 + "samples/event-f/"
E = html.escape
TBD = '<span class="v2-tbd">[to supply]</span>'
PH = "https://paraglidingatlas-maker.github.io/media-2026/"

# ---------------------------------------------------------------- the 2026 season (tools/v4_media.py SEASON, UPCOMING)
# span: Piedrahita and Tapalpa their own dates; PWC and Bassano the days their films and broadcasts came out
LINE = (datetime.date(2026, 5, 1), datetime.date(2026, 12, 1))
SEASON = [
    dict(key="pwc", name="PWC Super Final", short="PWC", edition="15th Paragliding World Cup Super Final",
         where="Pegalajar, Spain", when="May 2026", tag="May", made="5 highlight videos",
         span=("2026-05-13", "2026-05-20"), href="pwc.html"),
    dict(key="srs4", name="SRS Bassano", short="Bassano", edition="SRS Skywalk Bassano Edition",
         where="Monte&nbsp;Grappa, Italy", when="May 2026", tag="May",
         made="Live commentary: 5 broadcasts, 21&nbsp;h&nbsp;42&nbsp;min on air",
         span=("2026-05-25", "2026-05-30"), href="../../media.html#reach", planned=True),
    dict(key="srs5", name="SRS Piedrahita", short="Piedrahita", edition="SRS BGD Edition",
         where="Piedrahita, &Aacute;vila, Spain", when="22 to 29 Aug 2026", tag="22 to 29 Aug",
         made="325 photos and 3 films", span=("2026-08-22", "2026-08-29"), href="index.html"),
    dict(key="tapalpa", name="SRS Tapalpa", short="Tapalpa", edition="SRS Advance Edition",
         where="Tapalpa, Mexico", when="8 to 14 Nov 2026", tag="Now", made="7 tasks, 116 pilots from 44 countries; photos and films each task day",
         span=("2026-11-08", "2026-11-14"), href="../../media-srs-tapalpa-2026.html", now=True),
]
TOTAL = (LINE[1] - LINE[0]).days


def at(s):
    return (datetime.date.fromisoformat(s) - LINE[0]).days / TOTAL


def season_strip(cur, n):
    """the 2026 season line at the opening's foot, this event lit, and the fan that opens it into the task line"""
    i = [e["key"] for e in SEASON].index(cur)
    ev = SEASON[i]
    xa, xb = at(ev["span"][0]), at(ev["span"][1]) + 1 / TOTAL
    bars, names = [], []
    for e in SEASON:
        a, b = at(e["span"][0]), at(e["span"][1]) + 1 / TOTAL
        lit = e["key"] == cur
        cls = "ef-bar" + (" is-lit" if lit else "") + (" is-now" if e.get("now") else "")
        bars.append('<i class="%s" style="--x:%.4f;--w:%.4f"></i>' % (cls, a, b - a))
        lab = '<b>%s</b><small>%s</small>' % (E(e["short"]), e["tag"])
        if lit:
            names.append('<span class="ef-nm is-lit" style="--x:%.4f" aria-current="page">%s</span>' % (a, lab))
        else:
            names.append('<a class="ef-nm%s" style="--x:%.4f" href="%s">%s</a>'
                         % (" is-now" if e.get("now") else "", a, e["href"], lab))
    prev = SEASON[i - 1] if i > 0 else None
    nxt = SEASON[i + 1] if i + 1 < len(SEASON) else None
    pn = ('<a class="ef-pn-p" href="%s"><i aria-hidden="true">&larr;</i> <span><b>%s</b> %s</span></a>'
          % (prev["href"], E(prev["name"]), prev["tag"]) if prev else
          '<span class="ef-pn-p is-first"><span>The season starts here</span></span>')
    pn += ('<a class="ef-pn-n" href="%s"><span><b>%s</b> %s</span> <i aria-hidden="true">&rarr;</i></a>'
           % (nxt["href"], E(nxt["name"]), nxt["tag"]) if nxt else "")
    L = 50.0 / n                       # the task line's track runs from the first column's middle to the last's
    fan = ('<svg class="ef-fan" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
           '<defs><linearGradient id="ef-beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7517" stop-opacity=".22"/>'
           '<stop offset="1" stop-color="#ff7517" stop-opacity="0"/></linearGradient></defs>'
           '<path class="ef-beam" d="M%.3f 0 L%.3f 0 L%.3f 100 L%.3f 100 Z" fill="url(#ef-beam)"/>'
           '<line x1="%.3f" y1="0" x2="%.3f" y2="100"/><line x1="%.3f" y1="0" x2="%.3f" y2="100"/></svg>'
           % (xa * 100, xb * 100, 100 - L, L, xa * 100, L, xb * 100, 100 - L))
    return ('<nav class="ef-season" aria-label="The 2026 season: %s is event %d of %d">\n'
            '  <div class="ef-season-in" style="--xa:%.4f;--xb:%.4f">\n'
            '    <p class="ef-pn">%s</p>\n'
            '    <p class="ef-sh"><a href="../../media.html#reach">The 2026 season</a><span>%d of %d</span></p>\n'
            '    <div class="ef-strip"><span class="ef-names">%s</span><span class="ef-rule" aria-hidden="true">%s</span></div>\n'
            '    %s\n  </div>\n</nav>\n'
            % (E(ev["name"]), i + 1, len(SEASON), xa, xb, pn, i + 1, len(SEASON), "".join(names), "".join(bars), fan))


def season_rows(cur):
    """the foot: the whole season, each event at its real dates with its readout and one link"""
    rows = []
    for e in SEASON:
        here = e["key"] == cur
        go = ('<span class="ef-row-go is-here">You are here</span>' if here else
              '<a class="ef-row-go" href="%s">%s <i aria-hidden="true">&rarr;</i></a>'
              % (e["href"], "Open the season on Media" if e.get("planned") else "Open"))
        a, b = at(e["span"][0]), at(e["span"][1]) + 1 / TOTAL
        rows.append('<li class="ef-row%s%s"><span class="ef-row-d">%s%s</span>'
                    '<span class="ef-row-n"><b>%s</b><small>%s &middot; %s</small></span>'
                    '<span class="ef-row-m">%s</span>'
                    '<span class="ef-row-bar" aria-hidden="true"><i style="--x:%.4f;--w:%.4f"></i></span>%s</li>'
                    % (" is-here" if here else "", " is-now" if e.get("now") else "",
                       '<i class="ef-tally" aria-hidden="true"></i>Now &middot; ' if e.get("now") else "",
                       e["when"], E(e["name"]), e["edition"], e["where"], e["made"], a, b - a, go))
    note = ('<p class="ef-rows-f">Dates: Piedrahita and Tapalpa the comps\' own; PWC and Bassano the month their films '
            'and broadcasts came out (the comps\' own dates %s). Bassano\'s own page: %s</p>' % (TBD, TBD))
    return ('<section class="ef-foot" aria-labelledby="ef-foot-t"><div class="ef-foot-in">'
            '<h2 id="ef-foot-t" class="ef-foot-h">The 2026 Season</h2>'
            '<ol class="ef-rows">%s</ol>%s</div></section>\n' % ("".join(rows), note))


# ---------------------------------------------------------------- the shell, from today's Piedrahita page
src = open(V4 + "media-srs-piedrahita-2026.html").read()


def rel(s):
    """the sample sits two folders below v4: every relative URL gets ../../ in front"""
    def fix(m):
        a, q, u = m.group(1), m.group(2), m.group(3)
        if re.match(r"(https?:|#|mailto:|tel:|data:|/|javascript:|\?)", u) or u == "":
            return m.group(0)
        return '%s=%s../../%s' % (a, q, u)
    return re.sub(r'\b(href|src)=(["\'])([^"\']*)', fix, s)


page = rel(src)
page = page.replace('<link rel="stylesheet" href="../../v4-gallery.css',
                    '<link rel="stylesheet" href="event-f.css">\n<link rel="stylesheet" href="../../v4-gallery.css')
# my CSS must come after the gallery's: move it behind
page = page.replace('<link rel="stylesheet" href="event-f.css">\n', '')
page = re.sub(r'(<link rel="stylesheet" href="\.\./\.\./v4-gallery\.css[^>]*>)', r'\1\n<link rel="stylesheet" href="event-f.css">', page)
page = re.sub(r'(<script defer src="\.\./\.\./v4-gallery\.js[^>]*></script>)', r'\1\n<script defer src="event-f.js"></script>', page)
page = page.replace('<meta name="robots" content="noindex, nofollow">',
                    '<meta name="robots" content="noindex, nofollow"><!-- designer F sample, event landing pages, round 1 -->')

# ---------------------------------------------------------------- Piedrahita: the opening
lead = "SRS_5_T3_63"
opening = '''<header class="gf-lead ef-open">
  <div class="gf-lead-media"><img src="{ph}srs-piedrahita/{s}-1600.webp" srcset="{ph}srs-piedrahita/{s}-800.webp 800w, {ph}srs-piedrahita/{s}-1600.webp 1600w, {ph}srs-piedrahita/{s}-2400.webp 2400w" sizes="100vw" width="1600" height="1067" alt="Dozens of wings in a deep blue sky over Piedrahita, Task 3" fetchpriority="high"></div>
  <div class="gf-lead-copy ef-copy">
    <a class="gf-back" href="../../media.html"><i aria-hidden="true">&larr;</i> Media</a>
    <p class="gf-kicker">SRS BGD Edition &middot; Piedrahita, &Aacute;vila, Spain</p>
    <h1 class="gf-name ef-name">Piedrahita <span>2026</span></h1>
    <p class="ef-read"><span><b>22 to 29 Aug 2026</b></span><span>120 pilots, 54 countries</span><span>FAI Category 2</span></p>
    <p class="ef-have"><a href="#task-3"><b>325</b> photos</a><a href="#task-1"><b>3</b> films</a><a class="ef-off" href="https://airtribune.com/srs-2026-5/info" target="_blank" rel="noopener">Official event <i aria-hidden="true">&nearr;</i></a></p>
  </div>
</header>
'''.format(ph=PH, s=lead)
pied = re.sub(r'<header class="gf-lead">.*?</header>\n', lambda m: opening, page, count=1, flags=re.S)
pied = pied.replace('<div class="gf-body">\n<nav class="gf-line"', '<div class="gf-body">\n' + season_strip("srs5", 3) + '<nav class="gf-line"', 1)
pied = pied.replace('<section class="cta-band" id="book">', season_rows("srs5") + '<section class="cta-band" id="book">', 1)
pied = pied.replace('<main id="v4-main" class="gf"', '<main id="v4-main" class="gf ef" data-ev="srs5"', 1)
assert pied.count("ef-season") >= 1 and pied.count("ef-open") == 1 and "ef-foot" in pied
open(OUT + "index.html", "w").write(pied)

# ---------------------------------------------------------------- PWC: films only, the same template
# id: (stop, title, views, length, out, episode) from tools/v4_media.py V; the poster is a frame of the film itself
PWC = [
    ("day-1", "Day 1", "FOuAWMeoxs4", "Day 1 Highlights", 3537, "6:44", "13 May", "highlights-day-1-pwca-superfinal-2026", "maxres3"),
    ("task-1", "Task 1", "BRAX1XMU390", "Task 1 Highlights", 7342, "6:53", "14 May", "task-1-highlights-15th-paragliding-world-cup-super-final", "maxres1"),
    ("task-2", "Task 2", "7il6yV1vdIc", "Task 2 Highlights", 4034, "8:17", "16 May", "task-2-highlights-15th-paragliding-world-cup-super-final", "maxres1"),
    ("task-3", "Task 3", None, None, 0, None, None, None, None),
    ("task-4", "Task 4", "op1-O01xkH4", "Task 4 Highlights", 3437, "7:47", "18 May", "task-4-highlights-15th-paragliding-world-cup-super-final", "maxres3"),
    ("task-5", "Task 5", "vPnIYYKcvEg", "Task 5 Highlights", 3340, "8:08", "20 May", "task-5-highlights-15th-paragliding-world-cup-super-final", "maxres3"),
]
N = len(PWC)
OPEN = 1           # the most watched film opens first (the Media page's showreel lead, REEL)
PLAY = ('<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 1.2v7.6c0 .5.5.8.9.5l5.9-3.8c.4-.2.4-.8 0-1L2.9.7C2.5.4 '
        '2 .7 2 1.2z"/></svg>')
GLIDER = ('<span class="gf-glc" aria-hidden="true"><span class="gf-glw"><i class="gf-glider"><svg viewBox="0 0 22 14" aria-hidden="true">'
          '<path d="M1.5 5.2C6 1.4 16 1.4 20.5 5.2" stroke-width="1.6"/><path d="M2.6 5 11 12.2 19.4 5" stroke-width=".6"/>'
          '<circle cx="11" cy="12" r="1.5" fill="currentColor" stroke="none"/></svg></i></span></span>')

tps, stops = [], []
for i, (sid, name, vid, title, views, ln, out, ep, fr) in enumerate(PWC):
    st = "film" if vid else "none"
    rd = ('<span class="gf-tp-d">%s</span><span class="gf-tp-s">Out %s</span>' % (ln, out) if vid else
          '<span class="gf-tp-d">No film</span><span class="gf-tp-s">&nbsp;</span>')
    tps.append('<li class="gf-tp%s" data-i="%d" data-state="%s"><a href="#%s"%s><i class="gf-dot" aria-hidden="true"></i><b>%s</b>%s</a></li>'
               % ("", i, st, sid, "", name, rd))   # no JS: every stop stacked from Day 1, the glider on Day 1
    nav = []
    if i > 0:
        nav.append('<a class="gf-df-p" href="#%s" data-go="%d"><i aria-hidden="true">&larr;</i> %s</a>' % (PWC[i - 1][0], i - 1, PWC[i - 1][1]))
    if i + 1 < N:
        nav.append('<a class="gf-df-n" href="#%s" data-go="%d">Next leg: %s <i aria-hidden="true">&rarr;</i></a>' % (PWC[i + 1][0], i + 1, PWC[i + 1][1]))
    if vid:
        body = ('<div class="ef-screen"><div class="md-frame" data-vid="%s"><img src="https://i.ytimg.com/vi/%s/%s.jpg" alt="" width="1280" height="720" loading="%s" decoding="async">'
                '<a class="md-play" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" aria-label="Play %s, PWC Super Final">%s</a></div>'
                '<div class="ef-screen-f"><p class="ef-screen-t">%s</p>'
                '<p class="ef-screen-m"><span>%s</span><span>%s views</span><span>Out %s 2026</span></p>'
                '<p class="ef-screen-a"><a href="../../episodes/%s.html">Read the episode <i aria-hidden="true">&rarr;</i></a>'
                '<a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">Watch on YouTube <i aria-hidden="true">&nearr;</i></a></p></div></div>'
                % (vid, vid, fr, "eager" if i == OPEN else "lazy", vid, E(title), PLAY, E(title), ln, "{:,}".format(views), out, ep, vid))
        head = '<p class="gf-dh-r"><span>%s</span><span>Out %s 2026</span></p>' % (ln, out)
    else:
        body = ('<div class="ef-none"><p>No highlights film from Task 3 in the archive. Whether the task was flown, '
                'and its film: %s</p></div>' % TBD)
        head = '<p class="gf-dh-r"><span>No film</span></p>'
    stops.append('<section class="gf-day ef-stop%s" id="%s" data-i="%d" data-state="%s" aria-labelledby="ef-h-%d"><header class="gf-dh"><h2 id="ef-h-%d">%s</h2>%s</header>%s'
                 '<nav class="gf-df" aria-label="Other stops">%s</nav></section>'
                 % (" is-open" if i == OPEN else "", sid, i, st, i, i, name, head, body, "".join(nav)))

line = ('<nav class="gf-line ef-fline" aria-label="PWC Super Final, the films by task" style="--flown:%d;--open:%d">\n  <div class="gf-line-in">\n'
        '    <span class="gf-track" aria-hidden="true"><i class="gf-flown"></i></span>\n    %s\n    <ol class="gf-tps">%s</ol>\n  </div>\n</nav>\n'
        % (N - 1, 0, GLIDER, "".join(tps)))
amb = "https://i.ytimg.com/vi/op1-O01xkH4/maxres2.jpg"
pwc_main = '''<main id="v4-main" class="gf ef ef-films" data-ev="pwc" style="--n:{n}">

<header class="gf-lead ef-open ef-open--film">
  <div class="gf-lead-media"><img src="{amb}" width="1280" height="720" alt="A task drawn in red on a relief map, a frame from Task 4 Highlights" fetchpriority="high"></div>
  <div class="gf-lead-copy ef-copy">
    <a class="gf-back" href="../../media.html"><i aria-hidden="true">&larr;</i> Media</a>
    <p class="gf-kicker">15th Paragliding World Cup Super Final &middot; Pegalajar, Spain</p>
    <h1 class="gf-name ef-name">Pegalajar <span>2026</span></h1>
    <p class="ef-read"><span><b>May 2026</b></span><span>Comp dates {tbd}</span><span>Pilots {tbd}</span></p>
    <p class="ef-have"><a href="#task-1"><b>5</b> highlight films</a><span><b>21,690</b> views on YouTube, 3 Nov 2026</span><span class="ef-off">Official event {tbd}</span></p>
  </div>
</header>

<div class="gf-body">
{season}{line}
<div class="gf-days">
{stops}
</div>
</div>

{foot}<section class="cta-band" id="book">'''.format(n=N, amb=amb, tbd=TBD, season=season_strip("pwc", N), line=line,
                                                      stops="\n".join(stops), foot=season_rows("pwc"))

pwc = page
pwc = re.sub(r'<main id="v4-main".*?<section class="cta-band" id="book">', lambda m: pwc_main, pwc, count=1, flags=re.S)
# no photos on this page: no photo viewer, no gallery data, no gallery script; the films play through v4-media.js
pwc = re.sub(r'<dialog class="gfv".*?</dialog>\s*', '', pwc, flags=re.S)
pwc = re.sub(r'<script type="application/json" id="gf-data">.*?</script>\s*', '', pwc, flags=re.S)
pwc = re.sub(r'<script defer src="\.\./\.\./v4-gallery\.js[^>]*></script>\n?', '', pwc)
pwc = pwc.replace("<title>Piedrahita 2026: Paragliding Atlas</title>", "<title>PWC Super Final 2026: Paragliding Atlas</title>")
desc = "15th Paragliding World Cup Super Final, Pegalajar, Spain, May 2026: the five highlight films, by task. Films by Aninder Singh, Paragliding Atlas."
pwc = re.sub(r'(<meta (?:name|property)="(?:og:)?description" content=")[^"]*', lambda m: m.group(1) + desc, pwc)
pwc = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\1PWC Super Final 2026', pwc)
pwc = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\1https://i.ytimg.com/vi/BRAX1XMU390/maxres1.jpg', pwc)
pwc = pwc.replace("media-srs-piedrahita-2026.html", "media-pwc-superfinal-2026.html")
pwc = re.sub(r'\{"k":"page","n":"Piedrahita 2026"\}', '{"k":"page","n":"PWC Super Final 2026"}', pwc)
pwc = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "WebPage".*?</script>\n?', '', pwc, flags=re.S)
pwc = pwc.replace('Every task day: stills like these, and Daily Highlights, a video each task day with social clips and a results newsletter.', 'Every task day: Daily Highlights like these, a video each task day with social clips and a results newsletter.')
assert 'stills like these' not in pwc
assert "gf-data" not in pwc and "ef-fline" in pwc
open(OUT + "pwc.html", "w").write(pwc)
print("wrote index.html (%d KB) and pwc.html (%d KB)" % (len(pied) // 1024, len(pwc) // 1024))
