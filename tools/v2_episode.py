#!/usr/bin/env python3
"""
Build the v2 episode page from the live one (prototypes/v2/episodes/).

The live page (episodes/<slug>.html, written by generate_chapter_deck.py) is
the source: its transcript, chapters, player, sync hooks and side boxes are
kept exactly. This only rearranges the page around them and adds four things,
all from data the site already has (episode-meta.json), nothing invented:

  hero      the short title (the YouTube title split at its first colon or
            bar, the guest's name taken off the front or the end), the rest as
            a subtitle, the guest's portrait, and the listen buttons up top;
  stage     the player first and wide, the pull quote and the guest card beside
            it, and for a video a chapter timeline under the player;
  side      a "Fly with us" panel with the next departures (FLY below);
  up next   four episodes from the same series, nearest in date.

The guest card shows the photo, the name and the guest's other episodes. There
is no role or bio line: episode-meta.json has none for any guest.

Links are written as the live page would write them (relative to episodes/);
tools/v2_localize.py then points them at the v2 twins or the live files, and
adds the noindex, v2.css and the v2 scripts.

    python3 tools/v2_episode.py slug [slug ...]
    python3 tools/v2_episode.py --samples
    python3 tools/v2_episode.py --all
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "episodes")
OUT = os.path.join(S.DIR, "episodes")
SAMPLES = ["urs-haari-the-real-truth-about-reserve-parachutes-a", "anatomy-of-a-dream-with-damien-lacaze"]

# The next departures, as the dates table on the v2 homepage has them.
FLY = [
    ("India", "21 to 30 Oct 2026", "10 days", "&pound;1,100", "../destinations/india.html"),
    ("Kenya", "18 to 29 Jan 2027", "12 days", "US$2,100", "../destinations/kenya.html"),
]

# Clean portraits (no poster text), by the name the site's own alt text gives.
PORTRAITS = {
    "Alain Zoller": "alain", "Antoine Girard": "antoine", "Gabriel Orsini": "gabriel",
    "Helmut Schrempf": "helmut", "Honorin Hamard": "honorin", "Kinga Masztalerz": "kinga",
    "Luc Armant": "luc", "Dr Matt Wilkes": "matt", "Maxime Pinot": "maxime",
    "Ivelin Kalushkov": "meterology", "Michael Nesler": "michaiel", "Russell Ogden": "russel",
    "Tom Lolies": "tom", "Urs Haari": "urs", "Will Gadd": "will",
}

e = html.escape
HOST = "Aninder Singh"


def split_title(title, guest):
    t = title.strip()
    if guest and t.lower().startswith(guest.lower() + ":"):
        t = t[len(guest) + 1:].strip()
    m = re.search(r"\s[:|]\s|:\s", t)
    main, sub = (t[:m.start()], t[m.end():]) if m else (t, "")
    if main.strip().lower() in ("snippet", "trailer", "teaser", "bonus", "short") and sub:
        main, sub = sub, ""
    # "A Talk with Zsolt Ero" under "with Zsolt Ero" says nothing new
    if guest and re.fullmatch(r"(?:an?\s+)?(?:talk|conversation|chat|interview)?\s*(?:with|ft\.?|feat\.?)?\s*" + re.escape(guest) + r"[.!]?", sub.strip(), re.I):
        sub = ""
    if guest:
        main = re.sub(r"\s+(?:with|ft\.?|feat\.?)\s+" + re.escape(guest) + r"\s*$", "", main, flags=re.I)
    return main.strip(" :|"), sub.strip(" :|")


def portrait(ep):
    """Guest photo, else the episode's own artwork, else its video still."""
    g = PORTRAITS.get(ep.get("guest", ""))
    if g:
        return "../assets/podcast/guest-%s" % g, True, "is-portrait"
    art = os.path.join(ROOT, "assets", "podcast", "artwork", ep["slug"] + ".jpg")
    if os.path.exists(art):
        return "../assets/podcast/artwork/" + ep["slug"], True, "is-art"
    if ep.get("video_id"):
        return "https://i.ytimg.com/vi/%s/hqdefault.jpg" % ep["video_id"], False, "is-still"
    return None, False, ""


