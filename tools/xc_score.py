#!/usr/bin/env python3
"""Score a tracklog the way XContest does.

Three routes are tried over the airborne fixes and the one worth the most points wins:

  free flight     start, up to three turnpoints, end; the legs summed            1.0 pt/km
  free triangle   three turnpoints whose closing gap (route start to route end)
                  is under 20% of the three legs; scored as legs minus the gap   1.2 pt/km
                  (1.4 when the gap is under 5%: a closed triangle)
  FAI triangle    a free triangle whose shortest leg is at least 28% of the legs  1.4 pt/km
                  (1.6 when closed)

The search runs on every n-th fix so that at most ~720 points are in play, then each
of the five route points is moved through its neighbours at full resolution until
nothing improves. Distances are great-circle on the FAI sphere (6371 km), the same
sphere the IGC pipeline sums the track on.

    from xc_score import score
    r = score([(t, lat, lon, alt), ...])
    r["type"], r["closed"], r["distance_km"], r["points"], r["legs_km"], r["gap_km"], r["route"] (5 fix indices)
"""
import math
import numpy as np

R = 6371.0
MULT = {"free flight": 1.0, "free triangle": 1.2, "FAI triangle": 1.4}
MULT_CLOSED = {"free triangle": 1.4, "FAI triangle": 1.6}
MAX_N = 720


def unit(lat, lon):
    la, lo = np.radians(np.asarray(lat, float)), np.radians(np.asarray(lon, float))
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)


def dist(U, V):
    """great-circle km between rows of U and rows of V (broadcasting on the leading axes)"""
    c = np.clip(np.sum(U * V, axis=-1), -1, 1)
    return 2 * R * np.arcsin(np.clip(np.sqrt(np.maximum(0, 2 - 2 * c)) / 2, 0, 1))


def dmat(U):
    return dist(U[:, None, :], U[None, :, :])


def free_dp(D):
    """best start, three turnpoints, end over the sampled fixes: four legs summed"""
    N = len(D); NEG = -1e18
    tri = np.triu(np.ones((N, N), bool), 1)
    M = np.where(tri, D, NEG); args = [M.argmax(axis=0)]; best = M.max(axis=0)
    for _ in range(3):
        M = np.where(tri, best[:, None] + D, NEG); args.append(M.argmax(axis=0)); best = M.max(axis=0)
    j = int(best.argmax()); total = float(best[j]); path = [j]
    for a in reversed(args):
        j = int(a[j]); path.append(j)
    return total, path[::-1]


def tri_dp(D, fai):
    """best triangle under the closing rule (and the 28% leg rule for FAI): legs minus gap"""
    N = len(D); idx = np.arange(N)
    G = D.copy()                                              # G[a, c] = min over s <= a, e >= c of D[s, e]
    for a in range(1, N): G[a] = np.minimum(G[a], G[a - 1])
    for c in range(N - 2, -1, -1): G[:, c] = np.minimum(G[:, c], G[:, c + 1])
    upper = idx[None, :] > idx[:, None]                       # b < c
    best, at = -1.0, None
    for a in range(N - 2):
        ab = D[a]
        P = ab[:, None] + D + ab[None, :]                     # P[b, c] = D[a,b] + D[b,c] + D[c,a]
        valid = upper & (idx > a)[:, None]
        if fai:
            valid &= np.minimum(np.minimum(ab[:, None], D), ab[None, :]) >= 0.28 * P
        gap = G[a][None, :]
        valid &= gap < 0.2 * P
        sc = np.where(valid, P - gap, -1.0)
        k = int(sc.argmax()); b, c = divmod(k, N)
        if sc[b, c] > best:
            best, at = float(sc[b, c]), (a, b, c)
    if at is None:
        return None
    a, b, c = at
    sub = D[:a + 1, c:]; k = int(sub.argmin()); s, e = divmod(k, sub.shape[1]); e += c
    return best, [s, a, b, c, e]


