#!/usr/bin/env python3
"""Media, the owner's comp coverage portfolio: preview only (chat 16, 3 Nov 2026).

Owner, 3 Nov: the comp photos and daily videos "has to look like my portfolio" so they can sell a media
service; on the rest of the site it stays subtle (a photo credit, a line in the full-screen menu, a line in the
footer, owner's pick). Two pages in the site's own shell (partners.html) and tokens:

  media.html                      the portfolio: the strongest stills, the events covered, what an event gets,
                                  the call to book coverage
  media-srs-piedrahita-2026.html  one event: a section per day, its highlight video and its stills

Facts, each from the owner (3 Nov) or their YouTube playlists and the Air Tribune event page; nothing else:
  PWC Super Final, Pegalajar 2026: highlight videos only (Day 1, Tasks 1, 2, 4, 5);
  SRS Skywalk Bassano Edition 2026: live commentary on YouTube (Tasks 2 to 5);
  SRS BGD Edition, Piedrahita 2026: stills and video (Day 1, Task 1, Task 2 highlights; 20 chosen stills);
  SRS Advance Edition, Tapalpa: 8 to 14 Nov 2026 (registration 7 Nov), stills and video, to come.
Rates and turnaround are [to supply]. Videos open on YouTube (a page in claude.ai cannot embed them); on the
site they will play in place on a tap (youtube-nocookie, loaded only then).

Photos are web copies only (the owner keeps the originals): WebP at 1600 px and 800 px on the long side.
The preview's photos are not committed; the real ones go to the media repository.

    python3 tools/v4_media_preview.py PHOTOS_DIR THUMBS_DIR OUT_DIR
"""
import html
import os
import re
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(ROOT, "prototypes", "v4", "partners.html")
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"

PHOTOS = {   # file stem: (task, alt)
    "SRS_5_T1_9": (1, "An orange wing high over a patchwork of fields under cloud"),
    "SRS_5_T2_133-2": (2, "An orange and black wing between white clouds"),
    "SRS_5_T2_64": (2, "A red and white wing alone in a blue sky"),
    "SRS_5_T2_76": (2, "A lime wing above a forested slope"),
    "SRS_5_T2_83": (2, "A white wing with a red edge against a deep blue sky"),
    "SRS_5_T3_121": (3, "A white wing with a red edge seen from below"),
    "SRS_5_T3_127": (3, "A red wing seen from below"),
    "SRS_5_T3_150": (3, "An orange wing in a clear blue sky"),
    "SRS_5_T3_166": (3, "A blue and white wing in a deep blue sky"),
    "SRS_5_T3_172": (3, "A yellow wing in a blue sky"),
    "SRS_5_T3_21": (3, "A red and blue wing over the valley and its winding road"),
    "SRS_5_T3_27": (3, "A white and blue wing over the dry plain"),
    "SRS_5_T3_38": (3, "An orange wing over fields and trees"),
    "SRS_5_T3_47": (3, "A green wing above a winding road"),
    "SRS_5_T3_57": (3, "A white wing over the scrub"),
    "SRS_5_T3_63": (3, "The gaggle, dozens of wings in the blue"),
    "SRS_5_T3_64": (3, "Wings stacked in a climb"),
    "SRS_5_T3_66": (3, "The race spread high across the sky"),
    "SRS_5_T3_86": (3, "A red wing over the plain"),
    "SRS_5_T3_92": (3, "A yellow wing over a green hillside"),
}
HERO, HERO_P = "SRS_5_T3_21", "SRS_5_T3_38"
SELECT = ["SRS_5_T2_133-2", "SRS_5_T3_63", "SRS_5_T3_172", "SRS_5_T3_47", "SRS_5_T3_86", "SRS_5_T2_83",
          "SRS_5_T3_150", "SRS_5_T3_57"]   # an order that fills the grid in 3 and in 2 columns

