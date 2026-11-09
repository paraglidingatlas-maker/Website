"""One task's YouTube kit from SRS's scores, in one go (chat 21, 9 Nov 2026).

    python3 make_day.py N            e.g. python3 make_day.py 1   (Tapalpa Task N = SRS T6.N)

1. Reads api.airtribune.com/srs/scores/?indx=1&comp=9 for "T6.N": the date, the task id, the IGC zip and the KMZ.
2. Writes tN/results.json (Sports, Female and Team tables, provisional as SRS posts them), tN/igc/, tN/kmz/.
3. Renders 3840x2160 transparent PNGs into out/taskN/boards/: the Sports top 10, the Female top 5, the Team top 5,
   and the cards (task winner, first into goal, first woman, first team).
Then run make_kml.py tN N 10 (the Google Earth file) and make_anim.py N "<date>" "<next date>" (opener, end card).
Every figure comes from SRS's tables; nothing is added.
"""
import asyncio, html, io, json, os, re, sys, urllib.request, zipfile

K = os.path.dirname(os.path.abspath(__file__))
API = "https://api.airtribune.com/srs/scores/"
COMP, SERIES = 9, 6                      # Tapalpa is the 2026 series' 6th event: T6.n
TYPES = {"sports": 56, "female": 57, "team": 61}
E = html.escape


def get(url, binary=False):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
        b = r.read()
    return b if binary else b.decode("utf-8", "replace")


def task_links(n):
    t = re.sub(r"[?&]ts=\d+", "", get(API + "?indx=1&comp=%d" % COMP))
    m = re.search(r"<b>T%d\.%d\. ([^<]+)</b>(.*?)</p>" % (SERIES, n), t, re.S)
    if not m:
        sys.exit("T%d.%d is not on SRS's scores page yet" % (SERIES, n))
    blk = m.group(2)
    tid = re.search(r"meet=(\d+)&task=(\d+)", blk)
    igc = re.search(r'href="\.\./(files/task/[^"]+\.zip)"', blk)
    kmz = re.search(r'href="\.\./(files/task/[^"]+\.kmz)"', blk)
    base = API.rsplit("scores/", 1)[0]
    return dict(date=m.group(1).strip(), meet=tid.group(1), task=tid.group(2),
                igc=base + igc.group(1) if igc else None, kmz=base + kmz.group(1) if kmz else None)


def cells(row):
    return [re.sub(r"<[^>]+>", "", c).replace("&nbsp;", "").strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]


def name_case(s):
    # SRS writes "Matthijs GROENEVELD": the surname in capitals becomes "Groeneveld"
    return " ".join(w.capitalize() if w.isupper() and len(w) > 1 else w for w in s.split())


COLS = ["Rank", "ID", "Name", "Nation", "Glider", "Sponsor", "Start", "Finish", "Time", "Height", "Speed",
        "Distance", "DistP", "LOP", "SpdP", "LowP", "Score"]


