# Designer G (newsletter, inbox): notebook (newest first)

## 12 Nov 2026: built F's "The Task Line" as the MailerLite draft
Asked (chat 22): build the winner (F, verdict in direction.md: "Taken from G: the inbox craft ... and G builds the
MailerLite draft"; "Taken from D: one solid orange button only (the photos)") as ONE draft campaign; never send.
Built: campaign 203910238840031114 "Newsletter 01 · Tapalpa (draft, chat 22)", email 203910238857856907, subject
"Four tasks into Tapalpa", preview line as a hidden first div, sender "Aninder, Paragliding Atlas"
<aninder@paraglidingatlas.com> (the Kenya and India drafts' sender; no API for "the default"). Audience: none set,
so MailerLite counts all active subscribers (28). Nothing sent, scheduled or tested.
Editor: custom HTML (create_campaign content), not the simple editor. Why: the simple editor's blocks are single
column only (paragraph, heading, image, button, list, divider, code ...), no table or HTML block, and it has no
preheader field, so the readout, the season line, the task rows with their 104 px photos and the standings would all
break into stacked blocks. Cost: get_email_html refuses non-simple emails, so the read-back came from the campaign
record (fetch); later edits go through update_campaign content, not the block tools.
Changes from F's mock: absolute image URLs (assets/email/newsletter-2026-11/, 404 until the push to main); logo =
assets/logo/atlas-logo-white.png, as the welcome emails use (atlas-mark-dark.png is black letters for light
signatures, invisible on the dark ground); opener boxed "[DRAFT WORDS ...]"; Miguel's line starts with an orange
"[to supply: who Miguel Gutiérrez is]"; Task 4 "Film [to supply]" and "postal address [to supply]" in orange; the
practice-day credit is "@paco_peciado" (the gallery gives a handle, F's "Paco Peciado" was a guess); a "{$url}"
browser link in the footer; the longer preview padding. One solid button only, as in F (Patreon is an outline).
Files: docs/emails/newsletter-01-tapalpa.html.txt (stored HTML, 28.7 KB); renders 390, 600 and 390 images-off in
chat 22's scratchpad (pictures served from the repo copies).
Open for the owner: rewrite the opener; Task 4 film; who Miguel is; postal address; the "12 Nov" dateline and
"4 of 7" go stale if the send is after 14 Nov; PWC and Bassano pages still 404 live; the plain-text part is
MailerLite's generic one; dark mode in Gmail on iPhone not yet seen on a real phone (needs a test send, owner's yes).

## 12 Nov 2026: newsletter contest round 1
Asked (chat 22): the first subscriber newsletter, round 1 per docs/designers/newsletter-brief.md; concept
docs/designers/newsletter/G-concept.md, mock prototypes/v4/samples/newsletter-g/ (plus an images-off shot).
Proposed "The Letter From the Field": the owner's live-text opener ("Hey fellow pilot," and a "TAPALPA · MEXICO"
dateline, the welcome letter's grammar), one photo (the gallery cover SRS_6_T1_62), the results as an HTML table
(4 tasks, overall top 3, first woman; airtribune provisional on 12 Nov), three film rows with same-task posters, the
Miguel Gutiérrez talk as words only, the season list, Patreon, an honest footer. Two orange buttons in all.
Recommended subject "From the media team at Tapalpa" (personal, fits a phone), because it is the list's first email.
Facts checked: airtribune meet=93 tasks 344 to 347 and the overall; YouTube (vidIQ): the talk yhHoRUJtyOY, 53:23,
published 10 Nov UTC; no Task 4 film yet. Flags: PWC and Bassano pages 404 live; the live welcome is a letter set as
one image; "Maxico" in the talk's title; postal address [to supply]. Not done: MailerLite (round 1 forbids writes).

## 12 Nov 2026: created
Added by website chat 22 at the owner's request ("4 designers" = a new fourth designer). First job: the subscriber newsletter (all subscribers, send time chosen later by the owner, voice: a personal opener from the owner, then brand-style sections).
