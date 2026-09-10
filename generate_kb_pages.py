#!/usr/bin/env python3
"""Generates remaining Knowledge Base category and sub-series pages."""
import os

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "knowledge-base")

NAV_FOOTER = """
</div><!-- /.page-wrap -->

<footer>
  <div class="footer-content">
  <div class="footer-top">
    <div class="footer-col">
      <span class="wordmark"><img src="../assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img"></span>
      <p>Organisasjonsnummer: 937116934<br>Olav Troviks Vei M 46<br>Oslo, Norway</p>
    </div>
    <div class="footer-col">
      <h4>Enquiries</h4>
      <a href="../enquire.html">General</a>
      <a href="../index.html#destinations">Trips</a>
      <a href="#">FAQs</a>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <a href="../library.html">All Episodes</a>
      <a href="../index.html#destinations">Kenya Tour</a>
      <a href="../enquire.html">Contact Us</a>
    </div>
    <div class="footer-col">
      <h4>Links</h4>
      <a href="../knowledge-base.html">Knowledge Base</a>
      <a href="#">Passion</a>
      <a href="#">Mission Statement</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>Terms &amp; Conditions</span>
    <span>Privacy Policy</span>
    <span>Cookie Policy</span>
    <span>Paragliding Atlas 2026</span>
  </div>
  </div>
  <div class="footer-graphic">
    <img src="../assets/footer/mountains.png" alt="Paragliding Atlas — Touch the Sky with Glory">
  </div>
</footer>

<script src="../script.js"></script>
</body>
</html>
"""

NAV_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Knowledge Base: Paragliding Atlas</title>
<link rel="icon" type="image/png" href="../assets/logo/favicon.png">
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="../styles.css">
<style>
{css}
</style>
</head>
<body>

<div class="page-wrap">

<nav>
  <span class="nav-corner-l"></span>
  <span class="nav-corner-r"></span>
  <span class="nav-coords">59.9139°N · 10.7522°E</span>
  <a href="../index.html" class="wordmark"><img src="../assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img"></a>
  <div class="nav-links">
    <a href="../about.html">About Us</a>
    <span class="nav-sep">|</span>
    <a href="../knowledge-base.html">Knowledge Base</a>
    <span class="nav-sep">|</span>
    <a href="../podcast.html">Podcast</a>
  </div>
  <a href="../enquire.html" class="nav-cta" data-hover><span>Enquire Now</span></a>
</nav>
<div class="nav-chevron"></div>

