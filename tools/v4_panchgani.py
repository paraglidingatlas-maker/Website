#!/usr/bin/env python3
"""
Panchgani's destination page in v4 (chat 11, 24 Oct 2026; the owner: "it is a
proper tour which will need to have all its necessities like other destination
pages"). Run by hand, then the build:

    python3 tools/v4_panchgani.py && python3 tools/v4_build.py

It writes prototypes/v4/destinations/panchgani.html from the v4 Kenya page's
frame (head, nav, footer, the booking bar and the dst-* and kdates/kfaq
classes), and the hero photograph prototypes/v4/img/panchgani/plateau.jpg and
.webp: the opening's Panchgani ground with its wing put back where it flew
(the opening's `box`). The phone cut of the hero is tools/v4_phone_media.py's,
like the other trips'. Panchgani has no live page, so the canonical names the
address it will have; v2_check warns "no live twin", which is expected.

Every fact is the owner's (dates, length, place) or Vistasp Kharas's, from the
episode episodes/navigating-panchgani-vistasp-kharas.html, and says so; the
launch height, price, group size and pilot rating are the owner's to supply and
show as [to supply]. Idempotent: a second run writes the same bytes.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
OUT = os.path.join(V4, "destinations", "panchgani.html")
KENYA = os.path.join(V4, "destinations", "kenya.html")
URL = "https://paraglidingatlas.com/destinations/panchgani.html"
EP = "../episodes/navigating-panchgani-vistasp-kharas.html"
TBD = '<i class="v2-tbd">[to supply]</i>'

TITLE = "Panchgani: Paragliding the Sahyadri Tablelands | Paragliding Atlas"
OG_TITLE = "Panchgani: Paragliding the Sahyadri Tablelands"
DESC = ("An 8 day guided paragliding tour in Panchgani, India, 14 to 21 February 2027: the volcanic "
        "tablelands of the Sahyadri hills, where India held a pre World Cup.")
WHEN = "14 to 21 February 2027"

# the questions, each answer from the episode (Vistasp Kharas) or the owner's facts
FAQ = [
    ("Who is this tour for?", True,
     ["Pilots who can take off in strong wind and strong thermic conditions. Vistasp Kharas, who has flown "
      "Panchgani for more than ten years, advises an SIV course: the thermals can be punchy and there is wind "
      "in the mix. He would not send a pilot used only to alpine air with little knowledge of wind, because "
      "on the lee side the site is not forgiving.",
      "The pilot rating for the tour is %s." % TBD]),
    ("What wing should I bring?", False,
     ["A high B or a C is great, and even a low B does well; an A will be a bit frustrating. Do not bring your "
      "best wing: the take-off at Harrison's Folly is red dust, and the local pilots keep a second wing that "
      "is already red."]),
    ("How high does it get?", True,
     ["Take-off is at about 1,100 to 1,200 m, and in the peak of the season pilots climb to 3,000 to 4,000 m. "
      "The local rule: below 1,800 m, start looking for a safe landing, and stay off the terrain unless you "
      "know exactly what the wind is doing."]),
    ("Where do we land?", False,
     ["Top landing on the main tableland is forgiving late in the afternoon, once you know where the wind is "
      "from. In the valleys, land near a road in a field that has been cut: never standing crops or sugarcane. "
      "The power lines are above ground, so look for the poles and their shadows. The villagers are friendly, "
      "and a shared jeep back to town is cheap."]),
    ("How do I get there?", False,
     ["Panchgani is about two hours by road from Pune and four and a half to five hours from Mumbai. No train "
      "goes to Panchgani: take the train from Mumbai to Pune, about four hours, then a taxi or a bus.",
      "What the tour price covers is %s." % TBD]),
    ("What is the cancellation policy?", True,
     ['The deposit, when the balance is due and what happens if you cancel are all in the '
      '<a href="../terms.html#cancel-you">booking terms</a>. Read them before you book, and take out trip '
      'cancellation insurance.']),
]


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def hero_photo():
    """The opening's ground with its wing back in place, 1500 x 756 (written only when missing)."""
    d = os.path.join(V4, "img", "panchgani")
    jpg, webp = os.path.join(d, "plateau.jpg"), os.path.join(d, "plateau.webp")
    if os.path.exists(jpg) and os.path.exists(webp):
        return
    from PIL import Image
    os.makedirs(d, exist_ok=True)
    g = Image.open(os.path.join(V4, "img", "opening", "panchgani-ground.jpg")).convert("RGB")
    w = Image.open(os.path.join(V4, "img", "opening", "panchgani-wing.webp")).convert("RGBA")
    W, H = g.size
    box, pad = (0.4893, 0.4299, 0.5667, 0.5701), (0.0583, 0.0594)      # the opening's panchgani box and pad
    sw = (box[2] - box[0]) * W / (1 - 2 * pad[0])
    sh = (box[3] - box[1]) * H / (1 - 2 * pad[1])
    w = w.resize((round(sw), round(sh)), Image.LANCZOS)
    g.paste(w, (round(box[0] * W - pad[0] * sw), round(box[1] * H - pad[1] * sh)), w)
    g.save(jpg, "JPEG", quality=82, optimize=True, progressive=True)
    g.save(webp, "WEBP", quality=78, method=6)


