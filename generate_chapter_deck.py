#!/usr/bin/env python3
"""
Build individual episode pages in the agreed "Chapter Deck" format.

Inputs
------
transcripts/<slug>.vtt   WebVTT from Whisper, with [SPEAKER_NN] diarisation tags.
episode-meta.json        One entry per episode: title, guest, dates, chapters, etc.
library-data.js          Reused for the series each episode belongs to.

Output
------
episodes/<slug>.html     Uses episodes/episode.css, which is lifted verbatim from
                         prototypes/episode-page-chapter-deck-FINAL.html.

Chapters
--------
Chapter titles come from the episode's own show notes (the bullet list the host
already writes for every episode). Each chapter carries a `cue`: a short phrase
spoken in the episode. The generator finds that phrase in the transcript and
takes its timestamp, so the timings are real rather than estimated. A chapter can
instead carry an explicit `at` timestamp to override the search.

Run: python3 generate_chapter_deck.py [slug ...]
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TX = os.path.join(ROOT, "transcripts")
OUT = os.path.join(ROOT, "episodes")

CUE = re.compile(
    r"^(?P<s>\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s*-->\s*"
    r"(?P<e>\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s*(?P<rest>.*)$"
)
SPK = re.compile(r"^\[?SPEAKER[ _]?(?P<n>\d+)\]?\s*:\s*", re.I)
NOISE = re.compile(r"^\[.*(automatic caption|whisper|recognition error).*\]$", re.I)


# ---------------------------------------------------------------- parsing

def secs(stamp):
    stamp = stamp.replace(",", ".")
    bits = [float(b) for b in stamp.split(":")]
    while len(bits) < 3:
        bits.insert(0, 0.0)
    return bits[0] * 3600 + bits[1] * 60 + bits[2]


def clock(s):
    s = int(s)
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return "%d:%02d:%02d" % (h, m, sec) if h else "%02d:%02d" % (m, sec)


def parse_vtt(path):
    """Return a list of {start, speaker, text} cues."""
    cues, pending = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = CUE.match(line.strip())
        if m:
            if pending:
                cues.append(pending)
            rest = m.group("rest").strip()
            spk = None
            sm = SPK.match(rest)
            if sm:
                spk = int(sm.group("n"))
                rest = rest[sm.end():]
            pending = {"start": secs(m.group("s")), "end": secs(m.group("e")),
                       "speaker": spk, "text": rest}
            continue
        if pending is None or not line.strip():
            continue
        if line.strip().upper() == "WEBVTT" or line.strip().isdigit():
            continue
        extra = line.strip()
        sm = SPK.match(extra)
        if sm:
            if pending["speaker"] is None:
                pending["speaker"] = int(sm.group("n"))
            extra = extra[sm.end():]
        pending["text"] = (pending["text"] + " " + extra).strip()
    if pending:
        cues.append(pending)
    return [c for c in cues if c["text"] and not NOISE.match(c["text"])]


def paragraphs(cues, gap=2.5, max_words=110):
    """Merge cues into readable paragraphs, breaking on speaker change or a pause."""
    out, cur = [], None
    for c in cues:
        new = (
            cur is None
            or c["speaker"] != cur["speaker"]
            or c["start"] - cur["end"] > gap
            or len(cur["text"].split()) > max_words
        )
        if new:
            if cur:
                out.append(cur)
            cur = {"start": c["start"], "end": c["end"], "speaker": c["speaker"], "text": c["text"]}
        else:
            cur["text"] += " " + c["text"]
        cur["end"] = c.get("end", c["start"])
    if cur:
        out.append(cur)
    return out


# ---------------------------------------------------------------- chapters

def norm(t):
    return re.sub(r"[^a-z0-9 ]+", " ", t.lower()).strip()


def locate(cue_phrase, cues):
    """Find the timestamp where a phrase from the show notes is spoken."""
    want = norm(cue_phrase)
    if not want:
        return None
    words = want.split()
    joined, index = [], []
    for c in cues:
        for w in norm(c["text"]).split():
            joined.append(w)
            index.append(c["start"])
    best, at = 0.0, None
    for i in range(len(joined) - len(words) + 1):
        window = joined[i:i + len(words)]
        hit = sum(1 for a, b in zip(window, words) if a == b) / len(words)
        if hit > best:
            best, at = hit, index[i]
    return at if best >= 0.7 else None


def resolve_chapters(meta, cues):
    """Attach a real timestamp to every chapter. Returns (chapters, warnings)."""
    chapters, warn = [], []
    for n, ch in enumerate(meta.get("chapters", [])):
        at = None
        if ch.get("at"):
            at = secs(ch["at"] if ch["at"].count(":") >= 2 else "00:" + ch["at"])
        elif ch.get("cue"):
            at = locate(ch["cue"], cues)
            if at is None:
                warn.append("could not place chapter %r using cue %r" % (ch["title"], ch["cue"]))
        if at is None:
            at = 0.0 if n == 0 else None
        if at is None:
            continue
        chapters.append({"title": ch["title"], "at": at})
    chapters.sort(key=lambda c: c["at"])
    if chapters and chapters[0]["at"] > 1:
        chapters.insert(0, {"title": meta.get("opening", "Introduction"), "at": 0.0})
    return chapters, warn


# ---------------------------------------------------------------- rendering

def esc(t):
    return html.escape(str(t), quote=True)


def render_transcript(paras, chapters, speakers):
    """Group paragraphs under their chapter, so the rail can scrollspy them."""
    blocks, out = [], []
    if not chapters:
        chapters = [{"title": "Transcript", "at": 0.0}]
    bounds = [c["at"] for c in chapters] + [float("inf")]
    for n, ch in enumerate(chapters):
        inside = [p for p in paras if bounds[n] <= p["start"] < bounds[n + 1]]
        if inside:
            blocks.append((n + 1, ch, inside))
    for cid, ch, inside in blocks:
        lines, last = [], object()
        for p in inside:
            who = speakers.get(str(p["speaker"]), speakers.get("default", ""))
            show = who and p["speaker"] != last
            spk = '<span class="cd-spk">%s:</span> ' % esc(who) if show else ""
            last = p["speaker"]
            lines.append('        <p class="cd-line">%s%s</p>' % (spk, esc(p["text"])))
        out.append(
            '      <div class="cd-block" id="c%d">\n'
            '        <p class="cd-block-time">%s</p>\n'
            '        <h3>%s</h3>\n%s\n      </div>'
            % (cid, clock(ch["at"]), esc(ch["title"]), "\n".join(lines))
        )
    return "\n".join(out)


def render_rail(chapters):
    return "\n".join(
        '      <a class="cd-chap%s" href="#c%d">%s<time>%s</time></a>'
        % (" active" if n == 0 else "", n + 1, esc(c["title"]), clock(c["at"]))
        for n, c in enumerate(chapters)
    )


def render_list(items, cls="cd-link"):
    return "\n".join(
        '        <a class="%s" href="%s" target="_blank" rel="noopener">%s</a>'
        % (cls, esc(i["url"]), esc(i["label"])) for i in items
    )


def build(meta, cues, chapters):
    paras = paragraphs(cues)
    words = sum(len(p["text"].split()) for p in paras)
    vid = meta.get("video_id", "")
    tmpl = open(os.path.join(ROOT, "episode-template.html"), encoding="utf-8").read()

    jsonld = {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "name": meta["title"],
        "datePublished": meta.get("published", ""),
        "description": meta.get("summary", "")[:280],
        "partOfSeries": {"@type": "PodcastSeries", "name": "Paragliding Atlas"},
        "url": "https://paraglidingatlas-maker.github.io/Website/episodes/%s.html" % meta["slug"],
    }
    if meta.get("guest"):
        jsonld["actor"] = {"@type": "Person", "name": meta["guest"]}

    submeta = []
    if meta.get("guest"):
        submeta.append("<span><strong>%s</strong></span>" % esc(meta["guest"]))
    if meta.get("published_label"):
        submeta.append("<span>%s</span>" % esc(meta["published_label"]))
    if meta.get("duration_label"):
        submeta.append("<span>%s</span>" % esc(meta["duration_label"]))
    submeta.append("<span>Full transcript</span>")
    submeta_html = '<span class="cd-dot"></span>'.join(submeta)

    return tmpl.format(
        title=esc(meta["title"]),
        seo_desc=esc(meta.get("summary", "")[:155]),
        slug=meta["slug"],
        series=esc(meta.get("series", "")),
        series_slug=meta.get("series_slug", ""),
        epno=esc(meta.get("epno", "")),
        submeta=submeta_html,
        video_id=esc(vid),
        rail=render_rail(chapters),
        summary=esc(meta.get("summary", "")),
        transcript=render_transcript(paras, chapters, meta.get("speakers", {})),
        guest_name=esc(meta.get("guest", "")),
        guest_role=esc(meta.get("guest_role", "")),
        guest_links=render_list(meta.get("guest_links", [])),
        resources=render_list(meta.get("resources", [])),
        related=render_list(meta.get("related", [])),
        tags="\n".join('        <span class="cd-tag">%s</span>' % esc(t) for t in meta.get("tags", [])),
        spotify=esc(meta.get("spotify", "https://open.spotify.com/show/16jBM3RfjVERukNHJrIRec")),
        jsonld=json.dumps(jsonld, ensure_ascii=False, indent=2),
        words="{:,}".format(words),
    )


# ---------------------------------------------------------------- main

def main(only=None):
    metas = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    built, skipped = 0, []
    for meta in metas:
        slug = meta["slug"]
        if only and slug not in only:
            continue
        vtt = os.path.join(TX, slug + ".vtt")
        if not os.path.exists(vtt):
            skipped.append((slug, "no transcript at transcripts/%s.vtt" % slug))
            continue
        cues = parse_vtt(vtt)
        chapters, warn = resolve_chapters(meta, cues)
        for w in warn:
            print("  warning [%s] %s" % (slug, w))
        page = build(meta, cues, chapters)
        open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8").write(page)
        print("  built %-52s %2d chapters, %d cues" % (slug + ".html", len(chapters), len(cues)))
        built += 1
    print("\n%d page(s) built." % built)
    for s, why in skipped:
        print("  skipped %-46s %s" % (s, why))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
