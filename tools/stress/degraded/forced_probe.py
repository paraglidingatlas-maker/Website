#!/usr/bin/env python3
"""forced-colors: active check on specific drawings/controls: element crops + ink (97th pct contrast vs dominant colour).
usage: python3 forced_probe.py        Port 8814. Read-only on the repo. Crops go to out/forced/.
"""
import io
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lib  # noqa: E402
from degraded import new_ctx, goto, ink  # noqa: E402

CASES = [  # page, selector, viewport width, what it shows
    ("index.html", ".skill-meter", 1280, "skill level meter (4 of 5 filled on Bir)"),
    ("index.html", ".nav-toggle", 390, "phone menu button"),
    ("destinations/india.html", ".cfl-dots", 1280, "gallery pager buttons"),
    ("destinations/india.html", "svg.iroute-svg", 1280, "route drawing with place labels"),
    ("destinations/kenya.html", ".cfl-dots", 1280, "gallery pager buttons"),
    ("episodes/sky-gods-flying-8000ers-antoine-girard.html", ".nav-toggle", 390, "phone menu button"),
]
OUT = os.path.join(HERE, "out", "forced")
os.makedirs(OUT, exist_ok=True)


def main():
    import numpy as np
    from PIL import Image
    with lib.server(8814) as base:
        with lib.browser() as b:
            for page, sel, w, what in CASES:
                row = []
                for mode, kw in (("normal", {}), ("forced-dark", dict(forced_colors="active", color_scheme="dark")),
                                 ("forced-light", dict(forced_colors="active", color_scheme="light"))):
                    ctx = new_ctx(b, base, reduced_motion="reduce", viewport={"width": w, "height": 900 if w > 500 else 844},
                                  is_mobile=w < 500, has_touch=w < 500, **kw)
                    pg = ctx.new_page()
                    goto(pg, base + page)
                    time.sleep(0.8)
                    loc = pg.locator(sel).first
                    try:
                        loc.scroll_into_view_if_needed(timeout=3000)
                        time.sleep(0.5)
                        png = loc.screenshot(timeout=5000)
                    except Exception as e:
                        row.append("%s: ERR %s" % (mode, str(e)[:60]))
                        ctx.close()
                        continue
                    im = Image.open(io.BytesIO(png)).convert("RGB")
                    im.save(os.path.join(OUT, "%s__%s__%s.png" % (page.replace("/", "_"), sel.strip(".").replace(" ", "_"), mode)))
                    a = np.asarray(im)
                    row.append("%s ink=%s" % (mode, ink(a, (0, 0, a.shape[1], a.shape[0]))))
                    ctx.close()
                print("%-55s %-16s %4dpx %-40s %s" % (page, sel, w, what, " | ".join(row)))


if __name__ == "__main__":
    main()
