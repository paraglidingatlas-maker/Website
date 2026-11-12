"""SRS Tapalpa Talks: the overlays for a talk film, 4K, transparent (chat 22, 12 Nov 2026, Torsten Siegel's talk).

    python3 make_talk.py TALK.srt OUTDIR [names...]

Every overlay is timed from the talk's own captions (the SRT CapCut exported from the final cut), so the sheet
OUTDIR/timestamps.txt says where each one goes. Writes OUTDIR/<NN>_<name>_4K60_transparent.mov (QuickTime Animation with
alpha) and a 1080p transparent GIF and, for the end card, an opaque MP4. Needs OUTDIR/src/: srs-w.png
(prototypes/v4/img/media/logo-srs.png), advance-white.svg (cdn.advance.swiss .../Images/logo-white.svg),
atlas.png (assets/logo/atlas-logo-white.png).
"""
import asyncio, os, re, shutil, subprocess, sys
from playwright.async_api import async_playwright

K = os.path.dirname(os.path.abspath(__file__))
TPL = open(os.path.join(K, "talk.tpl")).read()
FPS = 60
OUT_E = "cubic-bezier(.6,0,.8,.4)"
NAME = "Torsten Siegel"
SERIES = "SRS Tapalpa <b>&middot;</b> Talks"
LOCK = ('<div class="lock"><img class="l-srs" src="src/srs-w.png"><i></i><div class="l-adv">'
        '<img src="src/advance-white.svg"><span>Advance<br>Edition</span></div></div>')
ELOCK = LOCK.replace('class="lock"', 'class="e-lock"')
TRI = '<div class="tri"><i></i><i></i><i></i></div>'
THUMB = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 21h3.5V9H2v12zm20-11c0-1.1-.9-2-2-2h-6.3l1-4.6v-.3'
         'c0-.4-.2-.8-.4-1.1L13.2 1 6.6 7.6c-.4.4-.6.9-.6 1.4V19c0 1.1.9 2 2 2h9c.8 0 1.5-.5 1.8-1.2l3-7.1c.1-.2.2-.5'
         '.2-.7v-2z"/></svg>')
BELL = ('<svg viewBox="0 0 24 24" fill="#111"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6V11c0-3.1-1.6-5.6'
        '-4.5-6.3V4c0-.8-.7-1.5-1.5-1.5S10.5 3.2 10.5 4v.7C7.6 5.4 6 7.9 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>')
CURSOR = ('<svg class="cur" viewBox="0 0 22 26"><path d="M2 2l0 19 5-5 3.5 8 3-1.3-3.5-7.8H17z" fill="#fff" '
          'stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>')
PATREON = '<svg viewBox="0 0 24 24" fill="#111"><circle cx="15" cy="9.5" r="6.5"/><rect x="2.5" y="3" width="3.6" height="18"/></svg>'


# ------------------------------------------------------------------ the talk's own clock, from its captions ----
def srt(path):
    cues = {}
    for b in open(path, encoding="utf-8").read().replace("\r", "").strip().split("\n\n"):
        l = b.split("\n")
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", l[1]) if len(l) > 2 else None
        if m:
            g = [int(x) for x in m.groups()]
            cues[int(l[0])] = (g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                               " ".join(l[2:]))
    return cues


def word(c, cue, w):
    """the moment a word of a cue is said, spread evenly over the cue (good to about a quarter of a second)"""
    a, b, t = c[cue]
    ws = t.split()
    i = next(i for i, x in enumerate(ws) if x.lower().startswith(w.lower()))
    return a + (b - a) * (i + .5) / len(ws)


