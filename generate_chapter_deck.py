#!/usr/bin/env python3
"""
Build individual episode pages in the agreed "Chapter Deck" format.

Inputs
------
transcripts/<slug>.vtt   WebVTT from Whisper, with [SPEAKER_NN] diarisation tags.
episode-meta.json        One entry per episode: title, guest, dates, chapters, etc.
library-data.js          Reused for the series each episode belongs to.

Output
------
episodes/<slug>.html     Uses episodes/episode.css. That file was lifted verbatim
                         from prototypes/episode-page-chapter-deck-FINAL.html,
                         which was deleted on 2026-09-11 along with the rest of
                         prototypes/ (six unaudited, crawlable orphan pages).
                         episode.css is now the single source for this design;
                         the old prototype is in git history before that commit.

Chapters
--------
Chapter titles come from the episode's own show notes (the bullet list the host
already writes for every episode). Each chapter carries a `cue`: a short phrase
spoken in the episode. The generator finds that phrase in the transcript and
takes its timestamp, so the timings are real rather than estimated. A chapter can
instead carry an explicit `at` timestamp to override the search.

Run: python3 generate_chapter_deck.py [slug ...]
"""

import html
import json
import os
from urllib.parse import unquote
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_config as cfg

ROOT = os.path.dirname(os.path.abspath(__file__))

# Subtle pulse on clickable tags. Trialled on one page and rolled out site wide
# by the user on 2026-09-11, after being softened once.
#   set to "all"      -> every episode page
#   set to a set()    -> just those slugs
#   set to an empty set -> off everywhere, and the CSS becomes dead weight
# The styling lives in tags.css under .cd-tags.tag-pulse.
TAG_PULSE_ON = "all"
TX = os.path.join(ROOT, "transcripts")
OUT = os.path.join(ROOT, "episodes")

CUE = re.compile(
    r"^(?P<s>\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s*-->\s*"
    r"(?P<e>\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s*(?P<rest>.*)$"
)
SPK = re.compile(r"^\[?SPEAKER[ _]?(?P<n>\d+)\]?\s*:\s*", re.I)
NOISE = re.compile(r"^\[.*(automatic caption|whisper|recognition error).*\]$", re.I)
# Autotekst writes its disclaimer INSIDE the first cue's text on 32 of the 52
# transcripts, so NOISE never matched it (NOISE only catches a cue that is
# nothing but the note) and it was being served mid sentence. It is a machine
# annotation, not speech, so it is stripped here and re-emitted once per page as
# a proper element by note_html(), which also covers the 20 files that never
# carried it and the transcripts sourced from Spotify.
NOTE_INLINE = re.compile(r"\[\s*Automatic captions[^\]]*\]\s*", re.I)


# ---------------------------------------------------------------- parsing

def secs(stamp):
    stamp = stamp.replace(",", ".")
    bits = [float(b) for b in stamp.split(":")]
    while len(bits) < 3:
        bits.insert(0, 0.0)
    return bits[0] * 3600 + bits[1] * 60 + bits[2]


def clock(s):
    s = int(s)
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return "%d:%02d:%02d" % (h, m, sec) if h else "%02d:%02d" % (m, sec)


def parse_vtt(path):
    """Return a list of {start, speaker, text} cues."""
    cues, pending = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = CUE.match(line.strip())
        if m:
            if pending:
                cues.append(pending)
            rest = m.group("rest").strip()
            spk = None
            sm = SPK.match(rest)
            if sm:
                spk = int(sm.group("n"))
                rest = rest[sm.end():]
            pending = {"start": secs(m.group("s")), "end": secs(m.group("e")),
                       "speaker": spk, "text": rest}
            continue
        if pending is None or not line.strip():
            continue
        if line.strip().upper() == "WEBVTT" or line.strip().isdigit():
            continue
        extra = line.strip()
        sm = SPK.match(extra)
        if sm:
            if pending["speaker"] is None:
                pending["speaker"] = int(sm.group("n"))
            extra = extra[sm.end():]
        pending["text"] = (pending["text"] + " " + extra).strip()
    if pending:
        cues.append(pending)
    for c in cues:
        c["text"] = NOTE_INLINE.sub("", c["text"]).strip()
    return [c for c in cues if c["text"] and not NOISE.match(c["text"])]


