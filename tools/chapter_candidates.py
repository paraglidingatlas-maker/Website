"""Print candidate chapter boundaries for an episode transcript.

A chapter is only useful if clicking it lands the reader in the right place, so
boundaries have to come from the transcript itself rather than from matching a
topic phrase against it. Keyword matching was tried and placed most topics on
unrelated passages.

In an interview the topic changes when the HOST speaks. Two ways to find that:
  - transcripts with [SPEAKER_NN] tags: take the turns belonging to the host
    (the speaker who asks the most questions), which are the real boundaries.
  - transcripts without tags (the Spotify ones): fall back to question shaped
    sentences, which are nearly always the host opening a new subject.

Either way every candidate carries a real timestamp taken from the cue it came
from, so a chapter placed on one cannot drift.

Usage: python3 tools/chapter_candidates.py <slug> [max]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def secs(t):
    b = [float(x) for x in t.replace(",", ".").split(":")]
    while len(b) < 3:
        b.insert(0, 0.0)
    return b[0] * 3600 + b[1] * 60 + b[2]


def clock(s):
    s = int(s)
    h, m, x = s // 3600, (s % 3600) // 60, s % 60
    return "%d:%02d:%02d" % (h, m, x) if h else "%02d:%02d" % (m, x)


def load(slug):
    cues, t = [], 0.0
    path = os.path.join(ROOT, "transcripts", slug + ".vtt")
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if "-->" in line:
            t = secs(line.split("-->")[0].strip())
            continue
        if not line or line == "WEBVTT" or line.isdigit():
            continue
        spk = None
        m = re.match(r"\[SPEAKER_(\d+)\]:\s*", line)
        if m:
            spk = int(m.group(1))
            line = line[m.end():]
        line = re.sub(r"\[Automatic captions[^\]]*\]", "", line).strip()
        if line:
            cues.append({"t": t, "spk": spk, "text": line})
    return cues


def main():
    slug = sys.argv[1]
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    cues = load(slug)
    if not cues:
        print("no cues"); return
    labelled = any(c["spk"] is not None for c in cues)
    total = cues[-1]["t"]
    print("=" * 96)
    print("%s   %s   %d cues   speaker labels: %s"
          % (slug, clock(total), len(cues), "yes" if labelled else "no"))
    print("=" * 96)

    cands = []
    if labelled:
        # the host is whoever asks the most questions
        qs = {}
        for c in cues:
            if "?" in c["text"]:
                qs[c["spk"]] = qs.get(c["spk"], 0) + 1
        host = max(qs, key=qs.get) if qs else 0
        prev = None
        for i, c in enumerate(cues):
            if c["spk"] == host and prev != host:
                win = " ".join(x["text"] for x in cues[i:i + 6])
                cands.append((c["t"], win))
            prev = c["spk"]
        print("(host is SPEAKER_%02d, %d turns)" % (host, len(cands)))
    else:
        for i, c in enumerate(cues):
            if "?" not in c["text"]:
                continue
            win = " ".join(x["text"] for x in cues[i:i + 6])
            cands.append((c["t"], win))

    # thin out: keep candidates spread across the episode
    keep, last = [], -999
    gap = max(60.0, total / (cap * 1.6))
    for t, w in cands:
        if t - last >= gap:
            keep.append((t, w)); last = t
    for t, w in keep[:cap]:
        print("[%s] %s" % (clock(t), " ".join(w.split())[:190]))


if __name__ == "__main__":
    main()
