/* Mandated check 2 for the sitemap.
   Inside the per node group the transform is already translate(n.x, n.y), so
   every coordinate in there is RELATIVE to the node. Using n.x or n.y inside
   applies the offset twice and flings the label off screen.

   This scans only the block that builds that group, from the line that sets the
   group's transform to the line that appends it. A whole file grep is useless
   here: edges, the camera and the layout all use n.x legitimately.

   Usage: node tools/check_sitemap_static.js */

const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'sitemap-graph.js'), 'utf8');
const lines = src.split('\n');

const startIdx = lines.findIndex((l) => /grp\.setAttribute\(\s*"transform"\s*,\s*"translate\("/.test(l));
if (startIdx === -1) {
  console.error('FAIL: could not find the node group transform. The draw code moved; fix this check.');
  process.exit(1);
}
let endIdx = -1;
for (let i = startIdx; i < lines.length; i++) {
  if (/g\.appendChild\(grp\)/.test(lines[i])) { endIdx = i; break; }
}
if (endIdx === -1) {
  console.error('FAIL: could not find where the node group is appended. Fix this check.');
  process.exit(1);
}

const offenders = [];
for (let i = startIdx + 1; i < endIdx; i++) {
  const line = lines[i];
  if (/^\s*\/[/*]/.test(line)) continue;          // comment
  const m = line.match(/\bn\.(x|y)\b/);
  if (m) offenders.push({ line: i + 1, text: line.trim() });
}

console.log(`scanned the node group block, lines ${startIdx + 1} to ${endIdx + 1}`);
if (offenders.length) {
  console.error('FAIL: absolute n.x / n.y used inside the translated node group');
  offenders.forEach((o) => console.error(`   L${o.line}: ${o.text.slice(0, 110)}`));
  process.exit(1);
}
console.log('PASS: nothing inside the node group uses absolute n.x / n.y');
