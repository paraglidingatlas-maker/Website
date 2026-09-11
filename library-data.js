// Library data for library.html.
// Order matches the YouTube channel export, which is newest first.
//
// SOURCE OF EACH PLACEMENT:
//   no marker  = taken from the Knowledge Base series page the episode already sits on
//   ** review  = not yet on any Knowledge Base page, assigned against the series description
//
// To move an episode, edit its topic value. Valid topics are the keys of LIB_TOPICS.

const LIB_TOPICS = {
  "Navigators":                  "Core series",
  "Sky Gods":                    "Core series",
  "Living the Dream":            "Core series",
  "World Cups":                  "Competitions",
  "Risk vs Reward":              "Competitions",
  "Resources, Tools and Tips":   "Competitions",
  "Weather Patterns":            "Meteorology",
  "Brand Stories":               "Industry",
  "Storytellers":                "Industry",
  "The Dark Side":               "Industry",
  "Flight Mechanics":            "Technical",
  "New Technologies":            "Technical",
  "Know Your Equipment":         "Technical",
};

const LIB_FEATURED = ["Risk vs Reward", "Know Your Equipment", "Sky Gods"];

// Left out of the library on purpose:
//   A Note of Thanks 😊  (A Note of Thanks: housekeeping, not an episode)
//   Art Of Flight in Norwegian Skies  (cinematic reel, no series fits)
//   Bird’s-Eye View of Oslo: Stunning Nordic Cityscape: Part 2  (cinematic reel, no series fits)
//   Just another day in Paradise ✨😍 #oslo #paragliding #norway  (short scenic clip, no series fits)
//   Bird’s-Eye View of Oslo: Stunning Nordic Cityscape  (cinematic reel, no series fits)
//   Touch The Sky With Glory  (show trailer, not an episode)

