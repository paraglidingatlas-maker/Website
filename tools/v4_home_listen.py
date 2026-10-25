#!/usr/bin/env python3
"""
The home page's podcast section (owner, 25 Oct 2026: "ok" to building the preview in): option B, Turnpoint's "Hear
Where We Fly", refined, with the lit trip leading and the globe leading the stage. One section takes the place of the
old #listen and #map.

Its source is the sample the owner reviewed, prototypes/v4/samples/listen-c/index.html (a full copy of the home
page; listen-b with the "More conversations" posters; owner, 25 Oct 2026: "yes Poster strip into home"). This copies its PART 2 (the section's own <style>, the section and its scripts) into prototypes/v4/index.html
in place of the old PART 2 (#listen) and the globe (#map), between marks, the sample's paths made the home page's own
(../../../../ is the site root, ../../ is prototypes/v4/).

Run it by hand after a change to the sample (like tools/v4_home_departures.py); the build keeps what it wrote.
Idempotent. tools/v4_polish.py no longer leans the home rail's cards; the posters' own lean comes with the section.

    python3 tools/v4_home_listen.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "samples", "listen-c", "index.html")
PAGE = os.path.join(V4, "index.html")
MARK = ("<!-- v4-home-listen: tools/v4_home_listen.py -->", "<!-- /v4-home-listen -->")
PART2 = re.compile(r"<!-- =+ PART 2: [^\n]*-->\n.*?(?=<!-- =+ PART 3: JOIN =+ -->)", re.S)


def main():
    src = open(SRC, encoding="utf-8").read()
    m = PART2.search(src)
    if not m or 'id="listen"' not in m.group(0) or "HEAR WHERE WE FLY" not in m.group(0):
        raise SystemExit("v4_home_listen: the sample's section is not where it was")
    sec = m.group(0).rstrip()
    sec = sec.replace("../../../../", "\0").replace("'../../'", "''").replace("../../", "").replace("\0", "../../")

    page = open(PAGE, encoding="utf-8").read()
    block = MARK[0] + "\n" + sec + "\n" + MARK[1] + "\n\n"
    if MARK[0] in page:
        page = re.sub(re.escape(MARK[0]) + r".*?" + re.escape(MARK[1]) + r"\n\n", lambda _: block, page, flags=re.S)
    else:
        old = PART2.findall(page)
        if len(old) != 1 or 'id="listen"' not in old[0] or 'id="map"' not in old[0]:
            raise SystemExit("v4_home_listen: the home page's old #listen and #map are not where they were")
        page = PART2.sub(lambda _: block, page)
    open(PAGE, "w", encoding="utf-8").write(page)
    print("v4 home listen: %d episode cards in index.html" % sec.count('class="ep-card'))


if __name__ == "__main__":
    main()
