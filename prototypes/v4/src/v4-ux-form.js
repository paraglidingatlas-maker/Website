/* THE ENQUIRY FORM'S MESSAGES (the usability pass, 27). Inlined in enquire.html
   only, by tools/v4_ux.py. A send with fields missing showed the browser's own
   bubble on the first one alone; now each field that needs something says so
   under itself, in the page's own style (orange, as the form's other messages),
   in the browser's own words for it, and the first is brought into view and
   focused. A message goes as soon as its field is put right. The send itself
   (mailto, or the Worker when it is switched on) is the page's own script,
   untouched: this runs first and lets it through only when the form is ready.
   Without script the browser's own checks stand. */
(function () {
  var d = document, form = d.getElementById("enqForm");
  if (!form || !form.checkValidity) return;
  form.noValidate = true;
  var tried = false;
  function fields() {
    return [].filter.call(form.elements, function (el) {
      return el.willValidate && el.type !== "hidden" && el.type !== "submit" && !el.closest('[aria-hidden="true"]');
    });
  }
  function holder(el) { return el.type === "checkbox" ? el.closest(".enq-consent") || el.parentNode : el.closest(".enq-field") || el.parentNode; }
  function msg(el, make) {
    var id = (el.id || el.name) + "-err", m = d.getElementById(id);
    if (!m && make) {
      m = d.createElement("p");
      m.className = "enq-err"; m.id = id;
      var h = holder(el);
      if (el.type === "checkbox") h.parentNode.insertBefore(m, h.nextSibling); else h.appendChild(m);
    }
    return m;
  }
  function describe(el, on) {
    var ids = (el.getAttribute("aria-describedby") || "").split(" ").filter(Boolean), id = (el.id || el.name) + "-err";
    ids = ids.filter(function (x) { return x !== id; });
    if (on) ids.push(id);
    if (ids.length) el.setAttribute("aria-describedby", ids.join(" ")); else el.removeAttribute("aria-describedby");
  }
  function check(el) {
    var bad = !el.checkValidity();
    var m = msg(el, bad);
    if (bad) { m.textContent = el.validationMessage; el.setAttribute("aria-invalid", "true"); }
    else { if (m) m.parentNode.removeChild(m); el.removeAttribute("aria-invalid"); }
    describe(el, bad);
    return !bad;
  }
  d.addEventListener("submit", function (e) {
    if (e.target !== form) return;
    tried = true;
    var first = null;
    fields().forEach(function (el) { if (!check(el) && !first) first = el; });
    if (!first) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    first.focus({ preventScroll: true });
    first.scrollIntoView({ block: "center", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }, true);
  function again(e) { if (tried && e.target.form === form && e.target.willValidate) check(e.target); }
  form.addEventListener("input", again);
  form.addEventListener("change", again);
})();
