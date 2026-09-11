"""Surface candidate pull quotes from a transcript.

The user's spec: 1 to 2 sentences, capturing the episode's core message or a
pivotal insight, favouring emotional resonance, actionable advice or a surprising
revelation, with the original wording preserved.

This does not choose. It narrows several thousand sentences down to a few dozen
worth reading, by looking for the shapes those qualities usually take: a flat
assertion about how things are, a rule of thumb, a contradiction, or a number.
Usage: python3 tools/quote_candidates.py <slug> [n]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARKERS = re.compile(r"\b(the (?:most important|key|whole point|biggest|only) "
                     r"|it'?s not (?:about|because)|never |always |you have to |you need to "
                     r"|the problem (?:is|with)|what matters|i think the|my advice"
                     r"|if you (?:don'?t|can'?t|want)|that'?s why|the truth is|people think"
                     r"|nobody |everybody |the difference between|i would say|remember that)", re.I)


def sentences(slug):
    p = os.path.join(ROOT, "transcripts", slug + ".vtt")
    out, cur = [], []
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if "-->" in line or not line or line == "WEBVTT" or line.isdigit():
            continue
        line = re.sub(r"\[SPEAKER_(\d+)\]:\s*", lambda m: "\x00%s\x00" % m.group(1), line)
        line = re.sub(r"\[Automatic captions[^\]]*\]", "", line)
        cur.append(line)
    text = " ".join(cur)
    spk = "?"
    for chunk in re.split(r"\x00(\d+)\x00", text):
        if chunk.isdigit() and len(chunk) <= 2:
            spk = chunk
            continue
        for s in re.split(r"(?<=[.?!])\s+", chunk):
            s = re.sub(r"\s+", " ", s).strip()
            n = len(s.split())
            if 8 <= n <= 45:
                out.append((spk, s))
    return out


def main():
    slug = sys.argv[1]
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    ss = sentences(slug)
    scored = []
    for spk, s in ss:
        sc = 0
        if MARKERS.search(s):
            sc += 3
        if re.search(r"\b\d", s):
            sc += 1
        if 12 <= len(s.split()) <= 32:
            sc += 1
        if s.endswith((".", "!", "?")):
            sc += 1
        if sc >= 4:
            scored.append((sc, spk, s))
    seen, out = set(), []
    for sc, spk, s in sorted(scored, key=lambda x: -x[0]):
        k = s[:40].lower()
        if k in seen:
            continue
        seen.add(k)
        out.append((sc, spk, s))
        if len(out) >= want:
            break
    print("=" * 92)
    print("%s   %d sentences scanned, %d candidates" % (slug, len(ss), len(out)))
    print("=" * 92)
    for sc, spk, s in out:
        print("[s%s] %s" % (spk, s[:180]))


if __name__ == "__main__":
    main()
