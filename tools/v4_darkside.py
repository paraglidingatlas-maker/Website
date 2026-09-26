#!/usr/bin/env python3
"""
The Dark Side's three drawings, redrawn on the owner's word (26 Sep 2026):
"remove these three and choose another episode instead". The page opening
(was a competition task), the governance drawing (was Julien Garcia's four
boxes, Ep. 54) and the rescue drawing (was Nick Neynens' downwash, Ep. 68)
give way to three drawn from other conversations in the series. Every label
is the page's own wording about that episode; nothing is measured, so
nothing is drawn to scale.

  kb-the-dark-side          the opening: Bill Belcourt's two events a week
                            apart (Ep. 59, chapter 11)
  kb-the-dark-side-section  governance: Bill Hughes & Goran Dimiskovski on
                            money (Ep. 60, chapter 5)
  kb-the-dark-side-brazil   What pilots say went wrong in Brazil: Tilen
                            Ceglar & Stan Radzikowski's timeline (Ep. 56,
                            chapter 3), in place of the downwash drawing

tools/v4_pass.py places them (FIGS, BRAZIL_FIG); tools/v4_kbsvg.py leaves
these names alone.

    python3 tools/v4_darkside.py      # writes prototypes/v4/img/kb/*.svg too
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_draw as K  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "kb")
NAMES = ("kb-the-dark-side", "kb-the-dark-side-section", "kb-the-dark-side-brazil")
GONE = ("kb-the-dark-side-downwash",)          # removed from the page


def wing(d, c, w=46, lift=16):
    """A small canopy seen from the front, with its pilot."""
    x, y = c
    d.spline([(x - w / 2, y), (x - w / 4, y - lift), (x + w / 4, y - lift), (x + w / 2, y)], "outline")
    d.line((x - w / 2 + 3, y + 1), (x, y + 30), "hair")
    d.line((x + w / 2 - 3, y + 1), (x, y + 30), "hair")
    d.circle((x, y + 34), 4, "detail")


def opening():
    """Bill Belcourt: two events a week apart."""
    d = K.Drawing(1200, 450, "ds-open",
                  "Two events a week apart, after Bill Belcourt",
                  "At one event the organisers made many of the calls for the field, and there was a serious accident "
                  "and several close calls. At a hike-and-fly race with weather briefings and no launch-condition rules, "
                  "pilots chose for themselves, and the only incident was a reserve throw with no injury. "
                  "Bill Belcourt, Episode 59, chapter 11. Schematic.", inline_css=False)
    d.backdrop(glow=(1010, 240), glow_r=260, sheet=False)
    d.text((540, 64), "Two events a week apart", "vw")
    for i, (x0, head, sub) in enumerate(((540, "Organisers made the calls", "many of them, for the field"),
                                          (880, "Pilots chose for themselves", "weather briefings, no launch-condition rules"))):
        d.line((x0, 84), (x0 + 300, 84), "hair")
        d.text((x0, 112), head, "lab")
        d.text((x0, 130), sub, "sub")
        xs = [x0 + 30 + 60 * k for k in range(5)]
        if i == 0:
            # one box above, a line down to every wing: the calls come from the top
            d.path("M%d,158 h180 v30 h-180 Z" % (x0 + 60), "detail", fill="card")
            d.text((x0 + 150, 178), "organisers", "sub", "middle")
            for x in xs:
                d.poly([(x0 + 150, 188), (x, 216)], "hair")
        else:
            # each pilot's own arrow: every one decides
            for k, x in enumerate(xs):
                dx = (-14, 10, -4, 16, -10)[k]
                d.arrow((x, 212), (x + dx, 176), "accent", 8)
        for x in xs:
            wing(d, (x, 244))
        d.line((x0, 318), (x0 + 300, 318), "hair")
    d.text((540, 346), "A serious accident", "tv")
    d.text((540, 364), "and several close calls", "tv")
    d.text((880, 346), "The only incident: a reserve throw,", "tv")
    d.text((880, 364), "no injury", "val")
    d.text((1180, 420), "Bill Belcourt, Ep. 59, ch. 11 · schematic", "tb", "end")
    return d


def money():
    """Bill Hughes & Goran Dimiskovski: the underlying problem is money."""
    d = K.Drawing(1200, 500, "ds-money",
                  "The underlying problem is money, after Bill Hughes and Goran Dimiskovski",
                  "People hold several roles because the sport is run on amateur budgets; paid staff, broadcasting and "
                  "sponsors would change that. Bill Hughes and Goran Dimiskovski, Episode 60, chapter 5. Schematic.",
                  inline_css=False)
    d.backdrop(glow=(900, 250), glow_r=260, sheet=False)
    d.text((640, 96), "The underlying problem is money", "vw")
    # one person, several roles
    x, y = 720, 262
    d.circle((x, y - 44), 15, "outline")
    d.path("M%d,%d c0,-30 60,-30 60,0 v34 h-60 Z" % (x - 30, y), "outline", fill="card")
    for k in range(3):
        d.path("M%d,%d h58 v18 h-58 Z" % (x + 44, y - 40 + 26 * k), "detail", fill="card")
    d.text((x - 36, y + 74), "Several roles", "lab")
    d.text((x - 36, y + 92), "the sport is run on amateur budgets", "sub")
    # would change that
    d.arrow((850, 250), (930, 250), "accent", 10)
    for k, name in enumerate(("paid staff", "broadcasting", "sponsors")):
        yy = 186 + 52 * k
        d.path("M960,%d h170 v34 h-170 Z" % yy, "detail", fill="card")
        d.text((980, yy + 22), name, "tv")
    d.text((960, 364), "would change that", "val")
    d.text((1180, 470), "Bill Hughes & Goran Dimiskovski, Ep. 60, ch. 5 · schematic", "tb", "end")
    return d


def brazil():
    """Tilen Ceglar & Stan Radzikowski: the goal field at the championship in Brazil."""
    d = K.Drawing(1200, 340, "ds-brazil",
                  "The championship in Brazil as two pilots tell it",
                  "The event moved to Castelo five months before it started. A new goal was set the evening before the "
                  "task and only checked by the organisers the next morning. Normally, official landings are proven over "
                  "two or three earlier events. Tilen Ceglar and Stan Radzikowski, Episode 56, chapter 3. Their account. "
                  "Schematic, not to scale.", inline_css=False)
    d.backdrop(glow=(980, 130), glow_r=220, sheet=False)
    d.text((80, 44), "This championship", "vw")
    y = 130
    d.line((80, y), (360, y), "detail")
    for bx in (372, 384):                                # a break: months pass here
        d.line((bx - 5, y + 9), (bx + 5, y - 9), "detail")
    d.line((396, y), (1100, y), "detail")
    d.head((1116, y), (1, 0), 10)
    d.dot((160, y), 4, False)
    d.text((160, y - 40), "The venue moved to Castelo", "lab", "middle")
    d.text((160, y - 22), "five months before it started", "sub", "middle")
    d.dot((800, y), 4, False)
    d.text((800, y - 40), "A new goal set", "lab", "middle")
    d.text((800, y - 22), "the evening before", "sub", "middle")
    d.dot((980, y), 5, True)
    d.text((980, y - 40), "Checked by the organisers", "lab", "middle")
    d.text((980, y - 22), "the next morning", "val", "middle")
    d.text((80, 234), "Normally", "vw")
    y2 = 280
    d.line((80, y2), (620, y2), "hair")
    for k, x in enumerate((180, 300, 420)):
        d.dot((x, y2), 3.2, False)
    d.text((300, y2 + 30), "two or three earlier events", "sub", "middle")
    d.arrow((440, y2), (590, y2), "accent", 9)
    d.text((604, y2 + 5), "official landings proven", "tv")
    d.text((1120, 320), "Tilen Ceglar & Stan Radzikowski, Ep. 56, ch. 3 · their account · not to scale", "tb", "end")
    return d


def brazil_phone():
    """The same timeline, running down the screen at reading size."""
    d = K.Drawing(360, 520, "ds-brazil-p",
                  "The championship in Brazil as two pilots tell it",
                  "The event moved to Castelo five months before it started. A new goal was set the evening before the "
                  "task and only checked by the organisers the next morning. Normally, official landings are proven over "
                  "two or three earlier events. Tilen Ceglar and Stan Radzikowski, Episode 56, chapter 3. Their account. "
                  "Schematic, not to scale.", inline_css=False)
    d.text((16, 26), "This championship", "vw")
    x = 34
    d.line((x, 50), (x, 104), "detail")
    for by in (114, 124):                                # a break: months pass here
        d.line((x - 8, by + 4), (x + 8, by - 4), "detail")
    d.line((x, 134), (x, 300), "detail")
    d.head((x, 314), (0, 1), 10)
    d.dot((x, 70), 4, False)
    d.text((x + 22, 66), "The venue moved to Castelo", "lab")
    d.text((x + 22, 84), "five months before it started", "sub")
    d.dot((x, 186), 4, False)
    d.text((x + 22, 182), "A new goal set", "lab")
    d.text((x + 22, 200), "the evening before", "sub")
    d.dot((x, 262), 5, True)
    d.text((x + 22, 258), "Checked by the organisers", "lab")
    d.text((x + 22, 276), "the next morning", "val")
    d.text((16, 366), "Normally", "vw")
    d.line((x, 390), (x, 470), "hair")
    for y in (398, 418, 438):
        d.dot((x, y), 3.2, False)
    d.text((x + 22, 422), "two or three earlier events", "sub")
    d.arrow((x, 446), (x, 486), "accent", 9)
    d.text((x + 22, 490), "official landings proven", "tv")
    d.text((344, 514), "Ep. 56, ch. 3 · their account · not to scale", "tb", "end")
    return d


def drawings_fns():
    return {"kb-the-dark-side": opening, "kb-the-dark-side-section": money, "kb-the-dark-side-brazil": brazil}


def phone_fns():
    return {"kb-the-dark-side-brazil": brazil_phone}


def drawings():
    return {k: fn() for k, fn in drawings_fns().items()}


# the Brazil drawing's words, placed under it on the page (the page's own sentences, shortened)
BRAZIL_CAPS = ('<figcaption class="bd-caps c2"><div><span>At Castelo</span>The event moved five months before it started; '
               'a new goal was set the evening before and only checked by the organisers the next morning.</div>'
               '<div><span>Normally</span>Official landings are proven over two or three earlier events.</div>'
               '<p class="bd-src">After Tilen Ceglar and Stan Radzikowski, '
               '<a href="../episodes/insights-from-the-gaggle-with-tilen-ceglar-stan.html#c3">Episode 56, chapter 3</a>. '
               'Their account, not an official finding. Schematic, not to scale.</p></figcaption>')


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, d in drawings().items():
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(d.svg() + "\n")
    for name in GONE:
        fp = os.path.join(OUT, name + ".svg")
        if os.path.exists(fp):
            os.remove(fp)
    print("v4 dark side: %s written, %s removed" % (", ".join(NAMES), ", ".join(GONE)))


if __name__ == "__main__":
    main()
