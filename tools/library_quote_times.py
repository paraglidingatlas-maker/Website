#!/usr/bin/env python3
"""Where in the episode each library quote is spoken, from the timed transcripts.

    python3 tools/library_quote_times.py      -> tools/data/library-quotes.json

For every episode in episode-meta.json with a quote, the transcript on its v4 episode page (blocks of
<span class="cd-ts">mm:ss</span> followed by text) is searched for the quote's words; the block that matches best
gives the time. The match is scored with difflib on normalised words, windowed to the quote's length. A score
under 0.55 is recorded as not found, so no time is shown for it. The exact second inside a block comes from the
audio when the clips are cut; the block time is the minute to deep link and label."""
import difflib, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, "episode-meta.json"); EPS = os.path.join(ROOT, "prototypes", "v4", "episodes")
OUT = os.path.join(ROOT, "tools", "data", "library-quotes.json")
TS = re.compile(r'<span class="cd-ts">(\d{1,2}:\d{2}(?::\d{2})?)</span>(.*?)(?=<span class="cd-ts">|</section>|</div>\s*</div>|$)', re.S)


def norm(s): return re.sub(r"[^a-z0-9' ]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)).lower()).split()


def secs(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def main():
    out, found = {}, 0
    for e in json.load(open(META, encoding="utf-8")):
        q = (e.get("quote") or "").strip(); p = os.path.join(EPS, e["slug"] + ".html")
        if not q or not os.path.exists(p): continue
        src = open(p, encoding="utf-8").read(); qw = norm(q); best = (0, None, "")
        for t, txt in TS.findall(src):
            w = norm(txt)
            if not w: continue
            n = len(qw)
            for i in range(0, max(1, len(w) - n + 1), max(1, n // 3)):
                r = difflib.SequenceMatcher(None, qw, w[i:i + n]).ratio()
                if r > best[0]: best = (r, t, " ".join(w[i:i + n]))
        if best[1] and best[0] >= 0.55:
            found += 1; out[e["slug"]] = {"at": best[1] if len(best[1]) > 4 else best[1], "at_s": secs(best[1]), "score": round(best[0], 2), "words": best[2][:120]}
        else: out[e["slug"]] = {"at": "", "at_s": 0, "score": round(best[0], 2), "words": ""}
    json.dump({"note": "The transcript block where each quote is spoken, found by word match; a score under 0.55 is not shown on the page. The second within the block comes from the audio when the clip is cut.", "quotes": out}, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("quotes", len(out), "timed", found)


if __name__ == "__main__":
    main()
