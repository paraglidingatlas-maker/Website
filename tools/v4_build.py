#!/usr/bin/env python3
"""
Rebuild prototypes/v4/ after the live build: every v4 generator and pass, in
the order that reproduces the committed pages byte for byte.

    ./build.sh && python3 tools/v4_build.py

The live build (./build.sh) regenerates the episode, knowledge base, policy,
tag, 404 and library pages from data; this carries the new data into v4. Each
step is a "python3 tools/..." subprocess (the Python running this script) run
from the repo root; every step is printed, and the build stops at the first
one that fails. Checked at c2751f9d: on a clean checkout "git status --short
prototypes/v4" is empty afterwards, and a second run changes nothing.

What it reads and writes: besides Python, its packages and git, it reads the
repo only (the live build's output, the committed v4 pages, tools/ and
tools/data/); it opens no network connection and reads nothing in /tmp. It
writes pages and files inside
prototypes/v4/ only, never prototypes/v2/ and never a live page. Outside it,
Python leaves its usual (gitignored) __pycache__/ folders under tools/; and
tools/v4_phone_media.py, only when a phone clip is missing, needs ffmpeg
(which the deploy workflow does not install) and keeps ffmpeg's two-pass logs
in /tmp/v4pm-<clip>. At c2751f9d every clip is committed, so no clip is cut
and nothing goes to /tmp. (The Navigators map in v4_pass used to fetch its
Natural Earth countries with pip into /tmp and read them with pyshp, and drew
a different map without them; tools/kbfig/nav_land.py now reads the same file
from tools/data/naturalearth_lowres.shp with the standard library.)

Needs: Python 3.11 with Pillow, numpy and contourpy (v4_pass draws the
knowledge base lens figures through v4_lens and v4_expert; v4_pwa and v4_ux
use Pillow). Byte identity was checked with Pillow 12.3.0, numpy 2.4.6 and
contourpy 1.3.3, the versions docs/v4-deploy-workflow.yml pins: v4_pwa
re-encodes the app icons and v4_pass computes the figures, so other versions
may change bytes. git, for the check below (without git it is skipped);
ffmpeg only when a phone clip is missing.

The pages their own generators own (samples/**, record-*.html,
expeditions*.html: step 11) are put back after the page passes as this found
them; only the app block (v4_pwa) and the ?v= hashes (version_assets) still
reach them, as they reach every page. So it first checks them against git's
index, read only, and stops before any step if one differs in more than its
?v= hashes: a chain step run on its own (v2_localize, v4_award, v4_library,
or v4_ux with no page list) or a hard kill of this script leaves the chain's
marks on them, and this cannot tell those from a generator's new output. A
hash alone is not such a mark: ./build.sh re-versions every page whenever a
file they link changes (a new episode changes library-episodes.js), and that
must never stop a deploy. The message names the pages; restore them with git
checkout, or git add the ones that are new output on purpose. Where git
cannot be asked (a copy of the site without its history, or git failing),
the check is skipped and says so. A run that fails or is stopped still puts
those pages back as it found them, and a new episode or twin page whose step
failed (an episode page that came out without its hero and player, say) is
removed again. A stop signal (SIGINT, SIGTERM, SIGHUP) sent to this script
lets the running step finish, so no page is left half written, and then
stops; Ctrl-C at a terminal reaches the running step as well. The other
pages may be left part-way through the chain; every step converges, so the
next run finishes them.

What follows the live data: the library's cards and flight log, the
podcast's wall of guests and newest episode, the topics' traces and the
search files are rebuilt from the data, and a new topic, knowledge base or
text page gets its v4 twin (tools/v2_twin.py). A new episode does NOT, yet:
tools/v2_episode.py cannot read the live episode header since 2 Oct (step
2), so a new episode in episode-meta.json stops this build, on purpose,
rather than ship an episode page without its hero and player. What does not
follow: the v4 episode, knowledge base, topic and text pages that exist
already, and the pages that list episodes on them. They carry the live
pages' dateModified of 25 Sep 2026 and v4's later passes and hand edits, so
rebuilding them from today's live pages (tools/v2_episode.py --site v4
--all, tools/v2_twin.py --site v4) would undo weeks of work; a change to one
of them is made in v4 itself.

THE ORDER, AND WHY
  1. v4_phone_media        the phone cuts v4_ux needs (writes only what is
                           missing). First, because it reads only the
                           committed trip and home pages and the live
                           artwork: when it fails (a missing clip and no
                           ffmpeg) no page has been touched yet.
  2. v2_episode, v2_twin   only for the pages v4 does not have yet. A new
                           episode page must come out with its hero and
                           player, or it is removed and the build stops:
                           since 2 Oct the live episode header opens on
                           <a class="cd-series">, not <p class="cd-epno">,
                           and v2_episode then drops both without a word, so
                           it has to learn the new header before a new
                           episode can be built.
  3. v2_library_cards      the library's cards, from library-data.js; before
     v4_library            the flight log, which adds its columns to them.
  4. v4_pass               nav, next step, titles, globes, kb figures and the
                           rest; after the generators. It redraws the kb
                           drawings in long path syntax, which v4_ux compacts.
  5. v4_catchup marks      only series_marks(): the Gold series mark beside an
                           episode number, after v4_pass's globe line. The
                           homepage globe and sitemap sky of v4_catchup.py are
                           left out: once v4_ux has run they do not come back
                           the same, and neither page is rebuilt here.
  6. v4_footage, v4_award, v4_topics
                           page passes on the twins and hubs; after v4_pass
                           (v4_award keeps its booking band whole) and before
                           v4_ux.
  7. v2_localize           links pointed at the v4 twin or the live file, the
                           noindex and the v2 tags; before v4_ux (its CSS goes
                           after the v2.css link) and v4_pwa (its head block
                           goes after the v2 scripts). Its live-canonical
                           check passes over the prototype-only pages, as
                           tools/v2_check.py does (samples/rss-options.html
                           has no canonical), so it exits 0 on a sound tree.
  8. v4_ux                 the usability pass, on every page but the pages
                           their own generators own (below).
     v4_trip_calm india    India's less-but-better pass (step 33): v4_ux
                           puts back two blocks it trims (the pinned
                           gallery's phone rules and the hero slideshow's
                           waker), so it runs after v4_ux; idempotent.
     v4_partners           Partners' less-but-better pass (step 34): after
                           v4_ux, like India's; it rewrites only its own
                           marks and the page's own <style>; idempotent.
     v4_sitemap_sky        the sitemap's night sky from real stars (step 35):
                           img/sitemap-stars.svg and one <style> in the
                           sitemap's head; after v4_ux; idempotent.
     v4_polish             the awwwards-direction polish (step 36), one
                           page's own <style> at a time; after v4_ux;
                           idempotent.
     v4_nav_record         the record attempt in every header (step 40),
                           between v4:needs marks; after v4_ux; idempotent.
  9. v4_search             the search files, read from the finished pages.
 10. v4_min                v2.css and the scripts, from src/.
 11. (put back)            the pages their own generators own, as they were
                           before this ran: samples/**, record-*.html and
                           expeditions*.html. v4_library, v4_award and
                           v2_localize touch them in passing; their own
                           generators (tools/v4_samples.py, v4_record*.py,
                           v4_expeditions*.py, ...) are not part of this, so
                           the page passes never reach these pages, and what
                           v4_library writes to samples/library-wall.html or
                           v4_award to expeditions.html is thrown away: their
                           content changes only when their own generator is
                           run by hand (steps 12 and 13 still give them the
                           app block and the ?v= hashes).
 12. v4_pwa                the app files and the app block on every page;
                           after the last page pass and v2_localize.
 13. version_assets        the ?v= hashes, last.

Left out on purpose: v4_trip, v4_flythrough and v4_tripmap (their source,
prototypes/v2/, is frozen; a rebuild drops the trips' hand edits),
v4_404_options --install (it deletes the end of src/v2.css), v4_kbsvg and
v4_lens/v4_darkside main (img/kb/ is committed and redrawn only when a figure
script changes), v4_opening, and every sample and option generator.
"""
import json
import os
import re
import signal
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
PY = sys.executable or "python3"     # the steps run in this script's own Python (numpy, contourpy, Pillow)


