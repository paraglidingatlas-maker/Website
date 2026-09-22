"""Quote-band image: fighting a thought against letting it be there. Two
curves of how loud an unhelpful thought gets over time: one pushed against,
which grows, and one acknowledged, which rises and fades. 2400x1000, subject
on the right."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from common import *
W, H = 2400, 1000; fig, ax = canvas(W, H)
x0, x1, yb = 1100, 2280, 780
L(ax, [[x0, yb], [x1, yb]], GR, 1.1, .6); L(ax, [[x0, yb], [x0, 260]], GR, 1.1, .6)
T(ax, x1, yb+34, "time in the air", GR, 13, "right"); T(ax, x0-16, 270, "how loud the thought is", GR, 13, "right")
t = np.linspace(0, 1, 300)
fight = yb - (120 + 380*t**1.3 + 18*np.sin(t*40))
allow = yb - (120 + 260*np.exp(-((t-.18)/.2)**2)*(t < .18) + 260*np.exp(-((t-.18)/.28)**2)*(t >= .18))
X = x0 + t*(x1-x0)
L(ax, np.c_[X, fight], WH, 1.8, .8, z=4); L(ax, np.c_[X, allow], OR, 2.2, .95, z=5)
T(ax, X[-1]-10, fight[-1]-28, "pushed against: it grows", WH, 15, "right", fw="bold")
T(ax, X[-1]-10, allow[-1]-26, "noticed and let be: it passes", OR, 15, "right", fw="bold")
finish(fig, W, H, sys.argv[1] if len(sys.argv) > 1 else "section.jpg", bloom=.3, glow=(.62, .6, .32))
print("ok")
