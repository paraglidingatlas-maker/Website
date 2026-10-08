"""Encyclopedia answer pages: one question per page.

WHY THIS EXISTS
The series pages answer the questions the guests raise. Nobody had answered the
questions people actually type: how does a paraglider fly, what is a glide ratio,
what does EN B mean. Those are the searches, and the questions people put to
ChatGPT and the rest. Each entry here becomes one page that answers one of them
in plain language, cites the open sources it was built from, and then adds what
no other site has: what the guests on the show said about it, linked to the
chapter where they said it.

RULES FOR WRITING ONE (docs/encyclopedia/README.md has the full process)
- The short answer comes first and stands on its own: 40 to 70 words, the
  answer itself, no preamble. It is the part answer engines lift.
- Every factual sentence carries a citation, written [n], where n is the
  position of the source in the entry's "sources" list. The build fails on a
  citation that points nowhere and on a source that is never cited.
- Rewrite, never copy. Only US government works (FAA, NASA, NOAA) are public
  domain; manuals, federations, magazines and Wikipedia are facts only.
- Arithmetic done here rather than quoted is called a worked example in the
  copy, so nobody mistakes it for a published figure.
- "show" items paraphrase a guest and point at the chapter: (who, episode slug,
  chapter id, card title, text). The build validates the chapter. Never quote
  the transcripts; they are automatic captions.
- Section headings are questions where they can be. They end in "?" and the
  schema injector turns them into FAQPage entries.
- {{slug|text}} links to another answer page; the build checks the slug.
- No em-dashes. British spelling. First person singular when the site speaks.
- status "draft" renders the page with noindex and keeps it out of the A to Z,
  the sitemap and llms.txt. Flip it to "published" and set "reviewed" once the
  page has been checked.
"""

# Episode slugs
LUC_M = "luc-armant-talks-about-the-moment-coefficient-enzo-3"
LUC_D = "luc-armant-talks-about-debunking-the-myths-and-upgrading"
TOM = "tom-lolies-explains-the-science-of-wing-design-and"
HELMUT = "helmut-schrempf-modernizing-siv-courses-how-this-new"
ALAIN = "alain-zoller-the-science-of-en-certifications-how-work"
BRETT = "how-to-thermal-like-a-pro-find-center-climb-paragliding"
BRYAN = "demystifying-the-science-behind-parakites-bryan-van-ostheim"
NESLER = "why-paraglidings-safety-future-looks-different-rast"
UPF = "new-technologies-5-frantisek-pavlousek"
SKYMATE = "understanding-skymate-paragliding-worlds-first-ai-driven"
ANTOINE = "sky-gods-flying-8000ers-antoine-girard"
BELC = "bill-belcourt-the-uncomfortable-truth-no-one-is-talking"
GIN = "legacy-and-lifetimes-of-gin-seok-song"

# Sources used on more than one page: (title, publisher, url, type)
FAA_GFH3 = ("Glider Flying Handbook (FAA-H-8083-13B), Chapter 3: Aerodynamics of Flight", "FAA",
            "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf",
            "Government handbook")
FAA_GFH5 = ("Glider Flying Handbook (FAA-H-8083-13B), Chapter 5: Glider Performance", "FAA",
            "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf",
            "Government handbook")
FAA_GFH10 = ("Glider Flying Handbook (FAA-H-8083-13B), Chapter 10: Soaring Techniques", "FAA",
             "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_10.pdf",
             "Government handbook")
FAA_PHAKG = ("Pilot's Handbook of Aeronautical Knowledge: Glossary", "FAA",
             "https://www.faa.gov/sites/faa.gov/files/21_phak_glossary.pdf", "Government handbook")
NASA_3F = ("Three Forces on a Glider", "NASA Glenn Research Center",
           "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/three-forces-on-a-glider", "Government")
NASA_LIFT = ("The Lift Equation", "NASA Glenn Research Center",
             "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-equation-2", "Government")
NASA_GLIDERS = ("Gliders", "NASA Glenn Research Center",
                "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/gliders/", "Government")
NASA_TN = ("A Theoretical Analysis of the Dynamic Lateral Stability and Control of a Parawing Vehicle (TN D-3461, 1966)",
           "NASA Langley Research Center",
           "https://ntrs.nasa.gov/api/citations/19660019921/downloads/19660019921.pdf", "Research")
AC006A = ("Aviation Weather (AC 00-6A), Chapter 16: Soaring Weather (historic circular)", "FAA",
          "https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC%2000-6A%20Chap%2016-Index.pdf",
          "Government")
WIKI_PG = ("Paragliding", "Wikipedia", "https://en.wikipedia.org/wiki/Paragliding", "Encyclopedia")
OZ_RUSH6 = ("Rush 6 pilot's manual (EN B)", "Ozone",
            "https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf", "Manufacturer")
OZ_SWIFT = ("SwiftMax pilot's manual", "Ozone",
            "https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/06/SwiftMax_manual_EN_v1.1.pdf", "Manufacturer")
OZ_DELTA4 = ("Delta 4 pilot's manual (EN C)", "Ozone",
             "https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/07/Delta-4-manual-EN-v1.0.pdf", "Manufacturer")
OZ_LM7 = ("LM7 pilot's manual (EN D)", "Ozone",
          "https://cdn1.flyozone.com/wp-content/uploads/sites/1/2019/12/LM7-manual-EN-v1.0.pdf", "Manufacturer")
GIN_B8 = ("Bolero 8 user manual (EN A)", "Gin Gliders",
          "https://static.gingliders.com/paragliders/bolero-8/documents/bolero-8-user-manual-en.pdf", "Manufacturer")
NIV_H6 = ("Hook 6 user manual (EN B)", "Niviuk",
          "https://niviuk.com/biblioteca/items/449_A/user_manual_hook_6_glider_niviuk_paragliders.pdf", "Manufacturer")
NIV_H6T = ("Hook 6 user manual and technical data (EN B)", "Niviuk",
           "https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf",
           "Manufacturer")
GRAD_GO = ("Go user manual", "Gradient (hosted by the DHV)",
           "https://service.dhv.de/dbfiles/managed/pruefung/2019/07/go_manual_en_r0_fin.pdf", "Manufacturer")
NOVA_M2 = ("Mentor 2 manual (EN B, 2011)", "Nova",
           "https://www.nova.eu/fileadmin/user_upload/glider/Manuals/Mentor2_V11_012011eng.pdf", "Manufacturer")
SKY_ATIS3 = ("Atis 3 user's manual (EN B, 2009)", "Sky Paragliders",
             "https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf", "Manufacturer")
MP_MUSE5 = ("Muse 5 technical data (EN A)", "Mac Para",
            "https://www.macpara.com/en/paragliders/free-flying/muse-5/", "Manufacturer")
MP_EDEN7 = ("Eden 7 technical data (EN B)", "Mac Para", "https://www.macpara.com/en/previous-products/eden-7",
            "Manufacturer")
MP_ELAN3 = ("Elan 3 technical data (EN C)", "Mac Para",
            "https://www.macpara.com/en/paragliders/free-flying/elan-3/", "Manufacturer")
SKYWALK = ("Chili 5 product page: why no performance figures are published", "Skywalk",
           "https://skywalk.info/project/chili5/", "Manufacturer")
ADV_A8 = ("Alpha 8 manual: flight characteristics (EN A)", "Advance", "https://manual.advance.ch/en/alpha_8/4009",
          "Manufacturer")
UP_LHOTSE = ("Lhotse manual (EN B)", "UP International",
             "https://www.up-paragliders.com/images/downloads/LHOTSE/Lhotse_Manual_E_V1.2.pdf", "Manufacturer")
UP_TALK = ("Franta and Jarda talk: 2 and 2.5 liner designs", "UP International",
           "https://www.up-paragliders.com/news/franta-jarda-talk-2-and-2-5-liner-designs", "Manufacturer")
DHV_CLASS = ("Classification (LTF A to D)", "DHV, German Hang Gliding and Paragliding Association",
             "https://www.dhv.de/en/type-inspection/classification/", "Federation")
DHV_SJ = ("Safety Journal", "DHV, German Hang Gliding and Paragliding Association",
          "https://dhv.de/en/safety/safety-journal", "Federation")
DHV_REC = ("Empfehlungen zur Auswahl der Gleitschirmklasse (class selection recommendations, German)",
           "DHV, German Hang Gliding and Paragliding Association",
           "https://www.dhv.de/media/seiten/02_fliegen/Sicherheit/EmpfehlungenAuswahlGleitschirmklasse.pdf",
           "Federation")
SHV_EN = ("Description des classes EN (EN class descriptions, French)", "SHV/FSVL, Swiss Hang Gliding Association",
          "https://www.shv-fsvl.ch/fileadmin/files/redakteure/Allgemein/Sicherheit/Sicherheit/EN-Klassen_Beschreibung_FR.pdf",
          "Federation")
CIVL_CCC = ("Sporting Code Section 7G: CIVL Competition Class paraglider requirements, 2024", "FAI / CIVL",
            "https://www.fai.org/sites/default/files/civl/documents/sporting_code_s7_g_-_ccc_paragliders_requirements_2024.pdf",
            "Federation")
FAI_CCC16 = ("What's Up With The New CCC Paragliders? (2016)", "FAI", "https://fai.org/node/21590", "Federation")
XC_BLOWOUT = ("Paragliding techniques: how to handle a collapse (2006)", "Cross Country Magazine",
              "https://xcmag.com/news/blowout/", "Magazine")
XC_ACTIVE = ("Active flying, extract from Bruce Goldsmith (2023)", "Cross Country Magazine",
             "https://xcmag.com/other/active-flying/", "Magazine")
FB_CONTROL = ("Paraglider control: stall, spin, collapse!", "Flybubble",
              "https://flybubble.com/blog/paraglider-control-stall-spin-collapse", "School")
FB_SAFETY = ("Paragliders: safety", "Flybubble", "https://flybubble.com/blog/paragliders-safety", "School")
FB_CLASS = ("Paragliders: which class?", "Flybubble", "https://flybubble.com/blog/paragliders-which-class", "School")
SN_BIG = ("Dealing with big collapses", "SkyNomad Paragliding School",
          "https://www.skynomad.com/dealing-with-big-collapses", "School")
CAA_NZ = ("Safety Investigation Report 20/153: fatal paraglider accident, Mount Cheeseman", "Civil Aviation Authority of New Zealand",
          "https://www.aviation.govt.nz/assets/publications/fatal-accident-reports/20-153-fatal-paraglider-accident-mount-cheeseman-canterbury.pdf",
          "Government")

