<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;1,800;1,900&family=Barlow:wght@600;700&display=block" rel="stylesheet">
<style>
:root{--g:#006847;--r:#ce1126;--o:#ff7517;--ink:#0b1a14}
*{box-sizing:border-box;margin:0}
html,body{background:transparent;width:3840px;height:2160px;overflow:hidden}
.plate{position:absolute;left:220px;bottom:300px;display:flex;align-items:stretch;filter:drop-shadow(0 18px 40px rgba(0,0,0,.45))}
.tri{display:flex;gap:10px;margin-right:18px;transform:skewX(-16deg)}
.tri i{display:block;width:22px}
.tri i:nth-child(1){background:var(--g)}.tri i:nth-child(2){background:#fff}.tri i:nth-child(3){background:var(--r)}
.col{display:flex;flex-direction:column}
.top{display:flex;align-items:stretch;height:170px}
.name{background:#fff;color:#111;font:900 italic 150px/1 "Barlow Condensed";text-transform:uppercase;padding:0 52px 0 44px;display:flex;align-items:center;letter-spacing:.005em;white-space:nowrap}
.nat{background:var(--o);color:#111;display:flex;align-items:center;gap:26px;padding:0 44px;font:800 italic 96px/1 "Barlow Condensed"}
.nat img{height:78px;width:auto;border-radius:6px;box-shadow:0 0 0 3px rgba(0,0,0,.25)}
.sub{align-self:flex-start;background:rgba(11,26,20,.92);color:#fff;font:700 54px/1 "Barlow";letter-spacing:.16em;text-transform:uppercase;padding:22px 44px;display:flex;gap:28px;align-items:center}
.sub b{color:var(--o);font-weight:700}
.tag{align-self:flex-start;margin-bottom:14px;padding-left:22px;color:#fff;font:800 italic 52px/1 "Barlow Condensed";letter-spacing:.18em;text-transform:uppercase;text-shadow:0 4px 18px rgba(0,0,0,.6)}
.tag b{color:var(--o)}
</style></head><body>
<div class="plate"><div class="tri"><i></i><i></i><i></i></div>
 <div class="col"><div class="tag">Tapalpa <b>&middot;</b> SRS Advance Edition</div>
  <div class="top"><div class="name" id="n"></div><div class="nat"><img id="f"><span id="c"></span></div></div>
  <div class="sub" id="s"></div></div></div>
<script>
function set(p){document.getElementById('n').textContent=p.name;document.getElementById('f').src=p.flag;document.getElementById('c').textContent=p.ioc;
 var s=document.getElementById('s'); s.innerHTML=p.glider?('<span>'+p.glider+'</span>'):''; s.style.display=p.glider?'flex':'none';}
</script></body></html>
