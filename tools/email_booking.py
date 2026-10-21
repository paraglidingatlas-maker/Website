"""The booking confirmation email, one per trip, in the site's own look.

Writes docs/emails/booking-confirmation-<trip>.html with live image URLs
(https://paraglidingatlas.com/...). With --preview DIR it also writes a copy
whose image paths are relative, next to the images, for a local render.

Merge tags (MailerLite): {$name} {$reference} {$trip} {$departure}
{$deposit_status} {$balance_due} {$preferences} {$unsubscribe}.
Facts and captions come from the trip pages (prototypes/v4/destinations) and
tools/data; nothing here is new copy about the places."""
import os, sys, shutil, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "https://paraglidingatlas.com/"

BG = "#141519"; CARD = "#202127"; LINE = "#2f3038"; ORANGE = "#ff7517"
INK = "#f6f4f4"; MUTED = "#a9a9ad"; DIM = "#7c7d84"
SANS = "'DM Sans',Helvetica,Arial,sans-serif"
DISP = "Poppins,Helvetica,Arial,sans-serif"
MONO = "'DM Mono',Menlo,Consolas,'Courier New',monospace"

TRIPS = {
    "india": {
        "place": "Bir Billing, Himachal Pradesh",
        "hero": "assets/destinations/india/hero/back-ranges.jpg",
        "hero_alt": "The snow ridges of the Dhauladhar back ranges from above",
        "map": "assets/email/india-map.jpg",
        "map_alt": "The Dhauladhar front with Billing launch, Bir landing, Palampur and Dharamshala marked",
        "profile": "assets/email/india-profile.png",
        "profile_alt": "The ground from the Bir landing field 26 km north, with the landing at 1,400 m and the launch at 2,400 m marked",
        # the three readouts, each a fact the India page states
        "readouts": [("Launch", "2,400 m"), ("Landing", "1,400 m"), ("Cloudbase", "over 3,000 m")],
        "photos": [
            ("assets/destinations/india/gallery/over-the-peaks.jpg", "A single wing high above a snow-streaked peak"),
            ("assets/destinations/india/gallery/monastery.jpg", "A Tibetan monastery with prayer flags against a blue sky"),
            ("assets/destinations/india/gallery/last-light.jpg", "The Bir landing field under big cumulus, snow peaks behind, one wing coming in"),
        ],
        "page": "destinations/india.html",
        "kit": "the packing list, the visa and insurance you need, and how the days run",
    },
    "kenya": {
        "place": "Kerio Valley and the Rift, Kenya",
        "hero": "assets/destinations/kenya/hero/kerio-valley.jpg",
        "hero_alt": "Paragliding at Kerio Valley, Kenya",
        "map": None, "profile": None, "readouts": [],
        "photos": [
            ("assets/destinations/kenya/gallery/chyulu-hills.jpg", "Paragliding at Chyulu Hills, Kenya"),
            ("assets/destinations/kenya/gallery/longonot.jpg", "Paragliding at Mount Longonot Crater, Kenya"),
            ("assets/destinations/kenya/gallery/equator.jpg", "The Equator"),
        ],
        "page": "destinations/kenya.html",
        "kit": "the packing list, the visa and insurance you need, and how the days run",
    },
}

CALL = "https://calendar.app.google/HaJMYuiomt5Db9eh8"
WA = "https://wa.me/4796757456"


def kicker(text, color=MUTED):
    return ('<div style="font-family:%s;font-size:11px;letter-spacing:3px;text-transform:uppercase;'
            'color:%s;">%s</div>' % (MONO, color, text))


