#!/usr/bin/env python3
"""
The phone lens (tools/v4_lens.py): the charts and diagrams in the knowledge
base's bands, redrawn with the kit, each with its own phone version: stacked,
at reading size, in place of a 720px drawing scrolled sideways. Every label
and number is the one the drawing it replaces carried (tools/kbfig/*.py).
Where the subject is a quantity the page names (jerk is the rate of change
of G), the phone and the wide drawing show it computed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
from v4_computed import P, rect  # noqa: E402

f = K.f


def wrap(s, n):
    out, line = [], ""
    for wd in s.split():
        if line and len(line) + 1 + len(wd) > n:
            out.append(line)
            line = wd
        else:
            line = (line + " " + wd).strip()
    return out + [line]


def lines(d, x, y, s, n, cls="sub", step=15, anchor="start"):
    for i, ln in enumerate(wrap(s, n)):
        d.text((x, y + step * i), ln, cls, anchor)
    return y + step * len(wrap(s, n))


# ---------------------------------------------------------------- world cups: the weight problem
WEIGHT_DESC = ("The size of the weight problem, by pilot all-up weight from 40 to 125 kg: the band drag noodles address, "
               "100 to 125 kg, about 5% difference in performance, against the gap between an extra small and an extra "
               "large, 65 to 125 kg, about 20%. Bruce Goldsmith's figures; MRT is aimed at the whole range, down to 40 kg "
               "pilots.")


def weight_axis(d, x0, w, y, step):
    X = lambda kg: x0 + (kg - 40) * w / 85
    d.line((X(40), y), (X(125), y), "detail")
    for kg in range(40, 126, step):
        d.line((X(kg), y - 5), (X(kg), y + 5), "hair")
        d.text((X(kg), y + 20), str(kg), "tb", "middle")
    d.text((X(125) + 8, y + 20), "kg", "tb")
    return X


def weight():
    d = K.Drawing(1200, 300, "cp-weight", "Performance gap by pilot weight", WEIGHT_DESC, inline_css=False)
    d.backdrop(glow=(800, 120), glow_r=300, sheet=False)
    X = weight_axis(d, 140, 900, 200, 10)
    rect(d, X(65), 70, X(125) - X(65), 30, "fa", .22)
    d.line((X(65), 70), (X(65), 200), "ghost")
    d.line((X(125), 70), (X(125), 200), "ghost")
    d.text(((X(65) + X(125)) / 2, 90), "about 20%", "val", "middle")
    d.text(((X(65) + X(125)) / 2, 58), "extra small against extra large", "sub", "middle")
    rect(d, X(100), 138, X(125) - X(100), 30, "fh", .3)
    d.text(((X(100) + X(125)) / 2, 158), "about 5%", "lab", "middle")
    d.text((X(100) - 10, 158), "what drag noodles can adjust", "sub", "end")
    d.text((140, 262), "Performance gap by pilot weight", "lab")
    d.text((140, 280), "Bruce Goldsmith's figures; MRT is aimed at the whole range, down to 40 kg pilots", "sub")
    return d


def weight_p():
    d = K.Drawing(360, 330, "cp-weight-p", "Performance gap by pilot weight", WEIGHT_DESC, inline_css=False)
    X = weight_axis(d, 24, 290, 200, 20)
    rect(d, X(65), 70, X(125) - X(65), 30, "fa", .22)
    d.text((X(65), 58), "extra small against extra large", "sub")
    d.text((X(65) + 8, 90), "about 20%", "val")
    rect(d, X(100), 138, X(125) - X(100), 30, "fh", .3)
    d.text((X(100) - 8, 150), "drag noodles", "sub", "end")
    d.text((X(100) - 8, 164), "can adjust", "sub", "end")
    d.text((X(100) + 6, 158), "5%", "lab")
    d.text((16, 258), "Performance gap by pilot weight", "lab")
    lines(d, 16, 278, "Bruce Goldsmith's figures; MRT is aimed at the whole range, down to 40 kg pilots", 46)
    return d


# ---------------------------------------------------------------- sky gods: hours a year
HOURS = [("Honorin Hamard, now", "about 500", [(0, 500, "fa", .9)]),
         ("Maxime Pinot, over 20 years", "250 to 450", [(0, 250, "fa", .9), (250, 450, "fa", .35)]),
         ("Pilots building towards the World Cup", "400 to 500", [(0, 400, "fw", .6), (400, 500, "fw", .25)]),
         ("Pinot in an X-Alps season", "450 flying + 450 on foot", [(0, 450, "fa", .9), (450, 900, "fh", .35)])]
HOURS_DESC = ("Hours in the air a year. Honorin Hamard now flies about 500 hours a year; Maxime Pinot has flown between 250 "
              "and 450 a year for two decades; pilots building towards the World Cup from scratch fly 400 to 500; and in "
              "an X-Alps season Pinot trained about 450 hours in the air and 450 on foot.")


def hours():
    d = K.Drawing(1200, 330, "cp-hours", "Hours in the air a year", HOURS_DESC, inline_css=False)
    d.backdrop(glow=(560, 160), glow_r=300, sheet=False)
    x0, x1 = 380, 1150
    X = lambda h: x0 + h / 1000 * (x1 - x0)
    for h in range(0, 1001, 100):
        d.line((X(h), 30), (X(h), 270), "hair" if h % 500 == 0 else "ghost")
        d.text((X(h), 290), "{:,}".format(h), "tb", "middle")
    d.text((x1, 312), "hours a year", "tb", "end")
    for i, (lab, val, segs) in enumerate(HOURS):
        y = 58 + 60 * i
        d.text((x0 - 16, y), lab, "lab", "end")
        d.text((x0 - 16, y + 16), val, "sub", "end")
        for a, b, c, op in segs:
            rect(d, X(a), y - 10, X(b) - X(a), 16, c, op)
    return d


def hours_p():
    d = K.Drawing(360, 420, "cp-hours-p", "Hours in the air a year", HOURS_DESC, inline_css=False)
    x0, x1 = 16, 330
    X = lambda h: x0 + h / 1000 * (x1 - x0)
    for h in range(0, 1001, 250):
        d.line((X(h), 20), (X(h), 360), "hair" if h % 500 == 0 else "ghost")
        d.text((X(h), 380), "{:,}".format(h), "tb", "middle" if h else "start")
    d.text((x1, 402), "hours a year", "tb", "end")
    for i, (lab, val, segs) in enumerate(HOURS):
        y = 40 + 82 * i
        d.text((x0, y), lab, "lab")
        d.text((x0, y + 16), val, "sub")
        for a, b, c, op in segs:
            rect(d, X(a), y + 28, X(b) - X(a), 14, c, op)
    return d


# ---------------------------------------------------------------- the dark side: a slower top class, full bar
DSS_DESC = ("Why a slower top class still means full bar. Speed ranges from trim to full bar as bars. Before 2011: open-class "
            "wings with a lot of speed that was rarely all used. Today: CCC wings about 20 km/h slower at the top and used "
            "most of the time, while slower wings in the same gaggle sit pinned at their limit. Schematic, no scale.")


def sbar(d, x0, y, length, used, lab, pegged=False, tag_x=None, lab_x=None):
    rect(d, x0, y - 6, length, 12, "fh", .18)
    rect(d, x0, y - 6, used, 12, "fa", .9 if pegged or used >= length - 2 else .55)
    rect(d, x0 + length - 1.5, y - 11, 3, 22, "fw")
    if lab_x is None:
        d.text((x0 - 12, y + 4), lab, "tv", "end")
    else:
        d.text((lab_x, y - 12), lab, "tv")
    if pegged:
        d.text((tag_x if tag_x else x0 + length + 12, y + 4), "pinned at full bar", "val")


def ds_speed():
    d = K.Drawing(1200, 300, "cp-dss", "A slower top class, still at full bar", DSS_DESC, inline_css=False)
    d.backdrop(glow=(860, 120), glow_r=300, sheet=False)
    x0 = 170
    sbar(d, x0, 110, 350, 215, "Open class")
    d.line((x0 + 215, 90), (x0 + 215, 130), "outline")
    d.text((x0 + 215, 78), "what was usually used", "sub", "middle")
    d.text((x0, 200), "Before 2011", "lab")
    d.text((x0, 218), "lots of speed, rarely all of it", "sub")
    x0, pace = 720, 260
    sbar(d, x0, 80, 280, 260, "CCC")
    sbar(d, x0, 116, 235, 235, "EN D", True, x0 + pace + 12)
    sbar(d, x0, 152, 200, 200, "EN C", True, x0 + pace + 12)
    d.line((x0 + pace, 56), (x0 + pace, 170), "accent")
    d.text((x0 + pace, 46), "pace of the lead gaggle", "val", "middle")
    d.text((x0, 200), "Today", "lab")
    d.text((x0, 218), "a slower top class, used most of the time", "sub")
    d.text((1180, 290), "schematic: bar length is speed range from trim to full bar, not to scale", "tb", "end")
    return d


def ds_speed_p():
    d = K.Drawing(360, 440, "cp-dss-p", "A slower top class, still at full bar", DSS_DESC, inline_css=False)
    d.text((16, 24), "Before 2011", "lab")
    d.text((16, 40), "lots of speed, rarely all of it", "sub")
    sbar(d, 16, 96, 300, 184, "Open class", lab_x=16)
    d.line((200, 80), (200, 112), "outline")
    d.text((200, 130), "what was usually used", "sub", "middle")
    d.text((16, 190), "Today", "lab")
    d.text((16, 206), "a slower top class, used most of the time", "sub")
    pace = 220
    for i, (lab, ln, peg) in enumerate((("CCC", 240, False), ("EN D", 202, True), ("EN C", 172, True))):
        sbar(d, 16, 262 + 44 * i, ln, min(ln, pace), lab, lab_x=16)
    d.line((16 + pace, 238), (16 + pace, 360), "accent")
    d.text((16 + pace, 378), "pace of the lead gaggle", "val", "middle")
    d.text((16, 404), "EN D and EN C: pinned at full bar", "sub")
    d.text((16, 432), "schematic, not to scale", "tb")
    return d


# ---------------------------------------------------------------- risk vs reward: ready to step up
STEP_DESC = ("The speed range of a wing as one bar, from minimum sink through trim to full bar. Subir Sidhu's rule: you are "
             "ready to move up when you are comfortable across all of it, not just at trim. 38 to 40 km/h at trim, from "
             "a low B to a CCC; the class shows on the bar.")
SEGS = [(0, .18, "min sink", "stall point behind you"), (.18, .42, "trim", "where everyone is comfortable"),
        (.42, 1.0, "speed bar", "half bar to full bar")]


def stepup_bar(d, x0, x1, y, vertical_labels=False):
    for a, b, lab, sub in SEGS:
        xa, xb = x0 + (x1 - x0) * a, x0 + (x1 - x0) * b
        rect(d, xa, y - 9, xb - xa, 18, "fa" if lab == "speed bar" else "fh", .85 if lab == "speed bar" else (.35 if lab == "trim" else .2))
        d.line((xa, y - 16), (xa, y + 16), "hair")
    d.line((x1, y - 16), (x1, y + 16), "hair")
    rect(d, x0 + (x1 - x0) * .06, y - 34, (x1 - x0) * .5, 6, "fh", .7)
    xs = x0 + (x1 - x0) * .56
    x = xs
    while x + 6 <= x1:                          # the part still missing, hatched
        d.line((x, y - 28), (x + 6, y - 34), "accent")
        x += 9


def stepup():
    d = K.Drawing(1200, 270, "cp-step", "Ready to step up", STEP_DESC, inline_css=False)
    d.backdrop(glow=(820, 120), glow_r=300, sheet=False)
    x0, x1, y = 120, 1080, 120
    stepup_bar(d, x0, x1, y)
    for a, b, lab, sub in SEGS:
        xm = x0 + (x1 - x0) * (a + b) / 2
        d.text((xm, y + 38), lab, "lab", "middle")
        d.text((xm, y + 54), sub, "sub", "middle")
    d.text((x0 + (x1 - x0) * .31, y - 44), "comfortable today", "sub", "middle")
    d.text((x0 + (x1 - x0) * .78, y - 44), "not yet: learn this first", "val", "middle")
    d.poly([(x0, y + 72), (x0, y + 80), (x1, y + 80), (x1, y + 72)], "hair")
    d.text(((x0 + x1) / 2, y + 100), "Ready to step up when all of this is comfortable in the air you fly in", "tv", "middle")
    d.text(((x0 + x1) / 2, 34), "38 to 40 km/h at trim, from a low B to a CCC. The class shows on the bar.", "sub", "middle")
    return d


def stepup_p():
    d = K.Drawing(360, 400, "cp-step-p", "Ready to step up", STEP_DESC, inline_css=False)
    x0, x1, y = 16, 344, 120
    lines(d, 16, 24, "38 to 40 km/h at trim, from a low B to a CCC. The class shows on the bar.", 46)
    d.text((x0 + (x1 - x0) * .06, y - 44), "comfortable today", "sub")
    d.text((x1, y - 44), "not yet", "val", "end")
    stepup_bar(d, x0, x1, y)
    for i, (a, b, lab, sub) in enumerate(SEGS):
        yy = 180 + 44 * i
        rect(d, 16, yy - 10, 10, 10, "fa" if lab == "speed bar" else "fh", .85 if lab == "speed bar" else (.35 if lab == "trim" else .2))
        d.text((34, yy), lab, "lab")
        d.text((34, yy + 16), sub, "sub")
    lines(d, 16, 332, "Ready to step up when all of this is comfortable in the air you fly in.", 44, "tv", 17)
    return d


# ---------------------------------------------------------------- new technologies: harness drag
DRAG = [("chair", "Chair", "about 23 N", 23), ("pod", "Pod with a fairing", "about 12 N", 12), ("sub", "Submarine", "about 8 N", 8)]
DRAG_DESC = ("Harness drag measured by Supair, three pilots side-on with a bar each: chair about 23 N, foil-faired pod "
             "about 12 N, submarine about 8 N. The drawings of the pilots are schematic.")
BODIES = {"chair": [(-95, -30), (-40, -38), (10, 0), (70, 10), (80, 60), (40, 70), (-10, 40), (-80, 30)],
          "pod": [(-100, -30), (-30, -40), (80, -18), (230, 5), (250, 22), (220, 40), (60, 50), (-60, 40), (-100, 20)],
          "sub": [(-110, -44), (-20, -58), (120, -30), (270, 0), (300, 20), (270, 34), (100, 44), (-60, 38), (-112, 10)]}


def pilot(d, cx, cy, kind, s):
    d.circle((cx - 70 * s, cy - 52 * s), 20 * s, "outline", fill="card")
    if kind == "chair":
        d.poly([(cx + x * s, cy + y * s) for x, y in [(40, 10), (100, 30), (106, 88), (90, 90), (80, 46)]], "detail", True, "card")
    d.spline([(cx + x * s, cy + y * s) for x, y in BODIES[kind]], "outline", True, "card", .35)
    d.line((cx - 60 * s, cy - 40 * s), (cx - 40 * s, cy - 150 * s), "ghost")


def drag():
    d = K.Drawing(1200, 320, "cp-drag", "Harness drag, measured", DRAG_DESC, inline_css=False)
    d.backdrop(glow=(1000, 140), glow_r=260, sheet=False)
    for i, (k, lab, val, n) in enumerate(DRAG):
        cx = 170 + i * 400
        pilot(d, cx, 140, k, .5)
        rect(d, cx - 80, 206, 23 * 11, 8, "fh", .2)
        rect(d, cx - 80, 206, n * 11, 8, "fa", .9)
        d.text((cx - 80, 244), lab, "lab")
        d.text((cx - 80, 262), val + " of drag", "val")
    d.text((1180, 310), "Supair's drag figures for pilot and harness · drawings schematic", "tb", "end")
    return d


def drag_p():
    d = K.Drawing(360, 480, "cp-drag-p", "Harness drag, measured", DRAG_DESC, inline_css=False)
    for i, (k, lab, val, n) in enumerate(DRAG):
        y = 70 + 140 * i
        pilot(d, 80, y, k, .42)
        d.text((200, y - 20), lab, "lab")
        d.text((200, y - 2), val, "val")
        rect(d, 16, y + 42, 23 * 12, 8, "fh", .2)
        rect(d, 16, y + 42, n * 12, 8, "fa", .9)
    d.text((16, 470), "Supair's figures · drawings schematic", "tb")
    return d


# ---------------------------------------------------------------- know your equipment: jerk
JERK_DESC = ("Two impact curves from a harness drop test. Left: foam or airbag, a smooth rise to the peak. Right: a crumple "
             "protector, flat until it yields, then a step. Same peak G; very different jerk. Under each, its jerk: the "
             "rate at which G changes, worked out from the curve above it.")


def g_curve(kind, n=240):
    ts = [i / (n - 1) for i in range(n)]
    if kind == "foam":
        g = [math.exp(-((t - .5) / .17) ** 2) for t in ts]
    else:
        g = []
        for t in ts:
            if t < .36:
                g.append(.02 + .06 * t)
            elif t < .4:
                g.append(.05 + (1 - .05) * (t - .36) / .04)
            else:
                g.append(math.exp(-((t - .52) / .16) ** 2) if t > .52 else 1.0)
    jerk = [0] + [(g[i + 1] - g[i - 1]) / 2 for i in range(1, n - 1)] + [0]
    return ts, g, jerk


def jerk_panel(d, x0, y0, w, kind, title, sub):
    ts, g, j = g_curve(kind)
    h, hj = 120, 50
    d.text((x0, y0), title, "lab")
    d.text((x0, y0 + 18), sub, "sub")
    gy = y0 + 40 + h
    d.line((x0, gy), (x0 + w, gy), "hair")
    d.line((x0, gy), (x0, gy - h), "hair")
    d.text((x0 - 6, gy - h + 4), "G", "tb", "end")
    pts = [(x0 + t * w, gy - v * (h - 10)) for t, v in zip(ts, g)]
    d.poly(pts, "accent" if kind == "foam" else "outline")
    d.line((x0, gy - (h - 10)), (x0 + w, gy - (h - 10)), "ghost")
    d.text((x0 + w, gy - h + 4), "same peak", "tb", "end")
    jy = gy + 30 + hj
    d.line((x0, jy), (x0 + w, jy), "hair")
    d.text((x0 - 6, jy - hj + 10), "jerk", "tb", "end")
    jm = max(max(abs(v) for v in j) for j in (g_curve("foam")[2], g_curve("crumple")[2]))
    jp = [(x0 + t * w, jy - max(v, 0) / jm * hj) for t, v in zip(ts, j)]
    d.poly(jp, "accent" if kind == "crumple" else "detail")
    d.text((x0 + w, jy + 16), "time", "tb", "end")
    return jp


def jerk():
    d = K.Drawing(1200, 360, "cp-jerk", "Same peak G, very different jerk", JERK_DESC, inline_css=False)
    d.backdrop(glow=(880, 220), glow_r=260, sheet=False)
    jerk_panel(d, 110, 40, 420, "foam", "Foam or airbag", "the rise is gradual: low jerk")
    jp = jerk_panel(d, 680, 40, 420, "crumple", "Crumple honeycomb", "nothing, then a step: high jerk")
    top = min(jp, key=lambda p: p[1])
    d.poly([(top[0] + 6, top[1]), (top[0] + 60, top[1] - 8), (top[0] + 70, top[1] - 8)], "hair")
    d.text((top[0] + 76, top[1] - 4), "the corner that breaks vertebrae", "val")
    d.text((1180, 350), "schematic curves · jerk worked out from each G curve", "tb", "end")
    return d


def jerk_p():
    d = K.Drawing(360, 620, "cp-jerk-p", "Same peak G, very different jerk", JERK_DESC, inline_css=False)
    jerk_panel(d, 44, 24, 290, "foam", "Foam or airbag", "the rise is gradual: low jerk")
    jp = jerk_panel(d, 44, 314, 290, "crumple", "Crumple honeycomb", "nothing, then a step: high jerk")
    top = min(jp, key=lambda p: p[1])
    d.text((top[0] + 10, top[1] + 4), "the corner that", "val")
    d.text((top[0] + 10, top[1] + 20), "breaks vertebrae", "val")
    d.text((344, 612), "schematic · jerk worked out from G", "tb", "end")
    return d


# ---------------------------------------------------------------- know your equipment: what EN 966 tests
HELMET_DESC = ("What EN 966 tests, in three panels: the 1.5 m drop, where the head form must see under 250 G (a good new "
               "helmet: 170 to 180 G); the penetration test, where a falling point must stop 5 mm short of the head; and "
               "the 5 mm rule for anything on the shell.")
HELMET = [("Drop test", "head form must see under 250 G", "a good new helmet: 170 to 180 G"),
          ("Penetration", "a falling point must stop 5 mm short of the head", "vented bike and climbing shells fail here"),
          ("Nothing to snag", "shell parts, mounts and cameras: 5 mm or less", "a line round a camera is the failure mode")]


def helmet(d, cx, cy, r):
    shell = [(cx + r * math.cos(t), cy + r * .92 * math.sin(t)) for t in [math.pi * (1.02 + 1.03 * k / 40) for k in range(41)]]
    d.poly(shell, "outline", True, "card")
    liner = [(cx + (r - r * .2) * math.cos(t), cy + (r - r * .2) * .92 * math.sin(t)) for t in [math.pi * (1.06 + .94 * k / 30) for k in range(31)]]
    d.poly(liner, "ghost")
    d.circle((cx, cy + r * .07), r * .6, "hair")


def helmet_panel(d, k, cx, cy, r):
    helmet(d, cx, cy, r)
    if k == 0:
        d.arrow((cx - r * 1.7, cy - r * 2.1), (cx - r * 1.7, cy - r * 1.0), "accent", 9)
        d.line((cx - r * 1.95, cy - r * 2.1), (cx - r * 1.45, cy - r * 2.1), "hair")
        d.line((cx - r * 1.95, cy - r * .8), (cx - r * 1.45, cy - r * .8), "hair")
        d.text((cx - r * 2.0, cy - r * 1.45), "1.5 m", "val", "end")
    elif k == 1:
        tip = cy - r * .95
        d.poly([(cx, tip), (cx - r * .14, tip - r * .6), (cx + r * .14, tip - r * .6)], "accent", True)
        d.arrow((cx, tip - r * 1.3), (cx, tip - r * .75), "accent", 8)
        d.line((cx + r * 1.15, cy - r * .9), (cx + r * 1.15, cy - r * .78), "accent")
        d.text((cx + r * 1.25, cy - r * .8), "5 mm gap", "val")
    else:
        d.path("M%s,%s h%s v%s h-%s Z" % (f(cx - r * .13), f(cy - r * 1.06), f(r * .26), f(r * .22), f(r * .26)), "accent", fill="card")
        d.text((cx + r * .4, cy - r * .92), "5 mm max", "val")
        d.line((cx - r * 2.4, cy - r * 1.8), (cx - r * .2, cy - r * 1.02), "ghost")


def helmet_fig():
    d = K.Drawing(1200, 300, "cp-helmet", "What EN 966 tests", HELMET_DESC, inline_css=False)
    d.backdrop(glow=(600, 150), glow_r=300, sheet=False)
    for k, (a, b, c) in enumerate(HELMET):
        cx = 220 + 390 * k
        helmet_panel(d, k, cx, 170, 55)
        d.text((cx, 226), a, "lab", "middle")
        d.text((cx, 244), b, "tv", "middle")
        d.text((cx, 260), c, "sub", "middle")
    return d


def helmet_p():
    d = K.Drawing(360, 620, "cp-helmet-p", "What EN 966 tests", HELMET_DESC, inline_css=False)
    for k, (a, b, c) in enumerate(HELMET):
        y = 20 + 200 * k
        helmet_panel(d, k, 236, y + 110, 38)
        d.text((16, y + 18), a, "lab")
        yy = lines(d, 16, y + 38, b, 22, "tv", 15)
        lines(d, 16, yy + 4, c, 22, "sub", 14)
    return d


# ---------------------------------------------------------------- flight mechanics: reading a thermal
THERMAL_DESC = ("Reading a thermal, after Brett Janaway. Left, from above: the core sits upwind; turning into wind finds it, "
                "turning downwind falls out of the back. Right, from the side: the column leans downwind, the strongest air "
                "at the upwind front.")


def glider(d, p, ang, accent, s=8):
    t = math.radians(ang)
    dx, dy = math.cos(t), math.sin(t)
    nx, ny = -dy, dx
    tri = [(p[0] + dx * s, p[1] + dy * s), (p[0] - dx * s * .6 + nx * s * .75, p[1] - dy * s * .6 + ny * s * .75),
           (p[0] - dx * s * .3, p[1] - dy * s * .3), (p[0] - dx * s * .6 - nx * s * .75, p[1] - dy * s * .6 - ny * s * .75)]
    d.raw('<path class="%s" d="M%s Z"/>' % ("fa" if accent else "fh", " L".join("%s,%s" % (f(a), f(b)) for a, b in tri)))


def top_view(d, C, s):
    """The thermal from above, wind left to right; s scales the 2400-wide original's geometry to this drawing."""
    cx, cy = C
    core = (cx - 120 * s, cy)
    for r, op in ((1.0, .18), (.78, .22), (.56, .28)):
        d.raw('<ellipse class="g" cx="%s" cy="%s" rx="%s" ry="%s" style="stroke-opacity:%s"/>' % (
            f(cx - 120 * s * (1 - r)), f(cy), f(300 * r * s), f(250 * r * s), op + .2))
    E = (cx + 30 * s, cy + 120 * s)
    d.path("M%s,%s L%s,%s" % (f(E[0] + 10 * s), f(E[1] + 230 * s), f(E[0]), f(E[1])), "ghost")
    glider(d, (E[0] + 4 * s, E[1] + 140 * s), -90, False)
    n, r0 = 300, 95 * s
    into = []
    for i in range(n):
        t = i / (n - 1)
        th, b = t * 2 * math.pi * 2.3, min(1, t * 2.2) ** .8
        c = ((E[0] - r0) * (1 - b) + core[0] * b, E[1] * (1 - b) + core[1] * b)
        rad = r0 * (1 - b) + 62 * s * b
        into.append((c[0] + rad * math.cos(th), c[1] - rad * math.sin(th)))
    d.poly(into, "accent")
    d.head(into[-1], (into[-1][0] - into[-4][0], into[-1][1] - into[-4][1]), 9, True)
    out, r2 = [], 70 * s
    for i in range(n):
        t = i / (n - 1)
        th = t * 2 * math.pi * 1.7
        c = (E[0] + r2 + t * 420 * s, E[1] - t * 10 * s)
        out.append((c[0] - r2 * math.cos(th), c[1] - r2 * math.sin(th)))
    d.poly(out, "ghost")
    d.head(out[-1], (out[-1][0] - out[-4][0], out[-1][1] - out[-4][1]), 8)
    d.dot(core, 5, True)
    return core