const LIB_EPISODES = [
  { order: 0, id: "G-gqUxq0C6Q", page: "how-to-thermal-like-a-pro-find-center-climb-paragliding", topic: "Flight Mechanics", title: "How to Thermal Like a Pro: Find, Center & Climb | Paragliding Tutorial with Brett Janaway" },   // ** review
  { order: 1, id: "NXUEyPQ3V4E", page: "srs-piedrahita-bgd-edition-task-2-highlights", topic: "World Cups", title: "SRS Piedrahita BGD Edition Task 2 Highlights" },   // ** review
  { order: 2, id: "pYzuw5bTIe8", page: "luc-armant-talks-about-the-moment-coefficient-enzo-3", topic: "Flight Mechanics", title: "Luc Armant talks about The Moment Coefficient, Enzo 3 Certification Debate & Physics of Stability" },   // ** review
  { order: 3, id: "uCEfssE40u8", page: "srs-piedrahita-bgd-edition-task-1-highlights", topic: "World Cups", title: "SRS Piedrahita BGD Edition Task 1 Highlights" },   // ** review
  { order: 4, id: "zzcktKfMcUI", page: "technical-masterclass-by-brett-janaway-science-of", topic: "Know Your Equipment", title: "Technical Masterclass by Brett Janaway | Science of Paraglider Trimming,Performance & New Legalities" },   // ** review
  { order: 5, id: "cuGs7Lk6Dt4", page: "srs-bgd-edition-2026-day-1-registration-pilots-penas-de", topic: "World Cups", title: "SRS BGD Edition 2026 | Day 1: Registration, Pilots & Pe\u00f1as de Piedrah\u00edta\ud83c\udf89" },   // ** review
  { order: 6, id: "aGiisCcG5v8", page: "robert-whittall-113-mins-of-unhinged-conversations-with", topic: "Brand Stories", title: "Robert (Robbie) Whittall: 113 mins of Unhinged conversations with The Man Behind Ozone Paragliders" },   // ** review
  { order: 7, id: "J5j3Hk_HcFQ", page: "metacognition-paragliding-s-hidden-psychology-with-beni", topic: "Risk vs Reward", title: "Metacognition: Paragliding's Hidden Psychology with Beni Kalin & Heli Schrempf" },   // ** review
  { order: 8, id: "itpkNQwV438", page: "the-russell-ogden-interview-decoding-paragliding-mastery", topic: "Sky Gods", title: "The Russell Ogden Interview: Decoding Paragliding Mastery Protocols: Progression, Fear & Competition" },   // ** review
  { order: 9, id: "vPnIYYKcvEg", page: "task-5-highlights-15th-paragliding-world-cup-super-final", topic: "World Cups", title: "Task 5 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 10, id: "op1-O01xkH4", page: "task-4-highlights-15th-paragliding-world-cup-super-final", topic: "World Cups", title: "Task 4 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 11, id: "7il6yV1vdIc", page: "task-2-highlights-15th-paragliding-world-cup-super-final", topic: "World Cups", title: "Task 2 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 12, id: "BRAX1XMU390", page: "task-1-highlights-15th-paragliding-world-cup-super-final", topic: "World Cups", title: "Task 1 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 13, id: "FOuAWMeoxs4", page: "highlights-day-1-pwca-superfinal-2026", topic: "World Cups", title: "Highlights Day 1 - PWCA Superfinal 2026" },   // ** review
  { order: 14, id: "_k2uxEkrN7s", page: "paragliding-physiology-safety-protocols-dr-matt-wilkes", topic: "Risk vs Reward", title: "Paragliding Physiology & Safety Protocols | Dr Matt Wilkes Explains: Biophysics in the Art of Flight" },   // ** review
  { order: 15, id: "AvSCngFI7R0", page: "if-you-fly-in-the-himalayas-alps-or-above-3000-mtrs-this", topic: "Risk vs Reward", title: "If you fly in the Himalayas, Alps, or above 3000 mtrs, this episode is for you - ft. Dr Matt Wilkes" },   // ** review
  { order: 16, id: "p_HpeN5x7dE", page: "cognitive-bias-of-dunning-kruger-effect-in-paragliding", topic: "Risk vs Reward", title: "Cognitive Bias of Dunning Kruger Effect in Paragliding | Explained by Beni Kalin & Heli Schrempf" },   // ** review
  { order: 17, id: "mYG80ZiHIyo", page: "sports-psychology-for-paragliding-train-your-mind-to-fly", topic: "Resources, Tools and Tips", title: "Sports Psychology for Paragliding: Train Your Mind to Fly Better with Yvonne Dathe" },
  { order: 18, id: "ylj8CZgqLyM", page: "from-cuba-to-socotra-inside-the-worlds-most-unique", topic: "Living the Dream", title: "From Cuba to Socotra: Inside the World\u2019s Most Unique Paragliding Tours" },
  { order: 19, id: "yNNqjTpQkRQ", page: "how-to-fly-with-your-dog-explained-by-shams", topic: "Living the Dream", title: "How to Fly With Your Dog | Explained by Shams" },
  { order: 20, id: "BceEzHgylwo", page: "survived-15-years-of-flying-then-a-rescue-helicopter", topic: "The Dark Side", title: "Survived 15 Years of Flying Then a Rescue Helicopter Changed Everything | A Talk With Nick Neynes" },
  { order: 21, id: "Kdd1R8x36vU", page: "from-tents-to-trophies-understanding-acro-champion-s", topic: "World Cups", title: "From Tents to Trophies: Understanding Acro Champion's Mindset on Ego, Glory & Drugs | Luke De Weert" },
  { order: 22, id: "iurDFHlgJjI", page: "tom-lolies-explains-the-science-of-wing-design-and", topic: "Flight Mechanics", title: "Tom Lolies Explains The Science Of Wing Design and Evolution from ENC to  CSC" },
  { order: 23, id: "3ZySapU_YLI", page: "the-art-of-capturing-human-flight-jake-holland-s-guide-to", topic: "Resources, Tools and Tips", title: "The Art of Capturing Human Flight | Jake Holland's Guide to Filming Passion Projects in Paragliding" },
  { order: 24, id: "CYVrlWuls6o", page: "scoring-in-paragliding-competitions-a-new-pilot-s-guide-to", topic: "World Cups", title: "Scoring in Paragliding Competitions: A New Pilot's Guide to the GAP Formula & Strategy | Joerg Ewald" },
  { order: 25, id: "wvJWd8lVZzc", page: "can-we-steer-a-round-reserve-parachute-urs-haari-answers", topic: "Know Your Equipment", title: "Can we Steer a Round Reserve Parachute? Urs Haari Answers!" },
  { order: 26, id: "kSoFk23TuX0", page: "watch-this-before-you-buy-a-paragliding-harness-a-talk", topic: "Know Your Equipment", title: "Watch this Before you Buy a Paragliding Harness | A Talk with Zsolt Ero" },
  { order: 27, id: "i9z4MyL6KgQ", page: "the-inside-story-of-sports-racing-series-by-brett-janaway", topic: "World Cups", title: "The Inside Story of Sports Racing Series (SRS) by Brett Janaway" },
  { order: 28, id: "VmaPERBK-lo", page: "the-unfiltered-truth-about-paragliding-governance-with", topic: "The Dark Side", title: "The Unfiltered Truth About Paragliding Governance: with Bill Hughes & Goran Dimiskovski" },
  { order: 29, id: "YyGdTDXC1Lc", page: "bill-belcourt-the-uncomfortable-truth-no-one-is-talking", topic: "The Dark Side", title: "Bill Belcourt: The Uncomfortable Truth No One is Talking about in the Current Safety Paradox" },
  { order: 30, id: "nlgbMKLNNk4", page: "bruce-goldsmith-explains-mrt-scoring-system-and-its-impact", topic: "World Cups", title: "Bruce Goldsmith explains MRT scoring system and its impact on Paragliding Competitions" },
  { order: 31, id: "xNMHk_8qbzo", page: "luc-armant-talks-about-debunking-the-myths-and-upgrading", topic: "Flight Mechanics", title: "Luc Armant talks about Debunking the Myths and Upgrading Enzo 3" },
  { order: 32, id: "jdiYdzJ9U5w", page: "insights-from-the-gaggle-with-tilen-ceglar-stan", topic: "The Dark Side", title: "Insights From The Gaggle with Tilen Ceglar & Stan Radzikowski" },
  { order: 33, id: "FvIZpqydhyo", page: "pal-takats-on-challenges-change-the-future-of-paragliding", topic: "Brand Stories", title: "Pal Takats on Challenges, Change & The Future of Paragliding " },
  { order: 34, id: "jSfQYxxbaWk", page: "what-is-civlresign-with-julien-garcia", topic: "The Dark Side", title: "What is #CIVLRESIGN with Julien Garcia" },
  { order: 35, id: "S2wiY4DO_TU", page: "understanding-skymate-paragliding-worlds-first-ai-driven", topic: "New Technologies", title: "Understanding Skymate: Paragliding Worlds First AI Driven Smart Harness System with Roman Barthelemy" },
  { order: 36, id: "rFC56EjtXCY", page: "the-resilience-equation-erlend-ukvitnes-unrelenting-path", topic: "World Cups", title: "The Resilience Equation: Erlend Ukvitne\u2019s Unrelenting Path to X-Alps and the Brink of a World Record" },
  { order: 37, id: "VqkYy6YhXcY", page: "consequence-over-probability-will-gadd-on-why-true-safety", topic: "Risk vs Reward", title: "Consequence Over Probability: Will Gadd on Why True Safety Lies in Clarity" },
  { order: 38, id: "YGU7-ctBYYE", page: "why-paraglidings-safety-future-looks-different-rast", topic: "New Technologies", title: "Why Paragliding\u2019s Safety Future Looks Different: RAST Inventor Michael Nesler & the LeelooX Effect" },
  { order: 39, id: "N4OGIzYNnl0", page: "the-silent-mind-in-screaming-winds-unlocking-peak-focus-to", topic: "Resources, Tools and Tips", title: "The Silent Mind In Screaming Winds : Unlocking Peak Focus To Attain Flow State In Paragliding" },
  { order: 40, id: "DIHf30B2NoY", page: "meteorology-101-a-beginners-guide-to-understanding-weather", topic: "Weather Patterns", title: "Meteorology 101: A beginner\u2019s Guide to Understanding Weather Apps and Decoding Endless Forecasting Options" },
  { order: 41, id: "EttlenmzWHM", page: "urs-haari-the-real-truth-about-reserve-parachutes-a", topic: "Know Your Equipment", title: "Urs Haari: The Real Truth About Reserve Parachutes : A Paragliding Survival Guide" },
  { order: 42, id: "cnizMhvNQrM", page: "shane-tighes-road-to-x-alps-engineering-conquests-in-the", topic: "World Cups", title: "Shane Tighe\u2019s Road to X-Alps : Engineering Conquests In The Sky from Australia\u2019s Flatlands to the Pinnacle of Hike and Fly" },
  { order: 43, id: "78PaTvxRWJ0", page: "aljaz-valic-777-paraglidings-slovenian-mavericks", topic: "Flight Mechanics", title: "Alja\u017e Vali\u010d : 777 : Paragliding\u2019s Slovenian Mavericks Redefining the EN B Class And Elevating Free Flight Performance" },
  { order: 44, id: "qZRa_Ozz0Hg", page: "sandrine-roy-vol-biv-freedom-unfiltered-a-human-powered", topic: "Living the Dream", title: "Sandrine Roy : Vol Biv & Freedom Unfiltered : A Human-Powered Odyssey By Paragliding, Biking & Sailing Around The Globe" },
  { order: 45, id: "CBxyezZ-UOw", page: "alain-zoller-the-science-of-en-certifications-how-work", topic: "Flight Mechanics", title: "Alain Zoller: The Science of EN Certifications : How Work Group 6 Shaped Paragliding Testing, Innovation & Safety" },
  { order: 46, id: "i-QoHo0ZaPU", page: "ziad-bassil-finest-paragliding-reviews-superpower-of", topic: "Resources, Tools and Tips", title: "Ziad Bassil : Finest Paragliding Reviews & Superpower of Changing Wings as A Human" },
  { order: 47, id: "ebwdsVgopnU", page: "eddie-colfox-storytime-chasing-adventure-with-the-real-og", topic: "Storytellers", title: "Eddie Colfox : Storytime : Chasing Adventure With the Real OG John Silvester & 3 Decades of Making Memories Across The Globe" },
  { order: 48, id: "jMVTzRFPWNw", page: "ashutosh-chopra-identifying-passion-vs-obsession-an", topic: "Resources, Tools and Tips", title: "Ashutosh Chopra: Identifying Passion Vs Obsession: An Aviator\u2019s Approach to Overcoming Adversity, Rebuilding Trust and Finding Joy in the Skies" },
  { order: 49, id: "pFxe7oZTH2E", page: "kinga-masztalerz-building-a-healthy-relationship-with-the", topic: "Risk vs Reward", title: "Kinga Masztalerz: Building a Healthy Relationship with the Skies: How to Master Fear, Build Resilience & Find Joy Through Paragliding" },
  { order: 50, id: "wTfS5kv1t9M", page: "helmut-schrempf-modernizing-siv-courses-how-this-new", topic: "Flight Mechanics", title: "Helmut Schrempf : Modernizing SIV Courses: How This New Training Method Can Help You Master Glider Control and Improve Paragliding Safety" },
  { order: 52, id: "T1pR130Umkk", page: "storytellers-marko-milutinovic", topic: "Storytellers", title: "Storytellers : Marko Milutinovic (Mid-Air Collision)" },
  { order: 55, id: "yUsfGCfI_30", page: "flying-filming-3-andreas-lattner", topic: "Resources, Tools and Tips", title: "Flying & Filming 3 : Andreas Lattner (hochzwei.media)" },
  { order: 56, id: "OiertfSq-6o", page: "flying-filming-2-benjamin-kellet", topic: "Resources, Tools and Tips", title: "Flying & Filming 2 : Benjamin Kellet" },
  { order: 57, id: "DmyYSA6NeMw", page: "risk-vs-reward-5-gabriel-orsini", topic: "Risk vs Reward", title: "Risk Vs Reward 5 : Gabriel Orsini (partytillimpact)" },
  { order: 58, id: "fKWV5YR8MRE", page: "helmet-safety-christian-ciech-icaro-2000", topic: "Know Your Equipment", title: "Helmet Safety : Christian Ciech : ICARO 2000 [1st Anniversary Edition]" },
  { order: 59, id: "MFYb9KmT15s", page: "risk-vs-reward-4-raul-rodriguez", topic: "Risk vs Reward", title: "Risk Vs Reward 4 : Ra\u00fal Rodr\u00edguez" },
  { order: 60, id: "9GfZcM3P3jY", page: "brand-stories-neo-eric-roussel", topic: "Brand Stories", title: "Brand Stories : Neo : Eric Roussel" },
  { order: 61, id: "QPkIlI2qG5A", page: "carabiner-fatigue-finsterwalder-charly", topic: "Know Your Equipment", title: "Carabiner Fatigue : Finsterwalder & Charly (whitepaper)" },
  { order: 63, id: "L2MrAoec24I", page: "flying-filming-1-benjamin-jordan", topic: "Resources, Tools and Tips", title: "Flying & Filming 1 : Benjamin Jordan" },
  { order: 64, id: "bDJ1zRG90cs", page: "living-the-dream-benjamin-jordan", topic: "Living the Dream", title: "Living The Dream : Benjamin Jordan" },
  { order: 65, id: "njoPDwe457w", page: "risk-vs-reward-3-manfred-ruhmer", topic: "Risk vs Reward", title: "Risk Vs Reward 3 : Manfred Ruhmer" },
  { order: 67, id: "J8visA4lxys", page: "risk-vs-reward-2-subir-sidhu", topic: "Risk vs Reward", title: "Risk Vs Reward 2 : Subir Sidhu" },
  { order: 68, id: "md9ls8OtBiA", page: "risk-vs-reward-1-philipp-zellner", topic: "Risk vs Reward", title: "Risk Vs Reward 1 : Philipp Zellner" },
  { order: 70, id: "zEnjmp9hrlE", page: "new-technologies-4-veselin-ovcharov", topic: "New Technologies", title: "New Technologies 4 : Veselin Ovcharov (Fly The Earth)" },
  { order: 71, id: "MxwM1lJEVIU", page: "new-technologies-2-guillem-batlle-adria-grau", topic: "New Technologies", title: "New Technologies 2 : Guillem Batlle & Adri\u00e0 Grau (Niviuk Paragliders)" },
  { order: 72, id: "aFO5Uk5BX9s", page: "new-technologies-1-beni-kalin", topic: "New Technologies", title: "New Technologies 1 : Beni K\u00e4lin (speedflyingschool.com)" },
  { order: 73, id: "ZjSojM_Ao0U", page: "pwc-lifestyle-klaudia-bulgakow", topic: "World Cups", title: "PWC Lifestyle: Klaudia Bulgakow" },
  { order: 74, id: "l1gmplS02FI", page: "pwca-goran-dimiskovski", topic: "World Cups", title: "PWCA: Goran Dimiskovski" },   // ** review
  { order: 75, id: "UVLF8l0qFlA", page: "pre-pwc-kenya-nikolay-yotov", topic: "Navigators", title: "Pre PWC Kenya: Nikolay Yotov" },
  { order: 76, id: "0VPg7TZ9hK0", page: "navigating-panchgani-vistasp-kharas", topic: "Navigators", title: "Navigating Panchgani (Pre PWC India) : Vistasp Kharas" },
  { order: 77, id: "zKabIDewXn0", page: "ama-1", topic: "Resources, Tools and Tips", title: "AMA #1" },
  { order: 78, id: "xXSGK8oB4Oc", page: "navigating-australia-godfrey-wenness", topic: "Navigators", title: "Navigating Australia : Godfrey Wenness" },
  { order: 79, id: "QmprO-5qkR8", page: "sky-gods-flying-to-win-honorin-hamard", topic: "Sky Gods", title: "Sky Gods : Flying to Win : Honorin Hamard" },
  { order: 80, id: "Q2oTFoQcrGw", page: "sky-gods-flying-8000ers-antoine-girard", topic: "Sky Gods", title: "Sky Gods : Flying 8000ers : Antoine Girard" },
  { order: 81, id: "_apo1PNabZI", page: "navigating-india-jigish-gohil", topic: "Navigators", title: "Navigating India: Jigish Gohil (Bonus Ep)" },
  { order: 82, id: "TO6gW69d7YE", page: "navigating-india-eddie-colfox", topic: "Navigators", title: "Navigating India: Eddie Colfox" },
  { order: 83, id: "kOgDYSvfUuo", page: "navigating-colombia-pal-takats", topic: "Navigators", title: "Navigating Colombia: Pal Takats" },
];
