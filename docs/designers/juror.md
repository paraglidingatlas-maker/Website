# The Juror's notebook (newest first)

The Juror (`.claude/agents/awwwards-juror.md`) scores built previews blind
against the Awwwards criteria. Called only after the owner has agreed to the
predicted time and cost of that review (owner, 24 Oct 2026).

## 24 Oct 2026, review 1: v4 before (48bfc475) against v4 now
Owner agreed to the estimate (10 to 15 min, 200k to 300k tokens): "Yes".
Judged home, expeditions, Kenya, podcast, knowledge base, the Panchgani
episode, about (and the new Panchgani page) at 1440x900 and 390x844; home
also with reduced motion and without JavaScript. Full write-up:
scratchpad `designers/juror-1.md`.

| | Design | Usability | Creativity | Content | Total |
|---|---|---|---|---|---|
| v4 before | 7.4 | 7.0 | 6.8 | 7.2 | 7.14 |
| v4 now | 8.2 | 7.3 | 8.3 | 7.0 | 7.83 |

Top three faults now:
1. Home, phone: the headline sits below the first screen and the trip panel
   fades to black on scroll, so it is never read. Headline under the name;
   hold the fade.
2. `[to supply]` on public pages (Kenya launch in the hero; Panchgani launch,
   price, group, rating). Owner supplies facts; hide empty fields meanwhile.
3. Home tells Kenya twice (opening, then the chapters) and lost "Find your
   expedition". Let the opening replace the chapters; one button to all trips.
