#!/usr/bin/env python3
"""
Episode page generator for Paragliding Atlas.

Usage: fill out EPISODES list below (or load from a JSON file) and run this
script. It generates one real, SEO-optimized HTML file per episode into
/episodes/, using the site's existing design system.

Each episode page includes:
  - Unique <title> and <meta name="description">
  - Open Graph tags (for link previews when shared)
  - JSON-LD structured data (schema.org PodcastEpisode) — this is the single
    most important piece for search engines to understand and index the page
    correctly as a podcast episode, not just generic text
  - Full transcript as real text (this is what actually gets crawled and
    ranked — audio itself is invisible to Google)
  - Guest info, keywords/tags, links out to listening platforms
  - Breadcrumb navigation and a link back to the full episode archive

Run with: python3 generate_episode_pages.py
"""

import os
import re
import json

SITE_URL = "https://paraglidingatlas.com"  # update once the real domain is live
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "episodes")

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Paragliding Atlas Podcast</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords_csv}">
<link rel="canonical" href="{site_url}/episodes/{slug}.html">

<!-- Open Graph tags: control how this looks when shared on social media -->
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site_url}/{thumb}">
<meta property="og:url" content="{site_url}/episodes/{slug}.html">

<!-- JSON-LD structured data: tells Google this is specifically a podcast
     episode, not just a generic page. This is the highest-value SEO element
     on this page. -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "PodcastEpisode",
  "url": "{site_url}/episodes/{slug}.html",
  "name": "{title}",
  "datePublished": "{date_iso}",
  "description": "{description}",
  "associatedMedia": {{
    "@type": "MediaObject",
    "contentUrl": "{spotify_url}"
  }},
  "partOfSeries": {{
    "@type": "PodcastSeries",
    "name": "Paragliding Atlas Podcast",
    "url": "{site_url}/podcast.html"
  }}
}}
</script>

<link rel="icon" type="image/png" href="../assets/logo/favicon.png">
<link rel="preload" href="../assets/fonts/poppins-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/poppins-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/dm-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/dm-sans-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="../styles.css">
<style>
  .ep-hero{{padding:clamp(3rem,7vw,4.5rem) clamp(1.5rem,5vw,4rem) 0;background:var(--bg);}}
  .breadcrumb{{color:var(--gray);font-size:0.8rem;margin-bottom:1.5rem;}}
  .breadcrumb a{{color:var(--gray-light);}}
  .breadcrumb a:hover{{color:var(--orange);}}
  .ep-hero h1{{font-family:var(--font-display);font-weight:800;font-size:clamp(1.8rem,4vw,2.8rem);color:var(--white);line-height:1.2;margin-bottom:1rem;max-width:900px;}}
  .ep-hero-guest{{color:var(--orange);font-size:1rem;font-weight:600;margin-bottom:2rem;}}
  .ep-meta-row{{display:flex;flex-wrap:wrap;gap:0.8rem;margin-bottom:2.5rem;}}
  .ep-tag{{background:var(--card);border:1px solid rgba(255,117,23,0.25);color:var(--gray-light);font-size:0.75rem;padding:0.35rem 0.8rem;text-transform:uppercase;letter-spacing:0.04em;}}

  .ep-body{{padding:0 clamp(1.5rem,5vw,4rem) clamp(4rem,9vw,6rem);background:var(--bg);display:grid;grid-template-columns:1fr 300px;gap:3rem;max-width:1300px;margin:0 auto;}}
  .ep-listen{{display:flex;flex-wrap:wrap;gap:0.9rem;margin-bottom:2.5rem;}}
  .ep-transcript-head{{font-family:var(--font-display);font-weight:700;font-size:1.3rem;color:var(--white);margin-bottom:1.2rem;border-bottom:1px solid rgba(180,180,180,0.15);padding-bottom:0.8rem;}}
  .ep-transcript{{color:var(--gray-light);line-height:1.85;font-size:0.98rem;}}
  .ep-transcript p{{margin-bottom:1.3rem;}}
  .transcript-missing{{background:var(--card);border-left:3px solid var(--orange);padding:1.5rem;color:var(--gray-light);font-size:0.9rem;}}

  .ep-sidebar-box{{background:var(--card);border:1px solid rgba(180,180,180,0.12);padding:1.5rem;margin-bottom:1.5rem;}}
  .ep-sidebar-box h3{{font-family:var(--font-display);font-weight:700;font-size:0.95rem;color:var(--orange);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.9rem;}}
  .ep-sidebar-box p{{color:var(--gray-light);font-size:0.9rem;line-height:1.6;}}
  .related-ep{{display:block;color:var(--gray-light);font-size:0.88rem;padding:0.6rem 0;border-bottom:1px solid rgba(180,180,180,0.1);}}
  .related-ep:hover{{color:var(--orange);}}
  .related-ep:last-child{{border-bottom:none;}}

  @media(max-width:820px){{
    .ep-body{{grid-template-columns:1fr;}}
  }}
</style>
</head>
<body>

