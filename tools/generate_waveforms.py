#!/usr/bin/env python3
"""Extract real waveform peaks from the episode audio.

Run this on a machine that can reach the audio host, then commit waveforms.js.
The player picks the shape up with no other change: it draws bars when a slug
has peaks and a plain track when it does not.

    python3 tools/generate_waveforms.py

Needs ffmpeg on PATH. Downloads nothing to disk: ffmpeg streams the audio and
writes raw mono 8-bit samples to stdout, which we reduce to BARS peak values.

WHY NOT IN THE BROWSER: these files run from 5MB to 154MB. Decoding one with the
Web Audio API means downloading all of it before a single bar can be drawn, and
it needs CORS headers the host does not send. Once, at build time, is the only
sensible place. The output is about 2KB per episode.

WHY NOT FAKED: a plausible looking squiggle is invented data. If this script has
not run, the player shows a plain track and says nothing it cannot back up.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BARS = 320          # bars across the strip; 320 is plenty at any realistic width
SR = 8000           # decode rate: peaks do not need fidelity, only shape
OUT = os.path.join(ROOT, "waveforms.js")

HEADER = """/* Real waveform peaks, keyed by episode slug.
 *
 * Written by tools/generate_waveforms.py, which decodes the actual audio with
 * ffmpeg and stores %d peak values per episode, one byte each.
 *
 * Regenerate with: python3 tools/generate_waveforms.py */
""" % BARS


def peaks_for(url):
    """Peak amplitude per bar, 0..255. None if ffmpeg cannot read the stream."""
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", url,
           "-ac", "1", "-ar", str(SR), "-f", "u8", "-"]
    try:
        raw = subprocess.run(cmd, capture_output=True, timeout=900).stdout
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print("    ffmpeg failed: %s" % e)
        return None
    if len(raw) < SR:
        return None
    step = len(raw) / float(BARS)
    out = []
    for i in range(BARS):
        a, b = int(i * step), int((i + 1) * step)
        chunk = raw[a:b] or raw[a:a + 1]
        # u8 PCM is centred on 128, so distance from centre is the amplitude
        out.append(min(255, max(chunk, key=lambda v: abs(v - 128)) and
                       int(max(abs(v - 128) for v in chunk) * 2)))
    top = max(out) or 1
    return [int(v * 255 / top) for v in out]


def main():
    mp3 = json.load(open(os.path.join(ROOT, "mp3-map.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    # only episodes that actually carry a player: the audio-only ones
    want = [e["slug"] for e in meta if not e.get("video_id") and e["slug"] in mp3]

    existing = {}
    if os.path.exists(OUT):
        txt = open(OUT, encoding="utf-8").read()
        i = txt.find("{")
        if i != -1:
            try:
                existing = json.loads(txt[i:txt.rindex("}") + 1])
            except ValueError:
                existing = {}

    done = 0
    for slug in want:
        if slug in existing and existing[slug]:
            print("  have    %s" % slug)
            continue
        print("  reading %s" % slug)
        p = peaks_for(mp3[slug]["url"])
        if p:
            existing[slug] = p
            done += 1
        else:
            print("    skipped, no peaks")

    body = json.dumps(existing, separators=(",", ":"), sort_keys=True)
    open(OUT, "w", encoding="utf-8").write(
        HEADER + "window.ATLAS_WAVEFORMS = " + body + ";\n")
    print("\n%d episode(s) added, %d total, %.1f KB written to waveforms.js"
          % (done, len(existing), len(body) / 1024.0))
    if done:
        print("Now run ./build.sh and commit waveforms.js.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