def paragraphs(cues, gap=2.5, max_words=110):
    """Merge cues into readable paragraphs, breaking on speaker change or a pause."""
    out, cur = [], None
    for c in cues:
        new = (
            cur is None
            or c["speaker"] != cur["speaker"]
            or c["start"] - cur["end"] > gap
            or len(cur["text"].split()) > max_words
        )
        if new:
            if cur:
                out.append(cur)
            cur = {"start": c["start"], "end": c["end"], "speaker": c["speaker"], "text": c["text"]}
        else:
            cur["text"] += " " + c["text"]
        cur["end"] = c.get("end", c["start"])
    if cur:
        out.append(cur)
    return out


# ---------------------------------------------------------------- chapters

def norm(t):
    return re.sub(r"[^a-z0-9 ]+", " ", t.lower()).strip()


def locate(cue_phrase, cues):
    """Find the timestamp where a phrase from the show notes is spoken."""
    want = norm(cue_phrase)
    if not want:
        return None
    words = want.split()
    joined, index = [], []
    for c in cues:
        for w in norm(c["text"]).split():
            joined.append(w)
            index.append(c["start"])
    best, at = 0.0, None
    for i in range(len(joined) - len(words) + 1):
        window = joined[i:i + len(words)]
        hit = sum(1 for a, b in zip(window, words) if a == b) / len(words)
        if hit > best:
            best, at = hit, index[i]
    return at if best >= 0.7 else None


def resolve_chapters(meta, cues):
    """Attach a real timestamp to every chapter. Returns (chapters, warnings)."""
    chapters, warn = [], []
    for n, ch in enumerate(meta.get("chapters", [])):
        at = None
        if ch.get("at"):
            at = secs(ch["at"] if ch["at"].count(":") >= 2 else "00:" + ch["at"])
        elif ch.get("cue"):
            at = locate(ch["cue"], cues)
            if at is None:
                warn.append("could not place chapter %r using cue %r" % (ch["title"], ch["cue"]))
        if at is None:
            at = 0.0 if n == 0 else None
        if at is None:
            continue
        chapters.append({"title": ch["title"], "at": at})
    chapters.sort(key=lambda c: c["at"])
    if chapters and chapters[0]["at"] > 1:
        chapters.insert(0, {"title": meta.get("opening", "Introduction"), "at": 0.0})
    return chapters, warn


# ---------------------------------------------------------------- rendering

def esc(t):
    return html.escape(str(t), quote=True)


