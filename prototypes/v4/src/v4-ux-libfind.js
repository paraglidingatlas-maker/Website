/* THE LIBRARY SEARCH'S EXTRAS (the usability pass, 17). Appended to
   library-find.js by tools/v4_search.py, so it arrives with the words it
   uses, on the first press or keystroke in the library's search (v2-library.js
   fetches it and calls V4_LIBFIND_UI after each search, through V4_LIB). On
   arrival: each card's search words take the episode's topics, chapter titles
   and summary, and the search runs again. Then, after each search, the first
   results under the field, at the top of the page; when nothing matches, the
   topics that do. Its styles come with it, so the library does not carry them
   on arrival. */
window.V4_LIBFIND_UI = (function () {
  var L = window.V4_LIB, FIND = window.V4_LIBFIND || { eps: {}, topics: [] }, $ = L.$, norm = L.norm;
  var css = document.createElement("style");
  css.textContent = window.V4_LIBFIND_CSS || "";
  document.head.appendChild(css);
  L.cards.forEach(function (c) {
    var x = FIND.eps[(c.getAttribute("href") || "").replace(/^.*?(episodes\/)/, "$1")];
    if (x) c.dataset.f += " " + x;
  });
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function topicsFor(words) {
    var out = [];
    if (words.length) FIND.topics.forEach(function (t) {
      var n = norm(t[0]);
      if (out.length < 6 && words.some(function (w) { return w.length > 2 && (n.indexOf(w) !== -1 || w.indexOf(n) !== -1); })) out.push(t);
    });
    if (!out.length) return '<p class="v4u-topics"><a class="v4u-topics-all" href="tags.html">Topics</a></p>';
    return '<p class="v4u-topics"><span>Topics</span> ' + out.map(function (t) {
      return '<a class="tg-chip" href="' + esc(t[1]) + '">' + esc(t[0]) + " <i>" + t[2] + "</i></a>";
    }).join(" ") + "</p>";
  }
  setTimeout(function () { if (L.state.q) L.draw(false); }, 0);
  return function (words, hits) {
    var none = $("none"), heroHits = $("qHits");
    if (none) {
      var old = none.querySelector(".v4u-topics");
      if (old) old.remove();
      if (!hits.length) none.insertAdjacentHTML("beforeend", topicsFor(words));
    }
    if (!heroHits) return;
    if (!words.length) { heroHits.innerHTML = ""; return; }
    if (!hits.length) { heroHits.innerHTML = '<li class="v4-hit-none">Nothing matches those filters. ' + topicsFor(words) + "</li>"; return; }
    heroHits.innerHTML = hits.slice(0, 5).map(function (c) {
      var t = c.querySelector(".ep-tile-title"), g = c.querySelector(".ep-log-guest"), no = c.querySelector(".ep-no");
      return '<li><a href="' + esc(c.getAttribute("href")) + '"><span class="v4-hit-k">' + esc(no ? no.textContent : "") +
        '</span><span class="v4-hit-t">' + esc(t ? t.textContent : "") + (g && g.textContent ? ' <span class="v4-hit-s">' + esc(g.textContent) + "</span>" : "") + "</span></a></li>";
    }).join("") + (hits.length > 5 ? '<li class="v4u-hits-all"><a href="#browse">See all ' + hits.length + " episodes</a></li>" : "");
  };
})();
