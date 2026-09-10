#!/usr/bin/env python3
"""Build the three policy pages: terms, privacy, cookies.

Kept as a generator rather than three hand written files so the nav, footer and
head block cannot drift apart between them. Edit the BODIES below and re-run:

    python3 generate_policies.py

Sources, so nobody has to guess later:
  - Privacy and Cookie text: the user's own drafts in the Drive Policies folder,
    CORRECTED against what the site actually loads. The drafts described Klarna,
    GoDaddy, Cookiebot, Google Analytics 4 and Leaflet. None of those are on the
    site. Publishing them unchanged would have described cookies that are never
    set, which is a false statement to users and to a regulator.
  - Terms: there was no terms document at all, only an empty Google Doc. The
    structure follows the Trek Travel waiver in the same folder, but the legal
    mechanism is deliberately NOT the same. See the note in the terms body.
"""
import datetime
import os
import re

UPDATED = "11 September 2026"
BASE = "https://paraglidingatlas-maker.github.io/Website/"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Paragliding Atlas</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}assets/images/hero.jpg">
<meta property="og:url" content="{base}{slug}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{title}","url":"{base}{slug}","description":"{desc}","isPartOf":{{"@type":"WebSite","name":"Paragliding Atlas","url":"{base}"}}}}
</script>
<link rel="icon" type="image/png" href="assets/logo/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="policies.css">
</head>
<body>

<div class="page-wrap">

<nav>
  <span class="nav-corner-l"></span>
  <span class="nav-corner-r"></span>
  <span class="nav-coords">59.9139&deg;N &middot; 10.7522&deg;E</span>
  <a href="index.html" class="wordmark"><img src="assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img"></a>
  <div class="nav-links">
    <a href="about.html">About Us</a>
    <span class="nav-sep">|</span>
    <a href="knowledge-base.html">Knowledge Base</a>
    <span class="nav-sep">|</span>
    <a href="podcast.html">Podcast</a>
    <span class="nav-sep">|</span>
    <a href="sitemap.html">Sitemap</a>
  </div>
  <a href="enquire.html" class="nav-cta" data-hover><span>Enquire Now</span></a>
</nav>
<div class="nav-chevron"></div>

<header class="pol-hero">
  <span class="kicker">{kicker}</span>
  <h1>{title}</h1>
  <p class="pol-meta">Last updated {updated} &middot; Paragliding Atlas, Oslo, Norway</p>
</header>

<div class="pol-wrap">
  <nav class="pol-toc" aria-label="On this page">
    <h2>On this page</h2>
{toc}  </nav>
  <div class="pol-body">
{body}  </div>
</div>

</div><!-- /.page-wrap -->

<footer>
  <div class="footer-content">
  <div class="footer-top">
    <div class="footer-col">
      <span class="wordmark"><img src="assets/logo/atlas-logo-white.png" alt="Paragliding Atlas" class="logo-img"></span>
      <p>Organisasjonsnummer: 937116934<br>Olav Troviks Vei M 46<br>Oslo, Norway</p>
    </div>
    <div class="footer-col">
      <h4>Enquiries</h4>
      <a href="#">General</a>
      <a href="index.html#destinations">Trips</a>
      <a href="#">FAQs</a>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <a href="library.html">All Episodes</a>
      <a href="index.html#destinations">Kenya Tour</a>
      <a href="#">Contact Us</a>
    </div>
    <div class="footer-col">
      <h4>Links</h4>
      <a href="knowledge-base.html">Knowledge Base</a>
      <a href="#">Passion</a>
      <a href="#">Mission Statement</a>
    </div>
  </div>
  <div class="footer-bottom">
    <a href="terms.html">Terms &amp; Conditions</a>
    <a href="privacy-policy.html">Privacy Policy</a>
    <a href="cookie-policy.html">Cookie Policy</a>
    <span>Paragliding Atlas 2026</span>
  </div>
  </div>
  <div class="footer-graphic">
    <img src="assets/footer/mountains.png" alt="Paragliding Atlas &mdash; Touch the Sky with Glory">
  </div>
</footer>

