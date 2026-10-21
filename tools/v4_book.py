#!/usr/bin/env python3
"""
The booking flow (owner, 21 Oct 2026: "activate the Hold a place / Book now
buttons by enabling a high-end booking system matching the vibe of the site").

    prototypes/v4/book.html

Built on the enquiry page's shell (head, menu, footer from
prototypes/v4/enquire.html, which stays as it is). Three steps on one page:

  1. Pick a departure. The four departures the trip pages list, as a choice;
     a link from a trip (book.html?trip=india&when=21+to+30+October+2026, the
     same query the Hold a place links already pass to enquire.html) arrives
     with that departure chosen.
  2. Who you are. Name, email, phone, country, licence, hours, wing, an
     emergency contact, how they heard of the trip.
  3. Hold the place. "Hold with a deposit" pays by card through
     booking-worker.js (Stripe Checkout) and comes back here with the
     reference; "Book a free 30-minute call" records the hold as deposit
     pending and opens the calendar. The amount due is shown only where the
     site states it (India: the full £1,100, both departures being within 120
     days, as the trip page says); where it does not (Kenya), it shows
     [to supply] and the deposit button is disabled with a note.

A confirmation in the instrument style (what was held, what happens next, the
reference to quote) replaces the form once the relay answers, and again on the
way back from Stripe (book.html?ref=PA-2026-XXXX). Without JavaScript the form
is a plain POST to the relay, which answers with its own plain confirmation.
Reduced motion: nothing moves. Nothing on the page is invented: every fact is
the trip pages' or the terms'; a missing one shows as [to supply].

Prototype only (tools/v2_site.py PROTO_ONLY) until the relay is deployed and
ENDPOINT below is filled in; noindex like every v4 page.

    python3 tools/v4_book.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "enquire.html")
OUT = os.path.join(V4, "book.html")

# The deployed booking-worker.js URL, e.g. "https://booking.paraglidingatlas.workers.dev".
# Empty: the page explains the relay is not connected yet and offers the call.
ENDPOINT = ""

CALENDAR = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
WHATSAPP = "https://wa.me/4796757456"
EMAIL = "aninder@paraglidingatlas.com"

# The departures, exactly as the trip pages state them. `due` is what the
# site says is payable when you book; None means the site does not say.
DEPS = [
    {"id": "india-1", "trip": "india", "title": "India Tour 1", "place": "Bir Billing",
     "when": "21 to 30 October 2026", "len": "10 days", "places": "6 places",
     "status": "Guaranteed to run", "price": "£1,100", "price_l": "per pilot", "due": "£1,100"},
    {"id": "india-2", "trip": "india", "title": "India Tour 2", "place": "Bir Billing",
     "when": "3 to 12 November 2026", "len": "10 days", "places": "6 places",
     "status": "Guaranteed to run", "price": "£1,100", "price_l": "per pilot", "due": "£1,100"},
    {"id": "kenya-1", "trip": "kenya", "title": "Kenya Tour 1", "place": "Kerio Valley",
     "when": "18 to 29 January 2027", "len": "12 days", "places": "",
     "status": "", "price": "Enquire for prices", "price_l": "", "due": None},
    {"id": "kenya-2", "trip": "kenya", "title": "Kenya Tour 2", "place": "Kerio Valley",
     "when": "1 to 12 February 2027", "len": "12 days", "places": "",
     "status": "", "price": "Enquire for prices", "price_l": "", "due": None},
]

# What the site says about the sum due, by trip. India: the trip page's own
# line under its departures table. Kenya: the page says only "Enquire for prices".
DUE_NOTE = {
    "india": "Both India departures are less than 120 days away, so the full £1,100 is due when you book, "
             "as the trip page and the booking terms set out. Deposits are not refunded (booking terms, section 5).",
    "kenya": "The deposit for Kenya is [to supply]. Until it is set, hold the place by booking a call and we will "
             "take it from there.",
}

HEAD_META = """<title>Hold a Place | Paragliding Atlas</title>
<meta name="description" content="Hold your place on a Paragliding Atlas trip: pick the departure, tell us who you are, then hold it with a deposit or book a free 30-minute call first.">
<link rel="canonical" href="https://paraglidingatlas.com/book.html">
<meta property="og:type" content="website">
<meta property="og:title" content="Hold a Place">
<meta property="og:description" content="Hold your place on a Paragliding Atlas trip: pick the departure, tell us who you are, then hold it with a deposit or book a free 30-minute call first.">
<meta property="og:image" content="https://paraglidingatlas.com/assets/images/hero.jpg">
<meta property="og:url" content="https://paraglidingatlas.com/book.html">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://paraglidingatlas.com/book.html#webpage",
  "name": "Hold a Place",
  "url": "https://paraglidingatlas.com/book.html",
  "isPartOf": {
    "@id": "https://paraglidingatlas.com/#website"
  },
  "publisher": {
    "@id": "https://paraglidingatlas.com/#organization"
  },
  "inLanguage": "en",
  "dateModified": "2026-10-21"
}
</script>"""

CSS = r"""
/* The booking flow (tools/v4_book.py). Tokens and chrome from styles.css and v2.css;
   the fields are the enquiry page's. Phone first: one column, the wide screen
   adds a second where a pair reads better. */
