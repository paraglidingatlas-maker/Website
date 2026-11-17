/* The site in other languages (tools/v4_i18n.py, chat 27): the words the page's own scripts write after it
   loads (a countdown, the photo viewer's buttons, Share, a form's replies). The page carries its checked
   dictionary as JSON (#v4-i18n-d: exact strings, and patterns where {1} stands for a part that is itself
   looked up, or kept as it is); this swaps a text or a label that matches, as the scripts write it. Dates
   the scripts write ("18 to 29 Jan 2027") are put in the language's own format by the browser. Nothing
   that is sent (the enquiry's email, the form's values) is touched. */
(function () {
  var D = document, el = D.getElementById("v4-i18n-d");
  if (!el || !window.MutationObserver) return;
  var C;
  try { C = JSON.parse(el.textContent); } catch (e) { return; }
  var LANG = C.lang, EX = C.exact || {}, PAT = [];
  (C.pat || []).forEach(function (p) {
    var parts = p[0].split(/\{(\d+)\}/), rx = "^", order = [];
    for (var i = 0; i < parts.length; i++) {
      if (i % 2) { rx += "(.+?)"; order.push(+parts[i]); }
      else rx += parts[i].replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }
    PAT.push([new RegExp(rx + "$"), order, p[1]]);
  });
  var MON = { jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5, jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11 };
  var MRX = "(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)";
  var R2 = new RegExp("\\b(\\d{1,2}) " + MRX + " to (\\d{1,2}) " + MRX + "(?: (\\d{4}))?\\b", "g");
  var R1 = new RegExp("\\b(\\d{1,2}) ?(?:to|–|-) ?(\\d{1,2}) " + MRX + "(?: (\\d{4}))?\\b", "g");
  var R0 = new RegExp("\\b(\\d{1,2}) " + MRX + "(?: (\\d{4}))?\\b", "g");
  var RM = /\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})\b/g;
  function mo(s) { return MON[s.slice(0, 3).toLowerCase()]; }
  function fmt(o) { try { return new Intl.DateTimeFormat(LANG, o); } catch (e) { return null; } }
  function range(a, b, y, longM) {
    var o = { day: "numeric", month: longM ? "long" : "short" }; if (y) o.year = "numeric";
    var f = fmt(o); if (!f) return null;
    return f.formatRange ? f.formatRange(a, b) : f.format(a) + " – " + f.format(b);
  }
  function dates(s) {
    var hit = false;
    s = s.replace(R2, function (m, d1, m1, d2, m2, y) { var Y = +(y || 2027), r = range(new Date(Y, mo(m1), +d1), new Date(Y, mo(m2), +d2), y); if (!r) return m; hit = true; return r; });
    s = s.replace(R1, function (m, d1, d2, m1, y) { var Y = +(y || 2027), r = range(new Date(Y, mo(m1), +d1), new Date(Y, mo(m1), +d2), y, m1.length > 4); if (!r) return m; hit = true; return r; });
    s = s.replace(R0, function (m, d, m1, y) { var o = { day: "numeric", month: m1.length > 4 ? "long" : "short" }; if (y) o.year = "numeric"; var f = fmt(o); if (!f) return m; hit = true; return f.format(new Date(+(y || 2027), mo(m1), +d)); });
    s = s.replace(RM, function (m, m1, y) { var f = fmt({ month: "long", year: "numeric" }); if (!f) return m; hit = true; return f.format(new Date(+y, mo(m1), 1)); });
    return hit ? s : null;
  }
  function one(s, deep) {
    if (EX.hasOwnProperty(s)) return EX[s];
    for (var i = 0; i < PAT.length; i++) {
      var m = PAT[i][0].exec(s);
      if (!m) continue;
      var out = PAT[i][2], ok = true;
      out = out.replace(/\{(\d+)\}/g, function (_, n) {
        var k = PAT[i][1].indexOf(+n), v = k >= 0 ? m[k + 1] : "";
        var t = deep < 3 ? one(v, deep + 1) : null;
        return t != null ? t : (dates(v) || v);
      });
      if (ok) return out;
    }
    if (!deep) {
      var d = dates(s);
      // a date alone, or dates with commas and "and" between them
      if (d != null && !/[A-Za-z]{3,}/.test(s.replace(new RegExp(MRX, "g"), "").replace(/\band\b|\bto\b/g, ""))) return d;
    }
    return null;
  }
  function tr(s) {
    var t = s.replace(/\s+/g, " ").trim();
    if (!t || !/[A-Za-z]{2}/.test(t)) return null;
    var r = one(t, 0);
    if (r == null || r === t) return null;
    var lead = s.match(/^\s*/)[0], trail = s.match(/\s*$/)[0];
    return lead + r + trail;
  }
  var SKIP = /^(SCRIPT|STYLE|TEXTAREA|NOSCRIPT|CODE)$/, ATTR = ["aria-label", "title", "placeholder", "alt"];
  function text(n) {
    var p = n.parentNode;
    if (!p || SKIP.test(p.nodeName) || (p.closest && p.closest("[translate=no],.v4-lang"))) return;
    var r = tr(n.data);
    if (r != null) n.data = r;
  }
  function attrs(e) {
    if (e.closest && e.closest(".v4-lang")) return;
    for (var i = 0; i < ATTR.length; i++) {
      var v = e.getAttribute(ATTR[i]);
      if (v) { var r = tr(v); if (r != null) e.setAttribute(ATTR[i], r); }
    }
  }
  function walk(root) {
    if (root.nodeType === 3) { text(root); return; }
    if (root.nodeType !== 1 || SKIP.test(root.nodeName)) return;
    attrs(root);
    var w = D.createTreeWalker(root, 5, null), n;
    while ((n = w.nextNode())) { if (n.nodeType === 3) text(n); else if (!SKIP.test(n.nodeName)) attrs(n); }
  }
  var mo2 = new MutationObserver(function (list) {
    for (var i = 0; i < list.length; i++) {
      var r = list[i];
      if (r.type === "characterData") text(r.target);
      else if (r.type === "attributes") attrs(r.target);
      else for (var j = 0; j < r.addedNodes.length; j++) walk(r.addedNodes[j]);
    }
  });
  mo2.observe(D.documentElement, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTR });
  function all() { if (D.body) walk(D.body); }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", all); else all();
})();
