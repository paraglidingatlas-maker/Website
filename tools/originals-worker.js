/**
 * Paragliding Atlas: full-size photo originals (owner, 9 Nov 2026)
 *
 * The comp galleries' "Original, full size" link points here:
 *     https://<this worker>/SRS_6_T1_62.jpg
 * and the visitor's browser simply downloads SRS_6_T1_62.jpg. The worker finds that photo in the owner's
 * link-shared Drive folder (and its subfolders, one per task), fetches it and streams it back under the
 * site's own file name. The visitor never sees Drive: no Drive page, no Drive link, no Drive file name.
 *
 * Setup (Cloudflare dashboard, once): Workers & Pages > Create > Worker > name it (e.g. atlas-originals) >
 * Deploy > Edit code > paste this file > Deploy. Then Settings > Variables and Secrets > Add > type Secret,
 * name FOLDERS, value: the comp's Drive folder ID (the part after /folders/ in its link). Several comps:
 * separate the IDs with commas. The IDs live only in Cloudflare, never in this repository or on the site.
 *
 * Locked down: only names shaped like the site's photo names (SRS_6_T1_62, SRS_6_T1_62-2) are served, and
 * only from the folders named in FOLDERS, so the worker cannot be used to fetch anything else.
 */

const NAME = /^SRS_\d+_T\d+_\d+(?:-\d+)?$/;
const PHOTO = /\.(jpe?g|png|tiff?)$/i;
const TTL = 10 * 60 * 1000; // the folder listing is re-read at most every 10 minutes per worker instance
let memo = { at: 0, map: null };

// "SRS_6_T1 (62).JPG" -> "SRS_6_T1_62": the same rule as tools/media_webcopies.py stem_of()
function stemOf(title) {
  const base = title.replace(/\.[^.]+$/, '');
  return base.replace(/\s*\((\d+)\)/g, '_$1').replace(/ /g, '_');
}

function unescapeHtml(s) {
  return s.replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}

async function listFolder(id, map, depth) {
  const r = await fetch('https://drive.google.com/embeddedfolderview?id=' + encodeURIComponent(id));
  if (!r.ok) return;
  const html = await r.text();
  const files = /<a href="https:\/\/drive\.google\.com\/file\/d\/([\w-]+)\/view[^"]*"[^>]*>[\s\S]*?<div class="flip-entry-title">([\s\S]*?)<\/div>/g;
  let m;
  while ((m = files.exec(html))) {
    const title = unescapeHtml(m[2]);
    if (PHOTO.test(title)) map.set(stemOf(title), m[1]);
  }
  if (depth > 0) {
    const subs = [...html.matchAll(/href="https:\/\/drive\.google\.com\/drive\/folders\/([\w-]+)"/g)].map((x) => x[1]);
    await Promise.all(subs.map((s) => listFolder(s, map, depth - 1)));
  }
}

async function photoMap(env, fresh) {
  if (!fresh && memo.map && Date.now() - memo.at < TTL) return memo.map;
  const map = new Map();
  const roots = String(env.FOLDERS || '').split(',').map((s) => s.trim()).filter(Boolean);
  await Promise.all(roots.map((r) => listFolder(r, map, 2)));
  memo = { at: Date.now(), map };
  return map;
}

export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('Method not allowed', { status: 405 });
    const url = new URL(request.url);
    const stem = decodeURIComponent(url.pathname.replace(/^\/+/, '')).replace(/\.jpe?g$/i, '');
    if (!NAME.test(stem)) return new Response('Not found', { status: 404 });

    const cache = caches.default;
    const key = new Request(url.origin + '/' + stem + '.jpg');
    const hit = await cache.match(key);
    if (hit) return hit;

    let map = await photoMap(env, false);
    if (!map.has(stem)) map = await photoMap(env, true); // a photo added since the last listing
    const id = map.get(stem);
    if (!id) return new Response('This photo is not available yet.', { status: 404 });

    const up = await fetch('https://drive.usercontent.google.com/download?id=' + id + '&export=download&confirm=t');
    const type = up.headers.get('content-type') || '';
    if (!up.ok || !type.startsWith('image/')) {
      return new Response('The original is busy right now. Please try again in a few minutes.', { status: 503 });
    }
    const headers = new Headers({
      'Content-Type': type,
      'Content-Disposition': 'attachment; filename="' + stem + '.jpg"',
      'Cache-Control': 'public, max-age=31536000, immutable',
      'Access-Control-Allow-Origin': '*',
    });
    const len = up.headers.get('content-length');
    if (len) headers.set('Content-Length', len);
    const res = new Response(request.method === 'HEAD' ? null : up.body, { status: 200, headers });
    if (request.method === 'GET') ctx.waitUntil(cache.put(key, res.clone()));
    return res;
  },
};
