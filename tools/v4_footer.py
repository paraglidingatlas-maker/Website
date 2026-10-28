#!/usr/bin/env python3
"""
The footer, shorter (owner, 28 Oct 2026). Same pages reachable, less height:
  - three menus of four, side by side with the brand: Listen (Podcast, Episode Library, Topics, Knowledge Base),
    Fly With Us (Kenya, India, Panchgani, Book a Call), Atlas (About, Mission, Partner With Me, Safety & Disclosure);
    gone as repeats: the motto's link (Mission is in Atlas), "Destinations" (Expeditions is in the menu bar, the
    three trips are listed), "All Episodes" beside "Podcast" (now Episode Library), "Enquire" (the menu bar's
    button);
  - the address in two lines, complete;
  - above the line: "Listen on" at the left, "(c) Paragliding Atlas" at the right; below it, one line on a
    desktop: the platforms at the left, the legal pages (Terms, Privacy, Cookies, Participant Agreement,
    Corrections, Sitemap) at the right;
  - no wind sound (owner); the footage pages' pause button, which sat beside it, keeps its place at the head of
    the "Listen on" row (src/v4-ux-footage.js), since moving pictures need a way to stop.
The look is in src/v2.css (FOOTER, shorter). Written between <!--v4f--> marks in place of the footer's own
content on every v4 page, links kept relative to each page. Run by tools/v4_build.py before tools/v4_loader.py.

    python3 tools/v4_footer.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
MARK = ("<!--v4f-->", "<!--/v4f-->")
CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
LISTEN_ON = [
    ("YouTube", "https://www.youtube.com/@ParaglidingAtlas"),
    ("Apple Podcasts", "https://podcasts.apple.com/us/podcast/paragliding-atlas-by-aninder-singh/id1735782803"),
    ("Spotify", "https://open.spotify.com/show/16jBM3RfjVERukNHJrIRec"),
    ("Castbox", "https://castbox.fm/channel/Paragliding-Atlas-by-Aninder-Singh-id6075445"),
    ("Podbean", "https://www.podbean.com/podcast-detail/tb6yq-2f5cd4/Paragliding-Atlas-by-Aninder-Singh-Podcast"),
    ("Patreon", "https://www.patreon.com/cw/ParaglidingAtlas"),
    ("Instagram", "https://www.instagram.com/anindersingh13"),
]
MENUS = [
    ("Listen", [("Podcast", "podcast.html"), ("Episode Library", "library.html"), ("Topics", "tags.html"), ("Knowledge Base", "knowledge-base.html")]),
    ("Fly With Us", [("Kenya", "destinations/kenya.html"), ("India", "destinations/india.html"), ("Panchgani", "destinations/panchgani.html"), ("Book a Call", CALL)]),
    ("Atlas", [("About", "about.html"), ("Mission", "mission.html"), ("Partner With Me", "partners.html"), ("Safety &amp; Disclosure", "safety-and-disclosure.html")]),
]
LEGAL = [("Terms", "terms.html"), ("Privacy", "privacy-policy.html"), ("Cookies", "cookie-policy.html"),
         ("Participant Agreement", "participant-agreement.html"), ("Corrections", "corrections.html"), ("Sitemap", "sitemap.html")]


def link(label, href, up):
    if href.startswith("http"):
        return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, label)
    return '<a href="%s%s">%s</a>' % (up, href, label)


def footer(up, logo):
    cols = "".join('\n    <div class="footer-col">\n      <h2>%s</h2>\n      %s\n    </div>' % (h, "\n      ".join(link(l, u, up) for l, u in items))
                   for h, items in MENUS)
    return ('\n  <div class="footer-content v4f-on">\n  <div class="footer-top">\n    <div class="footer-col footer-brand">\n      %s\n'
            '      <p class="footer-tagline">Touch The Sky With Glory</p>\n'
            '      <p class="footer-addr">Paragliding Atlas · Org. nr 937116934<br>Olav Troviks Vei M 46, 0864 Oslo, Norway</p>\n    </div>%s\n  </div>\n'
            '  <div class="v4f-k"><span class="footer-listen-label">Listen on</span><span>© Paragliding Atlas <span data-year>2026</span></span></div>\n'
            '  <div class="footer-bottom v4f">\n    <div class="v4f-ls">%s</div>\n    <div class="v4f-lg">%s</div>\n  </div>\n  </div>\n'
            % (logo, cols, "".join(link(l, u, "") for l, u in LISTEN_ON), "".join(link(l, u, up) for l, u in LEGAL)))


def main():
    n = 0
    for path in sorted(glob.glob(os.path.join(V4, "**", "*.html"), recursive=True)):
        src = open(path, encoding="utf-8").read()
        m = re.search(r"<footer[^>]*>(.*?)</footer>", src, re.S)
        if not m:
            continue
        inner = m.group(1)
        if MARK[0] in inner:
            inner = inner[inner.index(MARK[0]) + len(MARK[0]):inner.index(MARK[1])]
        logo = re.search(r'<a href="[^"]*"[^>]*class="wordmark".*?</a>', inner, re.S)
        if not logo or "footer-top" not in inner:
            continue
        up = re.match(r'<a href="((?:\.\./)*)', logo.group(0)).group(1)
        new = MARK[0] + footer(up, logo.group(0)) + MARK[1] + "\n"
        out = src[:m.start(1)] + new + src[m.end(1):]
        if out != src:
            open(path, "w", encoding="utf-8").write(out)
        n += 1
    print("v4 footer: the shorter footer on %d pages" % n)


if __name__ == "__main__":
    main()