<script src="script.js"></script>
</body>
</html>
"""

TERMS = """
<h2 id="who">1. Who we are</h2>
<p>Paragliding Atlas is a paragliding travel and media company registered in Norway. Organisasjonsnummer 937116934, Olav Troviks Vei M 46, Oslo, Norway. In these terms "we", "us" and "our" mean Paragliding Atlas, and "you" means the person making a booking and every participant named on it.</p>
<p>These terms apply to guided paragliding trips we organise. They do not restrict any right you have under Norwegian or EU consumer law that cannot be restricted by agreement.</p>

<h2 id="package">2. Package travel rights</h2>
<p>If your booking combines two or more travel services, for example flights and accommodation, or accommodation and guided flying that forms a significant part of the trip, it is likely to be a <strong>package</strong> under Directive (EU) 2015/2302 and the Norwegian Package Travel Act.</p>
<p>Where the trip is a package, you have the full set of rights that legislation gives you. Those include the right to receive all essential information before you book, the right to transfer your booking to another person, the right to cancel without a fee if the price rises by more than eight per cent, the right to cancel without a fee in the event of unavoidable and extraordinary circumstances at the destination, and protection of your payments if we become insolvent. We will give you the standard information form for package travel before you book, and it forms part of your contract.</p>

<h2 id="booking">3. Booking and payment</h2>
<p>A booking is made when we confirm your place in writing and you have paid the deposit. That confirmation, together with these terms and the trip description on this site, forms the contract between us.</p>
<p>Unless your trip page or confirmation says otherwise:</p>
<ul>
  <li>A deposit of <strong>25 per cent</strong> of the trip price secures your place.</li>
  <li>The <strong>balance is due 60 days</strong> before departure.</li>
  <li>Bookings made inside 60 days of departure are payable in full at the time of booking.</li>
</ul>
<p>If the balance is not received by the due date we may treat the booking as cancelled by you, and the cancellation charges in section 5 apply.</p>
<p>Please check your confirmation carefully as soon as you receive it and tell us straight away if anything is wrong, particularly the spelling of names, which must match your passport.</p>

<h2 id="price">4. What the price includes</h2>
<p>What is included and excluded is listed on the trip page and repeated in your booking confirmation. Unless we state otherwise, the price does not include international flights, visas, travel and rescue insurance, personal flying equipment, or anything of a personal nature.</p>
<p>We may increase the price after booking only for the reasons the Package Travel Act allows, such as changes to fuel costs, taxes or exchange rates, and never in the twenty days before departure. If an increase exceeds eight per cent of the trip price you may accept it, accept a substitute trip if we offer one, or cancel and receive a full refund. If the same costs fall, you are entitled to a corresponding reduction.</p>

<h2 id="cancel-you">5. If you change or cancel</h2>
<p>Tell us in writing as soon as you know. Cancellation charges apply from the date we receive your notice. They exist because we commit to guides, accommodation, permits and transport well in advance and cannot recover those costs late in the day.</p>
<div class="pol-tablewrap">
<table>
<tr><th>Notice we receive before departure</th><th>Charge</th></tr>
<tr><td>More than 90 days</td><td>Deposit only</td></tr>
<tr><td>60 to 89 days</td><td>50 per cent of the trip price</td></tr>
<tr><td>30 to 59 days</td><td>75 per cent of the trip price</td></tr>
<tr><td>Fewer than 30 days, or no show</td><td>100 per cent of the trip price</td></tr>
</table>
</div>
<p>If we are able to resell your place we will refund what we recover, less an administration fee. This is why we ask you to hold cancellation insurance: a policy that covers you for illness, injury or a change in circumstances will normally meet these charges where we cannot.</p>
<p>You may transfer your booking to another person who meets the pilot requirements in section 7, provided you tell us with reasonable notice and pay any costs the transfer causes.</p>
<div class="pol-note">
<p><strong>There is no fourteen day cooling off period.</strong> Under Article 16(l) of the Consumer Rights Directive, the right of withdrawal that normally applies to distance contracts does not apply to leisure services provided on a specific date. This is normal for guided trips and it is why insurance matters.</p>
</div>

<h2 id="cancel-us">6. If we change or cancel</h2>
<p>Flying trips depend on weather, airspace and ground conditions, and the daily plan will change to suit them. That is not a change to your contract, it is the trip working as intended. Where we have to make a significant change to a main feature of the trip before departure, we will tell you without delay and you may accept it, accept a substitute we offer, or cancel and receive a full refund.</p>
<p>We may cancel a trip if too few people book, provided we tell you within the periods the Package Travel Act sets, or if we are prevented by unavoidable and extraordinary circumstances. In either case you receive a full refund of everything you have paid us. We are not liable for costs you have incurred separately, such as flights booked independently, which is another reason to insure.</p>

