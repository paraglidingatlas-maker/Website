#!/usr/bin/env python3
"""
The India page's "Front Ridge, Frame By Frame" (#ridge, from india-e.html): 60 frames from the first three
seconds of the Bir clip (assets/video/bir-1080.mp4), drawn by the scroll. The immersion chat's frames were all
the clip's first picture (owner, 28 Oct 2026: "the frame by frame thing doesn't work at all"); this cuts them
again, 20 a second, at 1280 and 800 wide. Run by hand when the clip changes; needs ffmpeg.

    python3 tools/v4_india_ridge_frames.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIP = os.path.join(ROOT, "assets", "video", "bir-1080.mp4")
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "india", "ridge")
FRAMES, SECONDS = 60, 3


def main():
    for w, q in ((1280, 72), (800, 70)):
        d = os.path.join(OUT, str(w))
        os.makedirs(d, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", str(SECONDS), "-i", CLIP,
                        "-vf", "fps=%d,scale=%d:-2" % (FRAMES // SECONDS, w), "-frames:v", str(FRAMES),
                        "-c:v", "libwebp", "-quality", str(q), "-compression_level", "6",
                        os.path.join(d, "f%03d.webp")], check=True)
        print("v4 India ridge: %d frames at %d wide" % (len(os.listdir(d)), w))


if __name__ == "__main__":
    main()
