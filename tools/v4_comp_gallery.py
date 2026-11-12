#!/usr/bin/env python3
"""Comp gallery pages: one page per comp the owner covers, pilots browse by task, save the web copy free, buy the
original (chat 20, 4 Nov 2026).

Owner's answers (4 Nov): payment PayPal, EUR 1 a photo, one link per photo carrying its file name; the original is
downloaded on the site after paying (needs private storage and a payment check, not built: until then the buy
button is [to supply]); the free 2400 px copy is CC BY-NC 4.0. The design (D, E or F, docs/designers/gallery/) is
the owner's pick, still open on 4 Nov: render() below takes the chosen sample's markup.

The photos come from the media repo (paraglidingatlas-maker/media-2026), <folder>/photos.json, written by
tools/media_webcopies.py: [{"stem", "day" (T1, T2 ...), "w", "h", "shot"}] in the owner's file order. "shot" (EXIF
time) is never shown or sorted on (the Piedrahita originals read 31 Aug, after the comp). No Drive id or folder link
ever goes on a page: the originals are what the owner sells.

The pages are owned pages (tools/v4_build.py owned() takes media*.html), live through NEW_PAGES in tools/v2_site.py.
After running this, build in a clean worktree and copy the pages back before committing (the build writes its own
?v= hashes; see docs/v4-next-session.md, chat 19).

    python3 tools/v4_comp_gallery.py [tapalpa|piedrahita ...] [--repo /home/user/media-2026]
"""
import datetime
import html
import json
import re
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_media as M  # noqa: E402  (shell(), check(), TBD)

V4 = M.V4
E = html.escape
TBD = M.TBD
BASE = "https://paraglidingatlas-maker.github.io/media-2026/"
REPO = "/home/user/media-2026"
if "--repo" in sys.argv:
    REPO = sys.argv[sys.argv.index("--repo") + 1]

CREDIT = "Photo: Aninder Singh, Paragliding Atlas"
PRICE = "EUR 1"
# owner, 9 Nov 2026: instead of the EUR 1 original, the viewer's second button invites to Patreon (the paid
# originals wait for the owner's PayPal; the sheet stays in the code, unused)
PATREON = "https://www.patreon.com/15133612/join"     # the owner's join link (9 Nov)
# owner, 9 Nov: a link beside "Save, free" downloads the full-size original, through the owner's Cloudflare worker
# (tools/originals-worker.js: it fetches the file from the owner's Drive and hands it over under the site's name;
# the Drive folder IDs live only in Cloudflare). Empty: the link stays hidden until the worker is live.
ORIGINALS = ""

