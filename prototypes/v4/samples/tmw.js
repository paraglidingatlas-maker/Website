/* Tell me why (tools/v4_tellmewhy.py): BM25 over the transcript passages, on the
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