<h2 id="risk">7. The nature of the activity, and what you take on</h2>
<div class="pol-note">
<p>Paragliding is an air sport with inherent risks that cannot be removed by good organisation, good equipment or good judgement. Those risks include serious injury and death.</p>
</div>
<p>By booking you confirm that you understand this and that you choose to take part anyway. Specifically, you acknowledge that:</p>
<ul>
  <li>Conditions in the mountains and at altitude change quickly and can exceed forecasts.</li>
  <li>Sites may be remote, and medical help, road access and mobile coverage may be hours away.</li>
  <li>Rescue may require a helicopter, may be delayed by weather or darkness, and can be expensive.</li>
  <li>You fly as pilot in command. Every decision to launch, to continue and to land is yours, and no guide, briefing or forecast transfers that decision to us.</li>
  <li>Other pilots, both in our group and outside it, may make mistakes that affect you.</li>
</ul>
<p>You are responsible for holding a valid licence, for flying within the limits of your own experience and current fitness, for the airworthiness of your own equipment, and for complying with the air law of the country you are flying in.</p>
<p>Before departure we will ask you to complete our <a href="participant-agreement.html">Participant Agreement</a>, which records your licence, experience, insurance, emergency contact and any medical information relevant to flying. Participation is conditional on it.</p>
<p><strong>Minimum requirement.</strong> Unless the trip page states otherwise, you need an IPPI 2, APPI or equivalent national rating, and you must be able to launch yourself and land out on your own. Tell us honestly about your experience, recency and fitness when you book. We may refuse or end participation if we judge, at our sole discretion, that a participant is not safe to fly with the group, is unfit, or is affecting the safety or enjoyment of others. Where we do that for good reason, no refund is due.</p>

<h2 id="insurance">8. Insurance is mandatory</h2>
<p>You must hold travel and accident insurance that covers paragliding as an activity, at the altitudes flown on the trip, and that includes helicopter search and rescue, mountain rescue, medical treatment and repatriation. Cover that excludes air sports is not sufficient, and a policy that covers "adventure sports" generally often excludes paragliding, so read the wording.</p>
<p>We may ask for proof of cover before departure and may refuse participation without it. You remain responsible for rescue and medical costs your policy does not meet.</p>

<h2 id="liability">9. Our responsibility to you</h2>
<p>We are responsible for performing the travel services included in your booking with reasonable skill and care, and for putting things right where we do not.</p>
<div class="pol-note">
<p><strong>We do not ask you to sign away your right to claim for negligence, and we could not do so if we tried.</strong> Under Norwegian and EU law, a term that excludes or limits liability for death or personal injury caused by negligence is not binding. Any waiver you may have signed with an operator elsewhere that purports to do this has no effect here.</p>
</div>
<p>We are not responsible for a failure that is attributable to you, to a third party unconnected with the travel services and unforeseeable or unavoidable, or to unavoidable and extraordinary circumstances. Where our liability is capped by an international convention that applies to a service, that cap applies here too.</p>
<p>Nothing in these terms limits your rights under the Package Travel Act or other mandatory consumer law.</p>

<h2 id="conduct">10. Behaviour, equipment and other people</h2>
<p>You are responsible for your own equipment throughout the trip. Anything we lend you is to be returned in the condition it was given, fair wear and tear aside, and you are responsible for loss or damage beyond that.</p>
<p>Flying under the influence of alcohol or drugs is not permitted and will end your participation immediately, without refund. The same applies to behaviour that endangers or seriously disrupts other participants or local people.</p>

<h2 id="media">11. Photographs and film</h2>
<p>We often photograph and film our trips, and we may want to use those images in our own marketing, on this site, in the podcast, or on social media. If you would prefer not to appear, tell us at any point, before or after the trip, and we will not use images in which you are identifiable. You do not need to give a reason, and it will not affect your booking.</p>

