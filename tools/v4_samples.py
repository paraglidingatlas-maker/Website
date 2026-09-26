#!/usr/bin/env python3
"""
v4 sample pages (prototypes/v4/samples/, hidden: noindex, never linked from the
site, never switched live). Each one shows a v4 idea before it is rolled out.

    python3 tools/v4_samples.py            # every sample
    then: python3 tools/v2_localize.py --site v4

  three-view.html   the drawing kit: the paraglider three-view, before (the
                    raster the knowledge base uses today) and after (drawn with
                    tools/v4_draw.py), and the kit's pieces.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402
import v4_figs as F  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
OUT = os.path.join(V4, "samples")
SKIP = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/|\{|\$|%|data:)", re.I)


def deeper(html):
    """Links written for a page at the v4 root, moved one folder down."""
    fix = lambda u: u if (not u or SKIP.match(u)) else "../" + u
    html = re.sub(r'(\s(?:href|src|poster|data-src|data-loop)=")([^"]*)(")', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), html)
    html = re.sub(r'(\ssrcset=")([^"]*)(")', lambda m: m.group(1) + ", ".join(
        " ".join([fix(c.strip().split()[0])] + c.strip().split()[1:]) for c in m.group(2).split(",") if c.strip()) + m.group(3), html)
    return html


def shell(title, desc, body, css=""):
    src = open(os.path.join(V4, "terms.html"), encoding="utf-8").read()
    head = src[:src.index("</head>")]
    head = re.sub(r"<title>.*?</title>", "<title>%s (v4 sample)</title>" % title, head, flags=re.S)
    head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="%s">' % desc, head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    head = re.sub(r"<!-- site-schema -->.*?<!-- /site-schema -->", "", head, flags=re.S)
    head = re.sub(r'<meta (?:property|name)="(?:og|twitter):[^"]*"[^>]*>\s*', "", head)
    head = re.sub(r'<link rel="stylesheet" href="[^"]*policies\.css[^"]*">\s*', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://paraglidingatlas.com/">', head)
    rest = src[src.index("</head>"):]
    nav = rest[rest.index('<div class="page-wrap">'):rest.index('<header class="kit-hero')]
    foot_scripts = rest[rest.index("</div><!-- /.page-wrap -->"):]
    page = head + ("<style>%s</style>\n" % css if css else "") + '</head>\n<body data-v2="pg">\n' + nav + body + "\n" + foot_scripts
    return deeper(page)


SPEC_CSS = """
.v4s-pair{display:grid;gap:var(--sp-4);}
.v4s-fig{margin:0;}
.v4s-fig figcaption{margin-top:var(--sp-2);font-size:var(--fs-small);color:var(--gray);max-width:70ch;line-height:1.6;}
.v4s-fig figcaption b{color:var(--white);font-weight:600;}
.v4s-before img{display:block;width:100%;height:auto;}
.v4s-tag{display:inline-block;font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray-light);
  background:rgba(255,255,255,.05);padding:.3rem .6rem;margin-bottom:var(--sp-2);}
