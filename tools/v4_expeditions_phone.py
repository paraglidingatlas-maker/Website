#!/usr/bin/env python3
"""The expeditions page on phones (owner, 3 Nov 2026: "expeditions phone page is a go").

Below 1000 px the desktop flight runs in a phone shape: the camera flies the map in the top of the screen and
each photograph rises out of its ring there, sized to the stop's words (photo first, owner: "reduce the text in
phone view"); the words sit at the foot on a see-through shade, so nothing moves behind reading text once a stop
has landed. On phones a place keeps its label, name, dates, state, three facts (values only) and both buttons;
the one-line pitch and the small labels are left to the trip pages. Reduced motion and no script keep the still
journey. Desktop is unchanged. Applied by tools/v4_expeditions.py to the page it builds; checked on a phone at
390 x 683 (inside the Claude app) and 390 x 844, menu bar shown and hidden, at every stop.
"""


def phone(h):
    def rep(a, b, n=1):
        nonlocal h
        assert h.count(a) == n, (a[:80], h.count(a)); h = h.replace(a, b)
    # 1 the early switch: phones fly too (still under reduced motion)
    rep('if(m("(min-width: 1000px) and (min-height: 620px)").matches&&',
        'if((m("(min-width: 1000px) and (min-height: 620px)").matches||m("(max-width: 999px)").matches)&&')
    rep('r.classList.add("ex-fly");', 'r.classList.add("ex-fly");if(m("(max-width: 999px)").matches)r.classList.add("ex-phone");')
    # 2 the script
    rep('var mqWide = w.matchMedia("(min-width: 1000px) and (min-height: 620px)");',
        'var mqWide = w.matchMedia("(min-width: 1000px) and (min-height: 620px), (max-width: 999px)"); var PH = w.matchMedia("(max-width: 999px)"); var PT = [];')
    rep('    step = Math.max(1, (atlas.offsetHeight - H) / (N - 1 + HOLD));',
        '''    if (PH.matches) {   /* phone: the camera and the photographs own the screen above each stop's words */
          PT = S.map(function (s, i) {
            var el = stops[i], pn = el && el.querySelector(".ex-panel");
            return pn ? el.offsetTop + pn.offsetTop : H * .6;
          });
          regs = S.map(function (s, i) {
            var b = Math.max(.3, PT[i] / H - .06);
            if (i === 0) return [-.06, 1.06, .02, .62];
            if (i === N - 1) return [.03, .97, .08, .42];
            if (i === 1) return [.03, .97, .08, b];
            return [.1, .9, .1, b];
          });
          panelR = 0;
        }
        step = Math.max(1, (atlas.offsetHeight - H) / (N - 1 + HOLD));''')
    rep('  function photoRect(pl) {\n', '  function photoRect(pl) {\n    if (PH.matches) { var si = PL.indexOf(pl) + 2; return [0, 0, W, Math.round(Math.min(H * .85, (PT[si] || H * .6) + 110))]; }\n')
    rep("var y = (j + .5) / MH * rh, my = pk ? 1 : ss(0, rh * .26, y) * ss(0, rh * .3, rh - y);",
        "var y = (j + .5) / MH * rh, my = pk ? 1 : PH.matches ? ss(0, rh * .42, rh - y) : ss(0, rh * .26, y) * ss(0, rh * .3, rh - y);")
    rep("m = pk ? my : my * ss(0, rw * .5, x);", "m = pk ? my : PH.matches ? my : my * ss(0, rw * .5, x);")
    # 3 the phone layout
    css = '''<style>
    /* phone flight (preview): one window at the top where the camera flies and the photographs rise;
       the words sit on plain dark at the foot, nothing moves behind them */
    .ex-phone .ex-atlas{height:calc(100svh + (var(--n) - .55) * 110svh);margin-top:0;}
    .ex-phone .ex-stage{top:0;}
    .ex-phone .ex-stop:not(.ex-open){top:auto;bottom:0;left:0;right:0;width:auto;align-items:flex-end;
      padding:1.6rem 16px calc(var(--ex-yh) + 1.4rem);}
    .ex-phone .ex-stop.is-on:not(.ex-open,.ex-outro){background:linear-gradient(180deg,transparent 0,color-mix(in srgb,var(--bg) 55%,transparent) 3rem,var(--bg) 7.5rem);}
    .ex-phone .ex-place .ex-when .ex-lab,.ex-phone .ex-place .ex-facts dt{display:none;}
    .ex-phone .ex-place .ex-facts dd{margin-top:0;}
    .ex-phone .ex-place .ex-name{text-shadow:0 1px 18px color-mix(in srgb,var(--bg) 60%,transparent);}
    .ex-phone .ex-place .ex-panel,.ex-phone .ex-place.is-planned .ex-panel{--ex-namew:86vw;}
    .ex-phone .ex-name{font-size:min(calc(var(--ex-namew) * var(--ex-fit)),7.5svh);line-height:1;}
    .ex-phone .ex-co{display:none;}
    .ex-phone .ex-name{line-height:1.05;}
    .ex-phone .ex-place .ex-line{display:none;}
    .ex-phone .ex-line{font-size:.95rem;line-height:1.4;margin-top:.4rem;}
    .ex-phone .ex-year::before{inset:-25% 0 0;}
    .ex-phone .ex-when{margin-top:.5rem;}
    .ex-phone .ex-facts{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:.3rem;}
    .ex-phone .ex-facts div{padding:.45rem 0;}
    .ex-phone .ex-facts>div:nth-child(n+4){display:none;}
    .ex-phone .ex-acts{margin-top:.6rem;}
    .ex-phone .ex-world .ex-panel{max-width:none;}
    .ex-phone .ex-stop.ex-outro{top:0;align-items:flex-end;}
    .ex-phone .ex-out-ph{left:0;right:0;top:0;bottom:auto;height:74%;}
    .ex-phone .ex-outro .ex-h2{font-size:min(var(--fs-display),13vw);}
    .ex-phone .is-planned .ex-facts{grid-template-columns:repeat(2,minmax(0,1fr));}
    .ex-phone .is-planned .ex-facts>div{display:block;}
    /* no desktop shade on phones (it darkens the left half for words that sit at the foot here): only a soft
       fade from the camera window into the words */
    .ex-phone .ex-plate::after{background:none;}
    .ex-phone .ex-atlas:has(.ex-outro.is-on) .ex-pins{opacity:0!important;transition:opacity .4s var(--ease);}
    .ex-phone .ex-pic{inset:0;}
    .ex-phone .ex-pic .ex-sky-ph{width:100%;left:0!important;right:0!important;}
    .ex-phone .ex-pic.is-india{-webkit-mask-image:linear-gradient(180deg,#000 40%,transparent 62%);mask-image:linear-gradient(180deg,#000 40%,transparent 62%);}
    .ex-phone .ex-pic.is-kenya{-webkit-mask-image:linear-gradient(0deg,#000 45%,transparent 66%);mask-image:linear-gradient(0deg,#000 45%,transparent 66%);}
    </style>'''
    rep('</head>', css + '\n</head>')
    return h


def main():
    """Apply the phone layer to the committed expeditions page (the build keeps that file as committed; the
    page's own generator, tools/v4_expeditions.py, also applies it when it runs). Safe to run twice."""
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prototypes", "v4", "expeditions.html")
    h = open(path, encoding="utf-8").read()
    if "ex-phone" in h:
        print("v4_expeditions_phone: already applied")
        return
    open(path, "w", encoding="utf-8").write(phone(h))
    print("v4_expeditions_phone: applied to prototypes/v4/expeditions.html")


if __name__ == "__main__":
    main()
