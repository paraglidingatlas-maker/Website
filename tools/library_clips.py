#!/usr/bin/env python3
"""Cut the library's voice clips: the sentence each guest says in the hero, from the podcast's own audio.

    python3 tools/library_clips.py --plan <plan.json> --out prototypes/v4/img/library/clips

The plan maps slug -> {file: local audio from the podcast RSS enclosure, at_s: the transcript block's second, title}.
Around at_s a window is transcribed with faster-whisper (word timestamps); the quote's words are matched inside it
(difflib over normalised words); the clip runs from 0.35 s before the first matched word to 0.45 s after the last,
with a 60 ms fade each end, mono mp3 at 64 kb/s. A match under 0.6 is reported and not written. The second found
is recorded next to the clip in <out>/clips.json so the page's "at mm:ss" can be exact."""
import argparse, difflib, html, json, os, re, subprocess, tempfile

def norm(s): return re.sub(r"[^a-z0-9' ]+", " ", html.unescape(s).lower()).split()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True); ap.add_argument("--model", default="small.en"); ap.add_argument("--only", default="")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    meta = {e["slug"]: e for e in json.load(open(os.path.join(root, "episode-meta.json"), encoding="utf-8"))}
    plan = json.load(open(a.plan)); rec_p = os.path.join(a.out, "clips.json")
    rec = json.load(open(rec_p)) if os.path.exists(rec_p) else {}
    for slug, v in plan.items():
        if a.only and slug != a.only: continue
        q = norm(meta[slug]["quote"]); start = max(0, v["at_s"] - 45); length = 170
        with tempfile.TemporaryDirectory() as td:
            win = os.path.join(td, "w.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-t", str(length), "-i", v["file"], "-ac", "1", "-ar", "16000", win], check=True)
            import numpy as np, wave
            with wave.open(win) as wf: pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            segs, _ = model.transcribe(pcm, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
            words = []
            for sg in segs:
                for w in sg.words or []:
                    for tok in norm(w.word): words.append((tok, w.start, w.end))
        toks = [w[0] for w in words]; n = len(q); best = (0, 0)
        for i in range(0, max(1, len(toks) - n // 2)):
            r = difflib.SequenceMatcher(None, q, toks[i:i + n]).ratio()
            if r > best[0]: best = (r, i)
        if best[0] < 0.6: print("NO MATCH %.2f %s" % (best[0], slug)); rec[slug] = {"score": round(best[0], 2)}; continue
        i = best[1]; j = min(len(words) - 1, i + n - 1)
        # trim the matched span to the first and last quote words that line up
        t0 = max(0, words[i][1] - 0.35); t1 = words[j][2] + 0.45; dur = t1 - t0
        out = os.path.join(a.out, slug + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start + t0), "-t", "%.2f" % dur, "-i", v["file"], "-ac", "1", "-ar", "44100", "-b:a", "64k",
                        "-af", "afade=t=in:st=0:d=0.06,afade=t=out:st=%.2f:d=0.06" % max(0, dur - 0.06), out], check=True)
        at_s = int(start + t0); rec[slug] = {"score": round(best[0], 2), "at_s": at_s, "at": "%02d:%02d" % (at_s // 60, at_s % 60), "dur": round(dur, 1), "heard": " ".join(toks[i:j + 1])}
        print("%.2f %-42s %s %5.1fs  %s" % (best[0], slug[:42], rec[slug]["at"], dur, rec[slug]["heard"][:70]))
        json.dump(rec, open(rec_p, "w"), indent=1)

if __name__ == "__main__":
    main()
