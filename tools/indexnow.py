#!/usr/bin/env python3
"""Tell Bing (and Yandex, Naver, Seznam) which pages changed, via IndexNow.

Why: Bing's manual URL Submission has a daily quota and needs a human. IndexNow
is one POST per deploy and covers every engine that speaks the protocol.
ChatGPT search reads Bing's index, so this is also the fastest way into it.

    python3 tools/indexnow.py                 # pages changed in the last commit
    python3 tools/indexnow.py BEFORE AFTER    # pages changed between two shas
    python3 tools/indexnow.py --all           # everything in sitemap.xml
    python3 tools/indexnow.py --dry-run ...   # print the payload, send nothing
    python3 tools/indexnow.py --write-key     # (re)write the key file at root

The key file <KEY>.txt at the site root is how the engines verify ownership.
build.sh calls --write-key so it can never go missing. Run this AFTER the pages
are live: engines fetch the URLs you send, and a 404 is a wasted submission.
"""
import json, os, subprocess, sys, urllib.request

_R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _R)
import site_config as cfg

KEY = cfg.INDEXNOW_KEY
KEY_FILE = os.path.join(_R, KEY + ".txt")
ENDPOINT = "https://api.indexnow.org/indexnow"
SKIP = ("prototypes/", "templates/", "tools/", "transcripts/")


def write_key():
    if not (os.path.exists(KEY_FILE) and open(KEY_FILE).read().strip() == KEY):
        open(KEY_FILE, "w").write(KEY + "\n")


def url_for(path):
    path = path.replace(os.sep, "/")
    if path == "index.html":
        return cfg.BASE
    return cfg.BASE + path


def indexable(path):
    if not path.endswith(".html") or path.startswith(SKIP):
        return False
    try:
        head = open(os.path.join(_R, path), encoding="utf-8", errors="replace").read(4000)
    except OSError:
        return False                       # deleted pages are not submitted
    return "noindex" not in head


def changed(before, after):
    if before is None:
        rng = "%s~1..%s" % (after, after)
    elif set(before) == {"0"}:
        return None                        # first push to a branch: send all
    else:
        rng = "%s..%s" % (before, after)
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", rng], cwd=_R,
                                      text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None                        # unknown sha (shallow clone): send all
    return [p for p in out.split() if indexable(p)]


def from_sitemap():
    import re
    xml = open(os.path.join(_R, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def send(urls, dry):
    urls = sorted(set(urls))[:10000]
    if not urls:
        print("indexnow: nothing to submit")
        return
    body = {"host": cfg.DOMAIN, "key": KEY,
            "keyLocation": cfg.BASE + KEY + ".txt", "urlList": urls}
    print("indexnow: %d url(s)" % len(urls))
    for u in urls:
        print("  " + u)
    if dry:
        return
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("indexnow: HTTP %s" % r.status)
    except urllib.error.HTTPError as e:
        # 200/202 accepted; 422 = url outside host; 429 = slow down. Never fail the deploy.
        print("indexnow: HTTP %s %s" % (e.code, e.read().decode(errors="replace")[:200]))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = set(a for a in sys.argv[1:] if a.startswith("--"))
    write_key()
    if "--write-key" in flags and not args and "--all" not in flags:
        sys.exit(0)
    if "--all" in flags:
        urls = from_sitemap()
    else:
        before, after = (args[0], args[1]) if len(args) >= 2 else (None, args[0] if args else "HEAD")
        paths = changed(before, after)
        urls = from_sitemap() if paths is None else [url_for(p) for p in paths]
    send(urls, "--dry-run" in flags)
