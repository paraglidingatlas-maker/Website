#!/usr/bin/env python3
"""
The v2 switch-over: put every v2 page in the place of the live page it
replaces. PREPARED, NOT PERFORMED: the real run replaces paraglidingatlas.com
and waits for the owner's go (docs/v2-report.md has the runbook).

What one run does, to a site root (the repo, or a staging copy of it):

  1. every page in prototypes/v2/ except the prototype-only ones
     (styleguide.html, fly-options.html) is written to the same path at the
     root, over the live page;
  2. its links are turned back: a link to another v2 page points at that
     page's live address, a link to a v2 file (v2.css, v2.js, img/...) points
     at assets/v2/, and a link to a live file stays on that file;
  3. the prototype's noindex is taken out; the page keeps exactly the robots
     line the live page had (the 404 keeps its own noindex);
  4. the v2 styles, scripts and images are copied to assets/v2/.

Nothing else at the root is touched: the redirect stubs, sitemap.xml,
robots.txt, llms.txt, the feed and every asset stay as they are.

Because build.sh regenerates the episode, knowledge base, policy, tag, 404
and library pages in the old design, the switch is a step that runs at the
END of every build (after the live generators), not a one-off copy; the
v2 generators read the freshly generated live pages as their input.

    python3 tools/v2_switch.py --dry-run [--stage DIR]   # staging copy + checks
    python3 tools/v2_switch.py --apply --out _site       # the switched site, for publishing
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_site as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = S.DIR
ABSOLUTE = {"404.html"}                 # GitHub Pages serves it for any missing path
ASSET_DIR = S.ASSET_DIR
NOINDEX = '<meta name="robots" content="noindex, nofollow">\n'
SKIP = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/|\{|\$|%|data:)", re.I)
ATTR = re.compile(r'(\s(?:href|src|poster|data-src|data-poster|data-loop)=")([^"]*)(")', re.I)
SRCSET = re.compile(r'(\s(?:srcset|data-srcset)=")([^"]*)(")', re.I)
CSSURL = re.compile(r'(url\((["\']?))([^)"\']+)(\2\))')
V2_FILE = re.compile(r"\.(css|js|webp|jpg|jpeg|png|svg|gif|avif|json|woff2?)$", re.I)


def v2_pages():
    out = []
    for d, _, fs in os.walk(V2):
        for f in fs:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(d, f), V2).replace(os.sep, "/")
                if not S.proto_only(rel):
                    out.append(rel)
    return sorted(out)


def all_pages():
    out = []
    for d, _, fs in os.walk(V2):
        for f in fs:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(d, f), V2).replace(os.sep, "/"))
    return out


def v2_assets():
    out = []
    for d, _, fs in os.walk(V2):
        for f in fs:
            if V2_FILE.search(f):
                out.append(os.path.relpath(os.path.join(d, f), V2).replace(os.sep, "/"))
    return sorted(out)


def remap(url, page_rel, pages):
    """A link as written in prototypes/v2/<page_rel> -> the same link from <root>/<page_rel>."""
    if not url or SKIP.match(url):
        return url
    m = re.match(r"([^?#]*)(.*)$", url)
    path, tail = m.group(1), m.group(2)
    if not path:
        return url
    here = os.path.dirname(os.path.join(V2, page_rel))
    target = os.path.normpath(os.path.join(here, path))
    rel_v2 = os.path.relpath(target, V2).replace(os.sep, "/")
    if not rel_v2.startswith(".."):
        if rel_v2 in pages or rel_v2.endswith("/") or os.path.isdir(target):
            new = os.path.join(ROOT, rel_v2)                 # another v2 page -> its live address
        else:
            new = os.path.join(ROOT, ASSET_DIR, rel_v2)      # a v2 file -> assets/v2/
    else:
        new = target                                         # already a live file
    if page_rel in ABSOLUTE:        # served at any depth by the host: root-absolute links
        out = "/" + os.path.relpath(new, ROOT).replace(os.sep, "/")
    else:
        out = os.path.relpath(new, os.path.dirname(os.path.join(ROOT, page_rel))).replace(os.sep, "/")
    if path.endswith("/") and not out.endswith("/"):
        out += "/"
    return out + tail


def transform(rel, pages):
    with open(os.path.join(V2, rel), encoding="utf-8") as fh:
        src = fh.read()
    src = ATTR.sub(lambda m: m.group(1) + remap(m.group(2), rel, pages) + m.group(3), src)
    src = SRCSET.sub(lambda m: m.group(1) + ", ".join(
        " ".join([remap(c.strip().split(" ")[0], rel, pages)] + c.strip().split(" ")[1:])
        for c in m.group(2).split(",") if c.strip()) + m.group(3), src)
    src = CSSURL.sub(lambda m: m.group(1) + remap(m.group(3), rel, pages) + m.group(4), src)
    # robots: exactly what the live page had
    live = os.path.join(ROOT, rel)
    live_src = open(live, encoding="utf-8").read() if os.path.exists(live) else ""
    live_robots = re.findall(r'<meta name="robots"[^>]*>', live_src)
    src = src.replace(NOINDEX, "", 1)
    have = re.findall(r'<meta name="robots"[^>]*>', src)
    if have != live_robots:
        src = re.sub(r'<meta name="robots"[^>]*>\n?', "", src)
        if live_robots:
            src = src.replace("<head>\n", "<head>\n" + "\n".join(live_robots) + "\n", 1)
    return src


def apply(root):
    pages = set(v2_pages()) | set(p for p in all_pages() if S.proto_only(p))
    for a in v2_assets():
        dst = os.path.join(root, ASSET_DIR, a)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(V2, a), dst)
    n = 0
    for rel in v2_pages():
        out = transform(rel, pages)
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        n += 1
    return n


def live_html(root):
    out = set()
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in (".git", "prototypes", "node_modules", "__pycache__", "templates", "tools", "docs")]
        for f in fs:
            if f.endswith(".html"):
                out.add(os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/"))
    return out


def dry_run(stage, build=False):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import v2_check as C
    if os.path.exists(stage):
        shutil.rmtree(stage)
    shutil.copytree(ROOT, stage, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
    before = live_html(ROOT)
    if build:     # the real pipeline: the live generators first, then the switch step
        r = subprocess.run(["bash", "build.sh"], cwd=stage, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("stage build.sh failed:\n" + r.stdout[-800:] + r.stderr[-800:])
    n = apply(stage)
    after = live_html(stage)
    fails, notes = [], []
    # 1. no URL lost, none added by accident
    if before - after:
        fails.append("pages lost: %s" % sorted(before - after)[:5])
    added = after - before
    if added:
        fails.append("pages added at the root: %s" % sorted(added)[:5])
    locs = re.findall(r"<loc>https://paraglidingatlas\.com/([^<]*)</loc>", open(os.path.join(stage, "sitemap.xml")).read())
    miss = [l for l in locs if not os.path.exists(os.path.join(stage, l or "index.html"))]
    if miss:
        fails.append("sitemap URLs without a page: %s" % miss[:5])
    # 2. SEO/GEO parity, robots and links, page by page against the live original
    exempt = C.EXEMPT
    for rel in sorted(v2_pages()):
        a = C.seo(open(os.path.join(ROOT, rel), encoding="utf-8").read())
        s_src = open(os.path.join(stage, rel), encoding="utf-8").read()
        b = C.seo(s_src)
        for k in ("title", "description", "canonical", "og:title", "og:description", "og:image", "twitter:card", "jsonld", "episode"):
            if a[k] != b[k]:
                fails.append("%s: %s differs" % (rel, k))
        if b["words"] < a["words"] * 0.95 and "words" not in exempt.get(rel, {}):
            fails.append("%s: body text %d words, live %d" % (rel, b["words"], a["words"]))
        if b["chapters"] < a["chapters"]:
            fails.append("%s: chapters %d, live %d" % (rel, b["chapters"], a["chapters"]))
        lr = re.findall(r'<meta name="robots"[^>]*>', open(os.path.join(ROOT, rel), encoding="utf-8").read())
        sr = re.findall(r'<meta name="robots"[^>]*>', s_src)
        if lr != sr:
            fails.append("%s: robots %s, live %s" % (rel, sr, lr))
        if "prototypes/" + S.NAME in re.sub(r"<!--.*?-->", "", s_src, flags=re.S).replace("prototypes/v2/ only", ""):
            notes.append("%s: still mentions prototypes/%s" % (rel, S.NAME))
        # every relative link resolves inside the staging site
        here = os.path.dirname(os.path.join(stage, rel))
        refs = [m.group(2) for m in ATTR.finditer(s_src)] + [u.strip().split(" ")[0] for m in SRCSET.finditer(s_src) for u in m.group(2).split(",")]
        bad = set()
        for u in refs:
            u = html.unescape(u).strip()
            if not u or SKIP.match(u):
                continue
            f = u.split("#")[0].split("?")[0]
            if not f:
                continue
            t = os.path.normpath(os.path.join(here, f))
            if 'data-loop="%s"' % u in s_src:          # a looping-video prefix, not a file
                t = t + "-720.mp4"
            if os.path.isdir(t):
                t = os.path.join(t, "index.html")
            if not os.path.exists(t):
                bad.add(u)
        if bad:
            fails.append("%s: %d links missing, e.g. %s" % (rel, len(bad), sorted(bad)[:2]))
    # 3. the live site's own audit, run on the switched staging site
    r = subprocess.run([sys.executable, "tools/audit.py"], cwd=stage, capture_output=True, text=True)
    for ln in r.stdout.splitlines():
        if ln.startswith("FAIL"):
            fails.append("live audit: " + ln[5:].strip())
    return n, fails, notes


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    ap.add_argument("--stage", default=S.STAGE)
    ap.add_argument("--out", help="apply: write the switched site into this folder (a copy of the repo), never over the repo")
    ap.add_argument("--build", action="store_true", help="dry run: run build.sh in the stage first, as the real pipeline would")
    a = ap.parse_args()
    if a.apply:
        # the repo itself is never switched in place: the next build.sh would put
        # the old design back (and stops at the library markers). The switched site
        # is written to a separate folder, which is what gets published.
        if not a.out or os.path.abspath(a.out) == ROOT:
            raise SystemExit("--apply needs --out <folder>; the repo root is never switched in place")
        if os.path.exists(a.out):
            shutil.rmtree(a.out)
        shutil.copytree(ROOT, a.out, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules", "prototypes", "tools", "docs", "templates", "*.py", ".claude", ".github"))
        n = apply(a.out)
        print("switched site written to %s (%d pages)" % (a.out, n))
        return
    n, fails, notes = dry_run(a.stage, a.build)
    for x in fails:
        print("FAIL ", x)
    for x in notes:
        print("note ", x)
    print("\nswitch dry run: %d pages written into %s | %d FAIL | %d notes" % (n, a.stage, len(fails), len(notes)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
