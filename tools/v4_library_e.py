#!/usr/bin/env python3
"""The v4 library, option E: the ridge and the voices.

    python3 tools/v4_library_e.py            -> prototypes/v4/library-e.html

The page shell is prototypes/v4/library.html (head, nav, footer); the main is rebuilt. Every conversation is a
column on a ridge, by date and as tall as it is long. The scroll flies along the years and stops at twelve
voices, a guest's own sentence over their still; any column answers a touch with the guest and the sentence.
Below the ridge the finder: search, five shelves, the guests, the topics, and the rows. No sound on this page.
Data: episode-meta.json; stills from tools/library_stills.py; shelves here. Nothing moves unless the visitor does."""
import datetime, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
SRC = os.path.join(V4, "library.html"); OUT = os.path.join(V4, "library-e.html")
META = os.path.join(ROOT, "episode-meta.json"); STILLS = os.path.join(ROOT, "tools", "data", "library-stills.json")
SHELVES = [("Fly better", ["Flight Mechanics", "Know Your Equipment", "Weather Patterns", "Resources, Tools and Tips"], "Thermals, wings, weather and the tools of the trade."),
           ("Competition", ["World Cups", "Sky Gods"], "Task by task from the World Cup, and the pilots who win them."),
           ("Risk and safety", ["Risk vs Reward", "The Dark Side"], "The decisions that keep you flying, and the ones that do not."),
           ("Lives in the air", ["Living the Dream", "Navigators", "Storytellers"], "Journeys, records and the people behind them."),
           ("The industry", ["New Technologies", "Brand Stories"], "Who makes the gear and where it is going.")]
SHELF_OF = {s: i for i, (_, ss, _) in enumerate(SHELVES) for s in ss}
STOPS = 12                       # voices the flight stops at
TOPICS = 14                      # the most used tags, as the topic doors
esc = html.escape


def mins(e): return int(re.sub(r"\D", "", e.get("duration_label", "") or "") or 0)


def short_title(e):
    t = e["title"]
    if len(t) > 64 and ":" in t: t = t.split(":")[0]
    return t if len(t) <= 72 else t[:72].rsplit(" ", 1)[0] + "…"


