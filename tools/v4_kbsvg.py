#!/usr/bin/env python3
"""
The knowledge base figures, redrawn with the kit (docs/v4-plan.md step 7).

The figures were drawn by tools/kbfig/*.py (and tools/make_kb_*.py) with
matplotlib and saved as pictures. Their geometry, labels and numbers were
checked against each page's own text when they were made; this keeps all of
that and changes the drawing: each script runs unchanged, but its drawing
calls (canvas, L, AR, T, finish and the patches from common.py) write kit
SVG instead of pixels. Vector, sharp at any size, the site's type (the
drawings sit inline in the page), the kit's line weights (strokes that keep
their width at any size), the site's colours, a soft light where the old
figure had its glow. The raster originals stay in the repo for v2 and for
each page's og:image (parity).

    python3 tools/v4_kbsvg.py                 # every figure -> prototypes/v4/img/kb/*.svg
    python3 tools/v4_kbsvg.py nav_thirds      # one
"""
import html
import importlib.util
import math
import os
import re
import sys
import types

import numpy as np
from matplotlib.path import Path as _MPath      # the real one, for geometry questions (contains_points)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KBFIG = os.path.join(ROOT, "tools", "kbfig")
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "kb")

BG = "#141519"; OR = "#ff7517"; ORL = "#ff9a52"; GR = "#b4b4b4"; DIM = "#737373"; WH = "#e9e7e7"; FILL = "#24252c"
COLOR = {OR: "var(--orange,#ff7517)", ORL: "var(--orange-lite,#ff8a3d)", GR: "#b4b4b4", DIM: "#8a8a8a",
         WH: "var(--white,#f6f4f4)", FILL: "#202127", BG: "#141519", "none": "none", "white": "var(--white,#f6f4f4)"}
PT = 1.39                          # a matplotlib point on the 100 dpi canvas
LIFT = {"default": 1.2}             # small type is lifted for the page (large type stays as drawn); per figure below
LIFT["kb-risk-vs-reward-altitude"] = 1.0   # its type fills fixed boxes


def col(c):
    if c is None:
        return None
    if isinstance(c, (tuple, list, np.ndarray)):
        r, g, b = [int(round(float(v) * 255)) for v in list(c)[:3]]
        return "#%02x%02x%02x" % (r, g, b)
    c = str(c)
    return COLOR.get(c.lower() if c.startswith("#") else c, COLOR.get(c, c))


def f(v):
    s = ("%.1f" % float(v)).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def dash(ls, lw):
    if ls in (None, "-", "solid"):
        return ""
    if ls in ("--", "dashed"):          # matplotlib's patterns, in points times the line width
        pat = (3.7, 1.6)
    elif ls in (":", "dotted"):
        pat = (1, 1.65)
    elif ls in ("-.", "dashdot"):
        pat = (6.4, 1.6, 1, 1.6)
    elif isinstance(ls, tuple) and len(ls) == 2:
        pat = ls[1]
    else:
        return ""
    k = PT * max(float(lw or 1), 1)
    return ' stroke-dasharray="%s"' % " ".join(f(x * k) for x in pat)


def width(lw):
    lw = 1.0 if lw is None else float(lw)
    return max(.6, min(2.2, lw * .85))


class Fig:
    def __init__(self, W, H, bg):
        self.W, self.H, self.bg = W, H, bg
        self.els = []          # (z, n, svg)
        self.n = 0

    def add(self, z, svg):
        self.n += 1
        self.els.append((z if z is not None else 1, self.n, svg))


def style(fc=None, ec=None, lw=None, alpha=None, ls=None, fill=True):
    a = 1 if alpha is None else float(alpha)
    s = ""
    fcol = col(fc) if fill else "none"
    s += ' fill="%s"' % (fcol if fcol not in (None,) else "none")
    if fcol not in (None, "none") and a < 1:
        s += ' fill-opacity="%s"' % f(a)
    e = col(ec)
    if e and e != "none" and lw is not None and float(lw) >= 5:     # a bar drawn as a thick line: it scales with the drawing
        s += ' stroke="%s" stroke-width="%s"' % (e, f(float(lw) * PT))
        if a < 1:
            s += ' stroke-opacity="%s"' % f(a)
    elif e and e != "none":
        s += ' stroke="%s" stroke-width="%s" vector-effect="non-scaling-stroke" stroke-linejoin="round"' % (e, f(width(lw)))
        if a < 1:
            s += ' stroke-opacity="%s"' % f(a)
        s += dash(ls, lw)
    return s