# Facts: only from the owner (Tapalpa: 116 pilots confirmed, 44 countries, airtribune.com/srs-2026-6/info, 8 Nov), docs/designers/gallery-brief.md and the task videos (tools/v4_media.py V); a task's
# date: Tapalpa assumes one task a day from 8 Nov (set "dates" when a day is cancelled); Piedrahita's are not known
COMPS = {
    "tapalpa": dict(page="media-srs-tapalpa-2026.html", folder="srs-tapalpa", title="Tapalpa 2026", tz="America/Mexico_City",
                    kicker="SRS Advance Edition &middot; Tapalpa, Mexico", span="8 to 14 Nov 2026",
                    facts=["Tasks 8 to 14 Nov 2026", "12 Nov cancelled (weather)", "116 pilots, 44 countries", "Photos by Aninder Singh"],
                    desc="SRS Advance Edition, Tapalpa, Mexico, 8 to 14 Nov 2026: every photo by task, free to save. "
                         "Photos by Aninder Singh, Paragliding Atlas.",
                    # owner, 10 Nov: the link preview's title is the comp's full name and the newest task with photos
                    share_title="SRS Advance Edition Tapalpa 2026",
                    tasks=["P"] + ["T%d" % i for i in range(1, 7)], window=("2026-11-08", "2026-11-14"), one_a_day=True,
                    # srs.live, 12 Nov 12:02: the day's 57 km task was cancelled (cirrus, 100% cloud cover). SRS numbers
                    # only flown tasks, so Task 5 moves to 13 Nov, Task 6 to 14 Nov, and a seventh task no longer fits.
                    dates={"P": "2026-11-07", "T5": "2026-11-13", "T6": "2026-11-14"},
                    stories={"T5": "12 Nov was cancelled for weather: SRS set a 57 km task north, then called it off under full cirrus cover. The next task, Task 5, is planned for 13 Nov."},
                    # owner, 9 Nov: the practice day's photos are by Paco Peciado; credit with a link to their Instagram
                    credits={"P": ("@paco_peciado", "https://www.instagram.com/paco_peciado/")},
                    event=("SRS Advance Edition, Tapalpa", "https://airtribune.com/srs-2026-6/info"),
                    # owner, 9 Nov: the people photos first, then the wings, by number; the cover and the share
                    # picture from these four (the file names stay the originals', the ones a buyer quotes)
                    first={"T1": [2, 3, 4, 5, 15, 16, 17, 19]}, lead="SRS_6_T1_62",
                    # owner, 10 Nov: the link picture from Task 2 photos 22, 19, 43, 2 (was Task 1: 62, 10, 20, 58)
                    share=["SRS_6_T4_54", "SRS_6_T4_67", "SRS_6_T4_94", "SRS_6_T4_100", "SRS_6_T4_150"],   # Task 4, owner 12 Nov
                    # owner, 9 Nov 2026: "Add this link to photos page if anyone wants to see video highlights too for
                    # the task day". A task's Daily Highlights film, one line a night once it is on YouTube: its id, its
                    # title and length as YouTube has them (vidIQ), its line from the video's own description, and a
                    # photo of the same task as its poster ("pos": where the band crops it, as CSS object-position).
                    # No line in the description: leave "line" out (the band then shows only the YouTube link).
                    films={"T1": dict(id="ZTxWnsHeUmE", title="Task 1 Highlights", len="4:48",
                                      line="A 59.1 km opener that started low and ended with a long glide into the wind.",
                                      poster="SRS_6_T1_55", pos="50% 30%"),
                           "T2": dict(id="MXt0RJgXNs4", title="Task 2 Highlights", len="4:36",
                                      line="A 41.3 km task raced under a storm clock, which eventually got stopped by rain.",
                                      poster="SRS_6_T2_44", pos="50% 40%"),
                           "T3": dict(id="bB1TaxIN8Oo", title="Task 3 Highlights", len="6:41",
                                      line="A 58.7 km race on a day that looked better than forecast, the field raced the ridge, crossed the lake bed into the wind and ran a cloud street home.",
                                      poster="SRS_6_T3_141", pos="60% 40%")}),
    "piedrahita": dict(page="media-srs-piedrahita-2026.html", folder="srs-piedrahita", title="Piedrahita 2026", tz="Europe/Madrid",
                       kicker="SRS BGD Edition &middot; Piedrahita, Ávila, Spain", span="22 to 29 Aug 2026",
                       facts=["22 to 29 Aug 2026", "FAI Category 2", "120 pilots, 54 countries", "Photos by Aninder Singh"],
                       desc="SRS BGD Edition, Piedrahita, Spain, 22 to 29 Aug 2026: all 325 photos by task, free to save, "
                            "and the task videos. Photos by Aninder Singh, Paragliding Atlas.",
                       # chat 22 (D's fix): Day 1 (registration) is its own day, not Task 1's; it has a film and no photos
                       tasks=["D1", "T1", "T2", "T3"], window=("2026-08-22", "2026-08-29"), dates={}, lead="SRS_5_T3_63",
                       event=("SRS BGD Edition, Piedrahita", "https://airtribune.com/srs-2026-5/info"),
                       # the event landing page (chat 22): on; its row in tools/v4_media.py SEASON; the opening's readout
                       landing=True, season="srs5", lead_alt="Dozens of wings in a deep blue sky over Piedrahita, Task 3",
                       read=["<b>22 to 29 Aug 2026</b>", "120 pilots, 54 countries", "FAI Category 2"],
                       stories={"T3": "The race from the air."},
                       # the films as Tapalpa's bands (chat 22, D's fix: a photo of the same task as the poster, not the
                       # designed thumbnail); title and length from tools/v4_media.py V; the lines from the films' own
                       # descriptions, as the page had them. Posters: designer F's pick, [to supply] the owner's own pick.
                       # Day 1 has no photos: a frame of its own film (YouTube's frame grab, maxres1).
                       films={"D1": dict(id="cuGs7Lk6Dt4", line="Registration, the pilots and the Peñas de Piedrahíta fiesta.",
                                         still="https://i.ytimg.com/vi/cuGs7Lk6Dt4/maxres1.jpg", pos="50% 40%"),
                              "T1": dict(id="uCEfssE40u8", line="59 km, humid air, a 2,100 m ceiling and a long leg into a westerly wind.",
                                         poster="SRS_5_T1_10", pos="55% 35%"),
                              "T2": dict(id="NXUEyPQ3V4E", line="75 km, and a flatland gamble that cut the course short.",
                                         poster="SRS_5_T2_99", pos="60% 40%")}),
    # films-only events (chat 22): no photos; "stops" are the event's days in order with their films (ids from
    # tools/v4_media.py V, the title, length, views and date out from there); an empty stop is a dashed slot
    "pwc": dict(page="media-pwc-pegalajar-2026.html", folder=None, title="Pegalajar 2026", full="PWC Super Final 2026",
                kicker="15th Paragliding World Cup Super Final &middot; Pegalajar, Spain", season="pwc", landing=True,
                desc="15th Paragliding World Cup Super Final, Pegalajar, Spain, May 2026: the five highlight films, by task. "
                     "Films by Aninder Singh, Paragliding Atlas.",
                read=["<b>May 2026</b>", "Comp dates " + TBD, "Pilots and countries " + TBD],
                stops=[("D1", ["FOuAWMeoxs4"]), ("T1", ["BRAX1XMU390"]), ("T2", ["7il6yV1vdIc"]), ("T3", []),
                       ("T4", ["op1-O01xkH4"]), ("T5", ["vPnIYYKcvEg"])],
                # posters: frames of the owner's own films (YouTube's frame grabs), not the designed thumbnails;
                # [to supply]: stills the owner picks from the footage
                posters={"FOuAWMeoxs4": "maxres3", "BRAX1XMU390": "maxres1", "7il6yV1vdIc": "maxres1",
                         "op1-O01xkH4": "maxres3", "vPnIYYKcvEg": "maxres3"},
                lead=("op1-O01xkH4", "maxres2"), lead_alt="A task drawn in red on a relief map, a frame from Task 4 Highlights",
                tp="len", word=("film", "films", "highlight films"), none="No film",
                none_line="No highlights film of %s in the archive. Whether it was flown, and its film:"),
    "bassano": dict(page="media-srs-bassano-2026.html", folder=None, title="Bassano 2026", full="SRS Bassano 2026",
                    kicker="SRS Skywalk Bassano Edition &middot; Monte&nbsp;Grappa, Italy", season="srs4", landing=True,
                    desc="SRS Skywalk Bassano Edition, Monte Grappa, Italy, May 2026: the five live broadcasts, by task. "
                         "Live commentary by Paragliding Atlas.",
                    read=["<b>May 2026</b>", "Comp dates " + TBD, "Pilots and countries " + TBD],
                    # the broadcasts begin at Task 2: Task 1 is a dashed slot, [to supply]
                    stops=[("T1", []), ("T2", ["ZL9B5eXip5o"]), ("T3", ["SZWQjcO_fWk"]), ("T4", ["x8sSBSBy4dI", "DA4nGop3i9g"]),
                           ("T5", ["PEyO6MXngUw"])],
                    # posters: YouTube's own thumbnails, until the owner picks frames ([to supply]); the opening: a frame of
                    # the final day's broadcast, its live overlay and all
                    posters={}, lead=("PEyO6MXngUw", "maxres1"), lead_alt="A frame from the live broadcast of the final day, Task 5",
                    tp="date", word=("broadcast", "broadcasts", "live broadcasts"), none="No broadcast",
                    none_line="No broadcast of %s in the archive. Whether it was flown, and its broadcast:"),
}


def photos(comp):
    """the comp's photos.json, from the local media repo, else from the published site; [] before the first night"""
    c = COMPS[comp]
    if not c.get("folder"):        # a films-only event
        return []
    p = os.path.join(REPO, c["folder"], "photos.json")
    try:
        return json.load(open(p))
    except OSError:
        pass
    try:
        with urllib.request.urlopen(BASE + c["folder"] + "/photos.json", timeout=20) as r:
            return json.load(r)
    except Exception:
        return []


def order(stem):
    m = re.search(r"_(\d+)(?:-(\d+))?$", stem)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else (10 ** 9, 0)


