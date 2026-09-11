/* Sorting for the topic pages.
 *
 * THE RULE THIS OBEYS. Every episode is already in the served HTML, in
 * newest-first order, written by generate_tag_pages.py. This file only reorders
 * nodes that are already on the page. It never fetches, never hides and never
 * removes an item, so a crawler that does not run JavaScript sees exactly the
 * same episodes it always did. Do not "improve" this into something that
 * renders the list itself.
 *
 * The control is INJECTED by this script rather than written into the HTML by
 * the generator. If JavaScript does not run there is no sort bar at all, which
 * is better than a row of buttons that do nothing. Same reason the transcript
 * clip uses a .no-js escape hatch rather than trusting the script to arrive.
 *
 * Sort options are limited to what real data exists. episode-meta.json has a
 * publish date on 80 of 93 episodes and a title on all of them; duration is
 * empty on every single entry, so there is deliberately no "longest" or
 * "shortest" option. Adding one would mean inventing the data.
 *
 * The 13 episodes with no publish date are YouTube-only videos that never went
 * out on the podcast feed. On a date sort they are grouped at the end in both
 * directions rather than being treated as very old or very new, and the bar
 * says so, because silently scattering undated items through a date-ordered
 * list makes the order look wrong.
 */
(function () {
  "use strict";

  var list = document.querySelector(".tg-list");
  if (!list) return;

  var items = Array.prototype.slice.call(list.querySelectorAll(".tg-ep"));
  if (items.length < 2) return;            // nothing to sort

  var dated = items.filter(function (li) { return li.getAttribute("data-date"); });
  var undatedCount = items.length - dated.length;
  var canSortByDate = dated.length > 1;

  function val(li, attr) { return li.getAttribute(attr) || ""; }

  // Undated items keep their original relative order and always sit last.
  function byDate(dir) {
    return function (a, b) {
      var da = val(a, "data-date"), db = val(b, "data-date");
      if (!da && !db) return 0;
      if (!da) return 1;
      if (!db) return -1;
      if (da === db) return val(a, "data-title") < val(b, "data-title") ? -1 : 1;
      return da < db ? -dir : dir;
    };
  }

  function byTitle(dir) {
    return function (a, b) {
      var ta = val(a, "data-title"), tb = val(b, "data-title");
      if (ta === tb) return 0;
      return ta < tb ? -dir : dir;
    };
  }

  var MODES = [];
  if (canSortByDate) {
    MODES.push(["Newest", byDate(-1)]);
    MODES.push(["Oldest", byDate(1)]);
  }
  MODES.push(["A to Z", byTitle(1)]);
  MODES.push(["Z to A", byTitle(-1)]);

  var current = 0;

  var bar = document.createElement("div");
  bar.className = "tg-sort";
  bar.setAttribute("role", "group");
  bar.setAttribute("aria-label", "Sort episodes");

  var label = document.createElement("span");
  label.className = "tg-sort-label";
  label.textContent = "Sort";
  bar.appendChild(label);

  var buttons = MODES.map(function (mode, i) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "pill" + (i === 0 ? " on" : "");
    b.textContent = mode[0];
    b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
    b.addEventListener("click", function () { apply(i); });
    bar.appendChild(b);
    return b;
  });

  if (canSortByDate && undatedCount > 0) {
    var note = document.createElement("span");
    note.className = "tg-sort-note";
    note.textContent = undatedCount === 1
      ? "1 episode has no publish date and stays last on date sorts"
      : undatedCount + " episodes have no publish date and stay last on date sorts";
    bar.appendChild(note);
  }

  // A live region so a screen reader hears that the order changed. Without it
  // the reordering is completely silent and the buttons appear to do nothing.
  var status = document.createElement("p");
  status.className = "tg-sort-status";
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  bar.appendChild(status);

  function apply(i) {
    current = i;
    buttons.forEach(function (b, n) {
      b.classList.toggle("on", n === i);
      b.setAttribute("aria-pressed", n === i ? "true" : "false");
    });
    var sorted = items.slice().sort(MODES[i][1]);
    // One reflow rather than one per item.
    var frag = document.createDocumentFragment();
    sorted.forEach(function (li) { frag.appendChild(li); });
    list.appendChild(frag);
    status.textContent = items.length + " episodes, sorted by " + MODES[i][0];
  }

  list.parentNode.insertBefore(bar, list);
})();
