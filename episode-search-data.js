// Real episode data (title + YouTube video ID) powering the homepage search.
// Sourced from the bulk YouTube channel export.
const EPISODE_SEARCH_DATA = [
  {
    "title": "How to Thermal Like a Pro: Find, Center & Climb | Paragliding Tutorial with Brett Janaway",
    "video_id": "G-gqUxq0C6Q", "page": "how-to-thermal-like-a-pro-find-center-climb-paragliding"
  },
  {
    "title": "SRS Piedrahita BGD Edition Task 2 Highlights",
    "video_id": "NXUEyPQ3V4E", "page": "srs-piedrahita-bgd-edition-task-2-highlights"
  },
  {
    "title": "Luc Armant talks about The Moment Coefficient, Enzo 3 Certification Debate & Physics of Stability",
    "video_id": "pYzuw5bTIe8", "page": "luc-armant-talks-about-the-moment-coefficient-enzo-3"
  },
  {
    "title": "SRS Piedrahita BGD Edition Task 1 Highlights",
    "video_id": "uCEfssE40u8", "page": "srs-piedrahita-bgd-edition-task-1-highlights"
  },
  {
    "title": "Technical Masterclass by Brett Janaway | Science of Paraglider Trimming,Performance & New Legalities",
    "video_id": "zzcktKfMcUI", "page": "technical-masterclass-by-brett-janaway-science-of"
  },
  {
    "title": "SRS BGD Edition 2026 | Day 1: Registration, Pilots & Peñas de Piedrahíta🎉",
    "video_id": "cuGs7Lk6Dt4", "page": "srs-bgd-edition-2026-day-1-registration-pilots-penas-de"
  },
  {
    "title": "Robert (Robbie) Whittall: 113 mins of Unhinged conversations with The Man Behind Ozone Paragliders",
    "video_id": "aGiisCcG5v8", "page": "robert-whittall-113-mins-of-unhinged-conversations-with"
  },
  {
    "title": "Metacognition: Paragliding's Hidden Psychology with Beni Kalin & Heli Schrempf",
    "video_id": "J5j3Hk_HcFQ", "page": "metacognition-paragliding-s-hidden-psychology-with-beni"
  },
  {
    "title": "The Russell Ogden Interview: Decoding Paragliding Mastery Protocols: Progression, Fear & Competition",
    "video_id": "itpkNQwV438", "page": "the-russell-ogden-interview-decoding-paragliding-mastery"
  },
  {
    "title": "Task 5 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026",
    "video_id": "vPnIYYKcvEg", "page": "task-5-highlights-15th-paragliding-world-cup-super-final"
  },
  {
    "title": "Task 4 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026",
    "video_id": "op1-O01xkH4", "page": "task-4-highlights-15th-paragliding-world-cup-super-final"
  },
  {
    "title": "Task 2 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026",
    "video_id": "7il6yV1vdIc", "page": "task-2-highlights-15th-paragliding-world-cup-super-final"
  },
  {
    "title": "Task 1 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026",
    "video_id": "BRAX1XMU390", "page": "task-1-highlights-15th-paragliding-world-cup-super-final"
  },
  {
    "title": "Highlights Day 1 - PWCA Superfinal 2026",
    "video_id": "FOuAWMeoxs4", "page": "highlights-day-1-pwca-superfinal-2026"
  },
  {
    "title": "Paragliding Physiology & Safety Protocols | Dr Matt Wilkes Explains: Biophysics in the Art of Flight",
    "video_id": "_k2uxEkrN7s", "page": "paragliding-physiology-safety-protocols-dr-matt-wilkes"
  },
  {
    "title": "If you fly in the Himalayas, Alps, or above 3000 mtrs, this episode is for you - ft. Dr Matt Wilkes",
    "video_id": "AvSCngFI7R0", "page": "if-you-fly-in-the-himalayas-alps-or-above-3000-mtrs-this"
  },
  {
    "title": "Cognitive Bias of Dunning Kruger Effect in Paragliding | Explained by Beni Kalin & Heli Schrempf",
    "video_id": "p_HpeN5x7dE", "page": "cognitive-bias-of-dunning-kruger-effect-in-paragliding"
  },
  {
    "title": "Sports Psychology for Paragliding: Train Your Mind to Fly Better with Yvonne Dathe",
    "video_id": "mYG80ZiHIyo", "page": "sports-psychology-for-paragliding-train-your-mind-to-fly"
  },
  {
    "title": "From Cuba to Socotra: Inside the World’s Most Unique Paragliding Tours",
    "video_id": "ylj8CZgqLyM", "page": "from-cuba-to-socotra-inside-the-worlds-most-unique"
  },
  {
    "title": "How to Fly With Your Dog | Explained by Shams",
    "video_id": "yNNqjTpQkRQ", "page": "how-to-fly-with-your-dog-explained-by-shams"
  },
  {
    "title": "Survived 15 Years of Flying Then a Rescue Helicopter Changed Everything | A Talk With Nick Neynes",
    "video_id": "BceEzHgylwo", "page": "survived-15-years-of-flying-then-a-rescue-helicopter"
  },
  {
    "title": "From Tents to Trophies: Understanding Acro Champion's Mindset on Ego, Glory & Drugs | Luke De Weert",
    "video_id": "Kdd1R8x36vU", "page": "from-tents-to-trophies-understanding-acro-champion-s"
  },
  {
    "title": "Tom Lolies Explains The Science Of Wing Design and Evolution from ENC to  CSC",
    "video_id": "iurDFHlgJjI", "page": "tom-lolies-explains-the-science-of-wing-design-and"
  },
  {
    "title": "The Art of Capturing Human Flight | Jake Holland's Guide to Filming Passion Projects in Paragliding",
    "video_id": "3ZySapU_YLI", "page": "the-art-of-capturing-human-flight-jake-holland-s-guide-to"
  },
  {
    "title": "Scoring in Paragliding Competitions: A New Pilot's Guide to the GAP Formula & Strategy | Joerg Ewald",
    "video_id": "CYVrlWuls6o", "page": "scoring-in-paragliding-competitions-a-new-pilot-s-guide-to"
  },
  {
    "title": "Can we Steer a Round Reserve Parachute? Urs Haari Answers!",
    "video_id": "wvJWd8lVZzc", "page": "can-we-steer-a-round-reserve-parachute-urs-haari-answers"
  },
  {
    "title": "Watch this Before you Buy a Paragliding Harness | A Talk with Zsolt Ero",
    "video_id": "kSoFk23TuX0", "page": "watch-this-before-you-buy-a-paragliding-harness-a-talk"
  },
  {
    "title": "The Inside Story of Sports Racing Series (SRS) by Brett Janaway",
    "video_id": "i9z4MyL6KgQ", "page": "the-inside-story-of-sports-racing-series-by-brett-janaway"
  },
  {
    "title": "The Unfiltered Truth About Paragliding Governance: with Bill Hughes & Goran Dimiskovski",
    "video_id": "VmaPERBK-lo", "page": "the-unfiltered-truth-about-paragliding-governance-with"
  },
  {
    "title": "Bill Belcourt: The Uncomfortable Truth No One is Talking about in the Current Safety Paradox",
    "video_id": "YyGdTDXC1Lc", "page": "bill-belcourt-the-uncomfortable-truth-no-one-is-talking"
  },
  {
    "title": "Bruce Goldsmith explains MRT scoring system and its impact on Paragliding Competitions",
    "video_id": "nlgbMKLNNk4", "page": "bruce-goldsmith-explains-mrt-scoring-system-and-its-impact"
  },
  {
    "title": "Luc Armant talks about Debunking the Myths and Upgrading Enzo 3",
    "video_id": "xNMHk_8qbzo", "page": "luc-armant-talks-about-debunking-the-myths-and-upgrading"
  },
  {
    "title": "Insights From The Gaggle with Tilen Ceglar & Stan Radzikowski",
    "video_id": "jdiYdzJ9U5w", "page": "insights-from-the-gaggle-with-tilen-ceglar-stan"
  },
  {
    "title": "Pal Takats on Challenges, Change & The Future of Paragliding ",
    "video_id": "FvIZpqydhyo", "page": "pal-takats-on-challenges-change-the-future-of-paragliding"
  },
  {
    "title": "What is #CIVLRESIGN with Julien Garcia",
    "video_id": "jSfQYxxbaWk", "page": "what-is-civlresign-with-julien-garcia"
  },
  {
    "title": "Understanding Skymate: Paragliding Worlds First AI Driven Smart Harness System with Roman Barthelemy",
    "video_id": "S2wiY4DO_TU", "page": "understanding-skymate-paragliding-worlds-first-ai-driven"
  },
  {
    "title": "The Resilience Equation: Erlend Ukvitne’s Unrelenting Path to X-Alps and the Brink of a World Record",
    "video_id": "rFC56EjtXCY", "page": "the-resilience-equation-erlend-ukvitnes-unrelenting-path"
  },
  {
    "title": "Consequence Over Probability: Will Gadd on Why True Safety Lies in Clarity",
    "video_id": "VqkYy6YhXcY", "page": "consequence-over-probability-will-gadd-on-why-true-safety"
  },
  {
    "title": "Why Paragliding’s Safety Future Looks Different: RAST Inventor Michael Nesler & the LeelooX Effect",
    "video_id": "YGU7-ctBYYE", "page": "why-paraglidings-safety-future-looks-different-rast"
  },
  {
    "title": "The Silent Mind In Screaming Winds : Unlocking Peak Focus To Attain Flow State In Paragliding",
    "video_id": "N4OGIzYNnl0", "page": "the-silent-mind-in-screaming-winds-unlocking-peak-focus-to"
  },
  {
    "title": "Meteorology 101 A beginner’s Guide to Understanding Weather Apps and Decoding Endless Forecasting...",
    "video_id": "DIHf30B2NoY", "page": "meteorology-101-a-beginners-guide-to-understanding-weather"
  },
  {
    "title": "Urs Haari: The Real Truth About Reserve Parachutes : A Paragliding Survival Guide",
    "video_id": "EttlenmzWHM", "page": "urs-haari-the-real-truth-about-reserve-parachutes-a"
  },
  {
    "title": "Shane Tighe’s Road to X-Alps : Engineering Conquests In The Sky from Australia’s Flatlands to the...",
    "video_id": "cnizMhvNQrM", "page": "shane-tighes-road-to-x-alps-engineering-conquests-in-the"
  },
  {
    "title": "Aljaž Valič : 777 : Paragliding’s Slovenian Mavericks Redefining the EN B Class And Elevating Fre...",
    "video_id": "78PaTvxRWJ0", "page": "aljaz-valic-777-paraglidings-slovenian-mavericks"
  },
  {
    "title": "Sandrine Roy : Vol Biv & Freedom Unfiltered : A Human-Powered Odyssey By Paragliding, Biking & Sa...",
    "video_id": "qZRa_Ozz0Hg", "page": "sandrine-roy-vol-biv-freedom-unfiltered-a-human-powered"
  },
  {
    "title": "Alain Zoller: The Science of EN Certifications : How Work Group 6 Shaped Paragliding Testing, Inn...",
    "video_id": "CBxyezZ-UOw", "page": "alain-zoller-the-science-of-en-certifications-how-work"
  },
  {
    "title": "Ziad Bassil : Finest Paragliding Reviews & Superpower of Changing Wings as A Human",
    "video_id": "i-QoHo0ZaPU", "page": "ziad-bassil-finest-paragliding-reviews-superpower-of"
  },
  {
    "title": "Eddie Colfox : Storytime : Chasing Adventure With the Real OG John Silvester & 3 Decades of Makin...",
    "video_id": "ebwdsVgopnU", "page": "eddie-colfox-storytime-chasing-adventure-with-the-real-og"
  },
  {
    "title": "​Ashutosh Chopra: Identifying Passion Vs Obsession: An Aviator’s Approach to Overcoming Adversity...",
    "video_id": "jMVTzRFPWNw", "page": "ashutosh-chopra-identifying-passion-vs-obsession-an"
  },
  {
    "title": "Kinga Masztalerz: Building a Healthy Relationship with the Skies: How to Master Fear, Build Resil...",
    "video_id": "pFxe7oZTH2E", "page": "kinga-masztalerz-building-a-healthy-relationship-with-the"
  },
  {
    "title": "Helmut Schrempf : Modernizing SIV Courses: How This New Training Method Can Help You Master Glide...",
    "video_id": "wTfS5kv1t9M", "page": "helmut-schrempf-modernizing-siv-courses-how-this-new"
  },
  {
    "title": "A Note of Thanks 😊",
    "video_id": "B9mx2zGLk0I"
  },
  {
    "title": "Storytellers : Marko Milutinovic (Mid-Air Collision)",
    "video_id": "T1pR130Umkk", "page": "storytellers-marko-milutinovic"
  },
  {
    "title": "Art Of Flight in Norwegian Skies",
    "video_id": "l_iHET2H5E0"
  },
  {
    "title": "New Technologies 5 : Frantisek Pavlousek (UP Paragliders)",
    "video_id": "vmnrTFbu6vg", "page": "new-technologies-5-frantisek-pavlousek-2"
  },
  {
    "title": "Flying & Filming 3 : Andreas Lattner (hochzwei.media)",
    "video_id": "yUsfGCfI_30", "page": "flying-filming-3-andreas-lattner"
  },
  {
    "title": "Flying & Filming 2 : Benjamin Kellet",
    "video_id": "OiertfSq-6o", "page": "flying-filming-2-benjamin-kellet"
  },
  {
    "title": "Risk Vs Reward 5 : Gabriel Orsini (partytillimpact)",
    "video_id": "DmyYSA6NeMw", "page": "risk-vs-reward-5-gabriel-orsini"
  },
  {
    "title": "Helmet Safety : Christian Ciech : ICARO 2000 [1st Anniversary Edition]",
    "video_id": "fKWV5YR8MRE", "page": "helmet-safety-christian-ciech-icaro-2000"
  },
  {
    "title": "Risk Vs Reward 4 : Raúl Rodríguez",
    "video_id": "MFYb9KmT15s", "page": "risk-vs-reward-4-raul-rodriguez"
  },
  {
    "title": "Brand Stories : Neo : Eric Roussel",
    "video_id": "9GfZcM3P3jY", "page": "brand-stories-neo-eric-roussel"
  },
  {
    "title": "Carabiner Fatigue : Finsterwalder & Charly (whitepaper)",
    "video_id": "QPkIlI2qG5A", "page": "carabiner-fatigue-finsterwalder-charly"
  },
  {
    "title": "Bird’s-Eye View of Oslo: Stunning Nordic Cityscape: Part 2",
    "video_id": "7ezjN2F247A"
  },
  {
    "title": "Flying & Filming 1 : Benjamin Jordan",
    "video_id": "L2MrAoec24I", "page": "flying-filming-1-benjamin-jordan"
  },
  {
    "title": "Living The Dream : Benjamin Jordan",
    "video_id": "bDJ1zRG90cs", "page": "living-the-dream-benjamin-jordan"
  },
  {
    "title": "Risk Vs Reward 3 : Manfred Ruhmer",
    "video_id": "njoPDwe457w", "page": "risk-vs-reward-3-manfred-ruhmer"
  },
  {
    "title": "Just another day in Paradise ✨😍 #oslo #paragliding #norway",
    "video_id": "XHIQS658G24"
  },
  {
    "title": "Risk Vs Reward 2 : Subir Sidhu",
    "video_id": "J8visA4lxys", "page": "risk-vs-reward-2-subir-sidhu"
  },
  {
    "title": "Risk Vs Reward 1 : Philipp Zellner",
    "video_id": "md9ls8OtBiA", "page": "risk-vs-reward-1-philipp-zellner"
  },
  {
    "title": "Bird’s-Eye View of Oslo: Stunning Nordic Cityscape",
    "video_id": "Hei3hWbkbwg"
  },
  {
    "title": "New Technologies 4 : Veselin Ovcharov (Fly The Earth)",
    "video_id": "zEnjmp9hrlE", "page": "new-technologies-4-veselin-ovcharov"
  },
  {
    "title": "New Technologies 2 : Guillem Batlle & Adrià Grau (Niviuk Paragliders)",
    "video_id": "MxwM1lJEVIU", "page": "new-technologies-2-guillem-batlle-adria-grau"
  },
  {
    "title": "New Technologies 1 : Beni Kälin (speedflyingschool.com)",
    "video_id": "aFO5Uk5BX9s", "page": "new-technologies-1-beni-kalin"
  },
  {
    "title": "PWC Lifestyle: Klaudia Bulgakow",
    "video_id": "ZjSojM_Ao0U", "page": "pwc-lifestyle-klaudia-bulgakow"
  },
  {
    "title": "PWCA: Goran Dimiskovski",
    "video_id": "l1gmplS02FI", "page": "pwca-goran-dimiskovski"
  },
  {
    "title": "Pre PWC Kenya: Nikolay Yotov",
    "video_id": "UVLF8l0qFlA", "page": "pre-pwc-kenya-nikolay-yotov"
  },
  {
    "title": "Navigating Panchgani (Pre PWC India) : Vistasp Kharas",
    "video_id": "0VPg7TZ9hK0", "page": "navigating-panchgani-vistasp-kharas"
  },
  {
    "title": "AMA #1",
    "video_id": "zKabIDewXn0", "page": "ama-1"
  },
  {
    "title": "Navigating Australia : Godfrey Wenness",
    "video_id": "xXSGK8oB4Oc", "page": "navigating-australia-godfrey-wenness"
  },
  {
    "title": "Sky Gods : Flying to Win : Honorin Hamard",
    "video_id": "QmprO-5qkR8", "page": "sky-gods-flying-to-win-honorin-hamard"
  },
  {
    "title": "Sky Gods : Flying 8000ers : Antoine Girard",
    "video_id": "Q2oTFoQcrGw", "page": "sky-gods-flying-8000ers-antoine-girard"
  },
  {
    "title": "Navigating India: Jigish Gohil (Bonus Ep)",
    "video_id": "_apo1PNabZI", "page": "navigating-india-jigish-gohil"
  },
  {
    "title": "Navigating India: Eddie Colfox",
    "video_id": "TO6gW69d7YE", "page": "navigating-india-eddie-colfox"
  },
  {
    "title": "Navigating Colombia: Pal Takats",
    "video_id": "kOgDYSvfUuo", "page": "navigating-colombia-pal-takats"
  },
  {
    "title": "Touch The Sky With Glory",
    "video_id": "MLNGvJHrWQY"
  }
];
