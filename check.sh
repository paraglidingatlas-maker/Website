#!/usr/bin/env bash
# One command before you push.
#
#     ./check.sh
#
# Runs the three gates in the order that makes sense, stops at the first real
# failure, and exits non-zero so it can gate anything. Nothing here is new; it
# is build.sh, audit.py --drift and smoke.py with their results actually
# enforced instead of read.
#
# WHAT THIS CAN AND CANNOT DO
#
# It catches things that are malformed (audit: 104 checks over syntax, links,
# anchors, structure, tokens, copy) and things that are broken to use (smoke: 21
# checks that drive a real browser). It does not catch a decision that was wrong
# on purpose, and it never proves the absence of bugs. Every bug found on 14
# September passed the audit: the rail popup, the clipped player, the globe
# measured once, the pinch that was never wired up. Each was invisible to static
# checks and each now has a smoke check, which is the only reason they cannot
# come back quietly. Add one whenever something reaches you that this missed.
set -uo pipefail
cd "$(dirname "$0")"

BOLD=$'\033[1m'; RED=$'\033[31m'; GREEN=$'\033[32m'; DIM=$'\033[2m'; OFF=$'\033[0m'
fail=0

step() { printf "\n%s==> %s%s\n" "$BOLD" "$1" "$OFF"; }
bad()  { printf "%s    %s%s\n" "$RED" "$1" "$OFF"; fail=1; }
good() { printf "%s    %s%s\n" "$GREEN" "$1" "$OFF"; }

step "1/3  build"
if ./build.sh > /tmp/atlas-build.log 2>&1; then
  good "$(tail -1 /tmp/atlas-build.log)"
else
  bad "build.sh failed. Last lines:"
  tail -15 /tmp/atlas-build.log | sed 's/^/      /'
  printf "\n%sBuild failed, so nothing after it would mean anything. Stopping.%s\n" "$RED" "$OFF"
  exit 1
fi

# generate_episode_pages.py emits a page under a slug nothing links to. build.sh
# does not run it, but if it has been run by hand the stray file is still here
# and would be committed by a wide git add.
if [ -f episodes/watch-this-before-you-buy-a-paragliding-harness.html ]; then
  printf "%s    note: stray episodes/watch-this-before-you-buy-a-paragliding-harness.html present%s\n" "$DIM" "$OFF"
  printf "%s          slug mismatch with the committed -a-talk version, see TODO.md%s\n" "$DIM" "$OFF"
fi

step "2/3  audit: structure, links, tokens, copy, drift"
python3 tools/audit.py --drift > /tmp/atlas-audit.log 2>&1
grep -E "^FAIL" /tmp/atlas-audit.log | sed 's/^/      /'
if grep -qE "^FAIL" /tmp/atlas-audit.log; then
  bad "$(tail -1 /tmp/atlas-audit.log)"
else
  good "$(tail -1 /tmp/atlas-audit.log)"
  grep -E "^warn" /tmp/atlas-audit.log | sed "s/^/      ${DIM}/;s/$/${OFF}/"
fi

step "3/3  smoke: does the site actually work in a browser"
python3 tools/smoke.py > /tmp/atlas-smoke.log 2>&1
grep -E "^FAIL" /tmp/atlas-smoke.log | sed 's/^/      /'
if grep -qE "^FAIL" /tmp/atlas-smoke.log; then
  bad "$(tail -1 /tmp/atlas-smoke.log)"
elif grep -q "skipping interaction checks" /tmp/atlas-smoke.log; then
  printf "%s    skipped: %s%s\n" "$DIM" "$(grep 'skipping' /tmp/atlas-smoke.log)" "$OFF"
  printf "%s    nothing here was verified in a browser on this machine.%s\n" "$DIM" "$OFF"
else
  good "$(tail -1 /tmp/atlas-smoke.log)"
fi

step "what you are about to commit"
real=$(git diff -I'"dateModified"' --stat | tail -1)
untracked=$(git status --porcelain | grep -c '^??' || true)
printf "    %s\n" "${real:-no tracked changes}"
printf "    %s new file(s) not yet tracked\n" "$untracked"
printf "%s    dateModified churn is filtered out. To see it yourself:%s\n" "$DIM" "$OFF"
printf "%s      git diff -I'\"dateModified\"'%s\n" "$DIM" "$OFF"

if [ "$fail" -ne 0 ]; then
  printf "\n%sSomething failed. Full output in /tmp/atlas-audit.log and /tmp/atlas-smoke.log%s\n" "$RED" "$OFF"
  exit 1
fi
printf "\n%sAll three gates clean. Safe to push.%s\n" "$GREEN" "$OFF"