def simplify(P, tol=.6):
    """Ramer-Douglas-Peucker: drop points within tol canvas px of the line (a 2400 px canvas; invisible)."""
    P = np.asarray(P, float)
    if len(P) < 5:
        return P
    keep = np.zeros(len(P), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(P) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        d = P[b] - P[a]
        n = math.hypot(*d)
        seg = P[a + 1:b] - P[a]
        dist = np.abs(seg[:, 0] * d[1] - seg[:, 1] * d[0]) / n if n else np.hypot(seg[:, 0], seg[:, 1])
        i = int(np.argmax(dist))
        if dist[i] > tol:
            keep[a + 1 + i] = True
            stack += [(a, a + 1 + i), (a + 1 + i, b)]
    return P[keep]


def pts(P):
    return " ".join("%s,%s" % (f(x), f(y)) for x, y in simplify(P))


# ------------------------------------------------------------------ patches
class Patch:
    def __init__(self, **kw):
        self.kw = kw
        c = kw.get("color")
        self.fc = kw.get("fc", kw.get("facecolor", c if c is not None else FILL))
        self.ec = kw.get("ec", kw.get("edgecolor", c if c is not None else "none"))
        self.lw = kw.get("lw", kw.get("linewidth", 1))
        self.alpha = kw.get("alpha")
        self.ls = kw.get("ls", kw.get("linestyle"))
        self.z = kw.get("zorder", 1)
        if kw.get("fill") is False:
            self.fc = "none"

    def st(self):
        return style(self.fc, self.ec, self.lw, self.alpha, self.ls)


class Circle(Patch):
    def __init__(self, xy, radius=5, **kw):
        super().__init__(**kw)
        self.xy, self.r = xy, radius

    def svg(self):
        return '<circle cx="%s" cy="%s" r="%s"%s/>' % (f(self.xy[0]), f(self.xy[1]), f(self.r), self.st())


class Ellipse(Patch):
    def __init__(self, xy, width, height, angle=0, **kw):
        super().__init__(**kw)
        self.xy, self.w, self.h, self.a = xy, width, height, angle

    def svg(self):
        tr = ' transform="rotate(%s %s %s)"' % (f(self.a), f(self.xy[0]), f(self.xy[1])) if self.a else ""
        return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s"%s%s/>' % (f(self.xy[0]), f(self.xy[1]), f(self.w / 2), f(self.h / 2), tr, self.st())


class Polygon(Patch):
    def __init__(self, xy, closed=True, **kw):
        super().__init__(**kw)
        self.P, self.closed = np.asarray(xy, float), closed

    def svg(self):
        tag = "polygon" if self.closed else "polyline"
        st = self.st() if self.closed else style("none", self.ec, self.lw, self.alpha, self.ls)
        return '<%s points="%s"%s/>' % (tag, pts(self.P), st)


class Rectangle(Patch):
    def __init__(self, xy, width, height, angle=0, **kw):
        super().__init__(**kw)
        self.xy, self.w, self.h, self.a = xy, width, height, angle

    def svg(self):
        x, y, w, h = self.xy[0], self.xy[1], self.w, self.h
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        tr = ' transform="rotate(%s %s %s)"' % (f(self.a), f(self.xy[0]), f(self.xy[1])) if self.a else ""
        return '<rect x="%s" y="%s" width="%s" height="%s"%s%s/>' % (f(x), f(y), f(w), f(h), tr, self.st())


class FancyBboxPatch(Rectangle):
    def __init__(self, xy, width, height, boxstyle=None, **kw):
        super().__init__(xy, width, height, **kw)
        m = re.search(r"pad=([\d.]+)", str(boxstyle or ""))
        self.pad = float(m.group(1)) if m else 0
        m = re.search(r"rounding_size=([\d.]+)", str(boxstyle or ""))
        self.rx = float(m.group(1)) if m else (4 if "round" in str(boxstyle or "") else 0)

    def svg(self):
        p = self.pad
        return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s"%s/>' % (
            f(self.xy[0] - p), f(self.xy[1] - p), f(self.w + 2 * p), f(self.h + 2 * p), f(self.rx), self.st())


