/**
 * Paragliding Atlas — dedicated CORS proxy Worker
 *
 * Replaces the unreliable free public proxies (allorigins.win, corsproxy.io)
 * with an endpoint you actually own. Cloudflare's free tier gives 100,000
 * requests/day, and since this Worker isn't shared with random other
 * websites, there's no contention or time-of-day rate limiting.
 *
 * Locked down on purpose: only proxies the two specific feeds this site
 * needs (the podcast RSS feed and the YouTube channel feed), rejecting
 * everything else. This avoids becoming an open proxy that strangers could
 * discover and abuse, which would burn through your request quota.
 */

const ALLOWED_TARGETS = [
  'https://anchor.fm/s/ed1344d8/podcast/rss',
  'https://www.youtube.com/feeds/videos.xml?channel_id=UC0xDTfl8kurPl9CgpsLTr2Q',
];

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const target = url.searchParams.get('url');

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    if (!target || !ALLOWED_TARGETS.includes(target)) {
      return new Response('Forbidden: target URL not on the allowed list', {
        status: 403,
        headers: { 'Access-Control-Allow-Origin': '*' },
      });
    }

    try {
      const upstream = await fetch(target, {
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; ParaglidingAtlasBot/1.0)' },
      });
      const body = await upstream.text();

      return new Response(body, {
        status: upstream.status,
        headers: {
          'Content-Type': upstream.headers.get('Content-Type') || 'application/xml',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=300', // cache 5 minutes to reduce upstream load
        },
      });
    } catch (err) {
      return new Response('Upstream fetch failed: ' + err.message, {
        status: 502,
        headers: { 'Access-Control-Allow-Origin': '*' },
      });
    }
  },
};
