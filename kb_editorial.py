"""Editorial for knowledge base category pages.

WHY THIS EXISTS
A category page used to be a breadcrumb, one sentence, four topic chips and a
grid of episode tiles: about 250 words, most of it navigation. Nothing on the
page answered a question, so nothing on it could rank or be cited, while the
answers sat one level down in 90,000 words of transcript. This file holds, per
category, everything the page says. kb_layout.py turns an entry into the page.

RULES FOR WRITING ONE
- Every claim traces to a named guest and a chapter: ("slug", "cN"), the
  <div class="cd-block" id="cN"> anchors on the episode page. The build fails
  on a chapter that does not exist. If you cannot point at the chapter, leave
  the claim out.
- Paraphrase; never quote the transcript. Automatic captions are not reliable
  enough to quote, and a paraphrase reads better.
- FAQ questions end with a question mark and get a 40 to 80 word answer; that
  is what tools/inject_site_schema.py marks up as FAQPage.
- No em-dashes, per the site copy rule.
- The series name is the kicker; the H1 is the question a pilot would type.
  The URL never changes.

SHAPE (see the Flight Mechanics entry)
  layout=2 selects kb_layout. Images live in assets/images/ as
  kb-<slug>.jpg (hero, 2400x900), kb-<slug>-section.jpg (quote band, 2400x1000)
  and any figures the bands reference; each with a .webp beside it. The
  drawings are made by tools/make_kb_*.py.
"""

WILL = "consequence-over-probability-will-gadd-on-why-true-safety"
SUBIR = "risk-vs-reward-2-subir-sidhu"
MANFRED = "risk-vs-reward-3-manfred-ruhmer"
RAUL = "risk-vs-reward-4-raul-rodriguez"
GABRIEL = "risk-vs-reward-5-gabriel-orsini"
PHILIPP = "risk-vs-reward-1-philipp-zellner"
KINGA = "kinga-masztalerz-building-a-healthy-relationship-with-the"
RUSSELL = "the-russell-ogden-interview-decoding-paragliding-mastery"
META = "metacognition-paragliding-s-hidden-psychology-with-beni"
DK = "cognitive-bias-of-dunning-kruger-effect-in-paragliding"
MATT = "paragliding-physiology-safety-protocols-dr-matt-wilkes"
ALT = "if-you-fly-in-the-himalayas-alps-or-above-3000-mtrs-this"
BH = "Beni Kalin and Heli Schrempf"

URS = "urs-haari-the-real-truth-about-reserve-parachutes-a"
URS2 = "snippet-a-reserve-parachute-trick-every-pilot-should-know"
ZSOLT = "watch-this-before-you-buy-a-paragliding-harness-a-talk"
CIECH = "helmet-safety-christian-ciech-icaro-2000"
BRETT2 = "technical-masterclass-by-brett-janaway-science-of"
CARAB = "carabiner-fatigue-finsterwalder-charly"

BENI = "new-technologies-1-beni-kalin"
NIVIUK = "new-technologies-2-guillem-batlle-adria-grau"
STIEG = "new-technologies-3-stephan-stiegler"
VESELIN = "new-technologies-4-veselin-ovcharov"
UPF = "new-technologies-5-frantisek-pavlousek"
SKYMATE = "understanding-skymate-paragliding-worlds-first-ai-driven"
NESLER = "why-paraglidings-safety-future-looks-different-rast"

BELC = "bill-belcourt-the-uncomfortable-truth-no-one-is-talking"
GAGGLE = "insights-from-the-gaggle-with-tilen-ceglar-stan"
NICK = "survived-15-years-of-flying-then-a-rescue-helicopter"
GOV = "the-unfiltered-truth-about-paragliding-governance-with"
JULIEN = "what-is-civlresign-with-julien-garcia"