class Arc(Patch):
    def __init__(self, xy, width, height, angle=0, theta1=0, theta2=360, **kw):
        kw.setdefault("fc", "none")
        if "color" in kw and "ec" not in kw:
            kw["ec"] = kw["color"]
        super().__init__(**kw)
        self.fc = "none"
        self.xy, self.w, self.h, self.a, self.t1, self.t2 = xy, width, height, angle, theta1, theta2

    def svg(self):
        P = []
        n = max(8, int(abs(self.t2 - self.t1) / 3))
        for i in range(n + 1):
            t = math.radians(self.t1 + (self.t2 - self.t1) * i / n)
            x, y = self.w / 2 * math.cos(t), self.h / 2 * math.sin(t)
            r = math.radians(self.a)
            P.append((self.xy[0] + x * math.cos(r) - y * math.sin(r), self.xy[1] + x * math.sin(r) + y * math.cos(r)))
        return '<polyline points="%s"%s/>' % (pts(P), style("none", self.ec, self.lw, self.alpha, self.ls))


class FancyArrowPatch(Patch):
    def __init__(self, posA=None, posB=None, arrowstyle="-|>", mutation_scale=1, **kw):
        c = kw.get("color", GR)
        kw.setdefault("ec", c)
        super().__init__(**kw)
        self.A, self.B, self.style_ = posA, posB, str(arrowstyle)
        m = re.search(r"head_length=([\d.]+)", self.style_)
        self.hl = float(m.group(1)) if m else 10
        m = re.search(r"head_width=([\d.]+)", self.style_)
        self.hw = float(m.group(1)) if m else 4
        self.c = c

    def svg(self):
        return arrow_svg(self.A, self.B, self.c, self.lw, self.alpha, self.hl, self.hw, "<|-" in self.style_ or "<->" in self.style_)


def arrow_svg(p, q, c, lw, a, hl=12, hw=5, both=False):
    p, q = np.asarray(p, float), np.asarray(q, float)
    v = q - p
    L = float(np.hypot(*v)) or 1
    u = v / L
    n = np.array([-u[1], u[0]])
    hl = max(hl * 1.39, 16)              # matplotlib's head sizes are in points
    hw = max(hw * 1.39, 6.5)
    head = lambda tip, d: pts([tip, tip - d * hl + n * hw, tip - d * hl - n * hw])
    a_ = 1 if a is None else a
    body_a = p + (u * hl * .6 if both else 0)
    body_b = q - u * hl * .6
    s = '<line x1="%s" y1="%s" x2="%s" y2="%s"%s/>' % (f(body_a[0]), f(body_a[1]), f(body_b[0]), f(body_b[1]),
                                                         style("none", c, lw, a_))
    s += '<polygon points="%s" fill="%s"%s/>' % (head(q, u), col(c), ' fill-opacity="%s"' % f(a_) if a_ < 1 else "")
    if both:
        s += '<polygon points="%s" fill="%s"/>' % (head(p, -u), col(c))
    return s


class Path:        # matplotlib.path.Path, as the scripts use it (vertices and codes)
    MOVETO, LINETO, CURVE3, CURVE4, CLOSEPOLY = 1, 2, 3, 4, 79

    def __init__(self, vertices, codes=None, closed=False):
        self.vertices, self.codes = np.asarray(vertices, float), codes

    def contains_points(self, P):         # geometry only: the real matplotlib answers it
        return _MPath(self.vertices, self.codes).contains_points(P)


class PathPatch(Patch):
    def __init__(self, path, **kw):
        super().__init__(**kw)
        self.path = path

    def svg(self):
        V, C = self.path.vertices, self.path.codes
        d, i = "", 0
        while i < len(V):
            c = C[i] if C is not None else (1 if i == 0 else 2)
            if c == 1:
                d += "M%s %s" % (f(V[i][0]), f(V[i][1])); i += 1
            elif c == 2:
                d += "L%s %s" % (f(V[i][0]), f(V[i][1])); i += 1
            elif c == 3:
                d += "Q%s %s %s %s" % (f(V[i][0]), f(V[i][1]), f(V[i + 1][0]), f(V[i + 1][1])); i += 2
            elif c == 4:
                d += "C%s %s %s %s %s %s" % tuple(f(x) for x in (V[i][0], V[i][1], V[i + 1][0], V[i + 1][1], V[i + 2][0], V[i + 2][1])); i += 3
            else:
                d += "Z"; i += 1
        return '<path d="%s"%s/>' % (d, self.st())


