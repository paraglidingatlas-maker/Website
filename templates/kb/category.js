<script>
/* Flight Mechanics: immersive layer. Ambient canvas, reading progress, reveal on
   scroll, gentle parallax and a pointer light. Transform and opacity only, one
   rAF per scroll, and it all stands down for prefers-reduced-motion. */
(function () {
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var atm = d.createElement("div"); atm.className = "kb-atmos"; atm.setAttribute("aria-hidden", "true");
  atm.innerHTML = '<i class="g1"></i><i class="g2"></i><i class="g3"></i>'; d.body.insertBefore(atm, d.body.firstChild);
  var bar = d.createElement("div"); bar.className = "kb-progress"; bar.setAttribute("aria-hidden", "true"); d.body.appendChild(bar);

  if ("IntersectionObserver" in window && !reduce) {
    root.classList.add("kr-on");
    var groups = [".k-head", ".band .l", ".band .r", ".bf-q", ".band-draw", ".check", ".tk-lab", ".tk-row .cardx",
                  ".faq-l", ".faq-r details", ".nx a", "#episodes .ep-tile"];
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; el.classList.add("in"); io.unobserve(el);
        /* hand the element back to its own hover transforms once it has arrived */
        setTimeout(function () { el.classList.remove("kr"); el.style.removeProperty("--d"); }, 1900);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    groups.forEach(function (sel) {
      var list = d.querySelectorAll(sel), parents = [];
      Array.prototype.forEach.call(list, function (el) {
        var p = el.parentNode, i = parents.indexOf(p); if (i < 0) { parents.push(p); p._kri = 0; }
        el.classList.add("kr"); el.style.setProperty("--d", Math.min(p._kri++ * 0.07, 0.42) + "s"); io.observe(el);
      });
    });
    Array.prototype.forEach.call(d.querySelectorAll(".bf-media, .band-draw"), function (el) { el.classList.add("kr-wipe"); if (!el.classList.contains("kr")) { el.classList.add("kr"); io.observe(el); } });
  }

  var nums = Array.prototype.slice.call(d.querySelectorAll(".band .num")), ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY || root.scrollTop, vh = window.innerHeight, h = root.scrollHeight - vh;
    root.style.setProperty("--p", h > 0 ? Math.min(1, y / h).toFixed(4) : 0);
    if (reduce) return;
    atm.style.setProperty("--gy", (-(y * 0.08) % 60).toFixed(1) + "px");
    atm.style.setProperty("--g1", (Math.sin(y / 1300) * 22 * vh / 100).toFixed(1) + "px");
    atm.style.setProperty("--g2", (Math.cos(y / 1700) * 18 * vh / 100 + y * 0.02 % 1).toFixed(1) + "px");
    atm.style.setProperty("--g3", (Math.sin(y / 2100) * 12 * window.innerWidth / 100).toFixed(1) + "px");
    if (y < vh * 1.2) { root.style.setProperty("--hy", (y * 0.16).toFixed(1) + "px"); root.style.setProperty("--hs", (1 + y * 0.00007).toFixed(4)); }
    for (var i = 0; i < nums.length; i++) {
      var r = nums[i].parentNode.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) continue;
      nums[i].style.setProperty("--py", ((r.top - vh * 0.5) * -0.09).toFixed(1) + "px");
    }
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  window.addEventListener("resize", frame, { passive: true }); frame();

  d.addEventListener("pointermove", function (e) {
    var c = e.target.closest && e.target.closest(".cardx, .nx a, .check"); if (!c) return;
    var r = c.getBoundingClientRect(); c.style.setProperty("--mx", (e.clientX - r.left) + "px"); c.style.setProperty("--my", (e.clientY - r.top) + "px");
  }, { passive: true });
})();
</script>