EDITORIAL = {
    "flight-mechanics": {'layout': 2,
     'kicker': 'Flight Mechanics',
     'h1': 'How a Paraglider Actually Flies',
     'lead': 'Stability, collapses, certification and control, explained by the people who design, test and '
             'teach it.',
     'sub': 'Eight conversations. Why a wing with no tail stays stable, what really makes it collapse, what an '
            'EN letter can and cannot tell you, and how to read the air you climb in.',
     'seo_title': 'Paragliding Flight Mechanics: Stability & Control | Paragliding Atlas',
     'seo_desc': 'Why a paraglider with no tail stays stable, what makes it collapse, what an EN letter really '
                 'tells you, and how to read the air. Eight designers and test pilots.',
     'hero_alt': 'Three-view technical drawing of a paraglider: side view with airfoil, lines and pilot, front '
                 'view of the canopy arc, and top view of the planform, with reference frames',
     'bands': [{'num': '01',
                'kicker': 'Stability',
                'heading': 'Stability comes from the profile, not from you',
                'short': 'A paraglider has no tail. Everything that keeps it stable in pitch is built into the '
                         'profile shape, and every design choice trades that stability against speed.',
                'paras': ['A paraglider has no tail, so every bit of its pitch stability comes from the shape of '
                          'the profile. Luc Armant of Ozone explains it through the moment coefficient: on a '
                          'stable profile, as the angle of attack drops the lift resultant moves forward and '
                          'resists the pitch-down, while a profile with a lower moment coefficient carries its '
                          'lift further back, gives more speed for a given amount of speed-bar travel, and gives '
                          'up resistance to collapse in exchange.',
                          'Tom Lolies, designing for Skywalk, describes the same physics from the bench as '
                          'pitch-up tendency: the newer airfoils that, when the lines go slack in a gust, want '
                          'to pitch against the collapse rather than with it, so the pilot feels the tension '
                          'drop and has time to react instead of getting the whole thing at once.'],
                'bold': ['moment coefficient', 'pitch-up tendency'],
                'chips': [('Luc Armant', 'luc-armant-talks-about-the-moment-coefficient-enzo-3'),
                          ('Tom Lolies', 'tom-lolies-explains-the-science-of-wing-design-and')],
                'figure': None},
               {'num': '02',
                'kicker': 'Certification',
                'heading': 'What a test report cannot tell you',
                'short': 'A test report shows how a wing behaves after it collapses. It cannot tell you how hard '
                         'the wing is to collapse, which is the thing you actually care about.',
                'paras': ['That is why a certification report is a narrower document than most buyers assume. '
                          'Alain Zoller, who runs the Air Turquoise test house and sits on the Work Group 6 that '
                          'writes the standard, says a class does not make one wing better than another, only '
                          'better matched to a pilot, and that the collapses induced in testing are not '
                          'representative of what turbulence does.',
                          'Tom Lolies goes further: the standard has around twenty tests for how a wing behaves '
                          'once it has collapsed and effectively none for how hard it is to collapse, so a page '
                          'of A results can mean a beautifully behaved wing, or one that folds so easily that '
                          "nothing dramatic ever happens. Luc Armant's buying advice is the same from Ozone's "
                          'side: ignore any single letter and read who the manufacturer says the wing is for.'],
                'bold': ['not representative of what turbulence does', 'twenty tests'],
                'chips': [('Alain Zoller', 'alain-zoller-the-science-of-en-certifications-how-work'),
                          ('Tom Lolies', 'tom-lolies-explains-the-science-of-wing-design-and'),
                          ('Luc Armant', 'luc-armant-talks-about-debunking-the-myths-and-upgrading')],
                'figure': None},
               {'num': '03',
                'kicker': 'Control',
                'heading': 'The small-brake problem',
                'short': 'On a modern, stable profile a little brake is worse than none: it cancels the '
                         'stability without adding the drag. Fly on the Bs, or use plenty of brake.',
                'paras': ['On the control side, Tom Lolies and the SIV coach Helmut Schrempf arrive at the same '
                          'warning about the modern, more stable profiles: a small amount of brake is the worst '
                          'input you can give them, because it deflects the trailing edge enough to kill the '
                          'pitch-up tendency without adding enough drag to slow the wing. Fly hands-up on the B '
                          'risers or the C steering, or use a lot of brake when you need it, but not a little.',
                          'Bryan Van Ostheim describes the extreme version on a reflex parakite: a light brake '
                          'input during a surge removes the reflex, and the whole wing can fold. His advice is '
                          'to do nothing and let the reflex work, or pull a lot, never a little.'],
                'bold': ['a small amount of brake is the worst input', 'removes the reflex'],
                'chips': [('Tom Lolies', 'tom-lolies-explains-the-science-of-wing-design-and'),
                          ('Helmut Schrempf', 'helmut-schrempf-modernizing-siv-courses-how-this-new'),
                          ('Bryan Van Ostheim', 'demystifying-the-science-behind-parakites-bryan-van-ostheim')],
                'figure': {'img': 'kb-flight-mechanics-brakes',
                           'alt': 'The same profile three times: hands up, a little brake, a lot of brake, '
                                  'showing where the lift acts and how much drag there is',
                           'w': 2400,
                           'h': 640,
                           'captions': [('Hands up',
                                         'Lift sits forward, near the nose. In a gust the profile pitches back '
                                         'up, against the collapse.'),
                                        ('A little brake',
                                         'The trailing edge barely moves, but the lift slides back and the '
                                         'pitch-up tendency is gone. Hardly any extra drag, so the wing stays '
                                         'fast.'),
                                        ('A lot of brake',
                                         'High lift and high drag. The wing slows right down and a collapse '
                                         'becomes much less likely.')],
                           'source_html': 'After Tom Lolies, <a '
                                          'href="../episodes/tom-lolies-explains-the-science-of-wing-design-and.html#c12">Episode '
                                          '66, chapter 12</a>, and Helmut Schrempf, <a '
                                          'href="../episodes/helmut-schrempf-modernizing-siv-courses-how-this-new.html#c4">Episode '
                                          '32</a>. Orange: where the lift acts. Grey: drag.',
                           'cols': 3}},
               {'num': '04',
                'kicker': 'The air',
                'heading': 'Reading the air',
                'short': 'Thermals need contrast and triggers, not heat, and the strongest air sits at the '
                         'upwind front of the bubble. With no other information, turn into wind.',
                'paras': ['Brett Janaway covers the air itself. Thermals need contrast and triggers more than '
                          'heat, which is why Slovenia works in December and a desert often does not. The '
                          'strongest air sits at the upwind front of the bubble, because the hottest air rises '
                          'most steeply for the same drift, so you keep pushing into wind or slide out of the '
                          'back.',
                          'With no other information, turn into wind when you hit lift. The one exception he '
                          'gives is an inversion: there the thermal is usually downwind of you, rising slowly '
                          'through the lid, not upwind.'],
                'bold': ['contrast and triggers', 'upwind front', 'downwind of you'],
                'chips': [('Brett Janaway', 'how-to-thermal-like-a-pro-find-center-climb-paragliding')],
                'figure': {'img': 'kb-flight-mechanics-thermal',
                           'alt': 'A thermal from above and from the side: the core sits upwind, turning into '
                                  'wind finds it and turning downwind falls out of the back',
                           'w': 2400,
                           'h': 760,
                           'captions': [('From above',
                                         'The core sits on the upwind side. Turning into wind (orange) finds it; '
                                         'turning downwind (grey) drifts you out of the back.'),
                                        ('From the side',
                                         'The column leans with the wind and the strongest air rises at its '
                                         'upwind front. Fall out of the back and the core is now above and ahead '
                                         'of you.')],
                           'source_html': 'After Brett Janaway, <a '
                                          'href="../episodes/how-to-thermal-like-a-pro-find-center-climb-paragliding.html#c5">Episode '
                                          '80, chapters 5</a> and <a '
                                          'href="../episodes/how-to-thermal-like-a-pro-find-center-climb-paragliding.html#c7">7</a>. '
                                          'Wind blows left to right.',
                           'cols': 2}}],
     'quote_band': {'after_band': 1,
                    'img': 'kb-flight-mechanics-section',
                    'alt': 'Cutaway of a paraglider wing at a rib, with cross-ports, and airflow over the upper '
                           'and lower surface',
                    'kicker': 'Pitch-up tendency',
                    'quote': 'When a gust drops the angle of attack, a modern profile moves its lift forward '
                             'onto the A lines and pitches back against the collapse. You feel the tension go '
                             'before anything folds.',
                    'who': 'Tom Lolies, designer at Skywalk',
                    'cite_ep': 'tom-lolies-explains-the-science-of-wing-design-and',
                    'cite_ch': 'c5',
                    'cite_label': 'Episode 66, paraphrased',
                    'caption': 'Potential-flow sketch: faster, lower-pressure air over the top in orange; slower '
                               'air underneath in grey.'},
     'callout': {'kicker': 'Before your next flight',
                 'heading': 'Check your brake length',
                 'text': 'Dyneema brake lines shrink, pilots adapt without noticing, and brakes that end up too '
                         'short are a cofactor in accidents. Measure them regularly, and have the wing checked '
                         'if you have any doubt.',
                 'ep': 'tom-lolies-explains-the-science-of-wing-design-and',
                 'ch': 'c12',
                 'who': 'Tom Lolies',
                 'numbers': [('7', 'cm', 'at least, from hands fully up to the first tension'),
                             ('0', '', 'tension in the brakes at full speed bar')]},
     'takeaways_heading': 'Worth remembering',
     'groups': [('The wing',
                 [('The profile does the stabilising',
                   'A paraglider has no tail. The moment coefficient sets where the lift sits, and a 14 cm '
                   'speed-bar cap pushes race wings toward instability.',
                   'luc-armant-talks-about-the-moment-coefficient-enzo-3',
                   'c2',
                   'Luc Armant'),
                  ('Slack B lines at full speed',
                   'The lift has moved forward onto the A lines, a sign of a collapse-resistant airfoil. One '
                   'green flag among several, not a rule.',
                   'tom-lolies-explains-the-science-of-wing-design-and',
                   'c6',
                   'Tom Lolies'),
                  ('A results are not a safety score',
                   'Reports show how collapses went, never how easily they happen. A pitch-unstable wing can '
                   'score well because it folds so readily.',
                   'tom-lolies-explains-the-science-of-wing-design-and',
                   'c7',
                   'Tom Lolies')]),
                ('Your inputs',
                 [('The B risers stall sooner',
                   'With less pressure and less warning than the brakes. To slow down hard in turbulence, go to '
                   'deep brake, then back to the Bs.',
                   'tom-lolies-explains-the-science-of-wing-design-and',
                   'c13',
                   'Tom Lolies'),
                  ('Release into the drop',
                   'When a side drops, let the tension out of your hip on that side. Pressing in gives the wing '
                   'the wrong amount and starts the rolling.',
                   'helmut-schrempf-modernizing-siv-courses-how-this-new',
                   'c4',
                   'Helmut Schrempf'),
                  ('Turn into wind',
                   'The core sits upwind. Wrong at the front and you fall back into it; wrong at the back and '
                   'you are sinking and chasing it.',
                   'how-to-thermal-like-a-pro-find-center-climb-paragliding',
                   'c7',
                   'Brett Janaway')]),
                ('Your choices',
                 [('Wings drift out of trim',
                   'Usually slower, and unevenly if you always spiral one way. Regular checks keep it safe, and '
                   'a missed one can void the warranty.',
                   'alain-zoller-the-science-of-en-certifications-how-work',
                   'c9',
                   'Alain Zoller'),
                  ('Stepping down is fine',
                   'Match the wing to how much and how often you fly. Even a Skywalk designer goes back to a low '
                   'B after a break.',
                   'tom-lolies-explains-the-science-of-wing-design-and',
                   'c10',
                   'Tom Lolies')])],
     'faq_heading': 'Questions these conversations answer',
     'faq': [{'q': 'Why is a paraglider stable in pitch when it has no tail?',
              'a': 'Because the stability is built into the profile. Luc Armant explains that a profile has a '
                   'moment coefficient: on a stable one, as the angle of attack falls the lift resultant moves '
                   'forward, which pulls the nose back up. A profile with a low moment coefficient carries its '
                   'lift further back and is easier to accelerate, but resists collapse less.',
              'ep': 'luc-armant-talks-about-the-moment-coefficient-enzo-3',
              'ch': 'c2',
              'who': 'Luc Armant'},
             {'q': 'What is pitch-up tendency in a paraglider?',
              'a': 'Tom Lolies describes it as an airfoil that, when the angle of attack drops, moves its centre '
                   'of lift towards or beyond the nose, so the wing wants to pitch against a collapse rather '
                   'than with it. The pilot feels a loss of tension before anything folds and has time to react. '
                   'Older profiles tended the other way and collapsed completely and quickly.',
              'ep': 'tom-lolies-explains-the-science-of-wing-design-and',
              'ch': 'c5',
              'who': 'Tom Lolies'},
             {'q': 'Does EN certification tell me how likely a wing is to collapse?',
              'a': 'No. Alain Zoller, who runs a test house, says the induced collapses are not representative '
                   'of what the air does. Tom Lolies adds that the standard has roughly twenty tests for '
                   'behaviour after a collapse and no accepted test for collapse resistance; the only one, brake '
                   'application at full speed, is itself debated.',
              'ep': 'tom-lolies-explains-the-science-of-wing-design-and',
              'ch': 'c6',
              'who': 'Tom Lolies and Alain Zoller'},
             {'q': 'How should I read a paraglider test report before buying?',
              'a': 'Do not use it to rank wings. Luc Armant says to ignore any single result and read who the '
                   'manufacturer says the wing is for. Alain Zoller adds that the brake range is worth a look, '
                   'because a clean report with a very short range means little margin before the stall, and '
                   'that nothing replaces test-flying two or three candidates yourself.',
              'ep': 'luc-armant-talks-about-debunking-the-myths-and-upgrading',
              'ch': 'c8',
              'who': 'Luc Armant and Alain Zoller'},
             {'q': 'Why is a small amount of brake a problem on a modern two-liner?',
              'a': "Tom Lolies explains that a slight brake deflection is enough to cancel the profile's "
                   'pitch-up tendency, and so its collapse resistance, without creating enough drag to slow the '
                   'wing. On some high-level wings, touching the brakes at full speed makes them faster, not '
                   'slower. Fly on the B risers, or use plenty of brake, but avoid the small amount in between.',
              'ep': 'tom-lolies-explains-the-science-of-wing-design-and',
              'ch': 'c12',
              'who': 'Tom Lolies'},
             {'q': 'Is it better to fly on the B risers than on the brakes?',
              'a': 'In ordinary air, both Helmut Schrempf and Tom Lolies fly on the B risers to keep the profile '
                   'intact and the wing efficient. But the B risers are not brakes: Helmut says to switch to the '
                   'brakes when a collapse happens, and the pendulum gives you time to do it. On three-liners, C '
                   'steering needs the B-C bridge the manufacturer specifies.',
              'ep': 'helmut-schrempf-modernizing-siv-courses-how-this-new',
              'ch': 'c5',
              'who': 'Helmut Schrempf'},
             {'q': 'How do I check my brake line length?',
              'a': 'Tom Lolies gives two checks. From hands fully up to the first feeling of tension there '
                   'should be at least 7 cm of travel, and at full speed bar there should be no tension in the '
                   'brakes. Brake lines made of Dyneema shrink over time, so this is worth checking regularly '
                   'rather than once.',
              'ep': 'tom-lolies-explains-the-science-of-wing-design-and',
              'ch': 'c12',
              'who': 'Tom Lolies'},
             {'q': 'Which way should I turn when I hit a thermal?',
              'a': 'Into wind, unless you have better information. Brett Janaway explains that the core sits on '
                   'the upwind side, so turning into wind either finds it or, if you have overshot the front, '
                   'drops you back into it. Turning downwind at the back leaves you sinking and flying upwind to '
                   'reach a core that is now above and ahead of you.',
              'ep': 'how-to-thermal-like-a-pro-find-center-climb-paragliding',
              'ch': 'c7',
              'who': 'Brett Janaway'},
             {'q': 'Why do two Enzo 3s from the same batch feel different?',
              'a': 'Because the wing is built at the edge of pitch stability to stay competitive under the 14 cm '
                   'speed-bar limit. Luc Armant says the cloth shrinks and the rods tighten with use, and a '
                   'difference of about 5 mm on a rod over two metres long is enough to move one wing from fast '
                   'towards collapsing. Everyday EN wings carry far more margin.',
              'ep': 'luc-armant-talks-about-the-moment-coefficient-enzo-3',
              'ch': 'c4',
              'who': 'Luc Armant'},
             {'q': 'Should I move up a glider class?',
              'a': 'Only if there is nothing left to learn on the one you fly. Tom Lolies, who can fly any wing '
                   'he likes, still steps back to a low B after a break to rebuild currency, and says stepping '
                   "down should carry no stigma. Alain Zoller's version: know your glider at 100 percent before "
                   'you change it, and avoid the highest class you think you can handle.',
              'ep': 'tom-lolies-explains-the-science-of-wing-design-and',
              'ch': 'c10',
              'who': 'Tom Lolies and Alain Zoller'}],
     'next': {'main': ('risk-vs-reward.html',
                       'Risk vs Reward',
                       'How pilots make calculated decisions that balance competitive advantage with safety.'),
              'cards': [('Listen',
                         '../library.html#s=Flight%20Mechanics',
                         'The full Flight Mechanics series',
                         '8 episodes, 9h 13m, every one transcribed'),
                        ('Related',
                         'know-your-equipment.html',
                         'Know Your Equipment',
                         'Harnesses, reserves, lines and what wears out'),
                        ('Related',
                         'meteorology.html',
                         'Meteorology',
                         'The air that makes the thermals in band 04'),
                        ('Ask',
                         'mailto:aninder@paraglidingatlas.com?subject=Flight%20Mechanics%20question',
                         'A question we did not answer?',
                         'Send it in for the next AMA episode')]}},

    "risk-vs-reward": {
    "layout": 2,
    "kicker": "Risk vs Reward",
    "h1": "When to Push and When to Stop",
    "lead": "How pilots who have lasted decide: what could actually kill you, what capacity means, what fear is for, and when a wing is earned rather than bought.",
    "sub": "Twelve conversations. A Canadian adventurer, a Himalayan bivouac pilot, an acro founder, a hang-gliding world champion, an Ozone test pilot, two SIV coaches, a coach who lives in a van, a rigger who tests reserves for fun, and a doctor who studies what pilots do under G.",
    "seo_title": "Paragliding Risk: When to Push and When to Stop | Paragliding Atlas",
    "seo_desc": "How experienced pilots judge risk: consequence over probability, capacity, using fear, stepping up a wing, throwing the reserve, flying high. 12 interviews.",
    "hero_alt": "Section through a valley: from launch, a grey line climbs in a thermal and crosses high with landing fields below, while an orange line goes straight across, low over a gorge with no landing",
    "bands": [
        {"num": "01", "kicker": "Consequence", "heading": "Judge what could kill you, not what is likely",
         "short": "Probability is the wrong first question. Ask what the worst outcome is, decide whether you can live with it, and only then ask how likely it is.",
         "paras": [
             "Will Gadd's rule is consequence over probability. The tempting glide into the lee that wins the task is also the one where a collapse puts you into rocks, and if you make that kind of call on probability, because you will probably get away with it, you do not last. He takes three more turns in the thermal, glides later, and accepts not winning, because a working glider and a working spine were worth more than that day. With his kids he runs the same thing as a three-step ladder: bumps and bruises, hospital, death. Name the level, then decide what to do about it.",
             "Manfred Ruhmer, who competed at the top of hang gliding for three decades, splits risk into two kinds that get confused. One is losing the task: going low, landing out, a bad day. The other is flying where the landing options are gone, which puts you in hospital rather than at the bottom of the results. The first is the sport. The second is the one to design out of your flying, and it is also why Gadd rejects the phrase sucked into a cloud: nobody is sucked in, they fly in, and once you own that, you can fix it by leaving earlier and checking the radar on your phone."],
         "bold": ["consequence over probability", "bumps and bruises, hospital, death", "two kinds", "nobody is sucked in, they fly in"],
         "chips": [("Will Gadd", WILL), ("Manfred Ruhmer", MANFRED)],
         "figure": {"img": "kb-risk-vs-reward-ladder", "w": 2400, "h": 640,
                    "alt": "Three rows labelled bumps and bruises, hospital and death, each with what to do about it, and a small probability dial off to the side",
                    "captions": [("Name the level", "Before the odds, before the plan: which row are you in? A playground, a drop-off on a trail, a glide over terrain with nowhere to land."),
                                 ("Then mitigate", "Each row has its own answer. The bottom row's answer is to find the line that removes it, not to estimate how often it happens."),
                                 ("Odds come last", "Probability still matters, and base rates are worth knowing. But it is the second question, and it never overrides the row.")],
                    "source_html": 'After Will Gadd, <a href="../episodes/consequence-over-probability-will-gadd-on-why-true-safety.html#c11">Episode 45, chapter 11</a>, and Manfred Ruhmer, <a href="../episodes/risk-vs-reward-3-manfred-ruhmer.html#c6">Episode 19, chapter 6</a>.'}},
        {"num": "02", "kicker": "Capacity", "heading": "Build capacity before the day you need it",
         "short": "You can only recover from a configuration you have already seen. Capacity is what you have when the probability call goes wrong anyway.",
         "paras": [
             "Gadd's second tool is capacity: develop it so that when you still get it wrong, the outcome is a bruise rather than a funeral. He learned to roll a kayak with a friend holding the boat upside down and hitting him on the head, and for paragliding he went to a gymnastics gym, put on his harness, and jumped off a three-metre bar into mats until he knew how to turn a vertical fall into a slide. Subir Sidhu, who logged 1,500 hours in his first three and a half years without skipping a class, puts the same idea in flying terms: you can reliably recover a glider only from a shape you have put it in before, so an SIV belongs in the first 50 to 100 hours of anyone who thermals, because a thermal is turbulence you went looking for.",
             "The coaches sharpen where the capacity should go. Beni Kalin argues that keeping the wing open matters more than any manoeuvre: a stall you rehearsed a hundred times over a lake does nothing for a big collapse ten metres off the deck, so active flying is the skill, and SIV is what you do for the rest. Russell Ogden adds a limit most pilots never measure: G tolerance varies from person to person and day to day, so learn yours early, and throw the reserve before your vision goes, because a couple of seconds after it goes, you are unconscious. When he tests spirals he only ever spirals to the right, so that if he loses vision he knows the exit is always left."],
         "bold": ["capacity", "reliably recover a glider only from a shape you have put it in before", "keeping the wing open matters more than any manoeuvre", "G tolerance"],
         "chips": [("Will Gadd", WILL), ("Subir Sidhu", SUBIR), (BH, META), ("Russell Ogden", RUSSELL)],
         "figure": None},
        {"num": "03", "kicker": "Fear", "heading": "Fear is information, not an obstacle",
         "short": "The pilots who show up to overcome their fear do not last. The ones who listen to it, back up and do the work are the ones still flying.",
         "paras": [
             "Gadd is direct about it: if you feel fear on launch, it does not matter what a hundred and fifty other pilots are doing. Back up, slow it down, find out why, and progress when you want to. The people who arrive determined to overcome their fear either get hurt or wash out, because the fear was telling the truth. On the day he won the US Nationals he blew up his glider on full bar in rough air and was back on the bar in fifteen seconds, not because he ignored fear but because he had none: he had done the work and knew he could handle it. If you have prepared and you are still terrified, the preparation is not finished.",
             "Raúl Rodríguez, who invented much of acro, still feels it on the way to the box before something new, and his answer is preparation: talk the manoeuvre through with every variation, imagine it many times, and then commit, because once the manoeuvre starts the fear leaves and only the glider remains. Kinga Masztalerz says flying strips every story you tell about yourself; after 200 winter hours in Bassano she took her confidence to the Swiss Alps in April, hit a tree inside two weeks, and spent two years mistrusting her own decisions. The SIV coaches' version is shorter: when your stomach says keep some distance from that wall, keep it. Every time one of them got into trouble, he had not listened."],
         "bold": ["Back up, slow it down, find out why", "the preparation is not finished", "once the manoeuvre starts the fear leaves", "flying strips every story you tell about yourself"],
         "chips": [("Will Gadd", WILL), ("Raúl Rodríguez", RAUL), ("Kinga Masztalerz", KINGA), (BH, META)],
         "figure": None},
        {"num": "04", "kicker": "Progression", "heading": "Step up on evidence, not appetite",
         "short": "Every class flies about the same at trim. The difference is on the bar, so the test is whether you are comfortable across the whole speed range of the wing you already fly.",
         "paras": [
             "Subir Sidhu's rule for cross-country pilots: a low B and a CCC both trim at 38 to 40 km/h, so the performance you pay for lives on the speed bar. If you are not comfortable from minimum sink to full bar on your current wing, in the air you actually fly in, the next class gives you nothing you can use. He proved it on himself: 700 hours on a Xeno, then a CCC on which he was not confident on full bar in the same air, and his mentor's answer was neither more hours on the D nor calmer days on the Enzo, but acro, to learn wing control. Beni Kalin's threshold is blunter: fly 200 km in a day without a collapse, then think about moving up.",
             "The counterintuitive part is that flying more can make you less safe. Kalin sees it most in speed flying, where the air is smooth, the ground is close, and daily flying breeds overconfidence; a few months off is useful because the sport feels fast again when you come back. Russell Ogden, who flies around 500 hours a year as a test pilot, says the biggest danger to him and his colleagues is themselves and the days they decide to fly. His numbers for the rest of us: 100 hours a year, three or four competitions, and about fifteen years before you reach your best. And when you are new, Manfred Ruhmer says, listen to the pilots who fly a lot and never get hurt, not the ones who talk a lot."],
         "bold": ["38 to 40 km/h", "acro, to learn wing control", "200 km in a day without a collapse", "flying more can make you less safe", "fly a lot and never get hurt"],
         "chips": [("Subir Sidhu", SUBIR), (BH, DK), ("Russell Ogden", RUSSELL), ("Manfred Ruhmer", MANFRED)],
         "figure": {"img": "kb-risk-vs-reward-stepup", "w": 2400, "h": 520,
                    "alt": "A wing's speed range as one bar from minimum sink through trim to full speed bar, with the pilot's comfortable range covering only the first half",
                    "captions": [("Min sink to trim", "This is where most pilots live, and where every class feels much the same. Comfort here proves little."),
                                 ("The speed bar", "Half bar to full bar in real air is where the class shows and where collapses come from. Comfort here is the test."),
                                 ("The rule", "Ready to move up when the whole bar is comfortable on the wing you have. Not before.")],
                    "source_html": 'After Subir Sidhu, <a href="../episodes/risk-vs-reward-2-subir-sidhu.html#c9">Episode 18, chapter 9</a>, and Beni Kalin, <a href="../episodes/cognitive-bias-of-dunning-kruger-effect-in-paragliding.html#c3">Episode 72</a>.'}},
        {"num": "05", "kicker": "The body", "heading": "Your body sets limits before your skill does",
         "short": "Above about 3,000 metres you are impaired before you notice. Cold multiplies the problem, and the effects outlast the altitude.",
         "paras": [
             "Dr Matt Wilkes lists four environmental factors pilots underestimate: oxygen, cold, G force and sun. Oxygen is the sly one, because hypoxia narrows your thinking, your peripheral vision and your control of the glider, and you do not feel it happening. Most people start to be affected somewhere above 3,000 to 3,500 metres, and the general aviation rule of thumb is thirty minutes above 3,000 or any time above 4,000. He puts a note on his cockpit that asks what he is thinking, because mood, thermalling precision and speech change first, and a flying partner will often notice before you do.",
             "Two multipliers make it worse. Shivering raises the oxygen your body burns by about five times, so staying warm is margin rather than comfort. And the effect has a hangover: descend and you feel better, but you are not back to full for up to ninety minutes. Sleeping high acclimatises; a competition that sleeps in the valley does not. His reserve research applies the same logic to the worst moment: under G, pilots reach along their skeleton, to the hip bone rotating forward and further down the thigh rotating back, and nobody could improvise a fix. The gear has to work where the hand actually goes, and there was no measurable difference in how fast pilots found a front-mounted handle versus a hip one."],
         "bold": ["oxygen, cold, G force and sun", "3,000 to 3,500 metres", "five times", "ninety minutes", "along their skeleton"],
         "chips": [("Dr Matt Wilkes", ALT), ("Dr Matt Wilkes", MATT)],
         "figure": {"img": "kb-risk-vs-reward-altitude", "w": 2400, "h": 760,
                    "alt": "An altitude scale marking where hypoxia begins to affect pilots, beside three cards: cold multiplies oxygen demand by five, time up high drains bandwidth, and recovery takes up to ninety minutes",
                    "captions": [("The threshold", "Individual, and worse if you are tired, dehydrated or hungover. Sleeping high helps; sleeping in the valley does not."),
                                 ("The multipliers", "Cold is the big one: shivering burns oxygen about five times faster. Time up high stacks fatigue day on day."),
                                 ("The check", "Note your altitude, ask what you are thinking, and let a buddy tell you when your speech changes.")],
                    "source_html": 'After Dr Matt Wilkes, <a href="../episodes/if-you-fly-in-the-himalayas-alps-or-above-3000-mtrs-this.html#c5">Episode 73</a> and <a href="../episodes/paragliding-physiology-safety-protocols-dr-matt-wilkes.html#c7">Episode 74, chapter 7</a>.'}},
    ],
    "quote_band": {"after_band": 1, "img": "kb-risk-vs-reward-section",
                   "alt": "Wireframe paraglider in an asymmetric collapse, the right side folded under, the pilot weight-shifting toward it with the reserve handle marked",
                   "kicker": "Capacity",
                   "quote": "Having a working glider and a working spine was more important than winning that day. Step back a little and it is obvious. It is only when you think in probabilities that the bad call looks fine.",
                   "who": "Will Gadd", "cite_ep": WILL, "cite_ch": "c4", "cite_label": "Episode 45, paraphrased",
                   "caption": "Drawn: an asymmetric collapse with the pilot releasing into the dropped side, and the reserve handle where the hand goes under G."},
    "callout": {"kicker": "If it goes wrong", "heading": "Throw early, throw down",
                "text": "Will Gadd knows almost nobody who threw their reserve and did not walk away, and almost nobody who braced for impact and did. Under G, Gabriel Orsini throws straight down between the legs rather than sideways, because twisted and rotating you cannot tell which side is out. Matt Wilkes found the hand goes to the hip bone rotating forward and down the thigh rotating back. And test yours over water first.",
                "ep": WILL, "ch": "c13", "who": "Will Gadd",
                "numbers": [("2", "s", "extra to bring the bag to your centre and throw it down. Worth it."),
                            ("83", "", "pilots tested in rotation at 2 to 4 G. Not one could improvise a fix under stress.")]},
    "takeaways_heading": "Worth remembering",
    "groups": [
        ("Deciding", [
            ("Consequence first, then odds", "The row you are in, bumps, hospital or death, decides the plan. Probability is the second question.", WILL, "c4", "Will Gadd"),
            ("There are two kinds of risk", "Losing the task is one. Flying where the landing options are gone is the other. Design the second out.", MANFRED, "c6", "Manfred Ruhmer"),
            ("Nobody gets sucked in", "You flew into the cloud. Own it, then leave earlier and check the radar next time.", WILL, "c13", "Will Gadd")]),
        ("Training", [
            ("Recover only what you have seen", "A shape your glider has never been in is one you will not fix. That is what SIV is for, early.", SUBIR, "c8", "Subir Sidhu"),
            ("Keep it open first", "A rehearsed stall does nothing for a big collapse ten metres up. Active flying is the skill.", META, "c9", "Beni Kalin"),
            ("Know your G tolerance", "It varies by person and by day. Throw before your vision goes; a few seconds later you are out.", RUSSELL, "c4", "Russell Ogden")]),
        ("Yourself", [
            ("Fear is a signal", "If you feel it, back up and find out why. If you did the work and are still terrified, do more work.", WILL, "c5", "Will Gadd"),
            ("The outcome is not the lesson", "Got away with a bad launch? An incident still happened. Ask what, why, and whether you knew.", SUBIR, "c8", "Subir Sidhu"),
            ("More flying is not more safety", "Daily smooth-air flying breeds overconfidence. A break makes it feel fast again, which is the point.", DK, "c1", "Beni Kalin")]),
    ],
    "faq_heading": "Questions these conversations answer",
    "faq": [
        {"q": "How do I decide whether a risk in paragliding is worth taking?",
         "a": "Will Gadd's method is consequence before probability. Ask what the worst outcome is: a bruise, a hospital, or death. Decide whether you accept that row, then work out how to mitigate it, and only then think about how likely it is. Making the call on probability alone, because you will probably get away with it, is how pilots stop lasting.",
         "ep": WILL, "ch": "c4", "who": "Will Gadd"},
        {"q": "What does capacity mean in paragliding, and how do I build it?",
         "a": "Capacity is what you have left when the probability call goes wrong: the collapse you have recovered fifty times, the crash you know how to slide out of. Gadd built it by practising crashing in a gymnastics gym. Subir Sidhu builds it in SIV and now acro, because you can only reliably recover a glider from a shape you have put it in before.",
         "ep": WILL, "ch": "c4", "who": "Will Gadd and Subir Sidhu"},
        {"q": "When should I do my first SIV course?",
         "a": "Subir Sidhu recommends within the first 50 to 100 hours for anyone who flies thermals, because a thermal is turbulence you went looking for, and turbulence will eventually put the glider somewhere new. For pilots who only soar smooth coastal air it matters less. Expect the first one to be somewhere between fun and terrifying, and expect to learn what you do under panic.",
         "ep": SUBIR, "ch": "c8", "who": "Subir Sidhu"},
        {"q": "When am I ready to move up a glider class?",
         "a": "Two tests from two pilots. Subir Sidhu: when you are comfortable across the entire speed range of your current wing, minimum sink to full bar, in the air you actually fly in, because every class trims at about the same speed and the difference lives on the bar. Beni Kalin: when you can fly 200 km in a day without a collapse.",
         "ep": SUBIR, "ch": "c9", "who": "Subir Sidhu and Beni Kalin"},
        {"q": "Is it normal to feel afraid before flying?",
         "a": "Yes, and Will Gadd says you would be an idiot not to in some conditions. The point is what you do with it: listen, back up, find the reason, and progress when the fear is gone rather than trying to override it. If you have prepared properly and are still terrified on launch, the preparation is not finished and the answer is to stand down or fly last and easy.",
         "ep": WILL, "ch": "c5", "who": "Will Gadd"},
        {"q": "When should I throw my reserve?",
         "a": "Earlier than you think. Will Gadd knows almost nobody who threw and did not walk away, and almost nobody who rode the glider into the ground and did. Russell Ogden's line is your vision: if it starts to go, throw, because a couple of seconds later you are unconscious. Raúl Rodríguez, who has thrown many times, calls the reserve his best friend.",
         "ep": WILL, "ch": "c13", "who": "Will Gadd, Russell Ogden and Raúl Rodríguez"},
        {"q": "Which way should I throw the reserve in a spiral or autorotation?",
         "a": "Gabriel Orsini throws it down, between the legs, not sideways. Under real G you cannot tell which side is out of the turn, and a sideways throw gives the spinning wing time to catch the lines. Matt Wilkes's research adds that pilots find the handle along their skeleton, hip bone rotating forward and thigh rotating back, so the handle has to be there.",
         "ep": GABRIEL, "ch": "c4", "who": "Gabriel Orsini and Dr Matt Wilkes"},
        {"q": "At what altitude does hypoxia start to affect paraglider pilots?",
         "a": "For most people somewhere above 3,000 to 3,500 metres, though it varies with fitness, fatigue, dehydration and the altitude you sleep at. Dr Matt Wilkes uses the general aviation guide of thirty minutes above 3,000 or any time above 4,000, watches for mood and thermalling changes, and warns that shivering multiplies your oxygen demand by about five.",
         "ep": ALT, "ch": "c5", "who": "Dr Matt Wilkes"},
        {"q": "Who should I take advice from as a new pilot?",
         "a": "Manfred Ruhmer: the pilots who fly a lot, fly cross-country regularly and never get hurt, not the ones who talk a lot. A pilot who breaks a bone every couple of seasons is not the one to ask. Gabriel Orsini adds that sponsored pilots are contractually biased about gear, and that the honest instructor's answer may sound worse than the salesman's.",
         "ep": MANFRED, "ch": "c6", "who": "Manfred Ruhmer and Gabriel Orsini"},
        {"q": "What is intermediate syndrome in paragliding?",
         "a": "The stage where a pilot's confidence outruns their judgement, usually after a fast early progression. Kinga Masztalerz describes hers: 200 hours of gentle winter flying in Bassano, then the Swiss Alps in April, a tree inside two weeks, and two years of mistrusting her own decisions. Beni Kalin and Heli Schrempf see it in pilots who skip steps and reflect only after the crash.",
         "ep": KINGA, "ch": "c5", "who": "Kinga Masztalerz, Beni Kalin and Heli Schrempf"},
    ],
    "next": {"main": ("know-your-equipment.html", "Know Your Equipment", "Harnesses, reserves, lines, helmets, and what the people who design and test them wish pilots knew."),
             "cards": [("Listen", "../library.html#s=Risk%20vs%20Reward", "The full Risk vs Reward series", "12 episodes, 14h 04m, every one transcribed"),
                       ("Related", "flight-mechanics.html", "Flight Mechanics", "Why the wing collapses in the first place, and what keeps it open"),
                       ("Related", "meteorology.html", "Meteorology", "The other half of the consequence question: the air you are choosing"),
                       ("Ask", "mailto:aninder@paraglidingatlas.com?subject=Risk%20vs%20Reward%20question", "A question we did not answer?", "Send it in for the next AMA episode")]},
    },

    "know-your-equipment": {
    "layout": 2,
    "kicker": "Know Your Equipment",
    "h1": "What Your Gear Can and Cannot Do",
    "lead": "Reserves, harness protectors, helmets, carabiners and lines, from the people who design, test and repack them, with what the certification stamp does and does not promise.",
    "sub": "Six conversations. A reserve designer with 400 openings, a pilot who reverse-engineered the harness standard, the helmet maker who was also a world champion, a competition trimmer, and a whitepaper on why a carabiner that looks fine can still fail.",
    "seo_title": "Paragliding Gear: Reserves, Harnesses, Helmets | Paragliding Atlas",
    "seo_desc": "What paragliding gear really does: reserve size and deployment, harness protectors and jerk, EN 966 helmets, carabiner fatigue and line trim, from those who test it.",
    "hero_alt": "A round reserve parachute open above a pilot, the paraglider hanging neutralised beside them, with two arrows showing 5.5 metres per second down and 5.5 forward, the 1:1 glide certification allows",
    "bands": [
        {"num": "01", "kicker": "Reserves", "heading": "The reserve must dominate the wing",
         "short": "A small, light reserve passes certification because it is tested without a paraglider attached. Connected to one, it has to win a fight, and at 20 square metres it often does not.",
         "paras": [
             "Urs Haari has designed reserves for decades and has close to 400 openings, most of them above ground. His first rule is size. The current standard allows a certified reserve to glide at up to 1:1, so a canopy sinking at 5.5 metres a second may also be moving forward at 5.5, around 18 km/h. Small, light designs only reach the sink rate by gliding, and gliding is harmless right up until the moment a paraglider is connected to it. Then forward speed becomes a downplane, and in safety clinics he now sees more downplanes than ever. Testing a certified reserve over water with a tandem passenger in front of him, his instrument read 50 km/h over the ground.",
             "So his advice is to buy surface, not the lightest thing in the magazine: whatever the paraglider does, the reserve must dominate it, and at 20 square metres for an 80 kg pilot it will not. If you fly a hot wing and want a small reserve, carry two, because a reserve that ends up in the rotating paraglider's lines is game over if you are not high enough for a plan B. Round, square or Rogallo, his one-word answer to which is safest is all of them: there are good and bad designs of each, and the difference is whether it has been tested hundreds of times or only advertised."],
         "bold": ["glide at up to 1:1", "50 km/h over the ground", "the reserve must dominate it", "carry two"],
         "chips": [("Urs Haari", URS)],
         "figure": None},
        {"num": "02", "kicker": "Deploying", "heading": "The throw is a procedure, not a reflex",
         "short": "Throw, wait for the opening, act if it does not come, then neutralise the paraglider. Only after that do you steer. The order is the same for a steerable and a non-steerable reserve.",
         "paras": [
             "Haari runs clinics because the usual approach, a big collapse at the end of an SIV and throw it to see what happens, teaches nothing that lasts. The night before, pilots pull their reserve in a simulator, and 30 percent cannot get it out of the harness. Then the sequence: throw; wait for the opening; if nothing happens, get active, because pilots who wait and wait are the ones who never open it; and as it inflates, start neutralising the paraglider with a B-stall or C-stall so the two canopies stop fighting. Only then, if there is height, take a brake line of a steerable reserve in the free hand and turn away from the power line or the river.",
             "Two things most pilots do not know. A non-steerable square or round canopy can still be nudged: pull the lines on one side and it will drift the other way, enough to miss an obstacle. And a reserve opening at 30 or 40 metres still works; even one that ends up in a tree with you hanging in the lines is a success, because you did not hit the ground. He also carries a proper hook knife, having once had to cut lines on a prototype with a twisted riser, and points out that the toy-shop knives most pilots fly with will not cut a loaded riser."],
         "bold": ["30 percent", "get active", "still be nudged", "30 or 40 metres"],
         "chips": [("Urs Haari", URS), ("Urs Haari", URS2)],
         "figure": None},
        {"num": "03", "kicker": "Wear", "heading": "Fabric, metal and line all fail quietly",
         "short": "A reserve can be ruined in three moves on cut grass, a carabiner can be fatigued and look perfect, and a competition wing can drift 18 millimetres slow without the pilot noticing. None of it shows.",
         "paras": [
             "Do not ground-handle your reserve. Haari watches acro pilots dry Rogallos on the grass at Garda and says light fabric can be destroyed in two or three moves on a freshly cut slope; the damage is invisible until the canopy is hung under strong light. To air it before a repack, pull it in a simulator to check it comes out, avoid every sharp edge, and hang it on its lines indoors for 48 hours in normal humidity. Pack it the way the manufacturer says: trash packing works for acro pilots with a second reserve, but a careful pack opens cleaner and with fewer twists. Skydivers will not board a plane with a reserve packed more than four months ago. Paragliding has no such rule.",
             "Carabiners fail the same silent way. A 20 kN rating is a static number; the loads that matter are the cyclic ones, every launch and every reopening, which grow microscopic cracks in aluminium long before anything is visible. Finsterwalder and Charly's guidance is five years for aluminium, sooner for acro, rinsed after salt air and stored dry. And lines: Brett Janaway trims competition wings for a living, and the World Cup now checks three wings a day. A new wing inflates 10 to 15 mm fast, settles toward zero over its first hours as the cascade knots bed in, then drifts slow; on the British team he found one pilot 18 mm slow who had never trimmed in a year. The limit for competition trim came down from 20 mm fast to 10 because pilots were using the tolerance as a speed setting. His own rule for everyone else: if it flies nicely, leave it alone."],
         "bold": ["two or three moves", "48 hours", "four months", "cyclic ones", "10 to 15 mm fast", "if it flies nicely, leave it alone"],
         "chips": [("Urs Haari", URS), ("Finsterwalder & Charly", CARAB), ("Brett Janaway", BRETT2)],
         "figure": None},
        {"num": "04", "kicker": "Harness", "heading": "The number on the test report is the wrong number",
         "short": "The standard measures peak G in a vertical drop. What breaks vertebrae is how suddenly that G arrives, and a crumple protector delivers it as a step.",
         "paras": [
             "Zsolt Ero sat on the harness standard's working group as one of its independent pilots and came away convinced it tests the wrong thing. The drop is perfectly vertical, which no real impact is, and the pass mark is a peak G value. But the NASA ejection-seat studies the industry cites also set a limit on jerk, the rate at which G rises, because it was the pilots with a fast rise who fractured vertebrae, not the ones with the highest peak. Foam and airbags compress progressively, so the curve rises smoothly. A crumple honeycomb does nothing until the load exceeds its threshold, then collapses all at once: a corner in the graph, and in his measurements a jerk several times what the previous generation of race harnesses produced.",
             "His numbers from reading the published test files: the older race harnesses came in under the NASA limit without anyone having designed for it. Measuring jerk properly would push protectors from about 7 cm back to about 13, which is why the manufacturers' group has resisted it, and why he argues safety-critical gear should be governed independently of the people who sell it, as helmets are in motorsport. For the rest of us, the report on the test database shows the G curve for every harness; look at the shape of the rise, not just the peak. And once glide starts to matter, at around 50 hours, a stable pod is safer to progress in than a chair you are tiring of."],
         "bold": ["peak G", "jerk", "a corner in the graph", "about 7 cm back to about 13", "the shape of the rise"],
         "chips": [("Zsolt Ero", ZSOLT)],
         "figure": {"img": "kb-know-your-equipment-jerk", "w": 2400, "h": 640,
                    "alt": "Two G-versus-time curves from a harness drop test: a smooth bell for foam or airbag, and a flat line then a near-vertical step for a crumple honeycomb",
                    "captions": [("Foam or airbag", "Compresses progressively, so G rises smoothly. The peak can be the same as the other curve, but the body has time to load."),
                                 ("Crumple honeycomb", "Solid until its threshold, then it gives all at once. The step is the jerk, and it is what the ejection-seat research linked to fractured vertebrae.")],
                    "source_html": 'After Zsolt Ero, <a href="../episodes/watch-this-before-you-buy-a-paragliding-harness-a-talk.html#c10">Episode 62, chapters 10</a> and <a href="../episodes/watch-this-before-you-buy-a-paragliding-harness-a-talk.html#c11">11</a>. Schematic, not measured data.'}},
        {"num": "05", "kicker": "Helmet", "heading": "What EN 966 tests, and what a bike helmet fails",
         "short": "A flying helmet is dropped from 1.5 metres and must keep the head under 250 G, must stop a falling point 5 mm short of the skull, and may have nothing sticking out that a line could catch.",
         "paras": [
             "Christian Ciech competed at the top of hang gliding and now runs ICARO 2000, so he has both flown at the limit and built what protects you at it. EN 966 is the standard: a 1.5 metre drop with the head form registering under 250 G, a penetration test with a pointed weight that must stop at least 5 mm from the head, a chin strap that keeps the helmet on, and all of it repeated after conditioning at minus 20, plus 50, in UV and in water. A good new helmet passes at 170 to 180 G, and the softer, thicker liner that achieves that will dent under your fingertip. That is a feature.",
             "A motorcycle helmet protects more but fails the flying test in two ways: it is too heavy for hours under a wing, and its visor and vents protrude beyond the 5 mm the standard allows, so a line can catch. Vented bike and climbing helmets fail the penetration test outright. Full-face is more protective; open-face gives more vision. Neither is wrong, and he flies open-face himself. Replace after any crash of substance, and treat the five-year rule as a recommendation for helmets that get dropped and forgotten, not a law for one that has been looked after. Camera mounts are untested territory, and a line around one is the obvious way they go wrong."],
         "bold": ["1.5 metre drop", "under 250 G", "5 mm", "dent under your fingertip", "penetration test outright"],
         "chips": [("Christian Ciech", CIECH)],
         "figure": {"img": "kb-know-your-equipment-helmet", "w": 2400, "h": 600,
                    "alt": "Three helmet test panels: a 1.5 metre drop with a 250 G limit, a falling point that must stop 5 mm from the head, and a rule that nothing on the shell may protrude more than 5 mm",
                    "captions": [("Drop", "1.5 metres onto a head form, under 250 G. Repeated hot, cold, wet and after UV."),
                                 ("Penetration", "A pointed weight must stop 5 mm short. Big vents fail here, which is why bike and climbing helmets are not flying helmets."),
                                 ("Nothing to snag", "Anything on the shell within 5 mm. Motorcycle visors, and most camera mounts, are outside it.")],
                    "source_html": 'After Christian Ciech, <a href="../episodes/helmet-safety-christian-ciech-icaro-2000.html#c3">Episode 25, chapters 3</a>, <a href="../episodes/helmet-safety-christian-ciech-icaro-2000.html#c4">4</a> and <a href="../episodes/helmet-safety-christian-ciech-icaro-2000.html#c5">5</a>.'}},
    ],
    "quote_band": {"after_band": 0, "img": "kb-know-your-equipment-section",
                   "alt": "A 25 square metre paraglider planform drawn to the same scale as three reserve canopies of 20, 30 and 40 square metres",
                   "kicker": "Size",
                   "quote": "Opening time is not the question any more; they all open fast. The question is whether your reserve dominates your paraglider, whatever the paraglider does. At twenty square metres, it will not.",
                   "who": "Urs Haari, reserve designer", "cite_ep": URS, "cite_ch": "c11", "cite_label": "Episode 41, paraphrased",
                   "caption": "Drawn to scale: a 25 m² wing and three reserve canopies. Reserve hook-in weights are quoted without the paraglider attached."},
    "callout": {"kicker": "Before you need it", "heading": "Pull it out in a simulator",
                "text": "In Urs Haari's clinics, pilots hang in a simulator the night before and throw. Three in ten cannot get the reserve out of their harness. That is the cheapest, most decisive equipment test in the sport, and the one almost nobody does. Then, if you can, throw it for real over water.",
                "ep": URS, "ch": "c7", "who": "Urs Haari",
                "numbers": [("30", "%", "of pilots could not get their reserve out of the harness in the simulator"),
                            ("4", "mo", "the repack age past which a skydiver is refused a seat on the plane")]},
    "takeaways_heading": "Worth remembering",
    "groups": [
        ("Reserve", [
            ("Buy surface, not weight", "Certified reserves are allowed to glide 1:1. Connected to a paraglider that becomes a downplane. Go big, or go two.", URS, "c6", "Urs Haari"),
            ("If it does not open, act", "Pilots who throw and wait are the ones who never open it. Get active, then neutralise the paraglider.", URS, "c7", "Urs Haari"),
            ("You can steer a round one", "Pull the lines on one side and it drifts the other. Not a spot landing, just enough to miss the power line.", URS2, "c1", "Urs Haari")]),
        ("Protection", [
            ("Read the curve, not the peak", "Every harness report shows G against time. A smooth rise is what the body tolerates. A step is jerk.", ZSOLT, "c11", "Zsolt Ero"),
            ("A soft liner is a good sign", "The new helmets that pass at 170 G have thicker, softer polystyrene. If it dents under your fingertip, it is working.", CIECH, "c8", "Christian Ciech"),
            ("Bike helmets are not flying helmets", "Vents fail the penetration test and sharp edges catch lines. EN 966 or it is improvisation.", CIECH, "c5", "Christian Ciech")]),
        ("Wear", [
            ("Never ground-handle a reserve", "Two or three moves on cut grass can ruin light fabric, invisibly. Hang it indoors for 48 hours instead.", URS, "c13", "Urs Haari"),
            ("Aluminium fatigues in silence", "Five years for carabiners, less for acro. A 20 kN rating says nothing about cyclic loads or cracks you cannot see.", CARAB, "c3", "Finsterwalder & Charly"),
            ("A new wing is fast, then slow", "10 to 15 mm fast on first inflation, zero after the knots bed in, then drifting slow. If it flies nicely, leave it.", BRETT2, "c8", "Brett Janaway")]),
    ],
    "faq_heading": "Questions these conversations answer",
    "faq": [
        {"q": "How big should my reserve parachute be?",
         "a": "Bigger than the marketing suggests. Urs Haari's test is whether the reserve dominates the paraglider whatever the paraglider does, and he says a 20 square metre canopy for an 80 kg pilot will not. Certification allows a 1:1 glide, so small reserves pass by gliding, which becomes a downplane once a wing is attached. Buy surface, and if you insist on small, carry two.",
         "ep": URS, "ch": "c11", "who": "Urs Haari"},
        {"q": "Round, square or Rogallo: which reserve is safest?",
         "a": "All of them, and none of them, according to Haari, who has tested nearly everything on the market. There are good and bad rounds, squares and Rogallos. What separates them is whether the design has been tested hundreds of times in real openings or only described in a brochure. A steerable reserve only helps if you have practised steering it.",
         "ep": URS, "ch": "c9", "who": "Urs Haari"},
        {"q": "What do I do if my reserve does not open?",
         "a": "Get active. Haari says the pilots who throw and then wait are the ones who never see an opening; there are ways to help a hesitating canopy, and they need to be learned before the day. As it inflates, neutralise the paraglider with a B-stall or C-stall so the two stop fighting. Only after that, if there is height, steer.",
         "ep": URS, "ch": "c7", "who": "Urs Haari"},
        {"q": "Can I steer a non-steerable reserve?",
         "a": "A little, and it can be enough. Pull in the lines on one side of a round or square canopy and it will drift the other way; Haari uses it to avoid a power line, a house or a river, not to pick a landing. It works better with some wind. Try it over water first, because the first time is not the time to find out.",
         "ep": URS2, "ch": "c1", "who": "Urs Haari"},
        {"q": "Can I air my reserve on the grass before repacking?",
         "a": "No. Light reserve fabric can be ruined in two or three moves on freshly cut grass, and the damage does not show until the canopy is hung under strong light. Haari's method: pull it in a simulator to check it comes out, avoid any sharp edge, and hang it on its lines indoors for 48 hours before packing it the way the manual says.",
         "ep": URS, "ch": "c13", "who": "Urs Haari"},
        {"q": "Is a thin crumple protector as safe as foam?",
         "a": "Not in the way that matters, argues Zsolt Ero. It can pass the peak-G drop test, but a honeycomb does nothing until its threshold and then collapses at once, delivering the load as a step. The ejection-seat research the standard leans on links that rate of rise, the jerk, to fractured vertebrae. Foam and airbags compress progressively, and the older race harnesses came in under the limit.",
         "ep": ZSOLT, "ch": "c10", "who": "Zsolt Ero"},
        {"q": "How do I read a harness test report?",
         "a": "Every certified harness has a published drop-test graph of G against time. Most pilots look up the peak and stop. Ero says to look at the shape of the first rise: a smooth curve means a spring-like protector, a near-vertical corner means a crumple structure that did nothing until it gave way. The peak matters less than how suddenly it arrives.",
         "ep": ZSOLT, "ch": "c11", "who": "Zsolt Ero"},
        {"q": "Can I fly with a climbing or cycling helmet?",
         "a": "You can, but it is not a flying helmet. Christian Ciech says the vents that make them cool to hike in fail the EN 966 penetration test outright, and their sharp edges can catch lines. A motorcycle helmet fails for the opposite reasons: too heavy for hours of flying, and its visor and vents protrude beyond the 5 mm the standard allows.",
         "ep": CIECH, "ch": "c5", "who": "Christian Ciech"},
        {"q": "How often should I replace my helmet and carabiners?",
         "a": "Helmet: after any real crash, and otherwise the five-year rule is a recommendation for helmets that get dropped and forgotten, not a law for one that is looked after. Carabiners: aluminium fatigues from cyclic loads with no visible sign, so five years is the guidance, sooner for acro, and steel is not immune. Rinse after salt air, store dry.",
         "ep": CARAB, "ch": "c3", "who": "Finsterwalder & Charly and Christian Ciech"},
        {"q": "Why does a paraglider need trimming, and when?",
         "a": "Lines shrink with use and the cascade knots tighten, so a new wing that inflates 10 to 15 mm fast settles to zero over its first hours and then drifts slow. A slow competition wing climbs badly and recovers worse. Brett Janaway trims after about 20 to 30 hours, checks again as it stabilises, and never spirals a trimmed comp wing down. If it flies nicely, do not touch it.",
         "ep": BRETT2, "ch": "c8", "who": "Brett Janaway"},
    ],
    "next": {"main": ("meteorology.html", "Meteorology", "How pilots read the sky before and during the flight: fronts, inversions, valley winds and the day's timing."),
             "cards": [("Listen", "../library.html#s=Know%20Your%20Equipment", "The full Know Your Equipment series", "8 episodes, 6h 39m, every one transcribed"),
                       ("Related", "risk-vs-reward.html", "Risk vs Reward", "When to throw the reserve, and why earlier than you think"),
                       ("Related", "flight-mechanics.html", "Flight Mechanics", "What the lines and the trim actually do to the wing"),
                       ("Ask", "mailto:aninder@paraglidingatlas.com?subject=Equipment%20question", "A question we did not answer?", "Send it in for the next AMA episode")]},
    },
    "new-technologies": {
    "layout": 2,
    "kicker": "New Technologies",
    "h1": "Is New Paragliding Technology Making Wings Safer?",
    "lead": "Two-liners in the B class, harnesses that watch the wing, kites borrowed from the beach, and what the certification letter does and does not tell you, from the people who design them.",
    "sub": "Seven conversations. The inventor of RAST on his own two-liner, Niviuk's R&D team, designers from AirDesign, UP and Supair, an acro pilot who builds harnesses, and the man who took a kite to the mountains.",
    "seo_title": "New Paragliding Tech: Two-Liners, Smart Harnesses | Paragliding Atlas",
    "seo_desc": "What new paragliding technology changes: EN tests versus real safety, two-liner B wings, harness protectors and drag, AI harnesses and kite wings, from designers.",
    "hero_alt": "A thick modern paraglider airfoil drawn as a technical sheet, with two load-bearing line groups labelled AA and BB, the old A point kept as an unloaded line, a dashed flexing nose, and a sensor trace running beneath",
    "bands": [
        {"num": "01", "kicker": "Certification", "heading": "The letter rates the wing, not your flight",
         "short": "A certification test folds the wing along stickers and watches what it does. A real pilot reacts, and real turbulence loads every line at once. The letter is a fair comparison, not a forecast.",
         "paras": [
             "Frantisek Pavlousek has designed wings at UP for three decades and draws a clear line between safety according to certification and safety in real flight. They are linked but not the same: a low B can be as safe in the air as an A and miss the A on a single manoeuvre. The test is deliberately artificial. In the big asymmetric collapse the lab folds 50 percent of the trailing edge, plus or minus 2.5, along a line at 45 degrees to the open side, marked with stickers on the bottom surface, and the pilot releases the brake and does nothing. That is not what a trained pilot does, and the designer's easiest way to turn a C grade on that manoeuvre into a B is a slower trim speed.",
             "Stephan Stiegler of AirDesign describes the same tension from the other side: a norm has to be identical every time, so the collapse must land in the marked field even when the wing would rather fold flatter or steeper. Pavlousek explains that this is what folding lines are for; on a two-liner the correct fold is often hard or impossible to pull from the risers. Stiegler's conclusion is that the manufacturer carries the duty to make a wing actually fly like its class, and that counting the Bs on two reports tells a buyer little. Read the designer's description of who the wing is for. Michael Nesler goes further: some companies treat the test as a marketing hurdle to be passed with tricks."],
         "bold": ["safety in real flight", "50 percent of the trailing edge", "45 degrees", "slower trim speed", "folding lines", "counting the Bs"],
         "chips": [("Frantisek Pavlousek", UPF), ("Stephan Stiegler", STIEG), ("Michael Nesler", NESLER)],
         "figure": None},
        {"num": "02", "kicker": "Two-liners", "heading": "Fewer lines, because the profile got fatter",
         "short": "Thicker airfoils hold more air and more pressure, so they need fewer attachment points. The hard part is the long span between the two groups, and the nose ahead of the front one.",
         "paras": [
             "Michael Nesler invented RAST for Swing, and now builds his own two-liner, the LeelooX, certified in the B class. His explanation starts with the section. Forty years ago a paraglider profile was around 9 to 12 percent of the chord thick; today's are around 18. Paragliders fly slowly, so the thick section suits them, and the extra volume and pressure let a designer hang the wing on fewer points. The problem, even now, is the long unsupported stretch between the front and rear groups: push a wingover and the canopy squeezes there, the airfoil loses shape, and the wing loses lift. He sees it as a real problem on some of today's two-liners.",
             "His answer is to move the double A points far back, which shortens that gap and leaves a longer, softer nose in front. When the nose is loaded it deforms and the wing pitches forward and accelerates by itself, which he argues makes a two-liner safer than a three-liner. He kept the old A attachment as a line that carries no load, for launching and manoeuvres, and reports a longer brake range and a softer stall, crediting the canopy rather than the line count. Niviuk's engineers put it more cautiously: two lines are about drag, safety has to be held or improved on every project, and whether an A school wing goes two-line is still open."],
         "bold": ["9 to 12 percent", "around 18", "long unsupported stretch", "double A points far back", "accelerates by itself", "softer stall"],
         "chips": [("Michael Nesler", NESLER), ("Guillem Batlle & Adrià Grau", NIVIUK)],
         "figure": {"img": "kb-new-technologies-airfoil", "w": 2400, "h": 620,
                    "alt": "Two paraglider airfoils to the same chord: a thin profile of forty years ago with four attachment rows A to D, and a thick modern profile with only two groups, AA and BB",
                    "captions": [("Forty years ago", "A profile about 9 to 12 percent of chord needed four rows of lines to hold its shape."),
                                 ("Today", "Around 18 percent: more volume and pressure, so two groups can carry the load, with AA set well back from the nose.")],
                    "source_html": 'After Michael Nesler, <a href="../episodes/why-paraglidings-safety-future-looks-different-rast.html#c3">Episode 44, chapter 3</a>. Schematic, not a real wing.'}},
        {"num": "03", "kicker": "Harness", "heading": "The harness is the least developed thing you fly",
         "short": "The drop test is vertical, the reserve cable runs under your seat, and a slab of bed foam can pass. The designers trying to change that are working on protection, extraction and drag.",
         "paras": [
             "Veselin Ovcharov flies acro and builds harnesses, and his view is blunt: the sport has been flying rucksacks for decades. Certification is mostly about strength, webbing and stitching, plus a drop of a few metres onto the protector, and he says 12 centimetres of ordinary bed foam would pass it. He also points at the reserve: a skydiving rig routes the cable around the back so it pulls straight, while in a paraglider harness it runs under the seat and gets heavy under G. On Koroyd-type crumple protectors his advice is practical rather than technical: they suit good pilots who want protection for the rare hard crash; a beginner is better served by a classic protector that covers more scenarios.",
             "Niviuk's Guillem Batlle and Adrià Grau explain why a protector can pass and still fail a pilot: the test drop is vertical, and if a real impact is not, pieces can rotate or slip out of place. They drop-tested their Origami protector at different orientations and angles, designed it to stay locked in its foam, and ran it through six consecutive high-energy drops across the EN and LTF sequences; a foam giving the same protection would need to be more than 60 percent thicker. Drag is the other axis. Supair's Roman Barthelemy measures a chair at about 23 newtons, a faired pod at about 12 and a submarine at about 8; in real flying the submarine gains about half a point of glide over a good pod."],
         "bold": ["flying rucksacks", "12 centimetres of ordinary bed foam", "runs under the seat", "the test drop is vertical", "six consecutive high-energy drops", "half a point of glide"],
         "chips": [("Veselin Ovcharov", VESELIN), ("Guillem Batlle & Adrià Grau", NIVIUK), ("Roman Barthelemy", SKYMATE)],
         "figure": {"img": "kb-new-technologies-drag", "w": 2400, "h": 620,
                    "alt": "Three pilots in harness drawn side-on, a chair, a faired pod and a submarine, each with a bar showing drag of about 23, 12 and 8 newtons",
                    "captions": [("Chair", "About 23 N. The upright pilot is most of the frontal area."),
                                 ("Pod with a fairing", "About 12 N, roughly half the chair."),
                                 ("Submarine", "About 8 N, a third less again. In the air, about half a point of glide over a good pod.")],
                    "source_html": 'After Roman Barthelemy, <a href="../episodes/understanding-skymate-paragliding-worlds-first-ai-driven.html#c6">Episode 49, chapter 6</a>. Drawings schematic.'}},
        {"num": "04", "kicker": "Electronics", "heading": "A harness that knows the wing is spinning",
         "short": "Supair's Skymate reads the wing around a hundred times a second, is built to tell an autorotation from anything else, and can act when the pilot does not, with the same redundancy skydivers expect.",
         "paras": [
             "Roman Barthelemy designs harnesses at Supair and describes Skymate as an automatic activation device of the kind skydivers have used for years, rebuilt for a paraglider. A single sensor package in the wing, accelerometer, gyro, magnetometer and attitude, tracks exactly how the canopy is flying, around 100 readings a second during development. The system is tuned for one job first: separating an autorotation from everything else, which he says it now does very well. Because the dangerous sequence is a collapse that becomes a cravat and then a spin, it is already primed when it sees the collapse, before the pilot has recognised what is happening.",
             "For now deployment mode is limited to autorotation, and perhaps later twists. It uses two separate systems to release the reserve, as in skydiving, and it sends a rescue alert over 3G or 4G the moment a collapse turns into a spin, while the pilot is still high enough to have signal. It only works with Supair wings, because the model has to know how a given wing behaves. He is deliberately using a basic detection model rather than headline AI, because the priority is electronics that are durable and repairable, and recorded flights will be replayed on a bench to find the corner cases."],
         "bold": ["automatic activation device", "around 100 readings a second", "separating an autorotation", "two separate systems", "rescue alert", "Supair wings", "basic detection model"],
         "chips": [("Roman Barthelemy", SKYMATE)],
         "figure": None},
        {"num": "05", "kicker": "Borrowed ideas", "heading": "Most new ideas were tried somewhere else first",
         "short": "A kite taken to the mountains became a new kind of soaring wing. Closed cells were tried on paragliders and dropped. Aerospace ideas only work after a redesign. Progress is rarely a straight line.",
         "paras": [
             "Beni Kälin runs a speed flying school in Switzerland and started flying race kites on the dunes, hooked to a paragliding harness, before taking them to the mountains. His 11 metre kite flew like a paraglider with the speed of a 6 or 7 metre speed wing, but it was still a kite: if it collapsed it might not reopen, so it was only safe as low as you were willing to fall. That experience fed the Moustache, built from a closed-cell prototype that had never been put on the market. On a ridge you choose your height with the toggles and can dive and convert the speed back into lift. It is more collapse-stable on full bar than any paraglider, he says, but it is marketed away from thermals, because it makes strong wind easy, and 50 km/h of wind carries four times the energy of 25.",
             "Its SIV behaviour shows the trade. Collapses are hard to pull and the reaction is gentle, but a wing that folds while fully accelerated has little internal pressure, so hands-up it reopens slowly; a pump on the collapsed side brings it back. Closed cells and air valves were tried on paragliders long ago and abandoned as too dangerous, and Kälin thinks it is good that a paraglider can collapse. Niviuk's engineers add that an aerospace idea has to be redesigned before it helps a wing, and that ideas leave the market and return when the technology catches up. At AirDesign, Stiegler's Rise 4 stayed in production almost five years because prototype after prototype failed to beat it."],
         "bold": ["race kites", "only safe as low as you were willing to fall", "dive and convert the speed back into lift", "four times the energy", "a pump on the collapsed side", "abandoned as too dangerous", "almost five years"],
         "chips": [("Beni Kälin", BENI), ("Guillem Batlle & Adrià Grau", NIVIUK), ("Stephan Stiegler", STIEG)],
         "figure": None},
    ],
    "quote_band": {"after_band": 0, "img": "kb-new-technologies-section",
                   "alt": "A paraglider planform marked for the big asymmetric collapse test: half the trailing edge shaded, a fold line at 45 degrees with square stickers along it, and a dashed folding line running down to the risers",
                   "kicker": "Two kinds of safety",
                   "quote": "Certification and real safety are connected, but they are not the same thing. A low B can be as safe in the air as an A, and fail the A on just one manoeuvre.",
                   "who": "Frantisek Pavlousek, UP Paragliders", "cite_ep": UPF, "cite_ch": "c3", "cite_label": "Episode 29, paraphrased",
                   "caption": "How a lab marks a wing for the big asymmetric collapse: half the trailing edge, a fold at 45 degrees, stickers to aim at, and a folding line to pull it there."},
    "callout": {"kicker": "Reading a test report", "heading": "The collapse is aimed at stickers",
                "text": "Before a wing goes to the lab, markers are stuck to the bottom surface to show exactly where the big asymmetric collapse must fold, and folding lines are added to pull it there. Real turbulence hits all the lines together and folds more than any test can. Use the letter to compare wings under one rule, not to predict your own flight.",
                "ep": UPF, "ch": "c5", "who": "Frantisek Pavlousek",
                "numbers": [("50", "%", "of the trailing edge folded in the big asymmetric test, plus or minus 2.5"),
                            ("45", "°", "the angle the fold runs forward to the open side of the leading edge")]},
    "takeaways_heading": "Worth remembering",
    "groups": [
        ("Buying", [
            ("The letter is not the whole story", "A low B can match an A in the air. Read the designer's description of who the wing is for, not a tally of grades.", STIEG, "c7", "Stephan Stiegler"),
            ("You are the weakest link", "Safety and performance both follow the weakest point of the chain. A C wing flown by a B pilot gives neither.", UPF, "c6", "Frantisek Pavlousek"),
            ("Let a new model settle", "Pavlousek's long-time flying friends buy a wing once it has been on the market for a year and people know how it behaves.", UPF, "c10", "Frantisek Pavlousek")]),
        ("Wings", [
            ("Thick profiles made two-liners possible", "More volume and pressure means fewer attachment points. The weak spot is the long gap between groups.", NESLER, "c3", "Michael Nesler"),
            ("From mid B, fly actively", "Stiegler's threshold: be ready to stop the pitch, then learn to feel it coming. Then you fly the wing, not the other way round.", STIEG, "c6", "Stephan Stiegler"),
            ("Pump an accelerated collapse", "A fully accelerated wing has little pressure inside and reopens slowly hands-up. Countersteer and pump the closed side.", BENI, "c9", "Beni Kälin")]),
        ("Harness", [
            ("The drop test is vertical", "Crashes are not. Ask whether a protector was tested at angles, and whether it stays in place.", NIVIUK, "c11", "Guillem Batlle & Adrià Grau"),
            ("Crumple protectors suit good pilots", "For the rare hard crash, fine. A beginner gets more all-round protection from a classic protector.", VESELIN, "c10", "Veselin Ovcharov"),
            ("Electronics that watch the wing", "Skymate is built to spot a collapse turning into autorotation and send a rescue alert over 4G while you still have signal.", SKYMATE, "c13", "Roman Barthelemy")]),
    ],
    "faq_heading": "Questions these conversations answer",
    "faq": [
        {"q": "Does EN certification tell me how safe a paraglider is?",
         "a": "It tells you how the wing behaved in a fixed set of tests, which makes wings fair to compare. Frantisek Pavlousek of UP says certification safety and real safety are linked but not identical: a low B can be as safe in the air as an A that passed, and miss the A on one manoeuvre. Use the letter as a starting point, then read the manufacturer's description.",
         "ep": UPF, "ch": "c3", "who": "Frantisek Pavlousek"},
        {"q": "Why is the certification collapse done hands up?",
         "a": "Because a norm has to compare wings under one identical rule, and a pilot's reaction cannot be standardised. The test pilot pulls the A riser with no brake in hand and does nothing, which Pavlousek calls already outside reality, since a trained pilot reacts. It also explains a design trick: the easiest way to turn a C on the full-speed collapse into a B is a slower trim speed.",
         "ep": UPF, "ch": "c4", "who": "Frantisek Pavlousek"},
        {"q": "What are folding lines on a paraglider for?",
         "a": "They exist to make the certification collapse land where the norm says it must. The big asymmetric fold is defined as 50 percent of the trailing edge, plus or minus 2.5, at 45 degrees to the open side, marked with stickers. On many wings, and especially two-liners, the pilot cannot pull that shape from the risers, so extra folding lines are fitted for the test.",
         "ep": UPF, "ch": "c5", "who": "Frantisek Pavlousek"},
        {"q": "Is a two-liner paraglider safe for a B pilot?",
         "a": "Michael Nesler, who invented RAST and now builds a B-class two-liner, argues a well-designed two-liner can be safer than a three-liner: with the double A points set far back, the nose deforms under load and the wing pitches forward and speeds up by itself. He even thinks a two-liner would make a good school wing. Niviuk's engineers are more cautious about the A class.",
         "ep": NESLER, "ch": "c9", "who": "Michael Nesler"},
        {"q": "Why do modern paragliders need fewer lines?",
         "a": "Because the profile got thicker. Nesler says wings of forty years ago used sections around 9 to 12 percent of the chord; today's are around 18. A thick section suits the low speeds paragliders fly at, and the extra volume and pressure hold the shape between fewer attachment points. The remaining weakness is the long stretch between the front and rear groups, which can squeeze in manoeuvres.",
         "ep": NESLER, "ch": "c3", "who": "Michael Nesler"},
        {"q": "Are thin crumple protectors like Koroyd safe?",
         "a": "They can pass the vertical drop test and still move in a real crash. Niviuk's engineers explain that if the impact is not vertical, pieces can rotate or slip out of the foam, so they tested their Origami protector at several angles and designed it to lock in place. Veselin Ovcharov's advice: crumple protectors suit good pilots; beginners get broader protection from a classic protector.",
         "ep": NIVIUK, "ch": "c11", "who": "Guillem Batlle & Adrià Grau and Veselin Ovcharov"},
        {"q": "How much glide does a submarine harness add?",
         "a": "Less than the computer suggests. Roman Barthelemy of Supair says simulations showed nearly a full point of glide over a faired pod, but in real flying it is about half a point. Measured drag tells the story: a chair harness is around 23 newtons, a pod with a fairing about 12, and a submarine about 8, so most of the gain comes from leaving the chair.",
         "ep": SKYMATE, "ch": "c6", "who": "Roman Barthelemy"},
        {"q": "What is the Supair Skymate smart harness?",
         "a": "An automatic activation system, inspired by skydiving, that watches the wing through a sensor package in the canopy. Roman Barthelemy says it is tuned to distinguish autorotation from everything else, is primed as soon as it sees a collapse, can release the reserve through two separate systems, and sends a rescue alert over 3G or 4G. For now it works only with Supair wings.",
         "ep": SKYMATE, "ch": "c13", "who": "Roman Barthelemy"},
        {"q": "Can I fly a paraglider harness with kite risers?",
         "a": "Beni Kälin did exactly that, clipping race kite risers to carabiners on a paragliding harness, and says it works surprisingly simply. But it is still a kite: if it collapses it may not reopen, so it is only reasonable at heights you would be willing to fall from. Higher than that, he says, it is definitely not safe. Purpose-built closed-cell soaring wings exist for a reason.",
         "ep": BENI, "ch": "c5", "who": "Beni Kälin"},
        {"q": "Why don't paragliders use closed cells like kites?",
         "a": "They were tried. Beni Kälin says closed cells and air valves that let air in but not out were tested on paragliders years ago and abandoned because they were too dangerous. A closed-cell wing may gain some stability, but he thinks it is good that a paraglider can collapse. Closed-cell soaring wings like the Moustache are marketed for ridge soaring, not thermals.",
         "ep": BENI, "ch": "c12", "who": "Beni Kälin"},
    ],
    "next": {"main": ("know-your-equipment.html", "Know Your Equipment", "Reserves, harness protectors, helmets and carabiners, from the people who design, test and repack them."),
             "cards": [("Listen", "../library.html#s=New%20Technologies", "The full New Technologies series", "7 episodes, 9h 1m, every one transcribed"),
                       ("Related", "flight-mechanics.html", "Flight Mechanics", "What the lines and the trim actually do to the wing"),
                       ("Related", "risk-vs-reward.html", "Risk vs Reward", "How pilots weigh a new wing against their own ability"),
                       ("Ask", "mailto:aninder@paraglidingatlas.com?subject=New%20technology%20question", "A question we did not answer?", "Send it in for the next AMA episode")]},
    },
    "the-dark-side": {
    "layout": 2,
    "kicker": "The Dark Side",
    "h1": "How Safe Is Competition Paragliding, and Who Is Responsible?",
    "lead": "Fatal accidents, the speed of the modern gaggle, a World Championship that went wrong, and the fight over how the sport is governed, heard from racers, organisers, officials and a pilot who survived.",
    "sub": "Five conversations, and not one side of the argument. A veteran racer who puts training first, two World Cup pilots, the delegate behind CIVLRESIGN, two people answering for the governing side, and Nick Neynens on the accident that ended his paragliding.",
    "seo_title": "Competition Paragliding Safety and Governance | Paragliding Atlas",
    "seo_desc": "Why competition paragliding is dangerous, why the gaggle flies full bar, the World Championship accident debate and the CIVL governance dispute, from both sides.",
    "hero_alt": "A competition task drawn as a briefing sheet: start and turnpoint cylinders joined by an orange course line, a goal line with the last leg dashed, gradient wind arrows aloft and sea breeze arrows low down",
    "bands": [
        {"num": "01", "kicker": "Risk", "heading": "Racing raises the stakes, and training comes first",
         "short": "Accidents in competition are not new. What racing adds is the pressure to push harder than you would alone. The first answer from a racer of Bill Belcourt's experience is training, and knowing yourself.",
         "paras": [
             "Bill Belcourt's starting point is blunt: serious accidents have always happened, and racing simply makes them more likely, because pushing further than you normally would is what a race is. He prefers the comparison with downhill mountain biking to the usual Formula One one. Asked what would reduce fatalities, he puts training ahead of everything else, and he is direct that some pilots in the field are racing before they are ready to. Everyone is welcome to race, in his view, but they have to know what they can do and how to stay out of trouble. He rejects the idea that the community treats losses as survival of the fittest: the sports give a great deal, and for the same reason they can take a great deal away.",
             "He is also wary of taking decisions away from pilots. He compares two events a week apart: one where the organisers made many of the calls for the field and saw a serious accident and several close calls, and a hike-and-fly race with weather briefings and no launch-condition rules, where pilots chose for themselves and the only incident was a reserve throw with no injury. He reads that as the power of pilots owning their choices. Nick Neynens, who flew at the top of the sport for fifteen years, adds the other half: doing everything right makes you safer, not safe, and believing accidents only happen to people who make mistakes is a comfort, not a fact."],
         "bold": ["racing simply makes them more likely", "training ahead of everything else", "before they are ready", "owning their choices", "safer, not safe"],
         "chips": [("Bill Belcourt", BELC), ("Nick Neynens", NICK)],
         "figure": None},
        {"num": "02", "kicker": "Speed", "heading": "A slower top class, flown flat out",
         "short": "When open class ended in 2011, top speed came down by around 20 km/h. But the speed that is left is usable, so it is used, and pilots on slower wings in the same gaggle end up pinned at full bar just to keep up.",
         "paras": [
             "Stan Radzikowski, who came to racing after it, describes the open-class era as wings doing 80-plus km/h with trimmers open and the bar pushed, and the top ten pulling 15 to 20 km/h away from anyone who held back. So everyone opened their trimmers, whatever the manual said. Belcourt raced through that period and describes the change that followed: before 2011 pilots were frightened of full bar with trimmers out, and hardly ever used all of it. The CCC wings that replaced open class are a good 20 km/h slower at the top, and precisely because that speed is more usable in more conditions, it gets used, pulley to pulley, much of the time.",
             "The knock-on effect is on everyone else. A typical meet mixes classes, and a pilot on a C or a D who wants to stay in the game with a CCC gaggle flies at their own wing's limit almost all the time, while the CCC pilots can still choose to go slower or faster. In that sense the rule change slowed the sport down overall, but not the experience of the pilot on the slower wing, who has lost the margin."],
         "bold": ["80-plus km/h", "hardly ever used all of it", "20 km/h slower", "it gets used", "at their own wing's limit"],
         "chips": [("Bill Belcourt", BELC), ("Tilen Ceglar & Stan Radzikowski", GAGGLE)],
         "figure": {"img": "kb-the-dark-side-speed", "w": 2400, "h": 620,
                    "alt": "Schematic speed-range bars: an open-class wing before 2011 with much of its range unused, and today a CCC bar mostly used while EN D and EN C bars in the same gaggle are pinned at full bar",
                    "captions": [("Before 2011", "Open-class wings had a great deal of speed, and pilots rarely dared use all of it."),
                                 ("Today", "CCC is slower at the top and used most of the time. Slower wings keeping pace sit at their limit.")],
                    "source_html": 'After Bill Belcourt, <a href="../episodes/bill-belcourt-the-uncomfortable-truth-no-one-is-talking.html#c8">Episode 59, chapter 8</a>, and Stan Radzikowski, <a href="../episodes/insights-from-the-gaggle-with-tilen-ceglar-stan.html#c5">Episode 56, chapter 5</a>. Schematic, not to scale.'}},
        {"num": "03", "kicker": "The Worlds", "heading": "What pilots say went wrong in Brazil",
         "short": "Two pilots who were in the field describe a venue changed months before, a strong sea breeze, a goal field checked the morning after it was set, and a response afterwards that they found wanting. It is their account.",
         "paras": [
             "Tilen Ceglar flew the World Championship at which a Belgian pilot was fatally injured. His account: the event moved to Castelo five months before it started, a site where Brazilian pilots had warned that the sea breeze would make it tricky, and it proved strong, particularly low down. On the day, with a strong northwest wind forecast over mountainous terrain where the landing options were plentiful but not flat, a new goal was set the evening before and only checked by the organisers the next morning. Stan Radzikowski, who has worked closely with organisers, says that is not how a championship normally runs: official landings are usually proven over two or three earlier events.",
             "Both question what happens around an accident as much as before it. Radzikowski describes rescue and medical cover at some venues as of uncertain quality, and says French doctors have repeatedly filled the gap at major events. Ceglar says pilots were told they would receive a feedback survey and, a month later, had not. Radzikowski finds the way pilots are treated after serious accidents distasteful; Ceglar is careful to say that on most occasions activity stops while a helicopter is on its way, but that the minimum standard should put safety first every time."],
         "bold": ["five months before", "sea breeze", "only checked by the organisers the next morning", "two or three earlier events", "feedback survey"],
         "chips": [("Tilen Ceglar & Stan Radzikowski", GAGGLE)],
         "figure": None},
        {"num": "04", "kicker": "Governance", "heading": "The CIVL dispute, from both sides",
         "short": "One side says an institution failed and should acknowledge it by standing down. The other says the accusations are unfounded and the real problem is money. Both were given the microphone here.",
         "paras": [
             "Julien Garcia is France's delegate to CIVL, the FAI commission that runs category one events and sets the sport's competition guidelines, and one of the people behind CIVLRESIGN. He is explicit that it targets no individual: the people on the ground, he says, supported the injured pilot's family and did everything they could. The failure he describes is institutional. Organiser, CIVL and FAI share responsibility, nobody has a defined workflow for a situation like this, and so nobody feels entitled to take it. The movement asks the Bureau to resign and stand for new elections, which he stresses is not a lifetime ban, and insists that an organiser should always say what happened, whatever the liability.",
             "Bill Hughes and Goran Dimiskovski answer for the other side. Hughes disputes the accusations of centralised power and secret deals, says nobody has described what the deals are, and notes that a Bureau member who works for Flymaster was re-elected with that potential conflict disclosed. On proxy voting, he points out there were more proxy votes at the last meeting than members present, and Dimiskovski argues decisions are sounder made face to face than by remote proxy, which he sees as open to manipulation. Both say the underlying problem is money: people hold several roles because the sport is run on amateur budgets, and paid staff, broadcasting and sponsors would change that. Radzikowski asks the question in between: the costs are real, but where do the fees go?"],
         "bold": ["targets no individual", "institutional", "nobody feels entitled to take it", "always say what happened", "potential conflict disclosed", "more proxy votes", "money"],
         "chips": [("Julien Garcia", JULIEN), ("Bill Hughes & Goran Dimiskovski", GOV), ("Tilen Ceglar & Stan Radzikowski", GAGGLE)],
         "figure": None},
        {"num": "05", "kicker": "Aftermath", "heading": "After the crash: rescue, the record and the bill",
         "short": "A helicopter can make things worse. A story told wrongly can too. And the insurance question nobody asks until it matters is what the policy actually pays for.",
         "paras": [
             "Nick Neynens learned to fly in Queensland in 2007 and spent fifteen years flying remote mountains, much of it alone. His accident left him paraplegic, and he later concluded it was less his own fault than he had assumed: it was the rescue helicopter that blew him down the hill. Rotor downwash is heavy, and a pilot lying still with a wing attached can be dragged by it. He talks about what that has meant, about being told what he can no longer do, and about flying sailplanes now, which he calls the better way to fly and the less free one.",
             "Getting the record right matters too. A claim repeated in an earlier episode, that a World Cup task was flown over a dead pilot, was disputed by Bill Hughes, who was competing: a pilot had crashed badly, a helicopter was inbound, the start was minutes away, and the organisers chose to let the field fly away from the area rather than land everyone where the helicopter needed to come in. The pilot's death was only known after everyone had landed, and the next day was taken off in his memory. And on insurance, Neynens' advice is to read what a policy covers: it may or may not include getting you to hospital, the treatment, and getting you home."],
         "bold": ["blew him down the hill", "downwash", "disputed by Bill Hughes", "next day was taken off", "read what a policy covers"],
         "chips": [("Nick Neynens", NICK), ("Bill Hughes & Goran Dimiskovski", GOV)],
         "figure": {"img": "kb-the-dark-side-downwash", "w": 2400, "h": 620,
                    "alt": "Schematic of a helicopter above a slope, its rotor downwash spreading along the ground, and a paraglider still attached to a pilot refilling and dragging downhill",
                    "captions": [("Downwash", "Rotor wash hits the ground and spreads out along the slope."),
                                 ("A wing still attached", "A canopy connected to a pilot who cannot move can refill in that flow and drag them.")],
                    "source_html": 'After Nick Neynens, <a href="../episodes/survived-15-years-of-flying-then-a-rescue-helicopter.html#c4">Episode 68, chapter 4</a>, and <a href="../episodes/survived-15-years-of-flying-then-a-rescue-helicopter.html#c7">chapter 7</a>. Schematic.'}},
    ],
    "quote_band": {"after_band": 3, "img": "kb-the-dark-side-section",
                   "alt": "Four boxes, FAI, CIVL, the organiser and the pilot, joined by dashed lines around a question mark where the responsibility after an accident should sit",
                   "kicker": "Shared responsibility",
                   "quote": "The individuals did what they could. The trouble is institutional: when responsibility is shared between several bodies and nobody has defined who does what, nobody feels entitled to take it.",
                   "who": "Julien Garcia, French CIVL delegate", "cite_ep": JULIEN, "cite_ch": "c3", "cite_label": "Episode 54, paraphrased",
                   "caption": "Organiser, CIVL and FAI all have a part in a category one event. The argument is over where one ends and the next begins."},
    "callout": {"kicker": "Before you travel to fly", "heading": "Read what your insurance pays for",
                "text": "Nick Neynens' advice, from the other side of a serious accident abroad: a policy may or may not cover getting you to hospital, the medical care, and getting you home. Check each one, and any exemption for flying, before you need it. Where he was treated made a large difference to how quickly he was.",
                "ep": NICK, "ch": "c9", "who": "Nick Neynens",
                "numbers": [("3", "", "things to check: the rescue to hospital, the treatment, the journey home")]},
    "takeaways_heading": "Worth remembering",
    "groups": [
        ("Before you race", [
            ("Training comes first", "Belcourt's single answer to fewer fatalities. Some pilots are racing before they are ready.", BELC, "c6", "Bill Belcourt"),
            ("Safer is not safe", "Doing everything right lowers the odds. It does not make accidents something that only happens to others.", NICK, "c4", "Nick Neynens"),
            ("Own the decision", "Belcourt saw pilots who chose for themselves come through a hard event better than a field that was managed.", BELC, "c11", "Bill Belcourt")]),
        ("In the gaggle", [
            ("The pace is set by the fastest wings", "On a C or D in a CCC gaggle you will be at full bar most of the time. That margin is gone.", BELC, "c8", "Bill Belcourt"),
            ("Landings should be proven", "At a championship, official fields are normally checked over earlier events, not the morning of the task.", GAGGLE, "c3", "Stan Radzikowski"),
            ("Ask where the money goes", "The costs of running a meet are real. Radzikowski's point is that pilots are entitled to know.", GAGGLE, "c9", "Stan Radzikowski")]),
        ("After an accident", [
            ("Say what happened", "Garcia's central demand: an organiser should always communicate, whatever the liability.", JULIEN, "c1", "Julien Garcia"),
            ("Downwash can move a pilot", "Neynens was blown down the hill by the rescue helicopter. A wing still attached can drag.", NICK, "c4", "Nick Neynens"),
            ("Check the facts before repeating them", "Hughes, who was there, disputes the story of a task flown over a dead pilot.", GOV, "c2", "Bill Hughes")]),
    ],
    "faq_heading": "Questions these conversations answer",
    "faq": [
        {"q": "Is competition paragliding more dangerous than free flying?",
         "a": "Bill Belcourt, who has raced for decades, says serious accidents are nothing new and that racing makes them more likely, because pushing harder than you would alone is the nature of a race. He compares it with downhill mountain biking rather than Formula One. His view is that the sport's risk does not change, but a race changes how much of it pilots are willing to take.",
         "ep": BELC, "ch": "c2", "who": "Bill Belcourt"},
        {"q": "What is the best way to reduce paragliding fatalities?",
         "a": "Training, ahead of everything else, according to Bill Belcourt. He is direct that some pilots in competitions are racing before they are ready, and that anyone is welcome to race as long as they know their own limits and how to stay out of trouble. He points to climbing, which has no licence to buy gear, as a sport that relies on the same self-knowledge.",
         "ep": BELC, "ch": "c6", "who": "Bill Belcourt"},
        {"q": "Why do competition pilots fly at full speed all the time?",
         "a": "Because the speed is usable. Belcourt says CCC wings, which replaced open class after 2011, are a good 20 km/h slower at the top than the old open-class wings, and that makes full bar usable in more conditions, so it is used much of the time. Pilots on C or D wings in the same gaggle fly at their limit just to keep up, and lose their margin.",
         "ep": BELC, "ch": "c8", "who": "Bill Belcourt"},
        {"q": "What is CIVLRESIGN?",
         "a": "A movement asking the Bureau of CIVL, the FAI commission that governs international paragliding competition, to resign and stand for new elections. Julien Garcia, France's CIVL delegate and one of its backers, says it targets no individual and that resignation is not a lifetime ban. Its aim, in his words, is for the institution to acknowledge a systemic failure and adopt new principles and processes.",
         "ep": JULIEN, "ch": "c2", "who": "Julien Garcia"},
        {"q": "Who is responsible after an accident at a paragliding competition?",
         "a": "That is exactly what is disputed. Julien Garcia argues that the organiser, CIVL and FAI all share responsibility, but no workflow defines who does what when something goes badly wrong, so nobody feels entitled to take it. He stresses that the individuals involved supported the family and did what they could. His demand is that organisers always communicate what happened, whatever the liability.",
         "ep": JULIEN, "ch": "c3", "who": "Julien Garcia"},
        {"q": "Why is proxy voting at CIVL controversial?",
         "a": "Critics say proxies concentrate power in the hands of the same few people. Bill Hughes notes there were more proxy votes than members present at the last meeting, and Goran Dimiskovski argues that decisions made face to face at a plenary are sounder than remote proxies, which he sees as open to manipulation. Both say the deeper issue is that the sport lacks money.",
         "ep": GOV, "ch": "c5", "who": "Bill Hughes & Goran Dimiskovski"},
        {"q": "What went wrong at the paragliding World Championship in Castelo?",
         "a": "In Tilen Ceglar's account, the event was moved to Castelo five months beforehand, a site known for a strong sea breeze, and on the day of the fatal accident a new goal was set the evening before and only checked by organisers the next morning. Stan Radzikowski says official landings are normally proven over several earlier events. This is the pilots' view, not an official finding.",
         "ep": GAGGLE, "ch": "c3", "who": "Tilen Ceglar & Stan Radzikowski"},
        {"q": "Did a World Cup task really fly over a dead pilot?",
         "a": "Bill Hughes, who was competing, says that framing is a gross misrepresentation. A pilot had crashed badly, a helicopter was coming in and the start was minutes away, so organisers let the field fly away from the area rather than land everyone where the helicopter needed space. The death was only known after everyone had landed, and the next day was taken off in memory.",
         "ep": GOV, "ch": "c2", "who": "Bill Hughes"},
        {"q": "Can a rescue helicopter injure a paraglider pilot?",
         "a": "Nick Neynens believes his did. He spent years assuming his accident was his own fault, then concluded it was the rescue helicopter that blew him down the hill. Rotor downwash is strong, and a pilot lying on a slope with a paraglider still attached can be dragged when the wing refills. His accident left him paraplegic; he now flies sailplanes.",
         "ep": NICK, "ch": "c4", "who": "Nick Neynens"},
        {"q": "What should my paragliding insurance cover abroad?",
         "a": "Check three things separately, says Nick Neynens, who was badly hurt flying abroad: whether the policy pays to get you to hospital, whether it pays for the treatment, and whether it pays to get you home, plus any exemption for flying. He was covered at home in Australia, but treatment there would have taken far longer than it did in New Zealand.",
         "ep": NICK, "ch": "c9", "who": "Nick Neynens"},
    ],
    "next": {"main": ("risk-vs-reward.html", "Risk vs Reward", "How pilots decide what a flight is worth, and when to turn back, launch or throw the reserve."),
             "cards": [("Listen", "../library.html#s=The%20Dark%20Side", "The full Dark Side series", "5 episodes, 5h 54m, every one transcribed"),
                       ("Related", "world-cups.html", "World Cups", "Conversations from inside the competition circuit"),
                       ("Related", "new-technologies.html", "New Technologies", "What the certification letter does and does not tell you"),
                       ("Ask", "mailto:aninder@paraglidingatlas.com?subject=Dark%20Side%20question", "A question we did not answer?", "Send it in for the next AMA episode")]},
    },
}
