#!/usr/bin/env python3
"""
Turn a knowledge base tile into everything the episode popup needs.

WHY THIS EXISTS
The KB tiles were declared in generate_kb_pages.py with a short title and a
guest name and nothing else, so every popup on the site showed a broken
thumbnail and "Full episode details and show notes coming soon". All the real
data existed; nothing joined it up.

HOW THE JOIN WORKS, in order of confidence:
  1. kb_yt_mapping.json maps a tile title to a YouTube id. 61 of the 71 tiles
     are in there and it is exact, so it is tried first.
  2. Failing that, match on guest name plus series. That recovers tiles whose
     KB title is a shortened version of the real episode title, which is why
     the mapping misses them.
  3. Failing that, return None. The caller then emits the tile exactly as it is
     today. Nothing is guessed: a wrong episode behind a tile is worse than a
     plain tile.

CHAPTER ANCHORS ARE READ FROM THE BUILT EPISODE PAGE, NOT CALCULATED.
This matters and it is not obvious. The page numbers its transcript blocks from
c1, but the FIRST chapter is c2, because c1 is the audio before any chapter
starts. Worse, chapters with no transcript underneath them are dropped from the
page entirely, and that happens on 43 of the 78 episodes that have chapters, at
the start, the middle and the end. So chapter index plus one is wrong almost
half the time, and wrong in a way that still looks like it works: the link
opens the transcript, just at the wrong place.

build.sh runs generate_chapter_deck.py before generate_kb_pages.py, so the
episode pages exist when this reads them. If one is missing, the chapters come
back without anchors and the popup renders them as plain text.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_cache = {}


def _load(name):
    if name not in _cache:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            _cache[name] = json.load(fh)
    return _cache[name]


def _meta():
    return _load("episode-meta.json")


def _by_video():
    if "_byvid" not in _cache:
        _cache["_byvid"] = {e["video_id"]: e for e in _meta() if e.get("video_id")}
    return _cache["_byvid"]


def _pins():
    """Episode slug to (lon, lat), read out of globe.js.

    globe.js holds the only per-episode coordinates on the site, as
    [title, href, lon, lat]. 78 of 93 episodes have one.
    """
    if "_pins" not in _cache:
        src = open(os.path.join(ROOT, "globe.js"), encoding="utf-8").read()
        pins = {}
        for _q, _t, href, lon, lat in re.findall(
                r'\[\s*(["\'])(.*?)\1\s*,\s*\'(episodes/[^\']+)\'\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\]',
                src, re.S):
            pins[href.split("/")[-1].replace(".html", "")] = (float(lon), float(lat))
        _cache["_pins"] = pins
    return _cache["_pins"]


def _anchors(slug):
    """Chapter title to its real anchor on the built episode page."""
    path = os.path.join(ROOT, "episodes", slug + ".html")
    if not os.path.exists(path):
        return {}
    html = open(path, encoding="utf-8").read()
    out = {}
    for anchor, label in re.findall(
            r'<a class="cd-chap" href="#(c\d+)"[^>]*>(.*?)</a>', html, re.S):
        text = re.sub(r"<[^>]+>", "", label)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"\d?\d:\d\d(:\d\d)?$", "", text).strip()
        out[text] = anchor
    return out


def _tag_page(tag):
    slug = tag.lower().replace(" ", "-")
    return ("tags/%s.html" % slug
            if os.path.exists(os.path.join(ROOT, "tags", slug + ".html")) else None)


def _norm(s):
    """Loose form of a title for comparison: case, punctuation and & folded.

    `&amp;` is unescaped first. A tile title written with the HTML entity would
    otherwise normalise to "amp" and quietly fail to match, which is exactly what
    happened when the Dr Matt Wilkes tiles were added.
    """
    s = (s or "").lower().replace("&amp;", " and ").replace("&", " and ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def resolve(tile_title, tile_guest, series_name=None):
    """The episode behind a tile, or None if it cannot be identified.

    Four attempts, each one only accepted when it is UNAMBIGUOUS. A tile that
    matches two episodes is left unresolved on purpose: a plain tile is better
    than a card describing the wrong conversation.
    """
    # 1. The mapping file. Exact, and covers 61 of the 71 tiles.
    ep = _by_video().get(_load("kb_yt_mapping.json").get(tile_title))
    if ep is not None:
        return ep

    want = (tile_guest or "").strip().lower()
    meta = _meta()

    # 2. Guest within this series. Tight, so it is tried before guest alone.
    if want:
        hits = [e for e in meta
                if (e.get("guest") or "").strip().lower() == want
                and (series_name is None or (e.get("series") or "") == series_name)]
        if len(hits) == 1:
            return hits[0]

    # 3. Guest anywhere on the site, if that guest appears exactly once. Catches
    #    tiles filed under a different series name from the episode's own.
    if want:
        hits = [e for e in meta if (e.get("guest") or "").strip().lower() == want]
        if len(hits) == 1:
            return hits[0]

    # 4. The KB title is usually a shortened form of the episode title, so a
    #    unique containment match recovers the rest. "New Technologies 3" sits
    #    inside "New Technologies 3 : Stephan Stiegler (AirDesign Paragliders)".
    #    Unique only: "PWCA" appears in two episode titles and stays unresolved.
    n = _norm(tile_title)
    if n:
        hits = [e for e in meta if n in _norm(e.get("title", ""))]
        if len(hits) == 1:
            return hits[0]

    return None


def modal_data(tile_title, tile_guest, series_name, series_page):
    """Everything the popup renders, or None.

    Returns real values only. A field the data does not have comes back as None
    or an empty list and the popup leaves that part out rather than filling it.
    """
    ep = resolve(tile_title, tile_guest, series_name)
    if ep is None:
        return None

    slug = ep["slug"]
    anchors = _anchors(slug)
    chapters = []
    for c in (ep.get("chapters") or [])[:5]:
        chapters.append({
            "at": c.get("at", ""),
            "title": c.get("title", ""),
            "anchor": anchors.get(c.get("title", "")),
        })

    same = [e for e in _meta() if (e.get("series") or "") == (ep.get("series") or "")]
    same.sort(key=lambda e: e.get("published") or "")
    pos = next((i for i, e in enumerate(same, 1) if e["slug"] == slug), None)

    lonlat = _pins().get(slug)

    return {
        "slug": slug,
        "page": "../episodes/%s.html" % slug,
        "title": ep.get("title", ""),
        "guest": (ep.get("guest") or "").strip(),
        "quote": (ep.get("quote") or "").strip(),
        "summary": (ep.get("summary") or "").strip(),
        "video": (ep.get("video_id") or "").strip(),
        "epno": (ep.get("epno") or "").strip(),
        "date": (ep.get("published_label") or "").strip(),
        "dur": (ep.get("duration_label") or "").strip(),
        "series": (ep.get("series") or "").strip(),
        "seriesPage": series_page,
        "pos": pos,
        "nser": len(same),
        "nchapters": len(ep.get("chapters") or []),
        "chapters": chapters,
        "tags": [{"name": t, "page": _tag_page(t)} for t in (ep.get("tags") or [])[:6]],
        "lon": lonlat[0] if lonlat else None,
        "lat": lonlat[1] if lonlat else None,
    }
