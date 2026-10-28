#!/usr/bin/env python3
"""
The library goes live in the immersion chat's design (owner, 28 Oct 2026: "upload the library page, also
designed in the immersion tab chat, to the current website"). Its page is prototypes/v4/library-e.html ("the
ridge and the voices", script library-e.js); this writes it over prototypes/v4/library.html at the end of the
v4 build, after every pass, so the switch-over publishes it at /library.html.

Two things the option page did not have, added here:
  - its title without the "Option E: " the review copy carried;
  - the series links: 317 links across the site open library.html#s=<series> (an episode's series, a topic
    page's series). The option page filters by shelf, guest, topic and search, not by series, so a small script
    reads #s=, keeps the rows of that series (from episode-meta.json's own series), shows the series name in
    the list's heading with a way back to all, and takes the reader to the list.

Run by tools/v4_build.py after tools/v4_search.py. Idempotent.

    python3 tools/v4_library_live.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "library-e.html")
OUT = os.path.join(V4, "library.html")

SERIES_JS = r"""<script>
/* a series link (library.html#s=<series>, tools/v4_library_live.py): that series' rows, its name in the heading */
(function () {
  var m = /(?:^#|&)s=([^&]+)/.exec(location.hash), d = document;
  if (!m) return;
  var name = decodeURIComponent(m[1].replace(/\+/g, " ")), map = {};
  try { map = JSON.parse(d.getElementById("v4l-series").textContent); } catch (e) { return; }
  var keep = map[name];
  if (!keep) return;
  function run() {
    var set = {}, n = 0;
    keep.forEach(function (s) { set[s] = 1; });
    [].forEach.call(d.querySelectorAll("#browse .v4l-row"), function (r) {
      var on = !!set[r.getAttribute("data-s")]; r.hidden = !on; if (on) n++;
    });
    var more = d.querySelector("#browse .v4l-more"); if (more) more.hidden = true;
    var num = d.querySelector("#browse .v4l-n"); if (num) num.textContent = n;
    var f = d.querySelector("#browse .v4l-filter");
    if (f) {
      f.hidden = false; f.textContent = name + " ";
      var b = d.createElement("button"); b.type = "button"; b.textContent = "Show all";
      b.addEventListener("click", function () { location.hash = ""; location.reload(); });
      f.appendChild(b);
    }
    var br = d.getElementById("browse"); if (br) br.scrollIntoView();
  }
  if (d.readyState === "complete") run(); else window.addEventListener("load", run);
})();
</script>"""


def main():
    s = open(SRC, encoding="utf-8").read()
    s, n = re.subn(r"<title>Option E: ", "<title>", s, count=1)
    if not n and "<title>Option E" in s:
        raise SystemExit("v4_library_live: the title's option label moved")
    s = s.replace('content="Option E: ', 'content="')
    with open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    series = {}
    for e in meta:
        if e.get("series"):
            series.setdefault(e["series"], []).append(e["slug"])
    data = '<script type="application/json" id="v4l-series">%s</script>' % json.dumps(
        series, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    s = s.replace("</body>", data + "\n" + SERIES_JS + "\n</body>", 1)
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if s != old:
        open(OUT, "w", encoding="utf-8").write(s)
    print("v4 library live: library.html is the immersion design (%d series for #s= links)" % len(series))


if __name__ == "__main__":
    main()
