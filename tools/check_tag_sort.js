/* Runs the REAL topic page sort control and checks it.
 *
 * Run: NODE_PATH=/path/to/node_modules node tools/check_tag_sort.js
 * jsdom is a dev dependency. Do NOT symlink or commit node_modules: doing that
 * once broke two GitHub Pages deploys, because Pages rejects symlinks pointing
 * outside the repository and a failed build keeps serving the last good one.
 *
 * The check that matters most here is the LAST one. Sorting reorders nodes that
 * are already in the served HTML; it must never drop one. If a future change
 * turns this into something that renders the list itself, episode count will
 * stop matching and this fails.
 */
const fs = require("fs");
const path = require("path");
let JSDOM;
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  console.error("jsdom is not installed.  npm install jsdom  (never commit it)");
  process.exit(2);
}

const ROOT = path.join(__dirname, "..");
let failures = 0;
function check(name, cond, detail) {
  if (cond) console.log("  ok   " + name);
  else { failures++; console.log("  FAIL " + name + (detail ? "  -> " + detail : "")); }
}

// Pick the tag page with the most episodes, so the sort is exercised properly
// rather than on a three-item list where almost any order looks plausible.
const dir = path.join(ROOT, "tags");
let best = null;
for (const f of fs.readdirSync(dir)) {
  const html = fs.readFileSync(path.join(dir, f), "utf8");
  const n = (html.match(/class="tg-ep"/g) || []).length;
  if (!best || n > best.n) best = { f, n, html };
}
console.log(`\ntag page sort  (${best.f}, ${best.n} episodes)`);

const dom = new JSDOM(best.html, { runScripts: "dangerously", pretendToBeVisual: true });
const { window } = dom;
const doc = window.document;

const before = Array.from(doc.querySelectorAll(".tg-ep"));
const beforeHrefs = before.map((li) => li.querySelector("a").getAttribute("href"));
check("page ships every episode in the HTML before any script runs", before.length > 1,
  before.length + " items");

// Run the real script.
const script = doc.createElement("script");
script.textContent = fs.readFileSync(path.join(ROOT, "tags-sort.js"), "utf8");
doc.body.appendChild(script);

const bar = doc.querySelector(".tg-sort");
check("sort control was injected", !!bar);
if (!bar) { console.log("\n1 FAILED"); process.exit(1); }

const pills = Array.from(bar.querySelectorAll(".pill"));
check("four sort options offered", pills.length === 4,
  pills.map((p) => p.textContent).join(", "));
check("no duration option offered, since no episode has a duration",
  !pills.some((p) => /long|short|length|duration/i.test(p.textContent)));
check("first option starts active", pills[0].classList.contains("on"));

function order() {
  return Array.from(doc.querySelectorAll(".tg-ep"));
}
function titles() { return order().map((li) => li.getAttribute("data-title")); }
function dates() { return order().map((li) => li.getAttribute("data-date")); }

// A to Z
const az = pills.find((p) => p.textContent === "A to Z");
az.dispatchEvent(new window.Event("click", { bubbles: true }));
const t = titles();
const sortedT = t.slice().sort();
check("A to Z actually orders the list alphabetically",
  JSON.stringify(t) === JSON.stringify(sortedT),
  "first three: " + t.slice(0, 3).join(" | "));
check("A to Z marks itself active and clears the others",
  az.classList.contains("on") && pills.filter((p) => p.classList.contains("on")).length === 1);

// Z to A must be the exact reverse
pills.find((p) => p.textContent === "Z to A")
  .dispatchEvent(new window.Event("click", { bubbles: true }));
check("Z to A is the reverse of A to Z",
  JSON.stringify(titles()) === JSON.stringify(sortedT.slice().reverse()));

// Oldest: dated items ascending, undated pushed to the end.
pills.find((p) => p.textContent === "Oldest")
  .dispatchEvent(new window.Event("click", { bubbles: true }));
const d = dates();
const firstBlank = d.findIndex((x) => !x);
const datedPart = firstBlank === -1 ? d : d.slice(0, firstBlank);
const tailPart = firstBlank === -1 ? [] : d.slice(firstBlank);
check("Oldest puts dated episodes in ascending order",
  JSON.stringify(datedPart) === JSON.stringify(datedPart.slice().sort()),
  datedPart.slice(0, 3).join(" | "));
check("undated episodes are grouped at the end, not scattered",
  tailPart.every((x) => !x), tailPart.length + " undated in the tail");

// Newest
pills.find((p) => p.textContent === "Newest")
  .dispatchEvent(new window.Event("click", { bubbles: true }));
const d2 = dates().filter(Boolean);
check("Newest puts dated episodes in descending order",
  JSON.stringify(d2) === JSON.stringify(d2.slice().sort().reverse()),
  d2.slice(0, 3).join(" | "));

// THE ONE THAT MATTERS: nothing may ever be lost.
const afterHrefs = order().map((li) => li.querySelector("a").getAttribute("href"));
check("every episode survives every sort, none dropped or duplicated",
  afterHrefs.length === beforeHrefs.length &&
  JSON.stringify(afterHrefs.slice().sort()) === JSON.stringify(beforeHrefs.slice().sort()),
  afterHrefs.length + " after vs " + beforeHrefs.length + " before");

check("a screen reader is told the order changed",
  !!doc.querySelector(".tg-sort-status") &&
  /sorted by/.test(doc.querySelector(".tg-sort-status").textContent));

console.log("\n" + (failures ? failures + " FAILED" : "all checks passed"));
process.exit(failures ? 1 : 0);
