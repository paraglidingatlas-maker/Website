#!/usr/bin/env python3
"""
The loading screen (owner, 28 Oct 2026: "yes push", after the designers' advice in docs/designers/D.md, E.md,
F.md): shown only when a page is slow, once a visit, never in the way of a page that has already arrived.

What a visitor sees, if the page has not finished loading half a second after it began:
  - a trip page (India, Kenya): the dark ground, the place's name in spaced capitals with one fact from the page,
    and one orange hairline drawing the place's real ridge (the skyline of its open elevation data, India's
    img/india/dem, Kenya's Kerio h-kerio), its length the page's real loaded share, the share as a small number at
    its tip; when the page is ready the screen opens up and down from the line onto the page (Panchgani has no
    elevation data here, so its line is a plain horizon; nothing is invented);
  - the home page: the opening's first place name ("KENYA") outlined, and the season line along the foot filling;
    the page then comes up behind it;
  - the podcast, the library and the episodes: one column a conversation (episode-meta.json, by date, as tall as
    it is long, as on the library page) growing from left to right with the load;
  - any other page: one hairline and the page's name.
Rules: nothing at all before 0.5 s, and nothing if the page is loaded by then; once shown it stays at least 0.9 s
so it never flashes; a tap skips it; at most once a visit (sessionStorage); it gives up after 8 s; reduced motion
shows it still and swaps in; without JavaScript there is none. The progress is the page's own: the images it
loads eagerly and its fonts, then 100 at the window's load.

It is a small inline style and script at the top of every v4 page's head (between <!--v4ld--> marks, written
again on every run, so the build stays byte-identical), with the page's own settings as JSON. Run by
tools/v4_build.py after tools/v4_library_live.py.

    python3 tools/v4_loader.py
"""
import datetime
import glob
import html
import json
import os
import re

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(ROOT, "prototypes", "v4")
MARK = ("<!--v4ld-->", "<!--/v4ld-->")

TRIPS = {
    "destinations/india.html": ("Bir Billing, India", "The Dhauladhar · launch about 2,400 m", "img/india/dem/h-1k.png"),
    "destinations/kenya.html": ("Kerio Valley, Kenya", "Thermals to 6 m/s · 1,500 m above ground", "img/kenya/dem/h-kerio-1k.png"),
    "destinations/panchgani.html": ("Panchgani, India", "Take-off at about 1,100 to 1,200 m", None),
}
LISTEN = ("podcast.html", "library.html", "library-live.html")

CSS = (".v4ld{position:fixed;inset:0;z-index:2147483000;color:#f6f4f4;opacity:0;transition:opacity .3s cubic-bezier(.16,1,.3,1)}"
       ".v4ld.on{opacity:1}.v4ld svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}"
       ".v4ld-a,.v4ld-b{position:absolute;left:0;right:0;background:#141519;transition:transform .75s cubic-bezier(.16,1,.3,1)}"
       ".v4ld-a{top:0}.v4ld-b{bottom:0}.v4ld.open .v4ld-a{transform:translateY(-101%)}.v4ld.open .v4ld-b{transform:translateY(101%)}"
       ".v4ld svg,.v4ld-n,.v4ld-p,.v4ld-w{transition:opacity .35s}.v4ld.open svg,.v4ld.open .v4ld-n,.v4ld.open .v4ld-p,.v4ld.open .v4ld-w{opacity:0}"
       ".v4ld-n{position:absolute;left:0;right:0;top:27%;text-align:center;padding:0 16px;font:500 12px/1 'DM Mono',ui-monospace,monospace;"
       "letter-spacing:.5em;text-indent:.5em;text-transform:uppercase}"
       ".v4ld-n small{display:block;margin-top:1.1em;font-size:10px;letter-spacing:.32em;text-indent:.32em;color:#8d8c92}"
       ".v4ld-p{position:absolute;font:11px/1 'DM Mono',ui-monospace,monospace;letter-spacing:.08em;color:#c9c7cc;"
       "transform:translate(10px,-170%);font-variant-numeric:tabular-nums;white-space:nowrap}.v4ld-p i{font-style:normal;color:#8d8c92}"
       ".v4ld-w{position:absolute;left:0;right:0;top:12%;text-align:center;font:800 min(25vw,23rem)/1 Poppins,system-ui,sans-serif;"
       "letter-spacing:-.02em;color:transparent;-webkit-text-stroke:1px rgba(246,244,244,.32);white-space:nowrap}"
       "@media (max-width:700px){.v4ld-w{top:18%}}")