def rel(p):
    return os.path.relpath(p, V4).replace(os.sep, "/")


def owned():
    """The pages their own generators own: every file under samples/, and the
    record and expeditions pages (and their options) at the top."""
    out = []
    for d, _, fs in os.walk(os.path.join(V4, "samples")):
        out += [os.path.join(d, f) for f in fs]
    out += [os.path.join(V4, f) for f in os.listdir(V4)
            if f.endswith(".html") and (f.startswith("record-") or f.startswith("expeditions"))]
    return sorted(out)


def ux_pages():
    """Every v4 page v4_ux owns: all but src/, samples/ and the owned pages."""
    skip = set(owned())
    out = []
    for d, dirs, fs in os.walk(V4):
        dirs[:] = [x for x in dirs if x not in ("src", "samples")]
        out += [rel(os.path.join(d, f)) for f in fs if f.endswith(".html") and os.path.join(d, f) not in skip]
    return sorted(out)


def new_episodes():
    """Episodes in episode-meta.json that have no v4 page yet."""
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    return sorted(m["slug"] for m in meta
                  if not os.path.exists(os.path.join(V4, "episodes", m["slug"] + ".html")))


def new_twins():
    """Live knowledge base, topic and text pages that have no v4 twin yet."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from v2_twin import everything   # noqa: E402  (the pages v2_twin builds with no argument)
    return [r for r in everything() if not os.path.exists(os.path.join(V4, r))]


STOP = []     # the signal that asked this run to stop, once one has


def stopped(sig, frame):
    """Ctrl-C, SIGTERM or SIGHUP: the step that is running finishes (so no page is
    left half written), then the build stops and the owned pages go back."""
    STOP.append(sig)


def run(args):
    """One step: print it, run it from the repo root, stop the build if it fails."""
    if STOP:
        raise SystemExit("v4_build: stopped (signal %d)" % STOP[0])
    shown = ["python3"] + args[1:] if args[0] == PY else args
    print("== " + " ".join(shown if len(" ".join(shown)) < 160 else shown[:3] + ["... (%d pages)" % (len(shown) - 3)]),
          flush=True)
    r = subprocess.run(args, cwd=ROOT)
    if STOP:
        raise SystemExit("v4_build: stopped (signal %d)" % STOP[0])
    if r.returncode:
        raise SystemExit("v4_build: step failed (exit %d): %s" % (r.returncode, " ".join(shown[:3])))


def generate(step, args, pages, check=None):
    """Build the pages v4 does not have yet; if the step or its check fails, remove
    what it wrote, so the next run sees them missing and tries again."""
    try:
        run(step + args)
        if check:
            check(pages)
    except BaseException:
        for r in pages:
            if os.path.exists(os.path.join(V4, r)):
                os.remove(os.path.join(V4, r))
                print("   removed " + r, flush=True)
        raise


def check_episodes(pages):
    """A new episode page must have its hero and player (v2_episode drops both, silently,
    when it cannot read the live header)."""
    bad = []
    for r in pages:
        page = open(os.path.join(V4, r), encoding="utf-8").read()
        if not ('class="ep2-hero' in page and 'class="cd-player' in page):
            bad.append(r)
    if bad:
        raise SystemExit("v4_build: v2_episode built no hero or player for %s; the live episode header "
                         "has changed (tools/v2_episode.py head_re), fix the generator first" % ", ".join(bad))


VER = re.compile(rb"\?v=[0-9a-f]{8}\b")     # a ?v= hash, as tools/version_assets.py writes it
OWNED_GIT = ["prototypes/v4/samples/", ":(glob)prototypes/v4/record-*.html",
             ":(glob)prototypes/v4/expeditions*.html"]     # owned(), as git pathspecs


def changed_owned():
    """The owned pages whose bytes differ from git's index (or that are missing), or
    None when there is no git to ask (a copy of the site without its history). Read
    only: it compares blob ids (git ls-files, git hash-object without -w), where
    "git diff" would refresh and rewrite the index."""
    try:
        ls = subprocess.run(["git", "ls-files", "-s", "-z", "--"] + OWNED_GIT, cwd=ROOT, capture_output=True)
        if ls.returncode:
            return None
        index = {}
        for entry in ls.stdout.decode("utf-8").split("\0"):
            if entry:
                info, path = entry.split("\t", 1)
                index[path] = info.split()[1]
        here = sorted(p for p in index if os.path.isfile(os.path.join(ROOT, p)))
        h = subprocess.run(["git", "hash-object", "--stdin-paths"], cwd=ROOT, capture_output=True,
                           input="".join(p + "\n" for p in here).encode("utf-8"))
        if h.returncode:
            return None
    except OSError:
        return None
    now = dict(zip(here, h.stdout.decode("ascii").split()))
    out = []
    for p in sorted(index):
        if now.get(p) == index[p]:
            continue
        if p in now:
            # differs only in its ?v= hashes: ./build.sh re-versions every page when a file it
            # links changes, which is no mark of a chain step (read the committed blob, read only)
            b = subprocess.run(["git", "cat-file", "blob", index[p]], cwd=ROOT, capture_output=True)
            if b.returncode == 0:
                with open(os.path.join(ROOT, p), "rb") as fh:
                    if VER.sub(b"", fh.read()) == VER.sub(b"", b.stdout):
                        continue
        out.append(p)
    return out


def put_back(keep):
    """Write the owned pages back as they were when this run began."""
    print("== put back the pages their own generators own (%d files)" % len(keep), flush=True)
    for p, b in keep.items():
        try:
            with open(p, "rb") as fh:
                same = fh.read() == b
        except FileNotFoundError:
            same = False
        if not same:
            with open(p, "wb") as fh:
                fh.write(b)
            print("   " + rel(p), flush=True)


def main():
    os.chdir(ROOT)
    for name in ("SIGINT", "SIGTERM", "SIGHUP"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), stopped)
    # The owned pages are kept as this run finds them, so they must be as committed
    # (or as staged) to begin with: a chain step run on its own (v2_localize, v4_award,
    # v4_library, v4_ux without a page list) or a hard kill leaves its marks on them,
    # and this cannot tell those marks from a generator's new output.
    changed = changed_owned()
    if changed is None:
        print("== no git here: the pages their own generators own are kept as they are", flush=True)
    elif changed:
        raise SystemExit(
            "v4_build: these pages, which their own generators own, differ from git's index:\n  %s\n"
            "A chain step run on its own changes them (v2_localize, v4_award, v4_library, or v4_ux\n"
            "without a page list), and so does a hard kill of this script. Nothing has been run.\n"
            "If they are not your own new output, restore them, then run again:\n"
            "  git checkout -- %s\n"
            "If they are (their generator was run on purpose), git add them first; this then keeps them."
            % ("\n  ".join(changed), " ".join(changed)))
    keep = {p: open(p, "rb").read() for p in owned()}
    put = False
    try:
        run([PY, "tools/v4_phone_media.py"])

        eps = new_episodes()
        if eps:
            generate([PY, "tools/v2_episode.py", "--site", "v4"], eps, ["episodes/%s.html" % s for s in eps],
                     check=check_episodes)
        else:
            print("== v2_episode: every episode has its v4 page", flush=True)
        twins = new_twins()
        if twins:
            generate([PY, "tools/v2_twin.py", "--site", "v4"], twins, twins)
        else:
            print("== v2_twin: every page has its v4 twin", flush=True)

        run([PY, "tools/v2_library_cards.py", "--site", "v4"])
        run([PY, "tools/v4_library.py"])
        run([PY, "tools/v4_pass.py"])
        run([PY, "-c", "import sys; sys.path.insert(0, 'tools'); import v4_catchup; v4_catchup.series_marks()"])
        run([PY, "tools/v4_footage.py"])
        run([PY, "tools/v4_award.py"])
        run([PY, "tools/v4_topics.py"])
        run([PY, "tools/v2_localize.py", "--site", "v4"])
        run([PY, "tools/v4_ux.py"] + ux_pages())
        run([PY, "tools/v4_trip_calm.py", "india"])
        run([PY, "tools/v4_partners.py"])
        run([PY, "tools/v4_sitemap_sky.py"])
        run([PY, "tools/v4_polish.py"])
        run([PY, "tools/v4_nav_record.py"])
        run([PY, "tools/v4_search.py"])
        run([PY, "tools/v4_min.py"])

        put_back(keep)
        put = True
        run([PY, "tools/v4_pwa.py"])
        run([PY, "tools/version_assets.py"])
    finally:
        if not put:
            # a failed or stopped run: the owned pages go back as they were, so the
            # next run does not take the chain's marks on them for the real thing
            put_back(keep)
    print("v4 build complete")


if __name__ == "__main__":
    main()
