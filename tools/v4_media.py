#!/usr/bin/env python3
"""Media: the owner's comp photo and video coverage portfolio (chat 17, 3 Nov 2026).

Owner, 3 Nov: "this is my face to asking people to trust my site ... where I convert eyeballs into customers and
newsletter subscribers, but all in an elegant and effective way." Chat 16's first preview was rejected ("a joke ...
incomplete, no zoom on the pics, pay button is different from rest of the site"), so this page is built only from
the site's own parts: the About page's shell (head, nav, footer), kit-hero with kit-stats, kit-head, btn-solid and
btn-lines, kit-card v2-tour cards, v2-chip, the India page's photo viewer (fly.js, copied into v4-media.js), the
home page's play-in-place video (tap the still, youtube-nocookie loads only then), cta-band and the .v2-nl
newsletter form (/newsletter.js, MailerLite form 199520945794189126).

Pages written into prototypes/v4/ (owned by this generator, like record-*.html):
  media.html                       the portfolio, in the agreed order: hero with the proof, the showreel,
                                   selected stills (full frames, zoom), the comps, what an event gets, how it
                                   works, a quote ([to supply] until the owner sends one), booking, newsletter
  media-srs-piedrahita-2026.html   one comp: its videos and every chosen still, by task

Facts, each from the owner (3 Nov), their Canva pitches, or their YouTube videos (vidIQ, 3 Nov); nothing else.
Photos are web copies only (the owner keeps the originals): WebP 800, 1600 and 2400 px on the long side, from
tools/v4_media_photos.py. Where they are served from is MEDIA below (the photo repository, once it exists).

    python3 tools/v4_media.py                 # writes the two pages
    python3 tools/v4_media.py --media URL/    # with the photos served from URL/ (a preview)
"""
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
HERO, HERO_P, CARD = "SRS_5_T3_21", "SRS_5_T2_83", "SRS_5_T3_38"
SELECT = ["SRS_5_T2_133-2", "SRS_5_T3_63", "SRS_5_T3_172", "SRS_5_T3_64", "SRS_5_T3_27", "SRS_5_T3_92",
          "SRS_5_T1_9", "SRS_5_T3_86", "SRS_5_T3_150", "SRS_5_T3_121", "SRS_5_T2_76", "SRS_5_T3_57"]


def src(stem, w):
    return MEDIA + "%s-%d.webp" % (stem, w)