# ------------------------------------------------------------------ the axes
class Ax:
    def __init__(self, fig):
        self.fig = fig

    def add_patch(self, p):
        self.fig.add(getattr(p, "z", 1), p.svg())
        return p

    def plot(self, x, y=None, color=GR, lw=1, alpha=None, ls=None, zorder=2, linestyle=None, linewidth=None, c=None, **kw):
        if y is None:
            P = np.asarray(x, float)
        else:
            P = np.c_[np.asarray(x, float), np.asarray(y, float)]
        color = c or color
        lw = linewidth or lw
        self.fig.add(zorder, '<polyline points="%s"%s stroke-linecap="round"/>' % (pts(P), style("none", color, lw, alpha, ls or linestyle)))

    def text(self, x, y, s, color=GR, fontsize=14, ha="left", va="center", fontweight="normal", alpha=None, zorder=7, **kw):
        T(self, x, y, s, color, fontsize, ha, va, fontweight, .9 if alpha is None else alpha, zorder,
          rotation=kw.get("rotation", 0), ha_=kw.get("horizontalalignment"), va_=kw.get("verticalalignment"))

    def scatter(self, x, y, s=20, c=GR, color=None, alpha=None, zorder=5, **kw):
        c = color or c
        r = math.sqrt(float(np.max(s) if np.ndim(s) else s)) / 2 * 1.4
        for xx, yy in zip(np.atleast_1d(x), np.atleast_1d(y)):
            self.fig.add(zorder, '<circle cx="%s" cy="%s" r="%s" fill="%s"%s/>' % (f(xx), f(yy), f(r), col(c), ' fill-opacity="%s"' % f(alpha) if alpha is not None and alpha < 1 else ""))

    def fill_between(self, x, y1, y2=0, color=GR, alpha=None, zorder=1, fc=None, ec="none", lw=0, **kw):
        x = np.asarray(x, float)
        y1 = np.broadcast_to(np.asarray(y1, float), x.shape)
        y2 = np.broadcast_to(np.asarray(y2, float), x.shape)
        P = list(zip(x, y1)) + list(zip(x[::-1], y2[::-1]))
        self.fig.add(zorder, '<polygon points="%s"%s/>' % (pts(P), style(fc or color, ec, lw, alpha)))

    def contour(self, X, Y, Z, levels=10, colors=GR, linewidths=1, alpha=None, zorder=1, linestyles=None, **kw):
        import contourpy
        gen = contourpy.contour_generator(np.asarray(X, float), np.asarray(Y, float), np.asarray(Z, float))
        lv = levels if np.ndim(levels) else np.linspace(np.nanmin(Z), np.nanmax(Z), int(levels) + 2)[1:-1]
        cols = colors if isinstance(colors, (list, tuple)) and not isinstance(colors, str) and len(colors) == len(lv) else [colors] * len(lv)
        lws = linewidths if np.ndim(linewidths) else [linewidths] * len(lv)
        for i, L_ in enumerate(lv):
            for line in gen.lines(L_):
                if len(line) > 1:
                    self.fig.add(zorder, '<polyline points="%s"%s/>' % (pts(line), style("none", cols[i], lws[i], alpha)))

    def axis(self, *a, **k):
        pass

    def set_xlim(self, *a, **k):
        pass

    def set_ylim(self, *a, **k):
        pass


# ------------------------------------------------------------------ common.py's API
def canvas(W, H, bg=BG):
    fig = Fig(W, H, bg)
    return fig, Ax(fig)


def L(ax, P, c=GR, lw=1, a=.8, ls="-", z=2):
    P = np.asarray(P, float)
    ax.fig.add(z, '<polyline points="%s"%s stroke-linecap="round"/>' % (pts(P), style("none", c, lw, a, ls)))


def AR(ax, p, q, c, lw=1.6, hl=12, hw=5, a=1, z=6):
    ax.fig.add(z, arrow_svg(p, q, c, lw, a, hl, hw))


