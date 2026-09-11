// Interactive episode globe — D3 orthographic projection, drag to rotate
(function () {
  const container = document.getElementById('epMap');
  if (!container || !window.d3 || !window.topojson) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const popup = document.getElementById('mapPopup');
  const popupGuest = popup.querySelector('.popup-guest');
  const popupTitle = popup.querySelector('.popup-title');
  const popupLink = popup.querySelector('.popup-link');

  const width = container.clientWidth;
  const height = container.clientHeight;

  const projection = d3.geoOrthographic()
    .scale(Math.min(width, height) / 2.2)
    .translate([width / 2, height / 2])
    .clipAngle(90)
    .rotate([-20, -15]);

  const path = d3.geoPath(projection);

  const svg = d3.select(container)
    .insert('svg', '#mapPopup')
    .attr('width', width)
    .attr('height', height)
    .style('display', 'block')
    .style('cursor', 'grab');

  const sphere = svg.append('circle')
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', projection.scale())
    .attr('fill', 'var(--card)')
    .attr('stroke', 'rgba(180,180,180,0.3)');

  const graticule = d3.geoGraticule();
  const graticulePath = svg.append('path')
    .datum(graticule())
    .attr('fill', 'none')
    .attr('stroke', 'rgba(180,180,180,0.12)')
    .attr('d', path);

  const landPath = svg.append('path')
    .attr('fill', 'rgba(180,180,180,0.4)')
    .attr('stroke', 'rgba(20,21,25,0.4)')
    .attr('stroke-width', 0.5);

  // All 79 real episode titles, with locations inferred from cues in each title/guest
  // (nationality, named place, or brand HQ). Only the ~21 most recent have a confirmed
  // direct episode link from the RSS feed — the rest link to the main show page until
  // real per-episode links are supplied.
  const showUrl = 'https://open.spotify.com/show/16jBM3RfjVERukNHJrIRec';
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
    ['Snippet: A Reserve Parachute Trick Every Pilot Should Know, by Urs Haari', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Snippet-A-Reserve-Parachute-Trick-Every-Pilot-Should-Know--by-Urs-Haari-e3c6unr', 8.2, 46.8],
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
    return { title, href, lon: lon + jitterLon, lat: lat + jitterLat };
  });

  const pinGroup = svg.append('g');

  function isVisible(lon, lat) {
    const rotate = projection.rotate();
    const center = [-rotate[0], -rotate[1]];
    return d3.geoDistance([lon, lat], center) < Math.PI / 2;
  }

  function showPopup(d) {
    const pos = projection([d.lon, d.lat]);
    if (!pos) return;
    popupGuest.textContent = 'Paragliding Atlas Podcast';
    popupTitle.textContent = d.title;
    popupLink.href = d.href;
    popup.style.left = pos[0] + 'px';
    popup.style.top = pos[1] + 'px';
    popup.classList.add('visible');
  }

  function hidePopup() {
    popup.classList.remove('visible');
  }

  function render() {
    graticulePath.attr('d', path);
    landPath.attr('d', path);

    const pins = pinGroup.selectAll('g.pin').data(episodes);

    const pinsEnter = pins.enter()
      .append('g')
      .attr('class', 'pin')
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        event.stopPropagation();
        showPopup(d);
        stopAutoRotate();
        resetIdleTimer();
      });

    // Generous invisible hit area — makes clicking far more forgiving than the visible dot alone
    pinsEnter.append('circle')
      .attr('class', 'pin-hit')
      .attr('r', 14)
      .attr('fill', 'transparent');

    // Outer pulsing ring — radar-blip style
    const ring = pinsEnter.append('circle')
      .attr('class', 'pin-ring')
      .attr('r', 4)
      .attr('fill', 'none')
      .attr('stroke', 'var(--orange)')
      .attr('stroke-width', 1.2)
      .attr('opacity', 0.7);

    if (!reduceMotion) {
      ring.append('animate')
        .attr('attributeName', 'r')
        .attr('values', '4;13')
        .attr('dur', '2.2s')
        .attr('repeatCount', 'indefinite');
      ring.append('animate')
        .attr('attributeName', 'opacity')
        .attr('values', '0.7;0')
        .attr('dur', '2.2s')
        .attr('repeatCount', 'indefinite');
    }

    // Solid core
    pinsEnter.append('circle')
      .attr('class', 'pin-core')
      .attr('r', 3.2)
      .attr('fill', 'var(--orange)')
      .attr('stroke', 'var(--bg)')
      .attr('stroke-width', 1);

    pinsEnter.merge(pins)
      .attr('transform', d => {
        const pos = projection([d.lon, d.lat]);
        return pos ? `translate(${pos[0]},${pos[1]})` : 'translate(-9999,-9999)';
      })
      .style('display', d => isVisible(d.lon, d.lat) ? null : 'none');
  }

  /* Deep link: index.html#pin=<episode-slug> flies the globe to that episode.

     THE POINT IS THAT IT IS ONE MOVEMENT, NOT THREE.
     The first version jumped: page at the top, then a scroll, then a globe
     already rotated. Three separate events that read as a page assembling
     itself. Now the map is put on screen before anything is drawn, and the
     globe turns and pushes in as a single continuous shot, with the popup
     arriving as it settles.

     Called after the first render, never at script end: the land data arrives
     asynchronously and the projection must have drawn once before showPopup can
     place the popup correctly. */

  const FLY_MS = 1900;        /* long enough to read as travel, short enough to sit through */
  const FLY_ZOOM = 14;       /* within the wheel zoom's own 1 to 40 range.
                                 Set from a screenshot of the framing the user
                                 wanted, not by eye. The map is 1400 by 600 and
                                 baseScale is min(w,h)/2.2 = 272.7, so the arc
                                 visible across the width is
                                 2*asin(700 / (272.7*k)) degrees:
                                   k=3.2 -> 107 deg arc, ~150 deg of longitude
                                   k=6   ->  51 deg arc,  ~73 deg
                                   k=10  ->  30 deg arc,  ~43 deg
                                   k=14  ->  21 deg arc,  ~31 deg   <- this
                                 Counting graticule lines in the screenshot gave
                                 25 to 30 degrees of longitude across the frame.
                                 This is the only knob: the sphere radius and the
                                 projection scale both follow it, and the popup
                                 sits at the centre whatever it is set to. */

  function pinSlugFromHash() {
    const m = /^#pin=(.+)$/.exec(location.hash || '');
    return m ? decodeURIComponent(m[1]) : null;
  }

  function findPin(slug) {
    return slug ? episodes.find((e) => e.href === 'episodes/' + slug + '.html') : null;
  }

  /* Put the map on screen straight away, before the land has even loaded, so
     the visitor's first sight of the page is the globe rather than the top of
     the homepage. No smooth scroll here on purpose: an animated scroll followed
     by an animated flight is the stacking that looked artificial.

     THREE THINGS FIGHT THIS AND ALL THREE HAD TO BE HANDLED.

     1. SCROLL RESTORATION. The browser restores the scroll position it last had
        for a URL, and it does that AFTER this runs, so it lands on top of ours
        and the visitor sits at the top of the homepage. This is exactly why
        ctrl-clicking the link worked and plain clicking it did not: a new tab
        has no stored position to restore. Turned off for this arrival only.

     2. LAYOUT STILL MOVING. Images above the map are still arriving when this
        runs, so the position computed here drifts. Asserted again on load.

     3. THE BACK/FORWARD CACHE. Coming back to this page from history restores
        the whole document without re-running any of this, so `pageshow` with
        `persisted` is the only hook that fires. */
  /* 4. GSAP. script.js reveals `.ep-map-section` with a ScrollTrigger, so the
        section is transformed and ScrollTrigger recalculates every position on
        load. A single scrollIntoView lands correctly and is then moved out from
        under itself.

     So rather than scrolling once and hoping, hold the map on screen for the
     first second and give way the instant the visitor touches anything. */
  let holdUntil = 0;
  let holding = false;

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

  /* The visitor always wins. One wheel, touch or key and we stop immediately,
     so this can never feel like the page is fighting them. */
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach((evt) => {
    window.addEventListener(evt, () => { holdUntil = 0; }, { passive: true });
  });

  if (findPin(pinSlugFromHash())) {
    try { history.scrollRestoration = 'manual'; } catch (e) {}
    holdOnMap(1200);
    window.addEventListener('load', () => {
      if (findPin(pinSlugFromHash())) holdOnMap(900);
    });
  }

  function flyTo(d, animate) {
    stopAutoRotate();

    const r0 = projection.rotate();
    /* Shortest way round. A plain interpolation between longitudes can send the
       globe the long way, 300 degrees east to travel 60 degrees west. */
    const dLon = (((-d.lon) - r0[0] + 540) % 360) - 180;
    const r1 = [r0[0] + dLon, -d.lat, r0[2] || 0];
    const s0 = projection.scale();
    const s1 = baseScale * FLY_ZOOM;

    function settle() {
      /* The popup FIRST. Syncing d3.zoom's transform is housekeeping for the
         next wheel event; opening the popup is the entire point of the journey.
         Had these been the other way round, any failure in the zoom sync would
         have thrown before the popup appeared, and the visitor would have
         watched the globe fly somewhere and then show them nothing. */
      showPopup(d);
      try {
        /* Keep d3.zoom's own transform in step, or the next wheel event would
           snap back to wherever it thinks the scale is. */
        svg.call(zoom.transform, d3.zoomIdentity.scale(FLY_ZOOM));
      } catch (e) {
        /* Worst case the next wheel event jumps once. Not worth losing the
           popup over. */
      }
    }

    if (!animate) {
      projection.rotate(r1).scale(s1);
      sphere.attr('r', s1);
      render();
      settle();
      return;
    }

    d3.transition()
      .duration(FLY_MS)
      .ease(d3.easeCubicInOut)
      .tween('flyTo', () => {
        const ri = d3.interpolate(r0, r1);
        const si = d3.interpolate(s0, s1);
        return (k) => {
          projection.rotate(ri(k)).scale(si(k));
          sphere.attr('r', si(k));
          render();
        };
      })
      .on('end', settle);
  }

  function openPinFromHash() {
    const d = findPin(pinSlugFromHash());
    if (!d) return;          /* unknown slug: leave the globe exactly as it was */
    holdOnMap(900);
    flyTo(d, !reduceMotion);
  }

  /* resetIdleTimer() is deliberately NOT called anywhere in here. Clicking a pin
     normally starts a 5 second timer that hides the popup and resumes the spin,
     which is right for browsing. Someone who followed a link to one specific
     episode should not have it vanish while they read it, so the globe holds
     still until they touch it. Their first drag or wheel resumes the normal
     behaviour. */

  /* Someone already on the page who follows another #pin link, and the back
     button moving between pins once they are shareable. */
  window.addEventListener('hashchange', openPinFromHash);

  /* Restored from the back/forward cache: the document comes back intact and no
     script re-runs, so this is the only chance to fly again. */
  window.addEventListener('pageshow', (ev) => {
    if (ev.persisted) openPinFromHash();
  });

  d3.json('https://unpkg.com/world-atlas@2/land-110m.json').then((world) => {
    const land = topojson.feature(world, world.objects.land);
    landPath.datum(land);
    render();
    openPinFromHash();
  }).catch(() => {
    render();
    openPinFromHash();
  });

  // Drag to rotate — degrees-per-pixel scaled to the globe's actual radius
  let dragStart = null;
  let rotateStart = projection.rotate();

  const drag = d3.drag()
    .filter((event) => {
      // Don't let a click/drag on a pin (or its hit area) start rotating the globe —
      // this was the cause of clicks feeling unreliable.
      const t = event.target;
      return !(t.classList && (t.classList.contains('pin-hit') || t.classList.contains('pin-ring') || t.classList.contains('pin-core')));
    })
    .on('start', (event) => {
      dragStart = [event.x, event.y];
      rotateStart = projection.rotate();
      svg.style('cursor', 'grabbing');
      stopAutoRotate();
      resetIdleTimer();
    })
    .on('drag', (event) => {
      const dx = event.x - dragStart[0];
      const dy = event.y - dragStart[1];
      const degPerPixel = 180 / (Math.PI * projection.scale());
      const newLat = Math.max(-90, Math.min(90, rotateStart[1] - dy * degPerPixel));
      projection.rotate([rotateStart[0] + dx * degPerPixel, newLat]);
      render();
      hidePopup();
      resetIdleTimer();
    })
    .on('end', () => {
      svg.style('cursor', 'grab');
      resetIdleTimer();
    });

  svg.call(drag);

  // Scroll-to-zoom — only active while the cursor is over the globe itself.
  // d3.zoom's wheel handler calls preventDefault() only for wheel events that
  // land on this svg element, so page scroll is completely unaffected elsewhere.
  const baseScale = projection.scale();
  const zoom = d3.zoom()
    .scaleExtent([1, 40])
    .filter((event) => event.type === 'wheel')
    .on('zoom', (event) => {
      const k = event.transform.k;
      projection.scale(baseScale * k);
      sphere.attr('r', baseScale * k);
      render();
      stopAutoRotate();
      resetIdleTimer();
    });

  svg.call(zoom);

  document.addEventListener('click', hidePopup);
  popup.addEventListener('click', (e) => e.stopPropagation());

  // Gentle auto-rotate until the person interacts
  let autoRotateTimer = null;
  function startAutoRotate() {
    autoRotateTimer = d3.interval(() => {
      const r = projection.rotate();
      projection.rotate([r[0] + 0.12, r[1]]);
      render();
    }, 30);
  }
  function stopAutoRotate() {
    if (autoRotateTimer) {
      autoRotateTimer.stop();
      autoRotateTimer = null;
    }
  }

  // Resume gentle auto-rotation 5s after the last drag/zoom/click interaction
  let idleTimer = null;
  function resetIdleTimer() {
    if (idleTimer) clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      hidePopup();
      if (!reduceMotion) startAutoRotate();
    }, 5000);
  }
  if (!reduceMotion) startAutoRotate();
})();