def figure(stem, where="Piedrahita 2026"):
    w, h, t, alt = PH[stem]
    r = w / h
    return ('<figure class="md-ph" style="--r:%.4f"><a href="%s" data-full="%s"><img src="%s" srcset="%s 800w, %s 1600w" '
            'sizes="(max-width:700px) 70vw, 40vw" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></a>'
            '<figcaption><b>%s, Task %d</b></figcaption></figure>'
            % (r, src(stem, 2400), src(stem, 2400), src(stem, 800), src(stem, 800), src(stem, 1600),
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
    "DA4nGop3i9g": ("srs4", "Live: Task 4, part 2", 513, "3 h 55 min", "30 May 2026", None),
    "PEyO6MXngUw": ("srs4", "Live: Task 5, the final day", 680, "5 h 8 min", "30 May 2026", None),
}
COMPS = {"pwc": "PWC Super Final, Pegalajar", "srs5": "SRS Piedrahita", "srs4": "SRS Bassano, live"}
REEL = "BRAX1XMU390"
TOTAL = sum(v[2] for v in V.values())             # 31,250 on 3 Nov 2026
assert TOTAL == 31250, TOTAL

PLAY = ('<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 1.2v7.6c0 .5.5.8.9.5l5.9-3.8c.4-.2.4-.8 0-1L2.9.7C2.5.4 '
        '2 .7 2 1.2z"/></svg>')


def thumb(v, q="maxresdefault"):
    return "https://i.ytimg.com/vi/%s/%s.jpg" % (v, q)


def frame(v, eager=False):
    c, t, n, ln, d, ep = V[v]
    return ('<div class="md-frame" data-vid="%s"><img src="%s" alt="" width="1280" height="720"%s decoding="async">'
            '<a class="md-play" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" '
            'aria-label="Play %s, %s">%s</a></div>'
            % (v, thumb(v), "" if eager else ' loading="lazy"', v, E(t), E(COMPS[c]), PLAY))


def vmeta(v):
    c, t, n, ln, d, ep = V[v]
    return "%s views &middot; %s" % ("{:,}".format(n), ln)


# ---------------------------------------------------------------- the page parts ----
ICON_WA = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.3-18.1C18.1 1.5 15.1.2 12 .2 5.5.2.2 5.5.2 12c0 2.1.5 4.1 1.6 5.9L.1 24l6.3-1.6c1.7.9 3.7 1.4 5.6 1.4 6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.5-8.3z"/></svg>')


def cta(title, tag, body):
    return ('<section class="cta-band" id="book">\n  <div class="cta-card">\n  <span class="cta-hud-tag">%s</span>\n  <h2>%s</h2>\n'
            '  <div class="cta-buttons">\n    <a href="%s" target="_blank" rel="noopener" class="btn-solid" data-hover><span>Book a Call</span></a>\n'
            '    <a href="%s" target="_blank" rel="noopener" class="listen-btn" data-hover><span>%s WhatsApp</span></a>\n'
            '    <a href="enquire.html?trip=media" class="btn-lines" data-hover>Send a Media Enquiry</a>\n  </div>\n'
            '  <p class="cta-body">%s</p>\n  </div>\n</section>\n' % (tag, title, CALL, WA, ICON_WA, body))


NEWSLETTER = '''<section class="kit-band md-nl-band">
  <div class="kit-in">
    <div class="v2-nl md-nl" data-nl>
      <span class="kit-kicker">Stay In Touch</span>
      <h2 class="kit-title">Follow Tapalpa Day By Day</h2>
      <p class="kit-intro">SRS Tapalpa, Mexico, 8 to 14 Nov 2026: the daily highlights and results in your inbox, with trip updates and new episodes. No spam. Unsubscribe any time.</p>
      <label class="v2-search-label" for="newsletterEmail">Email Address</label>
      <div class="v2-nl-row">
        <input id="newsletterEmail" type="email" placeholder="you@example.com" autocomplete="email">
        <button class="btn-solid" data-hover><span>Sign Up</span></button>
      </div>
      <p class="nl-status" data-nl-status role="status" aria-live="polite"></p>
      <p class="fine-print">By submitting you consent to email updates from Paragliding Atlas. Unsubscribe any time.</p>
    </div>
  </div>
</section>
'''

VIEWER = ('<dialog class="v4i-fl-lb" id="v4i-fl-lb" aria-label="The photograph, enlarged"><div class="v4i-fl-lbs"><img alt="" draggable="false"></div>'
          '<button class="v4i-fl-lbx" type="button" aria-label="Close the photograph"></button><span class="v4i-fl-lbc"></span>'
          '<button class="v4i-fl-lbn v4i-fl-lbp" type="button" hidden aria-label="Previous photograph"><svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg></button>'
          '<button class="v4i-fl-lbn v4i-fl-lbnx" type="button" hidden aria-label="Next photograph"><svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5"/></svg></button>'
          '<span class="v4i-fl-lbh" aria-hidden="true">click to come closer &middot; scroll or pinch for more &middot; drag to move &middot; arrows for the next &middot; click outside to close</span></dialog>')

CSS = r'''
/* Media (tools/v4_media.py): only what the kit does not have */
html body .kit-hero .kit-stats{gap:var(--sp-3) clamp(1.6rem,4vw,3.4rem)}
html body .kit-hero .kit-stat b{font-family:var(--font-display);font-weight:700;font-size:clamp(1.7rem,3.6vw,2.8rem);line-height:1;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
html body .kit-hero .kit-stat span{color:var(--gray-light);margin-top:.55rem}
html body .kit-hero .kit-stat b>span{display:inline;margin:0;font:inherit;color:inherit;letter-spacing:inherit;text-transform:none}
html body .kit-hero .kit-stat b>.v4-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.md-hero .kit-actions{margin-top:var(--sp-4)}
.md-hero .kit-hero-media img{object-position:62% 40%}
.md-by{display:block;margin-top:var(--sp-4);font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}
.md-by b{color:var(--gray-light);font-weight:400}
/* the showreel: one big frame, the other videos beside it, each plays in place */
.md-reel{display:grid;grid-template-columns:minmax(0,1.85fr) minmax(0,1fr);gap:clamp(1.25rem,3vw,2.5rem);align-items:stretch;margin-top:var(--sp-5)}
.md-frame{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--card);border-radius:3px}
.md-frame>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .9s var(--ease-out),filter .45s var(--ease-out);filter:brightness(.82)}
.md-frame:hover>img{transform:scale(1.025);filter:none}
.md-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:#000}
.md-frame.is-on>img,.md-frame.is-on .md-play{display:none}
.md-play{position:absolute;left:50%;top:50%;z-index:2;display:grid;place-items:center;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;
  background:color-mix(in srgb,var(--bg) 62%,transparent);color:color-mix(in srgb,var(--white) 86%,transparent);transition:color .3s var(--ease),transform .3s var(--ease),background .3s var(--ease)}
.md-play::before{content:"";position:absolute;inset:0}
.md-frame:hover .md-play,.md-play:focus-visible{color:var(--white);background:color-mix(in srgb,var(--orange) 78%,transparent)}
.md-play:active{transform:scale(.94)}
.md-play:focus-visible{outline:1px solid var(--orange);outline-offset:3px}
.md-play svg{position:relative;display:block;width:18px;height:18px;margin-left:3px;fill:currentColor}
.md-now{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:.4rem 1.2rem;margin-top:var(--sp-2)}
.md-now h3{margin:0;font-family:var(--font-display);font-weight:600;font-size:var(--fs-h4);color:var(--white)}
.md-now p{margin:0;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.08em;color:var(--gray)}
.md-now a{color:var(--gray-light);text-decoration:none;border-bottom:1px solid var(--line)}
.md-now a:hover{color:var(--white);border-color:var(--orange)}
.md-side .v2-chips{margin:0 0 var(--sp-2)}
.md-list{list-style:none;margin:0;padding:0;max-height:min(30rem,62vh);overflow:auto;scrollbar-width:thin;scrollbar-color:var(--edge) transparent}
.md-list li[hidden]{display:none}
.md-list button{all:unset;box-sizing:border-box;display:grid;grid-template-columns:7.5rem minmax(0,1fr);gap:.9rem;align-items:center;width:100%;padding:.55rem .5rem;border-radius:3px;cursor:pointer;transition:background .2s var(--ease)}
.md-list button:hover,.md-list button:focus-visible{background:rgba(255,255,255,.05)}
.md-list button:focus-visible{outline:1px solid var(--orange)}
.md-list button[aria-current="true"]{background:rgba(255,117,23,.1)}
.md-list img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:2px}
.md-list b{display:block;font-family:var(--font-display);font-weight:600;font-size:.95rem;line-height:1.3;color:var(--white)}
.md-list small{display:block;margin-top:.25rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray)}
.md-list button[aria-current="true"] b{color:var(--orange)}
/* stills: full frames in justified rows, every photograph opens in the viewer */
.md-grid{display:flex;flex-wrap:wrap;gap:clamp(6px,.8vw,10px);margin-top:var(--sp-5);--rh:clamp(150px,19vw,270px)}
.md-grid::after{content:"";flex:999 1 0}
.md-grid.is-js::after{content:none}
.md-grid.is-js .md-ph{flex:none}
.md-ph{margin:0;flex:var(--r) 1 calc(var(--r) * var(--rh));position:relative;overflow:hidden;background:var(--card)}
.md-ph a{display:block;cursor:zoom-in}
.md-ph img{display:block;width:100%;height:auto;aspect-ratio:var(--r);transition:transform .8s var(--ease-out),filter .5s var(--ease-out)}
.md-ph a:hover img,.md-ph a:focus-visible img{transform:scale(1.03)}
.md-ph a:focus-visible{outline:1px solid var(--orange);outline-offset:2px}
.md-ph figcaption{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.md-more{margin-top:var(--sp-4)}
.md-swipe{display:none;margin-top:.6rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}
/* the comps */
.md-comps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-3);margin-top:var(--sp-5)}
.md-comps .kit-card-media{aspect-ratio:3/2}
.md-comps .kit-card-media img{width:100%;height:100%;object-fit:cover}
.md-next{display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:1.1rem;background:radial-gradient(80% 90% at 85% 10%,rgba(255,117,23,.22),transparent 70%),var(--card)}
.md-next b{font-family:var(--font-display);font-weight:700;font-size:clamp(1.6rem,2.6vw,2.2rem);line-height:1.05;letter-spacing:-.02em;color:var(--white)}
.md-next span{margin-top:.35rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--gray-light)}
.md-comps .v2-tour-facts{grid-template-columns:repeat(2,minmax(0,1fr))}
.md-did{margin:.2rem 0 .9rem;color:var(--gray-light);font-size:.95rem;line-height:1.55}
/* what an event gets: four pieces along the event */
.md-four{list-style:none;margin:var(--sp-5) 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(1.2rem,2.6vw,2.2rem);counter-reset:md}
.md-four li{border-top:1px solid;border-image:linear-gradient(90deg,var(--orange),var(--line) 45%,transparent) 1;padding-top:1rem;display:flex;flex-direction:column}
.md-when{display:block;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--orange)}
.md-four h3{margin:.5rem 0 .55rem;font-family:var(--font-display);font-weight:700;font-size:var(--fs-h4);color:var(--white);line-height:1.2}
.md-four p{margin:0;color:var(--gray-light);font-size:1rem;line-height:1.65}
.md-four .md-eg{margin-top:auto;padding-top:.9rem;font-size:.9rem}
.md-eg a{color:var(--white);text-decoration:none;border-bottom:1px solid var(--orange)}
.md-eg a:hover{color:var(--orange)}
.md-also{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--sp-3);margin-top:var(--sp-5)}
.md-also .kit-panel h3{margin:0 0 .4rem;font-family:var(--font-display);font-weight:600;font-size:1.05rem;color:var(--white)}
.md-also .kit-panel p{margin:0;color:var(--gray-light);font-size:.95rem;line-height:1.6}
/* how it works */
.md-steps{list-style:none;margin:var(--sp-5) 0 0;padding:0}
.md-steps li{display:grid;grid-template-columns:clamp(2.5rem,5vw,4rem) minmax(0,16rem) minmax(0,1fr);gap:0 clamp(1rem,3vw,2.5rem);align-items:baseline;padding:clamp(1rem,2vw,1.4rem) 0;border-top:1px solid var(--line)}
.md-steps li:last-child{border-bottom:1px solid var(--line)}
.md-steps small{font-family:var(--font-display);font-weight:600;font-size:.9rem;letter-spacing:.1em;color:var(--orange)}
.md-steps b{font-family:var(--font-display);font-weight:700;font-size:clamp(1.5rem,3.2vw,2.4rem);line-height:1.1;letter-spacing:-.02em;color:var(--white)}
.md-steps p{margin:0;color:var(--gray-light);font-size:1rem;line-height:1.65;max-width:34rem}
/* a word from the comps */
.md-quote{margin:0;max-width:52rem}
.md-quote p{margin:0;font-family:var(--font-display);font-weight:600;font-size:clamp(1.4rem,3vw,2.2rem);line-height:1.3;letter-spacing:-.01em;color:var(--white)}
.md-quote footer{margin-top:var(--sp-3);font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}
.md-nl{max-width:40rem}
.cta-buttons .btn-lines{align-self:center}
/* the comp page: a section per day */
.md-day+.md-day{border-top:1px solid var(--line)}
.md-day .md-frame{max-width:62rem;margin-top:var(--sp-4)}
.md-day .md-grid{max-width:62rem}
.md-day .md-now{max-width:62rem}
.md-back{display:inline-block;margin-bottom:var(--sp-3);font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--gray-light);text-decoration:none}
.md-back:hover{color:var(--white)}
@media (max-width:1100px){.md-comps{grid-template-columns:repeat(2,minmax(0,1fr))}.md-four{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:2.2rem}}
@media (min-width:901px){.md-side{position:relative}.md-side-in{position:absolute;inset:0;display:flex;flex-direction:column}.md-side .md-list{flex:1;min-height:0;max-height:none}}
@media (max-width:900px){.md-reel{grid-template-columns:minmax(0,1fr)}
  .md-list{display:flex;gap:.75rem;max-height:none;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scrollbar-width:none;margin-right:calc(-1 * var(--gutter));padding-right:var(--gutter)}
  .md-list::-webkit-scrollbar{display:none}
  .md-list li{flex:none;width:min(44vw,15rem);scroll-snap-align:start}
  .md-list button{grid-template-columns:minmax(0,1fr);gap:.5rem;padding:.4rem}}
@media (max-width:700px){
  .md-hero .kit-hero-media img{object-position:50% 30%}
  .md-grid{--rh:118px}
  .md-four,.md-also{grid-template-columns:minmax(0,1fr)}
  .md-comps{display:flex;gap:.9rem;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;margin-right:calc(-1 * var(--gutter));padding-right:var(--gutter)}
  .md-comps::-webkit-scrollbar{display:none}
  .md-comps>.kit-card{flex:none;width:82%;scroll-snap-align:start}
  html body .kit-hero .kit-stats{flex-wrap:nowrap;gap:1.2rem}
  html body .kit-hero .kit-stat b{font-size:1.55rem;white-space:nowrap}
  .md-swipe{display:block}
  .md-side .v2-chips{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin-right:calc(-1 * var(--gutter));padding-right:var(--gutter)}
  .md-side .v2-chips::-webkit-scrollbar{display:none}
  .md-side .v2-chip{flex:none}
  .md-steps li{grid-template-columns:2.5rem minmax(0,1fr)}
  .md-steps p{grid-column:2;margin-top:.4rem}
  .md-play{width:56px;height:56px;margin:-28px 0 0 -28px}
  .cta-buttons .btn-lines{align-self:auto;text-align:center}
}
@media (prefers-reduced-motion:reduce){.md-frame>img,.md-ph img{transition:none}.md-frame:hover>img,.md-ph a:hover img{transform:none}}
/* the photo viewer, as on the India page (fly.js) */
.v4i-fl-lb{border:0;padding:0;margin:0;max-width:none;max-height:none;width:100vw;height:100vh;background:transparent;overflow:hidden;opacity:0;transition:opacity .22s var(--ease)}
.v4i-fl-lb.is-in{opacity:1}
.v4i-fl-lb::backdrop{background:rgba(20,21,25,.9);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.v4i-fl-lbs{position:absolute;inset:0;display:grid;place-items:center;touch-action:none}
.v4i-fl-lb img{max-width:min(92vw,1800px);max-height:86vh;width:auto;height:auto;display:block;box-shadow:0 40px 120px rgba(0,0,0,.7);border-radius:3px;cursor:zoom-in;transform-origin:center center;transition:transform .18s var(--ease),opacity .22s var(--ease);user-select:none;-webkit-user-drag:none;transform:scale(.96)}
.v4i-fl-lb.is-in img{transform:none}
.v4i-fl-lb.is-zoomed img{cursor:grab}
.v4i-fl-lb.is-drag img{cursor:grabbing;transition:opacity .22s var(--ease)}
.v4i-fl-lbx{position:absolute;top:1rem;right:1rem;width:2.6rem;height:2.6rem;border-radius:50%;border:1px solid rgba(246,244,244,.3);background:rgba(20,21,25,.5);cursor:pointer;z-index:2;padding:0;transition:border-color .2s var(--ease),transform .2s var(--ease)}
.v4i-fl-lbx::before,.v4i-fl-lbx::after{content:"";position:absolute;left:50%;top:50%;width:14px;height:1px;margin:0 0 0 -7px;background:var(--white);transform:rotate(45deg)}
.v4i-fl-lbx::after{transform:rotate(-45deg)}
.v4i-fl-lbx:hover,.v4i-fl-lbx:focus-visible{border-color:var(--orange);outline:none;transform:rotate(90deg)}
.v4i-fl-lbc{position:absolute;left:1.25rem;bottom:1.1rem;max-width:50vw;display:flex;align-items:baseline;gap:.8rem;font-family:var(--font-display);font-weight:600;font-size:var(--fs-small);color:var(--white);pointer-events:none}
.v4i-fl-lbc .v4i-fl-lbi{font-family:var(--font-mono);font-weight:400;font-size:var(--fs-micro);letter-spacing:.08em;color:var(--gray)}
.v4i-fl-lbn{position:absolute;top:50%;transform:translateY(-50%);width:2.8rem;height:2.8rem;border-radius:50%;border:1px solid rgba(246,244,244,.3);background:rgba(20,21,25,.5);color:var(--white);cursor:pointer;z-index:2;display:grid;place-items:center;padding:0;transition:border-color .2s var(--ease),background .2s var(--ease)}
.v4i-fl-lbn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.v4i-fl-lbn:hover,.v4i-fl-lbn:focus-visible{border-color:var(--orange);background:rgba(255,117,23,.18);outline:none}
.v4i-fl-lbn[hidden]{display:none}
.v4i-fl-lbp{left:1rem}
.v4i-fl-lbnx{right:1rem}
.v4i-fl-lbh{position:absolute;right:1.25rem;bottom:1.2rem;font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.06em;color:var(--gray);white-space:nowrap;pointer-events:none}
@media (max-width:700px){.v4i-fl-lbh{display:none}.v4i-fl-lb img{max-width:100vw;max-height:78vh;border-radius:0}.v4i-fl-lbc{bottom:1rem;max-width:calc(100vw - 2.5rem)}
  .v4i-fl-lbn{top:auto;bottom:4rem;transform:none}.v4i-fl-lbp{left:auto;right:4.4rem}.v4i-fl-lbnx{right:1rem}.v4i-fl-lbx,.v4i-fl-lbn{width:2.75rem;height:2.75rem}}
@media (prefers-reduced-motion:reduce){.v4i-fl-lb,.v4i-fl-lb img,.v4i-fl-lbx{transition:none}}
'''


def shell(title, desc, canon, og_img, name, main, extra_head=""):
    s = open(SHELL).read()

    def rep(a, b, n=1):
        nonlocal s
        assert s.count(a) == n, (a[:80], s.count(a))
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
    ld = {"@context": "https://schema.org", "@type": "WebPage", "@id": "https://paraglidingatlas.com/%s#webpage" % canon,
          "name": title, "url": "https://paraglidingatlas.com/" + canon, "description": desc,
          "isPartOf": {"@id": "https://paraglidingatlas.com/#website"}, "publisher": {"@id": "https://paraglidingatlas.com/#organization"},
          "inLanguage": "en", "dateModified": "2026-11-03"}
    rep("<!-- site-schema -->", '<script type="application/ld+json">%s</script>\n<style>%s</style>%s\n<!-- site-schema -->'
        % (json.dumps(ld, ensure_ascii=False), CSS, extra_head))
    rep('<a href="about.html" aria-current="page" class="is-here">About</a>', '<a href="about.html">About</a>')
    a, b = s.index('<main id="v4-main">'), s.index("</main>")
    s = s[:a] + '<main id="v4-main">\n' + main + "\n" + s[b:]
    rep('<a href="partners.html">Partner With Me</a>', '<a href="partners.html">Partner With Me</a>\n      <a href="media.html">Media</a>')
    rep("</body>", '<script defer src="../../newsletter.js?v=d28c01a5"></script>\n<script defer src="v4-media.js"></script>\n</body>')
    return s


def comp_cards():
    pv = sum(v[2] for v in V.values() if v[0] == "pwc")
    sv = sum(v[2] for v in V.values() if v[0] == "srs5")
    lv = sum(v[2] for v in V.values() if v[0] == "srs4")
    w, h = PH[CARD][:2]
    cards = [
        ('<a class="kit-card v2-tour" href="#newsletter">'
         '<div class="kit-card-media"><div class="md-next"><b>8 to 14 Nov</b><span>7 tasks &middot; 44 countries</span></div><span class="v2-tour-tag is-go">Next</span></div>'
         '<div class="kit-card-body"><span class="kit-meta">SRS Advance Edition &middot; Tapalpa, Mexico</span><h3>Tapalpa 2026</h3>'
         '<p class="md-did">Stills and daily highlight videos, from registration to the last task.</p>'
         '<dl class="v2-tour-facts"><div><dt>Tasks</dt><dd>8 to 14 Nov</dd></div><div><dt>Pilots</dt><dd>Up to 120</dd></div></dl>'
         '<span class="v2-more">Follow it day by day <i aria-hidden="true">&rarr;</i></span></div></a>'),
        ('<a class="kit-card v2-tour" href="media-srs-piedrahita-2026.html">'
         '<div class="kit-card-media"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy"></div>'
         '<div class="kit-card-body"><span class="kit-meta">SRS BGD Edition &middot; Piedrahita, Spain</span><h3>Piedrahita 2026</h3>'
         '<p class="md-did">Stills and daily highlight videos. 120 pilots from 54 countries.</p>'
         '<dl class="v2-tour-facts"><div><dt>Dates</dt><dd>22 to 29 Aug</dd></div><div><dt>Views</dt><dd>%s</dd></div></dl>'
         '<span class="v2-more">See the photos and videos <i aria-hidden="true">&rarr;</i></span></div></a>'
         % (src(CARD, 800), 800, round(800 * h / w), E(PH[CARD][3]), "{:,}".format(sv))),
        ('<a class="kit-card v2-tour" href="#watch" data-comp="srs4">'
         '<div class="kit-card-media"><img src="%s" width="1280" height="720" alt="The live broadcast from Monte Grappa" loading="lazy"><span class="v2-tour-tag">Live</span></div>'
         '<div class="kit-card-body"><span class="kit-meta">SRS Skywalk Bassano Edition &middot; Monte Grappa, Italy</span><h3>Bassano 2026</h3>'
         '<p class="md-did">Live commentary on YouTube, every task day, from the sky and the ground.</p>'
         '<dl class="v2-tour-facts"><div><dt>On air</dt><dd>21 h 42 min</dd></div><div><dt>Views</dt><dd>%s</dd></div></dl>'
         '<span class="v2-more">Watch the broadcasts <i aria-hidden="true">&rarr;</i></span></div></a>' % (thumb("ZL9B5eXip5o"), "{:,}".format(lv))),
        ('<a class="kit-card v2-tour" href="#watch" data-comp="pwc">'
         '<div class="kit-card-media"><img src="%s" width="1280" height="720" alt="Racing at the Super Final over Pegalajar" loading="lazy"></div>'
         '<div class="kit-card-body"><span class="kit-meta">15th Paragliding World Cup Super Final &middot; Pegalajar, Spain</span><h3>Pegalajar 2026</h3>'
         '<p class="md-did">A highlight video for each day of racing.</p>'
         '<dl class="v2-tour-facts"><div><dt>Videos</dt><dd>5</dd></div><div><dt>Views</dt><dd>%s</dd></div></dl>'
         '<span class="v2-more">Watch the highlights <i aria-hidden="true">&rarr;</i></span></div></a>' % (thumb("7il6yV1vdIc"), "{:,}".format(pv))),
    ]
    return "".join(cards)


def reel():
    items = []
    for v, (c, t, n, ln, d, ep) in V.items():
        items.append('<li data-comp="%s"><button type="button" data-vid="%s" data-date="%s"%s%s><img src="%s" alt="" width="320" height="180" loading="lazy">'
                     '<span><b>%s</b><small>%s &middot; %s</small></span></button></li>'
                     % (c, v, d, ' data-ep="episodes/%s.html"' % ep if ep else "", ' aria-current="true"' if v == REEL else "",
                        thumb(v, "mqdefault"), E(t), E(COMPS[c]), vmeta(v)))
    chips = ('<div class="v2-chips" role="group" aria-label="Show the videos from">'
             '<button class="v2-chip" type="button" aria-pressed="true" data-comp="">All <i>13</i></button>'
             '<button class="v2-chip" type="button" aria-pressed="false" data-comp="pwc">Pegalajar <i>5</i></button>'
             '<button class="v2-chip" type="button" aria-pressed="false" data-comp="srs5">Piedrahita <i>3</i></button>'
             '<button class="v2-chip" type="button" aria-pressed="false" data-comp="srs4">Bassano live <i>5</i></button></div>')
    c, t, n, ln, d, ep = V[REEL]
    return ('<div class="md-reel"><div class="md-main">%s<div class="md-now"><h3>%s</h3><p><span>%s</span> &middot; <span>%s</span>'
            '<span class="md-ep"> &middot; <a href="episodes/%s.html">Read the episode</a></span></p></div></div>'
            '<div class="md-side"><div class="md-side-in">%s<ul class="md-list">%s</ul></div></div></div>'
            % (frame(REEL), E("%s, %s" % (COMPS[c], t)), vmeta(REEL), d, ep, chips, "".join(items)))


def media_page():
    w, h = PH[HERO][:2]
    main = '''
<header class="kit-hero md-hero">
  <div class="kit-hero-media">
    <picture><source media="(max-aspect-ratio: 2/3)" srcset="%(hp)s"><img src="%(h)s" srcset="%(h8)s 800w, %(h)s 1600w, %(h24)s 2400w" sizes="100vw" width="%(w)d" height="%(hh)d" alt="%(alt)s" fetchpriority="high"></picture>
  </div>
  <div class="kit-hero-copy">
    <span class="kit-kicker">Media &middot; Covered for SRS and the PWC</span>
    <h1>From The Comps</h1>
    <p class="kit-intro">Daily highlight videos, live commentary and stills from paragliding's racing circuits, made at the comp and out the same day.</p>
    <div class="kit-actions"><a class="btn-solid" href="%(call)s" target="_blank" rel="noopener" data-hover><span>Book a Call</span></a><a class="btn-lines" href="#watch" data-hover>Watch the Highlights</a></div>
    <div class="kit-stats">
      <div class="kit-stat"><b>31,250</b><span>Views on 13 comp videos</span></div>
      <div class="kit-stat"><b>21h 42m</b><span>Live commentary</span></div>
      <div class="kit-stat"><b>3</b><span>Comps in 2026</span></div>
    </div>
  </div>
</header>

<section class="kit-band" id="watch">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">Showreel</span>
      <h2 class="kit-title">Watch The <em class="v2-accent">Highlights</em></h2>
      <p class="kit-intro">The most watched first: Task 1 of the Paragliding World Cup Super Final, an 86.5 km sprint, %(rv)s views. Tap any video to play it here.</p>
    </div>
    %(reel)s
  </div>
</section>

<section class="kit-band v2-topo" id="stills">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">Stills</span>
      <h2 class="kit-title">Selected Work</h2>
      <p class="kit-intro">From the air at SRS Piedrahita, August 2026. Every frame shown whole: tap one to see it full size and zoom in.</p>
    </div>
    %(grid)s
    <div class="kit-actions md-more"><a class="btn-lines" href="media-srs-piedrahita-2026.html" data-hover>All 20 from Piedrahita, by task</a></div>
  </div>
</section>

<section class="kit-band" id="comps">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">2026 Season</span>
      <h2 class="kit-title">The Comps</h2>
      <p class="kit-intro">Each one filmed and edited on site, published day by day.</p>
    </div>
    <div class="v2-tours md-comps">%(cards)s</div>
    <p class="md-swipe" aria-hidden="true">Swipe for more &rarr;</p>
  </div>
</section>

<section class="kit-band v2-topo" id="offer">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">What An Event Gets</span>
      <h2 class="kit-title">Before, During, <em class="v2-accent">After</em></h2>
      <p class="kit-intro">Four pieces across your event, published as joint posts on your channels and on Paragliding Atlas. Start with what your budget allows and add more as it grows, for one event or a whole season.</p>
    </div>
    <ol class="md-four">
      <li><span class="md-when">Before the race</span><h3>Pre-Race Show</h3><p>A Paragliding Atlas podcast episode previewing the venue and its conditions, to build anticipation with pilots and audiences.</p><p class="md-eg">Example: <a href="episodes/pre-pwc-kenya-nikolay-yotov.html">Pre PWC Kenya, with Nikolay Yotov</a></p></li>
      <li><span class="md-when">Every task day</span><h3>Daily Highlights</h3><p>A video each day showing the task, the results, the race dynamics and what made the day special, with social clips and a results newsletter.</p><p class="md-eg">Example: <a href="#watch">Task 1 at the Super Final</a></p></li>
      <li><span class="md-when">After the race</span><h3>Aftermovie</h3><p>A highlights compilation of the whole event: task details, racing strategies, leaderboard standings and the fun of the week.</p></li>
      <li><span class="md-when">Between races</span><h3>Race Behind The Race</h3><p>Behind the scenes and athlete showreels: what it takes to organise a comp, and a deeper connection between audiences, athletes and organisers.</p></li>
    </ol>
    <div class="md-also">
      <div class="kit-panel"><h3>Live commentary</h3><p>The whole task live on YouTube, as at SRS Bassano: five broadcasts, 21 hours 42 minutes on air.</p></div>
      <div class="kit-panel"><h3>Stills</h3><p>Photographs from the air and the ground, as at SRS Piedrahita, delivered as web and full-size files.</p></div>
      <div class="kit-panel"><h3>When it arrives</h3><p>The same day or at the end of the week, as you need. Daily timing depends on the internet on site, when the task finishes and access to footage.</p></div>
    </div>
  </div>
</section>

<section class="kit-band" id="how">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">How It Works</span>
      <h2 class="kit-title">Three Steps To Your Coverage</h2>
    </div>
    <ol class="md-steps">
      <li><small aria-hidden="true">01</small><b>A call</b><p>Thirty minutes, free: your event, its dates, its place and what you would like to come out of it.</p></li>
      <li><small aria-hidden="true">02</small><b>A plan</b><p>Which pieces, when each goes out and on which channels, within your budget.</p></li>
      <li><small aria-hidden="true">03</small><b>At the comp</b><p>I film, photograph and edit on site, and deliver day by day.</p></li>
    </ol>
  </div>
</section>

<section class="kit-band v2-topo" aria-label="A word from the comps">
  <div class="kit-in">
    <blockquote class="md-quote"><p><i class="v2-tbd">[to supply]</i> A word from an organiser or a pilot.</p><footer><i class="v2-tbd">[to supply]</i></footer></blockquote>
  </div>
</section>

%(cta)s
<div id="newsletter"></div>
%(nl)s
%(viewer)s
''' % dict(hp=src(HERO_P, 1600), h=src(HERO, 1600), h8=src(HERO, 800), h24=src(HERO, 2400), w=1600, hh=round(1600 * h / w),
           alt=E(PH[HERO][3]), call=CALL, rv="{:,}".format(V[REEL][2]), reel=reel(),
           grid=grid(SELECT, "Selected stills from SRS Piedrahita 2026"), cards=comp_cards(),
           cta=cta("Book A Free <span class=\"v4-nw\">30-Minute</span> Call About Your Event", "Coverage For Your Comp",
                   "Tell me the event, the dates and the place, and what you would like to come out of it. Season coverage too."),
           nl=NEWSLETTER, viewer=VIEWER)
    return shell("Media", "Comp coverage by Paragliding Atlas: daily highlight videos, live commentary and stills from the 2026 SRS races and the Paragliding World Cup Super Final.",
                 "media.html", src(HERO, 1600), "Media", main)


def piedrahita_page():
    days = [("Day 1", "Registration, the pilots and the Peñas de Piedrahíta fiesta", "cuGs7Lk6Dt4", 0, None),
            ("Task 1", "59 km, humid air, a 2,100 m ceiling and a long leg into a westerly wind", "uCEfssE40u8", 1, None),
            ("Task 2", "75 km, and a flatland gamble that cut the course short", "NXUEyPQ3V4E", 2, None),
            ("Task 3", "The race from the air", None, 3, None)]
    out = []
    for k, (lab, line, v, t, _) in enumerate(days):
        stems = [s for s in PH if PH[s][2] == t] if t else []
        vid = ""
        if v:
            vid = ('%s<div class="md-now"><h3>%s</h3><p>%s &middot; %s &middot; <a href="episodes/%s.html">Read the episode</a></p></div>'
                   % (frame(v), E("Piedrahita, " + V[v][1]), vmeta(v), V[v][4], V[v][5]))
        out.append('<section class="kit-band md-day%s" id="%s"><div class="kit-in"><div class="kit-head"><span class="kit-kicker">%s</span>'
                   '<h2 class="kit-title">%s</h2></div>%s%s</div></section>'
                   % (" v2-topo" if k % 2 else "", lab.lower().replace(" ", "-"), lab, E(line), vid,
                      grid(stems, "Stills from %s" % lab) if stems else ""))
    w, h = PH["SRS_5_T3_63"][:2]
    main = '''
<header class="kit-hero md-hero">
  <div class="kit-hero-media">
    <picture><source media="(max-aspect-ratio: 2/3)" srcset="%(hp)s"><img src="%(h)s" srcset="%(h8)s 800w, %(h)s 1600w, %(h24)s 2400w" sizes="100vw" width="1600" height="%(hh)d" alt="%(alt)s" fetchpriority="high"></picture>
  </div>
  <div class="kit-hero-copy">
    <a class="md-back" href="media.html">&larr; Media</a>
    <span class="kit-kicker">SRS BGD Edition &middot; Piedrahita, Ávila, Spain</span>
    <h1>Piedrahita 2026</h1>
    <p class="kit-intro">22 to 29 Aug 2026, FAI Category 2: 120 pilots from 54 countries. Stills and a highlight video each day.</p>
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
''' % dict(hp=src("SRS_5_T2_133-2", 1600), h=src("SRS_5_T3_63", 1600), h8=src("SRS_5_T3_63", 800), h24=src("SRS_5_T3_63", 2400),
           hh=round(1600 * h / w), alt=E(PH["SRS_5_T3_63"][3]), days="\n".join(out),
           cta=cta("Coverage Like This For <span class=\"v4-nw\">Your Event</span>", "Coverage For Your Comp",
                   "A free 30-minute call: tell me the event, the dates and the place, and what you would like to come out of it."),
           viewer=VIEWER)
    return shell("Piedrahita 2026", "SRS BGD Edition, Piedrahita, Spain, 22 to 29 Aug 2026: the stills and daily highlight videos by Paragliding Atlas.",
                 "media-srs-piedrahita-2026.html", src("SRS_5_T3_63", 1600), "Piedrahita 2026", main)


if __name__ == "__main__":
    for name, page in (("media.html", media_page()), ("media-srs-piedrahita-2026.html", piedrahita_page())):
        assert "—" not in page.split("<main")[1], "an em dash in " + name
        open(os.path.join(V4, name), "w").write(page)
        print("wrote prototypes/v4/" + name, len(page))
