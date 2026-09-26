#!/usr/bin/env python3
"""
Sample: the drawings three ways (prototypes/v4/samples/drawings-expert.html,
hidden like every sample). The owner asked how the drawings would look made
by a mathematician or scientist, a painter, and a visualisation specialist.
One before/after pair for each:

  1. Flight Mechanics, the brakes (mathematician / scientist): the same
     profile and the same three brake positions as today's drawing, but the
     airflow, the pressure on the skin and the point where the lift acts are
     computed: a Hess-Smith panel method (sources on 120 panels plus one
     circulation, Kutta condition at the trailing edge), 2D, inviscid, at an
     illustrative 6 degrees. Checked against the textbook case first
     (NACA 0012 at 5 degrees: CL 0.60, centre of pressure at 26% of chord).
     Marked as a physics illustration: no separation, so heavy-brake suction
     is overstated.
  2. Meteorology, the opening (painter): the same low and cold front, painted:
     tonal bands between the isobars, line weight falling off with distance,
     isobars kinked at the front as they are on a real chart, the front the
     only orange.
  3. Navigators, the map (visualisation): the same five places on an equal-area
     map (Equal Earth) with a curved graticule, and its own phone version
     instead of a shrunken wide one.

    python3 tools/v4_expert.py && python3 tools/v2_localize.py --site v4
"""
import html
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
import v4_samples as SM  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
f = K.f


def P(pts):
    return " ".join("%s,%s" % (f(x), f(y)) for x, y in pts)


# ---------------------------------------------------------------- 1. the brakes, computed
def influence(px, py, x, y):
    """Velocity at (px, py) from a unit source and a unit vortex spread on each panel."""
    ax_, ay_, bx, by = x[:-1], y[:-1], x[1:], y[1:]
    S = np.hypot(bx - ax_, by - ay_)
    ex, ey = (bx - ax_) / S, (by - ay_) / S
    nx, ny = -ey, ex
    dx, dy = px[:, None] - ax_[None, :], py[:, None] - ay_[None, :]
    xi, eta = dx * ex + dy * ey, dx * nx + dy * ny
    r1, r2 = np.hypot(xi, eta), np.hypot(xi - S, eta)
    beta = np.arctan2(eta, xi - S) - np.arctan2(eta, xi)
    lnr = np.log(np.maximum(r1, 1e-12) / np.maximum(r2, 1e-12))
    u_s, v_s = lnr / (2 * np.pi), beta / (2 * np.pi)
    return (u_s * ex + v_s * nx, u_s * ey + v_s * ny, v_s * ex - u_s * nx, v_s * ey - u_s * ny)


def panel_solve(x, y, aoa):
    """Hess-Smith: a source strength per panel and one vortex strength; flow tangent at every panel,
    Kutta condition at the trailing edge. Panels run clockwise from the trailing edge along the lower surface."""
    N = len(x) - 1
    xc, yc = (x[:-1] + x[1:]) / 2, (y[:-1] + y[1:]) / 2
    S = np.hypot(np.diff(x), np.diff(y))
    tx, ty = np.diff(x) / S, np.diff(y) / S
    nx, ny = -ty, tx
    us, vs, uv, vv = influence(xc, yc, x, y)
    i = np.arange(N)
    us[i, i], vs[i, i], uv[i, i], vv[i, i] = .5 * nx, .5 * ny, .5 * tx, .5 * ty
    Ua, Va = math.cos(aoa), math.sin(aoa)
    A, b = np.zeros((N + 1, N + 1)), np.zeros(N + 1)
    A[:N, :N] = us * nx[:, None] + vs * ny[:, None]
    A[:N, N] = np.sum(uv * nx[:, None] + vv * ny[:, None], axis=1)
    b[:N] = -(Ua * nx + Va * ny)
    At = us * tx[:, None] + vs * ty[:, None]
    Bt = np.sum(uv * tx[:, None] + vv * ty[:, None], axis=1)
    A[N, :N], A[N, N] = At[0] + At[N - 1], Bt[0] + Bt[N - 1]
    b[N] = -((Ua * tx[0] + Va * ty[0]) + (Ua * tx[N - 1] + Va * ty[N - 1]))
    sol = np.linalg.solve(A, b)
    sig, gam = sol[:N], sol[N]
    Vt = At @ sig + Bt * gam + Ua * tx + Va * ty
    Cp = 1 - Vt ** 2
    fx, fy = -np.sum(Cp * S * nx), -np.sum(Cp * S * ny)
    CL = fy * math.cos(aoa) - fx * math.sin(aoa)
    xcp = np.sum(-Cp * S * (xc * ny - yc * nx)) / fy
    return dict(x=x, y=y, xc=xc, yc=yc, nx=nx, ny=ny, S=S, Cp=Cp, sig=sig, gam=gam, aoa=aoa, CL=CL, xcp=xcp)