def thumb(ep):
    """An episode's own picture for a card: its video still (16:9, no bars),
    else its artwork. Never the guest's portrait, so every card is alike."""
    if ep.get("video_id"):
        return "https://i.ytimg.com/vi/%s/mqdefault.jpg" % ep["video_id"], False, "is-still"
    art = os.path.join(ROOT, "assets", "podcast", "artwork", ep["slug"] + ".jpg")
    if os.path.exists(art):
        return "../assets/podcast/artwork/" + ep["slug"], True, "is-art"
    return portrait(ep)


def pic(src, webp, alt, cls="", lazy=True):
    load = ' loading="lazy" decoding="async"' if lazy else ""
    if src is None:
        return ""
    if webp:
        return ('<picture class="%s"><source srcset="%s.webp" type="image/webp"><img src="%s.jpg" alt="%s"%s></picture>'
                % (cls, src, src, e(alt), load))
    return '<picture class="%s"><img src="%s" alt="%s"%s></picture>' % (cls, src, e(alt), load)


def secs(at):
    p = [int(x) for x in at.split(":")]
    s = 0
    for x in p:
        s = s * 60 + x
    return s


def cut(s, start, end):
    """Remove s[start:end] and return (removed, rest)."""
    return s[start:end], s[:start] + s[end:]


def grab(s, open_re, close):
    m = re.search(open_re, s)
    if not m:
        return "", s
    end = s.index(close, m.end()) + len(close)
    return cut(s, m.start(), end)


