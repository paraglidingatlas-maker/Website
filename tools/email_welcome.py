"""The India welcome kit email, in the same system as the booking confirmation
(tools/email_booking.py). Writes docs/emails/welcome-kit-india.html with live
image URLs; --preview DIR writes a relative-path copy next to the images.
Every fact is the India trip page's or the packing checklist PDF's; the text is
the 21 Oct kit, re-set. Merge tags: {$name} {$reference} {$departure}."""
import os, sys, shutil, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from email_booking import (ROOT, LIVE, BG, CARD, LINE, ORANGE, INK, MUTED, DIM, SANS, DISP, MONO, kicker, WA)

HERO = "assets/destinations/india/hero/snowline.jpg"
HERO_ALT = "A red wing along the snowline of the Dhauladhar"
PHOTOS = [
    ("assets/destinations/india/gallery/meadows.jpg", "A meadow of white flowers below the snow-covered Dhauladhar"),
    ("assets/destinations/india/hero/bir-landing.jpg", "Bir's landing field among terraced fields, seen from the air"),
    ("assets/destinations/india/gallery/kangra-valley.jpg", "The Kangra valley from the air, villages and fields below the hills"),
]
OPEN_PHOTO = ("assets/destinations/india/hero/dhauladhar.jpg", "The Dhauladhar range under building cumulus, above the Kangra valley")
CLOSE_PHOTO = ("assets/destinations/india/gallery/last-light-pair.jpg", "Two paragliders silhouetted against the sunset")

# The nine rules on the India page, from two episodes of the show. Paraphrased there, paraphrased here.
RULES = [
    ("The wing you bring", "Fly something you can relax on", "Bir is not the place to find out what your new high end wing does in the afternoon. The flying is long rather than difficult, and the pilots who enjoy it are the ones not busy managing their glider: a wing calm enough that you would happily take a photo while flying it.", "Eddie Colfox", "India episode, 14:29"),
    ("Before you launch", "Tell someone your plan", "Say where you are going and who you are going with, every day, before you take off. Then close the loop in the evening. Most of what goes wrong here is survivable; being missing for six hours before anyone notices is what turns it into a rescue.", "Eddie Colfox", "India episode, 13:39"),
    ("The traffic", "Expect company, and a lot of it", "The thermals that make Bir easy are the same thermals everyone else is in, and autumn is when everyone comes. When he first came for an autumn season, about 200 pilots from around the world were flying there. In autumn 2023 it was about 800.", "Jigish Gohil", "Bir episode, 09:11"),
    ("In the thermal", "Turn the way everyone else is turning", "Join on the outside, take the established direction, and leave room. The mid-airs he describes came from pilots turning the wrong way, bunching up, or not watching where they were going. If the circle gets too tight for your comfort, leave for the next ridge. There is a thermal on every knob along the front range.", "Jigish Gohil", "Bir episode, 24:39"),
    ("Following", "Do not just follow the wing in front", "There are exceptional pilots at Bir, and some of them are doing things you should not copy. A line that works for a local on a two liner is not automatically a line for you. Some of the pilots in the air at Bir are superb, and some simply do not know better.", "Eddie Colfox", "India episode, 14:29"),
    ("The cloud", "Watch the sky, not just the climb", "Autumn at Bir can overdevelop. On 17 October 2024 a visiting pilot near the end of a long flight was swept from 3,000 m to above 7,000 m inside a storm cloud in about ten minutes, and survived; nine incidents were reported in the area that day. Watch how fast the clouds are building, stay out from under the big ones, and land early rather than late.", "Eddie Colfox", "India episode, 24:44"),
    ("The landing field", "Fly the approach, every time", "The Bir landing is big, grassy and busy, which is exactly why people get hurt on it. However big the field, pilots misjudge the last leg, arrive long, then stall the wing in from three or four metres up and break something. Anywhere else, the hazards are terraces and power lines, which show up late.", "Jigish Gohil", "Bir episode, 30:42"),
    ("Over the back", "Going deep is a commitment", "Behind the front range the ground gets big and the options get thin. Altitude, thermal strength, roughness and cold all step up at once, and help can take until the next day. His test for going over: a couple of hundred hours, an SIV course, gear to sleep out, and the fitness to walk for eight or nine hours.", "Jigish Gohil", "Bir episode, 27:35"),
    ("The tracker question", "Check what is legal before you pack", "Some satellite communicators are not technically legal in India, and the advice online has not all caught up. Ask me before you buy or pack one. Do not find this out at customs.", "Eddie Colfox", "India episode, 36:49"),
]
OPENING = [
    "It is your first morning at Bir. The valley is already warm. Four of you share a taxi up the hill, about 45 minutes of hairpins, and step out on the meadow at Billing at 2,400 m with the Dhauladhar standing over you and a queue of wings laid out along the grass. There is no wind to speak of. There almost never is. You lay out to the side, wait for your gap, and go.",
    "By early afternoon you are at cloudbase, over 3,000 m, where it is freezing, looking down a front range that works for tens of kilometres in either direction and up at the snow of the back ranges. By the end of the day you are picking a field at the edge of town with the light going and the whole valley turning gold.",
    "That is the trip. What follows is everything between now and that morning: the paperwork that cannot be done on the day, the nine things pilots who have flown here for decades want you to know, what to pack, and what Bir is when you are not in the air. Read it once now. Keep it for the week before you leave.",
]
BIR = [
    ("Tibet in the foothills", "Bir is a Tibetan settlement as much as a flying town. The monasteries, the prayer flags on the ridges and the momos in the cafes are not decoration; they are the place. Walk the colony on a rest day and let it be slow."),
    ("Dharamshala, under your flight", "The run west along the front ends above Dharamshala, home of the Dalai Lama in exile. You will fly over it; take a day to go there on the ground too."),
    ("The valley", "Palampur, on the map under the route, is Kangra tea country, and the landing field sits among terraces that have been farmed for generations. The ride back from a landing out goes through all of it, and it is part of the trip."),
    ("Last light", "Most days end at the Bir landing with the sun going down behind the ridge. Land early enough to watch it."),
]

