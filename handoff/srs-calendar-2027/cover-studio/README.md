# The cover: SRS_6_T1_51 as a studio shot (website chat 30, 24 Nov 2026). Replaces the black/brush cover (fd335aa).

The owner sent a studio car photograph (slate backdrop, top spotlight, floor, a little motion blur) and said "make it look
like this, do the contour again", then "go". Our own identity only: the Paragliding Atlas logo once. Same facts as before.
- hud_grade.py DIR: the masks (work/mask_wing.png, mask_pod.png, mask_lines.png) from DIR/src.jpg (the 2400px photo as JPG).
- matte.py DIR OUT: a difference matte (the haze behind each edge pixel estimated and separated), so the outline and the
  lines keep their natural soft edge; the pod edged from inside (fields behind it). Writes OUT/matte.png, OUT/wing.png.
- scene.py OUT: the studio at print size (3369 x 2382): backdrop.png (spotlight, floor, speed smear, floor shadow) and
  glider_layer.png (the glider lit from above).
- st2_build.js OUT: the page (faint "SRS 2027" set into the backdrop, logo and facts).
- pages/01-cover-1200.webp and -2400.webp: the finished cover.