JS = r"""(function(){var d=document,w=window,C=JSON.parse(d.getElementById("v4ld-c").textContent);
try{if(sessionStorage.getItem("v4ld"))return}catch(e){}
var done=false,shown=false,el,t0,raf=0,P=0,reduce=w.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
w.addEventListener("load",function(){done=true});
function share(){if(done)return 1;var im=d.images,n=0,k=0;for(var i=0;i<im.length;i++){if(im[i].loading=="lazy")continue;n++;if(im[i].complete)k++}
 var f=d.fonts&&d.fonts.status=="loaded"?1:0;return Math.min(.97,(k+f+(d.readyState!="loading"?1:0))/(n+2))}
function ns(t,a){var e=d.createElementNS("http://www.w3.org/2000/svg",t);for(var k in a)e.setAttribute(k,a[k]);return e}
function show(){if(done||d.readyState=="complete")return;shown=true;try{sessionStorage.setItem("v4ld","1")}catch(e){}
 el=d.createElement("div");el.className="v4ld";el.setAttribute("role","status");el.setAttribute("aria-label","Loading");
 var W=1000,H=600,s=ns("svg",{viewBox:"0 0 1000 600",preserveAspectRatio:"none","aria-hidden":"true"}),line,len=0,cols=[],tipY=360,x0=0,x1=1000;
 if(C.k=="trip"){var pts=C.r||[],dd="";if(pts.length){for(var i=0;i<pts.length;i++)dd+=(i?"L":"M")+(i/(pts.length-1)*1000).toFixed(1)+" "+(400-pts[i]*150).toFixed(1)}else dd="M0 360L1000 360";
  line=ns("path",{d:dd,fill:"none",stroke:"#ff7517","stroke-width":"1.2","stroke-linejoin":"round"});s.appendChild(line)}
 else if(C.k=="home"){tipY=560;x0=50;x1=950;s.appendChild(ns("line",{x1:50,y1:560,x2:950,y2:560,stroke:"rgba(246,244,244,.14)","vector-effect":"non-scaling-stroke"}));
  line=ns("line",{x1:50,y1:560,x2:50,y2:560,stroke:"#ff7517","stroke-width":"1.4","vector-effect":"non-scaling-stroke"});s.appendChild(line)}
 else if(C.k=="listen"){tipY=520;x0=60;x1=940;s.appendChild(ns("line",{x1:60,y1:520,x2:940,y2:520,stroke:"rgba(246,244,244,.14)","vector-effect":"non-scaling-stroke"}));
  (C.c||[]).forEach(function(c){var l=ns("line",{x1:60+c[0]*880,x2:60+c[0]*880,y1:520,y2:520,stroke:"#ff7517","stroke-width":"1.2","vector-effect":"non-scaling-stroke"});l._h=c[1];l._x=60+c[0]*880;s.appendChild(l);cols.push(l)})}
 else{tipY=360;x0=300;x1=700;line=ns("line",{x1:300,y1:360,x2:300,y2:360,stroke:"#ff7517","stroke-width":"1.4","vector-effect":"non-scaling-stroke"});s.appendChild(line)}
 var cut=(C.k=="trip"?400:tipY)/6,A=d.createElement("div"),B=d.createElement("div");A.className="v4ld-a";B.className="v4ld-b";A.style.height=cut+"%";B.style.height=(100-cut)+"%";el.appendChild(A);el.appendChild(B);
 el.appendChild(s);
 if(C.k=="home"&&C.w){var wd=d.createElement("div");wd.className="v4ld-w";wd.setAttribute("aria-hidden","true");wd.textContent=C.w;el.appendChild(wd)}
 var nm=d.createElement("div");nm.className="v4ld-n";nm.textContent=C.n;if(C.f){var sm=d.createElement("small");sm.textContent=C.f;nm.appendChild(sm)}if(C.k!="home")el.appendChild(nm);
 var pc=d.createElement("div");pc.className="v4ld-p";pc.setAttribute("aria-hidden","true");el.appendChild(pc);
 (d.body||d.documentElement).appendChild(el);if(line&&line.getTotalLength&&C.k=="trip"){len=line.getTotalLength();line.style.strokeDasharray=len;line.style.strokeDashoffset=len}
 el.addEventListener("click",out);requestAnimationFrame(function(){el.classList.add("on")});t0=performance.now();
 function frame(now){var a=share();P=reduce?a:P+(a-P)*.12;if(done&&P>.995)P=1;var x;
  if(C.k=="trip"){line.style.strokeDashoffset=(len*(1-P)).toFixed(1);var pt=line.getPointAtLength(len*P);x=pt.x;tipY=pt.y}
  else if(C.k=="listen"){x=x0+(x1-x0)*P;cols.forEach(function(l){var k=Math.max(0,Math.min(1,(x-l._x)/80));l.setAttribute("y2",(520-l._h*170*(1-Math.pow(1-k,3))).toFixed(1))})}
  else{x=x0+(x1-x0)*P;line.setAttribute("x2",x.toFixed(1))}
  pc.style.left=(x/10)+"%";pc.style.top=(tipY/6)+"%";pc.innerHTML=Math.round(P*100)+"<i>%</i>";
  if((P>=1&&now-t0>900)||now-t0>8000){out();return}raf=requestAnimationFrame(frame)}
 raf=requestAnimationFrame(frame)}
function out(){if(!el||el._out)return;el._out=1;cancelAnimationFrame(raf);
 if(reduce)el.classList.remove("on");else el.classList.add("open");setTimeout(function(){if(el&&el.parentNode)el.parentNode.removeChild(el)},reduce?350:850)}
setTimeout(show,500)})();"""