<nav>
  <span class="nav-corner-l"></span>
  <span class="nav-corner-r"></span>
  <span class="nav-coords">59.9139°N · 10.7522°E</span>
  <a href="../index.html" class="wordmark"><img src="../assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img"></a>
  <div class="nav-links">
    <a href="../about.html">About Us</a>
    <span class="nav-sep">|</span>
    <a href="../knowledge-base.html">Knowledge Base</a>
      <a href="../safety-and-disclosure.html">Safety &amp; Disclosure</a>
    <span class="nav-sep">|</span>
    <a href="../podcast.html">Podcast</a>
  </div>
  <a href="../enquire.html" class="nav-cta" data-hover><span>Enquire Now</span></a>
</nav>
<div class="nav-chevron"></div>

<header class="ep-hero">
  <p class="breadcrumb"><a href="../podcast.html">Podcast</a> / {title}</p>
  <h1>{title}</h1>
  <p class="ep-hero-guest">{guest} · {date_display}</p>
  <div class="ep-meta-row">
    {tags_html}
  </div>
</header>

<div class="ep-body">
  <div>
    <div class="ep-listen">
      <a href="{spotify_url}" target="_blank" rel="noopener" class="listen-btn" data-hover><span>Spotify</span></a>
      <a href="{youtube_url}" target="_blank" rel="noopener" class="listen-btn" data-hover><span>YouTube</span></a>
      <a href="{apple_url}" target="_blank" rel="noopener" class="listen-btn" data-hover><span>Apple Podcasts</span></a>
    </div>

    <p class="ep-transcript-head">Full Transcript</p>
    <div class="ep-transcript">
      {transcript_html}
    </div>
  </div>

  <aside>
    <div class="ep-sidebar-box">
      <h3>About The Guest</h3>
      <p>{guest_bio}</p>
    </div>
    <div class="ep-sidebar-box">
      <h3>More Episodes</h3>
      {related_html}
    </div>
  </aside>
</div>

</body>
</html>
"""


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:80]


def build_episode_html(ep):
    tags_html = "\n    ".join(f'<span class="ep-tag">{k}</span>' for k in ep["keywords"])

    if ep.get("transcript"):
        paragraphs = ep["transcript"].split("\n\n")
        transcript_html = "\n      ".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    else:
        transcript_html = (
            '<div class="transcript-missing">Transcript coming soon. '
            "In the meantime, listen to the full episode using the links above.</div>"
        )

    related_html = "\n      ".join(
        f'<a class="related-ep" href="{r["slug"]}.html">{r["title"]}</a>'
        for r in ep.get("related", [])
    ) or '<p style="color:var(--gray);font-size:0.85rem;">More episodes coming soon.</p>'

    return TEMPLATE.format(
        title=ep["title"],
        description=ep["description"],
        keywords_csv=", ".join(ep["keywords"]),
        site_url=SITE_URL,
        slug=ep["slug"],
        thumb=ep.get("thumb", "assets/logo/favicon.png"),
        date_iso=ep["date_iso"],
        spotify_url=ep.get("spotify_url", "#"),
        youtube_url=ep.get("youtube_url", "#"),
        apple_url=ep.get("apple_url", "#"),
        guest=ep["guest"],
        date_display=ep["date_display"],
        tags_html=tags_html,
        guest_bio=ep.get("guest_bio", "Guest bio coming soon."),
        transcript_html=transcript_html,
        related_html=related_html,
    )


# ── Episode data ─────────────────────────────────────────────────────────
# Loads from episodes_data.json if it exists (the real, bulk-populated data
# file) — otherwise falls back to the single hardcoded example below.
DATA_FILE = os.path.join(os.path.dirname(__file__), "episodes_data.json")

if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        EPISODES = json.load(f)
else:
    EPISODES = [
        {
            "slug": "watch-this-before-you-buy-a-paragliding-harness",
            "title": "Watch This Before You Buy a Paragliding Harness",
            "guest": "Zsolt Ero",
            "date_iso": "2025-12-04",
            "date_display": "December 4, 2025",
            "description": (
                "A masterclass on the science and strategy behind paragliding harnesses, "
                "with reserve parachute expert Zsolt Ero — what actually matters before you buy one."
            ),
            "keywords": ["paragliding harness", "reserve parachute", "back protector", "Zsolt Ero", "paragliding safety"],
            "spotify_url": "https://www.youtube.com/watch?v=kSoFk23TuX0",
            "youtube_url": "https://www.youtube.com/watch?v=kSoFk23TuX0",
            "apple_url": "#",
            "guest_bio": "Zsolt Ero writes Hyperpilot, researching paragliding harness safety, back protectors, and competition safety standards.",
            "transcript": "",
            "related": [],
        },
    ]

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for ep in EPISODES:
        html = build_episode_html(ep)
        path = os.path.join(OUTPUT_DIR, f"{ep['slug']}.html")
        with open(path, "w") as f:
            f.write(html)
        print(f"Generated: episodes/{ep['slug']}.html")
