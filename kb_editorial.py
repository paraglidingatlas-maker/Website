"""Editorial for knowledge base category pages.

WHY THIS EXISTS
A category page used to be a breadcrumb, one sentence, four topic chips and a
grid of episode tiles: about 250 words, most of it navigation. Nothing on the
page answered a question, so nothing on it could rank or be cited, while the
answers sat one level down in 90,000 words of transcript. This file holds, per
category, the text that turns the hub into an article: what the conversations
add up to, the takeaways worth remembering, and the questions they answer.

RULES FOR WRITING ONE
- Every claim traces to a named guest and a chapter. Link it: ("slug", "cN").
  The chapter ids are the <div class="cd-block" id="cN"> anchors on the
  episode page. If you cannot point at the chapter, leave the claim out.
- Paraphrase; do not quote the transcript. Automatic captions are not reliable
  enough to quote, and a paraphrase reads better anyway.
- Answers are 40 to 80 words. A question must end with a question mark and be
  followed by prose, or tools/inject_site_schema.py will not mark it up as an
  FAQPage entry (the question mark is the gate).
- No em-dashes, per the site copy rule.
- Keep the series name as the kicker; the H1 is the query a pilot would type.
"""

EDITORIAL = {
    "flight-mechanics": {
        "kicker": "Flight Mechanics",
        "h1": "How a Paraglider Actually Flies",
        "seo_title": "Paragliding Flight Mechanics: Stability & Control | Paragliding Atlas",
        "seo_desc": "Why a paraglider with no tail stays stable, what makes it collapse, what an EN letter really tells you, and how to read the air. Eight designers and test pilots.",
        "intro": "Stability, collapses, certification and control, explained by the people who design, test and teach it.",
        "sections": [
            {
                "heading": "What these eight conversations add up to",
                "paras": [
                    "A paraglider has no tail, so every bit of its pitch stability comes from the shape of the profile. Luc Armant of Ozone explains it through the moment coefficient: on a stable profile, as the angle of attack drops the lift resultant moves forward and resists the pitch-down, while a profile with a lower moment coefficient carries its lift further back, gives more speed for a given amount of speed-bar travel, and gives up resistance to collapse in exchange. Tom Lolies, designing for Skywalk, describes the same physics from the bench as pitch-up tendency: the newer airfoils that, when the lines go slack in a gust, want to pitch against the collapse rather than with it, so the pilot feels the tension drop and has time to react instead of getting the whole thing at once.",
                    "That is why a certification report is a narrower document than most buyers assume. Alain Zoller, who runs the Air Turquoise test house and sits on the Work Group 6 that writes the standard, says a class does not make one wing better than another, only better matched to a pilot, and that the collapses induced in testing are not representative of what turbulence does. Tom Lolies goes further: the standard has around twenty tests for how a wing behaves once it has collapsed and effectively none for how hard it is to collapse, so a page of A results can mean a beautifully behaved wing, or one that folds so easily that nothing dramatic ever happens. Luc Armant's buying advice is the same from Ozone's side: ignore any single letter and read who the manufacturer says the wing is for.",
                    "On the control side, Tom Lolies and the SIV coach Helmut Schrempf arrive at the same warning about the modern, more stable profiles: a small amount of brake is the worst input you can give them, because it deflects the trailing edge enough to kill the pitch-up tendency without adding enough drag to slow the wing. Fly hands-up on the B risers or the C steering, or use a lot of brake when you need it, but not a little. Bryan Van Ostheim describes the extreme version on a reflex parakite, where a light brake input during a surge removes the reflex and the whole wing can fold. Helmut's coaching method starts with the pilot's body before any manoeuvre: tension in the harness, and releasing that tension into a dropping side rather than pressing into it.",
                    "Brett Janaway covers the air itself. Thermals need contrast and triggers more than heat, which is why Slovenia works in December and a desert often does not; the strongest air sits at the upwind front of the bubble because it rises more vertically for the same drift; and with no other information you turn into wind. Aljaž Valič of 777 and Luc Armant close the loop on why wings look the way they do: internal structure and laser-cut ribs, the aspect-ratio and cell-count arguments inside the C class, and competition rules that push racing profiles to the edge of stability.",
                ],
            },
        ],
        "takeaways_heading": "Nine things worth remembering",
        "takeaways": [
            {"text": "Pitch stability comes only from the profile. The moment coefficient decides where the lift sits and how much speed the bar can deliver, and a rule that caps speed-bar travel at 14 cm pushes any wing built to win towards the unstable end.",
             "ep": "luc-armant-talks-about-the-moment-coefficient-enzo-3", "ch": "c2", "who": "Luc Armant"},
            {"text": "Check your brake length before anything else. From hands-up to first tension there should be at least 7 cm, and at full bar there should be no tension in the brakes at all. Dyneema brake lines shrink, pilots adapt without noticing, and shortened brakes are a cofactor in accidents.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c12", "who": "Tom Lolies"},
            {"text": "One green flag for a collapse-resistant airfoil: at full speed the B lines go light or slack, because the centre of lift has moved forward onto the A lines. Not a rule, but one signal among several.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c6", "who": "Tom Lolies"},
            {"text": "Counting A results on a test report is not a safety grade. The report shows how collapses went, never how easy they were to provoke, and a pitch-unstable wing can score well precisely because it collapses so readily.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c7", "who": "Tom Lolies"},
            {"text": "Stalling from the B risers comes sooner and with less warning than from the brakes. If turbulence means you need to slow down a lot, let go of the Bs, use a deep brake input, and go back to the Bs as soon as you can.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c13", "who": "Tom Lolies"},
            {"text": "When a side drops, release the tension in your body on that side and let the wing take what it needs. Pressing in actively usually gives it the wrong amount, which is where the rolling and pitching on speed bar comes from.",
             "ep": "helmut-schrempf-modernizing-siv-courses-how-this-new", "ch": "c4", "who": "Helmut Schrempf"},
            {"text": "A wing drifts out of trim with use and generally gets a little slower; spiralling always the same way shrinks one side differently. Get it checked and trimmed, and keep the logbook, because a missed check can also void the warranty.",
             "ep": "alain-zoller-the-science-of-en-certifications-how-work", "ch": "c9", "who": "Alain Zoller"},
            {"text": "With no other information, turn into wind when you hit lift. Get it wrong at the front and you fall back into the core; get it wrong at the back and you are sinking and flying upwind to a core that is now further away.",
             "ep": "how-to-thermal-like-a-pro-find-center-climb-paragliding", "ch": "c7", "who": "Brett Janaway"},
            {"text": "Stepping down a class is not a failure and stepping up is not a required step. Match the wing to what you want from flying and how current you are, and decouple the choice from ego.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c10", "who": "Tom Lolies"},
        ],
        "faq_heading": "Questions these conversations answer",
        "faq": [
            {"q": "Why is a paraglider stable in pitch when it has no tail?",
             "a": "Because the stability is built into the profile. Luc Armant explains that a profile has a moment coefficient: on a stable one, as the angle of attack falls the lift resultant moves forward, which pulls the nose back up. A profile with a low moment coefficient carries its lift further back and is easier to accelerate, but resists collapse less.",
             "ep": "luc-armant-talks-about-the-moment-coefficient-enzo-3", "ch": "c2", "who": "Luc Armant"},
            {"q": "What is pitch-up tendency in a paraglider?",
             "a": "Tom Lolies describes it as an airfoil that, when the angle of attack drops, moves its centre of lift towards or beyond the nose, so the wing wants to pitch against a collapse rather than with it. The pilot feels a loss of tension before anything folds and has time to react. Older profiles tended the other way and collapsed completely and quickly.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c5", "who": "Tom Lolies"},
            {"q": "Does EN certification tell me how likely a wing is to collapse?",
             "a": "No. Alain Zoller, who runs a test house, says the induced collapses are not representative of what the air does. Tom Lolies adds that the standard has roughly twenty tests for behaviour after a collapse and no accepted test for collapse resistance; the only one, brake application at full speed, is itself debated.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c6", "who": "Tom Lolies and Alain Zoller"},
            {"q": "How should I read a paraglider test report before buying?",
             "a": "Do not use it to rank wings. Luc Armant says to ignore any single result and read who the manufacturer says the wing is for. Alain Zoller adds that the brake range is worth a look, because a clean report with a very short range means little margin before the stall, and that nothing replaces test-flying two or three candidates yourself.",
             "ep": "luc-armant-talks-about-debunking-the-myths-and-upgrading", "ch": "c8", "who": "Luc Armant and Alain Zoller"},
            {"q": "Why is a small amount of brake a problem on a modern two-liner?",
             "a": "Tom Lolies explains that a slight brake deflection is enough to cancel the profile's pitch-up tendency, and so its collapse resistance, without creating enough drag to slow the wing. On some high-level wings, touching the brakes at full speed makes them faster, not slower. Fly on the B risers, or use plenty of brake, but avoid the small amount in between.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c12", "who": "Tom Lolies"},
            {"q": "Is it better to fly on the B risers than on the brakes?",
             "a": "In ordinary air, both Helmut Schrempf and Tom Lolies fly on the B risers to keep the profile intact and the wing efficient. But the B risers are not brakes: Helmut says to switch to the brakes when a collapse happens, and the pendulum gives you time to do it. On three-liners, C steering needs the B-C bridge the manufacturer specifies.",
             "ep": "helmut-schrempf-modernizing-siv-courses-how-this-new", "ch": "c5", "who": "Helmut Schrempf"},
            {"q": "How do I check my brake line length?",
             "a": "Tom Lolies gives two checks. From hands fully up to the first feeling of tension there should be at least 7 cm of travel, and at full speed bar there should be no tension in the brakes. Brake lines made of Dyneema shrink over time, so this is worth checking regularly rather than once.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c12", "who": "Tom Lolies"},
            {"q": "Which way should I turn when I hit a thermal?",
             "a": "Into wind, unless you have better information. Brett Janaway explains that the core sits on the upwind side, so turning into wind either finds it or, if you have overshot the front, drops you back into it. Turning downwind at the back leaves you sinking and flying upwind to reach a core that is now above and ahead of you.",
             "ep": "how-to-thermal-like-a-pro-find-center-climb-paragliding", "ch": "c7", "who": "Brett Janaway"},
            {"q": "Why do two Enzo 3s from the same batch feel different?",
             "a": "Because the wing is built at the edge of pitch stability to stay competitive under the 14 cm speed-bar limit. Luc Armant says the cloth shrinks and the rods tighten with use, and a difference of about 5 mm on a rod over two metres long is enough to move one wing from fast towards collapsing. Everyday EN wings carry far more margin.",
             "ep": "luc-armant-talks-about-the-moment-coefficient-enzo-3", "ch": "c4", "who": "Luc Armant"},
            {"q": "Should I move up a glider class?",
             "a": "Only if there is nothing left to learn on the one you fly. Tom Lolies, who can fly any wing he likes, still steps back to a low B after a break to rebuild currency, and says stepping down should carry no stigma. Alain Zoller's version: know your glider at 100 percent before you change it, and avoid the highest class you think you can handle.",
             "ep": "tom-lolies-explains-the-science-of-wing-design-and", "ch": "c10", "who": "Tom Lolies and Alain Zoller"},
        ],
    },
}
