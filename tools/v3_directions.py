#!/usr/bin/env python3
"""
Three visual directions for the rebuilt site, on one bookings-first structure.

prototypes/v3/ (hidden: noindex, canonical to the live page, never linked):
  index.html            the chooser: the three directions side by side
  home-a.html  trip-a.html   A  Summit       (Elite Exped, Bear Grylls)
  home-b.html  trip-b.html   B  Field Journal (XOVERLAND)
  home-c.html  trip-c.html   C  Clear Skies  (Trek Travel)

The content is the same in all three and is the site's own: trip facts, dates
and the India price from the destination pages, the guides from the India page,
the podcast and knowledge base lines from the live pages. Where the site has no
fact yet (Kenya price, Peru and Kazakhstan details, the wider team) the page
says so in a visible [to supply] mark rather than inventing one.

    python3 tools/v3_directions.py
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "prototypes", "v3")
A = "../../assets/"          # live assets
V2 = "../v2/"                # v2 pages, for the links that are not rebuilt here
e = html.escape

TRIPS = [
    dict(key="india", place="India", region="Bir Billing, Himalaya", title="The Majestic Himalayas",
         line="Big mountain flying from Bir Billing: one launch, a front range that works for tens of kilometres, and monasteries below.",
         img="destinations/india/hero/snowline", days="10 days", level="IPPI 2", level_n=4, group="6 pilots",
         season="October to November", next="21 to 30 Oct 2026", price="£1,100", status="Guaranteed to run",
         href=V2 + "destinations/india.html"),
    dict(key="kenya", place="Kenya", region="Kerio Valley, Rift Valley", title="A Journey Over The Cradle Of Humankind",
         line="Six sites down the Rift, 451 km end to end: world-record air in Kerio Valley, baobabs and giraffes below.",
         img="destinations/kenya/hero/longonot", days="12 days", level="IPPI 2", level_n=2, group="Small group",
         season="December to March", next="18 to 29 Jan 2027", price="[to supply]", status="Booking open",
         href=V2 + "destinations/kenya.html"),
    dict(key="peru", place="Peru", region="Lima and the Andes", title="Soar The Land Of The Incas",
         line="Long, graceful flights on the Pacific breeze, from Lima's cliffs to remote Andean communities.",
         img="images/peru-1", days="[to supply]", level="[to supply]", level_n=3, group="[to supply]",
         season="[to supply]", next="November 2027", price="[to supply]", status="Register interest",
         href="../../enquire.html?trip=peru"),
    dict(key="kazakhstan", place="Kazakhstan", region="The steppe", title="Beyond Roads, Beyond Maps",
         line="Our flagship: wind-carved canyons, dried ancient seabeds as landing fields, and a landscape untouched.",
         img="images/kazakhstan-1", days="[to supply]", level="[to supply]", level_n=5, group="[to supply]",
         season="[to supply]", next="June 2027", price="[to supply]", status="Register interest",
         href="../../enquire.html?trip=kazakhstan"),
]

DEPARTURES = [
    ("India", "Tour 1", "21 to 30 Oct 2026", "10 days", "6 places", "£1,100", "Guaranteed to run", V2 + "destinations/india.html#dates"),
    ("India", "Tour 2", "3 to 12 Nov 2026", "10 days", "6 places", "£1,100", "Guaranteed to run", V2 + "destinations/india.html#dates"),
    ("Kenya", "Tour 1", "18 to 29 Jan 2027", "12 days", "[to supply]", "[to supply]", "Booking open", V2 + "destinations/kenya.html#dates"),
    ("Kenya", "Tour 2", "1 to 12 Feb 2027", "12 days", "[to supply]", "[to supply]", "Booking open", V2 + "destinations/kenya.html#dates"),
    ("Kazakhstan", "", "June 2027", "[to supply]", "[to supply]", "[to supply]", "Register interest", "../../enquire.html?trip=kazakhstan"),
    ("Peru", "", "November 2027", "[to supply]", "[to supply]", "[to supply]", "Register interest", "../../enquire.html?trip=peru"),
]

GUIDES = [
    ("Aninder Singh", "Founder, Paragliding Atlas", A + "podcast/host-aninder-soft",
     "Took his first tandem flight as a child in the foothills of the Himalaya and has been flying for more than ten years since. Founded Paragliding Atlas in 2023 and hosts the podcast."),
    ("Gurpreet Dhindsa", "BHPA instructor · FAI Paul Tissandier Diploma 2026", None,
     "Flying since 1993, the first Indian to hold a BHPA instructor licence, founder of PG Gurukul at Bir, and part of drafting India's paragliding safety rules."),
    ("[Team member]", "[Role to supply]", None, "[Short bio to supply: who guides Kenya, Peru and Kazakhstan.]"),
]

GUESTS = [("guest-antoine", "Antoine Girard", "Flying 8000ers", "sky-gods-flying-8000ers-antoine-girard"),
          ("guest-urs", "Urs Haari", "The Real Truth About Reserve Parachutes", "urs-haari-the-real-truth-about-reserve-parachutes-a"),
          ("guest-will", "Will Gadd", "Consequence Over Probability", "consequence-over-probability-will-gadd-on-why-true-safety")]

DIRS = {
    "a": dict(name="Summit", ref="after Elite Exped and Bear Grylls",
              gist="Stark and cinematic. Near black, huge condensed capitals, full-bleed footage, hard lines. Credentials up front: it sells expertise and challenge."),
    "b": dict(name="Field Journal", ref="after XOVERLAND",
              gist="Documentary and warm. A serif voice, film grain, captions like log entries. The podcast and the trips are one story told from the field."),
    "c": dict(name="Clear Skies", ref="after Trek Travel",
              gist="Light and clear. White and sky, a trip finder in the hero, every card with dates, days, level and price. It sells certainty: pick a date, book."),
}


def mark(t):
    """[to supply] stays visible and styled, never passed off as a fact"""
    t = e(t)
    return t.replace("[", '<span class="tbd">[').replace("]", "]</span>")


def pic(src, alt, cls="", eager=False):
    return ('<picture class="%s"><source srcset="%s.webp" type="image/webp"><img src="%s.jpg" alt="%s"%s></picture>'
            % (cls, A + src, A + src, e(alt), "" if eager else ' loading="lazy"'))


def head(d, title, canonical):
    return f'''<!DOCTYPE html>
<html lang="en" class="dir-{d}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<link rel="canonical" href="https://paraglidingatlas.com/{canonical}">
<link rel="icon" type="image/png" href="{A}logo/favicon.png">
<link rel="stylesheet" href="../../fonts.css">
<link rel="stylesheet" href="v3.css">
<link rel="stylesheet" href="{d}.css">
</head>
<body>
'''


def nav(d):
    logo = A + "logo/atlas-logo-white.png"   # every header sits over a photograph
    return f'''<header class="nav">
  <a class="nav-logo" href="home-{d}.html"><img src="{logo}" alt="Paragliding Atlas" width="480" height="100"></a>
  <nav class="nav-links" aria-label="Main">
    <a href="home-{d}.html#trips">Expeditions</a><a href="home-{d}.html#dates">Dates &amp; Prices</a>
    <a href="{V2}podcast.html">Podcast</a><a href="{V2}knowledge-base.html">Knowledge Base</a><a href="{V2}about.html">About</a>
  </nav>
  <a class="btn btn-solid nav-cta" href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">Book a call</a>
</header>
<a class="dir-flag" href="index.html">Direction {d.upper()} · {e(DIRS[d]["name"])} <span>compare all three</span></a>
'''


def foot():
    return f'''<footer class="foot">
  <div class="foot-in">
    <div><img src="{A}logo/atlas-logo-white.png" alt="Paragliding Atlas" width="160" height="33" loading="lazy" class="foot-logo">
      <p>Organisasjonsnummer 937116934 · Olav Troviks Vei M 46, 0864 Oslo, Norway</p></div>
    <div class="foot-cols">
      <div><b>Fly</b><a href="{V2}destinations/india.html">India</a><a href="{V2}destinations/kenya.html">Kenya</a><a href="../../enquire.html">Enquire</a></div>
      <div><b>Listen</b><a href="{V2}podcast.html">Podcast</a><a href="{V2}library.html">All episodes</a><a href="{V2}knowledge-base.html">Knowledge Base</a></div>
      <div><b>About</b><a href="{V2}about.html">About us</a><a href="../../safety-and-disclosure.html">Safety &amp; disclosure</a><a href="../../terms.html">Terms</a></div>
    </div>
  </div>
</footer>
<script src="v3.js"></script>
</body>
</html>
'''


def level(n):
    return '<span class="lvl" role="img" aria-label="Skill level %d of 5">%s</span>' % (
        n, "".join('<i class="%s"></i>' % ("on" if i < n else "") for i in range(5)))


def home(d):
    t0 = TRIPS[0]
    cards = ""
    for t in TRIPS:
        cards += f'''
      <a class="trip" href="{t["href"]}">
        <div class="trip-media">{pic(t["img"], t["place"] + ", " + t["region"])}<span class="trip-status">{e(t["status"])}</span></div>
        <div class="trip-body">
          <span class="kicker">{e(t["place"])} · {e(t["region"])}</span>
          <h3>{e(t["title"])}</h3>
          <p>{e(t["line"])}</p>
          <dl class="facts">
            <div><dt>Next</dt><dd>{mark(t["next"])}</dd></div>
            <div><dt>Days</dt><dd>{mark(t["days"])}</dd></div>
            <div><dt>Level</dt><dd>{level(t["level_n"])}</dd></div>
            <div><dt>From</dt><dd class="price">{mark(t["price"])}</dd></div>
          </dl>
        </div>
      </a>'''
    rows = ""
    for place, tour, dates, days, places, price, status, href in DEPARTURES:
        rows += f'''
        <a class="dep" href="{href}"><span class="dep-place">{e(place)} <small>{e(tour)}</small></span><span class="dep-dates">{e(dates)}</span>
          <span>{mark(days)}</span><span>{mark(places)}</span><span class="dep-price">{mark(price)}</span>
          <span class="dep-status s-{status.split()[0].lower()}">{e(status)}</span><span class="dep-go" aria-hidden="true">&rarr;</span></a>'''
    guides = ""
    for name, role, img, bio in GUIDES:
        face = ('<picture class="g-face"><source srcset="%s.webp" type="image/webp"><img src="%s.png" alt="%s" loading="lazy"></picture>' % (img, img, e(name))) if img else '<span class="g-face g-blank" aria-hidden="true">%s</span>' % e(name[:1] if not name.startswith("[") else "?")
        guides += f'<article class="guide">{face}<h3>{mark(name)}</h3><span class="kicker">{mark(role)}</span><p>{mark(bio)}</p></article>'
    guests = "".join(
        f'<a class="guest" href="{V2}episodes/{slug}.html" style="--i:{i}">{pic("podcast/" + img, name)}<span class="guest-name">{e(name)}</span><span class="guest-hook">{e(hook)}</span></a>'
        if slug in ("urs-haari-the-real-truth-about-reserve-parachutes-a",) else
        f'<a class="guest" href="../../episodes/{slug}.html" style="--i:{i}">{pic("podcast/" + img, name)}<span class="guest-name">{e(name)}</span><span class="guest-hook">{e(hook)}</span></a>'
        for i, (img, name, hook, slug) in enumerate(GUESTS))
    finder = ""
    if d == "c":
        finder = '''
      <form class="finder" action="#dates" onsubmit="return false">
        <label><span>Where</span><select><option>Any destination</option><option>India</option><option>Kenya</option><option>Kazakhstan</option><option>Peru</option></select></label>
        <label><span>When</span><select><option>Any month</option><option>October 2026</option><option>November 2026</option><option>January 2027</option><option>February 2027</option><option>June 2027</option><option>November 2027</option></select></label>
        <label><span>Level</span><select><option>Any level</option><option>IPPI 2 and up</option></select></label>
        <button class="btn btn-solid" type="button">Find a trip</button>
      </form>'''
    return head(d, "Paragliding Atlas: Guided Paragliding Expeditions | Direction " + d.upper(), "") + nav(d) + f'''
<main>
  <section class="hero">
    <div class="hero-media">{pic("images/hero", "Two paragliders soaring above the clouds", "hero-pic", True)}
      <video data-src="{A}video/hero-1080" muted loop playsinline preload="none" aria-hidden="true"></video></div>
    <div class="hero-copy">
      <span class="kicker">Guided paragliding expeditions · Himalaya · Rift Valley · Andes · Steppe</span>
      <h1>Touch The Sky <br>With Glory</h1>
      <p class="lede">Small-group paragliding expeditions across the Rift Valley, the Himalayan frontier, the Andes, and the untouched steppe of Kazakhstan, fully guided from launch to landing.</p>
      <div class="actions"><a class="btn btn-solid" href="#trips">See the expeditions</a><a class="btn btn-line" href="#dates">Dates &amp; prices</a></div>{finder}
    </div>
    <a class="next" href="{t0["href"]}#dates"><span class="next-k">Next departure</span><b>India · {e(t0["next"])}</b><span>{e(t0["days"])} · 6 places · £1,100 · {e(t0["status"])}</span><i aria-hidden="true">&rarr;</i></a>
  </section>

  <section class="sec" id="trips">
    <div class="sec-head"><span class="kicker">Expeditions</span><h2>Where we fly</h2>
      <p>Four expeditions on four continents. Two run this season; two open for 2027.</p></div>
    <div class="trips">{cards}
    </div>
  </section>

  <section class="sec sec-dates" id="dates">
    <div class="sec-head"><span class="kicker">Dates &amp; prices</span><h2>Every departure</h2>
      <p>Small groups, fixed dates. Prices are per pilot.</p></div>
    <div class="deps">
      <div class="dep dep-h" aria-hidden="true"><span>Expedition</span><span>Dates</span><span>Length</span><span>Group</span><span>Price</span><span>Status</span><span></span></div>{rows}
    </div>
  </section>

  <section class="sec sec-why">
    <div class="sec-head"><span class="kicker">Why fly with us</span><h2>Guided from launch to landing</h2></div>
    <div class="stats"><div><b>10</b><span>Years in the air</span></div><div><b>500+</b><span>Guided flights</span></div><div><b>4</b><span>Continents flown</span></div><div><b>90+</b><span>Podcast conversations with the sport's best</span></div></div>
    <div class="proof">
      <div><h3>Flight safety, first and always</h3><p>If it's controllable, then control it. On-site fixes, weather mastery and rescue readiness, every detail mastered beforehand.</p></div>
      <div><h3>Exclusive journeys</h3><p>Like-minded pilots who craft each trip with passion, creativity and teamwork, so every flight feels made for you.</p></div>
      <div><h3>Local, and giving back</h3><p>By flying with us you help uplift local communities through welfare, training and opportunities for the next generation.</p></div>
    </div>
  </section>

  <section class="sec sec-team">
    <div class="sec-head"><span class="kicker">Who guides</span><h2>The people in the air with you</h2></div>
    <div class="guides">{guides}</div>
  </section>

  <section class="film">
    <video data-src="{A}video/bir-1080" muted loop playsinline preload="none" aria-hidden="true"></video>
    {pic("destinations/india/hero/snowline", "", "film-pic")}
    <div class="film-cap"><span class="kicker">From the air</span><p>Bir Billing, above the snowline.</p><span class="log">Billing launch · about 2,400 m</span></div>
  </section>

  <section class="sec sec-pod">
    <div class="sec-head"><span class="kicker">The Paragliding Atlas Podcast</span><h2>We learn from the best, then we guide</h2>
      <p>90+ long-form conversations with the designers, test pilots and champions who shape free flight, every one with a full transcript.</p></div>
    <div class="guests">{guests}</div>
    <a class="btn btn-line" href="{V2}podcast.html">Listen to the podcast</a>
  </section>

  <section class="sec sec-kb">
    <div class="kb-media">{pic("images/kb-flight-mechanics", "Three-view drawing of a paraglider")}</div>
    <div class="kb-copy"><span class="kicker">Knowledge base</span><h2>The sport organised by subject</h2>
      <p>Flight mechanics, weather, equipment, risk: what the guests of the podcast know, arranged so you can prepare before you fly.</p>
      <a class="btn btn-line" href="{V2}knowledge-base.html">Enter the knowledge base</a></div>
  </section>

  <section class="cta">
    <span class="kicker">Booking open</span><h2>Book a free 30-minute call</h2>
    <p>Tell us your hours, your wing and the trip you are picturing. We match pilots to the right route, not seats to a schedule.</p>
    <div class="actions"><a class="btn btn-solid" href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">Book a call</a><a class="btn btn-line" href="https://wa.me/4796757456" target="_blank" rel="noopener">WhatsApp</a></div>
  </section>
</main>
''' + foot()


def trip(d):
    t = TRIPS[0]
    days = [("01", "Briefing", "The forecast, the plan and the traffic: where the climbs are likely to be, which way to head, and what to do if the day shuts down early."),
            ("02", "Up the hill", "Shared taxis up to Billing, about 45 minutes from Bir, usually four pilots to a car."),
            ("03", "Launch", "Almost always nil-wind, and there will be a queue. Lay out to the side, and once your wing is up, go."),
            ("04", "Fly", "Leave the house thermal as soon as you have the height for the next knob. The front range works for tens of kilometres.")]
    steps = "".join(f'<li><span class="step-n">{n}</span><h3>{e(h)}</h3><p>{e(p)}</p></li>' for n, h, p in days)
    deps = "".join(f'''<article class="depcard"><span class="kicker">India {e(tour)}</span><h3>{e(dates)}</h3>
        <p>{e(note)}</p><dl class="facts"><div><dt>Places</dt><dd>6</dd></div><div><dt>Per pilot</dt><dd class="price">£1,100</dd></div><div><dt>Status</dt><dd>Guaranteed to run</dd></div></dl>
        <a class="btn btn-solid" href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">Book this departure</a></article>'''
                   for tour, dates, note in (("Tour 1", "21 to 30 October 2026", "Arrive 21 Oct · eight flying days, 22 to 29 Oct · leave 30 Oct"),
                                             ("Tour 2", "3 to 12 November 2026", "Arrive 3 Nov · eight flying days, 4 to 11 Nov · leave 12 Nov")))
    return head(d, "Paragliding in Bir Billing, India | Direction " + d.upper(), "destinations/india.html") + nav(d) + f'''
<main>
  <section class="hero hero-trip">
    <div class="hero-media">{pic("destinations/india/hero/snowline", "A red paraglider above snow-covered Himalayan ridges", "hero-pic", True)}
      <video data-src="{A}video/bir-1080" muted loop playsinline preload="none" aria-hidden="true"></video></div>
    <div class="hero-copy">
      <span class="kicker">India · Bir Billing · Himalaya</span>
      <h1>Bir Billing</h1>
      <p class="lede">Big Mountain Flying: ten days on the Dhauladhar, the wall of the Himalaya above Bir.</p>
      <div class="actions"><a class="btn btn-solid" href="#book">Dates &amp; booking</a><a class="btn btn-line" href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">Book a call</a></div>
    </div>
  </section>
  <div class="factbar">
    <div><span>Next departure</span><b>21 to 30 Oct 2026</b></div><div><span>Length</span><b>10 days, 8 flying</b></div>
    <div><span>Level</span><b>IPPI 2 {level(4)}</b></div><div><span>Group</span><b>6 pilots, 1 guide to 3</b></div>
    <div><span>Per pilot</span><b class="price">£1,100</b></div><a class="btn btn-solid" href="#book">Book</a>
  </div>

  <section class="sec sec-over">
    <div class="sec-head"><span class="kicker">Overview</span><h2>The Majestic Himalayas: A Paraglider's Ultimate Frontier</h2></div>
    <div class="over">
      <p class="big">Our Himalayan expedition delivers an aerial experience that makes you soar over landscapes shaped by time and legend, you get to drift over ancient monasteries while exploring your limits in thin air.</p>
      <p>Bir is where it starts: one launch at Billing, a landing field at the edge of town, and a front range that pilots have been flying out and back along since the 1980s. The plan follows the conditions, not a timetable. On the ground, Bir has a kilometre of road with around a hundred restaurants, trails to walk, hot springs, and monasteries where you can sit in on the chanting.</p>
    </div>
    <div class="alt"><div><b>2,400 m</b><span>Billing launch</span></div><div><b>3,000 m+</b><span>Cloudbase in season</span></div><div><b>~70 km</b><span>Front range to the west</span></div><div><b>Oct to Nov</b><span>Peak season</span></div></div>
  </section>

  <section class="sec sec-day">
    <div class="sec-head"><span class="kicker">How a day runs</span><h2>From briefing to the landing field</h2></div>
    <ol class="steps">{steps}</ol>
  </section>

  <section class="film">
    <video data-src="{A}video/bir-1080" muted loop playsinline preload="none" aria-hidden="true"></video>
    {pic("destinations/india/gallery/over-the-peaks", "", "film-pic")}
    <div class="film-cap"><span class="kicker">From the air</span><p>Over the front range, towards Dharamshala.</p><span class="log">Dhauladhar front range · Kangra valley below</span></div>
  </section>

  <section class="sec sec-book" id="book">
    <div class="sec-head"><span class="kicker">Dates &amp; prices</span><h2>Two departures, autumn 2026</h2>
      <p>Both are guaranteed to run: we will not cancel either one for low numbers. Because both are less than 120 days away, the full £1,100 is due when you book, as set out in our booking terms.</p></div>
    <div class="depcards">{deps}</div>
  </section>

  <section class="sec sec-team">
    <div class="sec-head"><span class="kicker">Who guides</span><h2>One guide to every three pilots</h2></div>
    <div class="guides">{"".join(f'<article class="guide">' + (('<picture class="g-face"><source srcset="%s.webp" type="image/webp"><img src="%s.png" alt="%s" loading="lazy"></picture>' % (img, img, e(n))) if img else '<span class="g-face g-blank" aria-hidden="true">%s</span>' % e(n[:1])) + f'<h3>{e(n)}</h3><span class="kicker">{e(r)}</span><p>{e(b)}</p></article>' for n, r, img, b in GUIDES[:2])}</div>
  </section>

  <section class="sec sec-more">
    <p class="more">The routes map, the gallery, the full FAQ, the packing list and the flying etiquette keep their current design and follow here: <a href="{V2}destinations/india.html#route">see them on the current page</a>.</p>
  </section>

  <section class="cta">
    <span class="kicker">Booking open</span><h2>Ready to fly Bir?</h2>
    <p>A free 30-minute call: your hours, your wing, the right departure.</p>
    <div class="actions"><a class="btn btn-solid" href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener">Book a call</a><a class="btn btn-line" href="https://wa.me/4796757456" target="_blank" rel="noopener">WhatsApp</a></div>
  </section>
</main>
''' + foot()


def chooser():
    cards = "".join(f'''<article class="ch">
      <a class="ch-shot" href="home-{k}.html"><img src="img/shot-{k}.jpg" alt="Direction {k.upper()}, homepage" loading="lazy"></a>
      <div class="ch-body"><span class="ch-k">Direction {k.upper()} · {e(v["ref"])}</span><h2>{e(v["name"])}</h2><p>{e(v["gist"])}</p>
      <p class="ch-links"><a href="home-{k}.html">Homepage</a><a href="trip-{k}.html">Trip page (India)</a></p></div></article>'''
                    for k, v in DIRS.items())
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow"><title>Three directions | Paragliding Atlas</title>
<link rel="canonical" href="https://paraglidingatlas.com/"><link rel="stylesheet" href="../../fonts.css"><link rel="stylesheet" href="v3.css">
<style>
body{{background:#101114;color:#eee;font-family:"DM Sans",sans-serif;margin:0;padding:clamp(1.5rem,4vw,3.5rem)}}
h1{{font-family:Poppins,sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);margin:0 0 .4rem}} .intro{{color:#b4b4b4;max-width:62ch;line-height:1.7;margin:0 0 2.5rem}}
.chs{{display:grid;gap:2rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr))}}
.ch{{background:#17181c;border:1px solid #26272d}} .ch-shot img{{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top}}
.ch-body{{padding:1.4rem 1.5rem 1.6rem}} .ch-k{{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:#ff7517;font-weight:600}}
.ch h2{{font-family:Poppins,sans-serif;margin:.4rem 0 .5rem}} .ch p{{color:#b4b4b4;line-height:1.65;margin:0 0 1rem}}
.ch-links a{{display:inline-block;margin-right:1.2rem;color:#fff;font-weight:600;padding:.6rem 0;border-bottom:1px solid #ff7517;text-decoration:none}}
.note{{margin-top:2.5rem;color:#8a8a8a;font-size:.9rem;line-height:1.7;max-width:70ch}}
</style></head><body>
<h1>Three directions, one structure</h1>
<p class="intro">The same bookings-first site, three ways. Same content, same order: next departure, the expeditions, every date and price, why us, who guides, a film break, the podcast, the knowledge base, a call to book. Pick the one that feels like Paragliding Atlas; the whole site is then built in it. Grey <b>[to supply]</b> marks are facts only you can give.</p>
<div class="chs">{cards}</div>
<p class="note">Kept whatever the direction: the knowledge base door, the globe, the Kenya and India photo sequences, route maps and galleries, the episode pages' Horizon look and transcript sync, the library's stone tiles, the time-of-day sky and the motion work.</p>
</body></html>
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    for d in DIRS:
        open(os.path.join(OUT, "home-%s.html" % d), "w", encoding="utf-8").write(home(d))
        open(os.path.join(OUT, "trip-%s.html" % d), "w", encoding="utf-8").write(trip(d))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(chooser())
    print("v3: 3 directions, 7 pages")


if __name__ == "__main__":
    main()
