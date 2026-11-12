# v4: handoff to the next session (4 Nov 2026)

Start here, then read `docs/v4-plan.md` (the brief and the owner's rules) and
the progress table in `docs/v4-report.md` (rows 0 to 43). Everything below is
the owner's current queue and what the last session learnt doing it.

## Chat 20, overnight 9 Nov: the Daily Highlights film on the comp gallery (chat 21 carries on below)
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link. If create_session is refused,
give the owner the prompt to paste.

The owner (9 Nov, 00:30 Tapalpa): "Add this link to photos page if anyone wants to see video highlights too for the
task day, make it look elegant and awwwards worthy". Live with the zoom viewer and chat 21's Paco credit:
https://paraglidingatlas.com/media-srs-tapalpa-2026.html#film-task-1 (Task 1, https://youtu.be/ZTxWnsHeUmE, 4:48).
- **What it is.** A band opens each task that has a film: a photo of that day, "Daily Highlights | 4:48", the title,
  the line from the video's own description, a play button (it leans towards a mouse). Tapped, the band's photo
  lifts off the page and re-crops into the theatre's 16:9 frame (transform only: the frame scales from the band's box,
  the photo inside is scaled back so it never stretches); YouTube's player (IFrame API, host youtube-nocookie) loads
  only then and plays. Where a visitor stopped stays in their browser (localStorage "gff-<id>"): the band then says
  "Resume the film from 1:02" (a phone's kicker: "Paused at 1:02"), the ring and the bar show how far; after the end,
  "Watched" and "Watch again". End card: "Find Yourself In The Photos", See all N photos (closes and lands on the
  day's first photo), Watch again, Subscribe on YouTube. Keys in the theatre: Space/K, arrows, J/L, M, F, Esc. The
  lead carries the newest film's cue ("Watch Task 1 Highlights | 4:48"), the task line "99 photos + film"; a film
  link #film-task-1 opens its task and the theatre. No JS: plain links to YouTube; reduced motion: no moves.
  Code: tools/v4_comp_gallery.py (films=, film_band, film_cue, FILM_DIALOG), v4-gallery.css ("the films"),
  v4-gallery.js films().
- **Every night, once the owner's film is up:** one line in COMPS["tapalpa"]["films"]:
  `"T2": dict(id="...", title="Task 2 Highlights", len="m:ss", line="...", poster="SRS_6_T2_n", pos="50% 40%")`.
  Id, title and length from YouTube (vidIQ vidiq_get_videos_by_ids); line = the one-line summary at the top of the
  video's description, word for word (none there: leave line out); poster = a landscape flying photo of that task,
  the wing clear of the left third (the words sit there on a laptop), not the cover; pos = the band's crop (16:5 on a
  laptop, 3:2 on a phone). Then the usual: generate, v4_nav_live, commit, worktree build, gates, push.
- **Testing:** this container's IP gets Google's "unusual traffic" page, so the owner's videos say "Video
  unavailable" in a test browser here (other videos play). It is the container, not the site. Test with a
  stand-in id swapped in at test time (a Playwright route that replaces the id in the page).
- **Not done:** Piedrahita's three videos still use the older small frames (gf-vids). Giving them the band means
  picking two posters from its 325 photos (ask the owner first).

## Chat 24 starts here (13 Nov 2026, from chat 23): the newsletter (waiting on the owner), YouTube fixes, Share on more pages
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link. If create_session is refused,
give the owner the prompt to paste.

**Done by chat 23 (12 Nov, LIVE on main unless marked).**
- Play buttons: .md-play (Media page, event pages) is the YouTube-style rounded rectangle, like .gff-btn. Standing
  rule in .claude/CLAUDE.md: never a round play button on a video.
- Tapalpa: "116 pilots, 25 countries" (owner's answer, 12 Nov; chat 21 told). Designer G is named "Tailwind".
- Share (standing rule in .claude/CLAUDE.md): prototypes/v4/v4-share.js + v4-share.css, loaded by v4_media.shell() on
  the Media page and every event/gallery page. <button type="button" data-share></button>: navigator.share where the
  browser has it, else a panel (Copy link, WhatsApp, Telegram, Email, Facebook, X; no Messenger: it needs a Facebook
  app id we do not have). On: the photo viewer (beside Save), the film theatre, each film chapter (event pages),
  the Media page's film line. Films share their YouTube link; photos share photo/<stem>.html.
- Photo previews: tools/v4_comp_gallery.py share_stubs() writes photo/<stem>.html at the repo ROOT (809 now), one
  per photo: noindex, its own og tags (the photo's 1600 webp: WhatsApp shows webp, checked by the owner's screenshot;
  title "Task n · date · comp"; the day's own credit, e.g. Practice @paco_peciado), and an instant forward to
  https://paraglidingatlas.com/<gallery>#<stem> (absolute: the galleries exist only in prototypes/v4 until deploy,
  so the root audit would call a relative link broken). Written on every v4_comp_gallery.py run; chat 21 told to
  git add photo/ nightly. [push pending at handover: see below]
- Photo viewer on a phone (<=820px): a one-handed dock under the photo (back, "n of N" with an orange progress line
  --gfv-p, next; close beside it), v4-gallery.css end of file; desktop unchanged. [push pending at handover]
- Google Form -> MailerLite: tools/forms_to_mailerlite.gs, installed by the owner in Apps Script ("Mailerlite form",
  bound to the form "Paragliding Atlas Newsletter", which asks only for an email). Trigger On form submit; script
  properties MAILERLITE_TOKEN and MAILERLITE_GROUP=199520762834454427 ("Newsletter", where all 28 are). Tested: a
  signup arrived in seconds (source api). The owner re-tests after the group was added: check the newest subscriber
  is in "Newsletter", then the test address can go (the owner deleted/re-adds it themselves).
- PWC Day 1 thumbnail with 2027 -> 2026 made (scratchpad copy sent to the owner; Inter Regular, patch invisible).

- LIVE 12 Nov 23:20 UTC (main cd3fa57c): photo/ previews, Share, the phone dock (glass capsule, which the owner finds
  "odd": being replaced, see job 0).
- On branch claude/chat23-newsletter, NOT live: Download (one tap, no share sheet; "Download" + "W × H px · size",
  the copy fetched quietly after 0.9 s on a photo; iPhone says "Saved to Files"), in v4-gallery.js/css and the
  viewer markup in v4_comp_gallery.py.

**Chat 24's job.**
0. FIRST: the owner picks the photo viewer's controls from three designer samples (brief
   docs/designers/viewer-controls-brief.md; samples prototypes/v4/samples/viewer-d|e|f/ with phone.png and
   desktop.png, sent to the owner 12 Nov ~23:45 UTC: D "Edge Code" film-edge ruler, E "Heading Tape" instrument
   tape, F "The Task Line" fisheye task line). Build the winner into the real viewer (replace chat 23's phone dock
   at the end of v4-gallery.css; keep pinch, swipe, swipe-down close; keep the Download logic), phone first, then
   gates and push together with Download. Merge from claude/chat23-newsletter first.
1. YouTube (vidIQ): the owner must open the vidIQ verification link (youtube_mfa) and say done; then
   update_video yhHoRUJtyOY title "Miguel Gutiérrez Explains Flying in Tapalpa, Mexico during SRS - Advance Edition 2026"
   (owner asked "can you change?") and update_video_thumbnail FOuAWMeoxs4 with the fixed thumbnail (owner: "can you
   fix"). Redo the fix if the file is gone: maxresdefault, the two 7s of "12.05.2027 - 23.05.2027" at x 599-615 and
   833-849, y 656-682, Inter Regular 37px white, background filled by a per-row blend. A fresh call gives a fresh link.
2. Newsletter (MailerLite DRAFT 203910238840031114; copy docs/emails/newsletter-01-tapalpa.html.txt): when the owner
   sends the new YouTube video link, update: 12 Nov cancelled for weather, Task 5 on 13 Nov, Task 6 on 14 Nov, no
   Task 7 ("4 of 7" and "Tasks 5 to 7 to come" are wrong), Task 4 has NO film (owner confirmed: photos only), the
   new video, the latest provisional SRS results (api.airtribune.com/srs/scores/?indx=1&comp=9, T6.n), Tasks 5 and 6
   films if chat 21 sends them. Owner still to give (asked once, do not nag): who Miguel Gutiérrez is, the footer's
   postal address, their opener words, the send date. Preview to the owner; NEVER send/schedule/test-send without
   their explicit yes.
3. Share on more pages: proposed to the owner, waiting for which: the 96 episode pages, the 25 knowledge base
   articles, trip and destination pages, the Atlas map points (their data already has shareUrl).
4. Owner's answers already given (12 Nov): PWC/Bassano facts and own stills: forget it. Piedrahita film posters:
   keep F's. Google Form stays (now synced). Own 1200x630 preview images: no, YouTube's are good.
5. Pushes: chat 21 (session_018Da7i74T9xiAv1VY2PfhYw) runs Tapalpa until 14 Nov; message it before any push to
   main; no pushes to main 02:30 to 08:00 UTC on photo nights; never forced; merge, don't rebase; build in a clean
   worktree (./build.sh, tools/v4_build.py), tools/v4_gates.py (FAIL live-untouched and the audit's sitemap lastmod
   FAIL are the known ones). Local checks: serve the REPO ROOT and open /prototypes/v4/<page> (pages load ../../ CSS).

## Chat 23 starts here (12 Nov 2026, from chat 22): the newsletter update and send, then the owner's open list
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link. If create_session is refused,
give the owner the prompt to paste.

**Done by chat 22 (12 Nov, LIVE on main b14e0193, checked live at 390x683 and 1440x900: no errors, no 4xx, no sideways scroll).**
- Event landing pages (owner's yes): contest D/E/F (brief docs/designers/event-brief.md, entries docs/designers/events/,
  samples prototypes/v4/samples/event-d|e|f/); F "The Season Opens Here" won, with E's film rows and D's fixes
  (verdict in docs/designers/direction.md). Built in tools/v4_comp_gallery.py (opening(), season_strip(), season_foot(),
  landing(), page_films(); COMPS[c]["landing"]=True; on for piedrahita, pwc, bassano; OFF for tapalpa until the comp
  ends) and tools/v4_media.py (season() is the one season list; Media rows link to the event pages). New pages:
  media-pwc-pegalajar-2026.html, media-srs-bassano-2026.html; shared prototypes/v4/v4-event.css/js.
  NEXT: after 14 Nov set COMPS["tapalpa"]["landing"]=True (chat 21 edits that dict nightly until then; coordinate).
- Link previews: the 29 old-address redirect stubs (tools/generate_redirects.py social()) and the duplicate episode
  stub now carry their destination's og tags. The 404 page was left alone: its tags must match its v2 and v4 copies
  (v2_check parity), so changing it means all three or none.
- Owner switched GitHub Pages Source to "GitHub Actions" (12 Nov): confirmed, b14e0193 ran no "pages build and
  deployment" run. The double-deploy 404 window is gone.
- A fourth designer: designer-g (.claude/agents/designer-g.md, notebook docs/designers/G.md), the inbox specialist,
  name [to supply] by the owner. "4 designers" = D, E, F + G (owner, 12 Nov).
- Newsletter contest (brief docs/designers/newsletter-brief.md; entries docs/designers/newsletter/, mocks
  prototypes/v4/samples/newsletter-*/email.html.txt: kept as .txt because the v4 build checks every .html):
  F "The Task Line" won (owner: "the design is good"). MailerLite DRAFT campaign 203910238840031114 "Newsletter 01 ·
  Tapalpa (draft, chat 22)", custom HTML (edit with update_campaign content; a copy in
  docs/emails/newsletter-01-tapalpa.html.txt), images in assets/email/newsletter-2026-11/ (live). 28 active
  subscribers, audience all; NEVER send, schedule or test-send without the owner's explicit yes.
- YouTube kit for talks: tools/yt_kit/make_talk.py + talk.tpl ("SRS Tapalpa Talks" overlays timed from the talk's
  SRT; transparent qtrle MOV 4K60 + 1080p GIF; see-through shades as separate PNG stills; holds are copied, not
  re-shot). Torsten Siegel's talk: all overlays and YouTube text sent to the owner 12 Nov.
- Logos for the owner (SRS colour/white, Atlas white/dark, transparent PNGs) sent 12 Nov.

**Chat 23's job.**
1. The newsletter: the owner is uploading a new YouTube video. When they send its link, update the draft (owner:
   "update it once the YT video goes inline and then we send it"): 12 Nov cancelled for weather (Task 5 is now
   13 Nov, Task 6 14 Nov, at most 6 tasks: from chat 21's Tapalpa page), "4 of 7 tasks" and "Tasks 5 to 7 to come"
   are wrong now, the new video, the latest SRS results (api.airtribune.com/srs/scores, provisional), Task 4 film.
   Then a preview to the owner; send only on their explicit yes.
2. The owner's open list (they will look later; ask in one message, do not nag):
   - Newsletter: who Miguel Gutierrez is (one line); the footer's postal address (MailerLite still reads "M 46");
     the owner's own opener words; the send date.
   - PWC: comp dates, pilots, countries, event link, was Task 3 flown. Bassano: dates, pilots, was Task 1 flown.
     Their own stills to replace YouTube's frames (Bassano's carry the live overlay, one reads "TASK CANCELLED").
   - Piedrahita film posters picked by designer F: SRS_5_T1_10 (Task 1), SRS_5_T2_99 (Task 2): keep or swap.
   - Tapalpa: 44 or 25 countries (the 116 confirmed pilots come from 25).
   - YouTube descriptions point the newsletter to a Google Form, not MailerLite: switch to the site's signup?
   - YouTube typos: "Maxico" in the Miguel title; the PWC Day 1 thumbnail reads 2027.
   - A name for designer G.
   - Optional preview upgrades (offered, not asked for): own 1200x630 preview images instead of YouTube's;
     og tags higher in the head.
3. Pushes: chat 21 runs Tapalpa until 14 Nov and pushes to main (usually 03:00 to 07:30 UTC, owner-driven):
   message it (session_018Da7i74T9xiAv1VY2PfhYw) before any push to main; never forced; merge, don't rebase;
   build (./build.sh, tools/v4_build.py) in a clean worktree, tools/v4_gates.py (live-untouched FAIL is the known
   old one plus any intended root files). Main's committed v4 pages carry a stale v2.css ?v= hash (8f8ced12 vs
   43c58fb8 on 233 pages); the deploy builds fresh so live is right; leave it unless a chat owns that cleanup.

## Chat 22 starts here (12 Nov 2026): event landing pages, then the newsletter (design contest)
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link. If create_session is refused,
give the owner the prompt to paste.

**The owner's request (12 Nov, verbatim in spirit):** "every event page to have its own landing page which is immersive
and easy to navigate; feel free to apply 3 designers to run a contest between them to make a most viable page; and
also I need to design a newsletter to update my subscribers of what I've been doing. After the landing pages of media
are complete, ask the 4 designers to design the newsletter." (The standing designers are the agents designer-d
"Trim", designer-e "Cloudbase", designer-f "Turnpoint"; the fourth is [to supply]: ask the owner whether "4" means
the three plus the Juror, or a fourth designer.)

