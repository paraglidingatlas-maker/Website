"""One transparent overlay track for a whole talk: every overlay make_talk.py rendered, placed at its time.

    python3 make_track.py TALK.srt OUTDIR

Reads OUTDIR/*_4K60_transparent.mov, the two shade stills and the end card, and writes
OUTDIR/Track_<name>_4K60_transparent.mov: transparent everywhere but the overlays, as long as the talk up to the
end card. In CapCut: drop it on the track above the talk at 0:00. Gaps are copies of one blank second, so the
long empty stretches cost nothing to build (chat 22, 12 Nov 2026).
"""
import asyncio, os, shutil, subprocess, sys
import numpy as np
from PIL import Image
import make_talk as mt

FPS = mt.FPS


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + list(a), check=True)


def frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return int(r.stdout.strip())


def main(srt_path, out):
    c = mt.srt(srt_path)
    seg = os.path.join(out, "track_parts"); os.makedirs(seg, exist_ok=True)
    M = lambda n: os.path.join(out, n + "_4K60_transparent.mov")
    _, _, t_car, _ = mt.career(c)
    _, _, t_br, _ = mt.brands(c)
    ch = [24, 141, 210, 274, 393, 420, 453, 483, 544, 622, 721]
    items = [(0.0, "opener"), (mt.word(c, 2, "Siegel") + 2.0, M("02_NamePlate")), (t_car, "career"),
             (t_br, M("04_Brands")), (c[96][0] - 0.2, M("17_LikeSubscribe")), (c[389][0], M("16_Patreon")),
             (c[857][1] + 0.3, "end")]
    items += [(c[cue][0], M("%02d_Chapter%02d" % (3 + i, i))) for i, cue in enumerate(ch, 2)]
    items.sort()

    # the shades drawn exactly (a browser gradient carries dither noise, which this codec cannot compress)
    W, H = 3840, 2160
    a = np.zeros((H, W), np.float32)
    x = np.arange(W) / W
    stops = [(0, .86), (.32, .62), (.55, .12), (.66, 0)]
    a[:] = np.interp(x, [s for s, _ in stops], [v for _, v in stops])
    op = np.dstack([np.full((H, W), 8), np.full((H, W), 10), np.full((H, W), 12), np.round(a * 255)]).astype(np.uint8)
    Image.fromarray(op, "RGBA").save(os.path.join(seg, "shade_opener.png"))
    b = np.zeros((H, W), np.float32)
    y = (np.arange(H) - (H - 900)) / 900.0          # the band: bottom 900 px, 0 at its top, .82 at the foot
    col = np.interp(1 - y, [0, .55, 1], [.82, .55, 0]); col[y < 0] = 0
    b[:] = col[:, None]
    bd = np.dstack([np.full((H, W), 8), np.full((H, W), 10), np.full((H, W), 12), np.round(b * 255)]).astype(np.uint8)
    Image.fromarray(bd, "RGBA").save(os.path.join(seg, "shade_band.png"))

    # the two overlays with a see-through shade: the still under the clip, faded in and out over 0.5 s
    def shaded(clip, still, name):
        n = frames(clip); d = n / FPS; p = os.path.join(seg, name + ".mov")
        ff("-loop", "1", "-framerate", str(FPS), "-i", still, "-i", clip, "-filter_complex",
           "[0]format=argb,fade=in:st=0:d=0.5:alpha=1,fade=out:st=%.3f:d=0.5:alpha=1[s];[s][1]overlay=format=auto,format=argb" % (d - 0.5),
           "-frames:v", str(n), "-c:v", "qtrle", "-g", "100000", "-pix_fmt", "argb", p)
        return p

    def lean(clip, name):
        """the clip again with one full picture at its start: unchanged lines then cost nothing"""
        p = os.path.join(seg, name + ".mov")
        ff("-i", clip, "-c:v", "qtrle", "-g", "100000", "-pix_fmt", "argb", p)
        return p
    # the end card on a flat ground, held to 15 s
    html, T = mt.endcard()
    fr = os.path.join(seg, "endframes")
    asyncio.run(mt.frames(html.replace('class="bg"', 'class="flat"'), T, fr, False, os.path.join(out, "src")))
    end = os.path.join(seg, "end.mov")
    ff("-framerate", str(FPS), "-i", fr + "/%05d.png", "-vf", "tpad=stop_mode=clone:stop_duration=13.4,format=argb",
       "-c:v", "qtrle", "-g", "100000", "-pix_fmt", "argb", end)
    shutil.rmtree(fr)
    files = {"opener": shaded(M("01_Opener"), os.path.join(seg, "shade_opener.png"), "opener"),
             "career": shaded(M("03_CareerLine"), os.path.join(seg, "shade_band.png"), "career"),
             "end": end}
    for t, f in items:
        if f not in files:
            files[f] = lean(f, os.path.basename(f).split("_4K60")[0])

    blanks = {}
    def blank(n):
        if n not in blanks:
            p = os.path.join(seg, "blank_%d.mov" % n)
            ff("-f", "lavfi", "-i", "color=c=black@0.0:s=3840x2160:r=%d,format=argb" % FPS, "-frames:v", str(n),
               "-c:v", "qtrle", "-g", "100000", "-pix_fmt", "argb", p)
            blanks[n] = p
        return blanks[n]

    lst, cur = [], 0
    for t, f in items:
        f = files.get(f, f)
        start = int(round(t * FPS))
        gap = start - cur
        if gap < 0:
            raise SystemExit("overlap before %s at %.2f s" % (f, t))
        for _ in range(gap // FPS):
            lst.append(blank(FPS))
        if gap % FPS:
            lst.append(blank(gap % FPS))
        lst.append(f)
        cur = start + frames(f)
    with open(os.path.join(seg, "list.txt"), "w") as fh:
        fh.writelines("file '%s'\n" % os.path.abspath(p) for p in lst)
    track = os.path.join(out, "Track_%s_4K60_transparent.mov" % mt.NAME.replace(" ", "_"))
    ff("-f", "concat", "-safe", "0", "-i", os.path.join(seg, "list.txt"), "-c", "copy", track)
    print("track:", track, "%d frames, %.1f s" % (cur, cur / FPS))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