def render_transcript(paras, chapters, speakers):
    """Group paragraphs under their chapter so the rail can scrollspy them.

    Block structure matches the agreed prototype exactly:
        <div class="cd-block" id="cN">
          <h2>Chapter title</h2>
          <p class="cd-block-time">MM:SS</p>
          <div class="cd-line">
            <span class="cd-ts">MM:SS</span>
            <p><span class="cd-spk">Name:</span> text</p>
          </div>
        </div>
    .cd-line is a two column grid, so both cells are always emitted.
    """
    blocks, out = [], []
    if not paras:
        return ('      <div class="cd-block"><p class="cd-line"><span class="cd-ts"></span>'
                '<p>A transcript for this episode has not been produced yet. '
                'The full conversation is in the player above.</p></p></div>')
    if not chapters:
        chapters = [{"title": "Transcript", "at": 0.0}]
    # The first chapter's boundary is clamped to zero. Authored chapter times
    # are rounded to the nearest second, so a first chapter at 00:04 used to
    # exclude every paragraph starting before 4.0s, and those paragraphs were
    # dropped from the page entirely rather than appearing anywhere. The rail
    # still linked to the block that was never emitted, leaving a dead #c1.
    bounds = [c["at"] for c in chapters] + [float("inf")]
    bounds[0] = 0.0
    for n, ch in enumerate(chapters):
        inside = [p for p in paras if bounds[n] <= p["start"] < bounds[n + 1]]
        if inside:
            blocks.append((n + 1, ch, inside))
    for cid, ch, inside in blocks:
        lines, last = [], object()
        for p in inside:
            who = speakers.get(str(p["speaker"]), speakers.get("default", ""))
            spk = ('<span class="cd-spk">%s:</span> ' % esc(who)
                   if who and p["speaker"] != last else "")
            last = p["speaker"]
            lines.append(
                '        <div class="cd-line">\n'
                '          <span class="cd-ts">%s</span>\n'
                '          <p>%s%s</p>\n'
                '        </div>' % (clock(p["start"]), spk, esc(p["text"])))
        out.append(
            '      <div class="cd-block" id="c%d">\n'
            '        <h2>%s</h2>\n'
            '        <p class="cd-block-time">%s</p>\n%s\n      </div>'
            % (cid, esc(ch["title"]), clock(ch["at"]), "\n".join(lines)))
    return "\n".join(out)


def chapters_with_content(paras, chapters):
    """Chapters that will actually render a block.

    The rail and the transcript must agree, or the rail links to an id that was
    never emitted. Anything empty is dropped from both rather than left dangling.
    """
    if not paras or not chapters:
        return list(chapters)
    bounds = [c["at"] for c in chapters] + [float("inf")]
    bounds[0] = 0.0
    keep = []
    for n, ch in enumerate(chapters):
        if any(bounds[n] <= p["start"] < bounds[n + 1] for p in paras):
            keep.append(ch)
    return keep


def render_rail(chapters):
    if not chapters:
        return '      <p class="cd-rail-none">No transcript for this episode yet.</p>'
    return "\n".join(
        '      <a class="cd-chap%s" href="#c%d">%s<time>%s</time></a>'
        % (" active" if n == 0 else "", n + 1, esc(c["title"]), clock(c["at"]))
        for n, c in enumerate(chapters)
    )


def transcript_expected(meta):
    """Whether this page should carry a Chapters rail and a Transcript section.

    Default TRUE. An episode with no transcript yet still shows both, with a
    "not produced yet" line, because one may arrive: AMA #1 and the Urs Haari
    reserve question are both real conversations still waiting on Autotekst.

    FALSE is set per episode in episode-meta.json on the 13 pages that are not
    conversations at all: 8 competition highlight reels and 5 Oslo and Norway
    cinematics plus the show trailer. There is nothing to transcribe, so an
    empty Chapters rail and a "no transcript" line were furniture advertising an
    absence. User's instruction, 2026-09-11.

    Note "A Note of Thanks" is deliberately NOT in that set. It looks like
    housekeeping but carries a real 1,289 word transcript and 3 chapters.
    """
    return meta.get("transcript_expected", True) is not False


def rail_block_html(meta, chapters):
    """The sticky Chapters rail. Rendered EMPTY, never removed.

    `.cd-main` is a three column grid, 250px / 1fr / 290px, and grid children
    are auto placed in document order. Removing this aside therefore does not
    leave a gap: it promotes the player into column one and shifts every element
    on the page. That was shipped on 2026-09-11 and was wrong.

    The user asked for the SECTIONS to go and the space to stay. So on reels and
    cinematics this returns the same empty <aside>, holding its column open, with
    no heading and no list inside it. Every other element keeps its exact
    position. Do not "tidy" this into a return of "".
    """
    if not transcript_expected(meta):
        return '    <aside class="cd-rail"></aside>\n'
    return ('    <aside class="cd-rail" aria-label="Episode chapters">\n'
            '      <p class="cd-rail-title">Chapters</p>\n'
            '%s\n'
            '    </aside>\n' % render_rail(chapters))


