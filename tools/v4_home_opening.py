#!/usr/bin/env python3
"""
The home page's opening (owner, 24 Oct 2026: "do it", then "put it on main V4 hero image"): design F2, the season
route over a giant place name with the wing cut out in front of it, and E's move through the cloud between places.

Its source is the sample the owner reviews, prototypes/v4/samples/opening/index.html. This copies that sample into the
v4 home page in place of the old hero (the footage, the ridge drawing and the headline):

  - its photo layers into prototypes/v4/img/opening/ (only the files that differ are written);
  - its hero markup between marks in prototypes/v4/index.html, the page links made the home page's own;
  - its styles fenced to #held (every rule scoped, its classes on <html> renamed op-*, its keyframes op-*), so the
    site's styles and the opening's leave each other alone; the sample's own header, body and font rules stay out;
  - its script, the photo paths under img/opening/.

Run it by hand after a change to the sample (like tools/v4_opening.py); the build keeps what it wrote. Idempotent.

    python3 tools/v4_home_opening.py
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "samples", "opening")
PAGE = os.path.join(V4, "index.html")
IMG = os.path.join(V4, "img", "opening")
MARK = ("<!-- v4-home-opening: tools/v4_home_opening.py -->", "<!-- /v4-home-opening -->")
HEAD = ("<!-- v4-home-opening-head -->", "<!-- /v4-home-opening-head -->")
TAIL = ("<!-- v4-home-opening-script -->", "<!-- /v4-home-opening-script -->")
MEDIA = (".webp", ".jpg", ".png", ".mp4", ".webm")
HTML_CLASSES = ("js", "arrive", "fine", "gl", "gl-on")        # the classes the opening puts on <html>
KEYFRAMES = ("settle", "glide-away", "glide", "draw", "rise", "bump")
SKIP = re.compile(r"^(\*|html|body|a|img|button|:root|\.nav\b|\.nav-|\.cta\b|\.menu\b|\.band\b|\.figs\b|\.logo\b)")


def split_rules(css):
    """Top-level blocks: (prelude, body) for rules, ('@...', inner) for at-rules with a block."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        pre = css[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        out.append((pre, css[j + 1:k - 1]))
        i = k
    return out


def scope_selector(sel):
    sel = sel.strip()
    if SKIP.match(sel):
        return None
    # a qualifier on <html> first: .js, .arrive, .fine, .gl, .gl-on, html:not(.js)
    m = re.match(r"^(html)?((?::not\(\.(?:%s)\)|\.(?:%s))+)(?=[\s>+~]|$)" % ("|".join(HTML_CLASSES), "|".join(HTML_CLASSES)), sel)
    if m and m.group(2):
        q = re.sub(r"\.(%s)\b" % "|".join(re.escape(c) for c in HTML_CLASSES), r".op-\1", m.group(2))
        rest = sel[m.end():].strip()
        if rest.startswith(".held") or rest.startswith(".auto"):
            return "html" + q + " " + scope_selector(rest)
        return "html" + q + " #held" + (" " + rest if rest else "")
    if sel.startswith(".held"):
        return "#held" + sel[len(".held"):]
    if sel.startswith(".auto"):                      # the autoplay class sits on the opening itself
        return "#held" + sel
    return "#held " + sel


def scope_css(css):
    out = []
    for pre, body in split_rules(css):
        if pre.startswith("@keyframes"):
            name = pre.split()[1]
            out.append("@keyframes op-%s{%s}" % (name, body.strip()))
        elif pre.startswith("@media") or pre.startswith("@supports"):
            inner = scope_css(body)
            if inner:
                out.append("%s{%s}" % (pre, inner))
        else:
            sels = [scope_selector(s) for s in pre.split(",")]
            sels = [s for s in sels if s]
            if sels:
                body = re.sub(r"\s*\n\s*", "", body.strip())
                for k in KEYFRAMES:
                    body = re.sub(r"(animation(?:-name)?:[^;]*?)\b%s\b" % re.escape(k), r"\1op-%s" % k, body)
                out.append("%s{%s}" % (",".join(sels), body))
    return "".join(out)


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def rename_html_classes(js):
    return re.sub(r"(classList\.(?:add|remove|toggle|contains)\(')(%s)(')" % "|".join(re.escape(c) for c in HTML_CLASSES),
                  r"\1op-\2\3", js)


