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


def overall_teams():
    """SRS's team overall: each team row (rank, name, total) followed by its pilots"""
    t = D.get(D.API + "?meet=%s&type=61" % MEET)
    body = t[t.find("<th>Rank</th>"):]
    out, team = [], None
    for r in re.findall(r"<tr>(.*?)</tr>", body, re.S):
        c = D.cells(r)
        b = re.search(r"<b>([^<]+)</b>", r)
        if b and c and c[0]:
            team = {"Rank": c[0], "Team": b.group(1).strip(), "Score": c[-1], "pilots": []}
            out.append(team)
        elif team is not None and len(c) > 4 and c[1]:
            team["pilots"].append({"Name": D.name_case(c[2])})
    return out


CSS = """
.panel{background:rgba(8,34,24,.40)!important;box-shadow:none!important}
.row{overflow:hidden}
.row .rk,.row .nm,.row .sc{text-shadow:0 3px 14px rgba(0,0,0,.45)}
.row .gl{color:#fff!important}
.title,.kick,.foot{text-shadow:0 4px 18px rgba(0,0,0,.45)}
.foot{color:#fff!important}
"""


def team_page(n, teams, foot, dur):
    F = D.flags()
    html = page("Teams &middot; after Task %d" % n, "Team <span>standings</span>", [], foot, 0, dur)
    rows = "".join(D.prow(i, t, F, True) for i, t in enumerate(teams))
    return html.replace('<div class="foot">', rows + '<div class="foot">', 1)


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


def task_stats(meet, task):
    """SRS's own Task Statistics block (and the stop time, when the task was stopped)"""
    import html as H
    t = D.get(D.API + "?meet=%s&task=%s&type=56" % (meet, task))
    j = t.find("Task Statistics")
    txt = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t[j:j + 4000])))
    out = {}
    for k in ("Total Pilots", "Pilots Landed Out", "Pilots at ESS", "Pilots in Goal", "Task Validity", "Max Task Points"):
        m = re.search(re.escape(k) + r":\s*([\d.]+)", txt)
        if m:
            out[k] = m.group(1)
    m = re.search(r"Stopped at (\d\d:\d\d)", t)
    if m:
        out["Stopped"] = m.group(1)
    m = re.search(r"<td>GOAL</td>.*?([\d.]+ km)</td><td[^>]*>([\d.]+ km)", t, re.S)
    if m:
        out["Distance"] = m.group(1)
    return out


TILES_CSS = """
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:0 60px;margin-top:10px}
.tile{padding:46px 0 40px;border-top:3px solid rgba(255,255,255,.14);overflow:hidden}
.tile b{display:block;font:900 italic 168px/.9 "Barlow Condensed";color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.45);white-space:nowrap}
.tile b.o{color:var(--o)}
.tile b small{font-size:.42em;font-weight:800;margin-left:.12em}
.tile span{display:block;margin-top:18px;font:600 46px/1.15 "Barlow";color:#fff;letter-spacing:.04em;text-shadow:0 3px 14px rgba(0,0,0,.45)}
.panel.wide{width:3480px;top:470px}
"""


STOP_WHY = {2: "rain"}
# a stopped task: pilots who reached the goal field after the scored stop time (srs.live 16:33, 9 Nov: "only 9
# people in goal"; SRS scores count 1, Castro, before the 14:40 stop). Owner, 10 Nov: show the 9.
REACHED_GOAL = {2: 9}      # from srs.live's commentary: Task 2 stopped for rain at the southern turnpoint


def numbers_page(n, R, S, dur):
    sp = R["sports"]
    fin = [p for p in sp if p.get("Time")]
    tiles = []
    if S.get("Distance"):
        v = S["Distance"].replace(" km", "")
        tiles.append(("%s<small>km</small>" % v, "Task distance", ""))
    tiles.append((S.get("Total Pilots", str(len(sp))), "Pilots flying", ""))
    if n in REACHED_GOAL:
        tot = int(S.get("Total Pilots", len(sp)))
        tiles.append((str(REACHED_GOAL[n]), "Reached goal", "o"))
        tiles.append((str(tot - REACHED_GOAL[n]), "Landed out", ""))
    else:
        tiles.append((S.get("Pilots in Goal", str(len(fin))), "In goal", "o"))
        tiles.append((S.get("Pilots Landed Out", "?"), "Landed out", ""))
    if fin:
        w = min(fin, key=lambda p: D.secs(p["Time"]))
        tiles.append((w["Time"].lstrip("0").replace(":", ":", 2) if not w["Time"].startswith("00") else w["Time"][3:], "Fastest time &middot; %s" % E(w["Name"]), "o"))
        tiles.append(("%s<small>km/h</small>" % E(w["Speed"]), "Fastest speed", ""))
    best = max((float(p["Distance"]) for p in sp if p.get("Distance") and not p.get("Time")), default=None)
    if n in REACHED_GOAL:
        k = S.get("Pilots in Goal", str(len(fin)))
        tiles.append((k, "Finish%s scored before the stop" % ("" if k == "1" else "es"), ""))
    elif best is not None:
        tiles.append(("%.1f<small>km</small>" % best, "Best distance at the stop" if S.get("Stopped") else "Furthest without goal", ""))
    if S.get("Stopped"):
        tiles.append((S["Stopped"], "Stopped (%s)" % STOP_WHY[n] if n in STOP_WHY else "Task stopped", "o"))
    elif S.get("Task Validity"):
        tiles.append(("%d<small>%%</small>" % round(float(S["Task Validity"]) * 100), "Task validity", ""))
    tiles = tiles[:8]
    body = "".join('<div class="tile"><b class="%s">%s</b><span>%s</span></div>' % (c, v, l) for v, l, c in tiles)
    foot = "SRS scores &middot; Task %d &middot; %s" % (n, E(R["date"]))
    tpl = open(os.path.join(K, "board.tpl")).read().replace("</style>", CSS + TILES_CSS + "</style>")
    html = ('<div class="panel wide"><div class="tri"></div><div class="kick">Tapalpa <b>&middot;</b> Task %d</div>'
            '<div class="title">Task %d <span>in numbers</span></div><div class="tiles">%s</div><div class="foot">%s</div></div>%s'
            % (n, n, body, foot, D.LOCK))
    js = page("", "", [], "", 0, dur).split("<script>", 1)[1].replace("'.row'", "'.tile'")
    return tpl.replace("BODY", html + "<script>" + js)


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
        ("Task%d_Teams_7s" % n, team_page(n, overall_teams()[:8], foot, 7000), 7000),
    ]
    if "--teams" in sys.argv:
        jobs = jobs[-1:]
    for name, html, dur in jobs:
        await clip(name, html, dur, out)


async def numbers(n, dur=7000):
    R = json.load(open(os.path.join(K, "t%d" % n, "results.json")))
    S = task_stats(R["meet"], R["task_id"])
    print(S)
    out = os.path.join(K, "out", "task%d" % n, "animated"); os.makedirs(out, exist_ok=True)
    await clip("Task%d_Numbers_7s" % n, numbers_page(n, R, S, dur), dur, out)


if __name__ == "__main__":
    if "--numbers" in sys.argv:
        asyncio.run(numbers(int(sys.argv[1])))
    else:
        asyncio.run(main(int(sys.argv[1])))
