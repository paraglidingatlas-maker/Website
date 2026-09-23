#!/usr/bin/env python3
"""Build the India packing checklist PDF from the kit on the India page.

The page is the source: groups, items, notes and the Essential flags are read
from its kit markup, so the PDF cannot drift from what the page says. Colours
come from the tokens in styles.css; fonts are the site's own woff2 files,
unpacked to TTF for ReportLab. The checkboxes are real form fields, so the PDF
can be ticked in any reader and saved, or printed.

Run: python3 tools/build_india_packing_pdf.py [page]
     (default page: prototypes/india.html; destinations/india.html once live)

Needs: pip install reportlab fonttools brotli
"""
import html
import os
import re
import sys
import tempfile

from fontTools.ttLib import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = sys.argv[1] if len(sys.argv) > 1 else "prototypes/india.html"
OUT = os.path.join(ROOT, "assets/destinations/india/india-packing-checklist.pdf")
URL = "paraglidingatlas.com/destinations/india"


def tokens():
    css = open(os.path.join(ROOT, "styles.css"), encoding="utf-8").read()
    root = css[css.index(":root"):css.index("}", css.index(":root"))]
    t = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", root))
    need = ("bg", "card", "orange", "white", "gray", "gray-light", "rule")
    missing = [k for k in need if k not in t]
    if missing:
        raise SystemExit("styles.css has no hex value for %s" % missing)
    return {k: HexColor(t[k]) for k in need}


def font(name, woff2):
    tmp = os.path.join(tempfile.gettempdir(), name + ".ttf")
    f = TTFont(os.path.join(ROOT, "assets/fonts", woff2))
    f.flavor = None
    f.save(tmp)
    pdfmetrics.registerFont(RLFont(name, tmp))


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def read_page():
    h = open(os.path.join(ROOT, PAGE), encoding="utf-8").read()
    sec = h[h.index('id="packing"'):]
    sec = sec[:sec.index("</section>")]
    intro = text(re.search(r'<div class="dst-head">.*?<p>(.*?)</p>', sec, re.S).group(1))
    gates = [(text(b), text(p)) for b, p in
             re.findall(r'<div><b>(.*?)</b><p>(.*?)</p></div>', sec.split('class="kkit-gate"')[1].split("</div>\n\n")[0])]
    groups = []
    for g in re.finditer(r'<div class="kkit-group".*?<span class="kkit-gname">(.*?)</span>(.*?)</ul>', sec, re.S):
        items = []
        for m in re.finditer(r'<button type="button" class="kkit-item( is-ess)?".*?<span class="kkit-txt">(.*?)</span>\s*</button>',
                             g.group(2), re.S):
            inner = m.group(2)
            note = re.search(r'<span class="kkit-note">(.*?)</span>', inner)
            items.append((text(re.sub(r"<span.*", "", inner, flags=re.S)),
                          text(note.group(1)) if note else "", bool(m.group(1))))
        groups.append((text(g.group(1)), items))
    return intro, gates, groups