YT = "https://www.youtube.com/watch?v=%s"
EVENTS = [
    dict(name="SRS Advance Edition, Tapalpa", when="8 to 14 Nov 2026", what="Stills and daily video",
         state="Next", href=None, thumb=None),
    dict(name="SRS BGD Edition, Piedrahita", when="2026", what="Stills and highlight videos",
         state="", href="media-srs-piedrahita-2026.html", thumb="NXUEyPQ3V4E"),
    dict(name="SRS Skywalk Bassano Edition", when="2026", what="Live commentary",
         state="", href=YT % "PEyO6MXngUw" + "&list=PLwalaswPmuBhoes6pMIu-bfntsAVM0eIK", thumb="PEyO6MXngUw"),
    dict(name="PWC Super Final, Pegalajar", when="2026", what="Highlight videos",
         state="", href=YT % "vPnIYYKcvEg" + "&list=PLwalaswPmuBgYtvCDEXKDP6kJC0qubzou", thumb="vPnIYYKcvEg"),
]
PIEDRAHITA_DAYS = [
    ("Day 1", "Registration, pilots and the Peñas de Piedrahíta", "cuGs7Lk6Dt4", 0),
    ("Task 1", "", "uCEfssE40u8", 1),
    ("Task 2", "", "NXUEyPQ3V4E", 2),
    ("Task 3", "", None, 3),
]
VIDEOS = ["cuGs7Lk6Dt4", "uCEfssE40u8", "NXUEyPQ3V4E", "PEyO6MXngUw", "vPnIYYKcvEg"]


def esc(s):
    return html.escape(s, quote=True)


def web_copies(src_dir, out_dir):
    """Each photo at 1600 and 800 px on its long side, WebP quality 80 (sharp at screen size)."""
    os.makedirs(out_dir, exist_ok=True)
    info = {}
    for stem in PHOTOS:
        im = ImageOps.exif_transpose(Image.open(os.path.join(src_dir, stem + ".jpg"))).convert("RGB")
        for w in (1600, 800):
            c = im.copy()
            c.thumbnail((w, w), Image.LANCZOS)
            c.save(os.path.join(out_dir, "%s-%d.webp" % (stem, w)), "WEBP", quality=80, method=6)
        c = im.copy(); c.thumbnail((1600, 1600))
        info[stem] = c.size
    return info


def video_stills(src_dir, out_dir):
    for v in VIDEOS:
        p = os.path.join(src_dir, v + ".jpg")
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((960, 960), Image.LANCZOS)
            im.save(os.path.join(out_dir, "yt-%s.webp" % v), "WEBP", quality=78, method=6)