def table(meet, task, typ):
    t = get(API + "?meet=%s&task=%s&type=%d" % (meet, task, typ))
    head = re.search(r"<h3>([^<]+)<em>([^<]*)</em>", t)
    status = head.group(2).strip() if head else ""
    body = t[t.find("<th>Rank</th>"):]
    # the columns by their headers: a stopped task adds "Alt Goal" and "Adj Dist" (T6.2, 9 Nov)
    hdr = [re.sub(r"<[^>]+>|&nbsp;", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", body[:body.find("</tr>")], re.S)]
    cols = [{"Dist P": "DistP", "LO P": "LOP", "Spd P": "SpdP", "Low P": "LowP", "Alt Goal": "AltGoal", "Adj Dist": "AdjDist"}.get(h, h) or "_" for h in hdr]
    body = body[body.find("</tr>") + 5:]
    rows = re.findall(r"<tr>(.*?)</tr>", body, re.S)
    out, team = [], None
    for r in rows:
        c = cells(r)
        if typ == TYPES["team"]:
            b = re.search(r"<b>([^<]+)</b>", r)
            if b and c and c[0]:
                team = {"Rank": c[0], "Team": b.group(1).strip(), "Score": c[-2], "pilots": []}
                out.append(team)
            elif team is not None and len(c) >= 17 and c[1]:
                p = dict(zip(cols, c)); p["Name"] = name_case(p["Name"])
                p["counts"] = "<del>" not in r
                team["pilots"].append(p)
            continue
        if len(c) >= 17 and c[1]:
            p = dict(zip(cols, c)); p["Name"] = name_case(p["Name"])
            out.append(p)
    return out, status


def fetch(n):
    d = os.path.join(K, "t%d" % n)
    os.makedirs(d, exist_ok=True)
    L = task_links(n)
    res = {"task": n, "date": L["date"], "meet": L["meet"], "task_id": L["task"]}
    for k, typ in TYPES.items():
        res[k], res[k + "_status"] = table(L["meet"], L["task"], typ)
    json.dump(res, open(os.path.join(d, "results.json"), "w"), indent=1, ensure_ascii=False)
    for key, sub in (("igc", "igc"), ("kmz", "kmz")):
        if L[key]:
            try:
                z = zipfile.ZipFile(io.BytesIO(get(L[key], True)))
                os.makedirs(os.path.join(d, sub), exist_ok=True)
                for nm in z.namelist():
                    if key == "kmz" and nm.endswith(".kml"):
                        open(os.path.join(d, sub, "doc.kml"), "wb").write(z.read(nm))
                    elif key == "igc" and nm.lower().endswith(".igc"):
                        # SRS names the tracks by competition ID somewhere in the file name
                        m = re.search(r"(\d{4})", os.path.basename(nm))
                        open(os.path.join(d, sub, (m.group(1) if m else os.path.basename(nm)[:-4]) + ".igc"), "wb").write(z.read(nm))
            except Exception as e:
                print("could not read", key, e)
    print("t%d: %s, %s; %d sports, %d female, %d teams; %s" % (n, L["date"], res["sports_status"], len(res["sports"]),
          len(res["female"]), len(res["team"]), ", ".join(sorted(os.listdir(d)))))
    return res


def flags():
    """IOC code -> local flag svg, from the airtribune pilot list's own flags"""
    f = os.path.join(K, "src", "flags.json")
    if os.path.exists(f):
        return json.load(open(f))
    t = get("https://airtribune.com/srs-2026-%d/info" % SERIES)
    j = json.loads(re.search(r"window\.ATDATA\.pilots = (\{.*?\});\s*\n", t, re.S).group(1))
    m = {}
    os.makedirs(os.path.join(K, "src", "flags"), exist_ok=True)
    for p in j["pilots"]:
        c = p.get("country") or {}
        ioc, svg = c.get("ioc_code"), c.get("flag-svg")
        if ioc and svg and ioc not in m:
            fn = os.path.join(K, "src", "flags", ioc + ".svg")
            if not os.path.exists(fn):
                try:
                    open(fn, "wb").write(get("https://airtribune.com" + svg, True))
                except Exception:
                    continue
            m[ioc] = "src/flags/%s.svg" % ioc
    json.dump(m, open(f, "w"))
    return m


# SRS writes ISO codes where airtribune's pilot list has IOC codes
ISO2IOC = {"CHE": "SUI", "NLD": "NED", "DEU": "GER", "PRT": "POR", "IRN": "IRI", "CRI": "CRC", "HND": "HON",
           "SGP": "SIN", "TWN": "TPE", "VIR": "ISV", "PRI": "PUR", "URY": "URU", "XKX": "KOS"}


def flag(F, p):
    n = p.get("Nation", "")
    return F.get(n) or F.get(ISO2IOC.get(n, ""), "")


LOCK = ('<div class="lock"><img class="l-srs" src="src/srs-w.png"><i></i><div class="l-adv">'
        '<img src="src/advance-white.svg"><span>Advance<br>Edition</span></div></div>')


def board(n, kick, title, rows, foot):
    return ('<div class="panel"><div class="tri"></div><div class="kick">Tapalpa <b>&middot;</b> %s</div>'
            '<div class="title">%s</div>%s<div class="foot">%s</div></div>%s' % (kick, title, "".join(rows), foot, LOCK))


def prow(i, p, F, team=False):
    fl = flag(F, p)
    img = '<img src="%s">' % fl if fl else "<span></span>"
    if team:
        sub = " &middot; ".join(E(q["Name"]) for q in p["pilots"])
        return ('<div class="row p%d"><div class="rk">%s</div><span></span><div class="nm">%s</div><div class="gl">%s</div>'
                '<div class="sc">%s</div></div>' % (i + 1, E(p["Rank"]), E(p["Team"]), sub, E(p["Score"])))
    small = ("%s" % p["Time"]) if p.get("Time") else ("%s km" % p["Distance"] if p.get("Distance") else "")
    return ('<div class="row p%d"><div class="rk">%s</div>%s<div class="nm">%s</div><div class="gl">%s</div>'
            '<div class="sc">%s<small>%s</small></div></div>' % (i + 1, E(p["Rank"]), img, E(p["Name"]), E(p["Glider"]),
                                                                 E(p["Score"]), E(small)))


def card(kick, p, line, F):
    fl = flag(F, p)
    return ('<div class="win"><div class="k">%s</div><div class="n">%s%s</div><div class="s">%s</div></div>%s'
            % (kick, E(p["Name"]), '<img src="%s">' % fl if fl else "", line, LOCK))


def secs(t):
    h, m, s = map(int, t.split(":")); return h * 3600 + m * 60 + s


def pages(R):
    n, F = R["task"], flags()
    st = R.get("sports_status", "").strip().capitalize() or "Provisional"
    foot = "Task %d &middot; %s &middot; SRS scores, %s" % (n, E(R["date"]), E(st.lower()))
    P = {}
    sp, fe, tm = R["sports"], R["female"], R["team"]
    P["Board_Sports_Top10"] = board(n, "Task %d results" % n, "Top <span>10</span>", [prow(i, p, F) for i, p in enumerate(sp[:10])], foot)
    if fe:
        P["Board_Female_Top5"] = board(n, "Task %d &middot; Female" % n, "Top <span>5</span> women", [prow(i, p, F) for i, p in enumerate(fe[:5])], foot)
    if tm:
        P["Board_Team_Top5"] = board(n, "Task %d &middot; Teams" % n, "Top <span>5</span> teams", [prow(i, p, F, True) for i, p in enumerate(tm[:5])], foot)
    w = sp[0]
    P["Card_Winner"] = card("Task %d winner" % n, w, "<span><b>%s</b> points</span>%s" % (E(w["Score"]), "<span>%s</span>" % E(w["Time"]) if w.get("Time") else ""), F)
    fin = [p for p in sp if p.get("Time")]
    if fin:
        f1 = min(fin, key=lambda p: secs(p["Time"]))
        P["Card_FirstIntoGoal"] = card("First into goal", f1, "<span><b>%s</b></span><span>%s km/h</span>" % (E(f1["Time"]), E(f1["Speed"])), F)
    if fe:
        P["Card_FirstWoman"] = card("Task %d &middot; first woman" % n, fe[0], "<span><b>%s</b> points</span>" % E(fe[0]["Score"]), F)
    if tm:
        P["Card_FirstTeam"] = ('<div class="win"><div class="k">Task %d &middot; first team</div><div class="n">%s</div>'
                               '<div class="s"><span><b>%s</b> points</span></div></div>%s' % (n, E(tm[0]["Team"]), E(tm[0]["Score"]), LOCK))
        ties = [t for t in tm if t["Rank"] == tm[0]["Rank"]]
        if len(ties) > 1:
            P["Card_FirstTeam"] = P["Card_FirstTeam"].replace(E(tm[0]["Team"]), " &amp; ".join(E(t["Team"]) for t in ties), 1).replace("first team", "first equal teams")
    return P


async def render(n, P):
    from playwright.async_api import async_playwright
    tpl = open(os.path.join(K, "board.tpl")).read()
    out = os.path.join(K, "out", "task%d" % n, "boards"); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 3840, "height": 2160})
        for name, body in P.items():
            f = os.path.join(K, "cur_board.html"); open(f, "w").write(tpl.replace("BODY", body))
            await pg.goto("file://" + f, wait_until="networkidle"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(out, "Task%d_%s.png" % (n, name)), omit_background=True)
            # a preview on dark grey, to look at without an editor
            await pg.add_style_tag(content="html,body{background:#3a3f44!important}")
            await pg.screenshot(path=os.path.join(K, "out", "task%d" % n, "preview_%s.jpg" % name), type="jpeg", quality=70)
        await b.close()
    os.remove(os.path.join(K, "cur_board.html"))
    print("boards:", ", ".join(P))


if __name__ == "__main__":
    n = int(sys.argv[1])
    R = fetch(n)
    asyncio.run(render(n, pages(R)))
