"""Graphics for the booking emails: a map plate and a terrain profile, both
drawn from the open terrain data already in the repo (tools/data). Writes
assets/email/india-map.jpg (1200x560) and assets/email/india-profile.png
(1200x260), shown at half size in the 600 px email so they stay sharp on
retina screens. Fonts: pass a directory holding DMMono-Regular.ttf,
DMMono-Medium.ttf, Poppins-ExtraBold.ttf (argv[1])."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = sys.argv[1]
OUT = os.path.join(ROOT, "assets", "email")
os.makedirs(OUT, exist_ok=True)
BG = (20, 21, 25); CARD = (32, 33, 39); ORANGE = (255, 117, 23)
INK = (246, 244, 244); MUTED = (180, 180, 180); HAIR = (60, 62, 70)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

# ---------- map plate ----------
front = json.load(open(os.path.join(ROOT, "tools/data/dhauladhar-front.json")))
relief = Image.open(os.path.join(ROOT, "prototypes/v4/img/india/dhauladhar-relief.webp")).convert("RGB")
# relief is 2000x800 for the 1000x400 plate: plate coords x2
W, H = 1200, 560
cx0, cy0 = 300, 110          # crop origin in relief pixels (plate 150, 55)
plate = relief.crop((cx0, cy0, cx0 + W, cy0 + H))
# dim and tint towards the site background so type sits on it
dim = Image.new("RGB", (W, H), BG)
plate = Image.blend(plate, dim, 0.42)
# soft vignette at the edges so the plate fades into the card
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle((70, 70, W - 70, H - 70), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(70))
plate = Image.composite(plate, dim, vig)
d = ImageDraw.Draw(plate, "RGBA")

def P(x, y):  # plate coords (1000x400) to crop pixels
    return (x * 2 - cx0, y * 2 - cy0)

# the 2,300 m front, west and east of Billing, as a dashed line
def dashed(pts, col, w=3, dash=14, gap=9):
    import math
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        if L == 0: continue
        t = 0.0
        while t < L:
            s = t / L; e = min(L, t + dash) / L
            d.line((x1 + (x2 - x1) * s, y1 + (y2 - y1) * s, x1 + (x2 - x1) * e, y1 + (y2 - y1) * e), fill=col, width=w)
            t += dash + gap
for key in ("west", "east"):
    pts = [P(p[0], p[1]) for p in front[key]]
    dashed(pts, (255, 117, 23, 210))

mono = font("DMMono-Regular.ttf", 22); monoS = font("DMMono-Regular.ttf", 18)
def label(name, pos, anchor="lm", dx=16, dy=0, big=False):
    x, y = P(*pos)
    r = 7 if big else 5
    d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=(255, 117, 23, 60))
    d.ellipse((x - r, y - r, x + r, y + r), fill=ORANGE)
    f = mono if big else monoS
    tx, ty = x + dx, y + dy
    # a dark pad behind the text for legibility
    bb = d.textbbox((tx, ty), name, font=f, anchor=anchor)
    d.rectangle((bb[0] - 8, bb[1] - 5, bb[2] + 8, bb[3] + 5), fill=(20, 21, 25, 170))
    d.text((tx, ty), name, font=f, fill=INK, anchor=anchor)
pts = front["points"]
label("Billing launch  2,400 m", pts["Billing launch"], big=True, dy=-14)
label("Bir landing  1,400 m", pts["Bir landing"], dy=16)
label("Dharamshala", pts["Dharamshala"], anchor="rm", dx=-16)
label("Palampur", pts["Palampur"], dy=18)
# scale bar: 7.33 px per km on the plate, so 14.66 px per km here
km = 20; L = int(km * 7.33 * 2)
sx, sy = 80, H - 54
d.line((sx, sy, sx + L, sy), fill=INK, width=2)
d.line((sx, sy - 6, sx, sy + 6), fill=INK, width=2); d.line((sx + L, sy - 6, sx + L, sy + 6), fill=INK, width=2)
d.text((sx + L / 2, sy - 12), "%d km" % km, font=monoS, fill=INK, anchor="mb")
d.text((W - 80, H - 54), "THE DHAULADHAR FRONT, 2,300 m", font=monoS, fill=MUTED, anchor="rm")
plate.save(os.path.join(OUT, "india-map.jpg"), quality=86, optimize=True, progressive=True)

# ---------- terrain profile ----------
flight = json.load(open(os.path.join(ROOT, "tools/data/india-flight.json")))
prof = flight["profile_bir_north_km_m"]
PW, PH = 1200, 260
im = Image.new("RGB", (PW, PH), CARD)
d = ImageDraw.Draw(im, "RGBA")
x0, x1, y0, y1 = 70, PW - 120, 44, PH - 60
kms = [p[0] for p in prof]; els = [p[1] for p in prof]
kmax = max(kms); emin, emax = 1200, max(els) + 200
def X(k): return x0 + (x1 - x0) * k / kmax
def Y(e): return y1 - (y1 - y0) * (e - emin) / (emax - emin)
line = [(X(k), Y(e)) for k, e in prof]
# ground fill under the line
d.polygon(line + [(X(kmax), y1), (X(0), y1)], fill=(255, 117, 23, 22))
d.line(line, fill=ORANGE, width=3, joint="curve")
# height rules
for e in (1400, 2400, 3000):
    d.line((x0, Y(e), x1, Y(e)), fill=(255, 255, 255, 22), width=1)
    d.text((x1 + 8, Y(e)), "%s m" % format(e, ","), font=monoS, fill=MUTED, anchor="lm")
# marks: landing at km 0, launch at the first point above 2,390 m
launch = next(p for p in prof if p[1] >= 2390)
for (k, e), name, anc, off in ((prof[0], "Bir landing", "la", 16), (launch, "Billing launch", "md", -16)):
    x, y = X(k), Y(e)
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 117, 23, 70)); d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=INK)
    d.text((x, y + off), name, font=monoS, fill=INK, anchor=anc)
d.text((x0, PH - 18), "0 km", font=monoS, fill=MUTED, anchor="lm")
d.text((x1, PH - 18), "%d km north of the landing field" % round(kmax), font=monoS, fill=MUTED, anchor="rm")
d.text((x0, 18), "THE GROUND UNDER THE FLIGHT", font=monoS, fill=MUTED, anchor="lm")
im.save(os.path.join(OUT, "india-profile.png"), optimize=True)
print("wrote", os.listdir(OUT), "launch at km", launch)