def faq_html():
    out = []
    for i, (q, key, ps) in enumerate(FAQ, 1):
        body = "\n        ".join("<p>%s</p>" % p for p in ps)
        out.append('''      <details class="kfaq-item%s">
        <summary>
          <span class="kfaq-n">%02d</span>
          <h3>%s</h3>
          <span class="kfaq-mark" aria-hidden="true"></span>
        </summary>
        <div class="kfaq-body"><div class="kfaq-inner">
        %s
        </div></div>
      </details>''' % (" is-key" if key else "", i, q, body))
    return "\n".join(out)


BODY = '''<header class="khero pg-hero">
  <div class="khero-stage">
    <div class="khero-par">
      <div class="khero-slide is-on">
        <picture>
          <source srcset="../img/panchgani/plateau.webp" type="image/webp">
          <img style="object-position:54% 50%" src="../img/panchgani/plateau.jpg" width="1500" height="756"
            draggable="false" fetchpriority="high" alt="A pilot under a white wing, small against the plateau and the terraced fields of Panchgani">
        </picture>
      </div>
    </div>
  </div>
  <div class="khero-scrim" aria-hidden="true"></div>
  <div class="khero-copy">
    <span class="kicker">Sahyadri hills</span>
    <h1 class="dst-country">Panchgani</h1>
    <p class="dst-tag">The land of five hills: volcanic tablelands, sharp cliffs and punchy thermals, two hours from Pune.</p>
    <div class="dst-hero-cta">
      <a href="#dates" class="btn-solid" data-hover><span>Hold a place</span></a>
      <a href="https://calendar.app.google/HaJMYuiomt5Db9eh8" target="_blank" rel="noopener" class="btn-lines" data-hover>Book a Call</a>
    </div>
  </div>
  <p class="pg-credit">Photo by Michael Gebert / <a href="https://www.instagram.com/flywithandy_paragliding/" target="_blank" rel="noopener">@flywithandy_paragliding</a></p>
  <a class="khero-cue" href="#overview"><span>Scroll</span><i></i></a>
</header>

<div class="dst-jump">
  <div class="dst-jump-in">
    <a href="#overview">Overview</a>
    <a href="#dates">Dates</a>
    <a href="#from-the-show">From The Show</a>
    <a href="#faq">FAQ</a>
    <a href="#enquire" class="last">Enquire</a>
    <span class="v4u-jbook"><span class="v4u-jprice"><small>From</small> TBD</span><a href="#dates" class="btn-solid" data-hover><span>Hold a place</span></a></span>
  </div>
</div>

<section class="dst-spec v4t-spec">
  <div class="dst-spec-grid">
    <div class="dst-spec-item"><span class="l">Country</span><span class="v">India</span></div>
    <div class="dst-spec-item"><span class="l">Duration</span><span class="v">8 days</span></div>
    <div class="dst-spec-item"><span class="l">Dates</span><span class="v">14 to 21 Feb 2027</span></div>
    <div class="dst-spec-item"><span class="l">Launch</span><span class="v">TBD</span></div>
    <div class="dst-spec-item"><span class="l">Pilot rating</span><span class="v">TBD</span></div>
    <div class="dst-spec-item"><span class="l">Group</span><span class="v">TBD</span></div>
    <div class="dst-spec-item"><span class="l">Season</span><span class="v">November to March</span></div>
  </div>
</section>
TRUST

<div class="dst-shell">
<div class="dst-main">
<section class="dst-sec is-loud pg-ov" id="overview">
  <div class="dst-head">
    <span class="kicker">Overview</span>
    <h2>The Land Of Five Hills</h2>
  </div>
  <p class="dst-lede">Panchgani sits on the Sahyadri, the range that runs down India's west coast about 100&nbsp;km inland, on the volcanic tablelands of the Deccan: flat tops and sharp vertical cliffs. Vistasp Kharas grew up here and has flown it for more than ten years. He calls it far more technical than Bir: a 30&nbsp;km flight in Panchgani is as good as 100&nbsp;km in Bir Billing.</p>
  <div class="kov-quiet">
    <div class="kov-q">
      <h3>The height</h3>
      <p>Take-off sits at about 1,100 to 1,200&nbsp;m, and in the peak of the season pilots climb to 3,000 to 4,000&nbsp;m, so on a good day the height above the ground beats Bir's.</p>
    </div>
    <div class="kov-q">
      <h3>The air</h3>
      <p>The cliffs heat through the morning and throw up strong thermals. There are inversions at several layers, the wind can change direction every thousand metres, and each valley and bowl has its own wind.</p>
    </div>
    <div class="kov-q">
      <h3>The window</h3>
      <p>Every evening the sea breeze comes in from the coast, so the flying day is timed around it. In the time you get for cross country, it is glorious.</p>
    </div>
    <div class="kov-q">
      <h3>The season</h3>
      <p>November to March. The wind starts from the north-northeast and turns southeast towards spring, so the take-off is chosen to match. The tour flies in February, in the heart of it.</p>
    </div>
  </div>
  <figure class="pg-quote">
    <blockquote>If you get below 1800 meters, start looking for a safe landing. Don't get close to the terrain unless you really know what you're doing.</blockquote>
    <figcaption>Vistasp Kharas <a href="EP#c6">Navigating Panchgani, 24:38</a></figcaption>
  </figure>
  <p class="pg-wc">Panchgani held its first pre World Cup in 2019, with almost 100 pilots, and its second, the first run by the Paragliding Association of India, in 2024. The longest local line runs about 100&nbsp;km north west to Kamshet.</p>
</section>

<section class="dst-sec is-loud kdates pg-dates" id="dates">
  <div class="dst-head">
    <span class="kicker">Season Package</span>
    <h2>One Week On The Plateau</h2>
    <p>Eight days in Panchgani, two days after the last Kenya tour ends.</p>
  </div>
  <div class="kdates-band" aria-hidden="true">
    <div class="kdates-track">
      <i class="kdates-tick" style="--p:19.87"></i><i class="kdates-tick" style="--p:40.4"></i><i class="kdates-tick" style="--p:60.93"></i><i class="kdates-tick" style="--p:79.47"></i>
      <i class="kdates-tour" style="--a:69.54;--w:5.3;--i:0"><b>01</b></i>
    </div>
    <div class="kdates-months">
      <span style="--p:0">Nov</span><span style="--p:19.87">Dec</span><span style="--p:40.4">Jan</span><span style="--p:60.93">Feb</span><span style="--p:79.47">Mar</span>
    </div>
    <p class="kdates-legend">The season, November to March. The tour sits in the middle of February.</p>
  </div>
  <div class="kdates-grid">
    <article class="kdates-card">
      <div class="kdates-card-l">
        <span class="kdates-n">01</span>
        <h3>Panchgani Tour</h3>
        <p class="kdates-when"><time datetime="2027-02-14">14</time> to <time datetime="2027-02-21">21 February</time> 2027</p>
        <p class="kdates-meta">8 days &middot; Sahyadri hills</p>
      </div>
      <div class="kdates-card-r">
        <p class="kdates-price"><span>Starting from</span><b class="v2-tbd">[to supply]</b></p>
        <a href="../enquire.html?trip=panchgani&amp;when=14+to+21+February+2027" class="btn-solid" data-hover><span>Hold a place</span></a>
      </div>
    </article>
  </div>
  <p class="kdates-terms"><span class="v4t-hold-note">Hold a place sends an enquiry for that departure.</span></p>
</section>

<section class="dst-sec v4t-show" id="from-the-show">
  <div class="dst-head">
    <span class="kicker">Before You Come</span>
    <h2>Hear The Site From Someone Who Flies It</h2>
  </div>
  <a class="dst-rel" href="EP">
    <div class="dst-rel-body">
      <span>Podcast · Episode 9 · 54 min</span>
      <h3>Navigating Panchgani: Vistasp Kharas</h3>
      <p>Vistasp Kharas walks through Panchgani ahead of the pre World Cup held there, covering what the site asks of a pilot and what to expect from competition flying in India.</p>
    </div>
  </a>
</section>

<section class="dst-sec is-quiet kfaq" id="faq">
  <div class="kfaq-wrap">
    <div class="kfaq-rail">
      <span class="kicker">Questions</span>
      <h2>What Pilots Ask Before Booking</h2>
      <details class="v4-fold v4t-fnote"><summary>About these questions</summary><p class="kfaq-note">The answers on the site come from Vistasp Kharas, on the show. If yours is not here, ask it on the call.</p></details>
      <a class="kfaq-cta" href="#enquire">Book a call</a>
    </div>
    <div class="kfaq-list">
FAQS
    </div>
  </div>
</section>

</div>
</div>

<script>
/* the season band draws its tour bar once it comes into view (Kenya's overview script does this there) */
(function () {
  var kd = document.querySelector('.kdates');
  if (!kd) return;
  if (!('IntersectionObserver' in window)) { kd.classList.add('is-on'); return; }
  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    kd.classList.add('is-on'); o.disconnect();
  }, { threshold: 0.3 }).observe(kd);
})();
</script>

'''

