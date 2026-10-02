#!/usr/bin/env bash
# Checks for the sitemap page.
#
# Since October 2026 the sitemap is the night sky (sitemap-sky.js); the network
# graph (sitemap-graph.js) it replaced is no longer on the page, so the two
# graph checks (check_sitemap_static.js, check_sitemap_render.js) no longer
# run here. The sky's behaviour is checked in a real browser by smoke.py
# (sitemap_sky): every episode is a star, and finding a constellation opens
# its list.
#
#   ./tools/check_sitemap.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== syntax =="
node --check sitemap-sky.js
echo "PASS: sitemap-sky.js parses"