def pic(stem, size, cls="md-ph", eager=False, sizes="(min-width: 1000px) 33vw, 100vw"):
    w, h = size[stem]
    alt = PHOTOS[stem][1]
    return ('<img class="%s" src="media-img/%s-1600.webp" srcset="media-img/%s-800.webp 800w, media-img/%s-1600.webp 1600w"'
            ' sizes="%s" width="%d" height="%d" alt="%s"%s>'
            % (cls, stem, stem, stem, sizes, w, h, esc(alt), ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'))


def tile(stem, size):
    w, h = size[stem]
    return ('<li class="md-t%s"><button type="button" class="md-open" data-full="media-img/%s-1600.webp" data-alt="%s">'
            '%s<span class="md-vh">Open the photo</span></button></li>'
            % (" is-tall" if h > w else "", stem, esc(PHOTOS[stem][1]), pic(stem, size)))


def video(vid, title, sub=""):
    return ('<a class="md-vid" href="%s" target="_blank" rel="noopener">'
            '<span class="md-vimg"><img src="media-img/yt-%s.webp" width="960" height="540" alt="" loading="lazy" decoding="async">'
            '<span class="md-play" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M8 5v14l11-7z"/></svg></span></span>'
            '<span class="md-vt">%s</span>%s<span class="md-vh"> (opens YouTube in a new tab)</span></a>'
            % (YT % vid, vid, esc(title), '<span class="md-vs">%s</span>' % esc(sub) if sub else ""))


CSS = r"""
/* Media: photo first. The site's tokens only; the photographs carry the colour. */
.md{--md-dim:color-mix(in srgb,var(--gray-light) 55%,var(--gray));}
.md-vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}
.md-hero{position:relative;min-height:min(92svh,980px);display:flex;align-items:flex-end;overflow:hidden;isolation:isolate;}
.md-hero picture,.md-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;}
.md-hero::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(180deg,transparent 35%,color-mix(in srgb,var(--bg) 62%,transparent) 62%,var(--bg) 100%);}
.md-hero-in .md-k,.md-h1,.md-lead{text-shadow:0 1px 16px color-mix(in srgb,var(--bg) 70%,transparent);}
.md-hero-in{padding:0 var(--gutter) clamp(2.2rem,6vw,4.5rem);max-width:60rem;}
.md-k{display:block;font:600 var(--fs-micro)/1.3 var(--font-body);letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin:0 0 var(--sp-2);}
.md-h1{margin:0;font:700 clamp(2.6rem,8vw,6.2rem)/.95 var(--font-display);letter-spacing:-.04em;color:var(--white);text-wrap:balance;}
.md-lead{margin:var(--sp-3) 0 0;max-width:40ch;font-size:var(--fs-lead);line-height:1.55;color:var(--gray-light);}
.md-by{margin:var(--sp-2) 0 0;font-size:var(--fs-small);color:var(--md-dim);}
.md-sec{padding:clamp(3rem,8vw,6rem) var(--gutter) 0;}
.md-h2{margin:0 0 var(--sp-4);font:700 var(--fs-h2)/1.1 var(--font-display);letter-spacing:-.02em;color:var(--white);text-wrap:balance;}
.md-sub{margin:calc(-1 * var(--sp-3)) 0 var(--sp-4);color:var(--md-dim);font-size:var(--fs-body-s);}
/* the stills: a calm grid, tall frames span two rows */
.md-grid{list-style:none;margin:0;padding:0;display:grid;gap:6px;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:44vw;grid-auto-flow:dense;}
@media (min-width:760px){.md-grid{grid-template-columns:repeat(3,minmax(0,1fr));grid-auto-rows:min(22vw,340px);}}
.md-t{margin:0;min-width:0;}
.md-t.is-tall{grid-row:span 2;}
.md-grid.is-one{grid-template-columns:minmax(0,52rem);grid-auto-rows:auto;}
.md-grid.is-one .md-ph{height:auto;}
.md-open{all:unset;box-sizing:border-box;display:block;width:100%;height:100%;cursor:zoom-in;overflow:hidden;border-radius:2px;}
.md-open:focus-visible{outline:2px solid var(--orange);outline-offset:2px;}
.md-ph{display:block;width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease),filter .8s var(--ease);}
@media (hover:hover) and (prefers-reduced-motion:no-preference){.md-open:hover .md-ph{transform:scale(1.035);}}
/* the events: one row each, like the expeditions index */
.md-ev{list-style:none;margin:0;padding:0;border-top:1px solid var(--line);}
.md-ev li{border-bottom:1px solid var(--line);}
.md-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.2rem var(--sp-3);align-items:baseline;padding:1.1rem 0;color:inherit;text-decoration:none;}
a.md-row:hover .md-en,a.md-row:focus-visible .md-en{text-decoration:underline;text-underline-offset:.2em;}
a.md-row:focus-visible{outline:2px solid var(--orange);outline-offset:4px;}
.md-en{font:600 clamp(1.15rem,2.6vw,1.6rem)/1.2 var(--font-display);color:var(--white);}
.md-ew{font-size:var(--fs-small);color:var(--md-dim);text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;}
.md-et{grid-column:1 / -1;font-size:var(--fs-body-s);color:var(--gray-light);}
.md-et b{font-weight:600;color:var(--orange);margin-right:.5rem;}
.md-arr{color:var(--md-dim);margin-left:.35rem;}
/* videos */
.md-vids{display:grid;gap:var(--sp-3);grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));}
.md-vid{display:grid;gap:.45rem;color:inherit;text-decoration:none;min-width:0;}
.md-vimg{position:relative;display:block;aspect-ratio:16 / 9;overflow:hidden;border-radius:2px;background:var(--card);}
.md-vimg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s var(--ease);}
.md-play{position:absolute;left:50%;top:50%;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;
  background:color-mix(in srgb,var(--bg) 55%,transparent);border:1px solid color-mix(in srgb,var(--white) 35%,transparent);display:grid;place-items:center;}
.md-play svg{width:22px;height:22px;fill:var(--white);margin-left:3px;}
.md-vt{font-weight:600;color:var(--white);}
.md-vs{font-size:var(--fs-small);color:var(--md-dim);}
@media (hover:hover) and (prefers-reduced-motion:no-preference){.md-vid:hover .md-vimg img{transform:scale(1.03);}}
.md-vid:focus-visible{outline:2px solid var(--orange);outline-offset:3px;}
/* what an event gets */
.md-offer{display:grid;gap:0;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));border-top:1px solid var(--line);}
.md-offer div{padding:var(--sp-3) var(--sp-3) var(--sp-3) 0;border-bottom:1px solid var(--line);}
.md-offer h3{margin:0 0 .35rem;font:600 var(--fs-h4)/1.25 var(--font-display);color:var(--white);}
.md-offer p{margin:0;color:var(--gray-light);font-size:var(--fs-body-s);line-height:1.55;}
.md-rate{margin:var(--sp-3) 0 0;color:var(--md-dim);font-size:var(--fs-small);}
.md-cta{padding:clamp(3rem,8vw,6rem) var(--gutter) clamp(3rem,8vw,6rem);}
.md-acts{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-2) var(--sp-4);margin-top:var(--sp-3);}
.md-acts .btn-solid{min-height:48px;box-sizing:border-box;display:inline-flex;align-items:center;}
.md-more{color:var(--white);text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:2px;}
.md-back{display:inline-block;margin:0 0 var(--sp-2);color:var(--md-dim);text-decoration:none;font-size:var(--fs-small);}
.md-back:hover{color:var(--white);}
/* an event's day */
.md-day{display:grid;gap:var(--sp-3);padding-top:var(--sp-4);margin-top:var(--sp-4);border-top:1px solid var(--line);}
.md-day:first-of-type{border-top:0;margin-top:0;padding-top:0;}
.md-dh{display:flex;flex-wrap:wrap;align-items:baseline;gap:.3rem var(--sp-3);}
.md-dh h2{margin:0;font:700 var(--fs-h3)/1.1 var(--font-display);color:var(--white);}
.md-dh p{margin:0;color:var(--md-dim);font-size:var(--fs-small);}
.md-day .md-vid{max-width:44rem;}
/* the full-screen view */
.md-lb{border:0;padding:0;margin:0;width:100vw;height:100svh;max-width:none;max-height:none;background:color-mix(in srgb,var(--bg) 96%,transparent);color:var(--white);}
.md-lb::backdrop{background:var(--bg);}
.md-lb[open]{display:grid;grid-template-rows:1fr auto;}
.md-lb img{width:100%;height:100%;object-fit:contain;display:block;min-height:0;}
.md-lbbar{display:flex;align-items:center;justify-content:space-between;gap:var(--sp-2);padding:.6rem var(--gutter) calc(.8rem + env(safe-area-inset-bottom,0px));}
.md-lbbar p{margin:0;font-size:var(--fs-small);color:var(--gray-light);min-width:0;}
.md-lbb{display:flex;gap:.4rem;flex:none;}
.md-lbb button{min-width:44px;min-height:44px;border:1px solid var(--line);border-radius:2px;background:none;color:var(--white);font:inherit;cursor:pointer;}
.md-lbb button:focus-visible{outline:2px solid var(--orange);outline-offset:2px;}
@media (prefers-reduced-motion:reduce){.md-ph,.md-vimg img{transition:none;}}
"""

LIGHTBOX = r"""<dialog class="md-lb" aria-label="Photo"><img alt=""><div class="md-lbbar"><p></p><div class="md-lbb">
<button type="button" data-go="-1" aria-label="Previous photo">&larr;</button><button type="button" data-go="1" aria-label="Next photo">&rarr;</button>
<button type="button" data-go="0" aria-label="Close">&times;</button></div></div></dialog>
<script>
(function () {
  var lb = document.querySelector(".md-lb"); if (!lb || !lb.showModal) return;
  var img = lb.querySelector("img"), cap = lb.querySelector("p");
  var all = [].slice.call(document.querySelectorAll(".md-open")), at = 0;
  function show(i) { at = (i + all.length) % all.length; var b = all[at]; img.src = b.getAttribute("data-full"); img.alt = b.getAttribute("data-alt"); cap.textContent = b.getAttribute("data-alt"); }
  all.forEach(function (b, i) { b.addEventListener("click", function () { show(i); lb.showModal(); }); });
  lb.addEventListener("click", function (e) {
    var g = e.target.closest("[data-go]");
    if (g) { var n = +g.getAttribute("data-go"); if (n) show(at + n); else lb.close(); }
    else if (e.target === img) lb.close();
  });
  lb.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") show(at + 1); if (e.key === "ArrowLeft") show(at - 1); });
  lb.addEventListener("close", function () { if (all[at]) all[at].focus(); });
  var x0 = null;
  lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) show(at + (dx < 0 ? 1 : -1)); x0 = null; }, { passive: true });
})();
</script>"""


def shell(title, desc):
    s = open(SHELL, encoding="utf-8").read()
    head, rest = s.split('<main id="v4-main">', 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", "<title>%s: Paragliding Atlas</title>" % esc(title), head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), head, count=1)
    head = re.sub(r"\n<style>.*?</style>\n(?=<!-- site-schema -->)", lambda m: "\n<style>" + CSS + "</style>\n", head, count=1, flags=re.S)
    head = head.replace(' aria-current="page" class="is-here"', "")
    if 'content="noindex' not in head:
        raise SystemExit("v4_media_preview: the shell lost its noindex")
    return head, tail.replace("</body>", LIGHTBOX + "\n</body>", 1)


def media_page(size):
    hero = ('<picture><source media="(max-width: 699px)" srcset="media-img/%s-800.webp 800w, media-img/%s-1600.webp 1600w" sizes="100vw">'
            '%s</picture>' % (HERO_P, HERO_P, pic(HERO, size, cls="md-heroimg", eager=True, sizes="100vw")))
    rows = []
    for e in EVENTS:
        inner = ('<span class="md-en">%s%s</span><span class="md-ew">%s</span><span class="md-et">%s%s</span>'
                 % (esc(e["name"]), '<span class="md-arr" aria-hidden="true">&rarr;</span>' if e["href"] else "", esc(e["when"]),
                    '<b>%s</b>' % esc(e["state"]) if e["state"] else "", esc(e["what"])))
        if e["href"]:
            ext = e["href"].startswith("http")
            rows.append('<li><a class="md-row" href="%s"%s>%s%s</a></li>' % (esc(e["href"]), ' target="_blank" rel="noopener"' if ext else "", inner,
                                                                         '<span class="md-vh"> (opens YouTube in a new tab)</span>' if ext else ""))
        else:
            rows.append('<li><div class="md-row">%s</div></li>' % inner)
    vids = "".join([video("NXUEyPQ3V4E", "SRS Piedrahita, Task 2", "Highlights"),
                    video("vPnIYYKcvEg", "PWC Super Final, Pegalajar", "Task 5 highlights"),
                    video("PEyO6MXngUw", "SRS Skywalk Bassano", "Live commentary, final day")])
    return ('<div class="md">'
            '<header class="md-hero">%s<div class="md-hero-in"><span class="md-k">Media</span>'
            '<h1 class="md-h1">From The Comps</h1>'
            '<p class="md-lead">Stills, daily highlight videos and live commentary from paragliding competitions.</p>'
            '<p class="md-by">By Aninder Singh</p></div></header>'
            '<section class="md-sec" aria-labelledby="md-st"><h2 class="md-h2" id="md-st">Selected Stills</h2>'
            '<p class="md-sub">SRS BGD Edition, Piedrahita 2026</p><ul class="md-grid">%s</ul></section>'
            '<section class="md-sec" aria-labelledby="md-ev-h"><h2 class="md-h2" id="md-ev-h">Events</h2><ul class="md-ev">%s</ul></section>'
            '<section class="md-sec" aria-labelledby="md-v"><h2 class="md-h2" id="md-v">On Film</h2><div class="md-vids">%s</div></section>'
            '<section class="md-sec" aria-labelledby="md-o"><h2 class="md-h2" id="md-o">For Your Event</h2><div class="md-offer">'
            '<div><h3>Daily Stills</h3><p>Edited selects from every task day, for the event and its pilots.</p></div>'
            '<div><h3>Daily Highlight Video</h3><p>A short film of each task, ready for the event&rsquo;s channels.</p></div>'
            '<div><h3>Live Commentary</h3><p>The race called live on YouTube, task by task.</p></div></div>'
            '<p class="md-rate">Rates and turnaround <i class="v2-tbd">[to supply]</i></p></section>'
            '<section class="md-cta" aria-labelledby="md-c"><h2 class="md-h2" id="md-c">Covering An Event?</h2>'
            '<p class="md-lead">Book a free 30-minute call, or send an enquiry.</p>'
            '<div class="md-acts"><a class="btn-solid" href="%s" target="_blank" rel="noopener"><span>Book a call<span class="md-vh"> (opens a new tab)</span></span></a>'
            '<a class="md-more" href="enquire.html">Enquire</a></div></section></div>'
            % (hero, "".join(tile(s, size) for s in SELECT), "".join(rows), vids, CALL))


def event_page(size):
    days = []
    for name, sub, vid, task in PIEDRAHITA_DAYS:
        stems = [s for s, (t, _) in PHOTOS.items() if t == task] if task else []
        body = video(vid, "%s highlights" % name if task else name, "Watch on YouTube") if vid else ""
        if stems:
            body += '<ul class="md-grid%s">%s</ul>' % (" is-one" if len(stems) == 1 else "", "".join(tile(s, size) for s in stems))
        days.append('<section class="md-day" aria-labelledby="d-%d"><div class="md-dh"><h2 id="d-%d">%s</h2>%s</div>%s</section>'
                    % (task, task, name, '<p>%s</p>' % esc(sub) if sub else "", body))
    hero = pic("SRS_5_T3_63", size, cls="md-heroimg", eager=True, sizes="100vw")
    return ('<div class="md"><header class="md-hero">%s<div class="md-hero-in"><a class="md-back" href="@@MEDIA@@">&larr; Media</a>'
            '<span class="md-k">Sports Racing Series</span><h1 class="md-h1">SRS BGD Edition, Piedrahita</h1>'
            '<p class="md-lead">2026. Stills and highlight videos, day by day.</p></div></header>'
            '<div class="md-sec">%s</div>'
            '<section class="md-cta" aria-labelledby="md-c"><h2 class="md-h2" id="md-c">Covering An Event?</h2>'
            '<div class="md-acts"><a class="btn-solid" href="%s" target="_blank" rel="noopener"><span>Book a call<span class="md-vh"> (opens a new tab)</span></span></a>'
            '<a class="md-more" href="@@MEDIA@@">More from the comps</a></div></section></div>'
            % (hero, "".join(days), CALL))


def main():
    photos, thumbs, out = sys.argv[1:4]
    size = web_copies(photos, os.path.join(out, "media-img"))
    video_stills(thumbs, os.path.join(out, "media-img"))
    for fn, title, desc, body in [
            ("media.html", "Media", "Stills, daily highlight videos and live commentary from paragliding competitions, by Aninder Singh.", media_page(size)),
            ("media-srs-piedrahita-2026.html", "SRS BGD Edition, Piedrahita", "Stills and highlight videos from SRS BGD Edition, Piedrahita 2026.", event_page(size))]:
        head, tail = shell(title, desc)
        page = head + '<main id="v4-main">' + body + "</main>" + tail
        if "—" in page:
            raise SystemExit("v4_media_preview: an em dash crept in")
        page = page.replace("@@MEDIA@@", os.environ.get("MEDIA_HREF", "media.html"))
        open(os.path.join(out, fn), "w", encoding="utf-8").write(page)
        print("wrote", fn, len(page) // 1024, "KB")


if __name__ == "__main__":
    main()
