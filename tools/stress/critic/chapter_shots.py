"""Screenshots + reader's-eye text for: click chapter in rail -> 'Continue reading'.
python3 chapter_shots.py [episode path] [chapter href]"""
import sys, os
sys.path.insert(0, "/home/user/Website/tools/stress"); import lib
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else "episodes/sky-gods-flying-8000ers-antoine-girard.html"
href = sys.argv[2] if len(sys.argv) > 2 else "#c8"
TOPTEXT = """() => { const ys=[60,200,400]; return ys.map(y => { const e=document.elementFromPoint(innerWidth/2,y);
  const b=e&&e.closest('.cd-block'); return (b?b.id+': ':'')+(e?e.textContent.trim().replace(/\\s+/g,' ').slice(0,70):''); }); }"""
with lib.server(8895) as base, lib.browser() as b:
    for mode, kw in (("phone", dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)),
                     ("desktop", dict(viewport={"width": 1280, "height": 800}))):
        ctx = b.new_context(**kw)
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(800)
        pg.locator('.cd-chap[href="%s"]' % href).first.click(); pg.wait_for_timeout(1400)
        st = pg.evaluate("() => { const c=document.getElementById('transcript-body'); return {clipScrollTop:c.scrollTop, scrollY:scrollY, more:document.querySelector('.cd-more').textContent.trim().replace(/\\s+/g,' ')}; }")
        print(mode, "after chapter click", st, pg.evaluate(TOPTEXT))
        # try to scroll inside the clip with wheel / touch-like scroll: does the reader get further?
        c = pg.locator('#transcript-body').bounding_box()
        pg.mouse.move(c['x'] + c['width'] / 2, c['y'] + 200)
        before = pg.evaluate("document.getElementById('transcript-body').scrollTop")
        pg.mouse.wheel(0, 600); pg.wait_for_timeout(500)
        after = pg.evaluate("[document.getElementById('transcript-body').scrollTop, scrollY]")
        print(mode, "wheel over clip: clip scrollTop", before, "->", after[0], "page scrollY ->", after[1])
        pg.evaluate("document.getElementById('transcript-body').scrollIntoView({block:'start'})")
        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(HERE, "shots", "chapter_%s_1_after_click.png" % mode))
        pg.locator(".cd-more").first.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
        pg.locator(".cd-more").first.click(); pg.wait_for_timeout(1200)
        tgt = pg.evaluate("(h) => { const t=document.getElementById(h.slice(1)).getBoundingClientRect(); return {targetTop: Math.round(t.top), scrollY, clipScrollTop: document.getElementById('transcript-body').scrollTop}; }", href)
        print(mode, "after Continue reading", tgt, pg.evaluate(TOPTEXT))
        pg.screenshot(path=os.path.join(HERE, "shots", "chapter_%s_2_after_continue.png" % mode))
        ctx.close()