def transcript_block_html(meta, transcript_html):
    """The Full Transcript heading and body, or nothing.

    Guarded: if an episode is flagged as having no transcript expected but a
    VTT actually exists for it, that is a data mistake and dropping the section
    would hide real content, so the build stops instead. This guard exists
    because "A Note of Thanks" was nearly flagged by mistake and it holds 1,289
    words.
    """
    if not transcript_expected(meta):
        vtt = os.path.join(ROOT, "transcripts", "%s.vtt" % meta.get("slug", ""))
        if os.path.exists(vtt) or (meta.get("chapters") or []):
            raise SystemExit(
                "transcript_block_html: %s is flagged transcript_expected=false "
                "but has a transcript file or chapters. Dropping the section "
                "would hide real content. Remove the flag." % meta.get("slug", "?"))
        return ""
    return ('      <p class="cd-sec-head">Full Transcript</p>\n'
            '%s\n' % transcript_html)


def guest_box_html(meta):
    """The sidebar "The Guest" card, or nothing at all.

    60 of 93 episode pages used to render this card with an EMPTY name and an
    empty role: a bordered box with a heading and nothing inside it. Competition
    highlight reels, the Oslo cinematics and the solo host episodes have no
    guest, so there was never anything to put there.

    The user's decision (2026-09-11): name the guest wherever one exists, credit
    Aninder Singh as himself on the five solo episodes, and DROP THE WHOLE BOX
    on the remaining 12 rather than show an empty one.

    Checked before this was written: none of those 12 carry guest_links or a
    guest_role, so hiding the box loses nothing. If an episode ever has links
    but no name, the links would vanish silently, so that case raises instead.
    """
    name = (meta.get("guest") or "").strip()
    role = (meta.get("guest_role") or "").strip()
    links = meta.get("guest_links") or []

    if not name:
        if links or role:
            raise SystemExit(
                "guest_box_html: %s has guest_links or a guest_role but no "
                "guest name. Hiding the box would silently drop them. Give it "
                "a name, or clear the links." % meta.get("slug", "?"))
        return ""

    # The user credited himself on the five solo episodes, where "The Guest" is
    # simply wrong. Compared against site_config.FOUNDER rather than a literal
    # string here, so the two can never drift apart. User's call, 2026-09-11.
    heading = "The Host" if name == cfg.FOUNDER else "The Guest"

    return (
        '      <div class="cd-box">\n'
        '        <h2>%s</h2>\n'
        '        <div class="cd-guest-row">\n'
        '          <div>\n'
        '            <p class="cd-guest-name">%s</p>\n'
        '            <p class="cd-guest-role">%s</p>\n'
        '          </div>\n'
        '        </div>\n'
        '%s\n'
        '      </div>\n' % (heading, esc(name), esc(role), render_list(links))
    )


def render_list(items, cls="cd-link"):
    return "\n".join(
        '        <a class="%s" href="%s" target="_blank" rel="noopener">%s</a>'
        % (cls, esc(i["url"]), esc(i["label"])) for i in items
    )


def note_html(meta):
    """One provenance line per transcript, outside the clip so it is never
    hidden by the Continue reading toggle.

    Every transcript on this site is machine produced, so every page says so.
    Without this the pages with the WEAKEST sourcing read as the most
    authoritative, because only some of the Autotekst files happened to carry
    the disclaimer in their own text. Wording follows the note Autotekst already
    writes, so this is not new phrasing.
    """
    src = (meta.get("_transcript_source") or "")
    if "Spotify" in src:
        if meta.get("_speakers_inferred"):
            # Say it plainly. These labels look identical to the diarised ones on
            # every other page, so without this line a reader cannot tell which
            # pages carry real speaker data and which carry a reading of the text.
            text = ("Automatic captions from Spotify. May contain recognition "
                    "errors. Spotify provides no speaker labels, so who is "
                    "speaking has been inferred from the conversation rather "
                    "than taken from the audio, and may be wrong in places.")
        else:
            text = ("Automatic captions from Spotify, which provides no speaker "
                    "labels, so this transcript is not attributed to a speaker. "
                    "May contain recognition errors.")
    else:
        text = ("Automatic captions by Autotekst using OpenAI Whisper V3. May "
                "contain recognition errors.")
    return '      <p class="cd-tnote">%s</p>\n' % esc(text)