<h2 id="complaints">12. If something goes wrong</h2>
<p>Tell your guide at the time, so we have the chance to fix it while you are still on the trip. If it cannot be resolved there, write to us at <a href="mailto:aninder@paraglidingatlas.com">aninder@paraglidingatlas.com</a> and we will reply within a reasonable time.</p>
<p>If we cannot settle it between us, you can bring the matter to the Norwegian Package Travel Complaints Board, Pakkereisenemnda. If you live elsewhere in the EEA you may also use the European Commission's online dispute resolution platform, and you keep the right to bring proceedings in the courts of the country where you live.</p>

<h2 id="data">13. Your personal data</h2>
<p>How we handle your data is set out in our <a href="privacy-policy.html">Privacy Policy</a>. In short, we collect what we need to run your booking and to keep you safe on the trip, including emergency contact and relevant medical information, and we do not sell it to anyone.</p>

<h2 id="law">14. Governing law</h2>
<p>These terms are governed by Norwegian law. If you are a consumer resident elsewhere in the EEA, this does not deprive you of the protection of the mandatory rules of the country where you live.</p>
<p>If any part of these terms is found to be unenforceable, the rest continues to apply.</p>

<h2 id="changes">15. Changes to these terms</h2>
<p>We may update these terms. The version that applies to your booking is the one published when you booked, and we will send it with your confirmation. The date at the top of this page shows when this version was published.</p>

<div class="pol-contact">
  <h3>Questions about these terms</h3>
  <p>Email <a href="mailto:aninder@paraglidingatlas.com">aninder@paraglidingatlas.com</a>, or write to Paragliding Atlas, Olav Troviks Vei M 46, Oslo, Norway.</p>
</div>
"""

PRIVACY = """
<h2 id="intro">1. Introduction</h2>
<p>Paragliding Atlas is committed to protecting your personal data and respecting your privacy. This policy explains what we collect when you visit this site or book a trip with us, why we collect it, and what you can do about it.</p>
<p>It follows the EU General Data Protection Regulation and applicable Norwegian law. Paragliding Atlas is the data controller, based in Oslo, Norway.</p>

<h2 id="collect">2. What we collect</h2>
<p><strong>Almost nothing, when you are only reading.</strong> This site has no analytics, no advertising tools and no tracking pixels. We do not build a profile of you, and we cannot tell who you are from a visit.</p>
<p>We collect personal data in three situations:</p>
<ul>
  <li><strong>When you contact us or enquire about a trip.</strong> Your name, email address, and whatever you choose to tell us about your flying experience and what you are looking for.</li>
  <li><strong>When you book a trip.</strong> The information needed to run the booking and keep you safe: contact details, passport name, licence and experience, emergency contact, insurance details, and any medical information you tell us is relevant to flying.</li>
  <li><strong>When you sign up for the newsletter.</strong> Your name and email address.</li>
</ul>
<p>Our hosting provider and the content networks listed below record technical information such as your IP address in their server logs, as every web server does. We do not have access to those logs as an identifiable record of you.</p>

<h2 id="why">3. Why we use it, and our legal basis</h2>
<div class="pol-tablewrap">
<table>
<tr><th>Purpose</th><th>Data</th><th>Legal basis</th></tr>
<tr><td>Replying to your enquiry</td><td>Contact details, what you told us</td><td>Steps taken at your request before a contract</td></tr>
<tr><td>Running your booking</td><td>Booking and travel data</td><td>Performance of a contract</td></tr>
<tr><td>Keeping you safe on the trip, including in an emergency</td><td>Emergency contact, insurance, relevant medical information</td><td>Your explicit consent, and protection of vital interests in an emergency</td></tr>
<tr><td>Meeting accounting and tax obligations</td><td>Transaction records</td><td>Legal obligation under Norwegian law</td></tr>
<tr><td>Sending the newsletter</td><td>Name, email</td><td>Consent, withdrawable at any time</td></tr>
</table>
</div>
<p>Health information is a special category of data under the GDPR. We ask for it only where it genuinely affects your safety in the air or a rescue, we keep it to the people who need it, and we delete it after the trip unless you ask us to keep it for a future booking.</p>