def skyline(path, n=120):
    a = np.asarray(Image.open(os.path.join(V4, path))).astype(float)
    h = a[..., 0] * 256 + a[..., 1]
    col = h.max(0)                                    # the highest ground down each column: the range seen from the south
    v = np.interp(np.linspace(0, len(col) - 1, n), np.arange(len(col)), col)
    v = np.convolve(np.pad(v, 1, mode="edge"), np.ones(3) / 3, "valid")
    return [round(float(x), 3) for x in (v - v.min()) / (v.max() - v.min())]


def columns():
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    rows = []
    for e in meta:
        m = int(re.sub(r"\D", "", e.get("duration_label", "") or "") or 0)
        try:
            day = datetime.date.fromisoformat(e.get("published", "")[:10])
        except ValueError:
            continue
        if m:
            rows.append((day, m))
    t0, t1 = min(r[0] for r in rows), max(r[0] for r in rows)
    top = max(r[1] for r in rows)
    span = max(1, (t1 - t0).days)
    return [[round((day - t0).days / span, 4), round(m / top, 3)] for day, m in sorted(rows)]


def config(rel, src, cache):
    if rel in TRIPS:
        n, f, dem = TRIPS[rel]
        c = {"k": "trip", "n": n, "f": f}
        if dem:
            c["r"] = cache.setdefault(dem, skyline(dem))
        return c
    if rel == "index.html":
        m = re.search(r'<span class="w"[^>]*>(.*?)</span>', src, re.S)
        word = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
        return {"k": "home", "n": "Paragliding Atlas", "w": word}
    if rel in LISTEN or rel.startswith("episodes/"):
        rows = len(re.findall(r'class="v4l-row"', open(os.path.join(V4, "library-live.html"), encoding="utf-8").read()))
        return {"k": "listen", "n": "The Paragliding Atlas Podcast", "f": "%d conversations" % rows if rows else "",
                "c": cache.setdefault("cols", columns())}
    m = re.search(r'<meta property="og:title" content="([^"]*)"', src) or re.search(r"<title>([^<|:]*)", src)
    name = html.unescape(m.group(1)).strip() if m else "Paragliding Atlas"
    return {"k": "page", "n": name}


def main():
    cache, n = {}, 0
    for path in sorted(glob.glob(os.path.join(V4, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(path, V4).replace(os.sep, "/")
        src = open(path, encoding="utf-8").read()
        clean = re.sub(re.escape(MARK[0]) + r".*?" + re.escape(MARK[1]) + r"\n?", "", src, flags=re.S)
        block = (MARK[0] + "<style>" + CSS + "</style><script type=\"application/json\" id=\"v4ld-c\">"
                 + json.dumps(config(rel, clean, cache), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
                 + "</script><script>" + JS + "</script>" + MARK[1] + "\n")
        m = re.search(r'<meta charset="UTF-8">\n', clean)
        if not m:
            continue
        out = clean[:m.end()] + block + clean[m.end():]
        if out != src:
            open(path, "w", encoding="utf-8").write(out)
        n += 1
    print("v4 loader: the loading screen on %d pages" % n)


if __name__ == "__main__":
    main()
