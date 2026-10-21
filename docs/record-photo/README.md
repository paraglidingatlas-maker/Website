# The record page photo (DSC06347)

The owner's photograph of a pilot in the Paragliding Atlas pod harness,
turning fast (20 Oct 2026: "it looks like an iconic shot and the harness looks
quite fast while turning"). The owner's idea: take the background away so the
harness blends into a page as a backdrop that moves with the scroll.

- `DSC06347-chat-copy.jpg`: the copy the owner pasted into the chat (1336 by
  2000). The original is `DSC06347.ARW` (49 MB, Sony RAW) in the owner's Google
  Drive; the Drive connection cannot bring a file that size into a session, so
  the chat copy is what there is until a full-size JPEG is exported.
- `harness-cutout.png`, `harness-cutout.webp`: the pilot and harness cut out
  (346 by 239, transparent), from the crop (330, 1070) to (770, 1380) of the
  chat copy, by rembg 2.0.67 with the `birefnet-general-lite` model in its own
  virtual environment (`isnet-general-use` cut off the raised arm and the
  visor; `u2net` kept a block of flats). At up to about 250 px wide on the
  page it stays sharp on a phone; a full-size export would allow it larger.

Built (21 Oct, the owner's choice from mock-ups of four backgrounds: "go
with your mix"): on the record page, in "01 The Mark To Beat", the harness
crosses the gap between 35.94 and 36 from left to right with the scroll,
nose down as photographed, eased in the page's one loop, three orange speed
streaks behind it (the header's Speed Record mark), and slips behind the
orange 36, which lights as it passes. Round it on one canvas: wind lines
bending round it (one orange), speed lines that stretch with its speed, and
drawn clouds at three depths (drawn because no photograph is used twice on
the site; the photographed sky and the ground contours were left out). It
never flies right to left: mirrored, its lettering would read backwards.
Reduced motion: it waits in the gap (on a phone it is left out); without
JavaScript it is not there. The image is `prototypes/v4/img/record/harness.webp`;
the code is `tools/v4_record.py`, 01 the mark and the script's part 2b.
