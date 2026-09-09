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
  { order: 0, id: "G-gqUxq0C6Q", topic: "Flight Mechanics", title: "How to Thermal Like a Pro: Find, Center & Climb | Paragliding Tutorial with Brett Janaway" },   // ** review
  { order: 1, id: "NXUEyPQ3V4E", topic: "World Cups", title: "SRS Piedrahita BGD Edition Task 2 Highlights" },   // ** review
  { order: 2, id: "pYzuw5bTIe8", topic: "Flight Mechanics", title: "Luc Armant talks about The Moment Coefficient, Enzo 3 Certification Debate & Physics of Stability" },   // ** review
  { order: 3, id: "uCEfssE40u8", topic: "World Cups", title: "SRS Piedrahita BGD Edition Task 1 Highlights" },   // ** review
  { order: 4, id: "zzcktKfMcUI", topic: "Know Your Equipment", title: "Technical Masterclass by Brett Janaway | Science of Paraglider Trimming,Performance & New Legalities" },   // ** review
  { order: 5, id: "cuGs7Lk6Dt4", topic: "World Cups", title: "SRS BGD Edition 2026 | Day 1: Registration, Pilots & Pe\u00f1as de Piedrah\u00edta\ud83c\udf89" },   // ** review
  { order: 6, id: "aGiisCcG5v8", topic: "Brand Stories", title: "Robert (Robbie) Whittall: 113 mins of Unhinged conversations with The Man Behind Ozone Paragliders" },   // ** review
  { order: 7, id: "J5j3Hk_HcFQ", topic: "Risk vs Reward", title: "Metacognition: Paragliding's Hidden Psychology with Beni Kalin & Heli Schrempf" },   // ** review
  { order: 8, id: "itpkNQwV438", topic: "Sky Gods", title: "The Russell Ogden Interview: Decoding Paragliding Mastery Protocols: Progression, Fear & Competition" },   // ** review
  { order: 9, id: "vPnIYYKcvEg", topic: "World Cups", title: "Task 5 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 10, id: "op1-O01xkH4", topic: "World Cups", title: "Task 4 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 11, id: "7il6yV1vdIc", topic: "World Cups", title: "Task 2 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 12, id: "BRAX1XMU390", topic: "World Cups", title: "Task 1 Highlights | 15th Paragliding World Cup Super Final Pegalajar 2026" },   // ** review
  { order: 13, id: "FOuAWMeoxs4", topic: "World Cups", title: "Highlights Day 1 - PWCA Superfinal 2026" },   // ** review
  { order: 14, id: "_k2uxEkrN7s", topic: "Risk vs Reward", title: "Paragliding Physiology & Safety Protocols | Dr Matt Wilkes Explains: Biophysics in the Art of Flight" },   // ** review
  { order: 15, id: "AvSCngFI7R0", topic: "Risk vs Reward", title: "If you fly in the Himalayas, Alps, or above 3000 mtrs, this episode is for you - ft. Dr Matt Wilkes" },   // ** review
  { order: 16, id: "p_HpeN5x7dE", topic: "Risk vs Reward", title: "Cognitive Bias of Dunning Kruger Effect in Paragliding | Explained by Beni Kalin & Heli Schrempf" },   // ** review
  { order: 17, id: "mYG80ZiHIyo", topic: "Resources, Tools and Tips", title: "Sports Psychology for Paragliding: Train Your Mind to Fly Better with Yvonne Dathe" },
  { order: 18, id: "ylj8CZgqLyM", topic: "Living the Dream", title: "From Cuba to Socotra: Inside the World\u2019s Most Unique Paragliding Tours" },
  { order: 19, id: "yNNqjTpQkRQ", topic: "Living the Dream", title: "How to Fly With Your Dog | Explained by Shams" },
  { order: 20, id: "BceEzHgylwo", topic: "The Dark Side", title: "Survived 15 Years of Flying Then a Rescue Helicopter Changed Everything | A Talk With Nick Neynes" },
  { order: 21, id: "Kdd1R8x36vU", topic: "World Cups", title: "From Tents to Trophies: Understanding Acro Champion's Mindset on Ego, Glory & Drugs | Luke De Weert" },
  { order: 22, id: "iurDFHlgJjI", topic: "Flight Mechanics", title: "Tom Lolies Explains The Science Of Wing Design and Evolution from ENC to  CSC" },
  { order: 23, id: "3ZySapU_YLI", topic: "Resources, Tools and Tips", title: "The Art of Capturing Human Flight | Jake Holland's Guide to Filming Passion Projects in Paragliding" },
  { order: 24, id: "CYVrlWuls6o", topic: "World Cups", title: "Scoring in Paragliding Competitions: A New Pilot's Guide to the GAP Formula & Strategy | Joerg Ewald" },
  { order: 25, id: "wvJWd8lVZzc", topic: "Know Your Equipment", title: "Can we Steer a Round Reserve Parachute? Urs Haari Answers!" },
  { order: 26, id: "kSoFk23TuX0", topic: "Know Your Equipment", title: "Watch this Before you Buy a Paragliding Harness | A Talk with Zsolt Ero" },
  { order: 27, id: "i9z4MyL6KgQ", topic: "World Cups", title: "The Inside Story of Sports Racing Series (SRS) by Brett Janaway" },
  { order: 28, id: "VmaPERBK-lo", topic: "The Dark Side", title: "The Unfiltered Truth About Paragliding Governance: with Bill Hughes & Goran Dimiskovski" },
  { order: 29, id: "YyGdTDXC1Lc", topic: "The Dark Side", title: "Bill Belcourt: The Uncomfortable Truth No One is Talking about in the Current Safety Paradox" },
  { order: 30, id: "nlgbMKLNNk4", topic: "World Cups", title: "Bruce Goldsmith explains MRT scoring system and its impact on Paragliding Competitions" },
  { order: 31, id: "xNMHk_8qbzo", topic: "Flight Mechanics", title: "Luc Armant talks about Debunking the Myths and Upgrading Enzo 3" },
  { order: 32, id: "jdiYdzJ9U5w", topic: "The Dark Side", title: "Insights From The Gaggle with Tilen Ceglar & Stan Radzikowski" },
  { order: 33, id: "FvIZpqydhyo", topic: "Brand Stories", title: "Pal Takats on Challenges, Change & The Future of Paragliding " },
  { order: 34, id: "jSfQYxxbaWk", topic: "The Dark Side", title: "What is #CIVLRESIGN with Julien Garcia" },
  { order: 35, id: "S2wiY4DO_TU", topic: "New Technologies", title: "Understanding Skymate: Paragliding Worlds First AI Driven Smart Harness System with Roman Barthelemy" },
  { order: 36, id: "rFC56EjtXCY", topic: "World Cups", title: "The Resilience Equation: Erlend Ukvitne\u2019s Unrelenting Path to X-Alps and the Brink of a World Record" },
  { order: 37, id: "VqkYy6YhXcY", topic: "Risk vs Reward", title: "Consequence Over Probability: Will Gadd on Why True Safety Lies in Clarity" },
  { order: 38, id: "YGU7-ctBYYE", topic: "New Technologies", title: "Why Paragliding\u2019s Safety Future Looks Different: RAST Inventor Michael Nesler & the LeelooX Effect" },
  { order: 39, id: "N4OGIzYNnl0", topic: "Resources, Tools and Tips", title: "The Silent Mind In Screaming Winds : Unlocking Peak Focus To Attain Flow State In Paragliding" },
  { order: 40, id: "DIHf30B2NoY", topic: "Weather Patterns", title: "Meteorology 101 A beginner\u2019s Guide to Understanding Weather Apps and Decoding Endless Forecasting..." },
  { order: 41, id: "EttlenmzWHM", topic: "Know Your Equipment", title: "Urs Haari: The Real Truth About Reserve Parachutes : A Paragliding Survival Guide" },
  { order: 42, id: "cnizMhvNQrM", topic: "World Cups", title: "Shane Tighe\u2019s Road to X-Alps : Engineering Conquests In The Sky from Australia\u2019s Flatlands to the..." },
  { order: 43, id: "78PaTvxRWJ0", topic: "Flight Mechanics", title: "Alja\u017e Vali\u010d : 777 : Paragliding\u2019s Slovenian Mavericks Redefining the EN B Class And Elevating Fre..." },
  { order: 44, id: "qZRa_Ozz0Hg", topic: "Living the Dream", title: "Sandrine Roy : Vol Biv & Freedom Unfiltered : A Human-Powered Odyssey By Paragliding, Biking & Sa..." },
  { order: 45, id: "CBxyezZ-UOw", topic: "Flight Mechanics", title: "Alain Zoller: The Science of EN Certifications : How Work Group 6 Shaped Paragliding Testing, Inn..." },
  { order: 46, id: "i-QoHo0ZaPU", topic: "Resources, Tools and Tips", title: "Ziad Bassil : Finest Paragliding Reviews & Superpower of Changing Wings as A Human" },
  { order: 47, id: "ebwdsVgopnU", topic: "Storytellers", title: "Eddie Colfox : Storytime : Chasing Adventure With the Real OG John Silvester & 3 Decades of Makin..." },
  { order: 48, id: "jMVTzRFPWNw", topic: "Resources, Tools and Tips", title: "\u200bAshutosh Chopra: Identifying Passion Vs Obsession: An Aviator\u2019s Approach to Overcoming Adversity..." },
  { order: 49, id: "pFxe7oZTH2E", topic: "Risk vs Reward", title: "Kinga Masztalerz: Building a Healthy Relationship with the Skies: How to Master Fear, Build Resil..." },
  { order: 50, id: "wTfS5kv1t9M", topic: "Flight Mechanics", title: "Helmut Schrempf : Modernizing SIV Courses: How This New Training Method Can Help You Master Glide..." },
  { order: 52, id: "T1pR130Umkk", topic: "Storytellers", title: "Storytellers : Marko Milutinovic (Mid-Air Collision)" },
  { order: 54, id: "vmnrTFbu6vg", topic: "New Technologies", title: "New Technologies 5 : Frantisek Pavlousek (UP Paragliders)" },
  { order: 55, id: "yUsfGCfI_30", topic: "Resources, Tools and Tips", title: "Flying & Filming 3 : Andreas Lattner (hochzwei.media)" },
  { order: 56, id: "OiertfSq-6o", topic: "Resources, Tools and Tips", title: "Flying & Filming 2 : Benjamin Kellet" },
  { order: 57, id: "DmyYSA6NeMw", topic: "Risk vs Reward", title: "Risk Vs Reward 5 : Gabriel Orsini (partytillimpact)" },
  { order: 58, id: "fKWV5YR8MRE", topic: "Know Your Equipment", title: "Helmet Safety : Christian Ciech : ICARO 2000 [1st Anniversary Edition]" },
  { order: 59, id: "MFYb9KmT15s", topic: "Risk vs Reward", title: "Risk Vs Reward 4 : Ra\u00fal Rodr\u00edguez" },
  { order: 60, id: "9GfZcM3P3jY", topic: "Brand Stories", title: "Brand Stories : Neo : Eric Roussel" },
  { order: 61, id: "QPkIlI2qG5A", topic: "Know Your Equipment", title: "Carabiner Fatigue : Finsterwalder & Charly (whitepaper)" },
  { order: 63, id: "L2MrAoec24I", topic: "Resources, Tools and Tips", title: "Flying & Filming 1 : Benjamin Jordan" },
  { order: 64, id: "bDJ1zRG90cs", topic: "Living the Dream", title: "Living The Dream : Benjamin Jordan" },
  { order: 65, id: "njoPDwe457w", topic: "Risk vs Reward", title: "Risk Vs Reward 3 : Manfred Ruhmer" },
  { order: 67, id: "J8visA4lxys", topic: "Risk vs Reward", title: "Risk Vs Reward 2 : Subir Sidhu" },
  { order: 68, id: "md9ls8OtBiA", topic: "Risk vs Reward", title: "Risk Vs Reward 1 : Philipp Zellner" },
  { order: 70, id: "zEnjmp9hrlE", topic: "New Technologies", title: "New Technologies 4 : Veselin Ovcharov (Fly The Earth)" },
  { order: 71, id: "MxwM1lJEVIU", topic: "New Technologies", title: "New Technologies 2 : Guillem Batlle & Adri\u00e0 Grau (Niviuk Paragliders)" },
  { order: 72, id: "aFO5Uk5BX9s", topic: "New Technologies", title: "New Technologies 1 : Beni K\u00e4lin (speedflyingschool.com)" },
  { order: 73, id: "ZjSojM_Ao0U", topic: "World Cups", title: "PWC Lifestyle: Klaudia Bulgakow" },
  { order: 74, id: "l1gmplS02FI", topic: "World Cups", title: "PWCA: Goran Dimiskovski" },   // ** review
  { order: 75, id: "UVLF8l0qFlA", topic: "Navigators", title: "Pre PWC Kenya: Nikolay Yotov" },
  { order: 76, id: "0VPg7TZ9hK0", topic: "Navigators", title: "Navigating Panchgani (Pre PWC India) : Vistasp Kharas" },
  { order: 77, id: "zKabIDewXn0", topic: "Resources, Tools and Tips", title: "AMA #1" },
  { order: 78, id: "xXSGK8oB4Oc", topic: "Navigators", title: "Navigating Australia : Godfrey Wenness" },
  { order: 79, id: "QmprO-5qkR8", topic: "Sky Gods", title: "Sky Gods : Flying to Win : Honorin Hamard" },
  { order: 80, id: "Q2oTFoQcrGw", topic: "Sky Gods", title: "Sky Gods : Flying 8000ers : Antoine Girard" },
  { order: 81, id: "_apo1PNabZI", topic: "Navigators", title: "Navigating India: Jigish Gohil (Bonus Ep)" },
  { order: 82, id: "TO6gW69d7YE", topic: "Navigators", title: "Navigating India: Eddie Colfox" },
  { order: 83, id: "kOgDYSvfUuo", topic: "Navigators", title: "Navigating Colombia: Pal Takats" },
];
