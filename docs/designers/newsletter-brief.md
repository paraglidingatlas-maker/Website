# Newsletter brief (chat 22, 12 Nov 2026)

## The job, in the owner's words (12 Nov)
"I need to design a newsletter to update my subscribers of what I've been doing. After the landing pages of media are
complete, ask the 4 designers to design the newsletter." The four: designer-d (Trim), designer-e (Cloudbase),
designer-f (Turnpoint) and designer-g (the new inbox specialist).

## Owner's answers (12 Nov)
- Audience: all subscribers (28 active on MailerLite on 12 Nov; no campaign has ever been sent: this is the first).
- Send time: the owner picks later. Build a MailerLite DRAFT only. Never send, schedule or test-send.
- Voice: a mix. A short personal opener in the owner's first person (Aninder Singh), then brand-style sections
  (Paragliding Atlas).

## What it reports (facts only; a missing fact is [to supply])
Content plan proposed by chat 21 (10 Nov), to be checked against the repo and SRS/airtribune before use:
- SRS Tapalpa (SRS Advance Edition, Tapalpa, Mexico, 8 to 14 Nov 2026), the owner on the media team: the tasks so far
  (task lines from COMPS["tapalpa"]["films"] in tools/v4_comp_gallery.py; results only from airtribune), the photos
  page https://paraglidingatlas.com/media-srs-tapalpa-2026.html, the daily highlight films (YouTube ids in COMPS).
- The 2026 season's new event pages (PWC Super Final, SRS Bassano, SRS Piedrahita, Tapalpa): links on
  https://paraglidingatlas.com/media.html.
- The podcast: the Miguel Gutierrez talk ([to supply]: its episode link and date; check the repo's episode list).
- Patreon: "Like what you see? Join me on Patreon" https://www.patreon.com/15133612/join.
- If the send is after 14 Nov, the final results replace "so far" (the chat updates the draft with the owner).

## Design rules
- One column, Gmail on a phone first; real text, not text in pictures; images with alt text and the email still
  readable with images off. Photos: the owner's web copies (https://paraglidingatlas-maker.github.io/media-2026/...
  -800 or -1600.webp is not safe in all clients: use JPEG/PNG hosted in assets/email/<newsletter>/ in the site repo,
  or MailerLite's file storage; never move or delete anything in assets/email/).
- The site's look as far as email allows: dark or light, one orange (#e5600a / #ff7517), Poppins headings with a
  fallback, DM Sans text with a fallback. The welcome email (MailerLite automation "Welcome to the Atlas list",
  old copy docs/emails/welcome-atlas-list-old.html.txt; images in assets/email/welcome/) is the house style so far.
- Subject and preview line: give two options each. No em dashes. Honest footer (why you get this, unsubscribe).

## Contest round 1: what each designer delivers
docs/designers/newsletter/<D|E|F|G>-concept.md: the idea in one line, the subject and preview options, the email
from top to bottom (every block, its words, its picture), why it gets read and clicked, and what you would steal from
the others. Plus a static HTML mock at prototypes/v4/samples/newsletter-<d|e|f|g>/index.html (email-safe: tables,
inline styles, 600 px max) and shot-390.png, shot-1440.png beside it.

Do NOT use MailerLite write tools in round 1, and do NOT run ./build.sh, tools/v4_build.py, tools/v4_gates.py, git
commit or push. The chat builds the winner as the draft.