.bk-hero{padding-bottom:var(--sp-3)}
.bk-hero .kit-intro{max-width:52ch}
.bk-wrap{padding:0 clamp(1.2rem,5vw,5.5rem) clamp(3rem,7vw,5rem);max-width:calc(var(--measure) + 2*clamp(1.2rem,5vw,5.5rem));margin:0 auto}
.bk-form{max-width:46rem}
/* The three steps, as a rail. The hairline under each lights as the step is done. */
.bk-rail{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6rem;list-style:none;margin:0 0 var(--sp-5);padding:0}
.bk-rail li{position:relative;padding:.7rem 0 0;border-top:1px solid var(--edge);font-size:var(--fs-small);color:var(--gray);line-height:1.4}
.bk-rail li::before{content:"";position:absolute;left:0;top:-1px;height:1px;width:0;background:var(--orange);transition:width .5s var(--ease)}
.bk-rail li.is-on{color:var(--white)}
.bk-rail li.is-on::before{width:2rem}
.bk-rail li.is-done::before{width:100%}
.bk-rail b{display:block;font-family:var(--font-mono);font-weight:500;font-size:var(--fs-micro);letter-spacing:.1em;color:var(--orange);margin-bottom:.15rem}
.bk-step{border:0;padding:0;margin:0 0 var(--sp-5)}
.bk-step legend{display:flex;align-items:baseline;gap:.8rem;font-family:var(--font-display);font-weight:700;font-size:var(--fs-h3);line-height:1.15;letter-spacing:-.015em;color:var(--white);margin:0 0 .4rem;padding:0}
.bk-step legend i{font:500 var(--fs-micro)/1 var(--font-mono);letter-spacing:.12em;color:var(--orange)}
.bk-step .enq-legend-note{margin-bottom:1.3rem}
/* Departures: a choice, each a row of the departures table. */
.bk-deps{display:grid;gap:.6rem;margin:0}
.bk-dep{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:.3rem 1rem;align-items:start;padding:1rem 1.1rem;background:var(--card);border:1px solid var(--line);cursor:pointer;color:var(--white);transition:border-color .25s var(--ease),background .25s var(--ease)}
.bk-dep input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
.bk-dep .n{font-family:var(--font-mono);font-size:var(--fs-micro);letter-spacing:.12em;color:var(--gray);padding-top:.25rem}
.bk-dep .t{font-family:var(--font-display);font-weight:600;font-size:1.05rem;line-height:1.3}
.bk-dep .t small{display:block;font:400 var(--fs-small)/1.5 var(--font-body);color:var(--gray-light)}
.bk-dep .w{grid-column:2;font-family:var(--font-mono);font-size:var(--fs-body-s);color:var(--white);font-variant-numeric:tabular-nums}
.bk-dep .m{grid-column:2;font-size:var(--fs-small);color:var(--gray-light)}
.bk-dep .m .v2-status{display:inline;margin:0 0 0 .6rem;font-size:var(--fs-micro)}
.bk-dep .p{grid-column:3;grid-row:1 / span 3;text-align:right;font-family:var(--font-display);font-weight:700;font-size:1.05rem;color:var(--white);white-space:nowrap}
.bk-dep .p small{display:block;font:400 var(--fs-micro)/1.5 var(--font-body);color:var(--gray)}
.bk-dep .p.is-ask{font:500 var(--fs-small)/1.4 var(--font-body);color:var(--gray-light);white-space:normal;max-width:7rem}
.bk-dep:hover{border-color:var(--live)}
.bk-dep:has(input:focus-visible){outline:2px solid var(--orange);outline-offset:2px}
.bk-dep:has(input:checked){border-color:var(--orange);background:radial-gradient(120% 120% at 0% 0%,rgba(255,117,23,.1) 0%,var(--card) 60%)}
.bk-dep:has(input:checked) .n{color:var(--orange)}
@media (max-width:560px){.bk-dep{grid-template-columns:auto minmax(0,1fr)}.bk-dep .p{grid-column:2;grid-row:auto;text-align:left;margin-top:.2rem}.bk-dep .p small{display:inline;margin-left:.4rem}.bk-dep .p.is-ask{max-width:none}}
.bk-note{color:var(--gray);font-size:var(--fs-small);line-height:1.6;margin:.9rem 0 0}
/* Hold the place: two panels, the sum as a readout. */
.bk-hold{display:grid;gap:var(--sp-3)}
@media (min-width:700px){.bk-hold{grid-template-columns:repeat(2,minmax(0,1fr))}}
.bk-panel{display:flex;flex-direction:column}
.bk-panel h3{margin-bottom:.6rem}
.bk-panel p{margin-bottom:1rem}
.bk-panel .spacer{flex:1 1 auto}
.bk-sum{display:grid;grid-template-columns:auto minmax(0,1fr);gap:.4rem 1rem;margin:0 0 1rem;padding:.8rem 0 .9rem;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.bk-sum dt{font-size:var(--fs-micro);font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--orange);padding-top:.25rem}
.bk-sum dd{margin:0;font-family:var(--font-mono);font-size:1.15rem;color:var(--white);font-variant-numeric:tabular-nums}
.bk-sum dd.is-sm{font-family:var(--font-body);font-size:var(--fs-body-s);color:var(--gray-light)}
.bk-panel .btn-solid[disabled],.bk-panel .btn-solid[aria-disabled=true]{opacity:.45;cursor:not-allowed}
.bk-panel .btn-solid,.bk-panel .listen-btn{align-self:flex-start}
.bk-panel .bk-note{margin-top:.8rem}
.bk-relay{margin:1.2rem 0 0}
/* The confirmation: an instrument. */
.bk-held{max-width:46rem}
.bk-held .v2-status{margin:0 0 .6rem}
.bk-held p.bk-ref{font-family:var(--font-mono);font-weight:500;font-size:clamp(1.8rem,5vw,2.6rem);letter-spacing:.04em;color:var(--white);line-height:1.1;margin:0 0 .4rem}
.bk-held p.bk-ref-l{font-size:var(--fs-micro);font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin:0 0 .2rem}
.bk-held p.quote{font-size:var(--fs-small)}
.bk-read{display:grid;grid-template-columns:auto minmax(0,1fr);gap:.55rem 1.2rem;margin:var(--sp-3) 0 0;padding:var(--sp-2) 0 0;border-top:1px solid var(--line)}
.bk-read dt{font-size:var(--fs-micro);font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gray);padding-top:.2rem}
.bk-read dd{margin:0;font-family:var(--font-mono);font-size:var(--fs-body-s);color:var(--white);line-height:1.5}
.bk-next{margin:var(--sp-4) 0 0;padding:0 0 0 1.4rem;color:var(--gray-light);font-size:var(--fs-body-s);line-height:1.7}
.bk-next li{margin:0 0 .5rem}
.bk-next li::marker{font-family:var(--font-mono);color:var(--orange)}
.bk-held .row{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:var(--sp-3)}
.bk-held .quote{margin-top:var(--sp-3);color:var(--gray);font-size:var(--fs-small)}
.bk-held .quote b{font-family:var(--font-mono);font-weight:500;color:var(--white)}
.bk-aside{margin-top:var(--sp-5);border-left:2px solid var(--rule);padding-left:1.3rem;border-image:linear-gradient(180deg,var(--rule),transparent) 1;max-width:46rem}
.bk-aside h3{font-family:var(--font-display);font-weight:600;color:var(--white);font-size:.98rem;margin:0 0 .6rem}
.bk-aside p{color:var(--gray-light);font-size:.9rem;line-height:1.75;margin:0 0 1.2rem}
.bk-aside a,.bk-note a,.bk-panel p a{color:var(--orange)}
[hidden]{display:none !important}
@media (prefers-reduced-motion:reduce){.bk-rail li::before,.bk-dep{transition:none}}
@media (pointer:coarse){.bk-dep{min-height:44px}}
"""


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def dep_html(i, d):
    meta = d["len"]
    if d["places"]:
        meta += " &middot; " + d["places"]
    status = ('<span class="v2-status is-go">%s</span>' % d["status"]) if d["status"] else ""
    if d["price_l"]:
        price = '<span class="p">%s<small>%s</small></span>' % (d["price"], d["price_l"])
    else:
        price = '<span class="p is-ask">%s</span>' % d["price"]
    return (
        '<label class="bk-dep">'
        '<input type="radio" name="departure" value="%s" data-trip="%s" data-when="%s" required>'
        '<span class="n">%02d</span>'
        '<span class="t">%s<small>%s</small></span>'
        '<span class="w">%s</span>'
        '<span class="m">%s%s</span>'
        '%s'
        '</label>'
    ) % (d["id"], d["trip"], esc(d["when"]), i, d["title"], d["place"], d["when"], meta, status, price)


def body():
    deps = "\n".join(dep_html(i + 1, d) for i, d in enumerate(DEPS))
    return """<header class="kit-hero is-sky v2-page-hero bk-hero">
  <div class="kit-hero-copy">
    <span class="kit-kicker">Hold A Place</span>
    <h1>Hold Your Place <em class="v2-accent">On The Trip</em></h1>
    <p class="kit-intro">Three steps. Pick the departure, tell us who you are, then hold the place with a deposit, or book a free call first if you would rather talk it through.</p>
  </div>