def side_view(d, S, s, G):
    x0 = S[0]
    d.line((x0 - 300 * s, G), (x0 + 770 * s, G), "hair")
    hs = [i / 40 for i in range(41)]
    lean = [330 * s * h ** 1.1 for h in hs]
    front = [(x0 - 60 * s - 40 * s * h + l, G - 560 * s * h) for h, l in zip(hs, lean)]
    back = [(x0 + 60 * s + 170 * s * h + l, G - 560 * s * h * .92) for h, l in zip(hs, lean)]
    d.raw('<path class="fa" style="fill-opacity:.08" d="M%s Z"/>' % " L".join("%s,%s" % (f(a), f(b)) for a, b in front + back[::-1]))
    d.poly(front, "detail")
    d.poly(back, "ghost")
    core = [(x0 - 20 * s + l - 10 * s * h, G - 560 * s * h) for h, l in zip(hs, lean)]
    d.poly(core, "accent")
    for fr in (.2, .45, .85):
        j = int(fr * 40)
        d.arrow((core[j][0], core[j][1] + 20 * s), (core[j][0] + 10 * s, core[j][1] - 40 * s), "accent", 8)
    cb = (core[-1][0] + 60 * s, core[-1][1] - 30 * s)
    for dx, dy, w, hh in ((-80, 10, 220, 90), (40, -10, 260, 120), (160, 12, 200, 90)):
        d.raw('<ellipse class="f" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (f(cb[0] + dx * s), f(cb[1] + dy * s), f(w * s / 2), f(hh * s / 2)))
    for dx, dy, w, hh in ((-80, 10, 220, 90), (40, -10, 260, 120), (160, 12, 200, 90)):
        d.raw('<ellipse class="d" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (f(cb[0] + dx * s), f(cb[1] + dy * s), f(w * s / 2), f(hh * s / 2)))
    glider(d, (core[27][0] + 26 * s, core[27][1] + 4 * s), -30, True, 9)
    b = back[15]
    glider(d, (b[0] + 60 * s, b[1] + 70 * s), 20, False)


def wind(d, x, y, s):
    for dy in (0, 45 * s):
        d.arrow((x, y + dy), (x + 130 * s, y + dy), "detail", 9)


def thermal():
    s = .5
    d = K.Drawing(1200, 380, "cp-thermal", "Reading a thermal", THERMAL_DESC, inline_css=False)
    d.backdrop(glow=(260, 195), glow_r=220, sheet=False)
    top_view(d, (290, 195), s)
    wind(d, 100, 48, s)
    side_view(d, (780, 345), s, 345)
    wind(d, 650, 55, s)
    d.line((600, 30), (600, 350), "ghost")
    d.text((40, 372), "from above", "tb")
    d.text((640, 372), "from the side", "tb")
    return d


def thermal_p():
    s = .34
    d = K.Drawing(360, 600, "cp-thermal-p", "Reading a thermal", THERMAL_DESC, inline_css=False)
    d.text((16, 22), "From above", "lab")
    wind(d, 16, 44, s)
    top_view(d, (150, 160), s)
    d.line((16, 290), (344, 290), "ghost")
    d.text((16, 318), "From the side", "lab")
    wind(d, 16, 340, s)
    side_view(d, (110, 580), s, 580)
    return d


def registry():
    return {
        "kb-world-cups-weight": (weight, weight_p),
        "kb-sky-gods-hours": (hours, hours_p),
        "kb-the-dark-side-speed": (ds_speed, ds_speed_p),
        "kb-risk-vs-reward-stepup": (stepup, stepup_p),
        "kb-new-technologies-drag": (drag, drag_p),
        "kb-know-your-equipment-jerk": (jerk, jerk_p),
        "kb-know-your-equipment-helmet": (helmet_fig, helmet_p),
        "kb-flight-mechanics-thermal": (thermal, thermal_p),
    }
