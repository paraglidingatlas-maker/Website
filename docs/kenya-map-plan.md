# The Kenya map: the India engine adapted to six sites 451 km apart

Written after the India flight section (option E) was built, so that the Kenya
section is a copy of a working machine with new data, not a new design.

## What is different about Kenya

The Kenya page already carries six route cards with positions, bearings and
distances (Kerio Valley 0.72 N 35.65 E; Rift Valley National Park 0.90 S 36.30 E;
Mount Longonot 0.91 S 36.45 E; Kijabe Hill 0.93 S 36.58 E; Machakos Hills
1.52 S 37.26 E; Chyulu Hills 2.68 S 37.88 E). End to end that is about 380 km
north to south and 250 km east to west. India's whole box was 128 by 100 km at
32 m per pixel. The same resolution over Kenya would be a 14,000 by 10,000 pixel
grid: impossible to ship. So the Kenya map is two layers, not one.

1. **The journey layer.** One coarse terrain for the whole box: zoom 10 tiles
   downsampled twice, about 300 m per pixel at the equator, roughly 1,500 by
   1,100 pixels. Same size as India's phone textures. It carries the Rift, the
   lakes, the towns and the route between sites, and is what the camera sees
   while it travels at height between chapters.
2. **The site layer.** One inset per site, 30 to 40 km across, at zoom 12
   (about 64 m per pixel, roughly 600 pixels square, under half a megabyte
   each with its colour). Loaded only as the camera approaches that chapter,
   never all at once. Drawn on top of the journey layer with a feathered edge
   so the seam is invisible under the fog. Heights come from the same source,
   so the two layers agree; only the detail differs.

Everything else is the India system unchanged: the live terrain shader, the
scroll-driven path through chapter keys, the grab-the-ground hands, the labels
with their keep-out rules, plates that never cover their pin, the photo rings
and dialogs, the tracks with XContest scoring, the dotted landmark names with
stories, the towns in capitals, the lightbox with navigation, the dynamic
resolution. The script becomes a shared module with a per-site data block.

## What the India build cost us, and the rule that prevents it

| India revision | Cost | Rule for Kenya |
|---|---|---|
| Map concept changed three times (flat, pre-rendered frames, live terrain) | Days, 120 dead frames | Go straight to the live engine. No flat map, no frames. |
| Terrain box enlarged after the real flights arrived | A full texture rebuild | Tracklogs come first; the box is drawn around them. |
| Three waypoint names wrong (launch 5 km out, a "station" that is a ridge, a temple that is the other temple) | Rewritten stories, dropped pictures | Every point from a file; names confirmed by the owner before a story is written. |
| Flight figures redone to the XContest rules | A pipeline rewrite | The scorer exists; reuse it. |
| Commons pictures | The slowest step of the build, rate limited | The owner's photographs first; Commons only as a fallback, fetched early in the background. |
| Plates over chapters, pins under plates, stale states | Several rounds of screenshots | The India test set runs from the first build: desktop, the short wide window, the phone. |

## Inputs before the first render, in one go

1. **Tracklogs.** The owner's Kerio Valley IGC files from 7 and 12 February
   2025 (in the Drive folder), plus any others with permission. They fix the
   Kerio inset and give the flights to draw. Other sites may have none; the
   "Flights flown here" chips simply stay empty there.
2. **Points per site.** Launch, landing, turnpoints, with names, from a
   waypoint file if the local pilots keep one, otherwise read from the tracks
   and named by the owner. Site centres already on the page are the inset
   centres until a launch point replaces them.
3. **Chapters.** The six cards on the page, in order, are the chapters. Confirm
   them before the path is keyed; changing one later means re-keying.
4. **Photographs.** The 62 Kerio originals have no GPS. The camera clock and the
   IGC clock place them; one photograph with a known place checks the offset.
   The existing eleven frames and the Chyulu, Longonot and Equator pictures
   cover the other sites. Every photograph once; each assigned a ground point.
5. **Landmarks.** The owner names the places worth a dotted story and supplies
   their pictures, coded by site. Stories only from sources, shorter where the
   sources are thin.
6. **Towns.** GeoNames, as for India: Iten, Eldoret, Kabarnet, Nakuru, Naivasha,
   Nairobi, Machakos and the rest inside the box.
7. **Water.** The Rift lakes (Baringo, Bogoria, Nakuru, Elementaita, Naivasha,
   Magadi) from Natural Earth, drawn as flat tinted water on the journey layer.
   They are the strongest visual anchor the journey legs have.

## Look and light

- **Tint.** No snow line. Dry ochre on the valley floors, greens on the
  escarpment tops and the highlands, dark lava on the Chyulu range, the same
  site tones as India for the darks and the haze.
- **Exaggeration.** India uses 1.25. The Rift walls are already a kilometre in
  ten, so Kenya starts at 1.1 and the same value is used on both layers, or
  the seams show.
- **Light.** The Elgeyo escarpment at Kerio faces east; the eastern Rift wall at
  Kijabe faces west. One sun cannot model both, so the sun becomes a per-key
  value interpolated along the path, like fog already is: eastern light over
  Kerio, higher and more westerly down the Rift.
- **Approval from one still.** As India's stage one: one frame of the Kerio
  escarpment from the launch and one of the whole journey from height, signed
  off before the path is keyed.

## Build stages and gates

1. **Inputs gathered** (owner). Gate: the box drawn around the tracks and the
   six sites, agreed.
2. **Terrain.** Fetch the journey layer and the six insets once. Tint, pack,
   two stills. Gate: the look approved.
3. **Engine.** The shared module gains two things only: a second mesh layer
   with lazy loading and feathered edges, and height lookups that consult the
   inset when inside one. Path keyed to the six chapters with fast high transit
   legs and slow low site legs. Harness run on three viewports. Gate: preview,
   with the phone test of the drag.
4. **Content.** Photographs placed by time, plates windowed per chapter,
   tracks scored and drawn at Kerio, landmarks and towns, the route line with
   the page's own bearings and distances in the readouts. Gate: preview.
5. **Ship.** Gates, weight check, commit on an option branch, hand-off to the
   push session. The Kenya price stays off the page.

## Weight

Journey layer about 1 MB desktop, 0.3 MB phone. Each inset under 0.5 MB,
loaded on approach. Arrival weight stays at the India level or below, because
nothing is loaded for a site the visitor has not scrolled to.

## Open questions for the owner

- Which sites have tracklogs besides Kerio?
- Is the second card "Rift Valley National Park" the name the tour uses, or
  should the map say Hell's Gate? The map will say what the page says.
- Which of the 62 originals may appear, and are any of them not the owner's?
