"""Packing-kit items (destinations): is the focus ring visible, or clipped by .kkit-gbody{overflow:hidden}?
Screenshot focused vs blurred and count orange ring pixels.
python3 probe_kit.py [page] [vp]"""
import sys, os, io, json
sys.path.insert(0, "/home/user/Website/tools/stress")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, keyboard as K
from PIL import Image
page = sys.argv[1] if len(sys.argv) > 1 else "destinations/kenya.html"
vp = sys.argv[2] if len(sys.argv) > 2 else "desktop"
HERE = os.path.dirname(os.path.abspath(__file__))
def orange(img):
    return sum(1 for p in img.getdata() if p[0] > 200 and 90 < p[1] < 150 and p[2] < 70)
with lib.server(K.PORT) as base, lib.browser() as b:
    ctx = K.new_ctx(b, base, K.VPS[vp]); pg = K.load(ctx, base, page)
    out = []
    for n in range(400):
        pg.keyboard.press("Tab"); pg.wait_for_timeout(30)
        if pg.evaluate("() => document.activeElement.classList.contains('kkit-item')"): break
    for k in range(3):
        if k: pg.keyboard.press("Tab")
        pg.wait_for_timeout(700)
        info = pg.evaluate("""() => { const e=document.activeElement, r=e.getBoundingClientRect(), c=e.closest('.kkit-gbody'), q=c.getBoundingClientRect(), cs=getComputedStyle(e);
            return {d: __kb.desc(e), text: e.innerText.trim().slice(0,30), fv: e.matches(':focus-visible'), outline: cs.outlineStyle+' '+cs.outlineWidth+' offset '+cs.outlineOffset,
                    el: [r.left, r.top, r.right, r.bottom].map(Math.round), body: [q.left, q.top, q.right, q.bottom].map(Math.round), body_overflow: getComputedStyle(c).overflow,
                    body_inline_height: c.style.height}; }""")
        x0, y0, x1, y1 = info["el"]
        clip = {"x": max(0, x0 - 8), "y": max(0, y0 - 8), "width": x1 - x0 + 16, "height": y1 - y0 + 16}
        a = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        a.save(os.path.join(HERE, "shots", "kit_%s_%d_focused.png" % (vp, k)))
        pg.evaluate("() => { window.__f = document.activeElement; document.activeElement.blur(); }"); pg.wait_for_timeout(400)
        bimg = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.keyboard.press("Shift"); pg.evaluate("() => window.__f.focus()"); pg.wait_for_timeout(200)
        info["orange_px_focused"] = orange(a); info["orange_px_blurred"] = orange(bimg)
        info["ring_px_expected_min"] = 2 * 2 * ((x1 - x0) + (y1 - y0))
        out.append(info)
    print(json.dumps(out, indent=1))
