"""Add INFERRED speaker turns to the Eric Roussel transcript.

Why this exists
---------------
Spotify's captions carry real timestamps but no diarisation. The other 45
transcripts on this site come from Autotekst, whose [SPEAKER_NN] tags come from
the audio. These labels do NOT. They were read off the text of a two person
interview: the host introduces, thanks and asks; the guest answers. The user
asked for them and agreed the page must say they are inferred.

How it works
------------
Every turn below is anchored to an exact phrase where the speaker changes. The
anchors are searched in order through the joined transcript, so each is found
after the previous one. A missing anchor is a hard error rather than a silent
mislabel, because a boundary that quietly fails to match would attribute one
person's words to the other, which is the whole risk here.

Where a turn starts mid cue the cue is split, and the split time is interpolated
across the cue by word position.

Run: python3 tools/infer_speakers_eric.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VTT = os.path.join(ROOT, "transcripts", "brand-stories-neo-eric-roussel.vtt")

HOST, GUEST = 0, 1

# (speaker, anchor). The file opens on a cold open clip of the guest, so the
# first turn is the guest and the first anchor below is the host's welcome.
TURNS = [
    (HOST,  "Thank you for coming, Eric"),
    (GUEST, "The name is Neil. It's not Neil Atalier"),
    (HOST,  "Thanks for explaining it so well"),
    (GUEST, "It's a part of the main strategy of NAO"),
    (HOST,  "That's wonderful to hear that that capitalism"),
    (GUEST, "And they all were 12 years ago, the first harness called the string"),
    (HOST,  "Have you found it challenging to meet the price bracket"),
    (GUEST, "It's a silence. We have to design our products"),
    (HOST,  "What a way to put it across"),
    (GUEST, "Freaking enough way of manufacturing the world"),
    (HOST,  "Wow, That's what passion projects are about"),
    (GUEST, "The first thing is to fly and love to fly"),
    (HOST,  "Why do some brands fail after a period of time"),
    (GUEST, "Because like I said, it's mainly based on the passion"),
    (HOST,  "This is one thing that I've commonly seen with a lot of creative people"),
    (GUEST, "I think the powergliding is expensive"),
    (HOST,  "Love the way you put it. This is pure gold"),
    (GUEST, "I got to talk with SIV instructors"),
    (HOST,  "Let's take Rogallo right?"),
    (GUEST, "The market is changing. 20 years ago we were flying with rescue"),
    (HOST,  "Very interesting, I love the way you explain it"),
    (GUEST, "It looks like we diversify, but in fact we didn't diversify"),
    (HOST,  "I'm curious about the helmet part"),
    (GUEST, "This is the only product we don't manufacture ourselves"),
    (HOST,  "Love your take on that"),
    (GUEST, "Well, when I start my brain off harness"),
    (HOST,  "I want to talk a little bit about the working of Korea"),
    (GUEST, "The main thing is the first"),
    (HOST,  "I'm just curious that did wasn't"),
    (GUEST, "Impact on the parallel lighting harness is not only about choroid"),
    (HOST,  "Makes sense, but."),
    (GUEST, "If he was falling, he cannot see"),
    (HOST,  "I'm just curious when it comes to twisting of the blocks"),
    (GUEST, "We improved a lot of this problem"),
    (HOST,  "But when I see that you guys are fusing materials"),
    (GUEST, "We tried some years ago to develop something like origami"),
    (HOST,  "No, I love your honesty, Eric"),
    (GUEST, "Just a problem of IO dynamics"),
    (HOST,  "Flexibility of the fairing is that you're saying?"),
    (GUEST, "Yes, how do you call like a boat?"),
    (HOST,  "Wonderful tool. Now you've answered 10 questions"),
    (GUEST, "In the paragliding design, it's very different"),
    (HOST,  "I agree, and I think having Maxim as part of your team"),
    (GUEST, "You can install Rogal Apex square rescue"),
    (HOST,  "I have come under down planning"),
    (GUEST, "everybody is studying the party"),
    (HOST,  "Brings back memories of Sharknose invention by Ozone"),
    (GUEST, "1st I open it because safety and paragliding is my passion"),
    (HOST,  "I think it's visible in your philosophy"),
    (GUEST, "Ten years ago, during the development of String 2"),
    (HOST,  "Surprised me when Dyneema is so much stronger"),
    (GUEST, "I always consider that in development of projects there's no magic solution"),
    (HOST,  "I love it, but I think that is the ideology behind your success"),
    (GUEST, "It was must start with non weaving fabrics"),
    (HOST,  "Your your brand isn't innovating in in small things"),
    (GUEST, "That people working in NEO"),
    (HOST,  "Lovett MA, more power to you"),
    (GUEST, "Thank you."),
]

CUE = re.compile(r"^(?P<s>[\d:.,]+)\s*-->\s*(?P<e>[\d:.,]+)")


def secs(stamp):
    bits = [float(b) for b in stamp.replace(",", ".").split(":")]
    while len(bits) < 3:
        bits.insert(0, 0.0)
    return bits[0] * 3600 + bits[1] * 60 + bits[2]


def stamp(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    rest = s - h * 3600 - m * 60
    return "%02d:%02d:%06.3f" % (h, m, rest)


def read_cues(path):
    cues, cur = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        m = CUE.match(line)
        if m:
            if cur:
                cues.append(cur)
            cur = {"start": secs(m.group("s")), "end": secs(m.group("e")), "text": ""}
            continue
        if not line or line.upper() == "WEBVTT" or line.isdigit():
            continue
        if cur is not None:
            cur["text"] = (cur["text"] + " " + line).strip()
    if cur:
        cues.append(cur)
    return [c for c in cues if c["text"]]


def main():
    cues = read_cues(VTT)
    # Joined stream plus the exact character span of each cue inside it. The
    # separator space belongs to NO cue: counting it into the following cue
    # shifts every offset by one and slices the first letter off each turn.
    parts, span, pos_c = [], [], 0
    for i, c in enumerate(cues):
        if parts:
            parts.append(" ")
            pos_c += 1
        span.append((pos_c, pos_c + len(c["text"])))
        parts.append(c["text"])
        pos_c += len(c["text"])
    stream = "".join(parts)

    # locate every boundary, in order
    marks, pos, missing = [], 0, []
    for spk, anchor in TURNS:
        at = stream.find(anchor, pos)
        if at == -1:
            missing.append(anchor)
            continue
        marks.append((at, spk, anchor))
        pos = at + len(anchor)

    if missing:
        print("FAIL: %d anchor(s) not found in the transcript. Nothing written." % len(missing))
        for a in missing:
            print("   " + a)
        sys.exit(1)

    # map each boundary to a cue and an offset inside that cue
    out = []
    cur_spk = GUEST          # the file opens on a cold open clip of the guest
    bi = 0
    for i, c in enumerate(cues):
        lo, hi = span[i]
        splits = []
        while bi < len(marks) and lo <= marks[bi][0] < hi:
            splits.append((marks[bi][0] - lo, marks[bi][1]))
            bi += 1
        if not splits:
            out.append(dict(c, speaker=cur_spk))
            continue
        # split this cue at each boundary, interpolating the time by word count
        text = c["text"]
        bounds = [0] + [s[0] for s in splits] + [len(text)]
        spks = [cur_spk] + [s[1] for s in splits]
        total = max(1, len(text))
        for n in range(len(bounds) - 1):
            seg = text[bounds[n]:bounds[n + 1]].strip()
            if not seg:
                continue
            t0 = c["start"] + (c["end"] - c["start"]) * (bounds[n] / total)
            t1 = c["start"] + (c["end"] - c["start"]) * (bounds[n + 1] / total)
            out.append({"start": t0, "end": max(t1, t0 + 0.2),
                        "text": seg, "speaker": spks[n]})
        cur_spk = spks[-1]

    lines = ["WEBVTT", ""]
    for c in out:
        lines.append("%s --> %s" % (stamp(c["start"]), stamp(c["end"])))
        lines.append("[SPEAKER_%02d]: %s" % (c["speaker"], c["text"]))
        lines.append("")
    open(VTT, "w", encoding="utf-8").write("\n".join(lines))

    turns = sum(1 for n in range(1, len(out)) if out[n]["speaker"] != out[n - 1]["speaker"]) + 1
    host_w = sum(len(c["text"].split()) for c in out if c["speaker"] == HOST)
    guest_w = sum(len(c["text"].split()) for c in out if c["speaker"] == GUEST)
    print("anchors matched : %d/%d" % (len(marks), len(TURNS)))
    print("cues written    : %d" % len(out))
    print("speaker turns   : %d" % turns)
    print("host words      : %d (%.0f%%)" % (host_w, 100.0 * host_w / (host_w + guest_w)))
    print("guest words     : %d (%.0f%%)" % (guest_w, 100.0 * guest_w / (host_w + guest_w)))


if __name__ == "__main__":
    main()