PDF = LIVE + "assets/destinations/india/india-packing-checklist.pdf"

PAPER = [
    ("Visa", "Most nationalities can use the e-visa, applied for at least 4 days before you arrive. It suits most nationalities, but not all, so check yours early."),
    ("e-Arrival Card", "Everyone files a free online e-Arrival Card in the 72 hours before flying in."),
    ("Passport", "Valid for 6 months, with two blank pages."),
    ("Licence", "Your IPPI 2 card or national licence. This is a tour for autonomous pilots."),
    ("Insurance, essential", "Travel and accident insurance valid for paragliding at the altitudes flown on this trip, covering search and rescue including helicopter, mountain rescue, medical treatment and repatriation. Standard travel insurance often excludes adventure sports, so read the policy wording. Save the policy number and the rescue hotline offline: you will want them when you are down the back with no signal."),
]
LIKE = [
    "Bir has a reputation as the easy Himalaya, and in the air it mostly earns it. What catches pilots out is everything around the flying: a nil-wind launch with a queue behind you, a house thermal full of wings, and a long approach into a busy landing field. Autumn at Bir now draws hundreds of visiting pilots, so you will share the sky to get it.",
    "It is built for autonomous pilots who want the Himalaya at its most approachable. You can launch cleanly in nil wind, without help from the breeze; you are comfortable thermalling in company and keep looking around while you climb; and you can choose a landing early and fly a full approach at the end of a long flight.",
    "Flying deep into the back ranges on a first visit takes a couple of hundred hours, an SIV course and kit for a night out, so that is not this trip. It is warm in the valley and freezing at cloudbase, on the same day. And the plan follows the conditions, not the other way round: there is no fixed timetable.",
]
DAY = [
    ("Briefing", "The forecast, the plan and the traffic: where the climbs are likely to be, which way to head, and what to do if the day shuts down early."),
    ("Up the hill", "Shared taxis up to Billing, about 45 minutes from Bir, the way everyone does it, usually four pilots to a car."),
    ("Launch", "Almost always nil-wind, and there will be a queue. Lay out to the side, and once your wing is up, go."),
    ("Fly", "Leave the house thermal as soon as you have the height for the next knob. The front range works for tens of kilometres either way, so there is no need to stay in the crowd."),
    ("Land", "Most days end back in Bir. Pick your field early, fly a full approach, and anywhere else, watch for terraces and power lines."),
]
DAY_NOTE = "Billing launches at about 2,400 m and cloudbase in season is over 3,000 m, where it is freezing. The front range is forgiving; the traffic is not. Land out over the back and help can take until the next day, so carry what you need for a night out. Guiding is 1 guide to 3 pilots."
READOUTS = [("Launch", "2,400 m"), ("Cloudbase", "over 3,000 m"), ("Guiding", "1 to 3")]
PACK = [
    ("Documents and money", ["Passport, valid 6 months, with two blank pages", "Indian visa, applied for before you travel", "e-Arrival Card, filed online", "IPPI 2 card or national licence", "Insurance covering paragliding (medical treatment, repatriation and search and rescue)", "Policy number and rescue hotline, saved offline", "Rupees in small notes, for taxis, chai and the ride back from a landing out"]),
    ("Clothing", ["Down jacket for flying, the one people underestimate", "Thermal layers", "Winter flying gloves, tested in easy air before the day you need them", "Hiking shoes, already broken in", "Sunscreen and sunglasses, the valley is warm and bright at midday", "Buff", "Warm layers for the evening, it cools off fast after landing"]),
    ("Flying gear", ["Wing you know well, EN or LTF certified: Bir rewards a wing you can relax on, not the hottest one you own", "Harness with back or airbag protection", "Reserve, repacked and in date", "Helmet", "Vario or GPS, with the airspace and waypoints loaded before you travel", "Radio, the group frequency is briefed on arrival", "Tracker, once you have checked it is legal: some satellite communicators are not technically legal in India, so ask me before you buy or pack one", "Spare lines", "Ripstop tape"]),
    ("On you", ["Offline maps of the front range", "Unlocked phone, so you can run a local SIM", "Powerbank and cables", "Headlamp", "Pocket knife"]),
    ("Health and stomach", ["Routine vaccinations up to date, checked with a travel clinic well before you go", "Rehydration salts", "Probiotic", "DEET repellent", "Basic first aid and any personal medication"]),
]
GROUND = [
    ("Getting there", "From New Delhi, Bir is an overnight bus ride north, or a short flight to Dharamshala and about two hours by road."),
    ("Money", "Indian rupees. Bir has only one or two ATMs, and they can run dry at weekends, so arrive with cash in small notes."),
    ("Language", "Hindi and English. English is widely spoken around Bir, which has welcomed visiting pilots for decades."),
    ("Power", "230 volts, 50 hertz, plug types C, D and M. Bring an adapter."),
]
READ = [
    ("The trip", "Bir Billing cross country routes, the FAQ and the full packing list", [("The India page", LIVE + "destinations/india.html")]),
    ("Knowledge base", "Meteorology, weather patterns, flight mechanics, risk versus reward, and your equipment: what the show's guests have taught me, written up", [("Meteorology", LIVE + "knowledge-base/meteorology.html"), ("Weather patterns", LIVE + "knowledge-base/weather-patterns.html"), ("Flight mechanics", LIVE + "knowledge-base/flight-mechanics.html"), ("Risk vs reward", LIVE + "knowledge-base/risk-vs-reward.html"), ("Know your equipment", LIVE + "knowledge-base/know-your-equipment.html")]),
    ("The paperwork", "The participant agreement every pilot completes, and the booking terms", [("Participant agreement", LIVE + "participant-agreement.html"), ("Booking terms", LIVE + "terms.html")]),
]