def T(ax, x, y, s, c=GR, fs=14, ha="left", va="center", fw="normal", a=.9, z=7, rotation=0, ha_=None, va_=None):
    ha, va = ha_ or ha, va_ or va
    anchor = {"left": "start", "center": "middle", "right": "end"}.get(ha, "start")
    base = {"center": "central", "top": "hanging", "bottom": "text-after-edge", "baseline": "alphabetic",
            "center_baseline": "central"}.get(va, "central")
    k = LIFT.get(CURRENT[0], LIFT["default"])
    size = fs * PT * (k if fs <= 16 else max(1.0, k - (k - 1) * (fs - 16) / 10))
    bold = str(fw) in ("bold", "semibold", "heavy", "600", "700")
    fam = "var(--font-display,'Poppins',sans-serif)" if (bold and fs >= 17) else "var(--font-body,'DM Sans',sans-serif)"
    rot = ' transform="rotate(%s %s %s)"' % (f(-rotation), f(x), f(y)) if rotation else ""
    lines = str(s).split("\n")
    body = html.escape(lines[0]) if len(lines) == 1 else "".join(
        '<tspan x="%s" dy="%s">%s</tspan>' % (f(x), "0" if i == 0 else f(size * 1.2), html.escape(t)) for i, t in enumerate(lines))
    op = ' fill-opacity="%s"' % f(min(1, a * 1.1)) if a is not None and a < .9 else ""
    ax.fig.add(z, '<text x="%s" y="%s" text-anchor="%s" dominant-baseline="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s"%s%s>%s</text>' % (
        f(x), f(y), anchor, base, fam, f(size), "600" if bold else "400", col(c), op, rot, body))


FINISHED = {}
CURRENT = [""]                     # the figure being drawn


def finish(fig, W, H, out, bloom=.4, glow=None):
    """The drawing, as inline SVG; the old soft glow becomes the kit's light."""
    els = [s for _, _, s in sorted(fig.els, key=lambda e: (e[0], e[1]))]
    defs = ""
    light = ""
    ident = re.sub(r"[^a-z0-9]+", "-", os.path.basename(str(out)).rsplit(".", 1)[0].lower())
    if glow:
        gx, gy, s = glow
        defs = ('<defs><radialGradient id="kb-%s-g"><stop offset="0" stop-color="#ff7517" stop-opacity=".16"/>'
                '<stop offset=".5" stop-color="#ff7517" stop-opacity=".05"/><stop offset="1" stop-color="#ff7517" stop-opacity="0"/></radialGradient></defs>' % ident)
        light = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#kb-%s-g)"/>' % (f(gx * W), f(gy * H), f(s * W * 1.6), f(s * H * 2.2), ident)
    FINISHED[out] = (W, H, defs + light + "".join(els))


# ------------------------------------------------------------------ a stand-in pyplot
class Done(Exception):
    """Raised by savefig: the drawing is captured; the script's raster post-processing is not needed."""


class _Patch:
    def set_facecolor(self, c):
        pass


class PltFig(Fig):
    def __init__(self, figsize=(24, 9), dpi=100, **k):
        super().__init__(int(figsize[0] * dpi), int(figsize[1] * dpi), BG)
        self.patch = _Patch()
        self.out = None

    def add_axes(self, *a, **k):
        return Ax(self)

    def savefig(self, path, **k):
        finish(self, self.W, self.H, getattr(sys.modules.get("__v4_main__"), "OUT_NAME", path))
        raise Done()

    def get_facecolor(self):
        return BG


def _fake_pyplot():
    plt = types.ModuleType("matplotlib.pyplot")
    plt.figure = lambda *a, **k: PltFig(*a, **k)
    plt.close = lambda *a, **k: None
    plt.rcParams = {}
    plt.switch_backend = lambda *a, **k: None     # matplotlib.use("Agg") in the scripts
    import matplotlib as mpl         # the real package (colours, colour maps); only the drawing is stood in for
    return mpl, plt


def _fill(self, x, y, color=None, fc=None, ec="none", lw=0, alpha=None, zorder=1, **kw):
    P = list(zip(np.asarray(x, float), np.asarray(y, float)))
    self.fig.add(zorder, '<polygon points="%s"%s/>' % (pts(P), style(fc or color or FILL, ec, lw, alpha)))


def _annotate(self, s, xy, xytext=None, color=GR, fontsize=12, ha="left", va="center", arrowprops=None, zorder=7, **kw):
    x, y = xytext if xytext is not None else xy
    T(self, x, y, s, color, fontsize, ha, va, kw.get("fontweight", "normal"), kw.get("alpha", .9), zorder)
    if arrowprops:
        self.fig.add(zorder, arrow_svg(xytext, xy, arrowprops.get("color", color), arrowprops.get("lw", 1), arrowprops.get("alpha", 1)))