def build():
    c_ = tokens()
    font("DMSans", "dm-sans-latin-400-normal.woff2")
    font("DMSans-Medium", "dm-sans-latin-500-normal.woff2")
    font("Poppins-SemiBold", "poppins-latin-600-normal.woff2")
    intro, gates, groups = read_page()
    total = sum(len(i) for _, i in groups)

    W, H = 595.2756, 841.8898
    M = 45.35
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("India Packing Checklist | Paragliding Atlas")
    c.setAuthor("Paragliding Atlas")
    c.setSubject("Packing checklist for the Bir Billing paragliding tour")
    c.setFillColor(c_["bg"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    logo = os.path.join(ROOT, "assets/logo/atlas-logo-white.png")
    c.drawImage(logo, M, H - 70, width=96, height=20, mask="auto")

    c.setFillColor(c_["white"])
    c.setFont("Poppins-SemiBold", 20)
    c.drawString(M, H - 100, "India packing checklist")
    c.setFont("DMSans", 8.6)
    c.setFillColor(c_["gray-light"])
    y = H - 118
    for line in simpleSplit(intro + " Tick these boxes in any PDF reader and save, or print it and use a pen.",
                            "DMSans", 8.6, W - 2 * M):
        c.drawString(M, y, line)
        y -= 11.5

    # three gate cards
    gw = (W - 2 * M - 2 * 12) / 3
    gh = 62
    gy = y - 8 - gh
    for i, (label, body) in enumerate(gates):
        x = M + i * (gw + 12)
        c.setFillColor(c_["card"])
        c.setStrokeColor(c_["rule"])
        c.rect(x, gy, gw, gh, stroke=1, fill=1)
        c.setFillColor(c_["orange"])
        c.setFont("DMSans-Medium", 6.2)
        c.drawString(x + 8, gy + gh - 13, label.upper())
        c.setFillColor(c_["gray-light"])
        c.setFont("DMSans", 7.4)
        ty = gy + gh - 25
        for line in simpleSplit(body, "DMSans", 7.4, gw - 16):
            c.drawString(x + 8, ty, line)
            ty -= 9.4

    # two columns, groups kept whole, filled left then right
    col_w = (W - 2 * M - 24) / 2
    top = gy - 34
    def height(items):
        h = 33
        for label, note, ess in items:
            h += 14.7 + (8.6 * len(simpleSplit(note, "DMSans", 6.9, col_w - 15)) if note else 0)
        return h

    # each group goes to whichever column is shorter so far, so the two
    # columns end level rather than one running long
    cols, used = [[], []], [0.0, 0.0]
    for g in groups:
        k = 0 if used[0] <= used[1] else 1
        cols[k].append(g)
        used[k] += height(g[1])
    form = c.acroForm
    n = 0
    for ci, col in enumerate(cols):
        x = M + ci * (col_w + 24)
        y = top
        for name, items in col:
            c.setFillColor(c_["white"])
            c.setFont("Poppins-SemiBold", 11)
            c.drawString(x, y, name)
            c.setFillColor(c_["gray"])
            c.setFont("DMSans", 7.5)
            c.drawString(x + pdfmetrics.stringWidth(name, "Poppins-SemiBold", 11) + 5, y, str(len(items)))
            c.setStrokeColor(c_["rule"])
            c.line(x, y - 5, x + col_w, y - 5)
            y -= 19
            for label, note, ess in items:
                form.checkbox(name="item%d" % n, tooltip=label, x=x, y=y - 2, size=9,
                              buttonStyle="check", borderColor=c_["gray"], fillColor=c_["bg"],
                              textColor=c_["orange"], borderWidth=0.8, forceBorder=True)
                n += 1
                c.setFillColor(c_["white"])
                c.setFont("DMSans-Medium", 8.4)
                c.drawString(x + 15, y, label)
                if ess:
                    lx = x + 15 + pdfmetrics.stringWidth(label, "DMSans-Medium", 8.4) + 6
                    c.setStrokeColor(c_["orange"])
                    c.setFillColor(c_["orange"])
                    c.roundRect(lx, y - 1.6, 37, 8.6, 1.5, stroke=1, fill=0)
                    c.setFont("DMSans-Medium", 5.4)
                    c.drawString(lx + 3.4, y + 0.6, "ESSENTIAL")
                y -= 10.5
                if note:
                    c.setFillColor(c_["gray"])
                    c.setFont("DMSans", 6.9)
                    for line in simpleSplit(note, "DMSans", 6.9, col_w - 15):
                        c.drawString(x + 15, y, line)
                        y -= 8.6
                y -= 4.2
            y -= 14

    c.setFillColor(c_["gray"])
    c.setFont("DMSans", 6.5)
    c.drawString(M, 28, URL)
    c.drawRightString(W - M, 28, "%d items" % total)
    c.save()
    print("wrote %s: %d items, %d boxes" % (os.path.relpath(OUT, ROOT), total, n))


if __name__ == "__main__":
    build()