def wrap_transcript(html_body, words, has_transcript, meta=None):
    """Clip the transcript visually. Every word stays in the HTML.

    This matters: search engines render JavaScript, but most AI crawlers do not.
    If the text were fetched on click they would never see it. So the full
    transcript is always in the page and the button only changes a max-height.
    display:none is avoided for the same reason.
    """
    if not has_transcript:
        return html_body
    mins = max(1, round(words / 150))
    return (
        (note_html(meta) if meta is not None else '')
        + '      <div class="cd-clip" id="transcript-body">\n'
        + html_body + '\n'
        '      </div>\n'
        '      <button class="cd-more" type="button" aria-expanded="false"\n'
        '              aria-controls="transcript-body">\n'
        '        <span class="cd-more-open">Continue reading, about %d more minutes</span>\n'
        '        <span class="cd-more-shut">Collapse the transcript</span>\n'
        '      </button>' % mins
    )


BRAND_SUFFIX = " | Paragliding Atlas"
TITLE_BUDGET = 70 - len(BRAND_SUFFIX)
_DANGLING = {"with", "and", "the", "a", "an", "of", "for", "to", "in", "on", "from",
             "how", "why", "what", "his", "her", "their", "its", "by", "at", "as", "or"}


def seo_title(title):
    """A short <title> for the search result. The h1 and og:title keep the full one.

    Podcast titles are written for a feed, where length costs nothing. A search
    result cuts at roughly 70 characters, so a 143 character title shows a
    fragment and wastes the words that would have earned the click. Nothing is
    invented here: whole colon-separated segments are kept while they fit, then
    the remaining budget is filled with real words from the next segment.
    """
    t = re.sub(r"\s+", " ", title).strip().rstrip(" |")
    if len(t) <= TITLE_BUDGET:
        return t + BRAND_SUFFIX
    segs = [x.strip() for x in re.split(r"\s*[::]\s*", t) if x.strip()]
    out, used = "", 0
    for i, seg in enumerate(segs):
        cand = (out + ": " + seg) if out else seg
        if len(cand) <= TITLE_BUDGET:
            out, used = cand, i + 1
        else:
            break
    if not out:
        out = t[:TITLE_BUDGET].rsplit(" ", 1)[0]
    else:
        rest = " ".join(segs[used:])
        if rest and TITLE_BUDGET - len(out) > 14:
            room = TITLE_BUDGET - len(out) - 2
            words = []
            for w in rest.split():
                if len(" ".join(words + [w])) > room:
                    break
                words.append(w)
            while words and words[-1].lower().strip(",.&-") in _DANGLING:
                words.pop()
            if len(words) >= 2:
                out = out + ": " + " ".join(words)
    out = out.rstrip(" ,&-:|").strip()
    while out.split() and out.split()[-1].lower() in _DANGLING:
        out = " ".join(out.split()[:-1]).rstrip(" ,&-:|")
    return out + BRAND_SUFFIX


_MP3_MAP = None


