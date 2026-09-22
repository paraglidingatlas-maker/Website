"""Figure: then and now, as Eddie Colfox tells it. Cross-country, hours and
competition wings in the early 1990s against today. 2400x620."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 620; fig, ax = canvas(W, H)
XL, XT, XN = 560, 640, 1480
T(ax, XT, 70, "EARLY 1990s", GR, 14, "left", fw="bold")
T(ax, XN, 70, "NOW", OR, 14, "left", fw="bold")
rows = [("Cross-country", ["a handful in the club;", "20 to 50 km flights in the UK"], ["at least half of UK club pilots expect to;", "keen pilots fly 100 km in their first couple of years"]),
        ("Hours", ["over 100 hours made you a rock star;", "a first logbook full of one-minute flights"], ["150 hours in your first year,", "if you live in the right country"]),
        ("Competition wings", ["expect massive collapses", "on every good day"], ["vastly improved,", "and safer"])]
for i, (lab, a, b) in enumerate(rows):
    y = 170 + i * 150
    L(ax, [(XT - 30, y - 55), (2280, y - 55)], GR, .6, .15)
    T(ax, XL, y, lab, WH, 17, "right", fw="bold")
    for j, s in enumerate(a): T(ax, XT, y - 14 + j * 30, s, GR, 15, "left")
    AR(ax, (XN - 150, y), (XN - 50, y), OR, 1.8, a=.8)
    for j, s in enumerate(b): T(ax, XN, y - 14 + j * 30, s, WH, 15, "left")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "then.jpg", bloom=.2)
print("ok")
