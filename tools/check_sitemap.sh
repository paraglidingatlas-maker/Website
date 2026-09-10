#!/usr/bin/env bash
# The three checks that must pass before any push touching the sitemap.
# They exist because three separate runtime bugs reached the live page while
# narrower checks passed. Syntax checks prove almost nothing on their own, so
# check 3 actually runs draw().
#
#   ./tools/check_sitemap.sh
#
# Exits non-zero on the first failure.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== 1/3  syntax =="
node --check sitemap-graph.js
echo "PASS: sitemap-graph.js parses"
echo

echo "== 2/3  static scan, absolute coordinates in the node group =="
node tools/check_sitemap_static.js
echo

echo "== 3/3  headless render, draw() actually runs =="
node tools/check_sitemap_render.js
echo
echo "All three checks passed."
