#!/usr/bin/env bash
# Full site build, in dependency order. Run this rather than individual
# generators: the schema injector must run LAST, because it post-processes
# whatever the generators produced.
set -e
cd "$(dirname "$0")"
python3 generate_chapter_deck.py    >/dev/null
python3 generate_kb_pages.py        >/dev/null 2>&1 || true
python3 generate_policies.py        >/dev/null
python3 generate_tag_pages.py       >/dev/null
python3 generate_sitemap.py         >/dev/null
python3 generate_robots_sitemap.py  >/dev/null
python3 generate_llms_txt.py        >/dev/null
python3 tools/inject_site_schema.py
echo "build complete"
