#!/usr/bin/env python3
"""
Before and after: the same screen in v2 and in v4, side by side, as JPG in
docs/v4-shots/ (the report's pictures; docs/v4-plan.md step 8). Needs the
preview server (python3 -m http.server 8765 --bind 127.0.0.1).

    python3 tools/v4_before_after.py
"""
import io
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "v4-shots")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
BASE = "http://127.0.0.1:8765/prototypes/%s/"
# name, page, width (390 = a touch phone), scroll to (a selector, or none), action
PAIRS = [
    ("home", "index.html", 1440, None, None),
    ("india-phone", "destinations/india.html", 390, None, None),
    ("kenya", "destinations/kenya.html", 1440, None, None),
    ("library", "library.html", 1440, None, None),
    ("kb-flight-mechanics", "knowledge-base/flight-mechanics.html", 1440, None, None),
    ("kb-figure", "knowledge-base/risk-vs-reward.html", 1440, ".band-draw", None),
    ("episode", "episodes/navigating-india-eddie-colfox.html", 1440, None, None),
    ("menu-phone", "index.html", 390, None, "menu"),
]


def shot(b, site, page, w, sel, action):
    phone = w == 390
    ctx = b.new_context(viewport={"width": w, "height": 844 if phone else 900}, is_mobile=phone, has_touch=phone,
                        device_scale_factor=2 if phone else 1)
    pg = ctx.new_page()
    pg.goto(BASE % site + page, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(1500)
    if sel:
        pg.evaluate("document.querySelectorAll('details').forEach(function(d){d.open=true})")
        el = pg.locator(sel).first
        el.scroll_into_view_if_needed()
        pg.evaluate("window.scrollBy(0, -120)")
        pg.wait_for_timeout(2800)
    if action == "menu":
        pg.locator(".nav-toggle").first.click()
        pg.wait_for_timeout(1500)
    png = pg.screenshot()
    ctx.close()
    return Image.open(io.BytesIO(png)).convert("RGB")


def label(im, text):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except OSError:
        f = ImageFont.load_default()
    d.rectangle([0, 0, 90, 40], fill=(255, 117, 23))
    d.text((14, 7), text, fill=(20, 21, 25), font=f)
    return im


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    total = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for name, page, w, sel, action in PAIRS:
            a = label(shot(b, "v2", page, w, sel, action), "v2")
            c = label(shot(b, "v4", page, w, sel, action), "v4")
            h = max(a.height, c.height)
            gap = 24
            S = Image.new("RGB", (a.width + c.width + gap, h), (40, 40, 44))
            S.paste(a, (0, 0))
            S.paste(c, (a.width + gap, 0))
            if S.width > 1800:
                S = S.resize((1800, round(S.height * 1800 / S.width)), Image.LANCZOS)
            fp = os.path.join(OUT, name + ".jpg")
            S.save(fp, quality=80, optimize=True, progressive=True)
            total += os.path.getsize(fp)
            print("%-22s %4d KB" % (name, os.path.getsize(fp) // 1024))
        b.close()
    print("v4 shots: %.1f MB in docs/v4-shots/" % (total / 1048576))


if __name__ == "__main__":
    main()
