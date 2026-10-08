# Source dossier: paragliding physics (encyclopedia answer pages)

Compiled 2026-10-08 for five answer pages on paraglidingatlas.com. Every fact below was taken from a URL that was actually fetched on that date. The excerpts are verbatim as returned by the fetch tool and are each under 40 words. Where the tool returned only part of a sentence, the excerpt starts or ends with "...". Paraphrase from these excerpts. Do not copy copyrighted wording onto the site.

## How to use this file

- **Fact** is written in plain words. **Excerpt** is the source's own wording, for checking the paraphrase against.
- **Licence key:**
  - **PD**: public domain, US government work (FAA, NASA, NOAA/NWS). Wording can be reused, but cite it anyway.
  - **C-facts**: copyrighted. Use the facts only and rewrite them in your own words.
  - **CC BY-SA**: Wikipedia, CC BY-SA 4.0. Use the facts only. Copying any wording would need attribution and a share-alike licence.
- **[DERIVED]** marks arithmetic done for this dossier from the cited principle. It is not a quotation, so label it as a worked example on the page.
- **[FLAG]** marks a disagreement between sources, a number that could not be verified, or a caveat on edition or provenance.
- **Unit conversions:** 1 kt = 0.514 m/s = 1.852 km/h; 100 ft/min = 0.508 m/s.

## Notes on access and editions (read first)

- **FAA Glider Flying Handbook (GFH).** The whole-book PDF on faa.gov is larger than 30 MB and could not be fetched. The per-chapter PDFs under `faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/` were fetched instead.
  - The front matter in that same folder (`gfh_front.pdf`) says: "This handbook supersedes FAA-H-8083-13A, Glider Flying Handbook, dated 2013", and the cover year is 2024. That makes these chapters the current FAA-H-8083-13B (2024) edition.
  - The chapter files themselves do not print the document number. [FLAG] The edition is inferred from the front matter.
  - One older 13A Chapter 10, hosted by the British Gliding Association, is cited separately and labelled as 13A.
- **FAA Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25C).** [FLAG] Not quoted. The faa.gov PHAK index page was fetched, which confirms the 25C edition, but the chapter PDF links could not be opened in this session. Glider Flying Handbook Chapter 3 covers the same lift and angle-of-attack material, so it stands in.
- **FAA Aviation Weather Handbook (FAA-H-8083-28).** [FLAG] Only the table of contents was retrievable. Convection is in section 5.6.3, buoyancy in section 12.4.4 and mountain waves in Chapter 16. The full text was not fetched. Two sources are used instead: the NOAA JetStream "Parcel Theory" page, and the FAA's historic AC 00-6A "Aviation Weather", Chapter 16 "Soaring Weather". AC 00-6A is still hosted on faa.gov but is a cancelled 1975-era circular, so treat it as background.
- **FAA Powered Parachute Flying Handbook (FAA-H-8083-29).** [FLAG] This would be the ideal public-domain source on ram-air wings and pendulum stability, but the PDF is larger than 30 MB and could not be fetched. The FAA Weight & Balance Handbook addendum supplies the pendulum statement instead.
- **National federations (USHPA, BHPA, DHV).** [FLAG] No federation page with usable physics content came up within this session's search budget. DHV appears only as the host of two manufacturer manuals. The search budget ran out near the end of the research, so some planned follow-up searches were not run (listed under Gaps at the end).
- **Manufacturer spec sheets.** [FLAG] Ozone, Gin, Niviuk, Nova, Advance and Skywalk do **not** publish trim speed, top speed, minimum sink or glide ratio for current wings. Skywalk explains why (see Q4.4). Numeric performance data therefore comes from manufacturers that do publish it: Mac Para (current and recent), Sky Paragliders (2009) and Sol (via Wikipedia).

---

## Q1. How does a paraglider fly?

### Q1.1 The wing is two fabric skins divided into cells that are open at the front
- **Fact:** A paraglider wing is two layers of fabric (top and bottom surfaces) joined by internal walls that divide it into cells. Most cells are open only at the leading edge. Air rushing in keeps the wing inflated and holds its shape.
- **Excerpt:** "Such wings comprise two layers of fabric that are connected to internal supporting material..." / "By leaving most of the cells open only at the leading edge..." / "...incoming air keeps the wing inflated, thus maintaining its shape."
- **Source:** *Paragliding* | Wikipedia | https://en.wikipedia.org/wiki/Paragliding | CC BY-SA

### Q1.2 The cell walls (ribs) carry the airfoil shape
- **Fact:** Internal walls divide the wing into cells. Air enters through the openings at the front edge and inflates it, and the walls are cut to the airfoil profile, so the inflated wing takes the profile's shape. The suspension lines attach where the cell walls meet the lower surface. The A lines are nearest the leading edge and the brake lines are at the trailing edge.
- **Excerpt:** "The wing consists of cells, divided by walls." / "This is where the airflow enters and inflates the wing with air." / "The A lines are the closest to the leading edge and the D lines are the furthest."
- **Source:** *Paraglider Structure, Materials and Maintenance* (N. Yotov and I. Kalushkov, last modified 9 Dec 2023) | SkyNomad | https://www.skynomad.com/articles/paraglider_construction.html | C-facts

### Q1.3 Ram-air inflation gives the canopy a wing cross-section
- **Fact:** Ram-air inflation is what turns the fabric into a proper airfoil.
- **Excerpt:** "Ram-air inflation forces the parafoil into a classic wing cross-section."
- **Source:** *Parafoil* | Wikipedia | https://en.wikipedia.com/wiki/Parafoil (resolves to en.wikipedia.org) | CC BY-SA

### Q1.4 Manufacturers design the openings to keep internal pressure steady
- **Fact:** The cell openings are sized and shaped so that the wing stays pressurised in every flight mode. Holding a constant internal pressure is the core aim of piloting in turbulence.
- **Excerpt (Gradient Go manual, Rev. 0, 22.7.2019):** "Small rectangular cell openings for sufficient pressurization during all flight modes"
- **Source:** *Go user manual* | Gradient (hosted by DHV) | https://service.dhv.de/dbfiles/managed/pruefung/2019/07/go_manual_en_r0_fin.pdf | C-facts
- **Excerpt (Ozone Rush 6, EN v1.0 Apr 2021):** "The goal is to maintain the wing directly overhead with a constant level of internal pressure." / "In turbulent conditions the internal pressure of the wing is constantly changing"
- **Source:** *Rush 6 Pilots Manual* | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt (Niviuk Hook 6, describing its air-inlet design):** "...to ensure optimal maintenance of internal pressure."
- **Source:** *Hook 6 user manual and technical data* | Niviuk | https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf | C-facts

### Q1.5 The lift equation
- **Fact:** Lift equals a lift coefficient × air density × half the square of the speed × wing area (L = Cl · ρV²/2 · A). The lift coefficient captures the effect of the wing's shape and its angle to the airflow, and in practice it is measured.
- **Excerpt:** "The lift equation states that lift L is equal to the lift coefficient Cl times the density rho..." / "...the shape of the body, and the body's inclination to the flow."
- **Source:** *Lift Equation* | NASA Glenn Research Center, Beginner's Guide to Aeronautics | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-equation-2 | PD

### Q1.6 Lift grows with the square of speed and falls with thinner air
- **Fact:** Doubling airspeed quadruples lift. Lift drops as air density drops with altitude or heat.
- **Excerpt:** "Lift also varies with the square of velocity or airspeed." / "As air density decreases with increasing altitude or rising temperature, lift decreases." (both p. 3-3)
- **Source:** *Glider Flying Handbook* (FAA-H-8083-13B), Ch. 3 "Aerodynamics of Flight" | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf | PD

### Q1.7 Angle of attack
- **Fact:** Angle of attack is the angle between the wing's chord line and the oncoming air. Lift rises roughly in step with angle of attack until a critical angle is reached, beyond which the wing stalls.
- **Excerpt:** "The angle of attack is the acute angle between the chord line of the wing and the relative wind developed by the motion of the glider through the air." / "The coefficient of lift increases linearly until reaching a critical angle..." (p. 3-3)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 3 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf | PD
- [FLAG] The angle-of-attack sentence was returned in two pieces across two fetches; the closing words "developed by the motion of the glider through the air" came from the second pass. Check it against the PDF before quoting it word for word.

