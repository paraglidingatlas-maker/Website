#!/usr/bin/env python3
"""
v4 catches up with the live site's work of 2 and 3 Oct 2026 (owner, 3 Oct:
"ok go", option 1 of the immersive list).

    python3 tools/v4_catchup.py

1. HOMEPAGE GLOBE. The live glass globe (globe.js, its world data and its
   episodes) as its own band between Listen and Join. The words are the live
   page's. The scripts are the live files, loaded only when the band comes
   near the screen (or at once for a #pin link), so the opening of the page
   carries none of their 470 KB. They sit in a <template> so build.sh still
   cache-busts them; the loader copies them out in order.

2. EPISODE SERIES MARK. The live episode header now carries the series'
   drawing beside the episode number. v4 already has the rest of that work
   in its own form (the header globe with the route from Oslo, the chapter
   timeline under the player), so it takes only the mark, drawn in v4's own
   Gold line (tools/v4_series_full.py, the library's tiles), linking to the
   series in the library.

3. SITEMAP NIGHT SKY. The live sitemap's sky (sitemap-sky.js, its data and
   its CSS) replaces v4's older branching graph. The page keeps v4's head,
   nav and footer; the sky section, the text index (inside <noscript>, as
   live) and the data come from the live page. Links in the data point at
   the v4 twin where there is one and at the live page otherwise, and the
   star thumbnails at the live images, so nothing depends on run time.

Every block sits between markers, so a rerun replaces it.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def put(html, start, end, block, before):
    """Replace start..end, or insert the block just before `before`."""
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    block = start + block + end
    if pat.search(html):
        return pat.sub(lambda m: block, html, count=1)
    if before not in html:
        raise SystemExit("v4_catchup: anchor not found: %s" % before[:60])
    return html.replace(before, block + "\n" + before, 1)


def live_globe_box():
    """The #epMap box exactly as the live homepage has it."""
    live = read(os.path.join(ROOT, "index.html"))
    m = re.search(r'(<div class="ep-map" id="epMap">.*?)\n  <p class="map-caption">', live, re.S)
    if not m:
        raise SystemExit("v4_catchup: live #epMap not found")
    box = m.group(1)
    # The popup's fallback link points at the library, which v4 has too.
    return box


GLOBE = """
<section id="map" class="kit-band v4-map" aria-labelledby="v4MapTitle">
  <div class="kit-in">
    <div class="kit-head">
      <span class="kit-kicker">A Map Of Every Place We've Ever Told A Story From</span>
      <h2 class="kit-title" id="v4MapTitle">Click A Pin, Hear The <em class="v2-accent">Story</em></h2>
    </div>
  %(box)s
  <p class="map-caption">Drag to rotate. Click a pin to see the episode.</p>
  </div>
  <template id="v4GlobeJs"><script src="../../assets/js/d3.min.js"></script><script src="../../globe-episodes.js"></script><script src="../../assets/js/globe-world.js"></script><script src="../../globe.js"></script></template>
  <script>
  (function(){
    var box=document.getElementById('epMap'),t=document.getElementById('v4GlobeJs');
    if(!box||!t)return;
    var done=false;
    function go(){
      if(done)return;done=true;
      var list=[].slice.call(t.content.querySelectorAll('script')).map(function(s){return s.getAttribute('src');});
      (function next(){
        var src=list.shift();if(!src)return;
        var s=document.createElement('script');s.src=src;s.onload=next;document.body.appendChild(s);
      })();
    }
    if(/^#pin/.test(location.hash)||!('IntersectionObserver' in window)){go();return;}
    var io=new IntersectionObserver(function(e){if(e[0].isIntersecting){io.disconnect();go();}},{rootMargin:'600px 0px'});
    io.observe(box);
  })();
  </script>
</section>
"""


def homepage_globe():
    p = os.path.join(V4, "index.html")
    html = read(p)
    html = put(html, "<!-- v4-globe -->", "<!-- /v4-globe -->",
               GLOBE % {"box": live_globe_box()},
               "<!-- ======================= PART 3: JOIN")
    write(p, html)
    print("v4_catchup: homepage globe")


EPNO = re.compile(r'(<div class="v4-epline">)?(?:<a class="v4-series"[^>]*>.*?</a>)*<p class="cd-epno">(.*?)</p>(?(1)</div>)', re.S)


def series_marks():
    import v4_series_full as F
    meta = {m["slug"]: m for m in json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))}
    cache, n = {}, 0
    d = os.path.join(V4, "episodes")
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"):
            continue
        m = meta.get(fn[:-5])
        series = (m or {}).get("series", "")
        if series not in F.CATS or not m.get("series_slug"):
            continue
        if series not in cache:
            svg = F.gold(series)
            svg = re.sub(r'\srole="img" aria-label="[^"]*"', ' aria-hidden="true" focusable="false"', svg, count=1)
            cache[series] = svg
        p = os.path.join(d, fn)
        html = read(p)
        mark = ('<a class="v4-series" href="../library.html#s=%s" aria-label="All of the %s series">%s</a>'
                % (m["series_slug"], series.replace("&", "&amp;"), cache[series]))
        new, k = EPNO.subn(lambda x: '<div class="v4-epline">' + mark + '<p class="cd-epno">' + x.group(2) + "</p></div>", html, count=1)
        if k and new != html:
            write(p, new)
            n += 1
    print("v4_catchup: series mark on %d episode pages" % n)


def sky_url(u, live_rel):
    """A link in the live sitemap's data, made to work from prototypes/v4/."""
    if not u or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/)", u):
        return u
    path, tail = re.match(r"([^?#]*)(.*)", u).groups()
    if os.path.exists(os.path.join(V4, path)):
        return u
    return "../../" + u


def sitemap_sky():
    live = read(os.path.join(ROOT, "sitemap.html"))
    p = os.path.join(V4, "sitemap.html")
    html = read(p)
    # the CSS: the live page's own block in place of the graph's
    lcss = re.search(r"<style>.*?</style>", live, re.S).group(0)
    html = re.sub(r"<style>.*?</style>", lambda m: lcss, html, count=1, flags=re.S)
    # the body: from v4's page header (or an earlier sky) to the end of the index
    body = re.search(r'<section class="sky">.*?</noscript>\n', live, re.S).group(0)
    start = re.search(r'<header class="kit-hero is-sky v2-page-hero">|<section class="sky">', html)
    end = html.index("</div><!-- /.page-wrap -->")
    html = html[:start.start()] + body + "\n" + html[end:]
    # the data: urls to the v4 twin or the live page, images to the live files
    data = re.search(r"<script>window\.SITEMAP_SKY = (.*?);?</script>", live, re.S).group(1)
    sky = json.loads(data)

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "url" and isinstance(v, str):
                    o[k] = sky_url(v, "")
                elif k == "img" and isinstance(v, str) and not v.startswith(("http", "/", "../")):
                    o[k] = "../../" + v
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(sky)
    tag = ("<script>window.SITEMAP_SKY = %s;</script>\n<script src=\"../../sitemap-sky.js\"></script>"
           % json.dumps(sky, ensure_ascii=False))
    html, k = re.subn(r"<script>window\.SITEMAP_(?:GRAPH|SKY) = .*?</script>\n<script src=\"\.\./\.\./sitemap-(?:graph|sky)\.js[^\"]*\"></script>",
                      lambda m: tag, html, count=1, flags=re.S)
    if not k:
        raise SystemExit("v4_catchup: sitemap data script not found")
    write(p, html)
    print("v4_catchup: sitemap night sky")


def main():
    homepage_globe()
    series_marks()
    sitemap_sky()


if __name__ == "__main__":
    main()
