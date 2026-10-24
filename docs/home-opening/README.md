# The home page opening: photo layers (chat 7, 24 Oct 2026)

Nothing here is on the site. These are the tools that made the photo choices
in the owner's review page https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG
(entries "F, with a choice of Kenya photo" and "The same choice for India").
The finished layers are that page's published files under `F2/` (read them
with the Artifact tool, `action: "read"`, `path`); the scripts are here so
the next photo can be made the same way.

## What one opening scene needs (design F, from C2)
For a place `p` and photo tag `t`: `p-t-ground.webp/.jpg` (the photo with
the gliders taken out), `p-t-wing.webp` (the gliders cut out, with their real
lines where the photo shows them), `p-t-shadow.png` (the cut-out's padded,
blurred silhouette at a third, for the shadow on the letters), and
`p-t-depth.jpg` (near is light). In F2/index.html each choice is one entry in
`PHOTOS` (sizes, pad, dim, desktop and phone placement); `?kenya=9522&india=launch`
picks them, and the pill at the top switches (review only).

## The scripts (set SCRATCH to a work folder; inputs in $SCRATCH/orig, work in $SCRATCH/k3)
- `sheet.py SRC_DIR OUT_PREFIX [n]`: contact sheets (three across, file name
  and size under each) for going through a Drive folder.
- `grade.py NAME...`: the site's grade for a full-size photo (haze cut,
  deeper, a little warmer, soft vignette) to `k3/NAME-graded.png`.
- `prep_site.py SRC NAME WARM`: the same, half strength, for photos that are
  already edited (the site's own copies).
- `seg.py NAME x0,y0,x1,y1 ...`: the gliders' mask, one box per glider (and a
  separate box for a pilot far below the wing), with rembg 2.0.67 and
  `birefnet-general-lite` (run it in its own venv; the model downloads from
  the rembg GitHub releases; huggingface.co is blocked here).
- `hough.py JSON` then `lineset.py JSON`: the real lines. Long straight
  segments of thin bright (or `"pol":"dark"`) ridges that run through the
  risers `C`, grouped into lines and followed from the risers to the wing; the
  alpha comes from the photo's own pixels. Tuned for 6000 px photos; scale
  `kern`, `minlen`, `perp`, `w` down for smaller ones.
- `scene.py JSON`: builds the four layers. The ground is filled tile by tile
  from clean ground nearby, over a smooth fill of the light (`lfd`: keep it
  small when sky meets dark ridge). Depth: Depth Anything v2 small ONNX from
  github.com/fabio-sim/Depth-Anything-ONNX releases (v2.0.0, `depth_anything_v2_vits.onnx`).

## The photos (owner's Drive, Paragliding Atlas > PG Atlas Photos > Photos by Self)
- Kenya Feb 2025: DSC_9452 (the photo C2 and F use), DSC_9522 (real lines
  found: 18), DSC_9492 (three gliders; no lines show). DSC_6210 is a 31 MB NEF,
  over the connector's 10 MB limit: needs a JPG export.
- India: no originals reachable. The Drive's India folder holds only the doc
  "Front Page Bir Billing"; "Hi Res Camera" (DSC00402 to 00426) is a launch
  above Oslo. The India choices use the site's 1400 px copies
  (`assets/destinations/india/gallery/red-wing.jpg`, `launch-day.jpg`), too
  small for lines; both are also in the India page gallery.

## Chat 8 (24 Oct): DSC_9492's follow shot
F2 only. For a photo with `push` in `PHOTOS`, the WebGL scene flies slowly into
the valley once (12 s) while the gliders shrink to 90% and drift toward the
valley's far point; one number `z` drives the gliders' size, drift, shadow gap
and darkness, and mouse pull. See `docs/v4-next-session.md` (chat 8) for the
numbers and the owner's words.