def build(slug, meta):
    ep = meta[slug]
    src = open(os.path.join(LIVE, slug + ".html"), encoding="utf-8").read()
    guest = ep.get("guest", "")
    main_t, sub_t = split_title(ep["title"], guest)
    # "Snippet:", "Trailer:" and the like come off the big title but stay in the heading
    lm = re.match(r"\s*(snippet|trailer|teaser|bonus|short)\s*[:|]", ep["title"], re.I)
    label = lm.group(1).title() if lm else ""
    is_audio = "cd-player-audio" in src

    # ---- take the pieces out of the live page ----
    listen, src = grab(src, r'\n\s*<div class="cd-listen">', "</div>")
    # the player's close is the first "</div>" at the player line's own indent
    open_at = src.index('<div class="cd-player')
    p_start = src.rindex("\n", 0, open_at)
    indent = src[p_start + 1:open_at]
    p_end = src.index("\n" + indent + "</div>", open_at) + len("\n" + indent + "</div>")
    player, src = cut(src, p_start, p_end)
    quote, src = grab(src, r'\n\s*<figure class="cd-quote">', "</figure>")
    guestbox, src = grab(src, r'\n\s*<div class="cd-box">\s*<h2>The Guest</h2>', "\n      </div>\n")

    # ---- hero ----
    img, webp, kind = portrait(ep)
    # every episode takes the player-beside-the-title layout (the owner's choice,
    # 26 Sep 2026); the portrait layout is kept in the code but no longer used
    face = False
    series = ep.get("series", "")
    head_re = re.compile(r'<p class="cd-epno">.*?</p>\s*<div class="cd-headgrid">.*?</header>', re.S)
    submeta = re.search(r'<div class="cd-submeta">.*?</div>', src, re.S).group(0)
    host = guest == HOST            # the host's own episodes (AMA, notes): no "with", no guest card
    no = re.search(r'<p class="cd-epno">(.*?)</p>', src)
    epno = " &middot; ".join(x for x in ((no.group(1).strip() if no else ""), e(series)) if x)
    hero = ('<p class="cd-epno">%s</p>' % epno.replace("\\", "\\\\")
            + '\n    <div class="ep2-hero%s">' % ("" if face else " is-media")
            + '\n      <div class="ep2-hero-copy">'
            # the guest's name stays inside the heading: it is in the live <h1>, and search reads it there
            + '\n        <h1>%s<span class="ep2-h1">%s</span>%s</h1>' % (
                '<span class="ep2-with">%s%s <strong>%s</strong></span> ' % (label + " &middot; " if label else "", "Hosted by" if host else "with", e(guest)) if guest
                else ('<span class="ep2-with">%s</span> ' % label if label else ""),
                e(main_t), ' <span class="ep2-sub">%s</span>' % e(sub_t) if sub_t else "")
            + "\n        " + submeta.replace("\\", "\\\\")
            + re.sub(r"<span>(Watch on|Listen on) ", r'<span><i class="ep2-lw">\1 </i>', listen.replace("\\", "\\\\")).replace('class="cd-listen"', 'class="cd-listen ep2-listen"')
            + "\n      </div>"
            # a face earns the hero; without one the player takes that space (filled in below)
            + ('\n      <figure class="ep2-portrait %s">%s</figure>' % (kind, pic(img, webp, guest or main_t, lazy=False).replace("\\", "\\\\")) if face else "\n      <!--ep2-hero-media-->")
            + "\n    </div>\n  </header>")
    src = head_re.sub(hero, src, count=1)

    # ---- stage: player, timeline, quote, guest card ----
    timeline = ""
    total = None
    dm = re.match(r"(\d+)\s*min", ep.get("duration_label", ""))
    if dm:
        total = int(dm.group(1)) * 60
    # the page's own chapter rail (it is what the transcript blocks follow)
    rail = re.findall(r'<a class="cd-chap[^"]*" href="#c(\d+)">(.*?)<time>([^<]+)</time></a>', src)
    if not is_audio and total and len(rail) > 1:
        ticks = []
        for k, (n, title, at) in enumerate(rail):
            a = secs(at)
            b = secs(rail[k + 1][2]) if k + 1 < len(rail) else total
            if a >= total:
                continue
            ticks.append('<a class="ep2-tick" href="#c%s" data-c="%s" style="--a:%.3f;--w:%.3f"><span class="ep2-tick-t">%s</span><time>%s</time></a>'
                         % (n, n, 100 * a / total, 100 * max(min(b, total) - a, 1) / total, title, e(at)))
        timeline = ('\n        <nav class="ep2-timeline" aria-label="Chapters on a timeline"><div class="ep2-track">%s</div></nav>' % "".join(ticks))

    others = [o for o in meta.values() if guest and not host and o.get("guest") == guest and o["slug"] != slug and o["_listed"]]
    card = ['\n        <div class="ep2-guest kit-panel">', '<span class="ep2-k">%s</span>' % ("The host" if host else "The guest")]
    if face:
        card.append('<span class="ep2-guest-face">%s</span>' % pic(img, webp, ""))
    card.append('<p class="ep2-guest-name">%s</p>' % e(guest or "Aninder Singh"))
    if others:
        card.append('<p class="ep2-guest-more">Also with %s</p>' % e(guest.split(" ")[0] if guest else ""))
        for o in sorted(others, key=lambda o: o.get("published", ""), reverse=True)[:3]:
            card.append('<a class="cd-link" href="%s.html">%s</a>' % (o["slug"], e(split_title(o["title"], guest)[0])))
    card.append("</div>")
    if not guest:                   # race highlights and flying films: nobody to introduce
        card = []

    side = quote.replace('class="cd-quote"', 'class="cd-quote ep2-quote"') + "".join(card)
    if face:
        stage = ('\n\n  <div class="ep2-stage">\n    <div class="ep2-stage-play">\n      %s%s\n    </div>\n    <div class="ep2-stage-side">%s\n    </div>\n  </div>\n'
                 % (player.strip(), timeline, side))
    else:
        src = src.replace("<!--ep2-hero-media-->", '<div class="ep2-hero-media">\n      %s%s\n      </div>' % (player.strip(), timeline), 1)
        stage = ('\n\n  <div class="ep2-stage is-side%s">\n    <div class="ep2-stage-side">%s\n    </div>\n  </div>\n'
                 % ("" if quote and card else " is-one", side)) if side.strip() else ""
    src = src.replace('\n  <div class="cd-main">', stage + '\n  <div class="cd-main">', 1)

    # ---- fly with us, first in the side column ----
    fly = ['\n      <div class="cd-box ep2-fly">', "        <h2>Fly with us</h2>"]
    for place, dates, days, price, href in FLY:
        fly.append('        <a class="ep2-fly-row" href="%s"><b>%s</b><span>%s &middot; %s &middot; from %s</span><i aria-hidden="true">&rarr;</i></a>' % (href, place, dates, days, price))
    fly.append('        <p class="ep2-fly-note">Small-group guided expeditions, from the people behind the podcast.</p>')
    fly.append("      </div>\n")
    src = src.replace('<aside class="cd-side">\n', '<aside class="cd-side">\n' + "\n".join(fly), 1)

    # ---- up next: same series, nearest in date ----
    pool = [o for o in meta.values() if o.get("series") == series and o["slug"] != slug and o.get("published") and o["_listed"]]
    pool.sort(key=lambda o: abs(int(o["published"].replace("-", "")) - int(ep.get("published", "0").replace("-", "") or 0)))
    cards = []
    for o in pool[:4]:
        oi, ow, ok = thumb(o)
        t, _ = split_title(o["title"], o.get("guest", ""))
        cards.append('<a class="ep2-card" href="%s.html"><span class="ep2-card-art %s">%s</span><span class="ep2-card-body"><span class="ep2-card-k">%s</span><span class="ep2-card-t">%s</span><span class="ep2-card-m">%s%s</span></span></a>'
                     % (o["slug"], ok, pic(oi, ow, ""), e(o.get("epno", "")), e(t), e(o.get("guest", "")),
                        (" &middot; " + e(o["duration_label"])) if o.get("duration_label") else ""))
    upnext = ""
    if cards:
        upnext = ('\n  <section class="ep2-next" aria-labelledby="ep2-next-h">\n    <div class="ep2-next-head"><span class="ep2-k">Up next</span>'
                  '<h2 id="ep2-next-h">More from %s</h2><a class="ep2-next-all" href="../library.html#s=%s">All of the series <i aria-hidden="true">&rarr;</i></a></div>\n    <div class="ep2-next-grid">%s</div>\n  </section>\n'
                  % (e(series), ep.get("series_slug", ""), "".join(cards)))
    # after the grid, still inside .cd-wrap
    src = re.sub(r"(\n    </aside>\n\n  </div>\n)(</div>)", lambda m: m.group(1) + upnext + m.group(2), src, count=1)

    # ---- page flags ----
    src = src.replace("<body>", '<body data-v2="ep">', 1)
    src = src.replace('<div class="cd-wrap cd-v2"', '<div class="cd-wrap cd-v2 ep2"', 1)
    return src


def library_slugs():
    """The episodes the library lists (library-data.js leaves out reels and housekeeping)."""
    src = open(os.path.join(ROOT, "library-data.js"), encoding="utf-8").read()
    return set(re.findall(r'page:\s*"([^"]+)"', src))


def main(argv):
    lib = library_slugs()
    meta = {m["slug"]: m for m in json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))}
    for m in meta.values():
        m["_listed"] = m["slug"] in lib
    # --all: every episode in episode-meta.json (the redirect stubs are not in it)
    slugs = SAMPLES if argv == ["--samples"] else sorted(meta) if argv == ["--all"] else argv
    os.makedirs(OUT, exist_ok=True)
    for slug in slugs:
        page = build(slug, meta)
        open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8").write(page)
        print("v2 episode:", slug)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
