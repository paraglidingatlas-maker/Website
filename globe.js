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
    ['Luc Armant talks about The Moment Coefficient, Enzo 3 Certification Debate & Physics of Stability', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Luc-Armant-talks-about-The-Moment-Coefficient--Enzo-3-Certification-Debate--Physics-of-Stability-e3o6qb5', -3.66, 37.68],
    ['Technical Masterclass by Brett Janaway: Science of Paraglider Trimming, Performance & New Legalities', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Technical-Masterclass-by-Brett-Janaway--Science-of-Paraglider-Trimming-Performance--New-Legalities-e3nshjb', -5.28, 40.46],
    ['Robert (Robbie) Whittall: 113 mins of Unhinged Conversations With The Man Behind Ozone Paragliders', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Robert-Robbie-Whittall-113-mins-of-Unhinged-conversations-with-The-Man-Behind-Ozone-Paragliders-e3nkg0l', 6.13, 45.9],
    ["Metacognition: Paragliding's Hidden Psychology with Beni Kalin & Heli Schrempf", 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Metacognition-Paraglidings-Hidden-Psychology-with-Beni-Kalin--Heli-Schrempf-e3n6aeu', 13.4, 47.3],
    ['The Russell Ogden Interview: Decoding The Paragliding Mastery Protocol', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/The-Russell-Ogden-Interview-Decoding-The-Paragliding-Mastery-Protocol-Progression--Fear--Competition-e3ld21b', -1.9, 52.5],
    ['Paragliding Physiology & Safety Protocols — Dr Matt Wikes Explains Biophysics in the Art of Flight', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Paragliding-Physiology--Safety-Protocols--Dr-Matt-Wikes-Explains-Biophysics-in-the-Art-of-Flight-e3i8068', -1.5, 52.0],
    ['If You Fly in the Himalayas, Alps, or Above 3000mtrs, This Episode Is For You — ft. Dr Matt Wikes', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/If-you-fly-in-the-Himalayas--Alps--or-above-3000-mtrs--this-episode-is-for-you---ft--Dr-Matt-Wikes-e3i3gda', 76.7, 32.0],
    ['Cognitive Bias of Dunning Kruger Effect in Paragliding — Beni Kalin & Heli Schrempf', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Cognitive-Bias-of-Dunning-Kruger-Effect-in-Paragliding--Explained-by-Beni-Kalin--Heli-Schrempf-e3hns3m', 13.4, 47.3],
    ['Sports Psychology for Paragliding: Train Your Mind to Fly Better with Yvonne Dathe', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Sports-Psychology-for-Paragliding-Train-Your-Mind-to-Fly-Better-with-Yvonne-Dathe-e3h150v', 10.4, 51.2],
    ["From Cuba to Socotra: Inside the World's Most Unique Paragliding Tours", 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/From-Cuba-to-Socotra-Inside-the-Worlds-Most-Unique-Paragliding-Tours-e3gnq77', -79.9, 21.5],
    ['How to Fly With Your Dog — Explained by Shams', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/How-to-Fly-With-Your-Dog--Explained-by-Shams-e3gg20j', 6.9, 45.9],
    ['Survived 15 Years of Flying Then a Rescue Helicopter Changed Everything — A Talk With Nick Neynens', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Survived-15-Years-of-Flying-Then-a-Rescue-Helicopter-Changed-Everything--A-Talk-With-Nick-Neynes-e3fvupf', 4.35, 50.85],
    ["From Tents to Trophies: Understanding Acro Champion's Mindset on Ego, Glory & Drugs — Luke De Weert", 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/From-Tents-to-Trophies-Understanding-Acro-Champions-Mindset-on-Ego--Glory--Drugs--Luke-De-Weert-e3eb0ve', 5.3, 52.1],
    ['Tom Lolies Explains The Science Of Wing Design and Evolution from ENC to CSC', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Tom-Lolies-Explains-The-Science-Of-Wing-Design-and-Evolution-from-ENC-to-CSC-e3da9jn', 4.35, 50.85],
    ["The Art of Capturing Human Flight — Jake Holland's Guide to Filming Passion Projects", 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/The-Art-of-Capturing-Human-Flight--Jake-Hollands-Guide-to-Filming-Passion-Projects-in-Paragliding-e3cra14', -2.5, 53.4],
    ["Master the Art of Scoring in Paragliding: A New Pilot's Guide to the GAP Formula & Strategy — Joerg Ewald", 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Master-the-Art-of-Scoring-in-Paragliding-A-New-Pilots-Guide-to-the-GAP-Formula--Strategy--Joerg-Ewald-e3cegbg', 10.4, 51.2],
    ['Snippet: A Reserve Parachute Trick Every Pilot Should Know — Urs Haari', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Snippet-A-Reserve-Parachute-Trick-Every-Pilot-Should-Know--by-Urs-Haari-e3c6unr', 8.2, 46.8],
    ['Watch This Before You Buy a Paragliding Harness — A Talk With Zsolt Ero', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Watch-this-Before-you-Buy-a-Paragliding-Harness--A-Talk-with-Zsolt-Ero-e3bsglh', 19.0, 47.5],
    ['The Inside Story of Sports Racing Series (SRS) by Brett Janaway', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/The-Inside-Story-of-Sports-Racing-Series-SRS-by-Brett-Janaway-e3b7t4g', -1.9, 52.5],
    ['The Unfiltered Truth About Paragliding Governance — Bill Hughes & Goran Dimiskovski', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/The-Unfiltered-Truth-About-Paragliding-Governance-with-Bill-Hughes--Goran-Dimiskovski-e3apoo6', 21.7, 41.6],
    ['Bill Belcourt: The Uncomfortable Truth No One Is Talking About in the Current Safety Paradox', 'https://podcasters.spotify.com/pod/show/paragliding-atlas/episodes/Bill-Belcourt-The-Uncomfortable-Truth-No-One-is-Talking-about-in-the-Current-Safety-Paradox-e3a7or9', -111.6, 40.6],
    ['Bruce Goldsmith Explains MRT Scoring System and Its Impact on Paragliding Competitions', showUrl, -1.9, 52.5],
    ['Luc Armant Talks About Debunking the Myths and Upgrading Enzo 3', showUrl, 6.13, 45.9],
    ['Insights From The Gaggle with Tilen Ceglar & Stan Radzikowski', showUrl, 14.8, 46.1],
    ['Pal Takats on Challenges, Change & The Future of Paragliding', showUrl, 19.0, 47.5],
    ['#CIVLRESIGN with Julien Garcia', showUrl, 2.35, 48.85],
    ['Anatomy of a Dream with Damien Lacaze: A Lifestyle Full of Grit, Grace and Vertical Freedom', showUrl, 6.13, 45.9],
    ['Demystifying The Science Behind Endless Fun Factor of Parakites With Bryan Van Ostheim', showUrl, 4.35, 50.85],
    ['Legacy and Lifetimes of Gin Seok Song: 5 Decades of Pioneering the Art of Free Flight', showUrl, 127.8, 36.5],
    ['Maxime Pinot: The Journey Within — Mapping Our Quest to Touch The Sky With Glory', showUrl, 6.13, 45.9],
    ["Understanding Skymate: Paragliding World's First AI Powered Smart Harness System with Roman Barthelemy", showUrl, 2.35, 48.85],
    ['Science Backed Pre Flight Rituals to Unlock Laser Sharp Paragliding Clarity: On Demand', showUrl, 10.75, 59.91],
    ["The Resilience Equation: Erlend Ukvitne's Unrelenting Path to X-Alps and the Brink of a Hike and Fly World Record", showUrl, 8.5, 60.5],
    ['Mastering the Unknown: Neuroscience of Crisis Management & Neuroplasticity Training', showUrl, 10.75, 59.91],
    ["Consequence Over Probability: Will Gadd's Field Protocols for Rewiring Risk Intuition and Why True Safety Lies in Clarity", showUrl, -106, 56],
    ["Why Paragliding's Safety Future Looks Different: RAST Inventor Michael Nesler & the LeelooX Effect", showUrl, 10.4, 51.2],
    ['Grant Smith: The Silent Mind In Screaming Winds — Unlocking Peak Focus To Attain Flow State In Paragliding', showUrl, -1.9, 52.5],
    ["Meteorology 101: A Beginner's Guide to Understanding Weather Apps and Decoding Endless Forecasting Options", showUrl, 10.75, 59.91],
    ['Urs Haari: The Real Truth About Reserve Parachutes — A Paragliding Survival Guide', showUrl, 8.2, 46.8],
    ["Shane Tighe's Road to X-Alps: Engineering Conquests In The Sky from Australia's Flatlands to the Pinnacle of Hike and Fly", showUrl, 133.8, -25.3],
    ["Aljaž Valič: 777 — Paragliding's Slovenian Mavericks Redefining the EN B Class And Elevating Free Flight Performance", showUrl, 14.8, 46.1],
    ['Sandrine Roy: Vol Biv & Freedom Unfiltered — A Human-Powered Odyssey By Paragliding, Biking & Sailing Around The Globe', showUrl, 2.35, 48.85],
    ['Alain Zoller: The Science of EN Certifications — How Work Group 6 Shaped Paragliding Testing, Innovation & Safety', showUrl, 8.2, 46.8],
    ['Ziad Bassil: Finest Paragliding Reviews & Superpower of Changing Wings as A Human', showUrl, 35.5, 33.9],
    ['Eddie Colfox: Storytime — Chasing Adventure With the Real OG John Silvester & 3 Decades of Making Memories Across The Globe', showUrl, -1.9, 52.5],
    ["Ashutosh Chopra: Identifying Passion Vs Obsession — An Aviator's Approach to Overcoming Adversity, Rebuilding Trust and Finding Joy in the Skies", showUrl, 78.9, 20.6],
    ['Kinga Masztalerz: Building a Healthy Relationship with the Skies — How to Master Fear, Build Resilience & Find Joy Through Paragliding', showUrl, 19.1, 52.2],
    ['Helmut Schrempf: Modernizing SIV Courses — How This New Training Method Can Help You Master Glider Control and Improve Paragliding Safety', showUrl, 13.4, 47.3],
    ['A Note of Thanks', showUrl, 10.75, 59.91],
    ['Storytellers: Marko Milutinovic (Mid-Air Collision)', showUrl, 21.0, 44.0],
    ['New Technologies 5: Frantisek Pavlousek (UP Paragliders)', showUrl, 15.5, 49.8],
    ['Flying & Filming 3: Andreas Lattner (hochzwei.media)', showUrl, 10.4, 51.2],
    ['Flying & Filming 2: Benjamin Kellet', showUrl, -1.9, 52.5],
    ['Risk Vs Reward 5: Gabriel Orsini (partytillimpact)', showUrl, 12.5, 41.9],
    ['Helmet Safety: Christian Ciech — ICARO 2000 [1st Anniversary Edition]', showUrl, 12.5, 41.9],
    ['Risk Vs Reward 4: Raúl Rodríguez', showUrl, -3.7, 40.4],
    ['Brand Stories: Neo — Eric Roussel', showUrl, 6.13, 45.9],
    ['Carabiner Fatigue: Finsterwalder & Charly (Whitepaper)', showUrl, 10.4, 51.2],
    ['Flying & Filming 1: Benjamin Jordan', showUrl, -106, 56],
    ['Living The Dream: Benjamin Jordan', showUrl, -106, 56],
    ['Risk Vs Reward 3: Manfred Ruhmer', showUrl, 13.4, 47.3],
    ['Risk Vs Reward 2: Subir Sidhu', showUrl, 78.9, 20.6],
    ['Risk Vs Reward 1: Philipp Zellner', showUrl, 13.4, 47.3],
    ['New Technologies 4: Veselin Ovcharov (Fly The Earth)', showUrl, 25.5, 42.7],
    ['New Technologies 3: Stephan Stiegler (AirDesign Paragliders)', showUrl, 13.4, 47.3],
    ['New Technologies 2: Guillem Batlle & Adrià Grau (Niviuk Paragliders)', showUrl, 2.15, 41.4],
    ['New Technologies 1: Beni Kälin (speedflyingschool.com)', showUrl, 8.2, 46.8],
    ['PWC Lifestyle: Klaudia Bulgakow', showUrl, 19.1, 52.2],
    ['PWCA: Goran Dimiskovski', showUrl, 21.7, 41.6],
    ['Pre PWC Kenya: Nikolay Yotov', showUrl, 36.8, -1.3],
    ['Navigating Panchgani (Pre PWC India): Vistasp Kharas', showUrl, 73.8, 17.9],
    ['AMA #1', showUrl, 10.75, 59.91],
    ['Navigating Australia: Godfrey Wenness', showUrl, 133.8, -25.3],
    ['Sky Gods: Flying to Win — Honorin Hamard', showUrl, 6.13, 45.9],
    ['Sky Gods: Flying 8000ers — Antoine Girard', showUrl, 86.9, 27.98],
    ['Navigating India: Jigish Gohil (Bonus Ep)', showUrl, 78.9, 20.6],
    ['Navigating India: Eddie Colfox', showUrl, 78.9, 20.6],
    ['Navigating Colombia: Pal Takats', showUrl, -74.3, 4.6],
    ['Touch The Sky With Glory', showUrl, 10.75, 59.91]
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

  d3.json('https://unpkg.com/world-atlas@2/land-110m.json').then((world) => {
    const land = topojson.feature(world, world.objects.land);
    landPath.datum(land);
    render();
  }).catch(() => {
    render();
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