def velocity(r, px, py):
    us, vs, uv, vv = influence(px, py, r["x"], r["y"])
    return (us @ r["sig"] + uv.sum(1) * r["gam"] + math.cos(r["aoa"]),
            vs @ r["sig"] + vv.sum(1) * r["gam"] + math.sin(r["aoa"]))


def profile(defl, n=121):
    """Today's brakes drawing's profile (tools/make_kb_brakes.py): 17% thick, 5% camber, the last third
    of the chord pulled down by the brake."""
    b = np.linspace(0, np.pi, n)
    c = (1 - np.cos(b)) / 2
    th = 0.17 * (2.969 * np.sqrt(c) - 1.26 * c - 3.516 * c ** 2 + 2.843 * c ** 3 - 1.015 * c ** 4)
    cam = 0.05 * np.sin(np.pi * c)
    tail = np.clip((c - 0.68) / 0.32, 0, 1) ** 2 * defl
    yu, yl = cam + th / 2 - tail, cam - th / 2 - tail
    x = np.r_[c[::-1], c[1:]]
    y = np.r_[yl[::-1], yu[1:]]
    y[0] = y[-1] = (yu[-1] + yl[-1]) / 2
    return x, y


def streamline(r, x0, y0, step=0.012, n=260):
    pts = [(x0, y0)]
    x, y = x0, y0
    for _ in range(n):
        def v(px, py):
            u, w = velocity(r, np.array([px]), np.array([py]))
            m = math.hypot(u[0], w[0]) or 1
            return u[0] / m, w[0] / m
        k1 = v(x, y)
        k2 = v(x + step / 2 * k1[0], y + step / 2 * k1[1])
        k3 = v(x + step / 2 * k2[0], y + step / 2 * k2[1])
        k4 = v(x + step * k3[0], y + step * k3[1])
        x += step / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += step / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        pts.append((x, y))
        if x > 1.75:
            break
    return pts


BRAKES = (("Hands up", 0.0), ("A little brake", 0.052), ("A lot of brake", 0.128))   # the page's words; today's deflections
AOA = 6.0


