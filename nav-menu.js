/* Mobile nav toggle.
 *
 * The four header links were display:none below 820px and nothing replaced them,
 * so About Us, Knowledge Base, Podcast and Sitemap were unreachable from the top
 * of all 181 pages on a phone. This adds the control that opens them.
 *
 * The button is built here rather than written into the markup because that
 * markup is duplicated across 181 files and emitted by four generators; the same
 * reasoning as the flex order note in styles.css. One file, every page.
 *
 * The button is inserted BEFORE .nav-links in the DOM and moved to the far right
 * with flex order. That way Tab runs logo, button, menu items, in the order they
 * are read, and no focus juggling is needed when the panel opens.
 */
(function () {
  "use strict";

  function init() {
    var nav = document.querySelector(".page-wrap > nav");
    if (!nav) return;
    var links = nav.querySelector(".nav-links");
    if (!links || nav.querySelector(".nav-toggle")) return;

    if (!links.id) links.id = "nav-links";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "nav-toggle";
    btn.setAttribute("aria-label", "Open menu");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", links.id);
    btn.innerHTML = '<span class="nav-toggle-bars" aria-hidden="true">' +
                    "<i></i><i></i><i></i></span>";
    links.parentNode.insertBefore(btn, links);

    function setOpen(open) {
      nav.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      setOpen(btn.getAttribute("aria-expanded") !== "true");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" && e.key !== "Esc") return;
      if (btn.getAttribute("aria-expanded") !== "true") return;
      setOpen(false);
      btn.focus();
    });

    document.addEventListener("click", function (e) {
      if (btn.getAttribute("aria-expanded") !== "true") return;
      if (nav.contains(e.target)) return;
      setOpen(false);
    });

    // Following a link should not leave the panel open behind the new page on a
    // same-page anchor, and the panel must not survive a rotate back to desktop.
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 940) setOpen(false);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
