<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,800;1,800;1,900&family=Barlow:wght@600;700&display=block" rel="stylesheet">
<style>
:root{--g:#006847;--w:#ffffff;--r:#ce1126;--o:#ff7517;--pine:#0d2a1f}
*{box-sizing:border-box;margin:0}
body{width:1280px;height:720px;overflow:hidden;background:#000;font-family:"Barlow Condensed",sans-serif}
.t{position:relative;width:1280px;height:720px;overflow:hidden}
.bg{position:absolute;inset:0;background-size:cover;background-position:var(--pos,50% 45%);filter:saturate(1.15) contrast(1.05)}
.atlas{position:absolute;left:50%;bottom:-6px;width:520px;transform:translateX(-50%);filter:drop-shadow(0 4px 14px rgba(0,0,0,.6))}
.srs{position:absolute;left:34px;top:26px;width:150px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))}
.ed-old{position:absolute;right:34px;top:30px;height:96px;width:250px;border:2px dashed rgba(255,255,255,.7);color:#fff;display:grid;place-items:center;font:600 22px "Barlow",sans-serif;text-align:center;background:rgba(0,0,0,.25)}
.flag{position:absolute;left:0;bottom:30px;display:flex;align-items:center;gap:12px;background:#fff;color:#111;padding:8px 18px 8px 26px;font:800 34px "Barlow Condensed";letter-spacing:.02em}
.flag i{display:block;width:42px;height:28px;background:linear-gradient(90deg,var(--g) 33.3%,#fff 33.3% 66.6%,var(--r) 66.6%)}

/* A: F1 grid — slashes and a huge italic number */
.A .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,22,16,.92) 0%,rgba(6,22,16,.72) 34%,rgba(6,22,16,0) 62%),linear-gradient(0deg,rgba(6,22,16,.75),rgba(6,22,16,0) 40%)}
.A .slash{position:absolute;top:-40px;bottom:-40px;width:34px;transform:skewX(-18deg)}
.A .s1{left:690px;background:var(--g)} .A .s2{left:734px;background:#fff} .A .s3{left:778px;background:var(--r)}
.A .kick{position:absolute;left:40px;top:196px;color:#fff;font:800 italic 40px "Barlow Condensed";letter-spacing:.14em;text-transform:uppercase}
.A .kick b{color:var(--o)}
.A .big{position:absolute;left:30px;top:228px;color:#fff;font:900 italic 250px/.86 "Barlow Condensed";letter-spacing:-.02em;text-transform:uppercase;text-shadow:0 8px 30px rgba(0,0,0,.45)}
.A .big span{color:var(--o)}
.A .strip{position:absolute;left:40px;top:470px;display:flex;gap:0;font:800 34px "Barlow Condensed";text-transform:uppercase}
.A .strip div{padding:6px 16px;background:#fff;color:#111}
.A .strip div+div{background:var(--o);color:#111}

/* B: SailGP clean — full photo, one broadcast bar */
.B .shade{position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,22,16,.95) 0%,rgba(6,22,16,.5) 30%,rgba(6,22,16,0) 52%),linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,0) 22%)}
.B .bar{position:absolute;left:0;right:0;bottom:118px;height:150px;display:flex;align-items:stretch}
.B .num{width:300px;background:var(--o);color:#111;display:flex;align-items:center;justify-content:center;font:900 italic 128px/1 "Barlow Condensed";clip-path:polygon(0 0,100% 0,88% 100%,0 100%)}
.B .num small{font-size:48px;margin-right:8px;font-weight:800;align-self:center}
.B .txt{flex:1;display:flex;flex-direction:column;justify-content:center;padding-left:24px;color:#fff}
.B .txt b{font:900 italic 96px/.95 "Barlow Condensed";text-transform:uppercase;letter-spacing:.005em}
.B .txt span{font:700 30px "Barlow";letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.85)}
.B .tri{position:absolute;left:0;right:0;bottom:268px;height:10px;background:linear-gradient(90deg,var(--g) 0 33.3%,#fff 33.3% 66.6%,var(--r) 66.6%)}

.lock{position:absolute;right:34px;top:26px;display:flex;align-items:center;gap:22px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.55))}
.lock .l-srs{width:150px}
.lock i{display:block;width:3px;height:84px;background:rgba(255,255,255,.7)}
.lock .l-adv{display:flex;flex-direction:column;align-items:center;gap:6px;color:#fff;font:700 22px/1.05 "Barlow";letter-spacing:.32em;text-transform:uppercase;text-align:center}
.lock .l-adv img{width:84px}
.A2 .srs{display:none}
.A2 .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,34,24,.80) 0%,rgba(8,34,24,.58) 30%,rgba(8,34,24,.18) 48%,rgba(8,34,24,0) 58%),linear-gradient(0deg,rgba(8,30,22,.55),rgba(8,30,22,0) 32%)}
.A2 .slash{position:absolute;top:-40px;bottom:-40px;width:34px;transform:skewX(-18deg)}
.A2 .s1{left:690px;background:var(--g)} .A2 .s2{left:734px;background:#fff} .A2 .s3{left:778px;background:var(--r)}
.A2 .kick{position:absolute;left:40px;top:150px;color:#fff;font:800 italic 40px "Barlow Condensed";letter-spacing:.14em;text-transform:uppercase}
.A2 .kick b{color:var(--o)}
.A2 .big{position:absolute;left:30px;top:186px;color:#fff;font:900 italic 250px/.86 "Barlow Condensed";letter-spacing:-.02em;text-transform:uppercase;text-shadow:0 8px 30px rgba(0,0,0,.45)}
.A2 .big span{color:var(--o)}
.A2 .strip{position:absolute;left:40px;top:430px;display:flex;font:800 34px "Barlow Condensed";text-transform:uppercase}
.A2 .strip div{padding:6px 16px;background:#fff;color:#111}
.A2 .strip div+div{background:var(--o);color:#111}
</style></head><body>
<div class="t VAR">
  <div class="bg" style="background-image:url(PHOTO.jpg);--pos:POS"></div>
  <div class="shade"></div>
  BODY
  <img class="srs" src="srs.png">
  <div class="lock"><img src="srs.png" class="l-srs"><i></i><div class="l-adv"><img src="adv.svg"><span>Advance<br>Edition</span></div></div>
  <div class="flag"><i></i>MEX</div>
  <img class="atlas" src="atlas.png">
</div></body></html>
