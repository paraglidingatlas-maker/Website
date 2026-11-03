#!/usr/bin/env python3
"""The expeditions page on phones, preview only (chat 16, 3 Nov 2026).

The owner (3 Nov): on a phone expeditions.html "doesn't have any animation that comes up in the desktop view,
and looks an oddly designed broken page". This writes one preview, samples/expeditions-phone/index.html, from
the built prototypes/v4/expeditions.html: the same page, with the desktop's flight switched on below 1000 px
in a phone shape. One window at the top of the screen is the camera (the map flies place to place, the route
draws, each photograph rises out of its ring through the air dissolve); the words of each stop sit on plain
dark at the foot, so nothing moves behind reading text. Reduced motion and no script keep the still journey.
Desktop is unchanged. When the owner says yes, these changes move into tools/v4_expeditions.py.

    python3 tools/v4_expeditions_phone_preview.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v4_expeditions_phone import phone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "prototypes", "v4", "expeditions.html")
out = os.path.join(ROOT, "prototypes", "v4", "samples", "expeditions-phone", "index.html")
h = open(src).read()
if "ex-phone" not in h:
    h = phone(h)
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:80], h.count(a)); h = h.replace(a, b)
# a preview one folder deep: resolve the page's relative addresses from prototypes/v4 as before
SKIP = ("http:", "https:", "#", "/", "mailto:", "tel:", "data:", "javascript:", "{")
def up(u):
    u = u.strip()
    return u if not u or u.startswith(SKIP) else "../../" + u
def attr(m):
    return '%s="%s"' % (m.group(1), up(m.group(2)))
h = re.sub(r'\b(src|href|poster)="([^"]*)"', attr, h)
h = re.sub(r'\b(srcset)="([^"]*)"', lambda m: '%s="%s"' % (m.group(1), ", ".join(
    " ".join([up(x.split()[0])] + x.split()[1:]) for x in m.group(2).split(",") if x.strip())), h)
h = re.sub(r'url\((["\']?)(?!data:|http|/|#)([^)"\']+)\1\)', lambda m: "url(%s../../%s%s)" % (m.group(1), m.group(2), m.group(1)), h)
h = re.sub(r'(&quot;(?:src|srcset|phone|href)&quot;:&quot;)(?!http|/|#)', r'\1../../', h)
h = re.sub(r'href="(#[^"]*)"', r'href="\1"', h)
h = h.replace("<title>", "<title>Phone preview: ", 1)
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w").write(h)
print("wrote", os.path.relpath(out, ROOT), len(h))