</header>

<div class="bk-wrap">
  <form id="bkForm" class="bk-form" method="post" action="%(action)s" novalidate>
    <ol class="bk-rail" id="bkRail" aria-label="The three steps">
      <li class="is-on" data-step="1"><b>01</b>Departure</li>
      <li data-step="2"><b>02</b>Who you are</li>
      <li data-step="3"><b>03</b>Hold the place</li>
    </ol>

    <fieldset class="bk-step" id="step1" data-step="1">
      <legend><i>01</i>Pick a departure</legend>
      <p class="enq-legend-note">The four departures on the trip pages. Dates, length and price are as the trip pages state them.</p>
      <div class="bk-deps" role="radiogroup" aria-label="Departure">
%(deps)s
      </div>
      <p class="bk-note">Both India departures are guaranteed to run: we will not cancel either one for low numbers. Kenya is priced on enquiry.</p>
    </fieldset>

    <fieldset class="bk-step" id="step2" data-step="2">
      <legend><i>02</i>Who you are</legend>
      <p class="enq-legend-note">So we can confirm the place, reach you on the day, and be sure the trip is right for you. Telling us you are less current than you would like is more useful than telling us you are fine.</p>
      <div class="enq-row">
        <div class="enq-field">
          <label for="name">Your name</label>
          <input type="text" id="name" name="name" autocomplete="name" required data-err="Your name, as it is in your passport.">
        </div>
        <div class="enq-field">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" autocomplete="email" required data-err="The confirmation goes to this address, so it needs to be right.">
        </div>
      </div>
      <div class="enq-row">
        <div class="enq-field">
          <label for="phone">Phone <span class="opt">(with the country code)</span></label>
          <input type="tel" id="phone" name="phone" autocomplete="tel" required data-err="A number we can reach you on, with the country code.">
        </div>
        <div class="enq-field">
          <label for="country">Where you are based</label>
          <input type="text" id="country" name="country" autocomplete="country-name" required data-err="The country you will be travelling from.">
        </div>
      </div>
      <div class="enq-row">
        <div class="enq-field">
          <label for="rating">Licence or rating</label>
          <input type="text" id="rating" name="rating" placeholder="IPPI 2, APPI, national licence" required data-err="This is a tour for autonomous pilots: IPPI 2 or a national licence.">
        </div>
        <div class="enq-field">
          <label for="total">Total airtime <span class="opt">(hours, roughly)</span></label>
          <input type="text" id="total" name="total" inputmode="numeric" required data-err="Hours in total, roughly.">
        </div>
      </div>
      <div class="enq-row">
        <div class="enq-field">
          <label for="recent">Hours in the last 12 months</label>
          <input type="text" id="recent" name="recent" inputmode="numeric" required data-err="Hours in the last twelve months. Less than you would like is a fine answer.">
        </div>
        <div class="enq-field">
          <label for="wing">Wing you fly <span class="opt">(make, model, EN class)</span></label>
          <input type="text" id="wing" name="wing" placeholder="Make, model, EN class" required data-err="The wing you will bring, with its EN class.">
        </div>
      </div>
      <div class="enq-row">
        <div class="enq-field">
          <label for="ice_name">Emergency contact</label>
          <input type="text" id="ice_name" name="ice_name" placeholder="Name" required data-err="Someone we can call if we need to.">
        </div>
        <div class="enq-field">
          <label for="ice_phone">Their phone</label>
          <input type="tel" id="ice_phone" name="ice_phone" placeholder="With the country code" required data-err="Their number, with the country code.">
        </div>
      </div>
      <div class="enq-field">
        <label for="heard">How you heard of the trip <span class="opt">(optional)</span></label>
        <select id="heard" name="heard">
          <option value="">Choose one</option>
          <option>The podcast</option>
          <option>YouTube</option>
          <option>Instagram</option>
          <option>Another pilot</option>
          <option>A search</option>
          <option>Somewhere else</option>
        </select>
      </div>
      <div class="enq-consent">
        <input type="checkbox" id="consent" name="consent" required data-err="Please read the terms and tick the box; a hold is a booking once it is confirmed.">
        <label for="consent">I have read the <a href="terms.html">booking terms</a> and the <a href="participant-agreement.html">participant agreement</a>, and I am happy for Paragliding Atlas to use these details to hold my place and to send me the booking confirmation and the welcome kit. They are not sold or shared for marketing, and I can ask for them to be deleted at any time. See the <a href="privacy-policy.html">Privacy Policy</a>.</label>
      </div>
    </fieldset>

    <fieldset class="bk-step" id="step3" data-step="3">
      <legend><i>03</i>Hold the place</legend>
      <p class="enq-legend-note">Two ways. Pay the sum due now by card and the place is yours, or hold it and book a call first; nothing is paid until we have spoken.</p>
      <div class="bk-hold">
        <div class="kit-panel bk-panel">
          <h3>Hold with a deposit</h3>
          <dl class="bk-sum">
            <dt>Departure</dt><dd id="sumDep">Choose one above</dd>
            <dt>Due now</dt><dd id="sumDue">[to supply]</dd>
          </dl>
          <p id="sumNote">Pick a departure and the sum due appears here.</p>
          <span class="spacer"></span>
          <button type="submit" class="btn-solid" name="mode" value="deposit" id="btnDeposit" data-hover disabled><span>Hold with a deposit</span></button>
          <p class="bk-note" id="depositNote">You pay by card on Stripe's page and come straight back here with your reference.</p>
        </div>
        <div class="kit-panel bk-panel">
          <h3>Book a free 30-minute call</h3>
          <p>Not sure yet, or a question first? Hold the place now and book a call. We talk through your flying and the trip, and the deposit waits until we have spoken.</p>
          <span class="spacer"></span>
          <button type="submit" class="listen-btn" name="mode" value="call" id="btnCall" data-hover><span>Book a free 30-minute call</span></button>
          <p class="bk-note">The place is held under your name and a reference. The call link comes next.</p>
        </div>
      </div>
      <!-- Spam traps, read by the relay. A person never sees or fills "website";
           a bot fills every field. "t" is stamped by the script. -->
      <div aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden;">
        <label for="website">Leave this empty</label>
        <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
      </div>
      <input type="hidden" id="t" name="t" value="">
      <input type="hidden" name="page" value="book.html">
      <p class="enq-status" id="bkStatus" role="status" aria-live="polite"></p>
      <noscript><p class="bk-note">Without JavaScript the form still sends: our relay answers with a plain confirmation page carrying your reference.</p></noscript>
    </fieldset>
  </form>

  <section class="kit-panel bk-held" id="bkHeld" hidden aria-live="polite" tabindex="-1">
    <span class="v2-status is-go">Held</span>
    <p class="bk-ref-l">Your reference</p>
    <p class="bk-ref" id="heldRef">PA-2026-0000</p>
    <dl class="bk-read">
      <dt>Trip</dt><dd id="heldTrip"></dd>
      <dt>Dates</dt><dd id="heldWhen"></dd>
      <dt>Payment</dt><dd id="heldPay"></dd>
      <dt>Confirmation to</dt><dd id="heldEmail"></dd>
    </dl>
    <ol class="bk-next" id="heldNext"></ol>
    <div class="row" id="heldRow"></div>
    <p class="quote">Quote <b id="heldRef2"></b> in any message about this booking.</p>
  </section>

  <aside class="bk-aside">
    <h3>What happens to this</h3>
    <p>Pressing either button passes your details through a small relay of our own, running on Cloudflare. It keeps the hold under your reference, takes the card payment on Stripe's own page if you pay now, and sends you the confirmation and, two days later, the welcome kit. Your card details never touch our relay or this site.</p>
    <h3>Before you book</h3>
    <p>Worth reading either way: the <a href="terms.html">booking terms</a>, and the <a href="participant-agreement.html">participant agreement</a> that every pilot completes before a trip. Both are published in full rather than sprung on you later.</p>
    <h3>Rather ask first?</h3>
    <p><a href="enquire.html">Send an enquiry</a>, message on <a href="%(wa)s" target="_blank" rel="noopener">WhatsApp</a>, or email <a href="mailto:%(email)s">%(email)s</a>.</p>
  </aside>
