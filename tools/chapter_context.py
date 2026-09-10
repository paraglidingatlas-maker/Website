"""Show each existing chapter's timestamp with the transcript at that point.

38 episodes carry chapter titles cut off mid sentence, generated from host
questions and never rewritten. Their TIMESTAMPS are already correct, so only the
titles need work. This prints the transcript around each existing chapter so a
real title can be written without re-choosing the boundary.

Usage: python3 tools/chapter_context.py <slug> [words]
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def secs(t):
    b = [float(x) for x in t.replace(",", ".").split(":")]
    while len(b) < 3: b.insert(0, 0.0)
    return b[0]*3600 + b[1]*60 + b[2]

def clock(s):
    s = int(s); h, m, x = s//3600, (s % 3600)//60, s % 60
    return "%d:%02d:%02d" % (h, m, x) if h else "%02d:%02d" % (m, x)

slug = sys.argv[1]
nw = int(sys.argv[2]) if len(sys.argv) > 2 else 30
meta = {e["slug"]: e for e in json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))}
e = meta[slug]
cues, t = [], 0.0
for raw in open(os.path.join(ROOT, "transcripts", slug + ".vtt"), encoding="utf-8"):
    line = raw.strip()
    if "-->" in line:
        t = secs(line.split("-->")[0].strip()); continue
    if not line or line == "WEBVTT" or line.isdigit(): continue
    line = re.sub(r"\[SPEAKER_\d+\]:\s*|\[Automatic captions[^\]]*\]", "", line).strip()
    if line: cues.append((t, line))

print("=" * 92)
print("%s   %d chapters" % (slug, len(e.get("chapters") or [])))
for c in e.get("chapters") or []:
    at = secs(c["at"]) if c.get("at") else 0.0
    i = 0
    for n, (ct, _) in enumerate(cues):
        if ct <= at: i = n
        else: break
    txt = " ".join(x[1] for x in cues[i:i+10])
    print("[%s] OLD: %s" % (clock(at), c["title"][:62]))
    print("        %s" % " ".join(txt.split()[:nw]))