def main():
    src = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()
    head_js = re.search(r"<script>\n(/\* One arrival.*?)</script>", src, re.S).group(1)
    css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)
    root = re.search(r":root\{(.*?)\}", css, re.S).group(1)
    held = re.search(r'(<header class="held" id="held">.*?</header>)', src, re.S).group(1)
    main_js = re.search(r"<script>\n(\(function \(\) \{.*?)</script>\n</body>", src, re.S).group(1)

    # the photo layers
    os.makedirs(IMG, exist_ok=True)
    names = sorted(f for f in os.listdir(SRC) if f.endswith(MEDIA) and f != "atlas-logo-white.png")
    for f in names:
        a, b = os.path.join(SRC, f), os.path.join(IMG, f)
        if not os.path.exists(b) or open(a, "rb").read() != open(b, "rb").read():
            shutil.copyfile(a, b)
    for f in os.listdir(IMG):
        if f not in names:
            os.remove(os.path.join(IMG, f))

    # the markup: the home page's own links and photo paths
    held = held.replace('href="../../', 'href="')
    held = re.sub(r'((?:src|srcset)=")([\w.-]+\.(?:webp|jpg|png))"', r'\1img/opening/\2"', held)
    held = held.replace('<a href="#listen" class="btn-lines">', '<a href="#listen" class="btn-lines" data-hover>')
    # the site styles every .kicker outside its heroes in grey; the opening's stays its own
    held = held.replace('class="kicker"', 'class="op-kicker"')

    # the styles, fenced to the opening; its tokens on #held so the site's own stay as they are
    tokens = "#held{%s}" % re.sub(r"\s*\n\s*", "", root.strip())
    base = ("#held,#held *{box-sizing:border-box}#held{color:var(--white);font-family:var(--font-body);-webkit-font-smoothing:antialiased}"
            "#held a{color:inherit;text-decoration:none}#held img{display:block;max-width:none}#held button{font:inherit;color:inherit}"
            "#held h1,#held h2,#held p,#held dl,#held dd,#held fieldset{margin:0}#held fieldset{border:0;padding:0;min-width:0}"
            # the site's solid button is an orange box slanted 10 degrees; the opening's slants only its colour, 8 degrees
            "#held .btn-solid,#held .btn-solid:hover{transform:none;background:none}"
            # the site's header lies over the photograph, as in the sample (it pins as the page scrolls, as everywhere)
            ".page-wrap:has(>#v4-main>#held)>nav:not(.v2-nav-pinned){position:absolute;top:0;left:0;right:0;z-index:40}")
    scoped = tokens + base + scope_css(strip_comments(css)).replace("#held .kicker", "#held .op-kicker")

    # the script: photo paths under img/opening/, its classes on <html> renamed
    js = rename_html_classes(main_js)
    if "(function () {\n  'use strict';" not in js:
        raise SystemExit("v4_home_opening: the script's start changed")
    # the folder from the page's own photo, whose src the switch-over rewrites (live: assets/v4/img/opening/);
    # a fixed 'img/opening/' 404'd on the live home (27 Oct)
    js = js.replace("'use strict';", "'use strict';\n  var OP = (function () { var i = document.querySelector('#held img[src*=\"opening/\"]');"
                    " return i ? i.getAttribute('src').replace(/[^\\/]*$/, '') : 'img/opening/'; })();", 1)
    for a, b in (("i.src = src;", "i.src = OP + src;"), ("so.src = s;", "so.src = OP + s;")):
        if js.count(a) != 1:
            raise SystemExit("v4_home_opening: the script's loader changed (%r)" % a)
        js = js.replace(a, b)
    js = js.replace("'f-arrived'", "'v4-op-arrived'")
    # the shader's own grain goes (owner, 28 Oct 2026, the grain rework: no grain on the home opening; v2.css GRAIN
    # keeps it only in the reading light behind long text)
    if ".045;'" not in js:
        raise SystemExit("v4_home_opening: the shader grain line moved")
    js = js.replace("-.5)*.045;'", "-.5)*0.;'", 1)
    head = rename_html_classes(head_js).replace("'f-arrived'", "'v4-op-arrived'")

    page = open(PAGE, encoding="utf-8").read()
    block = MARK[0] + "\n" + held + "\n" + MARK[1]
    if MARK[0] in page:
        page = re.sub(re.escape(MARK[0]) + r".*?" + re.escape(MARK[1]), lambda m: block, page, flags=re.S)
    else:
        m = re.search(r'(<div class="flightline" aria-hidden="true"><i></i></div>\n)?<header class="kit-hero v2-home-hero">.*?</header>', page, re.S)
        if not m:
            raise SystemExit("v4_home_opening: the home page's hero is not where it was")
        page = page[:m.start()] + block + page[m.end():]
    headblock = (HEAD[0] + '<link rel="preload" as="image" href="img/opening/kenya-9492-ground.webp" type="image/webp">'
                 "<script>" + head + "</script><style>" + scoped + "</style>" + HEAD[1])
    if HEAD[0] in page:
        page = re.sub(re.escape(HEAD[0]) + r".*?" + re.escape(HEAD[1]), lambda m: headblock, page, flags=re.S)
    else:
        page = page.replace("</head>", headblock + "\n</head>", 1)
    tail = TAIL[0] + "<script>\n" + js + "</script>" + TAIL[1]
    if TAIL[0] in page:
        page = re.sub(re.escape(TAIL[0]) + r".*?" + re.escape(TAIL[1]), lambda m: tail, page, flags=re.S)
    else:
        page = page.replace("</body>", tail + "\n</body>", 1)
    open(PAGE, "w", encoding="utf-8").write(page)
    print("v4 home opening: %d photo layers in img/opening/, the opening in index.html" % len(names))


if __name__ == "__main__":
    main()
