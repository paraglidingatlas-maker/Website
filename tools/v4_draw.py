#!/usr/bin/env python3
"""
The v4 drawing kit: technical drawings as inline SVG, one look for every
figure on the site.

  weights    a thick outline (2px), thin detail (1px), hairline dimensions and
             leaders (.75px). Strokes do not scale with the drawing
             (vector-effect), so a figure keeps its weights on a phone.
  type       the site's own (DM Sans for labels, Poppins for the title), set in
             the page: the SVG is inline, so it inherits the page's fonts.
  pieces     callouts with leaders, dimension lines with extension lines and
             arrowheads, angle arcs, hatching, real curves (Catmull-Rom splines
             turned into cubic Beziers, true circular and elliptical arcs), view
             labels, and a title block that cites the episode and the chapter
             where the page cites one.
  colour     the site's colours on dark: white outline, grey detail, orange for
             the one thing the figure is about.

The rule for content: every label, number and dimension comes from the page's
own text or the episode it cites. What the source does not give is left out.
No scale bar without a real scale: a title block says "Not to scale".

    import v4_draw as K
    d = K.Drawing(1200, 640, "fig-id", title="...", desc="...")
    d.spline([(x, y), ...], closed=True, w="outline", fill=True)
    d.callout((x, y), (lx, ly), "Trailing edge")
    d.dim((x1, y1), (x2, y2), 18, "7 cm")
    svg = d.svg()
"""
import html
import math

WEIGHTS = {"outline": 2.0, "detail": 1.0, "hair": 0.75, "ghost": 0.75}
CSS = """
.{p}{{font-family:var(--font-body,'DM Sans',system-ui,sans-serif);}}
.{p} .o{{fill:none;stroke:var(--white,#f6f4f4);stroke-width:2;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke;}}
.{p} .d{{fill:none;stroke:#b4b4b4;stroke-opacity:.72;stroke-width:1;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;}}
.{p} .h{{fill:none;stroke:#8d8d8d;stroke-width:.75;stroke-linecap:round;vector-effect:non-scaling-stroke;}}
.{p} .g{{fill:none;stroke:#737373;stroke-opacity:.55;stroke-width:.75;stroke-dasharray:6 5;vector-effect:non-scaling-stroke;}}
.{p} .c{{fill:none;stroke:#737373;stroke-opacity:.5;stroke-width:.75;stroke-dasharray:14 4 2 4;vector-effect:non-scaling-stroke;}}
.{p} .a{{fill:none;stroke:var(--orange,#ff7517);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;}}
.{p} .f{{fill:#202127;}}
.{p} .fa{{fill:var(--orange,#ff7517);}}
.{p} .fw{{fill:var(--white,#f6f4f4);}}
.{p} .fh{{fill:#8d8d8d;}}
.{p} .fx{{fill:url(#{p}-hatch);}}
.{p} .hl{{stroke:#737373;stroke-width:.75;vector-effect:non-scaling-stroke;}}
.{p} text{{fill:#b4b4b4;font-size:12px;letter-spacing:.02em;}}
.{p} .lab{{fill:var(--white,#f6f4f4);font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;}}
.{p} .sub{{fill:#8d8d8d;font-size:11px;}}
.{p} .val{{fill:var(--orange,#ff7517);font-size:12.5px;font-weight:600;letter-spacing:.04em;}}
.{p} .vw{{fill:#737373;font-size:10.5px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;}}
.{p} .vn{{fill:var(--orange,#ff7517);font-family:var(--font-display,'Poppins',sans-serif);font-size:13px;font-weight:700;}}
.{p} .tb{{fill:#8d8d8d;font-size:9.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;}}
.{p} .tt{{fill:var(--white,#f6f4f4);font-family:var(--font-display,'Poppins',sans-serif);font-size:14px;font-weight:700;letter-spacing:0;}}
.{p} .tv{{fill:#b4b4b4;font-size:11px;}}
"""


COMPACT = """
.{p} .lab{{font-size:10px;letter-spacing:.1em;}}
.{p} .sub{{font-size:10.5px;}}
"""


def f(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pts(ps):
    return " ".join("%s,%s" % (f(x), f(y)) for x, y in ps)


def catmull(points, closed=False, tension=0.5):
    """A smooth curve through the points: Catmull-Rom, written as cubic Beziers."""
    P = list(points)
    if len(P) < 3:
        return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in P)
    n = len(P)
    get = (lambda i: P[i % n]) if closed else (lambda i: P[max(0, min(n - 1, i))])
    segs = n if closed else n - 1
    d = "M%s,%s" % (f(P[0][0]), f(P[0][1]))
    k = tension / 3.0 * 2
    for i in range(segs):
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 2, p1[1] + (p2[1] - p0[1]) * k / 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 2, p2[1] - (p3[1] - p1[1]) * k / 2)
        d += " C%s,%s %s,%s %s,%s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d + (" Z" if closed else "")


