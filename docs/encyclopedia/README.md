# Encyclopedia: handoff

One page per question people actually ask about paragliding, answered in plain
language from open sources, then what the guests on the show add, linked to the
chapter where they say it. Plus an A to Z of every question the knowledge base
answers, including the ten FAQ answers on each series page.

Why: the series pages answer the questions guests raise. Nobody answered the
questions people type into Google or ask ChatGPT ("how does a paraglider fly",
"what does EN B mean"). A rewritten copy of a manual gives an answer engine no
reason to cite this site; a clear, sourced answer joined to primary-source
interviews nobody else has does.

## Where things live

| What | Where |
|---|---|
| Content, one dict per question | `kb_answers.py` |
| Generator (pages and A to Z) | `generate_answer_pages.py`, run by `build.sh` after `generate_kb_pages.py` |
| Answer-page and A to Z styles | `templates/kb/answer.css` (on top of `templates/kb/category.css`) |
| Output | `knowledge-base/encyclopedia/<slug>.html`, `knowledge-base/encyclopedia/index.html` |
| New drawings | `tools/kbfig/enc_*.py` -> `assets/images/kb-enc-*.jpg` + `.webp` |
| Question bank (245 questions, demand estimates) | `docs/encyclopedia/question-bank.csv`, notes in `question-bank-notes.md` |
| Source dossiers (verbatim excerpts per source) | `docs/encyclopedia/sources-*.md` |
| Independent fact-check of the pilot | `docs/encyclopedia/factcheck-pilot.md` |

Series pages list the published answers filed under them ("Answered in depth",
`kb_layout.in_depth`) with a link to the A to Z. Every FAQ answer on a series or
landing page now has a stable id (`kb_layout.faq_id`), and `category.js` opens
the answer when a link lands on it, which is how the A to Z links into them.

## Status

| Batch | Entries | Status |
|---|---|---|
| Pilot: Flight Mechanics | 10 | draft, awaiting Aninder's review |

## Draft and published

`"status": "draft"` renders the page with `noindex`, leaves it out of the A to
Z, the series page strip, the sitemap and llms.txt, and shows a "Draft for
review" badge. The A to Z itself stays `noindex` until at least one answer is
published. So drafts can sit on the live site at their real URLs without being
indexed or linked.

To publish an entry: set `"status": "published"` and `"reviewed": "YYYY-MM-DD"`,
then `./check.sh`. The build refuses a published entry without a reviewed date.

Review build, with drafts listed everywhere (for screenshots or a prototype, not
for pushing): `ENC_SHOW_DRAFTS=1 ./build.sh`, then rebuild normally before any commit.

## Making a batch

1. **Pick questions** from `question-bank.csv`: high demand first, and only
   where the show has something real to add. Avoid repeating a series-page FAQ;
   link to it instead.
2. **Source dossier.** For each question, collect facts with a verbatim excerpt
   under 40 words, title, publisher, URL and licence, into
   `docs/encyclopedia/sources-<batch>.md`. Prefer US government works (FAA
   handbooks, NASA Glenn, NOAA), then federations and test houses (DHV, SHV,
   Air Turquoise, CIVL), then manufacturer manuals, then Wikipedia for facts
   only. Note disagreements between sources; they usually become the most
   useful sentence on the page.
3. **Read the chapters.** Extract chapter text from `episodes/*.html`
   (`div.cd-block`), grep for the topic, read the hits in full. Captions
   mislabel speakers; when it is unclear who said something, leave it out.
4. **Write the entry** in `kb_answers.py`, copying the shape of an existing one.
   Rules are in the module docstring. The ones that matter most: short answer
   first and self-contained (35 to 80 words, no citations); every factual
   sentence cites [n]; arithmetic is called a worked example; guest cards are
   paraphrases with the chapter; safety pages set `"safety": True` and defer to
   the pilot's own manual; no em-dashes.
5. **Build and check:** `./check.sh` must say all three gates clean. The
   generator also fails on a dead citation, an unused source, a missing chapter,
   a missing image, an unknown related link, an over-long title.
6. **Fact-check with a separate agent** that has not seen the writing: give it
   `kb_answers.py`, the dossiers and the chapter text, and ask for HIGH, MEDIUM
   and LOW findings. Fix every HIGH and MEDIUM. The pilot's report is the
   example (`factcheck-pilot.md`).
7. **Review** by Aninder, then publish as above.

## Known gaps and follow-ups

- No search-volume data yet: vidIQ had no credits and Google's "People also
  ask" did not come through search. The Search Console query export (calendar
  reminder, Tue 20 Oct 2026) is the first real check on the bank's ratings.
- The A to Z groups the series FAQs by keyword rules (`TOPIC_RULES` in the
  generator). Check new FAQs land in a sensible topic; "More questions" should
  stay empty.
- The knowledge base hub (`knowledge-base.html`) does not link to the A to Z
  yet. That page is hand-designed, so the link is Aninder's call.
- Most big brands publish no speed, sink or glide figures; the speed and glide
  pages lean on Mac Para's tables. Swap in independent measurements if any
  appear.