</div>
""" % {"deps": deps, "action": (ENDPOINT + "/hold") if ENDPOINT else "", "wa": WHATSAPP, "email": EMAIL}


SCRIPT = r"""<script>
/* The booking flow. One script, three jobs: open on the departure a trip link
   names, keep step 3's readout true to the departure chosen, and send the hold
   to the relay. Without ENDPOINT the page says the relay is not connected and
   offers the call. Nothing here moves on its own. */
(function () {
  var ENDPOINT = %(endpoint)s;
  var CALENDAR = %(calendar)s, WHATSAPP = %(whatsapp)s, EMAIL = %(email)s;
  var DEPS = %(deps)s, NOTE = %(notes)s;
  var d = document, form = d.getElementById('bkForm'), status = d.getElementById('bkStatus');
  if (!form) return;
  var held = d.getElementById('bkHeld');
  var q; try { q = new URLSearchParams(location.search); } catch (e) { q = { get: function () { return null; } }; }

  function byId(id) { for (var i = 0; i < DEPS.length; i++) if (DEPS[i].id === id) return DEPS[i]; return null; }
  function chosen() { var r = form.querySelector('input[name="departure"]:checked'); return r ? byId(r.value) : null; }
  function text(id, v) { var e = d.getElementById(id); if (e) e.textContent = v; }

  /* Time trap stamp, read by the relay. */
  var stamp = d.getElementById('t'); if (stamp) stamp.value = String(Date.now());

  /* 1. A trip link arrives as ?trip=india&when=21+to+30+October+2026. */
  (function () {
    var trip = (q.get('trip') || '').toLowerCase(), when = q.get('when') || '';
    var radios = form.querySelectorAll('input[name="departure"]'), hit = null;
    for (var i = 0; i < radios.length; i++) {
      var r = radios[i];
      if (r.getAttribute('data-trip') === trip && (!when || r.getAttribute('data-when') === when)) { hit = r; break; }
    }
    if (hit) hit.checked = true;
  })();

  /* 2. Step 3 reads the departure. */
  var btnDeposit = d.getElementById('btnDeposit');
  function readout() {
    var dep = chosen();
    if (!dep) { text('sumDep', 'Choose one above'); text('sumDue', '[to supply]'); text('sumNote', 'Pick a departure and the sum due appears here.'); btnDeposit.disabled = true; return; }
    text('sumDep', dep.title + ', ' + dep.when);
    text('sumDue', dep.due || '[to supply]');
    text('sumNote', NOTE[dep.trip] || '');
    btnDeposit.disabled = !dep.due || !ENDPOINT;
  }
  form.addEventListener('change', readout);
  readout();

  /* The rail: a step is done when every field in it is valid. */
  var rail = d.getElementById('bkRail');
  function stepOk(n) {
    var fs = d.getElementById('step' + n), els = fs.querySelectorAll('input,select');
    for (var i = 0; i < els.length; i++) if (els[i].willValidate && !els[i].checkValidity()) return false;
    return true;
  }
  function light() {
    var on = false;
    for (var n = 1; n <= 3; n++) {
      var li = rail.querySelector('[data-step="' + n + '"]'), ok = n === 3 ? (stepOk(1) && stepOk(2)) : stepOk(n);
      li.classList.toggle('is-done', ok && n < 3);
      li.classList.toggle('is-on', !on && !(ok && n < 3));
      if (!on && !(ok && n < 3)) on = true;
    }
  }
  form.addEventListener('input', light); form.addEventListener('change', light); light();

  /* Validation that explains, in the page's words (data-err), inline under the field. */
  var tried = false;
  function holder(el) { return el.type === 'checkbox' ? el.closest('.enq-consent') : el.type === 'radio' ? el.closest('.bk-deps') : el.closest('.enq-field'); }
  function msg(el, make) {
    var id = (el.id || el.name) + '-err', m = d.getElementById(id);
    if (!m && make) { m = d.createElement('p'); m.className = 'enq-err'; m.id = id; var h = holder(el) || el.parentNode; if (el.type === 'checkbox' || el.type === 'radio') h.parentNode.insertBefore(m, h.nextSibling); else h.appendChild(m); }
    return m;
  }
  function check(el) {
    var bad = !el.checkValidity(), m = msg(el, bad);
    if (bad) { m.textContent = el.getAttribute('data-err') || (el.type === 'radio' ? 'Pick one of the four departures.' : el.validationMessage); el.setAttribute('aria-invalid', 'true'); el.setAttribute('aria-describedby', m.id); }
    else { if (m) m.parentNode.removeChild(m); el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby'); }
    return !bad;
  }
  function fields() { return [].filter.call(form.elements, function (el) { return el.willValidate && el.type !== 'hidden' && el.type !== 'submit' && !el.closest('[aria-hidden="true"]'); }); }
  function again(e) { if (tried && e.target.form === form && e.target.willValidate) check(e.target); }
  form.addEventListener('input', again); form.addEventListener('change', again);

  /* 3. The hold. */
  var mode = 'call';
  form.addEventListener('click', function (e) { var b = e.target.closest('button[name="mode"]'); if (b) mode = b.value; });

  function say(cls, t) { status.className = 'enq-status' + (cls ? ' ' + cls : ''); status.textContent = t; }

  function show(h) {
    /* The confirmation, an instrument: what was held, what happens next, the reference. */
    var dep = byId(h.departure_id) || {};
    text('heldRef', h.ref); text('heldRef2', h.ref);
    text('heldTrip', h.trip_title || dep.title || ''); text('heldWhen', h.when || dep.when || '');
    text('heldPay', h.payment || ''); text('heldEmail', h.email || '');
    var next = d.getElementById('heldNext'), row = d.getElementById('heldRow');
    next.innerHTML = ''; row.innerHTML = '';
    var steps = [];
    steps.push('A confirmation email is on its way to ' + (h.email || 'your address') + ' with this reference, the dates and the terms in one line.');
    if (h.mode === 'call') steps.push('Book the call below. The place stays held under your reference until we have spoken.');
    else if (h.status === 'paid') steps.push('Stripe sends the card receipt to the same address.');
    else steps.push('Once the payment clears, this page and the email say so.');
    steps.push('Two days after the confirmation, the welcome kit: the packing list, visa and insurance, and how the days run.');
    for (var i = 0; i < steps.length; i++) { var li = d.createElement('li'); li.textContent = steps[i]; next.appendChild(li); }
    function btn(href, label, solid) { var a = d.createElement('a'); a.href = href; a.target = '_blank'; a.rel = 'noopener'; a.className = solid ? 'btn-solid' : 'listen-btn'; var s = d.createElement('span'); s.textContent = label; a.appendChild(s); row.appendChild(a); }
    if (h.mode === 'call') btn(CALENDAR, 'Book the call', true);
    btn(WHATSAPP, 'WhatsApp', false);
    form.hidden = true; held.hidden = false; held.focus();
  }

  /* Back from Stripe, or a reload: ?ref=PA-2026-XXXX shows the hold. */
  var ref = q.get('ref');
  if (ref && /^PA-\d{4}-[A-Z0-9]{4}$/.test(ref)) {
    if (!ENDPOINT) { say('', 'Your reference is ' + ref + '. The confirmation email has the rest.'); }
    else {
      fetch(ENDPOINT + '/status?ref=' + encodeURIComponent(ref), { headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (h) { if (h && h.ok) show(h); else say('bad', 'We could not find that reference. Email ' + EMAIL + ' and quote ' + ref + '.'); })
        .catch(function () { say('bad', 'We could not reach the relay. Your reference is ' + ref + '; the confirmation email has the rest.'); });
    }
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    tried = true;
    var first = null;
    fields().forEach(function (el) { if (!check(el) && !first) first = el; });
    if (first) {
      first.focus({ preventScroll: true });
      first.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      return;
    }
    if (!ENDPOINT) {
      say('bad', 'The booking relay is not connected yet. Book the call and we will hold the place by hand: ');
      var a = d.createElement('a'); a.href = CALENDAR; a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'book a free 30-minute call'; a.style.color = 'inherit';
      status.appendChild(a); status.appendChild(d.createTextNode(', or email ' + EMAIL + '.'));
      return;
    }
    var btns = form.querySelectorAll('button[name="mode"]');
    for (var i = 0; i < btns.length; i++) btns[i].disabled = true;
    say('', mode === 'deposit' ? 'Holding the place and opening the card payment.' : 'Holding the place.');
    var fd = new FormData(form); fd.set('mode', mode);
    fetch(ENDPOINT + '/hold', { method: 'POST', body: fd, headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (res) {
        if (!res || !res.ok) throw { said: res && res.error };
        if (res.checkout_url) { location.href = res.checkout_url; return; }
        say('', ''); show(res);
      })
      .catch(function (err) {
        for (var i = 0; i < btns.length; i++) btns[i].disabled = false;
        readout();
        say('bad', (err && err.said) || 'That did not go through. Please try again, or email ' + EMAIL + '.');
      });
  });
})();
</script>"""


def build():
    t = open(SRC, encoding="utf-8").read()
    n0 = len(t)

    # the shell: everything before <main> and everything from </main> on
    head, rest = t.split('<main id="v4-main">', 1)
    _, tail = rest.split("</main>", 1)

    # the page's own identity, in place of the enquiry page's
    head = re.sub(r"<title>.*?</script>", HEAD_META, head, count=1, flags=re.S)
    # the enquiry page's own scripts and styles are not this page's
    head = re.sub(r"<!--v4u-css-->.*?<!--/v4u-css-->", "", head, count=1, flags=re.S)
    head = re.sub(r"<!--v4u-holding-->.*?<!--/v4u-holding-->", "", head, count=1, flags=re.S)
    # the enquiry page's field styles stay (they are this page's fields too); its hero and layout go
    head = re.sub(r"\.enq-hero\{.*?\n\.enq-aside a\{color:var\(--orange\);\}\n", "", head, count=1, flags=re.S)
    head = head.replace("</head>", "<style>" + CSS + "</style>\n</head>", 1)
    head = head.replace('<body class="enq" data-v2="pg">', '<body class="enq bk" data-v2="pg">', 1)
    head = head.replace('<a href="enquire.html" class="nav-cta" data-hover><span>Enquire Now</span></a>',
                        '<a href="book.html" class="nav-cta" data-hover><span>Hold a Place</span></a>', 1)

    # the foot: the footer and the shared scripts, none of the enquiry form's own
    tail = re.sub(r'<script>\n/\* A link from a trip arrives.*?</script>\n', "", tail, count=1, flags=re.S)
    tail = re.sub(r'<script>\n/\* Send the enquiry\..*?</script>\n', "", tail, count=1, flags=re.S)
    tail = re.sub(r"<!--v4u-hold-->.*?<!--/v4u-hold-->\n", "", tail, count=1, flags=re.S)
    tail = re.sub(r"<!--v4u-form-js-->.*?<!--/v4u-form-js-->", "", tail, count=1, flags=re.S)

    script = SCRIPT % {
        "endpoint": json.dumps(ENDPOINT), "calendar": json.dumps(CALENDAR), "whatsapp": json.dumps(WHATSAPP),
        "email": json.dumps(EMAIL), "deps": json.dumps(DEPS, ensure_ascii=False), "notes": json.dumps(DUE_NOTE, ensure_ascii=False),
    }
    tail = tail.replace("</body>", script + "\n</body>", 1)

    page = head + '<main id="v4-main">\n' + body() + "\n</main>" + tail
    assert "\u2014" not in page, "an em-dash crept in"
    for must in ("nav-menu", "footer-content", "bkForm", "bkHeld", "noindex"):
        assert must in page, must
    open(OUT, "w", encoding="utf-8").write(page)
    print("wrote", os.path.relpath(OUT, ROOT), n0, "->", len(page), "bytes")


if __name__ == "__main__":
    build()
