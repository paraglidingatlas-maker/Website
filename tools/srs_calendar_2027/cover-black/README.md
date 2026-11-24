# The cover: SRS_6_T1_51 lit on black (website chat 30, 24 Nov 2026). Replaces the HUD cover (c9a7d02), which the owner turned down.

The owner sent a reference (a racing car lit on black, with its reflection, an orange brush word and orange light) and said
"like this", then "fix the crop in the glider edges and then go live". Our own identity only: the Paragliding Atlas logo
once, no other brand's name, mark or type. Same facts as the cover it replaces (series, 2027, the five rounds and dates,
St Jean Montclar provisional), plus the photo line (Tapalpa, Mexico · SRS 2026 · Task 1 · Photo Aninder Singh).
- hud_grade.py DIR: the masks (work/mask_wing.png, mask_pod.png, mask_lines.png) from DIR/src.jpg (the 2400px photo as JPG).
- glider_cut.py DIR OUT: the glider lit for black (key and rim light, the pod lifted, the real lines drawn pale), its
  reflection, the orange light streaks; edges tightened and decontaminated so no haze shows.
- mc_build.js OUT FONTDIR: the page; the brush word uses Mr Dafoe (Google Fonts, SIL Open Font License), MrDafoe.ttf in FONTDIR.
- pages/01-cover-1200.webp and -2400.webp: the finished cover.
