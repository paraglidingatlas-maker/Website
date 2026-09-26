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