STYLE = '''<style>
/* Panchgani (tools/v4_panchgani.py): one photo, so no rail; the photographer's credit on it */
.pg-hero .pg-credit{position:absolute;right:var(--gutter);bottom:clamp(1rem,2.4vw,1.6rem);z-index:3;margin:0;
  font-size:var(--fs-small,.75rem);color:var(--gray-light);letter-spacing:.02em}
.pg-hero .pg-credit a{color:inherit;text-decoration:underline;text-underline-offset:2px}
.pg-ov .kov-quiet{margin-top:clamp(1.6rem,3vw,2.4rem)}
.pg-quote{margin:clamp(2rem,4vw,3rem) 0 0;padding-left:1.1rem;border-left:2px solid var(--orange);max-width:44rem}
.pg-quote blockquote{margin:0;font-family:var(--font-display);font-weight:600;color:var(--white);
  font-size:clamp(1.1rem,2vw,1.45rem);line-height:1.35}
.pg-quote figcaption{margin-top:.6rem;color:var(--gray);font-size:.85rem}
.pg-quote figcaption a{color:var(--gray-light)}
.pg-wc{margin:clamp(1.6rem,3vw,2.2rem) 0 0;color:var(--gray-light);max-width:44rem}
.pg-dates .kdates-grid{grid-template-columns:1fr}
@media (max-width:640px){.pg-hero .pg-credit{left:var(--gutter);right:var(--gutter);top:6.4rem;bottom:auto}}
</style>
'''