def build():
    t = open(SRC, encoding="utf-8").read()
    meta = json.load(open(META)); stills = json.load(open(STILLS)) if os.path.exists(STILLS) else {}
    eps = []
    for e in meta:
        if not (e.get("epno") or e.get("published") or e.get("video_id")): continue
        d = e.get("published") or ""
        eps.append(dict(slug=e["slug"], title=short_title(e), full=e["title"], guest=e.get("guest") or "", series=e.get("series") or "", shelf=SHELF_OF.get(e.get("series"), 4),
                        date=d, label=e.get("published_label") or "", mins=mins(e), quote=(e.get("quote") or "").strip(), tags=e.get("tags") or [], summary=e.get("summary") or "",
                        epno=e.get("epno") or "", chapters=len(e.get("chapters") or []), still=e["slug"] if e["slug"] in stills else "", face="face" in stills.get(e["slug"], {}).get("how", "")))
    dated = sorted([e for e in eps if e["date"]], key=lambda e: e["date"]); undated = [e for e in eps if not e["date"]]
    t0 = datetime.date.fromisoformat(dated[0]["date"]); t1 = datetime.date.fromisoformat(dated[-1]["date"])
    span = max(1, (t1 - t0).days); mx = max(e["mins"] for e in dated) or 1
    for e in dated: e["x"] = round((datetime.date.fromisoformat(e["date"]) - t0).days / span, 4); e["h"] = round(e["mins"] / mx, 3)
    # the stops: the voices along the years, one from each twelfth of the flight, a sentence and a face
    cands = [e for e in dated if e["quote"] and e["still"] and e["face"] and "&" not in e["guest"] and 40 <= len(e["quote"]) <= 190]
    stops = []
    for k in range(STOPS):
        lo, hi = k / STOPS, (k + 1) / STOPS
        pool = [e for e in cands if lo <= e["x"] < hi or (k == STOPS - 1 and e["x"] == 1)] or [e for e in cands if e not in stops]
        pool = [e for e in pool if e not in stops]
        if pool: stops.append(max(pool, key=lambda e: len(e["quote"])))
    stops.sort(key=lambda e: e["x"])
    hours = sum(e["mins"] for e in eps); chapters = sum(e["chapters"] for e in eps)
    counts = [sum(1 for e in eps if e["shelf"] == i) for i in range(5)]
    tagc = {}
    for e in eps:
        for g in e["tags"]:
            if g.lower() == "paragliding": continue
            tagc[g] = tagc.get(g, 0) + 1
    topics = sorted(tagc.items(), key=lambda kv: (-kv[1], kv[0]))[:TOPICS]
    gc = {}
    for e in eps:
        if e["guest"] and e["still"] and e["face"] and "&" not in e["guest"]: gc.setdefault(e["guest"], []).append(e)
    guests = sorted(gc.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:12]

    # ---- the data the page runs on
    data = dict(base="", t0=t0.isoformat(), t1=t1.isoformat(), stops=[e["slug"] for e in stops], shelves=[s[0] for s in SHELVES],
                eps=[dict(s=e["slug"], t=e["title"], g=e["guest"], sh=e["shelf"], d=e["label"], x=e.get("x", -1), h=e.get("h", 0), m=e["mins"], q=e["quote"], k=e["tags"], i=e["still"], n=e["epno"].replace("Episode ", "")) for e in dated + undated])
    data_js = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

    # ---- the flight
    def still(e, kind="s"): return "img/library/stills/%s/%s.webp" % (kind, e["still"]) if e["still"] else ""
    stop_html = "".join(
        '<figure class="v4l-stop" data-i="%d" data-s="%s"><img src="%s" alt="" loading="%s" decoding="async" width="960" height="720"></figure>'
        % (i, esc(e["slug"]), still(e, "w"), "eager" if i < 2 else "lazy") for i, e in enumerate(stops))
    first = stops[0]
    flight = (
        '<section class="v4l-fly" id="flight" aria-labelledby="flight-h" style="--n:%d">' % len(stops) +
        '<div class="v4l-fly-pin"><div class="v4l-bgs">%s</div>' % stop_html +
        '<div class="v4l-q"><span class="v4l-k"><b class="v4l-qn">%s</b><i class="v4l-qs">%s</i><i class="v4l-qd">%s</i></span>' % (esc(first["epno"]), esc(first["series"]), esc(first["label"])) +
        '<h1 id="flight-h" class="v4l-h1">Paragliding Podcast Episode Library</h1>' +
        '<p class="v4l-qt">%s</p><p class="v4l-qw"><b>%s</b> <span>%s · %d min</span></p>' % (esc(first["quote"]), esc(first["guest"]), esc(first["title"]), first["mins"]) +
        '<a class="v4l-open" href="episodes/%s.html">Open the episode <i aria-hidden="true">&rarr;</i></a></div>' % esc(first["slug"]) +
        '<div class="v4l-count"><b>%dh %02dm</b><span>of pilots talking · %d conversations · %s to %s</span></div>' % (hours // 60, hours % 60, len(eps), t0.year, t1.year) +
        '<div class="v4l-year" aria-hidden="true"><b>%d</b><span><i class="v4l-yi">1</i> of %d voices</span></div>' % (t0.year, len(stops)) +
        '<div class="v4l-ridge" aria-hidden="true"><svg class="v4l-rs" viewBox="0 0 1000 300" preserveAspectRatio="none"></svg><div class="v4l-tip" hidden><img alt="" width="64" height="64"><b></b><i></i><span></span></div>' +
        '<div class="v4l-yrs"></div></div>' +
        '<p class="v4l-hint"><span class="v4l-hint-fly">Scroll to fly along the years</span><a class="v4l-land" href="#find">Land now <i aria-hidden="true">&darr;</i></a></p>' +
        '<noscript><p class="v4l-noscript">Every conversation is listed below.</p></noscript></div></section>')

    # ---- the finder
    shelves = "".join('<button class="v4l-si" type="button" data-sh="%d"><em>0%d</em><b>%s</b><span>%d conversations</span><small>%s</small></button>'
                      % (i, i + 1, esc(n), counts[i], esc(" · ".join(ss))) for i, (n, ss, _) in enumerate(SHELVES))
    guest_html = "".join('<button class="v4l-g" type="button" data-g="%s"><img src="%s" alt="" loading="lazy" width="68" height="68"><span>%s</span><small>%d</small></button>'
                         % (esc(g), still(es[0]), esc(g), len(es)) for g, es in guests)
    topic_html = "".join('<button class="v4l-t" type="button" data-t="%s">%s <small>%d</small></button>' % (esc(g), esc(g), n) for g, n in topics)
    finder = (
        '<section class="v4l-find" id="find" aria-labelledby="find-h"><div class="v4l-find-in">'
        '<div><span class="v4l-kk">Landed · find a conversation</span><h2 id="find-h">Five shelves</h2>'
        '<label class="v4l-search"><span class="sr-only">Search episodes</span><input type="search" placeholder="Search episodes, guests and topics" autocomplete="off"></label>'
        '<div class="v4l-shelves">%s</div></div>' % shelves +
        '<div><span class="v4l-kk">By guest</span><h2>Who is talking</h2><div class="v4l-guests">%s</div>' % guest_html +
        '<span class="v4l-kk">By topic</span><div class="v4l-topics">%s</div></div></div></section>' % topic_html)

    # ---- the rows
    def row(e):
        im = ('<img src="%s" alt="" loading="lazy" width="96" height="54">' % still(e)) if e["still"] else '<span class="v4l-nost">still to come</span>'
        return ('<a class="v4l-row" href="episodes/%s.html" data-s="%s"><span class="v4l-no">%s</span><span class="v4l-dt">%s</span><span class="v4l-st">%s</span>'
                '<span class="v4l-tt"><b>%s</b><span>%s</span></span><span class="v4l-sh">%s</span><span class="v4l-ln">%s</span><span class="v4l-go" aria-hidden="true">&rarr;</span></a>'
                % (esc(e["slug"]), esc(e["slug"]), esc(e["epno"].replace("Episode ", "")), esc(e["label"]) if e["label"] else '<i>date to supply</i>', im, esc(e["title"]),
                   esc(e["guest"] or e["series"]), esc(SHELVES[e["shelf"]][0]), ("%d min" % e["mins"]) if e["mins"] else ""))
    rows = "".join(row(e) for e in list(reversed(dated)) + undated)
    browse = (
        '<section class="v4l-rows" id="browse" aria-labelledby="browse-h"><div class="v4l-rows-in">'
        '<span class="v4l-kk">Below the ridge</span><h2 id="browse-h">All <span class="v4l-n">%d</span> conversations<small class="v4l-filter" hidden></small></h2>' % len(eps) +
        '<div class="v4l-mini" aria-hidden="true"><svg viewBox="0 0 1000 80" preserveAspectRatio="none"></svg></div>'
        '<div class="v4l-head" aria-hidden="true"><span>No.</span><span>Date</span><span></span><span>Episode</span><span>Shelf</span><span>Length</span><span></span></div>'
        '<div class="v4l-list">%s</div><button class="v4l-more" type="button">Show 24 more</button>' % rows +
        '<p class="v4l-none" hidden>Nothing matches. Clear the filter to see all %d.</p></div></section>' % len(eps))

    main = ('<main id="v4-main">\n<script type="application/json" id="v4l-data">%s</script>\n' % data_js + flight + "\n" + finder + "\n" + browse + "\n" +
            '<section class="v4-next"><div class="v4-next-in"><span class="kit-kicker">Browse by subject</span><a class="v4-next-a" href="tags.html">Topics <i aria-hidden="true">&rarr;</i></a></div></section>\n</main>')
    i = t.index('<main id="v4-main">'); j = t.index("</main>") + len("</main>")
    t = t[:i] + main + t[j:]
    for js in ("library-episodes.js", "episode-modal.js", "v2-library.js"):              # the old rows' scripts: nothing for them here
        t = re.sub(r'<script[^>]+%s[^>]*></script>\n?' % re.escape(js), "", t)
    t = t.replace("<title>", "<title>Option E: ", 1)
    t = t.replace('<body class="v4-lib-log">', '<body class="v4-lib-log v4l">', 1)
    t = t.replace("</head>", "<style>" + CSS + "</style>\n</head>", 1)
    t = t.replace("</body>", '<script src="library-e.js" defer></script>\n</body>', 1)
    open(OUT, "w", encoding="utf-8").write(t)
    print("wrote %s %d bytes; %d episodes (%d dated), %d stops: %s" % (os.path.relpath(OUT, ROOT), len(t), len(eps), len(dated), len(stops), ", ".join(e["guest"] for e in stops)))


CSS = r"""
.v4l{--lb:#141519;--lc:#202127;--lo:#ff7517;--lw:#f6f4f4;--lg:#9a9aa3;--lgl:#c9c9cf;--lgut:var(--gutter,clamp(1.2rem,4vw,4rem))}
.v4l .v4l-k,.v4l .v4l-kk,.v4l .v4l-count span,.v4l .v4l-year span,.v4l .v4l-hint,.v4l .v4l-head,.v4l .v4l-no,.v4l .v4l-dt,.v4l .v4l-ln,.v4l .v4l-more,.v4l .v4l-si em,.v4l .v4l-si span,.v4l .v4l-yrs{font-family:var(--font-mono,"DM Mono",monospace)}
.v4l-k{display:flex;gap:.9em;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--lo)}.v4l-k i{font-style:normal;color:var(--lgl)}
.v4l-kk{display:flex;align-items:center;gap:10px;font-family:var(--font-body,"DM Sans",sans-serif)!important;font-size:13px;color:var(--lgl);margin:0 0 .2rem}.v4l-kk:before{content:"";width:22px;height:1px;background:var(--lg)}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
/* the flight */
.v4l-fly{position:relative;height:calc(var(--n) * 100vh + 60vh);background:var(--lb);color:var(--lw)}
.v4l-fly-pin{position:sticky;top:0;height:100vh;overflow:hidden}
.v4l-bgs{position:absolute;inset:0}.v4l-stop{position:absolute;inset:0;margin:0;opacity:0;transition:opacity .9s var(--ease,ease)}.v4l-stop.is-on{opacity:1}
.v4l-stop img{width:100%;height:100%;object-fit:cover;object-position:center 30%;filter:grayscale(.2) brightness(.4) blur(3px);transform:scale(1.04)}
.v4l-bgs:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,21,25,.94) 0%,rgba(20,21,25,.6) 50%,rgba(20,21,25,.25) 100%),linear-gradient(0deg,#141519 0%,rgba(20,21,25,0) 48%)}
.v4l-q{position:absolute;z-index:3;left:var(--lgut);top:18vh;max-width:min(760px,calc(100% - 2 * var(--lgut)))}
.v4l-h1{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.v4l-qt{font-family:var(--font-display,Poppins,sans-serif);font-weight:600;font-size:clamp(1.7rem,3.3vw,2.9rem);line-height:1.14;letter-spacing:-.01em;margin:.7rem 0 1rem;transition:opacity .5s var(--ease,ease)}
.v4l-qt:before{content:"\201C";color:var(--lo);margin-right:.1em}
.v4l-qw{font-size:1.05rem;color:var(--lgl);margin:0}.v4l-qw b{color:var(--lw);font-weight:500}
.v4l-open{display:inline-flex;align-items:center;gap:.6rem;margin-top:1.4rem;color:var(--lw);text-decoration:none;border:1px solid rgba(255,255,255,.22);padding:.7rem 1.1rem;border-radius:999px;font-size:.95rem}.v4l-open:hover{border-color:var(--lo)}
.v4l-q.is-swap .v4l-qt,.v4l-q.is-swap .v4l-qw,.v4l-q.is-swap .v4l-k{opacity:0}
.v4l-count{position:absolute;z-index:3;right:var(--lgut);top:17vh;text-align:right}.v4l-count b{font-family:var(--font-display,Poppins,sans-serif);font-size:clamp(2rem,3.4vw,2.9rem);display:block;line-height:1}.v4l-count span{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--lg)}
.v4l-year{position:absolute;z-index:3;right:var(--lgut);top:17vh;text-align:right;opacity:0;transition:opacity .5s var(--ease,ease)}.v4l-year b{font-family:var(--font-display,Poppins,sans-serif);font-size:clamp(2.6rem,4.4vw,4rem);display:block;line-height:1}.v4l-year span{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--lg)}.v4l-year i{font-style:normal}
.v4l-fly.is-flying .v4l-count{opacity:0}.v4l-fly.is-flying .v4l-year{opacity:1}
.v4l-ridge{position:absolute;z-index:2;left:0;right:0;bottom:0;height:34vh;min-height:220px}
.v4l-rs{position:absolute;left:0;right:0;bottom:44px;width:100%;height:calc(100% - 44px);overflow:visible}
.v4l-rs line{stroke:#d7d7de;stroke-width:1.5;opacity:.5;pointer-events:stroke;cursor:pointer;transition:opacity .4s var(--ease,ease)}.v4l-rs line.is-hot{opacity:1;stroke-width:2.5}.v4l-rs line.is-on{stroke:var(--lo);stroke-width:3;opacity:1}.v4l-rs line.is-dim{opacity:.12}.v4l-rs line.is-was{opacity:.85}
.v4l-rs .v4l-mk{fill:var(--lo)}.v4l-rs .v4l-ring{fill:none;stroke:var(--lo);opacity:.5}.v4l-rs .v4l-was{fill:var(--lo);opacity:.8}.v4l-rs .v4l-area{fill:url(#v4l-g)}
.v4l-yrs{position:absolute;left:var(--lgut);right:var(--lgut);bottom:16px;display:flex;justify-content:space-between;font-size:11px;color:var(--lg);border-top:1px solid rgba(255,255,255,.1);padding-top:8px}
.v4l-tip{position:absolute;z-index:4;display:grid;grid-template-columns:64px 1fr;gap:0 12px;align-items:center;background:var(--lc);border-left:2px solid var(--lo);padding:10px 14px 10px 10px;width:320px;max-width:calc(100% - 2 * var(--lgut));font-size:13px;color:var(--lgl);pointer-events:none}
.v4l-tip img{width:64px;height:64px;object-fit:cover;grid-row:1/4;border-radius:50%}.v4l-tip b{font-family:var(--font-display,Poppins,sans-serif);font-weight:600;color:var(--lw);font-size:14px}.v4l-tip i{display:block;color:var(--lw);font-size:13px;line-height:1.35}.v4l-tip span{font-family:var(--font-mono,monospace);font-size:11px;color:var(--lg)}.v4l-tip[hidden]{display:none}
.v4l-hint{position:absolute;z-index:3;right:var(--lgut);bottom:calc(34vh + 10px);margin:0;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--lg);display:flex;gap:1.6rem;align-items:center}.v4l-land{color:var(--lw);text-decoration:none;border-bottom:1px dotted var(--lg);padding-bottom:2px}.v4l-land:hover{color:var(--lo)}
.v4l-noscript{position:absolute;left:var(--lgut);bottom:36vh;color:var(--lgl)}
/* the finder */
.v4l-find,.v4l-rows{background:var(--lb);color:var(--lw);padding:clamp(3rem,7vh,5rem) var(--lgut)}
.v4l-find-in{display:grid;grid-template-columns:1.15fr 1fr;gap:clamp(2rem,5vw,4.5rem);max-width:var(--measure-wide,1320px);margin:0 auto}
.v4l-find h2,.v4l-rows h2{font-family:var(--font-display,Poppins,sans-serif);font-weight:700;font-size:clamp(1.8rem,3vw,2.3rem);margin:.3rem 0 1.4rem;letter-spacing:-.01em}
.v4l-search{display:block;margin-bottom:1.6rem}.v4l-search input{width:100%;background:var(--lc);border:1px solid #2a2b33;color:var(--lw);padding:.95rem 1.1rem;font:inherit;font-size:1rem;border-radius:4px}.v4l-search input:focus{outline:1px solid var(--lo);outline-offset:1px}
.v4l-si{display:grid;grid-template-columns:44px 1fr auto;gap:0 14px;align-items:baseline;width:100%;text-align:left;padding:15px 0;border:0;border-top:1px solid #26272e;background:none;color:inherit;cursor:pointer;font:inherit}.v4l-si:last-child{border-bottom:1px solid #26272e}
.v4l-si em{font-style:normal;color:var(--lo);font-size:13px}.v4l-si b{font-family:var(--font-display,Poppins,sans-serif);font-weight:600;font-size:1.35rem}.v4l-si span{font-size:12px;color:var(--lg)}.v4l-si small{grid-column:2/4;color:var(--lg);font-size:13px}
.v4l-si:hover b,.v4l-si.is-on b{color:var(--lo)}.v4l-si.is-on{background:linear-gradient(90deg,rgba(255,117,23,.08),transparent)}
.v4l-guests{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:1.8rem}.v4l-g{width:78px;background:none;border:0;padding:0;color:inherit;font:inherit;text-align:center;cursor:pointer}.v4l-g img{width:68px;height:68px;border-radius:50%;object-fit:cover;display:block;margin:0 auto 7px;border:2px solid transparent}.v4l-g span{display:block;font-size:12px;color:var(--lgl);line-height:1.3}.v4l-g small{display:block;font-family:var(--font-mono,monospace);font-size:10px;color:var(--lg)}.v4l-g:hover img,.v4l-g.is-on img{border-color:var(--lo)}
.v4l-topics{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:.6rem}.v4l-t{background:none;border:0;padding:0 0 2px;color:var(--lgl);font:inherit;font-size:.95rem;border-bottom:1px dotted #5a5b66;cursor:pointer}.v4l-t small{font-family:var(--font-mono,monospace);font-size:10px;color:var(--lg)}.v4l-t:hover,.v4l-t.is-on{color:var(--lo);border-bottom-color:var(--lo)}
/* the rows */
.v4l-rows{padding-top:0}.v4l-rows-in{max-width:var(--measure-wide,1320px);margin:0 auto}.v4l-filter{display:inline-block;margin-left:1rem;font-family:var(--font-mono,monospace);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--lo);vertical-align:middle}.v4l-filter button{background:none;border:0;color:var(--lgl);font:inherit;cursor:pointer;margin-left:.6rem;text-decoration:underline dotted}
.v4l-mini{height:80px;margin:0 0 1.2rem}.v4l-mini svg{width:100%;height:100%}.v4l-mini line{stroke:#d7d7de;stroke-width:2;opacity:.35;transition:opacity .4s var(--ease,ease)}.v4l-mini line.is-lit{stroke:var(--lo);opacity:1}.v4l-mini.is-filtered line:not(.is-lit){opacity:.1}
.v4l-head,.v4l-row{display:grid;grid-template-columns:50px 150px 96px 1fr 150px 70px 30px;gap:16px;align-items:center}
.v4l-head{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--lg);padding:0 0 10px;border-bottom:1px solid #26272e}
.v4l-row{padding:13px 0;border-bottom:1px solid #1f2027;color:inherit;text-decoration:none;transition:background .2s}.v4l-row:hover{background:linear-gradient(90deg,rgba(255,117,23,.07),transparent)}.v4l-row[hidden]{display:none}
.v4l-no,.v4l-dt,.v4l-ln{font-size:13px;color:var(--lgl)}.v4l-dt i{color:var(--lg)}.v4l-st img,.v4l-nost{width:96px;height:54px;object-fit:cover;display:grid;place-items:center;background:var(--lc);font-family:var(--font-mono,monospace);font-size:10px;color:var(--lg);text-align:center}
.v4l-tt b{display:block;font-family:var(--font-display,Poppins,sans-serif);font-weight:600;font-size:1rem;line-height:1.3}.v4l-tt span{font-size:13px;color:var(--lg)}.v4l-sh{font-size:14px;color:var(--lgl)}.v4l-go{color:var(--lg)}.v4l-row:hover .v4l-go{color:var(--lo)}
.v4l-more{display:block;margin:1.6rem auto 0;background:none;border:1px solid #33343d;color:var(--lgl);font-size:12px;letter-spacing:.14em;text-transform:uppercase;padding:.8rem 1.4rem;border-radius:999px;cursor:pointer}.v4l-more:hover{border-color:var(--lo);color:var(--lw)}.v4l-more[hidden]{display:none}
.v4l-none{color:var(--lgl);padding:1.5rem 0}
@media (max-width:900px){.v4l-find-in{grid-template-columns:1fr}.v4l-head,.v4l-row{grid-template-columns:50px 120px 96px 1fr 70px 30px}.v4l-sh{display:none}.v4l-head span:nth-child(5){display:none}}
@media (max-width:700px){
.v4l-q{top:11vh;max-width:none;right:var(--lgut)}.v4l-k{display:block;line-height:1.7}.v4l-k b,.v4l-k i{margin-right:.9em}.v4l-qt{font-size:1.55rem}.v4l-qw{font-size:.95rem}.v4l-open{margin-top:1rem;padding:.6rem .95rem;font-size:.88rem}
.v4l-count,.v4l-year{top:auto;bottom:calc(30vh + 36px);right:var(--lgut)}.v4l-count b,.v4l-year b{font-size:1.5rem}.v4l-count span,.v4l-year span{display:none}
.v4l-ridge{height:30vh;min-height:170px}.v4l-hint{display:none}.v4l-tip{width:240px;grid-template-columns:48px 1fr}.v4l-tip img{width:48px;height:48px}
.v4l-head{display:none}.v4l-row{grid-template-columns:72px 1fr 24px;gap:12px;padding:10px 0}.v4l-no,.v4l-dt,.v4l-sh,.v4l-ln{display:none}.v4l-st img,.v4l-nost{width:72px;height:72px}.v4l-tt b{font-size:.95rem}
.v4l-mini{height:56px}.v4l-guests{gap:10px}.v4l-g{width:68px}.v4l-g img{width:56px;height:56px}}
@media (prefers-reduced-motion:reduce){.v4l-stop,.v4l-qt,.v4l-rs line,.v4l-year,.v4l-count{transition:none}}
"""

if __name__ == "__main__":
    build()