def share_image(comp):
    """the link preview (WhatsApp, Facebook ...): a 1200x630 JPEG of the owner's chosen photos, two by two, written
    beside the photos in the media repo as share.jpg (push the media repo for it to be served)"""
    c = COMPS[comp]
    if not c.get("share"):
        return None
    from PIL import Image, ImageOps
    folder = os.path.join(REPO, c["folder"])
    tiles = [os.path.join(folder, s + "-800.webp") for s in c["share"]]
    if not all(os.path.exists(t) for t in tiles):
        return None
    W, H, g = 1200, 630, 6
    out = Image.new("RGB", (W, H), (20, 21, 25))

    def fit(t, tw, th):
        im = Image.open(t).convert("RGB")
        r = max(tw / im.width, th / im.height)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        x, y = (im.width - tw) // 2, (im.height - th) // 2
        return im.crop((x, y, x + tw, y + th))
    if len(tiles) >= 5:      # owner, 10 Nov (Task 3): five photos, the first big on the left, four 2 by 2 on the right
        bw = (W - g) // 2
        out.paste(fit(tiles[0], bw, H), (0, 0))
        tw, th = (W - bw - 2 * g) // 2, (H - g) // 2
        for i, t in enumerate(tiles[1:5]):
            out.paste(fit(t, tw, th), (bw + g + (i % 2) * (tw + g), (i // 2) * (th + g)))
    else:
        tw, th = (W - g) // 2, (H - g) // 2
        for i, t in enumerate(tiles[:4]):
            out.paste(fit(t, tw, th), ((i % 2) * (tw + g), (i // 2) * (th + g)))
    # a subtle lift (owner, 9 Nov: "a bit more vibrant ... currently it looks a bit shaded out")
    from PIL import ImageEnhance
    out = ImageEnhance.Color(out).enhance(1.22)
    out = ImageEnhance.Contrast(out).enhance(1.07)
    out = ImageEnhance.Brightness(out).enhance(1.04)
    out.save(os.path.join(folder, "share.jpg"), quality=85, optimize=True, progressive=True)
    return BASE + c["folder"] + "/share.jpg"


def src(comp, stem, w):
    return "%s%s/%s-%d.webp" % (BASE, COMPS[comp]["folder"], stem, w)


def srcset(comp, stem, ws=(800, 1600, 2400)):
    return ", ".join("%s %dw" % (src(comp, stem, w), w) for w in ws)


def label(task):
    if task.startswith("D") and task[1:].isdigit():      # an event day that is not a task (Piedrahita's Day 1: registration)
        return "Day " + task[1:]
    return "Task " + task[1:] if task.startswith("T") else {"P": "Practice"}.get(task, task)


def days(comp):
    """[(task, label, [photo rows])] for every task of the comp, in order, empty tasks included (they say when)"""
    rows = photos(comp)
    by = {}
    for r in rows:
        if r.get("hold"):          # out of focus by the sharpness check: off the page until the owner says
            continue
        by.setdefault(r.get("day") or "", []).append(r)
    first = COMPS[comp].get("first", {})
    for k, lst in by.items():       # the owner's chosen first photos of a task, in their order, then the rest by number
        want = ["%s_%d" % (re.sub(r"_\d+(-\d+)?$", "", lst[0]["stem"]), n) for n in first.get(k, [])] if lst else []
        pos = {st: i for i, st in enumerate(want)}
        lst.sort(key=lambda r: (pos.get(r["stem"], len(pos)), order(r["stem"])))
    stray = [k for k in by if k not in COMPS[comp]["tasks"]]
    assert not stray, "photos with a day the comp does not have: %s (check --day-re)" % stray
    return [(t, label(t), by.get(t, [])) for t in COMPS[comp]["tasks"]]


PAYPAL_EMAIL = None   # [to supply]: the owner's PayPal address; then each photo's button pays EUR 1 with its file name


def pay_template():
    """PayPal's standard payment link, one per photo: {stem} becomes the photo's file name (its item name)"""
    if not PAYPAL_EMAIL:
        return ""
    return ("https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=%s&item_name={stem}&amount=1.00"
            "&currency_code=EUR&no_shipping=1" % urllib.request.quote(PAYPAL_EMAIL))


def colour(comp, stem):
    """the photo's average colour, for its cell while it loads (from the local 800 px copy; grey without one)"""
    try:
        from PIL import Image
        with Image.open(os.path.join(REPO, COMPS[comp]["folder"], stem + "-800.webp")) as im:
            r, g, b = im.convert("RGB").resize((1, 1), Image.BILINEAR).getpixel((0, 0))
        return "#%02x%02x%02x" % (r, g, b)
    except Exception:
        return "#5f6064"


def nice(date):
    """'2026-11-08' -> ('Sun 8 Nov', 'Sun 8 Nov 2026', '8 Nov')"""
    dt = datetime.date.fromisoformat(date)
    return dt.strftime("%a ") + str(dt.day) + dt.strftime(" %b"), dt.strftime("%a ") + str(dt.day) + dt.strftime(" %b %Y"), str(dt.day) + dt.strftime(" %b")


def task_dates(comp):
    c = COMPS[comp]
    if c.get("one_a_day"):          # one task a day from the first day, until the owner's files say otherwise
        d0 = datetime.date.fromisoformat(c["window"][0])
        out = {t: (d0 + datetime.timedelta(days=k)).isoformat() for k, t in enumerate(x for x in c["tasks"] if x.startswith("T"))}
        out.update(c["dates"])
        return out
    return dict(c["dates"])


GLIDER = ('<svg viewBox="0 0 22 14" aria-hidden="true"><path d="M1.5 5.2C6 1.4 16 1.4 20.5 5.2" stroke-width="1.6"/>'
          '<path d="M2.6 5 11 12.2 19.4 5" stroke-width=".6"/><circle cx="11" cy="12" r="1.5" fill="currentColor" stroke="none"/></svg>')


def nphotos(n):
    return "%d photo%s" % (n, "" if n == 1 else "s")


def cell(comp, r, task, k, n):
    stem, w, h = r["stem"], r["w"], r["h"]
    tw, th = (800, round(800 * h / w)) if w >= h else (round(800 * w / h), 800)
    return ('<figure class="gf-ph" id="%s" style="--r:%.4f;--c:%s"><a href="%s" data-stem="%s" data-W="%d" data-H="%d">'
            '<img src="%s" width="%d" height="%d" alt="%s, photo %d of %d" loading="lazy" decoding="async"></a>'
            '<figcaption>%s</figcaption></figure>'
            % (E(stem), w / h, colour(comp, stem), src(comp, stem, 2400), E(stem), w, h, src(comp, stem, 800), tw, th,
               E(label(task)), k + 1, n, E(stem)))


def sid(task):
    if task.startswith("D") and task[1:].isdigit():
        return "day-" + task[1:]
    return "task-" + task[1:] if task.startswith("T") else {"P": "practice"}.get(task, task.lower())


# ---------------------------------------------------------------- the films (owner, 9 Nov 2026) ----
# A task with a Daily Highlights film opens with a band: a photo of that task, the film's title, length and line, and a
# play button. JS opens the film in the theatre (v4-gallery.js films()); without JS the band is a link to YouTube.
YT = "https://www.youtube.com/watch?v="
CHANNEL = "https://www.youtube.com/@ParaglidingAtlas"          # as linked across the site
# owner, 10 Nov: the play button as the site's other YouTube buttons (podcast page rail, library popup): a dark
# see-through rounded rectangle, 82 by 56, YouTube's own optically centred triangle, red on hover
PLAY = '<svg class="gff-tri" viewBox="0 0 68 48" aria-hidden="true"><path d="M45 24 27 14 27 34Z"/></svg>'
RING = ('<svg class="gff-ring" viewBox="0 0 82 56" aria-hidden="true"><rect x=".75" y=".75" width="80.5" height="54.5" rx="13.25"/>'
        '<rect class="gff-done" x="1.5" y="1.5" width="79" height="53" rx="12.5" pathLength="100"/></svg>')
EXT = '<svg class="gff-ext" viewBox="0 0 12 12" aria-hidden="true"><path d="M4.2 2.6h5.2v5.2M9.2 2.8 2.6 9.4"/></svg>'


def said(ln):
    """'4:48' -> '4 min 48 s', for the play button's name"""
    m, s = (int(x) for x in ln.split(":"))
    return "%d min %d s" % (m, s) if s else "%d min" % m


def film_band(comp, task, f):
    if f.get("still"):         # a day with no photos (Piedrahita's Day 1): a frame of the film itself, 16:9 on a phone
        media = ('<div class="gff ev-still" id="film-%s" data-film="%s" style="--pos:%s">'
                 '<div class="gff-media"><img src="%s" sizes="(min-width:1300px) 1300px, 100vw" width="1280" height="720" '
                 'alt="" loading="lazy" decoding="async"></div>' % (sid(task), E(f["id"]), E(f.get("pos", "50% 50%")), E(f["still"])))
    else:
        r = next(x for x in photos(comp) if x["stem"] == f["poster"])
        media = ('<div class="gff" id="film-%(s)s" data-film="%(id)s" style="--pos:%(pos)s">'
                 '<div class="gff-media"><img src="%(src)s" srcset="%(srcset)s" sizes="(min-width:1300px) 1300px, 100vw" '
                 'width="1600" height="%(h)d" alt="" loading="lazy" decoding="async"></div>'
                 % dict(s=sid(task), id=E(f["id"]), pos=E(f.get("pos", "50% 50%")), src=src(comp, f["poster"], 1600),
                        srcset=srcset(comp, f["poster"]), h=round(1600 * r["h"] / r["w"])))
    return media + ('<div class="gff-head"><p class="gff-k"><span>Daily Highlights</span><span class="gff-len">%(len)s</span><span class="gff-at" hidden></span></p>'
            '<h3 class="gff-t">%(title)s</h3></div>'
            '<a class="gff-play" href="%(yt)s" target="_blank" rel="noopener" aria-label="Play the film, %(title)s, %(said)s">'
            '<span class="gff-btn"><span class="gff-btn-in">%(ring)s%(play)s</span></span>'
            '<span class="gff-cta" aria-hidden="true"><b data-cta>Play the film</b><small data-cta-s>%(len)s</small></span></a>'
            '<p class="gff-line"><span>%(line)s</span> <a class="gff-yt" href="%(yt)s" target="_blank" rel="noopener">Watch on YouTube%(ext)s</a></p>'
            '<i class="gff-bar" aria-hidden="true"><i></i></i></div>'
            % dict(len=E(f["len"]), title=E(f["title"]), line=E(f.get("line", "")), yt=E(YT + f["id"]), ext=EXT,
                   said=said(f["len"]), ring=RING, play=PLAY))


def filled(f):
    """a film entry, its title and length from the Media page's list (tools/v4_media.py V) where it does not give them"""
    v = M.V.get(f["id"])
    if v and ("title" not in f or "len" not in f):
        f = dict(f, title=f.get("title", v[1]), len=f.get("len", v[3]))
    return f


def film_cue(f):
    """the lead's cue to the newest film (it shows whichever task is open)"""
    return ('<p class="gf-film"><a href="%s" target="_blank" rel="noopener" data-film-cue="%s"><span class="gf-film-i" aria-hidden="true">%s</span>'
            '<span class="gf-film-t">Watch %s</span><span class="gf-film-l">%s</span></a></p>'
            % (E(YT + f["id"]), E(f["id"]), PLAY, E(f["title"]), E(f["len"])))


FILM_DIALOG = """
<dialog class="gffv" id="gffv" aria-labelledby="gffv-t">
  <div class="gffv-bg" aria-hidden="true"></div>
  <div class="gffv-amb" aria-hidden="true"><img alt="" decoding="async"></div>
  <div class="gffv-stage">
    <div class="gffv-box">
      <div class="gffv-top">
        <div class="gffv-meta"><p class="gffv-k"><span>Daily Highlights</span><span class="gffv-len"></span></p><p class="gffv-t" id="gffv-t"></p></div>
        <a class="gffv-yt" href="%(channel)s" target="_blank" rel="noopener">YouTube%(ext)s</a>
        <button class="gffv-x" type="button" aria-label="Close the film"></button>
      </div>
      <div class="gffv-frame" tabindex="-1" aria-label="The film">
        <div class="gffv-pic"><img alt="" decoding="async"></div>
        <div class="gffv-player"></div>
        <span class="gffv-load" aria-hidden="true"><i></i></span>
        <div class="gffv-end" hidden>
          <p class="gffv-end-k"></p>
          <p class="gffv-end-t">Find Yourself In The Photos</p>
          <div class="gffv-end-a"><a class="btn-solid gffv-photos" href="#"><span>See the photos</span></a><button class="btn-lines gffv-again" type="button">Watch again</button></div>
          <p class="gffv-end-s"><a href="%(channel)s?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></p>
        </div>
      </div>
      <div class="gffv-foot">
        <p class="gffv-line"></p>
        <p class="gffv-resume" hidden><span></span> <button class="gffv-over" type="button">Start over</button></p>
        <p class="gffv-keys">Space plays and pauses &middot; F full screen &middot; Esc closes</p>
      </div>
    </div>
  </div>
</dialog>
""" % dict(channel=CHANNEL, ext=EXT)


def render(comp):
    c = COMPS[comp]
    ds, dates = days(comp), task_dates(comp)
    ds = [d for d in ds if d[2] or d[0] != "P"]       # the practice day shows only once it has photos
    N = len(ds)
    latest = max([i for i, (_, _, rows) in enumerate(ds) if rows] or [-1])
    # the lead: the comp's own chosen photo, else the first photo of the newest task, else a labelled stand-in
    lead_comp, lead, note = comp, c.get("lead"), ""
    if not lead and latest >= 0:
        lead = ds[latest][2][0]["stem"]
    if not lead:
        lead_comp, lead = "piedrahita", "SRS_5_T3_63"
        note = '<p class="gf-cred">Photo: SRS Piedrahita 2026. Tapalpa&#x27;s own photos from Task 1.</p>'
    lr = next(r for r in photos(lead_comp) if r["stem"] == lead)
    facts = "".join("<span>%s</span>" % f for f in c["facts"])
    films, fdata, cue = c.get("films", {}), {}, ""
    tps, secs, info = [], [], []
    for i, (task, lab, rows) in enumerate(ds):
        date = dates.get(task, "")
        short, full, dm = nice(date) if date else ("", "", "")
        n = len(rows)
        info.append({"i": i, "task": int(task[1:]) if task[0] == "T" and task[1:].isdigit() else 0, "name": lab, "date": date, "label": short, "n": n})
        cr = c.get("credits", {}).get(task)
        if cr:
            info[-1]["cred"] = cr[0]
        fm = filled(films[task]) if task in films else None
        filmday = bool(c.get("landing") and fm and not rows)     # a day with its film and no photos (state "film", v4-event.js)
        if fm:
            info[-1]["film"] = fm["id"]
            m, s = (int(x) for x in fm["len"].split(":"))
            fdata[fm["id"]] = {"title": fm["title"], "len": fm["len"], "secs": m * 60 + s, "line": fm.get("line", ""), "day": i,
                               "band": "film-" + sid(task), "amb": fm["still"] if fm.get("still") else src(comp, fm["poster"], 800)}
            cue = film_cue(fm)          # the newest film of the comp goes on the lead
        if filmday:
            tps.append('<li class="gf-tp" data-i="%d" data-film-only><a href="#%s"><i class="gf-dot" aria-hidden="true"></i><b>%s</b>'
                       '<span class="gf-tp-d">%s</span><span class="gf-tp-s ev-tp-s">%s</span></a></li>'
                       % (i, sid(task), lab, dm or "Film", "Film" if dm else ""))
        else:
            tps.append('<li class="gf-tp" data-i="%d"><a href="#%s"><i class="gf-dot" aria-hidden="true"></i><b>%s</b>'
                     '<span class="gf-tp-d">%s</span><span class="gf-tp-s"><span data-s="photos">%s%s</span>'
                     '<span data-s="today">Photos tonight</span><span data-s="coming">Photos coming</span>'
                     '<span data-s="soon">To come</span></span></a></li>'
                     % (i, sid(task), lab, dm or nphotos(n), nphotos(n) if dm else "",
                        '<span class="gf-tp-f"> + film</span>' if fm else ""))
        story = c.get("stories", {}).get(task)
        vids = [v for v in c.get("videos", {}).get(task, [])]
        vb = ""
        if vids:
            vb = '<div class="gf-vids">%s</div>' % "".join(
                '<figure>%s<figcaption>%s &middot; %s</figcaption></figure>' % (M.frame(v), E(M.V[v][1]), M.V[v][3]) for v in vids)
        when = ("<span>%s</span>" % full) if full else ""
        if filmday:
            head = ('<header class="gf-dh"><h2 id="gf-h-%d">%s</h2><p class="gf-dh-r">%s<span class="ev-dh-n">1 film, no photos this day</span></p>%s</header>'
                    % (i + 1, lab, when, '<p class="gf-story">%s</p>' % E(story) if story else ""))
        else:
            head = ('<header class="gf-dh"><h2 id="gf-h-%d">%s</h2><p class="gf-dh-r">%s<span class="gf-dh-n" data-s="photos">%s'
                '<span class="gf-dh-o">, in the order shot</span></span><span class="gf-dh-n" data-s="today">Flying today</span>'
                '<span class="gf-dh-n" data-s="coming">Photos coming</span><span class="gf-dh-n" data-s="soon">To come</span></p>%s%s</header>'
                % (i + 1, lab, when, nphotos(n), '<p class="gf-story">%s</p>' % E(story) if story else "",
                   '<p class="gf-dh-cred">Photos by <a href="%s" target="_blank" rel="noopener">%s</a></p>' % (E(cr[1]), E(cr[0])) if cr else ""))
        if filmday:
            body = ""
        elif rows:
            body = '<div class="gf-grid" aria-label="Photos of %s, in the order shot">%s</div>' % (lab, "".join(cell(comp, r, task, k, n) for k, r in enumerate(rows)))
        else:
            on = full or lab
            body = ('<div class="gf-wait"><div data-s="today"><p class="gf-wait-t"><i class="gf-tally" aria-hidden="true"></i>Photos tonight</p>'
                    '<p>%s flies today%s. The photos land here this evening.</p></div>'
                    '<div data-s="coming"><p class="gf-wait-t">Photos coming</p><p>%s%s. Its photos are on their way.</p></div>'
                    '<div data-s="soon"><p class="gf-wait-t">%s</p><p>%s. Photos land here on the evening of the task.</p></div>'
                    '<a class="gf-latest" href="#" data-latest hidden>See the latest photos <i aria-hidden="true">&rarr;</i></a></div>'
                    % (lab, ", " + short if short else "", lab, " was on " + short if short else " has flown", E(on), lab))
        nav = []
        if i > 0:
            nav.append('<a class="gf-df-p" href="#%s" data-go="%d"><i aria-hidden="true">&larr;</i> %s</a>' % (sid(ds[i - 1][0]), i - 1, ds[i - 1][1]))
        if i < N - 1:
            nd = dates.get(ds[i + 1][0], "")
            nav.append('<a class="gf-df-n" href="#%s" data-go="%d">Next leg: %s%s <i aria-hidden="true">&rarr;</i></a>'
                       % (sid(ds[i + 1][0]), i + 1, ds[i + 1][1], ", " + nice(nd)[0] if nd else ""))
        fb = film_band(comp, task, fm) if fm else ""
        secs.append('<section class="gf-day" id="%s" data-i="%d" data-date="%s"%s aria-labelledby="gf-h-%d">%s%s%s%s%s</section>'
                    % (sid(task), i, date, ' data-film-only data-state="film"' if filmday else "", i + 1, head, fb, vb, body, '<nav class="gf-df" aria-label="Other tasks">%s</nav>' % "".join(nav) if nav else ""))
    data = {"base": BASE + c["folder"] + "/", "tz": c["tz"], "days": info, "pay": pay_template()}
    if fdata:
        data["films"] = fdata
    if ORIGINALS:
        data["orig"] = ORIGINALS.rstrip("/") + "/"
    terms = ('Free web copy, <span class="gfv-px"></span>, under <a href="https://creativecommons.org/licenses/by-nc/4.0/" '
             'target="_blank" rel="license noopener">CC BY-NC 4.0</a>: share it with the credit &ldquo;<span class="gfv-cr">%s</span>&rdquo;, not for '
             'commercial use.' % E(CREDIT.replace("Photo: ", "Photo: ")))
    w, h = lr["w"], lr["h"]
    out = """
<header class="gf-lead">
  <div class="gf-lead-media"><img src="%(lead)s" srcset="%(leads)s" sizes="100vw" width="1600" height="%(lh)d" alt="%(lalt)s" fetchpriority="high"></div>
  <div class="gf-lead-copy">
    <a class="gf-back" href="media.html"><i aria-hidden="true">&larr;</i> Media</a>
    <p class="gf-kicker">%(kicker)s</p>
    <h1 class="gf-name">%(name)s <span>%(year)s</span></h1>
    <p class="gf-facts">%(facts)s</p>
    <p class="gf-event">Official event: <a href="%(evu)s" target="_blank" rel="noopener">%(evn)s</a></p>
    %(cue)s%(note)s
  </div>
</header>

<div class="gf-body">
<nav class="gf-line" aria-label="%(linelabel)s">
  <div class="gf-line-in">
    <span class="gf-track" aria-hidden="true"><i class="gf-flown"></i></span>
    <span class="gf-glc" aria-hidden="true"><span class="gf-glw"><i class="gf-glider">%(glider)s</i></span></span>
    <ol class="gf-tps">%(tps)s</ol>
  </div>
</nav>

<div class="gf-days">
<p class="gf-mode"><button type="button" data-m="all" aria-pressed="false">Every task on one page</button><button type="button" data-m="one" aria-pressed="true">One task at a time</button></p>
%(secs)s
</div>
</div>

%(cta)s

<dialog class="gfv" id="gfv" aria-label="The photo, enlarged">
  <div class="gfv-top">
    <button class="gfv-nav gfv-prev" type="button" aria-label="Previous photo"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg></button>
    <span class="gfv-pos" aria-live="polite"></span>
    <button class="gfv-nav gfv-next" type="button" aria-label="Next photo"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg></button>
    <button class="gfv-x" type="button" aria-label="Close the photo"></button>
  </div>
  <div class="gfv-stage"><img alt="" draggable="false"></div>
  <div class="gfv-foot">
    <div class="gfv-meta"><b class="gfv-name"></b><span class="gfv-where"></span></div>
    <div class="gfv-acts">
      <a class="btn-lines gfv-save" href="#" download data-hover>Save, free</a>
      <a class="gfv-orig" href="#" rel="nofollow" hidden>Full-size original</a>
      <a class="btn-solid gfv-patreon" href="%(patreon)s" target="_blank" rel="noopener" data-hover><span><small>Like what you see?</small>Join me on Patreon</span></a>
    </div>
    <p class="gfv-terms">%(terms)s</p>
  </div>
  <div class="gfv-sheet" role="region" aria-labelledby="gfv-sheet-t">
    <div class="gfv-sheet-in">
      <p class="gfv-sheet-k">The original</p>
      <h3 id="gfv-sheet-t" class="gfv-sheet-t" tabindex="-1">Full size, %(price)s</h3>
      <div class="gfv-ref"><span>Your photo</span><b class="gfv-ref-n"></b><button class="gfv-copy" type="button">Copy name</button></div>
      <p class="gfv-sheet-p">The camera&#x27;s full-size file, paid with PayPal. Licence of the original: %(tbd)s.</p>
      <div class="gfv-sheet-a">
        <a class="btn-solid gfv-pay" href="#" data-hover><span>Pay %(price)s</span></a>
        <button class="btn-lines gfv-back" type="button" data-hover>Back to the photo</button>
      </div>
      <p class="gfv-paynote">%(paynote)s</p>
    </div>
  </div>
</dialog>
%(filmdialog)s
<script type="application/json" id="gf-data">%(data)s</script>
""" % dict(lead=src(lead_comp, lead, 1600), leads=srcset(lead_comp, lead), lh=round(1600 * h / w),
           cue=cue, filmdialog=FILM_DIALOG if fdata else "",
           lalt=E("A photo from %s" % ("SRS Piedrahita 2026" if lead_comp != comp else c["title"])),
           kicker=c["kicker"], evn=E(c["event"][0]), evu=E(c["event"][1]), name=E(c["title"].rsplit(" ", 1)[0]), year=c["title"].rsplit(" ", 1)[1], facts=facts,
           note=note, linelabel=E("%s, %s" % (c["title"], "tasks " + c["span"])), glider=GLIDER, tps="".join(tps),
           secs="\n".join(secs), cta=M.cta("Coverage Like This For <span class=\"v4-nw\">Your Event</span>", "Coverage For Your Comp",
                                         "Every task day: stills like these, and Daily Highlights, a video each task day with social clips and a results newsletter."),
           price=PRICE, terms=terms, tbd=TBD, patreon=PATREON,
           paynote=("The payment carries the photo&#x27;s name. The download after paying: %s" % TBD) if PAYPAL_EMAIL
           else "Payment link: %s. It will carry the photo&#x27;s name." % TBD,
           data=json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    return landing(comp, out, ds) if c.get("landing") else out


# ---------------------------------------------------------------- the event landing pages (chat 22, designer F) ----
# "The Season Opens Here": the event's own page IS its gallery page (same URL), opening on the place, its facts and
# counts; at the opening's foot the 2026 season line, this event lit orange, fans out into the event's own task line;
# a previous / next event row on a phone; the whole season at the foot, each event a row with its picture. Switched on
# per comp by COMPS[c]["landing"] (absent: off, the plain gallery, as Tapalpa until its comp is over). A comp with no
# photos (films only) lists its "stops" instead of tasks: each task's films as chapters, a missing film as a dashed slot.
# The season comes from tools/v4_media.py season() (SEASON and UPCOMING), never a copy. Shared code: v4-event.css/js.
ARROW = '<i aria-hidden="true">&rarr;</i>'
NE = '<i aria-hidden="true">&nearr;</i>'


def season_strip(cur, n):
    """the 2026 season line under the opening, this event lit, and the fan that opens it into the task line"""
    S = M.season()
    i = [e["key"] for e in S].index(cur)
    ev = S[i]
    tot = (M.LINE[1] - M.LINE[0]).days

    def x(e):
        return M.at(e["first"]), M.at(e["last"]) + 1 / tot
    xa, xb = x(ev)
    bars, names = [], []
    for e in S:
        a, b = x(e)
        lit = e["key"] == cur
        when = ' data-first="%s" data-last="%s"' % (e["first"].isoformat(), e["last"].isoformat())
        bars.append('<i class="ev-bar%s"%s style="--x:%.4f;--w:%.4f"></i>' % (" is-lit" if lit else "", when, a, b - a))
        lab = '<b>%s</b><small>%s</small>' % (E(e["nick"]), e["tag"])
        if lit:
            names.append('<span class="ev-nm is-lit" style="--x:%.4f" aria-current="page">%s</span>' % (a, lab))
        else:
            names.append('<a class="ev-nm"%s style="--x:%.4f" href="%s">%s</a>' % (when, a, E(e["page"]), lab))
    prev = S[i - 1] if i > 0 else None
    nxt = S[i + 1] if i + 1 < len(S) else None
    pn = ('<a class="ev-pn-p" href="%s"><i aria-hidden="true">&larr;</i> <span><b>%s</b> %s</span></a>' % (E(prev["page"]), E(prev["name"]), prev["tag"])
          if prev else '<span class="ev-pn-p is-first"><span>The season starts here</span></span>')
    pn += ('<a class="ev-pn-n" href="%s"><span><b>%s</b> %s</span> %s</a>' % (E(nxt["page"]), E(nxt["name"]), nxt["tag"], ARROW)
           if nxt else '<span class="ev-pn-n is-last"><span>The latest event</span></span>')
    L = 50.0 / n                       # the task line's track runs from the first column's middle to the last's
    fan = ('<svg class="ev-fan" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
           '<defs><linearGradient id="ev-beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7517" stop-opacity=".22"/>'
           '<stop offset="1" stop-color="#ff7517" stop-opacity="0"/></linearGradient></defs>'
           '<path d="M%.3f 0 L%.3f 0 L%.3f 100 L%.3f 100 Z" fill="url(#ev-beam)"/>'
           '<line x1="%.3f" y1="0" x2="%.3f" y2="100"/><line x1="%.3f" y1="0" x2="%.3f" y2="100"/></svg>'
           % (xa * 100, xb * 100, 100 - L, L, xa * 100, L, xb * 100, 100 - L))
    return ('<nav class="ev-season" aria-label="The 2026 season: %s is event %d of %d">\n'
            '  <div class="ev-season-in">\n    <p class="ev-pn">%s</p>\n'
            '    <p class="ev-sh"><a href="media.html#reach">The 2026 season</a><span>%d of %d</span></p>\n'
            '    <div class="ev-strip"><span class="ev-names">%s</span><span class="ev-rule" aria-hidden="true">%s</span></div>\n'
            '    %s\n  </div>\n</nav>\n'
            % (E(ev["name"]), i + 1, len(S), pn, i + 1, len(S), "".join(names), "".join(bars), fan))


def season_foot(cur):
    """the whole season at the page's foot: each event a row with its picture, dates on its own rule, one link"""
    S = M.season()
    tot = (M.LINE[1] - M.LINE[0]).days
    rows = []
    for e in S:
        here = e["key"] == cur
        a, b = M.at(e["first"]), M.at(e["last"]) + 1 / tot
        go = ('<span class="ev-row-go is-here">You are here</span>' if here else
              '<a class="ev-row-go" href="%s" aria-label="%s: %s">%s %s</a>' % (E(e["page"]), E(e["name"]), e["go"].lower(), e["go"], ARROW))
        rows.append('<li class="ev-row%s" data-first="%s" data-last="%s">'
                    '<span class="ev-row-pic" aria-hidden="true"><img src="%s" alt="" width="320" height="180" loading="lazy" decoding="async"></span>'
                    '<span class="ev-row-d"><span class="ev-now"><i class="ev-tally" aria-hidden="true"></i>On air now &middot; </span>%s</span>'
                    '<span class="ev-row-n"><b>%s</b><small>%s &middot; %s</small></span><span class="ev-row-m">%s</span>'
                    '<span class="ev-row-bar" aria-hidden="true"><i style="--x:%.4f;--w:%.4f"></i></span>%s</li>'
                    % (" is-here" if here else "", e["first"].isoformat(), e["last"].isoformat(), E(e["pic"]), e["when"],
                       E(e["name"]), e["edition"], e["where"], e["made"], a, b - a, go))
    up = {u["key"] for u in M.UPCOMING}          # a comp's own dates: UPCOMING's, or a SEASON row's "span"
    own = [e["nick"] for e in S if e["key"] in up or any(x["comp"] == e["key"] and "span" in x for x in M.SEASON)]
    other = [e["nick"] for e in S if e["nick"] not in own]
    note = ('<p class="ev-rows-f">Dates on the line: %s the comps&#x27; own; %s the days the films and broadcasts came out '
            '(the comps&#x27; own dates %s).</p>' % (" and ".join(own), " and ".join(other), TBD)) if other else ""
    return ('<section class="ev-foot" aria-labelledby="ev-foot-t"><div class="ev-foot-in">'
            '<h2 id="ev-foot-t" class="ev-foot-h">The 2026 Season</h2>'
            '<ol class="ev-rows">%s</ol>%s<p class="ev-rows-m"><a href="media.html#reach">The season on the Media page %s</a></p></div></section>\n'
            % ("".join(rows), note, ARROW))


def opening(comp, have, media, film=False):
    """the event's opening: the picture, the place in giant type, its readout and what the page holds"""
    c = COMPS[comp]
    ev = c.get("event")
    off = ('<a class="ev-off" href="%s" target="_blank" rel="noopener">Official event %s</a>' % (E(ev[1]), NE) if ev
           else '<span class="ev-off">Official event %s</span>' % TBD)
    return ('<header class="gf-lead ev-open%s">\n  <div class="gf-lead-media">%s</div>\n  <div class="gf-lead-copy ev-copy">\n'
            '    <a class="gf-back" href="media.html"><i aria-hidden="true">&larr;</i> Media</a>\n'
            '    <p class="gf-kicker">%s</p>\n    <h1 class="gf-name ev-name">%s <span>%s</span></h1>\n'
            '    <p class="ev-read">%s</p>\n    <p class="ev-have">%s%s</p>\n  </div>\n</header>\n'
            % (" ev-open--film" if film else "", media, c["kicker"], E(c["title"].rsplit(" ", 1)[0]), c["title"].rsplit(" ", 1)[1],
               "".join("<span>%s</span>" % r for r in c["read"]), have, off))


def landing(comp, out, ds):
    """the gallery page made the event's landing page: the opening, the season strip over the task line, the foot"""
    c = COMPS[comp]
    nph = sum(len(r) for _, _, r in ds)
    with_ph = [t for t, _, r in ds if r]
    films = [t for t, _, _ in ds if t in c.get("films", {})]
    have = ""
    if nph:
        have += '<a href="#%s"><b>%s</b> photos</a>' % (sid(with_ph[-1]), M.n(nph))
    if films:
        have += '<a href="#film-%s"><b>%d</b> film%s</a>' % (sid(films[0]), len(films), "" if len(films) == 1 else "s")
    lead = c["lead"]
    lr = next(r for r in photos(comp) if r["stem"] == lead)
    media = ('<img src="%s" srcset="%s" sizes="100vw" width="1600" height="%d" alt="%s" fetchpriority="high">'
             % (src(comp, lead, 1600), srcset(comp, lead), round(1600 * lr["h"] / lr["w"]), E(c.get("lead_alt", "A photo from " + c["title"]))))
    out, k = re.subn(r'<header class="gf-lead">.*?</header>\n', lambda m: opening(comp, have, media), out, count=1, flags=re.S)
    assert k == 1
    a = '<div class="gf-body">\n<nav class="gf-line"'
    assert out.count(a) == 1
    out = out.replace(a, '<div class="gf-body">\n' + season_strip(c["season"], len(ds)) + '<nav class="gf-line"', 1)
    b = '<section class="cta-band" id="book">'
    assert out.count(b) == 1
    return out.replace(b, season_foot(c["season"]) + b, 1)


def chapter(comp, v, eager):
    """one film of a films-only event, as a chapter: its frame (plays in place, 16:9 at every width), title and readout"""
    c = COMPS[comp]
    k, t, views, ln, out, ep = M.V[v]
    live = t.startswith("Live: ")
    name = t[6:] if live else t
    q = c.get("posters", {}).get(v, "maxresdefault")
    badge = ""        # the broadcast's own frame carries the stream's LIVE overlay; the kicker says "Live broadcast"
    acts = ('<a href="episodes/%s.html">Read the episode %s</a>' % (E(ep), ARROW) if ep else "") + \
           '<a href="%s%s" target="_blank" rel="noopener">Watch on YouTube %s</a>' % (YT, E(v), NE)
    return ('<article class="ev-ch"><div class="md-frame" data-vid="%(v)s"><img src="%(img)s" alt="" width="1280" height="720"%(lazy)s decoding="async">'
            '<a class="md-play" href="%(yt)s" target="_blank" rel="noopener" aria-label="Play %(t)s, %(ev)s">%(play)s</a>%(badge)s</div>'
            '<div class="ev-ch-f"><p class="ev-ch-k">%(kind)s</p><h3 class="ev-ch-t">%(name)s</h3>'
            '<p class="ev-ch-m"><span>%(ln)s</span><span>%(views)s views</span><span>%(when)s %(out)s</span></p>'
            '<p class="ev-ch-a">%(acts)s</p></div></article>'
            % dict(v=E(v), img=M.thumb(v, q), lazy="" if eager else ' loading="lazy"', yt=E(YT + v), t=E(t), ev=E(c["title"]),
                   play=M.PLAY, badge=badge, kind="Live broadcast" if live else "Highlights film", name=E(name), ln=ln,
                   views=M.n(views), when="Live on" if live else "Out", out=out, acts=acts))


def render_films(comp):
    """a films-only event (no photos): the same opening, season and line; each stop its films as chapters"""
    c = COMPS[comp]
    stops = c["stops"]
    N = len(stops)
    ids = [v for _, vs in stops for v in vs]
    top = max(ids, key=lambda v: M.V[v][2])            # the most watched film's stop opens first
    start = next(i for i, (_, vs) in enumerate(stops) if top in vs)
    tps, secs = [], []
    for i, (task, vs) in enumerate(stops):
        lab, s = label(task), sid(task)
        if vs:
            outs = [M.V[v][4].rsplit(" ", 1)[0] for v in vs]
            dd = outs[0] if len(set(outs)) == 1 else "%s, %s" % (outs[0].split()[0], outs[-1])
            lens = M.V[vs[0]][3] if len(vs) == 1 else "%d parts" % len(vs)
            d1, d2 = (lens, "Out " + dd) if c.get("tp") == "len" else (dd, lens)
            tps.append('<li class="gf-tp%s" data-i="%d" data-state="film"><a href="#%s"%s><i class="gf-dot" aria-hidden="true"></i><b>%s</b>'
                       '<span class="gf-tp-d">%s</span><span class="gf-tp-s">%s</span></a></li>'
                       % (" is-open" if i == start else "", i, s, ' aria-current="true"' if i == start else "", lab, d1, d2))
            n = len(vs)
            head = ('<p class="gf-dh-r"><span>%s</span></p>' % ("%d %s" % (n, c["word"][1]) if n > 1 else "1 " + c["word"][0]))
            body = "".join(chapter(comp, v, i == start) for v in vs)
            st = "film"
        else:
            tps.append('<li class="gf-tp" data-i="%d" data-state="none"><a href="#%s"><i class="gf-dot" aria-hidden="true"></i><b>%s</b>'
                       '<span class="gf-tp-d">%s</span><span class="gf-tp-s">&nbsp;</span></a></li>' % (i, s, lab, c["none"]))
            head = '<p class="gf-dh-r"><span>%s</span></p>' % c["none"]
            body = ('<div class="ev-none"><p class="ev-none-t">%s, %s</p><p>%s %s</p></div>'
                    % (lab, c["none"].lower(), c["none_line"] % lab, TBD))
            st = "none"
        nav = []
        if i > 0:
            nav.append('<a class="gf-df-p" href="#%s" data-go="%d"><i aria-hidden="true">&larr;</i> %s</a>' % (sid(stops[i - 1][0]), i - 1, label(stops[i - 1][0])))
        if i + 1 < N:
            nav.append('<a class="gf-df-n" href="#%s" data-go="%d">Next leg: %s %s</a>' % (sid(stops[i + 1][0]), i + 1, label(stops[i + 1][0]), ARROW))
        secs.append('<section class="gf-day ev-stop%s" id="%s" data-i="%d" data-state="%s" aria-labelledby="gf-h-%d"><header class="gf-dh">'
                    '<h2 id="gf-h-%d">%s</h2>%s</header>%s<nav class="gf-df" aria-label="Other tasks">%s</nav></section>'
                    % (" is-open" if i == start else "", s, i, st, i + 1, i + 1, lab, head, body, "".join(nav)))
    views = sum(M.V[v][2] for v in ids)
    have = ('<a href="#%s"><b>%d</b> %s</a><span><b>%s</b> views on YouTube, %s</span>'
            % (sid(stops[start][0]), len(ids), c["word"][2], M.n(views), M.COUNTED))
    lv, lq = c["lead"]
    media = '<img src="%s" width="1280" height="720" alt="%s" fetchpriority="high">' % (M.thumb(lv, lq), E(c["lead_alt"]))
    line = ('<nav class="gf-line ev-fline" aria-label="%s" style="--flown:%d;--open:%d">\n  <div class="gf-line-in">\n'
            '    <span class="gf-track" aria-hidden="true"><i class="gf-flown"></i></span>\n'
            '    <span class="gf-glc" aria-hidden="true"><span class="gf-glw"><i class="gf-glider">%s</i></span></span>\n'
            '    <ol class="gf-tps">%s</ol>\n  </div>\n</nav>\n'
            % (E("%s, %s by task" % (c["title"], c["word"][1])), N - 1, start, GLIDER, "".join(tps)))
    return ('\n%s\n<div class="gf-body">\n%s%s\n<div class="gf-days">\n%s\n</div>\n</div>\n\n%s%s'
            % (opening(comp, have, media, film=True), season_strip(c["season"], N), line, "\n".join(secs), season_foot(c["season"]),
               M.cta("Coverage Like This For <span class=\"v4-nw\">Your Event</span>", "Coverage For Your Comp",
                     "Every task day: Daily Highlights, a video each task day with social clips and a results newsletter.")))


def page_films(comp):
    c = COMPS[comp]
    lv, lq = c["lead"]
    out = M.shell(c["full"], c["desc"], c["page"], M.thumb(lv, lq), c["full"], render_films(comp))
    M.check(c["page"], out)
    out = out.replace('<main id="v4-main">', '<main id="v4-main" class="gf ev ev-films" data-ev="%s" style="--n:%d">' % (c["season"], len(c["stops"])), 1)
    out = out.replace("<!-- site-schema -->", '<link rel="stylesheet" href="v4-gallery.css?v=%s">\n<link rel="stylesheet" href="v4-event.css?v=%s">\n<!-- site-schema -->'
                      % (M.ver("v4-gallery.css"), M.ver("v4-event.css")), 1)
    out = out.replace("</body>", '<script defer src="v4-event.js?v=%s"></script>\n</body>' % M.ver("v4-event.js"), 1)
    return out


def page(comp):
    c = COMPS[comp]
    if c.get("stops"):
        return page_films(comp)
    rows = photos(comp)
    og = share_image(comp) or (src(comp, rows[0]["stem"], 1600) if rows else "https://paraglidingatlas.com/assets/images/hero.jpg")
    out = M.shell(c["title"], c["desc"], c["page"], og, c["title"], render(comp))
    M.check(c["page"], out)
    if c.get("share_title"):
        new = [lab for t, lab, rs in days(comp) if rs and t.startswith("T")]
        st = c["share_title"] + (" · " + new[-1] if new else "")
        out = out.replace('<meta property="og:title" content="%s">' % E(c["title"]), '<meta property="og:title" content="%s">' % E(st), 1)
    k = len([d for d in days(comp) if d[2] or d[0] != "P"])
    out = out.replace('<main id="v4-main">', '<main id="v4-main" class="gf" style="--n:%d">' % k, 1)
    out = out.replace("<!-- site-schema -->", '<link rel="stylesheet" href="v4-gallery.css?v=%s">\n<!-- site-schema -->' % M.ver("v4-gallery.css"), 1)
    out = out.replace("</body>", '<script defer src="v4-gallery.js?v=%s"></script>\n</body>' % M.ver("v4-gallery.js"), 1)
    if c.get("landing"):         # the event landing page: its own styles and script after the gallery's
        out = out.replace('<main id="v4-main" class="gf"', '<main id="v4-main" class="gf ev" data-ev="%s"' % c["season"], 1)
        out = out.replace('<!-- site-schema -->', '<link rel="stylesheet" href="v4-event.css?v=%s">\n<!-- site-schema -->' % M.ver("v4-event.css"), 1)
        out = out.replace('</body>', '<script defer src="v4-event.js?v=%s"></script>\n</body>' % M.ver("v4-event.js"), 1)
    body = out.split('<main id="v4-main" class="gf')[1].split("</main>")[0]
    assert "drive.google" not in body, "a Drive link on " + c["page"]
    return out


if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if a in COMPS] or list(COMPS)
    for comp in which:
        s = page(comp)
        open(os.path.join(V4, COMPS[comp]["page"]), "w").write(s)
        print("wrote prototypes/v4/%s (%s)" % (COMPS[comp]["page"], "%d photos" % len(photos(comp)) if COMPS[comp].get("folder")
                                                else "%d films" % sum(len(v) for _, v in COMPS[comp]["stops"])))
