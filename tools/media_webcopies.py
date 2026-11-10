#!/usr/bin/env python3
"""Web copies of a comp's photos for the gallery pages (chat 19, 4 Nov 2026).

Reads a Google Drive folder shared by link (the owner's "All Tasks" folder for a comp), downloads one original at a
time, writes its 800, 1600 and 2400 px WebP copies (the long edge) into the media repo's comp folder, and deletes the
original at once, so the container's disk never holds more than a few originals (they are about 15 MB each). A copy
already written is skipped, so the run can stop and start again.

It also writes photos.json beside the copies: one entry per photo (stem, day, width and height of the 2400 copy, and
"shot", the camera's capture time from the original's EXIF, read from the first 256 KB of the file only), in shooting
order within each day (by the number in the owner's file names; see main() for why not by capture time). The Drive file ids are never written to the media repo (it is public, and the owner
sells the originals): they stay in the local list only.

    python3 tools/media_webcopies.py FOLDER_ID /home/user/media-2026/srs-piedrahita [--day-re 'SRS_5_(T\\d+)'] [--jobs 3]

Originals never go to GitHub. The site repo never holds a photo: copies go only to paraglidingatlas-maker/media-2026.
"""
import argparse, concurrent.futures as cf, html, io, json, os, re, subprocess, sys, tempfile

from PIL import Image, ImageFilter, ImageOps, ImageStat

SIZES = (800, 1600, 2400)
QUALITY = {800: 78, 1600: 80, 2400: 82}


def listing(folder):
    """(drive id, title) for every file in a folder shared by link, from Drive's embedded folder view"""
    url = "https://drive.google.com/embeddedfolderview?id=" + folder
    s = subprocess.run(["curl", "-sSL", "--retry", "3", url], capture_output=True, check=True).stdout.decode("utf8")
    items = re.findall(r'<a href="https://drive.google.com/file/d/([\w-]+)/view[^"]*"[^>]*>.*?'
                       r'<div class="flip-entry-title">(.*?)</div>', s, re.S)
    return [(i, html.unescape(t)) for i, t in items]


def stem_of(title):
    """'SRS_5_T1 (46)-4.jpg' -> 'SRS_5_T1_46-4', the names the site already uses"""
    base = os.path.splitext(title)[0]
    return re.sub(r"\s*\((\d+)\)", r"_\1", base).replace(" ", "_")


def order(stem):
    m = re.search(r"_(\d+)(?:-(\d+))?$", stem)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else (10 ** 9, 0)


def shot_time(path):
    """the camera's DateTimeOriginal as 2026-08-26T14:03:22, or "" (EXIF sits at the start of a JPEG)"""
    try:
        with Image.open(path) as im:
            ex = im.getexif()
            t = ex.get_ifd(0x8769).get(36867) or ex.get(306) or ""
        return t[:10].replace(":", "-") + "T" + t[11:19] if len(t) >= 19 else ""
    except Exception:
        return ""


def head_shot(fid):
    """capture time of a Drive original without downloading it: a ranged read of its first 256 KB"""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
        url = "https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t" % fid
        subprocess.run(["curl", "-sSL", "--retry", "3", "-r", "0-262143", "-o", tmp.name, url], check=True)
        return shot_time(tmp.name)


def sharpness(im):
    """how sharp the photo is: the spread of the edge map of an 800 px grey copy (out-of-focus photos score low)"""
    g = im.convert("L"); g.thumbnail((800, 800))
    return round(ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).stddev[0], 2)


def one(fid, title, out, prefix=""):
    stem = prefix + stem_of(title)
    paths = [os.path.join(out, "%s-%d.webp" % (stem, w)) for w in SIZES]
    if all(os.path.exists(p) for p in paths):
        with Image.open(paths[-1]) as im:
            return stem, im.size, "kept", None, sharpness(im)
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
        url = "https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t" % fid
        subprocess.run(["curl", "-sSL", "--retry", "4", "--retry-delay", "3", "-o", tmp.name, url], check=True)
        shot = shot_time(tmp.name)
        with Image.open(tmp.name) as src:
            im = ImageOps.exif_transpose(src).convert("RGB")
    size = None
    for w, p in zip(SIZES, paths):
        c = im.copy()
        c.thumbnail((w, w), Image.LANCZOS)
        c.save(p + ".part", "WEBP", quality=QUALITY[w], method=5)
        os.replace(p + ".part", p)
        size = c.size
    return stem, size, "made", shot, sharpness(im)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("out")
    ap.add_argument("--day-re", default=r"_(T\d+)[ _(]")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--prefix", default="", help="with --day: the stems' prefix instead of the day (e.g. SRS_6_T3_ for camera names like IMG_8236)")
    ap.add_argument("--day", help="every photo in this folder is this day (T1, P ...); the stems get it as a prefix")
    ap.add_argument("--keep-names", action="store_true", help="with --day: keep the owner's file names (no day prefix)")
    ap.add_argument("--hold-below", type=float, default=0,
                    help="photos whose sharpness is under this are marked hold (kept off the page until the owner says)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = [(i, t) for i, t in listing(a.folder) if t.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff"))]
    print("%d photos in the folder" % len(files), flush=True)
    ids = {t: i for i, t in files}
    done, n = {}, 0
    old = {}
    try:
        old = {r["stem"]: r for r in json.load(open(os.path.join(a.out, "photos.json")))}
    except (OSError, ValueError):
        pass
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = {ex.submit(one, i, t, a.out, (a.prefix or a.day + "_") if a.day and not a.keep_names else ""): t for i, t in files}
        for f in cf.as_completed(futs):
            t = futs[f]
            try:
                stem, size, how, shot, sharp = f.result()
            except Exception as e:                       # one bad file never stops the rest; run again to retry it
                print("FAILED %s: %s" % (t, e), flush=True)
                continue
            m = None if a.day else re.search(a.day_re, t + " ")
            if shot is None:                             # a copy made on an earlier run: its time from then, else a ranged read
                shot = old[stem].get("shot", "") if stem in old else head_shot(ids[t])
            done[stem] = {"stem": stem, "day": a.day or (m.group(1) if m else ""), "w": size[0], "h": size[1], "shot": shot,
                          "sharp": sharp}
            if a.hold_below and sharp < a.hold_below and not old.get(stem, {}).get("shown"):
                done[stem]["hold"] = True
            n += 1
            if n % 10 == 0 or n == len(files):
                print("%d/%d (%s %s)" % (n, len(files), how, stem), flush=True)
    # by the number in the owner's file names: the Piedrahita originals' capture times read 31 Aug, after the comp
    # (22 to 29 Aug), so a camera clock or the export is off and "shot" is kept as data only, never shown or sorted on
    if a.day:      # one day's folder: the other days already in photos.json stay as they are
        done.update({k: v for k, v in old.items() if v.get("day") != a.day})
    rows = sorted(done.values(), key=lambda r: (r["day"], order(r["stem"])))
    with open(os.path.join(a.out, "photos.json"), "w") as fh:
        json.dump(rows, fh, separators=(",", ":"))
    print("photos.json: %d photos" % len(rows))
    print("held for a look (sharpness under %s): %d" % (a.hold_below, sum(1 for r in rows if r.get("hold"))))
    return 0 if len(done) >= len(files) else 1


if __name__ == "__main__":
    sys.exit(main())