def route_value(U, r, kind):
    """the scored distance of route r (five fix indices) of the given kind, or -1 if it breaks the rules"""
    s, a, b, c, e = r
    if not (s <= a < b < c <= e):
        return -1.0
    if kind == "free flight":
        return float(dist(U[s], U[a]) + dist(U[a], U[b]) + dist(U[b], U[c]) + dist(U[c], U[e]))
    legs = np.array([dist(U[a], U[b]), dist(U[b], U[c]), dist(U[c], U[a])]); P = float(legs.sum()); gap = float(dist(U[s], U[e]))
    if gap >= 0.2 * P or (kind == "FAI triangle" and legs.min() < 0.28 * P):
        return -1.0
    return P - gap


def refine(U, r, kind, step):
    """move each route point through its full-resolution neighbours until nothing improves"""
    n = len(U); r = list(r); val = route_value(U, r, kind)
    for _ in range(8):
        moved = False
        for k in range(5):
            lo, hi = max(0, r[k] - step), min(n - 1, r[k] + step)
            if k > 0: lo = max(lo, r[k - 1] + (0 if k in (1, 4) else 1))
            if k < 4: hi = min(hi, r[k + 1] - (0 if k in (0, 3) else 1))
            cand = np.arange(lo, hi + 1)
            if not len(cand):
                continue
            s, a, b, c, e = r
            if kind == "free flight":
                pts = [s, a, b, c, e]
                prev = U[pts[k - 1]] if k > 0 else None; nxt = U[pts[k + 1]] if k < 4 else None
                v = np.zeros(len(cand))
                if prev is not None: v += dist(prev[None], U[cand])
                if nxt is not None: v += dist(U[cand], nxt[None])
                base = val - ((dist(U[pts[k - 1]], U[pts[k]]) if k > 0 else 0) + (dist(U[pts[k]], U[pts[k + 1]]) if k < 4 else 0))
                tot = base + v
                j = int(tot.argmax())
                if tot[j] > val + 1e-9:
                    r[k] = int(cand[j]); val = float(tot[j]); moved = True
            else:
                bestv, bestj = val, None
                for j in cand:
                    rr = r[:]; rr[k] = int(j); vv = route_value(U, rr, kind)
                    if vv > bestv + 1e-9: bestv, bestj = vv, int(j)
                if bestj is not None:
                    r[k] = bestj; val = bestv; moved = True
        if not moved:
            break
    return val, r


def score(fixes):
    """fixes: (t, lat, lon, alt) in time order, airborne only. Returns the best route by XContest points."""
    n = len(fixes)
    U = unit([f[1] for f in fixes], [f[2] for f in fixes])
    stride = max(1, int(math.ceil(n / float(MAX_N))))
    samp = list(range(0, n, stride))
    if samp[-1] != n - 1: samp.append(n - 1)
    Us = U[samp]; D = dmat(Us)
    out = []
    fv, fr = free_dp(D)
    fv, fr = refine(U, [samp[i] for i in fr], "free flight", stride)
    out.append(("free flight", fv, fr))
    for kind in ("free triangle", "FAI triangle"):
        t = tri_dp(D, kind == "FAI triangle")
        if t is None:
            continue
        tv, tr = refine(U, [samp[i] for i in t[1]], kind, stride)
        if tv > 0:
            out.append((kind, tv, tr))
    best = None
    for kind, v, r in out:
        s, a, b, c, e = r
        if kind == "free flight":
            legs = [float(dist(U[s], U[a])), float(dist(U[a], U[b])), float(dist(U[b], U[c])), float(dist(U[c], U[e]))]; gap = None; closed = False; mult = MULT[kind]
        else:
            legs = [float(dist(U[a], U[b])), float(dist(U[b], U[c])), float(dist(U[c], U[a]))]; gap = float(dist(U[s], U[e])); closed = gap < 0.05 * sum(legs)
            mult = MULT_CLOSED[kind] if closed else MULT[kind]
        pts = v * mult
        cand = dict(type=kind, closed=closed, distance_km=round(v, 2), points=round(pts, 2), legs_km=[round(x, 2) for x in legs], gap_km=None if gap is None else round(gap, 2), route=r, multiplier=mult)
        if best is None or pts > best["points"]:
            best = cand
    return best


if __name__ == "__main__":
    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from igc_tracks import parse
    for path in sys.argv[1:]:
        date, fixes, pilot, glider = parse(path)
        print(path, date, score(fixes))
