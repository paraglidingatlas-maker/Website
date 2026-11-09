"""Animated results boards for the highlights, to lay over footage (owner, 9 Nov 2026).

    python3 make_boards_anim.py N        (after make_day.py N has written tN/results.json)

Three clips, 4K 60 fps with a transparent background (QuickTime Animation codec, alpha): the task's top 10 (7 s),
the women's standings after the task (7 s) and the overall leaderboard after the task (10 s). The panel is 40%
opaque (60% see-through) so the drone shot shows through; the text is solid. The rows wipe in one after the other
(TV-graphics style), hold, and wipe out at the end. Standings come from SRS's Event Overalls (meet=93, Sports and
Female); no status word is printed, so nothing claims "final" before SRS does.
"""
import asyncio, json, os, re, shutil, subprocess, sys
import make_day as D

K = D.K
E = D.E
FPS = 60


def overall(typ):
    t = D.get(D.API + "?meet=%s&type=%d" % (MEET, typ))
    body = t[t.find("<th>Rank</th>"):]
    out = []
    for r in re.findall(r"<tr>(.*?)</tr>", body, re.S):
        c = D.cells(r)
        if len(c) >= 8 and c[1]:
            out.append({"Rank": c[0], "ID": c[1], "Name": D.name_case(c[2]), "Nation": c[3], "Glider": c[4], "Score": c[-1]})
    return out


CSS = """
.panel{background:rgba(8,34,24,.40)!important;box-shadow:none!important}
.row{overflow:hidden}
.row .rk,.row .nm,.row .sc{text-shadow:0 3px 14px rgba(0,0,0,.45)}
.row .gl{color:#fff!important}
.title,.kick,.foot{text-shadow:0 4px 18px rgba(0,0,0,.45)}
.foot{color:#fff!important}
"""


def page(kick, title, rows, foot, n_rows, dur):
    F = D.flags()
    body = D.board(0, kick, title, [D.prow(i, p, F) for i, p in enumerate(rows)], foot)
    tpl = open(os.path.join(K, "board.tpl")).read().replace("</style>", CSS + "</style>")
    js = """
<script>
function A(sel,kf,opt){document.querySelectorAll(sel).forEach(function(e,i){var o=Object.assign({fill:'both'},opt);delete o.ke;delete o.stagger;o.easing='linear';
 kf=kf.map(function(k){return Object.assign({easing:opt.ke||'cubic-bezier(.2,.8,.2,1)'},k)});o.delay=(opt.delay||0)+(opt.stagger||0)*i;e.animate(kf,o).pause()})}
function render(t){document.getAnimations().forEach(function(a){a.currentTime=t})}
var D=%(dur)d, OUT=D-650;
// in
A('.panel',[{opacity:0,transform:'translateX(-80px)'},{opacity:1,transform:'none'}],{duration:500});
A('.tri',[{transform:'scaleY(0)',transformOrigin:'top'},{transform:'scaleY(1)',transformOrigin:'top'}],{duration:600,delay:100});
A('.kick,.title',[{opacity:0,transform:'translateX(-120px)'},{opacity:1,transform:'none'}],{duration:500,delay:150,stagger:90});
A('.row',[{clipPath:'inset(0 100%% 0 0)',transform:'translateX(-70px)'},{clipPath:'inset(0 0%% 0 0)',transform:'none'}],{duration:420,delay:420,stagger:85});
A('.foot,.lock',[{opacity:0},{opacity:1}],{duration:400,delay:900,ke:'linear'});
// out
A('.row',[{clipPath:'inset(0 0 0 0%%)',transform:'none'},{clipPath:'inset(0 0 0 100%%)',transform:'translateX(70px)'}],{duration:300,delay:OUT,stagger:25,ke:'cubic-bezier(.6,0,.8,.4)',fill:'forwards'});
A('.kick,.title,.foot,.lock',[{opacity:1},{opacity:0}],{duration:300,delay:OUT+150,ke:'linear',fill:'forwards'});
A('.panel',[{opacity:1},{opacity:0}],{duration:350,delay:OUT+300,ke:'linear',fill:'forwards'});
</script>""" % {"dur": dur}
    return tpl.replace("BODY", body + js)


async def clip(name, html, dur, out):
    fr = os.path.join(K, "frames_" + name)
    shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    f = os.path.join(K, "cur_%s.html" % name); open(f, "w").write(html)
    nfr = dur * FPS // 1000
    settle = int(2.2 * FPS)                     # every row is in by 2.2 s
    out_from = (dur - 700) * FPS // 1000        # the exit starts at dur - 650 ms
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 3840, "height": 2160})
        await pg.goto("file://" + f, wait_until="networkidle"); await pg.wait_for_timeout(800)
        hold = None
        for i in range(nfr):
            path = "%s/%05d.png" % (fr, i)
            if settle <= i < out_from:          # the hold: one still, linked for every frame
                if hold is None:
                    await pg.evaluate("t=>render(t)", i * 1000 / FPS)
                    await pg.screenshot(path=path, omit_background=True); hold = path
                else:
                    os.link(hold, path)
                continue
            await pg.evaluate("t=>render(t)", i * 1000 / FPS)
            await pg.screenshot(path=path, omit_background=True)
        await b.close()
    os.remove(f)
    mov = os.path.join(out, name + "_4K60_alpha.mov")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", fr + "/%05d.png",
                    "-c:v", "qtrle", "-pix_fmt", "argb", "-g", "60", mov], check=True)
    # a preview on a photo-like grey, to check without an editor
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x6b7d8c:s=3840x2160:r=60",
                    "-framerate", str(FPS), "-i", fr + "/%05d.png", "-filter_complex",
                    "[0][1]overlay=shortest=1,scale=1280:-2,format=yuv420p", "-c:v", "libx264", "-crf", "23",
                    os.path.join(out, "preview_" + name + ".mp4")], check=True)
    shutil.rmtree(fr)
    print(name, os.path.getsize(mov) // (1 << 20), "MB")


async def main(n):
    global MEET
    R = json.load(open(os.path.join(K, "t%d" % n, "results.json")))
    MEET = R["meet"]
    date = E(R["date"])
    foot = "SRS scores &middot; Task %d &middot; %s" % (n, date)
    out = os.path.join(K, "out", "task%d" % n, "animated"); os.makedirs(out, exist_ok=True)
    jobs = [
        ("Task%d_Standings_7s" % n, page("Task %d" % n, "Task %d <span>standings</span>" % n, R["sports"][:10], foot, 10, 7000), 7000),
        ("Task%d_Women_7s" % n, page("Women &middot; after Task %d" % n, "Women&#x27;s <span>standings</span>", overall(57)[:10], foot, 10, 7000), 7000),
        ("Task%d_Overall_10s" % n, page("Overall &middot; after Task %d" % n, "Overall <span>leaderboard</span>", overall(56)[:10], foot, 10, 10000), 10000),
    ]
    for name, html, dur in jobs:
        await clip(name, html, dur, out)


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1])))
