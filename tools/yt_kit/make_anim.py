"""Tapalpa YouTube kit: the animated opener (over the owner's footage) and the end card, 4K 60 fps.

    python3 make_anim.py N "8 Nov" [next_date]     e.g. python3 make_anim.py 1 "8 Nov" "Mon 9 Nov"

Writes out/animated/Opener_TaskN_4K60_greenscreen.mp4 (CapCut: Chroma key on green), Opener_TaskN_4K60_alpha.mov
(transparent, PNG codec, for editors that read it) and EndCard_TaskN_4K60.mp4 (animates in, then holds 15 s for
YouTube's end screen). Every move is a Web Animation set frame by frame, so the render is exact at 60 fps.
"""
import asyncio, os, shutil, subprocess, sys
from playwright.async_api import async_playwright

K = os.path.dirname(os.path.abspath(__file__))
TPL = open(os.path.join(K, "anim.tpl")).read()
LOCK = ('<div class="lock"><img class="l-srs" src="src/srs-w.png"><i></i><div class="l-adv">'
        '<img src="src/advance-white.svg"><span>Advance<br>Edition</span></div></div>')
IN, OUT = "cubic-bezier(.2,.8,.2,1)", "cubic-bezier(.6,0,.8,.4)"


def opener(n, date):
    body = ('<div class="shade"></div><i class="slash s1"></i><i class="slash s2"></i><i class="slash s3"></i>'
            '<div class="kick">Tapalpa <b>&middot;</b> Day %d of 7</div><div class="big">Task <span>%d</span></div>'
            '<div class="strip"><div>%s</div><div>Highlights</div></div>%s') % (n, n, date, LOCK)
    # 0 to 0.6 s in, hold to 3.3 s, out by 4 s
    sc = """
function hold(a,b,ms,delay){return [a,Object.assign({},b,{offset:(600-delay)/ms}),Object.assign({},b,{offset:(3300-delay)/ms,easing:'%(OUT)s'}),a]}
A('.shade',hold({opacity:0},{opacity:1},4000,0),{duration:4000});
A('.slash',[{transform:'skewX(-18deg) translateY(-2600px)'},{transform:'skewX(-18deg) translateY(0)',offset:.15},{transform:'skewX(-18deg) translateY(0)',offset:.82,easing:'cubic-bezier(.7,0,.3,1)'},{transform:'skewX(-18deg) translateY(2600px)'}],{duration:4000,stagger:60,ke:'cubic-bezier(.7,0,.3,1)'});
A('.kick',[{opacity:0,transform:'translateX(-120px)'},{opacity:1,transform:'none',offset:.12},{opacity:1,transform:'none',offset:.8,easing:'%(OUT)s'},{opacity:0,transform:'translateX(-120px)'}],{duration:3700,delay:200});
A('.big',[{opacity:0,transform:'translateX(-260px)'},{opacity:1,transform:'none',offset:.12},{opacity:1,transform:'none',offset:.8,easing:'%(OUT)s'},{opacity:0,transform:'translateX(260px)'}],{duration:3650,delay:300});
A('.strip',[{opacity:0,transform:'translateY(60px)'},{opacity:1,transform:'none',offset:.14},{opacity:1,transform:'none',offset:.8,easing:'%(OUT)s'},{opacity:0}],{duration:3500,delay:450});
A('.lock',[{opacity:0},{opacity:1,offset:.15},{opacity:1,offset:.85},{opacity:0}],{duration:3800,delay:150,ke:'linear'});
""" % {"OUT": OUT}
    return TPL.replace("BODYCLASS", "").replace("BODY", body).replace("SCRIPT", sc), 4000


def endcard(n, next_date):
    last = n >= 7
    head = "That&#x27;s <span>a wrap</span>" if last else "Next: Task <span>%d</span>" % (n + 1)
    sub = "SRS Advance Edition &middot; Tapalpa 2026" if last else "%s &middot; Tapalpa" % next_date
    body = ('<i class="slash s1"></i><i class="slash s2"></i><i class="slash s3"></i>'
            '<div class="e-h">%s</div><div class="e-sub">%s</div>'
            '<div class="e-url">Free photos of every task: <b>paraglidingatlas.com</b></div>'
            '%s'
            '<img class="atlas" src="src/atlas.png">') % (head, sub, LOCK)
    sc = """
A('.slash',[{transform:'skewX(-18deg) translateY(-2600px)'},{transform:'skewX(-18deg) translateY(0)'}],{duration:900,stagger:70,ke:'cubic-bezier(.7,0,.3,1)'});
A('.e-h',[{opacity:0,transform:'translateX(-200px)'},{opacity:1,transform:'none'}],{duration:700,delay:400});
A('.e-sub,.e-url',[{opacity:0,transform:'translateY(40px)'},{opacity:1,transform:'none'}],{duration:600,delay:650,stagger:120});
A('.lock,.atlas',[{opacity:0},{opacity:1}],{duration:600,delay:500,ke:'linear'});
"""
    return TPL.replace("BODYCLASS", "bg").replace("BODY", body).replace("SCRIPT", sc), 1500


async def frames(html, ms, name, alpha, fps=60):
    fr = os.path.join(K, "frames_" + name)
    shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    page = os.path.join(K, "cur_%s.html" % name)
    open(page, "w").write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 3840, "height": 2160})
        await pg.goto("file://" + page, wait_until="networkidle"); await pg.wait_for_timeout(800)
        for i in range(int(ms * fps / 1000) + 1):
            await pg.evaluate("t=>render(t)", i * 1000 / fps)
            await pg.screenshot(path="%s/%05d.png" % (fr, i), omit_background=alpha)
        await b.close()
    return fr


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + list(a), check=True)


async def main(n, date, next_date):
    out = os.path.join(K, "out", "animated"); os.makedirs(out, exist_ok=True)
    fr = await frames(*opener(n, date), "opener%d" % n, True)
    ff("-f", "lavfi", "-i", "color=c=0x00ff00:s=3840x2160:r=60", "-framerate", "60", "-i", fr + "/%05d.png",
       "-filter_complex", "[0][1]overlay=shortest=1,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
       "%s/Opener_Task%d_4K60_greenscreen.mp4" % (out, n))
    ff("-framerate", "60", "-i", fr + "/%05d.png", "-c:v", "png", "-pix_fmt", "rgba", "%s/Opener_Task%d_4K60_alpha.mov" % (out, n))
    fr = await frames(*endcard(n, next_date), "endcard%d" % n, False)
    ff("-framerate", "60", "-i", fr + "/%05d.png", "-vf", "tpad=stop_mode=clone:stop_duration=15,format=yuv420p",
       "-c:v", "libx264", "-crf", "16", "-preset", "medium", "%s/EndCard_Task%d_4K60.mp4" % (out, n))


if __name__ == "__main__":
    n = int(sys.argv[1]); asyncio.run(main(n, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ""))
