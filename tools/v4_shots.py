#!/usr/bin/env python3
"""
Viewport screenshots of prototype pages, walking down the page, at the phone
(390 x 844, touch, scale 2) and desktop (1440 x 900) widths. Full-page shots
miss the fade-ins and the sticky parts, so this scrolls one screen at a time
and waits for the page to settle.

    python3 tools/v4_shots.py --site v4 index.html destinations/india.html
    python3 tools/v4_shots.py --site v4 --screens 3 --out DIR index.html
    python3 tools/v4_shots.py --site v4 --full index.html   # one full-page shot too
    python3 tools/v4_shots.py --site v4 --only phone index.html
    python3 tools/v4_shots.py --site v4 --jpg index.html     # JPG (for the report)

Needs the preview server (python3 -m http.server 8765 --bind 127.0.0.1).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DEFAULT_OUT = "/tmp/claude-0/shots"


def sheet(files, out, kind):
    """The screens side by side, small, in reading order (rows of 4 or 5)."""
    from PIL import Image
    ims = [Image.open(f).convert("RGB") for f in files]
    w = 360 if kind == "phone" else 640
    ims = [im.resize((w, int(im.height * w / im.width))) for im in ims]
    cols = 5 if kind == "phone" else 3
    rows = (len(ims) + cols - 1) // cols
    h = max(im.height for im in ims)
    pad = 8
    S_ = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + pad) + pad), (60, 60, 60))
    for i, im in enumerate(ims):
        S_.paste(im, (pad + (i % cols) * (w + pad), pad + (i // cols) * (h + pad)))
    S_.save(out, quality=80)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="+")
    ap.add_argument("--screens", type=int, default=6, help="viewport shots per page and width (0: all)")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--only", choices=("phone", "desktop"))
    ap.add_argument("--jpg", action="store_true")
    ap.add_argument("--reduced", action="store_true", help="prefers-reduced-motion")
    ap.add_argument("--nojs", action="store_true")
    ap.add_argument("--live", action="store_true", help="shoot the live page instead of the prototype")
    ap.add_argument("--at", type=int, default=None, help="scroll to this y first")
    ap.add_argument("--sheet", action="store_true", help="also one contact sheet per page and width")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    os.makedirs(a.out, exist_ok=True)
    base = "http://127.0.0.1:8765/" + ("" if a.live else S.URL_PATH)
    ext = "jpg" if a.jpg else "png"
    kinds = [("phone", dict(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True, device_scale_factor=2)),
             ("desktop", dict(viewport={"width": 1440, "height": 900}))]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()
        for kind, opts in kinds:
            if a.only and a.only != kind:
                continue
            if a.reduced:
                opts = dict(opts, reduced_motion="reduce")
            if a.nojs:
                opts = dict(opts, java_script_enabled=False)
            ctx = b.new_context(**opts)
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
            for rel in a.pages:
                errs.clear()
                pg.goto(base + rel, wait_until="load", timeout=45000)
                pg.wait_for_timeout(900)
                stem = ("live-" if a.live else S.NAME + "-") + rel.replace("/", "__").rsplit(".", 1)[0].replace("#", "_") + "-" + kind
                h = pg.evaluate("document.documentElement.scrollHeight")
                vh = opts["viewport"]["height"]
                n = (h + vh - 1) // vh if a.screens == 0 else a.screens
                y0 = a.at or 0
                shot_files = []
                for i in range(n):
                    y = y0 + i * vh
                    if y >= h:
                        break
                    pg.evaluate("y => window.scrollTo(0, y)", y)
                    pg.wait_for_timeout(700)
                    fn = os.path.join(a.out, "%s-%02d.%s" % (stem, i, ext))
                    pg.screenshot(path=fn, **({"type": "jpeg", "quality": 78} if a.jpg else {}))
                    shot_files.append(fn)
                if a.sheet and shot_files:
                    sheet(shot_files, os.path.join(a.out, stem + "-sheet.jpg"), kind)
                if a.full:
                    pg.evaluate("window.scrollTo(0, 0)")
                    pg.wait_for_timeout(300)
                    pg.screenshot(path=os.path.join(a.out, "%s-full.%s" % (stem, ext)), full_page=True,
                                  **({"type": "jpeg", "quality": 70} if a.jpg else {}))
                over = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                print("%-8s %-45s height %6d  overflow %d  errors %s" % (kind, rel, h, over, errs[:2] or 0))
            ctx.close()
        b.close()


if __name__ == "__main__":
    main()
