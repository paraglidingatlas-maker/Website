#!/usr/bin/env python3
"""Write the homepage guest card strip into index.html.

WHY A GENERATOR FOR FIFTEEN CARDS
They were written by hand, which is how the strip ended up with ten of fifteen
showing a placeholder and nobody noticing. Generated, the strip is a list of
episodes and the markup follows.

THE TYPE IS FITTED WITH REAL FONT METRICS, NOT GUESSED
Both text slots must not overflow, and a guest's name is whatever length it is:
"Will Gadd" is 5.47 em wide in Poppins 700 and "Ivelin Kalushkov" is 9.48. At one
size the second overflows its box, which it did.

So each card carries its own font size, worked out here from the actual advance
widths in the woff2:
  cap height of Poppins 700 is 0.7050 em
  the artwork sets the hook at 4.50% and the name at 5.45% of the frame HEIGHT
  the frame is 1.414 times as tall as it is wide
  so the design sizes are 9.03% and 10.93% of the card WIDTH
Those are ceilings. If a string is too wide for its box at that size, the size
comes down until it fits. Nothing is clipped and nothing is guessed.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "assets", "fonts", "poppins-latin-700-normal.woff2")

CAP = 0.7050          # cap height of Poppins 700, from the file
HOOK_CAP = 0.0450     # of frame height, measured from the supplied artwork
NAME_CAP = 0.0545
RATIO = 2000 / 1414   # the frame is this many times as tall as it is wide
HOOK_BOX = 0.82       # share of card width the hook may use
NAME_BOX = 0.88
HOOK_LINES = 2        # the hook never runs to a third line
WRAP_LOSS = 0.90      # words do not fill a line exactly


def widths():
    """Advance width of every character, in em, from the actual font."""
    from fontTools.ttLib import TTFont
    f = TTFont(FONT)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    return {chr(c): hmtx[g][0] / upm for c, g in cmap.items() if chr(c).isprintable()}, upm


W = None


def em_width(s):
    return sum(W.get(c, 0.6) for c in s.upper())


def fit(text, box, max_size, lines=1):
    """Largest font size, as a percent of card width, that fits."""
    total = em_width(text)
    if lines > 1:
        # the whole string across N lines, and no single word wider than one line
        by_total = box * lines * WRAP_LOSS / total
        longest = max((em_width(w) for w in text.split()), default=total)
        by_word = box / longest
        size = min(by_total, by_word)
    else:
        size = box / total
    return round(min(max_size, size * 100), 2)


def main():
    global W
    W, _ = widths()
    hook_max = HOOK_CAP / CAP * RATIO * 100
    name_max = NAME_CAP / CAP * RATIO * 100

    cards = json.load(open(os.path.join(ROOT, "homepage-cards.json"), encoding="utf-8"))
    out = []
    for c in cards:
        hf = fit(c["hook"], HOOK_BOX, hook_max, HOOK_LINES)
        nf = fit(c["guest"], NAME_BOX, name_max, 1)
        img = c.get("img") or "photo-needed"
        out.append(
            '\n      <a class="ep-card" href="episodes/%s.html" style="--hf:%scqw;--nf:%scqw">'
            '\n        <span class="ep-stamp">%s<i>%s</i></span>'
            '\n        <span class="ep-art">'
            '\n          <picture><source srcset="assets/podcast/%s.webp" type="image/webp">'
            '<img src="assets/podcast/%s.jpg" alt="%s" loading="lazy" width="480" height="679"></picture>'
            '\n          <span class="ep-plate"><span class="ep-hook">%s</span>'
            '<span class="ep-name">%s</span></span>'
            '\n          <span class="ep-open"><span class="s">%s</span>'
            '<span class="n">%s</span><span class="m">%s</span>'
            '<span class="g">Open the episode &rarr;</span></span>'
            '\n        </span>'
            '\n        <span class="ep-foot">%s<s>/</s>%s<i>%s</i></span>'
            '\n      </a>'
            % (c["slug"], hf, nf,
               c["series"].upper(), c["epno"].upper(),
               img, img, c["guest"],
               c["hook"], c["guest"],
               c["series"].upper(), c["guest"], c["chapters"],
               c["dur"], c["chapters"], EXPAND))
    strip = "".join(out)

    path = os.path.join(ROOT, "index.html")
    html = open(path, encoding="utf-8").read()
    pat = re.compile(r"(<!-- guest-cards:start -->).*?(<!-- guest-cards:end -->)", re.S)
    if not pat.search(html):
        raise SystemExit("guest-cards markers not found in index.html")
    # Test the MARKERS, not whether the text changed. The first version raised
    # "markers not found" on the second run, when the output was already correct,
    # because an idempotent generator produces an identical file.
    new = pat.sub(lambda m: m.group(1) + strip + "\n      " + m.group(2), html)
    if new != html:
        open(path, "w", encoding="utf-8").write(new)

    tight = [c["guest"] for c in cards
             if fit(c["guest"], NAME_BOX, name_max, 1) < name_max - 0.01]
    print("wrote %d guest cards" % len(cards))
    print("  names scaled down to fit: %s" % (tight or "none"))
    return 0


EXPAND = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<path d="M9 4H4v5"/><path d="M15 20h5v-5"/><path d="M4 4l6 6"/>'
          '<path d="M20 20l-6-6"/></svg>')

if __name__ == "__main__":
    raise SystemExit(main())
