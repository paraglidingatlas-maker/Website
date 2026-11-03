/* Media, designer D (Trim), "Clean Feed": the three things this page needs a script for. Without it the page is
   finished: the tally reads "Next on air", a package's "Check dates" lands on the form, the phone bar stays away. */
(function () {
  "use strict";
  function ready(f) { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", f); else f(); }
  ready(function () {
    /* the tally light is lit only while the event is on air (its task days), and goes once the event is over */
    var t = document.querySelector(".mdd-tally[data-live-from]");
    if (t) {
      var n = new Date(), day = new Date(n.getFullYear(), n.getMonth(), n.getDate());
      var from = new Date(t.getAttribute("data-live-from") + "T00:00:00"), to = new Date(t.getAttribute("data-live-to") + "T00:00:00");
      if (day >= from && day <= to) { t.classList.add("is-live"); t.querySelector(".mdd-tally-k").textContent = "On air now"; }
      else if (day > to) t.hidden = true;
    }

    /* a package's "Check dates" lands on the form with that package chosen */
    var sel = document.getElementById("f-package");
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-package]");
      if (!a || !sel) return;
      var want = a.getAttribute("data-package");
      for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === want) sel.selectedIndex = i;
    });

    /* the phone's bar (the episode pages' bar): once the opening's button has gone by, until the form comes up */
    var bar = document.querySelector(".mdd-bar"), act = document.querySelector(".mdd-act"), book = document.getElementById("dates");
    if (bar && act && book && "IntersectionObserver" in window) {
      var past = false, done = false;
      var set = function () { bar.classList.toggle("show", past && !done); };
      new IntersectionObserver(function (en) { var r = en[0]; past = !r.isIntersecting && r.boundingClientRect.top < 0; set(); }).observe(act);
      new IntersectionObserver(function (en) { var r = en[0]; done = r.isIntersecting || r.boundingClientRect.top < 0; set(); },
        { rootMargin: "0px 0px -15% 0px" }).observe(book);
    }
  });
})();
