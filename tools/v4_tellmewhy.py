#!/usr/bin/env python3
"""
"Tell me why": ask anything about free flight, and hear the answer from the
people on the show (owner, 2 Oct 2026: "an AI bot called Tell me why, who
answers every possible question based on the data from transcripts in the
episodes and videos", then "3": the transcript answers now, written answers
on top later).

Stage 1, this page: the question is matched, on the reader's own device,
against every passage of every published transcript (BM25 over about 9,000
timestamped passages from 80 episodes). The answer is the guests' own words:
the best passages, one per episode, each with who said it, the episode, the
chapter and the moment, and a link to that chapter. Nothing is written by a
model, so nothing can be invented.

Stage 2, later: set data-endpoint on the section to a small server that holds
an Anthropic API key. The page then also POSTs the question and the passages
it found, and shows the written answer (citing those passages) above them.
Nothing else changes.

    python3 tools/v4_tellmewhy.py   # writes prototypes/v4/samples/tell-me-why.html and samples/tmw-index.js
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v4_samples as SM  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
HOST = "Aninder"


def text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


NOT_NAMES = set("so my in the and but i we yes no okay ok well now then this that it you he she they there here what why how when "
                "oh yeah right because if or also just like um uh".split())


def episodes():
    eps, docs = [], []
    for fn in sorted(os.listdir(os.path.join(V4, "episodes"))):
        if not fn.endswith(".html"):
            continue
        s = open(os.path.join(V4, "episodes", fn), encoding="utf-8").read()
        if 'id="transcript-body"' not in s:
            continue
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        sub = re.search(r'<span class="ep2-sub">(.*?)</span>', h1.group(1), re.S) if h1 else None
        series = re.search(r'<span class="ep2-h1">(.*?)</span>', h1.group(1), re.S) if h1 else None
        title = text(sub.group(1)) if sub else text(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).split("|")[0].strip()
        e = len(eps)
        eps.append([fn[:-5], title, text(series.group(1)) if series else ""])
        body = s[s.index('id="transcript-body"'):]
        # a name counts as a speaker only if it labels a few lines (the captions sometimes label a stray word)
        from collections import Counter
        names = Counter(text(n).rstrip(":") for n in re.findall(r'<span class="cd-spk">([^<]*)</span>', body))
        real = {n for n, c in names.items() if c >= 3 and n[:1].isupper() and n.lower() not in NOT_NAMES}
        spk = ""
        for blk in re.finditer(r'<div class="cd-block" id="(c\d+)">\s*<h2>(.*?)</h2>(.*?)(?=<div class="cd-block" id="c\d+">|</div>\s*</div>\s*<(?:/|section|div class="cd-))', body, re.S):
            cid, chap, inner = blk.group(1), text(blk.group(2)), blk.group(3)
            for ts, p in re.findall(r'<span class="cd-ts">([^<]*)</span>\s*<p>(.*?)</p>', inner, re.S):
                m = re.match(r'\s*<span class="cd-spk">([^<:]*):?</span>', p)
                if m and text(m.group(1)).rstrip(":") in real:
                    spk = text(m.group(1)).rstrip(":")
                    spk = "A guest" if spk == "Guest" else spk
                t = text(re.sub(r'<span class="cd-spk">[^<]*</span>', "", p))
                if len(t.split()) < 8:
                    continue
                docs.append([e, cid, ts, spk, chap, t])
    return eps, docs


CSS = """
.tmw{padding:0 var(--gutter) var(--sp-5);max-width:1100px;margin:0 auto;}
.tmw-hero{padding:clamp(7rem,14vh,9rem) 0 var(--sp-4);display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:var(--sp-4);align-items:end;}
@media (max-width:820px){ .tmw-hero{grid-template-columns:1fr;} .tmw-art{display:none;} }
.tmw-hero h1{font-family:var(--font-display);font-size:var(--fs-display);line-height:1.02;margin:.5rem 0 1rem;color:#fff;letter-spacing:-.02em;}
.tmw-hero h1 em{font-style:normal;color:var(--orange);}
.tmw-art svg{width:100%;height:auto;display:block;}
.tmw-art path{fill:none;vector-effect:non-scaling-stroke;}
.tmw-ask{position:sticky;top:0;z-index:5;padding:var(--sp-2) 0;background:linear-gradient(180deg,var(--bg) 70%,transparent);}
.tmw-form{display:flex;gap:.6rem;align-items:stretch;border:1px solid var(--edge);background:rgba(255,255,255,.03);padding:.4rem;}
.tmw-form:focus-within{border-color:var(--orange);}
.tmw-form input{flex:1;min-width:0;background:none;border:0;color:#fff;font-size:1.15rem;padding:.8rem 1rem;outline:none;}
.tmw-form input::placeholder{color:var(--gray);}
.tmw-form button{min-height:48px;padding:0 1.4rem;}
.tmw-try{display:flex;flex-wrap:wrap;gap:.5rem;margin:var(--sp-2) 0 0;padding:0;list-style:none;}
.tmw-try button{background:none;border:1px solid var(--line);color:var(--gray-light);font-size:var(--fs-small);padding:.5rem .8rem;min-height:40px;cursor:pointer;}
.tmw-try button:hover,.tmw-try button:focus-visible{border-color:var(--orange);color:#fff;}
.tmw-status{color:var(--gray);font-size:var(--fs-small);min-height:1.5em;margin:var(--sp-2) 0 0;}
.tmw-written{display:none;border-left:2px solid var(--orange);padding:.2rem 0 .2rem 1.2rem;margin:var(--sp-3) 0;color:#fff;line-height:1.7;}
.tmw-written.is-on{display:block;}
.tmw-res{list-style:none;padding:0;margin:var(--sp-3) 0 0;display:grid;gap:var(--sp-3);}
.tmw-r{border-top:1px solid var(--line);padding-top:var(--sp-2);opacity:0;transform:translateY(10px);animation:tmw-in .5s cubic-bezier(.2,.8,.2,1) forwards;}
@keyframes tmw-in{to{opacity:1;transform:none;}}
.tmw-who{font-family:var(--font-display);font-weight:600;color:#fff;font-size:1.05rem;}
.tmw-meta{display:block;color:var(--gray);font-size:var(--fs-small);margin:.15rem 0 .6rem;}
.tmw-meta b{color:var(--orange);font-weight:600;font-variant-numeric:tabular-nums;}
.tmw-q{margin:0;color:rgba(246,244,244,.9);line-height:1.7;font-size:1.02rem;}
.tmw-q mark{background:rgba(255,117,23,.18);color:#fff;padding:0 .1em;}
.tmw-go{display:inline-flex;align-items:center;gap:.4rem;margin-top:.6rem;color:var(--orange);font-size:var(--fs-small);font-weight:600;text-decoration:none;min-height:40px;}
.tmw-more{margin-top:var(--sp-3);}
.tmw-note{color:var(--gray);font-size:var(--fs-micro);line-height:1.6;margin-top:var(--sp-5);border-top:1px solid var(--line);padding-top:var(--sp-2);}
@media (prefers-reduced-motion:reduce){ .tmw-r{animation:none;opacity:1;transform:none;} }
"""


ART = ('<svg viewBox="0 0 420 220" aria-hidden="true"><defs><linearGradient id="tmwG" x1="0" y1="0" x2="1" y2="0">'
       '<stop offset="0" stop-color="#f6f4f4"/><stop offset="1" stop-color="#ffcf94"/></linearGradient></defs>%s</svg>')


def art():
    """A voice that becomes a range of mountains: the waveform of a conversation, its peaks a ridgeline."""
    import math
    bars, ridge = "", []
    for i in range(70):
        x = 10 + i * 5.8
        h = 20 + 70 * math.exp(-((x - 130) / 55) ** 2) + 55 * math.exp(-((x - 300) / 60) ** 2) + 10 * math.sin(i * 1.7) ** 2
        bars += '<path d="M%.1f,170 V%.1f" stroke="url(#tmwG)" stroke-width="1.6" stroke-opacity=".75"/>' % (x, 170 - h)
        bars += '<path d="M%.1f,174 V%.1f" stroke="#f6f4f4" stroke-opacity=".18" stroke-width="1.2"/>' % (x, 174 + h * .25)
        ridge.append((x, 170 - h - 6))
    d = "M" + " L".join("%.1f,%.1f" % p for p in ridge)
    return ART % (bars + '<path d="%s" stroke="#ff7517" stroke-width="1.6"/>' % d)


TRY = ["Why do wings collapse?", "How do you read a cloud base?", "What makes a good thermal?", "Why fly at 8,000 metres?",
       "How do you choose a first wing?", "What scares you about flying?"]


def page(n_eps, n_docs):
    body = ('<main class="tmw"><section class="tmw-hero"><div><span class="kit-kicker">Ask the show</span>'
            '<h1>Tell me <em>why</em></h1><p class="kit-intro">Ask anything about free flight. The answer comes from the people on the show, '
            'in their own words: %d conversations, %s passages of transcript, each with the moment it was said.</p></div>'
            '<div class="tmw-art">%s</div></section>'
            '<section class="tmw-main" aria-labelledby="tmwL" data-endpoint="">'
            '<div class="tmw-ask"><form class="tmw-form" role="search"><label id="tmwL" class="visually-hidden" for="tmwQ">Your question</label>'
            '<input id="tmwQ" type="search" name="q" autocomplete="off" placeholder="Why do wings collapse in turbulence?" required>'
            '<button class="btn-solid" type="submit"><span>Tell me why</span></button></form></div>'
            '<ul class="tmw-try" aria-label="Questions to try">%s</ul>'
            '<p class="tmw-status" aria-live="polite"></p><div class="tmw-written" aria-live="polite"></div>'
            '<ol class="tmw-res"></ol><p class="tmw-more"></p>'
            '<p class="tmw-note">Answers are passages from the episode transcripts, found on your device. The transcripts are automatic '
            'captions and may contain recognition errors; follow the link to hear the moment in context.</p>'
            '<noscript><p>This needs JavaScript. Every transcript is on its episode page in the <a href="library.html">episode library</a>.</p></noscript>'
            '</section></main>' % (n_eps, "{:,}".format(n_docs), art(), "".join('<li><button type="button">%s</button></li>' % q for q in TRY)))
    return SM.shell("Tell me why", "Ask anything about free flight, answered in the words of the guests on the Paragliding Atlas podcast.", body,
                    CSS + ".visually-hidden{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}") \
        .replace("</body>", '<script src="tmw.js"></script>\n</body>', 1)


JS = r"""/* Tell me why (tools/v4_tellmewhy.py): BM25 over the transcript passages, on the
   reader's device; the index (tmw-index.js) loads on the first question. */
(function () {
  "use strict";
  var d = document, sec = d.querySelector(".tmw-main"); if (!sec) return;
  var form = sec.querySelector(".tmw-form"), q = sec.querySelector("#tmwQ"), st = sec.querySelector(".tmw-status");
  var res = sec.querySelector(".tmw-res"), more = sec.querySelector(".tmw-more"), wr = sec.querySelector(".tmw-written");
  var STOP = {}; ("a an the and or but if then so of to in on at by for with from about into over under is are was were be been being do does did " +
    "doing have has had having i you he she it we they me my your our their this that these those what which who whom whose why how when where " +
    "can could should would will shall may might must not no yes very just also more most some any all as than too there here " +
    "really get got go going thing things like know think say said lot kind way").split(" ").forEach(function (w) { STOP[w] = 1; });
  function stem(w) { return w.replace(/(ingly|edly|ing|ed|ies|es|s|ly)$/, function (m) { return m === "ies" ? "y" : ""; }); }
  function toks(s) { return (s.toLowerCase().match(/[a-z0-9]+(?:'[a-z]+)?/g) || []).map(function (w) { return w.replace(/'.*/, ""); }).filter(function (w) { return w.length > 1 && !STOP[w]; }).map(stem); }
  var I = null, loading = null;
  function load() {
    if (I) return Promise.resolve(I);
    if (loading) return loading;
    st.textContent = "Opening the transcripts…";
    loading = new Promise(function (ok, no) {
      var s = d.createElement("script"); s.src = "tmw-index.js";
      s.onload = function () {
        var D = window.TMW, docs = D.docs, N = docs.length, df = {}, tf = [], len = [], tot = 0;
        docs.forEach(function (r, i) {
          var t = toks(r[5] + " " + r[4] + " " + r[4]), m = {};
          t.forEach(function (w) { m[w] = (m[w] || 0) + 1; });
          Object.keys(m).forEach(function (w) { df[w] = (df[w] || 0) + 1; });
          tf.push(m); len.push(t.length); tot += t.length;
        });
        I = { eps: D.eps, docs: docs, df: df, tf: tf, len: len, avg: tot / N, N: N };
        ok(I);
      };
      s.onerror = function () { no(new Error("index")); };
      d.head.appendChild(s);
    });
    return loading;
  }
  function score(qt) {
    var k1 = 1.4, b = .75, out = [];
    for (var i = 0; i < I.N; i++) {
      var m = I.tf[i], sc = 0, hit = 0;
      for (var j = 0; j < qt.length; j++) {
        var w = qt[j], f = m[w]; if (!f) continue;
        hit++;
        var idf = Math.log(1 + (I.N - I.df[w] + .5) / (I.df[w] + .5));
        sc += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * I.len[i] / I.avg));
      }
      if (!sc) continue;
      sc *= 1 + .35 * (hit - 1);                                    // passages that hold more of the question rank higher
      var r = I.docs[i];
      if (r[3] && r[3].indexOf("Aninder") === 0) {
        // the host asking is not the answer: the guest's reply that follows is
        var nx = I.docs[i + 1];
        if (nx && nx[0] === r[0] && !(nx[3] && nx[3].indexOf("Aninder") === 0)) { out.push([sc * .9, i + 1]); continue; }
        sc *= .45;
      }
      out.push([sc, i]);
    }
    return out.sort(function (a, b) { return b[0] - a[0]; });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function excerpt(t, qt) {
    var words = t.split(/\s+/), best = 0, bi = 0, W = 70;
    if (words.length > W) {
      for (var i = 0; i + W <= words.length; i += 5) {
        var c = 0; for (var j = i; j < i + W; j++) if (qt.indexOf(stem(words[j].toLowerCase().replace(/[^a-z0-9]/g, ""))) >= 0) c++;
        if (c > best) { best = c; bi = i; }
      }
      words = words.slice(bi, bi + W);
    }
    var s = esc(words.join(" "));
    var re = new RegExp("\\b(" + qt.map(function (w) { return w.replace(/[^a-z0-9]/g, ""); }).filter(Boolean).join("|") + ")[a-z]*", "gi");
    return (bi > 0 ? "… " : "") + s.replace(re, "<mark>$&</mark>") + (words.length >= W ? " …" : "");
  }
  function render(list, qt, from) {
    list.forEach(function (x, k) {
      var r = I.docs[x[1]], e = I.eps[r[0]], li = d.createElement("li");
      li.className = "tmw-r"; li.style.animationDelay = (k * .08) + "s";
      li.innerHTML = '<span class="tmw-who">' + esc(r[3] || "On the show") + '</span>' +
        '<span class="tmw-meta">' + esc(e[2] ? e[2] + ": " : "") + esc(e[1]) + ' &middot; ' + esc(r[4]) + ' &middot; <b>' + esc(r[2]) + '</b></span>' +
        '<p class="tmw-q">' + excerpt(r[5], qt) + '</p>' +
        '<a class="tmw-go" href="../episodes/' + e[0] + '.html#' + r[1] + '">Hear it in context, at ' + esc(r[2]) + ' <i aria-hidden="true">&rarr;</i></a>';
      res.appendChild(li);
    });
  }
  function ask(text) {
    text = (text || "").trim(); if (!text) return;
    var qt = toks(text);
    res.innerHTML = ""; more.innerHTML = ""; wr.classList.remove("is-on"); wr.textContent = "";
    if (!qt.length) { st.textContent = "Ask it with a few more words, and the show will answer."; return; }
    load().then(function () {
      var all = score(qt), seen = {}, top = [], rest = [];
      var once = {}; all = all.filter(function (x) { if (once[x[1]]) return false; once[x[1]] = 1; return true; });
      all.forEach(function (x) { var e = I.docs[x[1]][0]; if (seen[e]) { if (rest.length < 30) rest.push(x); return; } seen[e] = 1; (top.length < 5 ? top : rest).push(x); });
      if (!top.length) { st.textContent = "Nobody on the show has talked about that yet, as far as the transcripts go. Try other words."; return; }
      st.textContent = "From " + Object.keys(seen).length + " conversation" + (Object.keys(seen).length === 1 ? "" : "s") + ", the clearest answers first.";
      render(top, qt);
      if (rest.length) {
        var b = d.createElement("button"); b.type = "button"; b.className = "btn-lines"; b.textContent = "More passages";
        b.addEventListener("click", function () { render(rest.slice(0, 10), qt); rest = rest.slice(10); if (!rest.length) b.remove(); });
        more.appendChild(b);
      }
      // stage 2: a written answer from the passages, when the page has a server to ask
      var ep = sec.getAttribute("data-endpoint");
      if (ep) {
        wr.classList.add("is-on"); wr.textContent = "Writing an answer from these passages…";
        fetch(ep, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: text,
          passages: top.concat(rest.slice(0, 7)).map(function (x) { var r = I.docs[x[1]], e = I.eps[r[0]]; return { episode: e[1], slug: e[0], chapter: r[1], ts: r[2], speaker: r[3], text: r[5] }; }) }) })
          .then(function (r) { return r.json(); }).then(function (j) { wr.textContent = j.answer || ""; if (!j.answer) wr.classList.remove("is-on"); })
          .catch(function () { wr.classList.remove("is-on"); });
      }
      try { history.replaceState(null, "", "?q=" + encodeURIComponent(text)); } catch (e) {}
    }, function () { st.textContent = "The transcripts did not load. Every one is also on its episode page in the library."; });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); ask(q.value); });
  sec.querySelectorAll(".tmw-try button").forEach(function (b) { b.addEventListener("click", function () { q.value = b.textContent; ask(b.textContent); }); });
  var pre = new URLSearchParams(location.search).get("q");
  if (pre) { q.value = pre; ask(pre); }
})();
"""


def main():
    eps, docs = episodes()
    out = os.path.join(V4, "samples")
    open(os.path.join(out, "tmw-index.js"), "w", encoding="utf-8").write(
        "/* Tell me why: the transcript passages (tools/v4_tellmewhy.py). eps: [slug, title, series]; docs: [episode, chapter id, time, speaker, chapter, text] */\n"
        "window.TMW=" + json.dumps({"eps": eps, "docs": docs}, ensure_ascii=False, separators=(",", ":")) + ";\n")
    open(os.path.join(out, "tmw.js"), "w", encoding="utf-8").write(JS)
    open(os.path.join(out, "tell-me-why.html"), "w", encoding="utf-8").write(page(len(eps), len(docs)))
    print("v4 tell me why: %d episodes, %d passages, index %d kB" % (len(eps), len(docs), os.path.getsize(os.path.join(out, "tmw-index.js")) // 1024))


if __name__ == "__main__":
    main()