ENTRIES = [
    # ------------------------------------------------------------------ 1
    {
        "slug": "how-does-a-paraglider-fly",
        "q": "How does a paraglider fly?",
        "also": ["How do paragliders work?", "How does paragliding work?", "Does a paraglider have an engine?"],
        "series": "flight-mechanics",
        "topic": "How a paraglider flies",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": False,
        "seo_title": "How Does a Paraglider Fly? Lift, Shape and Gravity",
        "seo_desc": "How a fabric wing inflates into an airfoil, where its lift comes from, why gravity is its engine "
                    "and how pilots steer. Sourced, with the designers on the show.",
        "short": "A paraglider is a fabric wing that only becomes a wing in flight. Air rushing into openings along "
                 "the front inflates its cells into an airfoil, and that airfoil makes lift as it moves through the "
                 "air. There is no engine: gravity pulls it forward along a gently descending glide, and it climbs "
                 "only when the air around it rises faster than it sinks.",
        "sources": [FAA_GFH3, NASA_3F, NASA_LIFT,
                    ("Effects of Inclination on Lift", "NASA Glenn Research Center",
                     "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/incline", "Government"),
                    WIKI_PG,
                    ("Paraglider structure, materials and maintenance", "SkyNomad Paragliding School",
                     "https://www.skynomad.com/articles/paraglider_construction.html", "School"),
                    OZ_RUSH6, GIN_B8, NIV_H6, GRAD_GO,
                    ("Weight and Balance Handbook (FAA-H-8083-1B), addendum", "FAA",
                     "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/Weight_Balance_HB_Addendum_%28MOSAIC%29.pdf",
                     "Government handbook"),
                    NASA_TN,
                    ("Active flying", "SkyNomad Paragliding School", "https://www.skynomad.com/active-flying",
                     "School"),
                    MP_EDEN7, SKY_ATIS3],
        "sections": [
            {"kicker": "Shape", "h": "How does a fabric wing keep its shape?",
             "short": "Air pressure does the job a rigid frame does on an aircraft. The cells fill through the "
                      "front and the ribs hold the profile.",
             "paras": [
                 "A paraglider is two skins of fabric, a top and a bottom surface, joined by internal walls called "
                 "ribs that divide the wing into cells [5][6]. Most cells are open only at the leading edge. As the "
                 "wing moves forward, air rams in through those openings, pressurises the inside and holds the "
                 "whole wing in shape [5]. Because the ribs are cut to the profile the designer wants, the inflated "
                 "wing takes on a proper airfoil cross-section [6].",
                 "The suspension lines attach underneath, where the ribs meet the bottom surface. The A lines sit "
                 "nearest the leading edge, the B, C and sometimes D rows follow behind them, and the brake lines "
                 "run to the trailing edge [5][6]. Designers size the cell openings so the wing stays pressurised in "
                 "every flight mode [10], and keeping that internal pressure steady is, as Ozone's manual puts it, "
                 "the goal of flying in rough air [7]."],
             "bold": ["ribs", "rams in"],
             "figure": {"img": "kb-flight-mechanics-section", "w": 2400, "h": 1000,
                        "alt": "Cutaway of a paraglider wing at a rib, with cross-ports, and airflow over the "
                               "upper and lower surface",
                        "cols": 2,
                        "captions": [("Cells", "Ribs cut to the airfoil divide the wing into cells, open at the nose "
                                               "so air can ram in."),
                                     ("Lines", "The lines attach under the ribs, from the A row nearest the nose to "
                                               "the brakes on the trailing edge.")],
                        "source_html": "Schematic, not to scale. Construction as described in sources 5 and 6."}},
            {"kicker": "Lift", "h": "Where does a paraglider's lift come from?",
             "short": "From the angle at which the wing meets the air. Change that angle and you change almost "
                      "everything about how the wing flies.",
             "paras": [
                 "Like any wing, a paraglider makes lift as air flows around it. NASA's lift equation sets out what "
                 "that lift depends on: the density of the air, the area of the wing, the square of its speed, and "
                 "a lift coefficient that captures the wing's shape and the angle at which it meets the airflow "
                 "[3]. Doubling the airspeed gives four times the lift, and thinner air, at altitude or on a hot "
                 "day, gives less [1].",
                 "That angle is the angle of attack: the angle between the wing's chord line and the oncoming air "
                 "[1]. Within the normal range, more angle of attack means more lift, almost in proportion. Past a "
                 "critical angle the airflow separates from the top surface and the lift is lost suddenly, which "
                 "is a stall [1][4].",
                 "A paraglider pilot changes the angle of attack directly. The brakes pull the trailing edge down, "
                 "which raises it [9]; the speed bar pulls the front risers down, which lowers it [10]. Almost "
                 "everything a paraglider does, from a {{what-is-a-stall-on-a-paraglider|stall}} at one end to a "
                 "{{what-happens-if-a-paraglider-collapses|collapse}} at the other, comes back to angle of attack."],
             "bold": ["angle of attack", "lift coefficient"]},
            {"kicker": "Gravity", "h": "With no engine, what pushes a paraglider forward?",
             "short": "Gravity. A glider is always descending through the air it flies in, and the slope of that "
                      "descent keeps it moving.",
             "paras": [
                 "Only three forces act on a glider: its weight, lift and drag. There is no thrust [2]. Lift acts at "
                 "right angles to the flight path and drag acts straight back along it, so the only way to balance "
                 "them is to fly a gently descending path. Along that path, part of the weight points forward and "
                 "pulls the glider along; the FAA's glider handbook calls gravity the glider's external engine [1].",
                 "So a paraglider always sinks relative to the air around it [2]. Manufacturers that publish the "
                 "figure claim a minimum sink of a little over one metre per second [14][15]. How far the wing "
                 "travels for each metre it descends is its {{what-is-the-glide-ratio-of-a-paraglider|glide ratio}}, "
                 "and staying up for hours is a matter of finding air that rises faster than the wing sinks: "
                 "{{how-does-a-paraglider-go-up|thermals and ridge lift}}."],
             "bold": ["gravity"]},
            {"kicker": "Pendulum", "h": "Why does the pilot hang so far below the wing?",
             "short": "Because a weight hanging well below a wing behaves like a pendulum, and a pendulum wants to "
                      "settle straight down.",
             "paras": [
                 "The pilot sits in a harness below the canopy, held up by a network of lines [5]. The "
                 "FAA describes the same arrangement on a powered parachute, the motorised cousin of the "
                 "paraglider: with the weight hanging beneath an inflated ram-air wing, the aircraft acts like a "
                 "pendulum [11]. Paragliding schools teach it the same way, as the wing's inherent pendulum "
                 "stability [13]. After a gust or a turn, the pilot's weight tends to swing back under the wing and "
                 "bring the whole system back to level.",
                 "Lower is not automatically better. NASA's research on wings with hanging payloads in the 1960s "
                 "found that increasing the distance between payload and wing reduced the damping of one rolling "
                 "motion [12]. And the pendulum is only half the story in pitch: a paraglider has no tail, so the "
                 "profile itself has to keep the nose from tucking, which is where the designers on the show come "
                 "in."],
             "bold": ["pendulum"]},
            {"kicker": "Steering", "h": "How do you steer a paraglider?",
             "short": "Lean first, then add brake on the side you want to turn towards. Both brakes together slow "
                      "the wing down.",
             "paras": [
                 "Each hand holds a brake handle connected to the trailing edge on that side of the wing. The brakes "
                 "control speed, steer together with weight shift, and flare the wing for landing [5]. Leaning in "
                 "the harness moves the hanging weight sideways and banks the wing, the centre-of-gravity steering "
                 "NASA describes for wings with suspended payloads [12].",
                 "Manufacturers teach the same order: shift your weight first, then add the inside brake smoothly, "
                 "and use the outside brake and your body to control the speed and radius of the turn [7][8]. As "
                 "the wing banks, its lift tilts: part of it still holds the pilot up and the sideways part pulls "
                 "the glider round the turn [1]. One rule from Ozone's manual is worth knowing early: never start a "
                 "turn at minimum speed with the brakes fully down, because it risks a spin [7]."],
             "bold": ["weight shift"]},
        ],
        "show": [
            ("Luc Armant", LUC_M, "c2", "Stability lives in the profile",
             "A paraglider has no tail, so its pitch stability has to come from the shape of the profile. Luc "
             "Armant of Ozone explains it through the moment coefficient: on a stable profile, as the angle of "
             "attack falls, the lift moves forward and pulls the nose back up."),
            ("Michael Nesler", NESLER, "c3", "Thick profiles, fewer lines",
             "Today's profiles are around 18 percent of the chord thick, Michael Nesler says, far thicker than the "
             "wings of the early years. Thick sections suit the low speeds paragliders fly at, and the extra volume "
             "holds the shape with fewer line attachment points."),
            ("Helmut Schrempf", HELMUT, "c4", "The pendulum buys time",
             "SIV coach Helmut Schrempf sees the pendulum as an ally. In the first moment of most collapses the "
             "angle of attack rises and the wing drops behind the pilot, and that swing gives time to let go of "
             "the B risers and get onto the brakes."),
        ],
        "related": ["how-does-a-paraglider-go-up", "what-is-the-glide-ratio-of-a-paraglider",
                    "how-fast-does-a-paraglider-fly", "what-is-a-stall-on-a-paraglider",
                    ("faq", "flight-mechanics", "Why is a paraglider stable in pitch when it has no tail?"),
                    ("faq", "flight-mechanics", "What is pitch-up tendency in a paraglider?")],
    },
    # ------------------------------------------------------------------ 2
    {
        "slug": "how-does-a-paraglider-go-up",
        "q": "How does a paraglider go up?",
        "also": ["How do paragliders gain altitude?", "How do paragliders climb?",
                 "How do paragliders stay in the air for hours?"],
        "series": "flight-mechanics",
        "topic": "Thermals and lift",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": False,
        "seo_title": "How Does a Paraglider Go Up? Thermals and Ridge",
        "seo_desc": "A paraglider always sinks through the air, so it climbs in air rising faster than it sinks: "
                    "thermals, ridge lift, wave and convergence, explained with sources.",
        "short": "By flying in air that rises faster than the wing sinks. A paraglider is always descending through "
                 "the air around it, at best a little over a metre per second, so pilots climb by circling in thermals "
                 "of sun-warmed air or by flying along a ridge where the wind is forced upwards. Typical thermals "
                 "rise at one to three metres per second.",
        "sources": [NASA_GLIDERS, MP_EDEN7, SKY_ATIS3, OZ_RUSH6, OZ_SWIFT,
                    ("Parcel theory (JetStream)", "NOAA National Weather Service",
                     "https://www.noaa.gov/jetstream/upperair/parcel-theory", "Government"),
                    AC006A, FAA_GFH10,
                    ("Thermal structure and behavior (W. M. Angevine, 2014)", "NOAA Chemical Sciences Laboratory (staff pages)",
                     "https://esrl.noaa.gov/csl/staff/wayne.m.angevine/wayne.m.angevine.presentations/thermals_2014.pdf",
                     "Research"),
                    ("Glider Flying Handbook (FAA-H-8083-13A, 2013), Chapter 10", "FAA, hosted by the British Gliding Association",
                     "https://www.gliding.co.uk/wp-content/uploads/sites/3/2019/11/Soaring-Chap10-FAA.pdf",
                     "Government handbook"),
                    WIKI_PG, CAA_NZ],
        "sections": [
            {"kicker": "The principle", "h": "How can a glider climb without an engine?",
             "short": "It cannot climb through the air. It climbs with the air, when that air rises faster than "
                      "the glider sinks.",
             "paras": [
                 "A glider always descends relative to the air it flies in. NASA puts the trick simply: find a "
                 "pocket of air rising faster than the glider is descending, and the glider goes up [1]. Everything "
                 "about soaring follows from that one idea.",
                 "Manufacturers that publish the figure claim a minimum sink of about 1.0 to 1.15 metres per second "
                 "for their paragliders [2][3]. Minimum sink is usually reached with a little brake rather than "
                 "hands up, about 20 cm on Ozone's Rush 6 [4], and it is the speed for the best climb [5]. As a "
                 "worked example from those figures: in air rising at 3 metres per second, a wing sinking at a "
                 "little over 1 metre per second climbs at a little under 2, before any losses from turning."],
             "bold": ["rising faster", "minimum sink"]},
            {"kicker": "Thermals", "h": "What is a thermal?",
             "short": "A rising bubble or column of air that the sun has warmed at the ground. Pilots circle inside "
                      "it to climb.",
             "paras": [
                 "Warm air is less dense than cool air. Gravity pulls the cooler, denser air down; it spreads along "
                 "the ground, undercuts the warm air and forces it upwards [6]. A thermal is the rising part of that "
                 "small convection current, and the cool air sinking around it to feed the circulation is why "
                 "pilots meet sinking air between thermals [7].",
                 "Some ground heats faster than other ground. A slope facing the sun receives more energy for each "
                 "square metre, and darker surfaces warm faster than grass, which is why thermals come from "
                 "particular places rather than anywhere [8]. When the rising air reaches its condensation level, a "
                 "cumulus cloud starts to form on top of it [8], which is why pilots read clouds as signposts to "
                 "lift.",
                 "Typical thermals rise at about 1 to 3 metres per second and are a few hundred metres to a couple "
                 "of kilometres across [9]. The lift often grows stronger near cloud base [10]."],
             "bold": ["convection", "cumulus"],
             "figure": {"img": "kb-flight-mechanics-thermal", "w": 2400, "h": 760, "cols": 2,
                        "alt": "A thermal from above and from the side: the core sits upwind, turning into wind "
                               "finds it and turning downwind falls out of the back",
                        "captions": [("From above", "The core sits on the upwind side. Turning into wind (orange) "
                                                    "finds it; turning downwind (grey) drifts you out of the back."),
                                     ("From the side", "The column leans with the wind and the strongest air rises "
                                                       "at its upwind front.")],
                        "source_html": 'After Brett Janaway, <a href="../../episodes/%s.html#c5">chapter 5</a> and '
                                       '<a href="../../episodes/%s.html#c7">chapter 7</a>. Wind blows left to right.'
                                       % (BRETT, BRETT)}},
            {"kicker": "Ridge lift", "h": "What is ridge lift?",
             "short": "Wind blowing against a hill is forced up and over it. Pilots fly back and forth in the band "
                      "of rising air in front of the slope.",
             "paras": [
                 "When wind meets a hill or ridge it flows up and over the rise [7]. On the upwind face that makes a "
                 "band of rising air that follows the shape of the slope, and pilots stay up by flying along it "
                 "[8][11]. As long as the wind keeps blowing onto the slope, the lift is there.",
                 "Two cautions. The FAA's figure for ideal ridge-soaring wind, 15 to 20 knots, is written for "
                 "sailplanes [8]; that is 28 to 37 km/h, close to a paraglider's own trim speed, so it is no guide "
                 "for paragliders. And the air that goes up the front of a hill comes down behind it: a New Zealand "
                 "investigation into a fatal accident found lee-side turbulence the most probable cause of the "
                 "collapse that began it [12]."],
             "bold": ["upwind face", "lee-side turbulence"]},
            {"kicker": "Other lift", "h": "What are wave lift and convergence?",
             "short": "Two rarer sources of lift: standing waves downwind of mountains, and lines where two air "
                      "masses meet.",
             "paras": [
                 "Strong wind across a mountain range can set up standing waves downwind of it, giving smooth, "
                 "continuous lift to great heights. Almost all high-altitude sailplane flights use it, and the sink "
                 "on the downward side of a wave can be strong [8][7].",
                 "Where two air masses meet, for example a sea breeze running into another airflow, the air is "
                 "pushed up along the line between them, and a row of cumulus often marks it [7][8]."],
             "bold": ["standing waves", "two air masses meet"]},
        ],
        "show": [
            ("Brett Janaway", BRETT, "c2", "Contrast beats heat",
             "Thermals depend on contrast and triggers more than on temperature, says Brett Janaway, who lives and "
             "flies in Slovenia and can fly 100 km there in any month of the year. A hot desert with nothing to "
             "break up the surface can be surprisingly stable."),
            ("Brett Janaway", BRETT, "c3", "A bubble under a skin",
             "He pictures a thermal source as a bubble of warm air under a skin: the colder, denser air above holds "
             "it down until a trigger, a pylon in his favourite example, breaks the skin and lets it go."),
            ("Brett Janaway", BRETT, "c5", "A 3 metre climb is a 4 metre thermal",
             "Brett puts the average thermal in most places pilots fly at about 2 to 3 metres per second, and points "
             "out that a 3 metre climb on the vario means air rising at about 4, because the wing is sinking the "
             "whole time. The hottest air rises most steeply, so the "
             "strongest lift sits at the upwind front of the bubble."),
        ],
        "related": ["how-does-a-paraglider-fly", "what-is-the-glide-ratio-of-a-paraglider",
                    ("faq", "flight-mechanics", "Which way should I turn when I hit a thermal?"),
                    ("faq", "navigators", "How do you find thermals in flat country?"),
                    ("faq", "weather-patterns", "What is a convergence line in paragliding?"),
                    ("faq", "meteorology", "Can a cloud suck you in when paragliding?")],
    },
    # ------------------------------------------------------------------ 3
    {
        "slug": "what-is-the-glide-ratio-of-a-paraglider",
        "q": "What is the glide ratio of a paraglider?",
        "also": ["How far can a paraglider glide?", "What is a good glide ratio for a paraglider?",
                 "Does a hang glider glide further than a paraglider?"],
        "series": "flight-mechanics",
        "topic": "Glide ratio",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": False,
        "seo_title": "Paraglider Glide Ratio: Real Numbers by Class",
        "seo_desc": "Most paragliders glide about 8 to 11 metres for every metre of height. What glide ratio means, "
                    "real figures by class, best-glide speed, wind, and how it compares.",
        "short": "Roughly 8 to 11. In still air, most paragliders travel about 8 to 11 metres forward for every "
                 "metre of height they lose: around 8 to 10 for school and intermediate wings and about 10 to 11 "
                 "for performance wings, with competition wings reported higher. Wind changes how far that takes "
                 "you over the ground, not the glide through the air.",
        "sources": [FAA_GFH3,
                    ("Drag to Lift Ratio", "NASA Glenn Research Center",
                     "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-to-lift-ratio", "Government"),
                    ("Vector Balance of Forces: Glider", "NASA Glenn Research Center",
                     "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/vector-balance-of-forces-glider",
                     "Government"),
                    FAA_GFH5, OZ_RUSH6, NIV_H6T,
                    ("Sol Prymus", "Wikipedia", "https://en.wikipedia.org/wiki/Sol_Prymus", "Encyclopedia"),
                    MP_MUSE5, MP_EDEN7, MP_ELAN3, SKY_ATIS3, WIKI_PG, SKYWALK,
                    ("Hang gliding", "Wikipedia", "https://en.wikipedia.org/wiki/Hang_gliding", "Encyclopedia"),
                    ("Glider (sailplane)", "Wikipedia", "https://en.wikipedia.org/wiki/Glider_(sailplane)",
                     "Encyclopedia"),
                    ("What is the difference between a hang glider and a sailplane?", "Soaring Society of America",
                     "https://www.ssa.org/faq-items/what-is-the-difference-between-a-hang-glider-and-a-sailplane/",
                     "Federation")],
        "sections": [
            {"kicker": "Definition", "h": "What does glide ratio measure?",
             "short": "Distance forward for each unit of height lost, in still air. A glide of 10 to 1 means 10 "
                      "metres forward for every metre down.",
             "paras": [
                 "The glide ratio is the distance a glider can travel for a given loss of height [1]. In a steady "
                 "glide it is the same number as the wing's lift-to-drag ratio, L/D: the more lift a wing makes for "
                 "each unit of drag, the flatter it glides and the further it goes for the same height [2][3].",
                 "Put in a pilot's terms, from 1,000 metres above the ground in still air, a wing gliding at 10 to 1 "
                 "reaches about 10 km before it lands. That is a worked example rather than a promise: real air is "
                 "rarely still, and the glide you get over the ground depends on the wind."],
             "bold": ["lift-to-drag ratio"],
             "figure": {"img": "kb-enc-glide", "w": 2400, "h": 700, "cols": 3,
                        "alt": "Glide paths from 1,000 metres drawn to scale: a paraglider reaching about 8 to 11 km, "
                               "a hang glider about 16 to 20 km and a sailplane about 38 to 60 km",
                        "captions": [("Paraglider", "About 8 to 11 km from 1,000 m in still air."),
                                     ("Hang glider", "About 16 to 20 km: flex wings near 17, rigid wings near "
                                                     "20."),
                                     ("Sailplane", "About 38 to 52 km for 15 to 18 metre ships, about 60 for the "
                                                   "open class and more than 70 for the largest.")],
                        "source_html": "Worked from the glide ratios in sources 7 to 12 and 14 to 16. Still air, "
                                       "horizontal distance to scale, height exaggerated."}},
            {"kicker": "Real numbers", "h": "What glide do real paragliders get?",
             "short": "Manufacturer claims run from about 8 for a school wing to 10.5 for an EN C. Most brands "
                      "publish no figure at all.",
             "paras": [
                 "Published figures are manufacturer claims, made in calm air by the maker's own method. Sol's EN A "
                 "Prymus 4 is listed at 8.3 [7]. Mac Para claims more than 10 for both its EN A Muse 5 and its EN B "
                 "Eden 7 [8][9], and 10.5 for its EN C Elan 3 [10]. An EN B from 2009, Sky's Atis 3, claimed more "
                 "than 8.8 [11]. Wikipedia's summary runs from 9.3 for recreational wings to about 11.3 for "
                 "competition models, and up to 13 in some cases [12], but no maker publishes a measured figure for "
                 "a current competition wing.",
                 "Most of the big brands publish no glide figure at all. Skywalk explains why: the number depends on "
                 "the pilot's harness and seated position, the size of the wing, the air mass and the total weight, "
                 "so it cannot be compared fairly between gliders [13]. Older sources give 8 to 1 as about the best "
                 "a paraglider could do [16]. Wings have improved since, but two claims from two brands are still "
                 "not a like-for-like test."],
             "bold": ["manufacturer claims"],
             "callout": {"kicker": "Manufacturer claims", "heading": "Still-air glide, three classes",
                         "text": "Claimed best glide in calm air, from the makers' own data. A rough guide to the "
                                 "range, not a ranking of wings.",
                         "cite": [7, 9, 10],
                         "numbers": [("8.3", "", "Sol Prymus 4, EN A"), ("10+", "", "Mac Para Eden 7, EN B"),
                                     ("10.5", "", "Mac Para Elan 3, EN C")]}},
            {"kicker": "Speed", "h": "At what speed does a paraglider glide best?",
             "short": "Usually hands up, at trim speed. A little brake gives the slowest sink; a lot of speed bar "
                      "costs glide.",
             "paras": [
                 "Every glider has a speed polar, a curve of sink rate against airspeed. Its highest point is the "
                 "minimum sink: the slowest descent and the longest time in the air. A line from the origin that "
                 "just touches the curve marks the best-glide speed, and dividing that speed by the sink rate there "
                 "gives the best glide ratio [4].",
                 "On a typical paraglider the best still-air glide comes at trim speed, hands up, and a little brake "
                 "moves the wing to minimum sink [5]. Up to about half speed bar costs little glide, while full bar "
                 "flies fastest but noticeably worse [5][6]. A heavier pilot on the same wing glides just as well, "
                 "only faster [4]."],
             "bold": ["speed polar", "best-glide speed"]},
            {"kicker": "Wind", "h": "How does wind change a paraglider's glide?",
             "short": "It changes the glide over the ground. Into a headwind you cover less ground for the same "
                      "height; with a tailwind, more.",
             "paras": [
                 "Wind does not change how the wing flies through the air, but it changes your groundspeed: a "
                 "headwind slows you over the ground and a tailwind speeds you up [4]. As a worked example, take a "
                 "wing gliding at 10 to 1 at 38 km/h. In a 20 km/h headwind it covers about 4.7 metres of ground "
                 "for every metre of height; with a 20 km/h tailwind, about 15.",
                 "That is why pilots fly faster into a headwind and through sinking air, which gains distance over "
                 "the ground [4], and it is what the speed bar is for [5]. With a tailwind the best speed lies "
                 "between minimum sink and best glide [4]."],
             "bold": ["groundspeed"]},
            {"kicker": "Comparison", "h": "How does a paraglider compare with a hang glider or a sailplane?",
             "short": "A hang glider glides roughly twice as far and a sailplane four to seven times as far. The "
                      "difference is speed, not sink.",
             "paras": [
                 "Flex-wing hang gliders glide at about 17 to 1 and rigid wings at about 20 [14]; the Soaring Society of "
                 "America puts hang gliders at 16 [16]. Sailplanes "
                 "with 15 to 18 metre spans glide at 38 to 52 to 1, open-class ships at around 60, and the largest, "
                 "the Eta, at more than 70 [15].",
                 "The surprise is the sink rate. The example sailplane in the FAA's handbook reaches its minimum "
                 "sink of 1.9 knots at 40 knots [4], about 1 metre per second at 74 km/h, which is no slower a "
                 "descent than a paraglider's best. The sailplane's advantage is that it sinks that slowly while "
                 "flying twice as fast, and glide ratio is simply forward speed divided by sink."],
             "bold": ["sink rate"]},
        ],
        "show": [
            ("Roman Barthelemy", SKYMATE, "c6", "The harness is part of the glide",
             "Roman Barthelemy of Supair puts the drag of a pod with a fairing at about 12 newtons, a chair harness "
             "at roughly 23, he thinks, and a submarine-style pod at about 8. The simulations promised nearly a full point of glide for "
             "the submarine over a good faired pod; in real flying he puts it at about half a point."),
            ("Luc Armant", LUC_D, "c7", "School wings could glide better",
             "Luc Armant of Ozone thinks even school wings could glide better without becoming less forgiving, for "
             "example by cutting line drag, and says schools would welcome more glide for their students."),
            ("Helmut Schrempf", HELMUT, "c5", "Find your own minimum sink",
             "The old rule of thumb that minimum sink sits at 15 to 20 percent brake may not hold on modern wings, "
             "Helmut Schrempf says; on higher aspect ratio wings it may be close to hands up. He has not measured "
             "it, and his advice is to find the point on your own wing."),
        ],
        "related": ["how-fast-does-a-paraglider-fly", "what-does-the-speed-bar-do-on-a-paraglider",
                    "what-is-aspect-ratio-on-a-paraglider", "how-does-a-paraglider-go-up",
                    ("faq", "new-technologies", "How much glide does a submarine harness add?")],
    },
    # ------------------------------------------------------------------ 4
    {
        "slug": "how-fast-does-a-paraglider-fly",
        "q": "How fast does a paraglider fly?",
        "also": ["What is the top speed of a paraglider?", "What is trim speed on a paraglider?",
                 "How slow can a paraglider fly?"],
        "series": "flight-mechanics",
        "topic": "Speed",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": False,
        "seo_title": "How Fast Does a Paraglider Fly? Real Speeds",
        "seo_desc": "Most paragliders fly about 37 to 40 km/h hands up, 23 to 25 km/h at minimum and 46 to 62 km/h "
                    "on full bar. Real figures by class, plus weight, altitude and wind.",
        "short": "Where makers publish figures, paragliders fly at about 37 to 40 km/h hands up, with a minimum speed of roughly 23 "
                 "to 25 km/h on the brakes. The speed bar adds the rest: from the high 40s on a school wing to the "
                 "low 50s on an EN B, the mid 50s on an EN C and above 60 km/h on high-end wings.",
        "sources": [MP_MUSE5, MP_EDEN7, MP_ELAN3, SKY_ATIS3,
                    ("Free flying gliders brochure 2020", "Mac Para",
                     "https://www.macpara.com/media/2553/free-gliders-mac_para-2020.pdf", "Manufacturer"),
                    WIKI_PG, FAA_GFH5, OZ_SWIFT, OZ_RUSH6, FAA_GFH3, SKYWALK,
                    ("UP's new two-liner Edge XR (2011)", "Cross Country Magazine",
                     "https://xcmag.com/news/ups-new-two-liner-edge-xr/", "Magazine"),
                    NIV_H6T,
                    ("Airwave Ten", "Wikipedia", "https://en.wikipedia.org/wiki/Airwave_Ten", "Encyclopedia"),
                    CIVL_CCC],
        "sections": [
            {"kicker": "The range", "h": "What are a paraglider's minimum, trim and top speeds?",
             "short": "Minimum and trim speed barely change between classes. Top speed is what separates them.",
             "paras": [
                 "A paraglider's speed comes as three numbers. Minimum speed is the slowest the wing flies, with "
                 "the brakes deep, just above the stall. Trim speed is hands up with no speed bar, the speed the "
                 "wing settles at on its own. Top speed is with the speed bar pushed all the way [6][9].",
                 "Mac Para publishes all three for its range: a minimum of 23 to 25 km/h in every class, trim of 37 "
                 "to 39 km/h on its EN A and EN B and 38 to 40 on its EN C, and top speeds of 46 to 48 km/h (EN A), "
                 "50 to 52 (EN B) and 53 to 55 (EN C) [1][2][3]. Its 2020 brochure lists the Magus, apparently an EN D, at "
                 "39 to 41 km/h trim and about 62 km/h on full bar [5]. Sky's EN B Atis 3 from 2009 sits in the same "
                 "place [4], and Niviuk's Hook 6 is certified with a 14 km/h speed range on the brakes and 25 km/h "
                 "in all with the speed bar [13]."],
             "bold": ["Minimum speed", "Trim speed", "Top speed"],
             "table": {"cols": ["Wing", "Class", "Minimum", "Trim", "Full bar"],
                       "rows": [["Mac Para Muse 5", "EN A", "23 to 25", "37 to 39", "46 to 48"],
                                ["Mac Para Eden 7", "EN B", "23 to 25", "37 to 39", "50 to 52"],
                                ["Sky Atis 3 (2009)", "EN B", "23", "37 to 38", "50 to 52"],
                                ["Mac Para Elan 3", "EN C", "23 to 25", "38 to 40", "53 to 55"],
                                ["Mac Para Magus", "EN D (probably)", "25", "39 to 41", "about 62"]],
                       "caption": "Speeds in km/h, manufacturer figures [1][2][4][3][5]. Most large brands publish "
                                  "no speed data, so these come from the makers that do."}},
            {"kicker": "Weight", "h": "Does pilot weight change a paraglider's speed?",
             "short": "Yes. A heavier pilot on the same wing flies faster, with almost the same glide.",
             "paras": [
                 "Adding weight shifts a glider's whole performance curve to higher speeds: it sinks faster at any "
                 "given speed but reaches the same best glide ratio, only faster. Sailplanes carry water ballast "
                 "for exactly this reason [7]. Paragliders follow the same rule: near the top of the certified "
                 "weight range the wing flies faster, and near the bottom it sinks a little more slowly [8].",
                 "The effect is smaller than many pilots expect. With lift equal to weight, speed rises with the "
                 "square root of the weight, so 10 percent more all-up weight gives about 5 percent more speed: a "
                 "worked example from the lift equation, not a measured figure. Ozone recommends the upper part of "
                 "the range for the most precise handling and advises against the very bottom [9]."],
             "bold": ["water ballast"]},
            {"kicker": "Altitude", "h": "Does a paraglider fly faster at altitude?",
             "short": "Yes. In thinner air the same wing has to fly faster to make the same lift.",
             "paras": [
                 "Lift falls as air density falls, with altitude or heat [10]. To carry the same weight in thinner "
                 "air, the wing has to fly faster through it, and Skywalk notes that a wing's speed changes with "
                 "altitude and with the total weight it carries [11]. Landings at high sites are faster for the "
                 "same reason, which the pilot on the show who flies highest describes below."],
             "bold": ["air density"],
             "figure": {"img": "kb-sky-gods-speed", "w": 2400, "h": 620, "cols": 2,
                        "alt": "Three horizontal bars for the same wing's speed: about 40 km/h at 2,000 m, about 50 "
                               "km/h at about 5,000 m and about 60 km/h at 8,000 m",
                        "captions": [("2,000 m to 8,000 m", "About 40 km/h becomes about 60. Everything, a collapse "
                                                            "included, happens faster."),
                                     ("Landing high", "At about 5,000 m you touch down at 25 to 30 km/h, too fast to "
                                                      "run out comfortably.")],
                        "source_html": 'After Antoine Girard, <a href="../../episodes/%s.html#c8">chapter 8</a>. '
                                       'Rounded, as he gives them.' % ANTOINE}},
            {"kicker": "Wind", "h": "How fast does a paraglider go over the ground?",
             "short": "Airspeed plus or minus the wind. A paraglider flies so slowly that the wind matters a great "
                      "deal.",
             "paras": [
                 "A headwind subtracts from groundspeed and a tailwind adds to it [7]. As a worked example, with a "
                 "trim speed of 38 km/h, a 20 km/h headwind leaves you crossing the ground at about 18 km/h, and a "
                 "headwind stronger than your trim speed moves you backwards. A tailwind of the same 20 km/h gives "
                 "close to 60 km/h over the ground.",
                 "That is why wind strength decides so much in paragliding, from whether a site is flyable to how "
                 "far a cross-country flight can go."],
             "bold": ["groundspeed"]},
            {"kicker": "Faster wings", "h": "How fast are competition paragliders?",
             "short": "The open-class racers of the early 2010s reached around 70 km/h. Today's competition rules "
                      "deliberately cap the speed system.",
             "paras": [
                 "UP's two-line open-class racer of 2011, the Edge XR, was quoted at a top speed of 70 km/h [12], "
                 "and a competition wing of the mid-2000s was listed at 65 km/h [14]. Competition wings today are "
                 "certified to CIVL's Competition Class, which limits how far the speed system may shorten the "
                 "front risers and so caps the top speed [15]."],
             "bold": ["Competition Class"]},
        ],
        "show": [
            ("Antoine Girard", ANTOINE, "c8", "Faster the higher you go",
             "At 2,000 metres his wing flies at about 40 km/h, at about 5,000 metres around 50 and at 8,000 metres "
             "around 60, Antoine Girard says. Everything happens faster up there, collapses included, and landings "
             "too: a wing that touches down at 15 to 20 km/h low down lands at 25 to 30 km/h at 5,000 metres."),
            ("Bill Belcourt", BELC, "c8", "Slower wings, more speed used",
             "By Bill Belcourt's reckoning, Competition Class wings are a good 20 km/h slower at the top than the "
             "open-class wings they replaced after 2011. That makes full speed usable most of the time, and pilots on slower C "
             "and D wings in the same gaggle fly flat out just to keep up."),
            ("Bryan Van Ostheim", BRYAN, "c3", "Parakites live above trim",
             "Parakites, the small reflex wings flown on dunes, are a different animal. Bryan Van Ostheim says they "
             "are flown above trim speed almost all the time, at 70 to 80 km/h along the dunes and over 100 km/h "
             "coming out of a turn."),
        ],
        "related": ["what-does-the-speed-bar-do-on-a-paraglider", "what-is-the-glide-ratio-of-a-paraglider",
                    "how-does-a-paraglider-fly",
                    ("faq", "sky-gods", "How fast does a paraglider fly at high altitude?"),
                    ("faq", "the-dark-side", "Why do competition pilots fly at full speed all the time?")],
    },
    # ------------------------------------------------------------------ 5
    {
        "slug": "what-does-the-speed-bar-do-on-a-paraglider",
        "q": "What does the speed bar do on a paraglider?",
        "also": ["What is a speed bar on a paraglider?", "How does a paraglider speed system work?",
                 "When should you use the speed bar?"],
        "series": "flight-mechanics",
        "topic": "Speed bar",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": True,
        "seo_title": "What Does the Speed Bar Do on a Paraglider?",
        "seo_desc": "How the speed bar shortens the front risers to lower the angle of attack, what it gains and "
                    "costs, and the safety rules every manual agrees on.",
        "short": "It makes the wing fly faster. Pushing the bar with your feet pulls the front risers down through "
                 "a set of pulleys, tilting the wing nose-down to a lower angle of attack. You gain speed and "
                 "progress into wind, at the cost of a higher sink rate and a wing that collapses more easily and "
                 "more violently.",
        "sources": [GRAD_GO, GIN_B8, NIV_H6T, NOVA_M2, OZ_RUSH6, CIVL_CCC, SKY_ATIS3, FAA_GFH5, OZ_LM7],
        "sections": [
            {"kicker": "Mechanism", "h": "How does a paraglider speed bar work?",
             "short": "It shortens the front risers. The wing tilts nose-down around the rear risers and flies "
                      "faster.",
             "paras": [
                 "The speed bar is a foot stirrup on the harness, connected by lines to pulleys on the risers. "
                 "Pushing it shortens the A risers most, the B risers less, and leaves the rear risers where they "
                 "are [1][3]. The wing rotates nose-down around the rear risers, its angle of attack falls, and it "
                 "flies faster [2][3]. At full bar the A risers of Niviuk's Hook 6 end up 145 mm shorter than the C "
                 "risers on most sizes [3]; on Nova's older Mentor 2 the difference was about 18 cm [4].",
                 "Many harnesses have a two-step bar. On Ozone's Rush 6 the lower step gives about half the "
                 "accelerated range, and full speed comes when the pulleys on the risers touch [5]. Competition "
                 "wings have a hard limit: CIVL's Competition Class lets the speed system shorten the front risers "
                 "by no more than 140 mm relative to the rearmost riser [6]."],
             "bold": ["foot stirrup", "angle of attack"],
             "figure": {"img": "kb-the-dark-side-speed", "w": 2400, "h": 620, "cols": 2,
                        "alt": "Schematic speed-range bars: an open-class wing before 2011 with much of its range "
                               "unused, and today a CCC bar mostly used while EN D and EN C bars sit at their limit",
                        "captions": [("Before 2011", "Open-class wings had a great deal of speed, and pilots rarely "
                                                     "dared use all of it."),
                                     ("Today", "Competition wings are slower at the top and used most of the time. "
                                               "Slower wings keeping pace sit at their limit.")],
                        "source_html": 'After Bill Belcourt, <a href="../../episodes/%s.html#c8">chapter 8</a>. '
                                       'Schematic, not to scale.' % BELC}},
            {"kicker": "Performance", "h": "How much faster does the speed bar make you?",
             "short": "On most wings, roughly 10 to 15 km/h over trim. Full bar is rarely the most efficient "
                      "choice.",
             "paras": [
                 "As a worked example from the Hook 6's certification figures, 14 km/h of speed range on the "
                 "brakes and 25 in all, the bar adds about 11 km/h above trim [3]. Makers' figures for EN A to EN C wings show full bar roughly 10 to 15 km/h above trim "
                 "(see {{how-fast-does-a-paraglider-fly|How fast does a paraglider fly?}}). Sky puts the gain at up "
                 "to 30 percent over trim [7]. The sink rate rises with speed, as every speed polar shows [8].",
                 "Used lightly, the bar costs little: up to half bar barely changes the glide on Ozone's Rush 6 [5]. "
                 "Full bar flies fastest but glides noticeably worse [3], and Sky's manual says plainly that full "
                 "bar is rarely the best choice [7]. The bar earns its keep into a headwind and through sinking air "
                 "between thermals, where flying faster covers more ground for the height lost [5][8]."],
             "bold": ["half bar", "headwind"]},
            {"kicker": "Safety", "h": "Is the speed bar dangerous?",
             "short": "It makes the wing easier to collapse, and a collapse at speed is harder and faster. The "
                      "manuals agree on four rules.",
             "paras": [
                 "A lower angle of attack leaves the wing closer to a collapse and more sensitive to turbulence "
                 "[5][3]. When a collapse does happen on bar, it comes faster and more dynamically than at trim "
                 "[2][1], and you may need more height to recover [4]. The manuals set out four rules:"],
             "list": [
                 "Keep accelerated flight away from the ground and be careful with it in turbulence: Ozone says to "
                 "avoid both, Gin to use caution in turbulence, and Gradient to use the bar very carefully, or not "
                 "at all, at low altitude [5][2][1].",
                 "Do not use the brakes while accelerated. Braking on bar weakens the profile and can cause the "
                 "very collapse you are trying to stop [5][2][4].",
                 "If the wing loses pressure or collapses, release the bar fully first, and only then correct [2][5]. "
                 "Niviuk's advice to add a light brake input fits the same order: bar off, then brake [3].",
                 "On wings fitted with rear-riser control, Ozone says to keep hold of the rear risers while "
                 "accelerated [5][9]."],
             "bold": ["four rules"]},
            {"kicker": "Riser control", "h": "Why do pilots fly on the risers when accelerated?",
             "short": "On performance wings the B or C risers control pitch without spoiling the profile the way the "
                      "brakes do.",
             "paras": [
                 "On many performance wings you can fly actively on the risers rather than the brakes while "
                 "gliding, which gives better feel [9]. Ozone's LM7 manual explains why: pulling the rear risers "
                 "raises the angle of attack more evenly across the chord and weakens the profile far less than "
                 "braking [9].",
                 "The inputs must be small, or you can stall part or all of the wing, and if the nose starts to fold "
                 "while you are on bar, release the bar first and only then make small C-riser inputs [9]. Riser control is for gliding in normal air; in strong "
                 "turbulence the manual sends you back to trim speed and active flying on the brakes [9]."],
             "bold": ["small"]},
        ],
        "show": [
            ("Luc Armant", LUC_M, "c2", "The rule that rewards the edge",
             "Luc Armant helped write the rule that limits how far the speed system of a competition wing can "
             "shorten the risers, to 14 cm. A very pitch-stable profile gets less speed out of that range, so the rule rewards wings built close "
             "to the edge of stability, a side effect he says the sport still has to solve."),
            ("Tom Lolies", TOM, "c12", "A touch of brake can speed you up",
             "On some high-level wings, touching the brakes at full speed makes the wing faster, not slower, Tom "
             "Lolies says: a barely visible deflection of the trailing edge reduces the profile's pitch-up "
             "tendency, so the profile pitches down and speeds up."),
            ("Helmut Schrempf", HELMUT, "c3", "Why two-liners steer on the Bs",
             "On bar, a two-liner's profile takes an S shape that pushes back when something tries to tuck the "
             "nose, Helmut Schrempf explains. Use the brakes instead of the B risers and you add lift at the "
             "trailing edge, and the front can collapse."),
        ],
        "related": ["how-fast-does-a-paraglider-fly", "what-happens-if-a-paraglider-collapses",
                    "what-is-active-flying-in-paragliding", "what-is-the-glide-ratio-of-a-paraglider",
                    ("faq", "flight-mechanics", "Why is a small amount of brake a problem on a modern two-liner?"),
                    ("faq", "the-dark-side", "Why do competition pilots fly at full speed all the time?")],
    },
    # ------------------------------------------------------------------ 6
    {
        "slug": "what-happens-if-a-paraglider-collapses",
        "q": "What happens if a paraglider collapses?",
        "also": ["Why does a paraglider collapse?", "What is a paraglider collapse?",
                 "What is the difference between an asymmetric and a frontal collapse?", "What is a cravat?"],
        "series": "flight-mechanics",
        "topic": "Collapses",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": True,
        "seo_title": "What Happens If a Paraglider Collapses?",
        "seo_desc": "Why paragliders collapse, asymmetric versus frontal collapses and cravats, what the manuals "
                    "say to do, and what the test pilots and designers on the show add.",
        "short": "Part of the wing loses its internal pressure and folds, usually because turbulence or sinking air "
                 "has suddenly lowered its angle of attack. A one-sided (asymmetric) collapse turns the wing towards "
                 "the folded side; a frontal collapse folds the leading edge across the span. Most collapses reopen "
                 "on their own. The pilot's job is to keep the wing flying straight and not overreact.",
        "sources": [OZ_DELTA4, GIN_B8, XC_BLOWOUT, NIV_H6, CAA_NZ, XC_ACTIVE, ADV_A8, SN_BIG, OZ_LM7, DHV_SJ,
                    FB_SAFETY,
                    ("A danger not only for paragliders (helicopter wake turbulence)", "Aero-Club der Schweiz",
                     "https://aeroclub.ch/en/eine-gefahr-nicht-nur-fur-gleitschirmflieger", "Federation")],
        "sections": [
            {"kicker": "Why it happens", "h": "Why does a paraglider collapse?",
             "short": "Because its angle of attack drops too low. Without pressure at the nose, part of a flexible "
                      "wing folds.",
             "paras": [
                 "A paraglider has no rigid structure; air pressure holds its shape, so turbulence can suddenly fold "
                 "part of it [1]. The trigger is a drop in angle of attack. When sinking air hits the leading edge, "
                 "it pushes the nose down and unloads the wing, and the pilot feels the pressure in the brakes fall "
                 "away first [3]. If the angle of attack goes strongly negative across the span, the whole leading "
                 "edge folds in a frontal collapse [2].",
                 "Angle of attack runs between two ways of losing the wing: too high and it stalls, too low and it "
                 "collapses. A brief brake input raises the angle for an instant and stops it going negative, which "
                 "is how pilots prevent many collapses before they happen [3]. These make a collapse more likely:"],
             "list": [
                 "Turbulence, especially when the pilot is not flying actively [4].",
                 "Entering or leaving strong thermals [4].",
                 "The speed bar, which lowers the angle of attack [1], and braking while accelerated [1][9].",
                 "Lee-side rotor behind terrain, the most probable cause of the collapse in a fatal accident "
                 "investigated in New Zealand [5].",
                 "The wake of a helicopter [12]."],
             "bold": ["angle of attack"],
             "figure": {"img": "kb-enc-aoa", "w": 2400, "h": 700, "cols": 3,
                        "alt": "One profile drawn at three angles to the oncoming air: too low, where the nose is "
                               "pushed in and the wing collapses; the normal flying range; and too high, where the "
                               "flow breaks away from the top surface and the wing stalls",
                        "captions": [("Too low: collapse", "Sinking air or the speed bar pushes the nose down. The "
                                                           "leading edge loses pressure and folds."),
                                     ("Flying", "Between the two, the wing is pressurised and flying. Active "
                                                "flying keeps it here."),
                                     ("Too high: stall", "Too much brake for too long. The airflow breaks away from "
                                                         "the top surface and the wing stops flying.")],
                        "source_html": "Schematic, not to scale. After sources 2 and 3, and the "
                                       "<a href=\"what-is-a-stall-on-a-paraglider.html\">stall</a> page."}},
            {"kicker": "Types", "h": "What is the difference between an asymmetric and a frontal collapse?",
             "short": "An asymmetric collapse folds one side and turns the wing. A frontal folds the leading edge and "
                      "usually reopens straight.",
             "paras": [
                 "In an asymmetric collapse one side of the wing deflates. The folded side adds drag and the wing "
                 "turns towards it, and as the pilot tilts with it, the turn can tighten [5]. Bruce Goldsmith, a "
                 "former world champion, puts the danger plainly: it is less the collapse itself than the spiral "
                 "dive that can follow [6].",
                 "In a frontal collapse the leading edge deflates across the span [5], and frontals usually reopen "
                 "without the wing turning [4]. After a collapse the wingtip sometimes catches in the lines and "
                 "stays trapped. That is a cravat, and it adds drag that keeps the wing turning [1][8]."],
             "bold": ["asymmetric collapse", "frontal collapse", "cravat"]},
            {"kicker": "What to do", "h": "What should you do when your paraglider collapses?",
             "short": "Keep flying straight with weight shift and a little brake on the open side. Let the wing "
                      "reopen. Do not overreact.",
             "paras": [
                 "If you are on the speed bar, release it first [2]. After that, the manufacturers agree on the first "
                 "response to an asymmetric collapse. Lean away from the "
                 "collapse, towards the side that is still flying, and use just enough brake on that side to hold "
                 "your direction [1][4][2]. Ozone says that alone brings the wing back most of the time [9]. Do not "
                 "over-brake the flying side: overreacting costs airspeed and can stall or spin the wing [4][8], "
                 "and Advance warns against forcing the wing open with heavy brake [7].",
                 "If the folded side does not reopen by itself, pump it, but the manuals differ on how: Niviuk "
                 "describes one full pull released at once, Advance a deep, fast but brief one, and Gin smooth, "
                 "progressive pumping [4][7][2]. They agree that pumping comes only after the wing has had the "
                 "chance to reopen by itself. A frontal usually "
                 "reopens without help; some manuals suggest a little symmetric brake and others none at all "
                 "[1][7][2]. Your own wing's manual is the authority.",
                 "For a cravat, first stabilise the wing and stop the turn, then clear the tip with the stabilo line "
                 "or with deep pumps on that side while leaning away [1][7]. For a very large cravat Ozone lists a "
                 "full stall as the next option, only with enough height and if you know what you are doing, and "
                 "says to throw the reserve at once if the rotation is accelerating and you cannot control it [1]."],
             "bold": ["Lean away from the collapse", "Your own wing's manual is the authority"]},
            {"kicker": "Testing", "h": "Does certification show how a wing behaves in a real collapse?",
             "short": "Only partly. Test collapses are pulled on purpose in calm air; real ones are often harder, in "
                      "every class.",
             "paras": [
                 "Certification collapses are induced deliberately in calm air. The DHV's safety officer notes that "
                 "real collapses are often more demanding than induced ones, in every class [10], and wings built "
                 "to resist collapse can recover more violently when they finally do fold [11]. No pilot and no "
                 "wing is immune, but correct active flying reduces the chances significantly [1].",
                 "The place to learn what your own wing does is a safety (SIV) course over water with qualified "
                 "instructors, not trial and error on a cross-country day."],
             "bold": ["more demanding"]},
        ],
        "show": [
            ("Gin Seok Song", GIN, "c10", "A wing has to be able to collapse",
             "A paraglider has to be able to collapse, Gin Seok Song says; one that never did would be more "
             "dangerous. What matters is how it reopens. A violent, impulsive reopening can fold the other side "
             "and cascade, and designers have spent twenty years making reopenings smoother through the internal "
             "structure and the shape of the inlets."),
            ("Tom Lolies", TOM, "c5", "A warning before the fold",
             "Modern profiles with pitch-up tendency fight a collapse instead of going with it, Tom Lolies "
             "explains. Instead of the whole wing folding at once, the pilot feels the harness go light as the "
             "lines lose tension, and gets time to react."),
            ("Helmut Schrempf", HELMUT, "c4", "Let the wing take what it needs",
             "On bar in rough air, before anything has folded, Helmut Schrempf keeps a little tension in his body. "
             "When he feels one side go light, he releases the tension in that hip and lets the wing take what it "
             "needs from his body. Pressing hard into the harness on that side, he says, rarely gives the "
             "wing the right amount and is how pilots start rolling."),
            ("Alain Zoller", ALAIN, "c9", "The flight envelope over collapses",
             "Alain Zoller, who runs the Air Turquoise test house, spends less time on collapses in safety courses "
             "because an induced collapse is not representative of what happens in the air. He works on the "
             "flight envelope instead: minimum speed, full stall, back-flying and recovery."),
        ],
        "related": ["what-is-active-flying-in-paragliding", "what-is-a-stall-on-a-paraglider",
                    "what-does-the-speed-bar-do-on-a-paraglider",
                    "what-do-en-a-b-c-and-d-paraglider-ratings-mean",
                    ("faq", "risk-vs-reward", "When should I throw my reserve?"),
                    ("faq", "risk-vs-reward", "When should I do my first SIV course?"),
                    ("faq", "brand-stories", "Why does a paraglider need to be able to collapse?")],
    },
    # ------------------------------------------------------------------ 7
    {
        "slug": "what-is-a-stall-on-a-paraglider",
        "q": "What is a stall on a paraglider?",
        "also": ["What is a parachutal stall?", "What is a deep stall in paragliding?",
                 "What is a spin on a paraglider?", "What is a full stall?"],
        "series": "flight-mechanics",
        "topic": "Stalls and spins",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": True,
        "seo_title": "Paraglider Stalls: Full, Spin and Parachutal",
        "seo_desc": "What makes a paraglider stall, the difference between a full stall, a spin and a parachutal "
                    "stall, what causes each and what the manuals say to do.",
        "short": "A stall happens when the wing meets the air past its critical angle of attack and stops flying. "
                 "On a paraglider that usually means too much brake for too long at too slow a speed, though "
                 "rear-riser input, a wet wing or lines out of trim can also cause one. A full stall drops the wing "
                 "behind the pilot, a one-sided stall becomes a spin, and a parachutal stall leaves the wing "
                 "inflated but sinking almost vertically.",
        "sources": [FAA_PHAKG,
                    ("Stall and Spin Awareness Training (AC 61-67C)", "FAA",
                     "https://www.faa.gov/documentlibrary/media/advisory_circular/ac_61-67c.pdf", "Government"),
                    FAA_GFH3, ADV_A8, OZ_DELTA4, FB_CONTROL, GIN_B8, DHV_SJ, UP_LHOTSE,
                    ("Flying in rain", "Ozone", "https://flyozone.com/paramotor/infozone/flying-in-the-rain",
                     "Manufacturer"),
                    ("Vector, November/December 2010: Life lines", "Civil Aviation Authority of New Zealand",
                     "https://aviation.govt.nz/assets/publications/vector/Vector_2010-6_Nov-Dec.pdf", "Government"),
                    OZ_LM7, XC_BLOWOUT],
        "sections": [
            {"kicker": "Aerodynamics", "h": "What causes a paraglider to stall?",
             "short": "Too much angle of attack. A stall is about the angle, not the speed.",
             "paras": [
                 "Every wing stalls at its critical angle of attack, whatever its airspeed, attitude or weight [1]. "
                 "Go past that angle and the airflow over the top separates and the wing stalls, every time [2]. A "
                 "stall can happen at any speed and in any attitude [2][3]. For aircraft in general, the FAA's rule "
                 "is that recovery means reducing the angle of attack [2]. On a paraglider that means letting the "
                 "brakes up, but only in the controlled way the manuals describe below.",
                 "On a paraglider the brakes are the pilot's main way of raising the angle of attack, so the hands "
                 "decide how close the wing is to a stall. Pulling both brakes down progressively and evenly is how a full "
                 "stall is entered on purpose [4], and holding a lot of brake for long in rough air can stall the "
                 "wing by accident [5]. Too much brake and the wing stalls [6]; too little angle of attack and it "
                 "collapses [13]. The two failures sit at opposite ends of the same scale."],
             "bold": ["critical angle of attack"],
             "figure": {"img": "kb-enc-aoa", "w": 2400, "h": 700, "cols": 3,
                        "alt": "One profile drawn at three angles to the oncoming air: too low, where the wing "
                               "collapses; the normal flying range; and too high, where the flow breaks away from "
                               "the top surface and the wing stalls",
                        "captions": [("Too low: collapse", "The nose loses pressure and folds. See the "
                                                           "collapse page."),
                                     ("Flying", "The wing is pressurised and flying, between the two limits."),
                                     ("Too high: stall", "The airflow breaks away from the top surface and the wing "
                                                         "stops flying, at any speed.")],
                        "source_html": "Schematic, not to scale. After sources 1, 2 and 13."}},
            {"kicker": "Full stall", "h": "What happens in a full stall?",
             "short": "The wing loses its airflow, deforms and drops behind you. Recovery is slow, even and "
                      "controlled.",
             "paras": [
                 "In a full stall the wing loses its airflow completely and deforms [7]. If the canopy falls behind "
                 "the pilot, the brakes have to be held down until it comes back overhead. They are then released "
                 "slowly and evenly at first, and fully only once the wing has refilled and is in front [7][4].",
                 "This is a manoeuvre for a safety course over water with an instructor, not something to try "
                 "alone. Designers also try to make the stall announce itself, as one of the guests explains below."],
             "bold": ["slowly and evenly"]},
            {"kicker": "Spin", "h": "What is a spin on a paraglider?",
             "short": "One side stalls while the other keeps flying, and the wing rotates around its vertical axis.",
             "paras": [
                 "In a spin one side of the wing stalls while the other keeps flying [7]. The glider rotates around "
                 "its vertical axis, one half moving forwards and the other backwards, and the slower you were "
                 "flying, the worse a spin tends to be [6]. That is why you should never start a turn at minimum "
                 "speed with the brakes fully down [5].",
                 "The first response the manuals give is hands up: release both brakes fully [4][7]. Gin adds one "
                 "condition: do not release a spin while the glider is far behind you [7]."],
             "bold": ["hands up"]},
            {"kicker": "Parachutal stall", "h": "What is a parachutal stall?",
             "short": "A stall in which the wing stays inflated but stops flying forward, sinking almost vertically. "
                      "It can look like normal flight.",
             "paras": [
                 "In a parachutal stall, which some manuals call a deep stall, the wing is stalled at a high angle "
                 "of attack but stays inflated because of the vertical descent [6]. It often looks as if it has "
                 "recovered properly while it carries on sinking straight down [5]. The signs are less airspeed and "
                 "wind noise, mushy brakes and a descent of about 4 to 5 metres per second [7]. The common causes:"],
             "list": [
                 "A wet wing, or ageing fabric that absorbs water more readily [7][8][10].",
                 "Lines out of trim: over time the front lines stretch and the rear lines shrink [7][11].",
                 "Brake lines that are too short [7][11], or low wing loading [7].",
                 "A very slow release from a B-line stall, or the aftermath of a frontal collapse [5].",
                 "Pulling the rear risers [9], or big ears, which raise the angle of attack, especially on a wet "
                 "wing [8][12]."],
             "after": [
                 "To get out of one: raise both hands fully, then push the A risers forward or use the speed bar "
                 "[5][7]. Never brake: even a few centimetres can turn it into a full stall [8][7]. With a wet "
                 "wing, Advance says to recover with the speed bar only [4]. If a landing in a parachutal stall "
                 "cannot be avoided, the DHV's advice is not to touch the brakes at all [8].",
                 "The manuals describe the recovery slightly differently, and the DHV has reported a case where the "
                 "standard methods failed [8], so the real defence is prevention: keep the wing in trim and the "
                 "brakes the right length. After any deep stall, have the wing and its line trim checked before "
                 "flying it again [7]."],
             "bold": ["Never brake"]},
        ],
        "show": [
            ("Tom Lolies", TOM, "c9", "A stall should announce itself",
             "Designers work to make the stall announce itself, Tom Lolies says: harder pressure in the brakes and "
             "a wing that deforms as it nears the stall, so the pilot knows to let the brakes up. He also counts "
             "learning the stall point, back-flying, the parachutal stall and the full stall as a key step in a "
             "pilot's progression, and a far easier one on a lower-class wing."),
            ("Tom Lolies", TOM, "c13", "The B risers stall sooner",
             "Stalling from the B risers is much easier than from the brakes, Tom warns. It comes a little sooner, "
             "the pressure is not as high as on the brakes, and on some gliders the recovery is trickier. To slow down hard in "
             "turbulence, use the brakes."),
            ("Tom Lolies", TOM, "c12", "Check the brake length",
             "Brake lines shrink and pilots get used to them, Tom says, and brakes that end up too short can leave "
             "a wing stuck in a parachutal stall at the worst moment. His checks: at least 7 cm of travel from "
             "hands up to the first tension, and no tension at full speed bar."),
        ],
        "related": ["what-happens-if-a-paraglider-collapses", "what-is-active-flying-in-paragliding",
                    "how-does-a-paraglider-fly", "what-does-the-speed-bar-do-on-a-paraglider",
                    ("faq", "flight-mechanics", "How do I check my brake line length?")],
    },
    # ------------------------------------------------------------------ 8
    {
        "slug": "what-is-active-flying-in-paragliding",
        "q": "What is active flying in paragliding?",
        "also": ["What is active piloting?", "How do you fly a paraglider actively?",
                 "How do you prevent paraglider collapses?"],
        "series": "flight-mechanics",
        "topic": "Active flying",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": True,
        "seo_title": "What Is Active Flying in Paragliding?",
        "seo_desc": "Active flying keeps the wing overhead and pressurised in moving air. How it works, why it "
                    "prevents most collapses, and how modern wings are changing it.",
        "short": "Active flying, or active piloting, is the stream of small corrections a pilot makes to keep the "
                 "wing directly overhead and fully pressurised in moving air. You feel the wing through the brakes "
                 "and the harness, brake when it surges ahead or loses pressure, and let it fly when it drops back. "
                 "It is the main defence against collapses, and modern wings are changing how it is done.",
        "sources": [OZ_DELTA4, OZ_LM7, GIN_B8, XC_ACTIVE, NIV_H6, SN_BIG, FB_CONTROL, DHV_CLASS, XC_BLOWOUT],
        "sections": [
            {"kicker": "Definition", "h": "What does active flying mean?",
             "short": "Keeping the wing overhead with a constant internal pressure, by feel.",
             "paras": [
                 "The aim is simple to state: keep the wing directly above you with a steady internal pressure [1]. "
                 "The method is to hold a constant pressure in the brakes and read the changes [1][2]. Bruce "
                 "Goldsmith describes active piloting as a way of feeling what is happening to the wing, keeping the "
                 "same weight and pressure on the brake lines at all times [4]. Pilots have long called it the main "
                 "defence against collapses [9].",
                 "To feel anything, the hands need contact. Ozone suggests flying with about 20 cm of brake applied "
                 "[1]; Gin describes a light, constant tension about equal to the weight of your arms [3]."],
             "bold": ["directly above you", "constant pressure"]},
            {"kicker": "Pressure", "h": "How do you stop a collapse before it happens?",
             "short": "When the pressure drops, brake on that side until it comes back, then give the wing its "
                      "speed again.",
             "paras": [
                 "If you feel the pressure fade, brake quickly until it returns, on one side or both [1]. Braking on "
                 "the side that is going soft raises its angle of attack and can stop the collapse before it starts "
                 "[5]. Then let the brake back up: make the input and restore the wing's flying speed, because "
                 "holding a correction too long can stall it [5]. Flying with a lot of brake for long periods in "
                 "rough air is how wings get stalled by accident [1]."],
             "bold": ["brake quickly", "restore the wing's flying speed"]},
            {"kicker": "Pitch", "h": "What do you do when the wing surges ahead or drops back?",
             "short": "Brake when it shoots ahead, let it fly when it falls behind, and be ready for the next "
                      "swing.",
             "paras": [
                 "If the wing pitches in front of you, brake to slow it. If it drops behind, release the brakes so "
                 "it can speed up, and be ready for the surge that follows [2]. These small, well-timed inputs keep "
                 "the glider flying smoothly overhead and dramatically reduce the chance of a collapse [2]."],
             "bold": ["pitches in front", "drops behind"],
             "figure": {"img": "kb-flight-mechanics-brakes", "w": 2400, "h": 640, "cols": 3,
                        "alt": "The same profile three times: hands up, a little brake, a lot of brake, showing "
                               "where the lift acts and how much drag there is",
                        "captions": [("Hands up", "Lift sits forward, near the nose. In a gust a modern profile "
                                                  "pitches back up, against the collapse."),
                                     ("A little brake", "The trailing edge barely moves, but the lift slides back "
                                                        "and the pitch-up tendency is gone, with hardly any extra "
                                                        "drag."),
                                     ("A lot of brake", "High lift and high drag. The wing slows right down and a "
                                                        "collapse becomes much less likely.")],
                        "source_html": 'After Tom Lolies, <a href="../../episodes/%s.html#c12">chapter 12</a>, and '
                                       'Helmut Schrempf, <a href="../../episodes/%s.html#c3">chapter 3</a>. Orange: '
                                       'where the lift acts. Grey: drag.' % (TOM, HELMUT)}},
            {"kicker": "Modern wings", "h": "Is active flying different on modern wings?",
             "short": "Yes. On stable modern profiles a little brake can do more harm than good, and many pilots "
                      "fly on the risers.",
             "paras": [
                 "Classic active flying assumes the brakes are always in play. Modern performance wings add another "
                 "option: piloting on the B or C risers while gliding, which gives better feel [2]. The risers "
                 "raise the angle of attack more evenly across the chord than the brakes, so they weaken the "
                 "profile less. Inputs must be small, the bar comes off first if the nose starts to fold, and in "
                 "strong turbulence Ozone sends pilots back to trim speed and the brakes [2].",
                 "Your wing's manual decides how you fly it. Two guests on the show add a point that matters for "
                 "anyone on a recent wing: Tom Lolies and Helmut Schrempf both say that on a stable modern profile "
                 "a small amount of brake can reduce the profile's own resistance to collapse without adding "
                 "enough drag to help. They fly hands up or on the risers and use plenty of brake when they need "
                 "it, Helmut still keeps light contact, and both stress that it depends on the wing."],
             "bold": ["small amount of brake", "Your wing's manual decides"]},
            {"kicker": "Limits", "h": "Does active flying prevent every collapse?",
             "short": "No. It reduces them greatly, but no wing and no pilot is immune.",
             "paras": [
                 "Ozone's manuals put it bluntly: no pilot and no glider are immune to collapses, but correct active "
                 "flying reduces the chances significantly [1]. Schools say the same [6][7]. The DHV's descriptions "
                 "of the higher classes assume it: C-class wings are for pilots who fly actively and regularly, "
                 "D-class wings for those who fly very actively [8].",
                 "Active flying is a skill for coping with turbulence, not a licence to go looking for it. Ozone's "
                 "own advice is to keep hold of the brakes at all times and not to fly in turbulent conditions [1]."],
             "bold": ["not a licence to go looking for it"]},
        ],
        "show": [
            ("Helmut Schrempf", HELMUT, "c3", "What schools used to teach",
             "Fifteen years ago schools taught that if you kept pressure on the brakes all the time, nothing would "
             "happen. Helmut Schrempf thinks that may have been wrong even then, and on today's wings a little "
             "brake removes the self-stabilising S shape of the profile without adding enough drag to steady the "
             "wing. His advice is more brake on both sides, or hands up and let the profile work, while keeping a "
             "little contact. He also warns that the old "
             "short, hard input on the outside brake can inject a collapse on a wing that is already correcting "
             "itself."),
            ("Helmut Schrempf", HELMUT, "c4", "Tension in the body",
             "On bar in rough air, Helmut keeps a little tension in his body so he notices when something changes. "
             "When he feels a carabiner drop, he releases that hip and lets the wing take what it needs; pressing "
             "into the harness, he says, rarely gives the wing the right amount."),
            ("Tom Lolies", TOM, "c12", "The worst input is a small one",
             "On the new, more stable wings, Tom Lolies says, the worst thing is a small amount of brake. Fly hands "
             "up on the B risers of a two-liner or the C steering of a three-liner, and use a lot of brake when you "
             "need it."),
            ("Bryan Van Ostheim", BRYAN, "c4", "On a reflex wing, all or nothing",
             "On reflex parakites, Bryan Van Ostheim says, a wing that shoots forward is best left alone so the "
             "reflex can catch it, or pulled a lot; a small brake input removes the reflex and can fold the whole "
             "wing. In heavy turbulence, though, he would never just do nothing: fly actively, with big inputs."),
        ],
        "related": ["what-happens-if-a-paraglider-collapses", "what-is-a-stall-on-a-paraglider",
                    "what-does-the-speed-bar-do-on-a-paraglider",
                    ("faq", "flight-mechanics", "Is it better to fly on the B risers than on the brakes?"),
                    ("faq", "flight-mechanics", "Why is a small amount of brake a problem on a modern two-liner?"),
                    ("faq", "competitions", "Which matters more for safety, SIV or active flying?")],
    },
    # ------------------------------------------------------------------ 9
    {
        "slug": "what-do-en-a-b-c-and-d-paraglider-ratings-mean",
        "q": "What do EN A, B, C and D paraglider ratings mean?",
        "also": ["What does EN B mean on a paraglider?", "What is the difference between EN A and EN B?",
                 "What is a low B and a high B paraglider?", "What is a CCC paraglider?"],
        "series": "flight-mechanics",
        "topic": "Certification",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": False,
        "seo_title": "EN A, B, C and D Paraglider Ratings Explained",
        "seo_desc": "What the EN 926-2 classes mean, how a paraglider is certified, what a rating cannot tell you, "
                    "and low B, high B, two-liner C and CCC explained, with sources.",
        "short": "They are the four flight-behaviour classes of the European standard EN 926-2. Test pilots fly a "
                 "fixed set of manoeuvres in calm air, including deliberate collapses, and each result is graded A "
                 "to D; the wing takes its most demanding result. EN A is the most forgiving class and EN D the most "
                 "demanding. The letter describes behaviour in those tests, not performance, and not how easily a "
                 "wing collapses in real air.",
        "sources": [("STN EN 926-2+A1:2022 preview (EN 926-2:2013+A1:2021)", "Slovak Office of Standards",
                     "https://normy.normoff.gov.sk/norma/134635/nahlad", "Standard"),
                    ("EVS-EN 926-2:2013+A1:2021", "Estonian Centre for Standardisation",
                     "https://evs.ee/en/evs-en-926-2-2013-a1-2021-consolidated", "Standard"),
                    ("prEN 926-2 rev", "Genorma", "https://genorma.com/en/standards/pren-926-2-rev", "Standard"),
                    ("About us", "Air Turquoise", "https://para-test.com/about", "Test house"),
                    DHV_CLASS,
                    ("prEN 926-2:2012 working draft (CEN/TC 136/WG 6)", "CEN, published by Cross Country Magazine",
                     "https://xcmag.com/wp-content/uploads/2012/08/DraftEN926-2.pdf", "Standard"),
                    DHV_REC,
                    ("Classification sticker PG_2189.2023, Apco Nestra L", "Air Turquoise, hosted by Apco",
                     "https://www.apcoaviation.com/wp-content/uploads/2024/04/PG_2189-2023_ST_NESTRA_L.pdf",
                     "Test house"),
                    ("Flight test certificates, Sky Fides 3", "Air Turquoise, hosted by Sky Paragliders",
                     "https://sky-cz.com/media/cache/file/4f/Fides3_EN-certification.pdf", "Test house"),
                    SHV_EN, DHV_SJ, FB_SAFETY,
                    ("Design insight: the EN-C class (2026)", "Cross Country Magazine",
                     "https://xcmag.com/gear-guide/paraglider-reviews/en-c-paraglider-reviews/design-insight-the-en-c-class/",
                     "Magazine"),
                    UP_TALK, CIVL_CCC],
        "sections": [
            {"kicker": "The standard", "h": "What is EN 926?",
             "short": "The European standard for paragliders. Part 1 tests strength; part 2 classifies flight "
                      "behaviour.",
             "paras": [
                 "EN 926-2 sets out the requirements and test methods for classifying a paraglider's flight safety "
                 "characteristics [1]. The current edition is EN 926-2:2013+A1:2021, listed by national standards bodies as "
                 "valid from 31 December 2021 [2]; its 2021 amendment changed how paragliders are classified [1], and a further revision has "
                 "been out for public comment [3]. The tests are made by independent laboratories such as Air "
                 "Turquoise in Switzerland [1][4]. EN 926-1 is the separate test of structural "
                 "strength [4][2].",
                 "In Germany, wings are classified to the national airworthiness requirements, the LTF, which use "
                 "the same A to D letters [5], and a modern classification sticker lists the EN parts and the "
                 "German rule side by side [8]."],
             "bold": ["EN 926-2", "EN 926-1"]},
            {"kicker": "The classes", "h": "What does each paraglider class mean?",
             "short": "From A, the most forgiving, to D, which demands precise and experienced piloting.",
             "paras": [],
             "table": {"cols": ["Class", "How the wing behaves", "Who it is designed for"],
                       "rows": [["EN A", "The most forgiving class: maximum passive safety and very forgiving "
                                         "flying characteristics.",
                                 "All pilots, including students at any stage of training."],
                                ["EN B", "Good passive safety and forgiving flying characteristics.",
                                 "All pilots; students only if the manufacturer recommends it."],
                                ["EN C", "Moderate passive safety, with potentially dynamic reactions to turbulence "
                                         "and pilot error. Recovery may need precise input.",
                                 "Pilots who know the recovery techniques, fly actively and regularly, and "
                                 "understand what reduced passive safety means."],
                                ["EN D", "Demanding flying characteristics, with potentially violent reactions to "
                                         "turbulence and pilot error. Recovery needs precise input.",
                                 "Pilots well practised in recovery, who fly very actively and have significant "
                                 "experience of turbulent air."]],
                       "caption": "Paraphrased from the 2012 working draft of EN 926-2 and the DHV's LTF class "
                                  "descriptions [6][5]. The final text of the standard is sold, not published."},
             "after": [
                 "The DHV adds rough guidance on airtime for choosing a class: fewer than about 15 to 20 hours a "
                 "year suits A; about 20 to 30 hours suits B, but a high B wants no less than 50; C wants more than "
                 "50 hours a year plus safety training on that class; and D at least about 100 [7]."],
             "callout": {"kicker": "DHV guidance", "heading": "Hours a year, by class",
                         "text": "A rule of thumb from the German federation for choosing a class, not a "
                                 "requirement.",
                         "cite": [7],
                         "numbers": [("15-20", "h", "EN A, or fewer"), ("20-30", "h", "EN B"),
                                     ("50+", "h", "EN C and high B"), ("100+", "h", "EN D")]}},
            {"kicker": "The test", "h": "How is a paraglider certified?",
             "short": "Two test pilots, calm air, around twenty-three manoeuvres. The most demanding grade sets the "
                      "class.",
             "paras": [
                 "According to the 2012 working draft of the standard, the flight test is flown by two pilots, one "
                 "at the minimum declared weight and one at the maximum [6], in calm air with little wind and no turbulence [6]. Collapses are induced deliberately, by "
                 "pulling lines on one side as fast as possible [6]. Each manoeuvre is graded on its own, and the "
                 "wing's overall class is its most demanding single result [6][5]. A recent Air Turquoise sticker "
                 "for an EN B wing shows the pattern: a mix of A and B results across about 23 test items, and B "
                 "overall [8]. Every size is tested and certified separately [9].",
                 "The tests rate flight characteristics only, not performance [5]."],
             "bold": ["most demanding single result"],
             "figure": {"img": "kb-new-technologies-section", "w": 2400, "h": 1000, "cols": 3,
                        "alt": "A paraglider planform marked for the big asymmetric collapse test: a fold line at 45 "
                               "degrees from halfway along the trailing edge, with marker stickers along it",
                        "captions": [("The fold", "The fold line meets the trailing edge at 50 percent, plus or minus "
                                                  "2.5, and runs at 45 degrees towards the open side, taking about "
                                                  "70 to 75 percent of the leading edge."),
                                     ("The markers", "Stickers on the wing show the test pilot where the fold has "
                                                     "to sit."),
                                     ("The lines", "Where the fold cannot be pulled from the risers, extra folding "
                                                   "lines are fitted for the test.")],
                        "source_html": 'After Frantisek Pavlousek, <a href="../../episodes/%s.html#c5">chapter 5</a>. '
                                       'Schematic.' % UPF}},
            {"kicker": "Limits", "h": "What does an EN rating not tell you?",
             "short": "How easily the wing collapses in real air, how it compares within its class, or how it "
                      "performs.",
             "paras": [
                 "Even the working group that writes the standard sees the flight tests as comparisons under "
                 "laboratory conditions rather than a guarantee of safety, according to the Swiss federation, which "
                 "adds that test collapses on modern, heavily reinforced wings are drifting further from reality, "
                 "especially from high B upwards [10]. The DHV's safety officer notes that real collapses are often "
                 "more demanding than induced ones, in every class [11]. And because most modern wings score A on "
                 "the 50 percent asymmetric collapse from trim speed, that single result says little when choosing "
                 "a wing [12].",
                 "The guests on the show agree: treat the letter as a starting point, then read who the "
                 "manufacturer says the wing is for, count the B results on a B report, and test-fly before you "
                 "buy."],
             "bold": ["not a guarantee of safety"]},
            {"kicker": "Inside the letters", "h": "What are low B, high B, two-liner C and CCC?",
             "short": "Labels for the real differences inside and above the four letters.",
             "paras": [
                 "EN B covers a wide range. The Swiss federation splits it into a low B, for all pilots including "
                 "students, and a high B for experienced, regular pilots, stable in calm air but able to surprise "
                 "the pilot after a collapse [10]. The DHV says high-B wings cannot be recommended for pilots who "
                 "fly irregularly [7].",
                 "Since the 2021 amendment, EN C wings may be certified using folding lines, extra lines that let "
                 "the test pilot produce the required collapse on a wing that resists it [10][13]. That opened the "
                 "class to two-liners, and EN C is increasingly made up of them [10][14].",
                 "CCC, the CIVL Competition Class, is the class for wings flown in top-level cross-country "
                 "competitions. It builds on EN rather than replacing it: the wing must meet a 23 G load "
                 "requirement, its flight tests are pass or fail rather than graded, and the speed system may "
                 "shorten the front risers by no more than 140 mm [15]."],
             "bold": ["low B", "high B", "folding lines", "CCC"]},
        ],
        "show": [
            ("Frantisek Pavlousek", UPF, "c3", "Certified safety is not real safety",
             "Certification safety and real safety are related but not the same, says Frantisek Pavlousek, chief "
             "designer at UP. A low B can be as safe in the air as an A, having missed the A on a single "
             "manoeuvre."),
            ("Frantisek Pavlousek", UPF, "c4", "Hands up, no reaction",
             "The certification collapse is pulled hands up, with no brake in hand and no reaction from the pilot, "
             "which he calls already outside reality. It also explains a design trick: the easiest way to turn a C "
             "on the full-speed collapse into a B is a slower trim speed."),
            ("Tom Lolies", TOM, "c5", "Why some Cs feel safer than Bs",
             "Folding lines in EN C let designers use genuinely stable airfoils, Tom Lolies says. EN B wings cannot "
             "use them, so their profiles must still collapse from the A lines, and he has seen EN C wings he "
             "considers safer than some EN Bs."),
            ("Alain Zoller", ALAIN, "c10", "Count the Bs",
             "On a B report, count the B results: that already tells a low B from a high B, says Alain Zoller of "
             "Air Turquoise, and many high Bs come from C designs, trimmed differently. His first rule is not to jump "
             "to the highest class in the hope of flying further, and to test-fly two or three candidates."),
            ("Luc Armant", LUC_D, "c8", "Read who it is for",
             "Do not choose a wing by any single test result, says Luc Armant of Ozone. Read who the manufacturer "
             "says the wing is for."),
        ],
        "related": ["what-happens-if-a-paraglider-collapses", "what-is-aspect-ratio-on-a-paraglider",
                    "what-is-active-flying-in-paragliding",
                    ("faq", "flight-mechanics", "How should I read a paraglider test report before buying?"),
                    ("faq", "flight-mechanics", "Should I move up a glider class?"),
                    ("faq", "new-technologies", "What are folding lines on a paraglider for?"),
                    ("faq", "new-technologies", "Does EN certification tell me how safe a paraglider is?")],
    },
    # ------------------------------------------------------------------ 10
    {
        "slug": "what-is-aspect-ratio-on-a-paraglider",
        "q": "What is aspect ratio on a paraglider?",
        "also": ["What is a good aspect ratio for a paraglider?",
                 "What is the difference between flat and projected aspect ratio?",
                 "Does a higher aspect ratio make a paraglider more dangerous?"],
        "series": "flight-mechanics",
        "topic": "Aspect ratio",
        "status": "draft", "updated": "2026-10-08", "reviewed": None, "safety": False,
        "seo_title": "Paraglider Aspect Ratio Explained, by Class",
        "seo_desc": "Aspect ratio is span squared over area. Why higher glides better, flat versus projected, real "
                    "figures from EN A to competition wings, and the trade-offs.",
        "short": "Aspect ratio describes how long and slender a wing is: its span squared divided by its area. "
                 "Measured flat, paragliders run from about 4.3 for a school wing to about 7.5 for a competition "
                 "wing. A higher aspect ratio cuts induced drag and improves the glide, but makes the wing more "
                 "demanding to launch, to turn and to recover when something goes wrong.",
        "sources": [("Wing Geometry", "NASA Glenn Research Center",
                     "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/wing-geometry", "Government"),
                    FAA_PHAKG, FAA_GFH3, CIVL_CCC, OZ_DELTA4,
                    ("Induced Drag Coefficient", "NASA Glenn Research Center",
                     "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/induced-drag-coefficient", "Government"),
                    ("Atom 3 pilot's manual (EN A)", "Ozone",
                     "https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/07/Atom-3-manual-EN.pdf",
                     "Manufacturer"),
                    GIN_B8, NIV_H6, UP_LHOTSE, OZ_LM7,
                    ("Ozone Zeno 2 (reproduces Ozone's specification table)", "Flybubble",
                     "https://flybubble.com/products/ozone-zeno-2", "Retailer"),
                    ("Ozone Enzo 3 (reproduces Ozone's specification table)", "Flybubble",
                     "https://flybubble.com/products/ozone-enzo-3", "Retailer"),
                    FB_CLASS, UP_TALK, FB_SAFETY, FAI_CCC16],
        "sections": [
            {"kicker": "Definition", "h": "How is aspect ratio measured?",
             "short": "Span squared divided by area. For a simple rectangle, that is just span divided by chord.",
             "paras": [
                 "Aspect ratio is the square of the wingspan divided by the wing area [1]. For a rectangular wing "
                 "that reduces to span divided by chord, and the FAA's version, span divided by average chord, is "
                 "the same thing [1][2][3]. A long, narrow wing has a high aspect ratio; a short, broad one a low "
                 "aspect ratio.",
                 "Most makers publish two figures. Flat aspect ratio is measured with the wing laid out flat, not "
                 "inflated, which is how the competition rules define the span [4]. Projected aspect ratio refers "
                 "to the wing's shape in flight and is always the lower number: Ozone lists its Delta 4 at 6.0 "
                 "flat and 4.4 projected [5]. Brands measure the projected figure in different ways, as one of the "
                 "designers explains below. When you compare wings, make sure both numbers are the same "
                 "kind."],
             "bold": ["Flat aspect ratio", "Projected aspect ratio"]},
            {"kicker": "Why it matters", "h": "Why does a higher aspect ratio glide better?",
             "short": "Less induced drag. The wingtips waste less energy in making the lift.",
             "paras": [
                 "A wing that makes lift sheds a pair of swirling vortices from its tips, and the drag that comes "
                 "with them is induced drag [6]. For the same area, a wing with a higher aspect ratio has less "
                 "induced drag [6], which means a better lift-to-drag ratio and a flatter glide; it is why "
                 "sailplanes have such long, slender wings [1][3].",
                 "Induced drag grows as airspeed falls [2], which is one reason aspect ratio matters so much on an "
                 "aircraft as slow as a paraglider."],
             "bold": ["induced drag"]},
            {"kicker": "Real numbers", "h": "What aspect ratio do paragliders have?",
             "short": "About 4.3 to 4.8 for school wings, 5.3 to 5.7 for EN B, around 6 for EN C, 6.5 to 7 for EN D "
                      "and over 7.5 for competition.",
             "paras": [],
             "table": {"cols": ["Wing", "Class", "Flat", "Projected"],
                       "rows": [["Ozone Atom 3", "EN A", "4.26", "3.04"],
                                ["Gin Bolero 8", "EN A", "4.8", "3.55"],
                                ["Niviuk Hook 6", "EN B", "5.3", "not listed"],
                                ["UP Lhotse", "EN B", "5.7", "4.1"],
                                ["Ozone Delta 4", "EN C", "6.0", "4.4"],
                                ["Ozone LM7", "EN D, two-liner", "6.5", "4.7"],
                                ["Ozone Zeno 2", "EN D", "6.9", "5.1"],
                                ["Ozone Enzo 3", "CCC, two-liner", "7.55", "5.5"]],
                       "caption": "From the manufacturers' manuals and specification tables [7][8][9][10][5][11]; the "
                                  "Zeno 2 and Enzo 3 figures come from a retailer's copy of Ozone's table [12][13]. "
                                  "Aspect ratio is the same for every size of a model. Some of these are earlier "
                                  "models: the pattern by class is the point."},
             "figure": {"img": "kb-enc-aspect", "w": 2400, "h": 620, "cols": 4,
                        "alt": "Four paraglider planforms of the same area drawn to scale, from a short, broad EN A "
                               "wing to a long, slender competition wing",
                        "captions": [("EN A", "Flat aspect ratio about 4.3. Short and broad."),
                                     ("EN B", "About 5.3."),
                                     ("EN C", "About 6.0."),
                                     ("CCC", "About 7.55. The same area, stretched long and slender.")],
                        "source_html": "Planforms of equal area drawn from the flat aspect ratios in the table. "
                                       "Shapes are schematic; spans are to scale."}},
            {"kicker": "Trade-offs", "h": "Does a higher aspect ratio make a paraglider more dangerous?",
             "short": "More demanding, rather than simply more fragile. The window for recovery shrinks.",
             "paras": [
                 "Wings with a very high aspect ratio and high wing loading are usually harder to launch, their "
                 "narrow tips bring a real risk of cravats in a collapse, and they turn on a wider arc [14]. As the "
                 "class rises, the window for a safe recovery gets much smaller [14]. Performance wings also pair "
                 "higher aspect ratios with less line [14].",
                 "It is not as simple as more aspect ratio, more collapses. UP's designers say the two-liner concept "
                 "is generally more resistant to collapse, though livelier in bumps [15], and wings built to resist "
                 "collapse can recover more violently when they do finally fold [16]. The fair summary is that a "
                 "high aspect ratio wing asks more of the pilot when something goes wrong."],
             "bold": ["window for a safe recovery"]},
            {"kicker": "Limits", "h": "Is there a limit on paraglider aspect ratio?",
             "short": "Competition rules set one in 2016, and designers still argue about where the limits should "
                      "sit.",
             "paras": [
                 "When the FAI updated its Competition Class in 2016, it capped flat aspect ratio at 7.90, the "
                 "highest of any EN-certified glider by the end of 2013 [17]. The 2024 version of the requirements "
                 "does not appear to repeat that cap [4], so check the current rules before relying on it. For the "
                 "EN classes, one of the designers in the working group describes the debate below."],
             "bold": ["7.90"]},
        ],
        "show": [
            ("Tom Lolies", TOM, "c9", "Projected has no fixed definition",
             "Projected aspect ratio has no objective definition, Tom Lolies points out, because the wing changes "
             "shape between full speed, trim and brakes, and brands measure it in different ways."),
            ("Tom Lolies", TOM, "c9", "Cells instead of a ceiling",
             "In working-group talks about reining in the top of EN C, a flat aspect ratio ceiling of about 6.7 was "
             "discussed. Tom and other designers preferred a limit of 66 cells instead, which he says puts the "
             "best aspect ratio at around 6.3 to 6.5 while leaving designers free to trade span against arc."),
            ("Tom Lolies", TOM, "c8", "Correlated with safety",
             "Aspect ratio and safety are correlated, Tom says, but the projected aspect ratio matters too."),
        ],
        "related": ["what-is-the-glide-ratio-of-a-paraglider", "what-do-en-a-b-c-and-d-paraglider-ratings-mean",
                    "what-happens-if-a-paraglider-collapses", "how-does-a-paraglider-fly",
                    ("faq", "flight-mechanics", "Should I move up a glider class?"),
                    ("faq", "new-technologies", "Why do modern paragliders need fewer lines?")],
    },
]
