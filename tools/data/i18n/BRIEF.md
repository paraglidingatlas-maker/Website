# Brief for every translation pass (tools/v4_i18n.py)

The site is paraglidingatlas.com: a paragliding podcast, a knowledge base, guided paragliding expeditions
(Kenya, India, Panchgani, Kazakhstan, Peru) and photo/film coverage of paragliding competitions (SRS,
Paragliding World Cup). Readers: paragliding pilots and locals near the flying sites. Tone: warm, plain,
precise, written by a pilot; never salesy, never invented.

## The segments
Each segment is a piece of the English page with its facts locked:
- `{1}`, `{2}` ... are locked facts (numbers, dates, prices, names, URLs). Keep every one, exactly once,
  unchanged (`{3}` stays `{3}`). Move them where the grammar of your language needs them. Never write a
  number, date or price yourself: there is no digit in your translation that is not inside a `{n}`.
- `<x1>`...`</x1>` and `<x2/>` are the page's markup (links, bold, line breaks). Keep each one, properly
  nested; you may move them so they wrap the right words.
- `[to supply]` is never translated (it is a locked fact too).
- "where" says which page and whether it is an attribute (an image description, a button label, a search
  snippet). Segments are short UI labels as often as sentences: translate a label as a label.

## Rules
1. Nothing invented, nothing dropped, nothing softened or strengthened. Same meaning, same facts, same
   promises. If the English is unclear, translate what it says and note it.
2. Names stay as written: people (pilots, guests), companies, brands, glider models, competitions
   (Paragliding World Cup, SRS - Advance Edition), the site's name (Paragliding Atlas), local place names
   (Tapalpa, Panchgani, Bir Billing, Kerio Valley ...). Countries ARE translated, with the standard name
   (Kenya -> Kenia (de), Kenya (fr), Kenia (es), 肯尼亚 (zh)). "Organisasjonsnummer" (Norwegian) stays.
3. Paragliding terms: use what pilots who speak the language actually say, as their federation uses it
   (German: DHV; French: FFVL; Spanish: RFAE/FMVL usage; Chinese: 中国航空运动协会 usage). The glossary
   tools/data/i18n/glossary.json, where present, is binding.
4. Headings: the English uses Title Case. Use your language's own convention (German: normal noun
   capitalisation; French, Spanish: sentence case; Chinese: no case).
5. Address the reader (a style choice, chat 27; the owner may change it): German "du"; French "vous";
   Spanish "tú"; Chinese 你.
6. Keep it short where the English is short: labels must fit the same buttons. Chinese: Simplified
   characters, full-width punctuation (，。：), no space between Chinese and a `{n}` unless the English had
   a unit word after it.
7. Units stay metric as in the English (km, m, m/s, h).

## Output
A JSON object: segment key -> translation string, for every key you were given, nothing else.

## The reviewer (third pass)
Input: `work/<lang>-review.json`: per key the English (`en`), where it is, what each `{n}` stands for
(`facts`), and two independent translations `a` and `b`. For each key write the final translation `tr`:
- pick the better of a and b, or merge them, or correct both. Better = same meaning as the English (nothing
  added, dropped, softened), natural to a native pilot, right paragliding term, consistent with the rest
  of the site (the same English label gets the same translation everywhere: check across keys).
- Use `facts` to fix grammar the translators guessed (gender, articles, prepositions around a `{n}`).
- Glossary (`glossary.json`, when it exists) is binding for sourced terms.
- Names stay: people, brands, glider models, competitions, local places. Episode titles and taglines are
  translated (the reader needs to understand them); the series name "Navigators" stays.
- A soft check you overrule on purpose (a person's name "left in English"; "India" inside an organisation's
  own name) goes in `waive` with the reason. Never game a check (no invisible characters, no added words
  to satisfy it).
Output `work/<lang>-tr.json`: `{"key": {"tr": "...", "note": "why, when you changed or merged", "waive":
{...}}}` for every key. Then `python3 tools/v4_i18n.py validate <lang> work/<lang>-tr.json
work/all-segments.json` must show no hard problem (tokens, markup, digit, brace, language).

## The comparer (fifth pass)
Input `work/<lang>-compare.json`: per key the English (`en`, with `facts`), the published `translation`, and
`back`, a blind back-translation of it into English by someone who never saw the English. Decide for each
key whether the translation says what the English says:
- "ok": same meaning, same facts, same promises, same tone. Wording, word order, idiom and an obvious
  back-translation slip do not matter (check the translation itself when back looks off).
- otherwise a short reason: what shifted (added, dropped, stronger, weaker, wrong referent, wrong sense of
  a word, wrong grammar around a `{n}`, a wrong paragliding term, reads as a different kind of label).
  Then also give `fix`: your corrected translation (keep every `{n}` and `<xN>`).
Be strict on meaning and facts, lenient on style. Output `work/<lang>-check.json`:
`{"key": {"verdict": "ok"}}` or `{"key": {"verdict": "<reason>", "fix": "..."}}` for every key.