def brakes_drawing(phone=False):
    W, H = (440, 960) if phone else (1200, 460)
    d = K.Drawing(W, H, "xb-brakes" + ("-p" if phone else ""), "The same profile at three brake positions, with the airflow computed",
                  "Streamlines, the pressure on the surface and the point where the lift acts, computed for today's "
                  "profile hands up, with a little brake and with a lot of brake: a 2D inviscid panel method at an "
                  "illustrative 6 degrees. As the brake comes on, the lift grows and its centre moves back along the "
                  "chord. A physics illustration, not a measurement.", inline_css=False, compact=phone)
    d.backdrop(glow=(220, 480) if phone else (600, 200), glow_r=380, sheet=False)
    a = math.radians(AOA)
    ca, sa = math.cos(-a), math.sin(-a)          # turn the frame so the air arrives level
    for k, (name, defl) in enumerate(BRAKES):
        r = panel_solve(*profile(defl), a)
        ox, oy, sc = (20, 150 + 300 * k, 300.0) if phone else (70 + 400 * k, 215, 250.0)
        ty = 300 * k if phone else 0                  # the panel's top, for its words
        tx = 20 if phone else ox + 20

        def T(px, py):
            rx, ry = px * ca - py * sa, px * sa + py * ca
            return ox + (rx + .15) * sc, oy - ry * sc
        # streamlines: seeded upstream, level; computed through the field
        for y0 in (-.42, -.28, -.16, -.07, .02, .11, .21, .33, .47):
            yy = y0 + math.tan(a) * -0.55
            pts = streamline(r, -0.55, yy + .03)
            q = [T(px, py) for px, py in pts]
            d.raw('<polyline class="d" points="%s" style="stroke-opacity:%s"/>' % (P(q), f(.34 if abs(y0) < .2 else .22)))
        # the surface pressure: suction (Cp < 0) drawn outward in orange, pressure inward in grey
        cp, xc, yc, nx, ny = r["Cp"], r["xc"], r["yc"], r["nx"], r["ny"]
        env = []
        for i in range(0, len(cp)):
            s = -cp[i] * .045                        # length on the page per unit Cp
            s = max(-.05, min(s, .26))
            env.append(T(xc[i] + nx[i] * s, yc[i] + ny[i] * s))
            if i % 5 == 2:
                p0, p1 = T(xc[i], yc[i]), T(xc[i] + nx[i] * s, yc[i] + ny[i] * s)
                d.raw('<line class="%s" x1="%s" y1="%s" x2="%s" y2="%s"/>' % ("a" if cp[i] < 0 else "h", f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1])))
        up = env[len(env) // 2:]
        d.raw('<polyline class="a" points="%s" style="stroke-opacity:.55"/>' % P(up))
        # the profile itself
        d.path("M" + " L".join("%s,%s" % (f(p[0]), f(p[1])) for p in (T(px, py) for px, py in zip(r["x"], r["y"]))) + " Z",
               "outline", fill="card")
        # where the lift acts: a dot on the chord and an arrow as long as the lift
        cx = r["xcp"]
        base = T(cx, np.interp(cx, r["x"][len(r["x"]) // 2:], r["y"][len(r["y"]) // 2:]))
        d.dot(base, 4, True)
        top = (base[0], base[1] - 18 * r["CL"])
        d.arrow((base[0], base[1] - 6), top, "accent", 10)
        d.text((tx, ty + (40 if phone else 58)), name, "lab")
        d.text((tx, ty + (262 if phone else 400)), "lift acts at %d%% of the chord" % round(cx * 100), "val")
        d.text((tx, ty + (282 if phone else 418)), "lift coefficient %.1f" % r["CL"], "sub")
        if k and phone:
            d.line((20, 300 * k), (W - 20, 300 * k), "hair")
        elif k:
            d.line((400 * k, 70), (400 * k, 430), "hair")
    if not phone:
        d.text((W - 20, 448), "2D inviscid panel method · illustrative 6° · no separation, so heavy-brake suction is overstated",
               "tb", "end")
    return d


# ---------------------------------------------------------------- 2. the low and its front, painted
def meteo_drawing():
    W, H = 1600, 600
    xs, ys = np.linspace(0, 1600, 480), np.linspace(0, 600, 190)
    X, Y = np.meshgrid(xs, ys)
    rng = np.random.default_rng(21)
    Z = -1.2 * np.exp(-(((X - 1167) / 220) ** 2 + ((Y - 287) / 173) ** 2))
    for _ in range(4):                                  # today's drawing's gentle background field
        cx, cy, s, amp = rng.uniform(667, 1600), rng.uniform(0, 600), rng.uniform(100, 253), rng.uniform(-1, 1)
        Z += .5 * amp * np.exp(-(((X - cx) / s) ** 2 + ((Y - cy) / s) ** 2))
    t = np.linspace(0, 1, 300)
    fx, fy = 1157 - 280 * t + 33 * np.sin(t * 3), 313 + 267 * t ** 1.1          # today's front, trailing from the low
    # a real front lies in a trough: pressure rises away from it on both sides, so the isobars kink there
    G = np.c_[X.ravel(), Y.ravel()]
    dist = np.full(len(G), np.inf)
    for k in range(0, len(fx), 25):                     # nearest distance to the front, in chunks
        dd = np.hypot(G[:, :1] - fx[None, k:k + 25], G[:, 1:] - fy[None, k:k + 25]).min(axis=1)
        dist = np.minimum(dist, dd)
    Z -= .16 * np.exp(-(dist.reshape(X.shape) / 70) ** 2) * np.clip((Y - 240) / 90, 0, 1)
    import contourpy
    gen = contourpy.contour_generator(X, Y, Z)
    levels = np.linspace(Z.min() + .05, Z.max() - .05, 16)
    d = K.Drawing(W, H, "xm-low", "A low with its cold front, painted",
                  "Isobars round a low, laid in tonal bands that deepen toward the centre, the lines heavier near the low "
                  "and fading with distance, bent where they cross the front as they are on a real chart; the cold front, "
                  "with its triangles, the only colour.", inline_css=False)
    # the light: one warm source over the low, falling off to the left
    d.raw('<defs><radialGradient id="xm-light" cx="72%" cy="48%" r="55%"><stop offset="0" stop-color="#ff7517" stop-opacity=".10"/>'
          '<stop offset=".6" stop-color="#ff7517" stop-opacity=".025"/><stop offset="1" stop-color="#ff7517" stop-opacity="0"/></radialGradient>'
          '<linearGradient id="xm-fade" x1="0" x2="1"><stop offset="0" stop-color="#141519"/><stop offset=".4" stop-color="#141519" stop-opacity="0"/></linearGradient></defs>')
    # tonal bands, darker to lighter toward the centre of the low
    for i in range(len(levels) - 1):
        polys = gen.filled(levels[i], levels[i + 1])
        tone = 1 - i / (len(levels) - 1)
        for pts, offs in zip(*polys):
            dpath = ""
            for a_, b_ in zip(offs[:-1], offs[1:]):
                ring = pts[a_:b_]
                if len(ring) > 2:
                    dpath += "M" + " L".join("%s,%s" % (f(px), f(py)) for px, py in ring[::2]) + " Z"
            if dpath:
                d.raw('<path d="%s" fill="#dfe3ea" fill-opacity="%s" fill-rule="evenodd"/>' % (dpath, f(.012 + .075 * tone ** 2)))
    d.raw('<rect width="%d" height="%d" fill="url(#xm-light)"/>' % (W, H))
    # the isobars: heavier near the low, lighter far out
    for i, lv in enumerate(levels):
        tone = 1 - i / (len(levels) - 1)
        for line in gen.lines(lv):
            if len(line) > 3:
                d.raw('<polyline points="%s" fill="none" stroke="#c9ccd3" stroke-opacity="%s" stroke-width="%s" '
                      'vector-effect="non-scaling-stroke" stroke-linejoin="round"/>' % (P(line[::2]), f(.16 + .5 * tone ** 1.5), f(.6 + 1.3 * tone ** 2)))
    # the front: the only orange, triangles pointing the way it moves (toward the warm side, east)
    d.raw('<polyline class="a" points="%s" style="stroke-width:2.4px"/>' % P(np.c_[fx, fy][::3]))
    for k in np.linspace(.07, .93, 10):
        i = int(k * 299)
        dx, dy = fx[i + 1] - fx[i - 1], fy[i + 1] - fy[i - 1]
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        nxv, nyv = -uy, ux
        if nxv < 0:
            nxv, nyv = -nxv, -nyv
        tri = [(fx[i] - ux * 10, fy[i] - uy * 10), (fx[i] + ux * 10, fy[i] + uy * 10), (fx[i] + nxv * 16, fy[i] + nyv * 16)]
        d.raw('<polygon class="fa" points="%s"/>' % P(tri))
    d.raw('<text x="1167" y="297" text-anchor="middle" style="font-family:var(--font-display);font-weight:700;font-size:26px;fill:#f6f4f4;fill-opacity:.8">L</text>')
    d.raw('<rect width="%d" height="%d" fill="url(#xm-fade)"/>' % (W, H))
    return d


# ---------------------------------------------------------------- 3. the Navigators map, equal area
PLACES = [("Cauca Valley", "Colombia", 4.0, -76.2), ("Kijabe", "Kenya", -0.93, 36.6), ("Bir", "India", 32.05, 76.72),
          ("Panchgani", "India", 17.9, 73.8), ("Manilla", "Australia", -30.75, 150.7)]     # today's map's places


def equal_earth(lat, lon):
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
    M = math.sqrt(3) / 2
    phi, lam = math.radians(lat), math.radians(lon)
    th = math.asin(M * math.sin(phi))
    x = lam * math.cos(th) / (M * (A1 + 3 * A2 * th ** 2 + th ** 6 * (7 * A3 + 9 * A4 * th ** 2)))
    y = th * (A1 + A2 * th ** 2 + th ** 6 * (A3 + A4 * th ** 2))
    return x, y


def land_rings():
    sys.path.insert(0, os.path.join(ROOT, "tools", "kbfig"))
    try:
        import nav_land
        return nav_land.rings()
    except Exception:            # noqa: BLE001 - offline: the land outlines kept in tools/data
        import v4_kbsvg
        return v4_kbsvg._nav_land().rings()


def map_drawing(phone=False):
    W, H = (720, 300) if phone else (1600, 640)
    ox, oy, sc = (W / 2, 150, 108) if phone else (1010, 300, 205)
    Pj = lambda la, lo: (ox + equal_earth(la, lo)[0] * sc, oy - equal_earth(la, lo)[1] * sc)
    d = K.Drawing(W, H, "xn-map" + ("-p" if phone else ""), "The places the Navigators conversations are about, on an equal-area map",
                  "Colombia's Cauca Valley, Kijabe in Kenya, Bir and Panchgani in India and Manilla in Australia, on an Equal "
                  "Earth map, which keeps every country's area true, with a curved graticule every 30 degrees.",
                  inline_css=False, compact=phone)
    # the graticule, curved as the projection curves it
    for lo in range(-180, 181, 30):
        d.raw('<polyline class="g" points="%s"/>' % P([Pj(la, lo) for la in range(-60, 81, 5)]))
    for la in range(-60, 81, 30):
        d.raw('<polyline class="g" points="%s"/>' % P([Pj(la, lo) for lo in range(-180, 181, 5)]))
    outline = [Pj(la, -180) for la in range(-60, 81, 5)] + [Pj(80, lo) for lo in range(-180, 181, 10)] + \
              [Pj(la, 180) for la in range(80, -61, -5)] + [Pj(-60, lo) for lo in range(180, -181, -10)]
    d.raw('<polygon class="h" points="%s" style="fill:none"/>' % P(outline))
    body = []
    for ring in land_rings():
        lons = [lo for lo, la in ring]
        if max(lons) - min(lons) > 180:
            continue
        pts = [Pj(max(-60, min(80, la)), lo) for lo, la in ring[::2] if la > -61]
        if len(pts) > 2:
            body.append("M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) + " Z")
    d.raw('<path class="f" d="%s"/><path class="d" d="%s" style="stroke-opacity:.5"/>' % ("".join(body), "".join(body)))
    for i, (name, country, la, lo) in enumerate(PLACES):
        x, y = Pj(la, lo)
        d.raw('<circle cx="%s" cy="%s" r="%s" fill="#ff7517" fill-opacity=".16"/>' % (f(x), f(y), f(12 if phone else 16)))
        d.dot((x, y), 4.2, True)
        if phone:
            d.text((x, y - 12), str(i + 1), "vn", "middle")
        else:
            dx = {"Cauca Valley": -24, "Kijabe": 24, "Bir": -22, "Panchgani": 24, "Manilla": -24}[name]
            dy = {"Cauca Valley": 36, "Kijabe": 40, "Bir": -28, "Panchgani": 30, "Manilla": 34}[name]
            anchor = "end" if dx < 0 else "start"
            d.poly([(x, y), (x + dx * .7, y + dy * .8)], "hair")
            d.text((x + dx, y + dy), name, "lab", anchor)
            d.text((x + dx, y + dy + 15), country, "sub", anchor)
    if not phone:
        d.text((W - 20, H - 16), "Equal Earth projection · graticule every 30° · places named in the conversations", "tb", "end")
    return d


# ---------------------------------------------------------------- the sample page
CSS = SM.SPEC_CSS + """
.xs-sec{padding:var(--sp-5) var(--gutter);max-width:1240px;margin:0 auto;}
.xs-sec h2{font-family:var(--font-display);font-size:var(--fs-h2);color:var(--white);margin:0 0 var(--sp-1);}
.xs-lens{color:var(--orange);font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;}
.xs-why{color:var(--gray-light);max-width:70ch;line-height:1.7;margin:var(--sp-2) 0 var(--sp-3);}
.xs-pair{display:grid;grid-template-columns:1fr;gap:var(--sp-3);}
.xs-pair figure{margin:0;background:#141519;border:1px solid var(--line);padding:var(--sp-2);}
.xs-pair figure svg,.xs-pair figure img{display:block;width:100%;height:auto;}
.xs-pair figcaption{margin-top:var(--sp-1);font-size:var(--fs-small);color:var(--gray);}
.xs-pair figcaption b{color:var(--white);font-weight:600;margin-right:.4rem;}
.xs-phone{display:none;}
.xs-list{display:none;list-style:none;margin:var(--sp-2) 0 0;padding:0;counter-reset:n;}
.xs-list li{counter-increment:n;padding:.5rem 0;border-top:1px solid var(--line);color:var(--white);font-weight:600;}
.xs-list li::before{content:counter(n);color:var(--orange);font-family:var(--font-display);margin-right:.8rem;}
.xs-list li span{color:var(--gray);font-weight:400;margin-left:.4rem;}
@media (max-width:760px){.xs-wide{display:none;} .xs-phone{display:block;} .xs-list{display:block;}}
"""


def inline(name):
    s = open(os.path.join(V4, "img", "kb", name + ".svg"), encoding="utf-8").read().strip()
    return s.replace("<svg ", '<svg role="img" aria-label="today\'s drawing" ', 1)


def section(lens, title, why, before, after, note=""):
    return ('<section class="xs-sec"><span class="xs-lens">%s</span><h2>%s</h2><p class="xs-why">%s</p>'
            '<div class="xs-pair"><figure>%s<figcaption><b>Today</b>the knowledge base drawing as it is in v4.</figcaption></figure>'
            '<figure>%s<figcaption><b>Redrawn</b>%s</figcaption></figure></div></section>' % (lens, title, why, before, after, note))


def page():
    list_html = '<ol class="xs-list">%s</ol>' % "".join("<li>%s<span>%s</span></li>" % (n, c) for n, c, _, _ in PLACES)
    body = ('<header class="kit-hero is-sky v2-page-hero"><div class="kit-hero-copy"><span class="kit-kicker">Sample, not live</span>'
            '<h1>The drawings, three ways</h1><p class="kit-intro">Three knowledge base drawings as a mathematician, a painter and a '
            'visualisation specialist would make them. Pick a direction before the rest are redrawn.</p></div></header>')
    body += section("Mathematician and scientist", "Flight Mechanics: the brakes, computed",
                    "Today's drawing illustrates the idea with hand-drawn airflow. Here the same profile at the same three brake "
                    "positions is put through a real calculation: the streamlines, the pressure on the surface (orange where it "
                    "sucks, grey where it presses) and the point where the lift acts all come out of it. It agrees with the "
                    "episode: as the brake comes on, the lift grows and moves back along the chord, if by less than today's "
                    "drawing suggests.",
                    inline("kb-flight-mechanics-brakes"),
                    '<div class="xs-wide">%s</div><div class="xs-phone">%s</div>' % (brakes_drawing().svg(), brakes_drawing(True).svg()),
                    "A 2D inviscid panel method (Hess-Smith, 120 panels), checked on the textbook case first. A physics "
                    "illustration at an assumed 6°, not a measurement of a real wing: it ignores separation, so the suction at "
                    "heavy brake is overstated. On a phone the three positions stack.")
    body += section("Painter", "Meteorology: the low and its front, painted",
                    "The same subject, composed as a picture: one light, one focal point, the only colour on the front. Tonal "
                    "bands deepen toward the centre of the low; the lines are heavier close in and fade with distance; the "
                    "isobars bend where they cross the front, as they do on a real chart, and the front's triangles point the "
                    "way it moves.",
                    inline("kb-meteorology"), meteo_drawing().svg(),
                    "Same field and front as today's; no new data.")
    body += section("Visualisation specialist", "Navigators: the map, equal area and made for a phone",
                    "Today's map uses a stretched rectangle, where the far north swells and Africa looks small, and on a phone it "
                    "shrinks until the names can't be read. Here it is on an Equal Earth map, which keeps every country's area "
                    "true, with the graticule curving as the projection does; on a phone it becomes its own drawing, numbered, "
                    "with the names in a list you can read.",
                    inline("kb-navigators"),
                    '<div class="xs-wide">%s</div><div class="xs-phone">%s%s</div>' % (map_drawing().svg(), map_drawing(True).svg(), list_html),
                    "Same five places as today. Narrow the window, or open this on a phone, to see the phone version.")
    return SM.shell("The drawings, three ways", "Three knowledge base drawings redrawn by lens: computed, painted, and made for a phone.",
                    body, CSS)


def main():
    out = os.path.join(V4, "samples", "drawings-expert.html")
    open(out, "w", encoding="utf-8").write(page())
    print("v4 expert sample: samples/drawings-expert.html")


if __name__ == "__main__":
    main()