H2 = '<div style="font-family:%s;font-weight:600;font-size:26px;line-height:1.2;letter-spacing:-0.3px;color:%s;padding:10px 0 %s;">%s</div>'
LINK = '<a href="%s" style="color:%s;text-decoration:none;border-bottom:1px solid %s;">%s</a>'
BOX = ('<td width="22" style="vertical-align:top;padding:3px 12px 0 0;"><div style="width:14px;height:14px;border:1.5px solid %s;border-radius:4px;font-size:0;line-height:0;">&nbsp;</div></td>' % ORANGE)


def section(k, h2, body, pad="44px 0 0"):
    return '<tr><td style="padding:%s;">%s%s%s</td></tr>' % (pad, kicker(k), (H2 % (DISP, INK, "18px", h2)) if h2 else "", body)


def build(base):
    U = lambda p: base + p
    pre = "Your first morning at Bir, the nine rules, the paperwork and the packing list. Reference {$reference}."
    head = '''
<tr><td style="padding:26px 0 18px;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>
    <td style="vertical-align:middle;"><img src="%(logo)s" alt="Paragliding Atlas" width="150" style="width:150px;height:auto;display:block;border:0;"></td>
    <td align="right" style="vertical-align:middle;font-family:%(mono)s;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:%(dim)s;">Ref {$reference}</td>
  </tr></table>
</td></tr>
<tr><td style="padding:0;">
<!--[if gte mso 9]>
<v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:460px;">
<v:fill type="frame" src="%(hero)s" color="#141519" />
<v:textbox inset="0,0,0,0"><![endif]-->
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" background="%(hero)s" style="background:#141519 url('%(hero)s') center center / cover no-repeat;border-radius:18px;">
<tr><td style="height:460px;vertical-align:bottom;padding:0;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0">
  <tr><td style="padding:28px 32px 0;vertical-align:top;">
    <span style="display:inline-block;background:rgba(20,21,25,.62);border-radius:999px;padding:8px 14px;font-family:%(mono)s;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:%(ink)s;">Bir Billing, Himachal Pradesh</span>
  </td></tr>
  <tr><td style="height:250px;font-size:0;line-height:0;">&nbsp;</td></tr>
  <tr><td style="padding:0 32px 30px;background:linear-gradient(to bottom, rgba(20,21,25,0) 0%%, rgba(20,21,25,.82) 55%%, rgba(20,21,25,.92) 100%%);border-radius:0 0 18px 18px;">
    <div style="font-family:%(mono)s;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:%(orange)s;padding:40px 0 10px;">Welcome kit</div>
    <div class="h1" style="font-family:%(disp)s;font-weight:800;font-size:44px;line-height:1.02;letter-spacing:-1px;color:%(ink)s;">Before<br>you fly.</div>
    <div style="font-family:%(mono)s;font-size:13px;line-height:1.5;color:%(ink)s;padding-top:14px;">{$departure} &middot; a ten minute read, then keep it</div>
  </td></tr>
  </table>
</td></tr>
</table>
<!--[if gte mso 9]></v:textbox></v:rect><![endif]-->
</td></tr>''' % dict(logo=U("assets/logo/atlas-logo-white.png"), mono=MONO, dim=DIM, hero=U(HERO), ink=INK, orange=ORANGE, disp=DISP)

    note = '''
<tr><td style="padding:36px 0 0;">
  %s
  <p style="margin:14px 0 0;font-family:%s;font-weight:600;font-size:22px;line-height:1.45;letter-spacing:-0.2px;color:%s;">{$name}, this is everything I would want in your hands before you fly to India. Your place is held under {$reference}.</p>
  <p style="margin:16px 0 0;font-family:%s;font-size:16px;line-height:1.7;color:%s;">It is paperwork before it is flying, and none of it can be sorted out on the morning you need it. So start with the morning itself.</p>
  <div style="font-family:%s;font-weight:600;font-size:15px;color:%s;padding-top:18px;">Aninder</div>
</td></tr>''' % (kicker("From the cockpit", ORANGE), DISP, INK, SANS, MUTED, DISP, INK)

    rows = "".join('<tr>%s<td style="vertical-align:top;padding:0 0 %s;"><div style="font-family:%s;font-weight:600;font-size:16px;line-height:1.3;color:%s;">%s</div><div style="font-family:%s;font-size:14px;line-height:1.65;color:%s;padding-top:4px;">%s</div></td></tr>'
                   % (BOX, "0" if i == len(PAPER) - 1 else "18px", DISP, INK, t, SANS, MUTED, b) for i, (t, b) in enumerate(PAPER))
    paper = '''<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%s;border-radius:18px;"><tr><td style="padding:28px 32px;"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table></td></tr></table>''' % (CARD, rows)

    like = "".join('<p style="margin:%s;font-family:%s;font-size:16px;line-height:1.7;color:%s;">%s</p>' % ("0" if i == 0 else "14px 0 0", SANS, INK if i == 0 else MUTED, t) for i, t in enumerate(LIKE))

    rail = ""
    for i, (t, b) in enumerate(DAY, 1):
        last = i == len(DAY)
        rail += ('<tr><td width="56" style="vertical-align:top;padding:0;"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="font-family:%s;font-size:13px;color:%s;padding:4px 0 0;">0%d</td></tr><tr><td style="padding:10px 0 0 7px;"><div style="width:1px;height:%s;background:%s;font-size:0;line-height:0;">&nbsp;</div></td></tr></table></td>'
                 '<td style="vertical-align:top;padding:0 0 %s;"><div style="font-family:%s;font-weight:600;font-size:17px;line-height:1.3;color:%s;">%s</div><div style="font-family:%s;font-size:15px;line-height:1.65;color:%s;padding-top:4px;">%s</div></td></tr>'
                 % (MONO, ORANGE, i, "0" if last else "100%", LINE, "0" if last else "22px", DISP, INK, t, SANS, MUTED, b))
    reads = "".join('<td width="33%%" style="padding:22px 0 0;vertical-align:top;"><div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:6px;">%s</div><div class="read" style="font-family:%s;font-size:20px;line-height:1.2;color:%s;">%s</div></td>' % (MONO, DIM, k, MONO, INK, v) for k, v in READOUTS)
    day = ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table>'
           '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>%s</tr></table>'
           '<p style="margin:18px 0 0;font-family:%s;font-size:14px;line-height:1.65;color:%s;">%s</p>' % (rail, reads, SANS, MUTED, DAY_NOTE))

    total = sum(len(v) for _, v in PACK)
    groups = ""
    for g, items in PACK:
        li = "".join('<tr>%s<td style="vertical-align:top;padding:0 0 10px;font-family:%s;font-size:14px;line-height:1.55;color:%s;">%s</td></tr>' % (BOX, SANS, INK, html.escape(x)) for x in items)
        groups += ('<tr><td style="padding:0 0 12px;"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%s;border-radius:16px;"><tr><td style="padding:22px 28px 14px;">'
                   '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr><td style="font-family:%s;font-weight:600;font-size:17px;color:%s;padding-bottom:14px;">%s</td><td align="right" style="font-family:%s;font-size:12px;letter-spacing:2px;color:%s;padding-bottom:14px;">%02d</td></tr></table>'
                   '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table></td></tr></table></td></tr>' % (CARD, DISP, INK, g, MONO, ORANGE, len(items), li))
    pack = ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table>'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" class="btns"><tr>'
            '<td style="padding:10px 8px 0 0;"><a href="%s" style="display:block;text-align:center;background:%s;color:#141519;font-family:%s;font-weight:700;font-size:14px;letter-spacing:0.3px;padding:17px 10px;border-radius:999px;text-decoration:none;">The checklist as a PDF</a></td>'
            '<td style="padding:10px 0 0 8px;"><a href="%sdestinations/india.html#packing" style="display:block;text-align:center;border:1px solid #45464e;color:%s;font-family:%s;font-weight:600;font-size:14px;letter-spacing:0.3px;padding:16px 10px;border-radius:999px;text-decoration:none;">The same list, tickable online</a></td></tr></table>'
            '<p style="margin:14px 0 0;font-family:%s;font-size:13px;line-height:1.6;color:%s;">Tick the boxes in any PDF reader and save, or print it and use a pen.</p>'
            % (groups, PDF, ORANGE, DISP, LIVE, INK, DISP, SANS, MUTED))

    gcells = "".join('<td width="50%%" style="padding:0 0 22px;vertical-align:top;"><div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:6px;">%s</div><div style="font-family:%s;font-size:14px;line-height:1.6;color:%s;padding-right:18px;">%s</div></td>' % (MONO, DIM, t, SANS, INK, b) for t, b in GROUND)
    ground = '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>%s</tr><tr>%s</tr></table>' % (gcells[:gcells.index('<td width="50%"', 10) if False else len(gcells)], "")
    # two rows of two
    cells = ['<td width="50%%" class="stack0" style="padding:0 0 22px;vertical-align:top;"><div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:6px;">%s</div><div style="font-family:%s;font-size:14px;line-height:1.6;color:%s;padding-right:18px;">%s</div></td>' % (MONO, DIM, t, SANS, INK, b) for t, b in GROUND]
    ground = '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>%s%s</tr><tr>%s%s</tr></table>' % tuple(cells)

    rcards = ""
    for t, b, links in READ:
        ls = " &nbsp;&nbsp; ".join(LINK % (u, INK, ORANGE, n) for n, u in links)
        rcards += '<tr><td style="padding:0 0 12px;"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="border:1px solid %s;border-radius:16px;"><tr><td style="padding:20px 24px;"><div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:8px;">%s</div><div style="font-family:%s;font-size:15px;line-height:1.6;color:%s;padding-bottom:12px;">%s</div><div style="font-family:%s;font-size:13px;line-height:2;color:%s;">%s</div></td></tr></table></td></tr>' % (LINE, MONO, ORANGE, t, SANS, INK, b, SANS, INK, ls)
    read = '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table>' % rcards

    pcells = "".join('<td width="33%%" class="ph" style="padding:%s;vertical-align:top;"><img src="%s" alt="%s" width="186" class="phimg" style="width:100%%;max-width:186px;height:auto;display:block;border:0;border-radius:12px;"><div style="font-family:%s;font-size:11px;line-height:1.5;color:%s;padding-top:10px;">%s</div></td>' % ("0 8px 0 0" if i == 0 else ("0 0 0 8px" if i == 2 else "0 4px"), U(f), html.escape(a), MONO, MUTED, html.escape(a)) for i, (f, a) in enumerate(PHOTOS))
    photos = '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>%s</tr></table>' % pcells

    signoff = '''
<tr><td style="padding:44px 0 0;">
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="border-top:1px solid %(line)s;"><tr><td style="padding:26px 0 0;">
  <p style="margin:0;font-family:%(sans)s;font-size:16px;line-height:1.7;color:%(ink)s;">If anything here is unclear, or you are unsure whether your experience or insurance is enough, reply to this email or message me on %(wa)s and ask. It is a much better conversation to have now than on a launch. See you in Bir.</p>
  <div style="font-family:%(disp)s;font-weight:600;font-size:15px;color:%(ink)s;padding-top:18px;">Aninder Singh</div>
  <div style="font-family:%(sans)s;font-size:13px;color:%(muted)s;padding-top:2px;">Paragliding Atlas</div>
  </td></tr></table>
</td></tr>''' % dict(line=LINE, sans=SANS, ink=INK, wa=LINK % (WA, INK, ORANGE, "WhatsApp"), disp=DISP, muted=MUTED)

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

    opening = ('<img src="%s" alt="%s" width="600" style="width:100%%;max-width:600px;height:auto;display:block;border:0;border-radius:18px;margin-bottom:22px;">' % (U(OPEN_PHOTO[0]), html.escape(OPEN_PHOTO[1]))
               + "".join('<p style="margin:%s;font-family:%s;font-size:%s;line-height:%s;color:%s;">%s</p>' % ("0" if i == 0 else "16px 0 0", DISP if i == 0 else SANS, "20px" if i == 0 else "16px", "1.5" if i == 0 else "1.7", INK if i < 2 else MUTED, t) for i, t in enumerate(OPENING)))
    rcards = ""
    for i, (k, rule, body_, who, where) in enumerate(RULES, 1):
        rcards += ('<tr><td style="padding:0 0 12px;"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%s;border-radius:16px;"><tr>'
                   '<td width="64" style="padding:24px 0 24px 26px;vertical-align:top;font-family:%s;font-size:22px;color:%s;">%02d</td>'
                   '<td style="padding:24px 26px 24px 0;vertical-align:top;">'
                   '<div style="font-family:%s;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:%s;padding-bottom:6px;">%s</div>'
                   '<div style="font-family:%s;font-weight:600;font-size:19px;line-height:1.3;color:%s;">%s</div>'
                   '<div style="font-family:%s;font-size:14px;line-height:1.65;color:%s;padding-top:8px;">%s</div>'
                   '<div style="font-family:%s;font-size:11px;letter-spacing:1px;color:%s;padding-top:12px;">%s, paraphrased &middot; %s</div>'
                   '</td></tr></table></td></tr>' % (CARD, MONO, ORANGE, i, MONO, DIM, k, DISP, INK, rule, SANS, MUTED, body_, MONO, DIM, who, where))
    rules = ('<p style="margin:0 0 18px;font-family:%s;font-size:16px;line-height:1.7;color:%s;">The weather at Bir is the easy part. What the pilots who know it talk about is traffic, and the accidents they describe are traffic accidents. These nine come from two episodes of the show, with Eddie Colfox, who has run trips from Bir since 2007, and Jigish Gohil, who has lived there for about a decade. Their words are paraphrased, not quoted.</p>'
             '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table>' % (SANS, MUTED, rcards))
    bcells = "".join('<td width="50%%" class="stack0" style="padding:0 18px 22px 0;vertical-align:top;"><div style="font-family:%s;font-weight:600;font-size:17px;line-height:1.3;color:%s;padding-bottom:6px;">%s</div><div style="font-family:%s;font-size:14px;line-height:1.65;color:%s;">%s</div></td>' % (DISP, INK, t, SANS, MUTED, b) for t, b in BIR)
    bir = (photos + '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="margin-top:26px;"><tr>%s%s</tr><tr>%s%s</tr></table>' % tuple(
        '<td width="50%%" class="stack0" style="padding:0 18px 22px 0;vertical-align:top;"><div style="font-family:%s;font-weight:600;font-size:17px;line-height:1.3;color:%s;padding-bottom:6px;">%s</div><div style="font-family:%s;font-size:14px;line-height:1.65;color:%s;">%s</div></td>' % (DISP, INK, t, SANS, MUTED, b) for t, b in BIR))
    closing = ('<img src="%s" alt="%s" width="600" style="width:100%%;max-width:600px;height:auto;display:block;border:0;border-radius:18px;">' % (U(CLOSE_PHOTO[0]), html.escape(CLOSE_PHOTO[1])))
    body = (head + note
            + section("Your first morning", "", opening, pad="40px 0 0")
            + section("Paperwork first", "Nothing here can be done on the day", paper)
            + section("The flying", "What this trip is actually like", like)
            + section("A day at Bir", "How a day runs", day)
            + section("Nine rules", "From pilots who have flown here for decades", rules)
            + section("Bir on the ground", "The Himalaya you will not see from the air", bir)
            + section("Packing", "%d items, six essential. The one everyone underestimates is in the second card." % total, pack)
            + section("Practical", "Getting there and getting by", ground)
            + section("Read before you go", "", read, pad="44px 0 0")
            + section("Last light", "", closing, pad="44px 0 0")
            + signoff + footer)
    doc = '''<!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="supported-color-schemes" content="dark">
<meta name="x-apple-disable-message-reformatting">
<title>Your welcome kit for Bir Billing</title>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
<!-- Paragliding Atlas, the India welcome kit. Generated by tools/email_welcome.py. -->
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<style>
:root{color-scheme:dark;supported-color-schemes:dark}
body{margin:0;padding:0;background:%(bg)s;-webkit-text-size-adjust:100%%}
table{border-collapse:collapse}
img{-ms-interpolation-mode:bicubic}
a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important}
@media only screen and (max-width:620px){
  .wrap{width:100%%!important}
  .pad{padding-left:16px!important;padding-right:16px!important}
  .h1{font-size:36px!important}
  .btns td{display:block!important;width:100%%!important;padding:0 0 10px!important}
  .stack0{display:block!important;width:100%%!important;box-sizing:border-box!important}
  .read{font-size:16px!important}
  .ph{display:block!important;width:100%%!important;box-sizing:border-box!important;padding:0 0 18px!important}
  .phimg{max-width:100%%!important}
  .foot td{display:block!important;width:100%%!important;text-align:left!important;padding-top:14px!important}
}
</style>
</head>
<body style="margin:0;padding:0;background:%(bg)s;">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:%(bg)s;">%(pre)s&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%(bg)s;">
<tr><td align="center" class="pad" style="padding:0 20px;">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0"><tr><td><![endif]-->
<table role="presentation" width="600" class="wrap" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;color:%(ink)s;">
%(body)s
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr>
</table>
</body>
</html>
''' % dict(bg=BG, pre=pre, ink=INK, body=body)
    assert "—" not in doc
    return doc


def main():
    out = os.path.join(ROOT, "docs", "emails", "welcome-kit-india.html")
    open(out, "w").write(build(LIVE)); print("wrote", out)
    if "--preview" in sys.argv:
        pv = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(pv, exist_ok=True)
        open(os.path.join(pv, "welcome-kit-india.html"), "w").write(build(""))
        for f in [HERO, OPEN_PHOTO[0], CLOSE_PHOTO[0], "assets/logo/atlas-logo-white.png"] + [x[0] for x in PHOTOS]:
            d = os.path.join(pv, os.path.dirname(f)); os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(ROOT, f), os.path.join(pv, f))


if __name__ == "__main__":
    main()