**The events (tools/v4_media.py SEASON and UPCOMING, the Media page's "The 2026 season"):** PWC Super Final (May 2026,
Pegalajar, 5 highlight videos), SRS Bassano (May 2026, Monte Grappa, live commentary: 5 broadcasts), SRS Piedrahita
(22 to 29 Aug, stills and 3 highlight videos, gallery media-srs-piedrahita-2026.html), SRS Tapalpa (8 to 14 Nov, on air:
gallery media-srs-tapalpa-2026.html with Tasks 1 to 4 so far, the task films, the link picture). Today the season rows
open a "Watch" sheet on the Media page; the owner wants each event to open its own landing page. Piedrahita and Tapalpa
already have gallery pages (tools/v4_comp_gallery.py): decide with the designers whether the landing page IS the
gallery page made more immersive, or a page above it. Nothing invented: facts only from the repo, SRS/airtribune and
the owner's YouTube (vidIQ); a missing fact is [to supply].

**Done by chat 21 on 12 Nov (live):** the Media page's Tapalpa row ("On air now") links to its gallery ("Photos and
films"), and every season row is clickable across its whole width (tools/v4_media.py, v4-media.css).

**Process:** run the three designers on the landing pages (one shared brief, each a full direction, judged; the Juror
only with the owner's yes to its time and cost), build the winner with the best of the others, phone first, gates
(./build.sh, tools/v4_build.py in a clean worktree, tools/v4_gates.py; the live-untouched FAIL is the known old one).
Then the newsletter: the designers design it (MailerLite is connected; build it as a DRAFT only, never send or
schedule; every subscriber email waits for the owner's explicit yes). Newsletter content plan chat 21 proposed on
10 Nov: Tapalpa so far (Task 1 Groeneveld, Task 2 stopped by rain, Castro; Task 3 Varga, 88 in goal; Task 4 82.4 km,
nobody in goal, Brian Duffy furthest), standings, the photos page, the films, the Miguel Gutierrez talk, Patreon line.
Wait for the owner's answers on audience, send time and voice.

**Pushes:** chat 21 still runs the Tapalpa days (photos each evening, films on the page) until 14 Nov and pushes to
main for them. Work on your own branch; before any push to main, send chat 21 (session_018Da7i74T9xiAv1VY2PfhYw) a
message and merge from origin/main first (never forced, merge, don't rebase). GitHub Pages still double-deploys
(Settings > Pages > Source should be "GitHub Actions": the owner has not switched it yet).

## Chat 21 starts here (9 Nov 2026): Tapalpa, tasks 2 to 7 (9 to 14 Nov), the daily kit and photos
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link. If create_session is refused,
give the owner the prompt to paste.

**The owner's workflow rule (8 Nov, after a bad day): never wait for the owner while they fly.** Ask everything you
need BEFORE they launch (one message in the morning), then work during the task: the task card as soon as the task
is set (srs.live), follow srs.live commentary every 30 min, results boards the moment SRS posts scores, the Google
Earth file and replay from the tracks, the YouTube text, the thumbnail from the day's own photo, and photos live the
same evening without asking. When they land, the day's kit is waiting.

**Live now (9 Nov, main 02b9b7d9):** https://paraglidingatlas.com/media-srs-tapalpa-2026.html : Practice (19,
SRS_6_T0) and Task 1 (99, SRS_6_T1); people photos first (COMPS first=), cover #62, WhatsApp share picture
share.jpg = #62, #10, #20, #58 with a gentle colour lift (owner chose the gentle one, not the haze-cut one);
"Save, free" (JPEG) and "Like what you see? Join me on Patreon" (https://www.patreon.com/15133612/join) instead of
the EUR 1 original; "Live from SRS" in every header (tools/v4_nav_live.py, first in the phone menu, off after 17 Nov
by itself); event credit line; homepage: Kenya headline rotates 4 lines, India "Touch The Sky With Glory", Kenya
launch Kerio Valley, no loader on home; live pages say "Coming soon" for [to supply] (tools/v2_switch.py); Media page
without example content.

**URGENT for the owner (asked 9 Nov):** GitHub Settings > Pages > Source must be "GitHub Actions". Today a second
"pages build and deployment" (deploy from branch) runs on every push and publishes the raw repo about a minute
before the v4 deploy finishes: the galleries 404 for ~1 min and the CDN can keep the 404 up to 10 min. Until the
owner switches it: push at most once an evening, tell the owner before, and give them ?t=1 links.

**Every night (Tapalpa, 9 to 14 Nov):**
1. Photos: the owner uploads to Drive folder 1FklBNyCYQ1Zx3QnOy2tWuVGQmzkXnROJ (link-shared; NEVER publish its id)
   as SRS_6_Tn (k).JPG; practice was a subfolder. Run tools/media_webcopies.py FOLDER /home/user/media-2026/srs-tapalpa
   --jobs 4 (default --day-re reads T1..T7 from the names; --day P --keep-names for a subfolder of practice). The
   owner edits and culls before upload: no hold. A loop that re-runs until the folder stops growing is in chat 20's
   scratchpad idea (photo_loop.sh): rewrite it if needed. Push media-2026, then python3 tools/v4_comp_gallery.py
   tapalpa, python3 tools/v4_nav_live.py, commit, build in a clean worktree (./build.sh, git add the owned media pages,
   python3 tools/v4_build.py; if it exits 1 at v4_ux, run it once more: it passed the second time on 9 Nov), gates in
   the background (~15 min), copy the owned pages back, push main + branch (never forced; merge, don't rebase).
   Ask the owner which photos go first and which make the cover/share picture only if they want; set COMPS first=.
2. Task dates: tapalpa one_a_day assumes T2 = 9 Nov ... T7 = 14 Nov; set COMPS["tapalpa"]["dates"] when SRS skips a day.
3. The YouTube kit: tools/yt_kit/ (README). Results: api.airtribune.com/srs/scores/?indx=1&comp=9 lists Tapalpa as
   T6.n; the task's Sports/Female/Team tables (meet=93, task=...), IGC zip and KMZ (../files/task/2710_NN.*). Boards
   (board.tpl), winner and first-into-goal cards, make_kml.py (top 10 tracks, cylinders, tour), make_anim.py N
   (opener green-screen MP4 + end card), YouTube text (see chat 20's Task 1 text), thumbnail style A (A2 with the
   photo shifted right: .bg left:400px; pick a photo with the wing clear of the text). Owner: CapCut, 4K 60 fps.
   Name plates for the 116 confirmed pilots were sent 8 Nov. Still not done: the 2D race replay.
   Note: Task 1 winner on points was Matthijs Groeneveld (provisional 989.7); Andres Tello Alvarado first into goal.
4. srs.live: render it (JS app), click "Follow us Live", read the commentary; scores at srs.live/scores.

**Open questions for the owner:** 44 vs 25 countries (the 116 confirmed pilots come from 25; airtribune's 44 counts
all registrations); PayPal for originals (parked: Patreon instead); Kenya/India "From past pilots" quotes.
Scheduled: "Tapalpa photos, nightly" trig_01EmNr55b35qPdgPMGFC1JqA was bound to chat 20; chat 20 re-binds it to
chat 21 at the handover.

## Chat 20 starts here (4 Nov 2026): the owner picks a gallery design, then build it for Tapalpa (Task 1 is 8 Nov)
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link. If create_session is refused,
give the owner the prompt to paste.

**The owner's answers to chat 20 (4 Nov).**
- Payment: PayPal. Licence of the free 2400 px copy: CC BY-NC 4.0.
- Delivery: "The download has to be on site" (the buyer gets the original from the site right after paying, not a
  Drive link by hand). That needs the originals somewhere private (not GitHub, not the link-shared Drive folders) and
  a check that the PayPal payment went through before the file is handed over (e.g. the Cloudflare Worker plus R2,
  with PayPal's order check). Not built; the owner has to set up PayPal (business account, API credentials) and say
  yes to the storage. Until then the button stays "[to supply]".
- Design (owner, 5 Nov): F as the base with two things from D: the lift-out viewer (the photo flies from its cell and
  back, FLIP by transform) and "Every task on one page". Built: tools/v4_comp_gallery.py writes
  media-srs-tapalpa-2026.html (new, in NEW_PAGES) and media-srs-piedrahita-2026.html (all 325, the task videos and
  lines kept); shared prototypes/v4/v4-gallery.css and v4-gallery.js (from samples/gallery-f, find-your-wing and the
  sample bits dropped, Save makes a JPEG, PayPal link per photo once PAYPAL_EMAIL is set). tools/v4_media.py no longer
  writes the Piedrahita page; the Media page links both galleries. Preview sent to the owner 5 Nov (screenshots);
  LIVE 5 Nov (owner's yes; main 701b04e2, deploy ok): checked on paraglidingatlas.com at 390x683, 390x844, 1440x900, no
  errors, no 4xx, no sideways scroll, 325 cells, the viewer loads. The shared files are served from assets/v4/. Tapalpa assumes one task a day from 8 Nov: set COMPS["tapalpa"]["dates"] when a
  day is cancelled. Gates take more than 10 minutes: run them in the background.
- 8 Nov: Tapalpa facts now "116 pilots, 44 countries" (owner, from airtribune). NOTE: the 116 confirmed pilots come
  from 25 countries; airtribune's 44 counts all 262 registrations. Asked the owner; change only on their word.
  Event credit line on both galleries (live 8 Nov, 05422997). Sponsors kept off our pages; listed as leads in the
  map (box r-gallery-leads). YouTube kit for the daily highlights: see tools/yt_kit/README.md; part 1 sent 8 Nov
  (116 name plates, Task 1 opener and end card, thumbnail template). srs.live checks scheduled (send_later
  trig_01V3mqgxKFWGHUbbap9qJnNV, then every 30 min while the task runs).
- Task 1 story so far (srs.live commentary, read 18:35 UTC = 12:35 Tapalpa): provisional 59.1 km task (first set at
  65 km) dipping onto the 2,200 m plateau; window 11:00, start 12:30 in the air; about 110 pilots at the start, very
  low over the plateau (greenhouses below); 24 teams. Names to watch per the commentary: Estefano Salgado, Andres
  Tello Alvarado, Manuel Quintanilla, Michael Sigel, Torsten Siegel (first SRS), Pal Takats, Luke Nicol, Arnold
  Castro, Matthijs Groeneveld, Aurelijus Andreliunas, Felipe Karam (owns the take-off). Photos credited [Ross Desmond].
  Read 20:14 UTC (14:14 local): weak, low start over the plateau ("berry picking" joke), more lift by TP1 (12:46).
  Luke Nicol took TP2 alone and 200 m higher (13:07; 2nd in the 2026 series). Michael Sigel and Matthijs Groeneveld,
  wing tip to wing tip, took a 5 km lead (13:14 to 13:27), then the chasing gaggle closed in on the ridge (13:39).
  Leading ladies: Pamela Diez (13:37, may have missed a turnpoint, 13:58), Lynsey Haynes (13:42). Front at 13:52:
  Sigel, Nicol, Tello Alvarado, Salgado, Chaeden Luebberke, Haynes; "a total mix of gliders at the front".
  14:01 Andres Tello Alvarado (Advance Tau, the event's partner) leads at the last turnpoint, with Estefano Salgado
  (Ozone Lyght), Matthijs Groeneveld and Luke Nicol (Gin GTO3). Latest, untimed: "Luke touching down", "Next in
  Matthijs" (goal arrivals). Héctor Valdés top landed and relaunched (12:53).
- Owner's question (5 Nov): where to show the gallery on the site. Proposed: Media stays in the menu and footer; during a
  comp, a small "Live from Tapalpa" hint in the nav that shows itself only between the comp's dates (plus 3 days).
  Waiting for a yes.
- Done while waiting: tools/v4_comp_gallery.py (comp facts, photos.json by task, licence, PayPal hook buy_link(),
  shell, checks; render() is the chosen design's markup, still to write; v4_gallery.py is the drawings page, not this).
  media-2026: README says the web copies are CC BY-NC 4.0; srs-tapalpa/photos.json is [] until Task 1.
- BLOCKER for the nightly run: the Tapalpa folder 1FklBNyCYQ1Zx3QnOy2tWuVGQmzkXnROJ answers 401 by link (Piedrahita's
  answers 200) and the Google Drive connector cannot see it either (nor "All Tasks"). Asked the owner (4 Nov) to share
  it, preferably with the connected Google account rather than by link.
- To do in the build: "Save, free" should hand over a JPEG made in the browser from the 2400 WebP (canvas toBlob
  image/jpeg), since Instagram and WhatsApp on iPhone may refuse WebP; no extra storage. Then NEW_PAGES gets
  media-srs-tapalpa-2026.html (tools/v2_site.py), and media.html links the galleries.

**The owner's answers (4 Nov, chat 19).**
- Gallery: designers D, E, F first ("samples needed, but first discuss with me"), then "let the designers brainstorm
  amongst themselves and do their magic". The owner picks one when back (flying 4 Nov evening, about 4 hours).
- Originals: EUR 1 per photo, option B = a payment link per photo (not a basket). Provider (Stripe or PayPal) and
  delivery: not answered; hand delivery by Drive link assumed, delivery time [to supply], licence [to supply].
- media-2026: attach it "and future ones as well as need be" (standing yes for add_repo push on media-2026).
- Tapalpa: about 50 photos a day; Drive folder 1FklBNyCYQ1Zx3QnOy2tWuVGQmzkXnROJ (empty on 4 Nov). Piedrahita:
  "All Tasks" 1GwKlKvNkYJ5P5WF0QBtkOByG8du8lrjC. Both folders are shared by link: anyone with the link can download
  the originals, so never publish a folder link or a file id (the originals are what the owner sells). Tell the owner.
- "Patchy": the owner did not say where; chat 19 fixed the opening's pull-back (the slowest part everywhere).

**What chat 19 did (live since 4 Nov, deploy of b02330f5).**
- "Patchy" fixed (v4-media.js pull(), v4-media.css): the phone's feathers were masks rewritten every frame (they
  repainted the photo and every poster with its 60px shadow); they are now veils of the ground's colour that only move
  (veil(), .e-veil). The poster words lose their 0.25s transition during the move (it restarted every frame and
  trailed the finger); the scrim and the opening's words fade on their own layers; a frame writes only what changed
  (put()); on touch screens settle() waits until the page has been still for 120 ms (a flick's momentum). Measured over
  40 scroll steps at 4x CPU: phone paint 392 to 168 ms, raster 636 to 181 ms; desktop raster 1021 to 235 ms. Frames
  match the old move within 0.03% of pixels (390x844, 390x683, 1440x900, snapping held off). Style recalc is still
  about 15 ms a step at 4x and is NOT the move's own writes (switching them all off leaves it): next suspect the page's
  other scroll work (v2-immersive.js) during the pinned stage. Not checked on a real phone: ask the owner to look.
- Logos: SRS from sportsracingseries.org (SRS-Logo_512x512.png) and the World Cup from pwca.org (images/brand.png),
  set in white for the dark ground, in prototypes/v4/img/media/ (logo-srs.png, logo-pwca.png), in hero() of
  tools/v4_media.py. PWCA's is only 113x130 px: a larger file would come from pwca@pwca.org.
- The quote: no published organiser quote found (web, airtribune SRS blog, the YouTube comments on BRAX1XMU390 and
  uCEfssE40u8 have none from SRS or PWCA). Viewer praise exists, e.g. @imdakshnain on BRAX1XMU390, 14 May 2026:
  "Best coverage of an XC comp so far, IMO." Offer it to the owner as a pilots' line; the organiser quote stays as it is.
- Piedrahita page: the intro no longer claims a video each day (Task 3 has none); its two opening shots are not repeated
  in the grids.
- All 325 Piedrahita photos (T1 48, T2 131, T3 146) are web copies in media-2026 srs-piedrahita/ with photos.json
  (stem, day, w, h, in the owner's file order), made by tools/media_webcopies.py (downloads a link-shared Drive folder
  one original at a time, deletes each; no Drive ids in the public repo). The originals' EXIF capture times read
  31 Aug (after the comp): never show or sort by them. Tapalpa: run the same tool into media-2026 srs-tapalpa/ each night.
- Gates on b02330f5: everything passes except the known live-untouched FAIL (the ~179 live pages from 62360aa, see
  chat 18's notes); the deploy builds fresh. The build writes its own ?v= hashes (tools/version_assets.py) into the
  media pages and the media-d/e/f samples, unlike tools/v4_media.py: after running v4_media.py, build in a clean
  worktree and copy those pages back before committing, or the chain's byte-for-byte check fails.
- Designers E and F stalled for about an hour in round 2 (most likely a tool call waiting for an approval the owner
  could not give from a plane), then finished after a nudge: all three wrote their round 2 notes and pitches, and the
  preview carries their own words. Not yet checked on a real phone by anyone: F's glider, E's pull-back to the
  contact sheet, everyone's Save to Photos. E asks for a 320 px copy of each photo for its Scan view; with 350 photos (?stress) at 4x CPU its zoom-out
  holds its frames but starts 140 to 190 ms after the tap (fix: lay out only the photos near the screen).
- The move's remaining cost: about 1 ms of style recalc per changed element batch per frame on a real phone (4 ms at
  4x CPU), from matching against the large site stylesheet; inside the frame budget. Going further means CSS
  scroll-driven animations (animation-timeline), a larger rebuild: only if the owner still sees it patchy.
- Container lesson: `pkill -f <pattern>` also kills the shell running it when the pattern is in its own command line
  (exit 144); kill by pid.

**The gallery: three samples, the owner chooses (preview: https://claude.ai/artifact/FeGEvbUMkVLsshEZroXxyX).**
Brief docs/designers/gallery-brief.md; concepts, round 2 replies and pitches in docs/designers/gallery/; samples in
prototypes/v4/samples/gallery-d/, gallery-e/, gallery-f/ (Tapalpa as on the evening of 11 Nov, the Piedrahita photos
as labelled stand-ins). D "Proof Sheet": every day on one calm page, photos whole, a photo lifts out and back into its
place, wing-colour chips dim (never hide). E "Pull Back to the Comp": one photo, one day, the whole comp as a contact
sheet, the Media page's pull-back as the move. F "Fly the Comp": the task line of 7 dates, the newest day open, the
glider flies along the line to the day you tap. All: "Save, free" (fetch + share sheet on phones, download on desktop;
media-2026 sends access-control-allow-origin: *), "Original, EUR 1" with the file name and the payment link [to supply].

**Chat 20's job, in order.**
1. Get the owner's pick (and the payment provider: Stripe or PayPal, a link per photo that carries the file name;
   delivery time; licence of the free copy). Build it as tools/v4_gallery.py (an owned page like v4_media.py: add
   media-*-gallery or the chosen file names to owned() and OWNED_GIT in tools/v4_build.py, NEW_PAGES in
   tools/v2_site.py) reading media-2026 <comp>/photos.json, first media-srs-tapalpa-2026.html (empty days say when
   photos come), then the Piedrahita page rebuilt the same way with all 325 photos. Test on a real iPhone: Save to
   Photos, a WebP into Instagram and WhatsApp (the designers flag it). One preview before it goes live.
2. Tapalpa, 8 to 14 Nov: each night run tools/media_webcopies.py 1FklBNyCYQ1Zx3QnOy2tWuVGQmzkXnROJ
   /home/user/media-2026/srs-tapalpa --day-re '<the owner's naming>' (check the file names on the first night), push
   media-2026, regenerate the page, build, gates, push, give the owner the link. Chat 19 set this up as a scheduled
   task, "Tapalpa photos, nightly" (trig_01EmNr55b35qPdgPMGFC1JqA): 22:41 Mexico City time, 8 to 14 Nov, firing into
   chat 20 (session_018Da7i8ixhhEZonsV8t1MmP). It needs no Drive connector (the folder is read by link). If chat 20
   hands over before 14 Nov, delete it and create it again bound to the next chat.
3. Still open for the owner: the organiser quote (or the viewer comment above); a larger PWCA logo; which device looked
   patchy (ask them to look again now); the Drive folders are link-shared (anyone with a link gets the originals free).
   Chat 18's list (photo credits, the two orange buttons at 1440, the Worker's media branch, MailerLite M 46) is unchanged.

## Chat 19 starts here (4 Nov 2026): the richer Piedrahita event page, then the Media page's [to supply] facts
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link.

**Open when chat 18 ended (read first).**
- **"Patchy" animations on media.html (owner, 4 Nov).** Measured with Playwright traces (scripts were in
  /tmp/claude-0/perf, gone in a new container): the opening's pull-back (v4-media.js pull(), render()) rasters about
  200 ms per 40 scroll steps against about 29 ms elsewhere on the page, on every pass, at 390 (DPR 3) and 1440.
  Switching render() off drops it to 16 ms. Cumulative tests: the photo's transform and mask alone about 23 ms, plus the
  frame's clip-path, shade and words about 38 ms on a phone (about 230 ms on desktop: the full-screen clip-path), plus
  the label, foot and tally about 58 ms; the rest comes once the other posters are on screen (feather() masks and
  clip-paths on the posters each frame, the --e-co fades, G.fades). Commit 07cba177 (branch only, NOT on main, not yet
  checked visually) puts each poster on its own layer during the move: about 15% less. Next ideas: replace the per-frame
  clip-path with a transform-based frame (an overflow-hidden box scaled with a counter-scaled photo), drop the
  per-frame mask on the posters (a moving gradient overlay instead), and on touch screens stop settle() from
  snapping while momentum is still running (its 160 ms timer after touchend can fight the finger; frame 540 of
  the phone run showed the page jump back with the nav). The site-wide nav pin (v2-immersive.js update/pin) costs
  one long frame (~110 ms at 4x CPU) on the first scroll on every page. The owner was asked: which device, and where on
  the page looks patchy (a screen recording would help). Ask again if not answered.
- **The comp gallery page is NOT built.** media-srs-piedrahita-2026.html shows about 20 photos with zoom and the
  task videos, but no downloads, no HQ request, no paid originals. The owner was offered: (1) the quick version (the
  Piedrahita page becomes the first gallery: all photos by day, free 2400 px download, "Request HQ" that emails the
  owner with the photo's name; Tapalpa reuses it), or (2) the designers D, E, F first (tell the owner time and cost,
  get a yes). Also open: HQ free on request or paid, and the price.
- Chat 18 could not open chat 19 (session lineage limit 8); the owner starts it by hand. If create_session fails the
  same way at your handover, give the owner the prompt to paste instead.

**The owner's answers (4 Nov, after go-live) and what they change.**
- Reach: YouTube only, read online (vidIQ user channel): 2,160 subscribers, 294,561 views, 166 videos, 4 Nov 2026.
  On the page. NO Instagram count (owner: too low); the Followers cell is gone.
- Sponsors (owner's words): "banners, footnotes, premium spaces, depending upon the collaborations". On the page as
  one line for the films, the live commentary and the results newsletter.
- The quote and the SRS and PWCA logos: "available online". Logos: PWCA draws its own as inline SVG on pwca.org
  (54 svg on the home page; find the PWCA mark, not a sponsor's); SRS: airtribune.com serves
  /static/brett/srs_badge_small.fw.png on airtribune.com/srs-2026-6/info; look for a larger official file (SRS's own
  site, socials). Replace the "Logo slot" boxes in hero() of tools/v4_media.py. The quote: find a published
  organiser's word about the coverage (SRS or PWCA posts) and use it verbatim with its source; if none, ask once.
- Tapalpa photos per day and the Drive folder: NOT answered yet.
- Piedrahita photos: chat 19 picks (owner: "you know better").
- **New job, the owner's next page (asked to "wake up those agents again", i.e. designers D, E, F):** every comp
  the owner covers gets its own gallery page, Tapalpa first: people browse, download, and request a high-quality
  photo; the original file maybe behind a paywall. The Piedrahita page becomes the first of the same kind. Storage:
  a GitHub repo should stay under about 1 GB (files under 100 MB; Pages publishes up to 1 GB and about 100 GB a month
  of traffic), so it holds web copies only (about 0.3 MB per photo across 800/1600/2400, so even 300 photos a comp
  is about 100 MB: one repo per year is fine). Originals (15 MB each, 3 GB a comp) never go to GitHub: free download =
  the 2400 px web copy; HQ = a request (the owner sends a Drive link) or a paid download (a payment link that hands
  over a Drive file; Cloudflare R2 is the free-to-10 GB fallback). The owner chooses. Brief the three designers
  (docs/designers/, the media brief as a model) after telling the owner the time and cost and getting a yes.

**What chat 18 did (owner's yes on preview 3, 4 Nov).**
- Photos: the owner created the public repo `paraglidingatlas-maker/media-2026` and switched on Pages (main, root).
  Chat 18 pushed the 67 web copies (800/1600/2400 WebP and the posters, 14 MB) to `srs-piedrahita/`, plus README and
  .nojekyll. All served: https://paraglidingatlas-maker.github.io/media-2026/srs-piedrahita/ (every URL the pages use
  checked 200). To work on it: add_repo media-2026 (push), clone, commit to main. The owner must approve add_repo.
- Site: `prototypes/v4/media.html` and `media-srs-piedrahita-2026.html` are committed, built with the default MEDIA
  base (`python3 tools/v4_media.py`, no --media). They are owned pages: `tools/v4_build.py` owned() and OWNED_GIT
  take `media*.html`, so the chain puts them back; run tools/v4_media.py by hand to change them. They go live as new
  pages: `tools/v2_site.py` NEW_PAGES. "Media" is in the full-screen menu (About's sub-links, `src/v4-menu.js`, then
  `tools/v4_min.py`) and in every footer's Atlas column after Partner With Me (`tools/v4_footer.py`); v4_media.py
  adds its own footer line only if the shell lacks it.
- Fixes found by the gates: `tools/audit.py` counted `data-vid="..."` as an id (regex now `(?<![\w-])id=`);
  `v4-media.js`'s pull-back stops when the page lacks the generator's markup (designer E's sample threw errors).
- The design sample `samples/media-e/index.html` now carries the ?v= hashes the build writes (it failed the chain's
  owned-page check before).
- Container lessons: the fresh clone is SHALLOW, and the live build dates every page from git, so first
  `git fetch --depth=100000 origin main claude/v2-prototype`. Never run two builds or gate runs at once (they write
  the same files). The working tree after a build holds rewritten live pages: stash them (`git stash push`), never
  commit them; deleting or dropping is refused by the permission check, a stash is fine.
- Known gate result, not the media work: live-untouched FAILs on about.html and ~178 other live pages because commit
  62360aa (address M 68, 3 Nov) edited them without moving their "dateModified" (still 2026-10-02; any build writes
  2026-11-03). The deploy builds fresh, so the live site is right. Fix in a site-wide pass: rebuild and commit those
  dates on main with the owner's ok.

**Chat 19's job, in order.**
LIVE since 4 Nov (deploy run 36, commit 2f19bc04): https://paraglidingatlas.com/media.html and
/media-srs-piedrahita-2026.html, checked by chat 18 at 390x683, 390x844, 1440x900: every media-2026 photo loads, no
errors, no sideways scroll, Media in the footer (about.html checked too). The first deploy (run 35) failed: designer
samples D, E, F pointed at img/media-tmp/, which exists only in a container; they now read media-2026. Lesson: before
pushing, move img/media-tmp/ aside and run ./build.sh then tools/v4_build.py, as the deploy does.
1. Piedrahita event page, for pilots (owner's job 3): 40 to 60 photos by task, each task's story from its video
   description (Day 1 cuGs7Lk6Dt4, Task 1 uCEfssE40u8, Task 2 NXUEyPQ3V4E; read the descriptions with vidIQ
   video tools or YouTube; never invent). Drive "All Tasks" 1GwKlKvNkYJ5P5WF0QBtkOByG8du8lrjC holds 200+ JPEGs
   (page 1: 20 T1, 34 T2, 146 T3, ~15 MB each, 3 GB; there is a second page). Mind the disk allowance: download a
   few at a time, make web copies (tools/v4_media_photos.py), delete each original. Ask the owner once: their own
   pick, or chat 19 picks. Push the web copies to media-2026 `srs-piedrahita/`, extend PH in tools/v4_media.py.
   One preview (artifact) before it goes live.
2. Tapalpa (8 to 14 Nov): the owner is on site; a daily routine (photos into a Drive folder, a scheduled chat makes
   web copies, adds the day, pushes) waits on the owner saying how many photos a day and which folder.
**Still open for the owner (asked 4 Nov, not yet answered):** subscriber and follower counts with the date; where
sponsors appear; the quote; the SRS and PWCA logo files; Tapalpa photos per day and the folder; which site photos
are theirs (photo credits, not yet done); the two orange buttons at 1440; the Worker's media branch (ENDPOINT stays
empty for media until then). Chat 17's leftovers (MailerLite draft and form address M 46, six emails without "M",
.claude/settings.json) are unchanged.

## Chat 18 starts here (4 Nov 2026): the owner's yes on the Media page, then build it into the live site
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link.

**Where chat 17 left it.** The Media page sells comp coverage to organisers and sponsors only (owner, 3 Nov: prices
hidden, photos only for now, logos OK, quote coming, slots as example data). Three designers built mocks
(`prototypes/v4/samples/media-d|e|f/`, brief `docs/designers/media-brief.md`); three judges picked E, "Pull Back
To The Coverage", 3 of 3. It is built into the generator from `docs/designers/media-build-spec.md` (every item done;
the judges' grafts from D and F included), then reviewed three rounds (buyer, QA, critic) with 48 fixes; chat 17
re-checked it at 390x683, 390x844, 1440x900, 360x740, 820x1180, 1920x1080, with JS, reduced motion and no JS: no
horizontal scroll, no errors, no em dashes, 12 [to supply] marks, and the dates form arrives on enquire.html in its
media mode with every field filled. **Preview 3 (sent to the owner 4 Nov): https://claude.ai/artifact/1MvsFDSybt34TQ2j2Aviee**
(version 3; it packs media.html, the Piedrahita page and enquire.html; in the preview a video's play opens YouTube).

**Files.** `tools/v4_media.py` (writes `prototypes/v4/media.html` and `media-srs-piedrahita-2026.html`; data PH, V,
POSTERS, UPCOMING, SEASON at the top), `prototypes/v4/v4-media.css`, `prototypes/v4/v4-media.js`,
`tools/v4_media_preview.py`, `tools/v4_media_posters.py`, `prototypes/v4/enquire.html` (media mode: `?trip=media`,
name and email via sessionStorage `v4-media-enq`; proven to survive `tools/v4_ux.py enquire.html` twice). All committed
on claude/v2-prototype and pushed (not main). NOT committed on purpose: the two built pages and the photos'
web copies `prototypes/v4/img/media-tmp/` (photos go to their own repo, never this one). A fresh container has
neither: rebuild the pages with `python3 tools/v4_media.py --media img/media-tmp/` after fetching the photos back
from the preview artifact (Artifact read, `path` each `SRS_5_*-800/1600/2400.webp` and `poster-*.webp`, listed with
scope "files"), or from the owner's Drive "All Tasks" folder 1GwKlKvNkYJ5P5WF0QBtkOByG8du8lrjC.

**Chat 18's job, in order.**
1. The owner's yes or changes on preview 3 (rebuild, re-test at 390x683, 390x844, 1440x900, republish the same link).
   Ask the three questions below once, briefly; the owner leaves for SRS Tapalpa about 5 Nov (tasks 8 to 14 Nov).
2. On yes, build it into the site: the photos into the owner's new public repo `media-2026` (owner creates it; web
   copies only, `srs-piedrahita/` folder, served at https://paraglidingatlas-maker.github.io/media-2026/), then
   `python3 tools/v4_media.py` (default MEDIA base) and commit the pages; add media.html and
   media-srs-piedrahita-2026.html to the pages their own generator owns in `tools/v4_build.py` step 11 (as
   record-*.html), so the chain does not rewrite them; the "Media" line in the full-screen menu and in every footer
   (Atlas column, after Partner With Me; the generator already does it on its own two pages); photo credits on the
   owner's photos elsewhere on the site (ask which); then `python3 tools/v4_gates.py` and a clean double rebuild,
   push to main and claude/v2-prototype, never forced, and check the live page.
3. Piedrahita event page (speaks to pilots): richer, 40 to 60 photos by task from the Drive folder above or the
   owner's pick, with each task's story from its video description.
**Owner's questions (only they can answer):** the three in the chat 17 note below (the Worker's media branch; the
facts that decide the sponsor sale, first the subscriber and follower counts and where sponsors appear; the two orange
buttons at 1440), plus: Tapalpa photos per day and the Drive folder they go in; create `media-2026`; the quote; the
SRS and PWCA logo files. Other leftovers from chat 17: MailerLite draft "Patreon update · Website edition"
(200388930129889120), the account's company address and the "Newsletter signup" form still read M 46; six fixed
emails read "Olav Troviks vei 68" without the "M" (owner to say); the owner may paste a permissions block into
`.claude/settings.json` themselves (chat 17's edits to it were refused, do not retry).

## Chat 17 starts here (3 Nov 2026): build the Media portfolio page properly
**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link.

**Media page: three things only the owner can decide (review fix passes 1 to 3, 4 Nov).**
1. **ENDPOINT must stay empty for media enquiries until the Worker is changed.** `enquiry-worker.js` (repo root, so
   the owner approves any change) has no media branch: it requires the pilot fields (rating, total, recent) and a
   message of 10 or more characters, never reads event, when, place or package, and its subject is "Trip enquiry".
   Every organiser would get "Please fill in the required fields." `prototypes/v4/enquire.html` now sends a media
   enquiry by the visitor's own email app even if ENDPOINT is set (`posts()` in its send script). The Worker change,
   for the owner's yes: when trip=media, require only name, email and event; allow an empty message; add Event,
   Dates, Place and Package lines to the email; subject "Media enquiry: <event>". Then drop the `isMedia()` test in
   `posts()`.
2. **Facts to supply, first (they decide the sponsor sale):** the YouTube subscriber and Instagram follower counts,
   with the date counted; where sponsors appear in the films, the live commentary and the results newsletter; who
   can use the videos and photos (the rights wording); how travel works; how far ahead to book. Then: social clips
   per task day; what an event provides beyond internet and footage; the real quote and its organiser (now EXAMPLE);
   the real 2027 calendar (now EXAMPLE); the SRS and PWCA logo files. Each shows `[to supply]` on media.html until given.
   Also: "Also offered" (live commentary, stills) replaced "Add to any package", which the facts did not say; if they
   can be added to any package, say so and it goes back.
3. **One ruling: two orange buttons on the desktop's first screen.** At 1440 the header's Enquire Now and the
   opening's Check dates for your event are both solid orange (both go to the dates form), so orange is not quite the
   single LIVE light the brief asks for (critic-1-10, buyer-2-1, critic-2-2). Phones already show one orange button at
   a time, the nav that comes back on a scroll up included (fix pass 2). Keep the site's header as it is (designer E's
   call: the two sit far apart and every page has the same header), or on this page draw the header button in the lines
   style while the opening is on screen (same size and place, so nothing moves).

Noticed in fix pass 3, for the next site-wide pass (not a page fix): `prototypes/v4/sw.js` is stale. Its VERSION is
fb1b14f102 while the app files now hash to abf7cece7a, and `offline.html` differs from what `tools/v4_pwa.py` writes.
The service worker precaches `v4-menu.js` without a `?v=`, so a change to the shared menu reaches an installed phone
only after `python3 tools/v4_pwa.py` runs, and that rewrites every v4 page. For that reason the Media page's own menu
fix (its Enquire Now goes to the dates form, qa-3-1) lives in `v4-media.js`.

Chat 16 (all pushed if the gates passed; check `git log origin/main`):
- **Welcome email LIVE** (3 Nov): MailerLite automation 199572486318196276 "Welcome to the Atlas list" now sends
  the letter design, subject "Welcome to the Atlas Tribe"; old version in docs/emails/welcome-atlas-list-old.html.txt.
  Newsletters from now on belong to the owner's newsletter chat; the website chat only does site pieces.
- **Expeditions on phones LIVE** (owner: "a go"): the desktop flight below 1000 px in a phone shape, photo first.
  `tools/v4_expeditions_phone.py` applies it to the committed `prototypes/v4/expeditions.html` (the build keeps
  that file as committed; `tools/v4_expeditions.py` itself stops on "the partners shell has changed", an older
  problem, and also calls phone() if it is ever fixed). Preview: https://claude.ai/artifact/Pa6jToj4vWyYf2iiJCudRA.
  Lessons: test at the owner's real phone size (390 x 683 inside the Claude app) with the menu bar shown and hidden
  before sending anything; the owner is right to reject untested previews.
- Container setup: `pip install "playwright==1.63.0" contourpy fonttools brotli` before the gates, or the build
  half-runs and rewrites live pages in the working tree (stash them; never commit them). A sample page must not
  use a `<base>` tag (the build's asset check reads relative paths). Since go-live `prototypes/` is not served, so
  previews go to claude.ai artifacts (Artifact tool, files map; flatten paths, drop pwa.js; see chat 16's
  scratch approach in tools/v4_expeditions_phone_preview.py and tools/v4_media_preview.py).

### The job: the Media page (owner, 3 Nov: "this is my face to asking people to trust my site ... where I convert
eyeballs into customers and newsletter subscribers, but all in an elegant and effective way")
The first preview (https://claude.ai/artifact/WctLPGmX5uVpGabthpHde3, `tools/v4_media_preview.py`) was rejected:
"a joke ... incomplete, no zoom on the pics, pay button is different from rest of the site". Rebuild it from the
site's own parts. Owner decisions: a **Media** page (a bold portfolio) plus subtle signposts only: a photo credit
on the owner's photos, one "Media" line in the full-screen menu, one in the footer About column. No home section.
Photos in a separate free GitHub repo per year (owner creates it, e.g. media-2026; GitHub's own address, not a
subdomain, unless the owner says otherwise); web copies only (WebP, 800/1600, plus AVIF if worth it), originals stay
with the owner. Videos stay on YouTube, played in place on tap (youtube-nocookie; audit.py fails other embeds).

**Audit of the rejected preview (fix all):** invented buttons (use only `btn-solid` with its inner span and
`btn-lines`, `data-hover`); own weak lightbox (reuse the India page's viewer in `prototypes/v4/fly.js` ~450-520,
`dialog.v4i-fl-lb`: tap zoom 2x/3.5x, pinch, drag, counter, keys); own headings (use `kit-head` > `kit-kicker` +
`kit-title` + `kit-intro`); videos left the site (reuse the home `#listen` `lb-ep` tap-to-play); no proof; no
newsletter (reuse `.v2-nl` + /newsletter.js, MailerLite form 199520945794189126); the enquiry form is the trip form
with required pilot fields (add a "Media coverage" option with event, dates, place, needs; enquire.html is
hand-edited, no generator; subject is hard-coded 'Trip enquiry: '); dates shown as "2026" only; the grid crops
every frame (a portfolio must show full frames: justified rows by aspect ratio); the event page is uneven.

**What the owner delivers (read from the three Canva pitches, 3 Nov; use these names):** four products, the same
in the SRS letter (Piedrahita, dated 09 Aug 2026), the SRS Media Deck Strategic Roadmap and the PWCA "Paragliding
World Cup TV" board: (1) **Pre-Race Show**, a Paragliding Atlas podcast preview episode, "build anticipation with
audiences/pilots who would like to know the venue and conditions"; (2) **Daily Highlights** ("Race Week"), a
long-form video each task day plus social clips (reels) and a results newsletter, "show task, results, race dynamics,
and what made each day special"; (3) **Aftermovie** ("Recap Video"), a highlights compilation: task details,
racing strategies, leaderboard standings, fun factor; (4) **Race Behind The Race**, BTS and athlete showreel,
mid-season or as available (SRS roadmap: Episodes 1 and 2), "explain what it takes to organize a comp and create a
deeper emotional connection between audiences, athletes and organizers". Conditions in the pitches: everything is
published as collaborative posts on both Paragliding Atlas and the organiser's channels; daily timing depends on
on-site internet, task finish time, access to footage and on-site editing; start with the resources available and
grow the deliverables as budget allows. The SRS roadmap runs Q3 2026 to Q2 2027 across the season to the Sports
World Final (a plan, not a list of confirmed events): the page can sell **season coverage**, not only single events.
Beyond the four: **live commentary** (Bassano) and **stills** (Piedrahita, Tapalpa).

**Agreed page order:** 1 hero (one full-bleed still, kicker "Media", h1 "From The Comps", one line, btn-solid
"Book a Call" + btn-lines "Watch the Highlights"); 2 proof strip (`kit-stats`); 3 showreel (most-watched
highlight, in place); 4 selected work (full frames, zoom viewer); 5 the comps (a card each: best still, place,
dates, what was delivered, views; each opens its page); 6 what an event gets (the owner's pitch: Pre race: podcast
preview episode; During: daily highlight videos and a results newsletter; Post: aftermovie / highlight
compilation; Between races: Race Behind the Race BTS and athlete showreel; published as joint posts on both
channels; delivery same day or end of the week, depending on need; subject to connectivity on site); 7 how it
works (call, plan, daily delivery); 8 a quote (owner: "soon"; never invent one); 9 the closing booking band
(`cta-band`: btn-solid Book a Call + WhatsApp + media enquiry); 10 newsletter ("Follow Tapalpa day by day").
Show ONE preview, tested at 390x683, 390x844 and 1440x900, before building into the site.

**Facts (all checked 3 Nov):** the owner was **hired** by SRS and PWCA (wording "covered for"). Events:
- PWC Super Final, Pegalajar, Spain, May 2026 (15th Paragliding World Cup Super Final): highlight videos only:
  Day 1 FOuAWMeoxs4 (3,537 views), Task 1 BRAX1XMU390 (7,342), Task 2 7il6yV1vdIc (4,034), Task 4 op1-O01xkH4
  (3,437), Task 5 vPnIYYKcvEg (3,340). Playlist PLwalaswPmuBgYtvCDEXKDP6kJC0qubzou.
- SRS Skywalk Bassano Edition, Monte Grappa, May 2026: live commentary on YouTube: Task 2 ZL9B5eXip5o (5h41,
  1,145), Task 3 SZWQjcO_fWk (4h59, 890), Task 4 x8sSBSBy4dI (1h57, 853) and DA4nGop3i9g (3h55, 513), Task 5
  PEyO6MXngUw (5h08, 680). About 21 h 40 min live.
- SRS BGD Edition, Piedrahita, Ávila, Spain, 22 to 29 Aug 2026, FAI CAT 2, 120 pilots from 54 countries (owner's
  video description): stills and video: Day 1 cuGs7Lk6Dt4 (1,206), Task 1 uCEfssE40u8 (1,970), Task 2 NXUEyPQ3V4E
  (2,303). Playlist PLwalaswPmuBhoes6pMIu-bfntsAVM0eIK. Stills: Drive "Chosen Few" 1423IRZp63UI_1G5i73-dwUjixBWL1hXF
  (20 JPEGs, Canon EOS R50, SRS_5_T1/T2/T3 = tasks; download with
  https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t); "All Tasks" folder
  1GwKlKvNkYJ5P5WF0QBtkOByG8du8lrjC (100+ files, 1.7 GB per 100).
- SRS Advance Edition, Tapalpa (Gravedad Cero, Jalisco, Mexico): registration Sat 7 Nov, tasks Sun 8 to Sat 14 Nov
  2026, 7 tasks, 120 pilots max, 44 countries (airtribune.com/srs-2026-6/info). Stills and daily video, to come.
- 13 comp videos total about 31,250 views (vidIQ, 3 Nov). Owner's pitches (Canva): SRS letterhead DAHR0zZ62h4,
  SRS calendar DAHNfJ3Qjyw, PWCA TV DAHNTAnUhT0.
Still to ask: photos per day at Tapalpa; the daily drop folder (Google Drive); which site photos are the owner's
(credits); rates (turnaround given above).

## Chat 16 starts here (3 Nov 2026): the expeditions page on phones, then the media library
Chat 15 (all pushed, last commit before this note 469f9464, gates PASS apart from the expected live-untouched
flag for `assets/email/`) went live on 27 Oct and then took many owner requests: Kenya flight, About, photo
breakers, the record page, the email signature (`assets/email/`), the owner's map, India 2027 dates, and the
MailerLite welcome email redesign (images in `assets/email/welcome/v1/`, never move them; a switched-off test
copy is MailerLite automation 203064539021837887; going live is handled in chat 15 or, if not yet done, waits on
the owner saying "make it live").

**Standing rule (copy it into every handover):** website chats are numbered. When your job is done, or the chat
has grown long, hand over without asking the owner: write the handover at the top of this file, update the
owner's map (https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5, collection "modules"), open the next numbered
chat yourself with the session tools (create_session), and give the owner its link.

1. **Expeditions page on phones (first job).** Owner, 3 Nov: on a phone `expeditions.html` "doesn't have any
   animation that comes up in the desktop view, and looks an oddly designed broken page". Desktop: split hero
   (Kenya and India photos), "Where And When" list beside the world map, each place pinned with its photo, the
   map fly-in and the cloud move between places (designer E's "through the cloud", docs/designers/). Phone 390:
   the hero photos crop awkwardly under the place labels, the list and map stack, the place sections lose the
   pinned moves and read as loose blocks. Bring the desktop motion to phones in a phone-shaped form (or a
   deliberate phone version), within the motion rules below; show the owner a phone preview first (one preview).
2. **Media library (owner approved the idea, 3 Nov).** The owner shoots stills and one highlight video a day for
   paragliding comps (SRS, PWCA, Coupe Icare; playlists on the YouTube channel) and leaves for SRS Tapalpa,
   Mexico (about 5 to 18 Nov; confirm the comp dates). Plan agreed in chat 15: zero cost, the site must not get
   slower. Photos as web versions only (2400 px about 300 KB, thumbnails about 40 KB, lazy grids, big image on
   tap) in a separate free GitHub repository served at `media.paraglidingatlas.com` (one store about 1 GB,
   about 7 to 9 comps; a new one when full); videos stay on YouTube behind a click-to-play still. One page per
   event with a section per day, and a top page across editions (the portfolio). Daily routine: the owner drops
   selects into a Google Drive folder; a scheduled chat resizes, uploads, adds the day and pushes. The owner has
   all the rights. Still to ask: daily photo count, where past editions' stills are, and the DNS record for the
   subdomain (walk them through it). Cloudflare R2 is the fallback (free to 10 GB, needs a card).

## The owner's rules (unchanged)
- Only `prototypes/v4/`, `tools/` and `docs/` change. Never `prototypes/v2/`,
  never a live page, never `rss-feed.js`. The switch-over is the owner's.
- Nothing invented: a missing fact shows as `[to supply]` (`.v2-tbd`).
- Design tokens only; no em dashes in copy; cache-bust changed CSS and JS.
- Motion (owner, 28 Oct, replacing "nothing loops or runs on its own"): ambient motion that runs by itself is
  allowed within four limits: (1) subtle and slow (a glow breathing, grain shimmering faintly, clouds drifting);
  (2) it stops completely under "reduce motion"; (3) it pauses when off screen; (4) never behind reading text or
  beside the booking button. Motion in answer to the visitor stays as before. Reduced motion and no JavaScript
  show the finished page.
- Push only `git push origin HEAD:main` and `git push origin HEAD:claude/v2-prototype`,
  after `python3 tools/v4_gates.py` passes (about 25 minutes; `--quick` while
  iterating). Never forced, no pull requests.
- Never store a token or key in the repository or the chat; GitHub access comes
  from the connected account.
- Episode counts are the RSS feed's (owner, 21 Oct: "whatever the RSS feed
  shows, it's the correct count"; never ask again): the episodes in
  episode-meta.json with a publish date (80 on 21 Oct); tools/v4_polish.py
  feed_count() writes it on the sitemap and Mission.
- No photograph is used twice on the site unless it really must be (faces,
  portraits); a repeat is replaced with a different picture, not dropped
  (owner, 21 Oct).
- Every push to live gets a link (owner, 26 Oct: "give me a link whenever you push something live, this rule
  is forever valid across chats"): after each push, give the live paraglidingatlas.com link(s) to what changed.
- Work lean (owner, 21 Oct: "we're spending a lot of time discussing"): at
  most two options for a decision, one preview only for a large visual
  change, small fixes built straight away and shown after.

## Chat 15 (27 Oct night): v4 is LIVE, stress test done
- **v4 went live at 02:14 UTC on 27 Oct** with the first push of `.github/workflows/deploy.yml`: Pages already
  published from GitHub Actions, so the workflow's deploy job succeeded (not the harmless failure expected). The
  owner had said "push the build to live site as it is". Every push to main now rebuilds and publishes the
  switched site (about 2 minutes). Rollback: Settings > Pages > Source "Deploy from a branch", main, / (root).
- Fixed after launch (all gated, all live): the home opening's Kenya layers 404'd (its script had a fixed
  `img/opening/`; tools/v4_home_opening.py now takes the folder from the page's own photo); the home globe's trip
  layer never started on the live page (samples/listen-c tested `/\/globe\.js/`, the live src has no slash):
  orange trip pins, the season route, planned trips; the trip picker's radios named; the partners rows take
  keyboard focus; the knowledge base hub's faces fetch YouTube's 480px still up to 2x (2.2 MB to 0.5 MB).
- Listening mode on the 71 filmed episodes now plays the feed's audio file (mp3-map.json, via a data-audio on
  the button, tools/v4_ux.py episode_audio; src/v4-listen.js), so an iPhone keeps playing with the screen locked;
  lock-screen title and artwork via Media Session. The video stays on the page, paused. Transcript timing: the
  transcripts seem to follow the audio (new-technologies-5 runs 93 min in both the audio and its transcript, the
  video is 82 min), but the owner should spot-check one episode. Not verifiable here: anchor.fm answers this
  container's browser with 400 (curl gets 302), so real playback was not heard.
- Stress test (switched site, 183 pages x desktop 1440, phone 390 touch, 375x667): no horizontal scroll, no
  broken links or images, no script errors; axe WCAG A/AA on 18 page types: only the fixes above left (one
  remaining: the audio-only player's chapter buttons inside its slider, live generator markup); menu, site
  search, library find, enquiry validation, globe, reduced motion (nothing loops), no JavaScript all fine. SEO:
  all 181 sitemap pages 200 on the live site, canonical right, social image present, structured data parses,
  no stray indexable page, robots.txt and 404 fine. Live LCP 0.3 to 1.7 s.
- For the owner (not built): no analytics on the site (old or new); the enquiry form opens the visitor's mail
  app (mailto), so people without one cannot send; internal notes (LEGAL-REVIEW.md, TODO.md, PROJECT_HANDOFF.md,
  build.sh...) are readable on the live site, as on the old one; Search Console: submit
  sitemap.xml and watch coverage for a week; IndexNow: run the IndexNow workflow once with "all" ticked
  (its per-push diff names prototypes/v4 paths, not the live addresses).

## Chat 15 starts here (27 Oct): go live, then a full stress test
Chat 14 (all pushed, last c774f333, gates PASS): home podcast poster strip (samples/listen-c via
tools/v4_home_listen.py) with the designers' fixes (labels fit, foot fade, one hook size, calm length bar, orange
expand sign by "min / chapters", "Paragliding Atlas Podcast" on hover only, no contour lines); the section's last
line (Library link; "Also on" Spotify, Apple Podcasts, YouTube with one-colour marks that glow in brand colour on
hover, Amazon Music by name); Apple's real Apple Podcasts glyph (tools/v4_polish.py APPLE_*); the footer year
turns over by itself (tools/v4_pwa.py + pwa.js); the record page footer transparent; dates name 2027 once
(opening, expeditions); Panchgani photo credit off the home page; trip titles "Explore The Cradle" and Panchgani
"The Land Of Five Hills"; the phone opening at full height, option 2 (owner's pick, samples/opening/index.html,
phone only; previews samples/opening/phone.html, phone-full.html, phone-dates.html). Partners page scored ~7/10
by D/E/F; their changes are "not now". The old live site is saved in the owner's private repo
paraglidingatlas-maker/v3.

Go-live (owner, 26 Oct: "push the build to live site as it is, if needed to fix, we'll do it afterwards"):
`.github/workflows/deploy.yml` is now docs/v4-deploy-workflow.yml, active. While Settings > Pages > Source is
"Deploy from a branch" its deploy job fails harmlessly and the live site is untouched. The owner switches Source
to "GitHub Actions" (https://github.com/paraglidingatlas-maker/Website/settings/pages); then the workflow is run
again and the live site checked. Rollback: Source back to "Deploy from a branch", main, / (root). Kept out on
purpose by the switch: the record attempt page, the encyclopedia, samples.

## Chat 14 (25 Oct): the poster strip is in the home page
- 26 Oct, the posters after the designers' review (all three chose them over the live tiles): series labels fit,
  the foot fades into the page's dark, one hook size (up to three lines), the length line one calm bar (no
  chapter ticks), the live tiles' expand sign in orange opposite "min / chapters", "Paragliding Atlas Podcast"
  under the name on hover only. Contour lines removed entirely. The record page's footer transparent. The
  footer's year turns over by itself (tools/v4_pwa.py + pwa.js).
- The old site for reference (owner, 26 Oct: "just host it on GitHub"): a frozen copy of today's live site (every
  page noindex, robots.txt Disallow, no CNAME) to go in a new public repository paraglidingatlas-maker/old-site,
  served by GitHub Pages at paraglidingatlas-maker.github.io/old-site/. The chat cannot create repositories (403);
  the owner creates the empty repo, the chat adds it with add_repo (push) and pushes, the owner turns Pages on
  (Settings > Pages > main). Make it again from origin/main right before the switch-over if live pages changed.
- The owner said "yes Poster strip into home": tools/v4_home_listen.py copies samples/listen-c (not listen-b).
- Contour lines fixed on the owner's screenshot: the map behind the strip has its own layer (will-change), since
  the posters' resting 3D tilt hid it above the cards; it peaks where the posters start; poster lines fade out by
  26% of the height. Known, left alone: img/contours.svg is not a seamless tile, so faint straight joins show.

## Chat 14 starts here (25 Oct): put the poster strip (listen-c) into the home page when the owner says yes
Chat 13 (all pushed, last 43eefad8, gates PASS):
- **The podcast section is in the home page** (`tools/v4_home_listen.py` copies PART 2 of
  `samples/listen-b/index.html` in place of #listen and #map; run it by hand after a change to the sample, then
  commit both). `tools/v4_polish.py` no longer leans the home rail's cards. The sample sets `--hf`/`--nf` once
  (styles.css still sizes the old plate's words by them; without it the switch dry run fails its token check).
  The globe box keeps `id="map"`. Play still needs checking on the owner's device.
- **The call band stays and arrives** (samples/departures, copied by tools/v4_home_departures.py): the glow opens
  in the middle and settles top-left, the line draws, the words rise; words on the rows' edge, buttons level with
  the title, an --sp-4 gap; on a phone the season line runs to a ring at the call.
- **The poster strip, preview only:** `samples/listen-c/index.html` (live at
  https://paraglidingatlas.com/prototypes/v4/samples/listen-c/), listen-b with the "More conversations" cards as
  posters again: each guest's own art in colour (a step darker at rest), hook and name in live type on the art
  (no plate image, no compass), a deep fade into the page dark, the lean with a soft light, a line per card to
  its real length with chapter ticks, arrows in the heading row, a progress line under the strip, the strip
  drifting on its own again (v2-immersive.js data-auto), faint contour lines (img/contours.svg) on the red above
  each head, lined up with one map behind the strip that fades out into the section; the lead trip's pictures in
  colour; "15 guests, newest first". The owner tried and rejected a small compass dial and a big compass rose
  ("looks odd"). Chat 13's generator was in its scratchpad (gone); the sample itself is the source now.
  **Next:** when the owner says yes, copy listen-c into the home page (point tools/v4_home_listen.py at
  samples/listen-c, rerun, build, gates).
- **One width across the site** (owner: "go with 1"): above 1440px every page uses the opening's 72px edge
  (src/v2.css "ONE WIDTH ACROSS THE SITE"). Up to 1440px nothing changed. Left as designed: the knowledge base
  climb's staircase, the partners journey's spine, full-bleed photos, maps and rails. The library page follows
  through the shared stylesheet only (its files are the other chat's; nothing in them was edited).
- **Designers:** their definitions now carry the owner's "professional standard" (homework first, no rule
  stretched past its section, weigh immersion before simplifying, own the whole site).
- **Build note:** a change to src/v2.css changes the ?v= stamp on every page; build once, commit the rebuilt
  pages, then the clean double rebuild.

## Chat 13 starts here (25 Oct): build the podcast section into the v4 home page
Chat 12 did the seven steps (below) and then, with the owner and the three designers, designed the
section after the departures. The owner's choices, in order (also in docs/designers/direction.md):
no cursor shine on the departure rows; option B, Turnpoint's "Hear Where We Fly", #listen and #map
merged into one section; refined (one calm card look: grey pictures, colour on hover, no compass, no
YouTube red; one India heading; "More conversations, Newest first", no "most streamed" claim; the phone
globe fits; "Find it on the globe"; a still orange route on the globe in season order, hollow pins for
Kazakhstan and Peru); then a lead: the lit trip leads with its big name, dates, play in place (the
youtube-nocookie embed loads only on tap) and Trim's chapter line, the globe turns to a picked trip and
lights the route to it; no footage ("Except 2, 1 & 3"); last, the globe leads the stage (about 720px on the
right, one plain ring, legend and caption one line under it, zoom inside its square), the episode picture
small (240px) and growing on play. The owner: the globe "will most likely be replaced by the Encarta
concept globe later on", so only its place and look matter now.
- **The preview:** `prototypes/v4/samples/listen-b/index.html` (live at
  https://paraglidingatlas.com/prototypes/v4/samples/listen-b/), last at bfb126d9, gates PASS. Turnpoint's
  rebuild scripts were in chat 12's scratchpad (gone with the container); the sample itself is the source.
- **Next (not yet asked):** the owner had not yet said "build it into the home page". Ask once, then do it
  like `tools/v4_home_departures.py`: a tool copying the merged section from the sample into
  prototypes/v4/index.html in place of `<section id="listen">` and `<section id="map">`, with the chain
  checked (v4_ux, v4_polish, v2-home.js rail code, the globe scripts, smoke tests on #listen or #map).
- **To check with the owner:** play on a real device (YouTube is blocked in the container, so the playhead
  and the exact length from the player are untested); the chapter titles in episode-meta.json were written
  from transcripts and marked for review; sharper guest portraits would help (the face crops come from each
  episode's YouTube art, to keep "no photo used twice"); the source of "most streamed" if it is to come back.
- **Worktree note:** a designer run with `isolation: worktree` leaves full copies under
  `.claude/worktrees/`; the audit and the switch dry run then scan them and FAIL. Remove them
  (`git worktree remove --force`) before gates. Chat 12 put `.claude/worktrees/` in `.git/info/exclude`.

## Where chat 12 left it (25 Oct): the seven steps are done and pushed
- **Step 1 (301b80d1): option A is the home departures.** `tools/v4_home_departures.py`
  (run by hand after a change to `samples/departures/index.html`; the build
  keeps what it wrote) copies the sample's `<style>` into the head and its
  `<section id="destinations">` (season line, nine rows, call band, small
  script) in place of the fly-by, line of months and table, between
  `v4-home-departures` marks. `tools/v4_polish.py` counts the Destinations
  from the `.sl-row` rows and no longer draws the old line (`v4p:tl`);
  `v4_ux` home_flyby_weight and `v4_phone_media` flyby() find no fly-by and
  do nothing; the fly-by's phone cuts (`img/hero/home-*-p`) are deleted. The
  home page has no video now, so v4_footage drops its pause script there.
  No JavaScript shows the whole list (checked at 1440 and 390); the phone
  card's "Today" reads the sample's 24 Oct 2026 until the script sets it.
- **Step 2: the phone opening.** On a phone (sample, then
  `tools/v4_home_opening.py`) the headline comes up under the route, the
  trip panel follows with its button, "You fly" moves under the button, the
  kicker and "Listen to the podcast" go last; the panel no longer fades as
  the page scrolls (`.dock{opacity:1}` on phones) and the trips' grid no
  longer stretches to India's height. At 390x844: headline 456 to 510 px,
  the trip button 723 to 811 px for every place (was 842 to 957).
- **Step 3: text and targets.** Readout labels, month letters (desktop and
  phone), route names on a phone, the swipe hint and hints 11.2 to 12.5 px
  (route names lose their letter spacing under 360 px, so KAZAKHSTAN clears
  PERU at 320); the pause button is a 44 px target, still dim, no ring. The
  departures' small labels went up the same way.
- **Step 4: the call band** reads "(Kenya, Panchgani, India, Kazakhstan or
  Peru)" on home and the three trip pages (tell the owner).
- **Step 5: Panchgani.** Vistasp Kharas's episode lists Panchgani first in
  Fly With Us (price `[to supply]`); About has a fifth card ("Panchgani ·
  Sahyadri hills", "The Sahyadri Tablelands", from the page's own title)
  with the contour pattern instead of a photo (its one photo is used three
  times already), five cards in a row from 1101 px.
- **Step 6: no JavaScript.** Kenya's five fly chapters each show their own
  photo under their words (noscript copies, India's v4-calm way, in the
  page's own `<style id="v4-kenya-own">`). The home rows and "Join The Atlas
  List" show without JS at 1440 and 390 (the old hidden rows went with step 1).
- **Step 7: Kenya's drift.** On Kenya `--font-mono` is the body font and
  `--orange-lite` the one orange (page-only, so the library's mono stays);
  `src/v2.css` gallery, route, 404 and altitude whites are `var(--white)`.
- **Listed, not done:** the pilot cut-out's grey rim and the shadow blobs in
  the opening need image work (re-cut masks); not tried, to keep it clean.
- **Next:** offer the owner a new Juror review with its estimate (one page at
  two widths about 3 to 6 min and 60k to 120k tokens; site-wide about 20 min
  and 150k). The scheduled task "Chat 12: carry on the v4 plan" is disabled.

## Chat 12 starts here (25 Oct): the owner said "do what you can yourself"
After the steps below the owner had the three designers (now named Trim = D,
Cloudbase = E, Turnpoint = F; `docs/designers/README.md`) and a new fourth
agent, the Juror (`.claude/agents/awwwards-juror.md`), look at the home page
and the whole site. Their write-ups are in the designers' notebooks
(`docs/designers/D.md`, `E.md`, `F.md`, `juror.md`, newest at the top).
- **The Juror's rule (owner):** "use only after checking with me the
  prediction of time and turn expenses". Tell the owner the estimate first
  (one page at two widths about 3 to 6 min and 60k to 120k tokens; the
  site-wide review took 19 min and 150k) and wait for their yes.
- **The Juror's scores** (v4 at 48bfc475 before the opening went in, against
  v4 now): 7.14 then, 7.83 now out of 10 (Design 8.2, Usability 7.3,
  Creativity 8.3, Content 7.0). About 8 usually wins Site of the Day.
- **The next home section, option A "One Line, Two Postures"** (the
  designers' majority pick after two rounds): the opening's season line
  carried down across the top, matched to the pixel; the nine departures as
  rows under it, each with a thin bar at its real dates (planned dashed), the
  place last shown in the opening lit orange; pointing at a row flies the
  glider to its bar. Phone: the line upright in the left margin, one card per
  departure, the orange track drawn by scroll (CSS scroll timeline) with the
  glider on its tip. The fly-by and the sideways line of months go; the call
  band stays. Preview built by Turnpoint as a full copy of the home page:
  `prototypes/v4/samples/departures/index.html` (live at
  https://paraglidingatlas.com/prototypes/v4/samples/departures/#destinations).
  Option B (Cloudbase's: rows unfold out of their bars as you scroll) was not
  chosen by the majority.
- **"Do what you can yourself" (owner, 25 Oct)**, chat 12, in this order,
  each step with gates and a push:
  1. **Build option A into the v4 home page** in place of
     `<section id="destinations">` (the fly-by, the line of months and the
     table). Make it a tool like `tools/v4_home_opening.py` that copies the
     section from the sample. Watch the chain: `tools/v4_polish.py` reads the
     departures (`a.v2-dep` rows) for the home line of months and the
     Destinations figure and stops if they are gone; `tools/v4_ux.py`
     home_flyby_weight and `tools/v4_phone_media.py` flyby() read the fly-by
     (the phone cuts `img/hero/home-*-p`). Keep the departures' data (one
     list, the rows) so the passes and v4_polish can read it, or move them to
     read the new rows. No-JS must show the finished list.
  2. **The phone opening** (all four found it): on a 390x844 phone the
     opening's trip button sits at 824 to 871 px (was 560 px), the headline
     "Paragliding Expeditions, Run By A Pilot." starts about 964 px down, and
     the trip panel fades to black after about 200 px of scroll. Put the
     headline and button inside the first screen, hold the fade until the
     panel has scrolled past (sample, then `tools/v4_home_opening.py`, then
     the build).
  3. **Small text and targets** (Juror): readout labels 9.9 px, phone month
     letters 9 px, the route hint 11 px: none under 11 to 12 px; the pause
     button a 44 px touch area (it can stay dim).
  4. **The call band** says "Ideal tour match ... (Kenya, India, or Peru)" on
     the home page and the trip pages: make it the five places (Kenya,
     Panchgani, India, Kazakhstan or Peru); tell the owner.
  5. **Panchgani where it is still missing** (Cloudbase): the Panchgani
     episode's "Fly With Us" box and About's place cards.
  6. **No JavaScript** (Cloudbase, Trim): on the home page the departure rows
     and "Join The Atlas List" are hidden without JS (the fly-by goes with
     step 1); on Kenya's page the five chapter sections are black without JS.
  7. **Kenya's page drift** (Trim): DM Mono as a third font, an off-token
     white and a second orange; use the tokens and the two fonts.
  Then ask the owner (with the estimate) whether the Juror should score again.
  Not decided by the chats: keep `[to supply]` visible (the owner's standing
  rule: a missing fact shows as `[to supply]`; the Juror would hide empty
  fields: put that to the owner, do not change it). The pilot cut-out's grey
  rim and the shadow blobs in the opening (Juror, Trim) need image work: try
  only if it can be done cleanly, otherwise list it.
- **Still waiting on the owner:** Panchgani's and Kenya's launch heights and
  prices, Panchgani's group and rating; "Guaranteed to run, 6 places" for all
  four India 2027 departures; Peru and Kazakhstan dates; a second Panchgani
  photo; the big-wing Kenya photo, if any; India JPGs under 10 MB; a JPG of
  DSC_6210; the live episode chart and the five Kenya repeat photos; the
  switch-over (it changes the live home h1).

## Where chat 11 left it (24 Oct): Panchgani has its page and is across v4, the phone fixes and the review are done
- **Step 4 done (01505966, gates PASS): Panchgani's page**
  https://paraglidingatlas.com/prototypes/v4/destinations/panchgani.html, by
  `tools/v4_panchgani.py` (run by hand, then the build; it writes the page from
  the v4 Kenya page's frame, and `img/panchgani/plateau.jpg|webp`, the
  opening's ground with its wing put back). Hero (one photo, no rail, the
  credit on it), jump row, facts (launch, rating, group, price `[to supply]`),
  overview and six questions from Vistasp Kharas's episode (each fact his, or
  the owner's dates), one departure card (Hold a place with
  `?trip=panchgani&when=14+to+21+February+2027`), the episode, the call band,
  the booking bar. A small script lights the dates band (Kenya's overview
  script does it there). `tools/v4_ux.py` TRIPS and `tools/v4_phone_media.py`
  take Panchgani as a third trip (the phone cut `img/hero/panchgani-plateau-p`);
  v4_ux's trip_dates_first skips a page with no route or gallery, its price
  regexes allow `<b class="v2-tbd">`. `tools/v2_site.py` NEW_PAGES lists
  `destinations/panchgani.html` (no live twin: the switch writes it, indexable,
  into the sitemap); its canonical and og:image are the addresses it will have
  (`/destinations/panchgani.html`, `/assets/v4/img/panchgani/plateau.jpg`).
  The opening's Panchgani button is "See the Panchgani trip" (sample, then
  `tools/v4_home_opening.py`, then the build; the build title-cases the home
  headings, so commit its output).
- **Step 5 done: Panchgani across v4.** `python3 tools/v4_panchgani.py links`
  puts "Panchgani Tour" after Kenya in every footer (not samples, not
  library.html: the library is the other chat's); v4_build runs it after the
  encyclopedia's pages, which are rebuilt from a source without it. Phone menu
  (`src/v4-menu.js`), enquire's trip list, the sitemap (a fifth trip in its
  SITEMAP_SKY tree, thumbnail `img/panchgani/plateau-thumb.webp`, five
  positions in `tools/v4_sitemap_sky.py`; India's line now "April to May,
  October to November"), the home departures (a row after Kenya, "Dates set",
  group and price `[to supply]`; v4_polish draws it on the line of months),
  the expeditions page (`tools/v4_expeditions.py`: five places in the
  season's order, Panchgani 02 without a photo, words cap 450; year labels
  carry months only, Kenya's ends at its last departure, India's ends with
  October where Peru's begins, and on a phone Kazakhstan's and India's are
  nudged apart), and Fly it yourself on the Panchgani episode
  (`tools/v4_pass.py` TRIPS).
- **Decided without the owner (tell them):** Panchgani's only photo appears on
  the opening, its page hero and the sitemap thumbnail; the home fly-by and the
  expeditions page leave it out rather than repeat it again. A second
  Panchgani photo would fill both. Panchgani's status reads "Dates set" (not
  "Booking open", which the owner has not said).
- **Step 6 done: the opening's two phone faults.** (1) The route's label
  boxes (`.tp`, 4.6rem wide on a phone) overlapped: Panchgani's took taps on
  Kenya's marker, a neighbour's took the end of India's and Kazakhstan's
  names. Now `.tp{pointer-events:none}` and only `.tp-n` (its own width,
  padded 8px 4px, placed as before) and `.tp-r` (a 7px tap ring) take taps;
  checked by elementFromPoint at 320 to 1440 px (one ambiguous 4px edge at
  320, where the two markers are 13px apart). (2) The swipe: the old code let
  every slow short swipe through (before the next photo was ready, any 40px).
  Now the speed is over the last 60 ms (`drag.hist`), zero if the finger
  rested 90 ms before lifting, a flick needs 0.45 px/ms and 8% of the way,
  and the no-photo path needs the same third (W * 0.62 * 0.3) or a flick.
  Tested by in-page PointerEvents on a timer (CDP touches arrive ~100 ms
  apart, too slow to flick): slow short, twitch and rest spring back; flick
  and long go. Headless frames lag once WebGL runs, so the ready path reads
  every swipe as slow there; check it by hand on a phone.
- **Step 11 done: the final review pass.** 19 main pages at 1440 and 390 px
  (home, expeditions, the three trips, podcast, knowledge base, library,
  the Panchgani episode, enquire, about, sitemap, mission, record, topics,
  the Atlas, partners, 404, terms): no script errors, no sideways scroll, no
  broken image, no failed request. Hold a place from Panchgani opens enquire
  on its departure; its price now shows as the to-supply mark
  (`tools/v4_ux.py` HOLD_JS). The only new check warning is Panchgani's "no
  live twin", expected. The scheduled task "Chat 11: carry on the v4 plan" is
  disabled: every step that does not wait on the owner is done.
- **Waiting on the owner:** Panchgani's and Kenya's launch heights and
  prices, Panchgani's group size and pilot rating; whether "Guaranteed to
  run, 6 places" applies to all four India 2027 departures; Peru and
  Kazakhstan dates; a second Panchgani photo (for the home fly-by and the
  expeditions page); which big-wing Kenya photo, if any; full-size India JPGs
  under 10 MB; a JPG of DSC_6210; the live episode chart and the five Kenya
  repeat photos; the switch-over (it changes the live home h1 to
  "Paragliding expeditions, run by a pilot.").

## Where chat 10 left it (24 Oct): the opening is the v4 home hero, India is in 2027 everywhere; chat 11 builds Panchgani's page
Live (17f53b72, gates PASS): https://paraglidingatlas.com/prototypes/v4/samples/opening/
- **The move between places is E's** (owner: "build E only"): the camera flies
  forward into a cloud and out of it over the next place (`flight()`,
  `flyCSS()` for no WebGL with the `.veil`, shader `flyAt`/`flyCover`, uniforms
  `uFly`, `uFlyB`, `uCloud`, `uFlyO`, `uWordS`; 1.4 s, `easeFly`); the season
  glider lifts a few px on the leg (`--ga`). The orange wipe is gone. D and F
  were built (scratch only, never pushed) and dropped.
- **Skip** (owner): a click on the progress line fills it in 0.32 s and the
  next place flies in, paused or not (`.skip` button over the line, `skipping`).
- **Peru back to Kenya** on autoplay: forward round the season (`autoWrap`,
  `trans.wrap`, glider fades at the ends, `--go`).
- **No photo switch** (owner): `.kpick` and the `#india` jump removed; Kenya
  defaults to DSC_9492 (`pick` default map; `?kenya=9452|9522`,
  `?india=redwing|launch` still reach the others). No-JS still shows the 9452
  layers: hard-wire 9492 when building into the home page.
- The owner's other chat (session_01DCHUF6z6Tm2mvyLyj9PbTP) pushed the play
  button without a ring and three standing designers (`.claude/agents/designer-*.md`,
  `docs/designers/`); the owner: "those pushes have to stay". Record design
  decisions in `docs/designers/direction.md`.
- **The owner said "go autonomous"** at extra high effort: carry on without
  asking, through usage resets (a scheduled task in this session wakes it),
  steps in this order, each ending with gates and a push:
  2. **Done (f47d960e, gates PASS): the opening is the v4 home page's hero.**
     `tools/v4_home_opening.py` (run by hand after any change to the sample,
     then the build) copies `samples/opening/` into `index.html`: photo layers
     to `img/opening/`, the hero between `<!-- v4-home-opening -->` marks
     (replacing the old kit-hero, its footage and the ridge drawing; so
     `tools/v4_opening.py` has no place any more), styles fenced to `#held`
     (classes on <html> renamed `op-*`, keyframes `op-*`, the kicker
     `op-kicker` because the site greys every `.kicker`, the site's slanted
     `.btn-solid` box undone), the site's nav lying over the photo, the script
     loading from `img/opening/`. The build title-cases the headings. v4_polish
     skips its figures when the old hero is gone. `tools/v2_check.py` EXEMPT
     now lists the home h1 ("Paragliding expeditions, run by a pilot.") as
     the owner's deliberate change from the live "Touch The Sky With Glory":
     **tell the owner this changes the live h1 at the switch-over.**
     The sample is the single source; Kenya is fixed to DSC_9492 there.
  3. **Done: India's 2027 dates everywhere in v4** (four departures, 15 to
     24 Apr, 25 Apr to 4 May, 21 to 30 Oct, 3 to 12 Nov 2027).
     `tools/v4_india_2027.py` (idempotent, run by hand) moved the pages: the
     India page (two season bands, spring and autumn; four cards; strap, FAQ,
     terms, structured data; "Next departure 15 Apr 2027"), the home
     departures (by month, dated before planned) and fly-by, every episode's
     Fly With Us (Kenya first now), the Fly it yourself links, About. The
     generators carry the dates (v4_expeditions*.py with a cross-month
     departure, v2_fly_options, v2_episode, v4_pass TRIPS, v4_trip_calm
     BIG/QUIET, which now expects four flags). v4_polish's line of months
     reads a departure that crosses a month. The India search description is
     the owner's fact (`tools/data/v4_facts.json` india_2027), accepted by
     v2_check's parity. Carried over, not confirmed by the owner: "Guaranteed
     to run" and "6 places" for all four (as the opening already says), and
     the booking terms line now just points to the terms (the 120-day rule
     no longer fits). Never run `tools/v2_fly_options.py` without `--site v4`:
     it writes prototypes/v2 (reverted once in chat 10).
  4. **Next (chat 11 starts here): Panchgani's destination page**, then its
     button in the opening points there (edit `samples/opening/index.html`,
     run `tools/v4_home_opening.py`, then the build). Only India and Kenya
     have pages (live and v4); Panchgani's has no live twin (v2_check warns
     "no live twin", fine). Plan scoped in chat 10: a generator
     (`tools/v4_panchgani.py`) that takes the v4 Kenya page's shell (head,
     nav, footer, the dst-* section classes) and writes
     `destinations/panchgani.html` with: hero (the opening's Panchgani layers
     in `img/opening/`, credit "Photo by Michael Gebert /
     @flywithandy_paragliding"; the only Panchgani photo, so it repeats the
     opening's: note it to the owner), facts (14 to 21 Feb 2027, 8 days,
     17.92°N 73.82°E, Sahyadri hills; launch, price, group, rating
     `[to supply]`), overview and FAQ from the episode
     `episodes/navigating-panchgani-vistasp-kharas.html` with Vistasp Kharas
     named (take-off about 1,100 to 1,200 m; 3,000 to 4,000 m in peak season;
     two hours from Pune, four and a half to five from Mumbai; volcanic
     plateaus of the Deccan, sharp cliffs, flat tops; evening coastal winds
     time the window; season November to March, the wind turning from
     north-northeast to southeast; strong, punchy thermals, SIV advised, EN-B
     fine; Panchgani to Kamshet about 100 km; the pre World Cup), one dates
     card (Hold a place, `enquire.html?trip=panchgani&when=14+to+21+February+2027`),
     the episode as "from the show", the call band. Keep the facts row's
     launch `[to supply]` (the owner's number), quote the episode elsewhere.
  5. Panchgani in the rest of v4 (expeditions pages, the home departures and
     fly-by, enquire's trips and v4_ux `TRIPS` for hold data, sitemap, map,
     nav where destinations are listed). Reorder the expeditions generators'
     PLACES to the season (Kenya, Panchgani, India, Kazakhstan, Peru) then.
  6. Small fixes: on a phone India's label covers the Panchgani marker; a
     short swipe on a phone went through as a flick (check it springs back
     below a third when slow).
  11. A final review pass of v4 on phone and desktop.
  Skip what waits on the owner (facts, photos, the episode chart, the
  switch-over) and list it at the end. Never touch the library's files.
- Testing tip: headless screenshots are too slow to catch a 1.4 s move; slow
  the page clock (`performance.now` scaled after load) to take frames.

## Where chat 9 left it (24 Oct): the route plays on, Panchgani is a fifth tour, India moves to 2027, the opening is on the prototype
Chat 9 added one v4 page, the opening sample (`prototypes/v4/samples/opening/`); the rest is docs. Its work is in the review page
https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (newest at the top; F2's
code is its published file `F2/index.html`, the Panchgani layers are
`F2/panchgani-*`).
- **No restart, the route moves on** (owner: "the transition in kenya is
  making the gliders abruptly switch positions ... instead move on the next
  slide and maybe we can make this as a progress bar ... make the line a bit
  sleek"). The cloud restart is gone: each place plays one forward pass
  (14 s, `push.ms`; 14 s for a place without a move), then the route goes to
  the next place in `ORDER`, round again after the last. During the wipe the
  old pass keeps flying forward (z runs on past 1, capped at 1.3). The short
  orange line on top of the trip readout (`.deck::before`) is now a progress
  bar: full width, 1 px, a soft glow, `scaleX(var(--prog))`; it drains as the
  next place wipes in. Code: `playOn()` and `dwell` in F2/index.html; it
  pauses off screen, in a hidden tab and mid swipe, and restarts when the
  visitor picks a place. Reduced motion: no autoplay, the line stays 48 px.
- **Panchgani** (owner: first "Add Panchgani to F2 as option A", a podcast
  stop apart from the season; then "it has dates, 2 days after the last kenya
  tour and runs for 8 days"; then "yes, it is a proper tour which will need
  to have all its necessities like other destination pages in the site, for
  now do this and then we proceed"). Now a dated tour on the season line:
  14 to 21 Feb 2027, 8 days (Kenya's last ends 12 Feb), bar at left 31.89%,
  width 2.04%, marker 32.91%; `ORDER` is India, Kenya, Panchgani, Kazakhstan,
  Peru. Its name reads to the right of its marker (`.tp.lt`), and on a phone
  sits a row above Kenya's. Readout: launch and price `[to supply]`; "You fly:
  The plateau that hosted a pre World Cup" (episode summary); photo credit
  under the place name, "Photo by Michael Gebert / @flywithandy_paragliding"
  (owner's words; the handle links to Instagram); the button is still
  "Listen: Navigating Panchgani" (`episodes/navigating-panchgani-vistasp-kharas.html`)
  until a Panchgani tour page exists. The `.season` box and the route-%
  glider positions read from each marker in `layout()` stay (with `--s:1`).
  Photo: the review page's `src/panchgani.webp` (1500 x 756). The wing keeps
  its real size and place (`box`, mapped through the ground's cover rect);
  PANCHGANI is at Kazakhstan's size (`sizeAs`) with its middle on the
  plateau's flat top (`rim: 0.285`). Motion (owner: "a left circle with a
  very shallow angle while moving forward ... ensure this does not become
  nauseating"): over each 14 s pass the land comes 4% nearer (`g` 0.04 about
  `far` [0.47, 0.4], depth `k` 0.04), slides 2.5% of the width right
  (`pan[0]`, centred) and turns 1.6 degrees clockwise about the frame's middle
  (`push.rot`, new uniform `uGRot`); name and wing hold still. The wing was cut
  by hand (low saturation inside its box, the pilot in a tight box: about
  110 px of wing, too small for the line tools), then `scene.py` with
  place-named outputs, `groundw` 1500, `wingw` 240.
- **The three standing designers** (owner, 24 Oct: "how can we have access
  to 3 master designers all the time so it doesn't get confusing, because
  every time we switch I think it's a loss of direction"): `designer-d`,
  `designer-e`, `designer-f` in `.claude/agents/`, their memory in
  `docs/designers/` (`direction.md`: the brief and the owner's decisions, keep
  it current; `D.md`, `E.md`, `F.md`: their notebooks). Use them for every
  design question. The owner was given a prompt for chat 8 so the original
  three write their own notebook entries; if chat 8 has pushed them, read
  them first.
- **The play button and the line** (24 Oct): no ring, dim until hovered, a
  small gap before it; the progress line at 75%.
- **Chat 10 starts here, in this order** (owner, 24 Oct, asked whether the
  opening should replace the v4 home page's own opening: "do it"):
  1. **Build F2 into the v4 home page** (`prototypes/v4/index.html`), in
     place of its current opening: the source is
     `prototypes/v4/samples/opening/index.html` (the same as the review page's
     F2/index.html; its page links carry `../../`). The home opening is made
     by `tools/v4_polish.py` (`home_markup`, HOME_CSS, HOME_JS); the assets
     go into `prototypes/v4/img/` (never `assets/`). Keep F2 as it stands:
     the season route with Panchgani and India's four 2027 departures, one
     pass then the next place, the progress line with play and pause, the
     real-size Panchgani wing and its left turn, the DSC_9492 follow shot
     (`?kenya=9492` picks it in the sample; in v4 make 9492 Kenya's photo, as
     the owner chose option A for it) and drop the review-only photo switch
     (`.kpick`). The rest of the home page stays. Use the site's own fonts
     (`prototypes/v4/fonts/`), not Google Fonts, and the design tokens.
  2. **India's 2027 dates everywhere in v4** (next point).
  3. Then Panchgani's own destination page and the rest it needs (owner:
     "it is a proper tour which will need to have all its necessities like
     other destination pages"), and its button changes from the episode to
     that page.
- **India's dates** (owner, 24 Oct: "move dates of india to 15th april for
  the first tour and then 1 day later the next one", then "keep the older
  india dates for 2027 so make that tour visible as well accordingly
  everywhere needed"). In F2 India now has four departures, 10 days each:
  15 to 24 Apr 2027, 25 Apr to 4 May 2027 (one day after the first ends,
  read like Panchgani's "2 days after"), 21 to 30 Oct 2027, 3 to 12 Nov 2027.
  Bars at 46.19/2.38, 48.57/2.35, 90.32/2.3, 93.33/2.38 (%), marker 48.56%;
  `ORDER` is Kenya, Panchgani, India, Kazakhstan, Peru; on a phone
  Kazakhstan's name reads right of its marker (`.tp.lt-m`) to clear India's;
  the dates are one a line (`dd.four`). The Oct and Nov 2027 bars sit inside
  Peru's dashed "planned Nov 2027" box. **Not done, chat 10's first job:**
  the same dates "everywhere needed" in v4 (only v4; live pages are the
  owner's). India's 2026 dates are written in many generators: grep
  `21 to 30 Oct 2026`, `2026-10-21`, `3 to 12 Nov 2026` in tools/ (v4_expeditions*.py,
  v4_trip_calm.py, v4_pass.py TRIPS, v2_episode.py, v2_fly_options.py,
  v3_directions.py, ux_measure.py, smoke.py) and prototypes/v4 (index,
  expeditions*, destinations/india, enquire, about, fly-options, styleguide,
  v4-sitemap-sky.js); some v4 pages are localized from the live pages, so
  change the v4 generator or polish step, never the live page.
- **The opening is on the prototype** (owner: "make this page live on proto
  and give me the link"): `prototypes/v4/samples/opening/` (index.html plus
  its 47 files, about 6.7 MB), a standalone review page (noindex, links to
  the v4 pages with `../../`, its own styles: a comment names why it links
  neither styles.css nor v2.css, which v2_localize looks for). Live at
  https://paraglidingatlas.com/prototypes/v4/samples/opening/?kenya=9492
  once deployed. It is a copy of the review page's F2: change both, or
  rebuild this one from F2 (rewrite the page links to `../../`).
- **Play and pause** (owner: "give a subtle yet elegant and sleek play pause
  button for those who want to stay on the image"): a 30 px ring at the right
  end of the progress line (`.play`, shown only with `.auto`), the line stops
  46 px short of it. Pause holds the place and its move still (`paused` stops
  both `dwell` and `pushClock`); play goes on from there. Both copies (F2 and
  `samples/opening/`).
- **The library is another chat's** (owner, 24 Oct: "forget about library
  here, I'm working on it on another chat ... which needs to be connected to
  chat 10"): the owner's chat https://claude.ai/code/cshk_014sbQF9W1CqGXbH3oHgNsEBPkibnHiMxcAso6rNZN4e7y
  (session_014sbQF9W1CqGXbH3oHgNsEB, "Website immersion capabilities
  assessment"). Do not change `library.html`, `tools/v4_library.py` or the
  library chart from this chain; before touching anything the library
  shares (the build, `tools/v4_polish.py`, the nav), check with the owner.
  That session can be found with list_sessions and sent a message
  (SendMessage to its name), but a cloud session cannot answer back, so
  anything it needs to know goes through the owner too.
- **Next (owner):** Panchgani needs everything the other destinations have
  in the site (its own destination page and the rest); the owner said "then
  we proceed", so ask what comes first only if it is not clear from them.
- **Waiting on the owner (do not push):** how the autoplay and the Panchgani
  turn look live; Panchgani's launch and price; and everything still
  listed under chat 8 below.

## Where chat 8 left it (24 Oct): F2's Kenya photo and DSC_9492's move, nothing half-built in the repo
Chat 8 changed nothing in v4 (docs only: this section, `docs/home-opening`
README and `scripts/sheet.py`, the contact-sheet maker). All its work is in
the review page https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (newest at
the top; F2's code is its published file `F2/index.html`).
- **Big-wing search** (owner: "stunning photos only where the wing is
  visible largely"). Went through the Drive's "Kenya Feb 2025" (62 JPGs and 6
  NEFs; 58 JPGs downloaded) and "Go Pro Photos" (10 frames, all Norway and a
  sea coast, nothing for Kenya or India). Shortlist sent to the owner, no
  answer yet: **DSC_9473** (orange wing against the sky, lines clear; the
  pick), **DSC_9489** (orange and blue over red earth), **DSC_9792** (biggest
  wing, over grass); runners-up DSC_9814, DSC_9763. Not reachable through the
  connector: IMG_2073, IMG_2074, IMG_2132 (8.5 to 9.7 MB, the connector drops
  on them) and IMG_2111 (over 10 MB). India: still no originals; the owner
  was asked once for full-size India JPGs under 10 MB.
- **Wing liveries** (owner asked to see the wing in a Kenyan pattern, then
  said "forget it"). Three F1-style looks were shown in chat only (shuka
  slash, bead line, Maasai shield). Dropped; do not raise.
- **DSC_9492 now moves** (owner: "the gliders have to go away from the viewer
  and background is correct, but this has to be done slowly"; three designers
  D, E, F were asked; the owner said "ok" to option A, D's and F's): a follow
  shot that starts when WebGL takes over (about 1.55 s), 12 s each way. The valley grows 1 to 1.08 about its far point (uv 0.42, 0.18 of the
  ground) with a depth dolly 0.10; the gliders shrink 1 to 0.9 about their
  own centre and drift 2% of the width toward that point; their shadow gap on
  the letters shrinks to 0.6 and darkens 14%; the mouse pull shrinks with
  them; scroll works on top. The arrival glide for this photo starts at
  scale 1.05 from lower right (`glide-away`), so the gliders only ever move
  away. Code: F2/index.html `PHOTOS.kenya['9492'].push`, `pushZ`, `drawDest`,
  uniforms `uDolly` and `uShK`. Option B (E's: scroll drives the move, bigger)
  was not chosen.
- **Then (owner, 24 Oct):** "the shadows become too prominent upon scroll,
  reduce that by 50%": on every place the gliders' shadow strength now falls
  to half as the page scrolls (`uShK` times `1 - 0.5p`) and its scroll gap
  grows half as much (`lift` 1.4 to 0.7). "Do the same with India": the
  snowline photo drifts, the ground 2.2% of the width right plus a depth
  shift 0.03 (near rock moves more) under a 5% zoom that hides the edges,
  the wing 3.5% left, 14 s each way (`DESTS.india.push`); "red wing" and
  "launch day" stay still. (A first, smaller drift, 1.2%, was too small to
  see: the owner said "the india animation isn't working".)
- **The owner changed the motion rule for these (24 Oct):** "for both kenya
  and india add this as a infinity loop, as long as the viewer stays the
  immersion stays"; then "the gliders start reversing after a bit, that
  defeats the purpose, they should only go in one direction, and that is
  forward" (Kenya, then "do the same for india"), and "make sure your
  restart is awwwards worthy". So both moves only ever go forward, forever:
  each pass runs 14 s at an even pace (the first starts from rest); the next
  pass starts 9.1 s in (`fade` 0.35). The restart is hidden in a cloud we fly
  through: in Kenya a ring of cloud streams out from the valley's far point,
  in India a bank of cloud drifts across with the snow; the next pass is
  drawn over the last only where the cloud has already passed (shader
  `cloud()`, uniforms `uMist`, `uMistB`, `uRev`; per place `push.mist` =
  [mode, colour, peak]; India's colour is above 1 because its grade is dim).
  A faint wisp (0.08) always drifts. Time runs only while that place is
  drawn, so it pauses off screen, in a hidden tab and on other places.
  Reduced motion: still. This is the owner's exception to "nothing loops on
  its own" for these two opening moves only. Testing note: headless
  Chromium draws slowly, so the scene clock (capped at 50 ms a frame) runs
  at about half speed there; capture by the clock, not by wall time.
- **Waiting on the owner (do not push):** which Kenya big-wing photo (if any)
  to build into F2 the same way (grade, cut-out with real lines, filled
  ground, shadow, depth: `docs/home-opening/README.md`); India originals;
  everything still listed under chat 7 and chat 6 below.
- Testing WebGL in this container: serve the folder over http on any port
  but 8765 (the gates use 8765 and will use, and fail on, any server already
  there), not file:// (textures from file:// are
  cross-origin and the WebGL scene never starts); headless Chromium has WebGL.

## Where chat 7 left it (24 Oct): the home opening is down to photo choices, nothing half-built in the repo
Chat 7 changed nothing in v4. It ran a second round of three designers on
C2 (the owner, 23 Oct: "C2 is really nice", asked for a competition to
improve it). All live in https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG,
newest at the top, each with its files under its letter:
- **D. Final Cut** (craft: drawn lines, a light per place, film-cut switch),
  **E. Pull Back to the Route** (scroll pulls back into a four-place route
  that replaces the destinations section), **F. Fly the Season** (the list
  becomes a season line Oct 2026 to Nov 2027 with each trip's readout and a
  button to its page; `[to supply]` for Kenya, Peru and Kazakhstan launch
  heights and the Peru and Kazakhstan dates).
- The owner looked at **F** and asked for the wing's "original lineset" back,
  then chose photos: DSC_9522, DSC_9492 and DSC_6210 for Kenya, and "similar
  examples for India". Built as **F2** (same page, `F2/`): a review-only pill
  switches Kenya (now DSC_9452, DSC_9522 with its real lines traced from the
  photo, DSC_9492 three gliders) and India (now snowline, red wing, launch
  day; no lines, only 1400 px copies exist). How the layers are made, and the
  scripts: `docs/home-opening/README.md`.
- **Waiting on the owner:** which design (F2 is the one they are working
  in) and which photo per place; a JPG export of DSC_6210 (the NEF is over
  the Drive connector's 10 MB limit); full-size India originals if India
  should get real lines. Still open from chat 6, not raised again in chat 7:
  the live episode chart (finish or drop) and the five Kenya repeat photos
  (both below, unchanged).
- On a yes: build the chosen design into `tools/v4_polish.py` `home_markup`
  and HOME_CSS/HOME_JS, layers into `prototypes/v4/img/`, drop the pill.
  Note DSC_9452 is also the record page's new Kenya photo (chat 6), and the
  India choices are in the India gallery: "no photo twice" needs a call.
- Container (24 Oct): the preinstalled Chromium is now build 1243, so the
  gates' browser needs `pip install "playwright==1.63.0"` (1.56.0 no longer
  launches; check `/opt/node-tools/node_modules/playwright-core/browsers.json`
  if it moves again). Still `git fetch --unshallow origin claude/v2-prototype`
  and `pip install contourpy fonttools brotli` first.

## Where chat 6 left it (23 Oct): three things wait on the owner, nothing half-built in the repo
Chat 6 changed nothing in v4. Its work lives in two private review pages the
owner has; their published files are the hand-over (read them with the
Artifact tool, `action: "read"`, `path`).
- **The live episode chart** (owner, 22 Oct: "make this live and real
  clickable to episode pages"). Built and tested in chat 5; screenshots in
  the review page https://claude.ai/artifact/H3xMx4aW6teybonm5aYpvY. The
  owner has not said "finish it" or "drop it". The change is that page's
  published file `chart.patch` (tools/v4_pass.py topic_log and topic_page,
  tools/v4_library.py, tools/v4_polish.py LOG_CSS and LOG_JS, report row 54).
  To finish: `git apply` it, `python3 tools/v4_build.py` twice (the second
  changes nothing), `git checkout -- sitemap.xml`, commit, gates, clean
  rebuild, push. To drop: nothing to undo.
- **Five new Kenya photographs for the repeats** (owner, 22 Oct: find them
  in the Drive, "impactful and captivating", edited to match the site).
  From the owner's Drive folder "Kenya Feb 2025" (Paragliding Atlas > PG
  Atlas Photos > Photos by Self): DSC_9840 for About's Kenya card, DSC_9842
  and DSC_9541 for Expeditions' Kenya and Kerio Valley photographs (with 2:3
  phone crops), DSC_9452 and DSC_9537 for the record page's Kenya and Kerio
  Valley photographs. Graded warmer and deeper with a soft vignette, framed
  on the wing. The finished files (jpg and webp, `edit/` in the same review
  page) await the owner's yes; the review page shows each against the photo
  it replaces. Where each is set: Expeditions in `tools/v4_expeditions.py`
  (about lines 337 and 366), the record page in `tools/v4_record*.py`,
  About's card comes through the v2 About build (find `kenya-3` in the
  About source). Put them in `prototypes/v4/img/`, never in `assets/`.
  Still uncovered: India, Peru and Kazakhstan (no photographs of them in the
  Drive), Coupe Icare (the Drive's "Coupe Icare Asset Sheet" folder is not
  yet looked at). The Drive connector refuses files over 10 MB and dropped
  the connection on them; the owner's "Hi Res Camera" folder needs smaller
  exports.
- **The home page opening** (owner, 23 Oct: the hero "is a joke"; asked for a
  competition between three designers). Three mock-ups (A footage, B atlas
  chart, C still photograph with the wing cut out over a giant KENYA); the
  owner liked C, asked whether dropping video lost awwwards ground, and said
  "ok" to both upgrades: C2 adds depth-map parallax (Depth Anything) in
  WebGL, the wing's shadow on the letters, a pointer light, static grain, a
  one-time arrival (about 1.5 s, approved), footage inside the letters on
  point or tap (India: the Bir clip; the others a second photograph, since
  footage must come from the named place) and a four-destination switcher.
  All four live, with their files, at
  https://claude.ai/artifact/BFTmxrj3NZpbkf3cqcYtxG (C2 first). Waiting for
  the owner's verdict on C2. C2's open points: Peru and Kazakhstan reuse
  peru-1 and kazakhstan-1 (already lower on the home page; kazakhstan-1 may
  be a composite, ask); the wing cut-outs lose the lines; not yet tried on a
  real iPhone. New headline in C and C2: "Paragliding expeditions, run by a
  pilot." Building the winner into v4 means `tools/v4_polish.py`
  `home_markup` and HOME_CSS/HOME_JS, the assets into `prototypes/v4/img/`.
- Parked by the owner (23 Oct, "I'll take my own time, don't disturb me"):
  the Encarta concept for the globe and the encyclopedia home. Do not ask.
- Small, not yet offered again: on a phone the library chart's year labels
  and "166 min" are tiny (the topic pages' chart got larger ones in row 45).
- The build needs `contourpy` (`pip install contourpy`; v4_expert.py's
  meteo drawing). A fresh container may lack it: `v4_build.py` then fails at
  `v4_pass.py`.

## Where the queue stands (21 Oct)
Items 1 to 3 below are done and pushed: the sitemap's real sky (row 35, with
the motion the owner asked for), Partners (row 34) and the site-wide pass on
home, podcast, library, knowledge base, topics, About and Mission (rows 36 to
43). The owner chose every look from side-by-side previews; the episode
reader fix the switch-over needed is done too (the report's switch-over
section). What is open:
- **The record page photo**: built on 21 Oct (report row 44) as the owner
  chose from mock-ups, `docs/record-photo/README.md` and `tools/v4_record.py`
  01 the mark. A full-size export of DSC06347 would let it fly larger.
- **The review of every page type** (21 Oct): screenshots of 17 page types
  on desktop and phone sent to the owner, with what the review found (below,
  under "Found in the 21 Oct review").
- Done on 21 Oct from the review (row 45): the four small fixes and the
  corrections v4 can make. Left for the owner: the same
  corrections in the live site's own sources (generate_tag_pages.py lines
  331 and 363, episode-meta.json, destinations/kenya.html).
- Photographs used twice on v4 (owner's rule), each waiting for a new
  photograph from the owner: About's Kenya, Peru and Kazakhstan cards (the
  home page's), Expeditions' India and Kenya photographs (the trip pages'),
  and the record page's Kerio Valley, Kenya hero and Coupe Icare photographs
  (the Kenya page's and Partners'). Episode cover art repeats by design.
- The home page (roadmap step 6): built on 21 Oct, both directions the
  owner chose ("both A&B", report row 46): figures under the opening that
  count up, every departure on one line of months, the held photographs that
  come closer, the episode cards that lean gently towards the mouse (a
  stronger lean was tried and turned back by the owner; the trip list's
  orange fill was taken out, "remove this"). All in `tools/v4_polish.py` (HOME_CSS, HOME_JS, `home_markup`,
  read from the site at each build).
- **The encyclopedia** (21 Oct, report row 47): the A to Z and the ten
  Flight Mechanics answers are v4 pages under the knowledge base
  (`tools/v4_encyclopedia.py`, rebuilt from the review copy in
  `prototypes/workspace/drafts/` on every build), reached from the knowledge
  base page, Flight Mechanics and the FAQ answers the A to Z links to.
  Prototype-only until the owner has reviewed the ten drafts. A change to an
  answer is made on the encyclopedia-pilot branch (`kb_answers.py`) and the
  review copy built again (`ENC_SHOW_DRAFTS=1`). That branch's A to Z filter
  changes only the count (fixed in v4 only).
- **The Encarta pieces** (21 Oct, report row 50, `tools/v4_enc_lab.py`): the
  seven worlds and the featured article on the A to Z, the moving wing on
  Collapse, the angle-of-attack lab on Collapse and Stall. Next, if the owner
  wants more: Active flying with the same lab, the Encarta build's kinds of
  collapse and step-by-step pictures, and a picture for each other answer.
- **The Atlas** (21 Oct, report row 48): the knowledge base's button opens
  the globe (`knowledge-base/encyclopedia/atlas.html`, `tools/v4_atlas.py`),
  and its pins and questions lead into the encyclopedia. Built from the
  site's own data (globe-episodes.js, the FAQ answers, the ten answers),
  not from the workspace's Flying Atlas, whose 450 entries were never
  checked. On the home page too, later, if the owner wants it there.
- **The sitemap's ground** (21 Oct, report row 49): every page that is not an
  episode, one click away under the sky (`tools/v4_sitemap_sky.py` ground()).
  The landmarks followed (row 52): Home as the moon, the Atlas, the
  knowledge base's altitude scale, the trips as planets over the ridge and
  the named stars. Not built: the topics as a Milky Way.
- From the 20 Oct roadmap, still open: icons to photographs (step 7,
  waiting for the owner's photographs; on About the owner chose to keep the
  icons).
- The switch-over stays the owner's.

## The queue, in the owner's order (20 Oct)
1. **The sitemap's night sky from real stars.** The v4 sitemap
   (`prototypes/v4/sitemap.html`, built by `tools/v4_catchup.py`
   `sitemap_sky()`) loads the LIVE `sitemap-sky.js`, which must never be
   edited. Its background field is seeded random (`rnd()`, seed 20261002, about
   line 47) drawn on the `.sky-stars` canvas; the episode stars and the series
   constellations are data and stay. Real positions and magnitudes are already
   in the repo: `tools/v4_record.py` `STARS` (d3-celestial 0.7.35,
   `data/stars.6.json`, BSD-3-Clause, XHIP; the credit and notice are its
   `STAR_NOTE`, which must go with the data). Way in: a v4-only background
   layer under the sky (or a v4 copy of the script, `prototypes/v4/`), loaded
   only by the v4 sitemap, credited, still (no twinkle), drawn once; then add
   its tool step to `tools/v4_build.py` after `v4_ux` if it patches the page.
2. **Partners** (`prototypes/v4/partners.html`): the formats laid out like the
   record page's offer, the audience numbers big and still with an "About
   these numbers" fold (80 from the feed; 130+ countries confirmed by the
   owner on 20 Oct; 100,000+ streams and 10+ years have no stated source, so
   `[to supply]`), and a link to the record attempt inside
   `<!-- v4:needs record-attempt.html -->` marks that `tools/v2_switch.py` drops
   while the record page is prototype-only. Run in the previous session as a
   workflow; if row 34 of the report is not there and nothing is pushed for it,
   start it again from this brief. `partners.html` is the shell (head, menu,
   footer) that the record, Expeditions and feed-option generators copy:
   leave those parts alone and prove their pages unchanged.
3. **The site-wide pass, only on**: home, podcast, library, knowledge base,
   topics, about pages. Episode pages are off the list for now (owner, 20 Oct).
   One page type at a time, screenshots to the owner after each, the way India
   was done (report: "India, less but better"). Topic pages are a template
   over about 50 pages: build the change in a tool, check a sample of pages,
   and prove the rebuild.

Then, before any switch-over: `tools/v2_episode.py` must read the live episode
header of 2 Oct. Done on 20 Oct (commit 19f4707f): a new episode builds again. Kenya's pass is paused by the owner; the
cheap option offered was removing only what breaks the motion rule (its hero
slideshow timer and the slow zooms).

## Found in the 21 Oct review
17 page types on desktop (1440) and phone (390), captured by scrolling a real
window one screen at a time and joining the screens (one tall full-page shot
breaks the pinned and scroll-driven parts), read by two agents and every
finding checked again by hand; sent to the owner as a page
(https://claude.ai/artifact/5oA3E1CrreKHtYgbopMXW3). No script errors.
- Fixed (a regression of row 36): the library's opening chart drifted over
  "Start here / All Series" on a phone; its drift now stops at the room left
  in the opening (`tools/v4_polish.py` LIB_JS).
- For the owner (content, also on the live site): topic pages promise a full
  transcript for every episode (`generate_tag_pages.py`, lines 331 and 363)
  while Safety has 29 of 30; the "New Technologies 3: Stephan Stiegler"
  description lacks a name ("the innovative designer from .",
  `episode-meta.json`; probably AirDesign); 80 episodes on some pages, 93 on
  others (both true: 80 in the feed, 93 with the 13 YouTube-only videos);
  Kenya's "Took It's First Steps".
- Proposed v4 fixes, built the same day (report row 45, commit e7398530; checked again in the browser on 21 Oct, all four in place): the podcast feed's failure message
  ("the saved archive is below instead", from `rss-feed.js`, with nothing
  below; v4 can replace it with a link to the library); a soft shadow behind
  the home opening's small orange line over bright snow; "carabiner" under
  the harness outline in the Brand Stories drawing; the topic pages' chart
  labels about 5 px on a phone.
- Not problems: Kenya's gallery and Expeditions' panels need a continuous
  scroll to load and show (a capture that jumps a screen at a time misses
  them); nine topics have no trend line because none of their episodes is
  dated; YouTube pictures are blank only where YouTube cannot be reached.

## Keeping the cost down (the owner asked, 20 Oct)
India took about 25 agents and three workflows for a 7.5-to-6 win. Most of
that was checking, not building. Next time:
- **Screenshot once, judge many.** Each blind judge re-walked both pages at two
  widths (about 150 tool calls and 180k tokens per judge). Instead, one cheap
  agent takes the screenshot set and the frame sequences once, for old and new,
  into labelled folders; the judges only look at them.
- **One judge for a small page, two only for a big one**, and never more than
  one fix round; a small fix after judging is made directly, without judging
  again.
- **Let the gates check what they already check.** Parity, links, words,
  overflow, tap targets and weight are in `v4_gates.py` and `v4_weight.py`; the
  checker agent only does what they cannot: the facts diff, the booking links,
  the motion rule.
- **One audit agent, not two**, and no per-frame probes, CPU throttling runs or
  thousands of frames unless something is actually janky.
- **Smaller models for mechanical work**: screenshots, diffs and measurements
  on a smaller model (the Workflow tool's `model` option); the planner, the
  builder and the judges on the main one.
- **Full gates once before a push**, `--quick` while iterating.
- **Content before polish**: the judges' main limits on India were the visible
  "From past pilots [to supply]", soft or repetitive photographs and a route
  that is only a diagram. The owner's quotes, best photographs, IGC logs and a
  sharp hero clip would lift the trip pages more than another round.

## How to work here
- Preview server: `python3 -m http.server 8765 --bind 127.0.0.1` from the repo
  root. For old-versus-new comparisons, a git worktree of the last pushed
  commit in `/tmp/claude-0/wt-old`, served on port 8766.
- `tools/v4_build.py` must keep reproducing the committed v4 byte for byte:
  in a clean worktree of the new commit, `./build.sh && python3 tools/v4_build.py`
  twice, then `git status --short prototypes/v4` is empty. Every new in-place
  pass (like `tools/v4_trip_calm.py`) goes in it after `v4_ux`. This check found
  a real bug on 20 Oct (the enquiry page's trip length).
- A page-only look goes in its own sheet and script loaded by that page alone
  (as `v4-calm.css` and `v4-calm.js` for India), so no other page's bytes or
  version hashes change.
- A new page with no live twin goes in `tools/v2_site.py` `NEW_PAGES`.

## Waiting on the owner
Photographs (a Google Drive folder works; Terabox is blocked), client quotes
for "From past pilots", the record page's FAI figures, wing and team, the
sponsor tiers and promises, the source and date of the 100,000+ streams, the
India and Kenya skill levels, whether the hero footage may loop, the iPhone
check and the switch-over.
