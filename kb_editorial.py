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
}
