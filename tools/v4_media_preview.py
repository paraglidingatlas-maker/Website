#!/usr/bin/env python3
"""Media: pack the two built pages into one claude.ai preview (chat 17, 3 Nov 2026).

prototypes/ is not served live since go-live, so the owner previews in a claude.ai artifact. This copies
prototypes/v4/media.html and media-srs-piedrahita-2026.html (built by tools/v4_media.py with
--media img/media-tmp/) into OUT_DIR with every file they use beside them under flat names: the site's CSS, JS,
fonts and logo, the photos, and the YouTube stills (an artifact can load nothing from other hosts). Links to
other site pages point at paraglidingatlas.com. An artifact cannot show a YouTube player, so in the preview a
video's play button opens it on YouTube; on the site it plays in place.

    python3 tools/v4_media.py --media img/media-tmp/
    python3 tools/v4_media_preview.py OUT_DIR
"""
import hashlib
import os
import re
import shutil
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
PAGES = ["media.html", "media-srs-piedrahita-2026.html"]
done = {}


def flat(path):
    """a local file under the repo -> its flat name in OUT (copied, CSS rewritten)"""
    path = os.path.normpath(path)
    if path in done:
        return done[path]
    base = os.path.basename(path)
    name = base if base not in done.values() else hashlib.md5(path.encode()).hexdigest()[:6] + "-" + base
    done[path] = name
    if path.endswith(".css"):
        css = open(path).read()
        d = os.path.dirname(path)
        css = re.sub(r'url\((["\']?)(?!data:|https?:|#)([^)"\'?#]+)([^)"\']*)\1\)',
                     lambda m: "url(%s%s%s)" % (m.group(1), flat(os.path.join(d, m.group(2))) if os.path.exists(os.path.join(d, m.group(2))) else m.group(2), m.group(1)), css)
        open(os.path.join(OUT, name), "w").write(css)
    else:
        shutil.copy(path, os.path.join(OUT, name))
    return name


def yt(url):
    name = "yt-" + url.split("/vi/")[1].replace("/", "-")
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        with urllib.request.urlopen(url) as r:
            open(p, "wb").write(r.read())
    return name


def fix(u):
    u0 = u
    if u.startswith("https://i.ytimg.com/"):
        return yt(u)
    if u.startswith(("http:", "https:", "#", "mailto:", "tel:", "data:", "javascript:")) or not u:
        return u
    path, _, rest = u.partition("?")
    path, _, frag = path.partition("#")
    if path in PAGES:
        return u
    full = os.path.normpath(os.path.join(V4, path))
    if path.endswith(".html") or os.path.isdir(full):
        rel = os.path.relpath(full, V4) if full.startswith(V4) else os.path.relpath(full, ROOT)
        return "https://paraglidingatlas.com/" + rel + ("?" + rest if rest else "") + ("#" + frag if frag else "")
    if os.path.exists(full):
        return flat(full)
    print("missing", u0)
    return u


for pg in PAGES:
    h = open(os.path.join(V4, pg)).read()
    h = re.sub(r'<script defer src="pwa\.js[^"]*"></script>', "", h)
    h = re.sub(r'<link rel="manifest"[^>]*>', "", h)
    h = re.sub(r'\b(src|href|data-full|data-ep)="([^"]*)"', lambda m: '%s="%s"' % (m.group(1), fix(m.group(2))), h)
    h = re.sub(r'\bsrcset="([^"]*)"', lambda m: 'srcset="%s"' % ", ".join(
        " ".join([fix(x.split()[0])] + x.split()[1:]) for x in m.group(1).split(",") if x.strip()), h)
    # the preview cannot show a YouTube player: the play buttons open YouTube, and the list's stills are local
    h = h.replace("<html lang=\"en\">", "<html lang=\"en\" data-md-out>", 1)
    h = h.replace("<title>", "<title>Preview: ", 1)
    open(os.path.join(OUT, pg), "w").write(h)
# the list swaps the big still by video id: keep those local too
js = open(os.path.join(OUT, done[os.path.normpath(os.path.join(V4, "v4-media.js"))])).read()
js = js.replace('img.src = "https://i.ytimg.com/vi/" + v + "/maxresdefault.jpg";', 'img.src = "yt-" + v + "-maxresdefault.jpg";')
open(os.path.join(OUT, "v4-media.js"), "w").write(js)
for v in re.findall(r'data-vid="([^"]+)"', open(os.path.join(OUT, PAGES[0])).read()):
    yt("https://i.ytimg.com/vi/%s/maxresdefault.jpg" % v)
print(len(os.listdir(OUT)), "files in", OUT)