.v4s-tag.is-after{background:var(--orange);color:var(--ink);}
.dk{display:block;width:100%;height:auto;}
.dk-wide{display:block;} .dk-narrow{display:none;}
@media (max-width:700px){ .dk-wide{display:none;} .dk-narrow{display:block;} }
.v4s-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));gap:var(--sp-3);margin:var(--sp-4) 0 0;padding:0;list-style:none;}
.v4s-list li{font-size:var(--fs-body-s);color:var(--gray-light);line-height:1.6;}
.v4s-list b{display:block;color:var(--white);font-family:var(--font-display);font-size:var(--fs-h4);margin-bottom:.3rem;}
"""


def kit_specimen(narrow=False):
    """The kit's pieces on one sheet: weights, a callout, a dimension, an
    angle, hatching, a spline and an arc, a view label, a title block. The
    shapes are abstract: a specimen, not a claim about anything."""
    w, h = (390, 620) if narrow else (1200, 300)
    d = K.Drawing(w, h, "kitn" if narrow else "kit", "The drawing kit's pieces",
                  "A specimen of the drawing kit: outline, detail and hairline weights, a callout, a dimension "
                  "line, an angle, hatching, a spline and an arc, a view label and a title block.",
                  compact=narrow)
    d.frame(4 if narrow else 8)
    if narrow:
        cols = [(20, 40), (20, 190), (20, 340), (20, 470)]
    else:
        cols = [(40, 60), (330, 60), (620, 60), (900, 60)]
    # weights
    x, y = cols[0]
    for i, (k, lab) in enumerate((("outline", "Outline 2 px"), ("detail", "Detail 1 px"), ("hair", "Hairline 0.75 px"), ("centre", "Centre line"))):
        d.line((x, y + i * 28), (x + 150, y + i * 28), k)
        d.text((x + 164, y + i * 28 + 4), lab, "sub")
    # a spline shape with hatching and a callout
    x, y = cols[1]
    shape = [(x, y + 60), (x + 60, y), (x + 170, y + 20), (x + 220, y + 80), (x + 120, y + 110), (x + 30, y + 100)]
    d.spline(shape, "outline", closed=True, fill="hatch")
    d.callout((x + 140, y + 18), (x + 190, y - 22) if not narrow else (x + 250, y + 8), "Callout", sub="a leader to the part")
    # dimension and angle
    x, y = cols[2]
    d.line((x, y + 100), (x + 200, y + 100), "outline")
    d.dim((x, y + 100), (x + 200, y + 100), 34, "value")
    d.line((x, y + 100), (x + 150, y + 40), "detail")
    d.angle((x, y + 100), 70, -22, 0, "angle")
    # arc and title block
    x, y = cols[3]
    if narrow:
        d.arc((x + 90, y + 70), 80, 50, 200, 340, "outline")
        d.view((x, y + 100), "A", "View label")
    else:
        d.arc((x + 110, y + 70), 100, 60, 200, 340, "outline")
        d.view((x, y + 100), "A", "View label")
        d.title_block(x, y + 128, 262, "Title block", [("Source", "Episode, chapter"), ("Scale", "Not to scale")])
    return d.svg("dk-narrow" if narrow else "dk-wide")


def three_view_page():
    wide = F.three_view("wide").replace('class="dk ', 'class="dk dk-wide ', 1)
    narrow = F.three_view("narrow").replace('class="dk ', 'class="dk dk-narrow ', 1)
    body = """<header class="kit-hero is-sky v2-page-hero">
  <div class="kit-hero-copy">
    <span class="kit-kicker">v4 sample &middot; not on the live site</span>
    <h1>The drawing kit</h1>
    <p class="kit-intro">The paraglider three-view, before and after. One kit for every figure on the site.</p>
  </div>
</header>
<main>
<section class="kit-band">
  <div class="kit-in v4s-pair">
    <figure class="v4s-fig v4s-before">
      <span class="v4s-tag">Before</span>
      <picture><source srcset="../../assets/images/kb-flight-mechanics.webp" type="image/webp"><img src="../../assets/images/kb-flight-mechanics.jpg" alt="The knowledge base's current three-view: a raster image with reference-frame symbols" loading="lazy" width="2400" height="900"></picture>
      <figcaption><b>Now, on Flight Mechanics.</b> A picture (2,400 by 900 pixels): it blurs when enlarged, its letters are symbols from flight-dynamics papers (K, P, B, AM, x<sub>b</sub>, &theta;<sub>b</sub>) that the page never explains, and none of it can be searched.</figcaption>
    </figure>
    <figure class="v4s-fig v4s-after">
      <span class="v4s-tag is-after">After</span>
      %s
      %s
      <figcaption><b>With the kit.</b> Drawn from geometry as vector lines in the site's type, sharp at any size, a second layout for the phone. Every label is a word the page uses (profile, nose, trailing edge, A lines, B lines, brake line, speed bar, angle of attack, lift resultant); the one number is the page's own: at least 7&nbsp;cm of brake travel from hands fully up to the first tension (Tom Lolies, Episode 66, chapter 12). No scale is claimed.</figcaption>
    </figure>
  </div>
</section>
<section class="kit-band">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">The kit</span>
      <h2 class="kit-title">One look for every figure</h2>
      <p class="kit-note">tools/v4_draw.py</p>
    </div>
    %s
    %s
    <ul class="v4s-list">
      <li><b>Weights</b>A thick outline, thin detail, hairline dimensions. They stay the same width on a phone.</li>
      <li><b>Type</b>The site's own: the drawing is part of the page, not a picture of text.</li>
      <li><b>Only real numbers</b>Labels, values and dimensions come from the page or the episode it cites. Nothing drawn to look measured.</li>
      <li><b>Title block</b>What the figure shows, the episode and chapter it comes from, and "Not to scale".</li>
    </ul>
  </div>
</section>
</main>
""" % (wide, narrow, kit_specimen(False), kit_specimen(True))
    return shell("The drawing kit", "The v4 drawing kit: the paraglider three-view, before and after.", body, SPEC_CSS)


def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "three-view.html"), "w", encoding="utf-8").write(three_view_page())
    print("v4 samples: three-view.html")


if __name__ == "__main__":
    main()
