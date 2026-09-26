#!/usr/bin/env python3
"""
The phone lens, second part (tools/v4_lens.py): the rest of the knowledge
base's band drawings, each redrawn with the kit and given its own phone
version. Labels and numbers are the ones the drawing it replaces carried
(tools/kbfig/*.py). The altitude drawing adds one computed scale: the share
of sea-level oxygen in each breath, from the standard atmosphere.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
from v4_computed import P, rect, isa  # noqa: E402
from v4_phone import wrap, lines  # noqa: E402

f = K.f


def box(d, x, y, w, h, accent=False, r=8):
    d.path("M%s,%s h%s a%s,%s 0 0 1 %s,%s v%s a%s,%s 0 0 1 -%s,%s h-%s a%s,%s 0 0 1 -%s,-%s v-%s a%s,%s 0 0 1 %s,-%s Z" % (
        f(x + r), f(y), f(w - 2 * r), r, r, r, r, f(h - 2 * r), r, r, r, r, f(w - 2 * r), r, r, r, r, f(h - 2 * r), r, r, r, r),
        "accent" if accent else "detail", fill="card")


# ---------------------------------------------------------------- living the dream: one idea, the projects it grew
CHAIN = [("The idea, 2003", "a novice's goal:", "fly Mexico to Canada", False),
         ("What was left", "he could walk and skateboard:", "skateboard across Canada", True),
         ("The next step", "motor on his back:", "powered paraglider across Canada", True),
         ("The original idea", "during COVID, free flight:", "Mexico to Canada, vol-biv", True)]
CHAIN_DESC = ("One idea, and the projects it grew. Benjamin Jordan's 2003 goal as a novice, to fly from Mexico to Canada, "
              "was out of reach, so he boiled it down to what was left: skateboarding across Canada, then a powered "
              "paraglider across Canada, and finally the free-flying vol-biv from Mexico to Canada, during COVID. Each "
              "project taught the skills for the next; the last one was the first idea.")


def chain():
    d = K.Drawing(1200, 300, "cq-chain", "One idea, and the projects it grew", CHAIN_DESC, inline_css=False)
    d.backdrop(glow=(1020, 130), glow_r=240, sheet=False)
    w, gap, y = 250, 40, 60
    for i, (k, a, b, acc) in enumerate(CHAIN):
        x = 40 + i * (w + gap)
        box(d, x, y, w, 110, acc)
        d.text((x + 16, y + 28), k, "lab")
        d.text((x + 16, y + 58), a, "sub")
        d.text((x + 16, y + 80), b, "tv")
        if i < 3:
            d.arrow((x + w + 6, y + 55), (x + w + gap - 6, y + 55), "accent", 8)
    xl, x0 = 40 + 3 * (w + gap) + w / 2, 40 + w / 2
    d.poly([(xl, y + 116), (xl, y + 160), (x0, y + 160)], "ghost")
    d.arrow((x0, y + 160), (x0, y + 118), "detail", 8)
    d.text((600, y + 196), "each project taught the skills for the next; the last one was the first idea", "sub", "middle")
    return d


def chain_p():
    d = K.Drawing(360, 560, "cq-chain-p", "One idea, and the projects it grew", CHAIN_DESC, inline_css=False)
    y = 16
    for i, (k, a, b, acc) in enumerate(CHAIN):
        box(d, 40, y, 304, 96, acc)
        d.text((56, y + 26), k, "lab")
        d.text((56, y + 52), a, "sub")
        d.text((56, y + 72), b, "tv")
        if i < 3:
            d.arrow((192, y + 100), (192, y + 124), "accent", 8)
        y += 128
    d.poly([(40, 16 + 3 * 128 + 48), (20, 16 + 3 * 128 + 48), (20, 64), (34, 64)], "ghost")
    d.head((38, 64), (1, 0), 8)
    lines(d, 16, 16 + 4 * 128 + 12, "each project taught the skills for the next; the last one was the first idea", 48)
    return d


# ---------------------------------------------------------------- living the dream: the whole kit
KIT = [("Wing", "about 1.8 kg, lines unsheathed", 0, 1.8, "fa", .9),
       ("Harness", "300 g", 1.8, 2.1, "fa", .5),
       ("Reserve", "about 800 g", 2.1, 2.9, "fw", .5)]
KIT_DESC = ("Sandrine Roy's whole flying kit, as she gives it: a wing of about 1.8 kg with unsheathed lines, a 300 g harness "
            "and a reserve of about 800 g: under 3 kg in all. All of it, with shoes and a waterproof, fits in one 24-litre "
            "bike bag; every piece is more than six years old.")


def kit_scale(d, x0, x1, y, h, step):
    X = lambda kg: x0 + kg / 3.0 * (x1 - x0)
    for g in range(0, 3001, 250):
        d.line((X(g / 1000), y - 14), (X(g / 1000), y + h + 14), "hair" if g % 1000 == 0 else "ghost")
        if g % step == 0:
            d.text((X(g / 1000), y + h + 32), "{:g} kg".format(g / 1000), "tb", "middle")
    for name, note, a, b, c, op in KIT:
        rect(d, X(a), y, X(b) - X(a) - 2, h, c, op)
    d.line((X(3.0), y - 30), (X(3.0), y + h + 16), "accent")
    return X


def kit():
    d = K.Drawing(1200, 280, "cq-kit", "Sandrine Roy's flying kit", KIT_DESC, inline_css=False)
    d.backdrop(glow=(900, 130), glow_r=280, sheet=False)
    X = kit_scale(d, 260, 1080, 110, 44, 500)
    for name, note, a, b, c, op in KIT:
        xm = (X(a) + X(b)) / 2
        d.text((X(a) + 6, 92), name, "lab")
        d.text((X(a) + 6 if name != "Harness" else X(a) + 6, 76 if name == "Harness" else 76), note, "sub")
    d.text((X(3.0) + 10, 100), "under 3 kg", "val")
    d.text((X(3.0) + 10, 116), "the whole setup", "sub")
    d.text((240, 128), "Sandrine Roy's", "lab", "end")
    d.text((240, 144), "flying kit", "sub", "end")
    d.text((600, 250), "all of it, with shoes and a waterproof, fits in one 24-litre bike bag; every piece is more than six years old",
           "sub", "middle")
    return d


def kit_p():
    d = K.Drawing(360, 380, "cq-kit-p", "Sandrine Roy's flying kit", KIT_DESC, inline_css=False)
    d.text((16, 24), "Sandrine Roy's flying kit", "lab")
    X = kit_scale(d, 16, 300, 70, 28, 1000)
    d.text((X(3.0) - 6, 52), "under 3 kg", "val", "end")
    for i, (name, note, a, b, c, op) in enumerate(KIT):
        y = 172 + 40 * i
        rect(d, 16, y - 10, 10, 10, c, op)
        d.text((34, y), name, "lab")
        d.text((34, y + 16), note, "sub")
    lines(d, 16, 306, "All of it, with shoes and a waterproof, fits in one 24-litre bike bag; every piece is more than six years old.", 48)
    return d


# ---------------------------------------------------------------- living the dream: the team
TEAM_DESC = ("Damien Lacaze's X-Alps team. The first time there were three of them; in 2025 there were nine: six supporters in "
             "two vans, three in each, the athlete, his coach Julien at home on the radio and live tracking, and his mental "
             "coach Delphine on the phone. Among the supporters, the Sherpa walks with him, carries his non-mandatory kit "
             "and flies down: fit, and a good pilot.")


def person(d, p, accent=False, r=7):
    d.circle(p, r, "accent" if accent else "detail", fill="card")
    d.dot(p, r * .45, accent)


def team():
    d = K.Drawing(1200, 300, "cq-team", "Damien Lacaze's X-Alps team", TEAM_DESC, inline_css=False)
    d.backdrop(glow=(700, 140), glow_r=300, sheet=False)
    d.text((40, 40), "The first time", "lab")
    for i in range(3):
        person(d, (60 + 34 * i, 130))
    d.text((40, 178), "a team of three", "tv")
    d.line((220, 30), (220, 250), "ghost")
    d.text((260, 40), "2025: nine", "val")
    for k, (vx, lab) in enumerate(((270, "van one"), (440, "van two"))):
        box(d, vx, 100, 140, 64)
        for i in range(3):
            person(d, (vx + 30 + 40 * i, 132))
        d.text((vx + 70, 184), lab, "sub", "middle")
    d.text((270, 86), "six supporters on the road", "tv")
    d.line((590, 132), (680, 132), "ghost")
    person(d, (710, 132), True, 12)
    d.text((710, 170), "Damien", "lab", "middle")
    d.text((710, 186), "racing", "sub", "middle")
    for x, name, r1, r2 in ((900, "Julien", "coach, at home", "radio and live tracking"),
                            (1080, "Delphine", "mental coach", "by phone when needed")):
        d.line((726, 132), (x - 10, 132), "ghost")
        person(d, (x, 132))
        d.text((x, 170), name, "lab", "middle")
        d.text((x, 186), r1, "sub", "middle")
        d.text((x, 200), r2, "sub", "middle")
    d.text((600, 270), "among the supporters, the Sherpa walks with him, carries his non-mandatory kit and flies down: fit, and a good pilot",
           "sub", "middle")
    return d


def team_p():
    d = K.Drawing(360, 560, "cq-team-p", "Damien Lacaze's X-Alps team", TEAM_DESC, inline_css=False)
    d.text((16, 24), "The first time: three", "lab")
    for i in range(3):
        person(d, (30 + 30 * i, 52))
    d.line((16, 84), (344, 84), "ghost")
    d.text((16, 112), "2025: nine", "val")
    d.text((16, 134), "six supporters on the road", "tv")
    for k, lab in enumerate(("van one", "van two")):
        vx = 16 + 172 * k
        box(d, vx, 148, 156, 56)
        for i in range(3):
            person(d, (vx + 36 + 42 * i, 176))
        d.text((vx + 78, 222), lab, "sub", "middle")
    person(d, (40, 272), True, 12)
    d.text((64, 268), "Damien", "lab")
    d.text((64, 284), "racing", "sub")
    for i, (name, r1, r2) in enumerate((("Julien", "coach, at home", "radio and live tracking"),
                                        ("Delphine", "mental coach", "by phone when needed"))):
        y = 330 + 60 * i
        person(d, (40, y))
        d.text((64, y - 4), name, "lab")
        d.text((64, y + 12), r1 + ", " + r2, "sub")
    lines(d, 16, 470, "Among the supporters, the Sherpa walks with him, carries his non-mandatory kit and flies down: fit, and a good pilot.", 48)
    return d


# ---------------------------------------------------------------- resources: where the footage comes from
CAM_DESC = ("Where the footage comes from. A pilot in flight with the camera positions the filmmakers describe: a helmet "
            "mount, a selfie stick or gimbal, a drone flown by a partner, and a compact camera on a tripod on the ground. "
            "Schematic.")
CAMS = [("helmet mount", "easy, but a line can catch it"), ("stick or gimbal", "the pilot in frame"),
        ("drone", "flown by someone else"), ("compact camera on a tripod", "most of the ground story")]


def flyer(d, px, py, s=1.0):
    arc = [(px + 110 * s * math.cos(t), py - 75 * s - 35 * s * math.sin(t)) for t in [.15 + (2.84 * k / 30) for k in range(31)]]
    d.poly(arc + [(x, y + 7 * s) for x, y in arc[::-1]], "outline", True, "card")
    for k in range(0, 31, 5):
        d.line((arc[k][0], arc[k][1] + 7 * s), (px, py), "ghost")
    d.circle((px, py + 4 * s), 6 * s, "outline", fill="card")
    d.poly([(px - 7 * s, py + 10 * s), (px + 20 * s, py + 13 * s), (px + 30 * s, py + 28 * s), (px - 5 * s, py + 26 * s)], "outline", True, "card")


def cam(d, x, y, s=1.0):
    rect(d, x - 5 * s, y - 4 * s, 10 * s, 8 * s, "fa")


def cameras():
    d = K.Drawing(1200, 320, "cq-cams", "Where the footage comes from", CAM_DESC, inline_css=False)
    d.backdrop(glow=(575, 150), glow_r=280, sheet=False)
    d.line((60, 260), (1140, 260), "hair")
    px, py = 575, 150
    flyer(d, px, py)
    cam(d, px, py - 4)
    d.text((px - 20, py - 18), CAMS[0][0], "val", "end")
    d.text((px - 20, py - 2), CAMS[0][1], "sub", "end")
    d.line((px + 15, py + 15), (px + 95, py - 20), "detail")
    cam(d, px + 97, py - 22)
    d.text((px + 110, py - 22), CAMS[1][0], "val")
    d.text((px + 110, py - 6), CAMS[1][1], "sub")
    dx, dy = 925, 85
    cam(d, dx, dy, 1.4)
    for s_ in (-1, 1):
        d.line((dx + s_ * 8, dy), (dx + s_ * 20, dy - 5), "detail")
        d.line((dx + s_ * 14, dy - 6), (dx + s_ * 26, dy - 6), "outline")
    d.line((dx - 10, dy + 5), (px + 60, py - 30), "ghost")
    d.text((dx, dy + 26), CAMS[2][0], "val", "middle")
    d.text((dx, dy + 42), CAMS[2][1], "sub", "middle")
    tx = 210
    for s_ in (-1, 0, 1):
        d.line((tx, 220), (tx + s_ * 17, 260), "outline")
    cam(d, tx, 214, 1.8)
    d.line((tx + 10, 215), (px - 30, py + 20), "ghost")
    d.text((tx, 284), CAMS[3][0], "val", "middle")
    d.text((tx, 300), CAMS[3][1], "sub", "middle")
    return d


def cameras_p():
    d = K.Drawing(360, 500, "cq-cams-p", "Where the footage comes from", CAM_DESC, inline_css=False)
    px, py = 180, 120
    flyer(d, px, py, .9)
    marks = [(px, py - 4), (px + 88, py - 20), (300, 40), (60, 210)]
    cam(d, *marks[0])
    d.line((px + 13, py + 13), (px + 86, py - 18), "detail")
    cam(d, *marks[1])
    cam(d, *marks[2], 1.4)
    for s_ in (-1, 1):
        d.line((300 + s_ * 14, 34), (300 + s_ * 26, 34), "outline")
    for s_ in (-1, 0, 1):
        d.line((60, 216), (60 + s_ * 15, 250), "outline")
    cam(d, *marks[3], 1.6)
    d.line((16, 250), (344, 250), "hair")
    for i, (m, (a, b)) in enumerate(zip(marks, CAMS)):
        d.text((m[0] + 8, m[1] - 10), str(i + 1), "vn")
        y = 300 + 48 * i
        d.text((16, y), str(i + 1), "vn")
        d.text((36, y), a, "val")
        d.text((36, y + 17), b, "sub")
    d.text((344, 494), "schematic", "tb", "end")
    return d


# ---------------------------------------------------------------- risk vs reward: Will Gadd's ladder
LADDER = [("Bumps and bruises", "Play. Pay attention, nothing more.", .22, "fh"),
          ("Hospital", "Slow down, keep a hand on the wall, choose the inside of the trail.", .55, "fa"),
          ("Death", "Find the line that removes this row before you look at the odds.", 1.0, "fa")]
LADDER_DESC = ("Will Gadd's three hazard levels, as a ladder: bumps and bruises, play; hospital, slow down, keep a hand on the "
               "wall, choose the inside of the trail; death, find the line that removes this row before you look at the "
               "odds. Probability is the second question: the row decides, not the odds.")


def ladder():
    d = K.Drawing(1200, 330, "cq-ladder", "Three hazard levels", LADDER_DESC, inline_css=False)
    d.backdrop(glow=(700, 250), glow_r=300, sheet=False)
    for i, (name, act, w, c) in enumerate(LADDER):
        y = 30 + 88 * i
        box(d, 60, y, 900, 72, r=4)
        rect(d, 60, y, 5, 72, c, .5 if i == 1 else .95)
        d.text((86, y + 30), name, "tt")
        d.text((86, y + 54), act, "tv")
        rect(d, 700, y + 26, 220 * w, 6, c, .5 if i == 1 else .95)
        d.line((700, y + 42), (920, y + 42), "ghost")
        d.text((700, y + 58), "consequence", "tb")
    cx, cy = 1070, 160
    for r in (50, 36):
        d.arc((cx, cy), r, r, 180, 360, "hair")
    for k in range(0, 181, 30):
        a = math.radians(k)
        d.line((cx + 36 * math.cos(a), cy - 36 * math.sin(a)), (cx + 50 * math.cos(a), cy - 50 * math.sin(a)), "hair")
    d.arrow((cx, cy), (cx + 42 * math.cos(math.radians(140)), cy - 42 * math.sin(math.radians(140))), "detail", 7)
    d.text((cx, cy + 22), "probability", "sub", "middle")
    d.text((cx, cy + 38), "the second question", "tb", "middle")
    return d


def ladder_p():
    d = K.Drawing(360, 460, "cq-ladder-p", "Three hazard levels", LADDER_DESC, inline_css=False)
    for i, (name, act, w, c) in enumerate(LADDER):
        y = 10 + 124 * i
        box(d, 16, y, 328, 112, r=4)
        rect(d, 16, y, 5, 112, c, .5 if i == 1 else .95)
        d.text((34, y + 28), name, "tt")
        yy = lines(d, 34, y + 50, act, 42, "tv", 15)
        rect(d, 34, y + 94, 180 * w, 5, c, .5 if i == 1 else .95)
        d.text((220, y + 100), "consequence", "tb")
    d.text((16, 400), "Probability: the second question.", "sub")
    d.text((16, 416), "The row decides, not the odds.", "sub")
    return d


# ---------------------------------------------------------------- risk vs reward: altitude
ALT_CARDS = [("Cold", "Shivering multiplies the oxygen your body burns by about five. Staying warm is margin.", "x5"),
             ("Time", "Each hour up high draws down bandwidth, and repeated days stack the fatigue.", "hrs"),
             ("After", "Back down low you feel better, but you are not back to full for up to 90 minutes.", "90 min")]
ALT_DESC = ("The altitude scale where hypoxia starts to matter, from Dr Matt Wilkes: fine low down; most pilots start to be "
            "affected at 3,000 to 3,500 m; above that, impaired and not aware of it. General aviation's rule: 30 minutes "
            "above 3,000 m, or any time above 4,000 m. Beside it, computed from the standard atmosphere, the oxygen in each "
            "breath as a share of sea level: about 69% at 3,000 m and 47% at 6,000 m. Three things shrink the margin: cold "
            "(shivering multiplies the oxygen burnt by about five), time, and the 90 minutes after coming down. The check: "
            "a note on the cockpit asking what you are thinking; mood, thermalling precision and speech change first.")


def o2(m):
    return isa(m)[0] / isa(0)[0]          # the air's oxygen fraction is constant; each breath holds less of it with the pressure


def alt_scale(d, x, top, bot, w):
    Y = lambda m: bot - (bot - top) * m / 6000
    d.line((x, top), (x, bot), "detail")
    for m in range(0, 6001, 1000):
        d.line((x - 6, Y(m)), (x + 6, Y(m)), "hair")
        d.text((x - 12, Y(m) + 4), "{:,} m".format(m), "tb", "end")
    rect(d, x + 10, Y(3500), w, Y(3000) - Y(3500), "fa", .22)
    rect(d, x + 10, Y(6000), w, Y(3500) - Y(6000), "fa", .38)
    d.text((x + 20, Y(3250) + 4), "most pilots start to be affected", "tv")
    d.text((x + 20, Y(4750) + 4), "impaired, and not aware of it", "tv")
    d.text((x + 20, Y(1500) + 4), "fine", "sub")
    d.line((x + 10, Y(2600)), (x + 10 + w, Y(2600)), "ghost")
    # the computed scale: oxygen per breath, share of sea level
    xs = x + 10 + w + 20
    pts = [(xs + 60 * o2(m), Y(m)) for m in range(0, 6001, 200)]
    d.poly(pts, "accent")
    for m in (0, 3000, 6000):
        d.dot((xs + 60 * o2(m), Y(m)), 3, True)
        d.text((xs + 60 * o2(m) + 8, Y(m) + 4), "%d%%" % round(o2(m) * 100), "val")
    return Y, xs


def altitude():
    d = K.Drawing(1200, 420, "cq-alt", "Where hypoxia starts to matter", ALT_DESC, inline_css=False)
    d.backdrop(glow=(300, 120), glow_r=260, sheet=False)
    Y, xs = alt_scale(d, 100, 30, 360, 290)
    d.text((110, Y(2600) - 8), "general aviation: 30 min above 3,000 m, or any time above 4,000 m", "sub")
    d.text((xs, 386), "oxygen per breath,", "tb")
    d.text((xs, 400), "share of sea level (computed)", "tb")
    for i, (h, b, big) in enumerate(ALT_CARDS):
        cx = 620 + i * 190
        box(d, cx, 30, 170, 210, r=4)
        rect(d, cx, 30, 170, 3, "fa")
        d.text((cx + 16, 80), big, "tt")
        d.text((cx + 16, 110), h, "lab")
        lines(d, cx + 16, 134, b, 25, "sub", 15)
    d.text((620, 290), "The check: a note on the cockpit asking what you are thinking.", "tv")
    d.text((620, 308), "Mood, thermalling precision and speech change first.", "sub")
    return d


def altitude_p():
    d = K.Drawing(360, 740, "cq-alt-p", "Where hypoxia starts to matter", ALT_DESC, inline_css=False)
    Y, xs = alt_scale(d, 60, 20, 330, 150)
    lines(d, 16, 360, "General aviation: 30 min above 3,000 m, or any time above 4,000 m. Orange line: oxygen per breath, share of sea level, computed.", 48)
    y = 420
    for h, b, big in ALT_CARDS:
        d.text((16, y), big, "tt")
        d.text((96, y), h, "lab")
        y = lines(d, 96, y + 18, b, 36, "sub", 15) + 18
    lines(d, 16, y + 8, "The check: a note on the cockpit asking what you are thinking. Mood, thermalling precision and speech change first.", 48, "tv", 16)
    return d


# ---------------------------------------------------------------- storytellers: then and now
THEN = [("Cross-country", ["a handful in the club;", "20 to 50 km flights in the UK"],
         ["at least half of UK club pilots expect to;", "keen pilots fly 100 km in their first couple of years"]),
        ("Hours", ["over 100 hours made you a rock star;", "a first logbook full of one-minute flights"],
         ["150 hours in your first year,", "if you live in the right country"]),
        ("Competition wings", ["expect massive collapses", "on every good day"], ["vastly improved,", "and safer"])]
THEN_DESC = ("Then and now, as Eddie Colfox tells it. Cross-country: in the early 1990s a handful in the club, 20 to 50 km "
             "flights in the UK; now at least half of UK club pilots expect to, and keen pilots fly 100 km in their first "
             "couple of years. Hours: over 100 made you a rock star, a first logbook full of one-minute flights; now 150 "
             "hours in your first year, if you live in the right country. Competition wings: expect massive collapses on "
             "every good day; now vastly improved, and safer.")


def then():
    d = K.Drawing(1200, 300, "cq-then", "Then and now", THEN_DESC, inline_css=False)
    d.backdrop(glow=(900, 150), glow_r=300, sheet=False)
    d.text((300, 30), "Early 1990s", "vw")
    d.text((740, 30), "Now", "val")
    for i, (lab, a, b) in enumerate(THEN):
        y = 70 + 80 * i
        d.line((280, y - 26), (1160, y - 26), "ghost")
        d.text((260, y), lab, "lab", "end")
        for j, s in enumerate(a):
            d.text((300, y + 18 * j), s, "sub")
        d.arrow((650, y + 4), (710, y + 4), "accent", 8)
        for j, s in enumerate(b):
            d.text((740, y + 18 * j), s, "tv")
    return d


def then_p():
    d = K.Drawing(360, 520, "cq-then-p", "Then and now", THEN_DESC, inline_css=False)
    y = 20
    for lab, a, b in THEN:
        d.text((16, y), lab, "lab")
        d.text((16, y + 22), "Early 1990s", "tb")
        yy = lines(d, 16, y + 40, " ".join(a), 48, "sub", 15)
        d.text((16, yy + 8), "Now", "tb")
        yy = lines(d, 16, yy + 26, " ".join(b), 46, "tv", 15)
        y = yy + 26
        d.line((16, y - 16), (344, y - 16), "ghost")
    return d


# ---------------------------------------------------------------- storytellers: two collisions, one height scale
HEIGHTS_DESC = ("Marko Milutinovic's two mid-air collisions on one height scale. France, 2023 Worlds: hit at about 600 m above "
                "the ground (it felt like ten seconds, it lasted three); the wing stayed open but had no brake pressure, and "
                "he went down to land. Spain, 2024 Europeans: hit at more than 1,000 m, tangled, spinning, a slow backflip, "
                "the reserve thrown at 400 to 600 m, and a landing between two olive trees: a gamble either way.")


def heights_scale(d, x0, x1, top, bot, labels=True):
    Y = lambda m: bot - m / 1200 * (bot - top)
    for m in range(0, 1201, 200):
        d.line((x0, Y(m)), (x1, Y(m)), "hair" if m == 0 else "ghost")
        if labels:
            d.text((x0 - 8, Y(m) + 4), "{:,} m".format(m), "tb", "end")
    return Y


def spin(d, x, Y):
    pts = [(x + 9 * math.sin(t * 40), Y(1050 - 550 * t)) for t in [k / 120 for k in range(121)]]
    d.poly(pts, "accent")


def heights():
    d = K.Drawing(1200, 360, "cq-heights", "Two collisions, one height scale", HEIGHTS_DESC, inline_css=False)
    d.backdrop(glow=(820, 150), glow_r=260, sheet=False)
    Y = heights_scale(d, 150, 1160, 50, 320)
    d.text((142, 30), "above the ground", "tb", "end")
    xf = 360
    d.text((xf, 30), "France, 2023 Worlds", "lab", "middle")
    d.path("M%s,%s L%s,%s" % (f(xf), f(Y(600)), f(xf), f(Y(0))), "accent", extra=' style="stroke-dasharray:5 4"')
    d.dot((xf, Y(600)), 6, True)
    d.text((xf + 16, Y(600) - 4), "hit at about 600 m", "tv")
    d.text((xf + 16, Y(600) + 12), "felt like ten seconds, lasted three", "sub")
    d.text((xf + 16, Y(330)), "wing open but no brake pressure:", "sub")
    d.text((xf + 16, Y(330) + 15), "he went down to land", "sub")
    xs = 820
    d.text((xs, 30), "Spain, 2024 Europeans", "lab", "middle")
    d.dot((xs, Y(1050)), 6, True)
    d.text((xs + 16, Y(1050) - 4), "hit at more than 1,000 m", "tv")
    d.text((xs + 16, Y(1050) + 12), "tangled, spinning, a slow backflip", "sub")
    spin(d, xs, Y)
    rect(d, xs - 30, Y(600), 60, Y(400) - Y(600), "fa", .18)
    d.text((xs + 40, Y(500)), "reserve thrown at 400 to 600 m", "val")
    d.text((xs + 40, Y(500) + 15), "the landing was a gamble either way", "sub")
    d.path("M%s,%s L%s,%s" % (f(xs), f(Y(450)), f(xs + 20), f(Y(0))), "detail", extra=' style="stroke-dasharray:3 4"')
    d.text((xs + 30, Y(0) - 8), "between two olive trees", "sub")
    return d


def heights_p():
    d = K.Drawing(360, 640, "cq-heights-p", "Two collisions, one height scale", HEIGHTS_DESC, inline_css=False)
    Y = heights_scale(d, 60, 344, 40, 330)
    d.text((16, 20), "height above the ground", "tb")
    xf, xs = 130, 260
    d.path("M%s,%s L%s,%s" % (f(xf), f(Y(600)), f(xf), f(Y(0))), "accent", extra=' style="stroke-dasharray:5 4"')
    d.dot((xf, Y(600)), 6, True)
    d.text((xf, Y(600) - 12), "1", "vn", "middle")
    d.dot((xs, Y(1050)), 6, True)
    d.text((xs, Y(1050) - 12), "2", "vn", "middle")
    spin(d, xs, Y)
    rect(d, xs - 22, Y(600), 44, Y(400) - Y(600), "fa", .18)
    d.path("M%s,%s L%s,%s" % (f(xs), f(Y(450)), f(xs + 14), f(Y(0))), "detail", extra=' style="stroke-dasharray:3 4"')
    y = 370
    d.text((16, y), "1", "vn")
    d.text((36, y), "France, 2023 Worlds", "lab")
    y = lines(d, 36, y + 18, "Hit at about 600 m; felt like ten seconds, lasted three. Wing open but no brake pressure: he went down to land.", 44)
    y += 16
    d.text((16, y), "2", "vn")
    d.text((36, y), "Spain, 2024 Europeans", "lab")
    lines(d, 36, y + 18, "Hit at more than 1,000 m; tangled, spinning, a slow backflip. Reserve thrown at 400 to 600 m (the band); the landing, between two olive trees, was a gamble either way.", 44)
    return d


# ---------------------------------------------------------------- world cups: how a race task is scored
TASK_DESC = ("How a race task is scored. A course from launch through the start cylinder (SSS), turnpoints, the end of speed "
             "section (ESS) and goal, with the three games marked: distance along the whole course, launch to goal; time "
             "and leading only between the start of speed and its end: how fast, and how far in front.")


def course(d, s, ox, oy):
    Pt = {"launch": (200, 300), "SSS": (520, 300), "TP1": (1000, 180), "TP2": (1480, 330), "ESS": (1900, 250), "goal": (2160, 250)}
    rad = {"SSS": 150, "TP1": 90, "TP2": 90, "ESS": 110}
    T = lambda p: (ox + p[0] * s, oy + p[1] * s)
    for k, r in rad.items():
        c = T(Pt[k])
        if k in ("SSS", "ESS"):
            d.raw('<circle class="fa" cx="%s" cy="%s" r="%s" style="fill-opacity:.07"/>' % (f(c[0]), f(c[1]), f(r * s)))
        d.circle(c, r * s, "detail")
    route = [Pt["launch"], (Pt["SSS"][0] + 150, 300), (Pt["TP1"][0], 270), (Pt["TP2"][0] - 60, 260), (Pt["ESS"][0] - 110, 250), Pt["goal"]]
    d.poly([T(p) for p in route], "outline")
    for k, p in Pt.items():
        q = T(p)
        d.dot(q, 3.5, k in ("SSS", "ESS", "goal"))
        d.text((q[0], q[1] - rad.get(k, 30) * s - 8), k, "lab" if k in ("SSS", "ESS", "goal") else "sub", "middle")
    g = T(Pt["goal"])
    d.line((g[0], g[1] - 16), (g[0], g[1] + 16), "outline")
    return T


def task():
    d = K.Drawing(1200, 340, "cq-task", "How a race task is scored", TASK_DESC, inline_css=False)
    d.backdrop(glow=(600, 130), glow_r=300, sheet=False)
    T = course(d, .5, 0, -10)
    a, b = T((200, 0))[0], T((2160, 0))[0]
    rect(d, a, 236, b - a, 4, "fw", .8)
    d.text((a, 258), "Distance", "lab")
    d.text((a + 80, 258), "how far along the course you got, launch to goal", "sub")
    a, b = T((670, 0))[0], T((1790, 0))[0]
    rect(d, a, 282, b - a, 4, "fa", .9)
    d.text((a, 304), "Time and leading", "val")
    d.text((a, 320), "only between the start of speed (SSS) and its end (ESS): how fast, and how far in front", "sub")
    return d


def task_p():
    d = K.Drawing(360, 420, "cq-task-p", "How a race task is scored", TASK_DESC, inline_css=False)
    T = course(d, .145, 4, 10)
    a, b = T((200, 0))[0], T((2160, 0))[0]
    rect(d, a, 110, b - a, 4, "fw", .8)
    a2, b2 = T((670, 0))[0], T((1790, 0))[0]
    rect(d, a2, 124, b2 - a2, 4, "fa", .9)
    d.text((16, 180), "Distance", "lab")
    lines(d, 16, 198, "how far along the course you got, launch to goal (white)", 46)
    d.text((16, 250), "Time and leading", "val")
    lines(d, 16, 268, "only between the start of speed (SSS) and its end (ESS): how fast, and how far in front (orange)", 46)
    return d


# ---------------------------------------------------------------- brand stories: where the tubercles go
TUB_DESC = ("Where the tubercles go, after Gin Seok Song. Two planforms, leading edge at the top. Left, the first try, with "
            "tubercles along the whole span: good glide, but the tips stall early and the wing spun early. Right, tubercles "
            "on the central 60% of the span; the tips keep a plain leading edge.")


def planform(d, cx, y0, span, ch, frac, accent):
    n = 400
    xs = [-1 + 2 * i / (n - 1) for i in range(n)]
    c = [ch * max(0, 1 - x * x) ** .42 for x in xs]
    te = [y0 + .4 * ci + 8 * x * x for x, ci in zip(xs, c)]
    le = []
    for x, ci, t in zip(xs, c, te):
        bump = 3.5 * max(0, math.sin(x * math.pi * 30)) ** .8 if abs(x) <= frac else 0
        le.append(t - ci - bump)
    X = [cx + span / 2 * x for x in xs]
    d.poly(list(zip(X, le)) + list(zip(X, te))[::-1], "detail", True, "card")
    for k in range(0, n, 20):
        d.line((X[k], le[k]), (X[k], te[k]), "ghost")
    seg = [(X[i], le[i]) for i in range(n) if abs(xs[i]) <= frac]
    d.poly(seg, "accent" if accent else "outline")
    return X, le


def tubercles():
    d = K.Drawing(1200, 280, "cq-tub", "Where the tubercles go", TUB_DESC, inline_css=False)
    d.backdrop(glow=(880, 140), glow_r=280, sheet=False)
    X, le = planform(d, 320, 170, 490, 95, 1.0, False)
    for k in (20, 379):
        d.circle((X[k], le[k] + 8), 17, "accent")
    d.text((320, 40), "Tubercles along the whole span", "lab", "middle")
    d.text((320, 58), "good glide, but the tips stall early", "sub", "middle")
    planform(d, 880, 170, 490, 95, .6, True)
    d.line((880 - 245 * .6, 90), (880 + 245 * .6, 90), "accent")
    for s_ in (-1, 1):
        d.line((880 + s_ * 245 * .6, 84), (880 + s_ * 245 * .6, 96), "accent")
    d.text((880, 80), "central 60%", "val", "middle")
    d.text((880, 40), "Tubercles on the central 60%", "lab", "middle")
    d.text((880, 58), "the tips keep a plain leading edge", "sub", "middle")
    d.text((1180, 270), "planforms, leading edge at the top", "tb", "end")
    return d


def tubercles_p():
    d = K.Drawing(360, 420, "cq-tub-p", "Where the tubercles go", TUB_DESC, inline_css=False)
    d.text((16, 22), "Tubercles along the whole span", "lab")
    d.text((16, 40), "good glide, but the tips stall early", "sub")
    X, le = planform(d, 180, 150, 320, 64, 1.0, False)
    for k in (20, 379):
        d.circle((X[k], le[k] + 6), 13, "accent")
    d.text((16, 222), "Tubercles on the central 60%", "lab")
    d.text((16, 240), "the tips keep a plain leading edge", "sub")
    planform(d, 180, 350, 320, 64, .6, True)
    d.line((180 - 160 * .6, 270), (180 + 160 * .6, 270), "accent")
    d.text((180, 262), "central 60%", "val", "middle")
    d.text((344, 412), "planforms, leading edge at the top", "tb", "end")
    return d


# ---------------------------------------------------------------- brand stories: the mirror effect
RESCUE_DESC = ("The mirror effect and the stand-up alternative, after Eric Roussel. Left, the reserve bridled to the shoulders "
               "pulls one way while the paraglider, still on the main carabiners, pulls the other: the pilot is stretched "
               "between them on their back. Right, reserve and wing join at the same point and the pilot sits upright, legs "
               "free, hands on the risers. Schematic.")


def res_canopy(d, cx, cy, r):
    top = [(cx + r * math.cos(t), cy + .55 * r * math.sin(t)) for t in [math.pi + math.pi * k / 30 for k in range(31)]]
    d.poly(top, "outline", True, "card")
    return [(cx - r, cy), (cx - r / 2, cy), (cx + r / 2, cy), (cx + r, cy)]


def res_wing(d, cx, cy, w, tilt):
    a = math.radians(tilt)
    pts = []
    for k in range(41):
        t = .12 * math.pi + .76 * math.pi * k / 40
        x, y = w / 2 * math.cos(t) / math.cos(.12 * math.pi), -.28 * w * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    d.poly(pts, "outline")
    return [pts[3], pts[20], pts[37]]


def mirror(d, ox, oy, s):
    T = lambda x, y: (ox + x * s, oy + y * s)
    a = math.radians(8)
    head = T(520, 470)
    hip = (head[0] + 70 * s * math.cos(a), head[1] + 70 * s * math.sin(a))
    sh = (head[0] + 22 * s * math.cos(a), head[1] + 22 * s * math.sin(a))
    for p in res_canopy(d, *T(300, 250), 120 * s):
        d.line(p, sh, "ghost")
    for p in res_wing(d, *T(880, 250), 300 * s, 10):
        d.line(p, hip, "ghost")
    d.circle(head, 13 * s, "outline", fill="card")
    d.line((head[0] + 14 * s, head[1] + 2 * s), hip, "outline")
    d.line(hip, (hip[0] + 70 * s, hip[1] + 18 * s), "outline")
    d.arrow(T(430, 400), T(330, 330), "accent", 9)
    d.arrow(T(720, 400), T(820, 320), "accent", 9)
    return T


def standup(d, ox, oy, s):
    T = lambda x, y: (ox + x * s, oy + y * s)
    J = T(1800, 420)
    for p in res_canopy(d, *T(1560, 250), 120 * s):
        d.line(p, J, "ghost")
    for p in res_wing(d, *T(2050, 250), 300 * s, 8):
        d.line(p, J, "ghost")
    head = T(1800, 440)
    seat = T(1800, 530)
    knee = T(1846, 538)
    d.circle(head, 13 * s, "outline", fill="card")
    d.poly([(head[0], head[1] + 14 * s), seat, knee, T(1850, 600)], "outline")
    d.dot(J, 4.5, True)
    return T


def rescue():
    d = K.Drawing(1200, 360, "cq-rescue", "The mirror effect, and one attachment point", RESCUE_DESC, inline_css=False)
    d.backdrop(glow=(900, 200), glow_r=280, sheet=False)
    T = mirror(d, 0, 0, .5)
    d.text((300, 30), "Reserve on the shoulders", "lab", "middle")
    d.text((300, 48), "the two canopies pull apart and the pilot ends up on their back", "sub", "middle")
    d.text((150, 88), "reserve", "sub", "middle")
    d.text((450, 72), "paraglider", "sub", "middle")
    d.text((300, 318), "mirror effect", "val", "middle")
    d.line((600, 60), (600, 330), "ghost")
    T2 = standup(d, 0, 0, .5)
    d.text((900, 30), "Reserve and wing at the same point", "lab", "middle")
    d.text((900, 48), "the pilot sits upright, legs free, hands on the risers", "sub", "middle")
    d.text((780, 88), "reserve", "sub", "middle")
    d.text((1030, 72), "paraglider", "sub", "middle")
    d.text((912, 206), "one attachment point", "val")
    d.text((1180, 350), "schematic", "tb", "end")
    return d


def rescue_p():
    d = K.Drawing(360, 560, "cq-rescue-p", "The mirror effect, and one attachment point", RESCUE_DESC, inline_css=False)
    d.text((16, 22), "Reserve on the shoulders", "lab")
    mirror(d, -30, 30, .32)
    d.text((16, 256), "mirror effect", "val")
    lines(d, 16, 274, "the two canopies pull apart and the pilot ends up on their back", 48)
    d.line((16, 300), (344, 300), "ghost")
    d.text((16, 326), "Reserve and wing at the same point", "lab")
    J = standup(d, -470, 316, .34)
    d.text((196, 470), "one attachment point", "val")
    lines(d, 16, 530, "the pilot sits upright, legs free, hands on the risers", 48)
    return d


# ---------------------------------------------------------------- navigators: a glide in thirds
THIRDS = [("Top third", "look at the clouds"), ("Middle third", "clouds and the ground"),
          ("Bottom third", "ground triggers only, three or four options ahead")]
THIRDS_DESC = ("A long glide managed in thirds, after Godfrey Wenness. Arriving in the top third of the height band, look at "
               "the clouds; in the middle third, clouds and ground; in the bottom third, only ground triggers, with three or "
               "four options ahead: options, not a single hope. Schematic, height above ground.")


def thirds_fig(d, x0, x1, top, g, s, compact=False):
    third = (g - top) / 3
    for i, (lab, sub) in enumerate(THIRDS):
        y0 = top + i * third
        rect(d, x0, y0, x1 - x0, third, "fa" if i == 2 else "fh", .07 if i == 2 else .03)
        d.line((x0, y0), (x1, y0), "ghost")
        d.text((x0 + 10, y0 + 22), lab, "val" if i == 2 else "lab")
        if not compact:
            d.text((x0 + 10, y0 + 38), sub, "sub")
    d.line((x0, g), (x1, g), "detail")
    for cx in (x0 + (x1 - x0) * .2, x0 + (x1 - x0) * .5, x0 + (x1 - x0) * .8):
        for dx, dy, r in ((0, 0, 19), (20, 4, 15), (-19, 5, 14), (9, -9, 13)):
            d.circle((cx + dx * s, top - 26 * s + dy * s), r * s, "detail", fill="card")
    path = [(x0 + (x1 - x0) * .2, top + 10), (x0 + (x1 - x0) * .4, top + third * 1.2), (x0 + (x1 - x0) * .58, top + third * 2.1),
            (x0 + (x1 - x0) * .75, g - 34)]
    d.poly(path, "outline")
    d.head(path[-1], (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]), 9)
    return path


def thirds():
    d = K.Drawing(1200, 320, "cq-thirds", "A glide in thirds", THIRDS_DESC, inline_css=False)
    d.backdrop(glow=(1000, 260), glow_r=220, sheet=False)
    thirds_fig(d, 60, 1150, 70, 280, .9)
    for tx, lab in ((930, "field on the upslope"), (1020, "tree line"), (1100, "creek bend")):
        d.dot((tx, 276), 4, True)
        d.text((tx, 300), lab, "sub", "middle")
    d.text((880, 262), "options, not a single hope", "val", "end")
    d.text((1180, 316), "schematic, height above ground", "tb", "end")
    return d


def thirds_p():
    d = K.Drawing(360, 470, "cq-thirds-p", "A glide in thirds", THIRDS_DESC, inline_css=False)
    thirds_fig(d, 16, 344, 60, 290, .6, compact=True)
    for tx in (280, 310, 336):
        d.dot((tx, 286), 3.5, True)
    y = 330
    for i, (lab, sub) in enumerate(THIRDS):
        d.text((16, y), lab, "val" if i == 2 else "lab")
        y = lines(d, 16, y + 17, sub + ("; options, not a single hope" if i == 2 else ""), 48) + 12
    d.text((344, 464), "schematic", "tb", "end")
    return d


def registry():
    return {
        "kb-living-the-dream-chain": (chain, chain_p),
        "kb-living-the-dream-kit": (kit, kit_p),
        "kb-living-the-dream-team": (team, team_p),
        "kb-resources-tools-tips-cameras": (cameras, cameras_p),
        "kb-risk-vs-reward-ladder": (ladder, ladder_p),
        "kb-risk-vs-reward-altitude": (altitude, altitude_p),
        "kb-storytellers-then": (then, then_p),
        "kb-storytellers-heights": (heights, heights_p),
        "kb-world-cups-task": (task, task_p),
        "kb-brand-stories-tubercles": (tubercles, tubercles_p),
        "kb-brand-stories-rescue": (rescue, rescue_p),
        "kb-navigators-thirds": (thirds, thirds_p),
    }