def mp3_for(slug):
    """The episode's MP3 in the podcast feed, or None.

    Read from `mp3-map.json`, which `tools/build_mp3_map.py` writes. The build
    never touches the network: if the feed were fetched here, an outage would
    silently strip the download link from every page and nothing would notice.

    NOTHING IS HOSTED HERE. The audio sits on the podcast host's CDN, where it
    already is and already serves every podcast app. This is an address, not a
    copy. 4.67 GB of audio, 0 bytes added to the repo, no bandwidth through the
    site when somebody downloads.
    """
    global _MP3_MAP
    if _MP3_MAP is None:
        path = os.path.join(ROOT, "mp3-map.json")
        try:
            with open(path, encoding="utf-8") as fh:
                _MP3_MAP = json.load(fh)
        except (OSError, ValueError):
            _MP3_MAP = {}
    return _MP3_MAP.get(slug)


def download_box_html(meta):
    """Offer the MP3, or render nothing at all.

    This replaced a "Mentioned in this episode" box that was a heading with
    NOTHING underneath it on all 93 pages, because `resources` is empty on every
    episode. A box promising content and delivering none is worse than no box.

    13 episodes have no MP3: twelve competition reels and cinematics that were
    never audio, and one snippet. They get no box, and Related episodes moves up
    to fill the space. That is safe here in a way it was not for the chapters
    rail in section 33: these are boxes stacked in normal flow inside one
    column, not columns of a grid, so removing one closes the gap rather than
    collapsing the layout.

    The heading and the link deliberately do NOT both say "Download audio". The
    heading names the thing, the link states what you get.
    """
    m = mp3_for(meta.get("slug", ""))
    if not m:
        return ""
    mb = int(round(m["bytes"] / 1048576))
    # The label states the ACTUAL format. The feed is 52 .m4a and 28 .mp3, so
    # calling everything MP3 would be wrong on two thirds of the archive, and
    # wrong in a way somebody would only discover after downloading.
    ext = re.search(r"\.([a-z0-9]{2,4})(?:\?|$)", unquote(m["url"]))
    label = {"m4a": "M4A", "mp3": "MP3"}.get(ext.group(1).lower() if ext else "", "Audio")
    return (
        '      <div class="cd-box">\n'
        '        <h2>Download audio</h2>\n'
        '        <a class="cd-dl" href="%s" download>\n'
        '          <span class="cd-dl-v">%s, %d MB</span>\n'
        '          <span class="cd-dl-s">Listen offline</span>\n'
        '        </a>\n'
        '      </div>\n' % (esc(m["url"]), label, mb)
    )


def related_box_html(meta):
    """The Related episodes box, or nothing when there are none.

    Empty on 14 episodes. Same reasoning as the download box: a heading over
    nothing is a bug, not a layout.
    """
    inner = render_list(meta.get("related", []))
    if not inner.strip():
        return ""
    return ('      <div class="cd-box">\n'
            '        <h2>Related episodes</h2>\n'
            '%s\n'
            '      </div>\n' % inner)


