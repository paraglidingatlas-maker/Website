# Newsletter, contest round 1: designer E (Cloudbase), "Pull Back to the Season"

Mock: `prototypes/v4/samples/newsletter-e/index.html` (shot-390.png, shot-1440.png beside it). Facts as of 12 Nov 2026.

## The idea in one line
The email is one camera pulling back as you scroll: one pilot close up, then the race, then the valley, then the
whole season, with a small four-step zoom meter that fills in orange at each frame.

## Subject and preview (two each, no em dashes)
- Subject A (recommended): **Tapalpa so far: four tasks, one storm, nobody in goal**
- Subject B: **Notes from Tapalpa, Mexico**
- Preview A (recommended): **Photos from every task, the nightly films, and a local pilot on how to fly Tapalpa.**
- Preview B: **My first newsletter, written from the media team at SRS Tapalpa.**

A is a story with a turn in it (a storm, then nobody in goal) and every word is a fact from airtribune. B is the
safe, personal one. If the send is after 14 Nov, A becomes "Tapalpa, all seven tasks: [winner] takes it" once the
final results are in.

## The email, top to bottom
Dark ground (#0e0f12 outside, #141519 card), one orange (#ff7517 for kickers, links and the meter; #e5600a for the
one button), Poppins headings and DM Sans text from Google Fonts with Arial fallbacks. One column, 600 px max,
tables and inline styles; all words are live text; every picture has alt text and a dark fill behind it.

1. **Masthead.** A 3 px orange hairline (as the old welcome email), the white Atlas logo
   (assets/logo/atlas-logo-white.png), "Field notes · Nov 2026" on the right.
2. **Frame 01, Close.** Full width photo SRS_6_T4_94 (a pilot waving from a black pod harness, Task 4), cropped 3:2,
   links to the Tapalpa photos page. Caption "Task 4, Wed 11 Nov. Photo SRS_6_T4_94." and the zoom meter (1 of 4 lit).
   Then the owner's opener: "Hey fellow pilot," (the welcome letter's greeting); "This is my first newsletter, and I am
   writing it from Tapalpa, Mexico. I am on the media team at the SRS Advance Edition, 8 to 14 Nov: photos of every
   task each evening and a highlights film each night."; **[to supply: one or two lines in your own words about the
   week]**; "Here is the week so far, starting with one pilot and pulling back to the whole season."
3. **Frame 02, The race** (meter 2 of 4). "Tapalpa so far", "116 pilots, 44 countries, 7 tasks planned. Four flown."
   Four task rows, a 132 px photo left, words right (stays a row on a phone):
   - Task 1 · Sun 8 Nov · 59.1 km. "Matthijs Groeneveld (NLD) won it. 26 pilots in goal." Watch the film, 4:48
     (ZTxWnsHeUmE). Photo SRS_6_T1_55.
   - Task 2 · Mon 9 Nov · 41.3 km. "Raced under a storm clock, stopped by rain at 14:40. Arnold Castro (ARG) was the
     only pilot home." Watch the film, 4:36 (MXt0RJgXNs4). Photo SRS_6_T2_44.
   - Task 3 · Tue 10 Nov · 58.7 km. "Abel Varga (HUN) won it. 88 pilots in goal." Watch the film, 6:41
     (bB1TaxIN8Oo). Photo SRS_6_T3_141.
   - Task 4 · Wed 11 Nov · 82.4 km. "The longest task, and nobody made goal. Brian Duffy (USA) flew furthest,
     65.6 km." Film [to supply]. Photo SRS_6_T4_150.
   - Standings, an orange left rule: "After four tasks: Andrés Tello Alvarado (MEX) leads, Bill Belcourt (USA) is
     second, Chaeden Luebberke (USA) third." Small: "Sports class, provisional. Full results on Airtribune. Bill was on
     the podcast last year: the safety paradox." (YyGdTDXC1Lc, 29 Oct 2025).
   - The one button: **See every photo, free to save** → media-srs-tapalpa-2026.html; under it "484 photos so far, by
     task. Find your wing."