def unit(v):
    L = math.hypot(v[0], v[1]) or 1.0
    return (v[0] / L, v[1] / L)


def add(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


class Drawing:
    def __init__(self, w, h, ident, title="", desc="", cls="", compact=False):
        self.w, self.h, self.id = w, h, ident
        self.compact = compact          # a phone drawing: labels a size smaller
        self.title, self.desc, self.cls = title, desc, cls
        self.el = []

    # ---- primitives -------------------------------------------------------
    def raw(self, s):
        self.el.append(s)

    def path(self, d, w="detail", fill=None, extra=""):
        c = {"outline": "o", "detail": "d", "hair": "h", "ghost": "g", "centre": "c", "accent": "a"}[w]
        cls = c + ({"card": " f", "hatch": " fx", None: ""}[fill] if fill in ("card", "hatch", None) else "")
        if fill == "card":
            # a filled shape: the fill underneath, then the stroke
            self.el.append('<path class="f" d="%s"/>' % d)
            cls = c
        elif fill == "hatch":
            self.el.append('<path class="f" d="%s"/><path class="fx" d="%s"/>' % (d, d))
            cls = c
        self.el.append('<path class="%s" d="%s"%s/>' % (cls, d, extra))

    def line(self, p, q, w="detail"):
        self.path("M%s,%s L%s,%s" % (f(p[0]), f(p[1]), f(q[0]), f(q[1])), w)

    def poly(self, ps, w="detail", closed=False, fill=None):
        d = "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in ps) + (" Z" if closed else "")
        self.path(d, w, fill)

    def spline(self, ps, w="outline", closed=False, fill=None, tension=0.5):
        self.path(catmull(ps, closed, tension), w, fill)

    def circle(self, c, r, w="detail", fill=None):
        d = "M%s,%s a%s,%s 0 1,0 %s,0 a%s,%s 0 1,0 %s,0" % (
            f(c[0] - r), f(c[1]), f(r), f(r), f(2 * r), f(r), f(r), f(-2 * r))
        self.path(d, w, fill)

    def arc(self, c, rx, ry, a0, a1, w="detail"):
        """A true elliptical arc, angles in degrees, 0 = +x, 90 = +y (down)."""
        p0 = (c[0] + rx * math.cos(math.radians(a0)), c[1] + ry * math.sin(math.radians(a0)))
        p1 = (c[0] + rx * math.cos(math.radians(a1)), c[1] + ry * math.sin(math.radians(a1)))
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 1 if a1 > a0 else 0
        self.path("M%s,%s A%s,%s 0 %d,%d %s,%s" % (f(p0[0]), f(p0[1]), f(rx), f(ry), large, sweep, f(p1[0]), f(p1[1])), w)

    def dot(self, p, r=2.6, accent=True):
        self.el.append('<circle class="%s" cx="%s" cy="%s" r="%s"/>' % ("fa" if accent else "fw", f(p[0]), f(p[1]), f(r)))

    def head(self, tip, direction, size=8, accent=False, open_=False):
        """An arrowhead at tip, pointing along direction."""
        u = unit(direction)
        n = (-u[1], u[0])
        b = add(tip, u, -size)
        a1, a2 = add(b, n, size * .32), add(b, n, -size * .32)
        cls = "fa" if accent else "fh"
        self.el.append('<path class="%s" d="M%s,%s L%s,%s L%s,%s Z"/>' % (
            cls, f(tip[0]), f(tip[1]), f(a1[0]), f(a1[1]), f(a2[0]), f(a2[1])))

    def arrow(self, p, q, w="accent", size=9):
        u = unit((q[0] - p[0], q[1] - p[1]))
        self.line(p, add(q, u, -size * .7), w)
        self.head(q, u, size, accent=(w == "accent"))

    def text(self, p, s, cls="", anchor="start", rotate=None, dy=None):
        tr = ' transform="rotate(%s %s %s)"' % (f(rotate), f(p[0]), f(p[1])) if rotate else ""
        dys = ' dy="%s"' % dy if dy else ""
        self.el.append('<text x="%s" y="%s"%s%s%s%s>%s</text>' % (
            f(p[0]), f(p[1]), ' class="%s"' % cls if cls else "",
            ' text-anchor="%s"' % anchor if anchor != "start" else "", dys, tr, html.escape(s)))

    # ---- drawing pieces -----------------------------------------------------
    def callout(self, target, at, label, sub=None, anchor=None, accent=False, elbow=True):
        """A dot on the part, a leader (with a short horizontal shoulder) to the
        label. anchor: 'start' puts the text right of the shoulder, 'end' left."""
        if anchor is None:
            anchor = "start" if at[0] >= target[0] else "end"
        sh = 14 if anchor == "start" else -14
        knee = at
        end = (at[0] + sh, at[1]) if elbow else at
        self.poly([target, knee, end], "hair")
        self.dot(target, 2.4, accent)
        tx = end[0] + (5 if anchor == "start" else -5)
        self.text((tx, end[1] + 4), label, "lab", anchor)
        if sub:
            for i, line in enumerate(sub if isinstance(sub, (list, tuple)) else [sub]):
                self.text((tx, end[1] + 19 + 14 * i), line, "sub", anchor)

    def dim(self, p, q, offset, label, sub=None, ext=True, gap=4, side_label=None):
        """A dimension: extension lines from p and q, offset along the normal,
        a hairline with arrowheads, the value in orange at its middle."""
        u = unit((q[0] - p[0], q[1] - p[1]))
        n = (-u[1], u[0])
        a, b = add(p, n, offset), add(q, n, offset)
        if ext:
            s = 1 if offset > 0 else -1
            self.line(add(p, n, s * gap), add(a, n, s * 6), "hair")
            self.line(add(q, n, s * gap), add(b, n, s * 6), "hair")
        self.line(add(a, u, 1), add(b, u, -1), "hair")
        self.head(a, (-u[0], -u[1]), 7)
        self.head(b, u, 7)
        m = lerp(a, b, .5)
        ang = math.degrees(math.atan2(u[1], u[0]))
        if ang > 90 or ang < -90:
            ang += 180
        if side_label:          # value beside a short dimension instead of on it
            self.text(side_label, label, "val")
            if sub:
                self.text((side_label[0], side_label[1] + 15), sub, "sub")
            return
        off = add(m, n, -7 if offset >= 0 else 14)
        self.text(off, label, "val", "middle", rotate=ang if abs(ang) > 1 else None)
        if sub:
            self.text(add(off, n, -14), sub, "sub", "middle", rotate=ang if abs(ang) > 1 else None)

    def angle(self, c, r, a0, a1, label, lab_r=None, accent=True):
        self.arc(c, r, r, a0, a1, "accent" if accent else "hair")
        m = math.radians((a0 + a1) / 2)
        rr = lab_r or r + 12
        self.text((c[0] + rr * math.cos(m), c[1] + rr * math.sin(m) + 4), label, "val" if accent else "sub",
                  "start" if math.cos(m) >= 0 else "end")

    def view(self, p, number, name):
        """A view label under a view: its letter in orange, the name spaced out."""
        self.text(p, number, "vn")
        self.text((p[0] + 16, p[1] - 1), name, "vw")
        self.line((p[0], p[1] + 8), (p[0] + 150, p[1] + 8), "hair")

    def title_block(self, x, y, w, title, rows):
        """Bottom-right title block: a title, then label / value rows."""
        rh = 17
        h = 30 + rh * len(rows)
        self.el.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#141519" fill-opacity=".6" '
                       'stroke="#737373" stroke-opacity=".55" stroke-width=".75" vector-effect="non-scaling-stroke"/>'
                       % (f(x), f(y), f(w), f(h)))
        self.line((x, y + 28), (x + w, y + 28), "hair")
        self.el.append('<rect class="fa" x="%s" y="%s" width="3" height="28"/>' % (f(x), f(y)))
        self.text((x + 12, y + 19), title, "tt")
        for i, (k, v) in enumerate(rows):
            yy = y + 28 + rh * (i + 1) - 5
            self.text((x + 12, yy), k, "tb")
            self.text((x + 88, yy), v, "tv")

    def frame(self, pad=8):
        """A drawing border with corner ticks, as on a drawing sheet."""
        x0, y0, x1, y1 = pad, pad, self.w - pad, self.h - pad
        L = 18
        for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
            self.poly([(cx + dx * L, cy), (cx, cy), (cx, cy + dy * L)], "hair")

    # ---- output ---------------------------------------------------------------
    def svg(self, extra_cls=""):
        p = "dk-" + self.id
        defs = ('<defs><pattern id="%s-hatch" width="6" height="6" patternUnits="userSpaceOnUse" '
                'patternTransform="rotate(45)"><line class="hl" x1="0" y1="0" x2="0" y2="6"/></pattern></defs>' % p)
        t = ('<title id="%s-t">%s</title><desc id="%s-d">%s</desc>' % (p, html.escape(self.title), p, html.escape(self.desc)))
        return ('<svg class="dk %s%s" viewBox="0 0 %s %s" role="img" aria-labelledby="%s-t %s-d" '
                'xmlns="http://www.w3.org/2000/svg">%s<style>%s</style>%s%s</svg>' % (
                    p, (" " + extra_cls) if extra_cls else "", f(self.w), f(self.h), p, p, t,
                    " ".join((CSS.format(p=p) + (COMPACT.format(p=p) if self.compact else "")).split()),
                    defs, "".join(self.el)))
