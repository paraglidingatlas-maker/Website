#!/usr/bin/env python3
"""Map each episode to the MP3 in the podcast feed, and cache the result.

WHY A CACHE FILE AND NOT A LIVE FETCH
`build.sh` must work with no network. If this fetched the feed every build, an
outage would silently drop the download link from every episode page and nobody
would notice until someone looked. So the mapping is written to `mp3-map.json`,
committed, and only refreshed when this tool is run deliberately with a feed it
can actually reach. A build never touches the network.

NOTHING IS HOSTED HERE. The MP3s live on the podcast host's CDN, where they
already are and already serve every podcast app. This only records the address.
4.67 GB of audio, 0 bytes added to the repo.

THE MATCHER, IN ORDER OF CONFIDENCE
  1. Normalised titles equal.
  2. One normalised title contained in the other, uniquely.
  3. Word overlap, but only with a DECISIVE margin: at least 8 shared words and
     at least 1.5x the runner up. Seven episodes need this, because the podcast
     title and the site title have drifted apart, including a typo in the feed
     ("Dr Matt Wikes" for Wilkes) and several episodes renamed on the site after
     publication.
Anything short of that is left unmapped rather than guessed. A download button
that hands somebody the wrong conversation is worse than no download button.

Usage:  python3 tools/build_mp3_map.py [--check]
        --check exits non-zero if the cached map would change, without writing.
"""
import html
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = "https://anchor.fm/s/ed1344d8/podcast/rss"
OUT = os.path.join(ROOT, "mp3-map.json")

MIN_OVERLAP = 8       # shared words before a fuzzy match is even considered
MIN_MARGIN = 1.5      # and it must beat the runner up by this much


def norm(s):
    s = (s or "").lower().replace("&amp;", " and ").replace("&", " and ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def fetch_feed():
    req = urllib.request.Request(FEED, headers={"User-Agent": "paragliding-atlas-build"})
    with urllib.request.urlopen(req, timeout=45) as fh:
        return fh.read().decode("utf-8", "replace")


def parse(xml):
    out = []
    for item in re.findall(r"<item>(.*?)</item>", xml, re.S):
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item, re.S)
        e = re.search(r'<enclosure[^>]*url="([^"]+)"[^>]*length="(\d+)"', item)
        if t and e:
            out.append({"title": html.unescape(t.group(1)).strip(),
                        "url": html.unescape(e.group(1)),
                        "bytes": int(e.group(2))})
    return out


def match(feed, meta):
    by_norm = {norm(e["title"]): e for e in meta}
    mapping, unmatched = {}, []
    for f in feed:
        n = norm(f["title"])
        ep = by_norm.get(n)
        how = "exact"
        if ep is None:
            c = [e for e in meta if n and (n in norm(e["title"]) or norm(e["title"]) in n)]
            if len(c) == 1:
                ep, how = c[0], "contained"
        if ep is None:
            words = set(n.split())
            scored = sorted(((len(words & set(norm(e["title"]).split())), e) for e in meta),
                            key=lambda x: -x[0])
            if scored and scored[0][0] >= MIN_OVERLAP:
                runner = scored[1][0] if len(scored) > 1 else 0
                if runner == 0 or scored[0][0] >= runner * MIN_MARGIN:
                    ep, how = scored[0][1], "overlap %d vs %d" % (scored[0][0], runner)
        if ep is None:
            unmatched.append(f["title"])
        else:
            mapping[ep["slug"]] = {"url": f["url"], "bytes": f["bytes"],
                                   "feed_title": f["title"], "matched_by": how}
    return mapping, unmatched


def main():
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    try:
        xml = fetch_feed()
    except Exception as exc:                       # noqa: BLE001
        print("could not reach the feed: %s" % exc)
        print("the cached mp3-map.json is unchanged, and the build does not need the feed")
        return 0
    feed = parse(xml)
    mapping, unmatched = match(feed, meta)
    print("feed items: %d | mapped: %d | unmatched: %d" % (len(feed), len(mapping), len(unmatched)))
    for u in unmatched:
        print("   unmatched: %s" % u[:70])
    fuzzy = {k: v for k, v in mapping.items() if v["matched_by"].startswith("overlap")}
    if fuzzy:
        print("matched by word overlap, check these by eye:")
        for k, v in fuzzy.items():
            print("   %-52s %s" % (k[:52], v["matched_by"]))
    new = json.dumps(mapping, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if "--check" in sys.argv:
        if new != old:
            print("mp3-map.json is out of date; run this without --check")
            return 1
        print("mp3-map.json is up to date")
        return 0
    open(OUT, "w", encoding="utf-8").write(new)
    print("wrote mp3-map.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
