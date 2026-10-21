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

The proposal (21 Oct, waiting for the owner's yes): on the record page, in
"01 The Mark To Beat", the harness flies across the gap between 35.94 and 36
from left to right with the scroll, nose down as in the photo, three orange
speed streaks behind it (the header's Speed Record mark), passing behind the
orange 36 on its way out; still and absent with reduced motion. It never
flies right to left: mirrored, its lettering would read backwards, which is
why it does not ride the course drawing out and back. Built, it belongs in
`tools/v4_record.py` (the record page is that tool's), the image in
`prototypes/v4/img/`.