def site_schema(head):
    """Kenya's site-schema block with this page's WebPage and FAQPage."""
    m = re.search(r'(<!-- site-schema -->\s*<script type="application/ld\+json">)(.*?)(</script>\s*<!-- /site-schema -->)', head, re.S)
    data = json.loads(m.group(2))
    graph = []
    for node in data["@graph"]:
        if node.get("@type") == "WebPage":
            node = dict(node, **{"@id": URL + "#webpage", "url": URL, "dateModified": "2026-10-24", "name": TITLE})
        elif node.get("@type") == "FAQPage":
            node = {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(
                    re.sub(r"\s+", " ", plain(p.replace(TBD, "to be confirmed"))).strip() for p in ps)}}
                for q, _, ps in FAQ]}
        graph.append(node)
    data["@graph"] = graph
    return head[:m.start()] + m.group(1) + "\n" + json.dumps(data, indent=1, ensure_ascii=False) + "\n" + m.group(3) + head[m.end():]


def build():
    k = open(KENYA, encoding="utf-8").read()
    b = k.index("<body")
    head, rest = k[:b], k[b:]

    # head: title, description, canonical, social, the trip's own data, the page's own <style>
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, head, count=1)
    for name in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % name, r"\g<1>%s\2" % DESC, head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r"\g<1>%s\2" % OG_TITLE, head, count=1)
    # og:image: where the switch-over puts v4's images (like the canonical, the address it will have)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                  r"\1https://paraglidingatlas.com/assets/v4/img/panchgani/plateau.jpg\2", head, count=1)
    head = head.replace("https://paraglidingatlas.com/destinations/kenya.html", URL)
    trip = {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Panchgani Paragliding Tour",
            "description": "An 8 day guided paragliding tour in Panchgani, in the Sahyadri hills of India.",
            "itinerary": {"@type": "Place", "name": "Panchgani", "geo": {"@type": "GeoCoordinates", "latitude": 17.92, "longitude": 73.82}},
            "provider": {"@type": "Organization", "name": "Paragliding Atlas", "url": "https://paraglidingatlas.com/"},
            "subTrip": [{"@type": "TouristTrip", "name": "Panchgani Tour", "startDate": "2027-02-14", "endDate": "2027-02-21"}]}
    head = re.sub(r'<script type="application/ld\+json">\n\{"@context":"https://schema.org","@type":"TouristTrip".*?</script>',
                  lambda _: '<script type="application/ld+json">\n%s\n</script>' % json.dumps(trip, separators=(",", ":"), ensure_ascii=False),
                  head, count=1, flags=re.S)
    head = site_schema(head)
    head = head.replace('<link rel="stylesheet" href="../../../destinations.css', STYLE + '<link rel="stylesheet" href="../../../destinations.css', 1)

    # the frame: nav (its coordinates), then the page; the enquiry band, booking bar and footer from Kenya
    nav = rest[:rest.index('<header class="khero">')]
    nav = re.sub(r'<span class="nav-coords">[^<]*</span>', '<span class="nav-coords">17.9200°N · 73.8200°E</span>', nav, count=1)
    trust = re.search(r'<aside class="v4t-trust".*?</aside>', rest, re.S).group(0)
    tail = rest[rest.index('<section class="cta-band" id="enquire">'):]
    tail = re.sub(r'<span class="n">.*?</span><span class="w">.*?</span></span></div>',
                  '<span class="n"><small>From</small> %s</span><span class="w"><span>8 days</span> &middot; '
                  '<span>Next departure 14 Feb 2027</span></span></div>' % TBD, tail, count=1, flags=re.S)
    # the scripts this page uses: the booking bar, the FAQ heights, the folds; not the slideshow,
    # the fly-through, the packing list or the etiquette run, which have no section here
    for marker in ("/* Hero. Five photographs", "/* Overview prototype.", "/* Packing kit:", "/* Flying Etiquette:"):
        i = tail.index(marker)
        a = tail.rindex("<script>", 0, i)
        z = tail.index("</script>", i) + len("</script>")
        tail = tail[:a].rstrip(" \n") + "\n" + tail[z:].lstrip("\n")

    body = (BODY.replace("TRUST", trust).replace("FAQS", faq_html()).replace("EP", EP)
            .replace(">TBD<", ">%s<" % TBD).replace("</small> TBD<", "</small> %s<" % TBD))
    page = head + nav + body + tail
    page = page.replace("—", ",")      # no em dashes
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)


def main():
    hero_photo()
    build()
    print("v4_panchgani: wrote %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