class LineCollection:
    def __init__(self, segs, colors=None, linewidths=1, zorder=2, **kw):
        self.segs, self.colors, self.lws, self.z = np.asarray(segs, float), colors, linewidths, zorder


def _add_collection(self, lc):
    """Colour-graded lines: joined into short runs, each with its mean colour."""
    segs = lc.segs
    cols = np.asarray(lc.colors) if lc.colors is not None else None
    lws = np.broadcast_to(np.asarray(lc.lws, float), (len(segs),))
    step = 12
    for i in range(0, len(segs), step):
        chunk = segs[i:i + step]
        P = [chunk[0][0]] + [s_[1] for s_ in chunk]
        if cols is not None and cols.ndim == 2:
            c = cols[i:i + step].mean(axis=0)
            rgb, a = col(c[:3]), float(c[3]) if len(c) > 3 else 1
        else:
            rgb, a = col(cols) if cols is not None else GR, 1
        if a < .03:
            continue
        self.fig.add(lc.z, '<polyline points="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s" '
                     'stroke-linecap="round" vector-effect="non-scaling-stroke"/>' % (pts(P), rgb, f(a), f(width(lws[i]))))


def _imshow(self, img, extent=None, origin="upper", zorder=1, **kw):
    """A soft field (a raster by nature): a small PNG inside the drawing."""
    import base64
    import io
    from PIL import Image
    a = np.asarray(img, float)
    if a.ndim == 3 and a.shape[2] == 4:
        a = np.nan_to_num(a)
        im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGBA")
    else:
        return
    if origin == "lower":
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    w = 260
    im = im.resize((w, max(2, int(im.height * w / im.width))), Image.BILINEAR)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    x0, x1, y0, y1 = extent
    x, y = min(x0, x1), min(y0, y1)
    self.fig.add(zorder, '<image x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none" href="data:image/png;base64,%s"/>' % (
        f(x), f(y), f(abs(x1 - x0)), f(abs(y1 - y0)), base64.b64encode(buf.getvalue()).decode()))


Ax.add_collection = _add_collection
Ax.imshow = _imshow
Ax.fill = _fill
Ax.annotate = _annotate


# ------------------------------------------------------------------ running a script
def run(script, argv):
    """Run one figure script with the kit standing in for matplotlib."""
    common = types.ModuleType("common")
    for k, v in dict(np=np, canvas=canvas, L=L, AR=AR, T=T, finish=finish, BG=BG, OR=OR, ORL=ORL, GR=GR, DIM=DIM, WH=WH,
                     FILL=FILL, Circle=Circle, Polygon=Polygon, Rectangle=Rectangle, Arc=Arc, FancyBboxPatch=FancyBboxPatch,
                     FancyArrowPatch=FancyArrowPatch, Ellipse=Ellipse).items():
        setattr(common, k, v)
    patches = types.ModuleType("matplotlib.patches")
    for k in ("Circle", "Polygon", "Rectangle", "Arc", "FancyBboxPatch", "FancyArrowPatch", "Ellipse", "PathPatch"):
        setattr(patches, k, globals()[k])
    mpath = types.ModuleType("matplotlib.path")
    mpath.Path = Path
    mpl, plt = _fake_pyplot()
    common.plt = plt
    common.matplotlib = mpl
    coll = types.ModuleType("matplotlib.collections")
    coll.LineCollection = LineCollection
    names = ("common", "matplotlib.pyplot", "matplotlib.patches", "matplotlib.path", "matplotlib.collections")
    saved = {k: sys.modules.get(k) for k in names}
    saved_attr = {k: getattr(mpl, k, None) for k in ("pyplot", "patches", "path", "collections")}
    sys.modules["common"], sys.modules["matplotlib.patches"], sys.modules["matplotlib.path"] = common, patches, mpath
    sys.modules["matplotlib.pyplot"], sys.modules["matplotlib.collections"] = plt, coll
    mpl.pyplot, mpl.patches, mpl.path, mpl.collections = plt, patches, mpath, coll
    old_argv, old_path = sys.argv, list(sys.path)
    sys.argv = [script] + argv
    sys.path.insert(0, os.path.dirname(script))
    FINISHED.clear()
    try:
        src = open(script, encoding="utf-8").read()
        g = {"__name__": "__main__", "__file__": script}
        try:
            exec(compile(src, script, "exec"), g)
        except Done:
            pass
    finally:
        sys.argv, sys.path[:] = old_argv, old_path
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
        for k, v in saved_attr.items():
            if v is None:
                try:
                    delattr(mpl, k)
                except AttributeError:
                    pass
            else:
                setattr(mpl, k, v)
    return dict(FINISHED)


