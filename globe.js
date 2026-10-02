// The episode globe on the homepage: a glass globe, drawn on canvas with the
// shading, rim and compass ring in SVG above it. Drag to turn it, Ctrl or Cmd
// and scroll (or pinch) to zoom, click a pin for the episode.
//
// THE GLASS GLOBE (settled in the globe prototype, October 2026). The far side
// shows through faintly, so a pin round the back is still a dim dot rather than
// gone; a lit rim and a compass ring frame it; stars sit behind it. Country
// borders, a name under the pointer, zoom buttons, and one "smart" pointer that
// picks the nearest pin instead of whichever happens to be drawn on top.
// Deliberately off: a glow, the line from Oslo to the open episode, and pins
// grouped into numbered clusters.
//
// The land and borders are assets/js/globe-world.js, hosted with the site. They
// used to be fetched from unpkg on every visit.
(function () {
  'use strict';
  const container = document.getElementById('epMap');
  if (!container || !window.d3) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const RAD = Math.PI / 180;
  const TAU = Math.PI * 2;
  const WORLD = window.GLOBE_WORLD || null;
  const LAND = WORLD ? WORLD.land : null;
  const BORDERS = WORLD ? WORLD.borders : null;

  const popup = document.getElementById('mapPopup');
  const popupTitle = popup.querySelector('.popup-title');
  const popupLink = popup.querySelector('.popup-link');
  const tipEl = container.querySelector('.gl-tip');
  const zoomEl = container.querySelector('.gl-zoom');
  const hintEl = container.querySelector('.gl-hint');

  /* Canvas cannot read a CSS variable, so the tokens are read once from :root.
     Every colour drawn below is one of these, with an alpha. */
  const TOK = (function () {
    const cs = getComputedStyle(document.documentElement);
    const mk = (name) => {
      const h = cs.getPropertyValue(name).trim().replace('#', '');
      const c = [0, 2, 4].map((i) => parseInt(h.substr(i, 2), 16)).join(',');
      return (a) => 'rgba(' + c + ',' + a + ')';
    };
    return { bg: mk('--bg'), card: mk('--card'), orange: mk('--orange'), light: mk('--gray-light') };
  })();

  /* The darker of the prototype's glass tones. "veil" is how much of the page
     background is laid over the sphere; the rest are the strengths of each part
     drawn on it. */
  const T = { veil: 0.5, front: 0.13, back: 0.07, coast: 0.78, grat: 0.10, backGrat: 0.045, border: 0.17 };
  const GRAT = d3.geoGraticule()();

  // Every episode with a place, with its location inferred from cues in the
  // title or guest (nationality, named place, or brand HQ).
  // tools/generate_globe_episodes.py reads this list, so keep its shape.
  const episodeData = [
    ['Luc Armant talks about The Moment Coefficient, Enzo 3 Certification Debate & Physics of Stability', 'episodes/luc-armant-talks-about-the-moment-coefficient-enzo-3.html', -3.66, 37.68],
    ["Technical Masterclass by Brett Janaway | Science of Paraglider Trimming,Performance & New Legalities", 'episodes/technical-masterclass-by-brett-janaway-science-of.html', -5.28, 40.46],
    ["How to Thermal Like a Pro: Find, Center & Climb | Paragliding Tutorial with Brett Janaway", 'episodes/how-to-thermal-like-a-pro-find-center-climb-paragliding.html', -5.28, 40.46],
    ["Robert (Robbie) Whittall: 113 mins of Unhinged conversations with The Man Behind Ozone Paragliders", 'episodes/robert-whittall-113-mins-of-unhinged-conversations-with.html', 6.13, 45.9],
    ["Metacognition: Paragliding's Hidden Psychology with Beni Kalin & Heli Schrempf", 'episodes/metacognition-paragliding-s-hidden-psychology-with-beni.html', 13.4, 47.3],
    ["The Russell Ogden Interview: Decoding Paragliding Mastery Protocols: Progression, Fear & Competition", 'episodes/the-russell-ogden-interview-decoding-paragliding-mastery.html', -1.9, 52.5],
    ["Paragliding Physiology & Safety Protocols | Dr Matt Wilkes Explains: Biophysics in the Art of Flight", 'episodes/paragliding-physiology-safety-protocols-dr-matt-wilkes.html', -1.5, 52.0],
    ["If you fly in the Himalayas, Alps, or above 3000 mtrs, this episode is for you - ft. Dr Matt Wilkes", 'episodes/if-you-fly-in-the-himalayas-alps-or-above-3000-mtrs-this.html', 76.7, 32.0],
    ["Cognitive Bias of Dunning Kruger Effect in Paragliding | Explained by Beni Kalin & Heli Schrempf", 'episodes/cognitive-bias-of-dunning-kruger-effect-in-paragliding.html', 13.4, 47.3],
    ['Sports Psychology for Paragliding: Train Your Mind to Fly Better with Yvonne Dathe', 'episodes/sports-psychology-for-paragliding-train-your-mind-to-fly.html', 10.4, 51.2],
    ["From Cuba to Socotra: Inside the World’s Most Unique Paragliding Tours", 'episodes/from-cuba-to-socotra-inside-the-worlds-most-unique.html', -79.9, 21.5],
    ["How to Fly With Your Dog | Explained by Shams", 'episodes/how-to-fly-with-your-dog-explained-by-shams.html', 6.9, 45.9],
    ["Survived 15 Years of Flying Then a Rescue Helicopter Changed Everything | A Talk With Nick Neynes", 'episodes/survived-15-years-of-flying-then-a-rescue-helicopter.html', 4.35, 50.85],
    ["From Tents to Trophies: Understanding Acro Champion's Mindset on Ego, Glory & Drugs | Luke De Weert", 'episodes/from-tents-to-trophies-understanding-acro-champion-s.html', 5.3, 52.1],
    ["Tom Lolies Explains The Science Of Wing Design and Evolution from ENC to  CSC", 'episodes/tom-lolies-explains-the-science-of-wing-design-and.html', 4.35, 50.85],
    ["The Art of Capturing Human Flight | Jake Holland's Guide to Filming Passion Projects in Paragliding", 'episodes/the-art-of-capturing-human-flight-jake-holland-s-guide-to.html', -2.5, 53.4],
    ["Scoring in Paragliding Competitions: A New Pilot's Guide to the GAP Formula & Strategy | Joerg Ewald", 'episodes/scoring-in-paragliding-competitions-a-new-pilot-s-guide-to.html', 10.4, 51.2],
    ['Snippet: A Reserve Parachute Trick Every Pilot Should Know, by Urs Haari', 'https://creators.spotify.com/pod/profile/paragliding-atlas/episodes/Snippet-A-Reserve-Parachute-Trick-Every-Pilot-Should-Know--by-Urs-Haari-e3c6unr', 8.2, 46.8],
    ["Watch this Before you Buy a Paragliding Harness | A Talk with Zsolt Ero", 'episodes/watch-this-before-you-buy-a-paragliding-harness-a-talk.html', 19.0, 47.5],
    ['The Inside Story of Sports Racing Series (SRS) by Brett Janaway', 'episodes/the-inside-story-of-sports-racing-series-by-brett-janaway.html', -1.9, 52.5],
    ["The Unfiltered Truth About Paragliding Governance: with Bill Hughes & Goran Dimiskovski", 'episodes/the-unfiltered-truth-about-paragliding-governance-with.html', 21.7, 41.6],
    ["Bill Belcourt: The Uncomfortable Truth No One is Talking about in the Current Safety Paradox", 'episodes/bill-belcourt-the-uncomfortable-truth-no-one-is-talking.html', -111.6, 40.6],
    ["Bruce Goldsmith explains MRT scoring system and its impact on Paragliding Competitions", 'episodes/bruce-goldsmith-explains-mrt-scoring-system-and-its-impact.html', -1.9, 52.5],
    ["Luc Armant talks about Debunking the Myths and Upgrading Enzo 3", 'episodes/luc-armant-talks-about-debunking-the-myths-and-upgrading.html', 6.13, 45.9],
    ['Insights From The Gaggle with Tilen Ceglar & Stan Radzikowski', 'episodes/insights-from-the-gaggle-with-tilen-ceglar-stan.html', 14.8, 46.1],
    ["Pal Takats on Challenges, Change & The Future of Paragliding ", 'episodes/pal-takats-on-challenges-change-the-future-of-paragliding.html', 19.0, 47.5],
    ["What is #CIVLRESIGN with Julien Garcia", 'episodes/what-is-civlresign-with-julien-garcia.html', 2.35, 48.85],
    ["Anatomy of a Dream with Damien Lacaze: A Lifestyle Full of Grit, Grace and Vertical Freedom", 'episodes/anatomy-of-a-dream-with-damien-lacaze.html', 6.13, 45.9],
    ["Demystifying The Science Behind Endless Fun Factor of Parakites With Bryan Van Ostheim", 'episodes/demystifying-the-science-behind-parakites-bryan-van-ostheim.html', 4.35, 50.85],
    ["Legacy and Lifetimes of Gin Seok Song: 5 Decades of Pioneering the Art of Free Flight", 'episodes/legacy-and-lifetimes-of-gin-seok-song.html', 127.8, 36.5],
    ["Maxime Pinot : The Journey Within : Mapping our Quest to Touch The Sky With Glory", 'episodes/maxime-pinot-the-journey-within.html', 6.13, 45.9],
    ["Understanding Skymate: Paragliding Worlds First AI Driven Smart Harness System with Roman Barthelemy", 'episodes/understanding-skymate-paragliding-worlds-first-ai-driven.html', 2.35, 48.85],
    ["Science Backed Pre Flight Rituals to Unlock Laser Sharp Paragliding Clarity: On Demand", 'episodes/science-backed-pre-flight-rituals.html', 10.75, 59.91],
    ["The Resilience Equation: Erlend Ukvitne’s Unrelenting Path to X-Alps and the Brink of a World Record", 'episodes/the-resilience-equation-erlend-ukvitnes-unrelenting-path.html', 8.5, 60.5],
    ["Mastering the Unknown: Neuroscience of Crisis Management & Neuroplasticity Training", 'episodes/mastering-the-unknown-neuroscience-of-crisis-management.html', 10.75, 59.91],
    ["Consequence Over Probability: Will Gadd's Field Protocols for Rewiring Risk Intuition and Why True Safety Lies in Clarity", 'episodes/consequence-over-probability-will-gadd-on-why-true-safety.html', -106, 56],
    ["Why Paragliding’s Safety Future Looks Different: RAST Inventor Michael Nesler & the LeelooX Effect", 'episodes/why-paraglidings-safety-future-looks-different-rast.html', 10.4, 51.2],
    ["The Silent Mind In Screaming Winds : Unlocking Peak Focus To Attain Flow State In Paragliding", 'episodes/the-silent-mind-in-screaming-winds-unlocking-peak-focus-to.html', -1.9, 52.5],
    ["Meteorology 101: A beginner’s Guide to Understanding Weather Apps and Decoding Endless Forecasting Options", 'episodes/meteorology-101-a-beginners-guide-to-understanding-weather.html', 10.75, 59.91],
    ["Urs Haari: The Real Truth About Reserve Parachutes : A Paragliding Survival Guide", 'episodes/urs-haari-the-real-truth-about-reserve-parachutes-a.html', 8.2, 46.8],
    ["Shane Tighe’s Road to X-Alps : Engineering Conquests In The Sky from Australia’s Flatlands to the Pinnacle of Hike and Fly", 'episodes/shane-tighes-road-to-x-alps-engineering-conquests-in-the.html', 133.8, -25.3],
    ["Aljaž Valič : 777 : Paragliding’s Slovenian Mavericks Redefining the EN B Class And Elevating Free Flight Performance", 'episodes/aljaz-valic-777-paraglidings-slovenian-mavericks.html', 14.8, 46.1],
    ["Sandrine Roy : Vol Biv & Freedom Unfiltered : A Human-Powered Odyssey By Paragliding, Biking & Sailing Around The Globe", 'episodes/sandrine-roy-vol-biv-freedom-unfiltered-a-human-powered.html', 2.35, 48.85],
    ["Alain Zoller: The Science of EN Certifications : How Work Group 6 Shaped Paragliding Testing, Innovation & Safety", 'episodes/alain-zoller-the-science-of-en-certifications-how-work.html', 8.2, 46.8],
    ["Ziad Bassil : Finest Paragliding Reviews & Superpower of Changing Wings as A Human", 'episodes/ziad-bassil-finest-paragliding-reviews-superpower-of.html', 35.5, 33.9],
    ["Eddie Colfox : Storytime : Chasing Adventure With the Real OG John Silvester & 3 Decades of Making Memories Across The Globe", 'episodes/eddie-colfox-storytime-chasing-adventure-with-the-real-og.html', -1.9, 52.5],
    ["Ashutosh Chopra: Identifying Passion Vs Obsession: An Aviator’s Approach to Overcoming Adversity, Rebuilding Trust and Finding Joy in the Skies", 'episodes/ashutosh-chopra-identifying-passion-vs-obsession-an.html', 78.9, 20.6],
    ["Kinga Masztalerz: Building a Healthy Relationship with the Skies: How to Master Fear, Build Resilience & Find Joy Through Paragliding", 'episodes/kinga-masztalerz-building-a-healthy-relationship-with-the.html', 19.1, 52.2],
    ["Helmut Schrempf : Modernizing SIV Courses: How This New Training Method Can Help You Master Glider Control and Improve Paragliding Safety", 'episodes/helmut-schrempf-modernizing-siv-courses-how-this-new.html', 13.4, 47.3],
    ['A Note of Thanks', 'episodes/a-note-of-thanks.html', 10.75, 59.91],
    ["Storytellers : Marko Milutinovic (Mid-Air Collision)", 'episodes/storytellers-marko-milutinovic.html', 21.0, 44.0],
    ["New Technologies 5 : Frantisek Pavlousek (UP Paragliders)", 'episodes/new-technologies-5-frantisek-pavlousek.html', 15.5, 49.8],
    ["Flying & Filming 3 : Andreas Lattner (hochzwei.media)", 'episodes/flying-filming-3-andreas-lattner.html', 10.4, 51.2],
    ["Flying & Filming 2 : Benjamin Kellet", 'episodes/flying-filming-2-benjamin-kellet.html', -1.9, 52.5],
    ["Risk Vs Reward 5 : Gabriel Orsini (partytillimpact)", 'episodes/risk-vs-reward-5-gabriel-orsini.html', 12.5, 41.9],
    ["Helmet Safety : Christian Ciech : ICARO 2000", 'episodes/helmet-safety-christian-ciech-icaro-2000.html', 12.5, 41.9],
    ["Risk Vs Reward 4 : Raúl Rodríguez", 'episodes/risk-vs-reward-4-raul-rodriguez.html', -3.7, 40.4],
    ["Brand Stories : Neo : Eric Roussel", 'episodes/brand-stories-neo-eric-roussel.html', 6.13, 45.9],
    ["Carabiner Fatigue : Finsterwalder & Charly (whitepaper)", 'episodes/carabiner-fatigue-finsterwalder-charly.html', 10.4, 51.2],
    ["Flying & Filming 1 : Benjamin Jordan", 'episodes/flying-filming-1-benjamin-jordan.html', -106, 56],
    ["Living The Dream : Benjamin Jordan", 'episodes/living-the-dream-benjamin-jordan.html', -106, 56],
    ["Risk Vs Reward 3 : Manfred Ruhmer", 'episodes/risk-vs-reward-3-manfred-ruhmer.html', 13.4, 47.3],
    ["Risk Vs Reward 2 : Subir Sidhu", 'episodes/risk-vs-reward-2-subir-sidhu.html', 78.9, 20.6],
    ["Risk Vs Reward 1 : Philipp Zellner", 'episodes/risk-vs-reward-1-philipp-zellner.html', 13.4, 47.3],
    ["New Technologies 4 : Veselin Ovcharov (Fly The Earth)", 'episodes/new-technologies-4-veselin-ovcharov.html', 25.5, 42.7],
    ["New Technologies 3 : Stephan Stiegler (AirDesign Paragliders)", 'episodes/new-technologies-3-stephan-stiegler.html', 13.4, 47.3],
    ["New Technologies 2 : Guillem Batlle & Adrià Grau (Niviuk Paragliders)", 'episodes/new-technologies-2-guillem-batlle-adria-grau.html', 2.15, 41.4],
    ["New Technologies 1 : Beni Kälin (speedflyingschool.com)", 'episodes/new-technologies-1-beni-kalin.html', 8.2, 46.8],
    ['PWC Lifestyle: Klaudia Bulgakow', 'episodes/pwc-lifestyle-klaudia-bulgakow.html', 19.1, 52.2],
    ['PWCA: Goran Dimiskovski', 'episodes/pwca-goran-dimiskovski.html', 21.7, 41.6],
    ['Pre PWC Kenya: Nikolay Yotov', 'episodes/pre-pwc-kenya-nikolay-yotov.html', 36.8, -1.3],
    ["Navigating Panchgani (Pre PWC India) : Vistasp Kharas", 'episodes/navigating-panchgani-vistasp-kharas.html', 73.8, 17.9],
    ['AMA #1', 'episodes/ama-1.html', 10.75, 59.91],
    ["Navigating Australia : Godfrey Wenness", 'episodes/navigating-australia-godfrey-wenness.html', 150.72, -30.72],
    ["Sky Gods : Flying to Win : Honorin Hamard", 'episodes/sky-gods-flying-to-win-honorin-hamard.html', 6.13, 45.9],
    ["Sky Gods : Flying 8000ers : Antoine Girard", 'episodes/sky-gods-flying-8000ers-antoine-girard.html', 86.9, 27.98],
    ['Navigating India: Jigish Gohil (Bonus Ep)', 'episodes/navigating-india-jigish-gohil.html', 76.72, 32.04],
    ['Navigating India: Eddie Colfox', 'episodes/navigating-india-eddie-colfox.html', 76.72, 32.04],
    ['Navigating Colombia: Pal Takats', 'episodes/navigating-colombia-pal-takats.html', -76.15, 4.41],
    ['Touch The Sky With Glory', 'episodes/touch-the-sky-with-glory.html', 10.75, 59.91]
  ];

  const episodes = episodeData.map(([title, href, lon, lat], i) => {
    const jitterLon = (((i * 37) % 100) / 100 - 0.5) * 1.4;
    const jitterLat = (((i * 53) % 100) / 100 - 0.5) * 1.4;
    return { i: i, title: title, href: href, lon: lon + jitterLon, lat: lat + jitterLat };
  });
  /* cos and sin of each pin's position, for drawing the ones on the far side. */
  const EP_VEC = (function () {
    const a = new Float32Array(episodes.length * 4);
    episodes.forEach((e, i) => {
      a[i * 4] = Math.cos(e.lon * RAD); a[i * 4 + 1] = Math.sin(e.lon * RAD);
      a[i * 4 + 2] = Math.cos(e.lat * RAD); a[i * 4 + 3] = Math.sin(e.lat * RAD);
    });
    return a;
  })();

  /* The globe fills less of the box than the old flat one did, to leave room
     for the compass ring and its labels. */
  const fitDiv = (w) => (w < 600 ? 2.36 : 2.72);
  let width = container.clientWidth || 300;
  let height = container.clientHeight || 300;
  let baseScale = Math.min(width, height) / fitDiv(width);
  let dpr = Math.min(window.devicePixelRatio || 1, 2);
  let starPts = [];

  const canvas = document.createElement('canvas');
  canvas.className = 'gl-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  container.insertBefore(canvas, container.firstChild);
  const ctx = canvas.getContext('2d');

  const HOME = [-20, -15];
  const projection = d3.geoOrthographic()
    .scale(baseScale).translate([width / 2, height / 2]).clipAngle(90).rotate(HOME);
  /* The far hemisphere, as seen through the globe from the front. */
  const back = d3.geoOrthographic().clipAngle(90).reflectX(true);
  const path = d3.geoPath(projection, ctx);
  const backPath = d3.geoPath(back, ctx);

  const svg = d3.select(container).insert('svg', '.gl-tip').attr('class', 'gl-svg');

  /* ---- Shading, rim and compass ring sit above the canvas. ---- */
  const defs = svg.append('defs');
  function grad(kind, id, attrs, stops) {
    const g = defs.append(kind).attr('id', id);
    Object.keys(attrs).forEach((k) => g.attr(k, attrs[k]));
    stops.forEach((s) => {
      g.append('stop').attr('offset', s[0])
        .style('stop-color', 'var(--' + s[1] + ')').style('stop-opacity', s[2]);
    });
  }
  grad('radialGradient', 'gShade', { cx: 0.36, cy: 0.33, r: 0.72 },
    [[0, 'bg', 0], [0.48, 'bg', 0], [0.78, 'bg', 0.46], [1, 'bg', 0.84]]);
  grad('radialGradient', 'gHi', { cx: 0.33, cy: 0.3, r: 0.44 },
    [[0, 'gray-light', 0.13], [1, 'gray-light', 0]]);
  grad('radialGradient', 'gLimb', { cx: 0.5, cy: 0.5, r: 0.5 },
    [[0.7, 'bg', 0], [0.9, 'bg', 0.3], [1, 'bg', 0.72]]);
  grad('linearGradient', 'gRim', { x1: 0.15, y1: 0.15, x2: 0.85, y2: 0.85 },
    [[0, 'white', 0.9], [0.2, 'orange', 0.9], [0.55, 'orange', 0.22], [1, 'gray-light', 0.05]]);

  const shell = svg.append('g').attr('class', 'gl-shell');
  const shadeHi = shell.append('circle').attr('fill', 'url(#gHi)');
  const shadeDir = shell.append('circle').attr('fill', 'url(#gShade)');
  const shadeLimb = shell.append('circle').attr('fill', 'url(#gLimb)');
  const pinGroup = svg.append('g').style('pointer-events', 'none');
  const shell2 = svg.append('g').attr('class', 'gl-shell');
  const rim = shell2.append('circle').attr('fill', 'none').attr('stroke', 'url(#gRim)').attr('stroke-width', 1.5);
  const bezel = shell2.append('g');
  const bzRing = bezel.append('circle').attr('fill', 'none').attr('stroke', 'var(--line)');
  const bzMinor = bezel.append('path').attr('fill', 'none').attr('stroke', 'var(--edge)');
  const bzMed = bezel.append('path').attr('fill', 'none').attr('stroke', 'var(--edge-hi)');
  const bzMajor = bezel.append('path').attr('fill', 'none').attr('stroke', 'var(--gray-light)');
  const bzLabels = bezel.append('g');
  const CARD = { 0: 'N', 90: 'E', 180: 'S', 270: 'W' };
  bzLabels.selectAll('text').data(d3.range(0, 360, 30)).enter().append('text')
    .attr('class', (a) => 'gl-bz-label' + (a === 0 ? ' n' : ''))
    .text((a) => CARD[a] || String(a).padStart(3, '0'));
  /* Swings to the bearing of the open episode, measured from Oslo. */
  const bzIndex = bezel.append('path').attr('class', 'gl-bz-index')
    .attr('fill', 'var(--orange)').style('opacity', 0);
  let indexAngle = 0;

  function polar(cx, cy, r, deg) {
    const a = (deg - 90) * RAD;
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  }
  function tick(cx, cy, r0, r1, deg) {
    const p = polar(cx, cy, r0, deg), q = polar(cx, cy, r1, deg);
    return 'M' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + 'L' + q[0].toFixed(1) + ',' + q[1].toFixed(1);
  }
  function layoutBezel(R) {
    const cx = width / 2, cy = height / 2;
    const small = width < 600;
    const r0 = R * (small ? 1.1 : 1.17);
    const step = small ? 5 : 2;
    const lenMin = small ? 3 : 4, lenMed = small ? 5 : 8, lenMaj = small ? 7 : 12;
    let dMin = '', dMed = '', dMaj = '';
    for (let a = 0; a < 360; a += step) {
      if (a % 30 === 0) dMaj += tick(cx, cy, r0, r0 + lenMaj, a);
      else if (a % 10 === 0) dMed += tick(cx, cy, r0, r0 + lenMed, a);
      else dMin += tick(cx, cy, r0, r0 + lenMin, a);
    }
    bzRing.attr('cx', cx).attr('cy', cy).attr('r', r0);
    bzMinor.attr('d', dMin); bzMed.attr('d', dMed); bzMajor.attr('d', dMaj);
    bzLabels.style('display', small ? 'none' : null)
      .selectAll('text')
      .attr('x', (a) => polar(cx, cy, r0 + lenMaj + 13, a)[0])
      .attr('y', (a) => polar(cx, cy, r0 + lenMaj + 13, a)[1]);
    const hw = small ? 4.5 : 6;
    const yTip = cy - (r0 - (small ? 11 : 14)), yBase = cy - (r0 - 3);
    bzIndex.attr('d', 'M' + cx + ',' + yTip + 'L' + (cx - hw) + ',' + yBase + 'L' + (cx + hw) + ',' + yBase + 'Z')
      .attr('transform', 'rotate(' + indexAngle + ' ' + cx + ' ' + cy + ')');
  }
  function swingIndex(deg) {
    const from = indexAngle;
    const to = from + ((((deg - from) % 360) + 540) % 360 - 180);
    bzIndex.style('opacity', 1);
    if (reduceMotion) {
      indexAngle = to;
      bzIndex.attr('transform', 'rotate(' + to + ' ' + (width / 2) + ' ' + (height / 2) + ')');
      return;
    }
    bzIndex.interrupt().transition().duration(800).ease(d3.easeCubicOut)
      .attrTween('transform', () => (k) => {
        indexAngle = from + (to - from) * k;
        return 'rotate(' + indexAngle + ' ' + (width / 2) + ' ' + (height / 2) + ')';
      });
  }

  function setR(R) {
    const cx = width / 2, cy = height / 2;
    [shadeHi, shadeDir, shadeLimb, rim].forEach((c) => c.attr('cx', cx).attr('cy', cy).attr('r', R));
    layoutBezel(R);
  }

  /* Fixed seed, so the stars do not reshuffle on every resize. */
  function layoutStars() {
    let s = 20260928;
    const rnd = () => {
      s |= 0; s = s + 0x6D2B79F5 | 0;
      let t = Math.imul(s ^ s >>> 15, 1 | s);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
    const n = Math.round(width * height / 5200);
    starPts = d3.range(n).map(() => [rnd() * width, rnd() * height, 0.4 + rnd() * 0.8, 0.08 + rnd() * rnd() * 0.5]);
  }

  /* ---- Pins. They take no pointer events: one handler for the whole globe
     decides which pin the pointer means (the smart pointer, below). ---- */
  const pins = pinGroup.selectAll('g.pin').data(episodes).enter().append('g').attr('class', 'pin');
  pins.each(function () {
    const g = d3.select(this);
    const ring = g.append('circle').attr('r', 4).attr('fill', 'none')
      .attr('stroke', 'var(--orange)').attr('stroke-width', 1.2).attr('opacity', 0.7);
    if (!reduceMotion) {
      ring.append('animate').attr('attributeName', 'r').attr('values', '4;13')
        .attr('dur', '2.2s').attr('repeatCount', 'indefinite');
      ring.append('animate').attr('attributeName', 'opacity').attr('values', '0.7;0')
        .attr('dur', '2.2s').attr('repeatCount', 'indefinite');
    }
    g.append('circle').attr('r', 3.2).attr('fill', 'var(--orange)')
      .attr('stroke', 'var(--bg)').attr('stroke-width', 1);
  });

  /* ---- Drawing the globe itself. ---- */
  function drawFarPins(R, cx, cy) {
    const rot = projection.rotate();
    const cdl = Math.cos(rot[0] * RAD), sdl = Math.sin(rot[0] * RAD);
    const cdp = Math.cos(rot[1] * RAD), sdp = Math.sin(rot[1] * RAD);
    ctx.beginPath();
    for (let i = 0; i < EP_VEC.length; i += 4) {
      const cl = EP_VEC[i], sl = EP_VEC[i + 1], cp = EP_VEC[i + 2], sp = EP_VEC[i + 3];
      const x = (cl * cdl - sl * sdl) * cp;
      if (x * cdp - sp * sdp >= -0.02) continue;             /* near side */
      const px = cx + R * (sl * cdl + cl * sdl) * cp;
      const py = cy - R * (sp * cdp + x * sdp);
      ctx.moveTo(px + 2, py);
      ctx.arc(px, py, 2, 0, TAU);
    }
    ctx.fillStyle = TOK.orange(0.34);
    ctx.fill();
  }

  function draw() {
    const R = projection.scale(), cx = width / 2, cy = height / 2;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = TOK.light(1);
    for (let i = 0; i < starPts.length; i++) {
      const s = starPts[i];
      ctx.globalAlpha = s[3];
      ctx.beginPath(); ctx.arc(s[0], s[1], s[2], 0, TAU); ctx.fill();
    }
    ctx.globalAlpha = 1;
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU);
    ctx.fillStyle = TOK.card(1); ctx.fill();
    ctx.save();
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.clip();
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU);
    ctx.fillStyle = TOK.bg(T.veil); ctx.fill();
    const rot = projection.rotate();
    back.scale(R).translate(projection.translate()).rotate([rot[0] + 180, -rot[1], 0]);
    ctx.beginPath(); backPath(GRAT);
    ctx.strokeStyle = TOK.light(T.backGrat); ctx.lineWidth = 1; ctx.stroke();
    if (LAND) {
      ctx.beginPath(); backPath(LAND);
      ctx.fillStyle = TOK.light(T.back); ctx.fill();
    }
    drawFarPins(R, cx, cy);
    ctx.beginPath(); path(GRAT);
    ctx.strokeStyle = TOK.light(T.grat); ctx.lineWidth = 1; ctx.stroke();
    if (LAND) {
      ctx.beginPath(); path(LAND);
      ctx.fillStyle = TOK.light(T.front); ctx.fill();
    }
    if (BORDERS) {
      ctx.beginPath(); path(BORDERS);
      ctx.strokeStyle = TOK.light(T.border); ctx.lineWidth = 0.6; ctx.stroke();
    }
    if (LAND) {
      ctx.beginPath(); path(LAND);
      ctx.strokeStyle = TOK.light(T.coast); ctx.lineWidth = 1; ctx.stroke();
    }
    ctx.restore();
  }

  function render() {
    draw();
    const rot = projection.rotate();
    const centre = [-rot[0], -rot[1]];
    pins.each(function (d) {
      const c = Math.cos(d3.geoDistance([d.lon, d.lat], centre));
      if (c <= 0) { this.style.display = 'none'; d._on = false; return; }
      const pos = projection([d.lon, d.lat]);
      d._on = true; d._x = pos[0]; d._y = pos[1];
      this.style.display = '';
      this.setAttribute('transform', 'translate(' + pos[0].toFixed(1) + ',' + pos[1].toFixed(1) + ')');
      /* Pins fade out towards the rim rather than vanishing at it. */
      this.style.opacity = Math.min(1, c / 0.34);
    });
    smartRefresh();
  }

  /* ---- Episode card. ---- */
  function showPopup(d) {
    const pos = projection([d.lon, d.lat]);
    if (!pos) return;

    /* Everything below comes from globe-episodes.js. Range and bearing are
       real: great circle distance and initial bearing from the Oslo coordinate
       printed in the site nav. Episodes pinned at the studio itself say where
       they are instead, because "0 km on 196 degrees" is a rounding artefact. */
    const slug = d.href.split('/').pop().replace('.html', '');
    const x = (window.GLOBE_EP || {})[slug] || null;
    const set = (sel, text) => {
      const el = popup.querySelector(sel);
      if (el) el.textContent = text || '';
    };
    popupTitle.textContent = (x && x.title) || d.title;
    popupLink.href = d.href;
    if (x) {
      const ns = x.lat >= 0 ? 'N' : 'S', ew = x.lon >= 0 ? 'E' : 'W';
      set('.mp-co', Math.abs(x.lat).toFixed(4) + '°' + ns + ' ' +
                    Math.abs(x.lon).toFixed(4) + '°' + ew);
      set('.mp-rng', x.home ? 'Oslo studio' : x.km.toLocaleString('en-GB') + ' km');
      set('.mp-brg', x.home ? '' : String(x.brg).padStart(3, '0') + '° ' + x.card);
      set('.mp-kick', [x.series, x.epno].filter(Boolean).join(' · ').toUpperCase());
      set('.mp-guest', x.guest);
      set('.mp-ch', x.nch === 1 ? '1 chapter' : (x.nch ? x.nch + ' chapters' : ''));
      set('.mp-dur', x.dur);
      const img = popup.querySelector('.mp-th img');
      const th = popup.querySelector('.mp-th');
      if (img && th) {
        if (x.video) {
          img.alt = x.title ? 'Episode thumbnail: ' + x.title : 'Episode thumbnail';
          img.src = 'https://i.ytimg.com/vi/' + x.video + '/maxresdefault.jpg';
          img.onerror = function () {
            this.onerror = null;
            this.src = 'https://i.ytimg.com/vi/' + x.video + '/mqdefault.jpg';
          };
          th.style.display = '';
        } else {
          th.style.display = 'none';   /* audio only: no still to show */
        }
      }
      if (!x.home) swingIndex(x.brg); else bzIndex.style('opacity', 0);
    } else {
      ['.mp-co', '.mp-rng', '.mp-brg', '.mp-kick', '.mp-guest', '.mp-ch', '.mp-dur'].forEach((s) => set(s, ''));
      bzIndex.style('opacity', 0);
    }

    /* Beside the pin, vertically centred on it, flipped to the other side when
       there is no room, then clamped inside the map. Made visible first: an
       element that is not displayed measures zero. */
    popup.classList.add('visible');
    const cw = container.clientWidth, ch = container.clientHeight;
    const pw = popup.offsetWidth || 336, ph = popup.offsetHeight || 370;
    const GAP = 22, EDGE = 10;
    let left = pos[0] + GAP;
    if (left + pw > cw - EDGE) left = pos[0] - GAP - pw;
    if (left < EDGE) left = Math.max(EDGE, (cw - pw) / 2);
    let top = pos[1] - ph / 2;
    top = Math.min(Math.max(EDGE, top), Math.max(EDGE, ch - ph - EDGE));
    popup.style.left = left + 'px';
    popup.style.top = top + 'px';
  }
  function hidePopup() {
    popup.classList.remove('visible');
    bzIndex.style('opacity', 0);
  }

  /* ---- Name under the pointer. ---- */
  function placeTip(d, title, sub) {
    if (!d._on) { tipEl.classList.remove('visible'); return; }
    tipEl.querySelector('b').textContent = title;
    tipEl.querySelector('i').textContent = sub;
    tipEl.classList.add('visible');
    const half = tipEl.offsetWidth / 2, th = tipEl.offsetHeight;
    const lift = 16;
    /* Above the pin, unless that would run off the top of the box. */
    const below = d._y - lift - th < 6;
    tipEl.classList.toggle('below', below);
    tipEl.style.left = Math.min(Math.max(d._x, half + 8), width - half - 8) + 'px';
    tipEl.style.top = (below ? d._y + lift : d._y - lift) + 'px';
  }
  function tipText(d) {
    const x = (window.GLOBE_EP || {})[d.href.split('/').pop().replace('.html', '')];
    return [(x && x.title) || d.title, (x && x.guest) || ''];
  }

  /* ---- Smart pointer. One handler for the whole globe picks the pin nearest
     the pointer, so a crowded area no longer depends on which pin happens to
     be drawn on top. Several pins on the same spot are pulled apart by a zoom
     instead of guessing which one was meant. ---- */
  const hoverRing = svg.append('circle').attr('class', 'gl-shell')
    .attr('fill', 'none').attr('stroke', 'var(--white)').attr('stroke-width', 1.5)
    .style('display', 'none');
  const coarse = window.matchMedia('(pointer: coarse)').matches;
  const REACH_MOUSE = 16, REACH_TOUCH = 22, STACK_PX = 9;
  let ptr = null;            /* last mouse position inside the box */
  let target = null;         /* { pin, stack, count } */
  let dragging = false;
  let hoverHold = false;
  let leaveTimer = null;
  let stillTimer = null;
  const STILL_MS = 3000;

  function localPoint(event) {
    const s = event.changedTouches ? event.changedTouches[0] : event;
    const r = container.getBoundingClientRect();
    return [s.clientX - r.left, s.clientY - r.top];
  }
  function inSphere(x, y, pad) {
    return Math.hypot(x - width / 2, y - height / 2) <= projection.scale() + (pad || 0);
  }
  function pick(x, y, reach) {
    let best = null, bd = reach;
    episodes.forEach((d) => {
      if (!d._on) return;
      const dist = Math.hypot(d._x - x, d._y - y);
      if (dist < bd) { bd = dist; best = d; }
    });
    if (!best) return null;
    /* Everything sitting on top of the chosen pin counts as one stack. */
    const stack = episodes.filter((d) => d._on && Math.hypot(d._x - best._x, d._y - best._y) < STACK_PX);
    return { pin: best, stack: stack, count: stack.length };
  }
  const zoomK = () => projection.scale() / baseScale;
  const canSplit = (t) => t.count > 1 && zoomK() < 30;

  function setCursor() {
    let c;
    if (dragging) c = 'grabbing';
    else if (target) c = 'pointer';
    else c = (ptr && inSphere(ptr[0], ptr[1])) ? 'grab' : 'default';
    svg.style('cursor', c);
  }
  function setTarget(t) {
    target = t;
    if (t) {
      hoverRing.style('display', null).attr('cx', t.pin._x).attr('cy', t.pin._y).attr('r', t.count > 1 ? 12 : 9);
      if (canSplit(t)) placeTip(t.pin, t.count + ' episodes here', 'Click to zoom in');
      else { const x = tipText(t.pin); placeTip(t.pin, x[0], x[1]); }
    } else {
      hoverRing.style('display', 'none');
      tipEl.classList.remove('visible');
    }
    setCursor();
  }
  function smartRefresh() {
    if (!ptr || dragging || !inSphere(ptr[0], ptr[1], 12)) { if (target) setTarget(null); else setCursor(); return; }
    setTarget(pick(ptr[0], ptr[1], REACH_MOUSE));
  }
  /* The globe holds still while the pointer moves over it, and for a moment
     after it leaves, so a pin never slides out from under the cursor. A pointer
     left resting on the globe does not freeze it for good: after three seconds
     without a move the hold is dropped and the pointer is forgotten until it
     moves again, so the spin comes back even while hovering. */
  function holdSpin() {
    if (leaveTimer) { clearTimeout(leaveTimer); leaveTimer = null; }
    if (!hoverHold) { hoverHold = true; syncSpin(); }
    clearTimeout(stillTimer);
    stillTimer = setTimeout(() => {
      stillTimer = null;
      ptr = null;
      setTarget(null);
      hoverHold = false;
      syncSpin();
    }, STILL_MS);
  }
  function releaseSpinSoon() {
    if (!hoverHold || leaveTimer) return;
    leaveTimer = setTimeout(() => { leaveTimer = null; hoverHold = false; syncSpin(); }, 900);
  }
  svg.on('pointermove', (event) => {
    if (event.pointerType !== 'mouse') return;
    ptr = localPoint(event);
    if (inSphere(ptr[0], ptr[1], 12)) holdSpin(); else releaseSpinSoon();
    smartRefresh();
  });
  svg.on('pointerleave', (event) => {
    if (event.pointerType !== 'mouse') return;
    ptr = null;
    clearTimeout(stillTimer); stillTimer = null;
    releaseSpinSoon();
    setTarget(null);
  });
  svg.on('click', (event) => {
    const p = localPoint(event);
    const touch = coarse || (event.pointerType && event.pointerType !== 'mouse');
    const t = inSphere(p[0], p[1], 12) ? pick(p[0], p[1], touch ? REACH_TOUCH : REACH_MOUSE) : null;
    if (!t) return;                      /* falls through and closes any open card */
    event.stopPropagation();
    /* The view is about to move under a pointer that is not moving. Forget
       where the pointer is until it moves again, so no stray name pops up
       beside the card. */
    ptr = null;
    setTarget(null);
    if (canSplit(t)) {
      const pts = t.stack.map((d) => [d.lon, d.lat]);
      const c = d3.geoCentroid({ type: 'MultiPoint', coordinates: pts });
      let spread = 0;
      pts.forEach((q) => { spread = Math.max(spread, d3.geoDistance(c, q)); });
      openGroup(c[0], c[1], spread);
    } else {
      openEpisode(t.pin);
    }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hidePopup(); });

  /* ---- Slow spin, only while it can be seen and nothing is open. The spin
     redraws the whole world about 33 times a second, so it stops off screen,
     in a background tab, and behind the episode popup. ---- */
  let autoRotateTimer = null, wantSpin = false, idleTimer = null, onScreen = false;
  function popupOpen() { return document.body.classList.contains('kb-modal-open'); }
  function syncSpin() {
    const run = wantSpin && onScreen && !document.hidden && !hoverHold && !popupOpen();
    if (run && !autoRotateTimer) {
      autoRotateTimer = d3.interval(() => {
        const r = projection.rotate();
        /* Slower the further in the view is, so the land drifts across the
           screen at the same gentle pace at any zoom. */
        projection.rotate([r[0] + 0.12 / Math.max(1, zoomK()), r[1]]);
        render();
      }, 30);
    } else if (!run && autoRotateTimer) { autoRotateTimer.stop(); autoRotateTimer = null; }
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((en) => { onScreen = en[0].isIntersecting; syncSpin(); },
      { rootMargin: '100px 0px' }).observe(container);
  } else { onScreen = true; }
  document.addEventListener('visibilitychange', syncSpin);
  new MutationObserver(syncSpin).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  function startAutoRotate() { wantSpin = true; syncSpin(); }
  function stopAutoRotate() { wantSpin = false; syncSpin(); }
  /* The spin comes back three seconds after the last touch, at whatever zoom
     the visitor left it. A click on a pin waits longer, so the card can be read
     before the globe takes it away. */
  function resetIdleTimer(ms) {
    if (idleTimer) clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      hidePopup();
      if (!reduceMotion) startAutoRotate();
    }, ms || 3000);
  }

  /* ---- Moving the view. ---- */
  const ZOOM_MIN = 1, ZOOM_MAX = 40;
  function syncZoom(k) {
    /* Keep d3.zoom's own transform in step, or the next wheel event would
       snap back to wherever it thinks the scale is. */
    svg.property('__zoom', d3.zoomIdentity.scale(k));
  }
  function flyTo(lon, lat, k, ms, done) {
    stopAutoRotate();
    const r0 = projection.rotate();
    /* Shortest way round, never 300 degrees east to travel 60 west. */
    const dLon = (((-lon) - r0[0] + 540) % 360) - 180;
    const r1 = [r0[0] + dLon, -lat, 0];
    const s0 = projection.scale();
    const s1 = k ? baseScale * Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, k)) : s0;
    const finish = () => {
      if (done) done();
      if (s1 !== s0) syncZoom(s1 / baseScale);
    };
    if (reduceMotion || !ms) {
      projection.rotate(r1).scale(s1); setR(s1); render(); finish();
      return;
    }
    d3.transition().duration(ms).ease(d3.easeCubicInOut)
      .tween('fly', () => {
        const ri = d3.interpolate(r0, r1);
        return (t) => {
          projection.rotate(ri(t));
          if (s1 !== s0) { const s = s0 * Math.pow(s1 / s0, t); projection.scale(s); setR(s); }
          render();
        };
      })
      .on('end', finish);
  }
  /* A click turns the pin to the middle before opening the card, so the card
     always opens in the same place with room around it. No zoom change: the
     view should not jump scale under somebody's hands. */
  function openEpisode(d) {
    hidePopup();
    flyTo(d.lon, d.lat, null, 650, () => { showPopup(d); resetIdleTimer(11000); });
  }
  function openGroup(lon, lat, spread) {
    hidePopup();
    const want = (60 / Math.max(spread, 0.004)) / baseScale;
    const k = Math.min(ZOOM_MAX, zoomK() * 10, Math.max(zoomK() * 1.8, want));
    flyTo(lon, lat, k, 800, () => resetIdleTimer(12000));
  }
  zoomEl.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    e.stopPropagation();
    hidePopup();
    const r = projection.rotate();
    if (b.dataset.zoom === 'reset') {
      flyTo(-HOME[0], -HOME[1], 1, 700, () => resetIdleTimer(900));
    } else {
      const k = zoomK() * (b.dataset.zoom === 'in' ? 1.8 : 1 / 1.8);
      flyTo(-r[0], -r[1], k, 350, () => resetIdleTimer());
    }
  });

  /* ---- Deep link: index.html#pin=<episode-slug> flies the globe to that
     episode as one continuous movement, with the card arriving as it settles.
     The map is put on screen first and held there for a moment, because scroll
     restoration, images still arriving above it, ScrollTrigger and the
     back/forward cache all move the page after this runs. The visitor always
     wins: one wheel, touch or key and the hold lets go. ---- */
  const FLY_MS = 1900;
  const FLY_ZOOM = 14;       /* about 25 to 30 degrees of longitude across the frame */
  let holdUntil = 0, holding = false;
  function holdOnMap(ms) {
    holdUntil = Date.now() + ms;
    if (holding) return;
    holding = true;
    (function keep() {
      if (Date.now() > holdUntil) { holding = false; return; }
      if (window.ScrollTrigger && window.ScrollTrigger.refresh) {
        try { window.ScrollTrigger.refresh(); } catch (e) {}
      }
      container.scrollIntoView({ block: 'center' });
      requestAnimationFrame(keep);
    })();
  }
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach((evt) => {
    window.addEventListener(evt, () => { holdUntil = 0; }, { passive: true });
  });
  function pinSlugFromHash() {
    const m = /^#pin=(.+)$/.exec(location.hash || '');
    if (!m) return null;
    try { return decodeURIComponent(m[1]); } catch (e) { return null; }
  }
  function findPin(slug) {
    return slug ? episodes.find((e) => e.href === 'episodes/' + slug + '.html') : null;
  }
  if (findPin(pinSlugFromHash())) {
    try { history.scrollRestoration = 'manual'; } catch (e) {}
    holdOnMap(1200);
    window.addEventListener('load', () => {
      if (findPin(pinSlugFromHash())) holdOnMap(900);
    });
  }
  /* No idle timer here: somebody who followed a link to one episode should not
     have its card vanish while they read it. Their first drag or zoom brings
     back the normal behaviour. */
  function openPinFromHash() {
    const d = findPin(pinSlugFromHash());
    if (!d) return;          /* unknown slug: leave the globe exactly as it was */
    holdOnMap(900);
    hidePopup();
    flyTo(d.lon, d.lat, FLY_ZOOM, reduceMotion ? 0 : FLY_MS, () => showPopup(d));
  }
  window.addEventListener('hashchange', openPinFromHash);
  window.addEventListener('pageshow', (ev) => { if (ev.persisted) openPinFromHash(); });

  /* ---- Drag to turn. Only the globe itself can be grabbed, and not where a
     click would open a pin; the empty corners of the box are left alone. ---- */
  let dragStart = null, rotateStart = projection.rotate(), pinching = false;
  const node = svg.node();
  node.addEventListener('touchstart', (e) => { if (e.touches.length > 1) pinching = true; }, { passive: true });
  node.addEventListener('touchend', (e) => { if (e.touches.length < 2) pinching = false; }, { passive: true });
  node.addEventListener('touchcancel', () => { pinching = false; }, { passive: true });

  svg.call(d3.drag()
    .filter((event) => {
      if (event.touches && event.touches.length > 1) return false;
      const p = localPoint(event);
      if (!inSphere(p[0], p[1], 12)) return false;
      return !pick(p[0], p[1], event.touches || coarse ? REACH_TOUCH : REACH_MOUSE);
    })
    .on('start', (event) => {
      dragStart = [event.x, event.y];
      rotateStart = projection.rotate();
      dragging = true; setCursor();
      stopAutoRotate();
      resetIdleTimer();
    })
    .on('drag', (event) => {
      if (pinching) return;
      const dx = event.x - dragStart[0], dy = event.y - dragStart[1];
      const degPerPixel = 180 / (Math.PI * projection.scale());
      const newLat = Math.max(-90, Math.min(90, rotateStart[1] - dy * degPerPixel));
      projection.rotate([rotateStart[0] + dx * degPerPixel, newLat]);
      hidePopup();
      render();
      resetIdleTimer();
    })
    .on('end', () => { dragging = false; setCursor(); smartRefresh(); resetIdleTimer(); }));

  /* ---- Zoom. A plain scroll is left to the page; zooming needs Ctrl or Cmd,
     which is also what a trackpad pinch sends. A scroll over the globe without
     it shows a hint saying so. ---- */
  svg.call(d3.zoom()
    .scaleExtent([ZOOM_MIN, ZOOM_MAX])
    .filter((event) => event.type === 'wheel' && (event.ctrlKey || event.metaKey))
    /* A trackpad pinch arrives as tiny steps with Ctrl set and needs the usual
       boost. A real wheel held with Ctrl arrives in big steps and must not get
       it, or one notch would jump most of the way in. */
    .wheelDelta((e) => {
      const unit = e.deltaMode === 1 ? 0.05 : e.deltaMode ? 1 : 0.002;
      const pinch = e.ctrlKey && Math.abs(e.deltaY) < 40;
      return -e.deltaY * unit * (pinch ? 10 : 2);
    })
    .on('zoom', (event) => {
      const k = event.transform.k;
      projection.scale(baseScale * k);
      setR(baseScale * k);
      tipEl.classList.remove('visible');
      render();
      stopAutoRotate();
      resetIdleTimer();
    }));

  const isMac = /Mac|iPhone|iPad/.test(navigator.platform || '');
  hintEl.textContent = 'Hold ' + (isMac ? '⌘' : 'Ctrl') + ' and scroll to zoom';
  let hintTimer = null;
  container.addEventListener('wheel', (e) => {
    if (e.ctrlKey || e.metaKey) return;
    const p = localPoint(e);
    if (!inSphere(p[0], p[1])) return;
    hintEl.classList.add('visible');
    clearTimeout(hintTimer);
    hintTimer = setTimeout(() => hintEl.classList.remove('visible'), 1400);
  }, { passive: true });

  /* PINCH TO ZOOM, done by hand, in the capture phase: d3-drag stops the
     touchmove of the first finger before a later listener could see it. */
  let pinchStartDist = 0, pinchStartScale = 0;
  const touchDist = (t) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
  node.addEventListener('touchstart', (e) => {
    if (e.touches.length !== 2) return;
    pinchStartDist = touchDist(e.touches);
    pinchStartScale = projection.scale();
    stopAutoRotate();
    resetIdleTimer();
  }, { passive: true, capture: true });
  node.addEventListener('touchmove', (e) => {
    if (e.touches.length !== 2 || !pinchStartDist) return;
    e.preventDefault();
    let sc = pinchStartScale * touchDist(e.touches) / pinchStartDist;
    sc = Math.max(baseScale * ZOOM_MIN, Math.min(baseScale * ZOOM_MAX, sc));
    projection.scale(sc);
    setR(sc);
    syncZoom(sc / baseScale);
    hidePopup();
    render();
    resetIdleTimer();
  }, { passive: false, capture: true });
  node.addEventListener('touchend', (e) => { if (e.touches.length < 2) pinchStartDist = 0; }, { passive: true, capture: true });
  node.addEventListener('touchcancel', () => { pinchStartDist = 0; }, { passive: true, capture: true });

  document.addEventListener('click', hidePopup);
  popup.addEventListener('click', (e) => e.stopPropagation());

  /* ---- Sizing. Measured whenever the box changes, keeping the visitor's
     zoom: on a phone the box may have no height yet when this first runs. ---- */
  function resize() {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return false;
    const k = zoomK() || 1;
    width = w; height = h;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    baseScale = Math.min(w, h) / fitDiv(w);
    projection.scale(baseScale * k).translate([w / 2, h / 2]);
    svg.attr('width', w).attr('height', h);
    layoutStars();
    setR(baseScale * k);
    render();
    return true;
  }
  if (window.ResizeObserver) {
    let t = null;
    new ResizeObserver(() => { clearTimeout(t); t = setTimeout(resize, 80); }).observe(container);
  } else {
    window.addEventListener('resize', resize);
  }

  resize();
  openPinFromHash();
  if (!reduceMotion && !findPin(pinSlugFromHash())) startAutoRotate();
})();