### Q1.8 Angle of attack matters a lot, and too much loses lift abruptly
- **Fact:** Angle of attack has a large effect on lift. For small angles (within about ±10°) lift changes almost linearly with it. At high angles the airflow separates and lift is lost suddenly (the stall).
- **Excerpt:** "Angle of attack has a large effect on the lift generated by a wing." / "...varies almost linearly for small angles of attack (within +/- 10 degrees)." / "The separation of the boundary layer explains why aircraft wings will abruptly lose lift at high inclination to the flow."
- **Source:** *Effects of Inclination on Lift Interactive* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/incline | PD

### Q1.9 Three forces act in a glide, with no thrust
- **Fact:** A glider has no engine. Only three forces act on it: weight, lift and drag. Lift acts at right angles to the flight path, and drag acts directly against the motion.
- **Excerpt:** "There are three forces acting on the glider; weight, lift, and drag."
- **Source:** *Vector Balance of Forces: Glider* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/vector-balance-of-forces-glider | PD
- **Excerpt:** "The glider, however, has no engine to generate thrust." / "Lift is directed perpendicular (at right angle) to the flight direction." / "The direction of the drag force is always opposite the direction of the motion."
- **Source:** *Three Forces on a Glider* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/three-forces-on-a-glider | PD

### Q1.10 A glider always descends through the air, and gravity is its engine
- **Fact:** A glider trades height for speed. Relative to the air around it, it is always going down. The forward component of its weight is what pulls it along, so gravity acts as its engine.
- **Excerpt:** "The simple answer is that a glider trades altitude for velocity." / "Gliders always descend relative to the air in which they are flying."
- **Source:** *Three Forces on a Glider* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/three-forces-on-a-glider | PD
- **Excerpt:** "Thus, gravity is the external engine that pulls the glider forward by acting on Wf." / "A glider descends through the surrounding air to make this conversion." (p. 3-5; Wf is the forward component of weight)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 3 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf | PD

### Q1.11 The pilot hangs well below the wing
- **Fact:** The pilot sits in a harness suspended underneath the wing by a network of lines.
- **Excerpt:** "The pilot is supported underneath the wing by a network of suspension lines."
- **Source:** *Paragliding* | Wikipedia | https://en.wikipedia.org/wiki/Paragliding | CC BY-SA

### Q1.12 The hanging weight behaves like a pendulum
- **Fact:** With the weight hanging far below a ram-air wing, the aircraft behaves like a pendulum. This is the basis of a paraglider's natural tendency to swing back to level beneath its wing. The FAA statement is about powered parachutes, which share the same hanging, ram-air arrangement.
- **Excerpt:** "A powered parachute acts like a pendulum with the weight of the aircraft hanging beneath the inflated wing (parachute)."
- **Source:** *Weight & Balance Handbook (FAA-H-8083-1B) Addendum*, 20 Oct 2025 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/Weight_Balance_HB_Addendum_(MOSAIC).pdf | PD
- **Excerpt:** "Paragliders can be seen as a simple pendulum body (CG) with a moving pivot point (CP)." / "...inherent pendulum stability."
- **Source:** *Active Flying* (N. Yotov, Mar 2023) | SkyNomad | https://www.skynomad.com/active-flying | C-facts

### Q1.13 [FLAG] Nuance: a low centre of gravity is not stabilising in every respect
- **Fact:** NASA parawing research lists "a centre of gravity far below the wing" as the defining feature of these vehicles. It also found that lowering the payload further reduced the damping of one roll mode. Write "pendulum stability keeps the wing overhead and damps big swings". Do not write "the further below, the more stable".
- **Excerpt:** "...a center-of-gravity location far below the wing..." / "Increasing the vertical distance between the payload and parawing led to decreased damping of the roll-subsidence mode."
- **Source:** Chambers and Boisseau, *A Theoretical Analysis of the Dynamic Lateral Stability and Control of a Parawing Vehicle*, NASA TN D-3461, June 1966 | NASA Langley | https://ntrs.nasa.gov/api/citations/19660019921/downloads/19660019921.pdf | PD

### Q1.14 Steering: brakes on the trailing edge plus weight shift
- **Fact:** Each hand holds a brake handle whose lines connect to the trailing edge on that side. The brakes adjust speed, steer (together with leaning the body) and flare the wing for landing. The pilot also has to lean (shift weight) to steer properly.
- **Excerpt:** "Brakes: controls held in each of the pilot's hands connect to the trailing edge of the left and right sides of the wing." / "The brakes are used to adjust speed, to steer (in addition to weight shift), and to flare (during landing)."
- **Source:** *Paragliding* | Wikipedia | https://en.wikipedia.org/wiki/Paragliding | CC BY-SA

### Q1.15 How manufacturers teach a turn
- **Fact:** Lean first, then smoothly add inside brake. Control the turn's radius and speed with weight shift and the outside brake. Never start a turn at minimum speed (full brakes), because of the spin risk.
- **Excerpt (Ozone Rush 6):** "The first input for directional change should be weight-shift, followed by a smooth application of the brake" / "To regulate the speed and radius of the turn, coordinate your weight shift and use the outer brake." / "Never initiate a turn at minimum speed (i.e. with full brakes on)"
- **Source:** *Rush 6 Pilots Manual* (EN B) | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt (Gin Bolero 8):** "Enter turns progressively with sufficient speed, initiate weight-shift, then apply inside brake." / "Once established, regulate turn radius primarily with weight-shift and the outside brake."
- **Source:** *Bolero 8 user manual* (EN A) | Gin Gliders | https://static.gingliders.com/paragliders/bolero-8/documents/bolero-8-user-manual-en.pdf | C-facts
- [FLAG] The fetch tool returned the Gin text as "weight -shift" (a PDF hyphenation artefact); it is normalised here.

### Q1.16 Weight shift is centre-of-gravity steering
- **Fact:** Moving the suspended weight sideways banks the wing. NASA describes this centre-of-gravity-shift control on parawings with hanging payloads.
- **Excerpt:** "This control system is, in effect, similar to the center-of-gravity shift type of control actually used on parawings with suspended payloads."
- **Source:** NASA TN D-3461 (1966) | NASA Langley | https://ntrs.nasa.gov/api/citations/19660019921/downloads/19660019921.pdf | PD

### Q1.17 Why banking turns the wing
- **Fact:** When the wing banks, its lift tilts. Part of the lift still holds up the weight, and the sideways part pulls the glider round the turn.
- **Excerpt:** "When a glider rolls away from wings-level, lift divides into two components." / "The vertical component opposes weight, while the other acts horizontally to oppose centrifugal force." (p. 3-10)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 3 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf | PD