# ------------------------------------------------------------------ every figure
SLUG = {"bs": "brand-stories", "ds": "the-dark-side", "kye": "know-your-equipment", "ltd": "living-the-dream",
        "nav": "navigators", "nt": "new-technologies", "rt": "resources-tools-tips", "rvr": "risk-vs-reward",
        "sg": "sky-gods", "st": "storytellers", "wc": "world-cups", "wp": "weather-patterns"}
PART = {"hero": "", "mb": "-millibars", "res": "-resolution"}
LANDING = ("competitions", "core-series", "industry", "meteorology", "technical")
MAKE = {"make_kb_brakes.py": "kb-flight-mechanics-brakes", "make_kb_section.py": "kb-flight-mechanics-section",
        "make_kb_thermal.py": "kb-flight-mechanics-thermal"}


def _nav_land():
    """nav_land.rings() from the Natural Earth 1:110m land kept in tools/data (public domain), in place of the
    copy the original fetched from the geopandas wheel: the same outlines, without the pip download."""
    import json
    m = types.ModuleType("nav_land")
    gj = json.load(open(os.path.join(ROOT, "tools", "data", "ne_110m_land.geojson"), encoding="utf-8"))

    def rings():
        out = []
        for ft in gj["features"]:
            g = ft["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            for poly in polys:
                out.extend([[tuple(p) for p in r] for r in poly])
        return out
    m.rings = rings
    return m


def jobs():
    """(asset name, script, argv) for every knowledge base figure."""
    out = []
    for fn in sorted(os.listdir(KBFIG)):
        pre, _, part = fn[:-3].partition("_")
        if pre in SLUG and part and part != "land":
            out.append(("kb-%s%s" % (SLUG[pre], PART.get(part, "-" + part)), os.path.join(KBFIG, fn), []))
    for slug in LANDING:
        out.append(("kb-" + slug, os.path.join(KBFIG, "landing_hero.py"), [slug]))
    for fn, name in MAKE.items():
        out.append((name, os.path.join(ROOT, "tools", fn), []))
    return out


def svg_file(W, H, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">%s</svg>\n' % (W, H, body))


def main(only):
    import gzip
    os.makedirs(OUT, exist_ok=True)
    try:                                   # the maps' outlines as the original draws them (Natural Earth countries)
        sys.path.insert(0, KBFIG)
        import nav_land
        nav_land.rings()
    except Exception:                      # noqa: BLE001 - offline: the land outlines kept in tools/data
        sys.modules["nav_land"] = _nav_land()
    finally:
        sys.path.remove(KBFIG)
    tot_svg = tot_raster = 0
    for name, script, argv in jobs():
        if only and not any(o in (name, os.path.basename(script)[:-3]) or o in name for o in only):
            continue
        CURRENT[0] = name
        res = run(script, argv + ["/tmp/claude-0/%s.jpg" % name])
        if not res:
            print("v4 kbsvg: NOTHING from %s" % script)
            continue
        W, H, body = list(res.values())[0]
        s = svg_file(W, H, body)
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s)
        gz = len(gzip.compress(s.encode(), 9))
        rp = os.path.join(ROOT, "assets", "images", name + ".webp")
        rb = os.path.getsize(rp) if os.path.exists(rp) else 0
        tot_svg += gz
        tot_raster += rb
        print("%-44s svg %6.1f KB gz   webp %6.1f KB" % (name, gz / 1024, rb / 1024))
    print("v4 kbsvg: svg %.0f KB gz against webp %.0f KB" % (tot_svg / 1024, tot_raster / 1024))
    if not only:                    # the three-view as a file too: the menu's Knowledge Base picture
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        import v4_figs
        open(os.path.join(OUT, "kb-flight-mechanics.svg"), "w", encoding="utf-8").write(v4_figs.three_view("wide") + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