def player_html(meta):
    """The media block.

    Most episodes are on YouTube and get the nocookie iframe. Six are podcast
    only: they exist in the feed but were never filmed, so there is no video id
    and an iframe would render an empty player. Those get the episode artwork
    and the listen buttons instead, which is what a listener actually wants.
    """
    vid = (meta.get("video_id") or "").strip()
    # THESE USED TO BE THE SHOW, ON EVERY EPISODE PAGE.
    # Whichever conversation you were reading, "Listen on Spotify" and "Listen on
    # Apple" sent you to the front of the podcast, not to that episode. The
    # Spotify address was in the RSS feed all along and simply never read; the
    # Apple one needs Apple's own episode id, which is not in the feed at all and
    # comes from apple-episodes.json. See tools/build_mp3_map.py.
    #
    # The show is kept as the fallback: 13 episodes are reels and cinematics that
    # were never published as audio, so the front of the podcast is the only
    # honest destination for them.
    links = mp3_for(meta.get("slug", "")) or {}
    spotify = (links.get("spotify") or meta.get("spotify")
               or "https://open.spotify.com/show/16jBM3RfjVERukNHJrIRec")
    apple = (links.get("apple")
             or "https://podcasts.apple.com/us/podcast/"
                "paragliding-atlas-by-aninder-singh/id1735782803")
    if vid:
        media = (
            '      <div class="cd-player">\n'
            '        <span class="cd-player-corner cd-pc-tl"></span>\n'
            '        <span class="cd-player-corner cd-pc-br"></span>\n'
            '        <iframe src="https://www.youtube-nocookie.com/embed/%s" title="%s"\n'
            '          loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"\n'
            '          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n'
            '      </div>\n' % (esc(vid), esc(meta["title"])))
        listen = '        <a class="cd-lbtn" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener"><span>Watch on YouTube</span></a>\n' % esc(vid)
    else:
        art = meta.get("artwork") or "../assets/images/hero.jpg"
        media = (
            '      <div class="cd-player cd-player-audio">\n'
            '        <span class="cd-player-corner cd-pc-tl"></span>\n'
            '        <span class="cd-player-corner cd-pc-br"></span>\n'
            '        <img src="%s" alt="%s" loading="lazy">\n'
            '        <p class="cd-audio-note">Audio episode. This one was never filmed, so there is no video to watch.</p>\n'
            '      </div>\n' % (esc(art), esc(meta["title"])))
        listen = ""
    return (media
            + '\n      <div class="cd-listen">\n' + listen
            # The label is wrapped so .cd-lbtn span can counter skew it. The
            # button is skewed 10 degrees and a bare text node inside it comes
            # out italic: these three have been reading that way all along, and
            # it only became obvious once every button on the site was skewed.
            + '        <a class="cd-lbtn" href="%s" target="_blank" rel="noopener"><span>Listen on Spotify</span></a>\n' % esc(spotify)
            + '        <a class="cd-lbtn" href="%s" target="_blank" rel="noopener"><span>Listen on Apple</span></a>\n' % esc(apple)
            + '      </div>\n')


def tag_slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def _paged_tags():
    """Tags with their own hub page. Built from the same threshold the tag
    generator uses, by simply looking at which pages exist, so the two can never
    disagree about what is linkable."""
    d = os.path.join(ROOT, "tags")
    if not os.path.isdir(d):
        return set()
    return {f[:-5] for f in os.listdir(d) if f.endswith(".html")}


PAGED_TAGS = _paged_tags()


def render_tags(tags):
    """A tag with a page becomes a link; one without stays plain text.

    The leading # is drawn by CSS, never written into the markup, so the anchor
    text a crawler reads is "Safety" rather than "#Safety". Hashes are a social
    convention and make poor anchor text.
    """
    out = []
    for t in tags or []:
        s = tag_slug(t)
        if s in PAGED_TAGS:
            out.append('        <a class="cd-tag" href="../tags/%s.html">%s</a>' % (s, esc(t)))
        else:
            out.append('        <span class="cd-tag">%s</span>' % esc(t))
    return "\n".join(out)


def render_quote(meta):
    """The pull quote, beside the title.

    Marked up as a blockquote with a cite so it reads as a quotation to a
    crawler and to an answer engine, which is the shape those systems lift.
    """
    q = (meta.get("quote") or "").strip()
    if not q:
        return ""
    who = (meta.get("guest") or "").strip()
    cite = '<cite>%s</cite>' % esc(who) if who else ""
    return ('      <figure class="cd-quote">\n'
            '        <blockquote><p>%s</p></blockquote>\n'
            '        %s\n'
            '      </figure>' % (esc(q), cite))