def ts(s):
    return "%d:%02d.%d" % (int(s // 60), int(s % 60), int(round((s % 1) * 10)) % 10)


# ------------------------------------------------------------------ animation helpers ----
def inout(sel, total, a, b, start=0, inms=650, outms=500, stagger=0, ke=None):
    """sel goes a -> b at start (inms), holds, and back to a in the last outms"""
    k1 = dict(a); k2 = dict(b, offset=round((start + inms) / total, 5))
    k3 = dict(b, offset=round((total - outms) / total, 5), easing=OUT_E); k4 = dict(a)
    import json
    o = {"duration": total, "stagger": stagger}
    if ke: o["ke"] = ke
    return "A(%s,%s,%s);\n" % (json.dumps(sel), json.dumps([k1, k2, k3, k4]), json.dumps(o))


FADE = ({"opacity": 0}, {"opacity": 1})
LEFT = ({"opacity": 0, "transform": "translateX(-90px)"}, {"opacity": 1, "transform": "none"})
UP = ({"opacity": 0, "transform": "translateY(50px)"}, {"opacity": 1, "transform": "none"})


def page(body, script, bg=""):
    return TPL.replace("BODYCLASS", bg).replace("BODY", body).replace("SCRIPT", script)


# ------------------------------------------------------------------ the overlays ----
def opener():
    T = 4200
    body = ('<div class="shade"></div><div class="tri o-tri"><i></i><i></i><i></i></div>'
            '<div class="o-kick sh">%s</div><div class="o-name sh">%s</div><div class="o-line"></div>%s'
            '<img class="o-atlas" src="src/atlas.png">') % (
        SERIES, "".join("<span>%s</span>" % w for w in NAME.split()), LOCK)
    sc = inout(".shade", T, *FADE, inms=700, outms=600, ke="linear")
    sc += inout(".o-tri", T, {"opacity": 0, "transform": "skewX(-14deg) scaleY(0)"}, {"opacity": 1, "transform": "skewX(-14deg) scaleY(1)"}, start=100, inms=700)
    sc += inout(".o-kick", T, *LEFT, start=250)
    sc += inout(".o-name span", T, {"opacity": 0, "transform": "translateX(-140px)"}, {"opacity": 1, "transform": "none"}, start=380, inms=750, stagger=0)
    sc += "document.querySelectorAll('.o-name span')[1].getAnimations()[0].effect.updateTiming({delay:110});\n"
    sc += inout(".o-line", T, {"transform": "scaleX(0)"}, {"transform": "scaleX(1)"}, start=700, inms=900)
    sc += inout(".lock,.o-atlas", T, *FADE, start=300, inms=800, ke="linear")
    return page(body, sc), T


def plate(T=6500):
    body = ('<div class="plate">%s<div class="p-col"><div class="p-tag sh">%s</div>'
            '<div class="p-name">%s</div><div class="p-bar"></div></div></div>') % (TRI, SERIES, NAME)
    sc = inout(".plate .tri", T, {"opacity": 0, "transform": "skewX(-14deg) scaleY(0)"}, {"opacity": 1, "transform": "skewX(-14deg) scaleY(1)"}, inms=500)
    sc += inout(".p-tag", T, *UP, start=150)
    sc += inout(".p-name", T, {"opacity": 0, "clipPath": "inset(0 100% 0 0)"}, {"opacity": 1, "clipPath": "inset(0 0% 0 0)"}, start=120, inms=700)
    sc += inout(".p-bar", T, {"transform": "scaleX(0)", "transformOrigin": "left"}, {"transform": "scaleX(1)", "transformOrigin": "left"}, start=450, inms=650)
    return page(body, sc), T


def career(c):
    """the line draws itself as he says each year; starts 0.4 s before the first, leaves 2 s after the last"""
    items = [("1989", "Started flying", word(c, 14, "89")),
             ("1994", "First competition", word(c, 16, "94")),
             ("1996", "World Cup", word(c, 17, "96")),
             ("2000", "German national team", word(c, 18, "German")),
             ("2025", "100th World Cup comp", word(c, 19, "100")),
             ("2026", "First SRS, Tapalpa", word(c, 20, "first"))]
    t0 = items[0][2] - 1.2
    T = int((items[-1][2] + 2.6 - t0) * 1000)
    xs = [300 + 270 + i * (3240 - 540) / 5 for i in range(6)]
    body = '<div class="band"></div><div class="cl-kick sh">%s <b>&middot;</b> In his words</div>' % NAME
    body += '<div class="cl-base"></div><div class="cl-fill"></div>'
    for i, (y, t, _) in enumerate(items):
        body += '<div class="cl-it it%d%s" style="left:%dpx"><div class="y sh">%s</div><i></i><div class="t sh">%s</div></div>' % (
            i, " last" if i == 5 else "", xs[i], y, t)
    sc = inout(".band", T, *FADE, inms=800, outms=700, ke="linear")
    sc += inout(".cl-kick,.cl-base", T, *FADE, start=200, inms=700, ke="linear")
    # the orange line grows from dot to dot, reaching each as its year is said
    import json
    kf = [{"transform": "scaleX(0)", "opacity": 1}]
    for i, (_, _, at) in enumerate(items):
        ms = (at - t0) * 1000
        kf.append({"transform": "scaleX(%.4f)" % ((xs[i] - 300) / 3240), "opacity": 1, "offset": round(max(ms - 50, 1) / T, 5)})
    kf.append({"transform": "scaleX(1)", "opacity": 1, "offset": round((T - 900) / T, 5), "easing": OUT_E})
    kf.append({"transform": "scaleX(1)", "opacity": 0})
    sc += "A('.cl-fill',%s,{duration:%d,ke:'cubic-bezier(.45,0,.25,1)'});\n" % (json.dumps(kf), T)
    for i, (_, _, at) in enumerate(items):
        sc += inout(".it%d" % i, T, {"opacity": 0, "transform": "translateY(40px) scale(.92)"}, {"opacity": 1, "transform": "none"},
                    start=int((at - t0) * 1000), inms=550, outms=600)
    return page(body, sc), T, t0, [(y, t, at) for y, t, at in items]


def brands(c):
    items = [("UP", "12 years", word(c, 67, "12")), ("Swing", "5 years", word(c, 68, "five")),
             ("Gin Gliders", "12 years", word(c, 76, "12")), ("Advance", "since last summer", word(c, 78, "advance"))]
    t0 = items[0][2] - 1.0
    T = int((items[-1][2] + 4.5 - t0) * 1000)
    body = '<div class="ch-wrap"><div class="ch-kick sh">%s <b>&middot;</b> In his words</div><div class="chips">' % NAME
    for i, (b, s, _) in enumerate(items):
        body += '<div class="chip c%d%s"><b>%s</b><span>%s</span></div>' % (i, " now" if i == 3 else "", b, s)
    body += "</div></div>"
    sc = inout(".ch-kick", T, *FADE, inms=600, ke="linear")
    for i, (_, _, at) in enumerate(items):
        sc += inout(".c%d" % i, T, {"opacity": 0, "transform": "translateY(50px)"}, {"opacity": 1, "transform": "none"},
                    start=int((at - t0) * 1000), inms=600, outms=600)
    return page(body, sc), T, t0, items


def chapter(n, title, T=5000):
    body = '<div class="cc">%s<div class="cc-col"><div class="cc-k">Chapter %02d</div><div class="cc-t">%s</div></div></div>' % (TRI, n, title)
    sc = inout(".cc .tri", T, {"opacity": 0, "transform": "skewX(-14deg) scaleY(0)"}, {"opacity": 1, "transform": "skewX(-14deg) scaleY(1)"}, inms=500)
    sc += inout(".cc-k", T, *LEFT, start=100)
    sc += inout(".cc-t", T, {"opacity": 0, "clipPath": "inset(0 100% 0 0)"}, {"opacity": 1, "clipPath": "inset(0 0% 0 0)"}, start=220, inms=750)
    return page(body, sc), T


def patreon(T=7000):
    body = ('<div class="pt"><div class="pt-q">Like what you see?</div><div class="pt-a">%s<span>Join me on Patreon</span></div>'
            '<div class="pt-s sh">Link in the description</div></div>') % PATREON
    sc = inout(".pt-q", T, *LEFT)
    sc += inout(".pt-a", T, {"opacity": 0, "clipPath": "inset(0 100% 0 0)"}, {"opacity": 1, "clipPath": "inset(0 0% 0 0)"}, start=200, inms=750)
    sc += inout(".pt-s", T, *FADE, start=700, ke="linear")
    return page(body, sc), T


def likesub(T=7000):
    body = ('<div class="ls"><div class="ls-who sh"><img src="src/atlas.png"></div>'
            '<div class="btn like">%s<span>Like</span><div class="on">%s<span>Liked</span></div></div>'
            '<div class="btn sub"><span>Subscribe</span><div class="done">Subscribed</div></div>'
            '<div class="bell">%s</div></div>%s') % (THUMB, THUMB, BELL, CURSOR)
    sc = inout(".ls-who", T, *FADE, inms=600, ke="linear")
    sc += inout(".like,.sub,.bell", T, {"opacity": 0, "transform": "translateY(60px) scale(.9)"}, {"opacity": 1, "transform": "none"}, inms=600, stagger=0)
    sc += ("document.querySelectorAll('.sub')[0].getAnimations()[0].effect.updateTiming({delay:120});"
           "document.querySelectorAll('.bell')[0].getAnimations()[0].effect.updateTiming({delay:240});\n")
    # the pointer: comes in, presses Like (1.4 s), Subscribe (2.7 s), the bell (3.9 s), leaves
    sc += """
(function(){var ls=document.querySelector('.ls').getBoundingClientRect(),L=document.querySelector('.like').getBoundingClientRect(),
S=document.querySelector('.sub').getBoundingClientRect(),B=document.querySelector('.bell').getBoundingClientRect();
function p(r){return 'translate('+(r.left+r.width*.55)+'px,'+(r.top+r.height*.55)+'px)'}
var T=%d,k=[[0,'translate(3900px,2300px)',0],[700,'translate(3900px,2300px)',1],[1250,p(L),1],[1400,p(L)+' scale(.85)',1],[1550,p(L),1],
[2450,p(S),1],[2600,p(S)+' scale(.85)',1],[2750,p(S),1],[3650,p(B),1],[3800,p(B)+' scale(.85)',1],[3950,p(B),1],[4700,p(B),1],[5300,'translate(3900px,2300px)',1],[T,'translate(3900px,2300px)',0]];
A('.cur',k.map(function(x){return {transform:x[1],opacity:x[2],offset:x[0]/T}}),{duration:T,ke:'cubic-bezier(.45,0,.25,1)'});
function sw(sel,at){A(sel,[{opacity:0},{opacity:0,offset:at/T},{opacity:1,offset:(at+120)/T},{opacity:1}],{duration:T,ke:'linear'})}
sw('.like .on',1400);sw('.sub .done',2600);
A('.bell svg',[{transform:'rotate(0)'},{transform:'rotate(0)',offset:3800/T},{transform:'rotate(18deg)',offset:3900/T},{transform:'rotate(-16deg)',offset:4000/T},{transform:'rotate(12deg)',offset:4100/T},{transform:'rotate(-8deg)',offset:4200/T},{transform:'rotate(0)',offset:4320/T},{transform:'rotate(0)'}],{duration:T,ke:'ease-in-out'});
})();
""" % T
    return page(body, sc), T


def endcard(T=1600):
    """animates in over 1.5 s; the encoder holds the last frame to 15 s"""
    body = ('<div class="tri e-tri"><i></i><i></i><i></i></div><div class="e-k">%s &middot; %s</div>'
            '<div class="e-h">Thanks for<br><span>watching</span></div>'
            '<div class="e-url">Free photos of every task: <b>paraglidingatlas.com</b></div>'
            '<div class="e-pt">The daily highlights of SRS Tapalpa are on this channel.</div>'
            '<div class="e-next">Watch <b>next</b></div><img class="e-atlas" src="src/atlas.png">%s') % (
        SERIES.replace("<b>&middot;</b>", "&middot;"), NAME, ELOCK)
    sc = ""
    for sel, st in ((".e-tri", 0), (".e-k", 150), (".e-h", 300), (".e-url", 550), (".e-pt", 700), (".e-next", 800), (".e-atlas,.e-lock", 500)):
        sc += "A(%r,[{opacity:0,transform:'translateY(40px)'},{opacity:1,transform:'none'}],{duration:700,delay:%d});\n" % (sel, st)
    return page(body, sc, "bg"), T


# ------------------------------------------------------------------ render ----
SIG = """t=>{render(t);return document.getAnimations().map(function(a,ai){var e=a.effect,tm=e.getComputedTiming(),k=e.getKeyframes();
 var p=tm.progress;if(p===null)return ai+':n';var i=0;while(i<k.length-1&&k[i+1].computedOffset<=p)i++;
 if(i>=k.length-1)return ai+':e';var A=Object.assign({},k[i]),B=Object.assign({},k[i+1]);
 ['offset','computedOffset','easing','composite'].forEach(function(x){delete A[x];delete B[x]});
 return JSON.stringify(A)===JSON.stringify(B)?ai+':s'+i:'m'}).join('|')}"""


async def frames(html, ms, fr, alpha, src, pages=4):
    """frames where nothing moves are copied from the one before, so long holds cost almost nothing"""
    shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    path = os.path.join(src, "..", "_cur_%s.html" % os.path.basename(fr))
    open(path, "w").write(html)
    n = int(ms * FPS / 1000) + 1
    step = -(-n // pages)
    async with async_playwright() as p:
        b = await p.chromium.launch()

        async def worker(k):
            pg = await b.new_page(viewport={"width": 3840, "height": 2160})
            await pg.goto("file://" + os.path.abspath(path), wait_until="networkidle"); await pg.wait_for_timeout(1200)
            last = None
            for i in range(k * step, min(n, (k + 1) * step)):
                sig = await pg.evaluate(SIG, i * 1000 / FPS)
                f = "%s/%05d.png" % (fr, i)
                if last is not None and "m" not in sig.split("|") and sig == last:
                    shutil.copy("%s/%05d.png" % (fr, i - 1), f)
                else:
                    await pg.screenshot(path=f, omit_background=alpha)
                last = sig
        await asyncio.gather(*[worker(k) for k in range(pages)])
        await b.close()
    os.remove(path)


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + list(a), check=True)


def mov(fr, out):
    """QuickTime Animation with alpha: true transparency, and small, because most of each frame is empty"""
    ff("-framerate", str(FPS), "-i", fr + "/%05d.png", "-c:v", "qtrle", "-pix_fmt", "argb", out)


def gif(fr, out):
    """1080p 30 fps GIF: the easy file; GIF has no soft edges (shadows and see-through shades drop out)"""
    ff("-framerate", str(FPS), "-i", fr + "/%05d.png", "-vf",
       "fps=30,scale=1920:-1:flags=lanczos,split[a][b];[a]palettegen=reserve_transparent=1:stats_mode=diff[p];"
       "[b][p]paletteuse=alpha_threshold=128", out)


async def main(srt_path, out, only):
    c = srt(srt_path)
    src = os.path.join(out, "src")
    jobs, sheet = [], []
    jobs.append(("01_Opener", *opener(), True)); sheet.append(("01_Opener", 0.0, 4.2, "Over the first seconds of the talk"))
    pl = word(c, 2, "Siegel") + 2.0   # after the opener has gone
    jobs.append(("02_NamePlate", *plate(), True)); sheet.append(("02_NamePlate", pl, 6.5, "He has just said his name"))
    h, T, t0, items = career(c)
    jobs.append(("03_CareerLine", h, T, True)); sheet.append(("03_CareerLine", t0, T / 1000, "Years pop in as he says them: " + ", ".join("%s at %s" % (y, ts(a)) for y, _, a in items)))
    h, T, t0, items = brands(c)
    jobs.append(("04_Brands", h, T, True)); sheet.append(("04_Brands", t0, T / 1000, "Chips pop in as he says them: " + ", ".join("%s at %s" % (b, ts(a)) for b, _, a in items)))
    ch = [(24, "From an engineering thesis to a life in paragliding"), (141, "The new glider design rules"),
          (210, "Parakites: game changer or hype?"), (274, "How a glider is designed"),
          (393, "Will Advance build a CCC wing?"), (420, "Ballast rules"), (453, "His favourite setup: Boomerang 11"),
          (483, "The Death Blade and aspect ratio"), (544, "Why Advance joined SRS"), (622, "EN C vs CCC: how it feels"),
          (721, "Discards, and how to get better in comps")]
    for i, (cue, title) in enumerate(ch, 2):
        nm = "%02d_Chapter%02d" % (3 + i, i)
        jobs.append((nm, *chapter(i, title), True)); sheet.append((nm, c[cue][0], 5.0, "Chapter %d: %s" % (i, title)))
    pt = c[389][0]   # "but yeah the details are...": the end of the wing-design answer
    jobs.append(("16_Patreon", *patreon(), True)); sheet.append(("16_Patreon", pt, 7.0, "The end of the glider-design answer, before the CCC question"))
    lsat = c[96][0] - 0.2   # "I think now you know a little bit about me"
    jobs.append(("17_LikeSubscribe", *likesub(), True)); sheet.append(("17_LikeSubscribe", lsat, 7.0, "\"Now you know a little bit about me\": once only"))
    endat = c[857][1] + 0.3
    jobs.append(("18_EndCard", *endcard(), False)); sheet.append(("18_EndCard", endat, 15.0, "After \"thank you very much\"; cut the film when it ends"))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "timestamps.txt"), "w") as f:
        f.write("SRS Tapalpa Talks, %s: where each overlay goes (from the final cut's captions)\n\n" % NAME)
        for nm, at, d, note in sorted(sheet, key=lambda x: x[1]):
            f.write("%-18s in %-8s out %-8s %s\n" % (nm, ts(at), ts(at + d), note))
        f.write("\nYouTube chapters (paste into the description):\n0:00 Who is %s\n" % NAME)
        for cue, title in ch:
            s = c[cue][0]
            f.write("%d:%02d %s\n" % (s // 60, s % 60, title))
    for nm, html, T, alpha in jobs:
        if only and not any(o in nm for o in only):
            continue
        fr = os.path.join(out, "frames", nm)
        await frames(html, T, fr, alpha, src)
        if alpha:
            mov(fr, os.path.join(out, nm + "_4K60_transparent.mov"))
            if nm not in ("01_Opener", "03_CareerLine"):   # these two need a see-through shade a GIF cannot hold
                gif(fr, os.path.join(out, nm + "_1080p_transparent.gif"))
            shutil.copy("%s/%05d.png" % (fr, int(T * FPS / 1000 * 0.5)), os.path.join(out, "preview_" + nm + ".png"))
        else:
            ff("-framerate", str(FPS), "-i", fr + "/%05d.png", "-vf", "tpad=stop_mode=clone:stop_duration=13.4", "-c:v", "libx264",
               "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(out, nm + "_4K60.mp4"))
            shutil.copy("%s/%05d.png" % (fr, int(T * FPS / 1000) - 1), os.path.join(out, "preview_" + nm + ".png"))
        if not os.environ.get("KEEP"): shutil.rmtree(fr)
        print("done", nm, flush=True)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
