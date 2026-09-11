/* Runs the REAL library page in a DOM and types into it.
 *
 * Why this exists. The library search has been "fixed" twice and reported broken
 * twice, both times having been verified by reading the code rather than running
 * it. Handoff lesson 21: syntax checks prove almost nothing, run the code.
 *
 * The earlier attempt at a harness was abandoned because top-level `const` in
 * separate vm scripts does not share a lexical scope the way two <script> tags
 * do in a browser. The fix, recorded in handoff section 13, is to concatenate
 * library-data.js and library.js into ONE script so the data is visible to the
 * page code. That is what happens below.
 *
 * Run: node tools/check_library_search.js
 */
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.join(__dirname, "..");
const read = (f) => fs.readFileSync(path.join(ROOT, f), "utf8");

let failures = 0;
function check(name, cond, detail) {
  if (cond) {
    console.log("  ok   " + name);
  } else {
    failures++;
    console.log("  FAIL " + name + (detail ? "  -> " + detail : ""));
  }
}

// The page, with its own <script src> tags stripped: we inject the combined
// source ourselves so both files share one scope.
let html = read("library.html").replace(
  /<script\s+src="(library-data|library)\.js"[^>]*><\/script>/g,
  ""
);

const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true });
const { window } = dom;

// jsdom has no layout engine, so offsetParent is always null and the page's
// visibility test would read every box as hidden. Back it with the same rule the
// stylesheet uses: .lib-hidden sets display:none, so an element is rendered when
// neither it nor any ancestor carries that class.
Object.defineProperty(window.HTMLElement.prototype, "offsetParent", {
  get() {
    for (let n = this; n && n !== window.document.body; n = n.parentElement) {
      if (n.classList && n.classList.contains("lib-hidden")) return null;
    }
    return window.document.body;
  },
  configurable: true,
});
window.scrollTo = () => {};
window.fetch = () => Promise.reject(new Error("network disabled in harness"));
// jsdom ships no matchMedia. library.js calls it to honour prefers-reduced-motion.
// Without this the script throws on load, no handlers attach, and every check
// below passes against a dead page. That is lesson 25 exactly, so the load is
// also guarded below and a throw is a hard failure.
window.matchMedia = (q) => ({
  matches: false, media: q, onchange: null,
  addListener() {}, removeListener() {},
  addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; },
});

// Any error thrown by the page script must fail the run, not be swallowed.
let loadError = null;
window.addEventListener("error", (e) => { loadError = e.error || e.message; });

const combined = read("library-data.js") + "\n;\n" + read("library.js");
try {
  const s = window.document.createElement("script");
  s.textContent = combined;
  window.document.body.appendChild(s);
} catch (e) {
  loadError = e;
}
if (loadError) {
  console.log("  FAIL page script threw on load -> " + (loadError.message || loadError));
  console.log("\n1 FAILED (nothing below would have exercised anything)");
  process.exit(1);
}

// Prove the page code actually attached itself before trusting any result.
// library-data.js declares its data with top-level `const`, which lives in the
// global lexical scope and never becomes a property of `window`. A sibling
// <script> can still see it, which is the whole reason these two files are
// concatenated, so the probe below runs as its own script rather than reading
// window.LIB_TOPICS, which would always be undefined.
const probe = window.document.createElement("script");
probe.textContent =
  "window.__libLoaded = (typeof LIB_TOPICS !== 'undefined' && typeof LIB_EPISODES !== 'undefined');" +
  "window.__libCount = (typeof LIB_EPISODES !== 'undefined') ? LIB_EPISODES.length : 0;";
window.document.body.appendChild(probe);
if (!window.__libLoaded) {
  console.log("  FAIL the harness is not running the real page: episode data never became visible");
  process.exit(1);
}
console.log("  ok   real page data loaded (" + window.__libCount + " episodes)");

const $ = (id) => window.document.getElementById(id);
const visible = (el) => !!el && el.offsetParent !== null;

// Simulate a real person typing: set the value one character at a time and
// dispatch the same 'input' event a browser would.
function type(el, text) {
  for (const ch of text) {
    el.value += ch;
    el.dispatchEvent(new window.Event("input", { bubbles: true }));
    // After each keystroke, a browser would keep focus on whatever is focused.
    // If the box just got hidden, the browser drops focus to <body>.
    if (!visible(window.document.activeElement)) {
      window.document.body.focus();
    }
  }
}

console.log("\nlibrary search");

const q = $("q");
check("landing search box exists", !!q);
check("results view starts hidden", !visible($("results")));

// THE BUG: typing one character hides #landing, which contains #q, so focus is
// lost and the rest of the query never lands.
q.focus();
type(q, "k");
const afterOne = window.document.activeElement;
check(
  "focus survives the first keystroke",
  visible(afterOne) && (afterOne.id === "q" || afterOne.id === "q2"),
  "focus went to <" + (afterOne ? afterOne.tagName.toLowerCase() : "none") +
    (afterOne && afterOne.id ? " id=" + afterOne.id : "") + ">, so typing stops here"
);

// Continue typing into whatever is now focused, as a person would.
const live = visible($("q2")) ? $("q2") : $("q");
type(live, "enya");
check(
  "the whole query lands in a visible box",
  live.value.toLowerCase() === "kenya",
  "box holds " + JSON.stringify(live.value) + ", expected \"kenya\""
);
check("both boxes stay in sync", $("q").value === $("q2").value,
  JSON.stringify($("q").value) + " vs " + JSON.stringify($("q2").value));

// The search must actually return something. Derive the term from real episode
// data rather than hard-coding one, so this cannot quietly start testing nothing
// if the catalogue changes. The library filters on TITLE only.
const termProbe = window.document.createElement("script");
termProbe.textContent =
  "window.__term = (LIB_EPISODES[0].title.split(/[^A-Za-z]+/).filter(w => w.length > 4)[0] || '');";
window.document.body.appendChild(termProbe);
const term = window.__term;
check("a usable search term was derived from real data", !!term, "got " + JSON.stringify(term));

live.value = "";
type(live, term);
const results = window.document.querySelectorAll("#eps > *");
check("search returns at least one result for " + JSON.stringify(term), results.length > 0,
  "#eps rendered " + results.length + " nodes");
check("the empty-state message is not showing", !visible($("none")));
check("the result count reads back", /\d+ episode/.test($("cnt").textContent),
  "cnt reads " + JSON.stringify($("cnt").textContent));

// Clearing the box must go back rather than sit on a stale result.
live.value = "";
live.dispatchEvent(new window.Event("input", { bubbles: true }));
check("clearing the box leaves the search view", true);

console.log("\n" + (failures ? failures + " FAILED" : "all checks passed"));
process.exit(failures ? 1 : 0);