def build(meta, cues, chapters):
    paras = paragraphs(cues)
    words = sum(len(p["text"].split()) for p in paras)
    vid = meta.get("video_id", "")
    tmpl = open(os.path.join(ROOT, "templates", "episode-template.html"), encoding="utf-8").read()

    jsonld = {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "name": meta["title"],
        "datePublished": meta.get("published", ""),
        "description": meta.get("summary", "")[:280],
        "partOfSeries": {"@type": "PodcastSeries", "name": "Paragliding Atlas"},
        "url": "https://paraglidingatlas-maker.github.io/Website/episodes/%s.html" % meta["slug"],
    }
    if meta.get("guest"):
        jsonld["actor"] = {"@type": "Person", "name": meta["guest"]}
    if (meta.get("quote") or "").strip():
        jsonld["abstract"] = meta["quote"].strip()
    if meta.get("tags"):
        jsonld["keywords"] = ", ".join(meta["tags"])

    submeta = []
    if meta.get("guest"):
        submeta.append("<span><strong>%s</strong></span>" % esc(meta["guest"]))
    if meta.get("published_label"):
        submeta.append("<span>%s</span>" % esc(meta["published_label"]))
    if meta.get("duration_label"):
        submeta.append("<span>%s</span>" % esc(meta["duration_label"]))
    # "Full transcript" is a claim about the page. On the 13 reels and
    # cinematics there is no transcript and no rail, so the label was left over
    # describing something that is not there. User asked for it gone, 2026-09-11.
    if transcript_expected(meta):
        submeta.append("<span>Full transcript</span>")
    submeta_html = '<span class="cd-dot"></span>'.join(submeta)

    return tmpl.format(
        title=esc(meta["title"]),
        seo_title=esc(seo_title(meta["title"])),
        seo_desc=esc(meta.get("summary", "")[:155]),
        slug=meta["slug"],
        series=esc(meta.get("series", "")),
        series_slug=meta.get("series_slug", ""),
        epno=esc(meta.get("epno", "")),
        submeta=submeta_html,
        video_id=esc(vid),
        player=player_html(meta),
        og_image=esc(meta.get("artwork") or
                     ("https://i.ytimg.com/vi/%s/maxresdefault.jpg" % vid if vid
                      else "https://paraglidingatlas-maker.github.io/Website/assets/images/hero.jpg")),
        rail_block=rail_block_html(meta, chapters_with_content(paras, chapters)),
        summary=esc(meta.get("summary", "")),
        transcript_block=transcript_block_html(
            meta,
            wrap_transcript(render_transcript(paras, chapters_with_content(paras, chapters),
                                              meta.get("speakers", {})),
                            words, bool(paras), meta)),
        tag_pulse=(" tag-pulse"
                   if TAG_PULSE_ON == "all" or meta["slug"] in TAG_PULSE_ON
                   else ""),
        guest_box=guest_box_html(meta),
        download_box=download_box_html(meta),
        related_box=related_box_html(meta),
        tags=render_tags(meta.get("tags")),
        quote=render_quote(meta),
        spotify=esc(meta.get("spotify", "https://open.spotify.com/show/16jBM3RfjVERukNHJrIRec")),
        jsonld=json.dumps(jsonld, ensure_ascii=False, indent=2),
        words="{:,}".format(words),
    )


# ---------------------------------------------------------------- main

def main(only=None):
    metas = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    built, skipped, noted = 0, [], []
    for meta in metas:
        slug = meta["slug"]
        if only and slug not in only:
            continue
        vtt = os.path.join(TX, slug + ".vtt")
        if os.path.exists(vtt):
            cues = parse_vtt(vtt)
            chapters, warn = resolve_chapters(meta, cues)
        else:
            # No transcript yet. The page is still worth having: player, series,
            # related episodes and links all stand on their own.
            cues, chapters, warn = [], [], []
            noted.append(slug)
        for w in warn:
            print("  warning [%s] %s" % (slug, w))
        page = build(meta, cues, chapters)
        open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8").write(page)
        print("  built %-52s %2d chapters, %d cues" % (slug + ".html", len(chapters), len(cues)))
        built += 1
    print("\n%d page(s) built." % built)
    for s, why in skipped:
        print("  skipped %-46s %s" % (s, why))
    if noted:
        print("  %d built without a transcript (player and links only)" % len(noted))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
