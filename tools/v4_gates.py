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


def main():
    quick = "--quick" in sys.argv
    os.makedirs(LOG, exist_ok=True)
    good = True
    g, _ = run("build", "./build.sh", r"build complete")
    good &= g
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