<h2 id="third">4. Who else is involved</h2>
<p>These are the third parties whose infrastructure this site actually uses. We have checked this list against the site's own code rather than assuming it.</p>
<div class="pol-tablewrap">
<table>
<tr><th>Service</th><th>What it does</th><th>What reaches them</th></tr>
<tr><td>GitHub Pages (Microsoft)</td><td>Hosts the site</td><td>IP address and request details, in server logs</td></tr>
<tr><td>Google Fonts</td><td>Serves the two typefaces the site uses</td><td>IP address, when a page loads</td></tr>
<tr><td>YouTube, in privacy enhanced mode</td><td>Episode video players</td><td>IP address for the thumbnail. Nothing further unless you press play</td></tr>
<tr><td>cdnjs and unpkg</td><td>Serve two animation and graphics libraries</td><td>IP address, when a page loads</td></tr>
<tr><td>Cloudflare Workers</td><td>Fetches the podcast feed so the episode library can show durations</td><td>IP address of the request</td></tr>
<tr><td>Google Calendar and WhatsApp</td><td>Only if you click "Book a Call" or the WhatsApp link</td><td>Whatever those services collect once you arrive there</td></tr>
</table>
</div>
<p>We do not use Google Analytics, an advertising network, a payment processor on this site, or a customer database that follows you around.</p>

<h2 id="retention">5. How long we keep it</h2>
<ul>
  <li><strong>Enquiries that do not become bookings:</strong> up to 24 months, then deleted.</li>
  <li><strong>Booking records:</strong> five years after the trip, because Norwegian accounting law requires it.</li>
  <li><strong>Medical and emergency contact information:</strong> deleted after the trip ends, unless you ask us to hold it for a future booking.</li>
  <li><strong>Newsletter:</strong> until you unsubscribe.</li>
</ul>

<h2 id="transfers">6. Transfers outside the EEA</h2>
<p>Some of the providers above are based in the United States. Where personal data is transferred outside the EEA, we rely on the European Commission's Standard Contractual Clauses and, where it applies, the EU-US Data Privacy Framework.</p>

<h2 id="rights">7. Your rights</h2>
<p>Under the GDPR you can ask us to give you a copy of your data, correct it, delete it, restrict how we use it, or send it to you in a portable format. You can object to processing based on legitimate interests, and you can withdraw consent at any time without affecting what we did before you withdrew it.</p>
<p>Email <a href="mailto:aninder@paraglidingatlas.com">aninder@paraglidingatlas.com</a> and we will respond within one month. If you are not satisfied, you can complain to the Norwegian Data Protection Authority, Datatilsynet, or to the supervisory authority in the EEA country where you live.</p>

<h2 id="security">8. Security</h2>
<p>The site is served over HTTPS. Booking correspondence is held in business email and cloud storage accounts protected by two factor authentication, and is shared only with the people running your trip.</p>

<h2 id="children">9. Children</h2>
<p>This site is not aimed at children, and we do not knowingly collect data from anyone under 16. Participants under 18 need the consent of a parent or guardian, who must also provide the emergency contact and medical information.</p>

<h2 id="changes">10. Changes</h2>
<p>If we change this policy we will publish the new version here and update the date at the top of the page.</p>

<div class="pol-contact">
  <h3>Contact for privacy matters</h3>
  <p>Paragliding Atlas, Olav Troviks Vei M 46, Oslo, Norway. Email <a href="mailto:aninder@paraglidingatlas.com">aninder@paraglidingatlas.com</a>.</p>
</div>
"""

COOKIES = """
<div class="pol-note">
<p><strong>This site does not set any cookies of its own, and there is no cookie banner because there is nothing to consent to on arrival.</strong></p>
<p>We checked the site's own code before writing this rather than describing a typical setup. There is no analytics, no advertising tag, no consent management platform, and no code anywhere on the site that writes a cookie or uses browser storage.</p>
</div>

<h2 id="what">1. What a cookie is</h2>
<p>A cookie is a small file a website asks your browser to store, so it can recognise the same browser later, either for the length of one visit, a session cookie, or across visits, a persistent cookie. They are ordinary and often useful. We simply do not need any.</p>

<h2 id="ours">2. Cookies we set</h2>
<p>None. You can confirm this yourself: open your browser's developer tools, look at the storage or application tab, and load any page on this site.</p>