4. **Frame 03, The valley** (meter 3 of 4). Full width photo SRS_6_T1_62 (a yellow wing over the lake bed and the
   white greenhouses, the widest view in the set), links to the talk. "How to fly Tapalpa": "Miguel Gutiérrez
   explains flying in Tapalpa: the airspace, local flying, the thermals and what you need to know to fly this
   Mexican paradise." (the video's own description) Watch the talk, 53 min (yhHoRUJtyOY, published 10 Nov 2026).
5. **Frame 04, The season** (meter 4 of 4). "Four events, one season": "Tapalpa is the fourth event I have covered
   this season. Each one has its own page: the photos, films or broadcasts, by task." The site's season line drawn
   in table cells (no picture, so it shows with images off): May Bassano (SRS, live broadcasts), May Pegalajar
   (PWC Super Final, films), Aug Piedrahita (SRS, photos and films), Nov · Now Tapalpa (the orange segment). Each
   links to its event page. "The whole season on the Media page →".
6. **Patreon**, a quiet panel: "Like what you see?" "Join me on Patreon: a weekly newsletter on flight safety, behind
   the scenes of the production and audio clips never released before." (the owner's own Patreon line from the
   YouTube descriptions) → patreon.com/15133612/join.
7. **Sign-off.** The owner's portrait (assets/email/portrait.png), "See you up there, Aninder" (the welcome's
   words), "Questions for the show? Send them to aninder@paraglidingatlas.com."
8. **Footer.** "Touch The Sky With Glory"; "You get this because you joined the Atlas list on paraglidingatlas.com.
   Paragliding Atlas, [to supply: postal address]." Unsubscribe ({$unsubscribe}) · Update your details
   ({$preferences}) · paraglidingatlas.com.

## Why it gets read and clicked
- The first screen on a phone is a person, not a logo or a headline: a pilot waving at the camera. Then the
  owner's own voice. That is the reason to keep scrolling.
- Each frame is wider than the last, and the meter shows it. The reader always knows where they are and that the
  email ends after four steps: no "how long is this?".
- Four task rows are four stories in one line each (a win, a storm, a full goal, an empty goal), each with its own
  film link: four chances to click, all to the owner's YouTube.
- One button only (the photos page), where a pilot who flew Tapalpa wants to go: to find their own wing.
- The Bill Belcourt line ties the race to the podcast with a fact, not a pitch.
- The season line is the site's own grammar (home page and event pages), so the email reads as the Atlas, not a
  template.

## What it costs to build
Six JPEGs (in the mock's img/; 4 to 140 KB, about 210 KB in all) to host at assets/email/newsletter-2026-11/ (a new
folder; nothing in assets/email/ moves) or in MailerLite's file storage. The zoom meter is four table cells per
frame. In MailerLite's simple editor the meter and the season line need a custom HTML block.

## What I would steal from the others
Not read (worked alone, as asked). What I would look for: G's inbox know-how on Gmail clipping, dark-mode
inversion and Outlook (my meter and season line depend on table cells rendering their fill); D's eye for the
smallest honest fact; F's season line if it is drawn better than mine.

## Facts and flags
- All results are airtribune's PROVISIONAL Sports class (api.airtribune.com/srs/scores, meet 93), read 12 Nov.
  Goal counts are my count of finish times in each task table: T1 26, T2 1, T3 88, T4 0.
- The Task 4 film is not on YouTube yet: [to supply].
- The Miguel talk is on YouTube only as far as the repo shows; its episode page or podcast-feed link: [to supply].
  Its YouTube title spells "Maxico".
- media-pwc-pegalajar-2026.html and media-srs-bassano-2026.html return 404 on paraglidingatlas.com today (on the
  branch, not pushed). They must be live before the send, or those two link to media.html.
- The welcome email promised "about four emails a month"; this is the first ever sent.
- Postal address for the footer: [to supply] (MailerLite may add the account's own).
- The opener is written in the present ("I am writing it from Tapalpa"); after 14 Nov it becomes the past tense
  and "so far" becomes the final results.