{body}
"""

CATEGORY_CSS = """
  .cat-hero{padding:clamp(3.5rem,8vw,5.5rem) clamp(1.5rem,5vw,4rem) clamp(2.5rem,6vw,3.5rem);background:var(--bg);}
  .breadcrumb{color:var(--gray);font-size:0.8rem;margin-bottom:1.2rem;}
  .breadcrumb a{color:var(--gray-light);text-decoration:none;}
  .breadcrumb a:hover{color:var(--orange);}
  .cat-hero h1{font-family:var(--font-display);font-weight:800;font-size:clamp(1.9rem,4vw,2.8rem);color:var(--white);margin-bottom:1rem;max-width:800px;}
  .cat-hero p{color:var(--gray-light);line-height:1.7;max-width:700px;}
  .series-body{padding:0 clamp(1.5rem,5vw,4rem) clamp(4rem,9vw,6rem);background:var(--bg);}
  .series-grid{display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:1.5rem;max-width:1300px;margin:0 auto;}
  .series-card{
    position:relative;background:var(--card);border:1px solid rgba(180,180,180,0.12);padding:1.8rem;
    text-decoration:none;display:flex;flex-direction:column;
    transition:border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
  }
  .series-card:hover{border-color:rgba(255,117,23,0.4);box-shadow:0 0 24px rgba(255,117,23,0.15);transform:translateY(-3px);}
  .series-icon{
    width:44px;height:44px;border-radius:50%;background:var(--orange);
    display:flex;align-items:center;justify-content:center;margin-bottom:1.1rem;
    transition:box-shadow 0.25s ease, transform 0.25s ease;
  }
  .series-icon svg{width:20px;height:20px;color:#171712;}
  .series-card:hover .series-icon{box-shadow:0 0 18px 3px rgba(255,117,23,0.6);transform:scale(1.08);}
  .series-card h3{font-family:var(--font-display);font-weight:700;font-size:1.15rem;color:var(--white);margin-bottom:0.9rem;}
  .series-card p{color:var(--gray-light);font-size:0.9rem;line-height:1.65;margin-bottom:1.2rem;}
  .series-points{list-style:none;margin-bottom:auto;}
  .series-points li{color:var(--gray-light);font-size:0.84rem;padding:0.4rem 0 0.4rem 1.2rem;position:relative;border-top:1px solid rgba(180,180,180,0.08);}
  .series-points li:first-child{border-top:none;}
  .series-points li::before{content:"▸";position:absolute;left:0;color:var(--orange);}
  .series-arrow{margin-top:1.2rem;color:var(--orange);font-size:0.85rem;font-weight:600;}
"""

SUBSERIES_CSS = """
  .cat-hero{padding:clamp(3.5rem,8vw,5.5rem) clamp(1.5rem,5vw,4rem) clamp(2.5rem,6vw,3.5rem);background:var(--bg);}
  .breadcrumb{color:var(--gray);font-size:0.8rem;margin-bottom:1.2rem;}
  .breadcrumb a{color:var(--gray-light);text-decoration:none;}
  .breadcrumb a:hover{color:var(--orange);}
  .cat-hero h1{font-family:var(--font-display);font-weight:800;font-size:clamp(1.9rem,4vw,2.8rem);color:var(--white);margin-bottom:1rem;}
  .cat-hero p{color:var(--gray-light);line-height:1.7;max-width:700px;margin-bottom:1.5rem;}
  .point-row{display:flex;flex-wrap:wrap;gap:1.5rem;}
  .point-row span{color:var(--gray-light);font-size:0.82rem;position:relative;padding-left:1rem;}
  .point-row span::before{content:"▸";position:absolute;left:0;color:var(--orange);}
  .ep-body{padding:0 clamp(1.5rem,5vw,4rem) clamp(4rem,9vw,6rem);background:var(--bg);}
  .ep-grid{display:grid;grid-template-columns:repeat(auto-fill, minmax(280px, 1fr));gap:1.3rem;max-width:1300px;margin:0 auto;}
  .ep-tile{
    cursor:pointer;
    position:relative;background:var(--card);border:1px solid rgba(180,180,180,0.15);
    text-decoration:none;overflow:hidden;aspect-ratio:16/10;display:flex;align-items:flex-end;
    transition:border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
  }
  .ep-tile:hover{border-color:rgba(255,117,23,0.45);box-shadow:0 0 24px rgba(255,117,23,0.18);transform:translateY(-3px);}
  .ep-tile-bg{position:absolute;inset:0;background:linear-gradient(135deg,#3a1010,#8a1c1c);}
  .ep-tile-overlay{position:relative;padding:1.2rem;background:linear-gradient(0deg, rgba(10,10,12,0.9), transparent 70%);width:100%;}
  .ep-tile-title{font-family:var(--font-display);font-weight:700;font-size:0.98rem;color:var(--white);margin-bottom:0.3rem;line-height:1.3;}
  .ep-tile-guest{color:var(--orange);font-size:0.8rem;font-weight:600;}
  .ep-empty{background:var(--card);border:1px solid rgba(255,117,23,0.2);border-left:3px solid var(--orange);padding:2rem;max-width:1300px;margin:0 auto;color:var(--gray-light);font-size:0.92rem;}
"""


def write(path, content):
    full = os.path.join(OUT, path)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)


def category_page(slug, title, intro, series_list):
    cards = ""
    for s in series_list:
        points = "".join(f"<li>{p}</li>" for p in s["points"])
        cards += f"""
    <a class="series-card" href="{s['slug']}.html">
      <div class="series-icon">{s['icon']}</div>
      <h3>{s['name']}</h3>
      <p>{s['desc']}</p>
      <ul class="series-points">{points}</ul>
      <span class="series-arrow">View Episodes →</span>
    </a>"""
    body = f"""<header class="cat-hero">
  <p class="breadcrumb"><a href="../knowledge-base.html">Knowledge Base</a> / {title}</p>
  <h1>{title}</h1>
  <p>{intro}</p>
</header>

<div class="series-body">
  <div class="series-grid">{cards}
  </div>
</div>"""
    html = NAV_HEADER.format(title=title, css=CATEGORY_CSS, body=body) + NAV_FOOTER
    write(f"{slug}.html", html)


def subseries_page(slug, category_slug, category_title, title, intro, points, episodes):
    point_html = "".join(f"<span>{p}</span>" for p in points)
    if episodes:
        tiles = "".join(
            f"""
    <div class="ep-tile" data-title="{e['title'].replace('"', '&quot;')}" data-guest="{e['guest']}" data-desc="{e.get('desc', '')}" data-readmore="{e.get('readmore', '../podcast.html')}" data-yt-id="{e.get('yt_id', '')}">
      <div class="ep-tile-bg"></div>
      <div class="ep-tile-overlay">
        <p class="ep-tile-title">{e['title']}</p>
        <p class="ep-tile-guest">{e['guest']}</p>
      </div>
    </div>"""
            for e in episodes
        )
        ep_html = f'<div class="ep-grid">{tiles}\n  </div>'
    else:
        ep_html = '<div class="ep-empty">Episodes for this series are coming soon. Check back shortly, or explore the <a href="../podcast.html" style="color:var(--orange);">full podcast archive</a> in the meantime.</div>'

    body = f"""<header class="cat-hero">
  <p class="breadcrumb"><a href="../knowledge-base.html">Knowledge Base</a> / <a href="{category_slug}.html">{category_title}</a> / {title}</p>
  <h1>{title}</h1>
  <p>{intro}</p>
  <div class="point-row">{point_html}</div>
</header>

<div class="ep-body">
  {ep_html}
</div>"""
    html = NAV_HEADER.format(title=title, css=SUBSERIES_CSS, body=body)
    html = html.replace(
        '<script src="../script.js"></script>\n</body>',
        '<script src="../script.js"></script>\n<script src="../episode-modal.js"></script>\n</body>'
    )
    write(f"{slug}.html", html + NAV_FOOTER.replace(
        '<script src="../script.js"></script>\n</body>',
        '<script src="../script.js"></script>\n<script src="../episode-modal.js"></script>\n</body>'
    ))


# ── Icons ────────────────────────────────────────────────────────────────
ICONS = {
    "flag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 20l6-11 4 6.5L16 9l5 11Z"/></svg>',
    "trophy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 4h8v4a4 4 0 0 1-8 0V4Z"/><path d="M6 5H4a2 2 0 0 0 0 4h2M18 5h2a2 2 0 0 1 0 4h-2M12 12v3M9 20h6M10 17h4v3h-4z"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v18M5 7l-3 6a3 3 0 0 0 6 0l-3-6ZM19 7l-3 6a3 3 0 0 0 6 0l-3-6ZM5 7h14M8 21h8"/></svg>',
    "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2-2Z"/></svg>',
    "cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6.5 19a4.5 4.5 0 0 1-.5-9 5 5 0 0 1 9.6-1.5A4 4 0 0 1 17.5 16.5"/><path d="M6.5 19h11a3.5 3.5 0 0 0 0-7"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.6 12.6 12 21.2 2.8 12 4 4l8-1.2 8.6 8.8Z"/><circle cx="8.5" cy="8.5" r="1.5" fill="currentColor" stroke="none"/></svg>',
    "mic": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>',
    "warning": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17h.01"/></svg>',
    "gear": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z"/></svg>',
    "backpack": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 8V6a5 5 0 0 1 10 0v2"/><rect x="5" y="8" width="14" height="13" rx="2"/><path d="M9 12h6M9 16h6"/></svg>',
}

# ── Build Navigators and Sky Gods (under Core Series) ────────────────────
subseries_page(
    "navigators", "core-series", "Core Series", "Navigators",
    "Site-specific guides built with local expert insights to help you understand not just where to fly, but how to fly it right.",
    ["In-depth site breakdowns", "Local weather patterns &amp; triggers", "Airspace rules and regulations", "Proven best practices (and common mistakes to avoid)"],
    [
        {"title": "Navigating Colombia", "guest": "Pal Takats"},
        {"title": "Navigating Australia", "guest": "Godfrey Wenness"},
        {"title": "Navigating India", "guest": "Eddie Colfox"},
        {"title": "Navigating India (Bonus Ep.)", "guest": "Jigish Gohil"},
        {"title": "Navigating Panchgani (Pre PWC India)", "guest": "Vistasp Kharas"},
        {"title": "Pre PWC Kenya", "guest": "Nikolay Yotov"},
    ],
)

subseries_page(
    "sky-gods", "core-series", "Core Series", "Sky Gods",
    "Step into the minds of the most influential pilots and understand what drives excellence at the highest level.",
    ["Career journeys and milestones", "Training philosophies", "Personal rituals and mindset", "Lessons from elite performance"],
    [
        {"title": "Sky Gods: Flying To Win", "guest": "Honorin Hamard", "readmore": "../podcast.html"},
        {"title": "Sky Gods: Flying 8000ers", "guest": "Antoine Girard"},
        {"title": "The Journey Within: Mapping Our Quest to Touch The Sky With Glory", "guest": "Maxime Pinot"},
    ],
)

# ── Living The Dream (under Core Series) ─────────────────────────────────
subseries_page(
    "living-the-dream", "core-series", "Core Series", "Living The Dream",
    "Explore real pathways to turning passion into a sustainable lifestyle.",
    ["Career opportunities in paragliding", "Business and income pathways", "Lifestyle and work balance", "Long-term sustainability insights"],
    [
        {"title": "Anatomy of a Dream: A Lifestyle Full of Grit, Grace and Vertical Freedom", "guest": "Damien Lacaze"},
        {"title": "Vol Biv & Freedom Unfiltered: A Human-Powered Odyssey By Paragliding, Biking & Sailing Around The Globe", "guest": "Sandrine Roy"},
        {"title": "From Cuba to Socotra: Inside the World's Most Unique Paragliding Tours", "guest": ""},
        {"title": "Touch The Sky With Glory", "guest": ""},
        {"title": "How to Fly With Your Dog", "guest": "Shams"},
        {"title": "Living The Dream", "guest": "Benjamin Jordan"},
    ],
)

# ── Competitions & Performance category + sub-series ────────────────────
category_page(
    "competitions", "Competitions & Performance",
    "Take a tour into the thrilling world of racing paragliders and learn how to push your performance boundaries safely and effectively — strategies, training techniques, and mindset from the pilots who have done it all.",
    [
        {"slug": "world-cups", "name": "World Cups, Racing and Competing", "icon": ICONS["trophy"],
         "desc": "A clear view of modern race formats and evolving rules, with insights from experienced competitors and organizers.",
         "points": ["Competition formats and scoring systems", "Race strategy and decision-making", "Event structures and calendars", "Insights from pilots and organizers"]},
        {"slug": "risk-vs-reward", "name": "Risk vs. Reward", "icon": ICONS["scale"],
         "desc": "How to make calculated decisions that balance competitive advantage with safety.",
         "points": ["Risk assessment in real conditions", "High-consequence scenario awareness", "Personal limit setting", "Practical decision-making frameworks"]},
        {"slug": "resources-tools-tips", "name": "Resources, Tools &amp; Tips", "icon": ICONS["wrench"],
         "desc": "Uncover the secrets behind epic flights, tracklog analysis, and decision-making in challenging conditions.",
         "points": ["Tracklog analysis techniques", "Performance review tools", "Case studies of notable flights", "Practical tips from experienced pilots"]},
    ],
)

subseries_page(
    "world-cups", "competitions", "Competitions & Performance", "World Cups, Racing and Competing",
    "Get a clear view of modern race formats and evolving rules, with insights from experienced competitors and organizers.",
    ["Competition formats and scoring systems", "Race strategy and decision-making", "Event structures and calendars", "Insights from pilots and organizers"],
    [
        {"title": "From Tents to Trophies: Understanding Acro Champion's Mindset on Ego, Glory & Drugs", "guest": "Luke De Weert"},
        {"title": "Master the Art of Scoring in Paragliding: A New Pilot's Guide to the GAP Formula & Strategy", "guest": "Joerg Ewald"},
        {"title": "The Inside Story of Sports Racing Series (SRS)", "guest": "Brett Janaway"},
        {"title": "Bruce Goldsmith Explains MRT Scoring System and Its Impact on Paragliding Competitions", "guest": "Bruce Goldsmith"},
        {"title": "Shane Tighe's Road to X-Alps: Engineering Conquests In The Sky from Australia's Flatlands to the Pinnacle of Hike and Fly", "guest": "Shane Tighe"},
        {"title": "The Resilience Equation: Erlend Ukvitne's Unrelenting Path to X-Alps and the Brink of a Hike and Fly World Record", "guest": "Erlend Ukvitne"},
        {"title": "PWC Lifestyle", "guest": "Klaudia Bulgakow"},
    ],
)

subseries_page(
    "risk-vs-reward", "competitions", "Competitions & Performance", "Risk vs. Reward",
    "Learn how to balance performance with safety by understanding when to push and when to hold back.",
    ["Risk assessment in real conditions", "High-consequence scenario awareness", "Personal limit setting", "Practical decision-making frameworks"],
    [
        {"title": "Risk Vs Reward 1", "guest": "Philipp Zellner"},
        {"title": "Risk Vs Reward 2", "guest": "Subir Sidhu"},
        {"title": "Risk Vs Reward 3", "guest": "Manfred Ruhmer"},
        {"title": "Risk Vs Reward 4", "guest": "Raúl Rodríguez"},
        {"title": "Risk Vs Reward 5", "guest": "Gabriel Orsini (partytillimpact)"},
        {"title": "Consequence Over Probability: Will Gadd's Field Protocols for Rewiring Risk Intuition and Why True Safety Lies in Clarity", "guest": "Will Gadd"},
        {"title": "Building a Healthy Relationship with the Skies: How to Master Fear, Build Resilience & Find Joy Through Paragliding", "guest": "Kinga Masztalerz"},
    ],
)

subseries_page(
    "resources-tools-tips", "competitions", "Competitions & Performance", "Resources, Tools & Tips",
    "Break down real flights and decisions using tools and insights that accelerate your learning curve.",
    ["Tracklog analysis techniques", "Performance review tools", "Case studies of notable flights", "Practical tips from experienced pilots"],
    [
        {"title": "Finest Paragliding Reviews & Superpower of Changing Wings as A Human", "guest": "Ziad Bassil"},
        {"title": "The Art of Capturing Human Flight: A Guide to Filming Passion Projects in Paragliding", "guest": "Jake Holland"},
        {"title": "Flying & Filming 1", "guest": "Benjamin Jordan"},
        {"title": "Flying & Filming 2", "guest": "Benjamin Kellet"},
        {"title": "Flying & Filming 3", "guest": "Andreas Lattner (hochzwei.media)"},
        {"title": "Science Backed Pre Flight Rituals to Unlock Laser Sharp Paragliding Clarity", "guest": "On Demand"},
        {"title": "The Silent Mind In Screaming Winds: Unlocking Peak Focus To Attain Flow State In Paragliding", "guest": "Grant Smith"},
        {"title": "Sports Psychology for Paragliding: Train Your Mind to Fly Better", "guest": "Yvonne Dathe"},
        {"title": "Mastering the Unknown: Neuroscience of Crisis Management & Neuroplasticity Training", "guest": ""},
        {"title": "Identifying Passion Vs Obsession: An Aviator's Approach to Overcoming Adversity, Rebuilding Trust and Finding Joy in the Skies", "guest": "Ashutosh Chopra"},
        {"title": "AMA #1", "guest": ""},
    ],
)

# ── Meteorology & Weather Analysis category + sub-series ────────────────
category_page(
    "meteorology", "Meteorology & Weather Analysis",
    "Understanding weather patterns and atmospheric conditions is crucial for safe paragliding — this section exists to help you build exactly that.",
    [
        {"slug": "weather-patterns", "name": "Weather Patterns and Forecasting", "icon": ICONS["cloud"],
         "desc": "Build a solid foundation in understanding weather systems and how they influence flying conditions.",
         "points": ["Pressure systems and fronts", "Cloud formations and indicators", "Wind patterns and thermals", "Forecast interpretation"]},
    ],
)

subseries_page(
    "weather-patterns", "meteorology", "Meteorology & Weather Analysis", "Weather Patterns and Forecasting",
    "Build a solid foundation in understanding weather systems and how they influence flying conditions.",
    ["Pressure systems and fronts", "Cloud formations and indicators", "Wind patterns and thermals", "Forecast interpretation"],
    [
        {"title": "Meteorology 101: A Beginner's Guide to Understanding Weather Apps and Decoding Endless Forecasting Options", "guest": ""},
    ],
)

# ── Industry & Community category + sub-series ───────────────────────────
category_page(
    "industry", "Industry & Community",
    "Explore the business side of paragliding and learn from the collective wisdom of our global community.",
    [
        {"slug": "brand-stories", "name": "Brand Stories &amp; Manufacturer Profiles", "icon": ICONS["tag"],
         "desc": "Discover the history and innovation behind the leading paragliding brands.",
         "points": ["Company histories and milestones", "Design philosophies", "Product development processes", "Certification and safety standards"]},
        {"slug": "storytellers", "name": "Storytellers", "icon": ICONS["mic"],
         "desc": "Go beyond flying and into the lives, journeys, and perspectives of the sport through human stories.",
         "points": ["Personal pilot journeys", "Community voices", "Cultural perspectives", "Real-world experiences"]},
        {"slug": "the-dark-side", "name": "The Dark Side: Learning from Incidents", "icon": ICONS["warning"],
         "desc": "Critical analysis of accidents and incidents to prevent future occurrences and improve safety standards.",
         "points": ["Incident case studies", "Root cause analysis", "Contributing factors", "Preventive lessons and insights"]},
    ],
)

subseries_page(
    "brand-stories", "industry", "Industry & Community", "Brand Stories &amp; Manufacturer Profiles",
    "Explore the evolution, philosophy, and innovation shaping the equipment you trust.",
    ["Company histories and milestones", "Design philosophies", "Product development processes", "Certification and safety standards"],
    [
        {"title": "On Challenges, Change & The Future of Paragliding", "guest": "Pal Takats"},
        {"title": "Legacy and Lifetimes: 5 Decades of Pioneering the Art of Free Flight", "guest": "Gin Seok Song"},
        {"title": "Brand Stories: Neo", "guest": "Eric Roussel"},
        {"title": "PWCA", "guest": "Goran Dimiskovski"},
    ],
)

subseries_page(
    "storytellers", "industry", "Industry & Community", "Storytellers",
    "Go beyond flying and into the lives, journeys, and perspectives of the sport through human stories.",
    ["Personal pilot journeys", "Community voices", "Cultural perspectives", "Real-world experiences"],
    [
        {"title": "Storytime: Chasing Adventure With the Real OG John Silvester & 3 Decades of Making Memories Across The Globe", "guest": "Eddie Colfox"},
        {"title": "Storytellers: Mid-Air Collision", "guest": "Marko Milutinovic"},
    ],
)

subseries_page(
    "the-dark-side", "industry", "Industry & Community", "The Dark Side: Learning from Incidents",
    "Understand accidents and incidents through detailed analysis to improve awareness and safety.",
    ["Incident case studies", "Root cause analysis", "Contributing factors", "Preventive lessons and insights"],
    [
        {"title": "The Uncomfortable Truth No One is Talking About in the Current Safety Paradox", "guest": "Bill Belcourt"},
        {"title": "Survived 15 Years of Flying, Then a Rescue Helicopter Changed Everything", "guest": "Nick Neynes"},
        {"title": "The Unfiltered Truth About Paragliding Governance", "guest": "Bill Hughes &amp; Goran Dimiskovski"},
        {"title": "Insights From The Gaggle", "guest": "Tilen Ceglar &amp; Stan Radzikowski"},
        {"title": "#CIVLRESIGN", "guest": "Julien Garcia"},
    ],
)

# ── Technical Focus & Flight Safety category + sub-series ────────────────
category_page(
    "technical", "Technical Focus & Flight Safety",
    "A deep dive into the technical aspects of free flight — comprehensive knowledge about the mechanics, equipment, and technological advances in paragliding.",
    [
        {"slug": "flight-mechanics", "name": "Flight Mechanics", "icon": ICONS["gear"],
         "desc": "Build a deeper understanding of the forces and principles that govern safe and efficient flight.",
         "points": ["Aerodynamic fundamentals", "AOA and airspeed", "Wing behavior in different phases", "Control inputs and their effects"]},
        {"slug": "new-technologies", "name": "New Technologies", "icon": ICONS["bolt"],
         "desc": "Explore innovations that are shaping performance, safety, and the future of flying.",
         "points": ["New materials and wing design", "Safety system innovations", "Flight instruments and analytics", "Emerging trends in paragliding tech"]},
        {"slug": "know-your-equipment", "name": "Know Your Equipment", "icon": ICONS["backpack"],
         "desc": "Gain confidence in your equipment through deeper understanding, maintenance, and selection knowledge.",
         "points": ["Canopy construction and materials", "Harness systems and protection", "Reserve parachute handling", "Maintenance and care practices"]},
    ],
)

subseries_page(
    "flight-mechanics", "technical", "Technical Focus & Flight Safety", "Flight Mechanics",
    "Build a deeper understanding of the forces and principles that govern safe and efficient flight.",
    ["Aerodynamic fundamentals", "AOA and airspeed", "Wing behavior in different phases", "Control inputs and their effects"],
    [
        {"title": "The Science Of Wing Design and Evolution from ENC to CSC", "guest": "Tom Lolies"},
        {"title": "Modernizing SIV Courses: How This New Training Method Can Help You Master Glider Control and Improve Paragliding Safety", "guest": "Helmut Schrempf"},
        {"title": "The Science of EN Certifications: How Work Group 6 Shaped Paragliding Testing, Innovation & Safety", "guest": "Alain Zoller"},
        {"title": "Demystifying The Science Behind the Endless Fun Factor of Parakites", "guest": "Bryan Van Ostheim"},
        {"title": "Debunking the Myths and Upgrading Enzo 3", "guest": "Luc Armant"},
        {"title": "777: Paragliding's Slovenian Mavericks Redefining the EN B Class And Elevating Free Flight Performance", "guest": "Aljaž Valič"},
    ],
)

subseries_page(
    "new-technologies", "technical", "Technical Focus & Flight Safety", "New Technologies",
    "Stay current with the latest trends and innovations in paragliding tech.",
    ["New materials and wing design", "Safety system innovations", "Flight instruments and analytics", "Emerging trends in paragliding tech"],
    [
        {"title": "New Technologies 1", "guest": "Beni Kälin (speedflyingschool.com)"},
        {"title": "New Technologies 2", "guest": "Guillem Batlle &amp; Adrià Grau (Niviuk Paragliders)"},
        {"title": "New Technologies 3", "guest": "Stephan Stiegler (AirDesign Paragliders)"},
        {"title": "New Technologies 4", "guest": "Veselin Ovcharov (Fly The Earth)"},
        {"title": "New Technologies 5", "guest": "Frantisek Pavlousek (UP Paragliders)"},
        {"title": "Understanding Skymate: Paragliding World's First AI Powered Smart Harness System", "guest": "Roman Barthelemy"},
        {"title": "Why Paragliding's Safety Future Looks Different: RAST Inventor Michael Nesler & the LeelooX Effect", "guest": "Michael Nesler"},
    ],
)

subseries_page(
    "know-your-equipment", "technical", "Technical Focus & Flight Safety", "Know Your Equipment",
    "Master your flying kit and gear with detailed tutorials and maintenance guides.",
    ["Canopy construction and materials", "Harness systems and protection", "Reserve parachute handling", "Maintenance and care practices"],
    [
        {"title": "The Real Truth About Reserve Parachutes: A Paragliding Survival Guide", "guest": "Urs Haari"},
        {"title": "Watch This Before You Buy a Paragliding Harness", "guest": "Zsolt Ero", "yt_id": "kSoFk23TuX0", "readmore": "../episodes/watch-this-before-you-buy-a-paragliding-harness.html"},
        {"title": "Snippet: A Reserve Parachute Trick Every Pilot Should Know", "guest": "Urs Haari"},
        {"title": "Helmet Safety: ICARO 2000 [1st Anniversary Edition]", "guest": "Christian Ciech"},
        {"title": "Carabiner Fatigue (Whitepaper)", "guest": "Finsterwalder &amp; Charly"},
        {"title": "A Note of Thanks", "guest": ""},
    ],
)

print("Done.")