<h2 id="third">3. Third party requests, and when a cookie could appear</h2>
<p>Although we set nothing, pages do load some things from other companies, and those requests reveal your IP address to them in the same way visiting their site would. One of them can set a cookie, but only if you choose to interact with it.</p>
<div class="pol-tablewrap">
<table>
<tr><th>Service</th><th>Why it is there</th><th>Does it set a cookie?</th></tr>
<tr><td>Google Fonts</td><td>The two typefaces the site is set in</td><td>No. Fonts are served without cookies</td></tr>
<tr><td>YouTube, privacy enhanced mode</td><td>The video player on episode pages</td><td>Not on page load. The players use youtube-nocookie.com, so YouTube stores nothing until you actually press play</td></tr>
<tr><td>cdnjs and unpkg</td><td>Two animation and graphics libraries</td><td>No</td></tr>
<tr><td>Cloudflare Workers</td><td>Fetches the podcast feed for episode durations</td><td>No</td></tr>
</table>
</div>
<p>If you press play on a video, YouTube may then store data on your device under its own terms. If you would rather it did not, do not press play, or watch the episode on YouTube directly where you can manage those settings in your Google account.</p>

<h2 id="control">4. Controlling cookies anyway</h2>
<p>Every browser lets you block or delete cookies in its settings, and the Help function in your browser will show you where. <a href="https://www.allaboutcookies.org/" target="_blank" rel="noopener">allaboutcookies.org</a> covers the major browsers in detail. Blocking cookies will not break anything on this site, because we do not rely on them.</p>

<h2 id="future">5. If this changes</h2>
<p>If we ever add analytics or anything else that sets a non-essential cookie, we will add a proper consent banner that blocks it until you agree, and we will update this page before doing so. We will not quietly start tracking and update the small print afterwards.</p>

<div class="pol-contact">
  <h3>Questions</h3>
  <p>Email <a href="mailto:aninder@paraglidingatlas.com">aninder@paraglidingatlas.com</a>. See also our <a href="privacy-policy.html">Privacy Policy</a>.</p>
</div>
"""

AGREEMENT = """
<div class="pol-note">
<p>This is the form every participant completes before a trip. It is published here so you can read it in full before you book, rather than meeting it for the first time a week before departure.</p>
<p><strong>It is not a waiver of our responsibility to you.</strong> Norwegian and EU law does not allow an operator to contract out of liability for death or personal injury caused by its own negligence, and we do not ask you to try. What this document does is record what you understand, what you are qualified to do, and how we reach someone if things go wrong.</p>
</div>

<h2 id="risk">1. What I am acknowledging</h2>
<p>I understand that paragliding is an air sport with risks that cannot be designed out, and that those risks include serious injury and death. I have read the trip page and section 7 of the <a href="terms.html">booking terms</a>, and I am choosing to take part with that understanding.</p>
<p>I understand specifically that:</p>
<ul>
  <li>Mountain and altitude conditions change faster than forecasts, and a day that begins calm may not stay that way.</li>
  <li>Sites may be remote. Road access, mobile coverage and medical help may be hours away.</li>
  <li>Rescue may need a helicopter, may be delayed by weather or darkness, and is expensive.</li>
  <li>Other pilots, in the group and outside it, can make mistakes that affect me.</li>
</ul>

<h2 id="command">2. I fly as pilot in command</h2>
<p>I understand that every decision to launch, to continue, to push on or to land is mine. Guides brief, advise, and set the plan for the day, and I am expected to listen to them. But a briefing is not an instruction to fly, and a forecast is not a guarantee. If I am not happy with a launch, the conditions, or my own state on the day, I will not fly, and nobody on this trip will think less of me for it.</p>

<h2 id="qualified">3. My licence and experience</h2>
<p>I confirm that I hold a current IPPI 2, APPI or equivalent national rating, or the rating stated on the trip page, and that I can launch myself and land out unassisted.</p>
<p>I confirm that what I have told Paragliding Atlas about my hours, recency, wing class and recent flying is accurate. I understand that overstating my experience puts the whole group at risk, and that participation may be refused or ended if what I described does not match what I can do.</p>
<p><em>To complete: licence type and number, issuing body, total airtime, hours in the last 12 months, wing make, model and EN class, year of manufacture, date of last inspection.</em></p>

<h2 id="equipment">4. My equipment</h2>
<p>I confirm that my wing, harness and reserve are airworthy, within their service life, and inspected and repacked in line with the manufacturer's guidance. I understand that my equipment is my responsibility throughout the trip, and that I am responsible for anything Paragliding Atlas lends me beyond fair wear and tear.</p>
<p>I will carry a 2m radio on the frequencies the trip uses, and I understand that a radio is for coordination and not a substitute for my own judgement.</p>

