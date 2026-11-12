# Brief: the photo viewer's controls (owner, 12 Nov 2026, chat 23)

**The owner, in their words:** "as for buttons to scroll through photos currently they are on top of the site in phone
display, I want to make them Awwwards worthy and easy for one hand operation"; then, on two attempts by chat 23 (a
row of boxes, then a glass capsule): "can we make the buttons more sleek futuristic and cool, these are just the old
boxes vibe" and "the buttons still look odd to me, ask the 3 designers to make some samples".

**What it is.** The photo viewer (lightbox) on the gallery pages, e.g. https://paraglidingatlas.com/media-srs-tapalpa-2026.html
(tap any photo). Markup: tools/v4_comp_gallery.py, the `<dialog class="gfv">` block (around line 508). Styles:
prototypes/v4/v4-gallery.css (the viewer section from ".gfv-top" around line 150, and chat 23's phone dock at the end
of the file). Behaviour: prototypes/v4/v4-gallery.js (show(), go(), swipe left/right to change photo, swipe down to
close, pinch to zoom).

**The controls to design (phone first, 390 x 844; then how it carries to desktop 1440 x 900):**
- previous / next photo, and where you are ("21 of 144" in a task; a sense of progress through the task is welcome)
- close
- Download: the free web copy (a JPEG, long edge 2400 px). The owner wants the button to say Download and show the
  photo's resolution and file size (e.g. "1600 × 2400 px · 1.4 MB"; size known once the file is fetched)
- Share (opens the phone's share sheet; prototypes/v4/v4-share.js)
- "Like what you see? Join me on Patreon" (keep it; it is the owner's support link)
- the photo's name (SRS_6_T3_21), its task and date ("Task 3 · Tue 10 Nov"), and the licence line (CC BY-NC 4.0, the
  credit) can be quieter, but must stay reachable

**Must.** One-handed: everything a thumb uses sits in the bottom third of a phone. Targets at least 44 px. The photo
stays the hero (do not cover it more than the current footer does). The site's look: dark ground, one orange
(#ff7517), Poppins headings (font-family var(--font-display)), DM Sans text. Works with reduced motion. No new fonts or
libraries. Nothing invented: no fake counts, sizes or names beyond the example values above.

**Deliver.** One self-contained sample page: prototypes/v4/samples/viewer-<your letter>/index.html (inline CSS and a
little JS; it may link ../../v2.css and ../../v4-gallery.css if useful, but must look right on its own). Use a real
photo: https://paraglidingatlas-maker.github.io/media-2026/srs-tapalpa/SRS_6_T3_21-1600.webp (portrait 1600 x 2400)
and, for a landscape check, https://paraglidingatlas-maker.github.io/media-2026/srs-tapalpa/SRS_6_T4_54-1600.webp
(1600 x 1135). Show the viewer open, with working prev/next between the two photos, the pressed states, and the
Download button in its three states (ready with resolution, getting it, saved). Add a 5-line note at the top of the
file: the idea in one sentence, why it suits one hand, what it borrows. Write a short entry in your notebook
docs/designers/<letter>.md. Touch no other file; do not commit.
