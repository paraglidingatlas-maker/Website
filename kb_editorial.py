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
}
