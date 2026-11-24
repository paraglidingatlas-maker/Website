#!/usr/bin/env python3
"""The SRS 2027 race calendar, online (chat 29, 23 Nov 2026).

Owner, 23 Nov: "put this online and put the lable in the place next instead of srs lvie"; earlier: "a digital
calendar for download like a luxry immersive experiecne to go on the webnsite". The calendar's pages are made in the
calendar design chat (their sources: tools/srs_calendar_2027/), one page at a time, from the owner's SRS 2026
Tapalpa photos; this writes the page that shows them:

  prototypes/v4/srs-2027-calendar.html   the opening (the cover, the words, Add to calendar), the months as a line
                                         (the ones still being made are dimmed), every finished page large on its
                                         own glow with Download and Share (three ways of laying a page out, in
                                         turn: centred, to the left with its words beside it, to the right; owner,
                                         23 Nov: "use different styles for different pics"), the months on their way, the five rounds
                                         with their dates, the credit and the next step

A page is shown as soon as its two files are in prototypes/v4/img/calendar/srs-2027/ (NN-name-1200.webp and
NN-name-2400.webp); a month without them is listed under "On Their Way". So a new month is: copy its two files
there, run this and tools/v4_nav_live.py, commit, build, gates, push (docs/v4-next-session.md, chat 29).

Its files: v4-calendar.css and v4-calendar.js (the viewer; without JavaScript each page is a link to its large
image), on tools/v4_media.py's shell (the About page's head, nav and footer; v4-share.js). An owned page like the
media pages (tools/v4_build.py owned()), new on the site (tools/v2_site.py NEW_PAGES), so the switch lists it in
sitemap.xml. The nav item that leads here is tools/v4_nav_live.py STAND.

Facts: the rounds and their dates as sportsracingseries.org/events listed them on 23 Nov 2026 (the design chat's
brief); the photo of each page from that brief. Nothing else.

    python3 tools/v4_srs_calendar.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_media as M  # noqa: E402  (shell(), check(), ver())

V4 = M.V4
NAME = "srs-2027-calendar.html"
IMG = "img/calendar/srs-2027/"
E = M.E
SRS = "https://sportsracingseries.org/events/"
READ = "23 Nov 2026"          # when the dates were read from the SRS events page

# n, place, country, dates, the month it falls in (1 to 12), status
ROUNDS = [("01", "Lijak", "Slovenia", "15 to 21 Mar 2027", 3, "Confirmed"),
          ("02", "St Jean Montclar", "France", "20 to 27 Jun 2027", 6, "Provisional"),
          ("03", "Gemona", "Italy", "17 to 24 Jul 2027", 7, "Confirmed"),
          ("04", "Krushevo", "North Macedonia", "22 to 29 Aug 2027", 8, "Confirmed"),
          ("05", "St André", "France", "12 to 19 Sep 2027", 9, "Confirmed")]
# file stem, anchor, name, the Tapalpa task its photo is from, what the photo shows
PAGES = [("01-cover", "cover", "Cover", "Task 1",
          "a pilot in a pod harness under an orange and navy wing, lit on black above its reflection, SRS 2027 in orange brush lettering behind"),
         ("02-january", "january", "January", "Task 6", "a pink, orange and yellow wing against dark forest"),
         ("03-february", "february", "February", "Task 6", "an orange and teal wing, the ground a blur behind it"),
         ("04-march", "march", "March", "Task 4", "a white and blue wing banking"),
         ("05-april", "april", "April", "Task 4", "a pilot in a black and red pod harness, close"),
         ("06-may", "may", "May", "Task 4", "two white and blue wings over forest"),
         ("07-june", "june", "June", "Task 4", "a gaggle of red, yellow and green wings over the hills"),
         ("08-july", "july", "July", "Task 3", "an orange, yellow and white wing seen from the side"),
         ("09-august", "august", "August", "Task 3", "an orange wing over fields and greenhouses"),
         ("10-september", "september", "September", "Task 3", "a gaggle of wings in a blue sky above the clouds"),
         ("11-october", "october", "October", "Task 3", "a pilot in a yellow pod harness under a lime wing, light trails streaked behind him"),
         ("12-november", "november", "November", "Task 6", "a pilot in a yellow pod under a yellow wing, seen from above over rows of greenhouses"),
         ("13-december", "december", "December", "Task 6",
          "a pilot in a pod harness under a lime wing, the daylight sky graded to sunset colours")]
PDF = "SRS-2027-Race-Calendar.pdf"   # the whole calendar (the design chat, 24 Nov 2026); its button shows when the file is there
W, H = 2400, 1696              # every page: A4 landscape


def ready(stem):
    return all(os.path.isfile(os.path.join(V4, IMG, "%s-%d.webp" % (stem, w))) for w in (1200, 2400))


def pic(stem, w):
    """a page's image with ?v= its content hash: a corrected page (October's wing, 24 Nov) then reaches a visitor
    who has the old one cached under the same name"""
    name = "%s%s-%d.webp" % (IMG, stem, w)
    return "%s?v=%s" % (name, M.ver(name))


def round_of(k):
    """the round held in month k (0 = the cover), or None"""
    return next((r for r in ROUNDS if r[4] == k), None)


def no(k):
    return "%02d / 12" % k if k else "Cover"


def sheet(k, stem, slug, name, task, shows):
    r = round_of(k)
    note = ('<span class="cal-rd"><b>Round %s</b> %s, %s &middot; %s%s</span>'
            % (r[0], E(r[1]), r[2], r[3][:-5], " &middot; provisional" if r[5] == "Provisional" else "")) if r else ""
    alt = ("The cover of the SRS 2027 race calendar: %s, and the five rounds with their dates" % shows if not k else
           "The %s 2027 page of the SRS race calendar: %s, beside the month's dates" % (name, shows))
    big, small = pic(stem, 2400), pic(stem, 1200)
    dl = "SRS-2027-Race-Calendar-%s.webp" % name
    return '''<figure class="cal-sheet cal-%(lay)s" id="%(slug)s" data-share-box>
  <span class="cal-glow" style="background-image:url(%(small)s)" aria-hidden="true"></span>
  <a class="cal-page" href="%(big)s" data-cal="%(i)d" aria-label="%(name)s: see the page large">
    <img src="%(small)s" srcset="%(small)s 1200w, %(big)s 2400w" sizes="(max-width:760px) 100vw, min(1500px, 88vw)" width="%(w)d" height="%(h)d" alt="%(alt)s"%(lazy)s>
  </a>
  <figcaption>
    <span class="cal-no">%(no)s</span>
    <h2 data-t>%(name)s</h2>
    %(note)s
    <span class="cal-ph">Photo: SRS Tapalpa 2026, %(task)s</span>
    <span class="cal-act">
      <a class="cal-dl" href="%(big)s" download="%(dl)s"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3v10M6.2 9.2 10 13l3.8-3.8M4 16.5h12"/></svg><span>Download</span></a>
      <button type="button" data-share data-share-url="#%(slug)s" data-share-title="%(title)s"></button>
    </span>
  </figcaption>
</figure>''' % dict(lay="abc"[k % 3], slug=slug, small=small, big=big, i=k, name=name, w=W, h=H, alt=E(alt), no=no(k), note=note, task=task, dl=dl,
                    title=name, lazy="" if not k else ' loading="lazy" decoding="async"')


def page():
    have = [(k, p) for k, p in enumerate(PAGES) if ready(p[0])]
    wait = [(k, p) for k, p in enumerate(PAGES) if not ready(p[0])]
    assert have and have[0][0] == 0, "the cover is missing from " + IMG
    months = [p[2] for k, p in have if k]
    # "January to August" when the finished months run on without a gap, else each by name
    run = all(a[0] + 1 == b[0] for a, b in zip(have, have[1:]))
    here = ("%s to %s" % (months[0], months[-1]) if run and len(months) > 1 else ", ".join(months)) if months else ""
    soon = [p[2] for _, p in wait]
    soon_run = ("%s to %s" if len(soon) > 2 else "%s and %s") % (soon[0], soon[-1]) if len(soon) > 1 else (soon[0] if soon else "")
    if wait:
        status = "The cover and %s are here. %s %s on %s way." % (here, soon_run, "are" if len(soon) > 1 else "is",
                                                               "their" if len(soon) > 1 else "its")
    else:
        status = "The cover and all twelve months are here."
    rail = "".join('<li><a href="#%s">%s</a></li>' % (p[1], "Cover" if not k else p[2][:3]) if ready(p[0]) else
                   '<li><span title="%s: on its way">%s</span></li>' % (p[2], p[2][:3]) for k, p in enumerate(PAGES))
    sheets = "\n".join(sheet(k, *p) for k, p in have)
    cover = PAGES[0]
    c_small, c_big = pic(cover[0], 1200), pic(cover[0], 2400)
    rounds = "".join(
        '<li%s><span class="cal-r-n">Round %s</span><b>%s</b><span class="cal-r-c">%s</span><span class="cal-r-d">%s</span>'
        '<span class="cal-r-s">%s</span></li>' % (' class="is-prov"' if r[5] == "Provisional" else "", r[0], E(r[1]), r[2], r[3], r[5])
        for r in ROUNDS)
    coming = ""
    if wait:
        tiles = ""
        for k, p in wait:
            r = round_of(k)
            tiles += ('<li><span class="cal-no">%s</span><b>%s</b>%s</li>'
                      % (no(k), p[2], '<span>Round %s &middot; %s, %s &middot; %s</span>' % (r[0], E(r[1]), r[2], r[3][:-5]) if r else ""))
        coming = '''
<section class="kit-band cal-soon" id="on-their-way" aria-labelledby="cal-soon-t">
  <div class="kit-in">
    <div class="kit-head"><span class="kit-kicker">Still Being Made</span><h2 class="kit-title" id="cal-soon-t">On Their Way</h2>
      <p class="kit-intro">%s %s Wallpapers and the complete calendar as one PDF follow once all twelve months are done.</p></div>
    <ul class="cal-wait">%s</ul>
  </div>
</section>''' % (soon_run, "are being made now, one page at a time, and will appear here as each is finished." if len(soon) > 1
                 else "is being made now and will appear here when it is finished.", tiles)
    pdf = pdf_note = ""
    what = "any page"
    pdf_path = os.path.join(V4, IMG, PDF)
    if os.path.isfile(pdf_path) and not wait:        # the PDF is the complete calendar: only beside all twelve months
        mb = os.path.getsize(pdf_path) / 1e6
        pdf = ('        <a class="btn-lines" href="%s%s?v=%s" download="%s" data-hover>Download the PDF</a>\n'
               % (IMG, PDF, M.ver(IMG + PDF), PDF))
        pdf_note = " The PDF is the whole calendar: %d pages, A4 landscape, %.1f MB." % (len(have), mb)
        what = "the whole calendar as a PDF or any page on its own"
    main = '''
<!-- chat 29, 23 Nov 2026: the SRS 2027 race calendar (tools/v4_srs_calendar.py). The signature moment: every page
     of the calendar lies on a glow of its own colours, like a print under a lamp. Reduced motion and no JavaScript
     show the finished page; without JavaScript a page opens as its large image. -->
<div class="cal" data-n="%(n)d">
<header class="cal-open">
  <span class="cal-glow" style="background-image:url(%(c_small)s)" aria-hidden="true"></span>
  <div class="cal-open-in">
    <div class="cal-open-copy">
      <span class="kit-kicker">Sports-Class Racing Series &middot; Download</span>
      <h1>SRS 2027 Race Calendar</h1>
      <p class="kit-intro">The five rounds of the 2027 season, month by month, on photographs from SRS Tapalpa 2026. Download %(what)s, or put the rounds in your own calendar.</p>
      <p class="cal-status">%(status)s</p>
      <div class="cal-cta">
        <a class="btn-solid" href="%(ics)s" download="srs-2027.ics" data-hover><span>Add to Calendar</span></a>
%(pdf)s        <a class="btn-lines" href="#cover" data-hover>See the Pages</a>
      </div>
      <p class="cal-fine">Add to Calendar downloads one small file (.ics) with the five rounds as all-day events. Apple Calendar, Google Calendar and Outlook open it.%(pdf_note)s</p>
    </div>
    <a class="cal-open-sheet" href="%(c_big)s" data-cal="0" aria-label="The cover: see the page large">
      <img src="%(c_small)s" srcset="%(c_small)s 1200w, %(c_big)s 2400w" sizes="(max-width:900px) 92vw, 52vw" width="%(w)d" height="%(h)d" alt="The cover of the SRS 2027 race calendar" fetchpriority="high">
    </a>
  </div>
  <nav class="cal-rail" aria-label="The calendar's pages"><ol>%(rail)s</ol></nav>
</header>

<section class="cal-sheets" id="pages" aria-label="The pages">
%(sheets)s
</section>
%(coming)s
<section class="kit-band cal-rounds" id="rounds" aria-labelledby="cal-rounds-t">
  <div class="kit-in">
    <div class="kit-head"><span class="kit-kicker">SRS 2027</span><h2 class="kit-title" id="cal-rounds-t">The Five Rounds</h2></div>
    <ol class="cal-r">%(rounds)s</ol>
    <div class="cal-cta">
      <a class="btn-solid" href="%(ics)s" download="srs-2027.ics" data-hover><span>Add to Calendar</span></a>
      <a class="btn-lines" href="%(srs)s" target="_blank" rel="noopener" data-hover>The SRS Events Page</a>
    </div>
    <p class="cal-fine">Dates as listed on sportsracingseries.org/events on %(read)s. St Jean Montclar is provisional there; check the SRS page before you book anything.</p>
  </div>
</section>

<section class="kit-band cal-foot" aria-labelledby="cal-foot-t">
  <div class="kit-in">
    <div class="kit-head"><span class="kit-kicker">The Photographs</span><h2 class="kit-title" id="cal-foot-t">All From SRS Tapalpa 2026</h2>
      <p class="kit-intro">Every page is a photograph by Aninder Singh / Paragliding Atlas from the Tapalpa round in Mexico. The whole gallery, task by task, is on the event page.</p></div>
    <div class="cal-cta"><a class="btn-lines" href="media-srs-tapalpa-2026.html" data-hover>See the Tapalpa Photos</a></div>
  </div>
</section>

<dialog class="cal-lb" id="cal-lb" aria-label="The calendar page, large">
  <div class="cal-lb-s"><img alt="" draggable="false"></div>
  <div class="cal-lb-bar">
    <span class="cal-lb-c" aria-live="polite"></span>
    <a class="cal-dl cal-lb-dl" href="#" download><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3v10M6.2 9.2 10 13l3.8-3.8M4 16.5h12"/></svg><span>Download</span></a>
    <button type="button" data-share class="cal-lb-sh"></button>
  </div>
  <button class="cal-lb-n cal-lb-p" type="button" aria-label="The page before"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg></button>
  <button class="cal-lb-n cal-lb-nx" type="button" aria-label="The next page"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg></button>
  <button class="cal-lb-x" type="button" aria-label="Close the page"></button>
</dialog>
</div>
''' % dict(pdf=pdf, pdf_note=pdf_note, what=what, n=len(have), c_small=c_small, c_big=c_big, status=status, ics=IMG + "srs-2027.ics", w=W, h=H, rail=rail,
           sheets=sheets, coming=coming, rounds=rounds, srs=SRS, read=READ)
    desc = ("The SRS 2027 race calendar by Paragliding Atlas: the five rounds of the Sports-Class Racing Series, month by "
            "month, on photographs from SRS Tapalpa 2026. Download each page, or add the rounds to your calendar.")
    out = M.shell("SRS 2027 Race Calendar", desc, NAME, "https://paraglidingatlas.com/assets/v4/" + IMG + "share.jpg",
                  "SRS 2027 Race Calendar", main)
    out = out.replace('"dateModified": "2026-11-03"', '"dateModified": "2026-11-23"', 1)
    out = out.replace("<!-- site-schema -->", '<link rel="stylesheet" href="v4-calendar.css?v=%s">\n<!-- site-schema -->'
                      % M.ver("v4-calendar.css"), 1)
    out = out.replace("</body>", '<script defer src="v4-calendar.js?v=%s"></script>\n</body>' % M.ver("v4-calendar.js"), 1)
    return out


if __name__ == "__main__":
    html = page()
    M.check(NAME, html)
    open(os.path.join(V4, NAME), "w", encoding="utf-8", newline="\n").write(html)
    print("wrote prototypes/v4/" + NAME, len(html))
