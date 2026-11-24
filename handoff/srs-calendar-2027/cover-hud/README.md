# The cover: SRS_6_T1_51 in an F1 HUD style (website chat 30, 24 Nov 2026)

The owner: "try an f1 style inspired by deviant art or pintrest hud style wallpaper" for
https://paraglidingatlas.com/media-srs-tapalpa-2026.html#SRS_6_T1_51, then "no make it the calndar cover so edit it accoridngly".
Same facts as the cover it replaces: Sports-Class Racing Series, SRS 2027, Race calendar, the five rounds (place, country,
dates, Confirmed / Provisional). No invented telemetry: the HUD is graphics only (brackets, a target ring, scan lines).
- hud_grade.py: `python3 hud_grade.py DIR` (DIR/src.jpg = the 2400px photo as JPG) writes DIR/work/hud.jpg and hud_cut.png.
- hud_cover.js: `node hud_cover.js DIR` renders DIR/work/cover.png (3366 x 2379, A4 landscape at 3x, as build.js does).
- pages/01-cover-1200.webp and -2400.webp: the finished cover.
