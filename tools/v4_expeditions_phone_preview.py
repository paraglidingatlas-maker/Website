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
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "prototypes", "v4", "expeditions.html")
out = os.path.join(ROOT, "prototypes", "v4", "samples", "expeditions-phone", "index.html")
h = open(src).read()

def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:80], h.count(a)); h = h.replace(a, b)
# 1 the early switch: phones fly too (still under reduced motion)
rep('if(m("(min-width: 1000px) and (min-height: 620px)").matches&&',
    'if((m("(min-width: 1000px) and (min-height: 620px)").matches||m("(max-width: 999px)").matches)&&')
rep('r.classList.add("ex-fly");', 'r.classList.add("ex-fly");if(m("(max-width: 999px)").matches)r.classList.add("ex-phone");')
# 2 the script
rep('var mqWide = w.matchMedia("(min-width: 1000px) and (min-height: 620px)");',
    'var mqWide = w.matchMedia("(min-width: 1000px) and (min-height: 620px), (max-width: 999px)"); var PH = w.matchMedia("(max-width: 999px)");')
rep('    step = Math.max(1, (atlas.offsetHeight - H) / (N - 1 + HOLD));',
    '''    if (PH.matches) {   /* phone: the camera works in the top window; the words own the foot */
      regs = S.map(function (s, i) {
        if (i === 0) return [-.06, 1.06, .02, .62];
        if (i === 1) return [.03, .97, .1, .34];
        if (i === N - 1) return [.03, .97, .12, .4];
        return s.reg[0] > .5 ? [.12, .88, .12, .40] : [.2, .8, .14, .40];
      });
      panelR = 0;
    }
    step = Math.max(1, (atlas.offsetHeight - H) / (N - 1 + HOLD));''')
rep('  function photoRect(pl) {\n', '  function photoRect(pl) {\n    if (PH.matches) return [0, 0, W, Math.round(H * .58)];\n')
rep("var y = (j + .5) / MH * rh, my = pk ? 1 : ss(0, rh * .26, y) * ss(0, rh * .3, rh - y);",
    "var y = (j + .5) / MH * rh, my = pk ? 1 : PH.matches ? ss(0, rh * .12, y) * ss(0, rh * .34, rh - y) : ss(0, rh * .26, y) * ss(0, rh * .3, rh - y);")
rep("m = pk ? my : my * ss(0, rw * .5, x);", "m = pk ? my : PH.matches ? my * ss(0, rw * .1, x) * ss(0, rw * .1, rw - x) : my * ss(0, rw * .5, x);")
# 3 the phone layout
css = '''<style>
/* phone flight (preview): one window at the top where the camera flies and the photographs rise;
   the words sit on plain dark at the foot, nothing moves behind them */
.ex-phone .ex-atlas{height:calc(100svh + (var(--n) - .55) * 110svh);margin-top:0;}
.ex-phone .ex-stage{top:0;}
.ex-phone .ex-stop:not(.ex-open){top:auto;bottom:0;left:0;right:0;width:auto;align-items:flex-end;
  padding:2.6rem 16px calc(var(--ex-yh) + 1.6rem);}
.ex-phone .ex-stop.is-on:not(.ex-open,.ex-outro){background:linear-gradient(180deg,transparent 0,var(--bg) 2.4rem);}
.ex-phone .ex-place .ex-panel,.ex-phone .ex-place.is-planned .ex-panel{--ex-namew:86vw;}
.ex-phone .ex-name{font-size:min(calc(var(--ex-namew) * var(--ex-fit)),11svh);}
.ex-phone .ex-co{display:none;}
.ex-phone .ex-name{line-height:1.05;}
.ex-phone .ex-line{font-size:1rem;line-height:1.4;margin-top:.6rem;}
.ex-phone .ex-year::before{inset:-25% 0 0;}
.ex-phone .ex-when{margin-top:.7rem;}
.ex-phone .ex-facts{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:.5rem;}
.ex-phone .ex-facts>div:nth-child(n+4){display:none;}
.ex-phone .ex-acts{margin-top:.8rem;}
.ex-phone .ex-world .ex-panel{max-width:none;}
.ex-phone .ex-stop.ex-outro{top:0;align-items:flex-end;}
.ex-phone .ex-out-ph{left:0;right:0;top:0;bottom:auto;height:74%;}
.ex-phone .ex-outro .ex-h2{font-size:min(var(--fs-display),13vw);}
.ex-phone .is-planned .ex-facts{grid-template-columns:repeat(2,minmax(0,1fr));}
.ex-phone .is-planned .ex-facts>div{display:block;}
.ex-phone .ex-pic{inset:0;}
.ex-phone .ex-pic .ex-sky-ph{width:100%;left:0!important;right:0!important;}
.ex-phone .ex-pic.is-india{-webkit-mask-image:linear-gradient(180deg,#000 40%,transparent 62%);mask-image:linear-gradient(180deg,#000 40%,transparent 62%);}
.ex-phone .ex-pic.is-kenya{-webkit-mask-image:linear-gradient(0deg,#000 45%,transparent 66%);mask-image:linear-gradient(0deg,#000 45%,transparent 66%);}
</style>'''
rep('</head>', css + '\n</head>')
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
