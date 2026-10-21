#!/usr/bin/env python3
"""Open-source photographs for the landmarks of the India flight (option E).

    python3 tools/fetch_landmarks.py [--dry-run] [--only B26,B22]

Reads tools/data/india-landmarks.json, asks the Wikimedia Commons API about the
files named there (and, when they are too few, the files in the place's category
or a search), keeps only files under CC0, public domain, CC BY or CC BY-SA terms
that are at least 1200 px wide and wider than tall, downloads the best two per
place at 1600 px, and writes them as WebP to
prototypes/v4/img/india/landmarks/{1400,700}/<code>-<n>.webp with each file's
author, licence and page in tools/data/india-landmarks-credits.json. The build
(tools/v4_india_e.py) shows only the files that exist and names their authors.
Hosts needed: commons.wikimedia.org and upload.wikimedia.org (thumbnails are asked
from the upload host too, which serves them as well as thumb.wikimedia.org does)."""
import io, json, os, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "data", "india-landmarks.json")
CREDITS = os.path.join(ROOT, "tools", "data", "india-landmarks-credits.json")
OUT = os.path.join(ROOT, "prototypes", "v4", "img", "india", "landmarks")
API = "https://commons.wikimedia.org/w/api.php"
UA = "ParaglidingAtlas/1.0 (https://paraglidingatlas.com; site build) python-urllib"
OK_LICENCE = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)?( \d(\.\d)?)?)", re.I)
BAD_LICENCE = re.compile(r"NC|ND|GFDL only|Fair use", re.I)
MIN_W, PER_PLACE, FETCH_W = 1200, 2, 1920      # Commons serves a fixed set of widths; 1920 is one of them


def ctx():
    c = ssl.create_default_context()
    for f in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"), "/root/.ccr/ca-bundle.crt"):
        if f and os.path.exists(f):
            c.load_verify_locations(f)
    return c


def get(url, binary=False):
    """one request; Wikimedia rate-limits shared addresses hard, so a 429 waits as long as it asks and tries again"""
    for attempt in range(10):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60, context=ctx()) as r:
                b = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 9:
                try: wait = int(e.headers.get("Retry-After") or 5)
                except ValueError: wait = 5
                time.sleep(wait + 2 + attempt * 3); continue
            raise
    time.sleep(2.5)                                           # politely spaced
    return b if binary else json.loads(b.decode("utf-8"))


def api(**params):
    params.update(action="query", format="json", formatversion="2")
    return get(API + "?" + urllib.parse.urlencode(params))


def plain(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def info(titles):
    """imageinfo for up to 50 File: titles -> {title: dict}"""
    out = {}
    for i in range(0, len(titles), 50):
        r = api(prop="imageinfo", iiprop="url|size|mime|extmetadata", iiurlwidth=str(FETCH_W),
                iiextmetadatafilter="Artist|LicenseShortName|LicenseUrl|Credit|ImageDescription|Restrictions",
                titles="|".join(titles[i:i + 50]))
        for p in r["query"].get("pages", []):
            if p.get("missing") or not p.get("imageinfo"):
                continue
            ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
            v = lambda k: em.get(k, {}).get("value", "")
            out[p["title"]] = dict(title=p["title"], w=ii.get("width", 0), h=ii.get("height", 0), mime=ii.get("mime", ""),
                                   thumb=(ii.get("thumburl") or ii.get("url")).replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/"), page=ii.get("descriptionurl", ""),
                                   author=plain(v("Artist")), licence=plain(v("LicenseShortName")), licence_url=v("LicenseUrl"),
                                   desc=plain(v("ImageDescription"))[:200], restrictions=v("Restrictions"))
    return out


def usable(f):
    if not OK_LICENCE.match(f["licence"]) or BAD_LICENCE.search(f["licence"]):
        return False
    if f["mime"] not in ("image/jpeg", "image/png"):
        return False
    return f["w"] >= MIN_W and f["w"] > f["h"] * 1.1


def candidates(place, enough):
    """the named files; then the category's files and a search, each only while fewer than `enough` are usable"""
    seen, out, files = set(), [], {}
    def add(titles):
        titles = [t.replace("_", " ") for t in titles]              # the API answers with spaces
        new = [t for t in titles if t not in seen]
        for t in new: seen.add(t); out.append(t)
        if new: files.update(info(new))
    def usable_n(): return sum(1 for t in out if t in files and usable(files[t]))
    add(["File:" + t for t in place.get("files", [])])
    if usable_n() < enough and place.get("category"):
        r = api(list="categorymembers", cmtitle="Category:" + place["category"], cmtype="file", cmlimit="40")
        add([m["title"] for m in r["query"].get("categorymembers", [])])
    if usable_n() < enough and place.get("search"):
        r = api(list="search", srnamespace="6", srsearch=place["search"], srlimit="30")
        add([m["title"] for m in r["query"].get("search", [])])
    return out, files


def save(b, code, n):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(b))).convert("RGB")
    for w in (1400, 700):
        d = os.path.join(OUT, str(w)); os.makedirs(d, exist_ok=True)
        r = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
        r.save(os.path.join(d, "%s-%d.webp" % (code, n)), "WEBP", quality=82, method=6)


def main():
    dry = "--dry-run" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    places = json.load(open(DATA))["places"]
    credits = json.load(open(CREDITS)) if os.path.exists(CREDITS) else {}
    for code, place in places.items():
        if only and code not in only:
            continue
        titles, files = candidates(place, PER_PLACE)
        good = [files[t] for t in titles if t in files and usable(files[t])]
        named = ["File:" + t.replace("_", " ") for t in place.get("files", [])]   # the API answers with spaces, whatever was asked
        good.sort(key=lambda f: (named.index(f["title"]) if f["title"] in named else 99, -f["w"]))
        pick = good[:PER_PLACE]
        print("%s %-34s %d candidates, %d usable -> %s" % (code, place["title"], len(titles), len(good), ", ".join(f["title"] for f in pick) or "none"))
        if dry or not pick:
            continue
        credits[code] = []
        for n, f in enumerate(pick, 1):
            save(get(f["thumb"], binary=True), code, n)
            credits[code].append(dict(n=n, file=f["title"], author=f["author"], licence=f["licence"], licence_url=f["licence_url"], page=f["page"], w=f["w"], h=f["h"], desc=f["desc"]))
        json.dump(credits, open(CREDITS, "w"), indent=1, ensure_ascii=False)
    if not dry:
        print("credits ->", os.path.relpath(CREDITS, ROOT))


if __name__ == "__main__":
    main()
