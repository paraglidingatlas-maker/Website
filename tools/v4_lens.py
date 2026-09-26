#!/usr/bin/env python3
"""
The knowledge base drawings redrawn by lens (owner, 26 Sep 2026: "all", after
samples/drawings-expert.html). Each drawing takes the approach that fits it:

  computed   physics the page states, worked out rather than sketched
             (a panel method for the brakes, the standard atmosphere for
             speed and pressure with height, areas to scale)
  painted    scenes composed as a picture: one light, one focal point,
             tonal depth, orange only on the subject
  phone      every drawing in a band gets its own phone version, stacked
             and at reading size, in place of a 720px drawing scrolled
             sideways

Nothing new is claimed: every label and number is the page's own, as in the
drawing it replaces.

This module is the registry: tools/v4_pass.py places what it lists
(kb_figure), tools/v4_kbsvg.py leaves these names alone, and main() writes
the wide versions to prototypes/v4/img/kb/ for the index and the menu.

    python3 tools/v4_lens.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "kb")


def registry():
    """name -> (wide drawing, phone drawing or None), both v4_draw.Drawing, built on demand."""
    import v4_expert as X
    import v4_darkside as DS
    reg = {
        "kb-flight-mechanics-brakes": (lambda: X.brakes_drawing(), lambda: X.brakes_drawing(True)),
        "kb-meteorology": (lambda: X.meteo_drawing(), None),
        "kb-navigators": (lambda: X.map_drawing(), None),
    }
    for name, fn in DS.drawings_fns().items():
        reg[name] = (fn, DS.phone_fns().get(name))
    for mod in ("v4_computed", "v4_painted", "v4_phone"):
        try:
            m = __import__(mod)
        except ImportError:
            continue
        reg.update(m.registry())
    return reg


# a figure's key, where the page's caption describes the drawing it replaces: {page: [(old, new)]}
LEGENDS = {
    "knowledge-base/flight-mechanics.html": [
        ("Orange: where the lift acts. Grey: drag.",
         "Orange: the suction along the upper surface and where the lift acts. Grey: the airflow. Computed with a "
         "2D panel method at an illustrative 6°; it does not model drag."),
    ],
}


def legends(rel, src):
    for old, new in LEGENDS.get(rel, ()):
        src = src.replace(old, new)
    return src


_CACHE = {}


def names():
    if "names" not in _CACHE:
        _CACHE["names"] = tuple(registry())
    return _CACHE["names"]


def build(name):
    """(wide svg, phone svg or None) for one name; each built once per run."""
    if name not in _CACHE:
        wide, phone = registry()[name]
        _CACHE[name] = (wide().svg(), phone().svg() if phone else None)
    return _CACHE[name]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in names():
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(build(name)[0] + "\n")
    print("v4 lens: %d drawings written" % len(names()))


if __name__ == "__main__":
    main()
