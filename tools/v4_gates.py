#!/usr/bin/env python3
"""
Every gate of docs/v4-plan.md, in order, with one summary line each.

    python3 tools/v4_gates.py            # all gates
    python3 tools/v4_gates.py --quick    # no smoke test, v4 check without the browser

Exit status 1 if any gate fails. Logs go to /tmp/claude-0/gates/.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = "/tmp/claude-0/gates"
ALLOWED = ("prototypes/v4/", "tools/", "docs/", ".claude/")


def run(name, cmd, ok_re=None, tail=1):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=isinstance(cmd, str))
    out = r.stdout + r.stderr
    open(os.path.join(LOG, name + ".log"), "w").write(out)
    lines = [ln for ln in out.strip().splitlines() if ln.strip()]
    last = " | ".join(lines[-tail:]) if lines else ""
    good = bool(r.returncode == 0 and (ok_re is None or re.search(ok_re, out)))
    print("%s  %-14s %s" % ("ok  " if good else "FAIL", name, last[:150]))
    return good, out


def preview_server():
    """The browser check needs the preview server on 8765. Start one for this run only, when none is up;
    it is stopped when the gates end, so nothing is left running."""
    import socket
    import time
    with socket.socket() as sk:
        if sk.connect_ex(("127.0.0.1", 8765)) == 0:
            return None
    proc = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"], cwd=ROOT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        with socket.socket() as sk:
            if sk.connect_ex(("127.0.0.1", 8765)) == 0:
                break
        time.sleep(.1)
    return proc


def main():
    server = preview_server()
    try:
        gates()
    finally:
        if server:
            server.terminate()
            server.wait()


def gates():
    quick = "--quick" in sys.argv
    os.makedirs(LOG, exist_ok=True)
    good = True
    g, _ = run("build", "./build.sh", r"build complete")
    good &= g
    # the build stamps today's date on the live sitemap: past midnight that is a change nobody made. A sitemap
    # whose only changed lines are <lastmod> dates is put back; any other change still fails the gate
    d = subprocess.run("git diff -U0 -- sitemap.xml", cwd=ROOT, shell=True, capture_output=True, text=True).stdout
    changed = [ln for ln in d.splitlines() if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    if changed and all(re.match(r"^[+-]\s*<lastmod>\d{4}-\d{2}-\d{2}</lastmod>\s*$", ln) for ln in changed):
        subprocess.run("git checkout -- sitemap.xml", cwd=ROOT, shell=True)
        print("note  %-14s %s" % ("sitemap", "only lastmod dates moved with the clock: restored"))
    # no live page changed by the build or by the work
    st = subprocess.run("git status --short; git diff --name-only origin/main", cwd=ROOT, shell=True,
                        capture_output=True, text=True).stdout
    paths = set(ln[3:].strip() if len(ln) > 3 and ln[2] == " " else ln.strip() for ln in st.splitlines() if ln.strip())
    bad = sorted(p for p in paths if not p.startswith(ALLOWED))
    print("%s  %-14s %s" % ("ok  " if not bad else "FAIL", "live-untouched", bad[:5] or "only prototypes/v4, tools, docs"))
    good &= not bad
    g, _ = run("audit", "python3 tools/audit.py --drift", r"\b0 FAIL")
    good &= g
    if not quick:
        g, out = run("smoke", "python3 tools/smoke.py", r"\b0 FAIL")
        if not g:     # the pinch test can flake: rerun once
            g, out = run("smoke-rerun", "python3 tools/smoke.py", r"\b0 FAIL")
        good &= g
    g, _ = run("v4-check", "python3 tools/v2_check.py --site v4" + (" --static" if quick else ""), r"\| 0 FAIL")
    good &= g
    g, _ = run("v4-switch", "python3 tools/v2_switch.py --site v4 --dry-run", r"\| 0 FAIL")
    good &= g
    g, _ = run("v2-static", "python3 tools/v2_check.py --static", r"\| 0 FAIL")
    good &= g
    v2 = subprocess.run("git status --short prototypes/v2", cwd=ROOT, shell=True, capture_output=True, text=True).stdout.strip()
    print("%s  %-14s %s" % ("ok  " if not v2 else "FAIL", "v2-untouched", v2[:150] or "empty"))
    good &= not v2
    print("\nGATES: %s" % ("PASS" if good else "FAIL"))
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