<h2 id="insurance">5. My insurance</h2>
<p>I confirm that I hold travel and accident insurance valid for paragliding, at the altitudes flown on this trip, covering search and rescue including helicopter, mountain rescue, medical treatment and repatriation.</p>
<p>I understand that a policy covering "adventure sports" often excludes air sports, that I have checked the wording rather than assumed, and that I remain responsible for any rescue or medical cost my policy does not meet.</p>
<p><em>To complete: insurer, policy number, 24 hour emergency number, confirmation that paragliding is covered.</em></p>

<h2 id="health">6. Health and emergency contact</h2>
<p>I have told Paragliding Atlas about any medical condition, medication, allergy or injury that could affect me in the air, at altitude, or in a rescue. I understand this information is held only for the duration of the trip, shared only with the people running it, and deleted afterwards unless I ask otherwise, as set out in the <a href="privacy-policy.html">Privacy Policy</a>.</p>
<p>I consent to Paragliding Atlas arranging emergency medical treatment or evacuation on my behalf if I am unable to consent at the time, and I understand I am responsible for the cost.</p>
<p><em>To complete: emergency contact name, relationship, phone number reachable during the trip, and any relevant medical information.</em></p>

<h2 id="conduct">7. Conduct</h2>
<p>I will not fly under the influence of alcohol or drugs, and I understand this ends my participation immediately and without refund. I will respect local rules, landowners, airspace and other site users, and I understand that behaviour endangering or seriously disrupting others has the same consequence.</p>

<h2 id="images">8. Photographs and film</h2>
<p>Paragliding Atlas often films and photographs its trips and may use those images in marketing, on the website, in the podcast or on social media.</p>
<p><em>Tick one: I agree to images of me being used / I would prefer images in which I am identifiable not to be used.</em></p>
<p>Either choice is fine, no reason is needed, and it can be changed at any time before or after the trip by emailing us.</p>

<h2 id="sign">9. Signature</h2>
<p>I confirm that I have read this agreement and the booking terms, that I have had the chance to ask questions, and that everything I have stated is true.</p>
<p><em>Name, date, signature. For a participant under 18, a parent or guardian signs, gives the emergency contact and medical information, and consents to emergency treatment.</em></p>

<div class="pol-contact">
  <h3>Before you sign</h3>
  <p>If anything here is unclear, or if you are unsure whether your experience or insurance is sufficient, email <a href="mailto:aninder@paraglidingatlas.com">aninder@paraglidingatlas.com</a> and ask. It is a much better conversation to have now than on a launch.</p>
</div>
"""

PAGES = [
    ("terms.html", "Terms &amp; Conditions", "Booking Terms",
     "Booking terms for Paragliding Atlas guided trips, including package travel rights, cancellation, insurance requirements and the risks of the activity.", TERMS),
    ("privacy-policy.html", "Privacy Policy", "Your Data",
     "What Paragliding Atlas collects, why, how long we keep it, and your rights under the GDPR. This site has no analytics and no tracking.", PRIVACY),
    ("participant-agreement.html", "Participant Agreement", "Before You Fly",
     "The form every participant completes before a Paragliding Atlas trip: risk acknowledgement, licence and experience, equipment, insurance, health and emergency contact.", AGREEMENT),
    ("cookie-policy.html", "Cookie Policy", "Cookies",
     "This site sets no cookies of its own and shows no cookie banner. What that means, and what the few third party requests do.", COOKIES),
]


def toc_from(body):
    out = []
    for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S):
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        text = re.sub(r"^\d+\.\s*", "", text)
        out.append('    <a href="#%s">%s</a>\n' % (m.group(1), text))
    return "".join(out)


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    for slug, title, kicker, desc, body in PAGES:
        plain = title.replace("&amp;", "and")
        html = HEAD.format(title=plain, desc=desc, base=BASE, slug=slug,
                           kicker=kicker, updated=UPDATED,
                           toc=toc_from(body), body=body)
        with open(os.path.join(root, slug), "w", encoding="utf-8") as f:
            f.write(html)
        print("built %-20s %2d sections, %5d words"
              % (slug, len(re.findall(r'<h2 id=', body)),
                 len(re.sub(r"<[^>]+>", " ", body).split())))


if __name__ == "__main__":
    main()