def build(trip, base):
    t = TRIPS[trip]
    U = lambda p: base + p
    pre = "Reference {$reference}. {$trip}, {$departure}. Keep this email: it is your booking."

    # ---------- hero with the headline on the photograph (VML for Outlook) ----------
    hero = '''
<tr><td style="padding:0 0 0;">
<!--[if gte mso 9]>
<v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:420px;">
<v:fill type="frame" src="%(hero)s" color="#141519" />
<v:textbox inset="0,0,0,0"><![endif]-->
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" background="%(hero)s" style="background:#141519 url('%(hero)s') center center / cover no-repeat;border-radius:18px;">
<tr><td style="height:420px;vertical-align:bottom;padding:0;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0">
  <tr><td style="padding:28px 32px 0;vertical-align:top;">
    <span style="display:inline-block;background:rgba(20,21,25,.62);border-radius:999px;padding:8px 14px;font-family:%(mono)s;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:%(ink)s;">%(place)s</span>
  </td></tr>
  <tr><td style="height:230px;font-size:0;line-height:0;">&nbsp;</td></tr>
  <tr><td style="padding:0 32px 30px;background:linear-gradient(to bottom, rgba(20,21,25,0) 0%%, rgba(20,21,25,.82) 55%%, rgba(20,21,25,.92) 100%%);border-radius:0 0 18px 18px;">
    <div style="font-family:%(mono)s;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:%(orange)s;padding:40px 0 10px;">Booking confirmation</div>
    <div style="font-family:%(disp)s;font-weight:800;font-size:44px;line-height:1.02;letter-spacing:-1px;color:%(ink)s;">Your place<br>is held.</div>
  </td></tr>
  </table>
</td></tr>
</table>
<!--[if gte mso 9]></v:textbox></v:rect><![endif]-->
</td></tr>''' % dict(hero=U(t["hero"]), mono=MONO, disp=DISP, ink=INK, orange=ORANGE,
                   place=html.escape(t["place"]))

    # ---------- the boarding card ----------
    cell = lambda label, value, mono=True, pad="18px 0 16px", border="border-top:1px solid %s;" % LINE: (
        '<td width="50%%" style="padding:%s;%svertical-align:top;">'
        '<div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:8px;">%s</div>'
        '<div style="font-family:%s;font-size:%s;line-height:1.45;color:%s;">%s</div></td>'
        % (pad, border, MONO, DIM, label, MONO if mono else SANS, "15px" if mono else "15px", INK, value))
    card = '''
<tr><td style="padding:16px 0 0;">
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%(card)s;border-radius:18px;">
<tr>
  <td class="stack0" style="padding:30px 32px 26px;vertical-align:top;">
    <div style="font-family:%(mono)s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%(dim)s;padding-bottom:10px;">Pilot</div>
    <div style="font-family:%(disp)s;font-weight:600;font-size:22px;line-height:1.2;color:%(ink)s;">{$name}</div>
    <div style="font-family:%(mono)s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%(dim)s;padding:26px 0 8px;">Reference</div>
    <div class="ref" style="font-family:%(mono)s;font-size:30px;line-height:1.1;letter-spacing:2px;color:%(orange)s;">{$reference}</div>
  </td>
  <td width="190" style="padding:30px 28px 26px 26px;border-left:1px dashed %(line)s;vertical-align:top;">
    <div style="font-family:%(mono)s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%(dim)s;padding-bottom:10px;">Departure</div>
    <div style="font-family:%(mono)s;font-size:17px;line-height:1.4;color:%(ink)s;">{$departure}</div>
    <div style="font-family:%(mono)s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%(dim)s;padding:26px 0 8px;">Trip</div>
    <div style="font-family:%(sans)s;font-size:15px;line-height:1.4;color:%(ink)s;">{$trip}</div>
  </td>
</tr>
<tr><td colspan="2" style="padding:0 32px;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="border-top:1px dashed %(line)s;"><tr><td style="font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table>
</td></tr>
<tr><td colspan="2" style="padding:6px 32px 30px;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0">
  <tr>%(pay)s%(bal)s</tr>
  </table>
  <div style="font-family:%(sans)s;font-size:13px;line-height:1.6;color:%(muted)s;padding-top:6px;">If you paid by card, this is your receipt from me and Stripe sends its own card receipt to this address too. If you held the place by booking a call, nothing has been charged.</div>
</td></tr>
</table>
</td></tr>''' % dict(card=CARD, mono=MONO, disp=DISP, sans=SANS, ink=INK, dim=DIM, orange=ORANGE, line=LINE, muted=MUTED,
                   pay=cell("Payment", "{$deposit_status}", mono=False, border=""),
                   bal=cell("Balance", "{$balance_due}", mono=False, border=""))

    # ---------- the ground: map plate, readouts, profile ----------
    ground = ""
    if t["map"]:
        reads = "".join(
            '<td width="33%%" style="padding:18px 0 0;vertical-align:top;">'
            '<div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:6px;">%s</div>'
            '<div class="read" style="font-family:%s;font-size:20px;line-height:1.2;color:%s;">%s</div></td>' % (MONO, DIM, k, MONO, INK, v)
            for k, v in t["readouts"])
        ground = '''
<tr><td style="padding:44px 0 0;">
  %(k)s
  <div style="font-family:%(disp)s;font-weight:600;font-size:26px;line-height:1.2;letter-spacing:-0.3px;color:%(ink)s;padding:10px 0 18px;">Where you will fly</div>
  <img src="%(map)s" alt="%(map_alt)s" width="600" style="width:100%%;max-width:600px;height:auto;display:block;border:0;border-radius:18px;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>%(reads)s</tr></table>
  <img src="%(prof)s" alt="%(prof_alt)s" width="600" style="width:100%%;max-width:600px;height:auto;display:block;border:0;border-radius:14px;margin-top:22px;">
</td></tr>''' % dict(k=kicker("The ground"), disp=DISP, ink=INK, map=U(t["map"]), map_alt=html.escape(t["map_alt"]),
                     reads=reads, prof=U(t["profile"]), prof_alt=html.escape(t["profile_alt"]))

    # ---------- the note ----------
    note = '''
<tr><td style="padding:44px 0 0;">
  %(k)s
  <p style="margin:14px 0 0;font-family:%(disp)s;font-weight:600;font-size:22px;line-height:1.45;letter-spacing:-0.2px;color:%(ink)s;">Thank you, {$name}. Your place is held under the reference above. Keep it: it is the one number that ties everything about this booking together.</p>
  <p style="margin:16px 0 0;font-family:%(sans)s;font-size:16px;line-height:1.7;color:%(muted)s;">Check the spelling of your name against your passport and tell me straight away if anything here is wrong. Quoting the reference in any message means I know exactly who and which departure you mean without asking.</p>
  <div style="font-family:%(disp)s;font-weight:600;font-size:15px;color:%(ink)s;padding-top:18px;">Aninder</div>
</td></tr>''' % dict(k=kicker("From the cockpit", ORANGE), disp=DISP, sans=SANS, ink=INK, muted=MUTED)

    # ---------- next, as a rail ----------
    steps = [
        ('If you held the place by booking a call rather than paying, book it now: <a href="%s" style="color:%s;text-decoration:none;border-bottom:1px solid %s;">a free 30-minute call</a>, nothing to prepare. The place stays held under your reference until we have spoken.' % (CALL, INK, ORANGE)),
        ('In two days you get the welcome kit: %s.' % t["kit"]),
        ('Before the trip, every pilot completes the <a href="%sparticipant-agreement.html" style="color:%s;text-decoration:none;border-bottom:1px solid %s;">participant agreement</a>: licence, experience, equipment, insurance and health. It is published in full, so read it now rather than on the day.' % (LIVE, INK, ORANGE)),
        ('Sort your insurance early: travel and accident cover valid for paragliding at the altitudes flown, including search and rescue by helicopter, mountain rescue, medical treatment and repatriation. Standard travel insurance often excludes it, so check the policy wording.'),
    ]
    rail = ""
    for i, s in enumerate(steps, 1):
        last = i == len(steps)
        rail += ('<tr><td width="56" style="vertical-align:top;padding:0;">'
                 '<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="font-family:%s;font-size:13px;color:%s;padding:2px 0 0;">0%d</td></tr>'
                 '<tr><td style="padding:10px 0 0 7px;"><div style="width:1px;height:%s;background:%s;font-size:0;line-height:0;">&nbsp;</div></td></tr></table></td>'
                 '<td style="vertical-align:top;padding:0 0 %s;font-family:%s;font-size:15px;line-height:1.65;color:%s;">%s</td></tr>'
                 % (MONO, ORANGE, i, "0" if last else "100%", LINE, "0" if last else "26px", SANS, INK, s))
    nxt = '''
<tr><td style="padding:44px 0 0;">
  %(k)s
  <div style="font-family:%(disp)s;font-weight:600;font-size:26px;line-height:1.2;letter-spacing:-0.3px;color:%(ink)s;padding:10px 0 22px;">What happens next</div>
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%(rail)s</table>
</td></tr>
<tr><td style="padding:34px 0 0;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>
    <td style="padding:0 8px 0 0;"><a href="%(call)s" style="display:block;text-align:center;background:%(orange)s;color:#141519;font-family:%(disp)s;font-weight:700;font-size:14px;letter-spacing:0.3px;padding:17px 10px;border-radius:999px;text-decoration:none;">Book the free 30-minute call</a></td>
    <td style="padding:0 0 0 8px;"><a href="%(wa)s" style="display:block;text-align:center;border:1px solid %(line2)s;color:%(ink)s;font-family:%(disp)s;font-weight:600;font-size:14px;letter-spacing:0.3px;padding:16px 10px;border-radius:999px;text-decoration:none;">Message me on WhatsApp</a></td>
  </tr></table>
</td></tr>''' % dict(k=kicker("Next"), disp=DISP, ink=INK, rail=rail, call=CALL, wa=WA, orange=ORANGE, line2="#45464e")

    # ---------- three photographs, none repeated ----------
    cells = "".join(
        '<td width="33%%" class="ph" style="padding:%s;vertical-align:top;">'
        '<img src="%s" alt="%s" width="186" class="phimg" style="width:100%%;max-width:186px;height:auto;display:block;border:0;border-radius:12px;">'
        '<div style="font-family:%s;font-size:11px;line-height:1.5;color:%s;padding-top:10px;">%s</div></td>'
        % ("0 8px 0 0" if i == 0 else ("0 0 0 8px" if i == 2 else "0 4px"), U(f), html.escape(a), MONO, MUTED, html.escape(a))
        for i, (f, a) in enumerate(t["photos"]))
    photos = '''
<tr><td style="padding:44px 0 0;">
  %(k)s
  <div style="font-family:%(disp)s;font-weight:600;font-size:26px;line-height:1.2;letter-spacing:-0.3px;color:%(ink)s;padding:10px 0 18px;">What you are coming for</div>
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>%(cells)s</tr></table>
  <div style="font-family:%(sans)s;font-size:14px;line-height:1.6;color:%(muted)s;padding-top:18px;">The whole trip, day by day, is on <a href="%(page)s" style="color:%(ink)s;text-decoration:none;border-bottom:1px solid %(orange)s;">your trip page</a>.</div>
</td></tr>''' % dict(k=kicker("The place"), disp=DISP, sans=SANS, ink=INK, muted=MUTED, cells=cells, page=LIVE + t["page"], orange=ORANGE)

    terms = '''
<tr><td style="padding:44px 0 0;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="border-top:1px solid %(line)s;"><tr><td style="padding:22px 0 0;">
  %(k)s
  <p style="margin:10px 0 0;font-family:%(sans)s;font-size:13px;line-height:1.7;color:%(muted)s;">The full balance is due 120 days before departure, your deposit is not refunded, and if you cancel a termination fee applies, worked out the way the Package Travel Act requires, which on a trip like this is usually most of the price. That is why I ask you to hold trip cancellation insurance. The full terms are at <a href="%(live)sterms.html" style="color:%(ink)s;text-decoration:none;border-bottom:1px solid %(orange)s;">paraglidingatlas.com/terms.html</a>.</p>
  </td></tr></table>
</td></tr>''' % dict(line=LINE, k=kicker("The terms, in one line"), sans=SANS, muted=MUTED, live=LIVE, ink=INK, orange=ORANGE)

    footer = '''
<tr><td style="padding:40px 0 36px;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0" class="foot"><tr>
    <td style="vertical-align:top;"><img src="%(logo)s" alt="Paragliding Atlas" width="120" style="width:120px;height:auto;display:block;border:0;"></td>
    <td align="right" style="vertical-align:top;font-family:%(mono)s;font-size:11px;letter-spacing:1px;line-height:2;">
      <a href="https://www.instagram.com/anindersingh13" style="color:%(muted)s;text-decoration:none;">Instagram</a>&nbsp;&nbsp;&nbsp;
      <a href="https://www.youtube.com/@ParaglidingAtlas" style="color:%(muted)s;text-decoration:none;">YouTube</a>&nbsp;&nbsp;&nbsp;
      <a href="https://www.patreon.com/cw/ParaglidingAtlas" style="color:%(muted)s;text-decoration:none;">Patreon</a>&nbsp;&nbsp;&nbsp;
      <a href="%(live)s" style="color:%(muted)s;text-decoration:none;">Website</a>
    </td>
  </tr></table>
  <div style="font-family:%(sans)s;font-size:11px;line-height:1.8;color:%(dim)s;padding-top:22px;">Aninder Singh, Paragliding Atlas, Olav Troviks Vei M 46, 0864 Oslo, Norway. Organisasjonsnummer 937116934. <a href="mailto:aninder@paraglidingatlas.com" style="color:%(dim)s;">aninder@paraglidingatlas.com</a><br>This email is about your booking. You can update your <a href="{$preferences}" style="color:%(muted)s;">preferences</a> or <a href="{$unsubscribe}" style="color:%(muted)s;">unsubscribe</a> from everything else.</div>
</td></tr>''' % dict(logo=U("assets/logo/atlas-logo-white.png"), mono=MONO, sans=SANS, muted=MUTED, dim=DIM, live=LIVE)

    doc = '''<!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="supported-color-schemes" content="dark">
<meta name="x-apple-disable-message-reformatting">
<title>Your place is held: {$reference}</title>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
<!-- Paragliding Atlas, booking confirmation (%(trip)s). Generated by tools/email_booking.py. -->
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<style>
:root{color-scheme:dark;supported-color-schemes:dark}
body{margin:0;padding:0;background:%(bg)s;-webkit-text-size-adjust:100%%}
table{border-collapse:collapse}
img{-ms-interpolation-mode:bicubic}
a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important}
@media (hover:hover){a.btn:hover{opacity:.9}}
@media only screen and (max-width:620px){
  .wrap{width:100%%!important}
  .pad{padding-left:16px!important;padding-right:16px!important}
  .h1{font-size:36px!important}
  .stack{display:block!important;width:100%%!important;box-sizing:border-box!important;border-left:0!important;border-top:1px dashed %(line)s!important;padding-left:32px!important}
  .btns td{display:block!important;width:100%%!important;padding:0 0 10px!important}
  .stack0{display:block!important;width:100%%!important;box-sizing:border-box!important;padding-bottom:22px!important}
  .ref{font-size:24px!important;letter-spacing:1px!important}
  .read{font-size:16px!important}
  .ph{display:block!important;width:100%%!important;box-sizing:border-box!important;padding:0 0 18px!important}
  .phimg{max-width:100%%!important}
  .foot td{display:block!important;width:100%%!important;text-align:left!important;padding-top:14px!important}
}
</style>
</head>
<body style="margin:0;padding:0;background:%(bg)s;">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:%(bg)s;">%(pre)s&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%(bg)s;">
<tr><td align="center" class="pad" style="padding:0 20px;">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0"><tr><td><![endif]-->
<table role="presentation" width="600" class="wrap" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;color:%(ink)s;">
<tr><td style="padding:26px 0 18px;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>
    <td style="vertical-align:middle;"><img src="%(logo)s" alt="Paragliding Atlas" width="150" style="width:150px;height:auto;display:block;border:0;"></td>
    <td align="right" style="vertical-align:middle;font-family:%(mono)s;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:%(dim)s;">Ref {$reference}</td>
  </tr></table>
</td></tr>
%(hero)s
%(card)s
%(ground)s
%(note)s
%(nxt)s
%(photos)s
%(terms)s
%(footer)s
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr>
</table>
</body>
</html>
''' % dict(trip=trip, bg=BG, ink=INK, line=LINE, pre=pre, logo=U("assets/logo/atlas-logo-white.png"), mono=MONO, dim=DIM,
           hero=hero, card=card, ground=ground, note=note, nxt=nxt, photos=photos, terms=terms, footer=footer)
    # responsive hooks
    doc = doc.replace('<td width="190" style="padding:30px 28px 26px 26px;border-left', '<td width="190" class="stack" style="padding:30px 28px 26px 26px;border-left')
    doc = doc.replace('font-size:44px;line-height:1.02;letter-spacing:-1px;color:%s;">Your place' % INK, 'font-size:44px;line-height:1.02;letter-spacing:-1px;color:%s;" class="h1">Your place' % INK)
    doc = doc.replace('<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>\n    <td style="padding:0 8px 0 0;"><a', '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="btns"><tr>\n    <td style="padding:0 8px 0 0;"><a')
    return doc


def main():
    out = os.path.join(ROOT, "docs", "emails")
    os.makedirs(out, exist_ok=True)
    preview = None
    if "--preview" in sys.argv:
        preview = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(preview, exist_ok=True)
    for trip in TRIPS:
        doc = build(trip, LIVE)
        assert "—" not in doc
        p = os.path.join(out, "booking-confirmation-%s.html" % trip)
        open(p, "w").write(doc)
        print("wrote", p, len(doc) // 1024, "KB")
        if preview:
            pd = build(trip, "")
            open(os.path.join(preview, "booking-confirmation-%s.html" % trip), "w").write(pd)
            t = TRIPS[trip]
            for f in [t["hero"], t["map"], t["profile"], "assets/logo/atlas-logo-white.png"] + [x[0] for x in t["photos"]]:
                if not f: continue
                d = os.path.join(preview, os.path.dirname(f)); os.makedirs(d, exist_ok=True)
                shutil.copy(os.path.join(ROOT, f), os.path.join(preview, f))


if __name__ == "__main__":
    main()
