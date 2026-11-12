/* v4-share.js: one Share button for every photo and film (owner, 12 Nov 2026).
   Any element with [data-share] shares a link. Where the browser has a share sheet (phones, Safari, Chrome and Edge on
   Windows and Mac) it opens the device's own sheet: every app and contact the visitor has. Elsewhere a small panel
   offers Copy link, WhatsApp, Telegram, Email, Facebook and X.
   The link: data-share-url (relative or absolute), or else the film in the same block ([data-vid] -> its YouTube
   link), or else the page itself. The title: data-share-title, or the block's heading, or the page's title. */
(function (w, d) {
  "use strict";
  var YT = "https://www.youtube.com/watch?v=";
  var ICON = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2.5v10M6.2 6.3 10 2.5l3.8 3.8M4 10.5V16a1.5 1.5 0 0 0 1.5 1.5h9A1.5 1.5 0 0 0 16 16v-5.5"/></svg>';
  var pop, last;

  function abs(u) { try { return new URL(u, location.href).href; } catch (e) { return location.href; } }
  function what(b) {
    var box = b.closest("[data-share-box], .md-now, .ev-ch, .gffv, .gfv, section, article") || d.body;
    var url = b.getAttribute("data-share-url"), vid;
    if (!url) { vid = box.querySelector("[data-vid]") || (box.parentNode && box.parentNode.querySelector("[data-vid]")); url = vid ? YT + vid.getAttribute("data-vid") : location.href.split("#")[0]; }
    var t = b.getAttribute("data-share-title");
    if (!t) { var h = box.querySelector("[data-t], h3, h2, .gffv-t"); t = h ? h.textContent.trim() : ""; }
    var page = d.title;
    t = t ? t + " · " + page.replace(/: Paragliding Atlas$/, "") : page;
    return { url: abs(url), title: t, text: b.getAttribute("data-share-text") || t };
  }

  function build() {
    pop = d.createElement("div");
    pop.className = "v4sh"; pop.hidden = true; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Share");
    pop.innerHTML = '<div class="v4sh-in"><p class="v4sh-k">Share</p><p class="v4sh-t"></p>' +
      '<button class="v4sh-copy" type="button"><span>Copy link</span></button><div class="v4sh-apps"></div>' +
      '<button class="v4sh-x" type="button" aria-label="Close"></button></div>';
    d.body.appendChild(pop);
    // the photo viewer and the film theatre listen for clicks, swipes and keys: the panel keeps its own
    ["pointerdown", "pointerup", "touchstart", "wheel"].forEach(function (t) { pop.addEventListener(t, function (e) { e.stopPropagation(); }, { passive: true }); });
    pop.addEventListener("click", function (e) {
      e.stopPropagation();
      if (e.target === pop || e.target.closest(".v4sh-x")) return close();
      var c = e.target.closest(".v4sh-copy");
      if (c) {
        var s = c.querySelector("span"), u = pop._u;
        var done = function () { s.textContent = "Link copied"; setTimeout(function () { s.textContent = "Copy link"; }, 1800); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(done, function () { prompt("Copy this link", u); });
        else prompt("Copy this link", u);
      }
    });
  }
  function close() { pop.hidden = true; if (last) try { last.focus(); } catch (e) {} }
  function panel(s, b) {
    if (!pop) build();
    var u = encodeURIComponent(s.url), t = encodeURIComponent(s.title);
    var apps = [["WhatsApp", "https://wa.me/?text=" + t + "%20" + u], ["Telegram", "https://t.me/share/url?url=" + u + "&text=" + t],
                ["Email", "mailto:?subject=" + t + "&body=" + t + "%0A%0A" + u], ["Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + u],
                ["X", "https://twitter.com/intent/tweet?url=" + u + "&text=" + t]];
    pop._u = s.url;
    pop.querySelector(".v4sh-t").textContent = s.title;
    pop.querySelector(".v4sh-apps").innerHTML = apps.map(function (a) {
      return '<a href="' + a[1] + '" target="_blank" rel="noopener">' + a[0] + "</a>";
    }).join("");
    // inside an open <dialog> (the photo viewer, the film theatre) the panel must live in it to be seen and clicked
    var host = b.closest("dialog[open]") || d.body;
    if (pop.parentNode !== host) host.appendChild(pop);
    last = b; pop.hidden = false;
    pop.querySelector(".v4sh-copy").focus();
  }

  d.addEventListener("click", function (e) {
    var b = e.target.closest("[data-share]");
    if (!b) return;
    e.preventDefault(); e.stopPropagation();
    var s = what(b), data = { title: s.title, text: s.text, url: s.url };
    if (navigator.share && (!navigator.canShare || navigator.canShare(data))) {
      navigator.share(data).catch(function (err) { if (err && err.name !== "AbortError") panel(s, b); });
    } else panel(s, b);
  }, true);

  d.addEventListener("keydown", function (e) { if (pop && !pop.hidden && e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(); } }, true);

  // buttons written as <button data-share></button> get the icon and the word
  function dress(root) {
    [].forEach.call((root || d).querySelectorAll("[data-share]:empty"), function (b) {
      b.innerHTML = ICON + "<span>Share</span>";
      if (!b.getAttribute("aria-label")) b.setAttribute("aria-label", "Share");
    });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", function () { dress(); }); else dress();
  w.v4Share = { dress: dress };
})(window, document);