**Q1 flags**
- [FLAG] The phrase "pulling down the trailing edge similar to a flap on an airplane" turned up in an aircraftspruce.com PDF excerpt (https://www.aircraftspruce.com/catalog/pdf/13-10230.pdf). The publisher and title could not be confirmed, so it is **not** used. Q1.14 covers the same point from Wikipedia.
- [FLAG] No manufacturer manual seen explains in physics terms why pulling a brake turns the wing (more drag and lift on the braked side). Explain it in your own words from Q1.14 to Q1.17, or leave it out.

---

## Q2. How do paragliders gain altitude?

### Q2.1 The core principle: find air rising faster than you sink
- **Fact:** A glider is always sinking through the air. If that air is rising faster than the glider sinks, the glider goes up.
- **Excerpt:** "If the pilot can locate a pocket of air that is rising faster than the glider is descending, the glider can actually gain altitude, increasing its potential energy."
- **Source:** *Gliders* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/gliders/ | PD

### Q2.2 Updrafts come from heated ground (thermals) and from wind meeting hills
- **Fact:** Rising air is called an updraft. Thermals are rising pockets of warm air. Wind blowing at a hill or mountain is forced upward over it. Birds circle in thermals to climb without flapping, and gliders do the same.
- **Excerpt:** "Pockets of rising air are called updrafts." / "Rising pockets of hot air are called thermals." / "Updrafts are found when a wind blowing at a hill or mountain has to rise to climb over it."
- **Source:** *Gliders* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/gliders/ | PD

### Q2.3 Why warm air rises (buoyancy)
- **Fact:** Warm air is less dense than cool air. Gravity pulls the denser, cooler air down. It spreads along the ground, undercuts the warm air and forces it upward.
- **Excerpt:** "Warm air has lower density compared to cooler air" / "Gravity pulls cooler, denser air toward the Earth's surface." / "As the denser air reaches the Earth's surface, it spreads out and undercuts the less dense air, which in turn forces the less dense air up and into motion, causing it to rise."
- **Source:** *Parcel Theory* (JetStream, updated 6 Oct 2023) | NOAA National Weather Service | https://www.noaa.gov/jetstream/upperair/parcel-theory (fetched as https://noaa.gov/node/10402) | PD

### Q2.4 A thermal is the updraft of a small convection cell
- **Fact:** A thermal is the rising part of a small convection current. Cooler air sinks around it to feed the circulation, which is why sink is found between thermals.
- **Excerpt:** "A thermal is simply the updraft in a small-scale convective current." / "Cool air must sink to force the warm air upward in thermals." (pp. 172-173)
- **Source:** *Aviation Weather* (AC 00-6A), Ch. 16 "Soaring Weather" | FAA | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC%2000-6A%20Chap%2016-Index.pdf | PD
- [FLAG] AC 00-6A is a cancelled 1975-era advisory circular, still hosted by the FAA. Its physics is sound, but cite it as historic.

### Q2.5 The sun heats some surfaces more, so thermals come from particular places
- **Fact:** Slopes facing the sun absorb more energy per square metre. Dark surfaces heat faster than grass. Hillsides tend to be drier and heat better than the lowlands around them, so thermals often form there. When a thermal reaches the condensation level, a cumulus cloud forms on top of it.
- **Excerpt:** "A sun facing slope receives more energy per unit of area and can warm the surrounding air more effectively." / "Darker ground or surface features heat quicker than grass covered fields." / "As any thermal rises from the surface and reaches the convective condensation level (CCL), a cloud begins to form."
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 10 "Soaring Techniques" (pp. 10-2 to 10-3) | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_10.pdf | PD
- **Excerpt:** "Thermals are columns of rising air that are formed on the ground through the warming of the surface by sunlight."
- **Source:** *Lift (soaring)* | Wikipedia | https://en.wikipedia.org/wiki/Lift_(soaring) | CC BY-SA

### Q2.6 Typical thermal strength
- **Fact:** Typical thermals rise at about 1 to 3 m/s. They are a few hundred metres to a couple of kilometres wide, and are driven by the temperature difference between ground and air.
- **Excerpt:** "...they rise at 1-3 meters per second." / "Thermals are driven by temperature contrast between the ground and the air." / "...the columns are a few hundred meters to as much as a couple of kilometers in diameter."
- **Source:** W. M. Angevine, *Thermal Structure and Behavior* (written Nov 2014) | hosted on NOAA Chemical Sciences Laboratory staff pages | https://esrl.noaa.gov/csl/staff/wayne.m.angevine/wayne.m.angevine.presentations/thermals_2014.pdf | C-facts (the page does not state the author's affiliation, so it is not treated as a US government work)
- **Fact:** Lift often strengthens near cloud base, for example from about 400 to 1,000 ft/min (about 2 to 5 m/s).
- **Excerpt:** "...the lift near cloud base often dramatically increases, for instance from 400 to 1,000 feet per minute (fpm)" (p. 10-3)
- **Source:** FAA *Glider Flying Handbook* (**FAA-H-8083-13A**, 2013 edition), Ch. 10, as hosted by the British Gliding Association | FAA | https://www.gliding.co.uk/wp-content/uploads/sites/3/2019/11/Soaring-Chap10-FAA.pdf | PD
- **Excerpt:** "Climb rates depend on conditions, but rates of several meters per second are common." (no citation in the article)
- **Source:** *Lift (soaring)* | Wikipedia | https://en.wikipedia.org/wiki/Lift_(soaring) | CC BY-SA
- [FLAG] AC 00-6A also says "Soaring pilots have encountered vertical currents exceeding 3,000 feet per minute," (about 15 m/s, p. 200). That is an extreme, not a typical value, so do not present it as normal.
- [DERIVED] With paraglider minimum sink at about 1.0 to 1.15 m/s (Q2.11), a 1 m/s thermal gives roughly zero climb when circling. Turning steepens the sink further, so that is before turning losses. A 3 m/s thermal gives about 2 m/s of climb. This is arithmetic from Q2.1, Q2.6 and Q2.11.

### Q2.7 Ridge (slope, dynamic) lift
- **Fact:** Wind blowing against a hill or ridge is deflected up and over it. Pilots fly in the band of rising air on the upwind face.
- **Excerpt:** "Wind blowing toward hills or ridges flows upward, over, and around the abrupt rises in terrain." (p. 195)
- **Source:** FAA AC 00-6A, Ch. 16 "Soaring Weather" | FAA | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC%2000-6A%20Chap%2016-Index.pdf | PD
- **Excerpt:** "...involves flying in the updraft along the upwind side of a ridge." / "Airflow follows the hill or ridge shape." (p. 10-13)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 10 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_10.pdf | PD
- **Excerpt:** "...allows lift to be obtained by using the wind directed upwards by a fixed object."
- **Source:** *Paragliding* | Wikipedia | https://en.wikipedia.org/wiki/Paragliding | CC BY-SA
- [FLAG] The GFH line "Surface winds of 15–20 knots perpendicular to the ridge optimize ridge soaring." (about 28 to 37 km/h) is for **sailplanes**. Paragliders trim at about 37 to 40 km/h (Q4), so that much wind is at or beyond the safe limit for most paraglider pilots. Do not carry the sailplane figure over to paragliders.

### Q2.8 Wave lift (brief)
- **Fact:** Strong wind blowing across a mountain range can set up standing waves downwind of it. These give smooth, continuous lift to great heights, and they are the main lift source for high-altitude glider flights. Expect strong sink on the downward side of the wave.
- **Excerpt:** "The great attraction of soaring in mountain waves stems from the continuous lift to great heights." (p. 198)
- **Source:** FAA AC 00-6A, Ch. 16 | FAA | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC%2000-6A%20Chap%2016-Index.pdf | PD
- **Excerpt:** "Almost all high-altitude glider flights use mountain lee waves as the primary source of lift." / "Sink on the downside of a lee wave can reach 2,000 fpm or more." (pp. 10-21, 10-22)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 10 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_10.pdf | PD

### Q2.9 Convergence lift (brief)
- **Fact:** Where two air masses meet (for example a sea breeze meeting another airflow), the air is forced upward along the line where they meet. Cumulus clouds often mark the line.
- **Excerpt:** "Sea breezes of different origin meet in the convergence zones producing vertical currents" (p. 194)
- **Source:** FAA AC 00-6A, Ch. 16 | FAA | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC%2000-6A%20Chap%2016-Index.pdf | PD
- **Excerpt:** "Pilots can most easily spot a convergence zone in the presence of cumulus clouds." / "A weaker convergence line often produces more lift than sink." (p. 10-28)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 10 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_10.pdf | PD

### Q2.10 Minimum sink is flown with a little brake, not hands-up
- **Fact:** A paraglider reaches its minimum sink rate (the best speed for climbing) with a small amount of brake applied. On the Ozone Rush 6 that is about 20 cm.
- **Excerpt:** "By applying approximately 20cm of brakes the Rush 6 will achieve its Minimum-Sink rate..."
- **Source:** *Rush 6 Pilots Manual* (EN B) | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt:** "...the SwiftMAX will achieve its minimum-sink rate; this is the speed for best climb"
- **Source:** *SwiftMax manual* EN v1.1 (EN C tandem) | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/06/SwiftMax_manual_EN_v1.1.pdf | C-facts

### Q2.11 Paraglider minimum sink: real published numbers (about 1.0 to 1.15 m/s confirmed)
| Wing (class) | Claimed min sink | Excerpt | Source / URL | Licence |
|---|---|---|---|---|
| Mac Para Muse 5 (EN A) | 1.05 m/s, all sizes | "Min. sink rate [m/s] \| 1.05 \| 1.05 \| 1.05..." | Mac Para product page, https://www.macpara.com/en/paragliders/free-flying/muse-5/ | C-facts |
| Mac Para Eden 7 (EN B) | 1.05 m/s | "Min. sink rate [m/s] \| 1.05 \| 1.05 \| 1.05..." | Mac Para, https://www.macpara.com/en/previous-products/eden-7 | C-facts |
| Mac Para Elan 3 (EN C) | 1.05 m/s | "Min. sink rate [m/s] \| 1.05 \| 1.05 \| 1.05..." | Mac Para, https://www.macpara.com/en/paragliders/free-flying/elan-3/ | C-facts |
| Sky Paragliders Atis 3 (EN B, manual Nov 2009) | under 1.15 m/s | "Min. sink rate (m/s): < 1,15" | *User's manual for ATIS 3*, Sky Paragliders, https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf | C-facts |
| Sol Prymus (EN A; figure probably for the original Prymus 1) | 1.1 m/s | "Rate of sink: 1.1 m/s (220 ft/min)" | *Sol Prymus*, Wikipedia (data from Bertrand, *World Directory of Leisure Aviation* 2003-04), https://en.wikipedia.org/wiki/Sol_Prymus | CC BY-SA |

- [FLAG] All of these are manufacturer claims, not independent measurements. Mac Para claims exactly 1.05 m/s for its EN A, EN B and EN C wings alike, which looks like a rounded house figure. Ozone, Gin, Niviuk, Nova, Advance and Skywalk publish no sink figure. Safe wording: "manufacturers that publish the figure typically claim a minimum sink of about 1.0 to 1.15 m/s".
- **Comparison (PD):** The GFH example sailplane polar shows "a minimum sink of 1.9 knots occurs at 40 knots." (p. 5-10), which is about 0.98 m/s at 74 km/h. A sailplane sinks no slower than a paraglider at minimum sink. Its advantage is that it does so while flying about twice as fast, which is where the far better glide comes from. Source: FAA GFH (FAA-H-8083-13B), Ch. 5, https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf [DERIVED comparison].

---

## Q3. What is the glide ratio of a paraglider?

### Q3.1 Definition
- **Fact:** Glide ratio is how far a glider travels forward for each unit of height it loses in still air. A glide ratio of 10:1 means 10 m forward for every 1 m of height lost.
- **Excerpt:** "The glide ratio gives the distance the glider can travel during a given descent in altitude." (p. 3-6)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 3 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf | PD
- **Excerpt:** "...a ratio of 12:1 means that in smooth air a glider can travel forward 12 metres while only losing 1 metre of altitude."
- **Source:** *Hang gliding* | Wikipedia | https://en.wikipedia.org/wiki/Hang_gliding | CC BY-SA

### Q3.2 Glide ratio equals the lift-to-drag ratio (L/D)
- **Fact:** In a steady glide, the glide ratio is numerically equal to the lift-to-drag ratio. A higher L/D means a flatter glide angle and more distance per metre of height.
- **Excerpt:** "...the lift divided by the drag is equal to the inverse of the glide angle for small angles."
- **Source:** *Vector Balance of Forces: Glider* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/vector-balance-of-forces-glider | PD
- **Excerpt:** "The higher the L/D, the lower the glide angle." / "...the greater the distance that a glider can travel across the ground for a given change in height."
- **Source:** *Drag to Lift Ratio* | NASA Glenn | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-to-lift-ratio | PD
- **Excerpt:** "A glider with more weight can fly faster while maintaining the same lift-to-drag (L/D) ratio (glide ratio)." (p. 5-8)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 5 "Glider Performance" | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf | PD

### Q3.3 The speed polar, minimum sink speed and best glide speed
- **Fact:** A glider's performance is drawn as a polar curve: sink rate plotted against airspeed. The top of the curve is the minimum sink rate, the slowest descent and the longest time aloft. A line drawn from the origin that just touches the curve marks the best glide (best L/D) speed. Best glide ratio = best-glide airspeed ÷ sink rate at that speed. In the FAA's example sailplane, the minimum sink is 1.9 kt at 40 kt and the best glide is 50 kt at 2.1 kt of sink, giving 24:1.
- **Excerpt:** "The peak of the blue sink rate curve determines minimum sink rate." / "A tangent from the origin to the polar indicates the best glide speed (best L/D)." (p. 5-10)
- **Excerpt:** "The glide ratio at best L/D speed is determined by dividing the best L/D speed by the sink rate at that speed" (p. 5-10)
- **Excerpt:** "Thus, this glider has a best glide ratio in calm air (no lift or sink and no headwind or tailwind) of 24:1 at 50 knots." (p. 5-10)
- **Excerpt:** "The speed that results in the lowest altitude loss over time, the minimum sink airspeed, also increases with weight." (p. 5-9)
- **Source (all four):** FAA GFH (FAA-H-8083-13B), Ch. 5 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf | PD

### Q3.4 On a paraglider, best glide is at trim (hands up)
- **Fact:** On a typical paraglider, flying hands-up (trim speed) gives the best still-air glide. A little brake gives minimum sink. Up to about half speed bar costs little glide, while full bar costs a lot.
- **Excerpt:** "Flying at trim speed (hands-up), the Rush 6 will achieve its 'best glide' speed for still air." / "Using up to half bar does not degrade the glide angle or stability significantly and will improve your flying performance."
- **Source:** *Rush 6 Pilots Manual* (EN B) | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt:** "Using full speed-bar, the wing will fly at maximum speed, but the glide will be adversely affected."
- **Source:** *Hook 6 manual* (EN B) | Niviuk | https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf | C-facts

### Q3.5 Wind changes glide over the ground, not through the air
- **Fact:** A headwind cuts groundspeed and so shortens the distance covered over the ground, while a tailwind stretches it. The glide through the air is unchanged. Into a headwind (or through sinking air), fly faster than best-glide speed to get the most distance. With a tailwind, fly between minimum sink and best-glide speed.
- **Excerpt:** "During cruising flight, headwinds reduce the groundspeed of the glider." / "A glider flying at 60 knots true airspeed into a headwind of 25 knots has a groundspeed of only 35 knots." / "Tailwinds increase the groundspeed of the glider." (p. 5-4)
- **Excerpt:** "...flying faster as headwinds increase results in a greater distance traveled over the ground." (p. 5-11)
- **Excerpt:** "The speed to fly in a tailwind lies between minimum sink and best L/D, but never lower than minimum sink speed." (p. 5-11)
- **Excerpt:** "Sinking air often exists between thermals and flying faster than best L/D can result in less time in sinking air..." (p. 5-11)
- **Source (all four):** FAA GFH (FAA-H-8083-13B), Ch. 5 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf | PD
- **Paraglider-specific excerpt:** "For better penetration in headwinds and improved glide performance in sinking air..." (speed-bar advice)
- **Source:** *Rush 6 Pilots Manual* | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- [FLAG] GFH rule of thumb, returned as: "...the pilot can add half the headwind component to the zero wind L/D to obtain maximum distance." (p. 5-11). Read in context, it means "add half the headwind to your still-air best-glide **airspeed**". Check the exact wording in the PDF before quoting it, because the word "speed" may have been dropped.
- [DERIVED worked example] Take a paraglider with a 10:1 still-air glide at a 38 km/h trim speed: it sinks 3.8 km/h (about 1.06 m/s).
  - In a 20 km/h headwind its groundspeed is 18 km/h, so it covers about 4.7 m per metre of height.
  - In a 20 km/h tailwind its groundspeed is 58 km/h, so it covers about 15.3 m per metre of height.
  - This is arithmetic from the GFH principle plus the Q4 trim speeds, not a quoted figure.

### Q3.6 Real paraglider glide numbers by class
| Wing (class, year) | Glide figure | Excerpt | Source / URL | Licence |
|---|---|---|---|---|
| Sol Prymus 4 (EN A, in production 2016) | 8.3:1 | "...glide ratio is 8.3:1" | *Sol Prymus*, Wikipedia (Prymus 4 specs cited to manufacturer ref. "Pry4"), https://en.wikipedia.org/wiki/Sol_Prymus | CC BY-SA |
| Mac Para Muse 5 (EN A, current) | "+10" | "Glide ratio \| +10 \| +10 \| +10..." | Mac Para, https://www.macpara.com/en/paragliders/free-flying/muse-5/ | C-facts |
| Sky Atis 3 (EN B, 2009) | over 8.8 | "Max. gliding ratio: > 8,8" | Sky Paragliders manual, https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf | C-facts |
| Mac Para Eden 7 (EN B, previous model) | "+10" | "Glide ratio \| +10 \| +10 \| +10..." | Mac Para, https://www.macpara.com/en/previous-products/eden-7 | C-facts |
| Mac Para Elan 3 (EN C, current; three line rows) | 10.5 | "Glide ratio \| 10.5 \| 10.5 \| 10.5..." | Mac Para, https://www.macpara.com/en/paragliders/free-flying/elan-3/ | C-facts |
| Mac Para Elan 2 (EN C, previous) | 10.5 | "Glide ratio \| 10.5 \| 10.5..." | Mac Para, https://www.macpara.com/en/previous-products/elan-2/ | C-facts |
| Airwave Ten (competition, mid-2000s) | 10:1 | "Maximum glide ratio: 10:1" | *Airwave Ten*, Wikipedia (data from Bertrand, WDLA 2004), https://en.wikipedia.org/wiki/Airwave_Ten | CC BY-SA |
| Range across classes (Wikipedia) | 9.3 recreational to about 11.3 competition, "in some cases up to 13" | "The glide ratio of paragliders ranges from 9.3 for recreational wings to about 11.3 for modern competition models," / "reaching in some cases up to 13." | *Paragliding*, Wikipedia (cites the FAI CIVL page and an aircross.eu report on a 2013 glide-ratio competition), https://en.wikipedia.org/wiki/Paragliding | CC BY-SA |
| "High performance" paraglider (Wikipedia table) | 11 | "High performance model \| 11" (uncited) | *Gliding flight*, Wikipedia, https://en.wikipedia.org/wiki/Gliding_flight | CC BY-SA |

- Mac Para says it tried a two-liner for the Elan 3 but went back to three line rows: "finally we returned to the three-row concept" (same Elan 3 URL). So it is **not** a two-liner data point.
- [FLAG] **Gap: no current CCC wing with a published or independently measured glide figure was found.** Ozone (Enzo 3), Gin (Boomerang), Niviuk (Icepeak X-One) and Ozone (Zeno, EN D two-liner) publish none. The X-One retailer page says only "Glide, top speed, and climb efficiency are all at the front of the CCC class." (https://www.paraglidingsanfrancisco.com/product/niviuk-x-one). For the competition end, the safest wording is Wikipedia's "about 11 to 13 for modern competition wings", labelled as approximate.
- [FLAG] **Older sources give much lower numbers (outdated; do not use as current):**
  - The Soaring Society of America FAQ says "Para-gliders rarely achieve glide ratios greater than 8:1" (https://www.ssa.org/faq-items/what-is-the-difference-between-a-hang-glider-and-a-sailplane/, C-facts).
  - The SHV/FSVL exam commentary (J. Oberson 2005, English translation 2010) says "maximum glide ratio of more than 8" and "while the highest performance wings hardly exceed 9" (https://soaringmeteo.org/examenTheoriqueEN4.pdf, C-facts).
  - Both reflect wings from about 2005 to 2010 and conflict with current manufacturer claims of 10 to 10.5.
- [FLAG] Mac Para's "+10" is a claim with no stated test method. Sky (2009) claims "> 8,8" for a comparable EN B. The roughly 1.2-point gap between them reflects both age and claiming style.
- [FLAG] Why the big brands publish nothing (Skywalk): "Performance data are dependent on the harness, the size of the glider, on the air mass and the total weight." Source: https://skywalk.info/project/chili5/ (C-facts). This is a useful caveat for the page.

### Q3.7 Comparison: hang gliders and sailplanes
| Aircraft | Figure | Excerpt | Source / URL | Licence |
|---|---|---|---|---|
| Open-class sailplane (Eta) | over 70:1 | "The largest open-class glider, the Eta, has a span of 30.9 meters and has a glide ratio over 70:1" | *Glider (sailplane)*, Wikipedia, https://en.wikipedia.org/wiki/Glider_(sailplane) | CC BY-SA |
| Open class, typical | about 60:1 | "open class sailplanes – typically around 60:1" | *Hang gliding*, Wikipedia (comparison table), https://en.wikipedia.org/wiki/Hang_gliding | CC BY-SA |
| 15 to 18 m sailplanes | 38:1 to 52:1 | "...glide ratios are between 38:1 and 52:1" | *Glider (sailplane)*, Wikipedia | CC BY-SA |
| Sailplanes, routine | 40:1 | "...sailplanes routinely achieve 40:1" | Soaring Society of America FAQ, https://www.ssa.org/faq-items/what-is-the-difference-between-a-hang-glider-and-a-sailplane/ | C-facts |
| Flex-wing hang glider | about 17:1 | "...glide ratio~17:1, speed range ~30–145 km/h (19–90 mph)" (2006 figures) | *Hang gliding*, Wikipedia, https://en.wikipedia.org/wiki/Hang_gliding | CC BY-SA |
| Rigid-wing hang glider | about 20:1 | "...glide ratio~20:1, speed range ~35–130 km/h (22–81 mph)" | *Hang gliding*, Wikipedia | CC BY-SA |
| Hang glider (SSA) | 16:1 | "...hang-gliders 16:1" | SSA FAQ | C-facts |
| Paraglider (comparison table) | about 10 | "about 10, relatively poor glide performance makes long distance flights more difficult" | *Hang gliding* / *Glider (sailplane)*, Wikipedia | CC BY-SA |

- [FLAG] The hang-glider figures vary between 15 (Wikipedia *Gliding flight* table), 16 (SSA) and 17 to 20 (Wikipedia *Hang gliding*). The sailplane figures vary between 40 routine, 60 open class and over 70 for the Eta; Wikipedia *Gliding flight* says "approaching 60 to 1" in its text but lists the Eta at 70 in its table. The ranges you proposed (sailplanes about 40 to 70:1, hang gliders about 15 to 20:1) are supported across these sources. All the comparison figures are Wikipedia or SSA, with no US-government source found.

---

## Q4. How fast does a paraglider fly?

### Q4.1 Overall range
- **Fact:** Paragliders typically fly between about 22 km/h (stall) and 55 km/h (full speed bar). Trim speed, hands-up with no bar, is typically 32 to 40 km/h.
- **Excerpt:** "The speed range of paragliders is typically 22–55 kilometres per hour (14–34 mph), from stall speed to maximum speed." / "...which is typically 32–40 kilometres per hour (20–25 mph)"
- **Source:** *Paragliding* | Wikipedia | https://en.wikipedia.org/wiki/Paragliding | CC BY-SA
- [FLAG] Both of those Wikipedia sentences are uncited. The manufacturer data in Q4.2 supports trim speeds of 37 to 41 km/h, which sits at the top of Wikipedia's 32 to 40 km/h range. A trim speed of 32 km/h is low for current wings.

### Q4.2 Real wings: minimum, trim and top speed (manufacturer figures)
| Wing (class) | Min speed | Trim speed | Top speed (full bar) | Excerpt | Source / URL |
|---|---|---|---|---|---|
| Mac Para Muse 5 (EN A) | 23-25 km/h | 37-39 km/h | 46-48 km/h | "Top speed (accelerator)[km/h] \| 46 - 48..." | https://www.macpara.com/en/paragliders/free-flying/muse-5/ |
| Mac Para Eden 7 (EN B) | 23-25 | 37-39 | 50-52 | "Top speed (accelerator)[km/h] \| 50 - 52..." | https://www.macpara.com/en/previous-products/eden-7 |
| Sky Atis 3 (EN B, 2009) | 23 | 37-38 | 50 (S), 51 (M, L), 52 (XL) | "Trim speed (km/h): 37-38" | https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf |
| Mac Para Elan 3 (EN C) | 23-25 | 38-40 | 53-55 | "Top speed (accelerator)[km/h] \| 53 - 55..." | https://www.macpara.com/en/paragliders/free-flying/elan-3/ |
| Mac Para Elan 2 (EN C, previous) | 23-25 | 38-40 | 55-56 | "Top speed (accelerator)[km/h] \| 55 - 56..." | https://www.macpara.com/en/previous-products/elan-2/ |
| Mac Para Magus (labelled "en-d" in the 2020 brochure) | 25 | 39-41 | 62 (±3) | "min. 25 \| trim. 39 - 41 \| max. 62 (+/-3)" | https://www.macpara.com/media/2553/free-gliders-mac_para-2020.pdf |
| UP Edge XR (two-line open-class competition, 2011) | n/a | n/a | 70 km/h | "...its impressive top speed of 70 km/hr should be approached with caution" | Cross Country Magazine, 10 Feb 2011, https://xcmag.com/news/ups-new-two-liner-edge-xr/ |
| Airwave Ten (competition, mid-2000s) | n/a | n/a | 65 km/h | "Maximum speed: 65 km/h (40 mph, 35 kn)" | Wikipedia (data from Bertrand, WDLA 2004), https://en.wikipedia.org/wiki/Airwave_Ten |

- Licence: manufacturer and XC Mag data are C-facts; Wikipedia rows are CC BY-SA.
- **Pattern for the writer:** minimum speed hardly changes across classes (about 23 to 25 km/h), and trim rises only a little (37 km/h to about 40 km/h). Top speed is what separates the classes: about 47 km/h for EN A, about 51 for EN B, about 54 for EN C, about 62 for EN D, and up to about 70 for older two-line competition wings.
- [FLAG] Mac Para's 2020 brochure and its website differ slightly for the Eden 7: the brochure says "max. 52 (+/-3)" and the website says "50 - 52". Use the website.
- [FLAG] The Magus's EN D label sits ambiguously on the brochure page, and the brochure does not say whether it is a two-liner. Treat the class as probable, not confirmed.
- [FLAG] The UP Edge XR article does not say whether its 70 km/h was measured or claimed. The CCC rule changes since 2015 (Q5.2) limit accelerator travel, so current CCC top speeds may differ. No current CCC top-speed figure was found.

### Q4.3 How much the speed bar adds
- **Fact:** Sky says full speed bar raises speed by about 30% over trim. Niviuk's certification sticker for the Hook 6 gives a 14 km/h speed range on the brakes alone and 25 km/h in total including the speed bar.
- **Excerpt:** "Operation of the speed bar can increase the maximum speed of the glider by 30 % (hands up, speed bar fully engaged)."
- **Source:** *User's manual for ATIS 3* | Sky Paragliders | https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf | C-facts
- **Excerpt:** "Speed range using brakes (km/h) 14" / "Total speed range with accessories (km/h) 25"
- **Source:** *Hook 6 manual* (certification sticker pages) | Niviuk | https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf | C-facts
- [FLAG] Which Hook 6 size those sticker figures belong to was not confirmed.

### Q4.4 Why most big brands publish no speeds
- **Fact:** Skywalk publishes no speed or glide figures. It says the numbers depend on the pilot's harness and seated drag, the glider size, the air mass, the total weight and altitude, so they cannot be compared fairly between gliders.
- **Excerpt:** "Performance data are highly dependent on the drag of the pilot and are therefore related to sitting position and harness." / "...speed varies with altitude and the associated different air pressure, but also with the total weight of the system."
- **Source:** *CHILI5* product page | Skywalk | https://skywalk.info/project/chili5/ | C-facts

### Q4.5 Wing loading: heavier means faster, with about the same glide
- **Fact (principle):** Adding weight shifts the whole polar to higher speeds. The glider sinks faster at any given speed but reaches the **same best glide ratio** at a higher airspeed, and its minimum-sink speed also rises. Sailplanes use water ballast for exactly this.
- **Excerpt:** "Although a heavier glider sinks faster, it glides the same horizontal distance (at a higher speed)..." (p. 5-8) / "The best glide ratio remains the same, but it occurs at a higher speed." (p. 5-11) / "Comparing the polar with and without ballast shows that the minimum sink increases..." (p. 5-11)
- **Source:** FAA GFH (FAA-H-8083-13B), Ch. 5 | FAA | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf | PD
- **Excerpt:** "...a heavier vehicle glides faster, but nearly maintains its glide ratio" (Wikipedia cites the FAA GFH for this)
- **Source:** *Gliding flight* | Wikipedia | https://en.wikipedia.org/wiki/Gliding_flight | CC BY-SA
- **Fact (paraglider manufacturer):** At the top of the certified weight range a paraglider flies faster. Near the bottom it sinks more slowly. Ozone also says the top of the range gives the most precise handling and is the place to be for strong or mountain conditions.
- **Excerpt:** "Flying at the upper limit of the weight range will give a faster speed" / "Flying near the lower weight will give improved sink rate performance"
- **Source:** *SwiftMax manual* EN v1.1 | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/06/SwiftMax_manual_EN_v1.1.pdf | C-facts
- **Excerpt:** "For the most precise and dynamic handling..." (benefit of flying at the top of the range) / "It is not recommended to fly at the very bottom of the weight range."
- **Source:** *Rush 6 Pilots Manual* | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- [DERIVED] With lift equal to weight and the angle of attack fixed, the lift equation (Q1.5) makes speed scale with the square root of weight. 10% more weight gives about 5% more speed. Going from the bottom to the top of the Eden 7 M range (82 to 103 kg, about +26%) gives about +12%, or roughly 37 to 41.5 km/h.
- [FLAG] Mac Para publishes trim as a 2 km/h band (37-39) for every size, a spread of about 5%. That is narrower than the roughly 12% the simple scaling predicts across the full range. The sources do not explain the gap: the published band may not be tied to weight, and pilot drag also matters. Safe page wording: "a few km/h faster at the top of the weight range, with essentially the same glide ratio".
- [FLAG] Nova's Mentor 7 product presentation (German, 2023) says it raised the upper weight limits by 5 kg so pilots can fly faster on strong days (https://www.nova.eu/fileadmin/user_upload/glider/MENTOR_7/NOVA_MENTOR_7_Produktpraesentation_2023_DE.pdf). That is a paraphrase only, because no verbatim excerpt was captured, so do not quote it.
- **Altitude note:** Skywalk says speed varies with altitude, and the GFH says lift falls as air thins (Q1.6). The same wing therefore flies at a higher true airspeed in thin air. (Both excerpts are above.)

---

## Q5. What does the speed bar do?

### Q5.1 Mechanism: the bar pulls the front risers down through pulleys
- **Fact:** The speed bar is a foot stirrup connected through pulleys on the harness and risers. Pushing it shortens the A risers most and the B risers less, while the rear (C) risers stay put. The whole wing tilts nose-down, pivoting about the rear risers, which lowers the angle of attack. Lower angle of attack means higher speed.
- **Excerpt:** "Pressure on the foot stirrup shortens the A and B risers and by this reduces the angle of attack of the canopy." (section 4.2, p. 5)
- **Source:** *Go user manual* (Rev. 0, 22.7.2019) | Gradient (hosted by DHV) | https://service.dhv.de/dbfiles/managed/pruefung/2019/07/go_manual_en_r0_fin.pdf | C-facts
- **Excerpt:** "...increases trim speed by progressively shortening the front risers..." / "...reducing the angle of attack."
- **Source:** *Bolero 8 user manual* (EN A) | Gin Gliders | https://static.gingliders.com/paragliders/bolero-8/documents/bolero-8-user-manual-en.pdf | C-facts
- **Excerpt:** "The acceleration system effects the A, A2 and B-risers."
- **Source:** *MESCAL6 Pro Guide* (EN A, ed. 1.1 04/20) | Skywalk (hosted by DHV) | https://service.dhv.de/dbfiles/managed/pruefung/2020/09/mescal6-pro_guide-en.pdf | C-facts
- **Excerpt:** "Released speed-bar: the A, B, C-risers are aligned." / "Full speed-bar: the difference between the A - C-risers becomes:" [120 mm on size 20; 145 mm on sizes 22 to 31] / "When we accelerate, the glider rotates over the C-riser and the trailing edge elevates."
- **Source:** *Hook 6 manual* (EN B) | Niviuk | https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf | C-facts
- **Excerpt:** "...the A riser will get about 18cm shorter than the C riser..." (full travel, Mentor 2 S and M)
- **Source:** *Mentor 2 manual*, Vers. 1.1, 01/2011 (EN B) | Nova | https://www.nova.eu/fileadmin/user_upload/glider/Manuals/Mentor2_V11_012011eng.pdf | C-facts
- **Excerpt:** "This control is used to increase speed and does so by decreasing the wing's angle of attack."
- **Source:** *Paragliding* | Wikipedia | https://en.wikipedia.org/wiki/Paragliding | CC BY-SA

### Q5.2 Two stages, and how far it travels
- **Fact:** Many harnesses have a two-step bar. The first step gives roughly half the accelerated range, and the second gives full speed. Full speed is reached when the riser pulleys touch. Competition rules cap how far the accelerator may shorten the front risers, which in turn caps top speed.
- **Excerpt:** "Fully extending the lower loop of the speed bar will accelerate the wing to approximately half its accelerated speed range." / "For full speed, hook your heels on to the upper bar and smoothly extend your legs" / "...maximum speed is when the pulleys on the risers overlap."
- **Source:** *Rush 6 Pilots Manual* | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt:** "...the speed system having pulleys with bearings to reduce friction to a minimum"
- **Source:** *Hook 6 manual* | Niviuk | (URL above) | C-facts
- **Excerpt:** "...restrict top speed by limiting the maximum accelerator effect to 14 cm maximum A-B difference"
- **Source:** *What's Up With The New CCC Paragliders?* (27 Feb 2016) | FAI | https://fai.org/node/21590 | C-facts
- [FLAG] Flybubble's 2014 summary of the first CCC spec says "Speedbar travel will be limited to 18cm (normal)." (https://flybubble.com/blog/ccc, C-facts). That measures something different (foot travel, where the FAI's 14 cm is the A-to-B riser difference), and it describes an earlier version of the rule. The current CIVL CCC document was not checked, so do not state a current CCC limit without checking it.
- [FLAG] Ozone's Rush 6 riser drawing table appears to show the A riser going from 530 mm to 350 mm (pulley axis to axis) at full bar, with the C riser unchanged. That reading comes from a table the fetch tool found hard to parse, so verify it before use. Sky's Atis 3 riser diagram similarly suggests an A-riser travel of about 15.4 cm (S and M).

### Q5.3 Effect on speed, sink and glide
- **Fact:** The bar raises speed (Sky: up to about 30% over trim). Sink rate also rises, as the polar shows (Q3.3). Light or moderate bar barely changes the glide and helps into headwinds and through sink. Full bar costs glide and is rarely the best choice in still air.
- **Excerpt:** "Full bar rarely is the best choice!"
- **Source:** *User's manual for ATIS 3* | Sky Paragliders | https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf | C-facts
- **Excerpt:** "Using up to half bar does not degrade the glide angle or stability significantly and will improve your flying performance."
- **Source:** *Rush 6 Pilots Manual* | Ozone | (URL above) | C-facts
- **Excerpt:** "Using full speed-bar, the wing will fly at maximum speed, but the glide will be adversely affected."
- **Source:** *Hook 6 manual* | Niviuk | (URL above) | C-facts
- **Excerpt:** "Optimal cross country glide between two thermals requires an ongoing choice of glider speed."
- **Source:** *IOTA DLS online manual*, Speed system section | Advance | https://manual.advance.ch/en/iota_dls/1127 | C-facts

### Q5.4 Safety: the wing is closer to collapse when accelerated
- **Fact:** A lower angle of attack makes the wing more prone to collapse and more sensitive to turbulence. When a collapse does happen at speed, it is more sudden and dynamic than at trim and can need more height to recover.
- **Excerpt:** "Using the accelerator decreases the angle of attack and makes the wing more prone to collapse..."
- **Source:** *Rush 6 Pilots Manual* (EN B) | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt:** "The glider reacts faster and more dynamically to collapses when accelerated."
- **Source:** *Bolero 8 user manual* (EN A) | Gin Gliders | https://static.gingliders.com/paragliders/bolero-8/documents/bolero-8-user-manual-en.pdf | C-facts
- **Excerpt:** "Don't forget that any collapse at full speed will be more severe than the same event experienced at normal trim speed." (5.1.3, p. 7)
- **Source:** *Go user manual* | Gradient | https://service.dhv.de/dbfiles/managed/pruefung/2019/07/go_manual_en_r0_fin.pdf | C-facts
- **Excerpt:** "...the wing behaves more dynamic if a collapse occurs in accelerated flight." / "...you might need more height to recover to normal flight!"
- **Source:** *Mentor 2 manual* (2011) | Nova | https://www.nova.eu/fileadmin/user_upload/glider/Manuals/Mentor2_V11_012011eng.pdf | C-facts
- **Excerpt:** "When accelerating the wing, the profile becomes more sensitive to turbulence and closer to a possible frontal collapse."
- **Source:** *Hook 6 manual* | Niviuk | https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf | C-facts
- **Excerpt:** "The profile´s angle of attack is thereby reduced, enhancing the risk for symmetric or asymmetric deformations and collapses."
- **Source:** *User's manual for ATIS 3* | Sky Paragliders | https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf | C-facts

### Q5.5 Safety: do not brake while accelerated
- **Fact:** Pulling the brakes while on the bar destabilises the profile and raises the collapse risk sharply. On performance wings, steer with the rear risers while accelerated.
- **Excerpt:** "Never apply the brakes whilst using the speed system - it makes the wing more prone to collapse." / "Always take control of your ACR risers during accelerated flight."
- **Source:** *Rush 6 Pilots Manual* | Ozone | (URL above) | C-facts
- **Excerpt:** "Applying brake while accelerated creates an unstable profile and significantly increases the risk of collapse."
- **Source:** *Bolero 8 user manual* | Gin Gliders | (URL above) | C-facts
- **Excerpt:** "...using the brakes whilst accelerated can actually lead to a collapse"
- **Source:** *SwiftMax manual* | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/06/SwiftMax_manual_EN_v1.1.pdf | C-facts
- **Excerpt:** "It doesn't make sense to apply the brakes during accelerated flight."
- **Source:** *Mentor 2 manual* | Nova | (URL above) | C-facts

### Q5.6 Safety: release the bar first, and keep it off near the ground and in turbulence
- **Fact:** If the wing loses pressure or collapses, release the bar immediately and fully, and only then correct. Avoid accelerated flight close to the ground or in turbulent air.
- **Excerpt:** "If a collapse occurs, immediately release the speed bar fully before applying any corrective inputs." / "Avoid flying accelerated close to the ground and use caution in turbulence."
- **Source:** *Bolero 8 user manual* | Gin Gliders | https://static.gingliders.com/paragliders/bolero-8/documents/bolero-8-user-manual-en.pdf | C-facts
- **Excerpt:** "If your Rush 6 collapses in accelerated flight, immediately release the accelerator..." / "Using the accelerator near the ground or in turbulent conditions should be avoided."
- **Source:** *Rush 6 Pilots Manual* | Ozone | https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf | C-facts
- **Excerpt:** "Use the speed system very carefully, or not at all at low altitude."
- **Source:** *Go user manual* | Gradient | https://service.dhv.de/dbfiles/managed/pruefung/2019/07/go_manual_en_r0_fin.pdf | C-facts
- **Excerpt:** "So you should keep more distance from the ground if you fly accelerated."
- **Source:** *Mentor 2 manual* | Nova | https://www.nova.eu/fileadmin/user_upload/glider/Manuals/Mentor2_V11_012011eng.pdf | C-facts

**Q5 flags**
- [FLAG] **Apparent conflict over brakes.** Niviuk says: "If a loss in internal wing pressure is felt, tension on the speed-bar should be reduced to a minimum" / "...and a slight pull on the brake lines is recommended to increase the wing's incidence angle." Ozone, Gin and Nova all say never to brake while accelerated. The two are consistent only if the order is kept: release the bar first, then brake. State it that way on the page.
- [FLAG] **Different tone on turbulence.** Advance says: "Thanks to its high stability the EPSILON 10 DLS can be flown accelerated in light turbulence without problem." (https://manual.advance.ch/en/epsilon_dls/1424, C-facts). The other manuals urge caution in turbulence. Both are model-specific; keep the general advice cautious.
- [FLAG] The Ozone Viper 5 (a reflex paramotor wing) says accelerating "can make the gliders recovery from a collapse more aggressive" (https://cdn1.flyozone.com/wp-content/uploads/sites/2/2021/08/Viper-5-manual-EN-v1.0.pdf). That is a paramotor wing, so cite it only as supporting evidence, if at all.
- The SHV/FSVL exam commentary makes the same point about shortening the A lines: "A front closure of the wing is more likely but the risk of a parachutal stall flight is reduced." (https://soaringmeteo.org/examenTheoriqueEN4.pdf, C-facts). Note it is a study aid, not an official SHV publication.

---

## Summary of disagreements and unverified numbers

1. **Paraglider glide ratio.** Sources split by era. SSA ("rarely greater than 8:1") and the SHV exam commentary (2005/2010, "hardly exceed 9") give low figures. Current manufacturer claims are 10 to 10.5 (Mac Para), and Wikipedia gives 9.3 to 11.3, "up to 13". Use current claims and say they are manufacturer figures.
2. **No CCC glide figure found.** Neither a manufacturer-published nor an independently measured figure turned up.
3. **Minimum sink.** Only manufacturer claims (1.05 to 1.15 m/s) were found. Mac Para's identical 1.05 m/s for EN A, EN B and EN C looks like a house figure. No independent measurement was found.
4. **Hang-glider glide** is given as 15, 16 or 17 to 20 depending on the source. **Sailplanes** are given as 40 routine, about 60 open class and over 70 for the Eta. These are consistent once the classes are separated.
5. **Wikipedia trim speed (32 to 40 km/h)** sits below current manufacturer data (37 to 41 km/h).
6. **Eden 7 top speed:** the 2020 brochure says "52 (±3)" and the website says "50-52".
7. **The Magus EN D label** is ambiguous on the brochure page.
8. **Wing-loading speed change:** simple physics predicts about 12% across the Eden 7 M weight range, while Mac Para's published trim band spans about 5%. Not reconciled.
9. **GFH headwind rule of thumb:** the wording needs checking against the PDF, because "speed" may be missing.
10. **GFH chapter edition** (13B) is inferred from the front matter, not printed on the chapter files.
11. **Brakes while accelerated:** Niviuk's "slight pull on the brake lines" applies after releasing the bar. Keep that order on the page.

## Gaps (not found or not retrievable in this session)

- PHAK (FAA-H-8083-25C) aerodynamics chapter: the index was reachable but the chapter PDF was not. GFH Ch. 3 is used instead.
- FAA Aviation Weather Handbook (FAA-H-8083-28) full text: table of contents only. NOAA JetStream and AC 00-6A are used instead.
- FAA Powered Parachute Flying Handbook: the PDF is too large to fetch. It would be the best public-domain source for the ram-air and pendulum explanation, so a manual check of its aerodynamics chapter is recommended.
- USHPA, BHPA and DHV explanatory pages: none found within the search budget, which ran out at the end of the session.
- A current CCC wing's glide or top speed. Also any manufacturer in the preferred list (Ozone, Advance, Gin, Nova, Niviuk, Skywalk) publishing speed, sink or glide numbers: none do for current wings.
- An independently measured paraglider polar.

---

## Sources to show on each page ("Sources")

**Q1. How does a paraglider fly?**
1. FAA, *Glider Flying Handbook* (FAA-H-8083-13B), Ch. 3 "Aerodynamics of Flight": https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_3.pdf
2. NASA Glenn Research Center, *Three Forces on a Glider*: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/three-forces-on-a-glider
3. NASA Glenn Research Center, *Lift Equation*: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-equation-2
4. FAA, *Weight & Balance Handbook Addendum* (pendulum): https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/Weight_Balance_HB_Addendum_(MOSAIC).pdf
5. Ozone, *Rush 6 Pilots Manual*: https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf

**Q2. How do paragliders gain altitude?**
1. NASA Glenn Research Center, *Gliders*: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/gliders/
2. FAA, *Glider Flying Handbook* (FAA-H-8083-13B), Ch. 10 "Soaring Techniques": https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_10.pdf
3. NOAA National Weather Service JetStream, *Parcel Theory*: https://www.noaa.gov/jetstream/upperair/parcel-theory
4. FAA, *Aviation Weather* (AC 00-6A), Ch. 16 "Soaring Weather": https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC%2000-6A%20Chap%2016-Index.pdf
5. Mac Para, *Eden 7* technical data (sink rate): https://www.macpara.com/en/previous-products/eden-7

**Q3. What is the glide ratio of a paraglider?**
1. FAA, *Glider Flying Handbook* (FAA-H-8083-13B), Ch. 5 "Glider Performance": https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf
2. NASA Glenn Research Center, *Drag to Lift Ratio*: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-to-lift-ratio
3. Mac Para, *Elan 3* technical data: https://www.macpara.com/en/paragliders/free-flying/elan-3/
4. Wikipedia, *Glider (sailplane)* (comparison table): https://en.wikipedia.org/wiki/Glider_(sailplane)
5. Skywalk, *CHILI5* (why glide figures are not comparable): https://skywalk.info/project/chili5/

**Q4. How fast does a paraglider fly?**
1. Mac Para, *Muse 5* technical data (EN A): https://www.macpara.com/en/paragliders/free-flying/muse-5/
2. Mac Para, *Elan 3* technical data (EN C): https://www.macpara.com/en/paragliders/free-flying/elan-3/
3. Sky Paragliders, *User's manual for ATIS 3*: https://sky-cz.com/media/cache/file/0f/5955-Atis3_manual_ENG.pdf
4. FAA, *Glider Flying Handbook* (FAA-H-8083-13B), Ch. 5 (weight and the polar): https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/glider_handbook/gfh_chapter_5.pdf
5. Ozone, *SwiftMax manual* (weight-range effect): https://cdn1.flyozone.com/wp-content/uploads/sites/1/2018/06/SwiftMax_manual_EN_v1.1.pdf

**Q5. What does the speed bar do?**
1. Gin Gliders, *Bolero 8 user manual*: https://static.gingliders.com/paragliders/bolero-8/documents/bolero-8-user-manual-en.pdf
2. Ozone, *Rush 6 Pilots Manual*: https://cdn1.flyozone.com/wp-content/uploads/sites/1/2021/06/Rush-6-manual-EN-v1.0.pdf
3. Niviuk, *Hook 6 manual*: https://niviuk.com/biblioteca/items/449_A/user_manual_tech_data_hook_6_niviuk_paragliders.pdf
4. Gradient, *Go user manual* (hosted by DHV): https://service.dhv.de/dbfiles/managed/pruefung/2019/07/go_manual_en_r0_fin.pdf
5. FAI, *What's Up With The New CCC Paragliders?* (accelerator limit): https://fai.org/node/21590
