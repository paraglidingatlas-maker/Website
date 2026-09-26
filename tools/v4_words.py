#!/usr/bin/env python3
"""Words on a page: in the body (as the checker counts them), and on first
read (outside any <details> body, outside hidden and aria-hidden parts).

    python3 tools/v4_words.py prototypes/v4/destinations/india.html [...]
"""
import html
import re
import sys


def text(fr):
    fr = re.sub(r"<(script|style|noscript|svg)\b.*?</\1>", " ", fr, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", fr)).split()


def body(src):
    b = src[src.find("<body"):]
    b = re.sub(r"<nav\b.*?</nav>", " ", b, flags=re.S)
    return re.sub(r"<footer\b.*?</footer>", " ", b, flags=re.S)


def first_read(src):
    b = body(src)
    # drop details bodies (keep summaries), innermost first
    while True:
        b2 = re.sub(r"<details\b[^>]*>\s*(<summary\b.*?</summary>)((?:(?!<details\b).)*?)</details>",
                    lambda m: m.group(1), b, flags=re.S)
        if b2 == b:
            break
        b = b2
    b = re.sub(r'<(\w+)\b[^>]*\bhidden\b[^>]*>.*?</\1>', " ", b, flags=re.S)
    return b


if __name__ == "__main__":
    for f in sys.argv[1:]:
        s = open(f, encoding="utf-8").read()
        print("%-50s body %5d  first read %5d" % (f, len(text(body(s))), len(text(first_read(s)))))


def browser(rels, site="v4", width=1440):
    """First-read words as the browser renders them: the text of the page
    (without nav and footer) with every <details> closed."""
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page(viewport={"width": width, "height": 900})
        for r in rels:
            pg.goto("http://127.0.0.1:8765/" + (r if r.startswith("prototypes/") or "/" in r and site == "live" else "prototypes/%s/%s" % (site, r)), wait_until="load")
            out[r] = pg.evaluate("""() => {
              document.querySelectorAll('details').forEach(d => d.open = false);
              const c = document.body.cloneNode(true);
              c.querySelectorAll('nav, footer, script, style, [aria-hidden="true"], .dst-mobar').forEach(e => e.remove());
              document.body.appendChild(c); c.style.position='absolute'; c.style.left='-99999px';
              const t = c.innerText; c.remove();
              return t.split(/\\s+/).filter(Boolean).length; }""")
        b.close()
    return out
